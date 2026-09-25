---
uid: auto-reload
title: Recarga automática desde el disco
author: Morten Lønskov
updated: 2026-09-22
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.27.0
      editions:
        - edition: Desktop
          none: true
          note: "La Edición de escritorio no puede abrir los metadatos del modelo desde un archivo o una carpeta, así que no hay nada en el disco con lo que mantenerse sincronizada."
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Recarga automática desde el disco

Mientras trabajas, existen dos copias de tu modelo: la que Tabular Editor mantiene en memoria y los archivos de metadatos en el disco desde los que se cargó. Cualquier cosa que modifique una sin modificar la otra hace que se desincronicen.

![Tabular Editor mantiene el modelo en memoria y los archivos en disco guardan ese mismo modelo; Archivo > Guardar escribe de la memoria al disco; una recarga automática devuelve los cambios en sentido contrario; y otra herramienta, como un agente, un script o un Git pull, escribe directamente en los archivos](~/content/assets/images/features/auto-reload-sync.png)

Tabular Editor mantiene ambos sincronizados en las dos direcciones:

| Dirección       | Qué lo mueve                                                                                                                     |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Memoria a disco | **Archivo > Guardar** (**Ctrl+S**), cuando quieras.                                           |
| Disco a memoria | Automático, ya que Tabular Editor supervisa los archivos y vuelve a cargar el modelo cuando algo más los cambia. |

La otra herramienta suele ser un agente de IA o un script, pero también puede ser otro editor, un `git pull` o un compañero que trabaje en una carpeta compartida.

> [!NOTE]
> Esta es una sincronización a nivel de archivo. No es lo mismo que **Realizar seguimiento de los cambios externos del modelo** y **Actualizar automáticamente los metadatos locales del Tabular Object Model**, que aparecen junto a esta en [Herramientas > Preferencias > Varios](xref:preferences#miscellaneous), pero inician una traza de Analysis Services para detectar cambios realizados en una _base de datos conectada_. Los dos mecanismos son independientes y cubren fuentes de cambio distintas.

## Qué supervisa Tabular Editor

| Modelo cargado desde                                                                            | Vigilado                                                                                                                                                                       |
| ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Un archivo `.bim`                                                                               | Solo ese archivo. Se ignoran los demás archivos de la misma carpeta.                                                                           |
| Una carpeta en formato JSON (Database.json)                  | Todos los archivos `.json` que estén bajo la raíz del modelo, incluidos los de las subcarpetas.                                                                |
| Una carpeta en formato [Tabular Model Definition Language (TMDL)](xref:tmdl) | Todos los archivos `.tmdl` debajo de la raíz del modelo, incluidas las subcarpetas.                                                                            |
| Una base de datos del Workspace                                                                 | Los archivos que respaldan el modelo en [modo del área de trabajo](xref:workspace-mode), supervisados según las mismas reglas que en las dos filas anteriores. |
| Una base de datos o Power BI Desktop, fuera del modo del área de trabajo                        | Nada. El modelo no tiene archivos en disco, así que no hay dos copias que conciliar.                                                           |
| Una plantilla `.pbit` o un modelo que nunca has guardado                                        | Nada. Un `.pbit` es un archivo binario que ninguna herramienta externa edita directamente.                                                     |

## Cuando solo cambiaron los archivos

Si no tienes cambios sin guardar, solo cambió una de las copias, así que no hay nada que decidir. Tabular Editor vuelve a cargar el modelo y ambas copias vuelven a estar sincronizadas.

## Cuando cambiaron ambas copias

Si también tienes cambios sin guardar, ambas copias cambiaron y ya no coinciden. Tabular Editor no puede combinar los metadatos del modelo, así que te pide que elijas qué copia debe prevalecer.

![Mensaje que aparece cuando Tabular Editor detecta que ambas copias se modificaron](~/content/assets/images/features/external-changes-prompt.png)

- **Recargar** descarta tus cambios sin guardar y usa la versión en disco.
- **Ignorar** conserva tus cambios y deja el modelo tal como está. Los archivos del disco no se tocan, así que ambas copias permanecen separadas hasta que el próximo guardado las sobrescriba.

**Ignorar** es la opción predeterminada más segura. Pulsar Esc o cerrar el aviso con el botón de la ventana conserva tus cambios exactamente igual que **Ignorar**.

> [!WARNING]
> Si eliges **Recargar**, Tabular Editor descartará los cambios no guardados sin pedir confirmación adicional y no podrás deshacer la recarga.

### Una secuencia típica

1. Abres un modelo TMDL basado en carpetas y cambias el nombre de una medida. La copia en memoria va por delante de los archivos.
2. Un agente de IA que trabaja en la misma carpeta reescribe cuatro archivos `.tmdl`. Ahora ambas copias han avanzado, pero en direcciones distintas.
3. Tabular Editor espera a que terminen las escrituras del agente y, después, muestra un único aviso: **Cambios externos detectados**.
4. Eliges **Recargar**. El cambio de nombre de tu medida se pierde, se cargan los cuatro archivos del agente, ambas copias vuelven a estar sincronizadas y el Explorador TOM sigue expandido en la tabla en la que estabas trabajando.

Si hubieras elegido **Ignorar**, el cambio de nombre se habría conservado, las copias habrían seguido separadas y los cuatro archivos del agente se sobrescribirían la próxima vez que pulsaras **Ctrl+S**.

## Agrupación y cambios en segundo plano

Una herramienta que reescribe un modelo serializado en carpetas modifica muchos archivos en rápida sucesión. Tabular Editor espera a que las escrituras se estabilicen y luego recarga una sola vez, no una vez por archivo.

Los cambios que llegan mientras Tabular Editor está en segundo plano quedan en espera en lugar de mostrarse de inmediato. Se te pregunta una sola vez cuando vuelves a Tabular Editor, así que, si regresas de una sesión con un agente que reescribió una docena de archivos, verás un único aviso.

## Modo del área de trabajo

[modo del área de trabajo](xref:workspace-mode) añade una tercera copia: la base de datos de Workspace en el servidor. Una recarga también la vuelve a implementar, de modo que las tres sigan sincronizadas, en lugar de dejar el servidor con metadatos que los archivos ya no describen.

## Desactivarlo

La recarga automática está habilitada de forma predeterminada. Para que la carga del disco a la memoria vuelva a ser manual, desmarca **Recargar automáticamente desde el disco** en **Herramientas > Preferencia > Varios**.

![Herramientas > Preferencia > Varios, mostrando la configuración de recarga automática en Sincronización de metadatos](~/content/assets/images/pref-miscellaneous.png)

Desactiva esta opción cuando la carpeta del modelo también la modifique continuamente algún proceso, como un cliente de sincronización de archivos o un checkout de CI que se actualiza en segundo plano. El cuadro de diálogo es modal, así que una carpeta que cambia con frecuencia te interrumpe en lugar de ayudarte.

Con la opción desactivada, Tabular Editor no supervisa nada y las dos copias solo vuelven a coincidir cuando usas **Archivo > Recargar desde el disco** o **Archivo > Guardar**.

Consulta [Preferencias](xref:preferences#miscellaneous) para ver el resto de las opciones de esa página.
