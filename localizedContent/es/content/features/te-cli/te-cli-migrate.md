---
uid: te-cli-migrate
title: Migración desde la línea de comandos de TE2
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

# Migración desde la línea de comandos de TE2

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

Los equipos con canalizaciones de compilación existentes que invocan `TabularEditor.exe` con opciones al estilo de TE2 (`-S`, `-A`, `-D`, `-O`, `-C`, etc.) pueden adoptar la nueva CLI de forma gradual. La CLI de Tabular Editor acepta ambos formatos de comandos: la nueva forma basada en subcomandos (`te deploy`, `te bpa run`, …) y la sintaxis heredada de opciones de TE2, mediante una capa de compatibilidad integrada.

Para consultar la referencia heredada de la línea de comandos de TE2 para Windows, ve a @command-line-options.

## Cómo funciona la compatibilidad con TE2

El modo de compatibilidad con TE2 se activa de cualquiera de estas tres maneras:

1. **Nombre del binario.** Cambia el nombre de `te` a `te2` (o crea un enlace simbólico) y la CLI se ejecutará en el modo exacto de TE2. Esta es la vía de reemplazo directo: sustituye `TabularEditor.exe` por `te2` en tu canalización existente y los mismos argumentos funcionarán.
2. **Variable de entorno.** Establece `TE_COMPAT=te2` antes de invocar `te` para forzar el modo TE2.
3. **Detección automática.** Si el primer argumento no es un subcomando de `te` (`deploy`, `validate`, …) y aparece al menos una opción de TE2 reconocida en algún punto de la lista de argumentos, la CLI redirige automáticamente al modo TE2. Esto significa que la mayoría de las invocaciones existentes de TE2 funcionan sin ningún cambio.

```bash
# All three are equivalent - each runs in TE2 mode
./te2 Model.bim -S fix.csx -D "localhost\tabular" MyDB -O
TE_COMPAT=te2 te Model.bim -S fix.csx -D "localhost\tabular" MyDB -O
te Model.bim -S fix.csx -D "localhost\tabular" MyDB -O
```

> [!NOTE]
> El modo TE2 ejecuta la misma canalización `Load → Scripts → Schema Check → Save → BPA → Deploy → TRX` que `TabularEditor.exe`, incluido el comportamiento de las opciones en función del contexto (por ejemplo, `-S` después de `-D` significa `-SHARED`, no `-SCRIPT`).

## El comando `migrate`

Usa `te util migrate` como referencia en vivo de cómo las opciones de TE2 se asignan a la nueva CLI. Muestra una tabla en color con todas las opciones conocidas de TE2, su estado (compatible, renombrada, prevista) y el comando `te` equivalente.

```bash
te util migrate                   # Full flag mapping table
te util migrate -A                # Look up a single flag
te util migrate --output-format json     # Machine-readable mapping
```

Consulta la salida del comando `te util migrate` para ver el mapeo actual, que refleja la versión de la CLI que tienes instalada.

## Mapeo de flags (subconjunto seleccionado)

A continuación se muestra un resumen no exhaustivo de las opciones más usadas. Ejecuta `te util migrate` para ver la lista completa.

