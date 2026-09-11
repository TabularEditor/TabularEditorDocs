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

- **`<path>`** - 解析为**恰好一个**对象或容器。 供更改模型或需要单个目标的命令使用：`te set`、`te add`、`te remove`、`te move`、`te deps`、`te macro run --on`，以及带 `-p`、`--deps` 或 `--properties` 的 `te get`。
- **`<path-filter>`** - 解析为**零个或多个**对象，并支持通配符。 供处理一组对象的命令使用：`te list`、普通 `te get`（通配符或容器路径会列出所有匹配项）、`te bpa run --path`，以及其他检查类命令。

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

路径中的保留字符包括 `/ [ ] ' \" * ?？ { }`。 任何包含 `* ? 的分段？ { }` 的分段必须加引号（`te get "Tables/'{foo}'"`、`te get 'Sales/"my*name"'`）；未加引号会被拒绝并报错，错误会指出该字符并展示加引号后的写法。 `?` 为保留字符，不表示通配符。 CLI 输出的每个路径——无论是在错误、提示、`--paths-only` 输出，还是 JSON 的 `objectPath` 字段中——都会以规范化的加引号形式输出，可直接粘贴回 `te get`。 混合引号形式需要 PowerShell 或 bash；cmd.exe 无法表示。

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
| `Tables`, `度量值`, `Columns`, `Hierarchies`, `分区`, `KPI`, `Sets`                                                        | 模型   | 模型中该类型的所有对象。 |
| `关系`, `角色`, `Perspectives`, `Cultures`, `DataSources`, `Expressions`, `CalculationGroups`, `Functions`, `Annotations` | 模型   | 模型级容器。       |
| `度量值`, `Columns`, `Hierarchies`, `分区`, `Calendars`, `CalculationItems`, `KPI`, `Sets`                                 | 表    | 表下的子容器。      |
| `Levels`                                                                                                              | 层次结构 | 层次结构的级别。     |
| `Members`, `TablePermissions`（别名 `Permissions`）                                                                       | 角色   | 角色的子级对象。     |

计算集只能以容器形式寻址（`<table>/Sets/<name>`）；单个 KPI 为 `<table>/<measure>/KPI`；日历可通过 `<table>/Calendars/<name>` 解析；关系可通过 `Relationships/<name>` 解析（即该关系在模型中的名称：GUID，或类似 `Relationship 1` 的标签；`--paths-only` 会输出它，同时也接受显示名称）。

以下示例展示普通路径与限定容器范围的路径之间的区别：

```bash
te get Sales/Revenue                       # Measure or column on Sales
te get Sales/Measures/Revenue              # Same, container-scoped - disambiguates if other kinds share the name
te get Sales/Geography/Levels/Year         # Specific level of a hierarchy
te get Roles/Admin/Members/bob@example.com # Role member
te get Sales/refreshPolicy                 # Refresh-policy sub-object on a table
te get Sales/Revenue/KPI                   # KPI sub-object of a measure
```

当实际对象名称恰好与关键字同名时，可为该分段加上引号，以强制进行字面名称匹配。 字面名称为 `Tables` 的表需要写作 `'Tables'`，可通过 `te get "'Tables'"` 访问。 名称为 `KPIs` 或 `Sets` 的表也是如此。

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

分段拼写错误时会给出一条与上下文相关的错误；如果 CLI 能猜到你的意图，还会附带“你是不是想输入……”的提示。 列表会提供表、度量值、列和层次结构，每项都以完整的 `Table/Object` 路径形式给出，可直接粘贴到下一条命令中。 用单引号写出的名称会被视为表引用（`te deps 'Revenue'` 会查找名为 Revenue 的表）；如果目标不是表，错误信息会提示使用 `Table/Object` 和 `"[Object]"` 这两种形式。 缺少父级的路径会在检查叶节点之前失败，因此信息会指向真正出错的分段。 错误或提示中输出的每个路径都取自你的模型，并已正确加引号，按原样即可解析——被拒绝时绝不会建议一个不存在的路径。 空容器（例如在没有层次结构的模型上运行 `te list Hierarchies`）不会报错，而是给出简单的“这里没有内容”提示。

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
| `--local`                  | 连接到本地运行的 Analysis Services 实例——Power BI Desktop、Visual Studio Workspace，或独立 SSAS（仅限 Windows）。                                                                                                                                                                                                                                                                                                                                          |
| `--auth <method>`          | 身份验证方法：`auto`、`interactive`、`spn`、`env`、`managed-identity`（默认值：`auto`）。                                                                                                                                                                                                                                                                                                                                                                |
| `--output-format <format>` | 标准输出格式：`text` (默认)、`json`、`csv`、`tmsl` (别名 `bim`)、`tmdl`。 输出表格数据的命令会识别 `csv`；`tmsl`/`tmdl` 仅由 `te get` 和 `te list` 用于整个对象的序列化。 命令会拒绝其不支持的格式。                                                                                                                                                                                                                                                     |
| `--error-format <format>`  | 用于错误、警告和提示的 stderr 格式：`text`（默认）或 `json`。 其他值将回退为 `text`。 它独立于 `--output-format`，因此你可以将 JSON 格式的 stdout 与纯文本错误配合使用（反之亦然）。                                                                                                                                                                                                                                                                                                              |
| `--recent [N]`             | 使用最近使用过的模型。 未提供值 = 进入交互式选择器；`N` = 最近使用列表中的第 N 个（1 = 最近一次使用）。                                                                                                                                                                                                                                                                                                                                                                           |
| `--non-interactive`        | 禁用所有交互式提示。 如果缺少必需输入，将给出可操作的错误提示并失败退出。                                                                                                                                                                                                                                                                                                                                                                                                  |
| `--debug`                  | 启用调试日志并输出到 stderr（连接字符串、身份验证流程、耗时）。                                                                                                                                                                                                                                                                                                                                                                                                    |

`te --version` 会打印 CLI 版本并退出。

对于读取模型的命令，解析顺序如下：

`--recent` → `--local` → `--server`/`--database`（远程）→ `--model` → 来自 `te connect` 的活动连接。

模型绝不是位置参数——命令行中多写一个路径会被拒绝，并报出“无法识别的命令或参数”错误。 （`te connect`、`te init`、`te diff` 和 `te query` 中的位置参数是这些命令各自的操作对象，不是模型。）

