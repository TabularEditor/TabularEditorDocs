---
uid: importing-tables
title: (Tutorial) Importing Tables
author: Daniel Otykier
updated: 2021-09-06
applies_to:
  editions:
    - edition: Desktop
      partial: TE3 Desktop Edition includes this feature. External tools adding/editing tables and columns to a Power BI Desktop model is not supported by Microsoft, however.
    - edition: Business
    - edition: Enterprise
---
# (Tutorial) Importing Tables

Tabular Editor 3 (starting with version 3.1.0) features a new **Table Import Wizard** that helps you create a data source in your model, and import tables/views from relational data sources such as a SQL Server database.

![Import Tables Wizard](~/images/import-tables-wizard.png)

## Types of TOM Data Sources

Depending on your version of Analysis Services, there are different ways of defining data sources within the model metadata:

- **Provider (aka. Legacy)**: Available in every version of Analysis Services and every compatibility level. Supports a limited range of sources, mostly relational through OLE DB/ODBC drivers. Partitions are usually defined using a SQL statement which is executed natively against the source. Credentials are managed in the Provider Data Source object in the Tabular Object Model and stored and encrypted server-side.
- **Structured (aka. Power Query)**: Available since SQL Server 2017 (compatibility level 1400+). Supports a wider range of data sources than Legacy providers. Partitions are usually defined using M (Power Query) expressions. Credentials are managed in the Structured Data Source object in the Tabular Object Model and needs to be specified upon every deployment to Analysis Services.
- **Implicit data sources**: Exclusively used by Power BI datasets. No explicit Data Source object is created in the model. Instead, the M (Power Query) expression implicitly defines the data source. Credentials are not stored in the Tabular Object Model, but managed by Power BI Desktop or the Power BI Service.

> [!NOTE]
> The Table Import Wizard and Update Table Schema feature of Tabular Editor 2.x only supports Legacy data sources with SQL partitions. In other words, there are no support for Power Query partitions. For this reason, Legacy data sources are usually recommended, as they provide the highest level of interoperability between the developer tools.

## Importing new tables

When importing tables (Model menu > Import tables...), Tabular Editor presents you with the options mentioned above (for creating a new data source), as well as a list of data sources already present in the model. Avoid creating new data sources if the tables you want to import are available in one of the data sources already specified in the model.

> [!TIP]
> A tabular model is generally regarded as an in-memory optimized semantic cache of a relational data warehouse. For this reason, a model should ideally only contain a single data source which would point to a SQL-based data warehouse or data mart.

## Creating a new data source

If you need to create a new data source, Tabular Editor provides you with a list of supported data sources:

![Create New Source](~/images/create-new-source.png)

