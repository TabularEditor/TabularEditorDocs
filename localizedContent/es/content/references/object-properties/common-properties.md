---
uid: object-properties-common
title: Propiedades comunes
author: Jeroen ter Heerdt
updated: 2026-10-05
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

# Propiedades comunes

<!--
SUMMARY: Properties that most objects in a semantic model share, such as Name, Description, Annotations and Lineage Tag.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

Las propiedades de esta página aparecen en muchos tipos de objetos y funcionan igual en todos los objetos que las tienen. Cada entrada indica el nombre de la propiedad en el Tabular Object Model (TOM), su tipo y su categoría. Las páginas específicas de cada objeto enlazan a estas entradas. Para las demás páginas, consulta @object-properties.

## Básico

### Nombre

`Name` · string · Básico

El nombre del objeto. DAX hace referencia a tablas, columnas, medidas, jerarquías y funciones definidas por el usuario por su nombre. Los nombres deben ser únicos entre elementos del mismo nivel, por lo que dos medidas no pueden compartir un nombre. En la mayoría de los modelos, una medida tampoco puede compartir nombre con ninguna columna (consulta `ForceUniqueNames` en @object-properties-model). Un KPI o un grupo de cálculo no tiene nombre propio y toma su nombre del objeto al que pertenece.

Cuando la **Corrección de fórmulas** está habilitada en **Herramientas > Preferencia**, cambiar el nombre de un objeto actualiza las expresiones DAX que hacen referencia a él. Cuando está deshabilitada, cambiar el nombre rompe las expresiones que usan el nombre anterior. Consulta @formula-fix-up-dependencies.

Para cambiar el nombre de muchos objetos a la vez, selecciónalos en el **Explorador TOM** y usa el renombrado por lotes, que admite expresiones regulares. Consulta @duplicate-and-batch. Las reglas del Best Practice Analyzer (BPA) @kb.bpa-trim-object-names y @kb.bpa-avoid-invalid-characters-names señalan los nombres con espacios al principio o al final, así como los nombres con caracteres de control.

### Descripción

`Description` · string · Básico

Texto libre que explica para qué sirve el objeto. Power BI muestra la descripción como información sobre herramientas en el panel **Datos**. La lista de campos de la tabla dinámica de Excel no muestra descripciones. Para traducir descripciones, usa `TranslatedDescriptions`.

En Tabular Editor 3, el **Explorador TOM** tiene una columna **Descripción** donde puedes leer y editar descripciones, y el Code Assist de DAX muestra en su información sobre herramientas la descripción de una tabla, columna o medida. Cuando una medida, columna calculada o tabla calculada no tiene descripción, la información sobre herramientas muestra las primeras líneas de su expresión.

La regla de BPA @kb.bpa-visible-objects-no-description marca los objetos visibles sin descripción, y @kb.bpa-avoid-invalid-characters-descriptions marca las descripciones que contienen caracteres de control.

### Carpeta de visualización

`DisplayFolder` · string · Básico

