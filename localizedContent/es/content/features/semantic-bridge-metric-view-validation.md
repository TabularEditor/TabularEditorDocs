---
uid: semantic-bridge-metric-view-validation
title: Validación de Metric View en Semantic Bridge
author: Greg Baldini
updated: 2026-07-01
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.25.0
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          none: true
        - edition: Enterprise
          full: true
---

# Validación de Semantic Bridge

<!--
SUMMARY: Describes the validation framework for Metric Views in the Semantic Bridge, including built-in validation rules, diagnostic messages (errors/warnings/info), and how validation integrates with the import workflow.
-->

Hay un marco de validación integrado en el Semantic Bridge que permite a los usuarios validar y definir reglas para comprobar una Metric View antes de importarla en Tabular.
Estos informes de diagnóstico se comparten en todas las etapas de la canalización de traducción,
desde la deserialización inicial de la Metric View hasta los errores al traducir a DAX y Tabular.

> [!NOTE]
> El Semantic Bridge está actualmente en versión preliminar pública, por lo que las interfaces pueden cambiar a medida que la funcionalidad madura.
> Por ahora, la única interfaz para la validación es a través de scripts de C#.

## Proceso de validación

Hay varias fases de validación

1. al deserializar YAML para comprobar que representa un Metric View válido
2. al actuar sobre el Metric View cargado
3. al traducir el Metric View a Tabular

La primera y la tercera son automáticas e internas del Semantic Bridge, pero en la segunda los usuarios pueden aportar sus propias reglas de validación.

La validación es el proceso de evaluar cada regla de validación de un conjunto sobre todos los objetos del Metric View.
Una regla de validación se define para aplicarse a un único tipo de objeto de Metric View; por ejemplo, un `Join` o un `Measure`.
Una vez completada la validación, se devuelven al usuario todos los diagnósticos de los incumplimientos de reglas para que actúe en consecuencia.

## Anatomía de una regla de validación

Todas las reglas de validación son instancias de [`IMetricViewValidationRule`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.Interfaces.IMetricViewValidationRule).
En lugar de profundizar en esa interfaz, es más fácil entender y trabajar con las reglas de validación mediante los métodos auxiliares:

- [`MakeValidationRuleForField`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.MakeValidationRuleForField%2A)
- [`MakeValidationRuleForJoin`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.MakeValidationRuleForJoin%2A)
- [`MakeValidationRuleForMeasure`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.MakeValidationRuleForMeasure%2A)
- [`MakeValidationRuleForView`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.MakeValidationRuleForView%2A)
- [`MakeValidationRule`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.MakeValidationRule%2A)

Las cuatro primeras son específicas para crear una regla para el tipo de objeto indicado en su nombre.
Ofrecen una interfaz simplificada en la que proporcionas:

- `name`: un nombre corto y único para identificar la regla
- `category`: útil para agrupar reglas similares, pero en última instancia es completamente opcional
- `message`: el texto que se mostrará en el mensaje de diagnóstico cuando se incumpla esta regla
- `isInvalid`: una función que tomará el objeto de Metric View como argumento y devolverá `true` si ese objeto no es válido

El nombre y la categoría están pensados para facilitar el trabajo con colecciones de reglas, como se hace en scripts de C# que utilizan reglas personalizadas.

Cada uno de estos métodos auxiliares también tiene una sobrecarga con un argumento final `minVersion`.
Este argumento acepta una cadena de versión, como "0.1" o "1.1".
Las reglas con `minVersion` establecido solo se evalúan para Metric Views con esa versión o superior.

Esto se entiende mejor con un ejemplo:

```csharp {compile}
// crear una regla para comprobar si hay guiones bajos en los nombres de los campos
var myRule = SemanticBridge.MetricView.MakeValidationRuleForField(
	"no_underscores",
	"naming",
	"No incluyas guiones bajos en los nombres de los campos. Usa nombres fáciles de leer con espacios.",
	(field) => field.Name.Contains('_')
	);
```

Esto crea una regla que se aplicará a todos los [`Field`s de la Metric View](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Field).
La regla se llama (irónicamente) "no_underscores".
Tiene la categoría "naming", para indicar que tiene que ver con cómo nombramos las cosas.
Los mensajes que verás cuando se infrinja la regla son: "No incluyas guiones bajos en los nombres de los campos. Use nombres fáciles de leer con espacios."
El último argumento define una función a la que se llamará para cada campo de Metric View del modelo; su cuerpo es una expresión booleana que devuelve `true` para un campo de Metric View con un guion bajo en su propiedad `Name`.

Aquí tienes un script completo que define una Metric View en línea y luego la deserializa y la valida, mostrando cómo se usa esta regla.

