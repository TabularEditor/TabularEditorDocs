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

Puedes desplegar Tabular Editor de forma desatendida y preaprovisionar la licencia mediante el Registro de Windows. Instala primero y, después, registra la licencia; debe estar configurada antes de iniciar la aplicación por primera vez.

### Instalar en modo silencioso

Sin interfaz de usuario ni reinicio:

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart /l*v C:\Temp\TE3_install.log
```

| Característica de MSI | Se muestra en el instalador como | Descripción                                     | Activar la instalación                                      |
| --------------------- | -------------------------------- | ----------------------------------------------- | ----------------------------------------------------------- |
| `MainFeature`         | Tabular Editor 3                 | Aplicación principal de Tabular Editor 3        | Sí (obligatorio)                         |
| `AIAssistant`         | Funciones de IA                  | El @ai-assistant y el servidor MCP | Sí, desde la versión 3.27.0 |

> [!IMPORTANT]
> El comando anterior instala el componente **Funciones de IA**. Hasta la versión 3.26.x había que seleccionarlo explícitamente y una instalación predeterminada lo dejaba fuera; desde la versión 3.27.0 forma parte de la instalación predeterminada. Si tu organización no quiere el Asistente de IA ni el servidor MCP en los equipos de los usuarios, tienes que indicarlo explícitamente, como se describe en la siguiente sección.

### Desplegar sin las funciones de IA

Para evitar que los archivos de IA se copien en el equipo, indica las características que quieres y omite `AIAssistant`:

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart ADDLOCAL=MainFeature /l*v C:\Temp\TE3_install.log
```

Para quitar el componente de los equipos que ya lo tienen, ejecuta el mismo paquete con `REMOVE`:

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart REMOVE=AIAssistant /l*v C:\Temp\TE3_install.log
```

En cualquiera de los dos casos, los ensamblados de IA nunca se copian en la carpeta de instalación, el panel **Asistente de IA** y el servidor MCP no aparecen en la aplicación, y nada se conecta a un proveedor de modelos. El resto de Tabular Editor 3 no se ve afectado.

Al actualizar una instalación existente, se conserva la selección de características que ya tiene ese equipo, por lo que un equipo que se implementó sin las funciones de IA antes de la versión 3.27.0 no las obtiene por el mero hecho de actualizarse. Usa `ADDLOCAL=MainFeature` en instalaciones nuevas, en las que no hay ninguna selección anterior que heredar.

> [!IMPORTANT]
> La línea de comandos controla lo que _tú_ implementas, no lo que un usuario puede instalar: las funciones de IA son la opción predeterminada, así que cualquiera que ejecute el instalador por su cuenta las instalará. Para que la decisión se mantenga, configura también la directiva `DisableAi` en @policies. A partir de la versión 3.27.0, el instalador lee esa directiva y excluye automáticamente el componente de IA, sin importar quién lo ejecute ni cómo se ejecute. Además, la directiva desactiva en tiempo de ejecución el Asistente de IA y el servidor MCP si el componente ya está presente. Configúrala a nivel de equipo, en `HKEY_LOCAL_MACHINE\Software\Policies\Tabular Editor ApS\TE3`, para que se aplique a todos los usuarios y no pueda sobrescribirse a nivel de usuario.

> [!NOTE]
> Al usar `ADDLOCAL`, incluye `MainFeature` junto con cualquier característica opcional. Si especificas solo `AIAssistant` sin `MainFeature`, la instalación quedará incompleta.

### Nombres de paquetes y otras opciones de MSI

También puedes usar `/package` en lugar de `/i`. Reemplaza `<version>` por la cadena de versión real.

Los paquetes MSI se denominan `TabularEditor.<version>.<architecture>.<runtime>.msi`, por ejemplo, `TabularEditor.3.27.0.x64.Net10.msi` o `TabularEditor.3.27.0.ARM64.Net8.msi`. Elige la arquitectura y el runtime que mejor se adapten a los equipos de destino; consulta @system-requirements. El MSI no instala el .NET Desktop Runtime, así que instálalo primero.

Para obtener información detallada sobre las opciones de línea de comandos de MSI disponibles, consulta la documentación oficial de Microsoft:
[Opciones de la línea de comandos de Microsoft Standard Installer - aplicaciones Win32 | Microsoft Learn](https://learn.microsoft.com/windows/win32/msi/command-line-options)

### Aprovisionar previamente la licencia

Escribe la licencia en el Registro _antes del primer inicio_ de la aplicación:

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

