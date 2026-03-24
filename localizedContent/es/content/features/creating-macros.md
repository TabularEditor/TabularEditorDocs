---
uid: macros
title: Creación de macros
author: Morten Lønskov
updated: 2023-12-07
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

# (Tutorial) Creación de macros

Las macros son scripts de C# que se han guardado en Tabular Editor para poder reutilizarlas fácilmente en distintos modelos semánticos.
Guardar un script como macro permite usar esa macro al hacer clic con el botón derecho en los objetos del Explorador TOM, lo que facilita aplicar el script a tu modelo.

## Crear una macro

El primer paso para crear una macro es crear y probar un C# Script.

> [!TIP]
> Una forma sencilla de empezar con el scripting de C# es usar la función de grabación integrada, que le permite registrar las acciones que realiza en el Explorador TOM.
> De esta manera puede ver cómo interactuar con los distintos objetos del modelo y crear scripts reutilizables.
> Otra forma es reutilizar scripts existentes, como los de nuestra [biblioteca de scripts](xref:csharp-script-library).
> En este tutorial usamos el script [Format Numeric Measures](xref:script-format-numeric-measures) para mostrar la funcionalidad de las macros.

Cuando el script funcione según los requisitos, se puede guardar con el botón de la barra de herramientas "Guardar como macro", que abrirá la ventana "Guardar macro".

![Cuadro de información: crear macro](~/content/assets/images/features/macros/macro_tutorial_create_infobox.png)

La ventana "Guardar macro" ofrece tres opciones:

1. Nombre de la macro: Asigna un nombre a la macro y utiliza la barra invertida "\" para crear la ruta de carpetas de la macro (ver más abajo)
2. Proporciona un texto de información sobre herramientas para la macro, para recordar en detalle lo que hace
3. Selecciona un contexto en el que la macro deba estar disponible.

![Cuadro de información: guardar macro](~/content/assets/images/features/macros/macro_tutorial_save_window.png)

En el ejemplo anterior, la macro se guardará en una carpeta llamada Formatting\Beginner y el script se llama "Formatear medidas numéricas". Se guardará en el contexto de las medidas.

### Contexto de la macro

Las macros se guardan en un "contexto válido" que determina a qué objetos del modelo se puede aplicar el script.

Esta macro se puede usar al hacer clic con el botón derecho sobre una medida en el Explorador TOM. El contexto indicado al guardar la macro determina en qué objetos aparecerá la macro al hacer clic con el botón derecho.

Tabular Editor sugerirá un contexto en función del script que se esté guardando.

![Acceso directo del menú de macros](~/content/assets/images/features/macros/macro_tutorial_menu_shortcut.png)

## Editar una macro

Una macro puede abrirse haciendo doble clic en ella en el panel de macros y, tras editar el C# Script, guardarse con _Ctrl + S_ o mediante el botón Editar macro.

![Cuadro de información de edición de macro](~/content/assets/images/features/macros/macro_tutorial_edit_infobox.png)

## Archivo JSON de macros

Las macros se almacenan en %LocalAppFolder%/TabularEditor3 como un archivo JSON llamado MacroActions.json. Para obtener más información sobre los tipos de archivo en Tabular Editor, consulte [Tipos de archivo compatibles](xref:supported-files#macroactionsjson)

## Ejemplo de archivo de macros

Aquí se puede encontrar un ejemplo de un archivo MacroActions.json. Contiene varios C# Scripts de nuestra biblioteca de scripts: [Descargar archivo MacroActions.json de ejemplo](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/MacroActions.json)


