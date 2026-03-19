---
uid: migrate-from-desktop
title: Migración desde Power BI Desktop
author: Daniel Otykier
updated: 2021-09-30
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

# Migración desde Power BI Desktop

Si ya estás familiarizado con los conceptos de modelado de datos en Power BI Desktop, este artículo pretende ayudarte a migrar el modelado de tu Data model a Tabular Editor. Por tanto, asumimos que tienes un sólido conocimiento de conceptos como el Editor de Power Query, las tablas importadas frente a las tablas calculadas, las columnas calculadas, las medidas, etc.

## Power BI y Tabular Editor

Históricamente, Tabular Editor se diseñó como una herramienta para desarrolladores de SQL Server Analysis Services (Tabular) y de Azure Analysis Services. Cuando se lanzó Power BI por primera vez, no había ninguna forma admitida para que las herramientas de terceros accedieran a la instancia de Analysis Services que alojaba el Data model de Power BI, así que la única manera de crear y editar un Dataset de Power BI era mediante Power BI Desktop.

Esto cambió en marzo de 2020, cuando [Microsoft anunció el punto de conexión XMLA de lectura/escritura en Power BI Premium](https://powerbi.microsoft.com/en-us/blog/announcing-read-write-xmla-endpoints-in-power-bi-premium-public-preview/). Unos meses después, incluso fue posible usar herramientas de terceros junto con Power BI Desktop, con el [anuncio de la función Herramientas externas](https://powerbi.microsoft.com/en-us/blog/announcing-public-preview-of-external-tools-in-power-bi-desktop/).

La disponibilidad del punto de conexión XMLA en Power BI Premium permite a los desarrolladores de Data model aprovechar sus habilidades y herramientas existentes, y no es ningún secreto que Microsoft está invirtiendo mucho en hacer de [Power BI Premium un superconjunto de Analysis Services](https://community.powerbi.com/t5/Webinars-and-Video-Gallery/Power-BI-Premium-as-a-superset-of-Analysis-Services-the-XMLA/m-p/1434121). En otras palabras, la integración de herramientas de terceros, tanto de la comunidad como comerciales, con Power BI es algo que ha llegado para quedarse. De hecho, Amir Netz, CTO de Microsoft Analytics, hizo una [declaración conjunta](https://powerbi.microsoft.com/en-us/blog/community-tools-for-enterprise-powerbi-and-analysisservices/) con Marco Russo, fundador de SQLBI, para reafirmar este punto.

En Tabular Editor ApS, creemos firmemente que Tabular Editor 3 es la mejor herramienta de modelado tabular de Data model disponible ahora mismo y, gracias a las integraciones mencionadas, ya no está reservada para los desarrolladores de SQL Server o de Azure Analysis Services.

Antes de continuar, es importante entender que Tabular Editor se puede usar junto con Power BI en dos escenarios muy diferentes:

- **Escenario 1:** Tabular Editor como herramienta externa para Power BI Desktop.
- **Escenario 2:** Tabular Editor con el punto de conexión XMLA de Power BI Premium.

> [!IMPORTANT]
> No puedes usar Tabular Editor para cargar directamente un archivo .pbix. Para más información, consulta <xref:desktop-limitations#power-bi-file-types>.

### Escenario 1: Tabular Editor como herramienta externa para Power BI Desktop

En general, este escenario está pensado para analistas de autoservicio y usuarios de Power BI Desktop sin acceso a Power BI Premium, para facilitar determinadas operaciones de modelado del Data model (por ejemplo, agregar y editar medidas) y para habilitar opciones avanzadas de modelado que, de otro modo, no estarían disponibles (grupos de cálculo, perspectivas y traducciones de metadatos).

Las herramientas externas se conectan al modelo de Analysis Services hospedado por Power BI Desktop. Esto permite que la herramienta realice determinados cambios en el Data model. Sin embargo, actualmente no todos los tipos de operaciones de modelado del Data model están admitidos por Power BI Desktop. Es importante entender esta limitación y cómo se comporta Tabular Editor cuando se usa como herramienta externa para Power BI Desktop. Consulta <xref:desktop-limitations> para obtener más información al respecto.

El flujo de trabajo típico en este escenario es el siguiente:

1. Abre un archivo .pbit o .pbix en Power BI Desktop
2. Inicia Tabular Editor desde la cinta de opciones Herramientas externas
3. Ve alternando entre Tabular Editor y Power BI Desktop, según el tipo de cambio que necesites realizar. Por ejemplo, puedes agregar y editar medidas con Tabular Editor, pero debes usar Power BI Desktop si necesitas agregar una nueva tabla al modelo.
4. Cada vez que hagas un cambio en Tabular Editor, usa **Archivo > Guardar** (CTRL+S) para guardar los cambios en Power BI Desktop.
5. Cuando termines de hacer cambios, cierra Tabular Editor. Después, publica o guarda el Report como de costumbre desde Power BI Desktop.

> [!NOTE]
> A partir de octubre de 2021, hay un error en Power BI Desktop que a veces impide que Power BI Desktop actualice automáticamente la lista de campos y los Visuales para reflejar los cambios realizados con herramientas externas. Cuando esto ocurre, guarda el archivo .pbix y vuelve a abrirlo, o actualiza manualmente una tabla del modelo; por lo general, esto hace que la lista de campos y todos los Visuales se actualicen correctamente.

Las [limitaciones de modelado](xref:desktop-limitations) que se aplican a las herramientas externas solo son relevantes en lo que respecta a operaciones de escritura o modificaciones del modelo. Aun así, puedes usar las funciones conectadas de Tabular Editor 3 para explorar los datos del modelo mediante vistas previas de los datos de las tablas, Pivot Grids o consultas DAX, como se describe más adelante en esta guía.

### Escenario 2: Tabular Editor con el punto de conexión XMLA de Power BI Premium

Este escenario está dirigido a profesionales de BI en organizaciones que usan capacidad de Power BI Premium o Workspaces de Power BI Premium por usuario, y que pretenden reemplazar por completo Power BI Desktop para el desarrollo de Datasets.

En esencia, el punto de conexión XMLA de Power BI Premium expone una instancia de Analysis Services (Tabular). En este escenario, Tabular Editor se comporta igual que cuando está conectado a Azure Analysis Services o a SQL Server Analysis Services (Tabular).

El flujo de trabajo típico en este escenario es el siguiente:

1. Al migrar por primera vez a Tabular Editor, usa el punto de conexión XMLA para abrir un Dataset de Power BI en Tabular Editor y después guarda los metadatos del modelo como un archivo (Model.bim) o una carpeta (Database.json). Consulta @parallel-development para obtener más información.
2. A partir de ahí, abre en Tabular Editor los metadatos del modelo desde el archivo o la carpeta que guardaste en el paso 1. Opcionalmente, usa el [modo del área de trabajo](xref:workspace-mode).
3. Aplica los cambios con Tabular Editor.
4. Si usas el modo del área de trabajo, los cambios deberían ser visibles de inmediato en el servicio de Power BI cada vez que pulses Guardar (CTRL+S) en Tabular Editor.
5. Si no usas el modo del área de trabajo o cuando hayas terminado de hacer cambios, usa la opción **Model > Deploy...** de Tabular Editor para publicar los cambios en el servicio de Power BI.

Dado que, en este escenario, la "fuente de verdad" de los metadatos del modelo es la estructura de archivos o carpetas almacenada en disco, este enfoque no solo permite el desarrollo en paralelo con integración del control de versiones, sino también la integración continua y la entrega/despliegue continuos (CI/CD) mediante un servidor de compilación automatizado como Azure DevOps.

> [!WARNING]
> En cuanto apliques cambios a un Dataset de Power BI a través del punto de conexión XMLA del servicio de Power BI, ese Dataset ya no se podrá descargar como archivo .pbix. Consulta [Conectividad del Dataset con el punto de conexión XMLA](https://docs.microsoft.com/en-us/power-bi/admin/service-premium-connect-tools#power-bi-desktop-authored-datasets) para obtener más información.

Cuando usas Tabular Editor para conectarte al Dataset mediante el punto de conexión XMLA, no hay limitaciones en cuanto a los tipos de operaciones de escritura o modificaciones del modelo que se pueden realizar.

El resto de este artículo se centra en las diferencias entre Power BI Desktop y Tabular Editor para el desarrollo de Data model. Algunas secciones solo se aplican al escenario 2, debido a las [limitaciones de modelado](xref:desktop-limitations) que se aplican cuando se usa Tabular Editor como herramienta externa para Power BI Desktop (escenario 1).

## Interfaz de usuario de Tabular Editor 3

Si eres nuevo en Tabular Editor, te recomendamos revisar los siguientes recursos para entender la interfaz de usuario de Tabular Editor 3:

- [Conoce la interfaz de usuario de Tabular Editor 3](xref:user-interface)
- [Vista del Explorador TOM](xref:tom-explorer-view)
- [vista de propiedades](xref:properties-view)
- [Editor de DAX](xref:dax-editor)

## Guías prácticas de Tabular Editor 3

A continuación encontrarás un recorrido rápido para realizar tareas habituales en Tabular Editor 3.

### Cómo agregar una medida

Para agregar una nueva medida al modelo, haz clic con el botón derecho en la tabla del **Explorador TOM** donde quieres que se ubique la nueva medida y selecciona **Crear > Medida** (atajo ALT+1). Después de agregar la medida, puedes escribir inmediatamente su nombre.

![Agregar medida](~/content/assets/images/add-measure.png)

### Cómo cambiar el nombre de una medida

Si necesitas editar el nombre de la medida (o de cualquier otro objeto), solo tienes que seleccionar la medida y pulsar F2 (o hacer doble clic en el nombre de la medida). Si seleccionas varios objetos, verás el cuadro de diálogo «Renombrar en lote», que facilita renombrar varios objetos de una sola vez.

![Renombrar en lote](~/content/assets/images/batch-rename.png)

> [!WARNING]
> Cambiar los nombres de los objetos en el Data model puede provocar que los Visual del Report dejen de funcionar, si los Visual dependen de uno o varios de los objetos cuyo nombre se haya cambiado. Las herramientas externas no pueden acceder a la información sobre los Visuales de Power BI, por lo que Tabular Editor no puede avisarte antes de que se renombre o se elimine un objeto que se use en un Visual.

### Cómo crear una copia de una medida

En Tabular Editor 3, puedes usar las conocidas operaciones Cortar (CTRL+X), Copiar (CTRL+C) y Pegar (CTRL+V) para mover objetos rápidamente y crear copias. También puedes arrastrar objetos entre tablas y carpetas de visualización con el **Explorador TOM**. Si cometes un error durante el proceso, puedes usar las opciones Deshacer (CTRL+Z) y Rehacer (CTRL+Y) (repetidamente) para desplazarte hacia atrás y hacia delante por el historial de cambios aplicados.

### Cómo modificar la expresión DAX de una medida

Busca la medida que quieres modificar en el **Explorador TOM** y selecciónala. Puedes alternar la visualización de objetos ocultos (CTRL+6) y de carpetas de visualización (CTRL+5) con los botones de la barra de herramientas cerca de la parte superior del Explorador TOM. También puedes escribir parte del nombre de la medida en el cuadro de búsqueda para filtrar el **Explorador TOM**.

Una vez seleccionada la medida, verás su expresión DAX en el **Editor de expresiones** y varias propiedades, como `Description`, `Format String`, `Hidden`, etc., en la cuadrícula de **Propiedades**.

![Modificar medida](~/content/assets/images/modify-measure.png)

Para modificar la expresión DAX, solo tienes que colocar el cursor en el **Editor de expresiones** y actualizar el código DAX. Pulsa F6 para dar formato al código automáticamente. Si seleccionas otro objeto en el Explorador TOM o haces clic en el botón con la marca de verificación verde **Expression > Accept** (F5), el cambio en la expresión se guarda localmente en Tabular Editor. También puedes cancelar la modificación que has hecho pulsando la "X" roja, en **Expression > Cancel**. Si pulsas **Accept** por accidente, siempre puedes deshacer el cambio con la opción **Edit > Undo** (CTRL+Z).

Para guardar los cambios en Power BI Desktop, en el punto de conexión XMLA de Power BI o en el archivo en disco desde el que se cargó el modelo, pulsa **File > Save** (CTRL+S).

Para obtener más información sobre las capacidades del Editor de expresiones al escribir código DAX, consulta <xref:dax-editor>.

### Cómo visualizar las dependencias entre medidas

Con una medida seleccionada en el **Explorador TOM**, usa la opción **Measure > Show dependencies** (SHIFT+F12). Esto hace que se abra una nueva ventana que muestra el árbol de dependencias de la expresión DAX de esa medida. Puedes alternar entre ver las dependencias ascendentes y descendentes.

![Show Dependencies](~/content/assets/images/show-dependencies.png)

Al hacer doble clic en un elemento de la vista de dependencias, se navegará hasta ese objeto en el **Explorador TOM**.

### Cómo cambiar la cadena de formato de una medida

Busca la medida que quieres modificar en el **Explorador TOM** y selecciónala. Puedes alternar la visualización de los objetos ocultos (CTRL+6) y las carpetas de visualización (CTRL+5) mediante los botones de la barra de herramientas situados en la parte superior del Explorador TOM. También puedes escribir parte del nombre de la medida en el cuadro de búsqueda para filtrar el **Explorador TOM**.

Una vez seleccionada la medida, busca la propiedad `Format String` en la cuadrícula de **Properties**, expándela y ajusta la cadena de formato según tus preferencias. Fíjate en el botón desplegable a la derecha de la propiedad `Format`. También puedes escribir libremente una cadena de formato directamente en la propiedad `Format String`.

![Format String](~/content/assets/images/format-string.png)

### Cómo modificar la expresión DAX de varias medidas

Tabular Editor 3 te permite seleccionar varias medidas para crear un **Script DAX**, con el que puedes modificar la expresión DAX y varias propiedades de todas las medidas seleccionadas a la vez.

Para crear un Script DAX basado en medidas existentes, solo tienes que seleccionar las medidas en el **Explorador TOM** (mantén pulsada la tecla CTRL para seleccionar varios objetos o la tecla SHIFT para seleccionar un rango de objetos). Después, haz clic con el botón derecho y selecciona **Script DAX**.

![Script Dax](~/content/assets/images/script-dax.png)

Puedes agregar o modificar propiedades como `Description`, `FormatString`, `Visible`, `DetailRows` y otras directamente en el script.

Pulsa F5 para aplicar el script al Data model. Ten en cuenta que, a diferencia del **Editor de expresiones**, al navegar a otro objeto no se aplicarán automáticamente los cambios realizados en el script. También puedes usar la opción **Edit > Undo** (CTRL+Z) para deshacer cualquier cambio aplicado por un Script DAX.

Consulta @dax-script-introduction para obtener más información.

### Cómo previsualizar datos en una tabla

Para ver el contenido de una tabla (similar a la pestaña Datos de Power BI Desktop), haz clic con el botón derecho en una tabla y elige "Preview data". Esto abrirá una nueva pestaña con una vista previa del contenido de la tabla. Puedes desplazarte por todas las filas de la tabla y aplicar ordenación o filtrado a las columnas. A diferencia de Power BI Desktop, puedes abrir tantas de estas pestañas de vista previa como quieras y organizarlas una junto a otra en la interfaz de usuario. La vista previa también funciona con tablas en [modo DirectQuery](https://docs.microsoft.com/en-us/power-bi/connect-data/desktop-use-directquery) (aunque la vista previa se limitará a los primeros 100 registros).

![Vista previa de datos](~/content/assets/images/preview-data.png)

> [!NOTE]
> La función **Vista previa de datos** solo está disponible cuando Tabular Editor está conectado a Power BI Desktop o a un Dataset en el punto de conexión XMLA de Power BI.

Consulta @refresh-preview-query para obtener más información.

### Cómo agregar un grupo de cálculo

Los [grupos de cálculo](https://docs.microsoft.com/en-us/analysis-services/tabular-models/calculation-groups?view=asallproducts-allversions) son útiles para definir y reutilizar un contexto de filtro de DAX modificado u otro tipo de lógica de negocio en todas las medidas del modelo. Para agregar un grupo de cálculo con Tabular Editor, usa la opción **Modelo > Nuevo grupo de cálculo** (ALT+7).

![Agregar grupo de cálculo](~/content/assets/images/add-calc-group.png)

Asigna un nombre al grupo de cálculo y, con el grupo de cálculo seleccionado en el **Explorador TOM**, agrega nuevos elementos de cálculo mediante la opción **Tabla del grupo de cálculo > Crear > Elemento de cálculo**. Puedes copiar (CTRL+C) y pegar (CTRL+V) elementos de cálculo para agilizar este proceso al crear elementos adicionales.

![Agregar elemento de cálculo](~/content/assets/images/add-calc-item.png)

### Cómo agregar una nueva tabla

Para agregar una tabla nueva a un modelo, usa la opción **Modelo > Importar tablas...**. El [Asistente para importar tablas](xref:importing-tables) de Tabular Editor te guiará durante el proceso.

> [!NOTE]
> Tabular Editor 3 no es compatible con todos los Data sources que admite Power BI. Si tu modelo usa un Data source que Tabular Editor no admite, la forma más sencilla de importar una tabla nueva desde el mismo Data source es copiar una tabla existente en Tabular Editor (CTRL+C / CTRL+V) y luego modificar la expresión de la partición y actualizar el esquema de la tabla, como se muestra a continuación. Para que esto funcione, asegúrate de que esté habilitada la opción **Herramientas > Preferencia > Comparación de esquema > Usar Analysis Services para la detección de cambios**. Consulta <xref:importing-tables#updating-table-schema-through-analysis-services> para obtener más información.

> [!IMPORTANT]
> Esta opción no está disponible de forma predeterminada al usar Tabular Editor como herramienta externa, ya que [Power BI Desktop no admite](xref:desktop-limitations) agregar o editar tablas mediante herramientas externas.

Consulta @importing-tables-data-modeling para obtener más información.

### Cómo modificar una expresión de Power Query en una tabla

Las expresiones de Power Query (M) que definen lo que se carga en cada tabla se encuentran en la **partición** correspondiente de la tabla. Puedes encontrar las particiones en el **Explorador TOM**. Al seleccionar una partición, Tabular Editor muestra la expresión M de esa partición en el **Editor de expresiones**, lo que te permite editarla. Tras editar y aceptar el cambio de expresión, puedes hacer clic con el botón derecho en la partición del **Explorador TOM** y elegir la opción **Actualizar esquema de la tabla...** para detectar si deben cambiarse las columnas importadas en la tabla, en función de la expresión actualizada de Power Query.

![Power Query: actualizar el esquema](~/content/assets/images/power-query-update-schema.png)

> [!NOTE]
> Actualmente, Tabular Editor 3 no realiza ninguna validación de la expresión de la partición. Para expresiones de Power Query (M), esto está previsto para una actualización posterior de Tabular Editor 3.

> [!IMPORTANT]
> Las expresiones de partición son de solo lectura de forma predeterminada al usar Tabular Editor como herramienta externa, ya que la edición de particiones mediante herramientas externas [no es compatible con Power BI Desktop](xref:desktop-limitations).

Si los cambios en la expresión de Power Query provocan modificaciones en las columnas importadas de la tabla, se mostrará un cuadro de diálogo que te permitirá revisarlas:

![Aplicar cambios de esquema](~/content/assets/images/combine-sourcecolumn-update.png)

### Cómo modificar una expresión compartida de Power Query

Las expresiones compartidas son consultas M que no se usan directamente para cargar datos en una tabla. Por ejemplo, cuando creas un parámetro de Power Query en Power BI Desktop, la expresión M de ese parámetro se almacena como una expresión compartida. En Tabular Editor, se puede acceder a ellas desde la carpeta Expresiones compartidas del **Explorador TOM** y editarlas igual que las consultas M de las particiones.

![Expresión compartida](~/content/assets/images/shared-expression.png)

> [!IMPORTANT]
> Las expresiones compartidas son de solo lectura de forma predeterminada al usar Tabular Editor como herramienta externa, ya que la edición de particiones mediante herramientas externas [no es compatible con Power BI Desktop](xref:desktop-limitations).

### Cómo agregar relaciones entre tablas

La forma más sencilla de agregar relaciones entre dos tablas es crear un nuevo diagrama, agregar ambas tablas al diagrama y, después, arrastrar una columna de una tabla a otra para indicar qué columnas deben participar en la relación. Esto es similar a cómo crearías una relación en Power BI Desktop.

1. Para crear un nuevo diagrama, usa la opción **Archivo > Nuevo > Diagrama**.
2. Para agregar tablas al diagrama, arrastra y suelta las tablas desde el **Explorador TOM** o usa la opción **Diagrama > Agregar tablas...**.
3. Una vez agregadas las tablas, busca la columna en la tabla de hechos (lado de muchos) y arrástrala a la columna correspondiente en la tabla de dimensiones (lado de uno).
4. Confirma la configuración de la relación y pulsa "OK".

![Crear relación mediante diagrama](~/content/assets/images/create-relationship-through-diagram.gif)

Consulta [Trabajar con diagramas](xref:importing-tables-data-modeling#working-with-diagrams) para obtener más información.

> [!IMPORTANT]
> Las relaciones no se pueden modificar al usar Tabular Editor como herramienta externa, ya que la edición de relaciones mediante herramientas externas [no es compatible con Power BI Desktop](xref:desktop-limitations).

### Cómo publicar en Power BI Service

Para publicar o actualizar un Dataset en el Power BI Service, usa la opción **Modelo > Implementar...** y especifica el punto de conexión XMLA del Workspace en el que quieras publicarlo.

Si cargaste los metadatos del modelo directamente desde el punto de conexión XMLA, solo tienes que hacer clic en **Archivo > Guardar** (CTRL+S) para actualizar el Dataset que se cargó en Tabular Editor.

> [!NOTE]
> La opción **Model > Deploy...** **no** está disponible en Tabular Editor 3 Edición de escritorio, ya que esta edición está pensada únicamente para usarse como herramienta externa para Power BI Desktop. [Más información](xref:editions).

## Pasos siguientes

- <xref:user-interface>
- @parallel-development
- @boosting-productivity-te3
- <xref:new-pbi-model>