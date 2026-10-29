---
uid: installation-activation-basic
title: Instalación y activación avanzadas
author: Morten Lønskov
updated: 2026-10-23
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

# Instalación y activación avanzadas

## Información general

Esta página trata de los escenarios avanzados de instalación y activación de Tabular Editor 3: activación manual (sin conexión), gestión de licencias basada en el registro, implementación silenciosa y administración de licencias de usuario de la edición Enterprise.

Para conocer el proceso de activación estándar, consulte @getting-started.

## Activación manual (sin conexión a Internet)

Si no tienes acceso a Internet, por ejemplo, debido a un proxy, Tabular Editor te pedirá que realices una activación manual.

![Mensaje de activación manual](~/content/assets/images/getting-started/Activation_manual_firstprompt.png)

Después de introducir su correo electrónico, aparecerá un cuadro de diálogo con un enlace a una clave de activación. Copie la URL y ábrala en un navegador web que esté conectado a Internet.

La URL devuelve un objeto JSON:

![Objeto JSON de activación manual](~/content/assets/images/getting-started/activation_manual_jsonobject.png)

Copia el objeto JSON completo y pégalo en el cuadro de diálogo. Su cuadro de diálogo de activación manual acabará teniendo el aspecto que se muestra en la captura de pantalla a continuación.

![Activación manual completada](~/content/assets/images/getting-started/activation_manual_dialogbox_filled.png)

A continuación, se verifica su licencia de Tabular Editor 3.

## Cambio de puestos en la Edición Enterprise

