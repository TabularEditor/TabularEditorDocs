---
uid: bpa
title: 使用 Best Practice Analyzer 提升代码质量
author: Daniel Otykier
updated: 2021-11-02
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 使用 Best Practice Analyzer 提升代码质量

到目前为止，你可能已经知道 Tabular Object Model (TOM) 是一个相对复杂的数据结构，包含许多不同类型的对象和属性。 这些属性该设置为哪些最佳值并不总是很清楚，而且很多时候取决于具体用例或模型设计。 Tabular Editor 的 **Best Practice Analyzer** 会持续扫描 TOM，检测是否存在违反你所定义的最佳实践规则的情况。 这能帮助你确保对象属性始终设置为最合适的值。

你可以使用 Best Practice Analyzer 检查的内容包括：

- **DAX 表达式** 创建规则，在使用特定 DAX 函数或写法时向你发出警告。
- **格式** 创建规则，提醒你指定格式字符串、说明等。
- **命名约定** 创建规则，检查某些类型的对象（例如键列、隐藏列等）是否 遵循特定的命名模式。
- **性能** 创建规则，检查模型中与性能相关的各项因素，例如建议减少计算列的数量等。

Best Practice Analyzer 可访问模型的完整元数据，还能访问 VertiPaq分析器的统计信息，以支持更高级的场景。

> [!NOTE]
> Tabular Editor 3 包含一整套 [内置 Best Practice Analyzer 规则](xref:built-in-bpa-rules)，并且默认启用。

# 管理最佳实践规则

要添加、删除或修改应用于模型的规则，你可以使用“工具 > 管理 BPA 规则...”菜单项。

![Bpa 管理器](~/content/assets/images/bpa-manager.png)

这个界面包含两个列表：上方列表表示当前已加载的规则**集合**。 在此列表中选择一个集合后，底部列表将显示该集合中定义的所有规则。 加载模型后，你会看到以下三个规则集：

- **当前模型中的规则**：顾名思义，这是在当前模型中定义的规则集合。 规则定义作为 Model 对象上的注释存储。
- **本地用户的规则**：这些规则存储在你的 `%LocalAppData%\TabularEditor3\BPARules.json` 文件中。 这些规则会对当前登录的 Windows 用户在 Tabular Editor 中加载的所有模型生效。
- **本地计算机上的规则**：这些规则存储在 `%ProgramData%\TabularEditor\BPARules.json` 文件中。 这些规则会对当前这台机器上在 Tabular Editor 中加载的所有模型生效。

如果同一条规则（按 ID）同时存在于多个集合中，则优先级顺序为自上而下。这意味着：在模型中定义的规则，会优先于在本地计算机上定义且 ID 相同的规则。 这样你就可以覆盖现有规则，例如将特定于模型的约定纳入考虑。

在列表顶部，你会看到一个特殊的集合，名为 **(生效规则)**。 选择这个集合会显示实际应用于当前加载的模型的规则列表，并会按前文所述处理相同 ID 规则的优先级。 下方列表会标明某条规则属于哪个集合。 此外，如果在更高优先级的集合中存在 ID 相同或相近的规则，你会看到该规则的名称会被加删除线：

![规则覆盖](~/content/assets/images/rule-overrides.png)

## 添加其他规则集

规则集可以添加到特定模型中。 如果你的规则文件位于网络共享上，你可以将该文件作为规则集包含到当前模型中。 如果你对该文件所在位置具有写入权限，你也可以在文件中添加/修改/删除规则。 以这种方式添加的规则集，其优先级高于模型内定义的规则。 如果你添加了多个此类规则集，可以将它们上移或下移，以控制它们之间的优先级。

点击“添加...”按钮，将新的规则集添加到模型中。 这将提供以下选项：

![添加最佳实践规则集](~/content/assets/images/add-rule-file.png)

