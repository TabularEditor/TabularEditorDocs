---
uid: semantic-bridge-metric-view-validation
title: Validación de Metric View en Semantic Bridge
author: Greg Baldini
updated: 2026-09-14
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
Estos Reports de diagnóstico se comparten en todas las etapas de la canalización de traducción,
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

## Códigos de diagnóstico integrados

La primera y la tercera fases generan sus propios diagnósticos, con códigos definidos por Semantic Bridge. Llegan del mismo modo que los diagnósticos de tus propias reglas: cada uno incluye `Severity`, `Code`, `Path`, `Context` y `Message`.

La gravedad puede ser `Error`, `Warning` o `Information`. Un `Error` detiene la operación. Un `Warning` significa que Semantic Bridge siguió adelante después de tomar una decisión por ti, y te indica cuál fue esa decisión.

### Lectura del YAML

| Código                                                             | Gravedad    | Se genera cuando                                                                                                                                                                                                       |
| ------------------------------------------------------------------ | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `METRIC_VIEW_FIELDS_AND_DIMENSIONS_BOTH_PRESENT`                   | Error       | La vista declara tanto `fields:` como `dimensions:` en el nivel superior. Son alias entre sí; usa solo uno                                                                                             |
| `METRIC_VIEW_DUPLICATE_NAME`                                       | Error       | Dos objetos de la misma colección declaran el mismo nombre. La coincidencia no distingue entre mayúsculas y minúsculas                                                                                 |
| `METRIC_VIEW_DEPRECATED_DIMENSIONS_KEYWORD`                        | Advertencia | Una vista de la especificación YAML 1.1 o posterior usa `dimensions:`. `fields:` es la forma canónica; ambas opciones siguen funcionando. Se lanza una vez por archivo |
| `METRIC_VIEW_FIELDS_KEYWORD_PRE_V11`                               | Advertencia | Una vista anterior a la especificación 1.1 usa `fields:`. `dimensions:` es la forma canónica en esa versión; se aceptan ambas opciones                                                 |
| `MISSING_VERSION`                                                  | Advertencia | El YAML no tiene la propiedad `version`. Se asume un valor predeterminado                                                                                                                              |
| `UNKNOWN_JOIN_CARDINALITY`                                         | Advertencia | En un join se declara una cardinalidad distinta de `many_to_one` o `one_to_many`. Se asume `many_to_one`                                                                                               |
| `MISSING_FORMAT_TYPE`, `UNKNOWN_FORMAT_TYPE`                       | Advertencia | Un formato no tiene tipo o tiene uno que Bridge no reconoce. El formato se ignora                                                                                                                      |
| `MISSING_DATE_FORMAT`, `UNKNOWN_DATE_FORMAT`                       | Advertencia | El valor predeterminado es `year_month_day`                                                                                                                                                                            |
| `MISSING_TIME_FORMAT`, `UNKNOWN_TIME_FORMAT`                       | Advertencia | El valor predeterminado es `locale_hour_minute_second`                                                                                                                                                                 |
| `MISSING_DECIMAL_TYPE`, `UNKNOWN_DECIMAL_TYPE`                     | Advertencia | El valor predeterminado es `all`                                                                                                                                                                                       |
| `MISSING_SEMIADDITIVE`, `UNKNOWN_SEMIADDITIVE`                     | Advertencia | El valor predeterminado es `Last`                                                                                                                                                                                      |
| `MISSING_MATERIALIZATION_MODE`, `UNKNOWN_MATERIALIZATION_MODE`     | Advertencia | El valor predeterminado es `relaxed`                                                                                                                                                                                   |
| `MISSING_MATERIALIZED_VIEW_TYPE`, `UNKNOWN_MATERIALIZED_VIEW_TYPE` | Advertencia | El valor predeterminado es `unaggregated`                                                                                                                                                                              |
| `VERSION_MISMATCH`                                                 | Advertencia | La versión declarada no coincide con la que se encontró                                                                                                                                                                |

