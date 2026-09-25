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

`te interactive` admite algunas opciones para ajustar la sesión:

- `--no-banner` - omite el banner de bienvenida al iniciar.
- `--echo` - envía a stdout cada comando ejecutado antes de mostrar su salida. Útil para registrar la actividad cuando controlas el REPL desde un script.
- `--batch` - modo por lotes no interactivo: lee los comandos de stdin línea a línea, ejecuta cada uno y termina al llegar a EOF. Se habilita automáticamente cuando stdin está redirigido.
- `--no-batch` - fuerza el modo TTY interactivo incluso cuando stdin está redirigido (mutuamente excluyente con `--batch`).

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

| Comando              | Propósito                                                                                                                                                                                                                    |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `help` o `?`         | Lista los comandos disponibles.                                                                                                                                                                              |
| `status` o `pwd`     | Muestra el modelo o la conexión en uso.                                                                                                                                                                      |
| `save`               | Confirma en el origen del modelo todas las ediciones en memoria que estén en fase.                                                                                                                           |
| `revert`             | Descarta todas las ediciones pendientes realizadas desde el último guardado.                                                                                                                                 |
| `clear` o `cls`      | Limpia la pantalla.                                                                                                                                                                                          |
| `exit`, `quit` o `q` | Sale del modo interactivo. Si hay ediciones pendientes sin guardar, se te pide confirmación (`n` es la opción predeterminada); `exit --force` las descarta sin preguntar. |

`save` dentro de la sesión no admite argumentos; para volver a serializar el modelo en otro formato o ubicación se usa `save-as` (por ejemplo, `save-as -o ./out --serialization bim`), exactamente igual que fuera de la sesión.

## Ediciones pendientes

Dentro de la sesión, los comandos que modifican el estado (`set`, `add`, `remove`, `move`, `script`, `macro run`, ...) dejan sus cambios en fase en memoria en lugar de escribirlos en el origen, y el prompt muestra un indicador mientras existan cambios en fase sin guardar. El comando integrado `save` aplica todos los cambios pendientes; `revert` descarta todos los cambios pendientes.

Cada comando que modifica el estado también puede decidir por sí mismo: `--save` guarda de inmediato el cambio de ese comando, `--stage` lo mantiene en memoria (opción predeterminada) y `--revert` revierte el cambio del comando después de mostrar su efecto; útil para comprobar «¿qué haría esto?». Las tres opciones son mutuamente excluyentes, y `--stage`/`--revert` solo existen dentro de la sesión.

El comportamiento predeterminado por comando se define en la clave de configuración `interactiveEditMode` (`stage` | `save` | `revert`) - consulta @te-cli-config.

Los cambios preparados nunca se descartan silenciosamente. Al cerrar una sesión que todavía los contiene —con `exit`, **Ctrl+D** o al llegar al final de la entrada canalizada—, primero se comprueba si hay cambios sin guardar. Si hay cambios sin guardar y hay un terminal activo, se te pide confirmación, con "no" como opción predeterminada, y, si respondes que no, vuelves al prompt con las ediciones intactas. Si nadie puede responder (stdin canalizado o redirigido, o `--non-interactive`), la sesión escribe una advertencia indicando los cambios sin guardar y sale con un código de error en lugar de uno de éxito. En ningún caso se guarda nada al salir: ejecuta primero `save`, o `exit --force` para descartar las ediciones de forma explícita.

## Edición de línea y teclas

El prompt permite editar una sola línea:

