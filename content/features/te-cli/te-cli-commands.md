---
uid: te-cli-commands
title: Command Reference
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
# Command Reference

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

This page gives a short description and one example per command. Every command accepts `--help` for exhaustive flag documentation:

```bash
te <command> --help
te <command> <subcommand> --help
```

> [!NOTE]
> During preview, the CLI's `--help` output is the authoritative reference for flags and options. The content on this page is hand-curated and will lag `--help` for anything added between preview releases.

## Object path syntax

Most commands accept object paths of the form:

- `Sales` — a table.
- `Sales/Revenue` — a measure or column.
- `Sales/Measures` — a sub-container inside a table (`Measures`, `Columns`, `Partitions`, `Hierarchies`).
- `Relationships`, `Roles`, `Perspectives`, `Cultures` — model-level containers.

Paths are consistent across `te get`, `te set`, `te add`, `te rm`, `te mv`, `te find`, `te replace`, and `te ls`.

## Global options

These flags are available on every command and sit before or after the subcommand name.

| Option | Description |
| -- | -- |
| `-m, --model <path>` | Path to semantic model (TMDL folder, `.bim` file, or TE folder). |
| `-s, --server <endpoint>` | Workspace name or endpoint (e.g., `MyWorkspace`, `powerbi://...`, `asazure://...`, `localhost`). |
| `-d, --database <name>` | Semantic model name on the workspace. |
| `--local` | Connect to a locally running Power BI Desktop instance (Windows only). |
| `--auth <method>` | Auth method: `auto`, `interactive`, `device-code`, `env`, `managed-identity` (default: `auto`). |
| `--output <format>` | Output format: `auto`, `text`, `json`, `csv` (default: `auto` — text for TTY, JSON for pipes). |
| `--recent [N]` | Use a recently used model. No value = interactive picker; `N` = Nth most recent (1 = last used). |
| `--non-interactive` | Disable all interactive prompts. Fail with an actionable error if required input is missing. |
| `--debug` | Enable debug logging to stderr (connection strings, auth flow, timing). |

For commands that read a model, the resolution order is: positional `<model>` argument → `--model` global flag → `--server`/`--database` (remote) → active connection from `te connect` → `--recent`.

## Model I/O

### load

Load a semantic model and display a summary.

```bash
te load ./model                            # TMDL folder
te load model.bim                          # BIM file
te load -s MyWorkspace -d MyModel          # Remote workspace
```

### save

Save a model to disk in a specified format.

- `-o, --output-path <path>` — target file or folder (required).
- `--format <fmt>` — `tmdl` (default), `bim`, `te-folder`, `pbip`, `database.json`.
- `--force` — skip validation and overwrite existing output.
- `--skip-bpa` / `--fix-bpa` — bypass or auto-fix the BPA gate.
- `--supporting-files` — generate Fabric supporting files (`.platform`, `definition.pbism`).

```bash
te save ./model.bim -o ./tmdl-out          # Convert BIM to TMDL
te save -o ./project --format pbip         # Save as a PBIP project
```

### export

Export a model from a workspace to local disk.

```bash
te export -o ./out -s my-workspace -d my-model
te export -o ./model.bim --format bim
```

### open

Open a model in Tabular Editor 3 Desktop (requires TE3 to be installed).

```bash
te open ./my-model
```

### init

Create a new empty semantic model at the given path.

```bash
te init ./new-model
```

## Model editing

### set

Set a property on a model object.

- `-q <property>` — property name (e.g., `expression`, `formatString`, `description`, `isHidden`).
- `-i <value>` — value (use `-` to read from stdin).
- `--save` / `--save-to <path>` — persist changes.

```bash
te set Sales/Amount -q expression -i "SUM(Sales[Amt])" --save
te set Sales -q isHidden -i true --save
```

### add

Add an object to the model. The type is inferred from the `.Type` suffix on the path:
`.Measure`, `.Table`, `.CalculatedColumn`, `.Role`, plus relationship shorthand
`"Sales[Key]->Dim[Key]"`.

```bash
te add Sales/Revenue.Measure -i "SUM(Sales[Amount])" --save
te add "Sales[ProdKey]->Product[ProdKey]" --save
```

For data-bound tables, `te add` also supports schema detection from SQL, Lakehouse, or Warehouse sources. See `te add --help` for `--source`, `--endpoint`, `--source-table`, `--columns`, etc.

### rm

Remove an object. Checks dependents by default; use `--force` to bypass, `--if-exists` for idempotent removes.

```bash
te rm Sales/Revenue --save
te rm Sales/Revenue --dry-run                # Preview only
te rm Sales/OldMeasure --if-exists --save    # Idempotent
```

### mv

Move or rename a model object.

