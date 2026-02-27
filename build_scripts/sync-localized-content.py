#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sync localized content with translation status tracking.

This script manages the synchronization between source content (English)
and localized content, tracking which translations are current vs outdated.

Features:
- Tracks source file hashes to detect changes
- Falls back to English for outdated/missing translations
- Provides status reports on translation coverage

Usage:
    python sync-localized-content.py --status              # Show all languages
    python sync-localized-content.py --status es           # Show Spanish details
    python sync-localized-content.py --sync es             # Sync Spanish content
    python sync-localized-content.py --init es             # Initialize tracking
    python sync-localized-content.py --mark-translated es  # Mark all as translated
    python sync-localized-content.py --json                # JSON output for CI
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config_loader import (
    compute_file_hash,
    get_content_directories,
    get_shared_directories,
    get_root_files,
    get_default_language,
)


# Status values
STATUS_TRANSLATED = "translated"
STATUS_OUTDATED = "outdated"
STATUS_UNTRANSLATED = "untranslated"

# Paths
CONTENT_DIR = Path("content")
LOCALIZED_DIR = Path("localizedContent")
STATUS_FILENAME = ".translation-status.json"


def load_translation_status(lang: str) -> dict[str, Any]:
    """Load the translation status file for a language."""
    status_path = LOCALIZED_DIR / lang / STATUS_FILENAME
    
    if not status_path.exists():
        return {
            "language": lang,
            "lastSync": None,
            "sourceBaseline": str(CONTENT_DIR),
            "files": {},
            "summary": {
                "translated": 0,
                "outdated": 0,
                "untranslated": 0,
                "total": 0,
                "completionPercent": 0
            }
        }
    
    with open(status_path, encoding="utf-8") as f:
        return json.load(f)


def save_translation_status(lang: str, status: dict[str, Any]) -> None:
    """Save the translation status file for a language."""
    status_path = LOCALIZED_DIR / lang / STATUS_FILENAME
    status_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Update timestamp
    status["lastSync"] = datetime.now(timezone.utc).isoformat()
    
    # Recalculate summary
    files = status.get("files", {})
    translated = sum(1 for f in files.values() if f.get("status") == STATUS_TRANSLATED)
    outdated = sum(1 for f in files.values() if f.get("status") == STATUS_OUTDATED)
    untranslated = sum(1 for f in files.values() if f.get("status") == STATUS_UNTRANSLATED)
    total = len(files)
    
    status["summary"] = {
        "translated": translated,
        "outdated": outdated,
        "untranslated": untranslated,
        "total": total,
        "completionPercent": round(translated / total * 100, 1) if total > 0 else 0
    }
    
    with open(status_path, "w", encoding="utf-8") as f:
        json.dump(status, f, indent=2, ensure_ascii=False)


def get_source_files() -> dict[str, str]:
    """Get all source content files with their hashes.
    
    Returns dict mapping relative path to hash.
    """
    files = {}
    
    # Content directories
    for dir_name in get_content_directories():
        dir_path = CONTENT_DIR / dir_name
        if dir_path.exists():
            for file_path in dir_path.rglob("*"):
                if file_path.is_file() and file_path.suffix in [".md", ".yml", ".yaml"]:
                    rel_path = str(file_path.relative_to(CONTENT_DIR)).replace("\\", "/")
                    files[rel_path] = compute_file_hash(file_path)
    
    # Root files
    for file_name in get_root_files():
        file_path = CONTENT_DIR / file_name
        if file_path.exists():
            files[file_name] = compute_file_hash(file_path)
    
    return files


def get_available_languages() -> list[str]:
    """Get list of available language codes from localizedContent/."""
    if not LOCALIZED_DIR.exists():
        return []
    
    languages = []
    for item in LOCALIZED_DIR.iterdir():
        if item.is_dir() and len(item.name) <= 5 and item.name != "en":
            languages.append(item.name)
    
    return sorted(languages)


def check_translation_status(lang: str, source_files: dict[str, str]) -> dict[str, Any]:
    """Check translation status for a language against source files.
    
    Returns updated status dict with current state of each file.
    """
    status = load_translation_status(lang)
    localized_content_dir = LOCALIZED_DIR / lang / "content"
    
    new_files = {}
    
    for rel_path, source_hash in source_files.items():
        localized_file = localized_content_dir / rel_path
        file_info = status.get("files", {}).get(rel_path, {})
        
        if not localized_file.exists():
            # No translation exists
            new_files[rel_path] = {
                "sourceHash": source_hash,
                "status": STATUS_UNTRANSLATED,
                "lastChecked": datetime.now(timezone.utc).isoformat()
            }
        else:
            stored_hash = file_info.get("sourceHash", "")
            
            if stored_hash == source_hash:
                # Source hasn't changed, translation is current
                new_files[rel_path] = {
                    "sourceHash": source_hash,
                    "status": STATUS_TRANSLATED,
                    "lastChecked": datetime.now(timezone.utc).isoformat(),
                    "translatedAt": file_info.get("translatedAt", datetime.now(timezone.utc).isoformat())
                }
            else:
                # Source changed since translation was made
                new_files[rel_path] = {
                    "sourceHash": source_hash,
                    "status": STATUS_OUTDATED,
                    "previousHash": stored_hash,
                    "lastChecked": datetime.now(timezone.utc).isoformat(),
                    "translatedAt": file_info.get("translatedAt")
                }
    
    status["files"] = new_files
    return status