> [!NOTE]
> **拼写错误的选项会被立即拒绝。** 如果你传入了当前命令无法识别的 `--flag`，CLI 会直接退出并给出可操作的错误信息，而不是悄悄把该标记当作位置参数吞掉。 这可以捕获 CI 脚本中把 `--force ` 误写成 `--forec` 之类的拼写错误。

> [!NOTE]
> **带点号的服务器名称。** `-s`/`--server` 会将带点号的名称（例如 `Sales.2026`）视为 Analysis Services 服务器主机名，而不是 Power BI Workspace。 当 CLI 需要这样判断时，会发出警告，并提示：如果你指的是 Power BI Workspace，请在末尾追加 `.Workspace`（例如 `Sales.2026.Workspace`），或使用完整的 `powerbi://` URL。 适用于 `te connect`、`te deploy`、`te refresh`、`te query`、`te vertipaq` 和 `te test run`。

## 模型初始化与保存

### save-as

将模型重新序列化为其他格式，或保存到其他位置。 可用于将远程 Workspace 中的模型写入本地文件、转换格式，或将编辑内容保存回源位置。 （别名：`save`。）

`te save-as` 接受：

- `-o, --output-path <path>` - 目标文件或文件夹。 **可选**：省略时，`te save-as` 会写回源位置，并保留原始格式。
- `--serialization <fmt>` - `tmdl`、`bim`（别名 `tmsl`）、`database.json`、`pbip`。 省略时，格式默认为已加载模型的格式；使用 `-o` 时，会根据输出路径推断格式（`.bim` 会输出为单文件 BIM，`.json` 会输出为包含 `Database.json` 的文件夹）。
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

使用 `--serialization pbip` 输出的内容可直接在 Power BI Desktop 中打开，且会以源模型命名（`SpaceParts.pbip`，而不是 `Model.pbip`）。 保存到已包含项目的文件夹时，只会补充缺失的文件，已存在的所有内容——Report 的页面、主题、连接以及项目标识——都会原样保留。因此，如果一次保存没有任何改动，在版本控制下项目也不会产生变化。

