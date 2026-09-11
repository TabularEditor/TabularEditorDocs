---
uid: te-cli-config
title: Configuración personalizada
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

# Configuración personalizada

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

La CLI de Tabular Editor lee una configuración opcional desde un archivo JSON. La configuración controla tres cosas:

- **File paths** - where the CLI reads macros and BPA rules, and where to write the query log.
- **Valores predeterminados de comportamiento** — controles de BPA, formato automático y validación.
- **Perfiles de conexión guardados** — la lista de perfiles con nombre entre los que puedes alternar.

La CLI es independiente: no lee ni escribe en ningún PATH de instalación de la versión de escritorio de Tabular Editor 3. Los archivos de reglas de BPA y de macros deben definirse explícitamente en esta configuración (o inicializarse cuando haga falta con `te bpa rules init` / `te macro init`).

La mayoría de los usuarios no necesitan editar el archivo de configuración directamente: `te config list`, `te config set <key> <value>` y `te profile set` cubren las operaciones habituales.

## Ubicación del archivo de configuración

Se comprueban las siguientes ubicaciones en este orden:

1. La variable de entorno `$TE_CONFIG` (si está definida y el archivo existe).
2. `~/.config/te/config.json` (en Windows, `%USERPROFILE%\.config\te\config.json`).
3. Si no hay archivo de configuración, la CLI usa los valores predeterminados integrados.

`TE_CONFIG` se tiene en cuenta de forma coherente en todas las operaciones del archivo de configuración: `te config list`, `te config set`, `te config init` y `te config paths` leen y escriben en la ruta resuelta. Está pensado principalmente para pruebas, instalaciones mediante scripts y configuración por entorno.

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

Usa `te config paths` para ver qué archivos usará realmente la CLI para las macros y las reglas de BPA. Es útil para depurar por qué faltan archivos de datos. La salida muestra dos filas: `macros` (la ruta del archivo de macros resuelta o `[not set]`) y `bpa.rules` (el primer archivo de reglas de BPA existente resuelto por el resolvedor de rutas, o `[not set]`).

> [!NOTE]
> `te config paths` emite campos `null` explícitamente en el modo `--output-format json` (por ejemplo, `{"macros": null, "bpa": {"rules": null}}`). Informar de los resultados de la resolución es precisamente el propósito del comando, así que `null` es una respuesta significativa: «se intentó, pero no se resolvió nada». `te config list --output-format json` elimina los campos `null` de forma predeterminada, así que conviene que quien lo consuma lo interprete con tolerancia.

## Configurar valores

```bash
te config set autoFormat true
te config set bpa.onDeploy false
te config set hidePreviewNotice true
te config set macros null              # Clear a path override
te config set -p spinner=false         # -p key=value works too
```

Keys can be passed positionally (`te config set <key> <value>`) or as `-p key=value`. Las claves desconocidas provocan que el comando finalice con el código de salida `1` y un error que enumera las claves válidas.

Si no existe ningún archivo de configuración, `te config set` crea uno automáticamente en la ruta resuelta (`$TE_CONFIG` si está establecido; de lo contrario, `~/.config/te/config.json`) antes de aplicar el cambio.

> [!NOTE]
> Puedes establecer cualquier clave del esquema mediante `te config set`, incluidas las claves anidadas mediante rutas con puntos (`bpa.onDeploy`, `formatOptions.useSqlBiDaxFormatter`, etc.). La única excepción es `formatVersion`, que la CLI administra automáticamente. Ejecuta `te config paths` para encontrar el archivo de configuración si prefieres editar el JSON directamente.

## Esquema completo

El esquema completo de configuración JSON con todas las claves en sus valores predeterminados. Úsalo como referencia al editar directamente el archivo de configuración o al buscar la ruta con puntos para una llamada a `te config set`.

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

