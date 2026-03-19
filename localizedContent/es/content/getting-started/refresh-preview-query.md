---
uid: refresh-preview-query
title: Actualización, vista previa y consulta de datos
author: Daniel Otykier
updated: 2026-01-08
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

# Actualización, vista previa y consulta de datos

Cuando Tabular Editor 3 se conecta a una instancia de Analysis Services, se habilitan varias **funciones conectadas** adicionales que le permiten usar Tabular Editor 3 como herramienta cliente para Analysis Services.

> [!NOTE]
> La expresión "conectado a una instancia de Analysis Services" se refiere a cualquiera de las siguientes opciones:
>
> - Cargar un modelo en el [**modo del área de trabajo**](xref:workspace-mode)
> - Cargar un modelo directamente desde SQL Server Analysis Services, Azure Analysis Services o el punto de conexión XMLA de Power BI
> - Usar Tabular Editor 3 como herramienta externa para Power BI Desktop

En resumen, estas funciones conectadas son:

- Operaciones de actualización de datos
- Vista previa de datos de las tablas
- PivotGrids
- Consulta DAX
- Analizador VertiPaq

# Actualización de datos

Tabular Editor no inicia automáticamente operaciones de actualización en Analysis Services cuando se realizan cambios en el Data model. Esto se hace así por diseño, para garantizar que guardar los cambios de metadatos en Analysis Services no lleve demasiado tiempo. Una operación de actualización puede tardar mucho en completarse; durante ese tiempo, no se puede actualizar ningún metadato adicional en el servidor. Como contrapartida, puede hacer cambios con Tabular Editor, lo que hace que el modelo pase a un estado en el que solo se puede consultar parcialmente o no se puede consultar en absoluto. Según el tipo de cambio realizado en el Data model, puede que necesites aplicar distintos niveles de actualización.

En general, los siguientes cambios requieren una actualización completa antes de poder consultar el objeto mencionado (es decir, una actualización de datos seguida de una actualización de cálculo):

- Agregar una nueva tabla al modelo
- Agregar una nueva columna a una tabla

En general, los siguientes cambios requieren una actualización de cálculo:

- Cambiar la expresión DAX de una tabla calculada o de una columna calculada
- Agregar o modificar una relación
- Agregar, cambiar el nombre o quitar un elemento de cálculo de un grupo de cálculo

Cabe destacar que añadir, modificar o quitar medidas a un modelo no requiere ningún tipo de actualización (a menos que la medida esté referenciada por una columna calculada; en ese caso, habrá que recalcular la tabla en la que se encuentra esa columna).

Para iniciar una actualización con Tabular Editor, haz clic con el botón derecho en la tabla o partición que quieras actualizar, ve a **Actualizar tabla** o **Actualizar partición** y elige el tipo de actualización que quieres ejecutar.

![Actualizar tabla](~/content/assets/images/refresh-table.png)

También puedes iniciar una actualización a nivel de modelo desde el menú **Modelo > Actualizar modelo**. Una vez iniciada la operación de actualización, verás el texto "Data refresh started... <ins>Ver cola de actualizaciones</ins>". Haz clic en el enlace o abre la vista **Actualización de datos** desde la opción de menú **Vista > Actualización de datos**. Esto mostrará una lista de todas las operaciones de actualización (tanto las pasadas como las que están en curso), con los mensajes de estado devueltos por Analysis Services, incluidos los contadores de progreso y la duración, y te permitirá cancelar una actualización iniciada por error.

![Vista de actualización de datos](~/content/assets/images/data-refresh-view2.png)

> [!TIP]
> La vista de actualización de datos incluye una columna **Hora de inicio** que muestra cuándo comenzó cada operación de actualización. Haz clic en el encabezado de la columna para ordenar las operaciones cronológicamente; así verás primero las actualizaciones más recientes. Puedes ordenar por cualquier columna para organizar las operaciones de actualización según tus necesidades. Consulta la [vista de actualización de datos](xref:data-refresh-view) para obtener más información.

