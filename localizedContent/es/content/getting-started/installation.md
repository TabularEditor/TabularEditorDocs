---
uid: installation-activation-basic
title: Instalación, activación y configuración básica
author: Daniel Otykier
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

## Instalación

Para instalar Tabular Editor 3, descarga la versión más reciente desde nuestra [página de descargas](xref:downloads).

Recomendamos descargar el instalador MSI de 64 bits, que es adecuado para la mayoría de los casos. Una vez descargado, haz doble clic en el archivo MSI y sigue los pasos del asistente de instalación.

![Instalar](~/content/assets/images/getting-started/install.png)

## Activar la instalación

La primera vez que inicias Tabular Editor 3 en un equipo nuevo, se te pedirá que actives el producto.

![Activación del producto](~/content/assets/images/getting-started/product-activation.png)

### Activación con una clave de licencia existente

Una vez que compres una licencia de Tabular Editor 3, deberías recibir un correo electrónico con una cadena de 25 caracteres; esa es tu clave de licencia. Cuando se te solicite, introduce la clave de licencia y haz clic en "Siguiente >" para activar el producto.

![Introducir clave de licencia](~/content/assets/images/getting-started/enter-license-key.png)

> [!NOTE]
> Para los tipos de licencia para varios usuarios, tendrás que introducir tu dirección de correo electrónico además de la clave de licencia. Tabular Editor 3 te lo solicitará si la clave de licencia que introduces corresponde a una licencia multiusuario.

<a name="manual-activation-no-internet"></a>

#### Activación manual (sin Internet)

Si no tienes acceso a Internet, por ejemplo, debido a un proxy, Tabular Editor te pedirá que realices una activación manual.

![Aviso de activación manual](~/content/assets/images/getting-started/Activation_manual_firstprompt.png)

Después de introducir tu correo electrónico, aparece un cuadro de diálogo con un enlace a una clave de activación.
Copia la URL y ábrela en un navegador web conectado a Internet.

La URL devuelve un objeto JSON:

![Objeto JSON de activación manual](~/content/assets/images/getting-started/activation_manual_jsonobject.png)

Copia el objeto JSON completo y pégalo en el cuadro de diálogo.
El cuadro de diálogo de activación manual debería quedar como el que se muestra a continuación.

![Activación manual completada](~/content/assets/images/getting-started/activation_manual_dialogbox_filled.png)

De este modo, se verificará tu licencia de Tabular Editor 3.

### Cambiar una clave de licencia

Cuando Tabular Editor 3 está activado, puedes cambiar la clave de licencia en el menú Ayuda seleccionando "Acerca de Tabular Editor".

![Acerca de Te3](~/content/assets/images/getting-started/about-te3.png)

En el cuadro de diálogo, selecciona "Cambiar clave de licencia". Ten en cuenta que esta opción solo está disponible si no hay ningún modelo cargado en Tabular Editor. Si ya has cargado un modelo, puedes cerrarlo en Archivo > Cerrar modelo.

Para obtener más detalles sobre la administración de las claves de licencia, consulta [Detalles del registro](xref:getting-started#registry-details).

## Configuración básica

Después de activar Tabular Editor 3, te recomendamos dedicar unos minutos a familiarizarte con la [interfaz básica](xref:user-interface). Además, Tabular Editor 3 ofrece muchas opciones de configuración. La configuración predeterminada es suficiente para la mayoría de los escenarios de desarrollo, pero hay algunas opciones de configuración importantes que deberías revisar siempre.

### Buscar actualizaciones al iniciar

De forma predeterminada, cada vez que inicias Tabular Editor 3, la herramienta comprueba en línea si hay una versión más reciente disponible. Puedes controlar cómo se realiza esta comprobación de actualizaciones en **Herramientas > Preferencias > Actualizaciones y comentarios**.

> [!NOTE]
> Recomendamos usar siempre la versión más reciente de Tabular Editor 3. Por lo general, nuestro equipo de soporte asumirá que siempre estás usando la versión más reciente antes de enviar un Report de errores.

### No participar en la recopilación de telemetría

Tabular Editor 3 recopila datos de uso anónimos y telemetría, lo que nos ayuda a mejorar el producto. Puedes optar por no participar en cualquier momento: abre Tabular Editor 3 y ve a **Herramientas > Preferencias > Actualizaciones y comentarios**. Desmarca la casilla **Ayuda a mejorar Tabular Editor recopilando datos de uso anónimos** para no participar.

![Recopilar telemetría](~/content/assets/images/getting-started/collect-telemetry.png)

### Configuración del proxy

Si estás en una red con conectividad a Internet limitada, puedes especificar la dirección, el nombre de usuario y la contraseña de un servidor proxy en **Herramientas > Preferencias > Configuración del proxy**. Esto es necesario antes de que Tabular Editor 3 pueda usar cualquier función que dependa de solicitudes web salientes. En concreto, son:

- Comprobación de actualizaciones
- Activación del producto
- Formato de DAX
- Descarga de reglas de prácticas recomendadas desde URL externas

> [!TIP]
> En ocasiones, la configuración del proxy puede interferir con los cuadros de diálogo de autenticación u otras indicaciones externas.
> Intenta cambiar la configuración del proxy entre "Sistema" y "Ninguno"; cierra y vuelve a abrir Tabular Editor 3 para comprobarlo.

### Otras preferencias

Además de la configuración mencionada anteriormente, Tabular Editor 3 incluye muchas otras opciones para controlar distintos comportamientos de la aplicación, lo que te permite ajustar la herramienta a tus necesidades. Para obtener más información sobre estas otras preferencias, consulta @preferences.

## Siguientes pasos

- @migrate-from-vs
- @migrate-from-desktop
- @migrate-from-te2