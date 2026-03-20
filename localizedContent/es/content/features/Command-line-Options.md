---
uid: command-line-options
title: Línea de comandos
author: Daniel Otykier
updated: 2021-08-26
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      none: true
---

# Línea de comandos

Tabular Editor se puede ejecutar desde la línea de comandos para realizar diversas tareas, lo que puede ser útil en escenarios de compilación e implementación automatizadas, etc.

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

file                Ruta de acceso completa al archivo Model.bim o a la carpeta del modelo database.json que se va a cargar.
server              Nombre de servidor\instancia o cadena de conexión desde la que se cargará el modelo
database            ID de la base de datos del modelo que se va a cargar. Si se deja en blanco (""), selecciona la primera
                      base de datos disponible en el servidor.
-L / -LOCAL         Se conecta a una instancia (local) de Analysis Services de Power BI Desktop. Si no se especifica un
                      nombre, se supone que se está ejecutando exactamente 1 instancia. En caso contrario,
                      el nombre debe coincidir con el nombre del archivo .pbix cargado en Power BI Desktop.
-S / -SCRIPT        Ejecuta el script especificado en el modelo después de cargarlo.
  scriptN             Ruta de acceso completa a uno o varios archivos que contienen un C# Script que se va a ejecutar o un
                      script en línea.
-SC / -SCHEMACHECK  Intenta conectarse a todos los orígenes de datos del proveedor para detectar cambios en el esquema de la tabla.
                    Genera...
                      ...advertencias para tipos de datos no coincidentes y columnas de origen no asignadas
                      ...errores para columnas del modelo no asignadas.
-A / -ANALYZE       Ejecuta Best Practice Analyzer y muestra el resultado en la consola.
  rules               Ruta opcional de un archivo o una URL con reglas BPA adicionales que se van a analizar. Si se
                      especifica, el modelo no se analiza con reglas locales del usuario o del equipo,
                      pero las reglas definidas dentro del modelo se siguen aplicando.
-AX / -ANALYZEX     Igual que -A / -ANALYZE, pero excluye las reglas especificadas en las anotaciones del modelo.
-B / -BIM / -BUILD  Guarda el modelo (después de la ejecución opcional del script) como un archivo Model.bim.
  output              Ruta de acceso completa del archivo Model.bim donde se guardará.
  id                  ID/nombre opcional que se asignará al objeto Database al guardar.
-F / -FOLDER        Guarda el modelo (después de la ejecución opcional del script) como una estructura de carpetas.
  output              Ruta de acceso completa de la carpeta donde se guardará. La carpeta se crea si no existe.
  id                  ID/nombre opcional que se asignará al objeto Database al guardar.
-TMDL               Guarda el modelo (después de la ejecución opcional del script) como una estructura de carpetas TMDL.
  output              Ruta de acceso completa de la carpeta TMDL donde se guardará. La carpeta se crea si no existe.
  id                  ID/nombre opcional que se asignará al objeto Database al guardar.
-V / -VSTS          Genera comandos de registro de Visual Studio Team Services.
-G / -GITHUB        Genera comandos de flujo de trabajo de GitHub Actions.
-T / -TRX         Genera un archivo VSTEST (trx) con detalles sobre la ejecución.
  resultsfile       Nombre de archivo del XML de VSTEST.
-D / -DEPLOY        Implementación desde la línea de comandos
                      Si no se especifican parámetros adicionales, este modificador guardará los metadatos del modelo
                      de nuevo en el origen (archivo o base de datos).
  server              Nombre del servidor en el que implementar o cadena de conexión a Analysis Services.
  database            ID de la base de datos que se va a implementar (crear/sobrescribir).
  -L / -LOGIN         Deshabilita la seguridad integrada al conectarse al servidor. Especifica:
    user                Nombre de usuario (debe ser un usuario con permisos de administrador en el servidor)
    pass                Contraseña
  -F / -FULL          Implementa todos los metadatos del modelo, permitiendo sobrescribir una base de datos existente.
  -O / -OVERWRITE     Permite implementar (sobrescribir) una base de datos existente.
    -C / -CONNECTIONS   Implementa (sobrescribe) los Data source existentes en el modelo. Después del modificador -C, puedes
                        (opcionalmente) especificar cualquier número de pares marcador de posición-valor. Al hacerlo,
                        se reemplazará cualquier aparición de los marcadores de posición especificados (plch1, plch2, ...) en las
                        cadenas de conexión de cada Data source del modelo por los valores especificados
                        (value1, value2, ...).
    -P / -PARTITIONS    Implementa (sobrescribe) las particiones de tabla existentes del modelo.
      -Y / -SKIPPOLICY    No sobrescribe particiones que tengan definidas políticas de actualización incremental.
    -S / -SHARED        Implementa (sobrescribe) expresiones compartidas.
    -R / -ROLES         Implementa roles.
      -M / -MEMBERS       Implementa miembros del rol.
  -X / -XMLA        Sin implementación. En su lugar, genera un script XMLA/TMSL para una implementación posterior.
    xmla_script       Nombre de archivo del nuevo script de salida XMLA/TMSL.
  -W / -WARN        Muestra, como advertencias, información sobre objetos no procesados.
  -E / -ERR         Devuelve un código de salida distinto de cero si Analysis Services devuelve algunos mensajes de error después de que
                      los metadatos se hayan implementado/actualizado.
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
// Esto reemplazará la cadena de conexión de todos los orígenes de datos de proveedor (heredados) del modelo
// por un marcador de posición basado en el nombre del origen de datos. Por ejemplo, si tu origen de datos se llama
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
  displayName: 'Deploy with Script Parameters'
  env:
    DEPLOY_ENV: $(deployEnv)
    SERVER_NAME: $(serverName)
```

**Ejemplo: tarea de PowerShell con variables de entorno:**

```yaml
- task: PowerShell@2
  displayName: 'Run Tabular Editor Script'
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

Info($"Configuring model for {deployEnv} environment on {serverName}");

// Apply environment-specific changes
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
| Error       | -DEPLOY                         | ¡La implementación falló! ...                                          | Motivo del fallo devuelto directamente por la instancia de Analysis Service (por ejemplo: base de datos no encontrada, no se permite sobrescribir la base de datos, etc.)                             |
| Información | -DEPLOY                         | Objeto sin procesar: ...                               | Objetos que están en el estado "NoData" o "CalculationNeeded" tras una implementación correcta. Utilice el modificador -W para tratarlos como Nivel=Advertencia.                                                         |
| Advertencia | -DEPLOY                         | El objeto no está en estado "Ready": ...               | Objetos que se encuentran en estado "DependencyError", "EvaluationError" o "SemanticError" después de un despliegue correcto. Si usa la opción -W, también incluye los objetos en estado "NoData" o "CalculationNeeded". |
| Advertencia | -DEPLOY                         | Error en X:...                                         | Objetos que contienen DAX no válido después de un despliegue correcto (medidas, columnas calculadas, tablas calculadas, roles). Use la opción -E para tratarlos como Level=Error.                     |

Si se encuentra alguno de los mensajes de nivel "Error", Tabular Editor devolverá el código de salida = 1. En caso contrario, 0.
