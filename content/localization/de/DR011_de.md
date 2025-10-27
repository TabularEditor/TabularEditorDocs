---
uid: DR011
category: Code actions
sub-category: Readability
title: Rewrite using ISBLANK
author: Daniel Otykier
updated: 2025-01-09
---

Code action `DR011` (Readability) **Rewrite using ISBLANK**

## Description

Instead of comparing an expression with the value returned by [`BLANK()`](https://dax.guide/BLANK), use the [`ISBLANK`](https://dax.guide/ISBLANK) function.

### Example

Change:

```dax
IF(
    Document[Type] == BLANK(), 
    [Sales Amount], 
    [Sales Amount] * 1.25
)
```

To:

```dax
IF(
    ISBLANK(Document[Type]), 
    [Sales Amount], 
    [Sales Amount] * 1.25
)
```

## Why is Tabular Editor suggesting this?

The `ISBLANK` function is a more concise and easier to read way of checking if an expression returns a blank value. By using `ISBLANK`, the code becomes more readable and the intent of the expression is clearer.

## Remarks

This code action only applies to [strict equality comparison (==)](https://dax.guide/op/strictly-equal-to/) with `BLANK()`. The regular equality comparison `Document[Type] = BLANK()` does not produce the same result as `ISBLANK(Document[Type])` if `[Type]` is an empty string, or zero (in which case `ISBLANK(Document[Type])` would return `FALSE` while `Document[Type] = BLANK()` would return `TRUE`).

## Further reading

- [SQLBI: Handling BLANK in DAX](https://www.sqlbi.com/articles/blank-handling-in-dax/)