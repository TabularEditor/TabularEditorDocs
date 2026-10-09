---
uid: object-properties-partitions
title: Partition properties
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
# Partition properties

<!--
SUMMARY: Reference for the properties of partitions (legacy, calculated, M, entity and policy range partitions), incremental refresh policies and data coverage definitions.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

This page covers the properties of partitions, incremental refresh policies and data coverage definitions. For properties that most objects share, see @object-properties-common.

A partition defines where one part of a table's data comes from. Every table except a calculation group has at least one partition, and most tables have exactly one. Each kind of partition describes its source differently:

| Kind | Source Type | Where the data comes from |
|---|---|---|
| Legacy (query) partition | `Query` | A native query, usually SQL, against a legacy (provider) data source. |
| Calculated partition | `Calculated` | The DAX expression of a calculated table. |
| M partition | `M` | A Power Query (M) expression. Power BI and most modern models use this kind. |
| Entity partition | `Entity` | A named entity, such as a Delta table in a lakehouse or warehouse. Direct Lake tables use this kind. |
| Policy range partition | `PolicyRange` | A date range of the table's incremental refresh policy. The engine creates these partitions. |

All kinds share the properties under [Properties of all partitions](#properties-of-all-partitions). The later sections list the properties specific to one kind.

## Properties of all partitions

These properties apply to every kind of partition. The **Properties** view only shows the ones that apply to the selected kind, for example `Query` only on legacy partitions and `QueryGroup` only on M partitions. When a table has a single partition with the same name as the table, renaming the table also renames the partition.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Error Message](xref:object-properties-common#error-message)
- [Object Type](xref:object-properties-common#object-type)
- [State](xref:object-properties-common#state)

### Data Source
`DataSource` · DataSource · Basic

The data source that the partition's query runs against. Tabular Editor shows this property on legacy (query) partitions and on entity partitions, where you pick one of the model's data sources from the dropdown. Policy range partitions also list the property, but it's always empty there.

M partitions don't use this property. Their M expression names the source directly, for example `Sql.Database("myserver", "mydb")`, or refers to a structured data source or shared expression. See @object-properties-data-sources.

### Expression
`Expression` · string · Basic

The expression that fills the partition with data. The **Properties** view only shows it on calculated partitions, where it holds the DAX expression of the calculated table. On legacy partitions the same text appears as `Query`, and on M partitions as `MExpression`.

The **TOM Explorer** doesn't show the partitions of calculated tables (field parameters included) or of calculation groups. Edit the DAX expression through `Expression` on the calculated table, or open the partition's properties with the @script-edit-hidden-partitions script.

In a C# script, `Expression` reads and writes the expression of legacy, calculated and M partitions alike. Setting it on any other kind of partition, such as an entity partition, throws an error.

### Query
`Query` · string · Basic

The native query that the engine sends to the legacy data source to fill the partition, for example:

```sql
SELECT * FROM dbo.FactSales WHERE OrderDate >= '2024-01-01'
```

`Query` only appears on legacy (query) partitions. It's an alias for `Expression`, and both names read and write the same value. The engine sends the query as-is, so write it in the source's own dialect. If you split a large table into several legacy partitions and their `WHERE` clauses overlap or leave gaps, rows load twice or not at all.

In Tabular Editor 3, a refresh override profile replaces the query of a partition for a single refresh, for example to load only the top 10,000 rows during development. See @refresh-overrides.

### Last Processed
`RefreshedTime` · DateTime · Metadata · read-only

The date and time the engine last refreshed the partition. Use it to confirm that a refresh reached a partition, for example after a scheduled refresh or an incremental refresh that only refreshes the most recent partitions.

A model that you open from a file shows the value stored in the file, if any. The value is only reliable when you're connected to a server or working in @workspace-mode.

When the **Ignore timestamps** serialization option is on (the default, see @preferences), Tabular Editor leaves timestamps out when it saves the model to a `.bim` file or a folder in the JSON format. These timestamps are `RefreshedTime` and the modified times of the model and its objects. Tabular Model Definition Language (TMDL) never stores timestamps, so a model saved as TMDL has no `RefreshedTime` value, whatever the option is set to.

In Tabular Editor 3, refresh a single partition by right-clicking it in the **TOM Explorer** and choosing **Refresh partition** and the type of refresh. The @data-refresh-view shows the progress of the refresh.

### DataCoverageDefinition
`DataCoverageDefinition` · DataCoverageDefinition · Options · compatibility level 1603+

The optional [data coverage definition](#data-coverage-definition) of the partition, which describes the rows a DirectQuery partition holds. When a query only asks for rows outside that range, the engine skips querying the source. Hybrid tables use it on the DirectQuery partition that holds the recent data, next to the imported partitions with older data.

Tabular Editor shows this property at compatibility level 1603 and higher, on partitions in `DirectQuery` or `Dual` mode and on any partition that already has a data coverage definition. Use the property's actions to add or remove the definition or to edit its expression. On the same partitions, the **Expression Editor** lists the data coverage definition expression, and typing an expression there on a partition without a definition adds one.

### Data View
`DataView` · DataViewType · Options

For DirectQuery models in Analysis Services: whether the partition holds all data or a sample of it. A sample partition holds a small, imported subset of a DirectQuery table for designing the model in Visual Studio. Queries from client tools use the full data.

| Value | Meaning |
|---|---|
| `Full` | The partition holds the complete data. |
| `Sample` | The partition holds a sample of the data, for use while designing the model. |
| `Default` | The partition uses `DefaultDataView` of the model. |

The Tabular Object Model (TOM) defines only these three values. According to Microsoft's documentation on DirectQuery mode, the **Set as Sample** feature of the Visual Studio model designer is currently not supported. Power BI doesn't use data views, so leave this property at its default in Power BI and Fabric models.

### Mode
`Mode` · ModeType · Options

The storage mode of the partition, which sets how the engine gets to the data in it.

| Value | Meaning |
|---|---|
| `Import` | Data is loaded into the model's memory at refresh time. Queries don't go to the source. |
| `DirectQuery` | Data stays in the source. Each query is translated into a query against the source, for example SQL. |
| `Dual` | The partition acts as Import or DirectQuery, whichever gives the better query in a composite model. Typically used for dimension tables that relate to both imported and DirectQuery fact tables. Compatibility level 1455+. |
| `DirectLake` | Data is read directly from Delta tables in OneLake and loaded into memory on demand. Fabric only. Used with entity partitions. Compatibility level 1604+. Not available in Tabular Editor editions without Direct Lake support. See @direct-lake-guidance. |
| `Push` | Data is pushed into the partition through the Power BI REST API, as in a push semantic model. There is no source query. Only the Power BI service supports it. |
| `Default` | The partition uses `DefaultMode` of the model. See @object-properties-model. |

The mode is set per partition, and all partitions of a table usually have the same mode. The main exception is a hybrid table, where an incremental refresh policy imports the historical partitions and keeps the most recent one in DirectQuery mode (see `Mode` under [Refresh policy](#refresh-policy)).

Switching a table from `Import` to `DirectQuery` removes its imported data, and some features, such as calculated columns that use certain DAX functions, don't work in DirectQuery. To convert a Direct Lake table to import or back, see @script-convert-dlol-to-import and @script-convert-import-to-dlol.

Tabular Editor accepts any combination of modes. When you save, the engine rejects the combinations it doesn't support, and SQL Server Analysis Services is much stricter than Power BI. SQL Server 2025 Analysis Services:

- rejects `Dual` partitions with the error `may not operate in Dual mode`
- rejects models that mix imported data with DirectQuery, both within a table and across tables, so composite models and hybrid tables aren't possible
- allows only one `DirectQuery` partition per table

The one mix it accepts is the older DirectQuery pattern of one `DirectQuery` partition plus `Import` partitions with `DataView` set to `Sample`.

The Power BI service accepts an `Import` and a `DirectQuery` partition in the same table, even without a refresh policy. `Dual` tables and relationships between imported and DirectQuery tables in either direction also work there. The service keeps the rule of one `DirectQuery` partition per table, and it rejects a `DirectQuery` or `Dual` partition whose expression doesn't refer to a data source, such as one built from literal data with `#table`.

### Query Group
`QueryGroup` · QueryGroup · Options · compatibility level 1480+

The query group (folder) that the partition's M query appears in, in the Power Query editor of Power BI Desktop. It only organizes queries in that editor and doesn't affect refresh or the field list. Tabular Editor shows this property on M partitions only, where you pick one of the model's query groups from the dropdown or leave it empty. For query groups, see @object-properties-data-sources.

### Source Type
`SourceType` · PartitionSourceType · Options · read-only

The kind of partition, set when the partition is created. To change the kind, create a new partition of the right kind and delete the old one.

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

TOM also defines the value `Parquet`, for an internal compatibility level that Microsoft doesn't release, so it doesn't appear in your models.

<!-- TODO (not verifiable from TE3 source): which kind of table or model feature creates Inferred partitions. TOM only says "populated by executing a query generated by the system" (CL 1563+), and TE3 has no special handling for it. Same open question as on @object-properties-tables. -->

## Legacy and calculated partitions

Legacy (query) partitions and calculated partitions have no properties beyond the ones under [Properties of all partitions](#properties-of-all-partitions).

- a **legacy partition** (`Query`) uses `DataSource` and `Query`. Models use it with provider data sources, typically in Analysis Services models below compatibility level 1400. See @import-tables. The Best Practice Analyzer (BPA) rule @kb.bpa-avoid-provider-partitions-structured flags legacy partitions that use a structured data source, a combination that Power BI doesn't support.
- a **calculated partition** (`Calculated`) belongs to a calculated table and uses `Expression`. Edit the DAX expression on the calculated table itself (see `Expression` on @object-properties-tables). The **TOM Explorer** doesn't show the partitions of calculated tables. To open one, use the @script-edit-hidden-partitions script.

## M partition

An M partition fills the table with the result of a Power Query (M) expression. It's the default kind of partition in Power BI models and in Analysis Services models at compatibility level 1400 and higher. The M expression typically starts from a source function, such as `Sql.Database`, or from a shared expression, and ends with the table to load.

### Common properties

The same as on [all partitions](#properties-of-all-partitions).

### Attributes
`Attributes` · string · Options

Extra M attributes stored with the partition's source. Most models leave it empty, and Power BI Desktop leaves it empty, also on tables with an incremental refresh policy.

<!-- TODO (not verifiable from TE3 source): which tools or scenarios fill in Attributes on an M partition. -->

### M Expression
`MExpression` · string · Options

The Power Query (M) expression that returns the data for the partition. Edit it in the **Expression Editor**. For example:

```m
let
    Source = Sql.Database("myserver", "AdventureWorks"),
    Sales = Source{[Schema = "dbo", Item = "FactInternetSales"]}[Data]
in
    Sales
```

The expression must return a table whose columns match the `SourceColumn` values of the table's data columns (see @object-properties-columns). If a column is renamed or removed in the source, refresh fails until you update the table's columns, for example with **Update table schema** (see @import-tables).

Parts that several partitions share, such as the server name, can go in a shared expression or an M parameter that the expressions refer to by name. See @script-create-m-parameter. In Tabular Editor 3, @script-create-and-replace-parameter also replaces the value with the new parameter in all M partitions.

In Tabular Editor 3, the @script-format-power-query script formats the M expression of the selected partition through an external formatting service.

## Entity partition

An entity partition reads its data from a named object, an *entity*. Each Direct Lake table has one entity partition that points to a Delta table in a Fabric lakehouse or warehouse. A shared expression holds the connection to the lakehouse or warehouse, and the partition refers to it through `ExpressionSource`.

See @direct-lake-sql-model and @direct-lake-guidance. In Tabular Editor 3, the @import-tables wizard creates Direct Lake tables from a Fabric lakehouse or warehouse.

### Common properties

The same as on [all partitions](#properties-of-all-partitions).

### Entity Name
`EntityName` · string · Options

The name of the source object the partition reads, for example the Delta table `FactSales` in the lakehouse. Like a column's `SourceColumn`, it has to match the source exactly. Renaming the table in the model doesn't change the entity name, so the table can have a friendlier name than the source. If the source table is renamed, update `EntityName` to match, or the partition fails the next time the model is framed or refreshed.

<!-- TODO (not verifiable from TE3 source): whether Entity Name is case-sensitive for Direct Lake. -->

If your changes to `EntityName` revert after you refresh the model in Power BI, see @direct-lake-entity-updates-reverting.

### Expression Source
`ExpressionSource` · NamedExpression · Options

The shared expression that holds the connection to the source. In a Direct Lake model this is typically a shared expression named `DatabaseQuery`, the name that the Tabular Editor 3 import wizard gives it. Its M expression depends on the kind of Direct Lake:

- **Direct Lake on SQL**: `Sql.Database("<SQL endpoint>", "<lakehouse or warehouse name>")`
- **Direct Lake on OneLake**: `AzureStorage.DataLake("https://onelake.dfs.fabric.microsoft.com/<workspace ID>/<item ID>", [HierarchicalNavigation=true])`

Tabular Editor tells the two kinds apart by the M function in this shared expression, and treats an entity partition without an expression source as Direct Lake on SQL. All Direct Lake tables of a model usually point to the same shared expression.

To point a Direct Lake model to a different lakehouse or warehouse, for example when you move it from development to production, change the M expression of that shared expression. The partitions keep pointing to it. The @script-convert-dlsql-to-dlol script switches a model from Direct Lake on SQL to Direct Lake on OneLake by changing the same M expression.

### Schema Name
`SchemaName` · string · Options · compatibility level 1604+

The schema of the source object, for lakehouses and warehouses that use schemas, for example `dbo` or `sales`. Leave it empty when the source has no schemas. Together with `EntityName`, it identifies the source table.

Microsoft's documentation describes this property as reserved for future use. Tabular Editor shows it at compatibility level 1604 and higher.

<!-- TODO (not verifiable from TE3 source): whether Direct Lake now uses Schema Name for schema-enabled lakehouses, despite the "reserved for future use" description in TOM. -->

## Policy range partition

A policy range partition holds one date range of a table that uses incremental refresh. The engine creates, merges and removes these partitions when it applies the table's refresh policy, for example during a refresh in the Power BI service or when you choose **Apply Refresh Policy** in Tabular Editor. Each partition covers one period, such as a day, a month, a quarter or a year, and older periods are merged into bigger partitions as they age. The M query of a policy range partition is `SourceExpression` of the refresh policy, with the partition's `Start` and `End` as the values of `RangeStart` and `RangeEnd`.

See @incremental-refresh-about, @incremental-refresh-setup and @incremental-refresh-modify. In Tabular Editor 3, the @advanced-refresh dialog applies the refresh policy as part of a refresh with an effective date that you pick, to test how the policy behaves at another point in time. When you deploy from Tabular Editor 3, you can leave out the partitions that a refresh policy governs. See @deployment.

### Common properties

The same as on [all partitions](#properties-of-all-partitions).

### End
`End` · DateTime · Refresh Policy

The end of the date range the partition covers. The partition holds the rows dated before `End`, and the engine passes the value as `RangeEnd` when it refreshes the partition. The engine sets it when it applies the refresh policy.

### Granularity
`Granularity` · RefreshGranularityType · Refresh Policy

The size of the period the partition covers.

| Value | Meaning |
|---|---|
| `Day` | One day. |
| `Month` | One calendar month. |
| `Quarter` | One calendar quarter. |
| `Year` | One calendar year. |
| `Invalid` | No granularity is set. |

Recent periods are usually small (days or months) and are merged into larger ones (quarters, then years) as they move out of the incremental refresh window.

### RefreshBookmark
`RefreshBookmark` · string · Refresh Policy · read-only

The value that `PollingExpression` of the refresh policy returned for this partition at its last refresh, for example the latest modified date in the partition's range. It's empty when the policy has no polling expression. On the next refresh, the engine evaluates the polling expression again and only refreshes the partition if the value has changed. **Detect data changes** in Power BI Desktop works this way.

The property is read-only in Tabular Editor and in the TOM library, but a Tabular Model Scripting Language (TMSL) `alter` command can set `refreshBookmark` on a partition, for example to an empty string. On the next refresh with the refresh policy applied, the engine compares the polling result with the stored bookmark and only refreshes the partitions where they differ, so changing the bookmark forces a refresh of that partition. A refresh with `applyRefreshPolicy` set to `false` refreshes the partitions without reading or updating the bookmarks.

### Start
`Start` · DateTime · Refresh Policy

The start of the date range the partition covers. The partition holds the rows dated on or after `Start`, and the engine passes the value as `RangeStart` when it refreshes the partition. Like `End`, the engine sets it when it applies the refresh policy.

## Refresh policy

A refresh policy defines how the engine partitions and refreshes a table incrementally: how much history to keep (the *rolling window*), how much of the most recent data to refresh each time (the *incremental window*) and the M query for each partition. The engine uses the policy to create and maintain the table's [policy range partitions](#policy-range-partition).

The refresh policy is on its table, under **Incremental Refresh** in the **Properties** view. Set **Enabled** (`EnableRefreshPolicy`) to `true` on the table, then expand **Refresh Policy** to edit the properties below. See `RefreshPolicy` on @object-properties-tables.

With `RollingWindowPeriods` set to `5`, `RollingWindowGranularity` to `Year`, `IncrementalPeriods` to `10` and `IncrementalGranularity` to `Day`, the table keeps five years of history and each refresh only reloads the last ten days.

See @incremental-refresh-about, @incremental-refresh-policy, @incremental-refresh-setup, @incremental-refresh-modify and @incremental-refresh-schema. The @script-implement-incremental-refresh script sets up a refresh policy for an import table from a date column you select, including the `RangeStart` and `RangeEnd` parameters.

### Common properties

- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Object Type](xref:object-properties-common#object-type)

### Incremental Granularity
`IncrementalGranularity` · RefreshGranularityType · Options

The unit of `IncrementalPeriods`: `Day`, `Month`, `Quarter` or `Year`. `Invalid` means the policy isn't configured yet. The unit is also the size of the partitions in the incremental window, for example one partition per day of the refreshed range for `Day`.

### Incremental Periods
`IncrementalPeriods` · int · Options

How many periods, counted back from today, the engine refreshes on each refresh. With `IncrementalGranularity` set to `Day` and `IncrementalPeriods` to `10`, each refresh reloads the last ten days and leaves older partitions alone. A larger window makes refreshes slower, and a window that's too small misses changes to older rows.

### Incremental Periods Offset
`IncrementalPeriodsOffset` · int · Options

Shifts the incremental window relative to today, in units of `IncrementalGranularity`:

- `0` ends the window with the current period
- a negative value moves it into the past, for example `-1` with `Day` refreshes up to and including yesterday, so the table only holds complete days
- a positive value moves it into the future, for sources that contain future-dated rows such as forecasts

The **Only refresh complete days** option in the incremental refresh dialog of Power BI Desktop sets `IncrementalPeriodsOffset` to `-1`.

### Mode
`Mode` · RefreshPolicyMode · Options · compatibility level 1565+

Whether the most recent period is imported too or kept in DirectQuery to show real-time data.

| Value | Meaning |
|---|---|
| `Import` | All partitions, including the most recent one, are imported. Data is only as fresh as the last refresh. |
| `Hybrid` | The historical partitions are imported, and the engine adds a DirectQuery partition for the rows after the incremental window. Queries always see the latest rows in the source, and the table becomes a hybrid table. Power BI Premium, Premium Per User and Power BI Embedded only. |

A hybrid table sends queries for the current period to the source. A [data coverage definition](#data-coverage-definition) on the DirectQuery partition avoids source queries for rows outside the current period. Microsoft recommends Dual storage mode for the tables related to a hybrid table.

### Policy Type
`PolicyType` · RefreshPolicyType · Options · read-only

The kind of refresh policy. The only value is `Basic`, the policy described on this page, and you can't change it in Tabular Editor.

### Polling Expression
`PollingExpression` · string · Options

An optional M expression that the engine evaluates for each partition in the incremental window before it refreshes the partition. It usually returns the latest modified date or a row count for the partition's range. The engine stores the result in the partition's `RefreshBookmark` and only refreshes the partition when the value has changed since the last refresh. When the property is empty, every partition in the incremental window refreshes every time.

The expression can use `RangeStart` and `RangeEnd`, like `SourceExpression`. This example returns the latest modified date in the partition's range:

```m
let
    Source = Sql.Database("myserver", "AdventureWorks"),
    Sales = Source{[Schema = "dbo", Item = "FactInternetSales"]}[Data],
    InRange = Table.SelectRows(Sales, each [OrderDate] >= RangeStart and [OrderDate] < RangeEnd),
    LastModified = List.Max(InRange[ModifiedDate])
in
    LastModified
```

Power BI Desktop fills this property when you select **Detect data changes** in the incremental refresh dialog. In Tabular Editor, edit the polling expression in the **Expression Editor** by selecting the table and picking **Polling Expression** from the dropdown. See [Configure 'Detect Data Changes'](xref:incremental-refresh-modify#configure-detect-data-changes).

### Rolling Window Granularity
`RollingWindowGranularity` · RefreshGranularityType · Options

The unit of `RollingWindowPeriods`: `Day`, `Month`, `Quarter` or `Year`. `Invalid` means the policy isn't configured yet.

### Rolling Window Periods
`RollingWindowPeriods` · int · Options

How many complete periods of history, counted back from today, the table keeps on top of the current, incomplete period. With `RollingWindowGranularity` set to `Year` and `RollingWindowPeriods` to `5`, the table holds the last five whole years in year partitions, plus the current year so far in quarter, month or day partitions. When a period falls out of the window, the engine removes its partition and the data in it at the next refresh.

The rolling window must be larger than the incremental window, which is its most recent part.

### Source Expression
`SourceExpression` · string · Options

The M expression that the engine uses as the query for every policy range partition it creates. It must filter the source on a date column with the M parameters `RangeStart` and `RangeEnd`, which the engine sets to each partition's `Start` and `End`. For example:

```m
let
    Source = Sql.Database("myserver", "AdventureWorks"),
    Sales = Source{[Schema = "dbo", Item = "FactInternetSales"]}[Data],
    InRange = Table.SelectRows(Sales, each [OrderDate] >= RangeStart and [OrderDate] < RangeEnd)
in
    InRange
```

Use `>=` on one parameter and `<` on the other. With `>=` and `<=`, a row that falls exactly on a boundary loads into two partitions.

`RangeStart` and `RangeEnd` must exist in the model as M parameters (shared expressions) of type `DateTime`. If the date column in the source is an integer key such as `20240131`, convert the parameters to that format inside the filter step. If the filter doesn't fold to the source, the source returns all rows for every partition.

Policy range partitions don't store a query of their own, and each refresh of one uses the current `SourceExpression`. A change takes effect on the next refresh, but only for the partitions that refresh reprocesses. A refresh with the refresh policy applied, which is what the Power BI service runs, only reprocesses the incremental partitions, and the historical partitions keep the data they loaded with the old expression. To reload all of them with the new expression, run a full refresh of the table with `applyRefreshPolicy` set to `false`.

## Data coverage definition

A data coverage definition describes, as a DAX expression, which rows a partition holds. The engine uses it to skip a DirectQuery partition when a query only asks for rows that the partition can't contain. In a hybrid table without one, every query on the table also queries the source through the DirectQuery partition, even when the query only asks for last year's data that's already imported.

The definition belongs to a single partition. Add it through [DataCoverageDefinition](#datacoveragedefinition) on the partition.

### Common properties

- [Description](xref:object-properties-common#description)
- [Annotations](xref:object-properties-common#annotations)
- [Error Message](xref:object-properties-common#error-message)
- [Object Type](xref:object-properties-common#object-type)
- [State](xref:object-properties-common#state)

### Expression
`Expression` · string · Options

A DAX expression that returns `TRUE` for the rows the partition covers. For example, for a DirectQuery partition that only holds the current year:

```dax
RELATED ( 'Date'[Year] ) = 2026
```

The engine trusts the expression and doesn't check it against the data. If the expression excludes a row that the partition holds, queries silently leave that row out, so update the expression when the partition's query changes.

To edit it, select the partition in the **TOM Explorer** and pick the data coverage definition expression in the dropdown of the **Expression Editor**.

The engine doesn't validate the expression when you save. SQL Server 2025 Analysis Services accepted every expression tried, including column filters, `IN` lists, `RELATED` and text that isn't DAX at all, and it also accepts a definition on an `Import` partition, where the definition has no purpose. Check the expression yourself before you deploy.

<!-- TODO (not verifiable from TE3 source): which DAX constructs are honored at query time in Power BI hybrid tables, and that a wrong definition silently leaves rows out of query results (needs a real hybrid table, which SSAS doesn't support). -->

### Partition
`Partition` · Partition · Options · read-only

The partition this data coverage definition belongs to. The **Properties** view doesn't show it. In C# scripts, use it to get from the definition back to its partition.
