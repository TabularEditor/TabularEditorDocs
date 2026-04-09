---
uid: code-actions
title: 代码操作
author: Daniel Otykier
updated: 2024-10-30
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.18.0
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 代码操作

Tabular Editor 3.18.0 引入了一项名为 **代码操作** 的新功能。 此功能默认启用，但可在 **工具 > 偏好** 对话框中，于 **文本编辑器 > DAX编辑器 > 代码操作** 下将其禁用。 此功能默认启用，但可在 **工具 > 偏好** 对话框中，于 **文本编辑器 > DAX编辑器 > 代码操作** 下将其禁用。

代码操作是一项提升效率的功能，会在不打断你工作的情况下提供改进 DAX 代码的建议。 单击即可应用这些建议。 代码操作还可让你快速访问常用的代码重构操作。 单击即可应用这些建议。 代码操作还可让你快速访问常用的代码重构操作。

代码操作分为三类：

1. **改进**：这些是围绕以下方面改进 DAX 代码的推荐建议：
   - 遵循最佳实践
   - 避免常见陷阱和反模式
   - 避免使用过时或已弃用的 DAX 功能
   - 编写更优、更高性能的 DAX 代码
2. **可读性**：这些是让你的 DAX 代码更易读的建议，方法包括……
   - 在可能的情况下简化复杂表达式
   - 删除冗余或不必要的代码
   - 应用一致的格式和命名规范
3. **重写**：这些是用于重构你的 DAX 代码的建议。 它们未必是改进，但在进行较大规模的代码重构时通常很有用。 例如： 它们未必是改进，但在进行较大规模的代码重构时通常很有用。 例如：
   - 将 DAX “语法糖”改写为更冗长但更明确的显式代码
   - 重命名变量或扩展列的所有实例
   - 格式化代码

## 如何使用代码操作

新增了一个命令及其对应的工具栏/菜单按钮 **显示代码操作**，默认键盘快捷键为 `Ctrl+.`。 该命令会在当前光标位置显示适用的代码操作： 该命令会在当前光标位置显示适用的代码操作：

![代码操作调用菜单](~/content/assets/images/features/code-action-invoke-menu.png)

你也可以通过右键上下文菜单中的 **重构** 子菜单找到适用的代码操作：

![代码操作重构子菜单](~/content/assets/images/features/code-action-refactor-submenu.png)

最后，当光标放在具有可用操作的代码分段上时，编辑器左侧边距会显示一个灯泡或螺丝刀图标。 点击该图标也会打开代码操作菜单： 点击该图标也会打开代码操作菜单：

![代码操作边距](~/content/assets/images/features/code-action-margin.png)

当你将鼠标指针悬停在代码操作菜单中的某个操作上时，工具提示会显示该操作的更多信息。 点击“了解更多”链接，即可查看该操作对应的知识库 (KB) 文章。 点击“了解更多”链接，即可查看该操作对应的知识库 (KB) 文章。

![代码操作工具提示](~/content/assets/images/features/code-action-tooltip.png)

## 代码操作指示器

**改进**和**可读性**类代码操作也会在代码编辑器中以可视化方式标记。 这能让你快速判断代码的哪些部分可以改进或提升可读性。 这能让你快速判断代码的哪些部分可以改进或提升可读性。

- **改进** 会在代码分段开头的前几个字符下方显示橙色圆点（除非该代码分段已显示橙色的警告波浪线）。 当光标移动到代码分段上时，左侧边距会出现一个_灯泡_图标。 当光标移动到代码分段上时，左侧边距会出现一个_灯泡_图标。
- **可读性**操作会在代码分段开头的前几个字符下方显示青绿色圆点。 当光标移到代码分段上时，左侧边距会显示一个_螺丝刀_图标。 当光标移到代码分段上时，左侧边距会显示一个_螺丝刀_图标。
- 代码本身不会在视觉上直接标示出 **重写**；不过，当光标放在包含可用重写的代码分段上时，左侧边距会显示 _螺丝刀_ 图标。

