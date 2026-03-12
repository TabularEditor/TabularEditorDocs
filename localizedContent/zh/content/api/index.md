---
uid: api-index
title: 脚本 API
author: Daniel Otykier
updated: 2026-01-27
---

# Tabular Editor API

这是 Tabular Editor 的 C# 脚本编写功能的 API 文档。

具体而言，可用于脚本编写的对象来自 **TOMWrapper.dll**、**TabularEditor3.Shared.dll** 和 **SemanticBridge.dll** 库。

## 入门

在 Tabular Editor 中编写脚本时，最常用的两个对象是 [`Selected`](xref:TabularEditor.Shared.Interaction.Selection)，它允许你访问当前在 TOM Explorer 中选中的对象，以及 [`Model`](xref:TabularEditor.TOMWrapper.Model)，它允许你访问当前加载的数据模型中的任何对象。 这两个对象都作为全局 [`ScriptHost`](xref:TabularEditor.Shared.Scripting.ScriptHost) 对象的成员属性提供。

此外，`ScriptHost` 对象还包含一些静态方法，这些方法会以全局方法的形式暴露给脚本（也就是说，你可以直接调用它们，无需加上 `ScriptHost` 前缀）。 这些方法也称为 @script-helper-methods（脚本帮助方法）。

## 示例

```csharp
// 显示一个对话框，提示用户选择一个度量值：
var myMeasure = SelectMeasure();

// 在模型的第一张表上创建一个新度量值，其名称和表达式
// 与前面选中的度量值相同：
Model.Tables.First().AddMeasure(myMeasure.Name + " copy", myMeasure.Expression);
```

更多示例请参阅 <xref:useful-script-snippets>。
