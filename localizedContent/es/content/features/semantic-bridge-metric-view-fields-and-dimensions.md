---
uid: semantic-bridge-metric-view-fields-and-dimensions
title: Campos y dimensiones en Metric Views
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

# Campos y dimensiones en Metric Views

<!--
SUMMARY: Explains the Databricks Metric View `dimensions` -> `fields` keyword rename and the
matching Semantic Bridge C# API rename (Dimension -> Field): what changed, that the old names
still work, migration guidance, and what Tabular Editor emits on round-trip.
-->

En la primavera de 2026, la especificación de Metric View redefinió una clave canónica de nivel superior del YAML de Metric View: cambió de `dimensions` (ahora heredada) a `fields`.
Ambas hacen referencia al conjunto de columnas disponible para consultar en la Metric View, tanto si son referencias directas a columnas de origen como si están definidas mediante una expresión SQL.
[La documentación indica que debe preferirse `fields`, pero ambos términos siguen siendo válidos](https://learn.microsoft.com/azure/databricks/business-semantics/metric-views/yaml-reference#dimensions).
Hemos actualizado el modelo de objetos de Metric View en Semantic Bridge para alinearlo con este cambio.
La serialización y la deserialización siguen funcionando con cualquiera de las dos claves, de conformidad con la especificación de Metric View.
Ofrecemos capas de compatibilidad con versiones anteriores en el modelo de objetos para los nombres antiguos asociados a "dimension".
Los usuarios del modelo de objetos en C# Scripts deberían migrar a los nombres asociados a "field" en cuanto puedan.

**A quién afecta**: cualquiera que escriba YAML de Metric View a mano y cualquiera que use el modelo de objetos de Metric View en C# Scripts en Tabular Editor.

## Control de versiones

Este cambio llegó después de que se publicara la especificación v1.1 y sin una nueva versión de la especificación.
Por ello, en Semantic Bridge adoptamos un enfoque conservador.
Consideramos `dimensions` como valor predeterminado para las Metric Views v0.1 y v1.1.
En el futuro, trataremos `fields` como valor predeterminado para las Metric Views de versiones posteriores.
Lo hacemos por cautela y para ofrecer la máxima interoperabilidad con otras herramientas que quizá no estén al día con la última especificación publicada de Metric View.

## Serialización y deserialización

Según la [documentación de Metric View](https://learn.microsoft.com/azure/databricks/business-semantics/metric-views/yaml-reference#dimensions), ambas claves siguen siendo válidas para la serialización.

| La fuente YAML utiliza | Versión                                       | La deserialización se realiza correctamente | Se emite una advertencia al deserializar                | Se vuelve a serializar con    |
| ---------------------- | --------------------------------------------- | ------------------------------------------- | ------------------------------------------------------- | ----------------------------- |
| `campos`               | <1.1 | sí                                          | sí                                                      | `campos`                      |
| `dimensiones`          | <1.1 | sí                                          | no                                                      | `dimensiones`                 |
| ninguno de los dos     | <1.1 | sí                                          | no                                                      | `dimensiones`                 |
| `campos`               | 1.1                           | sí                                          | no                                                      | `campos`                      |
| `dimensiones`          | 1.1                           | sí                                          | sí                                                      | `dimensiones`                 |
| ninguno de los dos     | 1.1                           | sí                                          | no                                                      | `dimensiones`                 |
| `campos`               | > 1.1                         | sí                                          | no                                                      | `campos`                      |
| `dimensiones`          | > 1.1                         | sí                                          | sí                                                      | `dimensiones`                 |
| ninguno de los dos     | > 1.1                         | sí                                          | no                                                      | `campos`                      |
| ambos                  | cualquiera                                    | no                                          | sí (error; falla la deserialización) | n/a; falla la deserialización |

Seguiremos admitiendo ambas palabras clave en todas las versiones de Metric View, a menos que una futura actualización de la especificación indique lo contrario.
Puedes seguir usando libremente cualquiera de las dos, como prefieras, teniendo en cuenta las notas anteriores sobre las advertencias y los valores predeterminados para la serialización y la deserialización.

Puedes observar que mostramos una advertencia sobre `dimensions` en una Metric View v1.1 y que también elegimos `dimensions` como valor predeterminado si no se proporciona ninguna clave en esa misma v1.1.
Este es nuestro valor predeterminado conservador porque, a mitad de la versión 1.1, se introdujo `fields` como opción preferida.
La advertencia está en consonancia con la documentación de Metric View, que indica que `fields` debe considerarse el valor predeterminado.
El valor predeterminado de `dimensions` permite la interoperabilidad con cualquier otra herramienta que quizá solo se haya ajustado a la especificación original v1.1 cuando se publicó por primera vez.

Consideramos un error que ambas claves aparezcan en una definición y no podremos deserializar una Metric View de ese tipo.
No conocemos ninguna forma de generar un caso así que no sea editando manualmente el YAML; desde luego, no puedes hacerlo por accidente mediante Semantic Bridge ni mediante ninguna de las operaciones que exponemos.
Una definición de Metric View de este tipo, que usa tanto `dimensions` como `fields`, requerirá una corrección manual.

Una nota importante sobre el bloque `materialization` de la definición YAML de Metric View: esta sección de YAML sigue usando solo `dimensions`, independientemente de la clave de nivel superior que se utilice.
[Consulta la documentación para obtener directrices definitivas sobre `materialization`](https://learn.microsoft.com/azure/databricks/business-semantics/metric-views/yaml-reference#materialization).

Por último, no hay ninguna diferencia de comportamiento ni semántica entre usar `dimensions` o `fields`.
Estas palabras clave son simplemente sinónimos, con la indicación de que debe preferirse `fields`.

## Cambio en la API del modelo de objetos de Metric View: de `Dimension` a `Field`

En línea con la recomendación de preferir `fields`, hemos aplicado este criterio en todo Semantic Bridge.
Ofrecemos un [modelo de objetos de Metric View para interactuar programáticamente con una Metric View](xref:semantic-bridge-metric-view-object-model), necesario para implementar las traducciones en el Semantic Bridge.
Hemos marcado como obsoleto el objeto `Dimension`, así como todos los métodos y propiedades asociados que tenían "dimension" o "dimensions" en su nombre.
Hemos creado un nuevo objeto `Field`, así como nuevos métodos y propiedades con "field" en su nombre.
El objeto `Dimension` y los métodos y propiedades asociados ahora mostrarán una advertencia sobre su estado obsoleto.
Todo el código basado en `Dimension` seguirá funcionando, pero es posible que retiremos estos elementos cuando haya transcurrido un tiempo prudencial.
Al igual que Databricks, recomendamos que utilices `Field` y los métodos asociados para todo trabajo nuevo.

En términos de implementación, todo el código basado en `Dimension` pasa por la implementación del código basado en `Field` o la reproduce.
Aunque recomendamos usar `Field`, puedes usar ambos indistintamente.
En general, la migración de `Dimension` a `Field` debería ser transparente.

Una nota técnica: [`Dimension`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Dimension) es una subclase de `Field`.
Por ello, puedes observar algunas diferencias entre el código de `Field` y el de `Dimension`, y existen soluciones alternativas razonables.
Para escribir código que siga funcionando cuando se elimine `Dimension`, bifurca y declara en términos de `Field`; nunca nombres ni compruebes el tipo concreto `Dimension`. Dado un campo `f`:

| Evita                                                                 | Usa en su lugar                                                               | Por qué deja de funcionar cuando se elimina `Dimension`                                                                           |
| --------------------------------------------------------------------- | ----------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `f is Dimension`                                                      | `f is Field`                                                                  | `Dimension` deja de compilar; `is Field` es verdadero en ambas épocas                                                             |
| `f is Dimension x`                                                    | `f is Field x`                                                                | igual                                                                                                                             |
| `case Dimension x:`                                                   | `case Field x:`                                                               | igual                                                                                                                             |
| `(Dimension)f`, `f as Dimension`                                      | usa `f` directamente como `Field` (sin conversión de tipo) | el tipo de destino de la conversión desaparece; `f` ya es un `Field`                                                              |
| `f.GetType() == typeof(Dimension)`                                    | `f is Field`                                                                  | `typeof(Dimension)` ya no compila                                                                                                 |
| `f.GetType() == typeof(Field)`                                        | `f is Field`                                                                  | false ahora (el tipo en tiempo de ejecución es `Dimension`), true más adelante, así que cambia silenciosamente |
| `f.GetType().Name == "Dimension"` (o `== "Field"`) | `f is Field`; para una etiqueta, `f.ToString()` o `f.Name`                    | la cadena del nombre del tipo es `"Dimension"` ahora, `"Field"` más adelante                                                      |
| `Dimension x = ...`, `List<Dimension>`, `IEnumerable<Dimension>`      | `Field x = ...`, `view.Fields`, `IReadOnlyList<Field>`                        | el nombre de tipo `Dimension` desaparece                                                                                          |
| `typeof(Dimension)`, `nameof(Dimension)`                              | `typeof(Field)`, `nameof(Field)`                                              | se elimina el símbolo `Dimension`                                                                                                 |
| `MakeValidationRule<MetricView.Dimension>(...)`                       | `MakeValidationRule<MetricView.Field>(...)`                                   | el argumento de tipo hace referencia a un tipo eliminado                                                                          |

> [!NOTE]
> La obsolescencia del tipo `Dimension` en el modelo de objetos, así como cualquier eliminación futura de este tipo y de los métodos asociados, no afectarán a la serialización ni a la deserialización con cualquiera de las dos palabras clave de YAML.

## Referencia de nombre: de `Dimension` a `Field`

La siguiente tabla enumera cada nombre basado en `Dimension` en desuso y su reemplazo canónico basado en `Field`. Los nombres heredados siguen compilando (con una advertencia de obsolescencia) y se comportan de forma idéntica; se recomienda usar los nombres canónicos en scripts nuevos.

| Nombre heredado (obsoleto)                   | Nombre canónico                                             | Dónde                                                                                                     |
| --------------------------------------------------------------- | ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `MetricView.Dimension` (tipo)                | `MetricView.Field` (tipo)                | Modelo de objetos                                                                                         |
| `view.Dimensions`                                               | `view.Fields`                                               | Colección de `View`                                                                                       |
| `view.Dimensions["name"]`                                       | `view.Fields["name"]`                                       | Indexación por nombre en la colección                                                                     |
| `view.AddDimension(name, expr)`                                 | `view.AddField(name, expr)`                                 | Método de `View`                                                                                          |
| `SemanticBridge.MetricView.MakeValidationRuleForDimension(...)` | `SemanticBridge.MetricView.MakeValidationRuleForField(...)` | Función auxiliar para reglas de validación (ambas sobrecargas, con y sin `minVersion`) |
| `context.DimensionNames`                                        | `context.FieldNames`                                        | Contexto que se pasa a una regla de validación                                                            |

## Relacionado

- @semantic-bridge
- @semantic-bridge-metric-view-object-model
- @semantic-bridge-metric-view-validation
- [API de Metric View](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView)
