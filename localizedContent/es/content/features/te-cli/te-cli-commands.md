---
uid: te-cli-commands
title: Referencia de comandos
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

- **`<path>`**: identifica **exactamente un** objeto o contenedor. Los utilizan los comandos que operan sobre un único destino: `te get`, `te set`, `te add`, `te remove`, `te move`, `te format -p`, `te deps`, `te macro run --on`.
- **`<path-filter>`**: identifica **cero o más** objetos y admite comodines. Los utilizan los comandos que operan sobre un conjunto: `te list`, `te bpa run --path` y otros comandos de inspección.

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
| `Tables`, `Medidas`, `Columns`, `Hierarchies`, `Particiones`                                                                     | Modelo    | Todos los objetos de ese tipo en todo el modelo. |
| `Relaciones`, `Roles`, `Perspectives`, `Cultures`, `DataSources`, `Expressions`, `CalculationGroups`, `Functions`, `Annotations` | Modelo    | Contenedores a nivel de modelo.                  |
| `Medidas`, `Columns`, `Hierarchies`, `Particiones`, `Calendars`, `CalculationItems`                                              | Tabla     | Subcontenedores dentro de una tabla.             |
| `Levels`                                                                                                                         | Jerarquía | Niveles de una jerarquía.                        |
| `Members`, `TablePermissions` (alias `Permissions`)                                                           | Rol       | Elementos hijos de un rol.                       |

Algunos ejemplos muestran en qué se diferencian las rutas simples y las rutas con ámbito de contenedor:

```bash
te get Sales/Revenue                       # Measure or column on Sales
te get Sales/Measures/Revenue              # Same, container-scoped - disambiguates if other kinds share the name
te get Sales/Geography/Levels/Year         # Specific level of a hierarchy
te get Roles/Admin/Members/bob@example.com # Role member
te get Sales/refreshPolicy                 # Refresh-policy sub-object on a table
te get "Measures/Revenue/KPI"              # KPI sub-object of a measure
```

Pon un segmento entre comillas para forzar la coincidencia literal del nombre cuando el nombre real de un objeto coincide con una palabra clave. La tabla cuyo nombre literal es `Tables` es `'Tables'` y se accede con `te get "'Tables'"`.

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

Los segmentos mal escritos generan un error contextual con una sugerencia de "quizás quisiste decir" cuando la CLI puede deducir lo que querías decir. Las rutas a las que les falta el elemento padre fallan antes de la comprobación del elemento hoja, así que los mensajes señalan el segmento que realmente está mal. Los contenedores vacíos (por ejemplo, `te list Hierarchies` en un modelo sin jerarquías) devuelven una sencilla indicación de "no hay nada aquí" en lugar de un error.

## Alias de comandos

La mayoría de los verbos en formato largo también aceptan un alias corto. Cada fila muestra el comando canónico y el comando equivalente en formato corto que admite como alias.

| Canónico                        | Forma(s) con alias |
| ------------------------------- | ------------------------------------- |
| `te list`                       | `te ls`                               |
| `te remove`                     | `te rm`                               |
| `te move`                       | `te mv`, `te rename`                  |
| `te bpa rules list`             | `te bpa rules ls`                     |
| `te bpa rules remove`           | `te bpa rules rm`                     |
| `te config list`                | `te config ls`                        |
| `te macro list`                 | `te macro ls`                         |
| `te macro remove`               | `te macro rm`                         |
| `te incremental-refresh remove` | `te incremental-refresh rm`           |
| `te profile list`               | `te profile ls`                       |
| `te profile remove`             | `te profile rm`                       |
| `te session list`               | `te session ls`                       |
| `te test list`                  | `te test ls`                          |

## Opciones globales

Estas opciones están disponibles en todos los comandos y se pueden usar antes o después del nombre del subcomando.

| Opción                     | Descripción                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `-m, --model <path>`       | Ruta al modelo semántico (carpeta TMDL, archivo `.bim`, carpeta `Database.json` o carpeta `.SemanticModel`).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `-s, --server <endpoint>`  | Analysis Services endpoint or Power BI workspace. A server name/FQDN (`MY.SERVER.COM`), IP address (`192.168.1.1`), `host:port`, `localhost`, `SERVER\INSTANCE`, `asazure://...`, or an MSOLAP connection string connects directly to Analysis Services / AAS. A bare single-token name (`MyWorkspace`), a Fabric `Name.Workspace[/Model.SemanticModel]` path, or a `powerbi://...` URL targets a Power BI workspace. A workspace name containing a dot is indistinguishable from a server name, so it is treated as a server and the CLI prints a warning; use its `.Workspace` form or full `powerbi://` URL to target Power BI. |
| `-d, --database <name>`    | Nombre del modelo semántico en el Workspace.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `--local`                  | Conecta a una instancia de Power BI Desktop en ejecución local (solo Windows).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `--auth <method>`          | Método de autenticación: `auto`, `interactive`, `spn`, `env`, `managed-identity` (predeterminado: `auto`).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `--output-format <format>` | Formato de Stdout: `text` (predeterminado), `json`, `csv`, `tmsl` (alias `bim`), `tmdl`. `csv` se respeta en los comandos que emiten datos tabulares; `tmsl`/`tmdl` solo se respetan en `te get` y `te list` para la serialización de objetos completos. Los comandos rechazan los formatos que no admiten.                                                                                                                                                                                                                                                                                                                                            |
| `--error-format <format>`  | Formato de stderr para errores, advertencias y sugerencias: `text` (predeterminado) o `json`. Para cualquier otro valor, se usa `text`. Es independiente de `--output-format`, así que puedes combinar stdout en JSON con errores en texto sin formato (o viceversa).                                                                                                                                                                                                                                                                                                                                                                                  |
| `--recent [N]`             | Usa un modelo que hayas usado recientemente. Sin valor = selector interactivo; `N` = el N-ésimo más reciente (1 = el último usado).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `--non-interactive`        | Desactiva todas las indicaciones interactivas. Finaliza con un error accionable si falta algún dato obligatorio.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `--debug`                  | Habilita el registro de depuración en stderr (cadenas de conexión, flujo de autenticación, tiempos).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

