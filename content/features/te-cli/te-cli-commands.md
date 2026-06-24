---
uid: te-cli-commands
title: Command Reference
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

- **`<path>`** - resolves to **exactly one** object or container. Used by commands that operate on a single target: `te get`, `te set`, `te add`, `te rm`, `te mv`, `te format -p`, `te deps`, `te macro run --on`.
- **`<path-filter>`** - resolves to **zero or more** objects, with wildcard support. Used by commands that operate on a set: `te ls`, `te bpa run --path`, and other inspection-style commands.

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
| `Tables`, `Measures`, `Columns`, `Hierarchies`, `Partitions` | Model | All objects of that kind across the model. |
| `Relationships`, `Roles`, `Perspectives`, `Cultures`, `DataSources`, `Expressions`, `CalculationGroups`, `Functions`, `Annotations` | Model | Model-level containers. |
| `Measures`, `Columns`, `Hierarchies`, `Partitions`, `Calendars`, `CalculationItems` | Table | Sub-containers under a table. |
| `Levels` | Hierarchy | Levels of a hierarchy. |
| `Members`, `TablePermissions` (alias `Permissions`) | Role | Children of a role. |

A few examples show how plain and container-scoped paths differ:

```bash
te get Sales/Revenue                       # Measure or column on Sales
te get Sales/Measures/Revenue              # Same, container-scoped - disambiguates if other kinds share the name
te get Sales/Geography/Levels/Year         # Specific level of a hierarchy
te get Roles/Admin/Members/bob@example.com # Role member
te get Sales/refreshPolicy                 # Refresh-policy sub-object on a table
te get "Measures/Revenue/KPI"              # KPI sub-object of a measure
```

Quote a segment to force literal-name matching when a real object name happens to coincide with a keyword. The table literally named `Tables` is `'Tables'`, addressed by `te get "'Tables'"`.

### Wildcards in filter paths

Filter paths add a single wildcard character - `*` - that matches any run of characters within one segment (greedy, single-segment). Wildcards are how `te ls` and similar commands narrow their results.

```bash
te ls 'Sa*'                          # Tables whose name starts with Sa
te ls 'Sales/*Amount'                # Children of Sales whose name ends with Amount
te ls '*/Amount'                     # An Amount column/measure across every table
te ls 'Roles/Re*/Members'            # Members of every role matching Re*
```

A filter path with **N segments** produces **N-level-deep** results - wildcards never auto-expand a level beyond what you typed. The single-segment shortcut `te ls Sales` is the exception: an unqualified, non-wildcarded table name expands to the table's direct children to match the "show me what's in Sales" intent. `te ls Sa*`, in contrast, returns just the matching tables - no expansion.

DAX bracket-suffix is rejected in filter paths; quote names containing `[` and `]` if you need to match them literally.

### Errors and hints

Misspelled segments emit a contextual error with a "did you mean" hint when the CLI can guess what you meant. Missing-parent paths fail before the leaf check, so the message points at the segment that's actually wrong. Empty containers (e.g., `te ls Hierarchies` on a model without hierarchies) emit a simply "nothing here" hint rather than an error.

## Global options

These flags are available on every command and can be used before or after the subcommand name.

| Option | Description |
| -- | -- |
| `-m, --model <path>` | Path to semantic model (TMDL folder, `.bim` file, or TE folder). |
| `-s, --server <endpoint>` | Analysis Services endpoint or Power BI workspace. A server name/FQDN (`MY.SERVER.COM`), IP address (`192.168.1.1`), `host:port`, `localhost`, `SERVER\INSTANCE`, `asazure://...`, or an MSOLAP connection string connects directly to Analysis Services / AAS. A bare single-token name (`MyWorkspace`), a Fabric `Name.Workspace[/Model.SemanticModel]` path, or a `powerbi://...` URL targets a Power BI workspace. A workspace name containing a dot is indistinguishable from a server name, so it is treated as a server and the CLI prints a warning; use its `.Workspace` form or full `powerbi://` URL to target Power BI. |
| `-d, --database <name>` | Semantic model name on the workspace. |
| `--local` | Connect to a locally running Power BI Desktop instance (Windows only). |
| `--auth <method>` | Auth method: `auto`, `interactive`, `spn`, `env`, `managed-identity` (default: `auto`). |
| `--output-format <format>` | Stdout format: `text` (default), `json`, `csv`, `tmsl` (alias `bim`), `tmdl`. `csv` is honored by commands that emit tabular data; `tmsl`/`tmdl` only by `te get` and `te ls` for whole-object serialization. Commands reject formats they don't support. |
| `--error-format <format>` | Stderr format for errors, warnings, and hints: `text` (default) or `json`. Other values fall back to text. Independent of `--output-format`, so you can pair JSON stdout with plain-text errors (or vice versa). |
| `--recent [N]` | Use a recently used model. No value = interactive picker; `N` = Nth most recent (1 = last used). |
| `--non-interactive` | Disable all interactive prompts. Fail with an actionable error if required input is missing. |
| `--debug` | Enable debug logging to stderr (connection strings, auth flow, timing). |