```bash
te mv Sales/Revenue Finance/Revenue --save    # Move measure to another table
te mv Sales/Revenue Sales/TotalRevenue --save # Rename measure
```

### replace

Find and replace text across model objects. Dry-run by default; add `--save` to apply.

- `--in <scope>` — `names`, `expressions`, `descriptions`, `displayFolders`, `formatStrings`, `annotations`, `all`.
- `--regex`, `--case-sensitive`.

```bash
te replace "OldTable" "NewTable" --in expressions --save
te replace "SUM" "SUMX" --regex --in expressions --save
```

## Inspection

### ls

List objects with filesystem-like navigation.

```bash
te ls                           # Tables (active model)
te ls Sales                     # Columns and measures in Sales
te ls Sales/Measures            # Only measures
te ls --type measure            # All measures across tables
te ls --paths-only              # One path per line, suitable for piping
```

### get

Get properties of a model object.

- `-q, --query <property>` — fetch a single property (e.g. `expression`, `formatString`).

```bash
te get Sales/Amount -q expression          # Print DAX
te get Model -q description
```

### find

Search for text across model objects.

- `--in <scope>` — as per `te replace` (default `all`).
- `--regex`, `--case-sensitive`, `--paths-only`.

```bash
te find "CALCULATE" --in expressions
te find "Revenue" --in names
```

### diff

Compare two models for structural differences. Exit codes: `0` = identical, `1` = differences found, `2` = error.

```bash
te diff ./model-v1 ./model-v2
te diff old.bim new.bim
```

### deps

Analyze an object's upstream and downstream dependencies.

```bash
te deps "Sales/Revenue"
```

## Analysis and quality

### validate

Validate model expressions, schema integrity, and TOM errors.

- `--ci <fmt>` — emit CI annotations to stderr: `vsts` or `github`.
- `--trx <path>` — write results as a VSTEST `.trx` file.

```bash
te validate ./model
te validate --ci github --trx results.trx
```

### bpa run

Run Best Practice Analyzer rules against a model.

- `-r, --rules <file-or-url>` — additional BPA rule file(s); repeatable.
- `--fix` — apply auto-fix expressions where rules define them.
- `--fail-on <severity>` — `error` (default) or `warning`.
- `--ci <fmt>` / `--trx <path>` — CI annotations and TRX output.
- `--skip-bpa`, `--no-model-rules`, `--no-defaults`, `--rule <id>`, `--path <objectPath>`, `--vpax <file>`, `--vpa-rules`.

```bash
te bpa run --fail-on error --ci github
te bpa run --fix --save
te bpa run --rule PERF_UNUSED_HIDDEN_COLUMN
```

### bpa rules

List and inspect BPA rules from all sources (built-in, user, machine, model).

```bash
te bpa rules list              # Active rules
te bpa rules list --all        # Include disabled and ignored rules
te bpa rules list --ignored
```

### vertipaq

Analyze VertiPaq storage statistics.

- `--columns`, `--relationships`, `--partitions`, `--all`.
- `--export <file.vpax>` / `--import <file.vpax>` — round-trip to VPAX.
- `--obfuscate` — obfuscate names and expressions in exported VPAX.
- `--top <N>`, `--stats`, `--annotate`, `--save`.

```bash
te vertipaq                    # Columns by size (default)
te vertipaq --all              # Tables, columns, relationships, partitions
te vertipaq --export stats.vpax
te vertipaq --import stats.vpax  # Analyze offline
```

### format

Format DAX or M/Power Query expressions.

- `-e, --expression <text>` — format a single inline expression.
- `-p, --path <objectPath>` — format a specific measure/column.
- `--lang <dax|m>` — default `dax`.
- `--save` / `--save-to` — persist formatted expressions.

```bash
te format --save                                           # Format all DAX
te format -p Sales/Amount --save                           # Single measure
te format -e "SUM ( Sales[Amount] )"                       # Inline
te format --lang m --save                                  # Format M
```

## Execution

### query

Execute a DAX query against a deployed model.

- `-q, --query <dax>` — inline query.
- `-f, --file <file.dax>` — query from file.
- `--limit <N>` — default 100.
- `-o, --output-file <path>` — write results to file (`.csv`, `.tsv`, `.json`, `.dax`).
- `--trace`, `--cold`, `--plan`, `--runs <N>` — performance tracing and benchmarking.
- `--no-validate` — skip pre-execution DAX semantic validation.

```bash
te query -q "EVALUATE TOPN(5, 'Sales')" -s my-ws -d my-model
te query -f query.dax --output json
```

### script

Execute one or more C# scripts against a semantic model.

- `-S, --script <file>` — `.cs` / `.csx` file (repeatable).
- `-e, --expression <code>` — inline C# (use `-` for stdin).
- `--save` / `--save-to` / `--format`.
- `--dry-run`, `--timeout <seconds>`.