Note that Analysis Services and Power BI in particular supports a much wider range of data sources, however the sources listed in the screenshot above are the ones that Tabular Editor is able to connect for the purpose of automatically importing table metadata (that is, column names and data types). For data sources not on this list, Tabular Editor 3 can still [update table schema by utilising Analysis Services](#updating-table-schema-through-analysis-services).

After choosing one of the data sources on the list, Tabular Editor displays a connection details dialog, allowing you to specify server addresses, credentials, etc. specific to the data source you want to create. The settings that you specify should be those that Tabular Editor should use for establishing a local connection to the source. These settings are saved in your @user-options.

![Sql Auth](~/images/sql-auth.png)

If you want Analysis Services to use different credentials when connecting, you can specify that by editing the data source properties of the Tabular Object Model after importing the tables.

## Choosing objects to import

Once your data source has been defined, you get the option of choosing tables/views from a list, or specifying a native query to be executed against the source.

![Source Options](~/images/source-options.png)

If you select the first option, Tabular Editor will connect to the source and display a list of tables and views that you can preview on the next page:

![Choose Source Objects](~/images/choose-source-objects.png)

You can import multiple tables/views at once by checking them on the left side. For each table/view, you may deselect/select columns to import.

> [!TIP]
> If you are in control of the source, we recommend to always create a view on top of the tables you wish to import. In the view, make sure to correct any names, spellings, etc. to be used in the tabular model, and get rid of any columns not needed by the tabular model (system columns, timestamps, etc.).
>
> Then, in the model, import all columns from this view (basically generating a `SELECT * FROM ...` statement). This makes maintenance easier, as only need to run a Schema Update in Tabular Editor to determine if anything was changed in the source.

![Advanced Import](~/images/advanced-import.png)

If you change the preview mode to "Schema only" using the dropdown in the top left corner, it is possible to change the imported data type and column name for every source column. This may be useful for example if your source using floating-point values, but you want the data to be imported as fixed-decimal.

![Confirm Selection](~/images/confirm-selection.png)

On the last page, confirm your selection and choose which type of partitions to create. For provider data sources, the default type of partition to be created is `SQL`, where as for structured data sources, it is `M`. 

At this point, you should see your tables imported with all columns, data types and source column mappings applied:

![Import Complete](~/images/import-complete.png)

## Updating table schema

If columns are added/changed in the source, you can use Tabular Editor's **Update table schema** feature at any time.

![Update Table Schema](~/images/update-table-schema.png)

This menu item can be invoked at the model level, as well as on a collection of tables or even individual table partitions.

When using this option, Tabular Editor will connect to all the relevant data sources (prompting for credentials as needed), in order to determine if new columns need to be added or existing column modified or removed.

> [!IMPORTANT]
> If a column that was previously imported to your tabular model has been removed or renamed in the source, you must update the table schema in your tabular model. Otherwise data refresh operations may fail.

![Schema Compare Dialog](~/images/schema-compare-dialog.png)

In the screenshot above, Tabular Editor detecgted a few new columns, a single data type change, and two columns that were renamed in the source. Note that detection of a column rename only works for simple changes. In other cases, a name change usually results in Tabular Editor detecting a column removal and a column addition, which is the case for the `Tax Amount` column below, which seems to have been renamed to `TaxAmt` in the source.

To avoid breaking existing DAX formulas that rely on the `[Tax Amount]` column, you can hold down the Ctrl-button and click on the two rows in the Schema Change dialog, then right-click in order to combine the column removal and column addition into a single SourceColumn update operation:

![Combine Sourcecolumn Update](~/images/combine-sourcecolumn-update.png)

If you do not want the name change to be propagated to the imported column (but only want to update the SourceColumn property to reflect the changed name in the data source), you can deselect the `Name` update operation in the dropdown:

![Deselect Name](~/images/deselect-name.png)

## Updating table schema through Analysis Services

By default, Tabular Editor 3 attempts to connect directly to the data source, for purposes of updating the imported table schema. Naturally, this only works when the data source is one that is supported by Tabular Editor 3. If you need to update the schema of a table imported from a data source that is not supported by Tabular Editor 3, you can enable the **Use Analysis Services for change detection** option under **Tools > Preferences > Schema Compare**.

![Update Table Schema Through As](../../images/update-table-schema-through-as.png)

When this option is enabled and Tabular Editor 3 is connected to Analysis Services or the Power BI XMLA endpoint, you can update the schema of tables imported from **any** data source supported by Analysis Services or Power BI.

> [!NOTE]
> The **Use Analysis Services for change detection** option only works while Tabular Editor 3 is connected to Analysis Services or the Power BI XMLA endpoint. For this reason, we recommend that developers always use the [Workspace Mode](xref:workspace-mode) when developing models.

When the **Use Analysis Services for change detection** option is enabled, Tabular Editor 3 will use the following technique when a schema update is requested:

1. A new transaction is created against the connected Analysis Services instance
2. A new temporary table is added to the model. This table uses a Power Query partition expression that returns the schema of the original expression, of which a schema update was requested. This is done using the [`Table.Schema` M function](https://docs.microsoft.com/en-us/powerquery-m/table-schema).
3. The temporary table is refreshed by Analysis Services. Analysis Services takes care of connecting to the data source in order to retrieve the updated schema.
4. Tabular Editor 3 queries the content of the temporary table to obtain the schema metadata.
5. The transaction is rolled back, leaving the Analysis Services database or Power BI dataset in the original state it was in before step 1.
6. Tabular Editor 3 displays the "Apply Schema Changes" dialog as shown above, in case there are any schema changes.

Using this technique, Tabular Editor 3 makes it possible to import and update tables from data sources otherwise not supported.

### Importing new tables through Analysis Services

In order to import a table from a data source otherwise not suported, you can simply copy an existing table from that data source, modify the M expression on the partition query of the copied table, then save your changes to the workspace database and update the table schema as described above.