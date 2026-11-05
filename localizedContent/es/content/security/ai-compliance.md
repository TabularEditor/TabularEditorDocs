---
uid: ai-compliance
title: Guía de cumplimiento normativo de las funciones de IA
author: Morten Lønskov
updated: 2026-10-23
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.27.0
      editions:
        - edition: Desktop
          partial: true
          note: "General policies only. No permission limits, provider lock or audit log"
        - edition: Business
          partial: true
          note: "General policies only. No permission limits, provider lock or audit log"
        - edition: Enterprise
          full: true
---

# Guía de cumplimiento normativo de las funciones de IA

El [asistente de IA](xref:ai-assistant) y el [servidor del Protocolo de Contexto de Modelo (MCP)](xref:mcp-server) de Tabular Editor 3 permiten a los modelos de IA acceder al modelo semántico abierto, dentro de los límites de los permisos que los administradores establecen mediante políticas de grupo y que la Edición Enterprise registra en un registro de auditoría. Esta página está dirigida a los equipos de TI, seguridad y cumplimiento normativo que aprueban estas funciones para una organización.

## Las funciones de IA

| Función | Qué hace | Qué llama al proveedor de IA | Tráfico de red |
| -- | -- | -- | -- |
| Asistente de IA | Un panel de chat en Tabular Editor 3 que lee, consulta y modifica el modelo semántico abierto | Tabular Editor 3, desde el equipo del usuario, con una clave de API que introduce el usuario | Saliente hacia el punto de conexión del proveedor configurado |
| Servidor MCP | Un servidor local al que se conecta un agente de IA que el usuario ya ejecuta, como Claude Code, GitHub Copilot, Codex o Cursor. A continuación, el agente lee, consulta y modifica el modelo semántico abierto | El agente, con su propia configuración y suscripción | Tráfico entrante solo en `127.0.0.1` |

