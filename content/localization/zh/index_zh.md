---
uid: api-index
title: 脚本API
author: Daniel Otykier
updated: 2022-06-16
---

# 表格编辑器API

这是表格编辑器C#脚本编写功能的API文档。

具体来说，可用于脚本编写的对象是在**TOMWrapper.dll**和**TabularEditor3.Shared.dll**库中找到的对象。

## 入门

在表格编辑器中编写脚本时，最常用的两个对象是[`Selected`](xref:TabularEditor.Shared.Interaction.Selection)（允许您访问当前在TOM浏览器中选定的对象）和[`Model`](xref:TabularEditor.TOMWrapper.Model)（允许您访问当前加载的数据模型中的任何对象）。 这两个对象都作为成员属性在全局[`ScriptHost`](xref:TabularEditor.Shared.Scripting.ScriptHost)对象上可用。

此外，`ScriptHost`对象包含静态方法，这些方法作为全局方法公开给脚本（即您可以不带`ScriptHost`前缀调用的方法）。 这些方法也称为@script-helper-methods。

## 示例

```csharp
// 向用户显示对话框，提示他们选择一个度量值：
var myMeasure = SelectMeasure();

// 在模型的第一个表上创建一个新度量值，具有相同的名称和表达式
// 作为之前选择的度量值：
Model.Tables.First().AddMeasure(myMeasure.Name + " copy", myMeasure.Expression);
```

有关更多示例，请参阅<xref:useful-script-snippets>。