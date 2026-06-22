---
uid: te-cli-commands
title: 命令参考
author: Peer Grønnerup
updated: 2026-05-12
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

- **`<path>`** - 解析为**恰好一个**对象或容器。 用于对单个目标执行操作的命令：`te get`、`te set`、`te add`、`te rm`、`te mv`、`te format -p`、`te deps`、`te macro run --on`。
- **`<path-filter>`** - 解析为**零个或多个**对象，并支持通配符。 用于对一组对象执行操作的命令：`te ls`、`te bpa run --path` 以及其他用于检查的命令。

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

### DAX 风格的引用（仅对象路径）

凡是允许使用 `<path>` 的位置，都接受两种 DAX 形式：

- **`'Table'[Member]`**：等同于 `Table/Member`。 方括号后缀会在存在歧义时优先匹配列和度量值，而不是层次结构/分区。
- **`[Member]`**：一&#x4E2A;_&#x72EC;&#x7ACB;_&#x7684;度量值或列，前面不带表名。 在整个模型中搜索具有该名称的度量值或列。 两者都存在时，优先选择度量值。

```bash
te get "'Sales'[Amount]"             # Same as te get Sales/Amount
te get "'Net Sales'[Sales Amount]"   # Spaced names via DAX form
te get "[Total Sales]"               # Model-wide measure-or-column lookup
```

### 容器和关键字

有一些名称可用作容器关键字。 关键字既可以单独使用（列出整个容器），也可以出现在路径中（跳转到当前父级下的该子集合）。

| 关键字                                                                                                                   | 范围   | 含义           |
| --------------------------------------------------------------------------------------------------------------------- | ---- | ------------ |
| `Tables`, `度量值`, `Columns`, `Hierarchies`, `分区`                                                                       | 模型   | 模型中该类型的所有对象。 |
| `关系`, `角色`, `Perspectives`, `Cultures`, `DataSources`, `Expressions`, `CalculationGroups`, `Functions`, `Annotations` | 模型   | 模型级容器。       |
| `度量值`, `Columns`, `Hierarchies`, `分区`, `Calendars`, `CalculationItems`                                                | 表    | 表下的子容器。      |
| `Levels`                                                                                                              | 层次结构 | 层次结构的级别。     |
| `Members`, `TablePermissions`（别名 `Permissions`）                                                                       | 角色   | 角色的子级对象。     |

以下示例展示普通路径与限定容器范围的路径之间的区别：

```bash
te get Sales/Revenue                       # Measure or column on Sales
te get Sales/Measures/Revenue              # Same, container-scoped - disambiguates if other kinds share the name
te get Sales/Geography/Levels/Year         # Specific level of a hierarchy
te get Roles/Admin/Members/bob@example.com # Role member
te get Sales/refreshPolicy                 # Refresh-policy sub-object on a table
te get "Measures/Revenue/KPI"              # KPI sub-object of a measure
```

当实际对象名称恰好与关键字同名时，可为该分段加上引号，以强制进行字面名称匹配。 字面名称为 `Tables` 的表需要写作 `'Tables'`，可通过 `te get "'Tables'"` 访问。

### 筛选路径中的通配符

筛选路径引入了一个通配符字符 `*`，用于匹配单个分段内任意长度的字符序列（贪婪匹配，且仅限单个分段）。 通配符是 `te ls` 和类似命令用来缩小结果范围的方式。

```bash
te ls 'Sa*'                          # Tables whose name starts with Sa
te ls 'Sales/*Amount'                # Children of Sales whose name ends with Amount
te ls '*/Amount'                     # An Amount column/measure across every table
te ls 'Roles/Re*/Members'            # Members of every role matching Re*
```

包含 **N 个分段** 的筛选路径会返回 **N 层深度** 的结果——通配符不会自动多展开一层，结果深度不会超过你输入的层级。 单分段快捷写法 `te ls Sales` 是个例外：未限定且不含通配符的表名会展开为该表的直接子项，以符合“让我看看 Sales 里有什么”的意图。 相比之下，`te ls Sa*` 只返回匹配的表，不会展开。

筛选路径中不支持 DAX 的方括号后缀；如需按字面匹配包含 `[` 和 `]` 的名称，请给名称加引号。

### 错误和提示

分段拼写错误时会给出一条与上下文相关的错误；如果 CLI 能猜到你的意图，还会附带“你是不是想输入……”的提示。 缺少父级的路径会在检查叶节点之前失败，因此信息会指向真正出错的分段。 空容器（例如，在没有层次结构的模型上运行 `te ls Hierarchies`）会给出简单的“这里没有内容”提示，而不是错误。

## 全局选项

这些标志适用于每个命令，可在子命令名称之前或之后使用。

