---
uid: DR014
category: Code actions
sub-category: Readability
title: Simplify using IN
author: Daniel Otykier
updated: 2025-01-09
---

Code action `DR014` (Readability) **Simplify using IN**

## Description

Rewrite compound predicates (equality comparisons of the same expression that are combined using [`OR`](https://dax.guide/OR) or [`||`](https://dax.guide/op/or/)) with the [`IN`](https://dax.guide/IN) operator.

### Example

Change:

```dax
IF(Document[Type] = "Invoice" || Document[Type] = "Credit Note", 1, 0)
```

To:

```dax
IF(Document[Type] IN {"Invoice", "Credit Note"}, 1, 0)
```

## Why is Tabular Editor suggesting this?

The `IN` operator is more concise and easier to read than multiple `||` operators or `OR` function calls. It also makes it easier to add or remove values from the list of values to compare against.