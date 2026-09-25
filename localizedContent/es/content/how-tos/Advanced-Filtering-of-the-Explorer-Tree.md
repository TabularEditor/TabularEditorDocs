---
uid: advanced-filtering-explorer-tree
title: Filtrado avanzado de objetos
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      partial: true
---

# Filtrado avanzado de objetos

Este artículo explica cómo usar el cuadro de texto "Filter" en Tabular Editor, una función increíblemente útil para navegar por modelos complejos.

## Modo de filtrado

Desde la versión [2.7.4](https://github.com/TabularEditor/TabularEditor/releases/tag/2.7.4), Tabular Editor te permite decidir cómo se aplica el filtro a los objetos de la jerarquía y cómo se muestran los resultados de búsqueda. Esto se controla con los tres botones más a la derecha de la barra de herramientas, junto al botón "Filter":

![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-01.png)

- ![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-02.png) **Jerárquico por elemento padre**: La búsqueda se aplicará a los objetos _padre_; es decir, a tablas y carpetas de visualización (si están habilitadas). Cuando un elemento padre cumpla los criterios de búsqueda, se mostrarán todos los elementos hijos.
- ![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-03.png) **Jerárquico por elementos hijo**: La búsqueda se aplicará a los objetos _hijos_; es decir, a medidas, columnas, jerarquías, etc. Los objetos padre solo se mostrarán si tienen al menos un objeto hijo que cumpla los criterios de búsqueda.
- ![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-04.png) **Plano**: La búsqueda se aplicará a todos los objetos y los resultados se mostrarán en una lista plana. Los objetos que contengan elementos secundarios seguirán mostrándolos de forma jerárquica.

## Búsqueda simple

Escribe lo que quieras en el cuadro de texto "Filter" y pulsa [Enter] para realizar una búsqueda sencilla sin distinguir entre mayúsculas y minúsculas en los nombres de los objetos. Por ejemplo, si escribes "sales" en el cuadro de texto "Filter" y usas el modo de filtrado "By Parent", obtendrás los siguientes resultados:

![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-05.png)

Al expandir cualquiera de las tablas, se mostrarán todas las medidas, columnas, jerarquías y particiones de la tabla. Si cambiamos el modo de filtrado a "By Child", los resultados se verán así:

![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-06.png)

Observa que la tabla "Employee" ahora aparece en la lista, ya que tiene un par de elementos secundarios (columnas, en este caso) que contienen la palabra "sales".

## Búsqueda con comodines

Al escribir una cadena en el cuadro de texto del filtro, puedes usar el comodín `?` para indicar cualquier carácter y `*` para indicar cualquier secuencia de caracteres (cero o más). Así, escribir `*sales*` produciría exactamente los mismos resultados que se muestran más arriba; sin embargo, si escribes `sales*`, solo se mostrarán los objetos cuyo nombre _empieza_ por la palabra "sales" (de nuevo, no distingue entre mayúsculas y minúsculas).

Búsqueda de `sales*` por elemento padre:

![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-07.png)

Búsqueda de `sales*` por elemento hijo:

![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-08.png)

Búsqueda plana de `sales*` (pulsa [Ctrl]+[F1] para mostrar u ocultar las columnas de información y ver información detallada de cada objeto):

![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-09.png)

Los comodines se pueden colocar en cualquier parte de la cadena y puedes incluir tantos como necesites. Si eso no te parece lo bastante complejo, sigue leyendo...

## Búsqueda con LINQ dinámico

También puedes usar [Dynamic LINQ](https://github.com/kahanu/System.Linq.Dynamic/wiki/Dynamic-Expressions) para buscar objetos; es lo mismo que haces al crear reglas del [Best Practice Analyzer](xref:best-practice-analyzer). Para habilitar el modo LINQ dinámico en el cuadro de texto Filtro, solo tienes que poner un `:` (dos puntos) delante de tu cadena de búsqueda. Por ejemplo, para ver todos los objetos cuyo nombre termina en "Key" (distingue entre mayúsculas y minúsculas), escribe:

```
:Name.EndsWith("Key")
```

...y pulsa [Enter]. En el modo de filtrado "Flat", el resultado se ve así:

![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-10.png)

Para una búsqueda sin distinción entre mayúsculas y minúsculas en LINQ dinámico, puedes convertir la cadena de entrada con algo como:

```
:Name.ToUpper().EndsWith("KEY")
```

o bien puedes proporcionar el argumento [StringComparison](https://docs.microsoft.com/en-us/dotnet/api/system.string.endswith?view=netframework-4.7.2#System_String_EndsWith_System_String_System_StringComparison_), por ejemplo:

```
:Name.EndsWith("Key", StringComparison.InvariantCultureIgnoreCase)
```

No estás limitado a buscar solo en los nombres de los objetos. Las cadenas de búsqueda de LINQ dinámico pueden ser tan complejas como quieras, para evaluar cualquier propiedad (incluidas las subpropiedades) de un objeto. Así que, si quieres encontrar todos los objetos que tengan una expresión que contenga la palabra "TODO", usarías el siguiente filtro de búsqueda:

```
:Expression.ToUpper().Contains("TODO")
```

Como otro ejemplo, lo siguiente mostrará todas las medidas ocultas del modelo que no estén referenciadas por ningún otro objeto:

```
:ObjectType="Measure" and (IsHidden or Table.IsHidden) and ReferencedBy.Count=0
```

También puedes usar expresiones regulares. Lo siguiente encontrará todas las columnas cuyo nombre contenga la palabra "Number" o "Amount":

```
:ObjectType="Column" and RegEx.IsMatch(Name,"(Number)|(Amount)")
```

Ten en cuenta que las opciones de visualización (los botones de la barra de herramientas justo encima del árbol) pueden afectar a los resultados al usar los modos de filtrado "By Parent" y "By Child". Por ejemplo, el filtro LINQ anterior solo devuelve columnas, pero si tus opciones de visualización están configuradas para no mostrar columnas, no se mostrará nada.