| 选项                         | 说明                                                                                                                                                                                 |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-m, --model <path>`       | 语义模型的路径（TMDL 文件夹、`.bim` 文件或 TE 文件夹）。                                                                                                                                               |
| `-s, --server <endpoint>`  | Workspace 名称或终结点（例如 `MyWorkspace`、`powerbi://...`、`asazure://...`、`localhost`）。                                                                                                    |
| `-d, --database <name>`    | Workspace 上的语义模型名称。                                                                                                                                                                |
| `--local`                  | 连接到本地运行的 Power BI Desktop 实例（仅限 Windows）。                                                                                                                                          |
| `--auth <method>`          | 身份验证方法：`auto`、`interactive`、`spn`、`env`、`managed-identity`（默认值：`auto`）。                                                                                                            |
| `--output-format <format>` | 标准输出格式：`text` (默认)、`json`、`csv`、`tmsl` (别名 `bim`)、`tmdl`。 `csv` 会被输出表格数据的命令采用；`tmsl`/`tmdl` 仅在 `te get` 和 `te ls` 中用于整个对象的序列化。 命令会拒绝其不支持的格式。 |
| `--error-format <format>`  | 用于错误、警告和提示的 stderr 格式：`text`（默认）或 `json`。 其他值将回退为 `text`。 它独立于 `--output-format`，因此你可以将 JSON 格式的 stdout 与纯文本错误配合使用（反之亦然）。                                                          |
| `--recent [N]`             | 使用最近使用过的模型。 未提供值 = 进入交互式选择器；`N` = 最近使用列表中的第 N 个（1 = 最近一次使用）。                                                                                                                       |
| `--non-interactive`        | 禁用所有交互式提示。 如果缺少必需输入，将给出可操作的错误提示并失败退出。                                                                                                                                              |
| `--debug`                  | 启用调试日志并输出到 stderr（连接字符串、身份验证流程、耗时）。                                                                                                                                                |

对于读取模型的命令，解析顺序如下：

位置参数 `<model>` → 全局选项 `--model` → `--server`/`--database`（远程）→ `te connect` 的当前活动连接 → `--recent`。

## 模型 I/O

### load

加载语义模型，并显示模型摘要——名称、兼容级别以及主要对象数量（表、度量值、列）。

```bash
te load ./model                            # TMDL folder
te load model.bim                          # BIM file
te load -s MyWorkspace -d MyModel          # Remote workspace
```

### save

将模型保存到磁盘。 可用于将远程 Workspace 中的模型写入本地文件、转换格式，或将编辑内容保存回源位置。

`te save` 接受：

- `-o, --output-path <path>` - 目标文件或文件夹。 **可选** - 若省略，`te save` 会写回源位置，保留原始格式。
- `--serialization <fmt>` - `tmdl`, `bim`, `te-folder`, `pbip`, `database.json`。 默认会从已加载的模型中推断（BIM 源 → BIM；TMDL `SemanticModel/` → `definition/` 下的 TMDL）。
- `--force` - 跳过验证并覆盖现有输出。 某些拒绝情况（例如容器不明确、项目根目录中存在多个 `SemanticModel`）即使使用 `--force` 也会触发。
- `--skip-bpa` - 完全绕过 BPA 检查。
- `--fix-bpa` - 当规则定义了修复表达式时，自动修复 BPA 违规项。
- `--bpa-rules <path>` - 可重复指定；仅对本次保存覆盖 CLI 配置中的 `bpa.rules`。 除非 `bpa.builtInRules` 为 `false`，否则内置规则仍会生效。
- `--skip-validation` - 跳过 DAX 语义分析和验证，以实现快速直通下载。
- `--supporting-files` - 生成 Fabric 支持文件（`.platform`、`definition.pbism`）。

```bash
te save                                    # Save back to source (no -o needed)
te save ./model.bim -o ./tmdl-out          # Convert BIM to TMDL
te save -o ./project --serialization pbip         # Save as a PBIP project
te save -o ./out -s my-workspace -d my-model --skip-validation   # Fast download
```

> [!TIP]
> 你可以用 `te save -o <path> -s <Workspace> -d <model>` 把远程模型下载到磁盘。 如果你只需要原始字节数据（不做 DAX 语义分析），配合 `--skip-validation` 可实现最快的直通下载。

### open

在 Tabular Editor 3 桌面版中打开模型。 **仅限 Windows**（需要先安装 TE3）。

```bash
te open ./my-model
```

### init

在指定路径创建一个新的空语义模型。

```bash
te init ./new-model
```

## 模型编辑

### set

设置模型对象的属性。 接受 `<path>` 参数。

`te set` 接受以下参数：