- **Izquierda/Derecha** mueven el cursor; **Inicio/Fin** (también **Ctrl+A**/**Ctrl+E**) saltan a los extremos; **Retroceso/Supr** editan en la posición actual.
- **Arriba/Abajo** recorren el historial de comandos, que se conserva entre sesiones.
- **Ctrl+C** cancela el comando actual sin salir de la sesión y descarta definitivamente la línea a medio escribir: nunca se ejecuta, **Arriba** no la recupera y no se añade al historial.
- Con **Ctrl+D** en un prompt vacío se sale (**Ctrl+Z** y después **Enter** en Windows).

No hay autocompletado con Tab dentro de la sesión: el autocompletado del shell mediante `te completion` solo se aplica al shell externo.

## Indicaciones guiadas

Cuando el modo interactivo está activo, los comandos que necesitan información faltante la solicitan en lugar de fallar. Al ejecutar `auth` sin un subcomando, se abre un selector para Iniciar sesión / Estado / Cerrar sesión; al ejecutar `deploy --execute` o `refresh --execute` sin `--force`, se muestra un resumen y se pide confirmación (`n` es la opción predeterminada más segura). Un `deploy` o `refresh` sin `--execute` es una simulación que imprime el TMSL que enviaría, así que nunca pide confirmación.

Para desactivar las indicaciones en un único comando dentro de la sesión, pasa `--non-interactive`.

## Entrada canalizada y redirigida

El modo interactivo también acepta stdin canalizado o redirigido, de modo que el mismo REPL puede controlarse desde un script en lugar de escribirse a mano. Cada línea de entrada se ejecuta como un comando, exactamente igual que si la hubieras escrito en el prompt, y la sesión termina cuando se agota la entrada (o cuando llega a una línea `exit`). Si en ese momento los cambios preparados siguen sin guardarse, la sesión emite una advertencia y sale con un código distinto de cero; termina cualquier script que haga cambios con `save` (o usa `exit --force` para descartarlos a propósito).

```bash
printf "ls\nexit\n" | te interactive --model ./model    # bash / git-bash
te interactive --model ./model < script.te              # redirected file
```

```bat
(echo ls & echo exit) | te interactive --model .\model  :: Windows cmd.exe
```

La convención de stdin con `-` (`set -p Expression=-`, `query -q -`, etc.) no se admite dentro de la sesión interactiva, porque la propia sesión ya usa stdin: úsala desde el shell externo.

Las líneas que empiezan por `#` se tratan como comentarios y se omiten, así que puedes anotar un archivo de script:

```
# script.te - inspect the model, then exit
ls tables
ls measures
exit
```

### Modo por lotes y códigos de salida

Cuando stdin está canalizado, `--batch` es la opción **predeterminada**: la sesión se detiene en el primer comando que falla y sale con un código distinto de cero, lo que hace que una ejecución canalizada sea segura para usarla como paso de compilación o de CI. Usa `--no-batch` para seguir ejecutando las líneas restantes incluso si falla un comando. El código de salida del proceso es `0` si la ejecución finaliza correctamente y distinto de cero cuando un comando falla en modo por lotes.

```bash
# Default when piped: stop at the first failing command, exit non-zero
printf "bpa run --fail-on error\ndeploy --execute --force\nexit\n" | te interactive --model ./model

# Run every line regardless of failures
printf "bpa run --fail-on error\ndeploy --execute --force\nexit\n" | te interactive --model ./model --no-batch
```

### Transcripciones legibles

`--echo` escribe cada línea de entrada en stdout antes de su salida correspondiente, lo que resulta útil al capturar una transcripción de una ejecución canalizada. Las líneas de comentario no se imprimen.

```bash
printf "ls tables\nexit\n" | te interactive --model ./model --echo
```

### Opciones

| Opción        | Descripción                                                                                                                                                                       |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--no-banner` | Suprime el banner de bienvenida.                                                                                                                                  |
| `--echo`      | Muestra cada línea de entrada en stdout (útil para transcripciones de ejecuciones canalizadas).                                                |
| `--batch`     | Finaliza con un código de salida distinto de cero en el primer comando que falle (comportamiento predeterminado cuando stdin está canalizado). |
| `--no-batch`  | Continúa tras los errores incluso cuando stdin está canalizado.                                                                                                   |

### Banner de bienvenida vs. aviso de vista previa

Al inicio de una sesión pueden aparecer dos mensajes distintos. No los confundas:

- El **banner de bienvenida** es la pantalla inicial interactiva descrita en [Iniciar una sesión](#starting-a-session). Se suprime con `--no-banner`. Cuando stdin se canaliza, el banner de bienvenida ni siquiera aparece, así que `--no-banner` solo tiene un efecto visible en una sesión interactiva real (TTY).
- El **aviso de caducidad de la vista previa** (`This is an early preview release ...`) es un mensaje distinto. Siempre se escribe en **stderr** y **no** se ve afectado por `--no-banner`. Suprímelo con `te config set hidePreviewNotice true`.

## Inicio automático al invocar sin argumentos

Ejecutar `te` en una terminal sin argumentos te lleva directamente a la REPL interactiva, así que explorar un modelo es tan rápido como abrir una shell y escribir `te`. Cuando stdin, stdout o stderr se redirigen (salida canalizada, pipelines de CI, scripts), la CLI continúa con su análisis normal y muestra la ayuda; así, los scripts de shell que invocan `te` sin un subcomando siguen comportándose igual.

El comportamiento se controla con la clave de configuración `launchInteractiveMode`, que admite tres valores:

| Valor                                      | Efecto                                                                                                                                             |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `auto` (predeterminado) | Inicia el REPL solo cuando los tres flujos estén adjuntos a un TTY. De lo contrario, pasa al análisis normal.      |
| `siempre`                                  | Inicia el REPL independientemente de la redirección de flujos. Útil cuando siempre quieres una sesión interactiva. |
| `nunca`                                    | No inicies nunca el REPL de forma automática. `te` por sí solo muestra la ayuda.                                   |

Cámbialo globalmente con:

```bash
te config set launchInteractiveMode never    # keep the classic help-on-empty behavior
te config set launchInteractiveMode auto     # restore the default
```

Anúlalo para una sola invocación mediante la variable de entorno `TE_INTERACTIVE` (los mismos valores) o pasando `--non-interactive` en la línea de comandos; ambas opciones fuerzan `never` en esa ejecución, por lo que `te --non-interactive` muestra la ayuda en lugar de iniciar el REPL.

## Cuándo usar el modo interactivo frente al no interactivo

- **El modo interactivo** es ideal para explorar, aprender la CLI, hacer ediciones masivas puntuales sobre un único modelo y realizar demos.
- **El modo no interactivo** (el predeterminado fuera de `te interactive`) es el indicado para escribir scripts, automatizar o ejecutar en CI. Consulta @te-cli-automation y @te-cli-cicd.

Ambos comparten el mismo árbol de comandos: cualquier comando que ejecutes dentro de `te interactive` puedes pegarlo en un script de shell anteponiendo `te`.

## Páginas relacionadas

- @te-cli-commands - referencia completa de comandos.
- @te-cli-auth - conéctate a los Workspace y administra perfiles.
- @te-cli-automation - cuándo salir del modo interactivo.