| Flag de TE2                                                        | Nuevo equivalente en la CLI                                                                 | Notas                                                                                                                                                                                                                                                                                                                                         |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `file` (posicional)                             | `--model <path>` (opción global)                                         | Siempre es la opción global `--model`; ningún comando toma el modelo como argumento posicional. O establece un modelo activo una vez con `te connect <path>`.                                                                                                                                                 |
| `server`, `database`                                               | `te connect <server> <database>` o las opciones globales `-s <server> -d <database>`        | `-s`/`-d` siempre identifican el origen del modelo; los destinos de despliegue usan `--target-server` / `--target-database`.                                                                                                                                                                                                  |
| `-L` / `-LOCAL`                                                    | `te connect --local`                                                                        | Solo para Windows.                                                                                                                                                                                                                                                                                                            |
| `-S` / `-SCRIPT`                                                   | `te script --file <file.csx>` o `--inline "code"`                                           | También funciona una ruta `.csx` sin más (`te script fix.csx`). Admite varios scripts (`--file a.csx --file b.csx`), código en línea y la entrada estándar stdin (`--inline -`); los archivos y el código en línea se ejecutan en el orden indicado. |
| `-A` / `-ANALYZE`                                                  | `te bpa run --rules <file-or-url>`                                                          | Admite `--fail-on`, `--fix` y varios archivos de reglas.                                                                                                                                                                                                                                                                      |
| `-AX` / `-ANALYZEX`                                                | `te bpa run --rules <file> --no-model-rules`                                                | Las reglas integradas en el modelo se incluyen de forma predeterminada; `--no-model-rules` las excluye, igual que hacía `-AX`.                                                                                                                                                                                                |
| `-B` / `-BIM`                                                      | `te save-as --model <model> -o <file.bim> --serialization bim`                              |                                                                                                                                                                                                                                                                                                                                               |
| `-F` / `-FOLDER`                                                   | `te save-as --model <model> -o <dir> --serialization Database.json`                         | Tras `-D`, el `-F` de TE2 significa `-FULL`. Consulta `--deploy-full`.                                                                                                                                                                                                                                        |
| `-TMDL`                                                            | `te save-as --model <model> -o <dir> --serialization tmdl`                                  | `--serialization` puede omitirse: el formato se infiere a partir de la ruta de salida.                                                                                                                                                                                                                        |
| `-D` / `-DEPLOY`                                                   | `te deploy --model <model> --target-server <server> --target-database <database> --execute` | Comando independiente con opciones con nombre. Sin `--execute`, `te deploy` realiza una simulación e imprime el TMSL que enviaría.                                                                                                                                                                            |
| `-O` / `-OVERWRITE`                                                | (predeterminado) o `--create-only` para no aplicarlo                     | La sobrescritura es el comportamiento predeterminado en la nueva CLI.                                                                                                                                                                                                                                                         |
| `-C` / `-CONNECTIONS`                                              | `te deploy --deploy-connections`                                                            |                                                                                                                                                                                                                                                                                                                                               |
| `-P` / `-PARTITIONS`                                               | `te deploy --deploy-partitions`                                                             |                                                                                                                                                                                                                                                                                                                                               |
| `-Y` / `-SKIPPOLICY`                                               | `te deploy --deploy-partitions --skip-refresh-policy`                                       | Requiere `--deploy-partitions`.                                                                                                                                                                                                                                                                                               |
| `-SHARED`                                                          | `te deploy --deploy-shared-expressions`                                                     | Después de `-D`, `-S` en TE2 significa `-SHARED`.                                                                                                                                                                                                                                                                             |
| `-R` / `-ROLES`                                                    | `te deploy --deploy-roles`                                                                  |                                                                                                                                                                                                                                                                                                                                               |
| `-M` / `-MEMBERS`                                                  | `te deploy --deploy-role-members`                                                           |                                                                                                                                                                                                                                                                                                                                               |
| `-FULL` (después de `-D`)                       | `te deploy --deploy-full`                                                                   | Equivale a: sobrescritura + conexiones + particiones + elementos compartidos + roles + miembros de rol.                                                                                                                                                                                                       |
| `-X` / `-XMLA <file>`                                              | `te deploy ... > <file>` (omite `--execute`)                             | La generación del script es el comportamiento predeterminado: sin `--execute`, `te deploy` se conecta en modo de solo lectura e imprime el TMSL en stdout; redirígelo a un archivo.                                                                                                                           |
| `-V` / `-VSTS`                                                     | `--ci vsts` en `validate`, `bpa run`, `deploy`, `test run`                                  | Emite anotaciones `##vso[...]` en stderr. `azdo` y `azure-devops` son alias aceptados.                                                                                                                                                                                                                        |
| `-G` / `-GITHUB`                                                   | `--ci github` (alias `gh`)                                               | Emite anotaciones `::error::` / `::warning::` / `::notice::`.                                                                                                                                                                                                                                                                 |
| `-T` / `-TRX <file>`                                               | `--trx <file>` en `validate`, `bpa run`, `test run`                                         | Archivo `.trx` de VSTEST para publicar pruebas en Azure DevOps.                                                                                                                                                                                                                                                               |
| `-W` / `-WARN`                                                     | (predeterminado)                                                         | Las advertencias siempre se incluyen en el Report de resultados de la implementación.                                                                                                                                                                                                                                         |
| `-E` / `-ERR`                                                      | (predeterminado)                                                         | La implementación devuelve un código de salida distinto de cero cuando hay errores de DAX.                                                                                                                                                                                                                                    |
| `-SC` / `-SCHEMACHECK`                                             | _Aún no se ha implementado._                                                | La comprobación del esquema de TE2 se conecta a los Data source reales. A diferencia de `te validate` (validación semántica de DAX, sin conexión al Data source).                                                                                                                          |
| `-L` / `-LOGIN <user> <pass>` (después de `-D`) | `te auth login -u <id> -p <secret> -t <tenant>`                                             | Usa una entidad de servicio o credenciales basadas en variables de entorno. El inicio de sesión se guarda en caché, así que los comandos posteriores obtienen tokens de forma silenciosa; consulta @te-cli-auth.                                                                                 |

