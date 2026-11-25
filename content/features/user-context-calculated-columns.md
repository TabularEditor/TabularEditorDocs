---
uid: user-context-calculated-columns
title: User-context calculated columns
author: Morten Lønskov
updated: 2026-11-12
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.27.0
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# User-context calculated columns

A *user-context calculated column* is a calculated column that's evaluated per user. Its expression can call functions such as [`USERPRINCIPALNAME`](https://dax.guide/userprincipalname) or [`USERNAME`](https://dax.guide/username) and return a different value for each user. In contrast, a standard calculated column is evaluated once, when the table is processed, and returns the same value for all users.

The calculated column's `ExpressionContext` property sets whether the column is evaluated once or per user:

| Expression Context | Meaning |
|---|---|
| `Standard` | The default, except for new calculated columns on [Direct Lake on OneLake tables](#direct-lake-on-onelake-tables). The expression can use only standard functions. The column has one value per row for all users. |
| `UserContext` | The expression can call user-context functions. The column is evaluated per user. |

Select a calculated column in the @tom-explorer-view and set **Expression Context** under **Options** in the @properties-view.

> [!NOTE]
> `ExpressionContext` requires compatibility level 1705 or higher, and below 1705 calculated columns are always `Standard`.

## Direct Lake on OneLake tables

`UserContext` is the only expression context Power BI supports for calculated columns on Direct Lake on OneLake tables. If a calculated column on a Direct Lake on OneLake table is set to `Standard` when you save the model to the Power BI service, the save fails with the error "Default expression context cannot be used for calculated columns in Direct Lake tables". Direct Lake on SQL tables don't support calculated columns.

At compatibility level 1705 or higher, a new calculated column on a Direct Lake on OneLake table is created with `UserContext`, also when a C# script or a DAX script adds it. New calculated columns on every other table, including Import and Direct Lake on SQL tables in the same model, are created with `Standard`. A column you copy and paste or duplicate keeps the expression context of its source column. Below compatibility level 1705, new columns are created with `Standard` and the compatibility level isn't changed.

A calculated column on a Direct Lake on OneLake table whose expression context is `Standard` gets an error in the @messages-view and on the column in the @tom-explorer-view. The DAX editor doesn't underline it. 

For the steps to check and fix the expression context of these columns, see [Calculated columns on Direct Lake on OneLake](xref:direct-lake-guidance#calculated-columns-on-direct-lake-on-onelake).

## What a user-context column can't be used for

Objects evaluated once for the whole model can't reference a user-context calculated column. The Tabular Editor Semantic Analyzer reports an error for each of these cases:

| A user-context column can't be referenced by | Message |
|---|---|
| A standard calculated column | "This expression references the user-context-aware calculated column `Table[Column]`, which is not allowed in a standard calculated column." |
| A calculated table | "This expression references the user-context-aware calculated column `Table[Column]`, which is not allowed in a calculated table." |
| A row-level security filter | "This expression references the user-context-aware calculated column `Table[Column]`, which is not allowed in a row-level security filter." |
| A relationship, as an endpoint | "A relationship cannot use the user-context-aware calculated column `Table[Column]` as an endpoint." |

The first three rules also apply to indirect references, for example through a measure. Measures and other user-context calculated columns can reference a user-context column.

## Where the errors appear

| How the column is referenced | DAX editor | @messages-view | [`te validate`](xref:te-cli-commands#validate) |
|---|---|---|---|
| Directly | Yes | Yes | Yes |
| Indirectly, for example through a measure | No | Yes | Yes |
| As a relationship endpoint | No | Yes | Yes |

The DAX editor doesn't underline indirect violations, so check the @messages-view for them before you deploy.

A relationship-endpoint violation also appears in the relationship's **Error Message** property. Active and inactive relationships are both checked, with errors reported per endpoint, so a relationship with user-context columns on both sides has two.

> [!NOTE]
> `te validate --errors-only` still reports these violations, because the option hides only warnings and anti-patterns.

## Next steps

- @messages-view
- @dax-editor
- @preferences
