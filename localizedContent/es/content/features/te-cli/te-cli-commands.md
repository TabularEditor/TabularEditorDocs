---
uid: te-cli-commands
title: Referencia de comandos
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

# Referencia de comandos

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

Esta página ofrece una breve descripción y un ejemplo por comando. Todos los comandos aceptan `--help` para consultar la documentación completa de las opciones:

```bash
te deploy --help            # Help for a single command
te bpa run --help           # Help for a command with subcommands
```

> [!NOTE]
> Durante la versión preliminar, la salida de `--help` de la CLI es la referencia definitiva de parámetros y opciones. El contenido de esta página se ha seleccionado manualmente y puede quedarse atrás respecto a `--help` cuando se añadan novedades entre versiones preliminares.

## Rutas de objeto

El direccionamiento de objetos en la CLI usa una única gramática compartida por todos los comandos. En la referencia siguiente aparecen dos tipos de ruta:

- **`<path>`**: identifica **exactamente un** objeto o contenedor. Lo usan los comandos que cambian el modelo o necesitan un único destino: `te set`, `te add`, `te remove`, `te move`, `te deps`, `te macro run --on` y `te get` con `-p`, `--deps` o `--properties`.
- **`<path-filter>`**: identifica **cero o más** objetos y admite comodines. Lo usan los comandos que operan sobre un conjunto: `te list`, `te get` a secas (una ruta con comodines o de contenedor enumera todas las coincidencias), `te bpa run --path` y otros comandos de tipo inspección.

Ambas formas de ruta comparten las mismas reglas de sintaxis; solo se diferencian en dos puntos:

- Las rutas de filtro permiten comodines `*`; las rutas de objeto no.
- Las rutas de objeto permiten el sufijo entre corchetes de DAX (por ejemplo, `Sales[Amount]`); las rutas de filtro no.

### Segmentos y separadores

Una ruta es una secuencia de **segmentos** separados por barras. Cada segmento nombra un único paso: una tabla, un objeto hijo o una palabra clave de contenedor.

- `Sales` — un segmento
- `Sales/Revenue` — dos segmentos
- `Roles/Admin/Members/bob` — cuatro segmentos

La entrada vacía y `.` significan «la raíz del modelo»: el punto de partida implícito para las rutas de filtro y el sujeto explícito de las consultas del tipo `te get .`.

### Uso de comillas

La mayoría de los nombres de segmentos funcionan tal cual. Pon un segmento entre comillas cuando su nombre contenga espacios, barras, corchetes o cualquier carácter que, de otro modo, se interpretaría como sintaxis. La CLI sigue las convenciones de comillas de DAX, por lo que el uso de comillas en las rutas de `te` coincide con lo que escribirías dentro de una expresión DAX:

| Forma            | Uso                                                                                                                                                                                                                                                     | Regla de escape                                                                                    |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `'Net Sales'`    | Tablas y objetos con nombre con espacios.                                                                                                                                                                                               | Duplica la comilla simple (`'Bob''s'` → `Bob's`).               |
| `"Net Sales"`    | Igual que arriba; conveniente entre distintos shells cuando es engorroso escapar comillas simples.                                                                                                                                      | Duplica la comilla doble (`"He said ""hi"""` → `He said "hi"`). |
| `[Sales Amount]` | Un sufijo entre corchetes al estilo DAX en una tabla (`'Sales'[Sales Amount]`) o una referencia global al modelo solo entre corchetes (`[Total Sales]`). Solo en rutas de objeto. | Duplica el corchete de cierre (`[foo]]bar]` → `foo]bar`).       |

Dentro de los segmentos entre comillas, `*` se trata como un carácter literal, no como un comodín. Por tanto, `'Sa*'` coincide con una tabla cuyo nombre es exactamente `Sa*`.

Los caracteres reservados en las rutas son `/ [ ] ' " * ? { }`. Un segmento que contenga cualquiera de `* ? { }` debe ir entre comillas (`te get "Tables/'{foo}'"`, `te get 'Sales/"my*name"'`); si se usa sin comillas, se rechaza con un error que indica el carácter y muestra la forma entrecomillada. `?` es un carácter reservado y no tiene significado de comodín. Toda ruta que la CLI imprima —en errores, sugerencias, la salida de `--paths-only` y el campo `objectPath` del JSON— se cita de forma canónica y se puede pegar tal cual en `te get`. Las formas con comillas mixtas requieren PowerShell o bash; cmd.exe no puede expresarlas.

### Referencias al estilo DAX (solo rutas de objeto)

Se aceptan dos formas con sintaxis DAX en cualquier lugar donde se admita un `<path>`:

- **`'Table'[Member]`** — equivalente a `Table/Member`. El sufijo entre corchetes hace que las coincidencias ambiguas se resuelvan a favor de columnas y medidas frente a jerarquías/particiones.
- **`[Member]`** — una medida o columna _independiente_, sin tabla delante. Busca en todo el modelo una medida o columna con ese nombre. Las medidas tienen prioridad cuando existen tanto la medida como la columna.

```bash
te get "'Sales'[Amount]"             # Same as te get Sales/Amount
te get "'Net Sales'[Sales Amount]"   # Spaced names via DAX form
te get "[Total Sales]"               # Model-wide measure-or-column lookup
```

### Contenedores y palabras clave

Varios nombres funcionan como palabras clave de contenedor. Una palabra clave puede usarse sola (para enumerar todo el contenedor) o aparecer dentro de una ruta (para entrar en esa subcolección del elemento padre actual).

| Palabra clave                                                                                                                    | Ámbito    | Significado                                                      |
| -------------------------------------------------------------------------------------------------------------------------------- | --------- | ---------------------------------------------------------------- |
| `Tables`, `Medidas`, `Columns`, `Hierarchies`, `Particiones`, `KPIs`, `Sets`                                                     | Modelo    | Todos los objetos de ese tipo en todo el modelo. |
| `Relaciones`, `Roles`, `Perspectives`, `Cultures`, `DataSources`, `Expressions`, `CalculationGroups`, `Functions`, `Annotations` | Modelo    | Contenedores a nivel de modelo.                  |
| `Medidas`, `Columns`, `Hierarchies`, `Particiones`, `Calendars`, `CalculationItems`, `KPIs`, `Sets`                              | Tabla     | Subcontenedores dentro de una tabla.             |
| `Levels`                                                                                                                         | Jerarquía | Niveles de una jerarquía.                        |
| `Members`, `TablePermissions` (alias `Permissions`)                                                           | Rol       | Elementos hijos de un rol.                       |

Los conjuntos calculados solo se pueden referenciar en forma de contenedor (`<table>/Sets/<name>`); un KPI individual es `<table>/<measure>/KPI`; los calendarios se resuelven en `<table>/Calendars/<name>`; las relaciones se resuelven en `Relationships/<name>` (el propio nombre de la relación en el modelo: un GUID o una etiqueta como `Relationship 1`; `--paths-only` lo imprime y también se acepta el nombre para mostrar).

Algunos ejemplos muestran en qué se diferencian las rutas simples y las rutas con ámbito de contenedor:

```bash
te get Sales/Revenue                       # Measure or column on Sales
te get Sales/Measures/Revenue              # Same, container-scoped - disambiguates if other kinds share the name
te get Sales/Geography/Levels/Year         # Specific level of a hierarchy
te get Roles/Admin/Members/bob@example.com # Role member
te get Sales/refreshPolicy                 # Refresh-policy sub-object on a table
te get Sales/Revenue/KPI                   # KPI sub-object of a measure
```

Pon un segmento entre comillas para forzar la coincidencia literal del nombre cuando el nombre real de un objeto coincide con una palabra clave. La tabla cuyo nombre literal es `Tables` es `'Tables'` y se accede con `te get "'Tables'"`. Lo mismo se aplica a las tablas llamadas `KPIs` o `Sets`.

### Comodines en rutas de filtro

Las rutas de filtro añaden un único carácter comodín - `*` - que coincide con cualquier secuencia de caracteres dentro de un solo segmento (codicioso, de un solo segmento). Los comodines son la forma en que `te list` y comandos similares acotan los resultados.

```bash
te list 'Sa*'                          # Tables whose name starts with Sa
te list 'Sales/*Amount'                # Children of Sales whose name ends with Amount
te list '*/Amount'                     # An Amount column/measure across every table
te list 'Roles/Re*/Members'            # Members of every role matching Re*
```

Una ruta de filtro con **N segmentos** produce resultados con **N niveles de profundidad**; los comodines nunca amplían automáticamente un nivel más allá de lo que hayas escrito. El atajo de un solo segmento `te list Sales` es la excepción: un nombre de tabla sin calificar y sin comodines se expande a los elementos secundarios directos de la tabla para reflejar la intención de "muéstrame qué hay en Sales". En cambio, `te list Sa*` devuelve solo las tablas coincidentes, sin expansión.

El sufijo entre corchetes de DAX se rechaza en las rutas de filtro; pon entre comillas los nombres que contengan `[` y `]` si necesitas que coincidan literalmente.

### Errores y sugerencias

Los segmentos mal escritos generan un error contextual con una sugerencia de "quizás quisiste decir" cuando la CLI puede deducir lo que querías decir. La lista ofrece tablas, medidas, columnas y jerarquías, cada una como una ruta completa `Table/Object` que puedes pegar directamente en el siguiente comando. Un nombre escrito entre comillas simples es una referencia a una tabla (`te deps 'Revenue'` busca una tabla llamada Revenue), y el error te indica las formas `Table/Object` y `"[Object]"` para todo lo que no sea una tabla. Las rutas a las que les falta el elemento padre fallan antes de la comprobación del elemento hoja, así que los mensajes señalan el segmento que realmente está mal. Toda ruta que aparezca en un error o sugerencia se toma de tu modelo y se entrecomilla para que se resuelva tal como se muestra; si algo se rechaza, nunca se sugiere una ruta que no exista. Los contenedores vacíos (por ejemplo, `te list Hierarchies` en un modelo sin jerarquías) muestran un simple mensaje de "no hay nada aquí" en lugar de un error.

## Alias de comandos

La mayoría de los verbos en formato largo también aceptan un alias corto. Cada fila muestra el comando canónico y el comando equivalente en formato corto que admite como alias.

| Canónico              | Forma(s) con alias |
| --------------------- | ------------------------------------- |
| `te save-as`          | `te save`                             |
| `te list`             | `te ls`                               |
| `te remove`           | `te rm`                               |
| `te move`             | `te mv`, `te rename`                  |
| `te bpa rules list`   | `te bpa rules ls`                     |
| `te bpa rules remove` | `te bpa rules rm`                     |
| `te config list`      | `te config ls`                        |
| `te macro list`       | `te macro ls`                         |
| `te macro remove`     | `te macro rm`                         |
| `te profile list`     | `te profile ls`                       |
| `te profile remove`   | `te profile rm`                       |
| `te session list`     | `te session ls`                       |
| `te test list`        | `te test ls`                          |

## Opciones globales

Estas opciones están disponibles en todos los comandos y se pueden usar antes o después del nombre del subcomando.