```bash
te script --script fix.cs --save
te script -e "Info(Model.Tables.Count)"
echo "Info(Model.Name);" | te script -e -
```

### macro

Manage and run Tabular Editor 3 macros from `MacroActions.json`.

```bash
te macro list                  # List macros
te macro run <name-or-id>      # Run a macro
te macro add <name>            # Add a macro
te macro set <name-or-id>      # Update macro properties
te macro rm <name-or-id>       # Remove a macro
te macro sort                  # Sort and re-assign IDs
```

## Deployment and refresh

### deploy

Deploy a semantic model to Power BI, Fabric, or Azure Analysis Services.

- `-s, --server` / `-d, --database` — target workspace and model.
- `--deploy-full` — overwrite + connections + partitions + shared expressions + roles + role members.
- `--deploy-connections`, `--deploy-partitions`, `--skip-refresh-policy`, `--deploy-roles`, `--deploy-role-members`, `--deploy-shared-expressions`, `--create-only`.
- `--xmla <file>` — generate XMLA/TMSL script instead of deploying (`-` for stdout).
- `--skip-bpa` / `--fix-bpa` — bypass or auto-fix the BPA gate.
- `--force` — skip interactive confirmation (required for CI).
- `--ci <fmt>` — `vsts` or `github`.
- `--profile <name>` — one-shot use of a saved @te-cli-auth profile.

```bash
te deploy ./model -s my-workspace -d my-model --force --ci github
te deploy ./model --xmla script.tmsl    # Generate TMSL only
te deploy ./model --profile staging --force
```

> [!IMPORTANT]
> `te deploy` runs the Best Practice Analyzer as a gate before executing. In interactive mode, a summary + confirmation prompt is shown with **`n` as the safe default**. In CI, pass `--force` to skip the prompt. See @te-cli-config for BPA gate configuration.

### refresh

Trigger a data refresh on a deployed model.

- `--type <type>` — `full`, `dataonly`, `automatic`, `calculate`, `clearvalues`, `defragment`, `add` (default: `automatic`).
- `--table <name>` — refresh specific table(s); repeatable.
- `--partition <Table.Partition>` — refresh specific partition(s).
- `--apply-refresh-policy`, `--effective-date <yyyy-MM-dd>`, `--max-parallelism <N>`.
- `--dry-run` — output the TMSL script without executing.
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

Additional subcommands (`set`, `remove`, `apply`) are documented via `te incremental-refresh --help`.

## Testing

### test run

Run a suite of DAX assertion tests against a deployed model.

- `--suite <path>` — test-suite directory (default: `.te-tests/`).
- `--tag <tag>` — only tests with this tag.
- `--fail-on <severity>` — `error` (default) or `warning`.
- `--ci <fmt>`, `--trx <path>` — CI annotations and TRX output.

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

## Connection and auth

### connect

Set (or display) the active connection for the current terminal session. See @te-cli-auth.

```bash
te connect                         # Show current active connection
te connect my-workspace my-model   # Remote
te connect ./model                 # Local
te connect --local                 # Power BI Desktop (Windows)
te connect --profile prod          # Activate a saved profile
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

### license

Manage CLI license state.

```bash
te license activate <key>
```

### migrate

Reference guide showing how legacy Tabular Editor 2 CLI flags map to the new CLI. Useful as a live lookup while porting a TE2-based pipeline. See @te-cli-migrate for the full migration guide.

```bash
te migrate                   # Full flag mapping table
te migrate -A                # Look up a single TE2 flag
te migrate --output json     # Machine-readable mapping
```

## Shell

### interactive

Start a guided REPL session with a model-aware prompt. See @te-cli-interactive.

```bash
te interactive                                # Connect later
te interactive ./model                        # Start with a local model
te interactive -s MyWorkspace -d MyModel      # Start with a remote model
```

### completion

Generate a shell completion script. See @te-cli-install.

```bash
te completion bash
te completion zsh
te completion pwsh
```

## Exit codes

| Exit | Meaning |
| -- | -- |
| `0` | Success. |
| `1` | Generic failure (invalid arguments, command failed, validation errors, auth failure, BPA gate failed at severity ≥ error). |
| `2` | Non-zero diff (`te diff`) — models differ. |

For fine-grained control in CI pipelines, combine exit codes with `--ci <vsts/github>` annotations and `--trx` results files — see @te-cli-cicd.

## Related pages

- @te-cli — overview and framing.
- @te-cli-install — install and set up the CLI.
- @te-cli-auth — authenticate and manage connections.
- @te-cli-config — configuration file, BPA gate, post-mutation behavior.
- @te-cli-migrate — TE2 → TE3 flag mapping.
