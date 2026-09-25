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

By now, you are probably already aware that the Tabular Object Model (TOM) is a relatively complex data structure, with many different types of objects and properties. It is not always clear what the best values to assign to these properties are, and many times it depends on specific use cases or model designs. Tabular Editor's **Best Practice Analyzer** continuously scans the TOM for violations of best practice rules that you can define. This helps you verify that object properties are always set to their ideal values.

你可以使用 Best Practice Analyzer 检查的内容包括：

- **DAX 表达式** 创建规则，在使用特定 DAX 函数或写法时向你发出警告。
- **格式** 创建规则，提醒你指定格式字符串、说明等。
- **命名约定** 创建规则，检查某些类型的对象（例如键列、隐藏列等）是否 follow certain name patterns.
- **性能** 创建规则，检查模型中与性能相关的各项因素，例如建议减少计算列的数量等。

Best Practice Analyzer 可访问模型的完整元数据，还能访问 VertiPaq分析器的统计信息，以支持更高级的场景。

> [!NOTE]
> Tabular Editor 3 包含一整套 [内置 Best Practice Analyzer 规则](xref:built-in-bpa-rules)，并且默认启用。

# 管理最佳实践规则

要添加、删除或修改应用于模型的规则，你可以使用“工具 > 管理 BPA 规则...”菜单项。

![Bpa 管理器](~/content/assets/images/bpa-manager.png)

这个界面包含两个列表：上方列表表示当前已加载的规则**集合**。 Selecting a collection in this list, will display all the rules that are defined within this collection in the bottom list. When a model is loaded, you will see the following three rule collections:

- **当前模型中的规则**：顾名思义，这是在当前模型中定义的规则集合。这些规则定义作为注释存储在 Model 对象上。
- **本地用户的规则**：这些规则存储在你的 `%LocalAppData%\TabularEditor3\BPARules.json` 文件中。 These rules will apply to all models that are loaded in Tabular Editor by the currently logged in Windows user.
- **本地计算机上的规则**：这些规则存储在 `%ProgramData%\TabularEditor\BPARules.json` 文件中。 These rules will apply to all models that are loaded in Tabular Editor on the current machine.

如果同一条规则（按 ID）同时存在于多个集合中，则优先级顺序为自上而下。这意味着：在模型中定义的规则，会优先于在本地计算机上定义且 ID 相同的规则。 This allows you to override existing rules, for example to take model specific conventions into account.

At the top of the list, you'll see a special collection called **(Effective rules)**. 选择这个集合会显示实际应用于当前加载的模型的规则列表，并会按前文所述处理相同 ID 规则的优先级。 The lower list will indicate which collection a rule belongs to. Also, you will notice that a rule will have its name striked out, if a rule with a similar ID exists in a collection of higher precedence:

![规则覆盖](~/content/assets/images/rule-overrides.png)

## 添加其他规则集

Rule collections can be added to a specific model. 如果你的规则文件位于网络共享上，你可以将该文件作为规则集包含到当前模型中。 If you have write access to the location of the file, you'll also be able to add/modify/remove rules from the file. Rule collections that are added this way take precedence over rules that are defined within the model. If you add multiple such collections, you can shift them up and down to control their mutual precedence.

点击“添加...”按钮，将新的规则集添加到模型中。 This provides the following options:

![添加最佳实践规则集](~/content/assets/images/add-rule-file.png)

