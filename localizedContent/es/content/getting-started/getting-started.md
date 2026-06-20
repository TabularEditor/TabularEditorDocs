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

Recomendamos el instalador MSI de 64 bits para la mayoría de los casos. Una vez descargado, haz doble clic en el archivo MSI y completa las pantallas del instalador.

![Editor del Registro](~/content/assets/images/troubleshooting/registry-editor.png)

### Requisitos previos

Ninguno.

### Requisitos del sistema

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

### Cuenta de Windows vs. cuenta de Power BI / Entra

La cuenta de Windows en la que está instalado Tabular Editor 3 es independiente de la cuenta de Microsoft Entra que se usa para autenticarse en un Workspace de Power BI / Fabric.

- **La activación de la licencia** se almacena en el Registro de Windows, en `HKEY_CURRENT_USER`, del usuario de Windows que activó el producto. La licencia no está vinculada a ninguna identidad en la nube.
- **La autenticación del Workspace** se realiza al conectarte, en el cuadro de diálogo **Cargar modelo semántico desde la base de datos**. Inicias sesión con la cuenta de Microsoft Entra que tiene permisos en el Workspace.

No necesitas iniciar Tabular Editor 3 con **Ejecutar como** desde otra cuenta de Windows solo porque uses una cuenta de Entra distinta (por ejemplo, una cuenta de administrador no habilitada para correo) para administrar el Workspace de Power BI. Inicia Tabular Editor 3 con tu cuenta habitual de Windows, actívalo con tu clave de licencia en esa cuenta y proporciona tus credenciales de administrador de Entra en el cuadro de diálogo de conexión.

Para más información sobre cómo Tabular Editor se autentica en el punto de conexión XMLA y cómo elegir el modo de autenticación adecuado (por ejemplo, **Microsoft Entra MFA** cuando tu inicio de sesión de Windows no coincide con tu cuenta de Power BI), consulta @xmla-as-connectivity.

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

## Instalado de forma predeterminada

Tabular Editor 3 ofrece muchas opciones de configuración. La configuración predeterminada es suficiente para la mayoría de los escenarios de desarrollo, pero revisa las opciones siguientes.

### Buscar actualizaciones al iniciar

De forma predeterminada, cada vez que se inicia Tabular Editor 3, la herramienta comprueba en línea si hay una versión más reciente disponible. Puedes controlar cómo se realiza esta comprobación de actualizaciones en **Herramientas > Preferencias > Actualizaciones y comentarios**.

> Cierra todas las instancias de Tabular Editor 3. Nuestro equipo de soporte asume que estás en la versión más reciente antes de enviar un Report de error.

### Desactivar la recopilación de telemetría

Tabular Editor 3 recopila datos de uso anónimos y telemetría, lo que nos ayuda a mejorar el producto. Puedes desactivar esta recopilación en cualquier momento: inicia Tabular Editor 3 y ve a **Herramientas > Preferencias > Actualizaciones y comentarios**. Para desactivar esta recopilación, desmarca la casilla **Ayudar a mejorar Tabular Editor recopilando datos de uso anónimos**.

![Recopilar telemetría](~/content/assets/images/getting-started/collect-telemetry.png)

### Configuración del proxy

Si estás en una red con conectividad a Internet limitada, especifica la dirección, el nombre de usuario y la contraseña de un servidor proxy en **Herramientas > Preferencias > Configuración del proxy**. Esto es necesario para que Tabular Editor 3 pueda usar cualquier funcionalidad que dependa de solicitudes web salientes. En concreto:

- Comprobaciones de actualizaciones
- Si utilizas una clave de licencia de **Edición Enterprise**, establece también el correo electrónico del usuario con licencia:
- Formato de DAX
- Descarga de reglas de mejores prácticas desde direcciones URL externas

> [!TIP]
> A veces, la configuración del proxy puede interferir con los cuadros de diálogo de autenticación u otros avisos externos. Prueba a cambiar la configuración del proxy entre **System** y **None** y, a continuación, cierra y vuelve a abrir Tabular Editor 3 para comprobarlo.

### Otras preferencias

Tabular Editor 3 incluye muchos otros ajustes para controlar el comportamiento de la aplicación. Para obtener más información, consulta @preferences.

## Escenarios avanzados

Para la activación manual (sin conexión a Internet), la administración de licencias basada en el registro, la implementación desatendida y la administración de asientos de Enterprise, consulta @installation-activation-basic.

## Siguientes pasos

- [Información general sobre la interfaz de usuario de Tabular Editor 3](xref:user-interface)
- @xmla-as-connectivity
- @migrate-from-vs
- @migrate-from-desktop
- @migrate-from-te2
- Instalación silenciosa y aprovisionamiento previo de licencias
