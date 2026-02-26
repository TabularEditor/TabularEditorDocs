#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Language manifest generator for multi-language documentation.

Scans localizedContent/ directory and generates languages.json manifest
with rich metadata for each available language.

Usage:
    python gen_languages.py              # Generate to docfxTranslations/
    python gen_languages.py --output .   # Generate to current directory
"""

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

# Language metadata lookup - maps language codes to display names
# Add new languages here as needed
LANGUAGE_METADATA = {
    "en": {"name": "English", "nativeName": "English"},
    "es": {"name": "Spanish", "nativeName": "Español"},
    "zh": {"name": "Chinese (Simplified)", "nativeName": "简体中文"},
    "zh-tw": {"name": "Chinese (Traditional)", "nativeName": "繁體中文"},
    "ja": {"name": "Japanese", "nativeName": "日本語"},
    "ko": {"name": "Korean", "nativeName": "한국어"},
    "de": {"name": "German", "nativeName": "Deutsch"},
    "fr": {"name": "French", "nativeName": "Français"},
    "it": {"name": "Italian", "nativeName": "Italiano"},
    "pt": {"name": "Portuguese", "nativeName": "Português"},
    "pt-br": {"name": "Portuguese (Brazil)", "nativeName": "Português (Brasil)"},
    "ru": {"name": "Russian", "nativeName": "Русский"},
    "ar": {"name": "Arabic", "nativeName": "العربية", "rtl": True},
    "he": {"name": "Hebrew", "nativeName": "עברית", "rtl": True},
    "nl": {"name": "Dutch", "nativeName": "Nederlands"},
    "pl": {"name": "Polish", "nativeName": "Polski"},
    "sv": {"name": "Swedish", "nativeName": "Svenska"},
    "da": {"name": "Danish", "nativeName": "Dansk"},
    "no": {"name": "Norwegian", "nativeName": "Norsk"},
    "fi": {"name": "Finnish", "nativeName": "Suomi"},
    "cs": {"name": "Czech", "nativeName": "Čeština"},
    "tr": {"name": "Turkish", "nativeName": "Türkçe"},
    "th": {"name": "Thai", "nativeName": "ไทย"},
    "vi": {"name": "Vietnamese", "nativeName": "Tiếng Việt"},
    "id": {"name": "Indonesian", "nativeName": "Bahasa Indonesia"},
    "ms": {"name": "Malay", "nativeName": "Bahasa Melayu"},
    "hi": {"name": "Hindi", "nativeName": "हिन्दी"},
}

# Default language (will be marked as default in manifest)
DEFAULT_LANGUAGE = "en"


def get_language_metadata(code: str) -> dict:
    """Get metadata for a language code, with fallback for unknown languages."""
    code_lower = code.lower()
    
    if code_lower in LANGUAGE_METADATA:
        metadata = LANGUAGE_METADATA[code_lower].copy()
    else:
        # Fallback for unknown languages - use code as name
        metadata = {
            "name": code.upper(),
            "nativeName": code.upper()
        }
    
    metadata["code"] = code_lower
    return metadata


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


def generate_manifest(languages: list[str], default_lang: str = DEFAULT_LANGUAGE) -> dict:
    """Generate the languages manifest with rich metadata."""
    lang_list = []
    
    for code in languages:
        metadata = get_language_metadata(code)
        if code == default_lang:
            metadata["default"] = True
        lang_list.append(metadata)
    
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
        "--default", "-d",
        default=DEFAULT_LANGUAGE,
        help=f"Default language code (default: {DEFAULT_LANGUAGE})"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print manifest without writing to file"
    )
    
    args = parser.parse_args()
    
    # Scan for languages
    localized_dir = Path(args.localized_dir)
    languages = scan_localized_content(localized_dir)
    
    if not languages:
        print(f"Warning: No languages found in {localized_dir}")
        print("Creating manifest with default language only.")
        languages = [args.default]
    
    print(f"Found languages: {', '.join(languages)}")
    
    # Generate manifest
    manifest = generate_manifest(languages, args.default)
    
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
