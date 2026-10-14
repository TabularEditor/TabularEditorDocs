---
uid: user-options
title: 用户选项（.tmuo）文件
author: Daniel Otykier
updated: 2026-09-15
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

# Tabular Model 用户选项（.tmuo）文件

Tabular Editor 3 引入了一种新的基于 JSON 的文件，用于存储开发者和模型专用的偏好设置。这个文件叫做 **Tabular Model User Options** 文件，并使用 **.tmuo** 文件扩展名。

当您从磁盘打开模型时，系统会在模型旁边创建该文件，文件名由模型名称和您的 Windows 用户名组成。每次从磁盘加载模型时，Tabular Editor 都会查找同名的文件。

| 您打开的项目                                                                  | 用户选项文件                                 |
| ----------------------------------------------------------------------- | -------------------------------------- |
| `SpaceParts.bim`，或任何 `.bim` / `.pbit` / `Database.json` 文件              | `SpaceParts.<UserName>.tmuo`，与其位于同一目录中 |
| `model.tmdl` 或 `database.tmdl` 文件                                       | `model.<UserName>.tmuo`，与其位于同一目录中      |
| 包含 `Database.json` 的文件夹                                                 | `database.<UserName>.tmuo`，位于该文件夹中     |
| 包含 Tabular Model Definition Language (TMDL) 模型文件的文件夹 | `model.<UserName>.tmuo`，位于该文件夹中        |

TMDL 始终使用 `model` 前缀，以延续早于 `database.tmdl` 的版本中的命名方式。

对于通过连接而非从磁盘打开的模型，由于无法在模型旁边存放该文件，因此会按服务器和数据库分别将其保存在 `%LocalAppData%\TabularEditor3\UserOptions\` 下。

是否会为新模型创建该文件，取决于 @preferences 下的 _创建用户选项（.tmuo）文件_ 偏好设置。

> [!IMPORTANT]
> **.tmuo** 文件包含用户特定的偏好，因此不应将其纳入共享的版本控制环境。如果你使用 Git 进行版本控制，请确保在 `.gitignore` 文件中加入 `.tmuo` 扩展名。

## 文件内容

该文件采用 JSON 格式，所有属性都是可选的。 Tabular Editor 只会在有内容需要存储时才写入文件，因此实际生成的文件只会包含下列区块中的少数几个，而不是全部。如果没有任何内容需要存储，就根本不会生成文件。

一个最小文件示例，适用于仅连接到 Workspace 数据库、除此之外不做任何操作的模型：

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

### 顶层属性

| 属性                            | 类型     | 写入条件                                                          |
| ----------------------------- | ------ | ------------------------------------------------------------- |
| `UseWorkspace`                | 布尔值    | 你已为该模型回答了 Workspace 相关问题。如果没有这个属性，Tabular Editor 每次加载模型时都会询问。 |
| `WorkspaceConnection`         | 字符串或对象 | 已设置 Workspace 连接。当连接字符串包含密码时，使用对象形式。                          |
| `WorkspaceConnectionAuthMode` | 字符串    | 仅为兼容旧版而保留，且仅在其不是 `Integrated` 时写入。现在可由连接字符串推断出身份验证模式。         |
| `WorkspaceDatabase`           | 字符串    | 已设置 Workspace 数据库名称。                                          |
| `Deployment`                  | 对象     | 已对该模型运行过 Deployment Wizard。                                   |
| `DataSourceOverrides`         | 对象     | 已定义至少一个数据源覆盖项。                                                |
| `TableImportSettings`         | 对象     | 至少有一个数据源具有导入设置。                                               |
| `RefreshOverrides`            | 对象     | 至少定义了一个刷新覆盖配置文件。                                              |
| `AIConsent`                   | 对象     | 旧版。存在时会读取，但绝不会回写。                                             |
| `Permissions`                 | 对象     | 至少已授予一项针对单个模型的 AI 授权。                                         |

它们按该顺序出现。

### Workspace 数据库

- `UseWorkspace` 决定 Tabular Editor 在加载模型时是否连接到 Workspace 数据库。 Workspace 数据库会被已加载的文件或文件夹结构中的元数据覆盖。
- `WorkspaceConnection` 是 Workspace 数据库要部署到的 Analysis Services 实例或 Power BI XMLA endpoint。
- `WorkspaceDatabase` 是该 Workspace 数据库的名称。应为每位开发人员、每个模型设置唯一值，因为目的就是让每位开发人员都有自己的数据库。

### 数据源覆盖

`DataSourceOverrides` 用于让 Workspace 数据库使用与模型文件中不同的连接信息，这样 Analysis Services 就会从模型所指定位置以外的数据源刷新数据。

| 属性                  | 类型   | 写入条件                                                                                                                                                          |
| ------------------- | ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ImpersonationMode` | 字符串  | 不是 `Default`。以下值之一：`Default`、`ImpersonateAccount`、`ImpersonateAnonymous`、`ImpersonateCurrentUser`、`ImpersonateServiceAccount`、`ImpersonateUnattendedAccount`。 |
| `Username`          | 字符串  | 已设置时写入。                                                                                                                                                       |
| `ConnectionString`  | 加密对象 | 已设置时写入。                                                                                                                                                       |
| `Password`          | 加密对象 | 已设置时写入。                                                                                                                                                       |
| `AccountKey`        | 加密对象 | 已设置时写入。用于 Blob 存储数据源。                                                                                                                                         |
| `PrivacySetting`    | 字符串  | 已设置时写入。                                                                                                                                                       |

