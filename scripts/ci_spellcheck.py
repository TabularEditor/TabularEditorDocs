#!/usr/bin/env python3
"""
CI Typo Check - Detect known typos in English markdown files.

This script provides a reliable, fast check for 100% confirmed typos.
It scans English markdown files in the content/ directory while skipping
code blocks, inline code, YAML frontmatter, and localized content.

For more nuanced checks, use cspell or LLM-based spellcheck.
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import NamedTuple, TypedDict


class TypoEntry(TypedDict):
    """A typo pattern entry."""
    wrong: str
    correct: str
    category: str


class TypoData(TypedDict, total=False):
    """Typo data file structure."""
    description: str
    version: str
    typos: list[TypoEntry]
    false_positives: list[str]


class TypoMatch(NamedTuple):
    """A typo match found in a file."""
    file: Path
    line_num: int
    line_text: str
    typo: str
    correction: str


class CompiledTypo(NamedTuple):
    """A precompiled typo pattern."""
    pattern: re.Pattern[str]
    wrong: str
    correct: str


# Directories to skip (pruned before traversal for performance)
EXCLUDED_DIRS = {
    ".git", ".github", ".vscode", ".idea",
    "node_modules", "venv", ".venv", "__pycache__",
    "site-packages", "dist", "build", ".cache",
    "_site", "public", "output",  # Generated site output
    "localizedContent",  # Skip non-English localized content
}


def load_and_validate_typo_data(data_path: Path) -> TypoData:
    """Load and validate typo patterns from JSON file."""
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {data_path}: {e}") from e

    # Validate structure
    if "typos" not in data:
        raise ValueError(f"Missing 'typos' key in {data_path}")
    if not isinstance(data["typos"], list):
        raise TypeError(f"'typos' must be a list in {data_path}")

    for i, entry in enumerate(data["typos"]):
        if not isinstance(entry, dict):
            raise TypeError(f"Typo entry {i} must be a dict")
        if "wrong" not in entry or "correct" not in entry:
            raise ValueError(f"Typo entry {i} missing 'wrong' or 'correct' key")
        # Validate string types and non-empty values
        if not isinstance(entry["wrong"], str) or not isinstance(entry["correct"], str):
            raise TypeError(f"Typo entry {i} 'wrong' and 'correct' must be strings")
        if not entry["wrong"].strip() or not entry["correct"].strip():
            raise ValueError(f"Typo entry {i} 'wrong' and 'correct' must be non-empty")

    return data


def compile_typo_patterns(typos: list[TypoEntry]) -> list[CompiledTypo]:
    """Precompile regex patterns for all typos (done once, not per file)."""
    compiled: list[CompiledTypo] = []
    for typo in typos:
        pattern = re.compile(rf"\b{re.escape(typo['wrong'])}\b", re.IGNORECASE)
        compiled.append(CompiledTypo(
            pattern=pattern,
            wrong=typo["wrong"],
            correct=typo["correct"],
        ))
    return compiled


def compile_false_positive_patterns(false_positives: list[str]) -> list[re.Pattern[str]]:
    """Precompile regex patterns for false positives with word boundaries."""
    return [
        re.compile(rf"\b{re.escape(fp)}\b", re.IGNORECASE)
        for fp in false_positives
    ]


def strip_code_blocks(content: str) -> list[tuple[int, str]]:
    """
    Return lines with code blocks removed.

    Returns list of (original_line_num, line_text) tuples,
    skipping lines inside fenced code blocks, indented code blocks,
    and YAML frontmatter.
    """
    # Strip UTF-8 BOM if present (appears at start of some files)
    if content.startswith("\ufeff"):
        content = content[1:]

    lines = content.splitlines()
    result: list[tuple[int, str]] = []
    in_fenced_block = False
    in_frontmatter = False
    prev_blank = True  # Track if previous line was blank (for indented code detection)

    for line_num, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Handle YAML frontmatter (must start at line 1, allow leading whitespace)
        if line_num == 1 and stripped == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if stripped == "---" or stripped == "...":
                in_frontmatter = False
            continue

        # Check for fenced code block markers (``` or ~~~)
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fenced_block = not in_fenced_block
            prev_blank = False
            continue

        if in_fenced_block:
            prev_blank = False
            continue

        # Skip indented code blocks (4+ spaces or tab after blank line)
        # Per CommonMark: indented code requires preceding blank line
        is_indented_code = (
            prev_blank and
            len(line) > 0 and
            (line.startswith("    ") or line.startswith("\t"))
        )
        if is_indented_code:
            # Don't update prev_blank - stay in indented code mode
            continue

        # Track blank lines for indented code detection
        prev_blank = len(stripped) == 0

        if stripped:  # Non-empty, non-code line
            # Strip inline code: handle both `code` and ``code with `backticks` inside``
            # First handle double-backtick spans, then single-backtick spans
            line_no_inline = re.sub(r"``[^`]+``", "", line)
            line_no_inline = re.sub(r"`[^`]+`", "", line_no_inline)
            result.append((line_num, line_no_inline))

    return result


def find_typos_in_lines(
    file_path: Path,
    lines: list[tuple[int, str]],
    compiled_typos: list[CompiledTypo],
    fp_patterns: list[re.Pattern[str]],
) -> list[TypoMatch]:
    """Search lines for known typos."""
    matches: list[TypoMatch] = []

    for line_num, line in lines:
        for compiled in compiled_typos:
            if compiled.pattern.search(line):
                # Check if this line matches a false positive pattern
                if any(fp_pat.search(line) for fp_pat in fp_patterns):
                    continue

                matches.append(TypoMatch(
                    file=file_path,
                    line_num=line_num,
                    line_text=line.strip(),
                    typo=compiled.wrong,
                    correction=compiled.correct,
                ))

    return matches


def find_repeated_words(
    file_path: Path,
    lines: list[tuple[int, str]],
) -> list[TypoMatch]:
    """Find repeated words like 'the the' or 'is is'."""
    matches: list[TypoMatch] = []

    # Catch any repeated word of 2+ chars (more comprehensive)
    repeated_pattern = re.compile(r"\b(\w{2,})\s+\1\b", re.IGNORECASE)

    for line_num, line in lines:
        # Use finditer to catch ALL repeated words on a line
        for match in repeated_pattern.finditer(line):
            matches.append(TypoMatch(
                file=file_path,
                line_num=line_num,
                line_text=line.strip(),
                typo=match.group(0),
                correction=f"{match.group(1)} (remove duplicate)",
            ))

    return matches


def is_safe_path(file_path: Path, project_root: Path) -> bool:
    """Check if path is safely within project root (no symlink escapes)."""
    try:
        resolved = file_path.resolve()
        root_resolved = project_root.resolve()
        return resolved.is_relative_to(root_resolved)
    except (OSError, ValueError):
        return False


def escape_gha_annotation(text: str) -> str:
    """Escape GitHub Actions workflow command control characters.

    GHA uses %, :, and newlines as control characters in annotations.
    Escaping prevents malicious input from injecting extra annotations.
    """
    return (
        text
        .replace("%", "%25")
        .replace("\r", "%0D")
        .replace("\n", "%0A")
        .replace(":", "%3A")
    )


def find_markdown_files(project_root: Path) -> list[Path]:
    """
    Find markdown files using os.walk with directory pruning.

    Scans the entire project root while excluding build artifacts,
    version control directories, and non-English localized content.

    This is more efficient than rglob() because it prunes excluded
    directories BEFORE traversing into them.
    """
    md_files: list[Path] = []

    for dirpath, dirnames, filenames in os.walk(project_root):
        # Prune excluded directories IN PLACE (modifies dirnames)
        # This prevents os.walk from descending into them
        dirnames[:] = [
            d for d in dirnames
            if d not in EXCLUDED_DIRS and not d.startswith(".")
        ]

        # Collect markdown files
        for filename in filenames:
            if filename.endswith(".md"):
                file_path = Path(dirpath) / filename
                # Safety check for symlinks
                if is_safe_path(file_path, project_root):
                    md_files.append(file_path)

    return md_files


def main() -> int:
    """Run spellcheck and return exit code."""
    # Find project root (where data/common_typos.json lives)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    data_path = project_root / "data" / "common_typos.json"
    if not data_path.exists():
        print(f"::error::Typo data not found at {data_path}", file=sys.stderr)
        return 1

    # Load and validate typo data
    try:
        typo_data = load_and_validate_typo_data(data_path)
    except (ValueError, TypeError) as e:
        print(f"::error::Invalid typo data file: {e}", file=sys.stderr)
        return 1

    typos = typo_data.get("typos", [])
    false_positives = typo_data.get("false_positives", [])

    # Precompile all patterns ONCE (not per file)
    compiled_typos = compile_typo_patterns(typos)
    fp_patterns = compile_false_positive_patterns(false_positives)

    print(f"Loaded {len(typos)} typo patterns")
    print(f"Loaded {len(false_positives)} false positive exclusions")
    print()

    # Find markdown files with directory pruning
    md_files = find_markdown_files(project_root)

    print(f"Scanning {len(md_files)} markdown files...")
    print()

    # Search for typos
    all_matches: list[TypoMatch] = []

    for md_file in md_files:
        try:
            # Read file ONCE
            content = md_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            print(f"Warning: Could not read {md_file}: {e}", file=sys.stderr)
            continue

        # Strip code blocks and inline code
        lines = strip_code_blocks(content)

        # Find typos (pass preprocessed lines)
        matches = find_typos_in_lines(md_file, lines, compiled_typos, fp_patterns)
        all_matches.extend(matches)

        # Find repeated words (pass same preprocessed lines)
        repeated = find_repeated_words(md_file, lines)
        all_matches.extend(repeated)

    # Report results
    if all_matches:
        print("=" * 60)
        print("TYPOS FOUND")
        print("=" * 60)
        print()

        # Group by file
        by_file: dict[Path, list[TypoMatch]] = {}
        for match in all_matches:
            by_file.setdefault(match.file, []).append(match)

        for file_path, matches in sorted(by_file.items()):
            rel_path = file_path.relative_to(project_root)
            print(f"File: {rel_path}")
            for match in matches:
                # GitHub Actions annotation format for inline PR comments
                # Escape control characters to prevent annotation injection
                safe_typo = escape_gha_annotation(match.typo)
                safe_correction = escape_gha_annotation(match.correction)
                print(f"::error file={rel_path},line={match.line_num}::"
                      f"Typo: '{safe_typo}' should be '{safe_correction}'")
                print(f"  Line {match.line_num}: '{match.typo}' -> '{match.correction}'")
                # Truncate long lines
                line_preview = match.line_text[:80]
                if len(match.line_text) > 80:
                    line_preview += "..."
                print(f"    {line_preview}")
            print()

        print("=" * 60)
        print(f"Total: {len(all_matches)} typo(s) found in {len(by_file)} file(s)")
        print()
        print("These are 100% reliable typo patterns.")
        print("If a match is a false positive, add it to data/common_typos.json false_positives list.")
        return 1
    else:
        print(f"Typo check passed: {len(md_files)} files checked, no typos found.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
