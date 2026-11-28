---
uid: tmdl
title: Lenguaje de definición de modelo tabular (TMDL)
author: Daniel Otykier
updated: 2026-11-12
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Lenguaje de definición de modelo tabular (TMDL)

**TMDL** es un formato de archivo de metadatos de modelo [anunciado por Microsoft en abril de 2023](https://powerbi.microsoft.com/en-us/blog/announcing-public-preview-of-the-tabular-model-definition-language-tmdl/). Su objetivo es ofrecer una alternativa basada en texto y legible para humanos al formato de archivo model.bim basado en JSON. TMDL se inspira en YAML y, por eso, es fácil de leer y escribir, con un uso mínimo de comillas en las cadenas y caracteres de escape. También serializa un modelo como varios archivos más pequeños en una estructura de carpetas y, por tanto, es más adecuado para la integración con el control de versiones.

## Guardar un modelo como TMDL en Tabular Editor 3

**Archivo > Guardar en carpeta...** guarda el modelo como una carpeta TMDL cuando **Guardar en formato de carpeta** en **Herramientas > Preferencias > Formatos de archivo > Guardar en carpeta** es **TMDL**, el valor predeterminado. La configuración de formato de TMDL, como la sangría, la codificación y las mayúsculas y minúsculas, se encuentra en **Herramientas > Preferencias > Formatos de archivo > Guardar en carpeta > Serialización de TMDL**. Consulte [Preferencias](xref:preferences#file-formats--save-to-folder--tmdl-serialization).

> [!NOTE]
> Un modelo cargado desde una carpeta Database.json se guarda en ese formato cuando se utiliza **Archivo > Guardar** (**Ctrl+S**). Use **Archivo > Guardar en carpeta...** con **Formato de guardar en carpeta** establecido en **TMDL** para convertirlo a TMDL.

En Tabular Editor 3 Edición Enterprise, una carpeta TMDL puede almacenar cada columna, medida, partición y jerarquía, así como cada función, expresión compartida, origen de datos y relación, en su propio archivo. Consulta @tmdl-per-object-serialization.

## Modelos nuevos

La configuración **Formato de guardado predeterminado** en **Herramientas > Preferencias > Formatos de archivo > General** controla cómo se guarda un nuevo modelo la primera vez. Con **Preguntar siempre** (opción predeterminada), Tabular Editor le pedirá que elija entre un archivo Model.bim y una carpeta en formato Database.json o TMDL. Con **TMDL**, los nuevos modelos se guardan como carpetas TMDL.

![Nuevo modelo Tmdl](~/content/assets/images/new-model-tmdl.png)

## TMDL y la integración con Git de Microsoft Fabric

TMDL es totalmente compatible con la característica de integración con Git de Microsoft Fabric. Al usar la opción **Guardar con archivos de apoyo** en Tabular Editor 3, el formato de serialización TMDL crea una estructura de carpetas que incluye todos los archivos de metadatos necesarios para la integración con Git de Microsoft Fabric.

La estructura de carpetas resultante incluye:

- Archivo **.platform** con metadatos (nombre para mostrar, descripción, ID lógico)
- Archivo **definition.pbism** con la configuración del modelo semántico
- carpeta **definition/** que contiene los archivos del modelo TMDL

Esta combinación te permite hacer commit de tus modelos semánticos en repositorios Git y sincronizarlos con los Workspaces de Microsoft Fabric mediante las capacidades de integración de Git integradas en Fabric. La naturaleza legible de TMDL lo hace especialmente adecuado para las revisiones de código y el seguimiento de cambios en sistemas de control de versiones.

Para obtener información detallada sobre cómo usar esta característica, consulta [Guardar con archivos auxiliares](xref:save-with-supporting-files).

# Siguientes pasos

- [Información general de TMDL (Microsoft Learn)](https://learn.microsoft.com/analysis-services/tmdl/tmdl-overview).
- [Primeros pasos con TMDL (Microsoft Learn)](https://learn.microsoft.com/analysis-services/tmdl/tmdl-how-to)