```csharp {run id=simple setup=none after=none output=true}
// crear una nueva Metric View sencilla
SemanticBridge.MetricView.Deserialize("""
    version: 1.1
    source: database.schema.table
    fields:
      - name: first_field
        expr: source.first_field
      - name: another field with no underscores
        expr: source.another_field_with_no_underscores
    """);

// crear una nueva regla de validación
var myRule = SemanticBridge.MetricView.MakeValidationRuleForField(
    "no_underscores",
    "naming",
    "No incluyas guiones bajos en los nombres de los campos. Usa nombres fáciles de leer con espacios.",
    (field) => field.Name.Contains('_')
    );

// ejecutar la validación con la regla definida arriba y mostrar los mensajes de diagnóstico
var sb = new System.Text.StringBuilder();
foreach (var d in SemanticBridge.MetricView.Validate([myRule]))
{
    sb.AppendLine($"[{d.Severity}] {d.Code} {d.Path}");
    sb.AppendLine($"    {d.Context} {d.Message}");
    sb.AppendLine();
}
Output(sb.ToString());
```

**Salida**

```
[Error] no_underscores Model.Fields["first_field"]
     No incluyas guiones bajos en los nombres de los campos. Usa nombres fáciles de leer con espacios.
```

Puedes ver que uno de los campos de Metric View tiene un guion bajo en su nombre.
Al ejecutar el script, verás un único mensaje de diagnóstico después de validar con la regla que definimos.
Puedes ver los detalles que se proporcionan en el mensaje de diagnóstico:

- Código: el nombre que le das a tu regla
- Contexto: estos métodos auxiliares no se encargan de establecerlo
- Mensaje: el mensaje que definiste en la regla
- Ruta: una representación de dónde se encuentra ese objeto en la Vista de métricas
- Gravedad: se establece en Error de forma predeterminada con estos métodos auxiliares

![salida de un campo que infringe la regla de validación](~/content/assets/images/features/semantic-bridge/semantic-bridge-metric-view-validation.png)

Si quieres más control sobre el mensaje de diagnóstico y más flexibilidad en la función de validación, puedes usar `MakeValidationRule` mencionado arriba para crear una regla de validación contextual.

```csharp {run id=contextual setup=none after=none output=true}
// necesario para usar el modelo de objetos de Metric View
// alias para evitar conflictos con objetos TOM que tienen el mismo nombre
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

// crear una nueva Metric View sencilla
SemanticBridge.MetricView.Deserialize("""
    version: 1.1
    source: database.schema.table
    fields:
      - name: customer
        expr: source.customer_id
      - name: repeat_customer
        expr: source.customer_id
    """);

// crear una nueva regla de validación
var myRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Field>(
    "no_aliased_fields",
    "modeling",
    (field, context) =>
    {
        var original = context.FieldNames.FirstOrDefault(seen => field.View.Fields[seen].Expr == field.Expr);
        return original == null
            ? []
            : [context.MakeError(
                "field_alias",
                $"El campo '{field.Name}' reutiliza la expresión de origen '{field.Expr}', que ya usa el campo '{original}'.",
                field)];
    });

// ejecutar la validación con la regla definida arriba y mostrar los mensajes de diagnóstico
var sb = new System.Text.StringBuilder();
foreach (var d in SemanticBridge.MetricView.Validate([myRule]))
{
    sb.AppendLine($"[{d.Severity}] {d.Code} {d.Path}");
    sb.AppendLine($"    {d.Context} {d.Message}");
    sb.AppendLine();
}
Output(sb.ToString());
```

**Salida**

```
[Error] field_alias Model.Fields["repeat_customer"]
     El campo 'repeat_customer' reutiliza la expresión de origen 'source.customer_id', que ya usa el campo 'customer'.
```

Este método auxiliar requiere que pases el tipo de objeto como parámetro de tipo, y ahora la función de validación es una función de dos parámetros, definida con la firma `(metricViewObject, context)`.
El primer parámetro es el objeto de Metric View para el que se evalúa la regla.
El segundo parámetro es un [`IReadOnlyValidationContext`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.Validation.IReadOnlyValidationContext).
Este objeto de contexto contiene colecciones con los nombres de los objetos que ya se han comprobado;
lo que significa que podemos usarlo para inspeccionar solo los objetos ya validados.
El objeto de contexto también incluye métodos auxiliares para crear nuevos mensajes de diagnóstico;
la ventaja es que tus mensajes no tienen por qué ser cadenas codificadas de forma estática,
sino que pueden incluir propiedades del objeto que estás comprobando.
Usamos `MakeError`, y el objeto de contexto también incluye `MakeWarning`.
En este ejemplo puedes ver que incluimos en los mensajes tanto el campo conflictivo como el campo del que es un alias.

