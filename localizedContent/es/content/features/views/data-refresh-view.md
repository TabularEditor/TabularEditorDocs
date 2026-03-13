---
uid: data-refresh-view
title: Vista de actualización de datos
author: Daniel Otykier
updated: 2021-09-08
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Escritorio
          full: true
        - edition: Negocios
          full: true
        - edition: Empresarial
          full: true
---

# Vista de actualización de datos

La vista de Actualización de datos le permite investigar en detalle cómo se están actualizando sus datos en el servidor.
Aparecerá una nueva actualización activa cuando se inicie una actualización desde el Explorador TOM.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-refresh-view.png" alt="Data Refresh View" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 1:</strong> Vista de actualización de datos en Tabular Editor. Se puede iniciar una nueva actualización haciendo clic con el botón derecho en una tabla y seleccionando Actualizar </figcaption>
</figure>

Una nueva actualización se ejecutará en segundo plano para que pueda seguir creando su conjunto de datos, y Tabular Editor le avisará mediante una ventana emergente si la actualización falla.

## Columnas de la vista de actualización de datos

La vista de actualización de datos muestra la siguiente información para cada operación de actualización:

- **Objeto**: El nombre del objeto del modelo que se está actualizando (tabla, partición o modelo)
- **Descripción**: Detalles adicionales sobre la operación de actualización y su estado actual
- **Progreso**: Muestra el número de filas que se han importado hasta el momento.
- **Hora de inicio**: La fecha y la hora en que comenzó la operación de actualización. Esto es útil para llevar un registro de cuándo se iniciaron las operaciones, especialmente cuando hay varias actualizaciones en cola
- **Duración**: El tiempo transcurrido desde que se inició la operación de actualización, actualizado en tiempo real para las operaciones activas

### Ordenar operaciones de actualización

Puedes ordenar las operaciones de actualización haciendo clic en el encabezado de cualquier columna. Esto es especialmente útil para:

- Hacer clic en la columna **Hora de inicio** para ordenar las operaciones de actualización de forma cronológica; las más recientes aparecen primero (orden descendente) o al final (orden ascendente)
- Ordenar por **Duración** para identificar operaciones de larga duración
- Ordenar por **Objeto** para agrupar las actualizaciones por nombre de tabla o partición

Haz clic una vez en el encabezado de una columna para ordenar de forma ascendente, y vuelve a hacer clic para ordenar de forma descendente. Esto facilita identificar las últimas operaciones de actualización cuando trabajas con varias colas de actualización.

> [!NOTA]
> Todos los mensajes y las duraciones que se muestran en la ventana de actualización de datos son solo estimaciones. Tabular Editor escucha los [eventos de seguimiento de SSAS](https://learn.microsoft.com/en-us/analysis-services/trace-events/analysis-services-trace-events?view=asallproducts-allversions) durante el procesamiento. SSAS no garantiza que envíe todos los mensajes de seguimiento al cliente (por ejemplo, puede limitar las notificaciones de eventos de seguimiento durante picos de consumo de CPU/memoria).

> [!TIP]
> Si necesita información precisa y fiable sobre el progreso y la duración de la actualización, debe conectar [SQL Server Profiler](https://learn.microsoft.com/en-us/sql/tools/sql-server-profiler/sql-server-profiler?view=sql-server-ver16) a su instancia de SSAS y recopilar la información manualmente durante el procesamiento.