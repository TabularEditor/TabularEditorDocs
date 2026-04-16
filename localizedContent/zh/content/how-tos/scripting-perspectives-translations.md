---
uid: how-to-work-with-透视-翻译
title: 如何使用透视和翻译
author: Morten Lønskov
updated: 2026-04-10
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 如何使用透视和翻译

透视用于控制哪些对象会显示在特定的客户端视图中。 翻译（区域设置）提供本地化的名称、描述和显示文件夹。 两者都使用 TOM 对象上的索引器属性。 有关如何访问 TOM 对象及其索引器的详细信息，详见 @how-to-navigate-tom-hierarchy。

## 快速参考

```csharp
// Perspectives
measure.InPerspective["Sales"] = true;              // include in perspective
measure.InPerspective["Sales"] = false;             // exclude from perspective
var isIn = measure.InPerspective["Sales"];           // check membership

// Translations
measure.TranslatedNames["da-DK"] = "Omsætning";    // set translated name
measure.TranslatedDescriptions["da-DK"] = "...";    // set translated description
measure.TranslatedDisplayFolders["da-DK"] = "Salg"; // set translated folder

var name = measure.TranslatedNames["da-DK"];     // read translation (empty string if unset)

// Iterate cultures
foreach (var culture in Model.Cultures)
    Info(culture.Name);                              // "da-DK", "de-DE", etc.
```

## 设置透视成员关系

The `InPerspective` 索引器可用于表、列、度量值和层次结构 (即任何实现 (xref:TabularEditor.TOMWrapper.ITabularPerspectiveObject) 的对象)。

```csharp
// Add all measures in a table to a perspective
Model.Tables["Sales"].Measures.ForEach(m => m.InPerspective["Sales Report"] = true);

// Remove a table and its children from a perspective
var table = Model.Tables["Internal"];
table.InPerspective["Sales Report"] = false;
```

## 复制透视成员关系

将一个对象的透视可见性复制到另一个对象。

```csharp
var source = Model.AllMeasures.First(m => m.Name == "Revenue");
var target = Model.AllMeasures.First(m => m.Name == "Revenue YTD");

foreach (var p in Model.Perspectives)
    target.InPerspective[p.Name] = source.InPerspective[p.Name];
```

## 创建和删除透视

```csharp
// Create a new perspective (empty upon creation -- add objects as shown above)
var p = Model.AddPerspective("Executive Dashboard");

// Remove a perspective
Model.Perspectives["Old View"].Delete();
```

## 设置翻译

翻译索引器可用于实现 (xref:TabularEditor.TOMWrapper.ITranslatableObject) 的对象（表、列、度量值、层次结构、级别）。 显示文件夹的翻译需要对象实现 (xref:TabularEditor.TOMWrapper.IFolderObject)（度量值、列、层次结构）。

```csharp
var m = Model.AllMeasures.First(m => m.Name == "Revenue");
m.TranslatedNames["da-DK"] = "Omsætning";
m.TranslatedDescriptions["da-DK"] = "Total omsætning i DKK";
m.TranslatedDisplayFolders["da-DK"] = "Salg";
```

## 查找缺失的翻译

```csharp
foreach (var culture in Model.Cultures)
{
    var missing = Model.AllMeasures
        .Where(m => string.IsNullOrEmpty(m.TranslatedNames[culture.Name]));

    Info($"{culture.Name}: {missing.Count()} measures without translated names");
}
```

## 根据命名约定批量设置翻译

```csharp
// Copy the default name as the translation for cultures that are missing it
foreach (var culture in Model.Cultures)
{
    Model.AllMeasures
        .Where(m => string.IsNullOrEmpty(m.TranslatedNames[culture.Name]))
        .ForEach(m => m.TranslatedNames[culture.Name] = m.Name);
}
```

## 创建和删除区域设置

```csharp
// Add a new culture
var culture = Model.AddTranslation("fr-FR");

// Remove a culture
Model.Cultures["fr-FR"].Delete();
```

## Dynamic LINQ 等效写法

在 BPA 规则表达式中，可直接访问透视和翻译索引器。

| C# Script                                          | Dynamic LINQ (BPA)            |
| -------------------------------------------------- | ------------------------------------------------ |
| `m.InPerspective["Sales"]`                         | `InPerspective["Sales"]`                         |
| `!m.InPerspective["Sales"]`                        | `not InPerspective["Sales"]`                     |
| `string.IsNullOrEmpty(m.TranslatedNames["da-DK"])` | `String.IsNullOrEmpty(TranslatedNames["da-DK"])` |

## 另见

- @perspectives-translations
- @import-export-translations
- @how-to-navigate-tom-hierarchy
