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

当你从磁盘打开模型时，会在模型旁边创建该文件，文件名由模型名称和你的 Windows 用户名组成。每次从磁盘加载模型时，Tabular Editor 都会查找同名文件。

| 你打开的内容                                                                  | 用户选项文件                             |
| ----------------------------------------------------------------------- | ---------------------------------- |
| `SpaceParts.bim`，或任何 `.bim` / `.pbit` / `Database.json` 文件              | `SpaceParts.<UserName>.tmuo`，紧挨着它  |
| 一个 `model.tmdl` 或 `database.tmdl` 文件                                    | `model.<UserName>.tmuo`，紧挨着它       |
| 包含 `Database.json` 的文件夹                                                 | `database.<UserName>.tmuo`，位于该文件夹中 |
| 包含 Tabular Model Definition Language (TMDL) 模型文件的文件夹 | `model.<UserName>.tmuo`，位于该文件夹中    |

为了与早于 `database.tmdl` 的版本保持延续性，TMDL 始终使用 `model` 前缀。

如果模型是通过连接打开而不是从磁盘打开的，就没有地方把该文件放在模型旁边，因此它会按服务器和数据库分别保存在 `%LocalAppData%\\TabularEditor3\\UserOptions\\` 下。

是否会为新模型创建该文件，取决于 @偏好 下的 _创建用户选项 (.tmuo) 文件_ 设置。

> [!IMPORTANT]
> **.tmuo** 文件包含用户专属的偏好设置，因此不应将其纳入共享的版本控制环境。如果你使用 Git 进行版本控制，请确保在 `.gitignore` 文件中加入 `.tmuo` 扩展名。

## 文件内容

该文件采用 JSON 格式，所有属性都是可选的。 Tabular Editor 只有在有内容需要存储时才会写入该文件，因此实际文件通常只包含下面的少数几个块，而不是全部。如果没有任何内容需要存储，就完全不会生成文件。

下面是一个最简文件示例，适用于只连接到 Workspace 数据库的模型：

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

| 属性                            | 类型     | 写入时机                                                            |
| ----------------------------- | ------ | --------------------------------------------------------------- |
| `UseWorkspace`                | 布尔值    | 你已经回答过此模型的 Workspace 相关问题。在缺少该属性时，Tabular Editor 会在每次加载模型时都询问你。 |
| `WorkspaceConnection`         | 字符串或对象 | 已设置 Workspace 连接。如果连接字符串包含密码，则使用对象形式。                           |
| `WorkspaceConnectionAuthMode` | 字符串    | 已弃用，且仅在其不为 `Integrated` 时写入。身份验证模式现在可由连接字符串推断。                  |
| `WorkspaceDatabase`           | 字符串    | 已设置 Workspace 数据库名称。                                            |
| `Deployment`                  | 对象     | 已对该模型运行过 Deployment Wizard。                                     |
| `DataSourceOverrides`         | 对象     | 已定义至少一个数据源覆盖项。                                                  |
| `TableImportSettings`         | 对象     | 至少有一个数据源具有导入设置。                                                 |
| `RefreshOverrides`            | 对象     | 至少定义了一个刷新覆盖配置文件。                                                |
| `AIConsent`                   | 对象     | 旧版。如果存在则读取，但绝不会回写。                                              |
| `Permissions`                 | 对象     | 已授予至少一项按模型划分的 AI 授权。                                            |

它们按该顺序出现。

### Workspace 数据库

- `UseWorkspace`：决定 Tabular Editor 在加载模型时是否连接到 Workspace 数据库。 Workspace 数据库将被所加载的文件或文件夹结构的元数据覆盖。
- `WorkspaceConnection`：是 Workspace 数据库要部署到的 Analysis Services 实例或 Power BI XMLA endpoint。
- `WorkspaceDatabase`：该 Workspace 数据库的名称。为每位开发者、每个模型设置唯一名称，因为这样每位开发者都能拥有自己的数据库。

