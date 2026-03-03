#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate staticwebapp.config.json for Azure Static Web Apps.

This script creates server-side redirects for:
1. Root URLs (/, /index.html) → /en/ (301)
2. Release notes aliases → /en/references/release-notes/{latest}.html (302, auto-detected)
3. Legacy shortcut URLs (/tmdl, /roslyn, etc.) → /en/... (301)

Note: Legacy directory wildcards (/features/*, etc.) are NOT handled here.
They fall through to 404.html which performs client-side meta-refresh redirects.

Usage:
    python gen_staticwebapp_config.py                    # Generate config
    python gen_staticwebapp_config.py --dry-run          # Preview without writing
    python gen_staticwebapp_config.py --output custom/   # Custom output path
"""

import argparse
import json
import re
from pathlib import Path
from typing import Any

from config_loader import get_legacy_shortcuts, get_default_language


# Load from centralized config
LEGACY_SHORTCUTS = get_legacy_shortcuts()
DEFAULT_LANGUAGE = get_default_language()


def find_latest_release_notes(site_dir: str = "_site", default_lang: str = "en") -> str | None:
    """Find the filename of the latest versioned release notes in the built site.

    Scans {site_dir}/{default_lang}/references/release-notes/ for files matching
    the pattern {major}_{minor}_{patch}.html, sorts them by semantic version,
    and returns the filename of the newest one (e.g. '3_25_5.html').
    Returns None if the directory doesn't exist or contains no versioned files.
    """
    release_notes_dir = Path(site_dir) / default_lang / "references" / "release-notes"

    if not release_notes_dir.exists():
        return None

    version_pattern = re.compile(r"^(\d+)_(\d+)_(\d+)\.html$")
    versioned: list[tuple[tuple[int, int, int], str]] = []

    for html_file in release_notes_dir.glob("*.html"):
        m = version_pattern.match(html_file.name)
        if m:
            version = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
            versioned.append((version, html_file.name))

    if not versioned:
        return None

    versioned.sort(key=lambda x: x[0], reverse=True)
    return versioned[0][1]


def generate_config(languages: list[str], default_lang: str | None = None, site_dir: str = "_site") -> dict[str, Any]:
    """Generate the staticwebapp.config.json content."""
    if default_lang is None:
        default_lang = DEFAULT_LANGUAGE
    routes: list[dict[str, Any]] = []

    # Resolve the latest release notes file, fall back to release-history.html
    latest_rn = find_latest_release_notes(site_dir, default_lang)
    if latest_rn:
        rn_rel_path = f"references/release-notes/{latest_rn}"
    else:
        rn_rel_path = "references/release-history.html"

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
            "redirect": f"/{lang}/{rn_rel_path}",
            "statusCode": 302
        })
        routes.append({
            "route": f"/{lang}/te3/other/release-notes",
            "redirect": f"/{lang}/{rn_rel_path}",
            "statusCode": 302
        })
    # Also handle non-prefixed paths
    routes.append({
        "route": "/references/release-notes",
        "redirect": f"/{default_lang}/{rn_rel_path}",
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
    config = generate_config(languages, args.default_lang, args.output)

    latest_rn = find_latest_release_notes(args.output, args.default_lang)
    rn_target = f"references/release-notes/{latest_rn}" if latest_rn else "references/release-history.html (fallback)"
    release_notes_count = len(languages) * 2 + 1
    print(f"\nGenerated {len(config['routes'])} routes:")
    print(f"  - Root redirects: 2")
    print(f"  - Release notes: {release_notes_count} → {rn_target}")
    print(f"  - Legacy shortcuts: {len(LEGACY_SHORTCUTS)}")
    
    if args.dry_run:
        print("\n--- DRY RUN: Config preview ---")
        print(json.dumps(config, indent=2))
        return 0
    
    # Write config
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "staticwebapp.config.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(config, f, separators=(",", ":"))
    
    print(f"\nGenerated: {output_file}")
    return 0


if __name__ == "__main__":
    exit(main())
