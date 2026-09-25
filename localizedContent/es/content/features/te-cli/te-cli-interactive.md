---
uid: te-cli-interactive
title: Modo interactivo
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

# Modo interactivo

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

El modo interactivo es un bucle guiado de lectura, evaluación e impresión (REPL) para explorar un modelo desde la terminal. Es la forma más sencilla de iniciarte si eres nuevo en la línea de comandos y un Workspace práctico para sesiones ad hoc con un único modelo.

## Iniciar una sesión

Para iniciar una sesión, ejecuta cualquiera de estos comandos:

```bash
te interactive                              # Start and connect to a model later
te interactive --model ./model              # Start with a local model
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
get Sales/Revenue -p expression
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

| Comando              | Propósito                                                                                                                                                                                             |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `help` o `?`         | Lista los comandos disponibles.                                                                                                                                                       |
| `status` o `pwd`     | Muestra el modelo o la conexión en uso.                                                                                                                                               |
| `save`               | Commit all staged in-memory edits back to the model source.                                                                                                                           |
| `revert`             | Discard all staged edits made since the last save.                                                                                                                                    |
| `clear` o `cls`      | Limpia la pantalla.                                                                                                                                                                   |
| `exit`, `quit` o `q` | Sale del modo interactivo. If staged edits are unsaved you are asked to confirm (`n` is the default); `exit --force` discards them without asking. |

`save` inside the session takes no arguments - re-serializing the model to another format or location is `save-as` (e.g. `save-as -o ./out --serialization bim`), exactly as outside the session.

## Staged edits

Inside the session, mutating commands (`set`, `add`, `remove`, `move`, `script`, `macro run`, ...) stage their changes in memory instead of writing to the source, and the prompt shows an indicator while unsaved staged edits exist. The built-in `save` command commits everything staged; `revert` discards everything staged.

Each mutating command can also decide for itself: `--save` persists that one command's change immediately, `--stage` keeps it in memory (the default), and `--revert` rolls the command's change back after showing its effect - useful for a "what would this do?" probe. The three are mutually exclusive, and `--stage`/`--revert` exist only inside the session.

The default per-command behavior is the `interactiveEditMode` config key (`stage` | `save` | `revert`) - see @te-cli-config.

Staged edits are never thrown away silently. Closing a session that still holds them - with `exit`, **Ctrl+D**, or by reaching the end of piped input - first checks for unsaved changes. If unsaved changes exist and a terminal is active, you are asked to confirm, with "no" as the default, and declining returns you to the prompt with the edits intact. Where nobody can answer (stdin piped or redirected, or `--non-interactive`), the session writes a warning naming the unsaved changes and exits with a failure code instead of a success one. Nothing is saved on the way out either way: run `save` first, or `exit --force` to discard the edits deliberately.

## Line editing and keys

The prompt offers single-line editing:

- **Left/Right** move the caret; **Home/End** (also **Ctrl+A**/**Ctrl+E**) jump to the ends; **Backspace/Delete** edit in place.
- **Up/Down** browse the command history, which persists across sessions.
- **Ctrl+C** cancels the current command without leaving the session and abandons the half-typed line for good - it is never run, Up does not bring it back, and it is not added to the history.
- **Ctrl+D** on an empty prompt exits (**Ctrl+Z** then **Enter** on Windows).

There is no tab completion inside the session - shell completion via `te completion` applies to the outer shell only.

## Indicaciones guiadas

Cuando el modo interactivo está activo, los comandos que necesitan información faltante la solicitan en lugar de fallar. Running `auth` without a subcommand opens a picker for Login / Status / Logout; running `deploy --execute` or `refresh --execute` without `--force` shows a summary and asks for confirmation (`n` is the safe default). A `deploy` or `refresh` without `--execute` is a dry run that prints the TMSL it would send, so it never prompts.

Para desactivar las indicaciones en un único comando dentro de la sesión, pasa `--non-interactive`.

## Piped and redirected input

Interactive mode also accepts piped or redirected stdin, so the same REPL can be driven from a script instead of typed by hand. Each line of input is run as a command, exactly as if you had entered it at the prompt, and the session exits when input is exhausted (or when it reaches an `exit` line). If staged edits are still unsaved at that point, the session warns and exits non-zero - end a mutating script with `save` (or `exit --force` to discard on purpose).

```bash
printf "ls\nexit\n" | te interactive --model ./model    # bash / git-bash
te interactive --model ./model < script.te              # redirected file
```

```bat
(echo ls & echo exit) | te interactive --model .\model  :: Windows cmd.exe
```

The `-` stdin convention (`set -p Expression=-`, `query -q -`, and so on) is refused inside the interactive session, because the session itself owns stdin - use it from the outer shell instead.

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
printf "bpa run --fail-on error\ndeploy --execute --force\nexit\n" | te interactive --model ./model

# Run every line regardless of failures
printf "bpa run --fail-on error\ndeploy --execute --force\nexit\n" | te interactive --model ./model --no-batch
```

### Readable transcripts

`--echo` writes each input line to stdout ahead of its output, which is handy when capturing a transcript of a piped run. Comment lines are not echoed.

```bash
printf "ls tables\nexit\n" | te interactive --model ./model --echo
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

| Valor                               | Effect                                                                                                                                     |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `auto` (default) | Launch the REPL only when all three streams are attached to a TTY. Otherwise fall through to normal parse. |
| `always`                            | Launch the REPL regardless of stream redirection. Useful when you always want an interactive session.      |
| `never`                             | Never auto-launch the REPL. `te` on its own prints help.                                                   |

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
