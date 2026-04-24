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

Tabular Editor 3.18.0 引入了一项名为 **代码操作** 的新功能。 该功能默认启用，但你可以在 **工具 > 偏好** 对话框中，依次进入 **文本编辑器 > DAX编辑器 > 代码操作** 将其禁用。

代码操作是一项提升效率的功能，会在不打扰你的情况下，为你提供改进 DAX 代码的建议。 你只需单击一次即可应用这些建议。 代码操作还让你能轻松执行常见的代码重构操作。

代码操作分为三个不同的类别：

1. **改进**：这类建议可从以下方面帮助你改进 DAX 代码：
   - 遵循最佳做法
   - 避免常见陷阱和反模式
   - 避免使用过时或已弃用的 DAX 功能
   - 编写更好、性能更高的 DAX 代码
2. **可读性**：这些建议可通过以下方式提高 DAX 代码的可读性……
   - 在可能的情况下简化复杂表达式
   - 删除冗余或不必要的代码
   - 应用一致的格式和命名规范
3. **重写**：这些是用于重构 DAX 代码的建议。 它们不一定是改进，但在进行较大规模的代码重构时通常很有用。 示例包括：
   - 将 DAX “语法糖”改写为更冗长但更明确的代码
   - 重命名某个变量或扩展列的所有出现位置
   - 格式化代码

## 如何使用代码操作

新增了 **显示代码操作** 命令及其对应的工具栏/菜单按钮，默认键盘快捷键为 `Ctrl+.`。 这个命令会显示当前光标位置可用的代码操作：

![代码操作调用菜单](~/content/assets/images/features/code-action-invoke-menu.png)

你也可以通过右键上下文菜单中的 **重构** 子菜单找到可用的代码操作：

![代码操作重构子菜单](~/content/assets/images/features/code-action-refactor-submenu.png)

最后，当光标位于包含可用操作的代码分段上时，编辑器左侧边距会显示灯泡或螺丝刀图标。 点击该图标也会打开代码操作菜单：

![代码操作边距](~/content/assets/images/features/code-action-margin.png)

将鼠标悬停在代码操作菜单中的某个操作上时，工具提示会显示该操作的更多信息。 点击“了解更多”链接，即可查看该操作对应的知识库 (KB) 文章。

![代码操作工具提示](~/content/assets/images/features/code-action-tooltip.png)

## 代码操作指示器

在代码编辑器中，**改进** 和 **可读性** 代码操作也会以视觉标识显示。 这样你就能快速判断代码中哪些部分可以改进，或提升可读性。

- **改进** 会以橙色圆点显示在代码分段前几个字符的下方（除非该代码分段已显示橙色警告波浪线）。 当光标移到该代码分段上时，左侧边距会显示一个 _灯泡_ 图标。
- **可读性** 操作会以蓝绿色圆点显示在代码分段前几个字符的下方。 当光标移到该代码分段上时，左侧边距会显示一个 _螺丝刀_ 图标。
- **重写**本身不会在代码中显示任何视觉标记；但当光标放在包含可用重写的代码分段上时，左侧边距会出现 _螺丝刀_ 图标。

## 应用到所有出现处

某些代码操作可应用于当前 DAX 表达式、DAX 脚本或 DAX 查询中的所有出现位置，而不仅仅是光标下的代码分段。 在这种情况下，该代码操作会显示在“代码操作”菜单中，并在操作描述后追加 " (All occurrences)"。 点击该操作后，将把更改应用于文档中的所有出现处。

例如，在下方截图中，**为变量添加“_”前缀**这个操作可以应用到文档中的所有出现位置（即所有变量），而不只是光标所在的 `totalSales` 变量：

![代码操作 所有出现位置](~/content/assets/images/features/code-action-all-occurrences.png)

<a name="list-of-code-actions"></a>

## 代码操作列表

下表列出了当前所有可用的代码操作。 你可以在 **工具 > 偏好** 对话框的 **文本编辑器 > DAX编辑器 > 代码操作** 下关闭代码操作（后续更新将允许你单独开关各项操作，以获得更个性化的体验）。 某些代码操作还提供额外的配置选项，例如为变量名使用哪个前缀。

### 改进

以下代码操作会在适用代码的前两个字符下方显示橙色圆点；当光标位于该代码分段上时，左侧边距还会出现灯泡图标：

