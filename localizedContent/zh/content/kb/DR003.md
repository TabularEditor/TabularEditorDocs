---
uid: DR003
category: Code actions
sub-category: Readability
title: Use VALUES instead of SUMMARIZE
author: Daniel Otykier
updated: 2025-01-06
---

Code action `DR003` (Readability) **Use VALUES instead of SUMMARIZE**

## Description

When [`SUMMARIZE`](https://dax.guide/SUMMARIZE) only specifies a single column, and that column belongs to the table specified in the first argument, the code can be more concisely written using [`VALUES`](https://dax.guide/VALUES).

### Example

Change:

```dax
SUMMARIZE(Sales, Sales[Product Key])
```

To:

```dax
VALUES(Sales[Product Key])
```

## Why is Tabular Editor suggesting this?

The `SUMMARIZE` function is a powerful function that can be used to group data and calculate aggregates. However, when you only need to retrieve the distinct values of a single column, the `VALUES` function is more concise and easier to read. By using the `VALUES` function, the code becomes more readable and the intent of the expression is clearer.

## Related to:

- [DR002 - Use aggregator instead of iterator](xref:DR002)