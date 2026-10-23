---
uid: supported-files
title: Tipos de archivo admitidos
author: Morten Lønskov
updated: 2026-10-12
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          partial: true
          note: "Desktop Edition does not support model metadata files"
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# Tipos de archivo admitidos

Tabular Editor 3 utiliza varios formatos de archivo y tipos de documentos diferentes, algunos de los cuales no son utilizados por Analysis Services ni por Power BI. Este artículo ofrece una visión general y una descripción de cada uno de estos tipos de archivo.

![Tipos de archivos compatibles](~/content/assets/images/file-types/te3-supported-file-types.png)

Hay archivos de ejemplo disponibles para cada uno de los distintos tipos de archivo, basados en el caso de negocio del curso 2 de [learn.tabulareditor.com](https://tabulareditor.com/learn).

## Tipos de archivos de conjuntos de datos

Tabular Editor admite cuatro tipos de archivos para modelos semánticos: .bim, archivos de Power BI (.pbit y .pbip), .json y .tmdl. Cada tipo de archivo tiene características y limitaciones diferentes, que se explican a continuación.

Además, las ediciones Business y Enterprise de Tabular Editor 3 permiten **guardar con archivos auxiliares** para la integración de Microsoft Fabric Git. Esto crea una estructura de carpetas que contiene los archivos de metadatos .platform y definition.pbism junto con los archivos de su modelo, lo que permite una sincronización perfecta con los espacios de trabajo de Fabric. Consulte [Guardar con archivos auxiliares](xref:save-with-supporting-files) para obtener más información.

> [!NOTE]
> Dado que **Tabular Editor 3 Desktop Edition** solo está pensada para usarse como herramienta externa para Power BI Desktop, esta edición no permite cargar ni guardar archivos de modelos semánticos. Sin embargo, aún puede usar Tabular Editor 2.x para este fin. Consulta <xref:editions> para obtener más información sobre las diferencias entre las ediciones de Tabular Editor 3.

### [Archivos de modelo tabular (.bim)](#tab/BIM)
Un archivo .bim es un archivo único compuesto por JSON anidado, conocido como TMSL. 

Es el formato original de un modelo semántico compatible con Microsoft. 

Sin embargo, tiene un gran inconveniente: al tratarse de un único archivo de gran tamaño, resulta difícil hacer un seguimiento de los cambios y aplicar buenas prácticas de desarrollo en equipo, como el control de código fuente con Git.

**.bim archivo en una carpeta**

![Tipos de archivos BIM compatibles](~/content/assets/images/file-types/te3-supported-file-bim.png)

[Descargar archivo .bim de ejemplo ](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/bim-file-example.bim)

**Guardar con archivos auxiliares para la integración de Fabric Git**

Al utilizar la opción **Guardar con archivos auxiliares** (ediciones Business y Enterprise), Tabular Editor crea una estructura de carpetas compatible con la integración de Microsoft Fabric Git:

```
DatabaseName.SemanticModel/
├── .platform
├── definition.pbism
└── model.bim
```

Esta estructura te permite confirmar tus modelos semánticos en repositorios Git y sincronizarlos con los espacios de trabajo de Fabric. Consulte [Guardar con archivos auxiliares](xref:save-with-supporting-files) para obtener la documentación completa.


### [Power BI](#tab/PowerBI)

Tabular Editor puede gestionar dos tipos de formatos de almacenamiento de Power BI:

- Archivos de plantilla de Power BI (.pbit)
- Carpetas de proyectos de Power BI (.pbip)



**Carpetas de proyectos de Power BI (.pbip) (Vista previa)**

Las carpetas de Proyectos de Power BI se introdujeron en junio de 2023 y están disponibles en Power BI Desktop como una función de vista previa (también conocida como «Modo desarrollador»). El formato de almacenamiento es una forma alternativa de almacenar el contenido de un archivo .pbix, en un formato más adecuado para el control de versiones y para que terceros puedan leer/editar el contenido.

> [!WARNING]
> Al igual que un archivo .pbix, una carpeta de Proyecto de Power BI puede contener **datos** del modelo además de **metadatos**, por lo que la carpeta debe tratarse como confidencial de la misma manera que debe tratarse un archivo .pbix.

En la raíz de las carpetas del Proyecto de Power BI se encuentra un archivo .pbip. El archivo es básicamente un puntero a un archivo de definición de informe de Power BI, que a su vez puede apuntar a un conjunto de datos de Power BI, ya sea localmente en la misma estructura de carpetas (almacenado como un archivo model.bim) o a un conjunto de datos publicado en el servicio Power BI (en este caso, se dice que el informe está en modo *Conexión en directo*). Si hay un conjunto de datos (archivo model.bim) en la carpeta del Proyecto de Power BI, Tabular Editor podrá cargar los metadatos de este modelo al abrir el archivo .pbip.

Para obtener más información sobre las carpetas de proyectos de Power BI, lea [esta entrada oficial del blog de Microsoft](https://powerbi.microsoft.com/en-us/blog/deep-dive-into-power-bi-desktop-developer-mode-preview/).

> [!IMPORTANT]
> El archivo de proyecto de Power BI es el formato recomendado cuando se utiliza Power BI con Tabular Editor, ya que admite [la gama más amplia de operaciones de modelado](https://learn.microsoft.com/power-bi/developer/projects/projects-overview#model-authoring). Realizar otros tipos de cambios en los metadatos del modelo distintos de los enumerados puede hacer que su modelo no se pueda cargar en Power BI Desktop y, en ese caso, el servicio de asistencia técnica de Microsoft no podrá ayudarle.

**Archivo de plantilla de Power BI (.pbit)**

Los archivos de plantilla de Power BI son similares a los archivos .pbix, con la excepción de que no contienen **datos** del modelo, sino únicamente **metadatos** del modelo. Por lo tanto, estos metadatos del modelo se pueden abrir y editar en Tabular Editor.

> [!WARNING]
> Aunque técnicamente es posible cargar y guardar metadatos del modelo en un archivo .pbit y desde él, Power BI Desktop no admite este enfoque. Tabular Editor mostrará una advertencia y bloqueará los cambios de forma predeterminada. En su lugar, utiliza las carpetas de Proyectos de Power BI si tienes intención de realizar cambios en tu modelo de Power BI a través de Tabular Editor.

### [Carpeta de modelo tabular (.json)](#tab/JSON)

Tabular Editor le permite guardar los objetos de su conjunto de datos como archivos JSON separados, que es un formato de serialización personalizado. 

Este formato conserva la estructura y las propiedades de tus objetos, como tablas, columnas, medidas y relaciones.

Este formato es compatible con Tabular Editor desde sus inicios y es un método probado, aunque no respaldado por Microsoft, para almacenar los objetos de su conjunto de datos como archivos individuales. De este modo, los desarrolladores pueden rastrear los cambios en el control de código fuente y colaborar en la construcción de modelos semánticos.

Existe una compatibilidad total entre Tabular Editor 2 y 3 en lo que respecta a la estructura de los archivos JSON.

Para guardar un modelo semántico en JSON, debe usar la opción «Guardar en carpeta» cuando lo guarde por primera vez. Los guardados posteriores de un modelo cargado a partir de un modelo estructurado en JSON mantienen la configuración. Siempre es posible convertir un modelo que esté en JSON a un archivo con la extensión .bim utilizando «Archivo > Guardar como».


![Tipos de archivos JSON compatibles](~/content/assets/images/file-types/te3-supported-file-json.png)

1. El modelo general tiene una base de datos JSON y cada encabezado TOM tiene su propia carpeta.
2. En las tablas, cada tabla existe en su propia carpeta.
3. Una tabla individual como archivo JSON con el nombre de la tabla y carpetas para medidas, columnas y particiones.
4. Cada una de las medidas de la tabla tiene su propio archivo JSON.

La profundidad de los objetos JSON que se crearán se gestiona mediante la configuración de serialización. 

Un único archivo JSON para una medida contiene todas las propiedades de esa medida:
 
![Tipos de archivos compatibles: archivo JSON](~/content/assets/images/file-types/te3-supported-file-json-measure.png)


Para obtener más información sobre «Guardar en carpeta» y los ajustes de serialización, consulta: [Guardar en carpeta](xref:save-to-folder)

[Descargar ejemplo de estructura de carpetas JSON](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/json-model-example.zip)

### [TMDL](#tab/TMDL)

TMDL son las siglas de «Lenguaje de definición de modelo tabular» y es un nuevo formato para definir y gestionar conjuntos de datos en un formato legible por humanos utilizando una sintaxis similar a YAML. 

Microsoft presentó TMDL como una función de vista previa en abril de 2023, con el objetivo de ofrecer una forma unificada y coherente de trabajar con conjuntos de datos en diferentes plataformas y herramientas. 

TMDL está diseñado para admitir el control de código fuente de los conjuntos de datos, lo que permite a los usuarios rastrear cambios, colaborar y automatizar flujos de trabajo con modelos semánticos. 
> [!NOTE]
> TMDL está en versión preliminar, lo que significa que no es totalmente estable y puede tener algunas limitaciones o problemas. 

![Tipos de archivos TMDL compatibles](~/content/assets/images/file-types/te3-supported-file-tmdl.png)

1. La serialización general se encuentra en el nivel de objeto superior del TOM.
2. Cada tabla es un archivo único.
3. El archivo TMDL consta de una sangría similar a YAML con cada columna y medida dentro del archivo.

Para obtener más información, consulte: [TMDL](xref:tmdl)

[Descargar ejemplo de estructura de carpetas TMDL](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/tmdl-model-example.zip)

**Guardar con archivos auxiliares para la integración de Fabric Git**

Al utilizar la opción **Guardar con archivos auxiliares** (ediciones Business y Enterprise), Tabular Editor crea una estructura de carpetas compatible con la integración de Microsoft Fabric Git:

```
DatabaseName.SemanticModel/
├── .platform
├── definition.pbism
└── definition/
    ├── database.tmdl
    ├── tables.tmdl
    └── ...
```

El formato TMDL legible por humanos es especialmente adecuado para el control de versiones y las revisiones de código cuando se utiliza la integración de Git de Fabric. Consulte [Guardar con archivos auxiliares](xref:save-with-supporting-files) para obtener la documentación completa.

***

## Archivos de integración de Fabric con Git

Al utilizar la función **Guardar con archivos auxiliares** (ediciones Business y Enterprise), Tabular Editor crea archivos de metadatos adicionales necesarios para la integración de Microsoft Fabric Git. Estos archivos se generan y gestionan automáticamente por Tabular Editor.

### .platform

El archivo .platform contiene metadatos sobre el elemento del modelo semántico, que incluyen:
- **type**: Identifica el elemento como un SemanticModel
- **displayName**: El nombre que se muestra en los espacios de trabajo de Fabric (sincronizado a partir de la propiedad `Name` de la base de datos)
- **description**: La descripción que se muestra en Fabric (sincronizada a partir de la propiedad `Description` de la base de datos)
- **logicalId**: Un identificador entre áreas de trabajo generado automáticamente

Este archivo es un archivo JSON que no debe editarse manualmente a menos que comprenda el formato de los elementos de Fabric.

> [!NOTE]
> Esta sincronización se aplica a un modelo cuyos metadatos llevan un nombre o una descripción. Un modelo semántico de Proyecto de Power BI (PBIP) creado por Power BI Desktop no contiene ninguno de los dos en su TMDL: ambos solo existen en el archivo «.platform».

### definition.pbism

El archivo definition.pbism contiene la definición general y los ajustes principales del modelo semántico. Este archivo funciona junto con los metadatos del modelo (almacenados como model.bim o en la carpeta definition/) para proporcionar la información completa del modelo semántico que requiere Microsoft Fabric.

Ambos archivos se crean automáticamente cuando marca la opción **Guardar con archivos auxiliares** durante las operaciones de guardado. La estructura de carpetas resultante (con el sufijo .SemanticModel) se puede confirmar en repositorios de Git y sincronizar con los espacios de trabajo de Fabric.

Para obtener documentación completa sobre esta función, consulte [Guardar con archivos auxiliares](xref:save-with-supporting-files).

## Archivos de compatibilidad de Tabular Editor

Los archivos de soporte son archivos que no utilizan Analysis Services ni Power BI. En cambio, todos estos archivos admiten diferentes tipos de flujos de trabajo de desarrollo en Tabular Editor 3 y otras herramientas.

Todos los archivos auxiliares se pueden guardar individualmente usando Ctrl+S o «Archivo > Guardar» mientras el documento o la ventana correspondiente están abiertos y seleccionados. 

### Opciones de usuario (.tmuo)

Un archivo «.tmuo» contiene su propia configuración local del equipo para un modelo: la base de datos del área de trabajo, las anulaciones de credenciales de la fuente de datos, la configuración de importación de tablas, las anulaciones de actualización y las concesiones de permisos de IA. Se encuentra junto al modelo y lleva el nombre de este y su nombre de usuario de Windows, de modo que varios desarrolladores pueden trabajar en el mismo modelo sin interferir entre sí.

Las credenciales que contiene están cifradas con tu clave de usuario de Windows, lo que significa que el archivo no se puede compartir de forma útil. Añada «*.tmuo» a «.gitignore».

Consulte @user-options para ver el contenido completo y dónde se escribe el archivo para cada formato de modelo.

### Archivo de diagrama (.te3diag)

Un archivo .te3diag es un formato de archivo que almacena el diagrama de un modelo creado con TE3. 

Estos archivos pueden ser útiles para documentar la estructura y la lógica del modelo para otros desarrolladores que trabajen en el mismo proyecto. Un archivo .te3diag se puede guardar en la misma carpeta que el archivo del modelo para facilitar el acceso y la consulta.

Los archivos de diagrama son en realidad archivos JSON que se almacenan en una extensión de Tabular Editor 3.

[Descargar archivo de diagrama de ejemplo](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/te3-diagram.te3diag)

### Archivos de consultas DAX (.dax o .msdax)

Las consultas DAX son expresiones que se pueden utilizar para manipular y analizar datos en modelos semánticos. Un archivo DAX es un archivo de texto que contiene una o más consultas DAX. 

Puedes guardar un archivo DAX en Tabular Editor 3 y usarlo más tarde para volver a ejecutar las consultas. También puedes abrir un archivo DAX en otras herramientas compatibles con DAX, como [DAX Studio](https://daxstudio.org).

[Descargar archivo DAX de ejemplo](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/dax-query-example.dax)

Estos archivos solo se pueden abrir mientras Tabular Editor 3 está conectado a una instancia de Analysis Services o al punto de conexión XMLA de Power BI / Fabric.

### Estructuras de Pivot Grid (.te3pivot)

Estos archivos contienen la estructura de un Pivot Grid en Tabular Editor 3. Son archivos JSON sencillos que especifican qué campos (medidas, columnas, jerarquías) se muestran en el Pivot Grid y cómo están organizados.

Estos archivos solo se pueden abrir mientras Tabular Editor 3 está conectado a una instancia de Analysis Services o al punto de conexión XMLA de Power BI / Fabric.

### Scripts DAX (.te3daxs)

Estos archivos son scripts DAX guardados (no consultas) que se utilizan en Tabular Editor para manipular muchos objetos DAX a la vez. Por ejemplo, para modificar varias medidas en un modelo semántico.

### Scripts de C# (.csx)

Crear y editar C# Scripts es una de las funciones de productividad más importantes de Tabular Editor.

Estos scripts se pueden guardar como archivos con la extensión .csc y cargarse en Tabular Editor, así como guardarse como macros. Tabular Editor mantiene un [archivo de configuración local MacroActions.json](xref:supported-files#macroactionsjson).

De esta manera, los scripts se pueden reutilizar sin tener que escribirlos desde cero cada vez. La [biblioteca de scripts](xref:csharp-script-library) es un buen lugar para investigar y reutilizar varios ejemplos de scripts, ya que muestran diferentes características y funcionalidades de C#. 

[Descargar archivo de ejemplo de script de C#](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/create-sum-measures-csharp.csx)

### Archivos de Vertipaq Analyzer (.vpax)

Con Tabular Editor, puede exportar e importar archivos .vpax utilizando la función Vertipaq Analyzer. Un archivo .vpax es un archivo comprimido que contiene información sobre el tamaño y la estructura de tu modelo semántico, pero no los datos reales. 

Puedes usar este archivo para analizar y optimizar el rendimiento de tu modelo, sin exponer datos confidenciales. Por ejemplo, puede usar la herramienta [DAX Optimizer](https://www.daxoptimizer.com/) para obtener sugerencias sobre cómo mejorar sus fórmulas DAX basándose en el archivo .vpax.

[Descargar archivo de ejemplo de Script DAX](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/dax-script-example.te3daxs)

A diferencia de otros tipos de archivos compatibles, la creación de un archivo .vpax se realiza en la ventana de Vertipaq Analyzer utilizando los botones «Importar» y «Exportar». 

![VPAX](~/content/assets/images/file-types/te3-supported-file-vpax.png)

[Descargar archivo VPAX de ejemplo](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/vpaq-example.vpax)

> [!WARNING]
> Si los metadatos de su modelo son confidenciales, un archivo .vpax también debe considerarse confidencial y solo debe compartirse teniendo esto en cuenta. Si le preocupa proteger la propiedad intelectual, Tabular Editor 3 tiene una opción para ofuscar los archivos VPAX.

### Archivos VPAX ofuscados (.ovpax)

Si necesita entregar el archivo VPAX a un tercero, como un consultor o un proveedor de herramientas, puede ofuscar el archivo para ocultar los metadatos del modelo. Para ello, seleccione la opción «Exportación ofuscada...» en el botón desplegable situado junto al botón «Exportar» de la ventana del analizador Vertipaq.

Un archivo VPAX ofuscado utiliza la extensión de archivo .ovpax.

![Exportar VPAX ofuscado](~/content/assets/images/obfuscated-vpax.png)

Para obtener más documentación sobre Vertipaq Analyzer, consulte: [sqlbi Vertipaq Analyzer](https://www.sqlbi.com/tools/vertipaq-analyzer) y [Documentación de sqlbi: Vertipaq Analyzer](https://docs.sqlbi.com/vertipaq-analyzer/)

Para obtener más información sobre la ofuscación de archivos VPAX, consulte: [Ofuscador VPAX](https://www.sqlbi.com/blog/marco/2024/03/15/vpax-obfuscator-a-library-to-obfuscate-vpax-files/)

## Archivos de configuración local

Tabular Editor mantiene varios archivos locales en la carpeta «%localappdata%\TabularEditor3». Estos archivos son funcionalmente relevantes para Tabular Editor 3 y es útil conocerlos.

Puede ser útil compartir estos archivos en un equipo para que todos los desarrolladores tengan las mismas macros y reglas BPA.

> [!TIP]
> Una forma nativa de Windows de sincronizar un archivo con control de versiones en la carpeta «%localappdata%\TabularEditor3» es utilizar [SymLink](https://www.howtogeek.com/16226/complete-guide-to-symbolic-links-symlinks-on-windows-or-linux/).
>
> Almacene los archivos necesarios en Git o OneDrive y cree un enlace simbólico a la carpeta «%localappdata%\TabularEditor3», pero tenga en cuenta que esto podría provocar problemas de sincronización si varios usuarios actualizan la misma versión del archivo.
> Sin embargo, Tabular Editor no admite esto directamente, así que impleméntelo a su propia discreción. 


### Registro de auditoría de IA

Solo está presente cuando se instala el componente de funciones de IA. Tabular Editor registra lo que hicieron el [Asistente de IA](xref:ai-assistant) y el [servidor MCP](xref:mcp-server): qué permisos se solicitaron y cómo se respondió a ellos, qué herramientas se ejecutaron y si cada una tuvo éxito, falló o fue rechazada, y el texto completo de cualquier script de C# que se ejecutara o se entregara para su revisión. Las indicaciones, las respuestas y los valores de datos de tu modelo nunca se registran.

Los archivos se escriben a razón de uno por día y se conservan durante 30 días de forma predeterminada. Acceda a la carpeta con **Abrir carpeta de auditoría** en **Herramientas > Preferencias > Funciones de IA**. Los administradores pueden moverla y cambiar el período de conservación mediante [políticas](xref:policies). Consulta @ai-audit-log para saber qué contiene cada registro.

A diferencia de los demás archivos de esta carpeta, este es un registro, no una configuración. No lo comparta ni lo sincronice: es un registro por equipo, y los scripts que contiene pueden revelar la estructura de los modelos en los que ha trabajado.

### MacroActions.json
Este archivo almacena todas las macros que has creado o importado. Puede ser útil compartir este archivo con sus compañeros o hacer una copia de seguridad en un sistema de control de versiones, y también se puede configurar para que se sincronice con un repositorio remoto que contenga macros (véase el consejo anterior).

Este archivo contiene el índice de cada macro que se utiliza en el software. Si necesita cambiar el orden o el nombre de alguna macro, puede editar este archivo manualmente con un editor de texto. Sin embargo, tenga cuidado de no introducir errores o incoherencias en el archivo que puedan dañarlo, así que asegúrese de crear una copia de seguridad.

[Descargar archivo MacroActions de ejemplo](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/MacroActions.json)


### BPARules.json
El archivo contiene las [reglas del Best Practice Analyzer](xref:using-bpa) y las expresiones de corrección. El único lugar para añadir y editar expresiones de corrección es dentro de este archivo JSON.
Se recomienda almacenar el archivo de reglas del BPA en el control de versiones, lo que también permite ejecutar las reglas del BPA en el modelo semántico antes de la implementación. 

Puedes descargar las reglas BPA oficiales de Microsoft aquí: [Reglas BPA](https://raw.githubusercontent.com/microsoft/Analysis-Services/master/BestPracticeRules/BPARules.json)

### RecentServers.json
Contiene los servidores a los que se ha conectado, con el tipo de autenticación, el nombre de usuario, el modo y el color de la barra de estado guardados para cada uno, así como la lista de servidores anclados. Las contraseñas no se almacenan. Para eliminar o anclar un servidor, haga clic derecho sobre él en la lista **Servidor** del cuadro de diálogo de conexión. Consulte [Servidores recientes y anclados](xref:xmla-as-connectivity#recent-and-pinned-servers).

### Layouts.json
Tabular Editor genera automáticamente el archivo Layouts al iniciar la aplicación. Contiene toda la información sobre cómo se configura el diseño de la interfaz de usuario de Tabular Editor 3.

> [!TIP]
> Si elimina este archivo, se restablecerá el diseño de Tabular Editor. Si el diseño de Tabular Editor no se comporta como se espera, un buen primer paso es hacer una copia de seguridad de este archivo en otro lugar, eliminar el original y reiniciar Tabular Editor 3.
