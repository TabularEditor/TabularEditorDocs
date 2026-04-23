---
uid: te-cli-automation
title: Automation and Scripting
author: Peer Grønnerup
updated: 2026-04-20
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

The Tabular Editor CLI is designed as a composable building block. Every command supports structured output, disables interactive prompts on demand, and returns predictable exit codes. The same primitives work equally well for shell pipelines, Python scripts, PowerShell automation, and agent-driven workflows.

## Structured output

Use `--output` to switch any command between text (human-readable) and machine-readable formats:

| Format | Use for | Notes |
| -- | -- | -- |
| `auto` (default) | General use | Text for TTY, JSON when stdout is piped or redirected. |
| `text` | Force text output | Useful when you want text in a CI log. |
| `json` | Programmatic consumers | Always valid JSON to stdout; errors and warnings go to stderr as separate JSON objects. |
| `csv` | Tabular results (`query`, `bpa`, `vertipaq`) | RFC 4180 escaping. |

```bash
te ls --output json
te query -q "EVALUATE VALUES('Date'[Year])" --output csv
te bpa run --output json
```

> [!TIP]
> When stdout is piped, `auto` already emits JSON. Explicit `--output json` is only necessary when you want JSON on a TTY, or when a consumer expects it regardless of how the command is invoked.

## Non-interactive mode

Add `--non-interactive` to any command to disable confirmation prompts, credential picklists, and guided wizards. If the command needs input it cannot resolve from flags, environment, or config, it exits non-zero with an actionable error instead of hanging.

```bash
te deploy ./model --non-interactive --force --ci github
```

## Exit codes

| Exit | Meaning |
| -- | -- |
| `0` | Success. |
| `1` | Generic failure — invalid arguments, command failed, validation errors, auth failure, BPA gate failed at severity ≥ error. |
| `2` | Used by `te diff` to indicate models differ (distinct from `0` identical and non-zero errors). |

Combine exit codes with `--ci <vsts\|github>` annotations and `--trx <file>` to surface rich failure information in CI — see @te-cli-cicd.

## Errors on stderr

Errors, warnings, and the preview banner are written to **stderr**; structured data is written to **stdout**. This means you can pipe JSON safely without it being contaminated by progress indicators or diagnostic messages:

```bash
te ls --output json | jq '.[] | .name'
te vertipaq --output json > stats.json
```

## Python

Invoke the CLI from Python with `subprocess.run`, request JSON, and parse stdout:

```python
import json
import subprocess

def query(server: str, database: str, dax: str) -> list[dict]:
    result = subprocess.run(
        ["te", "query",
         "-s", server,
         "-d", database,
         "-q", dax,
         "--output", "json",
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

Capture structured errors from stderr:

```python
import json
import subprocess

result = subprocess.run(
    ["te", "deploy", "./model",
     "-s", "Finance", "-d", "Revenue",
     "--output", "json", "--non-interactive", "--force"],
    capture_output=True, text=True,
)

if result.returncode != 0:
    try:
        err = json.loads(result.stderr.strip().splitlines()[-1])
        print("Deploy failed:", err.get("error"), "— hint:", err.get("hint"))
    except json.JSONDecodeError:
        print("Deploy failed:\n", result.stderr)
```

## PowerShell

PowerShell handles JSON natively. Because `te` is a normal console binary, there is no need for the `start /wait` dance required by `TabularEditor.exe`:

```powershell
$rows = te query -s Finance -d Revenue -q "EVALUATE TOPN(10, 'Sales')" --output json --non-interactive
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
$env:AZURE_CLIENT_ID     = "<app-id>"
$env:AZURE_CLIENT_SECRET = "<secret>"
$env:AZURE_TENANT_ID     = "<tenant>"

te deploy ./model `
  -s my-workspace -d my-model `
  --auth env --non-interactive --force --ci vsts
```

## Bash

Compose commands with pipes and `jq`. The CLI's text output is colorized for humans, but switching to `--output json` gives you a clean shape to work with:

```bash
# Count measures per table
te ls --type measure --output json \
  | jq -r '.[] | .table' \
  | sort | uniq -c | sort -rn
```

```bash
# Fail the shell script if BPA finds any errors
te bpa run --fail-on error --output json > bpa.json \
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

- **Idempotent removes.** `te rm Sales/OldMeasure --if-exists --save` exits `0` whether or not the object existed — safe to re-run.
- **Dry-run diffs.** `te replace` is dry-run by default; add `--save` only when you're satisfied with the preview.
- **Emit TMSL for review.** `te deploy ./model --xmla deploy.tmsl` produces the deployment script without touching the server — useful for DBA review or manual apply.
- **Path-only output.** `te ls --paths-only` and `te find --paths-only` emit one object path per line, ideal for piping to `xargs`, `te get`, or `te set`.
- **Benchmarking queries.** `te query --trace --cold --runs 5` runs a DAX query with cold cache, five iterations, and captures FE/SE trace events.

## Related pages

- @te-cli-cicd — pipeline-specific patterns and YAML examples.
- @te-cli-commands — full command reference.
- @te-cli-interactive — when interactive mode fits better than scripting.
