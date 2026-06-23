---
uid: te-cli-automation
title: Automation and Scripting
author: Peer Grønnerup
updated: 2026-06-11
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      none: true
    - product: Tabular Editor CLI
      full: true
---
# Automation and Scripting

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

The Tabular Editor CLI is composable; every command supports structured output, disables interactive prompts on demand, and returns predictable exit codes. The same primitives work equally well for shell pipelines, Python scripts, PowerShell automation, and agent-driven workflows.

## Structured output

Use `--output-format` to switch any command between text (human-readable) and machine-readable formats:

| Format | Use for | Notes |
| -- | -- | -- |
| `text` (default) | Human-readable use | Plain text on stdout regardless of whether the stream is a TTY or piped. |
| `json` | Machine-readable use | Always valid JSON to stdout. Use `--error-format json` if you also want machine-readable errors on stderr. |
| `csv` | Tabular results (`query`, `bpa run`, `bpa rules`, `vertipaq`, `validate`, `test`, `refresh`, `profile list`, `session list`, `find`, `replace`, `get`, `ls`) | RFC 4180 escaping. |
| `tmsl` (alias `bim`) | Whole-object TMSL/BIM serialization | Accepted by `te get` and `te ls`. |
| `tmdl` | Whole-object TMDL serialization | Accepted by `te get` only (single object). |

```bash
te ls --output-format json
te query -q "EVALUATE VALUES('Date'[Year])" --output-format csv
te bpa run --output-format json
```

> [!NOTE]
> `--output-format` and `--error-format` are independent. Setting `--output-format json` does *not* switch stderr to JSON; pass `--error-format json` for that. There is no automatic format switching when stdout is redirected - the default is always `text` unless you ask otherwise.

## Non-interactive mode

Add `--non-interactive` to any command to disable confirmation prompts, credential picklists, and guided wizards. If the command needs input it cannot resolve from flags, environment, or config, it exits non-zero with an actionable error instead of hanging.

```bash
te deploy ./model --non-interactive --force --ci github
```

## Exit codes

Every `te` command exits with a predictable status code so callers can branch on success or failure without parsing stdout.

| Exit | Meaning |
| -- | -- |
| `0` | Success. |
| `1` | Generic failure - invalid arguments, command failed, validation errors, auth failure, BPA gate failed at severity ≥ error. For `te diff`: differences found (like the `diff`/`cmp` convention). |
| `2` | `te diff` only: an error occurred while comparing, so the difference status is unknown. |

Combine exit codes with `--ci <vsts\|github>` annotations and `--trx <file>` to surface rich failure information in CI - see @te-cli-cicd.

## Errors on stderr

Errors, warnings, and the preview banner are written to **stderr**; structured data is written to **stdout**. This means you can pipe JSON safely without it being contaminated by progress indicators or diagnostic messages:

```bash
te ls --output-format json | jq '.[] | .name'
te vertipaq --output-format json > stats.json
```

## Python

Python is a natural host for orchestrating CLI calls from data pipelines, notebooks, or test harnesses. Invoke `te` with `subprocess.run`, request JSON, and parse stdout:

```python
import json
import subprocess

def query(server: str, database: str, dax: str) -> list[dict]:
    result = subprocess.run(
        ["te", "query",
         "-s", server,
         "-d", database,
         "-q", dax,
         "--output-format", "json",
         "--non-interactive"],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)

rows = query("Finance", "Revenue Model", "EVALUATE TOPN(10, 'Sales')")
for row in rows:
    print(row)
```

To capture structured errors from stderr:

```python
import json
import subprocess

result = subprocess.run(
    ["te", "deploy", "./model",
     "-s", "Finance", "-d", "Revenue",
     "--output-format", "json", "--non-interactive", "--force"],
    capture_output=True, text=True,
)

if result.returncode != 0:
    try:
        err = json.loads(result.stderr.strip().splitlines()[-1])
        print("Deploy failed:", err.get("error"), "- hint:", err.get("hint"))
    except json.JSONDecodeError:
        print("Deploy failed:\n", result.stderr)
```

## PowerShell

PowerShell handles JSON natively. `te` is a regular console binary that works directly in PowerShell pipelines (see @te-cli-migrate if you're porting from the older `TabularEditor.exe` CLI):

```powershell
$rows = te query -s Finance -d Revenue -q "EVALUATE TOPN(10, 'Sales')" --output-format json --non-interactive
  | ConvertFrom-Json

$rows | Format-Table

# Check exit code after the pipeline
if ($LASTEXITCODE -ne 0) {
    Write-Error "Query failed with exit $LASTEXITCODE"
    exit $LASTEXITCODE
}
```

Read secrets from the environment rather than passing them as plaintext:

```powershell
$env:AZURE_CLIENT_ID     = "your-app-id"
$env:AZURE_CLIENT_SECRET = "your-client-secret"
$env:AZURE_TENANT_ID     = "your-tenant-id"

te deploy ./model `
  -s my-workspace -d my-model `
  --auth env --non-interactive --force --ci vsts
```

## Bash

Compose commands with pipes and `jq`. The CLI's text output is colorized for humans, but switching to `--output-format json` gives you a clean shape to work with:

```bash
# Count measures per table
te ls --type measure --output-format json \
  | jq -r '.[] | .table' \
  | sort | uniq -c | sort -rn
```

```bash
# Fail the shell script if BPA finds any errors
te bpa run --fail-on error --output-format json > bpa.json \
  || { echo "BPA gate failed"; jq '.violations' bpa.json; exit 1; }
```

## Composability example

Generating a refresh TMSL script and version-controlling it is three commands:

```bash
te connect MyWorkspace MyModel
te refresh --type full --dry-run > refresh.tmsl
cat refresh.tmsl
```

The resulting TMSL can be reviewed in a pull request, committed, executed by the CLI (`te refresh --type full`), handed to a DBA, or applied by any XMLA-compatible tool. The CLI becomes a building block rather than a black box.

## Useful patterns

A handful of small idioms that come up often when composing `te` commands in scripts or pipelines:

- **Idempotent creates and removes.** `te add Sales/Marker -t Measure -i "0" --if-not-exists --save` and `te rm Sales/OldMeasure --if-exists --save` both exit `0` whether or not the object existed - safe to re-run in CI.
- **Dry-run diffs.** `te replace` is dry-run by default; add `--save` only when you're satisfied with the preview.
- **Emit TMSL for review.** `te deploy ./model --xmla deploy.tmsl` produces the deployment script without touching the server - useful for DBA review or manual apply.
- **Path-only output.** `te ls --paths-only` and `te find --paths-only` emit one object path per line, ideal for piping to `xargs`, `te get`, or `te set`. The model-level containers (`te ls Measures`, `te ls Columns`) compose well with this for whole-model sweeps.
- **Benchmarking queries.** `te query --trace --cold --runs 5` runs a DAX query with cold cache, five iterations, and captures FE/SE trace events.
- **Step timings in CI logs.** Long-running commands (`te deploy`, `te refresh`, `te script`, `te validate`) include a `durationMs` field in JSON output - useful for surfacing per-step timings in pipeline summaries.

## Related pages 

- @te-cli-cicd - pipeline-specific patterns and YAML examples.
- @te-cli-commands - full command reference.
- @te-cli-interactive - when interactive mode fits better than scripting.
