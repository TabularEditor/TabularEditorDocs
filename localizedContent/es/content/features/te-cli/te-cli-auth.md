---
uid: te-cli-auth
title: Autenticación y conexiones
author: Peer Grønnerup
updated: 2026-06-11
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      none: true
    - product: Tabular Editor CLI
      full: true
---

# Autenticación y conexiones

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

La CLI de Tabular Editor se autentica en Power BI Service, Microsoft Fabric y Azure Analysis Services con el mismo identificador de cliente de Power BI Desktop que utiliza Tabular Editor 3. Los tokens se almacenan en caché localmente, por lo que solo tienes que autenticarte una vez y puedes volver a ejecutar los comandos sin interacción hasta que caduque el token de actualización (normalmente a los 90 días).

## Métodos de autenticación

La CLI admite la cadena completa de credenciales de Azure Identity:

| Método                                                        | Cuándo usarlo                                                           | Valor de `--auth`                                        |
| ------------------------------------------------------------- | ----------------------------------------------------------------------- | -------------------------------------------------------- |
| Automatic                                                     | Tries environment credentials, then cached or interactive browser login | `auto` (default)                      |
| Navegador interactivo                                         | Desarrollo local: abre el navegador del sistema         | `interactive`                                            |
| Principal de servicio (secreto de cliente) | Automatización, CI/CD, sin interfaz gráfica / SSH / WSL                 | `spn` (con `-u / -p / -t`) o `env`    |
| Principal de servicio (certificado)        | Automatización con autenticación basada en certificados                 | `spn` (con `-u / -t / --certificate`) |
| Variables de entorno                                          | `AZURE_CLIENT_ID` / `AZURE_CLIENT_SECRET` / `AZURE_TENANT_ID`           | `env`                                                    |
| Identidad administrada                                        | Máquinas virtuales de Azure, Azure Container Apps y Azure Functions     | `managed-identity`                                       |

