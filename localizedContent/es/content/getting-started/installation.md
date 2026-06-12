---
uid: installation-activation-basic
title: Instalación, activación y configuración básica
author: Morten Lønskov
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

## Descripción general

Esta página abarca escenarios avanzados de instalación y activación de Tabular Editor 3: activación manual (sin conexión), administración de licencias mediante el Registro, despliegue desatendido y administración de asientos de la Edición Enterprise.

Para el flujo de activación estándar, consulta @getting-started.

<a name="manual-activation-no-internet"></a>

## Activación manual (sin Internet)

Si no tienes acceso a Internet, por ejemplo, debido a un proxy, Tabular Editor te pedirá que realices una activación manual.

![Activación del producto](~/content/assets/images/getting-started/product-activation.png)

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

<a name="registry-details"></a>

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

Puedes desplegar Tabular Editor de forma desatendida y preaprovisionar la licencia a través del Registro de Windows.

1. **Instalar en modo silencioso** (sin interfaz de usuario, sin reinicio):

   ```powershell
   msiexec /i TabularEditor.<version>.x64.Net8.msi /qn /norestart /l*v C:\Temp\TE3_install.log
   ```

   Para incluir la funcionalidad **AI Assistant**, especifica la propiedad `ADDLOCAL`. AI Assistant no se instala de forma predeterminada.

   ```powershell
   msiexec /i TabularEditor.<version>.x64.Net8.msi /qn /norestart ADDLOCAL=MainFeature,AIAssistant /l*v C:\Temp\TE3_install.log
   ```

   | Característica de MSI | Descripción                              | Activar la instalación              |
   | --------------------- | ---------------------------------------- | ----------------------------------- |
   | `MainFeature`         | Aplicación principal de Tabular Editor 3 | Sí (obligatorio) |
   | `AIAssistant`         | AI Assistant para Tabular Editor 3       | No                                  |

   > [!NOTE]> Al usar `ADDLOCAL`, incluye `MainFeature` junto con cualquier característica opcional. Si especificas solo `AIAssistant` sin `MainFeature`, la instalación quedará incompleta.

También puedes usar `/package` en lugar de `/i`. Reemplaza `<version>` por la cadena de versión real. Usa el MSI de ARM64 si corresponde.

Para obtener información detallada sobre las opciones de línea de comandos de MSI disponibles, consulta la documentación oficial de Microsoft:
[Opciones de la línea de comandos de Microsoft Standard Installer - aplicaciones Win32 | Microsoft Learn](https://learn.microsoft.com/windows/win32/msi/command-line-options)

2. **Escribe la licencia en el Registro** **antes de abrir la aplicación por primera vez**:

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

