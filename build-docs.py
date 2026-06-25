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
    --skip-api      Reuse existing content/api instead of regenerating API metadata
                    (~30-40% faster). LOCAL markdown iteration ONLY, with --serve/--lang;
                    never for testing, CI/CD, or release builds.
    --permissive    Don't fail the English build on DocFX warnings (local iteration)
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


_DOCFX_WARNING_RE = re.compile(r': warning ', re.IGNORECASE)


def run_command(cmd: list[str], description: str, check: bool = True, fail_on_warnings: bool = False) -> int:
    """Run a command and return exit code.

    If fail_on_warnings=True, streams output line-by-line, counts DocFX warning
    diagnostics (lines matching ': warning '), and returns exit code 1 if any
    are found — even when the process itself exits 0.
    """
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"{'='*60}")
    print(f"Running: {' '.join(cmd)}\n")

    if fail_on_warnings:
        warning_count = 0
        process = subprocess.Popen(
            cmd,
            shell=(os.name == 'nt'),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        for line in process.stdout:
            print(line, end='', flush=True)
            if _DOCFX_WARNING_RE.search(line):
                warning_count += 1
        process.wait()

        if check and process.returncode != 0:
            print(f"Error: Command failed with exit code {process.returncode}")
            return process.returncode

        if warning_count > 0:
            print(f"\nError: DocFX produced {warning_count} warning(s). Failing build.")
            return 1

        return process.returncode

    result = subprocess.run(cmd, shell=(os.name == 'nt'))

    if check and result.returncode != 0:
        print(f"Error: Command failed with exit code {result.returncode}")
        return result.returncode

    return result.returncode


DOCFX: list[str] = []          # cache; populated on first ensure_docfx()


def _local_docfx_available() -> bool:
    """True if a dotnet tool manifest in cwd or an ancestor declares docfx.

    Mirrors dotnet's manifest discovery (cwd upward, `.config/` or legacy path,
    stop at an isRoot manifest). Filesystem-only — does not verify the tool is
    restored; a missing restore surfaces as a clear `dotnet docfx` error at build time.
    """
    for d in (Path.cwd(), *Path.cwd().parents):
        manifest = next((m for m in (d / ".config" / "dotnet-tools.json",
                                      d / "dotnet-tools.json") if m.is_file()), None)
        if manifest is None:
            continue
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if "docfx" in {k.lower() for k in data.get("tools", {})}:
            return True
        if data.get("isRoot"):
            break  # root manifest without docfx: dotnet stops searching here too
    return False


def resolve_docfx() -> list[str]:
    """Resolve how to invoke docfx: $DOCFX override, then a repo-pinned local tool
    (`dotnet docfx`), then a global/PATH `docfx`. Raises if none is available."""
    override = os.environ.get("DOCFX")
    if override:
        return override.split()
    if shutil.which("dotnet") and _local_docfx_available():
        return ["dotnet", "docfx"]
    if shutil.which("docfx"):
        return ["docfx"]
    raise SystemExit(
        "Error: docfx not found.\n"
        "  Local:  dotnet tool install docfx   (then `dotnet tool restore`)\n"
        "  Global: dotnet tool install -g docfx"
    )


def ensure_docfx() -> list[str]:
    """Return the docfx invocation prefix, resolving (and caching) it on first use."""
    global DOCFX
    if not DOCFX:
        DOCFX = resolve_docfx()
    return DOCFX


def run_docfx(args: list[str], description: str, **kwargs) -> int:
    """Run docfx with the resolved invocation prefix (global/PATH or `dotnet docfx`)."""
    return run_command([*ensure_docfx(), *args], description, **kwargs)


def get_available_languages() -> list[str]:
    """Get list of available languages from metadata/languages.json or scan localizedContent/."""
    manifest_path = Path("metadata/languages.json")
    
    if manifest_path.exists():
        with open(manifest_path) as f:
            data = json.load(f)
            # Handle both simple array and rich metadata formats
            languages = data.get("languages", [])
            if languages and isinstance(languages[0], dict):
                return [lang["code"] for lang in languages]
            return languages
    
    # Fallback: scan localizedContent/ directly
    localized_dir = Path("localizedContent")
    if not localized_dir.exists():
        return []
    
    return sorted([
        d.name for d in localized_dir.iterdir()
        if d.is_dir() and len(d.name) <= 5
    ])


def prepare_localized_content(lang: str, sync: bool = False) -> int:
    """Run sync-localized-content.py for a language.

    For English: always copies all source content (required for docfx)
    For other languages:
        sync=True:  full English fallback sync (hash comparison, copy missing/outdated)
        sync=False: only sync shared directories (assets, api) — Crowdin manages translations
    """
    if lang == "en":
        # English always needs full sync
        return run_command(
            [sys.executable, "build_scripts/sync-localized-content.py", "--sync", "en"],
            "Syncing English content from source"
        )

    if sync:
        result = run_command(
            [sys.executable, "build_scripts/sync-localized-content.py", "--sync", lang],
            f"Syncing {lang} content (fallback to English for outdated)"
        )
    else:
        result = run_command(
            [sys.executable, "build_scripts/sync-localized-content.py", "--shared-only", lang],
            f"Syncing shared directories for {lang}"
        )
    if result != 0:
        return result

    # Repair Crowdin-collapsed DocFX alerts (e.g. "> [!NOTE]> text") before docfx
    # builds this language, so alerts render as styled boxes instead of plain quotes.
    result = run_command(
        [sys.executable, "build_scripts/normalize-localized-alerts.py", lang],
        f"Normalizing DocFX alerts for {lang}"
    )
    if result != 0:
        return result

    # Stabilize heading anchors: inject English-slug bookmark anchors before
    # translated headings so cross-reference links (#anchor) resolve even though
    # the heading text is translated. Prevents InvalidBookmark warnings.
    return run_command(
        [sys.executable, "build_scripts/normalize-localized-heading-anchors.py", lang],
        f"Stabilizing heading anchors for {lang}"
    )


def build_language(lang: str, sync: bool = False, skip_api: bool = False, permissive: bool = False) -> int:
    """Build documentation for a specific language."""
    config_path = f"localizedContent/{lang}/docfx.json"

    if not os.path.exists(config_path):
        print(f"Error: Config file not found: {config_path}")
        print("Run 'python gen_redirects.py' first to generate configs.")
        return 1

    # Prepare content (copy from source for en, or fallbacks for other langs)
    result = prepare_localized_content(lang, sync=sync)
    if result != 0:
        return result

    # Build the documentation — fail on DocFX warnings only for English (the
    # authored source). Localized content is Crowdin-managed and may carry
    # translation warnings that must not block deployment. `permissive` lifts the
    # English gate too, for local iteration where transient warnings are expected
    # (warnings are still printed, just not fatal); full/CI builds leave it off.
    #
    # `docfx build` skips API metadata regeneration and reuses the existing
    # content/api/*.yml (the _apiSource DLLs don't change between content edits),
    # which is ~30-40% faster; bare `docfx` regenerates metadata then builds.
    return run_docfx(
        [*(["build"] if skip_api else []), config_path],
        f"Building {lang} documentation",
        fail_on_warnings=(lang == "en" and not permissive)
    )


def copy_languages_manifest() -> int:
    """Copy languages.json to _site/ root for runtime access."""
    manifest_src = Path("metadata/languages.json")
    manifest_dest = Path("_site/languages.json")
    
    if not manifest_src.exists():
        print("Warning: languages.json not found, skipping copy")
        return 0
    
    # Ensure _site directory exists
    manifest_dest.parent.mkdir(parents=True, exist_ok=True)
    
    shutil.copy(manifest_src, manifest_dest)
    print(f"Copied languages.json to _site/")
    return 0


def copy_404_to_root() -> int:
    """Copy 404.html from English site to _site/ root for SWA fallback."""
    src_404 = Path("_site/en/404.html")
    dest_404 = Path("_site/404.html")
    
    if not src_404.exists():
        print("Warning: _site/en/404.html not found, skipping 404 copy")
        return 0
    
    shutil.copy(src_404, dest_404)
    print(f"Copied 404.html to _site/ root")
    return 0


def copy_index_to_root() -> int:
    """Copy index.html redirect from content to _site/ root for SWA validation."""
    src_index = Path("content/index.html")
    dest_index = Path("_site/index.html")
    
    if not src_index.exists():
        print("Warning: content/index.html not found, skipping index copy")
        return 0
    
    shutil.copy(src_index, dest_index)
    print(f"Copied index.html to _site/ root")
    return 0


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
    parser.add_argument("--no-api-copy", action="store_true", help="Skip copying API docs to localized sites")
    parser.add_argument("--skip-api", action="store_true", help="LOCAL markdown iteration only (requires --serve/--lang): reuse existing content/api, ~30-40%% faster. NEVER for testing/CI/CD/releases")
    parser.add_argument("--permissive", action="store_true", help="Don't treat English DocFX warnings as build failures (for local iteration; keep full/CI builds strict)")
    parser.add_argument("--sync", action="store_true", help="Sync English fallback for missing/outdated translations (for local dev)")
    
    args = parser.parse_args()
    
    # List available languages
    if args.list:
        langs = get_available_languages()
        print("Available languages:")
        for lang in langs:
            suffix = " (default)" if lang == "en" else ""
            print(f"  {lang}{suffix}")
        return 0

    # Resolve docfx now so a missing install exits before any build work happens.
    ensure_docfx()

    # --skip-api is strictly a fast LOCAL iteration aid for editing markdown: it reuses
    # the existing content/api/*.yml instead of regenerating API metadata. It must NEVER
    # be used for full builds, testing, CI/CD, or releases (those must regenerate the API).
    # Guard it conservatively: require an explicit single-target (--serve or --lang),
    # forbid --all / the default all-languages build, and require API metadata to already
    # exist so we never silently ship a site with missing or stale API docs.
    if args.skip_api:
        if args.all or not (args.serve or args.lang):
            print(
                "Error: --skip-api is for fast LOCAL iteration only and must target a single build.\n"
                "       Use it with --serve or --lang (e.g. `--serve --skip-api`, `--lang en --skip-api`).\n"
                "       Never use it for --all, testing, CI/CD, or release builds — omit it so API\n"
                "       metadata is regenerated.",
                file=sys.stderr,
            )
            return 1
        if not list(Path("content/api").glob("*.yml")):
            print(
                "Error: --skip-api reuses existing API metadata, but content/api/*.yml is missing.\n"
                "       Run a full build once (e.g. `python3 build-docs.py --lang en`) to generate it.",
                file=sys.stderr,
            )
            return 1
        print("\n" + "=" * 60)
        print("  WARNING: --skip-api active — reusing existing content/api/*.yml.")
        print("  Fast LOCAL markdown iteration ONLY; API docs may be stale.")
        print("  NEVER use --skip-api for testing, CI/CD, or release builds.")
        print("=" * 60)

    # Run gen_redirects.py first (unless skipped)
    if not args.skip_gen:
        result = run_command(
            [sys.executable, "build_scripts/gen_redirects.py"],
            "Generating docfx configurations"
        )
        if result != 0:
            return result
        
        # Generate languages manifest
        result = run_command(
            [sys.executable, "build_scripts/gen_languages.py"],
            "Generating languages manifest"
        )
        if result != 0:
            return result
    
    # Determine which languages to build
    available_langs = get_available_languages()
    
    if args.serve:
        # Build English only and serve
        result = build_language("en", sync=True, skip_api=args.skip_api, permissive=args.permissive)
        if result != 0:
            return result
        
        fix_xref_in_api()
        copy_languages_manifest()
        
        # Also copy to _site/en/ for local serving (docfx serve serves from en/)
        manifest_src = Path("metadata/languages.json")
        manifest_dest = Path("_site/en/languages.json")
        if manifest_src.exists():
            shutil.copy(manifest_src, manifest_dest)
            print("Copied languages.json to _site/en/")
        
        return run_docfx(
            ["serve", "_site/en"],
            "Serving documentation locally"
        )
    
    if args.lang:
        # Build specific languages
        build_langs = args.lang
        
        # Validate languages
        for lang in build_langs:
            if lang not in available_langs:
                print(f"Error: Language '{lang}' not found")
                print(f"Available: {', '.join(available_langs)}")
                return 1
    else:
        # Build all languages (default behavior)
        build_langs = available_langs
    
    # Ensure English is built first (needed for API docs)
    if "en" in build_langs:
        build_langs = ["en"] + [l for l in build_langs if l != "en"]
    
    # Build all requested languages
    for lang in build_langs:
        result = build_language(lang, sync=args.sync, skip_api=args.skip_api, permissive=args.permissive)
        if result != 0:
            return result
        
        if lang == "en":
            fix_xref_in_api()
    
    # Copy API docs to localized sites (non-English)
    non_en_langs = [l for l in build_langs if l != "en"]
    if non_en_langs and not args.no_api_copy and "en" in build_langs:
        copy_api_docs(non_en_langs)
    
    # Copy languages manifest to _site root
    copy_languages_manifest()
    
    # Copy 404.html to site root for SWA fallback
    copy_404_to_root()
    
    # Copy index.html to site root for SWA validation
    copy_index_to_root()
    
    # Inject SEO tags (hreflang, canonical) into HTML files for built languages
    for lang in build_langs:
        run_command(
            [sys.executable, "build_scripts/inject_seo_tags.py", "--lang", lang],
            f"Injecting SEO tags for {lang}"
        )
    
    # Generate staticwebapp.config.json for Azure SWA routing
    run_command(
        [sys.executable, "build_scripts/gen_staticwebapp_config.py"],
        "Generating staticwebapp.config.json"
    )

    # Generate site-wide sitemap index (references each language's sitemap.xml)
    # and robots.txt. Runs last so all per-language sitemaps already exist.
    run_command(
        [sys.executable, "build_scripts/gen_sitemap_index.py"],
        "Generating sitemap index and robots.txt"
    )

    print(f"\n{'='*60}")
    print("  Build complete!")
    print(f"{'='*60}")
    print(f"Output: _site/")
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