> [!NOTE]
> `--auth` es una opción **global**, disponible en todos los comandos `te`, no solo en `te auth login`. Úsalo en [`te deploy`](xref:te-cli-commands#deploy), [`te refresh`](xref:te-cli-commands#refresh), [`te query`](xref:te-cli-commands#query), [`te connect`](xref:te-cli-commands#connect) o en cualquier otro comando que se conecte a un punto de conexión remoto para sustituir la cadena predeterminada en esa ejecución. La opción predeterminada (`auto`) intenta primero las credenciales del entorno y, si no están disponibles, recurre al inicio de sesión en caché o interactivo en el navegador.

En escenarios sin interfaz gráfica, con SSH, WSL o devcontainer, usa una entidad de servicio: `te auth login -u <id> -p <secret> -t <tenant>` (o `--certificate`). El inicio de sesión se guarda en caché, por lo que los comandos posteriores obtienen tokens de forma silenciosa con `--auth auto`.

## `te auth login`

Autentícate y guarda el resultado en caché para los comandos posteriores:

```bash
# Browser-based interactive login (default)
te auth login

# Service principal with client secret
te auth login -u "$AZURE_CLIENT_ID" -p "$AZURE_CLIENT_SECRET" -t "$AZURE_TENANT_ID"

# Service principal - read secret from stdin
echo "$AZURE_CLIENT_SECRET" | te auth login -u "$AZURE_CLIENT_ID" -p - -t "$AZURE_TENANT_ID"

# Service principal with certificate
te auth login -u "$AZURE_CLIENT_ID" -t "$AZURE_TENANT_ID" --certificate ./sp.pfx --certificate-password "$CERT_PASSWORD"

# Managed identity (Azure-hosted)
te auth login --identity     # Alias: -I
```

Después de iniciar sesión correctamente con una entidad de servicio, la CLI **almacena las credenciales en caché** para que todos los comandos `te` posteriores puedan adquirir tokens de forma silenciosa; no hace falta volver a pasar `-u / -p / -t` ni establecer las variables de entorno `AZURE_CLIENT_*`. Pasa `--save=false` para iniciar sesión una sola vez sin actualizar la caché, o ejecuta `te auth logout` para borrarla.

> [!WARNING]
> Pasar secretos directamente en la línea de comandos los expone a los listados de procesos y al historial del shell. Es preferible usar la variable de entorno `AZURE_CLIENT_SECRET`, o pasar el secreto por stdin con `-p -`.

## `te auth status`

Muestra el estado actual de la autenticación sin abrir un navegador:

```bash
te auth status
te auth status --output-format json
```

Esto devuelve un código de salida `0` cuando existe una sesión válida y `1` cuando no se ha iniciado sesión o ha expirado.

## `te auth logout`

Borra todas las credenciales almacenadas en caché:

```bash
te auth logout
```

## Almacenamiento de credenciales

De forma predeterminada, la CLI almacena los tokens de acceso y de actualización, así como los registros de entidades de servicio, en el **almacén seguro nativo del sistema operativo**. Se selecciona automáticamente como alternativa un archivo `0600` solo cuando el almacén de claves del sistema operativo no está disponible (por ejemplo, en Linux sin entorno gráfico y sin libsecret/D-Bus).

| Plataforma                                  | Backend                                            | Ubicación de almacenamiento                                    |
| ------------------------------------------- | -------------------------------------------------- | -------------------------------------------------------------- |
| Windows                                     | DPAPI                                              | Por usuario, administrado por MSAL                             |
| Linux                                       | libsecret (llavero del sistema) | Por usuario, administrado por MSAL                             |
| macOS                                       | Llavero                                            | Servicio `com.tabulareditor.cli.*`, cuenta `te-msal-cache.bin` |
| Cualquiera (alternativo) | archivo `0600`                                     | `~/.te-cli/te-msal-cache.bin` y blobs `.bin` por clave         |

Los flujos de navegador interactivo y de principal de servicio comparten la misma caché; el modelo de cuentas de MSAL los distingue: no hay archivos auxiliares `auth-record*.json` separados. Ejecuta cualquier comando con `--debug` para ver qué backend se seleccionó al iniciar.

`te auth logout` borra todos los registros almacenados en caché (tanto la caché de tokens de MSAL como cualquier blob de SPN), independientemente del backend que se esté usando.

## `te connect` - establece la conexión activa

`te connect` guarda una conexión activa para la sesión actual del terminal. Los comandos posteriores que aceptan `-s` / `-d` pueden omitirlos:

```bash
# Remote workspace
te connect my-workspace my-model

# Local TMDL folder, .bim file, or .SemanticModel container
te connect ./my-model

# Connect to a running Power BI Desktop instance (Windows only)
te connect --local

# Show the active connection
te connect

# Clear the active connection (and any workspace mirror)
te connect --clear
```

El estado de la conexión activa es específico de cada sesión de terminal: al abrir un terminal nuevo, se empieza desde cero. Inspect or clean up session state with [`te session`](xref:te-cli-commands#session).

### Modo del área de trabajo (`-w` / `--workspace`)

`te connect -w <target>` vincula un origen principal con un espejo secundario, de modo que cada `--save` posterior guarde en ambos. Úsalo para mantener sincronizada una copia de trabajo local de un modelo remoto, o para enviar ediciones locales a un Workspace a medida que guardas:

```bash
# Mirror remote workspace ↔ local TMDL folder
te connect Finance "Revenue Model" -w ./revenue-model

# Mirror local source ↔ remote workspace (initial deploy + auto-redeploy on save)
te connect ./revenue-model -w Finance "Revenue Model"
```

El orden de guardado siempre es **primero local y después remoto**, para que la copia en disco refleje el cambio más reciente incluso si falla el envío al servidor. Consulta @te-cli-commands#workspace-mode--w----workspace para obtener información sobre `--workspace-format`, la semántica de sobrescritura y cómo vaciar el espejo del workspace.

## Conexión a distintas nubes

La CLI detecta el ámbito correcto a partir de la URL del servidor para:

- Power BI Service y Fabric (nubes: comercial, US Gov, China y Alemania)
- Azure Analysis Services (`asazure://...`)
- SSAS local (`localhost`, instancias con nombre; solo en Windows)

Pasa un punto de conexión XMLA, un nombre de Workspace o una URL `powerbi://` como `--server`:

```bash
te connect "powerbi://api.powerbi.com/v1.0/myorg/Finance" "Revenue Model"
te connect "powerbi://api.powerbi.com/v1.0/SpaceParts/Finance" "Revenue Model"
te connect "asazure://westeurope.asazure.windows.net/myaas" "MyModel"
te connect localhost "AdventureWorks"
```

## Perfiles de conexión

Si usas la misma conexión repetidamente —especialmente al implementar en varios entornos—, guarda perfiles con nombre:

```bash
# Save remote and local profiles
te profile set prod -s my-workspace -d my-model --description "Production"
te profile set dev --model ./model --description "Local dev TMDL"

# List and inspect
te profile list
te profile show prod

# Use a profile as the active connection
te connect --profile prod

# One-shot use without changing the active connection
te deploy ./model --profile staging --force
```

Los perfiles también pueden incluir sobrescrituras de comportamiento que se aplican siempre que el perfil esté activo:

```bash
# In dev, disable the BPA gate on deploy and loosen validation
te profile set dev --bpa-on-deploy false --validate-on-mutation false

# In prod, force auto-format before any mutation
te profile set prod --auto-format true
```

Consulta @te-cli-config para ver la lista completa de comportamientos anulables.

## Autenticación no interactiva

En canalizaciones de CI/CD, agentes o cualquier contexto desatendido, evita los flujos interactivos combinando lo siguiente:

- La opción global `--non-interactive` (falla de inmediato en lugar de pedir datos).
- Uno de los métodos de autenticación no interactiva: `env`, `managed-identity` o credenciales explícitas de una entidad de servicio.

Ejemplo basado en variables de entorno para una canalización:

```bash
export AZURE_CLIENT_ID="your-app-id"
export AZURE_CLIENT_SECRET="your-client-secret"
export AZURE_TENANT_ID="your-tenant-id"

te deploy ./model -s my-workspace -d my-model \
  --auth env \
  --non-interactive \
  --force \
  --ci github
```

Consulta @te-cli-cicd para ver ejemplos completos de GitHub Actions y Azure DevOps Pipelines.

## Variables de entorno de autenticación

La CLI tiene en cuenta las variables de entorno estándar de Azure.Identity cuando usas `--auth env` (y como parte de la cadena `auto`):

| Variable                        | Propósito                                                                                                                                                                                                                                                                                   |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AZURE_CLIENT_ID`               | ID de aplicación de la entidad de servicio.                                                                                                                                                                                                                                 |
| `AZURE_CLIENT_SECRET`           | Secreto de cliente de la entidad de servicio. Se usa junto con `AZURE_CLIENT_ID` y `AZURE_TENANT_ID`.                                                                                                                                                       |
| `AZURE_TENANT_ID`               | ID del inquilino (directorio) del principal de servicio.                                                                                                                                                                                                 |
| `AZURE_CLIENT_CERTIFICATE_PATH` | PATH a un archivo de certificado PEM o PKCS12 para la autenticación del principal de servicio basada en certificados. Se usa junto con `AZURE_CLIENT_ID` y `AZURE_TENANT_ID`.                                                                               |
| `AZURE_AUTHORITY_HOST`          | Anula el host de autoridad para nubes soberanas (p. ej., `login.microsoftonline.us`, `login.partner.microsoftonline.cn`, `login.microsoftonline.de`). De forma predeterminada, se usa la nube comercial. |

Para las variables de entorno específicas de la CLI (PATHs de configuración, registro de depuración, compatibilidad con TE2), consulta @te-cli-config.

## Próximos pasos

- @te-cli-commands - qué puedes hacer una vez conectado.
- @te-cli-config - configuración y comportamiento de los perfiles.
- @te-cli-cicd - ejemplos de canalizaciones que usan principales de servicio e identidad administrada.
