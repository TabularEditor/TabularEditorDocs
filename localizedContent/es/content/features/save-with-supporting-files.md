---
uid: save-with-supporting-files
title: Guardar con archivos de apoyo
author: Peer Grønnerup
updated: 2026-09-23
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Guardar con archivos de apoyo

La opción Guardar con archivos auxiliares guarda un modelo semántico junto con los archivos de metadatos que requiere la integración de Git de Microsoft Fabric. Úselo para sincronizar un modelo guardado con Tabular Editor entre un Workspace de Fabric y un repositorio de Git.

> [!NOTE]
> Guardar con archivos auxiliares está disponible al guardar en un archivo .bim (TMSL) o en una carpeta, con TMDL como modo de serialización.

## Estructura de archivos y propiedades del modelo

Tabular Editor crea una carpeta llamada **Database Name.SemanticModel** en la ubicación de guardado. El nombre proviene de la propiedad `Name` del objeto Database en el Explorador TOM. Fabric reconoce una carpeta como un elemento de modelo semántico solo si su nombre termina en **.SemanticModel**.

Tabular Editor también copia la propiedad `Name` de Database en la propiedad `displayName` del archivo de metadatos .platform, y la propiedad `Description` de Database en la propiedad `description`.

<a name="power-bi-desktop-authored-pbip-projects"></a>

### Proyectos PBIP creados con Power BI Desktop

En un modelo semántico de [Proyecto de Power BI (PBIP)](https://learn.microsoft.com/power-bi/developer/projects/projects-overview) creado en Power BI Desktop, el nombre y la descripción del elemento se almacenan solo en el archivo `.platform`, y los metadatos del modelo no incluyen ninguno de los dos.

Para estos modelos, Tabular Editor conserva los valores existentes de `displayName` y `description` en `.platform` y asigna a la nueva carpeta el nombre del elemento.

> [!NOTE]
> Antes de Tabular Editor 3.27.0, al guardar estos modelos se cambiaba el nombre del elemento y se borraba su descripción en el Workspace de Fabric en la siguiente sincronización con Git.

Si establece las propiedades `Name` y `Description` en el objeto Database, Tabular Editor las sincroniza con `.platform` en cada guardado.

### Archivos incluidos

Todos los modelos guardados incluyen estos archivos:

- **.platform**: metadatos del elemento, que incluyen su tipo, el nombre para mostrar, la descripción y `logicalId`, un identificador entre Workspaces generado automáticamente.
- **definition.pbism**: la definición y la configuración principal del modelo semántico.

El propio modelo se almacena según el formato de serialización:

| Formato                                            | Almacenamiento del modelo                                                    |
| -------------------------------------------------- | ---------------------------------------------------------------------------- |
| **TMDL**                                           | Carpeta `definition` que contiene archivos TMDL con los metadatos del modelo |
| **TMSL (.bim)** | archivo `model.bim` (el nombre del archivo es fijo)       |

Estructura de carpetas para una base de datos llamada "Sales":

```text
Sales.SemanticModel/
├── .platform
├── definition.pbism
├── model.bim                    (if saved as TMSL)
└── definition/                  (if saved as TMDL)
    ├── database.tmdl
    ├── tables.tmdl
    └── ...
```

## Cómo guardar con archivos auxiliares

1. Crea o abre un modelo semántico en Tabular Editor 3.
2. Establece la propiedad `Name` del objeto Database en el Explorador TOM. Esto establece el nombre de la carpeta y el `displayName` en el archivo .platform.
   ![Establecer la propiedad Name de la base de datos](~/content/assets/images/common/SaveWithSupportingFilesSetName.png)
3. Si guardas en una carpeta, establece el modo de serialización en TMDL en **Herramientas > Preferencias > Formatos de archivo**.
4. Selecciona **Archivo > Guardar como** o **Archivo > Guardar en carpeta**.
5. Elige una carpeta y selecciona **Guardar con archivos complementarios**.
   ![Cuadro de diálogo Guardar con archivos complementarios](~/content/assets/images/common/SaveWithSupportingFilesDialog.png)
6. Haz clic en **Guardar**.

Tabular Editor crea la carpeta **.SemanticModel** —por ejemplo, `Sales.SemanticModel`— en la ubicación de guardado y escribe los archivos en ella.

## Integración de Git en Microsoft Fabric

La integración de Git está disponible en los Workspace asignados a la capacidad Microsoft Fabric F-SKU, a la capacidad Power BI Premium o a Power BI Premium Per User (PPU).

> [!WARNING]
> La integración de Git para el elemento de modelo semántico se encuentra en versión preliminar. Para ver la lista de elementos compatibles, consulta [Elementos compatibles en la integración de Git de Fabric](https://learn.microsoft.com/en-us/fabric/cicd/git-integration/intro-to-git-integration#supported-items).

> [!CAUTION]
> No habilites la integración de Git en el Workspace de Fabric que aloja las bases de datos del Workspace de Tabular Editor. Si Tabular Editor sincroniza un modelo con un Workspace conectado a Git, el Workspace muestra cambios sin confirmar que no coinciden con el repositorio, y al sincronizarlos se generan conflictos de Git.
>
> Mantén separados el repositorio de Git y el Workspace, y despliega modelos semánticos en los Workspace con Tabular Editor, las API REST de Fabric, Fabric CLI o la biblioteca de Python fabric-cicd.

### Uso de la integración de Git con Tabular Editor

Después de guardar el modelo con archivos complementarios, sincronízalo con Microsoft Fabric:

1. Guarda el modelo en Tabular Editor con la opción **Guardar con archivos complementarios** seleccionada.
2. Haz commit de los cambios en tu repositorio de Git.
3. Conecta tu Workspace de Fabric al repositorio de Git.
4. Haz clic en **Actualizar todo** en el panel de control de código fuente del Workspace.
   ![Sincronizar el Workspace con Git](~/content/assets/images/common/WorkspaceGitSync.png)

El Workspace muestra el modelo semántico con el valor de `displayName` del archivo .platform, que es el `Name` de la base de datos que estableces en Tabular Editor.

Si el modelo no tiene configuración regional, Tabular Editor la establece en **en-US** al guardar con archivos de soporte. Sin una configuración regional, la sincronización inicial con Fabric deja cambios sin confirmar.

Para obtener más información, consulta:

- [Documentación de la integración de Git en Microsoft Fabric](https://learn.microsoft.com/en-us/fabric/cicd/git-integration/intro-to-git-integration?tabs=azure-devops)
- [Entrada del blog sobre la integración de Git entre Tabular Editor y Fabric](https://tabulareditor.com/blog/tabular-editor-and-fabric-git-integration)

## Comparación de formatos de serialización

La integración con Git de Fabric admite ambos formatos de serialización:

- **[TMDL](xref:tmdl)** es un formato de texto legible para humanos. Sus diferencias son más fáciles de revisar en Git.
- **TMSL (.bim)** almacena el modelo en un único archivo JSON, que las herramientas y los flujos de trabajo más antiguos pueden leer.

## Pasos a seguir

- [Guardar en carpeta](xref:save-to-folder)
- [TMDL - Lenguaje de definición de modelos tabulares](xref:tmdl)