| Opción                     | Descripción                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `-m, --model <path>`       | Ruta al modelo semántico (carpeta TMDL, archivo `.bim`, carpeta `Database.json` o carpeta `.SemanticModel`).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `-s, --server <endpoint>`  | Punto de conexión de Analysis Services o un Workspace de Power BI. Un nombre de servidor/FQDN (`MY.SERVER.COM`), una dirección IP (`192.168.1.1`), `host:port`, `localhost`, `SERVER\INSTANCE`, `asazure://...` o una cadena de conexión de MSOLAP se conecta directamente a Analysis Services/AAS. Un nombre sencillo de un solo token (`MyWorkspace`), una ruta de Fabric `Name.Workspace[/Model.SemanticModel]` o una URL `powerbi://...` apunta a un Workspace de Power BI. Un nombre de Workspace que contiene un punto no se puede distinguir de un nombre de servidor, por lo que se trata como un servidor y la CLI muestra una advertencia; usa su forma `.Workspace` o la URL completa `powerbi://` para dirigirte a Power BI. |
| `-d, --database <name>`    | Nombre del modelo semántico en el Workspace.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `--local`                  | Conéctate a una instancia de Analysis Services en ejecución en tu equipo: Power BI Desktop, Workspaces de Visual Studio o SSAS independiente (solo Windows).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `--auth <method>`          | Método de autenticación: `auto`, `interactive`, `spn`, `env`, `managed-identity` (predeterminado: `auto`).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `--output-format <format>` | Formato de Stdout: `text` (predeterminado), `json`, `csv`, `tmsl` (alias `bim`), `tmdl`. `csv` se respeta en los comandos que emiten datos tabulares; `tmsl`/`tmdl` solo se respetan en `te get` y `te list` para la serialización de objetos completos. Los comandos rechazan los formatos que no admiten.                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `--error-format <format>`  | Formato de stderr para errores, advertencias y sugerencias: `text` (predeterminado) o `json`. Para cualquier otro valor, se usa `text`. Es independiente de `--output-format`, así que puedes combinar stdout en JSON con errores en texto sin formato (o viceversa).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `--recent [N]`             | Usa un modelo que hayas usado recientemente. Sin valor = selector interactivo; `N` = el N-ésimo más reciente (1 = el último usado).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `--non-interactive`        | Desactiva todas las indicaciones interactivas. Finaliza con un error accionable si falta algún dato obligatorio.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `--debug`                  | Habilita el registro de depuración en stderr (cadenas de conexión, flujo de autenticación, tiempos).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |

`te --version` muestra la versión de la CLI y sale.

En los comandos que leen un modelo, el orden de resolución es:

`--recent` → `--local` → `--server`/`--database` (remoto) → `--model` → conexión activa de `te connect`.

El modelo nunca es un argumento posicional: una ruta suelta en la línea de comandos se rechaza con un error de "unrecognized command or argument". (Los argumentos posicionales de `te connect`, `te init`, `te diff` y `te query` corresponden a esos comandos, no al modelo.)

> [!NOTE]
> **Las opciones mal escritas se rechazan de entrada.** Si pasas un `--flag` que no se reconoce en el comando que invocaste, la CLI finaliza con un error claro en lugar de interpretarlo silenciosamente como un argumento posicional. Esto detecta errores tipográficos como, por ejemplo, que `--force ` se convierta accidentalmente en `--forec` en scripts de CI.

> [!NOTE]
> **Nombres de servidor con puntos.** `-s`/`--server` trata un nombre con puntos (por ejemplo, `Sales.2026`) como el nombre de host de un servidor de Analysis Services, no como un Workspace de Power BI. Se muestra una advertencia cuando la CLI tiene que hacer esta interpretación, con una sugerencia para agregar `.Workspace` (por ejemplo, `Sales.2026.Workspace`) o usar una URL `powerbi://` completa si en realidad te referías al Workspace de Power BI. Se aplica a `te connect`, `te deploy`, `te refresh`, `te query`, `te vertipaq` y `te test run`.

## Inicialización y guardado del modelo

### save-as

Re-serializa un modelo en un formato o una ubicación diferentes. Úsalo para escribir en archivos locales un modelo de un Workspace remoto, convertir formatos o guardar de nuevo las ediciones en el origen. (Alias: `save`.)

`te save-as` acepta:

- `-o, --output-path <path>` - archivo o carpeta de destino. **Opcional** - si se omite, `te save-as` vuelve a escribir en la ubicación de origen y conserva el formato original.
- `--serialization <fmt>` - `tmdl`, `bim` (alias `tmsl`), `Database.json`, `pbip`. Si se omite, el formato es el del modelo cargado; con `-o`, se infiere a partir de la ruta de salida (`.bim` escribe un BIM de un solo archivo y `.json`, una carpeta `Database.json`).
- `--force` - omite la validación y sobrescribe la salida existente. Algunos rechazos (contenedores ambiguos, raíces de proyecto con varios `SemanticModel`) siguen ocurriendo incluso con `--force`.
- `--skip-bpa` - omite por completo el control de BPA.
- `--fix-bpa` - corrige automáticamente las infracciones de BPA cuando las reglas definen una expresión de corrección.
- `--bpa-rules <path>` - repetible; reemplaza `bpa.rules` de la configuración de la CLI solo en este guardado. Las reglas integradas siguen aplicándose a menos que `bpa.builtInRules` sea `false`.
- `--skip-validation` - omite el análisis semántico y la validación de DAX para descargas rápidas en modo passthrough.
- `--supporting-files` - genera archivos auxiliares de Fabric (`.platform`, `definition.pbism`).

```bash
te save-as                                    # Save back to source (no -o needed)
te save-as -m ./model.bim -o ./tmdl-out       # Convert BIM to TMDL
te save-as -o ./project --serialization pbip         # Save as a PBIP project
te save-as -o ./out -s my-workspace -d my-model --skip-validation   # Fast download
```

La salida de `--serialization pbip` se abre directamente en Power BI Desktop y toma el nombre del modelo de origen (`SpaceParts.pbip`, no `Model.pbip`). Guardar en una carpeta que ya contiene un proyecto agrega solo los archivos que faltan y deja intacto todo lo que ya está allí —las páginas del Report, el tema, la conexión y la identidad del elemento— exactamente como estaba, de modo que un guardado que no cambia nada deja el proyecto sin cambios en el control de código fuente.