验证会保护保存操作：如果模型存在 Analysis Services 会拒绝的名称冲突（`TE0012` / `TE0013`，参见 [validate](#validate)），则不会写入，除非传入 `--force` 或 `--skip-validation`。

> [!TIP]
> 使用 `te save-as -o <path> -s <Workspace> -d <model>` 可将远程模型下载到磁盘。 如果你只需要原始字节数据（不做 DAX 语义分析），配合 `--skip-validation` 可实现最快的直通下载。

### init

在指定路径创建一个新的空语义模型。 默认为 `PowerBI` 兼容模式下、兼容级别为 1705 的 TMDL 模型。

`te init` 接受以下参数：

- `<output-path>` - 位置参数：用于创建模型的目录（省略时使用全局 `--model` 路径）。
- `--compatibility-mode <mode>` - `PowerBI`（默认）或 `AnalysisServices`。
- `--compatibility-level <N>`（别名 `--compat`）- 兼容级别。 模式为 `PowerBI` 时默认值为 `1705`，否则为 `1500`。 参见 @update-compatibility-level。
- `--name <name>` - 模型/数据库名称（默认：目录名称）。
- `--serialization <fmt>` - `tmdl`（默认）、`bim`（别名 `tmsl`）、`database.json`、`pbip`。
- `--force` - 覆盖目标路径下任何现有文件或目录。

```bash
te init ./new-model                                       # TMDL, PowerBI mode, compat 1705
te init ./new-model --serialization bim                   # Single-file BIM model
te init ./as-model --compatibility-mode AnalysisServices  # AS model, compat 1500
te init ./existing-dir --force                            # Overwrite non-empty directory
```

`te init` 具有幂等性：在它已经创建过的模型上再次运行时，会输出 `Already exists` 并以退出码 `0` 结束（使用 `--output-format json` 时：`{"created": false, "reason": "already_exists", ...}`）。 真正的冲突仍会以 `1` 退出；`--force` 会从头重新创建。

## 模型编辑

会修改内容的命令（`set`、`add`、`remove`、`move`，以及 `script`、`macro run`、`bpa run --fix`）**默认以干运行方式执行**：不带 `--save` 时，命令会报告将会发生哪些更改，并丢弃这些更改（`Dry run - nothing saved.`）。 Add --save to persist.`）。 添加 `--save`以保存到源位置，或使用`--save-to <path>`写入其他位置。 对于`set`、`add`、`remove`、`move`、`script`和`bpa run`，更改输出会按每个发生更改的对象，以统一 diff 的形式呈现；可用 `--stat`或`--name-only`切换（与默认的`--diff`互斥），也可通过`te config set mutationOutput diff|stat|name-only|none`设置长期默认值。 JSON 输出始终包含完整的 changes 数组。 如果变更引入了新的 DAX 验证错误，则会拒绝保存，除非使用`--force\`。

### set

设置模型对象的属性、格式化其表达式，或将表与其源架构同步。 接受 `<path>` 参数。

`te set` 接受以下参数：

- `-p, --property <Name=Value>` - 属性赋值（例如 `-p expression="SUM(Sales[Amt])"`、`-p isHidden=true`）。 **可重复**：第一个 `=` 之后的所有内容都会被视为值。 也支持直接使用位置赋值：`te set Sales/Amount formatString="#,0" --save`。 属性名不区分大小写；当网格标签与 TOM 名称不一致时，两种拼写都可接受（`Hidden` 和 `IsHidden`）；也支持点路径和索引器：`-p KPI.StatusGraphic=...`、`-p "Annotations[Tabular Editor]=..."`、`-p "TranslatedNames[fr-FR]=..."`。 运行 `te get <path> --properties` 以列出对象接受的所有名称；参见 [get](#get)。 无论分区是哪种类型，其表达式都用 `-p Expression` 表示（`MExpression` 和 `Query` 仍然可用）。 使用 `-p Name=-` 从 stdin 读取值（每个流只能赋值一次；通过管道传入的值会按原样使用，因此管道传入文本 `null` 时，存储的是单词 `null`）。 `-p Name=` 会赋值为空字符串。
- `--unset <Name>` - 清除某个属性；可重复使用（`--unset description --unset displayFolder`）。 `-p Name=null` 是简写。 适用于所有可以为空的属性(包括文本属性)，也适用于对象值属性(`SortByColumn`、`RefreshPolicy`); `-p "Annotations[key]=null"` 会移除一个注解。 数值、布尔值以及固定选项属性无法清空，尝试清空会被拒绝。
- `--format <PropertyName>` - 格式化该表达式属性（可重复使用；会根据属性自动检测 DAX 或 M）。 格式化器会调整 `--long`（减少换行）的行为；而 `--no-space-after-function` 需要在 DAX 属性上配合 `--format` 使用。 `--semicolons` 不能与 `--format` 一起使用：存储在模型中的表达式始终使用逗号分隔，因此分号方言永远无法解析它；如需格式化以分号编写的 DAX，请改用 [`te util format-dax --semicolons`](#util-format-dax)。
- `--update-schema` - 将表的列与其源架构同步：为源中新增加的列按检测到的类型创建列，对类型发生偏移的列重新设定类型，并保留每个现有列的其他所有信息（名称、说明、格式字符串、显示文件夹、排序依据列、可见性、注解、翻译、透视成员资格）。 已删除的源列默认只会发出警告，除非使用 `--drop-removed-columns`（破坏性操作）。 重命名后的源列会被视为“删除 + 新增”；请先用 `-p SourceColumn=<newName>` 重新映射它。 计算表格和计算组不支持此操作；也不能与 `-p` 或 `--format` 组合使用。 在未指定任何连接标志时，会从模型本身读取连接信息——即表分区绑定的数据源、写在表自身查询中的连接，或模型中唯一可用的数据源——而源表则取自分区绑定，找不到时回退到模型表名；当模型有多个可用源时，可用 `--data-source <name>` 进行选择。 使用与 `te add` 共享的架构检测标志(`--source sql|lakehouse|warehouse`, `--endpoint`, `--connection-string`, `--source-database`, `--source-table`)显式命名连接时，总是以该显式命名为准。 当无法推断源，或找不到源表时，错误信息会说明属于哪种情况，并指出它尝试查找的表名。
- `-t, --type <kind>` - 用于在同一路径可能解析为多种对象类型时消除歧义（`度量值`、`Column`、`CalculatedColumn`、`Hierarchy`、`Calendar`、`分区`、`CalculationItem`）。
- `--save` / `--save-to <path>` - 保存更改。
- `--diff` / `--stat` / `--name-only` - 更改输出的呈现方式（参见上面的说明）。
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

#### 增量刷新策略

刷新策略就是表的 `RefreshPolicy` 子对象上的普通属性，因此 `te get` 和 `te set` 可以像处理其他任何属性一样管理它们。 属性名：`Mode`、`RollingWindowPeriods`/`RollingWindowGranularity`、`IncrementalPeriods`/`IncrementalGranularity`、`IncrementalPeriodsOffset`、`SourceExpression`、`PollingExpression`（文件输入：`-p SourceExpression=- < src.m`）。

```bash
te get Sales/RefreshPolicy                                              # Inspect a table's refresh policy
te set Sales/RefreshPolicy -p RollingWindowPeriods=5 -p RollingWindowGranularity=Day -p IncrementalPeriods=1 -p IncrementalGranularity=Day --save
te set Sales -p RefreshPolicy=null --save                               # Remove the policy
```

首次执行 `set` 时会隐式创建该策略。 移除策略后，策略生成的分区会保留；如果它们是该表仅有的分区，则会拒绝移除。 要在服务器上应用该策略，请参见 [`te refresh --apply-refresh-policy`](#refresh)；如果只想将其应用到元数据，请使用 `te script --inline "Model.Tables[\"Sales\"].ApplyRefreshPolicy();" --save`。

### add

向模型添加对象。 为新对象传入 `<path>`（父级必须已存在；最后一个分段就是新名称），并通过 `-t` / `--type` 指定类型。 关系仍使用其简写语法（`Sales[Key]->Dim[Key]`）。 容器形式的路径可作为有效的添加目标（`Sales/Measures/Margin`、`Sales/Partitions/Q1`、`Sales/Calendars/Fiscal`、`Roles/Admin/TablePermissions/Sales`、`Roles/Admin/Members/user@x.com`）——CLI 输出的任何路径都可以直接再次用于 `te add`。

`te add` 支持以下选项：

- `-t, --type <type>` - 指定对象类型。 常见值：`Table`、`CalculatedTable`、`CalcGroup`、`Measure`、`CalculatedColumn`、`DataColumn`、`Hierarchy`、`Level`、`Calendar`、`CalcItem`、`KPI`、`Partition`、`Expression`、`Function`、`Perspective`、`Culture`、`Role`、`TablePermission`、`Member`。 支持 Tab 自动补全；可通过运行 `te add --help` 获取完整列表。
- `-p, --property <Name=Value>` - 对新对象进行属性赋值（可重复指定）。 表达式可以放在 `-p Expression="..."` 中，也可以使用 `--file`，或者用 `-p Expression=-` 从 stdin 读取。
- `--file <path>` - 从文件读取表达式，而不是内联提供。
- `--mode <mode>` - 新表的存储模式：`import`（默认）、`directquery`（别名 `dq`）、`dual`、`directlake`（别名 `dl`）。
- `--if-not-exists` - 如果对象已存在，则直接以 `0` 退出且不报错。 可用于幂等的 CI/CD 管道。
- `--save` / `--save-to <path>` - 保存更改。
- `--diff` / `--stat` / `--name-only` - 变更输出的呈现方式（参见 [模型编辑](#model-editing) 说明）。
- `--serialization <fmt>` - 保存时覆盖序列化格式（`tmdl`、`bim`（别名 `tmsl`）、`database.json`、`pbip`）。
- `--source-type <kind>` - 新表的初始分区源类型：`m`、`query` 或 `calculated`。 这会覆盖启发式检测结果。 `query` 会生成一个旧式 SQL `SELECT` 分区，并绑定到模型的 Provider数据源；在使用 Lakehouse/Warehouse 源，或不存在 Provider数据源时会被拒绝。`calculated` 仅在 `-t CalculatedTable` 下有效。
- `--partition-expression <m>` - 新表初始分区的原始 M 表达式。
- `--force` - 即使修改引入 DAX 验证错误，也会保存。

向现有表添加单个数据列时，请使用 `-t DataColumn`，且必须同时提供 `SourceColumn` 和 `DataType`（在计算表格和计算组上会被拒绝）：

```bash
te add Sales/Quantity -t DataColumn -p SourceColumn=Qty -p DataType=Int64 --save
```

表可以直接从模型**自身**的数据源一次性创建，无需任何连接参数。 CLI 会从模型的数据源读取连接信息，发现源表的列及其类型，并创建该表，同时生成一个已绑定到该源的分区。 在旧式（Provider）数据源上，分区会是一个包含生成的 `SELECT` 的旧式 SQL 查询，与桌面版 **导入表** 向导写入的内容一致；如需改用 Power Query (M) 分区，请传入 `--source-type m`。 在结构化（Power Query）数据源上，分区始终为 M。拒绝时不会创建任何内容，常见原因包括：模型中有多个可用数据源但未提供 `--data-source`；没有 CLI 可读取的数据源（支持 SQL Server、Azure SQL 和 Fabric SQL 源）；数据源的密码未存储在模型中；或连接找不到源表——错误会指出它查找的表名以及该名称的来源。

- `--source-table <schema.table>` - 从此源表创建该表。
- `--query "SELECT ..."` - 改为通过查询创建表：系统会基于该连接分析该查询而不执行它，新表会获得它返回的全部且仅有的列，并将该查询保留为分区内容。 既适用于推断出的连接，也适用于显式命名的连接。 `--source-type query` 会把 SQL 放到一个旧式 Query 分区中，该分区绑定到模型的旧式数据源。 不能与 `--mode directlake`（Direct Lake 分区不保存查询）、`--columns` 以及其自身的表达式（`-p Expression=` 或 `--file`）同时使用。
- `--data-source "<name>"` - 当模型有多个数据源时，用于消除歧义。

也支持针对显式指定的源进行架构检测，而且始终优先于推断：`--source sql|lakehouse|warehouse`、`--endpoint`、`--connection-string`、`--source-database`、`--source-table`，或手动列规范 `--columns "Id:Int64,Name:String"`。 完全不指定源时，`te add "<table>" -t Table` 仍会创建一个空表，供你自行填充。

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
- `--diff` / `--stat` / `--name-only` - 变更输出的呈现方式（参见 [模型编辑](#model-editing) 说明）。
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
- `--diff` / `--stat` / `--name-only` - 变更输出的呈现方式（参见 [模型编辑](#model-editing) 说明）。
- `--serialization <fmt>` - 保存时覆盖序列化格式（`tmdl`、`bim`（别名 `tmsl`）、`database.json`）。
- `--force` - 即使该变更会引入 DAX 验证错误，也仍会保存。

如果尝试重命名名称不由你设置的对象，将会被拒绝并以非零退出代码退出，而不是提示 `No changes.`——例如：关系（其名称始终描述它连接的列）、度量值的 KPI、角色的表格权限。

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

- `--type <kind>` - 限定为一种对象类型（`table`, `measure`, `column`, `hierarchy`, `partition`, `relationship`, `role`, `perspective`, `culture`, `calculationitem`, `kpi`, `set`, `function`）。 如果不提供 `<path-filter>`，这等同于输入匹配的容器关键字。
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

在 JSON 输出中，每个列出的对象都以其 `objectPath` 开头——这是一个可由 `te get` 直接解析的规范路径。

### get

获取模型对象的属性、筛选并列出对象集，以及分析依赖关系——`get` 是 CLI 统一的读取管道（`te list` 和 `te deps` 仍保留为快捷方式）。 接受一个 `<path>`；省略它即可列出模型（与 `te list` 相同），或者传入 `.` 表示模型根节点。 通配符路径（`te get "Sa*"`）或容器路径（`te get Sales/Measures`）会列出所有匹配项，无需 `--ls`；`-p`、`--deps` 和 `--properties` 都要求恰好对应一个对象，因此在通配符路径上会明确提示这一点，并建议去掉该标志。

`te get` 支持：

- `-p, --property <property>` - 仅输出单个属性（例如 `expression`、`formatString`）。
- `--where <Prop=Value>` - 筛选结果集；可重复使用（AND），不区分大小写。 不含 `*` 的值表示精确匹配；`*` 是通配符，因此包含搜索可写为 `--where Name=*margin*`。 不带路径时，`--where` 会筛选模型的 **顶级表**；传入容器可搜索其他类型（`te get Measures --where Name=*margin*`）。 空结果会说明搜索了什么、模式是如何匹配的，并提供扩大搜索范围的命令。
- `--properties` - 列出已解析对象上 `-p` 可接受的属性名，以及每个属性的类型、是否可写、其内容，以及——当某个属性只接受固定值集合时——它可接受的值。 在两种写法不同时，会同时显示两者（`Hidden` / `IsHidden`）；注释和翻译会按它们必须书写的方括号形式显示。 内部用途的属性默认省略；使用 `--all` 可将其包含在内。 仅支持文本和 JSON 输出；需要单对象路径，且不能与 `-p`、`--ls`、`--where`、`--deps` 或 `--unused` 组合使用。
- `--ls` - 紧凑表格布局（与 `te list` 的渲染方式相同）。
- `--deps [upstream|downstream]` - 依赖关系分析（默认：双向）；`--deep` 用于递归树，`--max-depth <N>`（默认 `10`）。
- `--unused` / `--hidden` - 像在 `te deps` 中一样，显示未使用或隐藏的对象。
- `--paths-only` - 每行输出一个规范对象路径，便于管道传递。
- `--no-multiline` - 将多行单元格折叠为单行（与 `--ls`/`--where` 一起使用）。 仅适用于文本输出。
- `-t, --type <kind>` - 当路径匹配到表下的多个子对象时，用于消除歧义（例如同名的列和层次结构）。 可选值：`Measure`、`Column`、`CalculatedColumn`、`Hierarchy`、`Calendar`、`Partition`、`CalculationItem`。
- `--output-format tmsl`（别名 `bim`）- 将解析后的对象输出为 TMSL/BIM JSON。
- `--output-format tmdl` - 将解析后的对象输出为 TMDL（仅限命名对象）。

`te get` 和 `te list` 共用同一个描述符目录，因此无论输出为哪种格式，属性的呈现方式都一致：文本表格、JSON 和 CSV 显示的都是同一组属性；给模型新增属性后，也会在所有格式中自动可见。

在 `te get <path>` 结果下方的 `Settable:` 行会列出 `te set` 可在该对象上接受的属性（其中包括 `SortByColumn`），并在末尾提示使用 `--properties` 查看完整列表；如果在 `te get -p` 或 `te set -p` 中使用未知属性名，也会指向同一列表。 `te get -p` 会对每个值为表达式的属性进行语法高亮，包括明细行和格式字符串表达式。 在 JSON 输出中，单个对象以 `objectPath` 开头（这是规范路径，可直接由 `te get`、`te set` 或 `te remove` 解析），后跟 `type` 和 `properties`；如果列表没有匹配项，则输出空数组。

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

在字符串属性中搜索文本，并报告每处匹配的位置。 默认情况下，模式是**按字面匹配且不区分大小写的子字符串**——`te find "Gross*"` 会查找字面的星号——因此如需模式匹配，请传入 `--regex`。 需要按属性值筛选对象而不是搜索文本时，请使用 `te get --where Name=*Gross*`。 当结果为空时，会说明所搜索的范围和使用的匹配模式，并提供可扩大搜索范围的命令；如果 `--regex` 模式不是有效的正则表达式，则会被拒绝，并报错指明该参数及其模式。

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

在 `--output-format json` 下，`te find` 会在输出匹配结果的同时，报告其搜索范围以及所用的匹配模式。

### diff

比较两个模型的结构差异。 返回以下退出码：`0` 表示相同，`1` 表示发现差异，`2` 表示错误。

变更的报告方式与会修改内容的命令相同：每个已变更对象对应一条汇总条目，文本输出中每个属性各有 `-`/`+` 行。 在 JSON 中，`changes` 数组的条目包含 `objectPath` (规范路径，可通过管道传给 `te get`)、`objectType` (与 findings JSON 相同的固定枚举值 - `KPI`、`Member`、...)、`changeKind` (`created`、`deleted`、`modified` 或 `moved` - 带有 Lineage tag 的重命名对象会作为单个 `moved` 条目呈现，并包含 `movedFromObjectPath`)，以及一个 `properties` 数组，其元素为使用 PascalCase 属性名的 `{property, before, after}`。 仅存在于两个模型之一中的对象会连同其内容一并列出：例如新角色的行级安全性筛选器、新表的列、度量值和分区、新层次结构的级别——每一项都会作为单独条目列出，汇总计数也会将其计入。

```bash
te diff ./model-v1 ./model-v2
te diff old.bim new.bim

# Branch on exit code (POSIX sh):
te diff ./a ./b; case $? in 0) echo same;; 1) echo different;; *) echo error;; esac

