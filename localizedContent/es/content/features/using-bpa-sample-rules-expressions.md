---
uid: using-bpa-sample-rules-expressions
title: Expresión de reglas de muestra de BPA
author: Morten Lønskov
updated: 2023-02-21
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

# Ejemplos de expresiones de reglas

En esta sección verás algunos ejemplos de expresiones de LINQ dinámico que se pueden usar para definir reglas. La expresión que se escribe en el Editor de expresiones se evaluará cada vez que el foco abandone el cuadro de texto, y cualquier error de sintaxis se mostrará en la parte superior de la pantalla:

![image](https://cloud.githubusercontent.com/assets/8976200/25380170/9f01634e-29af-11e7-952e-e10a1f28df32.png)

Sus expresiones de reglas pueden acceder a cualquier propiedad pública de los objetos del TOM. Si intenta acceder a una propiedad que no existe en ese tipo de objeto, también se mostrará un error:

![image](https://cloud.githubusercontent.com/assets/8976200/25381302/798bab98-29b3-11e7-931e-789e5286fc45.png)

"Expression" no existe en el objeto "Column", pero si cambiamos el menú desplegable a "Columnas calculadas", la instrucción anterior funciona sin problema:

![image](https://cloud.githubusercontent.com/assets/8976200/25380451/87b160da-29b0-11e7-8e2e-c4e47593007d.png)

LINQ dinámico admite todos los operadores aritméticos, lógicos y de comparación estándar y, mediante la notación ".", puede acceder a subpropiedades y -métodos de todos los objetos.

```
String.IsNullOrWhitespace(Expression) and not Name.StartsWith("Dummy")
```

La instrucción anterior, aplicada a columnas calculadas, tablas calculadas o medidas, marca aquellas que tienen una expresión DAX vacía, salvo que el nombre del objeto empiece por el texto "Dummy".

Con LINQ también podemos trabajar con colecciones de objetos. La siguiente expresión, aplicada a tablas, encontrará aquellas que tengan más de 10 columnas que no estén organizadas en carpetas de visualización:

```
Columns.Count(DisplayFolder = "") > 10
```

Cada vez que usamos un método LINQ para iterar sobre una colección, la expresión que se usa como argumento del método LINQ se evalúa para los elementos de la colección. En efecto, DisplayFolder es una propiedad de las columnas que no existe a nivel de tabla.

Aquí vemos esta regla en acción en el modelo tabular Adventure Works. Observa cómo la tabla "Reseller" aparece como incumpliendo la regla, mientras que "Reseller Sales" no aparece (las columnas de esta última se han organizado en carpetas de visualización):

![image](https://cloud.githubusercontent.com/assets/8976200/25380809/d9d1c3a4-29b1-11e7-839e-29450ad39c8a.png)

Para hacer referencia al objeto padre dentro de un método LINQ, usa la sintaxis especial "outerIt". Esta regla, aplicada a tablas, encontrará aquellas que contienen columnas cuyo nombre no empieza por el nombre de la tabla:

```
Columns.Any(not Name.StartsWith(outerIt.Name))
```

Probablemente tenga más sentido aplicar esta regla directamente a las columnas; en ese caso, debería escribirse así:

```
not Name.StartsWith(Table.Name)
```

Para comparar con propiedades de enumeración, basta con pasar el valor enumerado como una cadena. Esta regla encontrará todas las columnas cuyo nombre termina con la palabra "Key" o "ID", pero en las que la propiedad SummarizeBy no se ha establecido en "None":

```
(Name.EndsWith("Key") or Name.EndsWith("ID")) and SummarizeBy <> "None"
```

## Búsqueda de objetos sin usar

Al crear modelos tabulares, es importante evitar a toda costa las columnas de alta cardinalidad. Los culpables típicos son marcas de tiempo del sistema, claves técnicas, etc., que se han importado al modelo por error. En general, debemos asegurarnos de que el modelo solo contenga las columnas que realmente se necesitan. ¿No sería genial si el Best Practice Analyzer pudiera decirnos qué columnas probablemente no se necesitan en absoluto?

La siguiente regla informará sobre las columnas que:

- ...están ocultas (o cuya tabla padre está oculta)
- ...no están referenciadas por ninguna expresión DAX (considera todas las expresiones DAX del modelo, incluso drillthrough y expresiones de filtro de RLS)
- ...no participan en ninguna relación
- ...no se usan como columna de "Ordenar por" de ninguna otra columna
- ...no se usan como niveles de una jerarquía.

La expresión de LINQ dinámico para esta regla de BPA es:

```
(IsHidden or Table.IsHidden)
and ReferencedBy.Count = 0 
and (not UsedInRelationships.Any())
and (not UsedInSortBy.Any())
and (not UsedInHierarchies.Any())
```

La misma técnica se puede usar para encontrar medidas no utilizadas. Es un poco más sencillo, ya que las medidas no pueden participar en relaciones, etc. Así que, para hacerlo un poco más interesante, también vamos a tener en cuenta si los objetos dependientes que hacen referencia a una medida determinada están visibles o no. Es decir, si la medida [A] es referenciada por la medida [B], y tanto la medida [A] como [B] están ocultas, y ninguna otra expresión DAX hace referencia a estas dos medidas, deberíamos indicar al desarrollador que es seguro eliminar ambas:

```
(IsHidden or Table.IsHidden)
and not ReferencedBy.AllMeasures.Any(not IsHidden)
and not ReferencedBy.AllColumns.Any(not IsHidden)
and not ReferencedBy.AllTables.Any(not IsHidden)
and not ReferencedBy.Roles.Any()
```

## Corrección de objetos

En algunos casos, es posible corregir automáticamente los problemas en los objetos que cumplen los criterios de una regla. Por ejemplo, cuando solo se trata de establecer una propiedad simple en el objeto. Examine con más detalle el JSON detrás de la siguiente regla:

```json
{
    "ID": "FKCOLUMNS_HIDDEN",
    "Name": "Hide foreign key columns",
    "Category": null,
    "Description": "Columns used on the Many side of a relationship should be hidden.",
    "Severity": 1,
    "Scope": "Column",
    "Expression": "Model.Relationships.Any(FromColumn = outerIt) and not IsHidden and not Table.IsHidden",
    "FixExpression": "IsHidden = true",
    "CompatibilityLevel": 1200
}
```

Esta regla encuentra todas las columnas que se usan en una relación (en el lado "Many"/"From"), pero en las que ni la columna ni su tabla principal están ocultas. Se recomienda que estas columnas nunca se muestren, ya que los usuarios deberían filtrar los datos usando la tabla relacionada (de dimensión). Así, la corrección en este caso sería establecer la propiedad IsHidden de las columnas en true, que es exactamente lo que hace la cadena "FixExpression" anterior. Para verlo en acción, haz clic con el botón derecho en cualquier objeto que incumpla la regla y elige "Generar script de corrección". Esto coloca un pequeño script en el portapapeles, que se puede pegar en el Editor avanzado de scripts, desde donde puedes revisar el código fácilmente y ejecutarlo:

![image](https://cloud.githubusercontent.com/assets/8976200/25298489/9035bab6-26f5-11e7-8134-8502daaf4132.png)

Recuerda que siempre puedes deshacer (CTRL+Z) los cambios realizados en un modelo después de ejecutar el script.
