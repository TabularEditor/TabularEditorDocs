---
uid: user-interface
title: Interfaz de usuario básica
author: Daniel Otykier
updated: 2026-09-14
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Conociendo la interfaz de usuario de Tabular Editor 3

Este artículo describe la interfaz de usuario de Tabular Editor 3.

## Elementos básicos de la interfaz de usuario

La primera vez que inicies Tabular Editor 3 y cargues un modelo semántico, se te mostrará una interfaz como la que aparece en la captura de pantalla siguiente.

![Interfaz de usuario básica](~/content/assets/images/basic-ui.png)

1. **Barra de título**: Muestra el nombre del archivo cargado actualmente y, si está conectado, la base de datos de Analysis Services o el Dataset de Power BI.
2. **Barra de menús**: La barra de menús te da acceso a todas las funciones de Tabular Editor 3. Consulta [Menús](#menus) para ver una guía detallada de todos los elementos del menú.
3. **Barras de herramientas**: Las barras de herramientas te dan acceso rápido a las funciones más utilizadas. También puedes acceder desde los menús a todas las funciones disponibles en la barra de herramientas. Puedes personalizar las barras de herramientas y sus botones en **Herramientas > Personalizar...**
4. **Vista del Explorador TOM**: Una vista jerárquica de tu modelo de datos, con todos los objetos disponibles.  de los metadatos del [Tabular Object Model (TOM)](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) que representan tu modelo de datos. Los botones de alternancia de la parte superior te permiten filtrar qué objetos se muestran. El cuadro de búsqueda te permite filtrar objetos por nombre.
5. **Editor de expresiones**: El editor de expresiones ofrece una forma rápida de editar cualquier expresión DAX, SQL o M del objeto seleccionado actualmente en el Explorador TOM. Si cierras el editor de expresiones, puedes volver a abrirlo haciendo doble clic en un objeto del Explorador TOM. El menú desplegable de la parte superior te permite cambiar entre distintas propiedades de expresión, en caso de que el objeto seleccionado actualmente tenga más de una (por ejemplo, los KPI tienen Expresiones de objetivo, Expresiones de estado y Expresiones de tendencia, que son 3 expresiones DAX diferentes que pertenecen al mismo objeto KPI).
6. **Vista de propiedades**: Una vista detallada de todas las propiedades TOM disponibles para el/los objeto(s) seleccionados actualmente en el Explorador TOM. La mayoría de las propiedades se pueden editar desde la cuadrícula, incluso cuando hay varios objetos seleccionados. Algunas propiedades (como "Format String", "Connection String" y "Miembros de rol") tienen cuadros de diálogo emergentes o editores de colecciones que puedes abrir haciendo clic en el botón de puntos suspensivos dentro de la celda del valor de la propiedad.
7. **Vista de mensajes**: Tabular Editor 3 analiza continuamente las expresiones DAX de tu modelo para detectar errores semánticos. Cualquier error de este tipo se muestra aquí. Además, los mensajes que se muestran en esta vista pueden provenir de scripts de C# o de mensajes de error generados por Analysis Services.
8. **Barra de estado**: La barra de estado ofrece diversa información contextual sobre la selección actual, los hallazgos de Best Practice Analyzer, etc. When the [MCP server](xref:mcp-server) is available, an indicator at the right-hand end reads **MCP Started** or **MCP Stopped**, with the address the server is listening on in its tooltip. Click it to open the MCP Server dialog, or right-click it to start and stop the server, copy a registration configuration for your agent or jump to the preferences page.

Hay varias vistas adicionales disponibles, con distintos propósitos. Más información en la sección del [menú Ver](#view).

# Personalización de la interfaz de usuario

Todos los elementos de la interfaz de usuario se pueden redimensionar o reorganizar para adaptarlos a tus necesidades. Incluso puedes arrastrar vistas individuales fuera de la vista principal, dividiendo así una instancia de Tabular Editor 3 entre varios monitores. Tabular Editor 3 guardará la personalización al cerrar la aplicación y la cargará automáticamente la próxima vez que se inicie.

### Elegir un diseño diferente

Para restablecer la aplicación al diseño predeterminado, elige la opción **Ventana > Diseño predeterminado**. Los usuarios de Tabular Editor 2.x pueden preferir la opción **Ventana > Diseño clásico**, que coloca el Explorador TOM en el lado izquierdo de la pantalla y la vista de propiedades debajo del Editor de expresiones.

Use the **Window > Capture Layout** option to save a customized layout such that it will become available as a new layout option within the Window menu, allowing you to quickly switch back and forth between different layouts. Use the **Window > Layouts...** option to bring up a list of all available layouts, allowing you to apply, load, remove and save layouts. Al guardar un diseño en disco, el resultado es un archivo .xml que puedes compartir con otros usuarios de Tabular Editor 3.

![Administrar diseños](~/content/assets/images/manage-layouts.png)

### Opciones de acoplamiento de ventanas

Al reorganizar vistas y documentos en Tabular Editor 3, puedes elegir acoplar ventanas en distintas áreas de la interfaz. Al arrastrar una ventana a una nueva posición, aparecerán indicadores de acoplamiento que te mostrarán las ubicaciones de acoplamiento disponibles.

![Opciones de acoplamiento de ventanas](~/content/assets/images/window-docking-options.png)

Hay dos formas principales de acoplar ventanas, cada una con un propósito diferente:

**Acoplamiento como pestaña de documento (indicador central)**: Cuando arrastras una ventana al indicador de acoplamiento central, se colocará en el área principal de documentos. Las ventanas acopladas de esta forma se convierten en pestañas de documento que:

- Can be cycled through using **Ctrl+Tab**
- Se muestran en el área principal de trabajo junto con otros documentos, como consultas DAX, scripts y diagramas
- No admiten la función de ocultación automática

**Acoplamiento como ventana de herramientas (indicadores de borde)**: Cuando arrastras una ventana a los indicadores de acoplamiento de la izquierda, derecha, arriba o abajo, se acoplará como una ventana de herramientas. Las ventanas de herramientas:

- No son accesibles mediante **Ctrl+Tab**
- Muestran un icono de chincheta que permite la ocultación automática (la ventana se contrae cuando no se está usando)
- Se comportan de forma similar a otras ventanas de herramientas, como el Explorador TOM y la vista de mensajes
- Se pueden acoplar en varias posiciones alrededor del área principal de documentos

> [!TIP]
> El tamaño de una ventana acoplada lo determina el espacio disponible en el área en la que decidas acoplarla, no la opción de acoplamiento en sí. Puedes cambiar el tamaño de las ventanas arrastrando los separadores entre ellas.

### Cambiar temas y paletas

Puedes cambiar el aspecto visual de Tabular Editor 3 eligiendo un tema o una paleta diferentes. Tabular Editor 3 ships with five different themes (sometimes called "skins"), available through the **Window > Theme** menu:

- Basic y Bezier (basados en vectores, funcionan bien en pantallas high-DPI)
- Blue, Dark and Light (raster based, not recommended for high-DPI displays)

For the vector based themes (Basic and Bezier), use the **Window > Default palette** menu item to change the colors used by the theme.

![Palettes](~/content/assets/images/palettes.png)

# Menús

La siguiente sección describe los menús de Tabular Editor 3 con más detalle.

En la siguiente sección usamos el término **Documento activo** para indicar que el cursor está dentro de un documento, como el Editor de expresiones o la pestaña "Script DAX 1" de la captura de pantalla siguiente. Algunos atajos de teclado y elementos de menú se comportan de forma diferente dependiendo de si hay o no un documento activo, y de qué tipo de documento esté activo.

> [!NOTE]
> Los menús y las barras de herramientas están bloqueados de forma predeterminada para evitar cambios de posición accidentales. Para desbloquearlos, ve a **Herramientas > Personalizar... > Opciones** y desmarca la opción **Bloquear menús y barras de herramientas**

![Active Document](~/content/assets/images/active-document.png)

## Archivo

El menú **Archivo** contiene principalmente elementos de menú para cargar y guardar metadatos del modelo, así como archivos y documentos auxiliares.

![File Menu](~/content/assets/images/file-menu.png)

- **Nuevo**: Abre un submenú que te permite crear un Data model nuevo y en blanco (Ctrl+N) o crear varios [archivos auxiliares](xref:supported-files#supported-file-types), como una nueva Consulta DAX o un nuevo Script DAX (archivos de texto) o un diagrama del Data model (archivo JSON). Los archivos auxiliares (con la excepción de los C# Scripts) solo se pueden crear cuando ya hay un modelo cargado en Tabular Editor.

  ![File Menu New](~/content/assets/images/file-menu-new.png)

> [!IMPORTANT]
> La opción **Nuevo > Modelo...** no está disponible en la Edición de escritorio de Tabular Editor 3, ya que esta edición solo puede usarse como herramienta externa para Power BI Desktop. [Más información](xref:editions).

- **Abrir**: Abre un submenú con opciones para cargar un Data model desde varias fuentes, así como una opción para cargar cualquier otro tipo de archivo. Los elementos del submenú son:

  ![File Menu Open](~/content/assets/images/file-menu-open.png)

  - **Modelo desde archivo...** Abre los metadatos del modelo desde un archivo, como un .bim o .pbit.
  - **Modelo desde BD...** Especifique los detalles de conexión XMLA de Analysis Services o Power BI, o conéctese a una instancia local de Analysis Services (como el servidor de Workspace Integrada de Visual Studio o Power BI Desktop), para cargar los metadatos del modelo desde un modelo tabular que ya se ha implementado.
  - **Modelo desde carpeta...** Abre los metadatos del modelo desde una estructura de carpetas que se guardó previamente con cualquier versión de Tabular Editor.
  - **Archivo...** muestra un cuadro de diálogo que permite abrir cualquier tipo de archivo compatible con Tabular Editor 3, según la extensión del nombre del archivo. Consulta [Tipos de archivo compatibles](xref:supported-files) para obtener más información.
  - **Import from Metric View YAML...** Imports model metadata from a Databricks Metric View YAML file.

    ![Tipos de archivo compatibles](~/content/assets/images/supported-file-types.png)

> [!IMPORTANT]
> En Tabular Editor 3 Edición de escritorio, las opciones **Open > Model from file...** y **Open > Model from folder...** no están disponibles y el cuadro de diálogo **Open > File...** solo permite abrir [archivos compatibles](xref:supported-files#supported-file-types), no archivos que contengan metadatos.

- **Revertir**: Esta opción te permite volver a cargar los metadatos del modelo desde el origen, descartando cualquier cambio realizado en Tabular Editor que aún no se haya guardado. Esta opción resulta útil cuando Tabular Editor 3 se usa como una herramienta externa para Power BI Desktop y se realiza un cambio en Power BI Desktop mientras Tabular Editor 3 está conectado. Al elegir **Revertir**, Tabular Editor 3 puede volver a cargar los metadatos del modelo desde Power BI Desktop sin tener que reconectarse. If you loaded the model from a file or a folder you rarely need this command, because Tabular Editor reloads the model by itself when those files change on disk. See [Auto-reload from disk](xref:auto-reload).
- **Cerrar documento** (Ctrl+W): Cierra el documento o panel activo en el área principal, como una Consulta DAX, un C# Script, un diagrama del modelo de datos o cualquier otra vista que tenga el foco. Si el documento tiene cambios sin guardar, Tabular Editor te pedirá que los guardes antes de cerrar. Este comando tiene en cuenta el contexto y cerrará el elemento que esté activo actualmente en el área de trabajo principal.
- **Cerrar modelo**: Descarga de Tabular Editor los metadatos del modelo actualmente cargado. Si has realizado cambios en los metadatos, Tabular Editor te pedirá que los guardes antes de cerrar.
- **Guardar**: Guarda el documento activo en el archivo de origen. Si no hay ningún documento activo, esta opción guarda los metadatos del modelo en el origen, que puede ser un archivo Model.bim, un archivo Database.json (estructura de carpetas), una instancia conectada de Analysis Services (incluido Power BI Desktop) o el punto de conexión XMLA de Power BI.
- **Guardar como...**: Te permite guardar el documento activo como un archivo nuevo. Si no hay ningún documento activo, te permite guardar los metadatos del modelo como un archivo nuevo en formato .bim (basado en JSON).
- **Guardar en carpeta...**: Te permite guardar los metadatos del modelo como una [estructura de carpetas](xref:save-to-folder).
- **Guardar todo**: Guarda a la vez todos los documentos y metadatos del modelo que estén sin guardar.
- **Archivos recientes**: Muestra una lista de archivos auxiliares usados recientemente, para que puedas volver a abrirlos rápidamente.
- **Modelos tabulares recientes**: Muestra una lista de archivos o carpetas de metadatos de modelos usados recientemente, lo que te permite volver a cargar rápidamente los metadatos del modelo desde uno de ellos.

> [!IMPORTANT]
> En Tabular Editor 3 Edición de escritorio, las opciones **Guardar en carpeta** y **Modelos tabulares recientes** están deshabilitadas. Además, la opción **Guardar como** solo está habilitada para [archivos auxiliares](xref:supported-files#supported-file-types).

- **Salir**: Cierra la aplicación Tabular Editor 3. Antes de cerrar la aplicación, se te pedirá que guardes cualquier archivo sin guardar o los metadatos del modelo que no se hayan guardado.

## Editar

El menú **Editar** contiene los elementos de menú estándar de las aplicaciones de Windows para editar un documento o realizar cambios en los metadatos del modelo cargado actualmente.

![Menú Editar](~/content/assets/images/edit-menu.png)

- **Deshacer**: Esta opción deshace el último cambio realizado en los metadatos del modelo. Cuando no hay ningún documento activo, el conocido acceso directo CTRL+Z se asigna a esta opción.
- **Rehacer**: Esta opción rehace el último deshacer aplicado a los metadatos del modelo. Cuando no hay ningún documento activo, el conocido acceso directo CTRL+Y se asigna a esta opción.
- **Reemplazar**: Muestra el cuadro de diálogo "Buscar y reemplazar" con la pestaña "Reemplazar" seleccionada. [Más información](xref:find-replace#replace).
- **Buscar**: Muestra el cuadro de diálogo "Buscar y reemplazar" con la pestaña "Buscar" seleccionada. [Más información](xref:find-replace#find).
- **Cortar / Copiar / Pegar**: Son las conocidas operaciones de edición de Windows. Si hay un documento activo, se aplican a la selección de texto dentro de ese documento. En caso contrario, estas opciones se pueden usar para manipular objetos en el Explorador TOM. Por ejemplo, puede duplicar varias medidas manteniendo pulsada la tecla SHIFT o CTRL mientras selecciona las medidas en el Explorador TOM y, después, pulsando CTRL+C y luego CTRL+V.
- **Eliminar**: Elimina el texto seleccionado en el documento activo o el/los objeto(s) seleccionados actualmente en el Explorador TOM si no hay ningún documento activo.

> [!NOTE]
> Por lo general, Tabular Editor solo solicita confirmación al eliminar objetos cuando hay varios objetos seleccionados o cuando existen dependencias del/de los objeto(s) que se están eliminando. La eliminación de objetos se puede deshacer mediante la opción **Deshacer** (CTRL+Z).

- **Seleccionar todo**: Selecciona todo el texto del documento activo o todos los objetos que pertenecen al mismo elemento padre en el Explorador TOM.
- **Code Assist**: Esta opción está disponible cuando se edita código DAX. Proporciona un acceso directo a varias funciones de Code Assist relevantes para la edición de código DAX. Consulte [editor de DAX](xref:dax-editor#code-assist-features) para obtener más información.
- **Word Wrap**: Toggles word wrapping in the currently active text document.

## Vista

El menú **Vista** le permite navegar entre las distintas vistas de la interfaz de usuario de Tabular Editor 3. Si una vista está oculta, al hacer clic en el título de la vista en este menú se volverá a mostrar y pasará a primer plano. Ten en cuenta que los documentos no se muestran en el menú Ver. Para navegar entre documentos, usa el [menú Ventana](#window).

![Menú de vista](~/content/assets/images/model-menu.png)

- **Explorador TOM**: El Explorador TOM presenta una vista jerárquica de todo el [Tabular Object Model (TOM)](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) de los metadatos del modelo cargado actualmente. Consulta @tom-explorer-view para obtener más información.
- **AI Assistant**: The AI Assistant view lets you interact with an AI assistant that can help you with modeling tasks.
- **DAX Package Manager**: The DAX Package Manager view lets you browse and install DAX user-defined function packages into your model.
- **Best Practice Analyzer**: Best Practice Analyzer le ayuda a mejorar la calidad de su modelo al permitirle especificar reglas para la validación de mejores prácticas. Consulta @bpa-view para obtener más información.
- **Mensajes**: La vista de mensajes muestra errores, advertencias y mensajes informativos de varios orígenes, como el Analizador semántico de Tabular Editor 3. Consulta @messages-view para obtener más información.
- **Actualización de datos**: La vista Actualización de datos le permite hacer un seguimiento de las operaciones de actualización de datos que se ejecutan en segundo plano. Consulta @data-refresh-view para obtener más información.
- **Editor de expresiones**: Este es el "editor rápido" que le permite editar expresiones DAX, M o SQL en el objeto que esté seleccionado actualmente en el Explorador TOM. Consulta @dax-editor para obtener más información.
- **Macros**: La vista de macros le permite administrar cualquier macro que haya creado. Las macros se pueden crear desde @csharp-scripts. Consulta @creating-macros para obtener más información.
- **Analizador VertiPaq**: La vista Analizador VertiPaq le permite recopilar, importar y exportar estadísticas detalladas sobre los datos de su modelo para ayudarle a mejorar y depurar el rendimiento de DAX. El Analizador VertiPaq es creado y mantenido por [Marco Russo](https://twitter.com/marcorus) de [SQLBI](https://sqlbi.com) bajo la licencia MIT. Más información en la [página del proyecto en GitHub](https://github.com/sql-bi/VertiPaq-Analyzer).
- **Dependencies**: The [**DAX Dependencies** view](xref:creating-and-testing-dax#dax-dependencies) visualizes dependencies between the currently selected object and other objects in the model. Tick **Track TOM Explorer** to have it follow the tree selection.
- **DAX Optimizer**: The DAX Optimizer view integrates with [DAX Optimizer](https://www.daxoptimizer.com) to analyze your model for DAX performance issues.
- **Calendar Editor**: The Calendar Editor view lets you define and manage calendars in models using the modern time intelligence feature.
- **Perspective Editor**: The Perspective Editor view provides a matrix overview of which objects are included in each perspective of the model.
- **Metadata Translation Editor**: The Metadata Translation Editor view provides a grid for editing metadata translations (cultures) of model objects.
- **Toolbars / Properties**: The remaining items let you toggle the visibility of toolbars and bring up the Properties view (F4).

## Modelo

El menú **Modelo** muestra las acciones que se pueden realizar a nivel del objeto Modelo (el objeto raíz del Explorador TOM).

![Menú Herramientas](~/content/assets/images/tools-menu.png)

- **Implementar...**: Inicia el Asistente de implementación de Tabular Editor. Para obtener más información, consulta [Implementación del modelo](../deployment.md).

> [!IMPORTANT]
> La opción **Deploy** no está disponible en la Edición de escritorio de Tabular Editor 3. Para más información, consulte @editions.

- **Serialization options...** Lets you configure how model metadata is serialized when saving to disk (file or folder structure).
- **Importar tablas...** Inicia el Asistente de importación de tablas de Tabular Editor 3. Para más información, consulte @importing-tables.
- **Update schema (all tables)...** Detects schema changes in the data source(s) for all tables of the model compared to the currently imported columns. See [Updating table schema](xref:importing-tables#updating-table-schema) for more information.
- **Script DAX**: Genera un script DAX para el/los objeto(s) seleccionados actualmente (o para todos los objetos DAX del modelo, si no se ha seleccionado nada). Para más información, consulte @dax-scripts.
- **Actualizar modelo**: Cuando Tabular Editor está conectado a una instancia de Analysis Services, este submenú contiene opciones para iniciar una operación de actualización en segundo plano a nivel de modelo. El submenú incluye las siguientes opciones. Para más información, consulte [Comando Refresh (TMSL)](https://docs.microsoft.com/en-us/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions#request).
  - **Automático (modelo)**: Analysis Services determina qué objetos actualizar (solo los objetos que no están en el estado "Listo").
  - **Actualización completa (modelo)**: Analysis Services realiza una actualización completa del modelo.
  - **Calcular (modelo)**: Analysis Services vuelve a calcular todas las tablas calculadas, columnas calculadas, grupos de cálculo y relaciones. No se leen datos de los Data sources.
- **Add [object type]**: The remaining shortcuts in the **Model** menu lets you create new types of model child objects (tables, data sources, perspectives, etc.).

## Herramientas

El menú **Herramientas** contiene opciones para controlar las preferencias y personalizaciones de Tabular Editor 3.

![Menú Vista](~/content/assets/images/window-menu.png)

- **Personalizar...** Abre el cuadro de diálogo de personalización del diseño de la interfaz de usuario de Tabular Editor 3, que permite crear nuevas barras de herramientas, reorganizar y editar menús y botones de la barra de herramientas, etc.
- **Preferencias...** Abre el cuadro de diálogo de Preferencias de Tabular Editor 3, que funciona como un centro para administrar todos los demás aspectos de Tabular Editor y sus características, como la comprobación de actualizaciones, la configuración del proxy, los límites de filas de consulta, los tiempos de espera de las solicitudes, etc. Consulte @preferences para obtener más información.
- **Manage BPA rules...** Launches the Best Practice Analyzer rule manager, which lets you view and edit the Best Practice Analyzer rules and rule collections. Consulta @bpa-view para obtener más información.
- **MCP Server...** Launches the MCP Server dialog, from which you start and stop the server that lets an external AI agent work on the model you have open, review the permissions it will be given and copy a registration configuration for your agent. See @mcp-server for more information. The item is hidden when the AI features component is not installed, when **Enable MCP Server** is unchecked, or where an administrator has disabled it by policy.

## Ventana

El menú **Ventana** proporciona accesos directos para administrar y navegar entre las distintas vistas y documentos (conocidos colectivamente como _ventanas_) de la aplicación. También incluye elementos de menú para controlar los temas y las paletas de colores, tal como se describe [arriba](#changing-themes-and-palettes).

![Menú Ver](~/content/assets/images/view-menu.png)

- **Nuevo...** este submenú ofrece un acceso directo para crear nuevos [archivos auxiliares](xref:supported-files#supported-file-types). Las opciones aquí son idénticas a las de **Archivo > Nuevo**.

- **Flotar** desacopla la vista o el documento actual y lo coloca en una ventana flotante.

- **Anclar pestaña** ancla una pestaña. Cuando una pestaña está anclada, se muestra en el extremo izquierdo de las pestañas del documento y, al hacer clic con el botón derecho sobre las pestañas, se muestran accesos directos para cerrar solo las pestañas no ancladas.

  ![Menú contextual de pestaña](~/content/assets/images/tab-context-menu.png)

- **Nuevo grupo de pestañas horizontal/vertical**: Esta opción te permite dividir el área principal de documentos en varias secciones (también llamadas "grupos de pestañas"), para mostrar varios documentos simultáneamente, uno al lado del otro o uno encima del otro.

- **Close All**: Closes all document tabs. Se te pedirá que guardes los cambios no guardados, si los hay.

- **Restablecer el diseño de la ventana**: Restablece todas las personalizaciones aplicadas al área principal del documento.

- **1..N [documento]**: Aquí se muestran los primeros 10 documentos abiertos, lo que permite navegar entre ellos. También puedes usar el atajo CTRL+Tab para cambiar rápidamente entre documentos y vistas abiertos, como se muestra en la captura de pantalla siguiente:

  ![View Menu](~/content/assets/images/ctrl-tab.png)

- **Ventanas...**: Abre un cuadro de diálogo que enumera TODOS los documentos abiertos, y te permite cambiar entre ellos o cerrarlos individualmente.

  ![Administrador de ventanas](~/content/assets/images/windows-manager.png)

- **Capture Layout** / **Layouts...** / **Default layout** / **Classic layout**: These menu items were discussed [earlier in this article](#choosing-a-different-layout).

- **Tema** / **Paleta predeterminada**: Estos elementos del menú se trataron [antes en este artículo](#changing-themes-and-palettes).

- **Language**: Lets you change the display language of the Tabular Editor 3 user interface.

## Ayuda

El menú **Ayuda** ofrece accesos directos a recursos en línea y mucho más.

![Menú Ayuda](~/content/assets/images/help-menu.png)

- **Online Documentation**: This menu item opens [docs.tabulareditor.com](https://docs.tabulareditor.com), this documentation site, in your default web browser.
- **Onboarding Guide**: This menu item opens the Tabular Editor 3 onboarding guide, which helps new users get started with the application.
- **Soporte de la comunidad**: Este elemento del menú enlaza a nuestro [sitio público de soporte comunitario](https://github.com/TabularEditor/TabularEditor3).
- **Soporte dedicado**: Este elemento del menú te permite enviar un correo electrónico directamente a nuestra línea directa de soporte dedicado.
- **Get Started**: This menu item opens the **Get Started** page, which collects courses, demos and documentation for Tabular Editor. Prior to Tabular Editor 3.27.0 this item was called **What's New** and showed the release notes of the installed version; release notes now live in the @release-history.

> [!NOTE]
> El soporte dedicado está reservado a los clientes de la Edición Enterprise de Tabular Editor 3. El resto de los clientes debe ponerse en contacto a través del [sitio público de soporte de la comunidad](https://github.com/TabularEditor/TabularEditor3) para cualquier incidencia técnica, duda u otra consulta específica del producto.

- **Acerca de Tabular Editor**: Abre un cuadro de diálogo que muestra información detallada sobre la versión de Tabular Editor que se está utilizando, así como los detalles de instalación y licencia. El cuadro de diálogo también permite cambiar la clave de licencia.

## Menús dinámicos (dependientes del contexto)

Además de los menús mencionados anteriormente, pueden aparecer otros en determinados momentos, según qué elemento de la interfaz tenga el foco y qué objeto esté seleccionado actualmente en el Explorador TOM. Por ejemplo, si selecciona un objeto de tipo tabla, aparecerá un menú **Tabla**, con los mismos accesos directos específicos del contexto que cuando hace clic con el botón derecho en ese objeto en el Explorador TOM.

If you switch the input focus between different types of documents (i.e. DAX queries, Pivot Grids, diagrams, etc.), you should also see a menu representing the type of document currently in focus. Ese menú contendrá los elementos relevantes para el documento actual. Por ejemplo, cuando un diagrama tiene el foco, aparecerá un menú **Diagrama** que incluye, entre otros, un elemento para agregar tablas al diagrama.

Puede cambiar el comportamiento de estos menús dinámicos en **Herramientas > Preferencias > Interfaz de usuario**.

# Siguientes pasos

- @tom-explorer-view
- @supported-files
- @preferencias