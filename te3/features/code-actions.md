---
uid: code-actions
title: Code Actions
author: Daniel Otykier
updated: 2024-08-28
applies_to:
  editions:
    - edition: Desktop
    - edition: Business
    - edition: Enterprise
---

# Code Actions

Tabular Editor 3.18.0 introduces a new feature called **Code Actions**. This feature is enabled by default, but can be disabled in the **Tools > Preferences** dialog, under **Text Editors > DAX Editor > Code Actions**.

Code Actions is a productivity feature that discretely provides suggestions for improving your DAX code, letting you apply the suggestions with a single click. Code Actions also provide easy access to common code refactoring operations.

Code Actions are separated into three different categories:

1. **Improvements**: These are recommended suggestions for improving your DAX code, in terms of:
    - Following best practices
    - Avoiding common pitfalls and anti-patterns
    - Avoiding obsolete or deprecated DAX features
    - Writing better, more performant DAX code
2. **Readability**: These are suggestions for making your DAX code more readable, by:
    - Simplifying complex expressions, when possible
    - Remove redundant or unnecessary code
    - Applying consistent formatting and naming conventions
3. **Rewrites**: These are suggestions for refactoring your DAX code. They are not necessarily improvements, but are often useful as part of larger code refactorings. Examples are:
    - Convert DAX "syntax sugar" to more verbose, but more explicit code
    - Rename all occurrences of a variable or an extension column
    - Format code

## How to use Code Actions

A new command and corresponding toolbar / menu buttons have been added, **Show Code Actions**, with a default keyboard shortcut of `Ctrl+.`. This command will show the applicable Code Actions at the current cursor position:

![Code Action Invoke Menu](~/images/code-action-invoke-menu.png)

You can also find the applicable Code Actions through the **Refactor** submenu of the right-click context menu:

![Code Action Refactor Submenu](~/images/code-action-refactor-submenu.png)

Lastly, a lightbulb or screwdriver icon is shown in the left margin of the editor, when the cursor is placed on a code segment that has applicable actions. Clicking on the icon will also bring up the Code Actions menu::

![Code Actions Margin](~/images/code-action-margin.png)

## Code Action indicators

**Improvements** and **Readability** Code Actions will also be indicated visually in the code editor. This way, you can quickly determine which parts of your code can be improved or made more readable.

- **Improvements** are shown with orange dots under the first few characters of the code segment (unless that code segment already displays an orange warning squiggly). When the cursor is moved over the code segment, a *lightbulb* icon will appear in the left margin.
- **Readability** actions are shown with teal green dots under the first few characters of the code segment. When the cursor is moved over the code segment, a *screwdriver* icon will appear in the left margin.
- **Rewrites** are not visually indicated in the code itself, however, the *screwdriver* icon will appear in the left margin when the cursor is placed on a code segment that has applicable rewrites.

## Apply to all occurrences

Some Code Actions can be applied to all occurrences within the current DAX expression, DAX script or DAX query, rather than just the code segment under the cursor. When this is the case, the Code Action will be shown in the Code Actions menu with " (All occurrences)" appended to the action description. Clicking on the action will apply the change to all occurrences in the document.

In the screenshot below, for example, the **Prefix variable with '_'** action can be applied to all occurrences (i.e. all variables) in the document, not just the `totalSales` variable under the cursor:

![Code Action All Occurrences](~/images/code-action-all-occurrences.png)

## List of Code Actions

The table below lists all currently available Code Actions. By default, all of those are enabled, but you can toggle off individual actions through the **Tools > Preferences** dialog, under **Text Editors > DAX Editor > Code Actions**. Some Code Actions also has additional configuration options, such as which prefix to use for variable names.

### Improvements

The Code Actions below will appear with orange dots under the first two characters of the applicable code, and a lightbulb icon in the left margin when the cursor is placed on the code segment:

