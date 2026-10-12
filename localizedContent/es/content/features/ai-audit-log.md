---
uid: ai-audit-log
title: Registro de auditoría de IA
author: Morten Lønskov
updated: 2026-10-09
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

Tabular Editor 3 [Edición Enterprise](xref:editions), incluidas las licencias de prueba, escribe en tu equipo un registro local de la actividad del [Asistente de IA](xref:ai-assistant) y del [servidor MCP](xref:mcp-server). Registra:

- los permisos solicitados y cómo se respondió a cada solicitud
- qué herramientas se ejecutaron y cómo terminó cada una
- el texto completo de cualquier C# Script que el Asistente de IA o un agente MCP haya ejecutado o enviado a ejecutar

## Ubicación del registro

A menos que un administrador lo haya movido, el registro se escribe en:

```text
%LocalAppData%\TabularEditor3\AI\audit
```

El botón **Abrir carpeta de auditoría**, en **Herramientas > Preferencias > Funciones de IA** y en el cuadro de diálogo **Herramientas > Servidor MCP...**, abre esa carpeta. La carpeta se crea cuando se escribe el primer registro y contiene un archivo `ai-audit-<date>.jsonl` por día UTC, con los scripts guardados en `scripts\\<date>`.

## Qué se registra

Cada línea es un objeto JSON y cada registro comienza con los mismos campos:

| Campo       | Qué contiene                                                                                                                  |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `ts`        | Cuándo ocurrió, en UTC y con precisión de milisegundos                                                                        |
| `event`     | El tipo de registro, según la tabla siguiente                                                                                 |
| `surface`   | `chat` para el Asistente de IA, `mcp` para un agente externo a través del servidor MCP                                        |
| `sessionId` | La conversación o sesión de MCP a la que pertenece la acción. No aparece si no pertenece a ninguno de los dos |
| `model`     | El nombre del modelo semántico que estaba abierto. No aparece cuando no había ningún modelo abierto           |
| `user`      | El nombre de la cuenta de Windows                                                                                             |

Los campos que siguen a los comunes dependen del evento:

| `event`       | Se registra cuando                                                                   | Qué contiene                                                                                                                                                                                     |
| ------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `consent`     | Se solicita un permiso                                                               | El recurso, el nivel de acceso, si fue una concesión puntual o permanente, si lo concediste o lo denegaste, y durante cuánto tiempo                                                              |
| `tool_call`   | Se ejecuta una herramienta                                                           | El nombre de la herramienta, los permisos que necesitó como `Resource:Access`, cómo terminó, cuántos milisegundos tardó, los nombres de sus argumentos y el tamaño total de sus valores en bytes |
| `script`      | El Asistente de IA o un agente MCP ejecuta un C# Script o lo envía para su ejecución | La herramienta, el estado, el resultado, la ruta de la copia guardada, su hash SHA-256 y cuántos cambios realizó en el modelo                                                                    |
| `turn`        | Termina un turno de chat                                                             | El proveedor, el nombre del modelo, el host del endpoint, el resultado, el número de turno y los recuentos de tokens, incluidos los que se almacenaron en caché y los que se facturaron          |
| `config`      | La configuración de la IA cambia                                                     | El proveedor, el nombre del modelo y el host del endpoint                                                                                                                                        |
| `mcp_server`  | El servidor MCP se inicia o se detiene                                               | El puerto, si se requiere un token de acceso y, al iniciarse, el permiso concedido para cada uno de los cinco recursos                                                                           |
| `mcp_session` | Un agente se conecta o se desconecta                                                 | El nombre y la versión del cliente, y la versión negociada del protocolo MCP                                                                                                                     |

Un registro `tool_call` termina con uno de estos resultados:

- `ok`
- `error`
- `denied`: no se concedió el permiso necesario o una política del administrador lo bloqueó. Solo los registros `mcp` usan este resultado; en el Asistente de IA, una herramienta bloqueada de esta forma termina como `error`
- `cancelled`: interrumpiste el turno o el cliente se desconectó antes de que la herramienta terminara

### Los scripts se guardan completos

Cada script se guarda literalmente como un archivo `.csx` en `scripts\\<date>`, y el registro `script` solo contiene la ruta del archivo y el hash SHA-256. Usa el hash para verificar que el archivo coincide con el script que se ejecutó. Un script que no compila no se guarda.

## Lo que nunca se registra

- el texto de tus prompts y las respuestas del asistente
- cualquier valor de tu modelo (un registro `tool_call` solo registra los nombres de los argumentos y su tamaño total)
- Claves de API y tokens de acceso

## Retención

Los archivos de registro y las carpetas `scripts\\<date>` con más de 30 días se eliminan mediante una limpieza que se ejecuta una vez por sesión de Tabular Editor, antes de que se escriba el primer registro. Los administradores pueden cambiar el período de retención o conservarlo todo. Consulta las [políticas](#policies).

## Directivas

Estas [políticas](xref:policies), que requieren la Edición Enterprise en ambos casos, controlan el registro:

| Valor                     | Tipo                | Qué hace                                                                                                                                                                                                                                         |
| ------------------------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `AiAuditLogPath`          | Ruta                | Escribe el registro en otra carpeta para recopilarlo de forma centralizada, por ejemplo, en una ruta UNC a un recurso compartido de red. La ruta debe ser absoluta; si es relativa, se ignora y se usa la carpeta predeterminada |
| `AiAuditLogRetentionDays` | Número, de 0 a 3650 | Cuántos días se conserva. `0` conserva todo. El valor predeterminado es 30                                                                                                                                       |

Redirigir el registro también traslada los scripts guardados y, como el registro se escribe con la cuenta de Windows del usuario que ha iniciado sesión, esa cuenta necesita permisos de escritura en la carpeta redirigida. Los nombres de archivo no incluyen el nombre de usuario ni el del equipo, así que asigna a cada usuario una carpeta independiente. Las variables de entorno como `%USERNAME%` solo se expanden en un valor `REG_EXPAND_SZ`; la plantilla administrativa escribe `REG_SZ`, que se usa tal cual.

Si no se puede escribir en el registro, por ejemplo porque un recurso compartido de red no está disponible, Tabular Editor escribe una entrada informativa en su registro de aplicación para esa sesión y no registra fallos posteriores. El Asistente de IA y el servidor MCP siguen funcionando.

## Pasos a seguir

- @ai-assistant
- @mcp-server
- @policies
- @editions
