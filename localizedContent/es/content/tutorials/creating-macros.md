---
uid: creating-macros
title: Creación de macros
author: Morten Lønskov
updated: 2023-12-07
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
      note: "Se denominan Custom Actions"
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

Las macros son C# Scripts que se han guardado en Tabular Editor para reutilizarlos fácilmente en distintos modelos semánticos.
Guardar un script como macro permitirá usar esa macro al hacer clic con el botón derecho en los objetos del Explorador TOM, lo que facilita aplicar el script a tu modelo.

> [!NOTE]
> En Tabular Editor 2, la función para reutilizar C# Scripts se llama @custom-actions.

## Crear una macro

El primer paso para crear una macro es crear y probar un C# Script.

> [!TIP]
> Una forma sencilla de empezar a crear C# Scripts es usar la función integrada de grabación, que te permite grabar las acciones que realizas en el Explorador TOM.
> así puedes ver cómo interactuar con los distintos objetos del modelo y crear scripts reutilizables.
> otra opción es reutilizar scripts existentes, como los de nuestra [biblioteca de scripts](xref:csharp-script-library).
> en este tutorial usamos el script [Format Numeric Measures](xref:script-format-numeric-measures) para mostrar la funcionalidad de las macros.

Cuando el script funcione según lo previsto, puedes guardarlo con el botón de la barra de herramientas "Guardar como macro", que abrirá la ventana "Guardar macro".

![Cuadro de información para crear una macro](~/content/assets/images/features/macros/macro_tutorial_create_infobox.png)

La ventana "Guardar macro" ofrece tres opciones:

1. Nombre de la macro: Ponle un nombre a la macro y usa la barra invertida "\" para crear una ruta de carpetas para la macro (ver más abajo)
2. Añade un tooltip a la macro para recordar en detalle qué hace
3. Selecciona el contexto en el que debe estar disponible la macro.

![Cuadro de diálogo para guardar la macro](~/content/assets/images/features/macros/macro_tutorial_save_window.png)

En el ejemplo anterior, la macro se guardará en una carpeta llamada Formatting\Beginner y el script se llama "Formatear medidas numéricas". Se guardará en el contexto de medidas.

### Contexto de la macro

Las macros se guardan en un "contexto válido" que determina a qué objetos del modelo se puede aplicar el script.

Esta macro se puede usar al hacer clic con el botón derecho sobre una medida en el Explorador TOM. El contexto indicado al guardar la macro determina en qué objetos aparecerá la macro al hacer clic con el botón derecho sobre ellos.

Tabular Editor sugerirá un contexto en función del script que se esté guardando.

![Acceso directo al menú de macros](~/content/assets/images/features/macros/macro_tutorial_menu_shortcut.png)

## Editar una macro

Puedes abrir una macro haciendo doble clic en ella en el panel de macros y, tras editar el C# Script, guardarla con _Ctrl + S_ o con el botón Edit Macro.

![Infocuadro de edición de la macro](~/content/assets/images/features/macros/macro_tutorial_edit_infobox.png)

## Archivo JSON de macros

Las macros se almacenan en %LocalAppFolder%/TabularEditor3 como un archivo JSON llamado MacroActions.json. Para obtener más información sobre los tipos de archivo en Tabular Editor, consulta [Tipos de archivo compatibles](xref:supported-files#macroactionsjson)

## Ejemplo de archivo de macros

Aquí puedes encontrar un ejemplo de archivo MacroActions.json. Contiene varios de los C# Scripts de nuestra biblioteca: [Descargar archivo de ejemplo de MacroActions](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/MacroActions.json)


