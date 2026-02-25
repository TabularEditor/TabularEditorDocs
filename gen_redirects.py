#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate docfx configuration files and redirects.

This script:
1. Generates localizedContent/en/docfx.json for English with redirects
2. Scans localizedContent/ for language folders
3. Generates localizedContent/{lang}/docfx.json for each language
4. Creates docfxTranslations/languages.json manifest

Usage: python gen_redirects.py
"""

import copy
import json
import os
import posixpath
import shutil
import sys
import traceback
from typing import Any

# Content directories that need path replacement for localized builds
CONTENT_DIRS = [
    "features",
    "getting-started",
    "how-tos",
    "references",
    "kb",
    "security",
    "troubleshooting",
    "tutorials",
]

# Shared directories (assets, whats-new, api)
SHARED_DIRS = ["assets", "whats-new", "api"]


def get_available_languages() -> list[str]:
    """Scan localizedContent/ folder and return list of language codes (excluding 'en')."""
    localized_dir = "localizedContent"
    if not os.path.exists(localized_dir):
        return []
    
    languages = []
    for item in os.listdir(localized_dir):
        item_path = os.path.join(localized_dir, item)
        # Exclude 'en' since it's generated, not stored
        if os.path.isdir(item_path) and len(item) <= 5 and item != "en":
            languages.append(item)
    
    return sorted(languages)


def generate_localized_config(template: dict, lang: str) -> dict:
    """Generate a docfx config for a specific language based on the template.
    
    Note: Config files are placed in localizedContent/{lang}/docfx.json alongside
    a content/ subdirectory. This allows ~/content/... paths in markdown to resolve
    correctly (~ = config location = localizedContent/{lang}/).
    
    Structure:
        localizedContent/{lang}/
            docfx.json          <- generated config
            content/
                features/       <- localized/fallback content
                assets/images/  <- shared resources
                ...
    """
    config = copy.deepcopy(template)
    
    # Remove metadata section (API generation) - localized sites use copied API docs
    if "metadata" in config:
        del config["metadata"]
    
    build = config["build"]
    
    # Since docfx.json is in localizedContent/{lang}/ and content is in 
    # localizedContent/{lang}/content/, paths stay the same as the English template
    # No path modifications needed for content entries!
    
    # Resource paths: keep local content/ paths, but for any fallback to main
    # content folder, we'd use ../../content/ (but we copy everything locally now)
    
    # Set output destination to language subfolder (relative to project root)
    # From localizedContent/{lang}/, we go up twice to reach project root
    build["dest"] = f"../../_site/{lang}"
    
    # Update template paths - need to go up two levels to reach project root
    if "template" in build:
        new_templates = []
        for t in build["template"]:
            if t == "default":
                new_templates.append(t)
            else:
                # templates/tabulareditor -> ../../templates/tabulareditor
                new_templates.append(f"../../{t}")
        build["template"] = new_templates
    
    return config


def generate_redirects_config(template: dict, redirects_data: dict[str, str], en_content_dir: str) -> dict:
    """Generate English docfx.json with redirects added.
    
    Args:
        template: Base docfx config template
        redirects_data: Dict of redirect paths to target URLs
        en_content_dir: Directory for English content (localizedContent/en/content/)
    """
    config = copy.deepcopy(template)
    
    # Fix metadata paths (API generation) - need to go up two levels to reach project root
    # DocFX doesn't support ../ in file globs, so we use src to set the base directory
    if "metadata" in config:
        for meta in config["metadata"]:
            # Fix src paths - move ../ to src, keep files as relative globs
            if "src" in meta:
                new_src = []
                for src in meta["src"]:
                    if "files" in src:
                        # Transform files like "content/_apiSource/*.dll" to use src
                        new_files = []
                        for f in src["files"]:
                            # Extract directory and file pattern
                            # e.g., "content/_apiSource/*.dll" -> src="../..", files="content/_apiSource/*.dll"
                            new_files.append(f)
                        new_src.append({
                            "src": "../..",
                            "files": new_files
                        })
                    else:
                        new_src.append(src)
                meta["src"] = new_src
            # Fix dest path
            if "dest" in meta:
                meta["dest"] = f"../../{meta['dest']}"
            # Fix filter path
            if "filter" in meta:
                meta["filter"] = f"../../{meta['filter']}"
    
    dirs = dict[str, list[str]]()
    
    for key, value in redirects_data.items():
        # Redirect paths are relative to content/, convert to en_content_dir
        # e.g., content/old-page.md -> localizedContent/en/content/old-page.md
        dest_path = key.replace("content/", f"{en_content_dir}/", 1)
        dir_path = posixpath.dirname(dest_path)
        ext = posixpath.splitext(key)[1]
        
        if dir_path in dirs:
            dirs[dir_path].append(dest_path)
        else:
            dirs[dir_path] = [dest_path]
        
        os.makedirs(dir_path, exist_ok=True)
        
        if ext == ".md":
            content_list: list[Any] = config["build"]["content"]
            content_list.append({"files": posixpath.relpath(key, "content"), "src": "content"})
            with open(dest_path, mode="w", encoding="utf-8") as f:
                f.write(f"""---
