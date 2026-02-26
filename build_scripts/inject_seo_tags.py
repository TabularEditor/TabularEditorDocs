#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Inject SEO tags (hreflang, canonical) into built HTML files.

This script runs after docfx build to add:
1. Canonical URLs - prevents duplicate content penalties
2. hreflang tags - tells search engines about language alternatives
3. x-default hreflang - indicates the default language version

Usage:
    python inject_seo_tags.py                          # Process _site/
    python inject_seo_tags.py --base-url https://...   # Custom base URL
    python inject_seo_tags.py --dry-run                # Preview without changes
"""

import argparse
import json
import os
import re
from pathlib import Path
from typing import Optional

from config_loader import get_default_language


# Default base URL for the documentation site
DEFAULT_BASE_URL = "https://docs.tabulareditor.com"

# Default language (used for x-default hreflang) - loaded from config
DEFAULT_LANGUAGE = get_default_language()


def load_languages(site_dir: Path) -> list[dict]:
    """Load languages from the manifest file."""
    manifest_path = site_dir / "languages.json"
    
    if not manifest_path.exists():
        print(f"Warning: {manifest_path} not found, using default [en]")
        return [{"code": "en", "name": "English", "nativeName": "English", "default": True}]
    
    with open(manifest_path, encoding="utf-8") as f:
        data = json.load(f)
    
    languages = data.get("languages", [])
    
    # Handle both simple array and rich metadata formats
    result = []
    for lang in languages:
        if isinstance(lang, str):
            result.append({"code": lang})
        else:
            result.append(lang)
    
    return result


def get_page_path(html_file: Path, site_dir: Path, lang: str) -> str:
    """Get the page path relative to the language folder.
    
    Example: _site/en/features/overview.html -> features/overview.html
    """
    rel_path = html_file.relative_to(site_dir / lang)
    return str(rel_path).replace("\\", "/")


def generate_seo_tags(
    page_path: str,
    current_lang: str,
    languages: list[dict],
    base_url: str,
    default_lang: str = DEFAULT_LANGUAGE
) -> str:
    """Generate canonical and hreflang link tags."""
    lines = []
    
    # Canonical URL - always points to the current page
    canonical_url = f"{base_url}/{current_lang}/{page_path}"
    lines.append(f'    <link rel="canonical" href="{canonical_url}">')
    
    # hreflang tags for each language
    for lang in languages:
        code = lang.get("code", lang) if isinstance(lang, dict) else lang
        lang_url = f"{base_url}/{code}/{page_path}"
        lines.append(f'    <link rel="alternate" hreflang="{code}" href="{lang_url}">')
    
    # x-default points to the default language version
    default_url = f"{base_url}/{default_lang}/{page_path}"
    lines.append(f'    <link rel="alternate" hreflang="x-default" href="{default_url}">')
    
    return "\n".join(lines)


def inject_tags_into_html(html_content: str, seo_tags: str) -> str:
    """Inject SEO tags into HTML content after the opening <head> tag."""
    # Check if tags already exist (avoid duplicate injection)
    if 'rel="canonical"' in html_content:
        return html_content
    
    # Find the <head> tag and insert after it
    # Match <head> or <head ...>
    head_pattern = re.compile(r'(<head[^>]*>)', re.IGNORECASE)
    match = head_pattern.search(html_content)
    
    if match:
        insert_pos = match.end()
        return html_content[:insert_pos] + "\n" + seo_tags + html_content[insert_pos:]
    
    # Fallback: if no <head> found, return unchanged
    print("Warning: No <head> tag found")
    return html_content


def process_html_file(
    html_file: Path,
    site_dir: Path,
    lang: str,
    languages: list[dict],
    base_url: str,
    default_lang: str,
    dry_run: bool = False
) -> bool:
    """Process a single HTML file, injecting SEO tags.
    
    Returns True if file was modified, False otherwise.
    """
    try:
        page_path = get_page_path(html_file, site_dir, lang)
        seo_tags = generate_seo_tags(page_path, lang, languages, base_url, default_lang)
        
        with open(html_file, encoding="utf-8") as f:
            content = f.read()
        
        # Skip if already has canonical (avoid duplicate processing)
        if 'rel="canonical"' in content:
            return False
        
        # Skip HTML fragments without <head> tag (e.g., partial templates)
        if '<head' not in content.lower():
            return False
        
        new_content = inject_tags_into_html(content, seo_tags)
        
        if dry_run:
            print(f"  Would inject into: {html_file.relative_to(site_dir)}")
            return True
        
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(new_content)
        
        return True
    
    except Exception as e:
        print(f"Error processing {html_file}: {e}")
        return False


def process_language_folder(
    site_dir: Path,
    lang: str,
    languages: list[dict],
    base_url: str,
    default_lang: str,
    dry_run: bool = False
) -> int:
    """Process all HTML files in a language folder.
    
    Returns count of files modified.
    """
    lang_dir = site_dir / lang
    
    if not lang_dir.exists():
        print(f"Warning: Language folder {lang_dir} does not exist")
        return 0
    
    modified_count = 0
    
    for html_file in lang_dir.rglob("*.html"):
        # Skip toc.html files - they're navigation fragments, not full pages
        if html_file.name == "toc.html":
            continue
        if process_html_file(html_file, site_dir, lang, languages, base_url, default_lang, dry_run):
            modified_count += 1
    
    return modified_count


def main():
    parser = argparse.ArgumentParser(
        description="Inject SEO tags (hreflang, canonical) into HTML files"
    )
    parser.add_argument(
        "--site-dir", "-s",
        default="_site",
        help="Site output directory (default: _site)"
    )
    parser.add_argument(
        "--base-url", "-b",
        default=DEFAULT_BASE_URL,
        help=f"Base URL for the site (default: {DEFAULT_BASE_URL})"
    )
    parser.add_argument(
        "--default-lang", "-d",
        default=DEFAULT_LANGUAGE,
        help=f"Default language for x-default (default: {DEFAULT_LANGUAGE})"
    )
    parser.add_argument(
        "--lang", "-l",
        help="Process only this language (default: all)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files"
    )
    
    args = parser.parse_args()
    
    site_dir = Path(args.site_dir)
    
    if not site_dir.exists():
        print(f"Error: Site directory {site_dir} does not exist")
        return 1
    
    # Load languages
    languages = load_languages(site_dir)
    lang_codes = [l.get("code", l) if isinstance(l, dict) else l for l in languages]
    
    print(f"Base URL: {args.base_url}")
    print(f"Languages: {', '.join(lang_codes)}")
    print(f"Default: {args.default_lang}")
    
    if args.dry_run:
        print("\n--- DRY RUN MODE ---\n")
    
    total_modified = 0
    
    # Process specified language or all languages
    langs_to_process = [args.lang] if args.lang else lang_codes
    
    for lang in langs_to_process:
        print(f"\nProcessing {lang}/...")
        count = process_language_folder(
            site_dir,
            lang,
            languages,
            args.base_url,
            args.default_lang,
            args.dry_run
        )
        print(f"  Modified: {count} files")
        total_modified += count
    
    print(f"\nTotal: {total_modified} files {'would be ' if args.dry_run else ''}modified")
    return 0


if __name__ == "__main__":
    exit(main())
