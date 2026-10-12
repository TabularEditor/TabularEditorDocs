#!/usr/bin/env python
"""
Translate documentation content with Translated's AI translation (TranslationOS POST /translate/ai).

English sources live in content/, translations land at
localizedContent/{lang}/content/{same path} using two-letter folder codes, and
translation PRs arrive on the `localization` branch (see .github/workflows/translate.yml).

The AI endpoint is synchronous: one POST per file and language returns the translation in
the response (data[].translation, billed per character), so there are no pending jobs,
no polling and nothing to cancel. Every delivery is repaired against the English source
(code, markers, link targets restored), verified, and written in the same step.

Actions (exactly one per invocation):

  --plan         compare English source hashes with localizedContent/{lang}/.translation-status.json
                 and list what is missing, outdated, orphaned, pinned or unscoped (offline)
  --run          POST /translate/ai for every missing/outdated file (one request per file and
                 language), repair-verify-write each translation, and record the outcome
  --baseline     one-time migration step: run every existing translation through the same
                 repair-then-verify path as a delivery, mark the valid ones as current so only future
                 changes are sent, and mark the rest untranslated (offline; repairs are only written
                 back with --repair-existing)
  --self-test    offline proof that extraction, repair, verification and bookkeeping work
  --probe        GET service types and languages from the API and check the configuration
  --dump-orders  write the exact /translate/ai request bodies to a directory instead of sending them

Scope (which files are translated and how) comes from the "translation" section of
metadata/build-config.json; locales come from "translatedLocale" in
metadata/language-metadata.json. Target languages are the folders under
localizedContent/ that contain a content/ directory (same rule as gen_languages.py).

Usage (run from the docs repo root):
    python build_scripts/translate-content.py --plan [--lang es] [--file "features/*.md"]
    python build_scripts/translate-content.py --run --lang es --limit 3 [--force] [--report report.md]
    python build_scripts/translate-content.py --baseline [--baseline-ref d376766] [--overwrite-baseline] [--repair-existing]
    python build_scripts/translate-content.py --self-test
    python build_scripts/translate-content.py --probe
    python build_scripts/translate-content.py --dump-orders /tmp/orders

Environment:
    TRANSLATED_ENV            sandbox | production: selects translation.environments[...] in
                              build-config.json; required for --run/--probe. The sandbox account
                              has no AI-enabled service type (checked 2026-10-12), so only
                              production can actually run the AI endpoint.
    TRANSLATED_API_KEY        required for --run/--probe
    TRANSLATED_SERVICE_TYPE   overrides the environment's serviceType (both environments default to 'AI')

Exit code is 1 for configuration errors and when any /translate/ai request failed with an API
error. Individual files that fail verification do not fail the run; they are recorded under
"failures" in the status file (at the source hash they failed for, so they are not
resubmitted until the English changes or --retry-failed is given) and listed in the report.
"""

from __future__ import annotations

import argparse
import difflib
import fnmatch
import hashlib
import http.client
import io
import json
import os
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

CONTENT_DIR = Path("content")
LOCALIZED_DIR = Path("localizedContent")
STATUS_FILENAME = ".translation-status.json"
LANGUAGE_METADATA_PATH = Path("metadata/language-metadata.json")

STATUS_TRANSLATED = "translated"
STATUS_UNTRANSLATED = "untranslated"
STATUS_OUTDATED = "outdated"
STATUS_COPIED = "copied"

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

RETRYABLE_HTTP = frozenset({425, 429, 500, 502, 503, 504})
REPORT_LIST_CAP = 50
IDENTITY_MIN_LETTERS = 200
REPAIR_KINDS = ("fences", "inline code", "markers", "links")  # order used in "repaired: ..." lines
WARNING_KINDS = frozenset({"inline code"})  # count mismatches of these kinds are warnings, not problems

