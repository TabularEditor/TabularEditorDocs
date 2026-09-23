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

When you open a model from disk, the file is created next to it, named after it and after your Windows user name. Tabular Editor looks for a file with that name every time a model is loaded from disk.

| What you opened                                                                             | User options file                          |
| ------------------------------------------------------------------------------------------- | ------------------------------------------ |
| `SpaceParts.bim`, or any `.bim` / `.pbit` / `database.json` file                            | `SpaceParts.<UserName>.tmuo`, beside it    |
| A `model.tmdl` or `database.tmdl` file                                                      | `model.<UserName>.tmuo`, beside it         |
| A folder containing `database.json`                                                         | `database.<UserName>.tmuo`, in that folder |
| A folder containing Tabular Model Definition Language (TMDL) model files | `model.<UserName>.tmuo`, in that folder    |

TMDL always uses the `model` prefix, for continuity with versions that predate `database.tmdl`.

For a model opened over a connection rather than from disk there is nowhere beside the model to put the file, so it is kept per server and database under `%LocalAppData%\TabularEditor3\UserOptions\`.

Whether the file is created for a new model at all is governed by _Create user options (.tmuo) file_ under @preferences.

> [!IMPORTANT]
> **.tmuo** 文件包含用户专属的偏好设置，因此不应将其纳入共享的版本控制环境。如果你使用 Git 进行版本控制，请确保在 `.gitignore` 文件中加入 `.tmuo` 扩展名。

## 文件内容

The file is JSON and every property is optional. Tabular Editor writes one only when there's something to store, so a real file carries a handful of the blocks below rather than all of them. If nothing needs storing, no file is written at all.

A minimal file, for a model that does nothing but connect to a workspace database:

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

### Top-level properties

| 属性                            | Type             | Written when                                                                                                                                             |
| ----------------------------- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `UseWorkspace`                | Boolean          | You've answered the workspace question for this model. While it's absent, Tabular Editor asks each time the model loads. |
| `WorkspaceConnection`         | String or object | A workspace connection is set. Object form when the connection string carries a password.                                |
| `WorkspaceConnectionAuthMode` | String           | Legacy, and only when it isn't `Integrated`. The authentication mode is now implied by the connection string.            |
| `WorkspaceDatabase`           | String           | A workspace database name is set.                                                                                                        |
| `Deployment`                  | 对象               | The deployment wizard has run against this model.                                                                                        |
| `DataSourceOverrides`         | 对象               | At least one data source override is defined.                                                                                            |
| `TableImportSettings`         | 对象               | At least one data source has import settings.                                                                                            |
| `RefreshOverrides`            | 对象               | At least one refresh override profile is defined.                                                                                        |
| `AIConsent`                   | 对象               | Legacy. Read when present, never written back.                                                                           |
| `Permissions`                 | 对象               | At least one per-model AI grant has been given.                                                                                          |

They appear in that order.

### Workspace database

- `UseWorkspace` decides whether Tabular Editor connects to a workspace database when it loads the model. The workspace database is overwritten with the metadata of the loaded file or folder structure.
- `WorkspaceConnection` is the Analysis Services instance or Power BI XMLA endpoint the workspace database is deployed to.
- `WorkspaceDatabase` is the name of that database. Make it unique per developer and per model, since the whole point is that each developer gets their own.

### Data source overrides

`DataSourceOverrides` is usedto give the workspace database different connection details from the ones in the model file, so Analysis Services refreshes from somewhere other than what the model says.

| 属性                  | Type             | Written when                                                                                                                                                                                          |
| ------------------- | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ImpersonationMode` | String           | Not `Default`. One of `Default`, `ImpersonateAccount`, `ImpersonateAnonymous`, `ImpersonateCurrentUser`, `ImpersonateServiceAccount`, `ImpersonateUnattendedAccount`. |
| `Username`          | String           | Set.                                                                                                                                                                                  |
| `ConnectionString`  | Encrypted object | Set.                                                                                                                                                                                  |
| `Password`          | Encrypted object | Set.                                                                                                                                                                                  |
| `AccountKey`        | Encrypted object | Set. Used for blob storage sources.                                                                                                                                   |
| `PrivacySetting`    | String           | Set.                                                                                                                                                                                  |

An override whose data source no longer exists in the model is dropped the next time the file is written, and one whose data source was renamed follows the rename.

### Table import settings

`TableImportSettings` is used when you run [Import Table or Schema Update](xref:importing-tables), to browse the available tables and views and to pick up source schema changes.

