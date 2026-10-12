---
uid: te-cli-config
title: Configuración personalizada
author: Peer Grønnerup
updated: 2026-10-12
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      none: true
    - product: Tabular Editor CLI
      full: true
---

# Configuración personalizada

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

La CLI de Tabular Editor lee una configuración opcional desde un archivo JSON. The file sets:

- **File paths**: where the CLI reads macros and BPA rules, and where it writes the query log.
- **Behavioral defaults**: BPA gates, auto-format and validation.
- **Saved connection profiles**: the named profiles you switch between.

The CLI doesn't read from or write to Tabular Editor 3 desktop install paths. Set the BPA rules and macros files in this config, or create them with `te bpa rules init` and `te macro init`.

`te config list`, `te config set <key> <value>` and `te profile set` cover the common operations without editing the file.

## Ubicación del archivo de configuración

The CLI checks these locations in order:

1. La variable de entorno `$TE_CONFIG` (si está definida y el archivo existe).
2. `~/.config/te/config.json` (en Windows, `%USERPROFILE%\.config\te\config.json`).
3. Si no hay archivo de configuración, la CLI usa los valores predeterminados integrados.

`te config list`, `te config set`, `te config init` and `te config paths` all read and write the file at the resolved path, including a path set by `TE_CONFIG`. Use `TE_CONFIG` for testing, scripted installs and per-environment configuration.

Para crear una configuración predeterminada:

```bash
te config init             # Create config at TE_CONFIG (or ~/.config/te/config.json)
te config init --force     # Overwrite existing config
```

## Ver la configuración

```bash
te config list                         # Display all settings
te config list --output-format json    # Machine-readable
te config paths                        # Show resolved macros and BPA rule paths
```

`te config paths` shows which files the CLI uses for macros and BPA rules. The output has two rows: `macros`, the resolved macros file path, and `bpa.rules`, the first existing BPA rules file. Either row shows `[not set]` if nothing resolves.

> [!NOTE]
> With `--output-format json`, `te config paths` writes unresolved paths as explicit `null` fields, for example `{"macros": null, "bpa": {"rules": null}}`. `te config list --output-format json` omits null fields by default, so parsers must handle missing keys.

## Configurar valores

```bash
te config set autoFormat true
te config set bpa.onDeploy false
te config set hidePreviewNotice true
te config set macros null              # Clear a path override
te config set -p spinner=false         # -p key=value works too
```

Las claves pueden pasarse por posición (`te config set <key> <value>`) o como `-p key=value`. Las claves desconocidas provocan que el comando finalice con el código de salida `1` y un error que enumera las claves válidas.

Si no existe ningún archivo de configuración, `te config set` crea uno automáticamente en la ruta resuelta (`$TE_CONFIG` si está establecido; de lo contrario, `~/.config/te/config.json`) antes de aplicar el cambio.

> [!NOTE]
> `te config set` sets every key in the schema except `formatVersion`, which the CLI manages. Use dotted paths for nested keys, such as `bpa.onDeploy` or `formatOptions.useSqlBiDaxFormatter`. To edit the JSON directly, run `te config paths` to find the file.

## Esquema completo

The complete config schema, with every key at its default value:

```json
{
  "formatVersion": 2,
  "macros": null,
  "autoFormat": false,
  "validateOnMutation": true,
  "vertipaqOnRefresh": false,
  "mutationOutput": "diff",

  "bpa": {
    "rules": null,
    "onDeploy": true,
    "onSave": true,
    "onMutation": false,
    "builtInRules": true,
    "disabledBuiltInRuleIds": null
  },

  "interactiveEditMode": "stage",
  "launchInteractiveMode": "auto",

  "formatOptions": {
    "shortFormat": false,
    "skipSpaceAfterFunction": false,
    "useSqlBiDaxFormatter": false
  },

  "hidePreviewNotice": false,
  "spinner": true,
  "debug": false,
  "disableTelemetry": false,

  "queryLog": null,

  "profiles": {}
}
```

### Rutas de archivo