| ID    | 名称                                    | 描述                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ----- | ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DI001 | [删除未使用的变量](xref:DI001)                | 应删除未在任何地方被引用的变量。 示例：<br>`VAR a = 1 VAR b = 2 RETURN a` -> `VAR a = 1 RETURN a`                                                                                                                                                                                                                                                                                                                                         |
| DI002 | [删除所有未使用的变量](xref:DI002)              | 应删除 VAR 变量块中在 `RETURN` 部分未被使用的变量（无论直接使用还是通过其他变量间接使用）。 示例：<br>`VAR a = 1 VAR b = a RETURN 123` -> `123`                                                                                                                                                                                                                                                                                                                 |
| DI003 | [移除表名](xref:DI003)                    | 度量值引用中不应包含表名，因为引用度量值时表名是多余的。 此外，这样做也能让度量值引用与列引用更容易区分。 示例：<br>`Sales[Total Sales]` -> `[Total Sales]`                                                                                                                                                                                                                                                                                                                   |
| DI004 | [添加表名](xref:DI004)                    | 列引用应包含表名，以避免歧义，并让列引用与度量值引用更容易区分。 示例：<br>`SUM([SalesAmount])` -> `SUM(Sales[SalesAmount])`                                                                                                                                                                                                                                                                                                                              |
| DI005 | [将表筛选 FILTER 重写为标量谓词](xref:DI005)     | DAX 中一种常见的反模式是：在 [`CALCULATE`](https://dax.guide/CALCULATE) 的筛选参数中使用 `FILTER` 对整张表进行筛选，而实际上只需筛选该表中的一个或多个列即可。 示例：<br>`CALCULATE([Total Sales], FILTER(Products, Products[Color] = "Red"))` -> `CALCULATE([Total Sales], KEEPFILTERS(Products[Color] = "Red"))`<br>此代码操作支持原始表达式的多种变体。                                                                                                                                    |
| DI006 | [将多列筛选拆分为多个筛选](xref:DI006)            | 当使用 `AND`(或等效的 `&&` 运算符)将多个列组合起来筛选表时，通常可通过为每一列分别指定筛选条件来获得更好的性能。 示例：<br>`CALCULATE(..., Products[Color] = "Red" && Products[Size] = "Large")` -> `CALCULATE(..., Products[Color] = "Red", Products[Size] = "Large")`                                                                                                                                                                                 |
| DI007 | [简化 SWITCH 语句](xref:DI007)            | 对于 [`SWITCH`](https://dax.guide/SWITCH) 语句，如果其 **&lt;Expression&gt;** 参数指定为 `TRUE()`，并且所有 **&lt;Value&gt;** 参数都是对同一个 VAR 变量/度量值的简单比较，则可以简化。 示例：<br>`SWITCH(TRUE(), a = 1, ..., a = 2, ...)` -> `SWITCH(a, 1, ..., 2, ...)`                                                                                                             |
| DI008 | [移除多余的 CALCULATE](xref:DI008)         | 如果 [`CALCULATE`](https://dax.guide/CALCULATE) 并非必需——例如它不会修改筛选语境，或即使省略也会发生隐式语境转换——则应将其移除。 示例：<br>`CALCULATE([Total Sales])` -> `[Total Sales]`<br>`AVERAGEX(Product, CALCULATE([Total Sales]))` -> `AVERAGEX(Product, [Total Sales])`<br><br>当 `CALCULATE` / `CALCULATETABLE` 的第一个参数是 DAX 变量时，此规则同样适用，例如：<br>`VAR x = [Total Sales] RETURN CALCULATE(x, Product[Color] = "Red")` -><br>`VAR x = [Total Sales] RETURN x` |
| DI009 | [避免使用 CALCULATE 简写语法](xref:DI009)     | 示例：<br>`[Total Sales](Products[Color] = "Red")` -> `CALCULATE([Total Sales], Products[Color] = "Red")`                                                                                                                                                                                                                                                                                                                 |
| DI010 | [使用 MIN/MAX 代替 IF](xref:DI010)        | 当条件表达式用于返回两个值中的最小值或最大值时，使用 [`MIN`](https://dax.guide/MIN) 或 [`MAX`](https://dax.guide/MAX) 函数会更高效、更简洁。 示例：<br>`IF(a > b, a, b)` -> `MAX(a, b)`                                                                                                                                                                                                                                                                         |
| DI011 | [使用 ISEMPTY 代替 COUNTROWS](xref:DI011) | 检查表是否为空时，使用 [`ISEMPTY`](https://dax.guide/ISEMPTY) 函数比统计表的行数更高效。 示例：<br>`COUNTROWS(Products) = 0` -> `ISEMPTY(Products)`                                                                                                                                                                                                                                                                                               |
| DI012 | [使用 DIVIDE 代替除法](xref:DI012)          | 当在除法的分母中使用任意表达式时，建议使用 [`DIVIDE`](https://dax.guide/DIVIDE) 而不是除法运算符，以避免出现除以零错误。 示例：<br>`x / y` -> `DIVIDE(x, y)`                                                                                                                                                                                                                                                                                                       |
| DI013 | [使用除法运算符代替 DIVIDE](xref:DI013)        | 当 [`DIVIDE`](https://dax.guide/DIVIDE) 的第 2 个参数是非零常量时，使用除法运算符更高效。 示例：<br>`DIVIDE(x, 2)` -> `x / 2`                                                                                                                                                                                                                                                                                                                     |
| DI014 | [用 DIVIDE 代替 IFERROR](xref:DI014)     | 当除法的分母为零时，使用 [`DIVIDE`](https://dax.guide/DIVIDE) 函数而不是 [`IFERROR`](https://dax.guide/IFERROR) 来提供替代结果。 示例：<br>`IFERROR(x / y, 0)` -> `DIVIDE(x, y, 0)`                                                                                                                                                                                                                                                                |
| DI015 | [用 DIVIDE 替换 IF](xref:DI015)          | 使用 [`DIVIDE`](https://dax.guide/DIVIDE) 函数而不是 [`IF`](https://dax.guide/IF)，可更轻松地检查分母是否为零或空白。 示例：<br>`IF(y <> 0, x / y)` -> `DIVIDE(x, y)`                                                                                                                                                                                                                                                                              |
| DI016 | 使用正确的 UDF 语法                          | 用户定义函数表达式要使用正确的语法。 示例：<br>`(x, y) => x + y`                                                                                                                                                                                                                                                                                                                                                                            |

### 可读性

将光标置于代码分段上时，下面的代码操作会在适用代码的前两个字符下方显示青绿色圆点，并在左侧边距显示螺丝刀图标

| ID    | 名称                                   | 描述                                                                                                                                                                                                                                                                    |
| ----- | ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DR001 | [转换为标量谓词](xref:DR001)                | 列筛选器可以更简洁地写成标量谓词，而无需显式使用 [`FILTER`](https://dax.guide/FILTER) 函数。 示例：<br>`FILTER(ALL(Products[Color]), Products[Color] = "Red")` -> `Products[Color] = "Red"`<br>`FILTER(VALUES(Products[Color]), Products[Color] = "Red")` -> `KEEPFILTERS(Products[Color] = "Red")` |
| DR002 | [使用聚合函数而非迭代器函数](xref:DR002)          | 在可能的情况下，使用聚合函数而不是迭代器函数，以简化代码。 示例：<br>`SUMX(Products, Products[SalesAmount])` -> `SUM(Products[SalesAmount])`                                                                                                                                                          |
| DR003 | [使用 VALUES 而非 SUMMARIZE](xref:DR003) | 当 [`SUMMARIZE`](https://dax.guide/SUMMARIZE) 仅指定一列，且该列属于第一个参数指定的表时，可使用 [`VALUES`](https://dax.guide/VALUES) 将代码写得更简洁。 示例：<br>`SUMMARIZE(Products, Products[Color])` -> `VALUES(Products[Color])`                                                                      |
| DR004 | [为 VAR 变量添加前缀](xref:DR004)           | 变量应使用一致的命名规范。 建议使用前缀，例如下划线。 你可以配置要使用的前缀，以匹配你偏好的风格。 示例：<br>`VAR totalSales = SUM(Sales[SalesAmount])` -> `VAR _totalSales = SUM(Sales[SalesAmount])`                                                                                                                   |
| DR005 | [为临时列设置前缀](xref:DR005)               | 建议为临时列使用统一的前缀，以便更轻松地将其与基础列或度量值区分开来。 你可以配置要使用的前缀，以符合你偏好的风格。 示例：<br>`ADDCOLUMNS(Product, "SalesByProd", [Sales])` -> `ADDCOLUMNS(Product, "@SalesByProd", [Sales])`                                                                                                     |
| DR006 | [将常量聚合移入 VAR 变量](xref:DR006)         | 当聚合函数在迭代器或标量谓词中使用时，该聚合会为迭代中的每一行产生相同的结果。 因此，可以将该聚合移到迭代之外的 DAX VAR 变量中。 示例：<br>`CALCULATE(..., 'Date'[Date] = MAX('Date'[Date]))` -><br>`VAR _maxDate = MAX('Date'[Date]) RETURN CALCULATE(..., 'Date'[Date] = _maxDate)`                                               |
| DR007 | [简化 1 变量块](xref:DR007)               | 仅包含一个 VAR 变量的变量块可通过将表达式直接移到该块的 `RETURN` 部分来简化。 这假定该变量只被引用一次，且没有任何上下文修饰符。 示例：<br>`VAR _result = [Sales] * 1.25 RETURN _result` -> `[Sales] * 1.25`                                                                                                                     |
| DR008 | [简化多变量 VAR 块](xref:DR008)            | 对于包含多个变量的 VAR 变量块，若每个变量都只是对度量值的简单引用，并且每个变量在 `RETURN` 部分仅使用一次且不带任何上下文修饰符，则应简化该变量块。 示例：<br>`VAR _sales = [Sales] VAR _cost = [Cost] RETURN _sales - _cost` -> `[Sales] - [Cost]`                                                                                        |
| DR009 | [使用 DISTINCTCOUNT 重写](xref:DR009)    | 要统计列中不同值的数量，不要使用 `COUNTROWS(DISTINCT(T[c])`，而应使用 [`DISTINCTCOUNT`](https://dax.guide/DISTINCTCOUNT) 函数。                                                                                                                                                               |
| DR010 | [使用 COALESCE 重写](xref:DR010)         | 若要在 `RETURN` 中从一组表达式中返回第一个非空白值，不要使用 `IF`，而应使用 [`COALESCE`](https://dax.guide/COALESCE) 函数。 示例：<br>`IF(ISBLANK([Sales]), [Sales2], [Sales])` -> `COALESCE([Sales], [Sales2])`                                                                                          |
| DR011 | [使用 ISBLANK 重写](xref:DR011)          | 不要将表达式与 [`BLANK()`](https://dax.guide/BLANK) 进行比较，而应使用 [`ISBLANK`](https://dax.guide/ISBLANK) 函数。 示例：<br>`IF([Sales] = BLANK(), [Budget], [Sales])` -> `IF(ISBLANK([Sales], [Budget], [Sales])`                                                                       |
| DR012 | [移除不必要的 BLANK](xref:DR012)           | 某些 DAX 函数，例如 [`IF`](https://dax.guide/IF) 和 [`SWITCH`](https://dax.guide/SWITCH)，在条件不成立时已经会返回 `BLANK()`，因此无需显式指定 `BLANK()`。 示例：<br>`IF(a > b, a, BLANK())` -> `IF(a > b, a)`                                                                                          |
| DR013 | [简化取反逻辑](xref:DR013)                 | 对逻辑表达式取反时，通常改用对应的否定运算符来重写，这样更易读。 示例：<br>`NOT(a = b)` -> `a <> b`                                                                                                                                                                                                      |
| DR014 | [使用 IN 简化](xref:DR014)               | 使用 [`IN`](https://dax.guide/IN) 运算符来重写复合谓词（即针对同一表达式的相等比较，并通过 [`OR`](https://dax.guide/OR) 或 [`\\ a = 100` -> `a IN { 1, 2, 100 }`                                                                                                         |

### 重写

当光标放在代码分段上时，下方这些代码操作会以螺丝刀图标的形式显示在左侧边距。

| ID    | 名称                                     | 描述                                                                                                                                                                                                                                                                                                             |
| ----- | -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RW001 | [使用 CALCULATE 重写 TOTALxTD](xref:RW001) | [`TOTALMTD`](https://dax.guide/TOTALMTD)、[`TOTALQTD`](https://dax.guide/TOTALQTD) 和 [`TOTALYTD`](https://dax.guide/TOTALYTD) 等函数都可以使用 [`CALCULATE`](https://dax.guide/CALCULATE) 函数重写。这样表达力更强，也提供了更高的灵活性。 示例：<br>`TOTALYTD([Total Sales], 'Date'[Date])` -> `CALCULATE([Total Sales], DATESYTD('Date'[Date]))` |
| RW002 | [使用 FILTER 重写](xref:RW002)             | `CALCULATE` 的筛选参数中的标量谓词可以使用 `FILTER` 重写。 例如，当你需要添加更复杂的筛选逻辑时，这会很有用。 示例：<br>`CALCULATE(..., Products[Color] = "Red")` -> `CALCULATE(..., FILTER(ALL(Products[Color]), Products[Color] = "Red"))`                                                                                                                 |
| RW003 | [反转 IF](xref:RW003)                    | 为了提高可读性，有时反转 `IF` 语句会很有帮助。 示例：<br>`IF(a < b, "B is greater", "A is greater")` -> `IF(a > b, "A is greater", "B is greater")`                                                                                                                                                                                   |

## 自定义代码操作

你可以在 **工具 > 偏好** 对话框中，依次进入 **文本编辑器 > DAX编辑器 > 代码操作**，来自定义代码操作的行为。 在这里，你可以开启或关闭该功能，并为某些代码操作配置其他选项，例如用于变量名和扩展列的前缀。

我们计划在未来版本中为此界面添加更多配置选项，例如提供单独开启或关闭各个代码操作的选项。 敬请期待！

![代码操作偏好](~/content/assets/images/code-actions-preferences.png)

