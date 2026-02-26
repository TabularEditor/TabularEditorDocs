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


# Content directories that need wildcard migration redirects
CONTENT_DIRECTORIES = [
    "features",
    "getting-started", 
    "how-tos",
    "references",
    "tutorials",
    "api",
    "kb",
    "security",
    "troubleshooting",
    "images",
    "whats-new",
]

# Legacy shortcut redirects (manually maintained)
# These are short URLs that redirect to full paths
LEGACY_SHORTCUTS = {
    "/tmdl": "/en/features/tmdl.html",
    "/roslyn": "/en/how-tos/Advanced-Scripting.html#compiling-with-roslyn",
    "/eula": "/en/security/te3-eula.html",
    "/tmuo": "/en/references/user-options.html",
    "/workspace": "/en/tutorials/workspace-mode.html",
    "/privacy-policy.html": "/en/security/privacy-policy.html",
    "/user-options.html": "/en/references/user-options.html",
    "/Advanced-Scripting.html": "/en/how-tos/Advanced-Scripting.html",
    "/Best-Practice-Analyzer.html": "/en/features/Best-Practice-Analyzer.html",
    "/Importing-Tables.html": "/en/how-tos/Importing-Tables.html",
    "/Workspace-Database.html": "/en/tutorials/workspace-mode.html",
    "/Useful-script-snippets.html": "/en/features/Useful-script-snippets.html",
    "/Command-line-Options.html": "/en/features/Command-line-Options.html",
    "/Power-BI-Desktop-Integration.html": "/en/getting-started/Power-BI-Desktop-Integration.html",
    "/Custom-Actions.html": "/en/tutorials/creating-macros.html",
    "/FormatDax.html": "/en/references/FormatDax.html",
    "/common/Datasets/direct-lake-dataset.html": "/en/features/Semantic-Model/direct-lake-sql-model.html",
    "/other/downloads.html": "/en/references/downloads.html",
    "/te3/downloads.html": "/en/references/downloads.html",
    "/te3/logo.svg": "/en/logo.svg",
    # Old ReadTheDocs-style paths
    "/projects/te3/en/latest": "/en/",
    "/projects/te3": "/en/",
    "/projects/te3/en/latest/editions.html": "/en/getting-started/editions.html",
    "/projects/te3/en/latest/security-privacy.html": "/en/security/security-privacy.html",
    "/projects/te3/en/latest/downloads.html": "/en/references/downloads.html",
    "/projects/te3/en/latest/getting-started.html": "/en/getting-started/getting-started.html",
}


def generate_config(languages: list[str], default_lang: str = "en") -> dict[str, Any]:
    """Generate the staticwebapp.config.json content."""
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
    routes.append({
        "route": "/*/references/release-notes",
        "redirect": "/:1/references/release-history.html",
        "statusCode": 302
    })
    routes.append({
        "route": "/references/release-notes",
        "redirect": f"/{default_lang}/references/release-history.html",
        "statusCode": 302
    })
    routes.append({
        "route": "/*/te3/other/release-notes",
        "redirect": "/:1/references/release-history.html",
        "statusCode": 302
    })
    routes.append({
        "route": "/te3/other/release-notes",
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
    
    # 4. Directory wildcard migration redirects (301)
    # These redirect old non-language-prefixed URLs to /en/
    for directory in CONTENT_DIRECTORIES:
        routes.append({
            "route": f"/{directory}/*",
            "redirect": f"/{default_lang}/{directory}/:splat",
            "statusCode": 301
        })
    
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
        Path("docfxTranslations/languages.json"),
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
        default="en",
        help="Default language for fallback (default: en)"
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
