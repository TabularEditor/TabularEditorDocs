---
uid: te-cli-migrate
title: Migración desde la línea de comandos de TE2
author: Peer Grønnerup
updated: 2026-10-27
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

Los scripts (`-S`) en el modo TE2 se comportan como lo hacían en Tabular Editor 2:

- **Un script fallido detiene la ejecución.** Si un script genera un error o no se compila, la ejecución finaliza con el código `1` antes de que se guarde, analice o implemente nada. No hay ningún resultado de compilación (`-B`, `-F`, `-TMDL`), ningún resultado de BPA ni ningún archivo `-T`, y cualquier resultado de una ejecución anterior se mantiene tal como estaba. Un paso del «pipeline» que siempre lee el archivo `.trx` debe gestionar su ausencia.
- **Los errores de compilación muestran dónde se encuentran.** Cada error se escribe en stdout como `Error <code> on line <line>, col <column>: <message>`. Con `-V` o `-G`, se convierte en una anotación que señala la línea en el archivo de script.
- **Cada script se ejecuta como un solo cambio.** Los cambios posteriores, como la corrección de DAX que hace referencia a una columna cuyo nombre se ha cambiado, se aplican cuando finaliza el script, y no después de cada sentencia. Un script que cambia el nombre de una columna y luego lee una medida que la usa ve la expresión antigua hasta que finaliza el script.
- **`TECLI` está definido.** Los scripts ven el símbolo del preprocesador `TECLI` y no `TE3`, como ocurre con `te script`. Tabular Editor 2 no define ninguno de los dos.

## El comando `migrate`

Usa `te util migrate` como referencia en tiempo real para ver cómo se asignan las opciones de TE2 a la nueva CLI. Muestra una tabla en color con todas las opciones conocidas de TE2, su estado (compatible, renombrada, prevista) y el comando `te` equivalente.

```bash
te util migrate                   # Full flag mapping table
te util migrate -A                # Look up a single flag
te util migrate --output-format json     # Machine-readable mapping
```

Consulta la salida del comando `te util migrate` para conocer el mapeo actual, que refleja la versión de la CLI que tienes instalada.

## Mapeo de flags (subconjunto seleccionado)

A continuación se presenta un resumen no exhaustivo de las opciones más utilizadas. Ejecuta `te util migrate` para ver la lista completa.

