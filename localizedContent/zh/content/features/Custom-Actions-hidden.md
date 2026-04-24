---
uid: custom-actions
title: 自定义操作
---

# 自定义操作

> [!NOTE]
> 请注意：此功能与多维模型中的“自定义操作”功能无关。

假设你使用 `Selected` 对象创建了一个很实用的脚本，并且希望能在资源管理器树中对不同对象重复执行该脚本。 无需每次执行脚本都点击“播放”按钮，Tabular Editor 允许你将其保存为自定义操作： 无需每次执行脚本都点击“播放”按钮，Tabular Editor 允许你将其保存为自定义操作：

![图片](https://user-images.githubusercontent.com/8976200/33581673-0db35ed0-d952-11e7-90cd-e3164e198865.png)

保存自定义操作后，你会发现它会直接出现在资源管理器树的右键上下文菜单中，这样就能非常方便地对树中选中的任意对象调用该脚本。 你可以按需创建任意数量的自定义操作。 在名称中使用反斜杠（\\）可在上下文菜单中创建子菜单结构。 你可以按需创建任意数量的自定义操作。 在名称中使用反斜杠（\\）可在上下文菜单中创建子菜单结构。

![自定义操作会直接显示在上下文菜单中](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/InvokeCustomAction.png)

自定义操作存储在 %AppData%\Local\TabularEditor 下的 CustomActions.json 文件中。 在上面的示例中，该文件的内容如下： 在上面的示例中，该文件的内容如下：

```json
{
  "Actions": [
    {
      "Name": "Custom Formatting\\Number with 1 decimal",
      "Enabled": "true",
      "Execute": "Selected.Measures.ForEach(m => m.FormatString = \"0.0\";",
      "Tooltip": "Sets the FormatString property to \"0.0\"",
      "ValidContexts": "Measure, Column"
    }
  ]
}
```

如你所见，`Name` 和 `Tooltip` 的值来自保存该操作时所填写的内容。 `Execute` 是在调用该操作时实际要执行的脚本。 如你所见，`Name` 和 `Tooltip` 的值来自保存该操作时所填写的内容。 `Execute` 是在调用该操作时实际要执行的脚本。 请注意：CustomActions.json 文件中的任何语法错误都会导致 Tabular Editor 完全跳过加载所有自定义操作。因此，在将脚本保存为自定义操作之前，请先确保该脚本能在高级脚本编辑器中成功执行。

`ValidContexts` 属性包含一个对象类型列表，操作仅会对这些类型的对象可用。 `ValidContexts` 属性包含一个对象类型列表，操作仅会对这些类型的对象可用。 在树中选择对象时，如果当前选择中包含任何不在 `ValidContexts` 属性列表中的对象类型，该操作将不会显示在上下文菜单中。

## 控制操作可用性

如果你需要更精细地控制操作何时可从上下文菜单调用，可以将 `Enabled` 属性设置为一个自定义表达式。该表达式必须返回布尔值，用于指示在当前选择下该操作是否可用。 默认情况下，`Enabled` 属性的值为 "true"，表示在有效上下文中该操作始终可用。 请记住，在 `Selected` 对象上使用单数对象引用时要特别注意，例如 `Selected.Measure` 或 `Selected.Table`，因为如果当前选择未恰好包含一个该类型的对象，就会抛出错误。 在这种情况下，建议使用 `Enabled` 属性检查当前是否恰好选中了一个所需类型的对象： 默认情况下，`Enabled` 属性的值为 "true"，表示在有效上下文中该操作始终可用。 请记住，在 `Selected` 对象上使用单数对象引用时要特别注意，例如 `Selected.Measure` 或 `Selected.Table`，因为如果当前选择未恰好包含一个该类型的对象，就会抛出错误。 在这种情况下，建议使用 `Enabled` 属性检查当前是否恰好选中了一个所需类型的对象：

```json
{
  "Actions": [
    {
      "Name": "Reset measure name",
      "Enabled": "Selected.Measures.Count == 1",
      "Execute": "Selected.Measure.Name == \"New Measure\"",
      "ValidContexts": "Measure"
    }
  ]
}
```

这将禁用该上下文菜单项，除非在树状视图中恰好选中了一个度量值。

## 重用自定义操作

2.7 版本引入了新的脚本方法 `CustomAction(...)`，可用于调用之前保存的自定义操作。 你可以将此方法作为独立方法使用（类似于 `Output(...)`），也可以将其作为扩展方法用于任意对象集合： 你可以将此方法作为独立方法使用（类似于 `Output(...)`），也可以将其作为扩展方法用于任意对象集合：

```csharp
// 对当前选择执行“我的自定义操作”：
CustomAction("My custom action");                

// 对模型中的所有表执行“我的自定义操作”：
CustomAction(Model.Tables, "My custom action");

// 对当前选择中名称以“Sum”开头的每个度量值执行“我的自定义操作”：
Selected.Measures.Where(m => m.Name.StartsWith("Sum")).CustomAction("My custom action");
```

请注意，您必须指定自定义操作的完整名称，包括任何上下文菜单文件夹名称。

如果找不到指定名称的操作，脚本执行时将引发错误。
