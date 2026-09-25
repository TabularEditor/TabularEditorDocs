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

Tabular Editor lee los metadatos del modelo desde un archivo, una carpeta o un servidor, los carga en memoria y luego los vuelve a escribir en la misma ubicación o en una nueva.

> [!NOTE]
> Los metadatos son la definición de sus tablas, medidas, relaciones, etc.; no de sus datos. Al cargar un modelo, no se cargan las filas de sus tablas. Consulte [Vista previa de tabla](xref:pivot-grid) y [Actualización avanzada](xref:advanced-refresh) para trabajar con datos.

## Cargar un modelo

![El menú Archivo con el submenú Abrir desplegado, que muestra "Modelo desde archivo", "Modelo desde BD", "Modelo desde carpeta", "Archivo" e "Importar desde YAML de Vista de métricas", junto con los comandos "Guardar", "Guardar como" y "Guardar en carpeta"](~/content/assets/images/file-menu-open.png)

| Fuente                                                                                                                 | Comando                                                                                                                                                                        |
| ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Un archivo `Model.bim` o `.bim`                                                                                        | **Archivo > Abrir > Modelo desde archivo...**                                                                                  |
| Una estructura de carpetas, en formato JSON o [Tabular Model Definition Language (TMDL)](xref:tmdl) | **Archivo > Abrir > Modelo desde carpeta...**                                                                                  |
| Una base de datos XMLA de Analysis Services o Power BI                                                                 | **Archivo > Abrir > Modelo desde BD...** (**Ctrl+Shift+O**)                                                 |
| Una instancia de Power BI Desktop en ejecución                                                                         | **Archivo > Abrir > Modelo desde BD...**, o inicie Tabular Editor desde la cinta **Herramientas externas** de Power BI Desktop |

Un archivo `.bim` debe tener nivel de compatibilidad 1200 o posterior. Los niveles anteriores usan el formato antiguo basado en XML, que Tabular Editor no puede abrir.

Para ver todo lo que Tabular Editor reconoce, incluidos los tipos de archivo auxiliares que no son metadatos del modelo, consulta [Tipos de archivo admitidos](xref:supported-files).

> [!TIP]
> **Archivo > Modelos tabulares recientes** vuelve a abrir un modelo que tuviste abierto anteriormente, ya sea desde un archivo, una carpeta o una base de datos.

## Guardar un modelo

**Archivo > Guardar** (**Ctrl+S**) vuelve a guardar el modelo en el lugar del que lo cargaste. Un modelo cargado desde un archivo se guarda de nuevo en ese archivo. Un modelo cargado desde una carpeta se guarda de nuevo en esa carpeta, en el formato que ya usa. Un modelo cargado desde una base de datos se implementa de nuevo en esa base de datos.

Para guardar un modelo en otro lugar o en otro formato:

- **Archivo > Guardar como...** guarda los metadatos del modelo en un único archivo `.bim`.
- **Archivo > Guardar en carpeta...** guarda los metadatos del modelo como una [estructura de carpetas](xref:save-to-folder), en formato JSON o TMDL, según el modo de serialización establecido en la **preferencia** de **Herramientas > Preferencias > Formatos de archivo > Guardar en carpeta**.

> [!IMPORTANT]
> Un modelo cargado desde una estructura de carpetas JSON heredada se guarda en ese mismo formato cuando usas **Archivo > Guardar**, aunque la **preferencia** esté configurada en TMDL. El formato solo cambia cuando usas explícitamente **Archivo > Guardar en carpeta...**. Consulta [TMDL](xref:tmdl).

## Recargar

**Archivo > Recargar desde el disco** descarta todo lo que has cambiado desde la última vez que guardaste y vuelve a cargar los metadatos desde el origen. Si abriste el modelo desde un servidor, el comando aparece como **Recargar desde el servidor** y, para un modelo cuyo origen aún no se conoce, como **Recargar desde el origen**. En Tabular Editor 3.26 y versiones anteriores, y en Tabular Editor 2, el comando se llama **Archivo > Revertir**.

Solo se te pide confirmación cuando hay algo que perder: si hay cambios sin guardar, primero aparece el mensaje **¿Recargar los metadatos del modelo?**. La barra de estado muestra el Report de la recarga mientras se ejecuta e indica cuándo ha terminado.

Si un agente, un script o un `git pull` reescribe los archivos de metadatos mientras tienes el modelo abierto, Tabular Editor lo detecta y recarga el modelo por ti, para que ambas copias sigan sincronizadas sin necesidad de revertir manualmente. Consulta [Recarga automática desde el disco](xref:auto-reload).

> [!WARNING]
> Haz una copia de seguridad de los metadatos del modelo antes de permitir que cualquier herramienta escriba en ellos, incluido Tabular Editor. Guardar sobrescribe el origen, y la recarga no puede recuperar los cambios que ya hayas guardado.

## Pasos a seguir

- Consulta [Guardar en carpeta](xref:save-to-folder) para conocer los formatos de carpeta y la configuración de serialización que determina cómo se divide un modelo entre archivos.
- [Habilitar el desarrollo en paralelo con Git y la opción Guardar en carpeta](xref:parallel-development) si más de una persona trabaja en el modelo.
- [Implementación](xref:deployment) para escribir el modelo en un servidor de Analysis Services en lugar de guardarlo en el disco.
