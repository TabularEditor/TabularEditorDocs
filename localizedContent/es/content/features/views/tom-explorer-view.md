---
uid: tom-explorer-view
title: Vista del Explorador TOM
author: Morten Lønskov
updated: 2023-02-21
applies_to:
  products:
    - product: Tabular Editor 2
      partial: true
      note: "Funciona de forma distinta a como se muestra en este artículo"
    - product: Tabular Editor 3
      editions:
        - edition: Escritorio
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Uso del Explorador TOM en Tabular Editor 3

El Explorador TOM es la ventana principal para interactuar con los objetos del modelo de datos. Los objetos como tablas, columnas, medidas, grupos de seguridad, etc. se muestran en una estructura jerárquica. Un modelo de datos tabular se representa mediante el llamado [Tabular Object Model (TOM)](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions), y los metadatos de su TOM son los que se muestran en el Explorador TOM.

El Explorador TOM consta de dos áreas principales: en primer lugar, los objetos del modelo de datos y, en segundo lugar, la barra de menús, que permite filtrar y cambiar lo que se presenta en la ventana principal.

![Explorador TOM](~/content/assets/images/user-interface/TOMExplorer.png)

<br></br>

## Objetos del modelo de datos

Puede desplegar los objetos en el Explorador TOM para ver sus elementos secundarios y seguir la jerarquía de objetos hacia los niveles inferiores. Y, si hace clic con el botón derecho en cualquier objeto, verá una lista de opciones para interactuar con ese objeto en concreto. Como puede ver a continuación, hay varias opciones que puede usar con una tabla. Con este menú, por ejemplo, puede actualizar fácilmente sus tablas y ver el estado de esa actualización en @data-refresh-view

![Interacción del Explorador Tom](~/content/assets/images/user-interface/TomExplorerRightClick.png)

El menú del botón derecho incluye los siguientes elementos, algunos de los cuales se pueden expandir para ver más acciones. El menú depende del tipo de objeto seleccionado (tabla, partición, medida, columna, etc.) y la siguiente lista no es exhaustiva para todos los tipos de objetos, pero incluye los más utilizados.

### Opciones del menú contextual de clic derecho

- **Actualizar el esquema de la tabla...**:  
  Comprueba si se han producido cambios estructurales en el Data source externo y actualiza el esquema de la tabla en consecuencia. Esto es útil cuando se han agregado, cambiado de nombre o quitado columnas en el origen.

- **Script DAX**:  
  Genera un script DAX para la tabla seleccionada y sus objetos. Abre una nueva ventana del editor de scripts donde puede revisar o editar en conjunto las definiciones de DAX.

- **Vista previa de datos**:  
  Abre el panel de vista previa de datos y muestra un ejemplo de los datos cargados en la tabla seleccionada. Útil para validar o depurar. Solo existe al hacer clic con el botón derecho en las tablas.

- **Actualizar**:  
  Despliega una selección de posibles operaciones de actualización para la tabla seleccionada. Esto solo está disponible si el modelo está conectado a un modelo en vivo, ya sea de forma independiente o en modo del área de trabajo. Esta opción solo está disponible para tablas y particiones.

- **Crear**:  
  Despliega un submenú que permite crear nuevas medidas, columnas, jerarquías, carpetas de visualización o elementos de cálculo en el objeto seleccionado. Las opciones disponibles dependen del tipo de objeto seleccionado.

- **Mover a grupo**:  
  Permite organizar la tabla en un grupo de tablas dentro del Explorador TOM para facilitar la navegación por el modelo. Esta opción solo está disponible para tablas.

- **Hacer invisible**:  
  Marca el objeto como no visible en las herramientas cliente. La tabla sigue formando parte del modelo, pero está oculta para los autores de informes. Alternativamente, utilice el atajo `Ctrl+I` para ocultar el objeto.

- **Mostrar en perspectivas**:  
  Habilita o deshabilita la inclusión de la tabla en una o más perspectivas. Las perspectivas limitan lo que los usuarios finales pueden ver en herramientas como Power BI.

- **Cambio de nombre por lotes**: Al seleccionar más de un objeto, puede cambiarles el nombre por lotes mediante sustitución de cadenas o expresiones regulares. El atajo para cambiar el nombre en lote es `F2`.

- **Cambiar nombre en lote a elementos secundarios...**:  
  Permite cambiar el nombre de forma masiva a todos los objetos secundarios de la tabla o carpeta de visualización mediante reglas de expresiones regulares o de reemplazo de cadenas. También se puede acceder con el atajo `Shift+F2`.

- **Duplicar**:  
  Crea una copia de la tabla seleccionada, incluidas todas sus columnas, medidas y particiones. También existe para todos los demás objetos del Explorador TOM.

- **Marcar como tabla de fechas...**:  
  Marca la tabla como tabla de fechas, habilitando las funciones de inteligencia temporal. Requiere que la tabla contenga una columna de fecha válida.

