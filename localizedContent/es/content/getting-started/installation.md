---
uid: installation-activation-basic
title: Instalación y activación avanzadas
author: Morten Lønskov
updated: 2026-05-19
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

## Información general

En esta página se tratan escenarios avanzados de instalación y activación para Tabular Editor 3: activación manual (sin conexión), administración de licencias basada en el Registro, implementación silenciosa y administración de asientos de la edición Enterprise.

Para el flujo de activación estándar, consulta @getting-started.

<a name="manual-activation-no-internet"></a>

## Activación manual (sin Internet)

Si no tienes acceso a Internet, por ejemplo, por un proxy, Tabular Editor te solicitará que realices una activación manual.

![Mensaje de activación manual](~/content/assets/images/getting-started/Activation_manual_firstprompt.png)

Después de introducir tu correo electrónico, aparece un cuadro de diálogo con un enlace a una clave de activación. Copia la URL y ábrela en un navegador web que tenga conexión a Internet.

La URL devuelve un objeto JSON:

![Objeto JSON de activación manual](~/content/assets/images/getting-started/activation_manual_jsonobject.png)

Copia el objeto JSON completo y pégalo en el cuadro de diálogo. El cuadro de diálogo de activación manual se verá como en la captura de pantalla siguiente.

![Activación manual completada](~/content/assets/images/getting-started/activation_manual_dialogbox_filled.png)

A continuación, se verifica tu licencia de Tabular Editor 3.

## Cambiar asientos en la Edición Enterprise

Para cambiar un asiento de la edición Enterprise, anula el registro del usuario actual de ese asiento a través del [portal de autoservicio de Tabular Editor](https://tabulareditor.com/my-account/). El propietario de la suscripción o el administrador de licencias crea una cuenta o inicia sesión con una existente para administrar los asientos de licencia.

> [!NOTE]
> Cambiar de usuario solo es posible en la Edición Enterprise.

<a name="registry-details"></a>

## Detalles del Registro

Tabular Editor 3 usa el Registro de Windows para almacenar los datos de activación.

Para ver la clave de licencia actual asignada al equipo, ejecuta el siguiente comando en el Símbolo del sistema de Windows (Inicio > Ejecutar > cmd.exe):

```cmd
REG QUERY "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey
```

También puedes usar `regedit.exe` (Editor del Registro de Windows) y navegar hasta `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3` para ver y modificar los valores **LicenseKey** y **User**.

![Editor del Registro](~/content/assets/images/troubleshooting/registry-editor.png)

Un administrador del sistema también puede asignar de forma proactiva licencias de Tabular Editor 3 a un equipo especificando los valores **LicenseKey** y **User** en la clave del registro `SOFTWARE\Kapacity\Tabular Editor 3` de cada usuario. Consulta [Instalación desatendida y preaprovisionamiento de licencias](#instalacion-desatendida-y-preaprovisionamiento-de-licencias) para ver el procedimiento de implementación completo.

## Cambiar una clave de licencia a través del Registro

Si, por cualquier motivo, no puedes cambiar la clave de licencia mediante la opción estándar **Cambiar clave de licencia** del cuadro de diálogo **Acerca de Tabular Editor**, restablece la licencia desde el Editor del Registro:

1. Cierra todas las instancias de Tabular Editor 3.
2. Abre el Editor del Registro en Windows (Inicio > Ejecutar > regedit.msc).
3. Busca `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3` (consulta la captura de pantalla anterior).
4. Elimina todos los valores dentro de esta clave.
5. Cierra el Editor del Registro y reinicia Tabular Editor 3.

Como alternativa, ejecuta el siguiente comando en el Símbolo del sistema de Windows (Inicio > Ejecutar > cmd.exe):

```cmd
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /va
```

La próxima vez que inicies Tabular Editor 3, se te solicitará una clave de licencia, igual que cuando la herramienta se instaló por primera vez en el equipo.

## Instalación desatendida y preaprovisionamiento de licencias

Puedes implementar Tabular Editor de forma desatendida y preaprovisionar la licencia mediante el Registro de Windows.

1. **Instalar de forma silenciosa** (sin interfaz de usuario, sin reinicio):

   ```powershell
   msiexec /i TabularEditor.<version>.x64.Net8.msi /qn /norestart /l*v C:\Temp\TE3_install.log
   ```

   Para incluir la característica **Asistente de IA**, especifica la propiedad `ADDLOCAL`. El Asistente de IA no se instala de forma predeterminada.

   ```powershell
   msiexec /i TabularEditor.<version>.x64.Net8.msi /qn /norestart ADDLOCAL=MainFeature,AIAssistant /l*v C:\Temp\TE3_install.log
   ```

   | Característica MSI | Descripción                           | Instalado de forma predeterminada   |
   | ------------------ | ------------------------------------- | ----------------------------------- |
   | `MainFeature`      | Aplicación base de Tabular Editor 3   | Sí (obligatorio) |
   | `AIAssistant`      | Asistente de IA para Tabular Editor 3 | No                                  |

   > [!NOTE]> Al usar `ADDLOCAL`, incluye `MainFeature` junto con cualquier característica opcional. Si especificas solo `AIAssistant` sin `MainFeature`, la instalación quedará incompleta.

También puedes usar `/package` en lugar de `/i`. Reemplaza `<version>` por la cadena de la versión real. Usa el MSI de ARM64 si corresponde.

Para obtener más información sobre las opciones de línea de comandos de MSI disponibles, consulta la documentación oficial de Microsoft:
[Opciones de línea de comandos de Microsoft Standard Installer: aplicaciones Win32 | Microsoft Learn](https://learn.microsoft.com/windows/win32/msi/command-line-options)

2. **Escribe la licencia en el Registro** **antes de iniciar la aplicación por primera vez**:

   ```bat
   REM Per-user license key (HKCU)
   REG ADD "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey /t REG_SZ /d YOUR-25-CHAR-KEY /f
   ```

   Si usas una clave de licencia de la **Edición Enterprise**, establece también el correo electrónico del usuario con licencia:

   ```bat
   REG ADD "HKCU\Software\Kapacity\Tabular Editor 3" /v User /t REG_SZ /d user@example.com /f
   ```

**Notas**

- El instalador no acepta un parámetro de licencia; la licencia se administra mediante las entradas del Registro indicadas arriba.
- Las claves se almacenan en **HKCU** (por usuario). Asegúrate de que los comandos se ejecuten en el contexto del usuario de destino (por ejemplo, mediante un script de inicio de sesión) para que los valores se escriban en el perfil correcto.
- Para ver más claves y valores, consulta [detalles del Registro](#registry-details).

