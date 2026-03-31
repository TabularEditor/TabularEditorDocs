---
uid: personalizing-te3
title: 根据你的需求个性化定制并配置 Tabular Editor 3
author: Daniel Otykier
updated: 2021-09-28
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

Tabular Editor 3 提供了丰富的配置选项，让你可以根据具体需求和偏好的工作流来调整工具。 本文将带你了解个人模型开发者最常调整的设置。

本文涵盖的大多数设置都可以在 **工具 > 偏好** 菜单中找到。 为便于查阅，本文会用以下格式列出每项设置：

**_设置名称_（默认值）**<br/>设置说明。

> [!TIP]
> 使用“偏好设置”对话框顶部的**搜索框**，即可按名称或关键字快速定位设置。 搜索会实时过滤偏好设置树，帮助你直接跳转到所需设置。

# 常规功能

打开 **偏好** 对话框后，你首先会看到 **Tabular Editor > 功能** 页面（见下方截图）。 下面简要说明此页面上的各项功能，以及它们的常见用途：

![偏好设置：常规功能](~/content/assets/images/pref-general-features.png)

## Power BI

这些设置主要适用于将 Tabular Editor 3 用作 [Power BI Desktop 的外部工具](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-external-tools) 的开发者。

##### _允许执行不受支持的建模操作_（默认禁用）

Power BI Desktop 的外部工具存在一些 [限制](xref:desktop-limitations)。 默认情况下，Tabular Editor 3 会阻止你对 Data model 进行不受支持的更改。 有些高级建模功能虽然在上述链接中标为不受支持，但实际可能仍能正常工作。 要解锁所有 Tabular Object Model 对象和属性，请启用此设置。

##### _隐藏自动日期/时间警告_（已禁用）

当 Power BI Desktop 中的“自动日期/时间”设置启用时，会自动创建多个计算表格。 遗憾的是，这些表格包含的 DAX 代码会触发 Tabular Editor 3 内置的 DAX 分析器警告信息。 要隐藏这些警告，请启用此设置。

##### _DAX 首行换行_（已禁用）

在 Power BI Desktop 中，由于公式栏显示 DAX 代码的方式，通常会在 DAX 表达式的第一行插入换行符。 如果你经常在 Tabular Editor 和 Power BI Desktop 之间来回切换，建议启用此选项，让 Tabular Editor 3 在通过该工具编辑 DAX 表达式时自动插入首行换行符。

## 元数据同步

这些设置用于控制 Tabular Editor 3 在从 Analysis Services 实例上的数据库加载模型元数据时的行为。 这些设置用于指定 Tabular Editor 3 应如何处理从应用程序外部对数据库所做的元数据更改，例如其他用户对数据库进行了更改，或在将 Tabular Editor 3 作为外部工具使用的同时，你通过 Power BI Desktop 对模型进行了更改。

##### _当本地元数据与已部署的模型不同步时发出警告_（已启用）

勾选后，当你尝试保存更改时，如果自从模型元数据加载到你的 Tabular Editor 实例之后，已有其他用户或进程对数据库进行了更改，Tabular Editor 会显示一条警告信息。

##### _跟踪外部模型更改_（已启用）

此选项仅适用于 Analysis Services 的本地实例（即与 Tabular Editor 运行在同一台计算机上的 msmdsrv.exe 进程）。 勾选后，Tabular Editor 会在 Analysis Services 上启动跟踪，并在检测到外部更改时通知你。

##### _自动刷新本地 Tabular Object Model 元数据_（已启用）

当启用上述跟踪机制时，此选项允许 Tabular Editor 在检测到外部更改后自动刷新模型元数据。 如果你经常在 Power BI Desktop 和 Tabular Editor 3 之间来回切换，这会很有用，因为它能确保在 Power BI Desktop 中进行的更改会自动同步到 Tabular Editor。

##### _清理孤立的 Tabular Editor 跟踪_

通常情况下，Tabular Editor 3 会自动停止并移除因上述设置而启动的所有 AS 跟踪。 但是，如果应用程序被提前关闭，这些跟踪可能不会被停止。 点击此按钮后，将移除当前 Analysis Services 实例上由任何 Tabular Editor 实例启动的所有 AS 跟踪。

> [!NOTE]
> 清理按钮仅在 Tabular Editor 连接到 Analysis Services 实例时可用。

# TOM Explorer 设置

以下设置用于控制 TOM Explorer 的各个方面。 你可以在 **Tabular Editor > TOM Explorer** 中找到这些设置：

![Tom Explorer 设置](~/content/assets/images/tom-explorer-settings.png)

##### _显示完整分支_（已禁用）

在筛选 TOM Explorer 时，Tabular Editor 3 默认会显示层级结构中所有匹配筛选字符串的项目，包括它们的父级项目。 如果你也想查看所有子级项目（即使它们可能不匹配筛选字符串），就启用这个选项。

##### _始终显示删除警告_（已禁用）

如果你希望 Tabular Editor 3 在删除任何对象前都提示你确认，请启用此设置。 否则，Tabular Editor 3 只会在删除多个对象或删除被其他对象引用的对象时，提示你确认。

> [!NOTE]
> Tabular Editor 3 中的所有删除操作都可以通过按 CTRL+Z 撤销。

