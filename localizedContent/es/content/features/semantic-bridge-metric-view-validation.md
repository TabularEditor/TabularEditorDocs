---
uid: semantic-bridge-metric-view-validation
title: Validación de Metric View en Semantic Bridge
author: Greg Baldini
updated: 2025-01-23
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
Esta validación se comparte en todas las etapas de la canalización de traducción, desde la deserialización inicial del Metric View hasta la detección de errores al traducir a DAX y Tabular.

> [!NOTE]
> El Semantic Bridge se encuentra actualmente en su fase de MVP, por lo que las interfaces pueden cambiar a medida que la funcionalidad madure.
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

Las reglas de validación son todas instancias de [`IMetricViewValidationRule`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.Interfaces.IMetricViewValidationRule.html).
En lugar de profundizar en esa interfaz, es más fácil entender y trabajar con las reglas de validación mediante los métodos auxiliares:

- [`MakeValidationRuleForDimension`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_MakeValidationRuleForDimension_System_String_System_String_System_String_System_Func_TabularEditor_SemanticBridge_Platforms_Databricks_MetricView_Dimension_System_Boolean__)
- [`MakeValidationRuleForJoin`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_MakeValidationRuleForJoin_System_String_System_String_System_String_System_Func_TabularEditor_SemanticBridge_Platforms_Databricks_MetricView_Join_System_Boolean__)
- [`MakeValidationRuleForMeasure`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_MakeValidationRuleForMeasure_System_String_System_String_System_String_System_Func_TabularEditor_SemanticBridge_Platforms_Databricks_MetricView_Measure_System_Boolean__)
- [`MakeValidationRuleForView`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_MakeValidationRuleForView_System_String_System_String_System_String_System_Func_TabularEditor_SemanticBridge_Platforms_Databricks_MetricView_View_System_Boolean__)
- [`MakeValidationRule`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_MakeValidationRule__1_System_String_System_String_System_Func___0_TabularEditor_SemanticBridge_Platforms_Databricks_Validation_IReadOnlyValidationContext_System_Collections_Generic_IEnumerable_TabularEditor_SemanticBridge_Orchestration_DiagnosticMessage___)

Las cuatro primeras son específicas para crear una regla para el tipo de objeto indicado en su nombre.
Ofrecen una interfaz simplificada en la que proporcionas:

- `name`: un nombre corto y único para identificar la regla
- `category`: útil para agrupar reglas similares, pero en última instancia es completamente opcional
- `message`: el texto que se mostrará en el mensaje de diagnóstico cuando se incumpla esta regla
- `isInvalid`: una función que tomará el objeto de Metric View como argumento y devolverá `true` si ese objeto no es válido

El nombre y la categoría están pensados para facilitar el trabajo con colecciones de reglas, como se hace en scripts de C# que utilizan reglas personalizadas.

Esto se entiende mejor con un ejemplo:

```csharp
// crear una regla para comprobar si hay guiones bajos en los nombres de las dimensiones
var myRule = SemanticBridge.MetricView.MakeValidationRuleForDimension(
	"no_underscores",
	"naming",
	"No se deben incluir guiones bajos en los nombres de las dimensiones. Se deben usar nombres fáciles de leer con espacios.",
	(dimension) => dimension.Name.Contains('_')
	);
```

Esto crea una regla que se aplicará a todas las [`Dimension`s de Metric View](/api/TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Dimension.html).
La regla se llama (irónicamente) "no_underscores".
Tiene la categoría "naming", para indicar que tiene que ver con cómo nombramos las cosas.
El mensaje que verá cuando se incumpla la regla es: "No incluya guiones bajos en los nombres de las dimensiones. Use nombres fáciles de leer con espacios."
El último argumento define una función a la que se llamará para cada dimensión de Metric View del modelo; su cuerpo es una expresión booleana que devuelve `true` para una dimensión de Metric View con un guion bajo en su propiedad `Name`.

Aquí tienes un script completo que define una Metric View en línea y luego la deserializa y la valida, mostrando cómo se usa esta regla.

```csharp
// crear una nueva Metric View simple
SemanticBridge.MetricView.Deserialize("""
    version: 0.1
    source: database.schema.table
    dimensions:
      - name: first_field
        expr: source.first_field
      - name: another field with no underscores
        expr: source.another_field_with_no_underscores
    """);

// crear una nueva regla de validación
var myRule = SemanticBridge.MetricView.MakeValidationRuleForDimension(
    "no_underscores",
    "naming",
    "No incluya guiones bajos en los nombres de las dimensiones. Use nombres fáciles de leer con espacios.",
    (dimension) => dimension.Name.Contains('_')
    );

// ejecutar la validación con la regla definida arriba e imprimir los mensajes de diagnóstico
Output(SemanticBridge.MetricView.Validate([myRule]));
```

Puedes ver que uno de los campos definidos como dimensión de Metric View tiene un guion bajo en su nombre.
Al ejecutar el script, verás un único mensaje de diagnóstico después de validar con la regla que definimos.
Puedes ver los detalles que se proporcionan en el mensaje de diagnóstico:

- Código, Contexto: no se utilizan cuando usas uno de estos métodos auxiliares para crear la regla
- Mensaje: el mensaje que definiste en la regla
- Ruta: una representación de dónde se encuentra ese objeto en la Vista de métricas
- Gravedad: se establece en Error de forma predeterminada con estos métodos auxiliares

