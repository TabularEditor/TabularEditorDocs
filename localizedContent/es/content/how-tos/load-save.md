---
uid: load-save-model
title: Cargar y guardar metadatos del modelo
author: Morten Lønskov
updated: 2026-09-23
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

Tabular Editor lee los metadatos del modelo desde un archivo, una carpeta o un servidor, los carga en memoria y luego los vuelve a escribir en la misma ubicación o en una nueva.

> [!NOTE]
> Los metadatos definen tablas, medidas y relaciones, pero no contienen datos, y al cargar un modelo no se cargan las filas de sus tablas. Consulta [Vista previa de tabla](xref:table-preview) y [Actualización avanzada](xref:advanced-refresh) para trabajar con datos.

## Cargar un modelo

![El menú Archivo con el submenú Abrir desplegado, que muestra "Modelo desde archivo", "Modelo desde BD", "Modelo desde carpeta", "Archivo" e "Importar desde YAML de Vista de métricas", junto con los comandos "Guardar", "Guardar como" y "Guardar en carpeta"](~/content/assets/images/file-menu-open.png)

| Fuente                                                                                                                 | Comando                                                                                                                                                                        |
| ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Un archivo `Model.bim` o `.bim`                                                                                        | **Archivo > Abrir > Modelo desde archivo...**                                                                                  |
| Una estructura de carpetas, en formato JSON o [Tabular Model Definition Language (TMDL)](xref:tmdl) | **Archivo > Abrir > Modelo desde carpeta...**                                                                                  |
| Una base de datos XMLA de Analysis Services o Power BI                                                                 | **Archivo > Abrir > Modelo desde BD...** (**Ctrl+Shift+O**)                                                 |
| Una instancia de Power BI Desktop en ejecución                                                                         | **Archivo > Abrir > Modelo desde BD...**, o inicie Tabular Editor desde la cinta **Herramientas externas** de Power BI Desktop |

Un archivo `.bim` debe tener nivel de compatibilidad 1200 o posterior. Los niveles anteriores usan el formato antiguo basado en XML, que Tabular Editor no puede abrir.

Para todo lo que Tabular Editor reconoce, incluidos los tipos de archivo compatibles que no son metadatos de modelo, consulta [Tipos de archivo compatibles](xref:supported-files).

> [!TIP]
> **Archivo > Modelos tabulares recientes** reabre un modelo que tenías abierto anteriormente.

## Guardar un modelo

**Archivo > Guardar** (**Ctrl+S**) vuelve a guardar el modelo en el lugar del que lo cargaste. Un modelo cargado desde un archivo se guarda de nuevo en ese archivo. Un modelo cargado desde una carpeta se guarda de nuevo en esa carpeta, en el formato que ya usa. Un modelo cargado desde una base de datos se implementa de nuevo en esa base de datos.

Para guardar un modelo en otro lugar o en otro formato:

- **Archivo > Guardar como...** guarda los metadatos del modelo en un único archivo `.bim`.
- **Archivo > Guardar en carpeta...** guarda los metadatos del modelo como una [estructura de carpetas](xref:save-to-folder), en formato JSON o TMDL, según el modo de serialización de **Herramientas > Preferencias > Formatos de archivo > Guardar en carpeta**.

> [!IMPORTANT]
> Un modelo cargado desde una estructura de carpetas JSON heredada se guarda en ese mismo formato cuando usas **Archivo > Guardar**, aunque la **preferencia** esté configurada en TMDL. El formato solo cambia cuando usas **Archivo > Guardar en carpeta...**. Consulta [TMDL](xref:tmdl).

## Recargar

**Archivo > Recargar desde disco** descarta los cambios realizados desde el último guardado y vuelve a cargar los metadatos desde el origen. Si tienes cambios sin guardar, primero aparece el mensaje **¿Recargar los metadatos del modelo?**. La etiqueta del comando depende del origen del modelo:

| Origen del modelo                                                | Comando                                                                                                                                                              |
| ---------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Un archivo o una carpeta                                         | **Recargar desde disco**                                                                                                                                             |
| Un modelo en [modo del área de trabajo](xref:workspace-mode)     | **Recargar desde disco**. El modelo se vuelve a cargar desde sus archivos y se vuelve a desplegar en la base de datos del Workspace. |
| Analysis Services o Power BI, fuera del modo del área de trabajo | **Recargar desde el servidor**                                                                                                                                       |
| Ningún modelo cargado                                            | **Recargar desde el origen**, deshabilitado                                                                                                                          |

En Tabular Editor 3.26 y versiones anteriores, y en Tabular Editor 2, el comando se llama **Archivo > Revertir**.

En Tabular Editor 3.27.0 y versiones posteriores, cuando un agente, un script o un `git pull` modifica los archivos de metadatos del modelo abierto, el modelo se vuelve a cargar, después de un aviso si tienes cambios sin guardar. Consulta [Recarga automática desde el disco](xref:auto-reload).

> [!WARNING]
> Haz una copia de seguridad de los metadatos del modelo antes de permitir que cualquier herramienta escriba en ellos, incluido Tabular Editor. Guardar sobrescribe el origen, y la recarga no puede recuperar los cambios que ya hayas guardado.

## Pasos a seguir

- Consulta [Guardar en carpeta](xref:save-to-folder) para conocer los formatos de carpeta y la configuración de serialización que determina cómo se divide un modelo entre archivos.
- [Habilitar el desarrollo en paralelo con Git y la opción Guardar en carpeta](xref:parallel-development) si más de una persona trabaja en el modelo.
- [Despliegue](xref:deployment) para escribir el modelo en un servidor de Analysis Services.