- `-q <property>` - 属性名称（例如 `expression`、`formatString`、`description`、`isHidden`）。
- `-i <value>` - 值（使用 `-` 可从 stdin 读取）。
- `--save` / `--save-to <path>` - 保存更改。

```bash
te set Sales/Amount -q expression -i "SUM(Sales[Amt])" --save
te set "'Net Sales'[Sales Amount]" -q formatString -i "#,0" --save   # DAX form with spaced names
te set Sales -q isHidden -i true --save
```

### add

向模型添加对象。 为新对象传入 `<path>`（父级必须已存在；最后一个分段就是新名称），并通过 `-t` / `--type` 指定类型。 关系仍使用其简写语法（`Sales[Key]->Dim[Key]`）。

`te add` 支持以下选项：

- `-t, --type <type>` - 指定对象类型。 常用值：`Table`、`Measure`、`Column`、`CalculatedColumn`、`Hierarchy`、`Role`、`Perspective`、`Culture`、`CalculationGroup`、`CalculationItem`。 支持 Tab 自动补全；可通过运行 `te add --help` 获取完整列表。
- `--if-not-exists` - 如果对象已存在，则直接以 `0` 退出且不报错。 可用于幂等的 CI/CD 管道。

```bash
te add Sales/Revenue -t Measure -i "SUM(Sales[Amount])" --save
te add Sales -t Table --save
te add "Sales[ProdKey]->Product[ProdKey]" --save                           # Relationship shorthand
te add Sales/MarketingFlag -t CalculatedColumn -i "Sales[Amount] > 1000" --if-not-exists --save
te add Perspectives/Default/Sales --save                                   # Include Sales in the Default perspective
te add Roles/Reader -t Role --save                                         # New role at the model level
```

对于数据绑定表，`te add` 还支持从 SQL、Lakehouse 或 Warehouse 源推断架构。 有关 `--source`、`--endpoint`、`--source-table`、`--columns` 等参数，可查看 `te add --help`。

### rm

删除对象。 默认会检查依赖对象，以避免破坏现有引用。

`te rm` 接受：

- `<path>` — 位置参数：要删除的对象。
- `--force` — 跳过依赖对象检查。
- `--if-exists` — 如果对象不存在，则直接以 `0` 退出且不报错。 可用于幂等的 CI/CD 管道。
- `--dry-run` — 预览删除操作而不实际执行。
- `--save` — 将更改保存到已加载的模型。

```bash
te rm Sales/Revenue --save
te rm "'Sales'[Revenue]" --save              # DAX form
te rm Sales/Revenue --dry-run                # Preview only
te rm Sales/OldMeasure --if-exists --save    # Idempotent
```

### mv

移动或重命名模型对象。 源和目标都是 `<path>` 参数。

```bash
te mv Sales/Revenue Finance/Revenue --save    # Move measure to another table
te mv Sales/Revenue Sales/TotalRevenue --save # Rename measure
```

### replace

在各个模型对象中查找并替换文本。 默认仅进行干运行；添加 `--save` 才会实际应用更改。

`te replace` 接受：

- `--in <scope>` - 作用域：`names`、`expressions`、`descriptions`、`displayFolders`、`formatStrings`、`annotations`、`all`（默认值：`all`）。
- `--regex` - 将查找模式视为正则表达式。
- `--case-sensitive` - 启用大小写敏感匹配。
- `--dry-run` - 仅预览更改，不会实际应用。 默认行为。
- `--save` - 将变更保存回源位置。 与 `--revert` 和 `--stage` 互斥。
- `--save-to <path>` - 保存到不同的路径（意味着 `--save`）。
- `--serialization <fmt>` - 模型序列化格式：`tmdl`、`bim`、`te-folder`。
- `--force` - 即使替换引入 DAX 验证错误，也会保存。

`--in expressions` 会遍历所有包含表达式的属性：

- **度量值**：`Expression`、`DetailRowsExpression`
- **KPI**：`TargetExpression`、`StatusExpression`、`TrendExpression`
- **分区**：源 M、轮询 M
- **表格权限**：`FilterExpression`
- **计算组**：选择表达式
- **计算列**：DAX 表达式

在模型中新增具有表达式形态的属性后，工具会自动将其纳入遍历范围。

```bash
te replace "OldTable" "NewTable" --in expressions --save
te replace "SUM" "SUMX" --regex --in expressions --save
```

## 检查

### ls

以类似文件系统的导航方式列出对象。 接受一个支持通配符的 `<path-filter>` 参数。 同时支持模型级容器（`Tables`, `Measures`, `Columns`, `Hierarchies`, `Relationships`, `Roles`, `Perspectives`, `Cultures`）以及表范围容器（`Sales/Measures`, `Sales/Columns`, …） 均受支持。

`te ls` 支持：

