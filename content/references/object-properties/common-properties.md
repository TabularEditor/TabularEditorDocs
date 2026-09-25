---
uid: object-properties-common
title: Common properties
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
# Common properties

<!--
SUMMARY: Properties that most objects in a semantic model share, such as Name, Description, Annotations and Lineage Tag.
-->

The properties on this page appear on many object types. They behave the same way on every object that has them, so the object-specific pages link here instead of repeating them. For the other pages, see @object-properties.

## Basic

### Name
`Name` · string

The name of the object. For tables, columns, measures, hierarchies and user-defined functions, the name is also what you use to reference the object in DAX. Names must be unique among siblings: two measures can't share a name, and in most models a measure also can't share a name with any column (see **Force Unique Names** on @object-properties-model).

When you rename an object that DAX expressions refer to, Tabular Editor updates those expressions for you, as long as **Formula Fix-up** is enabled under **Tools > Preferences**. With it disabled, a rename can break the expressions that use the old name. See @formula-fix-up-dependencies.

Some objects have no name of their own, for example a KPI or a calculation group. Their name comes from the object they belong to.

To rename many objects at once, select them in the TOM Explorer and use batch rename, which supports regular expressions. See @duplicate-and-batch. The Best Practice Analyzer rules @kb.bpa-trim-object-names and @kb.bpa-avoid-invalid-characters-names flag names with leading or trailing spaces and names with control characters.

### Description
`Description` · string

Free text that explains what the object is for. Report authors see the description as a tooltip in the **Data** pane of Power BI, so it's the most direct way to document a model for the people who use it. Excel's PivotTable field list doesn't show descriptions. Descriptions are also useful for developers. In Tabular Editor 3, the TOM Explorer has a **Description** column where you can read and edit them, and DAX code assist shows the description of a table, column or measure in its tooltip. When a measure, calculated column or calculated table has no description, the tooltip shows the first lines of its expression instead.

Descriptions can be translated. See **Translated Descriptions** below.

The Best Practice Analyzer rule @kb.bpa-visible-objects-no-description flags visible objects without a description, and @kb.bpa-avoid-invalid-characters-descriptions flags descriptions that contain control characters.

### Display Folder
`DisplayFolder` · string

