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
          note: "La edición de escritorio no puede abrir los metadatos del modelo desde un archivo o una carpeta, así que no hay nada en el disco con lo que mantenerse sincronizada."
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Recarga automática desde el disco

Mientras trabajas, existen dos copias de tu modelo: la que Tabular Editor mantiene en memoria y los archivos de metadatos en disco desde los que se cargó. Cualquier cosa que modifique una sin modificar la otra hace que se desincronicen.

![Tabular Editor mantiene el modelo en memoria y los archivos en disco contienen el mismo modelo; Archivo > Guardar escribe de la memoria al disco, una recarga automática devuelve los cambios en sentido contrario y otra herramienta, como un agente, un script o un git pull, escribe directamente en los archivos](~/content/assets/images/features/auto-reload-sync.png)

Tabular Editor mantiene ambas copias sincronizadas en ambos sentidos:

| Dirección              | Qué lo mueve                                                                                                                         |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| De la memoria al disco | **Archivo > Guardar** (**Ctrl+S**), cuando quieras.                                               |
| Del disco a la memoria | Automático: Tabular Editor supervisa los archivos y recarga el modelo cuando otra cosa los modifica. |

La otra herramienta suele ser un agente de IA o un script, pero también puede ser otro editor, un `git pull` o un colega que trabaja en una carpeta compartida.

> [!NOTE]
> Se trata de sincronización a nivel de archivo. No es lo mismo que **Supervisar cambios externos del modelo** y **Actualizar automáticamente los metadatos locales de Tabular Object Model**, que aparecen justo al lado en [Herramientas > Preferencias > Varios](xref:preferences#miscellaneous); estas opciones inician una traza de Analysis Services para detectar cambios realizados en una _base de datos conectada_. Los dos mecanismos son independientes y cubren distintas fuentes de cambio.

## Qué supervisa Tabular Editor

| Modelo cargado desde                                                                            | Supervisado                                                                                                                                                                  |
| ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Un archivo `.bim`                                                                               | Ese único archivo. Los demás archivos de la misma carpeta se ignoran.                                                                        |
| Una carpeta en formato JSON (Database.json)                  | Todos los archivos `.json` bajo la raíz del modelo, incluidas las subcarpetas.                                                                               |
| Una carpeta en formato [Tabular Model Definition Language (TMDL)](xref:tmdl) | Todos los archivos `.tmdl` bajo la raíz del modelo, incluidas las subcarpetas.                                                                               |
| Una base de datos del Workspace                                                                 | Los archivos que respaldan el modelo en [modo del área de trabajo](xref:workspace-mode), supervisados con las mismas reglas que en las dos filas anteriores. |
| Una base de datos o Power BI Desktop, fuera del modo del área de trabajo                        | Nada. El modelo no tiene archivos en disco, así que no hay dos copias que conciliar.                                                         |
| Una plantilla `.pbit` o un modelo que nunca has guardado                                        | Nada. Un `.pbit` es un archivo binario que ninguna herramienta externa edita directamente.                                                   |

## Cuando solo cambiaron los archivos

Si no tienes cambios sin guardar, solo cambió una copia, así que no hay nada que sopesar. Tabular Editor vuelve a cargar el modelo y ambas copias quedan sincronizadas de nuevo.

## Cuando cambiaron ambas copias

Si también tienes cambios sin guardar, ambas copias cambiaron y no coinciden. Tabular Editor no puede combinar los metadatos del modelo, así que te pide que elijas qué copia prevalece.

![Mensaje mostrado cuando Tabular Editor detecta que cambiaron ambas copias](~/content/assets/images/features/external-changes-prompt.png)

- **Recargar** descarta tus cambios sin guardar y usa la versión en disco.
- **Ignorar** conserva tus cambios y deja el modelo tal como está. Los archivos del disco no se tocan, así que las dos copias siguen separadas hasta que tu próximo guardado los sobrescriba.

**Ignorar** es la opción predeterminada más segura. Pulsar Esc o cerrar el cuadro de diálogo con el botón de cierre de la ventana conserva tus cambios exactamente igual que **Ignorar**.

> [!WARNING]
> Si eliges **Recargar**, Tabular Editor descarta tus cambios no guardados sin pedirte otra confirmación y no puedes deshacer la recarga.

### Una secuencia típica

1. Abres un modelo TMDL basado en carpetas y cambias el nombre de una medida. La copia en memoria va por delante de los archivos.
2. Un agente de IA que trabaja en la misma carpeta reescribe cuatro archivos `.tmdl`. Ahora ambas copias han avanzado, pero en direcciones distintas.
3. Tabular Editor espera a que se estabilicen las escrituras del agente y luego muestra un único aviso de **External changes detected**.
4. Eliges **Recargar**. Se pierde el cambio de nombre de la medida, se cargan los cuatro archivos del agente, las dos copias quedan sincronizadas y el Explorador TOM sigue expandido en la tabla en la que estabas trabajando.

Si hubieras elegido **Ignorar**, el cambio de nombre se habría conservado, las copias habrían seguido separadas y los cuatro archivos del agente se sobrescribirían la próxima vez que pulsaras **Ctrl+S**.

## Consolidación y cambios en segundo plano

Una herramienta que reescribe un modelo serializado en carpetas modifica muchos archivos en rápida sucesión. Tabular Editor espera a que las escrituras se estabilicen y luego recarga una sola vez, no una vez por archivo.

Los cambios que llegan mientras Tabular Editor está en segundo plano se retienen en lugar de notificarse de inmediato. Se te pregunta una sola vez cuando vuelves a Tabular Editor, así que al regresar de una sesión con un agente que reescribió una docena de archivos recibes un único aviso.

## Modo del área de trabajo

El [modo del área de trabajo](xref:workspace-mode) añade una tercera copia: la base de datos del Workspace en el servidor. Al recargar, también se vuelve a implementar, de modo que las tres copias quedan sincronizadas en lugar de dejar al servidor con metadatos que los archivos ya no describen.

## Desactivarlo

La recarga automática está habilitada de forma predeterminada. Para que la sincronización del disco a la memoria vuelva a ser manual, desmarca **Recargar automáticamente desde el disco** en **Herramientas > Preferencia > Varios**.

![Herramientas > Preferencia > Varios, mostrando la configuración de recarga automática en Sincronización de metadatos](~/content/assets/images/pref-miscellaneous.png)

Desactiva esta opción cuando la carpeta del modelo también la modifique algún proceso que se ejecute de forma continua, como un cliente de sincronización de archivos o un checkout de CI que se actualice en segundo plano. El cuadro de diálogo es modal, así que una carpeta que cambia con frecuencia te interrumpe en lugar de ayudarte.

Con la opción desactivada, Tabular Editor no supervisa ningún cambio y las dos copias solo vuelven a coincidir cuando usas **Archivo > Recargar desde el disco** o **Archivo > Guardar**.

Consulta [Preferencias](xref:preferences#miscellaneous) para ver el resto de las opciones de esa página.
