---
uid: incremental-refresh-setup
title: Configurar una nueva política de actualización
author: Kurt Buhler
updated: 2023-01-09
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Configurar la actualización incremental

![Resumen Visual de la configuración de actualización incremental](~/content/assets/images/tutorials/incremental-refresh-setup-refresh-policy.png)

---

Para configurar la actualización incremental, debe definir una nueva política de actualización para la tabla. Esto se hace fácilmente configurando las propiedades de la política de actualización una vez que _EnableRefreshPolicy_ se haya establecido en `True`:

> [!IMPORTANT]
> La configuración de la actualización incremental con Tabular Editor 3 solo se admite para Datasets alojados en el servicio Power BI Datasets.
> Para Analysis Services, se requiere [particionado](https://learn.microsoft.com/en-us/analysis-services/tabular-models/partitions-ssas-tabular?view=asallproducts-allversions) personalizado.

### Configurar una nueva política de actualización

1. **Conéctese al modelo:** Conéctese al punto de conexión XMLA de Power BI de su Workspace y abra el Dataset en el que desea configurar la actualización incremental.
2. **Crea los parámetros `RangeStart` y `RangeEnd`:** La actualización incremental requiere que se creen los parámetros `RangeStart` y `RangeEnd` ([más información](https://docs.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-configure#create-parameters)). Agregue dos nuevas expresiones compartidas en Tabular Editor:

<img src="~/content/assets/images/create-shared-expression-te3.png" class="noscale" alt="Apply Refresh Policy" style="width:400px !important"/>

3. **Configure los parámetros `RangeStart` y `RangeEnd`:** Asígneles los nombres `RangeStart` y `RangeEnd`, respectivamente; establezca su propiedad `Kind` en "M" y defina su expresión como se indica a continuación (el valor real de fecha y hora que especifique no importa, ya que el servicio de Power BI lo establecerá al iniciar la actualización de datos):

```M
#datetime(2021, 6, 9, 0, 0, 0) 
   meta 
   [
      IsParameterQuery=true, 
      Type="DateTime", 
      IsParameterQueryRequired=true
   ]
```

<img src="~/content/assets/images/shared-expression-kind.png" class="noscale" alt="Apply Refresh Policy" style="width:400px !important"/>

4. **Copie el código M de la partición:** Vaya a la tabla para la que desea configurar la actualización incremental. Despliegue la tabla y seleccione la partición que contiene su expresión M de Power Query. Copia el código en el Bloc de notas; lo necesitarás en el paso 6.

5. **Habilite la política de actualización de la tabla:** En la ventana _Propiedades_, establezca la propiedad `EnableRefreshPolicy` de la tabla en `True`:

<img src="~/content/assets/images/tutorials/incremental-refresh-enable-refresh-policy.png" class="noscale" alt="Apply Refresh Policy" style="width:400px !important"/>

6. **Configura la actualización de la tabla:** A continuación, selecciona la tabla en la que quieres configurar la actualización incremental. En la ventana del **Editor de expresiones**, selecciona **'Source Expression'** en la lista desplegable, inserta tu expresión de Power Query M del paso 4 y modifícala para que incluya un paso de filtrado en la columna de fecha para la que habilitarás la actualización incremental.

   _A continuación se muestra un ejemplo de un paso de filtro válido:_

```M
// El paso de filtro debe poder plegarse de nuevo al Data source
// Ningún paso anterior debe romper el plegado de consultas
#"Incremental Refresh Filter Step" = 
    Table.SelectRows(
        Navigation,
        each 
            [OrderDate] >= #"RangeStart" and 
            [OrderDate] < #"RangeEnd"
    )
```

Las columnas de tipo fecha, cadena o entero también se pueden filtrar manteniendo el plegado de consultas, usando funciones que convierten `RangeStart` o `RangeEnd` al tipo de datos adecuado. Para obtener más información, consulta [aquí](https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview#supported-data-sources)

7. **Configura la política de actualización:** Configura las propiedades restantes según la política de actualización incremental que necesites. Recuerda especificar una expresión M para la propiedad `SourceExpression` (esta es la expresión que se añadirá a las particiones creadas por la política de actualización incremental y debe usar los parámetros `RangeStart` y `RangeEnd` para filtrar los datos en el origen). El operador = solo debe aplicarse a RangeStart o a RangeEnd, pero no a ambos, ya que podrían duplicarse los datos.

   - **Source Expression:** La expresión M que se añadirá a las particiones creadas por la política de actualización.
   - **IncrementalWindowGranularity:** La granularidad de la ventana incremental (de actualización).
   - **IncrementalWindowPeriods:** Número de períodos (con la granularidad indicada más arriba) durante los cuales se deben actualizar los datos.
   - **IncrementalWindowPeriodsOffset:** Establécelo en `-1` para configurar _'Only Refresh Complete Periods'_
   - **RollingWindowGranularity:** La granularidad de la ventana deslizante (de archivo).
   - **RollingWindowPeriods:** Número de períodos (con la granularidad indicada más arriba) durante los cuales se deben archivar los datos.
   - **Mode:** Si es una política de actualización `Import` estándar o `Hybrid`, en la que la última partición es DirectQuery.
   - **PollingExpression:** Una expresión M válida configurada para detectar cambios en los datos. Para más información sobre _Polling Expression_ u otras propiedades de la política de actualización, consulta [aquí](xref:incremental-refresh-about#overview-of-all-properties).
8. **Aplicar cambios al modelo:** Guarda el modelo (Ctrl+S).
9. **Aplicar política de actualización:** Haz clic con el botón derecho en la tabla y elige "Aplicar política de actualización".

<img src="~/content/assets/images/tutorials/incremental-refresh-apply-refresh-policy.png" class="noscale" alt="Apply Refresh Policy" style="width:400px !important"/>

**¡Listo!** En este punto, deberías ver que el servicio de Power BI ha generado automáticamente las particiones de tu tabla, según la política que especificaste. Solo queda actualizar todas las particiones.

<img src="~/content/assets/images/generated-partitions-te3.png" class="noscale" alt="Refresh All Partitions" style="width:400px !important"/>

10. **Actualizar todas las particiones:** Mantén pulsada Mayús y haz clic para seleccionar todas las particiones. Haz clic con el botón derecho y selecciona _Actualizar > Actualización completa (partición)_. Puedes hacer clic con el botón derecho en la tabla y seleccionar _'Preview data'_ para ver el resultado.

   <img src="~/content/assets/images/tutorials/incremental-refresh-refresh-all-partitions.png" class="noscale" alt="Refresh All Partitions" style="width:400px !important"/>

Por último, puedes configurar la actualización programada en Power BI Service. Power BI se encargará automáticamente de crear las particiones de tu tabla. Siempre puedes conectarte al modelo remoto para ver y validar las particiones, por ejemplo, usando el Analizador VertiPaq.

-------------

### Actualización incremental con claves de fecha de tipo entero

Si tu columna de fecha es de tipo entero, usa lo siguiente en lugar del paso 4 del filtro anterior:

1. **Crea la función personalizada:** Crea una expresión compartida llamada `ConvertDatetimeToInt`:

```M
   // A custom M function which will return a DateTime value as a YYYYMMDD integer
   (DateValue as datetime) => 
        Date.Year(DateValue) * 10000 + Date.Month(DateValue) * 100 + Date.Day(DateValue)
```

2. **Crea el paso de filtro:** Usa la función personalizada para convertir `RangeStart` y `RangeEnd` en línea a un entero. Por lo demás, el paso de filtro es idéntico al que usarías si la columna Date fuera de tipo DateTime:

```M
let
   // Conectar a tu Data source
   Source = 
      Sql.Database(#"SqlEndpoint", #"Database"),

// Cargar los datos de la tabla
   Data = 
      Source{ [Schema="Factview", Item="Orders"] }[Data],

   // Realizar las transformaciones que deban plegarse de nuevo en el Data source
   #"Remove Unnecessary Columns" = 
      Table.RemoveColumns ( 
         Data, 
         {
            "DWCreatedDate", 
            "Net Invoice Cost"
         } 
      ),

   // Agregar el paso de filtro de actualización incremental
   //    El paso de filtro debe poder plegarse de nuevo en el Data source
   //    Ningún paso anterior a este debería romper el plegado de consultas
   #"Actualización incremental" = 
     Table.SelectRows(
       #"Remove Unnecessary Columns",
         each [OrderDateKey] >= ConvertDatetimeToInt(#"RangeStart")
         and  [OrderDateKey] < ConvertDatetimeToInt(#"RangeEnd")
     )
in
   #"Actualización incremental" 
```

3. **Continúa con normalidad con los siguientes pasos:** Después, puedes continuar con la configuración y la aplicación de la política de actualización con _"Aplicar política de actualización"_ y, por último, actualizar todas las particiones. Previsualiza los datos de la tabla una vez finalicen las operaciones de actualización para ver el resultado.

-------------

### Actualización incremental con claves de fecha de tipo cadena

Si tu columna de fecha es de tipo cadena, deberías configurar el paso de filtro para analizar la columna Date sin romper el plegado de consultas. Esto variará en función del origen y de cómo esté formateada la fecha. A continuación se muestra un ejemplo hipotético de una fecha de pedido con el formato 'YYYY-MM-DD':

```M
let
   // Conectar a tu Data source
   Source = 
      Sql.Database(#"SqlEndpoint", #"Database"),

   // Cargar los datos de la tabla
   Data = 
      Source{ [Schema="Factview", Item="Orders"] }[Data],

   // Realizar las transformaciones que deban plegarse de nuevo en el Data source
   #"Remove Unnecessary Columns" = 
      Table.RemoveColumns ( 
         Data, 
         {
            "DWCreatedDate", 
            "Net Invoice Cost"
         } 
      ),

   // Agregar el paso de filtro de actualización incremental
   //    El paso de filtro debe poder plegarse de nuevo en el Data source
   //    Ningún paso anterior a este debería romper el plegado de consultas
   #"Actualización incremental" = 
     Table.SelectRows(
       #"Remove Unnecessary Columns",
       each 

       // Convierte "2022-01-09" a DateTime, por ejemplo
       DateTime.From(
         Date.FromText(
           [OrderDate], 
           [Format="yyyy-MM-dd"]
         )
       ) >= #"RangeStart"

       and 

       DateTime.From(
         Date.FromText(
           [OrderDate], 
           [Format="yyyy-MM-dd"]
         )
       ) < #"RangeEnd"      
     )
in
   #"Actualización incremental" 
```

Consulta también la documentación de la función `Date.FromText` en Power Query [aquí](https://learn.microsoft.com/en-us/powerquery-m/date-fromtext). Si no es posible convertir la columna Date sobre la marcha manteniendo el plegado de consultas, también puedes configurar la actualización incremental con una consulta nativa, como se describe en la sección siguiente.

-------------

### Actualización incremental con consultas nativas

Si has configurado una consulta nativa, quizá siga siendo posible configurar y usar la actualización incremental, según tu Data source. Para probarlo por tu cuenta, debes seguir estos pasos en lugar del paso 4 anterior:

1. **Redacta y guarda la consulta nativa:** Escribe tu consulta nativa en SQL Server Management Studio o Azure Data Studio. Incluye una cláusula `WHERE` de ejemplo que filtre con >= un parámetro DateTime y con < otro parámetro DateTime.

   <img src="~/content/assets/images/tutorials/incremental-refresh-native-query-sql.png" class="noscale" alt="Actualizar todas las particiones" style="width:650px !important"/>incremental-refresh-native-query-formatted.png

2. **Sustituye la cadena de consulta nativa en la expresión de origen:** Copia la consulta y sustituye la actual, que estará llena de caracteres como (lf) (salto de línea), (cr) (retorno de carro) y (n) (nueva línea). Esto hace que la consulta sea realmente legible y editable sin tener que recurrir a la interfaz de usuario de Consulta nativa de Power BI Desktop.

<img src="~/content/assets/images/tutorials/incremental-refresh-native-query-unformatted.png" class="noscale" alt="Refresh All Partitions" style="width:650px !important"/>

Sustituye el texto anterior en el parámetro `Query` por el siguiente, por ejemplo:

<img src="~/content/assets/images/tutorials/incremental-refresh-native-query-formatted.png" class="noscale" alt="Refresh All Partitions" style="width:650px !important"/>

3. **Añadir `RangeStart` y `RangeEnd`:** Concatena "RangeStart" y "RangeEnd" dentro de la cláusula `WHERE`, sustituyendo los campos de marcador de posición y convirtiendo los parámetros al tipo de fecha con `Date.From` y al tipo de texto mediante `Date.ToText`, con la opción `Format` establecida en `"yyyy-MM-dd`. No olvides incluir comillas simples `'` a ambos lados de la concatenación. A continuación tienes un ejemplo de cómo quedaría la consulta final:

```M
// Ejemplo de una consulta nativa completa que se pliega y funciona con actualización incremental
let
    Source = Sql.Database("yoursql.database.windows.net", "YourDatabaseName", 
    [Query="

SELECT
    [OrderDateKey]
   ,[DueDateKey]
   ,SUM([OrderQuantity]) AS 'TotalOrderQuantity'
   ,SUM([SalesAmount]  ) AS 'TotalSalesAmount'
   ,[CustomerKey]
   ,[ProductKey]
FROM [DW_fact].[Internet Sales]
WHERE
   CONVERT(DATE, CONVERT(VARCHAR(8), [OrderDateKey])) 
   >= CONVERT(DATE, '" & Date.ToText(Date.From(#"RangeStart"), [Format="yyyy-MM-dd"]) & "')
   AND
   CONVERT(DATE, CONVERT(VARCHAR(8), [OrderDateKey])) 
   < CONVERT(DATE, '" & Date.ToText(Date.From(#"RangeEnd"), [Format="yyyy-MM-dd"]) & "')
GROUP BY
    [OrderDateKey]
   ,[DueDateKey]
   ,[CustomerKey]
   ,[ProductKey]

"])
in
   Source
```

4. **Validar la nueva expresión M:** Puedes intentar guardar los cambios en la expresión M de la tabla antes de habilitar la política de actualización, para comprobar si obtienes los resultados esperados al establecer `RangeStart` y `RangeEnd` en valores concretos. Si es así, puedes continuar con normalidad; Power BI podrá encargarse de la creación de particiones como se espera si configuraste los pasos en Power Query.

   Puede que no sea necesario, pero en función de las transformaciones de la consulta nativa, también puedes probar a añadir el parámetro `[EnableFolding = True]` tal y como se describe en [este artículo de Chris Webb](https://blog.crossjoin.co.uk/2021/02/21/query-folding-on-sql-queries-in-power-query-using-value-nativequery-and-enablefoldingtrue/).

5. **Continúa con normalidad con los siguientes pasos:** Después, puedes seguir con la configuración y aplicación de la política de actualización con _'Aplicar política de actualización'_ y, por último, actualizar todas las particiones. Previsualiza los datos de la tabla cuando finalicen las operaciones de actualización para ver el resultado.