The folder the object appears in, in the field list of client tools. Use a backslash (`\`) to create subfolders, for example `Sales\Year to date`. Use a semicolon (`;`) to show the same object in more than one folder, for example `Sales;Finance`.

Display folders are only a way of organizing the field list. They don't affect DAX or security. Tabular Editor also uses them to group objects in the TOM Explorer.

To reorganize display folders, drag a folder onto another folder in the TOM Explorer. The objects and subfolders in it move along. See @drag-drop.

### Hidden
`IsHidden` · bool

When `true`, client tools such as Power BI hide the object from report authors. The object is still part of the model and can still be used in DAX, so hidden objects are typically helper columns, key columns and intermediate measures.

Hiding an object isn't a security feature. Anyone who can query the model can still query a hidden object. Use @roles-and-rls to secure data.

The Best Practice Analyzer rule @kb.bpa-hide-foreign-keys flags visible columns on the many side of a relationship. Its automatic fix hides them.

## Metadata

### Annotations
`Annotations` · collection of name/value pairs

Custom name/value pairs stored with the object. Analysis Services and Power BI ignore annotations, so tools use them to store their own information. For example, Power BI Desktop stores layout information in annotations, and many C# scripts and Best Practice Analyzer rules store settings in them.

In a C# script, use `GetAnnotation`, `SetAnnotation` and `RemoveAnnotation`. See @how-to-annotations-extended-properties.

### Extended Properties
`ExtendedProperties` · collection of name/value pairs

Like annotations, but the value can be either a string or a JSON document. Power BI uses extended properties, for example to store query information about parameters. Most models don't need them, so prefer annotations for your own metadata.

In a C# script, use `GetExtendedProperty` and `SetExtendedProperty`.

### Changed Properties
`ChangedPropertiesCollection` · collection

The names of properties that you changed on an object that comes from another source, such as a table in a composite model or an object that Power BI generates. The engine doesn't overwrite properties in this list when it synchronizes the object from its source.

Tabular Editor 3 doesn't add entries to this list for you: when you change such a property, add its name yourself. You can type a comma-separated list of TOM property names, for example `Name,FormatString`. Names that aren't properties of the object, and duplicates, are ignored. You can also expand the property and select the check box next to a property name. The expanded list always includes **Name**, plus the properties already in the list. To empty the list, right-click the property and choose **Clear Changed Properties**.

### DAX identifier
`DaxObjectFullName` · string · *computed* · read-only

The fully qualified name you use to reference the object in DAX, for example `'Sales'[Amount]` for a column or `[Total Sales]` for a measure. Useful in C# scripts that build DAX expressions. See @how-to-work-with-expressions.

### Error Message
`ErrorMessage` · string · read-only

The error the engine reported for the object, for example a syntax error in a DAX expression or a refresh error on a partition. It's empty when the object has no error.

In Tabular Editor 3, errors on DAX expressions are also shown while you type, before the model is saved to the engine. The @messages-view lists all errors and warnings in the model. Double-click a message to jump to the object it's about.

### Object Type
`ObjectTypeName` · string · *computed* · read-only

The kind of object, for example `Measure`, `Calculated Column` or `Table`.

### State
`State` · ObjectState · read-only

Whether the object is ready to be queried. The engine sets it; you can't change it. The values are:

| Value | Meaning |
|---|---|
| `Ready` | The object is valid and, where it holds data, the data is up to date. |
| `NoData` | The object is valid but holds no data yet. Refresh the table or partition. |
| `CalculationNeeded` | The object is valid but must be recalculated, for example a calculated column after a change to its expression. |
| `SemanticError` | The expression refers to something that doesn't exist or is invalid. See **Error Message**. |
| `EvaluationError` | The expression is valid but failed when it was evaluated. |
| `DependencyError` | An object this one depends on is in an error state. |
| `Incomplete` | Some of the object's data is missing, for example when a partition failed to refresh. |
| `ForceCalculationNeeded` | The object must be recalculated even though it seems up to date. |

A model that you open from a file isn't connected to an engine, so **State** has no meaningful value there. It's most useful when you're connected to a server or working in @workspace-mode.

In Tabular Editor 3, you can refresh a table from the TOM Explorer and follow the progress in the @data-refresh-view.

## Options

### Lineage Tag
`LineageTag` · string · compatibility level 1540+

A stable ID for the object, usually a GUID. Power BI uses lineage tags to follow an object through renames. For example, a report or a composite model that depends on a column keeps working after the column is renamed, because it tracks the column by its lineage tag.

Power BI Desktop assigns lineage tags automatically. Don't change or copy them: two objects with the same lineage tag confuse the tools that depend on it. When Tabular Editor creates a new object in a model that uses lineage tags, it assigns a new one.

### Source Lineage Tag
`SourceLineageTag` · string · compatibility level 1550+

The lineage tag of the object this one comes from. It's used when a model is built on top of another source, such as a composite model or a Direct Lake model, to link the object to the column or table it came from. For Direct Lake, it holds the name of the source column or table in the lakehouse or warehouse.

When you import Direct Lake tables in Tabular Editor 3, it sets **Source Lineage Tag** for you. On a table, the value is the schema and name of the source table, for example `[dbo].[Sales]`, or only `[Sales]` when the source doesn't use schemas. On a column, the value is the name of the source column. Tabular Editor 3 also sets it on the columns it adds when you update the table schema of a Direct Lake model.

## Translations, Perspectives, Security

### Translated Names
`TranslatedNames` · per culture

The object's name in each culture of the model. Client tools show the translation that matches the user's language. Leave a culture empty to use the untranslated name. See @how-to-work-with-perspectives-translations.

In Tabular Editor 3, the @metadata-translation-editor shows the translated names, descriptions and display folders of many objects side by side. To exchange translations with translators as a JSON file, see @import-export-translations. The Best Practice Analyzer rule @kb.bpa-translate-visible-names flags visible objects with a missing name translation.

### Translated Descriptions
`TranslatedDescriptions` · per culture

The object's description in each culture of the model. The Best Practice Analyzer rule @kb.bpa-translate-descriptions flags descriptions with a missing translation.

### Translated Display Folders
`TranslatedDisplayFolders` · per culture

The object's display folder in each culture of the model. Use the same backslash and semicolon syntax as in **Display Folder**. The Best Practice Analyzer rule @kb.bpa-translate-display-folders flags visible objects with a missing display folder translation.

### Synonyms
`Synonyms` · per culture

Other words users might type to find the object in natural-language features such as Q&A in Power BI. Synonyms are stored in the linguistic schema of each culture (see **Content** on @object-properties-perspectives-cultures).

In Tabular Editor 3, the property only appears when at least one culture has a linguistic schema in JSON format. The collapsed property shows how many linguistic schemas are defined. Expand it to see one entry per culture, with the synonyms as a comma-separated list, for example `revenue, turnover`. Edit the list to add or remove synonyms. Tabular Editor marks a removed synonym as deleted in the linguistic schema instead of removing it, and doesn't show deleted or suggested synonyms. Tables, columns, measures, hierarchies and levels can have synonyms.

### Shown in Perspective
`InPerspective` · per perspective

Whether the object is included in each perspective of the model. Perspectives let you show a smaller part of the model to a group of users. Like hiding, they aren't a security feature.

When you select several objects, you can change their perspective membership at once in the Properties view. See @perspectives-translations. In Tabular Editor 3, the @perspective-editor shows the perspective membership of all tables, columns, hierarchies and measures as checkboxes.
