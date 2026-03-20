---
uid: custom-actions
title: Acciones personalizadas
---

# Acciones personalizadas

> [!NOTE]
> Ten en cuenta que esta funcionalidad no está relacionada con la característica de Acciones personalizadas disponible para modelos multidimensionales.

Supón que has creado un script útil usando el objeto `Selected` y quieres poder ejecutarlo varias veces sobre distintos objetos del árbol del explorador. En lugar de pulsar el botón "Reproducir" cada vez que quieras ejecutar el script, Tabular Editor te permite guardarlo como una Acción personalizada:

![image](https://user-images.githubusercontent.com/8976200/33581673-0db35ed0-d952-11e7-90cd-e3164e198865.png)

Después de guardar la acción personalizada, verás que ya está disponible directamente en el menú contextual de clic derecho del árbol del explorador, lo que facilita mucho ejecutar el script sobre cualquier objeto seleccionado en el árbol. Puedes crear tantas acciones personalizadas como quieras. Usa barras invertidas (\\) en los nombres para crear una estructura de submenús dentro del menú contextual.

![Las acciones personalizadas aparecen directamente en el menú contextual](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/InvokeCustomAction.png)

Las acciones personalizadas se almacenan en el archivo CustomActions.json en %AppData%\Local\TabularEditor. En el ejemplo anterior, el contenido de este archivo se verá así:

```json
{
  "Actions": [
    {
      "Name": "Formato personalizado\\Número con 1 decimal",
      "Enabled": "true",
      "Execute": "Selected.Measures.ForEach(m => m.FormatString = \"0.0\";",
      "Tooltip": "Establece la propiedad FormatString en \"0.0\"",
      "ValidContexts": "Measure, Column"
    }
  ]
}
```

Como puedes ver, `Name` y `Tooltip` obtienen sus valores de lo que se haya especificado al guardar la acción. `Execute` es el script real que se ejecutará cuando se invoque la acción. Ten en cuenta que cualquier error de sintaxis en el archivo CustomActions.json hará que Tabular Editor omita por completo la carga de todas las acciones personalizadas; por tanto, asegúrate de que puedes ejecutar correctamente un script dentro del editor de scripts avanzado antes de guardarlo como acción personalizada.

La propiedad `ValidContexts` contiene una lista de tipos de objeto para los que la acción estará disponible. Al seleccionar objetos en el árbol, una selección que contenga cualquier objeto distinto de los tipos indicados en la propiedad `ValidContexts` ocultará la acción del menú contextual.

## Control de la disponibilidad de la acción

Si necesitas aún más control sobre cuándo se puede invocar una acción desde el menú contextual, puedes establecer la propiedad `Enabled` en una expresión personalizada que debe devolver un valor booleano, indicando si la acción estará disponible para la selección dada. De forma predeterminada, la propiedad `Enabled` tiene el valor "true", lo que significa que la acción siempre estará habilitada dentro del contexto válido. Ten esto en cuenta cuando uses las referencias de objeto en singular del objeto `Selected`, como `Selected.Measure` o `Selected.Table`, ya que estas generarán un error si la selección actual no contiene exactamente uno de ese tipo de objeto. En ese caso, se recomienda usar la propiedad `Enabled` para comprobar que se ha seleccionado uno y solo uno de los objetos del tipo requerido:

```json
{
  "Actions": [
    {
      "Name": "Restablecer nombre de la medida",
      "Enabled": "Selected.Measures.Count == 1",
      "Execute": "Selected.Measure.Name == \"New Measure\"",
      "ValidContexts": "medida"
    }
  ]
}
```

Esto deshabilitará la opción del menú contextual, a menos que se haya seleccionado exactamente una medida en el árbol.

## Reutilizando acciones personalizadas

La versión 2,7 introduce un nuevo método de script `CustomAction(...)`, que puede llamarse para invocar acciones personalizadas guardadas previamente. Puede usar este método como un método independiente (similar a `Output(...)`), o puede usarlo como un método de extensión en cualquier conjunto de objetos:

```csharp
// Ejecuta "My custom action" sobre la selección actual:
CustomAction("My custom action");                

// Ejecuta "My custom action" sobre todas las tablas del modelo:
CustomAction(Model.Tables, "My custom action");

// Ejecuta "My custom action" sobre cada medida en la selección actual cuyo nombre empieza por "Sum":
Selected.Measures.Where(m => m.Name.StartsWith("Sum")).CustomAction("My custom action");
```

Tenga en cuenta que debe especificar el nombre completo de la acción personalizada, incluidos los nombres de las carpetas del menú contextual.

Si no se encuentra ninguna acción con el nombre indicado, se genera un error al ejecutar el script.