Paths set in the config apply to every command. Per-command flags and environment variables override them, as described in [Path resolution priority](#path-resolution-priority).

| Clave       | Significado                                                                                                                                                                                                                                                                                                                                                                                          |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `macros`    | Ruta explícita a un archivo JSON de macros (normalmente `MacroActions.json`). La resuelve cualquier comando `te macro`. To use the same macros on several machines or in both the CLI and Tabular Editor 3, point it at a shared file, such as a file on a network share, in the repository or the Tabular Editor 3 desktop file. |
| `bpa.rules` | Lista ordenada de rutas o URL a archivos de reglas de BPA. `te bpa run` y la compuerta de implementación/guardado cargan **todas** las entradas existentes; `te bpa rules list` y `te config paths` usan la primera entrada existente. Los valores separados por comas en `te config set bpa.rules ...` se separan en el arreglo.                    |
| `queryLog`  | Ruta a un archivo de registro en el que cada invocación de `te query` añade el texto de la consulta y los metadatos de ejecución. Supports `~` for the home directory, for example `~/.config/te/queries.log`.                                                                                                                                                       |

### Prioridad de resolución de rutas

Para cada archivo proporcionado por el usuario (macros, reglas de BPA), la CLI resuelve la ruta en este orden:

1. **Opción de línea de comandos** - `--macros <path>` para comandos de macros; `--bpa-rules <path>` para la compuerta de implementación/guardado; `--rules-file <path>` para los subcomandos de `te bpa rules`.
2. **Variable de entorno** - `TE_MACROS_PATH` para macros, `TE_BPA_RULES` para reglas de BPA.
3. **Configuración de la CLI** - `macros` para macros, la primera entrada existente de `bpa.rules[]` para reglas de BPA.

The CLI doesn't detect Tabular Editor 3 install locations. To create a default file in the current directory, run `te macro init` (creates `./MacroActions.json`) or `te bpa rules init` (creates `./BPARules.json`).

Ejecuta `te config paths` para ver qué archivo resolvió realmente la CLI.

### Valores predeterminados de comportamiento

BPA settings are under the `bpa` object, and you address them with dotted keys in `te config set`.

| Clave                        | Predeterminado | Descripción                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ---------------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `autoFormat`                 | `false`        | Da formato automáticamente a las expresiones DAX modificadas por un comando de modificación. El formato se limita a los objetos que el comando haya modificado, pero abarca todas las propiedades de expresiones DAX que contengan (expresiones, expresiones de cadena de formato dinámica, filas de detalle, objetivo/estado/tendencia del KPI, expresiones de grupo de cálculo y de permiso de tabla, etc.). Las consultas de partición de Power Query (M) y SQL nunca se reformatean. Siempre usa el formateador integrado sin conexión en el dialecto de comas; se aplican las claves de diseño de `formatOptions`. |
| `validateOnMutation`         | `true`         | Después de un comando de modificación (`add`, `set`, `mv`, `macro run`), comprueba que todas las referencias `Table[Column]` del modelo sigan resolviéndose. This catches references broken by renames or removals before deployment.                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `mutationOutput`             | `diff`         | How mutating commands (`add`, `set`, `move`, `remove`, `script`, `bpa run --fix`) render the resulting change set in text output: `diff` (full before/after diff), `stat` (per-object change counts), `name-only` (changed object paths), or `none` (no change set; config only, with no `--none` flag). The `--diff`, `--stat` and `--name-only` flags override it for one invocation. JSON output always contains the full `changes` array.                                                                                                                                  |
| `bpa.onMutation`             | `false`        | Ejecuta un análisis de BPA acotado después de cada comando de modificación (`set`, `add`, `mv`, `rm`, `macro run`). Only the objects of the affected table are checked.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `bpa.onDeploy`               | `true`         | Ejecuta el control de BPA antes de que se ejecute `te deploy`. El despliegue se cancela si alguna regla se activa con una gravedad >= error. Omítelo en una invocación concreta con `--skip-bpa`, o corrígelo automáticamente con `--fix-bpa`.                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `bpa.onSave`                 | `true`         | Ejecuta el control de BPA antes de que `te save-as` escriba en disco. Omítelo en una invocación concreta con `--skip-bpa` o `--force`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `bpa.builtInRules`           | `true`         | Incluye el conjunto depurado de reglas integradas de BPA cada vez que se ejecute el control. If `false`, the gate runs only the rules in `bpa.rules` and rules embedded in the model.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `bpa.disabledBuiltInRuleIds` | `null`         | ID de reglas integradas individuales que se excluirán de la puerta de calidad. Change it with `te bpa rules disable <id>` and `te bpa rules enable <id>`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `vertipaqOnRefresh`          | `false`        | After a successful refresh (`full`, `dataonly`, `automatic`, or `add`), run VertiPaq analysis and show storage statistics for the refreshed tables.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `interactiveEditMode`        | `stage`        | Comportamiento predeterminado para las mutaciones en memoria dentro de `te interactive`. `stage` keeps mutations in memory until you run `save`. `save` writes to the source after every mutating command; on a remote source, every `set` is an XMLA write. `revert` discards mutations after each command unless you pass `--save` or `--stage`. The per-command `--save`, `--revert` and `--stage` flags override the setting.                                                                                                                                                                                                                             |
| `launchInteractiveMode`      | `auto`         | Indica si ejecutar `te` en un terminal sin argumentos inicia el REPL interactivo. `auto` (default) launches the REPL only if stdin, stdout and stderr are all attached to a TTY, so scripts and CI pipelines get normal parsing. `always` launches the REPL even with redirection. `never` shows help instead. The global `--non-interactive` flag forces `never` for one invocation, and the `TE_INTERACTIVE` environment variable sets the mode for one invocation.                                                                                                                                                                      |
| `disableTelemetry`           | `false`        | Desactiva la telemetría de uso anónima. Telemetry contains the command name, exit code and duration. It doesn't contain model content, paths or query text.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |

```bash
te config set bpa.rules "/etc/te/team.json,/etc/te/strict.json"
te config set bpa.onDeploy true
te config set bpa.builtInRules false
te config set bpa.disabledBuiltInRuleIds "TE3_BUILT_IN_DATE_TABLE_EXISTS,TE3_BUILT_IN_HIDE_FOREIGN_KEYS"
```

### Opciones de formato

The CLI's built-in DAX formatter works offline.

- The layout keys `shortFormat` and `skipSpaceAfterFunction` apply when `autoFormat` reformats mutated expressions and when `te query` renders query text.
- `te set <path> --format <Property>` and `te util format-dax` ignore the layout keys and take the flags `--long` and `--no-space-after-function`.
- Config-driven formatting always uses commas as list separators. For DAX written with semicolons, use the `--semicolons` flag of `te util format-dax`.
- `formatOptions.useSqlBiDaxFormatter` sends explicit formatting and `te query` rendering to the SQL BI [daxformatter.com](https://www.daxformatter.com) web service, which requires internet access. `autoFormat` always uses the built-in formatter.

| Clave                                  | Predeterminado | Descripción                                                                                                                                                                                                                                       |
| -------------------------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `formatOptions.shortFormat`            | `false`        | Use short, single-line formatting where possible.                                                                                                                                                                                 |
| `formatOptions.skipSpaceAfterFunction` | `false`        | Omit the space between a function name and its opening parenthesis, for example `SUM(x)`.                                                                                                                                         |
| `formatOptions.useSqlBiDaxFormatter`   | `false`        | Format DAX with the [SQL BI daxformatter.com](https://www.daxformatter.com) web service. Requiere acceso a Internet. The built-in formatter matches the Tabular Editor 3 default. |

### Visualización

These settings control terminal output and diagnostic logging.

| Clave               | Predeterminado | Descripción                                                                                                                                   |
| ------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `hidePreviewNotice` | `false`        | Suprime el banner amarillo de vista previa. **Se ignora cuando faltan menos de 14 días para el vencimiento.** |
| `spinner`           | `true`         | Muestra indicadores de progreso animados en el terminal. Desactivar para CI.                                  |
| `debug`             | `false`        | Activa siempre el registro de depuración (equivale a pasar `--debug`).                                     |

### Perfiles

Saved connection profiles are stored under the `profiles` key. Manage them with `te profile set`, `te profile remove` and `te profile list`, not by editing the file. Consulta @te-cli-auth.

A profile can override these behavioral defaults while it's active: `autoFormat`, `validateOnMutation`, `mutationOutput`, `bpa.onMutation`, `bpa.onDeploy`, `bpa.onSave`, `vertipaqOnRefresh`, `spinner` and `interactiveEditMode`. For example, a dev profile can turn off validation and the deploy gate while a prod profile formats DAX:

```bash
te profile set dev --validate-on-mutation false --bpa-on-deploy false
te profile set prod --auto-format true
```

`te profile set` has flags for `--auto-format`, `--validate-on-mutation`, `--bpa-on-mutation`, `--bpa-on-deploy`, `--vertipaq-on-refresh` and `--spinner`. Each accepts `true`, `false` or `null`, which clears the override.

## Control BPA

The BPA gate stops a save or deployment if the model has rule violations at error severity. It runs on these commands:

- `te deploy` ejecuta el control, a menos que se pase `--skip-bpa` o que `bpa.onDeploy` sea `false`.
- `te save-as` ejecuta la validación, a menos que se pase `--skip-bpa` (o `--force`) o que `bpa.onSave` sea `false`.
- `te add`, `te set`, `te move`, `te remove`, `te macro run` ejecutan la validación solo cuando `bpa.onMutation` es `true`.

El control carga las reglas de BPA desde `bpa.rules` y, de forma predeterminada, el conjunto de reglas integrado (controlado por `bpa.builtInRules`). `te bpa rules disable <id>` excludes an individual built-in rule by adding it to `bpa.disabledBuiltInRuleIds`, and `te bpa rules enable <id>` removes it from the list.

If the gate finds violations at severity `error` or higher, the command fails with exit code `1` and a summary of the violations. To proceed, use one of these options:

- `--fix-bpa` - aplica en memoria la `fixExpression` de la regla al artefacto que se va a desplegar o guardar; los archivos fuente no se modifican.
- `--skip-bpa` - desactiva el control solo para este comando.
- `--bpa-rules <path>` - repetible; sobrescribe `bpa.rules` para esta única invocación de `te deploy` o `te save-as`. Las reglas integradas siguen aplicándose salvo que `bpa.builtInRules` sea `false`.

To check the model against the rules without deploying, run `te bpa run`:

```bash
te bpa run --model ./model --fail-on error
te bpa run --model ./model --fix --save     # Apply fixes to the source
```

### Reglas de BPA integradas

The CLI includes a set of built-in BPA rules. Built-in rules are read-only: `te bpa rules set` and `te bpa rules remove` fail on built-in IDs and suggest `te bpa rules disable`. To change a built-in rule, copy it into your rules file with a new ID and disable the built-in rule.

`bpa.builtInRules` and `bpa.disabledBuiltInRuleIds` apply to the gate and to `te bpa run`, so a rule disabled with `te bpa rules disable` is excluded everywhere.

## Comportamiento tras la mutación

After a mutating command (`te add`, `te set`, `te move` or `te macro run`), the CLI runs these checks:

1. **TOM errors** always appear. Invalid DAX or M in measures, columns, partitions or calculation items fails the command.
2. **Schema validation** (`validateOnMutation`, default `true`) verifies that `Table[Column]` references in DAX still resolve.
3. **DAX auto-format** (`autoFormat`, default `false`) formats the expressions touched by the mutation with the built-in formatter.
4. **BPA on mutation** (`bpa.onMutation`, default `false`) runs BPA after the mutation and warns or fails according to `--fail-on`.

`te config set <key> false` turns a check off. A profile can override the key for one environment.

## Políticas de administrador

On Windows, `te` honors the same administrator policies as Tabular Editor 3 and reads them from these registry keys:

- `Software\Policies\Tabular Editor ApS`, for values shared by the CLI and the desktop application
- its `TECLI` subkey, for values that apply to the CLI only
- its `TE3` subkey, for values that apply to the desktop application only
- the earlier `Software\Policies\Kapacity\Tabular Editor` key, which is still honored

A machine-wide value (`HKEY_LOCAL_MACHINE`) takes precedence over a per-user one (`HKEY_CURRENT_USER`). Within a hive, a product-specific value takes precedence over a shared one. When a policy turns a feature off, the command names the policy, does nothing and exits with a failure, which fails any pipeline step that depends on the feature.

| Política               | Efecto en la CLI                                                                                                                                                                                                                                                                                                                                               |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DisableCSharpScripts` | Blocks `te script` and the automatic fixes of `te bpa run --fix`.                                                                                                                                                                                                                                                                              |
| `DisableMacros`        | Blocks every `te macro` command.                                                                                                                                                                                                                                                                                                               |
| `DisableBpaDownload`   | Blocks Best Practice Analyzer rules given as a URL. Los archivos de reglas en disco y las reglas integradas no se ven afectados.                                                                                                                                                                                               |
| `DisableTelemetry`     | Desactiva las estadísticas anónimas de uso, independientemente de lo que indique `disableTelemetry` en la configuración.                                                                                                                                                                                                                       |
| `BlockUnsafeScripts`   | Blocks `te script`, `te macro run` and `te bpa run --fix` when the code accesses files, the network, processes or external assemblies. See [What counts as staying within the model](xref:csharp-scripts#what-counts-as-staying-within-the-model) for the blocked APIs. JSON output reports `blockedByPolicy`. |

Policies for update checks, error reports, DAX Optimizer, the DAX Package Manager, the AI Assistant and the MCP server don't affect the CLI. Consulta @policies para ver la lista completa de directivas y cómo implementarlas.

In the desktop application, `BlockUnsafeScripts` requires Tabular Editor 3 Enterprise Edition. The CLI has no editions and applies the policy wherever it's set.

## Variables de entorno

The CLI reads these environment variables for paths, behavior and diagnostics. Para las variables de autenticación de Azure (`AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_CLIENT_CERTIFICATE_PATH`, etc.), consulta @te-cli-auth.

| Variable         | Propósito                                                                                                                                                                                                                                                                                                                               |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TE_CONFIG`      | Ruta de acceso a un archivo de configuración alternativo. Used by `te config list`, `set`, `init` and `paths`.                                                                                                                                                                                          |
| `TE_MACROS_PATH` | Override the macros file path, second in the [resolution order](#path-resolution-priority). La leen los comandos `te macro`.                                                                                                                                                                            |
| `TE_BPA_RULES`   | Anula la lista de archivos/URL de reglas de BPA utilizada por los subcomandos `te bpa run` y `te bpa rules`.                                                                                                                                                                                                            |
| `TE_BPA_CONFIG`  | Anula la ruta de acceso a la configuración del gate de BPA (`.te-bpa.json`) que lee el gate de despliegue/guardado.                                                                                                                                                                                  |
| `TE_DEBUG`       | Establece el valor en `1` para habilitar el registro de depuración globalmente (igual que `--debug` o `debug: true` en la configuración).                                                                                                                                                            |
| `NO_SPINNER`     | Establece el valor en `1` o `true` para desactivar los indicadores de progreso animados (alternativa a `spinner: false` en la configuración).                                                                                                                                                        |
| `CI`             | Se detecta automáticamente. Cuando vale `1` o `true`, la CLI desactiva el spinner y cambia a una salida de texto sin formato. Most CI runners set it.                                                                                                                                   |
| `TE_SESSION`     | Sobrescribe el identificador de sesión por terminal que se usa para el estado de la conexión activa. Set it to run isolated CLI sessions in the same shell, for example in parallel CI matrix jobs. Inspeccione y administre sesiones con [`te session`](xref:te-cli-commands#session). |
| `TE_INTERACTIVE` | Permite anular `launchInteractiveMode` para una sola invocación. Accepts `auto`, `always` or `never`. `TE_INTERACTIVE=always` launches the REPL, and `TE_INTERACTIVE=never` shows help.                                                                                                 |
| `TE_COMPAT`      | Establécela en `te2` para forzar el modo de compatibilidad con TE2; consulta @te-cli-migrate.                                                                                                                                                                                                              |

## Pasos a seguir

- @te-cli-auth - perfiles, autenticación y almacenamiento de credenciales.
- @te-cli-commands - subcomandos de `te config`.
- @te-cli-cicd - configuración del gate de BPA para pipelines.
