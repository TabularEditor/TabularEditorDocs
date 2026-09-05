---
uid: te-cli-findings
title: Findings JSON
author: Peer Grønnerup
updated: 2026-09-04
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      none: true
    - product: Tabular Editor CLI
      full: true
---
# Findings JSON

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

`te validate`, `te bpa run`, `te test run`, and `te query` report problems in one shared JSON shape, so a pipeline that gates on more than one of them needs one parser instead of four. Under `--output-format json`, each of these commands emits a **single document** - there is no way for one of them to leave nothing to parse.

> [!NOTE]
> `te query` emits the findings envelope only when its pre-execution DAX validation produces at least one error. A successful query emits the query result instead: `{columns, rows, rowCount, truncated, durationMs, trace?}`.

## The envelope

```json
{
  "command": "validate",
  "durationMs": 412,
  "summary": { "errors": 1, "warnings": 2, "info": 0, "total": 3 },
  "findings": [
    {
      "severity": "error",
      "source": "validate",
      "code": "TE0001",
      "message": "Unknown column 'Sales'[Amt]",
      "object": "Revenue",
      "objectType": "Measure",
      "objectPath": "Sales/Revenue",
      "expressionPosition": { "property": "Expression", "lineNumber": 3, "column": 9 },
      "fixable": false
    }
  ],
  "valid": false
}
```

- `command` - which command produced the document.
- `durationMs` - total run duration.
- `summary` - severity tally: `errors`, `warnings`, `info`, `total`.
- `findings` - one flat array, discriminated by `severity`.

## Per-finding keys

Present on **every** finding:

| Key | Values / meaning |
| -- | -- |
| `severity` | `error`, `warning`, or `info`. |
| `source` | `validate`, `bpa`, `test`, or `query`. |
| `code` | Stable finding code (a validation message ID, BPA rule ID, `TEST_FAIL` / `TEST_ERROR` / `TEST_SUITE_INVALID`, ...). |
| `message` | Human-readable description. |
| `object` | Bare name of the object the finding is about. |
| `objectType` | One of a closed vocabulary - see below. |
| `fixable` | `true` only for BPA violations whose rule defines a fix expression. |

Present **only where the CLI knows them** - these keys are *absent* rather than `null` when unset:

| Key | Populated by | Meaning |
| -- | -- | -- |
| `objectPath` | `validate` and `bpa` violations only | Canonical object path, resolvable as-is by `te get` or `te set`. Absent for test findings, query findings, and BPA rule errors. |
| `expressionPosition` | `validate` and `query` only | `{property, lineNumber, column}` inside the named expression property. **Optional on every source, including validate and query** - absent whenever the analyzer reported no usable position, and all-or-nothing (never a partial position). |
| `ruleName`, `category` | `bpa` only | The violated rule's name and category. |

### objectType vocabulary

The closed set of `objectType` values (the singular forms of the path-grammar containers, not a TOM enum):

`Measure`, `Column`, `Hierarchy`, `Level`, `Partition`, `CalculationItem`, `Table`, `Role`, `TablePermission`, `Perspective`, `Culture`, `DataSource`, `Expression`, `Function`, `Relationship`, `KPI`, `RefreshPolicy`, `Member`, `Calendar`, `Variation`, `Model`, `BpaRule`, `Test`, `TestSuite`, `Query`.

## Per-command extras

Each command keeps a few keys of its own at the top level of the envelope:

| Command | Extra keys |
| -- | -- |
| `te validate` | `valid` (boolean). |
| `te bpa run` | `model`, `rulesEvaluated`, `violations`, `ruleErrors`, `ignoredRules`. Rule-evaluation errors appear in `findings` at severity `error` with `objectType: "BpaRule"` - `violations` and `ruleErrors` split the two counts. |
| `te bpa run --fix` | A `fix` key inside the same single document: `changes`, `fixed`, `fixErrors`, `skipped`, `fixedItems`, `fixErrorItems`. If the fix pass itself fails, the envelope is still written with the reason in `fix.error`. Absent without `--fix`. |
| `te test run` | `suites`, `invalidSuites`, `testSummary` (per-status test tallies; `summary` remains the shared severity tally). |
| `te query` | None - and only on validation errors; see the note above. |

## CI annotations

All four commands share one annotation writer for `--ci vsts` / `--ci github` (annotations go to stderr; stdout stays parseable):

- Annotations carry the finding's code: `code=` on Azure DevOps, `title=` on GitHub.
- Info-severity findings are not warnings: on GitHub they emit `::notice::`, on Azure DevOps a plain log line. An Azure DevOps run whose only findings are informational reports **Succeeded**.
- Multi-line messages are escaped into a single annotation line, so a rule description cannot break the log format.

## Related pages

- @te-cli-commands#exit-codes - exit codes are unaffected by the output format.
- @te-cli-cicd - pipeline patterns that consume this shape.
- @te-cli-automation - parsing structured output from scripts.
