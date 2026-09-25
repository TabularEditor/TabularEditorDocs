---
uid: getting-started
title: Instalación y activación
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

# Instalación y activación

## Instalación

Descarga la versión más reciente de Tabular Editor 3 desde nuestra [página de descargas](xref:downloads).

We recommend the 64-bit `.exe` installer on .NET 10 for most scenarios. Once downloaded, double-click it and complete the installer pages.

![Instalar](~/content/assets/images/getting-started/install.png)

### Requisitos previos

For the `.exe` installer, the matching **.NET Desktop Runtime**: [10](https://dotnet.microsoft.com/download/dotnet/10.0) for the recommended build, or [8](https://dotnet.microsoft.com/download/dotnet/8.0) for the .NET 8 build. The installer offers to download and install it for you, so in practice there is nothing to do beforehand.

The other two packages differ. The `.msi` does not bring the runtime along, so install it yourself when deploying centrally, and the portable `.zip` is self-contained and needs no runtime at all.

### Requisitos del sistema

- **Sistema operativo:** Windows 10, Windows 11, Windows Server 2016, Windows Server 2019 o versiones posteriores
- **Arquitectura:** x64, ARM64 (nativo desde la versión 3.23.0)
- **.NET Runtime:** .NET Desktop Runtime 10 or 8, matching the build you install

See @system-requirements for the full matrix and for how to choose between the builds.

## Activación de su instalación

Tabular Editor 3 es software comercial. Visita nuestra [página principal](https://tabulareditor.com) para conocer los precios y las opciones de compra. Si no has usado antes Tabular Editor 3, puedes acceder a una prueba gratuita de 30 días.

La primera vez que inicie Tabular Editor 3 en un equipo nuevo, se le pedirá que active el producto.

![Activación del producto](~/content/assets/images/getting-started/product-activation.png)

### Activación con una clave de licencia existente

Cuando compres una licencia de Tabular Editor 3, recibirás un correo electrónico con una cadena de 25 caracteres, que es tu clave de licencia. Cuando se te solicite, escribe la clave de licencia y haz clic en **Siguiente >** para activar el producto.

![Introducir clave de licencia](~/content/assets/images/getting-started/enter-license-key.png)

> [!NOTE]
> Para los tipos de licencia multiusuario, además de la clave de licencia también debes introducir tu dirección de correo electrónico. Tabular Editor 3 te lo solicitará cuando la clave de licencia corresponda a una licencia multiusuario.

Las instalaciones de Tabular Editor 3 se activan **por usuario**. Si varios usuarios comparten el mismo equipo, cada usuario debe activar el producto en su propio perfil de usuario de Windows.

### Windows account vs Power BI / Entra account

The Windows account on which Tabular Editor 3 is installed is independent from the Microsoft Entra account used to authenticate against a Power BI / Fabric workspace.

- **License activation** is stored in the Windows Registry under `HKEY_CURRENT_USER` of the Windows user that activated the product. The license is not tied to any cloud identity.
- **Workspace authentication** happens at connection time in the **Load Semantic Model from Database** dialog. You sign in with the Microsoft Entra account that has permission on the workspace.

You do not need to launch Tabular Editor 3 with **Run as** under a different Windows account just because you use a separate Entra account (for example a non-mail-enabled admin account) to manage the Power BI workspace. Launch Tabular Editor 3 under your normal Windows account, activate it with your license key under that account, and provide your admin Entra credentials in the connection dialog.

For details on how Tabular Editor authenticates to the XMLA endpoint and how to pick the right authentication mode (for example **Microsoft Entra MFA** when your Windows login does not match your Power BI account), see @xmla-as-connectivity.

### Solicitar una licencia de prueba

Si no has usado antes Tabular Editor 3, puedes acceder a una prueba gratuita de 30 días. Al elegir esta opción, se te pedirá una dirección de correo electrónico. Usamos la dirección de correo electrónico para comprobar si ya tienes una activación previa de Tabular Editor 3.

> [!NOTE]
> Tabular Editor ApS no envía correos electrónicos no solicitados ni cede tu dirección de correo electrónico a terceros al registrarte para obtener una licencia de prueba de 30 días. Consulta nuestra @privacy-policy para obtener más información.

### Cambiar una clave de licencia

Una vez activado Tabular Editor 3, puedes cambiar la clave de licencia en el menú Ayuda seleccionando **Acerca de Tabular Editor**.

![About Te3](~/content/assets/images/getting-started/about-te3.png)

En el cuadro de diálogo, selecciona **Cambiar clave de licencia**. Esta opción solo está disponible cuando no hay ningún modelo cargado en Tabular Editor. Si hay un modelo abierto, ciérralo desde **Archivo > Cerrar modelo**. Al hacer clic en **Cambiar clave de licencia**, Tabular Editor te preguntará si quieres quitar la licencia actual:

![image](~/content/assets/images/getting-started-01.png)

Si aceptas, se quita la licencia actual y tendrás que volver a introducir una clave de licencia para usar el producto.

> [!IMPORTANT]
> Una vez eliminada una clave de licencia, el producto no puede ser utilizado por el usuario actual en ese equipo hasta que se introduzca una nueva clave de licencia.

## Configuración posterior a la instalación

Tabular Editor 3 provides many configuration options. The default settings are sufficient for most development scenarios, but review the options below.

### Check for updates on start-up

By default, whenever Tabular Editor 3 is launched, the tool checks online to see if a newer version is available. You control how this update check is performed under **Tools > Preferences > Updates and Feedback**.

> [!NOTE]
> Usa siempre la versión más reciente de Tabular Editor 3. Our support team assumes you are on the latest version before submitting a bug report.

### Opting out of telemetry collection

Tabular Editor 3 collects anonymous usage data and telemetry, which helps us improve the product. You opt out at any time by launching Tabular Editor 3 and navigating to **Tools > Preferences > Updates and Feedback**. Uncheck the **Help improve Tabular Editor by collecting anonymous usage data** checkbox to opt out.

![Collect Telemetry](~/content/assets/images/getting-started/collect-telemetry.png)

### Configuración del proxy

If you are on a network with limited internet connectivity, specify the address, username, and password of a proxy server under **Tools > Preferences > Proxy Settings**. This is required before Tabular Editor 3 can use any features that rely on outgoing web requests. Specifically:

- Update checks
- Activación del producto
- DAX Formatting
- Download of Best Practice Rules from external URLs

> [!TIP]
> The proxy settings can at times interfere with authentication dialog boxes or other external prompts. Try switching the proxy setting between **System** and **None**, then close and reopen Tabular Editor 3 to verify.

### Other preferences

Tabular Editor 3 contains many other settings for controlling application behavior. To learn more, see @preferences.

## Advanced scenarios

For manual (no-internet) activation, registry-based license management, silent deployment, and Enterprise seat administration, see @installation-activation-basic.

## Próximos pasos

- [Información general sobre la interfaz de usuario de Tabular Editor 3](xref:user-interface)
- @xmla-as-connectivity
- @migrate-from-vs
- @migrate-from-desktop
- @migrate-from-te2
- @installation-activation-basic
