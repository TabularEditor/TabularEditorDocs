---
uid: object-properties-common
title: 通用属性
author: Jeroen ter Heerdt
updated: 2026-10-05
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

# 通用属性

<!--
SUMMARY: Properties that most objects in a semantic model share, such as Name, Description, Annotations and Lineage Tag.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

本页所列属性适用于多种对象类型，并且在所有包含这些属性的对象上行为一致。每个条目都会列出该属性在 Tabular Object Model (TOM) 中的名称、类型和类别。各对象的专属页面都链接到这些条目。其他页面请参见 @object-properties。

## 基本

### 姓名

`Name` · string · 基本

对象的名称。 DAX 通过名称引用表、列、度量值、层次结构和用户定义函数。名称在同级对象中必须唯一，因此两个度量值不能同名。在大多数模型中，度量值也不能与任何列同名（见 @object-properties-model 中的 `ForceUniqueNames`）。 KPI 或计算组本身没有自己的名称，而是采用其所属对象的名称。

在 **工具 > 偏好** 中启用 **公式修正** 后，重命名对象会更新引用它的 DAX 表达式。禁用后，重命名会使使用旧名称的表达式失效。见 @formula-fix-up-dependencies。

要一次重命名多个对象，请在 **TOM Explorer** 中选择它们，然后使用支持正则表达式的批量重命名功能。见 @duplicate-and-batch。 Best Practice Analyzer (BPA) 规则 @kb.bpa-trim-object-names 和 @kb.bpa-avoid-invalid-characters-names 会标记带有前导或尾随空格的名称，以及包含控制字符的名称。

### 说明

`Description` · string · 基本

用于说明对象用途的自由文本。 Power BI 会在 **数据** 窗格中将该说明显示为工具提示。 Excel 的数据透视表字段列表不显示描述。要翻译这些描述，请使用 `TranslatedDescriptions`。

在 Tabular Editor 3 中，**TOM Explorer** 有一个 **描述** 列，你可以在这里查看和编辑描述；DAX Code Assist 还会在工具提示中显示表、列或度量值的描述。如果度量值、计算列或计算表格没有描述，工具提示会显示其表达式的前几行。

BPA 规则 @kb.bpa-visible-objects-no-description 会标记没有描述的可见对象，而 @kb.bpa-avoid-invalid-characters-descriptions 会标记包含控制字符的描述。

### 显示文件夹

`DisplayFolder` · 字符串 · 基本

对象在客户端工具字段列表中显示的文件夹。反斜杠（`\\`）会创建子文件夹，例如 `Sales\\Year to date`；分号（`;`）会让对象显示在多个文件夹中，例如 `Sales;Finance`。显示文件夹不会影响 DAX 或安全性。 Tabular Editor 也会用它们在 **TOM Explorer** 中对对象进行分组。

要连同其中的对象和子文件夹一起移动显示文件夹，在 **TOM Explorer** 中将其拖到另一个文件夹上即可。见 @drag-drop。

### 隐藏

`IsHidden` · 布尔值 · 基本

当值为 `true` 时，Power BI 等客户端工具会对 Report 作者隐藏该对象。该对象仍保留在模型中，DAX 表达式仍可引用它。任何能查询该模型的人也都能查询隐藏对象。要保护数据，见 @roles-and-rls。

BPA 规则 @kb.bpa-hide-foreign-keys 会标记关系中“多”侧的可见列。它的自动修复会隐藏这些列。

## 元数据

### 注释

`Annotations` · 名称/值对集合 · 元数据

与对象一同存储的自定义名称/值对。 Analysis Services 和 Power BI 会忽略这些注释，而各类工具会用它们来存储自身信息。例如，Power BI Desktop 会将布局信息存储在注释中，许多 C# Script 和 BPA 规则也会将设置存储在其中。

在 C# Script 中，使用 `GetAnnotation`、`SetAnnotation` 和 `RemoveAnnotation`。请参阅 @how-to-annotations-extended-properties。

### 扩展属性

`ExtendedProperties` · 名称/值对集合 · 元数据

与注释类似的名称/值对，其中值可以是字符串或 JSON 文档。 Power BI 会使用扩展属性，例如用于存储有关参数的查询信息。对于你自己的元数据，请使用注释。

在 C# Script 中，使用 `GetExtendedProperty` 和 `SetExtendedProperty`。

### 已更改的属性

`ChangedPropertiesCollection` · 集合 · 元数据

你在来自其他来源的对象上更改过的属性名称，例如复合模型中的表，或 Power BI 生成的对象。当引擎从源同步该对象时，不会覆盖此列表中的属性。

Tabular Editor 3 不会向此列表添加条目。更改这类属性时，需要你手动添加其名称。输入以逗号分隔的 TOM 属性名称列表，例如 `Name,FormatString`；或者展开该属性，并选中属性名称旁边的复选框。重复项以及不是该对象属性的名称都会被忽略。展开后的列表始终包含 `Name`，以及列表中已有的属性。要清空该列表，右键单击该属性，然后选择 **清除已更改的属性**。

### DAX 标识符

`DaxObjectFullName` · 字符串 · 元数据 · 只读 · _计算得出_

DAX 用于引用该对象的完全限定名称，例如列的 `'Sales'[Amount]`，或度量值的 `[Total Sales]`。 C# Script 会用它来构建 DAX 表达式。请参阅 @how-to-work-with-expressions。

### 错误信息

`ErrorMessage` · 错误信息 · 字符串 · 元数据 · 只读

引擎针对该对象报告的错误，例如 DAX 表达式中的语法错误或分区的刷新错误。如果对象没有错误，该值为空。

