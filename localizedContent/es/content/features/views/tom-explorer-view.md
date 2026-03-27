---
uid: tom-explorer-view
title: Vista del Explorador TOM
author: Morten Lønskov
updated: 2026-03-19
applies_to:
  products:
    - product: Tabular Editor 2
      partial: true
      note: "Funciona de forma distinta a como se muestra en este artículo"
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Uso del Explorador TOM en Tabular Editor 3

The TOM Explorer is your main window for interacting with the objects of your data model. Objects such as tables, columns, measures, security groups etc. are all displayed in a hierarchical structure. Un modelo de datos tabular se representa mediante el llamado [Tabular Object Model (TOM)](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions), y los metadatos de su TOM son los que se muestran en el Explorador TOM.

El Explorador TOM consta de dos áreas principales: en primer lugar, los objetos del modelo de datos y, en segundo lugar, la barra de menús, que permite filtrar y cambiar lo que se presenta en la ventana principal.

![Explorador TOM](~/content/assets/images/user-interface/TOMExplorer.png)

## Objetos del modelo de datos

Puede desplegar los objetos en el Explorador TOM para ver sus elementos secundarios y seguir la jerarquía de objetos hacia los niveles inferiores. Y, si hace clic con el botón derecho en cualquier objeto, verá una lista de opciones para interactuar con ese objeto en concreto. Como puede ver a continuación, hay varias opciones que puede usar con una tabla. Con este menú, por ejemplo, puede actualizar fácilmente sus tablas y ver el estado de esa actualización en @data-refresh-view

![Interacción del Explorador Tom](~/content/assets/images/user-interface/TomExplorerRightClick.png)

El menú del botón derecho incluye los siguientes elementos, algunos de los cuales se pueden expandir para ver más acciones. El menú depende del tipo de objeto seleccionado (tabla, partición, medida, columna, etc.) y la siguiente lista no es exhaustiva para todos los tipos de objetos, pero incluye los más utilizados.

### Opciones del menú contextual de clic derecho

- **Update table schema...**:
  Checks for structural changes in the external data source and updates the table's schema accordingly. Esto es útil cuando se han agregado, cambiado de nombre o quitado columnas en el origen.

- **Script DAX**:
  Generates a DAX script for the selected table and its objects. Abre una nueva ventana del editor de scripts donde puede revisar o editar en conjunto las definiciones de DAX.

- **Preview data**:
  Opens the data preview pane displaying a sample of the data loaded into the selected table. Útil para validar o depurar. Solo existe al hacer clic con el botón derecho en las tablas.

- **Refresh**:
  Expands to a selection of possible refresh operation for the selected table. Esto solo está disponible si el modelo está conectado a un modelo en vivo, ya sea de forma independiente o en modo del área de trabajo. Esta opción solo está disponible para tablas y particiones.

- **Create**:
  Expands to a submenu allowing the creation of new measures, columns, hierarchies, display folders or calculation items under the selected object. Las opciones disponibles dependen del tipo de objeto seleccionado.

- **Move to group**:
  Allows you to organize the table into a Table group within the TOM Explorer for easier model navigation. Esta opción solo está disponible para tablas.

- **Make invisible**:
  Marks the object as not visible in client tools. La tabla sigue formando parte del modelo, pero está oculta para los autores de informes. Alternative use the shortcut **Ctrl+I** to hide the object.

- **Shown in perspectives**:
  Enables or disables the table's inclusion in one or more perspectives. Las perspectivas limitan lo que los usuarios finales pueden ver en herramientas como Power BI.

- **Cambio de nombre por lotes**: Al seleccionar más de un objeto, puede cambiarles el nombre por lotes mediante sustitución de cadenas o expresiones regulares. The shortcut for batch rename is **F2**.

- **Batch rename children...**:
  Enables bulk renaming of all child objects under the table or display folder using regex or string replacement rules. Can also be accessed with the shortcut **Shift+F2**.

- **Duplicate**:
  Creates a copy of the selected table, including all its columns, measures and partitions. También existe para todos los demás objetos del Explorador TOM.

- **Mark as date table...**:
  Marks the table as a date table, enabling time intelligence features. Requiere que la tabla contenga una columna de fecha válida.

- **Show dependencies**:
  Visualizes dependencies between the selected table and other model objects. Can also be accessed via shortcut **Shift+F12**.

- **Export script**:
  Exports the selected objects as a TMSL or TMDL script for use in deployment or source control.

- **Macro Menus**:
  Macros can be placed into folders and run against the selected object. En el ejemplo anterior, el usuario tiene una carpeta de Modelado y análisis para scripts de macros aplicados a objetos de tabla.

- **Cut / Copy / Paste / Delete**:
  Standard clipboard operations. Úsalas para mover, duplicar o quitar objetos del modelo.

- **Properties**:
  Opens the Properties pane for the selected object. Shortcut: **Alt+Enter**. Used to inspect and edit metadata, expressions, formatting and visibility settings.

### Mostrar columnas de información

El Explorador TOM permite activar o desactivar columnas de información adicional sobre los objetos del modelo de datos. This can be done with the shortcut **Ctrl+7**.
These extra info also exists in the property window, but allow for a quick view of the Object Type, Format String, Data Type, Expression and Description.
![Tom Explorer Show Hide Columns](~/content/assets/images/user-interface/TOMExplorerInfoColumns.png)

## Barra de herramientas del Explorador TOM

The toolbar allows you to show and hide different types of objects, toggle perspectives and languages and search for specific objects in the data model.
![Barra de herramientas del Explorador TOM](~/content/assets/images/user-interface/TOMExplorerToolbar.png)

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

8. **Show/Hide Table Groups**
   Toggle the visibility of table groups in the TOM Explorer tree. This provides quick access to the same setting found in **Tools > Preferences** without leaving the explorer.

9. **Show/Hide Hidden Objects**
   Toggles whether hidden objects are shown.
   **Shortcut:** **Ctrl+6**

10. **Show/Hide Info Columns**
    Shows or hides metadata columns, such as data types or object status.
    **Shortcut:** **Ctrl+7**

11. **Perspective Selector**
    Drop-down to choose a specific perspective. Solo se mostrarán en el Explorador TOM los objetos de la perspectiva seleccionada.

12. **Language Selector**
    Allows switching between different languages for model metadata localization.

13. **Collapse All**
    Collapses all nodes in the TOM Explorer tree view.

14. **Search Bar**
    Provides real-time filtering and navigation within the TOM Explorer. Escribe para buscar en todos los objetos visibles del modelo.
