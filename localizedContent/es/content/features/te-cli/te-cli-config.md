---
uid: te-cli-config
title: Configuración personalizada
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

# Configuración personalizada

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

La CLI de Tabular Editor lee una configuración opcional desde un archivo JSON. La configuración controla tres cosas:

- **File paths** - where the CLI reads macros, BPA rules, and (optionally) the TE3 Desktop executable, and where to write the query log.
- **Behavioral defaults** - BPA gates, auto-format, validation.
- **Saved connection profiles** - the list of named profiles you can switch between.

La CLI es independiente: no lee ni escribe en ningún PATH de instalación de la versión de escritorio de Tabular Editor 3. Los archivos de reglas de BPA y de macros deben definirse explícitamente en esta configuración (o inicializarse cuando haga falta con `te bpa rules init` / `te macro init`).

Most users don't need to edit the config file directly - `te config list`, `te config set <key> <value>`, and `te profile set` cover the common operations.

## Ubicación del archivo de configuración

Se comprueban las siguientes ubicaciones en este orden:

1. La variable de entorno `$TE_CONFIG` (si está definida y el archivo existe).
2. `~/.config/te/config.json` (en Windows, `%USERPROFILE%\.config\te\config.json`).
3. Si no hay archivo de configuración, la CLI usa los valores predeterminados integrados.

`TE_CONFIG` is honored consistently by every config-file operation - `te config list`, `te config set`, `te config init`, and `te config paths` all read and write at the resolved path. Está pensado principalmente para pruebas, instalaciones mediante scripts y configuración por entorno.

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
> `te config paths` emite campos `null` explícitamente en el modo `--output-format json` (por ejemplo, `{"macros": null, "bpa": {"rules": null}}`). Informar de los resultados de la resolución es precisamente el propósito del comando, así que `null` es una respuesta significativa: «se intentó, pero no se resolvió nada». `te config list --output-format json` strips null fields by default, so consumers should parse it tolerantly.

## Configurar valores

```bash
te config set autoFormat true
te config set bpa.onDeploy false
te config set hidePreviewNotice true
te config set macros null              # Clear a path override
```

