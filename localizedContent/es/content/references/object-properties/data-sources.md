---
uid: object-properties-data-sources
title: Propiedades de los Data sources y de las expresiones
author: Jeroen ter Heerdt
updated: 2026-10-09
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Propiedades de los Data sources y de las expresiones

<!--
SUMMARY: Reference for the properties of legacy and structured data sources, shared expressions (including M parameters), query groups and data binding hints.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

Esta página describe los objetos que indican de dónde provienen los datos de un modelo: Data sources, expresiones compartidas, Query Groups y sugerencias de enlace de datos. Para las propiedades que comparten la mayoría de los objetos, consulta @object-properties-common. Para las particiones que usan estos objetos, consulta @object-properties-partitions.

Un modelo se conecta a sus orígenes mediante uno de estos tipos de Data source:

- **Los Data sources heredados (de proveedor)** contienen una cadena de conexión para un proveedor OLE DB, ODBC o administrado. Las particiones heredadas ejecutan una consulta nativa sobre ellos, normalmente SQL. Funcionan en cualquier nivel de compatibilidad. Consulta [origen de datos del proveedor](#provider-data-source).
- **Los Data sources estructurados (Power Query)** describen una conexión en términos de Power Query, como un protocolo y un servidor, y las particiones M hacen referencia a ellos por nombre. Existen en los modelos de Analysis Services con nivel de compatibilidad 1400 y superior. Consulta [origen de datos estructurado](#structured-data-source).
- **Los Data sources implícitos** son los que usan los modelos de Power BI y Fabric. No tienen ningún objeto de Data source: la expresión M de una partición o una expresión compartida nombra el Data source, y Power BI administra las credenciales.

Consulta @connectivity y @import-tables para ver cómo crear cada tipo. El script @script-show-data-source-dependencies enumera las tablas que usan un Data source heredado o un origen de datos estructurado. La regla de Best Practice Analyzer (BPA) @kb.bpa-remove-unused-data-sources marca los Data sources a los que no hace referencia ninguna partición ni expresión.

Al cambiar el nombre de un Data source heredado o de un origen de datos estructurado, Tabular Editor 3 actualiza las referencias a este en las expresiones M de las expresiones compartidas y de las particiones M, así como en las expresiones de sondeo y de origen de las políticas de actualización incremental. No puedes eliminar un Data source mientras las particiones sigan usándolo.

## Credenciales y guardado

Los Data sources pueden contener secretos, como una contraseña en una cadena de conexión, la contraseña de una cuenta suplantada o una clave de cuenta.

En la vista **Properties** de Tabular Editor 2 y 3, las propiedades `Password` se muestran como puntos; y, en una cadena de conexión, el valor asociado a las palabras clave `Password`, `Pwd`, `Secret` o `Key` se muestra como `********`. En Tabular Editor 3, si editas una cadena de conexión y dejas `********` tal cual, la contraseña almacenada permanece en el modelo.

Cuando guardas el modelo en un archivo `.bim` o en una carpeta en formato JSON, Tabular Editor 2 y 3 eliminan las propiedades `password`, `pwd`, `key` y `secret` de cada Data source. También eliminan la palabra clave de contraseña (`Password`, `Pwd`, `Secret` o `Key`) de las cadenas de conexión, tanto la `ConnectionString` de un origen de datos del proveedor como la que aparece en la dirección de un origen de datos estructurado. Así, los secretos quedan fuera del control de versiones.

Al guardar en Tabular Model Definition Language (TMDL), Tabular Editor 2 y 3 configuran el serializador de Tabular Object Model (TOM) para omitir información restringida, como las contraseñas. El serializador de TMDL escribe todas las contraseñas como `********`, incluida una contraseña dentro de una cadena de conexión; por ejemplo, `connectionString: Data source=srv;user id=u;password=********`.

Para incluir secretos en los archivos guardados, habilita **Incluir datos confidenciales** en uno de estos lugares:

- en Tabular Editor 3, en **Herramientas > Preferencias > Formatos de archivo** (consulta @preferences), o en **Modelo > Opciones de serialización...** para el modelo actual, lo cual tiene prioridad sobre las preferencias
- en Tabular Editor 2, en **Archivo > Preferencias...**, en la pestaña **Serialización**, en **Configuración general de serialización**, o, para el modelo abierto, en la pestaña **Modelo actual**, en **Configuración de serialización del modelo actual**

No se recomienda incluir datos confidenciales.

Cuando implementas con el Asistente de implementación de Tabular Editor 3, aparece una solicitud para cada secreto que falte en los Data sources que implementas, por ejemplo, después de cargar el modelo desde un archivo guardado sin datos confidenciales. Se considera que falta un secreto cuando está vacío o es `********`. El asistente contempla estos secretos:

- la palabra clave de contraseña en la `ConnectionString` de un origen de datos del proveedor
- la contraseña de un origen de datos del proveedor con `ImpersonationMode` `ImpersonateAccount`
- el secreto de un origen de datos estructurado con `AuthenticationKind` `Windows`, `UsernamePassword` o `Key` (una clave de cuenta)

Introduce las credenciales que usa el servidor para la actualización. Tabular Editor 3 las almacena cifradas como una anulación del Data source en el archivo @user-options y las usa en implementaciones posteriores sin mostrar ningún aviso. Solo aparece un aviso para la contraseña de una cadena de conexión cuando la palabra clave de contraseña está en la cadena de conexión. Al guardar sin datos confidenciales se elimina toda la palabra clave, así que tras un guardado de este tipo no aparece ningún aviso para ella.

Si desactivas [Implementar orígenes de datos](xref:deployment#deployment-options) en el Asistente de implementación, Tabular Editor 3 vuelve a implementar los propios Data sources del destino, por ejemplo, para mantener un Data source independiente por entorno. Se ejecuta la misma comprobación sobre ellos: cuando el servidor no devuelve una contraseña o una clave que uno de ellos necesita, aparece un aviso. Estas respuestas no se almacenan en el archivo de opciones de usuario, así que el aviso vuelve a aparecer en la siguiente implementación.

Las credenciales que Tabular Editor usa para explorar un origen y leer su esquema, por ejemplo en el asistente **Importar tablas**, se almacenan por cada usuario en el archivo @user-options y no forman parte del modelo. Durante la actualización, el servidor usa las credenciales del Data source.

Los modelos de Power BI y Fabric nunca contienen credenciales. Configúralas en el modelo semántico en el servicio de Power BI o en una conexión de Fabric (consulta [Sugerencia sobre el enlace de datos](#data-binding-hint)).

## Origen de datos del proveedor

Un Data source del proveedor (heredado) se conecta a un origen mediante un proveedor OLE DB, ODBC o .NET administrado, usando una cadena de conexión. Las particiones heredadas ejecutan una consulta nativa contra él, por ejemplo, una instrucción SQL `SELECT`. Es el único tipo de Data source por debajo del nivel de compatibilidad 1400.

### Propiedades comunes

- [Nombre](xref:object-properties-common#name)
- [Descripción](xref:object-properties-common#description)
- [Anotaciones](xref:object-properties-common#annotations)
- [Propiedades extendidas](xref:object-properties-common#extended-properties)
- [Tipo de objeto](xref:object-properties-common#object-type)

Algunos orígenes de datos del proveedor encapsulan un mashup de Power BI: la palabra clave `Provider=` en la cadena de conexión nombra un proveedor de Power BI o Mashup, y la palabra clave `Mashup` o `Extended Properties` contiene la definición de Power Query como un archivo ZIP codificado en base64. Algunos modelos antiguos de Power BI Desktop describen sus orígenes de esta manera. Para estos Data sources, `Name` muestra el valor de `Location` de la cadena de conexión, el nombre guardado se encuentra en [ID de origen](#source-id) y la vista **Propiedades** muestra la categoría **Detalles del origen de Power BI** con la consulta M decodificada. Para otros orígenes de datos del proveedor, la vista **Propiedades** oculta esta categoría.

<!-- TODO (not verifiable from TE3 source): which versions of Power BI Desktop, or which scenarios, produce provider data sources with an embedded mashup. -->

### Account

`Account` · string · Detalles de conexión

La cuenta de Windows que el servidor usa para conectarse al origen cuando `ImpersonationMode` es `ImpersonateAccount`, por ejemplo `CONTOSO\svc-ssas-reader`. Introduce su contraseña en `Password`. Para los demás modos de suplantación, déjalo vacío.

### Cadena de conexión

`ConnectionString` · string · Detalles de conexión

La cadena de conexión que el servidor usa para abrir la conexión. Las palabras clave dependen del proveedor, por ejemplo:

```text
Provider=MSOLEDBSQL;Data Source=myserver;Initial Catalog=AdventureWorks;Integrated Security=SSPI
```

Haz clic en el botón de puntos suspensivos para editar la cadena de conexión en un cuadro de diálogo. Tabular Editor 3 abre su cuadro de diálogo de conexión de SQL Server cuando `Provider` es `System.Data.SqlClient` o `Microsoft.Data.SqlClient`; en caso contrario, abre el cuadro de diálogo de Vínculo de datos OLE DB. La contraseña de una cadena de conexión se enmascara en la vista **Propiedades** y se elimina al guardar en un archivo (consulta [Credenciales y guardado](#credentials-and-saving)).

Al importar tablas o actualizar el esquema de la tabla, Tabular Editor puede conectarse usando sus propios datos de conexión locales (consulta @import-tables).

Para que el modelo apunte a un servidor distinto según el entorno, cambia la cadena de conexión con un C# Script o desde la línea de comandos antes de implementar, o desmarca **Implementar Data Sources** en el Asistente de implementación para conservar los Data sources del destino (consulta @deployment). En Tabular Editor 3, una anulación de Data source en el archivo @user-options hace que la base de datos de tu Workspace tenga sus propios datos de conexión.

La regla BPA @kb.bpa-specify-application-name marca las cadenas de conexión de SQL Server que no incluyen `Application Name`. Con un nombre de aplicación, los administradores de bases de datos pueden identificar qué consultas provienen del modelo.

### Modo de suplantación

`ImpersonationMode` · ImpersonationMode · Detalles de conexión

La identidad de Windows que usa el servidor para conectarse al origen durante la actualización, en los proveedores que usan autenticación de Windows. Con autenticación SQL, el servidor usa el nombre de usuario y la contraseña de la cadena de conexión.

| Valor                          | Significado                                                                                                                                                                                                                                                                   |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ImpersonateServiceAccount`    | La cuenta bajo la que se ejecuta el servicio de Analysis Services. Esa cuenta necesita acceso de lectura a todos los orígenes.                                                                                                                |
| `ImpersonateAccount`           | Una cuenta de Windows específica, definida en `Account` y `Password`.                                                                                                                                                                                         |
| `ImpersonateCurrentUser`       | La identidad del usuario que envía la consulta. Solo se aplica a DirectQuery. Azure Analysis Services no lo admite para orígenes locales.                                                                                     |
| `ImpersonateAnonymous`         | Una conexión anónima sin una identidad de Windows. La referencia de Microsoft TOM enumera este modo como no compatible.                                                                                                                       |
| `ImpersonateUnattendedAccount` | Una cuenta desatendida preconfigurada en el servidor.                                                                                                                                                                                                         |
| `Predeterminado`               | Sin modo explícito. El servidor usa la configuración de suplantación que hereda de la base de datos. Cuando Tabular Editor carga un origen de datos del proveedor con `Default`, lo establece en `ImpersonateServiceAccount`. |

En Azure Analysis Services, la mayoría de los orígenes utiliza autenticación SQL o de Microsoft Entra en la cadena de conexión. Consulta [Suplantación en modelos tabulares de Analysis Services](https://learn.microsoft.com/analysis-services/tabular-models/impersonation-ssas-tabular) para ver las opciones que admite cada entorno.

### Isolation

`Isolation` · DatasourceIsolation · Detalles de la conexión

El nivel de aislamiento de las transacciones de las consultas que el servidor ejecuta contra un origen relacional.

| Valor           | Significado                                                                                                                                                                                                                                                                              |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ReadCommitted` | Lee solo datos de transacciones confirmadas. Es la opción predeterminada.                                                                                                                                                                                |
| `Snapshot`      | Lee una instantánea coherente desde el punto de vista transaccional de los datos tal y como estaban cuando se inició la consulta, sin quedar bloqueada por otras transacciones. La base de datos de origen debe permitir el aislamiento de instantáneas. |

Con `Snapshot`, cada partición ve un estado coherente de los datos mientras un proceso ETL escribe en la misma base de datos.

### Password

`Password` · string · Detalles de la conexión

La contraseña de la cuenta de Windows indicada en `Account`, que se usa cuando `ImpersonationMode` es `ImpersonateAccount`. Está enmascarada en la vista **Properties**, y Tabular Editor 3 no la incluye al guardar en un archivo, a menos que incluyas datos confidenciales (consulta [Credenciales y guardado](#credentials-and-saving)). Si falta al implementar con el Asistente de implementación de Tabular Editor 3, se te pedirá que la introduzcas.

### Proveedor

`Provider` · string · Detalles de la conexión

El nombre del proveedor de datos administrado de .NET, por ejemplo `System.Data.SqlClient`. Para proveedores OLE DB, déjalo en blanco e indica el proveedor con la palabra clave `Provider=` en la cadena de conexión.

Cuando importas tablas desde SQL Server o un punto de conexión SQL de Fabric a un Data source heredado, Tabular Editor 3 establece `Provider` en `System.Data.SqlClient`. Para ODBC y Oracle, deja vacío `Provider` e inicia la cadena de conexión con `Provider=MSDASQL` o `Provider=OraOLEDB.Oracle`.

<!-- TODO (not verifiable from TE3 source): list which managed provider names Analysis Services accepts in Provider, besides System.Data.SqlClient. -->

Analysis Services admite menos proveedores OLE DB que Windows. Un proveedor que se conecta en Tabular Editor 3 falla durante la actualización en el servidor si el servidor no lo admite (consulta @connect-oledb).

### Timeout

`Timeout` · int · Detalles de la conexión

El tiempo, en segundos, que el servidor espera a que se complete un comando contra el origen. Un Data source nuevo tiene un `Timeout` de `0`. Auméntalo para orígenes lentos o particiones grandes cuyas consultas tardan en devolver sus primeras filas.

<!-- TODO (not verifiable from TE3 source): whether a Timeout of 0 means no timeout or the server's default timeout. SSAS 2025 accepts any value on save without validation, so this needs a slow source to observe. -->

### Conexiones máximas

`MaxConnections` · int · Opciones

El número máximo de conexiones que el servidor abre a este origen al mismo tiempo. Durante una actualización, el servidor procesa las particiones en paralelo, una conexión por cada una. Un Data source nuevo tiene un `MaxConnections` de `10`. Reduce el valor para proteger un origen que no puede manejar muchas consultas simultáneas, o auméntalo para actualizar más particiones en paralelo.

Establécelo en `-1` para usar las [conexiones máximas predeterminadas del Data source](xref:object-properties-model#data-source-default-max-connections) del modelo (nivel de compatibilidad 1510 y superior).

<!-- TODO (not verifiable from TE3 source): what the engine does with Max Connections 0 during refresh. SSAS 2025 accepts 0 and negative values on save without validation. -->

### Tipo

`Type` · DataSourceType · Opciones · solo lectura

El tipo de Data source: `Provider` para un origen de datos del proveedor, o `Structured` para un [origen de datos estructurado](#structured-data-source). Se establece cuando se crea el Data source.

### Consulta M

`MQuery` · string · Detalles del origen de Power BI · solo lectura · _calculado_

La expresión de Power Query (M) integrada en la cadena de conexión, leída del archivo `.m` dentro del archivo comprimido. Para cambiar la consulta, cámbiala en Power BI Desktop.

### ID de origen

`SourceID` · string · Detalles del origen de Power BI · solo lectura · _acceso directo al_ nombre del Data source en TOM

El nombre del Data source tal como se almacena en el modelo, normalmente un identificador generado.

## Origen de datos estructurado

Un origen de datos estructurado describe una conexión en términos de Power Query, con un protocolo (como SQL Server o Azure Blob Storage), una dirección (como un servidor y una base de datos) y una credencial. Las particiones de M y las expresiones compartidas hacen referencia a él por su nombre, por ejemplo:

```m
let
    Source = #"SQL/myserver;AdventureWorks",
    Sales = Source{[Schema = "dbo", Item = "FactInternetSales"]}[Data]
in
    Sales
```

Los orígenes de datos estructurados existen en los modelos de Analysis Services con nivel de compatibilidad 1400 o superior. Los modelos de Power BI y Fabric usan Data sources implícitos.

La mayoría de las propiedades siguientes son accesos directos a un valor de los detalles de conexión o de la credencial del Data source, que TOM almacena como JSON. Solo se usan las que se aplican a `Protocol`; por ejemplo, `Server` y `Database` para un origen de SQL Server y `Path` para un origen de archivo. Las demás quedan vacías.

### Propiedades comunes

- [Nombre](xref:object-properties-common#name)
- [Descripción](xref:object-properties-common#description)
- [Anotaciones](xref:object-properties-common#annotations)
- [Propiedades extendidas](xref:object-properties-common#extended-properties)
- [Tipo de objeto](xref:object-properties-common#object-type)

### Protocolo

`Protocol` · string · Básico

El tipo de conexión, por ejemplo `tds` para SQL Server y Azure SQL, `oracle` para Oracle, `odbc`, `ole-db`, `file` para un archivo local o de red, `azure-blobs` para Azure Blob Storage o `odata` para un feed OData. El protocolo determina cuáles de las propiedades de **Detalles de conexión** y **Credencial** se usan.

El valor es texto libre. La clase `DataSourceProtocol` de TOM enumera los nombres que TOM conoce, como `analysis-services`, `azure-tables`, `db2`, `folder`, `http`, `mysql`, `postgresql`, `sap-hana-sql`, `sharepoint-list` y `teradata` (consulta [DataSourceProtocol](https://learn.microsoft.com/dotnet/api/microsoft.analysisservices.tabular.datasourceprotocol) para ver la lista completa). Cuando importas tablas a un origen de datos estructurado, Tabular Editor 3 lo establece en `tds` para SQL Server y los puntos de conexión SQL de Fabric, o en `odbc`, `ole-db` u `oracle`.

### Account

`Account` · string · Detalles de conexión

El nombre de la cuenta de almacenamiento, para los protocolos que se conectan a una cuenta de almacenamiento de Azure, como Azure Blob Storage o Azure Table Storage. Junto con `Domain`, forma la dirección de la cuenta; por ejemplo, la cuenta `contosodata` y el dominio `blob.core.windows.net`.

### Dirección

`Address` · Dirección · Detalles de conexión · solo lectura

Todos los valores de dirección de conexión del Data source. Haz clic en el botón de puntos suspensivos para editarlos en un editor de colecciones, incluidos los valores que no tienen su propia propiedad de acceso directo. Las propiedades siguientes, como `Server` y `Database`, son atajos para acceder a valores individuales dentro de la dirección.

<!-- TODO (not verifiable from TE3 source or the TOM reference, which only names each ConnectionAddress property): which protocols use Model, ContentType, EmailAddress, Object, Property, Resource and View, with an example value for each. The examples below for Model (analysis-services), EmailAddress (Exchange) and Resource (web URL) are unconfirmed. -->

### Modelo

`AddressModel` · string · Detalles de la conexión

El nombre del modelo para protocolos que se conectan a un modelo semántico o a un cubo, como `analysis-services`.

### Cadena de conexión

`ConnectionString` · string · Detalles de la conexión

Una cadena de conexión para protocolos que la admiten, como `odbc` y `ole-db`. Por ejemplo:

```text
Driver={Snowflake};Server=contoso.snowflakecomputing.com;Warehouse=COMPUTE_WH
```

La contraseña incluida en la cadena de conexión se enmascara en la vista **Propiedades** y se elimina al guardar el archivo (consulta [Credenciales y guardado](#credentials-and-saving)).

### Tipo de contenido

`ContentType` · string · Detalles de la conexión

El tipo de contenido del origen, para protocolos que necesitan conocer el formato de lo que leen.

### Base de datos

`Database` · string · Detalles de la conexión

El nombre de la base de datos en el servidor; por ejemplo, `AdventureWorks` para el protocolo `tds`.

### Dominio

`Domain` · string · Detalles de la conexión

La parte del dominio de la dirección; por ejemplo, `blob.core.windows.net` para Azure Blob Storage. Se usa junto con `Account`.

### Dirección de correo electrónico

`EmailAddress` · string · Detalles de la conexión

Una dirección de correo electrónico, para protocolos que identifican la conexión por el correo electrónico del usuario, como Exchange.

### Objeto

`Object` · string · Detalles de la conexión

El nombre de un objeto en el origen, para protocolos que hacen referencia a un único objeto.

### Ruta

`Path` · string · Detalles de la conexión

La ruta de un archivo o carpeta, para protocolos como `file` y `folder`; por ejemplo, `\\fileserver\data\sales.csv`. El servidor que actualiza el modelo debe poder acceder a la ruta.

### Propiedad

`Property` · string · Detalles de la conexión

Un valor de dirección específico del protocolo.

### Query

`Query` · cadena · Detalles de la conexión

Una consulta nativa, normalmente SQL, que la conexión envía al origen, por ejemplo `SELECT * FROM dbo.Customer`. La mayoría de los modelos lo dejan vacío y aplican el filtro en las expresiones M de las particiones.

### Recurso

`Resource` · cadena · Detalles de la conexión

Un identificador de recurso específico del protocolo, como la URL de un recurso web.

### Esquema

`Schema` · cadena · Detalles de la conexión

El esquema de la base de datos, para los protocolos que hacen referencia a un esquema.

### Servidor

`Server` · cadena · Detalles de la conexión

El servidor al que se conecta, por ejemplo `myserver.database.windows.net` para el protocolo `tds`. Es el valor que normalmente cambias al implementar el mismo modelo en otro entorno.

### Url

`Url` · cadena · Detalles de la conexión

La URL del origen, para protocolos como `odata` y `http`, por ejemplo `https://services.odata.org/V4/Northwind/Northwind.svc`.

### Vista

`View` · cadena · Detalles de la conexión

El nombre de una vista en el origen, para los protocolos que permiten especificar una.

### AuthenticationKind

`AuthenticationKind` · cadena · Credencial

Cómo se autentica el servidor con el origen. Elige un valor de la lista desplegable o escribe uno:

| Valor              | Significado                                                                                                                                                                                                                                   |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Windows`          | Una cuenta de Windows, configurada en `Username` y `Password`.                                                                                                                                                                |
| `UsernamePassword` | Un nombre de usuario y una contraseña que el origen reconoce, como un inicio de sesión en SQL Server. El asistente **Importar tablas** de Tabular Editor 3 usa este tipo cuando eliges una cuenta específica. |
| `Clave`            | Una clave de cuenta, por ejemplo, para Azure Blob Storage, almacenada como el valor `Key` en `Credential`.                                                                                                                    |
| `OAuth2`           | Un token de OAuth 2.0, por ejemplo, para fuentes de Microsoft Entra ID.                                                                                                                                       |
| `ServiceAccount`   | La cuenta con la que se ejecuta el servicio de Analysis Services.                                                                                                                                                             |
| `CurrentUser`      | La identidad del usuario que ejecuta la consulta.                                                                                                                                                                             |
| `Unattended`       | Una cuenta desatendida preconfigurada en el servidor. El asistente **Importar tablas** usa este tipo cuando se elige la cuenta desatendida.                                                                   |
| `Implicit`         | Sin credencial explícita. El asistente **Importar tablas** usa este tipo cuando se elige el acceso anónimo.                                                                                                   |

Los tipos válidos dependen de `Protocol`. TOM define cuatro tipos más: `Exchange`, `KerberosS4U`, `SapBasic` y `WebApi`.

Cuando `AuthenticationKind` es `Windows`, `UsernamePassword` o `Key` y falta el secreto, se le pedirá que lo introduzca al implementar con el Asistente de implementación de Tabular Editor 3 (consulta [Credenciales y guardado](#credentials-and-saving)).

<!-- TODO (not verifiable from TE3 source): confirm that CurrentUser on a structured data source, like ImpersonateCurrentUser on a provider data source, only applies to DirectQuery. -->

### Credential

`Credential` · Credential · Credential · de solo lectura

Todos los valores de la credencial del Data source. Haga clic en el botón de puntos suspensivos para editarlos en un editor de colecciones, incluidos los valores sin su propia propiedad de acceso directo, como `Key` para una clave de cuenta. `AuthenticationKind`, `Username`, `Password`, `PrivacySetting` y `EncryptConnection` son accesos directos a valores individuales de la credencial.

Tabular Editor 3 elimina los valores secretos, como una contraseña o una clave, al guardar en un archivo, a menos que se incluyan datos confidenciales (consulta [Credenciales y guardado](#credentials-and-saving)).

### EncryptConnection

`EncryptConnection` · bool · Credential

Cuando es `true`, la conexión al origen debe estar cifrada, por ejemplo con TLS. Configúralo en `false` solo para orígenes que no admitan cifrado, como algunos servidores locales sin un certificado.

### Password

`Password` · string · Credencial

La contraseña de `Username`, cuando `AuthenticationKind` es `Windows` o `UsernamePassword`. Se muestra enmascarada en la vista **Propiedades**, y Tabular Editor 3 la omite al guardar en un archivo, salvo que incluyas datos confidenciales. Si falta la contraseña al implementar con el Asistente de implementación, aparecerá un aviso para que la introduzcas, junto con `Username` y `PrivacySetting` (consulta [Credenciales y guardado](#credentials-and-saving)).

Analysis Services no devuelve la contraseña al conectarte a un modelo implementado, por lo que un modelo que abras desde un servidor no tiene contraseña. Para los Data sources que implementes desde el modelo, Tabular Editor 3 almacena lo que introduzcas en el archivo @user-options, así que solo tienes que introducirlo una vez por modelo.

### PrivacySetting

`PrivacySetting` · string · Credencial

El nivel de privacidad de Power Query del origen: `None`, `Public`, `Organizational` o `Private`. Un valor vacío equivale a `None`. Cuando Power Query combina orígenes, los niveles de privacidad determinan si los datos de un origen pueden pasar a otro, por ejemplo, como valor de filtro en una consulta a un segundo origen. Los niveles de privacidad incompatibles pueden impedir el plegado de consultas o hacer que una actualización falle con un error del firewall.

Para ignorar los niveles de privacidad en todo el modelo, establece [Habilitar combinación rápida](xref:object-properties-model#enable-fast-combine) en el modelo.

En Tabular Editor 3, la opción **Ignorar configuración de privacidad** dentro de las opciones de serialización en @preferences elimina todos los valores de `PrivacySetting` del modelo al guardarlo en un archivo `.bim` o en una carpeta en formato JSON. El modelo que tienes abierto conserva los valores. Usa esta opción si implementas el modelo guardado con una versión anterior de `Microsoft.AnalysisServices.Deployment`, que no admite la propiedad.

### Username

`Username` · string · Credencial

El nombre de usuario que usa el servidor para conectarse, cuando `AuthenticationKind` es `Windows` o `UsernamePassword`, por ejemplo `CONTOSO\\svc-reader` o un inicio de sesión de SQL Server.

### Expresión de contexto

`ContextExpression` · string · Opciones

Información adicional sobre la estructura o los metadatos del origen, como el tipo de contenido, la forma del contenido y el formato, según se definen en la especificación del protocolo tabular de Analysis Services. La propia ubicación está en los detalles de la conexión. La mayoría de los modelos lo dejan vacío.

### Máximo de conexiones

`MaxConnections` · int · Options

El número máximo de conexiones que el servidor abre a este origen al mismo tiempo. Consulta [Máximo de conexiones](#max-connections) en un origen de datos del proveedor.

### Opciones

`Options` · Options · Options · solo lectura

Opciones de conexión específicas del protocolo. Haz clic en el botón de tres puntos para editarlas en un editor de colecciones. Tabular Editor 3 lee cada valor como JSON cuando puede, por lo que `true` se almacena como un valor booleano y `{...}` como un objeto. Las opciones disponibles dependen del `Protocol`.

Por ejemplo, la opción `hierarchicalNavigation` determina si el origen se recorre como una jerarquía de base de datos, esquema y tabla. Cuando importas tablas desde ODBC a un origen de datos estructurado, Tabular Editor 3 la establece en `true`. Si la opción no está establecida cuando Tabular Editor 3 genera la expresión M para una tabla importada, Tabular Editor 3 usa `true` para el protocolo `ole-db` y `false` para los demás.

### Tipo

`Type` · DataSourceType · Options · solo lectura

El tipo de Data source: `Structured` para este tipo, o `Provider` para un [origen de datos del proveedor](#provider-data-source).

## Expresión compartida

Una expresión compartida es una expresión de Power Query (M) con nombre a nivel de modelo, a la que las particiones y otras expresiones compartidas hacen referencia por su nombre; por ejemplo, una conexión que comparten varias tablas, una función auxiliar o un paso de transformación común. En Power BI Desktop, toda consulta que no se carga en una tabla se convierte en una expresión compartida. Las expresiones compartidas requieren un nivel de compatibilidad 1400 o superior.

Un _parámetro M_ es una expresión compartida con un registro `meta` que la marca como parámetro; por ejemplo:

```m
"myserver.database.windows.net" meta [IsParameterQuery = true, Type = "Text", IsParameterQueryRequired = true]
```

Puedes cambiar el valor de un parámetro en el servicio Power BI sin editar el modelo, por ejemplo, para cambiar el modelo de un entorno a otro. En Tabular Editor 3, un perfil de anulación de actualización asigna a un parámetro un valor distinto para una sola actualización y deja el modelo sin cambios (consulta @refresh-overrides). La actualización incremental necesita los parámetros `RangeStart` y `RangeEnd`, y @incremental-refresh-setup muestra cómo crearlos. En un modelo Direct Lake, una expresión compartida contiene la conexión al Lakehouse o al Warehouse (consulta `ExpressionSource` en @object-properties-partitions).

Consulta @how-to-work-with-expressions, @script-create-m-parameter y @script-create-and-replace-parameter.

### Propiedades comunes

- [Nombre](xref:object-properties-common#name)
- [Descripción](xref:object-properties-common#description)
- [Anotaciones](xref:object-properties-common#annotations)
- [Propiedades extendidas](xref:object-properties-common#extended-properties)
- [Tipo de objeto](xref:object-properties-common#object-type)
- [Etiqueta de linaje](xref:object-properties-common#lineage-tag)
- [Etiqueta de linaje de origen](xref:object-properties-common#source-lineage-tag)

### Expresión

`Expression` · cadena · Opciones

La expresión M. Edítala en el **Editor de expresiones**. Otras expresiones hacen referencia a ella por el nombre de la expresión compartida; por ejemplo, `Source = ServerName` o `Source = #"Server Name"` si el nombre tiene espacios.

Cuando cambias el nombre de una expresión compartida, Tabular Editor 3 no actualiza las expresiones M que hacen referencia a ella. Actualízalas manualmente; por ejemplo, con Buscar y reemplazar.

### Origen de la expresión

`ExpressionSource` · NamedExpression · Opciones · nivel de compatibilidad 1570 o superior

En un modelo compuesto que usa DirectQuery sobre otro modelo semántico, la expresión compartida que contiene la conexión a ese modelo remoto. Se establece junto con `RemoteParameterName` en una expresión compartida que representa un parámetro del modelo remoto. Cuando eliminas la expresión compartida a la que apunta, Tabular Editor borra `ExpressionSource`.

<!-- TODO (not verifiable from TE3 source; the TOM reference only says "A reference to the NamedExpression where the parameter associated with the remote model"): confirm the scenario for Expression Source and Remote Parameter Name on shared expressions, that is, proxy parameters for a remote model in a composite model. -->

### Tipo

`Kind` · ExpressionKind · Opciones

El lenguaje de la expresión. El único valor es `M`, para Power Query. Tabular Editor lo establece cuando crea la expresión compartida.

### Atributos M

`MAttributes` · cadena · Opciones · nivel de compatibilidad 1535 o superior

El registro `meta` de un parámetro M, almacenado por separado de la expresión; por ejemplo, `[IsParameterQuery = true, Type = "Text", IsParameterQueryRequired = true]`.

Power BI Desktop deja `MAttributes` vacío. Mantiene el registro de metadatos del parámetro al final de `Expression`, por ejemplo `#datetime(2026, 1, 1, 0, 0, 0) meta [IsParameterQuery=true, Type="DateTime", IsParameterQueryRequired=true]`.

<!-- TODO (not verifiable from TE3 source): what happens when both M Attributes and a meta record in Expression are set. -->

### Columna de valores del parámetro

`ParameterValuesColumn` · Columna · Opciones · nivel de compatibilidad 1545+

Vincula un parámetro M a una columna para que, al aplicar un filtro en esa columna en el Report, se establezca el valor del parámetro. Power BI llama a esto _parámetros dinámicos de consulta M_: cuando un usuario selecciona un valor en una segmentación de datos sobre esa columna, el valor pasa al parámetro y la consulta del origen de DirectQuery lo usa.

Al configurar esta propiedad, se permite que las consultas DAX sobrescriban el parámetro. El tipo de datos de la columna debe coincidir con el valor `Type` del registro `meta` del parámetro. La columna suele estar en una tabla pequeña y desconectada que enumera los valores permitidos.

El valor lo proporciona el usuario del Report, así que vincula solo parámetros que las consultas del origen puedan manejar de forma segura.

### Query Group

`QueryGroup` · QueryGroup · Opciones · nivel de compatibilidad 1480+

El Query Group (carpeta) en el que aparece la expresión compartida, en el editor de Power Query de Power BI Desktop. Por ejemplo, Power BI Desktop coloca los parámetros en un grupo llamado `Parameters`. Consulta la sección de Query Group más abajo.

### Nombre del parámetro remoto

`RemoteParameterName` · cadena · Opciones · nivel de compatibilidad 1570+

En un modelo compuesto que usa DirectQuery sobre otro modelo semántico, el nombre del parámetro en el modelo remoto al que corresponde esta expresión compartida. TOM lo describe como aplicable solo a un modelo proxy. Está vacío en las expresiones compartidas normales.

## Query Group

Un Query Group es una carpeta de consultas en el editor de Power Query de Power BI Desktop. Las expresiones compartidas y las particiones M pueden pertenecer a un Query Group. Los Query Group solo organizan el editor de Power Query: la actualización, DAX y la lista de campos no los usan, y Analysis Services los ignora.

Los Query Group requieren un nivel de compatibilidad 1480 o superior. Cuando se elimina un Query Group, Tabular Editor lo quita de las expresiones compartidas y de las particiones que lo usaban.

### Propiedades comunes

- [Nombre](xref:object-properties-common#name)
- [Descripción](xref:object-properties-common#description)
- [Anotaciones](xref:object-properties-common#annotations)
- [Tipo de objeto](xref:object-properties-common#object-type)

### Carpeta

`Folder` · cadena · Opciones

La ruta del Query Group, por ejemplo `Parameters` o `Staging\\Sales`, para un grupo dentro de otro grupo. El nombre de un Query Group coincide con el de su carpeta; cambiar uno cambia el otro.

Power BI Desktop separa los Query Groups anidados con una barra invertida y crea un Query Group para cada nivel. Para un grupo `Dates` dentro de un grupo `Staging`, el modelo contiene los Query Groups `Staging` y `Staging\\Dates`, y las consultas del grupo interno tienen `QueryGroup` `Staging\\Dates`.

## Sugerencia de vinculación de datos

Una sugerencia de vinculación de datos indica a Fabric qué conexión de datos debe usar para una referencia a un Data source en el modelo. Por ejemplo, cuando implementas un modelo en un Workspace de Fabric, una sugerencia de vinculación vincula la conexión del modelo a un servidor SQL con una conexión en la nube específica o una conexión de Gateway en Fabric, y no es necesario vincularla manualmente en la configuración del modelo semántico.

Fabric ignora la sugerencia cuando el Data source ya está vinculado o cuando la conexión de datos no existe en Fabric.

Las sugerencias de vinculación de datos requieren el nivel de compatibilidad 1608 o superior. Agréguelas y edítelas en la propiedad [Colección de información de vinculación](xref:object-properties-model#binding-info-collection) del modelo.

### Propiedades comunes

- [Nombre](xref:object-properties-common#name)
- [Descripción](xref:object-properties-common#description)
- [Anotaciones](xref:object-properties-common#annotations)
- [Propiedades extendidas](xref:object-properties-common#extended-properties)
- [Tipo de objeto](xref:object-properties-common#object-type)

<!-- TODO (not verifiable from TE3 source or the TOM reference): how Fabric matches a data binding hint to a data source reference in the model (by Name?), and where users find the connection ID in Fabric (settings of the connection under Manage connections and gateways?). -->

### Id. de conexión

`ConnectionId` · cadena · Opciones

El identificador de la conexión de datos de Fabric a la que se va a vincular, normalmente un GUID. Lo encontrarás en la configuración de la conexión, en **Manage connections and Gateways**, en Fabric.

### Tipo

`Type` · BindingInfoType · Opciones · de solo lectura

El tipo de información de enlace.

| Valor             | Significado                                                                                                                                                     |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DataBindingHint` | Una sugerencia para vincular una referencia de Data source a una conexión de datos de Fabric. Este es el único tipo que se usa. |
| `Unknown`         | No se ha establecido el tipo.                                                                                                                   |

Tabular Editor establece el valor y no puedes cambiarlo.