- **创建新的规则文件**：这会在指定位置创建一个新的空 .json 文件，之后你可以向其中添加规则。 选择文件时，请注意有一个选项可使用相对文件路径。 当你想把规则文件与当前模型一起存放在同一个代码 repository 中时，这会很有用。 不过要注意：相对规则文件引用只有在模型从磁盘加载时才有效（因为从 Analysis Services 实例加载模型时没有工作目录）。
- **包含本地规则文件**：如果你已经有一个包含规则的 .json 文件，并希望将其包含到模型中，就用这个选项。 同样，你也可以选择使用相对文件路径；如果该文件位于模型元数据附近，这可能会更方便。 如果文件位于网络共享上（或更一般地说，位于与当前加载的模型元数据所在位置不同的驱动器上），则只能使用绝对路径包含该文件。
- **从 URL 包含规则文件**：此选项允许你指定一个 HTTP/HTTPS URL，该 URL 应返回一组有效的规则（JSON 格式）。 当你希望从在线来源包含规则时，这会很有用，例如来自 [BestPracticeRules GitHub 站点](https://github.com/TabularEditor/BestPracticeRules) 的[标准 BPA 规则](https://raw.githubusercontent.com/TabularEditor/BestPracticeRules/master/BPARules-standard.json)。 注意：从在线来源添加的规则集会是只读的。

## 修改规则集中的规则

在你对规则集存储位置具有写入权限的前提下，屏幕下半部分可让你在当前选中的规则集中添加、编辑、克隆和删除规则。 此外，“移动到...”按钮允许你将所选规则移动或复制到另一个规则集，便于管理多个规则集。

## 添加规则

要向规则集添加新规则，点击 **新建规则...** 按钮。 这将打开“最佳实践规则”编辑器（见下方屏幕截图）。

![Bpa Rule Editor](~/content/assets/images/bpa-rule-editor.png)

创建新规则时，你必须指定以下详细信息：

- **名称**：规则的名称，将显示给 Tabular Editor 的用户
- **ID**：规则的内部 ID。 在同一规则集中必须唯一。 如果多个规则在不同规则集中具有相同的 ID，则只会应用优先级最高的规则集中的那条规则。
- **严重性**：严重性在 Tabular Editor 的 UI 中不会用到，但通过 [Tabular Editor 的命令行界面](xref:command-line-options)运行最佳实践分析时，这个数值会决定规则违规的“严重”程度。
  - 1 = 仅供参考
  - 2 = 警告
  - 3（及以上）= 错误
- **类别**：用于对规则进行逻辑分组，以便更方便地管理规则。
- **描述**（可选）：可用于描述该规则的用途。 它会在 Best Practice Analyzer 视图中以工具提示形式显示。 你可以在描述字段中使用以下占位符值，以提供更贴合上下文的信息：
  - `%object%` 返回对当前对象的完全限定的 DAX 引用（如适用）
  - `%objectname%` 仅返回当前对象的名称
  - `%objecttype%` 返回当前对象的类型
- **适用范围**：选择该规则应适用的对象类型(一个或多个)。
- **表达式**：输入一个 [Dynamic LINQ](https://dynamic-linq.net/expression-language) 搜索表达式，该表达式应对那些(在 **适用范围** 下拉列表中选定的对象类型中)违反规则的对象计算为 `true`。 Dynamic LINQ 表达式可以访问所选对象类型上可用的 TOM 属性，也可以使用大量标准 .NET 方法和属性。
- **最低兼容级别**：某些 TOM 属性并非在所有兼容级别中都可用。 如果你在创建通用规则，请使用此下拉列表指定该规则适用的模型的最低兼容级别。

当规则保存到磁盘上的规则集中时，上述所有属性都会以 JSON 格式存储。 你也可以通过编辑 JSON 文件来添加/编辑/删除规则，同时还能为规则指定 `FixExpression` 属性。 这是一个字符串，用于生成将应用到模型上的 [C# Script](xref:cs-scripts-and-macros)，以修复规则违规。

# 使用 Best Practice Analyzer 视图

Tabular Editor 会在 **Best Practice Analyzer 视图**中显示最佳实践规则的违规情况。 你还可以在主窗口底部的状态栏中查看规则违规的数量。 要切换到该视图，可以使用 **视图 > Best Practice Analyzer** 菜单选项，或点击状态栏中的“# BP issues”按钮。

![Best Practice Analyzer 视图](~/content/assets/images/best-practice-analyzer-view.png)

**Best Practice Analyzer 视图**会显示一个列表，其中包含所有存在违规对象的规则。 每条规则下方都会列出违规对象。 你可以在列表中双击某个对象，以在 **TOM Explorer** 中定位到该对象。

> [!TIP]
> **企业版用户**：内置 BPA 规则会与你定义的任何自定义规则一同显示。 这些规则默认启用，并提供全面的最佳实践指导。 你可以通过 **工具 > 管理 BPA 规则...** 来管理内置规则；它们会显示在 **（内置规则）** 集合中。 有关详细信息，请参阅 [内置 BPA 规则](xref:built-in-bpa-rules)。

![项目选项](~/content/assets/images/bpa-options.png)

右键点击某个对象时，你会看到如上所示的一组选项。 这些选项包括：

- **转到对象**：这与双击对象的效果相同，可在 **TOM Explorer** 中定位到该对象。
- **忽略对象**：这会在对象上添加一条注释，指示 Best Practice Analyzer 在该对象上忽略此特定规则。 被忽略的规则通过其 ID 指定。
- **生成修复脚本**：仅当某条规则指定了 `FixExpression` 属性时，此选项才可用。 选择此选项后，Tabular Editor 会基于所选规则(s)的 `FixExpression` 创建一个新的 C# Script。
- **应用修复**：仅当某条规则指定了 `FixExpression` 属性时，此选项才可用。 选择此选项后，Tabular Editor 会执行所选规则(s)的 `FixExpression`，以自动修复该规则违规问题。

> [!NOTE]
> 在 Best Practice Analyzer 视图中，你可以按住 Shift 或 Ctrl 键来多选对象。

上述选项也会以工具栏按钮的形式出现在 **Best Practice Analyzer 视图** 顶部。 此外，还提供用于展开/折叠所有项、显示已忽略的规则/对象，以及执行手动刷新（禁用后台扫描时需要，见下文）的按钮。

# 禁用 Best Practice Analyzer

在某些情况下，你可能希望禁用 Best Practice Analyzer 的后台扫描。 例如，当某些规则评估耗时较长，或你正在处理非常大的模型时。

你可以在 **工具 > 偏好 > Best Practice Analyzer** 下，取消勾选 **在后台扫描最佳实践违规** 来禁用后台扫描。

注意：即使已禁用后台扫描，你仍然可以按上述方式使用 **Best Practice Analyzer 视图** 的 **刷新** 按钮手动执行扫描。

# 后续步骤

- @cs-scripts-and-macros
- @personalizing-te3