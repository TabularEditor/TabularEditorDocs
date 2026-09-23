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

Ve a **Modelo > Importar tablas...** y selecciona Snowflake como origen. Cada autenticador necesita el servidor (la URL de tu cuenta) y el Warehouse.

![El cuadro de diálogo Conectar con Snowflake, con Navegador externo seleccionado en la lista de autenticadores y los campos de nombre de usuario y contraseña deshabilitados](~/content/assets/images/features/connectivity/snowflake-connection.png)

## Autenticadores

| Autenticador          | Lo que proporcionas                                                                                        | Se reconecta sin intervención    |
| --------------------- | ---------------------------------------------------------------------------------------------------------- | -------------------------------- |
| **Snowflake**         | Nombre de usuario y contraseña                                                                             | Sí                               |
| **Navegador externo** | Inicio de sesión en el navegador a través de tu proveedor de identidad                                     | No                               |
| **OAuth**             | Un token de tu proveedor de OAuth                                                                          | Sí, mientras el token sea válido |
| **Par de claves**     | Nombre de usuario y un archivo de clave privada RSA, además de tu frase de contraseña si la clave la tiene | Sí                               |

## Autenticación con par de claves

El par de claves es el método de autenticación que debes elegir para el trabajo desatendido ahora que Snowflake exige autenticación multifactor para las cuentas de servicio. No requiere un inicio de sesión interactivo, por lo que una conexión guardada se vuelve a conectar por sí sola.

Elige **Par de claves**, introduce tu nombre de usuario y selecciona el archivo de tu clave privada. El campo de contraseña pasa a llamarse **Frase de paso** mientras este autenticador esté seleccionado. **OK** permanece deshabilitado hasta que se completen el servidor, el Warehouse, el nombre de usuario y el archivo de la clave privada.

Los formatos de clave admitidos son PKCS#1 y PKCS#8 sin cifrar, y PKCS#8 cifrado con frase de paso, que es el formato que generan [las propias instrucciones de Snowflake para la autenticación con par de claves](https://docs.snowflake.com/en/user-guide/key-pair-auth).

> [!IMPORTANT]
> No se admite una clave cifrada con el esquema heredado de OpenSSL. Empiezan por `-----BEGIN RSA PRIVATE KEY-----` y llevan encabezados `Proc-Type` y `DEK-Info`. Conviértela con un único comando `openssl pkcs8 -topk8`. Esto no requiere generar un nuevo par de claves, por lo que la clave pública ya registrada para tu usuario de Snowflake sigue siendo válida.

<!-- IMAGE NEEDED: connectivity/snowflake-key-pair.png
     The Snowflake connection dialog with Key pair selected, so the Private key file field
     and its browse button are visible and the password field reads Passphrase.
     House border, 100% DPI.
     Alt text: "The Snowflake connection dialog with Key pair authentication selected" -->

## Inicios de sesión con navegador externo

El inicio de sesión en el navegador se guarda en caché para que no se te pida en cada operación. A partir de Tabular Editor 3.27.0, un inicio de sesión en caché que tu proveedor de identidad haya caducado o revocado ya no bloquea la conexión: Tabular Editor lo descarta en cuanto Snowflake lo rechaza y vuelve a abrir el inicio de sesión en el navegador.

Antes, cualquier operación posterior fallaba sin volver a abrir el navegador, el asistente mostraba tablas y columnas vacías en lugar de un error, y la única forma de solucionarlo era reiniciar Tabular Editor. Ahora, un inicio de sesión que abandones o que caduque por tiempo de espera cuenta como una cancelación en lugar de como un error que bloquee el trabajo posterior.

## Cambio de autenticador

Al volver a **Snowflake**, se borran la ruta de la clave privada y la frase de contraseña, en lugar de reutilizar la frase de contraseña como contraseña de la cuenta.

## Dónde se almacenan las credenciales

Las credenciales que introduzcas aquí se guardan por usuario y por modelo en el archivo de [opciones de usuario](xref:user-options) (`.tmuo`) junto al modelo, cifradas para que solo tu cuenta de Windows pueda leerlas. No forman parte de los metadatos del modelo, por lo que no se incluyen en el control de versiones, y un compañero que abra el mismo modelo proporcionará las suyas.

La expresión M generada solo nombra el servidor y el objeto. Nunca contiene una contraseña, un token ni una clave.
