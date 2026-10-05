---
uid: object-properties-relationships
title: Relationship properties
author: Jeroen ter Heerdt
updated: 2026-10-05
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
# Relationship properties

<!--
SUMMARY: Reference for the properties of relationships, such as cardinality, cross filtering behavior and security filtering behavior.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

This page covers the properties of relationships. For properties that most objects share, see @object-properties-common.

## Relationship

A relationship connects a column in one table to a column in another table, and a filter on one table then also filters the other. For example, a relationship from `Sales[ProductKey]` to `Product[ProductKey]` makes a filter on `Product[Color]` filter the rows of `Sales`.

Every relationship has a *from* side and a *to* side. In a typical one-to-many relationship, the from side is the table with many rows per key, such as a fact table, and the to side is the table with one row per key, such as a dimension table.

Tabular Editor 3 shows a relationship in the **TOM Explorer** with the from column on the left and the to column on the right, for example `'Sales'[ProductKey] ∞←1 'Product'[ProductKey]`. The symbols in the middle show the cardinality of each side (`∞` for `Many`, `1` for `One`) and the filter direction (`←` for a single direction, `↔` for both directions). The name updates when you change the columns, the cardinalities or the cross filtering behavior. Tabular Editor 2 uses the same column order without cardinality symbols, and its arrow shows the filter direction as `-->` for a single direction or `<-->` for both directions, for example `'Sales'[ProductKey] --> 'Product'[ProductKey]`.

You can create and edit relationships in the **Properties** view or, in Tabular Editor 3, in the @diagram-view. To create relationships from the primary and foreign keys defined in Databricks Unity Catalog, use the @script-create-databricks-relationships script.

### Common properties

- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Changed Properties](xref:object-properties-common#changed-properties)
- [Error Message](xref:object-properties-common#error-message)
- [Object Type](xref:object-properties-common#object-type)
- [State](xref:object-properties-common#state)

### From Column
`FromColumn` · Column · Basic

The column on the from side of the relationship. In a one-to-many relationship, this is usually the foreign key column in the fact table, for example `Sales[ProductKey]`. Choosing a column also sets `FromTable`.

### From Cardinality
`FromCardinality` · RelationshipEndCardinality · Basic

How many rows on the from side can have the same value in `FromColumn`.

| Value | Meaning |
|---|---|
| `Many` | Several rows can have the same value. The usual setting for the from side. |
| `One` | Each value appears at most once in the column. |
| `None` | The cardinality is unspecified. Don't use it. The relationship dialog in Tabular Editor 3 lists only `One` and `Many`, and the **TOM Explorer** shows `None` as `0`. |

### To Column
`ToColumn` · Column · Basic

The column on the to side of the relationship. In a one-to-many relationship, this is the key column of the dimension table, for example `Product[ProductKey]`. Choosing a column also sets `ToTable`.

The Best Practice Analyzer (BPA) rule @kb.bpa-relationship-same-datatype flags relationships where `FromColumn` and `ToColumn` have different data types.

### To Cardinality
`ToCardinality` · RelationshipEndCardinality · Basic

How many rows on the to side can have the same value in `ToColumn`. The values are the same as for `FromCardinality`, and `One` is the usual setting. The two cardinalities together set the type of relationship:

| From | To | Relationship |
|---|---|---|
| `Many` | `One` | Many-to-one. The standard relationship between a fact table and a dimension table. |
| `One` | `One` | One-to-one. Both columns must contain unique values. |
| `Many` | `Many` | Many-to-many. Neither column needs unique values. Needs compatibility level 1500 or higher. |

When a column on a `One` side contains duplicate values, refresh fails with an error. Many-to-many relationships are *limited* relationships: they don't add a blank row for missing keys, and they're often slower than many-to-one relationships. Use them only when the data has no unique key.

In the Tabular Object Model (TOM), the from side is always the many side of a one-to-many relationship. Tabular Editor accepts `FromCardinality` `One` with `ToCardinality` `Many`, and the engine rejects it when you save, with the error "From end cardinality must always be set to Many, unless the relationship is One-To-One". To relate the tables the other way, swap the from and to columns.

### Active
`IsActive` · bool · Basic

Whether the relationship filters data automatically. The engine rejects a model where active relationships create more than one path between two tables. This happens most often when several relationships use bidirectional cross filtering.

For a second relationship between the same tables, for example from `Sales[ShipDate]` to `Date[Date]` next to the active one from `Sales[OrderDate]`, set `IsActive` to `false` and turn the relationship on in a measure with [USERELATIONSHIP](https://dax.guide/userelationship):

```dax
Sales by Ship Date =
CALCULATE ( [Total Sales], USERELATIONSHIP ( Sales[ShipDate], 'Date'[Date] ) )
```

In the Tabular Editor 3 diagram view, you can also right-click a relationship to activate or deactivate it.

### ID
`ID` · string · Basic · read-only

The internal identifier of the relationship, which is the relationship's name in TOM. Power BI Desktop uses a GUID. Tabular Editor 3 and Tabular Editor 2 give a new relationship a unique name that starts with `New Single Column Relationship`. Use the ID to refer to a specific relationship in a C# script or a Tabular Model Scripting Language (TMSL) command.

### From Table
`FromTable` · Table · Options · read-only

The table that contains `FromColumn`. To change it, choose a different `FromColumn`. Tabular Editor 3 hides this property in the **Properties** view, where `FromColumn` already shows the table. You can still read it in a C# script.

### To Table
`ToTable` · Table · Options · read-only

The table that contains `ToColumn`. To change it, choose a different `ToColumn`. Tabular Editor 3 hides this property in the **Properties** view. You can still read it in a C# script.

### Cross Filtering Behavior
`CrossFilteringBehavior` · CrossFilteringBehavior · Options

The direction filters flow through the relationship.

| Value | Meaning |
|---|---|
| `OneDirection` | A filter on the to table filters the from table. For example, a filter on `Product` filters `Sales`. The default. |
| `BothDirections` | Filters flow both ways. A filter on `Sales` also filters `Product`, so a slicer on `Product` shows only products that have sales in the current filter. |
| `Automatic` | The engine analyzes the relationships and picks one of the other behaviors by using heuristics. |

SQL Server 2025 Analysis Services and Power BI Desktop both store a relationship saved with `Automatic` as `BothDirections`. In Power BI Desktop, a filter on the from table then filters the to table, as with `BothDirections`. Set `BothDirections` explicitly when you want filters to flow both ways.

`BothDirections` makes queries slower and makes it more likely that active relationships create more than one path between two tables, which the engine rejects. To filter in both directions for one measure, keep the relationship one-directional and use [CROSSFILTER](https://dax.guide/crossfilter) in the measure, for example `CROSSFILTER ( Sales[ProductKey], Product[ProductKey], BOTH )`.

Bidirectional filtering applies to row-level security only when you also set `SecurityFilteringBehavior`. The BPA rule @kb.bpa-many-to-many-single-direction flags many-to-many relationships that filter in both directions.

### Security Filtering Behavior
`SecurityFilteringBehavior` · SecurityFilteringBehavior · Options

The direction the filters of row-level security flow through the relationship. It matches **Apply security filter in both directions** in Power BI Desktop.

| Value | Meaning |
|---|---|
| `OneDirection` | Security filters flow from the to table to the from table only, even when `CrossFilteringBehavior` is `BothDirections`. The default. |
| `BothDirections` | Security filters flow both ways. Valid only when `CrossFilteringBehavior` is `BothDirections`. |
| `None` | Blocks security filters from flowing from the one side to the many side. Applies only to limited relationships in a composite model, where one table comes from a Power BI semantic model or Analysis Services database and the other from a different data source. Needs compatibility level 1561 or higher. |

Tabular Editor accepts `BothDirections` when `CrossFilteringBehavior` is `OneDirection`, and the engine rejects it when you save, with the error "cannot have SecurityFilterBehavior set to BothDirections when the CrossFilterBehavior is set to OneDirection". The same error occurs when you change `CrossFilteringBehavior` back to `OneDirection` on a relationship that filters security in both directions, so change `SecurityFilteringBehavior` first.

A typical use of `BothDirections` is dynamic row-level security, where a filter on a user table reaches a dimension table through a bridge table. See @roles-and-rls and @data-security-setup-rls. To check that security filters reach the right tables, test the role with impersonation. See @data-security-testing.

### Join On Date Behavior
`JoinOnDateBehavior` · DateTimeRelationshipBehavior · Options

How the engine matches values when both columns have the `DateTime` data type.

| Value | Meaning |
|---|---|
| `DateAndTime` | Values must match on both date and time. The default. |
| `DatePartOnly` | The engine compares only the date part and ignores the time. For example, `2026-09-23 14:30` matches the date `2026-09-23` in a date table. |

Use `DatePartOnly` when the from column contains a date and time and the to column is a date table with one row per day. With `DateAndTime`, only the values at exactly midnight match. Power BI Desktop uses `DatePartOnly` for the relationships between a date/time column and its auto date/time table.

<!-- TODO (not verifiable from TE3 source): whether DatePartOnly works in DirectQuery. -->

### Rely On Referential Integrity
`RelyOnReferentialIntegrity` · bool · Options

For DirectQuery: when `true`, the engine assumes that every value in `FromColumn` exists in `ToColumn`, and the SQL queries it sends to the source use `INNER JOIN`. When `false`, they use `OUTER JOIN`. `INNER JOIN` is usually faster. It matches **Assume referential integrity** in Power BI Desktop. The property has no effect on import tables.

Enable it only when the source guarantees that every key has a match, for example through a foreign key constraint. If rows on the from side have no match, they're missing from the results without an error.

<!-- TODO (not verifiable from TE3 source): Microsoft's TOM documentation says this property is "unused; reserved for future use", while the TOM library's own description (shown in Tabular Editor) says DirectQuery queries use INNER JOIN when it's true. Confirm which engines and storage modes honor it. -->

### Type
`Type` · RelationshipType · Options · read-only

The kind of relationship. The only value is `SingleColumn`, a relationship between one column on each side. Tabular Editor 3 hides this property in the **Properties** view.