| Flag de TE2                                                        | Nuevo equivalente en la CLI                                                                 | Notas                                                                                                                                                                                                                                                                                                                                      |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `file` (posicional)                             | `--model <path>` (opción global)                                         | Siempre se usa la opción global `--model`; ningún comando acepta el modelo como argumento posicional. O establece un modelo activo una vez con `te connect <path>`.                                                                                                                                        |
| `server`, `database`                                               | `te connect <server> <database>` o bien las opciones globales `-s <server> -d <database>`   | `-s`/`-d` siempre identifican el origen del modelo; los destinos de implementación usan `--target-server` / `--target-database`.                                                                                                                                                                                           |
| `-L` / `-LOCAL`                                                    | `te connect --local`                                                                        | Solo para Windows.                                                                                                                                                                                                                                                                                                         |
| `-S` / `-SCRIPT`                                                   | `te script --file <file.csx>` o `--inline "code"`                                           | También funciona indicar solo la ruta a un archivo `.csx` (`te script fix.csx`). Admite varios scripts (`--file a.csx --file b.csx`), código en línea y stdin (`--inline -`); los archivos y el código en línea se ejecutan en el orden indicado. |
| `-A` / `-ANALYZE`                                                  | `te bpa run --rules <file-or-url>`                                                          | Admite `--fail-on`, `--fix` y varios archivos de reglas.                                                                                                                                                                                                                                                                   |
| `-AX` / `-ANALYZEX`                                                | `te bpa run --rules <file> --no-model-rules`                                                | Las reglas integradas en el modelo se incluyen de forma predeterminada; `--no-model-rules` las excluye, como hacía `-AX`.                                                                                                                                                                                                  |
| `-B` / `-BIM`                                                      | `te save-as --model <model> -o <file.bim> --serialization bim`                              |                                                                                                                                                                                                                                                                                                                                            |
| `-F` / `-FOLDER`                                                   | `te save-as --model <model> -o <dir> --serialization database.json`                         | Tras `-D`, el `-F` de TE2 significa `-FULL`. Consulta `--deploy-full`.                                                                                                                                                                                                                                     |
| `-TMDL`                                                            | `te save-as --model <model> -o <dir> --serialization tmdl`                                  | `--serialization` puede omitirse: el formato se infiere a partir de la ruta de salida.                                                                                                                                                                                                                     |
| `-D` / `-DEPLOY`                                                   | `te deploy --model <model> --target-server <server> --target-database <database> --execute` | Comando independiente con opciones con nombre. Sin `--execute`, `te deploy` realiza una ejecución de prueba que imprime el TMSL que enviaría.                                                                                                                                                              |
| `-O` / `-OVERWRITE`                                                | (predeterminado) o `--create-only` para no aplicarlo                     | La sobrescritura es el comportamiento predeterminado en la nueva CLI.                                                                                                                                                                                                                                                      |
| `-C` / `-CONNECTIONS`                                              | `te deploy --deploy-connections`                                                            |                                                                                                                                                                                                                                                                                                                                            |
| `-P` / `-PARTITIONS`                                               | `te deploy --deploy-partitions`                                                             |                                                                                                                                                                                                                                                                                                                                            |
| `-Y` / `-SKIPPOLICY`                                               | `te deploy --deploy-partitions --skip-refresh-policy`                                       | Requiere `--deploy-partitions`.                                                                                                                                                                                                                                                                                            |
| `-SHARED`                                                          | `te deploy --deploy-shared-expressions`                                                     | Después de `-D`, `-S` en TE2 significa `-SHARED`.                                                                                                                                                                                                                                                                          |
| `-R` / `-ROLES`                                                    | `te deploy --deploy-roles`                                                                  |                                                                                                                                                                                                                                                                                                                                            |
| `-M` / `-MEMBERS`                                                  | `te deploy --deploy-role-members`                                                           |                                                                                                                                                                                                                                                                                                                                            |
| `-FULL` (después de `-D`)                       | `te deploy --deploy-full`                                                                   | Equivale a: sobrescritura + conexiones + particiones + elementos compartidos + roles + miembros de rol.                                                                                                                                                                                                    |
| `-X` / `-XMLA <file>`                                              | `te deploy ... > <file>` (omite `--execute`)                             | La emisión de scripts es el comportamiento predeterminado: sin `--execute`, deploy se conecta en modo de solo lectura y muestra el TMSL en stdout; redirígelo a un archivo.                                                                                                                                |
| `-V` / `-VSTS` | `--ci vsts` en `validate`, `bpa run`, `schemacheck`, `deploy`, `test run` | Emite anotaciones `##vso[...]` a stderr. `azdo` y `azure-devops` son alias aceptados. |
| `-G` / `-GITHUB`                                                   | `--ci github` (alias `gh`)                                               | Emite anotaciones `::error::` / `::warning::` / `::notice::`.                                                                                                                                                                                                                                                              |
| `-T` / `-TRX <file>` | `--trx <file>` en `validate`, `bpa run`, `schemacheck`, `test run` | Archivo VSTEST `.trx` para la publicación de pruebas de Azure DevOps. |
| `-W` / `-WARN`                                                     | (predeterminado)                                                         | Las advertencias siempre se incluyen en el Report de resultados de la implementación.                                                                                                                                                                                                                                      |
| `-E` / `-ERR`                                                      | (predeterminado)                                                         | La implementación devuelve un código de salida distinto de cero cuando hay errores de DAX.                                                                                                                                                                                                                                 |
| `-SC` / `-SCHEMACHECK` | `te schemacheck` | Mismos códigos de salida que TE2 y comprueba más tipos de tablas; consulte [Comprobación del esquema](#schema-check). |
| `-L` / `-LOGIN <user> <pass>` (después de `-D`) | `te auth login -u <id> -p <secret> -t <tenant>`                                             | Usa una entidad de servicio o credenciales basadas en variables de entorno. El inicio de sesión se guarda en caché, así que los comandos posteriores obtienen tokens de forma silenciosa; consulta @te-cli-auth.                                                                              |

## Guía de migración

La ruta recomendada para pasar de un pipeline basado en TE2 al nuevo CLI:

1. **Reemplazo directo.** Sustituye `TabularEditor.exe` por `te` (o `te2`) en tu pipeline actual. Comprueba que el pipeline siga funcionando: la compatibilidad con TE2 mantiene intacta la mayoría de las invocaciones.
2. **Sustituye las opciones de forma incremental.** Convierte un grupo de opciones a la vez:
   - Empieza con `-A` / `-AX` → `te bpa run` para obtener una salida de BPA más completa (`--fail-on`, `--fix`, `--trx`).
   - A continuación, `-SC` → `te schemacheck`, que también comprueba las tablas de Power Query y Direct Lake.
   - Después, `-D` → `te deploy` para un control de despliegue más detallado.
   - Por último, `-V` / `-G` → `--ci vsts` / `--ci github`.
3. **Cambie a indicadores de CI no interactivos.** Añada `--non-interactive` a todos los comandos `te` (y `--ci <vsts|github>` en `validate`, `bpa run`, `schemacheck`, `deploy` y `test run`), pase `--execute --force` en los pasos `deploy`/`refresh` que deban actuar y elimine cualquier contenedor `start /wait`: la nueva CLI es un binario de consola normal y no los necesita.
4. **Adopta la autenticación con entidad de servicio.** Sustituye `-D -L <user> <pass>` por `te auth login -u ... -p ... -t ...` o un paso del pipeline con credenciales de entorno. Consulta @te-cli-auth.

## Diferencias importantes

- **BPA como control previo al despliegue.** `te deploy` ahora ejecuta BPA como comprobación previa de forma predeterminada. Usa `--skip-bpa` para mantener el comportamiento anterior, o `--fix-bpa` para corregir automáticamente los incumplimientos antes del despliegue. Consulta @te-cli-config.
- **Simulación de forma predeterminada.** `te deploy` y `te refresh` imprimen el TMSL exacto que enviarían y no cambian nada; usa `--execute` para ejecutar la operación. `--execute` solicita confirmación en una terminal (con `n` como valor predeterminado seguro); las canalizaciones de CI deben pasar `--execute --force`.
- **Salida estructurada.** Todos los comandos admiten `--output-format json` para una salida procesable por máquinas; consulta @te-cli-automation.
- **No hace falta `start /wait`.** La nueva CLI es un binario de consola normal; ejecútalo directamente en scripts de shell, PowerShell y tareas de CI.
- **Multiplataforma.** La CLI funciona en Windows, macOS y Linux. Las conexiones locales a SSAS y Power BI Desktop siguen estando disponibles solo en Windows.

## Comprobación de esquema

Hay dos formas de ejecutar la comprobación de esquemas de Tabular Editor 2 con la nueva CLI:

- **`te2 <model> -SC`** funciona como antes. Solo comprueba las tablas que Tabular Editor 2 ha comprobado, las particiones de consultas heredadas en un origen de datos del proveedor y escribe los mismos resultados `-T`. Úselo para mover una canalización sin cambiar su resultado.
- **[`te schemacheck`](xref:te-cli-commands#schemacheck)** es el comando para los nuevos pipelines. También comprueba las tablas de Power Query (M) y Direct Lake, y admite la salida en formato JSON.

Ambos utilizan los códigos de salida de Tabular Editor 2: una columna de origen añadida o reescrita es una advertencia y finaliza con el código `0`, y una columna de origen faltante, o una consulta heredada que no se puede leer, es un error y finaliza con el código `1`. Ambos respetan las anotaciones de comprobación de esquemas de Tabular Editor 2, excepto `TabularEditor_AddFalseWhereClause`.

Diferencias con respecto a Tabular Editor 2:

- **Algunos orígenes ya no se comprueban.** Una partición de consulta heredada en Oracle, ODBC o un proveedor OLE DB distinto de SQL Server aparece en **No comprobada** y no hace que falle la ejecución. Los proveedores OLE DB de SQL Server solo se comprueban en Windows.
- **El archivo `-T` de `te2 -SC` coincide con el de Tabular Editor 2.** Tiene cuatro resultados por tabla, denominados `Table '<name>' <assertion>`, por lo que Azure DevOps conserva el historial de pruebas. Una tabla de uno de los orígenes anteriores obtiene cuatro resultados **Inconcluyentes**. `te schemacheck --trx` escribe un archivo diferente, con un resultado por hallazgo.
- **Las columnas de origen duplicadas ya no detienen la ejecución.** Tabular Editor 2 mostraba un cuadro de diálogo cuando una fuente devolvía la misma columna dos veces. La CLI lo informa una vez como información.

## Páginas relacionadas

- @command-line-options - la referencia heredada de la línea de comandos de TE2.
- @te-cli-commands - la referencia completa de comandos de la nueva CLI.
- @te-cli-cicd - ejemplos de canalizaciones para GitHub Actions y Azure DevOps.