- `--type <kind>` - 限定为一种对象类型（`table`, `measure`, `column`, `hierarchy`, `partition`, `relationship`, `role`, `perspective`, `culture`）。 如果不提供 `<path-filter>`，这等同于输入匹配的容器关键字。
- `--paths-only` - 每行输出一个对象路径，适合通过管道传给 `xargs`、`te get` 或 `te set`。
- `--no-multiline` - 将多行单元格（通常是 DAX 或 M 表达式）折叠为单行并截断，让宽表中的各行仍便于浏览。 仅影响文本输出；JSON/CSV/TMSL 输出不受影响。
- `--output-format tmsl`（别名 `bim`）- 将匹配的对象输出为 TMSL/BIM 脚本。 例如可用于 `te ls Tables --output-format bim > tables.json`。 `ls` 不支持 `--output-format tmdl`（TMDL 仅支持单对象输出——请使用 `te get`）。

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

获取模型对象的属性。 接受一个 `<path>`。

`te get` 支持：

- `-q, --query <property>` - 获取单个属性（例如 `expression`、`formatString`）。
- `-t, --type <kind>` - 当路径匹配到表下的多个子对象时，用于消除歧义（例如同名的列和层次结构）。 可选值：`Measure`、`Column`、`CalculatedColumn`、`Hierarchy`、`Calendar`、`Partition`、`CalculationItem`。
- `--output-format tmsl`（别名 `bim`）- 将解析后的对象输出为 TMSL/BIM JSON。
- `--output-format tmdl` - 将解析后的对象输出为 TMDL（仅限命名对象）。

`te get` 和 `te ls` 共用同一个描述符目录，因此无论输出为哪种格式，属性的呈现方式都一致：文本表格、JSON 和 CSV 显示的都是同一组属性；给模型新增属性后，也会在所有格式中自动可见。

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

在模型对象中搜索文本。

`te find` 支持：

- `--in <scope>` - 与 `te replace` 相同（默认值为 `all`）。
- `--regex`、`--case-sensitive`、`--paths-only`。
- `--no-multiline` - 将多行匹配上下文折叠为单行。 仅适用于文本输出。

`--in expressions` 涵盖模型中的每个 `IExpressionObject`——包括 KPI 的 `TargetExpression` / `StatusExpression` / `TrendExpression`、度量值的 `DetailRowsExpression`、分区源/轮询的 M 表达式、表权限的 `FilterExpression`，以及计算组的 `MultipleOrEmptySelection` / `NoSelection` 表达式——因此，设置在 KPI 目标上的字面量（例如 `123`）也会像度量值正文一样被找到。

```bash
te find "CALCULATE" --in expressions
te find "Revenue" --in names
te find "CALCULATE" --in expressions --paths-only | xargs -I{} te get {} -q expression
```

### diff

比较两个模型的结构差异。 返回以下退出码：`0` 表示相同，`1` 表示发现差异，`2` 表示错误。

```bash
te diff ./model-v1 ./model-v2
te diff old.bim new.bim
```

### deps

分析对象的上游和下游依赖关系，或找出整个模型中未使用的对象。 单对象形式接受一个 `<path>`。

`te deps` 接受以下选项：

- `--unused` - 列出未被任何 DAX 引用，且未用于任何关系、层次结构级别、排序依据、变体、AlternateOf 基对象或日历时间角色的度量值、计算列以及**所有数据列**。 每条结果在文本模式下会显示 `(hidden)`，在 JSON 中则包含 `isHidden` 字段。
- `--hidden` - 将 `--unused` 限制为仅包含隐藏对象。 隐藏且未使用的对象是最安全的清理候选项，因为没有任何用户可见内容依赖它们。

```bash
te deps Sales/Revenue                     # Upstream + downstream for one object
te deps "'Sales'[Revenue]"                # DAX form is accepted everywhere a <path> is
te deps --unused                          # All unused measures and columns
te deps --unused --hidden                 # Only hidden, unused objects
```

## 分析和质量

### validate

验证模型表达式、架构完整性和 TOM 错误。

`te validate` 接受以下选项：

- `--ci <fmt>` - 将 CI 注释输出到 stderr：`vsts` 或 `github`。
- `--trx <PATH>` - 将结果写入 VSTEST `.trx` 文件。

```bash
te validate ./model
te validate --ci github --trx results.trx
```

### bpa run

针对模型运行 Best Practice Analyzer 规则。

`te bpa run` 接受以下选项：