Ambas funciones se incluyen en el componente de funciones de IA, que forma parte de la instalación predeterminada de Tabular Editor 3.27.0. Comparten las concesiones de permisos, las políticas de administrador y el registro de auditoría, con las diferencias descritas en [Concesiones de permisos](#permission-grants).

Tabular Editor ApS no gestiona ningún servicio de IA y no incluye ninguna clave de API. Las indicaciones, las respuestas, los metadatos del modelo y los datos del modelo de cualquiera de las dos funciones nunca pasan por los servidores de Tabular Editor. Con la telemetría activada, Tabular Editor 3 envía eventos de uso de la IA a Tabular Editor ApS con el proveedor, el nombre del modelo, un ID de conversación y el número de «tokens». En el caso del servidor MCP, los eventos incluyen el nombre de la herramienta, el resultado y la duración de cada llamada a la herramienta, así como el nombre y la versión del cliente MCP si se trata de un cliente conocido. No se envían los argumentos de las herramientas, los resultados de las herramientas ni los mensajes de error. La directiva `DisableTelemetry` los desactiva.

El [Centro de confianza de Tabular Editor](https://trust.tabulareditor.com/) publica el informe de la prueba de penetración independiente para el Asistente de IA, el informe de auditoría SOC 2 y la lista de subencargados del tratamiento.

## Flujo de datos

### Asistente de IA

El Asistente de IA envía solicitudes directamente desde el equipo del usuario al proveedor configurado en **Herramientas > Preferencias > Funciones de IA > Asistente de IA**: OpenAI, Anthropic, Azure OpenAI o cualquier punto de conexión compatible con OpenAI, incluido un modelo alojado en su propia red. La autenticación se realiza únicamente mediante clave de API. Consulte [Proveedores compatibles](xref:ai-assistant#supported-providers).

Una solicitud al proveedor contiene:

- la indicación del sistema y las instrucciones personalizadas vigentes, incluidas las que publique tu organización
- los mensajes del usuario y el historial de la conversación
- contexto sobre el modelo abierto añadido a los mensajes del usuario: el nombre de la base de datos, el número de objetos, la selección actual, el título del documento activo, los errores del modelo y los cambios recientes. El ajuste **Metadatos del modelo** de un usuario no los retiene; un límite de `MaxModelMetadataAccess` de `Deny` sí lo hace.
- los resultados de las herramientas que el asistente ha llamado, dentro de los [permisos concedidos](#permission-grants)
- pasajes de la base de conocimientos de Tabular Editor, una base de datos local creada a partir de la documentación de Tabular Editor, el blog, los problemas de GitHub y los debates

Los metadatos del modelo abarcan toda la definición del modelo: nombres de objetos, descripciones y anotaciones, expresiones DAX y M, consultas de orígenes de particiones, detalles de conexión de orígenes de datos, roles, miembros de roles y filtros de seguridad a nivel de fila. Los valores introducidos en la definición del modelo, como una expresión `DATATABLE` o una tabla **Introducir datos**, forman parte de los metadatos.

El texto de estas fuentes pasa a formar parte de la solicitud e influye en lo que hace el asistente. Limite el acceso de escritura a una carpeta de instrucciones personalizadas de la organización a las personas que aprueban su contenido.

El acuerdo de su organización con el proveedor rige la retención, la región en la que se procesan los datos y si el proveedor utiliza las solicitudes para entrenar el modelo. Para seguir procesando en un inquilino de Azure o en una red gestionada por su organización, utilice Azure OpenAI, [Microsoft Foundry](xref:ai-assistant#using-microsoft-foundry) o un [modelo autoalojado](xref:ai-assistant#using-a-local-or-organizational-llm), y bloquee la configuración mediante una [política](#restrict-the-ai-provider).

### Servidor MCP

El servidor MCP es un «listener» HTTP vinculado a `127.0.0.1`, en el puerto 42100 de forma predeterminada. No tiene clave de API, no realiza solicitudes salientes y rechaza las solicitudes del navegador con un encabezado `Origin` no local.

El agente conectado envía lo que lee de Tabular Editor 3 a su propio proveedor, según la configuración del agente y las condiciones del proveedor. Tabular Editor 3 no tiene ningún ajuste para el proveedor del agente, por lo que debes controlar al agente a través de sus propios controles administrativos. Las propias herramientas del agente, como el acceso a archivos y al shell, también están fuera de Tabular Editor 3. La preferencia **Detalle del origen del modelo** establece qué parte de la ruta del archivo o del servidor del modelo recibe el agente junto con el nombre del modelo, y no cambia los detalles de la conexión en los metadatos del modelo. Consulte [Comprobar que ha funcionado](xref:mcp-server#check-that-it-worked). Los archivos de modelo en el disco, los archivos de conversación y los archivos de auditoría pueden ser leídos por cualquier agente que se ejecute como el usuario.

La opción **Requerir token de acceso** está desactivada de forma predeterminada. Mientras esté desactivada, cualquier proceso del equipo puede conectarse al servidor sin credenciales, incluidos los procesos de las sesiones de otros usuarios en un Escritorio remoto o en un host Citrix. La política `RequireMcpAccessToken` impone el token para todos los usuarios. Los archivos de registro del agente almacenan el token en texto plano, y la opción **Regenerar token** en el cuadro de diálogo **Herramientas > Servidor MCP...** invalida todos los registros existentes. Consulte [Ejecución en un equipo compartido](xref:mcp-server#running-on-a-shared-machine).

### Puntos de conexión de red

Permite estos puntos finales a través de tu cortafuegos o proxy para las funciones de IA:

| Tráfico | Punto de conexión |
| -- | -- |
| Solicitudes del Asistente de IA | El punto de conexión del proveedor configurado, por ejemplo, `https://api.openai.com`, `https://api.anthropic.com`, un recurso de Azure OpenAI o tu propia pasarela |
| Catálogo de modelos de IA | `https://api.tabulareditor.com/AiModels`. Una solicitud anónima de la lista de modelos, realizada cuando un usuario abre la lista de modelos de OpenAI o Anthropic. La lista se almacena en caché durante 24 horas. `DisableUpdates` la desactiva |
| Actualizaciones de la base de conocimientos de IA | `https://cdn.tabulareditor.com`. Una comprobación como máximo una vez al día mientras el asistente de IA esté configurado, sin datos sobre el usuario ni el modelo. Ninguna directiva lo desactiva, excepto `DisableAi`. Los usuarios desmarcan **Buscar actualizaciones de la base de conocimientos al iniciar** en **Herramientas > Preferencias > Funciones de IA > Asistente de IA** |
| Servidor MCP | Ninguno |

La validación de licencias, las comprobaciones de actualizaciones y la telemetría utilizan solicitudes separadas. Consulte [Solicitudes web](xref:security-privacy#web-requests).

### Datos almacenados en el equipo del usuario

Todas las rutas se encuentran en `%LocalAppData%\TabularEditor3`, a menos que se indique lo contrario.

| Elemento | Ubicación | Formato |
| -- | -- | -- |
| Clave de API del proveedor | `Preferences.json` | Cifrada con la API de protección de datos de Windows para el usuario actual. Se borra cuando el componente de IA no está cargado o se establece `DisableAi` |
| Token de acceso MCP | `Preferences.json` | Cifrado con la API de protección de datos de Windows para el usuario actual |
| Concesiones de permisos permanentes | `Preferences.json` | JSON |
| Concesiones de permisos por modelo | El archivo de [opciones de usuario](xref:user-options) (`.tmuo`) del modelo: junto a un modelo cargado desde archivos o en `UserOptions` para un modelo abierto desde un servidor | JSON |
| Conversaciones | `AI\Conversations` | JSON sin cifrar. Contiene indicaciones, respuestas y resultados de herramientas, incluidas las filas de consultas DAX y el texto de error de Analysis Services cuando **Datos del modelo** está en **Lectura**. Las copias archivadas se escriben antes de cada compactación. Los archivos permanecen hasta que el usuario elimina la conversación |
| Instrucciones personalizadas del usuario | `AI\CustomInstructions` | Markdown |
| Base de conocimientos | `kb.sqlite` | Base de datos SQLite |
| Catálogo de modelos de IA | `AiModels.json` | JSON |
| Registro de auditoría | `AI\audit` o la carpeta establecida por `AiAuditLogPath` | Consulte [Registro de auditoría](#audit-log) |

## Concesiones de permisos

Las concesiones de permisos controlan a qué acceden el asistente de IA y el servidor MCP, con un nivel de acceso por recurso. El usuario establece cada nivel en **Herramientas > Preferencias > Funciones de IA > Permisos**. En la Edición Enterprise, un administrador puede establecer un límite de permisos para cada recurso mediante una directiva:

| Recurso | A qué acceden las funciones de IA | Predeterminado | Límite para ambas funciones | Límite solo para el servidor MCP |
| -- | -- | -- | -- | -- |
| Metadatos del modelo | Lectura: la definición del modelo, las estadísticas del Analizador VertiPaq y los errores y advertencias del modelo. El texto del error del servidor también necesita **Datos del modelo > Lectura**. Escritura: modificación del modelo mediante scripts de C# | Lectura | `MaxModelMetadataAccess` | `McpMaxModelMetadataAccess` |
| Datos del modelo | Lectura: resultados de consultas DAX y texto de los errores devueltos por Analysis Services, que pueden contener valores de datos del modelo | Denegar | `MaxModelDataAccess` | `McpMaxModelDataAccess` |
| Best Practice Analyzer | Lectura: reglas y resultados del análisis. Escritura: añadir y cambiar reglas | Lectura | `MaxBpaAccess` | `McpMaxBpaAccess` |
| Documentos | Lectura: el contenido de los documentos abiertos de scripts de C#, consultas DAX y scripts DAX, así como los errores y las advertencias de los documentos abiertos, incluidas las tablas dinámicas. Escritura: crearlos y sobrescribirlos | Escritura | `MaxDocumentsAccess` | `McpMaxDocumentsAccess` |
| Macros | Lectura: la biblioteca de macros del usuario, incluido el código de las macros | Escritura | `MaxMacrosAccess` | `McpMaxMacrosAccess` |

En los niveles predeterminados, las funciones de IA leen la definición del modelo, ejecutan Best Practice Analyzer, leen la biblioteca de macros y leen y sobrescriben los documentos de script y de consultas abiertos. No leen los valores de los datos ni cambian el modelo. El código de las macros y los documentos abiertos pueden contener cadenas de conexión y otras credenciales. Establece `MaxMacrosAccess` y `MaxDocumentsAccess` si es el caso en tu organización.

El asistente de IA y el servidor MCP aplican los permisos de la siguiente manera:

- **Asistente de IA.** Cuando una solicitud necesita un acceso que no cubre el permiso permanente, aparece una tarjeta de permiso en el chat. El usuario lo permite para el turno, para la sesión o siempre, y para **Metadatos del modelo** y **Datos del modelo** también para el modelo actual. No aparece ninguna tarjeta para el acceso por encima de un límite de permisos.
- **Servidor MCP.** No aparece ningún mensaje. El servidor lee los permisos permanentes cuando se inicia, y las herramientas que un permiso no cubre no se ofrecen al agente. Los permisos concedidos para un modelo o una sesión se aplican únicamente al chat.

Un límite de permisos prevalece sobre todas las concesiones de los usuarios, incluidas las concesiones otorgadas para un modelo y las concesiones otorgadas antes de establecer la política, y el ajuste correspondiente ofrece solo los niveles hasta el límite. Un límite `McpMax...` solo reduce el límite compartido para el servidor MCP. Consulta [Permisos y consentimiento](xref:ai-assistant#permissions-and-consent).

## Medidas de protección ante cambios en el modelo

Las funciones de IA ejecutan scripts que modifican un modelo solo cuando los **Metadatos del modelo** están en **Escritura**. Cada cambio se ejecuta a través del [motor de scripting de C#](xref:csharp-scripts) en el modelo cargado en Tabular Editor 3:

- Los cambios de un script forman una entrada de deshacer, denominada **Script de C# (Asistente de IA)** o **Script de C# (MCP)**.
- Un script que falla a mitad de camino se revierte por completo.
- El asistente de IA ejecuta scripts solo cuando el usuario activa **Permitir que el asistente de IA ejecute C# Scripts directamente**, que está desactivado de forma predeterminada. Con la opción **Vista previa de los cambios** activada, que es la configuración predeterminada, un cuadro de diálogo de vista previa muestra los cambios de cada ejecución de script y el usuario los acepta o los cancela. Ambos ajustes son preferencias del usuario, sin ninguna directiva que los bloquee.
- **Ejecutar** en un script que el Asistente de IA escribe en el chat lo ejecuta como el propio script del usuario, en cualquier nivel de **Metadatos del modelo**. Se aplica la comprobación de seguridad; las restricciones de `ReadFile` y los métodos auxiliares de DAX que se indican a continuación no se aplican.
- Los scripts de un agente MCP se ejecutan sin un cuadro de diálogo de vista previa. El usuario revisa los cambios posteriormente en el **Explorador TOM** y en la vista **Propiedades**, que marcan todos los cambios no guardados.
- Los cambios permanecen sin guardar en el modelo cargado hasta que el usuario los guarda. Ninguna herramienta de IA guarda ni implementa un modelo. Los enlaces de las respuestas del asistente pueden iniciar comandos de Tabular Editor, incluidos **Guardar** e **Implementar**, cuando el usuario los selecciona. Si el usuario ha abierto el modelo a través de una conexión en tiempo real a Analysis Services o a un área de trabajo de Power BI, al guardar, los cambios se escriben en ese servidor.
- No se ejecuta un script que utilice el sistema de archivos, la red o un ensamblado externo. El asistente de IA lo muestra con una insignia de **No seguro** y con **Ejecutar** desactivado. En el caso de un agente MCP, se abre como documento de revisión o se rechaza cuando **Documentos** está por debajo de **Escritura**.
- La comprobación de seguridad analiza el script compilado. La reflexión, los árboles de expresiones, `Activator`, `AppDomain`, los lectores XML y la deserialización se consideran inseguros.
- En un script que ejecuta el Asistente de IA o un agente MCP, `ReadFile`, `SaveFile`, `Bpa.ExportCsv`, `ExecuteCommand`, las llamadas que ejecutan una macro y las llamadas de Semantic Bridge siempre fallan. `ExecuteCommand` envía al servidor comandos del lenguaje de scripting de modelo tabular (TMSL) y de XML for Analysis (XMLA).
- En los mismos scripts, los métodos auxiliares de DAX requieren **Datos del modelo** en **Lectura**, al igual que la herramienta de consultas DAX.

La política `BlockUnsafeScripts` aplica la misma comprobación de seguridad a todos los scripts y macros: del usuario, de Best Practice Analyzer, del asistente de IA, del servidor MCP o de Tabular Editor CLI. `DisableCSharpScripts` desactiva los documentos de script de C# y elimina la herramienta que ejecuta los scripts del Asistente de IA y ambas herramientas de script del servidor MCP. Las macros siguen ejecutándose, a menos que también se establezca `DisableMacros`. Consulta [Cómo cambia un agente tu modelo](xref:mcp-server#how-an-agent-changes-your-model).

## Controles del administrador

Los administradores aplican los controles a través de la política de grupo de Windows, con las plantillas administrativas que se incluyen con Tabular Editor 3 o escribiendo directamente los valores del registro. Consulta @policies para conocer las claves del registro, los tipos de valores y la configuración de las plantillas.

Una política bajo `HKEY_LOCAL_MACHINE` tiene prioridad sobre el mismo valor bajo `HKEY_CURRENT_USER`. Los usuarios estándar no pueden cambiar ninguna de las claves `Software\Policies`. Tabular Editor 3 lee las políticas cuando se inicia, y el servidor MCP lee las concesiones de permisos cuando se inicia, por lo que un cambio de política llega a una sesión en ejecución después de que el usuario reinicie Tabular Editor 3.

Las políticas de la Edición Enterprise se aplican a las licencias Enterprise, Consultancy y Trial. En las ediciones Desktop y Business, los administradores pueden desactivar las funciones de IA, aplicar el token de acceso MCP, desactivar los scripts y las macros de C# y desactivar la telemetría. En las siguientes tablas, **Todas** significa todas las ediciones de Tabular Editor 3.

### Desactivar las funciones de IA

| Requisito | Política | Edición |
| -- | -- | -- |
| Sin funciones de IA, y el componente de IA excluido de las nuevas instalaciones y eliminado en la actualización | `DisableAi` | Todas |
| Sin asistente de IA, servidor MCP permitido | `DisableAiChat` | Todas |
| Sin servidor MCP, asistente de IA permitido | `DisableMcpServer` | Todas |

`DisableAi` también borra cualquier configuración de proveedor almacenada, incluida la clave de API. Una instalación en la que el instalador no se ha ejecutado desde que se estableció la política mantiene los archivos de IA en el disco, y Tabular Editor 3 no los carga. Consulta [Aplicar la decisión con la directiva DisableAi](xref:installation-activation-basic#enforcing-the-decision-with-the-disableai-policy).

La compilación portátil de Tabular Editor 3 no tiene ningún paso de instalación. Respeta `DisableAi` en tiempo de ejecución. Utilice el control de aplicaciones, como AppLocker o el Control de aplicaciones de Windows Defender, si los usuarios no deben ejecutar versiones anteriores.

### Limitar el alcance de las funciones de IA

| Requisito | Política | Edición |
| -- | -- | -- |
| Un límite por recurso para ambas funciones | `MaxModelMetadataAccess`, `MaxModelDataAccess`, `MaxBpaAccess`, `MaxDocumentsAccess`, `MaxMacrosAccess` | Enterprise |
| Un límite inferior por recurso para los agentes MCP | `McpMaxModelMetadataAccess`, `McpMaxModelDataAccess`, `McpMaxBpaAccess`, `McpMaxDocumentsAccess`, `McpMaxMacrosAccess` | Enterprise |
| Retirar herramientas individuales a los agentes MCP | `McpDisabledTools` | Enterprise |
| Sin documentos de script de C#, herramientas de script de IA ni macros | `DisableCSharpScripts` y `DisableMacros` | Todos |
| Solo scripts de C# que superen la comprobación de seguridad | `BlockUnsafeScripts` | Enterprise |

Obtenga los nombres de las herramientas para `McpDisabledTools` de los registros `tool_call` del registro de auditoría.

### Restringir el proveedor de IA

| Requisito | Política | Edición |
| -- | -- | -- |
| Un proveedor aprobado | `AiProvider` | Enterprise |
| Un punto de conexión o una pasarela aprobados | `AiEndpoint` | Enterprise |
| Un modelo aprobado o una implementación de Azure OpenAI | `AiModel` | Enterprise |
| Facturación a una organización o proyecto de OpenAI aprobado | `AiOrganizationId`, `AiProjectId` | Enterprise |
| Una lista de proveedores aprobados | `AiAllowedProviders` | Enterprise |
| Una lista de hosts de puntos de conexión aprobados | `AiAllowedEndpointHosts` | Enterprise |

`AiProvider`, `AiEndpoint`, `AiModel`, `AiOrganizationId` y `AiProjectId` sustituyen la configuración del usuario, y si `AiProvider` se establece en `None`, el Asistente de IA se desactiva. Si la configuración interrumpe `AiAllowedProviders` o `AiAllowedEndpointHosts`, el asistente de IA no envía la solicitud y un error indica el nombre del proveedor o del host del punto de conexión. `AiAllowedEndpointHosts` solo comprueba un punto de conexión que introduce el usuario, por lo que OpenAI y Anthropic, sin un punto de conexión personalizado, acceden a su API pública independientemente de lo que contenga la lista. Combínelo con `AiProvider` o `AiAllowedProviders`. Ninguna política requiere HTTPS; bloquee `AiEndpoint` a una dirección `https://`. Las directivas no distribuyen claves de API. Si el punto de conexión está bloqueado para un recurso que pertenece a su organización, como un recurso de Azure OpenAI o una pasarela interna, solo funcionarán las claves que emita su organización. Con un punto de conexión público como `api.openai.com`, los usuarios pueden introducir una clave personal. Estas políticas se aplican únicamente al asistente de IA.

### Instrucciones personalizadas y el puerto MCP

| Requisito | Política | Edición |
| -- | -- | -- |
| Instrucciones personalizadas aprobadas por la organización para todos los usuarios | `AiCustomInstructionsPath` | Enterprise |
| Ignorar las instrucciones personalizadas que escriben los propios usuarios | `DisableUserCustomInstructions` | Enterprise |
| Los agentes MCP se autentican con un token de acceso | `RequireMcpAccessToken` | Todas |
| Un puerto fijo del servidor MCP | `McpPort` | Enterprise |

### Políticas de la Edición Enterprise en otras ediciones

Si hay algún valor de política Enterprise en un equipo cuya licencia no sea Enterprise, el asistente de IA y el servidor MCP no se inician, y un valor `BlockUnsafeScripts` impide que se ejecuten todos los scripts y macros. Un valor que Tabular Editor 3 no pueda interpretar deniega el recurso por un límite de permisos, hace que el Asistente de IA no esté disponible para `AiProvider` y aplica `BlockUnsafeScripts`. Cualquier otro valor no válido se ignora y el ajuste que controla permanece sin restricciones. Implemente las políticas Enterprise solo en los equipos con una licencia coincidente. Consulte [Qué sucede sin la Edición Enterprise](xref:policies#what-happens-without-enterprise-edition).

Para comprobar qué políticas se aplican en un equipo, abra **Herramientas > Preferencias > Tabular Editor > Actualizaciones y comentarios**. La sección **Gestionado por su organización** enumera todos los valores de políticas encontrados, su clave de origen y cualquier valor marcado como **(no válido)**.

## Registro de auditoría

En la Edición Enterprise, Tabular Editor 3 escribe un registro local de la actividad del Asistente de IA y del servidor MCP en un archivo JSON Lines al día. Cada registro incluye una marca de tiempo UTC, la función (`chat` o `mcp`), la sesión y el nombre del modelo abierto al que se aplican, así como el nombre de usuario de Windows. No se registra nada antes de activar una licencia.

El registro recoge:

- solicitudes de permiso y respuesta del usuario
- cada llamada a una herramienta, con el nombre de la herramienta, los permisos que necesitaba, su resultado (`ok`, `error`, `denied` o `cancelled`), su duración y los nombres y el tamaño total de sus argumentos
- Todos los scripts de C# enviados para su ejecución, incluidos los scripts que fallaron en tiempo de ejecución, fueron rechazados o devueltos para su revisión, guardados como archivo `.csx` con su hash SHA-256.
- el proveedor, el modelo, el host del punto de conexión y el número de tokens para cada turno del chat
- Cambios en la configuración de la IA
- Inicio y parada del servidor MCP, con el nivel de permiso de cada recurso
- Conexiones de agentes MCP, con el nombre y la versión que informa el cliente

No se registran el texto de la indicación, el texto de la respuesta, los valores de los argumentos, los valores de los datos del modelo, las claves de API ni los tokens de acceso. No se guardan los scripts que no se compilan ni los scripts que las funciones de IA escriben en un documento para que el usuario los ejecute.

Los archivos con más de 30 días de antigüedad se eliminan, a menos que `AiAuditLogRetentionDays` establezca otro período; si se establece `0`, se conservan todos los archivos. Cada copia de Tabular Editor 3 elimina los archivos caducados de la carpeta en la que escribe antes de escribir su primer registro en una sesión.

El registro lo escribe el propio proceso de Tabular Editor 3 del usuario, por lo que este tiene acceso de escritura y eliminación al mismo, incluso en un recurso compartido redirigido. Si no se puede escribir el registro, por ejemplo, porque no se puede acceder al recurso compartido, el asistente de IA y el servidor MCP siguen funcionando y el fallo se escribe una vez en el registro de la aplicación de Tabular Editor.

`AiAuditLogPath` redirige el registro. Se omite una ruta relativa. Los nombres de los archivos diarios y los nombres de los archivos de script no incluyen el nombre del usuario ni el de la máquina, así que asigne a cada usuario una carpeta independiente. Las variables de entorno como `%USERNAME%` solo se expanden en un valor `REG_EXPAND_SZ`; la plantilla administrativa escribe `REG_SZ`, que se usa tal como está escrito.

Consulte @ai-audit-log para conocer el formato del registro.

## Configuración básica recomendada

La siguiente línea de base es una orientación para una organización que permite el desarrollo de modelos asistidos por IA y mantiene los datos de los modelos alejados de los proveedores de IA. Ajústela a su propia evaluación de riesgos.

| Control | Configuración | Efecto |
| -- | -- | -- |
| Proveedor | `AiProvider`, `AiEndpoint`, `AiModel` y `AiAllowedEndpointHosts` establecidos en un recurso que su organización posee y para el que tiene un acuerdo de tratamiento de datos | El Asistente de IA envía solicitudes solo a ese punto de conexión, con claves emitidas por su organización |
| Datos del modelo | `MaxModelDataAccess` establecido en `Deny` | Ningún resultado de consulta DAX ni ningún texto de error de Analysis Services llega al Asistente de IA ni a un agente MCP |
| Macros | `MaxMacrosAccess` establecido en `Deny` | El código de la macro no se envía a un proveedor de IA |
| Scripts | `BlockUnsafeScripts` establecido en `1` | Ningún script ni macro escribe archivos, accede a la red, inicia otros programas ni carga código externo |
| Autenticación MCP | `RequireMcpAccessToken` establecido en `1` | Solo los clientes con el token de acceso del usuario se conectan al servidor MCP |
| Conservación de auditorías | `AiAuditLogRetentionDays` establecido según tu requisito de conservación | Los archivos de auditoría se conservan durante ese periodo |
| Ubicación de la auditoría | `AiAuditLogPath` establecido por usuario en una carpeta de un recurso compartido | Los archivos de auditoría se recopilan de forma centralizada |

El siguiente archivo de registro aplica la parte de la línea base que afecta a todo el equipo. Vincula el Asistente de IA a un recurso de Azure OpenAI y conserva los archivos de auditoría durante 365 días. Sustituya el punto de conexión y el nombre de la implementación por los suyos y aplique el archivo solo a los equipos con licencia para la Edición Enterprise:

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

`BlockUnsafeScripts` se encuentra en la clave compartida, por lo que Tabular Editor CLI también lo aplica. Establezca `AiAuditLogPath` en una carpeta para cada usuario: ya sea un valor `REG_EXPAND_SZ` como `\\fileserver\te-audit$\%USERNAME%` bajo la clave `HKEY_LOCAL_MACHINE`, o un valor `REG_SZ` por usuario bajo `HKEY_CURRENT_USER\SOFTWARE\Policies\Tabular Editor ApS\TE3`.

## Preguntas frecuentes

### ¿Tabular Editor ApS recibe nuestras indicaciones, metadatos o datos?

No. Consulte [Flujo de datos](#data-flow).

### ¿Se utilizan nuestros datos para entrenar modelos de IA?

Tabular Editor ApS no recibe ninguna solicitud, respuesta ni contenido del modelo. Tu acuerdo con el proveedor de IA determina si el proveedor entrena con las solicitudes.

### ¿Dónde se procesan nuestros datos?

En el punto de conexión configurado del asistente de IA y en cualquier lugar donde opere el proveedor de un agente MCP. Consulta [Restringir el proveedor de IA](#restrict-the-ai-provider).

### ¿Pueden los usuarios eludir una directiva?

Un usuario no puede cambiar una política sin derechos de administrador local. Las versiones anteriores a la 3.27.0, incluidas las compilaciones portátiles más antiguas, solo leen `HKEY_CURRENT_USER\Software\Policies\Kapacity\Tabular Editor` e ignoran todas las políticas de esta página. Consulte [Desactivar las funciones de IA](#turn-the-ai-features-off).

### ¿Pueden las funciones de IA cambiar o implementar un modelo de producción?

Ejecutan scripts en el modelo cargado solo con **Metadatos del modelo** en **Escritura**, y solo el usuario guarda o implementa. Consulte [Medidas de seguridad para los cambios en el modelo](#safeguards-on-model-changes).

### ¿Pueden las funciones de IA leer datos de nuestros modelos?

Los resultados de las consultas DAX y el texto de los errores de Analysis Services requieren **Datos del modelo** en **Lectura**, y el valor predeterminado es **Denegar**. Por debajo de **Lectura**, el texto de error del servidor se reemplaza por una frase fija. Los valores introducidos en la definición del modelo forman parte de los metadatos. Consulta [Flujo de datos](#data-flow).

### ¿Puede un agente MCP usar un proveedor que no hayamos aprobado?

Sí. Controle el agente a través de sus propios controles administrativos o establezca `DisableMcpServer`. Consulta [Servidor MCP](#mcp-server).

### ¿Cómo detenemos las funciones de IA en un incidente?

Establezca `DisableAi` y haga que los usuarios reinicien Tabular Editor 3. Revoque las claves de API afectadas en el proveedor. Consulte [Desactivar las funciones de IA](#turn-the-ai-features-off).

### ¿El registro de auditoría es a prueba de manipulaciones?

No. El usuario puede cambiar y eliminar sus propios archivos de auditoría. Consulta [Registro de auditoría](#audit-log).

## Véase también

- @ai-assistant
- @mcp-server
- @ai-audit-log
- @policies
- @security-privacy
- @editions
