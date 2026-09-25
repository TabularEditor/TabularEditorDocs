---
uid: te-cli-commands
title: 命令参考
author: Peer Grønnerup
updated: 2026-09-11
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      none: true
    - product: Tabular Editor CLI
      full: true
---

# 命令参考

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

This page gives a short description and one example per command. 每个命令都支持 `--help`，可查看详尽的标志与选项说明：

```bash
te deploy --help            # Help for a single command
te bpa run --help           # Help for a command with subcommands
```

> [!NOTE]
> 在预览版期间，CLI 的 `--help` 输出是标志和选项的权威参考。 The content on this page is hand-curated and will lag `--help` for anything added between preview releases.

## 对象路径

CLI 中的对象定位在所有命令中都采用同一套语法。 Two flavours of path appear in the reference below:

- **`<path>`** - resolves to **exactly one** object or container. Used by commands that change the model or need a single target: `te set`, `te add`, `te remove`, `te move`, `te deps`, `te macro run --on`, and `te get` with `-p`, `--deps`, or `--properties`.
- **`<path-filter>`** - 解析为**零个或多个**对象，并支持通配符。 Used by commands that operate on a set: `te list`, plain `te get` (a wildcard or container path lists every match), `te bpa run --path`, and other inspection-style commands.

两种路径形式共用同一套语法规则；仅有两处不同：

- 筛选路径允许使用 `*` 通配符；对象路径不允许。
- 对象路径允许使用 DAX 方括号后缀（例如 `Sales[Amount]`）；筛选路径不允许。

### 分段和分隔符

路径是由斜杠分隔的 **分段** 序列。 Each segment names a single step - a table, a child object, or a container keyword.

- `Sales` - one segment
- `Sales/Revenue` - two segments
- `Roles/Admin/Members/bob` - four segments

空输入和 `.` 都表示“模型根”——它既是筛选路径的隐式起点，也是 `te get .` 这类查询显式指向的对象。

### 引号

Most segment names work as-is. Quote a segment when its name contains spaces, slashes, brackets, or any character that would otherwise be parsed as syntax. The CLI follows DAX quoting conventions, so quoting in `te` paths matches what you'd type inside a DAX expression:

| 形式               | 用途                                                                                                                      | 转义规则                                         |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| `'Net Sales'`    | 表，以及名称中带空格的对象。                                                                                                          | 将引号写两次（`'Bob''s'` → `Bob's`）。                |
| `"Net Sales"`    | 同上；当单引号转义不方便时，跨不同 shell 使用会更省事。                                                                                         | 将引号写两次（`"He said ""hi"""` → `He said "hi"`）。 |
| `[Sales Amount]` | 表引用中的 DAX 方括号后缀（`'Sales'[Sales Amount]`），或不带表前缀、在整个模型范围内解析的单独方括号引用（`[Total Sales]`）。 Object paths only. | 将右方括号写两次（`[foo]]bar]` → `foo]bar`）。          |

Inside quoted segments, `*` is treated as a literal character, not a wildcard. 因此，`'Sa*'` 会匹配名称恰好为 `Sa*` 的表。

The reserved characters in paths are `/ [ ] ' " * ? { }`. A segment containing any of `* ? { }` must be quoted (`te get "Tables/'{foo}'"`, `te get 'Sales/"my*name"'`); unquoted use is rejected with an error naming the character and showing the quoted form. `?` is reserved and has no wildcard meaning. Every path the CLI prints - in errors, hints, `--paths-only` output, and the `objectPath` field in JSON - is canonically quoted and can be pasted straight back into `te get`. The mixed-quote forms require PowerShell or bash; cmd.exe cannot express them.

### DAX 风格的引用（仅对象路径）

凡是允许使用 `<path>` 的位置，都接受两种 DAX 形式：

- **`'Table'[Member]`**：等同于 `Table/Member`。 The bracket-suffix biases ambiguous matches toward columns and measures over hierarchies/partitions.
- **`[Member]`**：一个独立的度量值或列，前面不带表名。 Searches the whole model for a measure or column with that name. Measures win when both exist.

```bash
te get "'Sales'[Amount]"             # Same as te get Sales/Amount
te get "'Net Sales'[Sales Amount]"   # Spaced names via DAX form
te get "[Total Sales]"               # Model-wide measure-or-column lookup
```

### 容器和关键字

Several names act as container keywords. 关键字既可以单独使用（列出整个容器），也可以出现在路径中（跳转到当前父级下的该子集合）。

| 关键字                                                                                                                   | 作用范围 | 含义                                  |
| --------------------------------------------------------------------------------------------------------------------- | ---- | ----------------------------------- |
| `Tables`, `Measures`, `Columns`, `Hierarchies`, `Partitions`, `KPIs`, `Sets`                                          | 模型   | 模型中该类型的所有对象。                        |
| `关系`, `角色`, `Perspectives`, `Cultures`, `DataSources`, `Expressions`, `CalculationGroups`, `Functions`, `Annotations` | 模型   | 模型级容器。                              |
| `Measures`, `Columns`, `Hierarchies`, `Partitions`, `Calendars`, `CalculationItems`, `KPIs`, `Sets`                   | 表    | 表下的子容器。                             |
| `Levels`                                                                                                              | 层次结构 | 层次结构的级别。                            |
| `Members`, `TablePermissions`（别名 `Permissions`）                                                                       | 角色   | Children of a role. |

