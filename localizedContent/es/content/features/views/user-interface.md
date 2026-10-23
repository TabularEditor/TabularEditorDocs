---
uid: user-interface
title: Interfaz de usuario básica
author: Daniel Otykier
updated: 2026-10-13
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
# Conocer la interfaz de usuario de Tabular Editor 3

Este artículo describe la interfaz de usuario de Tabular Editor 3.

## Elementos básicos de la interfaz de usuario

Con un modelo semántico cargado, Tabular Editor 3 muestra el siguiente diseño predeterminado.

![Interfaz de usuario básica](~/content/assets/images/basic-ui.png)

1. **Barra de título**: el nombre del archivo cargado, o de la base de datos de Analysis Services o del modelo semántico de Power BI al que está conectado.
2. **Barra de menús**: todas las funciones de Tabular Editor 3. Consulte [Menús](#menus) para ver cada menú.
3. **Barras de herramientas**: las funciones más utilizadas. Todos los comandos de las barras de herramientas también están en los menús. Personalice las barras de herramientas y sus botones en **Herramientas > Personalizar...**.
4. **Vista del Explorador TOM**: un árbol de los objetos del modelo, construido a partir de los metadatos del [Tabular Object Model (TOM)](https://docs.microsoft.com/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions). Los botones de activación de la parte superior filtran qué tipos de objetos se muestran, y el cuadro de búsqueda filtra los objetos por nombre.
5. **Editor de expresiones**: edita las expresiones DAX, SQL o M del objeto seleccionado en el Explorador TOM. Si lo cierra, haga doble clic en un objeto del Explorador TOM para abrirlo de nuevo. Si el objeto tiene más de una propiedad de expresión, el menú desplegable de la parte superior permite alternar entre ellas. Por ejemplo, un KPI tiene un objetivo, un estado y una expresión de tendencia.
6. **Vista de propiedades**: todas las propiedades TOM de los objetos seleccionados en el Explorador TOM. Puedes editar la mayoría de las propiedades en la cuadrícula, incluso con varios objetos seleccionados. Algunas propiedades, como **Cadena de formato**, **Cadena de conexión** y **Miembros del rol**, abren un cuadro de diálogo o un editor de colecciones desde el botón de puntos suspensivos de la celda de valor.
7. **Vista de mensajes**: errores semánticos detectados por el análisis continuo de las expresiones DAX del modelo, además de mensajes de C# Scripts y errores notificados por Analysis Services.
8. **Barra de estado**: información sobre la selección actual, los resultados de Best Practice Analyzer y mucho más. El elemento de conexión muestra la base de datos y el servidor al que está conectado como `<database>@<server>`, o `<host>:<port>` para Power BI Desktop, y **(Sin conexión)** para un modelo cargado sin conexión. Cuando el [servidor MCP](xref:mcp-server) está disponible, un indicador en el extremo derecho indica **MCP iniciado** o **MCP detenido**, y su información sobre herramientas muestra la dirección en la que escucha el servidor. Haga clic en el indicador para abrir el cuadro de diálogo **Servidor MCP**, o haga clic con el botón derecho en él para iniciar o detener el servidor, copiar una configuración de registro para su agente o abrir la página de preferencias.

El [menú Vista](#view) abre las otras vistas.

## Personalización de la interfaz de usuario

Puede cambiar el tamaño y reorganizar todos los elementos de la interfaz de usuario, así como arrastrar las vistas fuera de la ventana principal, por ejemplo, a otro monitor. Tabular Editor 3 guarda el diseño cuando cierras la aplicación y lo restaura la próxima vez que la inicies.

### Elegir un diseño diferente

Seleccione **Ventana > Diseño predeterminado** para restablecer la aplicación al diseño predeterminado, o **Ventana > Diseño clásico** para colocar el Explorador TOM a la izquierda y la vista Propiedades debajo del Editor de expresiones, como en Tabular Editor 2.x.

Para cambiar entre sus propios diseños, guarde el actual con **Ventana > Capturar diseño**, y se convertirá en una opción del menú **Ventana**. **Ventana > Diseños...** muestra una lista de todos los diseños, donde puedes aplicarlos, cargarlos, quitarlos y guardarlos. Un diseño guardado en disco es un archivo .xml que puede compartir con otros usuarios de Tabular Editor 3.

![Gestionar diseños](~/content/assets/images/manage-layouts.png)

### Opciones de acoplamiento de ventanas

Cuando arrastra una vista o un documento, los indicadores de acoplamiento muestran dónde puede acoplarlo.

![Opciones de acoplamiento de ventanas](~/content/assets/images/window-docking-options.png)

El lugar donde suelte la ventana determina su comportamiento:

**Anclaje de pestañas de documentos (indicador central)**: una ventana que se suelte sobre el indicador central se convertirá en una pestaña de documentos en el área de documentos principal, junto a documentos como consultas DAX, scripts y diagramas. Las pestañas de documentos:
- se incluyen cuando se alterna con **Ctrl+Tab**
- no tienen ocultación automática

**Anclaje de ventanas de herramientas (indicadores de borde)**: una ventana que se suelta en el indicador izquierdo, derecho, superior o inferior se ancla como una ventana de herramientas, como el Explorador TOM y la vista Mensajes. Ventanas de herramientas:
- no se incluyen en **Ctrl+Tab**
- Tienen un icono de chincheta que activa la función de ocultación automática, que contrae la ventana cuando no está en uso.
- se acoplan en cualquier lado del área del documento principal

> [!TIP]
> El tamaño de una ventana acoplada depende del espacio disponible donde la acoples, y puedes cambiar su tamaño arrastrando los separadores entre ventanas.

### Cambio de temas y paletas

Elija un tema en **Ventana > Tema**:

- Basic y Bezier están basados en vectores y se escalan en pantallas de alta resolución (DPI).
- Azul, Oscuro y Claro se basan en ráster y no se escalan bien en pantallas de alta resolución (DPI).

En el caso de Basic y Bezier, **Ventana > Paleta predeterminada** cambia los colores del tema.

![Paletas](~/content/assets/images/palettes.png)

## Menús

Esta sección describe cada menú.

El *documento activo* es el documento en el que se encuentra el cursor, como el Editor de expresiones o la pestaña «Script DAX 1» en la captura de pantalla siguiente. Algunos atajos y elementos de menú dependen de si un documento está activo y de su tipo.

> [!NOTE]
> Los menús y las barras de herramientas están bloqueados en su lugar de forma predeterminada. Para desbloquearlos, desmarque **Bloquear menús y barras de herramientas** en **Herramientas > Personalizar... > Opciones**.

<!-- NUEVA CAPTURA DE PANTALLA (3.27.1): active-document.png. La barra de título utiliza el formato antiguo. Opcional. -->
![Documento activo](~/content/assets/images/active-document.png)

### Archivo

El menú **Archivo** carga y guarda los metadatos del modelo, los archivos auxiliares y los documentos.

![Menú Archivo](~/content/assets/images/file-menu.png)

- **Nuevo**: crea un nuevo modelo en blanco (**Ctrl+N**) o un [archivo de soporte](xref:supported-files#supported-file-types), como una consulta DAX, un script DAX (archivos de texto) o un diagrama (archivo JSON). Los archivos de soporte que no sean scripts de C# requieren un modelo cargado.
  
  ![Menú Archivo > Nuevo](~/content/assets/images/file-menu-new.png)

> [!IMPORTANT]
> **Nuevo > Modelo...** no está disponible en la edición Desktop de Tabular Editor 3, que funciona únicamente como herramienta externa para Power BI Desktop. Consulte @editions.

- **Abrir**: carga un modelo desde una de estas fuentes o abre cualquier otro archivo compatible:

  ![Menú Archivo > Abrir](~/content/assets/images/file-menu-open.png)

  - **Modelo desde archivo...** abre los metadatos del modelo desde un archivo, como un archivo .bim o .pbit.
  - **Modelo desde base de datos...** carga los metadatos de un modelo implementado. Introduzca los datos de conexión de Analysis Services o Power BI XMLA, o conéctese a una instancia local, como el servidor del espacio de trabajo integrado de Visual Studio o Power BI Desktop. Haga clic con el botón derecho en un servidor de la lista **Servidor** para anclarlo en la parte superior de la lista o eliminarlo. Consulte @xmla-as-connectivity.
  - **Modelo desde carpeta...** abre los metadatos del modelo desde una estructura de carpetas guardada por cualquier versión de Tabular Editor.
  - **Archivo...** abre cualquier tipo de archivo compatible con Tabular Editor 3, por extensión de nombre de archivo. Consulte [Tipos de archivos compatibles](xref:supported-files).
  - **Importar desde vista de métrica en formato YAML...** importa los metadatos del modelo desde un archivo YAML de vista de métrica de Databricks.

    ![Tipos de archivos compatibles](~/content/assets/images/supported-file-types.png)

> [!IMPORTANT]
> En la edición Desktop de Tabular Editor 3, las opciones **Abrir > Modelo desde archivo...** y **Abrir > Modelo desde carpeta...** no están disponibles, y **Abrir > Archivo...** solo abre [archivos compatibles](xref:supported-files#supported-file-types).

- **Recargar desde el disco** / **Recargar desde el servidor**: recarga los metadatos del modelo desde su origen y descarta todos los cambios no guardados. El comando dice **Volver a cargar desde el disco** para un modelo cargado desde un archivo o una carpeta, y **Volver a cargar desde el servidor** para un modelo abierto desde Analysis Services o Power BI. Si Tabular Editor 3 se ejecuta como una herramienta externa para Power BI Desktop y el modelo cambia en Power BI Desktop, utilice este comando para volver a cargar los metadatos del modelo sin volver a conectarse. Los modelos cargados desde un archivo o una carpeta se vuelven a cargar automáticamente cuando cambian los archivos. Consulte [Recarga automática desde el disco](xref:auto-reload). Los documentos abiertos de consultas DAX y Pivot Grid permanecen abiertos durante una recarga y se conectan al modelo recargado.
- **Cerrar documento** (**Ctrl+W**): cierra el documento o panel activo en el área principal, como una consulta DAX, un script de C# o un diagrama. Si el documento tiene cambios sin guardar, aparecerá un mensaje para guardarlos.
- **Cerrar modelo**: descarga los metadatos del modelo. Si ha modificado los metadatos, aparecerá un mensaje para guardar los cambios. Los documentos abiertos de consultas DAX y Pivot Grid se cierran con el modelo, y aparece un mensaje para guardar los cambios en cada uno de ellos que tenga cambios sin guardar.
- **Guardar**: guarda el documento activo en su archivo de origen. Si no hay ningún documento activo, guarda los metadatos del modelo en su origen: un archivo Model.bim, una estructura de carpetas Database.json, una instancia de Analysis Services (incluido Power BI Desktop) o el punto de conexión XMLA de Power BI.
- **Guardar como...** guarda el documento activo como un nuevo archivo. Si no hay ningún documento activo, guarda los metadatos del modelo como un nuevo archivo .bim (JSON).
- **Guardar en carpeta...** guarda los metadatos del modelo como una [estructura de carpetas](xref:save-to-folder).
- **Guardar todo**: guarda todos los documentos no guardados y los metadatos del modelo.
- **Archivos recientes**: enumera los archivos auxiliares utilizados recientemente.
- **Modelos tabulares recientes**: enumera los archivos y carpetas de metadatos de modelos utilizados recientemente.

Con **Detalle del origen del modelo** establecido en **Solo nombre** u **Oculto**, el texto que aparece al pasar el ratón por encima de los menús de archivos y modelos recientes muestra los nombres de los archivos sin los directorios.

> [!IMPORTANT]
> En la edición Desktop de Tabular Editor 3, las opciones **Guardar en carpeta** y **Modelos tabulares recientes** están deshabilitadas, y la opción **Guardar como** solo está habilitada para [archivos compatibles](xref:supported-files#supported-file-types).

- **Salir**: cierra Tabular Editor 3. Primero aparece un mensaje para guardar los archivos no guardados o los metadatos del modelo.

### Editar

El menú **Editar** permite editar el documento activo o los metadatos del modelo cargado.

![Menú Editar](~/content/assets/images/edit-menu.png)

- **Deshacer**: deshace el último cambio en la parte de la ventana que tiene el foco. En un control de texto, como un documento o el **Editor de expresiones**, deshace la escritura y muestra **Deshacer escritura**. En otros lugares, deshace el último cambio realizado en los metadatos del modelo. **Ctrl+Z** ejecuta este comando.
- **Rehacer**: rehace el último cambio deshecho, siguiendo las mismas reglas que **Deshacer**. **Ctrl+Y** ejecuta este comando.
- **Deshacer** / **Rehacer** seguido del nombre de un cambio en el modelo, por ejemplo, **Deshacer script de C# (MCP)**: aparecen solo cuando un control de texto tiene el foco y deshacen o rehacen el último cambio en los metadatos del modelo. Consulte [Deshacer en editores de texto](xref:undo-redo#undo-in-text-editors).
- **Buscar**: abre el cuadro de diálogo «Buscar y reemplazar» en la pestaña «Buscar». Consulte [Buscar](xref:find-replace#find).
- **Reemplazar**: abre el cuadro de diálogo «Buscar y reemplazar» en la pestaña «Reemplazar». Consulte [Reemplazar](xref:find-replace#replace).
- **Cortar / Copiar / Pegar**: cuando un control de texto tiene el foco, estas acciones se aplican al texto seleccionado. Cuando el Explorador TOM tiene el foco, se aplican a los objetos seleccionados. Por ejemplo, para duplicar varias medidas, selecciónelas con **Mayús** o **Ctrl** en el Explorador TOM y pulse **Ctrl+C** y, a continuación, **Ctrl+V**.
- **Eliminar**: elimina el texto seleccionado cuando un control de texto tiene el foco, o los objetos seleccionados cuando el Explorador TOM tiene el foco.

> [!NOTE]
> Solo aparece un mensaje de eliminación cuando se seleccionan varios objetos o cuando otros objetos dependen de los que se eliminan. **Deshacer** (**Ctrl+Z**) restaura los objetos eliminados.

- **Seleccionar todo**: selecciona todo el texto del documento activo o todos los objetos con el mismo elemento principal en el Explorador TOM.
- **Code Assist**: accesos directos a las funciones de Code Assist para DAX. Disponible mientras edita DAX. Consulte [Editor DAX](xref:dax-editor#code-assist-features).
- **Ajuste de línea**: activa o desactiva el ajuste de línea en el documento de texto activo.

### Vista

El menú **Vista** abre y centra las vistas de Tabular Editor 3, incluidas las ocultas. Los documentos no aparecen en la lista; cambie de uno a otro con el [menú Ventana](#window).

![Menú Ver](~/content/assets/images/view-menu.png)

- **TOM Explorer**: un árbol del [Tabular Object Model (TOM)](https://docs.microsoft.com/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) del modelo cargado. Consulte @tom-explorer-view.
- **Asistente de IA**: un chat con un asistente de IA para tareas de modelado.
- **Administrador de paquetes DAX**: explora los paquetes de funciones DAX definidas por el usuario y los instala en el modelo.
- **Best Practice Analyzer**: valida el modelo con respecto a las reglas de mejores prácticas que usted defina. Consulte @bpa-view.
- **Mensajes**: errores, advertencias y mensajes informativos procedentes de fuentes como el Analizador semántico de Tabular Editor 3. Consulte @messages-view.
- **Actualización de datos**: realiza un seguimiento de las operaciones de actualización que se ejecutan en segundo plano. Consulta @data-refresh-view.
- **Editor de expresiones**: edita las expresiones DAX, M o SQL del objeto seleccionado en el Explorador TOM. Consulte @dax-editor.
- **Macros**: gestiona las macros que ha creado a partir de @csharp-scripts. Consulte @creating-macros.
- **Analizador VertiPaq**: recopila, importa y exporta estadísticas sobre los datos del modelo, para optimizar el rendimiento de DAX. El Analizador VertiPaq ha sido creado y es mantenido por [Marco Russo](https://twitter.com/marcorus) de [SQLBI](https://sqlbi.com) bajo licencia MIT. Consulte la [página del proyecto en GitHub](https://github.com/sql-bi/VertiPaq-Analyzer).
- **Dependencias**: la vista [**Dependencias DAX**](xref:creating-and-testing-dax#dax-dependencies) muestra las dependencias entre el objeto seleccionado y otros objetos del modelo. Seleccione **Seguir Explorador TOM** para que siga la selección del Explorador TOM.
- **Optimizador de DAX**: analiza el modelo en busca de problemas de rendimiento de DAX con [DAX Optimizer](https://www.daxoptimizer.com).
- **Editor de calendarios**: define y gestiona los calendarios para la función moderna de inteligencia temporal.
- **Editor de perspectivas**: una matriz que indica qué objetos incluye cada perspectiva del modelo.
- **Metadata Translation Editor**: una cuadrícula para editar las traducciones de metadatos (culturas) de los objetos del modelo.
- **Barras de herramientas / Propiedades**: alterna la visibilidad de la barra de herramientas y abre la vista Propiedades (**F4**).

### Modelo

El menú **Modelo** contiene acciones sobre el objeto Model, la raíz del Explorador TOM.

![Menú Ver](~/content/assets/images/model-menu.png)

- **Implementar...**: abre el asistente de implementación de Tabular Editor. Consulte [Implementación del modelo](xref:deployment).

> [!IMPORTANT]
> **Implementar** no está disponible en la edición Desktop de Tabular Editor 3. Consulte @editions.

- **Opciones de serialización...** establece cómo se serializan los metadatos del modelo cuando se guardan en un archivo o en una estructura de carpetas.
- **Importar tablas...** abre el asistente de importación de tablas de Tabular Editor 3. Consulte @importing-tables.
- **Actualizar esquema (todas las tablas)...** compara las columnas de todas las tablas con sus fuentes de datos y detecta los cambios en el esquema. Consulte [Actualizar esquema de tabla](xref:importing-tables#updating-table-schema).
- **Script DAX**: genera un script DAX para los objetos seleccionados, o para todos los objetos DAX del modelo si no hay nada seleccionado. Consulte @dax-scripts.
- **Actualizar modelo**: inicia una actualización en segundo plano del modelo cuando Tabular Editor está conectado a Analysis Services. Consulte [Comando Actualizar (TMSL)](https://docs.microsoft.com/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions#request). El submenú tiene estas opciones:
  - **Automática (modelo)**: Analysis Services actualiza solo los objetos que no están en el estado «Listo».
  - **Actualización completa (modelo)**: Analysis Services realiza una actualización completa del modelo.
  - **Calcular (modelo)**: Analysis Services vuelve a calcular todas las tablas calculadas, las columnas calculadas, los grupos de cálculo y las relaciones. No se leen datos de los orígenes de datos.
- **Añadir [tipo de objeto]**: los elementos restantes crean objetos secundarios del modelo, como tablas, orígenes de datos y perspectivas.

### Herramientas

El menú **Herramientas** contiene las preferencias y personalizaciones de Tabular Editor 3.

![Menú Ver](~/content/assets/images/tools-menu.png)

- **Personalizar...** abre el cuadro de diálogo de personalización del diseño de la interfaz de usuario, donde puedes crear barras de herramientas y reorganizar y editar menús y botones de las barras de herramientas.
- **Preferencias...** abre el cuadro de diálogo Preferencias, con ajustes como las comprobaciones de actualizaciones, la configuración del proxy, los límites de filas de las consultas y los tiempos de espera de las solicitudes. Consulte @preferences.
- **Administrar reglas BPA...** abre el administrador de reglas del Best Practice Analyzer, donde puedes ver y editar reglas y conjuntos de reglas. Consulta @bpa-view.
- **Servidor MCP...** abre el cuadro de diálogo **Servidor MCP**, donde puedes iniciar y detener el servidor que permite que un agente de IA externo trabaje en el modelo abierto, revisar los permisos que obtiene el agente y copiar una configuración de registro para tu agente. Consulte @mcp-server. El elemento está oculto cuando el componente de funciones de IA no está instalado, cuando la opción **Habilitar servidor MCP** está desmarcada o cuando un administrador lo ha deshabilitado mediante una política.

### Ventana

El menú **Ventana** gestiona y alterna entre las vistas y los documentos de la aplicación, denominados conjuntamente *ventanas*, y también contiene los ajustes de [tema y paleta](#changing-themes-and-palettes).

![Menú «Ventana»](~/content/assets/images/window-menu.png)

- **Nuevo...** crea [archivos auxiliares](xref:supported-files#supported-file-types). Las opciones son las mismas que en **Archivo > Nuevo**.
- **Flotante** desacopla la vista o el documento actual en una ventana flotante.
- **Anclar pestaña** ancla una pestaña al extremo izquierdo de las pestañas de documentos. El menú contextual de la pestaña, al que se accede haciendo clic con el botón derecho, contiene comandos que cierran únicamente las pestañas que no están ancladas.
  
  ![Menú Ver](~/content/assets/images/tab-context-menu.png)

- **Nuevo grupo de pestañas horizontal/vertical**: divide el área principal del documento en grupos de pestañas, para mostrar varios documentos uno al lado del otro o uno encima del otro.
- **Cerrar todo**: cierra todas las pestañas de documentos. Primero aparece un mensaje para guardar los cambios sin guardar.
- **Restablecer diseño de ventana**: restablece toda la personalización del área principal del documento.
- **1..N [documento]**: los primeros 10 documentos abiertos. **Ctrl+Tab** también permite alternar entre los documentos abiertos y las vistas:

  ![Menú Ver](~/content/assets/images/ctrl-tab.png)

- **Ventanas...**: abre un cuadro de diálogo que enumera todos los documentos abiertos, donde puedes cambiar a cada uno o cerrarlo.

  ![Menú «Ver»](~/content/assets/images/windows-manager.png)

- **Capturar diseño** / **Diseños...** / **Diseño predeterminado** / **Diseño clásico**: consulte [Elegir un diseño diferente](#choosing-a-different-layout).
- **Tema** / **Paleta predeterminada**: consulte [Cambiar temas y paletas](#changing-themes-and-palettes).
- **Idioma**: cambia el idioma de visualización de la interfaz de usuario de Tabular Editor 3.

### Ayuda

El menú **Ayuda** enlaza con recursos en línea.

![Menú «Ver»](~/content/assets/images/help-menu.png)

- **Documentación en línea**: abre [docs.tabulareditor.com](https://docs.tabulareditor.com) en su navegador web predeterminado.
- **Guía de incorporación**: abre la guía de incorporación de Tabular Editor 3 para nuevos usuarios.
- **Soporte de la comunidad**: abre el [sitio público de soporte de la comunidad](https://github.com/TabularEditor/TabularEditor3).
- **Soporte dedicado**: envía un correo electrónico a la línea directa de soporte dedicado.
- **Primeros pasos**: abre la página **Primeros pasos**, que recopila cursos, demostraciones y documentación para Tabular Editor. Antes de Tabular Editor 3.27.0, este elemento se llamaba **Novedades**. Para consultar las notas de la versión, ve a @release-history.

> [!NOTE]
> El soporte especializado está destinado a los clientes de Tabular Editor 3 Edición Enterprise. Otros clientes utilizan el [sitio de soporte de la comunidad pública](https://github.com/TabularEditor/TabularEditor3) para plantear preguntas técnicas y sobre el producto.

- **Acerca de Tabular Editor**: muestra la versión, los detalles de instalación y de licencia, y le permite cambiar su clave de licencia.
 
### Menús dinámicos (dependientes del contexto)

Aparecen menús adicionales en función del elemento de la interfaz de usuario que tenga el foco y del objeto seleccionado en el Explorador TOM. Por ejemplo, si selecciona una tabla, aparece un menú **Tabla** con los mismos elementos que el menú contextual de la tabla en el Explorador TOM.

Cada tipo de documento, como las consultas DAX, las cuadrículas dinámicas y los diagramas, también añade un menú cuando un documento de ese tipo tiene el foco. Por ejemplo, un diagrama seleccionado añade un menú **Diagrama** con un elemento para añadir tablas al diagrama.

Configure el comportamiento de estos menús dinámicos en **Herramientas > Preferencias > Tabular Editor > Interfaz de usuario**.

## Próximos pasos

- @tom-explorer-view
- @supported-files
- @preferences