## 应用到所有出现位置

有些代码操作可以应用到当前 DAX 表达式、DAX 脚本或 DAX 查询中的所有出现位置，而不仅仅是光标所在的代码分段。 在这种情况下，代码操作会显示在“代码操作”菜单中，并在操作说明后追加 " (所有出现位置)"。 点击该操作会将更改应用到文档中的所有出现位置。 在这种情况下，代码操作会显示在“代码操作”菜单中，并在操作说明后追加 " (所有出现位置)"。 点击该操作会将更改应用到文档中的所有出现位置。

例如在下面的截图中，**为变量添加 '_' 前缀** 操作可以应用到文档中的所有出现位置（即所有变量），而不只是光标下的 `totalSales` 变量：

![代码操作：所有出现位置](~/content/assets/images/features/code-action-all-occurrences.png)

<a name="list-of-code-actions"></a>

## 代码操作列表

下表列出了当前所有可用的代码操作。 你可以在 **工具 > 偏好设置** 对话框的 **文本编辑器 > DAX编辑器 > 代码操作** 下关闭代码操作（未来更新将允许你单独切换各项操作，以获得更个性化的体验）。 部分代码操作还提供额外的配置选项，例如变量名要使用哪个前缀。

### 改进

当光标放在代码分段上时，下列代码操作会在适用代码的前两个字符下方显示橙色圆点，并在左侧边距显示一个灯泡图标：

