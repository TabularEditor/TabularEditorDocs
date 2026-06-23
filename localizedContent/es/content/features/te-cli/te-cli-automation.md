---
uid: te-cli-automation
title: Automatización y scripts
author: Peer Grønnerup
updated: 2026-06-11
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

| Formato                                    | Se utiliza para                                                                                                                                                                      | Notas                                                                                                                                                       |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `text` (predeterminado) | Para uso humano                                                                                                                                                                      | Texto sin formato en stdout, independientemente de si el flujo es un TTY o se canaliza.                                                     |
| `json`                                     | Para uso por máquina                                                                                                                                                                 | Siempre devuelve JSON válido en stdout. Use `--error-format json` si también quiere errores legibles por máquina en stderr. |
| `csv`                                      | Resultados tabulares (`query`, `bpa run`, `bpa rules`, `vertipaq`, `validate`, `test`, `refresh`, `profile list`, `session list`, `find`, `replace`, `get`, `ls`) | Escapado según RFC 4180.                                                                                                                    |
| `tmsl` (alias `bim`)    | Serialización TMSL/BIM del objeto completo                                                                                                                                           | Aceptado por `te get` y `te ls`.                                                                                                            |
| `tmdl`                                     | Serialización TMDL del objeto completo                                                                                                                                               | Aceptado solo por `te get` (un solo objeto).                                                                             |

```bash
te ls --output-format json
te query -q "EVALUATE VALUES('Date'[Year])" --output-format csv
te bpa run --output-format json
```

> [!NOTE]
> `--output-format` y `--error-format` son independientes. Establecer `--output-format json` _no_ cambia stderr a JSON; usa `--error-format json` para eso. No hay cambio automático de formato cuando stdout se redirige; el valor predeterminado siempre es `text`, a menos que indiques lo contrario.

## Modo no interactivo

Agrega `--non-interactive` a cualquier comando para deshabilitar las solicitudes de confirmación, las listas de selección de credenciales y los asistentes guiados. Si el comando necesita una entrada que no pueda determinar mediante opciones, variables de entorno o configuración, finaliza con un código distinto de cero y un error accionable, en lugar de quedarse bloqueado.

```bash
te deploy ./model --non-interactive --force --ci github
```

## Códigos de salida

Todos los comandos de `te` finalizan con un código de estado predecible, para que quien los invoque pueda tomar decisiones según el éxito o el error sin tener que analizar stdout.

| Código de salida | Significado                                                                                                                                                                                                                                                                                                            |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `0`              | Éxito.                                                                                                                                                                                                                                                                                                 |
| `1`              | Error genérico: argumentos inválidos, fallo del comando, errores de validación, error de autenticación, fallo en la comprobación de BPA con severidad ≥ error. For `te diff`: differences found (like the `diff`/`cmp` convention). |
| `2`              | `te diff` only: an error occurred while comparing, so the difference status is unknown.                                                                                                                                                                                                |

Combina los códigos de salida con las anotaciones `--ci <vsts\|github>` y `--trx <file>` para mostrar información detallada sobre los errores en CI; consulta @te-cli-cicd.

## Errores en stderr

Los errores, las advertencias y el banner de versión preliminar se escriben en **stderr**; los datos estructurados se escriben en **stdout**. Esto significa que puedes canalizar JSON de forma segura sin que se contamine con indicadores de progreso ni mensajes de diagnóstico:

```bash
te ls --output-format json | jq '.[] | .name'
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
    return json.loads(result.stdout)

rows = query("Finance", "Revenue Model", "EVALUATE TOPN(10, 'Sales')")
for row in rows:
    print(row)
```

Para capturar errores estructurados desde stderr:

```python
import json
import subprocess

result = subprocess.run(
    ["te", "deploy", "./model",
     "-s", "Finance", "-d", "Revenue",
     "--output-format", "json", "--non-interactive", "--force"],
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
$rows = te query -s Finance -d Revenue -q "EVALUATE TOPN(10, 'Sales')" --output-format json --non-interactive
  | ConvertFrom-Json

$rows | Format-Table

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

te deploy ./model `
  -s my-workspace -d my-model `
  --auth env --non-interactive --force --ci vsts
```

## Bash

Compón comandos con pipes y `jq`. La salida de texto de la CLI está coloreada para facilitar la lectura, pero si cambias a `--output-format json` obtienes una estructura limpia con la que trabajar:

```bash
# Count measures per table
te ls --type measure --output-format json \
  | jq -r '.[] | .table' \
  | sort | uniq -c | sort -rn
```

```bash
# Fail the shell script if BPA finds any errors
te bpa run --fail-on error --output-format json > bpa.json \
  || { echo "BPA gate failed"; jq '.violations' bpa.json; exit 1; }
```

## Ejemplo de composición

Generar un script TMSL de actualización y ponerlo bajo control de versiones solo requiere tres comandos:

```bash
te connect MyWorkspace MyModel
te refresh --type full --dry-run > refresh.tmsl
cat refresh.tmsl
```

El TMSL resultante puede revisarse en un pull request, confirmarse mediante un commit, ejecutarse mediante la CLI (`te refresh --type full`), entregarse a un DBA o aplicarse con cualquier herramienta compatible con XMLA. La CLI se convierte en un componente en lugar de una caja negra.

## Patrones útiles

Algunos patrones pequeños que aparecen a menudo al componer comandos de `te` en scripts o pipelines:

- **Creaciones y eliminaciones idempotentes de medidas.** `te add Sales/Marker -t Measure -i "0" --if-not-exists --save` y `te rm Sales/OldMeasure --if-exists --save` salen con código `0` exista o no el objeto; es seguro volver a ejecutarlos en CI.
- **Diferencias en modo de prueba.** `te replace` funciona en modo de prueba de forma predeterminada; añade `--save` solo cuando estés conforme con la vista previa.
- **Genera TMSL para revisión.** `te deploy ./model --xmla deploy.tmsl` produce el script de implementación sin tocar el servidor; útil para que lo revise un DBA o para aplicarlo manualmente.
- **Salida solo con rutas.** `te ls --paths-only` y `te find --paths-only` emiten una ruta de objeto por línea, ideal para canalizarlo a `xargs`, `te get` o `te set`. Los contenedores a nivel de modelo para medidas (`te ls Measures`, `te ls Columns`) se combinan bien con esto para recorridos completos del modelo.
- **Pruebas de rendimiento de consultas.** `te query --trace --cold --runs 5` ejecuta una consulta DAX con caché en frío, cinco iteraciones y captura eventos de traza de FE/SE.
- **Tiempos por paso en los logs de CI.** Los comandos de larga duración (`te deploy`, `te refresh`, `te script`, `te validate`) incluyen un campo `durationMs` en la salida JSON; útil para mostrar los tiempos de cada paso en los resúmenes del pipeline.

## Páginas relacionadas

- @te-cli-cicd - patrones específicos para pipelines y ejemplos en YAML.
- @te-cli-commands - referencia completa de los comandos.
- @te-cli-interactive - cuando el modo interactivo encaja mejor que el uso de scripts.
