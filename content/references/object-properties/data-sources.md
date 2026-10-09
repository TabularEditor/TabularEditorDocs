---
uid: object-properties-data-sources
title: Data source and expression properties
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
# Data source and expression properties

<!--
SUMMARY: Reference for the properties of legacy and structured data sources, shared expressions (including M parameters), query groups and data binding hints.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

This page covers the objects that describe where a model's data comes from: data sources, shared expressions, query groups and data binding hints. For properties that most objects share, see @object-properties-common. For the partitions that use these objects, see @object-properties-partitions.

A model connects to its sources through one of these kinds of data source:

- **legacy (provider) data sources** hold a connection string for an OLE DB, ODBC or managed provider. Legacy partitions run a native query against them, usually SQL. They work at every compatibility level. See [Provider data source](#provider-data-source).
- **structured (Power Query) data sources** describe a connection in Power Query terms, such as a protocol and a server, and M partitions refer to them by name. They exist in Analysis Services models at compatibility level 1400 and higher. See [Structured data source](#structured-data-source).
- **implicit data sources** are what Power BI and Fabric models use. They have no data source object: the M expression of a partition or a shared expression names the source, and Power BI manages the credentials.

See @connectivity and @import-tables for how to create each kind. The @script-show-data-source-dependencies script lists the tables that use a legacy or structured data source. The Best Practice Analyzer (BPA) rule @kb.bpa-remove-unused-data-sources flags data sources that no partition or expression refers to.

When you rename a legacy or structured data source, Tabular Editor 3 updates the references to it in the M expressions of shared expressions and M partitions, and in the polling and source expressions of incremental refresh policies. You can't delete a data source while partitions still use it.

## Credentials and saving

Data sources can hold secrets, such as a password in a connection string, the password of an impersonated account or an account key.

In the **Properties** view of Tabular Editor 2 and 3, `Password` properties show as dots, and in a connection string the value of a `Password`, `Pwd`, `Secret` or `Key` keyword shows as `********`. In Tabular Editor 3, if you edit a connection string and leave the `********` in place, the stored password stays in the model.

When you save the model to a `.bim` file or a folder in the JSON format, Tabular Editor 2 and 3 remove the `password`, `pwd`, `key` and `secret` properties of every data source. They also remove the password keyword (`Password`, `Pwd`, `Secret` or `Key`) from connection strings, both the `ConnectionString` of a provider data source and the one in the address of a structured data source. This keeps secrets out of source control.

When you save to Tabular Model Definition Language (TMDL), Tabular Editor 2 and 3 set the Tabular Object Model (TOM) serializer to leave out restricted information, such as passwords. The TMDL serializer writes every password as `********`, including a password inside a connection string, for example `connectionString: data source=srv;user id=u;password=********`.

To include secrets in the saved files, enable **Include sensitive** in one of these places:

- in Tabular Editor 3, under **Tools > Preferences > File Formats** (see @preferences), or in **Model > Serialization options...** for the current model, which takes precedence over the preferences
- in Tabular Editor 2, under **File > Preferences...** on the **Serialization** tab, under **General Serialization Settings**, or for the model you have open on the **Current Model** tab, under **Current Model Serialization Settings**

Including sensitive data isn't recommended.

When you deploy with the deployment wizard of Tabular Editor 3, a prompt appears for each missing secret of the data sources you deploy, for example after you load the model from a file saved without sensitive data. A secret is missing when it's empty or `********`. The wizard covers these secrets:

- the password keyword in the `ConnectionString` of a provider data source
- the password of a provider data source with `ImpersonationMode` `ImpersonateAccount`
- the secret of a structured data source with `AuthenticationKind` `Windows`, `UsernamePassword` or `Key` (an account key)

Enter the credentials the server uses for refresh. Tabular Editor 3 stores them, encrypted, as a data source override in the @user-options file and uses them on later deployments without a prompt. A connection string password only gets a prompt when the password keyword is in the connection string. Saving without sensitive data removes the whole keyword, so after such a save no prompt appears for it.

If you clear [Deploy Data Sources](xref:deployment#deployment-options) in the deployment wizard, Tabular Editor 3 deploys the target's own data sources again, for example to keep a separate source per environment. The same check runs on them: when the server doesn't return a password or key that one of them needs, a prompt appears. These answers aren't stored in the user options file, so the prompt appears again on the next deployment.

The credentials Tabular Editor uses to browse a source and read its schema, for example in the **Import Tables** wizard, are stored per user in the @user-options file and aren't part of the model. At refresh time, the server uses the credentials of the data source.

Power BI and Fabric models never contain credentials. Set them on the semantic model in the Power BI service, or on a Fabric connection (see [Data binding hint](#data-binding-hint)).

## Provider data source

A provider (legacy) data source connects to a source through an OLE DB, ODBC or managed .NET provider, using a connection string. Legacy partitions run a native query against it, for example a SQL `SELECT` statement. It's the only kind of data source below compatibility level 1400.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Object Type](xref:object-properties-common#object-type)

Some provider data sources wrap a Power BI mashup: the `Provider=` keyword in the connection string names a Power BI or Mashup provider, and the `Mashup` or `Extended Properties` keyword holds the Power Query definition as a base64-encoded zip archive. Some older Power BI Desktop models describe their sources this way. For these data sources, `Name` shows the `Location` from the connection string, the stored name is in [Source ID](#source-id), and the **Properties** view shows the **Power BI Source Details** category with the decoded M query. For other provider data sources, the **Properties** view hides this category.

<!-- TODO (not verifiable from TE3 source): which versions of Power BI Desktop, or which scenarios, produce provider data sources with an embedded mashup. -->

### Account
`Account` · string · Connection Details

The Windows account the server uses to connect to the source when `ImpersonationMode` is `ImpersonateAccount`, for example `CONTOSO\svc-ssas-reader`. Enter its password in `Password`. For the other impersonation modes, leave it empty.

### Connection String
`ConnectionString` · string · Connection Details

The connection string the server uses to open the connection. The keywords depend on the provider, for example:

```text
Provider=MSOLEDBSQL;Data Source=myserver;Initial Catalog=AdventureWorks;Integrated Security=SSPI
```

Click the ellipsis button to edit the connection string in a dialog. Tabular Editor 3 opens its SQL Server connection dialog when `Provider` is `System.Data.SqlClient` or `Microsoft.Data.SqlClient`, and the OLE DB Data Link dialog otherwise. A password in the connection string is masked in the **Properties** view and removed when you save to file (see [Credentials and saving](#credentials-and-saving)).

When you import tables or update the table schema, Tabular Editor can connect with its own local connection details (see @import-tables).

To point the model to a different server per environment, change the connection string with a C# script or the command line before you deploy, or clear **Deploy Data Sources** in the deployment wizard to keep the target's data sources (see @deployment). In Tabular Editor 3, a data source override in the @user-options file gives your workspace database its own connection details.

The BPA rule @kb.bpa-specify-application-name flags SQL Server connection strings without an `Application Name`. With an application name, database administrators can tell which queries come from the model.

### Impersonation Mode
`ImpersonationMode` · ImpersonationMode · Connection Details

The Windows identity the server uses to connect to the source during refresh, for providers that use Windows authentication. With SQL authentication, the server uses the user name and password in the connection string.

| Value | Meaning |
|---|---|
| `ImpersonateServiceAccount` | The account the Analysis Services service runs as. That account needs read access to every source. |
| `ImpersonateAccount` | A specific Windows account, set in `Account` and `Password`. |
| `ImpersonateCurrentUser` | The identity of the user who sends the query. Applies to DirectQuery only. Azure Analysis Services doesn't support it for on-premises sources. |
| `ImpersonateAnonymous` | An anonymous connection without a Windows identity. The Microsoft TOM reference lists this mode as not supported. |
| `ImpersonateUnattendedAccount` | An unattended account that's preconfigured on the server. |
| `Default` | No explicit mode. The server uses the impersonation setting it inherits from the database. When Tabular Editor loads a provider data source with `Default`, it sets it to `ImpersonateServiceAccount`. |

In Azure Analysis Services, most sources use SQL or Microsoft Entra authentication in the connection string. See [Impersonation in Analysis Services tabular models](https://learn.microsoft.com/analysis-services/tabular-models/impersonation-ssas-tabular) for the options each environment supports.

### Isolation
`Isolation` · DatasourceIsolation · Connection Details

The transaction isolation level of the queries the server runs against a relational source.

| Value | Meaning |
|---|---|
| `ReadCommitted` | Reads only data from committed transactions. This is the default. |
| `Snapshot` | Reads a transactionally consistent snapshot of the data as it was when the query started, without being blocked by other transactions. The source database must allow snapshot isolation. |

With `Snapshot`, each partition sees a consistent state of the data while an ETL process writes to the same database.

### Password
`Password` · string · Connection Details

The password of the Windows account in `Account`, used when `ImpersonationMode` is `ImpersonateAccount`. It's masked in the **Properties** view, and Tabular Editor 3 leaves it out when you save to file unless you include sensitive data (see [Credentials and saving](#credentials-and-saving)). If it's missing when you deploy with the deployment wizard of Tabular Editor 3, a prompt appears for it.

### Provider
`Provider` · string · Connection Details

The name of the managed .NET data provider, for example `System.Data.SqlClient`. For OLE DB providers, leave it empty and name the provider with the `Provider=` keyword in the connection string.

When you import tables from SQL Server or a Fabric SQL endpoint into a legacy data source, Tabular Editor 3 sets `Provider` to `System.Data.SqlClient`. For ODBC and Oracle, it leaves `Provider` empty and starts the connection string with `Provider=MSDASQL` or `Provider=OraOLEDB.Oracle`.

<!-- TODO (not verifiable from TE3 source): list which managed provider names Analysis Services accepts in Provider, besides System.Data.SqlClient. -->

Analysis Services supports fewer OLE DB providers than Windows does. A provider that connects in Tabular Editor 3 fails at refresh on the server if the server doesn't support it (see @connect-oledb).

### Timeout
`Timeout` · int · Connection Details

The time in seconds that the server waits for a command against the source to complete. A new data source has a `Timeout` of `0`. Increase it for slow sources or large partitions whose queries take long to return their first rows.

<!-- TODO (not verifiable from TE3 source): whether a Timeout of 0 means no timeout or the server's default timeout. SSAS 2025 accepts any value on save without validation, so this needs a slow source to observe. -->

### Max Connections
`MaxConnections` · int · Options

The maximum number of connections the server opens to this source at the same time. During a refresh, the server processes partitions in parallel, one connection each. A new data source has a `MaxConnections` of `10`. Lower the value to protect a source that can't handle many concurrent queries, or raise it to refresh more partitions in parallel.

Set it to `-1` to use the model's [Data Source Default Max Connections](xref:object-properties-model#data-source-default-max-connections) (compatibility level 1510 and higher).

<!-- TODO (not verifiable from TE3 source): what the engine does with Max Connections 0 during refresh. SSAS 2025 accepts 0 and negative values on save without validation. -->

### Type
`Type` · DataSourceType · Options · read-only

The kind of data source: `Provider` for a provider data source, or `Structured` for a [structured data source](#structured-data-source). It's set when the data source is created.

### M Query
`MQuery` · string · Power BI Source Details · read-only · *computed*

The Power Query (M) expression embedded in the connection string, read from the `.m` file inside the archive. To change the query, change it in Power BI Desktop.

### Source ID
`SourceID` · string · Power BI Source Details · read-only · *shortcut to* the data source's name in TOM

The data source's name as it's stored in the model, typically a generated ID.

## Structured data source

A structured data source describes a connection in Power Query terms, with a protocol (such as SQL Server or Azure Blob Storage), an address (such as a server and database) and a credential. M partitions and shared expressions refer to it by name, for example:

```m
let
    Source = #"SQL/myserver;AdventureWorks",
    Sales = Source{[Schema = "dbo", Item = "FactInternetSales"]}[Data]
in
    Sales
```

Structured data sources exist in Analysis Services models at compatibility level 1400 and higher. Power BI and Fabric models use implicit data sources.

Most of the properties below are shortcuts to a value in the data source's connection details or credential, which TOM stores as JSON. Only the ones that apply to the `Protocol` are used, for example `Server` and `Database` for a SQL Server source and `Path` for a file source. The others stay empty.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Object Type](xref:object-properties-common#object-type)

### Protocol
`Protocol` · string · Basic

The kind of connection, for example `tds` for SQL Server and Azure SQL, `oracle` for Oracle, `odbc`, `ole-db`, `file` for a local or network file, `azure-blobs` for Azure Blob Storage or `odata` for an OData feed. The protocol sets which of the **Connection Details** and **Credential** properties are used.

The value is free text. The TOM `DataSourceProtocol` class lists the names TOM knows, such as `analysis-services`, `azure-tables`, `db2`, `folder`, `http`, `mysql`, `postgresql`, `sap-hana-sql`, `sharepoint-list` and `teradata` (see [DataSourceProtocol](https://learn.microsoft.com/dotnet/api/microsoft.analysisservices.tabular.datasourceprotocol) for the full list). When you import tables into a structured data source, Tabular Editor 3 sets it to `tds` for SQL Server and Fabric SQL endpoints, or to `odbc`, `ole-db` or `oracle`.

### Account
`Account` · string · Connection Details

The storage account name, for protocols that connect to an Azure storage account, such as Azure Blob Storage or Azure Table Storage. Together with `Domain`, it forms the address of the account, for example the account `contosodata` and the domain `blob.core.windows.net`.

### Address
`Address` · Address · Connection Details · read-only

All connection address values of the data source. Click the ellipsis button to edit them in a collection editor, including values without their own shortcut property. The properties below, such as `Server` and `Database`, are shortcuts to individual values in the address.

<!-- TODO (not verifiable from TE3 source or the TOM reference, which only names each ConnectionAddress property): which protocols use Model, ContentType, EmailAddress, Object, Property, Resource and View, with an example value for each. The examples below for Model (analysis-services), EmailAddress (Exchange) and Resource (web URL) are unconfirmed. -->

### Model
`AddressModel` · string · Connection Details

The name of the model, for protocols that connect to a semantic model or cube, such as `analysis-services`.

### Connection String
`ConnectionString` · string · Connection Details

A connection string, for protocols that take one, such as `odbc` and `ole-db`. For example:

```text
Driver={Snowflake};Server=contoso.snowflakecomputing.com;Warehouse=COMPUTE_WH
```

A password in the connection string is masked in the **Properties** view and removed when you save to file (see [Credentials and saving](#credentials-and-saving)).

### ContentType
`ContentType` · string · Connection Details

The content type of the source, for protocols that need to know the format of what they read.

### Database
`Database` · string · Connection Details

The name of the database on the server, for example `AdventureWorks` for the `tds` protocol.

### Domain
`Domain` · string · Connection Details

The domain part of the address, for example `blob.core.windows.net` for Azure Blob Storage. It's used together with `Account`.

### EmailAddress
`EmailAddress` · string · Connection Details

An email address, for protocols that identify the connection by the user's email address, such as Exchange.

### Object
`Object` · string · Connection Details

The name of an object in the source, for protocols that address a single object.

### Path
`Path` · string · Connection Details

The path of a file or folder, for protocols such as `file` and `folder`, for example `\\fileserver\data\sales.csv`. The server that refreshes the model must be able to reach the path.

### Property
`Property` · string · Connection Details

A protocol-specific address value.

### Query
`Query` · string · Connection Details

A native query, typically SQL, that the connection sends to the source, for example `SELECT * FROM dbo.Customer`. Most models leave it empty and filter in the M expressions of the partitions.

### Resource
`Resource` · string · Connection Details

A protocol-specific resource identifier, such as the URL of a web resource.

### Schema
`Schema` · string · Connection Details

The schema in the database, for protocols that address a schema.

### Server
`Server` · string · Connection Details

The server to connect to, for example `myserver.database.windows.net` for the `tds` protocol. It's the value you usually change when you deploy the same model to a different environment.

### Url
`Url` · string · Connection Details

The URL of the source, for protocols such as `odata` and `http`, for example `https://services.odata.org/V4/Northwind/Northwind.svc`.

### View
`View` · string · Connection Details

The name of a view in the source, for protocols that address one.

### AuthenticationKind
`AuthenticationKind` · string · Credential

How the server authenticates to the source. Pick a value from the dropdown or type one:

| Value | Meaning |
|---|---|
| `Windows` | A Windows account, set in `Username` and `Password`. |
| `UsernamePassword` | A user name and password that the source knows, such as a SQL Server login. The **Import Tables** wizard of Tabular Editor 3 uses this kind when you choose a specific account. |
| `Key` | An account key, for example for Azure Blob Storage, stored as the `Key` value in `Credential`. |
| `OAuth2` | An OAuth 2.0 token, for example for Microsoft Entra ID sources. |
| `ServiceAccount` | The account the Analysis Services service runs as. |
| `CurrentUser` | The identity of the user who runs the query. |
| `Unattended` | An unattended account that's preconfigured on the server. The **Import Tables** wizard uses this kind when you choose the unattended account. |
| `Implicit` | No explicit credential. The **Import Tables** wizard uses this kind when you choose anonymous access. |

The valid kinds depend on the `Protocol`. TOM defines four more kinds: `Exchange`, `KerberosS4U`, `SapBasic` and `WebApi`.

When `AuthenticationKind` is `Windows`, `UsernamePassword` or `Key` and the secret is missing, a prompt appears for it when you deploy with the deployment wizard of Tabular Editor 3 (see [Credentials and saving](#credentials-and-saving)).

<!-- TODO (not verifiable from TE3 source): confirm that CurrentUser on a structured data source, like ImpersonateCurrentUser on a provider data source, only applies to DirectQuery. -->

### Credential
`Credential` · Credential · Credential · read-only

All credential values of the data source. Click the ellipsis button to edit them in a collection editor, including values without their own shortcut property, such as `Key` for an account key. `AuthenticationKind`, `Username`, `Password`, `PrivacySetting` and `EncryptConnection` are shortcuts to individual values in the credential.

Tabular Editor 3 removes secret values, such as a password or a key, when you save to file, unless you include sensitive data (see [Credentials and saving](#credentials-and-saving)).

### EncryptConnection
`EncryptConnection` · bool · Credential

When `true`, the connection to the source must be encrypted, for example with TLS. Set it to `false` only for sources that don't support encryption, such as some on-premises servers without a certificate.

### Password
`Password` · string · Credential

The password for `Username`, when `AuthenticationKind` is `Windows` or `UsernamePassword`. It's masked in the **Properties** view, and Tabular Editor 3 leaves it out when you save to file unless you include sensitive data. If the password is missing when you deploy with the deployment wizard, a prompt appears for it, together with `Username` and `PrivacySetting` (see [Credentials and saving](#credentials-and-saving)).

Analysis Services doesn't return the password when you connect to a deployed model, so a model you open from a server has no password. For data sources you deploy from the model, Tabular Editor 3 stores what you enter in the @user-options file, so you enter it once per model.

### PrivacySetting
`PrivacySetting` · string · Credential

The Power Query privacy level of the source: `None`, `Public`, `Organizational` or `Private`. An empty value is the same as `None`. When Power Query combines sources, the privacy levels set whether data from one source can go to another, for example as a filter value in a query to a second source. Mismatched privacy levels can stop query folding or make a refresh fail with a firewall error.

To ignore privacy levels for the whole model, set [Enable Fast Combine](xref:object-properties-model#enable-fast-combine) on the model.

In Tabular Editor 3, the **Ignore privacy settings** serialization option in @preferences removes every `PrivacySetting` value from the model when you save it to a `.bim` file or a folder in the JSON format. The model you have open keeps the values. Use this option if you deploy the saved model with an older version of `Microsoft.AnalysisServices.Deployment`, which doesn't support the property.

### Username
`Username` · string · Credential

The user name the server uses to connect, when `AuthenticationKind` is `Windows` or `UsernamePassword`, for example `CONTOSO\svc-reader` or a SQL Server login.

### Context Expression
`ContextExpression` · string · Options

Additional information about the structure or metadata of the source, such as content type, content shape and format, as defined in the Analysis Services tabular protocol specification. The location itself is in the connection details. Most models leave it empty.

### Max Connections
`MaxConnections` · int · Options

The maximum number of connections the server opens to this source at the same time. See [Max Connections](#max-connections) on a provider data source.

### Options
`Options` · Options · Options · read-only

Protocol-specific connection options. Click the ellipsis button to edit them in a collection editor. Tabular Editor 3 reads each value as JSON when it can, so `true` is stored as a boolean and `{...}` as an object. The available options depend on the `Protocol`.

For example, the `hierarchicalNavigation` option sets whether the source is navigated as a hierarchy of database, schema and table. When you import tables from ODBC into a structured data source, Tabular Editor 3 sets it to `true`. If the option isn't set when Tabular Editor 3 generates the M expression for an imported table, Tabular Editor 3 uses `true` for the `ole-db` protocol and `false` for the others.

### Type
`Type` · DataSourceType · Options · read-only

The kind of data source: `Structured` for this kind, or `Provider` for a [provider data source](#provider-data-source).

## Shared expression

A shared expression is a named Power Query (M) expression at the model level that partitions and other shared expressions refer to by name, for example a connection that several tables share, a helper function or a common transformation step. In Power BI Desktop, every query that isn't loaded into a table becomes a shared expression. Shared expressions need compatibility level 1400 or higher.

An *M parameter* is a shared expression with a `meta` record that marks it as a parameter, for example:

```m
"myserver.database.windows.net" meta [IsParameterQuery = true, Type = "Text", IsParameterQueryRequired = true]
```

You can change a parameter's value in the Power BI service without editing the model, for example to switch the model between environments. In Tabular Editor 3, a refresh override profile gives a parameter a different value for a single refresh and leaves the model unchanged (see @refresh-overrides). Incremental refresh needs the parameters `RangeStart` and `RangeEnd`, and @incremental-refresh-setup shows how to create them. In a Direct Lake model, a shared expression holds the connection to the lakehouse or warehouse (see `ExpressionSource` on @object-properties-partitions).

See @how-to-work-with-expressions, @script-create-m-parameter and @script-create-and-replace-parameter.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Object Type](xref:object-properties-common#object-type)
- [Lineage Tag](xref:object-properties-common#lineage-tag)
- [Source Lineage Tag](xref:object-properties-common#source-lineage-tag)

### Expression
`Expression` · string · Options

The M expression. Edit it in the **Expression Editor**. Other expressions refer to it by the shared expression's name, for example `Source = ServerName`, or `Source = #"Server Name"` for a name with spaces.

When you rename a shared expression, Tabular Editor 3 doesn't update the M expressions that refer to it. Update them yourself, for example with find and replace.

### Expression Source
`ExpressionSource` · NamedExpression · Options · compatibility level 1570+

In a composite model that uses DirectQuery over another semantic model, the shared expression that holds the connection to that remote model. It's set together with `RemoteParameterName` on a shared expression that stands for a parameter of the remote model. When you delete the shared expression it points to, Tabular Editor clears `ExpressionSource`.

<!-- TODO (not verifiable from TE3 source; the TOM reference only says "A reference to the NamedExpression where the parameter associated with the remote model"): confirm the scenario for Expression Source and Remote Parameter Name on shared expressions, that is, proxy parameters for a remote model in a composite model. -->

### Kind
`Kind` · ExpressionKind · Options

The language of the expression. The only value is `M`, for Power Query. Tabular Editor sets it when it creates the shared expression.

### M Attributes
`MAttributes` · string · Options · compatibility level 1535+

The `meta` record of an M parameter, stored separately from the expression, for example `[IsParameterQuery = true, Type = "Text", IsParameterQueryRequired = true]`.

Power BI Desktop leaves `MAttributes` empty. It keeps the parameter's metadata record at the end of `Expression`, for example `#datetime(2026, 1, 1, 0, 0, 0) meta [IsParameterQuery=true, Type="DateTime", IsParameterQueryRequired=true]`.

<!-- TODO (not verifiable from TE3 source): what happens when both M Attributes and a meta record in Expression are set. -->

### Parameter Values Column
`ParameterValuesColumn` · Column · Options · compatibility level 1545+

Binds an M parameter to a column, so a report filter on that column sets the parameter's value. Power BI calls this *dynamic M query parameters*: when a user selects a value in a slicer on the column, the value goes to the parameter and the DirectQuery source query uses it.

Setting this property allows DAX queries to override the parameter. The column's data type must match the `Type` in the parameter's `meta` record. The column is usually in a small, disconnected table that lists the allowed values.

The value comes from the report user, so only bind parameters that your source queries handle safely.

### Query Group
`QueryGroup` · QueryGroup · Options · compatibility level 1480+

The query group (folder) the shared expression appears in, in the Power Query editor of Power BI Desktop. Power BI Desktop, for example, puts parameters in a group named `Parameters`. See the query group section below.

### Remote Parameter Name
`RemoteParameterName` · string · Options · compatibility level 1570+

In a composite model that uses DirectQuery over another semantic model, the name of the parameter in the remote model that this shared expression stands for. TOM describes it as applicable only to a proxy model. It's empty for ordinary shared expressions.

## Query group

A query group is a folder for queries in the Power Query editor of Power BI Desktop. Shared expressions and M partitions can each belong to a query group. Query groups only organize the Power Query editor: refresh, DAX and the field list don't use them, and Analysis Services ignores them.

Query groups need compatibility level 1480 or higher. When you delete a query group, Tabular Editor removes it from the shared expressions and partitions that used it.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Annotations](xref:object-properties-common#annotations)

### Folder
`Folder` · string · Options

The path of the query group, for example `Parameters`, or `Staging\Sales` for a group inside another group. The name of a query group is the same as its folder, and changing one changes the other.

Power BI Desktop separates nested query groups with a backslash and writes a query group for each level. For a group `Dates` inside a group `Staging`, the model contains the query groups `Staging` and `Staging\Dates`, and the queries in the inner group have `QueryGroup` `Staging\Dates`.

## Data binding hint

A data binding hint tells Fabric which data connection to use for a data source reference in the model. For example, when you deploy a model to a Fabric workspace, a binding hint binds the model's connection to a SQL server to a specific cloud connection or gateway connection in Fabric, and you don't bind it by hand in the semantic model's settings.

Fabric ignores the hint when the data source is already bound, or when the data connection doesn't exist in Fabric.

Data binding hints need compatibility level 1608 or higher. Add and edit them in the [Binding Info Collection](xref:object-properties-model#binding-info-collection) property of the model.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Object Type](xref:object-properties-common#object-type)

<!-- TODO (not verifiable from TE3 source or the TOM reference): how Fabric matches a data binding hint to a data source reference in the model (by Name?), and where users find the connection ID in Fabric (settings of the connection under Manage connections and gateways?). -->

### Connection Id
`ConnectionId` · string · Options

The ID of the Fabric data connection to bind to, usually a GUID. You find it in the settings of the connection under **Manage connections and gateways** in Fabric.

### Type
`Type` · BindingInfoType · Options · read-only

The kind of binding information.

| Value | Meaning |
|---|---|
| `DataBindingHint` | A hint to bind a data source reference to a Fabric data connection. This is the only kind in use. |
| `Unknown` | The kind isn't set. |

Tabular Editor sets the value, and you can't change it.