La carpeta en la que aparece el objeto, en la lista de campos de las herramientas cliente. Una barra invertida (`\`) crea una subcarpeta, por ejemplo `Sales\Year to date`, y un punto y coma (`;`) muestra el objeto en más de una carpeta, por ejemplo `Sales;Finance`. Las carpetas de visualización no afectan a DAX ni a la seguridad. Tabular Editor también las usa para agrupar objetos en el **Explorador TOM**.

Para mover una carpeta de visualización con sus objetos y subcarpetas, arrástrala a otra carpeta en el **Explorador TOM**. Consulta @drag-drop.

### Oculto

`IsHidden` · bool · Básico

Cuando es `true`, las herramientas cliente como Power BI ocultan el objeto para los autores de Report. El objeto permanece en el modelo y las expresiones DAX pueden seguir haciendo referencia a él. Cualquiera que pueda consultar el modelo también puede consultar un objeto oculto. Para proteger los datos, consulta @roles-and-rls.

La regla de BPA @kb.bpa-hide-foreign-keys marca las columnas visibles del lado de muchos de una relación. Su corrección automática las oculta.

## Metadatos

### Anotaciones

`Annotations` · colección de pares nombre/valor · Metadatos

Pares nombre/valor personalizados almacenados junto con el objeto. Analysis Services y Power BI ignoran las anotaciones, y las herramientas las usan para almacenar su propia información. Por ejemplo, Power BI Desktop almacena información de diseño en las anotaciones, y muchos C# Scripts y reglas de BPA guardan allí su configuración.

En un C# Script, usa `GetAnnotation`, `SetAnnotation` y `RemoveAnnotation`. Consulta @how-to-annotations-extended-properties.

### Propiedades extendidas

`ExtendedProperties` · colección de pares nombre/valor · Metadatos

Pares nombre/valor como las anotaciones, donde el valor es una cadena o un documento JSON. Power BI usa propiedades extendidas, por ejemplo, para almacenar información de consulta sobre los parámetros. Para tus propios metadatos, usa anotaciones.

En un C# Script, usa `GetExtendedProperty` y `SetExtendedProperty`.

### Propiedades modificadas

`ChangedPropertiesCollection` · colección · Metadatos

Los nombres de las propiedades que modificaste en un objeto que viene de otra fuente, como una tabla de un modelo compuesto o un objeto que genera Power BI. Cuando el motor sincroniza el objeto desde su origen, no sobrescribe las propiedades de esta lista.

Tabular Editor 3 no agrega entradas a esta lista. Cuando cambies una propiedad de este tipo, agrega tú mismo su nombre. Escribe una lista de nombres de propiedades TOM separados por comas, por ejemplo `Name,FormatString`, o expande la propiedad y activa la casilla situada junto al nombre de una propiedad. Los duplicados y los nombres que no son propiedades del objeto se ignoran. La lista expandida siempre incluye `Name`, además de las propiedades que ya están en la lista. Para vaciar la lista, haz clic con el botón derecho en la propiedad y selecciona **Borrar propiedades modificadas**.

### Identificador DAX

`DaxObjectFullName` · cadena · Metadatos · solo lectura · _calculado_

El nombre completo que usa DAX para hacer referencia al objeto; por ejemplo, `'Sales'[Amount]` para una columna o `[Total Sales]` para una medida. Los C# Scripts lo usan para crear expresiones DAX. Consulta @how-to-work-with-expressions.

### Mensaje de error

`ErrorMessage` · cadena · Metadatos · solo lectura

El error que el motor notificó para el objeto, por ejemplo, un error de sintaxis en una expresión DAX o un error de actualización en una partición. Está vacío cuando el objeto no tiene ningún error.

En Tabular Editor 3, los errores en las expresiones DAX también aparecen mientras escribes, antes de que el modelo se guarde en el motor. La vista @messages-view muestra todos los mensajes de error y advertencia del modelo. Haz doble clic en un mensaje para ir a su objeto.

### Tipo de objeto

`ObjectTypeName` · string · Metadatos · solo de lectura · _calculado_

El tipo de objeto, por ejemplo `medida`, `columna calculada` o `Table`.

### State

`State` · ObjectState · Metadatos · solo de lectura

Indica si el objeto está listo para consultarse. El motor establece el valor.

| Valor                    | Significado                                                                                                                   |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| `Ready`                  | El objeto es válido y, cuando contiene datos, los datos están actualizados.                                   |
| `NoData`                 | El objeto es válido, pero todavía no contiene datos. Actualiza la tabla o la partición.       |
| `CalculationNeeded`      | El objeto es válido, pero debe recalcularse, por ejemplo, tras cambiar la expresión de una columna calculada. |
| `SemanticError`          | La expresión hace referencia a algo que no existe o no es válido. Consulta `ErrorMessage`.    |
| `EvaluationError`        | La expresión es válida, pero falló al evaluarse.                                                              |
| `DependencyError`        | Un objeto del que depende este se encuentra en estado de error.                                               |
| `Incomplete`             | Faltan algunos datos del objeto, por ejemplo, cuando una partición no se pudo actualizar.                     |
| `ForceCalculationNeeded` | El objeto debe volver a calcularse aunque parezca estar actualizado.                                          |

`State` solo tiene un valor significativo cuando se conecta a un servidor o trabaja en @workspace-mode. Un modelo que abres desde un archivo no está conectado a un motor.

En Tabular Editor 3, puedes actualizar una tabla desde el **Explorador TOM** y seguir el progreso en la @data-refresh-view.

## Opciones

### Etiqueta de linaje

`LineageTag` · cadena · Opciones · nivel de compatibilidad 1540+

Un identificador estable del objeto, normalmente un GUID. Power BI usa las etiquetas de linaje para seguir un objeto a través de cambios de nombre, de modo que un Report o un modelo compuesto que dependa de una columna siga funcionando después de que se cambie el nombre de la columna.

Power BI Desktop asigna etiquetas de linaje automáticamente. No las cambie ni las copie: las herramientas que dependen de las etiquetas de linaje no pueden distinguir entre dos objetos con la misma etiqueta. Cuando Tabular Editor crea un objeto en un modelo que usa etiquetas de linaje, asigna una nueva etiqueta de linaje.

### Etiqueta de linaje de origen

`SourceLineageTag` · cadena · Opciones · nivel de compatibilidad 1550+

La etiqueta de linaje del objeto del que procede este objeto. Los modelos creados sobre otra fuente, como un modelo compuesto o un modelo Direct Lake, la usan para vincular el objeto con la columna o tabla de origen. En Direct Lake, contiene el nombre de la columna o tabla de origen en el Lakehouse o el Warehouse.

Tabular Editor 3 establece `SourceLineageTag` al importar tablas de Direct Lake y en las columnas que agrega al actualizar el esquema de tabla de un modelo Direct Lake. En una tabla, el valor es el esquema y el nombre de la tabla de origen; por ejemplo, `[dbo].[Sales]` o `[Sales]` cuando el origen no usa esquemas. En una columna, el valor es el nombre de la columna de origen.

## Traducciones, perspectivas y seguridad

### Nombres traducidos

`TranslatedNames` · por configuración regional · Traducciones, perspectivas y seguridad

El nombre del objeto en cada configuración regional del modelo. Las herramientas de cliente muestran la traducción que coincide con el idioma del usuario. Cuando una configuración regional no tiene traducción, aparece el nombre sin traducir. Consulta @how-to-work-with-perspectives-translations.

En Tabular Editor 3, @metadata-translation-editor muestra, lado a lado, los nombres, las descripciones y las carpetas de visualización traducidos de muchos objetos. Para intercambiar traducciones con traductores en un archivo JSON, consulta @import-export-translations. La regla de BPA @kb.bpa-translate-visible-names señala los objetos visibles a los que les falta la traducción del nombre.

### Descripciones traducidas

`TranslatedDescriptions` · por configuración regional · traducciones, perspectivas, seguridad

La descripción del objeto en cada configuración regional del modelo. La regla de BPA @kb.bpa-translate-descriptions señala las descripciones a las que les falta traducción.

### Carpetas de visualización traducidas

`TranslatedDisplayFolders` · por configuración regional · traducciones, perspectivas, seguridad

La carpeta de visualización del objeto en cada configuración regional del modelo, con la misma sintaxis de barra invertida y punto y coma que `DisplayFolder`. La regla de BPA @kb.bpa-translate-display-folders señala los objetos visibles a los que les falta la traducción de la carpeta de visualización.

### Sinónimos

`Synonyms` · por configuración regional · traducciones, perspectivas, seguridad

Otras palabras que los usuarios escriben para encontrar el objeto en funciones de lenguaje natural, como Q&A en Power BI. Las tablas, las columnas, las medidas, las jerarquías y los niveles pueden tener sinónimos. Se almacenan en el esquema lingüístico de cada configuración regional (consulta `Content` en @object-properties-perspectives-cultures).

En Tabular Editor 3, la propiedad solo aparece cuando al menos una configuración regional tiene un esquema lingüístico en formato JSON. La propiedad colapsada muestra cuántos esquemas lingüísticos están definidos. Expándela para ver una entrada por configuración regional, con los sinónimos como una lista separada por comas, por ejemplo `revenue, turnover`, y edita la lista para agregar o quitar sinónimos. Un sinónimo eliminado se marca como borrado en el esquema lingüístico. Los sinónimos eliminados y sugeridos no aparecen en la lista.

### Mostrado en la perspectiva

`InPerspective` · por perspectiva · Traducciones, Perspectivas, Seguridad

Indica si el objeto está incluido en cada perspectiva del modelo. Una perspectiva muestra una parte más reducida del modelo a un grupo de usuarios. Al igual que `IsHidden`, las perspectivas no son una función de seguridad.

Cuando seleccionas varios objetos, puedes cambiar de una sola vez su pertenencia a las perspectivas desde la vista de propiedades. Consulta @perspectivas-traducciones. En Tabular Editor 3, el @perspective-editor muestra la pertenencia a las perspectivas de todas las tablas, columnas, jerarquías y medidas en forma de casillas de verificación.
