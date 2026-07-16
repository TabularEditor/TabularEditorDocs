---
uid: semantic-bridge-metric-view-fields-and-dimensions
title: Campos y dimensiones en las vistas de métricas
author: Greg Baldini
updated: 2026-06-25
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.26.2
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          none: true
        - edition: Enterprise
          full: true
---

# Campos y dimensiones en las vistas de métricas

<!--
SUMMARY: Explains the Databricks Metric View `dimensions` -> `fields` keyword rename and the
matching Semantic Bridge C# API rename (Dimension -> Field): what changed, that the old names
still work, migration guidance, and what Tabular Editor emits on round-trip.
-->

En la primavera de 2026, la especificación de Metric View redefinió una clave canónica de nivel superior en la especificación YAML de Metric View, pasando de `dimensions` (ahora en desuso) a `fields`.
Ambos términos se refieren al conjunto de columnas —ya sea como referencias directas a columnas de origen o definidas mediante una expresión SQL— disponible para consultar en la Metric View.
[La documentación indica que es preferible usar `fields`, pero ambos términos siguen siendo válidos](https://learn.microsoft.com/azure/databricks/business-semantics/metric-views/yaml-reference#dimensions).
Hemos actualizado el modelo de objetos de Metric View en Semantic Bridge para adaptarlo a este cambio.
La serialización y la deserialización siguen funcionando con cualquiera de las dos claves, conforme a la especificación de Metric View.
Ofrecemos capas de compatibilidad con versiones anteriores en el modelo de objetos para los antiguos nombres asociados a "dimension".
Quienes usen el modelo de objetos en C# Scripts deberían migrar a los nombres asociados a "field" cuando puedan.

**A quién afecta esto**: cualquiera que escriba YAML de Metric View a mano, cualquiera que use el modelo de objetos de Metric View en C# Scripts en Tabular Editor.

## Control de versiones

Este cambio se produjo después de publicarse la especificación v1.1, y sin que se publicara una nueva versión de la especificación.
Por ello, adoptamos un enfoque conservador en el Semantic Bridge.
Consideramos `dimensions` el valor predeterminado para las Metric Views v0.1 y v1.1.
En el futuro, trataremos `fields` como valor predeterminado para cualquier Metric View de una versión más reciente.
Esto se debe a la cautela y al deseo de ofrecer la máxima interoperabilidad con otras herramientas que quizá no estén al día con la última especificación publicada de Metric View.

## Serialización y deserialización

Según la [documentación de Metric View](https://learn.microsoft.com/azure/databricks/business-semantics/metric-views/yaml-reference#dimensions), ambas claves siguen siendo válidas para la serialización.

| El YAML de origen utiliza | Versión                                       | La deserialización tiene éxito | Se emite una advertencia al deserializar                                | Se vuelve a serializar con    |
| ------------------------- | --------------------------------------------- | ------------------------------ | ----------------------------------------------------------------------- | ----------------------------- |
| `fields`                  | <1.1 | sí                             | sí                                                                      | `fields`                      |
| `dimensions`              | <1.1 | sí                             | no                                                                      | `dimensiones`                 |
| ninguno de los dos        | <1.1 | sí                             | no                                                                      | `dimensiones`                 |
| `campos`                  | 1.1                           | sí                             | no                                                                      | `campos`                      |
| `dimensiones`             | 1.1                           | sí                             | sí                                                                      | `dimensiones`                 |
| ninguno de los dos        | 1.1                           | sí                             | no                                                                      | `dimensiones`                 |
| `campos`                  | > 1.1                         | sí                             | no                                                                      | `fields`                      |
| `dimensions`              | > 1.1                         | sí                             | sí                                                                      | `dimensions`                  |
| ninguno de los dos        | > 1.1                         | sí                             | no                                                                      | `fields`                      |
| ambos                     | cualquiera                                    | no                             | sí (error: falla la deserialización) | n/a, falla la deserialización |

Seguiremos admitiendo ambas palabras clave en todas las versiones de Metric View, salvo que una futura actualización de la especificación indique lo contrario.
Puedes seguir usando libremente cualquiera de ellas, según prefieras, teniendo en cuenta las notas anteriores sobre las advertencias y los valores predeterminados para la serialización y la deserialización.

Quizá notes que mostramos una advertencia sobre `dimensions` en un Metric View v1.1 y que, además, elegimos `dimensions` como valor predeterminado si no se proporciona ninguna de las dos para ese mismo v1.1.
Este es nuestro valor predeterminado conservador porque `fields` se introdujo como opción preferida a mitad de la versión 1.1.
La advertencia está en línea con la documentación de Metric View, que indica que `fields` debe considerarse el valor predeterminado.
El valor predeterminado de `dimensions` busca mantener la interoperabilidad con cualquier otra herramienta que solo se haya basado en la especificación original v1.1, tal y como se publicó inicialmente.

Tratamos como un error el caso en que ambas claves aparezcan en una definición y no podremos deserializar ese Metric View.
No conocemos ninguna forma de generar ese caso salvo editando el YAML manualmente; desde luego, no puedes hacerlo por accidente mediante Semantic Bridge ni con ninguna de las operaciones que exponemos.
Una definición de Metric View de este tipo, que use tanto `dimensions` como `fields`, requerirá corrección manual.

Una nota importante sobre el bloque `materialization` de la definición YAML de Metric View: esta sección del YAML sigue usando solo `dimensions`, independientemente de la clave de nivel superior que se utilice.
[Consulta la documentación para obtener una guía oficial sobre materialization](https://learn.microsoft.com/azure/databricks/business-semantics/metric-views/yaml-reference#materialization).

Por último, no hay ninguna diferencia de comportamiento ni semántica entre usar `dimensions` o `fields`.
Estas palabras clave son sinónimos; se recomienda usar `fields`.

## Cambio en la API del modelo de objetos de Metric View: de `Dimension` a `Field`

Siguiendo la recomendación de usar `fields`, hemos aplicado este criterio en todo el Semantic Bridge.
Proporcionamos un [modelo de objetos de Metric View para interactuar programáticamente con una Metric View](xref:semantic-bridge-metric-view-object-model), necesario para implementar las traducciones en el Semantic Bridge.
Hemos dejado obsoleto el objeto `Dimension`, así como todos los métodos y propiedades asociados que usaban "dimension" o "dimensions" en su nombre.
Hemos creado un nuevo objeto `Field` y nuevos métodos y propiedades cuyo nombre incluye "field".
El objeto `Dimension` y los métodos y propiedades asociados ahora mostrarán una advertencia sobre su estado de obsolescencia.
Todo el código basado en `Dimension` seguirá funcionando, pero es posible que los eliminemos una vez transcurrido un tiempo prudencial.
Al igual que Databricks, recomendamos usar `Field` y los métodos asociados para todo el trabajo nuevo.

En términos de implementación, todo el código basado en `Dimension` pasa por la implementación del código basado en `Field` o la refleja.
Aunque recomendamos usar `Field`, puedes usar ambos indistintamente.
En general, la migración de `Dimension` a `Field` debería ser transparente.

Nota técnica: [`Dimension`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Dimension) es una subclase de `Field`.
Por ello, hay algunas formas en las que puedes observar diferencias entre el código de `Field` y el de `Dimension`, y existen soluciones razonables.
Para escribir código que siga funcionando cuando se elimine `Dimension`, usa `Field` en las ramas condicionales y en las declaraciones; no nombres ni compruebes nunca el tipo concreto `Dimension`. Dado un campo `f`:

| Evita                                                                 | Usa en su lugar                                                          | Por qué deja de funcionar cuando se elimina `Dimension`                                                                         |
| --------------------------------------------------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| `f is Dimension`                                                      | `f is Field`                                                             | `Dimension` deja de compilar; `is Field` es verdadero en ambas etapas                                                           |
| `f is Dimension x`                                                    | `f is Field x`                                                           | igual                                                                                                                           |
| `case Dimension x:`                                                   | `case Field x:`                                                          | igual                                                                                                                           |
| `(Dimension)f`, `f as Dimension`                                      | usa `f` directamente como `Field` (sin hacer un cast) | el tipo de destino del cast desaparece; `f` ya es un `Field`                                                                    |
| `f.GetType() == typeof(Dimension)`                                    | `f is Field`                                                             | `typeof(Dimension)` ya no compila                                                                                               |
| `f.GetType() == typeof(Field)`                                        | `f is Field`                                                             | ahora es false (el tipo en tiempo de ejecución es `Dimension`), más adelante true, así que cambia sin avisar |
| `f.GetType().Name == "Dimension"` (o `== "Field"`) | `f is Field`; para una etiqueta, usa `f.ToString()` o `f.Name`           | la cadena con el nombre del tipo es `"Dimension"` ahora y `"Field"` más tarde                                                   |
| `Dimension x = ...`, `List<Dimension>`, `IEnumerable<Dimension>`      | `Field x = ...`, `view.Fields`, `IReadOnlyList<Field>`                   | el nombre del tipo `Dimension` desaparece                                                                                       |
| `typeof(Dimension)`, `nameof(Dimension)`                              | `typeof(Field)`, `nameof(Field)`                                         | se elimina el símbolo `Dimension`                                                                                               |
| `MakeValidationRule<MetricView.Dimension>(...)`                       | `MakeValidationRule<MetricView.Field>(...)`                              | el argumento de tipo hace referencia a un tipo que se ha eliminado                                                              |

> [!NOTE]
> La obsolescencia del tipo `Dimension` en el modelo de objetos, así como cualquier futura eliminación de este tipo y de los métodos asociados, no afectará a la serialización ni a la deserialización mediante cualquiera de las dos palabras clave de YAML.

## Referencia de nombre: de `Dimension` a `Field`

La tabla siguiente enumera cada nombre en desuso basado en `Dimension` y su reemplazo canónico basado en `Field`. Los nombres heredados siguen compilando (con una advertencia de obsolescencia) y se comportan de forma idéntica; en los scripts nuevos, usa los nombres canónicos.

| Nombre heredado (obsoleto)                   | Nombre canónico                                             | Dónde                                                                                            |
| --------------------------------------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `MetricView.Dimension` (tipo)                | `MetricView.Field` (tipo)                | Modelo de objetos                                                                                |
| `view.Dimensions`                                               | `view.Fields`                                               | Colección de `View`                                                                              |
| `view.Dimensions["name"]`                                       | `view.Fields["name"]`                                       | Indexación en la colección por nombre                                                            |
| `view.AddDimension(name, expr)`                                 | `view.AddField(name, expr)`                                 | Método de `View`                                                                                 |
| `SemanticBridge.MetricView.MakeValidationRuleForDimension(...)` | `SemanticBridge.MetricView.MakeValidationRuleForField(...)` | Asistente de reglas de validación (ambas sobrecargas, con y sin `minVersion`) |
| `context.DimensionNames`                                        | `context.FieldNames`                                        | Contexto que se proporciona a una regla de validación                                            |

## Relacionado

- @semantic-bridge
- @semantic-bridge-metric-view-object-model
- @semantic-bridge-metric-view-validation
- [API de Metric View](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView)