在 Tabular Editor 3 中，DAX 表达式的错误也会在你输入时就显示出来，无需等到模型保存到引擎之后。 @messages-view 视图会列出模型中的所有错误和警告。双击一条信息即可转到其对应的对象。

### 对象类型

`ObjectTypeName` · 字符串 · 元数据 · 只读 · _计算所得_

对象的类型，例如 `度量值`、`计算列` 或 `Table`。

### State

`State` · ObjectState · 元数据 · 只读

对象是否已准备好接受查询。该值由引擎设置。

| 值                        | 含义                                           |
| ------------------------ | -------------------------------------------- |
| `Ready`                  | 该对象有效；如果包含数据，则数据也是最新的。                       |
| `NoData`                 | 该对象有效，但尚未包含数据。刷新表或分区。                        |
| `CalculationNeeded`      | 该对象有效，但必须重新计算；例如，计算列在其表达式更改后需要重新计算。          |
| `SemanticError`          | 该表达式引用了不存在的内容，或引用的内容无效。查看 `ErrorMessage` 信息。 |
| `EvaluationError`        | 该表达式本身有效，但在求值时失败。                            |
| `DependencyError`        | 该对象所依赖的某个对象处于错误状态。                           |
| `Incomplete`             | 对象的部分数据缺失，例如某个分区刷新失败时。                       |
| `ForceCalculationNeeded` | 即使对象看起来已是最新状态，也必须重新计算。                       |

只有在连接到服务器或以 @workspace-mode 方式工作时，`State` 才有实际意义。从文件打开的模型不会连接到任何引擎。

在 Tabular Editor 3 中，你可以从 **TOM Explorer** 刷新表，并在 @data-refresh-view 中跟踪进度。

## 选项

### Lineage tag

`LineageTag` · string · 选项 · 兼容级别 1540+

对象的稳定 ID，通常是 GUID。 Power BI 会使用 Lineage tag 在对象重命名时持续跟踪其身份，因此依赖某个列的 Report 或复合模型在该列重命名后仍能正常工作。

Power BI Desktop 会自动分配 Lineage tag。不要更改或复制它们：依赖 Lineage tag 的工具无法区分两个具有相同 Lineage tag 的对象。当 Tabular Editor 在使用 Lineage tag 的模型中创建对象时，它会分配一个新的 Lineage tag。

### 源 Lineage tag

`SourceLineageTag` · string · 选项 · 兼容级别 1550+

此对象所源自的对象的 Lineage tag。构建在其他源之上的模型(例如复合模型或 Direct Lake 模型)会使用它将对象链接到源列或源表。对于 Direct Lake，该值保存 Lakehouse 或 Warehouse 中源列或源表的名称。

Tabular Editor 3 会在导入 Direct Lake 表时设置 `SourceLineageTag`，并在更新 Direct Lake 模型的表架构时，为其新增的列设置该值。对于表，该值是源表的架构和名称，例如 `[dbo].[Sales]`；当源不使用架构时，则为 `[Sales]`。对于列，该值是源列的名称。

## 翻译、透视和安全性

### 翻译后的名称

`TranslatedNames` · 按区域设置 · 翻译、透视和安全性

对象在模型各个区域设置中的名称。客户端工具会显示与用户所用语言相匹配的翻译。如果某个区域设置没有对应翻译，则会显示未翻译的名称。参见 @how-to-work-with-perspectives-translations。

在 Tabular Editor 3 中，@metadata-translation-editor 会并排显示许多对象的翻译名称、说明和显示文件夹。要以 JSON 文件形式与翻译人员交换翻译，参见 @import-export-translations。 BPA 规则 @kb.bpa-translate-visible-names 会标记缺少名称翻译的可见对象。

### 翻译后的描述

`TranslatedDescriptions` · 按区域设置 · 翻译、透视、安全性

模型中该对象在各区域设置下的描述。 BPA 规则 @kb.bpa-translate-descriptions 会标记缺少翻译的描述。

### 翻译后的显示文件夹

`TranslatedDisplayFolders` · 按区域设置 · 翻译、透视、安全性

模型中该对象在每个区域设置下的显示文件夹，使用与 `DisplayFolder` 相同的反斜杠和分号语法。 BPA 规则 @kb.bpa-translate-display-folders 会标记缺少显示文件夹翻译的可见对象。

### 同义词

`Synonyms` · 按区域设置 · 翻译、透视、安全性

用户在自然语言功能中（例如 Power BI 中的 Q&A）为查找该对象而输入的其他词语。表、列、度量值、层次结构和级别都可以设置同义词。它们存储在每个区域设置的语言架构中(请参见 @object-properties-perspectives-cultures 中的 `Content`)。

在 Tabular Editor 3 中，仅当至少有一个区域设置具有 JSON 格式的语言架构时，此属性才会显示。折叠状态下，该属性会显示已定义的语言架构数量。展开后，每个区域设置会显示一条记录，同义词以逗号分隔的列表呈现，例如 `revenue, turnover`。你可以编辑该列表以添加或删除同义词。被删除的同义词会在语言架构中标记为已删除。已删除和建议的同义词不会显示在列表中。

### 在透视中显示

`InPerspective` · 按透视 · 翻译、透视与安全

该对象是否包含在模型的各个透视中。透视会向一组用户展示模型中较小的一部分。与 `IsHidden` 一样，透视不是安全功能。

当你同时选中多个对象时，可以在属性视图中一次性更改它们在透视中的归属。参见 @perspectives-translations。在 Tabular Editor 3 中，@perspective-editor 会以复选框的形式显示所有表、列、层次结构和度量值在各透视中的归属情况。