`te --version` prints the CLI version and exits.

For commands that read a model, the resolution order is:

positional `<model>` argument → `--model` global flag → `--server`/`--database` (remote) → active connection from `te connect` → `--recent`.

## Model I/O

### load

Load a semantic model and display a summary of the model - name, compatibility level, and high-level object counts (tables, measures, columns).

```bash
te load ./model                            # TMDL folder
te load model.bim                          # BIM file
te load -s MyWorkspace -d MyModel          # Remote workspace
```

### save

Save a model to disk. Use it to write a remote workspace model to local files, convert formats, or persist edits back to the source.

`te save` accepts:

- `-o, --output-path <path>` - target file or folder. **Optional** - when omitted, `te save` writes back to the source location, preserving the original format. The file extension also drives format inference: `.bim` writes a single-file BIM, `.json` writes a `database.json` folder, and a bare path writes a TMDL folder.
- `--serialization <fmt>` - `tmdl`, `bim` (alias `tmsl`), `database.json`, `pbip`. When omitted, the format is inferred from the `-o` path extension (or from the loaded model when `-o` is omitted entirely).
- `--force` - skip validation and overwrite existing output. Some refusals (ambiguous containers, multi-`SemanticModel` project roots) fire even under `--force`.
- `--skip-bpa` - bypass the BPA gate entirely.
- `--fix-bpa` - auto-fix BPA violations where rules define a fix expression.
- `--bpa-rules <path>` - repeatable; override `bpa.rules` from your CLI config for this single save. Built-in rules still apply unless `bpa.builtInRules` is `false`.
- `--skip-validation` - skip DAX semantic analysis and validation for fast passthrough downloads.
- `--supporting-files` - generate Fabric supporting files (`.platform`, `definition.pbism`).

```bash
te save                                    # Save back to source (no -o needed)
te save ./model.bim -o ./tmdl-out          # Convert BIM to TMDL
te save -o ./project --serialization pbip         # Save as a PBIP project
te save -o ./out -s my-workspace -d my-model --skip-validation   # Fast download
```

> [!TIP]
> Use `te save -o <path> -s <workspace> -d <model>` to download a remote model to disk. Pair with `--skip-validation` for the fastest passthrough when you only need the bytes (no DAX semantic analysis).

### open

Open a model in Tabular Editor 3 Desktop. **Windows only** (requires TE3 to be installed). With no arguments, launches TE3 with a blank workspace.

```bash
te open                  # Launch TE3 with a blank workspace
te open ./my-model       # Open a TMDL folder in TE3
te open ./model.bim      # Open a BIM file in TE3
```

### init

Create a new empty semantic model at the given path. Defaults to a TMDL model in `PowerBI` compatibility mode at compatibility level 1702.

`te init` accepts:

- `<output-path>` - positional argument: directory to create the model in (omit to use the global `--model` path).
- `--compatibility-mode <mode>` - `PowerBI` (default) or `AnalysisServices`.
- `--compatibility-level <N>` (alias `--compat`) - compatibility level. Defaults to `1702` when the mode is `PowerBI`, `1500` otherwise. See @update-compatibility-level.
- `--name <name>` - model/database name (default: the directory name).
- `--serialization <fmt>` - `tmdl` (default), `bim` (alias `tmsl`), `database.json`, `pbip`.
- `--force` - replace any existing file or directory at the target path.

```bash
te init ./new-model                                       # TMDL, PowerBI mode, compat 1702
te init ./new-model --serialization bim                   # Single-file BIM model
te init ./as-model --compatibility-mode AnalysisServices  # AS model, compat 1500
te init ./existing-dir --force                            # Overwrite non-empty directory
```

## Model editing

### set

Set a property on a model object. Accepts a `<path>`.

`te set` accepts:

