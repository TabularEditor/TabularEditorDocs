# TabularEditorDocs

This is the GitHub repository for the Tabular Editor documentation site, https://docs.tabulareditor.com. The repository contains documentation articles for both the open-source Tabular Editor 2.x as well as the commercial Tabular Editor 3, including articles for common features and C# scripting documentation.

# Technical details

The site uses [DocFX](https://dotnet.github.io/docfx/) and GitHub flavoured markdown for all articles. Multi-language support is provided through the `localizedContent/` directory.

# How to contribute

All contributions are welcome. We will review all pull requests submitted.

To test your changes locally:
- Make sure [DocFX](https://dotnet.github.io/docfx/) and Python 3.11+ are installed.
- Run `python build-docs.py --serve` in the root of the project.

# Build Script Usage

The `build-docs.py` script handles all documentation building tasks including multi-language support.

## Quick Start

```bash
# Build and serve locally (English only, for development)
python build-docs.py --serve

# Or build all languages and serve with Azure Static Web Apps CLI
python build-docs.py --all
swa start _site
```

## Commands

| Command | Description |
|---------|-------------|
| `python build-docs.py` | Build all languages (default) |
| `python build-docs.py --all` | Build all languages |
| `python build-docs.py --lang en` | Build English only |
| `python build-docs.py --lang es zh` | Build specific languages |
| `python build-docs.py --list` | List available languages |
| `python build-docs.py --serve` | Build English and serve locally |

## Options

| Option | Description |
|--------|-------------|
| `--all` | Build all available languages |
| `--lang LANGS` | Build specific language(s), space-separated |
| `--list` | List available languages and exit |
| `--serve` | Build and serve locally (English only, for development) |
| `--skip-gen` | Skip running gen_redirects.py (use existing configs) |
| `--no-api-copy` | Skip copying API docs to localized sites |

## What the Build Script Does

1. **Generates DocFX configurations** - Runs `gen_redirects.py` to create `docfx.json` for each language
2. **Generates language manifest** - Creates `metadata/languages.json` for runtime language switching
3. **Syncs content** - Copies English source content; uses English as fallback for missing translations. Readds the english file if the file is modified in content or deleted in translation.
4. **Builds documentation** - Runs DocFX for each requested language
5. **Fixes API docs** - Patches xref links in generated API documentation
6. **Copies API docs** - Shares English API docs with localized sites
7. **Injects SEO tags** - Adds hreflang and canonical tags to HTML files
8. **Generates SWA config** - Creates `staticwebapp.config.json` for Azure Static Web Apps routing

# Project Structure

```
TEDoc/
├── build-docs.py              # Main build script
├── build_scripts/             # Helper scripts
│   ├── gen_redirects.py       # Generates docfx.json configs
│   ├── gen_languages.py       # Generates language manifest
│   ├── gen_staticwebapp_config.py
│   ├── inject_seo_tags.py
│   └── sync-localized-content.py
├── content/                   # English source content (tracked in git)
│   └── _ui-strings.json       # English UI strings (header, footer, banners)
├── localizedContent/          # Build directories for all languages
│   ├── en/                    # English build (generated, gitignored)
│   └── {lang}/                # Translated content
│       ├── content/           # Translated markdown and UI strings (tracked)
│       │   └── _ui-strings.json  # Translated UI strings for this language
│       └── docfx.json         # Generated config (gitignored)
├── metadata/
│   ├── languages.json         # Language manifest (generated)
│   ├── language-metadata.json # Language display names and RTL flags
│   └── redirects.json         # URL redirects (server 301s and client meta-refresh)
├── docfx-template.json        # Base DocFX configuration template
├── templates/                 # DocFX templates
└── _site/                     # Generated output
    ├── en/
    ├── es/
    └── ...
```

# Adding a New Language

1. Create `localizedContent/{lang}/content/` folder (e.g., `fr/content/`)
2. Add the language entry to `metadata/language-metadata.json` with name and nativeName
3. Add translated `.md` files to the content subdirectory
4. Add a translated `_ui-strings.json` to the content subdirectory (see [Translating UI Strings](#translating-ui-strings) below). If no translation is provided, an automatic fallback will be generated.
5. Run `python build-docs.py --all` to generate configs and build. Language will be added dynamically to language picker.

> **Note:** English content from `content/` is automatically copied to `localizedContent/en/content/` during build. For other languages, English content is used as fallback for missing translations. This includes `_ui-strings.json` — if no translated version exists, English UI strings are used.

# Translating UI Strings

The `_ui-strings.json` file controls the text of site-wide UI elements that are not part of the documentation content itself: the header navigation, header buttons, footer text, and the AI translation warning banner. These strings are applied at runtime by the JavaScript bundle for non-English pages.

The English source is at `content/_ui-strings.json`. To provide translations for a language, create `localizedContent/{lang}/content/_ui-strings.json` with the same keys and translated values.

If a key is missing from a language's file, or no `_ui-strings.json` exists at all, the English value is used as fallback.

## Available Keys

| Key | English value | Element |
|-----|--------------|---------|
| `aiTranslationWarning` | `This content has been translated by AI...` | Warning banner shown on translated pages |
| `header.nav.pricing` | `Pricing` | Header nav link |
| `header.nav.download` | `Download` | Header nav link |
| `header.nav.learn` | `Learn` | Header nav link |
| `header.nav.resources` | `Resources` | Header nav dropdown toggle |
| `header.nav.blog` | `Blog` | Resources dropdown item |
| `header.nav.newsletter` | `Newsletter` | Resources dropdown item |
| `header.nav.publications` | `Publications` | Resources dropdown item |
| `header.nav.documentation` | `Documentation` | Resources dropdown item |
| `header.nav.supportCommunity` | `Support community` | Resources dropdown item |
| `header.nav.contactUs` | `Contact Us` | Header nav link |
| `header.button1` | `Free trial` | Primary header CTA button |
| `header.button2` | `Main page` | Secondary header button |
| `footer.heading` | `Ready to get started?` | Footer section heading |
| `footer.button1` | `Try Tabular Editor 3 for free` | Footer CTA button |
| `footer.button2` | `Buy Tabular Editor 3` | Footer CTA button |
| `footer.aboutUs` | `About us` | Footer left link |
| `footer.contactUs` | `Contact us` | Footer left link |
| `footer.technicalSupport` | `Technical Support` | Footer left link |
| `footer.privacyPolicy` | `Privacy & Cookie policy` | Footer bottom link |
| `footer.termsConditions` | `Terms & Conditions` | Footer bottom link |
| `footer.licenseTerms` | `License terms` | Footer bottom link |

