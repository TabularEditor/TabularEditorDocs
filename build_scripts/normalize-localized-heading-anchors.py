#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Stabilize DocFX heading anchors across translated content.

DocFX derives a heading's anchor (its HTML id) from the heading *text*. Cross
references hardcode the English anchor, e.g. `[..](xref:te-cli-commands#model-io)`
or `<a href="...#object-paths">`. When a heading is translated the generated
slug changes ("Model I/O" -> "model-io" becomes "E/S del modelo" ->
"es-del-modelo"), so every English `#anchor` link breaks in es/zh and DocFX emits
an `InvalidBookmark` warning. English builds stay clean because the anchors match
there.

This script makes the *English* anchor resolvable in every translated page. For
each localized page it reads the matching English source file, computes each
heading's English DocFX slug, and injects a hidden bookmark anchor carrying that
slug immediately before the corresponding translated heading:

    <a id="model-io" data-loc-xref></a>
    ## E/S del modelo

DocFX accepts the injected `id` as a valid bookmark, so `#model-io` resolves and
the link lands on the right section, while the heading keeps its translated text.
This neutralizes the whole class of warning for current and future pages without
touching translations.

Headings are aligned to the English source positionally (Crowdin preserves
heading structure). If the heading count differs (a translation added/removed a
heading, or is stale), the file is skipped and reported rather than risk a
misaligned anchor. Frontmatter and fenced code blocks are skipped. Injected
anchors are tagged `data-loc-xref` so the script is idempotent: it strips its own
prior anchors before recomputing.

English (`en`) is never modified - it is the source of the slugs.

Usage:
    python normalize-localized-heading-anchors.py              # all languages (except en)
    python normalize-localized-heading-anchors.py --dry-run    # preview only
    python normalize-localized-heading-anchors.py --check      # exit 1 if changes needed (CI)
    python normalize-localized-heading-anchors.py es           # only Spanish
