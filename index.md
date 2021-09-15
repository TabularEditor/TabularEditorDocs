---
uid: index
title: Tabular Editor
author: Daniel Otykier
updated: 2021-09-09
---
# Tabular Editor

Tabular Editor is a tool that lets you easily manipulate and manage measures, calculated columns, display folders, perspectives and translations in Analysis Services Tabular and Power BI Models.

The tool is available in two different versions:

- Tabular Editor 2.x (free, [MIT license](https://github.com/TabularEditor/TabularEditor/blob/master/LICENSE)) - [GitHub project page](https://github.com/TabularEditor/TabularEditor)
- Tabular Editor 3.x (commercial) - [Home page](https://tabulareditor.com)

## Description
This site contains the documentation for both versions. Select your version in the navigation bar at the top of the screen for product specific documentation.

## Choosing between TE2 and TE3

Tabular Editor 3 is the evolution of Tabular Editor 2. It has been designed for those who seek a "one-tool-to-rule-them-all" solution for Tabular data modeling and development.

### Feature overview

The table below lists all the main features of both tools.

||TE2 (Free)|TE3 (Commercial)|
|---|---|---|
|Edit all TOM objects and properties|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|
|Batch editing and renaming|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|
|Copy/paste and drag/drop support|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|
|Undo/redo data modeling operations|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|
|Load/save model metadata to disk|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>*|
|Save-to-folder|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>*|
|[daxformatter.com](https://daxformatter.com) integration|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|
|Advanced data modeling (OLS, Perspectives, Calculation Groups, Metadata Translations, etc.)|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>*|
|Syntax highlighting and automatic formula fixup|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|
|View DAX dependencies between objects|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|
|Import Table Wizard|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|
|Deployment Wizard|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>*|
|Best Practice Analyzer|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|
|C# scripting and automation|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|
|Use as External Tool for Power BI Desktop|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>|
|Connect to SSAS/Azure AS/Power BI Premium|<span class="emoji">&#10004;</span>|<span class="emoji">&#10004;</span>*|
|Command-line interface|<span class="emoji">&#10004;</span>|*[Coming soon](xref:roadmap)*|
|Premium, customizable user-interface with high-DPI, multi-monitor and theming support||<span class="emoji">&#10004;</span>|
|World-class DAX editor with IntelliSense<sup>TM</sup>-like features||<span class="emoji">&#10004;</span>|
|Offline DAX syntax checking and column/data type inference||<span class="emoji">&#10004;</span>|
|Improved Table Import Wizard and Table Schema Update check with Power Query support||<span class="emoji">&#10004;</span>|
|DAX querying, table preview and Pivot Grids||<span class="emoji">&#10004;</span>|
|Create diagrams for visualizing and editing table relationships||<span class="emoji">&#10004;</span>|
|Execute data refresh operations in the background||<span class="emoji">&#10004;</span>*|
|C# macro recorder||<span class="emoji">&#10004;</span>|
|Edit multiple DAX expressions in a single document using DAX scripting||<span class="emoji">&#10004;</span>|
|[VertiPaq Analyzer](https://www.sqlbi.com/tools/vertipaq-analyzer/) integration||<span class="emoji">&#10004;</span>|

\***Note:** Limitations apply depending on which [edition](xref:editions) of Tabular Editor 3 you are using.

Below is a more detailed description of some of the features listed above.

### Common features

Both tools provide the same features in terms of which data modeling options are available, by basically exposing every object and property of the [Tabular Object Model](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions), in an intuitive and responsive user interface. You can edit advanced object properties that are not available through the standard tools. The tools can load model metadata from files or from any instance of Analysis Services. Changes are only synchronized when you hit Ctrl+S (save) thus providing an "offline" editing experience which most people consider to be superior to the "always synchronized"-mode of the standard tools. This is especially noticable when working on large and complex data models.

In addition, both tools enables making multiple model metadata changes in batches, renaming objects in batches, copy/pasting objects, dragging/dropping objects across tables and display folders, etc. The tools even have undo/redo support.

Both tools feature the Best Practice Analyzer, which continuously scans the model metadata for rules that you can define on your own, e.g. to enforce certain naming conventions, make sure non-dimension attribute columns are always hidden, etc.

You can also write and execute C#-style scripts in both tools, for automating repetitive tasks such as generating time-intelligence measures and auto-detecting relationships based on column names.

Lastly, thanks to the "Save-to-folder" functionality, a new file format where every object in the model is saved as an individual file, enables parallel development and version control integration, which is something that is not easy to achieve using only the standard tools. 

### Tabular Editor 2.x

Tabular Editor 2.x is a lightweight application for quickly modifying the TOM (Tabular Object Model) of an Analysis Services or Power BI data model. The tool was originally released in 2016 and receives regular updates and bugfixes.

![Tabular Editor 2.x](~/images/te2.png)

**Tabular Editor 2.x main features:**

- A very lightweight application with a simple and intuitive interface for navigating the TOM
- DAX Dependency View, and keyboard shortcuts for navigating between DAX objects
- Support for editing model perspectives and metadata translations
- Batch renaming
- Search box for quickly navigating large and complex models
- Deployment Wizard
- Best Practice Analyzer
- Advanced Scripting using C#-style scripts for automating repeated tasks
- Command line interface (can be used to integrate Tabular Editor and DevOps pipelines)

### Tabular Editor 3.x

Tabular Editor 3.x is a more advanced application which offers a premium experience with many convenient features to combine all your data modeling and development needs in one single tool.

![Tabular Editor 3.x](~/images/te3.png)

**Tabular Editor 3.x main features:**

- A highly-customizable and familiar UI
- High-DPI, multi-monitor and theming support (yes, dark mode is available!)
- World class DAX editor with syntax highlighting, semantic checking, auto-complete and much, much more
- Table browser, Pivot Grid browser and DAX Query editor
- Import Table Wizard with support for Power Query data sources
- Data Refresh view allows you to queue and execute refresh operations in the background
- Diagram editor to easily visualize and edit table relationships
- New DAX Scripting capability to edit DAX expressions for multiple objects in a single document
- VertiPaq Analyzer integration

## Conclusion

If you are new to tabular modeling in general, we recommend that you use the standard tools until you familiarize yourself with concepts such as calculated tables, measures, relationships, DAX, etc. At that point, try to give Tabular Editor 2.x a spin, and see how much faster it enables you to achieve certain tasks. If you like it and want more, consider Tabular Editor 3.x!

## Next steps

- [Tabular Editor 2.x documentation](te2/Getting-Started.md)
- [Tabular Editor 3.x documentation](te3/getting-started.md)
- [Tabular Editor 3 roadmap](xref:roadmap)
- [Common features](common/common-features.md)