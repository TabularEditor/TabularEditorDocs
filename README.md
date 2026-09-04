# TabularEditorDocs

This is the GitHub repository for the Tabular Editor documentation site, https://docs.tabulareditor.com. The repository contains documentation articles for both the open-source Tabular Editor 2.x as well as the commercial Tabular Editor 3, including articles for common features and C# scripting documentation.

# Technical details

The site uses [DocFX](https://dotnet.github.io/docfx/) and GitHub flavoured markdown for all articles. Multi-language support is provided through the `localizedContent/` directory.

# How to contribute

All contributions are welcome. We will review all pull requests submitted.

For convenience for typical contributions, we have built a simple wrapper around the build process.
Unless you are working specifically on localization or the build process itself, you should be able to get by with the `run` script.

Getting started:
1. Make sure you have Bash installed (included in most Linux distros, macOS, and [Git for Windows](https://git-scm.com/install/windows))
2. From the repo root, run the setup check and install any tools it reports as missing
   - (Linux distros and macOS): `./run setup`
   - (Windows): `bash run setup` (after this run everything from Git Bash)
3. To iterate on docs and see a preview in your browser:
   - in one terminal: `./run serve`: launches a localhost server that renders the docs at http://localhost:8080 where you can see the docs as they will be rendered on the docs website
   - in another terminal: `./run watch`: regenerates the rendered site every time you save a change to a markdown document, so you can refresh your browser to see it

These commands all build and work only on the English language docs, as the English markdown is our canonical version of documentation and the language we expect contributions in.

For more info, try `./run help` and `./run <subcommand> help`.
If you'd like more detail, [check out the run script README](build_scripts/run_scripts/README.md).

If you want to have more control over the build process, continue reading below about the `build-docs.py` script.

# Advanced build Script Usage

The `build-docs.py` script handles all documentation building tasks including multi-language support.
Make sure you have Python >=3.11 and docfx installed, the latter either globally or locally.

## Using build-docs.py directly

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
| `--skip-api` | Reuse existing API metadata in content/api, ~30-40% faster (local markdown iteration only, requires `--serve`/`--lang`; never for testing/CI/CD/releases) |
| `--permissive` | Don't treat English DocFX warnings as build failures (for local iteration; full/CI builds stay strict) |
| `--sync` | Copy English over missing/outdated translations for a local build. Fallback copies only: never commit them. The translation status file is not touched |

## What the Build Script Does

1. **Generates DocFX configurations** - Runs `gen_redirects.py` to create `docfx.json` for each language
2. **Generates language manifest** - Creates `metadata/languages.json` for runtime language switching
3. **Syncs content** - Copies English source to `localizedContent/en/`. For other languages, only shared directories (assets, api) are synced by default: the translations themselves are committed by the automated translation workflow (see [Translating Content](#translating-content)). Use `--sync` to copy English over missing/outdated translations for a local build; those fallback copies must never be committed, and the translation status file is left alone.
4. **Normalizes DocFX alerts** - Runs `normalize-localized-alerts.py` on each non-English language as a safety net that repairs collapsed Note/Tip/etc. alerts in translator output before building (see [DocFX Alerts and Translations](#docfx-alerts-and-translations))
5. **Stabilizes heading anchors** - Runs `normalize-localized-heading-anchors.py` on each non-English language to inject English-slug bookmark anchors before translated headings, so `#anchor` cross-references resolve even when the heading text is translated (see [Bookmark Links and Translations](#bookmark-links-and-translations))
6. **Builds documentation** - Runs DocFX for each requested language
7. **Fixes API docs** - Patches xref links in generated API documentation
8. **Copies API docs** - Shares English API docs with localized sites
9. **Injects SEO tags** - Adds hreflang and canonical tags to HTML files
10. **Generates SWA config** - Creates `staticwebapp.config.json` for Azure Static Web Apps routing

# Project Structure

```
/
├── .github/workflows/
│   ├── deploy.yml             # Build and deploy the site
│   └── translate.yml          # Automated translation workflow (Translated), see Translating Content
├── build-docs.py              # Main build script
├── run                        # Task runner for common dev tasks (see build_scripts/run_scripts/README.md)
├── build_scripts/             # Helper scripts
│   ├── check_links.py         # Dead-link checker for the generated _site
│   ├── config_loader.py       # Shared configuration loader for build scripts
│   ├── csharp_doctest.py      # Validates annotated C# code blocks in docs against the te CLI
│   ├── gen_languages.py       # Generates language manifest
│   ├── gen_redirects.py       # Generates docfx.json configs
│   ├── gen_sitemap_index.py   # Post-processes the English sitemap; generates the sitemap index
│   ├── gen_staticwebapp_config.py     # Generates Azure Static Web Apps routing config
│   ├── inject_seo_tags.py     # Adds hreflang and canonical tags to built HTML
│   ├── normalize-localized-alerts.py  # Repairs collapsed DocFX alerts in translations (safety net)
│   ├── normalize-localized-heading-anchors.py  # Injects English-slug bookmark anchors into translations
│   ├── sync-localized-content.py      # Syncs English content into localized build dirs (local builds)
│   ├── translate-content.py           # Submits changed English content to Translated, verifies and writes the translations
│   ├── te_script_runner.py    # Runs C# snippets against a throwaway model via the te CLI
│   ├── test-fixtures/         # Fixtures for the build-script tests
│   └── run_scripts/           # ./run subcommand scripts and shared lib.sh (see its README)
├── content/                   # English source content (tracked in git)
│   └── _ui-strings.json       # English UI strings (header, footer, banners)
├── localizedContent/          # Build directories for all languages
│   ├── en/                    # English build (generated, gitignored)
│   └── {lang}/                # Translated content
│       ├── .translation-status.json  # Per-file translation bookkeeping, owned by translate-content.py (tracked)
│       ├── content/           # Translated markdown and UI strings (tracked)
│       │   └── _ui-strings.json  # Translated UI strings for this language
│       └── docfx.json         # Generated config (gitignored)
├── metadata/
│   ├── build-config.json      # Content/shared dirs and the `translation` section (environments, sources, passthrough)
│   ├── languages.json         # Language manifest (generated)
│   ├── language-metadata.json # Language display names, RTL flags and translatedLocale
│   └── redirects.json         # URL redirects (server 301s and client meta-refresh)
├── docfx-template.json        # Base DocFX configuration template
├── pyproject.toml             # ruff/mypy configuration for the checked build scripts
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

> **Note:** English content from `content/` is automatically copied to `localizedContent/en/content/` during build. For other languages, translations arrive as review PRs from the automated translation workflow (see [Translating Content](#translating-content)); add `"translatedLocale"` (e.g. `"fr-FR"`) to the language's entry in `metadata/language-metadata.json` so it is picked up (the first run submits every scoped file for the new language, so start with `--limit`). Shared directories (assets, api) are always synced from English. To use English as fallback for missing/outdated translations during local development, add the `--sync` flag; never commit those copies.

# Translating Content

Translations are produced by [Translated](https://translated.com) through the TranslationOS API and arrive as review PRs from the `localization` branch, driven by `.github/workflows/translate.yml` and `build_scripts/translate-content.py`. English in `content/` is the only authored source; do not hand-edit `localizedContent/{lang}/content/` on `main` unless you also pin the file (see [Runbook](#runbook)).

## Scope and configuration

The `translation` section of `metadata/build-config.json` defines what is translated and where:

- **`sources`** - globs relative to `content/`: every `**/*.md` (including the sidebar `toc.md` files), `404.html`, `getting-started/app/**/*.html`, `toc.yml` and `_ui-strings.json`. Files under the shared directories (`assets`, `api`) are always skipped.
- **`passthrough`** - `whats-new/**/*.html`. The release-note pages are not translated: every run copies them from English byte-for-byte when their hash differs (or the target is missing) and records them in the status file with status `copied`.
- **`environments`** - the two endpoints the script can talk to. `sandbox` is `https://api.sandbox.translated.com/v2/` with service type `premium` (the only one the sandbox accepts); `production` is `https://api.translated.com/v2/` with service type `null` until the account's service type is known. `TRANSLATED_ENV` selects which one is active (see below).
- **`batchSize`** (200 orders per `/translate` call) and **`sandboxLimits`** (`maxFilesPerRun`: 20, `maxCharsPerRun`: 200000; see [Sandbox caps](#sandbox-caps)).
- **`instructions`** - file-level notes attached to every order. They are shown to human linguists on human service types; machine translation does not enforce them. Glossaries and do-not-translate lists are configured by Translated on the service type itself, not per request.

Every target language folder needs a `translatedLocale` (`es-ES`, `zh-CN`) in `metadata/language-metadata.json`. A run checks this up front and fails with the list of missing locales before submitting anything.

## Environment variables

| Variable | Where it lives | Meaning |
|----------|----------------|---------|
| `TRANSLATED_API_KEY` | repository secret / your shell | API key for the active environment. |
| `TRANSLATED_ENV` | repository variable / your shell | `sandbox` or `production`; selects the entry of `translation.environments` to use. There is no default: every network action (`--submit`, `--poll`, `--run`, `--probe`) refuses to run while it is unset or unknown. |
| `TRANSLATED_SERVICE_TYPE` | repository variable / your shell | Overrides the environment's `serviceType`. Production has no default and refuses to run while the resolved service type is empty; run `--probe` to list the account's service types. |

Offline actions (`--plan`, `--self-test`, `--dump-orders`, `--baseline`) need neither variable nor key. Before any network call the script prints the resolved environment, base URL and service type - read that line before you continue.

## Command-line reference

`python build_scripts/translate-content.py <action> [options]`. Exactly one action per invocation:

| Action | What it does | Network |
|--------|--------------|---------|
| `--plan` | Print what would happen per language: missing/outdated files to submit, pending jobs, recorded failures, pinned and unscoped entries, orphans, passthrough copies, character counts. | no |
| `--submit` | Submit missing/outdated files (one order per file and language), copy passthrough files, delete orphaned translations. | yes |
| `--poll` | Collect deliveries for the pending jobs, repair and verify them, write the translations. | yes |
| `--run` | `--submit` followed by `--poll` - what CI runs. | yes |
| `--baseline` | Accept the existing translations as current (see [Baseline](#baseline)). | no |
| `--self-test` | Offline test suite: identity round-trip over the whole corpus, verifier/repair fixtures, and a fake-client end-to-end run of `--submit`/`--poll` in a temporary mini repo. Exits 1 on any failure; CI runs it on every PR. | no |
| `--probe` | Fetch the account's service-type names and language list, print them, and check `sourceLocale`, every `translatedLocale` and the resolved service type against them (exit 1 with the closest matches on a mismatch). | yes |
| `--dump-orders DIR` | Build the exact `/translate` request bodies through the same code path as `--submit` and write them to `DIR/{lang}/{rel}.json` plus `DIR/summary.json` (counts, characters, environment). Nothing is sent and the status file is not modified. | no |

Options:

| Option | Meaning |
|--------|---------|
| `--lang X` | Restrict to one language (repeatable). |
| `--file GLOB` | Restrict to files matching a glob relative to `content/` (repeatable). |
| `--limit N` | Submit at most N files per language. |
| `--wait MINUTES` | How long `--poll`/`--run` keep waiting for deliveries. |
| `--force` | Treat the files matched by `--file`/`--limit` as outdated even when they are current. With neither filter it means the whole corpus. |
| `--retry-failed` | Re-plan files whose recorded failure is at the current source hash (otherwise they are skipped until the English source changes). |
| `--lenient` | Write deliveries even when verification finds problems. For local inspection only; the workflow never passes it. |
| `--allow-unbounded` | Lift the sandbox caps. The workflow never passes it. |
| `--report PATH` | Write the Markdown run report (used as the PR body). |
| `--baseline-ref REF` | With `--baseline`: hash the English sources at this git ref (via `git show`) instead of the working tree. |
| `--overwrite-baseline` | With `--baseline`: allow overwriting a status file that already has `files` entries. |

## How a run works

1. **Plan.** Each English file's SHA-256 (line endings normalized) is compared with the entry in `localizedContent/{lang}/.translation-status.json`. Missing and outdated files are submitted. Files with `"manual": true` are skipped and reported as *pinned*. Files whose recorded failure is at the current source hash are skipped until `--retry-failed` or `--force`. Status entries that are neither in `sources`, `passthrough` nor orphans are reported as *unscoped* and dropped. Translations whose English source no longer exists (*orphans*) are deleted - only when no `--file`/`--limit` filter is active.
2. **Submit.** One order per file and language, in batches of `batchSize`; every batch carries an `x-idempotency-id` so a retry after a timeout or 5xx never creates duplicate (billed) requests. Markdown is sent as `text/markdown`; `toc.yml` is sent as a JSON map of its `name` values so hrefs never reach the translator; in `_ui-strings.json` every `{name}` placeholder is encoded as `{{name}}` (a syntax Translated protects) and decoded on delivery. The status file is saved after every accepted batch, so nothing Translated accepted is ever left unrecorded. A rejected batch records each of its files under `failures` with the API error and the run continues with the next batch and language, exiting 1 at the end. When a file is resubmitted while an older job for it is still in flight, the old job is cancelled and reported as *superseded*.
3. **Poll.** One status request per language per round, every 30 s backing off to 60 s and 120 s, until `--wait` minutes have passed. Job status `delivered` or `invoiced` means done; `failed`, `failed delivery` or `cancelled` means failed; everything else (including `completed`) means still waiting. Jobs pending for more than 7 days time out. Each pending job records the environment it was submitted in; pending jobs from another environment than the active one are dropped with a report line ("dropped: submitted in sandbox").
4. **Repair, then verify.** Every delivery is compared with its English source. Whatever can be aligned positionally is restored from English rather than trusted: fenced code blocks (fence lines and bodies), inline code spans, alert and include markers (`[!NOTE]`, `[!include]`), link targets, HTML `href`/`src` attributes, the BOM and the line-ending style, and every frontmatter key except `title`/`description`, which take the translated value (quoted when YAML needs it). What cannot be aligned is a verification problem: heading count differs; fence, inline-code, marker or link counts differ; HTML tag set differs; JSON key set or per-key placeholder set differs; a `toc.yml` key is missing or a value contains a newline; the source has frontmatter and the delivery does not; or the delivered text is identical to the English source. The report says what was repaired (`repaired: n fences, m inline code, k markers, j links`).
5. **What "failed" means.** A delivery with problems is *not* written: the existing translation stays untouched, the file is recorded under `failures` in the status file (with the reasons and the API status), listed in the report, and not resubmitted until the English source changes or `--retry-failed`/`--force` is given. `--lenient` writes it anyway, for local inspection only.
6. **Commit and PR.** The workflow commits `localizedContent` to the target branch and opens the PR, or comments the run report on the open one. Production runs use `localization`; sandbox runs use `localization-sandbox` and open a *draft* PR titled "New translations (sandbox - do not merge)" labelled `sandbox`. The report shows, per language, the files submitted, delivered, repaired (per kind), copied, superseded, dropped, still pending, failed and removed, plus billed word counts when the API returns them. `deploy.yml` builds a `localization` PR only when a review is requested, so review it, request a review to get a preview build, then merge.

## The workflow (`translate.yml`)

Two jobs:

- **`dry_run`** runs on pull requests that touch the workflow, `translate-content.py`, `config_loader.py`, `build-config.json` or `language-metadata.json`. It checks out the PR head and runs `--self-test`, `--plan` and `--dump-orders` (uploaded as an artifact, appended to the job summary). Adding the label `translate-sandbox-dryrun` to the PR - with the sandbox key configured - additionally runs `--run --force --limit 1 --file "features/toc.md" --lang es --wait 5` against the sandbox and uploads the report and a `translations.patch` with the resulting diff. It never pushes and never opens a PR.
- **`translate`** runs on `workflow_dispatch` always, and on `push` to `main` (paths `content/**`, `metadata/build-config.json`, `metadata/language-metadata.json`, `translate-content.py`, `config_loader.py`, the workflow itself) and on the six-hourly schedule (`17 */6 * * *`) only when the repository variable `TRANSLATED_ENV` is `production`. Until then the automatic triggers are inert; a missing key or environment produces a warning, not a red run. Dispatch inputs: `mode` (`translate` | `probe` | `dry-run`), `target_branch` (default `localization`; refused when `TRANSLATED_ENV` is not `production`), `limit`, `wait`, `force` and `file`. The job merges the open translation branch into main's tree first (after deleting a stale branch whose PR was already merged or closed), runs `--self-test`, then `--run --wait <wait> --limit <limit> [--force] [--file <glob>] --report ...`, then pushes and opens or updates the PR. In `dry-run` mode it runs but skips push and PR; in `probe` mode it runs `--probe` only. The full report is always uploaded as an artifact and appended to the job summary.

Secrets and settings: `TRANSLATED_API_KEY` (repository secret), `TRANSLATED_ENV` and `TRANSLATED_SERVICE_TYPE` (repository variables), *Allow GitHub Actions to create and approve pull requests* enabled under Settings > Actions > General, and *Automatically delete head branches* enabled under Settings > General.

## Sandbox caps

With `TRANSLATED_ENV=sandbox` a run refuses (with the counts) to submit more than `sandboxLimits.maxFilesPerRun` files or `maxCharsPerRun` characters, and requires `--limit` or `--file`, unless `--allow-unbounded` is given. Translated blocks sandbox keys for excessive use of the human-translation workflow, and the sandbox `premium` service type is that workflow. Sandbox output is throwaway machine translation: never merge a sandbox PR and never commit sandbox translations from a local run.

## Local use

```bash
python build_scripts/translate-content.py --self-test                       # offline checks (no key)
python build_scripts/translate-content.py --plan                            # what would be sent, and how many characters
python build_scripts/translate-content.py --dump-orders /tmp/orders         # the exact request bodies; nothing is sent
export TRANSLATED_ENV=sandbox TRANSLATED_API_KEY=...                        # PowerShell: $env:TRANSLATED_ENV = "sandbox"
python build_scripts/translate-content.py --probe                           # key, endpoint, locales and service type
python build_scripts/translate-content.py --submit --lang es --limit 3      # send a few files
python build_scripts/translate-content.py --poll --wait 10 --report r.md    # collect deliveries
python build_scripts/translate-content.py --run --wait 25 --report r.md     # what CI does
```

Afterwards discard the sandbox output with `git checkout -- localizedContent` (a plain `git diff --stat` first shows what a real run would have changed).

## Baseline

`--baseline` was used once when migrating from the previous provider, and is the way to (re)seed a status file. For every scoped source with an existing translation it runs the verification step (no repair) between English and the existing translation: files that verify are recorded as `translated` at the English hash (taken from `--baseline-ref REF` when given, so pages edited since that ref are re-translated on the first run); files with problems are recorded as `untranslated` with an empty hash and the reason is printed, so they are submitted on the first run; missing targets are `untranslated`. Unscoped entries are dropped and passthrough entries are left alone. It refuses to run when the status file already has `files` entries unless `--overwrite-baseline` is given, and prints a per-language summary including the files it marked outdated and why.

## Status file

`localizedContent/{lang}/.translation-status.json` is owned by `translate-content.py` and committed with the translations. It holds `language`, `sourceBaseline`, `files` (per file: `sourceHash`, `status` = `translated` | `untranslated` | `copied`, and optionally `"manual": true`), `pendingJobs` and `failures` (present only when non-empty), and `summary` (counts including `copied`, `pinned`, `pendingJobs`, `failures`). `build-docs.py --sync` reads it but never writes it.

## Runbook

- **Fix a translation.** While the translation PR is open, push the fix to its branch (`localization`); the next run merges that branch before doing anything else, so the fix survives. After the PR is merged, edit the file on `main` through a normal PR. Either way the file is overwritten by the next machine translation when its English source changes, unless you pin it.
- **Pin (skip) a file.** Add `"manual": true` to the file's entry in `localizedContent/{lang}/.translation-status.json`. Pinned files are reported and never submitted or overwritten; remove the flag to hand the file back to the workflow.
- **Re-translate one file.** Dispatch `translate.yml` with `force=true` and `file=features/dax-query.md` (and `limit` as needed), or locally: `python build_scripts/translate-content.py --run --force --file "features/dax-query.md" --lang es --wait 10 --report r.md`. Local runs use whatever `TRANSLATED_ENV` says; only commit output from production.
- **A file failed.** The report and the `failures` entry list the reasons (for example "heading count differs" or "delivered content identical to source"). Usually the English source has a structure the translator cannot preserve: fix the English, and the changed hash resubmits the file on the next run (or use `--retry-failed` to try again unchanged). If the delivery is acceptable despite the problems, fetch it locally with `--run --force --file <rel> --lang <lang> --lenient --report r.md`, review the written file, and commit it through a normal PR.
- **Switch sandbox -> production.** (1) Replace the `TRANSLATED_API_KEY` secret with the production key. (2) Set the repository variable `TRANSLATED_ENV` to `production`; from now on the automatic triggers are live. (3) Dispatch `translate.yml` with `mode=probe`: it prints the account's service types and confirms `en-US`, `es-ES` and `zh-CN`. (4) Set the repository variable `TRANSLATED_SERVICE_TYPE` to the chosen service type (production refuses to run without one) and run the probe again. (5) Dispatch with `limit=3`, `force=true`, `file=features/toc.md` and the default `target_branch`; review the PR, request a review to get a preview build, merge. Afterwards record the service type in `build-config.json` (`environments.production.serviceType`) in a follow-up PR.
- **Stale-branch cleanup.** Before merging the translation branch into its tree, the workflow checks whether the branch tip is already contained in `main` or its PR is merged or closed (`gh pr list --head <branch> --state merged` / `--state closed`). If so it deletes the remote branch and starts from `main`, so a squash-merged translation PR never produces an empty follow-up PR. *Automatically delete head branches* makes this the normal path. Closing a translation PR without merging does not discard anything: the next run merges the branch again. To discard its content, delete the branch - the pending-job records on it are lost too, so those files are resubmitted (and billed) on the next run.

# Bookmark Links and Translations

When linking to a specific heading within a page (e.g., `#my-heading`), DocFX auto-generates the anchor ID from the heading **text**. Because translation changes that text, the generated anchor changes per language (`#model-io` becomes `#es-del-modelo`, etc.), so a hardcoded English `#anchor` link breaks in every translated page and DocFX logs an `InvalidBookmark` warning. English builds stay clean because the anchors match there.

## Automatic anchor stabilization (the build handles this)

`build_scripts/normalize-localized-heading-anchors.py` neutralizes this whole class of warning automatically. For each localized page it reads the matching English source, computes each heading's English slug, and injects a hidden bookmark anchor carrying that slug immediately before the corresponding translated heading:

```markdown
<a id="model-io" data-loc-xref></a>
## E/S del modelo
```

DocFX accepts the injected `id` as a valid bookmark, so `#model-io` resolves and the link lands on the right section while the heading keeps its translated text. Headings are aligned to the English source positionally; this is safe because the translation script rejects deliveries whose heading count differs from the English source. If the heading counts differ anyway (a stale or hand-edited translation), the file is skipped and reported rather than risk a misaligned anchor. The script is idempotent (it strips its own `data-loc-xref` anchors before recomputing) and never modifies English.

The build runs it automatically for each non-English language before DocFX (step 5 of [What the Build Script Does](#what-the-build-script-does)). You can also run it manually after merging a translation PR:

```bash
python build_scripts/normalize-localized-heading-anchors.py            # all languages
python build_scripts/normalize-localized-heading-anchors.py --dry-run  # preview without writing
python build_scripts/normalize-localized-heading-anchors.py --check    # exit 1 if changes are needed (CI)
python build_scripts/normalize-localized-heading-anchors.py es         # a single language
```

## Authoring guidance

- **Prefer the bracketed link form** `[text](xref:uid#anchor)` over the bare `@uid#anchor` autolink. The closing `)` delimits the anchor, so trailing punctuation in any language can never leak into it.
- **For a rename-proof anchor**, add an explicit `<a name="..."></a>` tag above the heading. Translators and machine translation leave HTML `name` attributes alone (and the translation script restores HTML attributes from English), so the anchor stays stable across all languages *and* survives English heading renames — unlike an auto-generated slug. Only add these to headings actually linked to; there is no need to add them everywhere.

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

Some translation exports collapse the two lines into one when an alert like this is nested inside a list item, producing `> [!NOTE]> Your note text here.`. DocFX requires the marker to be alone on its line, so the collapsed form is downgraded to a plain `<blockquote>` — losing the styled box — and the build logs an `invalid-note-section` warning. Only list-nested alerts are affected; top-level alerts round-trip unchanged.

`build_scripts/normalize-localized-alerts.py` repairs this by splitting the collapsed form back into two lines, preserving the original indentation so the alert stays inside its list item. It is a safety net for translator output: the translation script already restores alert markers from English, but older translations and hand edits can still carry the collapsed form. It is idempotent and only rewrites the exact collapsed pattern (text inside fenced code blocks is left untouched), so it is safe to run repeatedly.

The build runs it automatically for each non-English language before DocFX (step 4 of [What the Build Script Does](#what-the-build-script-does)). You can also run it manually after merging a translation PR:

```bash
python build_scripts/normalize-localized-alerts.py            # fix all languages
python build_scripts/normalize-localized-alerts.py --dry-run  # preview without writing
python build_scripts/normalize-localized-alerts.py --check    # exit 1 if fixes are needed (CI)
python build_scripts/normalize-localized-alerts.py es         # fix a single language
```

# Translating UI Strings

The `_ui-strings.json` file controls the text of site-wide UI elements that are not part of the documentation content itself: the header navigation, header buttons, footer text, and the AI translation warning banner. These strings are applied at runtime by the JavaScript bundle for non-English pages.

The English source is at `content/_ui-strings.json`. For existing languages the translated file `localizedContent/{lang}/content/_ui-strings.json` is produced by the automated translation workflow like any other source file (see [Translating Content](#translating-content)): the run encodes `{placeholder}` tokens so the translator leaves them alone and rejects a delivery whose key set or placeholders differ from English. For a new language you can also seed the file by hand with the same keys and translated values.

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
