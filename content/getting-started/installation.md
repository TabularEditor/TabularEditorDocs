---
uid: installation-activation-basic
title: Installation, activation and basic configuration
author: Daniel Otykier
updated: 2021-09-30
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

## Installation

In order to install Tabular Editor 3, download the latest version from our [downloads page](xref:downloads).

We recommend downloading the MSI 64-bit installer, which is suitable in most scenarios. Once downloaded, doubleclick the MSI file and go through the installation pages.

![Install](~/content/assets/images/getting-started/install.png)

## Activating your installation

The first time you launch Tabular Editor 3 on a new machine, you are prompted to activate the product.

![Product activation](~/content/assets/images/getting-started/product-activation.png)

### Activating using an existing license key

Once you purchase a license for Tabular Editor 3, you should receive an e-mail with a 25-character string which is your license key. When prompted, enter the license key and hit "Next >" to activate the product.

![Enter License Key](~/content/assets/images/getting-started/enter-license-key.png)

> [!NOTE]
> For multi-user license types, you will need to enter your e-mail address in addition to the license key. Tabular Editor 3 will prompt you to do so, if the license key you enter represents a multi-user license.

#### Manual Activation (No Internet)
If you do not have access to the internet e.g., due to a proxy Tabular Editor will prompt you to do a manual activation. 

![Manual Activation Prompt](~/content/assets/images/getting-started/Activation_manual_firstprompt.png)

After entering your email, a dialog box appears with a link to an activation key.
Copy the URL and open it in a web-browser that is connected to the internet. 

The URL returns a JSON object:

![Manual Activation JSON Object](~/content/assets/images/getting-started/activation_manual_jsonobject.png)

Copy the full JSON object and paste the full JSON object given into the dialog box.
Your manual activation dialog should end up looking like below. 

![Manual Activation Filled In](~/content/assets/images/getting-started/activation_manual_dialogbox_filled.png)

Your Tabular Editor 3 license will thereby be verified.

### Changing a license key

When Tabular Editor 3 is activated, you may change your license key in the Help menu by choosing "About Tabular Editor".

![About Te3](~/content/assets/images/getting-started/about-te3.png)

In the dialog, select "Change license key". Note that this option is only available if no model is loaded in Tabular Editor. IF you already loaded a model you can close it under File > Close model.

For more details on managing the license keys, see [Registry details](xref:getting-started#registry-details).

## Basic configuration

After Tabular Editor 3 is activated, we recommend spending a few minutes familiarizing yourself with the [basic interface](xref:user-interface). In addition, Tabular Editor 3 provides many different configuration options. The default settings are sufficient for most development scenarios, but there are a few important configuration options that you should always review.

### Check for updates on start-up

By default, whenever Tabular Editor 3 is launched, the tool will check online to see if a newer version is available. You can control how this update check is performed under **Tools > Preferences > Updates and Feedback**.

> [!NOTE]
> We recommend always using the latest version of Tabular Editor 3. Our support team will generally assume that you are always using the latest version before submitting a bug report.

### Opting out of telemetry collection

Tabular Editor 3 collects anonymous usage data and telemetry, which helps us improve the product. You can opt out at any time by launching Tabular Editor 3 and navigating to **Tools > Preferences > Updates and Feedback**. Uncheck the **Help improve Tabular Editor by collecting anonymous usage data** checkbox to opt out.

![Collect Telemetry](~/content/assets/images/getting-started/collect-telemetry.png)

### Proxy settings

If you are on a network with limited Internet connectivity, you can specify the address, username and password of a proxy server under **Tools > Preferences > Proxy Settings**. This is required before Tabular Editor 3 can use any features that rely on outgoing web requests. Specifically, these are:

- Update checks
- Product activation
- DAX Formatting
- Download of Best Practice Rules from external URLs

> [!TIP]
> The proxy settings can at times interfere with authentication dialog boxes or other external prompts.
> Try to switch the proxy setting between "System" and "None", close and reopen Tabular Editor 3 to verify.

### Other preferences

In addition to the settings mentioned above, Tabular Editor 3 contains many other settings for controlling various application behavior, allowing you to closely tailor the tool to your needs. To learn more about other these settings, see @preferences.

## Next steps

- @migrate-from-vs
- @migrate-from-desktop
- @migrate-from-te2