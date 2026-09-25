---
uid: object-properties-relationships
title: Relationship properties
author: Jeroen ter Heerdt
updated: 2026-09-23
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

This page covers the properties of relationships. For properties that most objects share, see @object-properties-common.

## Relationship

A relationship connects a column in one table to a column in another table, so that a filter on one table also filters the other. For example, a relationship from `Sales[ProductKey]` to `Product[ProductKey]` makes a filter on `Product[Color]` filter the rows of `Sales`.

Every relationship has a *from* side and a *to* side. In a typical one-to-many relationship, the *from* side is the table with many rows per key, such as a fact table, and the *to* side is the table with one row per key, such as a dimension table. Tabular Editor 3 shows a relationship in the TOM Explorer with the *from* column on the left and the *to* column on the right, for example `'Sales'[ProductKey] ∞←1 'Product'[ProductKey]`. The symbols in the middle show the cardinality of each side (`∞` for `Many`, `1` for `One`) and the filter direction: `←` for a single direction, `↔` for both directions. The name updates when you change the columns, the cardinalities or the cross filtering behavior.

Tabular Editor 2 also shows the *from* column on the left and the *to* column on the right, but without cardinality symbols. The arrow in the middle only shows the filter direction: `-->` for a single direction, `<-->` for both directions, for example `'Sales'[ProductKey] --> 'Product'[ProductKey]`.

You can create and edit relationships in the Properties view or, in Tabular Editor 3, visually in the @diagram-view. To create relationships from the primary and foreign keys defined in Databricks Unity Catalog, use the @script-create-databricks-relationships script.

### Common properties

- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Changed Properties](xref:object-properties-common#changed-properties)
- [Error Message](xref:object-properties-common#error-message)
- [Object Type](xref:object-properties-common#object-type)
- [State](xref:object-properties-common#state)

### Basic

#### From Column
`FromColumn` · Column

The column on the *from* side of the relationship. In a one-to-many relationship, this is usually the foreign key column in the fact table, for example `Sales[ProductKey]`. Choosing a column also sets **From Table**.

#### From Cardinality
`FromCardinality` · RelationshipEndCardinality

How many rows on the *from* side can have the same value in **From Column**.

| Value | Meaning |
|---|---|
| `Many` | Several rows can have the same value. This is the usual setting for the *from* side. |
| `One` | Each value appears at most once in the column. |
| `None` | The cardinality is unspecified. Don't use it. The relationship dialog in Tabular Editor 3 only offers `One` and `Many`, and the TOM Explorer shows `None` as `0`. |

#### To Column
`ToColumn` · Column

The column on the *to* side of the relationship. In a one-to-many relationship, this is the key column of the dimension table, for example `Product[ProductKey]`. Choosing a column also sets **To Table**.

The Best Practice Analyzer rule @kb.bpa-relationship-same-datatype flags relationships where **From Column** and **To Column** have different data types.

#### To Cardinality
`ToCardinality` · RelationshipEndCardinality

How many rows on the *to* side can have the same value in **To Column**. The values are the same as for **From Cardinality**. `One` is the usual setting.

Together, the two cardinalities give the type of relationship:

| From | To | Relationship |
|---|---|---|
| `Many` | `One` | Many-to-one. The standard relationship between a fact table and a dimension table. |
| `One` | `One` | One-to-one. Both columns must contain unique values. |
| `Many` | `Many` | Many-to-many. Neither column needs unique values. Needs compatibility level 1500 or higher. |

When a column on a `One` side contains duplicate values, refresh fails with an error. Many-to-many relationships are *limited* relationships: they don't add a blank row for missing keys, and they're often slower than many-to-one relationships. Use them only when the data really has no unique key.

There's no one-to-many relationship in TOM: the *from* side must always be the *many* side. Tabular Editor doesn't block **From Cardinality** `One` with **To Cardinality** `Many`, but the engine rejects it when you save, with the error *From end cardinality must always be set to Many, unless the relationship is One-To-One*. To relate the tables the other way, swap the from and to columns instead.

#### Active
`IsActive` · bool

Whether the relationship filters data automatically. Only one active path can exist between two tables. When you need a second relationship between the same tables, for example from `Sales[ShipDate]` to `Date[Date]` next to the active one from `Sales[OrderDate]`, set **Active** to `false` on it and turn it on in a measure with `USERELATIONSHIP`:

```dax
Sales by Ship Date =
CALCULATE ( [Total Sales], USERELATIONSHIP ( Sales[ShipDate], 'Date'[Date] ) )
```

The engine rejects a model where active relationships create more than one path between two tables. This happens most often when several relationships use bidirectional cross filtering.

In the Tabular Editor 3 diagram view, you can also right-click a relationship to activate or deactivate it.

#### ID
`ID` · string · read-only

The internal identifier of the relationship. In TOM, this is the relationship's name. Power BI Desktop uses a GUID. Tabular Editor 3 doesn't: it gives a new relationship a unique name that starts with `New Single Column Relationship`. You rarely need the ID, except to refer to a specific relationship in a C# script or a TMSL command. Tabular Editor 2 names a new relationship the same way.

### Options

#### From Table
`FromTable` · Table · read-only

The table that contains **From Column**. To change it, choose a different **From Column**. Tabular Editor 3 doesn't show this property in the Properties view, because **From Column** already includes the table. You can still read it in a C# script.

#### To Table
`ToTable` · Table · read-only

The table that contains **To Column**. To change it, choose a different **To Column**. Tabular Editor 3 doesn't show this property in the Properties view. You can still read it in a C# script.

#### Cross Filtering Behavior
`CrossFilteringBehavior` · CrossFilteringBehavior

Which direction filters flow through the relationship.

| Value | Meaning |
|---|---|
| `OneDirection` | A filter on the *to* table filters the *from* table, but not the other way around. For example, a filter on `Product` filters `Sales`. This is the default. |
| `BothDirections` | Filters flow both ways. A filter on `Sales` also filters `Product`, so a slicer on `Product` only shows products that have sales in the current filter. |
| `Automatic` | The engine analyzes the relationships and chooses one of the other behaviors by using heuristics. |

In practice, `Automatic` is the same as `BothDirections`. Both SQL Server 2025 Analysis Services and Power BI Desktop store a relationship saved with `Automatic` as `BothDirections`, and in Power BI Desktop a filter on the *from* table then filters the *to* table, as with `BothDirections`. Set `BothDirections` explicitly instead, so the model says what it does.

Use `BothDirections` with care. It makes queries slower, it can make results hard to predict, and it easily creates more than one path between two tables, which the engine rejects. A safer alternative is to keep the relationship one-directional and enable both directions only where you need it, in a measure with `CROSSFILTER ( Sales[ProductKey], Product[ProductKey], BOTH )`.

Bidirectional filtering doesn't apply to row-level security unless you also set **Security Filtering Behavior**.

The Best Practice Analyzer rule @kb.bpa-many-to-many-single-direction flags many-to-many relationships that filter in both directions.

#### Security Filtering Behavior
`SecurityFilteringBehavior` · SecurityFilteringBehavior

Which direction the filters of row-level security flow through the relationship. It's the same as **Apply security filter in both directions** in Power BI Desktop.

| Value | Meaning |
|---|---|
| `OneDirection` | Security filters flow from the *to* table to the *from* table only, even when **Cross Filtering Behavior** is `BothDirections`. This is the default. |
| `BothDirections` | Security filters flow both ways. Only valid when **Cross Filtering Behavior** is `BothDirections`. |
| `None` | Blocks security filters from flowing from the *one* side to the *many* side. It only applies to limited relationships where one table comes from a Power BI semantic model or Analysis Services database and the other table comes from a different data source, as in a composite model. Needs compatibility level 1561 or higher. |

Tabular Editor doesn't block `BothDirections` when **Cross Filtering Behavior** is `OneDirection`, but the engine rejects it when you save, with the error *cannot have SecurityFilterBehavior set to BothDirections when the CrossFilterBehavior is set to OneDirection*. The same happens when you change **Cross Filtering Behavior** back to `OneDirection` on a relationship that filters security in both directions: change **Security Filtering Behavior** first.

A typical use of `BothDirections` is dynamic row-level security, where a filter on a user table must reach a dimension table through a bridge table. See @roles-and-rls and @data-security-setup-rls. To check that security filters reach the right tables, test the role with impersonation. See @data-security-testing.

#### Join On Date Behavior
`JoinOnDateBehavior` · DateTimeRelationshipBehavior

How the engine matches values when both columns have the `DateTime` data type.

| Value | Meaning |
|---|---|
| `DateAndTime` | Values must match on both date and time. This is the default. |
| `DatePartOnly` | Only the date part is compared, and the time is ignored. For example, `2026-09-23 14:30` matches the date `2026-09-23` in a date table. |

Use `DatePartOnly` when the *from* column contains a date and time, and the *to* column is a date table with one row per day. Without it, only the values at exactly midnight would match. Power BI uses this setting for the relationships of its automatic date tables.

Power BI Desktop uses `DatePartOnly` for the relationships between a date/time column and its auto date/time table, so that a value such as `2026-01-15 14:30` still matches the date `2026-01-15`.

<!-- TODO (not verifiable from TE3 source): whether DatePartOnly works in DirectQuery. -->

#### Rely On Referential Integrity
`RelyOnReferentialIntegrity` · bool

For DirectQuery: when `true`, the engine assumes that every value in **From Column** exists in **To Column**. The SQL queries it sends to the source then use `INNER JOIN` instead of `OUTER JOIN`, which is usually faster. It's the same as **Assume referential integrity** in Power BI Desktop.

Only enable it when the source guarantees that every key has a match, for example through a foreign key constraint. If some rows on the *from* side have no match, they silently disappear from the results. The property has no effect on Import tables.

<!-- TODO (not verifiable from TE3 source): Microsoft's TOM documentation says this property is "unused; reserved for future use", while the TOM library's own description (shown in Tabular Editor) says DirectQuery queries use INNER JOIN when it's true. Confirm which engines and storage modes honor it. -->

#### Type
`Type` · RelationshipType · read-only

The kind of relationship. The only value is `SingleColumn`, a relationship between one column on each side. Tabular Editor 3 doesn't show this property in the Properties view.