`te --version` muestra la versión de la CLI y sale.

En los comandos que leen un modelo, el orden de resolución es:

el argumento posicional `<model>` → la opción global `--model` → `--server`/`--database` (remoto) → conexión activa de `te connect` → `--recent`.

> [!NOTE]
> **Las opciones mal escritas se rechazan de entrada.** Si pasas un `--flag` que no se reconoce en el comando que invocaste, la CLI finaliza con un error claro en lugar de interpretarlo silenciosamente como un argumento posicional. Esto detecta errores tipográficos como, por ejemplo, que `--force ` se convierta accidentalmente en `--forec` en scripts de CI.

> [!NOTE]
> **Nombres de servidor con puntos.** `-s`/`--server` trata un nombre con puntos (por ejemplo, `Sales.2026`) como el nombre de host de un servidor de Analysis Services, no como un Workspace de Power BI. Se muestra una advertencia cuando la CLI tiene que hacer esta interpretación, con una sugerencia para agregar `.Workspace` (por ejemplo, `Sales.2026.Workspace`) o usar una URL `powerbi://` completa si en realidad te referías al Workspace de Power BI. Se aplica a `te connect`, `te deploy`, `te refresh`, `te query`, `te vertipaq` y `te test run`.

## E/S del modelo

### load

Carga un modelo semántico y muestra un resumen del modelo: nombre, nivel de compatibilidad y recuentos generales de objetos (tablas, medidas, columnas).

```bash
te load ./model                            # TMDL folder
te load model.bim                          # BIM file
te load -s MyWorkspace -d MyModel          # Remote workspace
```

### save

Guarda un modelo en disco. Úsalo para escribir en archivos locales un modelo de un Workspace remoto, convertir formatos o guardar de nuevo las ediciones en el origen.

`te save` acepta:

- `-o, --output-path <path>` - archivo o carpeta de destino. **Opcional** - si se omite, `te save` vuelve a escribir en la ubicación de origen y conserva el formato original. La extensión del archivo también sirve para inferir el formato: `.bim` escribe un BIM en un solo archivo, `.json` escribe una carpeta `Database.json` y una ruta sin extensión escribe una carpeta TMDL.
- `--serialization <fmt>` - `tmdl`, `bim` (alias `tmsl`), `Database.json`, `pbip`. Si se omite, el formato se infiere a partir de la extensión de la ruta `-o` (o del modelo cargado cuando `-o` se omite por completo).
- `--force` - omite la validación y sobrescribe la salida existente. Algunos rechazos (contenedores ambiguos, raíces de proyecto con varios `SemanticModel`) siguen ocurriendo incluso con `--force`.
- `--skip-bpa` - omite por completo el control de BPA.
- `--fix-bpa` - corrige automáticamente las infracciones de BPA cuando las reglas definen una expresión de corrección.
- `--bpa-rules <path>` - repetible; reemplaza `bpa.rules` de la configuración de la CLI solo en este guardado. Las reglas integradas siguen aplicándose a menos que `bpa.builtInRules` sea `false`.
- `--skip-validation` - omite el análisis semántico y la validación de DAX para descargas rápidas en modo passthrough.
- `--supporting-files` - genera archivos auxiliares de Fabric (`.platform`, `definition.pbism`).

```bash
te save                                    # Save back to source (no -o needed)
te save ./model.bim -o ./tmdl-out          # Convert BIM to TMDL
te save -o ./project --serialization pbip         # Save as a PBIP project
te save -o ./out -s my-workspace -d my-model --skip-validation   # Fast download
```

> [!TIP]
> Use `te save -o <path> -s <Workspace> -d <model>` para descargar un modelo remoto a disco. Combínalo con `--skip-validation` para obtener el passthrough más rápido cuando solo necesites los bytes (sin análisis semántico de DAX).

### open

Abre un modelo en la aplicación de escritorio de Tabular Editor 3. **Solo para Windows** (requiere que TE3 esté instalado). Sin argumentos, inicia TE3 con un Workspace en blanco.

```bash
te open                  # Launch TE3 with a blank workspace
te open ./my-model       # Open a TMDL folder in TE3
te open ./model.bim      # Open a BIM file in TE3
```

### init

