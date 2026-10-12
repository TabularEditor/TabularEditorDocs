---
uid: ai-compliance
title: Guía de cumplimiento de las funciones de IA
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
          partial: true
          note: "Solo políticas generales. Sin límites de permisos, bloqueo de proveedor ni registro de auditoría"
        - edition: Business
          partial: true
          note: "Solo políticas generales. Sin límites de permisos, bloqueo de proveedor ni registro de auditoría"
        - edition: Enterprise
          full: true
---

# Guía de cumplimiento de las funciones de IA

El [Asistente de IA](xref:ai-assistant) y el [servidor de Model Context Protocol (MCP)](xref:mcp-server) de Tabular Editor 3 dan a los modelos de IA acceso al modelo semántico abierto, dentro de los permisos que los administradores limitan mediante directiva de grupo y que la Edición Enterprise registra en un registro de auditoría. Esta página está dirigida a los equipos de TI, seguridad y cumplimiento que aprueban estas funciones para una organización.

## Funciones de IA

| Funcionalidad   | Qué hace                                                                                                                                                                                                               | Qué realiza la llamada al proveedor de IA                                                    | Tráfico de red                                                |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| Asistente de IA | Un panel de chat de Tabular Editor 3 que lee, consulta y modifica el modelo semántico abierto                                                                                                                          | Tabular Editor 3, desde el equipo del usuario, con una clave de API que el usuario introduce | Saliente hacia el punto de conexión del proveedor configurado |
| Servidor MCP    | Un servidor local al que se conecta un agente de IA que el usuario ya ejecuta, como Claude Code, GitHub Copilot, Codex o Cursor. Luego, el agente lee, consulta y modifica el modelo semántico abierto | El agente, con su propia configuración y suscripción                                         | Solo tráfico entrante en `127.0.0.1`                          |

