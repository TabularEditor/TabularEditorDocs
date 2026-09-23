---
uid: ai-audit-log
title: Registro de auditoría de IA
author: Morten Lønskov
updated: 2026-09-22
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

La Edición Enterprise de Tabular Editor 3 mantiene un registro local de lo que el [Asistente de IA](xref:ai-assistant) y el [servidor MCP](xref:mcp-server) hicieron en este equipo. Responde a la pregunta que de verdad hace un auditor: qué permisos se solicitaron y cómo se respondieron, qué herramientas se ejecutaron y cómo terminó cada una, y el contenido de cualquier C# Script escrito por un agente.

El registro está diseñado para poder recopilarse de forma segura. Captura _categorías y resultados_, nunca el contenido. Es decir, no se registran nunca tus prompts, las respuestas del asistente ni los valores de datos de tu modelo.

## Dónde se guarda el registro

A menos que un administrador lo haya movido, el registro se escribe en:

```
%LocalAppData%\TabularEditor3\AI\audit
```

Puedes acceder a ella mediante **Abrir carpeta de auditoría**, que se encuentra en dos lugares: en **Herramientas > Preferencias > Funciones de IA** y en el cuadro de diálogo **Herramientas > Servidor MCP...**. La carpeta se crea la primera vez que hay algo que escribir, así que en una instalación nueva todavía no hay nada que abrir.

Dentro encontrarás un archivo por día, `ai-audit-<date>.jsonl`, con rotación por fecha UTC, además de una carpeta `scripts` que contiene los propios scripts en `scripts\<date>`.

## Qué se registra

Cada línea es un objeto JSON. Cada registro comienza con los mismos campos:

| Campo       | Qué contiene                                                                                                                    |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `ts`        | Cuándo ocurrió, en UTC y con precisión de milisegundos                                                                          |
| `event`     | Qué tipo de registro es, según la tabla siguiente                                                                               |
| `surface`   | `chat` para el Asistente de IA, `mcp` para un agente externo a través del servidor MCP                                          |
| `sessionId` | La conversación o sesión de MCP a la que pertenece la acción. Se omite cuando no pertenece a ninguno de los dos |
| `model`     | El nombre del modelo semántico que estaba abierto. No aparece cuando no había ningún modelo                     |
| `user`      | El nombre de la cuenta de Windows                                                                                               |

A continuación vienen los campos que pertenecen al evento:

| `event`       | Se escribe cuando                      | Qué contiene                                                                                                                                                                                      |
| ------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `consent`     | Se solicita un permiso                 | El recurso, el nivel de acceso, si fue una concesión puntual o permanente, si se concedió o se denegó y durante cuánto tiempo                                                                     |
| `tool_call`   | Se ejecuta una herramienta             | El nombre de la herramienta, los permisos que necesitó como `Recurso:Acceso`, cómo terminó, cuántos milisegundos tardó, los _nombres_ de sus argumentos y el tamaño total de sus valores en bytes |
| `script`      | Un agente ejecuta o envía un C# Script | La herramienta, el estado, el resultado, la ruta de la copia guardada, su hash SHA-256 y cuántos cambios realizó en el modelo                                                                     |
| `turn`        | Finaliza un turno de chat              | El proveedor, el nombre del modelo, el host del endpoint, el resultado, el número de turno y el recuento de tokens, incluido lo que se almacenó en caché y lo que se facturó                      |
| `config`      | La configuración de la IA cambia       | El proveedor, el nombre del modelo y el host del endpoint                                                                                                                                         |
| `mcp_server`  | El servidor MCP se inicia o se detiene | El puerto, si se requiere un token de acceso y, al iniciarse, el permiso concedido para cada uno de los cinco recursos                                                                            |
| `mcp_session` | Un agente se conecta o se desconecta   | El nombre y la versión del cliente, y la versión negociada del protocolo MCP                                                                                                                      |

Un registro `tool_call` finaliza de una de estas cinco maneras: `ok`, `error`, `denied` cuando no se concedió el permiso que necesitaba, `policy` cuando lo rechazó el límite establecido por un administrador, o `cancelled` cuando detuviste el turno o el cliente se desconectó antes de que terminara.

### Los scripts se conservan íntegros

El evento `script` es la excepción a «categorías, no contenido», y lo es deliberadamente: un script que un agente ejecutó en tu modelo es lo que más necesitas poder leer después. El texto del script no se incluye en la línea del registro. En su lugar, el script se guarda tal cual en su propio archivo `.csx` en `scripts\\<date>`, y la línea apunta a ese archivo e incluye su hash SHA-256, para que puedas demostrar que el archivo en el disco es el que se ejecutó.

## Qué no se registra nunca

- El texto de tus prompts y de las respuestas del asistente.
- Cualquier valor de tu modelo. Un `tool_call` registra que una herramienta tenía argumentos y su tamaño, nunca su contenido.
- Claves de API y tokens de acceso.

## Retención

Se eliminan los archivos con más de 30 días de antigüedad. La limpieza se ejecuta una vez por sesión, antes de que se escriba la primera línea, así que una copia de Tabular Editor que nunca se abre nunca elimina nada.

Los administradores pueden cambiar ese plazo, incluso conservarlo todo para siempre. Consulta las directivas a continuación.

## Cómo administrarlo

Dos [directivas](xref:policies) controlan el registro. Ambas requieren la Edición Enterprise.

| Valor                     | Tipo                | Qué hace                                                                                                                                                                                                                                                                      |
| ------------------------- | ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AiAuditLogPath`          | Ruta                | Escribe el registro en otra ubicación para que pueda recopilarse de forma centralizada. También funciona una ruta UNC a un recurso compartido de red. La ruta debe ser absoluta; si es relativa, se ignora y se usa la carpeta predeterminada |
| `AiAuditLogRetentionDays` | Número, de 0 a 3650 | Durante cuántos días se conserva. `0` conserva todo. El valor predeterminado es 30                                                                                                                                                            |

Al redirigir el registro, los scripts guardados se mueven con él, ya que se encuentran en la misma carpeta.

La auditoría nunca afecta a la funcionalidad que audita. Si no se puede escribir en el registro, por ejemplo porque no se puede acceder a un recurso compartido redirigido, el fallo se registra una sola vez en el propio registro de Tabular Editor, y el Asistente de IA y el servidor MCP siguen funcionando.

## Ver también

- @ai-assistant
- @mcp-server
- @policies
- @editions
