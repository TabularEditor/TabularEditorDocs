---
uid: getting-started
title: Installation and Activation
author: Morten Lønskov
updated: 2025-09-23
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
# Getting Started

## Installation

Download the latest version of Tabular Editor 3 from our [downloads page](xref:downloads).

## Prerequisites

None.

## System requirements

- **Operating system:** Windows 10, Windows 11, Windows Server 2016, Windows Server 2019 or newer
- **Architecture:** x64,  ARM64 (native from 3.23.0)
- **.NET Runtime:** [.NET Desktop Runtime 8.0](https://dotnet.microsoft.com/en-us/download/dotnet/8.0)

See the .NET supported OS policy for current Windows versions supported by each runtime.

## Activating your installation

Tabular Editor 3 is commercial software. Visit our [home page](https://tabulareditor.com) for pricing details and purchase options. If you haven't previously used Tabular Editor 3 you are eligible to a free 30-day trial.

The first time you launch Tabular Editor 3 on a new machine, you are prompted to activate the product.

![Product activation](~/content/assets/images/getting-started/product-activation.png)

### Activating using an existing license key

Once you purchase a license for Tabular Editor 3, you should receive an e-mail with a 25-character string which is your license key. When prompted, enter the license key and hit "Next >" to activate the product.

![Enter License Key](~/content/assets/images/getting-started/enter-license-key.png)

> [!NOTE]
> For multi-user license types, you will need to enter your e-mail address in addition to the license key. Tabular Editor 3 will prompt you to do so, if the license key you enter represents a multi-user license.

Note that Tabular Editor 3 installations are activated **per user**. In other words, if multiple users share the same machine, each user will have to activate the product on their Windows user profile.

### Requesting a trial license

If you haven't used Tabular Editor 3 before, you are eligible to a free 30-day trial. When choosing this option, you will be prompted for an e-mail address. We use the e-mail address to validate whether or not you have an existing activation of Tabular Editor 3.

> [!NOTE]
> Tabular Editor ApS will not sent unsolicited e-mails or forward your e-mail address to third parties, when signing up for a 30-day trial license. View our @privacy-policy for more information.

### Changing a license key

When Tabular Editor 3 is activated, you may change your license key in the Help menu by choosing "About Tabular Editor".

![About Te3](~/content/assets/images/getting-started/about-te3.png)

In the dialog, select "Change license key". Note that this option is only available if no model is loaded in Tabular Editor. If you already loaded a model you can close it under File > Close model. Once you click "Change license key", Tabular Editor will prompt you whether you want to remove the current license:

![image](https://user-images.githubusercontent.com/8976200/146754154-e691810b-342d-4311-8278-33da240d8d08.png)

By accepting this, the current license is removed, and you will have to re-enter a license key to use the product.

> [!IMPORTANT]
> Once a license key is removed, as described above, the product will not be usable by the current user on that machine until a new license key is entered.

#### Registry details

Tabular Editor 3 uses the Windows Registry to store activation details.

To view the current license key assigned to the machine, run the following command in the Windows Command Prompt (Start > Run > cmd.exe):

```cmd
REG QUERY "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey
```

You can also use `regedit.exe` (Windows Registry Editor) and navigate to `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3` to view and modify the **LicenseKey** and **User** values.

A system administrator may also proactively assign Tabular Editor 3 licenses to a machine by specifying the **LicenseKey** and **User** values under each user’s `SOFTWARE\Kapacity\Tabular Editor 3` registry key.

![Registry Editor](~/content/assets/images/troubleshooting/registry-editor.png)

### Changing a license key through the registry

If, for any reason, you are unable to change the license key using the procedure outlined above, you can always reset the license assigned to Tabular Editor 3 by using the Registry Editor:

1. Close all instances of Tabular Editor 3.  
2. Open the Registry Editor in Windows (Start > Run > regedit.msc).  
3. Locate `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3` (see screenshot above).  
4. Delete all values within this key.  
5. Close the Registry Editor and restart Tabular Editor 3.

Alternatively, run the following command in a Windows Command Prompt (Start > Run > cmd.exe):

```cmd
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /va
```

The next time you launch Tabular Editor 3, you will be prompted for a license key, just as when the tool was first installed on the machine.

### Silent installation and license pre-provisioning

You can deploy Tabular Editor silently and pre-provision the license through the Windows Registry.

1. **Install silently** (no UI, no reboot):
   ```powershell
   msiexec /i TabularEditor.<version>.x64.Net8.msi /qn /norestart /l*v C:\Temp\TE3_install.log
   ```

You may also use `/package` instead of `/i`. Replace `<version>` with the actual version string. Use the ARM64 MSI if applicable.

For details on available MSI command-line options, please refer to the official Microsoft documentation:  
[Microsoft Standard Installer command-line options - Win32 apps | Microsoft Learn](https://learn.microsoft.com/windows/win32/msi/command-line-options)

2. **Write the license to the Registry** **before the first launch** of the application:
   ```bat
   REM Per-user license key (HKCU)
   REG ADD "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey /t REG_SZ /d YOUR-25-CHAR-KEY /f
   ```

   If you are using an **Enterprise Edition** license key, also set the licensed user’s e‑mail:
   ```bat
   REG ADD "HKCU\Software\Kapacity\Tabular Editor 3" /v User /t REG_SZ /d user@example.com /f
   ```

**Notes**
- The installer does **not** accept a license parameter; licensing is handled via the Registry entries above.
- Keys are stored under **HKCU** (per-user). Ensure the commands run in the context of the target user (e.g., via logon script or similar) so the values are written to the correct profile.
- For additional keys and values, see the [Registry details](#registry-details).

## Next steps

- [Overview of Tabular Editor 3's user interface](xref:user-interface)