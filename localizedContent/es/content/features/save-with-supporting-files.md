---
uid: save-with-supporting-files
title: Guardar con archivos de apoyo
author: Peer Grønnerup
updated: 2026-01-19
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

Guardar con archivos de apoyo es una característica que permite guardar modelos semánticos con archivos de apoyo adicionales, siguiendo el formato de código fuente requerido para la integración con Git en Microsoft Fabric. Esta característica garantiza que sus modelos de Tabular Editor sean totalmente compatibles con las capacidades de integración con Git de Fabric, lo que permite flujos de trabajo de control de versiones e implementación sin fricciones.

Cuando guarda un modelo semántico con archivos de apoyo, Tabular Editor crea una estructura de carpetas que incluye todos los archivos de metadatos necesarios para la integración con Git de Microsoft Fabric. Esto le permite usar la integración con Git de Fabric para sincronizar sus modelos semánticos entre los espacios de trabajo de Fabric y los repositorios de Git.

> [!NOTE]
> Guardar con archivos de apoyo solo está disponible al guardar en .bim (TMSL) o cuando Guardar en carpeta se configura con TMDL como modo de serialización.

## Estructura de archivos y propiedades del modelo

Cuando guarda con archivos de apoyo, Tabular Editor crea una nueva carpeta en la ruta de guardado siguiendo la siguiente convención de nombres: **Database Name.SemanticModel**. El nombre de la carpeta se deriva de la propiedad `Name` del objeto Database en el Explorador TOM, a la que se añade el sufijo **.SemanticModel**. Microsoft Fabric necesita este sufijo para reconocer la carpeta como un elemento de modelo semántico.

La propiedad `Name` de Database también se sincroniza con la propiedad `displayName` en el archivo de metadatos .platform, que utiliza Microsoft Fabric.

> [!TIP]
> La propiedad `Name` del objeto Database en el Explorador TOM cumple dos objetivos:
>
> 1. Determina el nombre de la carpeta (con el sufijo .SemanticModel añadido)
> 2. Establece el valor de displayName en el archivo de metadatos .platform
>
> La propiedad `Description` también se sincroniza con el archivo de metadatos .platform.

### Archivos incluidos

Todos los modelos guardados incluyen estos archivos principales:

- **.platform**: metadatos sobre el elemento, incluidos su tipo, nombre para mostrar y descripción. También contiene la propiedad logicalId, un identificador entre áreas de trabajo generado automáticamente.
- **definition.pbism**: definición general y configuración principal del modelo semántico.

La estructura de archivos del modelo dentro de la carpeta creada depende de su formato de serialización:

| Formato                                            | Almacenamiento del modelo                                                                        |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| **TMDL**                                           | Carpeta `definition` que contiene archivos TMDL con los metadatos del modelo                     |
| **TMSL (.bim)** | Archivo `model.bim` (se guarda automáticamente con un nombre de archivo fijo) |

Ejemplo de estructura de carpetas para una base de datos llamada "Sales":

```
Sales.SemanticModel/
├── .platform
├── definition.pbism
├── model.bim                    (si se guarda como TMSL)
└── definition/                  (si se guarda como TMDL)
    ├── database.tmdl
    ├── tables.tmdl
    └── ...
```

## Cómo guardar con archivos auxiliares

Para guardar su modelo con archivos de apoyo:

1. Cree un modelo semántico nuevo o abra uno existente en Tabular Editor 3
2. **Configure el nombre del modelo** - Establezca la propiedad `Name` del objeto Database en el Explorador TOM
   - Esto establece el nombre de la carpeta (con el sufijo .SemanticModel) y el displayName en el archivo .platform  
     ![Establecer la propiedad Nombre de base de datos](~/content/assets/images/common/SaveWithSupportingFilesSetName.png)
3. Asegúrese de configurar el modo de serialización en TMDL o de guardar como un archivo .bim
   - Vaya a **Herramientas > Preferencias > Formatos de archivo** para configurar las opciones de serialización
4. Haga clic en **Archivo > Guardar como** o **Archivo > Guardar en carpeta**
5. Elija una carpeta donde quiera guardar su modelo
   - Marque la casilla **Guardar con archivos de apoyo**
     ![Cuadro de diálogo Guardar con archivos de apoyo](~/content/assets/images/common/SaveWithSupportingFilesDialog.png)
6. Haga clic en **Guardar**

