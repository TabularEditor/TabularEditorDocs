#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unified documentation build script for multi-language support.

Usage:
    python build-docs.py              # Build all languages (default)
    python build-docs.py --all        # Build all languages
    python build-docs.py --lang en    # Build English only
    python build-docs.py --lang es zh # Build specific languages
    python build-docs.py --list       # List available languages
    python build-docs.py --serve      # Build English and serve locally

Options:
    --all           Build all available languages
    --lang LANGS    Build specific language(s) (space-separated)
    --list          List available languages and exit
    --serve         Build and serve locally (English only, for development)
    --skip-gen      Skip running gen_redirects.py (use existing configs)
    --no-api-copy   Skip copying API docs to localized sites
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str, check: bool = True) -> int:
    """Run a command and return exit code."""
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"{'='*60}")
    print(f"Running: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, shell=(os.name == 'nt'))
    
    if check and result.returncode != 0:
        print(f"Error: Command failed with exit code {result.returncode}")
        return result.returncode
    
    return result.returncode


def get_available_languages() -> list[str]:
    """Get list of available languages from docfxTranslations/languages.json or scan localizedContent/."""
    manifest_path = Path("docfxTranslations/languages.json")
    
    if manifest_path.exists():
        with open(manifest_path) as f:
            data = json.load(f)
            return data.get("languages", [])
    
    # Fallback: scan localizedContent/ directly
    localized_dir = Path("localizedContent")
    if not localized_dir.exists():
        return []
    
    return sorted([
        d.name for d in localized_dir.iterdir()
        if d.is_dir() and len(d.name) <= 5
    ])


def prepare_localized_content(lang: str) -> int:
    """Run prepare-localized-content.py for a language."""
    return run_command(
        [sys.executable, "prepare-localized-content.py", lang],
        f"Preparing {lang} content (English fallback)"
    )


def build_english() -> int:
    """Build English documentation."""
    return run_command(
        ["docfx", "docfx.json", "--warningsAsErrors"],
        "Building English documentation"
    )


def build_language(lang: str) -> int:
    """Build documentation for a specific language."""
    config_path = f"localizedContent/{lang}/docfx.json"
    
    if not os.path.exists(config_path):
        print(f"Error: Config file not found: {config_path}")
        print("Run 'python gen_redirects.py' first to generate configs.")
        return 1
    
    # Prepare localized content (copy English fallbacks)
    result = prepare_localized_content(lang)
    if result != 0:
        return result
    
    # Build the documentation
    return run_command(
        ["docfx", config_path],
        f"Building {lang} documentation"
    )


def copy_api_docs(languages: list[str]) -> int:
    """Copy API docs from English to localized sites."""
    en_api = Path("_site/en/api")
    
    if not en_api.exists():
        print("Warning: English API docs not found, skipping API copy")
        return 0
    
    print(f"\n{'='*60}")
    print("  Copying API docs to localized sites")
    print(f"{'='*60}")
    
    for lang in languages:
        dest = Path(f"_site/{lang}/api")
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(en_api, dest)
        print(f"  Copied API docs to _site/{lang}/api")
    
    return 0


def fix_xref_in_api() -> int:
    """Fix shared xref links in API HTML files."""
    api_dir = Path("_site/en/api")
    
    if not api_dir.exists():
        return 0
    
    print(f"\n{'='*60}")
    print("  Fixing xref links in API docs")
    print(f"{'='*60}")
    
    count = 0
    for html_file in api_dir.rglob("*.html"):
        content = html_file.read_text(encoding="utf-8")
        if '<a class="xref" href="TabularEditor.Shared.html">Shared</a>' in content:
            content = content.replace(
                '<a class="xref" href="TabularEditor.Shared.html">Shared</a>',
                'Shared'
            )
            html_file.write_text(content, encoding="utf-8")
            count += 1
    
    print(f"  Fixed {count} file(s)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build documentation for one or more languages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("--all", action="store_true", help="Build all languages")
    parser.add_argument("--lang", nargs="+", help="Build specific language(s)")
    parser.add_argument("--list", action="store_true", help="List available languages")
    parser.add_argument("--serve", action="store_true", help="Build English and serve locally")
    parser.add_argument("--skip-gen", action="store_true", help="Skip gen_redirects.py")
    parser.add_argument("--no-api-copy", action="store_true", help="Skip copying API docs")
    
    args = parser.parse_args()
    
    # List available languages
    if args.list:
        langs = get_available_languages()
        print("Available languages:")
        print("  en (English) - default")
        for lang in langs:
            print(f"  {lang}")
        return 0
    
    # Run gen_redirects.py first (unless skipped)
    if not args.skip_gen:
        result = run_command(
            [sys.executable, "gen_redirects.py"],
            "Generating docfx configurations"
        )
        if result != 0:
            return result
    
    # Determine which languages to build
    available_langs = get_available_languages()
    
    if args.serve:
        # Build English only and serve
        result = build_english()
        if result != 0:
            return result
        
        fix_xref_in_api()
        
        return run_command(
            ["docfx", "serve", "_site/en"],
            "Serving documentation locally"
        )
    
    if args.lang:
        # Build specific languages
        build_en = "en" in args.lang
        build_langs = [l for l in args.lang if l != "en"]
        
        # Validate languages
        for lang in build_langs:
            if lang not in available_langs:
                print(f"Error: Language '{lang}' not found in localizedContent/")
                print(f"Available: {', '.join(available_langs)}")
                return 1
    elif args.all or not args.lang:
        # Build all languages (default behavior)
        build_en = True
        build_langs = available_langs
    else:
        build_en = True
        build_langs = []
    
    # Build English first (needed for API docs)
    if build_en:
        result = build_english()
        if result != 0:
            return result
        
        fix_xref_in_api()
    
    # Build localized languages
    for lang in build_langs:
        result = build_language(lang)
        if result != 0:
            return result
    
    # Copy API docs to localized sites
    if build_langs and not args.no_api_copy:
        copy_api_docs(build_langs)
    
    print(f"\n{'='*60}")
    print("  Build complete!")
    print(f"{'='*60}")
    print(f"Output: _site/")
    if build_en:
        print(f"  - en/ (English)")
    for lang in build_langs:
        print(f"  - {lang}/")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nBuild interrupted.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
