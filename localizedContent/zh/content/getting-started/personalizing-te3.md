---
uid: personalizing-te3
title: 根据你的需求个性化定制并配置 Tabular Editor 3
author: Daniel Otykier
updated: 2026-09-14
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 根据你的需求个性化定制并配置 Tabular Editor 3

Tabular Editor 3 提供了丰富的配置选项，让你可以根据具体需求和偏好的工作流来调整工具。 In this article, we will guide you through the settings that are most commonly adjusted by individual model developers.

本文涵盖的大多数设置都可以在 **工具 > 偏好** 菜单中找到。 Throughout the article, we will list individual settings in the following style, for easy reference:

**_设置名称_（默认值）**<br/>设置说明。

> [!TIP]
> Use the **search box** at the top of the Preferences dialog to quickly locate settings by name or keyword. The search filters the preferences tree in real-time, helping you navigate directly to the setting you need.

# 常规功能

打开 **偏好** 对话框后，你首先会看到 **Tabular Editor > 功能** 页面（见下方截图）。 Below is a short description of the features on this page, and what they are commonly used for:

![偏好设置：常规功能](~/content/assets/images/pref-general-features.png)

## Power BI

这些设置主要适用于将 Tabular Editor 3 用作 [Power BI Desktop 的外部工具](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-external-tools) 的开发者。

##### _允许执行不受支持的建模操作_（默认禁用）

External Tools for Power BI Desktop have some [limitations](xref:desktop-limitations). By default, Tabular Editor 3 will prevent the user from making unsupported changes to the data model. There may be some advanced modeling features which work well, even though they are not supported cf. the previous link. To unlock all Tabular Object Model objects and properties, enable this setting.

##### _隐藏自动日期/时间警告_（已禁用）

当 Power BI Desktop 中的“自动日期/时间”设置启用时，会自动创建多个计算表格。 Unfortunately, these tables contain DAX code which trigger a warning message by Tabular Editor 3's built-in DAX analyzer. To hide these warnings, enable this setting.

##### _DAX 首行换行_（已禁用）

在 Power BI Desktop 中，由于公式栏显示 DAX 代码的方式，通常会在 DAX 表达式的第一行插入换行符。 If you often switch back and forth between Tabular Editor and Power BI Desktop, consider enabling this option to have Tabular Editor 3 insert the line break automatically, whenever a DAX expression is edited through the tool.

## 元数据同步

These settings controls the behavior of Tabular Editor 3, when model metadata is loaded from a database on an instance of Analysis Services. 这些设置用于指定 Tabular Editor 3 应如何处理从应用程序外部对数据库所做的元数据更改，例如其他用户对数据库进行了更改，或在将 Tabular Editor 3 作为外部工具使用的同时，你通过 Power BI Desktop 对模型进行了更改。

##### _当本地元数据与已部署的模型不同步时发出警告_（已启用）

勾选后，当你尝试保存更改时，如果自从模型元数据加载到你的 Tabular Editor 实例之后，已有其他用户或进程对数据库进行了更改，Tabular Editor 会显示一条警告信息。

##### _跟踪外部模型更改_（已启用）

此选项仅适用于 Analysis Services 的本地实例（即与 Tabular Editor 运行在同一台计算机上的 msmdsrv.exe 进程）。 When checked, Tabular Editor starts a trace on Analysis Services and notifies you if external changes are made.

##### _自动刷新本地 Tabular Object Model 元数据_（已启用）

When the tracing mechanism as described above is enabled, this option allows Tabular Editor to automatically refresh the model metadata when an external change is detected. 如果你经常在 Power BI Desktop 和 Tabular Editor 3 之间来回切换，这会很有用，因为它能确保在 Power BI Desktop 中进行的更改会自动同步到 Tabular Editor。

##### _清理孤立的 Tabular Editor 跟踪_

通常，Tabular Editor 3 会自动停止并移除因上述设置而启动的所有 AS 跟踪。 However, if the application was shut down prematurely, the traces may never be stopped. 点击此按钮后，将移除当前 Analysis Services 实例上由任何 Tabular Editor 实例启动的所有 AS 跟踪。

> [!NOTE]
> 清理按钮仅在 Tabular Editor 连接到 Analysis Services 实例时可用。

# TOM Explorer 设置

The settings below control various aspects of the TOM Explorer. 你可以在 **Tabular Editor > TOM Explorer** 中找到这些设置：

![Tom Explorer Settings](~/content/assets/images/unsaved-changes/preferences.png)

##### _显示完整分支_（已禁用）

在筛选 TOM Explorer 时，Tabular Editor 3 默认会显示层级结构中所有匹配筛选字符串的项目，包括它们的父级项目。 If you want to see all child items as well (even though these might not match the filter string), enable this option.

##### _始终显示删除警告_（已禁用）

If you prefer Tabular Editor 3 to prompt you to confirm all object deletions, enable this setting. 否则，Tabular Editor 3 只会在删除多个对象或删除被其他对象引用的对象时，提示你确认。

> [!NOTE]
> Tabular Editor 3 中的所有删除操作都可以通过按 CTRL+Z 撤销。

# DAX编辑器常规设置

Tabular Editor 3 的 DAX编辑器可配置项非常丰富，容易让人眼花缭乱。 This section highlights the most common and important settings. Locate the general settings under **Text Editors > DAX Editor > General**:

![Dax 编辑器 常规](~/content/assets/images/dax-editor-general.png)

## 常规

_行号_、_代码折叠_、_可见空白字符_ 和 _缩进参考线_ 等设置可用于开启或关闭编辑器的多种 Visual 视觉辅助功能。 In the screenshot below, all four options have been enabled:

