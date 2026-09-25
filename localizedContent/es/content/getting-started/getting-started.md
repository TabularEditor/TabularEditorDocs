---
uid: getting-started
title: Instalación y activación
author: Morten Lønskov
updated: 2026-09-14
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

# Instalación y activación

## Instalación

Descarga la versión más reciente de Tabular Editor 3 desde nuestra [página de descargas](xref:downloads).

Recomendamos el instalador `.exe` de 64 bits para .NET 10 en la mayoría de los escenarios. Una vez descargado, haz doble clic y completa las pantallas del instalador.

![Instalar](~/content/assets/images/getting-started/install.png)

### Requisitos previos

Para el instalador `.exe`, el **.NET Desktop Runtime** correspondiente: [10](https://dotnet.microsoft.com/download/dotnet/10.0) para la versión recomendada o [8](https://dotnet.microsoft.com/download/dotnet/8.0) para la versión de .NET 8. El instalador te ofrece descargarlo e instalarlo, así que en la práctica no tienes que hacer nada de antemano.

Los otros dos paquetes son diferentes. El `.msi` no incluye el runtime, así que instálalo tú mismo al implementar de forma centralizada; el `.zip` portátil es autónomo y no necesita runtime.

### Requisitos del sistema

- **Sistema operativo:** Windows 10, Windows 11, Windows Server 2016, Windows Server 2019 o versiones posteriores
- **Arquitectura:** x64, ARM64 (nativo desde la versión 3.23.0)
- **Runtime de .NET:** .NET Desktop Runtime 10 u 8, según la compilación que instales

Consulta @system-requirements para ver la matriz completa y cómo elegir entre las compilaciones.

## Activación de su instalación

Tabular Editor 3 es software comercial. Visita nuestra [página principal](https://tabulareditor.com) para conocer los precios y las opciones de compra. Si no has usado antes Tabular Editor 3, puedes acceder a una prueba gratuita de 30 días.

La primera vez que inicie Tabular Editor 3 en un equipo nuevo, se le pedirá que active el producto.

![Activación del producto](~/content/assets/images/getting-started/product-activation.png)

### Activación con una clave de licencia existente

Cuando compres una licencia de Tabular Editor 3, recibirás un correo electrónico con una cadena de 25 caracteres, que es tu clave de licencia. Cuando se te solicite, escribe la clave de licencia y haz clic en **Siguiente >** para activar el producto.

![Introducir clave de licencia](~/content/assets/images/getting-started/enter-license-key.png)

> [!NOTE]
> Para los tipos de licencia multiusuario, además de la clave de licencia también debes introducir tu dirección de correo electrónico. Tabular Editor 3 te lo solicitará cuando la clave de licencia corresponda a una licencia multiusuario.

Las instalaciones de Tabular Editor 3 se activan **por usuario**. Si varios usuarios comparten el mismo equipo, cada usuario debe activar el producto en su propio perfil de usuario de Windows.

### Cuenta de Windows vs. cuenta de Power BI / Entra

La cuenta de Windows en la que se instala Tabular Editor 3 es independiente de la cuenta de Microsoft Entra que se usa para autenticarse en un Workspace de Power BI / Fabric.

- La **activación de la licencia** se almacena en el Registro de Windows, en `HKEY_CURRENT_USER`, del usuario de Windows que activó el producto. La licencia no está vinculada a ninguna identidad en la nube.
- La **autenticación del Workspace** se realiza en el momento de la conexión, en el cuadro de diálogo **Cargar modelo semántico desde la base de datos**. Inicia sesión con la cuenta de Microsoft Entra que tenga permisos en el Workspace.

No necesitas iniciar Tabular Editor 3 con **Ejecutar como** usando otra cuenta de Windows solo porque uses una cuenta de Entra distinta (por ejemplo, una cuenta de administrador sin correo habilitado) para administrar el Workspace de Power BI. Inicia Tabular Editor 3 con tu cuenta habitual de Windows, actívalo con tu clave de licencia en esa cuenta y proporciona tus credenciales de administrador de Entra en el cuadro de diálogo de conexión.

Para obtener más información sobre cómo Tabular Editor se autentica en el punto de conexión XMLA y cómo elegir el modo de autenticación correcto (por ejemplo, **Microsoft Entra MFA** cuando tu inicio de sesión de Windows no coincide con tu cuenta de Power BI), consulta @xmla-as-connectivity.

### Solicitar una licencia de prueba

Si no has usado antes Tabular Editor 3, puedes acceder a una prueba gratuita de 30 días. Al elegir esta opción, se te pedirá una dirección de correo electrónico. Usamos la dirección de correo electrónico para comprobar si ya tienes una activación previa de Tabular Editor 3.

> [!NOTE]
> Tabular Editor ApS no envía correos electrónicos no solicitados ni cede tu dirección de correo electrónico a terceros al registrarte para obtener una licencia de prueba de 30 días. Consulta nuestra @privacy-policy para obtener más información.

### Cambiar una clave de licencia

Una vez activado Tabular Editor 3, puedes cambiar la clave de licencia en el menú Ayuda seleccionando **Acerca de Tabular Editor**.

![Acerca de Te3](~/content/assets/images/getting-started/about-te3.png)

En el cuadro de diálogo, selecciona **Cambiar clave de licencia**. Esta opción solo está disponible cuando no hay ningún modelo cargado en Tabular Editor. Si hay un modelo abierto, ciérralo desde **Archivo > Cerrar modelo**. Al hacer clic en **Cambiar clave de licencia**, Tabular Editor te preguntará si quieres quitar la licencia actual:

![imagen](~/content/assets/images/getting-started-01.png)

Si aceptas, se quita la licencia actual y tendrás que volver a introducir una clave de licencia para usar el producto.

> [!IMPORTANT]
> Una vez eliminada una clave de licencia, el producto no puede ser utilizado por el usuario actual en ese equipo hasta que se introduzca una nueva clave de licencia.

## Configuración posterior a la instalación

Tabular Editor 3 ofrece muchas opciones de configuración. La configuración predeterminada es suficiente para la mayoría de los escenarios de desarrollo, pero revisa las opciones siguientes.

### Buscar actualizaciones al iniciar

De forma predeterminada, cada vez que se inicia Tabular Editor 3, la herramienta comprueba en línea si hay una versión más reciente disponible. Puedes controlar cómo se realiza esta comprobación de actualizaciones en **Herramientas > Preferencias > Actualizaciones y comentarios**.

> [!NOTE]
> Usa siempre la versión más reciente de Tabular Editor 3. Nuestro equipo de soporte asume que estás usando la versión más reciente antes de enviar un Report de errores.

### Desactivar la recopilación de telemetría

Tabular Editor 3 recopila datos de uso anónimos y telemetría, lo que nos ayuda a mejorar el producto. Puedes desactivarla en cualquier momento: inicia Tabular Editor 3 y ve a **Herramientas > Preferencias > Actualizaciones y comentarios**. Desmarca la casilla **Ayuda a mejorar Tabular Editor recopilando datos de uso anónimos** para dejar de participar.

![Recopilar telemetría](~/content/assets/images/getting-started/collect-telemetry.png)

### Configuración del proxy

Si estás en una red con conectividad limitada a Internet, especifica la dirección, el nombre de usuario y la contraseña de un servidor proxy en **Herramientas > Preferencias > Configuración de proxy**. Esto es necesario para que Tabular Editor 3 pueda usar cualquier característica que dependa de solicitudes web salientes. En concreto:

- Comprobaciones de actualizaciones
- Activación del producto
- Formato de DAX
- Descarga de reglas de prácticas recomendadas desde URL externas

> [!TIP]
> En ocasiones, la configuración de proxy puede interferir con los cuadros de diálogo de autenticación o con otros avisos externos. Prueba a cambiar la configuración de proxy entre **Sistema** y **Ninguno**; después, cierra y vuelve a abrir Tabular Editor 3 para comprobarlo.

### Otras preferencias

Tabular Editor 3 incluye muchas otras opciones para controlar el comportamiento de la aplicación. Para obtener más información, consulta @preferencias.

## Escenarios avanzados

Para la activación manual (sin conexión a Internet), la administración de licencias basada en el registro, la implementación silenciosa y la administración de puestos de Enterprise, consulta @installation-activation-basic.

## Próximos pasos

- [Información general sobre la interfaz de usuario de Tabular Editor 3](xref:user-interface)
- @xmla-as-connectivity
- @migrate-from-vs
- @migrate-from-desktop
- @migrate-from-te2
- @installation-activation-basic
