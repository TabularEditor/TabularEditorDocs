---
uid: xmla-as-connectivity
title: XMLA / Analysis Services 连接性
author: Daniel Otykier
updated: 2024-05-01
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

Tabular Editor 使用 [AMO 客户端库](https://learn.microsoft.com/en-us/analysis-services/amo/developing-with-analysis-management-objects-amo?view=asallproducts-allversions) 连接到 Power BI / Fabric XMLA endpoint，或 SQL Server 或 Azure Analysis Services（Tabular）实例。 身份验证和授权由 AMO 客户端库处理，这意味着 Tabular Editor 不会存储任何凭据或令牌。 此外，用户需要具备足够的权限，才能连接到 XMLA endpoint 或 Analysis Services 实例。 在大多数情况下，用户必须是 Analysis Services 服务器管理员角色的成员，或在 Power BI Workspace 中拥有管理员权限。 身份验证和授权由 AMO 客户端库处理，这意味着 Tabular Editor 不会存储任何凭据或令牌。 此外，用户需要具备足够的权限，才能连接到 XMLA endpoint 或 Analysis Services 实例。 在大多数情况下，用户必须是 Analysis Services 服务器管理员角色的成员，或在 Power BI Workspace 中拥有管理员权限。

在下文中，我们用“语义模型服务器”来指通过 Power BI / Fabric XMLA endpoint 访问的服务，或任意 SQL Server Analysis Services Tabular（SSAS）或 Azure Analysis Services（AAS）实例。

## 连接对话框

要连接到语义模型服务器，请依次选择 **文件** > **打开** > **从数据库加载模型...**，或按 **Ctrl+Shift+O**。

这将打开 **从数据库加载语义模型** 对话框，你可以在其中指定服务器名称、XMLA 连接字符串，或从下拉列表中选择本地 SSAS 实例。 此外，你还可以指定要使用的身份验证类型。 此外，你还可以指定要使用的身份验证类型。

> [!NOTE]
> 在 Tabular Editor 2.x 中，**高级选项**（用于指定读/写模式和自定义状态栏颜色）不提供。

![连接对话框](~/content/assets/images/connect-dialog.png)

## 选择数据库

点击“确定”后，Tabular Editor 会连接到语义模型服务器，并获取你有权访问的数据库列表。 选择你要使用的数据库，然后点击“确定”。 选择你要使用的数据库，然后点击“确定”。

## 高级连接字符串属性

在 Tabular Editor 的所有版本中，你都可以在 **Server** 文本框中指定一个 OLAP 连接字符串，而不只是服务器名称。

典型的 OLAP 连接字符串如下所示：

```
Provider=MSOLAP;Data Source=servername;Initial Catalog=databasename;Integrated Security=SSPI;
```

> [!NOTE]
> 如果在连接字符串中指定了 `Initial Catalog` 属性，则不会显示 **选择数据库** 对话框，Tabular Editor 将直接连接到指定的数据库。

除上述属性外，OLAP 连接字符串还支持许多其他属性。 除上述属性外，OLAP 连接字符串还支持许多其他属性。 如需完整的属性列表，请参阅 [Microsoft 文档](https://learn.microsoft.com/en-us/analysis-services/instances/connection-string-properties-analysis-services?view=asallproducts-allversions)。

除了文档中列出的属性外，AMO 连接字符串还支持以下属性：

### 区域设置标识符

你可以通过设置 `Locale Identifier` 属性来指定连接所使用的语言。 该值是一个数字，对应一种特定语言。 例如，`1033` 对应英语（美国）。 该值是一个数字，对应一种特定语言。 例如，`1033` 对应英语（美国）。

```
Provider=MSOLAP;Data Source=servername;Initial Catalog=databasename;Integrated Security=SSPI;Locale Identifier=1033;
```

如果你希望错误信息和其他服务器信息以特定语言显示，这会很有用。 如果未指定 `Locale Identifier` 属性，则使用客户端操作系统的语言。

大多数 Analysis Services 实例支持多种语言。 大多数 Analysis Services 实例支持多种语言。 完整的区域设置标识符（LCID）列表请参阅 [此页面](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-fulltext-languages-transact-sql?view=sql-server-ver16)。

## Fabric/Power BI XMLA 设置

要在 Fabric/Power BI 中启用 XMLA endpoint，必须启用两个管理员设置。

### 启用租户 XMLA endpoint

在 Fabric/Power BI 管理门户中，必须启用集成设置“允许 XMLA endpoints，并使用本地语义模型在 Excel 中进行分析”

在租户级别，该设置可能会被限制为仅允许特定用户使用。 在租户级别，该设置可能会被限制为仅允许特定用户使用。 如果你的组织对该设置做了限制，请确保所有需要的用户都被允许在租户级别使用 XMLA endpoint。

![Tennant Admin Setting](~/content/assets/images/common/XMLASettings/TennantAdminSetting.png)

### 在容量上启用 XMLA 读写

要使用 XMLA endpoint，承载语义模型的 Workspace 必须分配到容量（FSku 或 Power BI Premium Per User），并且该容量必须在容量设置中将 XMLA 设置为 ["Read Write" enabled in the capacity settings.](https://learn.microsoft.com/en-us/power-bi/enterprise/service-premium-connect-tools#enable-xmla-read-write)

![Tennant Admin Setting](~/content/assets/images/common/XMLASettings/CapacityAdminSetting.png)

要在 Admin Portal 中启用 Read Write，请依次导航至

1. 容量设置
2. 选择容量类型
3. 选择相应的容量
4. 转到 Power BI Workloads，向下滚动找到 XMLA endpoint 设置，然后选择“Read Write”

### Workspace 级别的用户权限

要使用 XMLA endpoint 编辑模型，用户账号需要在 Workspace 中拥有 **Contributor**、**Member** 或 **Admin** 权限。 在 Workspace 中选择“Manage Access”，添加该用户账号，或添加该用户所属的 Entra ID 组，并分配所需角色。 有关 Workspace 中角色的更多信息，可以查看 Microsoft 文档：[Roles in Workspaces](https://learn.microsoft.com/en-us/fabric/fundamentals/roles-workspaces) 在 Workspace 中选择“Manage Access”，添加该用户账号，或添加该用户所属的 Entra ID 组，并分配所需角色。 有关 Workspace 中角色的更多信息，可以查看 Microsoft 文档：[Roles in Workspaces](https://learn.microsoft.com/en-us/fabric/fundamentals/roles-workspaces)

### 语义模型的读/写权限

确保用户账号对该语义模型具有 Write 权限。 即使用户如上所述是 Workspace 的管理员，也可能仍然需要此权限。 即使用户如上所述是 Workspace 的管理员，也可能仍然需要此权限。

要确认你的账号具备所需权限，请先在 Fabric/Power BI 的 Workspace 中找到该模型，然后点击汉堡菜单图标 (3 个竖点)，并转到 "Manage permissions" 页面。

![在语义模型上管理权限](~/content/assets/images/common/XMLASettings/ManagePermissionsonSemanticModel.png)

核实或为用户账号或其所属的 Entra ID 组授予以下任一权限：**Workspace Admin**、**Workspace Contributor**，或在语义模型上具有 **Write permission**。 例如，在下面的截图中，只有以蓝色标出的 3 位用户可以通过 Tabular Editor 访问该模型： 例如，在下面的截图中，只有以蓝色标出的 3 位用户可以通过 Tabular Editor 访问该模型：

![语义模型上的用户权限](~/content/assets/images/common/XMLASettings/UserPermissionsonSemanticModel.png)

### 将 Workspace 设置为大型语义模型存储格式

为确保通过 XMLA endpoint 编辑模型时获得最佳体验，Workspace 应将其语义存储格式设置为 **Large Semantic model storage format**。 在 Fabric/Power BI workspace 右上角进入“Workspace Settings”。 先进入 'License info'，然后确认存储格式是否已设置为 large；如果没有，选择 'Edit' 以更改存储格式。 在 Fabric/Power BI workspace 右上角进入“Workspace Settings”。 先进入 'License info'，然后确认存储格式是否已设置为 large；如果没有，选择 'Edit' 以更改存储格式。

![大型语义模型存储格式](~/content/assets/images/common/XMLASettings/LargeSemanticModelStorageFormat.png)

## 其他 Fabric/Power BI 设置。

### 禁用组件刷新

如果除语义模型所有者之外的其他用户需要通过 XMLA endpoint 编辑该模型，则必须在 Fabric/Power BI 中禁用名为“阻止重新发布并禁用组件刷新”的安全管理员设置。

![租户管理员设置-禁用组件刷新](~/content/assets/images/common/XMLASettings/DisablePackageRefresh.png)

## 不支持的模型类型

有几种类型的模型不支持 XMLA 连接，[如下所列](https://learn.microsoft.com/en-us/power-bi/enterprise/service-premium-connect-tools#unsupported-semantic-models)。

以下语义模型无法通过 XMLA endpoint 访问。 这些语义模型不会显示在 Tabular Editor 或任何其他工具的 Workspace 下。 这些语义模型不会显示在 Tabular Editor 或任何其他工具的 Workspace 下。

- 基于对 Azure Analysis Services 或 SQL Server Analysis Services 模型的实时连接的语义模型。
- 基于对另一个 Workspace 中 Power BI 语义模型的实时连接的语义模型。
- 通过 REST API 推送数据的语义模型。
- 我的 Workspace 中的语义模型。
- Excel 工作簿语义模型

在 Fabric 中，Lakehouse 或 Warehouse 的默认语义模型可以在 Tabular Editor 中打开或连接，但[不能编辑](https://learn.microsoft.com/en-us/power-bi/enterprise/service-premium-connect-tools#considerations-and-limitations)。 此外，某些需要对特定 [DMVs](https://learn.microsoft.com/en-us/analysis-services/instances/use-dynamic-management-views-dmvs-to-monitor-analysis-services?view=asallproducts-allversions) 具有读取权限的操作，例如收集 VertiPaq分析器统计信息，在默认语义模型上可能不受支持。 此外，某些需要对特定 [DMVs](https://learn.microsoft.com/en-us/analysis-services/instances/use-dynamic-management-views-dmvs-to-monitor-analysis-services?view=asallproducts-allversions) 具有读取权限的操作，例如收集 VertiPaq分析器统计信息，在默认语义模型上可能不受支持。

## XMLA 连接故障排除

<a name="testing-a-simple-connection"></a>

### 测试简单连接

以下步骤展示了如何以最可靠的方式从 Tabular Editor 连接到 Fabric/Power BI 语义模型。

1. 在 Fabric 中连接到语义模型：通过“File”>“Open”>“Model from DB”（默认快捷键 Ctrl+Shift+O）

2. 系统会弹出一个对话框（见下图），你需要将 Power BI 连接字符串填入标为“Server”的文本框中。 其余选项保持与截图一致（这些是默认值）。 连接字符串的格式如下所示。 系统会弹出一个对话框（见下图），你需要将 Power BI 连接字符串填入标为“Server”的文本框中。 其余选项保持与截图一致（这些是默认值）。 连接字符串的格式如下所示。 你可以在 Power BI 服务中找到这个连接字符串（更多细节见这篇 [Microsoft 文档中“Connecting to a Premium Workspace”和“To get the workspace connection URL”两个部分](https://learn.microsoft.com/en-us/power-bi/enterprise/service-premium-connect-tools#connecting-to-a-premium-workspace)

![从数据库加载模型](~/content/assets/images/common/XMLASettings/LoadModelFromDatabase.png)

请直接从 Workspace 复制并粘贴连接字符串，不要从其他来源复制，也不要以任何方式修改。

3. 根据你的计算机配置（例如你的 Windows 登录是否已关联到 Entra ID 或身份提供程序），你可能会被提示登录。 请务必使用对 Workspace 具有权限的账户。 如果你的组织有多个租户，或你有多个登录账户，这可能和你的 Windows 登录账户不一致。 请使用 Fabric Web UI 中为你的用户显示的确切凭据。

![Authenticate to FabricPowerBI](~/content/assets/images/common/XMLASettings/AuthenticateToFabricPowerBI.png)

4. 成功完成身份验证后，会弹出“选择数据库”对话框。 选择一个，然后点击“Ok”。 选择一个，然后点击“Ok”。

![Choose Database](~/content/assets/images/common/XMLASettings/ChooseDatabase.png)

### 将身份验证类型设置为 Microsoft Entra ID

在某些情况下，“集成”安全选项使用的用户账户，可能并不是你用来对 Fabric/Power BI 服务进行身份验证的账户。 下一步是在打开模型对话框中选择 **Microsoft Entra MFA** 选项。

![Microsoft Entra MFA](~/content/assets/images/common/XMLASettings/LoadModelFromDatabaseMicrosoftEntraID.png)

选择“Microsoft Entra MFA”选项会强制进行多重身份验证，并允许你选择连接到 Workspace 所需的特定账户。

### 多个租户

如果你已按上述步骤反复核对了用户名和连接字符串但仍然有问题，下一步可以检查：在连接字符串中加入租户 GUID 是否会有所帮助。 如果你属于多个租户，可能就会遇到这个问题。 如果你属于多个租户，可能就会遇到这个问题。

可在 Power BI 中点击右上角的问号，然后选择“关于 Power BI”，直接找到租户 ID。 租户 ID 会显示在“租户 URL”的一部分中。 注意：在 Power BI 中，该文本框通常太小，无法在窗口里完整显示。 双击显示的 URL，即可选中整段内容，然后就可以复制并粘贴。 租户 ID 会显示在“租户 URL”的一部分中。 注意：在 Power BI 中，该文本框通常太小，无法在窗口里完整显示。 双击显示的 URL，即可选中整段内容，然后就可以复制并粘贴。

整个 URL 并不是租户 ID。 租户 ID 是该字符串末尾、在“ctid=”之后的 GUID。 因此在下面的截图里，我的租户 ID 以“ddec”开头，但你的会不同。 整个 URL 并不是租户 ID。 租户 ID 是该字符串末尾、在“ctid=”之后的 GUID。 因此在下面的截图里，我的租户 ID 以“ddec”开头，但你的会不同。 拿到租户 ID 后，你就可以修改上面使用的连接字符串：将路径中写着“myorg”的那一段替换为你的租户 ID。

示例如下。 示例如下。 你的租户 ID 和 Workspace 名称会与此处显示的不同。

- 旧：`powerbi://api.powerbi.com/v1.0/myorg/WorkspaceName`
- 新：`powerbi://api.powerbi.com/v1.0/eeds65sv-kl25-4d12-990a-770ca3eb6226/WorkspaceName`

你也可以像[这篇文章](https://learn.microsoft.com/en-us/fabric/enterprise/powerbi/service-premium-connect-tools#connecting-to-a-premium-workspace)中所示，使用租户名称（例如 `fabrikam.com`）。

然后，严格按照[测试简单连接](#testing-a-simple-connection)部分的说明尝试连接

### 重复名称

如果 Workspace 名称与另一个 Workspace 重名，或模型名称与另一个模型重名，则连接到模型时可能会出现问题。

如果存在重名，请参阅 Microsoft 文档中的[“重复 Workspace 名称”和“重复语义模型名称”](https://learn.microsoft.com/en-us/power-bi/enterprise/service-premium-connect-tools#duplicate-workspace-names)部分，了解如何通过修改连接字符串来解决这些问题

### 代理处理

另一个常见的连接问题原因是代理服务器。 想了解更多，可以看看[这篇文章](xref:proxy-settings)。

### 使用 PowerShell 测试连接

如果在尝试了上述故障排除步骤后连接问题仍然存在，也可以使用 [Microsoft 提供的 Analysis Services 客户端库](https://www.nuget.org/packages/Microsoft.AnalysisServices/) 直接连接到 XMLA endpoint，而 _无需_ 使用 Tabular Editor。 我们可以使用下面所示的简单 PowerShell 脚本来完成。 如果这个连接也失败了，就可以明确判断问题与 Tabular Editor 无关；此时，你应该考虑向 Microsoft 提交支持工单。 联系 Microsoft 时，请告知你使用的 **Microsoft.AnalysisServices.Tabular.dll** 和 **Microsoft.Identity.Client.dll** 的版本，并一并附上 PowerShell 脚本。 另外，也要说明你使用的是这些 DLL 的 .NET Core（Tabular Editor 3）版本，还是 .NET Framework（Tabular Editor 2）版本。 在支持请求中尽量不要直接提及 Tabular Editor，因为这可能会让他们的一线支持人员产生困惑。 创建支持工单后，也通过 support@tabulareditor.com 告诉我们一声，因为我们想跟踪此类问题的发生频率。 我们可以使用下面所示的简单 PowerShell 脚本来完成。 如果这个连接也失败了，就可以明确判断问题与 Tabular Editor 无关；此时，你应该考虑向 Microsoft 提交支持工单。 联系 Microsoft 时，请告知你使用的 **Microsoft.AnalysisServices.Tabular.dll** 和 **Microsoft.Identity.Client.dll** 的版本，并一并附上 PowerShell 脚本。 另外，也要说明你使用的是这些 DLL 的 .NET Core（Tabular Editor 3）版本，还是 .NET Framework（Tabular Editor 2）版本。 在支持请求中尽量不要直接提及 Tabular Editor，因为这可能会让他们的一线支持人员产生困惑。 创建支持工单后，也通过 support@tabulareditor.com 告诉我们一声，因为我们想跟踪此类问题的发生频率。

使用脚本的方法：

1. 通过 Windows 资源管理器进入 Tabular Editor 3 的安装文件夹
2. 在文件夹空白处单击右键，然后选择“在终端中打开”。 这应该会打开一个 PowerShell 窗口。 在文件夹空白处单击右键，然后选择“在终端中打开”。 这应该会打开一个 PowerShell 窗口。 你也可以打开常规命令窗口，输入 `pwsh` 来启动 PowerShell。
3. 确认 PowerShell 版本至少为 6.2.0。 如果受限语言模式导致无法运行脚本，请尝试以管理员身份打开终端，或联系你的 IT 管理团队协助运行该脚本。 如果受限语言模式导致无法运行脚本，请尝试以管理员身份打开终端，或联系你的 IT 管理团队协助运行该脚本。
4. 用记事本打开后，将下面脚本中的 XMLA URL 调整为你要连接的端点地址。 然后，将修改后的脚本复制到 PowerShell 窗口中，按下 [Enter] 键运行。 然后，将修改后的脚本复制到 PowerShell 窗口中，按下 [Enter] 键运行。

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

如果脚本执行 **成功**，说明你的计算机可以使用 Microsoft 客户端库连接到 XMLA endpoint。 如果脚本执行 **成功**，说明你的计算机可以使用 Microsoft 客户端库连接到 XMLA endpoint。 如果你同时 **无法** 使用 Tabular Editor 连接，可以在我们的 [Tabular Editor 2](https://github.com/TabularEditor/TabularEditor/issues) 或 [Tabular Editor 3](https://github.com/TabularEditor/TabularEditor3/issues) 支持页面提交工单，或发送邮件至 support@tabulareditor.com（**仅限 Tabular Editor 3 企业版客户**）。

如果脚本 **失败**，说明你的环境中有某些因素阻止了与 XMLA endpoint 的连接，因此 Tabular Editor 也将无法连接。 这种情况下，你可以先找你们的 IT 部门排查防火墙/代理问题，再去联系 Microsoft 支持。 这种情况下，你可以先找你们的 IT 部门排查防火墙/代理问题，再去联系 Microsoft 支持。

如果脚本在使用 Tabular Editor 2 的 DLL 时 **成功**，但在使用 Tabular Editor 3 的 DLL 时 **失败**（或反过来），你可以联系 Microsoft 支持，因为这类问题通常是 DLL 的 .NET Framework 版本（Tabular Editor 2 使用）和 DLL 的 .NET Core 版本（Tabular Editor 3 使用）之间存在差异导致的。
