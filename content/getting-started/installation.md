---
uid: installation-activation-basic
title: Advanced installation and activation
author: Morten Lønskov
updated: 2026-10-14
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Advanced installation and activation

## Overview

This page covers advanced installation and activation scenarios for Tabular Editor 3: manual (offline) activation, registry-based license management, silent deployment, and Enterprise seat administration.

For the standard activation flow, see @getting-started.

## Manual activation (no internet)

If you do not have access to the internet, for example due to a proxy, Tabular Editor prompts you to do a manual activation.

![Manual Activation Prompt](~/content/assets/images/getting-started/Activation_manual_firstprompt.png)

After entering your e-mail, a dialog appears with a link to an activation key. Copy the URL and open it in a web browser that is connected to the internet.

The URL returns a JSON object:

![Manual Activation JSON Object](~/content/assets/images/getting-started/activation_manual_jsonobject.png)

Copy the full JSON object and paste it into the dialog. Your manual activation dialog ends up looking like the screenshot below.

![Manual Activation Filled In](~/content/assets/images/getting-started/activation_manual_dialogbox_filled.png)

Your Tabular Editor 3 license is then verified.

## Changing seats on Enterprise Edition

To change an Enterprise seat, deregister the existing user from the seat through the [Tabular Editor Self-Service portal](https://tabulareditor.com/my-account/). The subscription owner or license administrator creates an account, or logs in with an existing one, to administer the license seats.

> [!NOTE]
> Changing a user is only possible on the Enterprise Edition.

## Registry details

Tabular Editor 3 stores activation details for each Windows user under `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3`.

| Value | Type | Content |
|-------|------|---------|
| `LicenseKey` | `REG_SZ` | The license key |
| `User` | `REG_SZ` | The e-mail address of the licensed user, for multi-user licenses |
| `ActivationKey` | `REG_SZ` | The activation returned by the licensing service |
| `Activation` | `REG_SZ` | An activation written by older versions of Tabular Editor 3. Tabular Editor 3 deletes it the next time it stores an activation |
| `InstallationDate` | `REG_QWORD` | The first launch of Tabular Editor 3 for this Windows user. Tabular Editor 3 creates it on launch if it's missing |

To view the current license key for the active Windows user, run the following command in the Windows Command Prompt (Start > Run > cmd.exe):

```cmd
REG QUERY "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey
```

You can also use `regedit.exe` (Windows Registry Editor) and navigate to `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3` to view and modify the values.

![Registry Editor](~/content/assets/images/troubleshooting/registry-editor.png)

A system administrator can also proactively assign Tabular Editor 3 licenses to a machine by specifying the **LicenseKey** and **User** values under each user's `SOFTWARE\Kapacity\Tabular Editor 3` registry key. See [Silent installation and license pre-provisioning](#silent-installation-and-license-pre-provisioning) for the full deployment procedure.

## Changing a license key through the registry

The **Change license key** option in **Help > About Tabular Editor** removes the `LicenseKey`, `User`, `ActivationKey` and `Activation` values and deactivates the installation on the licensing service. The option appears only when no model is loaded and the license is activated or its seat reservation has expired. If it isn't shown, for example because activation failed, reset the license through the Registry Editor:

1. Close all instances of Tabular Editor 3.
2. Open the Registry Editor in Windows (Start > Run > regedit.exe).
3. Locate `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3` (see screenshot above).
4. Delete the `LicenseKey`, `User`, `ActivationKey` and `Activation` values. Leave `InstallationDate` in place.
5. Close the Registry Editor and restart Tabular Editor 3.

Alternatively, run the following commands in a Windows Command Prompt (Start > Run > cmd.exe). A command reports an error if its value doesn't exist, and the remaining commands still run:

```cmd
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey /f
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /v User /f
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /v ActivationKey /f
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /v Activation /f
```

The next time you launch Tabular Editor 3, you're prompted for a license key.

> [!NOTE]
> Deleting the registry values doesn't deactivate the installation, use the [Tabular Editor Self-service portal](https://tabulareditor.com/my-account/) to manage your activated licenses. 

## Silent installation and license pre-provisioning

You can deploy Tabular Editor silently and pre-provision the license through the Windows Registry. Install first, then write the license, which has to be in place before the application is launched for the first time.

### Install silently

No UI, no reboot:

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart /l*v C:\Temp\TE3_install.log
```

| MSI feature | Shown in the installer as | Description | Installed by default |
|-------------|---------------------------|-------------|----------------------|
| `MainFeature` | Tabular Editor 3 | Core Tabular Editor 3 application | Yes (required) |
| `AIAssistant` | AI features | The @ai-assistant and the @mcp-server | Yes, from 3.27.0. Earlier versions install it only when it's selected |

> [!IMPORTANT]
> From 3.27.0, a new installation includes the **AI features** component unless you exclude it. If your organization doesn't allow the AI Assistant or the MCP server, exclude the component and set the `DisableAi` policy as described below.

### Deploying without the AI features

Leave `AIAssistant` out of `ADDLOCAL` to install Tabular Editor 3 without the AI features:

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart ADDLOCAL=MainFeature /l*v C:\Temp\TE3_install.log
```

Run the package with `REMOVE` to remove the component from machines that already have it:

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart REMOVE=AIAssistant /l*v C:\Temp\TE3_install.log
```

Without the component, the AI assemblies aren't in the installation folder, the **AI Assistant** pane and the MCP server are absent from the application and no requests go to a model provider. Other features are unaffected.

To change the selection on a single machine, run the installer again and select **Modify** in the maintenance dialog.

> [!NOTE]
> When using `ADDLOCAL`, list `MainFeature` alongside any optional features. Specifying only `AIAssistant` without `MainFeature` results in an incomplete installation.

### Upgrades and the AI features component

When you install a newer version of the same package over an existing installation, the installer keeps the feature selection the machine already has. This applies to interactive and silent installations. A machine deployed without the AI features before 3.27.0 stays without them after the upgrade, and a machine where the AI features were selected keeps them.

In these cases the installer applies the default selection or the selection on the command line:

| Situation | Result |
|--|--|
| The command line sets `ADDLOCAL`, `REMOVE` or another feature property | The command line sets the selection. `ADDLOCAL=MainFeature` removes the AI features from machines that have them, and `ADDLOCAL=ALL` installs them on machines that don't |
| The deployment uninstalls the earlier version before it installs the new one, for example an Intune supersedence set to uninstall | The installation is new and includes the AI features unless the command line excludes them |
| The package targets a different runtime than the installed one, for example the .NET 10 package on a machine with the .NET 8 package | The .NET 8 and .NET 10 packages are separate products. The installation is new and includes the AI features unless the command line excludes them |

The `DisableAi` policy overrides the selection in every case.

### Enforcing the decision with the DisableAi policy

A user who runs the installer gets the default selection, which includes the AI features. Set the `DisableAi` @policies to `1` under `HKEY_LOCAL_MACHINE\Software\Policies\Tabular Editor ApS\TE3` to keep the AI features off every installation on the machine. Tabular Editor 3 reads the policy at startup and turns off the AI Assistant and the MCP server.

From 3.27.0 the installer reads the policy as well:

- a new installation leaves out the AI features component, and the installer doesn't show it
- an upgrade removes the component from a machine that has it
- an existing installation keeps the AI files until the next upgrade. Tabular Editor 3 doesn't load them while the policy is set

A deployment tool that runs as the local system account doesn't read the `HKEY_CURRENT_USER` policies of the machine's users. Set the policy under `HKEY_LOCAL_MACHINE` for the installer to read it in a silent deployment.

### Package names and other MSI options

You can also use `/package` instead of `/i`. Replace `<version>` with the actual version string.

MSI packages are named `TabularEditor.<version>.<architecture>.<runtime>.msi`, for example `TabularEditor.3.27.0.x64.Net10.msi` or `TabularEditor.3.27.0.ARM64.Net8.msi`. Pick the architecture and runtime that suit the target machines; see @system-requirements. The MSI does not install the .NET Desktop Runtime, so deploy that first.

For details on available MSI command-line options, see the official Microsoft documentation:
[Microsoft Standard Installer command-line options - Win32 apps | Microsoft Learn](https://learn.microsoft.com/windows/win32/msi/command-line-options)

### Pre-provision the license

Write the license to the Registry *before the first launch* of the application:

```bat
REM Per-user license key (HKCU)
REG ADD "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey /t REG_SZ /d YOUR-25-CHAR-KEY /f
```

If you are using an **Enterprise Edition** license key, also set the licensed user's e-mail:

```bat
REG ADD "HKCU\Software\Kapacity\Tabular Editor 3" /v User /t REG_SZ /d user@example.com /f
```

**Notes**

- The installer does not accept a license parameter; licensing is handled via the Registry entries above.
- Keys are stored under **HKCU** (per-user). Ensure the commands run in the context of the target user (for example via a logon script) so the values are written to the correct profile.
- For additional keys and values, see [Registry details](#registry-details).

