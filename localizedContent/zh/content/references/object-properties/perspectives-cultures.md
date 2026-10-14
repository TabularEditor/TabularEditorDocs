---
uid: object-properties-perspectives-cultures
title: 透视和区域设置属性
author: Jeroen ter Heerdt
updated: 2026-10-09
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

# 透视和区域设置属性

<!--
SUMMARY: Reference for the properties of perspectives and cultures (translations), including linguistic metadata and translation statistics.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

本页介绍透视和区域设置的属性。有关大多数对象共有的属性，参见 @object-properties-common。

要添加或删除透视和区域设置，请使用模型上的 **透视** 和 **区域设置** 集合（参见 @object-properties-model），或在 **TOM Explorer** 中右键单击 **透视** 或 **翻译** 文件夹。 Tabular Editor 2 中的文件夹名称也相同。参见 @perspectives-translations。要使用 C# Script 创建和更改透视和区域设置，请参见 @how-to-work-with-perspectives-translations。

## 透视

透视是模型的一个命名子集：为某一组用户选取的一组表、列、度量值和层次结构。例如，`Sales` 透视只显示销售团队需要的对象。在支持透视的客户端工具(如 Excel)中，用户可以选择一个透视，并且只会看到其中的对象。 Power BI Report 作者无法在字段列表中选择透视，但你可以在通过 XMLA endpoint 连接到模型时，或在个性化的 Visual 中使用透视。

在 Power BI 服务中，你可以通过 XMLA endpoint 连接到某个透视，方法是在连接字符串中添加 `Cube=<perspective name>`。这只会更改架构信息中列出的对象，而 DAX 查询仍然可以使用模型中的每个表和度量值。

<!-- TODO (not verifiable from TE3 source): whether personalized visuals in the Power BI service still use perspectives. -->

> [!NOTE]
> 透视不会限制访问。无论用户使用哪个透视，都可以查询模型中的每个对象。要限制访问，请使用 @roles-and-rls。

