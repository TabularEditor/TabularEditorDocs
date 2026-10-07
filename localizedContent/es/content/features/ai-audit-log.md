---
uid: ai-audit-log
title: Registro de auditoría de IA
author: Morten Lønskov
updated: 2026-09-23
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.27.0
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          none: true
        - edition: Enterprise
          full: true
---

# Registro de auditoría de IA

Tabular Editor 3 [Enterprise Edition](xref:editions), including Trial licenses, writes a local log of [AI Assistant](xref:ai-assistant) and [MCP server](xref:mcp-server) activity on your computer. It records:

- which permissions were requested and how they were answered
- which tools ran and how each one ended
- the full text of any C# script the AI Assistant or an MCP agent ran or submitted to run

## Log location

A menos que un administrador lo haya movido, el registro se escribe en:

```text
%LocalAppData%\TabularEditor3\AI\audit
```

**Open audit folder** on **Tools > Preferences > AI Features** and in the **Tools > MCP Server...** dialog opens it. The folder is created when the first record is written and holds one `ai-audit-<date>.jsonl` file per UTC day, with saved scripts under `scripts\<date>`.

## Qué se registra

Each line is one JSON object, and every record starts with the same fields:

| Campo       | Qué contiene                                                                                                                  |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `ts`        | Cuándo ocurrió, en UTC y con precisión de milisegundos                                                                        |
| `event`     | Which kind of record this is, from the next table                                                                             |
| `surface`   | `chat` para el Asistente de IA, `mcp` para un agente externo a través del servidor MCP                                        |
| `sessionId` | La conversación o sesión de MCP a la que pertenece la acción. No aparece si no pertenece a ninguno de los dos |
| `model`     | El nombre del modelo semántico que estaba abierto. Absent when no model was open                              |
| `user`      | El nombre de la cuenta de Windows                                                                                             |

The fields that follow the common ones depend on the event:

| `event`       | Se registra cuando                                                    | Qué contiene                                                                                                                                                                            |
| ------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `consent`     | A permission is requested                                             | El recurso, el nivel de acceso, si fue una concesión puntual o permanente, si lo concediste o lo denegaste, y durante cuánto tiempo                                                     |
| `tool_call`   | Se ejecuta una herramienta                                            | The tool's name, the permissions it needed as `Resource:Access`, how it ended, how many milliseconds it took, the names of its arguments and the total size of their values in bytes    |
| `script`      | The AI Assistant or an MCP agent runs, or submits to run, a C# script | La herramienta, el estado, el resultado, la ruta de la copia guardada, su hash SHA-256 y cuántos cambios realizó en el modelo                                                           |
| `turn`        | Termina un turno de chat                                              | El proveedor, el nombre del modelo, el host del endpoint, el resultado, el número de turno y los recuentos de tokens, incluidos los que se almacenaron en caché y los que se facturaron |
| `config`      | La configuración de la IA cambia                                      | El proveedor, el nombre del modelo y el host del endpoint                                                                                                                               |
| `mcp_server`  | El servidor MCP se inicia o se detiene                                | El puerto, si se requiere un token de acceso y, al iniciarse, el permiso concedido para cada uno de los cinco recursos                                                                  |
| `mcp_session` | Un agente se conecta o se desconecta                                  | El nombre y la versión del cliente, y la versión negociada del protocolo MCP                                                                                                            |

A `tool_call` record ends with one of these outcomes:

- `ok`
- `error`
- `denied`: the permission it needed wasn't granted
- `policy`: an administrator's limit blocked it
- `cancelled`: you stopped the turn, or the client disconnected before the tool finished

### Scripts are saved in full

Each script is saved verbatim as a `.csx` file under `scripts\<date>`, and the `script` record holds only the file's path and SHA-256 hash. Use the hash to verify that the file matches the script that ran.

## Lo que nunca se registra

- the text of your prompts and the assistant's replies
- any value from your model (a `tool_call` records only argument names and their total size)
- API keys and access tokens

## Retención

Log files and `scripts\<date>` folders older than 30 days are deleted by a cleanup that runs once per Tabular Editor session, before the first record is written. Administrators can change the retention period, or keep everything. See [Policies](#policies).

## Policies

These [policies](xref:policies), both of which require Enterprise Edition, control the log:

| Valor                     | Tipo                | Qué hace                                                                                                                                                                                             |
| ------------------------- | ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AiAuditLogPath`          | Ruta                | Writes the log to another folder for central collection, such as a UNC path to a network share. The path must be absolute; a relative path is ignored and the default folder is used |
| `AiAuditLogRetentionDays` | Número, de 0 a 3650 | Cuántos días se conserva. `0` conserva todo. El valor predeterminado es 30                                                                                           |

Redirecting the log also moves the saved scripts, and because the log is written with the signed-in user's Windows account, that account needs write access to a redirected folder.

If the log can't be written, for example because a network share is unreachable, Tabular Editor writes one information entry to its application log for the session and doesn't log later failures. The AI Assistant and the MCP server keep working.

## Pasos a seguir

- @ai-assistant
- @mcp-server
- @policies
- @editions
