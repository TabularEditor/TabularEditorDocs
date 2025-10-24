---
uid: DI005
category: Code actions
sub-category: Improvements
title: Rewrite table filter as scalar predicate
author: Daniel Otykier
updated: 2024-12-19
---

Code action `DI005` (Improvement) **Rewrite table filter as scalar predicate**

## Description

Rewrite [`CALCULATE`](https://dax.guide/CALCULATE) filter arguments as scalar predicates when possible, instead of using the [`FILTER`](https://dax.guide/FILTER) function.

## Example 1

Change:

```dax
CALCULATE([Total Sales], FILTER(Products, Products[Color] = "Red"))
```

To:

```dax
CALCULATE([Total Sales], KEEPFILTERS(Products[Color] = "Red"))
```

## Example 2

Change:

```dax
CALCULATE([Total Sales], FILTER(ALL(Products), Products[Color] = "Red"))
```

To:

```dax
CALCULATE([Total Sales], ALL(Products), Products[Color] = "Red")
```

## Example 3

Change:

```dax
CALCULATE(
    [Total Sales],
    FILTER(
        ALL(Products), 
        Products[Color] = "Red" 
            && Products[Class] = "High-end"
    )
)
```

To:

```dax
CALCULATE(
    [Total Sales], 
    ALL(Products),
    Products[Color] = "Red", 
    Products[Class] = "High-end"
)
```

## Why is Tabular Editor suggesting this?

Filtering a table inside a `CALCULATE` filter argument is less efficient than filtering one or more columns from that table. By rewriting the filter as a scalar predicate, you make your code more efficient, consuming less memory and CPU resources.

For example, an expression such as `FILTER(Sales, < condition >)` will iterate over all rows in the `Sales` table, evaluating the condition for each row. In contrast, an expression such as `Sales[Quantity] > 0` will only iterate over the `Quantity` column, which is much more efficient, and does not cause all the columns from the `Sales` table to be added to the filter context.

By using scalar predicates, you also make your code more concise and easier to read.

Behind the scenes, scalar predicates are syntax sugar for a table expression that also uses the `FILTER` function. However, the `FILTER` function is applied to a single column, which is more efficient than filtering the entire table.