![salida de un campo que infringe la regla de validación más compleja](~/content/assets/images/features/semantic-bridge/semantic-bridge-metric-view-validation2.png)

## Buenas prácticas para reglas de validación

Es recomendable crear muchas reglas simples, en lugar de menos reglas más complejas.
El proceso de validación es muy ligero, así que no hay problemas de rendimiento por tener muchas reglas.
Por ejemplo, si quieres asegurarte de que los nombres de los campos de Metric View no estén en `camelCased`, ni en `kebab-cased` ni en `snake_cased`, es mejor crear tres reglas independientes en lugar de intentar comprobar cada una de esas condiciones en una sola regla.
Esto permite que cada regla sea simple y que los mensajes sean muy específicos y, por tanto, más fáciles de solucionar.

En general, cuando ya tienes una regla que detecta un problema concreto, es mejor dejarla tal cual en vez de editarla.
Si ves que a la regla le falta alguna condición que te gustaría detectar, solo tienes que añadir una regla nueva, pequeña y simple para cubrir esa condición.

Puedes guardar muchas reglas distintas en un C# Script para reutilizarlas con diferentes Metric Views.
Como [una Metric View cargada es accesible desde varios scripts](xref:semantic-bridge-metric-view-object-model#loading-and-accessing-the-metric-view), puedes guardar varios archivos C# Script que solo definan reglas y luego llamar a `SemanticBridge.MetricView.Validate` y reutilizar esos scripts de validación fácilmente.
Mira la imagen de abajo: el script de la izquierda, "deserialize-mv.csx", ya se ha ejecutado para cargar una Metric View en Tabular Editor.
Después, se ejecuta el segundo script, a la derecha, "run-rules.csx", para validar.
Este segundo script podría ser uno que tengas siempre a mano para todas tus Metric Views.

![salida de un campo que infringe la regla de validación más compleja](~/content/assets/images/features/semantic-bridge/semantic-bridge-metric-view-validation3.png)

Los scripts se copian a continuación por comodidad, pero no son más que reorganizaciones de los scripts que vimos anteriormente.

**"deserialize-mv.csx"**

```csharp {run id=deserialize setup=none after=none output=false}
// crear una nueva Metric View sencilla
SemanticBridge.MetricView.Deserialize("""
    version: 1.1
    source: database.schema.table
    fields:
      - name: customer
        expr: source.customer_id
      - name: repeat_customer
        expr: source.customer_id
    """);
```

**"run-rules.csx"**

```csharp {run id=run-rules setup=none after=deserialize output=true}
// necesario para usar el modelo de objetos de Metric View
// uso de alias para evitar conflictos con objetos TOM del mismo nombre
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

// crear una regla de validación sencilla
var simpleRule = SemanticBridge.MetricView.MakeValidationRuleForField(
    "no_underscores",
    "naming",
    "No incluyas guiones bajos en los nombres de los campos. Usa nombres claros con espacios.",
    (field) => field.Name.Contains('_')
    );

// crear una regla de validación contextual
var contextualRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Field>(
    "no_aliased_fields",
    "modeling",
    (field, context) =>
    {
        var original = context.FieldNames.FirstOrDefault(seen => field.View.Fields[seen].Expr == field.Expr);
        return original == null
            ? []
            : [context.MakeError(
                "field_alias",
                $"El campo '{field.Name}' reutiliza la expresión de origen '{field.Expr}', ya utilizada por el campo '{original}'.",
                field)];
    });

// ejecutar la validación con las reglas definidas arriba y mostrar los mensajes de diagnóstico
var sb = new System.Text.StringBuilder();
foreach (var d in SemanticBridge.MetricView.Validate([simpleRule, contextualRule]))
{
    sb.AppendLine($"[{d.Severity}] {d.Code} {d.Path}");
    sb.AppendLine($"    {d.Context} {d.Message}");
    sb.AppendLine();
}
Output(sb.ToString());
```

**Salida**

```
[Error] no_underscores Model.Fields["repeat_customer"]
     No incluyas guiones bajos en los nombres de los campos. Usa nombres claros con espacios.

[Error] field_alias Model.Fields["repeat_customer"]
     El campo 'repeat_customer' reutiliza la expresión de origen 'source.customer_id', ya utilizada por el campo 'customer'.
```

## Referencias

- @semantic-bridge-metric-view-object-model
- @semantic-bridge-metric-view-fields-and-dimensions
- @semantic-bridge-how-tos
