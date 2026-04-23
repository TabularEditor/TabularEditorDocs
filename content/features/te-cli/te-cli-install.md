---
uid: te-cli-install
title: Installation and Setup
author: Peer Grønnerup
updated: 2026-04-20
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      none: true
    - product: Tabular Editor CLI
      full: true
---
# Installation and Setup

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

The Tabular Editor CLI ships as a single self-contained executable named `te` (`te.exe` on Windows). It has no external runtime dependencies.

## Download

1. Sign in at [tabulareditor.com](https://tabulareditor.com) with a Tabular Editor account.
2. Download the archive for your platform and architecture:

   | Platform | 64-bit (Intel/AMD) | ARM64 |
   | -- | -- | -- |
   | Windows | `win-x64` | `win-arm64` |
   | macOS | `osx-x64` (Intel) | `osx-arm64` (Apple Silicon) |
   | Linux | `linux-x64` | `linux-arm64` |

   Pick the ARM64 build on Apple Silicon Macs (M1 and newer), Windows on ARM devices, and ARM-based Linux servers (including AWS Graviton, Azure Ampere, and Raspberry Pi 64-bit). Pick the `x64` build on everything else.

<!-- TBD: replace with the official download URL once confirmed with marketing. -->

## Install

Unzip the archive into a folder of your choice and add that folder to `PATH` so you can invoke `te` from any working directory.

### Windows (PowerShell)

```powershell
# Substitute te-win-x64.zip or te-win-arm64.zip depending on your machine.
Expand-Archive te-win-x64.zip -DestinationPath "$env:LOCALAPPDATA\Programs\te"

# Add to PATH (current user, persistent)
[Environment]::SetEnvironmentVariable(
  "PATH",
  [Environment]::GetEnvironmentVariable("PATH", "User") + ";$env:LOCALAPPDATA\Programs\te",
  "User")
```

Restart the terminal for the PATH change to take effect.

### macOS / Linux

```bash
# Substitute the archive that matches your platform/arch:
#   macOS Apple Silicon: te-osx-arm64.zip
#   macOS Intel:         te-osx-x64.zip
#   Linux x64:           te-linux-x64.zip
#   Linux ARM64:         te-linux-arm64.zip
mkdir -p ~/.local/bin
unzip te-osx-arm64.zip -d ~/.local/bin
chmod +x ~/.local/bin/te

# Ensure ~/.local/bin is on PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc   # or ~/.bashrc
```

On macOS, the first run may trigger a Gatekeeper quarantine warning. Remove the quarantine attribute with:

```bash
xattr -d com.apple.quarantine ~/.local/bin/te
```

## Verify

Check the installed version and list available commands:

```bash
te --version
te --help
```

`te --help` prints a colorized help index grouping commands by family. Every subcommand accepts `--help` for detailed usage:

```bash
te deploy --help
te bpa run --help
```

## Hide the preview banner

The CLI prints a yellow preview banner on stderr by default. To suppress it for routine commands:

```bash
te config set hidePreviewNotice true
```

> [!WARNING]
> The banner reappears on every command within **14 days of expiry** (2026-09-30), regardless of `hidePreviewNotice`. This ensures you have visible warning before the CLI stops functioning.

## Shell completion

Generate a shell completion script for your shell of choice:

```bash
te completion bash    > /etc/bash_completion.d/te
te completion zsh     > "${fpath[1]}/_te"
te completion pwsh   | Out-String | Invoke-Expression
```

Completion covers subcommands, global flags, and model paths (where tab-completion against the filesystem is meaningful).

## Cross-platform feature matrix

Most features are identical across platforms. A handful depend on Windows-only transports:

| Feature | Windows | macOS / Linux |
| -- | -- | -- |
| Load/save BIM and TMDL | Yes | Yes |
| Deploy to Power BI / Fabric / Azure Analysis Services | Yes | Yes |
| Best Practice Analyzer and VertiPaq Analyzer | Yes | Yes |
| C# scripting | Yes | Yes |
| DAX queries against cloud models | Yes | Yes |
| Auth: browser, device-code, service principal, env, managed identity | Yes | Yes |
| Connect to local SSAS instance (TCP transport) | Yes | No |
| Connect to Power BI Desktop (named-pipe transport) | Yes | No |

Local SSAS and Power BI Desktop connections rely on Windows-only transport protocols. All cloud-based workflows (Power BI Service, Fabric, Azure Analysis Services) work on every platform.

## Updating

To update to a newer preview build, download the latest archive and overwrite the previous installation. Configuration and cached credentials are stored outside the install folder (see @te-cli-config and @te-cli-auth) and are preserved across updates.

## Uninstalling

1. Delete the install folder.
2. Remove the PATH entry.
3. (Optional) Clear cached credentials and config:
   - Windows / Linux: `~/.te-cli/`, `~/.config/te/`
   - macOS: `~/.te-cli/token-cache.bin`, `~/.config/te/`

## Next steps

- @te-cli-auth — authenticate to Power BI, Fabric, or Azure Analysis Services.
- @te-cli-commands — full command reference.
- @te-cli-interactive — guided REPL mode.
