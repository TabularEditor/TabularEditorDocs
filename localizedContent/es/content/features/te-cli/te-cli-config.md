---
uid: te-cli-config
title: Configuración personalizada
author: Peer Grønnerup
updated: 2026-10-12
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

La CLI de Tabular Editor lee una configuración opcional desde un archivo JSON. El archivo define:

- **Rutas de archivos**: donde la CLI lee las macros y las reglas de BPA, y donde escribe el registro de consultas.
- **Valores predeterminados de comportamiento**: umbrales de BPA, formato automático y validación.
- **Perfiles de conexión guardados**: los perfiles con nombre entre los que puedes alternar.

La CLI no lee ni escribe en las rutas de instalación de la versión de escritorio de Tabular Editor 3. En esta configuración, establece los archivos de reglas de BPA y de macros, o créalos con `te bpa rules init` y `te macro init`.

`te config list`, `te config set <key> <value>` y `te profile set` cubren las operaciones habituales sin editar el archivo.

## Ubicación del archivo de configuración

La CLI comprueba estas ubicaciones en este orden:

1. La variable de entorno `$TE_CONFIG` (si está definida y el archivo existe).
2. `~/.config/te/config.json` (en Windows, `%USERPROFILE%\.config\te\config.json`).
3. Si no hay archivo de configuración, la CLI usa los valores predeterminados integrados.

`te config list`, `te config set`, `te config init` y `te config paths` leen y escriben el archivo en la ruta resuelta, incluida una ruta establecida mediante `TE_CONFIG`. Usa `TE_CONFIG` para pruebas, instalaciones mediante scripts y configuración por entorno.

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

`te config paths` muestra qué archivos usa la CLI para las macros y las reglas de BPA. La salida tiene dos filas: `macros`, la ruta resuelta del archivo de macros, y `bpa.rules`, el primer archivo de reglas de BPA existente. Cualquiera de las dos filas muestra `[not set]` si no se resuelve nada.

> [!NOTE]
> Con `--output-format json`, `te config paths` escribe las rutas sin resolver como campos `null` explícitos, por ejemplo `{"macros": null, "bpa": {"rules": null}}`. `te config list --output-format json` omite los campos `null` de forma predeterminada, así que los analizadores deben manejar las claves ausentes.

## Configurar valores

```bash
te config set autoFormat true
te config set bpa.onDeploy false
te config set hidePreviewNotice true
te config set macros null              # Clear a path override
te config set -p spinner=false         # -p key=value works too
```

Las claves pueden pasarse por posición (`te config set <key> <value>`) o como `-p key=value`. Las claves desconocidas provocan que el comando finalice con el código de salida `1` y un error que enumera las claves válidas.

Si no existe ningún archivo de configuración, `te config set` crea uno automáticamente en la ruta resuelta (`$TE_CONFIG` si está establecido; de lo contrario, `~/.config/te/config.json`) antes de aplicar el cambio.

> [!NOTE]
> `te config set` establece todas las claves del esquema excepto `formatVersion`, que gestiona la CLI. Usa rutas con puntos para las claves anidadas, como `bpa.onDeploy` o `formatOptions.useSqlBiDaxFormatter`. Para editar el JSON directamente, ejecuta `te config paths` para encontrar el archivo.

## Esquema completo

El esquema completo de configuración, con todas las claves en sus valores predeterminados:

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