## Guía de migración

La ruta recomendada para pasar de un pipeline basado en TE2 al nuevo CLI:

1. **Reemplazo directo.** Sustituye `TabularEditor.exe` por `te` (o `te2`) en tu pipeline actual. Comprueba que el pipeline siga funcionando: la compatibilidad con TE2 mantiene intacta la mayoría de las invocaciones.
2. **Sustituye las opciones de forma gradual.** Convierte un grupo de opciones cada vez:
   - Empieza con `-A` / `-AX` → `te bpa run` para obtener una salida de BPA más completa (`--fail-on`, `--fix`, `--trx`).
   - Después, `-D` → `te deploy` para un control de despliegue más detallado.
   - Por último, `-V` / `-G` → `--ci vsts` / `--ci github`.
3. **Cambia a las opciones de CI no interactivas.** Añade `--non-interactive` a todos los comandos `te` (y `--ci <vsts|github>` en `validate`, `bpa run`, `deploy` y `test run`), pasa `--execute --force` en los pasos `deploy`/`refresh` que deban realizar cambios y elimina cualquier wrapper `start /wait`: la nueva CLI es un binario de consola normal y no lo necesita.
4. **Adopta la autenticación con entidad de servicio.** Sustituye `-D -L <user> <pass>` por `te auth login -u ... -p ... -t ...` o un paso del pipeline con credenciales de entorno. Consulta @te-cli-auth.

## Diferencias importantes

- **BPA como control previo al despliegue.** `te deploy` ahora ejecuta BPA como comprobación previa de forma predeterminada. Usa `--skip-bpa` para mantener el comportamiento anterior, o `--fix-bpa` para corregir automáticamente los incumplimientos antes del despliegue. Consulta @te-cli-config.
- **Simulación de forma predeterminada.** `te deploy` y `te refresh` imprimen el TMSL exacto que enviarían y no cambian nada; usa `--execute` para realizar los cambios. `--execute` pide confirmación en la terminal (con `n` como opción segura predeterminada); los pipelines de CI deben pasar `--execute --force`.
- **Salida estructurada.** Todos los comandos admiten `--output-format json` para una salida procesable por máquinas; consulta @te-cli-automation.
- **No hace falta `start /wait`.** La nueva CLI es un binario de consola normal; ejecútalo directamente en scripts de shell, PowerShell y tareas de CI.
- **Multiplataforma.** La CLI funciona en Windows, macOS y Linux. Las conexiones locales a SSAS y Power BI Desktop siguen estando disponibles solo en Windows.

## Páginas relacionadas

- @command-line-options - la referencia heredada de la línea de comandos de TE2.
- @te-cli-commands - la referencia completa de comandos de la nueva CLI.
- @te-cli-cicd - ejemplos de canalizaciones para GitHub Actions y Azure DevOps.
