---
uid: DR010
category: Code actions
sub-category: Readability
title: Rewrite using COALESCE
author: Daniel Otykier
updated: 2025-01-09
---

Code action `DR010` (Readability) **Rewrite using COALESCE**

## Description

Instead of using [`IF`](https://dax.guide/IF) to return the first non-blank value from a list of expressions, use the [`COALESCE`](https://dax.guide/COALESCE) function.

### Example

Change:

```dax
IF(
    ISBLANK(Product[Long Description]), 
    Product[Short Description], 
    Product[Long Description]
)
```

To:

```dax
COALESCE(Product[Long Description], Product[Short Description])
```

## Why is Tabular Editor suggesting this?

The `COALESCE` function is a more concise and easier to read way of returning the first non-blank value from a list of expressions. By using `COALESCE`, the code becomes more readable and the intent of the expression is clearer.