---
uid: auto-reload
title: Recarga automática desde el disco
author: Morten Lønskov
updated: 2026-09-23
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.27.0
      editions:
        - edition: Desktop
          none: true
          note: "La Edición de escritorio no puede abrir ni guardar archivos de metadatos del modelo."
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Recarga automática desde el disco

Cuando los archivos de metadatos de un modelo que cargaste desde un archivo o una carpeta cambian en disco, Tabular Editor vuelve a cargar el modelo automáticamente. Si tienes cambios sin guardar, aparecerá un aviso en el que podrás elegir entre recargar o conservar tus cambios. Las fuentes típicas de cambios externos son un agente de IA, un script, otro editor, un `git pull` o un compañero que edita una carpeta compartida.

![Diagrama: Archivo > Guardar escribe el modelo de Tabular Editor en los archivos en disco; otra herramienta escribe en los archivos; una recarga automática vuelve a cargar los archivos modificados en Tabular Editor](~/content/assets/images/features/auto-reload-sync.png)

> [!NOTE]
> La recarga automática supervisa los archivos y es independiente de **Realizar seguimiento de cambios externos del modelo** y **Actualizar automáticamente los metadatos locales de Tabular Object Model** en [Herramientas > Preferencias > Tabular Editor > Varios](xref:preferences#miscellaneous). Esas opciones usan una traza de Analysis Services para detectar cambios en una base de datos conectada.

## Archivos supervisados

| Modelo cargado desde                                                                            | Archivos supervisados                                                                                                                                         |
| ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Un archivo `.bim`                                                                               | Ese archivo. Se ignoran los demás archivos de la misma carpeta.                                                               |
| Una carpeta en formato JSON (Database.json)                  | Todos los archivos `.json` que estén bajo la raíz del modelo, incluidos los de las subcarpetas.                                               |
| Una carpeta en formato [Tabular Model Definition Language (TMDL)](xref:tmdl) | Todos los archivos `.tmdl` debajo de la raíz del modelo, incluidas las subcarpetas.                                                           |
| Una base de datos del Workspace                                                                 | Los archivos que respaldan el modelo en [modo del área de trabajo](xref:workspace-mode), según las mismas reglas que en las filas anteriores. |
| Una base de datos o Power BI Desktop, fuera del modo del área de trabajo                        | Ninguno. El modelo no tiene archivos en disco.                                                                                |
| Una plantilla `.pbit` o un modelo que nunca has guardado                                        | Ninguno.                                                                                                                                      |

## Recargar con cambios sin guardar

Si tienes cambios sin guardar, aparece el aviso **Se detectaron cambios externos** y eliges qué versión conservar, porque Tabular Editor no las fusiona.

![Aviso «Se detectaron cambios externos» con los botones Recargar e Ignorar, con Recargar seleccionado](~/content/assets/images/features/external-changes-prompt.png)

- **Recargar** descarta tus cambios sin guardar y carga la versión en disco.
- **Ignorar** conserva tus cambios. Los archivos en disco conservan los cambios externos y la próxima vez que guardes los sobrescribirás.

Pulsar **Esc** o cerrar el aviso tiene el mismo efecto que **Ignorar**.

> [!WARNING]
> **Recargar** es el botón predeterminado, así que pulsar **Enter** en el aviso también recarga. Una recarga descarta tus cambios sin guardar sin más confirmación, y no puedes deshacerla.

### Ejemplo

1. Abres un modelo TMDL basado en carpetas y cambias el nombre de una medida.
2. Un agente de IA que trabaja en la misma carpeta reescribe cuatro archivos `.tmdl`.
3. Cuando el agente termina de escribir, aparece un único aviso **Se detectaron cambios externos**.
4. Eliges **Recargar**, lo que descarta el cambio de nombre y carga los cambios del agente. El Explorador TOM conserva sus nodos expandidos.

## Múltiples escrituras y cambios en segundo plano

Cuando una herramienta reescribe un modelo serializado en una carpeta, cambia muchos archivos en rápida sucesión y Tabular Editor se recarga una sola vez, cuando finalizan las escrituras.

Si Tabular Editor no es la ventana activa cuando cambian los archivos, la recarga o el aviso se produce cuando vuelves a activarlo. Todos los cambios realizados mientras estaba inactivo generan un único aviso.

## Modo del área de trabajo

En [modo del área de trabajo](xref:workspace-mode), una recarga también vuelve a implementar el modelo en la base de datos de Workspace.

## Desactivarlo

La recarga automática está activada de forma predeterminada. Para desactivarla, desmarca **Recargar automáticamente desde el disco (hot reload)** en **Herramientas > Preferencias > Tabular Editor > Varios**.

![Herramientas > Preferencias > Tabular Editor > Varios, que muestra la opción de recarga automática en Sincronización de metadatos](~/content/assets/images/pref-miscellaneous.png)

Desactívala si un proceso que se ejecuta continuamente también escribe en la carpeta del modelo, como un cliente de sincronización de archivos o un checkout de CI que se actualiza en segundo plano. Cada cambio desencadena una recarga o, si tienes cambios sin guardar, aparece un cuadro de diálogo modal.

Con la opción desmarcada, usa **Archivo > Recargar desde el disco** para cargar cambios externos, o **Archivo > Guardar** para sobrescribirlos con el modelo en Tabular Editor. Consulta [Preferencias](xref:preferences#miscellaneous) para ver las demás opciones de esa página.
