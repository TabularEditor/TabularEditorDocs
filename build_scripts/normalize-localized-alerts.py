#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Normalize DocFX alerts in Crowdin-translated content.

Crowdin collapses DocFX/GitHub-style alerts that are nested inside list items,
joining the marker line and the first content line. This:

    > [!NOTE]
    > text

comes back from Crowdin as:

    > [!NOTE]> text

DocFX requires the alert marker (e.g. [!NOTE]) to stand alone on its line.
Otherwise the parser emits an "invalid-note-section" warning and downgrades the
alert to a plain <blockquote>, losing the styled NOTE/TIP/IMPORTANT box.

This script finds the collapsed form and splits it back into two lines,
preserving the original indentation so the alert stays inside its list item.
It is idempotent and only rewrites the exact collapsed pattern, so it is safe
to run after every Crowdin pull. Lines inside fenced code blocks are skipped so
documentation that shows alert syntax verbatim is never altered.

Usage:
    python normalize-localized-alerts.py                 # fix all languages
    python normalize-localized-alerts.py --dry-run       # preview only
    python normalize-localized-alerts.py --check         # exit 1 if fixes needed (CI)
    python normalize-localized-alerts.py es              # fix only Spanish
"""

import argparse
import sys
import re
from pathlib import Path

# localizedContent/ lives one level up from this build_scripts/ directory.
TEDOC_ROOT = Path(__file__).resolve().parent.parent
LOCALIZED_DIR = TEDOC_ROOT / "localizedContent"

# A blockquote line where a DocFX alert marker is immediately followed by '>'
# and inline content, e.g. "   > [!NOTE]> text". Captures the leading
# indentation, the marker, and the trailing content.
COLLAPSED_ALERT_RE = re.compile(r"^([ \t]*)>[ \t]?(\[![A-Za-z]+\])>[ \t]?(.*)$")

# A fenced-code delimiter: 3+ backticks or 3+ tildes, optionally indented.
# Group 1 is the run of fence characters; group 2 is any trailing text
# (an info string on an opener; must be blank on a valid closer).
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")


def normalize_text(text: str, newline: str) -> tuple[str, int]:
    """Return (new_text, fixes) with collapsed alerts split into two lines.

    Fenced code blocks are tracked per CommonMark so alert-looking text inside a
    code sample is never rewritten: a fence is only *closed* by a delimiter using
    the same character, at least as long as the opener, with no trailing text.
    This keeps state in sync across nested/mismatched fences (e.g. a ```` block
    that contains ``` lines, or backtick and tilde fences mixed in one file).
    """
    lines = text.split(newline)
    out: list[str] = []
    fence_char = ""  # "" when outside a fence, else the opener's char ("`"/"~")
    fence_len = 0
    fixes = 0

    for line in lines:
        fence = FENCE_RE.match(line)
        if fence:
            run, tail = fence.group(1), fence.group(2)
            char, length = run[0], len(run)
            if not fence_char:
                fence_char, fence_len = char, length  # opening fence
            elif char == fence_char and length >= fence_len and not tail.strip():
                fence_char, fence_len = "", 0  # matching closing fence
            # Otherwise it's a fence-looking line inside the block: leave as content.
            out.append(line)
            continue

        if not fence_char:
            m = COLLAPSED_ALERT_RE.match(line)
            if m:
                indent, marker, rest = m.group(1), m.group(2), m.group(3)
                out.append(f"{indent}> {marker}")
                out.append(f"{indent}> {rest}" if rest else f"{indent}>")
                fixes += 1
                continue

        out.append(line)

    return newline.join(out), fixes


def normalize_file(path: Path, dry_run: bool) -> int:
    """Normalize a single file in place. Returns number of alerts fixed."""
    with open(path, "r", encoding="utf-8", newline="") as f:
        text = f.read()

    newline = "\r\n" if "\r\n" in text else "\n"
    new_text, fixes = normalize_text(text, newline)

    if fixes and not dry_run:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new_text)

    return fixes


def iter_markdown_files(lang: str | None):
    """Yield every .md file under localizedContent/ (optionally one language)."""
    base = LOCALIZED_DIR / lang if lang else LOCALIZED_DIR
    if not base.exists():
        return
    yield from sorted(base.rglob("*.md"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Split Crowdin-collapsed DocFX alerts back into two lines."
    )
    parser.add_argument(
        "lang", nargs="?",
        help="Language code to fix (default: all languages under localizedContent/)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would change without writing files",
    )
    parser.add_argument(
        "--check", action="store_true",
        help="Exit 1 if any file needs fixing (implies --dry-run). For CI.",
    )
    args = parser.parse_args()

    dry_run = args.dry_run or args.check

    if not LOCALIZED_DIR.exists():
        print(f"Error: {LOCALIZED_DIR} not found.")
        return 1

    total_files = 0
    total_fixes = 0

    for path in iter_markdown_files(args.lang):
        fixes = normalize_file(path, dry_run)
        if fixes:
            total_files += 1
            total_fixes += fixes
            rel = path.relative_to(LOCALIZED_DIR)
            verb = "Would fix" if dry_run else "Fixed"
            print(f"  {verb} {fixes} alert(s): {rel}")

    if total_fixes == 0:
        print("No collapsed alerts found. Everything is clean.")
        return 0

    action = "would be fixed" if dry_run else "fixed"
    print(f"\n{total_fixes} alert(s) across {total_files} file(s) {action}.")

    if args.check:
        print("Run without --check to apply the fixes.")
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(1)
