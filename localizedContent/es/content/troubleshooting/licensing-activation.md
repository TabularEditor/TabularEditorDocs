---
uid: licensing-activation
title: Instalar y activar Tabular Editor 3
author: Daniel Otykier
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

# Tabular Editor 3

## Instalación

Descarga la versión más reciente de Tabular Editor 3 desde nuestra [página de descargas](xref:downloads).

## Requisitos previos

Ninguno.

## Requisitos del sistema

- **Sistema operativo:** Windows 7, Windows 8, Windows 10, Windows Server 2016, Windows Server 2019 o posterior
- **.NET Framework:** [4.7.2](https://dotnet.microsoft.com/download/dotnet-framework)

## Activación de la instalación

Tabular Editor 3 es software comercial. Visita nuestra [página principal](https://tabulareditor.com) para consultar precios y opciones de compra. Si no has usado Tabular Editor 3 anteriormente, puedes optar a una prueba gratuita de 30 días.

La primera vez que inicies Tabular Editor 3 en un equipo nuevo, se te pedirá que actives el producto.

![Activación del producto](~/content/assets/images/getting-started/product-activation.png)

### Activación con una clave de licencia existente

Una vez que compres una licencia de Tabular Editor 3, recibirás un correo electrónico con una cadena de 25 caracteres, que será tu clave de licencia. Cuando se te solicite, introduce la clave de licencia y pulsa "Siguiente >" para activar el producto.

![Introducir la clave de licencia](~/content/assets/images/getting-started/enter-license-key.png)

> [!NOTE]
> Para los tipos de licencia multiusuario, tendrás que introducir tu dirección de correo electrónico además de la clave de licencia. Tabular Editor 3 te lo solicitará si la clave de licencia que introduces corresponde a una licencia multiusuario.

#### Cambiar asientos en la Edición Enterprise

Para cambiar un asiento de Enterprise, primero hay que dar de baja al usuario actual del asiento a través del [portal de autoservicio de Tabular Editor](https://tabulareditor.com/my-account/). El propietario de la suscripción o el administrador de licencias puede crear una cuenta o iniciar sesión con una cuenta existente para administrar los asientos de la licencia.

> [!NOTE]
> Cambiar un usuario solo es posible en la Edición Enterprise.

### Solicitar una licencia de prueba

Si aún no has usado Tabular Editor 3, tienes derecho a una prueba gratuita de 30 días. Al elegir esta opción, se te pedirá una dirección de correo electrónico. Usamos la dirección de correo electrónico para validar si ya tienes una activación de Tabular Editor 3.

> [!NOTE]
> Tabular Editor ApS no enviará correos electrónicos no solicitados ni compartirá tu dirección de correo electrónico con terceros al registrarte para obtener una licencia de prueba de 30 días. Consulta nuestra @privacy-policy para obtener más información.

### Cambiar una clave de licencia

Cuando Tabular Editor 3 esté activado, puedes cambiar tu clave de licencia en el menú Ayuda seleccionando "Acerca de Tabular Editor".

![Acerca de Te3](~/content/assets/images/getting-started/about-te3.png)

En el cuadro de diálogo, selecciona "Cambiar clave de licencia". Ten en cuenta que esta opción solo está disponible si no hay ningún modelo cargado en Tabular Editor. Si ya has cargado un modelo, puedes cerrarlo en Archivo > Cerrar modelo.

#### Detalles del Registro de Windows

Tabular Editor 3 usa el Registro de Windows para almacenar los detalles de activación.

Para ver la clave de licencia actual asignada al equipo, ejecuta el siguiente comando en el Símbolo del sistema de Windows (Inicio > Ejecutar > cmd.exe):

```cmd
REG QUERY "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey
```

También puedes usar `regedit.exe` (Editor del Registro de Windows) y navegar a `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3` para ver y modificar los valores **LicenseKey** y **User**.

Un administrador del sistema también puede asignar de forma proactiva licencias de Tabular Editor 3 a un equipo especificando los valores **LicenseKey** y **User** en la clave del Registro `SOFTWARE\Kapacity\Tabular Editor 3` de cada usuario.

![Editor del Registro](~/content/assets/images/troubleshooting/registry-editor.png)

### Cambiar una clave de licencia a través del Registro de Windows

Si por cualquier motivo no puedes cambiar la clave de licencia mediante el procedimiento descrito anteriormente, siempre puedes restablecer la licencia asignada a Tabular Editor 3 mediante el Editor del Registro:

1. Cierra todas las instancias de Tabular Editor 3.
2. Abre el Editor del Registro en Windows (Inicio > Ejecutar > regedit.msc).
3. Busca `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3` (consulta la captura de pantalla anterior).
4. Elimina todos los valores de esta clave.
5. Cierra el Editor del Registro y reinicia Tabular Editor 3.

Como alternativa, ejecuta el siguiente comando en el Símbolo del sistema de Windows (Inicio > Ejecutar > cmd.exe):

```cmd
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /va
```

La próxima vez que inicies Tabular Editor 3, se te pedirá una clave de licencia, igual que cuando la herramienta se instaló por primera vez en el equipo.