---
uid: find-replace
title: Buscar/Reemplazar
author: Morten Lønskov
updated: 2023-03-22
applies_to:
  products:
    - product: Tabular Editor 2
      partial: true
      note: "Funciona de forma distinta a como se muestra en este artículo"
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

<a name="find"></a>

# Buscar

En Tabular Editor, puede utilizar la funcionalidad avanzada de búsqueda para buscar expresiones específicas en todos los documentos abiertos y en el Dataset. Se puede acceder al cuadro de diálogo Buscar mediante el atajo de teclado Ctrl+F.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/user-interface/find-dialog.png" alt="Find Dialog Box" style="width: 300px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 3:</strong> Ventana de Reemplazar en Tabular Editor. Ctrl+F abre el cuadro de diálogo </figcaption>
</figure>

Para realizar una búsqueda, defina la expresión que desea buscar y utilice las Opciones para determinar si deben cumplirse determinados criterios. Por ejemplo, puede elegir si debe coincidir el uso de mayúsculas y minúsculas entre la expresión de búsqueda y el texto encontrado, o utilizar expresiones regulares.

## Buscar en

Además, puede especificar dónde buscar, en distintas áreas de su instancia de Tabular Editor, para limitar o ampliar el alcance de la búsqueda. Las opciones de Buscar en incluyen:

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/user-interface/find-dialog-look-in.png" alt="Find and Replace Dialog Box" style="width: 200px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 2:</strong> Ventana "Buscar/Reemplazar" en Tabular Editor. Ctrl+F abre el cuadro de diálogo. </figcaption>
</figure>

- _Selección_: Buscar dentro de la selección en el documento abierto actualmente (No se puede buscar en el Dataset)
- _Documento actual_: Buscar en todo el documento que tiene abierto (No se puede buscar en el Dataset)
- _Todos los documentos abiertos_: Buscar en todos los documentos abiertos (No se puede buscar en el Dataset)
- _Modelo completo_: Busca en el Explorador TOM coincidencias en el Dataset.
  - Permite buscar dentro de las partes individuales de su Dataset, como Nombres, Expresiones, Anotaciones, etc.
  - En este modo también puedes buscar con Dynamic LINQ para, por ejemplo, encontrar todas las columnas que no tengan summarize configurado en none.

> [!TIP]
> También puedes usar el campo de búsqueda del Explorador TOM para buscar en el Dataset en lugar del cuadro de diálogo Buscar

<a name="replace"></a>

## Reemplazar

El cuadro de diálogo Reemplazar le permite, al igual que Buscar, buscar una expresión y después reemplazarla por otra distinta.

El cuadro de diálogo Reemplazar no requiere nada en el campo _Reemplazar con_, pero si lo deja vacío, reemplazará la expresión buscada por una expresión vacía.
Tiene las mismas opciones que en el cuadro de diálogo Buscar para definir los criterios de búsqueda, pero la función _Buscar en_ solo está disponible para documentos; es decir, no puede buscar y reemplazar dentro de los objetos de su Dataset.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/user-interface/find-dialog.png" alt="Replace Dialog Box" style="width: 300px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 3:</strong> Ventana de Reemplazar en Tabular Editor. Ctrl+F abre el cuadro de diálogo. </figcaption>
</figure>

> [!TIP]
> Si está intentando cambiar el nombre de variables en una instrucción DAX (Expresión o Script), Ctrl+R le permitirá refactorizar una variable seleccionada