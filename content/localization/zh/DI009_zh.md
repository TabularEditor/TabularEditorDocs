---
uid: DI009
category: Code actions
sub-category: Improvements
title: Avoid calculate shortcut syntax
author: Daniel Otykier
updated: 2025-01-03
---

Code action `DI009` (Improvement) **Avoid calculate shortcut syntax**

## Description

Do not use the calculate shortcut syntax.

### Example

Change:

```dax
[Total Sales](Products[Color] = "Red")
```

To:

```dax
CALCULATE([Total Sales], Products[Color] = "Red")
```

## Why is Tabular Editor suggesting this?

The calculate shortcut syntax is a shorthand for the `CALCULATE` function, where the first argument is the measure to evaluate, and the second argument is the filter expression. While this syntax is valid, it is not recommended, as it can be confusing to read and understand. It is better to use the `CALCULATE` function explicitly, as it makes the code more readable and maintainable.