# Branch on exit code (PowerShell):
te diff ./a ./b; switch ($LASTEXITCODE) { 0 { 'same' } 1 { 'different' } default { 'error' } }
```

### deps

分析对象的上游和下游依赖关系，或找出整个模型中未使用的对象。 这是 `te get --deps` / `te get --unused` 的快捷方式。 单对象形式接受一个 `<path>`。

`te deps` 接受以下选项：

- `--upstream` - 仅显示上游依赖项（即此对象所使用的对象）。
- `--downstream` - 仅显示下游依赖项（即使用此对象的对象）。
- `--deep` - 显示递归依赖树，而不只显示直接依赖关系。
- `--max-depth <N>` - `--deep` 遍历的最大深度（默认：`10`）。
- `-t, --type <kind>` - 当路径匹配到表下的多个子对象时，用于消除歧义（例如同名的列和层次结构）。
- `--unused` - 列出未被任何 DAX 引用，且未用于任何关系、层次结构级别、排序依据、变体、AlternateOf 基对象或日历时间角色的度量值、计算列以及**所有数据列**。 每条结果在文本模式下会显示 `(hidden)`，在 JSON 中则包含 `isHidden` 字段。
- `--hidden` - 将 `--unused` 限制为仅包含隐藏对象。 隐藏且未使用的对象是最安全的清理候选项，因为没有任何用户可见内容依赖它们。

在 JSON 输出中，每个条目——以及每个 `upstream`、`downstream` 和 `--deep` 树节点——的命名方式都与 CLI 其余部分一致：`objectPath`（规范路径，可通过管道传给 `te get`）、`object`（不含路径的名称）和 `objectType`。

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

- `--ci <fmt>` - 向 stderr 输出 CI 注解：`vsts`（别名 `azdo`、`azure-devops`）或 `github`（别名 `gh`）。 `none` 或空值表示不输出注解；任何其他值都会在命令运行前被拒绝。
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

每条发现项都有一个稳定的代码，会显示在“错误”“警告”和“反模式”表的 **Code** 列中，也会出现在 JSON、`--ci` 注解和 `--trx` 中。 当涉及手工编写的模型时，有三个代码值得了解：`TE0012`（同一表中的某列与某个度量值同名，或两列同名）和 `TE0013`（度量值名称跨表重复）都属于错误——Analysis Services 会拒绝加载此类模型，而 `te save-as` 也会拒绝写出此类模型，除非传入 `--force` 或 `--skip-validation`；`TE0014` 则是一个警告，表示某个 TMDL 文件夹缺少 `database.tmdl`，因此当前生效的兼容级别会替代模型所声明的兼容级别。 该文件夹仍可加载，而且对于 `TE0014`，`te validate` 仍会以 `0` 退出；可像隐藏其他警告一样，使用 `--no-warnings` 或 `--errors-only` 将其隐藏。

在 `--output-format json` 下，`te validate` 会输出共享的 findings JSON 文档（`summary` 加上扁平的 `findings[]` 数组），该格式也被 `te bpa run`、`te test run` 和 `te query` 共用——参见 @te-cli-findings。

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
- `--diff` / `--stat` / `--name-only` - 用于修复阶段的变更输出呈现方式（参见[模型编辑](#model-editing)说明）。
- `--serialization <fmt>` - 模型序列化: `tmdl`、`bim` (别名 `tmsl`)、`database.json`。
- `--fail-on <severity>` - 失败阈值：`error`（默认）或 `warning`。 当违规项达到该阈值时，将以退出代码 `1` 退出。 无论 `--fail-on` 如何设置，规则加载或求值错误（表达式无效、规则文件无法读取）也会导致命令以非零状态退出。
- `--ci <fmt>` - 向 stderr 输出 CI 日志命令：`vsts`（Azure DevOps；别名 `azdo`、`azure-devops`）、`github`（GitHub Actions；别名 `gh`）。 无法识别的值会直接被拒绝。
- `--trx <path>` - 将结果作为 VSTEST `.trx` 文件写入指定路径。
- `--no-multiline` - 将违规表中的多行单元格内容折叠为单行。 仅限文本输出。

```bash
te bpa run --fail-on error --ci github
te bpa run --fix --save
te bpa run --rule PERF_UNUSED_HIDDEN_COLUMN
te bpa run --path Sales            # Tables touched by the Sales filter only
te bpa run --path 'Sa*'            # Wildcard - every table starting with Sa
te bpa run --path Sales/Measures   # Path filter applied to the matched tables
```

在 `--output-format json` 下，`te bpa run` 会输出共享的 findings JSON 文档（见 @te-cli-findings）；使用 `--fix` 时，JSON 会是单个文档，并额外包含 `fix` 变更集。

#### 规则来源与解析

每次调用 `te bpa run` 时，都会从三个彼此独立的层级整合规则：

1. **用户规则** - 按优先级顺序，只有一个来源会生效：
   - `-r, --rules <rules>` 标志，接受文件路径或 URL (优先级最高)
   - `TE_BPA_RULES` 环境变量
   - 来自 CLI 配置 (`~/.config/te/config.json`) 的 `bpa.rules` 数组
2. **内置默认规则** - 除非传入 `--no-defaults`，或配置中的 [`bpa.builtInRules`](xref:te-cli-config#built-in-bpa-rules) 为 `false`，否则会加载。 `bpa.disabledBuiltInRuleIds` 中列出的单个内置规则会被跳过。
3. **模型嵌入规则** - 模型 `BestPracticeAnalyzer_Rules` 注释中的规则；除非传入 `--no-model-rules`，否则会加载。 除非同时传入 `--allow-external-rules` 参数，否则会跳过外部 URL 注释。

内置默认规则与 Tabular Editor 3 文档中记录的[内置规则集](xref:built-in-bpa-rules)（`TE3_BUILT_IN_*` ID）完全一致，因此 `te bpa run` 与 TE3 Desktop 对内置规则会标记哪些问题的结果一致。 此前预览版中被当作内置规则提供的六条 VertiPaq分析器规则（`VPA_*`）不属于该规则集，`--vpa-rules` 标志也已不存在；如果某个管道依赖其中某条规则作为门禁条件，请把它的定义复制到你自己的规则文件中，并通过 `--rules`、`bpa.rules` 或 `TE_BPA_RULES` 指向该文件。 `--vpax` 保持不变，仍会提供可供你自己的支持 VPA 的规则读取的统计信息。 C# Script（`te script`、`te macro run`）也能通过 `Bpa.Rules` 和 `Bpa.Analyze()` 访问同一套规则集。

每个规则 ID 只会评估一次。 当同一 ID 出现在多个层级时，在 `te bpa run` 中以显式 `--rules` 文件中的定义为准，而在部署/保存门禁中则以内置定义为准。 然后会移除模型 `BestPracticeAnalyzer_IgnoreRules` 注释中的规则 ID。

输出中的 `Rules loaded:` 行会列出每个提供规则的层级，例如：

```
Rules loaded: 38 from 1 file(s) from bpa.rules config + built-in defaults + model annotations
```

### bpa rules

管理 BPA 规则集——在本地规则文件或模型注释中列出、检查、初始化，以及启用或禁用规则。 内置规则是只读的。要跳过其中某一条而保留其余规则，请使用 `te bpa rules disable`（不要直接编辑内置规则集）。

子命令：

| 子命令                                | 用途                           |
| ---------------------------------- | ---------------------------- |
| `add <id>`                         | 添加新的 BPA 规则。                 |
| [`disable`](#bpa-rules-disable)    | 为当前用户禁用一条内置 BPA 规则。          |
| [`enable`](#bpa-rules-enable)      | 重新启用先前已禁用的内置 BPA 规则。         |
| `ignore <rule-id>`                 | 将规则添加到模型的忽略列表。               |
| [`init`](#bpa-rules-init)          | 在解析后的 PATH 下创建一个空的 BPA 规则文件。 |
| [`list`](#bpa-rules-list)（别名 `ls`） | 列出来自所有来源的 BPA 规则及其状态。        |
| `remove <rule-id>`（别名 `rm`）        | 删除一条 BPA 规则。                 |
| `set <rule-id>`                    | 更新 BPA 规则的属性。                |
| `unignore <rule-id>`               | 从模型的忽略列表中移除一条规则。             |

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
- `te bpa rules set <id>` - 更新现有规则的属性。 使用 `-p, --property <name=value>`（可重复指定；`-` 表示从 stdin 读取值）。 属性名称：`name`、`expression`、`scope`、`category`、`severity`、`description`、`fixExpression`。
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

### 格式化表达式

表达式格式化分布在三个地方，具体取决于你要格式化的内容：

- **模型中的表达式**：`te set <path> --format <PropertyName> --save`；参见 [set](#set)。
- **独立表达式**（不在任何模型中）：`te util format-dax` / `te util format-m`；参见 [实用工具](#utilities)。
- **整个模型的批量处理**：`te script --inline "Model.AllMeasures.FormatDax();" --save`。

模型中的 DAX 始终使用逗号分隔，因此 `--semicolons` 只在 `te util format-dax` 上提供，用于处理你自己以分号输入的 DAX。

## 执行

### query

针对已部署的模型执行 DAX 查询。

`te query` 支持以下选项：

- `<dax>` - 位置参数：要执行的 DAX 查询。 等同于传入 `-q`。 选择你觉得更易读的写法即可；如果两者都提供，以显式的 `-q` 为准。
- `-q, --query <dax>` - 内联查询（即上述位置参数的命名参数形式）。 `-q -` 会从 stdin 读取查询；如果已通过管道传入输入且完全未提供查询，则会隐式读取 stdin。
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

- `--file <path>`：`.cs` / `.csx` 文件（可重复指定）。 也接受不带选项的 `.cs`/`.csx` 位置参数。
- `--inline <code>`：内联 C#（可重复指定；使用 `-` 表示从 stdin 读取）。
- `--validate`：编译脚本并报告（Report）错误，但不执行。 完全不需要模型，因此可离线作为 CI 的 lint 检查使用。
- `--save` / `--save-to` / `--serialization`。
- `--diff` / `--stat` / `--name-only`：更改输出的呈现方式（参见 [模型编辑](#model-editing) 说明）。
- `--force`：即使变更引入 DAX 验证错误，也会保存。

文件和内联代码片段会按它们在命令行中的书写顺序运行。

```bash
te script --file fix.cs --save
te script fix.cs cleanup.csx --save              # Bare positionals, run in order
te script --inline "Info(Model.Tables.Count);"
echo "Info(Model.Name);" | te script --inline -
te script --file fix.cs --validate               # Compile-only, no model needed
```

如果有任何脚本调用 `Error(...)`，本次运行将以非零状态退出，在 JSON 中报告 `"success": false`，并在结束时提示本次运行已完成但存在错误；如果指定了 `--save`，脚本此前已做出的更改仍会保存。 `Warning(...)` 和 `Info(...)` 永远不会导致运行失败。 在 Windows 上，`DisableCSharpScripts` 管理员策略会直接拒绝执行 `te script`；参见 [管理员策略](xref:te-cli-config#administrator-policies)。

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

通过宏 JSON 文件（通常为 `MacroActions.json`）管理和运行宏。 宏文件的 PATH 按以下顺序解析：`--macros <path>` → 环境变量 `TE_MACROS_PATH` → CLI 配置中的 `macros` → `./MacroActions.json`。 在 Windows 上，`DisableMacros` 管理员策略会拒绝所有 `te macro` 命令；参见 [管理员策略](xref:te-cli-config#administrator-policies)。

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
- `te macro set <name-or-id>` - 更新宏属性。 使用 `-p, --property <name=value>`（可重复指定；`-` 会从 stdin 读取值）。 属性名称：`name`、`execute`、`enabled`、`tooltip`、`validContexts`。
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
- `--save` / `--save-to` - 将宏所做的所有更改持久化保存。 与所有会修改内容的命令一样，未加 `--save` 时，`te macro run` 只会进行试运行。
- `--serialization <fmt>` / `--force`：与其他会修改内容的命令相同。

```bash
te macro run "Hide all measures"
te macro run "Format DAX" --on Sales/Revenue --save
te macro run "Format DAX" --on "'Net Sales'[Sales Amount]" --save   # DAX form works in --on too
```

## 部署和刷新

### deploy

将语义模型部署到 Power BI、Fabric、Azure Analysis Services 或本地 SQL Server Analysis Services。

**默认先试运行**：`te deploy` 会以只读方式连接，并将实际会发送的精确 TMSL 输出到 stdout。 加上 `--execute` 才会实际部署。

`te deploy` 支持以下参数：

- `-s, --server` / `-d, --database`：模型**源**，与其他所有命令完全一致。
- `--target-server <target>` / `--target-database <name>`：部署**目标**，即 Workspace 名称、端点或服务器，以及要创建或覆盖的语义模型名称。 使用服务器名称、FQDN、IP 地址或 MSOLAP 连接字符串时，会部署到 Analysis Services（本地环境使用 Windows 集成身份验证）；使用 Workspace 名称或 `powerbi://...` URL 时，会部署到 Power BI。 对于本地模型源，目标会回退到当前活动的 `te connect` 连接；当源为远程时，则必须提供这些目标参数。 将模型部署到自身会被拒绝。
- `--execute`：实际部署。 在交互模式下，会显示摘要和确认提示，且**默认安全选项为 `n`**；`--execute --force` 会跳过该提示（在 CI 中必须这样做，因为在没有 `--force` 的情况下出现提示会被视为错误）。
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
- `--force`：跳过交互式确认。
- `--ci <fmt>`：`vsts`（别名 `azdo`、`azure-devops`）或 `github`（别名 `gh`）；无法识别的值会被直接拒绝。
- `-p, --profile <name>` - 一次性使用已保存的 @te-cli-auth 配置文件。

