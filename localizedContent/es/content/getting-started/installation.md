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

## Descripción general

Esta página abarca escenarios avanzados de instalación y activación de Tabular Editor 3: activación manual (sin conexión), administración de licencias mediante el Registro, despliegue desatendido y administración de asientos de la Edición Enterprise.

Para el flujo de activación estándar, consulta @getting-started.

## Activación manual (sin Internet)

Si no tienes acceso a Internet, por ejemplo, debido a un proxy, Tabular Editor te pedirá que realices una activación manual.

![Aviso de activación manual](~/content/assets/images/getting-started/Activation_manual_firstprompt.png)

Después de introducir tu correo electrónico, aparece un cuadro de diálogo con un enlace a una clave de activación. Copia la URL y ábrela en un navegador web conectado a Internet.

La URL devuelve un objeto JSON:

![Objeto JSON de activación manual](~/content/assets/images/getting-started/activation_manual_jsonobject.png)

Copia el objeto JSON completo y pégalo en el cuadro de diálogo. El cuadro de diálogo de activación manual debería quedar como el que se muestra a continuación.

![Activación manual completada](~/content/assets/images/getting-started/activation_manual_dialogbox_filled.png)

De este modo, se verificará tu licencia de Tabular Editor 3.

## Cambiar asientos en la Edición Enterprise

Para cambiar un asiento de la Edición Enterprise, desasigna al usuario actual de ese asiento desde el [portal de autoservicio de Tabular Editor](https://tabulareditor.com/my-account/). El propietario de la suscripción o el administrador de licencias crea una cuenta, o inicia sesión con una cuenta existente, para administrar los asientos de la licencia.

> [!NOTE]
> Solo se puede cambiar de usuario en la Edición Enterprise.

## Detalles del Registro

Tabular Editor 3 usa el Registro de Windows para almacenar los detalles de activación.

Para ver la clave de licencia actual asignada al equipo, ejecuta el siguiente comando en el Símbolo del sistema de Windows (Inicio > Ejecutar > cmd.exe):

```cmd
REG QUERY "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey
```

También puedes usar `regedit.exe` (Editor del Registro de Windows) y navegar hasta `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3` para ver y modificar los valores **LicenseKey** y **User**.

![Editor del Registro](~/content/assets/images/troubleshooting/registry-editor.png)

Un administrador del sistema también puede asignar de forma proactiva licencias de Tabular Editor 3 a un equipo especificando los valores **LicenseKey** y **User** en la clave del Registro `SOFTWARE\Kapacity\Tabular Editor 3` de cada usuario. Consulta [Instalación desatendida y preaprovisionamiento de licencias](#silent-installation-and-license-pre-provisioning) para ver el procedimiento de despliegue completo.

## Cambiar una clave de licencia

En el cuadro de diálogo, selecciona "Cambiar clave de licencia". Ten en cuenta que esta opción solo está disponible si no hay ningún modelo cargado en Tabular Editor.

1. Cierra todas las instancias de Tabular Editor 3.
2. Abre el Editor del Registro en Windows (Inicio > Ejecutar > regedit.msc).
3. Localiza `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3` (consulta la captura de pantalla anterior).
4. Elimina todos los valores de esta clave.
5. Cierra el Editor del Registro y reinicia Tabular Editor 3.

Como alternativa, ejecuta el siguiente comando en el Símbolo del sistema de Windows (Inicio > Ejecutar > cmd.exe):

```cmd
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /va
```

La primera vez que inicias Tabular Editor 3 en un equipo nuevo, se te pedirá que actives el producto.

## Instalación desatendida y preaprovisionamiento de licencias

You can deploy Tabular Editor silently and pre-provision the license through the Windows Registry. Install first, then write the license, which has to be in place before the application is launched for the first time.

### Install silently

No UI, no reboot:

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart /l*v C:\Temp\TE3_install.log
```

| Característica de MSI | Shown in the installer as | Descripción                                       | Activar la instalación                           |
| --------------------- | ------------------------- | ------------------------------------------------- | ------------------------------------------------ |
| `MainFeature`         | Tabular Editor 3          | Aplicación principal de Tabular Editor 3          | Sí (obligatorio)              |
| `AIAssistant`         | AI features               | The @ai-assistant and the MCP server | Yes, from 3.27.0 |

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
> When using `ADDLOCAL`, list `MainFeature` alongside any optional features. Si especificas solo `AIAssistant` sin `MainFeature`, la instalación quedará incompleta.

### Package names and other MSI options

También puedes usar `/package` en lugar de `/i`. Reemplaza `<version>` por la cadena de versión real.

MSI packages are named `TabularEditor.<version>.<architecture>.<runtime>.msi`, for example `TabularEditor.3.27.0.x64.Net10.msi` or `TabularEditor.3.27.0.ARM64.Net8.msi`. Pick the architecture and runtime that suit the target machines; see @system-requirements. The MSI does not install the .NET Desktop Runtime, so deploy that first.

Para obtener información detallada sobre las opciones de línea de comandos de MSI disponibles, consulta la documentación oficial de Microsoft:
[Opciones de la línea de comandos de Microsoft Standard Installer - aplicaciones Win32 | Microsoft Learn](https://learn.microsoft.com/windows/win32/msi/command-line-options)

### Pre-provision the license

Write the license to the Registry _before the first launch_ of the application:

```bat
REM Clave de licencia por usuario (HKCU)
REG ADD "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey /t REG_SZ /d YOUR-25-CHAR-KEY /f
```

Si usas una clave de licencia de la **Edición Enterprise**, configura también el correo electrónico del usuario licenciado:

```bat
REG ADD "HKCU\Software\Kapacity\Tabular Editor 3" /v User /t REG_SZ /d user@example.com /f
```

**Notas**

- El instalador no acepta un parámetro de licencia; la licencia se gestiona mediante las entradas del Registro anteriores.
- Las claves se almacenan en **HKCU** (por usuario). Asegúrate de ejecutar los comandos en el contexto del usuario de destino (por ejemplo, mediante un script de inicio de sesión) para que los valores se escriban en el perfil correcto.
- Para obtener más claves y valores, consulta [Detalles del registro](#registry-details).

