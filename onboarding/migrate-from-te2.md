---
uid: migrate-from-te2
title: Migrating from Tabular Editor 2.x
author: Daniel Otykier
updated: 2021-09-30
---

# Migrating from Tabular Editor 2.x

This article is intended for developers who already have some experience using Tabular Editor 2.x for Power BI Dataset or Analysis Services Tabular development. The article highlights similarities and important feature additions of Tabular Editor 3, to get you quickly up to speed.

## Installation side-by-side

Tabular Editor 3 has a different product code than Tabular Editor 2.x. This means that you can install both tools side-by-side without issues. In fact, the tools are installed into separate program folders and their settings are also kept in separate folders. In other words, the term "upgrade" or "downgrade" between Tabular Editor 2.x and Tabular Editor 3 does not apply. It is better to think of Tabular Editor 3 as an entirely different product.

## Feature comparison

In terms of features, Tabular Editor 3 is essentially a superset of Tabular Editor 2.x, with few exceptions. The table below compares all major features of the two tools:

||Tabular Editor 2.x|Tabular Editor 3|
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

## Feature differences

Below is a summary of important feature differences.

### User interface

The first thing you will notice when launching Tabular Editor 3, is the new Visual Studio Shell-like interface. This interface is fully customizable, supports high-DPI, multiple monitors and even allows you to change the theming. All interface elements can be moved to different locations, so if you prefer the interface layout of Tabular Editor 2.x, immediately choose **Classic layout** from the **Window** menu.

In general, though, interface elements that exist in Tabular Editor 2.x have the same name in Tabular Editor 3, so it should be relatively easy to navigate the new interface. A few important differences are listed below:

- The **Advanced Scripting** tab in Tabular Editor 2.x is gone. In Tabular Editor 3, you instead create *C# Scripts** using the **File > New** menu. You are not limited to working on a single script at a time. In addition, **Custom actions** have been renamed to **Macros**.
- **Dynamic LINQ filtering** is not currently available within the TOM Explorer. Instead, if you want to find objects using [Dynamic LINQ](https://dynamic-linq.net/expression-language) you have to bring up the **Find and replace** dialog by pressing CTRL+F.
- If you close the **Expression Editor** you can bring it back by doubleclicking on the icon of an object in the **TOM Explorer**, or by choosing the **View > Expression Editor** menu option.
- When using the default layout in Tabular Editor 3, the **Best Practice Analyzer** will be located as a tab next to the **TOM Explorer**. Here, you will also find the new **Data Refresh** view (which lets you view the queue of background refresh operations) and the **Macros** view (which lets you manage any macros that was previously saved from C# scripts).
- Tabular Editor 3 displays all DAX syntax and semantic errors in the new **Messages View**. In the default layout, this is located at the bottom left of the interface.
- In addition, Tabular Editor 3 includes **VertiPaq Analyzer** (which you may be familiar with from [DAX Studio](https://daxstudio.org/)).
- As a final note, Tabular Editor 3 introduces the concept of **documents**, which is just a generic term for C# scripts, DAX scripts, DAX Queries, Diagrams, Data Previews and Pivot Grids.

For more information, see <xref:user-interface>.

### New DAX editor and semantic capabilities

Tabular Editor 3 features its very own DAX parsing engine (aka. the "semantic analyzer"), which means that the tool now understands the semantics of any DAX code in your model. This engine is also used to power our DAX editor (codename "Daxscilla"), to enable features such as syntax highligting, automatic formatting, code completion, calltips, refactoring and much more. Of course the editor is highly configurable, allowing you to tweak it to match your preferred DAX coding style.

To learn more about the new DAX editor, see <xref:dax-editor>.

In addition, the semantic analyzer continuously reports any DAX syntax or semantic errors across all objects in your model. This works even if not connected to Analysis Services and is lightning fast. The semantic analyzer also enabled Tabular Editor 3 to automatically infer data types from DAX expressions. In other words, Tabular Editor 3 automatically detects which columns would result from a calculated table expression. This is a big improvement over Tabular Editor 2.x, where you would have to manually map columns on a calculated table, or rely on Analysis Services to return the column metadata.

### Table Import and Schema Update with Power Query support

Another major advantage of Tabular Editor 3 over Tabular Editor 2.x is its support for structured data sources and Power Query (M) partitions. Specifically, the "Schema Update" feature now works for these types of data sources and partitions, and the Table Import Wizard can generate the necessary M code when importing new tables.

The schema compare dialog itself also has a number of improvements, for example allowing you to easily map a column delete+column insert operation to a single column rename operation (and vice versa). There are also options for controlling how floating and decimal data types should be treated (for example, sometimes your data source may be using a floating point data type, but you may still want to import it always as a decimal type).

To learn more, see <xref:importing-tables>.

### Workspace mode

Tabular Editor 3 introduces the concept of **workspace mode**, in which model metadata is loaded from disk (Model.bim or Database.json), and then immediately deployed to an Analysis Services instance of your choice. Whenever you hit Save (CTRL+S), the workspace database is synchronized and updated model metadata is saved back to the disk. The advantage of this approach, is that Tabular Editor is connected to Analysis Services, thus enabling the [connected features](#connected-features) listed below, while also making it easy to update the source files on disk. With Tabular Editor 2.x, you had to open a model from a database, and then remember to manually save to disk once in a while.

This approach is ideal to enable [parallel development](xref:parallel-development) and model metadata integration with version control systems.

For more information, see <xref:workspace-mode>.

### Connected features

Tabular Editor 3 includes a number of new connected features, allowing you to use it as a client tool for Analysis Services. These features are enabled whenever Tabular Editor 3 is connected to Analysis Services, either directly or when using the [workspace mode](#workspace-mode) feature.

The new connected features are:

- Table data previewing
- PivotGrids
- DAX Querying
- Data refresh operations
- VertiPaq Analyzer

### Diagrams

One highly requested feature of Tabular Editor 2.x, was the ability to better visualize relationships between tables. With Tabular Editor 3, you can now create model diagrams. Each diagram is a simple JSON file that holds the names and coordinates of tables to be included in the diagram. Tabular Editor 3 then renders the tables and relationships and provides features for easily editing relationships, adding additional tables to the diagram based on existing relationships, etc.

![Easily add related tables](~/images/diagram-menu.png)

See [Working with diagrams](xref:importing-tables-data-modeling#working-with-diagrams) for more information.

### C# Scripts and Macro recorder

The **Advanced Scripting** feature of Tabular Editor 2.x has carried over to Tabular Editor 3 as **C# Scripts**. One important difference in Tabular Editor 3 is that you are no longer limited to working with a single script. Instead, using the **File > New > C# Script** option, you can create and work with as many C# scripts as you need. Similar to Tabular Editor 2.x, these scripts can be saved as reusable actions that are integrated directly into the right-click context menu of the TOM Explorer. In Tabular Editor 3, we call these actions **Macros**, and you can even create your own menus and toolbars to which you can add macros.

Most importantly, Tabular Editor 3 features a **Macro recorder** that you can use to automatically generate C# code from user interactions.

To learn more, see @cs-scripts-and-macros.

### DAX Scripting

The last important feature you need to know about, when coming from Tabular Editor 2.x, is **DAX Scripting**. With this feature, you can create documents that allow you to edit the DAX expression and basic properties of several calculated objects at once. Calculated objects are measures, calculated columns, calculated tables, etc.

This is very convenient when authoring complex business logic across several objects. By (multi)selecting objects in the TOM Explorer, right-clicking and choosing the **Script DAX** option, you get a new DAX script containing the definitions of all selected objects. The DAX script editor of course has all of the same DAX capabilities of the Expression Editor and the DAX query editor. 

When working in **connected** or **workspace** mode, DAX scripting is an incredibly powerful tool to quickly modify and test updated business logic, for example when using it in conjunction with a Pivot Grid as shown in the screenshot below. Simply hitting SHIFT+F5 causes the database to be updated based on the DAX expressions in the script, after which the Pivot Grid will immediately update.

![Dax Scripting And Pivot](../images/dax-scripting-and-pivot.png)

To learn more, see @dax-script-introduction.

## Next steps

- @migrate-from-vs
- @parallel-development
- @boosting-productivity-te3
