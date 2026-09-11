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

- **`<path>`**: identifica **exactamente un** objeto o contenedor. Used by commands that change the model or need a single target: `te set`, `te add`, `te remove`, `te move`, `te deps`, `te macro run --on`, and `te get` with `-p`, `--deps`, or `--properties`.
- **`<path-filter>`**: identifica **cero o más** objetos y admite comodines. Used by commands that operate on a set: `te list`, plain `te get` (a wildcard or container path lists every match), `te bpa run --path`, and other inspection-style commands.

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

The reserved characters in paths are `/ [ ] ' " * ? { }`. A segment containing any of `* ? { }` must be quoted (`te get "Tables/'{foo}'"`, `te get 'Sales/"my*name"'`); unquoted use is rejected with an error naming the character and showing the quoted form. `?` is reserved and has no wildcard meaning. Every path the CLI prints - in errors, hints, `--paths-only` output, and the `objectPath` field in JSON - is canonically quoted and can be pasted straight back into `te get`. The mixed-quote forms require PowerShell or bash; cmd.exe cannot express them.

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
| `Tables`, `Measures`, `Columns`, `Hierarchies`, `Partitions`, `KPIs`, `Sets`                                                     | Modelo    | Todos los objetos de ese tipo en todo el modelo. |
| `Relaciones`, `Roles`, `Perspectives`, `Cultures`, `DataSources`, `Expressions`, `CalculationGroups`, `Functions`, `Annotations` | Modelo    | Contenedores a nivel de modelo.                  |
| `Measures`, `Columns`, `Hierarchies`, `Partitions`, `Calendars`, `CalculationItems`, `KPIs`, `Sets`                              | Tabla     | Subcontenedores dentro de una tabla.             |
| `Levels`                                                                                                                         | Jerarquía | Niveles de una jerarquía.                        |
| `Members`, `TablePermissions` (alias `Permissions`)                                                           | Rol       | Elementos hijos de un rol.                       |

