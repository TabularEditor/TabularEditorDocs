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

| Formato                                    | Se utiliza para                                                                                                                                                           | Notas                                                                                                                                                       |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `text` (predeterminado) | Para uso humano                                                                                                                                                           | Texto sin formato en stdout, independientemente de si el flujo es un TTY o se canaliza.                                                     |
| `json`                                     | Para uso por máquina                                                                                                                                                      | Siempre devuelve JSON válido en stdout. Use `--error-format json` si también quiere errores legibles por máquina en stderr. |
| `csv`                                      | Resultados tabulares (`query`, `bpa run`, `bpa rules`, `vertipaq`, `validate`, `test`, `refresh`, `profile list`, `session list`, `find`, `get`, `ls`) | Escapado según RFC 4180.                                                                                                                    |
| `tmsl` (alias `bim`)    | Serialización TMSL/BIM del objeto completo                                                                                                                                | Admitido por `te get` y `te list`.                                                                                                          |
| `tmdl`                                     | Serialización TMDL del objeto completo                                                                                                                                    | Aceptado solo por `te get` (un solo objeto).                                                                             |

```bash
te list --output-format json
te query -q "EVALUATE VALUES('Date'[Year])" --output-format csv
te bpa run --output-format json
```

Con `--output-format json`, `te validate`, `te bpa run`, `te test run` y `te query` comparten una misma estructura de documento JSON con un `summary`, una matriz plana `findings[]` y `durationMs`; consulta @te-cli-findings para ver la estructura que debes analizar.

> [!NOTE]
> `--output-format` y `--error-format` son independientes. Establecer `--output-format json` _no_ cambia stderr a JSON; usa `--error-format json` para eso. No hay cambio automático de formato cuando stdout se redirige; el valor predeterminado siempre es `text`, a menos que indiques lo contrario.

## Modo no interactivo

Agrega `--non-interactive` a cualquier comando para deshabilitar las solicitudes de confirmación, las listas de selección de credenciales y los asistentes guiados. Si el comando necesita una entrada que no pueda determinar mediante opciones, variables de entorno o configuración, finaliza con un código distinto de cero y un error accionable, en lugar de quedarse bloqueado.

Además, `te deploy` y `te refresh` se ejecutan en modo de simulación de forma predeterminada: imprimen el TMSL que enviarían y no tocan nada. `--execute` realiza la acción y, en ejecuciones con entrada canalizada o en CI, `--execute` requiere `--force` (no se puede responder al aviso de confirmación).

```bash
te deploy --model ./model --target-server my-workspace --target-database my-model \
  --non-interactive --execute --force --ci github
```

## Códigos de salida

Todos los comandos de `te` finalizan con un código de estado predecible, para que quien los invoque pueda tomar decisiones según el éxito o el error sin tener que analizar stdout.

| Código de salida | Significado                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `0`              | Éxito.                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `1`              | Error genérico: argumentos no válidos, fallo del comando, errores de validación, fallo de autenticación, gate de BPA fallido con gravedad >= error, una ejecución de `te script` en la que un script llamó a `Error(...)`, un `te deploy` que el servidor aceptó, pero con errores de objeto. En `te diff`: se encontraron diferencias (como en la convención `diff`/`cmp`). |
| `2`              | Solo en `te diff`: se produjo un error durante la comparación, por lo que se desconoce el estado de las diferencias.                                                                                                                                                                                                                                                                                                            |

Combina los códigos de salida con las anotaciones `--ci <vsts\|github>` y `--trx <file>` para mostrar información detallada sobre los errores en CI; consulta @te-cli-cicd.

## Errores en stderr

Los errores, las advertencias y los avisos de progreso y estado (el indicador giratorio, `Using active connection:`), el recordatorio de uso que aparece tras un error de argumentos y el banner de vista previa se escriben en **stderr**; stdout solo contiene el resultado. Por tanto, un comando rechazado deja stdout vacío, así que una ejecución de simulación capturada es o bien una salida válida o bien nada en absoluto, y puedes canalizar JSON con seguridad sin que se contamine con indicadores de progreso ni mensajes de diagnóstico:

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

## Ejemplo de composición

Generar un script TMSL de actualización y ponerlo bajo control de versiones solo requiere tres comandos:

```bash
te connect MyWorkspace MyModel
te refresh --type full > refresh.tmsl
cat refresh.tmsl
```

