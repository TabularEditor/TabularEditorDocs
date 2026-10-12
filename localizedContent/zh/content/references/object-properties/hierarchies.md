---
uid: object-properties-hierarchies
title: 层次结构和级别属性
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

# 层次结构和级别属性

<!--
SUMMARY: Reference for the properties of hierarchies and their levels.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

本页介绍用户定义的层次结构及其级别的属性。有关大多数对象共有的属性，参见 @object-properties-common。

## 层次结构

层次结构是同一张表中按顺序排列并命名的一组列，Report 作者可以在 Visual 和数据透视表中沿着这些列按层级向下钻取，例如 `Year` > `Quarter` > `Month` > `Date` 或 `Category` > `Subcategory` > `Product`。其中每一步都是一个级别。层次结构不会改变数据的存储或计算方式。

层次结构的所有级别都必须来自该层次结构所属的表。若要跨表构建层次结构，首先要将这些列放到同一个表中，例如使用 [RELATED](https://dax.guide/related) 的计算列。

在 **TOM Explorer** 中，把列拖到层次结构上即可向其中添加级别。参见 @drag-drop。

### 通用属性

- [名称](xref:object-properties-common#name)
- [描述](xref:object-properties-common#description)
- [显示文件夹](xref:object-properties-common#display-folder)
- [隐藏](xref:object-properties-common#hidden)
- [注释](xref:object-properties-common#annotations)
- [扩展属性](xref:object-properties-common#extended-properties)
- [已更改的属性](xref:object-properties-common#changed-properties)
- [错误消息](xref:object-properties-common#error-message)
- [对象类型](xref:object-properties-common#object-type)
- [状态](xref:object-properties-common#state)
- [Lineage tag](xref:object-properties-common#lineage-tag)
- [源 Lineage tag](xref:object-properties-common#source-lineage-tag)
- [翻译后的名称](xref:object-properties-common#translated-names)
- [翻译后的描述](xref:object-properties-common#translated-descriptions)
- [翻译后的显示文件夹](xref:object-properties-common#translated-display-folders)
- [同义词](xref:object-properties-common#synonyms)
- [在透视中显示](xref:object-properties-common#shown-in-perspective)

### 隐藏成员

`HideMembers` · HierarchyHideMembersType · 选项 · 兼容级别 1400+

指定客户端工具是否隐藏值为空的成员。将其用&#x4E8E;_&#x4E0D;平&#x8861;_&#x5C42;次结构，即某些分支的层级比其他分支更少。例如，在地理层次结构 `Country` > `State` > `City` 中，有些国家没有州，而使用 `Default` 时，用户会在国家与其城市之间的 `State` 级别看到一个空成员。**属性**视图会在兼容级别为 1400 或更高时显示 `HideMembers`。

| 值                  | 含义                              |
| ------------------ | ------------------------------- |
| `Default`          | 显示所有成员，包括空白成员。将其用于平衡层次结构。       |
| `HideBlankMembers` | 当成员的值为空白时隐藏该成员，并让其子成员直接显示在父成员下。 |

仅隐藏空白成员，`N/A` 之类的占位符值仍会显示。 Excel 会遵循此属性。 Power BI 会忽略此属性，并显示空白成员。

<!-- TODO (not verifiable from TE3 source): whether the engine treats an empty string as blank (Excel hiding real BLANK() members is confirmed on SSAS 2025). -->

## 级别

级别是层次结构中的一个层级。每个级别都指向该层次结构所属表中的一列，并且有自己的名称，该名称可以不同于列名。例如，名为 `Month` 的级别可以指向名为 `MonthName` 的列。

### 通用属性

- [名称](xref:object-properties-common#name)
- [描述](xref:object-properties-common#description)
- [注解](xref:object-properties-common#annotations)
- [扩展属性](xref:object-properties-common#extended-properties)
- [已更改的属性](xref:object-properties-common#changed-properties)
- [对象类型](xref:object-properties-common#object-type)
- [Lineage tag](xref:object-properties-common#lineage-tag)
- [源 Lineage tag](xref:object-properties-common#source-lineage-tag)
- [翻译后的名称](xref:object-properties-common#translated-names)
- [翻译后的描述](xref:object-properties-common#translated-descriptions)
- [同义词](xref:object-properties-common#synonyms)

级别本身不具备 `IsHidden` 或 `DisplayFolder` 属性，而是在透视中沿用其所属层次结构的设置。如果翻译了层次结构的名称，也请同时翻译其各级别的名称。 Best Practice Analyzer (BPA) 规则 @kb.bpa-translate-hierarchy-levels 会标记可见层次结构中在模型的一个或多个区域设置中没有翻译名称的级别。

### 列

`Column` · 列 · 基本

提供该级别值的列。它必须是与该层次结构位于同一表中的列，并且同一列在同一层次结构中只能使用一次。该级别会按列的排序顺序显示该列的值。若要按日历顺序显示月份，请在月份名称列上设置 `SortByColumn`（请参阅 @object-properties-columns）。

隐藏列在层次结构中仍然可用。隐藏级别列，让用户通过层次结构浏览数据。

### 序号

`Ordinal` · int · 基本

该级别在层次结构中的位置，顶层级别从 `0` 开始计。层次结构中各级别的序号必须为 `0`、`1`、`2` 等，不能有间断或重复。

Tabular Editor 3 会自动维护层级序号：

- 当你在 **TOM Explorer** 中拖动级别以调整顺序时，Tabular Editor 会重新为该层次结构中的所有级别编号
- 当你删除某个级别时，Tabular Editor 会对其余级别重新编号，以补上空缺
- 当你在 **属性** 视图中输入新的 `Ordinal` 时，Tabular Editor 会将该级别移动到相应位置，并重新编号其他级别
- 当你添加级别时，它会默认出现在层次结构底部；但如果你将该列拖放到两个现有级别之间，则会插入到两者之间

你一次只能为一个级别设置 `Ordinal`。 Tabular Editor 2 在你拖动级别调整顺序或删除级别时，也会以同样的方式重新编号级别序号。

你还可以将级别拖到同一表中的另一个层次结构上，将其移动到那里。参见 @drag-drop。