- **Mostrar dependencias**:  
  Visualiza las dependencias entre la tabla seleccionada y otros objetos del modelo. También se puede acceder mediante el método abreviado `Shift+F12`.

- **Exportar script**:  
  Exporta los objetos seleccionados como un script TMSL o TMDL para usarlo en la implementación o el control de código fuente.
  Exporta los objetos seleccionados como un script TMSL o TMDL para usarlo en la implementación o el control de código fuente.

- **Menús de macros**:  
  Las macros se pueden colocar en carpetas y ejecutar sobre el objeto seleccionado. En el ejemplo anterior, el usuario tiene una carpeta de Modelado y análisis para scripts de macros aplicados a objetos de tabla.

- **Cortar / Copiar / Pegar / Eliminar**:  
  Operaciones estándar del portapapeles. Úsalas para mover, duplicar o quitar objetos del modelo.

- **Propiedades**:  
  Abre el panel de Propiedades para el objeto seleccionado. Método abreviado: `Alt+Enter`. Se usa para inspeccionar y editar metadatos, expresiones, formato y configuración de visibilidad.

### Mostrar columnas de información

El Explorador TOM permite activar o desactivar columnas de información adicional sobre los objetos del modelo de datos. Puedes hacerlo con el método abreviado `CTRL+7`.
Esta información adicional también está disponible en la ventana de propiedades, pero permite ver rápidamente el tipo de objeto, la cadena de formato, el tipo de datos, la expresión y la descripción.
![Explorador TOM Mostrar/Ocultar columnas](~/content/assets/images/user-interface/TOMExplorerInfoColumns.png)

## Barra de herramientas del Explorador TOM

La barra de herramientas te permite mostrar y ocultar distintos tipos de objetos, alternar perspectivas e idiomas, así como buscar objetos específicos en el modelo de datos.
![Barra de herramientas del Explorador TOM](~/content/assets/images/user-interface/TOMExplorerToolbar.png)

1. **Mostrar/Ocultar medidas**  
   Alterna la visibilidad de las medidas dentro de las tablas.  
   **Método abreviado:** `Ctrl+1`

2. **Mostrar/Ocultar columnas**  
   Alterna la visibilidad de las columnas dentro de las tablas.  
   **Atajo:** `Ctrl+2`

3. **Mostrar/ocultar jerarquías**  
   Activa o desactiva la visualización de las jerarquías en el Explorador TOM.  
   **Atajo:** `Ctrl+3`

4. **Mostrar/ocultar particiones**  
   Controla si las particiones son visibles en las tablas.  
   **Atajo:** `Ctrl+4`

5. **Mostrar/ocultar calendarios**  
   Controla si los calendarios son visibles.  
   **Atajo:** `Ctrl+4`

6. **Mostrar/ocultar carpetas de visualización**

7. **Mostrar/ocultar calendarios**  
   Controla si los calendarios son visibles.  
   **Atajo:** `Ctrl+4`

8. **Mostrar/ocultar carpetas de visualización**  
   Activa o desactiva la organización por carpetas de visualización dentro de las tablas.  
   **Atajo:** `Ctrl+5`

9. \*\*Agrupar las funciones DAX definidas por el usuario por espacio de nombres
   Cuando está habilitado, las funciones DAX definidas por el usuario se agrupan jerárquicamente por [espacio de nombres](xref:udfs#namespaces), en lugar de mostrarse como una lista plana.

10. **Mostrar/ocultar objetos ocultos**

11. \*\*Agrupar las funciones DAX definidas por el usuario por espacio de nombres
    Cuando está habilitado, las funciones DAX definidas por el usuario se agrupan jerárquicamente por [espacio de nombres](xref:udfs#namespaces), en lugar de mostrarse como una lista plana.

12. **Mostrar/ocultar objetos ocultos**  
    Activa o desactiva la visualización de los objetos ocultos.  
    **Atajo:** `Ctrl+6`

13. **Mostrar/ocultar columnas de información**

14. **Mostrar/ocultar columnas de información**  
    Muestra u oculta columnas de metadatos, como tipos de datos o el estado del objeto.  
    **Atajo:** `Ctrl+7`

15. **Selector de perspectiva**

16. **Selector de perspectiva**  
    Lista desplegable para elegir una perspectiva concreta. Solo se mostrarán en el Explorador TOM los objetos de la perspectiva seleccionada.

17. **Selector de idioma**

18. **Selector de idioma**  
    Permite cambiar entre distintos idiomas para la localización de los metadatos del modelo.

19. **Contraer todo**  
    Contrae todos los nodos en la vista de árbol del Explorador TOM.

20. **Barra de búsqueda**

21. **Contraer todo**  
    Contrae todos los nodos en la vista de árbol del Explorador TOM.

22. **Barra de búsqueda**  
    Ofrece filtrado y navegación en tiempo real en el Explorador TOM. Escribe para buscar en todos los objetos visibles del modelo.