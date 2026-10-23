---
uid: user-options
title: 用户选项 (.tmuo) 文件
author: Daniel Otykier
updated: 2026-10-12
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# 表格模型用户选项 (.tmuo) 文件

Tabular Editor 3 引入了一种新的基于 JSON 的文件，用于存储特定于开发者和模型的首选项。此文件称为**表格模型用户选项**文件，并使用 **.tmuo** 文件扩展名。

当您从磁盘打开模型时，系统会在其旁边创建文件，文件名称以模型名称和您的 Windows 用户名命名。每次从磁盘加载模型时，Tabular Editor 都会查找具有该名称的文件。

| 您打开的文件 | 用户选项文件 |
|---|---|
| `SpaceParts.bim` 或任何 `.bim` / `.pbit` / `database.json` 文件 | `SpaceParts.<UserName>.tmuo`，位于其旁边 |
| `model.tmdl` 或 `database.tmdl` 文件 | `model.<UserName>.tmuo`，位于其旁边 |
| 包含 `database.json` 的文件夹 | `database.<UserName>.tmuo`，位于该文件夹中 |
| 包含表格模型定义语言 (TMDL) 模型文件的文件夹 | 该文件夹中的 `model.<UserName>.tmuo`，位于该文件夹中 |

TMDL 始终使用 `model` 前缀，以便与早于 `database.tmdl` 的版本保持一致。

