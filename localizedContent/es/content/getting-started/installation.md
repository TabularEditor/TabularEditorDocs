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

Tabular Editor 3 usa el Registro de Windows para almacenar los detalles de activación.

Para ver la clave de licencia actual asignada al equipo, ejecuta el siguiente comando en el Símbolo del sistema de Windows (Inicio > Ejecutar > cmd.exe):

```cmd
REG QUERY "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey
```

También puedes usar `regedit.exe` (Editor del Registro de Windows) y navegar a `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3` para ver y modificar los valores **LicenseKey** y **User**.

![Editor del Registro](~/content/assets/images/troubleshooting/registry-editor.png)

Un administrador del sistema también puede asignar de forma proactiva licencias de Tabular Editor 3 a un equipo, especificando los valores **LicenseKey** y **User** en la clave del Registro `SOFTWARE\Kapacity\Tabular Editor 3` de cada usuario. Consulta [Instalación desatendida y aprovisionamiento previo de la licencia](#silent-installation-and-license-pre-provisioning) para ver el procedimiento completo de implementación.

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

## Instalación desatendida y aprovisionamiento previo de la licencia

Puedes implementar Tabular Editor de forma desatendida y aprovisionar previamente la licencia a través del Registro de Windows. Instala primero y, después, escribe la licencia, que debe estar establecida antes de que la aplicación se inicie por primera vez.

### Instalar en silencio

Sin interfaz de usuario, sin reinicio:

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart /l*v C:\Temp\TE3_install.log
```

| Característica MSI | Se muestra en el instalador como | Descripción                                     | Activar la instalación                                            |
| ------------------ | -------------------------------- | ----------------------------------------------- | ----------------------------------------------------------------- |
| `MainFeature`      | Tabular Editor 3                 | Aplicación principal de Tabular Editor 3        | Sí (obligatorio)                               |
| `AIAssistant`      | Funciones de IA                  | El @ai-assistant y el servidor MCP | Sí, a partir de la versión 3.27.0 |

> [!IMPORTANT]
> El comando anterior instala el componente de **funciones de IA**. Hasta la versión 3.26.x había que seleccionarlo explícitamente y una instalación predeterminada lo dejaba fuera; desde la versión 3.27.0 forma parte de la instalación predeterminada. Si tu organización no quiere el Asistente de IA ni el servidor MCP en los equipos de los usuarios, debes indicarlo explícitamente, como se describe en la siguiente sección.

### Desplegar sin las funciones de IA

Para que los archivos de IA no se instalen en el equipo, indica las características que quieras y omite `AIAssistant`:

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart ADDLOCAL=MainFeature /l*v C:\Temp\TE3_install.log
```

Para quitar el componente de los equipos que ya lo tienen, ejecuta el mismo paquete con `REMOVE`:

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart REMOVE=AIAssistant /l*v C:\Temp\TE3_install.log
```

En cualquier caso, los ensamblados de IA nunca se copian en la carpeta de instalación; el panel del **Asistente de IA** y el servidor MCP no aparecen en la aplicación y nada se conecta a un proveedor de modelos. Todo lo demás en Tabular Editor 3 permanece sin cambios.

Al actualizar una instalación existente, se conserva la selección de características que ya tenga ese equipo, por lo que un equipo desplegado sin las funciones de IA antes de la 3.27.0 no las adquiere al actualizarse. Usa `ADDLOCAL=MainFeature` en instalaciones nuevas, donde no hay ninguna selección previa que heredar.

> [!IMPORTANT]
> La línea de comandos controla lo que _tú_ despliegas, no lo que un usuario puede instalar: las funciones de IA son la opción predeterminada, así que cualquiera que ejecute el instalador por su cuenta las obtendrá. Para que esa decisión se mantenga, configura también las @policies `DisableAi`. Desde la versión 3.27.0, el instalador lee esa política y excluye automáticamente el componente de IA, independientemente de quién lo ejecute y de cómo se ejecute; además, la política también desactiva el Asistente de IA y el servidor MCP en tiempo de ejecución si el componente ya está presente. Configúralo a nivel de máquina, en `HKEY_LOCAL_MACHINE\Software\Policies\Tabular Editor ApS\TE3`, para que se aplique a todos los usuarios y no pueda sobrescribirse por usuario.

> [!NOTE]
> Cuando uses `ADDLOCAL`, incluye `MainFeature` en la lista junto con cualquier característica opcional. Si especificas solo `AIAssistant` sin `MainFeature`, la instalación quedará incompleta.

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

