---
uid: user-interface
title: Basic user interface
author: Daniel Otykier
updated: 2021-09-08
---
# Getting to know Tabular Editor 3's User Interface

This article describes the user interface of Tabular Editor 3.

## Basic user interface elements

The first time you launch Tabular Editor 3 and load a data model, you will be presented with an interface as shown on the screenshot below.

![Basic user interface](~/images/basic-ui.png)

1. **Title bar**: This shows the name or the currently loaded file and Analysis Services database or Power BI dataset if connected.
2. **Menu bar**: The menu bar provides access to all of the various features of Tabular Editor 3. See [Menus](#menus) for a detailed walkthrough of all menu items.
3. **Toolbars**: The toolbars provide quick access to the most commonly used features. All features accessible through the toolbar can also be accessed through the menus. You may customize the toolbars and their buttons under **Tools > Customize...**
4. **TOM Explorer view**: A hierarchical view of your data model, with all objects available .  of the metadata from the [Tabular Object Model (TOM)](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) metadata that represents your data model. The toggle buttons at the top allow you to filter which objects are displayed. The search box allows you to filter objects by names.
5. **Expression Editor**: The expression editor provides a quick way to edit any DAX, SQL or M expressions of the currently selected object in the TOM Explorer. If you close the expression editor, you can bring it back up by double-clicking on an object in the TOM Explorer. The dropdown at the top allows you to switch between different expression properties, in case the currently selected object has more than one such property (for example, KPIs have Target Expressions, Status Expressions and Trend Expressions, which are 3 different DAX expressions belonging to the same KPI object).
6. **Properties view**: A detailed view of all TOM properties available on the currently selected object(s) in the TOM Explorer. Most properties can be edited through the grid, even when multiple objects are selected. Some properties (such as "Format String", "Connection String", "Role Members") have popup dialogs or collection editors that can be brought up by clicking on the ellipsis button within the property value cell.
7. **Messages view**: Tabular Editor 3 continuously analyzes the DAX expressions on your model for semantic errors. Any such errors are outputted here. In addition, messages shown in this view, can originate from C# scripts or from error messages reported by Analysis Services.
8. **Status bar**: The status bar provides various contextual information about the current selection, Best Practice Analyzer findings, etc.

There are a number of additional views available, serving various purposes. More information in the [View menu](#view) section.

# Customizing the user interface

All UI elements may be resized and/or rearranged to fit your needs. You can even drag individual views out of the main view, thus splitting up an instance of Tabular Editor 3 across multiple monitors. Tabular Editor 3 will save the customization when the application is closed, and reload it automatically upon next launch.

### Choosing a different layout

To reset the application to the default layout, choose the **Window > Default layout** option. Users of Tabular Editor 2.x may prefer the **Window > Classic layout** option which places the TOM Explorer on the left side of the screen, and the Properties view below the Expression Editor.

Use the **Window > Capture current layout..." option to save a customized layout such that it will become available as a new layout option within the Window menu, allowing you to quickly switch back and forth between different layouts. Use the **Window > Manage layouts...** option to bring up a list of all available layouts, allowing you to rename, save, delete layouts, etc. When saving a layout to disk, the result is an .xml file which you can share with other users of Tabular Editor 3.

![Manage Layouts](~/images/manage-layouts.png)

### Changing themes and palettes

The visual appearance of Tabular Editor 3 can be changed by choosing a different theme and/or palette. Tabular Editor 3 ships with five different themes (sometimes called "skins"), available through the **Window > Themes** menu:

- Basic and Bezier (vector based, works well on high-DPI displays)
- Blue, Dark and Light (raster based, not recommended for high-DIP Displays)

For the vector based themes (Basic and Bezier), use the **Window > Palette** menu item to change the colors used by the theme.

![Palettes](~/images/palettes.png)

# Menus

The following section describes the menus in Tabular Editor 3 in more details.

We use the term **Active document** in the following section, to mean that the cursor is placed within a document such as the Expression Editor or the "DAX Script 1" tab in the screenshot below. Some keyboard shortcuts and menu items behave differently depending on whether there is an active document or not, and what type of document is active.

![Active Document](~/images/active-document.png)

## File

The **File** menu primarily contains menu items for dealing with loading and saving model metadata and supporting files and documents.

![File Menu](~/images/file-menu.png)

- **New**: Opens a submenu that allows you to create a new blank data model (Ctrl+N), or create various [supporting files](xref:supported-files.#supported-file-types) such as a new DAX Query or DAX Script (text files) or a data model diagram (JSON file). Supporting files (with the exception of C# scripts), can be created only when a model is already loaded in Tabular Editor.
  
  ![File Menu New](~/images/file-menu-new.png)

> [!IMPORTANT]
> The **New > Model...** option is not available in Tabular Editor 3 Desktop Edition, as this edition may only be used as an External Tool for Poewr BI Desktop. [More information](xref:editions).

- **Open**: Opens a submenu with options for loading a data model from various sources, as well as on option for loading any other type of file. The submenu items are:

  ![File Menu Open](~/images/file-menu-open.png)

  - **Model from file...** Open model metadata from a file such as a .bim or .pbit file.
  - **Model from DB...** Specify Analysis Services or Power BI XMLA connection details, or connect to a local instance of Analysis Services (such as Visual Studio's Integrated Workspace server or Power BI Desktop), in order to load model metadata from a tabular model that has already been deployed.
  - **Model from folder...** Open model metadata from a folder structure which was previously saved using any version of Tabular Editor.
  - **File...** displays a dialog that lets you open any type of file supported by Tabular Editor 3, based on the file name extension. See [Supported file types](xref:supported-files) for more information.

    ![Supported File Types](~/images/supported-file-types.png)

> [!IMPORTANT]
> In Tabular Editor 3 Desktop Edition the **Open > Model from file...** and **Open > Model from folder...** options are not available and the **Open > File...** dialog only allows opening [supporting files](xref:supported-files#supported-file-types), not files containing metadata.

- **Revert**: This option lets you reload the model metadata from the source, discarding any changes that are made in Tabular Editor, which have not yet been saved. This option is useful when Tabular Editor 3 is used as an External Tool for Power BI Desktop, and a change is made in Power BI Desktop while Tabular Editor 3 is connected. By choosing **Revert**, Tabular Editor 3 can reload the model metadata from Power BI Desktop without having to reconnect.
- **Close**: This closes the active document (for example a DAX Query, a C# script or a data model diagram). If the document has unsaved changes, Tabular Editor will prompt you to save the changes before closing.
- **Close model**: This unloads the currently loaded model metadata from Tabular Editor. If you made changes to the metadata, Tabular Editor will prompt you to save the changes before closing.
- **Save**: This saves the active document back to the source file. If no document is active, this saves the model metadata back to the source, which could be a Model.bim file, a Database.json (folder structure) or a connected instance of Analysis Services (including Power BI Desktop) or the Power BI XMLA endpoint.
- **Save as...** This allows you to save the active document as a new file. If no document is active, this allows you to save the model metadata as a new file, using the .bim (JSON-based) file.
- **Save to folder...** This allows you to save the model metadata as a [folder structure](xref:save-to-folder).
- **Save all**: Saves all unsaved documents and model metadata at once.
- **Recent files**: Displays a list of recently used supporting files allowing you to quickly reopen them.
- **Recent tabular models**: Displays a list of recently used model metadata files or folders, allowing you to quickly reload model metadata from one of these.

> [!IMPORTANT]
> In Tabular Editor 3 Desktop Edition the **Save to folder** and **Recent tabular models** options are disabled. In addition, the **Save as** option is only enabled for [supporting files](xref:supported-files#supported-file-types).

- **Exit**: Shuts down the Tabular Editor 3 application. You are prompted to save any unsaved files or model metadata before the application is shut down.

## Edit

The **Edit** menu contains standard Windows application menu items for editing a document or making changes to the currently loaded model metadata.

![Edit Menu](~/images/edit-menu.png)

- **Undo**: This option undoes the last change made to the model metadata. When there is no active document, the familiar CTRL+Z shortcut maps to this option.
- **Redo**: This option undoes the last undo against the model metadata. When there is no active document, the familiar CTRL+Y shortcut maps to this option.
- **Undo typing**: Undoes the last text change in the currently active document. When there is no active document, this option is not available.
- **Redo typing**: Undoes the last undo within the currently active document. When there is no active document, this option is not available.
- **Find**: Displays the "Find and replace" dialog with the "Find" tab selected. [More information](xref:find-replace#find).
- **Replace**: Displays the "Find and replace" dialog with the "Replace" tab selected. [More information](xref:find-replace#replace).
- **Cut / Copy / Paste**: These are the familiar Windows editing operations. If there is an active document, then these apply to the text selection within that document. Otherwise, these options may be used to manipulate objects in the TOM Explorer. For example, you can duplicate multiple measures by holding down the SHIFT or CTRL key while selecting the measures in the TOM Explorer, then hitting CTRL+C followed by CTRL+V.
- **Delete**: Deletes the selected text in the active document, or the currently selected object(s) in the TOM Explorer if there is no active document.

> [!NOTE]
> Tabular Editor generally only prompts for object deletion when multiple objects are selected, or when there are dependencies to the object(s) being deleted. Object deletion can be undone by using the **Undo** option (CTRL+Z).

- **Select all**: Selects all text in the currently active document, or all objects belonging to the same parent within the TOM Explorer.
- **Code assist**: This option is available when editing DAX code. It provides a shortcut to various code assist features relevant for editing DAX code. See [DAX editor](xref:dax-editor#code-assist-features) for more information.

## View

The **View** menu lets you navigate between the different views of the Tabular Editor 3 UI. If a view has been hidden, click on the view title in this menu will unhide the view and bring it into focus. Note that documents are not shown in the View menu. To navigate between documents, use the [Window menu](#window).

![View Menu](~/images/view-menu.png)

- **TOM Explorer**: The TOM Explorer presents a hierarchical view of the entire [Tabular Object Model (TOM)](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) of the currently loaded model metadata. See @tom-explorer-view for more information.
- **Best Practice Analyzer**: The Best Practice Analyzer helps improve the quality of your model by letting you specify rules for best practice validation. See @bpa-view for more information.
- **Messages**: The Messages view displays errors, warnings and informational messages from various sources, such as the Tabular Editor 3 Semantic Analyzer. See @messages-view for more information.
- **Data Refresh**: The Data Refresh view allows you to track data refresh operations that are running in the background. See @data-refresh-view for more information.
- **Macros**: The Macros view allows you to manage any macros you have created. Macros can be created from @csharp-scripts. See @creating-macros for more information.
- **VertiPaq Analyzer**: The VertiPaq Analyzer view allows you to collect, import and export detailed statistics about the data in your model, to help improve and debug DAX performance. VertiPaq Analyzer is created and maintained by [Marco Russo](https://twitter.com/marcorus) of [SQLBI](https://sqlbi.com) under MIT license. More information on the [GitHub project page](https://github.com/sql-bi/VertiPaq-Analyzer).
- **Expression Editor**: This is the "quick editor" that lets you edit DAX, M or SQL expressions on whichever object is currently selected in the TOM Explorer. See @dax-editor for more information.

## Model

The **Model** menu displays actions that can be performed at the level of the Model object (the root object of the TOM Explorer).

![View Menu](~/images/model-menu.png)

- **Deploy...**: Launches the Tabular Editor Deployment wizard. For more information, see @deployment.

> [!IMPORTANT]
> The **Deploy** option is not available in Tabular Editor 3 Desktop Edition. For more information see @editions.

- **Import tables...** Launches the Tabular Editor 3 Import Table Wizard. For more information, see @importing-tables.
- **Update table schema...** Detects schema changes in the data source(s) for the currently selected table(s) or partition(s) compared to the currently imported columns. See @importing-tables#updating-table-schema for more information.
- **Script DAX**: Generates a DAX script for the currently selected object(s) (or all DAX objects in the model, if nothing is selected). See @dax-scripts for more information.
- **Refresh model**: When Tabular Editor is connected to an instance of Analysis Services, this submenu contains options for starting a background refresh operation at the model level. The submenu has the options below. For more information, see [Refresh command (TMSL)](https://docs.microsoft.com/en-us/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions#request).
  - **Automatic (model)**: Analysis Services determines which objects to refresh (only objects that are not in the "Ready" state).
  - **Full refresh (model)**: Analysis Services performs a full refresh of the model.
  - **Calculate (model)**: Analysis Services performs a re-calculation of all calculated tables, calculated columns, calculation groups and relationships. No data is read from the data sources.
- **Create [object type]**: The remaining shortcuts in the **Model** menu lets you create new types of model child objects (tables, data sources, perspectives, etc.).

## Tools

The **Tools** menu contains options for controlling Tabular Editor 3 preferences and customizations.

![View Menu](~/images/tools-menu.png)

- **Customize...** Launches the Tabular Editor 3 User Interface Layout customization dialog, which lets you create new toolbars, rearrange and edit menus and toolbar buttons, etc.
- **Preferences...** Launches the Tabular Editor 3 Preferences dialog, which is a central hub for managing all other aspects of Tabular Editor and its features, such as update checks, proxy settings, query row limits, request timeouts, etc. See @preferences for more information.

## Window

The **Window** menu provides shortcuts for managing and navigating between the various views and documents (collectively known as *windows*) of the application. It also has menu items for controlling the theming and color palettes as described [above](#changing-themes-and-palettes).

![View Menu](~/images/window-menu.png)

- **New...** this submenu provides a shortcut for creating new [supporting files](xref:supported-files#supported-file-types). The options here are identical to those under **File > New**.
- **Float** undocks the current view or document into a floating window.
- **Pin tab** pins a tab. When a tab is pinned, it is shown at the left-most side of the document tabs, and when right-clicking on the tabs, shortcuts are available for closing only unpinned tabs.
  
  ![View Menu](~/images/tab-context-menu.png)

- **New Horizontal/Vertical Tab Group**: This option lets you divide the main document area into multiple sections (aka. "tab groups), in order to have multiple documents displayed simultaneously side-by-side or top-by-bottom.
- **Close All Documents**: Closes all document tabs. You are prompted to save unsaved changes, if any.
- **Reset Window Layout**: Resets all customization applied to the main document area.
- **1..N [document]**: The first 10 open documents are listed here, allowing you to navigate between them. You can also use the CTLR+Tab shortcut to quickly switch between open documents and views, such as shown in the screenshot below:

  ![View Menu](~/images/ctrl-tab.png)

- **Windows...**: Opens a dialog listing ALL open documents, allowing you to switch between them or close them individually.

  ![View Menu](~/images/windows-manager.png)

- **Capture current layout** / **Manage layouts...** / **Default layout** / **Classic layout**: These menu items were discussed [earlier in this article](#choosing-a-different-layout).
- **Theme** / **Default palette**: These menu items were discussed [earlier in this article](#changing-themes-and-palettes).

## Help

The **Help** menu provides shortcuts for online resources and more.

![View Menu](~/images/help-menu.png)

- **Getting Started**: This menu item links to [this article](xref:getting-started).
- **Tabular Editor 3 Docs**: This menu item links to [docs.tabulareditor.com](https://docs.tabulareditor.com/te3).
- **Community Support**: This menu item links to our [public community support site](https://github.com/TabularEditor/TabularEditor3).
- **Dedicated Support**: This menu item lets you send an e-mail directly to our dedicated support hotline.

> [!NOTE]
> Dedicated support is reserved for Tabular Editor 3 Enterprise Edition customers. All other customers should reach out on the [public community support site](https://github.com/TabularEditor/TabularEditor3) for any technical issues, questions or other product-specific questions.

- **About Tabular Editor**: Launches a dialog that shows detailed information about the version of Tabular Editor being used as well installation and licensing details. The dialog also lets you change your license key.
 
## Dynamic menus (context dependent)

In addition to the menus mentioned above, other menus may appear at certain times, depending on which UI element currently has focus and which object is currently selected in the TOM Explorer. For example, if you select a Table-object, a **Table** menu will appear, holding the same context-specific shortcut items as when you right-click on that object in the TOM Explorer.

If you switch the input focus between different types of documents (i.e. DAX queries, Pivot Grids, diagrams, etc.), you should also see a menu representing the type of document currently in focus. That menu will hold items relevant for the current document. For example, when a diagram currently has focus, there will be a **Diagram** menu which has an item for adding tables to the diagram, among others.

You can change the behavior of these dynamic menus under **Tools > Preferences > User interface**.

# Next steps

- [Using the TOM Explorer in Tabular Editor 3](xref:tom-explorer-view)
- @supported-files
- @preferences