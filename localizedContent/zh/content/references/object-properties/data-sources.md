---
uid: object-properties-data-sources
title: 数据源和表达式属性
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

# 数据源和表达式属性

<!--
SUMMARY: Reference for the properties of legacy and structured data sources, shared expressions (including M parameters), query groups and data binding hints.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

本页介绍用于描述模型数据来源的对象：数据源、共享表达式、Query Group 以及数据绑定提示。有关大多数对象共有的属性，请参阅 @object-properties-common。有关使用这些对象的分区，请参阅 @object-properties-partitions。

模型会通过以下类型的数据源之一连接到其源数据：

- **旧式（提供程序）数据源** 保存 OLE DB、ODBC 或托管提供程序的连接字符串。旧式分区会针对它们执行原生查询，通常为 SQL。它们适用于所有兼容级别。参见 [Provider数据源](#provider-data-source)。
- **结构化（Power Query）数据源** 使用 Power Query 的术语描述连接，例如协议和服务器；M 分区会按名称引用它们。它们仅在兼容级别为 1400 及以上的 Analysis Services 模型中可用。参见 [Structured数据源](#structured-data-source)。
- Power BI 和 Fabric 模型使用的是 **隐式数据源**。它们没有数据源对象：分区或共享表达式中的 M 表达式会指定数据源，而凭据由 Power BI 管理。

关于如何创建每种类型，参见 @connectivity 和 @import-tables。 @script-show-data-source-dependencies 脚本会列出使用旧式或 Structured数据源的表。 Best Practice Analyzer (BPA) 规则 @kb.bpa-remove-unused-data-sources 会标记未被任何分区或表达式引用的数据源。

当你重命名旧式数据源或 Structured数据源时，Tabular Editor 3 会更新共享表达式和 M 分区的 M 表达式中对它的引用，以及增量刷新的刷新策略中的轮询表达式和源表达式。只要分区仍在使用某个数据源，你就无法删除它。

## 凭据与保存

数据源可能包含机密信息，例如连接字符串中的密码、被模拟账户的密码或账户密钥。

在 Tabular Editor 2 和 3 的 **属性** 视图中，`Password` 属性会显示为圆点；在连接字符串中，`Password`、`Pwd`、`Secret` 或 `Key` 关键字的值会显示为 `********`。在 Tabular Editor 3 中，如果你编辑连接字符串时保留 `********` 不变，模型中存储的密码会保持不变。

将模型保存为 `.bim` 文件或保存到采用 JSON 格式的文件夹时，Tabular Editor 2 和 3 会移除每个数据源中的 `password`、`pwd`、`key` 和 `secret` 属性。它们还会从连接字符串中移除密码关键字（`Password`、`Pwd`、`Secret` 或 `Key`），包括 Provider数据源的 `ConnectionString` 以及 Structured数据源地址中的连接字符串。这样可以避免机密信息进入源代码管理。

保存为 Tabular Model Definition Language (TMDL) 时，Tabular Editor 2 和 3 会将 Tabular Object Model (TOM) 序列化程序设置为省略受限信息，例如密码。 TMDL 序列化程序会将所有密码写为 `********`，包括连接字符串中的密码，例如 `connectionString: data source=srv;user id=u;password=********`，其中 data source 表示数据源。

若要在保存的文件中包含机密信息，请在以下任一位置启用 **包含敏感信息**：

- 在 Tabular Editor 3 中，位于 **工具 > 偏好 > 文件格式**（请参见 @preferences）；或者在当前模型的 **模型 > 序列化选项...** 中设置，且此设置优先于偏好设置
- 在 Tabular Editor 2 中，位于 **文件 > 偏好...** 的 **序列化** 选项卡，在 **常规序列化设置** 下设置；或者针对你当前打开的模型，在 **当前模型** 选项卡下的 **当前模型序列化设置** 中设置

不建议包含敏感数据。

使用 Tabular Editor 3 的 Deployment Wizard 部署时，向导会针对你要部署的数据源中每一项缺失的机密信息弹出提示，例如当你从不包含敏感数据的已保存文件中加载模型后。机密信息为空或为 `********` 时，即视为缺失。该向导涵盖以下机密信息：

- provider 数据源的 `ConnectionString` 中的 password 关键字
- `ImpersonationMode` 为 `ImpersonateAccount` 的 Provider数据源的密码
- `AuthenticationKind` 为 `Windows`、`UsernamePassword` 或 `Key`（账户密钥）的 Structured数据源的机密信息

输入服务器刷新时使用的凭据。 Tabular Editor 3 会将这些信息加密后作为数据源覆盖项存储在 @user-options 文件中，并在后续部署时直接使用，不再提示。只有当连接字符串中包含密码关键字时，才会提示输入连接字符串密码。保存时如果不包含敏感数据，会删除整个关键字，因此这样保存后不会再为此显示提示。

如果你在 Deployment Wizard 中取消选中 [部署数据源](xref:deployment#deployment-options)，Tabular Editor 3 会改为重新部署目标端自身的数据源，例如为每个环境保留单独的数据源。同样的检查也会对这些数据源执行：如果服务器未返回其中某个数据源所需的密码或密钥，就会出现提示。这些回答不会存储在用户选项文件中，因此下次部署时还会再次提示。

Tabular Editor 用于浏览源并读取其架构的凭据（例如在 **导入表** 向导中）会按用户存储在 @user-options 文件中，不属于模型的一部分。刷新时，服务器使用数据源的凭据。

Power BI 和 Fabric 模型从不包含凭据。在 Power BI 服务中的语义模型上设置这些凭据，或在 Fabric 连接上设置（参见 [数据绑定提示](#data-binding-hint)）。

## Provider数据源

Provider（旧版）数据源使用连接字符串，通过 OLE DB、ODBC 或托管的 .NET 提供程序连接到源。旧版分区会针对它运行本机查询，例如 SQL `SELECT` 语句。兼容级别低于 1400 时，这是唯一的数据源类型。

### 常见属性

- [名称](xref:object-properties-common#name)
- [说明](xref:object-properties-common#description)
- [注释](xref:object-properties-common#annotations)
- [扩展属性](xref:object-properties-common#extended-properties)
- [对象类型](xref:object-properties-common#object-type)

某些Provider数据源封装了 Power BI Mashup：连接字符串中的 `Provider=` 关键字指定 Power BI 或 Mashup 提供程序，而 `Mashup` 或 `Extended Properties` 关键字则以 Base64 编码的 ZIP 压缩包形式保存 Power Query 定义。一些较旧的 Power BI Desktop 模型会用这种方式描述它们的数据源。对于这些数据源，`Name` 会显示连接字符串中的 `Location`，实际存储的名称位于 [源 ID](#source-id)，并且 **属性** 视图会显示 **Power BI 源详细信息** 类别，其中包含解码后的 M 查询。对于其他Provider数据源，**属性** 视图会隐藏此类别。

<!-- TODO (not verifiable from TE3 source): which versions of Power BI Desktop, or which scenarios, produce provider data sources with an embedded mashup. -->

### Account

`Account` · string · 连接详细信息

当 `ImpersonationMode` 为 `ImpersonateAccount` 时，服务器使用该 Windows 账户连接到源，例如 `CONTOSO\\svc-ssas-reader`。在 `Password` 中输入该账户的密码。其他模拟模式下请留空。

### 连接字符串

`ConnectionString` · string · 连接详细信息

服务器用来打开连接的连接字符串。关键字因提供程序而异，例如：

```text
Provider=MSOLEDBSQL;Data Source=myserver;Initial Catalog=AdventureWorks;Integrated Security=SSPI
```

点击省略号按钮，在对话框中编辑连接字符串。当 `Provider` 为 `System.Data.SqlClient` 或 `Microsoft.Data.SqlClient` 时，Tabular Editor 3 会打开其 SQL Server 连接对话框；否则会打开 OLE DB 数据链接对话框。连接字符串中的密码会在 **属性** 视图中以掩码显示，并在保存到文件时被移除（请参阅 [凭据和保存](#credentials-and-saving)）。

导入表或更新表架构时，Tabular Editor 可以使用自己的本地连接信息进行连接（请参阅 @import-tables）。

若要让模型在不同环境中指向不同的服务器，请在部署前通过 C# Script 或命令行更改连接字符串，或者在 Deployment Wizard 中取消选择 **Deploy Data Sources**，以保留目标端的数据源（请参阅 @deployment）。在 Tabular Editor 3 中，@user-options 文件中的数据源覆盖设置可让你的 Workspace 数据库使用独立的连接信息。

BPA 规则 @kb.bpa-specify-application-name 会标记未包含 `Application Name` 的 SQL Server 连接字符串。有了应用程序名称，数据库管理员就能看出哪些查询来自该模型。

### 身份模拟模式

`ImpersonationMode` · ImpersonationMode · 连接详细信息

对于使用 Windows 身份验证的提供程序，这是服务器在刷新期间连接到源时所使用的 Windows 身份。使用 SQL 身份验证时，服务器会使用连接字符串中的用户名和密码。

| 值                              | 含义                                                                                                           |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| `ImpersonateServiceAccount`    | Analysis Services 服务运行所使用的账户。该账户需要对每个源具有读取权限。                                                                |
| `ImpersonateAccount`           | 在 `Account` 和 `Password` 中设置的特定 Windows 账户。                                                                  |
| `ImpersonateCurrentUser`       | 发送查询的用户的身份。仅适用于 DirectQuery。 Azure Analysis Services 不支持将此模式用于本地源。                                           |
| `ImpersonateAnonymous`         | 不使用 Windows 身份的匿名连接。 Microsoft TOM 参考文档将此模式列为不受支持。                                                           |
| `ImpersonateUnattendedAccount` | 服务器上预先配置的无人值守账户。                                                                                             |
| `Default`                      | 未明确指定模式。服务器使用从数据库继承的模拟设置。当 Tabular Editor 加载设置为 `Default` 的 Provider数据源时，会将其设置为 `ImpersonateServiceAccount`。 |

在 Azure Analysis Services 中，大多数数据源在连接字符串中使用 SQL 或 Microsoft Entra 身份验证。有关各环境支持的选项，请参阅 [Analysis Services 表格模型中的模拟](https://learn.microsoft.com/analysis-services/tabular-models/impersonation-ssas-tabular)。

### Isolation

`Isolation` · DatasourceIsolation · 连接详情

服务器针对关系数据源运行查询时使用的事务隔离级别。

| 值               | 含义                                          |
| --------------- | ------------------------------------------- |
| `ReadCommitted` | 只读取已提交事务中的数据。这是默认设置。                        |
| `Snapshot`      | 读取查询开始时的数据事务一致性快照，并且不会被其他事务阻塞。源数据库必须允许快照隔离。 |

在 `Snapshot` 模式下，即使 ETL 进程正在向同一数据库写入数据，各分区看到的数据状态也保持一致。

### Password

`Password` · string · 连接详细信息

在 `ImpersonationMode` 为 `ImpersonateAccount` 时，会使用 `Account` 中指定的 Windows 账户密码。它在 **属性** 视图中会以掩码显示；保存到文件时，除非你选择包含敏感数据，否则 Tabular Editor 3 不会将其写入文件（请参阅 [凭据和保存](#credentials-and-saving)）。如果使用 Tabular Editor 3 的 Deployment Wizard 进行部署时缺少该密码，系统会提示你输入。

### Provider

`Provider` · string · 连接详细信息

托管 .NET 数据提供程序的名称，例如 `System.Data.SqlClient`。对于 OLE DB 提供程序，请将其留空，并在连接字符串中使用 `Provider=` 关键字指定提供程序名称。

当你将 SQL Server 或 Fabric SQL 端点中的表导入到旧版数据源时，Tabular Editor 3 会将 `Provider` 设置为 `System.Data.SqlClient`。对于 ODBC 和 Oracle，会将 `Provider` 置空，并让连接字符串以 `Provider=MSDASQL` 或 `Provider=OraOLEDB.Oracle` 开头。

<!-- TODO (not verifiable from TE3 source): list which managed provider names Analysis Services accepts in Provider, besides System.Data.SqlClient. -->

Analysis Services 支持的 OLE DB 提供程序比 Windows 少。如果服务器不支持某个提供程序，即使它能在 Tabular Editor 3 中连接，在服务器上刷新时也会失败（见 @connect-oledb）。

### Timeout

`Timeout` · int · 连接详细信息

服务器等待针对该数据源的命令完成的时间（以秒为单位）。新数据源的 `Timeout` 默认为 `0`。对于速度较慢的数据源，或查询需要很长时间才能返回第一行数据的大型分区，可以增大此值。

<!-- TODO (not verifiable from TE3 source): whether a Timeout of 0 means no timeout or the server's default timeout. SSAS 2025 accepts any value on save without validation, so this needs a slow source to observe. -->

### 最大连接数

`MaxConnections` · int · 选项

服务器可同时为此数据源打开的最大连接数。刷新期间，服务器会并行处理各个分区，每个分区使用一个连接。新数据源的 `MaxConnections` 默认为 `10`。对于无法处理大量并发查询的数据源，可以调低此值；若要并行刷新更多分区，可以调高此值。

将其设为 `-1`，以使用模型的 [数据源默认最大连接数](xref:object-properties-model#data-source-default-max-connections)（兼容级别 1510 及更高版本）。

<!-- TODO (not verifiable from TE3 source): what the engine does with Max Connections 0 during refresh. SSAS 2025 accepts 0 and negative values on save without validation. -->

### 类型

`Type` · DataSourceType · 选项 · 只读

数据源的类型：`Provider` 表示 Provider数据源，`Structured` 表示 [Structured数据源](#structured-data-source)。它会在创建数据源时设置。

### M 查询

`MQuery` · string · Power BI 源详细信息 · 只读 · _计算生成_

这是嵌入在连接字符串中的 Power Query (M) 表达式，读取自存档中的 `.m` 文件。若要更改查询，可以在 Power BI Desktop 中修改。

### 源 ID

`SourceID` · string · Power BI 源详细信息 · 只读 · _TOM 中数据源名称的快捷引用_

数据源在模型中存储时使用的名称，通常是自动生成的 ID。

## Structured数据源

Structured数据源使用 Power Query 的术语来描述连接，包括协议（如 SQL Server 或 Azure Blob Storage）、地址（如服务器和数据库）以及凭据。 M 分区和共享表达式会按名称引用它，例如：

```m
let
    Source = #"SQL/myserver;AdventureWorks",
    Sales = Source{[Schema = "dbo", Item = "FactInternetSales"]}[Data]
in
    Sales
```

Structured数据源存在于兼容级别为 1400 及以上的 Analysis Services 模型中。 Power BI 和 Fabric 模型使用隐式数据源。

下面的大多数属性都是数据源连接详细信息或凭据中某个值的快捷方式，而 TOM 会将这些信息以 JSON 格式存储。只会使用适用于 `Protocol` 的那些属性，例如：SQL Server 源使用 `Server` 和 `Database`，文件源使用 `Path`。其余属性将保持为空。

### 常见属性

- [名称](xref:object-properties-common#name)
- [描述](xref:object-properties-common#description)
- [注释](xref:object-properties-common#annotations)
- [扩展属性](xref:object-properties-common#extended-properties)
- [对象类型](xref:object-properties-common#object-type)

### 协议

`Protocol` · 字符串 · 基本

连接类型，例如：SQL Server 和 Azure SQL 使用 `tds`，Oracle 使用 `oracle`；也可以是 `odbc`、`ole-db`；本地或网络文件使用 `file`；Azure Blob Storage 使用 `azure-blobs`；OData 源使用 `odata`。协议决定会使用哪些 **连接详细信息** 和 **凭据** 属性。

该值可自由填写。 TOM `DataSourceProtocol` 类列出了 TOM 识别的名称，例如 `analysis-services`、`azure-tables`、`db2`、`folder`、`http`、`mysql`、`postgresql`、`sap-hana-sql`、`sharepoint-list` 和 `teradata`（完整列表请参阅 [DataSourceProtocol](https://learn.microsoft.com/dotnet/api/microsoft.analysisservices.tabular.datasourceprotocol)）。将表导入 Structured数据源时，Tabular Editor 3 会将 `Protocol` 设置为 SQL Server 和 Fabric SQL 终结点所用的 `tds`，或设置为 `odbc`、`ole-db` 或 `oracle`。

### Account

`Account` · 字符串 · 连接详细信息

对于连接到 Azure 存储帐户的协议（例如 Azure Blob Storage 或 Azure Table Storage），此属性为存储帐户名称。它与 `Domain` 一起构成帐户地址，例如帐户 `contosodata` 和域 `blob.core.windows.net`。

### 地址

`Address` · 地址 · 连接详细信息 · 只读

数据源的所有连接地址值。单击省略号按钮，可以在集合编辑器中编辑这些值，包括那些没有对应快捷属性的值。下面这些属性，如 `Server` 和 `Database`，是地址中各个值的简写。

<!-- TODO (not verifiable from TE3 source or the TOM reference, which only names each ConnectionAddress property): which protocols use Model, ContentType, EmailAddress, Object, Property, Resource and View, with an example value for each. The examples below for Model (analysis-services), EmailAddress (Exchange) and Resource (web URL) are unconfirmed. -->

### 模型

`AddressModel` · string · 连接详细信息

`analysis-services` 等用于连接到语义模型或多维数据集的协议的模型名称。

### 连接字符串

`ConnectionString` · string · 连接详细信息

连接字符串，适用于需要连接字符串的协议，例如 `odbc` 和 `ole-db`。例如：

```text
Driver={Snowflake};Server=contoso.snowflakecomputing.com;Warehouse=COMPUTE_WH
```

在 **属性** 视图中，连接字符串中的密码会被遮蔽；保存到文件时会被移除（参见[凭据和保存](#credentials-and-saving)）。

### 内容类型

`ContentType` · string · 连接详细信息

源内容的类型，适用于需要了解读取内容格式的协议。

### 数据库

`Database` · string · 连接详细信息

服务器上数据库的名称，例如 `tds` 协议中的 `AdventureWorks`。

### 域名

`Domain` · string · 连接详细信息

地址中的域名部分，例如 Azure Blob 存储的 `blob.core.windows.net`。通常与 `Account` 搭配使用。

### 电子邮件地址

`EmailAddress` · string · 连接详细信息

电子邮件地址，适用于通过用户电子邮件地址标识连接的协议，例如 Exchange。

### 对象

`Object` · string · 连接详细信息

源中对象的名称，适用于指定单个对象的协议。

### 路径

`Path` · string · 连接详细信息

文件或文件夹的路径，适用于 `file` 和 `folder` 等协议，例如 `\\fileserver\data\sales.csv`。负责刷新模型的服务器必须能够访问该路径。

### 属性

`Property` · string · 连接详细信息

特定协议的地址值。

### Query

`Query` · 字符串 · 连接详细信息

连接发送到数据源的本机查询，通常为 SQL，例如 `SELECT * FROM dbo.Customer`。大多数模型会将其留空，并在分区的 M 表达式中进行筛选。

### 资源

`Resource` · 字符串 · 连接详细信息

特定于协议的资源标识符，例如 Web 资源的 URL。

### 架构

`Schema` · 字符串 · 连接详细信息

对于按架构寻址的协议，此处为数据库中的架构。

### 服务器

`Server` · 字符串 · 连接详细信息

要连接的服务器，例如 `tds` 协议中的 `myserver.database.windows.net`。将同一模型部署到不同环境时，你通常会更改这个值。

### 网址

`Url` · 字符串 · 连接详细信息

源的 URL，适用于 `odata` 和 `http` 等协议，例如 `https://services.odata.org/V4/Northwind/Northwind.svc`。

### 视图

`View` · 字符串 · 连接详细信息

对于按视图寻址的协议，此处为数据源中视图的名称。

### AuthenticationKind

`AuthenticationKind` · 字符串 · 凭据

服务器向数据源进行身份验证的方式。从下拉列表中选择一个值，或直接输入：

| 值                  | 含义                                                                                      |
| ------------------ | --------------------------------------------------------------------------------------- |
| `Windows`          | 在 `Username` 和 `Password` 中指定的 Windows 帐户。                                              |
| `UsernamePassword` | 数据源识别的用户名和密码，例如 SQL Server 登录名。当你选择特定帐户时，Tabular Editor 3 的 **Import Tables** 向导会使用此类型。 |
| `Key`              | 帐户密钥，例如 Azure Blob Storage 的密钥，会以 `Credential` 中的 `Key` 值存储。                            |
| `OAuth2`           | OAuth 2.0 令牌，例如用于 Microsoft Entra ID 数据源。                               |
| `ServiceAccount`   | Analysis Services 服务运行时所使用的帐户。                                                          |
| `CurrentUser`      | 运行查询的用户标识。                                                                              |
| `Unattended`       | 在服务器上预先配置的无人值守帐户。当选择无人值守帐户时，**导入表** 向导会使用此类型。                                           |
| `Implicit`         | 没有显式凭据。当选择匿名访问时，**导入表** 向导会使用此类型。                                                       |

可用的类型取决于 `Protocol`。 TOM 还定义了另外四种类型：`Exchange`、`KerberosS4U`、`SapBasic` 和 `WebApi`。

当 `AuthenticationKind` 为 `Windows`、`UsernamePassword` 或 `Key` 且缺少机密值时，在使用 Tabular Editor 3 的 Deployment Wizard 部署时会提示输入（请参阅 [凭据和保存](#credentials-and-saving)）。

<!-- TODO (not verifiable from TE3 source): confirm that CurrentUser on a structured data source, like ImpersonateCurrentUser on a provider data source, only applies to DirectQuery. -->

### Credential

`Credential` · Credential · Credential · 只读

数据源的所有凭据值。单击省略号按钮，在集合编辑器中编辑这些值，其中也包括没有单独快捷属性的值，例如帐户密钥的 `Key`。 `AuthenticationKind`、`Username`、`Password`、`PrivacySetting` 和 `EncryptConnection` 是用于访问凭据中各个值的快捷属性。

保存到文件时，Tabular Editor 3 会移除密码或密钥等机密值，除非选择包含敏感数据（请参阅 [凭据和保存](#credentials-and-saving)）。

### EncryptConnection

`EncryptConnection` · bool · Credential

当为 `true` 时，与数据源的连接必须加密，例如使用 TLS。仅对不支持加密的源才将其设置为 `false`，例如某些没有证书的本地服务器。

### Password

`Password` · string · 凭据

当 `AuthenticationKind` 为 `Windows` 或 `UsernamePassword` 时，`Username` 对应的密码。它在 **Properties** 视图中会以掩码形式显示；而在保存到文件时，除非你选择包含敏感数据，否则 Tabular Editor 3 不会将其写入文件。如果你使用 Deployment Wizard 部署时未提供密码，系统会提示你输入密码，并同时提示输入 `Username` 和 `PrivacySetting`（请参阅[凭据和保存](#credentials-and-saving)）。

连接到已部署的模型时，Analysis Services 不会返回密码，因此从服务器打开的模型不包含密码。对于通过模型部署的数据源，Tabular Editor 3 会将你输入的内容存储在 @user-options 文件中，因此每个模型只需输入一次。

### PrivacySetting

`PrivacySetting` · string · 凭据

数据源的 Power Query 隐私级别：`None`、`Public`、`Organizational` 或 `Private`。空值与 `None` 相同。当 Power Query 组合多个数据源时，隐私级别决定了一个数据源的数据是否可以传递到另一个数据源，例如作为对第二个数据源查询中的筛选值。隐私级别不匹配可能会阻止查询折叠，或导致刷新因防火墙错误而失败。

若要为整个模型忽略隐私级别，请在模型上设置[启用快速合并](xref:object-properties-model#enable-fast-combine)。

在 Tabular Editor 3 中，@preferences 里的 **Ignore privacy settings** 序列化选项会在你将模型保存为 `.bim` 文件或以 JSON 格式保存到文件夹时，从模型中移除所有 `PrivacySetting` 值。你当前打开的模型会保留这些值。如果你使用较旧版本的 `Microsoft.AnalysisServices.Deployment` 来部署已保存的模型，而该版本不支持此属性，请使用此选项。

### Username

`Username` · string · 凭据

当 `AuthenticationKind` 为 `Windows` 或 `UsernamePassword` 时，服务器用于连接的用户名，例如 `CONTOSO\svc-reader` 或 SQL Server 登录名。

### 上下文表达式

`ContextExpression` · string · 选项

关于数据源结构或元数据的补充信息，例如内容类型、内容形状和格式，这些在 Analysis Services 表格协议规范中有定义。位置本身在连接详细信息中指定。大多数模型都会将其留空。

### 最大连接数

`MaxConnections` · int · 选项

服务器同时向此源打开的最大连接数。请参阅 Provider数据源上的[最大连接数](#max-connections)。

### 选项

`Options` · Options · 选项 · 只读

特定于协议的连接选项。点击省略号按钮，在集合编辑器中编辑这些选项。 Tabular Editor 3 会在可能时将每个值解析为 JSON，因此 `true` 会存储为布尔值，`{...}` 会存储为对象。可用选项取决于 `Protocol`。

例如，`hierarchicalNavigation` 选项用于设置是否按数据库、架构和表的层次结构来导航该源。当你通过 ODBC 将表导入到 Structured数据源时，Tabular Editor 3 会将其设置为 `true`。如果在 Tabular Editor 3 为导入的表生成 M 表达式时未设置该选项，Tabular Editor 3 会对 `ole-db` 协议使用 `true`，对其他协议使用 `false`。

### 类型

`Type` · DataSourceType · 选项 · 只读

数据源类型：此类数据源为 `Structured`；[Provider数据源](#provider-data-source)为 `Provider`。

## 共享表达式

共享表达式是在模型级别命名的 Power Query (M) 表达式，分区和其他共享表达式可通过名称引用它，例如多个表共享的连接、辅助函数或通用转换步骤。在 Power BI Desktop 中，所有未加载到表中的查询都会成为共享表达式。共享表达式需要 1400 或更高的兼容级别。

_M 参数_ 是带有 `meta` 记录并标记为参数的共享表达式，例如：

```m
"myserver.database.windows.net" meta [IsParameterQuery = true, Type = "Text", IsParameterQueryRequired = true]
```

你可以在 Power BI 服务中更改参数值，而无需编辑模型，例如用于在不同环境之间切换模型。在 Tabular Editor 3 中，刷新覆盖配置文件可为单次刷新指定不同的参数值，而不会更改模型（见 @refresh-overrides）。增量刷新需要参数 `RangeStart` 和 `RangeEnd`，@incremental-refresh-setup 说明了如何创建它们。在 Direct Lake 模型中，共享表达式保存与 Lakehouse 或 Warehouse 的连接（见 @object-properties-partitions 中的 `ExpressionSource`）。

见 @how-to-work-with-expressions、@script-create-m-parameter 和 @script-create-and-replace-parameter。

### 常见属性

- [名称](xref:object-properties-common#name)
- [描述](xref:object-properties-common#description)
- [注释](xref:object-properties-common#annotations)
- [扩展属性](xref:object-properties-common#extended-properties)
- [对象类型](xref:object-properties-common#object-type)
- [Lineage tag](xref:object-properties-common#lineage-tag)
- [源 Lineage tag](xref:object-properties-common#source-lineage-tag)

### 表达式

`Expression` · string · 选项

M 表达式。在 **表达式编辑器**中编辑。其他表达式会通过共享表达式的名称来引用它，例如 `Source = ServerName`；如果名称中包含空格，则应使用 `Source = #"Server Name"`。

当你重命名共享表达式时，Tabular Editor 3 不会更新引用它的 M 表达式。请自行更新，例如使用“查找并替换”。

### 表达式来源

`ExpressionSource` · NamedExpression · 选项 · 兼容级别 1570+

在对另一个语义模型使用 DirectQuery 的复合模型中，用于保存与该远程模型连接的共享表达式。对于表示远程模型参数的共享表达式，此属性会与 `RemoteParameterName` 一起设置。当你删除它所指向的共享表达式时，Tabular Editor 会清除 `ExpressionSource`。

<!-- TODO (not verifiable from TE3 source; the TOM reference only says "A reference to the NamedExpression where the parameter associated with the remote model"): confirm the scenario for Expression Source and Remote Parameter Name on shared expressions, that is, proxy parameters for a remote model in a composite model. -->

### 类型

`Kind` · ExpressionKind · 选项

表达式的语言。唯一的取值是 `M`，用于 Power Query。 Tabular Editor 在创建共享表达式时设置此属性。

### M 属性

`MAttributes` · string · 选项 · 兼容级别 1535+

M 参数的 `meta` 记录，与表达式分开存储，例如 `[IsParameterQuery = true, Type = "Text", IsParameterQueryRequired = true]`。

Power BI Desktop 会将 `MAttributes` 留空。它会将参数的元数据记录保留在 `Expression` 的末尾，例如 `#datetime(2026, 1, 1, 0, 0, 0) meta [IsParameterQuery=true, Type="DateTime", IsParameterQueryRequired=true]`。

<!-- TODO (not verifiable from TE3 source): what happens when both M Attributes and a meta record in Expression are set. -->

### 参数值列

`ParameterValuesColumn` · 列 · 选项 · 兼容级别 1545+

将 M 参数绑定到某一列，这样该列上的 Report 筛选器就会设置该参数的值。 Power BI 将其称为 _动态 M 查询参数_：当用户在该列的切片器中选择某个值时，该值会传递给参数，DirectQuery 源查询会使用它。

设置此属性后，DAX 查询可以覆盖该参数。该列的数据类型必须与参数 `meta` 记录中的 `Type` 匹配。该列通常位于一个较小的断开连接表中，该表列出了允许的值。

该值来自 Report 用户，因此只应绑定源查询能够安全处理的参数。

### Query Group

`QueryGroup` · QueryGroup · 选项 · 兼容级别 1480+

共享表达式在 Power BI Desktop 的 Power Query 编辑器中显示所属的 Query Group（文件夹）。例如，Power BI Desktop 会将参数放入名为 `Parameters` 的组中。请参阅下方的 Query Group 章节。

### 远程参数名称

`RemoteParameterName` · string · 选项 · 兼容级别 1570+

在对另一个语义模型使用 DirectQuery 的复合模型中，此共享表达式所代表的远程模型中的参数名称。 TOM 将其描述为仅适用于代理模型。对于普通共享表达式，此属性为空。

## Query Group

Query Group 是 Power BI Desktop 的 Power Query 编辑器中用于存放查询的文件夹。共享表达式和 M 分区都可以属于某个 Query Group。 Query Group 仅用于组织 Power Query 编辑器：刷新、DAX 和字段列表都不会用到它，Analysis Services 也会忽略它。

Query Group 需要兼容级别 1480 或更高。删除某个 Query Group 时，Tabular Editor 会将其从使用它的共享表达式和分区中移除。

### 通用属性

- [名称](xref:object-properties-common#name)
- [描述](xref:object-properties-common#description)
- [注释](xref:object-properties-common#annotations)
- [对象类型](xref:object-properties-common#object-type)

### 文件夹

`Folder` · 字符串 · 选项

Query Group 的路径，例如 `Parameters`；若该组嵌套在其他组内，则为 `Staging\\Sales`。 Query Group 的名称与其文件夹相同，修改其中一个会同步修改另一个。

Power BI Desktop 使用反斜杠分隔嵌套的 Query Group，并为每个层级创建一个 Query Group。如果组 `Dates` 位于组 `Staging` 内，则模型包含 Query Group `Staging` 和 `Staging\Dates`，而内层组中的查询的 `QueryGroup` 为 `Staging\Dates`。

## 数据绑定提示

数据绑定提示会告知 Fabric，对于模型中的数据源引用应使用哪个数据连接。例如，当你将模型部署到 Fabric Workspace 时，数据绑定提示会将模型到 SQL Server 的连接绑定到 Fabric 中特定的云连接或 Gateway 连接，从而无需在语义模型的设置中手动绑定。

如果数据源已绑定，或者该数据连接在 Fabric 中不存在，Fabric 会忽略此提示。

数据绑定提示需要 1608 或更高的兼容级别。可以在模型的[绑定信息集合](xref:object-properties-model#binding-info-collection)属性中添加和编辑这些提示。

### 通用属性

- [名称](xref:object-properties-common#name)
- [描述](xref:object-properties-common#description)
- [注释](xref:object-properties-common#annotations)
- [扩展属性](xref:object-properties-common#extended-properties)
- [对象类型](xref:object-properties-common#object-type)

<!-- TODO (not verifiable from TE3 source or the TOM reference): how Fabric matches a data binding hint to a data source reference in the model (by Name?), and where users find the connection ID in Fabric (settings of the connection under Manage connections and gateways?). -->

### 连接 Id

`ConnectionId` · 字符串 · 选项

要绑定的 Fabric 数据连接的 ID，通常为 GUID。你可以在 Fabric 中该连接的设置里的 **Manage connections and gateways** 下找到它。

### 类型

`Type` · BindingInfoType · 选项 · 只读

绑定信息的类型。

| 值                 | 含义                                      |
| ----------------- | --------------------------------------- |
| `DataBindingHint` | 用于将数据源引用绑定到 Fabric 数据连接的提示。这是目前唯一使用的类型。 |
| `Unknown`         | 类型未设置。                                  |

该值由 Tabular Editor 设置，你无法更改。
