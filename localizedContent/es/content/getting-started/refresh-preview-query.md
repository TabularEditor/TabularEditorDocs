---
uid: refresh-preview-query
title: "Actualizar, obtener una vista previa y consultar datos"
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
# Actualizar, obtener vista previa y consultar datos

Cuando Tabular Editor 3 está conectado a una instancia de Analysis Services, hay disponibles varias **funciones conectadas** adicionales que le permiten usar Tabular Editor 3 como herramienta cliente para Analysis Services.

> [!NOTE]
> La expresión «conectado a una instancia de Analysis Services» significa cualquiera de las siguientes opciones:
> 
> - Cargar un modelo en [**modo de espacio de trabajo**](xref:workspace-mode)
> - Cargar un modelo directamente desde SQL Server Analysis Services, Azure Analysis Services o el punto de conexión XMLA de Power BI
> - Usar Tabular Editor 3 como herramienta externa para Power BI Desktop

En resumen, estas funciones conectadas son:

- Operaciones de actualización de datos
- Vista previa de los datos de la tabla
- PivotGrids
- Consultas DAX
- Analizador VertiPaq

# Actualización de datos

Tabular Editor no activa automáticamente las operaciones de actualización en Analysis Services cuando se realizan cambios en el modelo de datos. Esto es intencionado, para garantizar que guardar los cambios de metadatos en Analysis Services no lleve demasiado tiempo. Potencialmente, una operación de actualización puede tardar mucho tiempo en completarse, durante el cual no se pueden actualizar metadatos adicionales en el servidor. Por supuesto, el inconveniente de esto es que puedes realizar cambios utilizando Tabular Editor, lo que hace que el modelo entre en un estado en el que solo se pueden realizar consultas parcialmente o no se pueden realizar en absoluto. Dependiendo del tipo de cambio realizado en el modelo de datos, pueden ser necesarios diferentes niveles de actualización.

En general, los siguientes cambios requieren una actualización completa antes de que se pueda consultar el objeto mencionado (es decir, una actualización de datos seguida de una actualización de cálculo):

- Agregar una nueva tabla al modelo
- Agregar una nueva columna a una tabla

En general, los siguientes cambios requieren una actualización de cálculo:

- Cambiar la expresión DAX de una tabla calculada o de una columna calculada
- Añadir o modificar una relación
- Añadir, renombrar o eliminar un elemento de cálculo de un grupo de cálculos

Cabe destacar que añadir, modificar o eliminar medidas de un modelo no requiere ningún tipo de actualización (a menos que una columna calculada haga referencia a la medida, en cuyo caso hay que recalcular la tabla en la que se encuentra esa columna).

Para iniciar una actualización con Tabular Editor, simplemente haga clic con el botón derecho en la tabla o partición que desee actualizar, vaya a **Actualizar tabla** o **Actualizar partición** y, a continuación, elija el tipo de actualización que desea realizar.

![Actualizar tabla](~/content/assets/images/refresh-table.png)

También puede iniciar una actualización a nivel de modelo a través del menú **Modelo > Actualizar modelo**. Una vez que se inicie la operación de actualización, verá el texto «Actualización de datos iniciada... <ins>Ver cola de actualización</ins>». Haga clic en el enlace o busque la vista **Actualización de datos** a través de la opción de menú **Vista > Actualización de datos**. Esto mostrará una lista de todas las operaciones de actualización (tanto pasadas como actuales), con el mensaje de estado devuelto por Analysis Services, incluidos los contadores de progreso y la duración, y le permitirá cancelar una actualización no deseada.

![Vista de actualización de datos 2](~/content/assets/images/data-refresh-view2.png)

> [!TIP]
> La vista Actualización de datos incluye una columna **Hora de inicio** que muestra cuándo comenzó cada operación de actualización. Haga clic en el encabezado de la columna para ordenar las operaciones cronológicamente, lo que facilita ver primero las actualizaciones más recientes. Puede ordenar por cualquier columna para organizar las operaciones de actualización según sus necesidades. Consulte [Vista de actualización de datos](xref:data-refresh-view) para obtener más detalles.

Mientras se está realizando una actualización, puedes seguir trabajando en tu modelo de datos, consultando y previsualizando datos o poniendo en cola nuevas operaciones de actualización de datos de acuerdo con este artículo. Sin embargo, no podrá guardar los cambios del modelo en Analysis Services hasta que se completen todas las operaciones de actualización de datos.


