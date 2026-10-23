---
uid: advanced-filtering-explorer-tree
title: Filtrado avanzado de objetos
author: Morten Lønskov
updated: 2026-09-23
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      partial: true
---

# Filtrado avanzado de objetos

El cuadro de texto **Filtro** del árbol del explorador filtra los objetos que se muestran en el árbol por nombre, por patrón de comodines o por una expresión Dynamic LINQ.

## Modo de filtrado

Los tres botones de la barra de herramientas situados más a la derecha, junto al botón **Filtro**, añadidos en [Tabular Editor 2.7.4](https://github.com/TabularEditor/TabularEditor/releases/tag/2.7.4), determinan cómo se aplica el filtro a la jerarquía de objetos y cómo se muestran los resultados.

![Cuadro de texto de filtro y botones de modo de filtro en la barra de herramientas del Explorador](~/content/assets/images/advanced-filtering-of-the-explorer-tree-01.png)

* ![Botón Jerárquico por elemento principal](~/content/assets/images/advanced-filtering-of-the-explorer-tree-02.png) **Jerárquico por elemento principal**: la búsqueda se aplica a los objetos principales, es decir, a las tablas, y muestra las carpetas si están visibles. Cuando un elemento principal coincide, se muestran todos sus elementos secundarios.
* ![Botón Jerárquico por elementos secundarios](~/content/assets/images/advanced-filtering-of-the-explorer-tree-03.png) **Jerárquico por elementos secundarios**: la búsqueda se aplica a los objetos secundarios, como medidas, columnas y jerarquías. Un elemento principal solo se muestra si al menos uno de sus elementos secundarios coincide.
* ![Botón «Plano»](~/content/assets/images/advanced-filtering-of-the-explorer-tree-04.png) **Plano**: la búsqueda se aplica a todos los objetos y los resultados se muestran como una lista plana. Los objetos con elementos secundarios siguen mostrándolos de forma jerárquica.

## Búsqueda simple

Escriba texto en el cuadro de texto **Filtro** y pulse **Intro** para realizar una búsqueda de nombres de objetos sin distinguir entre mayúsculas y minúsculas. Por ejemplo, «ventas» en el modo «Por elemento principal» da estos resultados:

![Resultados de la búsqueda de «sales» en el modo «Por elemento principal»](~/content/assets/images/advanced-filtering-of-the-explorer-tree-05.png)

Al expandir una tabla se muestran todas sus medidas, columnas, jerarquías y particiones. En el modo «Por elemento secundario», la misma búsqueda da estos resultados:

![Resultados de la búsqueda de «sales» en el modo «Por elemento secundario»](~/content/assets/images/advanced-filtering-of-the-explorer-tree-06.png)

Ahora aparece la tabla «Empleado», porque algunas de sus columnas contienen la palabra «ventas».

## Búsqueda con comodines

En el cuadro de texto **Filtro**, `?` coincide con cualquier carácter individual y `*` coincide con cualquier secuencia de cero o más caracteres, y la coincidencia no distingue entre mayúsculas y minúsculas, como en la búsqueda simple. `*sales*` da los mismos resultados que los anteriores, y `sales*` muestra solo los objetos cuyos nombres comienzan por «sales».

Una búsqueda de «sales*» en el modo «Por elemento principal» da estos resultados:

![Resultados de la búsqueda de sales* en el modo «Por elemento principal»](~/content/assets/images/advanced-filtering-of-the-explorer-tree-07.png)

La misma búsqueda en el modo «Por elemento secundario» da estos resultados:

![Resultados de la búsqueda de sales* en el modo «Por elemento secundario»](~/content/assets/images/advanced-filtering-of-the-explorer-tree-08.png)

Búsqueda plana de «sales*», con las columnas de información mostradas (**Ctrl+F1**) para obtener detalles sobre cada objeto:

![Resultados de la búsqueda plana para sales* con columnas de información que muestran el elemento principal y el tipo](~/content/assets/images/advanced-filtering-of-the-explorer-tree-09.png)

Puede colocar cualquier número de comodines en cualquier parte de la cadena.

## Búsqueda Dynamic LINQ

El filtro también acepta expresiones [Dynamic LINQ](https://github.com/kahanu/System.Linq.Dynamic/wiki/Dynamic-Expressions), la sintaxis que utilizan las [reglas del Best Practice Analyzer](xref:best-practice-analyzer). Inicie la cadena de búsqueda con «:`» (dos puntos) para cambiar al modo Dynamic LINQ. Por ejemplo, este filtro muestra todos los objetos cuyo nombre termina en «Key» (distingue entre mayúsculas y minúsculas):

```text
:Name.EndsWith("Key")
```

Pulse **Intro** para aplicar el filtro, que en el modo «Plano» da este resultado:

![Resultados en modo plano para un filtro Dynamic LINQ sobre nombres que terminan en «Key»](~/content/assets/images/advanced-filtering-of-the-explorer-tree-10.png)

Para realizar una búsqueda sin distinguir entre mayúsculas y minúsculas en Dynamic LINQ, convierta la cadena:

```text
:Name.ToUpper().EndsWith("KEY")
```

o bien puede proporcionar el argumento [StringComparison](https://docs.microsoft.com/dotnet/api/system.string.endswith?view=netframework-4.7.2#System_String_EndsWith_System_String_System_StringComparison_), como:

```text
:Name.EndsWith("Key", StringComparison.InvariantCultureIgnoreCase)
```

Un filtro Dynamic LINQ puede evaluar cualquier propiedad de un objeto, incluidas las subpropiedades. Por ejemplo, este filtro busca todos los objetos cuya expresión contenga la palabra «TODO»:

```text
:Expression.ToUpper().Contains("TODO")
```

Este filtro muestra todas las medidas ocultas del modelo a las que no hace referencia ningún otro objeto:

```text
:ObjectType="Measure" and (IsHidden or Table.IsHidden) and ReferencedBy.Count=0
```

Las expresiones regulares también funcionan, como en este filtro que busca todas las columnas cuyo nombre contiene «Número» o «Importe»:

```text
:ObjectType="Column" and RegEx.IsMatch(Name,"(Number)|(Amount)")
```

En los modos «Por elemento principal» y «Por elemento secundario», las opciones de visualización y los botones de la barra de herramientas situados justo encima del árbol también filtran los resultados. Por ejemplo, el filtro anterior solo devuelve columnas, por lo que, si las opciones de visualización ocultan las columnas, el árbol no muestra nada.
