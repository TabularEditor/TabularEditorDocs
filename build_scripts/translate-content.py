#!/usr/bin/env python
"""
Translate documentation content with Translated (TranslationOS API).

Replaces the Crowdin GitHub integration while keeping its contract: English
sources live in content/, translations land at
localizedContent/{lang}/content/{same path} using two-letter folder codes, and
translation PRs arrive on the `localization` branch.

Per language the script:

  plan      compare English source hashes with localizedContent/{lang}/.translation-status.json
            and list what is missing, outdated, in flight or orphaned
  submit    POST /translate for every missing/outdated file (one request per file and
            language) and record the job under "pendingJobs" in the status file
  poll      POST /status for each pending job; when "delivered", verify the structure of
            the translation against the English source, write the file and mark it
            "translated" at the source hash it was translated from
  baseline  one-time migration step: mark every existing translation as current so only
            future changes are sent (optionally hashing the English sources at a git ref,
            e.g. the last Crowdin merge, so files edited since are picked up)

Scope (which files are translated and how) comes from the "translation" section of
metadata/build-config.json; locales come from "translatedLocale" in
metadata/language-metadata.json. Target languages are the folders under
localizedContent/ that contain a content/ directory (same rule as gen_languages.py).

Usage (run from the docs repo root):
    python build_scripts/translate-content.py --plan [--lang es]
    python build_scripts/translate-content.py --submit [--lang es] [--limit 3] [--file "features/*.md"]
    python build_scripts/translate-content.py --poll [--wait 20]
    python build_scripts/translate-content.py --run --wait 25 --report report.md   # submit + poll (CI)
    python build_scripts/translate-content.py --baseline [--baseline-ref d376766]

Environment:
    TRANSLATED_API_KEY        required for --submit / --poll / --run
    TRANSLATED_BASE_URL       overrides translation.baseUrl (sandbox by default)
    TRANSLATED_SERVICE_TYPE   overrides translation.serviceType

Exit code is 1 for configuration or API errors. Individual files that fail
verification do not fail the run; they are recorded under "failures" in the status
file and listed in the report so the PR reviewer sees them.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from config_loader import (
    compute_file_hash,
    get_default_language,
    get_shared_directories,
    load_build_config,
)

CONTENT_DIR = Path("content")
LOCALIZED_DIR = Path("localizedContent")
STATUS_FILENAME = ".translation-status.json"
LANGUAGE_METADATA_PATH = Path("metadata/language-metadata.json")

STATUS_TRANSLATED = "translated"
STATUS_UNTRANSLATED = "untranslated"

# Translated request statuses that end a job.
DELIVERED_STATUSES = {"delivered"}
FAILED_STATUSES = {"error", "cancelled", "canceled", "rejected"}

# A job not delivered within this window is treated as lost (same budget as Housekeeping).
PENDING_TIMEOUT = timedelta(days=7)

CONTENT_TYPES = {
    ".md": "text/markdown",
    ".html": "text/html",
    ".htm": "text/html",
    ".json": "application/json",
    ".yml": "application/json",   # toc.yml is sent as a JSON map of its `name` values, see extract_yaml_names
    ".yaml": "application/json",
}

# Markdown structure regexes (mirror normalize-localized-heading-anchors.py).
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
HEADING_RE = re.compile(r"^#{1,6}\s+\S")
ALERT_RE = re.compile(r"\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION|include)\b", re.IGNORECASE)
LINK_TARGET_RE = re.compile(r"\]\(([^)\s]+)")
FRONTMATTER_RE = re.compile(r"\A(﻿)?---\r?\n(.*?)\r?\n---[ \t]*\r?\n", re.S)
FM_TRANSLATABLE_RE = re.compile(r"^(title|description):[ \t]*(.*?)[ \t]*$")
YAML_NAME_RE = re.compile(r"^(\s*-?\s*name:[ \t]*)(.*?)[ \t]*$")
HTML_TAG_RE = re.compile(r"<\s*([a-zA-Z][a-zA-Z0-9-]*)")
HTML_REF_RE = re.compile(r"""\b(?:href|src)\s*=\s*["']([^"']+)["']""")
PLACEHOLDER_RE = re.compile(r"\{[a-zA-Z_][a-zA-Z0-9_]*\}")


def utc_now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

class TranslationConfig:
    def __init__(self, build_config: dict[str, Any]) -> None:
        section = build_config.get("translation")
        if not section:
            raise SystemExit("metadata/build-config.json has no 'translation' section.")
        self.base_url: str = os.environ.get("TRANSLATED_BASE_URL") or section.get(
            "baseUrl", "https://api.sandbox.translated.com/v2/"
        )
        if not self.base_url.endswith("/"):
            self.base_url += "/"
        self.service_type: str = os.environ.get("TRANSLATED_SERVICE_TYPE") or section.get("serviceType", "premium")
        self.source_locale: str = section.get("sourceLocale", "en-US")
        self.sources: list[str] = [s["pattern"] if isinstance(s, dict) else s for s in section.get("sources", [])]
        self.ignore: list[str] = list(section.get("ignore", []))
        self.instructions: str = section.get("instructions", "")
        self.batch_size: int = int(section.get("batchSize", 200))
        if not self.sources:
            raise SystemExit("translation.sources in metadata/build-config.json is empty.")

    @property
    def is_sandbox(self) -> bool:
        return "sandbox" in self.base_url


def load_locale_map() -> dict[str, str]:
    """Map two-letter folder code -> Translated locale (RFC 3066, e.g. es -> es-ES)."""
    with open(LANGUAGE_METADATA_PATH, encoding="utf-8") as f:
        meta = json.load(f)
    languages = meta.get("languages", meta)
    return {
        code: entry["translatedLocale"]
        for code, entry in languages.items()
        if isinstance(entry, dict) and entry.get("translatedLocale")
    }


def get_target_languages(default_lang: str) -> list[str]:
    if not LOCALIZED_DIR.exists():
        return []
    return sorted(
        p.name for p in LOCALIZED_DIR.iterdir()
        if p.is_dir() and p.name != default_lang and (p / "content").is_dir()
    )


# ---------------------------------------------------------------------------
# Source discovery
# ---------------------------------------------------------------------------

def rel_str(path: Path, base: Path) -> str:
    return str(path.relative_to(base)).replace("\\", "/")


def get_scoped_sources(config: TranslationConfig) -> dict[str, str]:
    """Return {relative path -> sha256} for every English file in translation scope."""
    shared = set(get_shared_directories())
    files: dict[str, str] = {}
    for pattern in config.sources:
        for path in sorted(CONTENT_DIR.glob(pattern)):
            if not path.is_file():
                continue
            rel = rel_str(path, CONTENT_DIR)
            top = rel.split("/", 1)[0]
            if top in shared:
                continue
            if any(fnmatch.fnmatch(rel, ig) for ig in config.ignore):
                continue
            files[rel] = compute_file_hash(path)
    return files


def hash_bytes(data: bytes) -> str:
    """Same normalization as config_loader.compute_file_hash (CRLF -> LF)."""
    return "sha256:" + hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def hashes_at_git_ref(ref: str, rel_paths: list[str]) -> dict[str, str]:
    """Hash content/{rel} as it was at a git ref. Missing files are omitted."""
    result: dict[str, str] = {}
    for rel in rel_paths:
        proc = subprocess.run(
            ["git", "show", f"{ref}:{CONTENT_DIR.as_posix()}/{rel}"],
            capture_output=True,
        )
        if proc.returncode == 0:
            result[rel] = hash_bytes(proc.stdout)
    return result


# ---------------------------------------------------------------------------
# Status file (shared with sync-localized-content.py)
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
    status.setdefault("pendingJobs", {})
    status.setdefault("failures", {})
    return status


def save_status(lang: str, status: dict[str, Any]) -> None:
    files = status["files"]
    total = len(files)
    translated = sum(1 for f in files.values() if f.get("status") == STATUS_TRANSLATED)
    outdated = sum(1 for f in files.values() if f.get("status") == "outdated")
    untranslated = sum(1 for f in files.values() if f.get("status") == STATUS_UNTRANSLATED)
    status["summary"] = {
        "translated": translated,
        "outdated": outdated,
        "untranslated": untranslated,
        "total": total,
        "completionPercent": round(translated / total * 100, 1) if total else 0,
        "pendingJobs": len(status["pendingJobs"]),
        "failures": len(status["failures"]),
    }
    # Keep the optional sections out of the file when empty so diffs stay small.
    for key in ("pendingJobs", "failures"):
        if not status[key]:
            status.pop(key)
    path = status_path(lang)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(status, f, indent=2, ensure_ascii=False)
        f.write("\n")
    status.setdefault("pendingJobs", {})
    status.setdefault("failures", {})


# ---------------------------------------------------------------------------
# Content extraction / reinsertion
# ---------------------------------------------------------------------------

def read_text(path: Path) -> str:
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def extract_yaml_names(text: str) -> tuple[str, int]:
    """toc.yml: only `name:` values are translatable. Send them as a JSON object so
    hrefs, homepage paths and structure never reach the translator."""
    names: dict[str, str] = {}
    for i, line in enumerate(text.lstrip("﻿").splitlines()):
        m = YAML_NAME_RE.match(line)
        if m and m.group(2):
            names[f"n{i}"] = m.group(2)
    return json.dumps(names, ensure_ascii=False, indent=2), len(names)


def reinsert_yaml_names(source_text: str, translated_json: str) -> str:
    names = json.loads(translated_json)
    if not isinstance(names, dict):
        raise ValueError("translated toc payload is not a JSON object")
    bom = "﻿" if source_text.startswith("﻿") else ""
    lines = source_text.lstrip("﻿").splitlines(keepends=True)
    for key, value in names.items():
        idx = int(key[1:])
        line = lines[idx]
        eol = line[len(line.rstrip("\r\n")):]
        m = YAML_NAME_RE.match(line.rstrip("\r\n"))
        if not m:
            raise ValueError(f"toc line {idx} no longer holds a name entry")
        value = str(value).strip()
        # Quote values YAML would otherwise misread; keep the source's quoting if it had any.
        already_quoted = value.startswith(('"', "'")) and value.endswith(value[0])
        if not already_quoted and re.search(r"[:#\[\]{},&*!|>'\"%@`]", value):
            value = json.dumps(value, ensure_ascii=False)
        lines[idx] = f"{m.group(1)}{value}{eol}"
    return bom + "".join(lines)


def prepare_payload(rel: str, source_text: str) -> tuple[str, str, dict[str, Any]]:
    """Return (content, content_type, extra job info) for a source file."""
    suffix = Path(rel).suffix.lower()
    content_type = CONTENT_TYPES.get(suffix)
    if content_type is None:
        raise ValueError(f"no content type for {rel}")
    if suffix in (".yml", ".yaml"):
        content, count = extract_yaml_names(source_text)
        return content, content_type, {"mode": "yaml-names", "units": count}
    # Strip a BOM so the translator never sees it; it is re-added on write when the source had one.
    return source_text.lstrip("﻿"), content_type, {"mode": "raw"}


def split_frontmatter(text: str) -> tuple[str, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return "", text
    return text[: m.end()], text[m.end():]


def merge_frontmatter(source_fm: str, translated_fm: str) -> str:
    """Rebuild the frontmatter from the English source, taking only translated
    `title`/`description` values. Keeps uid, author, dates and applies_to intact
    regardless of what the translator did to them."""
    if not source_fm:
        return ""
    translated_values: dict[str, str] = {}
    for line in translated_fm.splitlines():
        m = FM_TRANSLATABLE_RE.match(line)
        if m and m.group(2):
            translated_values[m.group(1)] = m.group(2)
    out: list[str] = []
    for line in source_fm.splitlines(keepends=True):
        bare = line.rstrip("\r\n")
        eol = line[len(bare):]
        m = FM_TRANSLATABLE_RE.match(bare)
        if m and m.group(1) in translated_values:
            out.append(f"{m.group(1)}: {translated_values[m.group(1)]}{eol}")
        else:
            out.append(line)
    return "".join(out)


def md_skeleton(body: str) -> dict[str, Any]:
    fences = 0
    headings = 0
    alerts: Counter[str] = Counter()
    links: Counter[str] = Counter()
    in_fence = False
    for line in body.splitlines():
        if FENCE_RE.match(line):
            fences += 1
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if HEADING_RE.match(line):
            headings += 1
        for a in ALERT_RE.findall(line):
            alerts[a.upper()] += 1
        for t in LINK_TARGET_RE.findall(line):
            links[t] += 1
    return {"fences": fences, "headings": headings, "alerts": alerts, "links": links}


def verify_markdown(source_body: str, translated_body: str) -> list[str]:
    s, t = md_skeleton(source_body), md_skeleton(translated_body)
    problems: list[str] = []
    if s["fences"] != t["fences"]:
        problems.append(f"code fences {s['fences']} -> {t['fences']}")
    if s["headings"] != t["headings"]:
        problems.append(f"headings {s['headings']} -> {t['headings']}")
    if s["alerts"] != t["alerts"]:
        problems.append(f"alert/include markers {dict(s['alerts'])} -> {dict(t['alerts'])}")
    if s["links"] != t["links"]:
        missing = list((s["links"] - t["links"]).elements())[:5]
        added = list((t["links"] - s["links"]).elements())[:5]
        problems.append(f"link targets changed (missing {missing}, added {added})")
    return problems


def verify_html(source: str, translated: str) -> list[str]:
    problems: list[str] = []
    s_tags, t_tags = Counter(x.lower() for x in HTML_TAG_RE.findall(source)), Counter(x.lower() for x in HTML_TAG_RE.findall(translated))
    if s_tags != t_tags:
        problems.append(f"tag counts differ {dict(s_tags - t_tags) or dict(t_tags - s_tags)}")
    s_refs, t_refs = Counter(HTML_REF_RE.findall(source)), Counter(HTML_REF_RE.findall(translated))
    if s_refs != t_refs:
        problems.append("href/src attributes changed")
    return problems


def verify_json_strings(source: str, translated: str) -> list[str]:
    try:
        s_obj, t_obj = json.loads(source.lstrip("﻿")), json.loads(translated.lstrip("﻿"))
    except json.JSONDecodeError as e:
        return [f"translated JSON does not parse: {e}"]
    if not isinstance(s_obj, dict) or not isinstance(t_obj, dict):
        return ["JSON root is not an object"]
    if set(s_obj) != set(t_obj):
        return [f"keys differ: missing {sorted(set(s_obj) - set(t_obj))[:5]} added {sorted(set(t_obj) - set(s_obj))[:5]}"]
    problems = []
    for key, value in s_obj.items():
        if isinstance(value, str) and Counter(PLACEHOLDER_RE.findall(value)) != Counter(PLACEHOLDER_RE.findall(str(t_obj[key]))):
            problems.append(f"placeholders changed in '{key}'")
    return problems


def finalize_translation(rel: str, job: dict[str, Any], source_text: str, translated: str) -> tuple[str, list[str]]:
    """Turn delivered content into the file to write. Returns (text, problems)."""
    suffix = Path(rel).suffix.lower()
    bom = "﻿" if source_text.startswith("﻿") else ""
    crlf = "\r\n" in source_text

    if job.get("mode") == "yaml-names":
        text = reinsert_yaml_names(source_text, translated)
        return text, []

    translated = translated.lstrip("﻿")
    if crlf and "\r\n" not in translated:
        translated = translated.replace("\n", "\r\n")

    if suffix == ".md":
        src_fm, src_body = split_frontmatter(source_text.lstrip("﻿"))
        tr_fm, tr_body = split_frontmatter(translated)
        problems = verify_markdown(src_body, tr_body)
        return bom + merge_frontmatter(src_fm, tr_fm) + tr_body, problems
    if suffix in (".html", ".htm"):
        return bom + translated, verify_html(source_text, translated)
    if suffix == ".json":
        problems = verify_json_strings(source_text, translated)
        if not problems:
            # Re-serialize so the file keeps the source formatting conventions.
            translated = json.dumps(json.loads(translated), indent=2, ensure_ascii=False) + "\n"
            if crlf:
                translated = translated.replace("\n", "\r\n")
        return bom + translated, problems
    return bom + translated, []


# ---------------------------------------------------------------------------
# Translated API client (port of Housekeeping's TranslatedClient)
# ---------------------------------------------------------------------------

class TranslatedClient:
    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url
        self.api_key = api_key

    def _post(self, endpoint: str, body: Any, retries: int = 3) -> Any:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        url = self.base_url + endpoint
        for attempt in range(retries + 1):
            req = urllib.request.Request(
                url, data=data, method="POST",
                headers={"x-api-key": self.api_key, "Content-Type": "application/json", "Accept": "application/json"},
            )
            try:
                with urllib.request.urlopen(req, timeout=180) as resp:
                    return json.loads(resp.read().decode("utf-8") or "null")
            except urllib.error.HTTPError as e:
                payload = e.read().decode("utf-8", errors="replace")[:500]
                if e.code in (429, 500, 502, 503, 504) and attempt < retries:
                    time.sleep(2 ** attempt * 2)
                    continue
                raise SystemExit(f"Translated API POST {endpoint} failed with {e.code}: {payload}") from None
            except urllib.error.URLError as e:
                if attempt < retries:
                    time.sleep(2 ** attempt * 2)
                    continue
                raise SystemExit(f"Translated API POST {endpoint} unreachable: {e.reason}") from None
        raise SystemExit(f"Translated API POST {endpoint}: retries exhausted")

    def translate(self, orders: list[dict[str, Any]]) -> list[dict[str, Any]]:
        items = self._post("translate", orders)
        if not isinstance(items, list):
            raise SystemExit(f"Translated API POST translate returned an unexpected body: {str(items)[:300]}")
        return items

    def status(self, id_content: str) -> list[dict[str, Any]]:
        # POST, not GET: the status endpoint rejects GET with 405.
        items = self._post("status", {"id_content": id_content, "fetch_content": True})
        return items if isinstance(items, list) else []


def require_client(config: TranslationConfig) -> TranslatedClient:
    api_key = os.environ.get("TRANSLATED_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("TRANSLATED_API_KEY is not set.")
    return TranslatedClient(config.base_url, api_key)


# ---------------------------------------------------------------------------
# Planning
# ---------------------------------------------------------------------------

class LanguagePlan:
    def __init__(self, lang: str) -> None:
        self.lang = lang
        self.to_submit: list[tuple[str, str]] = []   # (rel, reason)
        self.in_flight: list[str] = []
        self.orphans: list[str] = []                  # translated files whose English source is gone
        self.current = 0


def target_file(lang: str, rel: str) -> Path:
    return LOCALIZED_DIR / lang / "content" / rel


def build_plan(lang: str, sources: dict[str, str], status: dict[str, Any], file_filters: list[str]) -> LanguagePlan:
    plan = LanguagePlan(lang)
    files = status["files"]
    pending = status["pendingJobs"]
    for rel, src_hash in sources.items():
        if file_filters and not any(fnmatch.fnmatch(rel, pat) for pat in file_filters):
            continue
        entry = files.get(rel, {})
        exists = target_file(lang, rel).exists()
        if entry.get("status") == STATUS_TRANSLATED and entry.get("sourceHash") == src_hash and exists:
            plan.current += 1
            continue
        job = pending.get(rel)
        if job and job.get("sourceHash") == src_hash:
            plan.in_flight.append(rel)
            continue
        if not exists or entry.get("status") != STATUS_TRANSLATED:
            reason = "missing" if not exists else "untranslated"
        else:
            reason = "outdated"
        plan.to_submit.append((rel, reason))
    scoped_suffixes = set(CONTENT_TYPES)
    for rel in files:
        if (rel not in sources and Path(rel).suffix.lower() in scoped_suffixes
                and target_file(lang, rel).exists() and not (CONTENT_DIR / rel).exists()):
            plan.orphans.append(rel)
    return plan


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

class RunReport:
    def __init__(self) -> None:
        self.lines: list[str] = []
        self.per_lang: dict[str, dict[str, Any]] = {}

    def lang(self, lang: str) -> dict[str, Any]:
        return self.per_lang.setdefault(lang, {
            "submitted": [], "delivered": [], "failed": [], "still_pending": [], "deleted": [], "chars": 0,
        })

    def to_markdown(self, config: TranslationConfig) -> str:
        env = "sandbox" if config.is_sandbox else "production"
        out = [f"## Translation run ({env}, service type `{config.service_type}`)", ""]
        out.append("| Language | Submitted | Delivered | Still pending | Failed | Removed |")
        out.append("|---|---|---|---|---|---|")
        for lang, r in sorted(self.per_lang.items()):
            out.append(f"| {lang} | {len(r['submitted'])} | {len(r['delivered'])} | {len(r['still_pending'])} | {len(r['failed'])} | {len(r['deleted'])} |")
        for lang, r in sorted(self.per_lang.items()):
            if r["chars"]:
                out.append(f"\n{lang}: {r['chars']:,} characters submitted.")
            if r["failed"]:
                out.append(f"\n### {lang}: failed (translation kept as before)\n")
                out.extend(f"- `{rel}` — {reason}" for rel, reason in r["failed"])
            if r["still_pending"]:
                out.append(f"\n### {lang}: still pending at Translated\n")
                out.extend(f"- `{rel}`" for rel in r["still_pending"])
        return "\n".join(out) + "\n"


def cmd_plan(config: TranslationConfig, langs: list[str], sources: dict[str, str], file_filters: list[str]) -> None:
    for lang in langs:
        status = load_status(lang)
        plan = build_plan(lang, sources, status, file_filters)
        chars = 0
        print(f"\n{lang}: {plan.current} current, {len(plan.to_submit)} to submit, "
              f"{len(plan.in_flight)} in flight, {len(plan.orphans)} orphaned, {len(status['failures'])} failed earlier")
        for rel, reason in plan.to_submit:
            text = read_text(CONTENT_DIR / rel)
            content, _, _ = prepare_payload(rel, text)
            chars += len(content)
            print(f"  submit  {reason:<12} {rel}")
        for rel in plan.in_flight:
            print(f"  pending              {rel}")
        for rel in plan.orphans:
            print(f"  remove               {rel}")
        for rel, failure in status["failures"].items():
            print(f"  failed               {rel}: {failure.get('error')}")
        if plan.to_submit:
            print(f"  ~{chars:,} characters would be submitted for {lang}")


def cmd_baseline(langs: list[str], sources: dict[str, str], ref: str | None) -> None:
    ref_hashes = hashes_at_git_ref(ref, list(sources)) if ref else {}
    for lang in langs:
        status = load_status(lang)
        current = outdated = missing = 0
        for rel, src_hash in sources.items():
            if not target_file(lang, rel).exists():
                status["files"][rel] = {"sourceHash": "", "status": STATUS_UNTRANSLATED}
                missing += 1
                continue
            baseline_hash = ref_hashes.get(rel, src_hash) if ref else src_hash
            status["files"][rel] = {"sourceHash": baseline_hash, "status": STATUS_TRANSLATED}
            if baseline_hash == src_hash:
                current += 1
            else:
                outdated += 1
        save_status(lang, status)
        print(f"{lang}: baseline written — {current} current, {outdated} changed since {ref or 'HEAD'}, {missing} missing")


def cmd_submit(config: TranslationConfig, client: TranslatedClient, langs: list[str], sources: dict[str, str],
               locales: dict[str, str], file_filters: list[str], limit: int, report: RunReport) -> None:
    for lang in langs:
        locale = locales.get(lang)
        if not locale:
            raise SystemExit(f"No translatedLocale for '{lang}' in {LANGUAGE_METADATA_PATH}; add e.g. \"translatedLocale\": \"{lang}-XX\".")
        status = load_status(lang)
        plan = build_plan(lang, sources, status, file_filters)
        r = report.lang(lang)

        for rel in plan.orphans:
            target_file(lang, rel).unlink()
            status["files"].pop(rel, None)
            status["pendingJobs"].pop(rel, None)
            status["failures"].pop(rel, None)
            r["deleted"].append(rel)
            print(f"{lang}: removed orphan {rel}")

        queue = plan.to_submit[:limit] if limit else plan.to_submit
        orders: list[dict[str, Any]] = []
        jobs: dict[str, dict[str, Any]] = {}
        for rel, reason in queue:
            text = read_text(CONTENT_DIR / rel)
            content, content_type, info = prepare_payload(rel, text)
            if not content.strip() or info.get("units") == 0:
                # Nothing translatable (e.g. an empty file): copy the source through.
                write_text(target_file(lang, rel), text)
                status["files"][rel] = {"sourceHash": sources[rel], "status": STATUS_TRANSLATED}
                continue
            id_content = f"{lang}/{rel}"
            order: dict[str, Any] = {
                "id_content": id_content,
                "content": content,
                "content_type": content_type,
                "source_language": config.source_locale,
                "target_languages": [locale],
                "service_type": config.service_type,
            }
            if config.instructions:
                order["context"] = {"instructions": config.instructions}
            orders.append(order)
            jobs[rel] = {**info, "idContent": id_content, "sourceHash": sources[rel], "reason": reason,
                         "contentType": content_type, "chars": len(content)}

        for start in range(0, len(orders), config.batch_size):
            batch = orders[start:start + config.batch_size]
            items = client.translate(batch)
            by_id = {str(item.get("id_content")): item for item in items}
            for rel, job in list(jobs.items()):
                item = by_id.get(job["idContent"])
                if item is None or job["idContent"] not in {o["id_content"] for o in batch}:
                    continue
                job.update({
                    "jobId": item.get("id"),
                    "targetLanguage": item.get("target_language", locale),
                    "serviceType": config.service_type,
                    "submittedAt": utc_now(),
                })
                status["pendingJobs"][rel] = job
                status["failures"].pop(rel, None)
                r["submitted"].append(rel)
                r["chars"] += job["chars"]
                print(f"{lang}: submitted {rel} ({job['reason']}, {job['chars']:,} chars, job {job.get('jobId')})")
            for o in batch:
                if str(o["id_content"]) not in by_id:
                    rel = o["id_content"].split("/", 1)[1]
                    status["failures"][rel] = {"error": "no job returned by POST translate", "at": utc_now()}
                    r["failed"].append((rel, "no job returned by POST translate"))
        save_status(lang, status)


def cmd_poll(config: TranslationConfig, client: TranslatedClient, langs: list[str], sources: dict[str, str],
             wait_minutes: float, lenient: bool, report: RunReport) -> None:
    deadline = time.monotonic() + wait_minutes * 60
    first_round = True
    while True:
        outstanding = 0
        for lang in langs:
            status = load_status(lang)
            r = report.lang(lang)
            changed = False
            for rel, job in list(status["pendingJobs"].items()):
                items = client.status(job["idContent"])
                item = next((i for i in items if str(i.get("id")) == str(job.get("jobId"))), None)
                state = (item or {}).get("status", "unknown")
                if state in DELIVERED_STATUSES and item is not None:
                    changed = True
                    status["pendingJobs"].pop(rel)
                    problems = apply_delivery(lang, rel, job, item, sources, status, lenient)
                    if problems:
                        r["failed"].append((rel, "; ".join(problems)))
                        print(f"{lang}: REJECTED {rel}: {'; '.join(problems)}")
                    else:
                        r["delivered"].append(rel)
                        print(f"{lang}: delivered {rel}")
                elif state in FAILED_STATUSES:
                    changed = True
                    status["pendingJobs"].pop(rel)
                    status["failures"][rel] = {"error": f"Translated status '{state}'", "at": utc_now(), "jobId": job.get("jobId")}
                    r["failed"].append((rel, f"Translated status '{state}'"))
                    print(f"{lang}: FAILED {rel}: status {state}")
                else:
                    submitted = datetime.strptime(job.get("submittedAt", utc_now()), "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
                    if datetime.now(UTC) - submitted > PENDING_TIMEOUT:
                        changed = True
                        status["pendingJobs"].pop(rel)
                        status["failures"][rel] = {"error": f"not delivered within {PENDING_TIMEOUT.days} days (last status '{state}')", "at": utc_now(), "jobId": job.get("jobId")}
                        r["failed"].append((rel, "timed out"))
                        print(f"{lang}: TIMED OUT {rel}")
                    else:
                        outstanding += 1
                        if first_round:
                            print(f"{lang}: waiting  {rel} ({state})")
                time.sleep(0.05)
            if changed:
                save_status(lang, status)
        first_round = False
        if outstanding == 0 or time.monotonic() >= deadline:
            break
        remaining = int(deadline - time.monotonic())
        print(f"{outstanding} job(s) still pending; polling again in 30s ({remaining}s left)")
        time.sleep(min(30, max(1, remaining)))

    for lang in langs:
        status = load_status(lang)
        report.lang(lang)["still_pending"] = sorted(status["pendingJobs"])


def apply_delivery(lang: str, rel: str, job: dict[str, Any], item: dict[str, Any], sources: dict[str, str],
                   status: dict[str, Any], lenient: bool) -> list[str]:
    translated = item.get("translated_content")
    if not isinstance(translated, str) or not translated:
        status["failures"][rel] = {"error": "delivered without translated_content", "at": utc_now(), "jobId": job.get("jobId")}
        return ["delivered without translated_content"]
    source_path = CONTENT_DIR / rel
    if not source_path.exists():
        return ["English source no longer exists"]
    source_text = read_text(source_path)
    if job.get("sourceHash") != sources.get(rel):
        # Source changed while the job was in flight; the next submit run picks it up again.
        problems_note = "source changed while translating; will resubmit"
        try:
            text, problems = finalize_translation(rel, job, source_text, translated)
        except Exception as e:  # noqa: BLE001 - reported to the reviewer, never crashes the run
            return [f"{problems_note}; could not reinsert: {e}"]
        if problems and not lenient:
            status["failures"][rel] = {"error": "; ".join(problems), "at": utc_now(), "jobId": job.get("jobId")}
            return problems
        write_text(target_file(lang, rel), text)
        status["files"][rel] = {"sourceHash": job.get("sourceHash", ""), "status": STATUS_TRANSLATED}
        return []
    try:
        text, problems = finalize_translation(rel, job, source_text, translated)
    except Exception as e:  # noqa: BLE001
        status["failures"][rel] = {"error": f"could not reinsert translation: {e}", "at": utc_now(), "jobId": job.get("jobId")}
        return [f"could not reinsert translation: {e}"]
    if problems and not lenient:
        status["failures"][rel] = {"error": "; ".join(problems), "at": utc_now(), "jobId": job.get("jobId")}
        return problems
    write_text(target_file(lang, rel), text)
    status["files"][rel] = {"sourceHash": sources[rel], "status": STATUS_TRANSLATED}
    status["failures"].pop(rel, None)
    if problems:
        print(f"{lang}: written despite warnings ({'; '.join(problems)}): {rel}")
    return []


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Translate docs content with Translated (TranslationOS).")
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--plan", action="store_true", help="show what would be submitted; no API calls")
    actions.add_argument("--submit", action="store_true", help="submit missing/outdated files")
    actions.add_argument("--poll", action="store_true", help="fetch delivered translations")
    actions.add_argument("--run", action="store_true", help="submit, then poll (CI mode)")
    actions.add_argument("--baseline", action="store_true", help="mark existing translations as current")
    parser.add_argument("--lang", action="append", help="limit to a language folder (repeatable)")
    parser.add_argument("--file", action="append", default=[], help="glob relative to content/ (repeatable)")
    parser.add_argument("--limit", type=int, default=0, help="submit at most N files per language")
    parser.add_argument("--wait", type=float, default=0, help="minutes to keep polling for deliveries")
    parser.add_argument("--lenient", action="store_true", help="write translations that fail structural verification")
    parser.add_argument("--baseline-ref", help="git ref whose content/ hashes become the baseline (e.g. the last Crowdin merge)")
    parser.add_argument("--report", help="write a markdown run summary to this path")
    args = parser.parse_args()

    if not CONTENT_DIR.exists():
        print("Run from the docs repo root (content/ not found).", file=sys.stderr)
        return 1

    build_config = load_build_config()
    config = TranslationConfig(build_config)
    default_lang = get_default_language(build_config)
    langs = args.lang or get_target_languages(default_lang)
    if not langs:
        print("No target languages found under localizedContent/.", file=sys.stderr)
        return 1
    sources = get_scoped_sources(config)
    print(f"{len(sources)} source files in scope; languages: {', '.join(langs)}; "
          f"endpoint: {config.base_url} ({'sandbox' if config.is_sandbox else 'PRODUCTION'}), service type: {config.service_type}")

    if args.plan:
        cmd_plan(config, langs, sources, args.file)
        return 0
    if args.baseline:
        cmd_baseline(langs, sources, args.baseline_ref)
        return 0

    client = require_client(config)
    report = RunReport()
    if args.submit or args.run:
        cmd_submit(config, client, langs, sources, load_locale_map(), args.file, args.limit, report)
    if args.poll or args.run:
        cmd_poll(config, client, langs, sources, args.wait, args.lenient, report)

    summary = report.to_markdown(config)
    print("\n" + summary)
    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report).write_text(summary, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
