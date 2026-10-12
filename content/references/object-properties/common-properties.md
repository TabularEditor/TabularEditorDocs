---
uid: object-properties-common
title: Common properties
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
# Common properties

<!--
SUMMARY: Properties that most objects in a semantic model share, such as Name, Description, Annotations and Lineage Tag.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

The properties on this page appear on many object types and work the same way on every object that has them. Each entry gives the property's name in the Tabular Object Model (TOM), its type and its category. The object-specific pages link to these entries. For the other pages, see @object-properties.

## Basic

### Name
`Name` · string · Basic

The name of the object. DAX references tables, columns, measures, hierarchies and user-defined functions by their name. Names must be unique among siblings, so two measures can't share a name. In most models, a measure also can't share a name with any column (see `ForceUniqueNames` on @object-properties-model). A KPI or a calculation group has no name of its own and takes its name from the object it belongs to.

When **Formula Fix-up** is enabled under **Tools > Preferences**, renaming an object updates the DAX expressions that refer to it. When it's disabled, a rename breaks the expressions that use the old name. See @formula-fix-up-dependencies.

To rename many objects at once, select them in the **TOM Explorer** and use batch rename, which supports regular expressions. See @duplicate-and-batch. The Best Practice Analyzer (BPA) rules @kb.bpa-trim-object-names and @kb.bpa-avoid-invalid-characters-names flag names with leading or trailing spaces and names with control characters.

### Description
`Description` · string · Basic

Free text that explains what the object is for. Power BI shows the description as a tooltip in the **Data** pane. Excel's PivotTable field list doesn't show descriptions. To translate descriptions, use `TranslatedDescriptions`.

In Tabular Editor 3, the **TOM Explorer** has a **Description** column where you read and edit descriptions, and DAX code assist shows the description of a table, column or measure in its tooltip. When a measure, calculated column or calculated table has no description, the tooltip shows the first lines of its expression.

The BPA rule @kb.bpa-visible-objects-no-description flags visible objects without a description, and @kb.bpa-avoid-invalid-characters-descriptions flags descriptions that contain control characters.

### Display Folder
`DisplayFolder` · string · Basic