![可见空白字符](~/content/assets/images/visible-whitespace.png)

##### _使用制表符_（已禁用）

When this is checked, a tab character (`\t`) is inserted whenever the TAB button is hit. Otherwise, a number of spaces corresponding to the _Indent width_ setting is inserted.

##### _注释样式_（斜杠）

DAX 支持使用斜杠（`//`）或连字符（`--`）的行注释。 This setting determines which style of comment is used when Tabular Editor 3 generates DAX code, such as when using the DAX script feature.

## DAX 设置

These settings determine certain behavior of the DAX code analyzer. The _Locale_ setting is simply a matter of preference. All other settings are relevant only when Tabular Editor 3 cannot determine the version of Analysis Services used, as is the case for example when a Model.bim file is loaded directly. In this case, Tabular Editor tries to guess which version the model will be deployed to, based on the compatibility level specified in the model, but depending on the actual version of the deployment target, there may be various DAX language differences, which Tabular Editor cannot determine. If Tabular Editor reports incorrect semantic/syntax errors, you may need to tweak these settings.

# 自动格式化

在 **文本编辑器 > DAX编辑器 > 自动格式化** 页面上，你可以找到一系列设置，用于控制 DAX 代码的格式化方式。

![自动格式化设置](~/content/assets/images/auto-formatting-settings.png)

##### _输入时自动格式化代码_（已启用）

这个选项会在发生某些按键操作时，自动应用特定的格式规则。 For example, when a parenthesis is closed, this feature will ensure that everything within the parentheses is formatted according to the other settings on this page.

##### _自动格式化函数调用_（已启用）

此选项专门控制是否在右括号输入完成时自动格式化函数调用（即参数与括号之间的空格）。

##### _自动缩进_（已启用）

这个选项会在函数调用内插入换行时，自动缩进函数参数。

##### _Auto-brace_ (enabled)

当输入左括号或引号时，此选项会自动插入对应的右括号或引号。

##### _Wrap selection_ (enabled)

When enabled, this option automatically wraps the current selection with the closing brace, when an opening brace is entered.

## 格式化规则

这些设置控制 DAX 代码中的空白字符如何格式化：既适用于自动格式化，也适用于手动格式化代码时（使用 **格式化 DAX** 菜单选项）。

##### _函数后加空格_（已禁用）

# [已启用](#tab/tab1)

```DAX
SUM ( 'Sales'[Amount] )
```

# [已禁用](#tab/tab2)

```DAX
SUM( 'Sales'[Amount] )
```

***

##### _函数后换行_（已禁用）

仅在函数调用需要拆分为多行时生效。

# [已启用](#tab/tab3)

```DAX
SUM
(
    'Sales'[Amount]
)
```

# [已禁用](#tab/tab4)

```DAX
SUM(
    'Sales'[Amount]
)
```

***

##### _运算符前换行_（已启用）

仅在二元运算需要拆分为多行时适用。

# [已启用](#tab/tab5)

```DAX
[Internet Total Sales]
    + [Reseller Total Sales]
```

# [已禁用](#tab/tab6)

```DAX
[Internet Total Sales] +
    [Reseller Total Sales]
```

***

##### _Pad parentheses_ (enabled)

# [已启用](#tab/tab7)

```DAX
SUM( Sales[Amount] )
```

# [已禁用](#tab/tab8)

```DAX
SUM(Sales[Amount])
```

***

##### _长格式行长度限制_（120）

在使用 **格式化 DAX（长行）** 选项时，表达式在被拆分为多行之前，单行可保留的最大字符数。

##### _短格式行长度限制_（60）

使用 **Format DAX (short lines)** 选项时，表达式在拆分为多行之前，每行最多保留的字符数。

> [!NOTE]
> 上述大多数设置仅在使用（默认的）内置 DAX 格式化程序时生效。

## Casings and quotes

除了格式化 DAX 代码的空白字符外，Tabular Editor 3 还可以修正对象引用，以及函数/关键字的大小写。

##### _修正度量值/列限定符_（已启用）

勾选后，会自动从度量值引用中移除表前缀，并在列引用中自动插入表前缀。

##### _首选关键字大小写_（默认值：UPPER）

此设置可让你更改关键字的大小写形式，例如 `ORDER BY`、`VAR`、`EVALUATE` 等。 This also applies when a keyword is inserted through the auto-complete feature, including the fixed keyword values of functions that take them. See @preferences for the full list.

##### _首选函数大小写_（默认值：UPPER）

此设置可让你更改函数名称的大小写形式，例如 `CALCULATE(...)`、`SUM(...)` 等。 This also applies when a function is inserted through the auto-complete feature.

##### _修正关键字/函数大小写_（已启用）

勾选后，每当代码被自动格式化或手动格式化时，都会自动更正关键字和函数的大小写。

##### _修正对象引用大小写_（已启用）

DAX is a case-insensitive language. When this is enabled, references to tables, columns and measures are automatically corrected such that the casing matches the physical name of the referenced objects. This fixup happens whenever code is auto-formatted or manually formatted.

##### _始终为表名加引号_（已禁用）

在 DAX 中，引用某些表名时不需要用单引号括起来。 However, if you prefer table references to always be quoted, regardless of the table name, you can check this option.

##### _扩展列始终加前缀_（已禁用）

Extension columns can be defined without a table name. 勾选后，即使表名为空，DAX编辑器也会始终为扩展列添加表前缀。 In that case, the column reference will look like `''[Extension Column]`.

# 后续步骤

- @boosting-productivity-te3