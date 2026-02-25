# TabularEditorDocs
This is the GitHub repository for the Tabular Editor documentation site, https://docs.tabulareditor.com. The repository contains documentation articles for both the open-source Tabular Editor 2.x as well as the commercial Tabular Editor 3, including articles for common features and C# scripting documentation.

# Technical details
The site uses [DocFX](https://dotnet.github.io/docfx/) and GitHub flavoured markdown for all articles. Multi-language support is provided through the `localizedContent/` directory.

# How to contribute
All contributions are welcome. We will review all pull requests submitted.

## Local Development

Make sure [DocFX](https://dotnet.github.io/docfx/) and Python 3.11+ are installed.

### Quick Start (English only)
```bash
python build-docs.py --serve
```

### Build Commands
```bash
# Build all languages (English + all translations)
python build-docs.py --all

# Build English only
python build-docs.py --lang en

# Build specific languages
python build-docs.py --lang es zh

# List available languages
python build-docs.py --list

# Build and serve locally (English only)
python build-docs.py --serve
```

### Project Structure
- `content/` - English source content (tracked in git)
- `localizedContent/` - Build directories for all languages:
  - `en/` - English build (fully generated, gitignored)
  - `{lang}/` - Translated content for other languages:
    - `content/` - Translated markdown files (tracked)
    - `docfx.json` - Generated config (gitignored)
- `docfx-template.json` - Base DocFX configuration template
- `docfxTranslations/languages.json` - Language manifest (generated)
- `_site/` - Generated output (`en/`, `es/`, `zh/`, etc.)

### Adding a New Language
1. Create `localizedContent/{lang}/content/` folder (e.g., `fr/content/`)
2. Add translated `.md` files to the content subdirectory
3. Run `python build-docs.py --all` to generate configs and build

> **Note:** English content from `content/` is automatically copied to `localizedContent/en/content/` during build. For other languages, English content is used as fallback for missing translations.

