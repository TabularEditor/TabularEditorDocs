---
uid: user-context-calculated-columns
title: User-context calculated columns
author: Morten Lønskov
updated: 2026-09-14
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

A calculated column is normally evaluated once, when the table is processed, and every user who queries the model sees the same value. A *user-context calculated column* is evaluated per user instead, so its expression can call functions such as [`USERPRINCIPALNAME`](https://dax.guide/userprincipalname) or [`USERNAME`](https://dax.guide/username) and give each user a different answer.

This is controlled by the calculated column's **Expression Context** property.

| Expression Context | Meaning |
|---|---|
| **Standard** | The default. The expression can use only standard functions, and the column has one value per row for everybody |
| **User Context** | The expression can call user-context functions, and is evaluated per user |

Select a calculated column in the @tom-explorer-view and set **Expression Context** under **Options** in the @properties-view.

> [!NOTE]
> **Expression Context** requires compatibility level 1705 or above. Below that, a calculated column is always Standard.

## What a user-context column cannot be used for

Because the value depends on who is asking, a user-context calculated column cannot be read by anything that is evaluated once for the whole model. Tabular Editor's Semantic Analyzer checks the four cases and reports an error for each:

| A user-context column cannot be referenced by | Message |
|---|---|
| A **standard** calculated column | *This expression references the user-context-aware calculated column `Table[Column]`, which is not allowed in a standard calculated column.* |
| A **calculated table** | *This expression references the user-context-aware calculated column `Table[Column]`, which is not allowed in a calculated table.* |
| A **row-level security filter** | *This expression references the user-context-aware calculated column `Table[Column]`, which is not allowed in a row-level security filter.* |
| A **relationship**, as an endpoint | *A relationship cannot use the user-context-aware calculated column `Table[Column]` as an endpoint.* |

The first three apply *indirectly as well as directly*. Reaching the column through a measure is still reaching it, and is reported the same way.

Two things are explicitly allowed: a *measure* can reference a user-context column, and so can *another user-context calculated column*.

## Where the errors appear

| How the column is referenced | DAX editor | @messages-view | `te validate` |
|---|---|---|---|
| Directly | Yes | Yes | Yes |
| Indirectly, for example through a measure | No | Yes | Yes |
| As a relationship endpoint | No | Yes | Yes |

An indirect violation has no squiggle in the editor, because the expression you are looking at is perfectly valid on its own. The chain is what breaks. Check the @messages-view before deploying.

A relationship-endpoint violation also appears as the relationship's **Error Message** property, and is reported once per offending endpoint, so a relationship with user-context columns on both sides produces two errors. Inactive relationships are checked too.

> [!IMPORTANT]
> `te validate --errors-only` does *not* suppress these. They are errors, not warnings, and `--errors-only` only hides warnings and anti-patterns.

## Next steps

- @messages-view
- @dax-editor
- @preferences
