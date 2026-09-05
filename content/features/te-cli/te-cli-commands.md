---
uid: te-cli-commands
title: Command Reference
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
# Command Reference

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]
 
This page gives a short description and one example per command. Every command accepts `--help` for exhaustive flag documentation:

```bash
te deploy --help            # Help for a single command
te bpa run --help           # Help for a command with subcommands
```

> [!NOTE]
> During preview, the CLI's `--help` output is the authoritative reference for flags and options. The content on this page is hand-curated and will lag `--help` for anything added between preview releases.

## Object paths

Object addressing in the CLI uses a single grammar that's shared across every command. Two flavours of path appear in the reference below:

- **`<path>`** - resolves to **exactly one** object or container. Used by commands that operate on a single target: `te get`, `te set`, `te add`, `te remove`, `te move`, `te deps`, `te macro run --on`.
- **`<path-filter>`** - resolves to **zero or more** objects, with wildcard support. Used by commands that operate on a set: `te list`, `te bpa run --path`, and other inspection-style commands.

Both path forms share the same syntax rules; they differ in only two places:

- Filter paths allow `*` wildcards; object paths do not.
- Object paths allow DAX bracket-suffix (e.g. `Sales[Amount]`); filter paths do not.

### Segments and separators

A path is a slash-separated sequence of **segments**. Each segment names a single step - a table, a child object, or a container keyword.

- `Sales` - one segment
- `Sales/Revenue` - two segments
- `Roles/Admin/Members/bob` - four segments

Empty input and `.` both mean "the model root" - the implicit starting point for filter paths and the explicit subject for `te get .`-style queries.

### Quoting

Most segment names work as-is. Quote a segment when its name contains spaces, slashes, brackets, or any character that would otherwise be parsed as syntax. The CLI follows DAX quoting conventions, so quoting in `te` paths matches what you'd type inside a DAX expression:

| Form | Use for | Escape rule |
| -- | -- | -- |
| `'Net Sales'` | Tables, named objects with spaces. | Double the quote (`'Bob''s'` → `Bob's`). |
| `"Net Sales"` | Same as above; cross-shell convenience when single-quote escaping is awkward. | Double the quote (`"He said ""hi"""` → `He said "hi"`). |
| `[Sales Amount]` | DAX bracket-suffix on a table (`'Sales'[Sales Amount]`) or a lone-bracket model-wide reference (`[Total Sales]`). Object paths only. | Double the closing bracket (`[foo]]bar]` → `foo]bar`). |

Inside quoted segments, `*` is treated as a literal character, not a wildcard. So `'Sa*'` matches a table named exactly `Sa*`.

The reserved characters in paths are `/ [ ] ' " * ? { }`. A segment containing any of `* ? { }` must be quoted (`te get "Tables/'{foo}'"`, `te get 'Sales/"my*name"'`); unquoted use is rejected with an error naming the character and showing the quoted form. `?` is reserved and has no wildcard meaning. Every path the CLI prints - in errors, hints, `--paths-only` output, and the `objectPath` field in JSON - is canonically quoted and can be pasted straight back into `te get`. The mixed-quote forms require PowerShell or bash; cmd.exe cannot express them.

### DAX-style references (object paths only)

Two DAX-shaped forms are accepted anywhere a `<path>` is allowed:

- **`'Table'[Member]`** - equivalent to `Table/Member`. The bracket-suffix biases ambiguous matches toward columns and measures over hierarchies/partitions.
- **`[Member]`** - a *lone* measure or column, with no preceding table. Searches the whole model for a measure or column with that name. Measures win when both exist.

```bash
te get "'Sales'[Amount]"             # Same as te get Sales/Amount
te get "'Net Sales'[Sales Amount]"   # Spaced names via DAX form
te get "[Total Sales]"               # Model-wide measure-or-column lookup
```

### Containers and keywords

Several names act as container keywords. A keyword can stand alone (listing the whole container) or appear inside a path (jumping into that sub-collection on the current parent).

| Keyword | Scope | Meaning |
| -- | -- | -- |
| `Tables`, `Measures`, `Columns`, `Hierarchies`, `Partitions`, `KPIs`, `Sets` | Model | All objects of that kind across the model. |
| `Relationships`, `Roles`, `Perspectives`, `Cultures`, `DataSources`, `Expressions`, `CalculationGroups`, `Functions`, `Annotations` | Model | Model-level containers. |
| `Measures`, `Columns`, `Hierarchies`, `Partitions`, `Calendars`, `CalculationItems`, `KPIs`, `Sets` | Table | Sub-containers under a table. |
| `Levels` | Hierarchy | Levels of a hierarchy. |
| `Members`, `TablePermissions` (alias `Permissions`) | Role | Children of a role. |

Calculated sets are addressable in container form only (`<table>/Sets/<name>`); an individual KPI is `<table>/<measure>/KPI`; calendars resolve at `<table>/Calendars/<name>`; relationships resolve at `Relationships/{guid}` (`--paths-only` prints the GUID form, and the display name is also accepted).

A few examples show how plain and container-scoped paths differ:

```bash
te get Sales/Revenue                       # Measure or column on Sales
te get Sales/Measures/Revenue              # Same, container-scoped - disambiguates if other kinds share the name
te get Sales/Geography/Levels/Year         # Specific level of a hierarchy
te get Roles/Admin/Members/bob@example.com # Role member
te get Sales/refreshPolicy                 # Refresh-policy sub-object on a table
te get Sales/Revenue/KPI                   # KPI sub-object of a measure
```

Quote a segment to force literal-name matching when a real object name happens to coincide with a keyword. The table literally named `Tables` is `'Tables'`, addressed by `te get "'Tables'"`. The same applies to tables named `KPIs` or `Sets`.

### Wildcards in filter paths

Filter paths add a single wildcard character - `*` - that matches any run of characters within one segment (greedy, single-segment). Wildcards are how `te list` and similar commands narrow their results.

```bash
te list 'Sa*'                          # Tables whose name starts with Sa
te list 'Sales/*Amount'                # Children of Sales whose name ends with Amount
te list '*/Amount'                     # An Amount column/measure across every table
te list 'Roles/Re*/Members'            # Members of every role matching Re*
```

A filter path with **N segments** produces **N-level-deep** results - wildcards never auto-expand a level beyond what you typed. The single-segment shortcut `te list Sales` is the exception: an unqualified, non-wildcarded table name expands to the table's direct children to match the "show me what's in Sales" intent. `te list Sa*`, in contrast, returns just the matching tables - no expansion.

DAX bracket-suffix is rejected in filter paths; quote names containing `[` and `]` if you need to match them literally.

### Errors and hints

Misspelled segments emit a contextual error with a "did you mean" hint when the CLI can guess what you meant. Missing-parent paths fail before the leaf check, so the message points at the segment that's actually wrong. Empty containers (e.g., `te list Hierarchies` on a model without hierarchies) emit a simple "nothing here" hint rather than an error.

## Command aliases

Most long-form verbs also accept a short alias. Each row shows the canonical command and the equivalent short-form command it accepts as an alias.

| Canonical | Aliased form(s) |
| -- | -- |
| `te save-as` | `te save` |
| `te list` | `te ls` |
| `te remove` | `te rm` |
| `te move` | `te mv`, `te rename` |
| `te bpa rules list` | `te bpa rules ls` |
| `te bpa rules remove` | `te bpa rules rm` |
| `te config list` | `te config ls` |
| `te macro list` | `te macro ls` |
| `te macro remove` | `te macro rm` |
| `te profile list` | `te profile ls` |
| `te profile remove` | `te profile rm` |
| `te session list` | `te session ls` |
| `te test list` | `te test ls` |

## Global options

These flags are available on every command and can be used before or after the subcommand name.

