---
uid: connect-snowflake
title: Conectar con Snowflake
author: Morten Lønskov
updated: 2026-09-23
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

El conector de Snowflake se conecta a los Warehouses de datos de Snowflake y solo está disponible como un Data source implícito (consulta [Legacy, structured and implicit data sources](xref:connectivity#legacy-structured-and-implicit-data-sources)).

Selecciona **Modelo > Importar tablas...** y elige un origen de Snowflake para abrir el cuadro de diálogo.

![El cuadro de diálogo Conectar a Snowflake, con Navegador externo seleccionado en la lista Autenticador y los campos de nombre de usuario y contraseña deshabilitados](~/content/assets/images/features/connectivity/snowflake-connection.png)

## Campos de conexión

| Campo                                                                              | Descripción                                                                                                            |
| ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **Servidor**                                                                       | La dirección URL de tu cuenta de Snowflake. Obligatorio                                                |
| **Warehouse**                                                                      | El Warehouse en el que se ejecutarán las consultas. Obligatorio                                        |
| **Base de datos (opcional)**                                    | La base de datos desde la que se importará                                                                             |
| **Autenticador**                                                                   | La opción de autenticación. Consulta [Autenticación](#authentication)                                  |
| **Nombre de usuario**, **Contraseña** y **Archivo de clave privada**               | Las credenciales del método de autenticación seleccionado. Las etiquetas cambian según el autenticador |
| **Propiedades adicionales de la cadena de conexión (opcional)** | Configuración adicional de la cadena de conexión                                                                       |

## Autenticación

| Autenticación         | Qué debes proporcionar                                                                                                                    | Inicio de sesión interactivo |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- |
| **Snowflake**         | Nombre de usuario y contraseña                                                                                                            | No                           |
| **Navegador externo** | Un inicio de sesión en el navegador a través de tu proveedor de identidad                                                                 | Sí                           |
| **OAuth**             | Un token de acceso de OAuth de tu proveedor de OAuth, en el campo **Token**. Cuando el token caduque, introduce uno nuevo | No                           |
| **Par de claves**     | Nombre de usuario y un archivo de clave privada RSA, además de la frase de contraseña de la clave si está cifrada                         | No                           |

Tabular Editor guarda la configuración de conexión y las credenciales en tu archivo de opciones de usuario (consulta [Dónde se almacenan las credenciales](xref:connectivity#where-credentials-are-stored)).

## Autenticación mediante par de claves

Los usuarios de servicio de Snowflake (`TYPE = SERVICE`) no pueden iniciar sesión con una contraseña, así que usa **Par de claves** para ellos. Consulta [Planificación de la retirada de los inicios de sesión con contraseña de un solo factor](https://docs.snowflake.com/en/user-guide/security-mfa-rollout).

1. Selecciona **Key pair** en la lista **Authenticator**. El campo **Password** cambia a **Passphrase**.
2. Introduce tu nombre de usuario.
3. Busca y selecciona el archivo de tu clave privada.
4. Si la clave está cifrada, introduce su frase de contraseña.

El botón **OK** se habilita una vez que se han completado **Server**, **Warehouse**, **Username** y **Private key file**. El archivo de clave privada debe usar uno de estos formatos:

- sin cifrar PKCS#1
- sin cifrar PKCS#8
- cifrado con frase de contraseña PKCS#8, el formato que producen las [instrucciones de Snowflake para pares de claves](https://docs.snowflake.com/en/user-guide/key-pair-auth)

Cuando cambias entre **Key pair** y otro autenticador, se borra el campo **Password** o **Passphrase**. Tabular Editor guarda la ruta del archivo de clave privada solo mientras esté seleccionado **Par de claves**.

> [!IMPORTANT]
> No se admiten las claves cifradas con el esquema heredado de OpenSSL, que empiezan por `-----BEGIN RSA PRIVATE KEY-----` y llevan los encabezados `Proc-Type` y `DEK-Info`. Convierte esa clave a PKCS#8 cifrado:
>
> ```bash
> openssl pkcs8 -topk8 -v2 aes256 -in rsa_key.pem -out rsa_key.p8
> ```
>
> La conversión conserva el par de claves y la clave pública registrada en tu usuario de Snowflake sigue siendo válida.

<!-- IMAGE NEEDED: connectivity/snowflake-key-pair.png
     The Snowflake connection dialog with Key pair selected, so the Private key file field
     and its browse button are visible and the password field reads Passphrase.
     House border, 100% DPI.
     Alt text: "The Snowflake connection dialog with Key pair authentication selected" -->

## Inicios de sesión con navegador externo

Tabular Editor almacena en caché el inicio de sesión en el navegador. A partir de Tabular Editor 3.27.0, si Snowflake rechaza el inicio de sesión almacenado en caché, por ejemplo porque tu proveedor de identidades lo ha hecho caducar o lo ha revocado, Tabular Editor lo descarta y vuelve a abrir el inicio de sesión en el navegador. Si cierras el inicio de sesión en el navegador o se agota el tiempo de espera, la operación se cancela.