Las rutas definidas en la configuración se aplican a todos los comandos. Las opciones específicas de cada comando y las variables de entorno prevalecen sobre ellas, como se describe en [Prioridad de resolución de rutas](#path-resolution-priority).

| Clave       | Significado                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `macros`    | Ruta explícita a un archivo JSON de macros (normalmente `MacroActions.json`). La resuelve cualquier comando `te macro`. Para usar las mismas macros en varios equipos, o tanto en la CLI como en Tabular Editor 3, indícale un archivo compartido; por ejemplo, uno en un recurso compartido de red, en el repositorio o en el archivo de Tabular Editor 3 para escritorio. |
| `bpa.rules` | Lista ordenada de rutas o URL a archivos de reglas de BPA. `te bpa run` y la compuerta de implementación/guardado cargan **todas** las entradas existentes; `te bpa rules list` y `te config paths` usan la primera entrada existente. Los valores separados por comas en `te config set bpa.rules ...` se separan en el arreglo.                                                              |
| `queryLog`  | Ruta a un archivo de registro en el que cada invocación de `te query` añade el texto de la consulta y los metadatos de ejecución. Admite `~` para el directorio personal, por ejemplo `~/.config/te/queries.log`.                                                                                                                                                                                              |

### Prioridad de resolución de rutas

Para cada archivo proporcionado por el usuario (macros, reglas de BPA), la CLI resuelve la ruta en este orden:

1. **Opción de línea de comandos** - `--macros <path>` para comandos de macros; `--bpa-rules <path>` para la compuerta de implementación/guardado; `--rules-file <path>` para los subcomandos de `te bpa rules`.
2. **Variable de entorno** - `TE_MACROS_PATH` para macros, `TE_BPA_RULES` para reglas de BPA.
3. **Configuración de la CLI** - `macros` para macros, la primera entrada existente de `bpa.rules[]` para reglas de BPA.

La CLI no detecta las ubicaciones de instalación de Tabular Editor 3. Para crear un archivo predeterminado en el directorio actual, ejecuta `te macro init` (crea `./MacroActions.json`) o `te bpa rules init` (crea `./BPARules.json`).

Ejecuta `te config paths` para ver qué archivo resolvió realmente la CLI.

### Valores predeterminados de comportamiento

La configuración de BPA está bajo el objeto `bpa` y se accede a ella mediante claves separadas por puntos en `te config set`.

| Clave                        | Predeterminado | Descripción                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ---------------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `autoFormat`                 | `false`        | Da formato automáticamente a las expresiones DAX modificadas por un comando de modificación. El formato se limita a los objetos que el comando haya modificado, pero abarca todas las propiedades de expresiones DAX que contengan (expresiones, expresiones de cadena de formato dinámica, filas de detalle, objetivo/estado/tendencia del KPI, expresiones de grupo de cálculo y de permiso de tabla, etc.). Las consultas de partición de Power Query (M) y SQL nunca se reformatean. Siempre usa el formateador integrado sin conexión en el dialecto de comas; se aplican las claves de diseño de `formatOptions`. |
| `validateOnMutation`         | `true`         | Después de un comando de modificación (`add`, `set`, `mv`, `macro run`), comprueba que todas las referencias `Table[Column]` del modelo sigan resolviéndose. Esto detecta referencias rotas por cambios de nombre o eliminaciones antes del despliegue.                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `mutationOutput`             | `diff`         | Cómo los comandos que modifican (`add`, `set`, `move`, `remove`, `script`, `bpa run --fix`) muestran en la salida de texto el conjunto de cambios resultante: `diff` (diferencia completa antes/después), `stat` (recuentos de cambios por objeto), `name-only` (rutas de los objetos modificados) o `none` (sin conjunto de cambios; solo configuración, sin necesidad de usar la marca `--none`). Las marcas `--diff`, `--stat` y `--name-only` la anulan para una invocación. La salida JSON siempre contiene el array `changes` completo.                                  |
| `bpa.onMutation`             | `false`        | Ejecuta un análisis de BPA acotado después de cada comando de modificación (`set`, `add`, `mv`, `rm`, `macro run`). Solo se comprueban los objetos de la tabla afectada.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `bpa.onDeploy`               | `true`         | Ejecuta el control de BPA antes de que se ejecute `te deploy`. El despliegue se cancela si alguna regla se activa con una gravedad >= error. Omítelo en una invocación concreta con `--skip-bpa`, o corrígelo automáticamente con `--fix-bpa`.                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `bpa.onSave`                 | `true`         | Ejecuta el control de BPA antes de que `te save-as` escriba en disco. Omítelo en una invocación concreta con `--skip-bpa` o `--force`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `bpa.builtInRules`           | `true`         | Incluye el conjunto depurado de reglas integradas de BPA cada vez que se ejecute el control. Si es `false`, la comprobación ejecuta solo las reglas de `bpa.rules` y las reglas incrustadas en el modelo.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `bpa.disabledBuiltInRuleIds` | `null`         | ID de reglas integradas individuales que se excluirán de la puerta de calidad. Cámbialo con `te bpa rules disable <id>` y `te bpa rules enable <id>`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `vertipaqOnRefresh`          | `false`        | Tras una actualización correcta (`full`, `dataonly`, `automatic` o `add`), se ejecuta el análisis de VertiPaq y se muestran estadísticas de almacenamiento de las tablas actualizadas.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `interactiveEditMode`        | `stage`        | Comportamiento predeterminado para las mutaciones en memoria dentro de `te interactive`. `stage` mantiene las modificaciones en memoria hasta que ejecutes `save`. `save` escribe en el origen después de cada comando que modifica; en un origen remoto, cada `set` es una operación de escritura XMLA. `revert` descarta las modificaciones después de cada comando, salvo que pases `--save` o `--stage`. Las marcas `--save`, `--revert` y `--stage` por comando prevalecen sobre esta opción.                                                                                                                                                            |
| `launchInteractiveMode`      | `auto`         | Indica si ejecutar `te` en un terminal sin argumentos inicia el REPL interactivo. `auto` (predeterminado) inicia el REPL solo si stdin, stdout y stderr están todos conectados a un TTY, de modo que los scripts y las canalizaciones de CI usen el parseo normal. `always` inicia el REPL incluso con redirección. `never` muestra la ayuda en su lugar. La marca global `--non-interactive` fuerza `never` para una invocación, y la variable de entorno `TE_INTERACTIVE` establece el modo para una invocación.                                                                                                                         |
| `disableTelemetry`           | `false`        | Desactiva la telemetría de uso anónima. La telemetría contiene el nombre del comando, el código de salida y la duración. No contiene el contenido del modelo, las rutas ni el texto de las consultas.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |

```bash
te config set bpa.rules "/etc/te/team.json,/etc/te/strict.json"
te config set bpa.onDeploy true
te config set bpa.builtInRules false
te config set bpa.disabledBuiltInRuleIds "TE3_BUILT_IN_DATE_TABLE_EXISTS,TE3_BUILT_IN_HIDE_FOREIGN_KEYS"
```

### Opciones de formato

El formateador de DAX integrado de la CLI funciona sin conexión.

- Las claves de diseño `shortFormat` y `skipSpaceAfterFunction` se aplican cuando `autoFormat` vuelve a formatear expresiones modificadas y cuando `te query` muestra el texto de la consulta.
- `te set <path> --format <Property>` y `te util format-dax` ignoran las claves de diseño y usan las marcas `--long` y `--no-space-after-function`.
- El formato controlado por configuración siempre usa comas como separadores de lista. Para DAX escrito con punto y coma, usa la marca `--semicolons` de `te util format-dax`.
- `formatOptions.useSqlBiDaxFormatter` envía el formateo explícito y el renderizado de `te query` al servicio web de SQL BI [daxformatter.com](https://www.daxformatter.com), que requiere acceso a Internet. `autoFormat` siempre usa el formateador integrado.

| Clave                                  | Predeterminado | Descripción                                                                                                                                                                                                                                                                   |
| -------------------------------------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `formatOptions.shortFormat`            | `false`        | Usa un formato corto, de una sola línea, cuando sea posible.                                                                                                                                                                                                  |
| `formatOptions.skipSpaceAfterFunction` | `false`        | Omite el espacio entre el nombre de una función y su paréntesis de apertura, por ejemplo, `SUM(x)`.                                                                                                                                                           |
| `formatOptions.useSqlBiDaxFormatter`   | `false`        | Formatea DAX con el servicio web de [SQL BI daxformatter.com](https://www.daxformatter.com). Requiere acceso a Internet. El formateador integrado coincide con el formato predeterminado de Tabular Editor 3. |

### Visualización

Estos ajustes controlan la salida del terminal y el registro de diagnóstico.

| Clave               | Predeterminado | Descripción                                                                                                                                   |
| ------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `hidePreviewNotice` | `false`        | Suprime el banner amarillo de vista previa. **Se ignora cuando faltan menos de 14 días para el vencimiento.** |
| `spinner`           | `true`         | Muestra indicadores de progreso animados en el terminal. Desactivar para CI.                                  |
| `debug`             | `false`        | Activa siempre el registro de depuración (equivale a pasar `--debug`).                                     |

### Perfiles

Los perfiles de conexión guardados se almacenan bajo la clave `profiles`. Adminístralos con `te profile set`, `te profile remove` y `te profile list`, y no editando el archivo. Consulta @te-cli-auth.

Un perfil puede anular estos valores predeterminados de comportamiento mientras está activo: `autoFormat`, `validateOnMutation`, `mutationOutput`, `bpa.onMutation`, `bpa.onDeploy`, `bpa.onSave`, `vertipaqOnRefresh`, `spinner` e `interactiveEditMode`. Por ejemplo, un perfil de desarrollo puede desactivar la validación y el control de implementación, mientras que un perfil de producción formatea DAX:

```bash
te profile set dev --validate-on-mutation false --bpa-on-deploy false
te profile set prod --auto-format true
```

`te profile set` incluye opciones para `--auto-format`, `--validate-on-mutation`, `--bpa-on-mutation`, `--bpa-on-deploy`, `--vertipaq-on-refresh` y `--spinner`. Cada una acepta `true`, `false` o `null`, que elimina la sobrescritura.

## Control BPA

El control de BPA impide guardar o implementar si el modelo tiene infracciones de reglas con gravedad `error`. Se ejecuta con estos comandos:

- `te deploy` ejecuta el control, a menos que se pase `--skip-bpa` o que `bpa.onDeploy` sea `false`.
- `te save-as` ejecuta la validación, a menos que se pase `--skip-bpa` (o `--force`) o que `bpa.onSave` sea `false`.
- `te add`, `te set`, `te move`, `te remove`, `te macro run` ejecutan la validación solo cuando `bpa.onMutation` es `true`.

El control carga las reglas de BPA desde `bpa.rules` y, de forma predeterminada, el conjunto de reglas integrado (controlado por `bpa.builtInRules`). `te bpa rules disable <id>` excluye una regla integrada concreta añadiéndola a `bpa.disabledBuiltInRuleIds`, y `te bpa rules enable <id>` la quita de la lista.

Si el control encuentra infracciones con gravedad `error` o superior, el comando falla con el código de salida `1` y un resumen de las infracciones. Para continuar, usa una de estas opciones:

- `--fix-bpa` - aplica en memoria la `fixExpression` de la regla al artefacto que se va a desplegar o guardar; los archivos fuente no se modifican.
- `--skip-bpa` - desactiva el control solo para este comando.
- `--bpa-rules <path>` - repetible; sobrescribe `bpa.rules` para esta única invocación de `te deploy` o `te save-as`. Las reglas integradas siguen aplicándose salvo que `bpa.builtInRules` sea `false`.

Para comprobar el modelo con respecto a las reglas sin implementarlo, ejecuta `te bpa run`:

```bash
te bpa run --model ./model --fail-on error
te bpa run --model ./model --fix --save     # Apply fixes to the source
```

### Reglas de BPA integradas

La CLI incluye un conjunto de reglas BPA integradas. Las reglas integradas son de solo lectura: `te bpa rules set` y `te bpa rules remove` fallan con IDs integrados y sugieren `te bpa rules disable`. Para cambiar una regla integrada, cópiala en tu archivo de reglas con un ID nuevo y deshabilita la regla integrada.

`bpa.builtInRules` y `bpa.disabledBuiltInRuleIds` se aplican al control y a `te bpa run`, por lo que una regla deshabilitada con `te bpa rules disable` queda excluida en todas partes.

## Comportamiento tras la mutación

Después de un comando de modificación (`te add`, `te set`, `te move` o `te macro run`), la CLI ejecuta estas comprobaciones:

1. **Los errores de TOM** siempre se muestran. Las expresiones DAX o M no válidas en medidas, columnas, particiones o elementos de cálculo hacen que el comando falle.
2. **Validación de esquema** (`validateOnMutation`, valor predeterminado `true`) comprueba que las referencias `Table[Column]` en DAX se sigan resolviendo.
3. **Formato automático de DAX** (`autoFormat`, valor predeterminado `false`) da formato a las expresiones afectadas por la mutación con el formateador integrado.
4. **BPA tras la mutación** (`bpa.onMutation`, valor predeterminado `false`) ejecuta BPA después de la mutación y, según `--fail-on`, muestra una advertencia o finaliza con error.

`te config set <key> false` desactiva una comprobación. Un perfil puede reemplazar la clave en un entorno.

## Políticas de administrador

En Windows, `te` respeta las mismas directivas administrativas que Tabular Editor 3 y las lee de estas claves del Registro:

- `Software\\Policies\\Tabular Editor ApS`, para los valores compartidos por la CLI y la aplicación de escritorio
- su subclave `TECLI`, para los valores que solo se aplican a la CLI
- su subclave `TE3`, para los valores que solo se aplican a la aplicación de escritorio
- la clave anterior `Software\\Policies\\Kapacity\\Tabular Editor`, que aún se respeta

Un valor para todo el equipo (`HKEY_LOCAL_MACHINE`) tiene prioridad sobre uno por usuario (`HKEY_CURRENT_USER`). Dentro de la misma rama del Registro, un valor específico del producto tiene prioridad sobre uno compartido. Cuando una directiva desactiva una característica, el comando indica la directiva, no hace nada y sale con error, lo que hace fallar cualquier paso de la canalización que dependa de esa característica.

| Política               | Efecto en la CLI                                                                                                                                                                                                                                                                                                                                                                  |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DisableCSharpScripts` | Bloquea `te script` y las correcciones automáticas de `te bpa run --fix`.                                                                                                                                                                                                                                                                                         |
| `DisableMacros`        | Bloquea todos los comandos `te macro`.                                                                                                                                                                                                                                                                                                                            |
| `DisableBpaDownload`   | Bloquea las reglas de Best Practice Analyzer especificadas mediante una URL. Los archivos de reglas en disco y las reglas integradas no se ven afectados.                                                                                                                                                                                         |
| `DisableTelemetry`     | Desactiva las estadísticas anónimas de uso, independientemente de lo que indique `disableTelemetry` en la configuración.                                                                                                                                                                                                                                          |
| `BlockUnsafeScripts`   | Bloquea `te script`, `te macro run` y `te bpa run --fix` cuando el código accede a archivos, la red, procesos o ensamblados externos. Consulta [Qué cuenta como permanecer dentro del modelo](xref:csharp-scripts#what-counts-as-staying-within-the-model) para ver las API bloqueadas. La salida JSON reporta `blockedByPolicy`. |

Las directivas sobre la comprobación de actualizaciones, los Reports de errores, el Optimizador de DAX, el Administrador de paquetes de DAX, el Asistente de IA y el servidor MCP no afectan a la CLI. Consulta @policies para ver la lista completa de directivas y cómo implementarlas.

En la aplicación de escritorio, `BlockUnsafeScripts` requiere la Edición Enterprise de Tabular Editor 3. La CLI no tiene ediciones y aplica la directiva allí donde esté configurada.

## Variables de entorno

La CLI lee estas variables de entorno para rutas, comportamiento y diagnósticos. Para las variables de autenticación de Azure (`AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_CLIENT_CERTIFICATE_PATH`, etc.), consulta @te-cli-auth.

| Variable         | Propósito                                                                                                                                                                                                                                                                                                                                                                         |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TE_CONFIG`      | Ruta de acceso a un archivo de configuración alternativo. Se usa en `te config list`, `set`, `init` y `paths`.                                                                                                                                                                                                                                    |
| `TE_MACROS_PATH` | Sobrescribe la ruta del archivo de macros; es la segunda en el [orden de resolución](#path-resolution-priority). La leen los comandos `te macro`.                                                                                                                                                                                                 |
| `TE_BPA_RULES`   | Anula la lista de archivos/URL de reglas de BPA utilizada por los subcomandos `te bpa run` y `te bpa rules`.                                                                                                                                                                                                                                                      |
| `TE_BPA_CONFIG`  | Anula la ruta de acceso a la configuración del gate de BPA (`.te-bpa.json`) que lee el gate de despliegue/guardado.                                                                                                                                                                                                                            |
| `TE_DEBUG`       | Establece el valor en `1` para habilitar el registro de depuración globalmente (igual que `--debug` o `debug: true` en la configuración).                                                                                                                                                                                                      |
| `NO_SPINNER`     | Establece el valor en `1` o `true` para desactivar los indicadores de progreso animados (alternativa a `spinner: false` en la configuración).                                                                                                                                                                                                  |
| `CI`             | Se detecta automáticamente. Cuando vale `1` o `true`, la CLI desactiva el spinner y cambia a una salida de texto sin formato. La mayoría de los runners de CI lo configuran.                                                                                                                                                      |
| `TE_SESSION`     | Sobrescribe el identificador de sesión por terminal que se usa para el estado de la conexión activa. Configura esta opción para ejecutar sesiones aisladas de la CLI en el mismo shell, por ejemplo, en trabajos de matriz de CI en paralelo. Inspeccione y administre sesiones con [`te session`](xref:te-cli-commands#session). |
| `TE_INTERACTIVE` | Permite anular `launchInteractiveMode` para una sola invocación. Acepta `auto`, `always` o `never`. `TE_INTERACTIVE=always` inicia el REPL y `TE_INTERACTIVE=never` muestra la ayuda.                                                                                                                                             |
| `TE_COMPAT`      | Establécela en `te2` para forzar el modo de compatibilidad con TE2; consulta @te-cli-migrate.                                                                                                                                                                                                                                                        |

## Pasos a seguir

- @te-cli-auth - perfiles, autenticación y almacenamiento de credenciales.
- @te-cli-commands - subcomandos de `te config`.
- @te-cli-cicd - configuración del gate de BPA para pipelines.
