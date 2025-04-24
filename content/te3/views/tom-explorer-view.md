---
uid: tom-explorer-view
title: TOM Explorer view
author: Morten Lønskov
updated: 2023-02-21
applies_to:
  editions:
    - edition: Desktop
    - edition: Business
    - edition: Enterprise
---
# Using the TOM Explorer in Tabular Editor 3
The TOM Explorer is your main window for interacting with the objects of your data mode. Objects such has tables, columns, measures, security groups etc. are all displayed in a hierarchical structure. A Tabular data model is represented by the so called [Tabular Object Model (TOM)](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) and it is the metadata of your TOM that is displayed in the TOM Explorer. 

The TOM Explorer consists of two main areas, firstly the data model objects and secondly the menu bar that allows for filtering and changing what is presented in the main window. 

![Tom Explorer](~/content/assets/images/user-interface/TOMExplorer.png)

<br></br>

## Data Model Objects
You can fold out objects in the TOM Explorer to see their children and follow the hierarchy of objects downwards. And if you right click on any object you will be given a list of options to interact with that specific object. As you can see bellow there are several options that you can use with a table. It is with this menu that you for example can easily refresh your tables and see the status of that refresh in the @data-refresh-view

![Tom Explorer Interaction](~/content/assets/images/user-interface/TomExplorerRightClick.png) 

The right click menu has the following items some of which can be expanded for more actions. The menu depends on the object type chosen (Table, partition, measure, column etc.) and the list below is not exhaustive for all types of objects but contains those most used. 

### Options in Right-click menu
- **Update table schema...**:  
Checks for structural changes in the external data source and updates the table’s schema accordingly. This is useful when columns have been added, renamed, or removed in the source.

- **Script DAX**:  
Generates a DAX script for the selected table and its objects. Opens a new script editor window where you can review or edit DAX definitions collectively.

- **Preview data**:  
Opens the data preview pane displaying a sample of the data loaded into the selected table. Useful for validation or debugging. Only exists when right clicking tables.

- **Refresh**:  
Expands to a selection of possible refresh operation for the selected table. This is available only if the model is connected to live model either stand alone or in workspace mode. This option is only available on tables and partitions.

- **Create**:  
Expands to a submenu allowing the creation of new measures, columns, hierarchies, display folders or calculation items under the selected object. The available options depends on the object type selected.

- **Move to group**:  
Allows you to organize the table into a Table group within the TOM Explorer for easier model navigation. This option is only available for tables.

- **Make invisible**:  
Marks the object as not visible in client tools. The table remains part of the model but is hidden from report authors. Alternative use the shortcut `Ctrl+I` to hide the object.  

- **Shown in perspectives**:  
Enables or disables the table’s inclusion in one or more perspectives. Perspectives limit what end-users can see in tools like Power BI.

- **Batch rename**: When selecting more than one object you can batch rename those objects using string replacement or regex. The shortcut for batch rename is `F2`.

- **Batch rename children...**:  
Enables bulk renaming of all child objects under the table or display folder using regex or string replacement rules. Can also be accessed with the shortcut `Shift+F2`.

- **Duplicate**:  
Creates a copy of the selected table, including all its columns, measures, and partitions. Also exists for all other objects in the TOM Explorer.

- **Mark as date table...**:  
Marks the table as a date table, enabling time intelligence features. Requires that the table contains a valid date column.

- **Show dependencies**:  
Visualizes dependencies between the selected table and other model objects. Can also be accessed via shortcut `Shift+F12`.

- **Export script**:  
Exports the selected object as a TMSL or TMDL script for use in deployment or source control.

- **Macro Menus**:  
Macros can be placed into folders and run against the selected object. In the example above the user has a Modelling and Analysis folder for Macro scripts on table objects.

- **Cut / Copy / Paste / Delete**:  
Standard clipboard operations. Use these to move, duplicate, or remove model objects.

- **Properties**:  
Opens the Properties pane for the selected object. Shortcut: `Alt+Enter`. Used to inspect and edit metadata, expressions, formatting, and visibility settings.

> [!IMPORTANT]
> In Tabular Editor 3 Desktop Edition some options are disabled and greyed-out. This is due to the limitations of using Tabular Editor has an external tool. For more information see @desktop-limitations 

### Show Info Columns
The TOM Explorer allows for toggling on additional info columns about the data model objects. This can be done with the short cut `CTRL+7`
These extra info also exists in the property window, but allow for a quick view of the Object Type, Format String, Data Type, Expression and Description.
![Tom Explorer Show Hide Coloumns](~/content/assets/images/user-interface/TOMExplorerInfoColumns.png)

## TOM Explorer Toolbar
The toolbar allow you to show and hide different types of objects, toggling perspectives and languages ans well as searching for specific objects in the data model.
![Tom Explorer Toolbar](~/content/assets/images/user-interface/TOMExplorerToolbar.png)

1. **Show/Hide Measures**  
   Toggle the visibility of measures within tables.  
   **Shortcut:** `Ctrl+1`

2. **Show/Hide Columns**  
   Toggle the visibility of columns within tables.  
   **Shortcut:** `Ctrl+2`

3. **Show/Hide Hierarchies**  
   Toggle whether hierarchies are shown in the TOM Explorer.  
   **Shortcut:** `Ctrl+3`

4. **Show/Hide Partitions**  
   Controls whether partitions are visible for tables.  
   **Shortcut:** `Ctrl+4`

5. **Show/Hide Display Folders**  
   Enables or disables the display of folder organization within tables.  
   **Shortcut:** `Ctrl+5`

6. **Show/Hide Hidden Objects**  
   Toggles whether hidden objects are shown.  
   **Shortcut:** `Ctrl+6`

7. **Show/Hide Info Columns**  
   Shows or hides metadata columns, such as data types or object status.  
   **Shortcut:** `Ctrl+7`

8. **Perspective Selector**  
   Drop-down to choose a specific perspective. Only objects in the selected perspective will be shown in the TOM Explorer.

9. **Language Selector**  
   Allows switching between different languages for model metadata localization.

10. **Search Bar**  
   Provides real-time filtering and navigation within the TOM Explorer. Type to search across all visible model objects.