部署时会拒绝 `--output-format bim|tmdl`。 如果要保存部署脚本供审查，请重定向试运行输出：`te deploy ... > deploy.tmsl`。

```bash
te deploy -m ./model --target-server my-workspace --target-database my-model --execute --force --ci github
te deploy -m ./model --target-server MY.SERVER.COM --target-database my-model --execute --force    # On-prem SSAS
te deploy -m ./model --target-server my-workspace --target-database my-model > deploy.tmsl         # Dry run: TMSL only
te deploy -s src-workspace -d src-model --target-server dst-workspace --target-database copy --execute   # Remote to remote
te deploy --local --target-server my-workspace --target-database my-model --execute                # Publish a Desktop model
```

> [!IMPORTANT]
> `te deploy` 会在执行前运行 Best Practice Analyzer 作为门控检查。 BPA 门控配置请参见 @te-cli-config。

即使元数据已经写入，只要服务器报告一个或多个对象存在错误，部署也会**失败**：退出代码为非零，JSON 会返回 `"success": false`，并在 `error` 中给出原因；标题会说明部署已完成但带有错误；`--ci` 也会将这些对象错误报告为错误。 未处理的对象不算失败——仅部署元数据时，本来就可能让对象不包含任何数据。 通过 `te connect -w` 设置的 Workspace 镜像也适用同样的规则。