- `-q <property>` - property name (e.g., `expression`, `formatString`, `description`, `isHidden`). **Repeatable** - pair each `-q` with a following `-i` to set multiple properties in one command.
- `-i <value>` - value (use `-` to read from stdin). One `-i` per `-q`.
- `-t, --type <kind>` - disambiguation when the same path could resolve to multiple object kinds (`Measure`, `Column`, `CalculatedColumn`, `Hierarchy`, `Calendar`, `Partition`, `CalculationItem`).
- `--save` / `--save-to <path>` - persist changes.
- `--serialization <fmt>` - override the serialization when saving (`tmdl`, `bim` (alias `tmsl`), `database.json`).
- `--force` - save even if the mutation introduces DAX validation errors.

```bash
te set Sales/Amount -q expression -i "SUM(Sales[Amt])" --save
te set "'Net Sales'[Sales Amount]" -q formatString -i "#,0" --save   # DAX form with spaced names
te set Sales -q isHidden -i true --save
te set Sales/Amount -q formatString -i "#,0" -q description -i "Net sales" --save   # Multi-property
```

### add

Add an object to the model. Pass a `<path>` for the new object (the parent must already exist; the leaf segment is the new name) and the type via `-t` / `--type`. Relationships keep their shorthand syntax (`Sales[Key]->Dim[Key]`).

`te add` accepts:

- `-t, --type <type>` - object type. Common values: `Table`, `Measure`, `Column`, `CalculatedColumn`, `Hierarchy`, `Role`, `Perspective`, `Culture`, `CalculationGroup`, `CalculationItem`. Tab-completion is supported; the full list can be retrieved by running `te add --help`.
- `-i <value>` - expression or value to assign to the new object (DAX for measures/calculated columns, M for partitions, etc.). Pair with `-q` to set additional properties on the new object in the same command.
- `-q <property>` - additional property to set on the new object (repeatable; pairs with `-i`).
- `--file <path>` - read the expression for `-i` from a file instead of inline.
- `--mode <mode>` - storage mode for new tables: `import` (default), `directQuery`, `dual`, `directLake`.
- `--if-not-exists` - exit `0` without error if the object already exists. Use this for idempotent CI/CD pipelines.
- `--save` / `--save-to <path>` - persist changes.
- `--serialization <fmt>` - override the serialization when saving (`tmdl`, `bim` (alias `tmsl`), `database.json`).
- `--force` - save even if the mutation introduces DAX validation errors.

```bash
te add Sales/Revenue -t Measure -i "SUM(Sales[Amount])" --save
te add Sales -t Table --save
te add "Sales[ProdKey]->Product[ProdKey]" --save                           # Relationship shorthand
te add Sales/MarketingFlag -t CalculatedColumn -i "Sales[Amount] > 1000" --if-not-exists --save
te add Perspectives/Default/Sales --save                                   # Include Sales in the Default perspective
te add Roles/Reader -t Role --save                                         # New role at the model level
```

For data-bound tables, `te add` also supports schema detection from SQL, Lakehouse, or Warehouse sources. See `te add --help` for `--source`, `--endpoint`, `--source-table`, `--columns`, etc.

### rm

Remove an object. Checks dependents by default to prevent breaking existing references.

`te rm` accepts:

- `<path>` - positional argument: the object to remove.
- `-t, --type <kind>` - disambiguate when the path matches multiple table-children (e.g., a column and a hierarchy with the same name).
- `--force` - bypass the dependents check.
- `--if-exists` - exit `0` without error if the object doesn't exist. Use this for idempotent CI/CD pipelines.
- `--dry-run` - preview the removal without applying it.
- `--save` / `--save-to <path>` - persist the change.
- `--serialization <fmt>` - override the serialization when saving (`tmdl`, `bim` (alias `tmsl`), `database.json`).

```bash
te rm Sales/Revenue --save
te rm "'Sales'[Revenue]" --save              # DAX form
te rm Sales/Revenue --dry-run                # Preview only
te rm Sales/OldMeasure --if-exists --save    # Idempotent
```

### mv

Move or rename a model object. Both source and destination are `<path>` arguments.

`te mv` accepts:

- `-t, --type <kind>` - disambiguate when the source path matches multiple object kinds (e.g., a column and a hierarchy with the same name).
- `--save` / `--save-to <path>` - persist the change.
- `--serialization <fmt>` - override the serialization when saving (`tmdl`, `bim` (alias `tmsl`), `database.json`).
- `--force` - save even if the mutation introduces DAX validation errors.

