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

`te interactive` acepta algunas opciones para ajustar la sesión:

- `--no-banner` - omite el banner de bienvenida al iniciar.
- `--echo` - escribe en stdout cada comando ejecutado antes de su salida. Útil para llevar un registro cuando se controla la REPL desde un script.
- `--batch` - modo por lotes no interactivo: lee comandos de stdin línea por línea, ejecuta cada uno y sale al llegar a EOF. Se habilita automáticamente cuando stdin está redirigido.
- `--no-batch` - fuerza el modo TTY interactivo incluso cuando stdin está redirigido (mutuamente excluyente con `--batch`).

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

## Entrada canalizada y redirigida

El modo interactivo también acepta stdin canalizado o redirigido, de modo que puedes controlar la misma REPL desde un script en lugar de introducir los comandos a mano. Cada línea de entrada se ejecuta como un comando, exactamente igual que si la hubieras introducido en el prompt, y la sesión termina cuando se agota la entrada (o cuando llega a una línea `exit`).

```bash
printf "ls\nexit\n" | te interactive ./model        # bash / git-bash
te interactive ./model < script.te                  # redirected file
```

```bat
(echo ls & echo exit) | te interactive .\model      :: Windows cmd.exe
```

Las líneas que empiezan por `#` se tratan como comentarios y se omiten, así que puedes anotar un archivo de script:

```
# script.te - inspect the model, then exit
ls tables
ls measures
exit
```

### Modo por lotes y códigos de salida

Cuando stdin está canalizado, `--batch` es el valor **predeterminado**: la sesión se detiene en el primer comando que falla y sale con un código distinto de cero, lo que hace que una ejecución canalizada sea segura para usarla como paso de compilación o de CI. Usa `--no-batch` para seguir ejecutando las líneas restantes incluso después de que falle un comando. El código de salida del proceso es `0` si la ejecución finaliza correctamente y distinto de cero cuando falla un comando en modo por lotes.

```bash
# Default when piped: stop at the first failing command, exit non-zero
printf "bpa run --fail-on error\ndeploy --force\nexit\n" | te interactive ./model

# Run every line regardless of failures
printf "bpa run --fail-on error\ndeploy --force\nexit\n" | te interactive ./model --no-batch
```

### Transcripciones legibles

`--echo` escribe cada línea de entrada en stdout antes de su salida, lo que resulta práctico al capturar una transcripción de una ejecución canalizada. Las líneas de comentario no se muestran.

```bash
printf "ls tables\nexit\n" | te interactive ./model --echo
```

### Opciones

| Opción        | Descripción                                                                                                                                          |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--no-banner` | Suprime el banner de bienvenida.                                                                                                     |
| `--echo`      | Escribe cada línea de entrada en stdout (útil para transcripciones de ejecuciones canalizadas).                   |
| `--batch`     | Sale con un código distinto de cero en el primer comando que falla (predeterminado cuando stdin está canalizado). |
| `--no-batch`  | Continúa tras los errores incluso cuando stdin se canaliza por una tubería.                                                          |

### Banner de bienvenida frente al aviso de versión preliminar

Pueden aparecer dos mensajes distintos al iniciar una sesión; no los confundas:

- El **banner de bienvenida** es la pantalla inicial interactiva descrita en [Iniciar una sesión](#starting-a-session). Se suprime con `--no-banner`. Cuando stdin se canaliza por una tubería, el banner de bienvenida ni siquiera se muestra, así que `--no-banner` solo tiene un efecto visible en una sesión interactiva (TTY) real.
- El **aviso de caducidad de la versión preliminar** (`This is an early preview release ...`) es otro de los **mensajes**. Siempre se escribe en **stderr** y **no** se ve afectado por `--no-banner`. Suprímelo con `te config set hidePreviewNotice true`.

## Inicio automático al invocar sin argumentos

Ejecutar `te` en una terminal sin argumentos te lleva directamente al REPL interactivo, así que explorar un modelo es tan rápido como abrir una terminal y escribir `te`. Cuando stdin, stdout o stderr se redirigen (salida por tubería, pipelines de CI, scripts), la CLI continúa con el análisis habitual y muestra la ayuda en su lugar, así que los scripts de shell que invocan `te` sin un subcomando siguen comportándose de la misma manera.

Este comportamiento se controla con la clave de configuración `launchInteractiveMode`, que admite tres valores:

| Valor                                      | Efecto                                                                                                                                                                           |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `auto` (predeterminado) | Inicia el REPL solo cuando los tres flujos están adjuntos a un TTY. De lo contrario, pasa al análisis normal.                                    |
| `always`                                   | Inicia el REPL aunque haya redirección de flujos. Útil si siempre quieres una sesión interactiva.                                                |
| `never`                                    | No inicia nunca el REPL automáticamente. `te` por sí solo muestra la ayuda, igual que antes de la versión 0.6.0. |

Cámbialo globalmente con:

```bash
te config set launchInteractiveMode never    # keep the classic help-on-empty behavior
te config set launchInteractiveMode auto     # restore the default
```

Puedes anularlo para una única ejecución mediante la variable de entorno `TE_INTERACTIVE` (con los mismos valores) o pasar `--non-interactive` en la línea de comandos; ambas opciones fuerzan `never` en esa ejecución, por lo que `te --non-interactive` muestra la ayuda en lugar de iniciar el REPL.

## Cuándo usar el modo interactivo frente al no interactivo

- **El modo interactivo** es ideal para explorar, aprender la CLI, hacer ediciones masivas puntuales sobre un único modelo y realizar demos.
- **El modo no interactivo** (el predeterminado fuera de `te interactive`) es el indicado para escribir scripts, automatizar o ejecutar en CI. Consulta @te-cli-automation y @te-cli-cicd.

Ambos comparten el mismo árbol de comandos: cualquier comando que ejecutes dentro de `te interactive` puedes pegarlo en un script de shell anteponiendo `te`.

## Páginas relacionadas

- @te-cli-commands - referencia completa de comandos.
- @te-cli-auth - conéctate a los Workspace y administra perfiles.
- @te-cli-automation - cuándo salir del modo interactivo.
