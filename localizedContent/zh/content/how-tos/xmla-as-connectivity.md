---
uid: xmla-as-connectivity
title: XMLA / Analysis Services 连接性
author: Daniel Otykier
updated: 2026-09-14
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          partial: true
          note: "仅限高级每用户 XMLA 终结点"
        - edition: Enterprise
          full: true
---

# XMLA / Analysis Services 连接性

Tabular Editor 使用 [AMO 客户端库](https://learn.microsoft.com/en-us/analysis-services/amo/developing-with-analysis-management-objects-amo?view=asallproducts-allversions) 连接到 Power BI / Fabric XMLA endpoint，或 SQL Server 或 Azure Analysis Services（Tabular）实例。 Authentication and authorization is handled by the AMO client library, which means that Tabular Editor does not store any credentials or tokens. Moreover, users will need sufficient permissions to connect to the XMLA endpoint or Analysis Services instance. In most cases, the user must be a member of the Analysis Services server administrator role or have administrative permissions in the Power BI workspace.

在下文中，我们用“语义模型服务器”来指通过 Power BI / Fabric XMLA endpoint 访问的服务，或任意 SQL Server Analysis Services Tabular（SSAS）或 Azure Analysis Services（AAS）实例。

## 连接对话框

要连接到语义模型服务器，请依次选择 **文件** > **打开** > **从数据库加载模型...**，或按 **Ctrl+Shift+O**。

这将打开 **从数据库加载语义模型** 对话框，你可以在其中指定服务器名称、XMLA 连接字符串，或从下拉列表中选择本地 SSAS 实例。 Moreover, you can specify the type of authentication to use.

> [!NOTE]
> 在 Tabular Editor 2.x 中，**高级选项**（用于指定读/写模式和自定义状态栏颜色）不提供。

![连接对话框](~/content/assets/images/connect-dialog.png)

### Status bar color

**Advanced Options** includes a **Status bar color** picker. The color you choose is remembered with the connection, and Tabular Editor paints the status bar with it whenever a model is open on that server.

No particular color means anything in itself; assigning one is what matters. Giving production a color you would not choose for anything else makes it obvious, at a glance and without reading the server name, which environment the window in front of you is connected to. Leave it on **Default** to keep the theme's own status bar.

Closing the model restores the status bar to the active theme.

## 选择数据库

点击“确定”后，Tabular Editor 会连接到语义模型服务器，并获取你有权访问的数据库列表。 Select the database you want to work with, and click "OK".

## 高级连接字符串属性

在 Tabular Editor 的所有版本中，你都可以在 **Server** 文本框中指定一个 OLAP 连接字符串，而不只是服务器名称。

典型的 OLAP 连接字符串如下所示：

```
Provider=MSOLAP;Data Source=servername;Initial Catalog=databasename;Integrated Security=SSPI;
```

> [!NOTE]
> 如果在连接字符串中指定了 `Initial Catalog` 属性，则不会显示 **选择数据库** 对话框，Tabular Editor 将直接连接到指定的数据库。

OLAP connection strings support many properties in addition to the ones shown above. 如需完整的属性列表，请参阅 [Microsoft 文档](https://learn.microsoft.com/en-us/analysis-services/instances/connection-string-properties-analysis-services?view=asallproducts-allversions)。

除了文档中列出的属性外，AMO 连接字符串还支持以下属性：

### 区域设置标识符

你可以通过设置 `Locale Identifier` 属性来指定连接所使用的语言。 The value is a number that corresponds to a specific language. For example, `1033` corresponds to English (United States).

```
Provider=MSOLAP;Data Source=servername;Initial Catalog=databasename;Integrated Security=SSPI;Locale Identifier=1033;
```

This is useful if you want error messages and other server messages to be in a specific language. If the `Locale Identifier` property is not specified, the language of the client operating system is used.

Most Analysis Services instances support several languages. 完整的区域设置标识符（LCID）列表请参阅 [此页面](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-fulltext-languages-transact-sql?view=sql-server-ver16)。

## Fabric/Power BI XMLA 设置

XMLA read/write is enabled by default on all Fabric and Power BI capacities since June 2025. If you can't connect through the XMLA endpoint, verify that an admin hasn't disabled one of these two settings.

### Tenant XMLA endpoint setting

In the Fabric/Power BI admin portal, the integration setting "Allow XMLA endpoints and Analyze in Excel with on-premises semantic models" must be enabled.

At the tenant level, the setting may be restricted to only certain users. 如果你的组织对该设置做了限制，请确保所有需要的用户都被允许在租户级别使用 XMLA endpoint。

![Tenant admin setting](~/content/assets/images/common/XMLASettings/TennantAdminSetting.png)

### XMLA read/write on the capacity

To use the XMLA endpoint, assign the workspace that hosts the semantic model to a Fabric capacity (F SKU), a Power BI Embedded capacity (A or EM SKU), a legacy Premium capacity (P SKU) or a Premium Per User (PPU) license. The capacity must have the XMLA endpoint set to [**Read Write** in the capacity settings](https://learn.microsoft.com/en-us/fabric/enterprise/powerbi/service-premium-connect-tools#enable-xmla-read-write). This is the default since June 2025.

![Capacity admin setting](~/content/assets/images/common/XMLASettings/CapacityAdminSetting.png)

If read/write has been switched off, ask your capacity admin to re-enable it in the Admin Portal:

1. Open **Capacity Settings**.
2. Choose the type of capacity.
3. Select the relevant capacity.
4. Navigate to **Power BI Workloads** and set **XMLA Endpoint** to **Read Write**.

### Workspace 级别的用户权限

要使用 XMLA endpoint 编辑模型，用户账号需要在 Workspace 中拥有 **Contributor**、**Member** 或 **Admin** 权限。 In the workspace choose 'Manage Access' and add the user account or a Entra ID group that the user belongs to with the required role. For more information on roles in workspaces please see Microsoft's Documentation: [Roles in Workspaces](https://learn.microsoft.com/en-us/fabric/fundamentals/roles-workspaces)

### 语义模型的读/写权限

确保用户账号对该语义模型具有 Write 权限。 This can be required even if the user is an admin on the workspace as mentioned above.

要确认你的账号具备所需权限，请先在 Fabric/Power BI 的 Workspace 中找到该模型，然后点击汉堡菜单图标 (3 个竖点)，并转到 "Manage permissions" 页面。

![在语义模型上管理权限](~/content/assets/images/common/XMLASettings/ManagePermissionsonSemanticModel.png)

核实或为用户账号或其所属的 Entra ID 组授予以下任一权限：**Workspace Admin**、**Workspace Contributor**，或在语义模型上具有 **Write permission**。 For example, in the screenshot below, only the 3 users highlighted in Blue would be able to access the model through Tabular Editor:

![语义模型上的用户权限](~/content/assets/images/common/XMLASettings/UserPermissionsonSemanticModel.png)

### 将 Workspace 设置为大型语义模型存储格式

为确保通过 XMLA endpoint 编辑模型时获得最佳体验，Workspace 应将其语义存储格式设置为 **Large Semantic model storage format**。 Go to 'Workspace Settings' in the top right corner of the Fabric/Power BI workspace. First navigate to the 'License info', secondly validate if the storage format is set to large and if not choose 'Edit' to change the storage format.

![大型语义模型存储格式](~/content/assets/images/common/XMLASettings/LargeSemanticModelStorageFormat.png)

## 其他 Fabric/Power BI 设置。

### Disable Package Refresh

如果除语义模型所有者之外的其他用户需要通过 XMLA endpoint 编辑该模型，则必须在 Fabric/Power BI 中禁用名为“阻止重新发布并禁用组件刷新”的安全管理员设置。

![Block republish and disable package refresh setting](~/content/assets/images/common/XMLASettings/DisablePackageRefresh.png)

## 不支持的模型类型

有几种类型的模型不支持 XMLA 连接，[如下所列](https://learn.microsoft.com/en-us/power-bi/enterprise/service-premium-connect-tools#unsupported-semantic-models)。

以下语义模型无法通过 XMLA endpoint 访问。 These semantic models won't appear under the workspace in Tabular Editor or any other tool.

- 基于对 Azure Analysis Services 或 SQL Server Analysis Services 模型的实时连接的语义模型。
- 基于对另一个 Workspace 中 Power BI 语义模型的实时连接的语义模型。
- 通过 REST API 推送数据的语义模型。
- 我的 Workspace 中的语义模型。
- Excel 工作簿语义模型

在 Fabric 中，Lakehouse 或 Warehouse 的默认语义模型可以在 Tabular Editor 中打开或连接，但[不能编辑](https://learn.microsoft.com/en-us/power-bi/enterprise/service-premium-connect-tools#considerations-and-limitations)。 Moreover, some operations that require read access to certain [DMVs](https://learn.microsoft.com/en-us/analysis-services/instances/use-dynamic-management-views-dmvs-to-monitor-analysis-services?view=asallproducts-allversions), such as collecting VertiPaq Analyzer statistics, may not be supported on default semantic models.

## XMLA 连接故障排除

### 测试简单连接

以下步骤展示了如何以最可靠的方式从 Tabular Editor 连接到 Fabric/Power BI 语义模型。

1. 在 Fabric 中连接到语义模型：通过“File”>“Open”>“Model from DB”（默认快捷键 Ctrl+Shift+O）

2. You'll be presented with a dialogue (see below), and you need to put the Power BI connection string into the text box labeled 'Server'. Leave the rest of the options as configured in the screenshot (these are defaults). The connection string is in the form shown below. 你可以在 Power BI 服务中找到这个连接字符串（更多细节见这篇 [Microsoft 文档中“Connecting to a Premium Workspace”和“To get the workspace connection URL”两个部分](https://learn.microsoft.com/en-us/power-bi/enterprise/service-premium-connect-tools#connecting-to-a-premium-workspace)

![从数据库加载模型](~/content/assets/images/common/XMLASettings/LoadModelFromDatabase.png)

请直接从 Workspace 复制并粘贴连接字符串，不要从其他来源复制，也不要以任何方式修改。

3. Depending on your machine (if your Windows login is linked to Entra ID or your identity provider) you may be prompted to log in. It's important that the account you use is the one with permission to the workspace. If your organization has multiple tenants or if you have multiple logins, this might not match your Windows login. You should use the exact credential that is shown in the Fabric web UI for your user.

![Authenticate to FabricPowerBI](~/content/assets/images/common/XMLASettings/AuthenticateToFabricPowerBI.png)

4. 成功完成身份验证后，会弹出“选择数据库”对话框。 Select one and click 'Ok'.

![Choose Database](~/content/assets/images/common/XMLASettings/ChooseDatabase.png)

### 将身份验证类型设置为 Microsoft Entra ID

In some cases the 'Integrated' security option could be different from the user account that should be used for authenticating against the Fabric/Power BI service. The next step to take is to choose the **Microsoft Entra MFA** option in the open model dialog box.

![Microsoft Entra MFA](~/content/assets/images/common/XMLASettings/LoadModelFromDatabaseMicrosoftEntraID.png)

选择“Microsoft Entra MFA”选项会强制进行多重身份验证，并允许你选择连接到 Workspace 所需的特定账户。

### 多个租户

如果你已按上述步骤反复核对了用户名和连接字符串但仍然有问题，下一步可以检查：在连接字符串中加入租户 GUID 是否会有所帮助。 This might be an issue if you belong to multiple tenants.

可在 Power BI 中点击右上角的问号，然后选择“关于 Power BI”，直接找到租户 ID。 The tenant ID is shown as part of the 'Tenant URL'. Be careful, as the text box is typically too small to display the whole thing in the window in Power BI. Double-click on the URL shown, which will highlight the entire thing, that you can copy and paste.

The whole URL is not the tenant ID. The tenant ID is the GUID at the end of the string, after "ctid=". So in the screenshot below, my tenant ID starts with "ddec", but yours will be different. 拿到租户 ID 后，你就可以修改上面使用的连接字符串：将路径中写着“myorg”的那一段替换为你的租户 ID。

An example is below. 你的租户 ID 和 Workspace 名称会与此处显示的不同。

- 旧：`powerbi://api.powerbi.com/v1.0/myorg/WorkspaceName`
- 新：`powerbi://api.powerbi.com/v1.0/eeds65sv-kl25-4d12-990a-770ca3eb6226/WorkspaceName`

你也可以像[这篇文章](https://learn.microsoft.com/en-us/fabric/enterprise/powerbi/service-premium-connect-tools#connecting-to-a-premium-workspace)中所示，使用租户名称（例如 `fabrikam.com`）。

然后，严格按照[测试简单连接](#testing-a-simple-connection)部分的说明尝试连接

### 重复名称

如果 Workspace 名称与另一个 Workspace 重名，或模型名称与另一个模型重名，则连接到模型时可能会出现问题。

如果存在重名，请参阅 Microsoft 文档中的[“重复 Workspace 名称”和“重复语义模型名称”](https://learn.microsoft.com/en-us/power-bi/enterprise/service-premium-connect-tools#duplicate-workspace-names)部分，了解如何通过修改连接字符串来解决这些问题

### 代理处理

Another common cause of connectivity issues is proxies. For more information about this, please review [this article](xref:proxy-settings).

### 使用 PowerShell 测试连接

如果在尝试了上述故障排除步骤后连接问题仍然存在，也可以使用 [Microsoft 提供的 Analysis Services 客户端库](https://www.nuget.org/packages/Microsoft.AnalysisServices/) 直接连接到 XMLA endpoint，而 _无需_ 使用 Tabular Editor。 We can do this using a simple PowerShell script as shown below. If this connection also fails, it is a clear indication that the issue is unrelated to Tabular Editor; in this case, you should consider raising a support ticket with Microsoft. When contacting Microsoft, inform them of which version of the **Microsoft.AnalysisServices.Tabular.dll** and **Microsoft.Identity.Client.dll** you're using, and also include the PowerShell script. Also, inform them whether you're using the .NET Core (Tabular Editor 3) or .NET Framework (Tabular Editor 2) versions of the DLLs. Avoid mentioning Tabular Editor directly in your support request, as this may confuse their 1st-level support. After creating the support ticket, please also notify us via support@tabulareditor.com, as we are interested in tracking the frequency of these issues.

使用脚本的方法：

1. 通过 Windows 资源管理器进入 Tabular Editor 3 的安装文件夹
2. Right-click somewhere in the folder and choose "Open in Terminal". This should open a PowerShell window. 你也可以打开常规命令窗口，输入 `pwsh` 来启动 PowerShell。
3. 确认 PowerShell 版本至少为 6.2.0。 If the constrained language mode is restricted, try to open the terminal as an administrator or request assistance from your IT admin team to run the script.
4. 用记事本打开后，将下面脚本中的 XMLA URL 调整为你要连接的端点地址。 Then, copy the modified script into the PowerShell window and hit [Enter] to run it.

```powershell
# Run this script from the Tabular Editor 3 installation folder, since this folder
# contains all of the DLLs required.

# Config
# TODO: Update the XMLA URL below and modify connection string properties as needed
$xmla = "powerbi://api.powerbi.com/v1.0/myorg/workspace-name"
$connectionString = "Provider=MSOLAP;Data Source=$xmla;Interactive Login=Always;Identity Mode=Connection"

# Load DLLs
Add-Type -Path "Microsoft.AnalysisServices.Tabular.dll"

# Create Microsoft.AnalysisServices.Tabular.Server object:
$server = New-Object Microsoft.AnalysisServices.Tabular.Server

try {
	# Connect
	$server.Connect($connectionString)

	Write-Host "Connection succeeded." -ForegroundColor Green
	Write-Host "Connected to: $($server.Name)"
}
catch {
	Write-Host "Connection failed:" -ForegroundColor Red
	Write-Host $_.Exception.Message -ForegroundColor Red
}
```

If the script **succeeds**, it means that your machine is able to connect to the XMLA endpoint using the Microsoft client libraries. 如果你同时 **无法** 使用 Tabular Editor 连接，可以在我们的 [Tabular Editor 2](https://github.com/TabularEditor/TabularEditor/issues) 或 [Tabular Editor 3](https://github.com/TabularEditor/TabularEditor3/issues) 支持页面提交工单，或发送邮件至 support@tabulareditor.com（**仅限 Tabular Editor 3 企业版客户**）。

如果脚本 **失败**，说明你的环境中有某些因素阻止了与 XMLA endpoint 的连接，因此 Tabular Editor 也将无法连接。 In this case, please reach out to your IT department for troubleshooting firewalls/proxies, before contacting Microsoft support.

如果脚本在使用 Tabular Editor 2 的 DLL 时 **成功**，但在使用 Tabular Editor 3 的 DLL 时 **失败**（或反过来），你可以联系 Microsoft 支持，因为这类问题通常是 DLL 的 .NET Framework 版本（Tabular Editor 2 使用）和 DLL 的 .NET Core 版本（Tabular Editor 3 使用）之间存在差异导致的。
