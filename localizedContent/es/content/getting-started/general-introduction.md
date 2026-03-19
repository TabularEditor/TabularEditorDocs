---
uid: general-introduction
title: Introducción general y arquitectura
author: Daniel Otykier
updated: 2021-09-30
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Introducción general y arquitectura

Tabular Editor es una aplicación de escritorio para Windows que permite desarrollar modelos tabulares. En concreto, la herramienta le permite editar los metadatos del Tabular Object Model (TOM). La herramienta puede cargar los metadatos TOM desde un archivo o desde una base de datos de Analysis Services existente, y también puede implementar metadatos TOM actualizados en Analysis Services.

> [!NOTE]
> Usamos el término **modelo tabular** para referirnos tanto a los modelos tabulares de Analysis Services como a los **Dataset** de Power BI, ya que Analysis Services Tabular es el motor de **Data model** que usa Power BI. Del mismo modo, cuando usamos el término **Analysis Services**, nos referimos a «cualquier instancia de Analysis Services», que puede ser SQL Server Analysis Services, Power BI Desktop o el punto de conexión XMLA del servicio Power BI.

## Metadatos de Tabular Object Model (TOM)

Un **Data model** se compone de varias tablas. Cada tabla tiene una o varias columnas, y también puede contener medidas y jerarquías. Normalmente, el **Data model** también define relaciones entre tablas, uno o varios **Data source** con los detalles de conexión y particiones de tabla que contienen expresiones de origen de datos (consultas SQL o M) para cargar datos, etc. Toda esta información se denomina en conjunto los **metadatos del modelo** y se almacena en un formato basado en JSON conocido como **Tabular Object Model (TOM)**.

- Cuando se crea un modelo tabular con Visual Studio, el JSON que representa los metadatos TOM se guarda en un archivo llamado **Model.bim**.
- Cuando se crea un **Data model** con Power BI Desktop, los metadatos TOM se incrustan en el archivo .pbix o .pbit (ya que este formato de archivo también contiene muchos otros detalles, como definiciones de **Visual**, **Bookmark**, etc., que no están relacionados con el propio **Data model**).

Mediante una biblioteca cliente llamada [AMO/TOM](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions), Tabular Editor puede cargar y guardar metadatos en este formato basado en JSON. Además, la biblioteca cliente permite a Tabular Editor conectarse directamente a cualquier instancia de Analysis Services para obtener los metadatos del modelo desde una base de datos existente. Esto se ilustra en la figura siguiente.

![Architecture](~/content/assets/images/architecture.png)

> [!NOTE]
> En el párrafo anterior, usamos el término **base de datos** para referirnos a un modelo que se ha desplegado en Analysis Services. En el servicio de Power BI se usa el término **Dataset** para referirse a lo mismo, es decir, a un modelo tabular.

Tabular Editor puede cargar los metadatos del modelo desde las siguientes fuentes:

- [1] Archivos Model.bim
- [2] Archivos Database.json (consulta @parallel-development para más información)
- [3] Archivos .pbit (plantilla de Power BI)
- [4] Una base de datos en SQL Server Analysis Services (Tabular)
- [5] Una base de datos en Azure Analysis Services
- [6] Un Dataset en un Workspace de Power BI Premium\*
- [7] Un Report de Power BI Desktop en modo Import/DirectQuery

