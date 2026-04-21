---
uid: connecting-to-azure-databricks
title: 连接到 Azure Databricks
author: David Bojsen
updated: 2026-04-17
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.15.0
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# （教程）连接到 Azure Databricks

Tabular Editor 3 支持将 Azure Databricks 连接为语义模型的数据源。 本教程将引导你完成设置与 Azure Databricks 的连接并从中导入数据的流程。 本教程将引导你完成设置与 Azure Databricks 的连接并从中导入数据的流程。

## 先决条件

开始之前，先确认你具备以下条件：

- 有效的 Azure Databricks Workspace
- 访问 Databricks 数据的相应权限
- Tabular Editor 3（桌面版、商业版或企业版）
- 你电脑上安装的 [Databricks ODBC Driver](https://www.databricks.com/spark/odbc-drivers-download)

> [!IMPORTANT]
> Databricks 已发布新的 ODBC 驱动程序，用于取代旧版 Simba Spark ODBC Driver。 我们建议安装新的 [Databricks ODBC Driver](https://www.databricks.com/spark/odbc-drivers-download)。 Tabular Editor 3.26.0 及更高版本支持这两种驱动程序，但从今往后建议优先使用新驱动程序。 旧版 Simba 驱动程序可从 [Databricks ODBC 驱动程序存档](https://www.databricks.com/spark/odbc-drivers-archive#simba_odbc) 下载。 我们建议安装新的 [Databricks ODBC Driver](https://www.databricks.com/spark/odbc-drivers-download)。 Tabular Editor 3.26.0 及更高版本支持这两种驱动程序，但从今往后建议优先使用新驱动程序。 旧版 Simba 驱动程序可从 [Databricks ODBC 驱动程序存档](https://www.databricks.com/spark/odbc-drivers-archive#simba_odbc) 下载。

## 连接器实现方式

Tabular Editor 使用 Power Query `Databricks.Catalogs()` 函数连接到 Databricks。 此函数支持两种连接器实现： 此函数支持两种连接器实现：

- **实现 2.0 (ADBC)：** 使用 [Arrow Database Connectivity](https://learn.microsoft.com/en-us/power-query/connectors/databricks#arrow-database-connectivity-driver-connector-implementation-preview) 驱动程序。 这是 Tabular Editor 3.26.1 及更高版本中的默认实现，也与 Power BI Desktop 使用的默认设置一致。 较新的 Databricks Workspace 需要使用此实现。 这是 Tabular Editor 3.26.1 及更高版本中的默认实现，也与 Power BI Desktop 使用的默认设置一致。 较新的 Databricks Workspace 需要使用此实现。
- **实现 1.0（旧版）：** 原始的连接器实现。 **实现 1.0（旧版）：** 原始的连接器实现。 它在较旧的 Databricks Workspace 中仍可运行，但在较新的 Workspace 中会因“目录为空”错误而失败。

> [!NOTE]
> 运行 Tabular Editor 的计算机上无需安装 ADBC 驱动程序。 仅需 Databricks ODBC 驱动程序即可。 仅需 Databricks ODBC 驱动程序即可。

> [!IMPORTANT]
> 如果您已有使用 Tabular Editor 3.26.0 或更早版本创建的 M 查询，这些查询使用旧版实现（`Databricks.Catalogs()` 的第三个参数为 `null`）。 如果您在较新的 Databricks Workspace 中遇到刷新错误，请将这些查询更新为使用实现 2.0。 有关分步说明，请参阅 [Databricks 刷新因目录为空错误而失败](xref:databricks-refresh-empty-catalog)。 如果您在较新的 Databricks Workspace 中遇到刷新错误，请将这些查询更新为使用实现 2.0。 有关分步说明，请参阅 [Databricks 刷新因目录为空错误而失败](xref:databricks-refresh-empty-catalog)。

## 身份验证方式

连接到 Azure Databricks 时，您可以使用以下几种身份验证方法：

### 1。 1。 Microsoft Entra ID（原 Azure AD）身份验证

如果你的组织使用 Microsoft Entra ID，建议采用这种方式连接到 Azure Databricks。 这种方法可提供无缝的单点登录，并通过托管身份提升安全性。 这种方法可提供无缝的单点登录，并通过托管身份提升安全性。

#### 关于 Tabular Editor 企业应用

当您使用 Microsoft Entra ID 身份验证连接到 Azure Databricks 时，Tabular Editor 会使用一个已注册的企业应用，名称为“Tabular Editor 3 - User Delegated Access to Azure Databricks”，其应用程序（客户端）ID 为：`ea0fc0fe-ed02-40d7-a29a-cc0a59d8b42c`。

此企业应用需要以下 API 权限：

- **Microsoft Graph** (`00000003-0000-0000-c000-000000000000`)
  - `offline_access`（委托）- 此权限允许 Tabular Editor 即使在您未主动使用该应用时，也能持续访问您已授权的数据。 这是维持与 Databricks 持续连接所必需的。 这是维持与 Databricks 持续连接所必需的。
  - `openid`（委托）- 允许用户使用其工作或学校账户登录该应用，并允许该应用查看基本的用户个人资料信息。
  - `profile`（委托）- 允许该应用查看基本个人资料信息，例如姓名、电子邮件地址、照片和用户名。
  - `User.Read`（委托）- 允许该应用读取您的个人资料，并在访问 Databricks API 时识别您的身份。

- **Azure Databricks API** (`2ff814a6-3304-4ab8-85cb-cd0e6f879c1d`)
  - `user_impersonation`（委托）- 代表已登录用户访问 Azure Databricks。 `user_impersonation`（委托）- 代表已登录用户访问 Azure Databricks。 这使 Tabular Editor 能够使用您的凭据连接到您的 Databricks Workspace。

有关 Microsoft Entra ID 权限的更多信息，请参阅 [Microsoft 关于权限类型的文档](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-permissions-and-consent) 和 [应用同意体验](https://learn.microsoft.com/en-us/azure/active-directory/develop/application-consent-experience)。

> [!IMPORTANT]
> Tabular Editor 需要这些权限，才能通过您的 Microsoft Entra ID 凭据安全访问您的 Azure Databricks 数据。 [!IMPORTANT]
> Tabular Editor 需要这些权限，才能通过您的 Microsoft Entra ID 凭据安全访问您的 Azure Databricks 数据。 如果没有这些权限，Tabular Editor 将无法对您的 Azure Databricks Workspace 进行正确的身份验证。

#### Microsoft Entra ID 身份验证的同意流程

当您首次尝试使用 Microsoft Entra ID 身份验证连接到 Azure Databricks 时，系统可能会提示您同意所需的权限。 同意流程取决于您组织的 Microsoft Entra ID 策略： 同意流程取决于您组织的 Microsoft Entra ID 策略：

##### 用户同意

如果您的组织允许用户对应用程序授予同意：

1. 您会看到来自 Microsoft 的同意提示，要求授权 Tabular Editor 代表您访问 Azure Databricks
2. 查看正在请求的权限
3. 点击 **Accept** 以授予同意

> [!NOTE]
> 是否需要管理员同意取决于您组织的 Microsoft Entra ID 策略，而不一定取决于正在请求的具体 API 权限。 许多组织允许用户自行同意委托权限，而另一些组织则要求所有第三方应用程序无论权限级别如何都必须由管理员批准。 许多组织允许用户自行同意委托权限，而另一些组织则要求所有第三方应用程序无论权限级别如何都必须由管理员批准。

##### 需要管理员同意

如果贵组织限制用户同意（企业环境中很常见）：

1. 你会收到一条错误信息，提示需要管理员同意
2. 你需要联系 IT 部门或 Microsoft Entra ID 管理员
3. 向他们提供以下信息：
   - 应用程序名称：“Tabular Editor 3 - User Delegated Access to Azure Databricks”
   - 应用程序 ID：`ea0fc0fe-ed02-40d7-a29a-cc0a59d8b42c`
   - 所需权限：Microsoft Graph（offline_access、openid、profile、User.Read）以及 Azure Databricks API（user_impersonation）

管理员可以通过以下两种方式之一为整个组织授予同意：

**选项 1：通过 Microsoft Entra ID 管理门户**

1. 依次转到 Microsoft Entra ID > 企业应用程序
2. 搜索“Tabular Editor 3 - User Delegated Access to Azure Databricks”
3. 选择该应用，然后转到“权限”
4. 点击“为 [Organization] 授予管理员同意”

**选项 2：使用管理员同意直接 URL**
管理员可以使用以下直达链接授予同意：

```
https://login.microsoftonline.com/organizations/v2.0/adminconsent?client_id=ea0fc0fe-ed02-40d7-a29a-cc0a59d8b42c&scope=https://graph.microsoft.com/offline_access%20https://graph.microsoft.com/openid%20https://graph.microsoft.com/profile%20https://graph.microsoft.com/User.Read%202ff814a6-3304-4ab8-85cb-cd0e6f879c1d/user_impersonation&redirect_uri=https://tabulareditor.com
```

有关管理员同意的更多信息，请参阅 Microsoft 文档：[配置用户如何同意应用程序](https://learn.microsoft.com/en-us/azure/active-directory/manage-apps/configure-user-consent)。

#### Microsoft Entra ID 身份验证步骤：

1. 在 Tabular Editor 3 中，依次选择 **Model** > **Import tables...**
2. 选择 **New Source** > **Databricks**
3. 在连接对话框中：
   - 输入你的 Databricks Workspace URL（格式：`https://<region>.azuredatabricks.net`）
   - 选择 **Microsoft Entra ID** 作为身份验证方法
   - 在 HTTP Path 中，指定 Databricks Warehouse 的路径（例如：`/sql/1.0/warehouses/<warehouse-id>`）

> [!NOTE]
> 你的 Databricks Workspace URL 应采用 `https://<region>.azuredatabricks.net` 格式——例如：`https://westeurope.azuredatabricks.net`。

### 2。 2。 个人访问令牌（PAT）身份验证

如果 Microsoft Entra ID 集成不可用，或你更偏好基于令牌的身份验证，则可以使用个人访问令牌。

#### PAT 身份验证步骤：

1. 在 Azure Databricks Workspace 中生成个人访问令牌：
   - 前往你的 Databricks Workspace
   - 点击右上角的用户头像图标
   - 选择 **用户设置**
   - 切换到 **访问令牌** 选项卡
   - 点击 **生成新令牌**
   - 输入名称，并可选设置过期时间
   - 点击 **生成**，然后复制令牌值

2. 在 Tabular Editor 3 中，依次选择 **模型** > **导入表...**

3. 选择 **新建源** > **Databricks**

4. 在连接对话框中：
   - 输入你的 Databricks Workspace URL
   - 选择 **个人访问令牌** 作为身份验证方法
   - 将令牌粘贴到 Token 字段中
   - 在 HTTP Path 中，指定你的 Databricks Warehouse 路径（例如 `/sql/1.0/warehouses/<warehouse-id>`）

### 3) 3) OAuth 机器对机器 (M2M) 身份验证

从 Tabular Editor 3.26.1 开始，您可以使用 OAuth 机器对机器 (M2M) 流，通过 Databricks 服务主体进行身份验证。 这对于无人值守场景很有用——例如计划刷新或 CI/CD 管道——因为您不希望连接绑定到某个特定用户的凭据。 OAuth (M2M) 适用于所有 Databricks 云平台（Azure、AWS 和 GCP）。 这对于无人值守场景很有用——例如计划刷新或 CI/CD 管道——因为您不希望连接绑定到某个特定用户的凭据。 OAuth (M2M) 适用于所有 Databricks 云平台（Azure、AWS 和 GCP）。

#### 先决条件

- 在目标 SQL Warehouse 上具有 **Can Use** 权限的 Databricks 服务主体
- 在 Databricks 帐户控制台或 Workspace 设置中生成的、用于该服务主体的 OAuth **Client ID** 和 **Client Secret**

#### OAuth (M2M) 身份验证步骤：

1. 在 Tabular Editor 3 中，依次选择 **Model** > **Import tables...**
2. 选择 **新建源** > **Databricks**
3. 在连接对话框中：
   - 请输入 Databricks Workspace URL
   - 选择 **OAuth (M2M)** 作为身份验证方式
   - 输入服务主体的 **Client ID** 和 **Client Secret**
   - 在 HTTP Path 中，指定 SQL Warehouse 的路径（例如 `/sql/1.0/warehouses/<warehouse-id>`）

> [!NOTE]
> Databricks ODBC 驱动程序会自动获取并刷新 OAuth 令牌，Tabular Editor 端无需额外配置。

## 查找你的 HTTP Path

HTTP Path 参数对连接到 Databricks SQL Warehouse 至关重要。 查找该值的方法： 查找该值的方法：

1. 前往你的 Databricks Workspace
2. 依次选择 **SQL** > **SQL Warehouse**
3. 选择你要连接的 SQL Warehouse
4. 找到 **连接详细信息** 部分
5. 复制 HTTP Path 的值，格式应为：`/sql/1.0/warehouses/<warehouse-id>`

## 从 Databricks 导入表

完成连接配置后：

1. 点击 **测试连接**，验证你的凭据和连接设置
2. 如果连接成功，点击 **下一步**
3. 选择是导入特定表/视图，还是使用自定义 SQL 查询
4. 如果选择表/视图：
   - 浏览可用的目录、架构和表
   - 选择要导入的表
   - 可选择预览并筛选列
5. 核对所选内容，然后点击 **导入** 完成

## 排查连接问题

如果你在连接到 Azure Databricks 时遇到问题：

- 确认你的 Workspace URL 正确且可访问
- 确保您的 Personal Access Token 未过期（如果使用 PAT 身份验证）
- 检查你的用户账户在 Databricks 中是否具备所需权限
- 确认 HTTP Path 指向处于活动状态的 SQL Warehouse
- 确保你的网络允许连接到 Databricks 服务

### Databricks 相关故障排除指南

- [Databricks 刷新失败：空目录错误](xref:databricks-refresh-empty-catalog) —— 从较新版本的 Databricks Workspace 导入后刷新失败
- [Databricks 列注释长度错误](xref:databricks-column-comments-length) —— 当列注释超过 512 个字符时，导入失败

### 解决 Microsoft Entra ID 身份验证问题

如果你使用 Microsoft Entra ID 身份验证并遇到错误：

#### “AADSTS65001: 用户或管理员尚未同意使用此应用程序”

当未授予所需权限时，会出现该错误：

1. 如果你有足够的权限：
   - 点击错误信息中的同意链接
   - 查看并接受权限请求

2. 如果你没有足够的权限：
   - 联系你的 IT 管理员
   - 向他们提供应用程序 ID：`ea0fc0fe-ed02-40d7-a29a-cc0a59d8b42c`
   - 请他们为 Tabular Editor 企业应用授予组织级别的同意

#### "AADSTS700016: Application with identifier was not found in the directory"

如果你的组织启用了受限应用策略，可能会出现此问题：

1. 联系你的 Microsoft Entra ID 管理员
2. 请他们将 Tabular Editor 企业应用程序（ID：`ea0fc0fe-ed02-40d7-a29a-cc0a59d8b42c`）添加到你组织的允许应用程序列表中

> [!TIP]
> 在某些组织中，IT 部门在批准新的企业应用程序之前，可能需要提交正式申请或进行安全审查。 [!TIP]
> 在某些组织中，IT 部门在批准新的企业应用程序之前，可能需要提交正式申请或进行安全审查。 你需要说明：该应用由 Tabular Editor 3 使用，借助组织现有的 Microsoft Entra ID 身份验证基础架构，安全连接到 Azure Databricks 资源。

## 在 Databricks 中使用“更新表架构”

从 Azure Databricks 导入表后，你可以使用 Tabular Editor 的“**更新表架构**”功能，让模型与 Databricks 表中的更改保持同步。

要更新架构：

1. 在 TOM Explorer 中右键单击已导入的表
2. 选择“**更新表架构**”
3. 查看检测到的更改，并按需应用

对于复杂查询，或在架构检测过程中遇到问题时，可以参考 [更新表架构](xref:importing-tables#updating-table-schema-through-analysis-services) 文档中的说明，在“**工具**” > “**偏好**” > “**架构比较**”下启用“**使用 Analysis Services 进行更改检测**”选项。
