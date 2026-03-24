---
uid: incremental-refresh-workspace-mode
title: Uso del modo del área de trabajo en un modelo con actualización incremental
author: Kurt Buhler
updated: 2023-01-09
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.4.2 y versiones anteriores
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Modo del área de trabajo y actualización incremental

> [!IMPORTANT]
> Este artículo solo se aplica a las versiones 3.4.2 y anteriores de Tabular Editor.
> Desde la actualización 3.5.0, el _modo del área de trabajo_ no sobrescribirá las particiones de la política de actualización implementadas mediante actualizaciones programadas.
> Las particiones de política de actualización tampoco se serializarán en el control de código fuente. Puedes cambiar esta configuración en _'Tools > Preferencias... > Save-to-Folder'_.

---

![Resumen Visual del modo del área de trabajo con actualización incremental](~/content/assets/images/tutorials/incremental-refresh-workspace-mode.png)

---

La actualización incremental crea nuevas particiones en la primera actualización programada del día. Como resultado, cualquier metadato local (es decir, `.bim` o `Database.json`) quedará desincronizado respecto a los metadatos del modelo remoto después de la actualización. Como resultado, **al trabajar con un modelo que tenga tablas configuradas con actualización incremental, no se recomienda el _modo del área de trabajo_.**.

> [!IMPORTANT]
> La configuración de la actualización incremental con Tabular Editor 3 se limita al Dataset alojado en el servicio Power BI Datasets. Para Analysis Services, se requiere una [creación de particiones](https://learn.microsoft.com/en-us/analysis-services/tabular-models/partitions-ssas-tabular?view=asallproducts-allversions) personalizada.

---

### No se recomienda el modo del área de trabajo

El motivo es que el _modo del área de trabajo_ sobrescribirá los metadatos del modelo remoto con los archivos de metadatos locales; se perderán los cambios que no estén sincronizados (por ejemplo, en las particiones del intervalo de la política). Al trabajar con el _modo del área de trabajo_ en estos modelos, tendrías que _Aplicar la política de actualización_ a las tablas que usan actualización incremental antes de guardar los cambios cada día.

![El modo del área de trabajo puede desincronizarse de los metadatos locales.](~/content/assets/images/tutorials/incremental-refresh-workspace-mode-out-of-sync.png)

### Recomendación: Desarrollar e implementar desde metadatos locales

**En su lugar, se recomienda desarrollar el modelo a partir de los archivos de metadatos locales.** Puedes implementar los cambios excluyendo las particiones regidas por una política de actualización, por lo que no hay riesgo de sobrescribir las políticas creadas por Power BI. Puedes conectar una segunda instancia de lectura/actualización de Tabular Editor al modelo remoto con fines de prueba.

Para implementar el modelo, ve a _Model > Deploy..._, lo que abre el Asistente de implementación. Aquí puedes seleccionar si quieres incluir particiones regidas por políticas de actualización incremental:

![Implementar particiones, evitando las que tienen políticas de actualización.](~/content/assets/images/tutorials/incremental-refresh-deploy-partitions.png)

Al implementar el modelo sin estas particiones de Policy Range, mitigas cualquier posible impacto debido a particiones de actualización incremental desincronizadas entre los metadatos y el modelo remoto.