Crea un nuevo modelo semántico vacío en la ruta especificada. De forma predeterminada, usa un modelo TMDL en modo de compatibilidad `PowerBI`, con nivel de compatibilidad 1702.

`te init` acepta:

- `<output-path>` - argumento posicional: directorio donde se creará el modelo (omítelo para usar la ruta global `--model`).
- `--compatibility-mode <mode>` - `PowerBI` (predeterminado) o `AnalysisServices`.
- `--compatibility-level <N>` (alias `--compat`) - nivel de compatibilidad. De forma predeterminada, usa `1702` cuando el modo es `PowerBI`; `1500` en caso contrario. Consulta @update-compatibility-level.
- `--name <name>` - nombre del modelo o de la base de datos (predeterminado: el nombre del directorio).
- `--serialization <fmt>` - `tmdl` (predeterminado), `bim` (alias `tmsl`), `Database.json`, `pbip`.
- `--force` - reemplaza cualquier archivo o directorio existente en la ruta de destino.

```bash
te init ./new-model                                       # TMDL, PowerBI mode, compat 1702
te init ./new-model --serialization bim                   # Single-file BIM model
te init ./as-model --compatibility-mode AnalysisServices  # AS model, compat 1500
te init ./existing-dir --force                            # Overwrite non-empty directory
```

## Edición del modelo

### set

Establece una propiedad en un objeto del modelo. Acepta un argumento `<path>`.

`te set` acepta:

- `-q <property>` - nombre de la propiedad (por ejemplo, `expression`, `formatString`, `description`, `isHidden`). **Se puede repetir** — empareja cada `-q` con el `-i` siguiente para establecer varias propiedades en un solo comando.
- `-i <value>` - valor (usa `-` para leer desde stdin). Un `-i` por cada `-q`.
- `-t, --type <kind>` - desambiguación cuando la misma ruta podría referirse a varios tipos de objeto (`medida`, `Column`, `CalculatedColumn`, `Hierarchy`, `Calendar`, `partición`, `CalculationItem`).
- `--save` / `--save-to <path>` - guarda los cambios.
- `--serialization <fmt>` - sobrescribe la serialización al guardar (`tmdl`, `bim` (alias `tmsl`), `database.json`).
- `--force` - guarda incluso si la modificación introduce errores de validación de DAX.

```bash
te set Sales/Amount -q expression -i "SUM(Sales[Amt])" --save
te set "'Net Sales'[Sales Amount]" -q formatString -i "#,0" --save   # DAX form with spaced names
te set Sales -q isHidden -i true --save
te set Sales/Amount -q formatString -i "#,0" -q description -i "Net sales" --save   # Multi-property
```

### add

Agrega un objeto al modelo. Especifica un `<path>` para el nuevo objeto (el elemento padre ya debe existir; el segmento final es el nuevo nombre) y el tipo mediante `-t` / `--type`. Las relaciones mantienen su sintaxis abreviada (`Sales[Key]->Dim[Key]`).

`te add` acepta:

- `-t, --type <type>`: tipo de objeto. Valores comunes: `Table`, `Measure`, `Column`, `CalculatedColumn`, `Hierarchy`, `Role`, `Perspective`, `Culture`, `CalculationGroup`, `CalculationItem`. Se admite el autocompletado con la tecla Tab; la lista completa se puede obtener ejecutando `te add --help`.
- `-i <value>` - expresión o valor que se asignará al nuevo objeto (DAX para medidas/columnas calculadas, M para particiones, etc.). Combínalo con `-q` para establecer propiedades adicionales en el nuevo objeto en el mismo comando.
- `-q <property>` - propiedad adicional que se establecerá en el nuevo objeto (se puede repetir; se combina con `-i`).
- `--file <path>` - lee la expresión de `-i` desde un archivo en lugar de incluirla directamente en el comando.
- `--mode <mode>` - modo de almacenamiento para tablas nuevas: `import` (predeterminado), `directQuery`, `dual`, `directLake`.
- `--if-not-exists` - sale con código `0` sin error si el objeto ya existe. Úsalo en canalizaciones de CI/CD idempotentes.
- `--save` / `--save-to <path>` - guarda los cambios.
- `--serialization <fmt>` - sobrescribe la serialización al guardar (`tmdl`, `bim` (alias `tmsl`), `database.json`).
- `--source-type <kind>` - tipo de origen inicial de la partición en una tabla nueva: `m`, `query` o `calculated`. Anula la detección heurística. `calculated` solo es válido con `-t CalculatedTable`.
- `--force` - guarda incluso si la modificación introduce errores de validación de DAX.

```bash
te add Sales/Revenue -t Measure -i "SUM(Sales[Amount])" --save
te add Sales -t Table --save
te add "Sales[ProdKey]->Product[ProdKey]" --save                           # Relationship shorthand
te add Sales/MarketingFlag -t CalculatedColumn -i "Sales[Amount] > 1000" --if-not-exists --save
te add Perspectives/Default/Sales --save                                   # Include Sales in the Default perspective
te add Roles/Reader -t Role --save                                         # New role at the model level
```