> [!NOTE]
> 当设置 `--output-format json` 时，`te deploy` 的 JSON 输出始终包含解析后的 `server` 和 `database`，即使它们是从活动连接或配置文件中解析得到的，而不是显式传入的。 管道可使用这些字段来确认部署目标，而无需重新解析命令行。 在 `--output-format json` 下，`te deploy` 失败时也会以非零状态退出，这与其文本模式的行为一致——JSON 负载表示的是失败记录，不是成功信号。

### refresh

在已部署的模型上触发数据刷新。

**默认先试运行**：`te refresh` 会将刷新时实际会发送的 TMSL 输出到 stdout。 加上 `--execute` 才会实际执行。

`te refresh` 支持：

- `--type <type>` - `full`、`dataonly`（别名 `data-only`、`data`）、`automatic`（别名 `auto`）、`calculate`（别名 `calc`）、`clearvalues`（别名 `clear`）、`defragment`（别名 `defrag`）、`add`（默认值：`automatic`）。
- `--table <name>` - 刷新特定表(可为多个)；可重复指定。
- `--partition <Table.Partition>` - 刷新特定分区(可为多个)。
- `--execute`：实际执行刷新。 在终端中，会请求确认，且**默认安全选项为 `n`**；加上 `--force` 可跳过此提示。 无人值守运行（输出被重定向、使用 `--output-format json` 或 `--non-interactive`）时，如果未提供 `--force`，就会报错并停止，因此 `te refresh --type full --execute --force` 是适用于 CI 的形式。
- `--force` - 跳过确认提示。
- `--apply-refresh-policy <true|false|table>` - 应用增量刷新的刷新策略，以确定要刷新的分区；传入表名可将刷新范围限定到该表。 当刷新类型和范围兼容时，默认会应用这些策略，但托管在 Power BI Desktop 中的模型除外。 显式指定的值优先（若无法生效，会发出警告）。
- `--effective-date <yyyy-MM-dd>` - 设置刷新策略使用的生效日期（未应用任何策略时，将忽略此值并发出警告）。
- `--max-parallelism <N>` - 设置可并行刷新的最大分区数。 将刷新封装在 TMSL `sequence` 命令中。
- `--no-progress`, `--trace [path]`。 `--trace` 若未配合 `--execute` 使用，会发出警告并打印 TMSL。 跟踪时间以服务器时钟为准；日志会一直保留到服务器完成缓冲事件的传送；在启动带跟踪的刷新时，会停止并丢弃那些因运行中断而遗留、且已超过一小时的 `te-refresh-*` 跟踪（不会触碰其他工具的跟踪）。