\*Se requiere una capacidad de Power BI Premium/Embedded o Power BI Premium-Per-User para habilitar el [punto de conexión XMLA](https://docs.microsoft.com/en-us/power-bi/admin/service-premium-connect-tools). El punto de conexión XMLA debe estar habilitado para que cualquier herramienta de terceros pueda conectarse a los Datasets de Power BI.

> [!IMPORTANT]
> Tabular Editor 2.x admite todas las fuentes 1-7 anteriores. Tabular Editor 3 solo admite algunas fuentes, en función de la [edición de Tabular Editor 3](xref:editions) que estés utilizando.

Una vez cargados los metadatos del modelo en Tabular Editor, puedes agregar/editar/eliminar **objetos** y cambiar las **propiedades de los objetos**. Las modificaciones no se guardan en el origen hasta que guardes el modelo de forma explícita, ya sea seleccionando **Archivo > Guardar** o pulsando CTRL+S. Si los metadatos del modelo se cargaron desde una fuente de archivo (fuentes 1-3 anteriores), ese archivo se actualizará. Si los metadatos del modelo se cargaron desde Analysis Services (fuentes 4-7 anteriores), los cambios se guardan de nuevo en Analysis Services. Ten en cuenta que algunos cambios pueden hacer que los objetos pasen a un estado en el que los usuarios finales ya no puedan consultarlos. Por ejemplo, si agregas una columna a una tabla, tendrás que [actualizar la tabla](xref:refresh-preview-query#refreshing-data) antes de que los usuarios puedan consultar el contenido de esa tabla o cualquier medida que dependa de ella.

> [!WARNING]
> Se aplican ciertas limitaciones al guardar nuevamente en Power BI Desktop los cambios en los metadatos del modelo (fuente 7 anterior). Consulta @desktop-limitations para más información.

### Objetos y propiedades de TOM

Los metadatos de TOM se componen de **objetos** y **propiedades**.

Ejemplos de **objetos** de TOM:

- Data Sources
- Tablas
- Particiones
- Medidas
- KPI
- Columnas
- Roles del modelo

Ejemplos de **propiedades de objetos** de TOM:

- `Name` (texto)
- `Carpeta de visualización` (texto)
- `Description` (texto)
- `Hidden` (verdadero/falso)
- `Summarize By` (uno de los siguientes: None, Sum, Min, Max, ...)

La mayoría de las propiedades son valores simples (texto, verdadero/falso, selecciones de una lista, también llamadas. enumeraciones), pero las propiedades también pueden hacer referencia a otros objetos (por ejemplo, la propiedad `Sort By Column` debería hacer referencia a una columna). Las propiedades también pueden ser arreglos de objetos, como la propiedad `Members` del objeto rol del modelo.

Tabular Editor suele usar los mismos nombres para los objetos y las propiedades que los definidos en el [espacio de nombres Microsoft.AnalysisServices.Tabular](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular?view=analysisservices-dotnet). Si quieres saber más sobre objetos o propiedades específicas de TOM, consulta siempre la documentación del espacio de nombres. Por ejemplo, para saber qué hace la propiedad de columna "Summarize By", primero localiza la clase "Column" en la documentación de Microsoft; después, expande "Properties" y desplázate hasta "SummarizeBy". Entonces llegarás a [este artículo](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.column.summarizeby?view=analysisservices-dotnet).

![SummarizeBy en la documentación de Microsoft](~/content/assets/images/asdocs-summarizyby.png)

### Edición de valores de propiedades

Ambas versiones de Tabular Editor muestran los metadatos del modelo de objetos en una vista jerárquica conocida como el **Explorador TOM**, que se corresponde aproximadamente con la estructura jerárquica de los metadatos JSON:

![Explorador TOM](~/content/assets/images/tom-explorer.png)

En general, Tabular Editor te permite modificar las propiedades de los objetos seleccionando primero un objeto en el Explorador TOM (puedes seleccionar varios objetos a la vez manteniendo pulsadas las teclas SHIFT o CTRL) y, después, editando directamente el valor de la propiedad en la **vista de propiedades** (consulta la captura de pantalla a continuación).

![Vista de propiedades](~/content/assets/images/properties-view.png)

Tabular Editor no realiza una validación explícita de los valores de las propiedades modificadas, excepto por algunas reglas básicas (por ejemplo, los nombres de los objetos no pueden estar vacíos, los nombres de las medidas deben ser únicos, etc.). Como desarrollador de modelos tabulares, es tu responsabilidad saber qué propiedades debes establecer y qué valores usar.

Si cometes un error al editar los valores de las propiedades, siempre puedes pulsar CTRL+Z (Editar > Deshacer) para revertir el último cambio de propiedad.

## Arquitectura

Como se indicó anteriormente, Tabular Editor tiene dos modos de funcionamiento: metadatos desde un archivo (también conocido como **modo de archivo**) y metadatos desde Analysis Services (también conocido como **modo conectado**). Además, Tabular Editor 3 introduce un enfoque híbrido llamado [**modo del área de trabajo**](xref:workspace-mode).

Antes de continuar, es importante entender las diferencias entre estos modos:

- En el **modo de archivo**, Tabular Editor carga todos los metadatos del modelo desde un archivo en disco y los guarda de nuevo en ese mismo archivo. En este modo, Tabular Editor no puede interactuar con los **datos** del modelo (es decir, no se habilitan las vistas previas de tabla, las consultas DAX, Pivot Grid ni las operaciones de actualización de datos). Este modo puede usarse completamente sin conexión, incluso cuando no hay ninguna instancia de Analysis Services disponible. Los formatos de archivo compatibles para los metadatos del modelo son:
  - Model.bim (mismo formato que usa Visual Studio)
  - Database.json (estructura de carpetas que solo usa Tabular Editor)
  - .pbit (plantilla de Power BI)
- En el **modo conectado**, Tabular Editor carga los metadatos del modelo desde Analysis Services y los guarda de nuevo en Analysis Services. En este modo, es posible interactuar con los **datos** del modelo con Tabular Editor 3 (vistas previas de tabla, consultas DAX, Pivot Grid y actualización de datos). Este modo requiere conexión a una instancia de Analysis Services.
- En el **modo del área de trabajo**, Tabular Editor 3 carga los metadatos del modelo desde un archivo en disco y los despliega en Analysis Services. En los guardados posteriores (CTRL+S), las actualizaciones se guardan tanto en el disco como en la instancia de Analysis Services conectada. Es posible interactuar con los **datos** del modelo de forma similar al **modo conectado**.

### Sincronización de metadatos

Una de las principales ventajas de Tabular Editor frente a las herramientas estándar (Visual Studio, Power BI Desktop) es que los metadatos del modelo solo se guardan cuando lo solicitas. En otras palabras, puedes hacer varios cambios en objetos y propiedades sin tener que esperar a que una instancia de Analysis Services se sincronice después de cada cambio. La sincronización de la base de datos de Analysis Services es una operación que puede tardar varios segundos en completarse, según el tamaño y la complejidad del Data model. En Power BI Desktop, esta sincronización ocurre cada vez que aparece en pantalla el conocido indicador giratorio "Working on it". En Tabular Editor, esto solo ocurre cuando guardas explícitamente los cambios (CTRL+S).

La desventaja es, por supuesto, que tienes que acordarte de guardar explícitamente los cambios antes de poder probar el impacto de cualquier modificación de metadatos que hayas realizado.

## Próximos pasos

- @installation-activation-basic
- @migrate-from-vs
- @migrate-from-desktop
- @migrate-from-te2