---
uid: policies
title: 策略
author: Daniel Otykier
updated: 2026-09-22
applies_to:
  products:
    - product: Tabular Editor 2
      partial: true
      note: "Tabular Editor 2 只读取旧版注册表项，并且仅遵循下文标记为 TE2 的策略。"
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          partial: true
          note: "仅适用于通用策略"
        - edition: Business
          partial: true
          note: "仅适用于通用策略"
        - edition: Enterprise
          full: true
    - product: Tabular Editor CLI
      partial: true
      note: "仅适用于 Windows，且仅适用于下文标记为 CLI 的策略。"
---

# 策略

如果你在组织中负责管理 Tabular Editor，则可以通过组策略限制其功能，并代用户配置 AI Assistant 和 MCP 服务器。你可以手动在 Windows 注册表中设置这些值，也可以使用 Tabular Editor 3 随附的管理模板。

大多数策略都是通用策略，适用于 Tabular Editor 3 的所有版本。用于配置 AI Assistant 和 MCP 服务器的策略需要 [Tabular Editor 3 企业版](xref:editions)，并在下文中标记为 **企业版**。

> [!NOTE]
> 此功能需要以下版本的 Tabular Editor：
>
> - Tabular Editor [2.17.0](https://github.com/TabularEditor/TabularEditor/releases/tag/2.17.0) 或更高版本
> - Tabular Editor [3.3.5](https://github.com/TabularEditor/TabularEditor3/releases/tag/3.3.5) 或更高版本，适用于通用策略
> - Tabular Editor 3.27 或更高版本，适用于下方注册表项、计算机范围策略以及所有企业版策略
> - Tabular Editor CLI 0.7 或更高版本

## 注册表项

策略会从六个注册表项中读取；由第一个定义该值的项决定最终值。所有位于 `HKEY_LOCAL_MACHINE` 下的注册表项都高于 `HKEY_CURRENT_USER` 下的任何项，因此通过“计算机配置”设置的计算机范围策略不能被用户覆盖。在同一个注册表配置单元中，产品专用项高于共享项，而共享项又高于旧版项：

```
HKEY_LOCAL_MACHINE\Software\Policies\Tabular Editor ApS\TE3
HKEY_LOCAL_MACHINE\Software\Policies\Tabular Editor ApS
HKEY_LOCAL_MACHINE\Software\Policies\Kapacity\Tabular Editor
HKEY_CURRENT_USER\Software\Policies\Tabular Editor ApS\TE3
HKEY_CURRENT_USER\Software\Policies\Tabular Editor ApS
HKEY_CURRENT_USER\Software\Policies\Kapacity\Tabular Editor
```

- 仅 Tabular Editor 3 会读取 `Tabular Editor ApS\TE3`。 Tabular Editor CLI 则读取 `Tabular Editor ApS\TECLI` 作为对应项；其余四个注册表项对两者相同。
- `Tabular Editor ApS` 是共享项，Tabular Editor 3 和 CLI 都会读取它。
- `Kapacity\Tabular Editor` 是早期版本使用的注册表项。它仍会被读取，而且 Tabular Editor 2 只读取这一项。因此，如果策略也需要对 Tabular Editor 2 生效，也请在这里设置。

优先级对每个值分别适用：计算机范围的 `DisableTelemetry` 为 0 会覆盖按用户设置的 `DisableTelemetry` 为 1；而仅按用户设置的 `DisableCSharpScripts` 仍会生效。值名称不区分大小写。

## 值类型

| 设置类别     | 注册表类型          | 说明                                                            |
| -------- | -------------- | ------------------------------------------------------------- |
| 开/关策略    | `REG_DWORD`    | 任何非零值都会使该策略生效。 `0` 以及该值不存在都表示不强制执行。                           |
| 选项       | `REG_SZ`       | 选项的名称，例如 `Read`。也接受一个 `REG_DWORD`，其值为该选项在列表中的位置；这也是管理模板写入的形式。 |
| 列表       | `REG_MULTI_SZ` | 每行一个条目。也接受一个条目以分号分隔的 `REG_SZ`。                                |
| 路径、地址或名称 | `REG_SZ`       |                                                               |

Tabular Editor 仅在启动时读取一次策略值。更改会在你下次启动应用程序时生效。

## 常规策略

若要让其中一项生效，请添加一个名称与下方相同、值为非零的 `REG_DWORD` 值。**产品**列显示哪些产品会遵循该策略：**TE3** 指 Tabular Editor 3，**CLI** 指 Tabular Editor CLI，**TE2** 指 Tabular Editor 2，而它只读取旧版注册表项。

| 值                              | 产品          | 启用后……                                                                                                                  |
| ------------------------------ | ----------- | ---------------------------------------------------------------------------------------------------------------------- |
| DisableUpdates                 | TE3, TE2    | Tabular Editor 不会在线检查是否有新版本可用。用户也无法手动检查更新。                                                                             |
| DisableCSharpScripts           | TE3、TE2     | Tabular Editor 不允许用户创建或执行 C# Script。                                                                                   |
| DisableMacros                  | TE3、TE2     | Tabular Editor 不允许用户保存或运行宏。存储在 `%LocalAppData%` 文件夹中的宏在应用程序启动时不会加载。                                                    |
| DisableBpaDownload             | TE3、CLI、TE2 | 无法从网络下载 Best Practice Analyzer 规则。存储在本地或与模型一同存放的规则仍可继续使用。                                                              |
| DisableWebDaxFormatter         | TE3、CLI、TE2 | 会将代码发送到 daxformatter.com 的 DAX 格式化程序已被禁用。 Tabular Editor 3 仍提供内置格式化程序，不会通过网络发送任何内容。                    |
| DisableErrorReports            | TE3         | 用户无法向 Tabular Editor 支持团队发送错误或崩溃 Report。                                                                               |
| DisableTelemetry               | TE3、CLI     | 不会收集匿名使用数据，也不会将其发送给 Tabular Editor 支持团队。                                                                               |
| DisableDaxOptimizer            | TE3         | DAX优化器集成功能不可用。                                                                                                         |
| DisableDaxOptimizerUpload      | TE3         | 用户无法通过 DAX优化器的集成上传 VertiPaq分析器文件。在强制执行 `DisableDaxOptimizer` 时，此限制也会自动生效。                                              |
| RequireDaxOptimizerObfuscation | TE3         | 用户无法通过 DAX优化器的集成上传明文的 VertiPaq分析器文件；只能上传经过混淆的文件。在强制执行 `DisableDaxOptimizer` 或 `DisableDaxOptimizerUpload` 时，此限制也会自动生效。 |
| DisableDaxPackageManager       | TE3         | DAX 组件管理器不可用。                                                                                                          |
| DisableAi                      | TE3         | 所有 AI 功能均已关闭：AI 助手、MCP 服务器以及所有 AI 驱动的功能都不可用；应用启动时不会加载任何与 AI 相关的内容；并且会清除任何已存储的提供程序配置，包括 API 密钥。                         |
| DisableAiChat                  | TE3         | AI 助手聊天面板不可用。包括 MCP 服务器在内的其他 AI 功能不受影响。                                                                                |
| DisableMcpServer               | TE3         | MCP 服务器不可用，因此外部代理工具无法连接到 Tabular Editor 3。 AI 助手聊天不受影响。                                                                |
| RequireMcpAccessToken          | TE3         | 连接到 MCP 服务器的客户端必须提供 **工具 > MCP 服务器...** 对话框中显示的访问令牌，并且用户无法取消此要求。       |

### 在 TE CLI 中

在 Windows 上，Tabular Editor CLI 会遵循上文标记为 **CLI** 的策略，并按与 Tabular Editor 3 相同的顺序读取相同的键。对于 `te script`、`te macro run` 和 `te bpa run --fix`，它还会遵循下文[企业策略](#scripts-and-macros)中的 `BlockUnsafeScripts`。

操作被拒绝时不会悄无声息。 `te` 会指出拒绝该操作的策略，并以非零代码退出，因此管道步骤会失败，而不会看起来像是成功了却什么都没做。

CLI 不区分版本，因此，在桌面应用中要求 Tabular Editor 3 企业版的策略，CLI 都会直接应用，无论这台计算机持有什么许可证。

## 企业策略

这些策略决定 C# Script 可以执行哪些操作，并配置 AI 助手和 MCP 服务器。它们都要求使用 Tabular Editor 3 企业版，并应位于 `Tabular Editor ApS\TE3` 下；但 `BlockUnsafeScripts` 除外，Tabular Editor CLI 也会遵循该策略，因此它应放在共享的 `Tabular Editor ApS` 键中。如果只想作用于其中之一，请改为将其放在 `TE3` 或 `TECLI` 下。

### 脚本和宏

| 值                  | 类型  | 作用                                                                                      |
| ------------------ | --- | --------------------------------------------------------------------------------------- |
| BlockUnsafeScripts | 开/关 | 仅当 C# Script 和宏保持在语义模型范围内时才允许使用。凡是会读取或写入文件、访问网络、启动其他程序、引入外部代码，或直接向服务器发送命令的脚本，都会在运行前被拒绝。 |

无论脚本在哪里运行，此限制都适用：脚本文档中的 **Run script** 和 **Run with preview**，Best Practice Analyzer 中的 **Apply fix**，AI Assistant、MCP server，以及命令行中的 `te script`、`te macro run` 和 `te bpa run --fix`。被拒绝的脚本不等于运行失败的脚本。脚本不会对模型产生任何影响，错误列表仍保持为空，并会弹出 **Script not run** 对话框，说明触发的策略以及脚本使用了哪些受限项。

会访问模型外部的宏不会出现在任何菜单中，因此无法被误触运行。该宏仍会列在 **View > Macros** 下，且 **Blocked** 列会被填充；你仍可以打开并编辑它，从而将其调整回模型范围内，而无需从头重写。保存这类宏会成功，并提示它已保存，但无法运行。

是否算作在模型内运行，是通过分析脚本的编译结果来判定的，而不是通过搜索脚本文本；因此，借助反射、表达式树、`Activator`、`AppDomain`、XML 读取器或反序列化等间接方式访问相同目标的行为也会被拒绝。在内置的 [辅助方法](xref:script-helper-methods) 中，`SaveFile`、`ExecuteCommand` 和 `Bpa.ExportCsv` 这三个会向模型外写入内容的方法被视为不安全；只进行读取的则不算，包括 `ReadFile`、`ExecuteDax`、`EvaluateDax`、`ExecuteReader` 和 `ExportProperties`。脚本作者侧的同一规则，请参阅[管理员策略](xref:csharp-scripts#administrator-policies)。

在组策略编辑器中，此项名为 **仅允许停留在模型内的脚本和宏**；由于它写入共享注册表项，因此它直接位于 **管理模板 > Tabular Editor** 下，而不在 **Tabular Editor 3** 子文件夹中。

### 权限上限

以下每一项都为 AI 助手和 MCP 服务器可访问的某一类资源设定上限。可接受的值为 `Deny`、`Read` 和 `Write`，但模型数据除外，因为对模型数据来说，`Read` 已是最高且有意义的设置。

用户可授予的权限以上限为准：任何高于上限的现有权限都会被降到该上限；**工具 > 偏好 > AI 功能 > 权限** 下对应的选项以及 **工具 > MCP 服务器...** 对话框中的对应项都会显示为只读；AI 助手也不再请求无法授予的权限。任何已授予的权限都不能突破上限——无论是长期权限、针对单个模型授予的权限，还是在早期版本中授予的权限。用户在其偏好中的自选设置不会被改动，因此如果策略被移除，该设置会恢复生效。

| 值                         | 可接受的值    | 限制对以下资源的访问……                                                                                                                                                                   |
| ------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| MaxModelMetadataAccess    | 拒绝、读取、写入 | 当前打开的模型的元数据：表、列和度量值的名称、表达式、说明、Best Practice Analyzer 的结果以及 VertiPaq 统计信息。 `Write` 还允许助手针对该模型运行其自有的 C# Script。在 `Deny` 模式下，完全不会发送任何关于当前打开模型的信息——不会发送模型摘要、不会提示模型已更改，也不会发送当前所选内容。 |
| MaxModelDataAccess        | 拒绝、读取    | 模型中的数据值，也就是 DAX 查询的结果。                                                                                                                                                         |
| MaxBpaAccess              | 拒绝、读取、写入 | Best Practice Analyzer 规则。 `Read` 允许列出规则并运行分析；`Write` 还允许添加和更改规则。                                                                                                              |
| MaxDocumentsAccess        | 拒绝、读取、写入 | 用户当前打开的文档，例如 C# Script 和 DAX 查询。 `Read` 允许读取这些文档的内容；`Write` 还允许修改它们。                                                                                                           |
| MaxMacrosAccess           | 拒绝、读取、写入 | 用户的宏库。                                                                                                                                                                         |
| McpMaxModelMetadataAccess | 拒绝、读取、写入 | 同样的五类资源，但仅适用于 MCP 服务器。                                                                                                                                                         |
| McpMaxModelDataAccess     | 拒绝、读取    |                                                                                                                                                                                |
| McpMaxBpaAccess           | 拒绝、读取、写入 |                                                                                                                                                                                |
| McpMaxDocumentsAccess     | 拒绝、读取、写入 |                                                                                                                                                                                |
| McpMaxMacrosAccess 宏      | 拒绝、读取、写入 |                                                                                                                                                                                |

这五个 `McpMax...` 值仅适用于 MCP 服务器。如果其中某个值未设置，MCP 服务器将继承对应的 `Max...` 限制。这些值只能降低该上限，不能提高，因此无人值守代理获得的权限绝不会超过交互式助手。

### AI 服务提供商

| 值                      | 类型 | 可接受的值                                        | 作用                                                                               |
| ---------------------- | -- | -------------------------------------------- | -------------------------------------------------------------------------------- |
| AiProvider             | 选项 | None, OpenAI, Anthropic, AzureOpenAI, Custom | 将 AI 助手锁定为仅使用一个提供商。 `None` 会关闭 AI 助手；MCP 服务器不受影响。                                |
| AiEndpoint             | 地址 |                                              | 锁定请求发送到的端点或基础 URL，例如内部 Gateway 或 Azure OpenAI 资源。                                |
| AiModel                | 姓名 |                                              | 锁定模型；对于 Azure OpenAI，则锁定部署名称。聊天面板中的模型选择器会被替换为一个简单的指示器，因此用户无法切换模型。                |
| AiOrganizationId       | 姓名 |                                              | 锁定请求计费所属的 OpenAI 组织。                                                             |
| AiProjectId            | 姓名 |                                              | 锁定用于对请求计费的 OpenAI 项目。                                                            |
| AiAllowedProviders     | 列表 | 上述任一提供程序名称                                   | 限制用户可配置的提供程序。由 `AiProvider` 设置的提供程序无论是否列入此列表都允许使用，且始终提供 `None`——允许列表并不能阻止用户关闭助手。 |
| AiAllowedEndpointHosts | 列表 | 主机名                                          | 限制端点可指向的主机，例如 `gateway.contoso.com` 或 `*.contoso.com`。                           |

被锁定的设置会在 **工具 > 偏好 > AI 功能 > AI 助手** 下显示为只读，并且无论用户之前选择了什么，AI 助手都会使用锁定的配置。不会向用户自己的偏好写入任何内容，因此如果移除此策略，他们原先的提供程序、端点、模型和 API 密钥都会恢复。策略绝不会分发 API 密钥。

主机名仅与端点 URL 的主机部分进行匹配。匹配时会忽略大小写，也会忽略端口。前导 `*.` 可匹配某个域的所有子域，但不包括该域本身，因此如果两者都需要，请同时列出。只要设置了端点，此列表就会应用于所有提供程序，因此不能通过覆盖基础 URL 来绕过。

策略不允许的配置会被拒绝。AI 助手不会发送请求，而是会说明是哪条规则拒绝了该配置：提供程序不在允许列表中、端点主机不在主机允许列表中、在主机允许列表生效时端点不是有效 URL，或者被锁定的 Azure OpenAI 或 Custom 提供程序根本未设置端点。

### 自定义指令

| 值                             | 类型  | 作用                                                                                                      |
| ----------------------------- | --- | ------------------------------------------------------------------------------------------------------- |
| AiCustomInstructionsPath      | 路径  | 指定一个“自定义说明”文件夹。AI 助手会在加载产品随附的说明之外，还会为每位用户加载该文件夹中的内容。支持指向只读网络共享的 UNC 路径。如果组织说明与用户自己的说明使用相同的标识符，则以组织说明为准。 |
| DisableUserCustomInstructions | 开/关 | AI Assistant 会忽略用户放在其个人文件夹中的自定义指令，同时用于打开该文件夹的按钮会被禁用。随产品提供的指令以及任何组织文件夹中的指令仍会加载。                          |

### MCP 服务器

| 值                | 类型                | 作用                                                                                           |
| ---------------- | ----------------- | -------------------------------------------------------------------------------------------- |
| McpDisabledTools | 列表                | 永远不会提供给已连接客户端的 MCP 工具名称列表。列出的工具不会出现在客户端的工具列表中；即使客户端按名称请求某个工具，这些工具也不会运行。 AI Assistant 聊天不受影响。 |
| McpPort          | 数值范围：1024 到 49151 | 固定 MCP 服务器监听的端口，这样同一份客户端配置就可以在整个组织中共享。默认值为 42100。服务器始终只监听环回地址。                               |

### 审计日志

Tabular Editor 3 会在本地记录 AI Assistant 和 MCP 服务器的活动——包括工具调用、权限决策、配置以及服务器会话。提示词或响应的文本内容绝不会被记录。

该记录功能仅企业版提供。在企业版、Consultancy 和试用许可证下，会写入审计日志，并且 **打开审计日志文件夹** 会显示在 **工具 > 偏好 > AI 功能** 中，以及 **工具 > MCP 服务器...** 对话框内。在 Desktop 和 Business 版本中，以及许可证激活前，不会写入任何内容，也不会创建文件夹，两个按钮都不会显示。见 @ai-audit-log。

| 值                       | 类型             | 功能                                                                                                                                                                     |
| ----------------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AiAuditLogPath          | 路径             | 将审计日志重定向到其他位置，以便集中收集。支持指向网络共享的 UNC 路径。如果未设置该策略，日志将写入 `%LocalAppData%\TabularEditor3\AI\audit`；每天生成一个 `ai-audit-<date>.jsonl` 文件，记录的脚本位于 `audit\scripts\<date>` 下。 |
| AiAuditLogRetentionDays | 数字，范围 0 到 3650 | 指定审计日志保留的天数；较旧的文件会被删除。 `0` 表示全部保留。默认值为 30 天。                                                                                                                           |

## 未使用企业版时会怎样

企业策略绝不会被悄悄忽略。只要在上面的企业版表格中设置了任何值——即使只有一个值是 Tabular Editor 无法解析的——并且已安装的 Tabular Editor 3 未获得企业版许可，AI 助手和 MCP 服务器都会拒绝启动；AI 助手还会生成 Report，说明你的组织已配置需要 Tabular Editor 3 企业版的 AI 策略，并点明涉及的值。 Tabular Editor 3 中的其他所有功能仍可继续使用，上述常规策略也会继续生效。

当某个值无法解释时，企业策略也会采用“默认拒绝”的处理方式。如果权限限制拼写错误，会直接拒绝访问该资源，而不是被当作“无限制”；如果提供程序名称不被 Tabular Editor 识别，AI 助手将不可用，而不是回退到用户自己的选择。

`BlockUnsafeScripts` 也会以同样的方式“默认拒绝”，而且有必要准确了解它的具体行为，因为它影响的范围不止 AI 相关功能。在未获得企业版许可的副本中，只要存在该值，就会阻止 **所有** 脚本和宏运行，不论是否安全，并显示一条消息说明所需版本；宏也会从菜单中消失，直到激活企业版许可证后才会恢复，而且无需重启即可恢复。如果读取方无法解析某个值，就会继续施加限制，而不是解除限制。显式设置为 `0` 不会强制执行该限制，但仍会被视为已配置，因此也会让 AI 相关界面只能在企业版中使用。

要在没有企业版许可证的情况下关闭所有 AI 功能，就用通用 `DisableAi` 策略。

## 查看当前生效的策略

打开 **工具 > 偏好 > Tabular Editor > 更新和反馈**。只要设置了任意策略，**由你的组织管理** 部分就会列出 Tabular Editor 找到的每个值、该值本身，以及它来自哪个注册表项和哪个注册表配置单元。 Tabular Editor 无法解析的值会被标记为 _(invalid)_，这是在看似没有生效的策略中快速定位拼写错误的最快方法。

在 **偏好** 中的其他位置以及 **工具 > MCP Server...** 对话框中，凡是被策略在别处锁定或限制的控件都会以只读方式显示，并带有工具提示，说明该设置由你所在组织的策略控制。

## 使用管理模板

Tabular Editor 3.27 及更高版本会安装一对组策略管理模板，因此上述策略可以在组策略编辑器中设置，而不必直接编辑注册表。你可以在安装目录下的 `Policies` 文件夹中找到它们，默认路径为 `C:\\Program Files\\Tabular Editor 3\\Policies`：

- `TabularEditorApS.admx`
- `en-US\\TabularEditorApS.adml`

要在单台计算机上使用它们，请将这两个文件复制到 `%SystemRoot%\\PolicyDefinitions`，并保留 `en-US` 文件夹结构：

```
C:\Windows\PolicyDefinitions\TabularEditorApS.admx
C:\Windows\PolicyDefinitions\en-US\TabularEditorApS.adml
```

要在整个域中使用它们，请改为将它们复制到域控制器上的中央存储，并保持相同的目录结构：

```
\\<your-domain>\SYSVOL\<your-domain>\Policies\PolicyDefinitions\TabularEditorApS.admx
\\<your-domain>\SYSVOL\<your-domain>\Policies\PolicyDefinitions\en-US\TabularEditorApS.adml
```

然后打开本地组策略编辑器 (`gpedit.msc`) 或组策略管理编辑器，并查看以下位置：

- **计算机配置 > 管理模板 > Tabular Editor**：适用于整台计算机的策略
- **用户配置 > 管理模板 > Tabular Editor**：适用于单个用户的策略

Tabular Editor 3 与 CLI 共用的策略直接位于 **Tabular Editor** 下。仅 Tabular Editor 3 会遵循的策略位于 **Tabular Editor > Tabular Editor 3** 下，其中 AI 助手、MCP 服务器和 DAX优化器集成各自位于独立的子文件夹中。

将策略设置为 **已启用** 会写入其注册表值。将其设置为 **已禁用**，或保留为 **未配置**，都表示不会强制实施该策略。这些模板不会写入旧版 `Kapacity\\Tabular Editor` 注册表项，因此如果某项策略还需要作用于 Tabular Editor 2，请手动设置该项。

对于企业版策略，**已禁用** 会删除该注册表值，而不是写入 `0`。这是刻意为之：只要该企业版注册表值存在，AI 助手和 MCP 服务器就会被纳入企业版许可证检查范围，因此管理员刚关闭某项策略后，不能让该值继续保留下来。

## 禁用 Web 通信

如果希望确保 Tabular Editor 不会发起任何 Web 请求，请设置 `DisableUpdates`、`DisableBpaDownload`、`DisableWebDaxFormatter`、`DisableErrorReports`、`DisableTelemetry`、`DisableDaxOptimizer`、`DisableDaxPackageManager` 和 `DisableAi` 策略。

> [!NOTE]
> 即使已指定上述策略，Tabular Editor 3 仍会偶尔向 `https://api.tabulareditor.com` 发起请求，用于许可证验证。如果 Tabular Editor 3 无法访问此端点（由于防火墙或代理），用户将不得不每 30 天对产品进行一次[手动激活](xref:installation-activation-basic#manual-activation-no-internet)。

## 禁用自定义脚本

如果你想确保 Tabular Editor 不允许用户执行任意代码，请指定 `DisableCSharpScripts` 和 `DisableMacros` 策略。

如果你的组织希望保留脚本功能，但又不想让任何脚本访问文件系统、网络或其他程序，请改用 `BlockUnsafeScripts`。脚本和宏仍可针对模型运行，只有会离开模型、访问外部资源的部分会被拒绝。该策略需要企业版；上面两项策略适用于所有版本。

## 禁用 AI 功能

如果希望禁用所有 AI 功能，请设置 `DisableAi` 策略。这会阻止任何与 AI 相关的内容在启动时加载，并清除任何已存储的 API 密钥配置。它适用于所有版本，无需 Enterprise 许可证。

从 3.27.0 起，安装程序也会从全部六个键值中按相同的优先级读取该策略，并将 AI 组件完全排除在外，因此在策略禁用了 AI 的计算机上，AI 程序集绝不会写入安装文件夹。将该值设为 `REG_DWORD` 类型并赋值为 `1`：安装程序将 `1` 视&#x4E3A;_&#x7981;用_，将任何其他已存在的值视&#x4E3A;_&#x672A;禁用_；而应用程序则接受任何非零值。有关同时部署功能选择和策略的信息，请参阅 [不使用 AI 功能进行部署](xref:installation-activation-basic#deploying-without-the-ai-features)。

如果希望保留 AI 助手可用，但限制其可执行的操作，请改用上述 Enterprise 策略：将权限上限设置为贵组织可接受的范围，将提供程序和端点锁定到由你方运营的 Gateway，并使用 `McpDisabledTools` 从已连接的代理中屏蔽特定工具。