Ambas funciones se incluyen en el componente de funciones de IA, que forma parte de la instalación predeterminada desde Tabular Editor 3.27.0. Comparten las concesiones de permisos, las políticas de administrador y el registro de auditoría. Las diferencias se describen en [Concesiones de permisos](#permission-grants).

Tabular Editor ApS no opera ningún servicio de IA ni incluye una clave de API. Los prompts, las respuestas, los metadatos del modelo y los datos del modelo de cualquiera de las funciones nunca pasan por los servidores de Tabular Editor. Con la telemetría activada, Tabular Editor 3 envía a Tabular Editor ApS eventos de uso de la IA con el proveedor, el nombre del modelo, un ID de conversación y los recuentos de tokens. La directiva `DisableTelemetry` los desactiva.

El [Centro de confianza de Tabular Editor](https://trust.tabulareditor.com/) publica el Report independiente de pruebas de penetración del Asistente de IA, el Report de auditoría SOC 2 y la lista de subencargados del tratamiento.

## Flujo de datos

### Asistente de IA

El Asistente de IA envía solicitudes directamente desde tu equipo al proveedor configurado en **Herramientas > Preferencias > Funciones de IA > Asistente de IA**: OpenAI, Anthropic, Azure OpenAI o cualquier punto de conexión compatible con OpenAI, incluido un modelo alojado en tu propia red. La autenticación se realiza únicamente mediante clave de API. Consulta [Proveedores compatibles](xref:ai-assistant#supported-providers).

Una solicitud al proveedor contiene:

- el prompt del sistema y las Instrucciones personalizadas vigentes, incluidas las que publique tu organización
- tus mensajes y el historial de la conversación
- contexto sobre el modelo abierto añadido a tus mensajes: el nombre de la base de datos, el recuento de objetos, la selección actual, el título del documento activo, los errores del modelo y los cambios recientes. Tu configuración de **Metadatos del modelo** no impide su envío; sí lo hace un límite `MaxModelMetadataAccess` de `Deny`
- los resultados de las herramientas que invocó el asistente, dentro de las [concesiones de permisos](#permission-grants)
- pasajes de la base de conocimiento de Tabular Editor, una base de datos local creada a partir de la documentación, el blog, las incidencias y los debates de GitHub

Los metadatos del modelo abarcan toda la definición del modelo: nombres de objetos, descripciones y anotaciones, expresiones DAX y M, consultas de origen de las particiones, detalles de conexión del Data source, roles, miembros de los roles y filtros de seguridad a nivel de filas. Los valores escritos en la definición del modelo, como una expresión `DATATABLE` o una tabla de **Introducir datos**, forman parte de los metadatos.

El texto de estas fuentes pasa a formar parte de la solicitud e influye en lo que hace el asistente. Restringe el acceso de escritura a la carpeta de Instrucciones personalizadas de tu organización a las personas que aprueban su contenido.

El acuerdo de tu organización con el proveedor rige la retención, la región en la que se procesan los datos y si el proveedor usa las solicitudes para entrenar modelos. Para mantener el procesamiento dentro de un inquilino de Azure o de una red gobernada por tu organización, usa Azure OpenAI, [Microsoft Foundry](xref:ai-assistant#using-microsoft-foundry) o un [modelo autoalojado](xref:ai-assistant#using-a-local-or-organizational-llm), y bloquea la configuración mediante [directiva](#restrict-the-ai-provider).

### Servidor MCP

El servidor MCP es un listener HTTP enlazado a `127.0.0.1`, con el puerto 42100 como valor predeterminado. No tiene clave de API, no realiza solicitudes salientes y rechaza las solicitudes del navegador con un encabezado `Origin` no local.

El agente conectado envía lo que lee de Tabular Editor 3 a su propio proveedor, conforme a la configuración del agente y a las condiciones del proveedor. Tabular Editor 3 no tiene ninguna configuración para el proveedor del agente, así que gestiona el agente mediante sus propios controles administrativos. Las propias herramientas del agente, como el acceso a archivos y al shell, también quedan fuera de Tabular Editor 3. Los archivos de modelo en disco, los archivos de conversación y los archivos de auditoría pueden leerse por cualquier agente que se ejecute con la cuenta del usuario.

**Requerir token de acceso** está desactivado de forma predeterminada. Mientras esté desactivado, cualquier proceso del equipo puede conectarse al servidor sin credenciales, incluidos los procesos en las sesiones de otros usuarios en un host de Escritorio remoto o de Citrix. La directiva `RequireMcpAccessToken` exige el token para todos los usuarios. Los archivos de registro del agente almacenan el token en texto sin formato, y la opción **Regenerar token** del cuadro de diálogo **Herramientas > Servidor MCP...** invalida todos los registros existentes. Consulta [Ejecución en un equipo compartido](xref:mcp-server#running-on-a-shared-machine).

### Puntos de conexión de red

Permite el acceso a estos puntos de conexión a través del firewall o proxy para las funciones de IA:

| Tráfico                                           | Punto de conexión                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Solicitudes del Asistente de IA                   | El punto de conexión del proveedor configurado, por ejemplo `https://api.openai.com`, `https://api.anthropic.com`, un recurso de Azure OpenAI o tu propio Gateway                                                                                                                                                                                                                                                                               |
| Catálogo de modelos de IA                         | `https://api.tabulareditor.com/AiModels`. Una solicitud anónima para obtener la lista de modelos, que se realiza cuando un usuario abre la lista de modelos de OpenAI o Anthropic. La lista se almacena en caché durante 24 horas. `DisableUpdates` lo desactiva                                                                                                                                |
| Actualizaciones de la base de conocimientos de IA | `https://cdn.tabulareditor.com`. Una comprobación como máximo una vez al día mientras el Asistente de IA esté configurado, sin datos sobre el usuario ni el modelo. Ninguna directiva lo desactiva salvo `DisableAi`. Los usuarios desmarcan **Comprobar si hay actualizaciones de la base de conocimientos al iniciar** en **Herramientas > Preferencias > Funciones de IA > Asistente de IA** |
| Servidor MCP                                      | Ninguno                                                                                                                                                                                                                                                                                                                                                                                                                                         |

La validación de la licencia, la comprobación de actualizaciones y la telemetría usan solicitudes independientes. Consulta [Solicitudes web](xref:security-privacy#web-requests).

### Datos almacenados en el equipo del usuario

Todas las rutas están en `%LocalAppData%\TabularEditor3`, salvo que se indique lo contrario.

| Elemento                                 | Ubicación                                                                                                                                                                                                            | Formato                                                                                                                                                                                                                                                                                                                                                         |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Clave de API del proveedor               | `Preferences.json`                                                                                                                                                                                                   | Cifrada con la API de protección de datos de Windows para el usuario actual. Se borra cuando el componente de IA no está cargado o se establece `DisableAi`                                                                                                                                                                                     |
| Token de acceso de MCP                   | `Preferences.json`                                                                                                                                                                                                   | Cifrado con la API de protección de datos de Windows para el usuario actual                                                                                                                                                                                                                                                                                     |
| Permisos concedidos de forma permanente  | `Preferences.json`                                                                                                                                                                                                   | JSON                                                                                                                                                                                                                                                                                                                                                            |
| Permisos concedidos por modelo           | El archivo de [opciones de usuario](xref:user-options) (`.tmuo`) del modelo: junto a un modelo cargado desde archivos o en `UserOptions` para un modelo abierto desde un servidor | JSON                                                                                                                                                                                                                                                                                                                                                            |
| Conversaciones                           | `AI\Conversations`                                                                                                                                                                                                  | JSON sin cifrar. Contiene prompts, respuestas y resultados de herramientas, incluidas las filas de las consultas DAX cuando **Datos del modelo** está configurado en **Lectura**. Se crean copias archivadas antes de cada compactación. Los archivos se conservan hasta que el usuario elimine la conversación |
| Instrucciones personalizadas del usuario | `AI\\CustomInstructions`                                                                                                                                                                                           | Markdown                                                                                                                                                                                                                                                                                                                                                        |
| Base de conocimientos                    | `kb.sqlite`                                                                                                                                                                                                          | Base de datos SQLite                                                                                                                                                                                                                                                                                                                                            |
| Catálogo de modelos de IA                | `AiModels.json`                                                                                                                                                                                                      | JSON                                                                                                                                                                                                                                                                                                                                                            |
| Registro de auditoría                    | `AI\\audit`, o la carpeta configurada por `AiAuditLogPath`                                                                                                                                                         | Consulta [Registro de auditoría](#audit-log)                                                                                                                                                                                                                                                                                                                    |

## Permisos otorgados

Los permisos otorgados controlan a qué pueden acceder el Asistente de IA y el servidor MCP, con un nivel de acceso por recurso. El usuario configura cada nivel en **Herramientas > Preferencias > Funciones de IA > Permisos**. En la Edición Enterprise, un administrador puede establecer un límite de permiso para cada recurso mediante una directiva:

| Recurso                | A qué pueden acceder las funciones de IA                                                                                                                                                | Predeterminado | Límite para ambas funciones | Límite solo para el servidor MCP |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- | --------------------------- | -------------------------------- |
| Metadatos del modelo   | Lectura: la definición del modelo y las estadísticas del Analizador VertiPaq. Escritura: modificar el modelo mediante C# Scripts        | Leer           | `MaxModelMetadataAccess`    | `McpMaxModelMetadataAccess`      |
| Datos del modelo       | Lectura: resultados de consultas DAX, es decir, valores de datos del modelo                                                                                             | Denegar        | `MaxModelDataAccess`        | `McpMaxModelDataAccess`          |
| Best Practice Analyzer | Lectura: reglas y resultados del análisis. Escritura: agregar y cambiar reglas                                                          | Leer           | `MaxBpaAccess`              | `McpMaxBpaAccess`                |
| Documentos             | Lectura: el contenido de los documentos abiertos de C# Script, de consultas DAX y de scripts DAX. Escritura: crearlos y sobrescribirlos | Escribir       | `MaxDocumentsAccess`        | `McpMaxDocumentsAccess`          |
| Macros                 | Lectura: la biblioteca de macros del usuario, incluido el código de las macros                                                                                          | Escribir       | `MaxMacrosAccess`           | `McpMaxMacrosAccess`             |

En los niveles predeterminados, las funcionalidades de IA leen la definición del modelo, ejecutan el Best Practice Analyzer, leen la biblioteca de macros y leen y sobrescriben los documentos de scripts y consultas abiertos. No leen valores de datos ni cambian el modelo. El código de macros y los documentos abiertos pueden contener cadenas de conexión y otras credenciales. Configura `MaxMacrosAccess` y `MaxDocumentsAccess` si eso ocurre en tu organización.

El Asistente de IA y el servidor MCP aplican los permisos de la siguiente manera:

- **Asistente de IA.** Cuando una solicitud necesita un acceso que el permiso permanente no cubre, aparece una tarjeta de permisos en el chat. El usuario puede permitirlo para este turno, para la sesión o siempre; y, en **Metadatos del modelo** y **Datos del modelo**, también para el modelo actual. No aparece ninguna tarjeta para un acceso que supere un límite de permisos.
- **Servidor MCP.** No aparece ningún aviso. El servidor lee los permisos permanentes al iniciarse, y las herramientas que esos permisos no cubren no se ofrecen al agente. Los permisos que concedas para un modelo o una sesión se aplican solo al chat.

Un límite de permisos tiene prioridad sobre cualquier permiso que concedas, incluidos los que concedas para un modelo y los que hayas concedido antes de establecer la directiva; además, la configuración correspondiente solo ofrece los niveles hasta ese límite. Un límite `McpMax...` solo reduce el límite compartido para el servidor MCP. Consulta [Permisos y consentimiento](xref:ai-assistant#permissions-and-consent).

## Protecciones para los cambios del modelo

Las funciones de IA ejecutan scripts que cambian un modelo solo cuando **Metadatos del modelo** están en **Escritura**. Todos los cambios pasan por el [motor de C# Script](xref:csharp-scripts) sobre el modelo cargado en Tabular Editor 3:

- Los cambios de un script forman una sola entrada de deshacer, llamada **C# Script (AI Assistant)** o **C# Script (MCP)**.
- Un script que falla a mitad de ejecución se revierte por completo.
- El Asistente de IA ejecuta scripts solo cuando el usuario activa **Permitir que el asistente de IA ejecute C# Scripts directamente**, que está desactivada de forma predeterminada. Con **Vista previa de los cambios** activada, que es la opción predeterminada, un cuadro de diálogo de vista previa muestra los cambios de cada ejecución del script, y el usuario los acepta o los cancela. Ambas opciones son preferencias del usuario y no hay ninguna directiva para bloquearlas.
- Al seleccionar **Ejecutar** en un script que el Asistente de IA escribe en el chat, este se ejecuta como si fuera un script tuyo, con cualquier nivel de **Metadatos del modelo**. Se aplica la comprobación de seguridad; no se aplican las restricciones sobre `ReadFile` ni sobre los métodos auxiliares de DAX que se indican a continuación.
- Los scripts de un agente MCP se ejecutan sin cuadro de diálogo de vista previa. Después, el usuario revisa los cambios en el **Explorador TOM** y en la vista **Propiedades**, que marcan todos los cambios no guardados.
- Los cambios permanecen sin guardar en el modelo cargado hasta que el usuario los guarde. Ninguna herramienta de IA guarda ni implementa un modelo. Los enlaces en las respuestas del asistente pueden iniciar comandos de Tabular Editor, incluidos **Save** y **Deploy**, cuando el usuario los selecciona. Si el usuario abrió el modelo mediante una conexión en vivo a Analysis Services o a un Workspace de Power BI, al guardar se escriben los cambios en ese servidor.
- No se ejecuta ningún script que use el sistema de archivos, la red o un ensamblado externo. El Asistente de IA lo muestra con una insignia **Unsafe** y el comando **Execute** deshabilitado. Para un agente MCP, se abre como un documento de revisión o se rechaza cuando **Documents** está por debajo de **Write**.
- La comprobación de seguridad analiza el script compilado. La reflexión, los árboles de expresiones, `Activator`, `AppDomain`, los lectores XML y la deserialización se consideran inseguros.
- En un script que ejecute el Asistente de IA o un agente MCP, `ReadFile`, `SaveFile`, `Bpa.ExportCsv`, `ExecuteCommand`, las llamadas que ejecutan una macro y las llamadas a Semantic Bridge siempre fallan. `ExecuteCommand` envía comandos de Tabular Model Scripting Language (TMSL) y XML for Analysis (XMLA) al servidor.
- En esos mismos scripts, los métodos auxiliares de DAX requieren **Model data** en **Read**, igual que la herramienta de consultas DAX.

La directiva `BlockUnsafeScripts` aplica la misma comprobación de seguridad a todos los scripts y macros: del usuario, del Best Practice Analyzer, del Asistente de IA, del servidor MCP o de la CLI de Tabular Editor. `DisableCSharpScripts` desactiva los documentos de C# Script y elimina del Asistente de IA la herramienta que ejecuta scripts, y del servidor MCP ambas herramientas de scripts. Las macros siguen ejecutándose a menos que también se establezca `DisableMacros`. Consulta [Cómo un agente cambia tu modelo](xref:mcp-server#how-an-agent-changes-your-model).

## Controles del administrador

Los administradores aplican estos controles mediante la directiva de grupo de Windows, con las plantillas administrativas incluidas en Tabular Editor 3 o escribiendo directamente valores del Registro. Consulta @policies para conocer las claves del Registro, los tipos de valor y la configuración de las plantillas.

Una directiva en `HKEY_LOCAL_MACHINE` tiene prioridad sobre el mismo valor en `HKEY_CURRENT_USER`. Los usuarios estándar no pueden cambiar ninguna de las dos claves `Software\\Policies`. Tabular Editor 3 lee las directivas al iniciarse, y el servidor MCP lee las concesiones de permisos al iniciarse, por lo que un cambio de directiva surte efecto en una sesión en ejecución después de que el usuario reinicie Tabular Editor 3.

Las directivas de la Edición Enterprise se aplican a las licencias Enterprise, Consultancy y Trial. En Desktop y en la Edición Business, los administradores pueden desactivar las funciones de IA, exigir el token de acceso de MCP, desactivar los scripts de C# Script y las macros, y desactivar la telemetría. En las tablas siguientes, **All** significa todas las ediciones de Tabular Editor 3.

### Desactivar las funciones de IA

| Requisito                                               | Directiva          | Edición |
| ------------------------------------------------------- | ------------------ | ------- |
| Sin funciones de IA y sin el componente de IA instalado | `DisableAi`        | Todas   |
| Sin asistente de IA; se permite el servidor MCP         | `DisableAiChat`    | Todas   |
| Sin servidor MCP; se permite el asistente de IA         | `DisableMcpServer` | Todas   |

`DisableAi` también borra cualquier configuración del proveedor almacenada, incluida la clave de la API. Consulta [Implementación sin funciones de IA](xref:installation-activation-basic#deploying-without-the-ai-features).

La versión portátil de Tabular Editor 3 no tiene ningún paso de instalación. Respeta `DisableAi` en tiempo de ejecución. Use el control de aplicaciones, como AppLocker o Windows Defender Application Control, si los usuarios no deben ejecutar versiones anteriores.

### Limitar el alcance de las funciones de IA

| Requisito                                                            | Directiva                                                                                                              | Edición    |
| -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ---------- |
| Un límite por recurso para ambas funciones                           | `MaxModelMetadataAccess`, `MaxModelDataAccess`, `MaxBpaAccess`, `MaxDocumentsAccess`, `MaxMacrosAccess`                | Enterprise |
| Un límite mínimo por recurso para los agentes MCP                    | `McpMaxModelMetadataAccess`, `McpMaxModelDataAccess`, `McpMaxBpaAccess`, `McpMaxDocumentsAccess`, `McpMaxMacrosAccess` | Enterprise |
| Impedir que los agentes MCP usen herramientas concretas              | `McpDisabledTools`                                                                                                     | Enterprise |
| Sin documentos de C# Script, herramientas de scripts de IA ni macros | `DisableCSharpScripts` y `DisableMacros`                                                                               | Todas      |
| Solo C# Scripts que superen la comprobación de seguridad             | `BlockUnsafeScripts`                                                                                                   | Enterprise |

Extrae los nombres de las herramientas para `McpDisabledTools` de los registros `tool_call` del registro de auditoría.

### Restringir el proveedor de IA

| Requisito                                                        | Directiva                         | Edición    |
| ---------------------------------------------------------------- | --------------------------------- | ---------- |
| Un proveedor aprobado                                            | `AiProvider`                      | Enterprise |
| Un punto de conexión o un Gateway aprobados                      | `AiEndpoint`                      | Enterprise |
| Un modelo aprobado o una implementación de Azure OpenAI aprobada | `AiModel`                         | Enterprise |
| Facturación a una organización o proyecto de OpenAI aprobados    | `AiOrganizationId`, `AiProjectId` | Enterprise |
| Una lista de proveedores aprobados                               | `AiAllowedProviders`              | Enterprise |
| Una lista de hosts de endpoints aprobados                        | `AiAllowedEndpointHosts`          | Enterprise |

`AiProvider`, `AiEndpoint`, `AiModel`, `AiOrganizationId` y `AiProjectId` sustituyen la configuración del usuario, y `AiProvider` establecido en `None` desactiva el Asistente de IA. Si la configuración infringe `AiAllowedProviders` o `AiAllowedEndpointHosts`, el Asistente de IA no envía la solicitud y se muestra un error que indica el proveedor o el host del endpoint. `AiAllowedEndpointHosts` solo valida el endpoint que introduce el usuario, por lo que OpenAI y Anthropic, sin un endpoint personalizado, acceden a su API pública independientemente de lo que contenga la lista. Combínalo con `AiProvider` o `AiAllowedProviders`. Ninguna directiva exige HTTPS; restringe `AiEndpoint` a una dirección `https://`. Las directivas no distribuyen claves de API. Con el endpoint restringido a un recurso propiedad de su organización, como un recurso de Azure OpenAI o un Gateway interno, solo funcionan las claves emitidas por su organización. Con un endpoint público como `api.openai.com`, los usuarios pueden introducir una clave personal. Estas directivas se aplican solo al Asistente de IA.

### Instrucciones personalizadas y el puerto MCP

| Requisito                                                                          | Directiva                       | Edición    |
| ---------------------------------------------------------------------------------- | ------------------------------- | ---------- |
| Instrucciones personalizadas aprobadas por la organización para todos los usuarios | `AiCustomInstructionsPath`      | Enterprise |
| Ignorar las instrucciones personalizadas escritas por los propios usuarios         | `DisableUserCustomInstructions` | Enterprise |
| Los agentes MCP se autentican con un token de acceso                               | `RequireMcpAccessToken`         | Todas      |
| Un puerto fijo para el servidor MCP                                                | `McpPort`                       | Enterprise |

### Directivas de la edición Enterprise en otras ediciones

Si hay algún valor de directiva de Enterprise presente en un equipo cuya licencia no sea Enterprise, el Asistente de IA y el servidor MCP no se inician, y un valor de `BlockUnsafeScripts` impide que se ejecute cualquier script o macro. Un valor que Tabular Editor 3 no pueda interpretar deniega el recurso cuando existe un límite de permisos, hace que el Asistente de IA no esté disponible para `AiProvider` y aplica `BlockUnsafeScripts`. Cualquier otro valor no válido se ignora y la configuración que controla permanece sin restricciones. Implementa las directivas Enterprise solo en equipos que tengan la licencia correspondiente. Consulta [Qué ocurre sin la Edición Enterprise](xref:policies#what-happens-without-enterprise-edition).

Para comprobar qué directivas se aplican en un equipo, abre **Herramientas > Preferencias > Tabular Editor > Actualizaciones y comentarios**. La sección **Administrado por tu organización** enumera todos los valores de directiva encontrados, su clave de origen y cualquier valor marcado como **(no válido)**.

## Registro de auditoría

En la Edición Enterprise, Tabular Editor 3 escribe un registro local de la actividad del Asistente de IA y del servidor MCP en un archivo JSON Lines distinto cada día. Cada registro incluye una marca de tiempo UTC, la característica (`chat` o `mcp`), la sesión y, cuando corresponda, el nombre del modelo abierto, así como el nombre de usuario de Windows. No se registra nada antes de que se active una licencia.

El registro incluye:

- las solicitudes de permisos y la respuesta del usuario
- cada llamada a una herramienta, con el nombre de la herramienta, los permisos que necesitó, su resultado (`ok`, `error`, `denied` o `cancelled`), su duración y los nombres y el tamaño total de sus argumentos
- cada C# Script enviado para ejecutarse —incluidos los C# Scripts que fallaron en tiempo de ejecución, los que se rechazaron o los que se devolvieron para revisión— se guarda como un archivo `.csx` con su hash SHA-256
- el proveedor, el modelo, el host del punto de conexión y el recuento de tokens de cada turno del chat
- Cambios en la configuración de la IA
- Inicio y detención del servidor MCP, con el nivel de permisos de cada recurso
- Conexiones del agente MCP, con el nombre y la versión que informa el cliente

No se registran el texto del prompt, el texto de la respuesta, los valores de los argumentos, los valores de datos del modelo, las claves de API ni los tokens de acceso. No se guardan los scripts que no se pueden compilar ni los scripts que las funciones de IA escriben en un documento para que los ejecutes.

Los archivos con más de 30 días se eliminan, a menos que `AiAuditLogRetentionDays` establezca otro período; `0` conserva todos los archivos. Cada copia de Tabular Editor 3 elimina los archivos caducados de la carpeta en la que escribe antes de escribir su primer registro en una sesión.

El registro lo escribe tu propio proceso de Tabular Editor 3, por lo que tienes permisos de escritura y eliminación, incluso en un recurso compartido redirigido. Si no se puede escribir el registro, por ejemplo, porque no se puede acceder al recurso compartido, el AI Assistant y el servidor MCP siguen funcionando, y el error se registra una sola vez en el registro de la aplicación de Tabular Editor.

`AiAuditLogPath` redirige el registro. Se omite una ruta relativa. Los nombres de archivo diarios y los nombres de archivo de scripts no incluyen el nombre del usuario ni el del equipo, así que asigna una carpeta independiente a cada usuario. Las variables de entorno, como `%USERNAME%`, se expanden solo en un valor `REG_EXPAND_SZ`; la plantilla administrativa escribe `REG_SZ`, que se usa tal cual.

Consulta @ai-audit-log para ver el formato del registro.

## Línea de base recomendada

La siguiente línea de base sirve de orientación para una organización que permite el desarrollo de modelos asistido por IA y mantiene los datos del modelo fuera del alcance de los proveedores de IA. Ajústala a tu propia evaluación de riesgos.

| Control                   | Configuración                                                                                                                                                                                               | Efecto                                                                                                                  |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Proveedor                 | `AiProvider`, `AiEndpoint`, `AiModel` y `AiAllowedEndpointHosts` configurados para apuntar a un recurso propiedad de tu organización y para el que tu organización tenga un acuerdo de tratamiento de datos | El AI Assistant envía solicitudes solo a ese punto de conexión, con claves emitidas por tu organización                 |
| Datos del modelo          | `MaxModelDataAccess` establecido en `Deny`                                                                                                                                                                  | Ningún resultado de consulta DAX llega al Asistente de IA ni a un agente MCP                                            |
| Macros                    | `MaxMacrosAccess` establecido en `Deny`                                                                                                                                                                     | El código de la macro no se envía a un proveedor de IA                                                                  |
| Secuencias de comandos    | `BlockUnsafeScripts` establecido en `1`                                                                                                                                                                     | Ninguna secuencia de comandos ni macro escribe archivos, accede a la red, inicia otros programas o carga código externo |
| Autenticación de MCP      | `RequireMcpAccessToken` establecido en `1`                                                                                                                                                                  | Solo los clientes con el token de acceso del usuario se conectan al servidor MCP                                        |
| Retención de auditoría    | `AiAuditLogRetentionDays` establecido según tus requisitos de retención                                                                                                                                     | Los archivos de auditoría se conservan durante ese período                                                              |
| Ubicación de la auditoría | `AiAuditLogPath` establecido por usuario en una carpeta de un recurso compartido                                                                                                                            | Los archivos de auditoría se recopilan de forma centralizada                                                            |

El siguiente archivo del Registro aplica la parte de la línea base para toda la máquina. Restringe el Asistente de IA a un recurso de Azure OpenAI y conserva los archivos de auditoría durante 365 días. Sustituye el punto de conexión y el nombre de la implementación por los tuyos, y aplica el archivo solo a equipos con licencia para la Edición Enterprise:

```ini
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Tabular Editor ApS]
"BlockUnsafeScripts"=dword:00000001

[HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Tabular Editor ApS\TE3]
"AiProvider"="AzureOpenAI"
"AiEndpoint"="https://contoso-ai.openai.azure.com"
"AiModel"="tabular-editor-assistant"
"AiAllowedEndpointHosts"="contoso-ai.openai.azure.com"
"MaxModelDataAccess"="Deny"
"MaxMacrosAccess"="Deny"
"RequireMcpAccessToken"=dword:00000001
"AiAuditLogRetentionDays"=dword:0000016d
```

`BlockUnsafeScripts` está en la clave compartida, por lo que la CLI de Tabular Editor también lo aplica. Configura `AiAuditLogPath` en una carpeta para cada usuario: ya sea un valor `REG_EXPAND_SZ`, como `\\fileserver\te-audit$\%USERNAME%`, en la clave `HKEY_LOCAL_MACHINE`, o un valor `REG_SZ` por usuario en `HKEY_CURRENT_USER\SOFTWARE\Policies\Tabular Editor ApS\TE3`.

## Preguntas frecuentes

### ¿Recibe Tabular Editor ApS nuestros prompts, metadatos o datos?

No. Consulta [Flujo de datos](#data-flow).

### ¿Se utilizan nuestros datos para entrenar modelos de IA?

Tabular Editor ApS no recibe solicitudes, respuestas ni contenido del modelo. El acuerdo con el proveedor de IA determina si el proveedor entrena con las solicitudes.

### ¿Dónde se procesan nuestros datos?

En el punto de conexión configurado del Asistente de IA y allí donde se ejecute el proveedor de un agente MCP. Consulta [Restringir el proveedor de IA](#restrict-the-ai-provider).

### ¿Pueden los usuarios eludir una directiva?

Un usuario no puede cambiar una directiva sin derechos de administrador local. Las versiones anteriores a 3.27.0, incluidas las compilaciones portátiles antiguas, solo leen `HKEY_CURRENT_USER\Software\Policies\Kapacity\Tabular Editor` e ignoran todas las directivas de esta página. Consulta [Desactivar las funciones de IA](#turn-the-ai-features-off).

### ¿Pueden las funciones de IA modificar o desplegar un modelo en producción?

Solo ejecutan scripts en el modelo cargado si **Model metadata** está en **Write**, y solo el usuario puede guardar o desplegar. Consulta [Medidas de protección para los cambios del modelo](#safeguards-on-model-changes).

### ¿Pueden las funciones de IA leer datos de nuestros modelos?

Los resultados de las consultas DAX requieren que **Model data** esté en **Read**, y el valor predeterminado es **Deny**. Los valores escritos en la definición del modelo forman parte de los metadatos. Consulta [Flujo de datos](#data-flow).

### ¿Puede un agente MCP usar un proveedor que no hayamos aprobado?

Sí. Administra el agente mediante sus propios controles administrativos o establece `DisableMcpServer`. Consulta [Servidor MCP](#mcp-server).

### ¿Cómo podemos detener las funciones de IA durante un incidente?

Establece `DisableAi` y pide a los usuarios que reinicien Tabular Editor 3. Revoca las claves de API afectadas en el proveedor. Consulta [Desactivar las funciones de IA](#turn-the-ai-features-off).

### ¿El registro de auditoría permite detectar si se ha manipulado?

No. El usuario puede modificar y eliminar sus propios archivos de auditoría. Consulta el [registro de auditoría](#audit-log).

## Ver también

- @ai-assistant
- @mcp-server
- @ai-audit-log
- @policies
- @security-privacy
- @editions
