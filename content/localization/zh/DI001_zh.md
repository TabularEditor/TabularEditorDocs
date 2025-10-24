---
uid: DI001
category: Code actions
sub-category: Improvements
title: Remove unused variable
author: Daniel Otykier
updated: 2024-12-19
---

Code action `DI001` (Improvement) **Remove unused variable**

## Description

Variables that are not being referenced anywhere, should be removed.

## Example

Change:

```dax
VAR _internetSalesTaxed = [Internet Sales] * 1.25
VAR _cogsTaxed = [Cost of Sales] * 1.25
VAR _internetSales = [Internet Sales]
RETURN _internetSalesTaxed - _cogsTaxed
```

To:

```dax
VAR _internetSalesTaxed = [Internet Sales] * 1.25
VAR _cogsTaxed = [Cost of Sales] * 1.25
RETURN _internetSalesTaxed - _cogsTaxed
```

## Why is Tabular Editor suggesting this?

Unused variables can make your code harder to read and understand. By removing them, you make your code more concise and easier to maintain.

An unused variable is also an indication that the code may contain a mistake, or that the variable was intended to be used for something that was later removed. By removing the variable, you avoid potential confusion for other developers who may be reading your code.

## Related to:

- [DI002 - Remove all unused variables](xref:DI002)