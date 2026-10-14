---
uid: user-interface
title: Interfaz de usuario básica
author: Daniel Otykier
updated: 2026-10-12
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

Con un modelo semántico cargado, Tabular Editor 3 muestra el diseño predeterminado que aparece a continuación.

![Interfaz de usuario básica](~/content/assets/images/basic-ui.png)

1. **Barra de título**: Muestra el nombre del archivo cargado actualmente y, si está conectado, la base de datos de Analysis Services o el Dataset de Power BI.
2. **Barra de menús**: La barra de menús te da acceso a todas las funciones de Tabular Editor 3. Consulta [Menús](#menus) para ver una guía detallada de todos los elementos del menú.
3. **Barras de herramientas**: Las barras de herramientas te dan acceso rápido a las funciones más utilizadas. También puedes acceder desde los menús a todas las funciones disponibles en la barra de herramientas. Puedes personalizar las barras de herramientas y sus botones en **Herramientas > Personalizar...**
4. **Vista del Explorador TOM**: Una vista jerárquica de tu modelo de datos, con todos los objetos disponibles.  de los metadatos del [Tabular Object Model (TOM)](https://docs.microsoft.com/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) que representan tu Data model. Los botones de alternancia de la parte superior te permiten filtrar qué objetos se muestran. El cuadro de búsqueda te permite filtrar objetos por nombre.
5. **Editor de expresiones**: El editor de expresiones ofrece una forma rápida de editar cualquier expresión DAX, SQL o M del objeto seleccionado actualmente en el Explorador TOM. Si cierras el editor de expresiones, puedes volver a abrirlo haciendo doble clic en un objeto del Explorador TOM. El menú desplegable de la parte superior te permite cambiar entre distintas propiedades de expresión, en caso de que el objeto seleccionado actualmente tenga más de una (por ejemplo, los KPI tienen Expresiones de objetivo, Expresiones de estado y Expresiones de tendencia, que son 3 expresiones DAX diferentes que pertenecen al mismo objeto KPI).
6. **Vista de propiedades**: Una vista detallada de todas las propiedades TOM disponibles para el/los objeto(s) seleccionados actualmente en el Explorador TOM. La mayoría de las propiedades se pueden editar desde la cuadrícula, incluso cuando hay varios objetos seleccionados. Algunas propiedades (como "Format String", "Connection String" y "Miembros de rol") tienen cuadros de diálogo emergentes o editores de colecciones que puedes abrir haciendo clic en el botón de puntos suspensivos dentro de la celda del valor de la propiedad.
7. **Vista de mensajes**: Tabular Editor 3 analiza continuamente las expresiones DAX de tu modelo para detectar errores semánticos. Cualquier error de este tipo se muestra aquí. Además, los mensajes que se muestran en esta vista pueden provenir de scripts de C# o de mensajes de error generados por Analysis Services.
8. **Barra de estado**: La barra de estado ofrece diversa información contextual sobre la selección actual, los hallazgos de Best Practice Analyzer, etc. Cuando el [servidor MCP](xref:mcp-server) está disponible, un indicador en el extremo derecho muestra **MCP iniciado** o **MCP detenido**; en su información sobre herramientas aparece la dirección en la que está escuchando el servidor. Haz clic para abrir el cuadro de diálogo del servidor MCP, o haz clic con el botón derecho para iniciar o detener el servidor, copiar una configuración de registro para tu agente o ir a la página de preferencias.

El [menú Ver](#view) abre las demás vistas.

## Personalización de la interfaz de usuario

Puedes cambiar el tamaño y reorganizar todos los elementos de la interfaz de usuario, y arrastrar vistas fuera de la ventana principal, por ejemplo a otro monitor. Tabular Editor 3 guarda el diseño al cerrar la aplicación y lo restaura la próxima vez que se inicia.

### Elegir un diseño diferente

Elige **Ventana > Diseño predeterminado** para restablecer la aplicación al diseño predeterminado, o **Ventana > Diseño clásico** para colocar el Explorador TOM a la izquierda y la vista de propiedades debajo del Editor de expresiones, como en Tabular Editor 2.x.

Para cambiar entre tus propios diseños, guarda el actual con **Ventana > Capturar diseño** y aparecerá como opción en el menú **Ventana**. **Ventana > Diseños...** muestra todos los diseños; ahí puedes aplicarlos, cargarlos, quitarlos y guardarlos. Un diseño guardado en disco es un archivo .xml que puedes compartir con otros usuarios de Tabular Editor 3.

![Administrar diseños](~/content/assets/images/manage-layouts.png)

### Opciones de acoplamiento de ventanas

Al arrastrar una vista o un documento, los indicadores de acoplamiento muestran dónde puedes acoplarlo.

![Opciones de acoplamiento de ventanas](~/content/assets/images/window-docking-options.png)

El lugar donde sueltas la ventana determina cómo se comporta:

**Acoplamiento como pestaña de documento (indicador central)**: la ventana que sueltes en el indicador central se convierte en una pestaña de documento en el área principal de documentos, junto a documentos como consultas DAX, scripts y diagramas. Pestañas de documentos:

- se incluyen al recorrer con **Ctrl+Tab**
- no tienen ocultación automática

**Acoplamiento como ventana de herramientas (indicadores de borde)**: la ventana que sueltes en el indicador izquierdo, derecho, superior o inferior se acopla como ventana de herramientas, como el Explorador TOM y la vista de mensajes. Las ventanas de herramientas:

- no se incluyen en **Ctrl+Tab**
- tienen un icono de chincheta que activa la ocultación automática y contrae la ventana cuando no se está usando
- se pueden acoplar en cualquiera de los lados del área principal de documentos

> [!TIP]
> El tamaño de una ventana acoplada depende del espacio disponible en el lugar donde la acoples, y puedes cambiar su tamaño arrastrando los divisores entre ventanas.

### Cambiar temas y paletas

Elige un tema en **Ventana > Tema**:

- Los temas Basic y Bezier están basados en vectores y escalan bien en pantallas high-DPI.
- Los temas Blue, Dark y Light están basados en ráster y no escalan bien en pantallas high-DPI.

Para Basic y Bezier, **Ventana > Paleta predeterminada** cambia los colores del tema.

![Paletas](~/content/assets/images/palettes.png)

## Menús

Esta sección describe cada menú.

El _documento activo_ es el documento en el que está el cursor, como el Editor de expresiones o la pestaña "Script DAX 1" de la siguiente captura de pantalla. Algunos atajos de teclado y elementos de menú dependen de si hay un documento activo y de su tipo.

> [!NOTE]
> De forma predeterminada, los menús y las barras de herramientas están bloqueados. Para desbloquearlos, desmarca **Bloquear menús y barras de herramientas** en **Herramientas > Personalizar... > Opciones**.

![Documento activo](~/content/assets/images/active-document.png)

### Archivo

El menú **Archivo** carga y guarda metadatos del modelo, archivos de soporte y documentos.

![Menú Archivo](~/content/assets/images/file-menu.png)

- **Nuevo**: crea un nuevo modelo en blanco (**Ctrl+N**) o un [archivo auxiliar](xref:supported-files#supported-file-types), como una consulta DAX, un Script DAX (archivos de texto) o un diagrama (archivo JSON). Los archivos auxiliares que no sean C# Scripts requieren que haya un modelo cargado.

  ![Menú Archivo: Nuevo](~/content/assets/images/file-menu-new.png)

> [!IMPORTANT]
> **Nuevo > Modelo...** no está disponible en la Edición de escritorio de Tabular Editor 3, ya que esta edición solo puede usarse como herramienta externa para Power BI Desktop. Consulta @editions.

- **Abrir**: carga un modelo desde uno de estos orígenes, o abre cualquier otro tipo de archivo compatible:

  ![Menú Archivo: Abrir](~/content/assets/images/file-menu-open.png)

  - **Modelo desde archivo...** abre los metadatos del modelo desde un archivo, como un .bim o .pbit.
  - **Modelo desde BD...** carga los metadatos de un modelo implementado. Especifica los detalles de conexión de Analysis Services o del punto de conexión XMLA de Power BI, o conéctate a una instancia local, como el servidor de la Workspace Integrada de Visual Studio o Power BI Desktop.
  - **Modelo desde carpeta...** abre los metadatos del modelo desde una estructura de carpetas guardada con cualquier versión de Tabular Editor.
  - **Archivo...** abre cualquier tipo de archivo compatible con Tabular Editor 3, según la extensión del nombre de archivo. Consulta [Tipos de archivo compatibles](xref:supported-files).
  - **Importar desde Metric View YAML...** importa los metadatos del modelo desde un archivo YAML de Metric View de Databricks.

    ![Tipos de archivo compatibles](~/content/assets/images/supported-file-types.png)

> [!IMPORTANT]
> En la Edición de escritorio de Tabular Editor 3, **Abrir > Modelo desde archivo...** y **Abrir > Modelo desde carpeta...** no están disponibles, y **Abrir > Archivo...** solo abre [archivos auxiliares](xref:supported-files#supported-file-types).

- **Recargar desde disco** / **Recargar desde el servidor**: vuelve a cargar los metadatos del modelo desde su origen y descarta todos los cambios no guardados. El comando aparece como **Recargar desde disco** para un modelo cargado desde un archivo o carpeta, y como **Recargar desde el servidor** para un modelo abierto desde Analysis Services o Power BI. Si Tabular Editor 3 se ejecuta como herramienta externa para Power BI Desktop y el modelo cambia en Power BI Desktop, usa este comando para volver a cargar los metadatos del modelo sin volver a conectarte. Los modelos cargados desde un archivo o una carpeta se recargan automáticamente cuando cambian los archivos. Consulta [Recarga automática desde el disco](xref:auto-reload).
- **Cerrar documento** (**Ctrl+W**): cierra el documento o panel activo en el área principal, como una consulta DAX, un C# Script o un diagrama. Si el documento tiene cambios sin guardar, aparecerá un aviso para guardarlos.
- **Cerrar modelo**: descarga los metadatos del modelo. Si hay cambios en los metadatos, aparecerá un aviso para guardarlos.
- **Guardar**: guarda el documento activo en el archivo de origen. Si no hay ningún documento activo, guarda los metadatos del modelo en su origen: un archivo Model.bim, una estructura de carpetas con Database.json, una instancia de Analysis Services (incluido Power BI Desktop) o el punto de conexión XMLA de Power BI.
- **Guardar como...** guarda el documento activo como un nuevo archivo. Si no hay ningún documento activo, guarda los metadatos del modelo como un nuevo archivo .bim (JSON).
- **Guardar en carpeta...** guarda los metadatos del modelo como una [estructura de carpetas](xref:save-to-folder).
- **Guardar todo**: guarda todos los documentos sin guardar y los metadatos del modelo.
- **Archivos recientes**: enumera los archivos auxiliares usados recientemente.
- **Modelos tabulares recientes**: enumera los archivos y carpetas de metadatos del modelo usados recientemente.

> [!IMPORTANT]
> En la Edición de escritorio de Tabular Editor 3, **Guardar en carpeta** y **Modelos tabulares recientes** están desactivados, y **Guardar como** solo está habilitado para los [archivos auxiliares](xref:supported-files#supported-file-types).

- **Salir**: cierra Tabular Editor 3. En primer lugar, aparece un aviso para guardar los archivos o los metadatos del modelo que no se hayan guardado.

### Editar

El menú **Editar** permite editar el documento activo o los metadatos del modelo cargado.

![Menú Editar](~/content/assets/images/edit-menu.png)

- **Deshacer**: deshace el último cambio en los metadatos del modelo. Si no hay ningún documento activo, **Ctrl+Z** ejecuta este comando.
- **Rehacer**: rehace el último cambio deshecho en los metadatos del modelo. Si no hay ningún documento activo, **Ctrl+Y** ejecuta este comando.
- **Buscar**: abre el cuadro de diálogo "Buscar y reemplazar" en la pestaña "Buscar". Consulta [Buscar](xref:find-replace#find).
- **Reemplazar**: abre el cuadro de diálogo "Buscar y reemplazar" en la pestaña "Reemplazar". Consulta [Reemplazar](xref:find-replace#replace).
- **Cortar / Copiar / Pegar**: con un documento activo, estas opciones se aplican al texto seleccionado. De lo contrario, se aplican a los objetos seleccionados en el Explorador TOM. Por ejemplo, para duplicar varias medidas, selecciónalas con **Mayús** o **Ctrl** en el Explorador TOM y pulsa **Ctrl+C** y, a continuación, **Ctrl+V**.
- **Eliminar**: elimina el texto seleccionado en el documento activo o, si no hay ningún documento activo, los objetos seleccionados en el Explorador TOM.

> [!NOTE]
> Solo aparece una confirmación de eliminación cuando hay varios objetos seleccionados o cuando otros objetos dependen de los que eliminas. **Deshacer** (**Ctrl+Z**) restaura los objetos eliminados.

- **Seleccionar todo**: selecciona todo el texto del documento activo o todos los objetos que pertenecen al mismo elemento padre en el Explorador TOM.
- **Code Assist**: accesos directos a las características de Code Assist para DAX. Disponible mientras editas DAX. Consulta el [Editor de DAX](xref:dax-editor#code-assist-features).
- **Ajuste de línea**: activa o desactiva el ajuste de línea en el documento de texto activo.

### Vista

El menú **Ver** se abre y pone el foco en las vistas de Tabular Editor 3, incluidas las ocultas. Los documentos no aparecen en la lista; cambia entre ellos con el [menú Ventana](#window).

![Menú de vista](~/content/assets/images/model-menu.png)

- **Explorador TOM**: El Explorador TOM presenta una vista jerárquica de todo el [Tabular Object Model (TOM)](https://docs.microsoft.com/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) de los metadatos del modelo cargado actualmente. Consulta @tom-explorer-view para obtener más información.
- **Asistente de IA**: La vista Asistente de IA te permite interactuar con un asistente de IA que puede ayudarte con tareas de modelado.
- **Administrador de paquetes de DAX**: La vista Administrador de paquetes de DAX te permite examinar e instalar paquetes de funciones definidas por el usuario de DAX en tu modelo.
- **Best Practice Analyzer**: Best Practice Analyzer le ayuda a mejorar la calidad de su modelo al permitirle especificar reglas para la validación de mejores prácticas. Consulta @bpa-view para obtener más información.
- **Mensajes**: La vista de mensajes muestra errores, advertencias y mensajes informativos de varios orígenes, como el Analizador semántico de Tabular Editor 3. Consulta @messages-view para obtener más información.
- **Actualización de datos**: La vista Actualización de datos le permite hacer un seguimiento de las operaciones de actualización de datos que se ejecutan en segundo plano. Consulta @data-refresh-view para obtener más información.
- **Editor de expresiones**: Este es el "editor rápido" que le permite editar expresiones DAX, M o SQL en el objeto que esté seleccionado actualmente en el Explorador TOM. Consulta @dax-editor para obtener más información.
- **Macros**: La vista de macros le permite administrar cualquier macro que haya creado. Las macros se pueden crear desde @csharp-scripts. Consulta @creating-macros para obtener más información.
- **Analizador VertiPaq**: La vista Analizador VertiPaq le permite recopilar, importar y exportar estadísticas detalladas sobre los datos de su modelo para ayudarle a mejorar y depurar el rendimiento de DAX. El Analizador VertiPaq es creado y mantenido por [Marco Russo](https://twitter.com/marcorus) de [SQLBI](https://sqlbi.com) bajo la licencia MIT. Más información en la [página del proyecto en GitHub](https://github.com/sql-bi/VertiPaq-Analyzer).
- **Dependencias**: La vista [**Dependencias de DAX**](xref:creating-and-testing-dax#dax-dependencies) visualiza las dependencias entre el objeto seleccionado actualmente y otros objetos del modelo. Marca **Seguir el Explorador TOM** para que siga la selección en el árbol.
- **Optimizador de DAX**: La vista Optimizador de DAX se integra con [Optimizador de DAX](https://www.daxoptimizer.com) para analizar tu modelo en busca de problemas de rendimiento de DAX.
- **Editor de calendario**: La vista Editor de calendario te permite definir y administrar calendarios en modelos mediante la característica moderna de inteligencia temporal.
- **Editor de perspectivas**: La vista Editor de perspectivas proporciona una vista matricial de qué objetos se incluyen en cada perspectiva del modelo.
- **Editor de traducción de metadatos**: La vista Editor de traducción de metadatos proporciona una cuadrícula para editar las traducciones de metadatos (configuraciones regionales) de los objetos del modelo.
- **Barras de herramientas / Propiedades**: Los elementos restantes te permiten mostrar u ocultar las barras de herramientas y abrir la vista de propiedades (F4).

## Modelo

El menú **Modelo** muestra las acciones que se pueden realizar a nivel del objeto Modelo (el objeto raíz del Explorador TOM).

![Menú Herramientas](~/content/assets/images/tools-menu.png)

- **Implementar...**: abre el Asistente de implementación de Tabular Editor. Consulta [Implementación del modelo](xref:deployment).

> [!IMPORTANT]
> La opción **Deploy** no está disponible en la Edición de escritorio de Tabular Editor 3. Para más información, consulte @editions.

- **Opciones de serialización...** Te permiten configurar cómo se serializan los metadatos del modelo al guardarlos en disco (estructura de archivos o carpetas).
- **Importar tablas...** Inicia el Asistente de importación de tablas de Tabular Editor 3. Para más información, consulte @importing-tables.
- **Actualizar esquema (todas las tablas)...** Detecta cambios en el esquema de los Data source(s) de todas las tablas del modelo, en comparación con las columnas importadas actualmente. Consulta [Actualización del esquema de tabla](xref:importing-tables#updating-table-schema) para obtener más información.
- **Script DAX**: Genera un script DAX para el/los objeto(s) seleccionados actualmente (o para todos los objetos DAX del modelo, si no se ha seleccionado nada). Para más información, consulte @dax-scripts.
- **Actualizar modelo**: Cuando Tabular Editor está conectado a una instancia de Analysis Services, este submenú contiene opciones para iniciar una operación de actualización en segundo plano a nivel de modelo. El submenú incluye las siguientes opciones. Para más información, consulta [Comando Refresh (TMSL)](https://docs.microsoft.com/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions#request).
  - **Automático (modelo)**: Analysis Services determina qué objetos actualizar (solo los objetos que no están en el estado "Listo").
  - **Actualización completa (modelo)**: Analysis Services realiza una actualización completa del modelo.
  - **Calcular (modelo)**: Analysis Services vuelve a calcular todas las tablas calculadas, columnas calculadas, grupos de cálculo y relaciones. No se leen datos de los Data sources.
- **Agregar [tipo de objeto]**: los elementos restantes crean objetos secundarios del modelo, como tablas, Data sources y perspectivas.

### Herramientas

El menú **Herramientas** incluye las preferencias y personalizaciones de Tabular Editor 3.

![Menú Vista](~/content/assets/images/window-menu.png)

- **Personalizar...**: abre el cuadro de diálogo de personalización del diseño de la interfaz de usuario, donde puedes crear barras de herramientas y reordenar y editar menús y botones de la barra de herramientas.
- **Preferencias...**: abre el cuadro de diálogo de Preferencias, con opciones como comprobaciones de actualizaciones, configuración de proxy, límites de filas de consulta y tiempos de espera de las solicitudes. Consulta @preferences.
- **Administrar reglas de BPA...** abre el administrador de reglas de Best Practice Analyzer, donde puedes ver y editar reglas y colecciones de reglas. Consulta @bpa-view.
- **Servidor MCP...** abre el cuadro de diálogo **Servidor MCP**, donde puedes iniciar y detener el servidor que permite que un agente de IA externo trabaje en el modelo abierto, revisar los permisos que se le conceden al agente y copiar una configuración de registro para tu agente. Consulta @mcp-server. El elemento se oculta cuando no está instalado el componente de características de IA, cuando **Habilitar servidor MCP** está desactivado o cuando un administrador lo ha deshabilitado mediante una directiva.

### Ventana

El menú **Ventana** administra y permite cambiar entre las vistas y los documentos de la aplicación, denominados conjuntamente _ventanas_, y también incluye la configuración de [tema y paleta](#changing-themes-and-palettes).

![Menú Ver](~/content/assets/images/view-menu.png)

- **Nuevo...** crea [archivos auxiliares](xref:supported-files#supported-file-types). Las opciones son las mismas que en **Archivo > Nuevo**.

- **Flotar** desacopla la vista o el documento actual y lo coloca en una ventana flotante.

- **Fijar pestaña** fija una pestaña en el extremo izquierdo de la barra de pestañas del documento. El menú contextual de la pestaña tiene comandos que cierran solo las pestañas no fijadas.

  ![Menú contextual de pestaña](~/content/assets/images/tab-context-menu.png)

- **Nuevo grupo de pestañas horizontal/vertical**: divide el área principal de documentos en grupos de pestañas para mostrar varios documentos uno al lado del otro o uno encima del otro.

- **Cerrar todo**: cierra todas las pestañas de documentos. Primero aparece un aviso para guardar los cambios sin guardar.

- **Restablecer el diseño de la ventana**: restablece todas las personalizaciones aplicadas al área principal de documentos.

- **1..N [documento]**: los 10 primeros documentos abiertos. **Ctrl+Tab** también cambia entre los documentos y las vistas abiertas:

  ![Menú Ver](~/content/assets/images/ctrl-tab.png)

- **Ventanas...**: abre un cuadro de diálogo con una lista de todos los documentos abiertos, donde puedes cambiar a uno de ellos o cerrarlo.

  ![Administrador de ventanas](~/content/assets/images/windows-manager.png)

- **Capturar diseño** / **Diseños...** / **Diseño predeterminado** / **Diseño clásico**: consulta [Elegir un diseño diferente](#choosing-a-different-layout).

- **Tema** / **Paleta predeterminada**: consulta [Cambiar temas y paletas](#changing-themes-and-palettes).

- **Idioma**: cambia el idioma de visualización de la interfaz de usuario de Tabular Editor 3.

### Ayuda

El menú **Ayuda** enlaza a recursos en línea.

![Menú Ayuda](~/content/assets/images/help-menu.png)

- **Documentación en línea**: abre [docs.tabulareditor.com](https://docs.tabulareditor.com) en tu navegador web predeterminado.
- **Guía de introducción**: abre la guía de introducción de Tabular Editor 3 para nuevos usuarios.
- **Soporte de la comunidad**: abre el [sitio público de soporte comunitario](https://github.com/TabularEditor/TabularEditor3).
- **Soporte dedicado**: envía un correo electrónico a la línea directa de soporte dedicado.
- **Primeros pasos**: abre la página **Primeros pasos**, que reúne cursos, demostraciones y documentación de Tabular Editor. Antes de la versión 3.27.0 de Tabular Editor, este elemento se llamaba **Novedades**. Para ver las notas de la versión, consulta @release-history.

> [!NOTE]
> El soporte dedicado está reservado a los clientes de la Edición Enterprise de Tabular Editor 3. Los demás clientes deben usar el [sitio público de soporte de la comunidad](https://github.com/TabularEditor/TabularEditor3) para consultas técnicas y relacionadas con el producto.

- **Acerca de Tabular Editor**: muestra la versión, los detalles de instalación y de licencia, y te permite cambiar tu clave de licencia.

### Menús dinámicos (dependientes del contexto)

Aparecen menús adicionales en función de qué elemento de la interfaz de usuario tenga el foco y qué objeto esté seleccionado en el Explorador TOM. Por ejemplo, si seleccionas una tabla, aparece un menú **Tabla** con los mismos elementos que el menú contextual de la tabla en el Explorador TOM.

Cada tipo de documento, como las consultas DAX, los Pivot Grid y los diagramas, también añade un menú cuando un documento de ese tipo tiene el foco. Por ejemplo, cuando un diagrama tiene el foco, se agrega un menú **Diagrama** con una opción para agregar tablas al diagrama.

Configura el comportamiento de estos menús dinámicos en **Herramientas > Preferencias > Tabular Editor > Interfaz de usuario**.

## Siguientes pasos

- @tom-explorer-view
- @tipos de archivo compatibles
- @preferencias
