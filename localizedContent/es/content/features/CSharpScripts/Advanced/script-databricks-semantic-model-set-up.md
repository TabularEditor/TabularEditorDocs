---
uid: script-databricks-semantic-model-set-up
title: Configuración del modelo semántico de Databricks
author: Johnny Winter
updated: 2025-09-04
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Configuración del modelo semántico de Databricks

## Objetivo del script

Este script se creó como parte de la serie Tabular Editor x Databricks. En Databricks Unity Catalog no es posible usar letras mayúsculas en los nombres de las tablas. Una forma habitual de hacer más legibles los nombres de las tablas sin usar mayúsculas es adoptar snake_case. Además, aunque los nombres de columna pueden contener espacios, a menudo se desaconseja porque pueden ser engorrosos de manejar; por eso, lo más habitual es que los ingenieros de datos usen snake_case, camelCase o PascalCase.

Sin embargo, queremos que los usuarios de nuestro modelo semántico vean en él nombres amigables para el negocio.

El siguiente script recorrerá todas las tablas del modelo y se asegurará de que se aplique un formato legible en Proper Case.

Al hacerlo, también aplicará algunas recomendaciones de buenas prácticas: establecerá “Resumir por” de forma predeterminada en “Ninguno” para todas las columnas y también configurará cadenas de formato para los campos de tipo DateTime (este script está configurado para usar el formato 'yyyy-mm-dd', pero puedes cambiarlo en la línea 61 si lo prefieres) <br></br>

> [!NOTE]
> Este script no es estrictamente para usarse solo con Databricks; úsalo con cualquier modelo que quieras, independientemente de la fuente de datos, pero se ha creado teniendo en cuenta algunas de las limitaciones de Databricks. <br></br>

## Script

### Configuración del modelo semántico de Databricks

```csharp
/*
 * Title: Databricks Semantic Model Set-Up
 * Author: Johnny Winter, greyskullanalytics.com
 *
 *  This script, when executed, will loop through all tables and columns in the model and rename with friendly names. 
 *  Names in snake_case, camelCase or PascalCase will all be converted to Proper Case.
 *  No table selections are required as all tables in the model will be processed, simply run the script.
 *  Whilst looping though columns it also sets default summarization to none and sets a format string for all DateTime type fields 
 *  (currently it sets format 'yyyy-mm-dd' but you can change this on line 61 if you wish).
 *
 */
using System;
using System.Globalization;

//create script as class so it can be reused 
class p {

    public static void ConvertCase(dynamic obj)
    {
        TextInfo textInfo = CultureInfo.CurrentCulture.TextInfo;
        //replace underscores with a space
        var oldName = obj.Name.Replace("_", " ");
        var newName = new System.Text.StringBuilder();
        for(int i = 0; i < oldName.Length; i++) {
            // First letter should always be capitalized:
            if(i == 0) newName.Append(Char.ToUpper(oldName[i]));

            // A sequence of two uppercase letters followed by a lowercase letter should have a space inserted
            // after the first letter:
            else if(i + 2 < oldName.Length && char.IsLower(oldName[i + 2]) && char.IsUpper(oldName[i + 1]) && char.IsUpper(oldName[i]))
            {
                newName.Append(oldName[i]);
                newName.Append(" ");
            }

            // All other sequences of a lowercase letter followed by an uppercase letter, should have a space
            // inserted after the first letter:
            else if(i + 1 < oldName.Length && char.IsLower(oldName[i]) && char.IsUpper(oldName[i+1]))
            {
                newName.Append(oldName[i]);
                newName.Append(" ");
            }
            else
            {
                newName.Append(oldName[i]);
            }
        }
        //apply Proper Case where this has not already been taken care of above
        obj.Name = textInfo.ToTitleCase(newName.ToString());
    }
}

foreach(var t in Model.Tables) {
//convert table names
    p.ConvertCase(t);
//convert column names
    foreach(var c in t.Columns) {
        p.ConvertCase(c);
        c.SummarizeBy = AggregateFunction.None;
        if (c.DataType == DataType.DateTime)
        {c.FormatString = "yyyy-mm-dd";}
    }
}
```

### Explicación

Este script, al ejecutarse, recorrerá todas las tablas y columnas del modelo y las renombrará con nombres descriptivos. Los nombres en snake_case, camelCase o PascalCase se convertirán a Proper Case. No es necesario seleccionar tablas: se procesarán todas las tablas del modelo. Solo tienes que ejecutar el script. Mientras recorre las columnas, también establece “Resumir por” de forma predeterminada en “Ninguno” y define una cadena de formato para todos los campos de tipo DateTime.

