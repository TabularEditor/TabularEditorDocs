---
uid: object-properties-partitions
title: Partition properties
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
# Partition properties

<!--
SUMMARY: Reference for the properties of partitions (legacy, calculated, M, entity and policy range partitions), incremental refresh policies and data coverage definitions.
-->

This page covers the properties of partitions, of the incremental refresh policy that can generate them, and of the data coverage definition that can describe a DirectQuery partition. For properties that most objects share, see @object-properties-common.

A partition defines where one part of a table's data comes from. Every table that isn't a calculation group has at least one partition, and most tables have exactly one. There are several kinds of partitions, which differ in how they describe their source:

| Kind | Source Type | Where the data comes from |
|---|---|---|
| Legacy (query) partition | `Query` | A native query, usually SQL, run against a legacy (provider) data source. |
| Calculated partition | `Calculated` | The DAX expression of a calculated table. |
| M partition | `M` | A Power Query (M) expression. This is the kind Power BI and most modern models use. |
| Entity partition | `Entity` | A named entity, such as a Delta table in a lakehouse or warehouse. Direct Lake tables use this kind. |
| Policy range partition | `PolicyRange` | A date range of the table's incremental refresh policy. The engine creates these partitions for you. |

All kinds share the properties under [Properties of all partitions](#properties-of-all-partitions). The sections after that list only the properties that are specific to one kind.

## Properties of all partitions

The properties in this section apply to every kind of partition. Tabular Editor only shows the ones that make sense for the kind you select. For example, **Query** only appears on legacy partitions and **Query Group** only on M partitions.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Error Message](xref:object-properties-common#error-message)
- [Object Type](xref:object-properties-common#object-type)
- [State](xref:object-properties-common#state)

When a table has a single partition with the same name as the table, renaming the table also renames the partition.

### Basic

#### Data Source
`DataSource` · DataSource

The data source the partition's query runs against. Tabular Editor shows this property on legacy (query) partitions and on entity partitions. Pick one of the model's data sources from the dropdown. Policy range partitions also list the property, but it's always empty there.

M partitions don't use this property: the M expression names its source itself, either directly (for example `Sql.Database("myserver", "mydb")`) or through a structured data source or shared expression that it refers to. See @object-properties-data-sources.

#### Expression
`Expression` · string

The expression that fills the partition with data. In the Properties view, Tabular Editor only shows it on calculated partitions, where it holds the DAX expression of the calculated table. On other kinds, the same text appears under a more specific name: **Query** on legacy partitions and **M Expression** on M partitions.

In practice, you rarely see this property. The TOM Explorer doesn't show the partitions of calculated tables (field parameters included) or of calculation groups, so you can't select a calculated partition there. Edit the DAX expression through **Expression** on the calculated table instead, or use the @script-edit-hidden-partitions script to open the partition's properties.

In a C# script, `Expression` works on legacy, calculated and M partitions alike, which is useful when you loop over partitions of different kinds. Setting it on any other kind of partition, such as an entity partition, throws an error.

#### Query
`Query` · string

The native query that the engine sends to the legacy data source to fill the partition, for example:

```sql
SELECT * FROM dbo.FactSales WHERE OrderDate >= '2024-01-01'
```

Only shown on legacy (query) partitions. It's an alias for **Expression**: both names read and write the same value.

The engine sends the query as-is, so it must be valid in the source's own dialect. When you split a large table into several legacy partitions, make sure the `WHERE` clauses don't overlap and don't leave gaps, or rows are loaded twice or not at all.

In Tabular Editor 3, a refresh override profile can replace the query of a partition for a single refresh, for example to load only the top 10,000 rows while you develop, without changing the model. See @refresh-overrides.

### Metadata

#### Last Processed
`RefreshedTime` · DateTime · read-only

The date and time the partition was last refreshed. The engine sets it, and you can't edit it. Use it to check whether a refresh actually reached a partition, for example after a scheduled refresh or an incremental refresh that should only have touched the most recent partitions.

A model that you open from a file shows the value that was stored in the file, if any. The value is only reliable when you're connected to a server or working in @workspace-mode.

The **Ignore timestamps** serialization option (see @preferences), which is on by default, tells Tabular Editor to leave timestamp metadata out when it saves the model to a `.bim` file or a folder in the JSON format. **Last Processed** is one of those timestamps, together with the modified times of the model and its objects. TMDL never stores timestamps, so a model saved as TMDL has no **Last Processed** value, whatever the option is set to.

In Tabular Editor 3, you can refresh a single partition by right-clicking it in the TOM Explorer, choosing **Refresh partition** and then the type of refresh. The @data-refresh-view shows the progress of the refresh.

### Options

#### DataCoverageDefinition
`DataCoverageDefinition` · DataCoverageDefinition

The optional data coverage definition of the partition. It tells the engine which rows a DirectQuery partition holds, so the engine can skip querying the source when a query only asks for rows outside that range. It's mostly used in hybrid tables, where recent data comes from a DirectQuery partition and older data is imported. See [Data coverage definition](#data-coverage-definition) below.

Tabular Editor shows this property at compatibility level 1603 and higher, on partitions in `DirectQuery` or `Dual` mode, and on any partition that already has a data coverage definition. Use the property's actions to add or remove the definition, or to edit its expression. On the same partitions, the Expression Editor also offers the data coverage definition expression. If you type an expression there on a partition that doesn't have a definition yet, Tabular Editor adds one for you.

#### Data View
`DataView` · DataViewType

For DirectQuery models in Analysis Services: whether this partition holds all data or a sample of it. Sample partitions were meant to let designers work with a small, imported subset of a DirectQuery table while building the model in Visual Studio. Queries from client tools use the full data.

| Value | Meaning |
|---|---|
| `Full` | The partition holds the complete data. |
| `Sample` | The partition holds a sample of the data, for use while designing the model. |
| `Default` | The partition uses **Default Data View** of the model. |

TOM defines only these three values. Microsoft's documentation on DirectQuery mode states that the **Set as Sample** feature of the Visual Studio model designer is currently not supported, so you rarely need `Sample`. Power BI doesn't use data views. In Power BI and Fabric models, leave this at its default.

#### Mode
`Mode` · ModeType

The storage mode of the partition: how the engine gets to the data in it.

| Value | Meaning |
|---|---|
| `Import` | Data is loaded into the model's memory at refresh time. Queries don't go to the source. |
| `DirectQuery` | Data stays in the source. Each query is translated into a query against the source, for example SQL. |
| `Dual` | The partition can act as either Import or DirectQuery, whichever gives the better query in a composite model. Typically used for dimension tables that relate to both imported and DirectQuery fact tables. Compatibility level 1455+. |
| `DirectLake` | Data is read directly from Delta tables in OneLake and loaded into memory on demand. Fabric only. Used with entity partitions. Compatibility level 1604+. Tabular Editor editions that don't support Direct Lake don't let you pick this value. See @direct-lake-guidance. |
| `Push` | Data is pushed into the partition through the Power BI REST API, as in a push semantic model. There is no source query. Only the Power BI service supports it. |
| `Default` | The partition uses **Default Mode** of the model. See @object-properties-model. |

The mode is set per partition, but in practice all partitions of a table have the same mode. The main exception is a hybrid table, where an incremental refresh policy imports the historical partitions and keeps the most recent one in DirectQuery mode (see **Mode** of the refresh policy, below).

Changing the mode isn't just a setting change. For example, a table that you switch from `Import` to `DirectQuery` loses its imported data, and some features, such as calculated columns that use certain DAX functions, don't work in DirectQuery. To convert a Direct Lake table to import or back, see @script-convert-dlol-to-import and @script-convert-import-to-dlol.

Tabular Editor doesn't check these combinations. The engine does when you save, and SQL Server Analysis Services is much stricter than Power BI. SQL Server 2025 Analysis Services:

- rejects `Dual` partitions, with the error *may not operate in Dual mode*,
- rejects models that mix imported data with DirectQuery, both within a table and across tables, so composite models and hybrid tables aren't possible,
- allows only one `DirectQuery` partition per table.

The one mix it accepts is the older DirectQuery pattern, where a table has one `DirectQuery` partition plus `Import` partitions with **Data View** `Sample`.

In the Power BI service, the rules are much looser. The service accepts an `Import` and a `DirectQuery` partition in the same table, even without a refresh policy, `Dual` tables, and relationships between imported and DirectQuery tables in either direction. The rule it keeps is one `DirectQuery` partition per table. A `DirectQuery` or `Dual` partition also needs an expression that refers to a data source: one built from literal data, such as `#table`, is rejected.

#### Query Group
`QueryGroup` · QueryGroup · compatibility level 1480+

The query group (folder) the partition's M query appears in, in the Power Query editor of Power BI Desktop. It only organizes queries in that editor. It doesn't affect refresh or the field list. Tabular Editor shows this property on M partitions only.

Pick one of the model's query groups from the dropdown, or leave it empty. See **Query group** on @object-properties-data-sources.

#### Source Type
`SourceType` · PartitionSourceType · read-only

The kind of partition. It's set when the partition is created and you can't change it. To change the kind, create a new partition of the right kind and delete the old one.

| Value | Meaning |
|---|---|
| `Query` | A legacy partition with a native query against a provider data source. |
| `Calculated` | The partition of a calculated table, filled by a DAX expression. |
| `None` | The partition has no source. The data is pushed into it, for example in a push semantic model. |
| `M` | An M partition with a Power Query (M) expression. |
| `Entity` | An entity partition that reads a named entity, such as a table in a lakehouse. Direct Lake uses this kind. |
| `PolicyRange` | A partition generated by an incremental refresh policy. |
| `CalculationGroup` | The partition of a calculation group table. It holds no source; the engine fills it from the calculation items. |
| `Inferred` | A partition for which the engine generates the query itself. Compatibility level 1563+. |

TOM also defines the value `Parquet`, but only for an internal compatibility level that Microsoft doesn't release, so you won't see it in your models.

<!-- TODO (not verifiable from TE3 source): which kind of table or model feature creates Inferred partitions. TOM only says "populated by executing a query generated by the system" (CL 1563+), and TE3 has no special handling for it. Same open question as on @object-properties-tables. -->

## Legacy and calculated partitions

Legacy (query) partitions and calculated partitions have no properties beyond the ones under [Properties of all partitions](#properties-of-all-partitions).

- A **legacy partition** (`Query`) uses **Data Source** and **Query**. It's the kind of partition that models use with provider data sources, typically in Analysis Services models below compatibility level 1400. See @import-tables. The Best Practice Analyzer rule @kb.bpa-avoid-provider-partitions-structured flags legacy partitions that use a structured data source, a combination that Power BI doesn't support.
- A **calculated partition** (`Calculated`) belongs to a calculated table and uses **Expression**. You normally edit the DAX expression on the calculated table itself, not on its partition. See **Expression** on @object-properties-tables. Tabular Editor doesn't show the partitions of calculated tables in the TOM Explorer. To look at one anyway, use the @script-edit-hidden-partitions script.

## M partition

An M partition fills the table with the result of a Power Query (M) expression. It's the default kind of partition in Power BI models and in Analysis Services models at compatibility level 1400 and higher. The M expression typically starts from a source function, such as `Sql.Database`, or from a shared expression, and ends with the table to load.

### Common properties

The same as on [all partitions](#properties-of-all-partitions).

### Options

#### Attributes
`Attributes` · string

Extra M attributes stored with the partition's source. Power BI Desktop can set this, and most models leave it empty. You normally don't need to change it.

Power BI Desktop leaves it empty, also on tables with an incremental refresh policy.

<!-- TODO (not verifiable from TE3 source): which tools or scenarios fill in Attributes on an M partition. -->

#### M Expression
`MExpression` · string

The Power Query (M) expression that returns the data for the partition. Edit it in the Expression Editor. For example:

```m
let
    Source = Sql.Database("myserver", "AdventureWorks"),
    Sales = Source{[Schema = "dbo", Item = "FactInternetSales"]}[Data]
in
    Sales
```

The expression must return a table whose columns match the source columns of the table's data columns (**Source Column** on @object-properties-columns). If a column is renamed or removed in the source, refresh fails until you update the table's columns, for example with **Update table schema** (see @import-tables).

To reuse parts of an expression across partitions, such as the server name, put them in a shared expression or an M parameter and refer to it by name. See @script-create-m-parameter. In Tabular Editor 3, @script-create-and-replace-parameter also replaces the value with the new parameter in all M partitions.

To make a long M expression easier to read in Tabular Editor 3, run the @script-format-power-query script on the selected partition. The script sends the expression to an external formatting service.

## Entity partition

An entity partition reads its data from a named object, an *entity*, instead of running a query. Direct Lake models use entity partitions: each Direct Lake table has one entity partition that points to a Delta table in a Fabric lakehouse or warehouse. The connection to the lakehouse or warehouse is held by a shared expression, which the partition refers to through **Expression Source**.

See @direct-lake-sql-model and @direct-lake-guidance. In Tabular Editor 3, the @import-tables wizard can create Direct Lake tables from a Fabric lakehouse or warehouse for you.

### Common properties

The same as on [all partitions](#properties-of-all-partitions).

### Options

#### Entity Name
`EntityName` · string

The name of the source object the partition reads, for example the name of the Delta table in the lakehouse, such as `FactSales`. Like a column's **Source Column**, it has to match the source exactly. Renaming the table in the model doesn't change the entity name, so you can give the table a friendlier name than the source.

If the source table is renamed, update **Entity Name** to match, or the partition fails the next time the model is framed or refreshed.

<!-- TODO (not verifiable from TE3 source): whether Entity Name is case-sensitive for Direct Lake. -->

If your changes to **Entity Name** revert after you refresh the model in Power BI, see @direct-lake-entity-updates-reverting.

#### Expression Source
`ExpressionSource` · NamedExpression

The shared expression that holds the connection to the source. In a Direct Lake model this is typically a shared expression named `DatabaseQuery`, which is the name the Tabular Editor 3 import wizard gives it when it creates the expression for you. Its M expression depends on the kind of Direct Lake:

- **Direct Lake on SQL**: `Sql.Database("<SQL endpoint>", "<lakehouse or warehouse name>")`
- **Direct Lake on OneLake**: `AzureStorage.DataLake("https://onelake.dfs.fabric.microsoft.com/<workspace ID>/<item ID>", [HierarchicalNavigation=true])`

Tabular Editor tells the two kinds apart by the M function in this shared expression. An entity partition without an expression source counts as Direct Lake on SQL. All Direct Lake tables of the model usually point to the same shared expression.

To point a Direct Lake model to a different lakehouse or warehouse, for example when you move it from development to production, change the M expression of that shared expression rather than each partition.

To switch a model from Direct Lake on SQL to Direct Lake on OneLake, run the @script-convert-dlsql-to-dlol script, which changes the M expression of this shared expression.

#### Schema Name
`SchemaName` · string

The schema of the source object, for lakehouses and warehouses that use schemas, for example `dbo` or `sales`. Leave it empty when the source has no schemas. Together with **Entity Name**, it identifies the source table.

Microsoft's documentation describes this property as reserved for future use. Tabular Editor only shows it, and lets you edit it, at compatibility level 1604 and higher.

<!-- TODO (not verifiable from TE3 source): whether Direct Lake now uses Schema Name for schema-enabled lakehouses, despite the "reserved for future use" description in TOM. -->

## Policy range partition

A policy range partition holds one date range of a table that uses incremental refresh. You don't create these partitions yourself: the engine creates, merges and removes them when it applies the table's refresh policy, for example during a refresh in the Power BI service, or when you choose **Apply Refresh Policy** in Tabular Editor. Each partition covers one period, such as a day, a month, a quarter or a year. Older periods are merged into bigger partitions as they age.

The M query of a policy range partition comes from **Source Expression** of the refresh policy, with the partition's **Start** and **End** used as the values of `RangeStart` and `RangeEnd`.

See @incremental-refresh-about, @incremental-refresh-setup and @incremental-refresh-modify.

In Tabular Editor 3, the @advanced-refresh dialog can apply the refresh policy as part of a refresh, with an effective date that you pick, so you can test how the policy behaves at another point in time. When you deploy from Tabular Editor 3, you can choose not to deploy the partitions that a refresh policy governs. See @deployment.

### Common properties

The same as on [all partitions](#properties-of-all-partitions).

### Refresh Policy

#### End
`End` · DateTime

The end of the date range the partition covers. The end itself isn't included: the partition holds rows where the date is before **End**. It's the value the engine passes as `RangeEnd` when it refreshes the partition.

The engine sets it when it applies the refresh policy. Tabular Editor lets you edit it, but changing it by hand is rarely a good idea, because the next time the policy is applied the engine may recreate the partitions.

#### Granularity
`Granularity` · RefreshGranularityType

The size of the period the partition covers.

| Value | Meaning |
|---|---|
| `Day` | One day. |
| `Month` | One calendar month. |
| `Quarter` | One calendar quarter. |
| `Year` | One calendar year. |
| `Invalid` | No granularity is set. |

Recent periods are usually small (days or months) and are merged into larger ones (quarters, then years) as they move out of the incremental refresh window.

#### RefreshBookmark
`RefreshBookmark` · string · read-only

The value that **Polling Expression** of the refresh policy returned for this partition the last time it was refreshed, for example the latest modified date in the partition's range. On the next refresh, the engine evaluates the polling expression again and only refreshes the partition if the value has changed. This is what **Detect data changes** in Power BI Desktop uses.

It's empty when the policy has no polling expression. Tabular Editor shows the value but doesn't let you change it.

You can't change it in Tabular Editor or through the TOM library, where the property is read-only, but a TMSL `alter` command can set `refreshBookmark` on a partition, for example to an empty string. On the next refresh with the refresh policy applied, the engine compares the polling result with the stored bookmark and only refreshes the partitions where they differ, so changing the bookmark forces a refresh of that partition. A refresh with `applyRefreshPolicy` set to `false` refreshes the partitions without looking at or updating the bookmarks.

#### Start
`Start` · DateTime

The start of the date range the partition covers. The start is included: the partition holds rows where the date is on or after **Start**. It's the value the engine passes as `RangeStart` when it refreshes the partition.

Like **End**, the engine sets it when it applies the refresh policy.

## Refresh policy

A refresh policy tells the engine how to partition and refresh a table incrementally: how much history to keep (the *rolling window*), how much of the most recent data to refresh each time (the *incremental window*), and the M query to use for each partition. The engine uses the policy to create and maintain the table's [policy range partitions](#policy-range-partition).

You find the refresh policy on its table, under **Incremental Refresh**. Set **Enabled** to `true` on the table, then expand **Refresh Policy** to edit the properties below. See **Refresh Policy** on @object-properties-tables.

For example, with **Rolling Window Periods** `5`, **Rolling Window Granularity** `Year`, **Incremental Periods** `10` and **Incremental Granularity** `Day`, the table keeps five years of history and each refresh only reloads the last ten days.

See @incremental-refresh-about, @incremental-refresh-policy, @incremental-refresh-setup, @incremental-refresh-modify and @incremental-refresh-schema. To set up a refresh policy for an import table from a date column you select, including the `RangeStart` and `RangeEnd` parameters, use the @script-implement-incremental-refresh script.

### Common properties

- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Object Type](xref:object-properties-common#object-type)

### Options

#### Incremental Granularity
`IncrementalGranularity` · RefreshGranularityType

The unit of **Incremental Periods**: `Day`, `Month`, `Quarter` or `Year`. `Invalid` means the policy isn't configured yet. It also decides the size of the partitions in the incremental window. For example, `Day` creates one partition per day for the refreshed range.

#### Incremental Periods
`IncrementalPeriods` · int

How many periods, counted back from today, the engine refreshes on each refresh. With **Incremental Granularity** `Day` and `10`, each refresh reloads the last ten days and leaves older partitions alone.

Choose the smallest window that still catches late-arriving or changed rows in the source. A larger window makes refreshes slower; a window that's too small misses changes to older rows.

#### Incremental Periods Offset
`IncrementalPeriodsOffset` · int

Shifts the incremental window relative to today, in units of **Incremental Granularity**. `0` means the window ends with the current period. A negative value moves it into the past, for example `-1` with `Day` refreshes up to and including yesterday, so the table only holds complete days. A positive value moves it into the future, for sources that contain future-dated rows such as forecasts.

The **Only refresh complete days** option in Power BI Desktop's incremental refresh dialog sets **Incremental Periods Offset** to `-1`.

#### Mode
`Mode` · RefreshPolicyMode · compatibility level 1565+

Whether the most recent period is also imported, or kept in DirectQuery so it shows real-time data.

| Value | Meaning |
|---|---|
| `Import` | All partitions, including the most recent one, are imported. Data is only as fresh as the last refresh. |
| `Hybrid` | The historical partitions are imported, and the engine adds a DirectQuery partition for the rows after the incremental window. Queries always see the latest rows in the source. This makes the table a hybrid table. Power BI Premium, Premium Per User and Power BI Embedded only. |

A hybrid table sends queries to the source for the current period, so the source needs to handle that query load. Consider a data coverage definition on the DirectQuery partition (see [Data coverage definition](#data-coverage-definition)) to avoid unnecessary source queries.

Microsoft recommends Dual storage mode for the tables related to a hybrid table, to avoid performance penalties.

#### Policy Type
`PolicyType` · RefreshPolicyType

The kind of refresh policy. The only value is `Basic`, which is the policy described on this page. Tabular Editor doesn't let you change it.

#### Polling Expression
`PollingExpression` · string

An optional M expression that the engine evaluates for each partition in the incremental window before it refreshes it. It usually returns the latest modified date or a row count for the partition's range. The engine stores the result in the partition's **RefreshBookmark** and only refreshes the partition when the value has changed since the last refresh. Leave it empty to refresh every partition in the incremental window every time.

The expression can use `RangeStart` and `RangeEnd`, just like **Source Expression**. For example:

```m
let
    Source = Sql.Database("myserver", "AdventureWorks"),
    Sales = Source{[Schema = "dbo", Item = "FactInternetSales"]}[Data],
    InRange = Table.SelectRows(Sales, each [OrderDate] >= RangeStart and [OrderDate] < RangeEnd),
    LastModified = List.Max(InRange[ModifiedDate])
in
    LastModified
```

Power BI Desktop fills this property when you select **Detect data changes** in the incremental refresh dialog. In Tabular Editor, you edit the polling expression in the Expression Editor: select the table and pick **Polling Expression** from the dropdown. See [Configure 'Detect Data Changes'](xref:incremental-refresh-modify#configure-detect-data-changes).

#### Rolling Window Granularity
`RollingWindowGranularity` · RefreshGranularityType

The unit of **Rolling Window Periods**: `Day`, `Month`, `Quarter` or `Year`. `Invalid` means the policy isn't configured yet.

#### Rolling Window Periods
`RollingWindowPeriods` · int

How many complete periods of history, counted back from today, the table keeps. The current, incomplete period comes on top of that. With **Rolling Window Granularity** `Year` and `5`, the table holds the last five whole years in year partitions, plus the current year so far in quarter, month or day partitions. When a period falls out of the window, the engine removes its partition and the data in it at the next refresh.

The rolling window must be larger than the incremental window, since the incremental window is the recent part of it.

#### Source Expression
`SourceExpression` · string

The M expression the engine uses as the query for every policy range partition it creates. It must filter the source on a date column using the two M parameters `RangeStart` and `RangeEnd`, which the engine sets to each partition's **Start** and **End**. For example:

```m
let
    Source = Sql.Database("myserver", "AdventureWorks"),
    Sales = Source{[Schema = "dbo", Item = "FactInternetSales"]}[Data],
    InRange = Table.SelectRows(Sales, each [OrderDate] >= RangeStart and [OrderDate] < RangeEnd)
in
    InRange
```

Use `>=` on one parameter and `<` on the other, never `>=` and `<=`. Otherwise a row that falls exactly on a boundary is loaded into two partitions.

`RangeStart` and `RangeEnd` must exist in the model as M parameters (shared expressions) of type `DateTime`. If the date column in the source is an integer key such as `20240131`, convert the parameters to that format inside the filter step. For the filter to be efficient, it must fold to the source, so that the source only returns the rows of the partition.

Policy range partitions don't store a query of their own: whenever the engine refreshes one, it uses the current **Source Expression**. So a change takes effect on the next refresh, but only for the partitions that refresh reprocesses. A refresh with the refresh policy applied, which is what the Power BI service does, only reprocesses the incremental partitions, so the historical partitions keep the data they loaded with the old expression. To reload all of them with the new expression, run a full refresh of the table with `applyRefreshPolicy` set to `false`.


## Data coverage definition

A data coverage definition describes which rows a partition holds, as a DAX expression. The engine uses it to skip a DirectQuery partition when a query only asks for rows that the partition can't contain. This matters most in hybrid tables: without it, every query on the table also queries the source through the DirectQuery partition, even when the query only asks for last year's data that's already imported.

The definition belongs to a single partition. Add it through **DataCoverageDefinition** on the partition. See [DataCoverageDefinition](#datacoveragedefinition) above.

### Common properties

- [Description](xref:object-properties-common#description)
- [Annotations](xref:object-properties-common#annotations)
- [Error Message](xref:object-properties-common#error-message)
- [Object Type](xref:object-properties-common#object-type)
- [State](xref:object-properties-common#state)

### Options

#### Expression
`Expression` · string

A DAX expression that returns `TRUE` for the rows the partition covers. For example, for a DirectQuery partition that only holds the current year:

```dax
RELATED ( 'Date'[Year] ) = 2026
```

The expression is a hint: the engine trusts it and doesn't check it against the data. If the expression says a row isn't in the partition but it is, queries silently leave that row out. Keep the expression in line with the partition's actual query, and update it when the query changes.

To edit it, select the partition in the TOM Explorer and pick the data coverage definition expression in the Expression Editor's dropdown.

The engine doesn't validate the expression when you save. SQL Server 2025 Analysis Services accepted everything tried: column filters, `IN` lists, `RELATED`, and even text that isn't DAX at all. It also accepts a definition on an `Import` partition, where it has no purpose. So check the expression yourself before you deploy.

<!-- TODO (not verifiable from TE3 source): which DAX constructs are honored at query time in Power BI hybrid tables, and that a wrong definition silently leaves rows out of query results (needs a real hybrid table, which SSAS doesn't support). -->

#### Partition
`Partition` · Partition · read-only

The partition this data coverage definition belongs to. Tabular Editor doesn't show it in the Properties view. It's useful in C# scripts to get from the definition back to its partition.