对于通过连接而非从磁盘打开的模型，除了模型之外，没有其他地方可以放置该文件，因此该文件按服务器和数据库保存在 `%LocalAppData%\TabularEditor3\UserOptions\` 下。

是否为新模型创建文件由 @preferences 下的*创建用户选项 (.tmuo) 文件*控制。

> [!IMPORTANT]
> **.tmuo** 文件包含用户特定的首选项，因此不应将其纳入共享版本控制环境。如果你使用 Git 进行版本控制，请务必在 `.gitignore` 文件中包含 `.tmuo` 扩展名。

## 文件内容

该文件是 JSON 文件，每个属性都是可选的。只有当有内容需要存储时，Tabular Editor 才会写入一个文件，因此，一个实际的文件只包含以下几个块，而不是全部块。如果不需要存储任何内容，则根本不会写入任何文件。

对于一个除了连接到工作区数据库外什么都不做的模型，其最小文件如下：

```json
{
  "UseWorkspace": true,
  "WorkspaceConnection": {
    "ConnectionString": "data source=localhost",
    "EncryptedCredentials": "AQAAANCMnd8BFdERjHoAwE..."
  },
  "WorkspaceDatabase": "WorkspaceDB_MyUser_20260915"
}
```

### 顶级属性

| 属性 | 类型 | 写入时 |
|---|---|---|
| `UseWorkspace` | 布尔值 | 您已回答此模型的工作区问题。如果该属性不存在，Tabular Editor 会在每次加载模型时询问。|
| `WorkspaceConnection` | 字符串或对象 | 已设置工作区连接。当连接字符串包含密码时的对象形式。|
| `WorkspaceConnectionAuthMode` | 字符串 | 旧版，且仅当其不是 `Integrated` 时。身份验证模式现在由连接字符串隐含。|
| `WorkspaceDatabase` | 字符串 | 已设置工作区数据库名称。|
| `Deployment` | 对象 | 部署向导已对此模型运行。|
| `DataSourceOverrides` | 对象 | 至少定义了一个数据源替代。|
| `TableImportSettings` | 对象 | 至少一个数据源具有导入设置。|
| `RefreshOverrides` | 对象 | 已定义至少一个刷新覆盖配置文件。|
| `AIConsent` | 对象 | 旧版。存在时读取，绝不写回。|
| `Permissions` | 对象 | 已授予至少一个每模型 AI 权限。|

它们按该顺序显示。

### 工作区数据库

- `UseWorkspace` 决定 Tabular Editor 在加载模型时是否连接到工作区数据库。工作区数据库将被加载的文件或文件夹结构的元数据覆盖。
- `WorkspaceConnection` 是工作区数据库部署到的 Analysis Services 实例或 Power BI XMLA 端点。
- `WorkspaceDatabase` 是该数据库的名称。请确保每个开发者和每个模型都有唯一的名称，因为关键在于每个开发者都能拥有自己的名称。

### 数据源覆盖

`DataSourceOverrides` 用于为工作区数据库提供与模型文件中的连接详细信息不同的连接详细信息，因此 Analysis Services 会从模型指定位置以外的位置进行刷新。

| 属性 | 类型 | 写入时 |
|---|---|---|
| `ImpersonationMode` | 字符串 | 不是`Default`。以下之一:`Default`、`ImpersonateAccount`、`ImpersonateAnonymous`、`ImpersonateCurrentUser`、`ImpersonateServiceAccount`、`ImpersonateUnattendedAccount`。|
| `Username` | 字符串 | 已设置。|
| `ConnectionString` | 加密对象 | 已设置。|
| `Password` | 加密对象 | 已设置。|
| `AccountKey` | 加密对象 | 已设置。用于 Blob 存储源。|
| `PrivacySetting` | 字符串 | 设置。|

下次写入文件时，将删除数据源不再存在于模型中的覆盖，而数据源已重命名的覆盖将遵循重命名。

### 表格导入设置

`TableImportSettings` 用于在您运行[导入表或架构更新](xref:importing-tables)时，浏览可用表和视图并获取源架构更改。

| 属性 | 类型 | 写入时 |
|---|---|---|
| `ServerType` | 字符串 | 始终。`Sql`、`Oracle`、`Odbc`、`OleDb`、`Snowflake`、`Dataflow`、`PostgreSql`、`MySql`、`MariaDb`、`Db2`、`Databricks`、`OneLake` 之一。|
| `Options` | 字符串对象 | 集合不为空。|
| `UserId` | 字符串 | 已设置。|
| `Password` | 加密对象 | 已设置，*并且*您选择了保存。|
| `Provider` | 字符串 | `ServerType` 为 `OleDb`。|
| `PasswordKey`、`UserIdKey` | 字符串 | `ServerType` 为 `OleDb` 且已设置相应的值。|
| `Server` | 字符串 | `ServerType` 不是 `Odbc`，并且已设置。|
| `ServerKey`、`DatabaseKey` | 字符串 | `ServerType` 不是 `Sql`，并且已设置值。|
| `Database` | 字符串 | 已设置。|
| `Authentication` | 字符串 | `ServerType` 为 `Sql`、`OleDb` 或 `Databricks`。`Sql`、`WindowsIntegrated`、`AadInteractive`、`AadPassword`、`AadIntegrated`、`AadServicePrincipal`、`AccessToken`、`OAuth` 之一。|
| `Encrypt` | 布尔值 | 任意设置。|
| `Dsn` | 字符串 | 已设置。用于 ODBC。|
| `RowLimitClause`、`IdentifierQuoting` | 数字 | 不为默认值。|
| `Schema` | 字符串 | 已设置。|

`Options` 是特定于一个提供商的任何内容最终所在的位置，以纯字符串形式表示：Snowflake 仓库是 `Options.warehouse`，OneLake 工作区是 `Options.workspaceid`。`…Key` 属性是连接字符串键的*名称*，例如 `PWD`，而不是密钥。

`Password` 是此处唯一加密的值。`UserId`、`Server`、`Database`、`Dsn`以及`Options`中的所有内容均以纯文本形式存储，因此即使文件不包含密码，也应将其视为敏感文件。Power BI 访问令牌存储为 `Password`，并经过加密。

### 部署

`Deployment` 包含部署向导上次对此模型使用的内容。一旦块存在，七个布尔选项始终会被写入，无论它们是 true 还是 false：

| 属性 | 类型 | 写入时 |
|---|---|---|
| `DeployDataSources` | 布尔值 | 始终 |
| `DeployPartitions` | 布尔值 | 始终 |
| `DeployRefreshPolicyPartitions` | 布尔值 | 始终 |
| `DeployModelRoles` | 布尔值 | 始终 |
| `DeployModelRoleMembers` | 布尔值 | 始终 |
| `DeploySharedExpressions` | 布尔值 | 始终 |
| `DeployLinguisticMetadata` | 布尔值 | 始终 |
| `TargetConnectionString` | 字符串或对象 | 始终，如果未设置，则为 `null`。当连接字符串包含密码时的对象形式。|
| `TargetDatabase` | 字符串 | 始终，如果未设置，则为 `null`。|
| `TargetCredentials` | 对象 | 同时设置了用户名和密码。|

### 刷新覆盖

`RefreshOverrides` 以配置文件名称作为键，该键是存储该名称的唯一位置。每个配置文件都包含一个单独的 `Overrides` 数组，用于描述配置文件在运行时所做的更改。请参阅@refresh-overrides，了解配置文件的作用以及如何定义配置文件。

```json
"RefreshOverrides": {
  "Nightly": {
    "Overrides": [
      {
        "scope": { "table": "Sales" },
        "partitions": [
          {
            "originalObject": { "table": "Sales", "partition": "Sales-2025" },
            "source": { "query": "SELECT * FROM dbo.FactSales WHERE Year = 2025" }
          }
        ]
      }
    ]
  }
}
```

### 按模型划分的 AI 权限

`Permissions` 记录仅适用于此模型的 AI 权限授予，当您在 @ai-assistant 的权限卡上选择**允许用于此模型**时写入。

```json
"Permissions": {
  "Grants": { "ModelMetadata": "Write", "ModelData": "Read" },
  "LastGrantedAt": "2026-09-15T08:12:44.117Z"
}
```

`Grants` 为您已授予的每个资源包含一个条目：`ModelMetadata`、`ModelData`、`Bpa`、`Documents` 或 `Macros`，每个条目均设置为 `Deny`、`Read` 或 `Write`。此模型打开时，这些权限会提升您在聊天中的常驻授权。MCP 服务器仅读取全局授权，因此此处没有任何内容会传到它那里。

### 凭据的加密方式

所有敏感信息都会使用您自己的用户帐户下的 Windows 数据保护 API 进行加密，因此包含加密数据的文件无法与其他用户共享或移动到其他计算机。根据所保护的内容，会出现三种形状：

不包含密码的连接字符串完全不加密，仍是纯 JSON 字符串，这就是为什么在实践中“WorkspaceConnection”以两种形式出现的原因。

如果值无法解密（例如，因为文件来自其他用户），则该值将被读取为空，而不是导致加载失败。

## 当文件无法读取时

模型可以带或不带 `.tmuo` 文件打开。

如果文件无法反序列化，例如由于文件被手动编辑为无效的 JSON，Tabular Editor 会显示一个标题为*加载用户选项文件时发生错误(.tmuo)*的警告，其中包含底层错误，然后使用默认选项打开模型。模型本身不会丢失任何内容；您会丢失文件所包含的设置，下次保存时会写入新的设置。

## 后续步骤

- @workspace-mode