```bash
te mv Sales/Revenue Finance/Revenue --save                # Move measure to another table
te mv Sales/Revenue Sales/TotalRevenue --save             # Rename measure
te mv Sales/Date Sales/CalendarDate -t Hierarchy --save   # Disambiguate hierarchy from column
```

### replace

Find and replace text across model objects. Dry-run by default; add `--save` to apply.

`te replace` accepts:

- `--in <scope>` - scope: `names`, `expressions`, `descriptions`, `displayFolders`, `formatStrings`, `annotations`, `all` (default: `all`).
- `--regex` - treat the find pattern as a regular expression.
- `--case-sensitive` - enable case-sensitive matching.
- `--dry-run` - preview changes without applying. Default behavior.
- `--save` - persist the mutation to the source location. Mutually exclusive with `--revert` and `--stage`.
- `--save-to <path>` - save to a different path (implies `--save`).
- `--serialization <fmt>` - model serialization: `tmdl`, `bim` (alias `tmsl`), `database.json`.
- `--force` - save even if the replacement introduces DAX validation errors.

`--in expressions` walks every expression-bearing property:

- **Measure**: `Expression`, `DetailRowsExpression`
- **KPI**: `TargetExpression`, `StatusExpression`, `TrendExpression`
- **Partition**: source M, polling M
- **Table permission**: `FilterExpression`
- **Calculation group**: selection expressions
- **Calculated column**: DAX expression

Adding new expression-shaped properties to the model surfaces them automatically.

```bash
te replace "OldTable" "NewTable" --in expressions --save
te replace "SUM" "SUMX" --regex --in expressions --save
```

## Inspection

### ls

