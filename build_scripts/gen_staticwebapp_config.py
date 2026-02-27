#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate staticwebapp.config.json for Azure Static Web Apps.

This script creates server-side 301 redirects for:
1. Root URLs (/, /index.html) → /en/
2. Legacy shortcut URLs (/tmdl, /roslyn, etc.) → /en/...
3. Migration wildcards (/features/* → /en/features/*)

Usage:
    python gen_staticwebapp_config.py                    # Generate config
    python gen_staticwebapp_config.py --dry-run          # Preview without writing
    python gen_staticwebapp_config.py --output custom/   # Custom output path
"""

import argparse
import json
import os
from pathlib import Path
from typing import Any

from config_loader import get_redirect_directories, get_legacy_shortcuts, get_default_language


# Load from centralized config
CONTENT_DIRECTORIES = get_redirect_directories()
LEGACY_SHORTCUTS = get_legacy_shortcuts()
DEFAULT_LANGUAGE = get_default_language()


def generate_config(languages: list[str], default_lang: str | None = None) -> dict[str, Any]:
    """Generate the staticwebapp.config.json content."""
    if default_lang is None:
        default_lang = DEFAULT_LANGUAGE
    routes: list[dict[str, Any]] = []
    
    # 1. Root redirects (301 for SEO)
    routes.append({
        "route": "/",
        "redirect": f"/{default_lang}/",
        "statusCode": 301
    })
    routes.append({
        "route": "/index.html", 
        "redirect": f"/{default_lang}/",
        "statusCode": 301
    })
    
    # 2. Release notes special handling (302 - dynamic target)
    # These point to the latest release notes which changes over time
    # Generate explicit routes per language since Azure SWA doesn't support segment capture
    for lang in languages:
        routes.append({
            "route": f"/{lang}/references/release-notes",
            "redirect": f"/{lang}/references/release-history.html",
            "statusCode": 302
        })
        routes.append({
            "route": f"/{lang}/te3/other/release-notes",
            "redirect": f"/{lang}/references/release-history.html",
            "statusCode": 302
        })
    # Also handle non-prefixed paths
    routes.append({
        "route": "/references/release-notes",
        "redirect": f"/{default_lang}/references/release-history.html",
        "statusCode": 302
    })
    
    # 3. Legacy shortcut redirects (301)
    for old_path, new_path in sorted(LEGACY_SHORTCUTS.items()):
        routes.append({
            "route": old_path,
            "redirect": new_path,
            "statusCode": 301
        })
    
    # 4. Directory wildcard migration (fallback to 404.html)
    # Note: Azure SWA doesn't support wildcard capture in redirect targets.
    # Non-prefixed URLs like /features/x.html will fall through to 404.html,
    # which uses redirects.json to perform meta-refresh redirects.
    # This is SEO-acceptable as a 302 + client redirect for legacy URLs.
    #
    # For high-traffic legacy pages, add explicit routes to legacyShortcuts
    # in build-config.json for proper 301 server-side redirects.
    
    # Build final config
    # Note: 404.html is copied to site root during build for language-aware fallback
    config = {
        "routes": routes,
        "responseOverrides": {
            "404": {
                "rewrite": "/404.html"
            }
        }
    }
    
    return config


def load_languages() -> list[str]:
    """Load supported languages from languages.json manifest."""
    manifest_paths = [
        Path("metadata/languages.json"),
        Path("_site/languages.json"),
    ]
    
    for path in manifest_paths:
        if path.exists():
            with open(path) as f:
                data = json.load(f)
                languages = data.get("languages", [])
                # Handle both simple array and rich metadata formats
                if languages and isinstance(languages[0], dict):
                    return [lang["code"] for lang in languages]
                return languages
    
    # Fallback
    print("Warning: languages.json not found, using default [en]")
    return ["en"]


def main():
    parser = argparse.ArgumentParser(
        description="Generate staticwebapp.config.json for Azure Static Web Apps"
    )
    parser.add_argument(
        "--output", "-o",
        default="_site",
        help="Output directory (default: _site)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print config without writing to file"
    )
    parser.add_argument(
        "--default-lang", "-d",
        default=DEFAULT_LANGUAGE,
        help=f"Default language for fallback (default: {DEFAULT_LANGUAGE})"
    )
    
    args = parser.parse_args()
    
    # Load languages
    languages = load_languages()
    print(f"Languages: {', '.join(languages)}")
    print(f"Default: {args.default_lang}")
    
    # Generate config
    config = generate_config(languages, args.default_lang)
    
    print(f"\nGenerated {len(config['routes'])} routes:")
    print(f"  - Root redirects: 2")
    print(f"  - Release notes: 4")
    print(f"  - Legacy shortcuts: {len(LEGACY_SHORTCUTS)}")
    print(f"  - Directory wildcards: {len(CONTENT_DIRECTORIES)}")
    
    if args.dry_run:
        print("\n--- DRY RUN: Config preview ---")
        print(json.dumps(config, indent=2))
        return 0
    
    # Write config
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "staticwebapp.config.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    
    print(f"\nGenerated: {output_file}")
    return 0


if __name__ == "__main__":
    exit(main())
