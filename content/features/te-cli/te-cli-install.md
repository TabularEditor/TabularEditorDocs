---
uid: te-cli-install
title: Installation and Setup
author: Peer Grønnerup
updated: 2026-05-06
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

1. Sign in at [tabulareditor.com](https://tabulareditor.com/download-tabular-editor-cli) with a Tabular Editor account.
2. Download the archive for your platform and architecture:

   | Platform | 64-bit (Intel/AMD) | ARM64 | Archive |
   | -- | -- | -- | -- |
   | Windows | `te-win-x64.zip` | `te-win-arm64.zip` | `.zip` |
   | macOS | `te-osx-x64.tar.gz` (Intel) | `te-osx-arm64.tar.gz` (Apple Silicon) | `.tar.gz` |
   | Linux | `te-linux-x64.tar.gz` | `te-linux-arm64.tar.gz` | `.tar.gz` |

   Pick the ARM64 build on Apple Silicon Macs (M1 and newer), Windows on ARM devices, and ARM-based Linux servers (including AWS Graviton, Azure Ampere, and Raspberry Pi 64-bit). Pick the `x64` build on everything else.

## Install

Unzip the archive into a folder of your choice and add that folder to `PATH` so you can invoke `te` from any working directory.

### Windows (PowerShell)

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

#### Apple Silicon (ARM64)

```bash
mkdir -p ~/.local/bin
tar -xzf te-osx-arm64.tar.gz -C ~/.local/bin
chmod +x ~/.local/bin/te
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc   # or ~/.bashrc
```

#### Intel (x64)

```bash
mkdir -p ~/.local/bin
tar -xzf te-osx-x64.tar.gz -C ~/.local/bin
chmod +x ~/.local/bin/te
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc   # or ~/.bashrc
```

On macOS, the binary is signed with our Apple Developer ID and notarized by Apple, so the first run completes without a "cannot verify developer" Gatekeeper warning. Network access on first run is recommended so Gatekeeper can fetch the notarization ticket; offline first-runs may briefly prompt before being unblocked once network returns.

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
> The PATH change takes effect in **new** shell sessions. To run `te` in the shell where you ran the install, open a new terminal, or reload your profile: `source ~/.bashrc` / `source ~/.zshrc` on macOS/Linux, or close and reopen PowerShell on Windows.

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

The CLI prints a yellow preview banner on stderr by default. To suppress it run:

```bash
te config set hidePreviewNotice true
```

> [!WARNING]
> The banner reappears on every command within **14 days of the preview end date** (2026-09-30), regardless of `hidePreviewNotice`. This ensures you have visible warning before the CLI stops functioning.

## Shell completion

The CLI provides tab-completion scripts for **Bash**, **Zsh**, and **PowerShell**. Pick the block that matches your shell — each one installs the completion persistently for new shell sessions.

### Bash (macOS/Linux)

```bash
mkdir -p ~/.local/share/bash-completion/completions
te completion bash > ~/.local/share/bash-completion/completions/te
```

### Zsh (macOS/Linux)

```zsh
mkdir -p ~/.zfunc
te completion zsh > ~/.zfunc/_te
echo 'fpath=(~/.zfunc $fpath); autoload -U compinit; compinit' >> ~/.zshrc
```

### PowerShell (Windows/macOS/Linux)

```powershell
Add-Content $PROFILE 'te completion pwsh | Out-String | Invoke-Expression'
```

Open a new shell session for completion to take effect.

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
| Authentication: browser, device-code, service principal, env, managed identity | Yes | Yes |
| Connect to local SSAS instance (TCP transport) | Yes | **No** |
| Connect to Power BI Desktop (named-pipe transport) | Yes | **No** |

> [!IMPORTANT]
> Local SSAS and Power BI Desktop connections rely on Windows-only transport protocols. All cloud-based workflows (Power BI Service, Fabric, Azure Analysis Services) work on every platform.

## Updating

To update to a newer preview build, download the latest archive and overwrite the previous installation. Configuration and cached credentials are stored outside the install folder (see <xref:te-cli-config> and <xref:te-cli-auth>) and are preserved across updates.

## Uninstalling

1. Delete the install folder.
2. Remove the PATH entry.
3. (Optional) Clear cached credentials and config:
   - Run `te auth logout` first - it removes all cached tokens and SPN records from the active backend (OS keystore or file fallback).
   - Delete `~/.config/te/` (config and saved profiles).
   - Delete `~/.te-cli/` (residual cache files; only present when the file fallback was in use, or as legacy from older CLI builds).
   - To also purge the OS-native keystore entries - usually unnecessary, since `te auth logout` already clears them - see:
     - **Windows:** Credential Manager → Windows Credentials → entries named `com.tabulareditor.cli...` or `te-cli`.
     - **Linux:** `secret-tool search Component te-cli` and `secret-tool clear ...`, or use seahorse.
     - **macOS:** Keychain Access → search for `com.tabulareditor.cli`.

## Next steps

- @te-cli-auth - authenticate to Power BI, Fabric, or Azure Analysis Services.
- @te-cli-commands - full command reference.
- @te-cli-interactive - guided REPL mode.
