---
uid: object-properties-model
title: Model properties
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
# Model properties

<!--
SUMMARY: Reference for the properties of the model object, such as culture, collation, default storage mode and Direct Lake behavior.
-->

This page covers the properties of the model object. Each entry gives the property's name in the Tabular Object Model (TOM), its type and its category. For properties that most objects share, see @object-properties-common.

## Model

The model is the root object of a semantic model. Every table, relationship, role, perspective and culture belongs to it. Its properties apply to the whole model, such as the culture used for formatting, the default storage mode and options that change how Power BI and the engine behave. To see them, select the **Model** node at the top of the **TOM Explorer**.

Many model properties need a minimum compatibility level, and some apply only to Power BI and Fabric models or only to Analysis Services. The Properties view hides properties that don't apply to the current model. See @update-compatibility-level.

The properties in the **Data Access Options** category control how the Power Query (M) engine, also called the mashup engine, gets data during refresh. They apply only to data that the model loads through M, which means structured data sources and M partitions. They have no effect on legacy (provider) data sources or on DirectQuery queries. The TOM default is `false` for all three, and Power BI Desktop enables `LegacyRedirects` and `ReturnErrorValuesAsNull` on new models.

<!-- TODO (not verifiable from TE3 source): Microsoft's TOM reference only says these are "options for the M data engine". Confirm that they have no effect on provider data sources and DirectQuery, and that the Power BI service honors all three. -->

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Object Type](xref:object-properties-common#object-type)
- [Translated Names](xref:object-properties-common#translated-names)
- [Translated Descriptions](xref:object-properties-common#translated-descriptions)

### Database
`Database` · Database · Basic · read-only

The database that contains the model. Expand the property to see and change database-level settings, such as **Compatibility Level**, which sets the features and properties that the model supports.

In Tabular Editor 3, you can edit these settings under `Database`:

- **Name** and **ID**: the name and ID of the database. Changing them has no effect on a database that's already deployed.
- **Compatibility Level** and **Compatibility Mode**. When you're connected to a server, Tabular Editor 3 rejects a compatibility level that the server doesn't support.
- **Description**, **Unicode Character Behavior** and **Visible**.

These settings are read-only and only have a value when you're connected to a server: **Version**, **Estimated Size** (in MB), **Last Processed**, **Last Update**, **Last Schema Update**, **Created Timestamp**, **Server Name** and **Server Version**.

Tabular Editor 2 shows the same settings under `Database`, except **Unicode Character Behavior**, and shows **Estimated Size** as `EstimatedSize`.

You can't lower the compatibility level after you raise it. See @update-compatibility-level and @change-compatibility-mode. The Best Practice Analyzer (BPA) rule @kb.bpa-powerbi-latest-compatibility flags Power BI models that don't use the latest compatibility level.

### Enable Fast Combine
`FastCombine` · bool · Data Access Options · compatibility level 1400+

When `true`, Power Query ignores the privacy levels of the data sources. This is the same as the **Ignore the Privacy levels and potentially improve performance** option in Power BI Desktop.

Privacy levels stop Power Query from sending data from one source to another, for example from folding values from an Excel file into a SQL query. With privacy levels applied, refresh can be slower, or fail with a `Formula.Firewall` error when a query combines sources. Enable this option only when you trust all the data sources in the model.

### Enable Legacy Redirects
`LegacyRedirects` · bool · Data Access Options · compatibility level 1400+

When `true`, Power Query follows a redirect from an HTTPS address to an HTTP address, and the data then travels unencrypted. The TOM default is `false`. Power BI Desktop enables it on new models.

### Return Error Values As Null
`ReturnErrorValuesAsNull` · bool · Data Access Options · compatibility level 1400+

When `true`, a value that causes an error during refresh, for example text that can't be converted to a number, loads as a blank value. When `false`, the TOM default, the error makes the refresh fail. Power BI Desktop enables it on new models. With `true`, bad values become blanks without an error, which hides data quality problems.

### Collation
`Collation` · string · Options

The rules that the engine uses to compare and sort text, as a Windows collation name. The collation sets whether comparisons are case-sensitive and accent-sensitive. For example, with `Latin1_General_CI_AS` (case-insensitive), `apple` and `Apple` are the same value in a column, in relationships and in DAX comparisons. With `Latin1_General_CS_AS` (case-sensitive), they're different values.

When it's empty, the default collation of the server or service applies. Set it when the data depends on case, for example product codes where `ab1` and `AB1` are different products, or for a Direct Lake model on a case-sensitive Fabric warehouse (see @direct-lake-guidance).

Set the collation when you create the model or before you add any tables. The TOM API has separate operations, `UpdateCollation` and `UpdateCulture`, to change the collation of a model that already exists on a server. On SQL Server Analysis Services and Azure Analysis Services, you must set the data source credentials again after such a change.

Tabular Editor doesn't use those operations. If you change `Collation` in the Properties view and save to a database that already contains tables, the change is rejected with the error "Culture and Collation properties of the Model object may be changed only before any other object has been created". SQL Server 2025 Analysis Services, Azure Analysis Services and the Power BI service all return this error, and on SQL Server 2025 Analysis Services the database keeps its old collation.

### Culture
`Culture` · string · Options

The language and region of the model, as a culture name such as `en-US` or `de-DE`. The engine uses it to format values, for example the decimal separator and date format that the `FORMAT` function uses when you don't give it a locale, and to sort and compare text in a language-aware way. It's also the language of the model's untranslated names and descriptions. Translations for other languages are cultures in the `Cultures` collection. Pick the culture from the list in the Properties view.

According to Microsoft, you can't change the culture once a child object uses it. In practice, this applies as soon as the model contains any other object, such as a table. Tabular Editor 3 accepts the change in the Properties view, and the engine rejects it on save with the error "Culture and Collation properties of the Model object may be changed only before any other object has been created". SQL Server 2025 Analysis Services, the Power BI service and Azure Analysis Services all return this error. To change the culture of a model that already exists on a server, the TOM API has a separate `UpdateCulture` operation.

### Source Query Culture
`SourceQueryCulture` · string · Options · compatibility level 1520+

The culture that Power Query uses to interpret values during refresh, for example when it converts the text `1.234,5` to a number or `03/04/2026` to a date. It's the same setting as **Locale for import** under **Regional settings** in Power BI Desktop.

Set it when the source data uses another format than `Culture`, for example a model in `en-US` that loads CSV files written in `de-DE`. When it's empty, Power Query uses `Culture`. When it's set, it takes precedence over `Culture` during refresh. For example, in a model with `Culture` set to `en-US`, `Date.FromText ( "01/02/2024" )` returns 2 January 2024 when `SourceQueryCulture` is empty, and 1 February 2024 when it's `nl-NL`. In a new model saved from Power BI Desktop, it holds the file's **Locale for import**, for example `en-NL`.

### Default Mode
`DefaultMode` · ModeType · Options

The storage mode of the partitions whose own `Mode` is `Default`. Partitions with an explicit mode keep their mode when this property changes. See @object-properties-partitions.

| Value | Meaning |
|---|---|
| `Import` | Data is loaded into the model's memory at refresh time. Queries don't go to the source. |
| `DirectQuery` | Data stays in the source. Each query is translated into a query against the source. |
| `DirectLake` | Data is read directly from Delta tables in OneLake. Fabric only, compatibility level 1604 and higher. See @direct-lake-sql-model. |

The storage mode type also has the values `Dual`, `Push` and `Default`. Tabular Editor 3 accepts only `Import`, `DirectQuery` or `DirectLake` for the model, and `DirectLake` only in editions that support Direct Lake. `Default` applies only to partitions, where it means "use the model's `DefaultMode`".

In Analysis Services, set `DefaultMode` to `DirectQuery` to make the whole model a DirectQuery model. Power BI Desktop sets the mode on each partition.

To convert Import tables to Direct Lake on OneLake, use the @script-convert-import-to-dlol script.

### Default Data View
`DefaultDataView` · DataViewType · Options

For DirectQuery models in Analysis Services, the partitions that the engine uses to answer queries. Sample partitions hold a subset of the data, for use while designing a DirectQuery model in Visual Studio. Partitions with `DataView` set to `Default` inherit this setting.

| Value | Meaning |
|---|---|
| `Full` | Queries use the partitions whose `DataView` is `Full` or `Default`. Use this for in-memory models and for deployed DirectQuery models. |
| `Sample` | Queries use the partitions whose `DataView` is `Sample` or `Default`, for use while designing the model. |
| `Default` | Only valid on partitions, where it means "use the model's `DefaultDataView`". |

Power BI doesn't use data views.

SQL Server 2025 Analysis Services accepts `Sample` at compatibility level 1700. A table with a `DirectQuery` partition plus `Import` partitions whose `DataView` is `Sample` saves without errors.

<!-- TODO (not verifiable from TE3 source): whether the engine still uses sample partitions anywhere at compatibility level 1400 and higher (the save is accepted, the effect isn't observable). -->

### Default Measure
`DefaultMeasure` · Measure · Options · compatibility level 1400+

The measure that MDX clients such as Excel use when a query doesn't specify a measure. Pick it from the list of measures in the model. When it's empty, the engine chooses the measure. Power BI and DAX queries don't use a default measure.

### Default Power BI Data Source Version
`DefaultPowerBIDataSourceVersion` · PowerBIDataSourceVersion · Options · compatibility level 1450+

The format that Power BI uses to store data source definitions in the model.

| Value | Meaning |
|---|---|
| `PowerBI_V1` | Legacy format. The M expressions are stored directly inside the connection strings of the data sources. |
| `PowerBI_V2` | Legacy format. Data sources use shared M expressions. |
| `PowerBI_V3` | The *enhanced metadata* format, which supports basic partition management operations. Needs compatibility level 1465 or higher. Power BI Desktop has used it for all new models since 2020. |

Power BI uses this property when it converts a model from an older format. Editing a model through the XMLA endpoint requires `PowerBI_V3`. Don't change it on a model that Power BI created.

When you create a Power BI model at compatibility level 1450 or higher, Tabular Editor 3 sets this property to `PowerBI_V3`. Tabular Editor 3 treats a model with `PowerBI_V3` and an unknown compatibility mode as a Power BI model. When you open a Power BI Desktop model or a .pbit file with the setting that limits editing to features Power BI supports, a model that isn't `PowerBI_V3` opens read-only.

### Data Source Default Max Connections
`DataSourceDefaultMaxConnections` · int · Options · compatibility level 1510+

The maximum number of connections that the engine opens at the same time to a single data source during refresh. The default is `10`. It applies to data sources whose `MaxConnections` is `-1`, and to sources that have no data source object in the model, which is the case for most Power BI models, where the source is defined in M.

Increase it to refresh more tables or partitions in parallel when the source can handle the load, or decrease it to protect a busy source. The service can still limit the number of connections.

<!-- TODO (not verifiable from TE3 source): whether 0 or -1 have a special meaning on this property during refresh. SSAS 2025 accepts both on save without validation. -->

### Data Source Variables Override Behavior
`DataSourceVariablesOverrideBehavior` · DataSourceVariablesOverrideBehaviorType · Options · compatibility level 1475+

Whether a refresh command can override the data source variables of the model, for example to point the refresh at another server or database than the one defined in the model.

| Value | Meaning |
|---|---|
| `Disallow` | Overrides of data source variables are rejected. |
| `Allow` | Overrides of data source variables are allowed. |

<!-- TODO (not verifiable from TE3 source): Microsoft's TOM reference only says "Queries won't allow / allow data source variables override". Confirm what "data source variables" are and which commands can override them (possibly related to @refresh-overrides). -->

### Direct Lake Behavior
`DirectLakeBehavior` · DirectLakeBehavior · Options · compatibility level 1604+

What a Direct Lake model does when a query can't be answered in Direct Lake mode, for example when a table exceeds the guardrails of the capacity, a table is a SQL view or the SQL analytics endpoint enforces row-level security. In that case, the model can *fall back* to DirectQuery against the SQL analytics endpoint.

| Value | Meaning |
|---|---|
| `Automatic` | The query falls back to DirectQuery when needed. This is the default. |
| `DirectLakeOnly` | Fallback is disabled. A query that can't run in Direct Lake mode fails with an error. |
| `DirectQueryOnly` | All queries use DirectQuery. Use this to test or compare performance. |

Fallback is often much slower than Direct Lake, and `DirectLakeOnly` turns a slow fallback into an error. The property only applies to Direct Lake on SQL. Direct Lake on OneLake never falls back to DirectQuery. See @direct-lake-guidance and @direct-lake-sql-model.

### Default Direct Lake Indexing Behavior
`DefaultDirectLakeIndexingBehavior` · DirectLakeIndexingBehavior · Options · preview compatibility level

How the engine builds and persists the Direct Lake specific indexes of the model. Microsoft's TOM library describes the values as follows:

| Value | Meaning |
|---|---|
| `Auto` | Build in-memory indexes during data load or query execution when needed, as the TOM library describes it. |
| `Explicit` | The model builds and persists the index only when you request it with a *refresh indexes* operation. Other refresh types don't build indexes. |
| `Full` | The model builds and persists indexes as part of *refresh full*, *refresh calculate* and *refresh indexes* operations. |
| `Default` | Use the default index building and persistence behavior of the model. |

This property needs a preview compatibility level, and Tabular Editor 3 doesn't show it in the Properties view. You can set it in a C# script.

### Discourage Composite Models
`DiscourageCompositeModels` · bool · Options · compatibility level 1560+

When `true`, report authors can't build a composite model on top of this model, that is, connect to it with DirectQuery and combine it with other data. When a report author connects to a published model that has this set to `true`, Power BI Desktop doesn't show **Make changes to this model**, and the author can't add other data to the report. Only a live connection to the model remains possible.

### Discourage Implicit Measures
`DiscourageImplicitMeasures` · bool · Options · compatibility level 1470+

When `true`, report authors in Power BI can't create *implicit measures*, the sum or count that Power BI calculates when you drag a numeric column into a visual. Report authors can only use the measures defined in the model, and the `SummarizeBy` setting of columns no longer applies in reports.

Models with calculation groups must have it enabled, because calculation groups only apply to explicit measures. Power BI Desktop and Tabular Editor 3 turn it on when you add a calculation group. While the model contains a calculation group, you can't set it back to `false` in Tabular Editor 3.

### Discourage Report Measures
`DiscourageReportMeasures` · bool · Options

When `true`, Power BI discourages report authors from creating report-level measures in reports that connect live to this model.

You can't set this property. The TOM library only allows it at an internal compatibility level (2147483647), so Tabular Editor and any other tool that uses TOM reject the change at every released compatibility level. Tabular Editor 3 doesn't show it in the Properties view.

### Force Unique Names
`ForceUniqueNames` · bool · Options · compatibility level 1465+

When `true`, a measure can't have the same name as any column in the model, in any table, so a DAX reference such as `[Amount]` always points to one object. When `false`, a measure can share a name with a column in another table, and column references need the table name to tell them apart from the measure.

On SQL Server 2025 Analysis Services, the engine accepts setting it back to `false`. With `false`, a measure still can't have the same name as a column in its own table. The engine rejects setting it to `true` while a measure has the same name as a column in another table, so rename those first. The comparison ignores case.

A new model in Power BI Desktop has `ForceUniqueNames` set to `false`, and Power BI Desktop accepts changing it either way.

### Max Parallelism Per Query
`MaxParallelismPerQuery` · int · Options · compatibility level 1569+

The maximum number of storage engine operations that the engine runs in parallel for a single DAX query. It matters most for DirectQuery, where each operation is a separate query against the source. A higher value can make visuals faster when the source can handle the extra queries, and a lower value protects the source.

The default is `0`, which leaves the decision to the service. The Power BI service accepts any value without validation, including negative numbers and values as high as `100000`.

<!-- TODO (not verifiable from TE3 source): Microsoft's TOM reference describes this as "maximum degree of parallelism for query in formula engine". Confirm that 0 means "let the service decide", the valid range, and whether it applies to Import models too. -->

### Max Parallelism Per Refresh
`MaxParallelismPerRefresh` · int · Options · compatibility level 1568+

The maximum number of tasks, such as tables or partitions, that a refresh processes in parallel. The service can still limit the number based on the resources of the capacity. Decrease it to put less load on the data source, or increase it to refresh faster when the source and the capacity can handle it.

The default is `-1`, which leaves the number to the service. The Power BI service accepts any value without validation.

<!-- TODO (not verifiable from TE3 source): confirm that -1 means "let the service decide", and the valid range. -->

In Tabular Editor 3, you can also set the maximum parallelism for a single refresh operation in the [Advanced Refresh dialog](xref:advanced-refresh).

### Metadata Access Policy
`MetadataAccessPolicy` · MetadataCategory · Options · compatibility level 1703+

Which metadata users with read permission can see when they query the model's metadata, for example with DMVs or the DAX `INFO` functions. It doesn't apply to users with write or admin permission.

| Value | Meaning |
|---|---|
| `Inherited` | Use the behavior that the system defines. |
| `Basic` | Readers can't access sensitive metadata in the model, such as measure definitions or other calculation expressions. |
| `CalculationDefinitions` | Readers can also read the metadata related to the definitions of calculations. |

Set `Basic` when the logic in the model is sensitive and readers only need to use it. `MetadataAccessPolicy` doesn't hide any data. To secure data, see @roles-and-rls.

<!-- TODO (not verifiable from TE3 source): the meanings above come from Microsoft's TOM library. Confirm what the system-defined behavior for Inherited is (workspace, tenant or service setting) and exactly which metadata Basic hides. -->

### Selection Expression Behavior
`SelectionExpressionBehavior` · SelectionExpressionBehaviorType · Options · compatibility level 1609+

What the calculation groups in the model return when a user selects several calculation items or none and the calculation group has no `MultipleOrEmptySelectionExpression`, and how subtotals behave when a visual groups by the calculation group.

| Value | Meaning |
|---|---|
| `Automatic` | The default. Currently the same as `NonVisual`. According to Microsoft, models above a future compatibility level will use `Visual`. |
| `Visual` | A multiple or empty selection returns `BLANK()`. When a visual groups by the calculation group, subtotals are calculated by evaluating the selected measure in the context of the calculation group. |
| `NonVisual` | A multiple or empty selection returns `SELECTEDMEASURE()`. When a visual groups by the calculation group, subtotals are hidden. |

See @object-properties-calculation-groups.

### Value Filter Behavior
`ValueFilterBehavior` · ValueFilterBehaviorType · Options · compatibility level 1606+

How `SUMMARIZECOLUMNS` applies filters on two or more columns of the same table. Power BI generates `SUMMARIZECOLUMNS` for almost every visual, so this property affects most report queries.

| Value | Meaning |
|---|---|
| `Automatic` | The default. According to Microsoft, it currently means `Coalesced`. Microsoft plans to make new models set to `Automatic` use `Independent` in the future. |
| `Coalesced` | Filters on columns of the same table are combined, and only the combinations that exist in the table remain. This is known as *auto-exist*. It can make measures return unexpected results, for example when a measure removes one of the filters with `ALL`. |
| `Independent` | Each filter is applied on its own, without auto-exist. |

Changing this property can change the numbers in existing reports, so test the reports of a model that's in use before you change it. A new model saved from Power BI Desktop has `ValueFilterBehavior` set to `Independent`.

### M Attributes
`MAttributes` · string · Options · compatibility level 1535+

Attributes of the Power Query section document that holds the model's M expressions, as an M record. A new model saved from Power BI Desktop leaves it empty.

<!-- TODO (not verifiable from TE3 source): which tools or scenarios fill in M Attributes, with an example value. -->

### Storage Location
`StorageLocation` · string · Options

For Analysis Services only, the folder on the server's disk where the engine stores the model's data files. When it's empty, the server's default data folder applies. Power BI and Fabric don't use this property. Azure Analysis Services accepts a value without an error.

<!-- TODO (not verifiable from TE3 source): whether SQL Server Analysis Services 2016 and later or Azure Analysis Services still use Storage Location (the value is accepted, the effect isn't observable). -->

### Has Local Changes
`HasLocalChanges` · bool · Options · read-only

Whether the model has changes that haven't been saved to the engine yet. This is TOM's own state, separate from the unsaved changes in Tabular Editor. It's always `false` for a model that isn't connected to an engine, such as a model you opened from a file. Tabular Editor 3 doesn't show this property in the Properties view. You can read it in a C# script.

In Tabular Editor 3, the @unsaved-changes show which objects and properties differ from the last saved version of the model.

### Expressions
`Expressions` · collection of shared expressions · Options · read-only

The shared expressions of the model, such as Power Query parameters and queries that other queries refer to. Select **...** to edit the collection, or work with them in the **Shared Expressions** folder of the **TOM Explorer**. See @object-properties-data-sources. The @script-create-m-parameter script adds a Power Query parameter with a C# script.

### Query Groups
`QueryGroups` · collection of query groups · Options · read-only

The folders that group Power Query queries and parameters, as shown in the **Queries** pane of Power BI Desktop. See @object-properties-data-sources.

### Binding Info Collection
`BindingInfoCollection` · collection of binding info objects · Options · read-only

Hints that tell Fabric which data connection to use for a data source in the model, for example after the model is deployed to another workspace. See **Data binding hint** on @object-properties-data-sources.

### Functions
`Functions` · collection of functions · Options · read-only

The DAX User-Defined Functions (UDFs) of the model. See @object-properties-functions and @udfs. The BPA rule @kb.bpa-udf-use-compound-names flags functions whose names don't contain a `.` or `_` separator.

### Cultures
`Cultures` · collection of cultures · Translations, Perspectives, Security · read-only

The cultures, or translations, of the model. Each culture holds the translated names, descriptions and display folders for one language. Select **...** to add or remove cultures. To edit the translations, use the translation properties on each object or, in Tabular Editor 3, the @metadata-translation-editor. See @object-properties-perspectives-cultures and @how-to-work-with-perspectives-translations. To export the translations of a culture to a JSON file and import them again, see @import-export-translations.

### Perspectives
`Perspectives` · collection of perspectives · Translations, Perspectives, Security · read-only

The perspectives of the model. Select **...** to add or remove perspectives. To choose which objects each perspective shows, use `InPerspective` on each object or, in Tabular Editor 3, the @perspective-editor. See @object-properties-perspectives-cultures. The BPA rule @kb.bpa-perspectives-no-objects flags perspectives that contain no visible tables.

### Roles
`Roles` · collection of roles · Translations, Perspectives, Security · read-only

The security roles of the model. Roles control who can query the model and which data they see, through row-level and object-level security. Select **...** to add or remove roles. See @object-properties-security and @roles-and-rls. For step-by-step instructions, see @data-security-setup-rls and @data-security-setup-ols.
