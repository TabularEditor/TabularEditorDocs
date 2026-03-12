---
uid: detail-rows-expression
title: Detail Rows Expression
author: Just Blindbæk
updated: 2026-02-15
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Implementing Detail Rows Expressions

When a user double-clicks a value in an Excel PivotTable connected to a Power BI or Analysis Services model, they trigger a **drillthrough** — a sheet opens showing the underlying rows behind that aggregated value. By default, the model returns all columns from the measure's host table, which is rarely useful for end users.

A **Detail Rows Expression** lets you define exactly which columns appear in that drillthrough result. You write a DAX table expression that returns the shape of data you want the consumer to see — combining columns from the fact table with related attributes from dimension tables.

It is also worth noting that while an Excel PivotTable normally queries the model using MDX, a double-click drillthrough action is executed as a **DAX query**. This makes Detail Rows Expressions particularly effective for retrieving high-cardinality data — such as transaction IDs or individual order lines — where DAX significantly outperforms MDX.

In this tutorial, you configure a **table-level** Detail Rows Expression on the `Orders` table, so the same friendly drillthrough result applies to all measures on that table. You then see how to override it for a specific measure.

> [!NOTE]
> The steps in this tutorial apply to both Tabular Editor 2 and Tabular Editor 3. Screenshots show Tabular Editor 3.

## Prerequisites

Before you begin, you should have:

- Tabular Editor 2 or Tabular Editor 3
- A semantic model with at least one table containing measures
- Basic familiarity with DAX
- Excel connected to your model to test drillthrough

## Default Drillthrough Behavior

Before adding a Detail Rows Expression, it helps to see what end users experience by default.

When a user double-clicks an aggregated value in a PivotTable, the model returns all columns from the fact table — using raw internal column names, with no dimension attributes and no control over which columns are shown.

![Default drillthrough result in Excel showing raw, unformatted column names from the fact table](../assets/images/tutorials/detail-rows-expression/default-drillthrough.jpg)

The result is technically correct, but not useful: internal column names are exposed, related dimension attributes such as product names and customer accounts are missing, and there is no control over column order or selection.

## Table-Level vs. Measure-Level Detail Rows Expressions

A Detail Rows Expression can be defined at two levels:

| Level       | Property name                  | Scope                                                              |
| ----------- | ------------------------------ | ------------------------------------------------------------------ |
| **Table**   | Default Detail Rows Expression | Applies to all measures on the table                               |
| **Measure** | Detail Rows Expression         | Applies to that measure only; overrides the table-level expression |

Starting with a table-level expression is the most practical approach — one expression covers every measure on the table. If a specific measure requires different detail columns, you can override it with a measure-level expression, which takes precedence.

## Creating a Table-Level Detail Rows Expression

### Step 1: Select the table and locate the property

In the **TOM Explorer**, select the table you want to configure — in this case, the `Orders` table. In the **Properties** panel, find the **Default Detail Rows Expression** field under the **Options** group.

![The Orders table selected in TOM Explorer, with the Default Detail Rows Expression property visible and empty in the Properties panel](../assets/images/tutorials/detail-rows-expression/tom-and-default-detail-rows-expression-field.jpg)

### Step 2: Open the Expression Editor

Click the **Default Detail Rows Expression** field to open it in the **Expression Editor**.

### Step 3: Write the SELECTCOLUMNS expression

Enter a DAX expression using `SELECTCOLUMNS` to define the columns to return. Use `RELATED()` to bring in columns from dimension tables.

```dax
SELECTCOLUMNS(
    Orders,
    "Order Date", Orders[Order Date],
    "Product Name", RELATED( Products[Product Name] ),
    "Account Name", RELATED( Customers[Account Name] ),
    "Sales Order Document Number", Orders[Sales Order Document Number],
    "Quantity", [Quantity],
    "Value", [Value]
)
```