En las tablas vinculadas a datos, `te add` también admite la detección del esquema desde orígenes SQL, Lakehouse o Warehouse. Consulta `te add --help` para ver `--source`, `--endpoint`, `--source-table`, `--columns`, etc.

### remove

Elimina un objeto. De forma predeterminada, comprueba las dependencias para evitar romper referencias existentes. (Alias: `rm`.)

`te remove` acepta:

- `<path>` - argumento posicional: el objeto que se va a eliminar.
- `-t, --type <kind>` - desambigua cuando la ruta coincide con varios elementos secundarios de una tabla (p. ej., una columna y una jerarquía con el mismo nombre).
- `--force` - omite la comprobación de objetos dependientes.
- `--if-exists` - sale con código `0` sin error si el objeto no existe. Úsalo en canalizaciones de CI/CD idempotentes.
- `--dry-run` - muestra una vista previa de la eliminación sin aplicarla.
- `--save` / `--save-to <path>` - guarda el cambio.
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
- `--serialization <fmt>` - sobrescribe la serialización al guardar (`tmdl`, `bim` (alias `tmsl`), `database.json`).
- `--force` - guarda incluso si la mutación introduce errores de validación de DAX.

```bash
te move Sales/Revenue Finance/Revenue --save                # Move measure to another table
te move Sales/Revenue Sales/TotalRevenue --save             # Rename measure
te move Sales/Date Sales/CalendarDate -t Hierarchy --save   # Disambiguate hierarchy from column
```

### replace

Busca y reemplaza texto en los objetos del modelo. Simulación de forma predeterminada; añade `--save` para aplicar.

`te replace` acepta:

- `--in <scope>` — ámbito: `names`, `expressions`, `descriptions`, `displayFolders`, `formatStrings`, `annotations`, `all` (predeterminado: `all`).
- `--regex` — trata el patrón de búsqueda como una expresión regular.
- `--case-sensitive` — habilita la coincidencia que distingue entre mayúsculas y minúsculas.
- `--dry-run` - previsualiza los cambios sin aplicarlos. Comportamiento predeterminado.
- `--save` - guarda la modificación en la ubicación de origen. Incompatible con `--revert` y `--stage`.
- `--save-to <path>` - guarda en una ruta diferente (implica `--save`).
- `--serialization <fmt>` - serialización del modelo: `tmdl`, `bim` (alias `tmsl`), `database.json`.
- `--force` - guarda incluso si la sustitución introduce errores de validación de DAX.

`--in expressions` recorre todas las propiedades que contienen expresiones:

- **Medida**: `Expression`, `DetailRowsExpression`
- **KPI**: `TargetExpression`, `StatusExpression`, `TrendExpression`
- **Partición**: M de origen y M de sondeo
- **Permiso de tabla**: `FilterExpression`
- **Grupo de cálculo**: expresiones de selección
- **Columna calculada**: expresión DAX

Al añadir al modelo nuevas propiedades basadas en expresiones, se muestran automáticamente.

```bash
te replace "OldTable" "NewTable" --in expressions --save
te replace "SUM" "SUMX" --regex --in expressions --save
```

## Inspección

### list

Enumera objetos con una navegación similar a la del sistema de archivos. Acepta un argumento `<path-filter>` que admite comodines. Se admiten tanto contenedores de nivel de modelo como contenedores con ámbito de tabla; consulta la [tabla de palabras clave de contenedores](#containers-and-keywords) anterior para ver la lista completa. (Alias: `ls`.)

`te list` acepta:

- `--type <kind>` - limita a un tipo de objeto (`table`, `measure`, `column`, `hierarchy`, `partition`, `relationship`, `role`, `perspective`, `culture`). Sin `<path-filter>`, esto equivale a escribir la palabra clave del contenedor correspondiente.
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
te list "'Net Sales'/'Sales Amount'"        # Quote names containing spaces
te list Measures --paths-only               # One Table/Measure per line for piping
te list --type measure                      # Same as `te list Measures`
te list Measures --no-multiline             # Wide table with column dividers, single-line DAX
te list Tables --output-format bim > tables.json   # All tables emitted as TMSL/BIM
```

### get

Obtiene las propiedades de un objeto del modelo. Acepta un `<path>`.

`te get` acepta:

- `-q, --query <property>` - obtiene una única propiedad (por ejemplo, `expression`, `formatString`).
- `-t, --type <kind>` - desambigua cuando la ruta coincide con varios elementos secundarios de una tabla (p. ej., una columna y una jerarquía con el mismo nombre). Valores: `Measure`, `Column`, `CalculatedColumn`, `Hierarchy`, `Calendar`, `Partition`, `CalculationItem`.
- `--output-format tmsl` (alias `bim`) - genera el objeto resuelto como JSON TMSL/BIM.
- `--output-format tmdl` - genera el objeto resuelto como TMDL (solo objetos con nombre).

`te get` y `te list` comparten un único catálogo de descriptores, de modo que todas las propiedades se muestran igual en todos los formatos: la tabla de texto, JSON y CSV ven el mismo conjunto, y al agregar una propiedad nueva al modelo, esta queda expuesta en todos ellos.

```bash
te get Sales/Amount -q expression                # Print DAX
te get "'Sales'[Amount]"                         # DAX form: same as Sales/Amount
te get "[Total Sales]"                           # Lone-bracket: model-wide measure-or-column
te get "'Net Sales'[Sales Amount]" -q expression # DAX form with spaced names
te get "Sales/Revenue/KPI"                       # KPI sub-object of a measure
te get Sales --output-format tmdl                       # Emit the table as TMDL
te get Sales --output-format bim                        # Emit the table as TMSL/BIM
te get Model -q description
```

### find

Busca texto en todos los objetos del modelo.

`te find` acepta:

- `--in <scope>` - igual que en `te replace` (valor predeterminado: `all`).
- `--regex`, `--case-sensitive`, `--paths-only`.
- `--no-multiline` - contrae el contexto de coincidencia multilínea a una sola línea. Solo para la salida de texto.

`--in expressions` abarca todos los `IExpressionObject` del modelo, incluidas las `TargetExpression` / `StatusExpression` / `TrendExpression` de los KPI, la `DetailRowsExpression` de la medida, el M de origen/sondeo de la partición, la `FilterExpression` de los permisos de tabla y las expresiones `MultipleOrEmptySelection` / `NoSelection` del grupo de cálculo; así, un literal como `123` definido en el objetivo de un KPI aparece igual que el cuerpo de una medida.

```bash
te find "CALCULATE" --in expressions
te find "Revenue" --in names
te find "CALCULATE" --in expressions --paths-only | xargs -I{} te get {} -q expression
```

### diff

Compara dos modelos para detectar diferencias estructurales. Devuelve los siguientes códigos de salida: `0` = idéntico, `1` = diferencias encontradas, `2` = error.

```bash
te diff ./model-v1 ./model-v2
te diff old.bim new.bim

# Branch on exit code (POSIX sh):
te diff ./a ./b; case $? in 0) echo same;; 1) echo different;; *) echo error;; esac

