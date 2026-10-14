---
uid: object-properties-perspectives-cultures
title: Perspective and culture properties
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
# Perspective and culture properties

<!--
SUMMARY: Reference for the properties of perspectives and cultures (translations), including linguistic metadata and translation statistics.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

This page covers the properties of perspectives and cultures. For properties that most objects share, see @object-properties-common.

To add or remove perspectives and cultures, use the **Perspectives** and **Cultures** collections on the model (see @object-properties-model), or right-click the **Perspectives** or **Translations** folder in the **TOM Explorer**. Tabular Editor 2 uses the same folder names. See @perspectives-translations. To create and change perspectives and cultures with a C# script, see @how-to-work-with-perspectives-translations.

## Perspective

A perspective is a named subset of the model: a selection of tables, columns, measures and hierarchies for a group of users. For example, a `Sales` perspective shows only the objects that the sales team needs. In client tools that support perspectives, such as Excel, users pick a perspective and see only the objects in it. Power BI report authors can't pick a perspective in the field list, but you can use one when you connect to the model through the XMLA endpoint or in a personalized visual.

In the Power BI service, you connect to a perspective through the XMLA endpoint by adding `Cube=<perspective name>` to the connection string. That only changes which objects the schema information lists, and DAX queries can still use every table and measure in the model.

<!-- TODO (not verifiable from TE3 source): whether personalized visuals in the Power BI service still use perspectives. -->

> [!NOTE]
> Perspectives don't restrict access. A user can query every object in the model, whichever perspective they use. To restrict access, use @roles-and-rls.

A perspective has no properties of its own beyond the common ones. You choose which objects it contains on the objects themselves, with `InPerspective` (see [Shown in Perspective](xref:object-properties-common#shown-in-perspective)), or, in Tabular Editor 3, for many objects at once in the @perspective-editor.

The Best Practice Analyzer (BPA) rule @kb.bpa-perspectives-no-objects flags perspectives that contain no tables, and @kb.bpa-translate-perspectives flags perspectives whose name isn't translated in every culture.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Object Type](xref:object-properties-common#object-type)
- [Translated Names](xref:object-properties-common#translated-names)
- [Translated Descriptions](xref:object-properties-common#translated-descriptions)

## Culture

A culture holds the translations of the model for one language: the translated names, descriptions and display folders of its objects, and the linguistic metadata for that language. Client tools show the culture that matches the user's language settings, and the untranslated names when no culture matches.

The `Name` of a culture is the culture code, for example `da-DK` or `fr-FR`. It must be a valid culture name, and each culture can only appear once in the model. In Tabular Editor 3, the **Properties** view labels it **Language** and lists the cultures to pick from.

Translations are edited on each object, with `TranslatedNames`, `TranslatedDescriptions` and `TranslatedDisplayFolders`, or, in Tabular Editor 3, for many objects at once in the @metadata-translation-editor. To exchange translations with translators, see @import-export-translations.

The translation statistics properties show how much of the model is translated in this culture, for each type of object. Tabular Editor computes them, and they aren't stored in the model. Each value has the form `12 of 40`, the number of translations out of the total number of objects of that type in the model, hidden objects included. For names, a translation only counts when it isn't empty and differs from the object's untranslated name. To find the objects that are missing a translation, use the BPA rules @kb.bpa-translate-visible-names, @kb.bpa-translate-descriptions and @kb.bpa-translate-display-folders.

### Common properties

- [Name](xref:object-properties-common#name)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Object Type](xref:object-properties-common#object-type)

### Altered
`Altered` · bool (empty when mixed) · Basic · compatibility level 1571+ · *shortcut to* the **Altered** flag of every translation in the culture

Each translation in a culture carries an *altered* flag in the Tabular Object Model (TOM), which translation tools use to mark translations that a person has reviewed or changed. This property sums up the flags of all translations in the culture:

- `true`: every translation has the flag set
- `false`: no translation has the flag set
- empty: some translations have it and some don't

Set it to `true` or `false` to set or clear the flag on every translation in the culture at once. The **Properties** view shows this property at compatibility level 1571 and higher.

> [!WARNING]
> You can't undo a change to `Altered`.

The flag isn't saved in model files. Microsoft's TOM library doesn't write it to Tabular Model Scripting Language (TMSL), which covers `.bim` files, folders in the JSON format and deployment scripts, or to Tabular Model Definition Language (TMDL). The flag is lost when you save the model to a file and open it again.

When you set the flag through a live connection to a server, the server keeps it. On SQL Server 2025 Analysis Services, it survives a reconnect and shows in the `TMSCHEMA_OBJECT_TRANSLATIONS` DMV. A TMSL script generated from that server still leaves it out, so the flag is lost as soon as the model is saved to a file or deployed from one.

<!-- TODO (not verifiable from TE3 source): confirm which tools set and read the Altered flag. -->

### Content
`Content` · string · Linguistic Metadata · compatibility level 1465+

The linguistic schema of the culture: the natural-language metadata that Power BI Q&A used before it was retired. It contains the synonyms for tables, columns and measures, and phrasings that describe how objects relate, for example that customers buy products. The `Synonyms` property on each object reads and writes the synonyms stored here.

The content is a large JSON or XML document, depending on `ContentType`, and Power BI Desktop maintains it. The **Properties** view shows this property at compatibility level 1465 and higher.

In Tabular Editor 3, select **...** on the property to edit the content in a multi-line text editor. Tabular Editor doesn't validate the document, and it sets `ContentType` from the first character: content that starts with `{` is JSON, anything else is XML. Clearing the content removes the linguistic metadata from the culture. Tabular Editor reads and writes `Synonyms` only from JSON content.

### Content Type
`ContentType` · ContentType · Linguistic Metadata · read-only · compatibility level 1465+

The format of `Content`, `Json` for models created by Power BI or `Xml` for the older format. It's empty when the culture has no linguistic metadata. Tabular Editor sets it when you edit `Content`. The **Properties** view shows this property at compatibility level 1465 and higher.

### Translated Table Names
`StatsTableCaptions` · string · Translation Statistics · read-only · *computed*

How many table names are translated.

### Translated Column Names
`StatsColumnCaptions` · string · Translation Statistics · read-only · *computed*

How many column names are translated.

### Translated Column Folders
`StatsColumnDisplayFolders` · string · Translation Statistics · read-only · *computed*

How many column display folders are translated. The total is the number of columns in the model, including columns that have no display folder, so the first number is usually lower than the second, even when every display folder is translated.

### Translated Measure Names
`StatsMeasureCaptions` · string · Translation Statistics · read-only · *computed*

How many measure names are translated.

### Translated Measure Folders
`StatsMeasureDisplayFolders` · string · Translation Statistics · read-only · *computed*

How many measure display folders are translated. The total is the number of measures in the model, including measures that have no display folder.

### Translated Hierarchy Names
`StatsHierarchyCaptions` · string · Translation Statistics · read-only · *computed*

How many hierarchy names are translated.

### Translated Hierarchy Folders
`StatsHierarchyDisplayFolders` · string · Translation Statistics · read-only · *computed*

How many hierarchy display folders are translated. The total is the number of hierarchies in the model, including hierarchies that have no display folder.

### Translated Level Names
`StatsLevelCaptions` · string · Translation Statistics · read-only · *computed*

How many hierarchy level names are translated. The BPA rule @kb.bpa-translate-hierarchy-levels flags the levels of visible hierarchies that have no translated name.
