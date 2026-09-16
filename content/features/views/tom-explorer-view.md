---
uid: tom-explorer-view
title: TOM Explorer view
author: Morten Lønskov
updated: 2026-09-16
applies_to:
  products:
    - product: Tabular Editor 2
      partial: true
      note: "Works differently than shown in this article"
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# Using the TOM Explorer in Tabular Editor 3
The TOM Explorer is your main window for interacting with the objects of your data model. Objects such as tables, columns, measures, security groups etc. are all displayed in a hierarchical structure. A Tabular data model is represented by the so called [Tabular Object Model (TOM)](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) and it is the metadata of your TOM that is displayed in the TOM Explorer.

The TOM Explorer consists of two main areas, firstly the data model objects and secondly the menu bar that allows for filtering and changing what is presented in the main window.

![Tom Explorer](~/content/assets/images/user-interface/TOMExplorer.png)

## Data Model Objects
You can fold out objects in the TOM Explorer to see their children and follow the hierarchy of objects downwards. And if you right click on any object you will be given a list of options to interact with that specific object. As you can see below there are several options that you can use with a table. It is with this menu that you for example can easily refresh your tables and see the status of that refresh in the @data-refresh-view

![Tom Explorer Interaction](~/content/assets/images/user-interface/TomExplorerRightClick.png)

The right click menu has the following items some of which can be expanded for more actions. The menu depends on the object type chosen (Table, partition, measure, column etc.) and the list below is not exhaustive for all types of objects but contains those most used.

### Options in Right-click menu
- **Update table schema...**:
Checks for structural changes in the external data source and updates the table's schema accordingly. This is useful when columns have been added, renamed, or removed in the source.

- **Script DAX**:
Generates a DAX script for the selected table and its objects. Opens a new script editor window where you can review or edit DAX definitions collectively.

- **Preview data**:
Opens the data preview pane displaying a sample of the data loaded into the selected table. Useful for validation or debugging. Only exists when right clicking tables.

- **Refresh**:
Expands to a selection of possible refresh operation for the selected table. This is available only if the model is connected to live model either stand alone or in workspace mode. This option is only available on tables and partitions.

- **Create**:
Expands to a submenu allowing the creation of new measures, columns, hierarchies, display folders or calculation items under the selected object. The available options depends on the object type selected.

- **Move to group**:
Expands to a submenu for organizing the selected tables into a Table Group for easier model navigation. The submenu lists existing Table Groups, a **(New...)** entry that creates a new group from the selected tables and opens its name editor, and a **(None)** entry that removes the Table Group assignment. This option is only available for tables.

- **Make invisible**:
Marks the object as not visible in client tools. The table remains part of the model but is hidden from report authors. Alternative use the shortcut **Ctrl+I** to hide the object.

- **Shown in perspectives**:
Enables or disables the table's inclusion in one or more perspectives. Perspectives limit what end-users can see in tools like Power BI.

- **Batch rename**: When selecting more than one object you can batch rename those objects using string replacement or regex. The shortcut for batch rename is **F2**.

- **Batch rename children...**:
Enables bulk renaming of all child objects under the table or display folder using regex or string replacement rules. Can also be accessed with the shortcut **Shift+F2**.

- **Duplicate**:
Creates a copy of the selected table, including all its columns, measures and partitions. Also exists for all other objects in the TOM Explorer.

- **Mark as date table...**:
Marks the table as a date table, enabling time intelligence features. Requires that the table contains a valid date column.

- **Show dependencies**:
Visualizes dependencies between the selected table and other model objects. Can also be accessed via shortcut **Shift+F12**.

- **Export script**:
Exports the selected objects as a TMSL or TMDL script for use in deployment or source control.

- **Macro Menus**:
Macros can be placed into folders and run against the selected object. If you have created macros for the given object type, they appear as additional menu items or folders in the right-click menu.

- **Revert**:
Puts the selected object, and everything beneath it, back to the way it was when the model was last saved, leaving all other unsaved changes in place. Only shown for objects with [unsaved changes](xref:unsaved-changes), and for tables, display folders, table groups and the **Model** node when something beneath them has changed.