The folder that the object appears in, in the field list of client tools. A backslash (`\`) creates a subfolder, for example `Sales\Year to date`, and a semicolon (`;`) shows the object in more than one folder, for example `Sales;Finance`. Display folders don't affect DAX or security. Tabular Editor also uses them to group objects in the **TOM Explorer**.

To move a display folder with its objects and subfolders, drag it onto another folder in the **TOM Explorer**. See @drag-drop.

### Hidden
`IsHidden` · bool · Basic

When `true`, client tools such as Power BI hide the object from report authors. The object stays in the model, and DAX expressions can still refer to it. Anyone who can query the model can also query a hidden object. To secure data, see @roles-and-rls.

The BPA rule @kb.bpa-hide-foreign-keys flags visible columns on the many side of a relationship. Its automatic fix hides them.

## Metadata

### Annotations
`Annotations` · collection of name/value pairs · Metadata

Custom name/value pairs stored with the object. Analysis Services and Power BI ignore annotations, and tools use them to store their own information. For example, Power BI Desktop stores layout information in annotations, and many C# scripts and BPA rules store settings in them.

In a C# script, use `GetAnnotation`, `SetAnnotation` and `RemoveAnnotation`. See @how-to-annotations-extended-properties.

### Extended Properties
`ExtendedProperties` · collection of name/value pairs · Metadata

Name/value pairs like annotations, where the value is either a string or a JSON document. Power BI uses extended properties, for example to store query information about parameters. For your own metadata, use annotations.

In a C# script, use `GetExtendedProperty` and `SetExtendedProperty`.

### Changed Properties
`ChangedPropertiesCollection` · collection · Metadata

The names of the properties that you changed on an object that comes from another source, such as a table in a composite model or an object that Power BI generates. When the engine synchronizes the object from its source, it doesn't overwrite the properties in this list.

Tabular Editor 3 doesn't add entries to this list. When you change such a property, add its name yourself. Type a comma-separated list of TOM property names, for example `Name,FormatString`, or expand the property and select the check box next to a property name. Duplicates and names that aren't properties of the object are ignored. The expanded list always includes `Name`, plus the properties already in the list. To empty the list, right-click the property and select **Clear Changed Properties**.

### DAX identifier
`DaxObjectFullName` · string · Metadata · read-only · *computed*

The fully qualified name that DAX uses to reference the object, for example `'Sales'[Amount]` for a column or `[Total Sales]` for a measure. C# scripts use it to build DAX expressions. See @how-to-work-with-expressions.

### Error Message
`ErrorMessage` · string · Metadata · read-only

The error that the engine reported for the object, for example a syntax error in a DAX expression or a refresh error on a partition. It's empty when the object has no error.

In Tabular Editor 3, errors in DAX expressions also appear while you type, before the model is saved to the engine. The @messages-view lists all errors and warnings in the model. Double-click a message to go to its object.

### Object Type
`ObjectTypeName` · string · Metadata · read-only · *computed*

The kind of object, for example `Measure`, `Calculated Column` or `Table`.

### State
`State` · ObjectState · Metadata · read-only

Whether the object is ready to be queried. The engine sets the value.

| Value | Meaning |
|---|---|
| `Ready` | The object is valid and, where it holds data, the data is up to date. |
| `NoData` | The object is valid but holds no data yet. Refresh the table or partition. |
| `CalculationNeeded` | The object is valid but must be recalculated, for example a calculated column after a change to its expression. |
| `SemanticError` | The expression refers to something that doesn't exist or is invalid. See `ErrorMessage`. |
| `EvaluationError` | The expression is valid but failed when it was evaluated. |
| `DependencyError` | An object this one depends on is in an error state. |
| `Incomplete` | Some of the object's data is missing, for example when a partition failed to refresh. |
| `ForceCalculationNeeded` | The object must be recalculated even though it seems up to date. |

`State` only has a meaningful value when you're connected to a server or working in @workspace-mode. A model that you open from a file isn't connected to an engine.

In Tabular Editor 3, you can refresh a table from the **TOM Explorer** and follow the progress in the @data-refresh-view.

## Options

### Lineage Tag
`LineageTag` · string · Options · compatibility level 1540+

A stable ID for the object, usually a GUID. Power BI uses lineage tags to follow an object through renames, so a report or a composite model that depends on a column keeps working after the column is renamed.

Power BI Desktop assigns lineage tags automatically. Don't change or copy them: the tools that depend on lineage tags can't tell apart two objects with the same tag. When Tabular Editor creates an object in a model that uses lineage tags, it assigns a new lineage tag.

### Source Lineage Tag
`SourceLineageTag` · string · Options · compatibility level 1550+

The lineage tag of the object that this object comes from. Models built on top of another source, such as a composite model or a Direct Lake model, use it to link the object to the source column or table. For Direct Lake, it holds the name of the source column or table in the lakehouse or warehouse.

Tabular Editor 3 sets `SourceLineageTag` when you import Direct Lake tables, and on the columns it adds when you update the table schema of a Direct Lake model. On a table, the value is the schema and name of the source table, for example `[dbo].[Sales]`, or `[Sales]` when the source doesn't use schemas. On a column, the value is the name of the source column.

## Translations, Perspectives, Security

### Translated Names
`TranslatedNames` · per culture · Translations, Perspectives, Security

The object's name in each culture of the model. Client tools show the translation that matches the user's language. When a culture has no translation, the untranslated name appears. See @how-to-work-with-perspectives-translations.

In Tabular Editor 3, the @metadata-translation-editor shows the translated names, descriptions and display folders of many objects side by side. To exchange translations with translators as a JSON file, see @import-export-translations. The BPA rule @kb.bpa-translate-visible-names flags visible objects with a missing name translation.

### Translated Descriptions
`TranslatedDescriptions` · per culture · Translations, Perspectives, Security

The object's description in each culture of the model. The BPA rule @kb.bpa-translate-descriptions flags descriptions with a missing translation.

### Translated Display Folders
`TranslatedDisplayFolders` · per culture · Translations, Perspectives, Security

The object's display folder in each culture of the model, with the same backslash and semicolon syntax as `DisplayFolder`. The BPA rule @kb.bpa-translate-display-folders flags visible objects with a missing display folder translation.

### Synonyms
`Synonyms` · per culture · Translations, Perspectives, Security

Other words that users type to find the object in natural-language features, such as Q&A in Power BI. Tables, columns, measures, hierarchies and levels can have synonyms. They're stored in the linguistic schema of each culture (see `Content` on @object-properties-perspectives-cultures).

In Tabular Editor 3, the property only appears when at least one culture has a linguistic schema in JSON format. The collapsed property shows how many linguistic schemas are defined. Expand it to see one entry per culture, with the synonyms as a comma-separated list, for example `revenue, turnover`, and edit the list to add or remove synonyms. A removed synonym is marked as deleted in the linguistic schema. Deleted and suggested synonyms don't appear in the list.

### Shown in Perspective
`InPerspective` · per perspective · Translations, Perspectives, Security

Whether the object is included in each perspective of the model. A perspective shows a smaller part of the model to a group of users. Like `IsHidden`, perspectives aren't a security feature.

When you select several objects, you can change their perspective membership at once in the Properties view. See @perspectives-translations. In Tabular Editor 3, the @perspective-editor shows the perspective membership of all tables, columns, hierarchies and measures as check boxes.
