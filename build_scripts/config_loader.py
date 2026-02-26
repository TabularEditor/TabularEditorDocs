#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Shared configuration loader for build scripts.

Loads build-config.json, redirects.json, and language-metadata.json from metadata/.
Provides consistent access to directories, files, and settings across all scripts.
"""

import hashlib
import json
from pathlib import Path
from typing import Any


# Default paths (relative to project root)
BUILD_CONFIG_PATH = "metadata/build-config.json"
REDIRECTS_CONFIG_PATH = "metadata/redirects.json"
LANGUAGE_METADATA_PATH = "metadata/language-metadata.json"

# Cached configs
_build_config: dict | None = None
_redirects_config: dict | None = None


def load_build_config(config_path: Path | str | None = None) -> dict[str, Any]:
    """Load the build configuration from JSON file.
    
    Returns the full config dict with the following keys:
    - contentDirectories: directories with translatable content
    - sharedDirectories: assets/api that aren't translated
    - rootFiles: root-level files (index.md, toc.yml, etc.)
    - redirectDirectories: directories needing wildcard redirects
    """
    global _build_config
    
    if _build_config is not None and config_path is None:
        return _build_config
    
    if config_path is None:
        config_path = Path(BUILD_CONFIG_PATH)
    else:
        config_path = Path(config_path)
    
    if not config_path.exists():
        raise FileNotFoundError(f"Build config not found: {config_path}")
    
    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)
    
    if config_path == Path(BUILD_CONFIG_PATH):
        _build_config = config
    
    return config


def load_redirects_config(config_path: Path | str | None = None) -> dict[str, Any]:
    """Load the redirects configuration from JSON file.
    
    Returns the full config dict with the following keys:
    - serverRedirects: 301 redirects handled by Azure SWA
    - clientRedirects: meta-refresh HTML redirects
    """
    global _redirects_config
    
    if _redirects_config is not None and config_path is None:
        return _redirects_config
    
    if config_path is None:
        config_path = Path(REDIRECTS_CONFIG_PATH)
    else:
        config_path = Path(config_path)
    
    if not config_path.exists():
        raise FileNotFoundError(f"Redirects config not found: {config_path}")
    
    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)
    
    if config_path == Path(REDIRECTS_CONFIG_PATH):
        _redirects_config = config
    
    return config


def get_content_directories(config: dict | None = None) -> list[str]:
    """Get list of content directories that should be localized."""
    if config is None:
        config = load_build_config()
    return config.get("contentDirectories", {}).get("directories", [])


def get_shared_directories(config: dict | None = None) -> list[str]:
    """Get list of shared directories (assets, api) that aren't translated."""
    if config is None:
        config = load_build_config()
    return config.get("sharedDirectories", {}).get("directories", [])


def get_root_files(config: dict | None = None) -> list[str]:
    """Get list of root-level files to copy/localize."""
    if config is None:
        config = load_build_config()
    return config.get("rootFiles", {}).get("files", [])


def get_redirect_directories(config: dict | None = None) -> list[str]:
    """Get list of directories needing wildcard redirects."""
    if config is None:
        config = load_build_config()
    return config.get("redirectDirectories", {}).get("directories", [])


def get_legacy_shortcuts(config: dict | None = None) -> dict[str, str]:
    """Get legacy shortcut redirects (old URL → new URL).
    
    These are server-side 301 redirects for high-priority/vanity URLs.
    Filters out keys starting with '_' which are used for comments.
    """
    if config is None:
        config = load_redirects_config()
    redirects = config.get("serverRedirects", {}).get("redirects", {})
    # Filter out comment keys
    return {k: v for k, v in redirects.items() if not k.startswith("_")}


def get_client_redirects(config: dict | None = None) -> dict[str, str]:
    """Get client-side redirects for legacy content URLs.
    
    These are meta-refresh HTML redirects for content migration.
    Keys are paths like '/te2/Getting-Started.html', values are target paths.
    Filters out keys starting with '_' which are used for comments.
    """
    if config is None:
        config = load_redirects_config()
    redirects = config.get("clientRedirects", {}).get("redirects", {})
    # Filter out comment keys
    return {k: v for k, v in redirects.items() if not k.startswith("_")}


def get_all_redirects(config: dict | None = None) -> dict[str, str]:
    """Get all redirects (both server and client) merged together.
    
    Returns a combined dict of all redirects. Server redirects take precedence
    if there are any duplicates (though there shouldn't be).
    """
    if config is None:
        config = load_redirects_config()
    
    all_redirects = {}
    all_redirects.update(get_client_redirects(config))
    all_redirects.update(get_legacy_shortcuts(config))
    return all_redirects


def get_default_language(config: dict | None = None) -> str:
    """Get the default language code."""
    if config is None:
        config = load_build_config()
    return config.get("defaultLanguage", "en")


def compute_file_hash(file_path: Path | str) -> str:
    """Compute SHA256 hash of a file's contents.
    
    Returns a hex string prefixed with 'sha256:' for clarity.
    Returns empty string if file doesn't exist.
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        return ""
    
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read in chunks for large files
        for chunk in iter(lambda: f.read(8192), b""):
            sha256_hash.update(chunk)
    
    return f"sha256:{sha256_hash.hexdigest()}"


def get_all_content_files(content_dir: Path | str) -> list[Path]:
    """Get all content files (markdown, yaml) from a content directory.
    
    Returns list of paths relative to the content directory.
    """
    content_dir = Path(content_dir)
    
    if not content_dir.exists():
        return []
    
    files = []
    for pattern in ["**/*.md", "**/*.yml", "**/*.yaml"]:
        files.extend(content_dir.glob(pattern))
    
    return sorted(files)
