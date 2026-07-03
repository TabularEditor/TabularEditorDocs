# Build tools

All Python build scripts are linted and type-checked :

```shell
$ uvx ruff check --select F,B,SIM,I,UP  <python_sources>
$ uvx mypy --strict  <python_sources>
```

## Doc validation

### Code block validation and output generation

`te_script_runner.py` and `csharp_doctest.py` contribute to validating code blocks in docs.
Both need `te` on PATH.

Current state only validates semantic bridge docs.

#### `te_script_runner.py` -- generic runner

Runs (or compile-checks) C# snippets against a throwaway, empty `.bim` model.
stdout = the snippets' `Output()`; stderr = te's own stderr

```shell
$ te_script_runner.py run   -e '<expr>'    # execute (also -f <file>, or stdin)
$ te_script_runner.py check -e '<expr>'    # compile only (te --dry-run)
$ te_script_runner.py run -e '<expr1>' -f <file1> -e '<expr2> # execute multiple scripts in order; also works for `check`
```

Importable: `run_snippets(snippets, dry_run=..., last_only=...) -> Result`.
Snippets run in order in one te session,
so state (a loaded Metric View, model mutations) carries across them;
`last_only` reports only the final snippet's `Output()`.

#### `csharp_doctest.py` -- doc orchestrator

Checks annotated C# fences in a markdown file.
The annotation is invisible in rendered docfx output:

```
    ```csharp {compile}
    ```csharp {run id=<slug> setup=<mv-sample|none> after=<id,...|none> output=<true|false>}
```

- Unannotated csharp fence = skip.
- `{compile}` = compile-check only (catches API drift; never executes).
- `output=true` = the immediately-following plain fence is the expected output.
- `setup` prepends a preamble (see `SETUP_SCRIPTS`, e.g. the sample Metric View).
- `after` replays earlier run blocks for their state only (not their output).

The grammar for these `run` blocks is explicit:
every option must be provided in every block.

Commands (each validates first and bails on a malformed doc):

```shell
$ csharp_doctest.py validate <file>   # grammar + coverage counts, no CLI calls
$ csharp_doctest.py compile  <file>   # compile every {compile}/{run} block
$ csharp_doctest.py compare  <file>   # diff each {run} Output() against its fence
$ csharp_doctest.py update   <file>   # run {run} blocks, rewrite output blocks in place
```

Exits non-zero on any failure.
stdout = the report (verdicts + diffs);
stderr = te's stderr and harness/operational errors.

Sweep all docs with annotated code blocks for valid annotations, bailing on first error:

```shell
$ (set -eu; rg '```csharp \{' --glob content/**/*.md --files-with-matches | while read f; do python3 build_scripts/csharp_doctest.py validate $f; done)
```

Substitute `compile`, `compare`, or `update` for `validate` in above to run in the same way (bailing on first error).

This orchestrator uses a thread pool with a thread per code block.
Each invocation of `te` as a sub-process takes ~1-2s,
so parallelizing nets a significant performance gain.

#### Test fixtures (`test-fixtures/`)

Small, self-contained inputs that exercise each code path---a manual regression corpus you run by hand (there are no unit tests).
Run a command against a fixture and eyeball the result.

Markdown fixtures drive `csharp_doctest.py`:
- `doc-valid.md`: one of every block kind (skip / `{compile}` / `{run}`); everything passes.
- `doc-mismatch.md`: a `{run}` whose `Output()` differs from its fence, so `compare` fails (and `update` would rewrite it; don't call update and commit, instead revert if you do update).
- `doc-compile-drift.md`: a `{run}` calling a nonexistent API, so `compile` fails.
- `err-*.md`: each holds exactly one grammar error (missing option, no output fence, annotation on a non-csharp fence, unknown `after=`, unknown annotation), so `validate` bails.

`te-*.json` are canned `te --output-format json` outputs that drive `te_script_runner.py summarize` (its pure parser, no `te` needed):
the executed-run and `--dry-run` schemas, each in a success and a failure (compile / runtime) variant.

```shell
$ csharp_doctest.py validate test-fixtures/doc-valid.md          # passes
$ csharp_doctest.py compare  test-fixtures/doc-mismatch.md       # fails with a diff (nonzero exit)
$ csharp_doctest.py compile  test-fixtures/doc-compile-drift.md  # fails on the drifted API
$ csharp_doctest.py validate test-fixtures/err-unknown-after.md  # bails with the grammar error
$ te_script_runner.py summarize test-fixtures/te-runtime-error.json
```

### Link validation

`check_links.py` validates all links (`href`/`src`) in the built `_site`.
It walks the generated HTML,
resolves each reference to a local file or an external URL,
visits every unique target once, and reports references to broken targets.

Broken link checks:
- local links (to something defined in this docs repo): the target file must exist
  - detect old root links (e.g. `<a href="/Advanced-Scripting" ...>`) and resolve against the live docs site to check redirects; a dead one is an error, not a warning
- external links (to something not defined in this docs repo): must return a 2xx/3xx status -- a bad status (e.g. 404) or a transport error (DNS, TLS/certificate, timeout, refused connection) fails
- fragments: ensure the `#anchor` is defined in the body of the target page (local file or fetched external page)
- text links: ensure the literal `:~:text=` string is in the body of the target page (local file or fetched external page)

Internal failures are errors (nonzero exit) -- own-site links, i.e. local files and root-absolute links (the latter checked over HTTP).
External failures are warnings (network issues may be transient, or the target blocks bots),
listed as a set of URLs to verify by hand.

```shell
$ check_links.py validate                  # check _site: authored content, on-disk + external
$ check_links.py validate local            # on-disk checks only, skip external fetching
$ check_links.py validate all              # also include generated API and localized pages
$ check_links.py validate stats            # add per-host external-fetch diagnostics
$ check_links.py validate _site under=en   # only check links from pages under _site/en
```

- `local` = skip external URL fetching (on-disk checks only).
- `all` = include generated API and localized pages (default: authored `content/*.md` only).
- `stats` = print per-host external-fetch diagnostics.
- `under=<subpath>` = only check links from pages under `<root>/<subpath>`.

`extract`, `resolve`, `enumerate`, and `fetch` expose the internal stages for testing.

This script uses a rudimentary scheduler to avoid flooding a single host and getting a 429 storm.
We distribute work across a thread pool and the scheduler interleaves requests to different hosts.
There is a per-host maximum for in-flight requests,
and a per-host cooldown when we encounter 429s,
to avoid slamming a host that has already told us to back off.
On a 429 we honor `Retry-After` (otherwise exponential backoff: 1, 2, 4, ... seconds)
and also decrement that host's in-flight cap as ongoing backpressure;
after a per-URL retry limit we give up and record the last result.

Reachability uses a `HEAD` request;
a body-downloading `GET` runs only when a fragment or `:~:text=` directive must be verified,
so it never pulls installers or images just to check a link.
A failed `HEAD` falls back to `GET` (some hosts reject `HEAD`),
and known HEAD-hostile hosts skip straight to `GET`.

Including `stats` will show per-host statistics: `python3 build_scripts/check_links.py validate stats`.
