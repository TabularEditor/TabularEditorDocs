---
uid: command-line-options
title: Línea de comandos (Tabular Editor 2)
author: Daniel Otykier
updated: 2026-06-09
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      none: true
    - product: CLI de Tabular Editor
      none: true
---

# Línea de comandos (Tabular Editor 2)

Tabular Editor se puede ejecutar desde la línea de comandos para realizar diversas tareas, lo que puede ser útil en escenarios de compilación e implementación automatizadas, etc.

## Cómo encajan las herramientas

Tabular Editor 3 es una aplicación de escritorio para desarrolladores. No tiene su propia interfaz de línea de comandos. Para implementaciones automatizadas y canalizaciones de CI/CD, usa `TabularEditor.exe` (la CLI de Tabular Editor 2 documentada en esta página) o la nueva [CLI de Tabular Editor](xref:te-cli) multiplataforma (`te`).

Ejecutar `TabularEditor.exe` en una canalización de CI/CD no requiere una licencia de Tabular Editor 3. Solo los usuarios de la aplicación Tabular Editor 3 necesitan una licencia.

> [!TIP]
> ¿Busca la nueva CLI multiplataforma? Consulte @te-cli para obtener la CLI de Tabular Editor (versión preliminar pública limitada), su sucesora que se ejecuta en Windows, macOS y Linux.

## TabularEditor.exe frente a la CLI de Tabular Editor

La CLI de Tabular Editor (`te`) es la sucesora multiplataforma de `TabularEditor.exe`. No es solo una reescritura para macOS y Linux: incorpora la edición, la inspección, la comparación de diferencias de modelos, las pruebas, la activación de actualizaciones y el análisis de VertiPaq como operaciones de canalización de primera clase; nada de esto era posible con `TabularEditor.exe`. La CLI `te` está en versión preliminar pública limitada (expira el 2026-09-30); por ahora, usa `TabularEditor.exe` en canalizaciones de producción.

