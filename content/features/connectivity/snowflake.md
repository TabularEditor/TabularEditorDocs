---
uid: connect-snowflake
title: Connect to Snowflake
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

# Connect to Snowflake

The Snowflake connector connects to Snowflake data warehouses and is available only as an implicit data source (see [Legacy, structured and implicit data sources](xref:connectivity#legacy-structured-and-implicit-data-sources)).

Select **Model > Import tables...** and choose a Snowflake source to open the dialog.

![The Connect to Snowflake dialog, with External browser selected in the Authenticator list and the user name and password fields disabled](~/content/assets/images/features/connectivity/snowflake-connection.png)

## Connection fields

| Field | Description |
| -- | -- |
| **Server** | Your Snowflake account URL. Required |
| **Warehouse** | The warehouse to run queries on. Required |
| **Database (optional)** | The database to import from |
| **Authenticator** | The authentication option. See [Authentication](#authentication) |
| **Username**, **Password** and **Private key file** | The credentials for the selected authenticator. The labels change with the authenticator |
| **Additional connection string properties (optional)** | Extra connection string settings |

## Authentication

| Authentication | What you supply | Interactive sign-in |
| -- | -- | -- |
| **Snowflake** | User name and password | No |
| **External browser** | A browser sign-in against your identity provider | Yes |
| **OAuth** | An OAuth access token from your OAuth provider, in the **Token** field. When the token expires, enter a new one | No |
| **Key pair** | User name and an RSA private key file, plus the key's passphrase if it's encrypted | No |

Tabular Editor saves the connection settings and credentials in your user options file (see [Where credentials are stored](xref:connectivity#where-credentials-are-stored)).

## Key pair authentication

Snowflake service users (`TYPE = SERVICE`) can't sign in with a password, so use **Key pair** for them. See [Planning for the deprecation of single-factor password sign-ins](https://docs.snowflake.com/en/user-guide/security-mfa-rollout).

1. Select **Key pair** in the **Authenticator** list. The **Password** field changes to **Passphrase**.
2. Enter your username.
3. Browse to your private key file.
4. If the key is encrypted, enter its passphrase.

**OK** is enabled once **Server**, **Warehouse**, **Username** and **Private key file** are filled in. The private key file must use one of these formats:

- unencrypted PKCS#1
- unencrypted PKCS#8
- passphrase-encrypted PKCS#8, the format [Snowflake's key-pair instructions](https://docs.snowflake.com/en/user-guide/key-pair-auth) produce

When you switch between **Key pair** and another authenticator, the **Password** or **Passphrase** field is cleared. Tabular Editor saves the private key file path only while **Key pair** is selected.

> [!IMPORTANT]
> Keys encrypted with the legacy OpenSSL scheme, which begin with `-----BEGIN RSA PRIVATE KEY-----` and carry `Proc-Type` and `DEK-Info` headers, aren't supported. Convert such a key to encrypted PKCS#8:
>
> ```bash
> openssl pkcs8 -topk8 -v2 aes256 -in rsa_key.pem -out rsa_key.p8
> ```
>
> Conversion keeps the key pair, and the public key registered on your Snowflake user stays valid.

<!-- IMAGE NEEDED: connectivity/snowflake-key-pair.png
     The Snowflake connection dialog with Key pair selected, so the Private key file field
     and its browse button are visible and the password field reads Passphrase.
     House border, 100% DPI.
     Alt text: "The Snowflake connection dialog with Key pair authentication selected" -->

## External browser sign-ins

Tabular Editor caches the browser sign-in. From Tabular Editor 3.27.0, if Snowflake rejects the cached sign-in, for example because your identity provider expired or revoked it, Tabular Editor discards it and opens the browser sign-in again. If you close the browser sign-in or it times out, the operation is canceled.
