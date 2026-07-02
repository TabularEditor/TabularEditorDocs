---
uid: te-cli-install
title: 安装与设置
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

# 安装与设置

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

Tabular Editor CLI 以单个自包含的可执行文件形式发布，名为 `te`（在 Windows 上为 `te.exe`）。 它无需任何外部运行时依赖。

## 下载

1. 使用 Tabular Editor 帐户在 [tabulareditor.com](https://tabulareditor.com/download-tabular-editor-cli) 登录。
2. 下载适用于你的平台和架构的压缩包：

   | 平台      | 64 位（Intel/AMD）            | ARM64                                | 压缩包       |
   | ------- | -------------------------- | ------------------------------------ | --------- |
   | Windows | `te-win-x64.zip`           | `te-win-arm64.zip`                   | `.zip`    |
   | macOS   | `te-osx-x64.tar.gz`（Intel） | `te-osx-arm64.tar.gz`（Apple Silicon） | `.tar.gz` |
   | Linux   | `te-linux-x64.tar.gz`      | `te-linux-arm64.tar.gz`              | `.tar.gz` |

   在 Apple Silicon Mac（M1 及更新机型）、Windows on ARM 设备以及基于 ARM 的 Linux 服务器（包括 AWS Graviton、Azure Ampere 和 64 位 Raspberry Pi）上，请选择 ARM64 版本。 其他情况都选 `x64` 版本。

## 安装

将压缩包解压到你选择的文件夹中，并将该文件夹添加到 `PATH`，这样你就可以在任意工作目录运行 `te`。

### Windows（PowerShell）

#### x64

```powershell
Expand-Archive te-win-x64.zip -DestinationPath "$env:LOCALAPPDATA\Programs\te"
[Environment]::SetEnvironmentVariable(
  "PATH",
  [Environment]::GetEnvironmentVariable("PATH", "User") + ";$env:LOCALAPPDATA\Programs\te",
  "User")
```

#### ARM64

```powershell
Expand-Archive te-win-arm64.zip -DestinationPath "$env:LOCALAPPDATA\Programs\te"
[Environment]::SetEnvironmentVariable(
  "PATH",
  [Environment]::GetEnvironmentVariable("PATH", "User") + ";$env:LOCALAPPDATA\Programs\te",
  "User")
```

### macOS

#### Apple Silicon（ARM64）

```bash
mkdir -p ~/.local/bin
tar -xzf te-osx-arm64.tar.gz -C ~/.local/bin
chmod +x ~/.local/bin/te
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc   # or ~/.bashrc
```

#### Intel（x64）

```bash
mkdir -p ~/.local/bin
tar -xzf te-osx-x64.tar.gz -C ~/.local/bin
chmod +x ~/.local/bin/te
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc   # or ~/.bashrc
```

在 macOS 上，二进制文件使用我们的 Apple Developer ID 进行签名，并已通过 Apple 公证，因此首次运行时不会出现“无法验证开发者”的 Gatekeeper 警告。 建议首次运行时保持联网，以便 Gatekeeper 获取公证票证；如果首次运行时处于离线状态，可能会短暂弹出提示，待网络恢复后即可放行。

### Linux

#### x64

```bash
mkdir -p ~/.local/bin
tar -xzf te-linux-x64.tar.gz -C ~/.local/bin
chmod +x ~/.local/bin/te
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc   # or ~/.zshrc
```

#### ARM64

```bash
mkdir -p ~/.local/bin
tar -xzf te-linux-arm64.tar.gz -C ~/.local/bin
chmod +x ~/.local/bin/te
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc   # or ~/.zshrc
```

> [!NOTE]
> PATH 的更改会在**新的** shell 会话中生效。 要在执行安装命令的同一 shell 中运行 `te`，请打开一个新终端，或重新加载你的配置文件：在 macOS/Linux 上运行 `source ~/.bashrc` / `source ~/.zshrc`，或者在 Windows 上关闭并重新打开 PowerShell。

## 验证

检查已安装的版本并列出可用命令：

```bash
te --version
te --help
```

`te --help` 会输出带颜色的帮助索引，并按命令类别分组显示。 每个子命令都支持 `--help`，用于查看详细用法：

```bash
te deploy --help
te bpa run --help
```

## 隐藏预览版横幅

CLI 默认会向 stderr 输出黄色的预览横幅提示。 要隐藏它，运行：

```bash
te config set hidePreviewNotice true
```

> [!WARNING]
> 无论是否设置 `hidePreviewNotice`，在预览结束日期（2026-09-30）**前 14 天内**，每次执行命令都会再次显示该横幅。 这样可确保在 CLI 停止工作前，你能看到明确的警告。

## Shell 自动补全

CLI 提供适用于 **Bash**、**Zsh**、**PowerShell** 和 **Fish** 的 Tab 自动补全脚本。 Pick the block that matches your shell - each one installs the completion persistently for new shell sessions.

### Bash（macOS/Linux）

```bash
mkdir -p ~/.local/share/bash-completion/completions
te completion bash > ~/.local/share/bash-completion/completions/te
```

### Zsh（macOS/Linux）

```zsh
mkdir -p ~/.zfunc
te completion zsh > ~/.zfunc/_te
echo 'fpath=(~/.zfunc $fpath); autoload -U compinit; compinit' >> ~/.zshrc
```

### PowerShell（Windows/macOS/Linux）

```powershell
Add-Content $PROFILE 'te completion pwsh | Out-String | Invoke-Expression'
```

### Fish（macOS/Linux）

```bash
te completion fish > ~/.config/fish/completions/te.fish
```

打开新的 shell 会话后，自动补全才会生效。

自动补全涵盖子命令、全局标志以及模型路径（在需要针对文件系统进行 tab 补全时）。

## 跨平台功能矩阵

大多数功能在各个平台上都相同。 少数功能依赖仅 Windows 支持的传输机制：

| 功能                                              | Windows | macOS / Linux |
| ----------------------------------------------- | ------- | ------------- |
| 加载/保存 BIM 和 TMDL                                | 是的      | 是             |
| 部署到 Power BI / Fabric / Azure Analysis Services | 是的      | 是             |
| Best Practice Analyzer 和 VertiPaq分析器            | 是的      | 是             |
| C# Script 脚本编写                                  | 是的      | 是             |
| 针对云端模型的 DAX 查询                                  | 是的      | 是             |
| 身份验证：浏览器、设备代码、服务主体、环境变量、托管身份                    | 是的      | 是             |
| 连接到本地 SSAS 实例（TCP 传输）                           | 是       | **否**         |
| 连接到 Power BI Desktop（命名管道传输）                    | 是       | **否**         |

> [!IMPORTANT]
> 本地 SSAS 和 Power BI Desktop 连接依赖于仅限 Windows 的传输协议。 所有基于云的工作流（Power BI Service、Fabric、Azure Analysis Services）均可在所有平台上运行。

## 更新

若要更新到较新的预览构建版本，请下载最新压缩包并覆盖之前的安装。 配置和缓存的凭据存储在安装文件夹之外（见 <xref:te-cli-config> 和 <xref:te-cli-auth>），更新时会保留。

## 卸载

1. 删除安装文件夹。
2. 从 PATH 中移除相应条目。
3. （可选）清除缓存的凭据和配置：
   - 先运行 `te auth logout`——它会从当前使用的存储后端（操作系统密钥存储或文件回退方案）中移除所有缓存的令牌和 SPN 记录。
   - 删除 `~/.config/te/`（配置及已保存的配置档案）。
   - 删除 `~/.te-cli/`（残留的缓存文件；仅在启用文件回退时才会存在，或是旧版 CLI 的遗留内容）。
   - 如果还要清除系统原生密钥存储中的条目——通常没必要，因为 `te auth logout` 已经会清除它们——请参见：
     - **Windows:** 凭据管理器 → Windows 凭据 → 名为 `com.tabulareditor.cli...` 或 `te-cli` 的条目。
     - **Linux:** `secret-tool search Component te-cli` 和 `secret-tool clear ...`，或使用 seahorse。
     - **macOS:** 钥匙串访问 → 搜索 `com.tabulareditor.cli`。

## 后续步骤

- @te-cli-auth - 用于对 Power BI、Fabric 或 Azure Analysis Services 进行身份验证。
- @te-cli-commands - 完整的命令参考。
- @te-cli-interactive - 引导式 REPL 模式。
