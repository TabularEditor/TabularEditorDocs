---
uid: migrate-from-vs
title: Migración desde Visual Studio
author: Daniel Otykier
updated: 2021-09-30
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Migración desde Visual Studio / SQL Server Data Tools

Este artículo da por hecho que estás familiarizado con el desarrollo de modelos tabulares con [Analysis Services Projects for Visual Studio](https://marketplace.visualstudio.com/items?itemName=ProBITools.MicrosoftAnalysisServicesModelingProjects) (conocidos anteriormente como SQL Server Data Tools). Esto es habitual entre los desarrolladores que usan SQL Server Analysis Services (Tabular) o Azure Analysis Services.

- Si nunca has usado Visual Studio para el desarrollo de modelos tabulares, puedes omitir este tema sin problema.
- Si antes usabas Tabular Editor 2.x para el desarrollo de modelos tabulares, te recomendamos que pases directamente al artículo @migrate-from-te2.

## Migración parcial

Tabular Editor 3 incluye funciones que te permiten prescindir por completo de Visual Studio para el desarrollo de modelos tabulares. Esto contrasta con Tabular Editor 2.x, donde algunos usuarios seguían prefiriendo usar Visual Studio para tareas como importar tablas, visualizar relaciones y previsualizar datos.

Sin embargo, a medida que te familiarices con Tabular Editor 3, puede que te siga resultando útil abrir tus modelos tabulares en Visual Studio de vez en cuando. Esto es posible en cualquier momento, ya que Tabular Editor 3 no modifica el formato del archivo **Model.bim** (también conocido como [TOM JSON](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions)) que usa Visual Studio, lo que garantiza la compatibilidad con Visual Studio.

La única excepción se da si decides usar la función [Guardar en carpeta](xref:parallel-development#what-is-save-to-folder) de Tabular Editor, ya que este formato de archivo no es compatible con Visual Studio. Sin embargo, puedes volver a crear fácilmente un archivo Model.bim para usarlo con Visual Studio, usando la opción **Archivo > Guardar como...** en Tabular Editor. También puedes hacer la conversión inversa cargando un archivo Model.bim en Tabular Editor y luego usando la opción **Archivo > Guardar en carpeta...**.

### Automatización de la conversión de formatos de archivo

Si a menudo necesitas convertir de un lado a otro entre el formato basado en carpetas (Database.json) de Tabular Editor y el formato de archivo (model.bim) de Visual Studio, considera escribir un pequeño script de comandos de Windows usando la [CLI de Tabular Editor 2.x](xref:command-line-options) para automatizar el proceso de conversión.

# [De Model.bim a carpeta](#tab/frombim)

Para convertir de model.bim a Database.json (formato basado en carpetas):

```cmd
tabulareditor.exe model.bim -F Database.json
```

# [De carpeta a model.bim](#tab/fromfolder)

Para convertir de Database.json (formato basado en carpetas) a model.bim:

```cmd
tabulareditor.exe Database.json -B model.bim
```

***

> [!NOTE]
> El script de línea de comandos anterior asume que tienes instalado [Tabular Editor 2.x](xref:getting-started-te2). La ubicación de instalación de Tabular Editor 2.x también debe especificarse en tu [variable de entorno PATH](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/path).

## Servidor de Workspace Integrada

Al iniciar un nuevo proyecto de Analysis Services (Tabular) en Visual Studio, se te pedirá que elijas si quieres usar el servidor de Workspace Integrada de Visual Studio o proporcionar tu propia instancia de Analysis Services. Además, debes decidir el nivel de compatibilidad del modelo tabular (consulta la captura de pantalla a continuación).

![VS New Project](~/content/assets/images/vs-new-project.png)

En cambio, al crear un modelo nuevo en Tabular Editor, el uso de un servidor de Workspace es completamente opcional (aunque se recomienda; consulta [modo del área de trabajo](xref:workspace-mode)).

A continuación se muestra el cuadro de diálogo que aparece al crear un modelo nuevo en Tabular Editor 3:

![New model dialog](~/content/assets/images/new-model.png)

Si habilitas la opción **Usar base de datos del Workspace**, Tabular Editor te solicitará una instancia de Analysis Services y un nombre de base de datos que se usará como base de datos del Workspace mientras trabajas en el modelo. Si no activas esta opción, podrás crear y trabajar en tu modelo en modo "sin conexión", lo que te permite añadir tablas, relaciones, crear expresiones DAX, etc. Sin embargo, tendrás que desplegar tu modelo sin conexión en una instancia de Analysis Services antes de poder actualizar, obtener una vista previa y consultar los datos del modelo.

> [!IMPORTANT]
> Tabular Editor 3 no ofrece una característica equivalente a la opción de **Workspace Integrada** de Visual Studio. En esencia, la Workspace Integrada es una instancia de Analysis Services administrada por Visual Studio. Dado que Analysis Services es software propietario de Microsoft, no podemos incluirlo junto con Tabular Editor 3. En su lugar, si quieres ejecutar una instancia local de Analysis Services para usarla con Tabular Editor, te recomendamos que instales [SQL Server Developer Edition](https://www.microsoft.com/en-us/sql-server/sql-server-downloads).

### Requisitos del nivel de compatibilidad

Tabular Editor te permite elegir los siguientes niveles de compatibilidad para crear bases de datos de Analysis Services:

- 1200 (Azure Analysis Services / SQL Server 2016+)
- 1400 (Azure Analysis Services / SQL Server 2017+)
- 1500 (Azure Analysis Services / SQL Server 2019+)

Además, Tabular Editor permite elegir niveles de compatibilidad adecuados para los Datasets de Power BI que se publicarán en el servicio de Power BI a través del [punto de conexión XMLA](xref:powerbi-xmla).

> [!NOTE]
> Tabular Editor no admite niveles de compatibilidad inferiores a 1200, ya que estos no usan el formato de metadatos [Tabular Object Model (TOM)](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions). Si planea migrar el desarrollo de Visual Studio a Tabular Editor para un modelo con nivel de compatibilidad 1100 o 1103, **debe actualizar el nivel de compatibilidad al menos a 1200** antes de migrar a Tabular Editor. Al hacerlo, ya no podrá implementar el modelo en SQL Server 2014 Analysis Services.

## Proyectos de Visual Studio

Al crear un proyecto de Analysis Services (Tabular) en Visual Studio, se crean varios archivos en la carpeta del proyecto junto al archivo Model.bim. Estos archivos contienen información específica del proyecto y del usuario que no está relacionada con el Tabular Object Model (TOM). La siguiente captura de pantalla muestra los archivos resultantes de crear un nuevo proyecto tabular en Visual Studio.

![VS Project File Structure](~/content/assets/images/vs-file-structure.png)

Al migrar a Tabular Editor, solo necesita llevar el archivo Model.bim, ya que aquí no existe el concepto de "proyecto". En su lugar, Tabular Editor simplemente carga los metadatos del modelo directamente desde el archivo Model.bim. En algunos casos, se crea junto al archivo Model.bim un archivo llamado [archivo Tabular Model User Options (tmuo)](xref:user-options). Tabular Editor usa este archivo para almacenar configuración específica del usuario y del modelo, como si se debe usar o no una base de datos del Workspace, credenciales de usuario (cifradas) para los Data source, etc.

Para mantener limpia la carpeta del "proyecto", recomendamos copiar el archivo Model.bim creado por Visual Studio en una carpeta nueva antes de cargarlo en Tabular Editor.

![Te File Structure](~/content/assets/images/te-file-structure.png)

Si quiere usar la función [Guardar en carpeta](xref:parallel-development#what-is-save-to-folder), recomendada para el desarrollo en paralelo y la integración con sistemas de control de versiones, ahora es el momento de guardar el modelo en una carpeta desde Tabular Editor (**Archivo > Guardar en carpeta...**).

![Te Folder Structure](~/content/assets/images/te-folder-structure.png)

## Control de versiones

Tabular Editor no incluye ninguna solución Integrada de control de versiones para los metadatos del modelo. Sin embargo, como todos los metadatos del modelo se almacenan en el disco como archivos de texto sin formato (JSON), resulta sencillo incluir los metadatos del modelo tabular en cualquier tipo de sistema de control de versiones. Por este motivo, la mayoría de los usuarios de Tabular Editor prefieren seguir teniendo Visual Studio instalado para acceder a [Visual Studio Team Explorer](https://docs.microsoft.com/en-us/azure/devops/user-guide/work-team-explorer?view=azure-devops) o, específicamente para Git, a la nueva [ventana Cambios de Git](https://docs.microsoft.com/en-us/visualstudio/version-control/git-with-visual-studio?view=vs-2019) de Visual Studio 2019.

> [!NOTE]
> A día de hoy, parece que [git](https://git-scm.com/) es el sistema de control de versiones preferido por la mayoría de los desarrolladores. La integración con Git en Tabular Editor 3 está prevista para una actualización futura.

Una vez que migre a Tabular Editor, ya no necesita conservar el proyecto original del modelo Tabular ni los archivos de apoyo creados por Visual Studio. Aun así, puede usar Visual Studio Team Explorer o la ventana Cambios de Git para ver cambios en el código, administrar ramas del control de versiones, realizar check-ins, fusiones, etc.

Por supuesto, la mayoría de los sistemas de control de versiones también tienen su propio conjunto de herramientas que puedes usar sin depender de Visual Studio. Por ejemplo, Git tiene su línea de comandos y muchas herramientas populares que se integran directamente con el Explorador de Windows, como [TortoiseGit](https://tortoisegit.org/).

### Guardar en carpeta y control de versiones

La principal ventaja de usar la opción [Guardar en carpeta](xref:parallel-development#what-is-save-to-folder) es que los metadatos del modelo se dividen en varios archivos pequeños, en lugar de almacenar todo en un único documento JSON grande. Muchas propiedades del TOM son arrays de objetos (por ejemplo, tablas, medidas y columnas). Como todos estos objetos tienen nombres explícitos, su orden en el array no importa. A veces, al serializar a JSON, el orden cambia, y esto hace que la mayoría de los sistemas de control de versiones indiquen que el archivo ha cambiado. Sin embargo, como este orden no tiene ningún significado semántico, no deberíamos perder tiempo resolviendo conflictos de fusión que puedan surgir por este tipo de cambio.

Con la serialización de Guardar en carpeta, se reduce considerablemente el número de arrays utilizados en los archivos JSON, ya que los objetos que de otro modo se almacenarían como arrays ahora se separan en archivos individuales guardados en una subcarpeta. Cuando Tabular Editor carga los metadatos del modelo desde el disco, recorre todas estas subcarpetas para garantizar que todos los objetos se deserialicen correctamente en el TOM.

De este modo, la serialización de Guardar en carpeta reduce enormemente la probabilidad de encontrar conflictos de fusión cuando dos o más desarrolladores realizan cambios en paralelo sobre el mismo modelo tabular.

## Diferencias en la interfaz de usuario

Esta sección enumera las diferencias más importantes entre las interfaces de usuario de Tabular Editor 3 y Visual Studio para el desarrollo de modelos tabulares. Si eres un usuario habitual de Visual Studio, deberías sentirte bastante cómodo con la interfaz de usuario de Tabular Editor 3. Si quieres un recorrido más detallado, consulta <xref:user-interface>.

### Explorador de modelos tabulares vs. Explorador TOM

En Visual Studio, puedes encontrar una vista jerárquica de los metadatos del modelo en el **Explorador de modelos tabulares**.

![Vs Explorador Tom](~/content/assets/images/vs-tom-explorer.png)

En Tabular Editor, esta vista se llama **Explorador TOM**. En Tabular Editor, todo el modelado del Data model suele girar en torno a localizar los objetos relevantes en el Explorador TOM y, a continuación, realizar determinadas acciones mediante el menú contextual con clic derecho, desde el menú principal o editando las propiedades del objeto en la vista **Propiedades**. En Tabular Editor, puedes usar operaciones intuitivas como selección múltiple, arrastrar y soltar, copiar y pegar, y deshacer y rehacer para todas las operaciones de modelado del Data model.

![Vs Explorador Tom](~/content/assets/images/tom-explorer.png)

El Explorador TOM de Tabular Editor también incluye opciones de acceso directo para mostrar u ocultar determinados tipos de objetos, objetos ocultos, carpetas de visualización y para buscar y filtrar rápidamente la jerarquía de metadatos.

Consulta @tom-explorer-view para obtener más información.

### Cuadrícula de propiedades

Tanto Visual Studio como Tabular Editor incluyen una cuadrícula de propiedades que te permite editar la mayoría de las propiedades del objeto que esté seleccionado en ese momento. A continuación se muestra una comparación entre la cuadrícula de propiedades de Visual Studio (izquierda) y la cuadrícula de propiedades de Tabular Editor (derecha) para la misma medida:

![Cuadrícula de propiedades en Visual Studio y Tabular Editor](~/content/assets/images/property-grid-vs-te.png)

En general, ambas funcionan de la misma manera, salvo que Tabular Editor usa nombres de propiedades estrechamente alineados con las propiedades de los objetos TOM. Tabular Editor también agrega varias propiedades que no se encuentran en el TOM, para facilitar determinadas operaciones de modelado. Por ejemplo, al expandir la propiedad **Nombres traducidos**, puedes comparar y editar las traducciones de nombres de objetos en todas las configuraciones regionales del modelo.

### Edición de expresiones DAX

En Visual Studio, puedes usar la barra de fórmulas o abrir una ventana del editor de DAX haciendo clic con el botón derecho en una medida en el Explorador de modelos tabulares y eligiendo "Editar fórmula".

Tabular Editor funciona de forma muy similar; en lugar de la barra de fórmulas, se usa la vista **Editor de expresiones**. Además, si quieres editar las expresiones DAX de uno o varios objetos en un documento independiente, puedes hacer clic con el botón derecho en esos objetos (medidas, columnas calculadas, tablas calculadas) y elegir **Script DAX**.

El editor de código DAX de Tabular Editor 3 es uno de los principales motivos para usar la herramienta. Puedes leer más al respecto [aquí](xref:dax-editor).

### Lista de errores vs. vista de mensajes

En Visual Studio, los errores de sintaxis DAX se muestran como advertencias en la **Lista de errores** (ver la captura de pantalla a continuación). Además, las medidas que tienen errores se indican con un triángulo de advertencia en la cuadrícula de medidas.

![Lista de errores de Visual Studio](~/content/assets/images/vs-error-list.png)

En Tabular Editor, usamos la vista de mensajes para consolidar todos los mensajes de error, advertencia e informativos publicados por distintas fuentes durante el desarrollo del modelo. En concreto, los errores de sintaxis DAX se muestran como errores en la vista de mensajes, y cualquier medida que tenga un error se indica con un punto rojo en el Explorador TOM (ver la captura de pantalla a continuación).

![Mensajes de Tabular Editor](~/content/assets/images/te-messages.png)

En la captura anterior, fíjate en que hay tres fuentes diferentes que publican mensajes:

- **Analysis Services**: Cuando se guardan cambios de metadatos en una instancia conectada de Analysis Services, el servidor actualiza los metadatos TOM para indicar si algún objeto está en un estado erróneo. En concreto, se actualizan las propiedades [State](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.measure.state?view=analysisservices-dotnet#Microsoft_AnalysisServices_Tabular_Measure_State) y [ErrorMessage](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.measure.errormessage?view=analysisservices-dotnet#Microsoft_AnalysisServices_Tabular_Measure_ErrorMessage) de la medida. Tabular Editor muestra estos mensajes de error en la vista de mensajes. Estos mensajes no se muestran cuando Tabular Editor se usa sin conexión (es decir, sin conectarse a Analysis Services).
- **Análisis semántico de Tabular Editor**: Además, Tabular Editor 3 realiza su propio análisis semántico de todas las expresiones DAX del modelo. Cualquier error de sintaxis o de semántica que se encuentre se informa aquí.
- **Editor de expresiones**: Por último, si hay documentos abiertos en Tabular Editor 3, como el Editor de expresiones, cualquier error de sintaxis o de semántica de DAX que se encuentre en el documento se informa aquí.

### Vista previa de los datos de la tabla

En Visual Studio, las tablas y su contenido se muestran en una vista con pestañas una vez que se carga el archivo Model.bim. En Tabular Editor 3, puedes obtener una vista previa de los datos de una tabla haciendo clic con el botón derecho en una tabla del Explorador TOM y seleccionando **Vista previa de datos**. Esto abre una nueva pestaña de documento que te permite desplazarte por todas las filas de la tabla, así como filtrar y ordenar las columnas. ¡Incluso funciona en modelos que usan DirectQuery!

Además, puedes reorganizar los documentos libremente para ver el contenido de varias tablas a la vez (consulta la captura de pantalla siguiente).

![Vista previa de tabla de Te3](~/content/assets/images/te3-table-preview.png)

### Importación de tablas

Para importar nuevas tablas con Tabular Editor 3, usa la opción **Modelo > Importar tablas...**. Esto inicia el Asistente para importar tablas de Tabular Editor 3, que te guía durante el proceso de conectarte a un Data source y seleccionar las tablas que deseas importar. El proceso es bastante similar a la importación de tablas heredada en Visual Studio.

Una diferencia importante es que Tabular Editor 3 no incluye un editor Visual de Power Query. Aun así, puedes editar expresiones de Power Query (M) como texto, pero si tu modelo depende en gran medida de transformaciones de datos complejas expresadas como consultas de Power Query, considera seguir usando Visual Studio para editarlas.

> [!NOTE]
> Por lo general, no se recomienda realizar transformaciones de datos complejas con Power Query para el modelado de datos empresarial, debido a la sobrecarga adicional de las operaciones de actualización de datos. En su lugar, prepara los datos en un esquema en estrella con otras herramientas ETL y almacena los datos del esquema en estrella en una base de datos relacional, como SQL Server o Azure SQL Database. Después, importa las tablas a tu modelo tabular desde esa base de datos.

#### Edición de particiones y actualización del esquema de la tabla

En Tabular Editor 3, puedes actualizar el esquema de una tabla sin forzar una actualización de la tabla. Las particiones se muestran en el Explorador TOM como objetos individuales. Haz clic en una partición para editar su expresión (M o SQL) en el Editor de expresiones.

Una vez actualizada la expresión de una partición, Tabular Editor puede detectar automáticamente si el esquema de la tabla resultante difiere del conjunto de columnas definido en el modelo. Para realizar una actualización del esquema, haz clic con el botón derecho en la partición o la tabla en el Explorador TOM y elige **Actualizar esquema de tabla...**.

Para obtener más información sobre la importación de tablas y las actualizaciones de esquema, consulta @importing-tables.

### Visualización de relaciones

Visual Studio incluye una herramienta de diagramas que te permite visualizar y crear relaciones entre tablas.

Tabular Editor 3 también incluye una herramienta de diagramas a la que puedes acceder desde **Archivo > Nuevo > Diagrama**. Se creará una nueva pestaña de diagrama. Desde ahí podrás agregar tablas desde el Explorador TOM arrastrándolas y soltándolas, o desde el menú **Diagrama > Agregar tablas...**.

Una vez agregadas las tablas al diagrama, puedes crear una relación entre columnas simplemente arrastrando desde una columna a otra.

![Vista de diagrama de Te3](~/content/assets/images/te3-diagram-view.png)

> [!NOTE]
> Por razones de rendimiento, la herramienta de diagramas no inspecciona los datos del modelo ni valida la unicidad o la direccionalidad de las relaciones que crees. Depende de ti asegurarte de que las relaciones se crean correctamente. Si una relación se ha definido incorrectamente, Analysis Services devolverá un estado de error que se mostrará en la **vista de mensajes**.

### Implementación del modelo

Tabular Editor te permite implementar fácilmente los metadatos del modelo en cualquier instancia de Analysis Services. Puedes abrir el Asistente de implementación de Tabular Editor desde **Modelo > Implementar...** o pulsando CTRL+SHIFT+D.

Para obtener más información, consulta [Implementación del modelo](../features/deployment.md).

## Pasos siguientes

- @migrate-from-te2
- @parallel-development
- @boosting-productivity-te3