- `<model>` - 位置参数：模型路径（可替代全局标志 `--model`）。
- `-r, --rules <rules>` - JSON 格式的 BPA 规则文件(s)的路径(s)或 URL(s)。 可重复指定。 替换本次调用的用户规则层：请参阅下文的 [规则源和解析](#rule-sources-and-resolution)。
- `--no-model-rules` - 排除嵌入在模型注释中的 BPA 规则。
- `--no-defaults` - 排除内置的默认 BPA 规则。
- `--vpax <file>` - 从 `.vpax` 文件加载 VertiPaq分析器统计信息，以启用可感知 VPA 的规则。
- `--vpa-rules` - 包含内置的 VPA 感知规则（需要 `--vpax` 或预先标注的模型）。
- `--allow-external-rules` - 允许从嵌入在模型注释中的 URL 获取 BPA 规则文件。
- `--rule <id>` - 仅按 ID 运行指定规则(s)。 可重复指定。
- `--path <path-filter>` - 将分析限制为包含匹配对象的表。 支持字面名称、容器关键字和通配符（例如 `'Sales'`、`'Sa*'`、`'Sales/度量值'`、`'*/Amount'`）。
- `--fix` - 应用修复表达式，在可能的情况下自动修复违规项。
- `--save` - 应用修复后，将模型保存回原始位置。
- `--save-to <path>` - 应用修复后，将模型保存到其他路径。
- `--serialization <fmt>` - 模型序列化格式：`tmdl`、`bim`、`te-folder`。
- `--fail-on <severity>` - 失败阈值：`error`（默认）或 `warning`。 当违规项达到该阈值时，将以退出代码 `1` 退出。
- `--ci <fmt>` - 向 stderr 输出 CI 日志命令：`vsts`（Azure DevOps）、`github`（GitHub Actions）。
- `--trx <path>` - 将结果作为 VSTEST `.trx` 文件写入指定路径。
- `--no-multiline` - 将违规表中的多行单元格内容折叠为单行。 仅适用于文本输出。

```bash
te bpa run --fail-on error --ci github
te bpa run --fix --save
te bpa run --rule PERF_UNUSED_HIDDEN_COLUMN
te bpa run --path Sales            # Tables touched by the Sales filter only
te bpa run --path 'Sa*'            # Wildcard - every table starting with Sa
te bpa run --path Sales/Measures   # Path filter applied to the matched tables
```

#### 规则来源与解析

每次调用 `te bpa run` 时，都会从三个彼此独立的层级整合规则：

1. **用户规则** - 按优先级顺序，只有一个来源会生效：
   - `-r, --rules <rules>` 标志，接受文件路径或 URL (优先级最高)
   - `TE_BPA_RULES` 环境变量
   - 来自 CLI 配置 (`~/.config/te/config.json`) 的 `bpa.rules` 数组
2. **内置默认规则** - 除非传入 `--no-defaults`，或配置中的 [`bpa.builtInRules`](xref:te-cli-config#built-in-bpa-rules) 为 `false`，否则会加载。 `bpa.disabledBuiltInRuleIds` 中列出的单个内置规则会被跳过。
3. **模型嵌入规则** - 模型 `BestPracticeAnalyzer_Rules` 注释中的规则；除非传入 `--no-model-rules`，否则会加载。 除非同时传入 `--allow-external-rules` 参数，否则会跳过外部 URL 注释。

重复的规则 ID 会被去重（用户规则优先于内置规则）。 然后会移除模型 `BestPracticeAnalyzer_IgnoreRules` 注释中的规则 ID。

输出中的 `Rules loaded:` 行会列出每个提供规则的层级，例如：

```
Rules loaded: 41 from 1 file(s) from bpa.rules config + built-in defaults + model annotations
```

### bpa rules

管理 BPA 规则集——在本地规则文件或模型注释中列出、检查、初始化，以及启用或禁用规则。 内置规则是只读的。要跳过其中某一条而保留其余规则，请使用 `te bpa rules disable`（不要直接编辑内置规则集）。

子命令：

| 子命令                             | 用途                           |
| ------------------------------- | ---------------------------- |
| `add <id> [model]`              | 添加新的 BPA 规则。                 |
| [`disable`](#bpa-rules-disable) | 为当前用户禁用一条内置 BPA 规则。          |
| [`enable`](#bpa-rules-enable)   | 重新启用先前已禁用的内置 BPA 规则。         |
| `ignore <rule-id> [model]`      | 将规则添加到模型的忽略列表。               |
| [`init`](#bpa-rules-init)       | 在解析后的 PATH 下创建一个空的 BPA 规则文件。 |
| [`list`](#bpa-rules-list)       | 列出来自所有来源的 BPA 规则及其状态。        |
| `rm <rule-id> [model]`          | 删除一条 BPA 规则。                 |
| `set <rule-id> [model]`         | 更新 BPA 规则的属性。                |
| `unignore <rule-id> [model]`    | 从模型的忽略列表中移除一条规则。             |

`te bpa rules` 的所有子命令都接受以下选项：

- `--rules-file <path>` - 指定 BPA 规则 JSON 文件的 PATH。 默认使用你的 CLI 配置（`~/.config/te/config.json`）中 `bpa.rules` 的首个已存在条目，或使用 `TE_BPA_RULES` 环境变量。
- `--model-rules` - 操作嵌入在模型注释中的规则，而非文件中的规则。

> [!IMPORTANT]
> `te bpa rules set` 和 `te bpa rules rm` 会拒绝修改内置规则 ID。 如果尝试这样做，命令将以退出码 `1` 退出，并提示改用 `te bpa rules disable`。 要自定义内置规则的行为，先禁用该内置规则，再添加一个使用不同 ID 的自定义副本：
>
> ```bash
> te bpa rules disable TE3_BUILT_IN_DATE_TABLE_EXISTS
> te bpa rules add MY_DATE_TABLE_EXISTS
> ```

#### bpa rules list

列出来自所有来源的规则（内置、用户、模型）。

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

在配置的 PATH 处创建一个空的 BPA 规则文件（`[]`）。 在对尚不存在的路径执行 `te bpa rules set` / `te bpa rules rm` 之前，请先执行一次此命令。

`te bpa rules init` 接受以下选项：

- `--force` - 用 `[]` 覆盖现有文件。 如果目标文件已存在，则必须提供此选项。
- `--rules-file <path>` - 目标文件路径。 可出现在 `init` 子命令之前或之后。

路径解析（先匹配到的优先）：`--rules-file` → `TE_BPA_RULES` 环境变量 → CLI 配置中 `bpa.rules[]` 的第一项 → `./BPARules.json` (当前工作目录)。

```bash
te bpa rules init
te bpa rules init --rules-file ./MyRules.json
te bpa rules init --force
```

#### bpa rules disable

禁用单个内置 BPA 规则。 该规则 ID 会添加到 CLI 配置中的 `bpa.disabledBuiltInRuleIds`。 后续的门禁执行（deploy、save、mutation）以及 `te bpa run` 都会跳过已禁用的规则。

该命令是幂等的——对已禁用的规则再次运行 `disable` 会成功，但不会修改配置。 如果 `<rule-id>` 不是内置规则，命令会以退出代码 `1` 结束；可使用 `te bpa rules list` 查看有效的内置 ID。

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

- `--columns`, `--relationships`, `--partitions`, `--all`。
- `--export <file.vpax>` - 将 VertiPaq 统计信息导出为 `.vpax` 文件，以便离线分析。
- `--import <file.vpax>` - 加载之前导出的 `.vpax` 文件并进行离线分析。
- `--obfuscate` - 对导出的 VPAX 中的名称和表达式进行混淆处理。
- `--top <N>`、`--stats`、`--annotate`、`--save`。

```bash
te vertipaq                    # Columns by size (default)
te vertipaq --all              # Tables, columns, relationships, partitions
te vertipaq --export stats.vpax
te vertipaq --import stats.vpax  # Analyze offline
```

### format

格式化 DAX 或 M/Power Query 表达式。

`te format` 支持：

- `-e, --expression <text>` - 格式化单个内联表达式。
- `-p, --path <path>` - 格式化指定的度量值或列。
- `--lang <dax|m>` - 默认值为 `dax`。
- `--save` / `--save-to` - 持久化保存格式化后的表达式。

```bash
te format --save                                           # Format all DAX
te format -p Sales/Amount --save                           # Single measure
te format -e "SUM ( Sales[Amount] )"                       # Inline
te format --lang m --save                                  # Format M
```

## 执行

### query

针对已部署的模型执行 DAX 查询。

`te query` 支持以下选项：

- `-q, --query <dax>` - 内联查询。
- `--file <file.dax>` - 从文件读取查询。
- `--limit <N>` - 默认为 100。
- `-o, --output-file <path>` - 将结果写入文件（`.csv`、`.tsv`、`.json`、`.dax`）。
- `--trace`, `--cold`, `--plan`, `--runs <N>` - 用于性能跟踪和基准测试。
- `--no-validate` - 跳过执行前的 DAX 语义验证。

```bash
te query -q "EVALUATE TOPN(5, 'Sales')" -s my-ws -d my-model
te query --file query.dax --output-format json
```

### script

针对语义模型执行一个或多个 C# Script。 CLI 使用与 Tabular Editor 3 Desktop 相同的脚本宿主，因此能在 TE3 中运行的脚本在这里也可原样运行。

`te script` 支持以下选项：

- `-S, --script <file>` - `.cs` / `.csx` 文件（可重复指定）。
- `-e, --expression <code>` - 内联 C#（使用 `-` 表示从 stdin 读取）。
- `--save` / `--save-to` / `--serialization`。
- `--dry-run`, `--timeout <seconds>`。

```bash
te script --script fix.cs --save
te script -e "Info(Model.Tables.Count)"
echo "Info(Model.Name);" | te script -e -
```

> [!IMPORTANT]
> 如果你要迁移旧脚本，需要了解以下两个行为差异：
>
> - **CLI 脚本中不支持交互式选择。** 从 `te script` 调用 TE3 Desktop 辅助方法 `SelectMeasure()`, `SelectTable()`, `SelectColumn()`, `SelectObject()`, 和 `SelectObjects()` 时，会抛出 `NotSupportedException`，因为 CLI 没有可弹出的 UI。 在脚本外预先解析对象(s) 并将其传入；如果脚本需要与 TE3 共享，请将该调用包裹在 `try/catch` 中。
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

通过宏 JSON 文件（通常为 `MacroActions.json`）管理和运行宏。 宏文件的 PATH 按以下顺序解析：`--macros <path>` → 环境变量 `TE_MACROS_PATH` → CLI 配置中的 `macros` → `./MacroActions.json`。

子命令：

| 子命令                                | 用途                  |
| ---------------------------------- | ------------------- |
| `list`                             | 列出宏。                |
| 宏：[`run <name-or-id>`](#macro-run) | 运行宏。                |
| `add <name>`                       | 添加宏。                |
| `set <name-or-id>`                 | 更新宏属性。              |
| `rm <name-or-id>`                  | 删除宏。                |
| `sort`                             | 排序并重新分配 ID。         |
| 宏：[`init`](#macro-init)            | 在解析得到的路径处创建一个空的宏文件。 |

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
- `--save` / `--save-to` - 将宏所做的所有更改持久化保存。

```bash
te macro run "Hide all measures"
te macro run "Format DAX" --on Sales/Revenue --save
te macro run "Format DAX" --on "'Net Sales'[Sales Amount]" --save   # DAX form works in --on too
```

## 部署和刷新

### deploy

将语义模型部署到 Power BI、Fabric 或 Azure Analysis Services。

`te deploy` 支持以下参数：

- `-s, --server` / `-d, --database` - 目标 Workspace 和模型。
- `--deploy-full` - 覆盖现有内容，并同时部署连接、分区、共享表达式、角色及角色成员。
- `--deploy-connections`
- `--deploy-partitions`
- `--skip-refresh-policy`
- `--deploy-roles`
- `--deploy-role-members`
- `--deploy-shared-expressions`
- `--create-only`
- `--xmla <file>` - 生成 XMLA/TMSL 脚本，而不是部署（`-` 表示输出到标准输出）。
- `--skip-bpa` - 完全跳过 BPA 门控检查。
- `--fix-bpa` - 如果规则定义了修复表达式，则自动修复 BPA 违规项。
- `--bpa-rules <PATH>` - 可重复指定；仅针对本次部署覆盖 CLI 配置中的 `bpa.rules`。 除非 `bpa.builtInRules` 为 `false`，否则内置规则仍会生效。
- `--force` - 跳过交互式确认（CI 必需）。
- `--ci <fmt>` - `vsts` 或 `github`。
- `--profile <name>` - 一次性使用已保存的 @te-cli-auth 配置文件。

```bash
te deploy ./model -s my-workspace -d my-model --force --ci github
te deploy ./model --xmla script.tmsl    # Generate TMSL only
te deploy ./model --profile staging --force
```

> [!IMPORTANT]
> `te deploy` 会在执行前运行 Best Practice Analyzer 作为门控检查。 在交互模式下，会显示摘要和确认提示，且 **默认安全选项为 `n`**。 在 CI 中，传入 `--force` 可跳过该提示。 BPA 门控配置请参见 @te-cli-config。

### refresh

在已部署的模型上触发数据刷新。

`te refresh` 支持：

- `--type <type>` - `full`、`dataonly`、`automatic`、`calculate`、`clearvalues`、`defragment`、`add`（默认值：`automatic`）。
- `--table <name>` - 刷新特定表(可为多个)；可重复指定。
- `--partition <Table.Partition>` - 刷新特定分区(可为多个)。
- `--apply-refresh-policy` - 应用增量刷新的刷新策略，以确定要刷新的分区。
- `--effective-date <yyyy-MM-dd>` - 设置刷新策略使用的生效日期。
- `--max-parallelism <N>` - 设置可并行刷新的最大分区数。
- `--dry-run` - 输出 TMSL 脚本而不执行。
- `--no-progress`, `--trace [path]`。

```bash
te refresh --type full                                 # Full refresh
te refresh --table Sales --type full                    # Single table
te refresh --type full --dry-run > refresh.tmsl         # Emit TMSL only
```

### incremental-refresh

管理表的增量刷新策略。

```bash
te incremental-refresh show <table>
```

其他子命令（`set`、`remove`、`apply`）可通过 `te incremental-refresh --help` 查看说明。

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

### test init / spec / use / list / snapshot / compare

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
te connect                         # Show current active connection
te connect my-workspace my-model   # Remote
te connect ./model                 # Local
te connect --local                 # Power BI Desktop (Windows)
te connect --profile prod          # Activate a saved profile
te connect --clear                 # Clear the active connection (and any workspace mirror)
```

#### 工作区模式（`-w` / `--workspace`）

将主源与次要目标配对，使后续每次执行 `--save` 都会在两者之间同步镜像模型。 适合保留远程 Workspace 的本地工作副本，或在保存时将本地修改推送到 Workspace。

- `te connect <ws> <model> -w ./src` - 主源为远程；`./src` 会接收初始 TMDL 导出，并在每次保存时保持镜像同步。
- `te connect ./src -w <ws> <model>` - 主源为本地；首次部署会将模型推送到 Workspace，后续保存会自动重新部署。
- `--workspace-format <bim|tmdl>` - 在镜像到文件夹/文件时选择磁盘上的格式（例如，`-w ./model.bim` 会推断为 BIM）。
- `--force` - 当目标已存在（例如文件夹非空或数据库已存在）时必须使用。 如果不使用它，`te connect` 会显示交互式 `y/n` 提示，并以 `n` 作为安全的默认选项。

启用后，`te set --save`、`te rm --save`、`te script --save` 等都会透明地同时保存到本地和远程。 保存顺序始终是 **先本地，后远程**，因此即使推送到服务器失败，磁盘上的副本也会反映最新的用户更改。 使用 `te connect --clear` 清除镜像。

```bash
te connect Finance "Revenue Model" -w ./revenue-model    # Mirror remote → local TMDL
te connect ./revenue-model -w Finance "Revenue Model"    # Mirror local → remote
```

### auth login / status / logout

管理缓存的身份验证信息。 参见 @te-cli-auth。

### profile list / show / set / remove

管理命名连接配置文件。 参见 @te-cli-auth。

## 配置

### config show / paths / init / set

查看和管理 CLI 配置以及 TE3 PATH 覆盖设置。 参见 @te-cli-config。

```bash
te config show                          # Display all settings
te config paths                         # Resolved TE3 file paths
te config init                          # Create default config
te config set autoFormat true
```

### license

`te license` 保留用于正式发布 GA 版，在此预览版本中不可用。 这个命令仍会被解析器识别——所以调用它的现有脚本不会在解析阶段报错——但所有子命令都会以状态 `1` 退出，并显示“此预览版本中不可用”的信息。 关于更全面的许可说明，请参见概述页面上的[预览说明](xref:te-cli#preview-notice)。

### migrate

说明旧版 Tabular Editor 2 CLI 参数如何映射到新 CLI 的参考指南。 在迁移基于 TE2 的管道时，可作为实时速查参考。 完整迁移指南参见 @te-cli-migrate。

```bash
te migrate                   # Full flag mapping table
te migrate -A                # Look up a single TE2 flag
te migrate --output-format json     # Machine-readable mapping
```

## Shell

### interactive

使用具备模型感知能力的提示词启动引导式 REPL 会话。 参见 @te-cli-interactive。

```bash
te interactive                                # Connect later
te interactive ./model                        # Start with a local model
te interactive -s MyWorkspace -d MyModel      # Start with a remote model
```

引号和 DAX 风格的引用在会话内外的用法一致——有关 REPL 中支持括号感知的 argv 拆分的详细信息，请参见上文的[对象路径](#object-paths)一节以及 @te-cli-interactive。

### completion

生成 shell 补全脚本。 参见 @te-cli-install。

```bash
te completion bash
te completion zsh
te completion pwsh
```

## 退出代码

| 退出代码 | 含义                                                      |
| ---- | ------------------------------------------------------- |
| `0`  | 成功。                                                     |
| `1`  | 通用失败（参数无效、命令执行失败、校验错误、身份验证失败、BPA 门禁在严重级别 ≥ error 时未通过）。 |
| `2`  | 差异非零（`te diff`）——模型不一致。                                 |

如需在 CI 管道中进行更细致的控制，可将退出代码与 `--ci <vsts/github>` 注释以及 `--trx` 结果文件结合使用——参见 @te-cli-cicd。

## 相关页面

- @te-cli - 概览和背景说明。
- @te-cli-install - 安装并设置 CLI。
- @te-cli-auth - 进行身份验证并管理连接。
- @te-cli-config - 配置文件、BPA 门禁和变更后行为。
- @te-cli-migrate - TE2 → TE3 标志映射。
