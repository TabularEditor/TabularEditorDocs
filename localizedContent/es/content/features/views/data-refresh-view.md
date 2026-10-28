---
uid: data-refresh-view
title: Vista de actualización de datos
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
# Vista de actualización de datos

La vista **Actualización de datos** muestra el progreso de las operaciones de actualización en el servidor. Una actualización que inicie desde el Explorador TOM aparece en la vista como una actualización activa.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-refresh-view.png" alt="Vista de actualización de datos" style="width: 550px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 1:</strong> Vista de actualización de datos en Tabular Editor. Inicia una actualización haciendo clic con el botón derecho en una tabla y seleccionando «Actualizar».</figcaption>
</figure>

Las actualizaciones se ejecutan en segundo plano mientras sigues editando el modelo, y aparece un mensaje de error si una actualización falla.

## Columnas de la vista Actualización de datos

Cada operación de actualización tiene estas columnas:

- **Objeto**: el objeto del modelo que se está actualizando (tabla, partición o modelo).
- **Descripción**: detalles sobre la operación de actualización y su estado actual.
- **Progreso**: el número de filas importadas hasta el momento.
- **Hora de inicio**: la fecha y hora en que comenzó la operación.
- **Duración**: el tiempo transcurrido desde el inicio de la operación, actualizado en tiempo real para las operaciones activas.

### Ordenación de las operaciones de actualización

Haga clic en un encabezado de columna para ordenar por esa columna: una vez para ordenar de forma ascendente y otra vez para ordenar de forma descendente. Por ejemplo:

- Ordenar por **Hora de inicio**, en orden descendente, para mostrar primero las operaciones de actualización más recientes.
- Ordene por **Duración** para encontrar las operaciones de larga duración.
- Ordene por **Objeto** para agrupar las actualizaciones por nombre de tabla o de partición.

> [!NOTE]
> Todos los mensajes y las duraciones que se muestran en la ventana «Actualización de datos» son solo estimaciones. Tabular Editor escucha los [eventos de seguimiento de SSAS](https://learn.microsoft.com/analysis-services/trace-events/analysis-services-trace-events?view=asallproducts-allversions) durante el procesamiento. No se garantiza que SSAS envíe todos los mensajes de seguimiento al cliente (por ejemplo, puede limitar las notificaciones de eventos de seguimiento durante los momentos de máximo consumo de CPU/memoria). 

> [!TIP]
> Si necesita información precisa y fiable sobre el progreso y la duración de la actualización, debe conectar [SQL Server Profiler](https://learn.microsoft.com/sql/tools/sql-server-profiler/sql-server-profiler?view=sql-server-ver16) a su instancia de SSAS y recopilar la información manualmente durante el procesamiento.