![The SELECTCOLUMNS expression entered in the Expression Editor, targeting the Orders table](../assets/images/tutorials/detail-rows-expression/expression-editor.jpg)

`SELECTCOLUMNS` takes the source table as its first argument, followed by pairs of `"Column Name", expression`:

- Columns from the `Orders` fact table are referenced directly: `Orders[Order Date]`, `Orders[Sales Order Document Number]`
- Columns from related dimension tables are retrieved using `RELATED()`: `Products[Product Name]`, `Customers[Account Name]`
- Measures can also be included: `[Quantity]`, `[Value]`

> [!NOTE]
> `RELATED()` works here because `SELECTCOLUMNS` iterates over rows of the `Orders` table, giving each row a row context that allows navigation to related tables via existing relationships.

> [!TIP]
> While `SELECTCOLUMNS` is the standard pattern, any valid DAX table expression can be used. For example, you can wrap the expression in `CALCULATETABLE` to apply additional filters, use `ADDCOLUMNS` to include derived values, or call `DETAILROWS` to reuse another measure's Detail Rows Expression and avoid duplication.

### Step 4: Save the model

Save with **Ctrl+S** and deploy or publish the model to your target environment.

## Testing the Result

Open or refresh your Excel PivotTable and double-click any aggregated value. The drillthrough sheet now shows the columns you defined — with friendly names and dimension attributes included.

![Drillthrough result in Excel showing the custom columns defined in the Detail Rows Expression](../assets/images/tutorials/detail-rows-expression/dre-drillthrough.jpg)

Compare this to the default result: instead of raw internal column names, users see meaningful headers and values pulled from related dimension tables.

## Overriding with a Measure-Level Expression

If a specific measure requires a different set of detail columns, you can define a **Detail Rows Expression** directly on that measure. This overrides the table-level expression for that measure only.

1. In the **TOM Explorer**, expand the table and select the measure — for example, `Quantity` under `Orders`.
2. In the **Properties** panel, find the **Detail Rows Expression** field.
3. Enter a `SELECTCOLUMNS` expression tailored to that measure.

```dax
SELECTCOLUMNS(
    Orders,
    "Order Date", Orders[Order Date],
    "Billing Date", Orders[Billing Date],
    "Confirm Goods Receipt Date", Orders[Confirm Goods Receipt Date],
    "Product Name", RELATED( Products[Product Name] ),
    "Product MK", RELATED( Products[MK] ),
    "Account Name", RELATED( Customers[Account Name] ),
    "Sales Order Document Number", Orders[Sales Order Document Number],
    "Quantity", [Quantity]
)
```

![A measure-specific Detail Rows Expression defined on the Quantity measure, visible in both the Expression Editor and the Properties panel](../assets/images/tutorials/detail-rows-expression/specific-detail-rows-expression.jpg)

When a client tool requests drillthrough for this measure, the measure-level expression is used instead of the table default.

## Troubleshooting

**Drillthrough still shows raw columns**
The model may not have been saved and deployed after adding the expression. Save the model, redeploy, and reconnect Excel before testing.

**Expression not applied to a specific measure**
If you have defined both a table-level and a measure-level expression, the measure-level takes precedence. Verify which expression is active by selecting the measure in the **Properties** panel and checking the **Detail Rows Expression** field.

**`RELATED()` returns an error**
`RELATED()` requires an active many-to-one relationship from the source table to the referenced dimension table. Check that the relationship exists and is active in your model.

## Further Reading

- [DAX Guide: SELECTCOLUMNS](https://dax.guide/selectcolumns/)
- [DAX Guide: RELATED](https://dax.guide/related/)
- [Microsoft Docs: Detail Rows Expressions](https://learn.microsoft.com/en-us/analysis-services/tabular-models/detail-rows-expressions)
- [SQLBI: Controlling drillthrough in Excel PivotTables](https://www.sqlbi.com/articles/controlling-drillthrough-in-excel-pivottables-connected-to-power-bi-or-analysis-services/)
