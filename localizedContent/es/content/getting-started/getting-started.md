---
uid: getting-started
title: Instalación y activación
author: Morten Lønskov
updated: 2026-03-27
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

# Primeros pasos

## Instalación

Descarga la versión más reciente de Tabular Editor 3 desde nuestra [página de descargas](xref:downloads).

## Requisitos previos

Ninguno.

## Requisitos del sistema

- **Sistema operativo:** Windows 10, Windows 11, Windows Server 2016, Windows Server 2019 o versiones posteriores
- **Arquitectura:** x64, ARM64 (nativo a partir de 3.23.0)
- **Runtime de .NET:** [.NET Runtime de Escritorio 8.0](https://dotnet.microsoft.com/en-us/download/dotnet/8.0)

Consulta la directiva de sistemas operativos compatibles de .NET para ver qué versiones actuales de Windows admite cada entorno de ejecución.

## Activación de su instalación

Tabular Editor 3 es software comercial. Visita nuestra [página principal](https://tabulareditor.com) para conocer los precios y las opciones de compra. Si no ha usado Tabular Editor 3 previamente, puede optar a una prueba gratuita de 30 días.

La primera vez que inicie Tabular Editor 3 en un equipo nuevo, se le pedirá que active el producto.

![Activación del producto](~/content/assets/images/getting-started/product-activation.png)

### Activación con una clave de licencia existente

Una vez que compres una licencia de Tabular Editor 3, deberías recibir un correo electrónico con una cadena de 25 caracteres; esa es tu clave de licencia. Cuando se te solicite, introduce la clave de licencia y pulsa "Siguiente >" para activar el producto.

![Introducir clave de licencia](~/content/assets/images/getting-started/enter-license-key.png)

> [!NOTE]
> Para los tipos de licencia multiusuario, tendrás que introducir tu dirección de correo electrónico además de la clave de licencia. Tabular Editor 3 te lo solicitará si la clave de licencia que introduces corresponde a una licencia multiusuario.

Ten en cuenta que las instalaciones de Tabular Editor 3 se activan **por usuario**. En otras palabras, si varios usuarios comparten el mismo equipo, cada uno tendrá que activar el producto en su perfil de usuario de Windows.

### Solicitar una licencia de prueba

Si no ha usado Tabular Editor 3 antes, puede optar a una prueba gratuita de 30 días. Al elegir esta opción, se te solicitará una dirección de correo electrónico. Usamos la dirección de correo electrónico para validar si ya tienes una activación de Tabular Editor 3.

> [!NOTE]
> Al registrarse para obtener una licencia de prueba de 30 días, Tabular Editor ApS no le enviará correos electrónicos no solicitados ni reenviará su dirección de correo electrónico a terceros. Consulta nuestra @privacy-policy para obtener más información.

### Cambiar una clave de licencia

Cuando Tabular Editor 3 esté activado, puedes cambiar tu clave de licencia en el menú Ayuda seleccionando "Acerca de Tabular Editor".

![About Te3](~/content/assets/images/getting-started/about-te3.png)

En el cuadro de diálogo, selecciona "Cambiar clave de licencia". Ten en cuenta que esta opción solo está disponible si no hay ningún modelo cargado en Tabular Editor. Si ya has cargado un modelo, puedes cerrarlo desde Archivo > Cerrar modelo. Cuando hagas clic en "Cambiar clave de licencia", Tabular Editor te preguntará si quieres eliminar la licencia actual:

![imagen](https://user-images.githubusercontent.com/8976200/146754154-e691810b-342d-4311-8278-33da240d8d08.png)

Al aceptarlo, se quita la licencia actual y tendrás que volver a introducir una clave de licencia para usar el producto.

> [!IMPORTANT]
> Una vez que se quita una clave de licencia, tal como se describe arriba, el usuario actual no podrá usar el producto en ese equipo hasta que se introduzca una nueva clave de licencia.

<a name="registry-details"></a>

#### Detalles del registro

Tabular Editor 3 usa el Registro de Windows para almacenar los detalles de activación.

Para ver la clave de licencia actual asignada al equipo, ejecuta el siguiente comando en el Símbolo del sistema de Windows (Inicio > Ejecutar > cmd.exe):

```cmd
REG QUERY "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey
```

Un administrador del sistema también puede asignar por adelantado licencias de Tabular Editor 3 a un equipo, especificando los valores **LicenseKey** y **User** en la clave de registro `SOFTWARE\\Kapacity\\Tabular Editor 3` de cada usuario.

También puedes usar `regedit.exe` (Editor del Registro de Windows) y navegar a `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3` para ver y modificar los valores **LicenseKey** y **User**.

![Editor del Registro](~/content/assets/images/troubleshooting/registry-editor.png)

### Cambiar una clave de licencia mediante el Registro

Si por cualquier motivo no puedes cambiar la clave de licencia siguiendo el procedimiento descrito anteriormente, siempre puedes restablecer la licencia asignada a Tabular Editor 3 mediante el Editor del Registro:

1. Cierra todas las instancias de Tabular Editor 3.
2. Abre el Editor del Registro en Windows (Inicio > Ejecutar > regedit.msc).
3. Localiza `HKEY_CURRENT_USER\\SOFTWARE\\Kapacity\\Tabular Editor 3` (consulta la captura de pantalla anterior).
4. Elimina todos los valores dentro de esta clave.
5. Cierra el Editor del Registro y reinicia Tabular Editor 3.

Como alternativa, ejecuta el siguiente comando en el Símbolo del sistema de Windows (Inicio > Ejecutar > cmd.exe):

```cmd
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /va
```

La próxima vez que inicies Tabular Editor 3, se te pedirá una clave de licencia, igual que cuando la herramienta se instaló por primera vez en el equipo.

### Instalación silenciosa y aprovisionamiento previo de licencias

Puedes implementar Tabular Editor de forma silenciosa y aprovisionar previamente la licencia mediante el Registro de Windows.

1. **Instalar de forma silenciosa** (sin interfaz de usuario, sin reinicio):

   ```powershell
   msiexec /i TabularEditor.<version>.x64.Net8.msi /qn /norestart /l*v C:\Temp\TE3_install.log
   ```

   Para incluir la característica **Asistente de IA**, especifique la propiedad `ADDLOCAL`. El Asistente de IA no se instala de forma predeterminada.

   ```powershell
   msiexec /i TabularEditor.<version>.x64.Net8.msi /qn /norestart ADDLOCAL=MainFeature,AIAssistant /l*v C:\Temp\TE3_install.log
   ```

   | Característica de MSI | Descripción                              | Instalado de forma predeterminada   |
   | --------------------- | ---------------------------------------- | ----------------------------------- |
   | `MainFeature`         | Aplicación principal de Tabular Editor 3 | Sí (obligatorio) |
   | `AIAssistant`         | Asistente de IA para Tabular Editor 3    | No                                  |

   > [!NOTE]> When using `ADDLOCAL`, you must include `MainFeature` alongside any optional features. Especificar solo `AIAssistant` sin `MainFeature` da como resultado una instalación incompleta.

También puedes usar `/package` en lugar de `/i`. Sustituye `<version>` por la cadena de versión real. Usa el MSI de ARM64 si corresponde.

Para obtener más información sobre las opciones disponibles de la línea de comandos de MSI, consulte la documentación oficial de Microsoft:
[Opciones de línea de comandos de Microsoft Standard Installer - aplicaciones Win32 | Microsoft Learn](https://learn.microsoft.com/windows/win32/msi/command-line-options)

2. **Escribe la licencia en el Registro** **antes de la primera ejecución** de la aplicación:

   ```bat
   REM Clave de licencia por usuario (HKCU)
   REG ADD "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey /t REG_SZ /d YOUR-25-CHAR-KEY /f
   ```

   Si utilizas una clave de licencia de **Edición Enterprise**, establece también el correo electrónico del usuario con licencia:

   ```bat
   REG ADD "HKCU\Software\Kapacity\Tabular Editor 3" /v User /t REG_SZ /d user@example.com /f
   ```

**Notas**

- El instalador **no** acepta un parámetro de licencia; la gestión de licencias se realiza mediante las entradas del Registro indicadas arriba.
- Las claves se almacenan en **HKCU** (por usuario). Asegúrese de que los comandos se ejecuten en el contexto del usuario de destino (por ejemplo, mediante un script de inicio de sesión o similar) para que los valores se escriban en el perfil correcto.
- Para ver claves y valores adicionales, consulte los [detalles del Registro](#registry-details).

## Siguientes pasos

- [Información general sobre la interfaz de usuario de Tabular Editor 3](xref:user-interface)