La validación impide el guardado: un modelo con una colisión de nombres que Analysis Services rechazaría (`TE0012` / `TE0013`, ver [validate](#validate)) no se escribe a menos que se pase `--force` o `--skip-validation`.

> [!TIP]
> Use `te save-as -o <path> -s <Workspace> -d <model>` para descargar un modelo remoto en disco. Combínalo con `--skip-validation` para obtener el passthrough más rápido cuando solo necesites los bytes (sin análisis semántico de DAX).

### init

Crea un nuevo modelo semántico vacío en la ruta especificada. De forma predeterminada, usa un modelo TMDL en modo de compatibilidad `PowerBI` con nivel de compatibilidad 1705.

`te init` acepta:

- `<output-path>` - argumento posicional: directorio donde se creará el modelo (omítelo para usar la ruta global `--model`).
- `--compatibility-mode <mode>` - `PowerBI` (predeterminado) o `AnalysisServices`.
- `--compatibility-level <N>` (alias `--compat`) - nivel de compatibilidad. El valor predeterminado es `1705` cuando el modo es `PowerBI`; en caso contrario, `1500`. Consulta @update-compatibility-level.
- `--name <name>` - nombre del modelo o de la base de datos (predeterminado: el nombre del directorio).
- `--serialization <fmt>` - `tmdl` (predeterminado), `bim` (alias `tmsl`), `Database.json`, `pbip`.
- `--force` - reemplaza cualquier archivo o directorio existente en la ruta de destino.

```bash
te init ./new-model                                       # TMDL, PowerBI mode, compat 1705
te init ./new-model --serialization bim                   # Single-file BIM model
te init ./as-model --compatibility-mode AnalysisServices  # AS model, compat 1500
te init ./existing-dir --force                            # Overwrite non-empty directory
```

`te init` es idempotente: volver a ejecutarlo sobre un modelo que ya creó muestra `Already exists` y termina con `0` (con `--output-format json`: `{"created": false, "reason": "already_exists", ...}`). Los conflictos reales siguen devolviendo `1`; `--force` lo vuelve a crear desde cero.

## Edición del modelo

Los comandos que modifican (`set`, `add`, `remove`, `move` y también `script`, `macro run`, `bpa run --fix`) son **ejecuciones de prueba de forma predeterminada**: sin `--save`, el comando informa de lo que cambiaría y lo descarta (`Dry run - nothing saved. Agrega --save para conservar los cambios.`). Agrega `--save` para guardar en la ubicación de origen, o `--save-to <path>` para escribir en otra ubicación. En `set`, `add`, `remove`, `move`, `script` y `bpa run`, la salida de cambios se muestra como un diff unificado por cada objeto modificado; cámbiala con `--stat` o `--name-only` (mutuamente excluyentes con `--diff`, la opción predeterminada), o establece un valor predeterminado permanente con `te config set mutationOutput diff|stat|name-only|none`. La salida JSON siempre incluye el array completo de cambios. Se rechaza el guardado cuando la modificación introduce nuevos errores de validación de DAX, salvo que se use `--force`.

### set

Establece propiedades en un objeto del modelo, da formato a sus expresiones o sincroniza una tabla con su esquema de origen. Acepta un argumento `<path>`.

`te set` acepta:

- `-p, --property <Name=Value>` - asignación de propiedades (p. ej., `-p expression="SUM(Sales[Amt])"`, `-p isHidden=true`). **Repetible** - todo lo que va después del primer `=` es el valor. Las asignaciones posicionales sin prefijo también funcionan: `te set Sales/Amount formatString="#,0" --save`. Los nombres de las propiedades no distinguen entre mayúsculas y minúsculas, aceptan ambas grafías cuando la etiqueta de la cuadrícula y el nombre de TOM difieren (`Hidden` e `IsHidden`), y aceptan rutas con puntos e indexadores: `-p KPI.StatusGraphic=...`, `-p "Annotations[Tabular Editor]=..."`, `-p "TranslatedNames[fr-FR]=..."`. Ejecuta `te get <path> --properties` para enumerar todos los nombres que acepta un objeto; consulta [get](#get). La expresión de una partición es `-p Expression`, sea cual sea el tipo de partición (`MExpression` y `Query` siguen funcionando). Usa `-p Name=-` para leer el valor desde la entrada estándar, stdin (una asignación por flujo; un valor canalizado se toma literalmente, así que canalizar el texto `null` almacena la palabra `null`). `-p Name=` asigna una cadena vacía.
- `--unset <Name>`: limpia el valor de una propiedad; se puede repetir (`--unset description --unset displayFolder`). `-p Name=null` es la forma abreviada. Funciona con cualquier propiedad que pueda quedar sin valor —incluidas las propiedades de texto— y también con las que tienen valores de objeto (`SortByColumn`, `RefreshPolicy`); `-p "Annotations[key]=null"` elimina una anotación. Las propiedades numéricas, booleanas y de opción fija no se pueden limpiar y se rechazan.
- `--format <PropertyName>`: da formato a esa propiedad de expresión (se puede repetir; DAX o M se detecta a partir de la propiedad). Las opciones `--long` (menos saltos de línea) y `--no-space-after-function` son ajustes del formateador y requieren usar `--format` con una propiedad DAX. `--semicolons` no se admite junto con `--format`: una expresión almacenada en un modelo siempre va separada por comas, así que la variante con punto y coma nunca podrá analizarla; en su lugar, da formato al DAX escrito con punto y coma con [`te util format-dax --semicolons`](#util-format-dax).
- `--update-schema`: sincroniza las columnas de una tabla con su esquema de origen: añade nuevas columnas del origen con los tipos detectados, corrige el tipo de las que hayan cambiado y conserva todo lo demás de cada columna existente (nombre, descripción, cadena de formato, carpeta de visualización, columna de ordenación, visibilidad, anotaciones, traducciones, pertenencia a perspectivas). Las columnas de origen eliminadas solo generan una advertencia, salvo que uses `--drop-removed-columns` (destructivo). Una columna de origen renombrada parece una eliminación + una adición; remapéala primero con `-p SourceColumn=<newName>`. No se admite en tablas calculadas ni grupos de cálculo; no se puede combinar con `-p` ni con `--format`. Si no se especifica ninguna opción de conexión, la conexión se toma del propio modelo: el Data source al que están vinculadas las particiones de la tabla, la conexión escrita en la consulta de la propia tabla o el único Data source utilizable del modelo; y la tabla de origen se toma de la vinculación de la partición, recurriendo al nombre de la tabla del modelo si hace falta. `--data-source <name>` te permite elegir cuando el modelo tiene varios Data source utilizables. Si nombras una conexión explícitamente con las opciones de detección de esquema compartidas con `te add` (`--source sql|lakehouse|warehouse`, `--endpoint`, `--connection-string`, `--source-database`, `--source-table`), eso siempre prevalece. Cuando no se puede determinar ningún origen, o no se puede encontrar la tabla de origen, el error indica cuál de los dos casos se aplica y qué tabla buscó.
- `-t, --type <kind>` - desambiguación cuando la misma ruta podría referirse a varios tipos de objeto (`medida`, `Column`, `CalculatedColumn`, `Hierarchy`, `Calendar`, `partición`, `CalculationItem`).
- `--save` / `--save-to <path>` - guarda los cambios.
- `--diff` / `--stat` / `--name-only`: cambian cómo se representa la salida de cambios (consulta la nota anterior).
- `--serialization <fmt>` - sobrescribe la serialización al guardar (`tmdl`, `bim` (alias `tmsl`), `database.json`).
- `--force` - guarda incluso si la modificación introduce errores de validación de DAX.

```bash
te set Sales/Amount -p expression="SUM(Sales[Amt])" --save
te set "'Net Sales'[Sales Amount]" -p formatString="#,0" --save        # DAX form with spaced names
te set Sales -p isHidden=true --save
te set Sales/Amount -p formatString="#,0" -p description="Net sales" --save   # Multiple properties, one atomic change
te set "Sales/Total Sales" --unset description --save                   # Clear a property (same as -p description=null)
te set Sales/Amount --format Expression --save                          # Format one expression property
te set Sales --update-schema --save                                     # Sync columns with the source schema (connection inferred from the model)
te set Sales --update-schema --data-source "Sales DW" --save            # Pick the data source when the model has several
```

#### Políticas de actualización incremental

Las políticas de actualización son propiedades normales del subobjeto `RefreshPolicy` de una tabla, así que `te get` y `te set` las gestionan como cualquier otra propiedad. Nombres de propiedad: `Mode`, `RollingWindowPeriods`/`RollingWindowGranularity`, `IncrementalPeriods`/`IncrementalGranularity`, `IncrementalPeriodsOffset`, `SourceExpression`, `PollingExpression` (entrada desde archivo: `-p SourceExpression=- < src.m`).

```bash
te get Sales/RefreshPolicy                                              # Inspect a table's refresh policy
te set Sales/RefreshPolicy -p RollingWindowPeriods=5 -p RollingWindowGranularity=Day -p IncrementalPeriods=1 -p IncrementalGranularity=Day --save
te set Sales -p RefreshPolicy=null --save                               # Remove the policy
```

La política se crea implícitamente en el primer `set`. Eliminar una política deja las particiones generadas por la política en su sitio y no se permite cuando son las únicas particiones de la tabla. Para aplicar una política en el servidor, consulta [`te refresh --apply-refresh-policy`](#refresh); para aplicarla solo a nivel de metadatos, usa `te script --inline "Model.Tables[\"Sales\"].ApplyRefreshPolicy();" --save`.

### add

Agrega un objeto al modelo. Especifica un `<path>` para el nuevo objeto (el elemento padre ya debe existir; el segmento final es el nuevo nombre) y el tipo mediante `-t` / `--type`. Las relaciones mantienen su sintaxis abreviada (`Sales[Key]->Dim[Key]`). Las rutas en formato de contenedor son objetivos válidos para `add` (`Sales/Measures/Margin`, `Sales/Partitions/Q1`, `Sales/Calendars/Fiscal`, `Roles/Admin/TablePermissions/Sales`, `Roles/Admin/Members/user@x.com`) - cualquier ruta que muestre la CLI puede volver a pasarse a `te add`.

`te add` acepta:

- `-t, --type <type>`: tipo de objeto. Valores habituales: `Table`, `CalculatedTable`, `CalcGroup`, `medida`, `CalculatedColumn`, `DataColumn`, `Hierarchy`, `Level`, `Calendar`, `CalcItem`, `KPI`, `partición`, `Expression`, `Function`, `perspectiva`, `Culture`, `rol`, `TablePermission`, `Member`. Se admite el autocompletado con la tecla Tab; la lista completa se puede obtener ejecutando `te add --help`.
- `-p, --property <Name=Value>` - asignación de propiedades al nuevo objeto (repetible). La expresión va en `-p Expression="..."`, o usa `--file`, o `-p Expression=-` para leerla desde stdin.
- `--file <path>` - lee la expresión de un archivo en lugar de incluirla en línea.
- `--mode <mode>` - modo de almacenamiento para tablas nuevas: `import` (predeterminado), `directquery` (alias `dq`), `dual`, `directlake` (alias `dl`).
- `--if-not-exists` - sale con código `0` sin error si el objeto ya existe. Úsalo en canalizaciones de CI/CD idempotentes.
- `--save` / `--save-to <path>` - guarda los cambios.
- `--diff` / `--stat` / `--name-only` - formato de la salida de cambios (consulta la nota sobre [edición del modelo](#model-editing)).
- `--serialization <fmt>` - sobrescribe la serialización al guardar (`tmdl`, `bim` (alias `tmsl`), `database.json`, `pbip`).
- `--source-type <kind>` - tipo de origen inicial de la partición en una tabla nueva: `m`, `query` o `calculated`. Anula la detección heurística. `query` crea una partición heredada de SQL `SELECT`, vinculada al origen de datos del proveedor del modelo, y se rechaza con orígenes Lakehouse/Warehouse o cuando no existe ningún origen de proveedor; `calculated` solo es válido con `-t CalculatedTable`.
- `--partition-expression <m>` - expresión M sin procesar para la partición inicial de la tabla nueva.
- `--force` - guarda incluso si la modificación introduce errores de validación de DAX.

Para agregar una sola columna de datos a una tabla existente se usa `-t DataColumn`, con `SourceColumn` y `DataType` obligatorios (se rechaza en tablas calculadas y grupos de cálculo):

```bash
te add Sales/Quantity -t DataColumn -p SourceColumn=Qty -p DataType=Int64 --save
```

Las tablas pueden crearse de una sola vez a partir del **propio** Data source del modelo; no hacen falta opciones de conexión. La CLI toma la conexión del Data source del modelo, detecta las columnas de la tabla de origen y sus tipos, y crea la tabla con una partición ya vinculada a ese Data source. Con un Data source heredado (basado en proveedor), la partición es una consulta SQL heredada que contiene el `SELECT` generado, igual que el que genera el asistente de escritorio **Importar tablas**; pasa `--source-type m` para usar en su lugar una partición de Power Query (M). Con un Data source estructurado (Power Query), la partición siempre es M. Los rechazos son claros y no se crea nada: varios Data sources utilizables y sin `--data-source`; ningún Data source que la CLI pueda leer (se admiten orígenes de SQL Server, Azure SQL y Fabric SQL); un Data source cuya contraseña el modelo no almacena; o una tabla de origen que la conexión no puede encontrar. El error indica la tabla que buscó y de dónde salió ese nombre.

- `--source-table <schema.table>` - crea la tabla a partir de esta tabla de origen.
- `--query "SELECT ..."` - crea la tabla a partir de una consulta: la consulta se analiza sobre la conexión sin ejecutarse, la tabla nueva recibe exactamente las columnas que devuelve y la consulta se conserva como contenido de la partición. Funciona tanto con una conexión inferida como con una indicada explícitamente. `--source-type query` coloca el SQL en una partición Query heredada vinculada al Data source heredado del modelo. Se rechaza si se usa junto con `--mode directlake` (una partición Direct Lake no contiene ninguna consulta), con `--columns` y con una expresión propia (`-p Expression=` o `--file`).
- `--data-source "<name>"` - elimina la ambigüedad cuando el modelo tiene varios Data sources.

La detección de esquema sobre un origen explícito también funciona, y siempre prevalece sobre la inferencia: `--source sql|lakehouse|warehouse`, `--endpoint`, `--connection-string`, `--source-database`, `--source-table`, o una especificación manual de columnas `--columns "Id:Int64,Name:String"`. `te add "<table>" -t Table` sin ningún origen sigue creando una tabla vacía para que la completes tú mismo.

```bash
te add Sales/Revenue -t Measure -p Expression="SUM(Sales[Amount])" --save
te add Sales/Quantity -t DataColumn -p SourceColumn=Qty -p DataType=Int64 --save
te add "Sales[ProdKey]->Product[ProdKey]" --save                        # Relationship shorthand
te add Sales/MarketingFlag -t CalculatedColumn -p Expression="Sales[Amount] > 1000" --if-not-exists --save
te add Perspectives/Default/Sales --save                                # Include Sales in the Default perspective
te add Roles/Reader -t Role --save                                      # New role at the model level
te add Inventory -t Table --source-table dbo.Inventory --save           # Table from the model's own data source
te add TopCustomers -t Table --query "SELECT TOP 100 * FROM dbo.Customers" --save
```

### remove

Elimina un objeto. De forma predeterminada, comprueba las dependencias para evitar romper referencias existentes. (Alias: `rm`.)

`te remove` acepta:

- `<path>` - argumento posicional: el objeto que se va a eliminar.
- `-t, --type <kind>` - desambigua cuando la ruta coincide con varios elementos secundarios de una tabla (p. ej., una columna y una jerarquía con el mismo nombre).
- `--force` - omite la comprobación de objetos dependientes.
- `--if-exists` - sale con código `0` sin error si el objeto no existe. Úsalo en canalizaciones de CI/CD idempotentes.
- `--dry-run` - muestra una vista previa de la eliminación sin aplicarla.
- `--save` / `--save-to <path>` - guarda el cambio.
- `--diff` / `--stat` / `--name-only` - formato de la salida de cambios (consulta la nota sobre [edición del modelo](#model-editing)).
- `--serialization <fmt>` - sobrescribe la serialización al guardar (`tmdl`, `bim` (alias `tmsl`), `database.json`).

```bash
te remove Sales/Revenue --save
te remove "'Sales'[Revenue]" --save              # DAX form
te remove Sales/Revenue --dry-run                # Preview only
te remove Sales/OldMeasure --if-exists --save    # Idempotent
```

### move

Mueve o renombra un objeto del modelo. Tanto el origen como el destino son argumentos `<path>`. (Alias: `mv` y `rename`.)

`te move` acepta:

- `-t, --type <kind>` - desambigua cuando la ruta de origen coincide con varios tipos de objeto (p. ej., una columna y una jerarquía con el mismo nombre).
- `--save` / `--save-to <path>` - guarda el cambio.
- `--diff` / `--stat` / `--name-only` - formato de la salida de cambios (consulta la nota sobre [edición del modelo](#model-editing)).
- `--serialization <fmt>` - sobrescribe la serialización al guardar (`tmdl`, `bim` (alias `tmsl`), `database.json`).
- `--force` - guarda incluso si la mutación introduce errores de validación de DAX.

Se rechaza cambiar el nombre de un objeto cuyo nombre no tienes permiso para establecer, devolviendo un código de salida distinto de cero en lugar de informar `No changes.`: una relación (su nombre siempre describe las columnas que une), el KPI de una medida o el permiso de tabla de un rol.

```bash
te move Sales/Revenue Finance/Revenue --save                # Move measure to another table
te move Sales/Revenue Sales/TotalRevenue --save             # Rename measure
te move Sales/Date Sales/CalendarDate -t Hierarchy --save   # Disambiguate hierarchy from column
te move "Sales/Partitions/Old" "Sales/Partitions/New" --save   # Container-form paths work too
```

## Inspección

### list

Enumera objetos con una navegación similar a la del sistema de archivos. Acepta un argumento `<path-filter>` que admite comodines. Se admiten tanto contenedores de nivel de modelo como contenedores con ámbito de tabla; consulta la [tabla de palabras clave de contenedores](#containers-and-keywords) anterior para ver la lista completa. (Alias: `ls`.)

`te list` acepta:

- `--type <kind>` - limita a un tipo de objeto (`table`, `measure`, `column`, `hierarchy`, `partition`, `relationship`, `role`, `perspective`, `culture`, `calculationitem`, `kpi`, `set`, `function`). Sin `<path-filter>`, esto equivale a escribir la palabra clave del contenedor correspondiente.
- `--paths-only` - emite una ruta de objeto por línea, ideal para pasarlo a `xargs`, `te get` o `te set`.
- `--no-multiline` - contrae las celdas multilínea (normalmente expresiones DAX o M) a una sola línea y las trunca para que las filas sigan siendo fáciles de recorrer en tablas anchas. Solo afecta a la salida de texto; la salida JSON/CSV/TMSL no se ve afectada.
- `--output-format tmsl` (alias `bim`) - genera los objetos coincidentes como un script TMSL/BIM. Útil para `te list Tables --output-format bim > tables.json`. `--output-format tmdl` no es compatible con `ls` (TMDL solo admite un único objeto; usa `te get`).

```bash
te list                                     # All tables in the model
te list Sales                               # All children of Sales (columns + measures + hierarchies + partitions)
te list Sales/Measures                      # Just Sales's measures
te list 'Sales/*Amount'                     # Children of Sales whose name ends with Amount
te list 'Sa*'                               # Tables whose name starts with Sa (no auto-expansion)
te list '*/Amount'                          # An Amount column/measure across every table
te list 'Roles/Re*/Members'                 # Members of every role matching Re*
te list Sales/Geography/Levels              # All levels of the Geography hierarchy
te list KPIs                                # All KPIs (with parent measure)
te list Sales/KPIs                          # KPIs on measures of Sales
te list Sets                                # Calculated sets
te list Functions                           # DAX user-defined functions
te list "'Net Sales'/'Sales Amount'"        # Quote names containing spaces
te list Measures --paths-only               # One Table/Measure per line for piping
te list --type measure                      # Same as `te list Measures`
te list Measures --no-multiline             # Wide table with column dividers, single-line DAX
te list Tables --output-format bim > tables.json   # All tables emitted as TMSL/BIM
```

En la salida JSON, cada objeto listado empieza con su `objectPath`: una ruta canónica que se resuelve con `te get`.

### get

Obtén propiedades de un objeto del modelo, filtra y lista conjuntos de objetos, y analiza dependencias: `get` es el único pipeline de lectura de la CLI (`te list` y `te deps` se mantienen como accesos directos). Acepta un `<path>`; omítelo para listar el modelo (igual que `te list`) o pasa `.` para la raíz del modelo. Una ruta con comodines (`te get "Sa*"`) o una ruta de contenedor (`te get Sales/Measures`) lista todas las coincidencias sin necesidad de `--ls`; `-p`, `--deps` y `--properties` requieren exactamente un objeto, así que en una ruta con comodines lo indican y sugieren quitar la opción.

`te get` acepta:

- `-p, --property <property>` - proyecta una única propiedad (p. ej., `expression`, `formatString`).
- `--where <Prop=Value>` - filtra el conjunto de resultados; se puede repetir (AND), sin distinguir mayúsculas de minúsculas. Un valor sin `*` es una coincidencia exacta; `*` es un comodín, así que para buscar por contenido se usa `--where Name=*margin*`. Sin ruta, `--where` filtra las **tablas de nivel superior** del modelo; pasa un contenedor para buscar otros tipos (`te get Measures --where Name=*margin*`). Un resultado vacío indica qué se buscó y cómo se hizo coincidir el patrón, y ofrece comandos para ampliar la búsqueda.
- `--properties` - lista los nombres de propiedad que `-p` acepta en el objeto resuelto, con el tipo de cada propiedad, si se puede escribir, qué contiene y, cuando una propiedad admite un conjunto fijo de valores, los valores que acepta. Se muestran ambas grafías cuando difieren (`Hidden` / `IsHidden`), y las anotaciones y las traducciones aparecen en el formato entre corchetes en el que deben escribirse. Se omiten las propiedades internas de control; `--all` las agrega. Solo salida de texto y JSON; requiere una ruta de un solo objeto y no se puede combinar con `-p`, `--ls`, `--where`, `--deps` ni `--unused`.
- `--ls` - disposición compacta en tabla (la misma representación que `te list`).
- `--deps [upstream|downstream]` - análisis de dependencias (predeterminado: ambas direcciones); `--deep` para el árbol recursivo, `--max-depth <N>` (valor predeterminado `10`).
- `--unused` / `--hidden` - muestra los objetos no usados, como en `te deps`.
- `--paths-only` - una ruta canónica de objeto por línea, para usar en canalizaciones.
- `--no-multiline` - contrae las celdas multilínea (con `--ls`/`--where`). Solo para la salida de texto.
- `-t, --type <kind>` - desambigua cuando la ruta coincide con varios elementos secundarios de una tabla (p. ej., una columna y una jerarquía con el mismo nombre). Valores: `Measure`, `Column`, `CalculatedColumn`, `Hierarchy`, `Calendar`, `Partition`, `CalculationItem`.
- `--output-format tmsl` (alias `bim`) - genera el objeto resuelto como JSON TMSL/BIM.
- `--output-format tmdl` - genera el objeto resuelto como TMDL (solo objetos con nombre).

`te get` y `te list` comparten un único catálogo de descriptores, de modo que todas las propiedades se muestran igual en todos los formatos: la tabla de texto, JSON y CSV ven el mismo conjunto, y al agregar una propiedad nueva al modelo, esta queda expuesta en todos ellos.

La línea `Settable:` debajo del resultado de `te get <path>` enumera las propiedades que `te set` acepta en ese objeto (`SortByColumn` entre ellas) y termina con una referencia a `--properties` para la lista completa; un nombre de propiedad desconocido en `te get -p` o `te set -p` remite al mismo listado. `te get -p` resalta la sintaxis de todas las propiedades con valor de expresión, incluidas las filas de detalle y las expresiones de cadena de formato dinámicas. En la salida JSON, un solo objeto empieza con `objectPath` (la ruta canónica, que puede resolverse tal cual con `te get`, `te set` o `te remove`), seguido de `type` y `properties`; un listado que no coincide con nada imprime un array vacío.

```bash
te get Sales/Amount -p expression                # Print DAX
te get "'Sales'[Amount]"                         # DAX form: same as Sales/Amount
te get "[Total Sales]"                           # Lone-bracket: model-wide measure-or-column
te get "'Net Sales'[Sales Amount]" -p expression # DAX form with spaced names
te get Sales/Revenue/KPI                         # KPI sub-object of a measure
te get Sales --output-format tmdl                # Emit the table as TMDL
te get Sales --output-format bim                 # Emit the table as TMSL/BIM
te get . -p description                          # Model-level property
te get "Sa*"                                     # Every table matching the wildcard, no --ls needed
te get Measures --where IsHidden=true --ls       # Filter + list rendering
te get Measures --where Name=*margin*            # Contains-search across all measures
te get Sales/Amount --properties                 # Property names -p accepts, with types and allowed values
te get Sales/Revenue --deps downstream --deep    # Recursive dependents
```

### find

Busca texto en propiedades de cadena y muestra cada ubicación donde haya una coincidencia. De forma predeterminada, el patrón es una **subcadena literal sin distinción entre mayúsculas y minúsculas**; `te find "Gross*"` busca un asterisco literal, así que pasa `--regex` para la coincidencia de patrones. Usa `te get --where Name=*Gross*` cuando quieras filtrar objetos por el valor de una propiedad en lugar de hacer una búsqueda de texto. Un resultado vacío indica el ámbito en el que se buscó y el modo de coincidencia utilizado, y ofrece comandos para ampliar la búsqueda; si el patrón `--regex` no es una expresión regular válida, se rechaza con un error que indica la opción y el patrón.

`te find` acepta:

- `--in <scope>` — ámbito: `names`, `expressions`, `descriptions`, `displayFolders`, `formatStrings`, `annotations`, `all` (predeterminado: `all`).
- `--regex`, `--case-sensitive`, `--paths-only`.
- `--no-multiline` - contrae el contexto de coincidencia multilínea a una sola línea. Solo salida de texto.

`--in expressions` abarca todos los `IExpressionObject` del modelo, incluidas las `TargetExpression` / `StatusExpression` / `TrendExpression` de los KPI, la `DetailRowsExpression` de la medida, el M de origen/sondeo de la partición, la `FilterExpression` de los permisos de tabla y las expresiones `MultipleOrEmptySelection` / `NoSelection` del grupo de cálculo; así, un literal como `123` definido en el objetivo de un KPI aparece igual que el cuerpo de una medida.

```bash
te find "CALCULATE" --in expressions
te find "Revenue" --in names
te find "CALCULATE" --in expressions --paths-only | xargs -I{} te get {} -p expression
te find "Gross.*Margin" --in names --regex
```

Con `--output-format json`, `te find` emite un Report del ámbito que buscó y del modo de coincidencia que usó junto con las coincidencias.

### diff

Compara dos modelos para detectar diferencias estructurales. Devuelve los siguientes códigos de salida: `0` = idéntico, `1` = diferencias encontradas, `2` = error.

Los cambios se incluyen en el Report del mismo modo que los comandos que realizan modificaciones: una entrada consolidada por cada objeto cambiado, con líneas `-`/`+` por propiedad en la salida de texto. En JSON, las entradas del array `changes` incluyen `objectPath` (la ruta canónica, que puede pasarse por una tubería a `te get`), `objectType` (el mismo vocabulario cerrado que el JSON de hallazgos: `KPI`, `Member`, ...), `changeKind` (`created`, `deleted`, `modified` o `moved`; un objeto renombrado que lleva una etiqueta de linaje es una única entrada `moved` con `movedFromObjectPath`) y un array `properties` de `{property, before, after}` con nombres de propiedad en PascalCase. Un objeto que existe solo en uno de los dos modelos se lista junto con su contenido —los filtros de seguridad a nivel de filas de un rol nuevo, las columnas, medidas y particiones de una tabla nueva, los niveles de una jerarquía nueva—, cada elemento como una entrada independiente, y los recuentos del resumen los incluyen.

```bash
te diff ./model-v1 ./model-v2
te diff old.bim new.bim

# Branch on exit code (POSIX sh):
te diff ./a ./b; case $? in 0) echo same;; 1) echo different;; *) echo error;; esac

# Branch on exit code (PowerShell):
te diff ./a ./b; switch ($LASTEXITCODE) { 0 { 'same' } 1 { 'different' } default { 'error' } }
```

### deps

Analiza las dependencias ascendentes y descendentes de un objeto, o detecta objetos sin usar en todo el modelo. Un atajo para `te get --deps` / `te get --unused`. La forma de un solo objeto acepta un `<path>`.

`te deps` admite:

- `--upstream` - muestra solo las dependencias ascendentes (lo que usa este objeto).
- `--downstream` - muestra solo las dependencias descendentes (los objetos que usan este objeto).
- `--deep` - muestra el árbol de dependencias recursivo en lugar de solo las dependencias directas.
- `--max-depth <N>` - profundidad máxima para el recorrido de `--deep` (predeterminado: `10`).
- `-t, --type <kind>` - desambigua cuando la ruta coincide con varios elementos secundarios de una tabla (p. ej., una columna y una jerarquía con el mismo nombre).
- `--unused` - enumera las medidas, las columnas calculadas y **todas las columnas de datos** a las que no hace referencia ninguna expresión DAX y que no se usan en ninguna relación, nivel de jerarquía, ordenación por columna, variación, base de AlternateOf ni rol de tiempo de calendario. Cada resultado muestra `(hidden)` en modo de texto y un campo `isHidden` en JSON.
- `--hidden` - limita `--unused` a solo los objetos ocultos. Los objetos ocultos y sin usar son los candidatos más seguros para eliminar, porque ningún elemento visible para el usuario depende de ellos.

En la salida JSON, cada entrada —y cada nodo de árbol `upstream`, `downstream` y `--deep`— se nombra igual que el resto de la CLI nombra los objetos: `objectPath` (ruta canónica, que se puede canalizar a `te get`), `object` (nombre simple) y `objectType`.

```bash
te deps Sales/Revenue                     # Upstream + downstream for one object
te deps "'Sales'[Revenue]"                # DAX form is accepted everywhere a <path> is
te deps Sales/Revenue --downstream --deep # Everything that depends on Revenue, recursively
te deps --unused                          # All unused measures and columns
te deps --unused --hidden                 # Only hidden, unused objects
```

## Análisis y calidad

### validate

Valida las expresiones del modelo, la integridad del esquema y los errores de TOM.

`te validate` admite:

- `--ci <fmt>` - emite anotaciones de CI a stderr: `vsts` (alias `azdo`, `azure-devops`) o `github` (alias `gh`). `none` o un valor vacío indican que no hay anotaciones; cualquier otro valor se rechaza antes de ejecutar el comando.
- `--trx <PATH>` - escribe los resultados en un archivo `.trx` de VSTEST.
- `--errors-only` - forma abreviada de `--no-warnings --no-antipatterns`: muestra solo errores.
- `--no-warnings` - oculta las advertencias del analizador semántico.
- `--no-antipatterns` - oculta las sugerencias de antipatrones (recomendaciones de buenas prácticas de DAX).
- `--server-only` - muestra solo los errores notificados por el servidor conectado; omite el análisis semántico local.
- `--no-multiline` - contrae el contenido de varias líneas de las celdas (mensajes de error, expresiones) en una sola línea. Solo para la salida de texto.

```bash
te validate -m ./model
te validate --ci github --trx results.trx
te validate --errors-only                 # Hide warnings and anti-pattern hints
```

Cada hallazgo lleva un código estable, que se muestra en la columna **Código** de las tablas de Errores, Advertencias y Antipatrones, así como en JSON, en las anotaciones `--ci` y en `--trx`. Hay tres códigos que conviene conocer cuando se trabaja con un modelo escrito a mano: `TE0012` (una columna y una medida, o dos columnas, comparten nombre dentro de una misma tabla) y `TE0013` (el nombre de una medida se repite entre tablas) son errores: Analysis Services se niega a cargar ese modelo y `te save-as` se niega a escribirlo, salvo que se pase `--force` o `--skip-validation`; `TE0014` es una advertencia de que una carpeta TMDL no tiene `database.tmdl`, de modo que el nivel de compatibilidad en vigor sustituye al que declaró el modelo. La carpeta sigue cargándose y `te validate` sigue terminando con `0` para `TE0014`; oculta esta advertencia como cualquier otra con `--no-warnings` o `--errors-only`.

Con `--output-format json`, `te validate` emite el documento JSON compartido de hallazgos (`summary` más una matriz plana `findings[]`), el mismo que usan `te bpa run`, `te test run` y `te query`; consulta @te-cli-findings.

> [!NOTE]
> `te validate` no admite `--output-format csv`: CSV se rechaza desde el principio con un error claro, en lugar de producir un resultado parcial. Usa `text` o `json` para la salida de validación.

### bpa run

Ejecuta reglas de Best Practice Analyzer contra un modelo.

`te bpa run` admite:

- `-r, --rules <rules>` - ruta(s) o URL(s) a archivo(s) de reglas BPA en formato JSON. Se puede repetir. Sustituye la capa de reglas de usuario en esta invocación: consulta [Orígenes y resolución de reglas](#rule-sources-and-resolution) más abajo.
- `--no-model-rules` - excluye las reglas de BPA incrustadas en las anotaciones del modelo.
- `--no-defaults` - excluye las reglas predeterminadas de BPA integradas.
- `--vpax <file>` - carga estadísticas del Analizador VertiPaq desde un archivo `.vpax` para habilitar reglas compatibles con VPA.
- `--allow-external-rules` - permitir obtener archivos de reglas de BPA desde direcciones URL incrustadas en las anotaciones del modelo.
- `--rule <id>` - ejecutar solo regla(s) específicas por ID. Se puede repetir.
- `--path <path-filter>` - limitar el análisis a las tablas que contengan los objetos coincidentes. Acepta nombres literales, palabras clave de contenedor y comodines (por ejemplo, `'Sales'`, `'Sa*'`, `'Sales/Medidas'`, `'*/Amount'`).
- `--fix` - aplicar expresiones de corrección para corregir automáticamente las infracciones cuando sea posible.
- `--save` - volver a guardar el modelo en el origen después de aplicar las correcciones.
- `--save-to <path>` - guardar el modelo en una ruta diferente después de aplicar las correcciones.
- `--diff` / `--stat` / `--name-only` - controlan cómo se representa la salida de cambios en la pasada de corrección (consulta la nota [Edición del modelo](#model-editing)).
- `--serialization <fmt>` - serialización del modelo: `tmdl`, `bim` (alias `tmsl`), `database.json`.
- `--fail-on <severity>` - umbral de fallo: `error` (predeterminado) o `warning`. Sale con el código `1` cuando las infracciones alcanzan el umbral. Los errores al cargar o evaluar reglas (expresiones no válidas, archivos de reglas ilegibles) también provocan un código de salida distinto de cero, independientemente de `--fail-on`.
- `--ci <fmt>` - emite comandos de registro de CI a stderr: `vsts` (Azure DevOps; alias `azdo`, `azure-devops`), `github` (GitHub Actions; alias `gh`). Los valores no reconocidos se rechazan de entrada.
- `--trx <path>` - escribir los resultados como un archivo `.trx` de VSTEST en la PATH especificada.
- `--no-multiline` - contraer el contenido de varias líneas de las celdas de la tabla de infracciones en una sola línea. Solo para la salida de texto.

```bash
te bpa run --fail-on error --ci github
te bpa run --fix --save
te bpa run --rule PERF_UNUSED_HIDDEN_COLUMN
te bpa run --path Sales            # Tables touched by the Sales filter only
te bpa run --path 'Sa*'            # Wildcard - every table starting with Sa
te bpa run --path Sales/Measures   # Path filter applied to the matched tables
```

Con `--output-format json`, `te bpa run` emite el documento JSON compartido de hallazgos (consulta @te-cli-findings); con `--fix`, el JSON es un único documento que también incluye el conjunto de cambios `fix`.

#### Orígenes de las reglas y su resolución

Cada invocación de `te bpa run` reúne reglas de tres capas independientes:

1. **Reglas de usuario** - se aplica exactamente un origen, en este orden de prioridad:
   - `-r, --rules <rules>`: acepta una PATH de archivo o una URL (prioridad más alta)
   - La variable de entorno `TE_BPA_RULES`
   - la matriz `bpa.rules` de la configuración de la CLI (`~/.config/te/config.json`)
2. **Reglas integradas predeterminadas** - se cargan a menos que se pase `--no-defaults` o que [`bpa.builtInRules`](xref:te-cli-config#built-in-bpa-rules) sea `false` en la configuración. Se omiten las reglas integradas individuales incluidas en `bpa.disabledBuiltInRuleIds`.
3. **Reglas integradas en el modelo** - reglas en la anotación `BestPracticeAnalyzer_Rules` del modelo; se cargan a menos que se pase `--no-model-rules`. Se omiten las anotaciones de URL externas, a menos que también pases `--allow-external-rules`.

Los valores predeterminados integrados son exactamente el [conjunto de reglas integrado](xref:built-in-bpa-rules) documentado de Tabular Editor 3 (los identificadores `TE3_BUILT_IN_*`), por lo que `te bpa run` y TE3 Desktop coinciden en lo que marcan las reglas integradas. Las seis reglas del Analizador VertiPaq (`VPA_*`) que las versiones preliminares anteriores presentaban como integradas no forman parte de ese conjunto, y la opción `--vpa-rules` ya no existe; si una canalización depende de alguna de ellas para bloquearse, copia su definición en tu propio archivo de reglas y haz referencia a él con `--rules`, `bpa.rules` o `TE_BPA_RULES`. `--vpax` no cambia y sigue proporcionando las estadísticas que lee una regla propia compatible con VPA. Los C# Scripts y las macros (`te script`, `te macro run`) ven el mismo conjunto de reglas a través de `Bpa.Rules` y `Bpa.Analyze()`.

Cada identificador de regla se evalúa una vez. Cuando el mismo ID aparece en más de una capa, en `te bpa run` prevalece la definición de un archivo `--rules` explícito, mientras que en los controles de implementación y guardado prevalece la definición integrada. Después se eliminan los ID de reglas de la anotación `BestPracticeAnalyzer_IgnoreRules` del modelo.

La línea `Rules loaded:` de la salida atribuye cada capa que contribuye, por ejemplo:

```
Rules loaded: 38 from 1 file(s) from bpa.rules config + built-in defaults + model annotations
```

### bpa rules

Administra colecciones de reglas de BPA: enumera, inspecciona, inicializa y activa o desactiva reglas en tu archivo local de reglas o en las anotaciones del modelo. Las reglas integradas son de solo lectura; para omitir una sin perder el resto, usa `te bpa rules disable` (no edites directamente el conjunto integrado).

Subcomandos:

| Subcomando                                                | Propósito                                                                                   |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `add <id>`                                                | Agrega una nueva regla de BPA.                                              |
| [`disable`](#bpa-rules-disable)                           | Desactiva una regla de BPA integrada para el usuario actual.                |
| [`enable`](#bpa-rules-enable)                             | Vuelve a activar una regla de BPA integrada que se había desactivado antes. |
| `ignore <rule-id>`                                        | Agrega una regla a la lista de ignorados del modelo.                        |
| [`init`](#bpa-rules-init)                                 | Crea un archivo vacío de reglas de BPA en la ruta PATH resuelta.            |
| [`list`](#bpa-rules-list) (alias `ls`) | Enumera las reglas de BPA de todos los orígenes con su estado.              |
| `remove <rule-id>` (alias `rm`)        | Elimina una regla de BPA.                                                   |
| `set <rule-id>`                                           | Actualiza las propiedades de una regla del BPA.                             |
| `unignore <rule-id>`                                      | Elimina una regla de la lista de reglas ignoradas del modelo.               |

Todos los subcomandos de `te bpa rules` aceptan:

- `--rules-file <PATH>`: ruta a un archivo JSON de reglas del BPA. De forma predeterminada, se usa la primera entrada existente de `bpa.rules` en la configuración de la CLI (`~/.config/te/config.json`) o la variable de entorno `TE_BPA_RULES`.
- `--model-rules`: opera sobre las reglas incrustadas en la anotación del modelo en lugar de un archivo.

> [!IMPORTANT]
> `te bpa rules set` y `te bpa rules remove` se niegan a modificar los ID de reglas integradas. Si intentas hacerlo, el comando finaliza con el código `1` y te indica que uses `te bpa rules disable`. Para personalizar el comportamiento de una regla integrada, deshabilita la regla integrada y agrega una copia personalizada con un identificador distinto:
>
> ```bash
> te bpa rules disable TE3_BUILT_IN_DATE_TABLE_EXISTS
> te bpa rules add MY_DATE_TABLE_EXISTS
> ```

#### bpa rules list

Muestra las reglas de todos los orígenes (integradas, de usuario y del modelo). (Alias: `ls`.)

`te bpa rules list` acepta:

- (predeterminado) Solo las reglas activas.
- `--all`: incluye las reglas deshabilitadas e ignoradas.
- `--disabled`: solo los ID de reglas integradas que el usuario ha deshabilitado mediante `te bpa rules disable`.
- `--ignored`: solo las reglas cuyos ID aparecen en `BestPracticeAnalyzer_IgnoreRules` en el modelo.
- `--no-defaults`: excluye las reglas integradas de la salida.

```bash
te bpa rules list              # Active rules
te bpa rules list --all        # Include disabled and ignored rules
te bpa rules list --ignored
```

Las reglas integradas deshabilitadas se marcan con un marcador `[disabled]` junto al ID de la regla.

#### bpa rules init

Crea un archivo de reglas del BPA vacío (`[]`) en el PATH configurado. Úsalo una vez antes de ejecutar `te bpa rules set` / `te bpa rules remove` sobre una ruta que todavía no existe.

`te bpa rules init` acepta:

- `--force`: sobrescribe un archivo existente con `[]`. Es obligatorio si el archivo de destino ya existe.
- `--rules-file <path>` - ruta del archivo de destino. Puede aparecer antes o después del subcomando `init`.

Resolución de rutas (PATH; se usa la primera coincidencia): `--rules-file` → variable de entorno `TE_BPA_RULES` → primera entrada de `bpa.rules[]` en la configuración de tu CLI → `./BPARules.json` (directorio de trabajo actual).

```bash
te bpa rules init
te bpa rules init --rules-file ./MyRules.json
te bpa rules init --force
```

#### bpa rules add / set / remove / ignore / unignore

Modifica el archivo de reglas (`add`, `set`, `remove` (alias `rm`)) o la lista de exclusión integrada en el modelo (`ignore`, `unignore`). Los tres subcomandos de modificación actúan sobre `--rules-file <path>` o `--model-rules` y se niegan a modificar los ID de reglas integradas.

- `te bpa rules add <id>` - crea una regla nueva. Especifica cada propiedad como una opción con nombre:
  - `--name <text>` - nombre legible de la regla (obligatorio).
  - `--scope <list>` - tipos de objeto separados por comas a los que se aplica la regla: `medida`, `Column`, `Table`, `Hierarchy`, `partición`, `Relationship`, `Role`, `Perspective`, `Culture`, etc. (obligatorio).
  - `--expression <text>` - predicado de Dynamic LINQ. Devuelve `true` para los objetos que infringen la regla (obligatorio).
  - `--category <text>` - etiqueta de agrupación (por ejemplo, `Performance`, `Naming`, `DAX Expressions`).
  - `--severity <1|2|3>` - `1` (información), `2` (advertencia, valor predeterminado), `3` (error).
  - `--description <text>` - descripción orientada al usuario que se muestra cuando se activa la regla.
  - `--fix-expression <text>` - expresión de Dynamic LINQ que utiliza `te bpa run --fix` para corregir automáticamente.
- `te bpa rules set <id>` - actualiza las propiedades de una regla existente. Usa `-p, --property <name=value>` (se puede repetir; `-` lee el valor desde stdin). Nombres de propiedades: `name`, `expression`, `scope`, `category`, `severity`, `description`, `fixExpression`.
- `te bpa rules remove <id>` - elimina una regla.
- `te bpa rules ignore <id>` - añade un ID de regla a la anotación `BestPracticeAnalyzer_IgnoreRules` del modelo.
- `te bpa rules unignore <id>` - elimina un ID de regla de la lista de reglas ignoradas del modelo.

```bash
# Add a rule: measures that are not hidden and have no description
te bpa rules add MEASURE_NEEDS_DESCRIPTION \
    --name "Measures should have a description" \
    --scope Measure \
    --expression "not IsHidden and string.IsNullOrEmpty(Description)" \
    --severity 2 \
    --category Metadata

# Update severity on an existing rule
te bpa rules set MEASURE_NEEDS_DESCRIPTION -p severity=3

# Remove the rule
te bpa rules remove MEASURE_NEEDS_DESCRIPTION
```

#### bpa rules disable

Deshabilita una regla BPA integrada específica. El identificador de la regla se agrega a `bpa.disabledBuiltInRuleIds` en la configuración de tu CLI. Las ejecuciones posteriores del gate (deploy, save, mutation) y `te bpa run` omiten la regla deshabilitada.

El comando es idempotente: ejecutar `disable` sobre una regla ya deshabilitada finaliza correctamente sin modificar la configuración. Finaliza con el código `1` si `<rule-id>` no es una regla BPA integrada; usa `te bpa rules list` para ver los identificadores válidos de reglas BPA integradas.

```bash
te bpa rules disable TE3_BUILT_IN_DATE_TABLE_EXISTS
```

#### bpa rules enable

Vuelve a habilitar una regla BPA integrada deshabilitada anteriormente al quitar el identificador de la regla de `bpa.disabledBuiltInRuleIds`. Finaliza con el código `1` si la regla no está deshabilitada actualmente.

```bash
te bpa rules enable TE3_BUILT_IN_DATE_TABLE_EXISTS
```

### vertipaq

Analiza las estadísticas de almacenamiento de VertiPaq.

`te vertipaq` acepta:

- `<path>` - argumento posicional opcional: un nombre de tabla para filtrar el análisis y limitarlo a una sola tabla.
- `--columns`, `--relationships`, `--partitions`, `--all`.
- `--detail` - muestra columnas expandidas (desglose del tamaño de datos/diccionario/jerarquía, codificación, segmentos).
- `--fields <list>` - campos separados por comas para mostrar (p. ej., `--fields name,card,size,%tbl,%db,bar`). Los campos disponibles varían según la vista.
- `--export <file.vpax>` - exporta las estadísticas de VertiPaq a un archivo `.vpax` para analizarlas sin conexión.
- `--import <file.vpax>` - carga un archivo `.vpax` exportado previamente y lo analiza sin conexión.
- `--obfuscate` - ofusca nombres y expresiones en el VPAX exportado.
- `--top <N>`, `--stats`, `--annotate`, `--save`.
- `--auth <method>` - sustituye el método de autenticación al conectarse a un modelo remoto.

```bash
te vertipaq                      # Columns by size (default)
te vertipaq Sales                # Stats limited to the Sales table
te vertipaq --all                # Tables, columns, relationships, partitions
te vertipaq --export stats.vpax
te vertipaq --import stats.vpax  # Analyze offline
```

### Formato de expresiones

El formato de expresiones está en tres lugares, según lo que estés formateando:

- **Una expresión del modelo**: `te set <path> --format <PropertyName> --save` - consulta [set](#set).
- **Una expresión independiente** (que no está en ningún modelo): `te util format-dax` / `te util format-m` - consulta [Utilidades](#utilities).
- **Un barrido de todas las medidas del modelo**: `te script --inline "Model.AllMeasures.FormatDax();" --save`.

El DAX en un modelo siempre va separado por comas, así que `--semicolons` solo existe en `te util format-dax`, para el DAX que hayas escrito tú mismo con punto y coma.

## Ejecución

### query

Ejecuta una consulta DAX contra un modelo implementado.

`te query` admite:

- `<dax>` - argumento posicional: la consulta DAX que se va a ejecutar. Equivale a pasar `-q`. Utiliza la forma que se lea mejor; el `-q` explícito tiene prioridad si se proporcionan ambas.
- `-q, --query <dax>` - consulta en línea (variante con opción con nombre del argumento posicional anterior). `-q -` lee la consulta desde stdin; si hay entrada redirigida y no se proporciona ninguna consulta, stdin se lee implícitamente.
- `--file <file.dax>` - consulta desde un archivo.
- `--limit <N>` - valor predeterminado: 100.
- `-o, --output-file <path>` - escribe los resultados en un archivo (`.csv`, `.tsv`, `.json`, `.dax`).
- `--trace`, `--cold`, `--plan`, `--runs <N>` - seguimiento del rendimiento y pruebas comparativas.
- `--no-validate` - omite la validación semántica de DAX previa a la ejecución.

```bash
te query "EVALUATE TOPN(5, 'Sales')" -s my-ws -d my-model           # Positional DAX
te query -q "EVALUATE TOPN(5, 'Sales')" -s my-ws -d my-model        # Named-flag form
te query --file query.dax --output-format json
```

### script

Ejecuta uno o varios C# Scripts contra un modelo semántico. La CLI usa el mismo host de scripts que Tabular Editor 3 Desktop, así que un script que se ejecuta en TE3 se ejecuta aquí sin cambios.

`te script` admite:

- `--file <path>` - archivo `.cs` / `.csx` (repetible). También se aceptan argumentos posicionales `.cs`/`.csx` sin prefijo.
- `--inline <code>` - C# en línea (repetible; usa `-` para stdin).
- `--validate` - compila el/los script(s) e informa de los errores sin ejecutarlos. No necesita ningún modelo, así que funciona sin conexión como linter de CI.
- `--save` / `--save-to` / `--serialization`.
- `--diff` / `--stat` / `--name-only` - representación de la salida de cambios (consulta la nota [Edición del modelo](#model-editing)).
- `--force` - guarda incluso si la mutación introduce errores de validación de DAX.

Los archivos y los fragmentos en línea se ejecutan en el orden en que se escriben en la línea de comandos.

```bash
te script --file fix.cs --save
te script fix.cs cleanup.csx --save              # Bare positionals, run in order
te script --inline "Info(Model.Tables.Count);"
echo "Info(Model.Name);" | te script --inline -
te script --file fix.cs --validate               # Compile-only, no model needed
```

Una ejecución en la que cualquier script llama a `Error(...)` finaliza con un código distinto de cero, indica `"success": false` en JSON y termina indicando que la ejecución se completó con errores; los cambios que el script ya haya hecho se siguen guardando cuando se usa `--save`. `Warning(...)` e `Info(...)` nunca hacen que falle una ejecución. En Windows, la directiva administrativa `DisableCSharpScripts` rechaza `te script` de plano; consulta [Directivas de administrador](xref:te-cli-config#administrator-policies).

> [!IMPORTANT]
> Dos detalles de comportamiento que conviene conocer si vas a portar un script antiguo:
>
> - **No hay selección interactiva en los scripts de la CLI.** Los asistentes de TE3 Desktop `SelectMeasure()`, `SelectTable()`, `SelectColumn()`, `SelectObject()` y `SelectObjects()` lanzan `NotSupportedException` cuando se invocan desde `te script` - la CLI no tiene interfaz de usuario para mostrar una ventana emergente. Resuelve previamente el/los objeto(s) fuera del script y pásalos mediante variables de entorno o stdin, o envuelve la llamada en `try/catch` si el script se comparte con TE3.
> - **Las directivas `using` predeterminadas coinciden con las de TE3 Desktop.** Los scripts que usan `DataTable`, `File`, `StringBuilder` o `Regex` deben incluir explícitamente la directiva correspondiente `using System.Data;` / `using System.IO;` / `using System.Text;` / `using System.Text.RegularExpressions;`.

> [!NOTE]
> **Símbolos del preprocesador para scripts compartidos entre hosts.** Los scripts compilados por `te script` tienen definido el símbolo `TECLI`. En los scripts de TE3 Desktop se define `TE3` en su lugar, además de símbolos acotados por versión como `TE3_3_10_OR_GREATER` ... `TE3_3_X_OR_GREATER` para la versión menor actual de TE3. TE2 no define ninguno de los dos símbolos. Úselos para escribir scripts portátiles:
>
> ```csharp
> #if TECLI
>     // CLI-only code - no UI calls
>     Info($"Running under the CLI on {Environment.OSVersion.Platform}");
> #elif TE3
>     // TE3 Desktop-only code - UI APIs available
>     ShowMessage("Hello from TE3");
> #else
>     // TE2 (legacy) - neither TECLI nor TE3 is defined
>     Info("Hello from TE2");
> #endif
>
> #if TE3_3_15_OR_GREATER
>     // Gated on a specific TE3 minor version
> #endif
> ```
>
> Consulta @csharp-scripts para conocer el panorama general del scripting entre versiones.

### macro

Administra y ejecuta macros desde un archivo JSON de macros (normalmente `MacroActions.json`). El archivo de macros se determina en este orden: `--macros <PATH>` → la variable de entorno `TE_MACROS_PATH` → `macros` en la configuración de la CLI → `./MacroActions.json`. En Windows, la directiva administrativa `DisableMacros` rechaza todos los comandos `te macro`; consulta [Directivas de administrador](xref:te-cli-config#administrator-policies).

Subcomandos:

| Subcomando                                            | Propósito                                                             |
| ----------------------------------------------------- | --------------------------------------------------------------------- |
| `list` (alias `ls`)                | Listar macros.                                        |
| [`run <name-or-id>`](#macro-run)                      | Ejecutar una macro.                                   |
| `add <name>`                                          | Agregar una macro.                                    |
| `set <name-or-id>`                                    | Actualizar las propiedades de la macro.               |
| `remove <name-or-id>` (alias `rm`) | Eliminar una macro.                                   |
| `sort`                                                | Ordenar y reasignar los identificadores.              |
| [`init`](#macro-init)                                 | Crear un archivo de macros vacío en la ruta resuelta. |

#### macro add / set / remove

Modifica el archivo de macros (`add`, `set`, `remove` (alias `rm`)). Los tres operan sobre `--macros <path>` (o el archivo de macros resultante).

- `te macro add <name>` - crea una nueva macro. Indica el cuerpo del script mediante `-e "<code>"` (en línea) o `-s <file.cs>` (archivo de script). Opcional: `--tooltip <text>`, `--contexts <list>` (donde se aplica la macro; por ejemplo, `Table,Medida`), `--enabled true|false`.
- `te macro set <name-or-id>`: actualiza las propiedades de la macro. Usa `-p, --property <name=value>` (se puede repetir; `-` lee el valor desde stdin). Nombres de las propiedades: `name`, `execute`, `enabled`, `tooltip`, `validContexts`.
- `te macro remove <name-or-id>`: elimina una macro.

```bash
te macro add MyMacro -e "Info(Selected.Measure.Name);" --tooltip "Print measure name" --contexts Measure
te macro set MyMacro -p tooltip="Updated tooltip"
te macro remove MyMacro
```

#### macro init

Crea un archivo de macros vacío (`{"Actions":[]}`) en la ruta configurada. Úsalo una sola vez cuando el archivo de macros resultante aún no exista.

`te macro init` acepta:

- `--force` - sobrescribe un archivo existente. Obligatorio si el destino ya existe.
- `--macros <path>` - ruta del archivo de destino. Puede aparecer antes o después del subcomando `init`.

```bash
te macro init
te macro init --macros ./project-macros.json
te macro init --force
```

#### macro run

Ejecuta una macro. Las macros que emiten tablas mediante `dataTable.Output()` muestran una salida con formato en la terminal, por lo que las macros de consulta de estilo DAX funcionan igual en `te macro run` que en TE3.

`te macro run` acepta:

- `--on <path>` - establece el contexto de selección de la macro en un único objeto con nombre (una tabla, una medida, una columna, …). Equivale a hacer clic con el botón derecho en ese objeto en TE3 e invocar la macro desde el menú contextual.
- `--save` / `--save-to` - guarda cualquier cambio que realice la macro. Como todos los comandos que modifican el estado, `te macro run` realiza una simulación si no se usa `--save`.
- `--serialization <fmt>` / `--force` - igual que en los demás comandos que modifican el estado.

```bash
te macro run "Hide all measures"
te macro run "Format DAX" --on Sales/Revenue --save
te macro run "Format DAX" --on "'Net Sales'[Sales Amount]" --save   # DAX form works in --on too
```

## Implementación y actualización

### deploy

Implementa un modelo semántico en Power BI, Fabric, Azure Analysis Services o en SQL Server Analysis Services en local.

**Simulación por defecto**: `te deploy` se conecta en modo de solo lectura e imprime en stdout el TMSL exacto que enviaría. Añade `--execute` para realizar el despliegue.

`te deploy` acepta:

- `-s, --server` / `-d, --database` - el **origen** del modelo, exactamente igual que en cualquier otro comando.
- `--target-server <target>` / `--target-database <name>` - el **destino** del despliegue: el nombre de un Workspace, un endpoint o un servidor, y el nombre del modelo semántico que se va a crear o sobrescribir. Un nombre de servidor, FQDN, dirección IP o una cadena de conexión de MSOLAP implementa en Analysis Services (autenticación integrada de Windows para entornos locales); un nombre de Workspace o una URL `powerbi://...` implementa en Power BI. Si el origen del modelo es local, el destino usa como valor predeterminado la conexión activa de `te connect`; cuando el origen es remoto, las opciones de destino son obligatorias. No se permite desplegar un modelo sobre sí mismo.
- `--execute` - hace el despliegue de verdad. En modo interactivo, esto muestra un resumen y pide confirmación, con **`n` como opción segura predeterminada**; `--execute --force` omite el aviso (obligatorio en CI, donde un aviso sin `--force` es un error).
- `--deploy-full` - sobrescribir + conexiones + particiones + expresiones compartidas + roles + miembros de roles.
- `--deploy-connections`
- `--deploy-partitions`
- `--skip-refresh-policy`
- `--deploy-roles`
- `--deploy-role-members`
- `--deploy-shared-expressions`
- `--create-only`
- `--skip-bpa` - omite por completo el control de BPA.
- `--fix-bpa` - corrige automáticamente las infracciones de BPA cuando las reglas definan una expresión de corrección.
- `--bpa-rules <PATH>` - se puede repetir; anula `bpa.rules` de la configuración de tu CLI solo para este despliegue. Las reglas integradas siguen aplicándose a menos que `bpa.builtInRules` sea `false`.
- `--force` - omite la confirmación interactiva.
- `--ci <fmt>` - `vsts` (alias `azdo`, `azure-devops`) o `github` (alias `gh`); los valores no reconocidos se rechazan de entrada.
- `-p, --profile <name>` - uso puntual de un perfil de @te-cli-auth guardado.

`--output-format bim|tmdl` no se admite con `te deploy`. Para capturar el script de despliegue y revisarlo, redirige la salida de la simulación: `te deploy ... > deploy.tmsl`.

```bash
te deploy -m ./model --target-server my-workspace --target-database my-model --execute --force --ci github
te deploy -m ./model --target-server MY.SERVER.COM --target-database my-model --execute --force    # On-prem SSAS
te deploy -m ./model --target-server my-workspace --target-database my-model > deploy.tmsl         # Dry run: TMSL only
te deploy -s src-workspace -d src-model --target-server dst-workspace --target-database copy --execute   # Remote to remote
te deploy --local --target-server my-workspace --target-database my-model --execute                # Publish a Desktop model
```

> [!IMPORTANT]
> `te deploy` ejecuta el Best Practice Analyzer como control previo antes de realizar el despliegue. Consulta @te-cli-config para la configuración del control de BPA.

Un despliegue **falla** cuando el servidor informa de errores en uno o más objetos, aunque se hayan escrito los metadatos: el código de salida no es cero, el JSON indica `"success": false` con el motivo en `error`, el encabezado indica que el despliegue terminó con errores y `--ci` reporta los errores de los objetos como errores. Los objetos sin procesar no constituyen un fallo: un despliegue solo de metadatos puede dejar legítimamente objetos sin datos. La réplica del Workspace configurada con `te connect -w` aplica la misma regla.

> [!NOTE]
> Cuando se establece `--output-format json`, la carga JSON de `te deploy` siempre incluye los valores resueltos de `server` y `database`, incluso cuando se han resuelto a partir de la conexión activa o de un perfil, en lugar de pasarse explícitamente. Las canalizaciones pueden usar estos campos para confirmar el destino del despliegue sin volver a analizar la línea de comandos. `te deploy` también devuelve un código distinto de cero cuando falla con `--output-format json`, igual que en modo texto: la carga JSON es el registro del fallo, no una señal de éxito.

### refresh

Inicia una actualización de datos en un modelo implementado.

**Simulación por defecto**: `te refresh` imprime en stdout el TMSL que enviaría la actualización. Añade `--execute` para ejecutarla.

`te refresh` admite:

- `--type <type>` - `full`, `dataonly` (alias `data-only`, `data`), `automatic` (alias `auto`), `calculate` (alias `calc`), `clearvalues` (alias `clear`), `defragment` (alias `defrag`), `add` (predeterminado: `automatic`).
- `--table <name>` - actualiza tabla(s) específicas; se puede repetir.
- `--partition <Table.Partition>` - actualiza partición(es) específicas.
- `--execute` - ejecuta realmente la actualización. En un terminal pide confirmación, con **`n` como opción segura predeterminada**; añade `--force` para omitir la pregunta. Una ejecución desatendida (salida redirigida, `--output-format json` o `--non-interactive`) se detiene con un error si no se indica `--force`, así que `te refresh --type full --execute --force` es la forma que se usa en CI.
- `--force` - omite el aviso de confirmación.
- `--apply-refresh-policy <true|false|table>` - aplica las políticas de actualización incremental para determinar qué particiones se actualizan; indica el nombre de una tabla para limitar la actualización a esa tabla. Las políticas se aplican de forma predeterminada cuando el tipo y el ámbito de la actualización son compatibles, excepto en los modelos alojados en Power BI Desktop. Un valor explícito prevalece (con advertencias cuando no puede surtir efecto).
- `--effective-date <yyyy-MM-dd>` - establece la fecha efectiva que usa la política de actualización (se omite, con una advertencia, cuando no se aplica ninguna política).
- `--max-parallelism <N>` - establece el número máximo de particiones que se pueden actualizar en paralelo. Encapsula la actualización en un comando TMSL `sequence`.
- `--no-progress`, `--trace [path]`. `--trace` sin `--execute` muestra una advertencia e imprime el TMSL. Las marcas de tiempo de la traza provienen del reloj del servidor; el registro se conserva hasta que el servidor termina de entregar los eventos almacenados en búfer, y las trazas `te-refresh-*` de más de una hora que hayan quedado de ejecuciones interrumpidas se detienen y se descartan al inicio de una actualización con traza (las trazas de otras herramientas nunca se modifican).

Las actualizaciones ejecutadas con `--output-format json` siempre incluyen una matriz `progress`; con la clave de configuración `vertipaqOnRefresh` habilitada, también se incluye una matriz `vertipaq` por tabla (filas, tamaño, columnas); no hace falta `--trace`.

```bash
te refresh --type full --execute                        # Full refresh (asks for confirmation at a terminal)
te refresh --type full --execute --force                # Unattended: skip the confirmation
te refresh --table Sales --type full --execute          # Single table
te refresh --type full > refresh.tmsl                   # Dry run: emit TMSL only
te refresh --apply-refresh-policy Sales --execute       # Apply Sales' incremental refresh policy
```

Las políticas de actualización incremental se definen con [`te set`](#incremental-refresh-policies) en el subobjeto `RefreshPolicy` de una tabla.

## Pruebas

### test run

Ejecuta un conjunto de pruebas de aserción de DAX contra un modelo desplegado.

`te test run` admite:

- `--suite <path>` - directorio de la suite de pruebas (predeterminado: `.te-tests/`).
- `--tag <tag>` - solo las pruebas con esta etiqueta.
- `--fail-on <severity>` - `error` (predeterminado) o `warning`.
- `--ci <fmt>`, `--trx <PATH>` - anotaciones de CI y salida TRX.

```bash
te test run --ci github --trx results.trx
te test run --tag revenue
```

Las suites se validan antes de establecer cualquier conexión; una suite que no supera la validación (por ejemplo, si falta `query_file`) finaliza con `1` sin ejecutar nada. Con `--output-format json`, `te test run` emite el documento JSON compartido de hallazgos con campos adicionales específicos de las pruebas (`suites`, `invalidSuites`, `testSummary`); consulta @te-cli-findings.

### test init / spec / use / list / snapshot / compare

`te test list` también acepta el alias `ls`.

Los subcomandos adicionales permiten crear la estructura de las pruebas, imprimir el formato de la especificación de aserciones, cambiar la suite activa, listar las suites, capturar instantáneas y comparar modelos. Consulta `te test --help` para más detalles.

```bash
te test init --example             # Scaffold an example suite
te test spec                       # Print the full assertion format reference
te test init --from-model --model ./my-model  # Generate stubs from your measures
```

## Conexión y autenticación

### connect

Establece (o muestra) la conexión activa para la sesión actual del terminal. Consulta @te-cli-auth.

```bash
te connect                                # Show current active connection
te connect my-workspace my-model          # Remote (positional)
te connect -s my-workspace -d my-model    # Remote (named-flag form)
te connect ./model                        # Local
te connect --local                        # Local Analysis Services instance (Windows)
te connect --local my-model               # Match an instance (e.g. an open report's window title) or a database name
te connect --profile prod                 # Activate a saved profile
te connect --clear                        # Clear the active connection (and any workspace mirror)
```

`te connect --local` enumera todas las instancias locales de Analysis Services: Power BI Desktop (versiones de Store y del instalador), Workspaces de Visual Studio y SSAS independiente; cuando una instancia aloja varias bases de datos, muestra un mensaje en dos pasos (primero la instancia y luego la base de datos). El modo no interactivo falla con la lista de candidatos en lugar de elegir en silencio; acótala con `te connect --local <database>`.

#### Modo del área de trabajo (`-w` / `--workspace`)

Empareja un origen principal con un destino secundario para que cada `--save` posterior sincronice el modelo entre ambos. Útil para mantener una copia de trabajo local de un Workspace remoto o para enviar los cambios locales a un Workspace al guardar.

- `te connect <ws> <model> -w ./src` - el origen principal es remoto; `./src` recibe una exportación inicial de TMDL y refleja cada guardado.
- `te connect ./src -w <ws> <model>` - el origen principal es local; un despliegue inicial envía el modelo al Workspace, y los guardados posteriores lo vuelven a desplegar automáticamente.
- `--workspace-format <fmt>` - elige el formato en disco al reflejarlo en una carpeta/archivo: `tmdl`, `bim` (alias `tmsl`) o `database.json`. Cuando se omite, el formato se infiere a partir de la ruta de destino del Workspace (por ejemplo, `-w ./model.bim` infiere BIM).
- `--workspace-auth <method>` - método de autenticación para un destino de Workspace remoto cuando el principal es local. Toma el valor de `--auth` si está establecido; de lo contrario, `auto`.
- `--force`: obligatorio cuando el destino ya existe (carpeta no vacía o base de datos existente). Sin él, `te connect` muestra un prompt interactivo `y/n`, con `n` como opción segura predeterminada.

Una vez activado, `te set --save`, `te remove --save`, `te script --save`, etc. guardan de forma transparente en ambos destinos. El orden de guardado siempre es **primero local y después remoto**, para que la copia en disco refleje el último cambio del usuario aunque falle el envío al servidor. Borra la réplica con `te connect --clear`.

```bash
te connect Finance "Revenue Model" -w ./revenue-model    # Mirror remote → local TMDL
te connect ./revenue-model -w Finance "Revenue Model"    # Mirror local → remote
```

### auth login / status / logout

Administra la autenticación almacenada en caché. Consulta @te-cli-auth.

### profile list / show / set / remove

Administra perfiles de conexión con nombre. (`te profile list` tiene como alias `ls`; `te profile remove` tiene como alias `rm`.) Consulta @te-cli-auth.

## Configuración

### config list / paths / init / set

Ver y administrar la configuración de la CLI. (`te config list`, alias: `ls`.) Consulta @te-cli-config.

`te config set` acepta un par posicional `key value` o el equivalente `-p key=value`.

```bash
te config list                          # Display all settings
te config paths                         # Resolved macros and BPA rules file paths
te config init                          # Create default config
te config set autoFormat true
te config set -p spinner=false          # -p form
```

## Utilidades

Herramientas auxiliares que no requieren modelo. Los subcomandos de `te util` nunca actúan sobre un modelo: `--model`, `-s`/`-d`, `--local`, `--recent` y `--auth` se rechazan.

### util format-dax

Dar formato a una expresión DAX aislada.

- `<expression>` - la expresión que se va a formatear; `-` la lee de stdin.
- `--semicolons` - da formato a DAX escrito con punto y coma como separador de listas (configuración regional europea). La opción selecciona el dialecto con punto y coma tanto para la expresión que se lee como para la salida, así que está pensada para DAX que hayas escrito con punto y coma; el DAX separado por comas da un error de sintaxis si la usas. Solo se acepta aquí: `te set --format` lo rechaza, porque una expresión almacenada en un modelo siempre va separada por comas.
- `--long` - formato largo con menos saltos de línea. De forma predeterminada se usa el formato corto.
- `--no-space-after-function` - omite el espacio después de los nombres de función.

```bash
te util format-dax "SUM ( Sales[Amount] )"
cat query.dax | te util format-dax -
te util format-dax "CALCULATE(SUM(Sales[Amt]); Sales[Region] = \"EU\")" --semicolons   # Semicolon-authored DAX
```

La salida JSON incluye `success`, `formatted` y `errors`. Para las expresiones que ya estén en el modelo, usa `te set <path> --format <PropertyName>`; para un barrido de todas las medidas del modelo, `te script --inline "Model.AllMeasures.FormatDax();" --save`.

### util format-m

Da formato a una expresión M/Power Query independiente. `-` lee desde stdin; no hay opciones específicas del lenguaje. Una expresión mal formada —por ejemplo, una cadena sin cerrar— se reporta como un fallo con un código de salida distinto de cero y se devuelve el texto original sin cambios; nunca se devuelve en silencio un resultado truncado.

```bash
te util format-m "let x = 1 in x"
cat partition.m | te util format-m -
```

### util migrate

Guía de referencia que muestra cómo las opciones heredadas de la CLI de Tabular Editor 2 se corresponden con la nueva CLI. Útil como referencia rápida mientras migras una canalización basada en TE2. Consulta @te-cli-migrate para ver la guía de migración completa.

```bash
te util migrate                   # Full flag mapping table
te util migrate -A                # Look up a single TE2 flag
te util migrate --output-format json     # Machine-readable mapping
```

## Shell

### interactive

Inicia una sesión REPL guiada con un prompt adaptado al modelo. Consulta @te-cli-interactive.

> [!TIP]
> Si ejecutas `te` en un terminal sin argumentos, también accederás al REPL de forma predeterminada (como si ejecutaras `te interactive`). Se controla mediante la clave de configuración `launchInteractiveMode`. Consulta @te-cli-interactive#auto-launch-on-empty-invocation.

`te interactive` admite:

- `--no-banner` - omite el banner de bienvenida al iniciar. Útil si controlas el REPL desde scripts.
- `--echo` - muestra en stdout cada comando ejecutado antes de su salida. Útil cuando canalizas comandos por stdin para que el registro muestre qué se ejecutó.
- `--batch` - modo por lotes no interactivo: lee comandos de stdin línea a línea, ejecuta cada uno y sale al llegar al EOF. Se habilita automáticamente cuando stdin se redirige.
- `--no-batch` - fuerza el modo TTY interactivo incluso cuando stdin se redirige (es mutuamente excluyente con `--batch`).

```bash
te interactive                                # Connect later
te interactive --model ./model                # Start with a local model
te interactive -s MyWorkspace -d MyModel      # Start with a remote model
printf "list Measures\nexit\n" | te interactive --model ./model   # Pipe commands via stdin
```

Dentro de la sesión, los comandos que modifican dejan los cambios en preparación en memoria: `save` (sin argumentos) confirma las ediciones preparadas y `revert` las descarta, mientras que `save-as` vuelve a serializar en un formato o una ubicación. Al cerrar una sesión que aún tiene cambios pendientes, se pide confirmación (o, cuando nadie puede responder, se muestra una advertencia y se sale con un código distinto de cero); `exit --force` los descarta de forma deliberada; consulta @te-cli-interactive.

Las comillas y las referencias de estilo DAX funcionan igual que fuera de la sesión - consulta la sección [Rutas de objetos](#object-paths) de arriba y @te-cli-interactive para más detalles sobre la división de argv con reconocimiento de corchetes dentro del REPL.

### sesión

Muestra o administra la sesión actual del terminal. La CLI guarda el estado de cada terminal (conexión activa, perfil activo y conjunto de pruebas activo) en un archivo de sesión, aislado por proceso de shell. Establece la variable de entorno `TE_SESSION` para compartir una sesión con nombre entre procesos de shell.

Subcomandos:

| Subcomando                             | Propósito                                                                                                                                                                                                 |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `show`                                 | Muestra los detalles de la sesión actual (ID, ruta de archivo, estado activo). Es la opción predeterminada cuando no se proporciona ningún subcomando. |
| `list` (alias `ls`) | Lista todos los archivos de sesión.                                                                                                                                                       |
| `clear`                                | Borra el estado activo de la sesión actual.                                                                                                                                               |
| `prune`                                | Elimina los archivos de sesión cuyo proceso de shell ya no está en ejecución.                                                                                                             |

`te session prune` acepta:

- `--all` - también elimina las sesiones con shells activos, así como las sesiones con nombre (`TE_SESSION`). La sesión actual siempre se conserva.
- `--dry-run` - muestra qué se eliminaría, sin eliminar nada.

```bash
te session                        # Show current session details
te session list                   # List all session files
te session clear                  # Clear active state for this session
te session prune                  # Remove sessions whose shell is dead
te session prune --all --dry-run  # Preview a full cleanup
```

### completion

Genera un script de autocompletado para la shell en `bash`, `zsh`, `powershell` (alias `pwsh`) o `fish`. Consulta @te-cli-install.

```bash
te completion bash
te completion zsh
te completion pwsh
te completion fish
```

## Códigos de salida

| Código de salida | Significado                                                                                                                                                                                                                                                                                                                                                                                            |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `0`              | Éxito.                                                                                                                                                                                                                                                                                                                                                                                 |
| `1`              | Error genérico (argumentos no válidos, fallo del comando, errores de validación, error de autenticación, control de BPA fallido con gravedad >= error, una ejecución de `te script` en la que un script reportó un error, un `te deploy` que el servidor aceptó con errores de objeto). Para `te diff`: se encontraron diferencias. |
| `2`              | Solo en `te diff`: se produjo un error durante la comparación, por lo que se desconoce el estado de las diferencias.                                                                                                                                                                                                                                                   |

Para un control detallado en las canalizaciones de CI, combina los códigos de salida con las anotaciones `--ci <vsts/github>` y los archivos de resultados `--trx`; consulta @te-cli-cicd.

## Páginas relacionadas

- @te-cli - información general y contexto.
- @te-cli-install - instalación y configuración de la CLI.
- @te-cli-auth - autenticación y administración de conexiones.
- @te-cli-config - archivo de configuración, BPA gate y comportamiento tras la mutación.
- @te-cli-findings - el JSON de hallazgos compartido por validate, bpa run, test run y query.
- @te-cli-migrate - mapeo de opciones TE2 → TE3.
