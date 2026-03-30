---
uid: importing-tables-te2
title: Importación de tablas en TE2
author: Daniel Otykier
updated: 2020-05-03
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      partial: true
---

# Importación de tablas en Tabular Editor 2

Si ya tienes un Data source heredado en tu modelo, haz clic con el botón derecho sobre él y elige "Importar tablas...". Tabular Editor intentará conectarse mediante el proveedor de datos y las credenciales especificados en el Data source. Si la conexión se establece correctamente, deberías ver una lista de todas las bases de datos, tablas y vistas accesibles a través del Data source:

![image](https://user-images.githubusercontent.com/8976200/49701892-35ea3900-fbf2-11e8-951a-8858179426c6.png)

Al hacer clic en una tabla o vista en el lado izquierdo, se mostrará una vista previa de los datos a la derecha. Puedes desmarcar las columnas que no quieras incluir, aunque [la práctica recomendada de importación de datos](https://www.sqlbi.com/articles/data-import-best-practices-in-power-bi/) sugiere usar siempre vistas e incluir en esas vistas solo las columnas necesarias en el modelo tabular. La interfaz de usuario te mostrará la consulta SQL resultante. De forma predeterminada, Tabular Editor importará una tabla/vista usando `SELECT * FROM ...`, pero si activas o desactivas cualquier columna en la vista previa, la consulta resultante incluirá una lista explícita de columnas. Para volver a `SELECT * FROM ...`, marca la casilla "Seleccionar todas las columnas" en la esquina superior derecha.

Puedes seleccionar varias tablas/vistas para importarlas a la vez. Cuando hagas clic en "Importar", todas las tablas/vistas seleccionadas se importarán como nuevas tablas, con todas las columnas rellenadas a partir de los metadatos. Se creará una sola partición en cada tabla, que contendrá la consulta SQL resultante de la interfaz de usuario.

¡Listo! Se acabó ir y venir entre Tabular Editor y SSDT.

## Una nota sobre los Data sources heredados frente a los orígenes de datos estructurados

Como actualmente no hay forma de que Tabular Editor infiera los metadatos devueltos por las expresiones M (Power Query), esta interfaz de usuario solo admite Data sources heredados (también llamados Provider). Si necesitas usar orígenes de datos estructurados, aún puedes usar una conexión heredada temporal para importar inicialmente el esquema de la tabla (siempre que se pueda acceder a tu Data source mediante SQL, OLE DB u ODBC) y, después, cambiar manualmente las particiones de las tablas importadas para que usen los orígenes de datos estructurados. Si estás importando datos desde Data sources "poco habituales", como servicios web, Azure Data Lake Storage, etc., los metadatos del esquema no se pueden importar automáticamente, pero [hay una opción para proporcionar la información de metadatos a través del portapapeles](/Importing-Tables#power-query-data-sources).

En general, sin embargo, se recomienda usar siempre una conexión Legacy para los siguientes tipos de orígenes:

- Bases de datos de SQL Server
- Bases de datos de Azure SQL
- Azure SQL Data Warehouse
- Azure Databricks (mediante ODBC)
- Cualquier Data source relacional OLE DB
- Cualquier origen ODBC relacional

Para la autenticación con Azure Active Directory y MFA, consulta aquí.

## Importar sin un Data source preexistente

Si tu modelo aún no contiene ningún Data source, puedes importar tablas yendo al menú "Model" y haciendo clic en "Import Tables...". La IU resultante se ve así:

![image](https://user-images.githubusercontent.com/8976200/49702141-74cdbe00-fbf5-11e8-8a88-5bc2a0a6c80d.png)

Si dejas la selección en "Create a new Data source and add it to the model", al hacer clic en "Next" se mostrará el cuadro de diálogo de conexión. Este cuadro de diálogo te permite especificar los detalles de la conexión:

![image](https://user-images.githubusercontent.com/8976200/49702167-a5adf300-fbf5-11e8-8d06-d6670ad456d4.png)

Al hacer clic en "OK", se creará en tu modelo un Data source (Legacy) con la conexión especificada y se te llevará a la página de importación mostrada arriba.

La siguiente opción de la lista, "Use a temporary connection", no hará que se agregue un nuevo Data source al modelo. Esto significa que eres responsable de asignar un Data source a las particiones de la tabla recién importada antes de implementar el modelo.

La última opción, "Manually import metadata from another application", se usa cuando quieres importar una nueva tabla a partir de una lista de metadatos de columnas. Esto resulta útil para Data sources estructurados (Power Query); [consulta a continuación](/Importing-Tables#power-query-data-sources).

## Capacidades de SQL

Para los Data sources que no sean de SQL Server (o, más precisamente, los Data sources que no usan el controlador Native SQL Client), presta atención a los dos menús desplegables cerca de la parte inferior de la pantalla:

![image](https://user-images.githubusercontent.com/8976200/51613859-b952b600-1f24-11e9-8fd7-7c5269aaab26.png)

El menú desplegable "Reduce rows using" te permite especificar qué cláusula de reducción de filas se debe usar al consultar el origen para obtener datos de vista previa, ya que el Asistente de importación de tablas solo recuperará 200 filas de datos de la tabla o vista de origen. Puedes elegir entre las cláusulas de reducción de filas más comunes, como "TOP", "LIMIT", "FETCH FIRST", etc.

El menú desplegable "Comillas de identificador" te permite especificar cómo deben ir entrecomillados los nombres de los objetos (columnas, tablas) en las instrucciones SQL generadas. Esto se aplica tanto a la vista previa de los datos como a la sentencia SQL utilizada en la consulta de partición de la tabla cuando esta se importa en el modelo tabular. De forma predeterminada, se usan corchetes, pero puedes cambiarlo a otros tipos habituales de comillas de identificador.

## Cambiar el origen de una tabla

Otra forma de abrir la página de importación es hacer clic con el botón derecho en una tabla existente (que use un Data source heredado) y elegir "Seleccionar columnas...". Si esa tabla se importó previamente mediante la interfaz de usuario, la página de importación debería mostrarse con la tabla/vista de origen y las columnas importadas ya preseleccionadas. Puedes agregar o quitar columnas, o incluso elegir una tabla completamente distinta para importarla en lugar de la tabla que seleccionaste en tu modelo. Ten en cuenta que cualquier columna de tu tabla que hayas desmarcado o que ya no exista en la tabla/vista de origen se eliminará de tu modelo. Siempre puedes deshacer operaciones como esta con CTRL+Z.

<a name="refreshing-table-metadata"></a>

## Actualizar los metadatos de la tabla

Desde la versión 2,8, Tabular Editor incorpora una nueva función en la interfaz de usuario que te permite comprobar fácilmente la deriva del esquema. Es decir, permite detectar columnas cuyo tipo de datos haya cambiado o que se hayan añadido o eliminado en las tablas y vistas de origen. Esta comprobación puede ejecutarse a nivel de modelo (de nuevo, esto solo se aplica a Legacy Data Sources), a nivel de Data source, a nivel de tabla o a nivel de partición. Para ello, haz clic con el botón derecho en el objeto y elige "Actualizar metadatos de la tabla..."

![image](https://user-images.githubusercontent.com/8976200/49702346-7e582580-fbf7-11e8-9a62-04c6963179e5.png)

Los cambios se detectan en función de las propiedades "Columna de origen" y "Tipo de datos" de todas las columnas de datos en las tablas correspondientes. Si se detecta algún cambio, Tabular Editor mostrará la interfaz anterior, detallando los cambios. Puedes desmarcar los cambios que no quieras aplicar al modelo, aunque ten en cuenta que algunos cambios pueden provocar errores de procesamiento (por ejemplo, columnas de origen que no existen en la tabla/vista/consulta de origen).

Este mecanismo (al igual que la interfaz de Importar tabla) usa el indicador FormatOnly al consultar los metadatos del origen. Esto significa que puedes tener particiones de tabla que usen procedimientos almacenados. El indicador FormatOnly-flag garantiza que el procedimiento almacenado nunca se ejecute directamente. En su lugar, el servidor realiza un análisis estático para devolver solo los metadatos que describen el conjunto de resultados que devolvería el procedimiento almacenado al ejecutarse. Según el RDBMS que utilices, el indicador FormatOnly puede tener algunas limitaciones cuando se usa con procedimientos almacenados. Para más información sobre este tema al usar SQL Server como Data source, consulta [este artículo](https://docs.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-describe-first-result-set-transact-sql?view=sql-server-2017#remarks).

### Soporte para la CLI

Puedes realizar una comprobación de esquema a nivel de modelo desde la línea de comandos con la opción `-SC`. Ten en cuenta que la comprobación del esquema, cuando se ejecuta a través de la CLI, solo generará un Report de problemas de asignación. No realizará ningún cambio en tu modelo. Esto resulta útil si usas Tabular Editor en canalizaciones de CI/CD, ya que los problemas de asignación podrían ocasionar problemas después de desplegar tu modelo en un entorno de prueba/producción.

<a name="ignoring-objects"></a>

### Omitir objetos

A partir de Tabular Editor 2.9.8, puedes excluir objetos de las comprobaciones de esquema o de la actualización de metadatos. Esto se controla estableciendo una anotación en los objetos que quieras omitir. Como nombre de la anotación, usa los códigos que se indican a continuación. Puedes dejar el valor de la anotación en blanco o establecerlo en "1", "true" o "yes". Si estableces el valor de la anotación en "0", "false" o "no", la anotación quedará deshabilitada en la práctica, como si no existiera:

**Banderas de columna:**

- `TabularEditor_SkipSchemaCheck`: Hace que Tabular Editor omita por completo la comprobación de esquema en esta tabla.
- `TabularEditor_IgnoreMissingSourceColumn`: Tabular Editor ignorará la ausencia aparente de la columna de origen para esta columna concreta.
- `TabularEditor_IgnoreDataTypeChange`: Tabular Editor ignorará los tipos de datos que no coincidan en cualquier columna de la tabla.
- `TabularEditor_IgnoreMissingSourceColumn`: Tabular Editor ignorará las columnas importadas cuya columna de origen aparentemente no exista en el origen.

**Banderas de tabla:**

- `TabularEditor_IgnoreDataTypeChange`: Tabular Editor ignorará el tipo de datos que no coincida en esta columna concreta.
- `TabularEditor_IgnoreSourceColumnAdded`: Tabular Editor ignorará las columnas adicionales que no estén asignadas a ninguna columna de la tabla.

Las banderas afectan a la comprobación de esquema tanto en la UI como en la CLI.

### Tratar las advertencias como errores

De forma predeterminada, la CLI emitirá un Report de error cuando no se haya podido ejecutar una consulta de partición o cuando la tabla importada contenga una columna que no coincida con ninguna columna de la consulta de origen. La CLI generará un Report de advertencia cuando el tipo de datos de una columna no coincida con el de la columna en la consulta de origen, o si la consulta de origen contiene columnas que no estén asignadas a ninguna columna de la tabla importada. La CLI también generará un Report de advertencia cuando las consultas de origen de distintas particiones de la misma tabla no devuelvan las mismas columnas.

A partir de la versión 2.14.1 de Tabular Editor, puedes cambiar el comportamiento de la CLI para que todas las advertencias indicadas anteriormente aparezcan en el Report como errores. Para hacerlo, añade la siguiente anotación a nivel de **modelo**:

- `TabularEditor_SchemaCheckNoWarnings`: Hace que Tabular Editor trate todas las advertencias de comprobación de esquema como errores.

## Azure Active Directory con MFA

Si quieres importar tablas desde una base de datos Azure SQL o desde un pool de SQL de Azure Synapse, probablemente necesites la autenticación multifactor de Azure Active Directory. Lamentablemente, el proveedor SQL Native Client usado en .NET Framework no admite esto. En su lugar, usa el proveedor MSOLEDBSQL (con la ventaja adicional de que, por lo general, es más rápido que el cliente nativo cuando Analysis Services lee datos de la tabla). Asegúrate de tener instalada la [última versión (x86)](https://docs.microsoft.com/en-us/sql/connect/oledb/download-oledb-driver-for-sql-server?view=sql-server-ver15) de este controlador para que funcione en tu equipo local.

Aquí tienes instrucciones paso a paso para configurar el Data source y que funcione con MFA:

1. Crea un nuevo Data source heredado y agrégalo a tu modelo. Model > New Data Source (Legacy)
2. Especifica `System.Data.OleDb` como valor de la propiedad Provider y utiliza una cadena de conexión como la siguiente, sustituyendo los nombres correctos del servidor, la base de datos y el usuario:

### Para bases de datos de Azure SQL:

```
Provider=MSOLEDBSQL;Data Source=<synapse workspace name>-ondemand.sql.azuresynapse.net;User ID=daniel@adventureworks.com;Database=<database name>;Authentication=ActiveDirectoryInteractive
```

### Para pools de SQL de Synapse:

```
Provider=MSOLEDBSQL;Data Source=<sql server name>.database.windows.net;User ID=daniel@adventureworks.com;Database=<database name>;Authentication=ActiveDirectoryInteractive
```

3. Para importar tablas desde este origen, haz clic con el botón derecho en el Data source y elige "Import Tables...". Debería aparecer la interfaz del Import Table Wizard, mostrando una lista de tablas/vistas del origen. Ten en cuenta que, para pools de SQL de Synapse, puede que tengas que especificar "TOP (without NOLOCK)" como cláusula de filas para que la vista previa de los datos funcione.
4. Al implementar tu modelo en Analysis Services, lo más probable es que necesites especificar otras credenciales, como el ID de aplicación y el secreto de una entidad de servicio (Service Principal) o una cuenta de SQL, para que Analysis Services pueda autenticarse frente al origen al actualizar los datos de la tabla. Puedes especificarlo mediante TMSL o SSMS después de la implementación, o bien configurarlo como [parte de tu canalización de implementación de CI/CD](https://tabulareditor.com/blog/youre-deploying-it-wrong-as-edition-part-5#creating-your-first-release-pipeline).

## Importar manualmente el esquema y los metadatos

Si estás usando un Data source que no es compatible con el Import Tables Wizard, tienes la opción de importar los metadatos manualmente. Esta opción ofrece una interfaz en la que puedes escribir o pegar un esquema de tabla en el lado izquierdo, que se analizará automáticamente para obtener el nombre de las columnas y la información de tipo de datos. Como alternativa, puedes escribir manualmente cada nombre de columna en el lado derecho y elegir un tipo de datos en la lista desplegable. En cualquier caso, es más rápido que crear una tabla manualmente y agregar columnas de datos individuales desde la interfaz principal. Cuando termines, haz clic en "Import!", y ajusta el nombre de la tabla y la expresión de partición.

Al analizar el texto del lado izquierdo, Tabular Editor busca ciertas palabras clave para determinar cómo está estructurada la información. Es bastante tolerante al interpretar los datos; por ejemplo, puedes pegar una lista de columnas de un script SQL CREATE TABLE o la salida de la función de Power Query `Table.Schema(...)`, tal como se describe a continuación. El único requisito es que cada línea de texto represente una columna de los datos de origen.

![image](https://user-images.githubusercontent.com/8976200/70419758-6f07f400-1a66-11ea-838d-9a587c8021ca.png)

## Data sources de Power Query

Como no existe una forma oficialmente admitida de ejecutar o validar una expresión de Power Query/M, Tabular Editor solo ofrece compatibilidad limitada con los Data sources de Power Query. A partir de la versión 2.9.0, puedes usar la opción "Importar metadatos manualmente desde otra aplicación" del Asistente para importar tablas, como se describió anteriormente, para importar un esquema desde una consulta de Power Query en Excel o Power BI Desktop. El flujo de trabajo es el siguiente:

- En primer lugar, asegúrate de que tu modelo contiene un Data source de Power Query. Haz clic con el botón derecho en Data Sources > New Data Source (Power Query). Si vas a cargar datos desde SQL Server, especifica "tds" como protocolo y completa las propiedades Database, Server y AuthenticationKind.
  ![image](https://user-images.githubusercontent.com/8976200/70418811-6dd5c780-1a64-11ea-8332-d074c6b2d5c2.png)
- Para otros tipos de Data sources, puede resultarte más fácil crear el modelo inicial y las primeras tablas en SSDT para averiguar cómo debe configurarse el Data source, y luego usar la técnica que se describe a continuación solo al añadir tablas adicionales.
- Usa Power Query en Excel o Power BI Desktop para conectarte a tus datos de origen y aplicar las transformaciones necesarias.
- En el Editor avanzado de Power Query, añade un paso que use la [función M](https://docs.microsoft.com/en-us/powerquery-m/table-schema) `Table.Schema(...)` sobre el resultado anterior:
  ![image](https://user-images.githubusercontent.com/8976200/70416018-5562ae80-1a5e-11ea-8962-529304ce83f0.png)
- Selecciona toda la vista previa de la salida, cópiala al portapapeles (CTRL+A, CTRL+C) y pégala en el cuadro de texto de esquema/metadatos del Asistente para importar tablas:
  ![image](https://user-images.githubusercontent.com/8976200/70416817-2e0ce100-1a60-11ea-9e2b-430cecf88d0a.png)
- Haz clic en "Import!" y ponle un nombre adecuado a tu tabla.
- Por último, pega en la partición de la tabla recién creada la expresión M original que usaste en Excel/Power BI, la que tenías antes de modificarla con la función `Table.Schema(...)`. Modifica la expresión M para que apunte al origen que especificaste en el primer paso:
  ![image](https://user-images.githubusercontent.com/8976200/70418985-dae95d00-1a64-11ea-8bfb-8dda16c33742.png)