![salida de un campo que infringe la regla de validación](~/content/assets/images/features/semantic-bridge/semantic-bridge-metric-view-validation.png)

Si quieres más control sobre el mensaje de diagnóstico y más flexibilidad en la función de validación, puedes usar `MakeValidationRule` mencionado arriba para crear una regla de validación contextual.

```csharp
// necesario para usar el modelo de objetos de Metric View
// asignación de alias para evitar conflictos con objetos TOM con el mismo nombre
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

// crear una nueva Metric View sencilla
SemanticBridge.MetricView.Deserialize("""
    version: 0.1
    source: database.schema.table
    dimensions:
      - name: same_field
        expr: source.same_field
      - name: same_field
        expr: source.same_field
    """);

// crear una nueva regla de validación
var myRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Dimension>(
    "no_duplicate_dimensions",
    "naming",
    (dimension, context) =>
        context.DimensionNames.Contains(dimension.Name)
            ? [context.MakeError($"{dimension.Name} aparece más de una vez como dimensión")]
            : []
    );

// ejecutar la validación con la regla definida anteriormente y mostrar los mensajes de diagnóstico
Output(SemanticBridge.MetricView.Validate([myRule]));
```

Este método auxiliar requiere que pases el tipo de objeto como parámetro de tipo, y ahora la función de validación es una función de dos parámetros, definida con la firma `(objectType, context)`.
El primer parámetro es el objeto de Metric View para el que se evalúa la regla.
El segundo parámetro es un [`IReadOnlyValidationContext`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.Validation.IReadOnlyValidationContext.html).
Este objeto de contexto contiene colecciones con los nombres de los objetos ya comprobados; esto lo hace útil para detectar nombres duplicados.
El objeto de contexto también incluye un método auxiliar para crear un nuevo mensaje de diagnóstico; la ventaja es que el mensaje no tiene por qué ser una cadena codificada de forma fija, sino que puede incluir propiedades del objeto que estás comprobando.
En este ejemplo puedes ver que incluimos en el mensaje el nombre duplicado de la dimensión de Metric View.

![salida de un campo que infringe la regla de validación más compleja](~/content/assets/images/features/semantic-bridge/semantic-bridge-metric-view-validation2.png)

## Buenas prácticas para reglas de validación

Es recomendable crear muchas reglas simples, en lugar de menos reglas más complejas.
El proceso de validación es muy ligero, así que no hay problemas de rendimiento por tener muchas reglas.
Por ejemplo, si quieres asegurarte de que los nombres de las dimensiones de Metric View no estén en `camelCased`, ni en `kebab-cased` ni en `snake_cased`, es mejor crear tres reglas independientes, en lugar de intentar comprobar todas esas condiciones en una sola regla.
Esto permite que cada regla sea simple y que los mensajes sean muy específicos y, por tanto, más fáciles de solucionar.

En general, cuando ya tienes una regla que detecta un problema concreto, es mejor dejarla tal cual en vez de editarla.
Si ves que a la regla le falta alguna condición que te gustaría detectar, solo tienes que añadir una regla nueva, pequeña y simple para cubrir esa condición.

Puedes guardar muchas reglas distintas en un C# Script para reutilizarlas con diferentes Metric Views.
Como [una Metric View cargada es accesible desde varios scripts](xref:semantic-bridge-metric-view-object-model#loading-and-accessing-the-metric-view), puedes guardar varios archivos C# Script que solo definan reglas y luego llamar a `SemanticBridge.MetricView.Validate` y reutilizar esos scripts de validación fácilmente.
Mira la imagen de abajo: el script de la izquierda, "load-mv.csx", ya se ha ejecutado para cargar una Metric View en Tabular Editor.
Después, se ejecuta el segundo script, a la derecha, "run-rules.csx", para validar.
Este segundo script podría ser uno que tengas siempre a mano para todas tus Metric Views.

![salida de un campo que infringe la regla de validación más compleja](~/content/assets/images/features/semantic-bridge/semantic-bridge-metric-view-validation3.png)

Los scripts se copian a continuación por comodidad, pero no son más que reorganizaciones de los scripts que vimos anteriormente.

**"load-mv.csx"**

```csharp
// crear una nueva Metric View simple
SemanticBridge.MetricView.Deserialize("""
    version: 0.1
    source: database.schema.table
    dimensions:
      - name: same_field
        expr: source.same_field
      - name: same_field
        expr: source.same_field
    """);
```

**"run-rules.csx"**

```csharp
// necesario para usar el modelo de objetos de Metric View
// uso de alias para evitar conflictos con objetos TOM del mismo nombre
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

// crear una regla de validación sencilla
var simpleRule = SemanticBridge.MetricView.MakeValidationRuleForDimension(
    "no_underscores",
    "naming",
    "No incluya guiones bajos en los nombres de las dimensiones. Use nombres fáciles de usar con espacios.",
    (dimension) => dimension.Name.Contains('_')
    );

// crear una regla de validación contextual
var contextualRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Dimension>(
    "no_duplicate_dimensions",
    "naming",
    (dimension, context) =>
        context.DimensionNames.Contains(dimension.Name)
            ? [context.MakeError($"{dimension.Name} aparece más de una vez como dimensión")]
            : []
    );

// ejecutar la validación con las reglas definidas anteriormente y generar los mensajes de diagnóstico
Output(SemanticBridge.MetricView.Validate([simpleRule, contextualRule]));
```

## Referencias

- @semantic-bridge-how-tos