|                                                | CLI de TE2 (`TabularEditor.exe`)                      | CLI de TE (`te`)                                                                                                                                                                              |
| ---------------------------------------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Estado                                         | Estable y lista para producción                                          | Versión preliminar pública limitada (expira el 2026-09-30)                                                                                                                                    |
| Plataforma                                     | Solo para Windows                                                        | Windows, macOS, Linux                                                                                                                                                                                            |
| Requiere licencia                              | No                                                                       | No (versión preliminar); por determinar cuando llegue a GA                                                                                                                                    |
| Binario                                        | Aplicación WinForms; requiere el wrapper `start /wait`                   | Binario de consola diseñado específicamente para este fin; no requiere wrapper                                                                                                                                   |
| **Autenticación**                              |                                                                          |                                                                                                                                                                                                                  |
| Entidad de servicio                            | Mediante una cadena de conexión de MSOLAP                                | Compatibilidad nativa con `--auth spn`, `--auth env`, `--auth managed-identity`; credenciales a través de variables de entorno, stdin o certificado; almacén seguro de credenciales nativo del sistema operativo |
| Identidad administrada                         | No                                                                       | Sí (`--auth managed-identity`), para runners alojados en Azure                                                                                                                                |
| Inicio de sesión interactivo en el navegador   | No                                                                       | Sí (`te auth login`)                                                                                                                                                                          |
| **CI/CD**                                      |                                                                          |                                                                                                                                                                                                                  |
| Anotaciones de CI                              | `-V` (Azure DevOps), `-G` (GitHub) | `--ci vsts`, `--ci github` en cada comando                                                                                                                                                                       |
| Modo no interactivo                            | Sin opción explícita; si hay errores, puede solicitarte datos            | Opción global `--non-interactive`: falla de inmediato, sin solicitar datos                                                                                                                       |
| Códigos de salida predecibles                  | Parcial                                                                  | `0` = éxito, `1` = fallo, `2` = discrepancia del diff                                                                                                                                                            |
| Salida estructurada                            | No                                                                       | `--output-format json/csv/tmdl/tmsl` en cada comando                                                                                                                                                             |
| Resultados de VSTEST                           | Opción `-T`                                                              | `--trx <file>` en `validate`, `bpa run`, `test run`                                                                                                                                                              |
| **Implementación**                             |                                                                          |                                                                                                                                                                                                                  |
| Implementar el modelo                          | Opción `-D`                                                              | `te deploy` con opciones detalladas (`--deploy-roles`, `--deploy-partitions`, `--deploy-connections`, `--deploy-full`, etc.)                                                  |
| Generar XMLA/TMSL sin realizar el despliegue   | opción `-X`                                                              | `te deploy --xmla <file>` o `--dry-run`                                                                                                                                                                          |
| Comprobación de BPA antes del despliegue       | No                                                                       | Integrado; usa `--skip-bpa` o `--fix-bpa` para anularlo                                                                                                                                                          |
| Perfiles de conexión                           | No                                                                       | `te profile set/list/show` - perfiles reutilizables con nombre por entorno                                                                                                                                       |
| **Best Practice Analyzer**                     |                                                                          |                                                                                                                                                                                                                  |
| Ejecutar BPA                                   | opciones `-A` / `-AX`                                                    | `te bpa run` con `--fail-on warning/error`, `--fix`, delimitación mediante `--path` y `--vpax` para reglas compatibles con VPA                                                                                   |
| Gestión de reglas de BPA                       | No                                                                       | `te bpa rules add/rm/set/list/disable/enable/init`                                                                                                                                                               |
| **Edición de modelos en la canalización**      |                                                                          |                                                                                                                                                                                                                  |
| Ejecutar C# Script                             | opción `-S`                                                              | `te script` - múltiples scripts, código en línea, stdin, `--dry-run`, símbolos del preprocesador (`TECLI`)                                                                                    |
| Ejecutar macros                                | No                                                                       | `te macro run` con contexto `--on <object>`                                                                                                                                                                      |
| Establecer/consultar propiedades               | No                                                                       | `te get`, `te set`, `te add`, `te rm`, `te mv`, `te replace`                                                                                                                                                     |
| Formato DAX                                    | No                                                                       | `te format` - todas las expresiones o un único objeto; DAX y M                                                                                                                                                   |
| **Inspección**                                 |                                                                          |                                                                                                                                                                                                                  |
| Listar objetos del modelo                      | No                                                                       | `te ls` con filtros de ruta con comodines, `--type`, `--paths-only`, `--output-format bim`                                                                                                                       |
| Buscar expresiones/nombres                     | No                                                                       | `te find` con expresiones regulares y ámbito (`--in expressions/names/descriptions`)                                                                                                          |
| Comparar dos modelos                           | No                                                                       | `te diff` - comparación estructural con código de salida `2` ante cualquier diferencia                                                                                                                           |
| Análisis de dependencias                       | No                                                                       | `te deps` - dependencias ascendentes y descendentes para cualquier objeto; `--unused` para encontrar código muerto                                                                                               |
| **Actualización**                              |                                                                          |                                                                                                                                                                                                                  |
| Iniciar una actualización                      | No                                                                       | `te refresh` con `--type`, `--table`, `--partition`, `--apply-refresh-policy`, `--dry-run`                                                                                                                       |
| **Pruebas**                                    |                                                                          |                                                                                                                                                                                                                  |
| Pruebas de aserción de DAX                     | No                                                                       | `te test run` con `--tag`, `--trx`, `--ci`; `te test init/snapshot/compare`                                                                                                                                      |
| **Análisis de VertiPaq**                       |                                                                          |                                                                                                                                                                                                                  |
| Estadísticas de almacenamiento                 | No                                                                       | `te vertipaq` - columnas, relaciones, particiones; `--export`/`--import` VPAX                                                                                                                                    |
| **Otro**                                       |                                                                          |                                                                                                                                                                                                                  |
| REPL interactivo                               | No                                                                       | `te interactive` - shell con reconocimiento del modelo y autocompletado con Tab                                                                                                                                  |
| Autocompletado con Tab en el shell             | No                                                                       | `te completion bash/zsh/pwsh`                                                                                                                                                                                    |
| Compatibilidad con versiones anteriores de TE2 | Nativa                                                                   | Capa de compatibilidad integrada: las invocaciones existentes de `TabularEditor.exe` funcionan sin cambios                                                                                       |

Para ver una correspondencia opción por opción entre la sintaxis de TE2 y la nueva CLI, consulta @te-cli-migrate.

