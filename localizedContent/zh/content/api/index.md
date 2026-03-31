---
uid: api-index
title: 脚本 API
author: Daniel Otykier
updated: 2026-01-27
---

# Tabular Editor API

这是 Tabular Editor 的 C# Script 功能的 API 文档。

具体来说，可用于编写脚本的对象来自 **TOMWrapper.dll**、**TabularEditor3.Shared.dll** 和 **SemanticBridge.dll** 库。

## 开始使用

在 Tabular Editor 中编写脚本时，最常用的两个对象是 [`Selected`](xref:TabularEditor.Shared.Interaction.Selection) 和 [`Model`](xref:TabularEditor.TOMWrapper.Model)。前者可让你访问当前在 TOM Explorer 中选中的对象，后者可让你访问当前已加载的 Data model 中的任何对象。 这两个对象都可作为全局 [`ScriptHost`](xref:TabularEditor.Shared.Scripting.ScriptHost) 对象的成员属性使用。 这两个对象都可作为全局 [`ScriptHost`](xref:TabularEditor.Shared.Scripting.ScriptHost) 对象的成员属性使用。

此外，`ScriptHost` 对象还包含一些静态方法，这些方法会作为全局方法向脚本公开（也就是说，无需加上 `ScriptHost` 前缀即可调用）。 这些方法也称为 @script-helper-methods。 这些方法也称为 @script-helper-methods。

## 示例

```csharp
// 显示一个对话框，提示用户选择一个度量值：
var myMeasure = SelectMeasure();

// 在模型的第一张表上创建一个新的度量值，其名称和表达式
// 与先前选中的度量值相同：
Model.Tables.First().AddMeasure(myMeasure.Name + " copy", myMeasure.Expression);
```

更多示例请参阅 <xref:useful-script-snippets>。
