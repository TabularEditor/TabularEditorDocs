#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prepare localized content by copying English fallback files for missing translations.

Usage: python prepare-localized-content.py <language_code>
Example: python prepare-localized-content.py es
"""

import os
import shutil
import sys


# Content directories that should be localized
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

# Shared directories that should be copied (not translated, just needed for relative paths)
SHARED_DIRS = [
    "assets",
    "whats-new",
    "api",
]

# Root-level files that should be localized
ROOT_FILES = [
    "index.md",
    "toc.yml",
    "404.html",
]


def copy_missing_files(src_dir: str, dest_dir: str) -> int:
    """
    Copy files from src_dir to dest_dir if they don't already exist in dest_dir.
    Returns the number of files copied.
    """
    copied_count = 0
    
    if not os.path.exists(src_dir):
        print(f"  Warning: Source directory '{src_dir}' does not exist, skipping.")
        return 0
    
    os.makedirs(dest_dir, exist_ok=True)
    
    for root, dirs, files in os.walk(src_dir):
        # Calculate relative path from source directory
        rel_path = os.path.relpath(root, src_dir)
        target_root = os.path.join(dest_dir, rel_path) if rel_path != "." else dest_dir
        
        # Create subdirectories as needed
        os.makedirs(target_root, exist_ok=True)
        
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(target_root, file)
            
            # Only copy if destination doesn't exist (preserve translations)
            if not os.path.exists(dest_file):
                shutil.copy2(src_file, dest_file)
                copied_count += 1
                print(f"  Copied: {os.path.relpath(dest_file, dest_dir)}")
    
    return copied_count


def main(args: list[str]) -> int:
    if len(args) < 2:
        print("Usage: python prepare-localized-content.py <language_code>")
        print("Example: python prepare-localized-content.py es")
        return 1
    
    lang_code = args[1]
    content_dir = "content"
    # Structure: localizedContent/{lang}/content/
    # This allows docfx.json in localizedContent/{lang}/ to resolve ~/content/... paths
    localized_base = os.path.join("localizedContent", lang_code)
    localized_dir = os.path.join(localized_base, "content")
    
    if not os.path.exists(localized_dir):
        print(f"Creating localized content directory: {localized_dir}")
        os.makedirs(localized_dir, exist_ok=True)
    
    print(f"Preparing '{lang_code}' localized content with English fallbacks...")
    print(f"Source: {content_dir}")
    print(f"Destination: {localized_dir}")
    print()
    
    total_copied = 0
    
    # Copy content directories
    for dir_name in CONTENT_DIRS:
        src = os.path.join(content_dir, dir_name)
        dest = os.path.join(localized_dir, dir_name)
        print(f"Processing {dir_name}/...")
        copied = copy_missing_files(src, dest)
        total_copied += copied
        if copied == 0:
            print("  All files already present (translations or previous fallback)")
    
    # Copy shared directories (assets, whats-new, api) - always overwrite to stay in sync
    for dir_name in SHARED_DIRS:
        src = os.path.join(content_dir, dir_name)
        dest = os.path.join(localized_dir, dir_name)
        if os.path.exists(src):
            print(f"Copying shared {dir_name}/...")
            if os.path.exists(dest):
                shutil.rmtree(dest)
            shutil.copytree(src, dest)
            print(f"  Copied {dir_name}/ (shared resources)")

    # Copy root-level files to content/ directory
    print("Processing root files...")
    for file_name in ROOT_FILES:
        src_file = os.path.join(content_dir, file_name)
        dest_file = os.path.join(localized_dir, file_name)
        
        if os.path.exists(src_file) and not os.path.exists(dest_file):
            shutil.copy2(src_file, dest_file)
            total_copied += 1
            print(f"  Copied: {file_name}")
    
    print()
    print(f"Done! Copied {total_copied} fallback files for '{lang_code}'.")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
