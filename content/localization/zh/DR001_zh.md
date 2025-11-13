---
uid: DR001
category: Code actions
sub-category: Readability
title: Convert to scalar predicate
author: Daniel Otykier
updated: 2025-01-06
---

Code action `DR001` (Readability) **Convert to scalar predicate**

## Description

A column filter can be written more concisely as a scalar predicate, without explicitly using the [`FILTER`](https://dax.guide/FILTER) function.

### Example 1

Change:

```dax
CALCULATE(
	[Invoice Amount],
	FILTER(ALL('Document'[Document Type]), 'Document'[Document Type] = "Sales Order")
)
```

To:

```dax
CALCULATE(
	[Invoice Amount],
	'Document'[Document Type] = "Sales Order"
)
```

### Example 2

Change:

```dax
CALCULATE(
	[Invoice Amount],
	FILTER(VALUES('Document'[Document Type]), 'Document'[Document Type] = "Sales Order")
)
```

To:

```dax
CALCULATE(
	[Invoice Amount],
	KEEPFILTERS('Document'[Document Type] = "Sales Order")
)
```

## Why is Tabular Editor suggesting this?

A scalar predicate is a simpler and more concise way (e.g. "syntax sugar") to express a column filter, compared to using the `FILTER` function explicitly. By using a scalar predicate, the code becomes easier to read and understand, as it removes unnecessary complexity and makes the intent of the filter expression more clear.