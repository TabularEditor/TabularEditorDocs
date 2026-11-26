---
uid: data-refresh-view
title: Vista de actualización de datos
author: Daniel Otykier
updated: 2026-11-13
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
  <img class="noscale" src="~/content/assets/images/data-refresh-view.png" alt="Vista de actualización de datos con una tarea completada expandida a sus tablas y particiones, cada una con su propia duración" style="width: 550px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 1:</strong> Vista de actualización de datos en Tabular Editor. Inicia una actualización haciendo clic con el botón derecho en una tabla y seleccionando «Actualizar».</figcaption>
</figure>

Las actualizaciones se ejecutan en segundo plano mientras sigues editando el modelo, y aparece un mensaje de error si una actualización falla.

Cada actualización es una fila de trabajo que se expande a una fila por cada tabla y partición que actualiza el servidor. En el caso de una actualización breve, estas filas aparecen unos segundos después de que finalice el trabajo. Una fila para la que el servidor informa de un error permanece marcada como fallida. Si una actualización falla antes de llegar al servidor, una fila de error debajo de la tarea muestra el motivo.

## Columnas de la vista de actualización de datos

Cada operación de actualización tiene estas columnas:

- **Objeto**: el objeto del modelo que se está actualizando (tabla, partición o modelo).
- **Descripción**: detalles sobre la operación de actualización y su estado actual.
- **Progreso**: el número de filas importadas hasta el momento.
- **Hora de inicio**: la fecha y hora en que comenzó la operación.
- **Duración**: el tiempo que el servidor dedicó al objeto. Mientras se ejecuta una operación, la columna muestra el tiempo transcurrido hasta el momento, actualizado en tiempo real.

### Ordenar operaciones de actualización

Haga clic en un encabezado de columna para ordenar por esa columna: una vez para hacerlo de forma ascendente y otra vez para hacerlo de forma descendente. Por ejemplo:

- Ordenar por **Hora de inicio**, en orden descendente, para mostrar primero las operaciones de actualización más recientes.
- Ordene por **Duración** para encontrar las operaciones de larga duración.
- Ordene por **Objeto** para agrupar las actualizaciones por nombre de tabla o de partición.

> [!NOTE]
> Las filas, los mensajes y las duraciones proceden de los [eventos de seguimiento](https://learn.microsoft.com/analysis-services/trace-events/analysis-services-trace-events?view=asallproducts-allversions) que el servidor envía durante la actualización. El servidor no garantiza la entrega de todos los eventos de seguimiento, por ejemplo, cuando limita las notificaciones de seguimiento bajo una carga elevada de la CPU o de la memoria. Falta una fila cuyos eventos no llegan, y una fila cuyos primeros eventos no llegan muestra una duración demasiado corta.

> [!TIP]
> Si necesita información precisa y fiable sobre el progreso y la duración de las actualizaciones, debe conectar [SQL Server Profiler](https://learn.microsoft.com/sql/tools/sql-server-profiler/sql-server-profiler?view=sql-server-ver16) a su instancia de SSAS y recopilar la información manualmente durante el procesamiento.
