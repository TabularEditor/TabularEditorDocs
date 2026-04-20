---
uid: te-cli-auth
title: Authentication and Connections
author: Peer Grønnerup
updated: 2026-04-20
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      none: true
    - product: Tabular Editor CLI
      full: true
---
# Authentication and Connections

> [!IMPORTANT]
> The Tabular Editor CLI is in **Limited Public Preview**. It is offered for evaluation with a Tabular Editor account; no license is required during preview. Commands, flags, and outputs may change before general availability. **The preview build stops functioning after 2026-09-30.** We recommend against using the CLI in production CI/CD pipelines during preview.

The Tabular Editor CLI authenticates to Power BI Service, Microsoft Fabric, and Azure Analysis Services using the same Power BI Desktop client ID that Tabular Editor 3 uses. Tokens are cached locally so you authenticate once and re-run commands silently until the refresh token expires (typically 90 days).

## Authentication methods

The CLI supports the full Azure Identity credential chain:

| Method | When to use | `--auth` value |
| -- | -- | -- |
| Interactive browser | Local development — opens the system browser | `interactive` (default) |
| Device code | SSH sessions, headless VMs, devcontainers | `device-code` |
| Service principal (client secret) | Automation, CI/CD | `env` or pass `-u / -p / -t` |
| Service principal (certificate) | Automation with certificate-based auth | Pass `--certificate` |
| Environment variables | `AZURE_CLIENT_ID` / `AZURE_CLIENT_SECRET` / `AZURE_TENANT_ID` | `env` |
| Managed identity | Azure VMs, Azure Container Apps, Azure Functions | `managed-identity` |

The default (`auto`) tries environment credentials first, then falls back to interactive browser.

## `te auth login`

Authenticate and cache the result for subsequent commands:

```bash
# Browser-based interactive login (default)
te auth login

# Device code flow (headless / SSH / CI)
te auth login --device-code

# Service principal with client secret
te auth login -u <app-id> -p <secret> -t <tenant>

# Service principal — read secret from stdin
echo $AZURE_CLIENT_SECRET | te auth login -u <app-id> -p - -t <tenant>

# Service principal with certificate
te auth login -u <app-id> -t <tenant> --certificate ./sp.pfx --certificate-password ...

# Managed identity (Azure-hosted)
te auth login --identity
```

> [!WARNING]
> Passing secrets directly on the command line is visible in `ps` output and shell history. Prefer the `AZURE_CLIENT_SECRET` environment variable, or pipe the secret via stdin with `-p -`.

## `te auth status`

Display the current authentication state without opening a browser:

```bash
te auth status
te auth status --output json
```

Exit code is `0` when a valid session exists, `1` when not logged in or expired.

## `te auth logout`

Clear all cached credentials:

```bash
te auth logout
```

## Credential storage

Tokens are cached under your home directory. File permissions are restricted to the current user (`0600` on POSIX):

| Platform | Location | Notes |
| -- | -- | -- |
| Windows | `%USERPROFILE%\.te-cli\auth-record.json` | Token cache encrypted via DPAPI through Azure.Identity |
| Linux | `~/.te-cli/auth-record.json` | Token cache via libsecret through Azure.Identity |
| macOS | `~/.te-cli/token-cache.bin` | File-based cache (bypasses Keychain to avoid repeated prompts) |

Device-code and interactive browser flows use separate record files so they can coexist.

## `te connect` — set the active connection

`te connect` persists an active connection for the current terminal session. Subsequent commands that take `-s` / `-d` can omit them:

```bash
# Remote workspace
te connect my-workspace my-model

# Local TMDL folder or .bim file
te connect ./my-model

# Connect to a running Power BI Desktop instance (Windows only)
te connect --local

# Show the active connection
te connect
```

Active-connection state is per-terminal-session: opening a new terminal starts fresh.

## Connecting to different clouds

The CLI detects the correct scope from the server URL for:

- Power BI Service and Fabric (commercial, US Gov, China, Germany clouds)
- Azure Analysis Services (`asazure://...`)
- Local SSAS (`localhost`, named instances — Windows only)

Pass an XMLA endpoint, workspace name, or `powerbi://` URL as `--server`:

```bash
te connect "powerbi://api.powerbi.com/v1.0/myorg/Finance" "Revenue Model"
te connect "asazure://westeurope.asazure.windows.net/myaas" "MyModel"
te connect localhost "AdventureWorks"
```

## Connection profiles

For repeated use of the same connection — especially when you deploy to multiple environments — save named profiles:

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

Profiles can also carry behavioral overrides that take effect whenever the profile is active:

```bash
# In dev, disable the BPA gate on deploy and loosen validation
te profile set dev --bpa-on-deploy false --validate-on-mutation false

# In prod, force auto-format before any mutation
te profile set prod --auto-format true
```

See @te-cli-config for the full list of overridable behaviors.

## Non-interactive authentication

For CI/CD pipelines, agents, or any unattended context, avoid interactive flows by combining:

- The `--non-interactive` global flag (fails fast instead of prompting).
- One of the non-interactive auth methods: `env`, `managed-identity`, or explicit service principal credentials.

Environment-based example for a pipeline:

```bash
export AZURE_CLIENT_ID=<app-id>
export AZURE_CLIENT_SECRET=<secret>
export AZURE_TENANT_ID=<tenant>

te deploy ./model -s my-workspace -d my-model \
  --auth env \
  --non-interactive \
  --force \
  --ci github
```

See @te-cli-cicd for complete GitHub Actions and Azure DevOps Pipelines examples.

## Environment variable overrides

| Variable | Purpose |
| -- | -- |
| `AZURE_CLIENT_ID` / `AZURE_CLIENT_SECRET` / `AZURE_TENANT_ID` | Service principal credentials (used by `--auth env`). |
| `TE_CONFIG` | Override the config file path — see @te-cli-config. |
| `TE_COMPAT=te2` | Force TE2-compatibility mode — see @te-cli-migrate. |
| `TE_DEBUG=1` | Enable debug logging to stderr (connection strings, auth flow, timing). |

## Next steps

- @te-cli-commands — what you can do once connected.
- @te-cli-config — configuration and profile behavior.
- @te-cli-cicd — pipeline examples using service principals and managed identity.