| ID    | 名称                                   | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ----- | ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DI001 | [删除未使用的变量](xref:DI001)               | 未在任何位置被引用的变量应当删除。 示例：<br>`VAR a = 1 VAR b = 2 RETURN a` -> `VAR a = 1 RETURN a` 示例：<br>`VAR a = 1 VAR b = 2 RETURN a` -> `VAR a = 1 RETURN a`                                                                                                                                                                                                                                                                                                                                                       |
| DI002 | [删除所有未使用的变量](xref:DI002)             | 在变量块的 `RETURN` 部分未被使用的变量（无论是直接使用，还是通过其他变量间接使用）都应删除。 示例：<br>`VAR a = 1 VAR b = a RETURN 123` -> `123` 示例：<br>`VAR a = 1 VAR b = a RETURN 123` -> `123`                                                                                                                                                                                                                                                                                                                                               |
| DI003 | [移除表名](xref:DI003)                   | 度量值引用不应包含表名，因为引用度量值时无需表名。 此外，这种做法还能让度量值引用更容易与列引用区分开来。 示例：<br>`Sales[Total Sales]` -> `[Total Sales]`                                                                                                                                                                                                                                                                                                                                                                                                |
| DI004 | [添加表名](xref:DI004)                   | 列引用应包含表名，以避免歧义，并更容易将列引用与度量值引用区分开来。 示例：<br>`SUM([SalesAmount])` -> `SUM(Sales[SalesAmount])` 示例：<br>`SUM([SalesAmount])` -> `SUM(Sales[SalesAmount])`                                                                                                                                                                                                                                                                                                                                                |
| DI005 | [将表筛选重写为标量谓词](xref:DI005)            | DAX 中一个常见的反模式是：在 [`CALCULATE`](https://dax.guide/CALCULATE) 的筛选参数中对一个表进行筛选，而实际上只需筛选该表中的一个或多个列即可。 示例：<br>`CALCULATE([Total Sales], FILTER(Products, Products[Color] = "Red"))` -> `CALCULATE([Total Sales], KEEPFILTERS(Products[Color] = "Red"))`<br>此代码操作支持原始表达式的多种变体。 示例：<br>`CALCULATE([Total Sales], FILTER(Products, Products[Color] = "Red"))` -> `CALCULATE([Total Sales], KEEPFILTERS(Products[Color] = "Red"))`<br>此代码操作支持原始表达式的多种变体。                                                      |
| DI006 | [将多列筛选拆分为多个筛选](xref:DI006)           | 当使用 `AND` (或等效的 `&&` 运算符) 将表在多个列上的筛选组合在一起时，通常可以通过为每一列分别指定一个筛选来获得更好的性能。 示例：<br>`CALCULATE(..., Products[Color] = "Red" && Products[Size] = "Large")` -> `CALCULATE(..., Products[Color] = "Red", Products[Size] = "Large")`                                                                                                                                                                                                                                                       |
| DI007 | [简化 SWITCH 语句](xref:DI007)           | 当 [`SWITCH`](https://dax.guide/SWITCH) 语句将 **&lt;Expression&gt;** 参数指定为 `TRUE()`，且所有 **&lt;Value&gt;** 参数都是对同一变量/度量值的简单比较时，该语句可以被简化。 示例：<br>`SWITCH(TRUE(), a = 1, ..., a = 2, ...)` -> `SWITCH(a, 1, ..., 2, ...)` 示例：<br>`SWITCH(TRUE(), a = 1, ..., a = 2, ...)` -> `SWITCH(a, 1, ..., 2, ...)`                                                                                                                  |
| DI008 | [移除多余的 CALCULATE](xref:DI008)        | 应移除不必要的 [`CALCULATE`](https://dax.guide/CALCULATE) 函数：因为它不会修改筛选语境，或因为即使不写也会发生隐式语境转换。 应移除不必要的 [`CALCULATE`](https://dax.guide/CALCULATE) 函数：因为它不会修改筛选语境，或因为即使不写也会发生隐式语境转换。 示例：<br>`CALCULATE([Total Sales])` -> `[Total Sales]`<br>`AVERAGEX(Product, CALCULATE([Total Sales]))` -> `AVERAGEX(Product, [Total Sales])`<br><br>当 `CALCULATE` / `CALCULATETABLE` 的第一个参数是 DAX 变量时同样适用，例如：<br>`VAR x = [Total Sales] RETURN CALCULATE(x, Product[Color] = "Red")` -><br>`VAR x = [Total Sales] RETURN x` |
| DI009 | [避免使用 CALCULATE 简写语法](xref:DI009)    | 示例：<br>`[Total Sales](Products[Color] = "Red")` -> `CALCULATE([Total Sales], Products[Color] = "Red")`                                                                                                                                                                                                                                                                                                                                                                                              |
| DI010 | [用 MIN/MAX 替代 IF](xref:DI010)        | 当条件表达式用于返回两个值中的最小值或最大值时，使用 [`MIN`](https://dax.guide/MIN) 或 [`MAX`](https://dax.guide/MAX) 函数会更高效、更简洁。 示例：<br>`IF(a > b, a, b)` -> `MAX(a, b)` 示例：<br>`IF(a > b, a, b)` -> `MAX(a, b)`                                                                                                                                                                                                                                                                                                              |
| DI011 | [用 ISEMPTY 替代 COUNTROWS](xref:DI011) | 检查表是否为空时，使用 [`ISEMPTY`](https://dax.guide/ISEMPTY) 比统计表的行数更高效。 示例：<br>`COUNTROWS(Products) = 0` -> `ISEMPTY(Products)` 示例：<br>`COUNTROWS(Products) = 0` -> `ISEMPTY(Products)`                                                                                                                                                                                                                                                                                                                      |
| DI012 | [用 DIVIDE 替代除法运算符](xref:DI012)       | 当除法的分母是任意表达式时，请使用 [`DIVIDE`](https://dax.guide/DIVIDE) 而不是除法运算符，以避免除以零的错误。 示例：<br>`x / y` -> `DIVIDE(x, y)` 示例：<br>`x / y` -> `DIVIDE(x, y)`                                                                                                                                                                                                                                                                                                                                                        |
| DI013 | [使用除法运算符而不是 DIVIDE](xref:DI013)      | 当 [`DIVIDE`](https://dax.guide/DIVIDE) 的第二个参数是非零常量时，使用除法运算符更高效。 示例：<br>`DIVIDE(x, 2)` -> `x / 2` 示例：<br>`DIVIDE(x, 2)` -> `x / 2`                                                                                                                                                                                                                                                                                                                                                                   |
| DI014 | [用 DIVIDE 替换 IFERROR](xref:DI014)    | 当除法的分母为零时，请使用 [`DIVIDE`](https://dax.guide/DIVIDE) 函数替代 [`IFERROR`](https://dax.guide/IFERROR)，从而返回替代结果。 示例：<br>`IFERROR(x / y, 0)` -> `DIVIDE(x, y, 0)` 示例：<br>`IFERROR(x / y, 0)` -> `DIVIDE(x, y, 0)`                                                                                                                                                                                                                                                                                            |
| DI015 | [用 DIVIDE 替换 IF](xref:DI015)         | 使用 [`DIVIDE`](https://dax.guide/DIVIDE) 函数代替 [`IF`](https://dax.guide/IF)，可以更方便地检查分母是否为零或空白。 示例：<br>`IF(y <> 0, x / y)` -> `DIVIDE(x, y)` 示例：<br>`IF(y <> 0, x / y)` -> `DIVIDE(x, y)`                                                                                                                                                                                                                                                                                                              |
| DI016 | 使用正确的 UDF 语法                         | 为用户定义函数表达式使用正确的语法。 示例：<br>`(x, y) => x + y` 示例：<br>`(x, y) => x + y`                                                                                                                                                                                                                                                                                                                                                                                                                                |

### 可读性

当光标置于代码分段上时，下面的代码操作会在适用代码的前两个字符下方显示青绿色圆点，并在左侧边距显示螺丝刀图标

| ID    | 名称                                   | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| ----- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DR001 | [转换为标量谓词](xref:DR001)                | 列筛选器可以在不显式使用 [`FILTER`](https://dax.guide/FILTER) 函数的情况下，更简洁地写成标量谓词。 示例：<br>`FILTER(ALL(Products[Color]), Products[Color] = "Red")` -> `Products[Color] = "Red"`<br>`FILTER(VALUES(Products[Color]), Products[Color] = "Red")` -> `KEEPFILTERS(Products[Color] = "Red")` 示例：<br>`FILTER(ALL(Products[Color]), Products[Color] = "Red")` -> `Products[Color] = "Red"`<br>`FILTER(VALUES(Products[Color]), Products[Color] = "Red")` -> `KEEPFILTERS(Products[Color] = "Red")` |
| DR002 | [使用聚合函数替代迭代器](xref:DR002)            | 尽可能使用聚合函数而不是迭代器函数，以简化代码。 示例：<br>`SUMX(Products, Products[SalesAmount])` -> `SUM(Products[SalesAmount])`                                                                                                                                                                                                                                                                                                                                                                      |
| DR003 | [使用 VALUES 替代 SUMMARIZE](xref:DR003) | 当 [`SUMMARIZE`](https://dax.guide/SUMMARIZE) 只指定一列，且该列属于第一个参数中指定的表时，可以使用 [`VALUES`](https://dax.guide/VALUES) 更简洁地编写代码。 示例：<br>`SUMMARIZE(Products, Products[Color])` -> `VALUES(Products[Color])` 示例：<br>`SUMMARIZE(Products, Products[Color])` -> `VALUES(Products[Color])`                                                                                                                                                                                                |
| DR004 | [变量前缀](xref:DR004)                   | 变量应使用一致的命名约定。 建议使用前缀，例如下划线。 可以配置要使用的前缀，以符合偏好的样式。 示例：<br>`VAR totalSales = SUM(Sales[SalesAmount])` -> `VAR _totalSales = SUM(Sales[SalesAmount])`                                                                                                                                                                                                                                                                                                                            |
| DR005 | [为临时列添加前缀](xref:DR005)               | 建议为临时列使用一致的前缀，以便更容易将它们与基列或度量值区分开来。 你可以配置要使用的前缀，以符合你偏好的风格。 示例：<br>`ADDCOLUMNS(Product, "SalesByProd", [Sales])` -> `ADDCOLUMNS(Product, "@SalesByProd", [Sales])`                                                                                                                                                                                                                                                                                                             |
| DR006 | [将常量聚合移至变量](xref:DR006)              | 当在迭代器或标量谓词中使用聚合函数时，该聚合对迭代中的每一行都会返回相同的结果。 因此，可以将该聚合移到迭代之外的 DAX 变量中。 示例：<br>`CALCULATE(..., 'Date'[Date] = MAX('Date'[Date]))` -><br>`VAR _maxDate = MAX('Date'[Date]) RETURN CALCULATE(..., 'Date'[Date] = _maxDate)`                                                                                                                                                                                                                                                         |
| DR007 | [简化 1 个变量代码块](xref:DR007)            | 仅包含一个变量的变量块可通过将表达式直接移入块的 `RETURN` 部分来简化。 前提是该变量只被引用一次，且不带任何上下文修饰符。 示例：<br>`VAR _result = [Sales] * 1.25 RETURN _result` -> `[Sales] * 1.25` 前提是该变量只被引用一次，且不带任何上下文修饰符。 示例：<br>`VAR _result = [Sales] * 1.25 RETURN _result` -> `[Sales] * 1.25`                                                                                                                                                                                                                               |
| DR008 | [简化多变量代码块](xref:DR008)               | 对于包含多个变量的变量块，如果每个变量都是简单的度量值引用，并且仅在 `RETURN` 部分使用一次且没有任何上下文修饰符，则应进行简化。 示例：<br>`VAR _sales = [Sales] VAR _cost = [Cost] RETURN _sales - _cost` -> `[Sales] - [Cost]` 示例：<br>`VAR _sales = [Sales] VAR _cost = [Cost] RETURN _sales - _cost` -> `[Sales] - [Cost]`                                                                                                                                                                                                              |
| DR009 | [改用 DISTINCTCOUNT 重写](xref:DR009)    | 不要使用 `COUNTROWS(DISTINCT(T[c])` 来统计某列中不同值的数量，改用 [`DISTINCTCOUNT`](https://dax.guide/DISTINCTCOUNT) 函数。                                                                                                                                                                                                                                                                                                                                                                       |
| DR010 | [改用 COALESCE 重写](xref:DR010)         | 不要使用 `IF` 从一组表达式中返回第一个非空值，改用 [`COALESCE`](https://dax.guide/COALESCE) 函数。 示例：<br>`IF(ISBLANK([Sales]), [Sales2], [Sales])` -> `COALESCE([Sales], [Sales2])` 示例：<br>`IF(ISBLANK([Sales]), [Sales2], [Sales])` -> `COALESCE([Sales], [Sales2])`                                                                                                                                                                                                                                |
| DR011 | [使用 ISBLANK 重写](xref:DR011)          | 不要将表达式与 [`BLANK()`](https://dax.guide/BLANK) 进行比较，而应使用 [`ISBLANK`](https://dax.guide/ISBLANK) 函数。 示例：<br>`IF([Sales] = BLANK(), [Budget], [Sales])` -> `IF(ISBLANK([Sales], [Budget], [Sales])` 示例：<br>`IF([Sales] = BLANK(), [Budget], [Sales])` -> `IF(ISBLANK([Sales], [Budget], [Sales])`                                                                                                                                                                                |
| DR012 | [移除不必要的 BLANK](xref:DR012)           | 某些 DAX 函数，例如 [`IF`](https://dax.guide/IF) 和 [`SWITCH`](https://dax.guide/SWITCH) 在条件为 false 时本就会返回 `BLANK()`，因此无需显式指定 `BLANK()`。 示例：<br>`IF(a > b, a, BLANK())` -> `IF(a > b, a)` 示例：<br>`IF(a > b, a, BLANK())` -> `IF(a > b, a)`                                                                                                                                                                                                                                           |
| DR013 | [简化否定逻辑](xref:DR013)                 | 当对逻辑表达式取反时，使用相反的运算符重写表达式通常更易读。 示例：<br>`NOT(a = b)` -> `a <> b` 示例：<br>`NOT(a = b)` -> `a <> b`                                                                                                                                                                                                                                                                                                                                                                               |
| DR014 | [使用 IN 简化](xref:DR014)               | 将复合谓词（对同一表达式进行相等比较，并通过 [`OR`](https://dax.guide/OR) 或 [`\\|\\|`](https://dax.guide/op/or/) 组合）改写为使用 [`IN`](https://dax.guide/IN) 运算符。 示例：<br>`a = 1 \\|\\| a = 2 \\|\\| a = 100` -> `a IN { 1, 2, 100 }` 示例：<br>`a = 1 \|\| a = 2 \|\| a = 100` -> `a IN { 1, 2, 100 }`                                                                                                                                                                                                |

### 重写

当光标放在代码分段上时，下面的“代码操作”会在左侧边距以螺丝刀图标显示。

| ID    | 名称                                     | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ----- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| RW001 | [使用 CALCULATE 改写 TOTALxTD](xref:RW001) | 诸如 [`TOTALMTD`](https://dax.guide/TOTALMTD)、[`TOTALQTD`](https://dax.guide/TOTALQTD) 和 [`TOTALYTD`](https://dax.guide/TOTALYTD) 之类的函数，都可以用更具表达力且更灵活的 [`CALCULATE`](https://dax.guide/CALCULATE) 函数来重写。 诸如 [`TOTALMTD`](https://dax.guide/TOTALMTD)、[`TOTALQTD`](https://dax.guide/TOTALQTD) 和 [`TOTALYTD`](https://dax.guide/TOTALYTD) 之类的函数，都可以用更具表达力且更灵活的 [`CALCULATE`](https://dax.guide/CALCULATE) 函数来重写。 示例：<br>`TOTALYTD([Total Sales], 'Date'[Date])` -> `CALCULATE([Total Sales], DATESYTD('Date'[Date]))` |
| RW002 | [使用 FILTER 重写](xref:RW002)             | 在 `CALCULATE` 的筛选器参数中，标量谓词可以用 `FILTER` 重写。 例如，当你需要添加更复杂的筛选逻辑时，这会很有用。 示例：<br>`CALCULATE(..., Products[Color] = "Red")` -> `CALCULATE(..., FILTER(ALL(Products[Color]), Products[Color] = "Red"))` 例如，当你需要添加更复杂的筛选逻辑时，这会很有用。 示例：<br>`CALCULATE(..., Products[Color] = "Red")` -> `CALCULATE(..., FILTER(ALL(Products[Color]), Products[Color] = "Red"))`                                                                                                                                                             |
| RW003 | [反转 IF](xref:RW003)                    | 为了提升可读性，有时把 `IF` 语句反过来写会更清晰。 为了提升可读性，有时把 `IF` 语句反过来写会更清晰。 示例：<br>`IF(a < b, "B is greater", "A is greater")` -> `IF(a > b, "A is greater", "B is greater")`                                                                                                                                                                                                                                                                                                                                                        |

## 自定义代码操作

你可以通过 **工具 > 偏好** 对话框，在 **文本编辑器 > DAX编辑器 > 代码操作** 中自定义代码操作的行为。 在这里，你可以启用或禁用该功能，并为部分代码操作配置更多选项，例如用于变量名和扩展列的前缀。 在这里，你可以启用或禁用该功能，并为部分代码操作配置更多选项，例如用于变量名和扩展列的前缀。

我们计划在后续版本中为此界面增加更多配置项，例如用于单独启用或禁用某个代码操作的选项。 敬请期待！ 敬请期待！

![代码操作偏好](~/content/assets/images/code-actions-preferences.png)

