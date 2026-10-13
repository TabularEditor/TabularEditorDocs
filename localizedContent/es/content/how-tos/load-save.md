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
          note: "Desktop Edition can't open or save model metadata files."
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Cargar y guardar metadatos del modelo

Tabular Editor lee los metadatos del modelo desde un archivo, una carpeta o un servidor, los carga en memoria y luego los vuelve a escribir en la misma ubicación o en una nueva.

> [!NOTE]
> Metadata defines tables, measures and relationships but contains no data, and loading a model doesn't load the rows in its tables. See [Table Preview](xref:table-preview) and [Advanced refresh](xref:advanced-refresh) for working with data.

## Cargar un modelo

![El menú Archivo con el submenú Abrir desplegado, que muestra "Modelo desde archivo", "Modelo desde BD", "Modelo desde carpeta", "Archivo" e "Importar desde YAML de Vista de métricas", junto con los comandos "Guardar", "Guardar como" y "Guardar en carpeta"](~/content/assets/images/file-menu-open.png)

| Fuente                                                                                                                 | Comando                                                                                                                                                                        |
| ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Un archivo `Model.bim` o `.bim`                                                                                        | **File > Open > Model from File...**                                                                                           |
| Una estructura de carpetas, en formato JSON o [Tabular Model Definition Language (TMDL)](xref:tmdl) | **File > Open > Model from Folder...**                                                                                         |
| Una base de datos XMLA de Analysis Services o Power BI                                                                 | **Archivo > Abrir > Modelo desde BD...** (**Ctrl+Shift+O**)                                                 |
| Una instancia de Power BI Desktop en ejecución                                                                         | **Archivo > Abrir > Modelo desde BD...**, o inicie Tabular Editor desde la cinta **Herramientas externas** de Power BI Desktop |

Un archivo `.bim` debe tener nivel de compatibilidad 1200 o posterior. Los niveles anteriores usan el formato antiguo basado en XML, que Tabular Editor no puede abrir.

For everything Tabular Editor recognizes, including the supporting file types that aren't model metadata, see [Supported file types](xref:supported-files).

> [!TIP]
> **File > Recent Tabular Models** reopens a model you had open before.

## Guardar un modelo

**Archivo > Guardar** (**Ctrl+S**) vuelve a guardar el modelo en el lugar del que lo cargaste. Un modelo cargado desde un archivo se guarda de nuevo en ese archivo. Un modelo cargado desde una carpeta se guarda de nuevo en esa carpeta, en el formato que ya usa. Un modelo cargado desde una base de datos se implementa de nuevo en esa base de datos.

Para guardar un modelo en otro lugar o en otro formato:

- **Archivo > Guardar como...** guarda los metadatos del modelo en un único archivo `.bim`.
- **File > Save to Folder...** saves the model metadata as a [folder structure](xref:save-to-folder), in either the JSON or the TMDL format, depending on the serialization mode under **Tools > Preferences > File Formats > Save-to-folder**.

> [!IMPORTANT]
> Un modelo cargado desde una estructura de carpetas JSON heredada se guarda en ese mismo formato cuando usas **Archivo > Guardar**, aunque la **preferencia** esté configurada en TMDL. The format changes only when you use **File > Save to Folder...**. Consulta [TMDL](xref:tmdl).

## Recargar

**File > Reload from disk** discards your changes since the last save and reloads the metadata from the source. If you have unsaved changes, a **Reload model metadata?** prompt appears first. The command label depends on the model source:

| Model source                                          | Comando                                                                                                                         |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| A file or folder                                      | **Reload from disk**                                                                                                            |
| A model in [workspace mode](xref:workspace-mode)      | **Reload from disk**. The model reloads from its files and redeploys to the workspace database. |
| Analysis Services or Power BI, outside workspace mode | **Reload from server**                                                                                                          |
| No model loaded                                       | **Reload from source**, disabled                                                                                                |

En Tabular Editor 3.26 y versiones anteriores, y en Tabular Editor 2, el comando se llama **Archivo > Revertir**.

In Tabular Editor 3.27.0 and later, when an agent, a script or a `git pull` changes the metadata files of the open model, the model is reloaded, after a prompt if you have unsaved changes. Consulta [Recarga automática desde el disco](xref:auto-reload).

> [!WARNING]
> Haz una copia de seguridad de los metadatos del modelo antes de permitir que cualquier herramienta escriba en ellos, incluido Tabular Editor. Guardar sobrescribe el origen, y la recarga no puede recuperar los cambios que ya hayas guardado.

## Pasos a seguir

- Consulta [Guardar en carpeta](xref:save-to-folder) para conocer los formatos de carpeta y la configuración de serialización que determina cómo se divide un modelo entre archivos.
- [Habilitar el desarrollo en paralelo con Git y la opción Guardar en carpeta](xref:parallel-development) si más de una persona trabaja en el modelo.
- [Deployment](xref:deployment) to write the model to an Analysis Services server.