Calculated sets are addressable in container form only (`<table>/Sets/<name>`); an individual KPI is `<table>/<measure>/KPI`; calendars resolve at `<table>/Calendars/<name>`; relationships resolve at `Relationships/<name>` (the relationship's own name in the model: a GUID, or a label such as `Relationship 1`; `--paths-only` prints it, and the display name is also accepted).

Algunos ejemplos muestran en qué se diferencian las rutas simples y las rutas con ámbito de contenedor:

```bash
te get Sales/Revenue                       # Measure or column on Sales
te get Sales/Measures/Revenue              # Same, container-scoped - disambiguates if other kinds share the name
te get Sales/Geography/Levels/Year         # Specific level of a hierarchy
te get Roles/Admin/Members/bob@example.com # Role member
te get Sales/refreshPolicy                 # Refresh-policy sub-object on a table
te get Sales/Revenue/KPI                   # KPI sub-object of a measure
```

Pon un segmento entre comillas para forzar la coincidencia literal del nombre cuando el nombre real de un objeto coincide con una palabra clave. La tabla cuyo nombre literal es `Tables` es `'Tables'` y se accede con `te get "'Tables'"`. The same applies to tables named `KPIs` or `Sets`.

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

Los segmentos mal escritos generan un error contextual con una sugerencia de "quizás quisiste decir" cuando la CLI puede deducir lo que querías decir. The list offers tables, measures, columns, and hierarchies, each as a full `Table/Object` path that pastes straight back into the next command. A name written in single quotes is a table reference (`te deps 'Revenue'` looks for a table named Revenue), and the error points at the `Table/Object` and `"[Object]"` forms for anything that is not a table. Las rutas a las que les falta el elemento padre fallan antes de la comprobación del elemento hoja, así que los mensajes señalan el segmento que realmente está mal. Every path an error or hint prints is taken from your model and quoted so it resolves as printed - a refusal never suggests a path that does not exist. Empty containers (e.g., `te list Hierarchies` on a model without hierarchies) emit a simple "nothing here" hint rather than an error.

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
| `--local`                  | Connect to a locally running Analysis Services instance - Power BI Desktop, Visual Studio workspaces, or standalone SSAS (Windows only).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `--auth <method>`          | Método de autenticación: `auto`, `interactive`, `spn`, `env`, `managed-identity` (predeterminado: `auto`).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `--output-format <format>` | Formato de Stdout: `text` (predeterminado), `json`, `csv`, `tmsl` (alias `bim`), `tmdl`. `csv` se respeta en los comandos que emiten datos tabulares; `tmsl`/`tmdl` solo se respetan en `te get` y `te list` para la serialización de objetos completos. Los comandos rechazan los formatos que no admiten.                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `--error-format <format>`  | Formato de stderr para errores, advertencias y sugerencias: `text` (predeterminado) o `json`. Para cualquier otro valor, se usa `text`. Es independiente de `--output-format`, así que puedes combinar stdout en JSON con errores en texto sin formato (o viceversa).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `--recent [N]`             | Usa un modelo que hayas usado recientemente. Sin valor = selector interactivo; `N` = el N-ésimo más reciente (1 = el último usado).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `--non-interactive`        | Desactiva todas las indicaciones interactivas. Finaliza con un error accionable si falta algún dato obligatorio.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `--debug`                  | Habilita el registro de depuración en stderr (cadenas de conexión, flujo de autenticación, tiempos).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |

`te --version` muestra la versión de la CLI y sale.

En los comandos que leen un modelo, el orden de resolución es:

`--recent` → `--local` → `--server`/`--database` (remote) → `--model` → active connection from `te connect`.

The model is never a positional argument - a stray path on the command line is rejected with an "unrecognized command or argument" error. (Positional arguments on `te connect`, `te init`, `te diff`, and `te query` are those commands' own subjects, not the model.)

> [!NOTE]
> **Las opciones mal escritas se rechazan de entrada.** Si pasas un `--flag` que no se reconoce en el comando que invocaste, la CLI finaliza con un error claro en lugar de interpretarlo silenciosamente como un argumento posicional. Esto detecta errores tipográficos como, por ejemplo, que `--force ` se convierta accidentalmente en `--forec` en scripts de CI.

> [!NOTE]
> **Nombres de servidor con puntos.** `-s`/`--server` trata un nombre con puntos (por ejemplo, `Sales.2026`) como el nombre de host de un servidor de Analysis Services, no como un Workspace de Power BI. Se muestra una advertencia cuando la CLI tiene que hacer esta interpretación, con una sugerencia para agregar `.Workspace` (por ejemplo, `Sales.2026.Workspace`) o usar una URL `powerbi://` completa si en realidad te referías al Workspace de Power BI. Se aplica a `te connect`, `te deploy`, `te refresh`, `te query`, `te vertipaq` y `te test run`.

## Model initialization and save

### save-as

Re-serialize a model to a different format or location. Úsalo para escribir en archivos locales un modelo de un Workspace remoto, convertir formatos o guardar de nuevo las ediciones en el origen. (Alias: `save`.)

`te save-as` accepts:

- `-o, --output-path <path>` - archivo o carpeta de destino. **Optional** - when omitted, `te save-as` writes back to the source location, preserving the original format.
- `--serialization <fmt>` - `tmdl`, `bim` (alias `tmsl`), `Database.json`, `pbip`. When omitted, the format is the loaded model's format; with `-o`, it is inferred from the output path (`.bim` writes a single-file BIM, `.json` a `database.json` folder).
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

`--serialization pbip` output opens directly in Power BI Desktop and is named after the source model (`SpaceParts.pbip`, not `Model.pbip`). Saving into a folder that already holds a project adds only the files that are missing and leaves everything already there - the report's pages, theme, connection, and item identity - exactly as it was, so a save that changes nothing leaves the project unchanged under source control.

Validation guards saving: a model with a name collision Analysis Services would refuse (`TE0012` / `TE0013`, see [validate](#validate)) is not written unless `--force` or `--skip-validation` is passed.

> [!TIP]
> Use `te save-as -o <path> -s <workspace> -d <model>` to download a remote model to disk. Combínalo con `--skip-validation` para obtener el passthrough más rápido cuando solo necesites los bytes (sin análisis semántico de DAX).

### init

Crea un nuevo modelo semántico vacío en la ruta especificada. Defaults to a TMDL model in `PowerBI` compatibility mode at compatibility level 1705.

`te init` acepta:

- `<output-path>` - argumento posicional: directorio donde se creará el modelo (omítelo para usar la ruta global `--model`).
- `--compatibility-mode <mode>` - `PowerBI` (predeterminado) o `AnalysisServices`.
- `--compatibility-level <N>` (alias `--compat`) - nivel de compatibilidad. Defaults to `1705` when the mode is `PowerBI`, `1500` otherwise. Consulta @update-compatibility-level.
- `--name <name>` - nombre del modelo o de la base de datos (predeterminado: el nombre del directorio).
- `--serialization <fmt>` - `tmdl` (predeterminado), `bim` (alias `tmsl`), `Database.json`, `pbip`.
- `--force` - reemplaza cualquier archivo o directorio existente en la ruta de destino.

```bash
te init ./new-model                                       # TMDL, PowerBI mode, compat 1705
te init ./new-model --serialization bim                   # Single-file BIM model
te init ./as-model --compatibility-mode AnalysisServices  # AS model, compat 1500
te init ./existing-dir --force                            # Overwrite non-empty directory
```

`te init` is idempotent: re-running it over a model it already created prints `Already exists` and exits `0` (under `--output-format json`: `{"created": false, "reason": "already_exists", ...}`). Real conflicts still exit `1`; `--force` re-creates from scratch.

## Edición del modelo

Mutating commands (`set`, `add`, `remove`, `move`, and also `script`, `macro run`, `bpa run --fix`) are **dry runs by default**: without `--save` the command reports what would change and discards it (`Dry run - nothing saved. Add --save to persist.`). Add `--save` to persist to the source, or `--save-to <path>` to write elsewhere. On `set`, `add`, `remove`, `move`, `script`, and `bpa run`, the change output renders as a unified diff per changed object; switch it with `--stat` or `--name-only` (mutually exclusive with `--diff`, the default), or set a standing default with `te config set mutationOutput diff|stat|name-only|none`. JSON output always carries the full changes array. A save is refused when the mutation introduces new DAX validation errors, unless `--force`.

### set

Set properties on a model object, format its expressions, or sync a table with its source schema. Acepta un argumento `<path>`.

`te set` acepta:

- `-p, --property <Name=Value>` - property assignment (e.g., `-p expression="SUM(Sales[Amt])"`, `-p isHidden=true`). **Repeatable** - everything after the first `=` is the value. Bare positional assignments work too: `te set Sales/Amount formatString="#,0" --save`. Property names are case-insensitive, accept both spellings where the grid label and the TOM name differ (`Hidden` and `IsHidden`), and accept dotted paths and indexers: `-p KPI.StatusGraphic=...`, `-p "Annotations[Tabular Editor]=..."`, `-p "TranslatedNames[fr-FR]=..."`. Run `te get <path> --properties` to list every name an object accepts - see [get](#get). A partition's expression is `-p Expression` whatever kind of partition it is (`MExpression` and `Query` still work). Use `-p Name=-` to read the value from stdin (one assignment per stream; a piped value is taken verbatim, so piping the text `null` stores the word `null`). `-p Name=` assigns an empty string.
- `--unset <Name>` - clear a property; repeatable (`--unset description --unset displayFolder`). `-p Name=null` is the shorthand. Works on every property that can hold nothing - text properties included - and on object-valued ones (`SortByColumn`, `RefreshPolicy`); `-p "Annotations[key]=null"` removes an annotation. Numbers, booleans, and fixed-choice properties cannot be cleared and are refused.
- `--format <PropertyName>` - format that expression property (repeatable; DAX or M is detected from the property). The formatter tweaks `--long` (fewer line breaks) and `--no-space-after-function` require `--format` on a DAX property. `--semicolons` is refused together with `--format`: an expression stored in a model is always comma-separated, so the semicolon dialect can never parse it - format semicolon-authored DAX with [`te util format-dax --semicolons`](#util-format-dax) instead.
- `--update-schema` - sync a table's columns with its source schema: adds new source columns with detected types, retypes drifted ones, and preserves everything else about every existing column (name, description, format string, display folder, sort-by column, visibility, annotations, translations, perspective membership). Removed source columns only warn unless `--drop-removed-columns` (destructive). A renamed source column looks like remove + add - remap it first with `-p SourceColumn=<newName>`. Refused on calculated tables and calculation groups; cannot combine with `-p` or `--format`. With no connection flags, the connection is read from the model itself - the data source the table's partitions are bound to, the connection written into the table's own query, or the model's single usable data source - and the source table from the partition's binding, falling back to the model table's name; `--data-source <name>` chooses when the model has several usable sources. Naming a connection explicitly with the schema-detection flags shared with `te add` (`--source sql|lakehouse|warehouse`, `--endpoint`, `--connection-string`, `--source-database`, `--source-table`) always wins. When no source can be worked out, or the source table cannot be found, the error says which case you are in and names the table it looked for.
- `-t, --type <kind>` - desambiguación cuando la misma ruta podría referirse a varios tipos de objeto (`medida`, `Column`, `CalculatedColumn`, `Hierarchy`, `Calendar`, `partición`, `CalculationItem`).
- `--save` / `--save-to <path>` - guarda los cambios.
- `--diff` / `--stat` / `--name-only` - change-output rendering (see the note above).
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

#### Incremental refresh policies

Refresh policies are plain properties on a table's `RefreshPolicy` sub-object, so `te get` and `te set` manage them like anything else. Property names: `Mode`, `RollingWindowPeriods`/`RollingWindowGranularity`, `IncrementalPeriods`/`IncrementalGranularity`, `IncrementalPeriodsOffset`, `SourceExpression`, `PollingExpression` (file input: `-p SourceExpression=- < src.m`).

```bash
te get Sales/RefreshPolicy                                              # Inspect a table's refresh policy
te set Sales/RefreshPolicy -p RollingWindowPeriods=5 -p RollingWindowGranularity=Day -p IncrementalPeriods=1 -p IncrementalGranularity=Day --save
te set Sales -p RefreshPolicy=null --save                               # Remove the policy
```

The policy is created implicitly on the first `set`. Removing one leaves policy-generated partitions in place, and is refused when they are the table's only partitions. To apply a policy on the server, see [`te refresh --apply-refresh-policy`](#refresh); to apply it metadata-only, use `te script --inline "Model.Tables[\"Sales\"].ApplyRefreshPolicy();" --save`.

### add

Agrega un objeto al modelo. Especifica un `<path>` para el nuevo objeto (el elemento padre ya debe existir; el segmento final es el nuevo nombre) y el tipo mediante `-t` / `--type`. Las relaciones mantienen su sintaxis abreviada (`Sales[Key]->Dim[Key]`). Container-form paths are valid add targets (`Sales/Measures/Margin`, `Sales/Partitions/Q1`, `Sales/Calendars/Fiscal`, `Roles/Admin/TablePermissions/Sales`, `Roles/Admin/Members/user@x.com`) - any path the CLI prints can be fed back to `te add`.

`te add` acepta:

- `-t, --type <type>`: tipo de objeto. Common values: `Table`, `CalculatedTable`, `CalcGroup`, `Measure`, `CalculatedColumn`, `DataColumn`, `Hierarchy`, `Level`, `Calendar`, `CalcItem`, `KPI`, `Partition`, `Expression`, `Function`, `Perspective`, `Culture`, `Role`, `TablePermission`, `Member`. Se admite el autocompletado con la tecla Tab; la lista completa se puede obtener ejecutando `te add --help`.
- `-p, --property <Name=Value>` - property assignment on the new object (repeatable). The expression goes in `-p Expression="..."`, or use `--file`, or `-p Expression=-` to read it from stdin.
- `--file <path>` - read the expression from a file instead of inline.
- `--mode <mode>` - storage mode for new tables: `import` (default), `directquery` (alias `dq`), `dual`, `directlake` (alias `dl`).
- `--if-not-exists` - sale con código `0` sin error si el objeto ya existe. Úsalo en canalizaciones de CI/CD idempotentes.
- `--save` / `--save-to <path>` - guarda los cambios.
- `--diff` / `--stat` / `--name-only` - change-output rendering (see the [Model editing](#model-editing) note).
- `--serialization <fmt>` - override the serialization when saving (`tmdl`, `bim` (alias `tmsl`), `database.json`, `pbip`).
- `--source-type <kind>` - tipo de origen inicial de la partición en una tabla nueva: `m`, `query` o `calculated`. Anula la detección heurística. `query` builds a legacy SQL `SELECT` partition bound to the model's provider data source and is refused with lakehouse/warehouse sources or when no provider source exists; `calculated` is only valid with `-t CalculatedTable`.
- `--partition-expression <m>` - raw M expression for the new table's initial partition.
- `--force` - guarda incluso si la modificación introduce errores de validación de DAX.

Adding a single data column to an existing table takes `-t DataColumn` with both `SourceColumn` and `DataType` required (refused on calculated tables and calculation groups):

```bash
te add Sales/Quantity -t DataColumn -p SourceColumn=Qty -p DataType=Int64 --save
```

Tables can be created in one shot from the model's **own** data source - no connection flags needed. The CLI reads the connection off the model's data source, discovers the source table's columns and their types, and creates the table with a partition already bound to that source. Over a legacy (provider) data source the partition is a legacy SQL query holding the generated `SELECT`, matching what the desktop **Import Tables** wizard writes; pass `--source-type m` for a Power Query (M) partition instead. Over a structured (Power Query) data source the partition is always M. Refusals are clean and create nothing: several usable data sources and no `--data-source`, no data source the CLI can read (SQL Server, Azure SQL, and Fabric SQL sources are covered), a source whose password the model does not store, or a source table the connection cannot find - the error names the table it looked for and where that name came from.

- `--source-table <schema.table>` - create the table from this source table.
- `--query "SELECT ..."` - create the table from a query instead: the query is described against the connection without being run, the new table gets exactly the columns it returns, and the query is kept as the partition's content. Works with an inferred connection and with one named explicitly. `--source-type query` places the SQL in a legacy Query partition bound to the model's legacy data source. Refused together with `--mode directlake` (a Direct Lake partition holds no query), with `--columns`, and with an expression of its own (`-p Expression=` or `--file`).
- `--data-source "<name>"` - disambiguate when the model has several data sources.

Schema detection against an explicit source also works, and always wins over inference: `--source sql|lakehouse|warehouse`, `--endpoint`, `--connection-string`, `--source-database`, `--source-table`, or a manual column spec `--columns "Id:Int64,Name:String"`. `te add "<table>" -t Table` with no source at all still creates an empty table to fill in yourself.

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
- `--diff` / `--stat` / `--name-only` - change-output rendering (see the [Model editing](#model-editing) note).
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
- `--diff` / `--stat` / `--name-only` - change-output rendering (see the [Model editing](#model-editing) note).
- `--serialization <fmt>` - sobrescribe la serialización al guardar (`tmdl`, `bim` (alias `tmsl`), `database.json`).
- `--force` - guarda incluso si la mutación introduce errores de validación de DAX.

Renaming an object whose name is not yours to set is refused with a non-zero exit code rather than reported as `No changes.` - a relationship (its name always describes the columns it joins), a measure's KPI, a role's table permission.

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

- `--type <kind>` - narrow to one object kind (`table`, `measure`, `column`, `hierarchy`, `partition`, `relationship`, `role`, `perspective`, `culture`, `calculationitem`, `kpi`, `set`, `function`). Sin `<path-filter>`, esto equivale a escribir la palabra clave del contenedor correspondiente.
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

In JSON output, every listed object leads with its `objectPath` - a canonical path that resolves with `te get`.

### get

Get properties of a model object, filter and list sets of objects, and analyze dependencies - `get` is the CLI's one read pipeline (`te list` and `te deps` remain as shortcuts). Takes a `<path>`; omit it to list the model (same as `te list`), or pass `.` for the model root. A wildcard path (`te get "Sa*"`) or a container path (`te get Sales/Measures`) lists every match without needing `--ls`; `-p`, `--deps`, and `--properties` need exactly one object, so on a wildcard path they say so and suggest dropping the flag.

`te get` acepta:

- `-p, --property <property>` - project a single property (e.g. `expression`, `formatString`).
- `--where <Prop=Value>` - filter the result set; repeatable (AND), case-insensitive. A value with no `*` is an exact match; `*` is a wildcard, so a contains-search is `--where Name=*margin*`. With no path, `--where` filters the model's **top-level tables** - pass a container to search other kinds (`te get Measures --where Name=*margin*`). An empty result names what was searched and how the pattern was matched, and offers commands that widen the search.
- `--properties` - list the property names `-p` accepts on the resolved object, with each property's type, whether it can be written, what it holds, and - where a property takes a fixed set of values - the values it accepts. Both spellings are shown where they differ (`Hidden` / `IsHidden`), and annotations and translations appear in the bracket form they have to be written in. Internal bookkeeping properties are left out; `--all` adds them. Text and JSON output only; needs a single-object path and cannot combine with `-p`, `--ls`, `--where`, `--deps`, or `--unused`.
- `--ls` - compact table layout (the same rendering as `te list`).
- `--deps [upstream|downstream]` - dependency analysis (default: both directions); `--deep` for the recursive tree, `--max-depth <N>` (default `10`).
- `--unused` / `--hidden` - surface unused objects, as on `te deps`.
- `--paths-only` - one canonical object path per line, for piping.
- `--no-multiline` - collapse multi-line cells (with `--ls`/`--where`). Solo para la salida de texto.
- `-t, --type <kind>` - desambigua cuando la ruta coincide con varios elementos secundarios de una tabla (p. ej., una columna y una jerarquía con el mismo nombre). Valores: `Measure`, `Column`, `CalculatedColumn`, `Hierarchy`, `Calendar`, `Partition`, `CalculationItem`.
- `--output-format tmsl` (alias `bim`) - genera el objeto resuelto como JSON TMSL/BIM.
- `--output-format tmdl` - genera el objeto resuelto como TMDL (solo objetos con nombre).

`te get` y `te list` comparten un único catálogo de descriptores, de modo que todas las propiedades se muestran igual en todos los formatos: la tabla de texto, JSON y CSV ven el mismo conjunto, y al agregar una propiedad nueva al modelo, esta queda expuesta en todos ellos.

The `Settable:` line under a `te get <path>` result lists the properties `te set` accepts on that object (`SortByColumn` among them) and ends with a pointer to `--properties` for the full list; an unknown property name on `te get -p` or `te set -p` points at the same listing. `te get -p` syntax-highlights every expression-valued property, detail rows and format string expressions included. In JSON output, a single object leads with `objectPath` (the canonical path, resolvable as-is by `te get`, `te set`, or `te remove`), followed by `type` and `properties`; a listing that matches nothing prints an empty array.

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

Search string properties for text and report each match site. The pattern is a **literal, case-insensitive substring** by default - `te find "Gross*"` looks for a literal asterisk - so pass `--regex` for pattern matching. Use `te get --where Name=*Gross*` when you want to filter objects by a property value rather than search text. An empty result names the scope that was searched and the matching mode used, and offers commands that widen the search; a `--regex` pattern that is not a valid regular expression is refused with an error naming the flag and the pattern.

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

Under `--output-format json`, `te find` reports the scope it searched and the matching mode it used alongside the matches.

### diff

Compara dos modelos para detectar diferencias estructurales. Devuelve los siguientes códigos de salida: `0` = idéntico, `1` = diferencias encontradas, `2` = error.

Changes are reported the same way the mutating commands report theirs: one consolidated entry per changed object, with `-`/`+` lines per property in text output. In JSON, the `changes` array entries carry `objectPath` (the canonical path, pipeable into `te get`), `objectType` (the same closed vocabulary as the findings JSON - `KPI`, `Member`, ...), `changeKind` (`created`, `deleted`, `modified`, or `moved` - a renamed object that carries a lineage tag is a single `moved` entry with `movedFromObjectPath`), and a `properties` array of `{property, before, after}` with PascalCase property names. An object that exists in only one of the two models is listed together with its contents - a new role's row-level security filters, a new table's columns, measures, and partitions, a new hierarchy's levels - each as its own entry, and the summary counts include them.

```bash
te diff ./model-v1 ./model-v2
te diff old.bim new.bim

# Branch on exit code (POSIX sh):
te diff ./a ./b; case $? in 0) echo same;; 1) echo different;; *) echo error;; esac

# Branch on exit code (PowerShell):
te diff ./a ./b; switch ($LASTEXITCODE) { 0 { 'same' } 1 { 'different' } default { 'error' } }
```

### deps

Analiza las dependencias ascendentes y descendentes de un objeto, o detecta objetos sin usar en todo el modelo. A shortcut for `te get --deps` / `te get --unused`. La forma de un solo objeto acepta un `<path>`.

`te deps` admite:

- `--upstream` - muestra solo las dependencias ascendentes (lo que usa este objeto).
- `--downstream` - muestra solo las dependencias descendentes (los objetos que usan este objeto).
- `--deep` - muestra el árbol de dependencias recursivo en lugar de solo las dependencias directas.
- `--max-depth <N>` - profundidad máxima para el recorrido de `--deep` (predeterminado: `10`).
- `-t, --type <kind>` - desambigua cuando la ruta coincide con varios elementos secundarios de una tabla (p. ej., una columna y una jerarquía con el mismo nombre).
- `--unused` - enumera las medidas, las columnas calculadas y **todas las columnas de datos** a las que no hace referencia ninguna expresión DAX y que no se usan en ninguna relación, nivel de jerarquía, ordenación por columna, variación, base de AlternateOf ni rol de tiempo de calendario. Cada resultado muestra `(hidden)` en modo de texto y un campo `isHidden` en JSON.
- `--hidden` - limita `--unused` a solo los objetos ocultos. Los objetos ocultos y sin usar son los candidatos más seguros para eliminar, porque ningún elemento visible para el usuario depende de ellos.

In JSON output, every entry - and every `upstream`, `downstream`, and `--deep` tree node - is named the way the rest of the CLI names objects: `objectPath` (canonical path, pipeable into `te get`), `object` (bare name), and `objectType`.

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

- `--ci <fmt>` - emit CI annotations to stderr: `vsts` (aliases `azdo`, `azure-devops`) or `github` (alias `gh`). `none` or an empty value means no annotations; any other value is rejected before the command runs.
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

Every finding carries a stable code, shown in the **Code** column of the Errors, Warnings, and Anti-patterns tables as well as in JSON, `--ci` annotations, and `--trx`. Three codes are worth knowing when a hand-written model is involved: `TE0012` (a column and a measure, or two columns, share a name within one table) and `TE0013` (a measure name is repeated across tables) are errors - Analysis Services refuses to load such a model, and `te save-as` refuses to write one unless `--force` or `--skip-validation` is passed; `TE0014` is a warning that a TMDL folder has no `database.tmdl`, so the compatibility level in effect is a substitute for the one the model declared. The folder still loads and `te validate` still exits `0` for `TE0014`; hide it like any other warning with `--no-warnings` or `--errors-only`.

Under `--output-format json`, `te validate` emits the shared findings JSON document (`summary` plus a flat `findings[]` array) shared with `te bpa run`, `te test run`, and `te query` - see @te-cli-findings.

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
- `--diff` / `--stat` / `--name-only` - change-output rendering for the fix pass (see the [Model editing](#model-editing) note).
- `--serialization <fmt>` - serialización del modelo: `tmdl`, `bim` (alias `tmsl`), `database.json`.
- `--fail-on <severity>` - umbral de fallo: `error` (predeterminado) o `warning`. Sale con el código `1` cuando las infracciones alcanzan el umbral. Los errores al cargar o evaluar reglas (expresiones no válidas, archivos de reglas ilegibles) también provocan un código de salida distinto de cero, independientemente de `--fail-on`.
- `--ci <fmt>` - emit CI logging commands to stderr: `vsts` (Azure DevOps; aliases `azdo`, `azure-devops`), `github` (GitHub Actions; alias `gh`). Unrecognised values are rejected up front.
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

Under `--output-format json`, `te bpa run` emits the shared findings JSON document (see @te-cli-findings); with `--fix`, the JSON is a single document that also includes the `fix` change set.

#### Orígenes de las reglas y su resolución

Cada invocación de `te bpa run` reúne reglas de tres capas independientes:

1. **Reglas de usuario** - se aplica exactamente un origen, en este orden de prioridad:
   - `-r, --rules <rules>`: acepta una PATH de archivo o una URL (prioridad más alta)
   - La variable de entorno `TE_BPA_RULES`
   - la matriz `bpa.rules` de la configuración de la CLI (`~/.config/te/config.json`)
2. **Reglas integradas predeterminadas** - se cargan a menos que se pase `--no-defaults` o que [`bpa.builtInRules`](xref:te-cli-config#built-in-bpa-rules) sea `false` en la configuración. Se omiten las reglas integradas individuales incluidas en `bpa.disabledBuiltInRuleIds`.
3. **Reglas integradas en el modelo** - reglas en la anotación `BestPracticeAnalyzer_Rules` del modelo; se cargan a menos que se pase `--no-model-rules`. Se omiten las anotaciones de URL externas, a menos que también pases `--allow-external-rules`.

The built-in defaults are exactly Tabular Editor 3's documented [built-in rule set](xref:built-in-bpa-rules) (the `TE3_BUILT_IN_*` IDs), so `te bpa run` and TE3 Desktop agree on what the built-ins flag. The six VertiPaq Analyzer rules (`VPA_*`) that earlier previews presented as built-in are not part of that set, and the `--vpa-rules` flag no longer exists; if a pipeline gates on one of them, copy its definition into your own rules file and point at it with `--rules`, `bpa.rules`, or `TE_BPA_RULES`. `--vpax` is unchanged and still supplies the statistics a VPA-aware rule of your own reads. C# scripts (`te script`, `te macro run`) see the same rule set through `Bpa.Rules` and `Bpa.Analyze()`.

Each rule ID is evaluated once. When the same ID appears in more than one layer, an explicit `--rules` file's definition wins in `te bpa run`, while the built-in definition wins in the deploy/save gates. Después se eliminan los ID de reglas de la anotación `BestPracticeAnalyzer_IgnoreRules` del modelo.

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
- `te bpa rules set <id>` - actualiza las propiedades de una regla existente. Uses `-p, --property <name=value>` (repeatable; `-` reads the value from stdin). Nombres de propiedades: `name`, `expression`, `scope`, `category`, `severity`, `description`, `fixExpression`.
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

### Formatting expressions

Expression formatting lives in three places, depending on what you are formatting:

- **An expression in the model**: `te set <path> --format <PropertyName> --save` - see [set](#set).
- **A loose expression** (not in any model): `te util format-dax` / `te util format-m` - see [Utilities](#utilities).
- **A whole-model sweep**: `te script --inline "Model.AllMeasures.FormatDax();" --save`.

DAX in a model is always comma-separated, so `--semicolons` exists only on `te util format-dax`, for DAX you have typed with semicolons yourself.

## Ejecución

### query

Ejecuta una consulta DAX contra un modelo implementado.

`te query` admite:

- `<dax>` - argumento posicional: la consulta DAX que se va a ejecutar. Equivale a pasar `-q`. Utiliza la forma que se lea mejor; el `-q` explícito tiene prioridad si se proporcionan ambas.
- `-q, --query <dax>` - consulta en línea (variante con opción con nombre del argumento posicional anterior). `-q -` reads the query from stdin; with input piped and no query given at all, stdin is read implicitly.
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

- `--file <path>` - `.cs` / `.csx` file (repeatable). Bare positional `.cs`/`.csx` arguments are also accepted.
- `--inline <code>` - inline C# (repeatable; use `-` for stdin).
- `--validate` - compile the script(s) and report errors without executing them. Needs no model at all, so it works offline as a CI lint.
- `--save` / `--save-to` / `--serialization`.
- `--diff` / `--stat` / `--name-only` - change-output rendering (see the [Model editing](#model-editing) note).
- `--force` - save even if the mutation introduces DAX validation errors.

Files and inline snippets run in the order they are written on the command line.

```bash
te script --file fix.cs --save
te script fix.cs cleanup.csx --save              # Bare positionals, run in order
te script --inline "Info(Model.Tables.Count);"
echo "Info(Model.Name);" | te script --inline -
te script --file fix.cs --validate               # Compile-only, no model needed
```

A run in which any script calls `Error(...)` exits non-zero, reports `"success": false` in JSON, and closes by saying the run completed with errors; changes the script already made are still saved when `--save` is given. `Warning(...)` and `Info(...)` never fail a run. On Windows, the `DisableCSharpScripts` administrator policy refuses `te script` outright - see [Administrator policies](xref:te-cli-config#administrator-policies).

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

Administra y ejecuta macros desde un archivo JSON de macros (normalmente `MacroActions.json`). El archivo de macros se determina en este orden: `--macros <PATH>` → la variable de entorno `TE_MACROS_PATH` → `macros` en la configuración de la CLI → `./MacroActions.json`. On Windows, the `DisableMacros` administrator policy refuses every `te macro` command - see [Administrator policies](xref:te-cli-config#administrator-policies).

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
- `te macro set <name-or-id>`: actualiza las propiedades de la macro. Use `-p, --property <name=value>` (repeatable; `-` reads the value from stdin). Nombres de las propiedades: `name`, `execute`, `enabled`, `tooltip`, `validContexts`.
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
- `--save` / `--save-to` - guarda cualquier cambio que realice la macro. Like every mutating command, `te macro run` is a dry run without `--save`.
- `--serialization <fmt>` / `--force` - as on the other mutating commands.

```bash
te macro run "Hide all measures"
te macro run "Format DAX" --on Sales/Revenue --save
te macro run "Format DAX" --on "'Net Sales'[Sales Amount]" --save   # DAX form works in --on too
```

## Implementación y actualización

### deploy

Implementa un modelo semántico en Power BI, Fabric, Azure Analysis Services o en SQL Server Analysis Services en local.

**Dry run by default**: `te deploy` connects read-only and prints the exact TMSL it would send to stdout. Add `--execute` to actually deploy.

`te deploy` acepta:

- `-s, --server` / `-d, --database` - the model **source**, exactly as on every other command.
- `--target-server <target>` / `--target-database <name>` - the deploy **destination**: a workspace name, endpoint, or server, and the semantic model name to create or overwrite. Un nombre de servidor, FQDN, dirección IP o una cadena de conexión de MSOLAP implementa en Analysis Services (autenticación integrada de Windows para entornos locales); un nombre de Workspace o una URL `powerbi://...` implementa en Power BI. For local model sources, the target falls back to the active `te connect` connection; when the source is remote, the target flags are required. Deploying a model onto itself is refused.
- `--execute` - actually deploy. In interactive mode this shows a summary + confirmation prompt with **`n` as the safe default**; `--execute --force` skips the prompt (required in CI, where a prompt without `--force` is an error).
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
- `--force` - skip the interactive confirmation.
- `--ci <fmt>` - `vsts` (aliases `azdo`, `azure-devops`) or `github` (alias `gh`); unrecognised values are rejected up front.
- `-p, --profile <name>` - uso puntual de un perfil de @te-cli-auth guardado.

`--output-format bim|tmdl` is rejected on deploy. To capture the deployment script for review, redirect the dry-run output: `te deploy ... > deploy.tmsl`.

```bash
te deploy -m ./model --target-server my-workspace --target-database my-model --execute --force --ci github
te deploy -m ./model --target-server MY.SERVER.COM --target-database my-model --execute --force    # On-prem SSAS
te deploy -m ./model --target-server my-workspace --target-database my-model > deploy.tmsl         # Dry run: TMSL only
te deploy -s src-workspace -d src-model --target-server dst-workspace --target-database copy --execute   # Remote to remote
te deploy --local --target-server my-workspace --target-database my-model --execute                # Publish a Desktop model
```

> [!IMPORTANT]
> `te deploy` ejecuta el Best Practice Analyzer como control previo antes de realizar el despliegue. Consulta @te-cli-config para la configuración del control de BPA.

A deploy **fails** when the server reports errors on one or more objects, even though the metadata has been written: the exit code is non-zero, JSON reports `"success": false` with the reason in `error`, the headline says the deploy landed with errors, and `--ci` reports the object errors as errors. Unprocessed objects are not a failure - a metadata-only deploy legitimately leaves objects holding no data. The workspace mirror set up with `te connect -w` applies the same rule.

> [!NOTE]
> Cuando se establece `--output-format json`, la carga JSON de `te deploy` siempre incluye los valores resueltos de `server` y `database`, incluso cuando se han resuelto a partir de la conexión activa o de un perfil, en lugar de pasarse explícitamente. Las canalizaciones pueden usar estos campos para confirmar el destino del despliegue sin volver a analizar la línea de comandos. `te deploy` also exits non-zero on failure under `--output-format json`, matching its text-mode behavior - the JSON payload is the failure record, not a success signal.

### refresh

Inicia una actualización de datos en un modelo implementado.

**Dry run by default**: `te refresh` prints the TMSL a refresh would send to stdout. Add `--execute` to run it.

`te refresh` admite:

- `--type <type>` - `full`, `dataonly` (alias `data-only`, `data`), `automatic` (alias `auto`), `calculate` (alias `calc`), `clearvalues` (alias `clear`), `defragment` (alias `defrag`), `add` (predeterminado: `automatic`).
- `--table <name>` - actualiza tabla(s) específicas; se puede repetir.
- `--partition <Table.Partition>` - actualiza partición(es) específicas.
- `--execute` - actually run the refresh. At a terminal it asks for confirmation with **`n` as the safe default**; add `--force` to skip the question. An unattended run (redirected output, `--output-format json`, or `--non-interactive`) stops with an error unless `--force` is given, so `te refresh --type full --execute --force` is the CI form.
- `--force` - skip the confirmation prompt.
- `--apply-refresh-policy <true|false|table>` - apply incremental refresh policies to determine which partitions are refreshed; pass a table name to scope the refresh to that table. Policies apply by default when the refresh type and scope are compatible, except for models hosted in Power BI Desktop. An explicit value wins (with warnings when it cannot take effect).
- `--effective-date <yyyy-MM-dd>` - set the effective date used by the refresh policy (ignored, with a warning, when no policy applies).
- `--max-parallelism <N>` - establece el número máximo de particiones que se pueden actualizar en paralelo. Encapsula la actualización en un comando TMSL `sequence`.
- `--no-progress`, `--trace [path]`. `--trace` without `--execute` warns and prints the TMSL. Trace timing comes from the server's clock, the log is kept until the server has finished delivering buffered events, and `te-refresh-*` traces older than an hour that interrupted runs left behind are stopped and dropped at the start of a traced refresh (traces from other tools are never touched).

Executed refreshes under `--output-format json` always include a `progress` array; with the `vertipaqOnRefresh` config key enabled, a per-table `vertipaq` array (rows, size, columns) is included too - no `--trace` needed.

```bash
te refresh --type full --execute                        # Full refresh (asks for confirmation at a terminal)
te refresh --type full --execute --force                # Unattended: skip the confirmation
te refresh --table Sales --type full --execute          # Single table
te refresh --type full > refresh.tmsl                   # Dry run: emit TMSL only
te refresh --apply-refresh-policy Sales --execute       # Apply Sales' incremental refresh policy
```

Incremental refresh policies are authored with [`te set`](#incremental-refresh-policies) on a table's `RefreshPolicy` sub-object.

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

Suites are validated before any connection is made; a suite that fails validation (for example, a missing `query_file`) exits `1` without running anything. Under `--output-format json`, `te test run` emits the shared findings JSON document with test-specific extras (`suites`, `invalidSuites`, `testSummary`) - see @te-cli-findings.

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

`te connect --local` lists every local Analysis Services instance - Power BI Desktop (Store and installer versions), Visual Studio workspaces, and standalone SSAS - with a two-step prompt (instance, then database) when an instance hosts several databases. Non-interactive mode fails with the candidate list instead of picking silently; narrow it with `te connect --local <database>`.

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

View and manage CLI configuration. (`te config list`, alias: `ls`.) Consulta @te-cli-config.

`te config set` takes a positional `key value` pair or the equivalent `-p key=value`.

```bash
te config list                          # Display all settings
te config paths                         # Resolved macros and BPA rules file paths
te config init                          # Create default config
te config set autoFormat true
te config set -p spinner=false          # -p form
```

## Utilities

Model-free helpers. `te util` subcommands never touch a model - `--model`, `-s`/`-d`, `--local`, `--recent`, and `--auth` are rejected.

### util format-dax

Format a loose DAX expression.

- `<expression>` - the expression to format; `-` reads it from stdin.
- `--semicolons` - format DAX written with semicolons as list separators (European locale). The flag selects the semicolon dialect for the expression that is read as well as for the output, so it is for DAX you authored with semicolons - comma-separated DAX fails with a syntax error under it. It is accepted only here: `te set --format` refuses it, because an expression stored in a model is always comma-separated.
- `--long` - long format with fewer line breaks. De forma predeterminada se usa el formato corto.
- `--no-space-after-function` - omite el espacio después de los nombres de función.

```bash
te util format-dax "SUM ( Sales[Amount] )"
cat query.dax | te util format-dax -
te util format-dax "CALCULATE(SUM(Sales[Amt]); Sales[Region] = \"EU\")" --semicolons   # Semicolon-authored DAX
```

JSON output carries `success`, `formatted`, and `errors`. For expressions already in the model, use `te set <path> --format <PropertyName>` instead; for a whole-model sweep, `te script --inline "Model.AllMeasures.FormatDax();" --save`.

### util format-m

Format a loose M/Power Query expression. `-` reads from stdin; no language-specific options. A malformed expression - an unterminated string, for example - is reported as a failure with a non-zero exit code and the original text returned unchanged, never a silently shortened result.

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

Inside the session, mutating commands stage in memory: `save` (no arguments) commits the staged edits and `revert` discards them, while `save-as` re-serializes to a format or location. Closing a session that still holds staged edits asks for confirmation (or, when nobody can answer, warns and exits non-zero); `exit --force` throws them away deliberately - see @te-cli-interactive.

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

| Código de salida | Significado                                                                                                                                                                                                                                                                                                                                             |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `0`              | Éxito.                                                                                                                                                                                                                                                                                                                                  |
| `1`              | Generic failure (invalid arguments, command failed, validation errors, auth failure, BPA gate failed at severity >= error, a `te script` run in which a script reported an error, a `te deploy` the server accepted with object errors). Para `te diff`: se encontraron diferencias. |
| `2`              | Solo en `te diff`: se produjo un error durante la comparación, por lo que se desconoce el estado de las diferencias.                                                                                                                                                                                                    |

Para un control detallado en las canalizaciones de CI, combina los códigos de salida con las anotaciones `--ci <vsts/github>` y los archivos de resultados `--trx`; consulta @te-cli-cicd.

## Páginas relacionadas

- @te-cli - información general y contexto.
- @te-cli-install - instalación y configuración de la CLI.
- @te-cli-auth - autenticación y administración de conexiones.
- @te-cli-config - archivo de configuración, BPA gate y comportamiento tras la mutación.
- @te-cli-findings - the findings JSON shared by validate, bpa run, test run, and query.
- @te-cli-migrate - mapeo de opciones TE2 → TE3.
