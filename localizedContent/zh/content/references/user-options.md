---
uid: user-options
title: 用户选项（.tmuo）文件
author: Daniel Otykier
updated: 2021-09-27
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

Tabular Editor 3 引入了一种新的基于 JSON 的文件，用于存储开发者和模型专用的偏好设置。 这个文件叫做 **Tabular Model User Options** 文件，并使用 **.tmuo** 文件扩展名。

当你在 Tabular Editor 3 中打开 Model.bim 或 Database.json 文件时，系统会使用你加载的文件名和你的 Windows 用户名来创建该文件。 例如，如果用户打开名为 `AdventureWorks.bim` 的文件，用户选项文件将保存为 `AdventureWorks.<UserName>.tmuo`，其中 `<UserName>` 是当前用户的 Windows 用户名。 每次从磁盘加载模型时，Tabular Editor 都会查找具有此类名称的文件。

> [!IMPORTANT]
> **.tmuo** 文件包含用户专属的偏好设置，因此不应将其纳入共享的版本控制环境。 如果你使用 Git 进行版本控制，请确保在 `.gitignore` 文件中加入 `.tmuo` 扩展名。

## 文件内容

下面是文件内容示例：

```json
{
  "UseWorkspace": true,
  "WorkspaceConnection": "provider=MSOLAP;data source=localhost",
  "WorkspaceDatabase": "WorkspaceDB_DanielOtykier_20210904_222118",
  "DataSourceOverrides": {
    "SQLDW": {
      "ConnectionString": {
        "Encryption": "UserKey",
        "EncryptedString": "..."
      },
      "PrivacySetting": "NA"
    }
  },
  "TableImportSettings": {
    "SQLDW": {
      "ServerType": "Sql",
      "UserId": "sqladmin",
      "Password": {
        "Encryption": "UserKey",
        "EncryptedString": "..."
      },
      "Server": "localhost",
      "Database": "AdventureWorksDW2019",
      "Authentication": 0
    }
  }
}
```

在此示例中，所示 JSON 属性含义如下：

- `UseWorkspace`：指示 Tabular Editor 在加载模型时是否应连接到 Workspace 数据库。 Workspace 数据库会用已加载的文件/文件夹结构中的元数据进行覆盖。 如果未提供此值，Tabular Editor 会在加载模型时提示用户是否要使用 Workspace 数据库。
- `WorkspaceConnection`：要将 Workspace 数据库部署到的 Analysis Services 实例或 Power BI XMLA 端点的服务器名称。
- `WorkspaceDatabase`：要部署的 Workspace 数据库名称。 理想情况下，它对每个开发者和每个模型来说都应该是唯一的。
- `DataSourceOverrides`：此结构可用于指定备用的数据源属性和凭据，这些属性和凭据将在每次部署 Workspace 数据库时使用。 如果 Model.bim 文件中包含你希望为 Workspace 数据库替换的数据源连接详细信息，这会很有用。例如，当你希望 Analysis Services 从与 Model.bim 文件中指定的不同数据源刷新数据时。
- `TableImportSettings`：每当使用 Tabular Editor 的 [导入表或架构更新](xref:importing-tables) 功能时，都会用到此结构。 此处指定的凭据和设置会在 Tabular Editor 连接到源时使用，用于浏览可用的表/视图，并在源发生更改后更新已导入表的架构。

.tmuo 文件中的所有凭据和连接字符串都会使用 Windows 用户密钥进行加密。 换句话说，包含加密数据的 .tmuo 文件无法在多个用户之间共享。

## 后续步骤

- @workspace-mode