---
uid: object-properties-columns
title: Column properties
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
# Column properties

<!--
SUMMARY: Reference for the properties of data columns, calculated columns, calculated table columns, and the Alternate Of and Variation objects that belong to columns.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

This page lists the properties of the three kinds of columns and of the two objects that belong to a column, Alternate Of and Variation. For properties that most objects share, see @object-properties-common.

A table contains three kinds of columns:

- a **data column** gets its values from the table's partitions, for example from a Power Query (M) query or a SQL query
- a **calculated column** gets its values from a DAX expression that's evaluated for each row of the table
- a **calculated table column** is a column of a calculated table, defined by the calculated table's DAX expression

[Properties of all columns](#properties-of-all-columns) describes the properties that the three kinds share. The sections after it list the properties that are specific to one kind of column.

## Properties of all columns

These properties apply to data columns, calculated columns and calculated table columns.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Display Folder](xref:object-properties-common#display-folder)
- [Hidden](xref:object-properties-common#hidden)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Changed Properties](xref:object-properties-common#changed-properties)
- [DAX identifier](xref:object-properties-common#dax-identifier)
- [Error Message](xref:object-properties-common#error-message)
- [Object Type](xref:object-properties-common#object-type)
- [State](xref:object-properties-common#state)
- [Lineage Tag](xref:object-properties-common#lineage-tag)
- [Source Lineage Tag](xref:object-properties-common#source-lineage-tag)
- [Translated Names](xref:object-properties-common#translated-names)
- [Translated Descriptions](xref:object-properties-common#translated-descriptions)
- [Translated Display Folders](xref:object-properties-common#translated-display-folders)
- [Synonyms](xref:object-properties-common#synonyms)
- [Shown in Perspective](xref:object-properties-common#shown-in-perspective)

### Data Type
`DataType` · DataType · Basic

The data type of the column's values. It determines how the engine stores the values and which DAX functions and operators accept them. Both columns of a relationship must have the same data type.

| Value | Meaning |
|---|---|
| `String` | Text. Called **Text** in Power BI. |
| `Int64` | A 64-bit whole number. Called **Whole number** in Power BI. |
| `Double` | A 64-bit floating-point number. Called **Decimal number** in Power BI. Totals can show small rounding differences. |
| `Decimal` | A fixed-point number with four decimal places. Called **Fixed decimal number** in Power BI. Use it for currency amounts. |
| `DateTime` | A date and time. Power BI shows it as **Date**, **Time** or **Date/time**, depending on the format string. |
| `Boolean` | `TRUE` or `FALSE`. |
| `Binary` | Binary data, such as the bytes of an image. DAX can't use binary values and Power BI doesn't load binary columns. |
| `Automatic` | For internal use only. |
| `Unknown` | The initial value of a new column. The engine replaces it with the actual data type when the column is saved to the server. |
| `Variant` | A value that can be of different types. Used for measures only. |

The **Properties view** shows some values with a longer name, for example `Int64` as **Integer / Whole Number (int64)** and `Decimal` as **Currency / Fixed Decimal Number (decimal)**. The dropdown lists every value in the table, including `Automatic`, `Unknown` and `Variant`, and accepts all of them. For a data column, pick one of the first seven values.

For a data column, the data type must match the data that the partition query returns, or the engine converts the values during refresh. If a conversion fails, for example on text that isn't a number, the refresh fails. Changing the data type in Tabular Editor leaves the partition query unchanged: if you change a column from `String` to `Int64`, also make the query return whole numbers, for example by changing the type in Power Query.

For calculated columns and calculated table columns, the data type follows from the expression. See [Data Type Inferred](#data-type-inferred).

The Best Practice Analyzer (BPA) rule @kb.bpa-relationship-same-datatype flags relationships between columns that have different data types.

### Format String
`FormatString` · string · Basic

The format that client tools apply when they display the column's values, for example `#,0`, `0.00%` or `yyyy-mm-dd`. The syntax is the same as for the DAX [FORMAT](https://dax.guide/format) function. DAX queries return the unformatted value. The format also applies to the implicit measures that Power BI creates when a report author drags a numeric column into a visual.

Visible numeric and date columns without a format string show raw values such as `1234567.891` or a date with a time part. See @kb.bpa-format-string-columns.

### Sort By Column
`SortByColumn` · Column · Basic

Another column in the same table whose values set the order of this column's values. For example, sort a `Month Name` column by a `Month Number` column to show the months in calendar order.

Each value of this column must have exactly one value in the sort column. For example, `January` must always have month number `1`. If a value has more than one sort value, the engine reports an error when the column is refreshed or recalculated.

> [!NOTE]
> When a report groups by a column that has a sort column, Power BI also groups by the sort column. As a result, `CALCULATE ( [Sales], REMOVEFILTERS ( 'Date'[Month Name] ) )` keeps the filter on `'Date'[Month Number]` and returns an unchanged result. Remove the filter on both columns, or on the whole table.

The C# script @script-create-date-table creates a date table and sets `SortByColumn` on its name columns.

### Summarize By
`SummarizeBy` · AggregateFunction · Basic

The aggregation that client tools apply when a report author drags the column into a visual as a value, without a measure. Power BI calls this *default summarization*, and the measure it creates on the fly an *implicit measure*.

| Value | Meaning |
|---|---|
| `Default` | The client tool decides. Numeric columns are summed and other columns aren't summarized. |
| `None` | Don't summarize. Power BI shows it as **Don't summarize**. |
| `Sum` | The sum of the values. |
| `Min` | The smallest value. |
| `Max` | The largest value. |
| `Count` | The number of values. |
| `Average` | The average of the values. |
| `DistinctCount` | The number of distinct values. |

In Power BI Desktop, a numeric column with `Default` behaves like `Sum`: it shows with the Σ icon in the **Data** pane and is added to a visual as **Sum of** the column. A text column with `Default` isn't summarized. Excel ignores this property, and a PivotTable only aggregates through measures.

Set `None` on numeric columns that aren't meaningful to add up, such as keys, years, phone numbers or unit prices, or report authors get totals such as the sum of all customer IDs. See @kb.bpa-do-not-summarize-numeric.

`SummarizeBy` has no effect on DAX or on explicit measures. When `DiscourageImplicitMeasures` is enabled on the model (see @object-properties-model), Power BI creates no implicit measures and this property has no effect. The C# script @script-create-sum-measures-from-columns creates a `SUM` measure for each selected column and hides the column.

### Alignment
`Alignment` · Alignment · Options

The horizontal alignment of the column's values in client tools that support it.

| Value | Meaning |
|---|---|
| `Default` | The client tool decides. Most tools align numbers to the right and text to the left. |
| `Left` | Align to the left. |
| `Right` | Align to the right. |
| `Center` | Center the values. |

Power BI ignores this property. Table and matrix visuals always align text to the left and numbers to the right, and you set other alignments in the formatting options of the visual. In an Excel PivotTable connected to the model, right- and center-aligned columns also show with the default alignment.

### Alternate Of
`AlternateOf` · AlternateOf · Options · compatibility level 1460+

Makes this column part of a user-defined aggregation. An aggregation table holds pre-aggregated data, for example sales per customer and product. `AlternateOf` maps this column to the column of the detail table that it stands in for and sets how the values were aggregated, and the engine then answers queries from the smaller aggregation table when it can.

The property appears at compatibility level 1460 or higher and stays empty until you add an Alternate Of. In Tabular Editor 2 and Tabular Editor 3, click the **...** button of the empty property, or right-click the property and choose **Add Alternate Of**. The new Alternate Of has `Summarization` `Sum`. Expand the property to set the properties described under [Alternate Of](#alternate-of-1). To remove it, right-click the property and choose **Remove Alternate Of**. For a walkthrough, see @user-defined-aggregations.

The C# script @script-implement-user-defined-aggregations sets up the detail table for a selected aggregation table and configures `AlternateOf` on its numeric columns.

### Data Category
`DataCategory` · string · Options

The kind of value the column holds, which client tools use to treat the column in a special way. For example, Power BI puts a column with category `City` on a map, shows a column with category `ImageUrl` as an image and shows a column with category `WebUrl` as a clickable link. Leave it empty for a regular column.

In Tabular Editor 3, the dropdown lists all the categories that the protocol defines, in alphabetical order, and you can also type any other value. The value isn't validated, so spell it exactly as listed. Power BI uses these categories:

| Value | Shown in Power BI as | Use for |
|---|---|---|
| `Address` | Address | Street addresses. |
| `City` | City | City names. |
| `County` | County | County names. |
| `StateOrProvince` | State or Province | State or province names. |
| `PostalCode` | Postal code | Postal or ZIP codes. |
| `Country` | Country/Region | Country or region names or codes. |
| `Continent` | Continent | Continent names. |
| `Place` | Place | Names or descriptions of a location that don't fit another category. |
| `Latitude` | Latitude | Latitude in decimal degrees, for example `51.5072`. |
| `Longitude` | Longitude | Longitude in decimal degrees, for example `-0.1276`. |
| `WebUrl` | Web URL | Links that users can click. |
| `ImageUrl` | Image URL | URLs of images that visuals show as images. |
| `Barcode` | Barcode | Barcodes that the Power BI mobile app scans to filter a report. |

Geographic categories tell map visuals what kind of location a value is, for example that `Paris` is a `City`.

The dropdown spells two of the categories as `WebURL` and `ImageURL` and has no `Barcode` entry. Power BI ignores case, so `ImageUrl` and `ImageURL` both show the value as an image in a table visual, and `WebUrl` and `WebURL` both show it as a link. The Tabular Object Model (TOM) stores the value exactly as you type it. Power BI accepts `Barcode`, but a table visual shows the value as plain text; only the Power BI mobile apps use it.

The protocol defines many more categories, for example `Id`, `Image` and time categories such as `Years` and `Months`, which older tools used. Power BI ignores most of them. The dropdown also lists `PaddedDateTableDates`, a category that Power BI uses and the protocol doesn't define. Power BI Desktop writes the time categories on the columns of its auto date/time tables: `PaddedDateTableDates` on the date column, and `Years`, `Quarters`, `QuarterOfYear`, `Months`, `MonthOfYear` and `DayOfMonth` on the other columns.

<!-- TODO (not verifiable from TE3 source): whether Power BI uses these column categories for anything, or only writes them. -->

To mark a table as a date table, set `DataCategory` on the table to `Time` (see @object-properties-tables) and set `IsKey` to `true` on the table's date column.

### Display Ordinal
`DisplayOrdinal` · int · Options

A number that client tools can use to order the columns of a table, for example `10`, `20`, `30`. Only the relative order counts, so gaps leave room to insert a column later.

Power BI ignores it, and the **Data** pane in Power BI Desktop lists columns alphabetically whatever their `DisplayOrdinal`. To group columns there, use display folders.

### Encoding Hint
`EncodingHint` · EncodingHintType · Options · compatibility level 1400+

A hint to the engine about how to compress a numeric column in memory. Without a hint, the engine picks an encoding when it first loads data and can later re-encode the column during refresh, which takes time. With a hint, the engine starts with the hinted encoding.

| Value | Meaning |
|---|---|
| `Default` | The engine decides. |
| `Hash` | Store each distinct value once, in a dictionary, and refer to it by its position. Suits columns with few distinct values or with values that are far apart, such as key columns. |
| `Value` | Store the values themselves, made smaller with a little arithmetic. Suits numeric columns that you aggregate and whose values are close together, such as quantities or amounts. |

The engine can still choose a different encoding, and text columns always use hash encoding. Set a hint only when you've seen, for example in VertiPaq Analyzer, that the engine's encoding makes refresh slow or the model large.

### Group By Columns
`GroupByColumns` · GroupingColumnCollection · Options · read-only · compatibility level 1400+

Other columns in the same table that the engine also groups by whenever a query uses this column. Rows that have the same value in this column stay separate when their values in a group-by column differ.

Power BI uses this for field parameters. The column with the field names is grouped by the column with the field references, which keeps two fields with the same display name in separate rows. See @create-field-parameter.

MDX clients such as Excel treat these columns as a composite key, so you can't put a column with group-by columns in a PivotTable without the columns it's grouped by.

The property appears for Power BI and Fabric models at compatibility level 1400 or higher. You can change the columns in the collection: in Tabular Editor 3, click the **...** button to open a dialog with the other columns of the table, and select the columns to group by. TOM saves the columns in the column's `RelatedColumnDetails` object, and Tabular Editor removes that object when you remove the last column.

### Available In MDX
`IsAvailableInMDX` · bool · Options

Whether the engine builds an *attribute hierarchy* for the column, which MDX queries need. The default is `true`. Excel PivotTables use MDX and can only put a column on rows or columns when it's `true`. Power BI uses DAX and works without attribute hierarchies.

Setting it to `false` on hidden columns that MDX queries don't use, such as foreign keys and columns only used in measures, saves memory and refresh time. Keep it `true` for columns used in hierarchies, as a sort column, in variations or in calendars, and for columns that Excel users need. See @kb.bpa-set-isavailableinmdx-false and @kb.bpa-set-isavailableinmdx-true-necessary. The rule @kb.bpa-hide-foreign-keys flags foreign key columns that aren't hidden.

### Data Type Inferred
`IsDataTypeInferred` · bool · Options

Whether the engine derives the column's data type itself and ignores the value of `DataType`. It mostly matters for calculated columns and calculated table columns, whose data type follows from the DAX expression.

In Tabular Editor 3, while this is `true` on a calculated column or calculated table column, `DataType` is read-only and Tabular Editor updates it from the expression as you edit it, without a connection to a server. Set it to `false` to pick a data type yourself. When you set it back to `true` on a calculated table column, `DataType` resets to the data type of the column that the expression gets its values from.

<!-- TODO (not verifiable from TE3 source): document the effect of this property on data columns. TE3 has no special handling for data columns. -->

### Default Image
`IsDefaultImage` · bool · Options

Marks the column as the image that represents a row of the table, for example a product photo. It's one of the *table behavior* settings that Power View used. No current client uses it: Power View is retired, Power BI ignores it and Excel PivotTables ignore table behavior settings.

### Default Label
`IsDefaultLabel` · bool · Options

Marks the column as the label that identifies a row of the table to users, for example the product name. It's a table behavior setting that Power View used. No current client uses it. Power View and Power BI Q&A both supported it and are both retired.

### Key
`IsKey` · bool · Options

Marks the column as the key of the table, the column whose values identify each row. A table has at most one key column: when you set `IsKey` to `true` on a column, Tabular Editor sets it to `false` on the other columns of the table and leaves `IsUnique` and `IsNullable` unchanged. The key column can't contain duplicate or blank values, so a refresh that loads duplicates fails.

When you mark a table as a date table in Power BI, `IsKey` is set on the date column and the table's `DataCategory` is `Time`.

The BPA rule @kb.bpa-date-table-exists flags a model that has no calendar, no table with `DataCategory` `Time` and no `DateTime` key column.

### Nullable
`IsNullable` · bool · Options

Whether the column can contain blank (null) values. The default is `true`. If you set it to `false`, a refresh fails when the source returns a blank value, which works as a data quality check. A key column never allows blanks, whatever the value of this property.

### Unique
`IsUnique` · bool · Options

Whether the column contains only unique values. The engine enforces it, and a duplicate value makes a refresh of a data column fail. For a column of a calculated table, the save itself fails, because the engine recalculates the table right away. The error reads "Column 'Key' in Table 'Sales' contains a duplicate value 'a' and this is not allowed for columns on the one side of a many-to-one relationship or for columns that are used as the primary key of a table". Set it only on columns that are guaranteed to be unique, such as the key of a dimension table.

To see the distinct values of a column in a connected model, run the C# script @script-display-unique-column-values.

### Keep Unique Rows
`KeepUniqueRows` · bool · Options

A table behavior setting from Power View, meant to keep rows that share a value in this column separate when their keys differ, for example two customers with the same name. When it's `false`, those rows are grouped by value.

No current client acts on it. Power BI ignores it, and in an Excel PivotTable on SQL Server 2025 Analysis Services, two customers with the same name show as one row whether `KeepUniqueRows` is `true` or `false`. To show them separately, make the values unique, for example by adding the customer number to the name.

### Source Provider Type
`SourceProviderType` · string · Options

The column's data type in the data source, in the source's own terms, for example `nvarchar` or `WChar`. The engine can use it to generate queries against the source in DirectQuery mode. Tabular Editor 3 never fills it in, also not when it imports a table, so it only has a value when you or another tool set one. Most models, Power BI models included, leave it empty.

<!-- TODO (not verifiable from TE3 source): confirm which other tools fill in Source Provider Type (for example the Visual Studio table import wizard) and in which format (OLE DB type names or SQL type names). -->

### String Indexing Behavior
`StringIndexingBehavior` · IndexingBehavior · Options · compatibility level 1706+

Whether the engine builds an index on a text column, and whether it saves that index for reuse after a restart.

| Value | Meaning |
|---|---|
| `Off` | Don't build an index. |
| `Auto` | The default. Build the index when needed, without saving it. |
| `Explicit` | Build and save the index only when you run a refresh of type `RefreshIndex`. |
| `Full` | Build and save the index during a full refresh, a recalculation or a `RefreshIndex` refresh. |

In Power BI Desktop, whose engine supports compatibility level 1706, the engine accepts `Off` and `Auto` and rejects `Explicit` and `Full` with the error "Persist String Index feature is disabled". Recent versions of the TOM library only allow values other than `Auto` from compatibility level 1707.

<!-- TODO (not verifiable from TE3 source): document what the string index is used for (text search such as CONTAINSSTRING?) and when Explicit and Full become available. -->

### Full Text Indexing Behavior
`FullTextIndexingBehavior` · IndexingBehavior · Options · compatibility level 1708+

Whether the engine builds a full-text index on a text column and saves it. The full-text index enables the DAX functions `TEXTCONTAINS` and `TEXTSIMILARITY`. The default is `Off`.

| Value | Meaning |
|---|---|
| `Off` | The default. Don't build a full-text index. |
| `Auto` | The TOM library doesn't describe this value for full-text indexing. |
| `Explicit` | Build and save the index only when you run a refresh of type `RefreshIndex`. |
| `Full` | Build and save the index during refresh. |

<!-- TODO (not verifiable from TE3 source): what Auto does for full-text indexing, and which engines support compatibility level 1708. -->

### Table Detail Position
`TableDetailPosition` · int · Options

Adds the column to the table's *default field set*, the columns that a client tool shows when a user adds the whole table to a report or drills through to details. A positive number includes the column, and the columns appear in ascending order of this number. The default is `-1`, which leaves the column out. Power View and **Show Details** in Excel used the default field set.

Excel no longer uses it for drill-through: **Show Details** in an Excel PivotTable returns the table's columns whatever `TableDetailPosition` says. To choose the drill-through columns, set `DefaultDetailRowsExpression` on the table (see @object-properties-tables) or `DetailRowsExpression` on a measure (see @object-properties-measures).

### Variations
`Variations` · VariationCollection · Options · read-only

The variations of this column. A variation is something else that a client tool shows when a user picks this column. Power BI uses variations for *auto date/time*. See [Variation](#variation).

### Object Level Security
`ObjectLevelSecurity` · ColumnOLSIndexer · Translations, Perspectives, Security · read-only · compatibility level 1400+ · *shortcut to* the column permissions of each role

The object-level security (OLS) setting of this column in each role of the model. The property appears at compatibility level 1400 or higher when the model has at least one role. Expand it to see one entry per role, with one of these values:

| Value | Meaning |
|---|---|
| `Default` | No column-specific setting. The column follows the setting of its table in the role. In TOM, the role has no column permission for the column. |
| `None` | Users in the role can't see or query the column. For them the column doesn't exist, and visuals that use it show an error. |
| `Read` | Users in the role can see and query the column. |

You can change the value for each role. When you pick `None` or `Read`, Tabular Editor adds a column permission for the column to the role's table permission for the column's table, and creates that table permission if the role doesn't have one yet. When you pick `Default`, Tabular Editor removes the column permission. You can also set the same values on the role, under **OLS Column Permissions** (see @object-properties-security). See @data-security-setup-ols.

You can't combine row-level security from one role with object-level security from another. When a user is a member of such a combination of roles, the engine returns an error at query time.

Observed on SQL Server 2025 Analysis Services, the settings combine like this:

- `Default` follows the table: when the role's table permission is `Read`, the column is visible, and when it's `None`, the whole table is hidden, including this column
- a column can't be less restrictive than its table, and the engine rejects `Read` on a column whose table is `None`
- when a user is a member of several roles that all use OLS, the permissions add up, and the user can see a table or column if any of the roles allows it
- row-level and object-level security in the same role work together, for example a row filter on a table that the role hides with OLS still filters the related tables

## Data column

A data column gets its values from the table's partitions, in a Power BI model usually a Power Query (M) query. The column has the properties under [Properties of all columns](#properties-of-all-columns) and the one below.

In Tabular Editor 3, the @import-tables wizard creates data columns with their data types and source column mappings, and **Update table schema** updates them when the source changes.

### Source Column
`SourceColumn` · string · Basic

The name of the column in the result of the partition query that this column gets its values from. It must match the name that the query returns. If it doesn't, for example after someone renamed a column in Power Query, the refresh fails.

The column's `Name` and `SourceColumn` are separate, so you can rename the column in the model without changing the query and the other way round. Renaming a column in Tabular Editor leaves `SourceColumn` unchanged. With formula fix-up turned on, Tabular Editor updates the DAX expressions that refer to the renamed column. See @formula-fix-up-dependencies.

Every data column needs a source column. See @kb.bpa-data-column-source.

When a column is renamed in the source, **Update table schema** in Tabular Editor 3 reports a removed and a new column. Combine the two into a single `SourceColumn` update to keep the DAX formulas that use the column working.

## Calculated column

A calculated column gets its values from a DAX expression that's evaluated once for each row of the table when the table is refreshed. The engine stores the result like the values of a data column, which takes memory and makes the values fast to read. Use a calculated column for values that you slice, filter or group by, and a measure for values that you only aggregate.

The column has the properties under [Properties of all columns](#properties-of-all-columns) and the ones below. To add a calculated column in Tabular Editor 3, see @creating-and-testing-dax.

### Expression
`Expression` · string · Options

The DAX expression that calculates the value for each row, for example:

```dax
Sales[Quantity] * Sales[Unit Price]
```

The expression is evaluated in a *row context*, so it refers to the columns of the current row directly. To get a value from a related table, use [RELATED](https://dax.guide/related), for example `RELATED ( Product[Category] )`.

The engine recalculates the column when the table is refreshed, or when you change the expression and save the model to a connected server. In Tabular Editor 3, you edit the expression in the **Expression Editor** of the @dax-editor. The @table-preview shows the calculated values, or **(Calculation needed)** when the column must be recalculated first.

### Expression Context
`ExpressionContext` · ExpressionContext · Options · compatibility level 1705+

Whether the column has one value for everyone or is evaluated per user.

| Value | Meaning |
|---|---|
| `Standard` | The default. The column is calculated during refresh and has one value per row for all users. |
| `UserContext` | The column is evaluated per user, and the expression can call functions such as `USERPRINCIPALNAME`. |

Standard calculated columns, calculated tables, row-level security filters and relationships can't use a user-context column. See @user-context-calculated-columns.

## Calculated table column

A calculated table column is a column of a calculated table. The table's DAX expression defines which columns exist, their data types and their values, and you add or remove columns by changing that expression.

Tabular Editor 3 analyzes the expression as soon as you change it and adds, removes and updates the columns to match. This works without a connection to a server, so the columns are also up to date in a model that you edit offline. Tabular Editor 2 only updates the columns when you save the model to a database you're connected to, by reloading the table's columns from the server after the save. When you edit a model file in Tabular Editor 2, the columns stay as they are, you can add one with **Create New > Calculated Table Column** and you can't delete them.

You can change the column's display properties, such as `FormatString`, `IsHidden` and `SortByColumn`. To rename the column, first set `IsNameInferred` to `false`. The column has the properties under [Properties of all columns](#properties-of-all-columns) and the ones below.

### Source Column
`SourceColumn` · string · Basic · read-only

The name of the column in the result of the calculated table's expression that this column gets its values from. Tabular Editor 3 sets it when it analyzes the expression, and the engine sets it when the model is saved to a server. Renaming the column leaves it unchanged, which keeps the link between the column and the expression.

The value has one of two formats:

- `Table[Column]`, without quotes around the table name, for a column that the expression takes from another table, for example `Date[Year]` for `SUMMARIZE ( 'Date', 'Date'[Year] )`
- `[Column]` for a column that the expression creates, for example `[Sales Amount]` for `ADDCOLUMNS ( ..., "Sales Amount", ... )`, or `[Value]` for a table constructor or `UNION`

### Name Inferred
`IsNameInferred` · bool · Options

Whether the column's name follows the name in the calculated table's expression. When it's `true`, the engine and Tabular Editor 3 rename the column to match the expression, for example when the expression changes. Set it to `false` to keep a name that you gave the column yourself.

In Tabular Editor 3, `Name` is read-only while `IsNameInferred` is `true`. When you set it back to `true`, the column gets the name of the column that the expression takes it from, if there is one.

A C# script that creates a field parameter, for example, sets `IsNameInferred` to `false` on its columns to keep the names it gives them. See @create-field-parameter.

## Alternate Of

An Alternate Of object sits on a column of an aggregation table. It maps that column to a column, or to the whole table, of the detail table that it summarizes, and sets how the values were aggregated. With these mappings in place, the engine answers a query from the aggregation table when it can and skips the detail table, which is usually much larger and often in DirectQuery mode. This setup is called *user-defined aggregations*. For a walkthrough, see @user-defined-aggregations.

Alternate Of needs compatibility level 1460 or higher. It doesn't appear as a separate object in the **TOM Explorer**. To set the properties below, expand the column's `AlternateOf` property in the **Properties view**.

### Common properties

- [Annotations](xref:object-properties-common#annotations)
- [Object Type](xref:object-properties-common#object-type)

### Base Column
`BaseColumn` · Column · Options

The column in the detail table that this column aggregates. For example, the `Sales Amount` column of a `Sales Agg` table has base column `Sales[Sales Amount]` with summarization `Sum`.

Set either `BaseColumn` or `BaseTable`. Setting `BaseColumn` clears `BaseTable`.

### Base Table
`BaseTable` · Table · Options

The detail table whose rows this column counts. Use it with `Summarization` `Count` for a column that holds the number of detail rows, which lets the engine answer `COUNTROWS ( Sales )` from the aggregation table.

Set either `BaseColumn` or `BaseTable`. Setting `BaseTable` clears `BaseColumn` and sets `Summarization` to `Count`, and changing `Summarization` to any other value clears `BaseTable`. The **Properties view** only shows `BaseTable` when `Summarization` is `Count`.

### Column
`Column` · Column · Options · read-only

The column of the aggregation table that this Alternate Of belongs to. The **Properties view** hides it, and you can use it in C# scripts.

### Summarization
`Summarization` · SummarizationType · Options

How the values in this column were aggregated from the base column or base table.

| Value | Meaning |
|---|---|
| `GroupBy` | A group-by column that holds the same values as the base column. Required when the aggregation table isn't related to the dimension tables, for example when the detail table is a wide, flat table. |
| `Sum` | The sum of the base column. |
| `Count` | The number of rows of the base table, or the number of non-blank values of the base column. |
| `Min` | The smallest value of the base column. |
| `Max` | The largest value of the base column. |

For all summarizations except `Count`, the column must have the same data type as its base column, so a `Sum` of a `Decimal` base column is also `Decimal`. A `Count` column must be a whole number (`Int64`), whatever the data type of the base column. To let the engine answer `DISTINCTCOUNT` from the aggregation table, add the column with `GroupBy`, which also works when the aggregation table is related to the dimension tables. No distinct count summarization exists.

## Variation

A variation is something else that a client tool shows when a user picks a column. Power BI uses variations for auto date/time: for each date column, Power BI Desktop creates a hidden date table, a relationship to it and a variation on the date column. When a report author picks the date column, Power BI shows the **Date Hierarchy** of the hidden date table.

Variations mostly occur in Power BI and Fabric models. Tabular Editor shows the `Variations` property of a column at compatibility level 1400 or higher, in Analysis Services models too. If your model has its own date table, turn off auto date/time in Power BI Desktop to remove the hidden date tables and their variations. See @kb.bpa-remove-auto-date-table.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Object Type](xref:object-properties-common#object-type)

### Parent Column
`Column` · Column · Basic · read-only

The column this variation belongs to.

### Default Column
`DefaultColumn` · Column · Options

A column of the related table that the client tool shows when a user picks the parent column. Set either this or `DefaultHierarchy`. The variations that Power BI Desktop creates for auto date/time use `DefaultHierarchy` and leave `DefaultColumn` empty.

<!-- TODO (not verifiable from TE3 source): confirm whether Default Column and Default Hierarchy are mutually exclusive, and when Power BI uses Default Column. TE3 doesn't enforce either rule. -->

### Default Hierarchy
`DefaultHierarchy` · Hierarchy · Options

A hierarchy of the related table that the client tool shows when a user picks the parent column. For auto date/time, this is the **Date Hierarchy** of the hidden `LocalDateTable_...` table.

### Default
`IsDefault` · bool · Options

Whether this is the default variation of the column. When a column has more than one variation, the client tool shows the default one when a user picks the column.

### Relationship
`Relationship` · Relationship · Options

The relationship from the parent column to the table that holds the default column or default hierarchy. For auto date/time, it's the relationship from the date column to its hidden date table.
