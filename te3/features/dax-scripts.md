---
uid: dax-scripts
title: DAX Scripts
author: Daniel Otykier
updated: 2021-09-08
applies_to:
  editions:
    - edition: Desktop
    - edition: Business
    - edition: Enterprise
---
# DAX Scripts

**DAX Script** allow you to view and edit DAX expressions and basic properties for multiple objects, in a single document. This is useful, for example, when complex business logic is spread out across multiple measures.

You can script the DAX code for any TOM explorer object that has DAX expressions.

To use this feature, locate the objects for which you would like to generate a single document, in the TOM Explorer. Multi-select the objects, then right-click and choose **Script DAX**. A new document is created, containing the DAX expressions and basic properties of all the selected objects. You can also generate a DAX script for all objects within a table or all objects within the model, by choosing the table or model object respectively.

![Dax Script](~/images/dax-script.png)

Editing objects through a DAX script is slightly different than editing through the **Expression Editor**. With the latter, changes are applied immediately when you navigate to a different object. In a DAX script, however, changes are not applied until you explicitly do so by using the **Script > Apply** (F5) option. If you are connected to an instance of Analysis Services, you can use the **Script > Apply & Sync** (SHIFT+F5) option to simultaneously apply the changes and save the updated model metadata to Analysis Services.

You can undo/redo changes made by a DAX script using the usual keyboard shortcuts (Ctrl+Z / Ctrl+Y).

### Multiple DAX scripts

You can create as many DAX scripts as you want, if you prefer to have multiple document windows open instead of a single one. This way, you can use the usual IDE features to place the documents side by side, on different monitors, etc. Be aware, that the code within DAX script windows is not updated automatically when changes are made to the object expression/properties in the TOM. So in other words, if you have two or more DAX scripts containing the definition of the same object(s), then the last script to be applied (F5), will always override any changes made through other DAX scripts, or directly through the **Properties View**.

### Working with DAX script files

DAX scripts can be saved as text files, using the `.te3daxs` file extension. To save a DAX script as a file, simply use the **File > Save** (Ctrl+S) option. To open a DAX script from a text file, use the **File > Open > File...** (Ctrl+O) option.

> [!NOTE]
> DAX scripts are not model specific, but since DAX expressions may point to measures, columns and tables defined in the model, there are no guarantees that any DAX script can be applied to any model. DAX scripts are mostly useful for working with several DAX objects within a single document, in the context of a specific data model.

### DAX script editor

The DAX script editor has all the capabilities of the DAX editor used elsewhere in Tabular Editor 3. Specifically, auto-complete, auto-formatting, calltips, etc.

In addition, to easily manage large DAX scripts, two dropdowns are displayed at the top of the DAX script view. The dropdown on the left allows you to jump between objects defined in the script, where as the dropdown on the right allows you to jump between properties on the current object.

![Dax Script Navigation](~/images/dax-script-navigation.png)

### Define measures

If you want to include the definition of a measure that is referenced in the script, but not already defined in the script, you can do so by right-clicking on a measure reference, and choose the "Define Measure" or "Define Measure with dependencies" option.

![Define Measure With Deps](~/images/define-measure-with-deps.png)

### Shortcuts

To apply the script to the model, use the following shortcuts:

- **F5**: Apply the entire script to the local model metadata
- **Shift+F5**: Apply the entire script to the local model metadata, then save the model metadata back to the source
- **F8**: Apply the currently selected part of the script to the local model metadata
- **Shift+F8**: Apply the currently selected part of the script to the local model metadata, then save the model metadata back to the source

### DAX objects supported

Tabular Editor 3 supports editing the following types of objects using a DAX script:

- Measures (including KPIs)
- Calculated columns
- Calculated tables
- Calculation groups (including calculation items)

## DAX script syntax

The syntax for DAX scripts is the following:

```dax
<DAX script>:
MEASURE 'Table name'[Measure name] [= [<DAX expression>]]
    [<Measure properties>]

COLUMN 'Table name'[Column name] [= [<DAX expression>]]
    [<Column properties>]

TABLE 'Table name' [= [<DAX expression>]]
    [<Table properties>]

CALCULATIONGROUP 'Table name'[Column name]
    [<Calculation Group properties>]
    CALCULATIONITEM "Item 1" [= [<DAX expression>]]
        [<Calculation Item properties>]
    CALCULATIONITEM "Item 2" [= [<DAX expression>]]
        [<Calculation Item properties>]
    ...

<Measure properties>:
    DetailRows = [<DAX expression>]
    DisplayFolder = ["string"]
    FormatString = ["string" / <DAX expression>]
    Description = ["string"]
    Visible = TRUE/FALSE
    KpiStatusExpression = [<DAX expression>]
    KpiStatusDescription = ["string"]
    KpiStatusGraphic = ["string"]
    KpiTrendExpression = [<DAX expression>]
    KpiTrendDescription = ["string"]
    KpiTrendGraphic = ["string"]
    KpiTargetExpression = [<DAX expression>]
    KpiTargetDescription = ["string"]
    KpiTargetFormatString = ["string"]

<Column properties>:
    DisplayFolder = ["string"]
    FormatString = ["string"]
    Description = ["string"]
    Visible = TRUE / FALSE
    Datatype = BOOLEAN / DOUBLE / INTEGER / DATETIME / CURRENCY / STRING

<Table properties>:
    Description = ["string"]
    Visible = TRUE / FALSE
    DetailRows = [<DAX expression>]

<Calculation Group properties>:
    Description = ["string"]
    Visible = TRUE / FALSE
    Precedence = <integer value>

<Calculation Item properties>
    Description = ["string"]
    Ordinal = <integer value>
    FormatString = [<DAX expression>]
```