在 `--output-format json` 下执行的刷新始终包含 `progress` 数组；如果启用了 `vertipaqOnRefresh` 配置键，还会包含每个表的 `vertipaq` 数组（rows、size、columns）——无需 `--trace`。

```bash
te refresh --type full --execute                        # Full refresh (asks for confirmation at a terminal)
te refresh --type full --execute --force                # Unattended: skip the confirmation
te refresh --table Sales --type full --execute          # Single table
te refresh --type full > refresh.tmsl                   # Dry run: emit TMSL only
te refresh --apply-refresh-policy Sales --execute       # Apply Sales' incremental refresh policy
```

增量刷新的刷新策略是在表的 `RefreshPolicy` 子对象上通过 [`te set`](#incremental-refresh-policies) 定义的。

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

在建立任何连接之前会先验证测试套件；验证失败的套件（例如缺少 `query_file`）会以退出码 `1` 直接退出，不会运行任何内容。 在 `--output-format json` 下，`te test run` 会输出共享的 findings JSON 文档，并附带测试专用的额外字段（`suites`、`invalidSuites`、`testSummary`）——参见 @te-cli-findings。

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

`te connect --local` 会列出所有本地 Analysis Services 实例，包括 Power BI Desktop（Store 版和安装程序版）、Visual Studio Workspace 以及独立的 SSAS；当某个实例托管多个数据库时，会提供两步提示（先选实例，再选数据库）。 非交互模式不会静默选择，而是会连同候选列表一起报错；可使用 `te connect --local <database>` 缩小范围。

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

查看和管理 CLI 配置。 （`te config list` 的别名是 `ls`。） 参见 @te-cli-config。

`te config set` 接受位置参数形式的 `key value` 键值对，或等效的 `-p key=value`。

```bash
te config list                          # Display all settings
te config paths                         # Resolved macros and BPA rules file paths
te config init                          # Create default config
te config set autoFormat true
te config set -p spinner=false          # -p form
```

## 实用工具

不依赖模型的辅助工具。 `te util` 子命令不会触碰任何模型——`--model`、`-s`/`-d`、`--local`、`--recent` 和 `--auth` 都会被拒绝。

### util format-dax

格式化一个独立的 DAX 表达式。

- `<expression>` - 要格式化的表达式；`-` 表示从 stdin 读取。
- `--semicolons` - 按使用分号作为列表分隔符编写的 DAX 进行格式化（欧洲区域设置）。 该标志会让读取到的表达式和输出都采用分号语法，因此仅适用于你用分号编写的 DAX；逗号分隔的 DAX 在该模式下会因语法错误而失败。 仅在此处支持：`te set --format` 会拒绝它，因为存储在模型中的表达式始终以逗号分隔。
- `--long` - 使用较少换行的长格式。 默认为短格式。
- `--no-space-after-function` - 省略函数名称后的空格。

```bash
te util format-dax "SUM ( Sales[Amount] )"
cat query.dax | te util format-dax -
te util format-dax "CALCULATE(SUM(Sales[Amt]); Sales[Region] = \"EU\")" --semicolons   # Semicolon-authored DAX
```

JSON 输出包含 `success`、`formatted` 和 `errors`。 对于模型中已有的表达式，请改用 `te set <path> --format <PropertyName>`；如果需要遍历整个模型的度量值，则使用 `te script --inline "Model.AllMeasures.FormatDax();" --save`。

### util format-m

格式化独立的 M/Power Query 表达式。 `-` 从标准输入读取；没有针对特定语言的选项。 格式错误的表达式——例如未闭合的字符串——会被 Report 为失败，退出代码为非零，并原样返回原始文本；绝不会在不提示的情况下返回被截短的结果。

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

在会话中，修改类命令会先将更改暂存在内存中：`save`（无参数）提交这些暂存编辑，`revert` 将其丢弃，而 `save-as` 会重新序列化到某种格式或位置。 关闭仍包含暂存编辑的会话时，会要求确认（或在无人确认时发出警告并以非零代码退出）；`exit --force` 会主动丢弃这些更改——见 @te-cli-interactive。

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

| 退出代码 | 含义                                                                                                                                 |
| ---- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `0`  | 成功。                                                                                                                                |
| `1`  | 通用失败（参数无效、命令失败、验证错误、身份验证失败、BPA gate 在严重性 >= error 时失败、`te script` 运行中脚本 Report 了错误、服务器接受了 `te deploy`，但对象存在错误）。 用于 `te diff`：发现差异。 |
| `2`  | 仅适用于 `te diff`：比较时发生错误，因此差异状态未知。                                                                                                   |

如需在 CI 管道中进行更细致的控制，可将退出代码与 `--ci <vsts/github>` 注释以及 `--trx` 结果文件结合使用——参见 @te-cli-cicd。

## 相关页面

- @te-cli - 概览和背景说明。
- @te-cli-install - 安装并设置 CLI。
- @te-cli-auth - 进行身份验证并管理连接。
- @te-cli-config - 配置文件、BPA 门禁和变更后行为。
- @te-cli-findings - validate、bpa run、test run 和 query 共享的 findings JSON。
- @te-cli-migrate - TE2 → TE3 标志映射。
