---
uid: 策略
title: 策略
author: Daniel Otykier
updated: 2026-09-22
applies_to:
  products:
    - product: Tabular Editor 2
      partial: true
      note: "Tabular Editor 2 只读取旧版注册表项，并且仅应用下文标记为 TE2 的策略。"
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          partial: true
          note: "仅限常规策略"
        - edition: Business
          partial: true
          note: "仅限常规策略"
        - edition: Enterprise
          full: true
    - product: Tabular Editor CLI
      partial: true
      note: "仅适用于 Windows，且仅适用于下文标注为 CLI 的策略。"
---

# 策略

如果您为组织管理 Tabular Editor，可以通过组策略限制其功能，并代表用户配置 AI 助手和 MCP 服务器。你可以手动在 Windows 注册表中设置这些值，也可以使用 Tabular Editor 3 随附的管理模板。

大多数策略都是常规策略，在 Tabular Editor 3 的每个版本中都可用。用于配置 AI 助手和 MCP 服务器的策略需要 [Tabular Editor 3 企业版](xref:editions)，并在下文标注为 **Enterprise**。

> [!NOTE]
> 此功能需要以下版本的 Tabular Editor：
>
> - Tabular Editor [2.17.0](https://github.com/TabularEditor/TabularEditor/releases/tag/2.17.0) 或更高版本
> - 如需使用常规策略，需要 Tabular Editor [3.3.5](https://github.com/TabularEditor/TabularEditor3/releases/tag/3.3.5) 或更高版本
> - 如需使用下方的注册表项、计算机范围的策略以及所有 Enterprise 策略，需要 Tabular Editor 3.27 或更高版本
> - Tabular Editor CLI 0.7 或更高版本

## 注册表项

系统会从六个注册表项中读取策略，哪个注册表项最先定义某个值，就以哪个值为准。 `HKEY_LOCAL_MACHINE` 下的任何注册表项优先级都高于 `HKEY_CURRENT_USER` 下的任何注册表项，因此通过“计算机配置”设置的计算机范围策略不能由用户覆盖。在同一配置单元内，产品专用注册表项的优先级高于共享注册表项，而共享注册表项又高于旧版注册表项：

```
HKEY_LOCAL_MACHINE\Software\Policies\Tabular Editor ApS\TE3
HKEY_LOCAL_MACHINE\Software\Policies\Tabular Editor ApS
HKEY_LOCAL_MACHINE\Software\Policies\Kapacity\Tabular Editor
HKEY_CURRENT_USER\Software\Policies\Tabular Editor ApS\TE3
HKEY_CURRENT_USER\Software\Policies\Tabular Editor ApS
HKEY_CURRENT_USER\Software\Policies\Kapacity\Tabular Editor
```

- `Tabular Editor ApS\TE3` 仅由 Tabular Editor 3 读取。 Tabular Editor CLI 则改为读取 `Tabular Editor ApS\TECLI`；其余四个注册表项两者相同。
- `Tabular Editor ApS` 是共享注册表项，由 Tabular Editor 3 和 CLI 共同读取。
- `Kapacity\Tabular Editor` 是早期版本使用的注册表项。该键仍会被读取，而且这是 Tabular Editor 2 唯一会读取的键。因此，如果策略也需要对 Tabular Editor 2 生效，也要在此处设置。

优先级会分别应用到每个值：计算机范围的 `DisableTelemetry` 设为 0 时，会覆盖按用户设置为 1 的 `DisableTelemetry`；而只按用户设置的 `DisableCSharpScripts` 仍然生效。值名称不区分大小写。

## 值类型

| 设置类型     | 注册表类型          | 说明                                                               |
| -------- | -------------- | ---------------------------------------------------------------- |
| 开/关策略    | `REG_DWORD`    | 任何非零值都会强制执行该策略。 `0` 以及该值不存在，都表示不强制实施该策略。                         |
| 选项       | `REG_SZ`       | 选项的名称，例如 `Read`。也接受一个 `REG_DWORD` 值，用于保存该选项在列表中的位置；这也是管理模板写入的形式。 |
| 列表       | `REG_MULTI_SZ` | 每行一个条目。也接受使用分号分隔各条目的 `REG_SZ`。                                   |
| 路径、地址或名称 | `REG_SZ`       |                                                                  |

Tabular Editor 只会在启动时读取一次策略值。更改会在下次启动应用程序时生效。

## 常规策略

要强制执行其中一项，只需添加一个名为下述名称且数值为非零的 `REG_DWORD` 值。 **Products** 列显示哪些产品会遵循该策略：**TE3** 表示 Tabular Editor 3，**CLI** 表示 Tabular Editor CLI，**TE2** 表示 Tabular Editor 2，且它仅会读取旧版键。

| 值                              | 产品            | 启用后……                                                                                                             |
| ------------------------------ | ------------- | ----------------------------------------------------------------------------------------------------------------- |
| DisableUpdates                 | TE3, TE2      | Tabular Editor 不会在线检查是否有新版本可用。用户也无法手动检查更新。                                                                        |
| DisableCSharpScripts           | TE3, TE2      | Tabular Editor 不允许用户创建或执行 C# Script。                                                                              |
| DisableMacros                  | TE3, TE2      | Tabular Editor 不允许用户保存或运行宏。应用启动时不会加载存储在 `%LocalAppData%` 文件夹中的宏。                                                  |
| DisableBpaDownload             | TE3, CLI, TE2 | 无法从网络下载 Best Practice Analyzer 规则。保存在本地或随模型一起存放的规则仍可正常使用。                                                         |
| DisableWebDaxFormatter         | TE3, CLI, TE2 | 会将代码发送到 daxformatter.com 的 DAX 格式化程序已被禁用。 Tabular Editor 3 仍提供其内置格式化程序，不会通过网络发送任何数据。              |
| DisableErrorReports            | TE3           | 用户无法向 Tabular Editor 支持团队发送错误或崩溃 Report。                                                                          |
| DisableTelemetry               | TE3, CLI      | 不会收集匿名使用数据，也不会将其发送给 Tabular Editor 支持团队。                                                                          |
| DisableDaxOptimizer            | TE3           | DAX优化器集成功能不可用。                                                                                                    |
| DisableDaxOptimizerUpload      | TE3           | 用户无法通过DAX优化器集成上传VertiPaq分析器文件。强制执行 `DisableDaxOptimizer` 时，此项也会自动生效。                                              |
| RequireDaxOptimizerObfuscation | TE3           | 用户无法通过DAX优化器集成上传明文VertiPaq分析器文件；只能上传已混淆的文件。强制执行 `DisableDaxOptimizer` 或 `DisableDaxOptimizerUpload` 时，此项也会自动生效。   |
| DisableDax组件管理器                | TE3           | DAX 组件管理器不可用。                                                                                                     |
| DisableAi                      | TE3           | 所有 AI 功能都会关闭：AI 助手、MCP 服务器以及所有由 AI 提供支持的功能都将不可用；应用启动时不会加载任何与 AI 相关的内容；并会清除任何已存储的提供程序配置（包括 API 密钥）。                |
| DisableAiChat                  | TE3           | AI 助手聊天面板不可用。其他 AI 功能（包括 MCP 服务器）不受影响。                                                                            |
| DisableMcpServer               | TE3           | MCP 服务器不可用，因此外部代理工具无法连接到 Tabular Editor 3。 AI 助手聊天不受影响。                                                           |
| RequireMcpAccessToken          | TE3           | 连接到 MCP 服务器的客户端必须提供 **工具 > MCP 服务器...** 对话框中显示的访问令牌，而且用户无法关闭这一要求。 |

### 在 TE CLI 中

在 Windows 上，Tabular Editor CLI 会遵循上文标记为 **CLI** 的策略，并按与 Tabular Editor 3 相同的顺序读取相同的键。它也会遵循下方[企业策略](#scripts-and-macros)中的 `BlockUnsafeScripts`，适用于 `te script`、`te macro run` 和 `te bpa run --fix`。

被拒绝的操作不会悄无声息。 `te` 会指出拒绝该操作的策略，并以非零代码退出，因此流水线步骤会失败，而不是看起来成功却什么也没做。

CLI 没有版本之分，因此，在桌面应用中要求使用 Tabular Editor 3 企业版的策略，CLI 都会直接应用，无论该计算机持有什么许可证。

## 企业策略

这些策略决定 C# Script 可以执行哪些操作，并配置 AI Assistant 和 MCP 服务器。它们都要求使用 Tabular Editor 3 企业版，并且应位于 `Tabular Editor ApS\TE3` 下；但 `BlockUnsafeScripts` 例外，Tabular Editor CLI 也会遵循它，因此它应放在共享的 `Tabular Editor ApS` 键中。如果只想让两者中的一个生效，请改为将其放在 `TE3` 或 `TECLI` 下。

### 脚本和宏

| 值                  | 类型  | 作用                                                                                         |
| ------------------ | --- | ------------------------------------------------------------------------------------------ |
| BlockUnsafeScripts | 开/关 | 仅当 C# Script 和宏的操作限定在语义模型范围内时，才允许使用。凡是读取或写入文件、访问网络、启动其他程序、引入外部代码，或直接向服务器发送命令的脚本，都会在执行前被拒绝。 |

无论脚本在哪里运行，此限制都适用：脚本文档中的 **运行脚本** 和 **运行并预览**，Best Practice Analyzer 中的 **应用修复**，AI Assistant、MCP 服务器，以及命令行中的 `te script`、用于宏的 `te macro run` 和 `te bpa run --fix`。被拒绝的脚本不算脚本执行失败。模型不会受到任何影响，错误列表仍为空，并且 **脚本未运行** 对话框会显示对应的策略以及脚本使用了哪些功能。

超出模型范围的宏不会出现在任何菜单中，因此无法被误运行。它仍会列在 **视图 > 宏** 中，并且其 **Blocked** 列会被填充；你仍然可以打开并编辑它，这样就能把它改回允许范围内，而不必从头重写。这类宏可以保存，界面也会提示已保存，但实际上无法运行。

是否算作“保持在模型范围内”，是通过分析已编译的脚本来判断的，而不是通过搜索脚本文本。因此，任何通过间接方式到达同一位置的途径——反射、表达式树、`Activator`、`AppDomain`、XML 读取器或反序列化——同样会被拒绝。在内置的[辅助方法](xref:script-helper-methods)中，`SaveFile`、`ExecuteCommand` 和 `Bpa.ExportCsv` 这三个会向模型外部写入，因此被视为不安全；仅执行读取的方法则不算，包括 `ReadFile`、`ExecuteDax`、`EvaluateDax`、`ExecuteReader` 和 `ExportProperties`。如需从脚本作者的角度了解同一规则，请参阅[管理员策略](xref:csharp-scripts#administrator-policies)。

在组策略编辑器中，此项名为 **仅允许保持在模型范围内的脚本和宏**。由于它写入共享注册表项，因此它直接位于 **管理模板 > Tabular Editor** 下，而不是 **Tabular Editor 3** 子文件夹中。

### 权限上限

其中每一项都会为 AI Assistant 和 MCP 服务器可访问的某一类资源设定上限。可接受的值为 `Deny`、`Read` 和 `Write`，但模型数据除外，因为对模型数据来说，`Read` 已是最高且有意义的设置。

上限会限制用户可授予的权限：任何高于上限的现有权限都会被下调到该上限；**工具 > 偏好 > AI 功能 > 权限** 下对应的选项以及 **工具 > MCP Server...** 对话框中的对应选项都会显示为只读；AI Assistant 也不会再请求无法授予的权限。任何授权都不能高于上限——无论是常设权限、针对单个模型授予的权限，还是在早期版本中授予的权限。用户自己在偏好中的选择不会被改动，因此如果移除此策略，该选择会恢复生效。

| 值                         | 可接受的值             | 限制对以下内容的访问……                                                                                                                                                       |
| ------------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| MaxModelMetadataAccess    | Deny, Read, Write | 当前打开模型的元数据：表、列和度量值名称、表达式、说明、Best Practice Analyzer 结果以及 VertiPaq 统计信息。 `Write` 还允许助手对模型运行其自身的 C# Script。当设为 `Deny` 时，与当前打开模型有关的任何内容都不会发送——没有模型摘要、没有模型更改通知，也没有当前选择。 |
| MaxModelDataAccess        | Deny, Read        | 模型中的数据值，也就是 DAX 查询的结果。                                                                                                                                             |
| MaxBpaAccess              | Deny, Read, Write | Best Practice Analyzer 规则。 `Read` 允许列出规则并运行分析；`Write` 还允许添加和修改规则。                                                                                                  |
| MaxDocumentsAccess        | Deny, Read, Write | 用户当前打开的文档，例如 C# Script 脚本和 DAX 查询。 `Read` 允许读取其内容；`Write` 还允许对其进行修改。                                                                                               |
| 最大宏访问权限                   | Deny, Read, Write | 用户的宏库。                                                                                                                                                             |
| McpMaxModelMetadataAccess | Deny, Read, Write | 同样的五类资源，但仅适用于 MCP 服务器。                                                                                                                                             |
| McpMaxModelDataAccess     | Deny, Read        |                                                                                                                                                                    |
| McpMaxBpaAccess           | Deny, Read, Write |                                                                                                                                                                    |
| McpMaxDocumentsAccess     | Deny, Read, Write |                                                                                                                                                                    |
| Mcp 最大宏访问权限               | Deny, Read, Write |                                                                                                                                                                    |

这五个 `McpMax...` 值仅适用于 MCP 服务器。当其中某个值未设置时，MCP 服务器会继承对应的 `Max...` 限制。它们只能降低该限制，不能提高，因此无人值守代理的权限绝不会超过交互式助手。

### AI 提供商

| 值                      | 类型 | 可接受的值                                        | 用途                                                                            |
| ---------------------- | -- | -------------------------------------------- | ----------------------------------------------------------------------------- |
| AiProvider             | 选项 | None, OpenAI, Anthropic, AzureOpenAI, Custom | 将 AI 助手锁定为仅使用一个提供商。 `None` 会关闭 AI 助手；MCP 服务器不受影响。                             |
| AiEndpoint             | 地址 |                                              | 锁定请求发送到的端点或基础 URL，例如内部 Gateway 或 Azure OpenAI 资源。                             |
| AiModel                | 姓名 |                                              | 锁定模型或 Azure OpenAI 部署名称。聊天面板中的模型选择器会被替换为一个仅作显示的指示器，因此用户无法切换模型。                |
| AiOrganizationId       | 姓名 |                                              | 锁定 OpenAI 请求的计费组织。                                                            |
| AiProjectId            | 姓名 |                                              | 锁定 OpenAI 请求的计费项目。                                                            |
| AiAllowedProviders     | 列表 | 上述任一提供商名称                                    | 限制用户可配置的提供商。即使未在列表中，`AiProvider` 设置的提供商也始终允许使用，且始终提供 `None`——允许列表并不能阻止用户关闭助手。 |
| AiAllowedEndpointHosts | 列表 | 主机名                                          | 限制端点可指向的主机，例如 `gateway.contoso.com` 或 `*.contoso.com`。                        |

锁定的设置会在 **工具 > 偏好 > AI 功能 > AI 助手** 下显示为只读；无论用户之前如何选择，AI 助手都会使用锁定的配置。不会向用户自己的偏好中写入任何内容，因此如果移除该策略，提供程序、终结点、模型和 API 密钥将恢复为用户原先设置的值。策略绝不会分发 API 密钥。

主机名仅与终结点 URL 的主机部分匹配。匹配时不区分大小写，也会忽略端口。前导 `*.` 可匹配某个域的子域，但不包括该域本身，因此如果两者都需要，请同时列出。只要设置了终结点，此列表就会对所有提供程序生效，因此无法通过 base URL 覆盖来绕过它。

策略不允许的配置会被拒绝。AI 助手不会发送请求，而是说明是哪条规则拒绝了该配置：提供程序不在允许列表中、终结点主机不在主机允许列表中、在主机允许列表生效时终结点不是有效 URL，或者已锁定的 Azure OpenAI 或 Custom 提供程序完全没有终结点。

### 自定义指令

| 值                             | 类型  | 作用                                                                                                   |
| ----------------------------- | --- | ---------------------------------------------------------------------------------------------------- |
| AiCustomInstructionsPath      | 路径  | 指定一个“自定义说明”文件夹；除了产品随附的说明外，AI 助手还会为每个用户加载该文件夹中的内容。支持指向只读网络共享的 UNC 路径。如果组织说明与用户自己的说明使用相同的标识符，则以组织说明为准。 |
| DisableUserCustomInstructions | 开/关 | AI 助手会忽略用户放在自己文件夹中的“自定义说明”，用于打开该文件夹的按钮也将被禁用。产品随附的说明以及任何组织文件夹中的说明仍会加载。                                |

### MCP 服务器

| 值                | 类型              | 作用                                                                                    |
| ---------------- | --------------- | ------------------------------------------------------------------------------------- |
| McpDisabledTools | 列表              | 指定永远不会提供给已连接客户端的 MCP 工具名称。列出的工具不会出现在客户端的工具列表中，即使客户端按名称请求其中某个工具，也会拒绝执行。 AI 助手聊天功能不受影响。 |
| McpPort          | 数值范围：1024–49151 | 固定 MCP 服务器侦听的端口，这样整个组织就可以共享同一份客户端配置。默认值为 42100。服务器始终只侦听回环地址。                          |

### 审计日志

Tabular Editor 3 会在本地保留 AI 助手和 MCP 服务器活动记录——包括工具调用、权限决策、配置以及服务器会话。不会记录提示或响应的文本内容。

此记录功能仅在企业版中提供。在企业版、咨询版和试用版许可证下，会写入该记录；并且在 **工具 > 偏好 > AI 功能** 和 **工具 > MCP 服务器...** 对话框中会显示 **打开审计文件夹**。在 Desktop 版和 Business 版中，以及在许可证激活之前，不会写入任何内容，也不会创建文件夹，并且两个位置都不会显示该按钮。参见 @ai-audit-log。

| 值                       | 类型          | 作用                                                                                                                                                               |
| ----------------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AiAuditLogPath          | 路径          | 重定向审计日志，以便集中收集。支持指向网络共享的 UNC 路径。未设置该策略时，日志会写入 `%LocalAppData%\TabularEditor3\AI\audit`，每天生成一个 `ai-audit-<date>.jsonl` 文件；记录的脚本存放在 `audit\scripts\<date>` 下。 |
| AiAuditLogRetentionDays | 数值范围：0–3650 | 保留审计日志的天数；更旧的文件会被删除。 `0` 表示全部保留。默认值为 30 天。                                                                                                                       |

## 没有企业版时会发生什么

企业策略绝不会被悄悄忽略。如果上面的企业版表格中设置了任何值——哪怕只设置了一个 Tabular Editor 无法解析的值——而已安装的 Tabular Editor 3 又未获得企业版许可，AI Assistant 和 MCP 服务器都会拒绝启动；AI Assistant 还会提示你的组织已配置需要 Tabular Editor 3 企业版的 AI 策略，并点名列出相关值。 Tabular Editor 3 中的其他所有功能仍可正常运行，上述通用策略也会继续生效。

当某个值无法被解释时，企业策略也会采用“默认拒绝”，即 fail closed 的方式。如果权限限制值写错了，会拒绝访问该资源，而不会被当作“无限制”；如果提供程序名称不被 Tabular Editor 识别，AI Assistant 就会不可用，而不会回退到用户自己的选择。

`BlockUnsafeScripts` 也会以同样的默认拒绝方式处理，而且有必要确切了解它的行为，因为它影响的不只是 AI 相关界面。如果当前安装的副本未获得企业版许可，只要存在该值，就会阻止**所有**脚本和宏运行，无论是否安全，并显示一条消息，说明所需的版本；宏会从菜单中消失，直到激活企业版许可证，且激活后无需重启就会恢复到菜单中。读取方无法解析的值会强制执行限制，而不是解除限制。显式的 `0` 不会强制实施该限制，但仍会被视为已配置，因此它同样会让 AI 相关界面只能在企业版中使用。

要在没有企业版许可证的情况下关闭所有 AI 功能，请使用通用 `DisableAi` 策略。

## 查看当前生效的策略

打开 **工具 > 偏好 > Tabular Editor > 更新和反馈**。当设置了任意策略时，**由你的组织管理**部分会列出 Tabular Editor 找到的每个值、该值本身，以及它来自哪个注册表项和注册表配置单元。 Tabular Editor 无法解释的值会标记为 _(无效)_，这是找出看似没有效果的策略中拼写错误的最快方法。

在 **偏好** 的其他位置，以及 **工具 > MCP Server...** 对话框中，凡是被策略锁定或限制的控件都会显示为只读，并带有工具提示，说明该设置由你的组织策略控制。

## 使用管理模板

Tabular Editor 3.27 及更高版本会安装一对组策略管理模板，因此可在组策略编辑器中设置上述策略，而不必直接编辑注册表。你可以在安装目录下的 `Policies` 文件夹中找到它们，默认路径为 `C:\Program Files\Tabular Editor 3\Policies`：

- `TabularEditorApS.admx`
- `en-US\TabularEditorApS.adml`

若要在单台计算机上使用它们，请将这两个文件复制到 `%SystemRoot%\PolicyDefinitions`，并保留 `en-US` 文件夹结构：

```
C:\Windows\PolicyDefinitions\TabularEditorApS.admx
C:\Windows\PolicyDefinitions\en-US\TabularEditorApS.adml
```

若要在整个域中使用它们，请改为将它们复制到域控制器上的中央存储，并保留相同的目录结构：

```
\\<your-domain>\SYSVOL\<your-domain>\Policies\PolicyDefinitions\TabularEditorApS.admx
\\<your-domain>\SYSVOL\<your-domain>\Policies\PolicyDefinitions\en-US\TabularEditorApS.adml
```

然后打开本地组策略编辑器 (`gpedit.msc`) 或组策略管理编辑器，并查看以下位置：

- 整台计算机范围的策略：**计算机配置 > 管理模板 > Tabular Editor**
- 按用户生效的策略位于 **用户配置 > 管理模板 > Tabular Editor** 下

Tabular Editor 3 与 CLI 共用的策略直接位于 **Tabular Editor** 下。仅 Tabular Editor 3 会遵循的策略位于 **Tabular Editor > Tabular Editor 3** 下；AI 助手、MCP 服务器和 DAX优化器集成则分别位于各自的子文件夹中。

将策略设置为 **已启用** 会写入其注册表值。将其设置为 **已禁用**，或保留为 **未配置**，表示该策略不会被强制执行。这些模板不会写入旧版 `Kapacity\Tabular Editor` 键，因此如果某项策略还需要作用于 Tabular Editor 2，请手动设置该键。

对于企业版策略，**已禁用** 会删除注册表值，而不是写入 `0`。这是刻意设计的：只要存在任何企业版相关的值，AI 助手和 MCP 服务器就会受到企业版许可证检查，因此管理员刚关闭的策略不能遗留任何值。

## 禁用 Web 通信

如果希望确保 Tabular Editor 不会发起任何 Web 请求，请设置 `DisableUpdates`、`DisableBpaDownload`、`DisableWebDaxFormatter`、`DisableErrorReports`、`DisableTelemetry`、`DisableDaxOptimizer`、`DisableDaxPackageManager` 和 `DisableAi` 策略。

> [!NOTE]
> 即使已指定上述策略，Tabular Editor 3 仍会偶尔向 `https://api.tabulareditor.com` 发起请求，用于许可证验证。如果 Tabular Editor 3 无法访问此终结点（例如由于防火墙或代理），用户就必须每 30 天为该产品执行一次[手动激活](xref:installation-activation-basic#manual-activation-no-internet)。

## 禁用自定义脚本

如果你想确保 Tabular Editor 不允许用户执行任意代码，请指定 `DisableCSharpScripts` 和 `DisableMacros` 策略。

如果贵组织希望保留脚本功能，但不希望任何脚本访问文件系统、网络或其他程序，请改用 `BlockUnsafeScripts`。脚本和宏仍可对模型执行操作，只有超出模型范围的部分会被拒绝。该策略需要企业版；上面两项则适用于所有版本。

## 禁用 AI 功能

如果希望禁用所有 AI 功能，请设置 `DisableAi` 策略。这会阻止任何与 AI 相关的内容在启动时加载，并清除任何已存储的 API 密钥配置。它适用于所有版本，无需企业版许可证。

从 3.27.0 开始，安装程序也会按相同的优先级从全部六个键读取该策略，并完全省略 AI 组件；因此，对于策略禁用了 AI 的计算机，AI 程序集永远不会写入其安装文件夹。将该值设置为 `1` 的 `REG_DWORD`：安装程序将 `1` 视为 _禁用_，将任何其他已存在的值视为 _未禁用_；而应用程序则接受任何非零值。有关同时部署功能选择和该策略的信息，请参阅[不带 AI 功能进行部署](xref:installation-activation-basic#deploying-without-the-ai-features)。

若要保留 AI 助手但限制其可执行的操作，请改用上述企业版策略：将权限上限设置为贵组织可接受的范围，将提供程序和终结点锁定到由贵方运营的 Gateway，并使用 `McpDisabledTools` 为已连接的代理禁用特定工具。
