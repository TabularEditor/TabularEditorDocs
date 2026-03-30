---
uid: tmdl
title: Lenguaje de definición de modelo tabular (TMDL)
author: Daniel Otykier
updated: 2023-05-22
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

## Habilitar TMDL en Tabular Editor 3

Para habilitar TMDL en Tabular Editor 3, ve a **Herramientas > Preferencias > Formatos de archivo > Guardar en carpeta** y, en el desplegable **Modo de serialización**, selecciona "TMDL". La funcionalidad heredada "save-to-folder" seguirá existiendo en paralelo a TMDL, pero no es un formato admitido por Microsoft.

Después de hacerlo, Tabular Editor 3 usará el formato TMDL al guardar un modelo en una carpeta (**Archivo > Guardar en carpeta...**).

> [!NOTE]
> Cuando cargue un modelo desde una estructura de carpetas heredada de Tabular Editor, se seguirá guardando en ese mismo formato al usar **Archivo > Guardar** (Ctrl+S). Solo cuando uses explícitamente el comando **Archivo > Guardar en carpeta...** se guardará el modelo en el nuevo formato TMDL.

## Modelos nuevos

Al guardar un modelo nuevo por primera vez, Tabular Editor (desde la v. 3.7.0) ahora ofrece una opción para guardar el modelo como TMDL, incluso si el modo de serialización predeterminado no está configurado como TMDL, tal como se describe en la sección anterior.

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

- [Información general de TMDL (Microsoft Learn)](https://learn.microsoft.com/en-us/analysis-services/tmdl/tmdl-overview).
- [Primeros pasos con TMDL (Microsoft Learn)](https://learn.microsoft.com/en-us/analysis-services/tmdl/tmdl-how-to)
