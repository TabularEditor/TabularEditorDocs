---
uid: te-cli-interactive
title: Modo interactivo
author: Peer Grønnerup
updated: 2026-06-26
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      none: true
    - product: Tabular Editor CLI
      full: true
---

# Modo interactivo

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

El modo interactivo es un bucle guiado de lectura, evaluación e impresión (REPL) para explorar un modelo desde la terminal. Es la forma más sencilla de iniciarte si eres nuevo en la línea de comandos y un Workspace práctico para sesiones ad hoc con un único modelo.

## Iniciar una sesión

Para iniciar una sesión, ejecuta cualquiera de estos comandos:

```bash
te interactive                              # Start and connect to a model later
te interactive ./model                      # Start with a local model
te interactive -s MyWorkspace -d MyModel    # Start with a remote model
```

`te interactive` accepts a few flags for tuning the session:

- `--no-banner` - skip the welcome banner on startup.
- `--echo` - echo each executed command to stdout before its output. Useful for logging when driving the REPL from a script.
- `--batch` - non-interactive batch mode: read commands from stdin line by line, execute each, and exit on EOF. Automatically enabled when stdin is redirected.
- `--no-batch` - force interactive TTY mode even when stdin is redirected (mutually exclusive with `--batch`).

La sesión imprime un banner de bienvenida, muestra el modelo activo y te sitúa en un prompt con contexto del modelo:

![Sesión del modo interactivo de Tabular Editor CLI](~/content/assets/images/features/cli/cli-interactive-mode.png)

Si no hay ningún modelo establecido, el prompt es simplemente `te>`; usa `connect` para abrir el selector de conexiones, `connect <path>` o `connect <Workspace> <model>` para conectarte a uno.

## Comandos dentro de la sesión

Una vez iniciado un REPL, todos los subcomandos de `te` están disponibles **sin el prefijo `te`**:

```
ls tables
get "Sales/Revenue" -q expression
query -q "EVALUATE TOPN(5, 'Sales')"
bpa run --fail-on error
```

Cada comando acepta `--help` igual que fuera de la sesión:

```
deploy --help
```

## Comillas y rutas de estilo DAX

