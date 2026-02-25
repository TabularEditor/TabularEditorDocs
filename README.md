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
- `content/` - English source content
- `localizedContent/{lang}/` - Localized builds for each language:
  - `content/` - Translated content (markdown files, toc.yml, etc.)
  - `docfx.json` - Generated config (gitignored)
- `docfx-template.json` - Base DocFX configuration template
- `docfx.json` - Generated English config (do not edit)
- `docfxTranslations/languages.json` - Language manifest
- `_site/` - Generated output (`en/`, `es/`, `zh/`, etc.)

### Adding a New Language
1. Create `localizedContent/{lang}/content/` folder (e.g., `fr/content/`)
2. Add translated `.md` files to the content subdirectory
3. Run `python build-docs.py --all` to generate configs and build

> **Note:** English content is automatically used as fallback for missing translations. The `docfx.json` files inside `localizedContent/{lang}/` are auto-generated and gitignored.