- **Create new Rule File**: This will create a new, empty, .json file at a specified location, which you can subsequently add rules to. When choosing the file, notice that there is an option for using relative file paths. This is useful when you want to store the rule file in the same code repository as the current model. However, please be aware that a relative rule file reference only works, when the model has been loaded from disk (since there is no working directory when loading a model from an instance of Analysis Services).
- **包含本地规则文件**：如果你已经有一个包含规则的 .json 文件，并希望将其包含到模型中，就用这个选项。 Again, you have the option of using relative file paths, which may be beneficial if the file is located close to the model metadata. If the file is located on a network share (or generally, on a drive different than where the currently loaded model metadata resides), you can only include it using an absolute path.
- **Include Rule File from URL**: This option lets you specify an HTTP/HTTPS URL, that should return a valid set of rules (in json format). 当你希望从在线来源包含规则时，这会很有用，例如来自 [BestPracticeRules GitHub 站点](https://github.com/TabularEditor/BestPracticeRules) 的[标准 BPA 规则](https://raw.githubusercontent.com/TabularEditor/BestPracticeRules/master/BPARules-standard.json)。 Note that rule collections added from online sources will be read-only.

## 修改规则集中的规则

在你对规则集存储位置具有写入权限的前提下，屏幕下半部分可让你在当前选中的规则集中添加、编辑、克隆和删除规则。 Moreover, the "Move to..." button allows you to move or copy the selected rule to another collection, making it easy to manage multiple collections of rules.

## 添加规则

To add a new rule to a collection, click on the **New rule...** button. This brings up the Best Practice Rule editor (see screenshot below).

![Bpa Rule Editor](~/content/assets/images/bpa-rule-editor.png)

创建新规则时，你必须指定以下详细信息：

- **名称**：规则的名称，将显示给 Tabular Editor 的用户
- **ID**：规则的内部 ID。 Must be unique within a rule collection. If multiple rules have identical IDs across different collections, only the rule within the collection of the highest precedence is applied.
- **严重性**：严重性在 Tabular Editor 的 UI 中不会用到，但通过 [Tabular Editor 的命令行界面](xref:command-line-options)运行最佳实践分析时，这个数值会决定规则违规的“严重”程度。
  - 1 = 仅供参考
  - 2 = 警告
  - 3（及以上）= 错误
- **类别**：用于对规则进行逻辑分组，以便更方便地管理规则。
- **Description** (optional): Can be used to provide a description of what the rule is intended for. Will be shown in the Best Practice Analyzer view as a tooltip. You may use the following placeholder values within the description field, to provide a more contextual message:
  - `%object%` 返回对当前对象的完全限定的 DAX 引用（如适用）
  - `%objectname%` 仅返回当前对象的名称
  - `%objecttype%` 返回当前对象的类型
- **适用范围**：选择该规则应适用的对象类型(一个或多个)。
- **表达式**：输入一个 [Dynamic LINQ](https://dynamic-linq.net/expression-language) 搜索表达式，该表达式应对那些(在 **适用范围** 下拉列表中选定的对象类型中)违反规则的对象计算为 `true`。 The Dynamic LINQ expression can access the TOM properties available on the selected object types, as well as a wide range of standard .NET methods and properties.
- **最低兼容级别**：某些 TOM 属性并非在所有兼容级别中都可用。 If you are creating generic rules, use this dropdown to specify the minimum compatibility level of the models to which the rule should apply.

当规则保存到磁盘上的规则集中时，上述所有属性都会以 JSON 格式存储。 You can add/edit/delete rules by editing the JSON file as well, which also allows you to specify the `FixExpression` property on a rule. This is a string that is used to generate a [C# script](xref:cs-scripts-and-macros) which will be applied to the model in order to fix the rule violation.

# 使用 Best Practice Analyzer 视图

Tabular Editor 会在 **Best Practice Analyzer 视图**中显示最佳实践规则的违规情况。 You can also see the number of rule violations in the status bar at the bottom of the main window. To bring the view into focus, use the **View > Best Practice Analyzer** menu option or click on the "# BP issues" button in the status bar.

![Best Practice Analyzer 视图](~/content/assets/images/best-practice-analyzer-view.png)

**Best Practice Analyzer 视图**会显示一个列表，其中包含所有存在违规对象的规则。 Below each rule is a list of the violating objects. You can double-click on an object in the list, to navigate to that object in the **TOM Explorer**.

> [!TIP]
> **企业版用户**：内置 BPA 规则会与你定义的任何自定义规则一同显示。 These rules are enabled by default and provide comprehensive best practice guidance. You can manage built-in rules through **Tools > Manage BPA Rules...** where they appear in the **(Built-in rules)** collection. For more information, see [Built-in BPA rules](xref:built-in-bpa-rules).

![项目选项](~/content/assets/images/bpa-options.png)

右键点击某个对象时，你会看到如上所示的一组选项。 These are:

- **转到对象**：这与双击对象的效果相同，可在 **TOM Explorer** 中定位到该对象。
- **忽略对象**：这会在对象上添加一条注释，指示 Best Practice Analyzer 在该对象上忽略此特定规则。 Ignored rules are specified using their ID.
- **Generate fix script**: This option is available only if a rule has the `FixExpression` property specified. 选择此选项后，Tabular Editor 会基于所选规则(s)的 `FixExpression` 创建一个新的 C# Script。
- **应用修复**：仅当某条规则指定了 `FixExpression` 属性时，此选项才可用。 When choosing this option, Tabular Editor executes the `FixExpression` of the selected rule(s) in order to automatically fix the rule violation.

> [!NOTE]
> 在 Best Practice Analyzer 视图中，你可以按住 Shift 或 Ctrl 键来多选对象。

上述选项也会以工具栏按钮的形式出现在 **Best Practice Analyzer 视图** 顶部。 In addition, there are buttons available for expanding/collapsing all items, showing ignored rules/objects and for performing a manual refresh (which is needed when background scans are disabled, see below).

# 禁用 Best Practice Analyzer

在某些情况下，你可能希望禁用 Best Practice Analyzer 的后台扫描。 For example, when you have rules that take a relatively long time to evaluate, or when you are working with very large models.

你可以在 **工具 > 偏好 > Best Practice Analyzer** 下，取消勾选 **在后台扫描最佳实践违规** 来禁用后台扫描。

注意：即使已禁用后台扫描，你仍然可以按上述方式使用 **Best Practice Analyzer 视图** 的 **刷新** 按钮手动执行扫描。

# 后续步骤

- @C# 脚本和宏
- @personalizing-te3