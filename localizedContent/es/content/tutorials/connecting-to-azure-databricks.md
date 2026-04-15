---
uid: connecting-to-azure-databricks
title: Conexión a Azure Databricks
author: David Bojsen
updated: 2026-04-08
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.15.0
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# (Tutorial) Conexión a Azure Databricks

Tabular Editor 3 te permite conectarte a Azure Databricks como Data source para tus modelos semánticos. Este tutorial te guiará por el proceso de configurar una conexión a Azure Databricks e importar datos desde Databricks.

## Requisitos previos

Antes de empezar, asegúrate de tener lo siguiente:

- Un Workspace válido de Azure Databricks
- Permisos adecuados para acceder a los datos de Databricks
- Tabular Editor 3 (edición Desktop, Business o Edición Enterprise)
- The [Databricks ODBC Driver](https://www.databricks.com/spark/odbc-drivers-download) installed on your machine

> [!IMPORTANT]
> Databricks has released a new ODBC driver that replaces the legacy Simba Spark ODBC Driver. We recommend installing the new [Databricks ODBC Driver](https://www.databricks.com/spark/odbc-drivers-download). Tabular Editor 3.26.0 and later supports both drivers, but the new driver is the recommended option going forward. The legacy Simba driver is available from the [Databricks ODBC driver archive](https://www.databricks.com/spark/odbc-drivers-archive#simba_odbc).

## Métodos de autenticación

Al conectarte a Azure Databricks, tienes dos métodos principales de autenticación:

### 1. Autenticación de Microsoft Entra ID (antes Azure AD)

Este es el enfoque recomendado para conectarte a Azure Databricks cuando tu organización usa Microsoft Entra ID. Este método ofrece inicio de sesión único sin complicaciones y mayor seguridad mediante identidades administradas.

#### Acerca de la aplicación empresarial de Tabular Editor

Al conectarte a Azure Databricks mediante la autenticación de Microsoft Entra ID, Tabular Editor utiliza una aplicación empresarial registrada llamada "Tabular Editor 3 - User Delegated Access to Azure Databricks" con el identificador de aplicación (cliente): `ea0fc0fe-ed02-40d7-a29a-cc0a59d8b42c`.

Esta aplicación empresarial requiere los siguientes permisos de API:

- **Microsoft Graph** (`00000003-0000-0000-c000-000000000000`)
  - `offline_access` (Delegado): este permiso permite a Tabular Editor mantener el acceso a los datos para los que le has dado permiso, incluso cuando no estés usando la aplicación activamente. Esto es necesario para mantener una conexión persistente con Databricks.
  - `openid` (Delegado): permite que los usuarios inicien sesión en la aplicación con sus cuentas profesionales o educativas y permite que la aplicación vea información básica del perfil del usuario.
  - `profile` (Delegado): permite que la aplicación vea información básica del perfil, como nombre, correo electrónico, foto y nombre de usuario.
  - `User.Read` (Delegado): permite que la aplicación lea tu perfil y te identifique al acceder a la API de Databricks.

- **API de Azure Databricks** (`2ff814a6-3304-4ab8-85cb-cd0e6f879c1d`)
  - `user_impersonation` (Delegado): permite acceder a Azure Databricks en nombre del usuario que ha iniciado sesión. Esto permite que Tabular Editor se conecte a tu Workspace de Databricks usando tus credenciales.

Para más información sobre los permisos de Microsoft Entra ID, consulta la [documentación de Microsoft sobre los tipos de permisos](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-permissions-and-consent) y la [experiencia de consentimiento de aplicaciones](https://learn.microsoft.com/en-us/azure/active-directory/develop/application-consent-experience).

> [!IMPORTANT]
> Estos permisos son necesarios para que Tabular Editor acceda de forma segura a tus datos de Azure Databricks mediante tus credenciales de Microsoft Entra ID. Sin estos permisos, Tabular Editor no puede autenticarse correctamente en tu Workspace de Azure Databricks.

#### Proceso de consentimiento para la autenticación de Microsoft Entra ID

La primera vez que intentes conectarte a Azure Databricks mediante la autenticación de Microsoft Entra ID, es posible que se te pida que concedas consentimiento para los permisos necesarios. El proceso de consentimiento depende de las directivas de Microsoft Entra ID de tu organización:

##### Consentimiento del usuario

Si tu organización permite que los usuarios otorguen consentimiento a las aplicaciones:

1. Verás un aviso de consentimiento de Microsoft en el que se te pide permiso para que Tabular Editor acceda a Azure Databricks en tu nombre
2. Revisa los permisos que se están solicitando
3. Haz clic en **Aceptar** para otorgar el consentimiento

> [!NOTE]
> Que se requiera el consentimiento del administrador depende de las directivas de Microsoft Entra ID de tu organización, no necesariamente de los permisos de API específicos que se estén solicitando. Muchas organizaciones permiten que los usuarios otorguen por sí mismos el consentimiento para permisos delegados, mientras que otras requieren la aprobación del administrador para todas las aplicaciones de terceros, independientemente del nivel de permisos.

##### Consentimiento del administrador requerido

Si tu organización restringe el consentimiento del usuario (algo habitual en entornos empresariales):

1. Recibirás un mensaje de error en 'mensajes' que indica que se requiere el consentimiento del administrador
2. Tendrás que ponerte en contacto con tu departamento de TI o con el administrador de Microsoft Entra ID
3. Facilítales lo siguiente:
   - Nombre de la aplicación: "Tabular Editor 3 - User Delegated Access to Azure Databricks"
   - ID de la aplicación: `ea0fc0fe-ed02-40d7-a29a-cc0a59d8b42c`
   - Permisos necesarios: Microsoft Graph (offline_access, openid, profile, User.Read) y Azure Databricks API (user_impersonation)

Tu administrador puede conceder el consentimiento para toda la organización de una de estas dos formas:

**Opción 1: A través del portal de administración de Microsoft Entra ID**

1. Ve a Microsoft Entra ID > Aplicaciones empresariales
2. Busca "Tabular Editor 3 - User Delegated Access to Azure Databricks"
3. Selecciona la aplicación y ve a Permisos
4. Haz clic en "Conceder consentimiento del administrador para [Organization]"

**Opción 2: Con la URL directa de consentimiento del administrador**
Los administradores pueden usar el siguiente enlace directo para conceder el consentimiento:

```
https://login.microsoftonline.com/organizations/v2.0/adminconsent?client_id=ea0fc0fe-ed02-40d7-a29a-cc0a59d8b42c&scope=https://graph.microsoft.com/offline_access%20https://graph.microsoft.com/openid%20https://graph.microsoft.com/profile%20https://graph.microsoft.com/User.Read%202ff814a6-3304-4ab8-85cb-cd0e6f879c1d/user_impersonation&redirect_uri=https://tabulareditor.com
```

Para más información sobre el consentimiento del administrador, consulta la documentación de Microsoft sobre [Configurar cómo los usuarios dan su consentimiento a las aplicaciones](https://learn.microsoft.com/en-us/azure/active-directory/manage-apps/configure-user-consent).

#### Pasos para la autenticación con Microsoft Entra ID:

1. En Tabular Editor 3, ve a **Modelo** > **Importar tablas...**
2. Selecciona **Nuevo origen** > **Databricks**
3. En el cuadro de diálogo de conexión:
   - Introduce la URL de tu Workspace de Databricks (formato: `https://<region>.azuredatabricks.net`)
   - Selecciona **Microsoft Entra ID** como método de autenticación
   - Para HTTP Path, especifica la ruta a tu clúster de Databricks (p. ej., `/sql/1.0/warehouses/<warehouse-id>`)

> [!NOTE]
> La URL de tu Workspace de Databricks debe tener el formato `https://<region>.azuredatabricks.net`; por ejemplo, `https://westeurope.azuredatabricks.net`.

### 2. Autenticación mediante token de acceso personal (PAT)

Si la integración con Microsoft Entra ID no está disponible o si prefieres la autenticación basada en tokens, puedes usar un token de acceso personal.

#### Pasos para la autenticación con PAT:

1. Genera un token de acceso personal en tu Workspace de Azure Databricks:
   - Ve a tu Workspace de Databricks
   - Haz clic en el icono de tu perfil de usuario en la esquina superior derecha
   - Selecciona **Configuración de usuario**
   - Ve a la pestaña **Tokens de acceso**
   - Haz clic en **Generar nuevo token**
   - Indica un nombre y, si lo deseas, establece una fecha de caducidad
   - Haz clic en **Generar** y copia el valor del token

2. En Tabular Editor 3, ve a **Modelo** > **Importar tablas...**

3. Selecciona **Nueva fuente** > **Databricks**

4. En el cuadro de diálogo de conexión:
   - Introduce la URL de tu Workspace de Databricks
   - Selecciona **Token de acceso personal** como método de autenticación
   - Pega tu token en el campo **Token**
   - En HTTP Path, especifica la ruta a tu clúster de Databricks (p. ej., `/sql/1.0/warehouses/<warehouse-id>`)

## Cómo encontrar tu HTTP Path

El parámetro HTTP Path es esencial para conectarte a tu Databricks SQL Warehouse. Para encontrar este valor:

1. Ve a tu Workspace de Databricks
2. Ve a **SQL** > **SQL Warehouses**
3. Selecciona el SQL Warehouse al que quieres conectarte
4. Busca la sección **Detalles de conexión**
5. Copia el valor de la ruta HTTP, que debe tener el formato: `/sql/1.0/warehouses/<warehouse-id>`

## Importación de tablas desde Databricks

Una vez que hayas configurado la conexión:

1. Haz clic en **Probar conexión** para verificar tus credenciales y la configuración de la conexión
2. Si la conexión es correcta, haz clic en **Siguiente**
3. Selecciona si quieres importar tablas/vistas específicas o usar una consulta SQL personalizada
4. Si seleccionas tablas/vistas:
   - Explora los catálogos, esquemas y tablas disponibles
   - Selecciona las tablas que quieres importar
   - Opcionalmente, previsualiza y filtra las columnas
5. Revisa tus selecciones y haz clic en **Importar** para finalizar

## Solución de problemas de conexión

Si tienes problemas para conectarte a Azure Databricks:

- Comprueba que la URL de tu Workspace sea correcta y accesible
- Asegúrate de que tu token de acceso personal, Personal Access Token, no haya caducado (si usas la autenticación PAT)
- Comprueba que tu cuenta de usuario tiene los permisos necesarios en Databricks
- Comprueba que la ruta HTTP apunte a un SQL Warehouse activo
- Asegúrate de que tu red permita conexiones al servicio de Databricks

### Solución de problemas de autenticación de Microsoft Entra ID

Si usas la autenticación de Microsoft Entra ID y se producen errores:

#### "AADSTS65001: The user or administrator has not consented to use the application"

Este error se produce cuando no se han concedido los permisos necesarios:

1. Si tienes los privilegios necesarios:
   - Haz clic en el enlace de consentimiento en los mensajes de error
   - Revisa y acepta la solicitud de permisos

2. Si no tienes privilegios suficientes:
   - Contacta con tu administrador de TI
   - Proporciónale el identificador de la aplicación: `ea0fc0fe-ed02-40d7-a29a-cc0a59d8b42c`
   - Pídele que conceda el consentimiento de la organización para la aplicación empresarial de Tabular Editor

#### "AADSTS700016: Application with identifier was not found in the directory"

Esto puede ocurrir si tu organización usa una política de aplicaciones restringidas:

1. Contacta con tu administrador de Microsoft Entra ID
2. Pídele que añada la aplicación empresarial de Tabular Editor (ID: `ea0fc0fe-ed02-40d7-a29a-cc0a59d8b42c`) a la lista de aplicaciones permitidas de tu organización

> [!TIP]
> En algunas organizaciones, los departamentos de TI pueden exigir una solicitud formal o una revisión de seguridad antes de aprobar nuevas aplicaciones empresariales. Prepárate para explicar que Tabular Editor 3 utiliza esta aplicación para conectarse de forma segura a recursos de Azure Databricks mediante la infraestructura de autenticación existente de Microsoft Entra ID de la organización.

## Uso de «Actualizar esquema de tabla» con Databricks

Después de importar tablas desde Azure Databricks, puedes usar la característica **Actualizar esquema de tabla** de Tabular Editor para mantener tu modelo sincronizado con los cambios en las tablas de Databricks.

Para actualizar el esquema:

1. Haz clic con el botón derecho en la tabla importada en el Explorador TOM
2. Selecciona **Actualizar esquema de tabla**
3. Revisa los cambios detectados y aplícalos según sea necesario

Para consultas complejas o si tienes problemas con la detección del esquema, considera habilitar la opción **Usar Analysis Services para la detección de cambios** en **Herramientas** > **Preferencias** > **Comparación de esquemas**, tal como se describe en la documentación [Actualización del esquema de la tabla](xref:importing-tables#updating-table-schema-through-analysis-services).