除通用属性外，透视本身没有其他属性。你可以在各个对象上通过 `InPerspective` 指定其是否包含在该透视中（参见[在透视中显示](xref:object-properties-common#shown-in-perspective)）；或者在 Tabular Editor 3 中，在 @perspective-editor 里一次性为多个对象设置。

Best Practice Analyzer (BPA) 规则 @kb.bpa-perspectives-no-objects 会标记不包含任何表的透视，而 @kb.bpa-translate-perspectives 会标记名称未在每个区域设置中翻译的透视。

### 常用属性

- [名称](xref:object-properties-common#name)
- [描述](xref:object-properties-common#description)
- [注释](xref:object-properties-common#annotations)
- [扩展属性](xref:object-properties-common#extended-properties)
- [对象类型](xref:object-properties-common#object-type)
- [翻译名称](xref:object-properties-common#translated-names)
- [翻译描述](xref:object-properties-common#translated-descriptions)

## 区域设置

一个区域设置保存模型针对某种语言的翻译：其对象的翻译名称、描述和显示文件夹，以及该语言的语言元数据。客户端工具会显示与用户语言设置匹配的区域设置；如果没有匹配的区域设置，则显示未翻译的名称。

区域设置的 `Name` 是区域设置代码，例如 `da-DK` 或 `fr-FR`。它必须是有效的区域设置名称，并且每个区域设置在模型中只能出现一次。在 Tabular Editor 3 中，**属性**视图会将其标记为 **语言**，并列出可供选择的区域设置。

翻译可在各个对象上通过 `TranslatedNames`、`TranslatedDescriptions` 和 `TranslatedDisplayFolders` 进行编辑；或者在 Tabular Editor 3 中，通过 @metadata-translation-editor 一次性编辑多个对象。若要与翻译人员交换翻译内容，请参见 @import-export-translations。

翻译统计属性会按对象类型显示模型在此区域设置中的翻译完成情况。这些值由 Tabular Editor 计算，不会存储在模型中。每个值都采用 `12 of 40` 这种格式，表示模型中该类型对象已翻译的数量与该类型对象的总数之比，包括隐藏对象。对于名称，只有当翻译不为空且不同于对象的未翻译名称时，才会计入统计。要查找缺少翻译的对象，请使用 BPA 规则 @kb.bpa-translate-visible-names、@kb.bpa-translate-descriptions 和 @kb.bpa-translate-display-folders。

### 常用属性

- [名称](xref:object-properties-common#name)
- [注释](xref:object-properties-common#annotations)
- [扩展属性](xref:object-properties-common#extended-properties)
- [对象类型](xref:object-properties-common#object-type)

### Altered

`Altered` · bool（混合状态时为空）· 基本 · 兼容级别 1571+ · _快捷方式_：指向该区域设置中每个翻译的 **Altered** 标志

区域设置中的每个翻译在 Tabular Object Model (TOM) 中都带有一个 _altered_ 标志，翻译工具用它来标记人工已审核或已更改的翻译。此属性汇总了该区域设置中所有翻译的标志状态：

- `true`：每条翻译都已设置该标志
- `false`：没有任何翻译设置了该标志
- 空值：部分翻译设置了该标志，部分未设置

将其设为 `true` 或 `false`，即可一次性为该区域设置中的所有翻译设置或清除此标志。**属性**视图会在兼容级别 1571 及以上时显示此属性。

> [!WARNING]
> 你无法撤销对 `Altered` 的更改。

该标志不会保存在模型文件中。 Microsoft 的 TOM 库不会将它写入 Tabular Model Scripting Language (TMSL)（涵盖 `.bim` 文件、JSON 格式的文件夹和部署脚本），也不会写入 Tabular Model Definition Language (TMDL)。当你将模型保存到文件并再次打开时，该标志会丢失。

如果你通过与服务器的实时连接来设置该标志，服务器会保留它。在 SQL Server 2025 Analysis Services 上，它在重新连接后仍会保留，并会显示在 `TMSCHEMA_OBJECT_TRANSLATIONS` 翻译 DMV 中。即使如此，从该服务器生成的 TMSL 脚本仍不会包含它，因此模型一旦保存到文件或从文件部署，该标志就会丢失。

<!-- TODO (not verifiable from TE3 source): confirm which tools set and read the Altered flag. -->

### 内容

`Content` · string · 语言元数据 · 兼容级别 1465+

区域设置的语言架构：Power BI Q&A 在停用前使用的自然语言元数据。其中包含表、列和度量值的同义词，以及用于描述对象关系的表述，例如客户购买产品。每个对象上的 `Synonyms` 属性会读取和写入此处存储的同义词。

该内容是一个大型 JSON 或 XML 文档，具体取决于 `ContentType`，并由 Power BI Desktop 负责维护。兼容级别为 1465 或更高时，**属性**视图会显示此属性。

在 Tabular Editor 3 中，选择该属性上的 **...**，即可在多行文本编辑器中编辑内容。 Tabular Editor 不会验证文档，并会根据第一个字符设置 `ContentType`：以 `{` 开头的内容为 JSON，其他任何内容均为 XML。清除内容会从区域设置中移除语言元数据。 Tabular Editor 仅从 JSON 内容中读取和写入 `Synonyms`。

### 内容类型

`ContentType` · ContentType · 语言元数据 · 只读 · 兼容级别 1465+

`Content` 的格式。对于由 Power BI 创建的模型，为 `Json`；对于旧格式，则为 `Xml`。当区域设置没有语言元数据时，该属性为空。编辑 `Content` 时，Tabular Editor 会设置该值。兼容级别为 1465 或更高时，**属性**视图会显示此属性。

### 已翻译的表名

`StatsTableCaptions` · string · 翻译统计 · 只读 · _计算得出_

已翻译的表名数量。

### 已翻译的列名

`StatsColumnCaptions` · string · 翻译统计 · 只读 · _计算得出_

已翻译的列名数量。

### 已翻译的列显示文件夹

`StatsColumnDisplayFolders` · string · 翻译统计 · 只读 · _计算得出_

已翻译的列显示文件夹数量。总数是模型中的列数，包括没有显示文件夹的列，因此即使每个显示文件夹都已翻译，第一个数字通常也会小于第二个数字。

### 已翻译的度量值名

`StatsMeasureCaptions` · string · 度量值翻译统计 · 只读 · _计算得出_

已翻译的度量值名数量。

### 已翻译的度量值显示文件夹

`StatsMeasureDisplayFolders` · 字符串 · 度量值翻译统计 · 只读 · _计算得出_

已翻译的度量值显示文件夹数量。总数为模型中的度量值数量，包括没有显示文件夹的度量值。

### 已翻译的层次结构名称

`StatsHierarchyCaptions` · 字符串 · 翻译统计 · 只读 · _计算得出_

已翻译的层次结构名称数量。

### 已翻译的层次结构显示文件夹

`StatsHierarchyDisplayFolders` · 字符串 · 翻译统计 · 只读 · _计算得出_

已翻译的层次结构显示文件夹数量。总数为模型中的层次结构数量，包括没有显示文件夹的层次结构。

### 已翻译的级别名称

`StatsLevelCaptions` · 字符串 · 翻译统计 · 只读 · _计算得出_

已翻译的层次结构级别名称数量。 BPA 规则 @kb.bpa-translate-hierarchy-levels 会标记可见层次结构中名称尚未翻译的级别。