Configúralas en tu configuración para evitar pasar las mismas rutas en cada comando. Las opciones específicas de cada comando y las variables de entorno prevalecen sobre los valores de configuración; consulta [Prioridad de resolución de rutas](#path-resolution-priority) más abajo.

| Clave       | Significado                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `macros`    | Ruta explícita a un archivo JSON de macros (normalmente `MacroActions.json`). La resuelve cualquier comando `te macro`. Apunta a un archivo compartido (un recurso compartido de red, un archivo local del repositorio o incluso el archivo de escritorio de TE3) para reutilizar el mismo conjunto de macros en distintos equipos y entre la CLI y TE3 Desktop. |
| `bpa.rules` | Lista ordenada de rutas o URL a archivos de reglas de BPA. `te bpa run` y la compuerta de implementación/guardado cargan **todas** las entradas existentes; `te bpa rules list` y `te config paths` usan la primera entrada existente. Los valores separados por comas en `te config set bpa.rules ...` se separan en el arreglo.                                                                      |
| `queryLog`  | Ruta a un archivo de registro en el que cada invocación de `te query` añade el texto de la consulta y los metadatos de ejecución. Útil para mantener registros de auditoría o analizar patrones de consulta a lo largo del tiempo. Admite `~` para el directorio personal (p. ej., `~/.config/te/queries.log`).                                     |

### Prioridad de resolución de rutas

Para cada archivo proporcionado por el usuario (macros, reglas de BPA), la CLI resuelve la ruta en este orden:

1. **Opción de línea de comandos** - `--macros <path>` para comandos de macros; `--bpa-rules <path>` para la compuerta de implementación/guardado; `--rules-file <path>` para los subcomandos de `te bpa rules`.
2. **Variable de entorno** - `TE_MACROS_PATH` para macros, `TE_BPA_RULES` para reglas de BPA.
3. **Configuración de la CLI** - `macros` para macros, la primera entrada existente de `bpa.rules[]` para reglas de BPA.

La CLI no detecta automáticamente ninguna ubicación de instalación de TE3; configúralas explícitamente. Para empezar con un archivo predeterminado en el directorio de trabajo actual, ejecuta `te macro init` (crea `./MacroActions.json`) o `te bpa rules init` (crea `./BPARules.json`).

Ejecuta `te config paths` para ver qué archivo resolvió realmente la CLI.

### Valores predeterminados de comportamiento

Toda la configuración relacionada con BPA está en el objeto `bpa` y se referencia mediante claves con puntos en `te config set`.

| Clave                        | Predeterminado | Descripción                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ---------------------------- | -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `autoFormat`                 | `false`        | Automatically format the DAX expressions changed by a mutating command. Formatting is scoped to the objects the command touched but covers every DAX expression property they hold (expressions, format string expressions, detail rows, KPI target/status/trend, calculation group and table permission expressions, etc.). Power Query (M) and SQL partition queries are never reformatted. Always uses the built-in offline formatter in the comma dialect; the `formatOptions` layout keys apply.                                                                                                                                                                                                |
| `validateOnMutation`         | `true`         | After a mutating command (`add`, `set`, `mv`, `macro run`), check that every `Table[Column]` reference in the model still resolves. Detecta referencias huérfanas introducidas por cambios de nombre o eliminaciones antes de llegar al despliegue.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `mutationOutput`             | `diff`         | How mutating commands (`add`, `set`, `move`, `remove`, `script`, `bpa run --fix`) render the resulting change set in text output: `diff` (full before/after diff), `stat` (per-object change counts), `name-only` (changed object paths), or `none` (suppress the change set; config-only - there is no `--none` flag). The per-command `--diff` / `--stat` / `--name-only` flags override for one invocation. JSON output always carries the full `changes` array regardless.                                                                                                                                                                              |
| `bpa.onMutation`             | `false`        | Ejecuta un análisis de BPA acotado después de cada comando de modificación (`set`, `add`, `mv`, `rm`, `macro run`). Solo se comprueban los objetos de la tabla afectada, no los de todo el modelo; útil para obtener retroalimentación rápida durante ediciones iterativas.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `bpa.onDeploy`               | `true`         | Ejecuta el control de BPA antes de que se ejecute `te deploy`. El despliegue se aborta si se dispara alguna regla con una gravedad >= error. Omítelo en una invocación concreta con `--skip-bpa`, o corrígelo automáticamente con `--fix-bpa`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `bpa.onSave`                 | `true`         | Run the BPA gate before `te save-as` writes to disk. Omítelo en una invocación concreta con `--skip-bpa` o `--force`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `bpa.builtInRules`           | `true`         | Incluye el conjunto depurado de reglas integradas de BPA cada vez que se ejecute el control. Configúralo en `false` para ignorar por completo las reglas integradas; entonces el control ejecutará solo las reglas configuradas mediante `bpa.rules` y cualquier regla incrustada en el modelo.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `bpa.disabledBuiltInRuleIds` | `null`         | ID de reglas integradas individuales que se excluirán de la puerta de calidad. Este valor se modifica mediante `te bpa rules disable <id>` / `te bpa rules enable <id>`; es preferible usar esos comandos en lugar de editar el arreglo directamente.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `vertipaqOnRefresh`          | `false`        | Tras una actualización correcta (`full`, `dataonly`, `automatic` o `add`), ejecuta automáticamente el análisis de VertiPaq para mostrar estadísticas de almacenamiento de las tablas actualizadas. Útil para detectar de inmediato regresiones inesperadas de cardinalidad o memoria.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `interactiveEditMode`        | `stage`        | Comportamiento predeterminado para las mutaciones en memoria dentro de `te interactive`. `stage` mantiene las mutaciones en memoria hasta que se invoca `save` (la opción más segura); `save` escribe en el origen después de cada comando que modifica el estado (úsese con cuidado en orígenes remotos: cada `set` desencadena una escritura XMLA); `revert` descarta las mutaciones después de cada comando, a menos que se haya pasado `--save` o `--stage`. Las marcas `--save` / `--revert` / `--stage` por comando siempre prevalecen.                                                                                                                                                                        |
| `launchInteractiveMode`      | `auto`         | Indica si al ejecutar `te` en un terminal sin argumentos se inicia el REPL interactivo. `auto` (predeterminado) inicia el REPL solo cuando los tres flujos (stdin, stdout y stderr) están asociados a un TTY, de modo que los scripts y las canalizaciones de CI pasan al análisis normal. `always` inicia el REPL independientemente de la redirección. `never` desactiva por completo el inicio automático y restaura el comportamiento tradicional de mostrar ayuda cuando no hay argumentos. La opción global `--non-interactive` fuerza `never` para una sola invocación. También puede establecerse para una sola invocación mediante la variable de entorno `TE_INTERACTIVE`. |
| `disableTelemetry`           | `false`        | Desactiva la telemetría de uso anónima. La CLI recopila datos básicos de uso de comandos (nombre del comando, código de salida y duración) para orientar la priorización de funciones. La CLI nunca recopila el contenido del modelo, PATH ni el texto de las consultas.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |

```bash
te config set bpa.rules "/etc/te/team.json,/etc/te/strict.json"
te config set bpa.onDeploy true
te config set bpa.builtInRules false
te config set bpa.disabledBuiltInRuleIds "TE3_BUILT_IN_DATE_TABLE_EXISTS,TE3_BUILT_IN_HIDE_FOREIGN_KEYS"
```

### Opciones de formato

Applied whenever the CLI formats DAX. The CLI ships a formatter that works fully offline. The layout keys (`shortFormat`, `skipSpaceAfterFunction`) apply when `autoFormat` reformats mutated expressions and when `te query` renders query text; explicit formatting via `te set <path> --format <Property>` and `te util format-dax` takes the equivalent per-invocation flags (`--long`, `--no-space-after-function`) instead. There is deliberately no list-separator key: DAX stored in a model or sent to Analysis Services is always comma-separated, so every config-driven formatting pass uses commas. The one place the semicolon dialect applies is the `--semicolons` flag on `te util format-dax`, for DAX you have typed with semicolons yourself. `formatOptions.useSqlBiDaxFormatter` routes explicit formatting and `te query`'s rendering through the SQL BI [daxformatter.com](https://www.daxformatter.com) web service (requires internet access) if you need that style; `autoFormat` always uses the built-in formatter regardless.

| Clave                                  | Predeterminado | Descripción                                                                                                                                                                                                                                                                                                                               |
| -------------------------------------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `formatOptions.shortFormat`            | `false`        | Prefiere un formato corto, de una sola línea, cuando sea posible, en lugar del diseño predeterminado de varias líneas.                                                                                                                                                                                                    |
| `formatOptions.skipSpaceAfterFunction` | `false`        | Omite el espacio entre el nombre de una función y su paréntesis de apertura (por ejemplo, `SUM(x)` en lugar de `SUM (x)`).                                                                                                                                                                             |
| `formatOptions.useSqlBiDaxFormatter`   | `false`        | Format DAX via the [SQL BI daxformatter.com](https://www.daxformatter.com) web service instead of the built-in formatter. Requiere acceso a Internet. The built-in formatter (default) works offline and matches the Tabular Editor 3 Desktop default. |

### Visualización

Ajustes que controlan la salida del terminal de la CLI y el nivel de detalle de los diagnósticos.

| Clave               | Predeterminado | Descripción                                                                                                                                   |
| ------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `hidePreviewNotice` | `false`        | Suprime el banner amarillo de vista previa. **Se ignora cuando faltan menos de 14 días para el vencimiento.** |
| `spinner`           | `true`         | Muestra indicadores de progreso animados en el terminal. Desactivar para CI.                                  |
| `debug`             | `false`        | Activa siempre el registro de depuración (equivale a pasar `--debug`).                                     |

### Perfiles

Los perfiles de conexión guardados se almacenan bajo la clave `profiles`. No los edites a mano; usa `te profile set / remove / list`. Consulta @te-cli-auth para la gestión de perfiles.

Los perfiles pueden incluir **anulaciones** que sustituyen los valores predeterminados de comportamiento anteriores siempre que el perfil esté activo. The keys a profile can override are `autoFormat`, `validateOnMutation`, `mutationOutput`, `bpa.onMutation`, `bpa.onDeploy`, `bpa.onSave`, `vertipaqOnRefresh`, `spinner`, and `interactiveEditMode`. Así, un perfil de desarrollo puede relajar la validación y el BPA, mientras que uno de producción los mantiene estrictos:

```bash
te profile set dev --validate-on-mutation false --bpa-on-deploy false
te profile set prod --auto-format true
```

`te profile set` exposes flags for the common ones (`--auto-format`, `--validate-on-mutation`, `--bpa-on-mutation`, `--bpa-on-deploy`, `--vertipaq-on-refresh`, `--spinner`); each accepts `true`, `false`, or `null` to clear the override.

## Control BPA

El control BPA es la red de seguridad que impide que se guarde o se despliegue un modelo con infracciones de reglas. Se ejecuta automáticamente con los siguientes comandos:

- `te deploy` ejecuta el control, a menos que se pase `--skip-bpa` o que `bpa.onDeploy` sea `false`.
- `te save-as` runs the gate unless `--skip-bpa` (or `--force`) is passed or `bpa.onSave` is `false`.
- `te add`, `te set`, `te move`, `te remove`, `te macro run` run the gate only when `bpa.onMutation` is `true`.

El control carga las reglas de BPA desde `bpa.rules` y, de forma predeterminada, el conjunto de reglas integrado (controlado por `bpa.builtInRules`). Las reglas integradas pueden excluirse individualmente mediante `bpa.disabledBuiltInRuleIds`; se administran con `te bpa rules disable <id>` / `te bpa rules enable <id>`.

Cuando el control se activa y detecta incumplimientos con gravedad >= `error`, el comando falla con el código de salida `1` y un resumen de los incumplimientos. Opciones para resolverlo:

- `--fix-bpa` - aplica en memoria la `fixExpression` de la regla al artefacto que se va a desplegar o guardar; los archivos fuente no se modifican.
- `--skip-bpa` - desactiva el control solo para este comando.
- `--bpa-rules <path>` - repeatable; override `bpa.rules` for this single `te deploy` or `te save-as` invocation. Las reglas integradas siguen aplicándose salvo que `bpa.builtInRules` sea `false`.

Ejecuta `te bpa run` de forma independiente para previsualizar el comportamiento del control sin desplegar:

```bash
te bpa run --model ./model --fail-on error
te bpa run --model ./model --fix --save     # Apply fixes to the source
```

### Reglas de BPA integradas

La CLI incluye un único conjunto canónico de reglas de BPA integradas, incrustado como recurso JSON. Las reglas integradas son de solo lectura: `te bpa rules set` y `te bpa rules remove` se niegan a modificar los ID integrados y remiten a los usuarios a `te bpa rules disable` en su lugar. Para personalizar el comportamiento de una regla integrada, cópiala en tu archivo local de reglas como una regla nueva con un ID distinto y deshabilita la regla integrada.

Tanto `bpa.builtInRules` como `bpa.disabledBuiltInRuleIds` se aplican de forma coherente a la validación de implementación/guardado/mutación **y** al comando manual `te bpa run`: si deshabilitas una regla una vez con `te bpa rules disable`, queda excluida en todas partes.

## Comportamiento tras la mutación

When you run a mutating command (`te add`, `te set`, `te move`, `te macro run`), the CLI performs these checks automatically:

1. **Los errores de TOM** siempre se muestran. Un DAX o M no válidos en medidas, columnas, particiones o elementos de cálculo siempre hacen que el comando falle.
2. **La validación del esquema** (`validateOnMutation`, valor predeterminado `true`) comprueba que las referencias `Table[Column]` en DAX sigan resolviéndose y verifica la consistencia de los metadatos.
3. **Formato automático de DAX** (`autoFormat`, valor predeterminado `false`) da formato a cualquier expresión afectada por la mutación mediante el DAX Formatter integrado cuando está habilitado.
4. **BPA tras la mutación** (`bpa.onMutation`, valor predeterminado `false`) ejecuta BPA después de la mutación cuando está habilitado, y muestra una advertencia o hace que el comando falle según `--fail-on`.

Deshabilita una comprobación con `te config set <key> false`, o limita esa relajación a un entorno concreto mediante un perfil.

## Administrator policies

On Windows, `te` honors the same administrator policies as Tabular Editor 3. Policies are read from the registry under `Software\Policies\Tabular Editor ApS` - with an optional `TECLI` subkey for values that should apply to the CLI only, and a `TE3` subkey for the desktop - and from the earlier `Software\Policies\Kapacity\Tabular Editor` key, which keeps working unchanged. A machine-wide value (`HKEY_LOCAL_MACHINE`) takes precedence over a per-user one (`HKEY_CURRENT_USER`), and within a hive a product-specific value takes precedence over a shared one. Where a policy turns a feature off, the command names the policy responsible, does nothing, and exits with a failure - so a pipeline that depends on something an administrator has since turned off fails visibly rather than reporting success for work it never did.

| Policy                 | Effect on the CLI                                                                                                                              |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `DisableCSharpScripts` | Refuses `te script` and the automatic fixes of `te bpa run --fix`.                                                             |
| `DisableMacros`        | Refuses every `te macro` command.                                                                                              |
| `DisableBpaDownload`   | Refuses Best Practice Analyzer rules given as a URL. Rule files on disk and the built-in rules are unaffected. |
| `DisableTelemetry`     | Turns anonymous usage statistics off, whatever `disableTelemetry` in config says.                                              |

Policies that govern features the CLI does not have - update checks, error reports, DAX Optimizer, the DAX Package Manager, the AI assistant, and the MCP server - have no effect on it. See @policies for the full list of policies and how to deploy them.

## Variables de entorno

Usa las siguientes variables de entorno específicas de la CLI para PATH, comportamiento y diagnósticos. Para las variables de autenticación de Azure (`AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_CLIENT_CERTIFICATE_PATH`, etc.), consulta @te-cli-auth.

| Variable         | Propósito                                                                                                                                                                                                                                                                                                                                                                                                                |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `TE_CONFIG`      | Ruta de acceso a un archivo de configuración alternativo. Honored by every `te config` operation (`list`, `set`, `init`, `paths`).                                                                                                                                                                                                                                    |
| `TE_MACROS_PATH` | Anula la ruta del archivo de macros (segundo en el orden de resolución; ver arriba). La leen los comandos `te macro`.                                                                                                                                                                                                                                                 |
| `TE_BPA_RULES`   | Anula la lista de archivos/URL de reglas de BPA utilizada por los subcomandos `te bpa run` y `te bpa rules`.                                                                                                                                                                                                                                                                                             |
| `TE_BPA_CONFIG`  | Anula la ruta de acceso a la configuración del gate de BPA (`.te-bpa.json`) que lee el gate de despliegue/guardado.                                                                                                                                                                                                                                                                   |
| `TE_DEBUG`       | Establece el valor en `1` para habilitar el registro de depuración globalmente (igual que `--debug` o `debug: true` en la configuración).                                                                                                                                                                                                                                             |
| `NO_SPINNER`     | Establece el valor en `1` o `true` para desactivar los indicadores de progreso animados (alternativa a `spinner: false` en la configuración).                                                                                                                                                                                                                                         |
| `CI`             | Se detecta automáticamente. Cuando vale `1` o `true`, la CLI desactiva el spinner y cambia a una salida de texto sin formato. La mayoría de los runners de CI lo configuran automáticamente.                                                                                                                                                                             |
| `TE_SESSION`     | Sobrescribe el identificador de sesión por terminal que se usa para el estado de la conexión activa. Útil para ejecutar varias sesiones aisladas de la CLI dentro del mismo shell, por ejemplo, en trabajos de matriz de CI en paralelo. Inspecciona y gestiona las sesiones con [`te session`](xref:te-cli-commands#session).                                           |
| `TE_INTERACTIVE` | Anula `launchInteractiveMode` para una sola invocación. Acepta `auto`, `always` o `never`. Útil para scripts puntuales que quieran usar el REPL interactivo (`TE_INTERACTIVE=always`) o forzar el comportamiento clásico de mostrar ayuda cuando no hay argumentos (`TE_INTERACTIVE=never`) sin tocar el archivo de configuración. |
| `TE_COMPAT`      | Establécela en `te2` para forzar el modo de compatibilidad con TE2; consulta @te-cli-migrate.                                                                                                                                                                                                                                                                                               |

## Páginas relacionadas

- @te-cli-auth - perfiles, autenticación y almacenamiento de credenciales.
- @te-cli-commands - subcomandos de `te config`.
- @te-cli-cicd - configuración del gate de BPA para pipelines.
