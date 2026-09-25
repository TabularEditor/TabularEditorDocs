---
uid: te-cli-automation
title: Automatización y scripts
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

# Automatización y scripts

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

La CLI de Tabular Editor es componible: cada comando admite salida estructurada, permite desactivar los avisos interactivos cuando se necesite y devuelve códigos de salida previsibles. Las mismas primitivas funcionan igual de bien en canalizaciones de shell, scripts de Python, automatización con PowerShell y flujos de trabajo basados en agentes.

## Salida estructurada

Use `--output-format` para alternar cualquier comando entre el formato de texto (legible para personas) y formatos legibles por máquina:

| Formato                                    | Se utiliza para                                                                                                                                                      | Notas                                                                                                                                                       |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `text` (predeterminado) | Para uso humano                                                                                                                                                      | Texto sin formato en stdout, independientemente de si el flujo es un TTY o se canaliza.                                                     |
| `json`                                     | Para uso por máquina                                                                                                                                                 | Siempre devuelve JSON válido en stdout. Use `--error-format json` si también quiere errores legibles por máquina en stderr. |
| `csv`                                      | Tabular results (`query`, `bpa run`, `bpa rules`, `vertipaq`, `validate`, `test`, `refresh`, `profile list`, `session list`, `find`, `get`, `ls`) | Escapado según RFC 4180.                                                                                                                    |
| `tmsl` (alias `bim`)    | Serialización TMSL/BIM del objeto completo                                                                                                                           | Accepted by `te get` and `te list`.                                                                                                         |
| `tmdl`                                     | Serialización TMDL del objeto completo                                                                                                                               | Aceptado solo por `te get` (un solo objeto).                                                                             |

```bash
te list --output-format json
te query -q "EVALUATE VALUES('Date'[Year])" --output-format csv
te bpa run --output-format json
```

Under `--output-format json`, `te validate`, `te bpa run`, `te test run`, and `te query` share one JSON document shape with a `summary`, a flat `findings[]` array, and `durationMs` - see @te-cli-findings for the shape to parse.

> [!NOTE]
> `--output-format` y `--error-format` son independientes. Establecer `--output-format json` _no_ cambia stderr a JSON; usa `--error-format json` para eso. No hay cambio automático de formato cuando stdout se redirige; el valor predeterminado siempre es `text`, a menos que indiques lo contrario.

## Modo no interactivo

Agrega `--non-interactive` a cualquier comando para deshabilitar las solicitudes de confirmación, las listas de selección de credenciales y los asistentes guiados. Si el comando necesita una entrada que no pueda determinar mediante opciones, variables de entorno o configuración, finaliza con un código distinto de cero y un error accionable, en lugar de quedarse bloqueado.

`te deploy` and `te refresh` are additionally dry-run by default - they print the TMSL they would send and touch nothing. `--execute` performs the action, and in piped or CI runs `--execute` requires `--force` (the confirmation prompt cannot be answered).

```bash
te deploy --model ./model --target-server my-workspace --target-database my-model \
  --non-interactive --execute --force --ci github
```

## Códigos de salida

Todos los comandos de `te` finalizan con un código de estado predecible, para que quien los invoque pueda tomar decisiones según el éxito o el error sin tener que analizar stdout.

| Salir | Significado                                                                                                                                                                                                                                                                                                                                                                        |
| ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `0`   | Success.                                                                                                                                                                                                                                                                                                                                                           |
| `1`   | Generic failure - invalid arguments, command failed, validation errors, auth failure, BPA gate failed at severity >= error, a `te script` run in which a script called `Error(...)`, a `te deploy` the server accepted with object errors. For `te diff`: differences found (like the `diff`/`cmp` convention). |
| `2`   | `te diff` only: an error occurred while comparing, so the difference status is unknown.                                                                                                                                                                                                                                                            |

Combina los códigos de salida con las anotaciones `--ci <vsts\|github>` y `--trx <file>` para mostrar información detallada sobre los errores en CI; consulta @te-cli-cicd.

## Errores en stderr

Errors, warnings, progress and status notices (the spinner, `Using active connection:`), the usage reminder that follows an argument error, and the preview banner are written to **stderr**; stdout carries only the result. A rejected command therefore leaves stdout empty, so a captured dry run is either valid output or nothing at all, and you can pipe JSON safely without it being contaminated by progress indicators or diagnostic messages:

```bash
te list --output-format json | jq '.[] | .name'
te vertipaq --output-format json > stats.json
```

## Python

Python es una opción natural para orquestar llamadas a la CLI desde pipelines de datos, notebooks o bancos de pruebas. Invoca `te` con `subprocess.run`, solicita JSON y analiza stdout:

```python
import json
import subprocess

def query(server: str, database: str, dax: str) -> list[dict]:
    result = subprocess.run(
        ["te", "query",
         "-s", server,
         "-d", database,
         "-q", dax,
         "--output-format", "json",
         "--non-interactive"],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)["rows"]

rows = query("Finance", "Revenue Model", "EVALUATE TOPN(10, 'Sales')")
for row in rows:
    print(row)
```

Para capturar errores estructurados desde stderr:

```python
import json
import subprocess

result = subprocess.run(
    ["te", "deploy", "--model", "./model",
     "--target-server", "Finance", "--target-database", "Revenue",
     "--output-format", "json", "--error-format", "json",
     "--non-interactive", "--execute", "--force"],
    capture_output=True, text=True,
)

if result.returncode != 0:
    try:
        err = json.loads(result.stderr.strip().splitlines()[-1])
        print("Deploy failed:", err.get("error"), "- hint:", err.get("hint"))
    except json.JSONDecodeError:
        print("Deploy failed:\n", result.stderr)
```