# content_type values accepted by POST /translate/ai (text/markdown and application/json are
# rejected by its schema, verified 2026-10-12), so Markdown and the JSON-shaped payloads
# (toc.yml name maps, _ui-strings.json) are sent as text/plain; structure is restored and
# verified against the English source on delivery anyway.
CONTENT_TYPES = {
    ".md": "text/plain",
    ".html": "text/html",
    ".htm": "text/html",
    ".json": "text/plain",
    ".yml": "text/plain",  # toc.yml is sent as a JSON map of its `name` values, see extract_yaml_names
    ".yaml": "text/plain",
}

BOM = "﻿"

# Markdown structure regexes (mirror normalize-localized-heading-anchors.py).
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
HEADING_RE = re.compile(r"^#{1,6}\s+\S")
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
    """Return {relative path -> sha256} for every English file in translation scope."""
    return _glob_content(config.sources, set(config.shared_directories), config.ignore)


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
    # Legacy key from the asynchronous flow; the AI endpoint is synchronous, nothing is pending.
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
    same position. Returns (text, changed) when the counts match, None otherwise."""
    src_values = [m.group(group) for m in regex.finditer(source_text)]
    matches = list(regex.finditer(text))
    if len(src_values) != len(matches):
        return None
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
            findings = result.warnings if kind in WARNING_KINDS else result.problems
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
    ) -> None:
        self.base_url = base_url
        self.api_key = api_key
        self.sleep = sleep
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
            try:
                with self.opener(req, timeout=180) as resp:
                    return json.loads(resp.read().decode("utf-8") or "null")
            except urllib.error.HTTPError as e:
                payload = e.read().decode("utf-8", errors="replace")
                message, api_error = describe_api_error(payload)
                last_error = f"{e.code}: {message}"
                if e.code not in RETRYABLE_HTTP:
                    raise TranslatedApiError(
                        f"{method} {endpoint} failed with {last_error}", e.code, api_error
                    ) from None
            except (urllib.error.URLError, OSError, http.client.HTTPException, json.JSONDecodeError) as e:
                last_error = f"{type(e).__name__}: {e}"
            if attempt < retries:
                self.sleep(2**attempt * 2)
        raise TranslatedApiError(f"{method} {endpoint} failed after {retries + 1} attempts ({last_error})")

    def _post(self, endpoint: str, body: Any, extra_headers: dict[str, str] | None = None, retries: int = 3) -> Any:
        return self._request("POST", endpoint, body, extra_headers, retries)

    def _get(self, endpoint: str) -> Any:
        return self._request("GET", endpoint)

    def translate_ai(self, order: dict[str, Any]) -> list[dict[str, Any]]:
        """Synchronous AI translation of one file: the response's data[] holds the translated
        segments, positionally aligned with the request's content[]. One idempotency id per
        request, reused on every retry, so a timeout after server-side processing cannot bill
        the same content twice."""
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
        if failure and failure.get("sourceHash") == src_hash and not options.retry_failed:
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
            if r["repaired"]:
                kinds = ", ".join(f"{n} {kind}" for kind, n in sorted(r["repaired"].items()))
                out.append(f"\n{lang}: repaired from English: {kinds} in {len(r['repaired_files'])} file(s).")
            sections: list[tuple[str, list[str]]] = [
                (f"{lang}: failed (translation kept as before)", [f"`{rel}` — {why}" for rel, why in r["failed"]]),
                (f"{lang}: written with warnings", [f"`{rel}` — {why}" for rel, why in r["warnings"]]),
                (f"{lang}: removed (English source gone)", [f"`{x}`" for x in r["removed"]]),
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


def print_plan(lang: str, plan: LanguagePlan, limit: int = 0) -> None:
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
        content, _, _ = prepare_payload(rel, read_text(CONTENT_DIR / rel))
        chars += len(content)
        print(f"  submit  {reason:<12} {rel}")
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


def cmd_plan(langs: list[str], sources: dict[str, str], passthrough: dict[str, str], options: PlanOptions) -> None:
    for lang in langs:
        print_plan(lang, build_plan(lang, sources, passthrough, load_status(lang), options), options.limit)


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
            status["files"][rel] = {"sourceHash": baseline_hash, "status": STATUS_TRANSLATED}
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

    @property
    def chars(self) -> int:
        return sum(int(j["chars"]) for j in self.jobs.values())


def build_order(
    config: TranslationConfig, id_content: str, content: str, content_type: str, locale: str
) -> dict[str, Any]:
    # POST /translate/ai body (schema verified 2026-10-12): a single object per file with
    # target_language (singular) and content as a list of {text, translatable} segments;
    # the whole file is one translatable segment. id_content is not part of the schema but
    # is tolerated and kept for transaction tracing.
    order: dict[str, Any] = {
        "id_content": id_content,
        "source_language": config.source_locale,
        "target_language": locale,
        "content_type": content_type,
        "service_type": config.service_type,
        "content": [{"id": "s1", "text": content, "translatable": True}],
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
        content, content_type, info = prepare_payload(rel, read_text(CONTENT_DIR / rel))
        if not content.strip() or info.get("units") == 0:
            sub.empty_copies.append(rel)
            continue
        id_content = f"{lang}/{rel}"
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
        status["files"][rel] = {"sourceHash": passthrough[rel], "status": STATUS_COPIED}
    for rel in sub.empty_copies:
        write_text(target_file(lang, rel), read_text(CONTENT_DIR / rel))
        status["files"][rel] = {"sourceHash": sources[rel], "status": STATUS_TRANSLATED}
        status["failures"].pop(rel, None)
    save_status(lang, status)


def billed_chars(data: list[dict[str, Any]]) -> int:
    return sum(int(d["billed_chars"]) for d in data if isinstance(d.get("billed_chars"), (int, float)))


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
    try:
        text, problems, repaired, warnings = finalize_translation(rel, job, read_text(CONTENT_DIR / rel), translated)
    except Exception as e:  # noqa: BLE001 - reported to the reviewer, never crashes the run
        record_failure(status, rel, f"could not reinsert translation: {e}", job_hash)
        return [f"could not reinsert translation: {e}"], Counter(), []
    # --lenient only makes sense for raw Markdown/HTML, where the assembled text is still usable.
    # A structured payload (toc names, UI strings) with problems rebuilds to English or nothing.
    structured = job.get("mode") in ("yaml-names", "json-placeholders")
    if problems and (not lenient or not text or structured):
        if lenient:
            why = "no usable text" if not text else "structured payload cannot be written partially"
            print(f"{lang}: --lenient ignored for {rel}: {why}")
        record_failure(status, rel, "; ".join(problems), job_hash)
        return problems, repaired, warnings
    write_text(target_file(lang, rel), text)
    status["files"][rel] = {"sourceHash": job_hash, "status": STATUS_TRANSLATED}
    status["failures"].pop(rel, None)
    if problems:
        print(f"{lang}: written despite problems ({'; '.join(problems)}): {rel}")
    if warnings:
        print(f"{lang}: written with warnings ({'; '.join(warnings)}): {rel}")
    return [], repaired, warnings


def translate_language(
    client: TranslationClient,
    sub: LanguageSubmission,
    sources: dict[str, str],
    passthrough: dict[str, str],
    lenient: bool,
    report: RunReport,
) -> None:
    """One synchronous /translate/ai request per planned file: translate, repair, verify, write.
    The status file is saved after every file so an interrupted run never loses the record of a
    translation that was already billed and written."""
    lang, status = sub.lang, sub.status
    r = report.lang(lang)
    apply_local_changes(sub, sources, passthrough, r)
    orders = {str(o["id_content"]): o for o in sub.orders}
    try:
        for rel, job in sub.jobs.items():
            try:
                data = client.translate_ai(orders[job["idContent"]])
            except TranslatedApiError as e:
                report.request_failures += 1
                record_failure(status, rel, f"POST translate/ai failed: {e}", job["sourceHash"], apiError=e.details())
                r["failed"].append((rel, f"POST translate/ai failed: {e}"))
                print(f"{lang}: FAILED {rel}: {e}")
                save_status(lang, status)
                continue
            r["chars"] += int(job["chars"])
            r["billed_chars"] += billed_chars(data)
            translated = data[0].get("translation") if data else None
            problems, repaired, warnings = apply_translation(lang, rel, job, translated, status, lenient)
            if problems:
                r["failed"].append((rel, "; ".join(problems)))
                print(f"{lang}: REJECTED {rel}: {'; '.join(problems)}")
            else:
                r["translated"].append(rel)
                if repaired:
                    r["repaired"].update(repaired)
                    r["repaired_files"].append(rel)
                if warnings:
                    r["warnings"].append((rel, "; ".join(warnings)))
                suffix = f" (repaired {dict(repaired)})" if repaired else ""
                print(f"{lang}: translated {rel} ({job['reason']}, {job['chars']:,} chars){suffix}")
            save_status(lang, status)
    finally:
        save_status(lang, status)


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
) -> None:
    for sub in prepare_all(config, langs, sources, passthrough, locales, options, allow_unbounded):
        translate_language(client, sub, sources, passthrough, lenient, report)


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
            out, problems, repaired, warnings = finalize_translation(rel, info, text, content, check_identity=False)
        except Exception as e:  # noqa: BLE001
            bad.append(f"{rel}: raised {e}")
            continue
        if out != text or problems or repaired or warnings:
            bad.append(f"{rel}: {'differs' if out != text else ''} {problems} {dict(repaired)} {warnings}")
    t.check(f"{len(sources)} scoped sources round-trip byte-for-byte with zero problems", not bad, "; ".join(bad[:5]))
    passthrough = get_passthrough_sources(config, sources)
    t.check("passthrough files are outside the translation scope", not set(passthrough) & set(sources))


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
        "dropped inline code span -> warning, not a problem; delivered text kept",
        not problems
        and not repaired
        and warnings == ["inline code spans 2 -> 1 (missing ['`Selected.Tables`'], added [])"]
        and out == BOM + dropped_span,
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
    out, problems, repaired, warnings = fin(FIXTURE_MD, dropped_span.replace("(guide.md)", "(guia.md)"))
    t.check(
        "inline-code drift does not block the other repairs (link target still restored)",
        not problems and len(warnings) == 1 and repaired["links"] == 1 and out == BOM + dropped_span,
        f"{problems} {warnings} {dict(repaired)}",
    )
    _, problems, _, warnings = fin(FIXTURE_MD, dropped_span, repair=False)
    t.check(
        "inline-code drift is a warning in verify-only mode too", not problems and len(warnings) == 1, str(problems)
    )
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
        self.deliveries: dict[str, str] = {}  # id_content -> translated text (default: echo the source)
        self.empty_responses: set[str] = set()  # id_content answered with an empty data[]

    def translate_ai(self, order: dict[str, Any]) -> list[dict[str, Any]]:
        self.translate_calls += 1
        if self.raise_on_translate_call == self.translate_calls:
            raise TranslatedApiError(
                "POST translate/ai failed with 400: INVALID_PARAMS; boom",
                400,
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
        text = self.deliveries.get(id_content, str(order["content"][0]["text"]))
        return [{"translation": text, "translatable": True, "billed_chars": len(text)}]

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
    os.chdir(tmp)
    try:
        yield tmp
    finally:
        os.chdir(cwd)
        shutil.rmtree(tmp, ignore_errors=True)


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

    def run(self, options: PlanOptions | None = None, allow_unbounded: bool = True, lenient: bool = False) -> None:
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


def cmd_self_test(config: TranslationConfig) -> int:
    t = SelfTest()
    selftest_corpus(t, config)
    selftest_fixtures(t)
    selftest_fake_client(t)
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
        build_config, os.environ.get("TRANSLATED_ENV"), os.environ.get("TRANSLATED_SERVICE_TYPE")
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
        cmd_plan(langs, sources, passthrough, options)
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
    try:
        cmd_run(
            config, client, langs, sources, passthrough, locales, options, args.allow_unbounded, args.lenient, report
        )
    finally:
        summary = report.to_markdown(config)
        print("\n" + summary)
        if args.report:
            Path(args.report).parent.mkdir(parents=True, exist_ok=True)
            Path(args.report).write_text(summary, encoding="utf-8")
    return 1 if report.failed else 0


if __name__ == "__main__":
    sys.exit(main())
