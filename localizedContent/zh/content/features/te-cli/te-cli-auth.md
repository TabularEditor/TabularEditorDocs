---
uid: te-cli-auth
title: 身份验证与连接
author: Peer Grønnerup
updated: 2026-06-11
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      none: true
    - product: Tabular Editor CLI
      full: true
---

# 身份验证与连接

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

Tabular Editor CLI 使用与 Tabular Editor 3 相同的 Power BI Desktop 客户端 ID 来对 Power BI 服务、Microsoft Fabric 和 Azure Analysis Services 进行身份验证。 令牌会缓存在本地，因此你只需进行一次身份验证，之后无需再次登录即可重新运行命令，直到刷新令牌过期（通常为 90 天）。

## 身份验证方法

该 CLI 支持完整的 Azure Identity 凭据链：

| 方法          | 适用场景                                                          | `--auth` 值                          |
| ----------- | ------------------------------------------------------------- | ----------------------------------- |
| 自动          | 先尝试使用环境凭据，然后使用缓存凭据或通过交互式浏览器登录                                 | `auto`（默认）                          |
| 交互式浏览器      | 本地开发 - 打开系统浏览器                                                | `interactive`                       |
| 服务主体（客户端机密） | 自动化、CI/CD、无界面环境、SSH 或 WSL                                     | `spn`（配合 `-u / -p / -t`）或 `env`     |
| 服务主体（证书）    | 需要基于证书身份验证的自动化场景                                              | `spn`（配合 `-u / -t / --certificate`） |
| 环境变量        | `AZURE_CLIENT_ID` / `AZURE_CLIENT_SECRET` / `AZURE_TENANT_ID` | `env`                               |
| 托管标识        | Azure 虚拟机、Azure 容器应用、Azure Functions                          | `managed-identity`                  |