> [!TIP]
> Users of TMDL will undoubtedly have noticed that some similarities exist between the syntax of DAX scripts and the syntax of TMDL. In fact, TMDL was inspired by DAX scripts. However, to keep things simple, DAX scripts intentionally supports only objects that have one or more DAX expressions associated with them. Moreover, the DAX script syntax is designed to be compatible with the `DEFINE` section of a DAX query (provided the DAX script does not specify any object properties). TMDL, on the other hand, is used to define the entire model metadata, and is not limited to DAX objects. However, blocks of TMDL code cannot be readily used in a DAX query as the syntax for defining object names in TMDL, is not valid in DAX.

### Example 1: Measure

As an example, the script below defines the `[Internet Total Sales]` measure on the `'Internet Sales'` table. In addition to the DAX expression of the measure, the script also includes the measure description and format string.

```dax
----------------------------------
-- Measure: [Internet Total Sales]
----------------------------------
MEASURE 'Internet Sales'[Internet Total Sales] = SUM('Internet Sales'[Sales Amount])
    Description = "Returns the sum of all Internet Sales"
    FormatString = "\$#,0.00;(\$#,0.00);\$#,0.00"
```

### Example 2: Measure with status and target KPI

The DAX script below defines the `[Internet Current Quarter Sales Performance]` measure, which includes a KPI that has a status and a target expression. The status KPI uses the "Shapes" graphic.

```dax
--------------------------------------------------------
-- Measure: [Internet Current Quarter Sales Performance]
--------------------------------------------------------
MEASURE 'Internet Sales'[Internet Current Quarter Sales Performance] =
    IFERROR(
        [Internet Current Quarter Sales] / [Internet Previous Quarter Sales Proportion to QTD],
        BLANK()
    )
    , KpiStatusExpression =
        VAR x = [Internet Current Quarter Sales Performance]
        RETURN
            IF(
                ISBLANK( x ),
                BLANK(),
                IF(x < 1, -1, IF(x < 1.07, 0, 1))
            )
    , KpiStatusGraphic = "Shapes"
    , KpiTargetExpression = 1.1
```

### Example 3: Calculation group

The DAX script below defines the `'Time Intelligence'` calculation group with the `[Period]` column. The calculation group contains 6 calculation items that performs various time calculations. Notice how the `"YoY %"` item applies a different format string.

```dax
-----------------------------------------
-- Calculation Group: 'Time Intelligence'
-----------------------------------------
CALCULATIONGROUP 'Time Intelligence'[Period]
    Description = "Use this table to perform time calculations"

    CALCULATIONITEM "Current" = SELECTEDMEASURE()
        Ordinal = 0

    CALCULATIONITEM "MTD" = TOTALMTD(SELECTEDMEASURE(), 'Calendar'[Date])
        Ordinal = 1

    CALCULATIONITEM "YTD" = TOTALYTD(SELECTEDMEASURE(), 'Calendar'[Date])
        Ordinal = 2

    CALCULATIONITEM "PY" = CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Calendar'[Date]))
        Ordinal = 3

    CALCULATIONITEM "YoY" = 
        SELECTEDMEASURE()
         - CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Calendar'[Date]))
        Ordinal = 4

    CALCULATIONITEM "YoY %" = 
        VAR lastYear = 
            CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Calendar'[Date]))
        RETURN
            DIVIDE(
                SELECTEDMEASURE() - lastYear,
                lastYear
            )
        FormatString = "Percent"
        Ordinal = 5
```

## Unspecified or empty expressions / properties

As of Tabular Editor 3.16.0, it is possible to specify empty expressions and property values in DAX scripts, or omit object expressions entirely.

For example, the following script will create a measure with an empty DAX expression, an empty format string and no Display Folder. If the measure already exists, it will be updated to have an empty DAX expression, an empty format string and no Display Folder.

```dax
MEASURE 'Internet Sales'[Internet Total Sales] =
    , Description = "TODO: Ask business how this should be implemented and formatted."
    , FormatString =
    , DisplayFolder =
```

Note that the `,` (comma) before properties following an empty expression is mandatory. Commas are optional when the preceding expression is non-empty.

If you want to keep the existing DAX expression on a measure, you can omit the `=` sign after the object name:

```dax
MEASURE 'Internet Sales'[Internet Total Sales]
    DisplayFolder = "Totals"
```

The example above will update the `[Internet Total Sales]` measure to have the specified `DisplayFolder`, but will keep the existing DAX expression. All other properties on the object, such as `Description` and `FormatString`, will remain unchanged.

These new features make it easier to write scripts that only update specific properties of an object, without having to specify the entire object definition. This way, scripts can more easily be reused across different models.
