---
uid: object-properties-data-sources
title: Data source and expression properties
author: Jeroen ter Heerdt
updated: 2026-09-23
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
# Data source and expression properties

<!--
SUMMARY: Reference for the properties of legacy and structured data sources, shared expressions (including M parameters), query groups and data binding hints.
-->

This page covers the objects that describe where a model's data comes from: data sources, shared expressions, query groups and data binding hints. For properties that most objects share, see @object-properties-common. For the partitions that use these objects, see @object-properties-partitions.

A model can connect to its sources in three ways:

- **Legacy (provider) data sources** hold a connection string for an OLE DB, ODBC or managed provider. Legacy partitions run a native query, usually SQL, against them. They work at every compatibility level. See [Provider data source](#provider-data-source).
- **Structured (Power Query) data sources** describe a connection in Power Query terms, such as a protocol and a server. M partitions refer to them by name. Analysis Services only, compatibility level 1400 and higher. See [Structured data source](#structured-data-source).
- **Implicit data sources** are what Power BI and Fabric models use. There is no data source object at all: the M expression of a partition or a shared expression names the source, and Power BI manages the credentials.

See @connectivity and @import-tables for how to create each kind. To see which tables use a legacy or structured data source, run the @script-show-data-source-dependencies script. The Best Practice Analyzer rule @kb.bpa-remove-unused-data-sources flags data sources that no partition or expression refers to.

When you rename a legacy or structured data source, Tabular Editor 3 updates the references to it in the M expressions of shared expressions and M partitions, and in the polling and source expressions of incremental refresh policies. You can't delete a data source while partitions still use it.

## Credentials and saving

Data sources can hold secrets, such as a password in a connection string, a password for an impersonated account or an account key. Tabular Editor 3 handles these as follows:

- **In the Properties view**, passwords are masked. **Password** properties show as dots. In a connection string, the value of a `Password`, `Pwd`, `Secret` or `Key` keyword shows as `********`. If you edit the connection string and leave the `********` in place, Tabular Editor keeps the stored password.
- **When you save the model to a `.bim` file or a folder in the JSON format**, Tabular Editor 3 removes the `password`, `pwd`, `key` and `secret` properties of every data source. It also removes the password keyword (`Password`, `Pwd`, `Secret` or `Key`) from connection strings, both the **Connection String** of a provider data source and the one in the address of a structured data source. This keeps secrets out of source control. When you save to TMDL, Tabular Editor 3 tells the TOM serializer to leave out restricted information, such as passwords.
- **To include secrets anyway**, enable **Include sensitive** under **Tools > Preferences > File Formats** (see @preferences), or in **Model > Serialization options...**, which holds the settings for the current model and takes precedence over the preferences. That isn't recommended.
- **When you deploy with the deployment wizard**, Tabular Editor 3 checks every data source it deploys for a missing secret, for example because the model was loaded from a file without sensitive data. A secret counts as missing when it's empty or `********`. It checks:
  - a provider data source whose **Connection String** has a password keyword,
  - a provider data source with **Impersonation Mode** `ImpersonateAccount`,
  - a structured data source with **AuthenticationKind** `Windows` or `UsernamePassword`, or `Key` for an account key.

  For each missing secret, it asks you for the credentials the server should use for refresh. It stores what you enter, encrypted, as a data source override in the @user-options file, and uses it on the next deployment instead of asking again. It only asks about a connection string password when the password keyword is there: saving without sensitive data removes the whole keyword, so after that you aren't asked for it.
- **To keep the data sources on the target as they are**, for example because each environment connects to its own source, clear [Deploy Data Sources](xref:deployment#deployment-options) in the deployment wizard. Tabular Editor 3 then deploys the target's own data sources again, and runs the same check on them. When the server doesn't return a password or key that one of them needs, the wizard asks you for it. It doesn't store these answers in the user options file, so it asks again on the next deployment.
- **The credentials Tabular Editor itself uses** to browse a source and read its schema, for example in the Import Tables wizard, aren't stored in the model. They're stored per user in the @user-options file. They're separate from the credentials the server uses at refresh time.

In Power BI and Fabric models, credentials are never part of the model. You set them on the semantic model in the Power BI service, or on a Fabric connection (see [Data binding hint](#data-binding-hint)).

Tabular Editor 2 handles secrets in a similar way:

- In the Properties view, **Password** properties show as dots, and the value of a `Password`, `Pwd`, `Secret` or `Key` keyword in a connection string shows as `********`.
- When you save to a `.bim` file or a folder in the JSON format, it removes the same properties and connection string keywords as Tabular Editor 3. When you save to TMDL, it also tells the TOM serializer to leave out restricted information.
- To include secrets anyway, enable **Include sensitive** under **File > Preferences...**. It's on the **Serialization** tab, under **General Serialization Settings**, and on the **Current Model** tab, under **Current Model Serialization Settings**, for the model you have open.

TMDL files don't contain the secrets either. TOM's TMDL serializer, which both Tabular Editor 2 and 3 use, writes every password as `********`, including a password inside a connection string, for example `connectionString: data source=srv;user id=u;password=********`.

## Provider data source

A provider (legacy) data source connects to a source through an OLE DB, ODBC or managed .NET provider, using a connection string. Legacy partitions run a native query against it, for example a SQL `SELECT` statement. This is the only kind of data source available below compatibility level 1400, and it's still common in Analysis Services models because the query runs natively in the source, which makes it fast and predictable.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Object Type](xref:object-properties-common#object-type)

For a data source that wraps a Power BI mashup, **Name** shows the `Location` from the connection string instead of the stored name. The stored name is in **Source ID**. See [Power BI Source Details](#power-bi-source-details).

### Connection Details

#### Account
`Account` · string

The Windows account the server uses to connect to the source when **Impersonation Mode** is `ImpersonateAccount`, for example `CONTOSO\svc-ssas-reader`. Enter the password in **Password**. For the other impersonation modes, leave it empty.

#### Connection String
`ConnectionString` · string

The connection string the server uses to open the connection, for example:

```text
Provider=MSOLEDBSQL;Data Source=myserver;Initial Catalog=AdventureWorks;Integrated Security=SSPI
```

The keywords depend on the provider. Click the ellipsis button to edit the connection string in a dialog. When **Provider** is `System.Data.SqlClient` or `Microsoft.Data.SqlClient`, Tabular Editor 3 opens its SQL Server connection dialog. Otherwise, it opens the OLE DB Data Link dialog. A password in the connection string is masked in the Properties view and removed when you save to file. See [Credentials and saving](#credentials-and-saving).

The connection string is the server's connection, not Tabular Editor's. When you import tables or update the table schema, Tabular Editor can use its own local connection details instead. See @import-tables.

To point a model to a different server per environment, change the connection string with a C# script or the command line before deploying, or clear **Deploy Data Sources** in the deployment wizard so the target keeps its own. See @deployment. In Tabular Editor 3, a data source override in the @user-options file gives your workspace database different connection details from the ones in the model.

The Best Practice Analyzer rule @kb.bpa-specify-application-name flags SQL Server connection strings without an `Application Name`. With an application name, database administrators can tell which queries come from the model.

#### Impersonation Mode
`ImpersonationMode` · ImpersonationMode

Which Windows identity the server uses to connect to the source during refresh. This only matters for providers that use Windows authentication. With SQL authentication in the connection string, the user name and password in the connection string are used instead.

| Value | Meaning |
|---|---|
| `ImpersonateServiceAccount` | The account the Analysis Services service runs as. Simple, but that account then needs read access to every source. |
| `ImpersonateAccount` | A specific Windows account, set in **Account** and **Password**. Use this to give the model its own, least-privilege account. |
| `ImpersonateCurrentUser` | The identity of the user who sends the query. Only applies to DirectQuery, where each query goes to the source. Azure Analysis Services doesn't support it for on-premises sources. |
| `ImpersonateAnonymous` | An anonymous connection, without a Windows identity. The Microsoft TOM reference lists this mode as not supported. |
| `ImpersonateUnattendedAccount` | An unattended account that's preconfigured on the server. |
| `Default` | No explicit mode: the server uses the impersonation setting it inherits from the database. When Tabular Editor loads a provider data source with `Default`, it sets it to `ImpersonateServiceAccount`. |

In Azure Analysis Services, most sources use SQL or Microsoft Entra authentication in the connection string, so impersonation matters less. See [Impersonation in Analysis Services tabular models](https://learn.microsoft.com/analysis-services/tabular-models/impersonation-ssas-tabular) for which options each environment supports.

#### Isolation
`Isolation` · DatasourceIsolation

The transaction isolation level the server uses when it runs queries against a relational source.

| Value | Meaning |
|---|---|
| `ReadCommitted` | Only reads data from committed transactions. This is the default. |
| `Snapshot` | Reads a transactionally consistent snapshot of the data, as it was when the query started. Other transactions don't block the query. The source database must allow snapshot isolation. |

Use `Snapshot` when refreshes compete with a busy ETL process on the same database and you want each partition to see a consistent state.

#### Password
`Password` · string

The password of the Windows account in **Account**, used when **Impersonation Mode** is `ImpersonateAccount`. The Properties view masks it, and Tabular Editor 3 doesn't save it to file unless you include sensitive data. See [Credentials and saving](#credentials-and-saving).

When **Impersonation Mode** is `ImpersonateAccount` and the password is missing, the deployment wizard of Tabular Editor 3 asks for it.

#### Provider
`Provider` · string

The name of the managed .NET data provider, for example `System.Data.SqlClient`. Leave it empty for OLE DB providers: for those, the provider is named with the `Provider=` keyword in the connection string.

When you import tables from SQL Server or a Fabric SQL endpoint into a legacy data source, Tabular Editor 3 sets **Provider** to `System.Data.SqlClient`. For ODBC and Oracle, it leaves **Provider** empty and starts the connection string with `Provider=MSDASQL` or `Provider=OraOLEDB.Oracle`. **Provider** also decides which dialog the ellipsis button on **Connection String** opens.

<!-- TODO (not verifiable from TE3 source): list which managed provider names Analysis Services accepts in Provider, besides System.Data.SqlClient. -->

Analysis Services supports fewer OLE DB providers than Windows does, so a provider that connects in Tabular Editor 3 can still fail when the server refreshes. See @connect-oledb.

#### Timeout
`Timeout` · int

The time, in seconds, that the server waits for a command against the source before it gives up. Increase it for slow sources or large partitions whose queries take long to return their first rows.

A new data source has a **Timeout** of `0`.

<!-- TODO (not verifiable from TE3 source): whether a Timeout of 0 means no timeout or the server's default timeout. SSAS 2025 accepts any value on save without validation, so this needs a slow source to observe. -->

### Options

#### Max Connections
`MaxConnections` · int

The maximum number of connections the server opens to this source at the same time. During a refresh, the server can process several partitions in parallel, one connection each. Lower the value to protect a source that can't handle many concurrent queries. Raise it to refresh more partitions in parallel.

Set it to `-1` to use the model's [Data Source Default Max Connections](xref:object-properties-model#data-source-default-max-connections) instead (compatibility level 1510 and higher).

A new data source has a **Max Connections** of `10`.

<!-- TODO (not verifiable from TE3 source): what the engine does with Max Connections 0 during refresh. SSAS 2025 accepts 0 and negative values on save without validation. -->

#### Type
`Type` · DataSourceType · read-only

The kind of data source: `Provider` for a data source on this section, or `Structured` for a [structured data source](#structured-data-source). It's set when the data source is created.

### Power BI Source Details

These properties only appear when the connection string wraps a Power BI mashup, that is when the `Provider=` keyword in the connection string names a Power BI or Mashup provider, and the `Mashup` or `Extended Properties` keyword holds the Power Query definition as a base64-encoded zip archive. Some older Power BI Desktop models describe their sources this way. Tabular Editor decodes the connection string so you can see the M query behind the data source. For other provider data sources, the Properties view hides this category.

<!-- TODO (not verifiable from TE3 source): which versions of Power BI Desktop, or which scenarios, produce provider data sources with an embedded mashup. -->

#### M Query
`MQuery` · string · *computed* · read-only

The Power Query (M) expression embedded in the connection string, read from the `.m` file inside the archive. It's read-only. To change the query, change it in Power BI Desktop.

#### Source ID
`SourceID` · string · read-only · *shortcut to* the data source's name in TOM

The data source's name as it's stored in the model, typically a generated ID. For these data sources, Tabular Editor shows the more readable location from the connection string as the data source name, and keeps the stored name here.

## Structured data source

A structured data source describes a connection in Power Query terms: a protocol, such as SQL Server or Azure Blob Storage, an address, such as a server and database, and a credential. M partitions and shared expressions refer to it by name, for example:

```m
let
    Source = #"SQL/myserver;AdventureWorks",
    Sales = Source{[Schema = "dbo", Item = "FactInternetSales"]}[Data]
in
    Sales
```

Structured data sources exist in Analysis Services models at compatibility level 1400 and higher. Power BI and Fabric models don't use them: they use implicit data sources instead.

Most of the properties below are shortcuts to a value inside the data source's connection details or credential, which TOM stores as JSON. Only the ones that apply to the **Protocol** are used. For example, a SQL Server source uses **Server** and **Database**, and a file source uses **Path**. The others are left empty.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Object Type](xref:object-properties-common#object-type)

### Basic

#### Protocol
`Protocol` · string

The kind of connection, for example `tds` for SQL Server and Azure SQL, `oracle` for Oracle, `odbc`, `ole-db`, `file` for a local or network file, `azure-blobs` for Azure Blob Storage or `odata` for an OData feed. The protocol decides which of the **Connection Details** and **Credential** properties are used.

It's a free-text value. The TOM `DataSourceProtocol` class lists the names that TOM knows, such as `analysis-services`, `azure-tables`, `db2`, `folder`, `http`, `mysql`, `postgresql`, `sap-hana-sql`, `sharepoint-list` and `teradata`. See [DataSourceProtocol](https://learn.microsoft.com/dotnet/api/microsoft.analysisservices.tabular.datasourceprotocol) for the full list. When you import tables into a structured data source, Tabular Editor 3 uses `tds` for SQL Server and Fabric SQL endpoints, `odbc`, `ole-db` or `oracle`.

### Connection Details

#### Account
`Account` · string

The storage account name, for protocols that connect to an Azure storage account, such as Azure Blob Storage or Azure Table Storage. Together with **Domain**, it forms the address of the account, for example the account `contosodata` and the domain `blob.core.windows.net`.

#### Address
`Address` · Address · read-only

All connection address values of the data source. Click the ellipsis button to edit them in a collection editor, including values that don't have their own shortcut property. The properties below, such as **Server** and **Database**, are shortcuts to individual values in the address.

<!-- TODO (not verifiable from TE3 source or the TOM reference, which only names each ConnectionAddress property): which protocols use Model, ContentType, EmailAddress, Object, Property, Resource and View, with an example value for each. The examples below for Model (analysis-services), EmailAddress (Exchange) and Resource (web URL) are unconfirmed. -->

#### Model
`AddressModel` · string

The name of the model, for protocols that connect to a semantic model or cube, such as `analysis-services`.

#### Connection String
`ConnectionString` · string

A connection string, for protocols that take one, such as `odbc` and `ole-db`. For example:

```text
Driver={Snowflake};Server=contoso.snowflakecomputing.com;Warehouse=COMPUTE_WH
```

A password in the connection string is masked in the Properties view and removed when you save to file. See [Credentials and saving](#credentials-and-saving).

#### ContentType
`ContentType` · string

The content type of the source, for protocols that need to know the format of what they read.

#### Database
`Database` · string

The name of the database on the server, for example `AdventureWorks` for the `tds` protocol.

#### Domain
`Domain` · string

The domain part of the address, for example `blob.core.windows.net` for Azure Blob Storage. Used together with **Account**.

#### EmailAddress
`EmailAddress` · string

An email address, for protocols that identify the connection by the user's email address, such as Exchange.

#### Object
`Object` · string

The name of an object in the source, for protocols that address a single object.

#### Path
`Path` · string

The path of a file or folder, for protocols such as `file` and `folder`, for example `\\fileserver\data\sales.csv`. The path must be reachable from the server that refreshes the model, not only from your own machine.

#### Property
`Property` · string

A protocol-specific address value.

#### Query
`Query` · string

A native query, typically SQL, that the connection sends to the source, for example `SELECT * FROM dbo.Customer`. Most models leave this empty and filter in the M expression of the partitions instead.

#### Resource
`Resource` · string

A protocol-specific resource identifier, such as the URL of a web resource.

#### Schema
`Schema` · string

The schema in the database, for protocols that address a schema.

#### Server
`Server` · string

The server to connect to, for example `myserver.database.windows.net` for the `tds` protocol. This is the value you most often change when you deploy the same model to different environments.

#### Url
`Url` · string

The URL of the source, for protocols such as `odata` and `http`, for example `https://services.odata.org/V4/Northwind/Northwind.svc`.

#### View
`View` · string

The name of a view in the source, for protocols that address one.

### Credential

#### AuthenticationKind
`AuthenticationKind` · string

How the server authenticates to the source. Pick a value from the dropdown:

| Value | Meaning |
|---|---|
| `Windows` | A Windows account, set in **Username** and **Password**. |
| `UsernamePassword` | A user name and password that the source itself knows, such as a SQL Server login. The Import Tables wizard of Tabular Editor 3 uses this kind when you choose a specific account. |
| `Key` | An account key, for example for Azure Blob Storage. The key is stored as the `Key` value in **Credential**. |
| `OAuth2` | An OAuth 2.0 token, for example for Microsoft Entra ID sources. |
| `ServiceAccount` | The account the Analysis Services service runs as. |
| `CurrentUser` | The identity of the user who runs the query. |
| `Unattended` | An unattended account that's preconfigured on the server. The Import Tables wizard uses this kind when you choose the unattended account. |
| `Implicit` | No explicit credential. The Import Tables wizard uses this kind when you choose anonymous access. |

The kinds that are valid depend on the **Protocol**. The dropdown doesn't limit you to these values: you can also type a kind. TOM defines four more: `Exchange`, `KerberosS4U`, `SapBasic` and `WebApi`.

When **AuthenticationKind** is `Windows`, `UsernamePassword` or `Key` and the secret is missing, the deployment wizard of Tabular Editor 3 asks for it. See [Credentials and saving](#credentials-and-saving).

<!-- TODO (not verifiable from TE3 source): confirm that CurrentUser on a structured data source, like ImpersonateCurrentUser on a provider data source, only applies to DirectQuery. -->

#### Credential
`Credential` · Credential · read-only

All credential values of the data source. Click the ellipsis button to edit them in a collection editor, including values that don't have their own shortcut property, such as `Key` for an account key. **AuthenticationKind**, **Username**, **Password**, **PrivacySetting** and **EncryptConnection** are shortcuts to individual values in the credential.

Tabular Editor 3 removes secret values, such as a password or a key, when you save to file, unless you include sensitive data. See [Credentials and saving](#credentials-and-saving).

#### EncryptConnection
`EncryptConnection` · bool

When `true`, the connection to the source must be encrypted, for example with TLS. Set it to `false` only for sources that don't support encryption, such as some on-premises servers without a certificate.

#### Password
`Password` · string

The password for **Username**, when **AuthenticationKind** is `Windows` or `UsernamePassword`. The Properties view masks it, and Tabular Editor 3 doesn't save it to file unless you include sensitive data. If the password is missing when you deploy with the deployment wizard, Tabular Editor 3 asks for it, together with **Username** and **PrivacySetting**. See [Credentials and saving](#credentials-and-saving).

Analysis Services doesn't return the password when you connect to a deployed model, so a model you open from a server doesn't have it either. For data sources that you deploy from the model, the wizard remembers what you entered in the @user-options file, so you enter it once per model.

#### PrivacySetting
`PrivacySetting` · string

The Power Query privacy level of the source: `None`, `Public`, `Organizational` or `Private`. Power Query uses privacy levels to decide whether it may send data from one source to another while combining them, for example as a filter value in a query to a second source. An empty value is the same as `None`.

Mismatched privacy levels can stop query folding or make a refresh fail with a firewall error. To ignore privacy levels for the whole model, see **Enable Fast Combine** on @object-properties-model.

In Tabular Editor 3, the **Ignore privacy settings** serialization option in @preferences removes every `PrivacySetting` value from the model when you save it to a `.bim` file or a folder in the JSON format. The value stays in the model you have open. Use this option if you deploy the saved script with an older version of `Microsoft.AnalysisServices.Deployment`, which doesn't support the property.

#### Username
`Username` · string

The user name the server uses to connect, when **AuthenticationKind** is `Windows` or `UsernamePassword`, for example `CONTOSO\svc-reader` or a SQL Server login.

### Options

#### Context Expression
`ContextExpression` · string

Additional information about the structure or metadata of the source, such as content type, content shape and format, according to the Analysis Services tabular protocol specification. The location itself is in the connection details. Most models leave it empty.

#### Max Connections
`MaxConnections` · int

The maximum number of connections the server opens to this source at the same time. Same as **Max Connections** on a [provider data source](#provider-data-source).

#### Options
`Options` · Options · read-only

Protocol-specific connection options. Click the ellipsis button to edit them in a collection editor. Tabular Editor 3 reads each value as JSON when it can, so `true` is stored as a boolean and `{...}` as an object. The available options depend on the **Protocol**.

For example, the `hierarchicalNavigation` option decides whether the source is navigated as a hierarchy: database, then schema, then table. When you import tables from ODBC into a structured data source, Tabular Editor 3 sets it to `true`. When Tabular Editor 3 generates the M expression for an imported table and the option isn't set, it assumes `true` for the `ole-db` protocol and `false` for the others.

#### Type
`Type` · DataSourceType · read-only

The kind of data source: `Structured` for this kind, or `Provider` for a [provider data source](#provider-data-source).

## Shared expression

A shared expression is a named Power Query (M) expression at the model level, which partitions and other shared expressions can refer to by name. Use it for anything you want to define once, for example a connection that several tables share, a helper function or a common transformation step. In Power BI Desktop, every query that isn't loaded into a table becomes a shared expression.

An *M parameter* is a shared expression with a `meta` record that marks it as a parameter, for example:

```m
"myserver.database.windows.net" meta [IsParameterQuery = true, Type = "Text", IsParameterQueryRequired = true]
```

Parameters can be changed in the Power BI service without editing the model, which makes them the usual way to switch a model between environments. In Tabular Editor 3, a refresh override profile can give a parameter a different value for a single refresh, without changing the model. See @refresh-overrides. Incremental refresh needs two parameters, `RangeStart` and `RangeEnd`, and @incremental-refresh-setup shows how to create them. In a Direct Lake model, a shared expression holds the connection to the lakehouse or warehouse (see **Expression Source** on @object-properties-partitions).

Shared expressions need compatibility level 1400 or higher. See @how-to-work-with-expressions, @script-create-m-parameter and @script-create-and-replace-parameter.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Object Type](xref:object-properties-common#object-type)
- [Lineage Tag](xref:object-properties-common#lineage-tag)
- [Source Lineage Tag](xref:object-properties-common#source-lineage-tag)

### Options

#### Expression
`Expression` · string

The M expression. Edit it in the Expression Editor. Other expressions refer to it by the shared expression's name, for example `Source = ServerName` or, for names with spaces, `Source = #"Server Name"`.

When you rename a shared expression, Tabular Editor 3 doesn't update the M expressions that refer to it. Update them yourself, for example with find and replace. Renaming a data source is different: that does update the M expressions.

#### Expression Source
`ExpressionSource` · NamedExpression · compatibility level 1570+

In a composite model that uses DirectQuery over another semantic model: the shared expression that holds the connection to that remote model. It's set together with **Remote Parameter Name** on a shared expression that stands for a parameter of the remote model. When you delete the shared expression it points to, Tabular Editor clears **Expression Source**.

<!-- TODO (not verifiable from TE3 source; the TOM reference only says "A reference to the NamedExpression where the parameter associated with the remote model"): confirm the scenario for Expression Source and Remote Parameter Name on shared expressions, that is, proxy parameters for a remote model in a composite model. -->

#### Kind
`Kind` · ExpressionKind

The language of the expression. The only value is `M`, for Power Query. Tabular Editor sets it when it creates the shared expression.

#### M Attributes
`MAttributes` · string · compatibility level 1535+

The `meta` record of an M parameter, stored separately from the expression, for example `[IsParameterQuery = true, Type = "Text", IsParameterQueryRequired = true]`. Power BI Desktop uses it to recognize the shared expression as a parameter and to show its type and allowed values.

Power BI Desktop doesn't use this property for parameters. It keeps the parameter's metadata record at the end of **Expression**, for example `#datetime(2026, 1, 1, 0, 0, 0) meta [IsParameterQuery=true, Type="DateTime", IsParameterQueryRequired=true]`, and leaves **M Attributes** empty.

<!-- TODO (not verifiable from TE3 source): what happens when both M Attributes and a meta record in Expression are set. -->

#### Parameter Values Column
`ParameterValuesColumn` · Column · compatibility level 1545+

Binds an M parameter to a column, so that report filters on that column change the parameter's value. This is the feature Power BI calls *dynamic M query parameters*: when a user selects a value in a slicer on the column, the value is passed to the parameter, and the DirectQuery source query uses it.

Setting this property also means you allow DAX queries to override the parameter. The column's data type must match the `Type` in the parameter's `meta` record. The column is usually in a small, disconnected table that lists the allowed values.

Only use it on parameters that your source queries handle safely, since the value comes from the report user.

#### Query Group
`QueryGroup` · QueryGroup · compatibility level 1480+

The query group (folder) the shared expression appears in, in the Power Query editor of Power BI Desktop. Power BI Desktop, for example, puts parameters in a group named `Parameters`. See the query group section below.

#### Remote Parameter Name
`RemoteParameterName` · string · compatibility level 1570+

In a composite model that uses DirectQuery over another semantic model: the name of the parameter in the remote model that this shared expression stands for. TOM describes it as applicable only to a proxy model. Empty for ordinary shared expressions.

## Query group

A query group is a folder for queries in the Power Query editor of Power BI Desktop. Shared expressions and M partitions can each belong to a query group. Query groups only organize the Power Query editor. They don't affect refresh, DAX or the field list, and Analysis Services ignores them.

Query groups need compatibility level 1480 or higher. When you delete a query group, Tabular Editor removes it from the shared expressions and partitions that used it.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Annotations](xref:object-properties-common#annotations)

### Options

#### Folder
`Folder` · string

The path of the query group, for example `Parameters`, or `Staging\Sales` for a group inside another group. The name of a query group is the same as its folder: changing one changes the other.

Power BI Desktop separates nested query groups with a backslash, and writes a query group for each level. For a group `Dates` inside a group `Staging`, the model contains the query groups `Staging` and `Staging\Dates`, and the queries in the inner group have **Query Group** `Staging\Dates`.

## Data binding hint

A data binding hint tells Fabric which data connection to use for a data source reference in the model. For example, when you deploy a model to a Fabric workspace, a binding hint can say that the model's connection to a SQL server should use a specific cloud connection or gateway connection in Fabric, instead of you binding it by hand in the semantic model's settings.

It's a *hint*: Fabric ignores it when the data source is already bound, or when the data connection doesn't exist in Fabric.

Data binding hints need compatibility level 1608 or higher. You add and edit them in the [Binding Info Collection](xref:object-properties-model#binding-info-collection) property of the model.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Object Type](xref:object-properties-common#object-type)

<!-- TODO (not verifiable from TE3 source or the TOM reference): how Fabric matches a data binding hint to a data source reference in the model (by Name?), and where users find the connection ID in Fabric (settings of the connection under Manage connections and gateways?). -->

### Options

#### Connection Id
`ConnectionId` · string

The ID of the Fabric data connection to bind to, usually a GUID. You find it in the settings of the connection under **Manage connections and gateways** in Fabric.

#### Type
`Type` · BindingInfoType

The kind of binding information.

| Value | Meaning |
|---|---|
| `DataBindingHint` | A hint to bind a data source reference to a Fabric data connection. This is the only kind in use. |
| `Unknown` | The kind isn't set. |

Tabular Editor sets it for you and doesn't let you change it.
