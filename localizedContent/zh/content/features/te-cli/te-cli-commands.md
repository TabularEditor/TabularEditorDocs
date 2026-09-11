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

本页为每个命令提供简要说明和一个示例。 每个命令都支持 `--help`，可查看详尽的标志与选项说明：

```bash
te deploy --help            # Help for a single command
te bpa run --help           # Help for a command with subcommands
```

> [!NOTE]
> 在预览版期间，CLI 的 `--help` 输出是标志和选项的权威参考。 本页内容由人工整理，因此在两次预览版本之间新增的内容，本页更新会比 `--help` 更晚。

## 对象路径

CLI 中的对象定位在所有命令中都采用同一套语法。 以下参考中会出现两种路径形式：

- **`<path>`** - 解析为**恰好一个**对象或容器。 Used by commands that change the model or need a single target: `te set`, `te add`, `te remove`, `te move`, `te deps`, `te macro run --on`, and `te get` with `-p`, `--deps`, or `--properties`.
- **`<path-filter>`** - 解析为**零个或多个**对象，并支持通配符。 Used by commands that operate on a set: `te list`, plain `te get` (a wildcard or container path lists every match), `te bpa run --path`, and other inspection-style commands.

两种路径形式共用同一套语法规则；仅有两处不同：

- 筛选路径允许使用 `*` 通配符；对象路径不允许。
- 对象路径允许使用 DAX 方括号后缀（例如 `Sales[Amount]`）；筛选路径不允许。

### 分段和分隔符

路径是由斜杠分隔的 **分段** 序列。 每个分段表示一个步骤：一个表、一个子对象，或一个容器关键字。

- `Sales` — 一个分段
- `Sales/Revenue` — 两个分段
- `Roles/Admin/Members/bob` — 四个分段

空输入和 `.` 都表示“模型根”——它既是筛选路径的隐式起点，也是 `te get .` 这类查询显式指向的对象。

### 引号

大多数分段名称无需加引号即可直接使用。 如果分段名称包含空格、斜杠、方括号，或任何其他会被解析为语法的字符，请将该分段用引号括起来。 CLI 遵循 DAX 的引号规则，因此在 `te` 路径中加引号的写法与在 DAX 表达式中输入的一致：

| 形式               | 适用场景                                                                                         | 转义规则                                         |
| ---------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------- |
| `'Net Sales'`    | 表，以及名称中带空格的对象。                                                                               | 将引号写两次（`'Bob''s'` → `Bob's`）。                |
| `"Net Sales"`    | 同上；当单引号转义不方便时，跨不同 shell 使用会更省事。                                                              | 将引号写两次（`"He said ""hi"""` → `He said "hi"`）。 |
| `[Sales Amount]` | 表引用中的 DAX 方括号后缀（`'Sales'[Sales Amount]`），或不带表前缀、在整个模型范围内解析的单独方括号引用（`[Total Sales]`）。 仅限对象路径。 | 将右方括号写两次（`[foo]]bar]` → `foo]bar`）。          |

在带引号的分段内，`*` 会被视为字面字符，而不是通配符。 因此，`'Sa*'` 会匹配名称恰好为 `Sa*` 的表。

The reserved characters in paths are `/ [ ] ' " * ? { }`. A segment containing any of `* ? { }` must be quoted (`te get "Tables/'{foo}'"`, `te get 'Sales/"my*name"'`); unquoted use is rejected with an error naming the character and showing the quoted form. `?` is reserved and has no wildcard meaning. Every path the CLI prints - in errors, hints, `--paths-only` output, and the `objectPath` field in JSON - is canonically quoted and can be pasted straight back into `te get`. The mixed-quote forms require PowerShell or bash; cmd.exe cannot express them.

### DAX 风格的引用（仅对象路径）

凡是允许使用 `<path>` 的位置，都接受两种 DAX 形式：

- **`'Table'[Member]`**：等同于 `Table/Member`。 方括号后缀会在存在歧义时优先匹配列和度量值，而不是层次结构/分区。
- **`[Member]`**：一个独立的度量值或列，前面不带表名。 在整个模型中搜索具有该名称的度量值或列。 两者都存在时，优先选择度量值。

```bash
te get "'Sales'[Amount]"             # Same as te get Sales/Amount
te get "'Net Sales'[Sales Amount]"   # Spaced names via DAX form
te get "[Total Sales]"               # Model-wide measure-or-column lookup
```

### 容器和关键字

有一些名称可用作容器关键字。 关键字既可以单独使用（列出整个容器），也可以出现在路径中（跳转到当前父级下的该子集合）。

| 关键字                                                                                                                   | 范围   | 含义           |
| --------------------------------------------------------------------------------------------------------------------- | ---- | ------------ |
| `Tables`, `Measures`, `Columns`, `Hierarchies`, `Partitions`, `KPIs`, `Sets`                                          | 模型   | 模型中该类型的所有对象。 |
| `关系`, `角色`, `Perspectives`, `Cultures`, `DataSources`, `Expressions`, `CalculationGroups`, `Functions`, `Annotations` | 模型   | 模型级容器。       |
| `Measures`, `Columns`, `Hierarchies`, `Partitions`, `Calendars`, `CalculationItems`, `KPIs`, `Sets`                   | 表    | 表下的子容器。      |
| `Levels`                                                                                                              | 层次结构 | 层次结构的级别。     |
| `Members`, `TablePermissions`（别名 `Permissions`）                                                                       | 角色   | 角色的子级对象。     |

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

当实际对象名称恰好与关键字同名时，可为该分段加上引号，以强制进行字面名称匹配。 字面名称为 `Tables` 的表需要写作 `'Tables'`，可通过 `te get "'Tables'"` 访问。 The same applies to tables named `KPIs` or `Sets`.

### 筛选路径中的通配符

筛选路径引入了一个通配符字符 `*`，用于匹配单个分段内任意长度的字符序列（贪婪匹配，且仅限单个分段）。 通配符用于缩小 `te list` 和类似命令的结果范围。

```bash
te list 'Sa*'                          # Tables whose name starts with Sa
te list 'Sales/*Amount'                # Children of Sales whose name ends with Amount
te list '*/Amount'                     # An Amount column/measure across every table
te list 'Roles/Re*/Members'            # Members of every role matching Re*
```

包含 **N 个分段** 的筛选路径会返回 **N 层深度** 的结果——通配符不会自动多展开一层，结果深度不会超过你输入的层级。 单分段快捷写法 `te list Sales` 是个例外：未限定且不带通配符的表名会展开为该表的直接子对象，以符合“让我看看 Sales 里有什么”的意图。 相比之下，`te list Sa*` 只返回匹配的表，不会展开。

筛选路径中不支持 DAX 的方括号后缀；如需按字面匹配包含 `[` 和 `]` 的名称，请给名称加引号。

### 错误和提示