# Branch on exit code (PowerShell):
te diff ./a ./b; switch ($LASTEXITCODE) { 0 { 'same' } 1 { 'different' } default { 'error' } }
```

### deps

Analiza las dependencias ascendentes y descendentes de un objeto, o detecta objetos sin usar en todo el modelo. La forma de un solo objeto acepta un `<path>`.

`te deps` admite:

- `--upstream` - muestra solo las dependencias ascendentes (lo que usa este objeto).
- `--downstream` - muestra solo las dependencias descendentes (los objetos que usan este objeto).
- `--deep` - muestra el árbol de dependencias recursivo en lugar de solo las dependencias directas.
- `--max-depth <N>` - profundidad máxima para el recorrido de `--deep` (predeterminado: `10`).
- `-t, --type <kind>` - desambigua cuando la ruta coincide con varios elementos secundarios de una tabla (p. ej., una columna y una jerarquía con el mismo nombre).
- `--unused` - enumera las medidas, las columnas calculadas y **todas las columnas de datos** a las que no hace referencia ninguna expresión DAX y que no se usan en ninguna relación, nivel de jerarquía, ordenación por columna, variación, base de AlternateOf ni rol de tiempo de calendario. Cada resultado muestra `(hidden)` en modo de texto y un campo `isHidden` en JSON.
- `--hidden` - limita `--unused` a solo los objetos ocultos. Los objetos ocultos y sin usar son los candidatos más seguros para eliminar, porque ningún elemento visible para el usuario depende de ellos.

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

- `--ci <fmt>` - emite anotaciones de CI en stderr: `vsts` o `github`.
- `--trx <PATH>` - escribe los resultados en un archivo `.trx` de VSTEST.
- `--errors-only` - forma abreviada de `--no-warnings --no-antipatterns`: muestra solo errores.
- `--no-warnings` - oculta las advertencias del analizador semántico.
- `--no-antipatterns` - oculta las sugerencias de antipatrones (recomendaciones de buenas prácticas de DAX).
- `--server-only` - muestra solo los errores notificados por el servidor conectado; omite el análisis semántico local.
- `--no-multiline` - contrae el contenido de varias líneas de las celdas (mensajes de error, expresiones) en una sola línea. Solo salida de texto.

```bash
te validate ./model
te validate --ci github --trx results.trx
te validate --errors-only                 # Hide warnings and anti-pattern hints
```

> [!NOTE]
> `te validate` no admite `--output-format csv`: CSV se rechaza desde el principio con un error claro, en lugar de producir un resultado parcial. Usa `text` o `json` para la salida de validación.

### bpa run

Ejecuta reglas de Best Practice Analyzer contra un modelo.

`te bpa run` admite:

- `<model>` - argumento posicional: ruta al modelo (alternativa a la opción global `--model`).
- `-r, --rules <rules>` - ruta(s) o URL(s) a archivo(s) de reglas BPA en formato JSON. Se puede repetir. Sustituye la capa de reglas de usuario en esta invocación: consulta [Orígenes y resolución de reglas](#rule-sources-and-resolution) más abajo.
- `--no-model-rules` - excluye las reglas de BPA incrustadas en las anotaciones del modelo.
- `--no-defaults` - excluye las reglas predeterminadas de BPA integradas.
- `--vpax <file>` - carga estadísticas del Analizador VertiPaq desde un archivo `.vpax` para habilitar reglas compatibles con VPA.
- `--vpa-rules` - incluir reglas integradas compatibles con VPA (requiere `--vpax` o un modelo preanotado).
- `--allow-external-rules` - permitir obtener archivos de reglas de BPA desde direcciones URL incrustadas en las anotaciones del modelo.
- `--rule <id>` - ejecutar solo regla(s) específicas por ID. Se puede repetir.
- `--path <path-filter>` - limitar el análisis a las tablas que contengan los objetos coincidentes. Acepta nombres literales, palabras clave de contenedor y comodines (por ejemplo, `'Sales'`, `'Sa*'`, `'Sales/Medidas'`, `'*/Amount'`).
- `--fix` - aplicar expresiones de corrección para corregir automáticamente las infracciones cuando sea posible.
- `--save` - volver a guardar el modelo en el origen después de aplicar las correcciones.
- `--save-to <path>` - guardar el modelo en una ruta diferente después de aplicar las correcciones.
- `--serialization <fmt>` - serialización del modelo: `tmdl`, `bim` (alias `tmsl`), `database.json`.
- `--fail-on <severity>` - umbral de fallo: `error` (predeterminado) o `warning`. Sale con el código `1` cuando las infracciones alcanzan el umbral. Los errores al cargar o evaluar reglas (expresiones no válidas, archivos de reglas ilegibles) también provocan un código de salida distinto de cero, independientemente de `--fail-on`.
- `--ci <fmt>` - emitir comandos de registro de CI a stderr: `vsts` (Azure DevOps), `github` (GitHub Actions).
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

#### Orígenes de las reglas y su resolución

Cada invocación de `te bpa run` reúne reglas de tres capas independientes:

1. **Reglas de usuario** - se aplica exactamente un origen, en este orden de prioridad:
   - `-r, --rules <rules>`: acepta una PATH de archivo o una URL (prioridad más alta)
   - La variable de entorno `TE_BPA_RULES`
   - la matriz `bpa.rules` de la configuración de la CLI (`~/.config/te/config.json`)
2. **Reglas integradas predeterminadas** - se cargan a menos que se pase `--no-defaults` o que [`bpa.builtInRules`](xref:te-cli-config#built-in-bpa-rules) sea `false` en la configuración. Se omiten las reglas integradas individuales incluidas en `bpa.disabledBuiltInRuleIds`.
3. **Reglas integradas en el modelo** - reglas en la anotación `BestPracticeAnalyzer_Rules` del modelo; se cargan a menos que se pase `--no-model-rules`. Se omiten las anotaciones de URL externas, a menos que también pases `--allow-external-rules`.

Se eliminan los ID de reglas duplicados (las reglas del usuario prevalecen sobre las integradas). Después se eliminan los ID de reglas de la anotación `BestPracticeAnalyzer_IgnoreRules` del modelo.

La línea `Rules loaded:` de la salida atribuye cada capa que contribuye, por ejemplo:

```
Rules loaded: 41 from 1 file(s) from bpa.rules config + built-in defaults + model annotations
```

### bpa rules

Administra colecciones de reglas de BPA: enumera, inspecciona, inicializa y activa o desactiva reglas en tu archivo local de reglas o en las anotaciones del modelo. Las reglas integradas son de solo lectura; para omitir una sin perder el resto, usa `te bpa rules disable` (no edites directamente el conjunto integrado).

Subcomandos:

| Subcomando                                                 | Propósito                                                                                   |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `add <id> [model]`                                         | Agrega una nueva regla de BPA.                                              |
| [`disable`](#bpa-rules-disable)                            | Desactiva una regla de BPA integrada para el usuario actual.                |
| [`enable`](#bpa-rules-enable)                              | Vuelve a activar una regla de BPA integrada que se había desactivado antes. |
| `ignore <rule-id> [model]`                                 | Agrega una regla a la lista de ignorados del modelo.                        |
| [`init`](#bpa-rules-init)                                  | Crea un archivo vacío de reglas de BPA en la ruta PATH resuelta.            |
| [`list`](#bpa-rules-list) (alias `ls`)  | Enumera las reglas de BPA de todos los orígenes con su estado.              |
| `remove <rule-id> [model]` (alias `rm`) | Elimina una regla de BPA.                                                   |
| `set <rule-id> [model]`                                    | Actualiza las propiedades de una regla del BPA.                             |
| `unignore <rule-id> [model]`                               | Elimina una regla de la lista de reglas ignoradas del modelo.               |

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
- `te bpa rules set <id>` - actualiza las propiedades de una regla existente. Utiliza pares `-q <property> -i <value>` (repetibles). Nombres de propiedades: `name`, `expression`, `scope`, `category`, `severity`, `description`, `fixExpression`.
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
te bpa rules set MEASURE_NEEDS_DESCRIPTION -q severity -i 3

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

### format

Da formato a expresiones DAX o M/Power Query.

`te format` acepta:

- `-e, --expression <text>` - da formato a una sola expresión en línea.
- `-p, --path <path>` - da formato a una medida o columna específica mediante su ruta.
- `-t, --type <kind>` - desambigua cuando la ruta coincide con varios elementos secundarios de la tabla.
- `--lang <lang>` - lenguaje de expresión: `dax` (predeterminado) o `m`/`pq` para Power Query.
- `--semicolons` - usa el punto y coma como separador de listas (configuración regional europea).
- `--long` - usa el formato largo (más saltos de línea). De forma predeterminada se usa el formato corto.
- `--no-space-after-function` - omite el espacio después de los nombres de función.
- `--save` / `--save-to` - guarda las expresiones formateadas.

```bash
te format --save                                           # Format all DAX
te format -p Sales/Amount --save                           # Single measure
te format -e "SUM ( Sales[Amount] )"                       # Inline
te format --lang m --save                                  # Format M
```

## Ejecución

### query

Ejecuta una consulta DAX contra un modelo implementado.

`te query` admite:

- `<dax>` - argumento posicional: la consulta DAX que se va a ejecutar. Equivale a pasar `-q`. Utiliza la forma que se lea mejor; el `-q` explícito tiene prioridad si se proporcionan ambas.
- `-q, --query <dax>` - consulta en línea (variante con opción con nombre del argumento posicional anterior).
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

- `-S, --script <file>` - archivo `.cs` / `.csx` (repetible).
- `-e, --expression <code>` - C# en línea (usa `-` para stdin).
- `--save` / `--save-to` / `--serialization`.
- `--dry-run` - compila el/los script(s) y genera un Report de errores sin ejecutarlos.

```bash
te script --script fix.cs --save
te script -e "Info(Model.Tables.Count)"
echo "Info(Model.Name);" | te script -e -
```

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

Administra y ejecuta macros desde un archivo JSON de macros (normalmente `MacroActions.json`). El archivo de macros se determina en este orden: `--macros <PATH>` → la variable de entorno `TE_MACROS_PATH` → `macros` en la configuración de la CLI → `./MacroActions.json`.

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
- `te macro set <name-or-id>`: actualiza las propiedades de la macro. Usa pares `-q <property> -i <value>` (se pueden repetir). Nombres de las propiedades: `name`, `execute`, `enabled`, `tooltip`, `validContexts`.
- `te macro remove <name-or-id>`: elimina una macro.

```bash
te macro add MyMacro -e "Info(Selected.Measure.Name);" --tooltip "Print measure name" --contexts Measure
te macro set MyMacro -q tooltip -i "Updated tooltip"
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
- `--save` / `--save-to` - guarda cualquier cambio que realice la macro.

