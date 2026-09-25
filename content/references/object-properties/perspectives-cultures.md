---
uid: object-properties-perspectives-cultures
title: Perspective and culture properties
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
# Perspective and culture properties

<!--
SUMMARY: Reference for the properties of perspectives and cultures (translations), including linguistic metadata and translation statistics.
-->

This page covers the properties of perspectives and cultures. For properties that most objects share, see @object-properties-common.

To add or remove perspectives and cultures, use the **Perspectives** and **Cultures** collections on the model (see @object-properties-model), or right-click the **Perspectives** or **Translations** folder in the TOM Explorer. See @perspectives-translations. To create and change perspectives and cultures with a C# script, see @how-to-work-with-perspectives-translations. Tabular Editor 2 uses the same folder names.

## Perspective

A perspective is a named subset of the model: a selection of tables, columns, measures and hierarchies for a group of users. For example, a `Sales` perspective could show only the objects that the sales team needs. Client tools that support perspectives, such as Excel, let users pick one, and then show only the objects in it. Power BI doesn't let report authors pick a perspective in the field list, but you can use one when you connect to the model through the XMLA endpoint or in a personalized visual.

In the Power BI service, you connect to a perspective through the XMLA endpoint by adding `Cube=<perspective name>` to the connection string. That only changes which objects the schema information lists: DAX queries can still use every table and measure in the model.

<!-- TODO (not verifiable from TE3 source): whether personalized visuals in the Power BI service still use perspectives. -->

Perspectives aren't a security feature. A user can still query every object in the model, whichever perspective they use. To restrict access, use @roles-and-rls.

A perspective has no properties of its own beyond the common ones. You choose which objects it contains on the objects themselves, with **Shown in Perspective** (see [Shown in Perspective](xref:object-properties-common#shown-in-perspective)), or, in Tabular Editor 3, for many objects at once in the @perspective-editor.

The Best Practice Analyzer rule @kb.bpa-perspectives-no-objects flags perspectives that contain no tables, and @kb.bpa-translate-perspectives flags perspectives whose name isn't translated in every culture.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Object Type](xref:object-properties-common#object-type)
- [Translated Names](xref:object-properties-common#translated-names)
- [Translated Descriptions](xref:object-properties-common#translated-descriptions)

## Culture

A culture holds the translations of the model for one language: the translated names, descriptions and display folders of its objects, and the linguistic metadata that Power BI Q&A uses for that language. Client tools show the culture that matches the user's language settings. When no culture matches, they show the untranslated names.

The **Name** of a culture is the culture code, for example `da-DK` or `fr-FR`. It must be a valid culture name, and each culture can only appear once in the model. In Tabular Editor 3, the Properties view labels it **Language** and lets you pick the culture from a list.

You don't edit the translations on the culture itself. Instead, use the **Translated Names**, **Translated Descriptions** and **Translated Display Folders** properties on each object, or, in Tabular Editor 3, the @metadata-translation-editor for many objects at once. To exchange translations with translators, see @import-export-translations.

### Common properties

- [Name](xref:object-properties-common#name)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Object Type](xref:object-properties-common#object-type)

### Basic

#### Altered
`Altered` · bool (empty when mixed) · *shortcut to* the **Altered** flag of every translation in the culture

Each translation in a culture carries an *altered* flag in TOM. Translation tools use it to mark translations that a person has reviewed or changed, as opposed to ones that were generated automatically. This property sums up the flags of all translations in the culture:

- `true`: every translation has the flag set.
- `false`: no translation has the flag set.
- Empty: some translations have it and some don't.

Set it to `true` or `false` to set or clear the flag on every translation in the culture at once. The Properties view shows this property at compatibility level 1571 and higher.

> [!WARNING]
> You can't undo a change to **Altered**.

The flag isn't saved in model files. Microsoft's TOM library doesn't write it to TMSL (`.bim` files, folders in the JSON format and deployment scripts) or to TMDL, so it's lost when you save the model to a file and open it again.

When you set the flag through a live connection to a server, the server keeps it: on SQL Server 2025 Analysis Services, it survives a reconnect and shows in the `TMSCHEMA_OBJECT_TRANSLATIONS` DMV. A TMSL script generated from that server still leaves it out, so the flag is lost as soon as the model is saved to a file or deployed from one.

<!-- TODO (not verifiable from TE3 source): confirm which tools set and read the Altered flag. -->

### Linguistic Metadata

#### Content
`Content` · string

The linguistic schema of the culture, which Power BI Q&A uses to understand natural-language questions. It contains, among other things, the synonyms for tables, columns and measures, and phrasings that describe how objects relate, for example that customers *buy* products. The **Synonyms** property on each object reads and writes the synonyms stored here.

The content is a large JSON or XML document, depending on **Content Type**. Power BI Desktop maintains it. The Properties view shows this property at compatibility level 1465 and higher.

In Tabular Editor 3, select **...** on the property to edit the content in a multi-line text editor. Tabular Editor doesn't validate the document. It sets **Content Type** from the first character: content that starts with `{` is JSON, anything else is XML. Clearing the content removes the linguistic metadata from the culture. Edit it by hand with care: an invalid document can make Q&A stop working for the culture, and Tabular Editor can only read and write **Synonyms** from JSON content.

#### Content Type
`ContentType` · ContentType · read-only

The format of **Content**: `Json` for models created by Power BI, or `Xml` for the older format. It's empty when the culture has no linguistic metadata. Tabular Editor sets it for you when you edit **Content**. The Properties view shows this property at compatibility level 1465 and higher.

### Translation Statistics

These properties show how much of the model is translated in this culture, for each type of object. Use them to spot missing translations before you deploy. They're computed by Tabular Editor and aren't stored in the model.

Each value has the form `12 of 40`: the number of translations, out of the total number of objects of that type in the model. The total includes hidden objects. For names, a translation only counts when it isn't empty and differs from the object's untranslated name.

To find the objects that are missing a translation, use the Best Practice Analyzer rules @kb.bpa-translate-visible-names, @kb.bpa-translate-descriptions and @kb.bpa-translate-display-folders.

#### Translated Table Names
`StatsTableCaptions` · string · *computed* · read-only

How many table names are translated.

#### Translated Column Names
`StatsColumnCaptions` · string · *computed* · read-only

How many column names are translated.

#### Translated Column Folders
`StatsColumnDisplayFolders` · string · *computed* · read-only

How many column display folders are translated. The total is the number of columns in the model, including columns that have no display folder. So the first number is usually lower than the second, even when every display folder is translated.

#### Translated Measure Names
`StatsMeasureCaptions` · string · *computed* · read-only

How many measure names are translated.

#### Translated Measure Folders
`StatsMeasureDisplayFolders` · string · *computed* · read-only

How many measure display folders are translated. The total is the number of measures in the model, including measures that have no display folder.

#### Translated Hierarchy Names
`StatsHierarchyCaptions` · string · *computed* · read-only

How many hierarchy names are translated.

#### Translated Hierarchy Folders
`StatsHierarchyDisplayFolders` · string · *computed* · read-only

How many hierarchy display folders are translated. The total is the number of hierarchies in the model, including hierarchies that have no display folder.

#### Translated Level Names
`StatsLevelCaptions` · string · *computed* · read-only

How many hierarchy level names are translated. The Best Practice Analyzer rule @kb.bpa-translate-hierarchy-levels flags the levels of visible hierarchies that have no translated name.
