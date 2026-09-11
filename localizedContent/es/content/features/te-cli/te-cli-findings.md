---
uid: te-cli-findings
title: Resultados legibles por máquina (JSON)
author: Peer Grønnerup
updated: 2026-09-11
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      none: true
    - product: Tabular Editor CLI
      full: true
---

# Resultados legibles por máquina (JSON)

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

`te validate`, `te bpa run`, `te test run` y `te query` generan un Report de problemas en un mismo formato JSON. Con `--output-format json`, cada uno de estos comandos emite un **único documento**; no hay forma de que alguno de ellos no genere nada para analizar.

> [!NOTE]
> `te query` usa esta estructura JSON solo cuando su validación DAX previa a la ejecución produce al menos un error. Si la consulta se ejecuta correctamente, emite en su lugar el resultado de la consulta: `{columns, rows, rowCount, truncated, durationMs, trace?}`.

## El documento JSON

```json
{
  "command": "validate",
  "durationMs": 412,
  "summary": { "errors": 1, "warnings": 2, "info": 0, "total": 3 },
  "findings": [
    {
      "severity": "error",
      "source": "validate",
      "code": "TE0001",
      "message": "Unknown column 'Sales'[Amt]",
      "object": "Revenue",
      "objectType": "Measure",
      "objectPath": "Sales/Revenue",
      "expressionPosition": { "property": "Expression", "lineNumber": 3, "column": 9 },
      "fixable": false
    }
  ],
  "valid": false
}
```

- `command` - qué comando generó el documento.
- `durationMs` - duración total de la ejecución.
- `summary` - recuento por gravedad: `errors`, `warnings`, `info`, `total`.
- `findings` - un único array plano, clasificado por `severity`.

## Claves de cada hallazgo

Presentes en **cada** hallazgo:

| Clave        | Valores / significado                                                                                                                                                                                                     |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `severity`   | `error`, `warning` o `info`.                                                                                                                                                                              |
| `source`     | `validate`, `bpa`, `test` o `query`.                                                                                                                                                                      |
| `code`       | Código estable del hallazgo (ID de mensaje de validación, ID de regla de BPA, `TEST_FAIL` / `TEST_ERROR` / `TEST_SUITE_INVALID`, ...). |
| `message`    | Descripción legible para humanos.                                                                                                                                                                         |
| `object`     | Nombre sin calificar del objeto al que se refiere el hallazgo.                                                                                                                                            |
| `objectType` | Un valor de un vocabulario cerrado; véase más abajo.                                                                                                                                                      |
| `fixable`    | `true` solo en las infracciones de BPA cuya regla define una expresión de corrección.                                                                                                                     |

Se incluyen **solo cuando la CLI las conoce**; estas claves están _ausentes_ en lugar de `null` cuando no se establecen:

| Clave                  | Generado por                                 | Significado                                                                                                                                                                                                                                                                                                                                                    |
| ---------------------- | -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `objectPath`           | Solo para infracciones de `validate` y `bpa` | Ruta canónica del objeto, resoluble tal cual mediante `te get` o `te set`. No aparece en los hallazgos de pruebas, los hallazgos de consultas ni los errores de reglas de BPA.                                                                                                                                                 |
| `expressionPosition`   | Solo en `validate` y `query`                 | `{property, lineNumber, column}` dentro de la propiedad `Named Expression` de la expresión. **Opcional en todos los orígenes, incluidos validate y query**: no aparece cuando el analizador no hizo Report de ninguna posición utilizable y es de todo o nada (nunca una posición parcial). |
| `ruleName`, `category` | Solo en `bpa`                                | El nombre y la categoría de la regla infringida.                                                                                                                                                                                                                                                                                               |

### vocabulario de objectType

El conjunto cerrado de valores de `objectType` (las formas singulares de los contenedores de la gramática de rutas, no una enumeración de TOM):

`medida`, `Column`, `Hierarchy`, `Level`, `partición`, `CalculationItem`, `Table`, `rol`, `TablePermission`, `perspectiva`, `configuración regional`, `DataSource`, `Expression`, `Function`, `relación`, `KPI`, `RefreshPolicy`, `Member`, `Calendar`, `Variation`, `Model`, `BpaRule`, `Test`, `TestSuite`, `Query`.

## Elementos adicionales por comando

Cada comando mantiene algunas claves propias en el nivel superior del documento:

| Comando            | Claves adicionales                                                                                                                                                                                                                                                                                                           |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `te validate`      | `valid` (booleano).                                                                                                                                                                                                                                                                       |
| `te bpa run`       | `model`, `rulesEvaluated`, `violations`, `ruleErrors`, `ignoredRules`. Los errores de evaluación de reglas aparecen en `findings` con severidad `error` y `objectType: "BpaRule"`; `violations` y `ruleErrors` desglosan ambos recuentos.                                                    |
| `te bpa run --fix` | Una clave `fix` dentro del mismo documento: `changes`, `fixed`, `fixErrors`, `skipped`, `fixedItems`, `fixErrorItems`. Si falla la propia pasada de corrección, el documento se sigue escribiendo con la causa en `fix.error`. No está presente sin `--fix`. |
| `te test run`      | `suites`, `invalidSuites`, `testSummary` (recuentos de pruebas por estado; `summary` sigue siendo el recuento compartido por gravedad).                                                                                                                                                   |
| `te query`         | Ninguno, y solo en caso de errores de validación; consulta la nota anterior.                                                                                                                                                                                                                                 |

## Anotaciones de CI

Los cuatro comandos comparten un único generador de anotaciones para `--ci vsts` / `--ci github` (`azdo`, `azure-devops` y `gh` son alias admitidos; `none` desactiva las anotaciones; cualquier otro valor se rechaza antes de que se ejecute el comando). Las anotaciones se envían a stderr; stdout sigue siendo analizable:

- Las anotaciones incluyen el código del hallazgo: `code=` en Azure DevOps, `title=` en GitHub.
- Los hallazgos de severidad informativa no son advertencias: en GitHub se emiten como `::notice::`; en Azure DevOps, como una simple línea de registro. Una ejecución de Azure DevOps cuyos únicos hallazgos son informativos muestra **Succeeded** en el Report.
- Los mensajes de varias líneas se escapan en una sola línea de anotación, para que la descripción de una regla no pueda romper el formato del registro.

## Páginas relacionadas

- @te-cli-commands#exit-codes - los códigos de salida no se ven afectados por el formato de salida.
- @te-cli-cicd - patrones de pipeline que consumen esta estructura.
- @te-cli-automation - parseo de salida estructurada desde scripts.
