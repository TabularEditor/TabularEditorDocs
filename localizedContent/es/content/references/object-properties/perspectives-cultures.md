---
uid: object-properties-perspectives-cultures
title: Propiedades de las perspectivas y configuraciones regionales
author: Jeroen ter Heerdt
updated: 2026-10-09
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Propiedades de las perspectivas y configuraciones regionales

<!--
SUMMARY: Reference for the properties of perspectives and cultures (translations), including linguistic metadata and translation statistics.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

En esta página se describen las propiedades de las perspectivas y las configuraciones regionales. Para ver las propiedades que comparten la mayoría de los objetos, consulta @object-properties-common.

Para agregar o quitar perspectivas y configuraciones regionales, usa las colecciones **Perspectivas** y **Configuraciones regionales** del modelo (consulta @object-properties-model), o haz clic con el botón derecho en la carpeta **Perspectivas** o **Traducciones** del **Explorador TOM**. Tabular Editor 2 usa los mismos nombres de carpeta. Consulta @perspectivas-traducciones. Para crear y cambiar perspectivas y configuraciones regionales mediante un C# Script, consulta @how-to-work-with-perspectives-translations.

## Perspectiva

Una perspectiva es un subconjunto con nombre del modelo: una selección de tablas, columnas, medidas y jerarquías para un grupo de usuarios. Por ejemplo, una perspectiva `Sales` muestra solo los objetos que necesita el equipo de ventas. En las herramientas cliente que admiten perspectivas, como Excel, los usuarios eligen una perspectiva y solo ven los objetos que contiene. Los autores de Report de Power BI no pueden elegir una perspectiva en la lista de campos, pero puedes usar una al conectarte al modelo a través del punto de conexión XMLA o en un Visual personalizado.

En el servicio de Power BI, te conectas a una perspectiva a través del punto de conexión XMLA agregando `Cube=<perspective name>` a la cadena de conexión. Eso solo cambia qué objetos enumera la información del esquema; las consultas DAX pueden seguir usando todas las tablas y medidas del modelo.

<!-- TODO (not verifiable from TE3 source): whether personalized visuals in the Power BI service still use perspectives. -->

> [!NOTE]
> Las perspectivas no restringen el acceso. Un usuario puede consultar cualquier objeto del modelo, independientemente de la perspectiva que utilice. Para restringir el acceso, usa @roles-and-rls.

