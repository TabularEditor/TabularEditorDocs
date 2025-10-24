---
uid: DI012
category: Code actions
sub-category: Improvements
title: Use DIVIDE instead of division
author: Daniel Otykier
updated: 2025-01-03
---

Code action `DI012` (Improvement) **Use DIVIDE instead of division**

## Description

When using an arbitrary expression in the denominator of a division, use [`DIVIDE`](https://dax.guide/DIVIDE) instead of the division operator, to avoid division by zero errors.

### Example

Change:

```dax
[Total Sales] / [Total Cost]
```

To:

```dax
DIVIDE([Total Sales], [Total Cost])
```

## Why is Tabular Editor suggesting this?

When dividing two numbers in DAX, it is common to use the division operator `/`. However, if the denominator is zero, the result of the division is an error. This can be problematic in certain scenarios, as it can cause the entire expression to fail. Downstream measures may use [`IFERROR`](https://dax.guide/IFERROR) to handle this, but a more elegant and better performing solution is to use the `DIVIDE` function, which returns a specific value or (Blank) if the denominator is zero. This makes the code more robust and easier to read.

Tabular Editor will not suggest this action if the denominator is guaranteed to be non-zero, such as when dividing by a (non-zero) constant, in which case the division operator `/` is preferred.