### Mapeo de la vista de métricas

Todos los códigos de este grupo son `Warning`, salvo donde se indique lo contrario. El objeto se sigue creando, pero algo no se conservó intacto.

| Código                           | Se genera cuando                                                                                                                                                                                                                                                                         |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `JOIN_ON_EMPTY`                  | Un `join` no tiene cláusula `on`. La dimensión y su origen se crean, pero no se conecta ningún par de clave externa / clave primaria                                                                                                                                     |
| `JOIN_ON_UNRECOGNIZED`           | La cláusula `on` de un `join` no es una igualdad reconocida entre una columna aguas arriba y una columna de dimensión. De nuevo, no hay ningún par de claves                                                                                                             |
| `JOIN_ON_NO_SOURCE_SIDE`         | La cláusula `on` de un `join` no empareja ninguna columna aguas arriba. De nuevo, no hay ningún par de claves                                                                                                                                                            |
| `ONE_TO_MANY_JOIN_UNTRANSLATED`  | Un `join` declara `cardinality: one_to_many`, que el traductor no puede modelar. _Se omite la relación_, por lo que las medidas que hacen referencia a sus columnas pueden ser incorrectas o estar vacías; revísalas manualmente                                         |
| `DUPLICATE_JOIN_DIMENSION`       | Un join crearía una dimensión cuyo nombre colisiona con el de otra existente. Se omite el duplicado. Los nombres de los joins deben ser únicos en toda la vista                                                                                          |
| `UNRESOLVED_DIMENSION_REFERENCE` | Una referencia apunta a una dimensión que no está declarada como un join. Se genera un campo derivado de relleno, conservando la referencia original                                                                                                                     |
| `STRUCT_REFERENCE_UNSUPPORTED`   | Una dimensión hace referencia a un valor struct de fila completa o anidado, que no tiene un equivalente de columna en Tabular. Se genera la columna, pero no se resolverá al actualizar                                                                                  |
| `FORMAT_TRANSLATION_LOSSY`       | Una especificación de formato de Databricks no puede expresarse exactamente como una cadena de formato de Tabular                                                                                                                                                                        |
| `FIELD_COLLISION_RENAME`         | _Información._ Un nombre de campo generado entró en conflicto con una dimensión declarada por el usuario, por lo que se cambió el nombre del campo. Permanece en el modelo y sigue sirviendo de base para cualquier relación que hiciera referencia a él |
| `MEASURE_REF_OUT_OF_CONTEXT`     | Una referencia `MEASURE(...)` aparece en una expresión que no es una medida                                                                                                                                                                                                              |
| `UNRESOLVED_MEASURE_REFERENCE`   | Una referencia `MEASURE(...)` no nombra ninguna medida declarada. Se usa el texto fuente literal                                                                                                                                                                         |
| `FIELD_CONFIGURATION_UNEXPECTED` | Un campo tenía una configuración que el analizador no pudo clasificar y, por seguridad, se importó como un campo de hechos derivado. Comprueba el resultado                                                                                                              |

### Diagnóstico de expresiones, por tipo de objeto

Los problemas de expresión se informan en el Report con su propio código según el tipo de objeto, para que puedas ver de un vistazo qué tipo de objeto falló:

| Tipo   | No se pudo traducir               | No se pudo analizar              |
| ------ | --------------------------------- | -------------------------------- |
| Campo  | `FIELD_EXPRESSION_UNTRANSLATED`   | `FIELD_EXPRESSION_PARSE_ERROR`   |
| Medida | `MEASURE_EXPRESSION_UNTRANSLATED` | `MEASURE_EXPRESSION_PARSE_ERROR` |
| Unión  | `JOIN_EXPRESSION_UNTRANSLATED`    | `JOIN_EXPRESSION_PARSE_ERROR`    |

Se entendió una expresión _sin traducir_, pero usa una construcción que no tiene equivalente en DAX; el original se conserva como comentario. Un _error de análisis_ significa que no se pudo leer la expresión en absoluto; además, el `Context` del diagnóstico incluye el mensaje del propio analizador.

