---
uid: object-properties-tables
title: Table properties
author: Jeroen ter Heerdt
updated: 2026-10-09
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

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

This page covers the properties of the three kinds of tables in a semantic model: regular tables, calculated tables and calculation group tables. The [Table](#table) section describes the properties all three share. The sections for calculated tables and calculation group tables list what they add and which table properties the **Properties** view hides for them. For properties that most objects share, see @object-properties-common.

## Table

A table holds rows of data in columns and contains the measures and hierarchies that belong to it. A regular table gets its data from one or more partitions, each with a query against a data source, for example a Power Query (M) expression or a SQL query. The partition's mode sets how the data is loaded: import, DirectQuery or Direct Lake.

In Tabular Editor 3, you add tables from a data source with @import-tables and view a table's data with @table-preview.

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

### Table Group
`TableGroup` · string · Basic · *stored as an annotation* (`TabularEditor_TableGroup`)

The table group that contains the table in the **TOM Explorer** of Tabular Editor 3. Table groups work like folders for tables, for example to keep fact tables, dimension tables and calculation groups apart. Leave it empty to show the table at the top level. Table groups can't be nested, and client tools such as Power BI and Excel ignore them.

The group is saved with the model in the `TabularEditor_TableGroup` annotation, so other developers see the same groups. The **Properties** view shows `TableGroup` only while table groups are turned on in the **TOM Explorer**. See @table-groups.

In the **TOM Explorer**, you can also right-click tables and choose **Move to group**, or drag tables onto a table group (see @drag-drop). The @script-create-table-groups script puts all tables in groups based on their type and relationships.

### Enabled
`EnableRefreshPolicy` · bool · Incremental Refresh · *shortcut*: adds or removes the table's **Refresh Policy**

Turns incremental refresh on or off for the table. Setting it to `true` adds a refresh policy to the table and shows the `RefreshPolicy` property. Setting it to `false` removes the refresh policy object and leaves the table's partitions as they are, including any policy range partitions the policy created. To turn the table back into a table with a regular M partition, follow the steps in [Removing Incremental Refresh](xref:incremental-refresh-policy#removing-incremental-refresh-using-tabular-editor).

Incremental refresh is available for Power BI and Fabric models only. The **Properties** view shows `EnableRefreshPolicy` and `RefreshPolicy` when all of these are true:

- the model's compatibility mode is Power BI
- the compatibility level is 1450 or higher
- the table has no partitions yet, or has M or query partitions in import or dual mode

For Analysis Services models, you create and manage the partitions yourself. See @incremental-refresh-about and @incremental-refresh-setup. The @script-implement-incremental-refresh script sets up a refresh policy based on a date column you select, including the `RangeStart` and `RangeEnd` parameters.

### Refresh Policy
`RefreshPolicy` · BasicRefreshPolicy · Incremental Refresh · compatibility level 1450+

The incremental refresh policy of the table. Expand it in the **Properties** view to set how much history to keep, how much to refresh, the source expression and the other policy settings. The settings are described under refresh policy on @object-properties-partitions. See also @incremental-refresh-policy.

The engine creates the policy range partitions the first time the policy is applied, for example when you refresh the table in the Power BI service. To apply the policy from Tabular Editor 3, right-click the table in the **TOM Explorer** and choose **Apply refresh policy**. In Tabular Editor 2, the menu option is **Apply Refresh Policy**. Both versions apply the policy only when they're connected to the model and you've saved all changes first.

To change an existing policy, see @incremental-refresh-modify. In Tabular Editor 3, you can apply the refresh policy with an effective date other than today in the @advanced-refresh dialog, to test how the policy behaves at a different point in time.

### Source
`Source` · string · Metadata · read-only · *computed*

The name of the legacy (provider) data source that the table's first partition queries. If the partitions use different data sources, you see only the one of the first partition.

The **Properties** view shows `Source` only when the first partition is a query partition or an M partition. For an M partition the value is empty, because the connection is part of the M expression. `Source` isn't shown for calculated tables, calculation group tables, Direct Lake tables or tables with policy range partitions.

To list the tables that use an explicit (legacy) data source, run the @script-show-data-source-dependencies script.

### Source Type
`SourceType` · PartitionSourceType · Metadata · read-only · *shortcut to* **Source Type** of the first partition

The kind of source the table's first partition uses. For a table with partitions of different kinds, you see the kind of the first one. A table without partitions shows `None`.

The **Properties** view hides `SourceType` on calculated tables and calculation group tables. In a C# script, those return `Calculated` and `CalculationGroup`.

| Value | Meaning |
|---|---|
| `Query` | The partitions run a query, for example SQL, against a legacy (provider) data source. |
| `Calculated` | The table is a calculated table and gets its data from a DAX expression. |
| `None` | No source is defined. The data is pushed into the table, for example in a push semantic model in Power BI. |
| `M` | The partitions use a Power Query (M) expression. Most common in Power BI models. Compatibility level 1400+. |
| `Entity` | The partitions read a named entity, such as a table in a lakehouse or warehouse. Used by Direct Lake tables. Compatibility level 1400+. |
| `PolicyRange` | An incremental refresh policy created the partitions. Compatibility level 1450+. |
| `CalculationGroup` | The table is a calculation group table. Compatibility level 1470+. |
| `Inferred` | The engine generates the query that fills the partition. Compatibility level 1563+. |

<!-- TODO (not verifiable from TE3 source): which kind of partition uses Inferred. TOM only says "The data in this partition is populated by executing a query generated by the system." -->

### Alternate Source Precedence
`AlternateSourcePrecedence` · int · Options · compatibility level 1460+

The order in which the engine considers this table when it looks for an aggregation table that can answer a query. It applies only to aggregation tables, that is, tables with columns whose `AlternateOf` points to a column in a detail table. When more than one aggregation table can answer a query, the engine uses the one with the highest value. The default is `0`.

In Power BI Desktop, this is the **Precedence** setting in **Manage aggregations**. To set up an aggregation table in Tabular Editor, see @user-defined-aggregations. The @script-implement-user-defined-aggregations script automates those steps for a fact table you select.

### Calendars
`Calendars` · collection of Calendar · Options · compatibility level 1701+

The custom calendars defined on the table. A calendar maps the columns of a date table that hold the year, quarter, month, week and date, and calendar-based time intelligence functions use it to work with fiscal, retail or other non-standard calendars. Custom calendars need compatibility level 1701 or higher. See @object-properties-calendars.

In Tabular Editor 3, right-click a table and choose **Create > Calendar...** to add a calendar, then map its columns in the **Calendar Editor**. See @calendars.

### Data Category
`DataCategory` · string · Options

The kind of data the table holds, for client tools. In Power BI, the value `Time` marks the table as a date table: Power BI uses the table's date column (the column with `IsKey` set to `true`) for time intelligence and turns off the auto date/time table for it. **Mark as date table** in Power BI Desktop sets this value.

Leave it empty or set it to `Regular` for all other tables. The other values come from multidimensional models, and only some Excel features and older client tools use them: `Geography`, `Organization`, `BillOfMaterials`, `Accounts`, `Customers`, `Products`, `Scenario`, `Quantitative`, `Utility`, `Currency`, `Rates`, `Channel` and `Promotion`. The dropdown in the **Properties** view lists these values and `Unknown`, and you can also type a value.

<!-- TODO (not verifiable from TE3 source): whether an empty value and "Regular" behave the same in the engine and client tools, and which client tools use the values other than Time. -->

In Tabular Editor, you can also right-click the table in the @tom-explorer-view and choose **Mark as date table...**. The Best Practice Analyzer (BPA) rule @kb.bpa-date-table-exists flags models that have no date table. The @script-create-date-table script creates a date table from the date columns in your model and sets `DataCategory` to `Time`.

### Default Detail Rows Expression
`DefaultDetailRowsExpression` · string · Options · compatibility level 1400+

A DAX table expression that returns the rows a user sees when they drill through on a measure in this table, for example with **Show Details** in an Excel PivotTable. It applies to every measure in the table that has no `DetailRowsExpression` of its own (see @object-properties-measures). Power BI doesn't use this property.

This expression shows the order number, customer and amount for each sales row:

```dax
SELECTCOLUMNS (
    Sales,
    "Order", Sales[OrderNumber],
    "Customer", RELATED ( Customer[Name] ),
    "Amount", Sales[Amount]
)
```

See @detail-rows-expression. In Tabular Editor 3, you write the expression in the **Expression Editor** of the @dax-editor, with auto-complete and parameter info. To remove the expression, clear the value.

### Direct Lake Indexing Behavior
`DirectLakeIndexingBehavior` · DirectLakeIndexingBehavior · Options · Preview compatibility level

When the engine builds and saves the indexes it uses for a Direct Lake table. Building indexes during a refresh makes the first queries after the refresh faster, and building them on demand makes refreshes faster. It applies only to tables in Direct Lake mode.

The Tabular Object Model (TOM) doesn't assign this property a released compatibility level yet, so the **Properties** view in the current version of Tabular Editor 3 hides it for every model.

| Value | Meaning |
|---|---|
| `Default` | Uses the model's default, set with **Default Direct Lake Indexing Behavior** on @object-properties-model. |
| `Auto` | Build in-memory indexes during data load or query execution when needed, as the TOM library describes it. |
| `Full` | The engine builds and saves the indexes as part of a full refresh, a calculate refresh and a refresh of type indexes. |
| `Explicit` | The engine builds and saves the indexes only when you run a refresh of type indexes. |

<!-- TODO (not verifiable from TE3 source): the behavior of each value and which indexes this covers; check the Microsoft documentation once the feature is out of preview. -->

### Exclude From Automatic Aggregations
`ExcludeFromAutomaticAggregations` · bool · Options · compatibility level 1572+

When `true`, Power BI leaves the table out when it builds automatic aggregations. Automatic aggregations are a Power BI Premium and Fabric feature for DirectQuery models, where the service creates aggregation tables based on the queries it receives. Set it on a table whose data changes too often for a cached aggregation to be useful.

<!-- TODO (not verifiable from TE3 source): the exact effect. TOM only says "An indication whether the table is excluded from the automatic aggregations feature." Is the table excluded as a source for aggregations, or are queries against it never answered from aggregations? -->

### Exclude From Model Refresh
`ExcludeFromModelRefresh` · bool · Options · compatibility level 1480+

When `true`, a refresh of the whole model skips this table's partitions if they already hold data. Partitions without data are still refreshed, so a new or cleared table gets loaded. You can still refresh the table by selecting it explicitly. Use it for tables that rarely change or are expensive to load, such as a large historical table or a table that a separate process fills.

On SQL Server 2025 Analysis Services, the model-level refresh types **Full**, **Automatic**, **Data only** and **Calculate** all skip the table when its partitions hold data. **Clear values** does clear the table's data, and the next model refresh then loads the table again.

In Tabular Editor 3, you refresh a single table by right-clicking it in the **TOM Explorer** and choosing **Refresh table**. See @refresh-preview-query.

### Partitions
`Partitions` · collection of Partition · Options · read-only

The partitions of the table. Each partition defines where a part of the table's data comes from, for example an M expression, and you can refresh each one separately. Most tables have a single partition. Large import tables often have one partition per period, created by you or by an incremental refresh policy.

Click the ellipsis button to open the collection editor, where you add, remove and edit partitions. See @object-properties-partitions.

The **Properties** view shows `Partitions` only when the table's first partition is an M partition or a query partition. It's hidden for calculated tables (including field parameters), calculation group tables, Direct Lake tables and tables with policy range partitions. To view and edit the partitions of calculated tables and calculation group tables, run the @script-edit-hidden-partitions script.

### Private
`IsPrivate` · bool · Options

When `true`, client tools don't show the table, even to developers who turn on hidden objects. Power BI Desktop sets it on the date table template of the auto date/time feature (the table named `DateTableTemplate_` followed by a GUID). It's always available in Power BI models and needs compatibility level 1400 or higher in Analysis Services models.

In Power BI Desktop, a private table doesn't appear in the **Data** pane at all, while a hidden table can still be shown there. SQL Server 2025 Analysis Services stores the flag and doesn't act on it. In both, the table is still listed in the schema information the engine returns, you can query it with DAX and measures in other tables can use it.

> [!NOTE]
> `IsPrivate` and `IsHidden` aren't security features. To secure a table, use object-level security (see [Object Level Security](#object-level-security)).

The BPA rule @kb.bpa-remove-auto-date-table flags the `DateTableTemplate_` and `LocalDateTable_` tables that auto date/time creates, so you can replace them with a single date table.

### Sets
`Sets` · collection of Set · Options · read-only · compatibility level 1400+

The calculated sets defined on the table. A set is a named DAX expression that returns a set of members, which client tools can show as a predefined selection. Sets are supported in Power BI models only: the **Properties** view shows `Sets` when the model's compatibility mode is Power BI and the compatibility level is 1400 or higher. Sets don't appear as objects in the **TOM Explorer**, so you add and edit them in the collection editor of this property. See @object-properties-functions.

<!-- TODO (not verifiable from TE3 source): what calculated sets are used for, and which client tools support them. -->

### Show As Variations Only
`ShowAsVariationsOnly` · bool · Options

When `true`, client tools show the table in the field list only through a column variation that points to it. Power BI Desktop sets it on the date tables that auto date/time creates (the tables named `LocalDateTable_` followed by a GUID), which appear as the date hierarchy under a date column. See `Variations` on @object-properties-columns.

It's always available in Power BI models and needs compatibility level 1400 or higher in Analysis Services models. SQL Server 2025 Analysis Services stores the flag and doesn't act on it: the table is still listed in the schema information that client tools read, you can query it with DAX and measures in other tables can use it.

### System Managed
`SystemManaged` · bool · Options · compatibility level 1562+

When `true`, the engine or the service creates and deletes the table. Don't set this property on your own tables, and don't edit a system-managed table: Tabular Editor doesn't block those edits.

The auto date/time tables that Power BI Desktop creates aren't system-managed. Desktop sets `IsHidden` and `IsPrivate` on the template table, and `IsHidden` and `ShowAsVariationsOnly` on each local date table.

<!-- TODO (not verifiable from TE3 source): which features create system-managed tables, for example automatic aggregations. -->

### Object Level Security
`ObjectLevelSecurity` · per role · Translations, Perspectives, Security · compatibility level 1400+ · *shortcut to* the table permissions of each role

The object-level security (OLS) permission of the table in each role of the model. Expand the property to see one entry per role. The **Properties** view shows the property only when the model has at least one role. Tabular Editor stores the permission in the table permission of each role.

| Value | Meaning |
|---|---|
| `Default` | No permission is set for this role. Members of the role can see the table. |
| `Read` | Members of the role can see and query the table. |
| `None` | The table and everything that depends on it are hidden from members of the role. Queries and measures that refer to the table return an error for them. |

With `None`, the table and its metadata don't exist for members of the role, so every measure that refers to the table fails for them. See @data-security-setup-ols and @object-properties-security. To check that OLS and row-level security work as intended, test them with impersonation in Tabular Editor 3. See @data-security-testing.

### Row Level Security
`RowLevelSecurity` · per role · Translations, Perspectives, Security · read-only · *shortcut to* the table permissions of each role

The row-level security (RLS) filter of the table in each role of the model. Expand the property to see one entry per role. Each entry is a DAX expression that returns `TRUE` for the rows that members of the role can see, for example:

```dax
Customer[Country] = "Denmark"
```

The property itself is read-only, and you edit each role's entry, which accepts multi-line expressions. The **Properties** view shows the property only when the model has at least one role. Tabular Editor stores the filter in the table permission of each role.

An empty entry doesn't filter the table for that role. Filters flow along relationships, so a filter on a dimension table also filters the fact tables related to it. See @roles-and-rls, @data-security-setup-rls and @object-properties-security.

## Calculated table

A calculated table gets its data from a DAX expression, for example a date table built with [CALENDAR](https://dax.guide/calendar) or a table that summarizes another table. The engine evaluates the expression when you refresh the table or the model and stores the result like any other imported table.

A calculated table has all the properties of a [table](#table), plus `Expression`. It has exactly one partition, which Tabular Editor manages, and it can't have an incremental refresh policy. The **Properties** view hides `Partitions`, `Source`, `SourceType`, `EnableRefreshPolicy` and `RefreshPolicy` on calculated tables and shows `AlternateSourcePrecedence`.

Field parameters in Power BI are calculated tables. The @create-field-parameter script creates one from the columns or measures you select.

### Common properties

The same as on [tables](#table).

### Expression
`Expression` · string · Options · *shortcut to* the expression of the table's calculated partition

The DAX expression that returns the table's rows. It must return a table, for example:

```dax
ADDCOLUMNS (
    CALENDAR ( DATE ( 2020, 1, 1 ), DATE ( 2030, 12, 31 ) ),
    "Year", YEAR ( [Date] ),
    "Month", FORMAT ( [Date], "mmm" )
)
```

Each column the expression returns becomes a calculated table column (see @object-properties-columns). Adding, removing or renaming columns this way affects other DAX expressions that refer to the table and hierarchies that use its columns.

In Tabular Editor 3, the columns change as soon as you change the expression. Tabular Editor 3 works them out with its own DAX semantic analysis, which also works when you edit a model file without a connection to Analysis Services or Power BI (see @creating-and-testing-dax). Tabular Editor 2 updates the columns only when you save the model to a database you're connected to, by reloading the table's columns from the server after the save. When you edit a model file in Tabular Editor 2, the columns don't change with the expression.

Edit the expression in the **Expression Editor**. In Tabular Editor 3, the **Expression Editor** of the @dax-editor has auto-complete and parameter info. The engine recalculates the table's data when the table is refreshed and when a table it depends on is refreshed. After you change the expression, refresh the table before you use it in a report. See [Refreshing data](xref:refresh-preview-query#refreshing-data).

## Calculation group table

A calculation group table holds a calculation group. It has one column with the names of the calculation items, and usually an ordinal column that sets the order of the items. Report authors use the column like any other column, for example in a slicer, and the selected calculation item changes how the measures in the report are calculated. See @object-properties-calculation-groups for the properties of the calculation group and its items.

Microsoft documents calculation groups for compatibility level 1500 or higher, which includes all Power BI semantic models. Tabular Editor 3 shows **Create > Calculation Group** from compatibility level 1470, the level at which TOM added calculation groups.

A calculation group table has the properties below in addition to the common properties. Most of them are shortcuts to properties of the calculation group in the table, which you can't select in the **TOM Explorer**. Of the other table properties, the **Properties** view shows only `TableGroup` and `DefaultDetailRowsExpression`. Calculation groups don't support detail rows expressions, row-level security or object-level security, so leave `DefaultDetailRowsExpression` empty.

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

### Table Group
`TableGroup` · string · Basic · *stored as an annotation* (`TabularEditor_TableGroup`)

The same as [Table Group](#table-group) on a table.

### Calculation Group Description
`CalculationGroupDescription` · string · Basic · *shortcut to* **Description** of the calculation group

The description stored on the calculation group, separate from the table's own `Description`. Client tools don't show it. When you hover over a calculation group table in the **Data** pane of Power BI Desktop, the table's `Description` appears, and Excel's field list shows no descriptions. Put the text for report authors in the table's `Description` and use this property for notes to other developers.

### Calculation Group Precedence
`CalculationGroupPrecedence` · int · Basic · *shortcut to* **Precedence** of the calculation group

The order in which the calculation group is applied when a query uses more than one calculation group. See `Precedence` on @object-properties-calculation-groups.

### Calculation Group Annotations
`CalculationGroupAnnotations` · collection of name/value pairs · Metadata · read-only · *shortcut to* **Annotations** of the calculation group

The annotations stored on the calculation group. The table has its own annotations (see [Annotations](xref:object-properties-common#annotations)). The property itself is read-only. Click the ellipsis button to open the annotation editor, where you add, change and remove the annotations. This works with one calculation group table selected at a time.

### Multiple or Empty Selection Expression
`MultipleOrEmptySelectionExpression` · string · Options · compatibility level 1605+ · *shortcut to* the calculation group

A DAX expression that the engine evaluates in place of the measure when the filter on the calculation group selects more than one calculation item, or selects none because the filter matches no item. Use [SELECTEDMEASURE](https://dax.guide/selectedmeasure) to refer to the measure. Below compatibility level 1605, the **Properties** view hides this property and the other selection expression properties below. To remove the expression, clear the value.

When the expression is empty, the calculation group isn't applied in those cases, and [Selection Expression Behavior](xref:object-properties-model#selection-expression-behavior) on the model sets what measures return:

- `Automatic` or `NonVisual`: the measure's normal value
- `Visual`: a blank value

A normal value can mislead users, for example when a user selects two currencies in a currency conversion calculation group and sees a total that's in neither currency. This expression returns an error message:

```dax
ERROR ( "Select a single currency." )
```

This expression returns a blank value:

```dax
BLANK ()
```

In Tabular Editor 3, you write the expression in the **Expression Editor** of the @dax-editor, with auto-complete and parameter info.

### Multiple or Empty Selection Expression Description
`MultipleOrEmptySelectionDescription` · string · Options · compatibility level 1605+ · *shortcut to* the calculation group

A description of the multiple or empty selection expression, for other developers. Client tools don't show it to report authors.

### Multiple or Empty Selection Format String Expression
`MultipleOrEmptySelectionFormatStringExpression` · string · Options · compatibility level 1605+ · *shortcut to* the calculation group

A DAX expression that returns the format string to use when the multiple or empty selection expression applies. It works like `FormatStringExpression` on a calculation item. Inside the expression, [SELECTEDMEASUREFORMATSTRING](https://dax.guide/selectedmeasureformatstring) returns the format string of the measure.

### No-selection Expression
`NoSelectionExpression` · string · Options · compatibility level 1605+ · *shortcut to* the calculation group

A DAX expression that the engine evaluates in place of the measure when there's no filter on the calculation group, that is, when the user hasn't selected a calculation item. When it's empty, measures return their normal value when nothing is selected. Use it to set a default calculation that users can override by selecting a calculation item. No-selection expressions need compatibility level 1605 or higher.

In this currency conversion example, sales amounts are stored in US dollars and a `Currency Rate` table holds the daily exchange rates. The expression converts amounts to the currency selected in a `Currency` table, without the user picking a calculation item:

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

### No-selection Expression Description
`NoSelectionExpressionDescription` · string · Options · compatibility level 1605+ · *shortcut to* the calculation group

A description of the no-selection expression, for other developers. Client tools don't show it to report authors.

### No-selection Format String Expression
`NoSelectionFormatStringExpression` · string · Options · compatibility level 1605+ · *shortcut to* the calculation group

A DAX expression that returns the format string to use when the no-selection expression applies. It works like `FormatStringExpression` on a calculation item. Inside the expression, [SELECTEDMEASUREFORMATSTRING](https://dax.guide/selectedmeasureformatstring) returns the format string of the measure.