### 数据源覆盖

`DataSourceOverrides` 用于为 Workspace 数据库提供与模型文件不同的连接信息，使 Analysis Services 刷新时从模型所述位置之外的其他位置获取数据。

| 属性                  | 类型   | 写入时机                                                                                                                                                         |
| ------------------- | ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `ImpersonationMode` | 字符串  | 非 `Default`。以下值之一：`Default`、`ImpersonateAccount`、`ImpersonateAnonymous`、`ImpersonateCurrentUser`、`ImpersonateServiceAccount`、`ImpersonateUnattendedAccount`。 |
| `Username`          | 字符串  | 已指定。                                                                                                                                                         |
| `ConnectionString`  | 加密对象 | 已设置。                                                                                                                                                         |
| `Password`          | 加密对象 | 已设置。                                                                                                                                                         |
| `AccountKey`        | 加密对象 | 已设置。用于 Blob 存储数据源。                                                                                                                                           |
| `PrivacySetting`    | 字符串  | 已设置。                                                                                                                                                         |

如果某个覆盖项对应的数据源在模型中已不存在，则在下次写入文件时会将其删除；如果其数据源已重命名，则该覆盖项也会随之重命名。

### 表导入设置

运行 [导入表或架构更新](xref:importing-tables) 时，会使用 `TableImportSettings` 来浏览可用的表和视图，并获取源架构的更改。

