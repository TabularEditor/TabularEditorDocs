---
uid: system-requirements
title: Requisitos del sistema
author: Morten Lønskov
updated: 2026-09-14
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

# Requisitos del sistema

Tabular Editor 3 is a Windows desktop application. From version 3.27.0 it is published on two .NET runtimes, for two processor architectures, in three package formats.

## Operating system

- Windows 10, Windows 11, Windows Server 2016, Windows Server 2019 or newer

Which Windows versions are supported at any given moment follows Microsoft's .NET supported OS policy for the runtime you install, so it can narrow over time independently of Tabular Editor.

## What is published

| Runtime                                                    | Arquitectura | Formats                                   |
| ---------------------------------------------------------- | ------------ | ----------------------------------------- |
| .NET 10 _(recommended)_ | x64, ARM64   | `.exe` installer, `.msi`, portable `.zip` |
| .NET 8                                     | x64, ARM64   | `.exe` installer, `.msi`, portable `.zip` |

The .NET 10 and .NET 8 builds are _functionally identical_. Nothing is available in one and missing from the other, and the two can be installed side by side.

ARM64 builds are native, from version 3.23.0 onwards.

## Entorno de ejecución para «.NET»

| Build            | Needs                                                                                                                                                                                                                                                                                                        |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `.exe` installer | The matching [.NET Desktop Runtime](https://dotnet.microsoft.com/download/dotnet): [10](https://dotnet.microsoft.com/download/dotnet/10.0) or [8](https://dotnet.microsoft.com/download/dotnet/8.0). The installer offers to download and install it for you |
| `.msi`           | The matching .NET Desktop Runtime, installed beforehand. The MSI does _not_ bring it along, which is what makes it suitable for unattended deployment                                                                                                                        |
| Portable `.zip`  | Nothing. It is self-contained                                                                                                                                                                                                                                                                |

It must be the _Desktop_ runtime. The ASP.NET Core runtime and the plain .NET runtime do not carry the Windows Forms and WPF libraries the application needs.

## Choosing a build

Take the **.NET 10 x64 `.exe` installer** unless you have a reason not to. The reasons are:

- **ARM64**: you are on an ARM-based PC
- **.NET 8**: your organization cannot install the .NET 10 desktop runtime yet
- **`.msi`**: you are deploying centrally. See [silent installation](xref:installation-activation-basic)
- **portable `.zip`**: you cannot install software on the machine, or you want several versions side by side

## Optional components

| Component                                                                                   | Needed for                                                                 | Notas                                                                                                                                                                                                      |
| ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Microsoft Edge WebView2 runtime](https://developer.microsoft.com/microsoft-edge/webview2/) | The in-application **Get Started** page and the @ai-assistant | Present on current Windows installations. Where it is missing, Tabular Editor falls back to the built-in browser control or offers a link to open the page in your default browser         |
| AI features                                                                                 | The @ai-assistant and the MCP server                          | An installer component, selected by default. It can be deselected during installation, and an administrator can disable AI features regardless with the `DisableAi` @policies |

## Where the downloads are

See @downloads for the current version, and @release-history for previous ones.

## Pasos a seguir

- @downloads
- @getting-started
- @installation-activation-basic