Calculated sets are addressable in container form only (`<table>/Sets/<name>`); an individual KPI is `<table>/<measure>/KPI`; calendars resolve at `<table>/Calendars/<name>`; relationships resolve at `Relationships/<name>` (the relationship's own name in the model: a GUID, or a label such as `Relationship 1`; `--paths-only` prints it, and the display name is also accepted).

以下示例展示普通路径与限定容器范围的路径之间的区别：

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

筛选路径中不支持 DAX 的方括号后缀；如需按字面匹配包含 `[` 和 `]` 的名称，请给名称加引号。

### 错误和提示

Misspelled segments emit a contextual error with a "did you mean" hint when the CLI can guess what you meant. The list offers tables, measures, columns, and hierarchies, each as a full `Table/Object` path that pastes straight back into the next command. A name written in single quotes is a table reference (`te deps 'Revenue'` looks for a table named Revenue), and the error points at the `Table/Object` and `"[Object]"` forms for anything that is not a table. Missing-parent paths fail before the leaf check, so the message points at the segment that's actually wrong. Every path an error or hint prints is taken from your model and quoted so it resolves as printed - a refusal never suggests a path that does not exist. Empty containers (e.g., `te list Hierarchies` on a model without hierarchies) emit a simple "nothing here" hint rather than an error.

## Command aliases

Most long-form verbs also accept a short alias. Each row shows the canonical command and the equivalent short-form command it accepts as an alias.

| Canonical             | Aliased form(s) |
| --------------------- | ---------------------------------- |
| `te save-as`          | `te save`                          |
| `te list`             | `te ls`                            |
| `te remove`           | `te rm`                            |
| `te move`             | `te mv`, `te rename`               |
| `te bpa rules list`   | `te bpa rules ls`                  |
| `te bpa rules remove` | `te bpa rules rm`                  |
| `te config list`      | `te config ls`                     |
| `te macro list`       | `te macro ls`                      |
| `te macro remove`     | `te macro rm`                      |
| `te profile list`     | `te profile ls`                    |
| `te profile remove`   | `te profile rm`                    |
| `te session list`     | `te session ls`                    |
| `te test list`        | `te test ls`                       |

## 全局选项

这些标志适用于每个命令，可在子命令名称之前或之后使用。

| 选项                         | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `-m, --model <path>`       | Path to semantic model (TMDL folder, `.bim` file, `database.json` folder, or `.SemanticModel` folder).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `-s, --server <endpoint>`  | Analysis Services endpoint or Power BI workspace. A server name/FQDN (`MY.SERVER.COM`), IP address (`192.168.1.1`), `host:port`, `localhost`, `SERVER\INSTANCE`, `asazure://...`, or an MSOLAP connection string connects directly to Analysis Services / AAS. A bare single-token name (`MyWorkspace`), a Fabric `Name.Workspace[/Model.SemanticModel]` path, or a `powerbi://...` URL targets a Power BI workspace. A workspace name containing a dot is indistinguishable from a server name, so it is treated as a server and the CLI prints a warning; use its `.Workspace` form or full `powerbi://` URL to target Power BI. |
| `-d, --database <name>`    | Workspace 上的语义模型名称。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `--local`                  | Connect to a locally running Analysis Services instance - Power BI Desktop, Visual Studio workspaces, or standalone SSAS (Windows only).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `--auth <method>`          | 身份验证方法：`auto`、`interactive`、`spn`、`env`、`managed-identity`（默认值：`auto`）。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `--output-format <format>` | 标准输出格式：`text` (默认)、`json`、`csv`、`tmsl` (别名 `bim`)、`tmdl`。 `csv` is honored by commands that emit tabular data; `tmsl`/`tmdl` only by `te get` and `te list` for whole-object serialization. Commands reject formats they don't support.                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `--error-format <format>`  | Stderr format for errors, warnings, and hints: `text` (default) or `json`. Other values fall back to text. 它独立于 `--output-format`，因此你可以将 JSON 格式的 stdout 与纯文本错误配合使用（反之亦然）。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `--recent [N]`             | Use a recently used model. 未提供值 = 进入交互式选择器；`N` = 最近使用列表中的第 N 个（1 = 最近一次使用）。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `--non-interactive`        | Disable all interactive prompts. Fail with an actionable error if required input is missing.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `--debug`                  | Enable debug logging to stderr (connection strings, auth flow, timing).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |

`te --version` prints the CLI version and exits.

对于读取模型的命令，解析顺序如下：

`--recent` → `--local` → `--server`/`--database` (remote) → `--model` → active connection from `te connect`.

The model is never a positional argument - a stray path on the command line is rejected with an "unrecognized command or argument" error. (Positional arguments on `te connect`, `te init`, `te diff`, and `te query` are those commands' own subjects, not the model.)

> [!NOTE]
> **Mistyped options are rejected up front.** If you pass a `--flag` that isn't recognised on the command you invoked, the CLI exits with an actionable error rather than silently absorbing the token as a positional argument. This catches typos like `--force ` accidentally becoming `--forec` in CI scripts.

> [!NOTE]
> **Dotted server names.** `-s`/`--server` treats a dotted name (e.g. `Sales.2026`) as an Analysis Services server hostname, not a Power BI workspace. A warning fires when the CLI has to make this call, with a hint to append `.Workspace` (e.g. `Sales.2026.Workspace`) or use a full `powerbi://` URL if you meant the Power BI workspace. Applies to `te connect`, `te deploy`, `te refresh`, `te query`, `te vertipaq`, and `te test run`.

## Model initialization and save

### save-as

Re-serialize a model to a different format or location. 可用于将远程 Workspace 中的模型写入本地文件、转换格式，或将编辑内容保存回源位置。 (Alias: `save`.)

`te save-as` accepts:

- `-o, --output-path <path>` - 目标文件或文件夹。 **Optional** - when omitted, `te save-as` writes back to the source location, preserving the original format.
- `--serialization <fmt>` - `tmdl`, `bim` (alias `tmsl`), `database.json`, `pbip`. When omitted, the format is the loaded model's format; with `-o`, it is inferred from the output path (`.bim` writes a single-file BIM, `.json` a `database.json` folder).
- `--force` - skip validation and overwrite existing output. Some refusals (ambiguous containers, multi-`SemanticModel` project roots) fire even under `--force`.
- `--skip-bpa` - 完全跳过 BPA 门控检查。
- `--fix-bpa` - 如果规则定义了修复表达式，则自动修复 BPA 违规项。
- `--bpa-rules <path>` - 可重复指定；仅对本次保存覆盖 CLI 配置中的 `bpa.rules`。除非 `bpa.builtInRules` 为 `false`，否则内置规则仍会生效。
- `--skip-validation` - 跳过 DAX 语义分析和验证，以实现快速直通下载。
- `--supporting-files` - 生成 Fabric 支持文件（`.platform`、`definition.pbism`）。

```bash
te save-as                                    # Save back to source (no -o needed)
te save-as -m ./model.bim -o ./tmdl-out       # Convert BIM to TMDL
te save-as -o ./project --serialization pbip         # Save as a PBIP project
te save-as -o ./out -s my-workspace -d my-model --skip-validation   # Fast download
```

`--serialization pbip` output opens directly in Power BI Desktop and is named after the source model (`SpaceParts.pbip`, not `Model.pbip`). Saving into a folder that already holds a project adds only the files that are missing and leaves everything already there - the report's pages, theme, connection, and item identity - exactly as it was, so a save that changes nothing leaves the project unchanged under source control.

Validation guards saving: a model with a name collision Analysis Services would refuse (`TE0012` / `TE0013`, see [validate](#validate)) is not written unless `--force` or `--skip-validation` is passed.

> [!TIP]
> Use `te save-as -o <path> -s <workspace> -d <model>` to download a remote model to disk. Pair with `--skip-validation` for the fastest passthrough when you only need the bytes (no DAX semantic analysis).

### init

在指定路径创建一个新的空语义模型。 Defaults to a TMDL model in `PowerBI` compatibility mode at compatibility level 1705.

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

## 模型编辑

Mutating commands (`set`, `add`, `remove`, `move`, and also `script`, `macro run`, `bpa run --fix`) are **dry runs by default**: without `--save` the command reports what would change and discards it (`Dry run - nothing saved. Add --save to persist.`). Add `--save` to persist to the source, or `--save-to <path>` to write elsewhere. On `set`, `add`, `remove`, `move`, `script`, and `bpa run`, the change output renders as a unified diff per changed object; switch it with `--stat` or `--name-only` (mutually exclusive with `--diff`, the default), or set a standing default with `te config set mutationOutput diff|stat|name-only|none`. JSON output always carries the full changes array. A save is refused when the mutation introduces new DAX validation errors, unless `--force`.

### set

Set properties on a model object, format its expressions, or sync a table with its source schema. Accepts a `<path>`.

`te set` 接受以下参数：

- `-p, --property <Name=Value>` - property assignment (e.g., `-p expression="SUM(Sales[Amt])"`, `-p isHidden=true`). **Repeatable** - everything after the first `=` is the value. Bare positional assignments work too: `te set Sales/Amount formatString="#,0" --save`. Property names are case-insensitive, accept both spellings where the grid label and the TOM name differ (`Hidden` and `IsHidden`), and accept dotted paths and indexers: `-p KPI.StatusGraphic=...`, `-p "Annotations[Tabular Editor]=..."`, `-p "TranslatedNames[fr-FR]=..."`. Run `te get <path> --properties` to list every name an object accepts - see [get](#get). A partition's expression is `-p Expression` whatever kind of partition it is (`MExpression` and `Query` still work). Use `-p Name=-` to read the value from stdin (one assignment per stream; a piped value is taken verbatim, so piping the text `null` stores the word `null`). `-p Name=` assigns an empty string.
- `--unset <Name>` - clear a property; repeatable (`--unset description --unset displayFolder`). `-p Name=null` is the shorthand. Works on every property that can hold nothing - text properties included - and on object-valued ones (`SortByColumn`, `RefreshPolicy`); `-p "Annotations[key]=null"` removes an annotation. Numbers, booleans, and fixed-choice properties cannot be cleared and are refused.
- `--format <PropertyName>` - format that expression property (repeatable; DAX or M is detected from the property). The formatter tweaks `--long` (fewer line breaks) and `--no-space-after-function` require `--format` on a DAX property. `--semicolons` is refused together with `--format`: an expression stored in a model is always comma-separated, so the semicolon dialect can never parse it - format semicolon-authored DAX with [`te util format-dax --semicolons`](#util-format-dax) instead.
- `--update-schema` - sync a table's columns with its source schema: adds new source columns with detected types, retypes drifted ones, and preserves everything else about every existing column (name, description, format string, display folder, sort-by column, visibility, annotations, translations, perspective membership). Removed source columns only warn unless `--drop-removed-columns` (destructive). A renamed source column looks like remove + add - remap it first with `-p SourceColumn=<newName>`. Refused on calculated tables and calculation groups; cannot combine with `-p` or `--format`. With no connection flags, the connection is read from the model itself - the data source the table's partitions are bound to, the connection written into the table's own query, or the model's single usable data source - and the source table from the partition's binding, falling back to the model table's name; `--data-source <name>` chooses when the model has several usable sources. Naming a connection explicitly with the schema-detection flags shared with `te add` (`--source sql|lakehouse|warehouse`, `--endpoint`, `--connection-string`, `--source-database`, `--source-table`) always wins. When no source can be worked out, or the source table cannot be found, the error says which case you are in and names the table it looked for.
- `-t, --type <kind>` - disambiguation when the same path could resolve to multiple object kinds (`Measure`, `Column`, `CalculatedColumn`, `Hierarchy`, `Calendar`, `Partition`, `CalculationItem`).
- `--save` / `--save-to <path>` - 保存更改。
- `--diff` / `--stat` / `--name-only` - change-output rendering (see the note above).
- `--serialization <fmt>` - override the serialization when saving (`tmdl`, `bim` (alias `tmsl`), `database.json`).
- `--force` - save even if the mutation introduces DAX validation errors.

```bash
te set Sales/Amount -p expression="SUM(Sales[Amt])" --save
te set "'Net Sales'[Sales Amount]" -p formatString="#,0" --save        # DAX form with spaced names
te set Sales -p isHidden=true --save
te set Sales/Amount -p formatString="#,0" -p description="Net sales" --save   # Multiple properties, one atomic change
te set "Sales/Total Sales" --unset description --save                   # Clear a property (same as -p description=null)
te set Sales/Amount --format Expression --save                          # Format one expression property
te set Sales --update-schema --save                                     # Sync columns with the source schema (connection inferred from the model)
te set Sales --update-schema --data-source "Sales DW" --save            # Pick the data source when the model has several
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

Add an object to the model. 为新对象传入 `<path>`（父级必须已存在；最后一个分段就是新名称），并通过 `-t` / `--type` 指定类型。 Relationships keep their shorthand syntax (`Sales[Key]->Dim[Key]`). Container-form paths are valid add targets (`Sales/Measures/Margin`, `Sales/Partitions/Q1`, `Sales/Calendars/Fiscal`, `Roles/Admin/TablePermissions/Sales`, `Roles/Admin/Members/user@x.com`) - any path the CLI prints can be fed back to `te add`.

`te add` 支持以下选项：

- `-t, --type <type>` - object type. Common values: `Table`, `CalculatedTable`, `CalcGroup`, `Measure`, `CalculatedColumn`, `DataColumn`, `Hierarchy`, `Level`, `Calendar`, `CalcItem`, `KPI`, `Partition`, `Expression`, `Function`, `Perspective`, `Culture`, `Role`, `TablePermission`, `Member`. Tab-completion is supported; the full list can be retrieved by running `te add --help`.
- `-p, --property <Name=Value>` - property assignment on the new object (repeatable). The expression goes in `-p Expression="..."`, or use `--file`, or `-p Expression=-` to read it from stdin.
- `--file <path>` - read the expression from a file instead of inline.
- `--mode <mode>` - storage mode for new tables: `import` (default), `directquery` (alias `dq`), `dual`, `directlake` (alias `dl`).
- `--if-not-exists` - exit `0` without error if the object already exists. Use this for idempotent CI/CD pipelines.
- `--save` / `--save-to <path>` - 保存更改。
- `--diff` / `--stat` / `--name-only` - change-output rendering (see the [Model editing](#model-editing) note).
- `--serialization <fmt>` - override the serialization when saving (`tmdl`, `bim` (alias `tmsl`), `database.json`, `pbip`).
- `--source-type <kind>` - initial partition source type on a new table: `m`, `query`, or `calculated`. Overrides heuristic detection. `query` builds a legacy SQL `SELECT` partition bound to the model's provider data source and is refused with lakehouse/warehouse sources or when no provider source exists; `calculated` is only valid with `-t CalculatedTable`.
- `--partition-expression <m>` - raw M expression for the new table's initial partition.
- `--force` - save even if the mutation introduces DAX validation errors.

Adding a single data column to an existing table takes `-t DataColumn` with both `SourceColumn` and `DataType` required (refused on calculated tables and calculation groups):

```bash
te add Sales/Quantity -t DataColumn -p SourceColumn=Qty -p DataType=Int64 --save
```

Tables can be created in one shot from the model's **own** data source - no connection flags needed. The CLI reads the connection off the model's data source, discovers the source table's columns and their types, and creates the table with a partition already bound to that source. Over a legacy (provider) data source the partition is a legacy SQL query holding the generated `SELECT`, matching what the desktop **Import Tables** wizard writes; pass `--source-type m` for a Power Query (M) partition instead. Over a structured (Power Query) data source the partition is always M. Refusals are clean and create nothing: several usable data sources and no `--data-source`, no data source the CLI can read (SQL Server, Azure SQL, and Fabric SQL sources are covered), a source whose password the model does not store, or a source table the connection cannot find - the error names the table it looked for and where that name came from.

- `--source-table <schema.table>` - create the table from this source table.
- `--query "SELECT ..."` - create the table from a query instead: the query is described against the connection without being run, the new table gets exactly the columns it returns, and the query is kept as the partition's content. Works with an inferred connection and with one named explicitly. `--source-type query` places the SQL in a legacy Query partition bound to the model's legacy data source. Refused together with `--mode directlake` (a Direct Lake partition holds no query), with `--columns`, and with an expression of its own (`-p Expression=` or `--file`).
- `--data-source "<name>"` - disambiguate when the model has several data sources.

Schema detection against an explicit source also works, and always wins over inference: `--source sql|lakehouse|warehouse`, `--endpoint`, `--connection-string`, `--source-database`, `--source-table`, or a manual column spec `--columns "Id:Int64,Name:String"`. `te add "<table>" -t Table` with no source at all still creates an empty table to fill in yourself.

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

移动或重命名模型对象。 Both source and destination are `<path>` arguments. (Aliases: `mv`, `rename`.)

`te move` accepts:

- `-t, --type <kind>` - disambiguate when the source path matches multiple object kinds (e.g., a column and a hierarchy with the same name).
- `--save` / `--save-to <path>` - persist the change.
- `--diff` / `--stat` / `--name-only` - change-output rendering (see the [Model editing](#model-editing) note).
- `--serialization <fmt>` - override the serialization when saving (`tmdl`, `bim` (alias `tmsl`), `database.json`).
- `--force` - save even if the mutation introduces DAX validation errors.

Renaming an object whose name is not yours to set is refused with a non-zero exit code rather than reported as `No changes.` - a relationship (its name always describes the columns it joins), a measure's KPI, a role's table permission.

```bash
te move Sales/Revenue Finance/Revenue --save                # Move measure to another table
te move Sales/Revenue Sales/TotalRevenue --save             # Rename measure
te move Sales/Date Sales/CalendarDate -t Hierarchy --save   # Disambiguate hierarchy from column
te move "Sales/Partitions/Old" "Sales/Partitions/New" --save   # Container-form paths work too
```

## 检查

### list

List objects with filesystem-like navigation. Takes a `<path-filter>` argument supporting wildcards. Both model-level containers and table-scoped containers are supported - see the [container keyword table](#containers-and-keywords) above for the full list. (Alias: `ls`.)

`te list` accepts:

- `--type <kind>` - narrow to one object kind (`table`, `measure`, `column`, `hierarchy`, `partition`, `relationship`, `role`, `perspective`, `culture`, `calculationitem`, `kpi`, `set`, `function`). With no `<path-filter>` this is equivalent to typing the matching container keyword.
- `--paths-only` - 每行输出一个对象路径，适合通过管道传给 `xargs`、`te get` 或 `te set`。
- `--no-multiline` - 将多行单元格（通常是 DAX 或 M 表达式）折叠为单行并截断，让宽表中的各行仍便于浏览。 Text output only; JSON/CSV/TMSL output is unaffected.
- `--output-format tmsl`（别名 `bim`）- 将匹配的对象输出为 TMSL/BIM 脚本。 Useful for `te list Tables --output-format bim > tables.json`. `--output-format tmdl` is not supported by `ls` (TMDL is single-object only - use `te get`).

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

Get properties of a model object, filter and list sets of objects, and analyze dependencies - `get` is the CLI's one read pipeline (`te list` and `te deps` remain as shortcuts). Takes a `<path>`; omit it to list the model (same as `te list`), or pass `.` for the model root. A wildcard path (`te get "Sa*"`) or a container path (`te get Sales/Measures`) lists every match without needing `--ls`; `-p`, `--deps`, and `--properties` need exactly one object, so on a wildcard path they say so and suggest dropping the flag.

`te get` 支持：

- `-p, --property <property>` - project a single property (e.g. `expression`, `formatString`).
- `--where <Prop=Value>` - filter the result set; repeatable (AND), case-insensitive. A value with no `*` is an exact match; `*` is a wildcard, so a contains-search is `--where Name=*margin*`. With no path, `--where` filters the model's **top-level tables** - pass a container to search other kinds (`te get Measures --where Name=*margin*`). An empty result names what was searched and how the pattern was matched, and offers commands that widen the search.
- `--properties` - list the property names `-p` accepts on the resolved object, with each property's type, whether it can be written, what it holds, and - where a property takes a fixed set of values - the values it accepts. Both spellings are shown where they differ (`Hidden` / `IsHidden`), and annotations and translations appear in the bracket form they have to be written in. Internal bookkeeping properties are left out; `--all` adds them. Text and JSON output only; needs a single-object path and cannot combine with `-p`, `--ls`, `--where`, `--deps`, or `--unused`.
- `--ls` - compact table layout (the same rendering as `te list`).
- `--deps [upstream|downstream]` - dependency analysis (default: both directions); `--deep` for the recursive tree, `--max-depth <N>` (default `10`).
- `--unused` / `--hidden` - surface unused objects, as on `te deps`.
- `--paths-only` - one canonical object path per line, for piping.
- `--no-multiline` - collapse multi-line cells (with `--ls`/`--where`). Text output only.
- `-t, --type <kind>` - disambiguate when the path matches multiple table-children (e.g., a column and a hierarchy with the same name). Values: `Measure`, `Column`, `CalculatedColumn`, `Hierarchy`, `Calendar`, `Partition`, `CalculationItem`.
- `--output-format tmsl`（别名 `bim`）- 将解析后的对象输出为 TMSL/BIM JSON。
- `--output-format tmdl` - 将解析后的对象输出为 TMDL（仅限命名对象）。

`te get` and `te list` share a single descriptor catalog, so every property surfaces the same way across formats - the text table, JSON, and CSV all see the same set, and adding a new property to the model exposes it everywhere.

The `Settable:` line under a `te get <path>` result lists the properties `te set` accepts on that object (`SortByColumn` among them) and ends with a pointer to `--properties` for the full list; an unknown property name on `te get -p` or `te set -p` points at the same listing. `te get -p` syntax-highlights every expression-valued property, detail rows and format string expressions included. In JSON output, a single object leads with `objectPath` (the canonical path, resolvable as-is by `te get`, `te set`, or `te remove`), followed by `type` and `properties`; a listing that matches nothing prints an empty array.

```bash
te get Sales/Amount -p expression                # Print DAX
te get "'Sales'[Amount]"                         # DAX form: same as Sales/Amount
te get "[Total Sales]"                           # Lone-bracket: model-wide measure-or-column
te get "'Net Sales'[Sales Amount]" -p expression # DAX form with spaced names
te get Sales/Revenue/KPI                         # KPI sub-object of a measure
te get Sales --output-format tmdl                # Emit the table as TMDL
te get Sales --output-format bim                 # Emit the table as TMSL/BIM
te get . -p description                          # Model-level property
te get "Sa*"                                     # Every table matching the wildcard, no --ls needed
te get Measures --where IsHidden=true --ls       # Filter + list rendering
te get Measures --where Name=*margin*            # Contains-search across all measures
te get Sales/Amount --properties                 # Property names -p accepts, with types and allowed values
te get Sales/Revenue --deps downstream --deep    # Recursive dependents
```

### find

Search string properties for text and report each match site. The pattern is a **literal, case-insensitive substring** by default - `te find "Gross*"` looks for a literal asterisk - so pass `--regex` for pattern matching. Use `te get --where Name=*Gross*` when you want to filter objects by a property value rather than search text. An empty result names the scope that was searched and the matching mode used, and offers commands that widen the search; a `--regex` pattern that is not a valid regular expression is refused with an error naming the flag and the pattern.

`te find` 支持：

- `--in <scope>` - 作用域：`names`、`expressions`、`descriptions`、`displayFolders`、`formatStrings`、`annotations`、`all`（默认值：`all`）。
- `--regex`、`--case-sensitive`、`--paths-only`。
- `--no-multiline` - 将多行匹配上下文折叠为单行。 Text output only.

`--in expressions` 涵盖模型中的每个 `IExpressionObject`——包括 KPI 的 `TargetExpression` / `StatusExpression` / `TrendExpression`、度量值的 `DetailRowsExpression`、分区源/轮询的 M 表达式、表权限的 `FilterExpression`，以及计算组的 `MultipleOrEmptySelection` / `NoSelection` 表达式——因此，设置在 KPI 目标上的字面量（例如 `123`）也会像度量值正文一样被找到。

```bash
te find "CALCULATE" --in expressions
te find "Revenue" --in names
te find "CALCULATE" --in expressions --paths-only | xargs -I{} te get {} -p expression
te find "Gross.*Margin" --in names --regex
```

Under `--output-format json`, `te find` reports the scope it searched and the matching mode it used alongside the matches.

### diff

Compare two models for structural differences. 返回以下退出码：`0` 表示相同，`1` 表示发现差异，`2` 表示错误。

Changes are reported the same way the mutating commands report theirs: one consolidated entry per changed object, with `-`/`+` lines per property in text output. In JSON, the `changes` array entries carry `objectPath` (the canonical path, pipeable into `te get`), `objectType` (the same closed vocabulary as the findings JSON - `KPI`, `Member`, ...), `changeKind` (`created`, `deleted`, `modified`, or `moved` - a renamed object that carries a lineage tag is a single `moved` entry with `movedFromObjectPath`), and a `properties` array of `{property, before, after}` with PascalCase property names. An object that exists in only one of the two models is listed together with its contents - a new role's row-level security filters, a new table's columns, measures, and partitions, a new hierarchy's levels - each as its own entry, and the summary counts include them.

```bash
te diff ./model-v1 ./model-v2
te diff old.bim new.bim

# Branch on exit code (POSIX sh):
te diff ./a ./b; case $? in 0) echo same;; 1) echo different;; *) echo error;; esac

# Branch on exit code (PowerShell):
te diff ./a ./b; switch ($LASTEXITCODE) { 0 { 'same' } 1 { 'different' } default { 'error' } }
```

### deps

分析对象的上游和下游依赖关系，或找出整个模型中未使用的对象。 A shortcut for `te get --deps` / `te get --unused`. The single-object form takes a `<path>`.

`te deps` 接受以下选项：

- `--upstream` - show only upstream dependencies (what this object uses).
- `--downstream` - show only downstream dependents (what uses this object).
- `--deep` - show the recursive dependency tree instead of direct dependencies only.
- `--max-depth <N>` - maximum depth for `--deep` traversal (default: `10`).
- `-t, --type <kind>` - disambiguate when the path matches multiple table-children (e.g., a column and a hierarchy with the same name).
- `--unused` - list measures, calculated columns, and **all data columns** that no DAX references and that aren't used in any relationship, hierarchy level, sort-by, variation, AlternateOf base, or calendar time role. Each result shows `(hidden)` in text mode and an `isHidden` field in JSON.
- `--hidden` - 将 `--unused` 限制为仅包含隐藏对象。 Hidden, unused objects are the safest prune candidates because nothing user-facing depends on them.

In JSON output, every entry - and every `upstream`, `downstream`, and `--deep` tree node - is named the way the rest of the CLI names objects: `objectPath` (canonical path, pipeable into `te get`), `object` (bare name), and `objectType`.

```bash
te deps Sales/Revenue                     # Upstream + downstream for one object
te deps "'Sales'[Revenue]"                # DAX form is accepted everywhere a <path> is
te deps Sales/Revenue --downstream --deep # Everything that depends on Revenue, recursively
te deps --unused                          # All unused measures and columns
te deps --unused --hidden                 # Only hidden, unused objects
```

## 分析和质量

### validate

验证模型表达式、架构完整性和 TOM 错误。

`te validate` 接受以下选项：

- `--ci <fmt>` - emit CI annotations to stderr: `vsts` (aliases `azdo`, `azure-devops`) or `github` (alias `gh`). `none` or an empty value means no annotations; any other value is rejected before the command runs.
- `--trx <PATH>` - 将结果写入 VSTEST `.trx` 文件。
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

Every finding carries a stable code, shown in the **Code** column of the Errors, Warnings, and Anti-patterns tables as well as in JSON, `--ci` annotations, and `--trx`. Three codes are worth knowing when a hand-written model is involved: `TE0012` (a column and a measure, or two columns, share a name within one table) and `TE0013` (a measure name is repeated across tables) are errors - Analysis Services refuses to load such a model, and `te save-as` refuses to write one unless `--force` or `--skip-validation` is passed; `TE0014` is a warning that a TMDL folder has no `database.tmdl`, so the compatibility level in effect is a substitute for the one the model declared. The folder still loads and `te validate` still exits `0` for `TE0014`; hide it like any other warning with `--no-warnings` or `--errors-only`.

Under `--output-format json`, `te validate` emits the shared findings JSON document (`summary` plus a flat `findings[]` array) shared with `te bpa run`, `te test run`, and `te query` - see @te-cli-findings.

> [!NOTE]
> `te validate` does not support `--output-format csv` - CSV is rejected up front with an actionable error rather than producing a partial result. Use `text` or `json` for validation output.

### bpa run

针对模型运行 Best Practice Analyzer 规则。

`te bpa run` 接受以下选项：

- `-r, --rules <rules>` - JSON 格式的 BPA 规则文件(s)的路径(s)或 URL(s)。 Repeatable. Replaces the user-rule layer for this invocation: see [Rule sources and resolution](#rule-sources-and-resolution) below.
- `--no-model-rules` - 排除嵌入在模型注释中的 BPA 规则。
- `--no-defaults` - 排除内置的默认 BPA 规则。
- `--vpax <file>` - 从 `.vpax` 文件加载 VertiPaq分析器统计信息，以启用可感知 VPA 的规则。
- `--allow-external-rules` - 允许从嵌入在模型注释中的 URL 获取 BPA 规则文件。
- `--rule <id>` - 仅按 ID 运行指定规则(s)。 Repeatable.
- `--path <path-filter>` - 将分析限制为包含匹配对象的表。 Accepts literal names, container keywords, and wildcards (e.g., `'Sales'`, `'Sa*'`, `'Sales/Measures'`, `'*/Amount'`).
- `--fix` - 应用修复表达式，在可能的情况下自动修复违规项。
- `--save` - 应用修复后，将模型保存回原始位置。
- `--save-to <path>` - 应用修复后，将模型保存到其他路径。
- `--diff` / `--stat` / `--name-only` - change-output rendering for the fix pass (see the [Model editing](#model-editing) note).
- `--serialization <fmt>` - model serialization: `tmdl`, `bim` (alias `tmsl`), `database.json`.
- `--fail-on <severity>` - 失败阈值：`error`（默认）或 `warning`。 Exits with code `1` when violations meet the threshold. Rule-loading or evaluation errors (invalid expressions, unreadable rule files) also cause a non-zero exit regardless of `--fail-on`.
- `--ci <fmt>` - emit CI logging commands to stderr: `vsts` (Azure DevOps; aliases `azdo`, `azure-devops`), `github` (GitHub Actions; alias `gh`). Unrecognised values are rejected up front.
- `--trx <path>` - 将结果作为 VSTEST `.trx` 文件写入指定路径。
- `--no-multiline` - 将违规表中的多行单元格内容折叠为单行。 Text output only.

```bash
te bpa run --fail-on error --ci github
te bpa run --fix --save
te bpa run --rule PERF_UNUSED_HIDDEN_COLUMN
te bpa run --path Sales            # Tables touched by the Sales filter only
te bpa run --path 'Sa*'            # Wildcard - every table starting with Sa
te bpa run --path Sales/Measures   # Path filter applied to the matched tables
```

Under `--output-format json`, `te bpa run` emits the shared findings JSON document (see @te-cli-findings); with `--fix`, the JSON is a single document that also includes the `fix` change set.

#### 规则来源与解析

每次调用 `te bpa run` 时，都会从三个彼此独立的层级整合规则：

1. **用户规则** - 按优先级顺序，只有一个来源会生效：
   - `-r, --rules <rules>` 标志，接受文件路径或 URL (优先级最高)
   - `TE_BPA_RULES` 环境变量
   - 来自 CLI 配置 (`~/.config/te/config.json`) 的 `bpa.rules` 数组
2. **内置默认规则** - 除非传入 `--no-defaults`，或配置中的 [`bpa.builtInRules`](xref:te-cli-config#built-in-bpa-rules) 为 `false`，否则会加载。 Individual built-ins listed in `bpa.disabledBuiltInRuleIds` are skipped.
3. **模型嵌入规则** - 模型 `BestPracticeAnalyzer_Rules` 注释中的规则；除非传入 `--no-model-rules`，否则会加载。 External URL annotations are skipped unless `--allow-external-rules` is also passed.

The built-in defaults are exactly Tabular Editor 3's documented [built-in rule set](xref:built-in-bpa-rules) (the `TE3_BUILT_IN_*` IDs), so `te bpa run` and TE3 Desktop agree on what the built-ins flag. The six VertiPaq Analyzer rules (`VPA_*`) that earlier previews presented as built-in are not part of that set, and the `--vpa-rules` flag no longer exists; if a pipeline gates on one of them, copy its definition into your own rules file and point at it with `--rules`, `bpa.rules`, or `TE_BPA_RULES`. `--vpax` is unchanged and still supplies the statistics a VPA-aware rule of your own reads. C# scripts (`te script`, `te macro run`) see the same rule set through `Bpa.Rules` and `Bpa.Analyze()`.

Each rule ID is evaluated once. When the same ID appears in more than one layer, an explicit `--rules` file's definition wins in `te bpa run`, while the built-in definition wins in the deploy/save gates. 然后会移除模型 `BestPracticeAnalyzer_IgnoreRules` 注释中的规则 ID。

输出中的 `Rules loaded:` 行会列出每个提供规则的层级，例如：

```
Rules loaded: 38 from 1 file(s) from bpa.rules config + built-in defaults + model annotations
```

### bpa rules

Manage BPA rule collections - list, inspect, initialize, and toggle rules in your local rules file or in model annotations. Built-in rules are read-only - to skip one without losing the rest, use `te bpa rules disable` (do not edit the built-in set directly).

子命令：

| 子命令                                                       | 用途                           |
| --------------------------------------------------------- | ---------------------------- |
| `add <id>`                                                | 添加新的 BPA 规则。                 |
| [`disable`](#bpa-rules-disable)                           | 为当前用户禁用一条内置 BPA 规则。          |
| [`enable`](#bpa-rules-enable)                             | 重新启用先前已禁用的内置 BPA 规则。         |
| `ignore <rule-id>`                                        | 将规则添加到模型的忽略列表。               |
| [`init`](#bpa-rules-init)                                 | 在解析后的 PATH 下创建一个空的 BPA 规则文件。 |
| [`list`](#bpa-rules-list) (alias `ls`) | 列出来自所有来源的 BPA 规则及其状态。        |
| `remove <rule-id>` (alias `rm`)        | 删除一条 BPA 规则。                 |
| `set <rule-id>`                                           | 更新 BPA 规则的属性。                |
| `unignore <rule-id>`                                      | 从模型的忽略列表中移除一条规则。             |

`te bpa rules` 的所有子命令都接受以下选项：

- `--rules-file <path>` - path to a BPA rules JSON file. 默认使用你的 CLI 配置（`~/.config/te/config.json`）中 `bpa.rules` 的首个已存在条目，或使用 `TE_BPA_RULES` 环境变量。
- `--model-rules` - 操作嵌入在模型注释中的规则，而非文件中的规则。

> [!IMPORTANT]
> `te bpa rules set` and `te bpa rules remove` refuse to mutate built-in rule IDs. Attempting to do so exits with code `1` and points at `te bpa rules disable`. To customize a built-in rule's behavior, disable the built-in and add a custom copy with a different ID:
>
> ```bash
> te bpa rules disable TE3_BUILT_IN_DATE_TABLE_EXISTS
> te bpa rules add MY_DATE_TABLE_EXISTS
> ```

#### bpa rules list

列出来自所有来源的规则（内置、用户、模型）。 (Alias: `ls`.)

`te bpa rules list` 接受以下选项：

- （默认）仅显示生效的规则。
- `--all` - 包含已禁用和已忽略的规则。
- `--disabled` - 仅显示你通过 `te bpa rules disable` 禁用的内置规则 ID。
- `--ignored` - 仅显示其 ID 出现在模型的 `BestPracticeAnalyzer_IgnoreRules` 中的规则。
- `--no-defaults` - 从输出中排除内置规则。

```bash
te bpa rules list              # Active rules
te bpa rules list --all        # Include disabled and ignored rules
te bpa rules list --ignored
```

已禁用的内置规则会在规则 ID 旁标记 `[disabled]`。

#### bpa rules init

Create an empty BPA rules file (`[]`) at the configured path. Use this once before invoking `te bpa rules set` / `te bpa rules remove` against a path that does not yet exist.

`te bpa rules init` 接受以下选项：

- `--force` - 用 `[]` 覆盖现有文件。 Required if the target file exists.
- `--rules-file <path>` - 目标文件路径。 Can appear before or after the `init` subcommand.

路径解析（先匹配到的优先）：`--rules-file` → `TE_BPA_RULES` 环境变量 → CLI 配置中 `bpa.rules[]` 的第一项 → `./BPARules.json` (当前工作目录)。

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

The command is idempotent - running `disable` against an already-disabled rule succeeds without modifying the config. 如果 `<rule-id>` 不是内置规则，命令会以退出代码 `1` 结束；可使用 `te bpa rules list` 查看有效的内置 ID。

```bash
te bpa rules disable TE3_BUILT_IN_DATE_TABLE_EXISTS
```

#### bpa rules enable

通过从 `bpa.disabledBuiltInRuleIds` 中移除规则 ID，重新启用此前已禁用的内置 BPA 规则。 Exits with code `1` if the rule isn't currently disabled.

```bash
te bpa rules enable TE3_BUILT_IN_DATE_TABLE_EXISTS
```

### vertipaq

分析 VertiPaq 存储统计信息。

`te vertipaq` 支持：

- `<path>` - optional positional argument: a table name to filter the analysis to a single table.
- `--columns`, `--relationships`, `--partitions`, `--all`。
- `--detail` - show expanded columns (data/dict/hierarchy size breakdown, encoding, segments).
- `--fields <list>` - comma-separated fields to display (e.g., `--fields name,card,size,%tbl,%db,bar`). Available fields vary by view.
- `--export <file.vpax>` - 将 VertiPaq 统计信息导出为 `.vpax` 文件，以便离线分析。
- `--import <file.vpax>` - 加载之前导出的 `.vpax` 文件并进行离线分析。
- `--obfuscate` - 对导出的 VPAX 中的名称和表达式进行混淆处理。
- `--top <N>`、`--stats`、`--annotate`、`--save`。
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

DAX in a model is always comma-separated, so `--semicolons` exists only on `te util format-dax`, for DAX you have typed with semicolons yourself.

## 执行

### query

针对已部署的模型执行 DAX 查询。

`te query` accepts:

- `<dax>` - positional argument: the DAX query to execute. Equivalent to passing `-q`. Use whichever shape reads better; explicit `-q` wins if both are supplied.
- `-q, --query <dax>` - inline query (named-flag form of the positional above). `-q -` reads the query from stdin; with input piped and no query given at all, stdin is read implicitly.
- `--file <file.dax>` - 从文件读取查询。
- `--limit <N>` - 默认为 100。
- `-o, --output-file <path>` - 将结果写入文件（`.csv`、`.tsv`、`.json`、`.dax`）。
- `--trace`, `--cold`, `--plan`, `--runs <N>` - 用于性能跟踪和基准测试。
- `--no-validate` - 跳过执行前的 DAX 语义验证。

```bash
te query "EVALUATE TOPN(5, 'Sales')" -s my-ws -d my-model           # Positional DAX
te query -q "EVALUATE TOPN(5, 'Sales')" -s my-ws -d my-model        # Named-flag form
te query --file query.dax --output-format json
```

### script

Execute one or more C# scripts against a semantic model. CLI 使用与 Tabular Editor 3 Desktop 相同的脚本宿主，因此能在 TE3 中运行的脚本在这里也可原样运行。

`te script` 支持以下选项：

- `--file <path>` - `.cs` / `.csx` file (repeatable). Bare positional `.cs`/`.csx` arguments are also accepted.
- `--inline <code>` - inline C# (repeatable; use `-` for stdin).
- `--validate` - compile the script(s) and report errors without executing them. Needs no model at all, so it works offline as a CI lint.
- `--save` / `--save-to` / `--serialization`。
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

A run in which any script calls `Error(...)` exits non-zero, reports `"success": false` in JSON, and closes by saying the run completed with errors; changes the script already made are still saved when `--save` is given. `Warning(...)` and `Info(...)` never fail a run. On Windows, the `DisableCSharpScripts` administrator policy refuses `te script` outright - see [Administrator policies](xref:te-cli-config#administrator-policies).

> [!IMPORTANT]
> 如果你要迁移旧脚本，需要了解以下两个行为差异：
>
> - **CLI 脚本中不支持交互式选择。** 从 `te script` 调用 TE3 Desktop 辅助方法 `SelectMeasure()`, `SelectTable()`, `SelectColumn()`, `SelectObject()`, 和 `SelectObjects()` 时，会抛出 `NotSupportedException`，因为 CLI 没有可弹出的 UI。 Pre-resolve the object(s) outside the script and pass them in via environment variables or stdin, or wrap the call in `try/catch` if the script is shared with TE3.
> - **默认的 `using` 指令与 TE3 Desktop 一致。** 使用 `DataTable`、`File`、`StringBuilder` 或 `Regex` 的脚本，必须显式包含对应的 `using System.Data;` / `using System.IO;` / `using System.Text;` / `using System.Text.RegularExpressions;` 指令。

> [!NOTE]
> **Preprocessor symbols for cross-host scripts.** Scripts compiled by `te script` have the symbol `TECLI` defined. TE3 Desktop 脚本会改为定义 `TE3`，并且还会定义带版本范围限定的符号，例如 `TE3_3_10_OR_GREATER` ……当前 TE3 次版本对应的是 `TE3_3_X_OR_GREATER`。 TE2 defines neither symbol. Use these to write portable scripts:
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
> 更全面的跨版本脚本说明，见 @csharp-scripts。

### macro

Manage and run macros from a macros JSON file (typically `MacroActions.json`). 宏文件的 PATH 按以下顺序解析：`--macros <path>` → 环境变量 `TE_MACROS_PATH` → CLI 配置中的 `macros` → `./MacroActions.json`。 On Windows, the `DisableMacros` administrator policy refuses every `te macro` command - see [Administrator policies](xref:te-cli-config#administrator-policies).

子命令：

| 子命令                                                   | 用途                  |
| ----------------------------------------------------- | ------------------- |
| `list` (alias `ls`)                | 列出宏。                |
| 宏：[`run <name-or-id>`](#macro-run)                    | 运行宏。                |
| `add <name>`                                          | 添加宏。                |
| `set <name-or-id>`                                    | 更新宏属性。              |
| `remove <name-or-id>` (alias `rm`) | 删除宏。                |
| `sort`                                                | 排序并重新分配 ID。         |
| 宏：[`init`](#macro-init)                               | 在解析得到的路径处创建一个空的宏文件。 |

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

在配置的路径下创建一个空的宏文件（`{\"Actions\":[]}`）。 Use this once when the resolved macros file does not yet exist.

`te macro init` 接受：

- `--force` - overwrite an existing file. Required if the target exists.
- `--macros <path>` - 目标文件路径。 Can appear before or after the `init` subcommand.

```bash
te macro init
te macro init --macros ./project-macros.json
te macro init --force
```

#### macro run

运行宏。通过 `dataTable.Output()` 输出表格的宏会在终端中显示格式化输出，因此 DAX 风格的查询宏在 `te macro run` 中的行为与在 TE3 中相同。

`te macro run` 接受：

- `--on <path>` - 将宏的选择上下文设置为单个已命名对象（如表、度量值、列等…）。 Equivalent to right-clicking that object in TE3 and invoking the macro from the context menu.
- `--save` / `--save-to` - 将宏所做的所有更改持久化保存。 Like every mutating command, `te macro run` is a dry run without `--save`.
- `--serialization <fmt>` / `--force` - as on the other mutating commands.

```bash
te macro run "Hide all measures"
te macro run "Format DAX" --on Sales/Revenue --save
te macro run "Format DAX" --on "'Net Sales'[Sales Amount]" --save   # DAX form works in --on too
```

## 部署和刷新

### deploy

Deploy a semantic model to Power BI, Fabric, Azure Analysis Services, or on-prem SQL Server Analysis Services.

**Dry run by default**: `te deploy` connects read-only and prints the exact TMSL it would send to stdout. Add `--execute` to actually deploy.

`te deploy` accepts:

- `-s, --server` / `-d, --database` - the model **source**, exactly as on every other command.
- `--target-server <target>` / `--target-database <name>` - the deploy **destination**: a workspace name, endpoint, or server, and the semantic model name to create or overwrite. A server name, FQDN, IP address, or MSOLAP connection string deploys to Analysis Services (Windows Integrated auth for on-prem); a workspace name or `powerbi://...` URL deploys to Power BI. For local model sources, the target falls back to the active `te connect` connection; when the source is remote, the target flags are required. Deploying a model onto itself is refused.
- `--execute` - actually deploy. In interactive mode this shows a summary + confirmation prompt with **`n` as the safe default**; `--execute --force` skips the prompt (required in CI, where a prompt without `--force` is an error).
- `--deploy-full` - 覆盖现有内容，并同时部署连接、分区、共享表达式、角色及角色成员。
- `--deploy-connections`
- `--deploy-partitions`
- `--skip-refresh-policy`
- `--deploy-roles`
- `--deploy-role-members`
- `--deploy-shared-expressions`
- `--create-only`
- `--skip-bpa` - 完全跳过 BPA 门控检查。
- `--fix-bpa` - 如果规则定义了修复表达式，则自动修复 BPA 违规项。
- `--bpa-rules <path>` - repeatable; override `bpa.rules` from your CLI config for this single deploy. 除非 `bpa.builtInRules` 为 `false`，否则内置规则仍会生效。
- `--force` - skip the interactive confirmation.
- `--ci <fmt>` - `vsts` (aliases `azdo`, `azure-devops`) or `github` (alias `gh`); unrecognised values are rejected up front.
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

A deploy **fails** when the server reports errors on one or more objects, even though the metadata has been written: the exit code is non-zero, JSON reports `"success": false` with the reason in `error`, the headline says the deploy landed with errors, and `--ci` reports the object errors as errors. Unprocessed objects are not a failure - a metadata-only deploy legitimately leaves objects holding no data. The workspace mirror set up with `te connect -w` applies the same rule.

> [!NOTE]
> When `--output-format json` is set, `te deploy`'s JSON payload always includes the resolved `server` and `database`, even when they were resolved from active connection or profile rather than passed explicitly. Pipelines can use these fields to confirm the deploy target without re-parsing the command line. `te deploy` also exits non-zero on failure under `--output-format json`, matching its text-mode behavior - the JSON payload is the failure record, not a success signal.

### refresh

在已部署的模型上触发数据刷新。

**Dry run by default**: `te refresh` prints the TMSL a refresh would send to stdout. Add `--execute` to run it.

`te refresh` 支持：

- `--type <type>` - `full`, `dataonly` (alias `data-only`, `data`), `automatic` (alias `auto`), `calculate` (alias `calc`), `clearvalues` (alias `clear`), `defragment` (alias `defrag`), `add` (default: `automatic`).
- `--table <name>` - 刷新特定表(可为多个)；可重复指定。
- `--partition <Table.Partition>` - 刷新特定分区(可为多个)。
- `--execute` - actually run the refresh. At a terminal it asks for confirmation with **`n` as the safe default**; add `--force` to skip the question. An unattended run (redirected output, `--output-format json`, or `--non-interactive`) stops with an error unless `--force` is given, so `te refresh --type full --execute --force` is the CI form.
- `--force` - skip the confirmation prompt.
- `--apply-refresh-policy <true|false|table>` - apply incremental refresh policies to determine which partitions are refreshed; pass a table name to scope the refresh to that table. Policies apply by default when the refresh type and scope are compatible, except for models hosted in Power BI Desktop. An explicit value wins (with warnings when it cannot take effect).
- `--effective-date <yyyy-MM-dd>` - set the effective date used by the refresh policy (ignored, with a warning, when no policy applies).
- `--max-parallelism <N>` - 设置可并行刷新的最大分区数。 Wraps the refresh in a TMSL `sequence` command.
- `--no-progress`, `--trace [path]`。 `--trace` without `--execute` warns and prints the TMSL. Trace timing comes from the server's clock, the log is kept until the server has finished delivering buffered events, and `te-refresh-*` traces older than an hour that interrupted runs left behind are stopped and dropped at the start of a traced refresh (traces from other tools are never touched).

Executed refreshes under `--output-format json` always include a `progress` array; with the `vertipaqOnRefresh` config key enabled, a per-table `vertipaq` array (rows, size, columns) is included too - no `--trace` needed.

```bash
te refresh --type full --execute                        # Full refresh (asks for confirmation at a terminal)
te refresh --type full --execute --force                # Unattended: skip the confirmation
te refresh --table Sales --type full --execute          # Single table
te refresh --type full > refresh.tmsl                   # Dry run: emit TMSL only
te refresh --apply-refresh-policy Sales --execute       # Apply Sales' incremental refresh policy
```

Incremental refresh policies are authored with [`te set`](#incremental-refresh-policies) on a table's `RefreshPolicy` sub-object.

## 测试

### test run

针对已部署的模型运行一组 DAX 断言测试。

`te test run` 支持以下选项：

- `--suite <path>` - 测试套件目录（默认：`.te-tests/`）。
- `--tag <tag>` - 仅运行带有此标签的测试。
- `--fail-on <severity>` - `error`（默认）或 `warning`。
- `--ci <fmt>`, `--trx <PATH>` - CI 标注和 TRX 输出。

```bash
te test run --ci github --trx results.trx
te test run --tag revenue
```

Suites are validated before any connection is made; a suite that fails validation (for example, a missing `query_file`) exits `1` without running anything. Under `--output-format json`, `te test run` emits the shared findings JSON document with test-specific extras (`suites`, `invalidSuites`, `testSummary`) - see @te-cli-findings.

### test init / spec / use / list / snapshot / compare

`te test list` also accepts the `ls` alias.

Additional subcommands scaffold tests, print the assertion spec format, switch the active suite, list suites, capture snapshots, and compare models. See `te test --help` for details.

```bash
te test init --example             # Scaffold an example suite
te test spec                       # Print the full assertion format reference
te test init --from-model --model ./my-model  # Generate stubs from your measures
```

## 连接和身份验证

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

#### 工作区模式（`-w` / `--workspace`）

Pair a primary source with a secondary target so every subsequent `--save` mirrors the model between the two. Useful for keeping a local working copy of a remote workspace, or pushing local edits to a workspace as you save.

- `te connect <ws> <model> -w ./src` - 主源为远程；`./src` 会接收初始 TMDL 导出，并在每次保存时保持镜像同步。
- `te connect ./src -w <ws> <model>` - 主源为本地；首次部署会将模型推送到 Workspace，后续保存会自动重新部署。
- `--workspace-format <fmt>` - choose the on-disk format when mirroring to a folder/file: `tmdl`, `bim` (alias `tmsl`), or `database.json`. When omitted, the format is inferred from the workspace target path (e.g., `-w ./model.bim` infers BIM).
- `--workspace-auth <method>` - auth method for a remote workspace target when the primary is local. Defaults to `--auth` if set, else `auto`.
- `--force` - required when the target already exists (non-empty folder, existing database). Without it, `te connect` shows an interactive `y/n` prompt with `n` as the safe default.

Once active, `te set --save`, `te remove --save`, `te script --save`, etc. all dual-save transparently. Save order is always **local first, then remote** so the on-disk copy reflects the latest user change even if the server push fails. Clear the mirror with `te connect --clear`.

```bash
te connect Finance "Revenue Model" -w ./revenue-model    # Mirror remote → local TMDL
te connect ./revenue-model -w Finance "Revenue Model"    # Mirror local → remote
```

### auth login / status / logout

管理缓存的身份验证信息。 See @te-cli-auth.

### profile list / show / set / remove

Manage named connection profiles. (`te profile list` alias: `ls`; `te profile remove` alias: `rm`.) See @te-cli-auth.

## 配置

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
- `--semicolons` - format DAX written with semicolons as list separators (European locale). The flag selects the semicolon dialect for the expression that is read as well as for the output, so it is for DAX you authored with semicolons - comma-separated DAX fails with a syntax error under it. It is accepted only here: `te set --format` refuses it, because an expression stored in a model is always comma-separated.
- `--long` - long format with fewer line breaks. Default is short.
- `--no-space-after-function` - skip the space after function names.

```bash
te util format-dax "SUM ( Sales[Amount] )"
cat query.dax | te util format-dax -
te util format-dax "CALCULATE(SUM(Sales[Amt]); Sales[Region] = \"EU\")" --semicolons   # Semicolon-authored DAX
```

JSON output carries `success`, `formatted`, and `errors`. For expressions already in the model, use `te set <path> --format <PropertyName>` instead; for a whole-model sweep, `te script --inline "Model.AllMeasures.FormatDax();" --save`.

### util format-m

Format a loose M/Power Query expression. `-` reads from stdin; no language-specific options. A malformed expression - an unterminated string, for example - is reported as a failure with a non-zero exit code and the original text returned unchanged, never a silently shortened result.

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

Inside the session, mutating commands stage in memory: `save` (no arguments) commits the staged edits and `revert` discards them, while `save-as` re-serializes to a format or location. Closing a session that still holds staged edits asks for confirmation (or, when nobody can answer, warns and exits non-zero); `exit --force` throws them away deliberately - see @te-cli-interactive.

引号和 DAX 风格的引用在会话内外的用法一致——有关 REPL 中支持括号感知的 argv 拆分的详细信息，请参见上文的[对象路径](#object-paths)一节以及 @te-cli-interactive。

### session

Show or manage the current terminal session. The CLI keeps per-terminal state (active connection, active profile, active test suite) in a session file, isolated per shell process. Set the `TE_SESSION` environment variable to share one named session across shells.

子命令：

| 子命令                                    | 用途                                                                                                                                                  |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `show`                                 | Show current session details (ID, file path, active state). Default when no subcommand is given. |
| `list` (alias `ls`) | List all session files.                                                                                                             |
| `clear`                                | Clear active state for the current session.                                                                                         |
| `prune`                                | Delete session files whose shell process is no longer running.                                                                      |

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

## 退出代码

| 退出  | 含义                                                                                                                                                                                                                                                                                                                                            |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `0` | 成功。                                                                                                                                                                                                                                                                                                                                           |
| `1` | Generic failure (invalid arguments, command failed, validation errors, auth failure, BPA gate failed at severity >= error, a `te script` run in which a script reported an error, a `te deploy` the server accepted with object errors). For `te diff`: differences found. |
| `2` | `te diff` only: an error occurred while comparing, so the difference status is unknown.                                                                                                                                                                                                                       |

如需在 CI 管道中进行更细致的控制，可将退出代码与 `--ci <vsts/github>` 注释以及 `--trx` 结果文件结合使用——参见 @te-cli-cicd。

## 相关页面

- @te-cli - 概览和背景说明。
- @te-cli-install - 安装并设置 CLI。
- @te-cli-auth - 进行身份验证并管理连接。
- @te-cli-config - 配置文件、BPA 门禁和变更后行为。
- @te-cli-findings - the findings JSON shared by validate, bpa run, test run, and query.
- @te-cli-migrate - TE2 → TE3 标志映射。
