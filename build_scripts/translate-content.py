#!/usr/bin/env python
"""
Translate documentation content with Translated's AI translation (TranslationOS POST /translate/ai).

English sources live in content/; translations land at localizedContent/{lang}/content/{same
path} and arrive as review PRs on the `localization` branch (.github/workflows/translate.yml).
The endpoint is synchronous: one POST per file and language returns the translation (billed
per character), so nothing is pending between runs. Every delivery is repaired against the
English source (code, markers, link targets restored), verified, and written in the same step.

An outdated translation is updated from changed segments only: the English version it was made
from (status `sourceBlob`, verified against `sourceHash`) is diffed block by block against the
current English (translation_segments.py), unchanged blocks are kept from the translation and
only changed blocks, JSON keys or toc names are sent. Missing files, unaligned translations and
files whose text mostly changed are sent whole.

Actions (exactly one per invocation):
  --plan         list missing/outdated/orphaned/pinned/unscoped files (offline)
  --run          translate every missing/outdated file, verify and write the results
  --baseline     seed the status file from the existing translations (offline)
  --migrate-blobs  record sourceBlob for status entries that only have a sourceHash (offline)
  --merge-status OURS THEIRS  rebuild the status files entry by entry after merging a translation branch (offline)
  --self-test    offline test suite (no key, no network)
  --probe        check service types and languages against the API
  --dump-orders  write the exact request bodies to a directory instead of sending

Scope comes from the "translation" section of metadata/build-config.json, locales from
"translatedLocale" in metadata/language-metadata.json; target languages are the folders
under localizedContent/ with a content/ directory.

Environment: TRANSLATED_ENV (sandbox | production; the sandbox account has no AI-enabled
service type, so only production can run), TRANSLATED_API_KEY, and
TRANSLATED_SERVICE_TYPE (optional override; both environments default to 'AI') and
TRANSLATED_CONTEXT_SEGMENTS (optional override of translation.segmentDiff.contextSegments).

Exit code 1 on configuration errors or failed API requests. A rejected API key (401/403) stops
the run and records nothing for the file. Any other failed request is recorded under "failures"
and planned again by the next run. Files whose delivery fails verification do not fail the run:
they are recorded under "failures" and skipped until the English changes or --retry-failed, and
--keep-rejected saves the billed delivery. Full reference: README.md > Translating Content.
"""

from __future__ import annotations

import argparse
import difflib
import email.utils
import fnmatch
import hashlib
import http.client
import io
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import uuid
from collections import Counter
from collections.abc import Callable, Iterator
from contextlib import contextmanager, redirect_stdout
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol

from config_loader import compute_file_hash, get_default_language, load_build_config
from translation_segments import (
    ACTION_ENGLISH,
    ACTION_REPAIR,
    ACTION_REUSE,
    ACTION_TRANSLATE,
    KIND_HEADING,
    KIND_LIST_ITEM,
    LIST_ITEM_RE,
    Action,
    Block,
    context_indices,
    diff_blocks,
    reused_layout,
    segment,
)

CONTENT_DIR = Path("content")
LOCALIZED_DIR = Path("localizedContent")
STATUS_FILENAME = ".translation-status.json"
LANGUAGE_METADATA_PATH = Path("metadata/language-metadata.json")

STATUS_TRANSLATED = "translated"
STATUS_UNTRANSLATED = "untranslated"
STATUS_OUTDATED = "outdated"
STATUS_COPIED = "copied"

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

RETRYABLE_HTTP = frozenset({408, 425, 429, 500, 502, 503, 504})
AUTH_HTTP = frozenset({401, 403})
MAX_RETRY_DELAY = 60.0
REPORT_LIST_CAP = 50
IDENTITY_MIN_LETTERS = 200
REPAIR_KINDS = ("fences", "inline code", "markers", "links")  # order used in "repaired: ..." lines
WARNING_KINDS = frozenset({"inline code"})  # count mismatches of these kinds are warnings, not problems

# /translate/ai accepts text/plain and text/html but rejects text/markdown and
# application/json, so everything non-HTML is sent as text/plain.
CONTENT_TYPES = {
    ".md": "text/plain",
    ".html": "text/html",
    ".htm": "text/html",
    ".json": "text/plain",
    ".yml": "text/plain",  # toc.yml is sent as a JSON map of its `name` values, see extract_yaml_names
    ".yaml": "text/plain",
}

BOM = "﻿"
WHOLE_FILE_TYPE = "file type is translated whole"

# Markdown structure regexes (mirror normalize-localized-heading-anchors.py).
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
HEADING_RE = re.compile(r"^#{1,6}\s+\S")
HEADING_MARKS_RE = re.compile(r"^#{1,6}(?=[ \t])")
# Any `[!word` token: alert markers ([!NOTE]), includes ([!include[...]) and code refs ([!code-yaml[...]).
# Deliberately broad so a translated marker ([!NOTA]) is still counted and restored positionally.
ALERT_RE = re.compile(r"\[![A-Za-z][A-Za-z0-9-]*")
LINK_TARGET_RE = re.compile(r"\]\(([^)\s]+)")
INLINE_CODE_RE = re.compile(r"(`+)(?!`)[^`\n]+?\1(?!`)")
FRONTMATTER_RE = re.compile(r"\A(﻿)?---\r?\n(.*?)\r?\n---[ \t]*\r?\n", re.S)
FM_TRANSLATABLE_RE = re.compile(r"^(title|description):[ \t]*(.*?)[ \t]*$")
YAML_NAME_RE = re.compile(r"^(\s*-?\s*name:[ \t]*)(.*?)[ \t]*$")
YAML_NAME_KEY_RE = re.compile(r"n\d+")
YAML_SPECIAL_RE = re.compile(r"[:#\[\]{},&*!|>'\"%@`]")
YAML_INDICATOR_START = tuple("-?*&!%@`|>'\"[{:,]}#")
YAML_SCALARS = frozenset({"true", "false", "yes", "no", "null", "on", "off", "~"})
HTML_TAG_RE = re.compile(r"<\s*([a-zA-Z][a-zA-Z0-9-]*)")
HTML_REF_RE = re.compile(r"""\b(?:href|src)\s*=\s*["']([^"']+)["']""")
# Bookmark anchors that build-docs (normalize-localized-heading-anchors.py) injects into a local tree.
INJECTED_ANCHOR_RE = re.compile(r'^<a id="[^"]*" data-loc-xref></a>\n', re.M)
TOC_HREF_RE = re.compile(r"^\s*href:[ \t]*(.*?)[ \t]*$")
# {{cN}} (inline code) and {{fN}} (fenced block) placeholders; quotation marks the service puts
# around one are matched so they can be dropped.
CODE_TOKEN_RE = re.compile(r"([«“\"‘「『]?)\{\{\s*([cf])(\d+)\s*\}\}([»”\"’」』]?)")
QUOTE_PAIRS = {"«": "»", "“": "”", '"': '"', "‘": "’", "「": "」", "『": "』"}
PLACEHOLDER_RE = re.compile(r"(?<!\{)\{([a-zA-Z_][a-zA-Z0-9_]*)\}(?!\})")
ENCODED_PLACEHOLDER_RE = re.compile(r"\{\{([a-zA-Z_][a-zA-Z0-9_]*)\}\}")


def utc_now() -> str:
    return datetime.now(UTC).strftime(TIMESTAMP_FORMAT)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


def normalize_base_url(url: str) -> str:
    """Accept https://host, https://host/v2 and https://host/v2/; always return .../v2/."""
    url = url.strip().rstrip("/")
    if not url.endswith("/v2"):
        url += "/v2"
    return url + "/"


def _patterns(items: Any) -> list[str]:
    return [s["pattern"] if isinstance(s, dict) else str(s) for s in (items or [])]


class TranslationConfig:
    def __init__(
        self,
        build_config: dict[str, Any],
        environment: str | None = None,
        service_type_override: str | None = None,
        context_segments_override: str | None = None,
    ) -> None:
        section = build_config.get("translation")
        if not section:
            raise SystemExit("metadata/build-config.json has no 'translation' section.")
        self.environments: dict[str, dict[str, Any]] = section.get("environments") or {}
        if not self.environments:
            raise SystemExit("translation.environments in metadata/build-config.json is empty.")
        self.environment: str | None = (environment or "").strip() or None
        env_def = self.environments.get(self.environment) if self.environment else None
        self.base_url: str | None = normalize_base_url(str(env_def["baseUrl"])) if env_def else None
        override = (service_type_override or "").strip()
        env_service = (env_def or {}).get("serviceType")
        self.service_type: str | None = override or (str(env_service) if env_service else None)
        self.source_locale: str = section.get("sourceLocale", "en-US")
        self.sources: list[str] = _patterns(section.get("sources"))
        self.passthrough: list[str] = _patterns(section.get("passthrough"))
        self.ignore: list[str] = _patterns(section.get("ignore"))
        self.instructions: str = section.get("instructions", "")
        limits = section.get("sandboxLimits") or {}
        self.max_files_per_run: int = int(limits.get("maxFilesPerRun", 20))
        self.max_chars_per_run: int = int(limits.get("maxCharsPerRun", 200000))
        segment_diff = section.get("segmentDiff") or {}
        self.segment_diff: bool = bool(segment_diff.get("enabled", True))
        self.max_changed_ratio: float = float(segment_diff.get("maxChangedRatio", 0.8))
        context = (context_segments_override or "").strip() or segment_diff.get("contextSegments", 2)
        try:
            self.context_segments: int = int(context)
        except ValueError:
            raise SystemExit(
                f"Context segments must be an integer (-1 = whole page, 0 = none), got {context!r} "
                "(TRANSLATED_CONTEXT_SEGMENTS or translation.segmentDiff.contextSegments)."
            ) from None
        self.shared_directories: list[str] = list(build_config.get("sharedDirectories", {}).get("directories", []))
        if not self.sources:
            raise SystemExit("translation.sources in metadata/build-config.json is empty.")

    @property
    def is_sandbox(self) -> bool:
        return self.environment == "sandbox"

    @property
    def environment_label(self) -> str:
        return self.environment or "unset"

    def require_network(self, action: str, need_service_type: bool = True) -> None:
        """Refuse any API call until the environment is unambiguous."""
        known = ", ".join(sorted(self.environments))
        if not self.environment:
            raise SystemExit(f"{action} needs TRANSLATED_ENV set to one of: {known}.")
        if self.environment not in self.environments:
            raise SystemExit(
                f"TRANSLATED_ENV='{self.environment}' is not defined in translation.environments ({known})."
            )
        if need_service_type and not self.service_type:
            raise SystemExit(
                f"No service type is configured for environment '{self.environment}'. Run --probe to list the "
                "account's service types, then set TRANSLATED_SERVICE_TYPE (or translation.environments."
                f"{self.environment}.serviceType in metadata/build-config.json)."
            )


def load_locale_map(path: Path = LANGUAGE_METADATA_PATH) -> dict[str, str]:
    """Map two-letter folder code -> Translated locale (RFC 3066, e.g. es -> es-ES)."""
    with open(path, encoding="utf-8") as f:
        meta = json.load(f)
    languages = meta.get("languages", meta)
    return {
        code: str(entry["translatedLocale"])
        for code, entry in languages.items()
        if isinstance(entry, dict) and entry.get("translatedLocale")
    }


def require_locales(langs: list[str], locales: dict[str, str]) -> None:
    missing = [lang for lang in langs if not locales.get(lang)]
    if missing:
        raise SystemExit(
            f"No translatedLocale for {', '.join(missing)} in {LANGUAGE_METADATA_PATH}; "
            'add e.g. "translatedLocale": "xx-XX" to each language entry.'
        )


def get_target_languages(default_lang: str) -> list[str]:
    if not LOCALIZED_DIR.exists():
        return []
    return sorted(
        p.name for p in LOCALIZED_DIR.iterdir() if p.is_dir() and p.name != default_lang and (p / "content").is_dir()
    )


# ---------------------------------------------------------------------------
# Source discovery
# ---------------------------------------------------------------------------


def rel_str(path: Path, base: Path) -> str:
    return str(path.relative_to(base)).replace("\\", "/")


def _glob_content(patterns: list[str], shared: set[str], ignore: list[str]) -> dict[str, str]:
    files: dict[str, str] = {}
    for pattern in patterns:
        for path in sorted(CONTENT_DIR.glob(pattern)):
            if not path.is_file():
                continue
            rel = rel_str(path, CONTENT_DIR)
            if rel.split("/", 1)[0] in shared or any(fnmatch.fnmatch(rel, ig) for ig in ignore):
                continue
            files[rel] = compute_file_hash(path)
    return files


def get_scoped_sources(config: TranslationConfig) -> dict[str, str]:
    """Return {relative path -> sha256} for every English file in translation scope.
    A file matched by a passthrough pattern is never in scope, even when a source pattern matches it."""
    shared = set(config.shared_directories)
    passthrough = _glob_content(config.passthrough, shared, config.ignore)
    return {rel: h for rel, h in _glob_content(config.sources, shared, config.ignore).items() if rel not in passthrough}


def get_passthrough_sources(config: TranslationConfig, sources: dict[str, str]) -> dict[str, str]:
    """Files copied verbatim from English (e.g. whats-new/*.html); never sent for translation."""
    found = _glob_content(config.passthrough, set(config.shared_directories), config.ignore)
    return {rel: h for rel, h in found.items() if rel not in sources}


def hash_bytes(data: bytes) -> str:
    """Same normalization as config_loader.compute_file_hash (CRLF -> LF)."""
    return "sha256:" + hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


GitRunner = Callable[[list[str]], subprocess.CompletedProcess[bytes]]


