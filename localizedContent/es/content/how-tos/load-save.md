---
uid: load-save-model
title: Cargar y guardar metadatos del modelo
author: Morten Lønskov
updated: 2026-09-22
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
          note: "La Edición de escritorio no puede abrir ni guardar archivos de metadatos del modelo."
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Cargar y guardar metadatos del modelo

Tabular Editor carga en memoria los metadatos del modelo desde un archivo, una carpeta o un servidor, y luego los guarda de nuevo en el mismo lugar o en otro.

> [!NOTE]
> Los metadatos son la definición de sus tablas, medidas, relaciones, etc., no los datos en sí. Al cargar un modelo no se cargan las filas de sus tablas. Consulta [Vista previa de tabla](xref:pivot-grid) y [Actualización avanzada](xref:advanced-refresh) para trabajar con datos.

## Cargar un modelo

![El menú Archivo con el submenú Abrir expandido, que muestra Modelo desde archivo, Modelo desde BD, Modelo desde carpeta, Archivo e Importar desde YAML de la vista de métricas, junto con los comandos Guardar, Guardar como y Guardar en carpeta](~/content/assets/images/file-menu-open.png)

| Fuente                                                                                                                           | Comando                                                                                                                                                                       |
| -------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Un archivo `Model.bim` o `.bim`                                                                                                  | **Archivo > Abrir > Modelo desde archivo...**                                                                                 |
| Una estructura de carpetas, en formato JSON o [Lenguaje de definición de modelos tabulares (TMDL)](xref:tmdl) | **Archivo > Abrir > Modelo desde carpeta...**                                                                                 |
| Una base de datos XMLA de Analysis Services o Power BI                                                                           | **Archivo > Abrir > Modelo desde BD...** (**Ctrl+Shift+O**)                                                |
| Una instancia de Power BI Desktop en ejecución                                                                                   | **Archivo > Abrir > Modelo desde BD...** o inicia Tabular Editor desde la cinta **Herramientas externas** de Power BI Desktop |

Un archivo `.bim` debe tener nivel de compatibilidad 1200 o posterior. Los niveles anteriores usan el formato antiguo basado en XML, que Tabular Editor no abre.

Para ver todo lo que reconoce Tabular Editor, incluidos los tipos de archivo admitidos que no son metadatos del modelo, consulta [Tipos de archivo admitidos](xref:supported-files).

> [!TIP]
> **Archivo > Modelos tabulares recientes** vuelve a abrir un modelo que tenías abierto antes, tanto si procedía de un archivo como de una carpeta o una base de datos.

## Guardar un modelo

**Archivo > Guardar** (**Ctrl+S**) guarda de nuevo el modelo en la ubicación desde la que lo cargaste. Un modelo cargado desde un archivo vuelve a ese mismo archivo. Un modelo cargado desde una carpeta vuelve a esa carpeta, en el formato que ya utiliza. Un modelo cargado desde una base de datos se vuelve a implementar en esa misma base de datos.

Para guardar un modelo en otro lugar o en un formato distinto:

- **Archivo > Guardar como...** guarda los metadatos del modelo como un único archivo `.bim`.
- **Archivo > Guardar en carpeta...** guarda los metadatos del modelo como una [estructura de carpetas](xref:save-to-folder), en formato JSON o TMDL, según el modo de serialización configurado en **Herramientas > Preferencia > Formatos de archivo > Guardar en carpeta**.

> [!IMPORTANT]
> Un modelo cargado desde una estructura heredada de carpetas JSON se guarda en ese mismo formato cuando usas **Archivo > Guardar**, aunque tu preferencia indique TMDL. El formato solo cambia cuando usas explícitamente **Archivo > Guardar en carpeta...**. Consulta [TMDL](xref:tmdl).

## Recarga

**Archivo > Recargar desde disco** descarta todo lo que has cambiado desde la última vez que guardaste y vuelve a cargar los metadatos desde el origen. Si abriste un modelo desde un servidor, el comando aparece como **Recargar desde servidor**; y, si el origen del modelo aún no se conoce, como **Recargar desde el origen**. En Tabular Editor 3.26 y versiones anteriores, y en Tabular Editor 2, el comando se llama **Archivo > Revertir**.

Solo se te pide confirmación cuando hay algo que perder: si hay cambios sin guardar, primero aparece el mensaje **¿Recargar metadatos del modelo?**. La barra de estado muestra el Report de la recarga mientras se ejecuta y también cuando ha terminado.

Si un agente, un script o un `git pull` reescribe los archivos de metadatos mientras tienes el modelo abierto, Tabular Editor lo detecta y recarga el modelo por ti, para que ambas copias sigan sincronizadas sin tener que revertir manualmente. Consulta [Recarga automática desde disco](xref:auto-reload).

> [!WARNING]
> Haz una copia de seguridad de los metadatos del modelo antes de permitir que cualquier herramienta escriba en ellos, incluido Tabular Editor. Al guardar se sobrescribe el origen, y al recargar no se pueden recuperar los cambios que ya has guardado.

## Pasos a seguir

- Consulta [Guardar en carpeta](xref:save-to-folder) para conocer los formatos basados en carpetas y la configuración de serialización que controla cómo se divide un modelo entre varios archivos.
- Consulta [Habilitar el desarrollo en paralelo con Git y Guardar en carpeta](xref:parallel-development) si más de una persona trabaja en el modelo.
- Consulta [Implementación](xref:deployment) para escribir el modelo en un servidor de Analysis Services en lugar de hacerlo en disco.
