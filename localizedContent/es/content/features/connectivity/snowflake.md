---
uid: connect-snowflake
title: Conectar con Snowflake
author: Morten Lønskov
updated: 2026-09-21
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

# Conectar con Snowflake

Empieza en **Modelo > Importar tablas...** y elige Snowflake como origen. En todos los casos, necesitas el servidor (la URL de tu cuenta) y el Warehouse.

![El cuadro de diálogo Conectar con Snowflake, con Navegador externo seleccionado en la lista de autenticadores y los campos de nombre de usuario y contraseña deshabilitados](~/content/assets/images/features/connectivity/snowflake-connection.png)

## Autenticadores

| Autenticador          | Qué debes proporcionar                                                                                | Se reconecta sin intervención    |
| --------------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------- |
| **Snowflake**         | Nombre de usuario y contraseña                                                                        | Sí                               |
| **Navegador externo** | Un inicio de sesión en el navegador a través de tu proveedor de identidad                             | No                               |
| **OAuth**             | Un token de tu proveedor de OAuth                                                                     | Sí, mientras el token sea válido |
| **Par de claves**     | Nombre de usuario y un archivo de clave privada RSA, además de su frase de paso, si la clave la tiene | Sí                               |

## Autenticación mediante par de claves

El autenticador **Par de claves** es la opción recomendada para el trabajo desatendido, ahora que Snowflake exige autenticación multifactor para las cuentas de servicio. No requiere inicio de sesión interactivo, así que una conexión guardada se vuelve a conectar por sí sola.

Elige **Par de claves**, introduce tu nombre de usuario y selecciona el archivo de tu clave privada. Mientras este autenticador esté seleccionado, el campo **Contraseña** pasa a llamarse **Frase de contraseña**. **OK** sigue deshabilitado hasta que se hayan completado el servidor, el Warehouse, el nombre de usuario y el archivo de la clave privada.

Los formatos de clave compatibles son PKCS#1 y PKCS#8 sin cifrar, y PKCS#8 cifrado con frase de contraseña; este es el formato que generan las [instrucciones de Snowflake sobre autenticación mediante par de claves](https://docs.snowflake.com/en/user-guide/key-pair-auth).

> [!IMPORTANT]
> No se admite una clave cifrada con el esquema heredado de OpenSSL. Estas empiezan por `-----BEGIN RSA PRIVATE KEY-----` y llevan los encabezados `Proc-Type` y `DEK-Info`. Conviértela con un único comando `openssl pkcs8 -topk8`. Esto no requiere generar un nuevo par de claves, así que la clave pública ya registrada en tu usuario de Snowflake sigue siendo válida.

<!-- IMAGE NEEDED: connectivity/snowflake-key-pair.png
     The Snowflake connection dialog with Key pair selected, so the Private key file field
     and its browse button are visible and the password field reads Passphrase.
     House border, 100% DPI.
     Alt text: "The Snowflake connection dialog with Key pair authentication selected" -->

## Inicios de sesión con navegador externo

El inicio de sesión en el navegador se almacena en caché para que no se te pida en cada operación. A partir de Tabular Editor 3.27.0, un inicio de sesión almacenado en caché que haya caducado o que tu proveedor de identidades haya revocado ya no bloquea la conexión: Tabular Editor lo descarta en cuanto Snowflake lo rechaza y vuelve a abrir el inicio de sesión en el navegador.

Antes, todas las operaciones posteriores fallaban a menos que se volviera a abrir el navegador; el asistente mostraba tablas y columnas vacías en lugar de un error, y la única forma de solucionarlo era reiniciar Tabular Editor. Un inicio de sesión que abandones, o que caduque por tiempo de espera, ahora cuenta como una cancelación en lugar de como un error que bloquea el trabajo posterior.

## Cambiar de autenticador

Al volver a **Snowflake**, se borran la ruta de la clave privada y la frase de contraseña, en lugar de reutilizar la frase de contraseña como contraseña de la cuenta.

## Dónde se almacenan las credenciales

Las credenciales que escribes aquí se guardan por usuario y por modelo en el archivo de [opciones de usuario](xref:user-options) (`.tmuo`) junto al modelo, cifradas para que solo tu cuenta de Windows pueda leerlas. No forman parte de los metadatos del modelo, así que no se registran en el control de código fuente y cualquier compañero que abra el mismo modelo usará las suyas.

La expresión M generada solo especifica el servidor y el objeto. Nunca contiene una contraseña, un token ni una clave.