def run_git(cmd: list[str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(cmd, capture_output=True)


def resolve_git_ref(ref: str, run: GitRunner = run_git) -> str:
    """Return the commit sha `ref` names, or raise SystemExit when this clone does not have it."""
    proc = run(["git", "rev-parse", "--verify", "--quiet", "--end-of-options", f"{ref}^{{commit}}"])
    if proc.returncode != 0:
        raise SystemExit(f"--baseline-ref {ref} is not a commit in this clone (fetch it or check the spelling)")
    return proc.stdout.decode("utf-8", errors="replace").strip()


def hashes_at_git_ref(ref: str, rel_paths: list[str], run: GitRunner = run_git) -> dict[str, str]:
    """Hash content/{rel} as it was at a git ref. Missing files are omitted."""
    result: dict[str, str] = {}
    for rel in rel_paths:
        proc = run(["git", "show", f"{ref}:{CONTENT_DIR.as_posix()}/{rel}"])
        if proc.returncode == 0:
            result[rel] = hash_bytes(proc.stdout)
    return result


_WORK_TREE: dict[str, bool] = {}


def in_git_work_tree(run: GitRunner = run_git) -> bool:
    cwd = os.getcwd()
    if run is run_git and cwd in _WORK_TREE:
        return _WORK_TREE[cwd]
    proc = run(["git", "rev-parse", "--is-inside-work-tree"])
    inside = proc.returncode == 0 and proc.stdout.strip() == b"true"
    if run is run_git:
        _WORK_TREE[cwd] = inside
    return inside


def read_git_blob(blob: str, run: GitRunner = run_git) -> bytes | None:
    proc = run(["git", "cat-file", "blob", blob])
    return proc.stdout if proc.returncode == 0 else None


def git_stdout(proc: subprocess.CompletedProcess[bytes]) -> str | None:
    out = proc.stdout.decode("utf-8", errors="replace").strip()
    return out if proc.returncode == 0 and out else None


def current_source_blob(rel: str, source_hash: str, run: GitRunner = run_git) -> str | None:
    """Git blob id of content/{rel} when the file's hash is `source_hash`; None outside a git work tree."""
    path = CONTENT_DIR / rel
    if not path.exists() or hash_bytes(path.read_bytes()) != source_hash or not in_git_work_tree(run):
        return None
    # -w stores the blob, so an uncommitted English version stays readable as the base of the next diff.
    return git_stdout(run(["git", "hash-object", "-w", "--", path.as_posix()]))


def blob_at_git_ref(sha: str, rel: str, run: GitRunner = run_git) -> str | None:
    return git_stdout(run(["git", "rev-parse", "--verify", "--quiet", f"{sha}:{CONTENT_DIR.as_posix()}/{rel}"]))


def find_source_blob(rel: str, source_hash: str, run: GitRunner = run_git) -> tuple[str, bytes] | None:
    """The English version of content/{rel} whose hash is `source_hash`: the working file when it
    matches, else the newest committed version that does. Returns (blob id, content)."""
    if not source_hash:
        return None
    current = current_source_blob(rel, source_hash, run)
    if current:
        return current, (CONTENT_DIR / rel).read_bytes()
    if not in_git_work_tree(run):
        return None
    proc = run(["git", "log", "--no-abbrev", "--format=", "--raw", "--", f"{CONTENT_DIR.as_posix()}/{rel}"])
    if proc.returncode != 0:
        return None
    seen: set[str] = set()
    for line in proc.stdout.decode("utf-8", errors="replace").splitlines():
        # :100644 100644 <old blob> <new blob> M<TAB>path
        parts = line.split()
        if len(parts) < 5 or not parts[0].startswith(":") or not parts[3].strip("0") or parts[3] in seen:
            continue
        seen.add(parts[3])
        data = read_git_blob(parts[3], run)
        if data is not None and hash_bytes(data) == source_hash:
            return parts[3], data
    return None


def recorded_source_text(rel: str, entry: dict[str, Any], run: GitRunner = run_git) -> str | None:
    """The English text an existing translation was made from: the entry's sourceBlob when its
    content still hashes to sourceHash, else the version found by find_source_blob."""
    source_hash = str(entry.get("sourceHash") or "")
    if not source_hash:
        return None
    blob = entry.get("sourceBlob")
    if isinstance(blob, str) and blob:
        data = read_git_blob(blob, run)
        if data is not None and hash_bytes(data) == source_hash:
            return data.decode("utf-8")
    found = find_source_blob(rel, source_hash, run)
    return found[1].decode("utf-8") if found else None


def source_entry(
    rel: str, source_hash: str, status_value: str, run: GitRunner = run_git, blob: str | None = None
) -> dict[str, Any]:
    """A status entry; sourceBlob is recorded when the English version is in git (the base of the next diff)."""
    entry: dict[str, Any] = {"sourceHash": source_hash}
    blob = blob or current_source_blob(rel, source_hash, run)
    if blob:
        entry["sourceBlob"] = blob
    entry["status"] = status_value
    return entry


def matches_filters(rel: str, file_filters: list[str]) -> bool:
    return not file_filters or any(fnmatch.fnmatch(rel, pat) for pat in file_filters)


# ---------------------------------------------------------------------------
# Status file (read by sync-localized-content.py; written only here)
# ---------------------------------------------------------------------------


def status_path(lang: str) -> Path:
    return LOCALIZED_DIR / lang / STATUS_FILENAME


def load_status(lang: str) -> dict[str, Any]:
    path = status_path(lang)
    if path.exists():
        with open(path, encoding="utf-8") as f:
            status: dict[str, Any] = json.load(f)
    else:
        status = {"language": lang, "sourceBaseline": str(CONTENT_DIR), "files": {}}
    status.setdefault("files", {})
    status.setdefault("failures", {})
    # Legacy key from the old asynchronous flow.
    status.pop("pendingJobs", None)
    return status


def summarize_status(status: dict[str, Any]) -> dict[str, Any]:
    files = status["files"]
    counts = Counter(str(f.get("status")) for f in files.values())
    total = len(files)
    done = counts[STATUS_TRANSLATED] + counts[STATUS_COPIED]
    return {
        "translated": counts[STATUS_TRANSLATED],
        "outdated": counts[STATUS_OUTDATED],
        "untranslated": counts[STATUS_UNTRANSLATED],
        "copied": counts[STATUS_COPIED],
        "pinned": sum(1 for f in files.values() if f.get("manual") is True),
        "total": total,
        "completionPercent": round(done / total * 100, 1) if total else 0,
        "failures": len(status["failures"]),
    }


def save_status(lang: str, status: dict[str, Any]) -> None:
    # Case-insensitive so Windows and Linux runs order the file identically (stable diffs).
    status["files"] = dict(sorted(status["files"].items(), key=lambda kv: kv[0].lower()))
    status["summary"] = summarize_status(status)
    # Keep the optional section out of the file when empty so diffs stay small.
    if not status["failures"]:
        status.pop("failures")
    path = status_path(lang)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(status, f, indent=2, ensure_ascii=False)
        f.write("\n")
    status.setdefault("failures", {})


def record_failure(status: dict[str, Any], rel: str, error: str, source_hash: str, **extra: Any) -> None:
    entry: dict[str, Any] = {"error": error, "at": utc_now(), "sourceHash": source_hash}
    entry.update({k: v for k, v in extra.items() if v is not None})
    status["failures"][rel] = entry


# ---------------------------------------------------------------------------
# Content extraction / repair / verification
# ---------------------------------------------------------------------------


def read_text(path: Path) -> str:
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def to_lf(text: str) -> str:
    return text.replace("\r\n", "\n")


def yaml_scalar(value: str, source_value: str | None = None) -> str:
    """Return `value` as a YAML plain or quoted scalar. A value identical to the source's is
    kept verbatim (the source already parses); anything YAML could misread is JSON-quoted."""
    value = value.strip()
    if source_value is not None and value == source_value.strip():
        return source_value.strip()
    if value.startswith('"') and value.endswith('"') and len(value) >= 2:
        try:
            json.loads(value)
        except json.JSONDecodeError:
            return json.dumps(value, ensure_ascii=False)
        return value
    if re.fullmatch(r"'(?:[^']|'')*'", value):
        return value
    needs_quotes = (
        not value
        or value.lower() in YAML_SCALARS
        or value.startswith(YAML_INDICATOR_START)
        or ": " in value
        or " #" in value
        or value.endswith(":")
        or YAML_SPECIAL_RE.search(value) is not None
    )
    return json.dumps(value, ensure_ascii=False) if needs_quotes else value


def yaml_name_map(text: str) -> dict[str, str]:
    names: dict[str, str] = {}
    for i, line in enumerate(to_lf(text.lstrip(BOM)).split("\n")):
        m = YAML_NAME_RE.match(line)
        if m and m.group(2):
            names[f"n{i}"] = m.group(2)
    return names


def extract_yaml_names(text: str) -> tuple[str, int]:
    """toc.yml: only `name:` values are translatable. Send them as a JSON object so
    hrefs, homepage paths and structure never reach the translator."""
    names = yaml_name_map(text)
    return json.dumps(names, ensure_ascii=False, indent=2), len(names)


def reinsert_yaml_names(source_text: str, translated_json: str) -> tuple[str, list[str]]:
    """Rebuild toc.yml from the English source with translated `name:` values.
    Returns (text, problems); on problems the text is the source."""
    try:
        names = json.loads(translated_json.lstrip(BOM))
    except json.JSONDecodeError as e:
        return source_text, [f"translated toc payload does not parse: {e}"]
    if not isinstance(names, dict):
        return source_text, ["translated toc payload is not a JSON object"]
    expected = yaml_name_map(source_text)
    problems: list[str] = []
    bad_keys = sorted(k for k in names if not YAML_NAME_KEY_RE.fullmatch(str(k)))
    if bad_keys:
        problems.append(f"toc payload has malformed keys {bad_keys[:5]}")
    missing = sorted(set(expected) - set(names), key=lambda k: int(k[1:]))
    extra = sorted(set(names) - set(expected) - set(bad_keys), key=lambda k: int(k[1:]))
    if missing:
        problems.append(f"toc payload is missing {len(missing)} name(s): {missing[:5]}")
    if extra:
        problems.append(f"toc payload has {len(extra)} unexpected key(s): {extra[:5]}")
    newlines = sorted(k for k, v in names.items() if "\n" in str(v) or "\r" in str(v))
    if newlines:
        problems.append(f"toc names contain line breaks: {newlines[:5]}")
    if problems:
        return source_text, problems
    bom = BOM if source_text.startswith(BOM) else ""
    crlf = "\r\n" in source_text
    lines = to_lf(source_text.lstrip(BOM)).split("\n")
    for key, value in names.items():
        idx = int(key[1:])
        m = YAML_NAME_RE.match(lines[idx])
        if m is None:
            return source_text, [f"toc line {idx} no longer holds a name entry"]
        lines[idx] = f"{m.group(1)}{yaml_scalar(str(value), expected[key])}"
    text = "\n".join(lines)
    return bom + (text.replace("\n", "\r\n") if crlf else text), []


def encode_placeholders(text: str) -> str:
    """{name} -> {{name}}: Translated protects Twig-style placeholders, not single braces."""
    return PLACEHOLDER_RE.sub(r"{{\1}}", text)


def decode_placeholders(text: str) -> str:
    return ENCODED_PLACEHOLDER_RE.sub(r"{\1}", text)


def mask_code(text: str, fences: bool = True) -> tuple[str, list[str]]:
    """Replace fenced code blocks (when `fences`) and inline code spans with {{fN}} / {{cN}}
    placeholders. The service keeps such placeholders intact; it rewrites backticks as quotation
    marks. Returns (masked text, the original code by N)."""
    spans: list[str] = []

    def token(kind: str, value: str) -> str:
        spans.append(value)
        return "{{" + f"{kind}{len(spans) - 1}" + "}}"

    out: list[str] = []
    for seg, is_fence in split_fences(text) if fences else [(text, False)]:
        if is_fence:
            block = seg[:-1] if seg.endswith("\n") else seg
            out.append(token("f", block) + seg[len(block) :])
        else:
            out.append(INLINE_CODE_RE.sub(lambda m: token("c", m.group(0)), seg))
    return "".join(out), spans


def unmask_code(text: str, spans: list[str]) -> tuple[str, list[str]]:
    """Put the original code back for every placeholder, dropping quotation marks the service put
    around one. Returns (text, problems): placeholders missing, repeated or unknown."""
    seen: Counter[int] = Counter()
    unknown: list[str] = []

    def put(m: re.Match[str]) -> str:
        n = int(m.group(3))
        if n >= len(spans):
            unknown.append(m.group(0))
            return m.group(0)
        seen[n] += 1
        opening, closing = m.group(1), m.group(4)
        if opening and QUOTE_PAIRS.get(opening) == closing:
            opening = closing = ""
        return opening + spans[n] + closing

    text = CODE_TOKEN_RE.sub(put, text)
    problems: list[str] = []
    missing = [n for n in range(len(spans)) if not seen[n]]
    repeated = sorted(n for n, k in seen.items() if k > 1)
    if missing:
        problems.append(f"code placeholders missing in the delivery: {missing[:5]} ({len(missing)} of {len(spans)})")
    if repeated:
        problems.append(f"code placeholders repeated in the delivery: {repeated[:5]}")
    if unknown:
        problems.append(f"unknown code placeholders in the delivery: {unknown[:5]}")
    return text, problems


def prepare_payload(rel: str, source_text: str) -> tuple[str, str, dict[str, Any]]:
    """Return (content, content_type, extra job info) for a source file."""
    suffix = Path(rel).suffix.lower()
    content_type = CONTENT_TYPES.get(suffix)
    if content_type is None:
        raise ValueError(f"no content type for {rel}")
    if suffix in (".yml", ".yaml"):
        content, count = extract_yaml_names(source_text)
        return content, content_type, {"mode": "yaml-names", "units": count}
    # Strip a BOM and send LF line endings so Windows and Linux checkouts produce the same payload;
    # both are restored from the source when the delivery is written.
    content = to_lf(source_text.lstrip(BOM))
    if suffix == ".json":
        return encode_placeholders(content), content_type, {"mode": "json-placeholders"}
    if suffix == ".md":
        masked, spans = mask_code(content)
        return masked, content_type, {"mode": "raw", "codeSpans": spans}
    return content, content_type, {"mode": "raw"}


def split_frontmatter(text: str) -> tuple[str, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return "", text
    return text[: m.end()], text[m.end() :]


def frontmatter_values(fm: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in fm.splitlines():
        m = FM_TRANSLATABLE_RE.match(line)
        if m and m.group(2):
            values[m.group(1)] = m.group(2)
    return values


def merge_frontmatter(source_fm: str, translated_fm: str) -> tuple[str, list[str]]:
    """Rebuild the frontmatter from the English source, taking only translated
    `title`/`description` values. Keeps uid, author, dates and applies_to intact
    regardless of what the translator did to them. Returns (frontmatter, problems)."""
    if not source_fm:
        return "", []
    problems: list[str] = []
    if not translated_fm:
        problems.append("frontmatter missing or malformed in the delivery")
    translated_values = frontmatter_values(translated_fm)
    out: list[str] = []
    for line in source_fm.splitlines(keepends=True):
        bare = line.rstrip("\r\n")
        eol = line[len(bare) :]
        m = FM_TRANSLATABLE_RE.match(bare)
        if m and m.group(2):
            key = m.group(1)
            if key in translated_values:
                out.append(f"{key}: {yaml_scalar(translated_values[key], m.group(2))}{eol}")
                continue
            if translated_fm:
                problems.append(f"frontmatter '{key}' not found in the delivery")
        out.append(line)
    return "".join(out), problems


def split_fences(body: str) -> list[tuple[str, bool]]:
    """Split a Markdown body into alternating (text, False) / (fenced block, True) segments.
    A fenced block spans its opening fence line through its closing fence line; an unclosed
    fence runs to the end. The list always starts and ends with a text segment."""
    segments: list[tuple[str, bool]] = []
    text: list[str] = []
    block: list[str] = []
    in_fence = False
    for line in body.splitlines(keepends=True):
        if FENCE_RE.match(line):
            if in_fence:
                block.append(line)
                segments.append(("".join(block), True))
                block = []
            else:
                segments.append(("".join(text), False))
                text = []
                block.append(line)
            in_fence = not in_fence
        elif in_fence:
            block.append(line)
        else:
            text.append(line)
    if block:
        segments.append(("".join(block), True))
    segments.append(("".join(text), False))
    return segments


def count_fence_lines(body: str) -> int:
    return sum(1 for line in body.splitlines() if FENCE_RE.match(line))


def restore_positionally(text: str, source_text: str, regex: re.Pattern[str], group: int) -> tuple[str, int] | None:
    """Replace every match of `regex` (its `group`) in `text` with the source's value at the
    same position. Returns (text, changed) when the counts match, None otherwise. Values that
    are the source's values in another order are left as delivered (word order differs by language)."""
    src_values = [m.group(group) for m in regex.finditer(source_text)]
    matches = list(regex.finditer(text))
    if len(src_values) != len(matches):
        return None
    if Counter(src_values) == Counter(m.group(group) for m in matches):
        return text, 0
    out: list[str] = []
    pos = 0
    changed = 0
    for m, value in zip(matches, src_values, strict=True):
        start, end = m.span(group)
        if m.group(group) != value:
            changed += 1
        out.append(text[pos:start])
        out.append(value)
        pos = end
    out.append(text[pos:])
    return "".join(out), changed


def count_diff(source_text: str, text: str, regex: re.Pattern[str], group: int, what: str) -> str:
    s = Counter(m.group(group) for m in regex.finditer(source_text))
    t = Counter(m.group(group) for m in regex.finditer(text))
    missing = list((s - t).elements())[:5]
    added = list((t - s).elements())[:5]
    return f"{what} {sum(s.values())} -> {sum(t.values())} (missing {missing}, added {added})"


def letters(text: str) -> int:
    return sum(1 for c in text if c.isalpha())


def resplit_by_lines(joined: str, original_segments: list[str]) -> list[str]:
    """Split `joined` back into pieces with the same line counts as `original_segments`.
    Positional restoration never adds or removes newlines (every span regex excludes them),
    so line counts identify the original prose/fence boundaries."""
    pieces: list[str] = []
    pos = 0
    for i, seg in enumerate(original_segments):
        if i == len(original_segments) - 1:
            pieces.append(joined[pos:])
            break
        end = pos
        for _ in range(seg.count("\n")):
            end = joined.index("\n", end) + 1
        pieces.append(joined[pos:end])
        pos = end
    return pieces


@dataclass
class RepairResult:
    text: str
    problems: list[str] = field(default_factory=list)
    repaired: Counter[str] = field(default_factory=Counter)
    warnings: list[str] = field(default_factory=list)


MD_RESTORE_RULES: tuple[tuple[re.Pattern[str], int, str, str], ...] = (
    (INLINE_CODE_RE, 0, "inline code", "inline code spans"),
    (ALERT_RE, 0, "markers", "alert/include markers"),
    (LINK_TARGET_RE, 1, "links", "link targets"),
)


def prose_key(text: str) -> str:
    """The text with everything the repair step restores from English, a list marker and heading marks,
    masked out."""
    text = LIST_ITEM_RE.sub("\x00", text, count=1)
    text = HEADING_MARKS_RE.sub("\x00", text, count=1)
    for regex, _group, _kind, _what in MD_RESTORE_RULES:
        text = regex.sub("\x00", text)
    return text


def repair_markdown_body(source_body: str, translated_body: str, repair: bool = True) -> RepairResult:
    """Repair-then-verify for a Markdown body (LF line endings, no frontmatter).
    Fenced blocks, inline code, alert/include markers and link targets are restored from
    the source positionally when their counts match; count mismatches and heading count
    differences are problems. With repair=False, differences become problems (verify only).
    Exception: an inline-code count mismatch is only a warning (MT routinely adds or drops a
    backtick pair) and the delivered spans are kept as they are."""
    result = RepairResult(translated_body)
    src_fences, tr_fences = count_fence_lines(source_body), count_fence_lines(translated_body)
    if src_fences != tr_fences:
        result.problems.append(f"code fences {src_fences} -> {tr_fences}")
        return result
    src_segments = split_fences(source_body)
    tr_segments = split_fences(translated_body)
    fixed_blocks = sum(1 for s, t in zip(src_segments, tr_segments, strict=True) if s[1] and s[0] != t[0])
    if fixed_blocks and repair:
        result.repaired["fences"] += fixed_blocks
    elif fixed_blocks:
        result.problems.append(f"fenced code differs in {fixed_blocks} block(s)")
    src_text = "".join(seg for seg, is_fence in src_segments if not is_fence)
    tr_text_segments = [seg for seg, is_fence in tr_segments if not is_fence]
    tr_text = "".join(tr_text_segments)

    for regex, group, kind, what in MD_RESTORE_RULES:
        restored = restore_positionally(tr_text, src_text, regex, group)
        if restored is None:
            lost = sum(1 for _ in regex.finditer(tr_text)) < sum(1 for _ in regex.finditer(src_text))
            findings = result.warnings if kind in WARNING_KINDS and not lost else result.problems
            findings.append(count_diff(src_text, tr_text, regex, group, what))
        elif restored[1] and repair:
            result.repaired[kind] += restored[1]
            tr_text = restored[0]
        elif restored[1]:
            result.problems.append(f"{what} differ in {restored[1]} place(s)")

    src_headings = sum(1 for line in src_text.splitlines() if HEADING_RE.match(line))
    tr_headings = sum(1 for line in tr_text.splitlines() if HEADING_RE.match(line))
    if src_headings != tr_headings:
        result.problems.append(f"headings {src_headings} -> {tr_headings}")
    if result.problems or not repair:
        return result
    prose = iter(resplit_by_lines(tr_text, tr_text_segments))
    result.text = "".join(src_seg if is_fence else next(prose) for src_seg, is_fence in src_segments)
    return result


def markdown_prose(body: str) -> str:
    return "".join(seg for seg, is_fence in split_fences(body) if not is_fence)


def verify_html_tags(source: str, translated: str) -> list[str]:
    s_tags = Counter(x.lower() for x in HTML_TAG_RE.findall(source))
    t_tags = Counter(x.lower() for x in HTML_TAG_RE.findall(translated))
    if s_tags != t_tags:
        return [f"tag counts differ {dict(s_tags - t_tags) or dict(t_tags - s_tags)}"]
    return []


def repair_html(source: str, translated: str, repair: bool = True) -> RepairResult:
    result = RepairResult(translated)
    result.problems.extend(verify_html_tags(source, translated))
    restored = restore_positionally(translated, source, HTML_REF_RE, 1)
    if restored is None:
        result.problems.append(count_diff(source, translated, HTML_REF_RE, 1, "href/src attributes"))
    elif restored[1] and repair:
        result.repaired["links"] += restored[1]
        result.text = restored[0]
    elif restored[1]:
        result.problems.append(f"href/src attributes differ in {restored[1]} place(s)")
    return result


def json_indent(text: str) -> int:
    m = re.search(r'^( +)"', text, re.M)
    return len(m.group(1)) if m else 2


def verify_json_strings(source: str, translated: str) -> tuple[str, list[str]]:
    """Decode placeholders, check keys and placeholders, re-serialise like the source.
    Returns (text, problems); text is empty when there are problems."""
    try:
        s_obj = json.loads(source.lstrip(BOM))
        t_obj = json.loads(decode_placeholders(translated.lstrip(BOM)))
    except json.JSONDecodeError as e:
        return "", [f"translated JSON does not parse: {e}"]
    if not isinstance(s_obj, dict) or not isinstance(t_obj, dict):
        return "", ["JSON root is not an object"]
    if set(s_obj) != set(t_obj):
        missing = sorted(set(s_obj) - set(t_obj))[:5]
        added = sorted(set(t_obj) - set(s_obj))[:5]
        return "", [f"keys differ: missing {missing} added {added}"]
    problems = [
        f"placeholders changed in '{key}'"
        for key, value in s_obj.items()
        if isinstance(value, str)
        and Counter(PLACEHOLDER_RE.findall(value)) != Counter(PLACEHOLDER_RE.findall(str(t_obj[key])))
    ]
    if problems:
        return "", problems
    text = json.dumps(t_obj, indent=json_indent(source), ensure_ascii=False)
    if to_lf(source).endswith("\n"):
        text += "\n"
    return text, []


def match_trailing_newline(text: str, source: str) -> str:
    if source.endswith("\n") and not text.endswith("\n"):
        return text + "\n"
    if not source.endswith("\n") and text.endswith("\n"):
        return text.rstrip("\n")
    return text


def finalize_translation(
    rel: str,
    job: dict[str, Any],
    source_text: str,
    translated: str,
    repair: bool = True,
    check_identity: bool = True,
) -> tuple[str, list[str], Counter[str], list[str]]:
    """Turn delivered content into the file to write.
    Returns (text, problems, repaired counts by kind, warnings). The text is only written when
    problems is empty (or --lenient is given); warnings never block writing."""
    suffix = Path(rel).suffix.lower()
    if job.get("mode") == "yaml-names":
        text, toc_problems = reinsert_yaml_names(source_text, translated)
        return text, toc_problems, Counter(), []

    bom = BOM if source_text.startswith(BOM) else ""
    crlf = "\r\n" in source_text
    source_lf = to_lf(source_text.lstrip(BOM))
    delivered = to_lf(translated.lstrip(BOM))
    repaired: Counter[str] = Counter()
    problems: list[str] = []
    warnings: list[str] = []

    if suffix == ".md":
        src_fm, src_body = split_frontmatter(source_lf)
        if src_fm:
            delivered = delivered.lstrip()
        tr_fm, tr_body = split_frontmatter(delivered)
        fm, fm_problems = merge_frontmatter(src_fm, tr_fm)
        problems.extend(fm_problems)
        result = repair_markdown_body(src_body, tr_body, repair)
        problems.extend(result.problems)
        repaired.update(result.repaired)
        warnings.extend(result.warnings)
        body = match_trailing_newline(result.text, src_body)
        if (
            check_identity
            and not problems
            and letters(markdown_prose(body)) > IDENTITY_MIN_LETTERS
            and markdown_prose(body) == markdown_prose(src_body)
        ):
            problems.append("delivered content identical to source")
        text = fm + body
    elif suffix in (".html", ".htm"):
        result = repair_html(source_lf, delivered, repair)
        problems.extend(result.problems)
        repaired.update(result.repaired)
        warnings.extend(result.warnings)
        text = match_trailing_newline(result.text, source_lf)
        if check_identity and not problems and letters(text) > IDENTITY_MIN_LETTERS and text == source_lf:
            problems.append("delivered content identical to source")
    elif suffix == ".json":
        text, json_problems = verify_json_strings(source_lf, delivered)
        problems.extend(json_problems)
    else:
        text = delivered
    if crlf:
        text = text.replace("\n", "\r\n")
    return bom + text, problems, repaired, warnings


# ---------------------------------------------------------------------------
# Segment-level updates (only what changed since the English the translation was made from)
# ---------------------------------------------------------------------------

Assembler = Callable[[dict[str, str]], tuple[str, list[str], Counter[str], list[str]]]


@dataclass
class Delta:
    """The content[] items of a segment-level order and how to rebuild the file from the delivery.
    `assemble` takes {segment id -> translation} and returns (text, problems, repaired, warnings)."""

    mode: str
    items: list[dict[str, Any]]
    assemble: Assembler
    changed: int  # translatable units sent
    total: int  # translatable units in the file
    changed_chars: int
    total_chars: int

    @property
    def chars(self) -> int:
        return sum(len(str(i["text"])) for i in self.items if i["translatable"])


def unquote_scalar(value: str) -> str:
    v = value.strip()
    if len(v) >= 2 and v[0] == v[-1] == '"':
        try:
            return str(json.loads(v))
        except json.JSONDecodeError:
            return v
    if len(v) >= 2 and v[0] == v[-1] == "'":
        return v[1:-1].replace("''", "'")
    return v


def newline_eol(text: str) -> tuple[str, str, bool]:
    """(BOM, LF text without BOM, CRLF?) of a source file."""
    return (BOM if text.startswith(BOM) else ""), to_lf(text.lstrip(BOM)), "\r\n" in text


def match_block_end(text: str, english: str) -> str:
    """`text` with the trailing newline of its English block (a reused last block may lack one)."""
    if english.endswith("\n") and not text.endswith("\n"):
        return text + "\n"
    if not english.endswith("\n") and text.endswith("\n"):
        return text.rstrip("\n")
    return text


def restore_list_marker(english: str, text: str) -> tuple[str, bool]:
    source_marker = LIST_ITEM_RE.match(english)
    delivered_marker = LIST_ITEM_RE.match(text)
    if source_marker and delivered_marker and source_marker.group(0) != delivered_marker.group(0):
        return source_marker.group(0) + text[delivered_marker.end() :], True
    return text, False


def restore_heading_marks(english: str, text: str) -> str:
    source_marks = HEADING_MARKS_RE.match(english)
    marks = HEADING_MARKS_RE.match(text)
    if source_marks and marks and source_marks.group(0) != marks.group(0):
        return source_marks.group(0) + text[marks.end() :]
    return text


def repair_by_value(old: str, new: str, loc: str) -> str | None:
    """`loc` (the translation of `old`) with every code span, marker and link target replaced by its
    counterpart in `new`: the old value at position k becomes the new value at position k, wherever
    the translation placed it. None when one old value maps to two new values or the translation's
    spans are not the old spans."""
    text = loc
    for regex, group, _kind, _what in MD_RESTORE_RULES:
        old_values = [m.group(group) for m in regex.finditer(old)]
        new_values = [m.group(group) for m in regex.finditer(new)]
        if len(old_values) != len(new_values):
            return None
        mapping: dict[str, str] = {}
        for o, n in zip(old_values, new_values, strict=True):
            if mapping.setdefault(o, n) != n:
                return None
        matches = list(regex.finditer(text))
        if Counter(m.group(group) for m in matches) != Counter(old_values):
            return None
        out: list[str] = []
        pos = 0
        for m in matches:
            start, end = m.span(group)
            out.append(text[pos:start])
            out.append(mapping[m.group(group)])
            pos = end
        out.append(text[pos:])
        text = "".join(out)
    return text


def finalize_block(block: Block, delivered: str) -> tuple[str, list[str], Counter[str], list[str]]:
    """Repair and verify one delivered Markdown block against its English block. The delivery must
    segment as exactly one block of the same kind, so the page keeps aligning with the English.
    Returns (text, problems, repaired, warnings)."""
    lines = to_lf(delivered.lstrip(BOM)).split("\n")
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    indent = block.text[: len(block.text) - len(block.text.lstrip(" \t"))]
    if indent and block.kind != KIND_LIST_ITEM:
        lines = [line if line.startswith(indent) else indent + line.lstrip(" \t") for line in lines]
    text = match_block_end("\n".join(lines), block.text)
    seg = segment(text)
    if seg.lead or len(seg.blocks) != 1 or seg.blocks[0].kind != block.kind or seg.blocks[0].gap:
        return text, [f"{block.kind} block came back as {' + '.join(seg.kinds) or 'nothing'}"], Counter(), []
    repaired: Counter[str] = Counter()
    if block.kind == KIND_HEADING:
        marks, delivered_marks = block.text.split(None, 1)[0], text.split(None, 1)[0]
        if marks != delivered_marks:
            return text, [f"heading level {marks} -> {delivered_marks}"], Counter(), []
    if block.kind == KIND_LIST_ITEM:
        text, changed = restore_list_marker(block.text, text)
        repaired["markers"] += changed
    result = repair_markdown_body(block.text, text)
    repaired.update(result.repaired)
    return result.text, result.problems, +repaired, result.warnings


def heading_count(body: str) -> int:
    return sum(1 for line in markdown_prose(body).splitlines() if HEADING_RE.match(line))


def md_delta(new_text: str, old_text: str, loc_text: str, context_width: int = 0) -> Delta | str:
    bom, new_lf, crlf = newline_eol(new_text)
    new_fm, new_body = split_frontmatter(new_lf)
    old_fm, old_body = split_frontmatter(to_lf(old_text.lstrip(BOM)))
    loc_fm, loc_body = split_frontmatter(INJECTED_ANCHOR_RE.sub("", to_lf(loc_text.lstrip(BOM))))
    new_seg, old_seg, loc_seg = segment(new_body), segment(old_body), segment(loc_body)
    if old_seg.kinds != loc_seg.kinds:
        return f"unaligned ({len(old_seg.blocks)} English blocks, {len(loc_seg.blocks)} translated)"
    loc_prose = markdown_prose(loc_body)
    translatable_letters = sum(letters(b.text) for b in loc_seg.blocks if b.translatable)
    if translatable_letters > IDENTITY_MIN_LETTERS and loc_prose in (
        markdown_prose(old_body),
        markdown_prose(new_body),
    ):
        return "existing translation is the English text"
    existing = repair_markdown_body(old_body, loc_body)
    if existing.problems:
        return f"existing translation does not verify against its English ({existing.problems[0]})"
    actions = diff_blocks(old_seg.blocks, new_seg.blocks, prose_key)
    repaired_blocks: dict[int, str] = {}
    for j, a in enumerate(actions):
        if a.kind == ACTION_REPAIR:
            b = new_seg.blocks[j]
            fixed = repair_by_value(old_seg.blocks[a.old_index].text, b.text, loc_seg.blocks[a.old_index].text)
            if fixed is None:
                actions[j] = Action(ACTION_TRANSLATE)
            elif b.kind == KIND_LIST_ITEM:
                repaired_blocks[j] = restore_list_marker(b.text, fixed)[0]
            else:
                repaired_blocks[j] = restore_heading_marks(b.text, fixed) if b.kind == KIND_HEADING else fixed
    new_vals, old_vals, loc_vals = frontmatter_values(new_fm), frontmatter_values(old_fm), frontmatter_values(loc_fm)
    reused_fm = {k: loc_vals[k] for k, v in new_vals.items() if old_vals.get(k) == v and k in loc_vals}
    masks: dict[str, list[str]] = {}

    def item(item_id: str, text: str, translatable: bool) -> dict[str, Any]:
        masked, masks[item_id] = mask_code(text, fences=False)
        return {"id": item_id, "text": masked, "translatable": translatable}

    def delivered(item_id: str, translations: dict[str, str]) -> tuple[str | None, list[str]]:
        if item_id not in translations:
            return None, []
        text, mask_problems = unmask_code(translations[item_id], masks[item_id])
        return (None if mask_problems else text), mask_problems

    items: list[dict[str, Any]] = [
        item(f"fm:{k}", unquote_scalar(v), True) for k, v in new_vals.items() if k not in reused_fm
    ]
    changed = {j for j, a in enumerate(actions) if a.kind == ACTION_TRANSLATE}
    context = set(context_indices(actions, new_seg.blocks, context_width))
    for j, b in enumerate(new_seg.blocks):
        if j in changed or j in context:
            items.append(item(f"{'b' if j in changed else 'c'}{j}", b.text.rstrip("\n"), j in changed))
    translatable_blocks = [b for b in new_seg.blocks if b.translatable]

    def assemble(translations: dict[str, str]) -> tuple[str, list[str], Counter[str], list[str]]:
        problems: list[str] = []
        warnings: list[str] = []
        repaired: Counter[str] = Counter()
        texts: list[str] = []
        pairs: list[tuple[str, str]] = []
        for j, (b, a) in enumerate(zip(new_seg.blocks, actions, strict=True)):
            if a.kind == ACTION_ENGLISH:
                text = b.text
            elif a.kind == ACTION_REPAIR:
                text = repaired_blocks[j]
            elif a.kind == ACTION_REUSE:
                # Restored against its own English block only: a page-wide positional pass would move
                # spans across blocks when one block's count drifts.
                text = loc_seg.blocks[a.old_index].text
                fixed = repair_markdown_body(b.text, text)
                if not fixed.problems:
                    text = fixed.text
                    repaired.update(fixed.repaired)
            elif (block := delivered(f"b{j}", translations))[0] is None:
                problems.extend(f"block {j}: {p}" for p in block[1] or ["missing in the delivery"])
                text = b.text
            else:
                text, block_problems, block_repaired, block_warnings = finalize_block(b, str(block[0]))
                problems.extend(f"block {j}: {p}" for p in block_problems)
                warnings.extend(f"block {j}: {w}" for w in block_warnings)
                repaired.update(block_repaired)
                pairs.append((b.text, text))
            texts.append(match_block_end(text, b.text))
        lead, gaps = reused_layout(actions, new_seg, len(old_seg.blocks), loc_seg)
        body = new_seg.join(texts, gaps, lead)
        if count_fence_lines(body) != count_fence_lines(new_body):
            problems.append(f"code fences {count_fence_lines(new_body)} -> {count_fence_lines(body)}")
        if heading_count(body) != heading_count(new_body):
            problems.append(f"headings {heading_count(new_body)} -> {heading_count(body)}")
        if segment(body).kinds != new_seg.kinds:
            problems.append("delivered blocks change the page structure")
        if pairs and sum(letters(e) for e, _ in pairs) > IDENTITY_MIN_LETTERS and all(e == t for e, t in pairs):
            problems.append("delivered content identical to source")
        fm = ""
        if new_fm:
            # merge_frontmatter reports a value that is missing here (or held a line break) as not found.
            values = dict(reused_fm)
            for k in new_vals:
                if k in reused_fm:
                    continue
                value, value_problems = delivered(f"fm:{k}", translations)
                problems.extend(f"frontmatter '{k}': {p}" for p in value_problems)
                if value and value.strip() and "\n" not in value.strip():
                    values[k] = value.strip()
            synthetic = "---\n" + "".join(f"{k}: {v}\n" for k, v in values.items()) + "---\n"
            fm, fm_problems = merge_frontmatter(new_fm, synthetic)
            problems.extend(fm_problems)
        text = fm + body
        if crlf:
            text = text.replace("\n", "\r\n")
        return bom + text, problems, repaired, warnings

    sent = [i for i in items if i["translatable"]]
    return Delta(
        "md-blocks",
        items,
        assemble,
        changed=len(sent),
        total=len(new_vals) + len(translatable_blocks),
        changed_chars=sum(len(str(i["text"])) for i in sent),
        total_chars=sum(len(unquote_scalar(v)) for v in new_vals.values())
        + sum(len(b.text.rstrip("\n")) for b in translatable_blocks),
    )


def json_delta(new_text: str, old_text: str, loc_text: str) -> Delta | str:
    bom, new_lf, crlf = newline_eol(new_text)
    new, old, loc = (json.loads(to_lf(t.lstrip(BOM))) for t in (new_text, old_text, loc_text))
    if not all(isinstance(x, dict) for x in (new, old, loc)):
        return "unaligned (JSON root is not an object)"
    if loc in (old, new):
        return "existing translation is the English text"
    reuse = {k for k, v in new.items() if isinstance(v, str) and old.get(k) == v and isinstance(loc.get(k), str)}
    changed = [k for k, v in new.items() if isinstance(v, str) and k not in reuse]
    indent = json_indent(new_lf)
    subset = json.dumps({k: new[k] for k in changed}, indent=indent, ensure_ascii=False) + "\n"
    items = [{"id": "json", "text": encode_placeholders(subset), "translatable": True}] if changed else []

    def assemble(translations: dict[str, str]) -> tuple[str, list[str], Counter[str], list[str]]:
        translated: dict[str, Any] = {}
        if changed:
            if "json" not in translations:
                return "", ["no translation in the response"], Counter(), []
            text, problems = verify_json_strings(subset, translations["json"])
            if problems:
                return "", problems, Counter(), []
            translated = json.loads(text)
        out = {k: translated[k] if k in translated else loc[k] if k in reuse else v for k, v in new.items()}
        text = json.dumps(out, indent=indent, ensure_ascii=False) + ("\n" if new_lf.endswith("\n") else "")
        if crlf:
            text = text.replace("\n", "\r\n")
        return bom + text, [], Counter(), []

    strings = [v for v in new.values() if isinstance(v, str)]
    return Delta(
        "json-keys",
        items,
        assemble,
        changed=len(changed),
        total=len(strings),
        changed_chars=sum(len(new[k]) for k in changed),
        total_chars=sum(len(v) for v in strings),
    )


def toc_entry_keys(text: str, names: dict[str, str]) -> dict[str, tuple[str, str]]:
    """{name key -> (name, href on the next line)}: an entry is matched by both, so two entries
    with the same English name keep their own translations when they move."""
    lines = to_lf(text.lstrip(BOM)).split("\n")
    keys: dict[str, tuple[str, str]] = {}
    for key, name in names.items():
        i = int(key[1:]) + 1
        m = TOC_HREF_RE.match(lines[i]) if i < len(lines) else None
        keys[key] = (name, m.group(1) if m else "")
    return keys


def toc_delta(new_text: str, old_text: str, loc_text: str) -> Delta | str:
    new_names, old_names, loc_names = yaml_name_map(new_text), yaml_name_map(old_text), yaml_name_map(loc_text)
    if list(old_names) != list(loc_names):
        return f"unaligned ({len(old_names)} English names, {len(loc_names)} translated)"
    if list(loc_names.values()) in (list(old_names.values()), list(new_names.values())):
        return "existing translation is the English text"
    old_entries, new_entries = toc_entry_keys(old_text, old_names), toc_entry_keys(new_text, new_names)
    old_keys, new_keys = list(old_names), list(new_names)
    first_key: dict[tuple[str, str], str] = {}
    for k in old_keys:
        first_key.setdefault(old_entries[k], k)
    matcher = difflib.SequenceMatcher(
        None, [old_entries[k] for k in old_keys], [new_entries[k] for k in new_keys], autojunk=False
    )
    reused: dict[str, str] = {}
    for tag, i1, _i2, j1, j2 in matcher.get_opcodes():
        for j in range(j1, j2):
            key = new_keys[j]
            if tag == "equal":
                reused[key] = loc_names[old_keys[i1 + (j - j1)]]
            elif new_entries[key] in first_key:
                reused[key] = loc_names[first_key[new_entries[key]]]
    changed = [k for k in new_keys if k not in reused]
    payload = json.dumps({k: new_names[k] for k in changed}, ensure_ascii=False, indent=2)
    items = [{"id": "toc", "text": payload, "translatable": True}] if changed else []

    def assemble(translations: dict[str, str]) -> tuple[str, list[str], Counter[str], list[str]]:
        names = dict(reused)
        if changed:
            try:
                delivered = json.loads(translations.get("toc", "").lstrip(BOM))
            except json.JSONDecodeError as e:
                return new_text, [f"translated toc payload does not parse: {e}"], Counter(), []
            if not isinstance(delivered, dict) or set(delivered) != set(changed):
                got = sorted(delivered) if isinstance(delivered, dict) else type(delivered).__name__
                return (
                    new_text,
                    [f"toc payload keys differ: expected {changed[:5]}, got {str(got)[:120]}"],
                    Counter(),
                    [],
                )
            names.update({k: str(v) for k, v in delivered.items()})
        text, problems = reinsert_yaml_names(new_text, json.dumps(names, ensure_ascii=False))
        return text, problems, Counter(), []

    return Delta(
        "toc-names",
        items,
        assemble,
        changed=len(changed),
        total=len(new_keys),
        changed_chars=sum(len(new_names[k]) for k in changed),
        total_chars=sum(len(v) for v in new_names.values()),
    )


def plan_delta(
    config: TranslationConfig, lang: str, rel: str, entry: dict[str, Any], run: GitRunner = run_git
) -> Delta | str:
    """A segment-level update for an outdated translation, or why it is translated as a whole file."""
    suffix = Path(rel).suffix.lower()
    if suffix not in (".md", ".json", ".yml", ".yaml"):
        return WHOLE_FILE_TYPE
    target = target_file(lang, rel)
    if not target.exists():
        return "no existing translation"
    old = recorded_source_text(rel, entry, run)
    if old is None:
        return "English version of the translation not found in git"
    new, loc = read_text(CONTENT_DIR / rel), read_text(target)
    try:
        if suffix == ".md":
            delta = md_delta(new, old, loc, config.context_segments)
        elif suffix == ".json":
            delta = json_delta(new, old, loc)
        else:
            delta = toc_delta(new, old, loc)
    except json.JSONDecodeError as e:
        return f"unaligned (JSON does not parse: {e})"
    if isinstance(delta, str):
        return delta
    if delta.total_chars and delta.changed_chars > config.max_changed_ratio * delta.total_chars:
        return f"mostly changed ({delta.changed_chars * 100 // delta.total_chars}% of the text)"
    return delta


def map_segment_translations(items: list[dict[str, Any]], data: list[dict[str, Any]]) -> dict[str, str] | str:
    """{segment id -> translation} from a /translate/ai response. data[] is positional: either one
    entry per content[] item or one per translatable item. An echoed id must match."""
    translatable = [i for i in items if i["translatable"]]
    if len(data) == len(items):
        pairs = list(zip(items, data, strict=True))
    elif len(data) == len(translatable):
        pairs = list(zip(translatable, data, strict=True))
    else:
        return f"response has {len(data)} item(s) for {len(items)} segment(s) ({len(translatable)} translatable)"
    out: dict[str, str] = {}
    for item, d in pairs:
        if "id" in d and str(d["id"]) != str(item["id"]):
            return f"response item id {d['id']!r} where {item['id']!r} was sent"
        if not item["translatable"]:
            continue
        translation = d.get("translation")
        if not isinstance(translation, str):
            return f"no translation for segment {item['id']}"
        out[str(item["id"])] = translation
    return out


# ---------------------------------------------------------------------------
# Translated API client
# ---------------------------------------------------------------------------


class TranslatedApiError(Exception):
    """A non-retryable API failure or exhausted retries. Carries the parsed api_error."""

    def __init__(self, message: str, http_status: int | None = None, api_error: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.http_status = http_status
        self.api_error = api_error or {}

    def details(self) -> dict[str, Any]:
        out: dict[str, Any] = {"message": str(self)}
        if self.http_status is not None:
            out["httpStatus"] = self.http_status
        for key in ("code", "id_transaction"):
            if self.api_error.get(key):
                out[key] = self.api_error[key]
        params = self.api_error.get("params")
        if isinstance(params, list):
            out["params"] = [
                {"field": p.get("field"), "reason": p.get("reason")} for p in params if isinstance(p, dict)
            ]
        return out


class TranslatedAuthError(TranslatedApiError):
    """The API rejected the key. Nothing was billed; the run stops without recording failures."""


def parse_retry_after(value: str | None, now: datetime | None = None) -> float | None:
    """Seconds to wait from a Retry-After header (delay-seconds or HTTP-date), or None."""
    if not value or not value.strip():
        return None
    v = value.strip()
    if v.isdigit():
        return float(v)
    try:
        when = email.utils.parsedate_to_datetime(v)
    except (TypeError, ValueError):
        return None
    if when.tzinfo is None:
        when = when.replace(tzinfo=UTC)
    return max(0.0, (when - (now or datetime.now(UTC))).total_seconds())


def retry_delay(attempt: int, retry_after: float | None, jitter: Callable[[], float]) -> float:
    """Retry-After when the server sent one, else exponential backoff with jitter; at most MAX_RETRY_DELAY."""
    if retry_after is not None:
        return min(retry_after, MAX_RETRY_DELAY)
    base = min(float(2**attempt * 2), MAX_RETRY_DELAY)
    return base / 2 + jitter() * base / 2


def describe_api_error(payload: str) -> tuple[str, dict[str, Any]]:
    """Build a readable message from an api_error body when it parses, else from the raw text."""
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError:
        return payload[:500], {}
    if not isinstance(parsed, dict):
        return payload[:500], {}
    parts = [str(parsed.get(k)) for k in ("code", "message") if parsed.get(k)]
    for p in parsed.get("params") or []:
        if isinstance(p, dict):
            parts.append(f"{p.get('field')}: {p.get('reason')}")
    if parsed.get("id_transaction"):
        parts.append(f"transaction {parsed['id_transaction']}")
    return "; ".join(parts) or payload[:500], parsed


class TranslationClient(Protocol):
    def translate_ai(self, order: dict[str, Any]) -> list[dict[str, Any]]: ...

    def service_type_names(self) -> list[dict[str, Any]]: ...

    def languages(self) -> list[dict[str, Any]]: ...


class TranslatedClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        sleep: Callable[[float], None] = time.sleep,
        opener: Callable[..., Any] = urllib.request.urlopen,
        jitter: Callable[[], float] = random.random,
    ) -> None:
        self.base_url = base_url
        self.api_key = api_key
        self.sleep = sleep
        self.jitter = jitter
        self.opener = opener  # urlopen-compatible; injectable so the self-test can fake HTTP answers offline

    def _request(
        self,
        method: str,
        endpoint: str,
        body: Any = None,
        extra_headers: dict[str, str] | None = None,
        retries: int = 3,
    ) -> Any:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
        url = self.base_url + endpoint
        headers = {"x-api-key": self.api_key, "Accept": "application/json"}
        if data is not None:
            headers["Content-Type"] = "application/json"
        headers.update(extra_headers or {})
        last_error = "retries exhausted"
        for attempt in range(retries + 1):
            req = urllib.request.Request(url, data=data, method=method, headers=headers)
            retry_after: float | None = None
            try:
                with self.opener(req, timeout=180) as resp:
                    return json.loads(resp.read().decode("utf-8") or "null")
            except urllib.error.HTTPError as e:
                payload = e.read().decode("utf-8", errors="replace")
                message, api_error = describe_api_error(payload)
                last_error = f"{e.code}: {message}"
                if e.code in AUTH_HTTP:
                    raise TranslatedAuthError(
                        f"{method} {endpoint} failed with {last_error}. The API key was rejected: check the "
                        "TRANSLATED_API_KEY secret, and that it belongs to the TRANSLATED_ENV environment.",
                        e.code,
                        api_error,
                    ) from None
                if e.code not in RETRYABLE_HTTP:
                    raise TranslatedApiError(
                        f"{method} {endpoint} failed with {last_error}", e.code, api_error
                    ) from None
                retry_after = parse_retry_after(e.headers.get("Retry-After") if e.headers else None)
            except (urllib.error.URLError, OSError, http.client.HTTPException, json.JSONDecodeError) as e:
                last_error = f"{type(e).__name__}: {e}"
            if attempt < retries:
                self.sleep(retry_delay(attempt, retry_after, self.jitter))
        raise TranslatedApiError(f"{method} {endpoint} failed after {retries + 1} attempts ({last_error})")

    def _post(self, endpoint: str, body: Any, extra_headers: dict[str, str] | None = None, retries: int = 3) -> Any:
        return self._request("POST", endpoint, body, extra_headers, retries)

    def _get(self, endpoint: str) -> Any:
        return self._request("GET", endpoint)

    def translate_ai(self, order: dict[str, Any]) -> list[dict[str, Any]]:
        """Synchronous AI translation of one file; data[] is positionally aligned with content[].
        The idempotency id is reused on retries so a timeout cannot bill the same content twice."""
        result = self._post("translate/ai", order, {"x-idempotency-id": str(uuid.uuid4())})
        data = result.get("data") if isinstance(result, dict) else None
        if not isinstance(data, list):
            raise TranslatedApiError(f"POST translate/ai returned an unexpected body: {str(result)[:300]}")
        return [i for i in data if isinstance(i, dict)]

    def service_type_names(self) -> list[dict[str, Any]]:
        items = self._get("symbol/service-type-names")
        return [i for i in items if isinstance(i, dict)] if isinstance(items, list) else []

    def languages(self) -> list[dict[str, Any]]:
        items = self._get("symbol/languages")
        return [i for i in items if isinstance(i, dict)] if isinstance(items, list) else []


def require_client(config: TranslationConfig, action: str, need_service_type: bool = True) -> TranslatedClient:
    config.require_network(action, need_service_type)
    api_key = os.environ.get("TRANSLATED_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("TRANSLATED_API_KEY is not set.")
    assert config.base_url is not None
    return TranslatedClient(config.base_url, api_key)


# ---------------------------------------------------------------------------
# Planning
# ---------------------------------------------------------------------------


@dataclass
class PlanOptions:
    file_filters: list[str] = field(default_factory=list)
    limit: int = 0
    force: bool = False
    retry_failed: bool = False

    @property
    def filtered(self) -> bool:
        return bool(self.file_filters) or self.limit > 0


@dataclass
class LanguagePlan:
    lang: str
    to_submit: list[tuple[str, str]] = field(default_factory=list)  # (rel, reason)
    orphans: list[str] = field(default_factory=list)  # translated files whose English source is gone
    pinned: list[str] = field(default_factory=list)  # files[rel].manual == true
    skipped_failed: list[tuple[str, str]] = field(default_factory=list)  # failed at the current hash
    unscoped: list[str] = field(default_factory=list)  # status entries for files outside scope
    passthrough: list[str] = field(default_factory=list)  # passthrough files in scope (after --file)
    to_copy: list[str] = field(default_factory=list)  # ... whose copy is byte-stale or missing
    current: int = 0
    passthrough_current: int = 0


def target_file(lang: str, rel: str) -> Path:
    return LOCALIZED_DIR / lang / "content" / rel


def passthrough_stale(lang: str, rel: str) -> bool:
    target = target_file(lang, rel)
    return not target.exists() or target.read_bytes() != (CONTENT_DIR / rel).read_bytes()


def build_plan(
    lang: str,
    sources: dict[str, str],
    passthrough: dict[str, str],
    status: dict[str, Any],
    options: PlanOptions,
) -> LanguagePlan:
    plan = LanguagePlan(lang)
    files = status["files"]
    failures = status["failures"]
    for rel, src_hash in sources.items():
        if not matches_filters(rel, options.file_filters):
            continue
        entry = files.get(rel, {})
        if entry.get("manual") is True:
            plan.pinned.append(rel)
            continue
        exists = target_file(lang, rel).exists()
        current = entry.get("status") == STATUS_TRANSLATED and entry.get("sourceHash") == src_hash and exists
        if options.force:
            plan.to_submit.append((rel, "forced"))
            continue
        if current:
            plan.current += 1
            continue
        failure = failures.get(rel)
        # A failed request was not billed, so it is planned again; a rejected delivery waits for --retry-failed.
        if (
            failure
            and failure.get("sourceHash") == src_hash
            and not failure.get("request")
            and not options.retry_failed
        ):
            plan.skipped_failed.append((rel, str(failure.get("error"))))
            continue
        if not exists or entry.get("status") != STATUS_TRANSLATED:
            reason = "missing" if not exists else "untranslated"
        else:
            reason = "outdated"
        plan.to_submit.append((rel, reason))

    for rel in passthrough:
        if not matches_filters(rel, options.file_filters):
            continue
        plan.passthrough.append(rel)
        if passthrough_stale(lang, rel):
            plan.to_copy.append(rel)
        else:
            plan.passthrough_current += 1

    for rel in files:
        if rel in sources or rel in passthrough:
            continue
        if not options.filtered and target_file(lang, rel).exists() and not (CONTENT_DIR / rel).exists():
            plan.orphans.append(rel)
        elif not (target_file(lang, rel).exists() and not (CONTENT_DIR / rel).exists()):
            plan.unscoped.append(rel)
    return plan


# ---------------------------------------------------------------------------
# Run report
# ---------------------------------------------------------------------------


class RunReport:
    def __init__(self) -> None:
        self.per_lang: dict[str, dict[str, Any]] = {}
        self.request_failures = 0  # POST /translate/ai calls that failed with an API error
        self.notes: list[str] = []

    @property
    def failed(self) -> bool:
        return self.request_failures > 0

    def lang(self, lang: str) -> dict[str, Any]:
        return self.per_lang.setdefault(
            lang,
            {
                "translated": [],
                "repaired_files": [],
                "repaired": Counter(),
                "warnings": [],
                "copied": [],
                "failed": [],
                "removed": [],
                "chars": 0,  # characters submitted
                "billed_chars": 0,  # characters billed by the API
                "segmented": [],  # (rel, Delta) written from changed segments only
                "whole_file": [],  # (rel, reason) outdated files that were sent whole
            },
        )

    @staticmethod
    def _capped(items: list[str]) -> list[str]:
        shown = items[:REPORT_LIST_CAP]
        if len(items) > REPORT_LIST_CAP:
            shown.append(f"... and {len(items) - REPORT_LIST_CAP} more")
        return shown

    def to_markdown(self, config: TranslationConfig) -> str:
        out = [f"## Translation run ({config.environment_label}, service type `{config.service_type or 'unset'}`)", ""]
        out.append("| Language | Translated | Repaired | Warnings | Copied | Failed | Removed |")
        out.append("|---|---|---|---|---|---|---|")
        for lang, r in sorted(self.per_lang.items()):
            out.append(
                f"| {lang} | {len(r['translated'])} | {len(r['repaired_files'])} | "
                f"{len(r['warnings'])} | {len(r['copied'])} | {len(r['failed'])} | {len(r['removed'])} |"
            )
        for lang, r in sorted(self.per_lang.items()):
            if r["chars"] or r["billed_chars"]:
                out.append(f"\n{lang}: {r['chars']:,} characters submitted, {r['billed_chars']:,} billed.")
            if r["segmented"]:
                changed = sum(d.changed_chars for _, d in r["segmented"])
                total = sum(d.total_chars for _, d in r["segmented"])
                out.append(
                    f"\n{lang}: {len(r['segmented'])} file(s) updated from changed segments only "
                    f"({changed:,} of {total:,} translatable characters sent)."
                )
            if r["repaired"]:
                kinds = ", ".join(f"{n} {kind}" for kind, n in sorted(r["repaired"].items()))
                out.append(f"\n{lang}: repaired from English: {kinds} in {len(r['repaired_files'])} file(s).")
            sections: list[tuple[str, list[str]]] = [
                (f"{lang}: failed (translation kept as before)", [f"`{rel}` — {why}" for rel, why in r["failed"]]),
                (f"{lang}: written with warnings", [f"`{rel}` — {why}" for rel, why in r["warnings"]]),
                (f"{lang}: removed (English source gone)", [f"`{x}`" for x in r["removed"]]),
                (
                    f"{lang}: translated as a whole file instead of changed segments",
                    [f"`{rel}` — {why}" for rel, why in r["whole_file"]],
                ),
            ]
            for title, items in sections:
                if items:
                    out.append(f"\n### {title}\n")
                    out.extend(f"- {item}" for item in self._capped(items))
        if self.notes:
            out.append("\n### Notes\n")
            out.extend(f"- {n}" for n in self._capped(self.notes))
        return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# Commands: plan / baseline
# ---------------------------------------------------------------------------


DeltaLookup = Callable[[str, str], Delta | str | None]


def print_plan(lang: str, plan: LanguagePlan, limit: int = 0, delta_for: DeltaLookup | None = None) -> None:
    print(
        f"\n{lang}: {plan.current} current, {len(plan.to_submit)} to submit, "
        f"{len(plan.skipped_failed)} failed at this hash, {len(plan.pinned)} pinned, {len(plan.orphans)} orphaned, "
        f"{len(plan.unscoped)} unscoped, {len(plan.to_copy)} passthrough to copy "
        f"({plan.passthrough_current} passthrough current)"
    )
    # Same cut as prepare_submission, so the printed character total is what --run --limit would send.
    queue = plan.to_submit[:limit] if limit else plan.to_submit
    chars = 0
    for rel, reason in queue:
        delta = delta_for(rel, reason) if delta_for else None
        if isinstance(delta, Delta) and not delta.changed:
            print(f"  update  {'no text':<12} {rel}")
            continue
        if isinstance(delta, Delta):
            chars += delta.chars
            print(
                f"  submit  {'changed':<12} {rel} ({delta.changed}/{delta.total} units, "
                f"{delta.changed_chars:,}/{delta.total_chars:,} chars)"
            )
            continue
        content, _, _ = prepare_payload(rel, read_text(CONTENT_DIR / rel))
        chars += len(content)
        note = f" (whole file: {delta})" if delta and delta != WHOLE_FILE_TYPE else ""
        print(f"  submit  {reason:<12} {rel}{note}")
    if len(queue) < len(plan.to_submit):
        print(f"  ... {len(plan.to_submit) - len(queue)} more beyond --limit {limit}")
    for rel, error in plan.skipped_failed:
        print(f"  failed               {rel}: {error}")
    for rel in plan.pinned:
        print(f"  pinned               {rel}")
    for rel in plan.to_copy:
        print(f"  copy    passthrough  {rel}")
    for rel in plan.orphans:
        print(f"  remove  orphan       {rel}")
    for rel in plan.unscoped:
        print(f"  drop    unscoped     {rel}")
    if queue:
        print(f"  ~{chars:,} characters would be submitted for {lang}")


def file_delta(
    config: TranslationConfig, lang: str, rel: str, reason: str, entry: dict[str, Any], options: PlanOptions
) -> Delta | str | None:
    """Delta or fallback reason for an outdated file; None for files that are always sent whole."""
    if reason != "outdated" or options.force or not config.segment_diff:
        return None
    return plan_delta(config, lang, rel, entry)


def cmd_plan(
    config: TranslationConfig,
    langs: list[str],
    sources: dict[str, str],
    passthrough: dict[str, str],
    options: PlanOptions,
) -> None:
    for lang in langs:
        status = load_status(lang)

        def delta_for(rel: str, reason: str, lang: str = lang, status: dict[str, Any] = status) -> Delta | str | None:
            return file_delta(config, lang, rel, reason, status["files"].get(rel, {}), options)

        print_plan(lang, build_plan(lang, sources, passthrough, status, options), options.limit, delta_for)


def check_existing_translation(
    rel: str, source_text: str, translated_text: str
) -> tuple[str, list[str], Counter[str], list[str]]:
    """Run an existing translation through the delivery path (repair, then verify) against its
    English source. Returns (repaired text, problems, repaired counts by kind, warnings)."""
    suffix = Path(rel).suffix.lower()
    if suffix in (".yml", ".yaml"):
        src_names, tr_names = yaml_name_map(source_text), yaml_name_map(translated_text)
        problems = [] if set(src_names) == set(tr_names) else [f"toc names {len(src_names)} -> {len(tr_names)}"]
        return translated_text, problems, Counter(), []
    job = {"mode": "json-placeholders" if suffix == ".json" else "raw"}
    if suffix == ".json":
        translated_text = encode_placeholders(translated_text)
    try:
        return finalize_translation(rel, job, source_text, translated_text, repair=True, check_identity=False)
    except Exception as e:  # noqa: BLE001 - reported, never crashes the baseline
        return translated_text, [f"could not verify: {e}"], Counter(), []


def format_repairs(repaired: Counter[str]) -> str:
    return ", ".join(f"{repaired[kind]} {kind}" for kind in REPAIR_KINDS)


def cmd_baseline(
    langs: list[str],
    sources: dict[str, str],
    passthrough: dict[str, str],
    ref: str | None,
    overwrite: bool,
    repair_existing: bool = False,
    run: GitRunner = run_git,
) -> None:
    ref_hashes: dict[str, str] = {}
    sha = ""
    if ref:
        sha = resolve_git_ref(ref, run)
        print(f"baseline ref {ref} -> {sha}")
        ref_hashes = hashes_at_git_ref(sha, list(sources), run)
    verb = "repaired" if repair_existing else "would repair"
    for lang in langs:
        status = load_status(lang)
        scoped_entries = [rel for rel in status["files"] if rel in sources]
        if scoped_entries and not overwrite:
            raise SystemExit(
                f"{status_path(lang)} already tracks {len(scoped_entries)} file(s); pass --overwrite-baseline "
                "to replace the baseline."
            )
        current = outdated = missing = 0
        marked: list[tuple[str, str]] = []
        notes: list[str] = []
        repairs: Counter[str] = Counter()
        repaired_files = 0
        warned = 0
        for rel, src_hash in sources.items():
            entry = status["files"].get(rel, {})
            if entry.get("manual") is True:
                continue
            target = target_file(lang, rel)
            if not target.exists():
                status["files"][rel] = {"sourceHash": "", "status": STATUS_UNTRANSLATED}
                missing += 1
                continue
            text, problems, repaired, warnings = check_existing_translation(
                rel, read_text(CONTENT_DIR / rel), read_text(target)
            )
            if problems:
                status["files"][rel] = {"sourceHash": "", "status": STATUS_UNTRANSLATED}
                marked.append((rel, "; ".join(problems)))
                continue
            if warnings:
                warned += 1
                notes.append(f"  {'warning':<13} {rel}: {'; '.join(warnings)}")
            if repaired:
                repairs.update(repaired)
                repaired_files += 1
                notes.append(f"  {verb:<13} {rel}: {format_repairs(repaired)}")
                if repair_existing:
                    write_text(target, text)
            if ref and rel not in ref_hashes:
                notes.append(f"  new           {rel}: not in content/ at {ref}; baselined at the current hash")
            baseline_hash = ref_hashes.get(rel, src_hash) if ref else src_hash
            ref_blob = blob_at_git_ref(sha, rel, run) if ref and rel in ref_hashes else None
            status["files"][rel] = source_entry(rel, baseline_hash, STATUS_TRANSLATED, run, ref_blob)
            if baseline_hash == src_hash:
                current += 1
            else:
                outdated += 1
                marked.append((rel, f"English changed since {ref}"))
        for rel in list(status["files"]):
            if rel not in sources and rel not in passthrough:
                status["files"].pop(rel)
                print(f"{lang}: dropped unscoped entry {rel}")
        save_status(lang, status)
        print(
            f"\n{lang}: baseline written — {current} current, {outdated} changed since {ref or 'HEAD'}, "
            f"{len(marked) - outdated} structurally stale, {missing} missing, {repaired_files} {verb}, "
            f"{warned} accepted with inline-code warnings"
        )
        for line in notes:
            print(line)
        if repaired_files:
            hint = "" if repair_existing else " (pass --repair-existing to write the repaired text)"
            print(f"  {lang}: {verb} {repaired_files} file(s): {format_repairs(repairs)}{hint}")
        for rel, why in marked:
            print(f"  outdated      {rel}: {why}")


def cmd_migrate_blobs(langs: list[str], sources: dict[str, str], run: GitRunner = run_git) -> None:
    """Record sourceBlob for status entries that only have a sourceHash (entries from before
    segment-level updates). The blob is the English version whose content hashes to sourceHash.
    Passthrough files are copied, never diffed, and are skipped."""
    if not in_git_work_tree(run):
        raise SystemExit("--migrate-blobs needs a git work tree with the history of content/.")
    found: dict[tuple[str, str], tuple[str, bytes] | None] = {}
    for lang in langs:
        status = load_status(lang)
        recorded = kept = 0
        missing: list[str] = []
        for rel, entry in status["files"].items():
            source_hash = str(entry.get("sourceHash") or "")
            if rel not in sources or not source_hash:
                continue
            blob = entry.get("sourceBlob")
            if isinstance(blob, str) and blob:
                data = read_git_blob(blob, run)
                if data is not None and hash_bytes(data) == source_hash:
                    kept += 1
                    continue
            key = (rel, source_hash)
            if key not in found:
                found[key] = find_source_blob(rel, source_hash, run)
            match = found[key]
            if match is None:
                missing.append(rel)
                continue
            rest = {k: v for k, v in entry.items() if k not in ("sourceHash", "sourceBlob")}
            status["files"][rel] = {"sourceHash": source_hash, "sourceBlob": match[0], **rest}
            recorded += 1
        save_status(lang, status)
        print(f"\n{lang}: sourceBlob recorded for {recorded}, already valid for {kept}, not found for {len(missing)}")
        for rel in missing:
            print(f"  not found     {rel}: no English version in git hashes to the recorded sourceHash")


def status_at_ref(ref: str, lang: str, run: GitRunner = run_git) -> dict[str, Any]:
    """The status file of a language at a git ref; empty sections when the file is missing there."""
    proc = run(["git", "show", f"{ref}:{status_path(lang).as_posix()}"])
    status: dict[str, Any] = json.loads(proc.stdout.decode("utf-8")) if proc.returncode == 0 else {}
    status.setdefault("files", {})
    status.setdefault("failures", {})
    return status


def merge_entries(base: dict[str, Any], ours: dict[str, Any], theirs: dict[str, Any]) -> tuple[dict[str, Any], int]:
    """Three-way merge of one status section. An entry the translation branch (theirs) added, changed or
    removed since the merge base comes from the branch; every other entry comes from ours, so an entry
    the branch merely carries in an older state never overwrites a newer one. Returns (merged, taken)."""
    merged: dict[str, Any] = {}
    taken = 0
    for key in [*ours, *(k for k in theirs if k not in ours), *(k for k in base if k not in ours and k not in theirs)]:
        if theirs.get(key) != base.get(key):
            taken += 1
            if key in theirs:
                merged[key] = theirs[key]
        elif key in ours:
            merged[key] = ours[key]
    return merged, taken


def cmd_merge_status(langs: list[str], ours_ref: str, theirs_ref: str, run: GitRunner = run_git) -> None:
    """Rebuild each status file after the translation branch was merged into the run's tree. A text merge
    (-X theirs) resolves conflicting hunks of the JSON from the branch; this keeps main's entries the branch
    did not touch."""
    if not in_git_work_tree(run):
        raise SystemExit("--merge-status needs a git work tree.")
    ours_sha, theirs_sha = resolve_git_ref(ours_ref, run), resolve_git_ref(theirs_ref, run)
    proc = run(["git", "merge-base", ours_sha, theirs_sha])
    if proc.returncode != 0:
        raise SystemExit(f"--merge-status: {ours_ref} and {theirs_ref} have no merge base.")
    base_sha = proc.stdout.decode("utf-8").strip()
    for lang in langs:
        base, ours, theirs = (status_at_ref(sha, lang, run) for sha in (base_sha, ours_sha, theirs_sha))
        status = load_status(lang)
        status["files"], taken = merge_entries(base["files"], ours["files"], theirs["files"])
        status["failures"], _ = merge_entries(base["failures"], ours["failures"], theirs["failures"])
        save_status(lang, status)
        print(f"{lang}: {taken} status entries taken from {theirs_ref}, the others from {ours_ref}")


# ---------------------------------------------------------------------------
# Commands: run / dump-orders
# ---------------------------------------------------------------------------


@dataclass
class LanguageSubmission:
    lang: str
    locale: str
    status: dict[str, Any]
    plan: LanguagePlan
    orders: list[dict[str, Any]] = field(default_factory=list)
    jobs: dict[str, dict[str, Any]] = field(default_factory=dict)  # rel -> pending job record
    empty_copies: list[str] = field(default_factory=list)  # nothing translatable: copied through
    deltas: dict[str, Delta] = field(default_factory=dict)  # rel -> segment-level update sent in its order
    local_deltas: dict[str, Delta] = field(default_factory=dict)  # changes without translatable text
    whole_file: list[tuple[str, str]] = field(default_factory=list)  # outdated files sent whole, with the reason

    @property
    def chars(self) -> int:
        return sum(int(j["chars"]) for j in self.jobs.values())


def build_order(
    config: TranslationConfig,
    id_content: str,
    content: str,
    content_type: str,
    locale: str,
    segments: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    # /translate/ai body: one object per file, target_language singular, content a list of
    # {id, text, translatable} segments: the whole file as one segment, or the given segments.
    order: dict[str, Any] = {
        "id_content": id_content,
        "source_language": config.source_locale,
        "target_language": locale,
        "content_type": content_type,
        "service_type": config.service_type,
        "content": segments if segments is not None else [{"id": "s1", "text": content, "translatable": True}],
    }
    if config.instructions:
        order["context"] = {"instructions": config.instructions}
    return order


def prepare_submission(
    config: TranslationConfig,
    lang: str,
    locale: str,
    sources: dict[str, str],
    passthrough: dict[str, str],
    options: PlanOptions,
) -> LanguageSubmission:
    """Plan one language and build its /translate/ai orders without touching anything."""
    status = load_status(lang)
    plan = build_plan(lang, sources, passthrough, status, options)
    sub = LanguageSubmission(lang, locale, status, plan)
    queue = plan.to_submit[: options.limit] if options.limit else plan.to_submit
    for rel, reason in queue:
        id_content = f"{lang}/{rel}"
        failure = status["failures"].get(rel, {})
        if options.retry_failed and failure.get("segmentUpdate") and failure.get("sourceHash") == sources[rel]:
            delta: Delta | str | None = "retry of a failed segment update"
        else:
            delta = file_delta(config, lang, rel, reason, status["files"].get(rel, {}), options)
        if isinstance(delta, Delta):
            if not delta.changed:
                sub.local_deltas[rel] = delta
                continue
            sub.orders.append(build_order(config, id_content, "", "text/plain", locale, delta.items))
            sub.jobs[rel] = {
                "mode": delta.mode,
                "idContent": id_content,
                "sourceHash": sources[rel],
                "reason": "changed",
                "contentType": "text/plain",
                "chars": delta.chars,
            }
            sub.deltas[rel] = delta
            continue
        if delta is not None and delta != WHOLE_FILE_TYPE:
            sub.whole_file.append((rel, delta))
        content, content_type, info = prepare_payload(rel, read_text(CONTENT_DIR / rel))
        if not content.strip() or info.get("units") == 0:
            sub.empty_copies.append(rel)
            continue
        sub.orders.append(build_order(config, id_content, content, content_type, locale))
        sub.jobs[rel] = {
            **info,
            "idContent": id_content,
            "sourceHash": sources[rel],
            "reason": reason,
            "contentType": content_type,
            "chars": len(content),
        }
    return sub


def enforce_sandbox_caps(
    config: TranslationConfig, submissions: list[LanguageSubmission], allow_unbounded: bool
) -> None:
    if not config.is_sandbox or allow_unbounded:
        return
    files = sum(len(s.jobs) for s in submissions)
    chars = sum(s.chars for s in submissions)
    if files > config.max_files_per_run or chars > config.max_chars_per_run:
        raise SystemExit(
            f"Refusing to submit {files} file(s) / {chars:,} characters to the sandbox in one run "
            f"(limits: {config.max_files_per_run} files, {config.max_chars_per_run:,} characters). "
            "Narrow with --limit/--file or pass --allow-unbounded."
        )


def apply_local_changes(
    sub: LanguageSubmission, sources: dict[str, str], passthrough: dict[str, str], r: dict[str, Any]
) -> None:
    """Orphan removal, unscoped cleanup, passthrough and empty-file copies; saved right away."""
    lang, status, plan = sub.lang, sub.status, sub.plan
    for rel in plan.orphans:
        target_file(lang, rel).unlink()
        for section in ("files", "failures"):
            status[section].pop(rel, None)
        r["removed"].append(rel)
        print(f"{lang}: removed orphan {rel}")
    for rel in plan.unscoped:
        status["files"].pop(rel, None)
        print(f"{lang}: dropped unscoped status entry {rel}")
    for rel in plan.passthrough:
        if rel in plan.to_copy:
            target = target_file(lang, rel)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(CONTENT_DIR / rel, target)
            r["copied"].append(rel)
            print(f"{lang}: copied passthrough {rel}")
        # Always (re)record the entry so legacy "translated" tags on passthrough files become "copied".
        status["files"][rel] = source_entry(rel, passthrough[rel], STATUS_COPIED)
    for rel in sub.empty_copies:
        write_text(target_file(lang, rel), read_text(CONTENT_DIR / rel))
        status["files"][rel] = source_entry(rel, sources[rel], STATUS_TRANSLATED)
        status["failures"].pop(rel, None)
    save_status(lang, status)


def billed_chars(data: list[dict[str, Any]]) -> int:
    return sum(int(d["billed_chars"]) for d in data if isinstance(d.get("billed_chars"), (int, float)))


def write_delivery(
    lang: str,
    rel: str,
    source_hash: str,
    text: str,
    problems: list[str],
    warnings: list[str],
    status: dict[str, Any],
    lenient: bool,
    structured: bool,
) -> list[str]:
    """Write a verified delivery and record it. Returns the problems that rejected it (empty when written).
    --lenient only makes sense for raw Markdown/HTML, where the assembled text is still usable.
    A structured payload (toc names, UI strings) with problems rebuilds to English or nothing."""
    if problems and (not lenient or not text or structured):
        if lenient:
            why = "no usable text" if not text else "structured payload cannot be written partially"
            print(f"{lang}: --lenient ignored for {rel}: {why}")
        record_failure(status, rel, "; ".join(problems), source_hash)
        return problems
    write_text(target_file(lang, rel), text)
    status["files"][rel] = source_entry(rel, source_hash, STATUS_TRANSLATED)
    status["failures"].pop(rel, None)
    if problems:
        print(f"{lang}: written despite problems ({'; '.join(problems)}): {rel}")
    if warnings:
        print(f"{lang}: written with warnings ({'; '.join(warnings)}): {rel}")
    return []


def apply_translation(
    lang: str,
    rel: str,
    job: dict[str, Any],
    translated: Any,
    status: dict[str, Any],
    lenient: bool,
) -> tuple[list[str], Counter[str], list[str]]:
    """Repair, verify and write one translation. Returns (problems, repaired counts, warnings).
    Problems reject the translation (unless --lenient); warnings are written and reported."""
    job_hash = str(job.get("sourceHash", ""))
    if not isinstance(translated, str) or not translated:
        record_failure(status, rel, "no translation in the response", job_hash)
        return ["no translation in the response"], Counter(), []
    spans = job.get("codeSpans")
    if isinstance(spans, list):
        translated, mask_problems = unmask_code(translated, spans)
        if mask_problems:
            record_failure(status, rel, "; ".join(mask_problems), job_hash)
            return mask_problems, Counter(), []
    try:
        text, problems, repaired, warnings = finalize_translation(rel, job, read_text(CONTENT_DIR / rel), translated)
    except Exception as e:  # noqa: BLE001 - reported to the reviewer, never crashes the run
        record_failure(status, rel, f"could not reinsert translation: {e}", job_hash)
        return [f"could not reinsert translation: {e}"], Counter(), []
    structured = job.get("mode") in ("yaml-names", "json-placeholders")
    rejected = write_delivery(lang, rel, job_hash, text, problems, warnings, status, lenient, structured)
    return rejected, repaired, warnings


def apply_delta(
    lang: str,
    rel: str,
    source_hash: str,
    delta: Delta,
    translations: dict[str, str],
    status: dict[str, Any],
    lenient: bool,
) -> tuple[list[str], Counter[str], list[str]]:
    """Rebuild one file from reused, translated and English blocks, verify and write it."""
    try:
        text, problems, repaired, warnings = delta.assemble(translations)
    except Exception as e:  # noqa: BLE001 - reported to the reviewer, never crashes the run
        record_failure(status, rel, f"could not reassemble translation: {e}", source_hash, segmentUpdate=True)
        return [f"could not reassemble translation: {e}"], Counter(), []
    structured = delta.mode != "md-blocks"
    rejected = write_delivery(lang, rel, source_hash, text, problems, warnings, status, lenient, structured)
    if rejected:
        status["failures"][rel]["segmentUpdate"] = True
    return rejected, repaired, warnings


def record_result(
    lang: str,
    rel: str,
    r: dict[str, Any],
    problems: list[str],
    repaired: Counter[str],
    warnings: list[str],
    done: str,
) -> None:
    if problems:
        r["failed"].append((rel, "; ".join(problems)))
        print(f"{lang}: REJECTED {rel}: {'; '.join(problems)}")
        return
    r["translated"].append(rel)
    if repaired:
        r["repaired"].update(repaired)
        r["repaired_files"].append(rel)
    if warnings:
        r["warnings"].append((rel, "; ".join(warnings)))
    suffix = f" (repaired {dict(repaired)})" if repaired else ""
    print(f"{lang}: {done}{suffix}")


def translate_language(
    client: TranslationClient,
    sub: LanguageSubmission,
    sources: dict[str, str],
    passthrough: dict[str, str],
    lenient: bool,
    report: RunReport,
    rejected_dir: Path | None = None,
) -> None:
    """One synchronous /translate/ai request per planned file: translate, repair, verify, write.
    The status file is saved after every file so an interrupted run loses no billed work. A rejected
    key stops the run (TranslatedAuthError) before anything else is recorded for the file."""
    lang, status = sub.lang, sub.status
    r = report.lang(lang)
    apply_local_changes(sub, sources, passthrough, r)
    r["whole_file"].extend(sub.whole_file)
    orders = {str(o["id_content"]): o for o in sub.orders}
    try:
        for rel, local in sub.local_deltas.items():
            problems, repaired, warnings = apply_delta(lang, rel, sources[rel], local, {}, status, lenient)
            if not problems:
                r["segmented"].append((rel, local))
            record_result(lang, rel, r, problems, repaired, warnings, f"updated {rel} (no changed text to translate)")
        save_status(lang, status)
        for rel, job in sub.jobs.items():
            order = orders[job["idContent"]]
            try:
                data = client.translate_ai(order)
            except TranslatedAuthError:
                raise
            except TranslatedApiError as e:
                report.request_failures += 1
                record_failure(
                    status, rel, f"POST translate/ai failed: {e}", job["sourceHash"], apiError=e.details(), request=True
                )
                r["failed"].append((rel, f"POST translate/ai failed: {e}"))
                print(f"{lang}: FAILED {rel}: {e}")
                save_status(lang, status)
                continue
            r["chars"] += int(job["chars"])
            r["billed_chars"] += billed_chars(data)
            delta = sub.deltas.get(rel)
            if delta is None:
                translated = data[0].get("translation") if data else None
                problems, repaired, warnings = apply_translation(lang, rel, job, translated, status, lenient)
                done = f"translated {rel} ({job['reason']}, {job['chars']:,} chars)"
            else:
                translations = map_segment_translations(order["content"], data)
                if isinstance(translations, str):
                    record_failure(status, rel, translations, job["sourceHash"], segmentUpdate=True)
                    problems, repaired, warnings = [translations], Counter(), []
                else:
                    problems, repaired, warnings = apply_delta(
                        lang, rel, job["sourceHash"], delta, translations, status, lenient
                    )
                if not problems:
                    r["segmented"].append((rel, delta))
                done = (
                    f"translated {rel} (changed segments {delta.changed}/{delta.total}, "
                    f"{delta.changed_chars:,}/{delta.total_chars:,} chars)"
                )
            record_result(lang, rel, r, problems, repaired, warnings, done)
            if problems and rejected_dir is not None:
                kept = keep_rejected(rejected_dir, lang, rel, order, data, problems)
                print(f"{lang}: kept the rejected delivery of {rel} in {kept}")
            save_status(lang, status)
    finally:
        save_status(lang, status)


def keep_rejected(
    out_dir: Path, lang: str, rel: str, order: dict[str, Any], data: list[dict[str, Any]], problems: list[str]
) -> Path:
    """Save a billed delivery that failed verification, so it can be repaired by hand instead of bought again."""
    path = out_dir / lang / f"{rel}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {"language": lang, "file": rel, "problems": problems, "order": order, "response": data}
    path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def prepare_all(
    config: TranslationConfig,
    langs: list[str],
    sources: dict[str, str],
    passthrough: dict[str, str],
    locales: dict[str, str],
    options: PlanOptions,
    allow_unbounded: bool,
) -> list[LanguageSubmission]:
    require_locales(langs, locales)
    submissions = [prepare_submission(config, lang, locales[lang], sources, passthrough, options) for lang in langs]
    enforce_sandbox_caps(config, submissions, allow_unbounded)
    return submissions


def cmd_run(
    config: TranslationConfig,
    client: TranslationClient,
    langs: list[str],
    sources: dict[str, str],
    passthrough: dict[str, str],
    locales: dict[str, str],
    options: PlanOptions,
    allow_unbounded: bool,
    lenient: bool,
    report: RunReport,
    rejected_dir: Path | None = None,
) -> None:
    for sub in prepare_all(config, langs, sources, passthrough, locales, options, allow_unbounded):
        translate_language(client, sub, sources, passthrough, lenient, report, rejected_dir)


def cmd_dump_orders(
    config: TranslationConfig,
    out_dir: Path,
    langs: list[str],
    sources: dict[str, str],
    passthrough: dict[str, str],
    locales: dict[str, str],
    options: PlanOptions,
    allow_unbounded: bool,
) -> None:
    submissions = prepare_all(config, langs, sources, passthrough, locales, options, allow_unbounded)
    summary: dict[str, Any] = {
        "environment": config.environment_label,
        "baseUrl": config.base_url,
        "serviceType": config.service_type,
        "languages": {},
    }
    for sub in submissions:
        for order in sub.orders:
            rel = str(order["id_content"]).split("/", 1)[1]
            path = out_dir / sub.lang / f"{rel}.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(order, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        summary["languages"][sub.lang] = {
            "orders": len(sub.orders),
            "characters": sub.chars,
            "passthroughCopies": sub.plan.to_copy,
            "emptyCopies": sub.empty_copies,
            "segmented": {
                rel: {"units": f"{d.changed}/{d.total}", "chars": f"{d.changed_chars}/{d.total_chars}"}
                for rel, d in sub.deltas.items()
            },
            "localUpdates": sorted(sub.local_deltas),
            "wholeFile": dict(sub.whole_file),
            "orphans": sub.plan.orphans,
            "unscoped": sub.plan.unscoped,
            "pinned": sub.plan.pinned,
            "skippedFailed": [rel for rel, _ in sub.plan.skipped_failed],
        }
        print(f"{sub.lang}: {len(sub.orders)} order(s), {sub.chars:,} characters -> {out_dir / sub.lang}")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"summary -> {out_dir / 'summary.json'} (nothing was sent; status files untouched)")


# ---------------------------------------------------------------------------
# Commands: probe
# ---------------------------------------------------------------------------


def cmd_probe(config: TranslationConfig, client: TranslationClient, langs: list[str], locales: dict[str, str]) -> int:
    service_types = client.service_type_names()
    languages = client.languages()
    names = [str(s.get("name")) for s in service_types]
    print(f"\n{len(service_types)} service type(s):")
    for s in service_types:
        flags = [k.replace("_enabled", "") for k in ("human_enabled", "machine_enabled") if s.get(k)]
        print(f"  {s.get('name')}" + (f"  [{', '.join(flags)}]" if flags else ""))
    keys = [str(lang_item.get("key")) for lang_item in languages]
    print(f"\n{len(languages)} language(s): {', '.join(keys)}")
    ok = True
    wanted = {"sourceLocale": config.source_locale}
    wanted.update({f"translatedLocale[{lang}]": locales.get(lang, "<missing>") for lang in langs})
    for what, code in wanted.items():
        if code in keys:
            print(f"OK   {what} = {code}")
        else:
            ok = False
            print(
                f"FAIL {what} = {code} is not in /symbol/languages; closest: {difflib.get_close_matches(code, keys, 5)}"
            )
    if config.service_type:
        if config.service_type in names:
            print(f"OK   service type '{config.service_type}' exists")
        else:
            ok = False
            print(
                f"FAIL service type '{config.service_type}' is not in /symbol/service-type-names; "
                f"closest: {difflib.get_close_matches(config.service_type, names, 5)}"
            )
    else:
        print("NOTE no service type resolved; set TRANSLATED_SERVICE_TYPE to one of the names above")
    return 0 if ok else 1


# ---------------------------------------------------------------------------
# Self-test (offline; no key, no network)
# ---------------------------------------------------------------------------


class SelfTest:
    def __init__(self) -> None:
        self.passed = 0
        self.failures: list[str] = []

    def check(self, name: str, ok: bool, detail: str = "") -> None:
        if ok:
            self.passed += 1
            print(f"  ok    {name}")
        else:
            self.failures.append(name)
            print(f"  FAIL  {name}" + (f" -- {detail[:300]}" if detail else ""))

    def expect_raises(self, name: str, fn: Callable[[], object], error: type[BaseException]) -> None:
        try:
            fn()
        except error:
            self.check(name, True)
            return
        self.check(name, False, f"no {error.__name__} raised")

    def expect_exit(self, name: str, fn: Callable[[], object], fragment: str = "") -> None:
        try:
            fn()
        except SystemExit as e:
            self.check(name, fragment in str(e), f"message: {e}")
            return
        self.check(name, False, "no SystemExit raised")

    def section(self, title: str) -> None:
        print(f"\n[{title}]")


def captured(fn: Callable[[], object]) -> str:
    """Run fn and return what it printed to stdout."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        fn()
    return buf.getvalue()


FIXTURE_MD = (
    BOM + "---\ntitle: Getting started\ndescription: Intro to TE3\nuid: getting-started\nauthor: Nedas\n---\n"
    "# Getting started\n\nOpen `View → Options` and read [the guide](guide.md).\n\n"
    "> [!NOTE]\n> Use `Selected.Tables` here.\n\n"
    "```csharp\n// Assembly references must be at the very top\nvar x = 1;\n```\n\n"
    "## Next steps\n\nSee [next](next.md#anchor) and [!include[part](includes/part.md)].\n"
)
FIXTURE_JSON = '{\n  "greeting": "Hello {name}, {count} items",\n  "bye": "Bye"\n}\n'
FIXTURE_TOC = (
    BOM
    + "- name: Home\n  href: index.md\n- name: Getting started\n  href: getting-started/\n  items:\n  - name: Install\n    href: install.md\n"
)
FIXTURE_HTML = '<html>\n<body>\n<a href="page.html">Go</a>\n<img src="img/a.png">\n<p>Text</p>\n</body>\n</html>\n'


def fin(
    source: str, delivered: str, rel: str = "x.md", check_identity: bool = False, repair: bool = True
) -> tuple[str, list[str], Counter[str], list[str]]:
    _, _, info = prepare_payload(rel, source)
    return finalize_translation(rel, info, source, delivered, repair=repair, check_identity=check_identity)


def selftest_corpus(t: SelfTest, config: TranslationConfig) -> None:
    t.section("corpus identity round-trip (prepare_payload -> finalize_translation)")
    sources = get_scoped_sources(config)
    bad: list[str] = []
    for rel in sources:
        text = read_text(CONTENT_DIR / rel)
        content, _, info = prepare_payload(rel, text)
        try:
            delivered, mask_problems = unmask_code(content, info.get("codeSpans", []))
            if mask_problems:
                bad.append(f"{rel}: {mask_problems}")
                continue
            out, problems, repaired, warnings = finalize_translation(rel, info, text, delivered, check_identity=False)
        except Exception as e:  # noqa: BLE001
            bad.append(f"{rel}: raised {e}")
            continue
        if out != text or problems or repaired or warnings:
            bad.append(f"{rel}: {'differs' if out != text else ''} {problems} {dict(repaired)} {warnings}")
    t.check(f"{len(sources)} scoped sources round-trip byte-for-byte with zero problems", not bad, "; ".join(bad[:5]))
    passthrough = get_passthrough_sources(config, sources)
    t.check("passthrough files are outside the translation scope", not set(passthrough) & set(sources))

    t.section("corpus segmentation (segment -> join, unchanged page rebuilds to itself)")
    md_sources = [rel for rel in sources if rel.endswith(".md")]
    bad = []
    for rel in md_sources:
        text = read_text(CONTENT_DIR / rel)
        fm, body = split_frontmatter(to_lf(text.lstrip(BOM)))
        seg = segment(body)
        if seg.join() != body:
            bad.append(f"{rel}: segment/join differs")
            continue
        # Stand-in translation: " (es)" after the first line of every translatable block.
        marked = [b.text.replace("\n", " (es)\n", 1) if b.translatable else b.text for b in seg.blocks]
        translation = fm + seg.join(marked)
        delta = md_delta(text, text, translation)
        if isinstance(delta, str) or delta.changed:
            bad.append(f"{rel}: {delta if isinstance(delta, str) else f'{delta.changed} changed unit(s)'}")
            continue
        out, problems, _, _ = delta.assemble({})
        expected = (BOM if text.startswith(BOM) else "") + translation
        if "\r\n" in text:
            expected = expected.replace("\n", "\r\n")
        if out != expected or problems:
            bad.append(f"{rel}: {'differs' if out != expected else ''} {problems}")
    t.check(
        f"{len(md_sources)} Markdown sources segment, and an unchanged page rebuilds its translation byte-for-byte",
        not bad,
        "; ".join(bad[:5]),
    )


def selftest_fixtures(t: SelfTest) -> None:
    t.section("markdown repair-then-verify")
    identity = FIXTURE_MD.lstrip(BOM)
    out, problems, repaired, _ = fin(FIXTURE_MD, identity)
    t.check(
        "identity delivery reproduces the source (BOM restored)", out == FIXTURE_MD and not problems and not repaired
    )
    _, problems, _, _ = fin(FIXTURE_MD, identity.replace("## Next steps\n", ""))
    t.check("dropped heading -> problem", any("headings" in p for p in problems), str(problems))
    out, problems, repaired, _ = fin(FIXTURE_MD, identity.replace("(guide.md)", "(guia.md)"))
    t.check(
        "changed link target (equal count) -> repaired", out == FIXTURE_MD and not problems and repaired["links"] == 1
    )
    _, problems, _, _ = fin(FIXTURE_MD, identity + "\n[more](extra.md)\n")
    t.check("extra link -> problem", any("link targets" in p for p in problems), str(problems))
    _, problems, _, _ = fin(FIXTURE_MD, identity.replace("var x = 1;\n```\n", "var x = 1;\n"))
    t.check("missing fence line -> problem", any("code fences" in p for p in problems), str(problems))
    out, problems, repaired, _ = fin(FIXTURE_MD, identity.replace("// Assembly references", "// Las referencias"))
    t.check(
        "translated fenced comment -> restored to English",
        out == FIXTURE_MD and not problems and repaired["fences"] == 1,
    )
    out, problems, repaired, _ = fin(FIXTURE_MD, identity.replace("`View → Options`", "`Ver → Opciones`"))
    t.check(
        "changed inline code (equal count) -> repaired",
        out == FIXTURE_MD and not problems and repaired["inline code"] == 1,
    )
    dropped_span = identity.replace("`Selected.Tables`", "Selected.Tables")
    out, problems, repaired, warnings = fin(FIXTURE_MD, dropped_span)
    t.check(
        "dropped inline code span -> problem (the code was lost)",
        problems == ["inline code spans 2 -> 1 (missing ['`Selected.Tables`'], added [])"] and not warnings,
        f"{problems} {warnings}",
    )
    extra_span = identity.replace("Open `View", "Open `true` `View")
    out, problems, _, warnings = fin(FIXTURE_MD, extra_span)
    t.check(
        "added inline code span -> warning, not a problem; delivered text kept",
        not problems
        and warnings == ["inline code spans 2 -> 3 (missing [], added ['`true`'])"]
        and out == BOM + extra_span,
        f"{problems} {warnings}",
    )
    out, problems, repaired, warnings = fin(FIXTURE_MD, extra_span.replace("(guide.md)", "(guia.md)"))
    t.check(
        "an added inline code span does not block the other repairs (link target still restored)",
        not problems and len(warnings) == 1 and repaired["links"] == 1 and out == BOM + extra_span,
        f"{problems} {warnings} {dict(repaired)}",
    )
    _, problems, _, warnings = fin(FIXTURE_MD, extra_span, repair=False)
    t.check(
        "an added inline code span is a warning in verify-only mode too",
        not problems and len(warnings) == 1,
        str(problems),
    )
    _, problems, _, warnings = fin(FIXTURE_MD, dropped_span, repair=False)
    t.check("a dropped inline code span is a problem in verify-only mode too", len(problems) == 1, str(problems))
    out, problems, repaired, _ = fin(FIXTURE_MD, identity.replace("[!NOTE]", "[!NOTA]"))
    t.check(
        "[!NOTE] -> [!NOTA] (equal count) -> repaired", out == FIXTURE_MD and not problems and repaired["markers"] == 1
    )
    out, problems, _, _ = fin(FIXTURE_MD, identity.replace("[!NOTE]", "[!note]"))
    t.check("[!note] lowercase -> repaired to [!NOTE]", out == FIXTURE_MD and not problems)
    _, problems, _, _ = fin(FIXTURE_MD, identity.replace("> [!NOTE]\n", "> NOTE\n"))
    t.check("dropped alert marker -> problem", any("markers" in p for p in problems), str(problems))
    out, problems, _, _ = fin(
        FIXTURE_MD,
        identity.replace("uid: getting-started\nauthor: Nedas", "uid: empezar\nauthor: Pedro").replace(
            "title: Getting started", "title: Empezar"
        ),
    )
    t.check(
        "uid/author rewritten -> restored from English, title kept",
        "uid: getting-started\nauthor: Nedas" in out and "title: Empezar\n" in out and not problems,
    )
    out, problems, _, _ = fin(FIXTURE_MD, identity.replace("title: Getting started", "title: Guía: introducción"))
    t.check("title gaining ': ' -> quoted", 'title: "Guía: introducción"\n' in out and not problems, out[:80])
    out, _, _, _ = fin(FIXTURE_MD, identity.replace("title: Getting started", "title: Scripts de C#"))
    t.check("title with '#' -> quoted", 'title: "Scripts de C#"\n' in out)
    _, problems, _, _ = fin(FIXTURE_MD, identity.replace("description: Intro to TE3\n", ""))
    t.check("description dropped from frontmatter -> problem", any("description" in p for p in problems), str(problems))
    _, problems, _, _ = fin(FIXTURE_MD, identity.split("---\n", 2)[2])
    t.check("frontmatter dropped -> problem", any("frontmatter missing" in p for p in problems), str(problems))
    out, problems, _, _ = fin(FIXTURE_MD, "\n" + identity)
    t.check("blank line before frontmatter -> tolerated", out == FIXTURE_MD and not problems)
    out, problems, _, _ = fin(FIXTURE_MD, identity)
    t.check("BOM stripped by translator -> restored", out.startswith(BOM))
    crlf_src = FIXTURE_MD.replace("\n", "\r\n")
    out, problems, _, _ = fin(crlf_src, identity)
    t.check("LF delivery for a CRLF source -> CRLF restored", out == crlf_src and not problems)
    out, problems, _, _ = fin(FIXTURE_MD, identity.replace("\n", "\r\n"))
    t.check("CRLF delivery for an LF source -> LF", out == FIXTURE_MD and not problems)
    out, problems, _, _ = fin(FIXTURE_MD, identity.rstrip("\n"))
    t.check("trailing newline restored", out == FIXTURE_MD and not problems)
    long_src = "# T\n\n" + ("The quick brown fox jumps over the lazy dog. " * 8) + "\n"
    _, problems, _, _ = fin(long_src, long_src, check_identity=True)
    t.check(
        "delivered body identical to source (>200 letters) -> problem",
        any("identical" in p for p in problems),
        str(problems),
    )
    _, problems, _, _ = fin(long_src, long_src.replace("quick", "rápido"), check_identity=True)
    t.check("translated long body -> no identity problem", not problems, str(problems))
    _, problems, _, _ = fin(FIXTURE_MD, identity, check_identity=True)
    t.check("short identical body (<200 letters) -> accepted", not problems, str(problems))
    _, problems, _, _ = fin(FIXTURE_MD, identity.replace("// Assembly references", "// Las referencias"), repair=False)
    t.check(
        "verify-only mode reports fenced differences instead of repairing",
        any("fenced code differs" in p for p in problems),
        str(problems),
    )

    t.section("json (_ui-strings.json)")
    payload, _, info = prepare_payload("_ui-strings.json", FIXTURE_JSON)
    t.check(
        "{name} encoded as {{name}} in the payload",
        "{{name}}" in payload and "{{count}}" in payload and "{name}" not in payload.replace("{{name}}", ""),
    )
    out, problems, _, _ = finalize_translation("_ui-strings.json", info, FIXTURE_JSON, payload)
    t.check("json identity round-trip", out == FIXTURE_JSON and not problems, str(problems))
    _, problems, _, _ = finalize_translation(
        "_ui-strings.json", info, FIXTURE_JSON, '{\n  "greeting": "Hola {{name}}, {{count}} items"\n}\n'
    )
    t.check("json key dropped -> problem", any("keys differ" in p for p in problems), str(problems))
    _, problems, _, _ = finalize_translation(
        "_ui-strings.json", info, FIXTURE_JSON, payload.replace("{{count}}", "{{recuento}}")
    )
    t.check(
        "{count} translated to {recuento} -> problem after decode",
        any("placeholders" in p for p in problems),
        str(problems),
    )
    _, problems, _, _ = finalize_translation(
        "_ui-strings.json", info, FIXTURE_JSON, payload.replace("{{count}}", "{count}")
    )
    t.check("single-brace placeholder returned unencoded -> still accepted", not problems, str(problems))
    out, problems, _, _ = finalize_translation("_ui-strings.json", info, BOM + FIXTURE_JSON, BOM + payload)
    t.check("json BOM handling", out == BOM + FIXTURE_JSON and not problems)
    _, problems, _, _ = finalize_translation("_ui-strings.json", info, FIXTURE_JSON, "not json")
    t.check("unparseable json -> problem", any("does not parse" in p for p in problems))

    t.section("toc.yml (yaml-names)")
    payload, _, info = prepare_payload("toc.yml", FIXTURE_TOC)
    names = json.loads(payload)
    t.check(
        "toc payload holds only names",
        set(names.values()) == {"Home", "Getting started", "Install"}
        and all(YAML_NAME_KEY_RE.fullmatch(k) for k in names),
    )
    out, problems, _, _ = finalize_translation("toc.yml", info, FIXTURE_TOC, payload)
    t.check("toc identity round-trip (BOM kept)", out == FIXTURE_TOC and not problems, str(problems))
    crlf_toc = FIXTURE_TOC.replace("\n", "\r\n")
    out, problems, _, _ = finalize_translation("toc.yml", info, crlf_toc, payload)
    t.check("toc CRLF source round-trip", out == crlf_toc and not problems)
    out, problems, _, _ = finalize_translation("toc.yml", info, FIXTURE_TOC, BOM + payload)
    t.check("toc payload with BOM -> parsed", out == FIXTURE_TOC and not problems, str(problems))
    translated = dict(names)
    key_home = next(k for k, v in names.items() if v == "Home")
    translated[key_home] = "Inicio: página"
    out, problems, _, _ = finalize_translation("toc.yml", info, FIXTURE_TOC, json.dumps(translated))
    t.check("toc name gaining ': ' -> quoted", '- name: "Inicio: página"\n' in out and not problems, out)
    translated[key_home] = "true"
    out, _, _, _ = finalize_translation("toc.yml", info, FIXTURE_TOC, json.dumps(translated))
    t.check("toc name 'true' -> quoted", '- name: "true"\n' in out)
    translated[key_home] = "- Inicio"
    out, _, _, _ = finalize_translation("toc.yml", info, FIXTURE_TOC, json.dumps(translated))
    t.check("toc name starting with '-' -> quoted", '- name: "- Inicio"\n' in out)
    translated[key_home] = "Inicio"
    _, problems, _, _ = finalize_translation(
        "toc.yml", info, FIXTURE_TOC, json.dumps({k: v for k, v in translated.items() if k != key_home})
    )
    t.check("toc payload missing a key -> problem", any("missing" in p for p in problems), str(problems))
    _, problems, _, _ = finalize_translation("toc.yml", info, FIXTURE_TOC, json.dumps({**translated, "n99": "Extra"}))
    t.check("toc payload with an unexpected key -> problem", any("unexpected" in p for p in problems), str(problems))
    _, problems, _, _ = finalize_translation("toc.yml", info, FIXTURE_TOC, json.dumps({**translated, "x": "Bad"}))
    t.check("toc payload with a malformed key -> problem", any("malformed" in p for p in problems), str(problems))
    _, problems, _, _ = finalize_translation("toc.yml", info, FIXTURE_TOC, json.dumps(["Home"]))
    t.check(
        "toc payload not a dict -> problem (no exception)",
        any("not a JSON object" in p for p in problems),
        str(problems),
    )
    _, problems, _, _ = finalize_translation(
        "toc.yml", info, FIXTURE_TOC, json.dumps({**translated, key_home: "Ini\ncio"})
    )
    t.check("toc name with a line break -> problem", any("line breaks" in p for p in problems), str(problems))
    t.check(
        "yaml_scalar keeps a source-identical special value verbatim",
        yaml_scalar("C# Scripts", "C# Scripts") == "C# Scripts",
    )
    t.check(
        "yaml_scalar quotes yes/no/null/on/off",
        all(yaml_scalar(v).startswith('"') for v in ("yes", "No", "null", "on", "OFF")),
    )
    t.check(
        "yaml_scalar keeps valid quoted values",
        yaml_scalar('"a: b"') == '"a: b"' and yaml_scalar("'it''s'") == "'it''s'",
    )
    t.check(
        "yaml_scalar quotes leading indicators",
        all(yaml_scalar(v).startswith('"') for v in ("?x", "*x", "&x", "!x", "%x", "@x", "`x", "|x", ">x", "[x", "{x")),
    )

    t.section("html")
    payload, _, info = prepare_payload("404.html", FIXTURE_HTML)
    out, problems, _, _ = finalize_translation("404.html", info, FIXTURE_HTML, payload)
    t.check("html identity round-trip", out == FIXTURE_HTML and not problems)
    out, problems, repaired, _ = finalize_translation(
        "404.html", info, FIXTURE_HTML, payload.replace("page.html", "pagina.html")
    )
    t.check("changed href (equal count) -> repaired", out == FIXTURE_HTML and not problems and repaired["links"] == 1)
    _, problems, _, _ = finalize_translation("404.html", info, FIXTURE_HTML, payload.replace("<p>Text</p>\n", "Text\n"))
    t.check("dropped tag -> problem", any("tag counts" in p for p in problems), str(problems))
    _, problems, _, _ = finalize_translation(
        "404.html", info, FIXTURE_HTML, payload.replace("<p>Text</p>", '<p><a href="x.html">Text</a></p>')
    )
    t.check("extra href -> problem", any("href/src" in p for p in problems), str(problems))
    crlf_html = FIXTURE_HTML.replace("\n", "\r\n")
    out, problems, _, _ = finalize_translation("404.html", info, crlf_html, payload)
    t.check("html CRLF source restored", out == crlf_html and not problems)

    t.section("configuration and client helpers")
    t.check(
        "normalize_base_url",
        {
            normalize_base_url(u)
            for u in ("https://api.translated.com", "https://api.translated.com/v2", "https://api.translated.com/v2/")
        }
        == {"https://api.translated.com/v2/"},
    )
    build_config = mini_build_config()
    cfg = TranslationConfig(build_config)
    t.expect_exit(
        "network action without TRANSLATED_ENV -> SystemExit", lambda: cfg.require_network("--run"), "TRANSLATED_ENV"
    )
    t.expect_exit(
        "unknown TRANSLATED_ENV -> SystemExit",
        lambda: TranslationConfig(build_config, "staging").require_network("--run"),
        "not defined",
    )
    prod = TranslationConfig(build_config, "production")
    t.expect_exit(
        "production without service type -> SystemExit mentioning --probe",
        lambda: prod.require_network("--run"),
        "--probe",
    )
    prod.require_network("--probe", need_service_type=False)
    t.check("--probe is allowed without a service type", True)
    t.check(
        "TRANSLATED_SERVICE_TYPE override",
        TranslationConfig(build_config, "production", "enterprise").service_type == "enterprise",
    )
    sandbox = TranslationConfig(build_config, "sandbox")
    sandbox_tier = build_config["translation"]["environments"]["sandbox"]["serviceType"]
    t.check(
        "sandbox environment resolved (service type taken from build-config.json, not hard-coded)",
        sandbox.is_sandbox
        and bool(sandbox_tier)
        and sandbox.service_type == sandbox_tier
        and sandbox.base_url == "https://api.sandbox.translated.com/v2/",
        f"service type {sandbox.service_type!r}, config {sandbox_tier!r}",
    )
    t.check(
        "is_sandbox is the environment name, not a URL substring",
        not TranslationConfig(build_config, "production", "x").is_sandbox,
    )
    msg, parsed = describe_api_error(
        '{"error":true,"code":"INVALID_PARAMS","message":"Bad","id_transaction":"abc","params":[{"field":"service_type","reason":"is not valid"}]}'
    )
    t.check(
        "api_error parsed into a readable message",
        msg == "INVALID_PARAMS; Bad; service_type: is not valid; transaction abc"
        and parsed["code"] == "INVALID_PARAMS",
    )
    t.expect_exit("missing translatedLocale fails fast", lambda: require_locales(["es", "xx"], {"es": "es-ES"}), "xx")
    t.expect_exit(
        "sandbox without --limit/--file refused", lambda: check_sandbox_filter(sandbox, PlanOptions(), False), "--limit"
    )
    check_sandbox_filter(sandbox, PlanOptions(limit=1), False)
    check_sandbox_filter(sandbox, PlanOptions(), True)
    t.check("sandbox with --limit or --allow-unbounded passes", True)
    parser = build_parser()
    t.expect_exit(
        "--repair-existing without --baseline refused",
        lambda: check_option_combinations(parser.parse_args(["--plan", "--repair-existing"])),
        "--baseline",
    )
    check_option_combinations(parser.parse_args(["--baseline", "--repair-existing", "--overwrite-baseline"]))
    t.check("--baseline --repair-existing accepted", True)
    help_text = " ".join(parser.format_help().split())
    t.check("--baseline-ref help names no provider", "previous translation provider" in help_text)

    t.section("git ref resolution (monkeypatched git)")

    def git_ok(cmd: list[str]) -> subprocess.CompletedProcess[bytes]:
        return subprocess.CompletedProcess(cmd, 0, b"deadbeef0000\n", b"")

    def git_missing(cmd: list[str]) -> subprocess.CompletedProcess[bytes]:
        return subprocess.CompletedProcess(cmd, 128, b"", b"fatal: Needed a single revision\n")

    seen: list[list[str]] = []

    def git_spy(cmd: list[str]) -> subprocess.CompletedProcess[bytes]:
        seen.append(cmd)
        return git_ok(cmd)

    t.check("resolve_git_ref returns the sha", resolve_git_ref("d376766", git_spy) == "deadbeef0000")
    t.check(
        "resolve_git_ref uses rev-parse --verify --quiet --end-of-options <ref>^{commit}",
        seen == [["git", "rev-parse", "--verify", "--quiet", "--end-of-options", "d376766^{commit}"]],
        str(seen),
    )
    t.expect_exit(
        "unknown --baseline-ref -> SystemExit",
        lambda: resolve_git_ref("bogus", git_missing),
        "is not a commit in this clone",
    )
    if shutil.which("git"):
        t.expect_exit(
            "unknown --baseline-ref against real git -> SystemExit",
            lambda: resolve_git_ref("no-such-ref-for-the-self-test"),
            "is not a commit in this clone",
        )


# --- fake client end-to-end ---------------------------------------------------


class FakeTranslatedClient:
    """In-memory stand-in for TranslatedClient with the same surface (synchronous AI endpoint)."""

    def __init__(self) -> None:
        self.orders: list[dict[str, Any]] = []
        self.translate_calls = 0
        self.raise_on_translate_call: int | None = None  # 1-based call index that raises an API error
        self.raise_http_status = 400  # status of that error; 401/403 raise TranslatedAuthError
        # id_content -> translated text of a whole-file order, or {segment id -> text} (default: echo the source)
        self.deliveries: dict[str, str | dict[str, str]] = {}
        self.translatable_only = False  # answer with data[] items for translatable segments only
        self.empty_responses: set[str] = set()  # id_content answered with an empty data[]

    def translate_ai(self, order: dict[str, Any]) -> list[dict[str, Any]]:
        self.translate_calls += 1
        if self.raise_on_translate_call == self.translate_calls:
            error = TranslatedAuthError if self.raise_http_status in AUTH_HTTP else TranslatedApiError
            raise error(
                f"POST translate/ai failed with {self.raise_http_status}: INVALID_PARAMS; boom",
                self.raise_http_status,
                {
                    "code": "INVALID_PARAMS",
                    "message": "boom",
                    "id_transaction": "t1",
                    "params": [{"field": "content", "reason": "x"}],
                },
            )
        self.orders.append(order)
        id_content = str(order["id_content"])
        if id_content in self.empty_responses:
            return []
        delivery = self.deliveries.get(id_content)
        items: list[dict[str, Any]] = order["content"]
        out: list[dict[str, Any]] = []
        for item in items:
            if isinstance(delivery, dict):
                text = delivery.get(str(item["id"]), str(item["text"]))
            elif delivery is not None and len(items) == 1:
                text = delivery
            else:
                text = str(item["text"])
            if self.translatable_only and not item["translatable"]:
                continue
            billed = len(text) if item["translatable"] else 0
            out.append(
                {"id": item["id"], "translation": text, "translatable": item["translatable"], "billed_chars": billed}
            )
        return out

    def service_type_names(self) -> list[dict[str, Any]]:
        return [
            {"name": "economy", "human_enabled": False, "machine_enabled": True},
            {"name": "premium", "human_enabled": True, "machine_enabled": False},
        ]

    def languages(self) -> list[dict[str, Any]]:
        return [
            {"key": "en-US", "value": "English"},
            {"key": "es-ES", "value": "Spanish"},
            {"key": "zh-CN", "value": "Chinese"},
        ]


MINI_FILES: dict[str, str] = {
    "index.md": BOM + "---\ntitle: Home\n---\n# Home\n\nShort intro with `code` and [link](guide.md).\n",
    "guide.md": "# Guide\n\nA short guide.\n\n> [!NOTE]\n> Note text.\n",
    "toc.yml": "- name: Home\n  href: index.md\n- name: Guide\n  href: guide.md\n",
    "_ui-strings.json": '{\n  "greeting": "Hello {name}",\n  "bye": "Bye"\n}\n',
    "whats-new/1-0-0.html": "<p>Release notes</p>\n",
}
# Extra source used by the baseline checks only (not in MINI_FILES so the order counts above stay put).
CODE_MD = "# Code\n\n```csharp\n// Assembly references go first\nvar x = 1;\n```\n"
CODE_MD_TRANSLATED_FENCE = CODE_MD.replace("// Assembly references go first", "// Las referencias van primero")
OLD_INDEX_MD = BOM + "---\ntitle: Home\n---\n# Home\n\nOlder intro.\n"
INLINE_MD = "# Inline\n\nSet `enabled` to true.\n"
INLINE_MD_EXTRA_SPAN = INLINE_MD.replace("Set `enabled` to true.", "Establece `enabled` en `true`.")
INLINE_WARNING = "inline code spans 1 -> 2 (missing [], added ['`true`'])"


def mini_build_config(max_files: int = 3) -> dict[str, Any]:
    return {
        "sharedDirectories": {"directories": ["assets", "api"]},
        "translation": {
            "environments": {
                "sandbox": {"baseUrl": "https://api.sandbox.translated.com", "serviceType": "economy"},
                "production": {"baseUrl": "https://api.translated.com/v2/", "serviceType": None},
            },
            "sourceLocale": "en-US",
            "sources": ["**/*.md", "404.html", "toc.yml", "_ui-strings.json"],
            "passthrough": ["whats-new/**/*.html"],
            "sandboxLimits": {"maxFilesPerRun": max_files, "maxCharsPerRun": 100000},
            "instructions": "Keep structure.",
        },
    }


@contextmanager
def mini_repo() -> Iterator[Path]:
    tmp = Path(tempfile.mkdtemp(prefix="translate-selftest-"))
    cwd = os.getcwd()
    for rel, text in MINI_FILES.items():
        write_text(tmp / CONTENT_DIR / rel, text)
    (tmp / LOCALIZED_DIR / "es" / "content").mkdir(parents=True)
    ceiling = os.environ.get("GIT_CEILING_DIRECTORIES")
    # Keep git from finding a repository above the temp dir; git_mini_repo creates one inside it.
    os.environ["GIT_CEILING_DIRECTORIES"] = str(tmp.parent)
    os.chdir(tmp)
    try:
        yield tmp
    finally:
        os.chdir(cwd)
        if ceiling is None:
            os.environ.pop("GIT_CEILING_DIRECTORIES", None)
        else:
            os.environ["GIT_CEILING_DIRECTORIES"] = ceiling
        for p in tmp.rglob("*"):
            os.chmod(p, 0o700)  # git object files are read-only; rmtree cannot delete them on Windows
        shutil.rmtree(tmp, ignore_errors=True)


def git(*args: str) -> str:
    return subprocess.run(["git", *args], check=True, capture_output=True).stdout.decode("utf-8").strip()


def commit_all(message: str) -> None:
    git("add", "-A")
    git("commit", "-q", "--allow-empty", "-m", message)


@contextmanager
def git_mini_repo(extra: dict[str, str] | None = None) -> Iterator[Path]:
    """mini_repo as a git repository with the English sources (plus `extra`) committed."""
    with mini_repo() as tmp:
        for rel, text in (extra or {}).items():
            write_text(CONTENT_DIR / rel, text)
        git("init", "-q")
        git("config", "user.email", "selftest@example.com")
        git("config", "user.name", "selftest")
        git("config", "core.autocrlf", "false")
        git("config", "commit.gpgsign", "false")
        git("config", "core.hooksPath", ".git/no-hooks")
        commit_all("English sources")
        yield tmp


@dataclass
class Harness:
    config: TranslationConfig
    client: FakeTranslatedClient = field(default_factory=FakeTranslatedClient)
    report: RunReport = field(default_factory=RunReport)
    locales: dict[str, str] = field(default_factory=lambda: {"es": "es-ES"})

    @property
    def sources(self) -> dict[str, str]:
        return get_scoped_sources(self.config)

    @property
    def passthrough(self) -> dict[str, str]:
        return get_passthrough_sources(self.config, self.sources)

    def run(
        self,
        options: PlanOptions | None = None,
        allow_unbounded: bool = True,
        lenient: bool = False,
        rejected_dir: Path | None = None,
    ) -> None:
        cmd_run(
            self.config,
            self.client,
            ["es"],
            self.sources,
            self.passthrough,
            self.locales,
            options or PlanOptions(),
            allow_unbounded,
            lenient,
            self.report,
            rejected_dir,
        )

    def plan(self, options: PlanOptions | None = None) -> LanguagePlan:
        return build_plan("es", self.sources, self.passthrough, load_status("es"), options or PlanOptions())


def prod_harness() -> Harness:
    return Harness(TranslationConfig(mini_build_config(), "production", "mt-test"))


def selftest_fake_client(t: SelfTest) -> None:
    t.section("fake client end-to-end: one request per file, identity translations")
    with mini_repo():
        h = prod_harness()
        h.run()
        status = load_status("es")
        r = h.report.lang("es")
        t.check(
            "4 requests sent, one per file, all translated in the same run",
            len(h.client.orders) == 4 and sorted(r["translated"]) == sorted(h.sources),
            str(sorted(o["id_content"] for o in h.client.orders)),
        )
        json_order = next(o for o in h.client.orders if o["id_content"].endswith("_ui-strings.json"))
        t.check("json order content has encoded placeholders", "{{name}}" in json_order["content"][0]["text"])
        toc_order = next(o for o in h.client.orders if o["id_content"].endswith("toc.yml"))
        t.check(
            "toc order is a JSON map of names without hrefs, sent as text/plain",
            "index.md" not in toc_order["content"][0]["text"]
            and "Home" in toc_order["content"][0]["text"]
            and toc_order["content_type"] == "text/plain",
        )
        t.check(
            "orders have the /translate/ai shape: one translatable segment, singular target_language",
            all(
                o["service_type"] == "mt-test"
                and o["target_language"] == "es-ES"
                and o["source_language"] == "en-US"
                and [c["translatable"] for c in o["content"]] == [True]
                and o["context"]["instructions"]
                for o in h.client.orders
            ),
        )
        t.check(
            "passthrough copied and recorded 'copied'",
            target_file("es", "whats-new/1-0-0.html").read_bytes()
            == (CONTENT_DIR / "whats-new/1-0-0.html").read_bytes()
            and status["files"]["whats-new/1-0-0.html"]["status"] == STATUS_COPIED
            and r["copied"] == ["whats-new/1-0-0.html"],
        )
        md_passthrough = mini_build_config()
        md_passthrough["translation"]["passthrough"].append("guide.md")
        cfg = TranslationConfig(md_passthrough, "production", "mt-test")
        scoped = get_scoped_sources(cfg)
        t.check(
            "a passthrough pattern takes a file out of sources even when a source pattern matches it",
            "guide.md" not in scoped and "guide.md" in get_passthrough_sources(cfg, scoped),
        )
        t.check(
            "all 4 files translated at the current source hash",
            all(
                status["files"][rel] == {"sourceHash": h.sources[rel], "status": STATUS_TRANSLATED} for rel in h.sources
            ),
        )
        t.check(
            "written translations are byte-identical to the sources",
            all(target_file("es", rel).read_bytes() == (CONTENT_DIR / rel).read_bytes() for rel in h.sources),
        )
        t.check(
            "report: submitted and billed characters aggregated",
            r["chars"] == sum(len(o["content"][0]["text"]) for o in h.client.orders) and r["billed_chars"] > 0,
        )
        t.check(
            "summary has copied/pinned/failures",
            {"copied", "pinned", "failures", "translated"} <= set(status["summary"])
            and status["summary"]["copied"] == 1,
        )
        md = h.report.to_markdown(h.config)
        t.check("report header shows environment and service type", "(production, service type `mt-test`)" in md)
        h.run()
        t.check("second run is a no-op", len(h.client.orders) == 4)
        h.report = RunReport()
        h.run(PlanOptions(force=True, file_filters=["guide.md"]))
        t.check(
            "--force --file retranslates a current file",
            len(h.client.orders) == 5 and h.client.orders[-1]["id_content"] == "es/guide.md",
        )

    t.section("fake client: broken delivery gates the plan until --retry-failed")
    with mini_repo():
        h = prod_harness()
        h.client.deliveries["es/guide.md"] = MINI_FILES["guide.md"].replace("# Guide\n\n", "")
        h.run()
        status = load_status("es")
        failure = status["failures"].get("guide.md", {})
        t.check(
            "failure recorded with sourceHash and reason",
            failure.get("sourceHash") == h.sources["guide.md"] and "headings" in failure.get("error", ""),
            str(failure),
        )
        t.check("file not written", not target_file("es", "guide.md").exists())
        t.check("other files translated", status["files"]["index.md"]["status"] == STATUS_TRANSLATED)
        kept_dir = Path("rejected")
        h.run(PlanOptions(retry_failed=True, file_filters=["guide.md"]), rejected_dir=kept_dir)
        kept_path = kept_dir / "es" / "guide.md.json"
        kept = json.loads(kept_path.read_text(encoding="utf-8")) if kept_path.exists() else {}
        t.check(
            "--keep-rejected saves the billed delivery with its order and problems",
            kept.get("file") == "guide.md"
            and "headings" in kept["problems"][0]
            and kept["order"]["id_content"] == "es/guide.md"
            and kept["response"][0]["translation"] == h.client.deliveries["es/guide.md"],
            str(kept)[:300],
        )
        t.check(
            "only rejected deliveries are kept",
            [p.name for p in kept_dir.rglob("*.json")] == ["guide.md.json"],
        )
        t.check("verification failures do not flag the run (exit 0)", not h.report.failed)
        plan = h.plan()
        t.check(
            "plan skips the failed file at this hash",
            [rel for rel, _ in plan.skipped_failed] == ["guide.md"]
            and "guide.md" not in {rel for rel, _ in plan.to_submit},
        )
        t.check(
            "--retry-failed re-plans it",
            "guide.md" in {rel for rel, _ in h.plan(PlanOptions(retry_failed=True)).to_submit},
        )
        t.check("--force re-plans it", "guide.md" in {rel for rel, _ in h.plan(PlanOptions(force=True)).to_submit})
        write_text(CONTENT_DIR / "guide.md", MINI_FILES["guide.md"] + "\nMore.\n")
        t.check(
            "English change re-plans it (failure hash differs)", "guide.md" in {rel for rel, _ in h.plan().to_submit}
        )
        h.report = RunReport()
        h.client.deliveries.pop("es/guide.md")
        h.run(PlanOptions(retry_failed=True))
        status = load_status("es")
        t.check(
            "retranslation clears the failure and writes the file",
            "guide.md" not in status["failures"] and status["files"]["guide.md"]["status"] == STATUS_TRANSLATED,
        )

    t.section("fake client: lenient writes usable Markdown despite problems, never structured payloads")
    with mini_repo():
        h = prod_harness()
        h.client.deliveries["es/guide.md"] = MINI_FILES["guide.md"].replace("# Guide\n\n", "")
        h.client.deliveries["es/_ui-strings.json"] = '{\n  "greeting": "Hola {{name}}"\n}\n'
        h.client.deliveries["es/toc.yml"] = json.dumps({"n0": "Inicio"})
        h.run(lenient=True)
        status = load_status("es")
        t.check(
            "--lenient writes the Markdown file (heading mismatch) and marks it translated",
            target_file("es", "guide.md").exists()
            and status["files"]["guide.md"]["status"] == STATUS_TRANSLATED
            and "guide.md" not in status["failures"],
        )
        t.check(
            "--lenient does not write a JSON delivery with a dropped key",
            not target_file("es", "_ui-strings.json").exists()
            and "keys differ" in status["failures"].get("_ui-strings.json", {}).get("error", ""),
            str(status["failures"]),
        )
        t.check(
            "--lenient does not write a toc delivery with a missing key",
            not target_file("es", "toc.yml").exists()
            and "missing" in status["failures"].get("toc.yml", {}).get("error", ""),
            str(status["failures"]),
        )

    t.section("fake client: orphans, unscoped, pinned, filters")
    with mini_repo():
        h = prod_harness()
        write_text(target_file("es", "old.md"), "# Old\n")
        write_text(CONTENT_DIR / "other/thing.yaml", "a: 1\n")
        status = load_status("es")
        status["files"]["old.md"] = {"sourceHash": "sha256:x", "status": STATUS_TRANSLATED}
        status["files"]["other/thing.yaml"] = {"sourceHash": "sha256:y", "status": STATUS_TRANSLATED}
        status["files"]["guide.md"] = {"sourceHash": "", "status": STATUS_UNTRANSLATED, "manual": True}
        save_status("es", status)
        plan = h.plan()
        t.check(
            "plan reports pinned, orphan and unscoped entries",
            plan.pinned == ["guide.md"] and plan.orphans == ["old.md"] and plan.unscoped == ["other/thing.yaml"],
        )
        plan = h.plan(PlanOptions(file_filters=["index.md"]))
        t.check(
            "--file filter plans only the matched file and no orphans",
            [rel for rel, _ in plan.to_submit] == ["index.md"] and not plan.orphans,
        )
        t.check("--limit is applied at submit time", len(h.plan(PlanOptions(limit=1)).to_submit) == 3)
        first = h.plan().to_submit[0][0]
        first_chars = len(prepare_payload(first, read_text(CONTENT_DIR / first))[0])
        out = captured(lambda: print_plan("es", h.plan(), limit=1))
        t.check(
            "--plan honours --limit: one submit line, rest counted as beyond --limit, chars match",
            out.count("\n  submit  ") == 1
            and f"  submit  missing      {first}" in out
            and "2 more beyond --limit 1" in out
            and f"~{first_chars:,} characters would be submitted" in out,
            out,
        )
        h.run(PlanOptions(file_filters=["index.md"]))
        t.check("orphan kept when a filter is active", target_file("es", "old.md").exists())
        h.run(PlanOptions(limit=1))
        t.check(
            "orphan kept when --limit is active; limit honoured",
            target_file("es", "old.md").exists() and len(h.client.orders) == 2,
        )
        h.report = RunReport()
        h.run()
        status = load_status("es")
        t.check(
            "orphan deleted and reported without filters",
            not target_file("es", "old.md").exists()
            and "old.md" not in status["files"]
            and h.report.lang("es")["removed"] == ["old.md"],
        )
        t.check(
            "unscoped entry dropped, pinned file untouched and never sent",
            "other/thing.yaml" not in status["files"]
            and status["files"]["guide.md"].get("manual") is True
            and not any(o["id_content"] == "es/guide.md" for o in h.client.orders),
        )

    t.section("fake client: empty responses and request failures")
    with mini_repo():
        h = prod_harness()
        h.client.empty_responses.add("es/guide.md")
        h.run()
        status = load_status("es")
        t.check(
            "empty data[] -> 'no translation in the response' failure, others translated",
            "no translation in the response" in status["failures"].get("guide.md", {}).get("error", "")
            and not target_file("es", "guide.md").exists()
            and status["files"]["index.md"]["status"] == STATUS_TRANSLATED,
            str(status["failures"]),
        )
    with mini_repo():
        h = prod_harness()
        h.client.raise_on_translate_call = 2
        h.run()
        status = load_status("es")
        failed = [rel for rel, f in status["failures"].items() if "POST translate/ai failed" in f["error"]]
        t.check(
            "request 2 failure recorded with api error details; the other files are translated",
            len(failed) == 1
            and status["failures"][failed[0]].get("apiError", {}).get("code") == "INVALID_PARAMS"
            and sum(1 for f in status["files"].values() if f["status"] == STATUS_TRANSLATED) == 3,
            str(status["failures"]),
        )
        t.check("run flagged as failed (exit 1)", h.report.request_failures == 1 and h.report.failed)
        t.check(
            "a failed request is not billed, so the next plan sends the file again without --retry-failed",
            [rel for rel, _ in h.plan().to_submit] == failed and not h.plan().skipped_failed,
        )
        h.client.raise_on_translate_call = None
        h.run()
        status = load_status("es")
        t.check(
            "the next run translates it and clears the failure",
            not status["failures"] and status["files"][failed[0]]["status"] == STATUS_TRANSLATED,
            str(status["failures"]),
        )
    with mini_repo():
        h = prod_harness()
        h.client.raise_on_translate_call = 2
        h.client.raise_http_status = 401
        t.expect_raises("a rejected key (401) stops the run", lambda: h.run(), TranslatedAuthError)
        status = load_status("es")
        t.check(
            "after a rejected key: the file translated before is saved, nothing is recorded as failed",
            sum(1 for f in status["files"].values() if f["status"] == STATUS_TRANSLATED) == 1
            and not status["failures"]
            and len(h.plan().to_submit) == 3,
            str(status),
        )

    t.section("fake client: sandbox caps")
    with mini_repo():
        sandbox = TranslationConfig(mini_build_config(max_files=3), "sandbox")
        h = Harness(sandbox)
        t.expect_exit(
            "sandbox refuses 4 files over the 3-file cap",
            lambda: h.run(allow_unbounded=False),
            "Refusing to submit 4 file(s)",
        )
        t.check(
            "nothing sent and no status file written by the refused run",
            not h.client.orders and not status_path("es").exists(),
        )
        h.run(PlanOptions(limit=2), allow_unbounded=False)
        t.check("sandbox run within the cap passes", len(h.client.orders) == 2)
        h.run(allow_unbounded=True)
        t.check("--allow-unbounded lifts the cap", len(h.client.orders) == 4)

    t.section("fake client: inline-code count drift is written with a warning")
    with mini_repo():
        h = prod_harness()
        drifted = MINI_FILES["guide.md"].replace("Note text.", "Texto de `nota`.")
        h.client.deliveries["es/guide.md"] = drifted
        out = captured(h.run)
        status = load_status("es")
        r = h.report.lang("es")
        warning = "inline code spans 0 -> 1 (missing [], added ['`nota`'])"
        t.check(
            "delivery with an extra backtick pair is written as delivered and recorded translated",
            read_text(target_file("es", "guide.md")) == drifted
            and status["files"]["guide.md"] == {"sourceHash": h.sources["guide.md"], "status": STATUS_TRANSLATED}
            and "guide.md" not in status["failures"]
            and "guide.md" in r["translated"]
            and not r["failed"],
            out,
        )
        t.check(
            "warning printed and collected per language in the report",
            f"es: written with warnings ({warning}): guide.md" in out and r["warnings"] == [("guide.md", warning)],
            out + str(r["warnings"]),
        )
        md = h.report.to_markdown(h.config)
        t.check(
            "report has a Warnings column and a 'written with warnings' section",
            "| Warnings |" in md
            and "| es | 4 | 0 | 1 | 1 | 0 | 0 |" in md
            and "### es: written with warnings" in md
            and f"- `guide.md` — {warning}" in md,
            md,
        )

    t.section("baseline and dump-orders")
    with mini_repo() as tmp:
        cfg = TranslationConfig(mini_build_config())
        write_text(CONTENT_DIR / "code.md", CODE_MD)
        write_text(CONTENT_DIR / "inline.md", INLINE_MD)
        sources = get_scoped_sources(cfg)
        passthrough = get_passthrough_sources(cfg, sources)
        write_text(target_file("es", "index.md"), MINI_FILES["index.md"].replace("title: Home", "title: Inicio"))
        write_text(target_file("es", "guide.md"), MINI_FILES["guide.md"].replace("# Guide\n\n", ""))
        write_text(target_file("es", "toc.yml"), MINI_FILES["toc.yml"].replace("Home", "Inicio"))
        write_text(target_file("es", "code.md"), CODE_MD_TRANSLATED_FENCE)
        write_text(target_file("es", "inline.md"), INLINE_MD_EXTRA_SPAN)
        status = load_status("es")
        status["files"]["other/thing.yaml"] = {"sourceHash": "sha256:y", "status": STATUS_TRANSLATED}
        status["files"]["whats-new/1-0-0.html"] = {"sourceHash": "sha256:z", "status": STATUS_COPIED}
        save_status("es", status)
        out = captured(lambda: cmd_baseline(["es"], sources, passthrough, None, overwrite=False))
        status = load_status("es")
        t.check(
            "baseline: valid translation marked translated at the current hash",
            status["files"]["index.md"] == {"sourceHash": sources["index.md"], "status": STATUS_TRANSLATED},
        )
        t.check(
            "baseline: toc with equal names marked translated",
            status["files"]["toc.yml"]["status"] == STATUS_TRANSLATED,
        )
        t.check(
            "baseline: structurally stale translation (heading mismatch) marked untranslated",
            status["files"]["guide.md"] == {"sourceHash": "", "status": STATUS_UNTRANSLATED}
            and "outdated      guide.md: headings 1 -> 0" in out,
            out,
        )
        t.check(
            "baseline: missing translation marked untranslated",
            status["files"]["_ui-strings.json"]["status"] == STATUS_UNTRANSLATED,
        )
        t.check(
            "baseline: unscoped dropped, passthrough untouched",
            "other/thing.yaml" not in status["files"]
            and status["files"]["whats-new/1-0-0.html"]["sourceHash"] == "sha256:z",
        )
        t.check(
            "baseline: repairable translation (translated fence) is 'translated', file unchanged, 'would repair' shown",
            status["files"]["code.md"] == {"sourceHash": sources["code.md"], "status": STATUS_TRANSLATED}
            and read_text(target_file("es", "code.md")) == CODE_MD_TRANSLATED_FENCE
            and "would repair  code.md: 1 fences, 0 inline code, 0 markers, 0 links" in out
            and "es: would repair 1 file(s): 1 fences, 0 inline code, 0 markers, 0 links (pass --repair-existing" in out
            and "1 would repair" in out,
            out,
        )
        t.check(
            "baseline: inline-code count drift is accepted as translated with a warning, file unchanged",
            status["files"]["inline.md"] == {"sourceHash": sources["inline.md"], "status": STATUS_TRANSLATED}
            and read_text(target_file("es", "inline.md")) == INLINE_MD_EXTRA_SPAN
            and f"warning       inline.md: {INLINE_WARNING}" in out
            and "1 accepted with inline-code warnings" in out,
            out,
        )
        t.expect_exit(
            "baseline refuses to overwrite without --overwrite-baseline",
            lambda: cmd_baseline(["es"], sources, passthrough, None, overwrite=False),
            "--overwrite-baseline",
        )
        out = captured(lambda: cmd_baseline(["es"], sources, passthrough, None, overwrite=True, repair_existing=True))
        status = load_status("es")
        t.check(
            "baseline: --overwrite-baseline rewrites",
            status["files"]["index.md"]["status"] == STATUS_TRANSLATED,
        )
        t.check(
            "baseline --repair-existing: fence body rewritten from English, recorded translated, 'repaired' shown",
            read_text(target_file("es", "code.md")) == CODE_MD
            and status["files"]["code.md"] == {"sourceHash": sources["code.md"], "status": STATUS_TRANSLATED}
            and "repaired      code.md: 1 fences, 0 inline code, 0 markers, 0 links" in out
            and "es: repaired 1 file(s): 1 fences, 0 inline code, 0 markers, 0 links" in out
            and "would repair" not in out,
            out,
        )
        t.check(
            "baseline --repair-existing: heading mismatch still untranslated, file untouched",
            status["files"]["guide.md"] == {"sourceHash": "", "status": STATUS_UNTRANSLATED}
            and read_text(target_file("es", "guide.md")) == MINI_FILES["guide.md"].replace("# Guide\n\n", ""),
        )
        t.check(
            "baseline --repair-existing: inline-code drift still accepted, nothing rewritten",
            status["files"]["inline.md"]["status"] == STATUS_TRANSLATED
            and read_text(target_file("es", "inline.md")) == INLINE_MD_EXTRA_SPAN,
        )
        crlf_target = target_file("es", "code.md")
        write_text(crlf_target, CODE_MD_TRANSLATED_FENCE.replace("\n", "\r\n"))
        cmd_baseline(["es"], sources, passthrough, None, overwrite=True, repair_existing=True)
        t.check(
            "baseline --repair-existing: written like a delivery (source line endings, no BOM added)",
            read_text(crlf_target) == CODE_MD,
        )

        def fake_git(cmd: list[str]) -> subprocess.CompletedProcess[bytes]:
            if cmd[1] == "rev-parse":
                return subprocess.CompletedProcess(cmd, 0, b"0123abcd\n", b"")
            if cmd[1] == "show" and cmd[2].endswith(":content/index.md"):
                return subprocess.CompletedProcess(cmd, 0, OLD_INDEX_MD.encode("utf-8"), b"")
            return subprocess.CompletedProcess(cmd, 128, b"", b"fatal: path does not exist\n")

        out = captured(lambda: cmd_baseline(["es"], sources, passthrough, "old", overwrite=True, run=fake_git))
        status = load_status("es")
        t.check(
            "baseline --baseline-ref: resolved sha printed, changed file hashed at the ref, new file noted",
            "baseline ref old -> 0123abcd" in out
            and status["files"]["index.md"]["sourceHash"] == hash_bytes(OLD_INDEX_MD.encode("utf-8"))
            and status["files"]["index.md"]["sourceHash"] != sources["index.md"]
            and "outdated      index.md: English changed since old" in out
            and "new           toc.yml: not in content/ at old; baselined at the current hash" in out
            and status["files"]["toc.yml"]["sourceHash"] == sources["toc.yml"],
            out,
        )
        t.expect_exit(
            "baseline with an unknown --baseline-ref exits before touching anything",
            lambda: cmd_baseline(
                ["es"],
                sources,
                passthrough,
                "bogus",
                overwrite=True,
                run=lambda cmd: subprocess.CompletedProcess(cmd, 128, b"", b""),
            ),
            "--baseline-ref bogus is not a commit in this clone",
        )
        cmd_baseline(["es"], sources, passthrough, None, overwrite=True)
        prod = TranslationConfig(mini_build_config(), "production", "mt-test")
        before = status_path("es").read_bytes()
        out_dir = tmp / "orders"
        cmd_dump_orders(prod, out_dir, ["es"], sources, passthrough, {"es": "es-ES"}, PlanOptions(), False)
        summary = json.loads((out_dir / "summary.json").read_text(encoding="utf-8"))
        t.check(
            "dump-orders writes one file per order plus summary.json",
            (out_dir / "es" / "guide.md.json").exists()
            and (out_dir / "es" / "_ui-strings.json.json").exists()
            and summary["languages"]["es"]["orders"] == 2
            and summary["environment"] == "production",
        )
        t.check("dump-orders leaves the status file untouched", status_path("es").read_bytes() == before)
        dumped = json.loads((out_dir / "es" / "guide.md.json").read_text(encoding="utf-8"))
        t.check(
            "dumped order has the /translate/ai shape",
            set(dumped)
            == {
                "id_content",
                "content",
                "content_type",
                "source_language",
                "target_language",
                "service_type",
                "context",
            }
            and isinstance(dumped["content"], list)
            and set(dumped["content"][0]) == {"id", "text", "translatable"},
        )

    t.section("probe against the fake client")
    with mini_repo():
        prod = TranslationConfig(mini_build_config(), "production", "premium")
        client = FakeTranslatedClient()
        t.check(
            "probe passes for known locales and service type", cmd_probe(prod, client, ["es"], {"es": "es-ES"}) == 0
        )
        t.check("probe fails for an unknown locale", cmd_probe(prod, client, ["es"], {"es": "es-MX"}) == 1)
        t.check(
            "probe fails for an unknown service type",
            cmd_probe(TranslationConfig(mini_build_config(), "production", "gold"), client, ["es"], {"es": "es-ES"})
            == 1,
        )


# --- segment-level updates ------------------------------------------------------

SEG_MD = (
    "---\ntitle: Refresh guide\ndescription: How to refresh\nuid: refresh\n---\n"
    "# Refresh guide\n\nOpen the dialog with **Ctrl+R**.\n\n"
    "- First option explained.\n- Second option explained.\n\n"
    "| Option | Meaning |\n|---|---|\n| Full | Refresh everything |\n\n"
    "```csharp\nvar x = 1;\n```\n\n"
    "<!-- IMAGE NEEDED: dialog.png -->\n\n- @refresh-uid\n\n"
    "## Details\n\nThis paragraph is removed later.\n\nFinal paragraph stays.\n"
)
SEG_MD_ES = (
    "---\ntitle: Guía de actualización\ndescription: Cómo actualizar\nuid: refresh\n---\n"
    "# Guía de actualización\n\nAbre el cuadro de diálogo con **Ctrl+R**.\n\n"
    "- Primera opción explicada.\n- Segunda opción explicada.\n\n"
    "| Opción | Significado |\n|---|---|\n| Full | Actualiza todo |\n\n"
    "```csharp\nvar x = 1;\n```\n\n"
    "<!-- IMAGE NEEDED: dialog.png -->\n\n- @refresh-uid\n\n"
    "## Detalles\n\nEste párrafo se elimina más tarde.\n\nEl párrafo final se mantiene.\n"
)
SEG_MD_V2 = (
    SEG_MD.replace("title: Refresh guide", "title: Refresh guide for models")
    .replace("**Ctrl+R**", "**Ctrl+Shift+R**")
    .replace("- Second option explained.\n", "- Second option explained.\n- Third option explained.\n")
    .replace("var x = 1;", "var x = 2;")
    .replace("This paragraph is removed later.\n\n", "")
)
SEG_MD_ES_V2 = (
    SEG_MD_ES.replace("title: Guía de actualización", "title: Guía de actualización de modelos")
    .replace("**Ctrl+R**", "**Ctrl+Shift+R**")
    .replace("- Segunda opción explicada.\n", "- Segunda opción explicada.\n- Tercera opción explicada.\n")
    .replace("var x = 1;", "var x = 2;")
    .replace("Este párrafo se elimina más tarde.\n\n", "")
)
SEG_V2_DELIVERY = {
    "fm:title": "Guía de actualización de modelos",
    "b1": "Abre el cuadro de diálogo con **Ctrl+Shift+R**.",
    "b4": "- Tercera opción explicada.",
}
SEGMENT_SAMPLE = (
    "\n# Title\n\nPara one\ncontinues here.\n\n- item one\n  continued\n- item two\n***\n\n"
    "> [!NOTE]\n> Note line\n> second line\n\n| a | b |\n|---|---|\n\n"
    "```\ncode\n\nmore code\n```\n\n<!-- comment\n\nstill comment -->\n\n"
    "[!include[part](includes/part.md)]\n\n- @uid-one, @uid-two\n\n"
    '<img src="a.png" alt="Dialog picture">\n\nhttps://example.com\n'
)


def selftest_segments(t: SelfTest) -> None:
    t.section("block segmentation and block diff")
    seg = segment(SEGMENT_SAMPLE)
    t.check("segment + join round-trips byte-for-byte", seg.join() == SEGMENT_SAMPLE)
    t.check(
        "kinds: heading, paragraph, list items (with continuation), rule, alert, table rows, fence, comment",
        seg.kinds == ["h", "p", "li", "li", "hr", "alert", "tr", "tr", "fence", "comment", "p", "li", "p", "p"],
        str(seg.kinds),
    )
    t.check(
        "untranslatable: rule, table separator, fence, comment, include line, xref-only item, bare URL",
        [b.translatable for b in seg.blocks]
        == [True, True, True, True, False, True, True, False, False, False, False, False, True, False],
        str([b.translatable for b in seg.blocks]),
    )
    t.check("leading blank line kept as the lead", seg.lead == "\n" and seg.blocks[0].text == "# Title\n")
    a, b, c = (Block("p", f"{x}\n", "\n") for x in "ABC")
    moved = diff_blocks([a, b, c], [c, a, b])
    t.check(
        "a moved block reuses its old translation",
        [(m.kind, m.old_index) for m in moved] == [(ACTION_REUSE, 2), (ACTION_REUSE, 0), (ACTION_REUSE, 1)],
        str(moved),
    )
    d = Block("p", "D\n", "\n")
    actions = diff_blocks([a, b, c], [a, d, c])
    t.check(
        "a changed block is translated, its neighbours reused",
        [m.kind for m in actions] == [ACTION_REUSE, ACTION_TRANSLATE, ACTION_REUSE],
    )
    t.check("context picks one unchanged block on each side", context_indices(actions, [a, d, c], 1) == [0, 2])
    link_old, link_new = Block("p", "See [x](a.md) and `A`.\n"), Block("p", "See [x](b.md) and `B`.\n")
    t.check(
        "a block whose only change is code or a link target is reused with repair",
        [(m.kind, m.old_index) for m in diff_blocks([link_old], [link_new], prose_key)] == [(ACTION_REPAIR, 0)],
    )
    t.check(
        "without prose_key the same change is translated",
        [m.kind for m in diff_blocks([link_old], [link_new])] == [ACTION_TRANSLATE],
    )
    t.check(
        "a heading whose only change is its level is reused with repair; changed heading text is translated",
        [m.kind for m in diff_blocks([Block("h", "##### Setup\n")], [Block("h", "## Setup\n")], prose_key)]
        == [ACTION_REPAIR]
        and [m.kind for m in diff_blocks([Block("h", "## Setup\n")], [Block("h", "## Set up\n")], prose_key)]
        == [ACTION_TRANSLATE],
    )
    t.check(
        "heading marks restored from English",
        restore_heading_marks("## Setup\n", "##### Configuración\n") == "## Configuración\n"
        and restore_heading_marks("## Setup\n", "## Configuración\n") == "## Configuración\n",
    )
    t.check("width 0 sends no context", context_indices(actions, [a, d, c], 0) == [])
    t.check(
        "width -1 sends every unchanged translatable block",
        context_indices([*actions, Action(ACTION_ENGLISH)], [a, d, c, Block("fence", "```\nx\n```\n")], -1) == [0, 2],
    )
    t.check("no context without a changed block", context_indices([Action(ACTION_REUSE, 0)], [a], -1) == [])
    t.check(
        "context width defaults to 2; TRANSLATED_CONTEXT_SEGMENTS overrides the config value",
        TranslationConfig(mini_build_config()).context_segments == 2
        and TranslationConfig(mini_build_config(), None, None, "5").context_segments == 5
        and TranslationConfig(mini_build_config(), None, None, " ").context_segments == 2,
    )
    t.expect_exit(
        "a context width that is not an integer stops the run",
        lambda: TranslationConfig(mini_build_config(), None, None, "many"),
        "Context segments must be an integer",
    )
    fence_old, fence_new = Block("fence", "```\nx\n```\n"), Block("fence", "```\ny\n```\n")
    t.check(
        "a changed untranslatable block is taken from the English",
        [m.kind for m in diff_blocks([fence_old], [fence_new])] == [ACTION_ENGLISH],
    )
    text, problems, repaired, _ = finalize_block(Block("li", "- Item one\n"), "* Elemento uno")
    t.check(
        "delivered list marker restored from English",
        text == "- Elemento uno\n" and not problems and repaired["markers"] == 1,
        f"{text!r} {problems}",
    )
    _, problems, _, _ = finalize_block(Block("h", "## Details\n"), "### Detalles")
    t.check("heading level change is a problem", problems == ["heading level ## -> ###"], str(problems))
    _, problems, _, _ = finalize_block(Block("p", "One line.\n"), "Línea uno.\n\nLínea dos.")
    t.check("a block split in two is a problem", problems == ["p block came back as p + p"], str(problems))
    _, problems, _, _ = finalize_block(Block("h", "## Details\n"), "Detalles")
    t.check("a heading delivered as text is a problem", problems == ["h block came back as p"], str(problems))
    reordered = restore_positionally("usa `b` y `a`", "use `a` and `b`", INLINE_CODE_RE, 0)
    t.check("reordered inline code is left as delivered", reordered == ("usa `b` y `a`", 0), str(reordered))
    items = [
        {"id": "c0", "text": "x", "translatable": False},
        {"id": "b1", "text": "y", "translatable": True},
    ]
    t.check(
        "response mapped with one item per segment",
        map_segment_translations(items, [{"translation": "x"}, {"translation": "Y"}]) == {"b1": "Y"},
    )
    t.check(
        "response mapped with one item per translatable segment",
        map_segment_translations(items, [{"id": "b1", "translation": "Y"}]) == {"b1": "Y"},
    )
    t.check(
        "response with another item count is an error",
        isinstance(map_segment_translations(items, [{}, {}, {}]), str),
    )
    t.check(
        "response with a mismatched id is an error",
        "id 'b9'" in str(map_segment_translations(items, [{"id": "c0"}, {"id": "b9", "translation": "Y"}])),
    )


def seg_harness(context: int = 0, ratio: float = 0.8) -> Harness:
    cfg = mini_build_config()
    cfg["translation"]["segmentDiff"] = {"enabled": True, "maxChangedRatio": ratio, "contextSegments": context}
    return Harness(TranslationConfig(cfg, "production", "mt-test"))


def seed_seg_translation(h: Harness) -> None:
    """Whole-file translation of seg.md at the committed English, then commit it."""
    h.client.deliveries["es/seg.md"] = mask_code(SEG_MD_ES)[0]
    h.run(PlanOptions(file_filters=["seg.md"]))
    commit_all("Spanish")


def selftest_segment_updates(t: SelfTest) -> None:
    t.section("segment-level updates: only changed blocks are sent")
    with git_mini_repo({"seg.md": SEG_MD}):
        h = seg_harness()
        seed_seg_translation(h)
        entry = load_status("es")["files"]["seg.md"]
        t.check(
            "whole-file run records sourceBlob of the English",
            entry.get("sourceBlob") == git("hash-object", "content/seg.md"),
            str(entry),
        )
        write_text(CONTENT_DIR / "seg.md", SEG_MD_V2)
        commit_all("English v2")
        out = captured(
            lambda: print_plan(
                "es",
                h.plan(),
                0,
                lambda rel, reason: file_delta(
                    h.config, "es", rel, reason, load_status("es")["files"].get(rel, {}), PlanOptions()
                ),
            )
        )
        t.check("--plan shows the changed units", "submit  changed      seg.md (3/11 units" in out, out)
        h.client.deliveries["es/seg.md"] = SEG_V2_DELIVERY
        h.report = RunReport()
        h.run(PlanOptions(file_filters=["seg.md"]))
        order = h.client.orders[-1]
        t.check(
            "order holds only the changed title, paragraph and list item",
            [c["id"] for c in order["content"]] == ["fm:title", "b1", "b4"]
            and all(c["translatable"] for c in order["content"])
            and order["content_type"] == "text/plain",
            str(order["content"]),
        )
        written = read_text(target_file("es", "seg.md"))
        t.check(
            "file rebuilt: unchanged blocks kept, changed blocks translated, code from English, removed block gone",
            written == SEG_MD_ES_V2,
            written,
        )
        entry = load_status("es")["files"]["seg.md"]
        t.check(
            "status advanced to the new English hash and blob",
            entry
            == {
                "sourceHash": h.sources["seg.md"],
                "sourceBlob": git("hash-object", "content/seg.md"),
                "status": STATUS_TRANSLATED,
            },
            str(entry),
        )
        r = h.report.lang("es")
        md = h.report.to_markdown(h.config)
        t.check(
            "report counts the file as updated from changed segments",
            [rel for rel, _ in r["segmented"]] == ["seg.md"]
            and r["chars"] == sum(len(c["text"]) for c in order["content"])
            and "1 file(s) updated from changed segments only" in md,
            md,
        )
        commit_all("Spanish v2")

        write_text(CONTENT_DIR / "seg.md", SEG_MD_V2.replace("var x = 2;", "var x = 3;"))
        commit_all("code only")
        sent = len(h.client.orders)
        out = captured(lambda: h.run(PlanOptions(file_filters=["seg.md"])))
        t.check(
            "a code-only change is applied without a request",
            len(h.client.orders) == sent
            and read_text(target_file("es", "seg.md")) == SEG_MD_ES_V2.replace("var x = 2;", "var x = 3;")
            and "updated seg.md (no changed text to translate)" in out
            and load_status("es")["files"]["seg.md"]["sourceHash"] == h.sources["seg.md"],
            out,
        )
        commit_all("Spanish code only")

        write_text(CONTENT_DIR / "seg.md", read_text(CONTENT_DIR / "seg.md").replace("## Details\n", "### Details\n"))
        commit_all("heading level only")
        sent = len(h.client.orders)
        expected = read_text(target_file("es", "seg.md")).replace("## Detalles\n", "### Detalles\n")
        out = captured(lambda: h.run(PlanOptions(file_filters=["seg.md"])))
        t.check(
            "a heading-level change is applied without a request",
            len(h.client.orders) == sent
            and read_text(target_file("es", "seg.md")) == expected
            and "updated seg.md (no changed text to translate)" in out
            and load_status("es")["files"]["seg.md"]["sourceHash"] == h.sources["seg.md"],
            out,
        )
        commit_all("Spanish heading level")

        before = read_text(target_file("es", "seg.md"))
        status_before = load_status("es")["files"]["seg.md"]
        write_text(CONTENT_DIR / "seg.md", read_text(CONTENT_DIR / "seg.md").replace("stays.", "stays here."))
        h.client.deliveries["es/seg.md"] = {"b12": "Línea uno.\n\nLínea dos."}
        h.run(PlanOptions(file_filters=["seg.md"]))
        status = load_status("es")
        t.check(
            "a delivery that splits a block is rejected; file and status kept",
            "p block came back as p + p" in status["failures"].get("seg.md", {}).get("error", "")
            and read_text(target_file("es", "seg.md")) == before
            and status["files"]["seg.md"] == status_before,
            str(status["failures"]),
        )
        h.client.deliveries["es/seg.md"] = mask_code(before.replace("se mantiene.", "se queda aquí."))[0]
        h.run(PlanOptions(file_filters=["seg.md"], retry_failed=True))
        status = load_status("es")
        t.check(
            "--retry-failed after a failed segment update sends the whole file; written, failure cleared",
            [c["id"] for c in h.client.orders[-1]["content"]] == ["s1"]
            and "seg.md" not in status["failures"]
            and read_text(target_file("es", "seg.md")).endswith("El párrafo final se queda aquí.\n"),
            str(status["failures"]),
        )
        commit_all("final paragraph")

        write_text(
            target_file("es", "seg.md"),
            read_text(target_file("es", "seg.md")).replace(
                "## Detalles\n", "## Detalles\n\nPárrafo añadido por un revisor.\n"
            ),
        )
        write_text(CONTENT_DIR / "seg.md", read_text(CONTENT_DIR / "seg.md").replace("here.", "now."))
        h.report = RunReport()
        h.run(PlanOptions(file_filters=["seg.md"]))
        r = h.report.lang("es")
        t.check(
            "a translation that no longer aligns is sent as a whole file, with the reason reported",
            [c["id"] for c in h.client.orders[-1]["content"]] == ["s1"]
            and r["whole_file"]
            and r["whole_file"][0][1].startswith("unaligned"),
            str(r["whole_file"]),
        )

    t.section("segment-level updates: fallbacks, context, response shapes")
    with git_mini_repo({"seg.md": SEG_MD}):
        h = seg_harness(ratio=0.3)
        seed_seg_translation(h)
        write_text(
            CONTENT_DIR / "seg.md",
            SEG_MD.replace("explained.", "described in detail.")
            .replace("stays.", "stays where it is.")
            .replace("Refresh everything", "Refresh every table")
            .replace("removed later", "removed soon"),
        )
        reason = file_delta(h.config, "es", "seg.md", "outdated", load_status("es")["files"]["seg.md"], PlanOptions())
        t.check("mostly changed text is sent as a whole file", str(reason).startswith("mostly changed"), str(reason))
        t.check(
            "--force sends the whole file",
            file_delta(h.config, "es", "seg.md", "outdated", {}, PlanOptions(force=True)) is None,
        )
    with git_mini_repo({"seg.md": SEG_MD}):
        h = seg_harness(context=-1)
        seed_seg_translation(h)
        write_text(CONTENT_DIR / "seg.md", SEG_MD.replace("**Ctrl+R**", "**Ctrl+Shift+R**"))
        h.client.deliveries["es/seg.md"] = {"b1": "Abre el cuadro de diálogo con **Ctrl+Shift+R**."}
        h.report = RunReport()
        h.run(PlanOptions(file_filters=["seg.md"]))
        order = h.client.orders[-1]
        context_ids = [c["id"] for c in order["content"] if not c["translatable"]]
        t.check(
            "contextSegments -1 sends every unchanged translatable block as context; only the change is counted",
            context_ids == ["c0", "c2", "c3", "c4", "c6", "c10", "c11", "c12"]
            and [c["id"] for c in order["content"] if c["translatable"]] == ["b1"]
            and h.report.lang("es")["chars"] == len("Open the dialog with **Ctrl+Shift+R**.")
            and "**Ctrl+Shift+R**" in read_text(target_file("es", "seg.md")),
            str(context_ids),
        )
    with git_mini_repo({"seg.md": SEG_MD}):
        h = seg_harness(context=1)
        seed_seg_translation(h)
        write_text(CONTENT_DIR / "seg.md", SEG_MD.replace("**Ctrl+R**", "**Ctrl+Shift+R**"))
        h.client.deliveries["es/seg.md"] = {"b1": "Abre el cuadro de diálogo con **Ctrl+Shift+R**.", "c0": "IGNORED"}
        h.run(PlanOptions(file_filters=["seg.md"]))
        order = h.client.orders[-1]
        t.check(
            "context segments are sent untranslatable and never written",
            [(c["id"], c["translatable"]) for c in order["content"]] == [("c0", False), ("b1", True), ("c2", False)]
            and "IGNORED" not in read_text(target_file("es", "seg.md"))
            and "**Ctrl+Shift+R**" in read_text(target_file("es", "seg.md")),
            str(order["content"]),
        )
        commit_all("context run")
        h.client.translatable_only = True
        write_text(CONTENT_DIR / "seg.md", read_text(CONTENT_DIR / "seg.md").replace("stays.", "stays here."))
        h.client.deliveries["es/seg.md"] = {"b12": "El párrafo final se queda aquí."}
        h.run(PlanOptions(file_filters=["seg.md"]))
        t.check(
            "a response with items for translatable segments only is mapped",
            read_text(target_file("es", "seg.md")).endswith("El párrafo final se queda aquí.\n")
            and "seg.md" not in load_status("es")["failures"],
            str(load_status("es")["failures"]),
        )

    t.section("segment-level updates: JSON keys and toc names")
    with git_mini_repo():
        h = seg_harness()
        h.client.deliveries["es/_ui-strings.json"] = '{\n  "greeting": "Hola {{name}}",\n  "bye": "Adiós"\n}\n'
        h.client.deliveries["es/toc.yml"] = json.dumps({"n0": "Inicio", "n2": "Guía"})
        h.run(PlanOptions(file_filters=["_ui-strings.json", "toc.yml"]))
        commit_all("Spanish")
        write_text(
            CONTENT_DIR / "_ui-strings.json",
            '{\n  "greeting": "Hello {name}",\n  "bye": "Goodbye",\n  "extra": "Extra {count}"\n}\n',
        )
        write_text(
            CONTENT_DIR / "toc.yml",
            "- name: Home\n  href: index.md\n- name: Reference\n  href: ref.md\n- name: Guide\n  href: guide.md\n",
        )
        commit_all("English v2")
        h.client.deliveries["es/_ui-strings.json"] = {
            "json": '{\n  "bye": "Hasta luego",\n  "extra": "Extra {{count}}"\n}\n'
        }
        h.client.deliveries["es/toc.yml"] = {"toc": json.dumps({"n2": "Referencia"})}
        h.run(PlanOptions(file_filters=["_ui-strings.json", "toc.yml"]))
        json_order = next(o for o in h.client.orders[::-1] if o["id_content"] == "es/_ui-strings.json")
        toc_order = next(o for o in h.client.orders[::-1] if o["id_content"] == "es/toc.yml")
        t.check(
            "JSON order holds only the changed and the new key",
            json.loads(decode_placeholders(json_order["content"][0]["text"]))
            == {"bye": "Goodbye", "extra": "Extra {count}"},
            str(json_order["content"]),
        )
        t.check(
            "JSON rebuilt with the kept translation and the new ones",
            read_text(target_file("es", "_ui-strings.json"))
            == '{\n  "greeting": "Hola {name}",\n  "bye": "Hasta luego",\n  "extra": "Extra {count}"\n}\n',
            read_text(target_file("es", "_ui-strings.json")),
        )
        t.check(
            "toc order holds only the new name; toc rebuilt with the kept names",
            json.loads(toc_order["content"][0]["text"]) == {"n2": "Reference"}
            and read_text(target_file("es", "toc.yml"))
            == "- name: Inicio\n  href: index.md\n- name: Referencia\n  href: ref.md\n- name: Guía\n  href: guide.md\n",
            read_text(target_file("es", "toc.yml")),
        )
        commit_all("Spanish v2")
        write_text(CONTENT_DIR / "_ui-strings.json", '{\n  "greeting": "Hello {name}",\n  "bye": "Goodbye"\n}\n')
        sent = len(h.client.orders)
        h.run(PlanOptions(file_filters=["_ui-strings.json"]))
        t.check(
            "a removed key is dropped without a request",
            len(h.client.orders) == sent
            and read_text(target_file("es", "_ui-strings.json"))
            == '{\n  "greeting": "Hola {name}",\n  "bye": "Hasta luego"\n}\n',
            read_text(target_file("es", "_ui-strings.json")),
        )

    t.section("segment-level updates: code and link target changes are repaired without a request")
    with git_mini_repo():
        h = seg_harness()
        index_es = BOM + "---\ntitle: Inicio\n---\n# Inicio\n\nIntroducción breve con `code` y [enlace](guide.md).\n"
        h.client.deliveries["es/index.md"] = mask_code(index_es)[0]
        h.run(PlanOptions(file_filters=["index.md"]))
        commit_all("Spanish")
        write_text(
            CONTENT_DIR / "index.md",
            MINI_FILES["index.md"].replace("`code`", "`code2`").replace("guide.md", "guide2.md"),
        )
        sent = len(h.client.orders)
        h.run(PlanOptions(file_filters=["index.md"]))
        t.check(
            "translation kept, inline code and link target taken from the new English, nothing sent",
            len(h.client.orders) == sent
            and read_text(target_file("es", "index.md"))
            == index_es.replace("`code`", "`code2`").replace("guide.md", "guide2.md"),
            read_text(target_file("es", "index.md")),
        )
        commit_all("code and link")
        write_text(CONTENT_DIR / "index.md", MINI_FILES["index.md"].replace("Short intro", "Long intro"))
        reason = file_delta(
            seg_harness(ratio=1.0).config,
            "es",
            "index.md",
            "outdated",
            load_status("es")["files"]["index.md"],
            PlanOptions(),
        )
        t.check(
            "a prose change in the same block is translated",
            isinstance(reason, Delta) and [i["id"] for i in reason.items] == ["b1"],
            str(reason),
        )
        write_text(target_file("es", "index.md"), read_text(target_file("es", "index.md")).replace("](guide2.md)", ""))
        reason = file_delta(
            seg_harness(ratio=1.0).config,
            "es",
            "index.md",
            "outdated",
            load_status("es")["files"]["index.md"],
            PlanOptions(),
        )
        t.check(
            "a translation that does not verify against its own English is sent as a whole file",
            str(reason).startswith("existing translation does not verify against its English (link targets"),
            str(reason),
        )

    t.section("segment-level updates: source version lookup and --migrate-blobs")
    with git_mini_repo({"seg.md": SEG_MD}):
        h = seg_harness()
        seed_seg_translation(h)
        status = load_status("es")
        recorded_blob = status["files"]["seg.md"].pop("sourceBlob")
        save_status("es", status)
        write_text(CONTENT_DIR / "seg.md", SEG_MD.replace("**Ctrl+R**", "**Ctrl+Shift+R**"))
        commit_all("English v2")
        entry = load_status("es")["files"]["seg.md"]
        t.check(
            "an entry without sourceBlob finds the English version by its hash in git history",
            isinstance(file_delta(h.config, "es", "seg.md", "outdated", entry, PlanOptions()), Delta),
        )
        wrong = dict(entry, sourceBlob=git("hash-object", "content/seg.md"))
        t.check(
            "a sourceBlob whose content does not match sourceHash is ignored in favour of the lookup",
            recorded_source_text("seg.md", wrong) == SEG_MD,
        )
        t.check(
            "no English version with the hash -> whole file",
            file_delta(h.config, "es", "seg.md", "outdated", dict(entry, sourceHash="sha256:0"), PlanOptions())
            == "English version of the translation not found in git",
        )
        out = captured(lambda: cmd_migrate_blobs(["es"], h.sources))
        t.check(
            "--migrate-blobs records the blob of the version the translation was made from",
            load_status("es")["files"]["seg.md"].get("sourceBlob") == recorded_blob
            and "es: sourceBlob recorded for 1," in out,
            out,
        )
        out = captured(lambda: cmd_migrate_blobs(["es"], h.sources))
        t.check("--migrate-blobs keeps valid blobs", "recorded for 0," in out, out)
    with mini_repo():
        t.expect_exit(
            "--migrate-blobs outside a git work tree exits",
            lambda: cmd_migrate_blobs(["es"], {}),
            "needs a git work tree",
        )
        t.check(
            "outside a git work tree no sourceBlob is recorded",
            source_entry("index.md", get_scoped_sources(TranslationConfig(mini_build_config()))["index.md"], "x").get(
                "sourceBlob"
            )
            is None,
        )


def assembled(delta: Delta | str, translations: dict[str, str]) -> tuple[str, list[str]]:
    if isinstance(delta, str):
        return f"<{delta}>", []
    text, problems, _, _ = delta.assemble(translations)
    return text, problems


def selftest_segment_edge_cases(t: SelfTest) -> None:
    t.section("segment-level updates: edge cases")
    long_para = "Paragraph with enough words to pass the identity threshold of letters. " * 4
    english = f"# Title\n\n{long_para}\n\nSecond paragraph.\n"
    t.check(
        "a translation that is the English text (local --sync fallback copy) is sent whole",
        md_delta(english.replace("Second", "Next"), english, english) == "existing translation is the English text"
        and json_delta('{"a": "Hi there"}', '{"a": "Hi"}', '{"a": "Hi"}') == "existing translation is the English text"
        and toc_delta("- name: B\n", "- name: A\n", "- name: A\n") == "existing translation is the English text",
    )
    delta = md_delta(
        "Use `a` and `b` there.\n\nThen `b` and `c`.\n",
        "Use `a` and `b` here.\n\nThen `b` and `c`.\n",
        "Usa `a` y `b` aquí.\n\nLuego `b` y `c` con `d`.\n",
    )
    text, problems = assembled(delta, {"b0": "Usa {{c0}} y {{c1}} y `true` allí."})
    t.check(
        "an extra span in a new block never shifts spans into a reused block",
        text == "Usa `a` y `b` y `true` allí.\n\nLuego `b` y `c` con `d`.\n" and not problems,
        f"{text!r} {problems}",
    )
    t.check(
        "a translation that lost a code span is sent whole",
        str(md_delta("Use `y` here.\n", "Use `x` here.\n", "Usa x aquí.\n")).startswith(
            "existing translation does not verify against its English (inline code spans 1 -> 0"
        ),
    )
    delta = md_delta("Run `b` before `a`.\n", "Run `a` before `b`.\n", "Ejecuta `a` antes de `b`.\n")
    t.check(
        "spans reordered in the English are mapped by value into the translation",
        isinstance(delta, Delta) and not delta.items and assembled(delta, {})[0] == "Ejecuta `b` antes de `a`.\n",
        str(assembled(delta, {})),
    )
    zh_old, zh_new = "Use `a` then `b`.\n", "Use `a` then `c`.\n"
    delta = md_delta(zh_new, zh_old, "先 `b` 后 `a`。\n")
    t.check(
        "a changed span lands where the translation placed the old one",
        isinstance(delta, Delta) and not delta.items and assembled(delta, {})[0] == "先 `c` 后 `a`。\n",
        str(assembled(delta, {})),
    )
    text, problems, _, _ = finalize_block(Block("p", "   Detail one.\n"), "Detalle uno.")
    t.check(
        "indentation of a block inside a list is restored", text == "   Detalle uno.\n" and not problems, repr(text)
    )
    text, problems, _, _ = finalize_block(Block("p", "Text.\n"), " \nTexto.\n ")
    t.check("whitespace-only lines around a delivery are dropped", text == "Texto.\n" and not problems, repr(text))
    delta = md_delta("First.\n\nLast.\n\nAdded.\n", "First.\n\nLast.\n", "Primero.\n\nÚltimo.")
    text, problems = assembled(delta, {"b2": "Añadido."})
    t.check(
        "a block appended after a translation without a final newline stays a separate block",
        text == "Primero.\n\nÚltimo.\n\nAñadido.\n" and not problems,
        f"{text!r} {problems}",
    )
    delta = md_delta(
        "1. One.\n2. New.\n3. Two.\n4. Three.\n", "1. One.\n2. Two.\n3. Three.\n", "1. Uno.\n2. Dos.\n3. Tres.\n"
    )
    text, problems = assembled(delta, {"b1": "2. Nuevo."})
    t.check(
        "a step inserted into a numbered list sends only the new step; later steps are renumbered",
        isinstance(delta, Delta)
        and [i["id"] for i in delta.items] == ["b1"]
        and text == "1. Uno.\n2. Nuevo.\n3. Dos.\n4. Tres.\n"
        and not problems,
        f"{text!r} {problems}",
    )
    delta = toc_delta(
        "- name: Overview\n  href: b.md\n- name: Overview\n  href: a.md\n",
        "- name: Overview\n  href: a.md\n- name: Overview\n  href: b.md\n",
        "- name: Resumen A\n  href: a.md\n- name: Resumen B\n  href: b.md\n",
    )
    t.check(
        "toc entries with the same name are matched by href when they move",
        isinstance(delta, Delta)
        and not delta.changed
        and assembled(delta, {})[0] == "- name: Resumen B\n  href: b.md\n- name: Resumen A\n  href: a.md\n",
        str(assembled(delta, {})),
    )
    delta = md_delta("# T\n\nText changed.\n", "# T\n\nText.\n", '<a id="t" data-loc-xref></a>\n# T es\n\nTexto.\n')
    t.check(
        "bookmark anchors injected by a local build do not break alignment",
        assembled(delta, {"b1": "Texto cambiado."}) == ("# T es\n\nTexto cambiado.\n", []),
        str(assembled(delta, {"b1": "Texto cambiado."})),
    )
    with git_mini_repo({"seg.md": SEG_MD}):
        h = seg_harness()
        seed_seg_translation(h)
        uncommitted = SEG_MD.replace("**Ctrl+R**", "**Ctrl+Shift+R**")
        write_text(CONTENT_DIR / "seg.md", uncommitted)
        h.client.deliveries["es/seg.md"] = {"b1": "Abre el cuadro de diálogo con **Ctrl+Shift+R**."}
        h.run(PlanOptions(file_filters=["seg.md"]))
        write_text(CONTENT_DIR / "seg.md", uncommitted.replace("stays.", "stays here."))
        t.check(
            "the English of an uncommitted run stays readable as the base of the next diff",
            recorded_source_text("seg.md", load_status("es")["files"]["seg.md"]) == uncommitted,
        )


def selftest_code_placeholders(t: SelfTest) -> None:
    t.section("code placeholders (the service turns backticks into quotation marks)")
    body = FIXTURE_MD.lstrip(BOM)
    masked, spans = mask_code(body)
    t.check(
        "fenced blocks and inline code become {{fN}} / {{cN}}; nothing with a backtick is sent",
        "`" not in masked
        and spans
        == [
            "`View → Options`",
            "`Selected.Tables`",
            "```csharp\n// Assembly references must be at the very top\nvar x = 1;\n```",
        ]
        and "{{c0}}" in masked
        and "{{f2}}\n" in masked,
        f"{masked!r} {spans}",
    )
    t.check("mask + unmask round-trips byte-for-byte", unmask_code(masked, spans) == (body, []))
    t.check(
        "quotation marks the service put around a placeholder are dropped",
        unmask_code("Abre «{{c0}}», “{{ c1 }}” y {{c2}}.", ["`a`", "`b`", "`c`"]) == ("Abre `a`, `b` y `c`.", []),
    )
    t.check(
        "unpaired quotation marks are kept",
        unmask_code("«{{c0}}” y {{c1}}", ["`a`", "`b`"])[0] == "«`a`” y `b`",
    )
    t.check(
        "a missing, repeated or unknown placeholder is a problem",
        unmask_code("{{c0}}", ["`a`", "`b`"])[1] == ["code placeholders missing in the delivery: [1] (1 of 2)"]
        and unmask_code("{{c0}} {{c0}}", ["`a`"])[1] == ["code placeholders repeated in the delivery: [0]"]
        and unmask_code("{{c0}} {{c7}}", ["`a`"])[1] == ["unknown code placeholders in the delivery: ['{{c7}}']"],
    )
    content, _, info = prepare_payload("x.md", FIXTURE_MD)
    t.check(
        "Markdown payloads are masked; the job keeps the code",
        "`" not in content and info.get("codeSpans") == spans and info.get("mode") == "raw",
    )
    t.check("JSON and toc payloads are not masked", "codeSpans" not in prepare_payload("a.json", FIXTURE_JSON)[2])

    with mini_repo():
        h = prod_harness()
        source = MINI_FILES["index.md"]
        h.client.deliveries["es/index.md"] = (
            "---\ntitle: Inicio\n---\n# Inicio\n\nIntroducción breve con «{{c0}}» y [enlace](guide.md).\n"
        )
        h.client.deliveries["es/guide.md"] = "# Guía\n\nUna guía breve.\n\n> [!NOTE]\n> Texto.\n"
        h.run(PlanOptions(file_filters=["index.md", "guide.md"]))
        index_order = next(str(o["content"][0]["text"]) for o in h.client.orders if o["id_content"] == "es/index.md")
        t.check(
            "whole file: the order carries placeholders; quoted placeholders come back as inline code",
            "{{c0}}" in index_order
            and "`" not in index_order
            and read_text(target_file("es", "index.md"))
            == source.replace("title: Home", "title: Inicio")
            .replace("# Home", "# Inicio")
            .replace("Short intro with `code` and [link]", "Introducción breve con `code` y [enlace]"),
            read_text(target_file("es", "index.md")),
        )
        h.client.deliveries["es/index.md"] = "---\ntitle: Inicio\n---\n# Inicio\n\nIntroducción breve con «code».\n"
        h.run(PlanOptions(file_filters=["index.md"], force=True))
        status = load_status("es")
        t.check(
            "whole file: a delivery that lost a placeholder is rejected, the file kept",
            "code placeholders missing" in status["failures"].get("index.md", {}).get("error", "")
            and "`code`" in read_text(target_file("es", "index.md")),
            str(status["failures"]),
        )

    delta = md_delta("Set `a` to `b` now.\n\nKeep.\n", "Set `a` to `b`.\n\nKeep.\n", "Pon `a` en `b`.\n\nMantener.\n")
    t.check(
        "segment: sent blocks carry placeholders",
        isinstance(delta, Delta) and [str(i["text"]) for i in delta.items] == ["Set {{c0}} to {{c1}} now."],
        str(delta),
    )
    t.check(
        "segment: quoted placeholders come back as inline code",
        assembled(delta, {"b0": "Pon «{{c0}}» en «{{c1}}» ahora."}) == ("Pon `a` en `b` ahora.\n\nMantener.\n", []),
        str(assembled(delta, {"b0": "Pon «{{c0}}» en «{{c1}}» ahora."})),
    )
    t.check(
        "segment: a block that lost a placeholder is a problem",
        assembled(delta, {"b0": "Pon «a» en {{c1}} ahora."})[1]
        == ["block 0: code placeholders missing in the delivery: [0] (1 of 2)"],
        str(assembled(delta, {"b0": "Pon «a» en {{c1}} ahora."})),
    )


class FakeHttpResponse:
    def __init__(self, body: str) -> None:
        self.body = body

    def __enter__(self) -> FakeHttpResponse:
        return self

    def __exit__(self, *_: object) -> None:
        return None

    def read(self) -> bytes:
        return self.body.encode("utf-8")


def fake_http_error(code: int, retry_after: str | None = None) -> urllib.error.HTTPError:
    headers = http.client.HTTPMessage()
    if retry_after is not None:
        headers["Retry-After"] = retry_after
    body = io.BytesIO(b'{"code": "E", "message": "m"}')
    return urllib.error.HTTPError("https://api.example/v2/translate/ai", code, "error", headers, body)


def selftest_http_client(t: SelfTest) -> None:
    t.section("HTTP client: retries, Retry-After, jitter, rejected key")
    ok_body = '{"data": [{"id": "s1", "translation": "hola"}]}'

    def client_for(answers: list[Any], jitter: float = 0.5) -> tuple[TranslatedClient, list[float], list[int]]:
        sleeps: list[float] = []
        calls: list[int] = []

        def opener(_req: Any, timeout: float = 0) -> FakeHttpResponse:
            calls.append(1)
            answer = answers.pop(0)
            if isinstance(answer, BaseException):
                raise answer
            return FakeHttpResponse(str(answer))

        return TranslatedClient("https://api.example/v2/", "k", sleeps.append, opener, lambda: jitter), sleeps, calls

    order: dict[str, Any] = {"content": []}
    client, sleeps, _ = client_for([fake_http_error(429, "7"), ok_body])
    t.check(
        "429 waits the Retry-After seconds, then succeeds",
        client.translate_ai(order)[0]["translation"] == "hola" and sleeps == [7.0],
        str(sleeps),
    )
    client, sleeps, _ = client_for([fake_http_error(503, "600"), ok_body])
    client.translate_ai(order)
    t.check("Retry-After is capped", sleeps == [MAX_RETRY_DELAY], str(sleeps))
    client, sleeps, _ = client_for([fake_http_error(408), fake_http_error(500), ok_body])
    client.translate_ai(order)
    t.check(
        "408 is retried; backoff is jittered between half and all of 2, 4, ... s", sleeps == [1.5, 3.0], str(sleeps)
    )
    client, sleeps, calls = client_for([fake_http_error(401)])
    t.expect_raises("401 raises TranslatedAuthError", lambda: client.translate_ai(order), TranslatedAuthError)
    t.check("a rejected key is not retried", sleeps == [] and len(calls) == 1)
    client, sleeps, calls = client_for([fake_http_error(400)])
    raised: BaseException | None = None
    try:
        client.translate_ai(order)
    except TranslatedApiError as e:
        raised = e
    t.check(
        "400 is not retried and is not an auth error",
        isinstance(raised, TranslatedApiError) and not isinstance(raised, TranslatedAuthError) and len(calls) == 1,
    )
    now = datetime(2026, 1, 1, tzinfo=UTC)
    t.check(
        "Retry-After as an HTTP date; unparsable values ignored",
        parse_retry_after("Thu, 01 Jan 2026 00:00:30 GMT", now) == 30.0
        and parse_retry_after("soon", now) is None
        and parse_retry_after(None) is None,
    )
    t.check(
        "backoff without Retry-After stays within 60 s",
        retry_delay(2, None, lambda: 0.0) == 4.0
        and retry_delay(2, None, lambda: 1.0) == 8.0
        and retry_delay(10, None, lambda: 1.0) == MAX_RETRY_DELAY,
    )


def selftest_merge_status(t: SelfTest) -> None:
    t.section("--merge-status: status files merged entry by entry")

    def entry(source_hash: str) -> dict[str, Any]:
        return {"sourceHash": source_hash, "status": STATUS_TRANSLATED}

    with git_mini_repo():
        files = {rel: entry(f"{rel[0]}0") for rel in ("a.md", "b.md", "c.md", "d.md")}
        save_status("es", {"language": "es", "files": files, "failures": {}})
        commit_all("base")
        main = git("rev-parse", "HEAD")
        git("checkout", "-q", "-b", "localization")
        status = load_status("es")
        status["files"]["c.md"] = entry("c1")
        status["files"]["e.md"] = entry("e1")
        del status["files"]["d.md"]
        status["failures"]["b.md"] = {"error": "x", "sourceHash": "b0"}
        save_status("es", status)
        commit_all("translation branch")
        git("checkout", "-q", main)
        status = load_status("es")
        status["files"]["b.md"] = entry("b1")
        status["files"]["c.md"] = entry("c2")
        status["files"]["f.md"] = entry("f1")
        save_status("es", status)
        commit_all("main")
        ours = git("rev-parse", "HEAD")
        # Worst case of the fold: a conflict resolved by taking the branch's localizedContent as-is.
        git("checkout", "localization", "--", status_path("es").as_posix())
        captured(lambda: cmd_merge_status(["es"], ours, "localization"))
        merged = load_status("es")
        t.check(
            "entries the branch changed, added or removed come from the branch; the others from main",
            merged["files"]
            == {
                "a.md": entry("a0"),
                "b.md": entry("b1"),
                "c.md": entry("c1"),
                "e.md": entry("e1"),
                "f.md": entry("f1"),
            },
            str(merged["files"]),
        )
        t.check("failures are merged the same way", set(merged["failures"]) == {"b.md"}, str(merged["failures"]))


def cmd_self_test(config: TranslationConfig) -> int:
    t = SelfTest()
    selftest_corpus(t, config)
    selftest_fixtures(t)
    selftest_fake_client(t)
    selftest_segments(t)
    selftest_segment_updates(t)
    selftest_segment_edge_cases(t)
    selftest_code_placeholders(t)
    selftest_http_client(t)
    selftest_merge_status(t)
    print(f"\nself-test: {t.passed} passed, {len(t.failures)} failed")
    for name in t.failures:
        print(f"  FAILED: {name}")
    return 1 if t.failures else 0


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def check_sandbox_filter(config: TranslationConfig, options: PlanOptions, allow_unbounded: bool) -> None:
    if config.is_sandbox and not allow_unbounded and not options.filtered:
        raise SystemExit(
            "Sandbox runs need --limit or --file (or --allow-unbounded) so a full-corpus submission cannot happen by accident."
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Translate docs content with Translated (TranslationOS).")
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--plan", action="store_true", help="show what would be submitted; no API calls")
    actions.add_argument(
        "--run", action="store_true", help="translate missing/outdated files (one synchronous request per file)"
    )
    actions.add_argument(
        "--baseline", action="store_true", help="mark existing, structurally valid translations as current"
    )
    actions.add_argument(
        "--migrate-blobs",
        action="store_true",
        help="record the English git blob (sourceBlob) for status entries that only have a sourceHash",
    )
    actions.add_argument(
        "--merge-status",
        nargs=2,
        metavar=("OURS", "THEIRS"),
        help="after merging translation branch THEIRS into OURS: rebuild each status file entry by entry, taking "
        "THEIRS only where it changed an entry since the merge base (offline)",
    )
    actions.add_argument("--self-test", action="store_true", help="offline self-test (no key, no network)")
    actions.add_argument("--probe", action="store_true", help="check service types and languages against the API")
    actions.add_argument(
        "--dump-orders", metavar="DIR", help="write the /translate/ai bodies to DIR instead of sending"
    )
    parser.add_argument("--lang", action="append", help="limit to a language folder (repeatable)")
    parser.add_argument("--file", action="append", default=[], help="glob relative to content/ (repeatable)")
    parser.add_argument("--limit", type=int, default=0, help="submit at most N files per language")
    parser.add_argument("--force", action="store_true", help="retranslate matched files even when they are current")
    parser.add_argument("--lenient", action="store_true", help="write translations that fail structural verification")
    parser.add_argument("--allow-unbounded", action="store_true", help="lift the sandbox per-run caps")
    parser.add_argument(
        "--retry-failed", action="store_true", help="re-plan files that failed at the current source hash"
    )
    parser.add_argument("--report", help="write a markdown run summary to this path")
    parser.add_argument(
        "--keep-rejected",
        metavar="DIR",
        help="with --run: save billed deliveries that fail verification (order, response, problems) under DIR",
    )
    parser.add_argument(
        "--baseline-ref",
        help="git ref whose content/ hashes become the baseline "
        "(e.g. the last merge from the previous translation provider)",
    )
    parser.add_argument(
        "--overwrite-baseline", action="store_true", help="allow --baseline to replace an existing baseline"
    )
    parser.add_argument(
        "--repair-existing",
        action="store_true",
        help="with --baseline: write code, markers and link targets restored from English back into existing "
        "translations (without it the baseline only reports what it would repair)",
    )
    return parser


def check_option_combinations(args: argparse.Namespace) -> None:
    if args.repair_existing and not args.baseline:
        raise SystemExit("--repair-existing is only valid together with --baseline.")
    if args.keep_rejected and not args.run:
        raise SystemExit("--keep-rejected is only valid together with --run.")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = build_parser().parse_args()
    check_option_combinations(args)

    if not CONTENT_DIR.exists():
        print("Run from the docs repo root (content/ not found).", file=sys.stderr)
        return 1

    build_config = load_build_config()
    config = TranslationConfig(
        build_config,
        os.environ.get("TRANSLATED_ENV"),
        os.environ.get("TRANSLATED_SERVICE_TYPE"),
        os.environ.get("TRANSLATED_CONTEXT_SEGMENTS"),
    )
    if args.self_test:
        return cmd_self_test(config)

    default_lang = get_default_language(build_config)
    langs = args.lang or get_target_languages(default_lang)
    if not langs:
        print("No target languages found under localizedContent/.", file=sys.stderr)
        return 1
    sources = get_scoped_sources(config)
    passthrough = get_passthrough_sources(config, sources)
    options = PlanOptions(args.file, args.limit, args.force, args.retry_failed)
    print(
        f"{len(sources)} source files in scope, {len(passthrough)} passthrough; languages: {', '.join(langs)}; "
        f"environment: {config.environment_label} ({config.base_url or 'no endpoint'}), "
        f"service type: {config.service_type or 'unset'}"
    )

    if args.plan:
        cmd_plan(config, langs, sources, passthrough, options)
        return 0
    if args.migrate_blobs:
        cmd_migrate_blobs(langs, sources)
        return 0
    if args.merge_status:
        cmd_merge_status(langs, *args.merge_status)
        return 0
    if args.baseline:
        cmd_baseline(langs, sources, passthrough, args.baseline_ref, args.overwrite_baseline, args.repair_existing)
        return 0
    locales = load_locale_map()
    if args.dump_orders:
        cmd_dump_orders(
            config, Path(args.dump_orders), langs, sources, passthrough, locales, options, args.allow_unbounded
        )
        return 0
    if args.probe:
        return cmd_probe(config, require_client(config, "--probe", need_service_type=False), langs, locales)

    client = require_client(config, "--run")
    check_sandbox_filter(config, options, args.allow_unbounded)
    report = RunReport()
    rejected_dir = Path(args.keep_rejected) if args.keep_rejected else None
    try:
        cmd_run(
            config,
            client,
            langs,
            sources,
            passthrough,
            locales,
            options,
            args.allow_unbounded,
            args.lenient,
            report,
            rejected_dir,
        )
    except TranslatedAuthError as e:
        report.notes.append(f"Run stopped: {e}")
        print(f"Run stopped: {e}", file=sys.stderr)
        return 1
    finally:
        summary = report.to_markdown(config)
        print("\n" + summary)
        if args.report:
            Path(args.report).parent.mkdir(parents=True, exist_ok=True)
            Path(args.report).write_text(summary, encoding="utf-8")
    return 1 if report.failed else 0


if __name__ == "__main__":
    sys.exit(main())
