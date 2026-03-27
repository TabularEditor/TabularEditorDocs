---
uid: incremental-refresh-about
title: ¿Qué es una política de actualización?
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

# ¿Qué es una política de actualización?

![Resumen Visual de la actualización incremental](~/content/assets/images/tutorials/incremental-refresh-header.png)

---

Los Datasets alojados en el servicio de Power BI pueden configurar la [actualización incremental](https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview) en una o varias tablas de datos. **El objetivo de la actualización incremental es lograr actualizaciones más rápidas y eficientes al recuperar solo los datos recientes o cambiantes y _actualizar la tabla de forma incremental_.** Para ello, la tabla se divide automáticamente en particiones, de modo que solo <span style="color:#01a99d">se actualizan los datos recientes o cambiantes (particiones "hot")</span> o incluso <span style="color:#8d7bae">se recuperan en tiempo real ([particiones "DirectQuery" en "tablas híbridas"](https://learn.microsoft.com/en-us/power-bi/connect-data/service-dataset-modes-understand#hybrid-tables))</span>, mientras que <span style="color:#939799">los datos más antiguos y estáticos se archivan (particiones "cold").</span>

_La actualización incremental se puede configurar y modificar fácilmente desde Tabular Editor._

> [!NOTE]
> Configurar la actualización incremental puede aportar ventajas a tu Data model:
>
> - Reduce el tiempo de actualización y el consumo de recursos
> - Disfruta de actualizaciones programadas más cortas y fiables

> [!IMPORTANT]
> La configuración de la actualización incremental con Tabular Editor 3 se limita a Datasets alojados en el servicio de Datasets de Power BI. Para Analysis Services, se requiere un [particionamiento](https://learn.microsoft.com/en-us/analysis-services/tabular-models/partitions-ssas-tabular?view=asallproducts-allversions) personalizado.

---

### ¿Cómo funciona?

Para crear las particiones, Power BI usa los parámetros _datetime_ `RangeStart` y `RangeEnd` en Power Query. Estos parámetros se usan en un paso de filtrado de la expresión M de la partición de la tabla, filtrando una columna de fecha y hora de la tabla. Las columnas de tipo fecha, cadena o entero pueden seguir filtrándose manteniendo el plegado de consultas, query folding, mediante funciones que convierten `RangeStart`, `RangeEnd` o la columna de fecha al tipo de datos adecuado. Para más información sobre esto, consulta [aquí](https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview#supported-data-sources)

A continuación se muestra un ejemplo. La actualización incremental se aplica a la tabla _'Orders'_ en la columna _[Order Date]_:

# [Solo el paso de filtro](#tab/filterstep)

```M
// Idealmente, el paso de filtro debería poder plegarse de nuevo al Data source
// Ningún paso anterior a este debería interrumpir el plegado de consultas
#"Incremental Refresh Filter Step" = 
    Table.SelectRows(
        Navigation,
        each 
            [OrderDate] >= #"RangeStart" and 
            [OrderDate] < #"RangeEnd"
    )
```

# [Expresión M completa](#tab/fullexp)

```M
let
    // Idealmente, el Data source debería admitir el plegado de consultas
    Source = Sql.Database(#"ServerParameter", #"DatabaseParameter"),

    Navigation = 
        Source{ 
            [ Schema="DW_fact", Item="Internet Sales" ] 
        } [Data],

    // Idealmente, el paso de filtro debería poder plegarse de nuevo al Data source
    // Ningún paso anterior a este debería interrumpir el plegado de consultas
    #"Incremental Refresh Filter Step" = 
        Table.SelectRows(
            Navigation,
            each 
                [OrderDate] >= #"RangeStart" and 
                [OrderDate] < #"RangeEnd"
        )
in
    #"Incremental Refresh Filter Step"
```

# [RangeStart](#tab/rangestart)

```M
// No importa cuál sea el valor inicial del parámetro RangeStart
// El parámetro debe ser del tipo de datos "datetime"
#datetime(2022, 12, 01, 0, 0, 0) 
    meta 
        [
            IsParameterQuery = true, 
            IsParameterQueryRequired = true, 
            Type = type datetime
        ]
```

# [RangeEnd](#tab/rangend)

```M
// No importa cuál sea el valor inicial del parámetro RangeEnd
// El parámetro debe ser del tipo de datos "datetime"
#datetime(2022, 12, 31, 0, 0, 0) 
    meta 
        [
            IsParameterQuery = true, 
            IsParameterQueryRequired = true, 
            Type = type datetime
        ]
```

***

> [!WARNING]
> La actualización incremental está diseñada para Data source que admiten el [plegado de consultas de Power Query](https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview#:~:text=Incremental%20refresh%20is%20designed%20for%20data%20sources%20that%20support%20query%20folding). Lo ideal es que el [plegado de consultas no se rompa](https://learn.microsoft.com/en-us/power-query/step-folding-indicators) antes de aplicar el paso de filtro.
> No existe un requisito explícito de que la consulta final se pliegue, excepto al implementar [tablas híbridas](https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview#:~:text=However%2C%20if%20the%20incremental%20refresh%20policy%20includes%20getting%20real%2Dtime%20data%20with%20DirectQuery%2C%20non%2Dfolding%20transformations%20can%27t%20be%20used.).

---

### ¿Qué es una política de actualización?

Una _política de actualización_ determina cómo se particionan los datos y cuáles de estas particiones del rango de la política se actualizarán al realizar una actualización. Consta de un conjunto de propiedades TOM de la tabla que se pueden configurar o cambiar.

> [!WARNING]
> **Limitaciones de Power BI Desktop:** No se admite configurar la actualización incremental cuando se está conectado a un modelo local de Power BI Desktop. Para configurar la actualización incremental en un modelo local de Power BI Desktop, utiliza la interfaz de usuario de Power BI Desktop.

---

### Propiedades de la política de actualización

<img src="~/content/assets/images/tutorials/Incremental-refresh-properties.png" class="noscale" alt="Properties of Incremental Refresh"  style="width:704px !important"/>

Una política de actualización básica se compone de cuatro tipos distintos de propiedades:

1. <span style="color:#455C86">**Ventana incremental**</span> **propiedades**: El período durante el cual los datos se <span style="color:#455C86">_mantienen actualizados_</span>.
2. <span style="color:#BC4A47">**Ventana deslizante**</span> **propiedades**: El período durante el cual los datos se <span style="color:#BC4A47">_archivan_</span>.
3. **Expresiones de origen**: Definen el esquema de la tabla y las transformaciones de Power Query de la tabla.
4. **Modo**: Si se usan tablas `Import` o `Hybrid`.

![Ventanas de la política de actualización de la actualización incremental](~/content/assets/images/tutorials/incremental-refresh-policy-windows.png)

---

#### Comparación con Power BI Desktop

En Power BI Desktop, estas propiedades se denominan de forma diferente. A continuación se muestra una descripción general de cómo se corresponden las propiedades con la interfaz de usuario de Power BI Desktop.

![Propiedades de las ventanas de la política de actualización incremental](~/content/assets/images/tutorials/incremental-refresh-window-properties.png)

---

#### Propiedades avanzadas

Según las propiedades configuradas, la actualización incremental puede funcionar de forma diferente. A continuación se muestra una descripción general de las distintas configuraciones de actualización incremental:

# [Estándar (Importación)](#tab/import)

En la configuración estándar de actualización incremental, todas las particiones se importan en memoria. Las particiones de la <span style="color:#BC4A47">ventana móvil</span> se archivan, mientras que las de la <span style="color:#455C86">ventana incremental</span> se actualizan.

# [Híbrida](#tab/hybrid)

En la configuración <span style="color:#01a99d">**_[híbrida](https://learn.microsoft.com/en-us/power-bi/connect-data/service-dataset-modes-understand#hybrid-tables)_**</span> de la actualización incremental del Dataset, la partición más reciente del rango definido por la política en la <span style="color:#455C86">ventana incremental</span> se consulta en tiempo real mediante DirectQuery.

Esto se configura mediante la propiedad <em>Mode</em> cuando se establece en <code>Hybrid</code>.

![Ventanas de política de actualización incremental](~/content/assets/images/tutorials/incremental-refresh-mode-pbi-match.png)

# [Actualizar solo períodos completos](#tab/completeperiods)

En esta configuración, el intervalo de la política no incluirá el período actual en la <span style="color:#BC4A47">ventana móvil</span>.

En la configuración estándar de actualización incremental, el período actual siempre está en la <span style="color:#455C86">ventana incremental</span>. Puede que este comportamiento no sea el deseado, ya que los datos cambiarán con cada actualización. Si los usuarios no esperan ver datos parciales de un día incompleto, puede configurar "Actualizar solo períodos completos".

Esto se configura con la propiedad <em>IncrementalPeriodsOffset</em>. En el ejemplo anterior, un valor de <code>-1</code> para un <em>IncrementalGranularity</em> de <code>Day</code> excluirá la fecha actual de la <span style="color:#455C86">ventana incremental</span> y, por tanto, del ámbito de datos; solo se actualizarán los días completos.

![Ventanas de política de actualización incremental](~/content/assets/images/tutorials/incremental-refresh-period-offset-pbi-match.png)

# [Detectar cambios en los datos](#tab/datachanges)

En esta configuración, no se actualizan todos los registros en la <span style="color:#455C86">ventana incremental</span>. En su lugar, los registros solo se actualizan si cambian. Detectar cambios en los datos puede optimizar aún más el rendimiento de actualización al usar la actualización incremental. Para identificar cambios en los datos, usa una _Polling Expression_. Una Polling Expression es una propiedad independiente que espera una expresión M válida para identificar la fecha máxima de una lista de fechas.

Normalmente, se usa una Polling Expression en una columna de tipo DateTime de una tabla para identificar la fecha más reciente. Si hay registros que coinciden con esa fecha, se actualizarán. Un ejemplo típico es usar una columna como [LastUpdateDt] para marcar los registros que se actualizaron o se agregaron con el valor DateTime actual. Se actualizan los registros cuyos valores sean iguales al [LastUpdateDt] más reciente.

> [!NOTE]
> Los registros en particiones archivadas _no_ se actualizan.

A continuación se muestra un ejemplo de una propiedad `Polling Expression` válida. Puedes usarlo como plantilla al configurar _Detect Data Changes_ en tu modelo desde Tabular Editor:

```M
// Retrieves the maximum value of the column [LastUpdateDt]
let
    #"maxDateOfLastUpdate" =
        List.max(
            Orders[LastUpdateDt]
        ),

    accountForNu11 =
        if #"maxDateOfLastUpdate" = null
        then #datetime(1901, 01, 01, 00, 00, 00)
        else #"maxDateOfLastUpdate"
in
    accountForNu11
```

![Ventanas de la política de actualización incremental](~/content/assets/images/tutorials/incremental-refresh-detect-changes-pbi-match.png)

***

#### Resumen de todas las propiedades

_A continuación se muestra un resumen de las propiedades de TOM de un Data model que se usan para configurar la actualización incremental:_

<!-- Specific styling for the below table -->

<style>
    th.formatting {
        text-align: center; 
        vertical-align: middle!important;
        border-left: none!important; 
        border-right: none!important;
    }
    td.formatting {
        height:120px;
        vertical-align: middle!important;
        border-left: none!important;
        border-right: none!important;
    }
</style>

<!-- Refresh Policy TOM Properties table -->

<div class="table-responsive" id="RefreshPolicyPropertiesOverview">
    <table class="table table-bordered table-striped table-condensed">
        <thead>
            <tr>
                <th class="formatting">Nombre de la propiedad</th>
                <th class="formatting">Equivalente en Power BI Desktop</th>
                <th class="formatting">Descripción</th>
                <th class="formatting">Valor esperado</th>
            </tr>
        </thead>
        <tbody style="font-size:80%;">
            <tr>
                <td class="formatting"><span id="enablerefreshpolicy"><em><b>EnableRefreshPolicy</b></em></a></span></td>
                <td class="formatting">Actualizar esta tabla de forma incremental</td>
                <td class="formatting">Indica si la tabla tiene habilitada una política de actualización.<br /><br>En Tabular Editor, el resto de las propiedades de la política de actualización solo se mostrarán si este valor se establece en <code>True</code>.</td>
                <td class="formatting"><code>True</code> o <code>False</code>.</td>
            </tr>
            <tr>
                <td class="formatting"><span style="color:#455C86" id="incrementalgranularity"><em><b>IncrementalGranularity</b></em></span></td>
                <td class="formatting">Período de actualización incremental</td>
                <td class="formatting">La granularidad de la ventana incremental.<br /><br>Ejemplo:<br /><em>"Actualizar los datos de los últimos 30 <strong><em>días</em></strong> anteriores a la fecha de actualización."</em></td>
                <td class="formatting"><code>Day</code>, <code>Month</code>, <code>Quarter</code> o <code>Year</code>. Debe ser menor o igual que el IncrementalGranularity.</td>
            </tr>
            <tr>
                <td class="formatting"><span style="color:#455C86" id="incrementalperiods"><em><b>IncrementalPeriods</b></em></span></td>
                <td class="formatting">Número de períodos de actualización incremental</td>
                <td class="formatting">El número de períodos de la ventana incremental.<br /><br>Ejemplo:<br /><em>"Actualizar los datos de los últimos <strong><em>30</em></strong> días antes de la fecha de actualización."</em></td>
                <td class="formatting">Un número entero que indique el número de períodos de <em>IncrementalGranularity</em>. Debe definir un período total inferior a <em>RollingWindowPeriods</em></td>
            </tr>
            <tr>
                <td class="formatting"><span style="color:#455C86" id="incrementaloffset"><b><em>IncrementalPeriodsOffset</b></em></span></td>
                <td class="formatting">Actualizar solo días completos</td>
                <td class="formatting">El desplazamiento que se aplicará a <em>IncrementalPeriods</em>.<br /><br>Ejemplo para:<br /><em>IncrementalPeriodsOffset</em>=<code>-1</code>; <br /><em>IncrementalPeriods</em> = <code>30</code>;<br /><em>IncrementalGranularity</em> = <code>Day</code>: <br /><em>"Actualizar solo los datos de los últimos 30 días, desde el día anterior a la fecha de actualización.</em></td>
                <td class="formatting">Un número entero con el número de períodos de <em>IncrementalGranularity</em> para desplazar la ventana incremental.</td>
            </tr>
            <tr>
                <td class="formatting"><span id="refreshpolicymode"><b><em>Modo</b></em></span></td>
                <td class="formatting">Obtenga los datos más recientes en tiempo real con DirectQuery</td>
                <td class="formatting">Especifica si la actualización incremental se configura únicamente con particiones de importación o también con una partición de DirectQuery, para dar como resultado una <a href="https://learn.microsoft.com/en-us/power-bi/connect-data/service-dataset-modes-understand#hybrid-tables">"tabla híbrida"</a>.</td>
                <td class="formatting"><code>Import</code> o <code>Hybrid</code>.</td>
            </tr>
            <tr>
                <td class="formatting"><b><em>PolicyType</b></em></td>
                <td class="formatting">N/A</td>
                <td class="formatting">Especifica el tipo de política de actualización.</td>
                <td class="formatting">Solo puede contener un único valor: <code>Basic</code>.</td>
            </tr>
            <tr>
                <td class="formatting"><span id="pollingexpression"><b><em>PollingExpression</b><br />(Opcional)</em></span></td>
                <td class="formatting">Detectar cambios en los datos</td>
                <td class="formatting">La expresión M que se usa para detectar cambios en una columna específica, como <em>LastUpdateDate</em><br /><br>En Tabular Editor, <strong>la <em>PollingExpression</em> se puede ver y modificar desde la ventana del <em>Editor de expresiones</em></strong> seleccionándola en el menú desplegable de la esquina superior izquierda.</td>.
                <table class="table table-bordered table-striped table-condensed">
        <thead>
            <tr>
                <th class="formatting">Nombre de la propiedad</th>
                <th class="formatting">Equivalente en Power BI Desktop</th>
                <th class="formatting">Descripción</th>
                <th class="formatting">Valor esperado</th>
            </tr>
        </thead>
        <tbody style="font-size:80%;">
            <tr>
                <td class="formatting"><span id="enablerefreshpolicy"><em><b>EnableRefreshPolicy</b></em></a></span></td>
                <td class="formatting">Actualizar esta tabla de forma incremental</td>
                <td class="formatting">Indica si hay una política de actualización habilitada para la tabla.<br /><br>En Tabular Editor, otras propiedades de la política de actualización solo serán visibles si este valor se establece en <code>True</code>.</td>
                <td class="formatting"><code>True</code> o <code>False</code>.</td>
            </tr>
            <tr>
                <td class="formatting"><span style="color:#455C86" id="incrementalgranularity"><em><b>IncrementalGranularity</b></em></span></td>
                <td class="formatting">Período de actualización incremental</td>
                <td class="formatting">La granularidad de la ventana incremental.<br /><br>Ejemplo:<br /><em>"Actualice los datos de los últimos 30 <strong><em>días</em></strong> antes de la fecha de actualización."</em></td>
                <td class="formatting"><code>Day</code>, <code>Month</code>, <code>Quarter</code> o <code>Year</code>. Debe ser menor o igual que el valor de IncrementalGranularity.</td>
            </tr>
            <tr>
                <td class="formatting"><span style="color:#455C86" id="incrementalperiods"><em><b>IncrementalPeriods</b></em></span></td>
                <td class="formatting">Número de períodos de actualización incremental</td>
                <td class="formatting">El número de períodos de la ventana incremental.<br /><br>Ejemplo:<br /><em>"Actualice los datos de los últimos <strong><em>30</em></strong> días antes de la fecha de actualización."</em></td>
                <td class="formatting">Un número entero que indica la cantidad de períodos de <em>IncrementalGranularity</em>. Debe definir un período total inferior a <em>RollingWindowPeriods</em></td>
            </tr>
            <tr>
                <td class="formatting"><span style="color:#455C86" id="incrementaloffset"><b><em>IncrementalPeriodsOffset</b></em></span></td>
                <td class="formatting">Actualizar solo los días completos</td>
                <td class="formatting">El desplazamiento que se aplicará a <em>IncrementalPeriods</em>.<br /><br>Ejemplo para:<br /><em>IncrementalPeriodsOffset</em>=<code>-1</code>; <br /><em>IncrementalPeriods</em> = <code>30</code>;<br /><em>IncrementalGranularity</em> = <code>Day</code>: <br /><em>"Actualizar solo los datos de los últimos 30 días, desde el día anterior a la fecha de actualización.</em></td>
                <td class="formatting">Un número entero que indica la cantidad de períodos de <em>IncrementalGranularity</em> para desplazar la ventana incremental.</td>
            </tr>
            <tr>
                <td class="formatting"><span id="refreshpolicymode"><b><em>Mode</b></em></span></td>
                <td class="formatting">Obtener los datos más recientes en tiempo real con DirectQuery</td>
                <td class="formatting">Especifica si la actualización incremental está configurada solo con particiones de importación o también con una partición de DirectQuery, para crear una <a href="https://learn.microsoft.com/en-us/power-bi/connect-data/service-dataset-modes-understand#hybrid-tables">"tabla híbrida"</a>.</td>
                <td class="formatting"><code>Import</code> o <code>Hybrid</code>.</td>
            </tr>
            <tr>
                <td class="formatting"><b><em>PolicyType</b></td>
                <td class="formatting">N/A</td>
                <td class="formatting">Especifica el tipo de política de actualización.</td>
                <td class="formatting">Solo puede contener un único valor: <code>Basic</code>.</td>
            </tr>
            <tr>
                <td class="formatting"><span id="pollingexpression"><b><em>PollingExpression</b><br />(Opcional)</em></span></td>
                <td class="formatting">Detectar cambios en los datos</td>
                <td class="formatting">La expresión M utilizada para detectar cambios en una columna específica, como <em>LastUpdateDate</em>.<br /><br>En Tabular Editor, <strong>la <em>Polling Expression</em> se puede ver y modificar desde la ventana del <em>Editor de expresiones</em></strong> seleccionándola en el menú desplegable de la esquina superior izquierda.</td><td class="formatting">Una expresión M válida que devuelve un valor escalar de la fecha más reciente de una columna. Se actualizarán todos los registros de las particiones activas de la ventana incremental que contengan ese valor en la columna.<br><br>Los registros de las particiones archivadas <i>no</i> se actualizan.</td>
            </tr>
            <tr>
                <td class="formatting"><span style="color:#BC4A47" id="rollinggranularity"><b><em>RollingWindowGranularity</b></em></span></td>
                <td class="formatting">Período de archivado de datos</td>
                <td class="formatting">La granularidad de la ventana deslizante.<br /><br>Ejemplo:<br /><em>"Archivar datos a partir de 3 <strong><em>años</em></strong> antes de la fecha de actualización."</em></td>
                <td class="formatting"><code>Day</code>, <code>Month</code>, <code>Quarter</code> o <code>Year</code>. Debe ser mayor o igual que IncrementalGranularity.</td>
            </tr>
            <tr>
                <td class="formatting"><span style="color:#BC4A47" id="rollingperiods"><b><em>RollingWindowPeriods</b></em></span></td>
                <td class="formatting">Número de períodos de datos archivados</td>
                <td class="formatting">El número de períodos para la ventana móvil.<br /><br>Ejemplo:<br /><em>"Archivar datos a partir de <strong><em>3</em></strong> años antes de la fecha de actualización."</em></td>
                <td class="formatting">Un entero con el número de períodos de <em>RollingWindowGranularity</em>. Debe definir un período total mayor que el   <em>IncrementalPeriods</em></td>
            </tr>
            <tr>
                <td class="formatting"><b><em>SourceExpression</b></td>
                <td class="formatting">Expresión de origen de Power Query</td>
                <td class="formatting">La expresión M para el Data source de la tabla. Aquí es donde se encuentra la expresión M original de la tabla y donde se modificarían las transformaciones existentes de Power Query.<br /><br>En Tabular Editor, <strong>la <em>Source Expression</em> se puede ver y modificar desde el <em>Editor de expresiones</em></strong> seleccionándola en el menú desplegable de la parte superior izquierda.</td>
                <td class="formatting">Una expresión M válida que contenga un paso de filtro usando adecuadamente <code>RangeStart</code> y <code>RangeEnd</code>.</td>
            </tr>
        </tbody>
    </table>
</div>