```bash
te macro run "Hide all measures"
te macro run "Format DAX" --on Sales/Revenue --save
te macro run "Format DAX" --on "'Net Sales'[Sales Amount]" --save   # DAX form works in --on too
```

## Implementación y actualización

### deploy

Deploy a semantic model to Power BI, Fabric, Azure Analysis Services, or on-prem SQL Server Analysis Services.

`te deploy` acepta:

- `-s, --server` / `-d, --database` - target server/workspace and model. A server name, FQDN, IP address, or MSOLAP connection string deploys to Analysis Services (Windows Integrated auth for on-prem); a workspace name or `powerbi://...` URL deploys to Power BI. See the [global options](#global-options) table for how `-s` is interpreted.
- `--deploy-full` - sobrescribir + conexiones + particiones + expresiones compartidas + roles + miembros de roles.
- `--deploy-connections`
- `--deploy-partitions`
- `--skip-refresh-policy`
- `--deploy-roles`
- `--deploy-role-members`
- `--deploy-shared-expressions`
- `--create-only`
- `--xmla <file>` - genera un script XMLA/TMSL en lugar de realizar el despliegue (`-` para stdout).
- `--skip-bpa` - omite por completo el control de BPA.
- `--fix-bpa` - corrige automáticamente las infracciones de BPA cuando las reglas definan una expresión de corrección.
- `--bpa-rules <PATH>` - se puede repetir; anula `bpa.rules` de la configuración de tu CLI solo para este despliegue. Las reglas integradas siguen aplicándose a menos que `bpa.builtInRules` sea `false`.
- `--force` - omite la confirmación interactiva (necesario para CI).
- `--ci <fmt>` - `vsts` o `github`.
- `-p, --profile <name>` - uso puntual de un perfil de @te-cli-auth guardado.

```bash
te deploy ./model -s my-workspace -d my-model --force --ci github
te deploy ./model -s MY.SERVER.COM -d my-model --force    # On-prem SSAS (Integrated auth)
te deploy ./model --xmla script.tmsl    # Generate TMSL only
te deploy ./model --profile staging --force
```

> [!IMPORTANT]
> `te deploy` ejecuta el Best Practice Analyzer como control previo antes de realizar el despliegue. En modo interactivo, se muestran un resumen y un mensaje de confirmación, con **`n` como opción segura predeterminada**. En CI, pasa `--force` para omitir la confirmación. Consulta @te-cli-config para la configuración del control de BPA.

> [!NOTE]
> Cuando se establece `--output-format json`, la carga JSON de `te deploy` siempre incluye los valores resueltos de `server` y `database`, incluso cuando se han resuelto a partir de la conexión activa o de un perfil, en lugar de pasarse explícitamente. Las canalizaciones pueden usar estos campos para confirmar el destino del despliegue sin volver a analizar la línea de comandos. `te deploy` y `te format` también devuelven un código de salida distinto de cero si fallan con `--output-format json`, igual que en modo texto: la carga JSON es el registro del error, no una señal de éxito.

### refresh

Inicia una actualización de datos en un modelo implementado.

`te refresh` admite:

- `--type <type>` - `full`, `dataonly` (alias `data-only`, `data`), `automatic` (alias `auto`), `calculate` (alias `calc`), `clearvalues` (alias `clear`), `defragment` (alias `defrag`), `add` (predeterminado: `automatic`).
- `--table <name>` - actualiza tabla(s) específicas; se puede repetir.
- `--partition <Table.Partition>` - actualiza partición(es) específicas.
- `--apply-refresh-policy` - aplica la política de actualización para determinar qué particiones se actualizan con la actualización incremental.
- `--effective-date <yyyy-MM-dd>` - establece la fecha efectiva que usa la política de actualización.
- `--max-parallelism <N>` - establece el número máximo de particiones que se pueden actualizar en paralelo. Encapsula la actualización en un comando TMSL `sequence`.
- `--dry-run` - muestra el script TMSL sin ejecutarlo.
- `--no-progress`, `--trace [path]`.

```bash
te refresh --type full                                 # Full refresh
te refresh --table Sales --type full                    # Single table
te refresh --type full --dry-run > refresh.tmsl         # Emit TMSL only
```

### incremental-refresh

Gestiona las políticas de actualización para la actualización incremental de las tablas.

```bash
te incremental-refresh show <table>
```

Los subcomandos adicionales (`set`, `remove` (alias `rm`), `apply`) están documentados en `te incremental-refresh --help`.

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
te connect --local                        # Power BI Desktop (Windows)
te connect --local my-report              # Filter by report name (multiple PBI Desktop instances)
te connect --profile prod                 # Activate a saved profile
te connect --clear                        # Clear the active connection (and any workspace mirror)
```

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

Consulta y administra la configuración de la CLI y las sobrescrituras de PATH de TE3. (`te config list`, alias: `ls`.) Consulta @te-cli-config.

```bash
te config list                          # Display all settings
te config paths                         # Resolved TE3 file paths
te config init                          # Create default config
te config set autoFormat true
```

### migrate

Guía de referencia que muestra cómo las opciones heredadas de la CLI de Tabular Editor 2 se corresponden con la nueva CLI. Útil como referencia rápida mientras migras una canalización basada en TE2. Consulta @te-cli-migrate para ver la guía de migración completa.

```bash
te migrate                   # Full flag mapping table
te migrate -A                # Look up a single TE2 flag
te migrate --output-format json     # Machine-readable mapping
```

## Shell

### interactive

Inicia una sesión REPL guiada con un prompt adaptado al modelo. Consulta @te-cli-interactive.

> [!TIP]
> Si ejecutas `te` en un terminal sin argumentos, también accederás al REPL de forma predeterminada (como si ejecutaras `te interactive`). Se controla mediante la clave de configuración `launchInteractiveMode`. Consulta @te-cli-interactive#auto-launch-on-empty-invocation.

`te interactive` admite:

- `<model>` - argumento posicional opcional: inicia la sesión con un modelo local, un archivo `.bim` o una carpeta `.SemanticModel` ya cargados.
- `--no-banner` - omite el banner de bienvenida al iniciar. Útil si controlas el REPL desde scripts.
- `--echo` - muestra en stdout cada comando ejecutado antes de su salida. Útil cuando canalizas comandos por stdin para que el registro muestre qué se ejecutó.
- `--batch` - modo por lotes no interactivo: lee comandos de stdin línea a línea, ejecuta cada uno y sale al llegar al EOF. Se habilita automáticamente cuando stdin se redirige.
- `--no-batch` - fuerza el modo TTY interactivo incluso cuando stdin se redirige (es mutuamente excluyente con `--batch`).

```bash
te interactive                                # Connect later
te interactive ./model                        # Start with a local model
te interactive -s MyWorkspace -d MyModel      # Start with a remote model
printf "list Measures\nexit\n" | te interactive ./model   # Pipe commands via stdin
```

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

| Código de salida | Significado                                                                                                                                                                                                                                                              |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `0`              | Éxito.                                                                                                                                                                                                                                                   |
| `1`              | Fallo genérico (argumentos no válidos, fallo del comando, errores de validación, fallo de autenticación, el gate de BPA falló con una gravedad >= error). Para `te diff`: se encontraron diferencias. |
| `2`              | Solo en `te diff`: se produjo un error durante la comparación, por lo que se desconoce el estado de las diferencias.                                                                                                                     |

Para un control detallado en las canalizaciones de CI, combina los códigos de salida con las anotaciones `--ci <vsts/github>` y los archivos de resultados `--trx`; consulta @te-cli-cicd.

## Páginas relacionadas

- @te-cli - información general y contexto.
- @te-cli-install - instalación y configuración de la CLI.
- @te-cli-auth - autenticación y administración de conexiones.
- @te-cli-config - archivo de configuración, BPA gate y comportamiento tras la mutación.
- @te-cli-migrate - mapeo de opciones TE2 → TE3.