- **Restore**:
Brings back a deleted object, exactly as it was the moment before it was deleted. Only shown when right-clicking objects that were [deleted since the last save](xref:unsaved-changes#deleted-objects), which remain visible in the TOM Explorer with a struck-through name.

- **Cut / Copy / Paste / Delete**:
Standard clipboard operations. Use these to move, duplicate, or remove model objects. Deleted objects stay visible in the TOM Explorer, struck through, until the model is saved. See @unsaved-changes.

- **Properties**:
Opens the Properties pane for the selected object. Shortcut: **Alt+Enter**. Used to inspect and edit metadata, expressions, formatting and visibility settings.

### Copying and moving objects

Pasting an object (**Edit > Paste**, or **Ctrl+V**) selects the pasted object, gives it focus and scrolls it into view, so you can rename or edit it straight away. The original is left unselected.

Moving an object to another table by drag and drop, and duplicating one, both keep whatever error and warning indicators the object already carried. An expression that was invalid before the move is still marked as invalid afterwards, without needing to be edited again.

### Selecting a partition

Selecting a partition shows its expression in the **Expression Editor**. For a partition with no query expression of its own, such as a Direct Lake partition or one generated by an incremental refresh policy, the editor shows the **Data Coverage Definition Expression** where one is defined, and is empty otherwise.

### Show Info Columns
The TOM Explorer allows for toggling on additional info columns about the data model objects. This can be done with the shortcut **Ctrl+7**.
These extra info also exists in the property window, but allow for a quick view of the Object Type, Format String, Data Type, Expression and Description.
![Tom Explorer Show Hide Columns](~/content/assets/images/user-interface/TOMExplorerInfoColumns.png)

### Unsaved changes
Objects that differ from the last saved version of the model are tinted and badged: orange for edited objects, green for added objects and red for deleted objects, which also stay in the tree, struck through, until the model is saved. Tables, folders and groups that contain changed objects get a hatched fill. Deleted objects can be brought back with the right-click **Restore** option, and the **Show changes** toolbar button filters the tree down to the changed objects. See @unsaved-changes for details, including how to revert individual changes and how to adjust the indicators under **Tools > Preferences**.

![Tom Explorer Unsaved Changes](~/content/assets/images/user-interface/TOMExplorerUnsavedChanges.png)

## TOM Explorer Toolbar
The toolbar allows you to show and hide different types of objects, toggle perspectives and languages and search for specific objects in the data model.
![Tom Explorer Toolbar](~/content/assets/images/user-interface/TOMExplorerToolbar.png)

1. **Show/Hide Measures**
   Toggle the visibility of measures within tables.
   **Shortcut:** **Ctrl+1**

2. **Show/Hide Columns**
   Toggle the visibility of columns within tables.
   **Shortcut:** **Ctrl+2**

3. **Show/Hide Hierarchies**
   Toggle whether hierarchies are shown in the TOM Explorer.
   **Shortcut:** **Ctrl+3**

4. **Show/Hide Partitions**
   Controls whether partitions are visible for tables.
   **Shortcut:** **Ctrl+4**

5. **Show/Hide Calendars**
   Controls whether calendars are visible.
   **Shortcut:** **Ctrl+8**

6. **Show/Hide Display Folders**
   Enables or disables the display of folder organization within tables.
   **Shortcut:** **Ctrl+5**

7. **Group User-Defined Functions by Namespace**
   When enabled, DAX User-Defined Functions are grouped hierarchically by [namespace](xref:udfs#namespaces), rather than being shown as a flat list.

8. **Show/Hide Hidden Objects**
   Toggles whether hidden objects are shown.
   **Shortcut:** **Ctrl+6**

9. **Show/Hide Info Columns**
   Shows or hides metadata columns, such as data types or object status.
   **Shortcut:** **Ctrl+7**

10. **Show/Hide Table Groups**
    Toggle the visibility of table groups in the TOM Explorer tree. This provides quick access to the same setting found in **Tools > Preferences** without leaving the explorer.

11. **Show Changes**
    Filters the tree down to objects with [unsaved changes](xref:unsaved-changes), together with the tables, folders and groups needed to reach them. While the filter is active, the title of the view reads **TOM Explorer (Changed)**.

12. **Perspective Selector**
    Drop-down to choose a specific perspective. Only objects in the selected perspective will be shown in the TOM Explorer.

13. **Language Selector**
    Allows switching between different languages for model metadata localization.

14. **Collapse All**
    Collapses all nodes in the TOM Explorer tree view.

15. **Search Bar**
    Provides real-time filtering and navigation within the TOM Explorer. Type to search across all visible model objects.