如果某个覆盖项对应的数据源在模型中已不存在，则会在下次写入文件时被删除；如果其数据源已重命名，该覆盖项也会随之重命名。

### 表导入设置

运行 [导入表或架构更新](xref:importing-tables) 时，会使用 `TableImportSettings` 来浏览可用的表和视图，并获取源架构更改。

| 属性                                   | 类型    | 在以下情况下写入                                                                                                                                                                  |
| ------------------------------------ | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ServerType`                         | 字符串   | 始终写入。 `Sql`、`Oracle`、`Odbc`、`OleDb`、`Snowflake`、`Dataflow`、`PostgreSql`、`MySql`、`MariaDb`、`Db2`、`Databricks`、`OneLake` 之一。                                                |
| `Options`                            | 字符串对象 | 该包不是空的。                                                                                                                                                                   |
| `UserId`                             | 字符串   | 已设置。                                                                                                                                                                      |
| `Password`                           | 加密对象  | 已设置，_并&#x4E14;_&#x4F60;已选择将其保存。                                                                                                                                           |
| `Provider`                           | 字符串   | `ServerType` 为 `OleDb`。                                                                                                                                                   |
| `PasswordKey`、`UserIdKey`            | 字符串   | `ServerType` 为 `OleDb`，且已设置对应的值。                                                                                                                                          |
| `服务器`                                | 字符串   | `ServerType` 不是 `Odbc`，且已设置。                                                                                                                                              |
| `ServerKey`、`DatabaseKey`            | 字符串   | `ServerType` 不是 `Sql`，且已设置该值。                                                                                                                                             |
| `数据库`                                | 字符串   | 已设置。                                                                                                                                                                      |
| `身份验证`                               | 字符串   | `ServerType` 可以是 `Sql`、`OleDb` 或 `Databricks`。 `Sql`、`WindowsIntegrated`、`AadInteractive`、`AadPassword`、`AadIntegrated`、`AadServicePrincipal`、`AccessToken` 或 `OAuth` 之一。 |
| `Encrypt`                            | 布尔值   | 无论设为 true 还是 false，都会写入。                                                                                                                                                  |
| `Dsn`                                | 字符串   | 已设置时写入。用于 ODBC。                                                                                                                                                           |
| `RowLimitClause`、`IdentifierQuoting` | 数字    | 不为默认值时写入。                                                                                                                                                                 |
| `Schema`                             | 字符串   | 已设置时写入。                                                                                                                                                                   |

`Options` 用于存放特定于某个提供程序的内容，并以纯字符串形式保存：Snowflake 的 Warehouse 对应 `Options.warehouse`，OneLake 的 Workspace 对应 `Options.workspaceid`。`…Key` 属性保存的是连接字符串键&#x7684;_&#x540D;称_，例如 `PWD`，而不是机密本身。

`Password` 是这里唯一经过加密的值。 `UserId`、`Server`、`Database`、`Dsn` 以及 `Options` 中的所有内容都以纯文本存储，因此即使文件中不含密码，也要把它当作敏感文件处理。 Power BI 访问令牌存储在 `Password` 中，并且会被加密。

### 部署

`Deployment` 保存 Deployment Wizard 上次用于此模型的内容。一旦该块存在，这六个布尔选项就会始终写入，无论其值为 true 还是 false：

| 属性                              | 类型     | 写入时机                                  |
| ------------------------------- | ------ | ------------------------------------- |
| `DeployDataSources`             | 布尔值    | 始终                                    |
| `DeployPartitions`              | 布尔值    | 始终                                    |
| `DeployRefreshPolicyPartitions` | 布尔值    | 始终                                    |
| `DeployModelRoles`              | 布尔值    | 始终                                    |
| `DeployModelRoleMembers`        | 布尔值    | 始终                                    |
| `DeploySharedExpressions`       | 布尔值    | 始终                                    |
| `TargetConnectionString`        | 字符串或对象 | 始终返回；未设置时为 `null`。当连接字符串包含密码时，使用对象形式。 |
| `TargetDatabase`                | 字符串    | 始终返回；未设置时为 `null`。                    |
| `TargetCredentials`             | 对象     | 用户名和密码均已设置。                           |

### 刷新覆盖

`RefreshOverrides` 以配置文件名称为键，且该键是存储该名称的唯一位置。每个配置文件都包含一个 `Overrides` 数组，用于描述该配置文件运行时会更改哪些内容。有关这些配置文件的作用以及如何定义它们，请参阅 @refresh-overrides。

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

`Permissions` 会记录仅适用于该模型的 AI 权限授予；当你在 @ai-assistant 的权限卡片上选择 **允许用于此模型** 时，系统会将其写入其中。

```json
"Permissions": {
  "Grants": { "ModelMetadata": "Write", "ModelData": "Read" },
  "LastGrantedAt": "2026-09-15T08:12:44.117Z"
}
```

`Grants` 会为你已授权的每种资源各保存一条记录：`ModelMetadata`、`ModelData`、`Bpa`、`Documents` 或 `Macros`，每条都设置为 `Deny`、`Read` 或 `Write`。在你打开此模型期间，这些设置会提升该聊天的默认授权级别。 MCP 服务器只会读取全局授权，因此这里的任何内容都不会传到它那里。

### 凭据的加密方式

所有敏感信息都会在你自己的用户账户下使用 Windows Data Protection API 进行加密，因此包含加密数据的文件既无法与其他用户共享，也无法移动到另一台计算机上。根据受保护的内容不同，会出现三种形式：

不含密码的连接字符串完全不会加密，会保持为纯 JSON 字符串；因此在实际使用中，`WorkspaceConnection` 会以两种形式出现。

如果某个值无法解密，例如因为文件来自其他用户，则会将该值读取为空，而不是导致加载失败。

## 文件无法读取时

无论有没有 `.tmuo` 文件，模型都可以打开。

如果该文件无法反序列化，例如因为手动编辑后成了无效的 JSON，Tabular Editor 会显示一个标题为 _加载用户选项文件 (.tmuo) 时出错_ 的警告，其中包含底层错误信息，然后使用默认选项打开模型。模型本身不会丢失任何内容；丢失的是该文件保存的设置，而下一次保存时会写入一个新的文件。

## 后续步骤

- @Workspace-mode