def sync_language(lang: str, source_files: dict[str, str], dry_run: bool = False) -> dict[str, int]:
    """Sync content for a language, falling back to English for outdated/missing.
    
    Returns dict with counts of actions taken.
    """
    status = check_translation_status(lang, source_files)
    localized_content_dir = LOCALIZED_DIR / lang / "content"
    
    counts = {"copied": 0, "replaced": 0, "kept": 0}
    
    for rel_path, file_info in status["files"].items():
        source_file = CONTENT_DIR / rel_path
        dest_file = localized_content_dir / rel_path
        file_status = file_info.get("status")
        
        if file_status == STATUS_TRANSLATED:
            # Keep existing translation
            counts["kept"] += 1
        elif file_status == STATUS_OUTDATED:
            # Replace with English (fallback)
            if not dry_run:
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_file, dest_file)
                # Update status to untranslated (since we replaced with English)
                file_info["status"] = STATUS_UNTRANSLATED
                file_info["replacedAt"] = datetime.now(timezone.utc).isoformat()
            counts["replaced"] += 1
            print(f"  Replaced (outdated): {rel_path}")
        elif file_status == STATUS_UNTRANSLATED:
            # Copy English as fallback
            if not dry_run:
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                if not dest_file.exists():
                    shutil.copy2(source_file, dest_file)
                    counts["copied"] += 1
                    print(f"  Copied (new): {rel_path}")
                else:
                    counts["kept"] += 1
            else:
                if not dest_file.exists():
                    counts["copied"] += 1
                else:
                    counts["kept"] += 1
    
    # Copy shared directories (assets, api) - always overwrite
    for dir_name in get_shared_directories():
        src = CONTENT_DIR / dir_name
        dest = localized_content_dir / dir_name
        if src.exists() and not dry_run:
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest)
            print(f"  Synced shared: {dir_name}/")
    
    if not dry_run:
        save_translation_status(lang, status)
    
    return counts


def sync_english(dry_run: bool = False) -> dict[str, int]:
    """Sync English content (copy all from source).
    
    Note: This preserves any existing files in the destination that don't exist
    in the source (e.g., redirect stub files generated by gen_redirects.py).
    """
    en_content_dir = LOCALIZED_DIR / "en" / "content"
    counts = {"copied": 0, "updated": 0}
    
    if not dry_run:
        en_content_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy content directories (overwrite existing, preserve unrelated)
    for dir_name in get_content_directories():
        src = CONTENT_DIR / dir_name
        dest = en_content_dir / dir_name
        if src.exists():
            if not dry_run:
                # Remove destination dir if exists (to get clean copy of this dir)
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(src, dest)
            file_count = sum(1 for _ in src.rglob("*") if _.is_file())
            counts["copied"] += file_count
    
    # Copy shared directories (overwrite)
    for dir_name in get_shared_directories():
        src = CONTENT_DIR / dir_name
        dest = en_content_dir / dir_name
        if src.exists() and not dry_run:
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest)
    
    # Copy root files (overwrite)
    for file_name in get_root_files():
        src = CONTENT_DIR / file_name
        if src.exists():
            if not dry_run:
                shutil.copy2(src, en_content_dir / file_name)
            counts["copied"] += 1
    
    return counts


def init_language(lang: str, source_files: dict[str, str]) -> None:
    """Initialize translation tracking for an existing language.
    
    Marks all existing translations as 'translated' with current source hash.
    """
    localized_content_dir = LOCALIZED_DIR / lang / "content"
    
    if not localized_content_dir.exists():
        print(f"Error: No content found for '{lang}' at {localized_content_dir}")
        return
    
    status = {
        "language": lang,
        "lastSync": datetime.now(timezone.utc).isoformat(),
        "sourceBaseline": str(CONTENT_DIR),
        "files": {}
    }
    
    for rel_path, source_hash in source_files.items():
        localized_file = localized_content_dir / rel_path
        
        if localized_file.exists():
            # File exists - mark as translated with current hash
            status["files"][rel_path] = {
                "sourceHash": source_hash,
                "status": STATUS_TRANSLATED,
                "lastChecked": datetime.now(timezone.utc).isoformat(),
                "translatedAt": datetime.now(timezone.utc).isoformat()
            }
        else:
            # File missing - mark as untranslated
            status["files"][rel_path] = {
                "sourceHash": source_hash,
                "status": STATUS_UNTRANSLATED,
                "lastChecked": datetime.now(timezone.utc).isoformat()
            }
    
    save_translation_status(lang, status)
    
    summary = status["summary"]
    print(f"Initialized tracking for '{lang}':")
    print(f"  Translated: {summary['translated']}")
    print(f"  Untranslated: {summary['untranslated']}")


