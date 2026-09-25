---
uid: connect-snowflake
title: Connect to Snowflake
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

# Connect to Snowflake

Start from **Model > Import tables...** and choose a Snowflake source. Every authenticator needs the server (your account URL) and the warehouse.

![The Connect to Snowflake dialog, with External browser chosen in the Authenticator list and the user name and password fields disabled](~/content/assets/images/features/connectivity/snowflake-connection.png)

## Authenticators

| Authenticator        | What you supply                                                               | Reconnects unattended         |
| -------------------- | ----------------------------------------------------------------------------- | ----------------------------- |
| **Snowflake**        | User name and password                                                        | Sí                            |
| **External browser** | A browser sign-in against your identity provider                              | No                            |
| **OAuth**            | A token from your OAuth provider                                              | Yes, while the token is valid |
| **Key pair**         | User name and an RSA private key file, plus its passphrase if the key has one | Sí                            |

## Key pair authentication

Key pair is the authenticator to choose for unattended work now that Snowflake enforces multi-factor authentication for service accounts. It needs no interactive sign-in, so a saved connection reconnects on its own.

Choose **Key pair**, enter your user name and browse to your private key file. The password field is relabelled **Passphrase** while this authenticator is selected. **OK** stays disabled until the server, warehouse, user name and private key file are all filled in.

Supported key formats are unencrypted PKCS#1 and PKCS#8, and passphrase-encrypted PKCS#8, which is what [Snowflake's own key-pair instructions](https://docs.snowflake.com/en/user-guide/key-pair-auth) produce.

> [!IMPORTANT]
> A key encrypted with the legacy OpenSSL scheme is not supported. These begin `-----BEGIN RSA PRIVATE KEY-----` and carry `Proc-Type` and `DEK-Info` headers. Convert it with a single `openssl pkcs8 -topk8` command. This does not require generating a new key pair, so the public key already registered on your Snowflake user stays valid.

<!-- IMAGE NEEDED: connectivity/snowflake-key-pair.png
     The Snowflake connection dialog with Key pair selected, so the Private key file field
     and its browse button are visible and the password field reads Passphrase.
     House border, 100% DPI.
     Alt text: "The Snowflake connection dialog with Key pair authentication selected" -->

## External browser sign-ins

A browser sign-in is cached so you are not prompted for every operation. From Tabular Editor 3.27.0, a cached sign-in that your identity provider has expired or revoked no longer blocks the connection: Tabular Editor discards it as soon as Snowflake rejects it and reopens the browser sign-in.

Previously every later operation failed without reopening the browser, the wizard showed empty tables and columns instead of an error, and the only recovery was restarting Tabular Editor. A sign-in you abandon, or that times out, now counts as a cancellation rather than an error that blocks later work.

## Switching authenticator

Switching back to **Snowflake** clears the private key path and the passphrase rather than carrying the passphrase over as an account password.

## Where the credentials are stored

Credentials you enter here are saved per user and per model in the [user options](xref:user-options) file (`.tmuo`) beside the model, encrypted so that only your Windows account can read them. They are not part of the model metadata, so they are not committed to source control and a colleague opening the same model supplies their own.

The generated M expression names the server and the object only. It never contains a password, a token or a key.