# DAX编辑器常规设置

Tabular Editor 3 的 DAX编辑器可配置项非常丰富，容易让人眼花缭乱。 本节将重点介绍最常用、最重要的设置。 在 **Text Editors > DAX编辑器 > General** 中找到常规设置：

![Dax 编辑器 常规](~/content/assets/images/dax-editor-general.png)

## 常规

_行号_、_代码折叠_、_可见空白字符_ 和 _缩进参考线_ 等设置可用于开启或关闭编辑器的多种 Visual 视觉辅助功能。 在下面的截图中，这四个选项都已启用：

![可见空白字符](~/content/assets/images/visible-whitespace.png)

##### _使用制表符_（已禁用）

勾选此项后，每次按下 TAB 键都会插入一个制表符（`\t`）。 否则，将插入与 _缩进宽度_ 设置对应数量的空格。

##### _注释样式_（斜杠）

DAX 支持使用斜杠（`//`）或连字符（`--`）的行注释。 此设置决定 Tabular Editor 3 在生成 DAX 代码时使用哪种注释样式，例如使用 DAX 脚本功能时。

<a name="dax-settings"></a>

## DAX 设置

这些设置决定 DAX 代码分析器的某些行为。 _Locale_ 区域设置仅是个人偏好问题。 其他设置仅在 Tabular Editor 3 无法确定所使用的 Analysis Services 版本时才适用，例如直接加载 Model.bim 文件时。 在这种情况下，Tabular Editor 会根据模型中指定的兼容级别来推测模型将部署到哪个版本。不过，实际部署目标的版本可能不同，DAX 语言也可能存在各种差异，而这些差异 Tabular Editor 无法确定。 如果 Tabular Editor 错误地报告语义/语法错误，你可能需要微调这些设置。

# 自动格式化

在 **文本编辑器 > DAX编辑器 > 自动格式化** 页面上，你可以找到一系列设置，用于控制 DAX 代码的格式化方式。

![自动格式化设置](~/content/assets/images/auto-formatting-settings.png)

##### _键入时自动格式化代码_（已启用）

该选项会在发生特定按键操作时自动应用某些格式化规则。 例如，当右括号输入完成时，此功能会确保括号内的内容按本页的其他设置进行格式化。

##### _自动格式化函数调用_（已启用）

此选项专门控制是否在右括号输入完成时自动格式化函数调用（即参数与括号之间的空格）。

##### _自动缩进_（已启用）

当在函数调用中插入换行时，此选项会自动缩进函数参数。

##### _自动补全括号_（已启用）

当输入左括号或引号时，此选项会自动插入对应的右括号或引号。

##### _包裹选中内容_（已启用）

启用后，当输入左括号时，此选项会使用对应的右括号自动包裹当前选中内容。

## 格式化规则

这些设置控制 DAX 代码中的空白字符如何格式化：既适用于自动格式化，也适用于手动格式化代码时（使用 **格式化 DAX** 菜单选项）。

##### _函数名后空格_（已禁用）

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

仅在函数调用需要拆分为多行时适用。

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

##### _括号内加空格_（已启用）

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

使用 **格式化 DAX（长行）** 选项时，在表达式被拆分为多行之前，允许单行保留的最大字符数。

##### _短格式行长度限制_（60）

使用 **格式化 DAX（短行）** 选项时，在表达式被拆分为多行之前，允许单行保留的最大字符数。

> [!NOTE]
> 上述大多数设置仅在使用（默认的）内置 DAX 格式化程序时生效。

## 大小写与引号

除了格式化 DAX 代码的空白字符之外，Tabular Editor 3 还可以修正对象引用以及函数/关键字的大小写。

##### _修复度量值/列限定符_（已启用）

勾选后，会自动从度量值引用中移除表前缀，并在列引用中自动插入表前缀。

##### _首选关键字大小写_（默认值：UPPER）

此设置可让你更改关键字的大小写形式，例如 `ORDER BY`、`VAR`、`EVALUATE` 等。 通过自动完成功能插入关键字时也会应用此设置。

##### _首选函数大小写_（默认值：UPPER）

此设置可让你更改函数名称的大小写形式，例如 `CALCULATE(...)`、`SUM(...)` 等。 通过自动完成功能插入函数时也会应用此设置。

##### _修复关键字/函数大小写_（已启用）

勾选后，每当代码被自动格式化或手动格式化时，都会自动更正关键字和函数的大小写。

##### _修复对象引用大小写_（已启用）

DAX 是一种不区分大小写的语言。 启用后，对表、列和度量值的引用会自动更正，使其大小写与所引用对象的实际名称一致。 每当代码自动格式化或手动格式化时，都会执行此修复。

##### _始终为表名加引号_（已禁用）

在 DAX 中引用某些表名时，不需要用单引号括起来。 不过，如果你希望无论表名是什么，引用表时都始终用单引号括起来，可以勾选此选项。

##### _始终为扩展列添加前缀_（已禁用）

扩展列可以在不指定表名的情况下定义。 勾选后，即使表名为空，DAX编辑器也会始终为扩展列添加表前缀。 在这种情况下，列引用将如下所示：`''[Extension Column]`。

# 后续步骤

- @boosting-productivity-te3