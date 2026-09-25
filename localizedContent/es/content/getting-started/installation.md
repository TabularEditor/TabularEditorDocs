---
uid: installation-activation-basic
title: Instalación, activación y configuración básica
author: Morten Lønskov
updated: 2026-09-15
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

# Instalación, activación y configuración básica

## Resumen

This page covers advanced installation and activation scenarios for Tabular Editor 3: manual (offline) activation, registry-based license management, silent deployment, and Enterprise seat administration.

For the standard activation flow, see @getting-started.

## Activación manual (sin Internet)

Si no tienes acceso a Internet, por ejemplo, debido a un proxy, Tabular Editor te pedirá que realices una activación manual.

![Aviso de activación manual](~/content/assets/images/getting-started/Activation_manual_firstprompt.png)

Después de introducir tu correo electrónico, aparece un cuadro de diálogo con un enlace a una clave de activación. Copia la URL y ábrela en un navegador web conectado a Internet.

La URL devuelve un objeto JSON:

![Objeto JSON de activación manual](~/content/assets/images/getting-started/activation_manual_jsonobject.png)

Copia el objeto JSON completo y pégalo en el cuadro de diálogo. El cuadro de diálogo de activación manual debería quedar como el que se muestra a continuación.

![Activación manual completada](~/content/assets/images/getting-started/activation_manual_dialogbox_filled.png)

De este modo, se verificará tu licencia de Tabular Editor 3.

## Changing seats on Enterprise Edition

To change an Enterprise seat, deregister the existing user from the seat through the [Tabular Editor Self-Service portal](https://tabulareditor.com/my-account/). The subscription owner or license administrator creates an account, or logs in with an existing one, to administer the license seats.

> [!NOTE]
> Changing a user is only possible on the Enterprise Edition.

## Registry details

Tabular Editor 3 uses the Windows Registry to store activation details.

To view the current license key assigned to the machine, run the following command in the Windows Command Prompt (Start > Run > cmd.exe):

```cmd
REG QUERY "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey
```

You can also use `regedit.exe` (Windows Registry Editor) and navigate to `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3` to view and modify the **LicenseKey** and **User** values.

![Editor del Registro](~/content/assets/images/troubleshooting/registry-editor.png)

A system administrator can also proactively assign Tabular Editor 3 licenses to a machine by specifying the **LicenseKey** and **User** values under each user's `SOFTWARE\Kapacity\Tabular Editor 3` registry key. See [Silent installation and license pre-provisioning](#silent-installation-and-license-pre-provisioning) for the full deployment procedure.

## Cambiar una clave de licencia

En el cuadro de diálogo, selecciona "Cambiar clave de licencia". Ten en cuenta que esta opción solo está disponible si no hay ningún modelo cargado en Tabular Editor.

1. Cierra todas las instancias de Tabular Editor 3.
2. Open the Registry Editor in Windows (Start > Run > regedit.msc).
3. Locate `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3` (see screenshot above).
4. Elimina todos los valores de esta clave.
5. Close the Registry Editor and restart Tabular Editor 3.

Alternatively, run the following command in a Windows Command Prompt (Start > Run > cmd.exe):

```cmd
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /va
```

La primera vez que inicias Tabular Editor 3 en un equipo nuevo, se te pedirá que actives el producto.

## Silent installation and license pre-provisioning

You can deploy Tabular Editor silently and pre-provision the license through the Windows Registry. Install first, then write the license, which has to be in place before the application is launched for the first time.

### Install silently

No UI, no reboot:

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart /l*v C:\Temp\TE3_install.log
```

| MSI Feature   | Shown in the installer as | Descripción                                       | Activar la instalación                           |
| ------------- | ------------------------- | ------------------------------------------------- | ------------------------------------------------ |
| `MainFeature` | Tabular Editor 3          | Core Tabular Editor 3 application                 | Yes (Required)                |
| `AIAssistant` | AI features               | The @ai-assistant and the MCP server | Yes, from 3.27.0 |

> [!IMPORTANT]
> The command above installs the **AI features** component. Up to 3.26.x it had to be selected deliberately and a default installation left it out; from 3.27.0 it is part of a default installation. If your organization does not want the AI Assistant or the MCP server on user machines, you have to say so explicitly, as described in the next section.

### Deploying without the AI features

To keep the AI files off the machine, name the features you want and leave `AIAssistant` out:

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart ADDLOCAL=MainFeature /l*v C:\Temp\TE3_install.log
```

To take the component off machines that already have it, run the same package with `REMOVE`:

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart REMOVE=AIAssistant /l*v C:\Temp\TE3_install.log
```

Either way, the AI assemblies are never written to the installation folder, the **AI Assistant** pane and the MCP server are absent from the application, and nothing reaches out to a model provider. Everything else in Tabular Editor 3 is unaffected.

Upgrading an existing installation keeps the feature selection that machine already has, so a machine that was deployed without the AI features before 3.27.0 does not gain them by being upgraded. Pass `ADDLOCAL=MainFeature` on fresh installations, where there is no earlier selection to inherit.

> [!IMPORTANT]
> The command line controls what _you_ deploy, not what a user can install: the AI features are the default, so anyone who runs the installer themselves gets them. To make the decision stick, set the `DisableAi` @policies as well. From 3.27.0 the installer reads that policy and leaves the AI component out on its own, whoever runs it and however it is run, and the policy also turns the AI Assistant and the MCP server off at runtime if the component is already present. Set it machine-wide, under `HKEY_LOCAL_MACHINE\Software\Policies\Tabular Editor ApS\TE3`, so it applies to every user and cannot be overridden per user.

> [!NOTE]
> When using `ADDLOCAL`, list `MainFeature` alongside any optional features. Specifying only `AIAssistant` without `MainFeature` results in an incomplete installation.

### Package names and other MSI options

You can also use `/package` instead of `/i`. Replace `<version>` with the actual version string.

MSI packages are named `TabularEditor.<version>.<architecture>.<runtime>.msi`, for example `TabularEditor.3.27.0.x64.Net10.msi` or `TabularEditor.3.27.0.ARM64.Net8.msi`. Pick the architecture and runtime that suit the target machines; see @system-requirements. The MSI does not install the .NET Desktop Runtime, so deploy that first.

For details on available MSI command-line options, see the official Microsoft documentation:
[Microsoft Standard Installer command-line options - Win32 apps | Microsoft Learn](https://learn.microsoft.com/windows/win32/msi/command-line-options)

### Pre-provision the license

Write the license to the Registry _before the first launch_ of the application:

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

