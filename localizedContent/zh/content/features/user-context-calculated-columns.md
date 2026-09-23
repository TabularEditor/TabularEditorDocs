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

A calculated column is normally evaluated once, when the table is processed, and every user who queries the model sees the same value. A _user-context calculated column_ is evaluated per user instead, so its expression can call functions such as [`USERPRINCIPALNAME`](https://dax.guide/userprincipalname) or [`USERNAME`](https://dax.guide/username) and give each user a different answer.

This is controlled by the calculated column's **Expression Context** property.

| Expression Context | 含义                                                                                                                              |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| **Standard**       | The default. The expression can use only standard functions, and the column has one value per row for everybody |
| **User Context**   | The expression can call user-context functions, and is evaluated per user                                                       |

Select a calculated column in the @tom-explorer-view and set **Expression Context** under **Options** in the @properties-view.

> [!NOTE]
> **Expression Context** requires compatibility level 1705 or above. Below that, a calculated column is always Standard.

## What a user-context column cannot be used for

Because the value depends on who is asking, a user-context calculated column cannot be read by anything that is evaluated once for the whole model. Tabular Editor's Semantic Analyzer checks the four cases and reports an error for each:

| A user-context column cannot be referenced by | 信息                                                                                                                                                           |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| A **standard** calculated column              | _This expression references the user-context-aware calculated column `Table[Column]`, which is not allowed in a standard calculated column._ |
| A **calculated table**                        | _This expression references the user-context-aware calculated column `Table[Column]`, which is not allowed in a calculated table._           |
| A **row-level security filter**               | _This expression references the user-context-aware calculated column `Table[Column]`, which is not allowed in a row-level security filter._  |
| A **relationship**, as an endpoint            | _A relationship cannot use the user-context-aware calculated column `Table[Column]` as an endpoint._                                         |

The first three apply _indirectly as well as directly_. Reaching the column through a measure is still reaching it, and is reported the same way.

Two things are explicitly allowed: a _measure_ can reference a user-context column, and so can _another user-context calculated column_.

## Where the errors appear

| How the column is referenced              | DAX editor | @messages-view | `te validate` |
| ----------------------------------------- | ---------- | --------------------------- | ------------- |
| Directly                                  | 是的         | 是的                          | 是的            |
| Indirectly, for example through a measure | 否          | 是的                          | 是的            |
| As a relationship endpoint                | 否          | 是的                          | 是的            |

An indirect violation has no squiggle in the editor, because the expression you are looking at is perfectly valid on its own. The chain is what breaks. Check the @messages-view before deploying.

A relationship-endpoint violation also appears as the relationship's **Error Message** property, and is reported once per offending endpoint, so a relationship with user-context columns on both sides produces two errors. Inactive relationships are checked too.

> [!IMPORTANT]
> `te validate --errors-only` does _not_ suppress these. They are errors, not warnings, and `--errors-only` only hides warnings and anti-patterns.

## 后续步骤

- @messages-view
- @dax-editor
- @偏好