**Nota:** Dado que TabularEditor.exe es una aplicación WinForms, si la ejecutas directamente desde un símbolo del sistema de Windows, el hilo volverá inmediatamente al símbolo del sistema. Esto puede provocar problemas en scripts de comandos, etc. Para esperar a que TabularEditor.exe termine sus tareas de línea de comandos, ejecútalo siempre así: `start /wait TabularEditor ...`

Para ver las opciones de línea de comandos disponibles en Tabular Editor, ejecuta el siguiente comando:

**Línea de comandos de Windows:**

```shell
start /wait TabularEditor.exe /?
```

**PowerShell:**

```powershell
$p = Start-Process -filePath TabularEditor.exe -Wait -NoNewWindow -PassThru -ArgumentList "/?"
```

Salida:

```cmd
Uso:

TABULAREDITOR ( file | server database | -L [name] ) [-S script1 [script2] [...]]
    [-SC] [-A [rules] | -AX rules] [(-B | -F | -TMDL) output [id]] [-V | -G] [-T resultsfile]
    [-D [server database [-L user pass] [-F | -O [-C [plch1 value1 [plch2 value2 [...]]]]
        [-P [-Y]] [-S] [-R [-M]]]
        [-X xmla_script]] [-W] [-E]]

file                Ruta completa del archivo Model.bim o de la carpeta del modelo database.json que se va a cargar.
server              Nombre del servidor\instancia o cadena de conexión desde la que se cargará el modelo.
database            Id de la base de datos del modelo que se va a cargar. Si se deja en blanco ("), se selecciona la primera
                      base de datos disponible en el servidor.
-L / -LOCAL         Se conecta a una instancia (local) de Analysis Services de Power BI Desktop. Si no se
                      especifica ningún nombre, se asume que hay exactamente 1 instancia en ejecución. En caso contrario,
                      el nombre debe coincidir con el nombre del archivo .pbix cargado en Power BI Desktop.
-S / -SCRIPT        Ejecuta el script especificado en el modelo después de cargarlo.
  scriptN             Ruta completa de uno o varios archivos que contienen un C# Script para ejecutar o un
                      script en línea.
-SC / -SCHEMACHECK  Intenta conectarse a todos los orígenes de datos del proveedor para detectar cambios en el esquema
                    de las tablas. Genera...
                      ...advertencias por tipos de datos no coincidentes y columnas de origen no asignadas
                      ...errores por columnas del modelo no asignadas.
-A / -ANALYZE       Ejecuta Best Practice Analyzer y muestra el resultado en la consola.
  rules               Ruta opcional de un archivo o la URL de reglas BPA adicionales que se van a analizar. Si
                      se especifica, el modelo no se analiza con las reglas del usuario local ni de la máquina local,
                      pero las reglas definidas dentro del modelo se siguen aplicando.
-AX / -ANALYZEX     Igual que -A / -ANALYZE, pero excluye las reglas especificadas en las anotaciones del modelo.
-B / -BIM / -BUILD  Guarda el modelo (después de la ejecución opcional del script) como un archivo Model.bim.
  output              Ruta completa del archivo Model.bim donde se guardará.
  id                  Id/nombre opcional que se asignará al objeto Database al guardar.
-F / -FOLDER        Guarda el modelo (después de la ejecución opcional del script) como una estructura de carpetas.
  output              Ruta completa de la carpeta donde se guardará. La carpeta se crea si no existe.
  id                  Id/nombre opcional que se asignará al objeto Database al guardar.
-TMDL               Guarda el modelo (después de la ejecución opcional del script) como una estructura de carpetas TMDL.
  output              Ruta completa de la carpeta TMDL donde se guardará. La carpeta se crea si no existe.
  id                  Id/nombre opcional que se asignará al objeto Database al guardar.
-V / -VSTS          Genera comandos de registro de Visual Studio Team Services.
-G / -GITHUB        Genera comandos de flujo de trabajo para GitHub Actions.
-T / -TRX         Genera un archivo VSTEST (trx) con detalles de la ejecución.
  resultsfile       Nombre del archivo XML de VSTEST.
-D / -DEPLOY        Despliegue desde la línea de comandos
                      Si no se especifican parámetros adicionales, este modificador guardará los metadatos del modelo
                      de nuevo en el origen (archivo o base de datos).
  server              Nombre del servidor donde se realizará el despliegue o cadena de conexión a Analysis Services.
  database            Id de la base de datos que se va a desplegar (crear/sobrescribir).
  -L / -LOGIN         Desactiva la seguridad integrada al conectarse al servidor. Especifica:
    user                Nombre de usuario (debe ser un usuario con derechos de administrador en el servidor)
    pass                Contraseña
  -F / -FULL          Despliega todos los metadatos del modelo, permitiendo sobrescribir una base de datos existente.
  -O / -OVERWRITE     Permite desplegar (sobrescribir) una base de datos existente.
    -C / -CONNECTIONS   Despliega (sobrescribe) los Data sources existentes en el modelo. Después del modificador -C,
                        puedes especificar, opcionalmente, cualquier cantidad de pares marcador de posición/valor. Al hacerlo,
                        se reemplazará cualquier aparición de los marcadores de posición especificados (plch1, plch2, ...) en las
                        cadenas de conexión de cada Data source del modelo por los valores especificados
                        (value1, value2, ...).
    -P / -PARTITIONS    Despliega (sobrescribe) las particiones de tabla existentes en el modelo.
      -Y / -SKIPPOLICY    No sobrescribe las particiones que tengan definidas políticas de actualización incremental.
    -S / -SHARED        Despliega (sobrescribe) expresiones compartidas.
    -R / -ROLES         Despliega roles.
      -M / -MEMBERS       Despliega miembros del rol.
  -X / -XMLA        No realiza ningún despliegue. En su lugar, genera un script XMLA/TMSL para desplegarlo más tarde.
    xmla_script       Nombre del archivo de salida del nuevo script XMLA/TMSL.
  -W / -WARN        Muestra información sobre objetos sin procesar en forma de advertencias.
  -E / -ERR         Devuelve un código de salida distinto de cero si Analysis Services devuelve mensajes de error después de que
                      se hayan desplegado o actualizado los metadatos.
```