Tabular Editor creará una nueva carpeta usando el nombre de la base de datos con el sufijo **.SemanticModel** (por ejemplo, `Sales.SemanticModel`) en la ubicación de guardado y la rellenará con todos los archivos necesarios en un formato compatible con la integración de Git de Microsoft Fabric.

## Integración de Git en Microsoft Fabric

La característica **Guardar con archivos auxiliares** está diseñada para funcionar de forma fluida con las capacidades de integración de Git de Microsoft Fabric. La integración de Git está disponible en los Workspaces asignados a la capacidad Microsoft Fabric F-SKU, a la capacidad Power BI Premium o a Power BI Premium Per User (PPU).

> [!WARNING]
> La integración de Git para el elemento de modelo semántico se encuentra actualmente en versión preliminar. Para obtener la información más reciente sobre los elementos compatibles con la integración de Git de Fabric, consulte [Elementos compatibles en la integración de Git de Fabric](https://learn.microsoft.com/en-us/fabric/cicd/git-integration/intro-to-git-integration#supported-items).

> [!CAUTION]
> **No** habilite la integración de Git en el Workspace de Fabric que utiliza para hospedar las bases de datos del Workspace de Tabular Editor.
> Mantener modelos semánticos tanto en el Workspace hospedado como en los archivos del repositorio a la vez, con la integración de Git habilitada, crea riesgos de cambios sin confirmar y conflictos. Cuando un modelo se sincroniza entre Tabular Editor y el Workspace, es posible que los cambios no se alineen correctamente con el estado del repositorio de Git, lo que puede dejar cambios sin confirmar fuera de sincronización y provocar posibles conflictos de Git.
>
> En su lugar, utilice flujos de trabajo de implementación para desplegar modelos semánticos en Workspaces mediante Tabular Editor, las API REST de Fabric, Fabric CLI o la biblioteca de Python fabric-cicd. Esto garantiza una separación clara entre su repositorio de Git y el Workspace.

### Uso de la integración de Git con Tabular Editor

Cuando su modelo semántico se guarda con archivos auxiliares y se sincroniza con su repositorio de Git, puede sincronizarlo con Microsoft Fabric mediante el siguiente flujo de trabajo:

1. **Guarda tu modelo** en Tabular Editor con la opción Guardar con archivos de soporte
2. **Haz commit de los cambios** en tu repositorio de Git
3. **Conecta tu Workspace de Fabric** al repositorio de Git
4. **Sincroniza** tu modelo entre Fabric y Git con el botón **Actualizar todo** en el panel de control de código fuente del Workspace
   ![Sincronizar Workspace con Git](~/content/assets/images/common/WorkspaceGitSync.png)

Cuando tu modelo se sincroniza con Microsoft Fabric/Power BI, el nombre del modelo semántico que se muestra en el Workspace se basa en la propiedad `displayName` del archivo .platform, que se establece automáticamente a partir de la propiedad `Name` de la base de datos en Tabular Editor. Esto significa que el nombre que configures en Tabular Editor será el que se muestre en Fabric/Power BI.

Tabular Editor establece automáticamente la configuración regional del modelo en **en-US** al guardar con archivos de soporte. Esto garantiza que la configuración regional del modelo esté presente al sincronizar con Fabric, evitando cambios sin confirmar que pueden producirse si la configuración regional no se establece durante la sincronización inicial.

Para obtener más información, consulta:

- [Documentación de la integración de Git en Microsoft Fabric](https://learn.microsoft.com/en-us/fabric/cicd/git-integration/intro-to-git-integration?tabs=azure-devops)
- [Entrada del blog sobre la integración de Git entre Tabular Editor y Fabric](https://tabulareditor.com/blog/tabular-editor-and-fabric-git-integration)

## Comparación de formatos de serialización

Al usar Guardar con archivos de soporte, puedes elegir entre dos formatos de serialización:

### TMDL (Tabular Model Definition Language)

- Formato de texto legible
- Más fácil revisar los cambios en los diffs de Git
- Mejor para revisiones de código y colaboración
- Más información: [Documentación de TMDL](tmdl.md)

### TMSL/JSON (.bim)

- Formato basado en JSON
- Representación en un único archivo
- Compatible con herramientas y flujos de trabajo más antiguos

Ambos formatos son compatibles con la integración de Git de Microsoft Fabric, y la elección depende de las preferencias de tu equipo y de los requisitos del flujo de trabajo.

## Ver también

- [Guardar en carpeta](save-to-folder.md)
- [TMDL - lenguaje de definición de modelos tabulares](tmdl.md)
