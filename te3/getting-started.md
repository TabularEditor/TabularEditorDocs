﻿---
uid: getting-started
title: Getting Started
author: Daniel Otykier
updated: 2021-09-08
---
# Getting Started

## Installation

Download the latest version of Tabular Editor 3 from our [downloads page](xref:downloads).

## Prerequisites

None.

## System requirements

- **Operating system:** Windows 7, Windows 8, Windows 10, Windows 11, Windows Server 2016, Windows Server 2019 or newer
- **.NET Runtime:** [.NET Desktop Runtime 6.0.8](https://dotnet.microsoft.com/en-us/download/dotnet/6.0)

## Activating your installation

Tabular Editor 3 is commercial software. Visit our [home page](https://tabulareditor.com) for pricing details and purchase options. If you haven't previously used Tabular Editor 3 you are eligible to a free 30-day trial.

The first time you launch Tabular Editor 3 on a new machine, you are prompted to activate the product.

![Product activation](~/images/product-activation.png)

### Activating using an existing license key

Once you purchase a license for Tabular Editor 3, you should receive an e-mail with a 25-character string which is your license key. When prompted, enter the license key and hit "Next >" to activate the product.

![Enter License Key](~/images/enter-license-key.png)

> [!NOTE]
> For multi-user license types, you will need to enter your e-mail address in addition to the license key. Tabular Editor 3 will prompt you to do so, if the license key you enter represents a multi-user license.

Note that Tabular Editor 3 installations are activated **per user**. In other words, if multiple users share the same machine, each user will have to activate the product on their Windows user profile.

### Requesting a trial license

If you haven't used Tabular Editor 3 before, you are eligible to a free 30-day trial. When choosing this option, you will be prompted for an e-mail address. We use the e-mail address to validate whether or not you have an existing activation of Tabular Editor 3.

> [!NOTE]
> Tabular Editor ApS will not sent unsolicited e-mails or forward your e-mail address to third parties, when signing up for a 30-day trial license. View our @privacy-policy for more information.

### Changing a license key

When Tabular Editor 3 is activated, you may change your license key in the Help menu by choosing "About Tabular Editor".

![About Te3](~/images/about-te3.png)

In the dialog, select "Change license key". Note that this option is only available if no model is loaded in Tabular Editor. If you already loaded a model you can close it under File > Close model. Once you click "Change license key", Tabular Editor will prompt you whether you want to remove the current license:

![image](https://user-images.githubusercontent.com/8976200/146754154-e691810b-342d-4311-8278-33da240d8d08.png)

By accepting this, the current license is removed, and you will have to re-enter a license key to use the product.

> [!IMPORTANT]
> Once a license key is removed, as described above, the product will not be usable by the current user on that machine until a new license key is entered.

#### Registry details

Tabular Editor 3 uses the registry database for storing activation details. An alternative to using the "About Tabular Editor" dialog for changing the license key as shown above, is to enter the registry database and delete all values from within the `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3` registry key.

A system administrator may assign Tabular Editor 3 licenses by specifying the LicenseKey and User values in the corresponding users `HKEY_USERS\{Profile-ID}\SOFTWARE\Kapacity\Tabular Editor 3` registry key.

![Registry Editor](~/images/registry-editor.png)

### Changing a license key through the registry

If for some reason you are unable to change the license key using the procedure outlined above, you can always "reset" the license assigned to Tabular Editor 3 by using the Registry Editor.

1. Close all instances of Tabular Editor 3
2. Open the Registry Editor in Windows (Start > Run > regedit.msc)
3. Locate `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3` (see screenshot above)
4. Delete the User, LicenseKey and Activation values
5. Close the Registry Editor and restart Tabular Editor 3

Tabular Editor 3 should now prompt you for a license key, similar to when the tool was first installed on the machine.

## Next steps

- [Overview of Tabular Editor 3's user interface](xref:user-interface)
- [What's new in Tabular Editor 3](whats-new.md)
- [Tabular Editor 3 Onboarding Guide](xref:onboarding-te3)
