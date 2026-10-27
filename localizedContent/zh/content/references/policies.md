---
uid: policies
title: 政策
author: Morten Lønskov
updated: 2026-10-23
applies_to:
  products:
    - product: Tabular Editor 2
      partial: true
      note: "Tabular Editor 2 reads the legacy registry key only, and honors only the policies marked TE2 below."
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          partial: true
          note: "General policies only"
        - edition: Business
          partial: true
          note: "General policies only"
        - edition: Enterprise
          full: true
    - product: Tabular Editor CLI
      partial: true
      note: "On Windows, and only for the policies marked CLI below."
---

# 策略

如果您为组织管理 Tabular Editor，则可以通过组策略限制其功能，并代表用户配置 AI 助手和 MCP 服务器。手动在 Windows 注册表中设置值，或使用 Tabular Editor 3 随附的管理模板。

大多数策略都是通用策略，在 Tabular Editor 3 的每个版本中都可用。配置 AI 助手和 MCP 服务器的策略需要[Tabular Editor 3 企业版](xref:editions)，并在下方标记为**企业版**。

> [!NOTE]
> 此功能需要以下版本的 Tabular Editor：
>
>   - Tabular Editor [2.17.0](https://github.com/TabularEditor/TabularEditor/releases/tag/2.17.0) 或更高版本
>   - Tabular Editor [3.3.5](https://github.com/TabularEditor/TabularEditor3/releases/tag/3.3.5) 或更高版本，用于常规策略
>   - Tabular Editor 3.27 或更高版本，适用于以下注册表项、整机策略以及所有企业策略
>   - Tabular Editor CLI 0.7 或更高版本

## 注册表键

策略从六个键中读取，定义值的第一个键决定该值。`HKEY_LOCAL_MACHINE` 下的每个键的优先级都高于 `HKEY_CURRENT_USER` 下的每个键，因此用户无法覆盖通过“计算机配置”设置的整机策略。在一个配置单元中，特定于产品的键的优先级高于共享键，而共享键的优先级又高于旧版键：

```
HKEY_LOCAL_MACHINE\Software\Policies\Tabular Editor ApS\TE3
HKEY_LOCAL_MACHINE\Software\Policies\Tabular Editor ApS
HKEY_LOCAL_MACHINE\Software\Policies\Kapacity\Tabular Editor
HKEY_CURRENT_USER\Software\Policies\Tabular Editor ApS\TE3
HKEY_CURRENT_USER\Software\Policies\Tabular Editor ApS
HKEY_CURRENT_USER\Software\Policies\Kapacity\Tabular Editor
```

- `Tabular Editor ApS\TE3` 仅由 Tabular Editor 3 读取。Tabular Editor CLI 读取的是 `Tabular Editor ApS\TECLI`；其他四个项对于两者来说是相同的。
- `Tabular Editor ApS` 是共享项，由 Tabular Editor 3 和 CLI 共同读取。
- `Kapacity\Tabular Editor` 是早期版本使用的项。该项仍会被读取，并且是 Tabular Editor 2 读取的唯一项，因此，如果还需要应用于 Tabular Editor 2，也请在该项中设置策略。

优先级分别适用于每个值：全机器范围的 `DisableTelemetry` 为 0 会覆盖每个用户的 `DisableTelemetry` 为 1，而仅针对每个用户设置的 `DisableCSharpScripts` 仍然适用。
值名称不区分大小写。

## 值类型

| 设置类型 | 注册表类型 | 注意事项 |
|--|--|--|
| 开/关策略 | `REG_DWORD` | 任何非零值都会强制执行该策略。`0`和不存在该值都表示不强制执行该策略。|
| 选择 | `REG_SZ` | 选择的名称，例如 `Read`，这是管理模板写入的内容。也接受包含选项在列表中的位置的 `REG_DWORD`。|
| 数字 | `REG_DWORD` | 管理模板写入的内容。也接受包含该数字的 `REG_SZ`。|
| 列表 | `REG_MULTI_SZ` | 每行一个条目。也接受条目由分号分隔的 `REG_SZ`。|
| 路径、地址或名称 | `REG_SZ` | |

Tabular Editor 在启动时读取一次策略值。更改将在您下次启动应用程序时生效。

## 常规策略

要强制执行其中一项，请添加一个具有以下名称和非零值的 `REG_DWORD` 值。“**产品**”列显示了哪些产品遵循该策略：**TE3** 是 Tabular Editor 3，**CLI** 是 Tabular Editor CLI，**TE2** 是 Tabular Editor 2，后者仅读取旧版键。

|值|产品|强制执行时……|
|--|--|--|
| DisableUpdates | TE3、TE2 | Tabular Editor 将不会检查是否有更新版本在线可用。用户也无法手动检查更新。|
| DisableCSharpScripts | TE3、TE2 | Tabular Editor 不允许用户创建或执行 C# 脚本。|
| DisableMacros | TE3、TE2 | Tabular Editor 不允许用户保存或运行宏。应用程序启动时，不会加载存储在`%LocalAppData%`文件夹中的宏。|
| DisableBpaDownload | TE3、CLI、TE2 | 无法从网络下载 Best Practice Analyzer 规则。存储在本地或与模型一起存储的规则仍可正常使用。|
| DisableWebDaxFormatter | TE3、CLI、TE2 | 已禁用将代码发送到 daxformatter.com 的 DAX 格式化工具。Tabular Editor 3 仍提供其内置的格式化工具，该工具不会通过网络发送任何内容。|
| DisableErrorReports | TE3 | 用户无法向 Tabular Editor 支持团队发送错误或崩溃报告。|
| DisableTelemetry | TE3、CLI | 不收集匿名使用数据，也不将此类数据发送给 Tabular Editor 支持团队。|
| DisableDaxOptimizer | TE3 | DAX Optimizer 集成不可用。|
| DisableDaxOptimizerUpload | TE3 | 用户无法通过 DAX Optimizer 集成上传 VertiPaq Analyzer 文件。当强制执行`DisableDaxOptimizer`时隐含。|
| RequireDaxOptimizerObfuscation | TE3 | 用户无法通过 DAX 优化器集成上传明文 VertiPaq 分析器文件；只能上传混淆的文件。当强制执行`DisableDaxOptimizer`或`DisableDaxOptimizerUpload`时隐含。|
| DisableDaxPackageManager | TE3 | DAX 包管理器不可用。|
| DisableAi | TE3 | 所有 AI 功能均已关闭：AI 助手、MCP 服务器和所有由 AI 提供支持的功能均不可用，应用程序启动时不会加载任何与 AI 相关的项，并且所有存储的提供商配置（包括 API 密钥）都将被清除。|
| DisableAiChat | TE3 | AI 助手聊天面板不可用。其他 AI 功能（包括 MCP 服务器）不受影响。|
| DisableMcpServer | TE3 | MCP 服务器不可用，因此外部代理工具无法连接到 Tabular Editor 3。AI 助手聊天不受影响。|
| RequireMcpAccessToken | TE3 | 连接到MCP服务器的客户端必须出示**“工具”>“MCP服务器…”**对话框中显示的访问令牌，用户无法关闭该要求。|
| RequireNativeLibrarySignatureVerification | TE3 | Tabular Editor 3 在加载代码编辑器库 `Scintilla.dll` 和 `Lexilla.dll` 之前，会验证其 Authenticode 签名。如果计算机无法验证发布者的证书链，代码编辑器将无法启动，Tabular Editor 3 将关闭。在组策略编辑器中，此策略的名称为**要求对代码编辑器支持库进行签名验证**。|

### 在 TE CLI 中

在 Windows 上，Tabular Editor CLI 遵循上述标记为 **CLI** 的策略，以与 Tabular Editor 3 相同的顺序读取相同的键。它还遵循以下[企业策略](#scripts-and-macros)中的 `BlockUnsafeScripts`，适用于 `te script`、`te macro run` 和 `te bpa run --fix`。

被拒绝的操作不会静默处理。`te` 会指明拒绝该操作的策略，并以非零代码退出，因此管道步骤会失败，而不是显示为成功但未执行任何操作。

CLI 没有版本，因此，无论计算机持有何种许可证，CLI 都会直接应用要求桌面应用程序使用 Tabular Editor 3 企业版的策略。

## 企业策略

这些策略决定了 C# 脚本可以执行的操作，并配置 AI 助手和 MCP 服务器。它们都需要 Tabular Editor 3 企业版，并属于 `Tabular Editor ApS\TE3` 下 - 但 `BlockUnsafeScripts` 除外，Tabular Editor CLI 也遵循该策略，因此它属于共享的 `Tabular Editor ApS` 项。改为将其置于 `TE3` 或 `TECLI` 下，以便仅影响两者之一。

### 脚本和宏

|值|类型|作用|
|--|--|--|
| BlockUnsafeScripts | 开/关 | 仅当 C# 脚本和宏位于语义模型内时，才允许使用它们。对于读取或写入文件、访问网络、启动其他程序、引入外部代码或直接向服务器发送命令的脚本，系统会在其运行之前拒绝。|

无论脚本在何处运行，此限制均适用：脚本文档中的**运行脚本**和**运行并预览**、Best Practice Analyzer 中的**应用修复**、AI 助手、MCP 服务器以及命令行中的 `te script`、`te macro run` 和 `te bpa run --fix`。被拒绝的脚本并不是失败的脚本。没有任何内容到达模型，错误列表保持为空，并且**脚本未运行**对话框会列出策略以及脚本所使用的内容。

超出模型范围的宏会被从每个菜单中排除，因此不会被意外运行。它仍列在**“视图”>“宏”**下，其**“已阻止”**列已填写，并且仍可打开和编辑，因此可以将其带回界限内，而无需从头开始重写。保存此类宏成功，并显示其已保存但不会运行。

是否算作停留在模型内是由分析已编译的脚本而非搜索其文本来决定的，因此通往同一位置的间接路径（反射、表达式树、`Activator`、`AppDomain`、XML 读取器或反序列化）也会被拒绝。在内置的[帮助程序方法](xref:script-helper-methods)中，在模型外部写入的三个方法 `SaveFile`、`ExecuteCommand` 和 `Bpa.ExportCsv` 被视为不安全；而仅进行读取的方法，包括 `ReadFile`、`ExecuteDax`、`EvaluateDax`、`ExecuteReader` 和 `ExportProperties`，则不被视为不安全。请参阅[管理员策略](xref:csharp-scripts#administrator-policies)，了解脚本作者方面的同一条规则。

在组策略编辑器中，此策略名为**仅允许停留在模型内的脚本和宏**，并且由于它被写入共享项，因此它直接位于**管理模板 > Tabular Editor** 下，而不是位于**Tabular Editor 3** 子文件夹中。

### 权限限制

其中每一项都对 AI 助手和 MCP 服务器可以访问的某种资源设定了上限。可接受的值为 `Deny`、`Read` 和 `Write`，但模型数据除外，对于模型数据，`Read` 是最高有意义的设置。

限制对用户可以授予的权限设置上限：高于该限制的现有权限将被降至该限制，**工具 > 首选项 > AI 功能 > 权限**下的匹配选项以及**工具 > MCP 服务器…**对话框中的匹配选项将显示为只读，并且 AI 助手将不再请求无法授予的权限。任何授权都不能超过限制——无论是长期权限、针对单个模型的权限，还是在早期版本中授予的权限。用户的偏好设置中保留其自己的选择，因此如果删除策略，该选择将恢复。

|值|可接受的值|限制对……的访问|
|--|--|--|
| MaxModelMetadataAccess | 拒绝、读取、写入 | 打开模型的元数据：表、列和度量值名称、表达式、描述、Best Practice Analyzer 结果和 VertiPaq 统计信息。`Write` 还允许助手对模型运行其自身的 C# 脚本。如果设置为`Deny`，则完全不会发送有关打开的模型的任何信息：没有模型摘要，没有模型已更改的通知，也没有当前所选内容。|
| MaxModelDataAccess | 拒绝、读取 | 来自模型的数据值，即 DAX 查询的结果。|
| MaxBpaAccess | 拒绝、读取、写入 | Best Practice Analyzer 规则。`Read` 允许列出规则并运行分析；`Write` 还允许添加和更改规则。|
| MaxDocumentsAccess | 拒绝、读取、写入 | 用户已打开的文档，例如 C# 脚本和 DAX 查询。`Read` 允许读取其内容；`Write` 还允许对其进行更改。|
| MaxMacrosAccess | 拒绝、读取、写入 | 用户的宏库。|
| McpMaxModelMetadataAccess | 拒绝、读取、写入 | 仅针对 MCP 服务器的相同五项资源。|
| McpMaxModelDataAccess | 拒绝、读取 | |
| McpMaxBpaAccess | 拒绝、读取、写入 | |
| McpMaxDocumentsAccess | 拒绝、读取、写入 | |
| McpMaxMacrosAccess | 拒绝、读、写 | |

五个`McpMax...`值仅适用于 MCP 服务器。当其中一个未设置时，MCP 服务器将继承相应的 `Max...` 限制。它们只能降低该限制，绝不能提高该限制，因此无人值守代理的权限绝不能超过交互式助手的权限。

### AI 提供程序

|值|类型|可接受的值|作用|
|--|--|--|--|
| AiProvider | 选择 | None、OpenAI、Anthropic、AzureOpenAI、Custom | 将 AI 助手锁定到一个提供商。`None` 会关闭 AI 助手；MCP 服务器不受影响。|
| AiEndpoint | 地址 | | 锁定请求发送到的端点或基本 URL，例如内部网关或 Azure OpenAI 资源。|
| AiModel | 名称 | | 锁定模型或 Azure OpenAI 部署名称。聊天面板中的模型选择器被一个普通指示器替换，因此用户无法切换模型。|
| AiOrganizationId | 名称 | | 锁定向其计费的 OpenAI 组织请求。|
| AiProjectId | 名称 | | 锁定 OpenAI 项目请求的计费对象。|
| AiAllowedProviders | 列表 | 上述任何提供程序名称 | 限制用户可以配置的提供程序。无论是否列出，`AiProvider` 设置的提供商均被允许，并且始终提供`None` - 允许列表并不是阻止用户关闭助手的办法。|
| AiAllowedEndpointHosts | 列表 | 主机名 | 限制端点可以指向的主机，例如 `gateway.contoso.com` 或 `*.contoso.com`。|

锁定的设置在**工具 > 首选项 > AI 功能 > AI 助手**下显示为只读，无论用户之前选择了什么，AI 助手都会使用锁定的配置。用户的个人偏好设置中不会写入任何内容，因此如果删除该策略，其提供商、端点、模型和 API 密钥将恢复。API 密钥绝不会通过策略分发。

主机名仅与端点 URL 的主机部分进行匹配。匹配时忽略大小写，并忽略端口。开头的`*.`涵盖域的子域，但不涵盖域本身，因此如果两者都需要，请同时列出。每当设置端点时，该列表都适用于每个提供商，因此不能使用基准 URL 覆盖来绕过它。

政策不允许的配置将被拒绝，AI 助手会说明是哪条规则拒绝了该配置，而不是发送请求：不在允许列表中的提供商、不在主机允许列表中的端点主机、在适用主机允许列表时不是有效 URL 的端点，或者根本没有端点的已锁定 Azure OpenAI 或自定义提供商。

### 自定义指令

|值|类型|作用|
|--|--|--|
| AiCustomInstructionsPath | 路径 | 指定一个自定义指令文件夹的名称，除了产品随附的指令外，AI 助手还会为每个用户加载该文件夹中的指令。支持指向只读网络共享的 UNC 路径。如果组织指令和用户自己的指令具有相同的标识符，则以组织指令为准。|
| DisableUserCustomInstructions | 开/关 | AI 助手会忽略用户放置在自己文件夹中的自定义指令，并且用于打开该文件夹的按钮会被禁用。产品随附的指令以及任何组织文件夹仍会加载。|

### MCP 服务器

|值|类型|作用|
|--|--|--|
| McpDisabledTools | 列表 | 从不向已连接的客户端提供的 MCP 工具的名称。列出的工具不在客户端的工具列表中，即使客户端按名称请求某个工具，该工具也拒绝运行。AI 助手聊天不受影响。|
| McpPort | 数字，1024 至 49151 | 锁定 MCP 服务器侦听的端口，以便一个客户端配置可以在整个组织中共享。默认值为 42100。服务器仅在环回地址上侦听。|

### 审计日志

Tabular Editor 3 保留 AI 助手和 MCP 服务器活动的本地记录，包括工具调用、权限决策、配置和服务器会话。提示或回复的文本绝不会被记录。

记录是企业版功能。在企业版、咨询版和试用版许可证中，该记录会被写入，并且**打开审计文件夹**会显示在**工具 > 首选项 > AI 功能**以及**工具 > MCP 服务器……**对话框中。在 Desktop 和 Business 版本中，以及在激活许可证之前，不会写入任何内容，不会创建任何文件夹，也不会显示任何按钮。请参阅 @ai-audit-log。

|值|类型|作用|
|--|--|--|
| AiAuditLogPath | 路径 | 重定向审计日志，以便集中收集。支持指向网络共享的 UNC 路径。未设置策略时，日志将写入 `%LocalAppData%\TabularEditor3\AI\audit`，每天一个 `ai-audit-<date>.jsonl` 文件，记录的脚本位于 `audit\scripts\<date>` 下。|
| AiAuditLogRetentionDays | 数字，0 至 3650 | 保留多少天的审计日志；较旧的文件将被删除。`0`表示保留所有内容。默认为 30 天。|

## 没有企业版会发生什么

企业策略绝不会被悄然忽略。如果上述企业版表格中的任何值已设置（即使只有一个 Tabular Editor 无法解释），并且已安装的 Tabular Editor 3 副本未获得企业版许可证，则 AI 助手和 MCP 服务器将拒绝启动，AI 助手将报告您的组织已配置需要 Tabular Editor 3 企业版的 AI 策略，并指明相关值。Tabular Editor 3 中的其他所有功能仍可正常运行，上述常规策略仍将继续执行。

当无法解释某个值时，企业策略也会以“故障关闭”的方式处理。如果权限限制输入有误，则会拒绝资源，而不是被解读为“无限制”；如果提供商名称是 Tabular Editor 无法识别的，则会使 AI 助手不可用，而不是回退到用户自己的选择。

`BlockUnsafeScripts` 以同样的方式失效并关闭，值得确切了解其具体方式，因为它影响的范围超出了 AI 界面。在未获得企业版许可证的副本上，如果存在该值，则会阻止**所有**脚本和宏（无论是否安全）运行，并显示一条消息，指明所需的版本；宏将从菜单中移除，直到激活企业版许可证，然后它们将返回菜单，无需重启。如果读取器无法解释某个值，则会强制执行限制，而不是解除限制。显式的 `0` 不会强制执行此限制，但仍被视为已配置，因此它也会将 AI 界面置于 Enterprise 版的门槛之外。

若要在没有企业版许可证的情况下关闭所有 AI 功能，请使用通用 `DisableAi` 策略。

## 查看哪些策略处于生效状态

打开**工具 > 首选项 > Tabular Editor > 更新和反馈**。设置任何策略时，“**由您的组织管理**”部分会列出 Tabular Editor 找到的每个值、值本身以及其所属的注册表项和配置单元。Tabular Editor 无法解释的值会被标记为 *(无效)*，这是在看似不起作用的策略中找到拼写错误的最快方法。

在**“首选项”**的其他位置以及**“工具”>“MCP 服务器...”**对话框中，策略已锁定或限制的控件将以只读形式显示，并带有工具提示，说明该设置受贵组织策略的控制。

## 使用管理模板

Tabular Editor 3.27 及更高版本会安装一对组策略管理模板，因此上述策略可以从组策略编辑器中设置，而无需编辑注册表。您可以在安装文件夹的`Policies`文件夹中找到它们，默认情况下，该文件夹为`C:\Program Files\Tabular Editor 3\Policies`：

- `TabularEditorApS.admx`
- `en-US\TabularEditorApS.adml`

要在单台计算机上使用它们，请将这两个文件复制到 `%SystemRoot%\PolicyDefinitions`，并保留 `en-US` 文件夹结构：

```
C:\Windows\PolicyDefinitions\TabularEditorApS.admx
C:\Windows\PolicyDefinitions\en-US\TabularEditorApS.adml
```

要在整个域中使用它们，请将它们复制到域控制器上的中央存储，并保持相同的结构：

```
\\<your-domain>\SYSVOL\<your-domain>\Policies\PolicyDefinitions\TabularEditorApS.admx
\\<your-domain>\SYSVOL\<your-domain>\Policies\PolicyDefinitions\en-US\TabularEditorApS.adml
```

然后，打开本地组策略编辑器 (`gpedit.msc`) 或组策略管理编辑器，查看以下位置：

- **计算机配置 > 管理模板 > Tabular Editor**，用于查看全机策略
- **用户配置 > 管理模板 > Tabular Editor**，用于针对每个用户的策略

Tabular Editor 3 和 CLI 共享的策略直接位于**Tabular Editor**下方。仅 Tabular Editor 3 适用的策略位于**Tabular Editor > Tabular Editor 3** 下，AI 助手、MCP 服务器和 DAX 优化器集成位于各自的子文件夹中。

将策略设置为**已启用**会写入其注册表值。将其设置为**禁用**，或将其保留为**未配置**，则表示该策略未实施。模板不会写入旧的 `Kapacity\Tabular Editor` 键，因此，如果策略还需要应用于 Tabular Editor 2，请手动设置该键。

对于企业版策略，**Disabled** 会删除注册表值，而不是写入`0`。这是有意的：只要存在 Enterprise 值，就会将 AI 助手和 MCP 服务器置于 Enterprise 许可证检查之后，因此管理员刚刚禁用的策略绝不能留下任何值。

## 禁用网络通信

如果您想确保 Tabular Editor 不执行 Web 请求，请指定 `DisableUpdates`、`DisableBpaDownload`、`DisableWebDaxFormatter`、`DisableErrorReports`、`DisableTelemetry`、`DisableDaxOptimizer`、`DisableDaxPackageManager` 和 `DisableAi` 策略。

> [!NOTE]
> 即使指定了上述策略，Tabular Editor 3 仍会出于许可证验证的目的，不时向 `https://api.tabulareditor.com` 发出请求。如果 Tabular Editor 3 无法访问此端点（由于防火墙或代理服务器），用户将需要每 30 天[手动激活](xref:installation-activation-basic#manual-activation-no-internet)一次产品。

## 禁用自定义脚本

如果您想确保 Tabular Editor 不允许用户执行任意代码，请指定 `DisableCSharpScripts` 和 `DisableMacros` 策略。

如果您的组织希望保留脚本功能，但不想让任何脚本访问文件系统、网络或其他程序，请改用 `BlockUnsafeScripts`。脚本和宏将继续对模型执行操作，仅拒绝离开模型的那些部分。该策略需要企业版；上述两项策略适用于所有版本。

## 禁用 AI 功能

如果您想禁用所有 AI 功能，请指定 `DisableAi` 策略。这可以防止任何与 AI 相关的功能在启动时加载，并清除所有已存储的 API 密钥配置。此策略适用于所有版本，无需企业版许可证。

从 3.27.0 版本开始，安装程序也会从所有六个键读取该策略，并具有相同的优先级。新安装将不包含 AI 组件，升级将从已安装该组件的计算机中将其删除。现有安装会保留 AI 文件，直至下一次升级，并且在设置了该策略时，Tabular Editor 3 不会加载这些文件。将值设置为 `REG_DWORD` 的 `1`：安装程序将 `1` 视为*禁用*，将任何其他存在的值视为*未禁用*，其中应用程序接受任何非零数字。请参阅[使用 DisableAi 策略强制执行决策](xref:installation-activation-basic#enforcing-the-decision-with-the-disableai-policy)，了解如何同时部署功能选择和策略。

要使 AI 助手保持可用，但限制其可能执行的操作，请改用上述企业策略：将权限限制设置为您的组织可以接受的范围，将提供程序和终结点锁定到您运营的网关，并使用 `McpDisabledTools` 来阻止已连接的代理使用个别工具。
