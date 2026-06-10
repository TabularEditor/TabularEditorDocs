---
uid: te-cli-interactive
title: Modo interactivo
author: Peer Grønnerup
updated: 2026-05-12
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

## Cuándo usar el modo interactivo frente al no interactivo

- **El modo interactivo** es ideal para explorar, aprender la CLI, hacer ediciones masivas puntuales sobre un único modelo y realizar demos.
- **El modo no interactivo** (el predeterminado fuera de `te interactive`) es el indicado para escribir scripts, automatizar o ejecutar en CI. Consulta @te-cli-automation y @te-cli-cicd.

Ambos comparten el mismo árbol de comandos: cualquier comando que ejecutes dentro de `te interactive` puedes pegarlo en un script de shell anteponiendo `te`.

## Páginas relacionadas

- @te-cli-commands - referencia completa de comandos.
- @te-cli-auth - conéctate a los Workspace y administra perfiles.
- @te-cli-automation - cuándo salir del modo interactivo.