## PowerShell

PowerShell maneja JSON de forma nativa. `te` es un ejecutable de consola normal que funciona directamente en canalizaciones de PowerShell (consulta @te-cli-migrate si estás migrando desde la antigua CLI de `TabularEditor.exe`):

```powershell
$result = te query -s Finance -d Revenue -q "EVALUATE TOPN(10, 'Sales')" --output-format json --non-interactive
  | ConvertFrom-Json

$result.rows | Format-Table

# Check exit code after the pipeline
if ($LASTEXITCODE -ne 0) {
    Write-Error "Query failed with exit $LASTEXITCODE"
    exit $LASTEXITCODE
}
```

Lee los secretos desde el entorno en lugar de pasarlos como texto sin formato:

```powershell
$env:AZURE_CLIENT_ID     = "your-app-id"
$env:AZURE_CLIENT_SECRET = "your-client-secret"
$env:AZURE_TENANT_ID     = "your-tenant-id"

te deploy --model ./model `
  --target-server my-workspace --target-database my-model `
  --auth env --non-interactive --execute --force --ci vsts
```

## Bash

Compón comandos con pipes y `jq`. La salida de texto de la CLI está coloreada para facilitar la lectura, pero si cambias a `--output-format json` obtienes una estructura limpia con la que trabajar:

```bash
# Count measures per table
te list --type measure --output-format json \
  | jq -r '.[] | .table' \
  | sort | uniq -c | sort -rn
```

```bash
# Fail the shell script if BPA finds any errors
te bpa run --fail-on error --output-format json > bpa.json \
  || { echo "BPA gate failed"; jq '.violations' bpa.json; exit 1; }
```

## Composability example

Generar un script TMSL de actualización y ponerlo bajo control de versiones solo requiere tres comandos:

```bash
te connect MyWorkspace MyModel
te refresh --type full > refresh.tmsl
cat refresh.tmsl
```

The resulting TMSL can be reviewed in a pull request, committed, executed by the CLI (`te refresh --type full --execute`), handed to a DBA, or applied by any XMLA-compatible tool. La CLI se convierte en un componente en lugar de una caja negra.

## Patrones útiles

Algunos patrones pequeños que aparecen a menudo al componer comandos de `te` en scripts o pipelines:

- **Idempotent creates and removes.** `te add Sales/Marker -t Measure -p Expression="0" --if-not-exists --save` and `te remove Sales/OldMeasure --if-exists --save` both exit `0` whether or not the object existed - safe to re-run in CI.
- **Nothing persists without `--save`.** Mutating commands (`te add`, `te set`, `te move`, `te remove`, `te script`, `te macro run`) apply the change in memory, report what they did, and then print `Dry run - nothing saved. Add --save to persist.` Run one bare to confirm it resolves the objects you expect, then re-run with `--save`. `te remove --dry-run` goes further and reports what would be removed without applying anything.
- **Emit TMSL for review.** `te deploy --model ./model --target-server my-workspace --target-database my-model > deploy.tmsl` - deploy is dry-run by default and prints the exact target-aware TMSL to stdout, so redirecting it produces the deployment script without touching the server. Useful for DBA review or manual apply.
- **Piped values via `-`.** Every value-taking option reads piped stdin through `-` (trailing newline removed, byte-order mark stripped; errors immediately when nothing is piped): `cat query.dax | te query -q -` (bare piped stdin with no `-q` also works), `te set Sales/Amount -p Expression=- < expr.dax --save`, `cat fix.csx | te script --inline - --save`, `cat messy.dax | te util format-dax -`. A piped value is taken verbatim - piping the text `null` stores the word `null`, where `-p Name=null` or `--unset Name` clears the property.
- **Discover property names.** `te get <path> --properties --output-format json` returns every name `-p` accepts on that object with its type, writability, and allowed values - the list to consult before generating `te set` calls.
- **Parseable change sets.** Mutating commands (`set`, `add`, `remove`, `move`, `script`, `bpa run --fix`) render a diff by default; `--stat` and `--name-only` give compact text alternatives, and `te config set mutationOutput diff|stat|name-only|none` sets a standing default. JSON output always carries the full `changes` array (one entry per changed object with `objectPath`, `objectType`, `changeKind`, and before/after property pairs) regardless of these flags - the stable shape to parse in scripts. `te diff` reports its differences in the same shape.
- **Path-only output.** `te list --paths-only` and `te find --paths-only` emit one object path per line, ideal for piping to `xargs`, `te get`, or `te set`. The model-level containers (`te list Measures`, `te list Columns`) compose well with this for whole-model sweeps.
- **Pruebas de rendimiento de consultas.** `te query --trace --cold --runs 5` ejecuta una consulta DAX con caché en frío, cinco iteraciones y captura eventos de traza de FE/SE.
- **Step timings in CI logs.** Long-running commands (`te deploy`, `te refresh`, `te script`, `te validate`, `te query`) include a `durationMs` field in JSON output - useful for surfacing per-step timings in pipeline summaries.

## Páginas relacionadas

- @te-cli-cicd - patrones específicos para pipelines y ejemplos en YAML.
- @te-cli-commands - referencia completa de comandos.
- @te-cli-interactive - cuando el modo interactivo encaja mejor que el uso de scripts.