> [!NOTE]
> `--auth` 是一个**全局**选项，所有 `te` 命令都可用，而不只是 `te auth login`。 将其传递给 [`te deploy`](xref:te-cli-commands#deploy)、[`te refresh`](xref:te-cli-commands#refresh)、[`te query`](xref:te-cli-commands#query)、[`te connect`](xref:te-cli-commands#connect)，或任何其他需要连接远程端点的命令，以覆盖该次调用的默认身份验证链。 默认值 (`auto`) 会先尝试环境凭据，然后再回退到缓存的登录信息或交互式浏览器登录。

对于无界面、SSH、WSL 或 devcontainer 场景，可使用服务主体：`te auth login -u <id> -p <secret> -t <tenant>`（或 `--certificate`）。 登录会被缓存，因此后续命令可通过 `--auth auto` 静默获取令牌。

## `te auth login`

进行身份验证并缓存结果，供后续命令使用：

```bash
# Browser-based interactive login (default)
te auth login

# Service principal with client secret
te auth login -u "$AZURE_CLIENT_ID" -p "$AZURE_CLIENT_SECRET" -t "$AZURE_TENANT_ID"

# Service principal - read secret from stdin
echo "$AZURE_CLIENT_SECRET" | te auth login -u "$AZURE_CLIENT_ID" -p - -t "$AZURE_TENANT_ID"

# Service principal with certificate
te auth login -u "$AZURE_CLIENT_ID" -t "$AZURE_TENANT_ID" --certificate ./sp.pfx --certificate-password "$CERT_PASSWORD"

# Managed identity (Azure-hosted)
te auth login --identity     # Alias: -I
```

服务主体登录成功后，CLI 会**缓存凭据**，这样后续所有 `te` 命令都能静默获取令牌，无需再次传入 `-u / -p / -t`，也不用设置 `AZURE_CLIENT_*` 环境变量。 传入 `--save=false` 可进行一次性登录且不更新缓存，或者运行 `te auth logout` 清除缓存。

> [!WARNING]
> 在命令行中直接传递密钥会使其暴露在进程列表和 shell 历史记录中。 优先使用 `AZURE_CLIENT_SECRET` 环境变量，或通过 stdin 配合 `-p -` 管道传入密钥。

## `te auth status`

显示当前身份验证状态，无需打开浏览器：

```bash
te auth status
te auth status --output-format json
```

如果存在有效会话，则返回退出代码 `0`；如果未登录或会话已过期，则返回 `1`。

## `te auth logout`

清除所有缓存的凭据：

```bash
te auth logout
```

## 凭据存储

默认情况下，CLI 会将访问令牌和刷新令牌以及服务主体记录存储在**操作系统原生的安全存储**中。 仅当操作系统密钥库不可用时（例如无界面 Linux 且未安装 libsecret/D-Bus），才会自动回退为 `0600` 权限的文件存储。

| 平台       | 后端               | 存储位置                                                |
| -------- | ---------------- | --------------------------------------------------- |
| Windows  | DPAPI            | 按用户存储，由 MSAL 管理                                     |
| Linux    | libsecret（系统密钥环） | 按用户存储，由 MSAL 管理                                     |
| macOS    | 钥匙串              | 服务 `com.tabulareditor.cli.*`，账户 `te-msal-cache.bin` |
| 任意平台（回退） | `0600` 文件        | `~/.te-cli/te-msal-cache.bin` 以及每个键对应的 `.bin` blob  |

交互式浏览器流和服务主体流共用同一缓存；MSAL 的账户模型会区分它们，不会有单独的 `auth-record*.json` 配套文件。 使用 `--debug` 运行任意命令，即可查看启动时选择了哪个后端。

无论当前使用哪个后端，`te auth logout` 都会清除所有缓存记录（包括 MSAL 令牌缓存和所有 SPN blob）。

## `te connect`：设置活动连接

`te connect` 会为当前终端会话保存一个活动连接。 之后支持 `-s` / `-d` 的命令可以省略这两个参数：

```bash
# Remote workspace
te connect my-workspace my-model

# Local TMDL folder, .bim file, or .SemanticModel container
te connect ./my-model

# Connect to a running Power BI Desktop instance (Windows only)
te connect --local

# Filter by report name when multiple Power BI Desktop instances are running
te connect --local my-report

# Show the active connection
te connect

# Clear the active connection (and any workspace mirror)
te connect --clear
```

活动连接状态按终端会话分别保存：打开新的终端会话后将重新开始。 通过 [`te session`](xref:te-cli-commands#session) 查看或清理会话状态。

### 工作区模式（Workspace，`-w` / `--workspace`）

`te connect -w <target>` 会将一个主源与一个辅助镜像配对，因此后续每次执行 `--save` 都会同时写入两者。 可用它让远程模型的本地工作副本保持同步，或在保存时将本地修改推送到 Workspace：

```bash
# Mirror remote workspace ↔ local TMDL folder
te connect Finance "Revenue Model" -w ./revenue-model

# Mirror local source ↔ remote workspace (initial deploy + auto-redeploy on save)
te connect ./revenue-model -w Finance "Revenue Model"
```

保存顺序始终是 **先本地，后远程**，因此即使推送到服务器失败，磁盘上的副本也能反映用户的最新更改。 有关 `--workspace-format`、覆盖语义以及清理镜像，请参阅 [工作区模式](xref:te-cli-commands#workspace-mode--w----workspace)。

## 连接到不同的云

对于以下目标，CLI 会从服务器 URL 中检测正确的作用域：

- Power BI 服务和 Fabric（商业云、美国政府云、中国云和德国云）
- Azure Analysis Services (`asazure://...`)
- 本地 SSAS（`localhost`、命名实例，仅限 Windows）

`--server` 可传入 XMLA endpoint、Workspace 名称或 `powerbi://` URL：

```bash
te connect "powerbi://api.powerbi.com/v1.0/myorg/Finance" "Revenue Model"
te connect "powerbi://api.powerbi.com/v1.0/SpaceParts/Finance" "Revenue Model"
te connect "asazure://westeurope.asazure.windows.net/myaas" "MyModel"
te connect localhost "AdventureWorks"
```

## 连接配置文件

为便于反复使用同一连接——尤其是在部署到多个环境时——请保存具名配置文件：

```bash
# Save remote and local profiles
te profile set prod -s my-workspace -d my-model --description "Production"
te profile set dev --model ./model --description "Local dev TMDL"

# List and inspect
te profile list
te profile show prod

# Use a profile as the active connection
te connect --profile prod

# One-shot use without changing the active connection
te deploy ./model --profile staging --force
```

配置文件还可以包含行为覆盖项，并在配置文件激活时生效：

```bash
# In dev, disable the BPA gate on deploy and loosen validation
te profile set dev --bpa-on-deploy false --validate-on-mutation false

# In prod, force auto-format before any mutation
te profile set prod --auto-format true
```

有关可覆盖行为的完整列表，请参见 @te-cli-config。

## 非交互式身份验证

对于 CI/CD 管道、代理或任何无人值守场景，可结合以下方式避免交互式流程：

- `--non-interactive` 全局标志（不会提示，而是立即失败）。
- 以下任一非交互式身份验证方法：`env`、`managed-identity`，或显式提供的服务主体凭据。

适用于管道的基于环境变量的示例：

```bash
export AZURE_CLIENT_ID="your-app-id"
export AZURE_CLIENT_SECRET="your-client-secret"
export AZURE_TENANT_ID="your-tenant-id"

te deploy ./model -s my-workspace -d my-model \
  --auth env \
  --non-interactive \
  --force \
  --ci github
```

完整的 GitHub Actions 和 Azure DevOps Pipelines 示例，参见 @te-cli-cicd。

## 身份验证环境变量

当使用 `--auth env`（以及作为 `auto` 链的一部分）时，CLI 会遵循标准的 Azure.Identity 环境变量：

| 变量                              | 用途                                                                                                                  |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `AZURE_CLIENT_ID`               | 服务主体应用程序 ID。                                                                                                        |
| `AZURE_CLIENT_SECRET`           | 服务主体客户端机密。 需与 `AZURE_CLIENT_ID` 和 `AZURE_TENANT_ID` 配合使用。                                                           |
| `AZURE_TENANT_ID`               | 服务主体的租户（目录）ID。                                                                                                      |
| `AZURE_CLIENT_CERTIFICATE_PATH` | 用于基于证书的服务主体身份验证的 PEM 或 PKCS12 证书文件的 PATH。 需与 `AZURE_CLIENT_ID` 和 `AZURE_TENANT_ID` 配合使用。                            |
| `AZURE_AUTHORITY_HOST`          | 为主权云覆盖授权主机（例如 `login.microsoftonline.us`, `login.partner.microsoftonline.cn`, `login.microsoftonline.de`）。 默认使用商业云。 |

有关 CLI 专用环境变量（配置 PATH、调试日志、TE2 兼容性），请参见 @te-cli-config。

## 后续步骤

- @te-cli-commands - 连接后可执行的操作。
- @te-cli-config - 配置与配置文件的行为。
- @te-cli-cicd - 使用服务主体和托管标识的流水线示例。