| Option | Description |
| -- | -- |
| `-m, --model <path>` | Path to semantic model (TMDL folder, `.bim` file, `database.json` folder, or `.SemanticModel` folder). |
| `-s, --server <endpoint>` | Analysis Services endpoint or Power BI workspace. A server name/FQDN (`MY.SERVER.COM`), IP address (`192.168.1.1`), `host:port`, `localhost`, `SERVER\INSTANCE`, `asazure://...`, or an MSOLAP connection string connects directly to Analysis Services / AAS. A bare single-token name (`MyWorkspace`), a Fabric `Name.Workspace[/Model.SemanticModel]` path, or a `powerbi://...` URL targets a Power BI workspace. A workspace name containing a dot is indistinguishable from a server name, so it is treated as a server and the CLI prints a warning; use its `.Workspace` form or full `powerbi://` URL to target Power BI. |
| `-d, --database <name>` | Semantic model name on the workspace. |
| `--local` | Connect to a locally running Analysis Services instance - Power BI Desktop, Visual Studio workspaces, or standalone SSAS (Windows only). |
| `--auth <method>` | Auth method: `auto`, `interactive`, `spn`, `env`, `managed-identity` (default: `auto`). |
| `--output-format <format>` | Stdout format: `text` (default), `json`, `csv`, `tmsl` (alias `bim`), `tmdl`. `csv` is honored by commands that emit tabular data; `tmsl`/`tmdl` only by `te get` and `te list` for whole-object serialization. Commands reject formats they don't support. |
| `--error-format <format>` | Stderr format for errors, warnings, and hints: `text` (default) or `json`. Other values fall back to text. Independent of `--output-format`, so you can pair JSON stdout with plain-text errors (or vice versa). |
| `--recent [N]` | Use a recently used model. No value = interactive picker; `N` = Nth most recent (1 = last used). |
| `--non-interactive` | Disable all interactive prompts. Fail with an actionable error if required input is missing. |
| `--debug` | Enable debug logging to stderr (connection strings, auth flow, timing). |

`te --version` prints the CLI version and exits.

For commands that read a model, the resolution order is:

`--recent` → `--local` → `--server`/`--database` (remote) → `--model` → active connection from `te connect`.

