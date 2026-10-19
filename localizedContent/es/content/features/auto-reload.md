---
uid: auto-reload
title: Recarga automática desde el disco
author: Morten Lønskov
updated: 2026-10-11
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.27.0
      editions:
        - edition: Desktop
          none: true
          note: "Desktop Edition can't open or save model metadata files."
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# Recarga automática desde el disco

Cuando los archivos de metadatos de un modelo que ha cargado desde un archivo o una carpeta cambian en el disco, Tabular Editor vuelve a cargar el modelo automáticamente. Si tienes cambios sin guardar, aparecerá un mensaje en el que podrás elegir si quieres volver a cargar o conservar tus cambios. Las fuentes típicas de cambios externos son un agente de IA, un script, otro editor, un «git pull» o un compañero que edita una carpeta compartida.

![Diagrama: Archivo > Guardar escribe el modelo en Tabular Editor en los archivos del disco; otra herramienta escribe en los archivos; una recarga automática vuelve a cargar los archivos modificados en Tabular Editor](~/content/assets/images/features/auto-reload-sync.png)

> [!NOTE]
> La recarga automática supervisa los archivos y es independiente de **Rastrear cambios externos del modelo** y **Actualizar automáticamente los metadatos locales de Tabular Object Model** en [Herramientas > Preferencias > Tabular Editor > Varios](xref:preferences#tabular-editor--miscellaneous). Esos ajustes utilizan un seguimiento de Analysis Services para detectar cambios en una base de datos conectada.

## Archivos supervisados

| Modelo cargado desde | Archivos supervisados |
|---|---|
| Un archivo «.bim» | Ese archivo. Se ignoran otros archivos de la misma carpeta. |
| Una carpeta en formato JSON (Database.json) | Todos los archivos «.json» situados bajo la raíz del modelo, incluidas las subcarpetas. |
| Una carpeta en formato [Lenguaje de definición de modelo tabular (TMDL)](xref:tmdl) | Todos los archivos «.tmdl» situados por debajo de la raíz del modelo, incluidas las subcarpetas. |
| Una base de datos del área de trabajo | Los archivos que respaldan el modelo en [modo de área de trabajo](xref:workspace-mode), según las mismas reglas que las filas anteriores. |
| Una base de datos o Power BI Desktop, fuera del modo de área de trabajo | Ninguno. El modelo no tiene archivos en el disco. |
| Una plantilla «.pbit» o un modelo que nunca ha guardado | Ninguno. |

## Recargar con cambios sin guardar

Si tiene cambios sin guardar, aparecerá el mensaje **Cambios externos detectados** y podrá elegir qué versión conservar, ya que Tabular Editor no las combina.

![Mensaje de cambios externos detectados con los botones «Volver a cargar» e «Ignorar», con «Volver a cargar» seleccionado](~/content/assets/images/features/external-changes-prompt.png)

- **Volver a cargar** descarta sus cambios sin guardar y carga la versión en disco.
- **Ignorar** conserva sus cambios. Los archivos en el disco conservan los cambios externos, y su próximo guardado los sobrescribe.

Pulsar **Esc** o cerrar el mensaje tiene el mismo efecto que **Ignorar**.

> [!WARNING]
> **Volver a cargar** es el botón predeterminado, por lo que pulsar **Intro** en el mensaje también vuelve a cargar. Al recargar, se descartan los cambios no guardados sin necesidad de confirmación adicional, y no se puede deshacer la acción.

### Ejemplo

1. Abres un modelo de carpeta TMDL y cambias el nombre de una medida.
2. Un agente de IA que trabaja en la misma carpeta reescribe cuatro archivos «.tmdl».
3. Cuando el agente termina de escribir, aparece un mensaje de **Cambios externos detectados**.
4. Elige **Recargar**, lo que descarta el cambio de nombre y carga los cambios del agente. El Explorador TOM mantiene sus nodos expandidos.

## Múltiples escrituras y cambios en segundo plano

Cuando una herramienta reescribe un modelo serializado en carpetas, cambia muchos archivos en rápida sucesión, y Tabular Editor se vuelve a cargar una vez, cuando finalizan las escrituras.

Si Tabular Editor no es la ventana activa cuando cambian los archivos, la recarga o el mensaje se producen cuando vuelves a él. Todos los cambios realizados mientras estaba inactivo generan un aviso.

## Modo de área de trabajo

En el [modo de área de trabajo](xref:workspace-mode), una recarga también vuelve a implementar el modelo en la base de datos del área de trabajo.

## Desactivación

La recarga automática está habilitada de forma predeterminada y puede desactivarla desmarcando **Recargar automáticamente desde el disco (recarga en caliente)** en **Herramientas > Preferencias > Tabular Editor > Varios**.

![Herramientas > Preferencias > Tabular Editor > Varios, donde se muestra la configuración de recarga automática en Sincronización de metadatos](~/content/assets/images/pref-miscellaneous.png)

Desactívela si un proceso que se ejecuta de forma continua también escribe en la carpeta del modelo, como un cliente de sincronización de archivos o una comprobación de CI que se actualiza en segundo plano. Cada cambio activa una recarga o el mensaje modal cuando tienes cambios sin guardar.

Con el ajuste desactivado, use **Archivo > Recargar desde el disco** para cargar los cambios externos o **Archivo > Guardar** para sobrescribirlos con el modelo en Tabular Editor. Consulte [Preferencias](xref:preferences#tabular-editor--miscellaneous) para ver los demás ajustes de esa página.
