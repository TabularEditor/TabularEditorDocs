---
uid: installation-activation-basic
title: Instalación, activación y configuración básica
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

# Instalación, activación y configuración básica

## Resumen

Esta página cubre escenarios avanzados de instalación y activación de Tabular Editor 3: activación manual (sin conexión), gestión de licencias basada en el Registro, implementación desatendida y administración de puestos en la Edición Enterprise.

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

## Cambiar puestos en la Edición Enterprise

Para cambiar un puesto de la Edición Enterprise, anula el registro del usuario actual de ese puesto a través del [portal de autoservicio de Tabular Editor](https://tabulareditor.com/my-account/). El propietario de la suscripción o el administrador de licencias crea una cuenta o inicia sesión en una existente para administrar los puestos de licencia.

> [!NOTE]
> Cambiar un usuario solo es posible en la Edición Enterprise.

## Detalles del registro

Tabular Editor 3 almacena los detalles de activación de cada usuario de Windows en `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3`.

| Valor              | Tipo        | Contenido                                                                                                                                                    |
| ------------------ | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `LicenseKey`       | `REG_SZ`    | La clave de licencia                                                                                                                                         |
| `User`             | `REG_SZ`    | La dirección de correo electrónico del usuario con licencia, para licencias multiusuario                                                                     |
| `ActivationKey`    | `REG_SZ`    | La activación devuelta por el servicio de licencias                                                                                                          |
| `Activation`       | `REG_SZ`    | Una activación guardada por versiones anteriores de Tabular Editor 3. Tabular Editor 3 la elimina la próxima vez que almacena una activación |
| `InstallationDate` | `REG_QWORD` | La primera vez que este usuario de Windows inicia Tabular Editor 3. Tabular Editor 3 la crea al iniciarse si no existe                       |

Para ver la clave de licencia actual del usuario de Windows activo, ejecuta el siguiente comando en el Símbolo del sistema de Windows (Inicio > Ejecutar > cmd.exe):

```cmd
REG QUERY "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey
```

También puedes usar `regedit.exe` (Editor del Registro de Windows) y navegar hasta `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3` para ver y modificar los valores.

![Editor del Registro](~/content/assets/images/troubleshooting/registry-editor.png)

Un administrador del sistema también puede asignar de forma proactiva licencias de Tabular Editor 3 a un equipo, especificando los valores **LicenseKey** y **User** en la clave del Registro `SOFTWARE\Kapacity\Tabular Editor 3` de cada usuario. Consulta [Instalación desatendida y aprovisionamiento previo de la licencia](#silent-installation-and-license-pre-provisioning) para ver el procedimiento completo de implementación.

## Cambiar una clave de licencia

La opción **Cambiar clave de licencia** en **Ayuda > Acerca de Tabular Editor** elimina los valores `LicenseKey`, `User`, `ActivationKey` y `Activation`, y desactiva la instalación en el servicio de licencias. La opción solo aparece cuando no hay ningún modelo cargado y la licencia está activada o la reserva de asiento ha caducado. Si no aparece, por ejemplo porque la activación falló, restablece la licencia desde el Editor del Registro:

1. Cierra todas las instancias de Tabular Editor 3.
2. Abre el Editor del Registro de Windows (Inicio > Ejecutar > regedit.exe).
3. Localiza `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3` (consulta la captura de pantalla anterior).
4. Elimina los valores `LicenseKey`, `User`, `ActivationKey` y `Activation`. Deja `InstallationDate` tal cual.
5. Cierra el Editor del Registro y reinicia Tabular Editor 3.

Como alternativa, ejecuta los siguientes comandos en el Símbolo del sistema de Windows (Inicio > Ejecutar > cmd.exe). Un comando Report informa de un error si su valor no existe, y los demás comandos siguen ejecutándose:

```cmd
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey /f
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /v User /f
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /v ActivationKey /f
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /v Activation /f
```

La próxima vez que inicies Tabular Editor 3, se te pedirá una clave de licencia.

> [!NOTE]
> Eliminar los valores del registro no desactiva la instalación. Usa el [portal de autoservicio de Tabular Editor](https://tabulareditor.com/my-account/) para gestionar tus licencias activadas.

## Instalación desatendida y aprovisionamiento previo de la licencia

Puedes implementar Tabular Editor de forma desatendida y aprovisionar previamente la licencia a través del Registro de Windows. Instala primero y, después, escribe la licencia, que debe estar establecida antes de que la aplicación se inicie por primera vez.

### Instalar en silencio

Sin interfaz de usuario, sin reinicio:

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart /l*v C:\Temp\TE3_install.log
```

| MSI feature   | Se muestra en el instalador como | Descripción                                                     | Activar la instalación                                                                                                |
| ------------- | -------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `MainFeature` | Tabular Editor 3                 | Aplicación principal de Tabular Editor 3                        | Yes (required)                                                                                     |
| `AIAssistant` | Funciones de IA                  | The @ai-assistant and the @mcp-server | Yes, from 3.27.0. Earlier versions install it only when it's selected |

> [!IMPORTANT]
> From 3.27.0, a new installation includes the **AI features** component unless you exclude it. If your organization doesn't allow the AI Assistant or the MCP server, exclude the component and set the `DisableAi` policy as described below.

### Desplegar sin las funciones de IA

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
> Cuando uses `ADDLOCAL`, incluye `MainFeature` en la lista junto con cualquier característica opcional. Si especificas solo `AIAssistant` sin `MainFeature`, la instalación quedará incompleta.

### Upgrades and the AI features component

When you install a newer version of the same package over an existing installation, the installer keeps the feature selection the machine already has. This applies to interactive and silent installations. A machine deployed without the AI features before 3.27.0 stays without them after the upgrade, and a machine where the AI features were selected keeps them.

In these cases the installer applies the default selection or the selection on the command line:

| Situation                                                                                                                                                            | Resultado                                                                                                                                                                                         |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The command line sets `ADDLOCAL`, `REMOVE` or another feature property                                                                                               | The command line sets the selection. `ADDLOCAL=MainFeature` removes the AI features from machines that have them, and `ADDLOCAL=ALL` installs them on machines that don't         |
| The deployment uninstalls the earlier version before it installs the new one, for example an Intune supersedence set to uninstall                                    | The installation is new and includes the AI features unless the command line excludes them                                                                                                        |
| The package targets a different runtime than the installed one, for example the .NET 10 package on a machine with the .NET 8 package | The .NET 8 and .NET 10 packages are separate products. The installation is new and includes the AI features unless the command line excludes them |

The `DisableAi` policy overrides the selection in every case.

### Enforcing the decision with the DisableAi policy

A user who runs the installer gets the default selection, which includes the AI features. Set the `DisableAi` @policies to `1` under `HKEY_LOCAL_MACHINE\Software\Policies\Tabular Editor ApS\TE3` to keep the AI features off every installation on the machine. Tabular Editor 3 reads the policy at startup and turns off the AI Assistant and the MCP server.

From 3.27.0 the installer reads the policy as well:

- a new installation leaves out the AI features component, and the installer doesn't show it
- an upgrade removes the component from a machine that has it
- an existing installation keeps the AI files until the next upgrade. Tabular Editor 3 doesn't load them while the policy is set

A deployment tool that runs as the local system account doesn't read the `HKEY_CURRENT_USER` policies of the machine's users. Set the policy under `HKEY_LOCAL_MACHINE` for the installer to read it in a silent deployment.

### Nombres de paquetes y otras opciones de MSI

También puedes usar `/package` en lugar de `/i`. Reemplaza `<version>` por la cadena de versión real.

Los paquetes MSI se llaman `TabularEditor.<version>.<architecture>.<runtime>.msi`, por ejemplo `TabularEditor.3.27.0.x64.Net10.msi` o `TabularEditor.3.27.0.ARM64.Net8.msi`. Elige la arquitectura y el runtime que mejor se adapten a los equipos de destino; consulta @system-requirements. El MSI no instala el .NET Desktop Runtime, así que instálalo primero.

Para obtener información detallada sobre las opciones de línea de comandos de MSI disponibles, consulta la documentación oficial de Microsoft:
[Microsoft Standard Installer command-line options - Win32 apps | Microsoft Learn](https://learn.microsoft.com/windows/win32/msi/command-line-options)

### Aprovisiona previamente la licencia

Escribe la licencia en el Registro _antes de iniciar la aplicación por primera vez_:

```bat
REM Per-user license key (HKCU)
REG ADD "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey /t REG_SZ /d YOUR-25-CHAR-KEY /f
```

Si usas una clave de licencia de la **Edición Enterprise**, establece también el correo electrónico del usuario con licencia:

```bat
REG ADD "HKCU\Software\Kapacity\Tabular Editor 3" /v User /t REG_SZ /d user@example.com /f
```

**Notas**

- El instalador no acepta un parámetro de licencia; la licencia se gestiona mediante las entradas del Registro anteriores.
- Las claves se almacenan en **HKCU** (por usuario). Asegúrate de que los comandos se ejecuten en el contexto del usuario de destino (por ejemplo, mediante un script de inicio de sesión) para que los valores se escriban en el perfil correcto.
- Para conocer más claves y valores, consulta [Detalles del Registro](#registry-details).

