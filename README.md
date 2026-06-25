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
| `--sync` | Sync English fallback for missing/outdated translations (for local dev) |

## What the Build Script Does

1. **Generates DocFX configurations** - Runs `gen_redirects.py` to create `docfx.json` for each language
2. **Generates language manifest** - Creates `metadata/languages.json` for runtime language switching
3. **Syncs content** - Copies English source to `localizedContent/en/`. For other languages, only shared directories (assets, api) are synced by default since Crowdin manages translations. Use `--sync` to enable full English fallback for missing/outdated translations (useful for local development).
4. **Normalizes DocFX alerts** - Runs `normalize-localized-alerts.py` on each non-English language to repair Crowdin-collapsed Note/Tip/etc. alerts before building (see [DocFX Alerts and Translations](#docfx-alerts-and-translations))
5. **Stabilizes heading anchors** - Runs `normalize-localized-heading-anchors.py` on each non-English language to inject English-slug bookmark anchors before translated headings, so `#anchor` cross-references resolve even when the heading text is translated (see [Bookmark Links and Translations](#bookmark-links-and-translations))
6. **Builds documentation** - Runs DocFX for each requested language
7. **Fixes API docs** - Patches xref links in generated API documentation
8. **Copies API docs** - Shares English API docs with localized sites
9. **Injects SEO tags** - Adds hreflang and canonical tags to HTML files
10. **Generates SWA config** - Creates `staticwebapp.config.json` for Azure Static Web Apps routing

# Project Structure

```
TEDoc/
├── build-docs.py              # Main build script
├── build_scripts/             # Helper scripts
│   ├── gen_redirects.py       # Generates docfx.json configs
│   ├── gen_languages.py       # Generates language manifest
│   ├── gen_staticwebapp_config.py
│   ├── inject_seo_tags.py
│   ├── sync-localized-content.py
│   ├── normalize-localized-alerts.py  # Repairs Crowdin-collapsed DocFX alerts
│   └── normalize-localized-heading-anchors.py  # Injects English-slug bookmark anchors into translations
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

> **Note:** English content from `content/` is automatically copied to `localizedContent/en/content/` during build. For other languages, Crowdin manages translations via PRs. Shared directories (assets, api) are always synced from English. To use English as fallback for missing/outdated translations during local development, add the `--sync` flag.

# Bookmark Links and Translations

When linking to a specific heading within a page (e.g., `#my-heading`), DocFX auto-generates the anchor ID from the heading **text**. Because Crowdin translates that text, the generated anchor changes per language (`#model-io` becomes `#es-del-modelo`, etc.), so a hardcoded English `#anchor` link breaks in every translated page and DocFX logs an `InvalidBookmark` warning. English builds stay clean because the anchors match there.

## Automatic anchor stabilization (the build handles this)

`build_scripts/normalize-localized-heading-anchors.py` neutralizes this whole class of warning automatically. For each localized page it reads the matching English source, computes each heading's English slug, and injects a hidden bookmark anchor carrying that slug immediately before the corresponding translated heading:

```markdown
<a id="model-io" data-loc-xref></a>
## E/S del modelo
```

DocFX accepts the injected `id` as a valid bookmark, so `#model-io` resolves and the link lands on the right section while the heading keeps its translated text. Headings are aligned to the English source positionally (Crowdin preserves heading structure); if the heading counts differ, the file is skipped and reported rather than risk a misaligned anchor. The script is idempotent (it strips its own `data-loc-xref` anchors before recomputing) and never modifies English.

The build runs it automatically for each non-English language before DocFX (step 5 of [What the Build Script Does](#what-the-build-script-does)). You can also run it manually after a Crowdin pull:

```bash
python build_scripts/normalize-localized-heading-anchors.py            # all languages
python build_scripts/normalize-localized-heading-anchors.py --dry-run  # preview without writing
python build_scripts/normalize-localized-heading-anchors.py --check    # exit 1 if changes are needed (CI)
python build_scripts/normalize-localized-heading-anchors.py es         # a single language
```

## Authoring guidance

- **Prefer the bracketed link form** `[text](xref:uid#anchor)` over the bare `@uid#anchor` autolink. The closing `)` delimits the anchor, so trailing punctuation in any language can never leak into it.
- **For a rename-proof anchor**, add an explicit `<a name="..."></a>` tag above the heading. Crowdin does not translate HTML `name` attributes, so the anchor stays stable across all languages *and* survives English heading renames — unlike an auto-generated slug. Only add these to headings actually linked to; there is no need to add them everywhere.

  ```markdown
  <a name="my-heading"></a>
  ## My Heading
  ```

# DocFX Alerts and Translations

DocFX renders styled alert boxes (Note, Tip, Important, Warning, Caution) from a two-line blockquote where the marker stands alone on the first line:

```markdown
> [!NOTE]
> Your note text here.
```

When an alert like this is nested inside a list item, Crowdin collapses the two lines into one on export, producing `> [!NOTE]> Your note text here.`. DocFX requires the marker to be alone on its line, so the collapsed form is downgraded to a plain `<blockquote>` — losing the styled box — and the build logs an `invalid-note-section` warning. Only list-nested alerts are affected; top-level alerts round-trip through Crowdin unchanged.

`build_scripts/normalize-localized-alerts.py` repairs this by splitting the collapsed form back into two lines, preserving the original indentation so the alert stays inside its list item. It is idempotent and only rewrites the exact collapsed pattern (text inside fenced code blocks is left untouched), so it is safe to run repeatedly.

The build runs it automatically for each non-English language before DocFX (step 4 of [What the Build Script Does](#what-the-build-script-does)). You can also run it manually after a Crowdin pull:

```bash
python build_scripts/normalize-localized-alerts.py            # fix all languages
python build_scripts/normalize-localized-alerts.py --dry-run  # preview without writing
python build_scripts/normalize-localized-alerts.py --check    # exit 1 if fixes are needed (CI)
python build_scripts/normalize-localized-alerts.py es         # fix a single language
```

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
| `footer.button1` | `Try Tabular Editor 3` | Footer CTA button |
| `footer.button2` | `Buy Tabular Editor 3` | Footer CTA button |
| `footer.aboutUs` | `About us` | Footer left link |
| `footer.contactUs` | `Contact us` | Footer left link |
| `footer.technicalSupport` | `Technical Support` | Footer left link |
| `footer.privacyPolicy` | `Privacy & Cookie policy` | Footer bottom link |
| `footer.termsConditions` | `Terms & Conditions` | Footer bottom link |
| `footer.licenseTerms` | `License terms` | Footer bottom link |
| `appliesTo` | `Applies to: ` | "Applies to" label on article metadata |
| `availableSince` | `Available since` | Version availability label (e.g., "Available since 3.5.0") |
| `availableIn` | `Available in` | Version range label (e.g., "Available in 3.5.0–3.8.0") |
| `inThisArticle` | `In this article` | Sidebar table of contents heading |
| `searchResultsCount` | `{count} results for "{query}"` | Search results summary |
| `searchNoResults` | `No results for "{query}"` | No search results message |
| `tocFilter` | `Filter by title` | TOC filter input placeholder |
| `nextArticle` | `Next` | Next article navigation |
| `prevArticle` | `Previous` | Previous article navigation |
| `themeLight` | `Light` | Theme picker option |
| `themeDark` | `Dark` | Theme picker option |
| `themeAuto` | `Auto` | Theme picker option |
| `changeTheme` | `Change theme` | Theme picker label |
| `copy` | `Copy` | Code block copy button |
| `downloadPdf` | `Download PDF` | PDF download button |
| `search` | `Search documentation` | Search input placeholder |
| `note` | `Note` | Alert box heading |
| `warning` | `Warning` | Alert box heading |
| `tip` | `Tip` | Alert box heading |
| `important` | `Important` | Alert box heading |
| `caution` | `Caution` | Alert box heading |
| `tableOfContents` | `Table of Contents` | Mobile TOC offcanvas title |
| `selectLanguage` | `Select language` | Language picker label |
| `copyCode` | `Copy code` | Code block copy button aria-label |