分段拼写错误时会给出一条与上下文相关的错误；如果 CLI 能猜到你的意图，还会附带“你是不是想输入……”的提示。 The list offers tables, measures, columns, and hierarchies, each as a full `Table/Object` path that pastes straight back into the next command. A name written in single quotes is a table reference (`te deps 'Revenue'` looks for a table named Revenue), and the error points at the `Table/Object` and `"[Object]"` forms for anything that is not a table. 缺少父级的路径会在检查叶节点之前失败，因此信息会指向真正出错的分段。 Every path an error or hint prints is taken from your model and quoted so it resolves as printed - a refusal never suggests a path that does not exist. Empty containers (e.g., `te list Hierarchies` on a model without hierarchies) emit a simple "nothing here" hint rather than an error.

## 命令别名

大多数长格式命令也有对应的简短别名。 每行显示规范命令及其可用的等效短格式别名。

| 规范命令                  | 别名形式(s) |
| --------------------- | -------------------------- |
| `te save-as`          | `te save`                  |
| `te list`             | `te ls`                    |
| `te remove`           | `te rm`                    |
| `te move`             | `te mv`, `te rename`       |
| `te bpa rules list`   | `te bpa rules ls`          |
| `te bpa rules remove` | `te bpa rules rm`          |
| `te config list`      | `te config ls`             |
| `te 宏 list`           | `te 宏 ls`                  |
| `te 宏 remove`         | `te 宏 rm`                  |
| `te profile list`     | `te profile ls`            |
| `te profile remove`   | `te profile rm`            |
| `te session list`     | `te session ls`            |
| `te test list`        | `te test ls`               |

## 全局选项

这些标志适用于每个命令，可在子命令名称之前或之后使用。

| 选项                         | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-m, --model <path>`       | 语义模型的路径（TMDL 文件夹、`.bim` 文件、`Database.json` 文件夹或 `.SemanticModel` 文件夹）。                                                                                                                                                                                                                                                                                                                                                                 |
| `-s, --server <endpoint>`  | Analysis Services 端点或 Power BI Workspace。 服务器名称/FQDN（`MY.SERVER.COM`）、IP 地址（`192.168.1.1`）、`host:port`、`localhost`、`SERVER\\INSTANCE`、`asazure://...` 或 MSOLAP 连接字符串可用于直接连接到 Analysis Services / AAS。 单一标记名称（`MyWorkspace`）、Fabric `Name.Workspace[/Model.SemanticModel]` 路径或 `powerbi://...` URL 会指向 Power BI Workspace。 名称中包含点号的 Workspace 无法与服务器名称区分，因此会被视为服务器，CLI 会输出警告；如需指向 Power BI，请使用其 `.Workspace` 形式或完整的 `powerbi://` URL。 |
| `-d, --database <name>`    | Workspace 上的语义模型名称。                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `--local`                  | Connect to a locally running Analysis Services instance - Power BI Desktop, Visual Studio workspaces, or standalone SSAS (Windows only).                                                                                                                                                                                                                                                            |
| `--auth <method>`          | 身份验证方法：`auto`、`interactive`、`spn`、`env`、`managed-identity`（默认值：`auto`）。                                                                                                                                                                                                                                                                                                                                                                |
| `--output-format <format>` | 标准输出格式：`text` (默认)、`json`、`csv`、`tmsl` (别名 `bim`)、`tmdl`。 输出表格数据的命令会识别 `csv`；`tmsl`/`tmdl` 仅由 `te get` 和 `te list` 用于整个对象的序列化。 命令会拒绝其不支持的格式。                                                                                                                                                                                                                                                     |
| `--error-format <format>`  | 用于错误、警告和提示的 stderr 格式：`text`（默认）或 `json`。 其他值将回退为 `text`。 它独立于 `--output-format`，因此你可以将 JSON 格式的 stdout 与纯文本错误配合使用（反之亦然）。                                                                                                                                                                                                                                                                                                              |
| `--recent [N]`             | 使用最近使用过的模型。 未提供值 = 进入交互式选择器；`N` = 最近使用列表中的第 N 个（1 = 最近一次使用）。                                                                                                                                                                                                                                                                                                                                                                           |
| `--non-interactive`        | 禁用所有交互式提示。 如果缺少必需输入，将给出可操作的错误提示并失败退出。                                                                                                                                                                                                                                                                                                                                                                                                  |
| `--debug`                  | 启用调试日志并输出到 stderr（连接字符串、身份验证流程、耗时）。                                                                                                                                                                                                                                                                                                                                                                                                    |

`te --version` 会打印 CLI 版本并退出。

对于读取模型的命令，解析顺序如下：

`--recent` → `--local` → `--server`/`--database` (remote) → `--model` → active connection from `te connect`.