Una perspectiva no tiene propiedades propias, aparte de las comunes. Eliges qué objetos contiene la perspectiva en los propios objetos, con `InPerspective` (consulta [Mostrado en perspectiva](xref:object-properties-common#shown-in-perspective)) o, en Tabular Editor 3, para muchos objetos a la vez, en el @perspective-editor.

La regla del Best Practice Analyzer (BPA) @kb.bpa-perspectives-no-objects marca las perspectivas que no contienen tablas, y @kb.bpa-translate-perspectives marca las perspectivas cuyo nombre no está traducido en todas las configuraciones regionales.

### Propiedades comunes

- [Nombre](xref:object-properties-common#name)
- [Descripción](xref:object-properties-common#description)
- [Anotaciones](xref:object-properties-common#annotations)
- [Propiedades extendidas](xref:object-properties-common#extended-properties)
- [Tipo de objeto](xref:object-properties-common#object-type)
- [Nombres traducidos](xref:object-properties-common#translated-names)
- [Descripciones traducidas](xref:object-properties-common#translated-descriptions)

## Configuración regional

Una configuración regional contiene las traducciones del modelo para un idioma: los nombres traducidos, las descripciones traducidas y las carpetas de visualización traducidas de sus objetos, así como los metadatos lingüísticos de ese idioma. Las herramientas cliente muestran la configuración regional que coincide con la configuración de idioma del usuario y, cuando no hay ninguna que coincida, los nombres sin traducir.

El `Name` de una configuración regional es el código de la configuración regional, por ejemplo `da-DK` o `fr-FR`. Debe ser un nombre de configuración regional válido, y cada configuración regional solo puede aparecer una vez en el modelo. En Tabular Editor 3, la vista **Propiedades** lo etiqueta como **Idioma** y muestra una lista de configuraciones regionales para elegir.

Las traducciones se editan en cada objeto, con `TranslatedNames`, `TranslatedDescriptions` y `TranslatedDisplayFolders`, o, en Tabular Editor 3, para muchos objetos a la vez en @metadata-translation-editor. Para intercambiar traducciones con traductores, consulta @import-export-translations.

Las propiedades de estadísticas de traducción muestran qué parte del modelo está traducida en esta configuración regional, para cada tipo de objeto. Tabular Editor las calcula y no se almacenan en el modelo. Cada valor tiene el formato `12 of 40`: el número de traducciones sobre el total de objetos de ese tipo en el modelo, incluidos los objetos ocultos. En el caso de los nombres, una traducción solo cuenta si no está vacía y es distinta del nombre sin traducir del objeto. Para encontrar los objetos a los que les falta una traducción, usa las reglas de BPA @kb.bpa-translate-visible-names, @kb.bpa-translate-descriptions y @kb.bpa-translate-display-folders.

### Propiedades comunes

- [Nombre](xref:object-properties-common#name)
- [Anotaciones](xref:object-properties-common#annotations)
- [Propiedades extendidas](xref:object-properties-common#extended-properties)
- [Tipo de objeto](xref:object-properties-common#object-type)

### Altered

`Altered` · bool (vacío cuando hay valores mixtos) · Básico · nivel de compatibilidad 1571+ · _acceso directo al_ indicador **Altered** de cada traducción de la configuración regional

Cada traducción de una configuración regional lleva un indicador _altered_ en el Tabular Object Model (TOM), que las herramientas de traducción utilizan para marcar las traducciones que una persona ha revisado o modificado. Esta propiedad resume los indicadores de todas las traducciones de la configuración regional:

- `true`: todas las traducciones tienen el indicador activado
- `false`: ninguna traducción tiene el indicador activado
- vacío: algunas traducciones lo tienen y otras no

Establece `true` o `false` para activar o desactivar el indicador en todas las traducciones de la configuración regional a la vez. La vista de **Propiedades** muestra esta propiedad en el nivel de compatibilidad 1571 o superior.

> [!WARNING]
> No puedes deshacer un cambio en la propiedad `Altered`.

El indicador no se guarda en los archivos del modelo. La biblioteca TOM de Microsoft no lo escribe en Tabular Model Scripting Language (TMSL), que abarca los archivos `.bim`, las carpetas en formato JSON y los scripts de implementación, ni en Tabular Model Definition Language (TMDL). El indicador se pierde cuando guardas el modelo en un archivo y lo vuelves a abrir.

Cuando estableces la marca mediante una conexión activa a un servidor, el servidor la conserva. En SQL Server 2025 Analysis Services, se mantiene tras una reconexión y aparece en la DMV `TMSCHEMA_OBJECT_TRANSLATIONS` de traducciones. Un script TMSL generado desde ese servidor sigue sin incluirlo, así que el indicador se pierde en cuanto el modelo se guarda en un archivo o se implementa desde uno.

<!-- TODO (not verifiable from TE3 source): confirm which tools set and read the Altered flag. -->

### Contenido

`Content` · string · Metadatos lingüísticos · nivel de compatibilidad 1465+

El esquema lingüístico de la configuración regional: los metadatos en lenguaje natural que usaba Power BI Q&A antes de que se retirara. Contiene los sinónimos de tablas, columnas y medidas, y formulaciones que describen cómo se relacionan los objetos; por ejemplo, que los clientes compran productos. La propiedad `Synonyms` de cada objeto lee y escribe los sinónimos almacenados aquí.

El contenido es un documento JSON o XML de gran tamaño, según `ContentType`, y Power BI Desktop lo mantiene. La vista **Propiedades** muestra esta propiedad a partir del nivel de compatibilidad 1465.

En Tabular Editor 3, seleccione **...** en la propiedad para editar el contenido en un editor de texto de varias líneas. Tabular Editor no valida el documento y establece `ContentType` en función del primer carácter: el contenido que comienza con `{` es JSON; cualquier otra cosa es XML. Al borrar el contenido se eliminan los metadatos lingüísticos de la configuración regional. Tabular Editor solo lee y escribe `Synonyms` desde contenido JSON.

### Tipo de contenido

`ContentType` · ContentType · Metadatos lingüísticos · solo lectura · nivel de compatibilidad 1465+

El formato de `Content`: `Json` para modelos creados por Power BI o `Xml` para el formato anterior. Está vacío cuando la configuración regional no tiene metadatos lingüísticos. Tabular Editor lo establece cuando edita `Content`. La vista **Propiedades** muestra esta propiedad a partir del nivel de compatibilidad 1465.

### Nombres de tablas traducidos

`StatsTableCaptions` · cadena · Estadísticas de traducción · solo lectura · _calculado_

Cuántos nombres de tablas están traducidos.

### Nombres de columnas traducidos

`StatsColumnCaptions` · cadena · Estadísticas de traducción · solo lectura · _calculado_

Cuántos nombres de columnas están traducidos.

### Carpetas de visualización de columnas traducidas

`StatsColumnDisplayFolders` · cadena · Estadísticas de traducción · solo lectura · _calculado_

Cuántas carpetas de visualización de columnas están traducidas. El total es el número de columnas del modelo, incluidas las columnas que no tienen carpeta de visualización, por lo que el primer número suele ser menor que el segundo, incluso cuando todas las carpetas de visualización están traducidas.

### Nombres de medidas traducidos

`StatsMeasureCaptions` · cadena · Estadísticas de traducción de medidas · solo lectura · _calculado_

Cuántos nombres de medidas están traducidos.

### Carpetas de visualización de medidas traducidas

`StatsMeasureDisplayFolders` · string · Estadísticas de traducción de medidas · solo lectura · _calculado_

Número de carpetas de visualización de medidas traducidas. El total es el número de medidas del modelo, incluidas las medidas que no tienen carpeta de visualización.

### Nombres de jerarquías traducidos

`StatsHierarchyCaptions` · string · Estadísticas de traducción · solo lectura · _calculado_

Número de nombres de jerarquía traducidos.

### Carpetas de visualización de jerarquías traducidas

`StatsHierarchyDisplayFolders` · string · Estadísticas de traducción · solo lectura · _calculado_

Número de carpetas de visualización de jerarquías traducidas. El total es el número de jerarquías del modelo, incluidas las jerarquías que no tienen carpeta de visualización.

### Nombres de niveles traducidos

`StatsLevelCaptions` · string · Estadísticas de traducción · solo lectura · _calculado_

Número de nombres de nivel de jerarquía traducidos. La regla BPA @kb.bpa-translate-hierarchy-levels señala los niveles de las jerarquías visibles que no tienen un nombre traducido.