El separador de línea del REPL reconoce las mismas formas de comillas que las [rutas de objeto](xref:te-cli-commands#object-paths), de modo que las referencias con forma de DAX se interpretan como un único argumento:

- `'...'` y `"..."`: segmentos entre comillas simples y dobles. Se eliminan los caracteres de comilla y las comillas duplicadas permiten incluir una comilla literal.
- `[...]`: segmento entre corchetes. **Los corchetes se conservan** en el argumento resultante, de modo que una ruta como `'Internet Sales'[Sales Amount]` llega al comando como un único token que el analizador de rutas puede volver a interpretar como una referencia DAX. Los corchetes de cierre duplicados (`]]`) se mantienen literalmente por la misma razón.

```
get 'Internet Sales'[Sales Amount]   # One argument, DAX form
get [Total Sales]                    # Lone-bracket model-wide lookup
ls 'Net Sales'/'Sales Amount'        # Quoted segments with a slash separator
```

Los grupos sin cerrar abarcan hasta el final de la línea, por lo que una comilla o un corchete de apertura sueltos provocan un error explícito en lugar de dividir la entrada sin avisar.

## Comandos integrados del REPL

Estos comandos los gestiona el propio REPL, no el árbol de comandos habitual:

| Comando              | Propósito                                               |
| -------------------- | ------------------------------------------------------- |
| `help` o `?`         | Lista los comandos disponibles.         |
| `status` o `pwd`     | Muestra el modelo o la conexión en uso. |
| `clear` o `cls`      | Limpia la pantalla.                     |
| `exit`, `quit` o `q` | Sale del modo interactivo.              |

## Indicaciones guiadas

Cuando el modo interactivo está activo, los comandos que necesitan información faltante la solicitan en lugar de fallar. Ejecutar `auth` sin un subcomando abre un menú para Iniciar sesión / Estado / Cerrar sesión; ejecutar `deploy` sin `--force` muestra un resumen y pide confirmación (`n` es la opción predeterminada más segura).

Para desactivar las indicaciones en un único comando dentro de la sesión, pasa `--non-interactive`.

## Piped and redirected input

Interactive mode also accepts piped or redirected stdin, so the same REPL can be driven from a script instead of typed by hand. Each line of input is run as a command, exactly as if you had entered it at the prompt, and the session exits when input is exhausted (or when it reaches an `exit` line).

```bash
printf "ls\nexit\n" | te interactive ./model        # bash / git-bash
te interactive ./model < script.te                  # redirected file
```

```bat
(echo ls & echo exit) | te interactive .\model      :: Windows cmd.exe
```

Lines that start with `#` are treated as comments and skipped, so you can annotate a script file:

```
# script.te - inspect the model, then exit
ls tables
ls measures
exit
```

### Batch mode and exit codes

When stdin is piped, `--batch` is the **default**: the session stops at the first command that fails and exits with a non-zero code, which makes a piped run safe to use as a build or CI step. Pass `--no-batch` to keep running the remaining lines even after a command fails. The process exit code is `0` for a clean run and non-zero when a command fails under batch mode.

```bash
# Default when piped: stop at the first failing command, exit non-zero
printf "bpa run --fail-on error\ndeploy --force\nexit\n" | te interactive ./model

# Run every line regardless of failures
printf "bpa run --fail-on error\ndeploy --force\nexit\n" | te interactive ./model --no-batch
```

### Readable transcripts

`--echo` writes each input line to stdout ahead of its output, which is handy when capturing a transcript of a piped run. Comment lines are not echoed.

```bash
printf "ls tables\nexit\n" | te interactive ./model --echo
```

### Opciones

| Opción        | Descripción                                                                                                  |
| ------------- | ------------------------------------------------------------------------------------------------------------ |
| `--no-banner` | Suppress the welcome banner.                                                                 |
| `--echo`      | Echo each input line to stdout (useful for piped transcripts).            |
| `--batch`     | Exit non-zero on the first failing command (default when stdin is piped). |
| `--no-batch`  | Continue after errors even when stdin is piped.                                              |

### Welcome banner vs. preview notice

Two separate messages can appear at the start of a session - don't conflate them:

- The **welcome banner** is the interactive splash described under [Starting a session](#starting-a-session). It is suppressed with `--no-banner`. When stdin is piped, no welcome banner is emitted in the first place, so `--no-banner` has a visible effect only in a true interactive (TTY) session.
- The **preview-expiry notice** (`This is an early preview release ...`) is a different message. It is always written to **stderr** and is **not** affected by `--no-banner`. Suppress it with `te config set hidePreviewNotice true`.

## Auto-launch on empty invocation

Running `te` in a terminal with no arguments drops you straight into the interactive REPL, so exploring a model is as fast as opening a shell and typing `te`. When stdin, stdout, or stderr is redirected (piped output, CI pipelines, scripts), the CLI falls through to its normal parse and prints help instead - so shell scripts that invoke `te` without a subcommand keep behaving the same way.

The behavior is controlled by the `launchInteractiveMode` config key with three values:

| Valor                               | Effect                                                                                                                                                    |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `auto` (default) | Launch the REPL only when all three streams are attached to a TTY. Otherwise fall through to normal parse.                |
| `always`                            | Launch the REPL regardless of stream redirection. Useful when you always want an interactive session.                     |
| `never`                             | Never auto-launch the REPL. `te` on its own prints help, matching the pre-0.6.0 behavior. |

Change it globally with:

```bash
te config set launchInteractiveMode never    # keep the classic help-on-empty behavior
te config set launchInteractiveMode auto     # restore the default
```

Override for a single invocation via the `TE_INTERACTIVE` environment variable (same values), or pass `--non-interactive` on the command line - both force `never` for that call, so `te --non-interactive` prints help instead of launching the REPL.

## Cuándo usar el modo interactivo frente al no interactivo

- **El modo interactivo** es ideal para explorar, aprender la CLI, hacer ediciones masivas puntuales sobre un único modelo y realizar demos.
- **El modo no interactivo** (el predeterminado fuera de `te interactive`) es el indicado para escribir scripts, automatizar o ejecutar en CI. Consulta @te-cli-automation y @te-cli-cicd.

Ambos comparten el mismo árbol de comandos: cualquier comando que ejecutes dentro de `te interactive` puedes pegarlo en un script de shell anteponiendo `te`.

## Páginas relacionadas

- @te-cli-commands - referencia completa de comandos.
- @te-cli-auth - conéctate a los Workspace y administra perfiles.
- @te-cli-automation - cuándo salir del modo interactivo.