### Emisión a Tabular

| Código                             | Se produce cuando                                                                                                                                                   |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `REFERENCE_FIELD_INVALID_SOURCE`   | Un campo de referencia apunta a un id de campo inexistente o que no corresponde a un campo de origen. Se genera una columna de marcador de posición |
| `DERIVED_FIELD_UNTRANSLATED`       | La expresión de un campo derivado no se pudo traducir a DAX. El original se conserva como comentario                                                |
| `DERIVED_FIELD_NO_EXPRESSION`      | Un campo derivado no tiene expresión                                                                                                                                |
| `MEASURE_UNTRANSLATED`             | No se pudo traducir la expresión de una medida. El original se conserva como comentario                                                             |
| `CALCULATED_MEASURE_NO_EXPRESSION` | Una medida calculada no tiene expresión de origen. Se genera un cuerpo de marcador de posición                                                      |
| `MEASURE_UNRESOLVED_AT_EMIT`       | Una medida hace referencia a una medida que no se ha emitido. Vuelve a la fuente literal                                                            |
| `TABLE_UNRESOLVED_AT_EMIT`         | Una medida hace referencia a una tabla que no se ha emitido. Vuelve a la fuente literal                                                             |
| `COLUMN_UNRESOLVED_AT_EMIT`        | Una medida hace referencia a un campo que no se ha emitido como columna. Vuelve a la fuente literal                                                 |
| `MEASURE_WINDOW_UNSUPPORTED`       | Una medida usa una especificación de ventana no admitida. Se deja inerte, y la definición original se conserva como comentario                      |

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
Las reglas con `minVersion` definido solo se evalúan para las Metric Views cuya versión sea igual o superior a esa versión.

Esto se entiende mejor con un ejemplo:

```csharp {compile}
// create a rule to check for underscores in field names
var myRule = SemanticBridge.MetricView.MakeValidationRuleForField(
	"no_underscores",
	"naming",
	"Do not include underscores in field names. Use user-friendly names with spaces.",
	(field) => field.Name.Contains('_')
	);
```

Esto crea una regla que se aplicará a todos los [`Field`s de Metric View](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Field).
La regla se llama (irónicamente) "no_underscores".
Tiene la categoría "naming", para indicar que tiene que ver con cómo nombramos las cosas.
El mensaje que verás cuando se incumpla la regla es: "No incluyas guiones bajos en los nombres de los campos." Use nombres fáciles de leer con espacios."
El último argumento define una función a la que se llamará para cada campo de Metric View del modelo; su cuerpo es una expresión booleana que devuelve `true` para un campo de Metric View con un guion bajo en su propiedad `Name`.

Aquí tienes un script completo que define una Metric View en línea y luego la deserializa y la valida, mostrando cómo se usa esta regla.

```csharp {run id=simple setup=none after=none output=true}
// create a new simple Metric View
SemanticBridge.MetricView.Deserialize("""
    version: 1.1
    source: database.schema.table
    fields:
      - name: first_field
        expr: source.first_field
      - name: another field with no underscores
        expr: source.another_field_with_no_underscores
    """);

// create a new validation rule
var myRule = SemanticBridge.MetricView.MakeValidationRuleForField(
    "no_underscores",
    "naming",
    "Do not include underscores in field names. Use user-friendly names with spaces.",
    (field) => field.Name.Contains('_')
    );

// run validation with the rule defined above and output the diagnostic messages
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
     Do not include underscores in field names. Use user-friendly names with spaces.
```

Puedes ver que uno de los campos de Metric View tiene un guion bajo en su nombre.
Al ejecutar el script, verás un único mensaje de diagnóstico después de validar con la regla que definimos.
Puedes ver los detalles que se proporcionan en el mensaje de diagnóstico:

