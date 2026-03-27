---
uid: master-model-pattern
title: Patrón del modelo maestro
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Patrón del modelo maestro

No es raro que una organización tenga varios modelos tabulares, con un solapamiento funcional considerable. Para el equipo de desarrollo, mantener estos modelos al día con funcionalidades compartidas puede ser un quebradero de cabeza. En este artículo veremos un enfoque alternativo que puede ser adecuado cuando tenga sentido combinar todos estos modelos en un único modelo "maestro", que luego se despliega parcialmente en varios modelos derivados distintos. Tabular Editor habilita este enfoque utilizando las perspectivas de una forma especial (sin dejar de permitir que las perspectivas funcionen de la manera habitual).

**Descargo de responsabilidad:** Aunque esta técnica funciona, Microsoft no la admite y requiere una buena dosis de aprendizaje, escritura de scripts y algo de hacking. Decide por ti mismo si crees que es el enfoque adecuado para tu equipo.

Para simplificar, consideremos el modelo de ejemplo AdventureWorks:

![image](https://user-images.githubusercontent.com/8976200/43959290-895c1c96-9cae-11e8-8112-008f54cb400a.png)

Supongamos que, por alguna razón, hay que desplegar todo lo relacionado con Internet Sales como un modelo y todo lo relacionado con Reseller Sales como otro. Puede ser por motivos de seguridad, rendimiento, escalabilidad o incluso porque tu equipo da servicio a varios clientes externos y cada cliente necesita su propia copia del modelo, con funcionalidad tanto compartida como específica.

En lugar de mantener una rama de desarrollo para cada una de las versiones, la técnica que se presenta aquí te permite mantener un único modelo y usar metadatos para indicar cómo debe dividirse en el momento del despliegue.

## (Ab)uso de perspectivas

La idea es bastante simple. Empieza agregando varias perspectivas nuevas al modelo, en función del número de modelos de destino que necesites implementar. Asegúrate de anteponer un prefijo coherente a estas perspectivas para separarlas de las perspectivas orientadas al usuario:

![image](https://user-images.githubusercontent.com/8976200/43960154-6b637042-9cb1-11e8-906b-6671bbb9558e.png)

Aquí usamos el signo `-` como prefijo en los nombres de las perspectivas. Más adelante veremos cómo se eliminan estas perspectivas del modelo, de modo que los usuarios finales no las vean. Solo las usan los desarrolladores del modelo.

Ahora, simplemente agrega a estas perspectivas todos los objetos que se necesiten en los modelos individuales. Usa la lista desplegable de perspectiva en Tabular Editor para confirmar que un modelo contiene los objetos necesarios. Aquí tienes un script práctico que también puedes usar para asegurarte de que todas las dependencias estén incluidas en la perspectiva:

```csharp
// Recorre todas las jerarquías de la perspectiva actual:
foreach(var h in Model.AllHierarchies.Where(h => h.InPerspective[Selected.Perspective]))
{
    // Asegúrate de que las columnas usadas en los niveles de jerarquía estén incluidas en la perspectiva:
    foreach(var level in h.Levels) {
        level.Column.InPerspective[Selected.Perspective] = true;
    }
}

// Recorre todas las medidas y columnas de la perspectiva actual:
foreach(var obj in Model.AllMeasures.Cast<ITabularPerspectiveObject>()
    .Concat(Model.AllColumns).Where(m => m.InPerspective[Selected.Perspective])
    .OfType<IDaxDependantObject>().ToList())
{
    // Recorre todos los objetos de los que depende el objeto actual:
    foreach(var dep in obj.DependsOn.Deep())
    {
        // Incluye las dependencias de columnas, medidas y tablas:
        var columnDep = dep as Column; if(columnDep != null) columnDep.InPerspective[Selected.Perspective] = true;
        var measureDep = dep as Measure; if(measureDep != null) measureDep.InPerspective[Selected.Perspective] = true;
        var tableDep = dep as Table; if(tableDep != null) tableDep.InPerspective[Selected.Perspective] = true;
    }    
}

// Recorre todas las columnas que tienen una SortByColumn en la perspectiva actual:
foreach(var c in Model.AllColumns.Where(c => c.InPerspective[Selected.Perspective] && c.SortByColumn != null))
{
    c.SortByColumn.InPerspective[Selected.Perspective] = true;   
}
```

**Explicación:** Primero, el script recorre todas las jerarquías de la perspectiva actual (la perspectiva seleccionada en ese momento en la lista desplegable de la parte superior de la pantalla). Para cada una de estas jerarquías, se asegura de que todas las columnas usadas como niveles de jerarquía aparezcan en la perspectiva. A continuación, el script recorre todas las columnas y medidas de la perspectiva actual. Para cada uno de estos objetos, también se incluyen en la perspectiva todas las dependencias de DAX en forma de referencias a medidas, columnas o tablas. Ten en cuenta que expresiones como `DISTINCTCOUNT('Customer'[CustomerId])` harán que se incluyan en la perspectiva todas las columnas de la tabla 'Customer', ya que Tabular Editor trata ese tipo de expresión como si tuviera una dependencia tanto de la propia columna [CustomerId] como de la tabla 'Customer'. Por último, el script se asegura de que cualquier columna que se use como columna de "Ordenar por" también se incluya en la perspectiva.

Te recomiendo guardar este script como una acción personalizada a nivel de modelo para que te resulte fácil ejecutarlo en adelante.

Por cierto, si quieres hacer una copia de una perspectiva, ya puedes hacerlo desde la IU. Haz clic en el nodo "perspectivas" del árbol del explorador y, después, haz clic en el botón de puntos suspensivos de la cuadrícula de propiedades:

![image](https://user-images.githubusercontent.com/8976200/44028910-c7ffab80-9efb-11e8-813a-5b0f5c137bab.png)

Esto abrirá un cuadro de diálogo que te permite crear y eliminar perspectivas, así como clonar las existentes:

![image](https://user-images.githubusercontent.com/8976200/44028953-f13c91ca-9efb-11e8-936a-1f0e1d4eb93f.png)

Para complementar esto, aquí tienes un script que elimina de una perspectiva todos los objetos invisibles y sin uso, por si necesitas hacer un poco de limpieza:

```csharp
// Recorre todas las columnas de la perspectiva actual:
foreach(var c in Model.AllColumns.Where(c => c.InPerspective[Selected.Perspective])) {
    if(
        // Si la columna está oculta (o la tabla principal está oculta):
        (c.IsHidden || c.Table.IsHidden) 

        // Y no se usa en ninguna relación:
        && !c.UsedInRelationships.Any()
        
        // Y no se usa como SortByColumn para ninguna otra columna de la perspectiva:
        && !c.UsedInSortBy.Any(sb => !sb.IsHidden && sb.InPerspective[Selected.Perspective])
        
        // Y no se usa en ninguna jerarquía de la perspectiva:
        && !c.UsedInHierarchies.Any(h => h.InPerspective[Selected.Perspective])
        
        // Y no se hace referencia a ella en ninguna expresión DAX de otros objetos visibles de la perspectiva:
        && !c.ReferencedBy.Deep().OfType<ITabularPerspectiveObject>()
            .Any(obj => obj.InPerspective[Selected.Perspective] && !(obj as IHideableObject).IsHidden)
            
        // Y no se hace referencia a ella desde ningún rol:
        && !c.ReferencedBy.Roles.Any()    )
    {
        // Si se cumple todo lo anterior, la columna se puede quitar de la perspectiva actual:
        c.InPerspective[Selected.Perspective] = false; 
    }
}

// Recorre todas las medidas de la perspectiva actual:
foreach(var m in Model.AllMeasures.Where(m => m.InPerspective[Selected.Perspective])) {
    if(
        // Si la medida está oculta (o la tabla principal está oculta):
        (m.IsHidden || m.Table.IsHidden) 

        // Y no se hace referencia a ella en ninguna expresión DAX de otros objetos visibles de la perspectiva:
        && !m.ReferencedBy.Deep().OfType<ITabularPerspectiveObject>()
            .Any(obj => obj.InPerspective[Selected.Perspective] && !(obj as IHideableObject).IsHidden)
    )
    {
        // Si se cumple todo lo anterior, la medida se puede quitar de la perspectiva actual:
        m.InPerspective[Selected.Perspective] = false; 
    }
}
```

**Explicación:** Primero, el script recorre todas las columnas de la perspectiva seleccionada actualmente. Quita una columna de la perspectiva solo si se cumple todo lo siguiente:

- La columna está oculta (o la tabla que contiene la columna está oculta)
- La columna no participa en ninguna relación
- La columna no se usa como SortByColumn de ninguna otra columna visible en la perspectiva
- La columna no se usa como nivel en ninguna jerarquía de la perspectiva
- No se hace referencia directa ni indirecta a la columna en ninguna expresión DAX de otros objetos visibles en la perspectiva
- La columna no se usa en ninguna expresión de filtro a nivel de fila

Para las medidas, hacemos lo mismo, pero de forma simplificada: solo quitamos las medidas que cumplan los siguientes criterios:

- La medida está oculta (o la tabla donde se encuentra la medida está oculta)
- No se hace referencia a la medida, directa ni indirectamente, en ninguna expresión DAX de otros objetos visibles de la perspectiva

Si trabajas en un equipo de desarrolladores en el modelo, ya deberías estar usando la funcionalidad ["Guardar en carpeta"](xref:folder-serialization) de Tabular Editor junto con un entorno de control de código fuente como Git. Asegúrate de activar la opción "Serializar perspectivas por objeto" en "Archivo" > "Preferencias" > "Guardar en carpeta" para evitar un montón de conflictos de fusión en las definiciones de tus perspectivas.

![image](https://user-images.githubusercontent.com/8976200/44029969-935e0efe-9eff-11e8-93de-c1223f7ebe7f.png)

## Añadir un control más granular

A estas alturas, probablemente ya hayas adivinado que vamos a usar scripts para crear una versión del modelo para cada una de nuestras perspectivas de desarrollador prefijadas. El script simplemente quitará del modelo todos los objetos que no estén incluidos en una perspectiva de desarrollador determinada. Sin embargo, antes de hacerlo, hay un par de situaciones más que debemos contemplar.

### Controlar objetos que no pertenecen a ninguna perspectiva

Algunos objetos, como las perspectivas, los Data sources y los roles, no se incluyen ni se excluyen en las propias perspectivas, pero aun así puede que necesitemos una forma de especificar a qué versiones del modelo deben pertenecer. Para esto, vamos a usar anotaciones. Volviendo a nuestro modelo de Adventure Works, puede que queramos que las perspectivas "Inventory" y "Internet Operation" aparezcan en "$InternetModel" y "$ManagementModel", mientras que "Reseller Operation" debería aparecer en "$ResellerModel" y "$ManagementModel".

Así que vamos a añadir una nueva anotación llamada "DevPerspectives" en cada una de las 3 perspectivas originales, y simplemente proporcionaremos los nombres de las perspectivas de desarrollador como una cadena separada por comas:

![image](https://user-images.githubusercontent.com/8976200/44032304-01bdcc70-9f07-11e8-9b28-db0912ea1ade.png)

Cuando agregues nuevas perspectivas de _usuario_ al modelo, recuerda añadir la misma anotación y proporcionar los nombres de las perspectivas de desarrollador en las que quieres que se incluya la perspectiva de _usuario_. Cuando más adelante generemos mediante scripting las versiones finales del modelo, usaremos la información de estas anotaciones para incluir las perspectivas necesarias. Podemos hacer lo mismo con los Data sources y los roles.

### Controlar metadatos de los objetos

También puede haber situaciones en las que la misma medida deba tener expresiones o cadenas de formato ligeramente distintas entre las diferentes versiones del modelo. De nuevo, podemos usar anotaciones para proporcionar los metadatos por perspectiva de desarrollador y, luego, aplicar esos metadatos cuando generemos mediante scripting el modelo final.

La forma más sencilla de serializar todas las propiedades de los objetos en texto probablemente sea la función de script [ExportProperties](/Useful-script-snippets#export-object-properties-to-a-file). Sin embargo, para nuestro caso de uso es un poco excesivo, así que vamos a especificar directamente qué propiedades queremos guardar como anotaciones. Crea el siguiente script:

```csharp
foreach(var m in Selected.Measures) { 
    m.SetAnnotation(Selected.Perspective.Name + "_Expression", m.Expression);
    m.SetAnnotation(Selected.Perspective.Name + "_FormatString", m.FormatString);
    m.SetAnnotation(Selected.Perspective.Name + "_Description", m.Description);
}
```

A continuación, guárdalo como una acción personalizada llamada "Save Metadata as Annotations":

![image](https://user-images.githubusercontent.com/8976200/44033695-7a754482-9f0b-11e8-937b-0bc0987ce7cb.png)

Del mismo modo, guarda el siguiente script como una acción personalizada llamada "Load Metadata from Annotations":

```csharp
foreach(Measure m in Selected.Measures) { 
    var expr = m.GetAnnotation(Selected.Perspective.Name + "_Expression"); if(expr == null) continue;
    m.Expression = expr;
    m.FormatString = m.GetAnnotation(Selected.Perspective.Name + "_FormatString");
    m.Description = m.GetAnnotation(Selected.Perspective.Name + "_Description");
}
```

La idea es crear una anotación para cada una de las propiedades de las que queremos mantener versiones distintas, según la perspectiva del desarrollador. Si necesitas mantener por separado otras propiedades además de las que se muestran en el script (Expression, FormatString, Description), simplemente añádelas al script. Puedes hacer lo mismo con otros tipos de objetos, pero probablemente no tenga mucho sentido salvo para medidas y quizá columnas calculadas y particiones (para mantener, por ejemplo, distintas expresiones de consulta por versión del modelo).

Usa tus nuevas acciones personalizadas para aplicar cambios específicos de la versión del modelo a las perspectivas del desarrollador (o añade las anotaciones a mano). Por ejemplo, en nuestro ejemplo de Adventure Works, queremos que la medida [Day Count] tenga una expresión diferente en la perspectiva $ResellerModel; para ello, aplicamos los cambios a la medida y ejecutamos la acción "Save Metadata as Annotations" con la perspectiva "$ResellerModel" seleccionada en el desplegable:

![image](https://user-images.githubusercontent.com/8976200/44033944-3104e414-9f0c-11e8-9f06-396bf85a0e4f.png)

En la captura anterior, tenemos 3 anotaciones para cada una de las perspectivas del desarrollador. Sin embargo, en la práctica solo tendríamos que crear estas anotaciones para aquellas perspectivas del desarrollador en las que las propiedades deban diferir de sus valores originales.

## Modificar las consultas de partición

Podemos usar una técnica similar para aplicar cambios a las consultas de partición entre las distintas versiones. Por ejemplo, quizá quieras criterios SQL `WHERE` distintos en algunas consultas de partición según la versión. Empecemos creando un conjunto de nuevas anotaciones en nuestros objetos de _tabla_ para especificar la consulta SQL base que queremos que usen nuestras particiones para cada versión. Aquí, por ejemplo, queremos restringir qué registros se incluyen en la tabla Product en dos de nuestras tres versiones:

![image](https://user-images.githubusercontent.com/8976200/44736562-69221580-aaa4-11e8-82ee-88388015d30d.png)

En las tablas que tienen varias particiones, especifica los criterios WHERE mediante "marcadores de posición", que se reemplazarán más adelante:

![image](https://user-images.githubusercontent.com/8976200/44737015-b3f05d00-aaa5-11e8-9bad-cadd5b4dae35.png)

Define los valores de los marcadores de posición dentro de cada partición (nota: debes usar [Tabular Editor v. 2.7.3](https://github.com/TabularEditor/TabularEditor/releases/tag/2.7.3) o una versión posterior para editar las anotaciones de partición desde la interfaz de usuario):

![image](https://user-images.githubusercontent.com/8976200/44737199-2a8d5a80-aaa6-11e8-8813-8189b593da98.png)

En escenarios de particionado dinámico, no olvides incluir estas anotaciones en el script que uses al crear las nuevas particiones. En la siguiente sección, veremos cómo aplicar estos valores de los marcadores de posición durante la implementación.

## Despliegue de distintas versiones

Por fin, estamos listos para desplegar nuestro modelo en 3 versiones diferentes. Por desgracia, la interfaz del Asistente de implementación de Tabular Editor no puede dividir el modelo en función de las perspectivas y anotaciones que hemos creado, así que tendríamos que crear un script adicional que reduzca nuestro modelo a una versión concreta. ¿Este script puede ejecutarse entonces como parte de un despliegue desde la línea de comandos, de modo que todo el proceso de despliegue pueda empaquetarse en un archivo de comandos, un ejecutable de PowerShell o quizá incluso integrarse en tu proceso de compilación/despliegue automatizado?

El script que necesitamos es el siguiente. La idea es crear un script por cada perspectiva de desarrollador. Guarda el script como un archivo de texto y llámalo, por ejemplo, `ResellerModel.cs`:

```csharp
var version = "ResellerModel"; // TODO: Sustituye esto por el nombre de tu perspectiva de desarrollador

// Quita tablas, medidas, columnas y jerarquías que no formen parte de la perspectiva:
foreach(var t in Model.Tables.ToList()) {
    if(!t.InPerspective[version]) t.Delete();
    else {
        foreach(var m in t.Measures.ToList()) if(!m.InPerspective[version]) m.Delete();   
        foreach(var c in t.Columns.ToList()) if(!c.InPerspective[version]) c.Delete();
        foreach(var h in t.Hierarchies.ToList()) if(!h.InPerspective[version]) h.Delete();
    }
}

// Quita las perspectivas de usuario en función de las anotaciones y todas las perspectivas de desarrollador:
foreach(var p in Model.Perspectives.ToList()) {
    if(p.Name.StartsWith("Dev")) p.Delete();

    // Conserva todas las demás perspectivas que no tengan la anotación "DevPerspectives", y elimina
    // las que sí la tengan si <version> no está especificado en la anotación:
    if(p.GetAnnotation("DevPerspectives") != null && !p.GetAnnotation("DevPerspectives").Contains(version)) 
        p.Delete();
}

// Quita los Data sources en función de las anotaciones:
foreach(var ds in Model.DataSources.ToList()) {
    if(ds.GetAnnotation("DevPerspectives") == null) continue;
    if(!ds.GetAnnotation("DevPerspectives").Contains(version)) ds.Delete();
}

// Quita roles en función de las anotaciones:
foreach(var r in Model.Roles.ToList()) {
    if(r.GetAnnotation("DevPerspectives") == null) continue;
    if(!r.GetAnnotation("DevPerspectives").Contains(version)) r.Delete();
}

// Modifica medidas en función de las anotaciones:
foreach(Measure m in Model.AllMeasures) {
    var expr = m.GetAnnotation(version + "_Expression"); if(expr == null) continue;
    m.Expression = expr;
    m.FormatString = m.GetAnnotation(version + "_FormatString");
    m.Description = m.GetAnnotation(version + "_Description");    
}

// Establece las consultas de partición según las anotaciones:
foreach(Table t in Model.Tables) {
    var queryWithPlaceholders = t.GetAnnotation(version + "_PartitionQuery"); if(queryWithPlaceholders == null) continue;
    
    // Recorre todas las particiones de esta tabla:
    foreach(Partition p in t.Partitions) {
        
        var finalQuery = queryWithPlaceholders;

        // Sustituye todos los valores de los marcadores de posición:
        foreach(var placeholder in p.Annotations.Keys) {
            finalQuery = finalQuery.Replace("%" + placeholder + "%", p.GetAnnotation(placeholder));
        }

        p.Query = finalQuery;
    }
}

// TODO: Modifica otros objetos en función de las anotaciones, si procede...
```

**Explicación:** Primero, quitamos todas las tablas, columnas, medidas y jerarquías que no formen parte de la perspectiva definida en la línea 1 del script. Después, quitamos cualquier objeto adicional en el que hayamos aplicado la anotación "DevPerspectives", tal y como se describió antes, junto con todas las perspectivas de desarrollador. A continuación, aplicamos cualquier cambio en las expresiones de medida, cadenas de formato o descripciones en función de las anotaciones, si las hubiera. Por último, aplicamos las consultas de partición definidas en las anotaciones (si las hubiera) y, además, sustituimos los valores de los marcadores de posición por los valores anotados (si los hubiera).

Ten en cuenta que también podríamos añadir cambios específicos adicionales del modelo directamente a este script si quisiéramos, pero el objetivo de este ejercicio era ver cómo podemos mantener varios modelos directamente desde Tabular Editor. El script anterior es el mismo, independientemente de la versión que queramos desplegar (salvo, por supuesto, la línea 1).

Por último, podemos cargar nuestro archivo Model.bim, ejecutar el script y desplegar el modelo modificado de una sola vez, usando la siguiente [sintaxis de línea de comandos](/Command-line-Options):

```sh
start /wait /d "c:\Program Files (x86)\Tabular Editor" TabularEditor.exe Model.bim -S ResellerModel.cs -D localhost AdventureWorksReseller -O -R
```

Para desplegar las versiones Internet o Management, tendríamos que hacer lo mismo e indicar los scripts correspondientes:

```sh
start /wait /d "c:\Program Files (x86)\Tabular Editor" TabularEditor.exe Model.bim -S InternetModel.cs -D localhost AdventureWorksInternet -O -R
start /wait /d "c:\Program Files (x86)\Tabular Editor" TabularEditor.exe Model.bim -S ManagementModel.cs -D localhost AdventureWorksManagement -O -R
```

Esto supone que estás ejecutando el comando desde el directorio donde se encuentra tu archivo Model.bim (o el archivo Database.json si usas la funcionalidad "Guardar en carpeta"). El modificador -S indica a Tabular Editor que aplique al modelo el script proporcionado, y el modificador -D realiza el despliegue. El modificador -O permite sobrescribir una base de datos existente con el mismo nombre, y el modificador -R indica que también queremos sobrescribir los roles de la base de datos de destino.

## Procesamiento del modelo maestro

Si tienes un servidor de procesamiento dedicado y existe un gran solapamiento de datos entre los modelos individuales, puede tener sentido procesar primero los datos en el modelo maestro antes de dividirlo. Así puedes evitar procesar los mismos datos varias veces en modelos individuales. **No obstante, esto supone que no estás procesando ninguna tabla en la que la consulta de partición haya cambiado entre versiones, como se muestra en [esta sección](/xref:Master-model-pattern#altering-partition-queries).** La receta para hacerlo se describe a continuación:

1. (Opcional, en caso de que haya cambios en los metadatos) Implementa tu modelo maestro en tu servidor de procesamiento
2. Realiza el procesamiento que necesites en tu modelo maestro (no proceses las tablas que tengan consultas de partición específicas de la versión).
3. Sincroniza el modelo maestro en cada modelo individual y usa el comando anterior para depurar los modelos individuales después de la sincronización; a continuación, ejecuta un ProcessRecalc si es necesario.
4. (Opcional) Procesa las tablas de los modelos individuales que tengan consultas de partición específicas de la versión.

## Consejos y trucos

Cuando empiezas a usar con frecuencia anotaciones personalizadas, puede haber situaciones en las que quieras enumerar todos los objetos con una anotación concreta. Aquí es donde las expresiones LINQ dinámicas del cuadro de filtro resultan muy útiles.

Para empezar, supongamos que queremos encontrar todos los objetos en los que hemos añadido una anotación con el nombre "$InternetModel_Expression". Escribe lo siguiente en el cuadro de texto del filtro y pulsa ENTER:

```
:GetAnnotation("$InternetModel_Expression")<>null
```

O, si quieres encontrar todos los objetos que tengan una anotación que termine en "_Expression", usa:

```
:GetAnnotations().Any(EndsWith("_Expression"))
```

Ten en cuenta que estas funciones distinguen entre mayúsculas y minúsculas; por lo tanto, si tu anotación se escribió en minúsculas, el filtro anterior no la encontrará.

También puedes buscar objetos en los que la anotación tenga un valor específico:

```
:GetAnnotation("$InternetModel_Description").Contains("TODO")
```

## Conclusión

La técnica que se describe aquí puede ser muy útil para mantener muchos modelos similares con gran parte de funcionalidad compartida, como las tablas de calendario y otras dimensiones comunes. Los scripts utilizados se pueden reutilizar fácilmente como acciones personalizadas en Tabular Editor, mientras que el despliegue se puede automatizar de varias formas.