| 属性                                    | 类型    | 写入时机                                                                                                                                                                    |
| ------------------------------------- | ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ServerType`                          | 字符串   | 始终。以下之一：`Sql`、`Oracle`、`Odbc`、`OleDb`、`Snowflake`、`Dataflow`、`PostgreSql`、`MySql`、`MariaDb`、`Db2`、`Databricks`、`OneLake`。                                               |
| `Options`                             | 字符串对象 | 当属性包不为空时。                                                                                                                                                               |
| `UserId`                              | 字符串   | 已设置。                                                                                                                                                                    |
| `Password`                            | 加密对象  | 已设置，_&#x4E14;_&#x4F60;选择了保存。                                                                                                                                            |
| `提供方`                                 | 字符串   | `ServerType` 为 `OleDb`。                                                                                                                                                 |
| `PasswordKey`、`UserIdKey`             | 字符串   | `ServerType` 为 `OleDb`，并且已设置相应的值。                                                                                                                                       |
| `服务器`                                 | 字符串   | `ServerType` 不是 `Odbc`，并且已设置。                                                                                                                                           |
| `ServerKey`、`DatabaseKey`             | 字符串   | `ServerType` 不是 `Sql`，并且已设置该值。                                                                                                                                          |
| `数据库`                                 | 字符串   | 已设置。                                                                                                                                                                    |
| `身份验证`                                | 字符串   | `ServerType` 为 `Sql`、`OleDb` 或 `Databricks`。以下值之一：`Sql`、`WindowsIntegrated`、`AadInteractive`、`AadPassword`、`AadIntegrated`、`AadServicePrincipal`、`AccessToken`、`OAuth`。 |
| `Encrypt`                             | 布尔值   | 无论设置为 true 还是 false，都会写入。                                                                                                                                               |
| `Dsn`                                 | 字符串   | 设置后。用于 ODBC。                                                                                                                                                            |
| `RowLimitClause`, `IdentifierQuoting` | 数值    | 非默认值时。                                                                                                                                                                  |
| `Schema`                              | 字符串   | 设置后。                                                                                                                                                                    |

`Options` 用来保存特定于某个提供程序的内容，全部以纯字符串形式存储：Snowflake Warehouse 对应 `Options.warehouse`，OneLake Workspace 对应 `Options.workspaceid`。`…Key` 属性表示连接字符串键&#x7684;_&#x540D;称_，例如 `PWD`，而不是机密本身。

`Password` 是这里唯一加密存储的值。 `UserId`、`Server`、`Database`、`Dsn` 以及 `Options` 中的所有内容都以纯文本存储，所以即使文件里没有密码，也要把它当作敏感文件。 Power BI 访问令牌存储为 `Password`，并会被加密。

### 部署

`Deployment` 保存的是 Deployment Wizard 上次用于这个模型的设置。这六个布尔选项一旦该块存在就总会写入，无论其值为 true 还是 false：

| 属性                              | 类型     | 写入条件                                  |
| ------------------------------- | ------ | ------------------------------------- |
| `DeployDataSources`             | 布尔值    | 始终                                    |
| `DeployPartitions`              | 布尔值    | 始终                                    |
| `DeployRefreshPolicyPartitions` | 布尔值    | 始终                                    |
| `DeployModelRoles`              | 布尔值    | 始终                                    |
| `DeployModelRoleMembers`        | 布尔值    | 始终                                    |
| `DeploySharedExpressions`       | 布尔值    | 始终                                    |
| `TargetConnectionString`        | 字符串或对象 | 始终写入；未设置时为 `null`。当连接字符串包含密码时，使用对象形式。 |
| `TargetDatabase`                | 字符串    | 始终写入；未设置时为 `null`。                    |
| `TargetCredentials`             | 对象     | 用户名和密码均已设置。                           |

### 刷新覆盖项

`RefreshOverrides` 使用配置文件名称作为键，而该键也是存储该名称的唯一位置。每个配置文件都包含一个 `Overrides` 数组，用于说明该配置文件运行时会更改哪些内容。有关这些配置文件的作用以及如何定义它们，见 @refresh-overrides。

```json
"RefreshOverrides": {
  "Nightly": {
    "Overrides": [
      {
        "scope": { "table": "Sales" },
        "分区": [
          {
            "originalObject": { "table": "Sales", "分区": "Sales-2025" },
            "source": { "query": "SELECT * FROM dbo.FactSales WHERE Year = 2025" }
          }
        ]
      }
    ]
  }
}
```

### 按模型的 AI 权限

当你在 @ai-assistant 的权限卡片上选择 **允许用于此模型** 时，会写入 `Permissions`，用于记录仅适用于该模型的 AI 权限授予。

```json
"Permissions": {
  "Grants": { "ModelMetadata": "Write", "ModelData": "Read" },
  "LastGrantedAt": "2026-09-15T08:12:44.117Z"
}
```

`Grants` 会为你已授予权限的每种资源各记录一项：`ModelMetadata`、`ModelData`、`Bpa`、`Documents` 或 `Macros`，每项的值为 `Deny`、`Read` 或 `Write`。在该模型打开期间，这些设置会提升你在此聊天中的常设授权级别。 MCP 服务器只读取全局授权，因此这里的设置不会传递给它。

### 凭据的加密方式

所有敏感信息都会在你自己的用户账户下使用 Windows Data Protection API 加密，因此包含加密数据的文件既不能与其他用户共享，也不能移到另一台计算机上使用。根据受保护内容的不同，会出现三种形式：

不包含密码的连接字符串完全不会加密，会保持为普通的 JSON 字符串；这也是为什么在实际使用中，`WorkspaceConnection` 既会以明文也会以加密形式出现。

如果某个值无法解密，例如文件来自另一位用户，系统会将该值读取为空，而不是让加载失败。

## 文件无法读取时

无论是否存在 `.tmuo` 文件，模型都可以打开。

如果该文件无法反序列化，例如被手动编辑成了无效的 JSON，Tabular Editor 会显示一个标题为 _加载用户选项文件 (.tmuo) 时出错_ 的警告，其中包含底层错误信息，然后使用默认选项打开模型。模型本身不会丢失任何内容；丢失的只是该文件中保存的设置，下一次保存时会写入一个新的文件。

## 后续步骤

- @workspace-mode