The model is never a positional argument - a stray path on the command line is rejected with an "unrecognized command or argument" error. (Positional arguments on `te connect`, `te init`, `te diff`, and `te query` are those commands' own subjects, not the model.)

> [!NOTE]
> **Mistyped options are rejected up front.** If you pass a `--flag` that isn't recognised on the command you invoked, the CLI exits with an actionable error rather than silently absorbing the token as a positional argument. This catches typos like `--force ` accidentally becoming `--forec` in CI scripts.

> [!NOTE]
> **Dotted server names.** `-s`/`--server` treats a dotted name (e.g. `Sales.2026`) as an Analysis Services server hostname, not a Power BI workspace. A warning fires when the CLI has to make this call, with a hint to append `.Workspace` (e.g. `Sales.2026.Workspace`) or use a full `powerbi://` URL if you meant the Power BI workspace. Applies to `te connect`, `te deploy`, `te refresh`, `te query`, `te vertipaq`, and `te test run`.

## Model I/O

### save-as

Re-serialize a model to a different format or location. Use it to write a remote workspace model to local files, convert formats, or persist edits back to the source. (Alias: `save`.)

`te save-as` accepts:

- `-o, --output-path <path>` - target file or folder. **Optional** - when omitted, `te save-as` writes back to the source location, preserving the original format.
- `--serialization <fmt>` - `tmdl`, `bim` (alias `tmsl`), `database.json`, `pbip`. When omitted, the format is the loaded model's format; with `-o`, it is inferred from the output path (`.bim` writes a single-file BIM, `.json` a `database.json` folder).
- `--force` - skip validation and overwrite existing output. Some refusals (ambiguous containers, multi-`SemanticModel` project roots) fire even under `--force`.
- `--skip-bpa` - bypass the BPA gate entirely.
- `--fix-bpa` - auto-fix BPA violations where rules define a fix expression.
- `--bpa-rules <path>` - repeatable; override `bpa.rules` from your CLI config for this single save. Built-in rules still apply unless `bpa.builtInRules` is `false`.
- `--skip-validation` - skip DAX semantic analysis and validation for fast passthrough downloads.
- `--supporting-files` - generate Fabric supporting files (`.platform`, `definition.pbism`).

```bash
te save-as                                    # Save back to source (no -o needed)
te save-as -m ./model.bim -o ./tmdl-out       # Convert BIM to TMDL
te save-as -o ./project --serialization pbip         # Save as a PBIP project
te save-as -o ./out -s my-workspace -d my-model --skip-validation   # Fast download
```

`--serialization pbip` output opens directly in Power BI Desktop and is named after the source model (`SpaceParts.pbip`, not `Model.pbip`).

> [!TIP]
> Use `te save-as -o <path> -s <workspace> -d <model>` to download a remote model to disk. Pair with `--skip-validation` for the fastest passthrough when you only need the bytes (no DAX semantic analysis).

### init

Create a new empty semantic model at the given path. Defaults to a TMDL model in `PowerBI` compatibility mode at compatibility level 1705.

`te init` accepts:

- `<output-path>` - positional argument: directory to create the model in (omit to use the global `--model` path).
- `--compatibility-mode <mode>` - `PowerBI` (default) or `AnalysisServices`.
- `--compatibility-level <N>` (alias `--compat`) - compatibility level. Defaults to `1705` when the mode is `PowerBI`, `1500` otherwise. See @update-compatibility-level.
- `--name <name>` - model/database name (default: the directory name).
- `--serialization <fmt>` - `tmdl` (default), `bim` (alias `tmsl`), `database.json`, `pbip`.
- `--force` - replace any existing file or directory at the target path.

```bash
te init ./new-model                                       # TMDL, PowerBI mode, compat 1705
te init ./new-model --serialization bim                   # Single-file BIM model
te init ./as-model --compatibility-mode AnalysisServices  # AS model, compat 1500
te init ./existing-dir --force                            # Overwrite non-empty directory
```

`te init` is idempotent: re-running it over a model it already created prints `Already exists` and exits `0` (under `--output-format json`: `{"created": false, "reason": "already_exists", ...}`). Real conflicts still exit `1`; `--force` re-creates from scratch.

## Model editing

Mutating commands (`set`, `add`, `remove`, `move`, and also `script`, `macro run`, `bpa run --fix`) are **dry runs by default**: without `--save` the command reports what would change and discards it (`Dry run - nothing saved. Add --save to persist.`). Add `--save` to persist to the source, or `--save-to <path>` to write elsewhere. On `set`, `add`, `remove`, `move`, `script`, and `bpa run`, the change output renders as a unified diff per changed object; switch it with `--stat` or `--name-only` (mutually exclusive with `--diff`, the default), or set a standing default with `te config set mutationOutput diff|stat|name-only|none`. JSON output always carries the full changes array. A save is refused when the mutation introduces new DAX validation errors, unless `--force`.

### set

Set properties on a model object, format its expressions, or sync a table with its source schema. Accepts a `<path>`.

`te set` accepts:

- `-p, --property <Name=Value>` - property assignment (e.g., `-p expression="SUM(Sales[Amt])"`, `-p isHidden=true`). **Repeatable** - everything after the first `=` is the value. Bare positional assignments work too: `te set Sales/Amount formatString="#,0" --save`. Property names accept dotted paths and indexers: `-p KPI.StatusGraphic=...`, `-p "Annotations[Tabular Editor]=..."`, `-p "TranslatedNames[fr-FR]=..."`. Use `-p Name=-` to read the value from stdin (one assignment per stream), and `-p Name=null` to clear object-valued properties (`SortByColumn=null`, `RefreshPolicy=null`).
- `--format <PropertyName>` - format that expression property (repeatable; DAX or M is detected from the property). Formatter tweaks `--semicolons`, `--long` (fewer line breaks), and `--no-space-after-function` require `--format` on a DAX property.
- `--update-schema` - sync a table's columns with its source schema: adds new source columns with detected types, retypes drifted ones, and preserves column properties. Removed source columns only warn unless `--drop-removed-columns` (destructive). A renamed source column looks like remove + add - remap it first with `-p SourceColumn=<newName>`. Refused on calculated tables and calculation groups; cannot combine with `-p` or `--format`. Shares the schema-detection source flags with `te add` (`--source sql|lakehouse|warehouse`, `--endpoint`, `--connection-string`, `--source-database`, `--source-table`); when the source flags are omitted, the source is taken from the partition's own binding.
- `-t, --type <kind>` - disambiguation when the same path could resolve to multiple object kinds (`Measure`, `Column`, `CalculatedColumn`, `Hierarchy`, `Calendar`, `Partition`, `CalculationItem`).
- `--save` / `--save-to <path>` - persist changes.
- `--diff` / `--stat` / `--name-only` - change-output rendering (see the note above).
- `--serialization <fmt>` - override the serialization when saving (`tmdl`, `bim` (alias `tmsl`), `database.json`).
- `--force` - save even if the mutation introduces DAX validation errors.

```bash
te set Sales/Amount -p expression="SUM(Sales[Amt])" --save
te set "'Net Sales'[Sales Amount]" -p formatString="#,0" --save        # DAX form with spaced names
te set Sales -p isHidden=true --save
te set Sales/Amount -p formatString="#,0" -p description="Net sales" --save   # Multiple properties, one atomic change
te set Sales/Amount --format Expression --save                          # Format one expression property
te set Sales --update-schema --save                                     # Sync columns with the source schema
```

#### Incremental refresh policies

Refresh policies are plain properties on a table's `RefreshPolicy` sub-object, so `te get` and `te set` manage them like anything else. Property names: `Mode`, `RollingWindowPeriods`/`RollingWindowGranularity`, `IncrementalPeriods`/`IncrementalGranularity`, `IncrementalPeriodsOffset`, `SourceExpression`, `PollingExpression` (file input: `-p SourceExpression=- < src.m`).

```bash
te get Sales/RefreshPolicy                                              # Inspect a table's refresh policy
te set Sales/RefreshPolicy -p RollingWindowPeriods=5 -p RollingWindowGranularity=Day -p IncrementalPeriods=1 -p IncrementalGranularity=Day --save
te set Sales -p RefreshPolicy=null --save                               # Remove the policy
```

The policy is created implicitly on the first `set`. Removing one leaves policy-generated partitions in place, and is refused when they are the table's only partitions. To apply a policy on the server, see [`te refresh --apply-refresh-policy`](#refresh); to apply it metadata-only, use `te script --inline "Model.Tables[\"Sales\"].ApplyRefreshPolicy();" --save`.

### add

Add an object to the model. Pass a `<path>` for the new object (the parent must already exist; the leaf segment is the new name) and the type via `-t` / `--type`. Relationships keep their shorthand syntax (`Sales[Key]->Dim[Key]`). Container-form paths are valid add targets (`Sales/Measures/Margin`, `Sales/Partitions/Q1`, `Sales/Calendars/Fiscal`, `Roles/Admin/TablePermissions/Sales`, `Roles/Admin/Members/user@x.com`) - any path the CLI prints can be fed back to `te add`.

`te add` accepts:

- `-t, --type <type>` - object type. Common values: `Table`, `CalculatedTable`, `CalcGroup`, `Measure`, `CalculatedColumn`, `DataColumn`, `Hierarchy`, `Level`, `Calendar`, `CalcItem`, `KPI`, `Partition`, `Expression`, `Function`, `Perspective`, `Culture`, `Role`, `TablePermission`, `Member`. Tab-completion is supported; the full list can be retrieved by running `te add --help`.
- `-p, --property <Name=Value>` - property assignment on the new object (repeatable). The expression goes in `-p Expression="..."`, or use `--file`, or `-p Expression=-` to read it from stdin.
- `--file <path>` - read the expression from a file instead of inline.
- `--mode <mode>` - storage mode for new tables: `import` (default), `directquery` (alias `dq`), `dual`, `directlake` (alias `dl`).
- `--if-not-exists` - exit `0` without error if the object already exists. Use this for idempotent CI/CD pipelines.
- `--save` / `--save-to <path>` - persist changes.
- `--diff` / `--stat` / `--name-only` - change-output rendering (see the [Model editing](#model-editing) note).
- `--serialization <fmt>` - override the serialization when saving (`tmdl`, `bim` (alias `tmsl`), `database.json`, `pbip`).
- `--source-type <kind>` - initial partition source type on a new table: `m`, `query`, or `calculated`. Overrides heuristic detection. `query` builds a legacy SQL `SELECT` partition bound to the model's provider data source and is refused with lakehouse/warehouse sources or when no provider source exists; `calculated` is only valid with `-t CalculatedTable`.
- `--partition-expression <m>` - raw M expression for the new table's initial partition.
- `--force` - save even if the mutation introduces DAX validation errors.

Adding a single data column to an existing table takes `-t DataColumn` with both `SourceColumn` and `DataType` required (refused on calculated tables and calculation groups):

```bash
te add Sales/Quantity -t DataColumn -p SourceColumn=Qty -p DataType=Int64 --save
```

Tables can be created in one shot from the model's **own** data source - no connection flags needed. Columns are detected by reading the model's data source; missing credentials, no data source, or no columns is a clean refusal with nothing created:

- `--source-table <schema.table>` - create the table from this source table.
- `--query "SELECT ..."` - create the table from a query instead (columns inferred by describing the query; long form only).
- `--data-source "<name>"` - disambiguate when the model has several data sources.

Schema detection against an explicit source also works: `--source sql|lakehouse|warehouse`, `--endpoint`, `--connection-string`, `--source-database`, `--source-table`, or a manual column spec `--columns "Id:Int64,Name:String"`.

```bash
te add Sales/Revenue -t Measure -p Expression="SUM(Sales[Amount])" --save
te add Sales/Quantity -t DataColumn -p SourceColumn=Qty -p DataType=Int64 --save
te add "Sales[ProdKey]->Product[ProdKey]" --save                        # Relationship shorthand
te add Sales/MarketingFlag -t CalculatedColumn -p Expression="Sales[Amount] > 1000" --if-not-exists --save
te add Perspectives/Default/Sales --save                                # Include Sales in the Default perspective
te add Roles/Reader -t Role --save                                      # New role at the model level
te add Inventory -t Table --source-table dbo.Inventory --save           # Table from the model's own data source
te add TopCustomers -t Table --query "SELECT TOP 100 * FROM dbo.Customers" --save
```

### remove

Remove an object. Checks dependents by default to prevent breaking existing references. (Alias: `rm`.)

`te remove` accepts:

- `<path>` - positional argument: the object to remove.
- `-t, --type <kind>` - disambiguate when the path matches multiple table-children (e.g., a column and a hierarchy with the same name).
- `--force` - bypass the dependents check.
- `--if-exists` - exit `0` without error if the object doesn't exist. Use this for idempotent CI/CD pipelines.
- `--dry-run` - preview the removal without applying it.
- `--save` / `--save-to <path>` - persist the change.
- `--diff` / `--stat` / `--name-only` - change-output rendering (see the [Model editing](#model-editing) note).
- `--serialization <fmt>` - override the serialization when saving (`tmdl`, `bim` (alias `tmsl`), `database.json`).

```bash
te remove Sales/Revenue --save
te remove "'Sales'[Revenue]" --save              # DAX form
te remove Sales/Revenue --dry-run                # Preview only
te remove Sales/OldMeasure --if-exists --save    # Idempotent
```

### move

Move or rename a model object. Both source and destination are `<path>` arguments. (Aliases: `mv`, `rename`.)

`te move` accepts:

- `-t, --type <kind>` - disambiguate when the source path matches multiple object kinds (e.g., a column and a hierarchy with the same name).
- `--save` / `--save-to <path>` - persist the change.
- `--diff` / `--stat` / `--name-only` - change-output rendering (see the [Model editing](#model-editing) note).
- `--serialization <fmt>` - override the serialization when saving (`tmdl`, `bim` (alias `tmsl`), `database.json`).
- `--force` - save even if the mutation introduces DAX validation errors.

```bash
te move Sales/Revenue Finance/Revenue --save                # Move measure to another table
te move Sales/Revenue Sales/TotalRevenue --save             # Rename measure
te move Sales/Date Sales/CalendarDate -t Hierarchy --save   # Disambiguate hierarchy from column
te move "Sales/Partitions/Old" "Sales/Partitions/New" --save   # Container-form paths work too
```

## Inspection

### list

List objects with filesystem-like navigation. Takes a `<path-filter>` argument supporting wildcards. Both model-level containers and table-scoped containers are supported - see the [container keyword table](#containers-and-keywords) above for the full list. (Alias: `ls`.)

`te list` accepts:

- `--type <kind>` - narrow to one object kind (`table`, `measure`, `column`, `hierarchy`, `partition`, `relationship`, `role`, `perspective`, `culture`, `calculationitem`, `kpi`, `set`, `function`). With no `<path-filter>` this is equivalent to typing the matching container keyword.
- `--paths-only` - emit one object path per line, suitable for piping to `xargs`, `te get`, or `te set`.
- `--no-multiline` - collapse multi-line cells (typically DAX or M expressions) to a single line and truncate, so rows stay scannable in wide tables. Text output only; JSON/CSV/TMSL output is unaffected.
- `--output-format tmsl` (alias `bim`) - emit the matching objects as a TMSL/BIM script. Useful for `te list Tables --output-format bim > tables.json`. `--output-format tmdl` is not supported by `ls` (TMDL is single-object only - use `te get`).

```bash
te list                                     # All tables in the model
te list Sales                               # All children of Sales (columns + measures + hierarchies + partitions)
te list Sales/Measures                      # Just Sales's measures
te list 'Sales/*Amount'                     # Children of Sales whose name ends with Amount
te list 'Sa*'                               # Tables whose name starts with Sa (no auto-expansion)
te list '*/Amount'                          # An Amount column/measure across every table
te list 'Roles/Re*/Members'                 # Members of every role matching Re*
te list Sales/Geography/Levels              # All levels of the Geography hierarchy
te list KPIs                                # All KPIs (with parent measure)
te list Sales/KPIs                          # KPIs on measures of Sales
te list Sets                                # Calculated sets
te list Functions                           # DAX user-defined functions
te list "'Net Sales'/'Sales Amount'"        # Quote names containing spaces
te list Measures --paths-only               # One Table/Measure per line for piping
te list --type measure                      # Same as `te list Measures`
te list Measures --no-multiline             # Wide table with column dividers, single-line DAX
te list Tables --output-format bim > tables.json   # All tables emitted as TMSL/BIM
```

In JSON output, every listed object leads with its `objectPath` - a canonical path that resolves with `te get`.

### get

Get properties of a model object, filter and list sets of objects, and analyze dependencies - `get` is the CLI's one read pipeline (`te list` and `te deps` remain as shortcuts). Takes a `<path>`; omit it to list the model (same as `te list`), or pass `.` for the model root.

`te get` accepts:

- `-p, --property <property>` - project a single property (e.g. `expression`, `formatString`).
- `--where <Prop=Value>` - filter the result set; repeatable (AND), case-insensitive. A value with no `*` is an exact match; `*` is a wildcard, so a contains-search is `--where Name=*margin*`.
- `--ls` - compact table layout (the same rendering as `te list`).
- `--deps [upstream|downstream]` - dependency analysis (default: both directions); `--deep` for the recursive tree, `--max-depth <N>` (default `10`).
- `--unused` / `--hidden` - surface unused objects, as on `te deps`.
- `--paths-only` - one canonical object path per line, for piping.
- `--no-multiline` - collapse multi-line cells (with `--ls`/`--where`). Text output only.
- `-t, --type <kind>` - disambiguate when the path matches multiple table-children (e.g., a column and a hierarchy with the same name). Values: `Measure`, `Column`, `CalculatedColumn`, `Hierarchy`, `Calendar`, `Partition`, `CalculationItem`.
- `--output-format tmsl` (alias `bim`) - emit the resolved object as TMSL/BIM JSON.
- `--output-format tmdl` - emit the resolved object as TMDL (named objects only).

`te get` and `te list` share a single descriptor catalog, so every property surfaces the same way across formats - the text table, JSON, and CSV all see the same set, and adding a new property to the model exposes it everywhere.

```bash
te get Sales/Amount -p expression                # Print DAX
te get "'Sales'[Amount]"                         # DAX form: same as Sales/Amount
te get "[Total Sales]"                           # Lone-bracket: model-wide measure-or-column
te get "'Net Sales'[Sales Amount]" -p expression # DAX form with spaced names
te get Sales/Revenue/KPI                         # KPI sub-object of a measure
te get Sales --output-format tmdl                # Emit the table as TMDL
te get Sales --output-format bim                 # Emit the table as TMSL/BIM
te get . -p description                          # Model-level property
te get Measures --where IsHidden=true --ls       # Filter + list rendering
te get Sales/Revenue --deps downstream --deep    # Recursive dependents
```

### find

Search for text across model objects.

`te find` accepts:

- `--in <scope>` - scope: `names`, `expressions`, `descriptions`, `displayFolders`, `formatStrings`, `annotations`, `all` (default: `all`).
- `--regex`, `--case-sensitive`, `--paths-only`.
- `--no-multiline` - collapse multi-line match context to a single line. Text output only.

`--in expressions` covers every `IExpressionObject` in the model - including KPI `TargetExpression` / `StatusExpression` / `TrendExpression`, measure `DetailRowsExpression`, partition source/polling M, table-permission `FilterExpression`, and calculation-group `MultipleOrEmptySelection` / `NoSelection` expressions - so a literal like `123` set on a KPI's target turns up the same way a measure body would.

```bash
te find "CALCULATE" --in expressions
te find "Revenue" --in names
te find "CALCULATE" --in expressions --paths-only | xargs -I{} te get {} -p expression
```

### diff

Compare two models for structural differences. Returns the following exit codes: `0` = identical, `1` = differences found, `2` = error.

```bash
te diff ./model-v1 ./model-v2
te diff old.bim new.bim

# Branch on exit code (POSIX sh):
te diff ./a ./b; case $? in 0) echo same;; 1) echo different;; *) echo error;; esac

# Branch on exit code (PowerShell):
te diff ./a ./b; switch ($LASTEXITCODE) { 0 { 'same' } 1 { 'different' } default { 'error' } }
```

### deps

Analyze an object's upstream and downstream dependencies, or surface unused objects across the model. A shortcut for `te get --deps` / `te get --unused`. The single-object form takes a `<path>`.

`te deps` accepts:

- `--upstream` - show only upstream dependencies (what this object uses).
- `--downstream` - show only downstream dependents (what uses this object).
- `--deep` - show the recursive dependency tree instead of direct dependencies only.
- `--max-depth <N>` - maximum depth for `--deep` traversal (default: `10`).
- `-t, --type <kind>` - disambiguate when the path matches multiple table-children (e.g., a column and a hierarchy with the same name).
- `--unused` - list measures, calculated columns, and **all data columns** that no DAX references and that aren't used in any relationship, hierarchy level, sort-by, variation, AlternateOf base, or calendar time role. Each result shows `(hidden)` in text mode and an `isHidden` field in JSON.
- `--hidden` - narrow `--unused` to hidden objects only. Hidden, unused objects are the safest prune candidates because nothing user-facing depends on them.

```bash
te deps Sales/Revenue                     # Upstream + downstream for one object
te deps "'Sales'[Revenue]"                # DAX form is accepted everywhere a <path> is
te deps Sales/Revenue --downstream --deep # Everything that depends on Revenue, recursively
te deps --unused                          # All unused measures and columns
te deps --unused --hidden                 # Only hidden, unused objects
```

## Analysis and quality

### validate

Validate model expressions, schema integrity, and TOM errors.

`te validate` accepts:

- `--ci <fmt>` - emit CI annotations to stderr: `vsts` or `github`.
- `--trx <path>` - write results as a VSTEST `.trx` file.
- `--errors-only` - shorthand for `--no-warnings --no-antipatterns`: only show errors.
- `--no-warnings` - hide warnings from the semantic analyzer.
- `--no-antipatterns` - hide anti-pattern suggestions (DAX best-practice hints).
- `--server-only` - only show errors reported by the connected server; skip local semantic analysis.
- `--no-multiline` - collapse multi-line cell content (error messages, expressions) to a single line. Text output only.

```bash
te validate -m ./model
te validate --ci github --trx results.trx
te validate --errors-only                 # Hide warnings and anti-pattern hints
```

Under `--output-format json`, `te validate` emits the unified findings envelope (`summary` plus a flat `findings[]` array) shared with `te bpa run`, `te test run`, and `te query` - see @te-cli-findings.

> [!NOTE]
> `te validate` does not support `--output-format csv` - CSV is rejected up front with an actionable error rather than producing a partial result. Use `text` or `json` for validation output.

### bpa run

Run Best Practice Analyzer rules against a model.

`te bpa run` accepts:

- `-r, --rules <rules>` - path(s) or URL(s) to BPA rule file(s) in JSON format. Repeatable. Replaces the user-rule layer for this invocation: see [Rule sources and resolution](#rule-sources-and-resolution) below.
- `--no-model-rules` - exclude BPA rules embedded in the model's annotations.
- `--no-defaults` - exclude built-in default BPA rules.
- `--vpax <file>` - load VertiPaq Analyzer stats from a `.vpax` file to enable VPA-aware rules.
- `--allow-external-rules` - allow fetching BPA rule files from URLs embedded in model annotations.
- `--rule <id>` - run only specific rule(s) by ID. Repeatable.
- `--path <path-filter>` - limit analysis to the tables containing the matched objects. Accepts literal names, container keywords, and wildcards (e.g., `'Sales'`, `'Sa*'`, `'Sales/Measures'`, `'*/Amount'`).
- `--fix` - apply fix expressions to auto-fix violations where possible.
- `--save` - save the model back to source after applying fixes.
- `--save-to <path>` - save the model to a different path after applying fixes.
- `--diff` / `--stat` / `--name-only` - change-output rendering for the fix pass (see the [Model editing](#model-editing) note).
- `--serialization <fmt>` - model serialization: `tmdl`, `bim` (alias `tmsl`), `database.json`.
- `--fail-on <severity>` - failure threshold: `error` (default) or `warning`. Exits with code `1` when violations meet the threshold. Rule-loading or evaluation errors (invalid expressions, unreadable rule files) also cause a non-zero exit regardless of `--fail-on`.
- `--ci <fmt>` - emit CI logging commands to stderr: `vsts` (Azure DevOps), `github` (GitHub Actions).
- `--trx <path>` - write results as a VSTEST `.trx` file to the specified path.
- `--no-multiline` - collapse multi-line cell content in the violations table to a single line. Text output only.

```bash
te bpa run --fail-on error --ci github
te bpa run --fix --save
te bpa run --rule PERF_UNUSED_HIDDEN_COLUMN
te bpa run --path Sales            # Tables touched by the Sales filter only
te bpa run --path 'Sa*'            # Wildcard - every table starting with Sa
te bpa run --path Sales/Measures   # Path filter applied to the matched tables
```

Under `--output-format json`, `te bpa run` emits the unified findings envelope (see @te-cli-findings); with `--fix`, the JSON is a single document that also includes the `fix` change set.

#### Rule sources and resolution

Each `te bpa run` invocation assembles rules from three independent layers:

1. **User rules** - exactly one source wins, in priority order:
   - `-r, --rules <rules>` flag, accepts a file path or URL (highest)
   - `TE_BPA_RULES` environment variable
   - `bpa.rules` array from CLI config (`~/.config/te/config.json`)
2. **Built-in defaults** - loaded unless `--no-defaults` is passed or [`bpa.builtInRules`](xref:te-cli-config#built-in-bpa-rules) is `false` in config. Individual built-ins listed in `bpa.disabledBuiltInRuleIds` are skipped.
3. **Model-embedded rules** - rules in the model's `BestPracticeAnalyzer_Rules` annotation, loaded unless `--no-model-rules` is passed. External URL annotations are skipped unless `--allow-external-rules` is also passed.

The built-in defaults are exactly Tabular Editor 3's built-in rule set (the `TE3_BUILT_IN_*` IDs), so `te bpa run` and TE3 Desktop agree on what the built-ins flag.

Each rule ID is evaluated once. When the same ID appears in more than one layer, an explicit `--rules` file's definition wins in `te bpa run`, while the built-in definition wins in the deploy/save gates. Rule IDs in the model's `BestPracticeAnalyzer_IgnoreRules` annotation are then removed.

The `Rules loaded:` line in the output attributes each contributing layer, for example:

```
Rules loaded: 38 from 1 file(s) from bpa.rules config + built-in defaults + model annotations
```

### bpa rules

Manage BPA rule collections - list, inspect, initialize, and toggle rules in your local rules file or in model annotations. Built-in rules are read-only - to skip one without losing the rest, use `te bpa rules disable` (do not edit the built-in set directly).

Subcommands:

| Subcommand | Purpose |
| -- | -- |
| `add <id>` | Add a new BPA rule. |
| [`disable`](#bpa-rules-disable) | Disable a built-in BPA rule for the current user. |
| [`enable`](#bpa-rules-enable) | Re-enable a previously disabled built-in BPA rule. |
| `ignore <rule-id>` | Add a rule to the model's ignore list. |
| [`init`](#bpa-rules-init) | Create an empty BPA rules file at the resolved path. |
| [`list`](#bpa-rules-list) (alias `ls`) | List BPA rules from all sources with status. |
| `remove <rule-id>` (alias `rm`) | Remove a BPA rule. |
| `set <rule-id>` | Update a BPA rule's properties. |
| `unignore <rule-id>` | Remove a rule from the model's ignore list. |

All `te bpa rules` subcommands accept:

- `--rules-file <path>` - path to a BPA rules JSON file. Defaults to the first existing entry of `bpa.rules` in your CLI config (`~/.config/te/config.json`), or the `TE_BPA_RULES` environment variable.
- `--model-rules` - operate on rules embedded in the model annotation instead of a file.

> [!IMPORTANT]
> `te bpa rules set` and `te bpa rules remove` refuse to mutate built-in rule IDs. Attempting to do so exits with code `1` and points at `te bpa rules disable`. To customize a built-in rule's behavior, disable the built-in and add a custom copy with a different ID:
>
> ```bash
> te bpa rules disable TE3_BUILT_IN_DATE_TABLE_EXISTS
> te bpa rules add MY_DATE_TABLE_EXISTS
> ```

#### bpa rules list

List rules from all sources (built-in, user, model). (Alias: `ls`.)

`te bpa rules list` accepts:

- (default) Active rules only.
- `--all` - include disabled and ignored rules.
- `--disabled` - only built-in rule IDs the user has disabled via `te bpa rules disable`.
- `--ignored` - only rules whose IDs appear in `BestPracticeAnalyzer_IgnoreRules` on the model.
- `--no-defaults` - exclude built-in rules from output.

```bash
te bpa rules list              # Active rules
te bpa rules list --all        # Include disabled and ignored rules
te bpa rules list --ignored
```

Disabled built-in rules are flagged with a `[disabled]` marker next to the rule ID.

#### bpa rules init

Create an empty BPA rules file (`[]`) at the configured path. Use this once before invoking `te bpa rules set` / `te bpa rules remove` against a path that does not yet exist.

`te bpa rules init` accepts:

- `--force` - overwrite an existing file with `[]`. Required if the target file exists.
- `--rules-file <path>` - target file path. Can appear before or after the `init` subcommand.

Path resolution (first match wins): `--rules-file` → `TE_BPA_RULES` env var → first entry of `bpa.rules[]` in your CLI config → `./BPARules.json` (current working directory).

```bash
te bpa rules init
te bpa rules init --rules-file ./MyRules.json
te bpa rules init --force
```

#### bpa rules add / set / remove / ignore / unignore

Mutate the rules file (`add`, `set`, `remove` (alias `rm`)) or model-embedded ignore list (`ignore`, `unignore`). All three mutating subcommands operate on `--rules-file <path>` or `--model-rules` and refuse to touch built-in rule IDs.

- `te bpa rules add <id>` - create a new rule. Pass each property as a named option:
  - `--name <text>` - human-readable rule name (required).
  - `--scope <list>` - comma-separated object kinds the rule applies to: `Measure`, `Column`, `Table`, `Hierarchy`, `Partition`, `Relationship`, `Role`, `Perspective`, `Culture`, etc. (required).
  - `--expression <text>` - Dynamic LINQ predicate. Returns `true` for objects that violate the rule (required).
  - `--category <text>` - grouping label (e.g. `Performance`, `Naming`, `DAX Expressions`).
  - `--severity <1|2|3>` - `1` (info), `2` (warning, default), `3` (error).
  - `--description <text>` - user-facing description shown when the rule fires.
  - `--fix-expression <text>` - Dynamic LINQ expression used by `te bpa run --fix` to auto-remediate.
- `te bpa rules set <id>` - update properties on an existing rule. Uses `-p, --property <name=value>` (repeatable; `-` reads the value from stdin). Property names: `name`, `expression`, `scope`, `category`, `severity`, `description`, `fixExpression`.
- `te bpa rules remove <id>` - remove a rule.
- `te bpa rules ignore <id>` - add a rule ID to the model's `BestPracticeAnalyzer_IgnoreRules` annotation.
- `te bpa rules unignore <id>` - remove a rule ID from the model's ignore list.

```bash
# Add a rule: measures that are not hidden and have no description
te bpa rules add MEASURE_NEEDS_DESCRIPTION \
    --name "Measures should have a description" \
    --scope Measure \
    --expression "not IsHidden and string.IsNullOrEmpty(Description)" \
    --severity 2 \
    --category Metadata

# Update severity on an existing rule
te bpa rules set MEASURE_NEEDS_DESCRIPTION -p severity=3

# Remove the rule
te bpa rules remove MEASURE_NEEDS_DESCRIPTION
```

#### bpa rules disable

Disable an individual built-in BPA rule. The rule ID is added to `bpa.disabledBuiltInRuleIds` in your CLI config. Subsequent gate runs (deploy, save, mutation) and `te bpa run` skip the disabled rule.

The command is idempotent - running `disable` against an already-disabled rule succeeds without modifying the config. It exits with code `1` if `<rule-id>` is not a built-in rule; use `te bpa rules list` to see valid built-in IDs.

```bash
te bpa rules disable TE3_BUILT_IN_DATE_TABLE_EXISTS
```

#### bpa rules enable

Re-enable a previously disabled built-in BPA rule by removing the rule ID from `bpa.disabledBuiltInRuleIds`. Exits with code `1` if the rule isn't currently disabled.

```bash
te bpa rules enable TE3_BUILT_IN_DATE_TABLE_EXISTS
```

### vertipaq

Analyze VertiPaq storage statistics.

`te vertipaq` accepts:

- `<path>` - optional positional argument: a table name to filter the analysis to a single table.
- `--columns`, `--relationships`, `--partitions`, `--all`.
- `--detail` - show expanded columns (data/dict/hierarchy size breakdown, encoding, segments).
- `--fields <list>` - comma-separated fields to display (e.g., `--fields name,card,size,%tbl,%db,bar`). Available fields vary by view.
- `--export <file.vpax>` - export VertiPaq stats to a `.vpax` file for offline analysis.
- `--import <file.vpax>` - load a previously exported `.vpax` file and analyze it offline.
- `--obfuscate` - obfuscate names and expressions in exported VPAX.
- `--top <N>`, `--stats`, `--annotate`, `--save`.
- `--auth <method>` - auth method override when connecting to a remote model.

```bash
te vertipaq                      # Columns by size (default)
te vertipaq Sales                # Stats limited to the Sales table
te vertipaq --all                # Tables, columns, relationships, partitions
te vertipaq --export stats.vpax
te vertipaq --import stats.vpax  # Analyze offline
```

### Formatting expressions

Expression formatting lives in three places, depending on what you are formatting:

- **An expression in the model**: `te set <path> --format <PropertyName> --save` - see [set](#set).
- **A loose expression** (not in any model): `te util format-dax` / `te util format-m` - see [Utilities](#utilities).
- **A whole-model sweep**: `te script --inline "Model.AllMeasures.FormatDax();" --save`.

## Execution

### query

Execute a DAX query against a deployed model.

`te query` accepts:

- `<dax>` - positional argument: the DAX query to execute. Equivalent to passing `-q`. Use whichever shape reads better; explicit `-q` wins if both are supplied.
- `-q, --query <dax>` - inline query (named-flag form of the positional above). `-q -` reads the query from stdin; with input piped and no query given at all, stdin is read implicitly.
- `--file <file.dax>` - query from file.
- `--limit <N>` - default 100.
- `-o, --output-file <path>` - write results to file (`.csv`, `.tsv`, `.json`, `.dax`).
- `--trace`, `--cold`, `--plan`, `--runs <N>` - performance tracing and benchmarking.
- `--no-validate` - skip pre-execution DAX semantic validation.

```bash
te query "EVALUATE TOPN(5, 'Sales')" -s my-ws -d my-model           # Positional DAX
te query -q "EVALUATE TOPN(5, 'Sales')" -s my-ws -d my-model        # Named-flag form
te query --file query.dax --output-format json
```

### script

Execute one or more C# scripts against a semantic model. The CLI uses the same scripting host as Tabular Editor 3 Desktop, so a script that runs in TE3 runs unchanged here.

`te script` accepts:

- `--file <path>` - `.cs` / `.csx` file (repeatable). Bare positional `.cs`/`.csx` arguments are also accepted.
- `--inline <code>` - inline C# (repeatable; use `-` for stdin).
- `--validate` - compile the script(s) and report errors without executing them. Needs no model at all, so it works offline as a CI lint.
- `--save` / `--save-to` / `--serialization`.
- `--diff` / `--stat` / `--name-only` - change-output rendering (see the [Model editing](#model-editing) note).
- `--force` - save even if the mutation introduces DAX validation errors.

Files and inline snippets run in the order they are written on the command line.

```bash
te script --file fix.cs --save
te script fix.cs cleanup.csx --save              # Bare positionals, run in order
te script --inline "Info(Model.Tables.Count);"
echo "Info(Model.Name);" | te script --inline -
te script --file fix.cs --validate               # Compile-only, no model needed
```

> [!IMPORTANT]
> Two behavioral details to know if you're porting an older script:
>
> - **No interactive selection in CLI scripts.** The TE3 Desktop helpers `SelectMeasure()`, `SelectTable()`, `SelectColumn()`, `SelectObject()`, and `SelectObjects()` throw `NotSupportedException` when called from `te script` - the CLI has no UI to pop up. Pre-resolve the object(s) outside the script and pass them in via environment variables or stdin, or wrap the call in `try/catch` if the script is shared with TE3.
> - **Default `using` directives match TE3 Desktop.** Scripts that use `DataTable`, `File`, `StringBuilder`, or `Regex` must include the corresponding `using System.Data;` / `using System.IO;` / `using System.Text;` / `using System.Text.RegularExpressions;` directive explicitly.

> [!NOTE]
> **Preprocessor symbols for cross-host scripts.** Scripts compiled by `te script` have the symbol `TECLI` defined. TE3 Desktop scripts have `TE3` defined instead, plus version-bracketed symbols like `TE3_3_10_OR_GREATER` ... `TE3_3_X_OR_GREATER` for the current TE3 minor version. TE2 defines neither symbol. Use these to write portable scripts:
>
> ```csharp
> #if TECLI
>     // CLI-only code - no UI calls
>     Info($"Running under the CLI on {Environment.OSVersion.Platform}");
> #elif TE3
>     // TE3 Desktop-only code - UI APIs available
>     ShowMessage("Hello from TE3");
> #else
>     // TE2 (legacy) - neither TECLI nor TE3 is defined
>     Info("Hello from TE2");
> #endif
>
> #if TE3_3_15_OR_GREATER
>     // Gated on a specific TE3 minor version
> #endif
> ```
>
> See @csharp-scripts for the broader cross-version scripting story.

### macro

Manage and run macros from a macros JSON file (typically `MacroActions.json`). The macros file is resolved in this order: `--macros <path>` → `TE_MACROS_PATH` env var → `macros` in CLI config → `./MacroActions.json`.

Subcommands:

| Subcommand | Purpose |
| -- | -- |
| `list` (alias `ls`) | List macros. |
| [`run <name-or-id>`](#macro-run) | Run a macro. |
| `add <name>` | Add a macro. |
| `set <name-or-id>` | Update macro properties. |
| `remove <name-or-id>` (alias `rm`) | Remove a macro. |
| `sort` | Sort and re-assign IDs. |
| [`init`](#macro-init) | Create an empty macros file at the resolved path. |

#### macro add / set / remove

Mutate the macros file (`add`, `set`, `remove` (alias `rm`)). All three operate on `--macros <path>` (or the resolved macros file).

- `te macro add <name>` - create a new macro. Provide the script body via `-e "<code>"` (inline) or `-s <file.cs>` (script file). Optional: `--tooltip <text>`, `--contexts <list>` (where the macro applies, e.g., `Table,Measure`), `--enabled true|false`.
- `te macro set <name-or-id>` - update macro properties. Use `-p, --property <name=value>` (repeatable; `-` reads the value from stdin). Property names: `name`, `execute`, `enabled`, `tooltip`, `validContexts`.
- `te macro remove <name-or-id>` - remove a macro.

```bash
te macro add MyMacro -e "Info(Selected.Measure.Name);" --tooltip "Print measure name" --contexts Measure
te macro set MyMacro -p tooltip="Updated tooltip"
te macro remove MyMacro
```

#### macro init

Create an empty macros file (`{"Actions":[]}`) at the configured path. Use this once when the resolved macros file does not yet exist.

`te macro init` accepts:

- `--force` - overwrite an existing file. Required if the target exists.
- `--macros <path>` - target file path. Can appear before or after the `init` subcommand.

```bash
te macro init
te macro init --macros ./project-macros.json
te macro init --force
```

#### macro run

Run a macro. Macros that emit tables via `dataTable.Output()` render formatted output in the terminal, so DAX-style query macros work the same in `te macro run` as they do in TE3.

`te macro run` accepts:

- `--on <path>` - set the macro's selection context to a single named object (a table, measure, column, …). Equivalent to right-clicking that object in TE3 and invoking the macro from the context menu.
- `--save` / `--save-to` - persist any changes the macro makes. Like every mutating command, `te macro run` is a dry run without `--save`.
- `--serialization <fmt>` / `--force` - as on the other mutating commands.

```bash
te macro run "Hide all measures"
te macro run "Format DAX" --on Sales/Revenue --save
te macro run "Format DAX" --on "'Net Sales'[Sales Amount]" --save   # DAX form works in --on too
```

## Deployment and refresh

### deploy

Deploy a semantic model to Power BI, Fabric, Azure Analysis Services, or on-prem SQL Server Analysis Services.

**Dry run by default**: `te deploy` connects read-only and prints the exact TMSL it would send to stdout. Add `--execute` to actually deploy.

`te deploy` accepts:

- `-s, --server` / `-d, --database` - the model **source**, exactly as on every other command.
- `--target-server <target>` / `--target-database <name>` - the deploy **destination**: a workspace name, endpoint, or server, and the semantic model name to create or overwrite. A server name, FQDN, IP address, or MSOLAP connection string deploys to Analysis Services (Windows Integrated auth for on-prem); a workspace name or `powerbi://...` URL deploys to Power BI. For local model sources, the target falls back to the active `te connect` connection; when the source is remote, the target flags are required. Deploying a model onto itself is refused.
- `--execute` - actually deploy. In interactive mode this shows a summary + confirmation prompt with **`n` as the safe default**; `--execute --force` skips the prompt (required in CI, where a prompt without `--force` is an error).
- `--deploy-full` - overwrite + connections + partitions + shared expressions + roles + role members.
- `--deploy-connections`
- `--deploy-partitions`
- `--skip-refresh-policy`
- `--deploy-roles`
- `--deploy-role-members`
- `--deploy-shared-expressions`
- `--create-only`
- `--skip-bpa` - bypass the BPA gate entirely.
- `--fix-bpa` - auto-fix BPA violations where rules define a fix expression.
- `--bpa-rules <path>` - repeatable; override `bpa.rules` from your CLI config for this single deploy. Built-in rules still apply unless `bpa.builtInRules` is `false`.
- `--force` - skip the interactive confirmation.
- `--ci <fmt>` - `vsts` or `github`.
- `-p, --profile <name>` - one-shot use of a saved @te-cli-auth profile.

`--output-format bim|tmdl` is rejected on deploy. To capture the deployment script for review, redirect the dry-run output: `te deploy ... > deploy.tmsl`.

```bash
te deploy -m ./model --target-server my-workspace --target-database my-model --execute --force --ci github
te deploy -m ./model --target-server MY.SERVER.COM --target-database my-model --execute --force    # On-prem SSAS
te deploy -m ./model --target-server my-workspace --target-database my-model > deploy.tmsl         # Dry run: TMSL only
te deploy -s src-workspace -d src-model --target-server dst-workspace --target-database copy --execute   # Remote to remote
te deploy --local --target-server my-workspace --target-database my-model --execute                # Publish a Desktop model
```

> [!IMPORTANT]
> `te deploy` runs the Best Practice Analyzer as a gate before executing. See @te-cli-config for BPA gate configuration.

> [!NOTE]
> When `--output-format json` is set, `te deploy`'s JSON payload always includes the resolved `server` and `database`, even when they were resolved from active connection or profile rather than passed explicitly. Pipelines can use these fields to confirm the deploy target without re-parsing the command line. `te deploy` also exits non-zero on failure under `--output-format json`, matching its text-mode behavior - the JSON payload is the failure record, not a success signal.

### refresh

Trigger a data refresh on a deployed model.

**Dry run by default**: `te refresh` prints the TMSL a refresh would send to stdout. Add `--execute` to run it.

`te refresh` accepts:

- `--type <type>` - `full`, `dataonly` (alias `data-only`, `data`), `automatic` (alias `auto`), `calculate` (alias `calc`), `clearvalues` (alias `clear`), `defragment` (alias `defrag`), `add` (default: `automatic`).
- `--table <name>` - refresh specific table(s); repeatable.
- `--partition <Table.Partition>` - refresh specific partition(s).
- `--execute` - actually run the refresh.
- `--apply-refresh-policy <true|false|table>` - apply incremental refresh policies to determine which partitions are refreshed; pass a table name to scope the refresh to that table. Policies apply by default when the refresh type and scope are compatible, except for models hosted in Power BI Desktop. An explicit value wins (with warnings when it cannot take effect).
- `--effective-date <yyyy-MM-dd>` - set the effective date used by the refresh policy (ignored, with a warning, when no policy applies).
- `--max-parallelism <N>` - set the maximum number of partitions to refresh in parallel. Wraps the refresh in a TMSL `sequence` command.
- `--no-progress`, `--trace [path]`. `--trace` without `--execute` warns and prints the TMSL.

Executed refreshes under `--output-format json` always include a `progress` array; with the `vertipaqOnRefresh` config key enabled, a per-table `vertipaq` array (rows, size, columns) is included too - no `--trace` needed.

```bash
te refresh --type full --execute                        # Full refresh
te refresh --table Sales --type full --execute          # Single table
te refresh --type full > refresh.tmsl                   # Dry run: emit TMSL only
te refresh --apply-refresh-policy Sales --execute       # Apply Sales' incremental refresh policy
```

Incremental refresh policies are authored with [`te set`](#incremental-refresh-policies) on a table's `RefreshPolicy` sub-object.

## Testing

### test run

Run a suite of DAX assertion tests against a deployed model.

`te test run` accepts:

- `--suite <path>` - test-suite directory (default: `.te-tests/`).
- `--tag <tag>` - only tests with this tag.
- `--fail-on <severity>` - `error` (default) or `warning`.
- `--ci <fmt>`, `--trx <path>` - CI annotations and TRX output.

```bash
te test run --ci github --trx results.trx
te test run --tag revenue
```

Suites are validated before any connection is made; a suite that fails validation (for example, a missing `query_file`) exits `1` without running anything. Under `--output-format json`, `te test run` emits the unified findings envelope with test-specific extras (`suites`, `invalidSuites`, `testSummary`) - see @te-cli-findings.

### test init / spec / use / list / snapshot / compare

`te test list` also accepts the `ls` alias.

Additional subcommands scaffold tests, print the assertion spec format, switch the active suite, list suites, capture snapshots, and compare models. See `te test --help` for details.

```bash
te test init --example             # Scaffold an example suite
te test spec                       # Print the full assertion format reference
te test init --from-model --model ./my-model  # Generate stubs from your measures
```

## Connection and authentication

### connect

Set (or display) the active connection for the current terminal session. See @te-cli-auth.

```bash
te connect                                # Show current active connection
te connect my-workspace my-model          # Remote (positional)
te connect -s my-workspace -d my-model    # Remote (named-flag form)
te connect ./model                        # Local
te connect --local                        # Local Analysis Services instance (Windows)
te connect --local my-model               # Match an instance (e.g. an open report's window title) or a database name
te connect --profile prod                 # Activate a saved profile
te connect --clear                        # Clear the active connection (and any workspace mirror)
```

`te connect --local` lists every local Analysis Services instance - Power BI Desktop (Store and installer versions), Visual Studio workspaces, and standalone SSAS - with a two-step prompt (instance, then database) when an instance hosts several databases. Non-interactive mode fails with the candidate list instead of picking silently; narrow it with `te connect --local <database>`.

#### Workspace mode (`-w` / `--workspace`)

Pair a primary source with a secondary target so every subsequent `--save` mirrors the model between the two. Useful for keeping a local working copy of a remote workspace, or pushing local edits to a workspace as you save.

- `te connect <ws> <model> -w ./src` - primary is remote; `./src` receives an initial TMDL export and mirrors every save.
- `te connect ./src -w <ws> <model>` - primary is local; an initial deploy pushes the model to the workspace, and subsequent saves re-deploy automatically.
- `--workspace-format <fmt>` - choose the on-disk format when mirroring to a folder/file: `tmdl`, `bim` (alias `tmsl`), or `database.json`. When omitted, the format is inferred from the workspace target path (e.g., `-w ./model.bim` infers BIM).
- `--workspace-auth <method>` - auth method for a remote workspace target when the primary is local. Defaults to `--auth` if set, else `auto`.
- `--force` - required when the target already exists (non-empty folder, existing database). Without it, `te connect` shows an interactive `y/n` prompt with `n` as the safe default.

Once active, `te set --save`, `te remove --save`, `te script --save`, etc. all dual-save transparently. Save order is always **local first, then remote** so the on-disk copy reflects the latest user change even if the server push fails. Clear the mirror with `te connect --clear`.

```bash
te connect Finance "Revenue Model" -w ./revenue-model    # Mirror remote → local TMDL
te connect ./revenue-model -w Finance "Revenue Model"    # Mirror local → remote
```

### auth login / status / logout

Manage cached authentication. See @te-cli-auth.

### profile list / show / set / remove

Manage named connection profiles. (`te profile list` alias: `ls`; `te profile remove` alias: `rm`.) See @te-cli-auth.

## Configuration

### config list / paths / init / set

View and manage CLI configuration. (`te config list` alias: `ls`.) See @te-cli-config.

`te config set` takes a positional `key value` pair or the equivalent `-p key=value`.

```bash
te config list                          # Display all settings
te config paths                         # Resolved macros and BPA rules file paths
te config init                          # Create default config
te config set autoFormat true
te config set -p spinner=false          # -p form
```

## Utilities

Model-free helpers. `te util` subcommands never touch a model - `--model`, `-s`/`-d`, `--local`, `--recent`, and `--auth` are rejected.

### util format-dax

Format a loose DAX expression.

- `<expression>` - the expression to format; `-` reads it from stdin.
- `--semicolons` - semicolons as list separators (European locale).
- `--long` - long format with fewer line breaks. Default is short.
- `--no-space-after-function` - skip the space after function names.

```bash
te util format-dax "SUM ( Sales[Amount] )"
cat query.dax | te util format-dax -
te util format-dax "SUM(Sales[Amount])" --semicolons
```

JSON output carries `success`, `formatted`, and `errors`. For expressions already in the model, use `te set <path> --format <PropertyName>` instead; for a whole-model sweep, `te script --inline "Model.AllMeasures.FormatDax();" --save`.

### util format-m

Format a loose M/Power Query expression. `-` reads from stdin; no language-specific options.

```bash
te util format-m "let x = 1 in x"
cat partition.m | te util format-m -
```

### util migrate

Reference guide showing how legacy Tabular Editor 2 CLI flags map to the new CLI. Useful as a live lookup while porting a TE2-based pipeline. See @te-cli-migrate for the full migration guide.

```bash
te util migrate                   # Full flag mapping table
te util migrate -A                # Look up a single TE2 flag
te util migrate --output-format json     # Machine-readable mapping
```

## Shell

### interactive

Start a guided REPL session with a model-aware prompt. See @te-cli-interactive.

> [!TIP]
> Running `te` in a terminal with no arguments also drops you into the REPL by default (as if you ran `te interactive`). Controlled by the `launchInteractiveMode` config key - see @te-cli-interactive#auto-launch-on-empty-invocation.

`te interactive` accepts:

- `--no-banner` - skip the welcome banner on startup. Useful when driving the REPL from scripts.
- `--echo` - echo each executed command to stdout before its output. Helpful when piping commands via stdin so the log shows what was run.
- `--batch` - non-interactive batch mode: read commands from stdin line by line, execute each, and exit on EOF. Automatically enabled when stdin is redirected.
- `--no-batch` - force interactive TTY mode even when stdin is redirected (mutually exclusive with `--batch`).

```bash
te interactive                                # Connect later
te interactive --model ./model                # Start with a local model
te interactive -s MyWorkspace -d MyModel      # Start with a remote model
printf "list Measures\nexit\n" | te interactive --model ./model   # Pipe commands via stdin
```

Inside the session, mutating commands stage in memory: `save` (no arguments) commits the staged edits and `revert` discards them, while `save-as` re-serializes to a format or location - see @te-cli-interactive.

Quoting and DAX-style references work the same as outside the session - see the [Object paths](#object-paths) section above and @te-cli-interactive for details on bracket-aware argv splitting inside the REPL.

### session

Show or manage the current terminal session. The CLI keeps per-terminal state (active connection, active profile, active test suite) in a session file, isolated per shell process. Set the `TE_SESSION` environment variable to share one named session across shells.

Subcommands:

| Subcommand | Purpose |
| -- | -- |
| `show` | Show current session details (ID, file path, active state). Default when no subcommand is given. |
| `list` (alias `ls`) | List all session files. |
| `clear` | Clear active state for the current session. |
| `prune` | Delete session files whose shell process is no longer running. |

`te session prune` accepts:

- `--all` - also remove sessions with live shells and named (`TE_SESSION`) sessions. The current session is always kept.
- `--dry-run` - show what would be removed without doing it.

```bash
te session                        # Show current session details
te session list                   # List all session files
te session clear                  # Clear active state for this session
te session prune                  # Remove sessions whose shell is dead
te session prune --all --dry-run  # Preview a full cleanup
```

### completion

Generate a shell completion script for `bash`, `zsh`, `powershell` (alias `pwsh`) or `fish`. See @te-cli-install.

```bash
te completion bash
te completion zsh
te completion pwsh
te completion fish
```

## Exit codes

| Exit | Meaning |
| -- | -- |
| `0` | Success. |
| `1` | Generic failure (invalid arguments, command failed, validation errors, auth failure, BPA gate failed at severity >= error). For `te diff`: differences found. |
| `2` | `te diff` only: an error occurred while comparing, so the difference status is unknown. |

For fine-grained control in CI pipelines, combine exit codes with `--ci <vsts/github>` annotations and `--trx` results files - see @te-cli-cicd.

## Related pages

- @te-cli - overview and framing.
- @te-cli-install - install and set up the CLI.
- @te-cli-auth - authenticate and manage connections.
- @te-cli-config - configuration file, BPA gate, post-mutation behavior.
- @te-cli-findings - the findings JSON shared by validate, bpa run, test run, and query.
- @te-cli-migrate - TE2 → TE3 flag mapping.