Para cambiar una licencia Enterprise, da de baja al usuario existente de la licencia a través del [portal de autoservicio de Tabular Editor](https://tabulareditor.com/my-account/). El titular de la suscripción o el administrador de licencias crea una cuenta, o inicia sesión con una existente, para administrar las plazas de licencia.

> [!NOTE]
> Cambiar un usuario solo es posible en la Edición Enterprise.

## Detalles del registro

Tabular Editor 3 almacena los datos de activación de cada usuario de Windows en `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3`.

| Valor | Tipo | Contenido |
|-------|------|---------|
| `LicenseKey` | `REG_SZ` | La clave de licencia |
| `User` | `REG_SZ` | La dirección de correo electrónico del usuario con licencia, para licencias multiusuario |
| `ActivationKey` | `REG_SZ` | La activación devuelta por el servicio de licencias |
| `Activation` | `REG_SZ` | Una activación escrita por versiones anteriores de Tabular Editor 3. Tabular Editor 3 la elimina la próxima vez que almacena una activación |
| `InstallationDate` | `REG_QWORD` | El primer inicio de sesión de Tabular Editor 3 para este usuario de Windows. Tabular Editor 3 lo crea al iniciarse si no existe |

Para ver la clave de licencia actual del usuario activo de Windows, ejecute el siguiente comando en el símbolo del sistema de Windows (Inicio > Ejecutar > cmd.exe):

```cmd
REG QUERY "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey
```

También puedes usar `regedit.exe` (Editor del Registro de Windows) y navegar hasta `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3` para ver y modificar los valores.

![Editor del Registro](~/content/assets/images/troubleshooting/registry-editor.png)

Un administrador del sistema también puede asignar de forma proactiva licencias de Tabular Editor 3 a un equipo especificando los valores **LicenseKey** y **User** en la clave de registro `SOFTWARE\Kapacity\Tabular Editor 3` de cada usuario. Consulta [Instalación silenciosa y aprovisionamiento previo de licencias](#silent-installation-and-license-pre-provisioning) para conocer el procedimiento de implementación completo.

## Cambio de una clave de licencia a través del registro

La opción **Cambiar clave de licencia** en **Ayuda > Acerca de Tabular Editor** elimina los valores `LicenseKey`, `User`, `ActivationKey` y `Activation` y desactiva la instalación en el servicio de licencias. La opción solo aparece cuando no hay ningún modelo cargado y la licencia está activada o su reserva de licencia ha caducado. Si no se muestra, por ejemplo, porque la activación ha fallado, restablezca la licencia a través del Editor del Registro:

1. Cierra todas las instancias de Tabular Editor 3.
2. Abra el Editor del Registro en Windows (Inicio > Ejecutar > regedit.exe).
3. Busca `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3` (consulta la captura de pantalla anterior).
4. Elimine los valores `LicenseKey`, `User`, `ActivationKey` y `Activation`. Deje `InstallationDate` donde está.
5. Cierre el Editor del Registro y reinicie Tabular Editor 3.

Como alternativa, ejecuta los siguientes comandos en un símbolo del sistema de Windows (Inicio > Ejecutar > cmd.exe). Un comando informa de un error si su valor no existe, pero los comandos restantes se ejecutan igualmente:

```cmd
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey /f
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /v User /f
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /v ActivationKey /f
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /v Activation /f
```

La próxima vez que inicies Tabular Editor 3, se te pedirá una clave de licencia.

> [!NOTE]
> Eliminar los valores del registro no desactiva la instalación. Utiliza el [Portal de autoservicio de Tabular Editor](https://tabulareditor.com/my-account/) para gestionar tus licencias activadas. 

## Instalación silenciosa y aprovisionamiento previo de licencias

Puedes implementar Tabular Editor de forma silenciosa y aprovisionar previamente la licencia a través del Registro de Windows. Primero instale y, a continuación, introduzca la licencia, que debe estar en su sitio antes de iniciar la aplicación por primera vez.

### Instalación silenciosa

Sin interfaz de usuario, sin reinicio:

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart /l*v C:\Temp\TE3_install.log
```

| Función MSI | Mostrada en el instalador como | Descripción | Instalada de forma predeterminada |
|-------------|---------------------------|-------------|----------------------|
| `MainFeature` | Tabular Editor 3 | Aplicación principal de Tabular Editor 3 | Sí (obligatoria) |
| `AIAssistant` | Funciones de IA | El @ai-assistant y el @mcp-server | Sí, a partir de la versión 3.27.0. Las versiones anteriores lo instalan solo cuando está seleccionado |

> [!IMPORTANT]
> A partir de la versión 3.27.0, una nueva instalación incluye el componente **Funciones de IA**, a menos que lo excluyas. Si tu organización no permite el Asistente de IA ni el servidor MCP, excluye el componente y establece la política `DisableAi` como se describe a continuación.

### Implementación sin las funciones de IA

Deja `AIAssistant` fuera de `ADDLOCAL` para instalar Tabular Editor 3 sin las funciones de IA:

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart ADDLOCAL=MainFeature /l*v C:\Temp\TE3_install.log
```

Ejecute el paquete con `REMOVE` para eliminar el componente de los equipos que ya lo tengan:

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart REMOVE=AIAssistant /l*v C:\Temp\TE3_install.log
```

Sin el componente, los ensamblados de IA no están en la carpeta de instalación, el panel **Asistente de IA** y el servidor MCP no están presentes en la aplicación y no se envían solicitudes a ningún proveedor de modelos. Las demás funciones no se ven afectadas.

Para cambiar la selección en un solo equipo, vuelve a ejecutar el instalador y selecciona **Modificar** en el cuadro de diálogo de mantenimiento.

> [!NOTE]
> Cuando utilice `ADDLOCAL`, incluya `MainFeature` junto con cualquier función opcional. Si se especifica solo `AIAssistant` sin `MainFeature`, la instalación quedará incompleta.

### Actualizaciones y el componente de funciones de IA

Cuando instala una versión más reciente del mismo paquete sobre una instalación existente, el instalador mantiene la selección de funciones que ya tiene el equipo. Esto se aplica a las instalaciones interactivas y silenciosas. Un equipo implementado sin las funciones de IA antes de la versión 3.27.0 se queda sin ellas después de la actualización, y un equipo en el que se seleccionaron las funciones de IA las conserva.

En estos casos, el instalador aplica la selección predeterminada o la selección de la línea de comandos:

| Situación | Resultado |
|--|--|
| La línea de comandos establece `ADDLOCAL`, `REMOVE` u otra propiedad de función | La línea de comandos establece la selección. `ADDLOCAL=MainFeature` elimina las funciones de IA de los equipos que las tienen, y `ADDLOCAL=ALL` las instala en los equipos que no las tienen |
| La implementación desinstala la versión anterior antes de instalar la nueva, por ejemplo, una sustitución de Intune configurada para desinstalar | La instalación es nueva e incluye las funciones de IA, a menos que la línea de comandos las excluya |

La política `DisableAi` anula la selección en todos los casos.

### Cambiar entre los paquetes .NET 8 y .NET 10

Los paquetes .NET 8 y .NET 10 se sustituyen entre sí. Cuando instala uno en un equipo que tiene la otra edición en la misma versión o en una versión anterior, el instalador elimina la otra edición antes de instalar ningún archivo y conserva la selección de funciones de esa edición. Un dispositivo que tenga instaladas ambas ediciones tendrá una sola instalación después de la siguiente instalación, y en **Configuración > Aplicaciones > Aplicaciones instaladas** aparecerá un solo **Tabular Editor 3**.

Si la otra edición está instalada en una versión más reciente, la instalación se detiene y aparece un mensaje. Desinstala primero la edición más reciente y, a continuación, vuelve a ejecutar el instalador.

### Aplicar la decisión con la directiva DisableAi

Un usuario que ejecute el instalador obtendrá la selección predeterminada, que incluye las funciones de IA. Establezca las @políticas `DisableAi` en `1` en `HKEY_LOCAL_MACHINE\Software\Policies\Tabular Editor ApS\TE3` para mantener desactivadas las funciones de IA en todas las instalaciones del dispositivo. Tabular Editor 3 lee la política al iniciarse y desactiva el Asistente de IA y el servidor MCP.

A partir de la versión 3.27.0, el instalador también lee la directiva:

- Una nueva instalación omite el componente de funciones de IA, y el instalador no lo muestra.
- Una actualización elimina el componente de un equipo que lo tiene.
- Una instalación existente conserva los archivos de IA hasta la siguiente actualización. Tabular Editor 3 no los carga mientras la política esté establecida.

Una herramienta de implementación que se ejecuta como la cuenta del sistema local no lee las políticas `HKEY_CURRENT_USER` de los usuarios del equipo. Establece la política en `HKEY_LOCAL_MACHINE` para que el instalador la lea en una implementación silenciosa.

### Nombres de paquetes y otras opciones de MSI

También puedes usar `/package` en lugar de `/i`. Sustituye `<version>` por la cadena de la versión real.

Los paquetes MSI se denominan `TabularEditor.<version>.<architecture>.<runtime>.msi`, por ejemplo, `TabularEditor.3.27.0.x64.Net10.msi` o `TabularEditor.3.27.0.ARM64.Net8.msi`. Elija la arquitectura y el tiempo de ejecución que se adapten a los equipos de destino; consulte @system-requirements. El MSI no instala .NET Desktop Runtime, así que despliéguelo primero.

Para obtener más información sobre las opciones de línea de comandos de MSI disponibles, consulte la documentación oficial de Microsoft:
[Opciones de la línea de comandos del instalador estándar de Microsoft - Aplicaciones Win32 | Microsoft Learn](https://learn.microsoft.com/windows/win32/msi/command-line-options)

### Aprovisionar previamente la licencia

Escribe la licencia en el Registro *antes del primer inicio* de la aplicación:

```bat
REM Per-user license key (HKCU)
REG ADD "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey /t REG_SZ /d YOUR-25-CHAR-KEY /f
```

Si está utilizando una clave de licencia de la **Edición Enterprise**, establezca también el correo electrónico del usuario con licencia:

```bat
REG ADD "HKCU\Software\Kapacity\Tabular Editor 3" /v User /t REG_SZ /d user@example.com /f
```

**Notas**

- El instalador no acepta un parámetro de licencia; las licencias se gestionan a través de las entradas del Registro indicadas anteriormente.
- Las claves se guardan en **HKCU** (por usuario). Asegúrese de que los comandos se ejecuten en el contexto del usuario de destino (por ejemplo, mediante un script de inicio de sesión) para que los valores se escriban en el perfil correcto.
- Para conocer otras claves y valores, consulte [Detalles del Registro](#registry-details).

