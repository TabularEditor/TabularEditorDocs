---
uid: object-properties-tables
title: Table properties
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
# Table properties

<!--
SUMMARY: Reference for the properties of tables, calculated tables and calculation group tables.
-->

This page covers the properties of the three kinds of tables in a semantic model: regular tables, calculated tables and calculation group tables. Calculated tables and calculation group tables are based on a regular table, so the shared properties are described once, under [Table](#table). The sections for the other two kinds cover what they add and which table properties the Properties view hides for them. For properties that most objects share, see @object-properties-common.

## Table

A table holds rows of data in columns, and it's also the container for the measures and hierarchies that belong to it. A regular table gets its data from one or more partitions, each with a query against a data source, for example a Power Query (M) expression or a SQL query. How the data gets there depends on the partition's mode: import, DirectQuery or Direct Lake.

In Tabular Editor 3, you add tables from a data source with @import-tables, and you look at a table's data with @table-preview.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Hidden](xref:object-properties-common#hidden)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Changed Properties](xref:object-properties-common#changed-properties)
- [DAX identifier](xref:object-properties-common#dax-identifier)
- [Error Message](xref:object-properties-common#error-message)
- [Object Type](xref:object-properties-common#object-type)
- [Lineage Tag](xref:object-properties-common#lineage-tag)
- [Source Lineage Tag](xref:object-properties-common#source-lineage-tag)
- [Translated Names](xref:object-properties-common#translated-names)
- [Translated Descriptions](xref:object-properties-common#translated-descriptions)
- [Synonyms](xref:object-properties-common#synonyms)
- [Shown in Perspective](xref:object-properties-common#shown-in-perspective)

### Basic

#### Table Group
`TableGroup` · string · *stored as an annotation* (`TabularEditor_TableGroup`)

The table group the table appears in, in the TOM Explorer of Tabular Editor 3. Table groups work like folders for tables and help you find your way in a large model, for example by keeping fact tables, dimension tables and calculation groups apart. Leave it empty to show the table at the top level.

Table groups can't be nested, and client tools such as Power BI and Excel ignore them. Tabular Editor stores the group in an annotation called `TabularEditor_TableGroup` on the table, so the grouping is saved with the model and other developers see the same groups. The Properties view only shows **Table Group** while table groups are turned on in the TOM Explorer. See @table-groups.

In the TOM Explorer, you can also right-click tables and use **Move to group**, or drag tables onto a table group (see @drag-drop). To put all tables in groups at once, based on their type and relationships, run the @script-create-table-groups script.

### Incremental Refresh

#### Enabled
`EnableRefreshPolicy` · bool · *shortcut*: adds or removes the table's **Refresh Policy**

Turns incremental refresh on or off for the table. When you set it to `true`, Tabular Editor adds a refresh policy to the table, and the **Refresh Policy** property appears so you can configure it. When you set it back to `false`, Tabular Editor removes the refresh policy object from the table. It doesn't touch the table's partitions: any policy range partitions that the policy created stay in the table. To turn the table back into a table with a regular M partition, follow the steps in [Removing Incremental Refresh](xref:incremental-refresh-policy#removing-incremental-refresh-using-tabular-editor).

Incremental refresh is only available for Power BI and Fabric models. The Properties view only shows **Enabled** and **Refresh Policy** when the model's compatibility mode is Power BI, the compatibility level is 1450 or higher, and the table either has no partitions yet or has M or query partitions in import or dual mode. For Analysis Services models, you create and manage the partitions yourself. See @incremental-refresh-about and @incremental-refresh-setup.

The @script-implement-incremental-refresh script sets up a refresh policy based on a date column you select, including the `RangeStart` and `RangeEnd` parameters.

#### Refresh Policy
`RefreshPolicy` · BasicRefreshPolicy

The incremental refresh policy of the table. Expand it in the Properties view to set how much history to keep, how much to refresh, the source expression and the other settings of the policy. The individual settings are described under refresh policy on @object-properties-partitions. See also @incremental-refresh-policy.

A refresh policy doesn't create partitions by itself. The engine creates the policy range partitions the first time the policy is applied, for example when you refresh the table in the Power BI service, or when you right-click the table in the TOM Explorer of Tabular Editor 3 and choose **Apply refresh policy**. Tabular Editor only applies the policy when it's connected to the model and you've saved all changes to it first.

In Tabular Editor 2, right-click the table in the TOM Explorer and choose **Apply Refresh Policy**. It has the same requirements.

To change an existing policy, see @incremental-refresh-modify. In Tabular Editor 3, the @advanced-refresh dialog can apply the refresh policy with an effective date other than today, so you can test how the policy behaves at a different point in time.

### Metadata

#### Source
`Source` · string · *computed* · read-only

The name of the legacy (provider) data source that the table's first partition queries. It's a quick way to see where a table comes from without opening its partitions. Tabular Editor only looks at the first partition, so if the partitions use different data sources, you only see the first one.

The Properties view only shows **Source** when the first partition is a query partition or an M partition. For an M partition it's empty, because M partitions don't refer to a data source object: the connection is part of the M expression. It isn't shown for calculated tables, calculation group tables, Direct Lake tables or tables with policy range partitions.

To go the other way and list the tables that use an explicit (legacy) data source, run the @script-show-data-source-dependencies script.

#### Source Type
`SourceType` · PartitionSourceType · read-only · *shortcut to* **Source Type** of the first partition

The kind of source the table's partitions use. It tells you at a glance whether the table is imported with M, part of a Direct Lake model, and so on. Tabular Editor takes it from the table's first partition, so for a table with partitions of different kinds, you see the kind of the first one. A table without partitions shows `None`.

The Properties view doesn't show **Source Type** on calculated tables and calculation group tables. In a C# script, those return `Calculated` and `CalculationGroup`.

| Value | Meaning |
|---|---|
| `Query` | The partitions run a query, for example SQL, against a legacy (provider) data source. |
| `Calculated` | The table is a calculated table. Its data comes from a DAX expression. |
| `None` | The source isn't defined. The data is pushed into the table, for example in a push semantic model in Power BI. |
| `M` | The partitions use a Power Query (M) expression. This is the most common value in Power BI models. Compatibility level 1400+. |
| `Entity` | The partitions read a named entity, such as a table in a lakehouse or warehouse. Direct Lake tables use this. Compatibility level 1400+. |
| `PolicyRange` | The partitions were created by an incremental refresh policy. Compatibility level 1450+. |
| `CalculationGroup` | The table is a calculation group table. Compatibility level 1470+. |
| `Inferred` | The engine generates the query that fills the partition. Compatibility level 1563+. |

<!-- TODO (not verifiable from TE3 source): which kind of partition uses Inferred. TOM only says "The data in this partition is populated by executing a query generated by the system." -->

### Options

#### Alternate Source Precedence
`AlternateSourcePrecedence` · int · compatibility level 1460+

The order in which the engine considers this table when it looks for an aggregation table that can answer a query. It's only relevant when the table is an aggregation table, that is, when some of its columns have **Alternate Of** set to a column in a detail table. When more than one aggregation table can answer a query, the engine uses the one with the highest value.

Typically you give a small, highly summarized aggregation table a higher value than a larger, more detailed one, so the engine tries the smaller table first. The default is `0`. In Power BI Desktop, this is the **Precedence** setting in **Manage aggregations**. To set up an aggregation table in Tabular Editor, see @user-defined-aggregations. The @script-implement-user-defined-aggregations script automates those steps for a fact table you select.

#### Calendars
`Calendars` · collection of Calendar · read-only

The custom calendars defined on the table. A calendar tells the engine which columns of a date table hold the year, quarter, month, week and date, so that calendar-based time intelligence functions work with fiscal, retail or other non-standard calendars. Custom calendars need compatibility level 1701 or higher. See @object-properties-calendars.

In Tabular Editor 3, right-click a table and choose **Create > Calendar...** to add a calendar, then map its columns in the Calendar Editor. See @calendars.

#### Data Category
`DataCategory` · string

Tells client tools what kind of data the table holds. In practice, the only value that matters in Power BI is `Time`: it marks the table as a date table. Power BI then uses the table's date column (the column with **Key** set to `true`) for time intelligence and turns off the auto date/time table for it. When you use **Mark as date table** in Power BI Desktop, this is what it sets.

Leave it empty, or set it to `Regular`, for all other tables. The other values come from multidimensional models and only some Excel features and older client tools use them: `Geography`, `Organization`, `BillOfMaterials`, `Accounts`, `Customers`, `Products`, `Scenario`, `Quantitative`, `Utility`, `Currency`, `Rates`, `Channel` and `Promotion`. The dropdown in the Properties view lists these values and `Unknown`, but you can also type a value yourself.

<!-- TODO (not verifiable from TE3 source): whether an empty value and "Regular" behave the same in the engine and client tools, and which client tools use the values other than Time. -->

In Tabular Editor, you can also right-click the table in the @tom-explorer-view and choose **Mark as date table...**. The Best Practice Analyzer rule @kb.bpa-date-table-exists flags models that have no date table. To create a date table from the date columns in your model, run the @script-create-date-table script, which also sets **Data Category** to `Time`.

#### Default Detail Rows Expression
`DefaultDetailRowsExpression` · string · compatibility level 1400+

A DAX table expression that defines the rows a user sees when they drill through on a measure in this table, for example with **Show Details** in an Excel PivotTable. It applies to every measure in the table that doesn't have its own **Detail Rows Expression** (see @object-properties-measures).

For example, to show the order number, customer and amount for each sales row:

```dax
SELECTCOLUMNS (
    Sales,
    "Order", Sales[OrderNumber],
    "Customer", RELATED ( Customer[Name] ),
    "Amount", Sales[Amount]
)
```

Power BI doesn't use this property. See @detail-rows-expression. In Tabular Editor 3, you write the expression in the Expression Editor of the @dax-editor, with auto-complete and parameter info. To remove the expression, clear the value.

#### Direct Lake Indexing Behavior
`DirectLakeIndexingBehavior` · DirectLakeIndexingBehavior · Preview compatibility level

Controls when the engine builds and saves the indexes it uses for a Direct Lake table. Building indexes takes time. Doing it during a refresh means the first queries after a refresh are faster, and doing it on demand means refreshes are faster. It only applies to tables in Direct Lake mode.

TOM doesn't assign this property a released compatibility level yet, so the Properties view in the current version of Tabular Editor 3 hides it for every model.

| Value | Meaning |
|---|---|
| `Default` | Use the model's default, set with **Default Direct Lake Indexing Behavior** on @object-properties-model. |
| `Auto` | The engine may build in-memory indexes when it loads data or runs a query. |
| `Full` | The engine builds and saves the indexes as part of a full refresh, a calculate refresh and a refresh of type indexes. |
| `Explicit` | The engine only builds and saves the indexes when you explicitly run a refresh of type indexes. Other refresh types don't build them. |

<!-- TODO (not verifiable from TE3 source): the behavior of each value and which indexes this covers; check the Microsoft documentation once the feature is out of preview. -->

#### Exclude From Automatic Aggregations
`ExcludeFromAutomaticAggregations` · bool · compatibility level 1572+

When `true`, the table isn't used when Power BI builds automatic aggregations. Automatic aggregations are a Power BI Premium and Fabric feature for DirectQuery models: the service watches the queries and creates aggregation tables for you. Set this property on a table you don't want included, for example because its data changes too often for a cached aggregation to be useful.

<!-- TODO (not verifiable from TE3 source): the exact effect. TOM only says "An indication whether the table is excluded from the automatic aggregations feature." Is the table excluded as a source for aggregations, or are queries against it never answered from aggregations? -->

#### Exclude From Model Refresh
`ExcludeFromModelRefresh` · bool · compatibility level 1480+

When `true`, a refresh of the whole model doesn't refresh this table's partitions if they already hold data. You can still refresh the table by selecting it explicitly. Use it for tables that rarely change or are expensive to load, such as a large historical table or a table filled with a separate process, so that a scheduled model refresh doesn't reload them every time.

Partitions that don't hold data yet are still refreshed, so a new or cleared table gets loaded.

In Tabular Editor 3, you refresh a single table by right-clicking it in the TOM Explorer and choosing **Refresh table**. See @refresh-preview-query.

On SQL Server 2025 Analysis Services, every type of model-level refresh skips the table when its partitions already hold data: **Full**, **Automatic**, **Data only** and **Calculate**. The exception is **Clear values**, which does clear the table's data. The next model refresh then loads the table again, because its partitions are empty.

#### Partitions
`Partitions` · collection of Partition · read-only

The partitions of the table. Each partition defines where a part of the table's data comes from, for example an M expression, and each can be refreshed separately. Most tables have a single partition. Large import tables often have one partition per period, either created by you or by an incremental refresh policy.

Click the ellipsis button to open the collection editor, where you can add, remove and edit partitions. See @object-properties-partitions.

The Properties view only shows **Partitions** when the table's first partition is an M partition or a query partition. It doesn't show it for calculated tables (including field parameters), calculation group tables, Direct Lake tables or tables with policy range partitions. To view and edit the partitions of calculated tables and calculation group tables anyway, run the @script-edit-hidden-partitions script.

#### Private
`IsPrivate` · bool · compatibility level 1400+

When `true`, client tools don't show the table at all, not even to developers who choose to see hidden objects. Power BI Desktop uses this for the date table template that the auto date/time feature uses to create its date tables (the table named `DateTableTemplate_` followed by a GUID). You rarely need to set it yourself.

It's always available in Power BI models. In Analysis Services models it needs compatibility level 1400 or higher. SQL Server 2025 Analysis Services stores the flag but doesn't act on it: the table is still listed in the schema information that client tools read, you can query it with DAX, and measures in other tables can use it.

Like **Hidden**, this isn't a security feature. To secure a table, use object-level security (see **Object Level Security** below).

In Power BI Desktop, a private table doesn't appear in the **Data** pane at all, unlike a hidden table, which you can still show there. It still works in DAX: you can query it, and measures in other tables can use it. It's also still listed in the schema information that the engine returns.

The Best Practice Analyzer rule @kb.bpa-remove-auto-date-table flags the `DateTableTemplate_` and `LocalDateTable_` tables that auto date/time creates, so you can replace them with a single date table.

#### Sets
`Sets` · collection of Set · read-only

The calculated sets defined on the table. A set is a named DAX expression that returns a set of members, which client tools can offer as a predefined selection. Sets are only supported in Power BI models: the Properties view only shows **Sets** when the model's compatibility mode is Power BI and the compatibility level is 1400 or higher. Sets don't appear as objects in the TOM Explorer, so you add and edit them here, in the collection editor. See @object-properties-functions.

<!-- TODO (not verifiable from TE3 source): what calculated sets are used for, and which client tools support them. -->

#### Show As Variations Only
`ShowAsVariationsOnly` · bool · compatibility level 1400+

When `true`, client tools don't show the table in the field list on its own. It only appears through a column variation that points to it. Power BI Desktop uses this for the date tables that auto date/time creates (the tables named `LocalDateTable_` followed by a GUID): you see them as the date hierarchy under a date column, and not as separate tables. See **Variations** on @object-properties-columns.

It's always available in Power BI models. In Analysis Services models it needs compatibility level 1400 or higher. SQL Server 2025 Analysis Services stores the flag but doesn't act on it: the table is still listed in the schema information that client tools read, you can query it with DAX, and measures in other tables can use it.

#### System Managed
`SystemManaged` · bool · compatibility level 1562+

When `true`, the engine or the service owns the table: it creates and deletes it, and you shouldn't change it by hand. Don't set this property on your own tables. Tabular Editor doesn't stop you from editing a system-managed table, so take care not to change one by accident.

The auto date/time tables that Power BI Desktop creates aren't system-managed: Desktop marks the template table as hidden and private, and each local date table as hidden with **Show As Variations Only**.

<!-- TODO (not verifiable from TE3 source): which features create system-managed tables, for example automatic aggregations. -->

### Translations, Perspectives, Security

#### Object Level Security
`ObjectLevelSecurity` · per role · compatibility level 1400+ · *shortcut to* the table permissions of each role

The object-level security (OLS) permission of the table in each role of the model. Expand the property to see one entry per role. The Properties view only shows the property when the model has at least one role. The values are:

| Value | Meaning |
|---|---|
| `Default` | No permission is set for this role. Members of the role can see the table. |
| `Read` | Members of the role can see and query the table. |
| `None` | The table is hidden from members of the role, together with everything that depends on it. Queries and measures that refer to it return an error for them. |

Unlike **Hidden** and **Private**, OLS is a real security feature: the table and its metadata don't exist for members of the role. Use it with care, because every measure that refers to the table fails for those users. Tabular Editor stores the permission in the table permission of each role. See @data-security-setup-ols and @object-properties-security.

To check that OLS and RLS work as intended, test them with impersonation in Tabular Editor 3. See @data-security-testing.

#### Row Level Security
`RowLevelSecurity` · per role · read-only · *shortcut to* the table permissions of each role

The row-level security (RLS) filter of the table in each role of the model. Expand the property to see one entry per role. Each entry is a DAX expression that returns `TRUE` for the rows that members of the role may see, for example:

```dax
Customer[Country] = "Denmark"
```

The property itself is read-only, but you can edit each role's entry, and the entries accept multi-line expressions. The Properties view only shows the property when the model has at least one role.

Leave an entry empty to not filter the table for that role. Filters also flow along relationships, so filtering a dimension table also filters the fact tables it's related to. Tabular Editor stores the filter in the table permission of each role. See @roles-and-rls, @data-security-setup-rls and @object-properties-security.

## Calculated table

A calculated table gets its data from a DAX expression instead of from a data source, for example a date table built with `CALENDAR` or a table that summarizes another table. The engine evaluates the expression when you refresh the table or the model, and stores the result like any other imported table.

A calculated table has all the properties of a [table](#table), plus **Expression**.

A calculated table has exactly one partition, which Tabular Editor manages for you, and it can't have an incremental refresh policy. That's why the Properties view hides **Partitions**, **Source**, **Source Type**, **Enabled** and **Refresh Policy** on calculated tables. **Alternate Source Precedence** is still shown.

Field parameters in Power BI are calculated tables too. The @create-field-parameter script creates one from the columns or measures you select.

### Common properties

The same as on [tables](#table).

### Options

#### Expression
`Expression` · string

The DAX expression that returns the table's rows. It must return a table, for example:

```dax
ADDCOLUMNS (
    CALENDAR ( DATE ( 2020, 1, 1 ), DATE ( 2030, 12, 31 ) ),
    "Year", YEAR ( [Date] ),
    "Month", FORMAT ( [Date], "mmm" )
)
```

The table's columns come from the expression: each column the expression returns becomes a calculated table column (see @object-properties-columns). In Tabular Editor 3, the columns change as soon as you change the expression: Tabular Editor works them out with its own DAX semantic analysis, so this also works when you edit a model file without a connection to Analysis Services or Power BI (see @creating-and-testing-dax). Adding, removing or renaming columns this way can affect other DAX expressions that refer to the table, and hierarchies that use its columns.

Tabular Editor 2 doesn't analyze the expression. It only updates the columns when you save the model to a database you're connected to: after the save, it reloads the table's columns from the server. When you edit a model file, the columns don't change with the expression.

Edit the expression in the Expression Editor. In Tabular Editor 3, the Expression Editor of the @dax-editor offers auto-complete and parameter info. The engine recalculates the table's data when the table is refreshed, and also when a table it depends on is refreshed.

After you change the expression, refresh the table before you use it in a report. See [Refreshing data](xref:refresh-preview-query#refreshing-data).

## Calculation group table

A calculation group table is the table that holds a calculation group. It has one column, whose values are the names of the calculation items, and usually an ordinal column that sets the order of the items. Report authors use the column like any other column, for example in a slicer, and the selected calculation item changes how the measures in the report are calculated. See @object-properties-calculation-groups for the properties of the calculation group and its items.

Microsoft documents calculation groups for compatibility level 1500 or higher, which includes all Power BI semantic models. Tabular Editor 3 already offers **Create > Calculation Group** from compatibility level 1470, the level at which TOM added calculation groups.

A calculation group table is a table, plus the properties below. Most of them are shortcuts to properties of the calculation group that the table holds, so you can edit them without selecting the calculation group itself.

Many table properties don't apply to a calculation group table, because its data doesn't come from a data source, so the Properties view hides them. Of the table properties, it only shows the common properties listed below, **Table Group** and **Default Detail Rows Expression**. Calculation groups don't support detail rows expressions, row-level security or object-level security, so leave **Default Detail Rows Expression** empty.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Hidden](xref:object-properties-common#hidden)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Object Type](xref:object-properties-common#object-type)
- [Translated Names](xref:object-properties-common#translated-names)
- [Translated Descriptions](xref:object-properties-common#translated-descriptions)
- [Shown in Perspective](xref:object-properties-common#shown-in-perspective)

### Basic

#### Calculation Group Description
`CalculationGroupDescription` · string · *shortcut to* **Description** of the calculation group

The description of the calculation group. It's stored on the calculation group, not on the table, and it's separate from the table's own **Description**. Client tools don't show it. In the **Data** pane of Power BI Desktop, hovering over a calculation group table shows the table's own **Description**, not this one, and Excel's field list shows no descriptions at all. So put the text you want users to see in the table's **Description**, and use this property for notes to other developers.

#### Calculation Group Precedence
`CalculationGroupPrecedence` · int · *shortcut to* **Precedence** of the calculation group

The order in which the calculation group is applied when a query uses more than one calculation group. It's a shortcut to **Precedence** on the calculation group. See **Precedence** on @object-properties-calculation-groups for how it works.

### Metadata

#### Calculation Group Annotations
`CalculationGroupAnnotations` · collection of name/value pairs · read-only · *shortcut to* **Annotations** of the calculation group

The annotations stored on the calculation group, as opposed to the annotations on the table (see [Annotations](xref:object-properties-common#annotations)). Tools rarely use these. The property itself is read-only, but you can click the ellipsis button to open the annotation editor, where you add, change and remove the annotations. You can only do this with one calculation group table selected.

### Options

#### Multiple or Empty Selection Expression
`MultipleOrEmptySelectionExpression` · string · compatibility level 1605+ · *shortcut to* the calculation group

A DAX expression that the engine uses instead of the measure when the filter on the calculation group selects more than one calculation item, or selects none because the filter doesn't match any item. Without it, the calculation group isn't applied in those cases. What measures then return depends on [Selection Expression Behavior](xref:object-properties-model#selection-expression-behavior) on the model: with `Automatic` or `NonVisual` they return their normal value, and with `Visual` they return a blank value. A normal value can be misleading, for example when a user selects two currencies in a currency conversion calculation group and sees a total that isn't in either currency.

Use `SELECTEDMEASURE()` to refer to the measure. For example, to return an error message:

```dax
ERROR ( "Select a single currency." )
```

Or to return a blank value:

```dax
BLANK ()
```

Multiple or empty selection expressions need compatibility level 1605 or higher. Below that level, the Properties view doesn't show this property or the other selection expression properties below. To remove the expression, clear the value.

In Tabular Editor 3, you write the expression in the Expression Editor of the @dax-editor, with auto-complete and parameter info.

#### Multiple or Empty Selection Expression Description
`MultipleOrEmptySelectionDescription` · string · *shortcut to* the calculation group

A description of the multiple or empty selection expression, for other developers. Client tools don't show it to report authors.

#### Multiple or Empty Selection Format String Expression
`MultipleOrEmptySelectionFormatStringExpression` · string · *shortcut to* the calculation group

A DAX expression that returns the format string to use when the multiple or empty selection expression applies. It works like **Format String Expression** on a calculation item. Inside the expression, `SELECTEDMEASUREFORMATSTRING()` returns the format string of the measure.

#### No-selection Expression
`NoSelectionExpression` · string · compatibility level 1605+ · *shortcut to* the calculation group

A DAX expression that the engine uses instead of the measure when there's no filter on the calculation group at all, that is, when the user hasn't selected any calculation item. Without it, measures return their normal value when nothing is selected.

Use it to set a default calculation that users can still override by selecting a calculation item. For example, in a currency conversion calculation group, you can convert amounts to the currency selected in a `Currency` table without the user having to pick a calculation item. Sales amounts are stored in US dollars, and a `Currency Rate` table holds the daily exchange rates:

```dax
IF (
    SELECTEDVALUE ( 'Currency'[CurrencyName], "US Dollar" ) = "US Dollar",
    SELECTEDMEASURE (),
    SUMX (
        VALUES ( 'Date'[Date] ),
        CALCULATE ( DIVIDE ( SELECTEDMEASURE (), MAX ( 'Currency Rate'[EndOfDayRate] ) ) )
    )
)
```

No-selection expressions need compatibility level 1605 or higher.

#### No-selection Expression Description
`NoSelectionExpressionDescription` · string · *shortcut to* the calculation group

A description of the no-selection expression, for other developers. Client tools don't show it to report authors.

#### No-selection Format String Expression
`NoSelectionFormatStringExpression` · string · *shortcut to* the calculation group

A DAX expression that returns the format string to use when the no-selection expression applies. It works like **Format String Expression** on a calculation item. Inside the expression, `SELECTEDMEASUREFORMATSTRING()` returns the format string of the measure.