| 属性                                    | Type              | Written when                                                                                                                                                                                                        |
| ------------------------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ServerType`                          | String            | Always. One of `Sql`, `Oracle`, `Odbc`, `OleDb`, `Snowflake`, `Dataflow`, `PostgreSql`, `MySql`, `MariaDb`, `Db2`, `Databricks`, `OneLake`.                                         |
| `Options`                             | Object of strings | The bag isn't empty.                                                                                                                                                                                |
| `UserId`                              | String            | Set.                                                                                                                                                                                                |
| `Password`                            | Encrypted object  | Set, _and_ you chose to save it.                                                                                                                                                                    |
| `Provider`                            | String            | `ServerType` is `OleDb`.                                                                                                                                                                            |
| `PasswordKey`, `UserIdKey`            | String            | `ServerType` is `OleDb` and the corresponding value is set.                                                                                                                                         |
| `Server`                              | String            | `ServerType` isn't `Odbc`, and it's set.                                                                                                                                                            |
| `ServerKey`, `DatabaseKey`            | String            | `ServerType` isn't `Sql`, and the value is set.                                                                                                                                                     |
| `Database`                            | String            | Set.                                                                                                                                                                                                |
| `Authentication`                      | String            | `ServerType` is `Sql`, `OleDb` or `Databricks`. One of `Sql`, `WindowsIntegrated`, `AadInteractive`, `AadPassword`, `AadIntegrated`, `AadServicePrincipal`, `AccessToken`, `OAuth`. |
| `Encrypt`                             | Boolean           | Set either way.                                                                                                                                                                                     |
| `Dsn`                                 | String            | Set. Used for ODBC.                                                                                                                                                                 |
| `RowLimitClause`, `IdentifierQuoting` | Number            | Not at their defaults.                                                                                                                                                                              |
| `Schema`                              | String            | Set.                                                                                                                                                                                                |

`Options` is where anything specific to one provider ends up, as plain strings: a Snowflake warehouse is `Options.warehouse`, a OneLake workspace is `Options.workspaceid`. The `…Key` properties are the _names_ of connection string keys, such as `PWD`, not secrets.

`Password` is the only encrypted value here. `UserId`, `Server`, `Database`, `Dsn` and everything in `Options` are stored as plain text, so treat the file as sensitive even when it holds no password. A Power BI access token is stored as `Password`, and is encrypted.

### 部署

`Deployment` holds what the deployment wizard last used for this model. The six Boolean options are always written once the block exists, whether they're true or false:

| 属性                              | Type             | Written when                                                                                                        |
| ------------------------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------- |
| `DeployDataSources`             | Boolean          | 始终                                                                                                                  |
| `DeployPartitions`              | Boolean          | 始终                                                                                                                  |
| `DeployRefreshPolicyPartitions` | Boolean          | 始终                                                                                                                  |
| `DeployModelRoles`              | Boolean          | 始终                                                                                                                  |
| `DeployModelRoleMembers`        | Boolean          | 始终                                                                                                                  |
| `DeploySharedExpressions`       | Boolean          | 始终                                                                                                                  |
| `TargetConnectionString`        | String or object | Always, `null` if unset. Object form when the connection string carries a password. |
| `TargetDatabase`                | String           | Always, `null` if unset.                                                                            |
| `TargetCredentials`             | 对象               | Both a user name and a password are set.                                                            |

### Refresh overrides

`RefreshOverrides` is keyed by profile name, and that key is the only place the name is stored. Each profile holds a single `Overrides` array describing what the profile changes when it runs. See @refresh-overrides for what the profiles do and how to define them.

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

### Per-model AI permissions

`Permissions` records the AI permission grants that apply to this model alone, written when you answer **Allow for this model** on a permission card in the @ai-assistant.

```json
"Permissions": {
  "Grants": { "ModelMetadata": "Write", "ModelData": "Read" },
  "LastGrantedAt": "2026-09-15T08:12:44.117Z"
}
```

`Grants` carries one entry per resource you've granted: `ModelMetadata`, `ModelData`, `Bpa`, `Documents` or `Macros`, each set to `Deny`, `Read` or `Write`. These raise your standing grant for the chat while this model is open. The MCP server reads the global grants only, so nothing here reaches it.

### How credentials are encrypted

Everything sensitive is encrypted with the Windows Data Protection API under your own user account, so a file containing encrypted data can't be shared with another user or moved to another machine. Three shapes appear, depending on what's being protected:

A connection string with no password in it isn't encrypted at all and stays a plain JSON string, which is why `WorkspaceConnection` appears both ways in practice.

If a value can't be decrypted, for instance because the file came from another user, the value is read as empty rather than failing the load.

## When the file cannot be read

A model opens with or without a `.tmuo` file.

If the file cannot be deserialized, for instance because it was hand-edited into invalid JSON, Tabular Editor shows a warning titled _Error loading User Options file (.tmuo)_ carrying the underlying error, and then opens the model with default options. Nothing is lost from the model itself; you lose the settings the file held, and the next save writes a fresh one.

## 后续步骤

- @workspace-mode