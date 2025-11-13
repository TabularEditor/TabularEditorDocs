---
uid: DI010
category: Code actions
sub-category: Improvements
title: Use MIN/MAX instead of IF
author: Daniel Otykier
updated: 2025-01-03
---

Code action `DI010` (Improvement) **Use MIN/MAX instead of IF**

## Description

When a conditional expression is used to return the minimum or maximum of two values, it is more efficient and compact to use the [`MIN`](https://dax.guide/MIN) or [`MAX`](https://dax.guide/MAX) function.

### Example

Change:

```dax
IF([Total Sales] > 0, [Total Sales], 0))
```

To:

```dax
MAX([Total Sales], 0)
```

## Why is Tabular Editor suggesting this?

A common anti-pattern in DAX is to use an `IF` statement to return the smaller or larger of two values, by first comparing them, and then returning the appropriate value. However, this pattern can be simplified by using the `MIN` or `MAX` functions, which are more efficient and easier to read. The `MIN` function, when called with two arguments, returns the smallest value of the two arguments, while the `MAX` function returns the largest value. By using these functions, the code becomes more concise and easier to understand.

Moreover, if any measure references are included in the arguments, they are only evaluated once, which can improve performance.