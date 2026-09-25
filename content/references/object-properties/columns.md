---
uid: object-properties-columns
title: Column properties
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
# Column properties

<!--
SUMMARY: Reference for the properties of data columns, calculated columns, calculated table columns, and the Alternate Of and Variation objects that belong to columns.
-->

This page covers the properties of the three kinds of columns, and of the two objects that can belong to a column: **Alternate Of** and **Variation**. For properties that most objects share, see @object-properties-common.

A table can contain three kinds of columns:

- A **data column** gets its values from the table's partitions, for example from a Power Query (M) query or a SQL query.
- A **calculated column** gets its values from a DAX expression that's evaluated for each row of the table.
- A **calculated table column** is a column of a calculated table. The calculated table's DAX expression defines the column, so you can't add or remove these columns yourself.

The three kinds share most of their properties. Those are described once, under [Properties of all columns](#properties-of-all-columns). The sections after it only list the properties that are specific to one kind of column.

## Properties of all columns

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

### Basic

#### Data Type
`DataType` · DataType

The data type of the values in the column. The data type decides how the engine stores the values, which DAX functions and operators you can use on them, and which relationships the column can take part in: both columns of a relationship must have the same data type.

| Value | Meaning |
|---|---|
| `String` | Text. Called *Text* in Power BI. |
| `Int64` | A 64-bit whole number. Called *Whole number* in Power BI. |
| `Double` | A 64-bit floating-point number. Called *Decimal number* in Power BI. Can show small rounding differences, for example in totals. |
| `Decimal` | A fixed-point number with four decimal places. Called *Fixed decimal number* in Power BI. Use it for currency amounts, where rounding differences aren't acceptable. |
| `DateTime` | A date and time. Power BI shows it as *Date*, *Time* or *Date/time*, depending on the format string. |
| `Boolean` | `TRUE` or `FALSE`. |
| `Binary` | Binary data, such as the bytes of an image. You can't use binary values in DAX, and Power BI doesn't load binary columns. |
| `Automatic` | For internal use only. Don't pick it for a column. |
| `Unknown` | The initial value of a new column. The engine replaces it with the actual data type when the column is saved to the server. |
| `Variant` | The value can be of different types. Only used for measures, not for columns. |

The Properties view shows some values with a longer name, for example `Int64` as *Integer / Whole Number (int64)* and `Decimal` as *Currency / Fixed Decimal Number (decimal)*. The dropdown lists all the values above, including `Automatic`, `Unknown` and `Variant`, and Tabular Editor doesn't stop you from picking them. For a data column, only pick one of the first seven values.

For a data column, the data type must match the data that the partition query returns, or the engine converts the values during refresh. A conversion that fails, for example text that isn't a number, makes the refresh fail. For calculated columns and calculated table columns, the data type follows from the expression. Tabular Editor 3 works it out itself while you edit the expression, without a connection to a server. See **Data Type Inferred** below.

In Tabular Editor 3, **Data Type** is read-only on calculated columns and calculated table columns as long as **Data Type Inferred** is `true`. To pick a data type yourself, set **Data Type Inferred** to `false` first.

Changing the data type of a data column in Tabular Editor doesn't change the partition query. If you change a column from `String` to `Int64`, also make sure the query returns whole numbers, for example by changing the type in Power Query.

The Best Practice Analyzer rule @kb.bpa-relationship-same-datatype flags relationships between columns that have different data types.

#### Format String
`FormatString` · string

How client tools display the column's values, for example `#,0` for a whole number with a thousands separator, `0.00%` for a percentage or `yyyy-mm-dd` for a date. The format only affects display: DAX and tools that request unformatted values still get the raw value.

The format string uses the same syntax as the DAX `FORMAT` function. It also applies to the implicit measures that Power BI creates when a report author drags a numeric column into a visual.

Visible numeric and date columns without a format string show raw values such as `1234567.891` or a date with a time part. See @kb.bpa-format-string-columns.

#### Sort By Column
`SortByColumn` · Column

Another column in the same table that decides the order of this column's values. The classic example is a `Month Name` column sorted by a `Month Number` column, so that months appear as January, February, March instead of alphabetically.

Every value of this column must have exactly one value in the sort column. For example, `January` must always have month number `1`. If one value has more than one sort value, the engine reports an error when the column is refreshed or recalculated.

> [!NOTE]
> When a report groups by a column that has a sort column, Power BI also groups by the sort column. This affects DAX: `CALCULATE ( [Sales], REMOVEFILTERS ( 'Date'[Month Name] ) )` doesn't remove the filter on `'Date'[Month Number]`, so the result doesn't change. Remove the filter on both columns, or on the whole table, instead.

The C# script @script-create-date-table creates a date table and sets **Sort By Column** on its name columns for you.

#### Summarize By
`SummarizeBy` · AggregateFunction

The aggregation that client tools use when a report author drags the column into a visual as a value, without using a measure. Power BI calls this *default summarization*, and the measure it creates on the fly an *implicit measure*.

| Value | Meaning |
|---|---|
| `Default` | Let the client tool decide. Numeric columns are summed, other columns aren't summarized. |
| `None` | Don't summarize. Power BI shows the column's values instead, as *Don't summarize*. |
| `Sum` | The sum of the values. |
| `Min` | The smallest value. |
| `Max` | The largest value. |
| `Count` | The number of values. |
| `Average` | The average of the values. |
| `DistinctCount` | The number of distinct values. |

In Power BI Desktop, a numeric column with `Default` behaves like `Sum`: it shows with the Σ icon in the **Data** pane and is added to a visual as *Sum of* the column. A text column with `Default` isn't summarized. Excel doesn't use this property: a PivotTable only aggregates through measures.

Set this to `None` for numeric columns that shouldn't be added up, such as keys, years, phone numbers or unit prices. Otherwise report authors get meaningless totals, like the sum of all customer IDs. See @kb.bpa-do-not-summarize-numeric.

**Summarize By** doesn't affect DAX or explicit measures. When **Discourage Implicit Measures** is enabled on the model (see @object-properties-model), Power BI doesn't create implicit measures at all, so this property has no effect there. To give report authors explicit measures instead, the C# script @script-create-sum-measures-from-columns creates a `SUM` measure for each selected column and hides the column.

### Options

#### Alignment
`Alignment` · Alignment

The horizontal alignment of the column's values in client tools that support it.

| Value | Meaning |
|---|---|
| `Default` | Let the client tool decide. Most tools align numbers to the right and text to the left. |
| `Left` | Align to the left. |
| `Right` | Align to the right. |
| `Center` | Center the values. |

Power BI ignores this property. In table and matrix visuals, text is always left-aligned and numbers right-aligned, whatever **Alignment** says. To align values in a Power BI report, use the formatting options of the visual.

Excel ignores it too: in an Excel PivotTable connected to the model, right- and center-aligned columns show with the default alignment.

#### Alternate Of
`AlternateOf` · AlternateOf

Turns this column into part of a user-defined aggregation. An aggregation table holds pre-aggregated data, for example sales per customer and product. **Alternate Of** tells the engine which column of the detail table this column can stand in for, and how it was aggregated. The engine then answers queries from the smaller aggregation table when it can, instead of querying the detail table.

A column has no Alternate Of until you add one. In Tabular Editor 3, click the **...** button of the empty **Alternate Of** property, or right-click the property and choose **Add Alternate Of**. The new Alternate Of has **Summarization** `Sum`. Then expand **Alternate Of** to set its properties, which are described under [Alternate Of](#alternate-of-1) below. To remove it, right-click the property and choose **Remove Alternate Of**. The property only appears at compatibility level 1460 or higher. For a walkthrough, see @user-defined-aggregations. Tabular Editor 2 works the same way: click the **...** button of the empty **Alternate Of** property, or right-click the property and choose **Add Alternate Of** or **Remove Alternate Of**.

The C# script @script-implement-user-defined-aggregations sets up the detail table for a selected aggregation table and configures **Alternate Of** on its numeric columns.

#### Data Category
`DataCategory` · string

Tells client tools what kind of value the column holds, so they can treat it in a special way. For example, Power BI puts a column with category `City` on a map, shows a column with category `ImageUrl` as an image, and shows a column with category `WebUrl` as a clickable link. Leave it empty for a regular column.

The value is a string. In Tabular Editor 3, the dropdown lists all the categories that the protocol defines, in alphabetical order, but you can also type any other value. Tabular Editor doesn't check it, so spell it exactly as listed. The categories that Power BI uses are:

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
| `Barcode` | Barcode | Barcodes that the Power BI mobile app can scan to filter a report. |

Geographic categories help map visuals find the right location. For example, `Paris` is more likely to be placed in France when the column has category `City` and the report also uses a `Country` column.

The dropdown spells two of them differently, as `WebURL` and `ImageURL`, and has no `Barcode` entry. That doesn't matter: Power BI ignores case, so `ImageUrl` and `ImageURL` both show the value as an image in a table visual, and `WebUrl` and `WebURL` both show it as a link. TOM stores the value exactly as you type it. Power BI accepts `Barcode`, but a table visual shows the value as plain text; it's used by the Power BI mobile apps.

The protocol defines many more categories, for example `Id`, `Image` and time categories such as `Years` and `Months`, which older tools used. Power BI ignores most of them. The dropdown also lists `PaddedDateTableDates`, a category that Power BI uses but the protocol doesn't define. Power BI Desktop still writes the time categories on the columns of its auto date/time tables: `PaddedDateTableDates` on the date column, and `Years`, `Quarters`, `QuarterOfYear`, `Months`, `MonthOfYear` and `DayOfMonth` on the other columns.

<!-- TODO (not verifiable from TE3 source): whether Power BI uses these column categories for anything, or only writes them. -->

To mark a table as a date table, don't use a column category. Set **Data Category** on the table to `Time` (see @object-properties-tables) and set **Key** to `true` on the table's date column.

#### Display Ordinal
`DisplayOrdinal` · int

A number that client tools can use to order the columns of a table, for example `10`, `20`, `30`. The numbers only need to be in the right relative order, so leave gaps to make it easy to insert a column later.

Power BI doesn't use it: the **Data** pane in Power BI Desktop always lists columns alphabetically, whatever their **Display Ordinal**. Use display folders to group columns instead.

#### Encoding Hint
`EncodingHint` · EncodingHintType · compatibility level 1400+

A hint to the engine about how to compress a numeric column in memory. The engine normally picks an encoding itself when it first loads data, and it may later have to re-encode the column during refresh, which takes time. A hint lets it start with the right encoding.

| Value | Meaning |
|---|---|
| `Default` | Let the engine decide. |
| `Hash` | Store each distinct value once, in a dictionary, and refer to it by its position. Works well for columns with few distinct values, or with values that are spread far apart, such as key columns. |
| `Value` | Store the values themselves, with a little arithmetic to make them smaller. Works well for numeric columns that you aggregate and whose values are close together, such as quantities or amounts. |

It's only a hint: the engine can still choose a different encoding. Text columns always use hash encoding. Only set this when you've seen, for example in VertiPaq Analyzer, that the engine picks an encoding that makes refresh slow or the model large.

#### Group By Columns
`GroupByColumns` · GroupingColumnCollection · read-only

Other columns in the same table that the engine also groups by whenever this column is used in a query. This keeps rows apart that have the same value in this column but a different value in the group-by column.

Power BI uses this for field parameters. The column that shows the field names is grouped by the column that holds the field references, so each field stays a separate row even if two fields have the same display name. See @create-field-parameter.

Because MDX clients such as Excel treat these columns as a composite key, you can't put a column with group-by columns in a PivotTable without the columns it's grouped by.

The property only appears for Power BI and Fabric models, at compatibility level 1400 or higher. The property itself is read-only, but you can change the columns in it: in Tabular Editor 3, click the **...** button to open a dialog that lists the other columns of the table, and select the columns to group by. In TOM, the columns are saved in the column's `RelatedColumnDetails` object. When you remove the last column, Tabular Editor removes that object too.

#### Available In MDX
`IsAvailableInMDX` · bool

Whether the engine builds an *attribute hierarchy* for the column, which MDX queries need. The default is `true`. Excel PivotTables use MDX, so they can only put a column on rows or columns when it's `true`. Power BI uses DAX and doesn't need attribute hierarchies.

Setting it to `false` on hidden columns that nobody uses in MDX, such as foreign keys and columns only used in measures, saves memory and refresh time. Keep it `true` for columns that are used in hierarchies, as a sort column, in variations or in calendars, and for columns that Excel users need. See @kb.bpa-set-isavailableinmdx-false and @kb.bpa-set-isavailableinmdx-true-necessary. The rule @kb.bpa-hide-foreign-keys also flags foreign key columns that aren't hidden.

#### Data Type Inferred
`IsDataTypeInferred` · bool

Whether the engine works out the data type of the column itself, instead of using the value of **Data Type**. This mostly matters for calculated columns and calculated table columns, where the data type follows from the DAX expression.

In Tabular Editor 3, while this is `true` on a calculated column or calculated table column, **Data Type** is read-only and Tabular Editor updates it from the expression. Set it to `false` to pick a data type yourself. When you set it back to `true` on a calculated table column, Tabular Editor resets **Data Type** to the data type of the column the expression gets its values from.

<!-- TODO (not verifiable from TE3 source): document the effect of this property on data columns. TE3 has no special handling for data columns. -->

#### Default Image
`IsDefaultImage` · bool

Marks the column as the image that represents a row of the table, for example a product photo. It's part of the *table behavior* settings that Power View used. No current client uses it: Power View has been retired, Power BI doesn't use it, and Excel PivotTables ignore table behavior settings.

#### Default Label
`IsDefaultLabel` · bool

Marks the column as the label that identifies a row of the table to users, for example the product name. Like **Default Image**, it's a *table behavior* setting that Power View used. No current client uses it: Power View and Power BI Q&A, which could use it, have both been retired.

#### Key
`IsKey` · bool

Marks the column as the key of the table: a column whose values identify each row. A table can have only one key column: when you set **Key** to `true` on a column, Tabular Editor sets it to `false` on the other columns of the table. Tabular Editor doesn't change **Unique** or **Nullable** when you set **Key**. The key column can't contain duplicate or blank values, so a refresh that loads duplicates fails.

In Power BI, you set this on the date column when you mark a table as a date table. The table's **Data Category** is then `Time`.

The Best Practice Analyzer rule @kb.bpa-date-table-exists flags a model that has no calendar, no table with **Data Category** `Time` and no `DateTime` key column.

#### Nullable
`IsNullable` · bool

Whether the column can contain blank (null) values. The default is `true`. Set it to `false` to make a refresh fail when the source returns a blank value, as a data quality check. A key column never allows blanks, whatever the value of this property.

#### Unique
`IsUnique` · bool

Whether the column contains only unique values. The engine enforces it. When the column contains a duplicate value, a refresh of a data column fails. For a column of a calculated table, the save itself fails, because the engine recalculates the table right away. The error looks like *Column 'Key' in Table 'Sales' contains a duplicate value 'a' and this is not allowed for columns on the one side of a many-to-one relationship or for columns that are used as the primary key of a table*. Only set it on columns that are guaranteed to be unique, such as the key of a dimension table.

To see the distinct values of a column in a connected model, run the C# script @script-display-unique-column-values.

#### Keep Unique Rows
`KeepUniqueRows` · bool

Another *table behavior* setting from Power View. It's meant to keep rows that share the same value in this column separate when they have different keys, for example two customers with the same name. When it's `false`, those rows are grouped by value.

No current client acts on it. Power BI doesn't use it, and in an Excel PivotTable on SQL Server 2025 Analysis Services, two customers with the same name still show as one row whether **Keep Unique Rows** is `true` or `false`. To show them separately, make the values unique, for example by adding the customer number to the name.

#### Source Provider Type
`SourceProviderType` · string

The column's data type in the data source, in the source's own terms, for example `nvarchar` or `WChar`. The engine can use it to generate queries against the source in DirectQuery mode. Tabular Editor 3 never fills it in, not even when it imports a table, so it's only set when you or another tool set it. Most models, and most Power BI models, leave it empty.

<!-- TODO (not verifiable from TE3 source): confirm which other tools fill in Source Provider Type (for example the Visual Studio table import wizard) and in which format (OLE DB type names or SQL type names). -->

#### String Indexing Behavior
`StringIndexingBehavior` · IndexingBehavior · compatibility level 1706+

Whether the engine builds an index on a text column, and whether it saves that index so it doesn't have to build it again after a restart.

| Value | Meaning |
|---|---|
| `Off` | Don't build an index. |
| `Auto` | The default. Build the index when needed, but don't save it. |
| `Explicit` | Build and save the index only when you run a refresh of type `RefreshIndex`. |
| `Full` | Build and save the index during a full refresh, a recalculation or a `RefreshIndex` refresh. |

Support is still limited. In Power BI Desktop, whose engine supports compatibility level 1706, the engine accepts `Off` and `Auto`, but rejects `Explicit` and `Full` with the error *Persist String Index feature is disabled*. Recent versions of the TOM library only allow values other than `Auto` from compatibility level 1707.

<!-- TODO (not verifiable from TE3 source): document what the string index is used for (text search such as CONTAINSSTRING?) and when Explicit and Full become available. TOM also has a separate FullTextIndexingBehavior property (for TEXTCONTAINS and TEXTSIMILARITY), which TE3 currently hides in the Properties view. -->

#### Table Detail Position
`TableDetailPosition` · int

Adds the column to the table's *default field set*: the columns a client tool shows when a user adds the whole table to a report or drills through to details. A positive number includes the column, and columns are shown in ascending order of this number. Power View and Excel's **Show Details** used the default field set.

For a more flexible way to control drill-through in Excel, use **Default Detail Rows Expression** on the table (see @object-properties-tables) or **Detail Rows Expression** on a measure (see @object-properties-measures).

The default is `-1`, which leaves the column out of the default field set.

Excel no longer uses it for drill-through. **Show Details** in an Excel PivotTable returns the table's columns whatever **Table Detail Position** says. To choose the columns, set a detail rows expression.

#### Variations
`Variations` · VariationCollection · read-only

The variations of this column. A variation lets a client tool show something else when a user picks this column. Power BI uses variations for *auto date/time*: when a report author picks a date column, Power BI shows the date hierarchy of a hidden date table instead. See [Variation](#variation) below.

### Translations, Perspectives, Security

#### Object Level Security
`ObjectLevelSecurity` · ColumnOLSIndexer · read-only · *shortcut to* the column permissions of each role

The object-level security (OLS) setting of this column in each role of the model. The property only appears at compatibility level 1400 or higher, and only when the model has at least one role. Expand the property to see one entry per role, with these values:

| Value | Meaning |
|---|---|
| `Default` | No column-specific setting. The column follows the setting of its table in the role. In TOM, the role has no column permission for the column. |
| `None` | Users in the role can't see or query the column. For them, it's as if the column doesn't exist, so visuals that use it show an error. |
| `Read` | Users in the role can see and query the column. |

The property itself is read-only, but you can change the value for each role. When you pick `None` or `Read`, Tabular Editor adds a column permission to the role's table permission for the column's table, and creates that table permission if the role doesn't have one yet. When you pick `Default`, it removes the column permission. You can also set the same values on the role, under **OLS Column Permissions** (see @object-properties-security). See @data-security-setup-ols.

You can't combine row-level security from one role with object-level security from another. When a user is a member of such a combination of roles, the engine returns an error at query time.

How the settings combine, as observed on SQL Server 2025 Analysis Services:

- `Default` follows the table: when the role's table permission is `Read`, the column is visible, and when it's `None`, the whole table is hidden, including this column.
- A column can't be less restrictive than its table. The engine rejects `Read` on a column whose table is `None`.
- When a user is a member of several roles that all use OLS, the permissions add up: the user can see a table or column if any of the roles allows it.
- Row-level and object-level security in the *same* role work together. For example, a row filter on a table that the role hides with OLS still filters the related tables.

## Data column

A data column gets its values from the table's partitions. In a Power BI model, that's usually a Power Query (M) query. The column has all the properties under [Properties of all columns](#properties-of-all-columns), plus this one.

In Tabular Editor 3, the @import-tables wizard creates data columns with their data types and source column mappings, and **Update table schema** updates them when the source changes.

### Basic

#### Source Column
`SourceColumn` · string

The name of the column, in the result of the partition query, that this column gets its values from. It must match the name that the query returns. When it doesn't, for example after someone renamed a column in Power Query, the refresh fails.

Because the column's **Name** and its **Source Column** are separate, you can rename a column in the model without changing the query, and the other way round. Tabular Editor doesn't change **Source Column** when you rename a column. With formula fix-up turned on, it does update the DAX expressions that refer to the renamed column. See @formula-fix-up-dependencies.

Every data column needs a source column. See @kb.bpa-data-column-source.

When a column is renamed in the source, **Update table schema** in Tabular Editor 3 reports a removed and a new column. You can combine the two into a single **Source Column** update, so the DAX formulas that use the column keep working.

## Calculated column

A calculated column gets its values from a DAX expression that's evaluated once for each row of the table, when the table is refreshed. The result is stored like the values of a data column, so it takes memory, but reading it is fast. Use a calculated column when you need the value to slice, filter or group by. For values that you only aggregate, a measure is usually a better choice.

The column has all the properties under [Properties of all columns](#properties-of-all-columns), plus these. To add a calculated column in Tabular Editor 3, see @creating-and-testing-dax.

### Options

#### Expression
`Expression` · string

The DAX expression that calculates the value for each row, for example:

```dax
Sales[Quantity] * Sales[Unit Price]
```

The expression is evaluated in a *row context*, so you can refer to the columns of the current row directly. To get a value from a related table, use `RELATED`, for example `RELATED ( Product[Category] )`.

The engine recalculates the column when the table is refreshed, or when you change the expression and save the model to a connected server. In Tabular Editor 3, you edit the expression in the Expression Editor of the @dax-editor, which offers syntax highlighting and code assist. The @table-preview shows the calculated values, or *(Calculation needed)* when the column must be recalculated first.

#### Expression Context
`ExpressionContext` · ExpressionContext · compatibility level 1705+

Whether the column is evaluated once for everyone, or per user.

| Value | Meaning |
|---|---|
| `Standard` | The default. The column is calculated during refresh and has one value per row for all users. |
| `UserContext` | The column is evaluated per user, so the expression can call functions such as `USERPRINCIPALNAME`. |

A user-context column can't be used by a standard calculated column, a calculated table, a row-level security filter or a relationship. See @user-context-calculated-columns.

## Calculated table column

A calculated table column is a column of a calculated table. The table's DAX expression decides which columns exist, what their data types are and which values they hold. You can't add or delete these columns yourself: change the table's expression instead. Tabular Editor 3 analyzes the DAX expression itself as soon as you change it, and adds, removes and updates the columns to match. This works without a connection to a server, so the columns are also up to date in a model that you edit offline. Tabular Editor 2 doesn't analyze the expression. It only updates the columns when you save the model to a database you're connected to: after the save, it reloads the table's columns from the server. When you edit a model file, the columns stay as they are, and you can add one yourself with **Create New > Calculated Table Column**. Tabular Editor 2 doesn't let you delete calculated table columns either.

You can still change the column's display properties, such as **Format String**, **Hidden** and **Sort By Column**. To rename the column, first set **Name Inferred** to `false`. The column has all the properties under [Properties of all columns](#properties-of-all-columns), plus these.

### Basic

#### Source Column
`SourceColumn` · string · read-only

The name of the column in the result of the calculated table's expression that this column gets its values from. Tabular Editor 3 sets it when it analyzes the expression, and the engine sets it when the model is saved to a server. It stays the same when you rename the column, so the link between the column and the expression survives a rename.

The value has one of two formats:

- `Table[Column]`, without quotes around the table name, for a column that the expression takes from another table, for example `Date[Year]` for `SUMMARIZE ( 'Date', 'Date'[Year] )`.
- `[Column]` for a column that the expression creates, for example `[Sales Amount]` for `ADDCOLUMNS ( ..., "Sales Amount", ... )`, or `[Value]` for a table constructor or `UNION`.

### Options

#### Name Inferred
`IsNameInferred` · bool

Whether the column's name follows the name in the calculated table's expression. When it's `true`, the engine and Tabular Editor 3 rename the column to match the expression, for example when the expression changes. Set it to `false` to keep a name that you gave the column yourself.

In Tabular Editor 3, **Name** is read-only while **Name Inferred** is `true`, so you set it to `false` before you rename the column. When you set it back to `true`, Tabular Editor gives the column the name of the column the expression takes it from, if there is one.

For example, a C# script that creates a field parameter sets **Name Inferred** to `false` on its columns, so the friendly names it gives them stick. See @create-field-parameter.

## Alternate Of

An Alternate Of object sits on a column of an aggregation table. It maps that column to a column, or to the whole table, of the detail table that it summarizes, and says how the values were aggregated. With these mappings in place, the engine can answer a query from the aggregation table instead of from the (usually much larger, often DirectQuery) detail table. This is known as *user-defined aggregations*. For a walkthrough, see @user-defined-aggregations.

Alternate Of needs compatibility level 1460 or higher. It isn't a separate object in the TOM Explorer: you set it through the **Alternate Of** property of the column, which you expand in the Properties view to see the properties below.

### Common properties

- [Annotations](xref:object-properties-common#annotations)

### Options

#### Base Column
`BaseColumn` · Column

The column in the detail table that this column is an aggregate of. For example, the `Sales Amount` column of a `Sales Agg` table has base column `Sales[Sales Amount]` with summarization `Sum`.

Set either **Base Column** or **Base Table**, not both. When you set **Base Column**, Tabular Editor clears **Base Table**.

#### Base Table
`BaseTable` · Table

The detail table whose rows this column counts. Use it with **Summarization** `Count` for a column that holds the number of detail rows, so that the engine can answer `COUNTROWS ( Sales )` from the aggregation table.

Set either **Base Column** or **Base Table**, not both. The Properties view only shows **Base Table** when **Summarization** is `Count`. When you set **Base Table**, Tabular Editor clears **Base Column** and sets **Summarization** to `Count`. When you change **Summarization** to anything other than `Count`, it clears **Base Table**.

#### Column
`Column` · Column · read-only

The column of the aggregation table that this Alternate Of belongs to. The Properties view doesn't show it, because you always reach the Alternate Of from its column. You can use it in C# scripts.

#### Summarization
`Summarization` · SummarizationType

How the values in this column were aggregated from the base column or base table.

| Value | Meaning |
|---|---|
| `GroupBy` | The column is a group-by column that holds the same values as the base column. Needed when the aggregation table isn't related to the dimension tables, for example when the detail table is a wide, flat table. |
| `Sum` | The column holds the sum of the base column. |
| `Count` | The column holds the number of rows of the base table, or the number of non-blank values of the base column. |
| `Min` | The column holds the smallest value of the base column. |
| `Max` | The column holds the largest value of the base column. |

For all summarizations except `Count`, the column must have the same data type as its base column. For example, a `Sum` of a `Decimal` base column must also be `Decimal`. A `Count` column must be a whole number (`Int64`), whatever the data type of the base column. There's no distinct count summarization: to let the engine answer `DISTINCTCOUNT` from the aggregation table, add the column with `GroupBy` instead. That also works when the aggregation table is related to the dimension tables, where `GroupBy` is otherwise optional.

## Variation

A variation is an alternative that a client tool can show when a user picks a column. Power BI uses variations for *auto date/time*: for each date column, Power BI Desktop creates a hidden date table, a relationship to it and a variation on the date column. When a report author then picks the date column, Power BI shows the *Date Hierarchy* of the hidden date table instead of the column itself.

Variations are mostly found in Power BI and Fabric models. Tabular Editor shows the **Variations** property of a column at compatibility level 1400 or higher, in Analysis Services models too. You rarely create variations yourself. If your model has a proper date table, consider turning off auto date/time in Power BI Desktop to remove the hidden date tables and their variations. See @kb.bpa-remove-auto-date-table.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Object Type](xref:object-properties-common#object-type)

### Basic

#### Parent Column
`Column` · Column · read-only

The column this variation belongs to.

### Options

#### Default Column
`DefaultColumn` · Column

A column of the related table that the client tool shows instead of the parent column. Set either this or **Default Hierarchy**. The variations that Power BI Desktop creates for auto date/time use **Default Hierarchy** and leave **Default Column** empty.

<!-- TODO (not verifiable from TE3 source): confirm whether Default Column and Default Hierarchy are mutually exclusive, and when Power BI uses Default Column. TE3 doesn't enforce either rule. -->

#### Default Hierarchy
`DefaultHierarchy` · Hierarchy

A hierarchy of the related table that the client tool shows instead of the parent column. For auto date/time, this is the *Date Hierarchy* of the hidden `LocalDateTable_...` table.

#### Default
`IsDefault` · bool

Whether this is the default variation of the column. A column can have more than one variation. The default one is what the client tool shows when a user picks the column.

#### Relationship
`Relationship` · Relationship

The relationship from the parent column to the table that holds the default column or default hierarchy. For auto date/time, it's the relationship from the date column to its hidden date table.
