---
uid: incremental-refresh-policy
title: Actualización incremental
author: Daniel Otykier
updated: 2021-02-15
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          partial: true
          note: "Limitado a SQL Server Standard Edition"
        - edition: Enterprise
          full: true
---

# Actualización incremental

Los Datasets alojados en el servicio de Power BI pueden tener configurada la [actualización incremental](https://docs.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview) en una o varias tablas. Para configurar o modificar la actualización incremental en un Dataset de Power BI, puedes usar directamente el [punto de conexión XMLA del servicio de Power BI](https://docs.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-xmla), o puedes usar Tabular Editor conectado al punto de conexión XMLA, como se describe a continuación:

> [!IMPORTANT]
> La configuración de la actualización incremental con Tabular Editor 3 está limitada a los Datasets alojados en el servicio Power BI Datasets. En Analysis Services se requieren [particiones](https://learn.microsoft.com/en-us/analysis-services/tabular-models/partitions-ssas-tabular?view=asallproducts-allversions) personalizadas.

## Configurar la actualización incremental desde cero con Tabular Editor

1. Conéctate al punto de conexión XMLA R/W de Power BI de tu Workspace, y abre el Dataset en el que quieres configurar la actualización incremental.
2. La actualización incremental requiere crear los parámetros `RangeStart` y `RangeEnd` ([más información](https://docs.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-configure#create-parameters)), así que empecemos por agregar dos nuevas expresiones compartidas en Tabular Editor:
   ![Agregar expresiones compartidas](~/content/assets/images/incremental-refresh2-01.png)
3. Asígnales los nombres `RangeStart` y `RangeEnd`, respectivamente, establece su propiedad `Kind` en "M" y define su expresión como sigue (el valor real de fecha y hora que especifiques no importa, ya que lo establecerá el servicio de Power BI al iniciar la actualización de datos):

```M
#datetime(2021, 6, 9, 0, 0, 0) meta [IsParameterQuery=true, Type="DateTime", IsParameterQueryRequired=true]
```

![Establecer la propiedad Kind](~/content/assets/images/incremental-refresh2-02.png)
4. A continuación, selecciona la tabla en la que quieres habilitar la actualización incremental
5. Establece la propiedad `EnableRefreshPolicy` de la tabla en "true":
![Habilitar la política de actualización](~/content/assets/images/incremental-refresh2-03.png)
6. Configura las propiedades restantes según la política de actualización incremental que necesites. Recuerda especificar una expresión M para la propiedad `SourceExpression` (esta es la expresión que se agregará a las particiones creadas por la política de actualización incremental, y debería usar los parámetros `RangeStart` y `RangeEnd` para filtrar los datos en el origen). El operador = solo debe aplicarse a RangeStart o a RangeEnd, pero no a ambos, ya que los datos podrían duplicarse.
![Configurar propiedades](~/content/assets/images/incremental-refresh2-04.png)
7. Guarda el modelo (Ctrl+S).
8. Haz clic derecho en la tabla y elige "Aplicar política de actualización".
![Aplicar la política de actualización](~/content/assets/images/incremental-refresh2-05.png)

¡Eso es todo! En este punto, deberías ver que el servicio de Power BI ha generado automáticamente las particiones en tu tabla, en función de la política que especificaste.

![Particiones generadas](~/content/assets/images/incremental-refresh2-06.png)

El siguiente paso es actualizar los datos de las particiones. Para ello, puedes usar el servicio de Power BI o actualizar las particiones por lotes mediante [XMLA/TMSL desde SQL Server Management Studio](https://docs.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-xmla#refresh-management-with-sql-server-management-studio-ssms), o incluso con el scripting de [Tabular Editor](https://www.elegantbi.com/post/datarefreshintabulareditor).

### Actualización completa con la política de actualización incremental aplicada

Si has aplicado una política de actualización a tu tabla y quieres realizar una actualización completa, debes asegurarte de establecer [applyRefreshPolicy a false](https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-xmla#override-incremental-refresh-behavior) en tu script. Esto garantiza que realices una actualización completa de todas las particiones de tu tabla.
En nuestro ejemplo, el comando TMSL tendría este aspecto:

```
{
"refresh": {
  "type": "full",
  "applyRefreshPolicy": false
  "objects": [
    {
      "database": "AdventureWorks",
      "table": "Internet Sales"
    }
  ]
}
}
```

## Modificar políticas de actualización existentes

También puedes usar Tabular Editor para modificar las políticas de actualización existentes que se han configurado con Power BI Desktop. En este caso, simplemente sigue los pasos 6-8 anteriores.

## Aplicar políticas de actualización con `EffectiveDate`

Si quieres generar particiones sobrescribiendo la fecha actual (para generar distintos rangos de ventana móvil), puedes usar un pequeño script en Tabular Editor para aplicar la política de actualización con el parámetro [EffectiveDate](https://docs.microsoft.com/en-us/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions#optional-parameters).

Con la tabla de actualización incremental seleccionada, ejecuta el siguiente script en el panel "Advanced Scripting" de Tabular Editor, en lugar del paso 8 anterior:

```csharp
var effectiveDate = new DateTime(2020, 1, 1);  // Todo: replace with your effective date
Selected.Table.ApplyRefreshPolicy(effectiveDate);
```

![Usar scripts para aplicar la política de actualización](~/content/assets/images/incremental-refresh2-07.png)

## Eliminar la actualización incremental con Tabular Editor

Puede que debas quitar la política de actualización para la actualización incremental de una tabla.

1. Selecciona la tabla en la vista TOM, obtén el código M de la propiedad SourceExpression y guárdalo en algún lugar.
2. Cambia el valor de EnableRefreshPolicy de TRUE a FALSE.
3. Haz clic con el botón derecho en la tabla y crea una nueva partición M.
4. Pega el código M del paso 1 anterior como la expresión de la partición.
5. Edita el código M para quitar el paso que contiene la función Table.SelectRows() para los parámetros RangeStart/RangeEnd.
6. Elimina todas las particiones históricas. Tienen el valor "Policy Range" en SourceType.
7. Actualiza la tabla (en Tabular Editor 3) o, en el servicio, actualiza el Dataset para volver a poblarla.
8. Opcionalmente, elimina las expresiones compartidas RangeStart/RangeEnd si no hay ninguna otra tabla en el modelo con una política de actualización para la actualización incremental configurada.
