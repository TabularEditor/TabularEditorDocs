#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Post-process the English sitemap and generate the site-wide entry point.

DocFX emits a sitemap for the default (English) language at
_site/{default_lang}/sitemap.xml (configured via build.sitemap in the generated
docfx.json). Non-default languages do not emit a sitemap. This script:

  1. Removes Tabular Editor 2-only URLs from the English sitemap per the
     'exclude' rules in build-config.json.
  2. Downranks selected URLs in the English sitemap (API reference pages) per
     the 'downrank' rules in build-config.json.
  3. Writes _site/sitemap.xml: a <sitemapindex> pointing at the English sitemap
     (the published sitemap covers English only).
  4. Writes _site/robots.txt: allows all crawlers and advertises the index.

Run after the English build so _site/{default_lang}/sitemap.xml exists.

Usage:
    python gen_sitemap_index.py              # Process _site/
    python gen_sitemap_index.py --dry-run    # Preview without writing
"""

import argparse
import xml.etree.ElementTree as ET
from pathlib import Path

from config_loader import (
    get_base_url,
    get_default_language,
    get_sitemap_downrank,
    get_sitemap_exclude,
)


SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"


def apply_exclude(sitemap_path: Path, rules: list[dict], dry_run: bool = False) -> int:
    """Remove <url> entries whose <loc> matches an exclude rule. Returns count removed.

    A rule matches when its 'match' substring appears anywhere in the URL's
    <loc>. Used to drop Tabular Editor 2-only pages from the published sitemap.
    """
    if not rules or not sitemap_path.exists():
        return 0

    ET.register_namespace("", SITEMAP_NS)
    tree = ET.parse(sitemap_path)
    root = tree.getroot()

    matches = [m for r in rules if (m := r.get("match"))]

    removed = 0
    for url in list(root.findall(f"{{{SITEMAP_NS}}}url")):
        loc_el = url.find(f"{{{SITEMAP_NS}}}loc")
        if loc_el is None or not loc_el.text:
            continue
        if any(m in loc_el.text for m in matches):
            root.remove(url)
            removed += 1

    if removed and not dry_run:
        tree.write(sitemap_path, encoding="utf-8", xml_declaration=True)

    return removed


def apply_downrank(sitemap_path: Path, rules: list[dict], dry_run: bool = False) -> int:
    """Lower <priority> for URLs matching downrank rules. Returns count changed.

    A rule matches when its 'match' substring appears anywhere in the URL's
    <loc>. Rules are evaluated in order; the first match wins.
    """
    if not rules or not sitemap_path.exists():
        return 0

    ET.register_namespace("", SITEMAP_NS)
    tree = ET.parse(sitemap_path)
    root = tree.getroot()

    changed = 0
    for url in root.findall(f"{{{SITEMAP_NS}}}url"):
        loc_el = url.find(f"{{{SITEMAP_NS}}}loc")
        if loc_el is None or not loc_el.text:
            continue
        loc = loc_el.text
        for rule in rules:
            match = rule.get("match")
            priority = rule.get("priority")
            if not match or priority is None:
                continue
            if match in loc:
                priority_el = url.find(f"{{{SITEMAP_NS}}}priority")
                if priority_el is None:
                    priority_el = ET.SubElement(url, f"{{{SITEMAP_NS}}}priority")
                priority_el.text = f"{float(priority):.1f}"
                changed += 1
                break

    if changed and not dry_run:
        tree.write(sitemap_path, encoding="utf-8", xml_declaration=True)

    return changed


def build_index_xml(base_url: str, default_lang: str, site_dir: Path) -> tuple[str, bool]:
    """Build the sitemap index XML referencing only the default language.

    Returns (xml_string, included) where included is True if the default
    language sitemap exists.
    """
    included = (site_dir / default_lang / "sitemap.xml").exists()

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    if included:
        lines.append("  <sitemap>")
        lines.append(f"    <loc>{base_url}/{default_lang}/sitemap.xml</loc>")
        lines.append("  </sitemap>")
    lines.append("</sitemapindex>")
    return "\n".join(lines) + "\n", included


def build_robots_txt(base_url: str) -> str:
    """Build a robots.txt that allows all crawlers and advertises the sitemap index."""
    return (
        "User-agent: *\n"
        "Allow: /\n\n"
        f"Sitemap: {base_url}/sitemap.xml\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Post-process the English sitemap and generate the site-wide index"
    )
    parser.add_argument(
        "--site-dir", "-s",
        default="_site",
        help="Site output directory (default: _site)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview output without writing files"
    )

    args = parser.parse_args()

    site_dir = Path(args.site_dir)
    if not site_dir.exists():
        print(f"Error: site directory {site_dir} does not exist")
        return 1

    base_url = get_base_url()
    default_lang = get_default_language()
    en_sitemap = site_dir / default_lang / "sitemap.xml"

    print(f"Base URL: {base_url}")
    print(f"Default language: {default_lang}")

    # 1. Remove Tabular Editor 2-only pages from the English sitemap
    exclude_rules = get_sitemap_exclude()
    removed = apply_exclude(en_sitemap, exclude_rules, dry_run=args.dry_run)
    print(f"Exclude rules: {len(exclude_rules)}; URLs removed: {removed}")

    # 2. Downrank API reference pages in the English sitemap
    rules = get_sitemap_downrank()
    changed = apply_downrank(en_sitemap, rules, dry_run=args.dry_run)
    print(f"Downrank rules: {len(rules)}; URLs adjusted: {changed}")

    # 3. Build the English-only sitemap index
    index_xml, included = build_index_xml(base_url, default_lang, site_dir)
    if not included:
        print(f"Warning: {en_sitemap} not found - sitemap index will be empty. "
              "Check that build.sitemap is set in the English docfx.json.")

    # 4. robots.txt
    robots_txt = build_robots_txt(base_url)

    if args.dry_run:
        print("\n--- _site/sitemap.xml ---")
        print(index_xml)
        print("--- _site/robots.txt ---")
        print(robots_txt)
        return 0

    (site_dir / "sitemap.xml").write_text(index_xml, encoding="utf-8")
    (site_dir / "robots.txt").write_text(robots_txt, encoding="utf-8")

    print(f"\nGenerated: {site_dir / 'sitemap.xml'} (English only)")
    print(f"Generated: {site_dir / 'robots.txt'}")
    return 0


if __name__ == "__main__":
    exit(main())
