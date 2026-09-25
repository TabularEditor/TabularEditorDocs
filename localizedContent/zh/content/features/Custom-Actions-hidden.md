---
uid: custom-actions
title: 自定义操作
---

# 自定义操作

> [!NOTE]
> 请注意：此功能与多维模型中的“自定义操作”功能无关。

假设你使用 `Selected` 对象创建了一个很实用的脚本，并且希望能在资源管理器树中对不同对象重复执行该脚本。 Instead of hitting the "Play" button whenever you want to execute the script, Tabular Editor lets you save it as a Custom Action:

![image](~/content/assets/images/custom-actions-01.png)

保存自定义操作后，你会发现它会直接出现在资源管理器树的右键上下文菜单中，这样就能非常方便地对树中选中的任意对象调用该脚本。 You can create as many custom actions as you want. Use backslashes (\\) in the names to create a submenu structure within the context menu.

![Custom Actions show up directly in the context menu](~/content/assets/images/custom-actions-02.png)

自定义操作存储在 %AppData%\Local\TabularEditor 下的 CustomActions.json 文件中。 In the above example, the contents of this file will look like this:

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

As you can see, `Name` and `Tooltip` gets their values from whatever was specified when the action was saved. `Execute` is the actual script to be executed when the action is invoked. 请注意：CustomActions.json 文件中的任何语法错误都会导致 Tabular Editor 完全跳过加载所有自定义操作。因此，在将脚本保存为自定义操作之前，请先确保该脚本能在高级脚本编辑器中成功执行。

The `ValidContexts` property holds a list of object types for which the Action will be available. 在树中选择对象时，如果当前选择中包含任何不在 `ValidContexts` 属性列表中的对象类型，该操作将不会显示在上下文菜单中。

## 控制操作可用性

如果你需要更精细地控制操作何时可从上下文菜单调用，可以将 `Enabled` 属性设置为一个自定义表达式。该表达式必须返回布尔值，用于指示在当前选择下该操作是否可用。 By default, the `Enabled` property has the value "true", which means that the action will always be enabled within the valid context. Keep this in mind, when using the singular object references on the `Selected` object, such as `Selected.Measure` or `Selected.Table`, as these will throw an error if the current selection does not contain exactly one of that type of object. In such a case, it is recommended to use the `Enabled` property to check that one and only one object of the required type, has been selected:

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

2.7 版本引入了新的脚本方法 `CustomAction(...)`，可用于调用之前保存的自定义操作。 You can use this method as a stand-alone method (similar to `Output(...)`), or you can use it as an extension method on any set of objects:

```csharp
// Executes "My custom action" against the current selection:
CustomAction("My custom action");                

// Executes "My custom action" against all tables in the model:
CustomAction(Model.Tables, "My custom action");

// Executes "My custom action" against every measure in the current selection whose name starts with "Sum":
Selected.Measures.Where(m => m.Name.StartsWith("Sum")).CustomAction("My custom action");
```

请注意，您必须指定自定义操作的完整名称，包括任何上下文菜单文件夹名称。

如果找不到指定名称的操作，脚本执行时将引发错误。
