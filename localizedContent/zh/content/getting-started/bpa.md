---
uid: bpa
title: 使用 Best Practice Analyzer 提升代码质量
author: Daniel Otykier
updated: 2026-10-12
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

**Best Practice Analyzer** (BPA) 会在后台扫描已加载模型的 Tabular Object Model (TOM)，查找违反你定义的最佳实践规则的对象。 TOM 有许多[对象类型和属性](xref:TabularEditor.TOMWrapper)，而属性的正确取值通常取决于模型设计。 BPA 规则用于检查每个属性的值是否符合你的约定要求。

使用 Best Practice Analyzer 规则检查以下内容：

- **DAX 表达式**：在使用特定 DAX 函数或写法时发出警告。
- **格式设置**：要求提供格式字符串、描述等类似属性。
- **命名约定**：检查键列、隐藏列等对象是否遵循命名模式。
- **性能**：检查模型中与性能相关的方面，例如计算列的数量。

规则可以访问完整的模型元数据以及 VertiPaq分析器的统计信息。

> [!NOTE]
> Tabular Editor 3 包含[内置 Best Practice Analyzer 规则](xref:built-in-bpa-rules)，并默认启用。它们会显示在 **Best Practice Analyzer 视图**中，与自定义规则一起列出；同时也会显示在 **工具 > 管理 BPA 规则...** 下的 **（内置规则）** 集合中。

## 管理最佳实践规则

打开 **工具 > 管理 BPA 规则...**，以添加、删除或修改应用于你的模型的规则。

![“管理最佳实践规则”对话框，顶部是规则集列表，下方是所选规则集的规则](~/content/assets/images/bpa-manager.png)

上方列表显示已加载的**规则集**，下方列表显示所选规则集中的规则。加载模型后，会列出以下规则集：

- **当前模型中的规则**：在当前模型中定义的规则，作为 Model 对象上的注解存储。
- **本地用户的规则**：存储在 `%LocalAppData%\TabularEditor3\BPARules.json` 中的规则。这些规则适用于当前 Windows 用户在 Tabular Editor 中加载的每个模型。
- **本地计算机上的规则**：存储在 `%ProgramData%\TabularEditor\BPARules.json` 中的规则。这些规则适用于在这台计算机上通过 Tabular Editor 加载的每个模型。

如果多个规则集中存在相同 ID 的规则，则列表中位置更高的规则集优先。模型中定义的规则会覆盖本地计算机上具有相同 ID 的规则，因此你可以根据特定模型的约定调整共享规则。

列表顶部的 **（生效规则）** 集合显示在确定优先级后实际应用于已加载模型的规则。下方列表显示每条规则所属的规则集。如果在更高优先级的集合中存在 ID 相同的规则，该规则名称会以删除线划掉：

![生效规则列表，其中被覆盖的规则会以删除线显示](~/content/assets/images/rule-overrides.png)

### 添加其他规则集

你可以将规则文件，例如位于网络共享上的文件，作为规则集添加到当前模型中。如果你有该文件的写入权限，就可以添加、修改和删除其中的规则。以这种方式添加的规则集，其优先级高于模型中定义的规则。如果你添加了多个规则集，可以上下移动它们来设置优先级。

点击 **添加...** 将规则集添加到模型中：

![添加最佳实践规则集](~/content/assets/images/add-rule-file.png)