The model is never a positional argument - a stray path on the command line is rejected with an "unrecognized command or argument" error. (Positional arguments on `te connect`, `te init`, `te diff`, and `te query` are those commands' own subjects, not the model.)

> [!NOTE]
> **拼写错误的选项会被立即拒绝。** 如果你传入了当前命令无法识别的 `--flag`，CLI 会直接退出并给出可操作的错误信息，而不是悄悄把该标记当作位置参数吞掉。 这可以捕获 CI 脚本中把 `--force ` 误写成 `--forec` 之类的拼写错误。

> [!NOTE]
> **带点号的服务器名称。** `-s`/`--server` 会将带点号的名称（例如 `Sales.2026`）视为 Analysis Services 服务器主机名，而不是 Power BI Workspace。 当 CLI 需要这样判断时，会发出警告，并提示：如果你指的是 Power BI Workspace，请在末尾追加 `.Workspace`（例如 `Sales.2026.Workspace`），或使用完整的 `powerbi://` URL。 适用于 `te connect`、`te deploy`、`te refresh`、`te query`、`te vertipaq` 和 `te test run`。

## Model initialization and save

### save-as

Re-serialize a model to a different format or location. 可用于将远程 Workspace 中的模型写入本地文件、转换格式，或将编辑内容保存回源位置。 (Alias: `save`.)

`te save-as` accepts:

- `-o, --output-path <path>` - 目标文件或文件夹。 **Optional** - when omitted, `te save-as` writes back to the source location, preserving the original format.
- `--serialization <fmt>` - `tmdl`、`bim`（别名 `tmsl`）、`database.json`、`pbip`。 When omitted, the format is the loaded model's format; with `-o`, it is inferred from the output path (`.bim` writes a single-file BIM, `.json` a `database.json` folder).
- `--force` - 跳过验证并覆盖现有输出。 某些拒绝情况（例如容器不明确、项目根目录中存在多个 `SemanticModel`）即使使用 `--force` 也会触发。
- `--skip-bpa` - 完全绕过 BPA 检查。
- `--fix-bpa` - 当规则定义了修复表达式时，自动修复 BPA 违规项。
- `--bpa-rules <path>` - 可重复指定；仅对本次保存覆盖 CLI 配置中的 `bpa.rules`。 除非 `bpa.builtInRules` 为 `false`，否则内置规则仍会生效。
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
> Use `te save-as -o <path> -s <workspace> -d <model>` to download a remote model to disk. 如果你只需要原始字节数据（不做 DAX 语义分析），配合 `--skip-validation` 可实现最快的直通下载。

### init

在指定路径创建一个新的空语义模型。 Defaults to a TMDL model in `PowerBI` compatibility mode at compatibility level 1705.

`te init` 接受以下参数：

- `<output-path>` - 位置参数：用于创建模型的目录（省略时使用全局 `--model` 路径）。
- `--compatibility-mode <mode>` - `PowerBI`（默认）或 `AnalysisServices`。
- `--compatibility-level <N>`（别名 `--compat`）- 兼容级别。 Defaults to `1705` when the mode is `PowerBI`, `1500` otherwise. 参见 @update-compatibility-level。
- `--name <name>` - 模型/数据库名称（默认：目录名称）。
- `--serialization <fmt>` - `tmdl`（默认）、`bim`（别名 `tmsl`）、`database.json`、`pbip`。
- `--force` - 覆盖目标路径下任何现有文件或目录。

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

Set properties on a model object, format its expressions, or sync a table with its source schema. 接受 `<path>` 参数。

`te set` 接受以下参数：

- `-p, --property <Name=Value>` - property assignment (e.g., `-p expression="SUM(Sales[Amt])"`, `-p isHidden=true`). **Repeatable** - everything after the first `=` is the value. Bare positional assignments work too: `te set Sales/Amount formatString="#,0" --save`. Property names are case-insensitive, accept both spellings where the grid label and the TOM name differ (`Hidden` and `IsHidden`), and accept dotted paths and indexers: `-p KPI.StatusGraphic=...`, `-p "Annotations[Tabular Editor]=..."`, `-p "TranslatedNames[fr-FR]=..."`. Run `te get <path> --properties` to list every name an object accepts - see [get](#get). A partition's expression is `-p Expression` whatever kind of partition it is (`MExpression` and `Query` still work). Use `-p Name=-` to read the value from stdin (one assignment per stream; a piped value is taken verbatim, so piping the text `null` stores the word `null`). `-p Name=` assigns an empty string.
- `--unset <Name>` - clear a property; repeatable (`--unset description --unset displayFolder`). `-p Name=null` is the shorthand. Works on every property that can hold nothing - text properties included - and on object-valued ones (`SortByColumn`, `RefreshPolicy`); `-p "Annotations[key]=null"` removes an annotation. Numbers, booleans, and fixed-choice properties cannot be cleared and are refused.
- `--format <PropertyName>` - format that expression property (repeatable; DAX or M is detected from the property). The formatter tweaks `--long` (fewer line breaks) and `--no-space-after-function` require `--format` on a DAX property. `--semicolons` is refused together with `--format`: an expression stored in a model is always comma-separated, so the semicolon dialect can never parse it - format semicolon-authored DAX with [`te util format-dax --semicolons`](#util-format-dax) instead.
- `--update-schema` - sync a table's columns with its source schema: adds new source columns with detected types, retypes drifted ones, and preserves everything else about every existing column (name, description, format string, display folder, sort-by column, visibility, annotations, translations, perspective membership). Removed source columns only warn unless `--drop-removed-columns` (destructive). A renamed source column looks like remove + add - remap it first with `-p SourceColumn=<newName>`. Refused on calculated tables and calculation groups; cannot combine with `-p` or `--format`. With no connection flags, the connection is read from the model itself - the data source the table's partitions are bound to, the connection written into the table's own query, or the model's single usable data source - and the source table from the partition's binding, falling back to the model table's name; `--data-source <name>` chooses when the model has several usable sources. Naming a connection explicitly with the schema-detection flags shared with `te add` (`--source sql|lakehouse|warehouse`, `--endpoint`, `--connection-string`, `--source-database`, `--source-table`) always wins. When no source can be worked out, or the source table cannot be found, the error says which case you are in and names the table it looked for.
- `-t, --type <kind>` - 用于在同一路径可能解析为多种对象类型时消除歧义（`度量值`、`Column`、`CalculatedColumn`、`Hierarchy`、`Calendar`、`分区`、`CalculationItem`）。
- `--save` / `--save-to <path>` - 保存更改。
- `--diff` / `--stat` / `--name-only` - change-output rendering (see the note above).
- `--serialization <fmt>` - 保存时覆盖序列化格式（`tmdl`、`bim`（别名 `tmsl`）、`database.json`）。
- `--force` - 即使修改引入 DAX 验证错误，也会保存。

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

向模型添加对象。 为新对象传入 `<path>`（父级必须已存在；最后一个分段就是新名称），并通过 `-t` / `--type` 指定类型。 关系仍使用其简写语法（`Sales[Key]->Dim[Key]`）。 Container-form paths are valid add targets (`Sales/Measures/Margin`, `Sales/Partitions/Q1`, `Sales/Calendars/Fiscal`, `Roles/Admin/TablePermissions/Sales`, `Roles/Admin/Members/user@x.com`) - any path the CLI prints can be fed back to `te add`.

`te add` 支持以下选项：

- `-t, --type <type>` - 指定对象类型。 Common values: `Table`, `CalculatedTable`, `CalcGroup`, `Measure`, `CalculatedColumn`, `DataColumn`, `Hierarchy`, `Level`, `Calendar`, `CalcItem`, `KPI`, `Partition`, `Expression`, `Function`, `Perspective`, `Culture`, `Role`, `TablePermission`, `Member`. 支持 Tab 自动补全；可通过运行 `te add --help` 获取完整列表。
- `-p, --property <Name=Value>` - property assignment on the new object (repeatable). The expression goes in `-p Expression="..."`, or use `--file`, or `-p Expression=-` to read it from stdin.
- `--file <path>` - read the expression from a file instead of inline.
- `--mode <mode>` - storage mode for new tables: `import` (default), `directquery` (alias `dq`), `dual`, `directlake` (alias `dl`).
- `--if-not-exists` - 如果对象已存在，则直接以 `0` 退出且不报错。 可用于幂等的 CI/CD 管道。
- `--save` / `--save-to <path>` - 保存更改。
- `--diff` / `--stat` / `--name-only` - change-output rendering (see the [Model editing](#model-editing) note).
- `--serialization <fmt>` - override the serialization when saving (`tmdl`, `bim` (alias `tmsl`), `database.json`, `pbip`).
- `--source-type <kind>` - 新表的初始分区源类型：`m`、`query` 或 `calculated`。 这会覆盖启发式检测结果。 `query` builds a legacy SQL `SELECT` partition bound to the model's provider data source and is refused with lakehouse/warehouse sources or when no provider source exists; `calculated` is only valid with `-t CalculatedTable`.
- `--partition-expression <m>` - raw M expression for the new table's initial partition.
- `--force` - 即使修改引入 DAX 验证错误，也会保存。

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

### 删除

删除对象。 默认会检查依赖对象，以避免破坏现有引用。 （别名：`rm`。）

`te remove` 支持以下参数：

- `<path>` - 位置参数：要删除的对象。
- `-t, --type <kind>` - 当路径匹配到表下的多个子对象时，用于消除歧义（例如同名的列和层次结构）。
- `--force` - 跳过依赖对象检查。
- `--if-exists` - 如果对象不存在，则直接以 `0` 退出且不报错。 可用于幂等的 CI/CD 管道。
- `--dry-run` - 预览删除操作而不实际执行。
- `--save` / `--save-to <path>` - 保存更改。
- `--diff` / `--stat` / `--name-only` - change-output rendering (see the [Model editing](#model-editing) note).
- `--serialization <fmt>` - 保存时覆盖序列化格式（`tmdl`、`bim`（别名 `tmsl`）、`database.json`）。

```bash
te remove Sales/Revenue --save
te remove "'Sales'[Revenue]" --save              # DAX form
te remove Sales/Revenue --dry-run                # Preview only
te remove Sales/OldMeasure --if-exists --save    # Idempotent
```

### 移动

移动或重命名模型对象。 源和目标都是 `<path>` 参数。 （别名：`mv`、`rename`。）

`te move` 支持以下参数：

- `-t, --type <kind>` - 当源路径匹配到多种对象类型时，用于消除歧义（例如同名的列和层次结构）。
- `--save` / `--save-to <path>` - 保存更改。
- `--diff` / `--stat` / `--name-only` - change-output rendering (see the [Model editing](#model-editing) note).
- `--serialization <fmt>` - 保存时覆盖序列化格式（`tmdl`、`bim`（别名 `tmsl`）、`database.json`）。
- `--force` - 即使该变更会引入 DAX 验证错误，也仍会保存。

Renaming an object whose name is not yours to set is refused with a non-zero exit code rather than reported as `No changes.` - a relationship (its name always describes the columns it joins), a measure's KPI, a role's table permission.

```bash
te move Sales/Revenue Finance/Revenue --save                # Move measure to another table
te move Sales/Revenue Sales/TotalRevenue --save             # Rename measure
te move Sales/Date Sales/CalendarDate -t Hierarchy --save   # Disambiguate hierarchy from column
te move "Sales/Partitions/Old" "Sales/Partitions/New" --save   # Container-form paths work too
```

## 检查

### list

以类似文件系统的导航方式列出对象。 接受一个支持通配符的 `<path-filter>` 参数。 支持模型级容器和表作用域容器——完整列表见上方的[容器关键字表](#containers-and-keywords)。 （别名：`ls`。）

`te list` 支持：

- `--type <kind>` - narrow to one object kind (`table`, `measure`, `column`, `hierarchy`, `partition`, `relationship`, `role`, `perspective`, `culture`, `calculationitem`, `kpi`, `set`, `function`). 如果不提供 `<path-filter>`，这等同于输入匹配的容器关键字。
- `--paths-only` - 每行输出一个对象路径，适合通过管道传给 `xargs`、`te get` 或 `te set`。
- `--no-multiline` - 将多行单元格（通常是 DAX 或 M 表达式）折叠为单行并截断，让宽表中的各行仍便于浏览。 仅影响文本输出；JSON/CSV/TMSL 输出不受影响。
- `--output-format tmsl`（别名 `bim`）- 将匹配的对象输出为 TMSL/BIM 脚本。 适用于 `te list Tables --output-format bim > tables.json`。 `ls` 不支持 `--output-format tmdl`（TMDL 仅支持单对象输出——请使用 `te get`）。

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
- `--no-multiline` - collapse multi-line cells (with `--ls`/`--where`). 仅适用于文本输出。
- `-t, --type <kind>` - 当路径匹配到表下的多个子对象时，用于消除歧义（例如同名的列和层次结构）。 可选值：`Measure`、`Column`、`CalculatedColumn`、`Hierarchy`、`Calendar`、`Partition`、`CalculationItem`。
- `--output-format tmsl`（别名 `bim`）- 将解析后的对象输出为 TMSL/BIM JSON。
- `--output-format tmdl` - 将解析后的对象输出为 TMDL（仅限命名对象）。

`te get` 和 `te list` 共用同一个描述符目录，因此无论输出为哪种格式，属性的呈现方式都一致：文本表格、JSON 和 CSV 显示的都是同一组属性；给模型新增属性后，也会在所有格式中自动可见。

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
- `--no-multiline` - 将多行匹配上下文折叠为单行。 仅适用于文本输出。

`--in expressions` 涵盖模型中的每个 `IExpressionObject`——包括 KPI 的 `TargetExpression` / `StatusExpression` / `TrendExpression`、度量值的 `DetailRowsExpression`、分区源/轮询的 M 表达式、表权限的 `FilterExpression`，以及计算组的 `MultipleOrEmptySelection` / `NoSelection` 表达式——因此，设置在 KPI 目标上的字面量（例如 `123`）也会像度量值正文一样被找到。

```bash
te find "CALCULATE" --in expressions
te find "Revenue" --in names
te find "CALCULATE" --in expressions --paths-only | xargs -I{} te get {} -p expression
te find "Gross.*Margin" --in names --regex
```

Under `--output-format json`, `te find` reports the scope it searched and the matching mode it used alongside the matches.

### diff

比较两个模型的结构差异。 返回以下退出码：`0` 表示相同，`1` 表示发现差异，`2` 表示错误。

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

分析对象的上游和下游依赖关系，或找出整个模型中未使用的对象。 A shortcut for `te get --deps` / `te get --unused`. 单对象形式接受一个 `<path>`。

`te deps` 接受以下选项：

- `--upstream` - 仅显示上游依赖项（即此对象所使用的对象）。
- `--downstream` - 仅显示下游依赖项（即使用此对象的对象）。
- `--deep` - 显示递归依赖树，而不只显示直接依赖关系。
- `--max-depth <N>` - `--deep` 遍历的最大深度（默认：`10`）。
- `-t, --type <kind>` - 当路径匹配到表下的多个子对象时，用于消除歧义（例如同名的列和层次结构）。
- `--unused` - 列出未被任何 DAX 引用，且未用于任何关系、层次结构级别、排序依据、变体、AlternateOf 基对象或日历时间角色的度量值、计算列以及**所有数据列**。 每条结果在文本模式下会显示 `(hidden)`，在 JSON 中则包含 `isHidden` 字段。
- `--hidden` - 将 `--unused` 限制为仅包含隐藏对象。 隐藏且未使用的对象是最安全的清理候选项，因为没有任何用户可见内容依赖它们。

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
- `--errors-only` - `--no-warnings --no-antipatterns` 的简写：仅显示错误。
- `--no-warnings` - 隐藏语义分析器发出的警告。
- `--no-antipatterns` - 隐藏反模式建议（DAX 最佳实践提示）。
- `--server-only` - 仅显示所连接服务器报告的错误；跳过本地语义分析。
- `--no-multiline` - 将多行单元格内容（错误信息、表达式）折叠为单行。 仅文本输出。

```bash
te validate -m ./model
te validate --ci github --trx results.trx
te validate --errors-only                 # Hide warnings and anti-pattern hints
```

Every finding carries a stable code, shown in the **Code** column of the Errors, Warnings, and Anti-patterns tables as well as in JSON, `--ci` annotations, and `--trx`. Three codes are worth knowing when a hand-written model is involved: `TE0012` (a column and a measure, or two columns, share a name within one table) and `TE0013` (a measure name is repeated across tables) are errors - Analysis Services refuses to load such a model, and `te save-as` refuses to write one unless `--force` or `--skip-validation` is passed; `TE0014` is a warning that a TMDL folder has no `database.tmdl`, so the compatibility level in effect is a substitute for the one the model declared. The folder still loads and `te validate` still exits `0` for `TE0014`; hide it like any other warning with `--no-warnings` or `--errors-only`.

Under `--output-format json`, `te validate` emits the shared findings JSON document (`summary` plus a flat `findings[]` array) shared with `te bpa run`, `te test run`, and `te query` - see @te-cli-findings.

> [!NOTE]
> `te validate` 不支持 `--output-format csv`——CSV 会在一开始就被拒绝，并给出可操作的错误提示，而不是生成不完整的结果。 验证输出使用 `text` 或 `json`。

### bpa run

针对模型运行 Best Practice Analyzer 规则。

`te bpa run` 接受以下选项：

- `-r, --rules <rules>` - JSON 格式的 BPA 规则文件(s)的路径(s)或 URL(s)。 可重复指定。 替换本次调用的用户规则层：请参阅下文的 [规则源和解析](#rule-sources-and-resolution)。
- `--no-model-rules` - 排除嵌入在模型注释中的 BPA 规则。
- `--no-defaults` - 排除内置的默认 BPA 规则。
- `--vpax <file>` - 从 `.vpax` 文件加载 VertiPaq分析器统计信息，以启用可感知 VPA 的规则。
- `--allow-external-rules` - 允许从嵌入在模型注释中的 URL 获取 BPA 规则文件。
- `--rule <id>` - 仅按 ID 运行指定规则(s)。 可重复指定。
- `--path <path-filter>` - 将分析限制为包含匹配对象的表。 支持字面名称、容器关键字和通配符（例如 `'Sales'`、`'Sa*'`、`'Sales/度量值'`、`'*/Amount'`）。
- `--fix` - 应用修复表达式，在可能的情况下自动修复违规项。
- `--save` - 应用修复后，将模型保存回原始位置。
- `--save-to <path>` - 应用修复后，将模型保存到其他路径。
- `--diff` / `--stat` / `--name-only` - change-output rendering for the fix pass (see the [Model editing](#model-editing) note).
- `--serialization <fmt>` - 模型序列化: `tmdl`、`bim` (别名 `tmsl`)、`database.json`。
- `--fail-on <severity>` - 失败阈值：`error`（默认）或 `warning`。 当违规项达到该阈值时，将以退出代码 `1` 退出。 无论 `--fail-on` 如何设置，规则加载或求值错误（表达式无效、规则文件无法读取）也会导致命令以非零状态退出。
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
2. **内置默认规则** - 除非传入 `--no-defaults`，或配置中的 [`bpa.builtInRules`](xref:te-cli-config#built-in-bpa-rules) 为 `false`，否则会加载。 `bpa.disabledBuiltInRuleIds` 中列出的单个内置规则会被跳过。
3. **模型嵌入规则** - 模型 `BestPracticeAnalyzer_Rules` 注释中的规则；除非传入 `--no-model-rules`，否则会加载。 除非同时传入 `--allow-external-rules` 参数，否则会跳过外部 URL 注释。

The built-in defaults are exactly Tabular Editor 3's documented [built-in rule set](xref:built-in-bpa-rules) (the `TE3_BUILT_IN_*` IDs), so `te bpa run` and TE3 Desktop agree on what the built-ins flag. The six VertiPaq Analyzer rules (`VPA_*`) that earlier previews presented as built-in are not part of that set, and the `--vpa-rules` flag no longer exists; if a pipeline gates on one of them, copy its definition into your own rules file and point at it with `--rules`, `bpa.rules`, or `TE_BPA_RULES`. `--vpax` is unchanged and still supplies the statistics a VPA-aware rule of your own reads. C# scripts (`te script`, `te macro run`) see the same rule set through `Bpa.Rules` and `Bpa.Analyze()`.

Each rule ID is evaluated once. When the same ID appears in more than one layer, an explicit `--rules` file's definition wins in `te bpa run`, while the built-in definition wins in the deploy/save gates. 然后会移除模型 `BestPracticeAnalyzer_IgnoreRules` 注释中的规则 ID。

输出中的 `Rules loaded:` 行会列出每个提供规则的层级，例如：

```
Rules loaded: 38 from 1 file(s) from bpa.rules config + built-in defaults + model annotations
```

### bpa rules

管理 BPA 规则集——在本地规则文件或模型注释中列出、检查、初始化，以及启用或禁用规则。 内置规则是只读的。要跳过其中某一条而保留其余规则，请使用 `te bpa rules disable`（不要直接编辑内置规则集）。

子命令：

| 子命令                                                | 用途                           |
| -------------------------------------------------- | ---------------------------- |
| `add <id>`                                         | 添加新的 BPA 规则。                 |
| [`disable`](#bpa-rules-disable)                    | 为当前用户禁用一条内置 BPA 规则。          |
| [`enable`](#bpa-rules-enable)                      | 重新启用先前已禁用的内置 BPA 规则。         |
| `ignore <rule-id>`                                 | 将规则添加到模型的忽略列表。               |
| [`init`](#bpa-rules-init)                          | 在解析后的 PATH 下创建一个空的 BPA 规则文件。 |
| [`list`](#bpa-rules-list)（别名 `ls`）                 | 列出来自所有来源的 BPA 规则及其状态。        |
| `remove <rule-id>` (alias `rm`) | 删除一条 BPA 规则。                 |
| `set <rule-id>`                                    | 更新 BPA 规则的属性。                |
| `unignore <rule-id>`                               | 从模型的忽略列表中移除一条规则。             |

`te bpa rules` 的所有子命令都接受以下选项：

- `--rules-file <path>` - 指定 BPA 规则 JSON 文件的 PATH。 默认使用你的 CLI 配置（`~/.config/te/config.json`）中 `bpa.rules` 的首个已存在条目，或使用 `TE_BPA_RULES` 环境变量。
- `--model-rules` - 操作嵌入在模型注释中的规则，而非文件中的规则。

> [!IMPORTANT]
> `te bpa rules set` 和 `te bpa rules remove` 会拒绝修改内置规则 ID。 如果尝试这样做，命令将以退出码 `1` 退出，并提示改用 `te bpa rules disable`。 要自定义内置规则的行为，先禁用该内置规则，再添加一个使用不同 ID 的自定义副本：
>
> ```bash
> te bpa rules disable TE3_BUILT_IN_DATE_TABLE_EXISTS
> te bpa rules add MY_DATE_TABLE_EXISTS
> ```

#### bpa rules list

列出来自所有来源的规则（内置、用户、模型）。 （别名：`ls`。）

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

在配置的 PATH 处创建一个空的 BPA 规则文件（`[]`）。 在对尚不存在的路径执行 `te bpa rules set` / `te bpa rules remove` 之前，先运行一次这个命令。

`te bpa rules init` 接受以下选项：

- `--force` - 用 `[]` 覆盖现有文件。 如果目标文件已存在，则必须提供此选项。
- `--rules-file <path>` - 目标文件路径。 可出现在 `init` 子命令之前或之后。

路径解析（先匹配到的优先）：`--rules-file` → `TE_BPA_RULES` 环境变量 → CLI 配置中 `bpa.rules[]` 的第一项 → `./BPARules.json` (当前工作目录)。

```bash
te bpa rules init
te bpa rules init --rules-file ./MyRules.json
te bpa rules init --force
```

#### bpa rules add / set / remove / ignore / unignore

修改规则文件（`add`、`set`、`remove`（别名 `rm`））或模型内嵌的忽略列表（`ignore`、`unignore`）。 这三个修改型子命令都针对 `--rules-file <path>` 或 `--model-rules` 操作，并且会拒绝修改内置规则 ID。

- `te bpa rules add <id>` - 创建新规则。 将每个属性作为命名选项传入：
  - `--name <text>` - 便于阅读的规则名称（必填）。
  - `--scope <list>` - 规则适用的对象类型（以逗号分隔）：`度量值`、`Column`、`Table`、`Hierarchy`、`分区`、`Relationship`、`Role`、`Perspective`、`Culture` 等 (必填)。
  - `--expression <text>` - Dynamic LINQ 谓词。 对于违反规则的对象，返回 `true`（必需）。
  - `--category <text>` - 分组标签（例如 `Performance`、`Naming`、`DAX Expressions`）。
  - `--severity <1|2|3>` - `1`（信息）、`2`（警告，默认）、`3`（错误）。
  - `--description <text>` - 规则触发时向用户显示的说明。
  - `--fix-expression <text>` - `te bpa run --fix` 用于自动修复的 Dynamic LINQ 表达式。
- `te bpa rules set <id>` - 更新现有规则的属性。 Uses `-p, --property <name=value>` (repeatable; `-` reads the value from stdin). 属性名称：`name`、`expression`、`scope`、`category`、`severity`、`description`、`fixExpression`。
- `te bpa rules remove <id>` - 删除规则。
- `te bpa rules ignore <id>` - 将规则 ID 添加到模型的 `BestPracticeAnalyzer_IgnoreRules` 注解中。
- `te bpa rules unignore <id>` - 从模型的忽略列表中移除规则 ID。

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

禁用单个内置 BPA 规则。 该规则 ID 会添加到 CLI 配置中的 `bpa.disabledBuiltInRuleIds`。 后续的门禁执行（deploy、save、mutation）以及 `te bpa run` 都会跳过已禁用的规则。

该命令是幂等的——对已禁用的规则再次运行 `disable` 也会成功，且不会修改配置。 如果 `<rule-id>` 不是内置规则，命令会以退出代码 `1` 结束；可使用 `te bpa rules list` 查看有效的内置 ID。

```bash
te bpa rules disable TE3_BUILT_IN_DATE_TABLE_EXISTS
```

#### bpa rules enable

通过从 `bpa.disabledBuiltInRuleIds` 中移除规则 ID，重新启用此前已禁用的内置 BPA 规则。 如果该规则当前并未被禁用，则以退出代码 `1` 结束。

```bash
te bpa rules enable TE3_BUILT_IN_DATE_TABLE_EXISTS
```

### vertipaq

分析 VertiPaq 存储统计信息。

`te vertipaq` 支持：

- `<path>` - 可选的位置参数：表名，用于将分析范围限定在单个表上。
- `--columns`, `--relationships`, `--partitions`, `--all`。
- `--detail` - 显示扩展列（数据/字典/层次结构大小明细、编码、分段）。
- `--fields <list>` - 要显示的字段，以逗号分隔（例如：`--fields name,card,size,%tbl,%db,bar`）。 可用字段因视图而异。
- `--export <file.vpax>` - 将 VertiPaq 统计信息导出为 `.vpax` 文件，以便离线分析。
- `--import <file.vpax>` - 加载之前导出的 `.vpax` 文件并进行离线分析。
- `--obfuscate` - 对导出的 VPAX 中的名称和表达式进行混淆处理。
- `--top <N>`、`--stats`、`--annotate`、`--save`。
- `--auth <method>` - 连接到远程模型时，用于覆盖默认的身份验证方法。

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

`te query` 支持以下选项：

- `<dax>` - 位置参数：要执行的 DAX 查询。 等同于传入 `-q`。 选择你觉得更易读的写法即可；如果两者都提供，以显式的 `-q` 为准。
- `-q, --query <dax>` - 内联查询（即上述位置参数的命名参数形式）。 `-q -` reads the query from stdin; with input piped and no query given at all, stdin is read implicitly.
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

针对语义模型执行一个或多个 C# Script。 CLI 使用与 Tabular Editor 3 Desktop 相同的脚本宿主，因此能在 TE3 中运行的脚本在这里也可原样运行。

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
> - **CLI 脚本中不支持交互式选择。** 从 `te script` 调用 TE3 Desktop 辅助方法 `SelectMeasure()`, `SelectTable()`, `SelectColumn()`, `SelectObject()`, 和 `SelectObjects()` 时，会抛出 `NotSupportedException`，因为 CLI 没有可弹出的 UI。 在脚本外预先解析对象(s)，并通过环境变量或 stdin 传入；如果脚本与 TE3 共享，请将调用包装在 `try/catch` 中。
> - **默认的 `using` 指令与 TE3 Desktop 一致。** 使用 `DataTable`、`File`、`StringBuilder` 或 `Regex` 的脚本，必须显式包含对应的 `using System.Data;` / `using System.IO;` / `using System.Text;` / `using System.Text.RegularExpressions;` 指令。

> [!NOTE]
> **跨宿主脚本的预处理器符号。** 由 `te script` 编译的脚本会定义符号 `TECLI`。 TE3 Desktop 脚本会改为定义 `TE3`，并且还会定义带版本范围限定的符号，例如 `TE3_3_10_OR_GREATER` …… 当前 TE3 次版本对应的是 `TE3_3_X_OR_GREATER`。 TE2 不定义这两个符号。 使用这些符号可编写可移植脚本：
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

通过宏 JSON 文件（通常为 `MacroActions.json`）管理和运行宏。 宏文件的 PATH 按以下顺序解析：`--macros <path>` → 环境变量 `TE_MACROS_PATH` → CLI 配置中的 `macros` → `./MacroActions.json`。 On Windows, the `DisableMacros` administrator policy refuses every `te macro` command - see [Administrator policies](xref:te-cli-config#administrator-policies).

子命令：

| 子命令                                | 用途                  |
| ---------------------------------- | ------------------- |
| `list`（别名 `ls`）                    | 列出宏。                |
| 宏：[`run <name-or-id>`](#macro-run) | 运行宏。                |
| `add <name>`                       | 添加宏。                |
| `set <name-or-id>`                 | 更新宏属性。              |
| `remove <name-or-id>`（别名 `rm`）     | 删除宏。                |
| `sort`                             | 排序并重新分配 ID。         |
| 宏：[`init`](#macro-init)            | 在解析得到的路径处创建一个空的宏文件。 |

#### 宏：add / set / remove

修改宏文件 (`add`、`set`、`remove` (别名 `rm`))。 这三个命令都操作 `--macros <path>`（或解析得到的宏文件）。

- `te macro add <name>` - 创建新宏。 使用 `-e "<code>"`（内联）或 `-s <file.cs>`（脚本文件）提供脚本主体。 可选：`--tooltip <text>`、`--contexts <list>`（宏适用的上下文，例如 `Table,Measure`，即“表、度量值”）、`--enabled true|false`。
- `te macro set <name-or-id>` - 更新宏属性。 Use `-p, --property <name=value>` (repeatable; `-` reads the value from stdin). 属性名称：`name`、`execute`、`enabled`、`tooltip`、`validContexts`。
- `te macro remove <name-or-id>` - 删除宏。

```bash
te macro add MyMacro -e "Info(Selected.Measure.Name);" --tooltip "Print measure name" --contexts Measure
te macro set MyMacro -p tooltip="Updated tooltip"
te macro remove MyMacro
```

#### macro init

在配置的路径下创建一个空的宏文件（`{\"Actions\":[]}`）。 当解析后的宏文件尚不存在时，只需运行一次该命令。

`te macro init` 接受：

- `--force` - 覆盖现有文件。 如果目标已存在，则必须指定此参数。
- `--macros <path>` - 目标文件路径。 可放在 `init` 子命令之前或之后。

```bash
te macro init
te macro init --macros ./project-macros.json
te macro init --force
```

#### macro run

运行宏。 通过 `dataTable.Output()` 输出表格的宏会在终端中显示格式化输出，因此 DAX 风格的查询宏在 `te macro run` 中的行为与在 TE3 中相同。

`te macro run` 接受：

- `--on <path>` - 将宏的选择上下文设置为单个已命名对象（如表、度量值、列等…）。 这相当于在 TE3 中右键单击该对象，并从上下文菜单调用宏。
- `--save` / `--save-to` - 将宏所做的所有更改持久化保存。 Like every mutating command, `te macro run` is a dry run without `--save`.
- `--serialization <fmt>` / `--force` - as on the other mutating commands.

```bash
te macro run "Hide all measures"
te macro run "Format DAX" --on Sales/Revenue --save
te macro run "Format DAX" --on "'Net Sales'[Sales Amount]" --save   # DAX form works in --on too
```

## 部署和刷新

### deploy

将语义模型部署到 Power BI、Fabric、Azure Analysis Services 或本地 SQL Server Analysis Services。

**Dry run by default**: `te deploy` connects read-only and prints the exact TMSL it would send to stdout. Add `--execute` to actually deploy.

`te deploy` 支持以下参数：

- `-s, --server` / `-d, --database` - the model **source**, exactly as on every other command.
- `--target-server <target>` / `--target-database <name>` - the deploy **destination**: a workspace name, endpoint, or server, and the semantic model name to create or overwrite. 使用服务器名称、FQDN、IP 地址或 MSOLAP 连接字符串时，会部署到 Analysis Services（本地环境使用 Windows 集成身份验证）；使用 Workspace 名称或 `powerbi://...` URL 时，会部署到 Power BI。 For local model sources, the target falls back to the active `te connect` connection; when the source is remote, the target flags are required. Deploying a model onto itself is refused.
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
- `--bpa-rules <PATH>` - 可重复指定；仅针对本次部署覆盖 CLI 配置中的 `bpa.rules`。 除非 `bpa.builtInRules` 为 `false`，否则内置规则仍会生效。
- `--force` - skip the interactive confirmation.
- `--ci <fmt>` - `vsts` (aliases `azdo`, `azure-devops`) or `github` (alias `gh`); unrecognised values are rejected up front.
- `-p, --profile <name>` - 一次性使用已保存的 @te-cli-auth 配置文件。

`--output-format bim|tmdl` is rejected on deploy. To capture the deployment script for review, redirect the dry-run output: `te deploy ... > deploy.tmsl`.

```bash
te deploy -m ./model --target-server my-workspace --target-database my-model --execute --force --ci github
te deploy -m ./model --target-server MY.SERVER.COM --target-database my-model --execute --force    # On-prem SSAS
te deploy -m ./model --target-server my-workspace --target-database my-model > deploy.tmsl         # Dry run: TMSL only
te deploy -s src-workspace -d src-model --target-server dst-workspace --target-database copy --execute   # Remote to remote
te deploy --local --target-server my-workspace --target-database my-model --execute                # Publish a Desktop model
```

> [!IMPORTANT]
> `te deploy` 会在执行前运行 Best Practice Analyzer 作为门控检查。 BPA 门控配置请参见 @te-cli-config。

A deploy **fails** when the server reports errors on one or more objects, even though the metadata has been written: the exit code is non-zero, JSON reports `"success": false` with the reason in `error`, the headline says the deploy landed with errors, and `--ci` reports the object errors as errors. Unprocessed objects are not a failure - a metadata-only deploy legitimately leaves objects holding no data. The workspace mirror set up with `te connect -w` applies the same rule.

> [!NOTE]
> 当设置 `--output-format json` 时，`te deploy` 的 JSON 输出始终包含解析后的 `server` 和 `database`，即使它们是从活动连接或配置文件中解析得到的，而不是显式传入的。 管道可使用这些字段来确认部署目标，而无需重新解析命令行。 `te deploy` also exits non-zero on failure under `--output-format json`, matching its text-mode behavior - the JSON payload is the failure record, not a success signal.

### refresh

在已部署的模型上触发数据刷新。

**Dry run by default**: `te refresh` prints the TMSL a refresh would send to stdout. Add `--execute` to run it.

`te refresh` 支持：

- `--type <type>` - `full`、`dataonly`（别名 `data-only`、`data`）、`automatic`（别名 `auto`）、`calculate`（别名 `calc`）、`clearvalues`（别名 `clear`）、`defragment`（别名 `defrag`）、`add`（默认值：`automatic`）。
- `--table <name>` - 刷新特定表(可为多个)；可重复指定。
- `--partition <Table.Partition>` - 刷新特定分区(可为多个)。
- `--execute` - actually run the refresh. At a terminal it asks for confirmation with **`n` as the safe default**; add `--force` to skip the question. An unattended run (redirected output, `--output-format json`, or `--non-interactive`) stops with an error unless `--force` is given, so `te refresh --type full --execute --force` is the CI form.
- `--force` - skip the confirmation prompt.
- `--apply-refresh-policy <true|false|table>` - apply incremental refresh policies to determine which partitions are refreshed; pass a table name to scope the refresh to that table. Policies apply by default when the refresh type and scope are compatible, except for models hosted in Power BI Desktop. An explicit value wins (with warnings when it cannot take effect).
- `--effective-date <yyyy-MM-dd>` - set the effective date used by the refresh policy (ignored, with a warning, when no policy applies).
- `--max-parallelism <N>` - 设置可并行刷新的最大分区数。 将刷新封装在 TMSL `sequence` 命令中。
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

`te test list` 也支持使用 `ls` 作为别名。

其他子命令可用于搭建测试脚手架、打印断言规范格式、切换当前活动套件、列出套件、捕获快照以及比较模型。 查看 `te test --help` 了解详情。

```bash
te test init --example             # Scaffold an example suite
te test spec                       # Print the full assertion format reference
te test init --from-model --model ./my-model  # Generate stubs from your measures
```

## 连接和身份验证

### connect

设置（或显示）当前终端会话的活动连接。 查看 @te-cli-auth。

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

将主源与次要目标配对，使后续每次执行 `--save` 都会在两者之间同步镜像模型。 适合保留远程 Workspace 的本地工作副本，或在保存时将本地修改推送到 Workspace。

- `te connect <ws> <model> -w ./src` - 主源为远程；`./src` 会接收初始 TMDL 导出，并在每次保存时保持镜像同步。
- `te connect ./src -w <ws> <model>` - 主源为本地；首次部署会将模型推送到 Workspace，后续保存会自动重新部署。
- `--workspace-format <fmt>` - 将内容镜像到文件夹/文件时，选择磁盘上的格式：`tmdl`、`bim`（别名 `tmsl`）或 `database.json`。 若省略，则会根据 Workspace 目标路径推断格式（例如，`-w ./model.bim` 会推断为 BIM）。
- `--workspace-auth <method>` - 当主目标为本地时，为远程 Workspace 目标指定身份验证方式。 若设置了 `--auth`，则默认与其一致；否则默认为 `auto`。
- `--force` - 当目标已存在（例如文件夹非空或数据库已存在）时必须使用。 如果不使用它，`te connect` 会显示交互式 `y/n` 提示，并以 `n` 作为安全的默认选项。

启用后，`te set --save`、`te remove --save`、`te script --save` 等都会透明地进行双重保存。 保存顺序始终是 **先本地，后远程**，因此即使推送到服务器失败，磁盘上的副本也会反映最新的用户更改。 使用 `te connect --clear` 清除镜像。

```bash
te connect Finance "Revenue Model" -w ./revenue-model    # Mirror remote → local TMDL
te connect ./revenue-model -w Finance "Revenue Model"    # Mirror local → remote
```

### auth login / status / logout

管理缓存的身份验证信息。 参见 @te-cli-auth。

### profile list / show / set / remove

管理命名连接配置文件。 （`te profile list` 的别名：`ls`；`te profile remove` 的别名：`rm`。） 参见 @te-cli-auth。

## 配置

### config list / paths / init / set

View and manage CLI configuration. （`te config list` 的别名是 `ls`。） 参见 @te-cli-config。

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
- `--long` - long format with fewer line breaks. 默认为短格式。
- `--no-space-after-function` - 省略函数名称后的空格。

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

说明旧版 Tabular Editor 2 CLI 参数如何映射到新 CLI 的参考指南。 在迁移基于 TE2 的管道时，可作为实时速查参考。 完整迁移指南参见 @te-cli-migrate。

```bash
te util migrate                   # Full flag mapping table
te util migrate -A                # Look up a single TE2 flag
te util migrate --output-format json     # Machine-readable mapping
```

## Shell

### interactive

使用具备模型感知能力的提示词启动引导式 REPL 会话。 参见 @te-cli-interactive。

> [!TIP]
> 在终端中直接运行不带任何参数的 `te`，默认也会进入 REPL（就像运行 `te interactive` 一样）。 此行为由 `launchInteractiveMode` 配置项控制，参见 @te-cli-interactive#auto-launch-on-empty-invocation。

`te interactive` 接受以下选项：

- `--no-banner` - 启动时跳过欢迎横幅。 从脚本驱动 REPL 时很有用。
- `--echo` - 在输出结果之前，将每条已执行命令回显到 stdout。 当通过 stdin 管道传入命令时很有帮助，这样日志会显示实际运行了什么。
- `--batch` - 非交互式批处理模式：逐行从 stdin 读取命令，执行每条命令，并在 EOF 时退出。 当 stdin 被重定向时会自动启用。
- `--no-batch` - 即使 stdin 被重定向，也强制使用交互式 TTY 模式（与 `--batch` 互斥）。

```bash
te interactive                                # Connect later
te interactive --model ./model                # Start with a local model
te interactive -s MyWorkspace -d MyModel      # Start with a remote model
printf "list Measures\nexit\n" | te interactive --model ./model   # Pipe commands via stdin
```

Inside the session, mutating commands stage in memory: `save` (no arguments) commits the staged edits and `revert` discards them, while `save-as` re-serializes to a format or location. Closing a session that still holds staged edits asks for confirmation (or, when nobody can answer, warns and exits non-zero); `exit --force` throws them away deliberately - see @te-cli-interactive.

引号和 DAX 风格的引用在会话内外的用法一致——有关 REPL 中支持括号感知的 argv 拆分的详细信息，请参见上文的[对象路径](#object-paths)一节以及 @te-cli-interactive。

### 会话

显示或管理当前终端会话。 CLI 会将每个终端的状态（活动连接、活动配置文件、活动测试套件）保存在会话文件中，并在各个 shell 进程之间相互隔离。 设置 `TE_SESSION` 环境变量，以在不同 shell 之间共享一个命名会话。

子命令：

| 子命令             | 用途                                       |
| --------------- | ---------------------------------------- |
| `show`          | 显示当前会话的详细信息（ID、文件路径、活动状态）。 未提供子命令时的默认行为。 |
| `list`（别名 `ls`） | 列出所有会话文件。                                |
| `clear`         | 清除当前会话的活动状态。                             |
| `prune`         | 删除其 shell 进程已停止运行的会话文件。                  |

`te session prune` 支持以下选项：

- `--all` - 还会删除 shell 仍在运行的会话，以及已命名（`TE_SESSION`）的会话。 当前会话始终会被保留。
- `--dry-run` - 仅显示将要删除的内容，不执行实际删除。

```bash
te session                        # Show current session details
te session list                   # List all session files
te session clear                  # Clear active state for this session
te session prune                  # Remove sessions whose shell is dead
te session prune --all --dry-run  # Preview a full cleanup
```

### completion

为 `bash`、`zsh`、`powershell`（别名 `pwsh`）或 `fish` 生成 shell 自动补全脚本。 参见 @te-cli-install。

```bash
te completion bash
te completion zsh
te completion pwsh
te completion fish
```

## 退出代码

| 退出代码 | 含义                                                                                                                                                                                                                                                                                             |
| ---- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `0`  | 成功。                                                                                                                                                                                                                                                                                            |
| `1`  | Generic failure (invalid arguments, command failed, validation errors, auth failure, BPA gate failed at severity >= error, a `te script` run in which a script reported an error, a `te deploy` the server accepted with object errors). 用于 `te diff`：发现差异。 |
| `2`  | 仅适用于 `te diff`：比较时发生错误，因此差异状态未知。                                                                                                                                                                                                                                                               |

如需在 CI 管道中进行更细致的控制，可将退出代码与 `--ci <vsts/github>` 注释以及 `--trx` 结果文件结合使用——参见 @te-cli-cicd。

## 相关页面

- @te-cli - 概览和背景说明。
- @te-cli-install - 安装并设置 CLI。
- @te-cli-auth - 进行身份验证并管理连接。
- @te-cli-config - 配置文件、BPA 门禁和变更后行为。
- @te-cli-findings - the findings JSON shared by validate, bpa run, test run, and query.
- @te-cli-migrate - TE2 → TE3 标志映射。
