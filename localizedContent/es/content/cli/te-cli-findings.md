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

`te validate`, `te bpa run`, `te test run` y `te query` generan un Report de problemas con un formato JSON compartido. Con `--output-format json`, cada uno de estos comandos emite un **único documento**; no hay forma de que alguno no emita nada que analizar.

> [!NOTE]
> `te query` usa esta estructura JSON solo cuando su validación de DAX previa a la ejecución produce al menos un error. Una consulta correcta emite el resultado de la consulta: `{columns, rows, rowCount, truncated, durationMs, trace?}`.

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

- `command` — qué comando generó el documento.
- `durationMs` — duración total de la ejecución.
- `summary` — recuento por gravedad: `errors`, `warnings`, `info`, `total`.
- `findings` — un único array plano, discriminado por `severity`.

## Claves por hallazgo

Presentes en **todos** los hallazgos:

| Clave        | Valores / significado                                                                                                                                                                                                  |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `severity`   | `error`, `warning` o `info`.                                                                                                                                                                           |
| `source`     | `validate`, `bpa`, `test` o `query`.                                                                                                                                                                   |
| `code`       | Código estable del hallazgo (ID de mensaje de validación, ID de regla BPA, `TEST_FAIL` / `TEST_ERROR` / `TEST_SUITE_INVALID`, ...). |
| `message`    | Descripción legible para humanos.                                                                                                                                                                      |
| `object`     | Nombre simple del objeto al que se refiere el hallazgo.                                                                                                                                                |
| `objectType` | Uno de los valores de un vocabulario cerrado; ver más abajo.                                                                                                                                           |
| `fixable`    | `true` solo para infracciones de BPA cuya regla define una expresión de corrección.                                                                                                                    |

**Solo se incluyen cuando la CLI las conoce**; estas claves están _ausentes_, y no como `null`, cuando no se han establecido:

| Clave                  | Generado por                                 | Significado                                                                                                                                                                                                                                                                                                           |
| ---------------------- | -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `objectPath`           | Solo para infracciones de `validate` y `bpa` | Ruta canónica del objeto, que `te get` o `te set` pueden resolver tal cual. Ausente en hallazgos de prueba, hallazgos de consulta y errores de reglas de BPA.                                                                                                                         |
| `expressionPosition`   | Solo para `validate` y `query`               | `{property, lineNumber, column}` dentro de la propiedad Named Expression. **Opcional en cualquier origen, incluidos validate y query**; está ausente cuando el analizador no informó ninguna posición utilizable y es de todo o nada (nunca una posición parcial). |
| `ruleName`, `category` | Solo para `bpa`                              | El nombre y la categoría de la regla infringida.                                                                                                                                                                                                                                                      |

### vocabulario de `objectType`

El conjunto cerrado de valores de `objectType` (las formas en singular de los contenedores de la gramática de rutas, no una enumeración de TOM):

`medida`, `Column`, `Hierarchy`, `Level`, `partición`, `CalculationItem`, `Table`, `rol`, `TablePermission`, `perspectiva`, `configuración regional`, `DataSource`, `Expression`, `Function`, `relación`, `KPI`, `RefreshPolicy`, `Member`, `Calendar`, `Variation`, `Model`, `BpaRule`, `Test`, `TestSuite`, `Query`.

## Extras por comando

Cada comando mantiene algunas claves propias en el nivel superior del documento:

| Comando            | Claves adicionales                                                                                                                                                                                                                                                                                                       |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `te validate`      | `valid` (booleano).                                                                                                                                                                                                                                                                   |
| `te bpa run`       | `model`, `rulesEvaluated`, `violations`, `ruleErrors`, `ignoredRules`. Los errores al evaluar reglas aparecen en `findings` con severidad `error` y `objectType: "BpaRule"`; `violations` y `ruleErrors` separan ambos recuentos.                                                        |
| `te bpa run --fix` | Una clave `fix` en ese mismo documento: `changes`, `fixed`, `fixErrors`, `skipped`, `fixedItems`, `fixErrorItems`. Si falla la propia fase de corrección, el documento se escribe igualmente con el motivo en `fix.error`. No está presente sin `--fix`. |
| `te test run`      | `suites`, `invalidSuites`, `testSummary` (totales de pruebas por estado; `summary` sigue siendo el recuento compartido por gravedad).                                                                                                                                                 |
| `te query`         | Ninguna, y solo en errores de validación; consulta la nota anterior.                                                                                                                                                                                                                                     |

## Anotaciones de CI

Los cuatro comandos comparten un mismo generador de anotaciones para `--ci vsts` / `--ci github` (`azdo`, `azure-devops` y `gh` son alias aceptados; `none` desactiva las anotaciones; cualquier otro valor se rechaza antes de que se ejecute el comando). Las anotaciones se envían a stderr; stdout sigue siendo analizable:

- Las anotaciones incluyen el código del hallazgo: `code=` en Azure DevOps, `title=` en GitHub.
- Los hallazgos con gravedad informativa no son advertencias: en GitHub emiten `::notice::`; en Azure DevOps, una línea de registro normal. Una ejecución de Azure DevOps cuyos únicos hallazgos son de tipo Report con gravedad informativa finaliza con el estado **Succeeded**.
- Los mensajes de varias líneas se escapan y se condensan en una sola línea de anotación, para que la descripción de una regla no pueda romper el formato del registro.

## Páginas relacionadas

- @te-cli-commands#exit-codes - los códigos de salida no se ven afectados por el formato de salida.
- @te-cli-cicd - patrones de pipeline que consumen esta estructura.
- @te-cli-automation - analizando la salida estructurada de scripts.
