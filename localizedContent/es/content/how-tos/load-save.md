---
uid: load-save-model
title: Cargar y guardar metadatos del modelo
author: Morten Lønskov
updated: 2026-10-11
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

Tabular Editor lee los metadatos del modelo en la memoria desde un archivo, una carpeta o un servidor, y los vuelve a escribir en el mismo lugar o en uno nuevo.

> [!NOTE]
> Los metadatos definen tablas, medidas y relaciones, pero no contienen datos, y al cargar un modelo no se cargan las filas de sus tablas. Consulte [Vista previa de tabla](xref:table-preview) y [Actualización avanzada](xref:advanced-refresh) para trabajar con datos.

## Cargar un modelo

![El menú «Archivo» con el submenú «Abrir» expandido, que muestra las opciones «Modelo desde archivo», «Modelo desde base de datos», «Modelo desde carpeta», «Archivo» e «Importar desde vista de métrica en formato YAML», junto con los comandos «Guardar», «Guardar como» y «Guardar en carpeta»](~/content/assets/images/file-menu-open.png)

| Origen | Comando |
|---|---|
| Un archivo «Model.bim» o «.bim» | **Archivo > Abrir > Modelo desde archivo...** |
| Una estructura de carpetas, en formato JSON o en formato [Lenguaje de definición de modelo tabular (TMDL)](xref:tmdl) | **Archivo > Abrir > Modelo desde carpeta...** |
| Una base de datos XMLA de Analysis Services o de Power BI | **Archivo > Abrir > Modelo desde BD...** (**Ctrl+Mayús+O**) |
| Una instancia en ejecución de Power BI Desktop | **Archivo > Abrir > Modelo desde BD...**, o inicie Tabular Editor desde la cinta de opciones **Herramientas externas** de Power BI Desktop |

Un archivo «.bim» debe tener un nivel de compatibilidad 1200 o superior. Los niveles anteriores utilizan el formato basado en XML más antiguo, que Tabular Editor no abre.

Para conocer todo lo que Tabular Editor reconoce, incluidos los tipos de archivos compatibles que no son metadatos del modelo, consulte [Tipos de archivos compatibles](xref:supported-files).

> [!TIP]
> **Archivo > Modelos tabulares recientes** vuelve a abrir un modelo que había abierto anteriormente.

## Guardar un modelo

**Archivo > Guardar** (**Ctrl+S**) vuelve a escribir el modelo en el lugar desde donde lo cargó. Un modelo cargado desde un archivo vuelve a ese archivo. Un modelo cargado desde una carpeta vuelve a esa carpeta, en el formato que ya utiliza. Un modelo cargado desde una base de datos se implementa de nuevo en esa base de datos.

Para guardar un modelo en otro lugar o en un formato diferente:

- **Archivo > Guardar como...** guarda los metadatos del modelo como un único archivo «.bim».
- **Archivo > Guardar en carpeta...** guarda los metadatos del modelo como una [estructura de carpetas](xref:save-to-folder), en formato JSON o TMDL, según el modo de serialización establecido en **Herramientas > Preferencias > Formatos de archivo > Guardar en carpeta**.

> [!IMPORTANT]
> Un modelo cargado desde una estructura de carpetas JSON heredada se guarda en ese mismo formato cuando usa **Archivo > Guardar**, incluso si sus preferencias indican TMDL. El formato solo cambia cuando usa **Archivo > Guardar en carpeta...**. Consulta [TMDL](xref:tmdl).

## Recarga

**Archivo > Recargar desde disco** descarta los cambios realizados desde la última vez que se guardó y vuelve a cargar los metadatos desde el origen. Si tienes cambios sin guardar, primero aparecerá el mensaje «**¿Volver a cargar los metadatos del modelo?**». La etiqueta del comando depende del origen del modelo:

| Origen del modelo | Comando |
|---|---|
| Un archivo o una carpeta | **Volver a cargar desde el disco** |
| Un modelo en [modo área de trabajo](xref:workspace-mode) | **Volver a cargar desde el disco**. El modelo se vuelve a cargar a partir de sus archivos y se vuelve a implementar en la base de datos del área de trabajo. |
| Analysis Services o Power BI, fuera del modo de espacio de trabajo | **Volver a cargar desde el servidor** |
| No se cargó ningún modelo | **Volver a cargar desde el origen**, desactivado |

En Tabular Editor 3.26 y versiones anteriores, y en Tabular Editor 2, el comando se llama **Archivo > Revertir**.

En Tabular Editor 3.27.0 y versiones posteriores, cuando un agente, un script o un «git pull» modifican los archivos de metadatos del modelo abierto, el modelo se vuelve a cargar, tras un aviso si hay cambios sin guardar. Consulte [Recarga automática desde el disco](xref:auto-reload).

Los documentos abiertos de consultas DAX y Pivot Grid permanecen abiertos durante una recarga manual o automática y se conectan al modelo recargado.

> [!WARNING]
> Haga una copia de seguridad de los metadatos de su modelo antes de permitir que ninguna herramienta escriba en ellos, incluido Tabular Editor. Al guardar, se sobrescribe el origen, y la recarga no puede recuperar los cambios que ya hayas guardado.

## Próximos pasos

- [Guardar en carpeta](xref:save-to-folder) para conocer los formatos de carpeta y la configuración de serialización que controlan cómo se divide un modelo entre los archivos.
- [Habilitar el desarrollo paralelo mediante Git y Guardar en carpeta](xref:parallel-development) si más de una persona trabaja en el modelo.
- [Implementación](xref:deployment) para escribir el modelo en un servidor de Analysis Services.
