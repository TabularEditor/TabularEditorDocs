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

El Explorador TOM es tu ventana principal para interactuar con los objetos de tu Data model. Objetos como tablas, columnas, medidas, grupos de seguridad, etc. se muestran en una estructura jerárquica. Un modelo de datos tabular se representa mediante el llamado [Tabular Object Model (TOM)](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions), y los metadatos de su TOM son los que se muestran en el Explorador TOM.

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
  Marks the object as not visible in client tools. La tabla sigue formando parte del modelo, pero está oculta para los autores de informes. Como alternativa, usa el atajo **Ctrl+I** para ocultar el objeto.

- **Shown in perspectives**:
  Enables or disables the table's inclusion in one or more perspectives. Las perspectivas limitan lo que los usuarios finales pueden ver en herramientas como Power BI.

- **Cambio de nombre por lotes**: Al seleccionar más de un objeto, puede cambiarles el nombre por lotes mediante sustitución de cadenas o expresiones regulares. El atajo para renombrar por lotes es **F2**.

- **Batch rename children...**:
  Enables bulk renaming of all child objects under the table or display folder using regex or string replacement rules. También se puede acceder mediante el atajo **Shift+F2**.

- **Duplicate**:
  Creates a copy of the selected table, including all its columns, measures and partitions. También existe para todos los demás objetos del Explorador TOM.

- **Mark as date table...**:
  Marks the table as a date table, enabling time intelligence features. Requiere que la tabla contenga una columna de fecha válida.

- **Show dependencies**:
  Visualizes dependencies between the selected table and other model objects. También se puede acceder mediante el atajo **Shift+F12**.

- **Export script**:
  Exports the selected objects as a TMSL or TMDL script for use in deployment or source control.

- **Macro Menus**:
  Macros can be placed into folders and run against the selected object. En el ejemplo anterior, el usuario tiene una carpeta de Modelado y análisis para scripts de macros aplicados a objetos de tabla.

- **Cut / Copy / Paste / Delete**:
  Standard clipboard operations. Úsalas para mover, duplicar o quitar objetos del modelo.

- **Properties**:
  Opens the Properties pane for the selected object. Atajo: **Alt+Enter**. Úsalo para inspeccionar y editar metadatos, expresiones, formato y configuración de visibilidad.

### Mostrar columnas de información

El Explorador TOM permite activar o desactivar columnas de información adicional sobre los objetos del modelo de datos. Puedes hacerlo con el atajo **Ctrl+7**.
Esta información adicional también está disponible en la ventana de propiedades, pero permite ver rápidamente el tipo de objeto, la cadena de formato, el tipo de datos, la expresión y la descripción.
![Explorador TOM: mostrar/ocultar columnas](~/content/assets/images/user-interface/TOMExplorerInfoColumns.png)

## Barra de herramientas del Explorador TOM

La barra de herramientas te permite mostrar y ocultar distintos tipos de objetos, alternar perspectivas e idiomas y buscar objetos específicos en el Data model.
![Barra de herramientas del Explorador TOM](~/content/assets/images/user-interface/TOMExplorerToolbar.png)

1. **Mostrar/Ocultar medidas**
   Alterna la visibilidad de las medidas dentro de las tablas.
   **Atajo:** **Ctrl+1**

2. **Mostrar/Ocultar columnas**
   Alterna la visibilidad de las columnas dentro de las tablas.
   **Atajo:** **Ctrl+2**

3. **Mostrar/Ocultar jerarquías**
   Alterna la visualización de las jerarquías en el Explorador TOM.
   **Atajo:** **Ctrl+3**

4. **Mostrar/Ocultar particiones**
   Controla si las particiones son visibles en las tablas.
   **Atajo:** **Ctrl+4**

5. **Mostrar/Ocultar calendarios**
   Controla si los calendarios son visibles.
   **Atajo:** **Ctrl+8**

6. **Mostrar/Ocultar carpetas de visualización**
   Activa o desactiva la visualización de la organización por carpetas dentro de las tablas.
   **Atajo:** **Ctrl+5**

7. **Agrupar funciones definidas por el usuario por espacio de nombres**
   Cuando está habilitado, las funciones DAX definidas por el usuario se agrupan jerárquicamente por [espacio de nombres](xref:udfs#namespaces), en lugar de mostrarse como una lista plana.

8. **Mostrar/ocultar grupos de tablas**
   Activa o desactiva la visibilidad de los grupos de tablas en el árbol del Explorador TOM. Proporciona acceso rápido a la misma preferencia que se encuentra en **Herramientas > Preferencias** sin salir del explorador.

9. **Mostrar/ocultar objetos ocultos**
   Activa o desactiva si se muestran los objetos ocultos.
   **Acceso directo:** **Ctrl+6**

10. **Mostrar/ocultar columnas de información**
    Muestra u oculta columnas de metadatos, como los tipos de datos o el estado de los objetos.
    **Acceso directo:** **Ctrl+7**

11. **Selector de perspectiva**
    Lista desplegable para seleccionar una perspectiva específica. Solo se mostrarán en el Explorador TOM los objetos de la perspectiva seleccionada.

12. **Selector de idioma**
    Permite cambiar entre diferentes idiomas para la localización de los metadatos del modelo.

13. **Contraer todo**
    Contrae todos los nodos de la vista en árbol del Explorador TOM.

14. **Barra de búsqueda**
    Proporciona filtrado y navegación en tiempo real dentro del Explorador TOM. Escribe para buscar en todos los objetos visibles del modelo.