Las claves desconocidas provocan que el comando finalice con el código de salida `1` y un error que enumera las claves válidas.

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
    "useSemicolons": false,
    "shortFormat": false,
    "skipSpaceAfterFunction": false,
    "useSqlBiDaxFormatter": false
  },

  "hidePreviewNotice": false,
  "spinner": true,
  "debug": false,
  "disableTelemetry": false,

  "queryLog": null,
  "te3ExePath": null,

  "profiles": {}
}
```

### Rutas de archivo

Configúralas en tu configuración para evitar pasar las mismas rutas en cada comando. Las opciones específicas de cada comando y las variables de entorno prevalecen sobre los valores de configuración; consulta [Prioridad de resolución de rutas](#path-resolution-priority) más abajo.

| Clave        | Significado                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `macros`     | Ruta explícita a un archivo JSON de macros (normalmente `MacroActions.json`). La resuelve cualquier comando `te macro`. Apunta a un archivo compartido (un recurso compartido de red, un archivo local del repositorio o incluso el archivo de escritorio de TE3) para reutilizar el mismo conjunto de macros en distintos equipos y entre la CLI y TE3 Desktop. |
| `bpa.rules`  | Lista ordenada de rutas o URL a archivos de reglas de BPA. `te bpa run` y la compuerta de implementación/guardado cargan **todas** las entradas existentes; `te bpa rules list` y `te config paths` usan la primera entrada existente. Los valores separados por comas en `te config set bpa.rules ...` se separan en el arreglo.                                                                      |
| `te3ExePath` | Ruta explícita al ejecutable de Tabular Editor 3 Desktop (`TabularEditor.exe`). `te open` lo usa **solo** para iniciar la aplicación de escritorio; puedes dejarlo sin configurar en Linux/macOS o cuando no uses `te open`. Si no está configurado, `te open` recurre a una búsqueda en `PATH`.                                                                                    |
| `queryLog`   | Ruta a un archivo de registro en el que cada invocación de `te query` añade el texto de la consulta y los metadatos de ejecución. Útil para mantener registros de auditoría o analizar patrones de consulta a lo largo del tiempo. Admite `~` para el directorio personal (p. ej., `~/.config/te/queries.log`).                                     |

### Prioridad de resolución de rutas

Para cada archivo proporcionado por el usuario (macros, reglas de BPA), la CLI resuelve la ruta en este orden:

1. **Opción de línea de comandos** - `--macros <path>` para comandos de macros; `--bpa-rules <path>` para la compuerta de implementación/guardado; `--rules-file <path>` para los subcomandos de `te bpa rules`.
2. **Variable de entorno** - `TE_MACROS_PATH` para macros, `TE_BPA_RULES` para reglas de BPA.
3. **Configuración de la CLI** - `macros` para macros, la primera entrada existente de `bpa.rules[]` para reglas de BPA.

La CLI no detecta automáticamente ninguna ubicación de instalación de TE3; configúralas explícitamente. Para empezar con un archivo predeterminado en el directorio de trabajo actual, ejecuta `te macro init` (crea `./MacroActions.json`) o `te bpa rules init` (crea `./BPARules.json`).

Ejecuta `te config paths` para ver qué archivo resolvió realmente la CLI.

### Valores predeterminados de comportamiento

Toda la configuración relacionada con BPA está en el objeto `bpa` y se referencia mediante claves con puntos en `te config set`.

| Clave                        | Predeterminado | Descripción                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ---------------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `autoFormat`                 | `false`        | Run the DAX Formatter on modified expressions after `te add` / `te set` / `te move` / `te macro run`. Usa el formateador interno de forma predeterminada; puedes optar por el servicio web de SQL BI mediante `formatOptions.useSqlBiDaxFormatter`.                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `validateOnMutation`         | `true`         | Después de un comando de modificación (`add`, `set`, `mv`, `replace --save`, `macro run`), comprueba que todas las referencias `Table[Column]` del modelo se sigan resolviendo. Detecta referencias huérfanas introducidas por cambios de nombre o eliminaciones antes de llegar al despliegue.                                                                                                                                                                                                                                                                                                                                                                 |
| `bpa.onMutation`             | `false`        | Ejecuta un análisis de BPA acotado después de cada comando de modificación (`set`, `add`, `mv`, `rm`, `macro run`). Solo se comprueban los objetos de la tabla afectada, no los de todo el modelo; útil para obtener retroalimentación rápida durante ediciones iterativas.                                                                                                                                                                                                                                                                                                                                                                                     |
| `bpa.onDeploy`               | `true`         | Ejecuta el control de BPA antes de que se ejecute `te deploy`. The deploy is aborted if any rule fires at severity >= error. Omítelo en una invocación concreta con `--skip-bpa`, o corrígelo automáticamente con `--fix-bpa`.                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `bpa.onSave`                 | `true`         | Ejecuta el control de BPA antes de que `te save -o` escriba en disco. Omítelo en una invocación concreta con `--skip-bpa` o `--force`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `bpa.builtInRules`           | `true`         | Incluye el conjunto depurado de reglas integradas de BPA cada vez que se ejecute el control. Configúralo en `false` para ignorar por completo las reglas integradas; entonces el control ejecutará solo las reglas configuradas mediante `bpa.rules` y cualquier regla incrustada en el modelo.                                                                                                                                                                                                                                                                                                                                                                                    |
| `bpa.disabledBuiltInRuleIds` | `null`         | ID de reglas integradas individuales que se excluirán de la puerta de calidad. Este valor se modifica mediante `te bpa rules disable <id>` / `te bpa rules enable <id>`; es preferible usar esos comandos en lugar de editar el arreglo directamente.                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `vertipaqOnRefresh`          | `false`        | Tras una actualización correcta (`full`, `dataonly`, `automatic` o `add`), ejecuta automáticamente el análisis de VertiPaq para mostrar estadísticas de almacenamiento de las tablas actualizadas. Útil para detectar de inmediato regresiones inesperadas de cardinalidad o memoria.                                                                                                                                                                                                                                                                                                                                                                           |
| `interactiveEditMode`        | `stage`        | Comportamiento predeterminado para las mutaciones en memoria dentro de `te interactive`. `stage` mantiene las mutaciones en memoria hasta que se invoca `save` (la opción más segura); `save` escribe en el origen después de cada comando que modifica el estado (úsese con cuidado en orígenes remotos: cada `set` desencadena una escritura XMLA); `revert` descarta las mutaciones después de cada comando, a menos que se haya pasado `--save` o `--stage`. Las marcas `--save` / `--revert` / `--stage` por comando siempre prevalecen.                                                                |
| `launchInteractiveMode`      | `auto`         | Whether running `te` in a terminal with no arguments launches the interactive REPL. `auto` (default) launches the REPL only when all three streams (stdin, stdout, stderr) are attached to a TTY, so scripts and CI pipelines fall through to normal parse. `always` launches the REPL regardless of redirection. `never` disables the auto-launch entirely, restoring the traditional help-on-empty behavior. The global `--non-interactive` flag forces `never` for a single invocation. Can also be set for one invocation via the `TE_INTERACTIVE` environment variable. |
| `disableTelemetry`           | `false`        | Desactiva la telemetría de uso anónima. La CLI recopila datos básicos de uso de comandos (nombre del comando, código de salida y duración) para orientar la priorización de funciones. La CLI nunca recopila el contenido del modelo, PATH ni el texto de las consultas.                                                                                                                                                                                                                                                                                                                                                                        |

```bash
te config set bpa.rules "/etc/te/team.json,/etc/te/strict.json"
te config set bpa.onDeploy true
te config set bpa.builtInRules false
te config set bpa.disabledBuiltInRuleIds "TE3_BUILT_IN_DATE_TABLE_EXISTS,TE3_BUILT_IN_HIDE_FOREIGN_KEYS"
```

### Opciones de formato

Se aplica siempre que la CLI invoque un formateador de DAX (para `te format` y, cuando está habilitado, para `autoFormat` en las mutaciones). La CLI incluye un formateador propio que funciona completamente sin conexión; activa el servicio web de SQL BI [daxformatter.com](https://www.daxformatter.com) mediante `formatOptions.useSqlBiDaxFormatter` si necesitas ese estilo o quieres igualar el comportamiento de TE2 o TE3 con "Use daxformatter.com..." activado.

| Clave                                  | Predeterminado | Descripción                                                                                                                                                                                                                                                                                                                                                                         |
| -------------------------------------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `formatOptions.useSemicolons`          | `false`        | Usa `;` como separador de listas (según la configuración regional europea/de la UE). El valor predeterminado `,` coincide con la configuración regional en-US.                                                                                                                                                                   |
| `formatOptions.shortFormat`            | `false`        | Prefiere un formato corto, de una sola línea, cuando sea posible, en lugar del diseño predeterminado de varias líneas.                                                                                                                                                                                                                                              |
| `formatOptions.skipSpaceAfterFunction` | `false`        | Omite el espacio entre el nombre de una función y su paréntesis de apertura (por ejemplo, `SUM(x)` en lugar de `SUM (x)`).                                                                                                                                                                                                                       |
| `formatOptions.useSqlBiDaxFormatter`   | `false`        | Formatea DAX con el servicio web [SQL BI daxformatter.com](https://www.daxformatter.com) en lugar del formateador interno. Requiere acceso a Internet. El formateador interno (predeterminado) funciona sin conexión y coincide con la configuración predeterminada de Tabular Editor 3 Desktop. |

### Visualización

Ajustes que controlan la salida del terminal de la CLI y el nivel de detalle de los diagnósticos.

| Clave               | Predeterminado | Descripción                                                                                                                                   |
| ------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `hidePreviewNotice` | `false`        | Suprime el banner amarillo de vista previa. **Se ignora cuando faltan menos de 14 días para el vencimiento.** |
| `spinner`           | `true`         | Muestra indicadores de progreso animados en el terminal. Desactivar para CI.                                  |
| `debug`             | `false`        | Activa siempre el registro de depuración (equivale a pasar `--debug`).                                     |

### Perfiles

Los perfiles de conexión guardados se almacenan bajo la clave `profiles`. No los edites a mano; usa `te profile set / remove / list`. Consulta @te-cli-auth para la gestión de perfiles.

Los perfiles pueden incluir **anulaciones** que sustituyen los valores predeterminados de comportamiento anteriores siempre que el perfil esté activo. Así, un perfil de desarrollo puede relajar la validación y el BPA, mientras que uno de producción los mantiene estrictos:

```bash
te profile set dev --validate-on-mutation false --bpa-on-deploy false
te profile set prod --auto-format true
```

## Control BPA

El control BPA es la red de seguridad que impide que se guarde o se despliegue un modelo con infracciones de reglas. Se ejecuta automáticamente con los siguientes comandos:

- `te deploy` ejecuta el control, a menos que se pase `--skip-bpa` o que `bpa.onDeploy` sea `false`.
- `te save` ejecuta el control, a menos que se pase `--skip-bpa` (o `--force`) o que `bpa.onSave` sea `false`.
- `te add`, `te set`, `te move`, `te macro run` run the gate only when `bpa.onMutation` is `true`.

El control carga las reglas de BPA desde `bpa.rules` y, de forma predeterminada, el conjunto de reglas integrado (controlado por `bpa.builtInRules`). Las reglas integradas pueden excluirse individualmente mediante `bpa.disabledBuiltInRuleIds`; se administran con `te bpa rules disable <id>` / `te bpa rules enable <id>`.

When the gate fires and finds violations at severity >= `error`, the command fails with exit code `1` and a summary of the violations. Opciones para resolverlo:

- `--fix-bpa` - aplica en memoria la `fixExpression` de la regla al artefacto que se va a desplegar o guardar; los archivos fuente no se modifican.
- `--skip-bpa` - desactiva el control solo para este comando.
- `--bpa-rules <path>` - repetible; sobrescribe `bpa.rules` para esta única invocación de `te deploy` o `te save`. Las reglas integradas siguen aplicándose salvo que `bpa.builtInRules` sea `false`.

Ejecuta `te bpa run` de forma independiente para previsualizar el comportamiento del control sin desplegar:

```bash
te bpa run ./model --fail-on error
te bpa run ./model --fix --save     # Apply fixes to the source
```

### Reglas de BPA integradas

La CLI incluye un único conjunto canónico de reglas de BPA integradas, incrustado como recurso JSON. Built-in rules are read-only - `te bpa rules set` and `te bpa rules remove` refuse to mutate built-in IDs and point users at `te bpa rules disable` instead. Para personalizar el comportamiento de una regla integrada, cópiala en tu archivo local de reglas como una regla nueva con un ID distinto y deshabilita la regla integrada.

Tanto `bpa.builtInRules` como `bpa.disabledBuiltInRuleIds` se aplican de forma coherente a la validación de implementación/guardado/mutación **y** al comando manual `te bpa run`: si deshabilitas una regla una vez con `te bpa rules disable`, queda excluida en todas partes.

## Comportamiento tras la mutación

When you run a mutating command (`te add`, `te set`, `te move`, `te replace --save`, `te macro run`), the CLI performs these checks automatically:

1. **Los errores de TOM** siempre se muestran. Un DAX o M no válidos en medidas, columnas, particiones o elementos de cálculo siempre hacen que el comando falle.
2. **La validación del esquema** (`validateOnMutation`, valor predeterminado `true`) comprueba que las referencias `Table[Column]` en DAX sigan resolviéndose y verifica la consistencia de los metadatos.
3. **Formato automático de DAX** (`autoFormat`, valor predeterminado `false`) da formato a cualquier expresión afectada por la mutación mediante el DAX Formatter integrado cuando está habilitado.
4. **BPA tras la mutación** (`bpa.onMutation`, valor predeterminado `false`) ejecuta BPA después de la mutación cuando está habilitado, y muestra una advertencia o hace que el comando falle según `--fail-on`.

Deshabilita una comprobación con `te config set <key> false`, o limita esa relajación a un entorno concreto mediante un perfil.

## Variables de entorno

Usa las siguientes variables de entorno específicas de la CLI para PATH, comportamiento y diagnósticos. Para las variables de autenticación de Azure (`AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_CLIENT_CERTIFICATE_PATH`, etc.), consulta @te-cli-auth.

| Variable         | Propósito                                                                                                                                                                                                                                                                                                                                                                               |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TE_CONFIG`      | Ruta de acceso a un archivo de configuración alternativo. Se respeta en todas las operaciones de `te config` (`show`, `set`, `init`, `paths`).                                                                                                                                                                                       |
| `TE_MACROS_PATH` | Anula la ruta del archivo de macros (segundo en el orden de resolución; ver arriba). La leen los comandos `te macro`.                                                                                                                                                                                                                |
| `TE_BPA_RULES`   | Anula la lista de archivos/URL de reglas de BPA utilizada por los subcomandos `te bpa run` y `te bpa rules`.                                                                                                                                                                                                                                                            |
| `TE_BPA_CONFIG`  | Anula la ruta de acceso a la configuración del gate de BPA (`.te-bpa.json`) que lee el gate de despliegue/guardado.                                                                                                                                                                                                                                  |
| `TE3_EXE_PATH`   | Ruta al binario de escritorio de Tabular Editor 3. Se usa **solo** con `te open`; puedes dejarla sin definir en Linux/macOS o si no usas `te open`. Si no se especifica, se usa la búsqueda en `PATH`.                                                                                                                                  |
| `TE_DEBUG`       | Establece el valor en `1` para habilitar el registro de depuración globalmente (igual que `--debug` o `debug: true` en la configuración).                                                                                                                                                                                                            |
| `NO_SPINNER`     | Establece el valor en `1` o `true` para desactivar los indicadores de progreso animados (alternativa a `spinner: false` en la configuración).                                                                                                                                                                                                        |
| `CI`             | Se detecta automáticamente. Cuando vale `1` o `true`, la CLI desactiva el spinner y cambia a una salida de texto sin formato. La mayoría de los runners de CI lo configuran automáticamente.                                                                                                                                            |
| `TE_SESSION`     | Sobrescribe el identificador de sesión por terminal que se usa para el estado de la conexión activa. Útil para ejecutar varias sesiones aisladas de la CLI dentro del mismo shell, por ejemplo, en trabajos de matriz de CI en paralelo. Inspecciona y gestiona las sesiones con [`te session`](xref:te-cli-commands#session).          |
| `TE_INTERACTIVE` | Override `launchInteractiveMode` for a single invocation. Accepts `auto`, `always`, or `never`. Handy for one-off scripts that want the interactive REPL (`TE_INTERACTIVE=always`) or want to force the classic help-on-empty behavior (`TE_INTERACTIVE=never`) without touching the config file. |
| `TE_COMPAT`      | Establécela en `te2` para forzar el modo de compatibilidad con TE2; consulta @te-cli-migrate.                                                                                                                                                                                                                                                              |

## Páginas relacionadas

- @te-cli-auth - perfiles, autenticación y almacenamiento de credenciales.
- @te-cli-commands - subcomandos de `te config`.
- @te-cli-cicd - configuración del gate de BPA para pipelines.