- **创建新规则文件**：在你指定的位置创建一个空的 .json 文件。在文件对话框中，可以选择“相对文件路径”选项，这样即可将规则文件与模型存放在同一 repository 中。只有在模型从磁盘加载时，相对引用才有效。从 Analysis Services 实例加载的模型没有工作目录。
- **包含本地规则文件**：包含一个现有的 .json 规则文件。如果文件和模型元数据在同一驱动器上，你就可以使用相对路径。位于网络共享或其他驱动器上的文件必须使用绝对路径。
- **从 URL 包含规则文件**：包含通过 HTTP 或 HTTPS URL 获取的规则，例如来自 [BestPracticeRules GitHub 站点](https://github.com/TabularEditor/BestPracticeRules) 的 [标准 BPA 规则](https://raw.githubusercontent.com/TabularEditor/BestPracticeRules/master/BPARules-standard.json)。从 URL 添加的规则集是只读的。

### 修改规则集中的规则

如果你对所选规则集的存储位置有写入权限，则可在对话框下半部分对该规则集中的规则进行添加、编辑、克隆和删除。**移动到...**：将所选规则移动或复制到另一个规则集中。

### 添加规则

点击 **新建规则...** 来打开最佳实践规则编辑器：

![最佳实践规则编辑器，包含名称、ID、严重性、类别、说明、适用对象和表达式字段](~/content/assets/images/bpa-rule-editor.png)

规则具有以下属性：

- **名称**：在 Tabular Editor 中显示的规则名称。
- **ID**：内部 ID，在同一规则集中必须唯一。如果不同规则集中的规则共用同一个 ID，则只有优先级最高的规则集中的规则会生效。
- **严重性**：在 Tabular Editor 界面中未使用。当你从[命令行](xref:command-line-options)运行最佳做法分析时，该数字用于指示违规的严重程度：
  - 1 = 仅供参考
  - 2 = 警告
  - 3（及以上）= 错误
- **类别**：用于将相关规则归为一组。
- **描述**（可选）：规则的说明，会在 **Best Practice Analyzer 视图** 中显示为工具提示。描述支持以下占位符：
  - `%object%` 返回对当前对象的完全限定的 DAX 引用（如适用）
  - `%objectname%` 仅返回当前对象的名称
  - `%objecttype%` 返回当前对象的类型
- **适用范围**：规则检查的对象类型。
- **表达式**：一个 [Dynamic LINQ](https://dynamic-linq.net/expression-language) 表达式，用于对 **适用范围** 中所选类型里违反该规则的对象求值，并返回 `true`。该表达式可以使用所选对象类型的 TOM 属性，以及大量标准 .NET 方法和属性。
- **最低兼容级别**：规则适用的模型的最低兼容级别。某些 TOM 属性并非在所有兼容级别中都存在。

磁盘上的规则集会以 JSON 格式存储这些属性。你也可以直接在 JSON 文件中添加、编辑和删除规则。在该文件中，你可以设置规则的 `FixExpression` 属性：它是一个字符串，用于生成用于修复该违规的 [C# Script](xref:cs-scripts-and-macros)。

## 使用 Best Practice Analyzer 视图

**Best Practice Analyzer 视图**会列出规则的违规情况，主窗口底部的状态栏会显示其数量。可通过 **视图 > Best Practice Analyzer** 或状态栏中的 **# BP issues** 按钮打开该视图。

![Best Practice Analyzer 视图](~/content/assets/images/best-practice-analyzer-view.png)

该视图会列出每条存在违规对象的规则，并在其下方显示这些对象。双击对象可在 **TOM Explorer** 中选中它。

![Best Practice Analyzer 视图中对象的上下文菜单](~/content/assets/images/bpa-options.png)

右键单击对象可使用以下选项：

- **转到对象**：在 **TOM Explorer** 中选中该对象，与双击效果相同。
- **忽略对象**：在对象上添加一条注释，使 Best Practice Analyzer 在该对象上跳过这条规则。该注释会存储规则 ID。
- **生成修复脚本**：根据所选规则的 `FixExpression` 生成 C# Script。仅当规则具有 `FixExpression` 时可用。
- **应用修复**：对所选规则执行其 `FixExpression`。仅当规则具有 `FixExpression` 时可用。

> [!NOTE]
> 按住 Shift 或 Ctrl 键，即可在 Best Practice Analyzer 视图中选择多个对象。

视图顶部的工具栏提供相同的选项，另外还包含用于展开或折叠所有项、显示已忽略的规则和对象，以及手动刷新扫描的按钮。

## 禁用 Best Practice Analyzer

如果某些规则评估耗时较长，或模型非常大，可以关闭后台扫描：在 **工具 > 偏好 > Tabular Editor > 杂项** 的 **Best Practice Analyzer** 部分，清除 **在后台扫描 Best Practice 违规** 的勾选。关闭后台扫描后，点击 **Best Practice Analyzer 视图** 中的 **刷新** 即可扫描。

## 后续步骤

- @C# 脚本和宏
- @personalizing-te3
