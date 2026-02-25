#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate docfx configuration files and redirects.

This script:
1. Generates docfx.json for English with redirects
2. Scans localizedContent/ for language folders
3. Generates docfxTranslations/docfx-{lang}.json for each language
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
    """Scan localizedContent/ folder and return list of language codes."""
    localized_dir = "localizedContent"
    if not os.path.exists(localized_dir):
        return []
    
    languages = []
    for item in os.listdir(localized_dir):
        item_path = os.path.join(localized_dir, item)
        if os.path.isdir(item_path) and len(item) <= 5:  # Language codes are short (e.g., es, zh, pt-br)
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


def generate_redirects_config(template: dict, redirects_data: dict[str, str]) -> dict:
    """Generate English docfx.json with redirects added."""
    config = copy.deepcopy(template)
    
    dirs = dict[str, list[str]]()
    
    for key, value in redirects_data.items():
        dir_path = posixpath.dirname(key)
        ext = posixpath.splitext(key)[1]
        
        if dir_path in dirs:
            dirs[dir_path].append(key)
        else:
            dirs[dir_path] = [key]
        
        os.makedirs(dir_path, exist_ok=True)
        
        if ext == ".md":
            content: list[Any] = config["build"]["content"]
            content.append({"files": posixpath.relpath(key, "content"), "src": "content"})
            with open(key, mode="w", encoding="utf-8") as f:
                f.write(f"""---
redirect_url: {value}
---
""")
        elif ext == ".html":
            resource: list[Any] = config["build"]["resource"]
            resource.append({"files": posixpath.relpath(key, "content"), "src": "content"})
            with open(key, mode="w", encoding="utf-8") as f:
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
    
    # Update .gitignore files for redirect files
    for dir_path, files in dirs.items():
        gitignore_path = posixpath.join(dir_path, ".gitignore")
        with open(gitignore_path, "a") as f:
            f.write("\n")
            f.writelines("/" + posixpath.basename(file) + "\n" for file in files)
            f.write("/.gitignore\n")
    
    # Set English output destination
    config["build"]["dest"] = "_site/en"
    
    return config


def main(args: list[str]) -> int:
    config_input_path = "docfx-template.json"
    config_output_path = "docfx.json"
    redirects_path = "redirects.json"
    translations_dir = "docfxTranslations"
    localized_content_dir = "localizedContent"
    
    # Load template
    with open(config_input_path) as f:
        template = json.load(f)
    
    # Load redirects
    with open(redirects_path) as f:
        redirects_data: dict[str, str] = json.load(f)
    
    # Generate English config with redirects
    print("Generating docfx.json (English)...")
    english_config = generate_redirects_config(template, redirects_data)
    with open(config_output_path, "w") as f:
        json.dump(english_config, f, indent=4)
    
    # Get available languages from localizedContent/
    languages = get_available_languages()
    print(f"Found {len(languages)} language(s) in localizedContent/: {', '.join(languages) if languages else 'none'}")
    
    if languages:
        # Create docfxTranslations directory for manifest (keeps backward compat)
        os.makedirs(translations_dir, exist_ok=True)
        
        # Generate config for each language - placed inside localizedContent/{lang}/
        for lang in languages:
            lang_dir = os.path.join(localized_content_dir, lang)
            os.makedirs(lang_dir, exist_ok=True)
            
            config_path = os.path.join(lang_dir, "docfx.json")
            print(f"Generating {config_path}...")
            
            localized_config = generate_localized_config(template, lang)
            with open(config_path, "w") as f:
                json.dump(localized_config, f, indent=4)
        
        # Generate languages.json manifest
        manifest = {
            "languages": languages,
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