## Operaciones de actualización compatibles

Tabular Editor 3 admite operaciones de actualización en diferentes tipos de objetos. Los tipos de actualización admitidos se muestran a continuación:

- **Modelo** (automática, cálculo, completa)
- **Tabla (importada)** (automática, calcular, solo datos, completa)
- **Partición** (completa)
- **Tabla calculada** (Calcular)
- **Grupo de cálculo** (Calcular)

Consulte [Tipos de actualización](https://docs.microsoft.com/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions#request) para obtener más información sobre los tipos de operaciones de actualización compatibles con Analysis Services / Power BI.

# Vista previa de datos de tabla

En determinados momentos durante la creación de DAX y el desarrollo del modelo de datos, es posible que deba inspeccionar el contenido de sus tablas fila por fila. Por supuesto, podría escribir una consulta DAX para conseguirlo, pero Tabular Editor 3 lo hace aún más fácil al permitirle previsualizar los datos de las tablas directamente. Para ello, haga clic derecho en una tabla y elija la opción **Obtener vista previa de datos**.

![Vista previa de los datos](~/content/assets/images/preview-data-big.png)

Puede abrir varias vistas previas de tablas de este tipo y organizarlas como desee en la interfaz de usuario. Tabular Editor ejecuta una consulta DAX en el modelo para devolver solo un pequeño número de registros adecuados para rellenar la vista actual y, a continuación, va paginando más filas a medida que se desplaza.

Cada encabezado de columna incluye una opción de ordenación y un filtro. El menú contextual de la cuadrícula (al hacer clic con el botón derecho) permite abrir la expresión de una columna calculada o recalcular la tabla, y la opción **Mostrar consulta DAX real...** le proporciona la consulta subyacente a la vista previa como un nuevo documento de consulta DAX. Al seleccionar una columna en el Explorador TOM, la vista previa se desplaza hasta ella.

Consulte @table-preview para ver la barra de herramientas, el menú contextual, hasta dónde puede desplazarse en cada modo de almacenamiento y las preferencias que rigen el orden de las columnas y el menú desplegable de filtros.

# Pivot Grids

Después de añadir o editar medidas DAX en un modelo, es habitual que los desarrolladores de modelos prueben estas medidas. Tradicionalmente, esto solía hacerse utilizando herramientas cliente como Excel o Power BI. Con Tabular Editor 3, ahora puedes utilizar **cuadrículas dinámicas**, que funcionan de forma muy parecida a las famosas tablas dinámicas de Excel. La cuadrícula dinámica te permite crear rápidamente vistas resumidas de los datos de tu modelo, lo que te permite probar el comportamiento de tus medidas DAX al filtrar y segmentar por varias columnas y jerarquías.

Para crear una nueva Pivot Grid, utilice la opción **Archivo > Nuevo > Pivot Grid**. Desde aquí, puede arrastrar medidas, columnas y jerarquías del TOM Explorer a la cuadrícula, o puede usar la opción de menú **Pivot Grid > Show fields** para mostrar una lista emergente de todos los campos que se pueden arrastrar a la Pivot Grid (vea la captura de pantalla a continuación).

![Mostrar campos de tabla dinámica](~/content/assets/images/show-fields-pivot.png)

A medida que se arrastran campos al Pivot Grid, Tabular Editor genera consultas MDX que se envían a Analysis Services para mostrar los datos resultantes. En este sentido, el comportamiento es muy similar al de las tablas dinámicas de Excel. Puede reorganizar los campos en el Pivot Grid arrastrándolos y soltándolos, y hay varias opciones de menú disponibles al hacer clic con el botón derecho para personalizar la forma en que se muestran los datos.

![Personalización de Pivot Grids](~/content/assets/images/customizing-pivot-grids.png)

Pivot Grid se actualiza automáticamente cuando se realiza un cambio en el modelo o cuando finaliza una operación de actualización. Puede activar o desactivar esta función de actualización automática en el menú **Pivot Grid**.

# Consultas DAX

Una forma más directa de consultar los datos de tu modelo es escribir una consulta DAX. Use la opción de menú **Archivo > Nuevo > Consulta DAX** para crear un nuevo documento de consulta DAX. Puede tener varios documentos de consultas DAX abiertos al mismo tiempo.

Las consultas DAX se pueden guardar y cargar en archivos independientes y desde ellos utilizando la extensión de archivo `.dax` o `.msdax`. Consulta @supported-files para obtener más información.

Escriba su consulta DAX `EVALUATE` en el editor y pulse **Consulta > Ejecutar** (F5) para enviar la consulta a Analysis Services y ver el resultado. De forma predeterminada, Tabular Editor 3 limita el número de filas devueltas por Analysis Services a 1000, pero esto se puede cambiar en **Herramientas > Preferencias > Exploración de datos > Consulta DAX**. Si una consulta supera este límite, Tabular Editor 3 muestra un acceso directo que le permite recuperar todos los registros (vea la captura de pantalla a continuación).

![Límite del conjunto de filas de la consulta](~/content/assets/images/query-rowset-limit.png)

> [!WARNING]
> Mostrar un gran número de registros en la ventana de resultados de la consulta podría llevar un tiempo y aumentar drásticamente la memoria consumida por Tabular Editor 3.

Tabular Editor 3 utiliza el mismo editor de código DAX para editar consultas que para definir expresiones DAX en objetos. Por lo tanto, están disponibles todas las funciones relacionadas con la finalización de código, el formato automático, etc. Consulta @dax-editor para obtener más información. Además, dado que una consulta DAX tiene una sintaxis ligeramente diferente a la de las expresiones de objetos, el editor de consultas DAX ofrece algunas opciones más para las tareas habituales.

Por ejemplo, si hace clic con el botón derecho en una referencia de medida, hay una opción para **Definir medida**, como se ve en la captura de pantalla siguiente. Esta opción añadirá una instrucción `DEFINE MEASURE` en la parte superior de su consulta DAX, lo que le permitirá modificar fácilmente la expresión DAX de esa medida dentro del ámbito de la consulta.

![Funciones de consulta Dax](~/content/assets/images/dax-query-features.png)

Además, una consulta DAX puede contener varias instrucciones `EVALUATE`. Cuando ese es el caso, Tabular Editor 3 muestra el resultado de cada una de esas sentencias en una pestaña separada y numerada. Si solo quieres ejecutar una única instrucción `EVALUATE`, aunque tu documento contenga varias, puedes colocar el cursor en algún punto de la instrucción que quieras ejecutar y, a continuación, usar la opción **Consulta > Ejecutar selección** (MAYÚS+F5).

Una consulta DAX en Tabular Editor 3 se actualiza automáticamente cuando se realiza un cambio en el modelo o cuando finaliza una operación de actualización. Puede activar o desactivar esta función de actualización automática en el menú **Consulta**.

# Simulación de usuario

Al consultar los datos del modelo, a veces resulta útil poder suplantar a un usuario específico o a una combinación de roles, para ver cuál sería el comportamiento del modelo desde la perspectiva de un usuario final. Tabular Editor 3 te permite suplantar a un usuario específico o a uno o varios roles haciendo clic en el botón **Suplantar...**. Esto se aplica a las [vistas previas de tablas](#previewing-table-data), las [cuadrículas dinámicas](#pivot-grids) y las [consultas DAX](#dax-queries). 

> [!NOTE]
> Para suplantar a un usuario, Tabular Editor añade la [propiedad `EffectiveUserName`](https://docs.microsoft.com/analysis-services/instances/connection-string-properties-analysis-services?view=asallproducts-allversions#effectiveusername) a la cadena de conexión, al conectarse a Analysis Services. Para suplantar un rol, Tabular Editor añade la [propiedad `Roles`](https://docs.microsoft.com/analysis-services/instances/connection-string-properties-analysis-services?view=asallproducts-allversions#roles) a la cadena de conexión. Esto solo se aplica a la vista de datos (es decir, la consulta DAX, Pivot Grid o la vista previa de la tabla) en la que se especifica la suplantación.

Al hacer clic en el botón **Suplantación...** (que también se puede encontrar a través del menú **Consulta**, **Cuadrícula dinámica** o **Vista previa de tabla**, dependiendo del tipo de vista de datos que esté activa), una ventana emergente le permite especificar un usuario o seleccionar uno o más roles.

![Seleccionar simulación de usuario](~/content/assets/images/select-impersonation.png)

Una vez habilitada la suplantación, se marca el botón **Suplantación...** y la suplantación se aplicará a la vista de datos actual. Al hacer clic en la pequeña flecha situada junto al botón **Suplantación...**, puede ver y cambiar rápidamente entre las 10 suplantaciones más recientes que se hayan usado.

![Menú desplegable de suplantación](~/content/assets/images/impersonation-dropdown.png)

Cuando la actualización automática está habilitada en una vista de datos, al cambiar la suplantación se actualizará inmediatamente la vista. 

## CustomData

La función CustomData le permite pasar un valor de cadena personalizado que se puede usar en expresiones DAX, normalmente para implementar escenarios de seguridad dinámica a nivel de fila. Esta función se puede combinar con cualquiera de las opciones de simulación de usuario descritas anteriormente, incluida la opción **Sin simulación de usuario**.

![Seleccionar simulación de usuario](~/content/assets/images/impersonation-customdata.png)

Cuando introduce un valor en el campo de entrada **CustomData**, Tabular Editor 3 añade la [propiedad `CustomData`](https://docs.microsoft.com/analysis-services/instances/connection-string-properties-analysis-services?view=asallproducts-allversions#customdata) a la cadena de conexión. A continuación, este valor puede recuperarse dentro de sus expresiones DAX utilizando la [función `CUSTOMDATA()`](https://dax.guide/customdata/).

CustomData se usa habitualmente para implementar seguridad dinámica a nivel de filas cuando una aplicación utiliza autenticación personalizada. El valor que proporcione puede aprovecharse en expresiones de filtro de roles para controlar qué filas pueden ver los usuarios en función de los datos personalizados que se transmiten a través de la cadena de conexión.

Esta función es especialmente útil en escenarios de **Power BI Embedded**, donde puedes utilizar de forma nativa CustomData para añadir filtros de filas que pasan texto libre (cadenas) con el fin de aprovechar la seguridad dinámica a nivel de fila en informes, paneles y mosaicos integrados.

**Ejemplo de caso de uso:** Puede pasar el departamento o la región de un usuario como CustomData y, a continuación, usar ese valor en la expresión de filtro de un rol, como en el siguiente ejemplo:
```dax
'Department'[DepartmentCode] = CUSTOMDATA()
```   

# Analizador VertiPaq

Tabular Editor 3 incluye una versión de la herramienta de código abierto [Analizador VertiPaq](https://www.sqlbi.com/tools/vertipaq-analyzer/), creada por [SQLBI](https://sqlbi.com). El Analizador VertiPaq es útil para analizar las estructuras de almacenamiento VertiPaq de su modelo de datos de Power BI o tabular.

Con Tabular Editor 3, puedes recopilar estadísticas del Analizador VertiPaq mientras estás conectado a cualquier instancia de Analysis Services. También puede exportar las estadísticas como un [archivo .vpax](https://www.youtube.com/watch?v=zRa9y01Ub30) o importar estadísticas desde un archivo .vpax.

Para recopilar estadísticas, simplemente pulse el botón **Recopilar estadísticas** en la vista **Analizador VertiPaq**.

Si no se pueden leer las estadísticas a partir de los datos del modelo, por ejemplo, cuando una columna de alta cardinalidad supera el límite de memoria por consulta de una capacidad de Power BI, las estadísticas se recopilan únicamente a partir de los metadatos del modelo. Aparece una advertencia de **Estadísticas recopiladas sin leer los datos** junto con el error del servidor, y es posible que falten cardinalidades o que sean inexactas. Para omitir la lectura de estadísticas de los datos, desmarque **Leer estadísticas de datos** en **Herramientas > Preferencias > Formatos de archivo > Analizador VertiPaq**.

![Recopilar estadísticas de Vertipaq Analyzer](~/content/assets/images/vertipaq-analyzer-collect-stats.png)

Una vez recopiladas las estadísticas, VertiPaq Analyzer muestra un resumen del tamaño del modelo, el número de tablas, etc. Puedes consultar estadísticas más detalladas en las pestañas **Tablas**, **Columnas**, **Relaciones** y **Particiones**.

Además, siempre que se hayan cargado estadísticas, Tabular Editor 3 mostrará la información de cardinalidad y tamaño como una información emergente al pasar el cursor del ratón sobre los objetos en el Explorador TOM:

![Estadísticas del Analizador VertiPaq en el Explorador TOM](~/content/assets/images/vertipaq-analyzer-stats.png)

...o cuando pase el cursor del ratón sobre las referencias de objetos en las expresiones DAX:

![Estadísticas de Vertipaq Analyzer en una expresión DAX](~/content/assets/images/vertipaq-analyzer-stats-dax.png)

# Próximos pasos

- @crear-y-probar-dax