List objects with filesystem-like navigation. Takes a `<path-filter>` argument supporting wildcards. Both model-level containers and table-scoped containers are supported - see the [container keyword table](#containers-and-keywords) above for the full list.

`te ls` accepts:

- `--type <kind>` - narrow to one object kind (`table`, `measure`, `column`, `hierarchy`, `partition`, `relationship`, `role`, `perspective`, `culture`). With no `<path-filter>` this is equivalent to typing the matching container keyword.
- `--paths-only` - emit one object path per line, suitable for piping to `xargs`, `te get`, or `te set`.
- `--no-multiline` - collapse multi-line cells (typically DAX or M expressions) to a single line and truncate, so rows stay scannable in wide tables. Text output only; JSON/CSV/TMSL output is unaffected.
- `--output-format tmsl` (alias `bim`) - emit the matching objects as a TMSL/BIM script. Useful for `te ls Tables --output-format bim > tables.json`. `--output-format tmdl` is not supported by `ls` (TMDL is single-object only - use `te get`).

```bash
te ls                                     # All tables in the model
te ls Sales                               # All children of Sales (columns + measures + hierarchies + partitions)
te ls Sales/Measures                      # Just Sales's measures
te ls 'Sales/*Amount'                     # Children of Sales whose name ends with Amount
te ls 'Sa*'                               # Tables whose name starts with Sa (no auto-expansion)
te ls '*/Amount'                          # An Amount column/measure across every table
te ls 'Roles/Re*/Members'                 # Members of every role matching Re*
te ls Sales/Geography/Levels              # All levels of the Geography hierarchy
te ls "'Net Sales'/'Sales Amount'"        # Quote names containing spaces
te ls Measures --paths-only               # One Table/Measure per line for piping
te ls --type measure                      # Same as `te ls Measures`
te ls Measures --no-multiline             # Wide table with column dividers, single-line DAX
te ls Tables --output-format bim > tables.json   # All tables emitted as TMSL/BIM
```

### get

Get properties of a model object. Takes a `<path>`.

`te get` accepts:

- `-q, --query <property>` - fetch a single property (e.g. `expression`, `formatString`).
- `-t, --type <kind>` - disambiguate when the path matches multiple table-children (e.g., a column and a hierarchy with the same name). Values: `Measure`, `Column`, `CalculatedColumn`, `Hierarchy`, `Calendar`, `Partition`, `CalculationItem`.
- `--output-format tmsl` (alias `bim`) - emit the resolved object as TMSL/BIM JSON.
- `--output-format tmdl` - emit the resolved object as TMDL (named objects only).

`te get` and `te ls` share a single descriptor catalog, so every property surfaces the same way across formats - the text table, JSON, and CSV all see the same set, and adding a new property to the model exposes it everywhere.

```bash
te get Sales/Amount -q expression                # Print DAX
te get "'Sales'[Amount]"                         # DAX form: same as Sales/Amount
te get "[Total Sales]"                           # Lone-bracket: model-wide measure-or-column
te get "'Net Sales'[Sales Amount]" -q expression # DAX form with spaced names
te get "Sales/Revenue/KPI"                       # KPI sub-object of a measure
te get Sales --output-format tmdl                       # Emit the table as TMDL
te get Sales --output-format bim                        # Emit the table as TMSL/BIM
te get Model -q description
```

### find

Search for text across model objects.

`te find` accepts:

- `--in <scope>` - as per `te replace` (default `all`).
- `--regex`, `--case-sensitive`, `--paths-only`.
- `--no-multiline` - collapse multi-line match context to a single line. Text output only.

`--in expressions` covers every `IExpressionObject` in the model - including KPI `TargetExpression` / `StatusExpression` / `TrendExpression`, measure `DetailRowsExpression`, partition source/polling M, table-permission `FilterExpression`, and calculation-group `MultipleOrEmptySelection` / `NoSelection` expressions - so a literal like `123` set on a KPI's target turns up the same way a measure body would.

```bash
te find "CALCULATE" --in expressions
te find "Revenue" --in names
te find "CALCULATE" --in expressions --paths-only | xargs -I{} te get {} -q expression
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

Analyze an object's upstream and downstream dependencies, or surface unused objects across the model. The single-object form takes a `<path>`.

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
te validate ./model
te validate --ci github --trx results.trx
te validate --errors-only                 # Hide warnings and anti-pattern hints
```

### bpa run

Run Best Practice Analyzer rules against a model.

`te bpa run` accepts:

- `<model>` - positional argument: path to model (alternative to the `--model` global flag).
- `-r, --rules <rules>` - path(s) or URL(s) to BPA rule file(s) in JSON format. Repeatable. Replaces the user-rule layer for this invocation: see [Rule sources and resolution](#rule-sources-and-resolution) below.
- `--no-model-rules` - exclude BPA rules embedded in the model's annotations.
- `--no-defaults` - exclude built-in default BPA rules.
- `--vpax <file>` - load VertiPaq Analyzer stats from a `.vpax` file to enable VPA-aware rules.
- `--vpa-rules` - include built-in VPA-aware rules (requires `--vpax` or a pre-annotated model).
- `--allow-external-rules` - allow fetching BPA rule files from URLs embedded in model annotations.
- `--rule <id>` - run only specific rule(s) by ID. Repeatable.
- `--path <path-filter>` - limit analysis to the tables containing the matched objects. Accepts literal names, container keywords, and wildcards (e.g., `'Sales'`, `'Sa*'`, `'Sales/Measures'`, `'*/Amount'`).
- `--fix` - apply fix expressions to auto-fix violations where possible.
- `--save` - save the model back to source after applying fixes.
- `--save-to <path>` - save the model to a different path after applying fixes.
- `--serialization <fmt>` - model serialization: `tmdl`, `bim` (alias `tmsl`), `database.json`.
- `--fail-on <severity>` - failure threshold: `error` (default) or `warning`. Exits with code `1` when violations meet the threshold.
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

#### Rule sources and resolution

Each `te bpa run` invocation assembles rules from three independent layers:

1. **User rules** - exactly one source wins, in priority order:
   - `-r, --rules <rules>` flag, accepts a file path or URL (highest)
   - `TE_BPA_RULES` environment variable
   - `bpa.rules` array from CLI config (`~/.config/te/config.json`)
2. **Built-in defaults** - loaded unless `--no-defaults` is passed or [`bpa.builtInRules`](xref:te-cli-config#built-in-bpa-rules) is `false` in config. Individual built-ins listed in `bpa.disabledBuiltInRuleIds` are skipped.
3. **Model-embedded rules** - rules in the model's `BestPracticeAnalyzer_Rules` annotation, loaded unless `--no-model-rules` is passed. External URL annotations are skipped unless `--allow-external-rules` is also passed.

Duplicate rule IDs are de-duplicated (user rules win over built-ins). Rule IDs in the model's `BestPracticeAnalyzer_IgnoreRules` annotation are then removed.

The `Rules loaded:` line in the output attributes each contributing layer, for example:

```
Rules loaded: 41 from 1 file(s) from bpa.rules config + built-in defaults + model annotations
```

### bpa rules

Manage BPA rule collections - list, inspect, initialize, and toggle rules in your local rules file or in model annotations. Built-in rules are read-only - to skip one without losing the rest, use `te bpa rules disable` (do not edit the built-in set directly).

Subcommands:

| Subcommand | Purpose |
| -- | -- |
| `add <id> [model]` | Add a new BPA rule. |
| [`disable`](#bpa-rules-disable) | Disable a built-in BPA rule for the current user. |
| [`enable`](#bpa-rules-enable) | Re-enable a previously disabled built-in BPA rule. |
| `ignore <rule-id> [model]` | Add a rule to the model's ignore list. |
| [`init`](#bpa-rules-init) | Create an empty BPA rules file at the resolved path. |
| [`list`](#bpa-rules-list) | List BPA rules from all sources with status. |
| `rm <rule-id> [model]` | Remove a BPA rule. |
| `set <rule-id> [model]` | Update a BPA rule's properties. |
| `unignore <rule-id> [model]` | Remove a rule from the model's ignore list. |

All `te bpa rules` subcommands accept:

- `--rules-file <path>` - path to a BPA rules JSON file. Defaults to the first existing entry of `bpa.rules` in your CLI config (`~/.config/te/config.json`), or the `TE_BPA_RULES` environment variable.
- `--model-rules` - operate on rules embedded in the model annotation instead of a file.

> [!IMPORTANT]
> `te bpa rules set` and `te bpa rules rm` refuse to mutate built-in rule IDs. Attempting to do so exits with code `1` and points at `te bpa rules disable`. To customize a built-in rule's behavior, disable the built-in and add a custom copy with a different ID:
>
> ```bash
> te bpa rules disable TE3_BUILT_IN_DATE_TABLE_EXISTS
> te bpa rules add MY_DATE_TABLE_EXISTS
> ```

#### bpa rules list

List rules from all sources (built-in, user, model).

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

Create an empty BPA rules file (`[]`) at the configured path. Use this once before invoking `te bpa rules set` / `te bpa rules rm` against a path that does not yet exist.

`te bpa rules init` accepts:

- `--force` - overwrite an existing file with `[]`. Required if the target file exists.
- `--rules-file <path>` - target file path. Can appear before or after the `init` subcommand.

Path resolution (first match wins): `--rules-file` → `TE_BPA_RULES` env var → first entry of `bpa.rules[]` in your CLI config → `./BPARules.json` (current working directory).

```bash
te bpa rules init
te bpa rules init --rules-file ./MyRules.json
te bpa rules init --force
```

#### bpa rules add / set / rm / ignore / unignore

Mutate the rules file (`add`, `set`, `rm`) or model-embedded ignore list (`ignore`, `unignore`). All three mutating subcommands operate on `--rules-file <path>` or `--model-rules` and refuse to touch built-in rule IDs.

- `te bpa rules add <id>` - create a new rule. Pass each property with `-q <name> -i <value>` pairs. Property names: `name`, `expression`, `scope`, `category`, `severity`, `description`, `fixExpression`.
- `te bpa rules set <id>` - update properties on an existing rule. Same `-q`/`-i` pairs as `add` (repeatable).
- `te bpa rules rm <id>` - remove a rule.
- `te bpa rules ignore <id>` - add a rule ID to the model's `BestPracticeAnalyzer_IgnoreRules` annotation.
- `te bpa rules unignore <id>` - remove a rule ID from the model's ignore list.

```bash
te bpa rules add MY_RULE -q name -i "My rule" -q expression -i "Measure" -q severity -i 2
te bpa rules set MY_RULE -q severity -i 3
te bpa rules rm MY_RULE
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

### format

Format DAX or M/Power Query expressions.

`te format` accepts:

- `-e, --expression <text>` - format a single inline expression.
- `-p, --path <path>` - format a specific measure/column.
- `-t, --type <kind>` - disambiguate when the path matches multiple table-children.
- `--lang <lang>` - expression language: `dax` (default) or `m`/`pq` for Power Query.
- `--semicolons` - use semicolons as list separators (European locale).
- `--long` - use long format (more line breaks). Default is short.
- `--no-space-after-function` - skip the space after function names.
- `--save` / `--save-to` - persist formatted expressions.

```bash
te format --save                                           # Format all DAX
te format -p Sales/Amount --save                           # Single measure
te format -e "SUM ( Sales[Amount] )"                       # Inline
te format --lang m --save                                  # Format M
```

## Execution

### query

Execute a DAX query against a deployed model.

`te query` accepts:

- `<dax>` - positional argument: the DAX query to execute. Equivalent to passing `-q`. Use whichever shape reads better; explicit `-q` wins if both are supplied.
- `-q, --query <dax>` - inline query (named-flag form of the positional above).
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

- `-S, --script <file>` - `.cs` / `.csx` file (repeatable).
- `-e, --expression <code>` - inline C# (use `-` for stdin).
- `--save` / `--save-to` / `--serialization`.
- `--dry-run` - compile the script(s) and report errors without executing them.

```bash
te script --script fix.cs --save
te script -e "Info(Model.Tables.Count)"
echo "Info(Model.Name);" | te script -e -
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
| `list` | List macros. |
| [`run <name-or-id>`](#macro-run) | Run a macro. |
| `add <name>` | Add a macro. |
| `set <name-or-id>` | Update macro properties. |
| `rm <name-or-id>` | Remove a macro. |
| `sort` | Sort and re-assign IDs. |
| [`init`](#macro-init) | Create an empty macros file at the resolved path. |

#### macro add / set / rm

Mutate the macros file (`add`, `set`, `rm`). All three operate on `--macros <path>` (or the resolved macros file).

- `te macro add <name>` - create a new macro. Provide the script body via `-e "<code>"` (inline) or `-s <file.cs>` (script file). Optional: `--tooltip <text>`, `--contexts <list>` (where the macro applies, e.g., `Table,Measure`), `--enabled true|false`.
- `te macro set <name-or-id>` - update macro properties. Use `-q <property> -i <value>` pairs (repeatable). Property names: `name`, `execute`, `enabled`, `tooltip`, `validContexts`.
- `te macro rm <name-or-id>` - remove a macro.

```bash
te macro add MyMacro -e "Info(Selected.Measure.Name);" --tooltip "Print measure name" --contexts Measure
te macro set MyMacro -q tooltip -i "Updated tooltip"
te macro rm MyMacro
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
- `--save` / `--save-to` - persist any changes the macro makes.

```bash
te macro run "Hide all measures"
te macro run "Format DAX" --on Sales/Revenue --save
te macro run "Format DAX" --on "'Net Sales'[Sales Amount]" --save   # DAX form works in --on too
```

## Deployment and refresh

### deploy

Deploy a semantic model to Power BI, Fabric, Azure Analysis Services, or on-prem SQL Server Analysis Services.

`te deploy` accepts:

- `-s, --server` / `-d, --database` - target server/workspace and model. A server name, FQDN, IP address, or MSOLAP connection string deploys to Analysis Services (Windows Integrated auth for on-prem); a workspace name or `powerbi://...` URL deploys to Power BI. See the [global options](#global-options) table for how `-s` is interpreted.
- `--deploy-full` - overwrite + connections + partitions + shared expressions + roles + role members.
- `--deploy-connections`
- `--deploy-partitions`
- `--skip-refresh-policy`
- `--deploy-roles`
- `--deploy-role-members`
- `--deploy-shared-expressions`
- `--create-only`
- `--xmla <file>` - generate XMLA/TMSL script instead of deploying (`-` for stdout).
- `--skip-bpa` - bypass the BPA gate entirely.
- `--fix-bpa` - auto-fix BPA violations where rules define a fix expression.
- `--bpa-rules <path>` - repeatable; override `bpa.rules` from your CLI config for this single deploy. Built-in rules still apply unless `bpa.builtInRules` is `false`.
- `--force` - skip interactive confirmation (required for CI).
- `--ci <fmt>` - `vsts` or `github`.
- `-p, --profile <name>` - one-shot use of a saved @te-cli-auth profile.

```bash
te deploy ./model -s my-workspace -d my-model --force --ci github
te deploy ./model -s MY.SERVER.COM -d my-model --force    # On-prem SSAS (Integrated auth)
te deploy ./model --xmla script.tmsl    # Generate TMSL only
te deploy ./model --profile staging --force
```

> [!IMPORTANT]
> `te deploy` runs the Best Practice Analyzer as a gate before executing. In interactive mode, a summary + confirmation prompt is shown with **`n` as the safe default**. In CI, pass `--force` to skip the prompt. See @te-cli-config for BPA gate configuration.

### refresh

Trigger a data refresh on a deployed model.

`te refresh` accepts:

- `--type <type>` - `full`, `dataonly` (alias `data-only`, `data`), `automatic` (alias `auto`), `calculate` (alias `calc`), `clearvalues` (alias `clear`), `defragment` (alias `defrag`), `add` (default: `automatic`).
- `--table <name>` - refresh specific table(s); repeatable.
- `--partition <Table.Partition>` - refresh specific partition(s).
- `--apply-refresh-policy` - apply the incremental refresh policy to determine which partitions are refreshed.
- `--effective-date <yyyy-MM-dd>` - set the effective date used by the refresh policy.
- `--max-parallelism <N>` - set the maximum number of partitions to refresh in parallel. Wraps the refresh in a TMSL `sequence` command.
- `--dry-run` - output the TMSL script without executing.
- `--no-progress`, `--trace [path]`.

```bash
te refresh --type full                                 # Full refresh
te refresh --table Sales --type full                    # Single table
te refresh --type full --dry-run > refresh.tmsl         # Emit TMSL only
```

### incremental-refresh

Manage incremental refresh policies on tables.

```bash
te incremental-refresh show <table>
```

Additional subcommands (`set`, `rm`, `apply`) are documented via `te incremental-refresh --help`.

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

### test init / spec / use / list / snapshot / compare

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
te connect --local                        # Power BI Desktop (Windows)
te connect --local my-report              # Filter by report name (multiple PBI Desktop instances)
te connect --profile prod                 # Activate a saved profile
te connect --clear                        # Clear the active connection (and any workspace mirror)
```

#### Workspace mode (`-w` / `--workspace`)

Pair a primary source with a secondary target so every subsequent `--save` mirrors the model between the two. Useful for keeping a local working copy of a remote workspace, or pushing local edits to a workspace as you save.

- `te connect <ws> <model> -w ./src` - primary is remote; `./src` receives an initial TMDL export and mirrors every save.
- `te connect ./src -w <ws> <model>` - primary is local; an initial deploy pushes the model to the workspace, and subsequent saves re-deploy automatically.
- `--workspace-format <fmt>` - choose the on-disk format when mirroring to a folder/file: `tmdl`, `bim` (alias `tmsl`), or `database.json`. When omitted, the format is inferred from the workspace target path (e.g., `-w ./model.bim` infers BIM).
- `--workspace-auth <method>` - auth method for a remote workspace target when the primary is local. Defaults to `--auth` if set, else `auto`.
- `--force` - required when the target already exists (non-empty folder, existing database). Without it, `te connect` shows an interactive `y/n` prompt with `n` as the safe default.

Once active, `te set --save`, `te rm --save`, `te script --save`, etc. all dual-save transparently. Save order is always **local first, then remote** so the on-disk copy reflects the latest user change even if the server push fails. Clear the mirror with `te connect --clear`.

```bash
te connect Finance "Revenue Model" -w ./revenue-model    # Mirror remote → local TMDL
te connect ./revenue-model -w Finance "Revenue Model"    # Mirror local → remote
```

### auth login / status / logout

Manage cached authentication. See @te-cli-auth.

### profile list / show / set / remove

Manage named connection profiles. See @te-cli-auth.

## Configuration

### config show / paths / init / set

View and manage CLI configuration and TE3 path overrides. See @te-cli-config.

```bash
te config show                          # Display all settings
te config paths                         # Resolved TE3 file paths
te config init                          # Create default config
te config set autoFormat true
```

### migrate

Reference guide showing how legacy Tabular Editor 2 CLI flags map to the new CLI. Useful as a live lookup while porting a TE2-based pipeline. See @te-cli-migrate for the full migration guide.

```bash
te migrate                   # Full flag mapping table
te migrate -A                # Look up a single TE2 flag
te migrate --output-format json     # Machine-readable mapping
```

## Shell

### interactive

Start a guided REPL session with a model-aware prompt. See @te-cli-interactive.

```bash
te interactive                                # Connect later
te interactive ./model                        # Start with a local model
te interactive -s MyWorkspace -d MyModel      # Start with a remote model
```

Quoting and DAX-style references work the same as outside the session - see the [Object paths](#object-paths) section above and @te-cli-interactive for details on bracket-aware argv splitting inside the REPL.

### session

Show or manage the current terminal session. The CLI keeps per-terminal state (active connection, active profile, active test suite) in a session file, isolated per shell process. Set the `TE_SESSION` environment variable to share one named session across shells.

Subcommands:

| Subcommand | Purpose |
| -- | -- |
| `show` | Show current session details (ID, file path, active state). Default when no subcommand is given. |
| `list` | List all session files. |
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
- @te-cli-migrate - TE2 → TE3 flag mapping.