| Name | Description |
| --- | --- |
| Remove unused variable | Variables that are not being referenced anywhere, should be removed. Example:<br>`VAR a = 1 VAR b = 2 RETURN a` -> `VAR a = 1 RETURN a` |
| Remove all unused variables | Variables that are not being used (directly or indirectly through other variables) in the `RETURN` part of a variable block, should be removed. Example:<br>`VAR a = 1 VAR b = a RETURN 123` -> `123` |
| Remove table name | Measure references should not include the table name, as the table name is unnecessary when referencing measures. Moreover, this practice makes measure references more easily distinguishable from column references. Example:<br>`Sales[Total Sales]` -> `[Total Sales]` 
| Add table name | Column references should include the table name to avoid ambiguities, and to more easily distinguish column references from measure references. Example:<br>`SUM([SalesAmount])` -> `SUM(Sales[SalesAmount])` |
| Rewrite table filter as scalar predicate | A common anti-pattern in DAX is to filter a table inside a [`CALCULATE`](https://dax.guide/CALCULATE) filter argument, when it is sufficient to filter one or more columns from that table. Example:<br>`CALCULATE([Total Sales], FILTER(Products, Products[Color] = "Red"))` -> `CALCULATE([Total Sales], KEEPFILTERS(Products[Color] = "Red"))`<br>This Code Action supports various variations of the original expression. |
| Split multi-column filter into multiple filters | When filtering a table on multiple columns combined using `AND` (or the equivalent `&&` operator), better performance can often be achieved by specifying multiple filters, one for each column. Example:<br>`CALCULATE(..., Products[Color] = "Red" && Products[Size] = "Large")` -> `CALCULATE(..., Products[Color] = "Red", Products[Size] = "Large")` |
| Simplify SWITCH statement | A [`SWITCH`](https://dax.guide/SWITCH) statement that specifies `TRUE()` for the **&lt;Expression&gt;** argument, and where all **&lt;Value&gt;** arguments are simple comparisons of the same variable/measure, can be simplified. Example:<br>`SWITCH(TRUE(), a = 1, ..., a = 2, ...)` -> `SWITCH(a, 1, ..., 2, ...)` |
| Remove superfluous CALCULATE | A [`CALCULATE`](https://dax.guide/CALCULATE) function that is not necessary, because it does not modify the filter context, or because an implicit context transition would happen anyway, should be removed. Examples:<br>`CALCULATE([Total Sales])` -> `[Total Sales]`<br>`AVERAGEX(Product, CALCULATE([Total Sales]))` -> `AVERAGEX(Product, [Total Sales])`<br><br>Also applies when the first argument of `CALCULATE` / `CALCULATETABLE` is a DAX variable, e.g.:<br>`VAR x = [Total Sales] RETURN CALCULATE(x, Product[Color] = "Red")` -><br>`VAR x = [Total Sales] RETURN x` |
| Avoid calculate shortcut syntax | Example:<br>`[Total Sales](Products[Color] = "Red")` -> `CALCULATE([Total Sales], Products[Color] = "Red")` |
| Use MIN/MAX instead of IF | When a conditional expression is used to return the minimum or maximum of two values, it is more efficient and compact to use the [`MIN`](https://dax.guide/MIN) or [`MAX`](https://dax.guide/MAX) function. Example:<br>`IF(a > b, a, b)` -> `MAX(a, b)` |
| Use ISEMPTY instead of COUNTROWS | When checking if a table is empty, it is more efficient to use the [`ISEMPTY`](https://dax.guide/ISEMPTY) function than to count the rows of the table. Examples:<br>`COUNTROWS(Products) = 0` -> `ISEMPTY(Products)` |
| Use DIVIDE instead of division | When using an arbitrary expression in the denominator of a division, use [`DIVIDE`](https://dax.guide/DIVIDE) instead of the division operator, to avoid division by zero errors. Example:<br>`x / y` -> `DIVIDE(x, y)` |
| Use division instead of DIVIDE | When the 2nd argument of [`DIVIDE`](https://dax.guide/DIVIDE) is a non-zero constant, it is more efficient to use the division operator. Example:<br>`DIVIDE(x, 2)` -> `x / 2` |

### Readability

The Code Actions below will appear with teal green dots under the first two characters of the applicable code, and a screwdriver icon in the left margin when the cursor is placed on the code segment

| Name | Description |
| --- | --- |
| Convert to scalar predicate | A column filter can be written more concisely as a scalar predicate, without explicitly using the [`FILTER`](https://dax.guide/FILTER) function. Examples:<br>`FILTER(ALL(Products[Color]), Products[Color] = "Red")` -> `Products[Color] = "Red"`<br>`FILTER(VALUES(Products[Color]), Products[Color] = "Red")` -> `KEEPFILTERS(Products[Color] = "Red")` |
| Use aggregator instead of iterator | Use an aggregator function instead of an iterator function when possible, to simplify the code. Example:<br>`SUMX(Products, Products[SalesAmount])` -> `SUM(Products[SalesAmount])` |
| Use VALUES instead of SUMMARIZE | When [`SUMMARIZE`](https://dax.guide/SUMMARIZE) only specifies a single column, and that column belongs to the table specified in the first argument, the code can be more concisely written using [`VALUES`](https://dax.guide/VALUES). Example:<br>`SUMMARIZE(Products, Products[Color])` -> `VALUES(Products[Color])` |
| Prefix variable | Variables should use a consistent naming convention. It is recommended to use a prefix, such as an underscore. You can configure which prefix to use, to match your preferred style. Example:<br>`VAR totalSales = SUM(Sales[SalesAmount])` -> `VAR _totalSales = SUM(Sales[SalesAmount])` |
| Prefix temporary column | It is recommended to use a consistent prefix for temporary columns, to more easily distinguish them from base columns or measures. You can configure which prefix to use, to match your preferred style. Example:<br>`ADDCOLUMNS(Product, "SalesByProd", [Sales])` -> `ADDCOLUMNS(Product, "@SalesByProd", [Sales])` |
| Move constant aggregation to variable | When an aggregation function is used inside an iterator or a scalar predicate, the aggregation produces the same result for every row of the iteration, and therefore the aggregation could be moved to a DAX variable outside of the iteration. Example:<br>`CALCULATE(..., 'Date'[Date] = MAX('Date'[Date]))` -><br>`VAR _maxDate = MAX('Date'[Date]) RETURN CALCULATE(..., 'Date'[Date] = _maxDate)` |
| Simplify 1-variable block | A variable block with only one variable can be simplified by moving the expression directly into the `RETURN` part of the block. This assumes the variable is only referenced once without any context modifiers. Example:<br>`VAR _result = [Sales] * 1.25 RETURN _result` -> `[Sales] * 1.25` |
| Simplify multi-variable block | A variable block with multiple variables where each is a simple measure reference, which are only used once in the `RETURN` section without any context modifiers, should be simplified. Example:<br>`VAR _sales = [Sales] VAR _cost = [Cost] RETURN _sales - _cost` -> `[Sales] - [Cost]` |
| Rewrite using DISTINCTCOUNT | Instead of using `COUNTROWS(DISTINCT(T[c])` to count the number of distinct values in a column, use the [`DISTINCTCOUNT`](https://dax.guide/DISTINCTCOUNT) function. |
| Rewrite using COALESCE | Instead of using `IF` to return the first non-blank value from a list of expressions, use the [`COALESCE`](https://dax.guide/COALESCE) function. Example:<br>`IF(ISBLANK([Sales]), [Sales2], [Sales])` -> `COALESCE([Sales], [Sales2])` |
| Rewrite using ISBLANK | Instead of comparing an expression with `BLANK()`, use the [`ISBLANK`](https://dax.guide/ISBLANK) function. Example:<br>`IF([Sales] = BLANK(), [Budget], [Sales])` -> `IF(ISBLANK([Sales], [Budget], [Sales])` |
| Remove unnecessary BLANK | Some DAX functions, such as [`IF`](https://dax.guide/IF) and [`SWITCH`](https://dax.guide/SWITCH) already return `BLANK()` when the condition is false, so there is no need to explicitly specify `BLANK()`. Example:<br>`IF(a > b, a, BLANK())` -> `IF(a > b, a)` |
| Simplify negated logic | When a logical expression is negated, it is often more readable to rewrite the expression using the negated operator. Example:<br>`NOT(a = b)` -> `a <> b` |

### Rewrites

The Code Actions below will appear with a screwdriver icon in the left margin when the cursor is placed on the code segment.

| Name | Description |
| --- | --- |
| Rewrite TOTALxTD using CALCULATE | Functions such as [`TOTALMTD`](https://dax.guide/TOTALMTD), [`TOTALQTD`](https://dax.guide/TOTALQTD) and [`TOTALYTD`](https://dax.guide/TOTALYTD) can be rewritten using the [`CALCULATE`](https://dax.guide/CALCULATE) function, which is more expressive and provides greater flexibility. Example:<br>`TOTALYTD([Total Sales], 'Date'[Date])` -> `CALCULATE([Total Sales], DATESYTD('Date'[Date]))` |
| Rewrite using FILTER | A scalar predicate in a filter argument to `CALCULATE` can be rewritten using `FILTER`. This is useful, for example when you need to add more complex filtering logic. Example:<br>`CALCULATE(..., Products[Color] = "Red")` -> `CALCULATE(..., FILTER(ALL(Products[Color]), Products[Color] = "Red"))` |
| Invert IF | To improve readability, it is sometimes useful to invert `IF` statements. Example:<br>`IF(a < b, "B is greater", "A is greater")` -> `IF(a > b, "A is greater", "B is greater")` |