def mark_translated(lang: str, file_paths: list[str] | None, source_files: dict[str, str]) -> None:
    """Mark files as translated with current source hash.
    
    If file_paths is None, marks all files in the language.
    """
    status = load_translation_status(lang)
    now = datetime.now(timezone.utc).isoformat()
    
    if file_paths is None:
        # Mark all files
        file_paths = list(source_files.keys())
    
    updated = 0
    for rel_path in file_paths:
        if rel_path in source_files:
            status["files"][rel_path] = {
                "sourceHash": source_files[rel_path],
                "status": STATUS_TRANSLATED,
                "lastChecked": now,
                "translatedAt": now
            }
            updated += 1
    
    save_translation_status(lang, status)
    print(f"Marked {updated} file(s) as translated for '{lang}'")


def print_status_summary(json_output: bool = False) -> None:
    """Print status summary for all languages."""
    languages = get_available_languages()
    source_files = get_source_files()
    
    results = []
    
    for lang in languages:
        status = check_translation_status(lang, source_files)
        summary = status.get("summary", {})
        results.append({
            "language": lang,
            "translated": summary.get("translated", 0),
            "outdated": summary.get("outdated", 0),
            "untranslated": summary.get("untranslated", 0),
            "total": summary.get("total", 0),
            "completionPercent": summary.get("completionPercent", 0)
        })
    
    if json_output:
        print(json.dumps({"languages": results}, indent=2))
        return
    
    if not results:
        print("No languages found in localizedContent/")
        return
    
    print("\nTranslation Status Report")
    print("=" * 60)
    print()
    print(f"{'Language':<10} {'Translated':<12} {'Outdated':<10} {'Untranslated':<14} {'Completion':<10}")
    print("-" * 60)
    
    for r in results:
        print(f"{r['language']:<10} {r['translated']:<12} {r['outdated']:<10} {r['untranslated']:<14} {r['completionPercent']:.1f}%")
    
    print()
    print("Run with --status <lang> for details.")


def print_language_status(lang: str, source_files: dict[str, str], json_output: bool = False) -> None:
    """Print detailed status for a specific language."""
    status = check_translation_status(lang, source_files)
    files = status.get("files", {})
    summary = status.get("summary", {})
    
    if json_output:
        print(json.dumps(status, indent=2))
        return
    
    print(f"\nTranslation Status: {lang}")
    print("=" * 60)
    print()
    print(f"Summary: {summary['translated']}/{summary['total']} translated "
          f"({summary['completionPercent']:.1f}%), "
          f"{summary['outdated']} outdated, "
          f"{summary['untranslated']} untranslated")
    print()
    
    # Group by status
    outdated = [(p, f) for p, f in files.items() if f.get("status") == STATUS_OUTDATED]
    untranslated = [(p, f) for p, f in files.items() if f.get("status") == STATUS_UNTRANSLATED]
    
    if outdated:
        print(f"OUTDATED ({len(outdated)} files - will use English fallback):")
        for path, info in sorted(outdated)[:20]:  # Limit output
            print(f"  - {path}")
        if len(outdated) > 20:
            print(f"  ... and {len(outdated) - 20} more")
        print()
    
    if untranslated:
        print(f"UNTRANSLATED ({len(untranslated)} files - using English):")
        for path, info in sorted(untranslated)[:20]:
            print(f"  - {path}")
        if len(untranslated) > 20:
            print(f"  ... and {len(untranslated) - 20} more")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync localized content with translation tracking"
    )
    parser.add_argument(
        "--status", "-s",
        nargs="?",
        const="__all__",
        metavar="LANG",
        help="Show translation status (optionally for specific language)"
    )
    parser.add_argument(
        "--sync",
        metavar="LANG",
        help="Sync content for a language (use 'en' for English)"
    )
    parser.add_argument(
        "--init",
        metavar="LANG",
        help="Initialize tracking for existing translations"
    )
    parser.add_argument(
        "--mark-translated",
        metavar="LANG",
        help="Mark files as translated (all files if no --files specified)"
    )
    parser.add_argument(
        "--files",
        nargs="+",
        help="Specific files to mark as translated"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    
    args = parser.parse_args()
    
    # Get source files (needed for most operations)
    source_files = get_source_files()
    
    if args.status:
        if args.status == "__all__":
            print_status_summary(args.json)
        else:
            print_language_status(args.status, source_files, args.json)
        return 0
    
    if args.sync:
        lang = args.sync
        print(f"Syncing content for '{lang}'...")
        
        if lang == "en":
            counts = sync_english(args.dry_run)
            print(f"\nEnglish sync complete: {counts['copied']} files copied")
        else:
            counts = sync_language(lang, source_files, args.dry_run)
            print(f"\nSync complete for '{lang}':")
            print(f"  Kept (translated): {counts['kept']}")
            print(f"  Replaced (outdated->English): {counts['replaced']}")
            print(f"  Copied (new->English): {counts['copied']}")
        return 0
    
    if args.init:
        init_language(args.init, source_files)
        return 0
    
    if args.mark_translated:
        mark_translated(args.mark_translated, args.files, source_files)
        return 0
    
    # Default: show help
    parser.print_help()
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