> [!WARNING]
> La incorporación de la opción de implementación `-S` / `-SHARED` en [Tabular Editor 2.27.0](https://github.com/TabularEditor/TabularEditor/releases/tag/2.27.0) es un **cambio incompatible**. Si estás usando la CLI de Tabular Editor para realizar implementaciones y vas a actualizar desde una versión anterior de Tabular Editor, asegúrate de incluir esa opción en tus comandos de la CLI, ya que, de lo contrario, **no se implementarán las expresiones compartidas**.

> [!TIP]
> La opción `-F` se introdujo en [Tabular Editor 2.27.0](https://github.com/TabularEditor/TabularEditor/releases). Se usa para realizar una implementación "completa" y equivale a especificar `-O -C -P -S -R -M`.

## Conexión a Azure Analysis Services

Puedes usar cualquier cadena de conexión válida de SSAS en lugar de un nombre de servidor en el comando. El siguiente comando carga un modelo desde Azure Analysis Services y lo guarda localmente como un archivo Model.bim:

**Línea de comandos de Windows:**

```shell
start /wait TabularEditor.exe "Provider=MSOLAP;Data Source=asazure://northeurope.asazure.windows.net/MyAASServer;User ID=xxxx;Password=xxxx;Persist Security Info=True;Impersonation Level=Impersonate" MyModelDB -B "C:\Projects\FromAzure\Model.bim"
```

**PowerShell:**

```powershell
$p = Start-Process -filePath TabularEditor.exe -Wait -NoNewWindow -PassThru `
       -ArgumentList "`"Provider=MSOLAP;Data Source=asazure://northeurope.asazure.windows.net/MyAASServer;User ID=xxxx;Password=xxxx;Persist Security Info=True;Impersonation Level=Impersonate`" MyModelDB -B C:\Projects\FromAzure\Model.bim"
```

Si prefieres conectarte usando una entidad de servicio (ID de aplicación y clave) en lugar de la autenticación de Azure Active Directory, puedes usar la siguiente cadena de conexión:

```
Provider=MSOLAP;Data Source=asazure://northeurope.asazure.windows.net/MyAASServer;User ID=app:<APPLICATION ID>@<TENANT ID>;Password=<APPLICATION KEY>;Persist Security Info=True;Impersonation Level=Impersonate
```

## Automatización de cambios de script

Si has creado un script dentro de Tabular Editor y quieres aplicarlo a un archivo Model.bim antes del despliegue, puedes usar la opción de línea de comandos "-S" (Script):

**Línea de comandos de Windows:**

```shell
start /wait TabularEditor.exe "C:\Projects\MyModel\Model.bim" -S "C:\Projects\MyModel\MyScript.cs" -D localhost\tabular MyModel
```

**PowerShell:**

```powershell
$p = Start-Process -filePath TabularEditor.exe -Wait -NoNewWindow -PassThru `
       -ArgumentList "`"C:\Projects\MyModel\Model.bim`" -S `"C:\Projects\MyModel\MyScript.cs`" -D `"localhost\tabular`" `"MyModel`""
```

Este comando cargará el archivo Model.bim en Tabular Editor, aplicará el script especificado y desplegará el modelo modificado en el servidor "localhost\tabular" como una nueva base de datos "MyModel". Usa la opción "-O" (Overwrite) si quieres sobrescribir una base de datos existente en el servidor con el mismo nombre.

Puedes usar la opción "-B" (Build) en lugar de la opción "-D" (Deploy) para generar el modelo modificado como un nuevo archivo Model.bim, en vez de desplegarlo directamente en un servidor. Esto es útil si quieres desplegar el modelo con otra herramienta de despliegue o si quieres inspeccionarlo en Visual Studio o Tabular Editor antes de desplegarlo. También puede ser útil en escenarios de compilación automatizada, donde quieres guardar el modelo modificado como un artefacto de la versión antes de desplegarlo.

## Modificar cadenas de conexión durante el despliegue

Supongamos que tienes un modelo que contiene un origen de datos con la siguiente cadena de conexión:

```
Provider=SQLOLEDB.1;Data Source=sqldwdev;Persist Security Info=False;Integrated Security=SSPI;Initial Catalog=DW
```

Durante el despliegue, quieres modificar la cadena para que apunte a una base de datos de UAT o de producción. La mejor manera de hacerlo es, primero, usar un script que cambie toda la cadena de conexión por un valor de marcador de posición y, después, usar la opción -C para sustituir el marcador por la cadena de conexión real.

Coloca el siguiente script en un archivo llamado "ClearConnectionStrings.cs" o similar:

```csharp
// Esto reemplazará la cadena de conexión de todos los orígenes de datos del proveedor (heredados) del modelo
// por un marcador de posición basado en el nombre del Data source. Por ejemplo, si tu Data source se llama
// "SQLDW", la cadena de conexión después de ejecutar este script sería "SQLDW":

foreach(var ds in Model.DataSources.OfType<ProviderDataSource>())
    ds.ConnectionString = ds.Name;
```

Podemos indicar a Tabular Editor que ejecute el script y, a continuación, realizar la sustitución de marcadores de posición con el siguiente comando:

**Línea de comandos de Windows:**

```shell
start /wait TabularEditor.exe "Model.bim" -S "ClearConnectionStrings.cs" -D localhost\tabular MyModel -C "SQLDW" "Provider=SQLOLEDB.1;Data Source=sqldwprod;Persist Security Info=False;Integrated Security=SSPI;Initial Catalog=DW"
```

**PowerShell:**

```powershell
$p = Start-Process -filePath TabularEditor.exe -Wait -NoNewWindow -PassThru `
       -ArgumentList "Model.bim -S ClearConnectionStrings.cs -D localhost\tabular MyModel -C SQLDW `"Provider=SQLOLEDB.1;Data Source=sqldwprod;Persist Security Info=False;Integrated Security=SSPI;Initial Catalog=DW`""
```

El comando anterior desplegará el archivo Model.bim como una nueva base de datos de SSAS "MyModel" en la instancia de SSAS "localhost\tabular". Antes del despliegue, el script se usa para reemplazar todas las cadenas de conexión en los orígenes de datos del proveedor (heredados) por el nombre del origen de datos, que se usará como marcador de posición. Suponiendo que solo tengamos un único origen de datos llamado "SQLDW", el conmutador -C actualizará la cadena de conexión, reemplazando "SQLDW" por la cadena completa especificada.

Esta técnica es útil en escenarios en los que quieres desplegar el mismo modelo en varios entornos que deben procesar datos de diferentes orígenes (idénticos), por ejemplo, una base de datos de producción, preproducción o UAT. Si usas Azure DevOps (ver más abajo), considera usar una variable para almacenar la cadena de conexión real que se utilizará, en lugar de dejarla codificada en el comando.

## Integración con Azure DevOps

Si quieres usar el CLI de Tabular Editor dentro de una canalización de Azure DevOps, deberías usar el modificador "-V" en cualquier comando de TabularEditor.exe que ejecute tu script. Este modificador hará que Tabular Editor emita comandos de registro en un [formato legible por Azure DevOps](https://github.com/Microsoft/vsts-tasks/blob/master/docs/authoring/commands.md). Esto permite que Azure DevOps reaccione correctamente ante errores, etc.

Al realizar el despliegue desde la línea de comandos, se mostrará en la consola información sobre los objetos sin procesar. En escenarios de despliegue automatizado, puede que quieras que tu agente de compilación reaccione cuando haya objetos que queden sin procesar, por ejemplo al agregar nuevas columnas, cambiar la expresión DAX de una tabla calculada, etc. En ese caso, puedes usar el modificador "-W" además del modificador "-V" mencionado anteriormente, para emitir esta información como advertencias. Al hacerlo, el despliegue devolverá a Azure DevOps el estado "SucceededWithIssues" una vez que se haya completado el despliegue. También puede usar el modificador "-E" si desea que el despliegue devuelva el estado "Failed" en caso de que el servidor informe de cualquier error de DAX después de un despliegue satisfactorio.

`start /wait` no es necesario al ejecutar TabularEditor.exe dentro de una tarea de línea de comandos en una canalización de Azure DevOps. Esto se debe a que la tarea de línea de comandos no finalizará hasta que todos los hilos iniciados por la tarea hayan terminado. Dicho de otro modo, solo necesitas usar `start /wait` si tienes comandos adicionales después de la llamada a TabularEditor.exe y, en ese caso, asegúrate de usar `start /B /wait`. El modificador `/B` es obligatorio para que la salida de TabularEditor.exe se redirija correctamente al registro de la canalización.

```shell
TabularEditor.exe "C:\Projects\My Model\Model.bim" -D ssasserver databasename -O -C -P -S -V -E -W
```

O con varios comandos:

```shell
start /B /wait TabularEditor.exe "C:\Projects\Finance\Model.bim" -D ssasserver Finance -O -C -P -S -V -E -W
start /B /wait TabularEditor.exe "C:\Projects\Sales\Model.bim" -D ssasserver Sales -O -C -P -S -V -E -W
```

La figura siguiente muestra el aspecto de este tipo de compilación en Azure DevOps:

![image](https://user-images.githubusercontent.com/8976200/27128146-bc044356-50fd-11e7-9a67-b893fc48ea50.png)

Si el despliegue falla por cualquier motivo, Tabular Editor devuelve el estado "Fallido" a Azure DevOps, independientemente de si está usando o no el modificador "-W".

Para obtener más información sobre Azure DevOps y Tabular Editor, [eche un vistazo a esta serie de entradas del blog](https://tabulareditor.github.io/2019/02/20/DevOps1.html) (especialmente [el capítulo 3](https://tabulareditor.github.io/2019/10/08/DevOps3.html) y los capítulos posteriores).

### Tarea de PowerShell de Azure DevOps

Si prefiere usar una tarea de PowerShell en lugar de una tarea de línea de comandos, debe ejecutar TabularEditor.exe con el cmdlet `Start-Process`, tal como se muestra arriba. Además, asegúrese de pasar el código de salida del proceso como el parámetro de salida en su script de PowerShell, para que los errores que se produzcan en Tabular Editor hagan que la tarea de PowerShell falle:

```powershell
$p = Start-Process -filePath TabularEditor.exe -Wait -NoNewWindow -PassThru `
       -argumentList "`"C:\Projects\My Model\Model.bim`" -D ssasserver databasename -O -C -P -S -V -E -W"
exit $p.ExitCode
```

### Pasar parámetros a scripts mediante variables de entorno

Al ejecutar scripts de C# con la opción `-S` en pipelines de Azure DevOps, la forma recomendada de pasar parámetros es mediante variables de entorno en lugar de argumentos de la línea de comandos. Los scripts de C# pueden leer variables de entorno usando `Environment.GetEnvironmentVariable()`, y Azure DevOps pone automáticamente a disposición todas las variables del pipeline como variables de entorno.

**Ejemplo: establecer variables de entorno en YAML:**

```yaml
variables:
  deployEnv: 'Production'
  serverName: 'prod-sql-server'

steps:
- script: TabularEditor.exe "Model.bim" -S "UpdateModel.csx" -D "$(serverName)" "MyDatabase" -O -V -E -W
  displayName: 'Despliegue con parámetros de script'
  env:
    DEPLOY_ENV: $(deployEnv)
    SERVER_NAME: $(serverName)
```

**Ejemplo: tarea de PowerShell con variables de entorno:**

```yaml
- task: PowerShell@2
  displayName: 'Ejecutar script de Tabular Editor'
  env:
    DEPLOY_ENV: 'UAT'
    CONNECTION_STRING: $(sqldwConnectionString)
  inputs:
    targetType: 'inline'
    script: |
      $p = Start-Process -filePath TabularEditor.exe -Wait -NoNewWindow -PassThru `
             -ArgumentList "`"Model.bim`" -S `"ConfigureModel.csx`" -B `"output/Model.bim`" -V"
      exit $p.ExitCode
```

**En su script de C# (por ejemplo, UpdateModel.csx):**

```csharp
var deployEnv = Environment.GetEnvironmentVariable("DEPLOY_ENV");
var serverName = Environment.GetEnvironmentVariable("SERVER_NAME");

Info($"Configurando el modelo para el entorno {deployEnv} en {serverName}");

// Aplicar cambios específicos del entorno
foreach(var ds in Model.DataSources.OfType<ProviderDataSource>())
{
    ds.ConnectionString = ds.ConnectionString.Replace("{SERVER}", serverName);
}
```

Este enfoque es más limpio y más fácil de mantener que codificar valores en los scripts o usar técnicas complejas de reemplazo de cadenas. Para más información sobre el uso de variables de entorno en scripts de C#, consulte [C# Scripts - Acceso a variables de entorno](xref:csharp-scripts#accessing-environment-variables).

## Ejecutar Best Practice Analyzer

Puede usar el modificador "-A" para que Tabular Editor analice su modelo y detecte todos los objetos que infrinjan cualquiera de las reglas de mejores prácticas definidas en el equipo local (en el archivo %AppData%\..\Local\TabularEditor\BPARules.json), o como anotaciones dentro del propio modelo. Como alternativa, puede especificar la ruta de un archivo .json que contenga reglas de mejores prácticas después del modificador "-A", para analizar el modelo con las reglas definidas en el archivo. Los objetos que incumplan las reglas se mostrarán en la consola.

Si también está usando el modificador "-V", el nivel de gravedad de cada regla determinará cómo se notifica la infracción a la canalización de compilación:

- Gravedad = 1: solo informativo
- Gravedad = 2 generará una ADVERTENCIA
- Gravedad >= 3 generará un ERROR

## Realizar una comprobación del esquema de la fuente de datos

A partir de la [versión 2.8](https://github.com/TabularEditor/TabularEditor/releases/tag/2.8) (2.8), puede usar el modificador -SC (-SCHEMACHECK) para validar las consultas de origen de las tablas. Esto equivale a invocar la [interfaz de usuario de Refresh Table Metadata](xref:importing-tables-te2#refreshing-table-metadata), con la diferencia de que no se realizará ningún cambio en el modelo, pero las diferencias de esquema se notifican en la consola. Los tipos de datos cambiados y las columnas que se hayan agregado al origen se notificarán como advertencias. Las columnas de origen que falten se notificarán como errores. Si se especifican los modificadores -SC (-SCHEMACHECK) y -S (-SCRIPT), la comprobación de esquema se ejecutará después de que el script se haya ejecutado correctamente, lo que le permite modificar las propiedades de la fuente de datos antes de realizar la comprobación de esquema, por ejemplo, para especificar la contraseña de una credencial.

También puede anotar tablas y columnas si quiere que la comprobación de esquema las trate de una manera específica. [Más información aquí](xref:importing-tables-te2#ignoring-objects).

## Salida de la línea de comandos y códigos de salida

La línea de comandos proporciona varios detalles, en función de los parámetros usados y de los eventos que se produzcan durante la ejecución. Los códigos de salida se introdujeron en la [versión 2.7.4](https://github.com/TabularEditor/TabularEditor/releases/tag/2.7.4).

| Nivel       | Comando                         | Mensaje                                                                                                                | Aclaración                                                                                                                                                                                                                                               |
| ----------- | ------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Error       | (Cualquiera) | Sintaxis de argumentos no válida                                                                                       | Se proporcionaron argumentos no válidos al CLI de Tabular Editor                                                                                                                                                                                         |
| Error       | (Cualquiera) | Archivo no encontrado: ...                             |                                                                                                                                                                                                                                                          |
| Error       | (Cualquiera) | Error al cargar el archivo: ...                        | El archivo está dañado o no contiene metadatos TOM válidos en formato JSON                                                                                                                                                                               |
| Error       | (Cualquiera) | Error al cargar el modelo: ...                         | No se pudo conectar a la instancia de Analysis Services proporcionada; no se encontró la base de datos; los metadatos de la base de datos están dañados; o la base de datos no tiene un nivel de compatibilidad admitido                                 |
| Error       | -SCRIPT                         | No se encontró el archivo de script especificado                                                                       |                                                                                                                                                                                                                                                          |
| Error       | -SCRIPT                         | Errores de compilación del script:                                                                     | El script contenía sintaxis de C# no válida. Los detalles se mostrarán en las líneas siguientes.                                                                                                                         |
| Error       | -SCRIPT                         | Error al ejecutar el script: ...                       | Excepción no controlada al ejecutar el script.                                                                                                                                                                                           |
| Información | -SCRIPT                         | Nº de línea del script: ...                            | Uso de los métodos `Info(string)` o `Output(string)` dentro del script.                                                                                                                                                                  |
| Advertencia | -SCRIPT                         | Advertencia del script: ...                            | Uso del método `Warning(string)` dentro del script.                                                                                                                                                                                      |
| Error       | -SCRIPT                         | Error del script: ...                                  | Uso del método `Error(string)` dentro del script.                                                                                                                                                                                        |
| Error       | -FOLDER, -BIM                   | Los argumentos -FOLDER y -BIM son mutuamente excluyentes.                                              | Tabular Editor no puede guardar el modelo cargado actualmente en una estructura de carpetas y en un archivo .bim al mismo tiempo.                                                                                        |
| Error       | -ANALYZE                        | No se encontró el archivo de reglas: ...               |                                                                                                                                                                                                                                                          |
| Error       | -ANALYZE                        | Archivo de reglas no válido: ...                       | El archivo de reglas de BPA especificado está dañado o no contiene un JSON válido.                                                                                                                                                       |
| Información | -ANALYZE                        | ... viola la regla ... | Resultados del Best Practice Analyzer para reglas con un nivel de gravedad de 1 o inferior.                                                                                                                                              |
| Advertencia | -ANALYZE                        | ... viola la regla ... | Resultados del Best Practice Analyzer para reglas con un nivel de gravedad de 2.                                                                                                                                                         |
| Error       | -ANALYZE                        | ... viola la regla ... | Resultados del Best Practice Analyzer para reglas con un nivel de gravedad de 3 o superior.                                                                                                                                              |
| Error       | -DEPLOY                         | ¡Falló el despliegue! ...                                              | Motivo del fallo devuelto directamente por la instancia de Analysis Service (por ejemplo: base de datos no encontrada, no se permite sobrescribir la base de datos, etc.)                             |
| Información | -DEPLOY                         | Objeto sin procesar: ...                               | Objetos que están en el estado "NoData" o "CalculationNeeded" tras una implementación correcta. Utilice el modificador -W para tratarlos como Nivel=Advertencia.                                                         |
| Advertencia | -DEPLOY                         | El objeto no está en estado "Ready": ...               | Objetos que se encuentran en estado "DependencyError", "EvaluationError" o "SemanticError" después de un despliegue correcto. Si usa la opción -W, también incluye los objetos en estado "NoData" o "CalculationNeeded". |
| Advertencia | -DEPLOY                         | Error en X:...                                         | Objetos que contienen DAX no válido después de un despliegue correcto (medidas, columnas calculadas, tablas calculadas, roles). Use la opción -E para tratarlos como Level=Error.                     |

Si se encuentra alguno de los mensajes de nivel "Error", Tabular Editor devolverá el código de salida = 1. En caso contrario, 0.