Mientras una actualización está en curso, puedes seguir trabajando en tu Data model, consultando y previsualizando datos o poniendo en cola nuevas operaciones de actualización de datos, tal como se describe en este artículo. Sin embargo, no podrás guardar los cambios del modelo en Analysis Services hasta que finalicen todas las operaciones de actualización de datos.

## Operaciones de actualización compatibles

Tabular Editor 3 admite operaciones de actualización en distintos tipos de objetos. Los tipos de actualización compatibles se muestran a continuación:

- **Modelo** (Automática, cálculo, completa)
- **Tabla (importada)** (Automática, cálculo, solo datos, completa)
- **Partición** (Completa)
- **Tabla calculada** (Calculate)
- **Grupo de cálculo** (Calculate)

Consulta [Tipos de actualización](https://docs.microsoft.com/en-us/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions#request) para obtener más información sobre los tipos de operaciones de actualización compatibles con Analysis Services / Power BI.

# Vista previa de los datos de la tabla

En determinados momentos, durante la creación de DAX y el desarrollo del Data model, es posible que necesites inspeccionar el contenido de tus tablas fila por fila. Por supuesto, podrías escribir una consulta DAX para hacerlo, pero Tabular Editor 3 lo pone aún más fácil al permitirte previsualizar los datos de la tabla directamente. Para ello, haz clic con el botón derecho en una tabla y elige la opción **Vista previa de datos**.

![Preview Data](~/content/assets/images/preview-data-big.png)

Puedes abrir varias vistas previas de tabla y organizarlas como quieras en la interfaz de usuario. Además, puedes ordenar o filtrar columnas individuales. No hay un límite práctico para el número de filas que se pueden previsualizar. Tabular Editor simplemente ejecuta una consulta DAX [`TOPNSKIP`](https://dax.guide/topnskip) contra el modelo y devuelve solo un número reducido de registros, suficiente para rellenar la vista actual.

Si una o más columnas calculadas están en un estado no válido, esas columnas contienen el texto _(Calculation needed)_. Puedes recalcular la tabla haciendo clic con el botón derecho en la columna y eligiendo la opción **Recalcular tabla...**.

![Recalculate Table](~/content/assets/images/recalculate-table.png)

# Pivot Grid

Después de agregar o editar medidas DAX en un modelo, es habitual que los desarrolladores del modelo prueben estas medidas. Tradicionalmente, esto solía hacerse con herramientas cliente como Excel o Power BI. Con Tabular Editor 3, ahora puedes usar **Pivot Grid**, que se comportan de forma muy parecida a las conocidas tablas dinámicas de Excel. Pivot Grid te permite crear rápidamente vistas resumidas de los datos de tu modelo, lo que te permite probar el comportamiento de tus medidas DAX al filtrar y segmentar por varias columnas y jerarquías.

Para crear una nueva Pivot Grid, usa la opción **Archivo > Nuevo > Pivot Grid**. Desde aquí, puedes arrastrar medidas, columnas y jerarquías desde el Explorador TOM a la cuadrícula, o bien usar la opción de menú **Pivot Grid > Mostrar campos** para ver una lista emergente de todos los campos que se pueden arrastrar a la Pivot Grid (consulta la captura de pantalla a continuación).

![Show Fields Pivot](~/content/assets/images/show-fields-pivot.png)

A medida que se arrastran campos a la Pivot Grid, Tabular Editor genera consultas MDX que se envían a Analysis Services para mostrar los datos resultantes. En este sentido, el comportamiento es muy similar al de las tablas dinámicas de Excel. Puedes reorganizar los campos del Pivot Grid arrastrándolos y soltándolos, y hay varias opciones en el menú contextual para personalizar la forma en que se muestran los datos.

![Personalizar Pivot Grid](~/content/assets/images/customizing-pivot-grids.png)

El Pivot Grid se actualiza automáticamente cuando se realiza un cambio en el modelo o finaliza una operación de actualización. Puedes activar o desactivar esta actualización automática en el menú **Pivot Grid**.

# Consultas DAX

Una forma más directa de consultar los datos de tu modelo es escribir una consulta DAX. Usa la opción de menú **Archivo > Nuevo > Consulta DAX** para crear un nuevo documento de consulta DAX. Puedes tener varios documentos de consulta DAX abiertos al mismo tiempo.

Las consultas DAX se pueden guardar y cargar desde archivos independientes usando la extensión `.dax` o `.msdax`. Consulta @supported-files para obtener más información.

Escribe tu consulta DAX `EVALUATE` en el editor y pulsa **Consulta > Ejecutar** (F5) para enviar la consulta a Analysis Services y ver el resultado. De forma predeterminada, Tabular Editor 3 limita a 1000 el número de filas devueltas por Analysis Services, pero esto se puede cambiar en **Herramientas > Preferencias > Navegación de datos > Consulta DAX**. Si una consulta supera este límite, Tabular Editor 3 muestra un acceso directo que te permite recuperar todos los registros (consulta la captura de pantalla a continuación).

![Límite de filas del conjunto de resultados de la consulta](~/content/assets/images/query-rowset-limit.png)

> [!WARNING]
> Mostrar un gran número de registros en la ventana de resultados de la consulta podría tardar un rato y aumentar drásticamente la memoria consumida por Tabular Editor 3.

Tabular Editor 3 usa el mismo editor de código DAX para editar consultas que para definir expresiones DAX en los objetos. Por tanto, están disponibles todas las funciones de autocompletado, formato automático, etc. Consulta @dax-editor para obtener más información. Además, como una consulta DAX tiene una sintaxis ligeramente distinta a las expresiones de objetos, el editor de consultas DAX ofrece algunas opciones adicionales para tareas comunes.

Por ejemplo, si haces clic con el botón derecho en una referencia a una medida, aparece la opción **Definir medida**, como se ve en la captura de pantalla siguiente. Esta opción añadirá una instrucción `DEFINE MEASURE` en la parte superior de tu consulta DAX, lo que te permitirá modificar fácilmente la expresión DAX de esa medida dentro del ámbito de la consulta.

![Funciones de la Consulta Dax](~/content/assets/images/dax-query-features.png)

Además, una consulta DAX puede contener varias instrucciones `EVALUATE`. En ese caso, Tabular Editor 3 muestra el resultado de cada instrucción en una pestaña numerada independiente. Si solo quieres ejecutar una única instrucción `EVALUATE`, aunque tu documento contenga varias, puedes colocar el cursor en cualquier parte de la instrucción que quieras ejecutar y, a continuación, usar la opción **Consulta > Ejecutar selección** (SHIFT+F5).

Una Consulta DAX en Tabular Editor 3 se actualiza automáticamente cuando se realiza un cambio en el modelo o cuando finaliza una operación de actualización. Puedes activar o desactivar esta función de actualización automática en el menú **Consulta**.

# Suplantación

Al consultar los datos del modelo, a veces resulta útil poder suplantar a un usuario específico o una combinación de roles, para ver cómo se comporta el modelo desde la perspectiva de un usuario final. Tabular Editor 3 te permite suplantar a un usuario específico o a uno o varios roles haciendo clic en el botón **Suplantar...**. Esto se aplica a las [Vistas previas de tabla](#previewing-table-data), los [Pivot Grid](#pivot-grids) y las [Consultas DAX](#dax-queries).

> [!NOTE]
> Para suplantar a un usuario, Tabular Editor agrega la propiedad [`EffectiveUserName`](https://docs.microsoft.com/en-us/analysis-services/instances/connection-string-properties-analysis-services?view=asallproducts-allversions#effectiveusername) a la cadena de conexión al conectarse a Analysis Services. Para suplantar un rol, Tabular Editor agrega la propiedad [`Roles`](https://docs.microsoft.com/en-us/analysis-services/instances/connection-string-properties-analysis-services?view=asallproducts-allversions#roles) a la cadena de conexión. Esto solo se aplica a la vista de datos (es decir, la Consulta DAX, el Pivot Grid o la Vista previa de tabla) en la que se especifica la suplantación.

Al hacer clic en el botón **Suplantación...** (que también puedes encontrar en el menú **Consulta**, **Pivot Grid** o **Vista previa de tabla**, según el tipo de vista de datos activa), se abre un cuadro de diálogo que te permite especificar un usuario o seleccionar uno o varios roles.

![Seleccionar suplantación](~/content/assets/images/select-impersonation.png)

Una vez habilitada la suplantación, el botón **Suplantación...** queda marcado y se aplicará a la vista de datos actual. Al hacer clic en la pequeña flecha junto al botón **Suplantación...**, puedes ver y cambiar rápidamente entre las 10 suplantaciones más recientes que has usado.

![Menú desplegable de suplantación](~/content/assets/images/impersonation-dropdown.png)

Cuando la actualización automática está habilitada en una vista de datos, cambiar la suplantación actualizará la vista de inmediato.

## CustomData

La característica CustomData permite pasar un valor de cadena personalizado que puede usarse en expresiones DAX, normalmente para implementar escenarios dinámicos de seguridad a nivel de filas. Esta característica se puede combinar con cualquiera de las opciones de suplantación descritas anteriormente, incluida la opción **Sin suplantación**.

![Seleccionar suplantación](~/content/assets/images/impersonation-customdata.png)

Cuando introduces un valor en el campo de entrada **CustomData**, Tabular Editor 3 agrega la propiedad [`CustomData`](https://docs.microsoft.com/en-us/analysis-services/instances/connection-string-properties-analysis-services?view=asallproducts-allversions#customdata) a la cadena de conexión. A continuación, puedes recuperar este valor en tus expresiones DAX mediante la [`función CUSTOMDATA()`](https://dax.guide/customdata/).

CustomData se usa habitualmente para implementar seguridad a nivel de filas dinámica cuando una aplicación utiliza autenticación personalizada. El valor que proporciones puede utilizarse en las expresiones de filtro del rol para controlar qué filas pueden ver los usuarios en función de los datos personalizados que se pasan a través de la cadena de conexión.

Esta característica es especialmente útil en escenarios de **Power BI Embedded**, donde puedes utilizar CustomData de forma nativa para agregar filtros de fila que transmitan texto libre (cadenas) y así aprovechar la seguridad a nivel de filas dinámica en Reports, Dashboards y Tiles integrados.

**Ejemplo de caso de uso:** Podrías pasar el departamento o la región de un usuario como CustomData y, luego, usar ese valor en la expresión de filtro de un rol, por ejemplo:

```dax
'Department'[DepartmentCode] = CUSTOMDATA()
```

# Analizador VertiPaq

Tabular Editor 3 incluye una versión de la herramienta de código abierto [Analizador VertiPaq](https://www.sqlbi.com/tools/vertipaq-analyzer/), creada por [SQLBI](https://sqlbi.com). El Analizador VertiPaq es útil para analizar las estructuras de almacenamiento VertiPaq de tu Data model de Power BI o de un Data model tabular.

Con Tabular Editor 3, puedes recopilar estadísticas del Analizador VertiPaq mientras estás conectado a cualquier instancia de Analysis Services. También puedes exportar las estadísticas como un [archivo .vpax](https://www.youtube.com/watch?v=zRa9y01Ub30) o importar estadísticas desde un archivo .vpax.

Para recopilar estadísticas, simplemente haz clic en el botón **Recopilar estadísticas** en la vista **Analizador VertiPaq**.

![Analizador VertiPaq: Recopilar estadísticas](~/content/assets/images/vertipaq-analyzer-collect-stats.png)

Una vez recopiladas las estadísticas, el Analizador VertiPaq muestra un resumen del tamaño del modelo, el número de tablas, etc. Puedes encontrar estadísticas más detalladas en las pestañas **Tablas**, **Columnas**, **Relaciones** y **Particiones**.

Además, siempre que se hayan cargado estadísticas, Tabular Editor 3 mostrará información de cardinalidad y tamaño en una información sobre herramientas al pasar el cursor del ratón sobre los objetos del Explorador TOM:

![Estadísticas del Analizador VertiPaq en el Explorador TOM](~/content/assets/images/vertipaq-analyzer-stats.png)

...o al situar el cursor sobre las referencias a objetos en expresiones DAX:

![Estadísticas del Analizador VertiPaq en una expresión DAX](~/content/assets/images/vertipaq-analyzer-stats-dax.png)

# Siguientes pasos

- @creating-and-testing-dax