- Code: el nombre que asignas a tu regla
- Context: estos métodos auxiliares no lo establecen
- Mensaje: el mensaje que definiste en la regla
- Ruta: una representación de dónde se encuentra ese objeto en la Vista de métricas
- Gravedad: se establece en Error de forma predeterminada con estos métodos auxiliares

![salida de un campo que infringe la regla de validación](~/content/assets/images/features/semantic-bridge/semantic-bridge-metric-view-validation.png)

Si quieres más control sobre el mensaje de diagnóstico y más flexibilidad en la función de validación, puedes usar `MakeValidationRule` mencionado arriba para crear una regla de validación contextual.

```csharp {run id=contextual setup=none after=none output=true}
// necessary to use the Metric View object model
// aliasing to avoid conflicts with same-named TOM objects
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

// create a new simple Metric View
SemanticBridge.MetricView.Deserialize("""
    version: 1.1
    source: database.schema.table
    fields:
      - name: customer
        expr: source.customer_id
      - name: repeat_customer
        expr: source.customer_id
    """);

// create a new validation rule
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
                $"Field '{field.Name}' reuses source expression '{field.Expr}', already used by field '{original}'.",
                field)];
    });

// run validation with the rule defined above and output the diagnostic messages
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
     Field 'repeat_customer' reuses source expression 'source.customer_id', already used by field 'customer'.
```

Este método auxiliar requiere que pases el tipo de objeto como parámetro de tipo, y ahora la función de validación es una función de dos parámetros, definida con la firma `(metricViewObject, context)`.
El primer parámetro es el objeto de Metric View para el que se evalúa la regla.
El segundo parámetro es un [`IReadOnlyValidationContext`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.Validation.IReadOnlyValidationContext).
Este objeto de contexto contiene colecciones con los nombres de los objetos ya comprobados; esto significa que podemos usarlo para inspeccionar solo los objetos ya validados.
El objeto de contexto también tiene métodos auxiliares para crear un nuevo mensaje de diagnóstico; la ventaja aquí es que tu mensaje no tiene por qué estar codificado como una cadena fija, sino que puede incluir propiedades del objeto que estás comprobando.
Usamos `MakeError` y el objeto de contexto también incluye `MakeWarning`.
Puedes ver en este ejemplo que incluimos en el mensaje tanto el campo que incumple la regla como el campo al que sirve de alias.

![salida de un campo que infringe la regla de validación más compleja](~/content/assets/images/features/semantic-bridge/semantic-bridge-metric-view-validation2.png)

## Buenas prácticas para reglas de validación

Es recomendable crear muchas reglas simples, en lugar de menos reglas más complejas.
El proceso de validación es muy ligero, así que no hay problemas de rendimiento por tener muchas reglas.
Por ejemplo, si quieres asegurarte de que los nombres de los campos de Metric View no sean `camelCased`, `kebab-cased` ni `snake_cased`, es mejor crear tres reglas independientes en lugar de intentar comprobar todas esas condiciones en una sola regla.
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
// create a new simple Metric View
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
// necessary to use the Metric View object model
// aliasing to avoid conflicts with same-named TOM objects
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

//create a simple validation rule
var simpleRule = SemanticBridge.MetricView.MakeValidationRuleForField(
    "no_underscores",
    "naming",
    "Do not include underscores in field names. Use user-friendly names with spaces.",
    (field) => field.Name.Contains('_')
    );

// create a contextual validation rule
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
                $"Field '{field.Name}' reuses source expression '{field.Expr}', already used by field '{original}'.",
                field)];
    });

// run validation with the rules defined above and output the diagnostic messages
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
     Do not include underscores in field names. Use user-friendly names with spaces.

[Error] field_alias Model.Fields["repeat_customer"]
     Field 'repeat_customer' reuses source expression 'source.customer_id', already used by field 'customer'.
```

## Referencias

- @semantic-bridge-metric-view-object-model
- @semantic-bridge-metric-view-fields-and-dimensions
- @semantic-bridge-how-tos
