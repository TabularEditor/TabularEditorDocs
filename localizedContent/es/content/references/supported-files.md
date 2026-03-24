---
uid: supported-files
title: Tipos de archivo compatibles
author: Morten Lønskov
updated: 2023-10-17
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Escritorio
          partial: true
          note: "La Edición de escritorio no admite archivos de metadatos del modelo"
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

<a name="supported-file-types"></a>
# Tipos de archivo compatibles

Tabular Editor 3 utiliza varios formatos de archivo y tipos de documento, algunos de los cuales no se usan en Analysis Services ni en Power BI. Este artículo ofrece una descripción general y una explicación de cada uno de estos tipos de archivo.

![Tipos de archivo compatibles](~/content/assets/images/file-types/te3-supported-file-types.png)

Hay archivos de ejemplo disponibles para cada tipo de archivo, basados en el caso práctico “Business Case” del curso 2 de [learn.tabulareditor.com](https://tabulareditor.com/learn).

## Tipos de archivo del Dataset

Tabular Editor admite cuatro tipos de archivo para modelos semánticos: .bim, archivos de Power BI (.pbit y .pbip), .json y .tmdl. Cada tipo de archivo tiene características y limitaciones distintas, que se explican a continuación.

Además, las ediciones Business y Edición Enterprise de Tabular Editor 3 admiten **guardar con archivos auxiliares** para la integración de Git de Microsoft Fabric. Esto crea una estructura de carpetas que contiene los archivos de metadatos .platform y definition.pbism junto a los archivos de tu modelo, lo que permite una sincronización fluida con los Workspaces de Fabric. Consulta [Guardar con archivos auxiliares](xref:save-with-supporting-files) para obtener más información.

> [!NOTE]
> Dado que **Tabular Editor 3 Edición de escritorio** solo está diseñado para usarse como herramienta externa de Power BI Desktop, esta edición no permite cargar ni guardar archivos de modelo semántico. No obstante, puedes seguir usando Tabular Editor 2.x para este fin. Consulta <xref:editions> para obtener más información sobre las diferencias entre las ediciones de Tabular Editor 3.

### [Archivos de modelo tabular (.bim)](#tab/BIM)

Un archivo .bim es un único archivo que contiene JSON anidado, conocido como TMSL.

Es el formato original de un modelo semántico que Microsoft admite.

Sin embargo, tiene un gran inconveniente: al ser un único archivo grande, es difícil hacer seguimiento de los cambios y aplicar buenas prácticas de desarrollo en equipo, como el control de versiones con Git.

#### Archivo «.bim» en una carpeta

![Supported File Types BIM](~/content/assets/images/file-types/te3-supported-file-bim.png)

[Descarga el archivo de ejemplo .bim](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/bim-file-example.bim)

#### Guardar con archivos auxiliares para la integración de Git de Fabric

Al usar la opción **Guardar con archivos auxiliares** (ediciones Business y Edición Enterprise), Tabular Editor crea una estructura de carpetas compatible con la integración de Git de Microsoft Fabric:

```
DatabaseName.SemanticModel/
├── .platform
├── definition.pbism
└── model.bim
```

Esta estructura te permite realizar commits de tus modelos semánticos en repositorios Git y sincronizarlos con los Workspaces de Fabric. Consulta [Guardar con archivos auxiliares](xref:save-with-supporting-files) para ver la documentación completa.

### [Power BI](#tab/PowerBI)

Tabular Editor puede trabajar con dos tipos de formatos de almacenamiento de Power BI:

- Archivos de plantilla de Power BI (.pbit)
- Carpetas del Proyecto de Power BI (.pbip)

#### Carpetas del Proyecto de Power BI (.pbip) _(Versión preliminar)_

Las carpetas del Proyecto de Power BI se introdujeron en junio de 2023 y están disponibles en Power BI Desktop como una funcionalidad en versión preliminar (también conocida como "Modo de desarrollador"). Este formato de almacenamiento es una forma alternativa de guardar el contenido de un archivo .pbix, en un formato más compatible con el control de versiones y con la lectura/edición del contenido por parte de terceros.

> [!WARNING]
> Al igual que un archivo .pbix, una carpeta del Proyecto de Power BI puede contener **datos** del modelo además de **metadatos**; por tanto, debe tratarse como información confidencial, del mismo modo que un archivo .pbix.

En la raíz de las carpetas del Proyecto de Power BI se encuentra un archivo .pbip. En esencia, el archivo es un puntero a un archivo de definición de informe de Power BI, que a su vez puede apuntar a un Dataset de Power BI: ya sea de forma local, en la misma estructura de carpetas (almacenado como un archivo model.bim), o a un Dataset publicado en el servicio de Power BI (en este caso, se considera que el Report está en modo _Live connect_). Si hay un Dataset (archivo model.bim) en la carpeta del Proyecto de Power BI, Tabular Editor podrá cargar estos metadatos del modelo al abrir el archivo .pbip.

Para obtener más información sobre las carpetas del Proyecto de Power BI, consulta [esta entrada oficial del blog de Microsoft](https://powerbi.microsoft.com/en-us/blog/deep-dive-into-power-bi-desktop-developer-mode-preview/).

> [!IMPORTANT]
> El archivo del Proyecto de Power BI es el formato recomendado cuando usas Power BI con Tabular Editor, ya que admite la [gama más amplia de operaciones de modelado](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview#model-authoring). Realizar cambios en los metadatos del modelo distintos de los enumerados puede hacer que el modelo deje de poder cargarse en Power BI Desktop; en ese caso, el Soporte técnico de Microsoft no podrá ayudarte.

#### Archivo de plantilla de Power BI (.pbit)

Los archivos de plantilla de Power BI son similares a los archivos .pbix, con la diferencia de que no contienen **datos** del modelo; solo **metadatos** del modelo. Por tanto, estos metadatos del modelo se pueden abrir y editar en Tabular Editor.

> [!WARNING]
> Aunque técnicamente es posible cargar metadatos del modelo desde un archivo .pbit y volver a guardarlos en un .pbit, este enfoque no está admitido por Power BI Desktop. Tabular Editor mostrará una advertencia y bloqueará los cambios de forma predeterminada. En su lugar, usa carpetas del Proyecto de Power BI si tienes previsto hacer cambios en tu modelo de Power BI a través de Tabular Editor.

### [Carpeta de modelo tabular (.json)](#tab/JSON)

Tabular Editor te permite guardar los objetos de tu Dataset como archivos JSON independientes, usando un formato de serialización personalizado.

Este formato conserva la estructura y las propiedades de tus objetos, como tablas, columnas, medidas y relaciones.

Este formato es compatible con Tabular Editor desde sus inicios y es un método probado —aunque Microsoft no lo admite— para almacenar los objetos del Dataset como archivos individuales. De este modo, los desarrolladores pueden hacer un seguimiento de los cambios en el control de código fuente y colaborar en la creación de modelos semánticos.

Hay compatibilidad total entre Tabular Editor 2 y 3 en lo que respecta a la estructura de archivos JSON.

Para guardar un modelo semántico en JSON, debes usar la opción "Guardar en carpeta" la primera vez que lo guardes. Los guardados posteriores de un modelo cargado desde un modelo estructurado en JSON mantienen la configuración. siempre es posible convertir un modelo que está en JSON a un archivo .bim usando 'Archivo > Guardar como'

![Tipos de archivo compatibles JSON](~/content/assets/images/file-types/te3-supported-file-json.png)

1. El modelo completo incluye un archivo json de la base de datos y cada encabezado TOM tiene su propia carpeta
2. En la carpeta tables, cada tabla tiene su propia carpeta
3. Una tabla individual como un archivo json de TableName con carpetas para medidas, columnas y particiones
4. Las medidas de la tabla tienen cada una su propio archivo json.

La configuración de serialización gestiona la profundidad de los objetos json que se crearán.

Un único archivo JSON para una medida contiene todas las propiedades de esa medida:

![Tipos de archivo compatibles: archivo JSON de una medida](~/content/assets/images/file-types/te3-supported-file-json-measure.png)

Para más información sobre Guardar en carpeta y la configuración de serialización, consulta: [Guardar en carpeta](xref:save-to-folder)

[Descargar ejemplo de estructura de carpetas JSON](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/json-model-example.zip)

### [TMDL](#tab/TMDL)

TMDL significa Tabular Model Definition Language y es un nuevo formato para definir y administrar los Dataset en un formato legible para las personas, usando una sintaxis similar a YAML.

Microsoft presentó TMDL como una característica en versión preliminar en abril de 2023, con el objetivo de ofrecer una forma unificada y coherente de trabajar con los Dataset en distintas plataformas y herramientas.

TMDL está diseñado para admitir el control de código fuente de los Dataset, lo que permite a los usuarios hacer un seguimiento de los cambios, colaborar y automatizar flujos de trabajo con modelos semánticos.

> [!Note]
> TMDL está en versión preliminar, lo que significa que aún no es totalmente estable y puede tener algunas limitaciones o problemas.

![Tipos de archivo compatibles TMDL](~/content/assets/images/file-types/te3-supported-file-tmdl.png)

1. La serialización general se realiza en el nivel del objeto superior de TOM
2. Cada tabla es un único archivo
3. El archivo TMDL usa una sangría similar a la de YAML e incluye cada columna y medida dentro del archivo.

Para ampliar información, consulta: [TMDL](xref:tmdl)

[Descargar ejemplo de estructura de carpetas TMDL](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/tmdl-model-example.zip)

#### Guardar con archivos auxiliares para la integración de Git de Fabric

Al usar la opción **Guardar con archivos auxiliares** (ediciones Business y Edición Enterprise), Tabular Editor crea una estructura de carpetas compatible con la integración de Git de Microsoft Fabric:

```
DatabaseName.SemanticModel/
├── .platform
├── definition.pbism
└── definition/
    ├── database.tmdl
    ├── tables.tmdl
    └── ...
```

El formato TMDL legible para humanos es especialmente adecuado para el control de versiones y las revisiones de código cuando se usa la integración de Git de Fabric. Consulta [Guardar con archivos auxiliares](xref:save-with-supporting-files) para ver la documentación completa.

***

## Archivos de integración de Git de Fabric

Al usar la característica **Guardar con archivos auxiliares** (ediciones Business y Edición Enterprise), Tabular Editor crea archivos de metadatos adicionales necesarios para la integración de Git de Microsoft Fabric. Tabular Editor genera y gestiona estos archivos automáticamente.

### .platform

El archivo .platform contiene metadatos sobre el elemento de modelo semántico, incluidos:

- **type**: Identifica el elemento como SemanticModel
- **displayName**: El nombre que se muestra en los Workspaces de Fabric (sincronizado desde la propiedad `Name` de `Database`)
- **description**: La descripción que se muestra en Fabric (sincronizada desde la propiedad `Description` de `Database`)
- **logicalId**: Un identificador entre Workspaces generado automáticamente

Este archivo JSON no debe editarse manualmente a menos que entiendas el formato de elementos de Fabric.

### definition.pbism

El archivo definition.pbism contiene la definición general y la configuración principal del modelo semántico. Este archivo funciona junto con los metadatos del modelo (almacenados como model.bim o en la carpeta definition/) para proporcionar la información completa del modelo semántico que requiere Microsoft Fabric.

Ambos archivos se crean automáticamente cuando seleccionas la opción **Save with supporting files** durante las operaciones de guardado. La estructura de carpetas resultante (con el sufijo .SemanticModel) puede confirmarse en repositorios de Git y sincronizarse con los Workspaces de Fabric.

Para consultar la documentación completa de esta característica, consulta [Save with supporting files](xref:save-with-supporting-files).

## Archivos de soporte de Tabular Editor

Los archivos de soporte son archivos que no utilizan Analysis Services ni Power BI. En su lugar, estos archivos sirven de apoyo a distintos flujos de trabajo de desarrollo en Tabular Editor 3 y otras herramientas.

Todos los archivos auxiliares se pueden guardar individualmente con Ctrl+S o con 'Archivo > Guardar', siempre que tengas abierto y en primer plano el documento o la ventana correspondiente.

<a name="diagram-file-te3diag"></a>
### Archivo de diagrama (.te3diag)

Un archivo .te3diag es un archivo que almacena el diagrama de un modelo creado con TE3.

Estos archivos pueden ser útiles para documentar la estructura y la lógica del modelo para otros desarrolladores que trabajen en el mismo proyecto. Un archivo .te3diag se puede guardar en la misma carpeta que el archivo del modelo para facilitar el acceso y la consulta.

Los archivos de diagrama en realidad son archivos JSON almacenados en una extensión de Tabular Editor 3.

[Descargar archivo de diagrama de ejemplo](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/te3-diagram.te3diag)

### Archivos de consulta DAX (.dax o .msdax)

Las consultas DAX son expresiones que se pueden usar para manipular y analizar datos en modelos semánticos. Un archivo DAX es un archivo de texto que contiene una o varias consultas DAX.

Puedes guardar un archivo DAX en Tabular Editor 3 y usarlo más adelante para volver a ejecutar las consultas. También puedes abrir un archivo DAX en otras herramientas que admitan DAX, como [DAX Studio](https://daxstudio.org).

[Descargar archivo DAX de ejemplo](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/dax-query-example.dax)

Estos archivos solo se pueden abrir cuando Tabular Editor 3 está conectado a una instancia de Analysis Services o al punto de conexión XMLA de Power BI / Fabric.

### Diseños de Pivot Grid (.te3pivot)

Estos archivos contienen el diseño de un Pivot Grid en Tabular Editor 3. Son archivos JSON sencillos que especifican qué campos (medidas, columnas, jerarquías) se muestran en el Pivot Grid y cómo se organizan.

Estos archivos solo se pueden abrir cuando Tabular Editor 3 está conectado a una instancia de Analysis Services o al punto de conexión XMLA de Power BI / Fabric.

### Scripts DAX (.te3daxs)

Estos archivos son Scripts DAX guardados (no consultas) que se usan en Tabular Editor para manipular varios objetos DAX a la vez. Por ejemplo, modificar varias medidas en un modelo semántico.

### C# Script (.csx)

Crear y editar C# Scripts es una de las funciones de productividad más potentes de Tabular Editor.

Estos scripts se pueden guardar como archivos con la extensión .csc, cargarse en Tabular Editor y también guardarse como macros. Tabular Editor mantiene un [archivo de configuración local llamado MacroActions.json](xref:supported-files#macroactionsjson).

Así, puedes reutilizar los scripts sin tener que escribirlos desde cero cada vez. La [biblioteca de scripts](xref:csharp-script-library) es un buen lugar para explorar y reutilizar varios ejemplos de scripts, ya que muestran distintas características y funcionalidades de C#.

[Descargar archivo de ejemplo de script de C#](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/create-sum-measures-csharp.csx)

### Archivos de VertiPaq Analyzer (.vpax)

Con Tabular Editor, puedes exportar e importar archivos .vpax con la función VertiPaq Analyzer. Un archivo .vpax es un archivo comprimido que contiene información sobre el tamaño y la estructura de tu modelo semántico, pero no los datos reales.

Puedes usar este archivo para analizar y optimizar el rendimiento del modelo, sin exponer datos confidenciales. Por ejemplo, puedes usar la herramienta [DAX optimizer](https://www.daxoptimizer.com/) para obtener sugerencias sobre cómo mejorar tus fórmulas DAX en función del archivo .vpax.

[Descargar archivo de ejemplo de script DAX](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/dax-script-example.te3daxs)

A diferencia de otros tipos de archivos compatibles, la creación de un archivo .vpax se realiza en la ventana de VertiPaq Analyzer mediante los botones 'Import' y 'Export'.

![VPAX](~/content/assets/images/file-types/te3-supported-file-vpax.png)

[Descargar archivo VPAX de ejemplo](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/vpaq-example.vpax)

> [!WARNING]
> Si los metadatos de tu modelo son confidenciales, un archivo .vpax también debe considerarse confidencial y compartirse únicamente teniendo esto en cuenta. Si te preocupa proteger la propiedad intelectual, Tabular Editor 3 ofrece una opción para ofuscar archivos VPAX.

#### Ofuscación

Si necesitas entregar el archivo VPAX a un tercero, como un consultor o un proveedor de herramientas, puedes ofuscarlo para ocultar los metadatos del modelo. Para hacerlo, selecciona la opción "Obfuscated Export..." en el menú desplegable junto al botón "Export" en la ventana de VertiPaq Analyzer.

Un archivo VPAX ofuscado usa la extensión .ovpax.

![Export obfuscated VPAX](~/content/assets/images/obfuscated-vpax.png)

Para más documentación sobre VertiPaq Analyzer, consulta: [sqlbi Vertipaq Analyzer](https://www.sqlbi.com/tools/vertipaq-analyzer) y [sqlbi Docs: Vertipaq Analyzer](https://docs.sqlbi.com/vertipaq-analyzer/)

Para más información sobre la ofuscación de archivos VPAX, consulta: [VPAX Obfuscator](https://www.sqlbi.com/blog/marco/2024/03/15/vpax-obfuscator-a-library-to-obfuscate-vpax-files/)

## Archivos de configuración local

Tabular Editor mantiene varios archivos locales en la carpeta "%localappdata%\TabularEditor3". Estos archivos son funcionalmente relevantes para Tabular Editor 3 y conviene conocerlos.

Te puede resultar útil compartir estos archivos con el equipo para que todos los desarrolladores tengan las mismas macros y reglas de BPA.

> [!TIP]
> Una forma nativa de Windows de sincronizar un archivo con control de versiones en la carpeta "%localappdata%\TabularEditor3" es usar [SymLink](https://www.howtogeek.com/16226/complete-guide-to-symbolic-links-symlinks-on-windows-or-linux/).
>
> Guarda los archivos necesarios en Git u OneDrive y crea un Symlink a la carpeta "%localappdata%\TabularEditor3", pero ten en cuenta que esto puede acabar causando problemas de sincronización si varios usuarios actualizan la misma versión del archivo.
> Sin embargo, Tabular Editor no lo admite directamente, así que impleméntalo bajo tu propia responsabilidad.

### MacroActions.json

Este archivo almacena todas las macros que hayas creado o importado. Te puede resultar útil compartir este archivo con tus compañeros o guardarlo como copia de seguridad en un sistema de control de versiones. También puedes configurarlo para que se sincronice con un repositorio remoto que contenga macros (consulta el consejo anterior).

Este archivo contiene el índice de cada macro que se utiliza en la aplicación. Si necesitas cambiar el orden o el nombre de alguna macro, puedes editar este archivo manualmente con un editor de texto. Eso sí: ten cuidado de no introducir errores o incoherencias en el archivo, ya que podrías corromperlo; asegúrate de crear una copia de seguridad.

[Descargar archivo MacroActions.json de ejemplo](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/MacroActions.json)

### BPARules.json

El archivo contiene las [reglas de Best Practice Analyzer](xref:using-bpa) y expresiones de corrección. El único lugar donde puedes añadir y editar expresiones de corrección es este archivo JSON.
Se recomienda almacenar el archivo de reglas de BPA en un sistema de control de versiones, lo que también permite ejecutar las reglas de BPA contra el modelo semántico antes del despliegue.

Puedes descargar aquí las reglas oficiales de BPA de Microsoft: [PBA Rules](https://raw.githubusercontent.com/microsoft/Analysis-Services/master/BestPracticeRules/BPARules.json)

### RecentServers.json

Contiene todos los servidores a los que te has conectado. Te puede venir bien editarlo manualmente para "olvidar" servidores anteriores que ya no sean relevantes.

### Layouts.json

El archivo Layouts lo genera automáticamente Tabular Editor al iniciar la aplicación. Contiene toda la información sobre cómo se configura el diseño de la interfaz de usuario de Tabular Editor 3.

> [!TIP]
> Si eliminas este archivo, se restablecerá el diseño de Tabular Editor. Si el diseño de Tabular Editor no se comporta como esperas, un buen primer paso es guardar una copia de seguridad de este archivo en otro lugar, eliminar el original y reiniciar Tabular Editor 3.
