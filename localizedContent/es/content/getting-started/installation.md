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

| Funcionalidad MSI | Se muestra en el instalador como | Descripción                                                 | Activar la instalación                                                                                                                        |
| ----------------- | -------------------------------- | ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `MainFeature`     | Tabular Editor 3                 | Aplicación principal de Tabular Editor 3                    | Sí (obligatorio)                                                                                                           |
| `AIAssistant`     | Funciones de IA                  | El @ai-assistant y el @mcp-server | Sí, a partir de la versión 3.27.0. Las versiones anteriores solo lo instalan si se selecciona |

> [!IMPORTANT]
> A partir de la versión 3.27.0, una nueva instalación incluye el componente de **funciones de IA** a menos que lo excluyas. Si tu organización no permite el Asistente de IA ni el servidor MCP, excluye el componente y configura la directiva `DisableAi` como se describe a continuación.

### Desplegar sin las funciones de IA

No incluyas `AIAssistant` en `ADDLOCAL` para instalar Tabular Editor 3 sin las funciones de IA:

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart ADDLOCAL=MainFeature /l*v C:\Temp\TE3_install.log
```

Ejecuta el paquete con `REMOVE` para quitar el componente de los equipos que ya lo tienen:

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart REMOVE=AIAssistant /l*v C:\Temp\TE3_install.log
```

Sin el componente, los ensamblados de IA no están en la carpeta de instalación; el panel del **Asistente de IA** y el servidor MCP no están disponibles en la aplicación, y no se envía ninguna solicitud a un proveedor de modelos. Las demás funciones no se ven afectadas.

Para cambiar la selección en un solo equipo, vuelve a ejecutar el instalador y selecciona **Modificar** en el cuadro de diálogo de mantenimiento.

> [!NOTE]
> Cuando uses `ADDLOCAL`, incluye `MainFeature` en la lista junto con cualquier característica opcional. Si especificas solo `AIAssistant` sin `MainFeature`, la instalación quedará incompleta.

### Actualizaciones y el componente de funciones de IA

Cuando instalas una versión más reciente del mismo paquete sobre una instalación existente, el instalador conserva la selección de funciones que ya tiene el equipo. Esto se aplica a las instalaciones interactivas y silenciosas. Un equipo implementado sin las funciones de IA antes de la versión 3.27.0 seguirá sin ellas después de la actualización, y un equipo en el que se seleccionaron las funciones de IA las conservará.

En estos casos, el instalador aplica la selección predeterminada o la selección indicada en la línea de comandos:

| Situación                                                                                                                                                               | Resultado                                                                                                                                                                                                          |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| La línea de comandos establece `ADDLOCAL`, `REMOVE` u otra propiedad de característica                                                                                  | La línea de comandos establece la selección. `ADDLOCAL=MainFeature` quita las funciones de IA de los equipos que las tienen, y `ADDLOCAL=ALL` las instala en los equipos que no las tienen         |
| La implementación desinstala la versión anterior antes de instalar la nueva; por ejemplo, una sustitución de Intune configurada para desinstalar                        | La instalación es nueva e incluye las funciones de IA, a menos que la línea de comandos las excluya                                                                                                                |
| El paquete usa un entorno de ejecución distinto del instalado; por ejemplo, el paquete de .NET 10 en un equipo con el paquete de .NET 8 | Los paquetes de .NET 8 y .NET 10 son productos independientes. La instalación es nueva e incluye las funciones de IA, a menos que la línea de comandos las excluya |

La directiva `DisableAi` prevalece sobre la selección en todos los casos.

### Imponer la decisión con la directiva DisableAi

Un usuario que ejecuta el instalador obtiene la selección predeterminada, que incluye las funciones de IA. Establece `DisableAi` @policies en `1` bajo `HKEY_LOCAL_MACHINE\Software\Policies\Tabular Editor ApS\TE3` para mantener desactivadas las funciones de IA en todas las instalaciones del equipo. Tabular Editor 3 lee la directiva al iniciarse y desactiva el Asistente de IA y el servidor MCP.

A partir de la versión 3.27.0, el instalador también lee la directiva:

- una nueva instalación omite el componente de funciones de IA y el instalador no lo muestra
- una actualización elimina el componente de un equipo que lo tiene
- una instalación existente conserva los archivos de IA hasta la siguiente actualización. Tabular Editor 3 no los carga mientras la directiva esté establecida

Una herramienta de implementación que se ejecuta con la cuenta del sistema local no lee las directivas de `HKEY_CURRENT_USER` de los usuarios del equipo. Configura la directiva en `HKEY_LOCAL_MACHINE` para que el instalador la lea en una implementación desatendida.

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