"""

import argparse
import re
import sys
from pathlib import Path

TEDOC_ROOT = Path(__file__).resolve().parent.parent
LOCALIZED_DIR = TEDOC_ROOT / "localizedContent"

FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
# A bookmark anchor this script previously injected.
INJECTED_RE = re.compile(r'^<a id="[^"]*" data-loc-xref></a>$')
# Inline markdown to strip from heading text before slugifying.
MD_LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")


def slugify(text: str) -> str:
    """Replicate DocFX/markdig heading-id generation.

    Verified against DocFX 2.78 output: lowercase; drop every character that is
    not a Unicode letter/digit/hyphen/underscore; turn each space into a single
    hyphen (consecutive spaces are NOT collapsed, e.g. "Connection & Auth" ->
    "connection--auth"); Unicode letters (incl. CJK) are preserved verbatim.
    """
    # Strip inline markdown so the text matches what DocFX renders.
    text = MD_LINK_RE.sub(r"\1", text)
    text = text.replace("`", "")
    text = re.sub(r"(\*\*|__|\*|~~)", "", text)
    text = text.strip().lower()
    out = []
    for ch in text:
        if ch == " " or ch == "\t":
            out.append("-")
        elif ch.isalnum() or ch in "-_":
            out.append(ch)
        # everything else (punctuation, symbols) is dropped
    return "".join(out)


def parse_headings(text: str):
    """Return (heading_texts, heading_line_indices) for ATX headings, skipping
    YAML frontmatter and fenced code blocks. Indices refer to `text.split(nl)`."""
    lines = text.split("\n")
    texts, indices = [], []
    fence_char, fence_len = "", 0
    in_frontmatter = False
    for i, raw in enumerate(lines):
        line = raw.rstrip("\r")
        # YAML frontmatter delimited by leading '---' on the very first line.
        if i == 0 and line.strip() == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if line.strip() in ("---", "..."):
                in_frontmatter = False
            continue
        fence = FENCE_RE.match(line)
        if fence:
            run, tail = fence.group(1), fence.group(2)
            char, length = run[0], len(run)
            if not fence_char:
                fence_char, fence_len = char, length
            elif char == fence_char and length >= fence_len and not tail.strip():
                fence_char, fence_len = "", 0
            continue
        if fence_char:
            continue
        m = HEADING_RE.match(line)
        if m:
            texts.append(m.group(2))
            indices.append(i)
    return texts, indices


def dedup_slugs(texts):
    """Compute slugs with DocFX-style collision suffixes (-1, -2, ...)."""
    seen = {}
    slugs = []
    for t in texts:
        s = slugify(t)
        if s in seen:
            seen[s] += 1
            s = f"{s}-{seen[s]}"
        else:
            seen[s] = 0
        slugs.append(s)
    return slugs


def english_source_for(loc_path: Path, lang: str) -> Path:
    """Map localizedContent/<lang>/content/.../x.md -> content/.../x.md."""
    rel = loc_path.relative_to(LOCALIZED_DIR / lang)  # e.g. content/features/x.md
    return TEDOC_ROOT / rel


def process_file(loc_path: Path, lang: str, dry_run: bool):
    """Inject English-slug anchors before translated headings. Returns one of:
    ('ok', n_injected) | ('skip-no-source', 0) | ('skip-mismatch', (en, loc))."""
    with open(loc_path, "r", encoding="utf-8", newline="") as f:
        text = f.read()
    newline = "\r\n" if "\r\n" in text else "\n"
    norm = text.replace("\r\n", "\n")
    had_bom = norm.startswith("﻿")
    if had_bom:
        norm = norm[1:]

    # Idempotency: drop previously injected anchors before recomputing.
    cleaned_lines = [ln for ln in norm.split("\n") if not INJECTED_RE.match(ln)]

    en_path = english_source_for(loc_path, lang)
    if not en_path.exists():
        return ("skip-no-source", 0)

    with open(en_path, "r", encoding="utf-8-sig", newline="") as f:
        en_text = f.read().replace("\r\n", "\n")
    en_texts, _ = parse_headings(en_text)
    loc_texts, loc_indices = parse_headings("\n".join(cleaned_lines))

    if len(en_texts) != len(loc_texts):
        # Still write back the cleaned file (stale anchors removed) so we never
        # leave a misaligned anchor behind, but inject nothing.
        rebuilt = newline.join(cleaned_lines)
        if had_bom:
            rebuilt = "﻿" + rebuilt
        if rebuilt != text and not dry_run:
            with open(loc_path, "w", encoding="utf-8", newline="") as f:
                f.write(rebuilt)
        return ("skip-mismatch", (len(en_texts), len(loc_texts)))

    en_slugs = dedup_slugs(en_texts)
    inject_at = dict(zip(loc_indices, en_slugs))

    out = []
    for i, ln in enumerate(cleaned_lines):
        if i in inject_at:
            out.append(f'<a id="{inject_at[i]}" data-loc-xref></a>')
        out.append(ln)
    rebuilt = newline.join(out)
    if had_bom:
        rebuilt = "\ufeff" + rebuilt

    changed = rebuilt != text
    if changed and not dry_run:
        with open(loc_path, "w", encoding="utf-8", newline="") as f:
            f.write(rebuilt)
    return ("ok", len(inject_at) if changed else 0)


def iter_languages(lang):
    if lang:
        return [lang] if lang != "en" else []
    if not LOCALIZED_DIR.exists():
        return []
    return sorted(
        d.name for d in LOCALIZED_DIR.iterdir()
        if d.is_dir() and d.name != "en"
    )


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Inject English heading-slug bookmark anchors into translated pages."
    )
    ap.add_argument("lang", nargs="?", help="Language code (default: all except en)")
    ap.add_argument("--dry-run", action="store_true", help="Preview without writing")
    ap.add_argument("--check", action="store_true",
                    help="Exit 1 if any file needs changes (implies --dry-run). For CI.")
    args = ap.parse_args()
    dry_run = args.dry_run or args.check

    if not LOCALIZED_DIR.exists():
        print(f"Error: {LOCALIZED_DIR} not found.")
        return 1

    total_files = total_anchors = changed_files = mismatches = 0
    for lang in iter_languages(args.lang):
        base = LOCALIZED_DIR / lang
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.md")):
            if path.name == "toc.md":
                continue  # navigation files use '## @uid' lines, not real headings
            status, info = process_file(path, lang, dry_run)
            total_files += 1
            rel = path.relative_to(LOCALIZED_DIR)
            if status == "skip-mismatch":
                mismatches += 1
                en_n, loc_n = info
                print(f"  SKIP (heading count {en_n} en vs {loc_n} loc): {rel}")
            elif status == "ok" and info:
                changed_files += 1
                total_anchors += info

    verb = "Would inject" if dry_run else "Injected"
    print(f"\n{verb} {total_anchors} heading anchor(s) across {changed_files} file(s); "
          f"{mismatches} file(s) skipped on heading-count mismatch; "
          f"{total_files} file(s) scanned.")

    if args.check and (changed_files or mismatches):
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(1)
