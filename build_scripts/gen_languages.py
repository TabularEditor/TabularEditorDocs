#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Language manifest generator for multi-language documentation.

Scans localizedContent/ directory and generates languages.json manifest
with rich metadata for each available language.

Language metadata is loaded from docfxTranslations/language-metadata.json.
Unknown languages fall back to using the code as the display name.

Usage:
    python gen_languages.py              # Generate to docfxTranslations/
    python gen_languages.py --output .   # Generate to current directory
"""

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path


# Default paths
METADATA_FILE = "docfxTranslations/language-metadata.json"
DEFAULT_LANGUAGE = "en"

# Cached metadata (loaded on first use)
_language_metadata: dict | None = None
_default_language: str | None = None


def load_language_metadata(metadata_path: Path | None = None) -> tuple[dict, str]:
    """Load language metadata from JSON file.
    
    Returns tuple of (metadata_dict, default_language).
    """
    global _language_metadata, _default_language
    
    if _language_metadata is not None:
        return _language_metadata, _default_language or DEFAULT_LANGUAGE
    
    # Find metadata file
    if metadata_path is None:
        metadata_path = Path(METADATA_FILE)
    
    if not metadata_path.exists():
        print(f"Warning: {metadata_path} not found, using built-in defaults")
        _language_metadata = {
            "en": {"name": "English", "nativeName": "English"}
        }
        _default_language = DEFAULT_LANGUAGE
        return _language_metadata, _default_language
    
    with open(metadata_path, encoding="utf-8") as f:
        data = json.load(f)
    
    _language_metadata = data.get("languages", {})
    _default_language = data.get("defaultLanguage", DEFAULT_LANGUAGE)
    
    return _language_metadata, _default_language


def get_language_metadata(code: str, metadata: dict | None = None) -> dict:
    """Get metadata for a language code, with fallback for unknown languages."""
    code_lower = code.lower()
    
    if metadata is None:
        metadata, _ = load_language_metadata()
    
    if code_lower in metadata:
        result = metadata[code_lower].copy()
    else:
        # Fallback for unknown languages - use code as name
        result = {
            "name": code.upper(),
            "nativeName": code.upper()
        }
    
    result["code"] = code_lower
    return result


def scan_localized_content(localized_dir: Path) -> list[str]:
    """Scan localizedContent directory for available languages."""
    if not localized_dir.exists():
        return []
    
    languages = []
    for item in localized_dir.iterdir():
        if item.is_dir():
            # Check if it looks like a language code (2-5 chars)
            name = item.name.lower()
            if 2 <= len(name) <= 5 and name.replace("-", "").isalpha():
                # Verify it has content (docfx.json or content folder)
                if (item / "docfx.json").exists() or (item / "content").exists():
                    languages.append(name)
    
    return sorted(languages)


def generate_manifest(languages: list[str], metadata: dict, default_lang: str) -> dict:
    """Generate the languages manifest with rich metadata."""
    lang_list = []
    
    for code in languages:
        lang_meta = get_language_metadata(code, metadata)
        if code == default_lang:
            lang_meta["default"] = True
        lang_list.append(lang_meta)
    
    # Ensure default language is first in the list
    lang_list.sort(key=lambda x: (not x.get("default", False), x["code"]))
    
    return {
        "languages": lang_list,
        "defaultLanguage": default_lang,
        "generated": datetime.now(timezone.utc).isoformat()
    }


def main():
    parser = argparse.ArgumentParser(
        description="Generate languages.json manifest from localizedContent/"
    )
    parser.add_argument(
        "--output", "-o",
        default="docfxTranslations",
        help="Output directory for languages.json (default: docfxTranslations)"
    )
    parser.add_argument(
        "--localized-dir", "-l",
        default="localizedContent",
        help="Directory containing localized content (default: localizedContent)"
    )
    parser.add_argument(
        "--metadata", "-m",
        default=METADATA_FILE,
        help=f"Path to language metadata JSON (default: {METADATA_FILE})"
    )
    parser.add_argument(
        "--default", "-d",
        help="Override default language code (default: from metadata file)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print manifest without writing to file"
    )
    
    args = parser.parse_args()
    
    # Load language metadata
    metadata, default_from_file = load_language_metadata(Path(args.metadata))
    default_lang = args.default or default_from_file
    
    print(f"Loaded metadata from: {args.metadata}")
    print(f"Default language: {default_lang}")
    
    # Scan for languages
    localized_dir = Path(args.localized_dir)
    languages = scan_localized_content(localized_dir)
    
    if not languages:
        print(f"Warning: No languages found in {localized_dir}")
        print("Creating manifest with default language only.")
        languages = [default_lang]
    
    print(f"Found languages: {', '.join(languages)}")
    
    # Generate manifest
    manifest = generate_manifest(languages, metadata, default_lang)
    
    if args.dry_run:
        print("\nGenerated manifest (dry run):")
        print(json.dumps(manifest, indent=2, ensure_ascii=False))
        return 0
    
    # Write manifest
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "languages.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print(f"\nGenerated: {output_file}")
    print(f"Languages: {len(manifest['languages'])}")
    
    return 0


if __name__ == "__main__":
    exit(main())