redirect_url: {value}
---
""")
        elif ext == ".html":
            resource: list[Any] = config["build"]["resource"]
            resource.append({"files": posixpath.relpath(key, "content"), "src": "content"})
            with open(dest_path, mode="w", encoding="utf-8") as f:
                f.write(f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="0;URL='{value}'">
    <link rel="canonical" href="{value}">
  </head>
</html>
""")
        else:
            print("Unknown file type:", key, file=sys.stderr)
    
    # Set English output destination (relative to localizedContent/en/)
    config["build"]["dest"] = "../../_site/en"
    
    # Update template paths - need to go up two levels to reach project root
    if "template" in config["build"]:
        new_templates = []
        for t in config["build"]["template"]:
            if t == "default":
                new_templates.append(t)
            else:
                new_templates.append(f"../../{t}")
        config["build"]["template"] = new_templates
    
    return config


def main(args: list[str]) -> int:
    config_input_path = "docfx-template.json"
    redirects_path = "redirects.json"
    translations_dir = "docfxTranslations"
    localized_content_dir = "localizedContent"
    
    # Load template
    with open(config_input_path) as f:
        template = json.load(f)
    
    # Load redirects
    with open(redirects_path) as f:
        redirects_data: dict[str, str] = json.load(f)
    
    # Create English directory
    en_dir = os.path.join(localized_content_dir, "en")
    en_content_dir = os.path.join(en_dir, "content")
    os.makedirs(en_content_dir, exist_ok=True)
    
    # Generate English config with redirects in localizedContent/en/
    en_config_path = os.path.join(en_dir, "docfx.json")
    print(f"Generating {en_config_path} (English)...")
    english_config = generate_redirects_config(template, redirects_data, en_content_dir)
    with open(en_config_path, "w") as f:
        json.dump(english_config, f, indent=4)
    
    # Get available languages from localizedContent/ (excludes 'en')
    languages = get_available_languages()
    all_languages = ["en"] + languages
    print(f"Found {len(all_languages)} language(s): {', '.join(all_languages)}")
    
    # Create docfxTranslations directory for manifest
    os.makedirs(translations_dir, exist_ok=True)
    
    # Generate config for each non-English language
    for lang in languages:
        lang_dir = os.path.join(localized_content_dir, lang)
        os.makedirs(lang_dir, exist_ok=True)
        
        config_path = os.path.join(lang_dir, "docfx.json")
        print(f"Generating {config_path}...")
        
        localized_config = generate_localized_config(template, lang)
        with open(config_path, "w") as f:
            json.dump(localized_config, f, indent=4)
    
    # Generate languages.json manifest (includes 'en')
    manifest = {
        "languages": all_languages,
        "default": "en",
        "generated": True
    }
    manifest_path = os.path.join(translations_dir, "languages.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=4)
    print(f"Generated {manifest_path}")
    
    print("Done!")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as ex:
        traceback.print_exception(ex, file=sys.stderr)
        sys.exit(1)