El TMSL resultante puede revisarse en un pull request, incluirse en un commit, ejecutarse con la CLI (`te refresh --type full --execute`), entregarse a un DBA o aplicarse con cualquier herramienta compatible con XMLA. La CLI se convierte en un componente en lugar de una caja negra.

## Patrones útiles

Algunos patrones pequeños que aparecen a menudo al componer comandos de `te` en scripts o pipelines:

- **Creaciones y eliminaciones idempotentes de medidas.** `te add Sales/Marker -t Measure -p Expression="0" --if-not-exists --save` y `te remove Sales/OldMeasure --if-exists --save` salen con código `0` exista o no el objeto; es seguro volver a ejecutarlos en CI.
- **Nada persiste sin `--save`.** Los comandos que modifican (`te add`, `te set`, `te move`, `te remove`, `te script`, `te macro run`) aplican el cambio en memoria, generan un Report de lo que han hecho y luego imprimen `Ejecución de simulación: no se guardó nada.`. Agrega --save para que el cambio persista.`Ejecuta uno sin opciones para confirmar que resuelve los objetos que esperas y luego vuelve a ejecutarlo con`--save`. `te remove --dry-run\` va un paso más allá y genera un Report de lo que se quitaría sin aplicar nada.
- **Genera TMSL para revisión.** `te deploy --model ./model --target-server my-workspace --target-database my-model > deploy.tmsl` - deploy se ejecuta en modo de simulación de forma predeterminada e imprime en stdout el TMSL exacto ajustado al destino, por lo que al redirigirlo obtienes el script de implementación sin tocar el servidor. Útil para que lo revise un DBA o para aplicarlo manualmente.
- **Valores canalizados mediante `-`.** Todas las opciones que aceptan un valor leen la entrada estándar stdin canalizada a través de `-` (se quita la nueva línea final, se elimina la marca de orden de bytes; si no se canaliza nada, falla de inmediato): `cat query.dax | te query -q -` (también funciona canalizar la stdin sin `-q`), `te set Sales/Amount -p Expression=- < expr.dax --save`, `cat fix.csx | te script --inline - --save`, `cat messy.dax | te util format-dax -`. Un valor canalizado se toma literalmente: canalizar el texto `null` almacena la palabra `null`, mientras que `-p Name=null` o `--unset Name` borra la propiedad.
- **Descubre los nombres de las propiedades.** `te get <path> --properties --output-format json` devuelve cada nombre que `-p` acepta en ese objeto, junto con su tipo, si es editable y sus valores permitidos; es la lista que debes consultar antes de generar llamadas a `te set`.
- **Conjuntos de cambios analizables.** Los comandos que modifican (`set`, `add`, `remove`, `move`, `script`, `bpa run --fix`) muestran un diff de forma predeterminada; `--stat` y `--name-only` ofrecen alternativas de texto compactas, y `te config set mutationOutput diff|stat|name-only|none` establece un valor predeterminado permanente. La salida JSON siempre incluye la matriz completa `changes` (una entrada por cada objeto cambiado con `objectPath`, `objectType`, `changeKind` y pares de propiedades antes/después) independientemente de estas opciones; es la estructura estable que debes analizar en scripts. `te diff` genera un Report de sus diferencias con la misma estructura.
- **Salida solo con rutas.** `te list --paths-only` y `te find --paths-only` emiten una ruta de objeto por línea, ideal para canalizar la salida a `xargs`, `te get` o `te set`. Los contenedores a nivel de modelo para medidas (`te list Measures`, `te list Columns`) se combinan bien con esto para realizar barridos de todo el modelo.
- **Pruebas de rendimiento de consultas.** `te query --trace --cold --runs 5` ejecuta una consulta DAX con caché en frío, cinco iteraciones y captura eventos de traza de FE/SE.
- **Tiempos por paso en los logs de CI.** Los comandos de larga duración (`te deploy`, `te refresh`, `te script`, `te validate`, `te query`) incluyen un campo `durationMs` en la salida JSON; útil para mostrar los tiempos de cada paso en los resúmenes del pipeline.

## Páginas relacionadas

- @te-cli-cicd - patrones específicos para pipelines y ejemplos en YAML.
- @te-cli-commands - referencia completa de los comandos.
- @te-cli-interactive - cuando el modo interactivo encaja mejor que el uso de scripts.
