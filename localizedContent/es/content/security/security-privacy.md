---
uid: security-privacy
title: Resumen de seguridad
author: Daniel Otykier
updated: 2026-09-17
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

# Seguridad y privacidad de Tabular Editor 3

Este documento describe las consideraciones de seguridad y privacidad de Tabular Editor 3 y su uso. A continuación, la expresión "Tabular Editor" puede referirse tanto a la herramienta comercial Tabular Editor 3 como a la herramienta de código abierto Tabular Editor 2.X. Cuando algo se refiera solo a una de las herramientas, utilizaremos sus nombres explícitos: "Tabular Editor 3" o "Tabular Editor 2.X".

## Recomendaciones de Microsoft sobre herramientas de terceros como Tabular Editor

Microsoft respalda el uso de herramientas de terceros de la comunidad, tal y como se indica aquí: [Herramientas comunitarias y de terceros para desarrollar modelos empresariales de Power BI y Analysis Services](https://powerbi.microsoft.com/en-us/blog/community-tools-for-enterprise-powerbi-and-analysisservices)

La documentación de planificación de implementación de Power BI de Microsoft incluye específicamente Tabular Editor en escenarios avanzados de modelado de datos y desarrollo empresarial: [Escenarios de uso de Power BI: Administración avanzada del Data model](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-advanced-data-model-management#tabular-editor)

## Trust Center

En Tabular Editor, estamos comprometidos con la transparencia y con prácticas de seguridad sólidas. Visita nuestro [Trust Center](https://trust.tabulareditor.com/) para ver detalles de nuestro Report de auditoría SOC 2, documentos clave de políticas, términos de licencia y nuestro enfoque sobre la seguridad de la infraestructura y la organización. También encontrarás información sobre nuestros subprocesadores y sobre cómo trabajamos para mantener tus datos seguros.

## Metadatos y privacidad de los datos

Tabular Editor es principalmente una herramienta sin conexión, lo que significa que todos los datos y metadatos se almacenan localmente en el equipo cliente donde está instalado Tabular Editor, y que todas las interacciones del usuario también se realizan de forma local. No se requiere una conexión a Internet para ejecutar y usar Tabular Editor.

Dicho esto, hay escenarios en los que Tabular Editor se conecta a servicios remotos con distintos fines. Se describen a continuación:

### Protocolo XMLA de Analysis Services

Toda la comunicación con las instancias de Analysis Services o con los Workspace de Power BI Premium se realiza mediante las bibliotecas cliente de [Microsoft Analysis Management Objects (AMO)](https://docs.microsoft.com/en-us/analysis-services/amo/developing-with-analysis-management-objects-amo?view=asallproducts-allversions) o, más específicamente, la [extensión Tabular Object Model (TOM) para AMO](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions). Estas bibliotecas cliente las proporciona Microsoft para su redistribución en aplicaciones de terceros, como Tabular Editor. Para conocer los detalles de la licencia, consulta el [EULA de AMO](https://go.microsoft.com/fwlink/?linkid=852989).

Cuando Tabular Editor se conecta a una instancia de Analysis Services (en la red local o en la nube) o a un Workspace de Power BI Premium (en la nube), esta conexión se realiza a través de las bibliotecas cliente mencionadas anteriormente. Por diseño, la biblioteca AMO se encarga de la autenticación y la autorización del usuario. Solo los usuarios con privilegios administrativos en la instancia de Analysis Services o en el Workspace de Power BI Premium pueden conectarse. Esto no difiere de lo que ocurre al usar herramientas de Microsoft como SQL Server Management Studio o SQL Server Data Tools (que usan las mismas bibliotecas cliente para conectarse).

### Metadatos del Tabular Object Model

Una vez que la biblioteca cliente AMO/TOM establece la conexión, Tabular Editor solicitará todos los metadatos del Tabular Object Model (TOM) correspondientes a la base de datos de Analysis Services o al Dataset de Power BI específico al que el usuario quiera conectarse. A continuación, la biblioteca cliente AMO/TOM proporciona estos metadatos a la aplicación cliente (Tabular Editor) de forma programática, lo que permite a la aplicación aplicar cambios de metadatos, como cambiar el nombre de un objeto, agregar una descripción, modificar una expresión DAX, etc. Además, la biblioteca cliente AMO/TOM ofrece métodos para serializar los metadatos de TOM en un formato basado en JSON. Tabular Editor utiliza esta técnica para permitir a los usuarios guardar los metadatos del modelo como un archivo JSON local, con fines de control de versiones de la estructura del Data model. **Nota: El archivo JSON generado de este modo no contiene ningún registro de datos real. El archivo contiene únicamente metadatos del modelo; es decir, información sobre la estructura del modelo en cuanto a tablas, columnas, medidas, expresiones DAX, etc.** Aunque, por lo general, los metadatos del modelo no se consideran información confidencial, es responsabilidad del usuario de Tabular Editor tratar cualquier archivo generado de este modo con la confidencialidad requerida (por ejemplo, no compartir el archivo con terceros, etc.).

**Tabular Editor no recopila, publica, comparte, transfiere ni hace públicos de ningún otro modo los metadatos del modelo obtenidos a través de la biblioteca cliente AMO/TOM, a menos que el usuario inicie explícitamente una acción para hacerlo** (por ejemplo, guardando el archivo JSON de metadatos del modelo en una ubicación de red compartida o implementando los metadatos del modelo en otra instancia de Analysis Services o en un Workspace de Power BI).

### Contenido de datos del modelo

En lo que sigue, "datos del modelo" se refiere a los registros de datos reales almacenados en la base de datos de Analysis Services o en el Dataset de Power BI. Según la base de datos de origen o el Dataset, es muy probable que los datos del modelo sean confidenciales.

Dado que se requiere que el usuario tenga privilegios administrativos en la instancia de Analysis Services o en el Workspace de Power BI al que se está conectando, el usuario, por definición, también tendrá acceso a todo el contenido de datos de la base de datos de Analysis Services o del Dataset de Power BI. Tabular Editor solo permite recuperar datos a través de la biblioteca cliente AMO mencionada anteriormente. Tabular Editor 3 ofrece funcionalidades para explorar y consultar los datos del modelo. Independientemente de la técnica que se utilice para acceder a los datos, **Tabular Editor solo almacena los datos recuperados en la memoria local. Tabular Editor no recopila, publica, comparte, transfiere ni hace públicos de ningún otro modo los datos del modelo obtenidos a través de la herramienta**. Si un usuario decide copiar o exportar los resultados de consultas obtenidos a través de Tabular Editor, es su responsabilidad tratar los datos copiados o exportados de acuerdo con el nivel de confidencialidad de esos datos. Esto no difiere de cuando un usuario se conecta a la base de datos de Analysis Services o al Dataset de Power BI mediante herramientas cliente como Excel o Power BI; en ese caso, también tendrá la opción de copiar los resultados de la consulta.

### Asistente de IA

Tabular Editor 3 incluye un asistente de IA para el desarrollo de modelos semánticos mediante chat. A partir de la versión 3.27.0 forma parte de la instalación predeterminada; antes había que seleccionarlo expresamente. Si el componente no está instalado, no hay ningún código relacionado con la IA en el equipo y no se aplica nada de lo descrito en esta sección.

El Asistente de IA usa un modelo **bring-your-own-key**. Proporcionas una clave de API de un proveedor de IA compatible (OpenAI, Anthropic, Azure OpenAI o cualquier punto de conexión compatible con OpenAI). No se incluye ninguna clave de API integrada y Tabular Editor no proporciona ni intermedia ningún servicio de IA.

**Flujo de datos.** Toda la comunicación entre el Asistente de IA y el proveedor de IA se realiza directamente desde el equipo cliente hasta la API del proveedor. Ningún dato pasa por los servidores de Tabular Editor. Lo que se envía depende de lo que solicites y está limitado por cinco recursos de permisos, cada uno con un nivel de acceso:

| Recurso                | Qué abarca                                                                                                                                                        | Niveles                       | Predeterminado |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- | -------------- |
| Metadatos del modelo   | Nombres de tablas, columnas y medidas, expresiones, descripciones y similares. La lectura también abarca las estadísticas del Analizador VertiPaq | Denegar / Leer / Escribir     | Leer           |
| Datos del modelo       | Valores de datos de tu modelo, como los resultados de consultas DAX. Requiere una conexión en directo                                             | Denegar / Leer                | Denegar        |
| Best Practice Analyzer | Leer enumera las reglas y ejecuta el análisis; Escribir añade o modifica reglas                                                                                   | Denegar / Leer / Escribir     | Leer           |
| Documentos             | Tus editores abiertos de C# Script y de consultas DAX. Leer permite acceder a su contenido; Escribir es necesario para crearlos o modificarlos    | Denegar / Leer / Escribir     | Escribir       |
| Macros                 | Tu biblioteca de macros                                                                                                                                           | Denegar / Lectura / Escritura | Escritura      |

Escritura incluye Lectura. El acceso a los datos del modelo se deniega de forma predeterminada porque los metadatos describen un modelo en el que los valores de datos son el contenido del modelo.

**Gestión de permisos.** Las autorizaciones son configuraciones permanentes, no avisos por solicitud. Revísalas y cámbialas en **Herramientas > Preferencias > Funciones de IA > Permisos** o en el cuadro de diálogo **Herramientas > Servidor MCP...**, que edita el mismo registro. Si el chat necesita algo que una autorización no cubra, muestra una tarjeta de permiso en ese momento y puedes responder para el turno, la sesión, el modelo actual o siempre. **Permitir siempre** aumenta la autorización permanente y nunca la reduce. Las autorizaciones globales se almacenan en el archivo local Preferences.json; las autorizaciones concedidas para un único modelo se almacenan en el archivo de opciones de usuario (.tmuo) de ese modelo y se aplican solo al chat. Restablecer un recurso a **Denegar** hace que el chat vuelva a preguntar.

**Límites del administrador.** En las ediciones Enterprise, Consultancy y Trial, un administrador puede fijar un límite para cada recurso mediante una [política](xref:policies), por separado para el chat y para el servidor MCP, y el límite del MCP solo puede ser inferior. Un límite prevalece sobre cualquier autorización, incluida una que el usuario ya haya dado, y la opción correspondiente se muestra como de solo lectura. Estas políticas fallan en modo seguro: si en un equipo no licenciado aparece cualquier valor de política de nivel Enterprise, el Asistente de IA y el servidor MCP se niegan a iniciarse en lugar de ignorar la política.

**Registro de auditoría.** Tabular Editor 3 escribe un registro local de lo que hicieron el Asistente de IA y el servidor MCP: qué permisos se solicitaron y cómo se respondieron, qué herramientas se ejecutaron y si cada una tuvo éxito, falló o fue rechazada, y el texto completo de cualquier C# Script que ejecutara un agente o que este entregara para revisión. No se registran los prompts, las respuestas ni los valores de datos. Los archivos diarios se conservan durante 30 días, y la opción **Abrir carpeta de auditoría** en **Herramientas > Preferencias > Funciones de IA** los abre. Los administradores pueden cambiar la ubicación y el período de retención.

**Almacenamiento de claves de API.** Las claves de API se almacenan cifradas en el equipo local, en el archivo de preferencias Preferences.json. Si el módulo de IA no se carga (por ejemplo, porque se excluyó durante la instalación o se deshabilitó mediante una directiva), cualquier configuración de claves de API almacenada anteriormente se borra automáticamente.

**Almacenamiento de conversaciones.** Las conversaciones se almacenan localmente en el equipo cliente en `%LocalAppData%\TabularEditor3\AI\Conversations\`. No se envían datos de conversaciones a los servidores de Tabular Editor.

**Deshabilitar el Asistente de IA.** Puedes excluir el componente de funciones de IA durante la instalación, borrar el proveedor en **Herramientas > Preferencias > Funciones de IA > Asistente de IA** o aplicar una [política](xref:policies) mediante el Registro de Windows: `DisableAi` desactiva toda la funcionalidad de IA, incluido el servidor MCP, y borra la configuración del proveedor almacenada, mientras que `DisableAiChat` desactiva solo el chat y deja el servidor MCP en ejecución.

**Pruebas de penetración.** Se ha realizado una prueba de penetración independiente del Asistente de IA. El Report está disponible en nuestro [Trust Center](https://trust.tabulareditor.com/).

### Servidor MCP

Tabular Editor 3 puede actuar como servidor MCP (Model Context Protocol) para que un agente de IA que se ejecute en el mismo equipo pueda trabajar en el modelo que tienes abierto. Consulta @mcp-server para obtener información sobre la función en sí.

**Exposición de red.** El servidor es un listener HTTP enlazado explícitamente a `127.0.0.1`, de forma predeterminada, en el puerto 42100. No es accesible desde otro equipo. Las solicitudes del navegador que llevan un encabezado `Origin` no local se rechazan como medida de protección frente al DNS rebinding. El servidor se ejecuta solo después de iniciarlo, o desde el inicio de la aplicación si así lo has indicado.

**Autenticación.** La vinculación a loopback es el perímetro de seguridad predeterminado, por lo que el servidor acepta conexiones locales sin credenciales de forma predeterminada. En un host en el que varias personas tienen sesión iniciada a la vez, como un servidor de Remote Desktop o Citrix, eso no basta: cualquier sesión de la máquina puede acceder a `127.0.0.1`. Mientras el token esté desactivado, cualquier proceso de la máquina puede conectarse sin credenciales. Activa **Requerir token de acceso** en **Herramientas > Preferencias > Funciones de IA > Servidor MCP** y los clientes tendrán que presentar un bearer token, que se almacena cifrado en el archivo local Preferences.json. Los administradores pueden imponerlo con la [directiva](xref:policies) `RequireMcpAccessToken`.

**Flujo de datos.** Tabular Editor no contacta con ningún proveedor de IA para esta característica ni almacena ninguna clave de API para ella. El agente es la única parte que se comunica con un proveedor, con su propia configuración y su propia suscripción. Lo que el agente puede leer del modelo está limitado por las mismas cinco concesiones de permisos que rigen el Asistente de IA, capturadas al iniciarse el servidor, y nunca se ofrece al agente ninguna herramienta que no esté cubierta por una de ellas. El acceso a los datos del modelo está denegado de forma predeterminada, por lo que ningún valor de datos sale del modelo a menos que lo autorices explícitamente.

**Cambios en el modelo.** Un agente solo cambia el modelo a través del motor de scripting de C#, usando **C# Script**, de forma atómica y como un único paso de deshacer, y solo con la concesión de metadatos del modelo en Write. La ejecución directa de TMSL y XMLA nunca está disponible para un agente, y nunca se ejecuta para él un script que vaya más allá del modelo.

**Registro de auditoría.** Las decisiones sobre permisos, las llamadas a herramientas y el texto completo de cualquier **C# Script** que un agente haya ejecutado o entregado para su revisión se escriben en un registro de auditoría local. Los prompts, las respuestas y los valores de datos no se registran.

**Desactivación del servidor MCP.** Desmarca **Habilitar servidor MCP** en **Herramientas > Preferencias > Funciones de IA > Servidor MCP**, o aplica la [directiva](xref:policies) `DisableMcpServer` o `DisableAi`. El servidor forma parte del componente de funciones de IA, por lo que, si excluyes ese componente durante la instalación, también se quitará.

### Solicitudes web

Tabular Editor puede realizar solicitudes a recursos en línea (URL web) solo en los siguientes casos:

- **Activación de licencia\*.** Cuando Tabular Editor 3 se inicia por primera vez y, posteriormente, a intervalos periódicos, la herramienta puede realizar una solicitud a nuestro servicio de licencias. Esta solicitud contiene información cifrada sobre la clave de licencia introducida por el usuario, la dirección de correo electrónico del usuario (si se proporciona), el nombre del equipo local y un hash codificado unidireccional que identifica la instalación actual. No se transmite ningún otro dato en esta solicitud. El propósito de esta solicitud es activar y validar la clave de licencia utilizada por la instalación, aplicar las limitaciones de la versión de prueba y permitir que el usuario gestione sus instalaciones de Tabular Editor 3 a través de nuestro servicio de licencias.
- **Comprobaciones de actualización\*.** Cada vez que se inicia Tabular Editor 3, puede realizar una solicitud a nuestro servicio de aplicaciones para determinar si hay disponible una versión más reciente de Tabular Editor 3. Esta solicitud no contiene ningún dato.
- **Telemetría de uso\*.** De forma predeterminada, Tabular Editor 3 recopila y transmite datos de uso anónimos a medida que los usuarios interactúan con la herramienta. Estos datos incluyen información sobre los objetos de la interfaz de usuario con los que interactúa un usuario y el momento de cada interacción. También contiene información de alto nivel sobre el Data model tabular que se está editando con la herramienta. Esta información solo se refiere a propiedades de alto nivel como el nivel de compatibilidad y el modo, el número de tablas, el tipo de servidor (Analysis Services vs. Power BI vs. Power BI Desktop), etc. **No se recopilan datos personales identificables de esta manera**, ni recopilamos información sobre los nombres de los objetos o las expresiones DAX en el propio Tabular Object Model. Un usuario puede optar por no enviarnos datos de telemetría en cualquier momento.
- **Reports de error\*.** Cuando se produce un error inesperado, transmitimos la traza de la pila y los mensajes de error (anonimizados), junto con una descripción opcional proporcionada por el usuario. Si un usuario decide no enviar datos de telemetría, tampoco se enviarán los Reports de error.
- **Uso del formateador de DAX.** (Solo Tabular Editor 2.x) Se puede dar formato a una expresión DAX haciendo clic en un botón en Tabular Editor. En este caso, la expresión DAX (y nada más) se envía al servicio web www.daxformatter.com. La primera vez que un usuario hace clic en este botón, se muestra un mensaje de advertencia explícito para que confirme su intención. Tabular Editor 3 no realiza solicitudes web al dar formato al código DAX.
- **Optimizador de DAX**. Si un usuario tiene una [cuenta de Tabular Tools](https://tabulartools.com) con una suscripción a [Optimizador de DAX](https://daxoptimizer.com), podrá explorar su Workspace del Optimizador de DAX, ver incidencias y sugerencias, y cargar nuevos archivos VPAX directamente desde Tabular Editor 3. Los archivos VPAX contienen metadatos y estadísticas del modelo, pero no _datos_ reales del modelo. La función de integración del Optimizador de DAX en Tabular Editor 3 realiza varias solicitudes a uno o varios de los endpoints indicados a continuación (en función del tipo de autenticación y de la región especificados al crear la cuenta de Tabular Tools).<br/>
  Para obtener más información, consulta la [documentación de Optimizador de DAX](https://docs.daxoptimizer.com/legal/data-processing).<br/>
  Endpoints utilizados:
  - https://account.tabulartools.com
  - https://licensing.api.daxoptimizer.com/api
  - https://australiaeast.api.daxoptimizer.com/api
  - https://eastus.api.daxoptimizer.com/api
  - https://westeurope.api.daxoptimizer.com/api
- **Asistente de IA.** Cuando el Asistente de IA está configurado y en uso, Tabular Editor 3 envía solicitudes directamente a la API del proveedor de IA configurado. Los endpoints dependen del proveedor seleccionado (por ejemplo, `https://api.openai.com` para OpenAI, `https://api.anthropic.com` para Anthropic o el endpoint que especifiques para Azure OpenAI y proveedores personalizados). En estas solicitudes solo se incluyen los datos cubiertos por las concesiones de permisos. Consulta la sección [Asistente de IA](#ai-assistant) anterior para ver los recursos y sus valores predeterminados.
- **Actualizaciones de la base de conocimientos de IA.** La base de conocimientos en la que busca el Asistente de IA es una base de datos local incluida en el componente de funciones de IA. Tabular Editor 3 comprueba si hay una copia más reciente y la descarga desde `https://cdn.tabulareditor.com`. La solicitud no contiene datos sobre ti ni sobre tu modelo.
- **Servidor MCP.** El servidor MCP no realiza solicitudes salientes. Solo acepta conexiones en la interfaz loopback, y el agente que se conecta a él es quien se comunica con un proveedor de IA, con su propia configuración. Consulta la sección [servidor MCP](#mcp-server) anterior.
- **Importación de reglas de prácticas recomendadas.** Tabular Editor incluye una funcionalidad que permite especificar una dirección URL desde la que obtener una lista de reglas de prácticas recomendadas en formato JSON. Este tipo de solicitud solo descarga los datos JSON desde la URL; no se transmite ningún dato a la URL.
- **Uso de C# Scripts.** Tabular Editor permite a los usuarios escribir y ejecutar código en C# con fines de automatización. Este tipo de script puede conectarse a recursos en línea mediante características del lenguaje C# y el entorno de ejecución de .NET. El usuario es siempre responsable de garantizar que el código ejecutado no provoque ningún intercambio de datos no deseado. Tabular Editor ApS no se hace responsable de ningún daño, pérdida o filtración causados por el uso, en general, de la funcionalidad de C# Script. Tabular Editor nunca ejecutará C# Scripts sin una acción explícita del usuario.

\***Toda la información que obtengamos a través del servicio de activación de licencias, la telemetría de uso o los Reports de errores se mantendrá confidencial. No compartiremos, publicaremos ni distribuiremos los datos recopilados de ninguna forma.**

**Lista de permitidos / aceptados del firewall**
Para permitir el tráfico de las solicitudes web mencionadas anteriormente, deberás incluir en la lista de permitidos:

- Activación de licencias / comprobaciones de actualización: **https://api.tabulareditor.com**
- Telemetría de uso / Reports de errores: **https://\*.in.applicationinsights.azure.com**
- DAX Formatter (solo Tabular Editor 2.x): **https://www.daxformatter.com**
- Importar reglas de prácticas recomendadas / C# Scripts: depende del contexto
- Optimizador de DAX: puntos de conexión enumerados arriba.
- Asistente de IA: Depende del proveedor configurado (p. ej., **https://api.openai.com**, **https://api.anthropic.com** o endpoints de Azure OpenAI o personalizados especificados por el usuario)
- Actualizaciones de la base de conocimientos de IA: **https://cdn.tabulareditor.com**
- Servidor MCP: nada. Escucha en **127.0.0.1** y no realiza solicitudes salientes

> [!NOTE]
> Un administrador del sistema puede aplicar determinadas [directivas](xref:policies), que pueden usarse para deshabilitar algunas o todas las funciones mostradas en la lista anterior.

## Seguridad de la aplicación

Tabular Editor no requiere ningún privilegio elevado en el equipo Windows donde está instalado, ni accede a ningún recurso restringido del equipo. Una excepción a esta regla es si se usa el archivo del instalador de Tabular Editor (.msi); en ese caso, el ejecutable y los archivos de soporte necesarios para la herramienta se copian, de forma predeterminada, en la carpeta `Program Files`, que normalmente requiere permisos elevados. Tanto los archivos binarios de Tabular Editor como el archivo del instalador se han firmado con un certificado de firma de código emitido a Kapacity A/S, lo cual garantiza que el código no ha sido manipulado por terceros.

Mientras la aplicación se está ejecutando, todo el acceso a recursos externos se realiza a través de la biblioteca cliente AMO/TOM o de las solicitudes web mencionadas anteriormente.

La funcionalidad de C# Script permite a Tabular Editor ejecutar código C# arbitrario dentro del runtime de .NET. Ese código solo se compila y ejecuta cuando lo solicitas explícitamente. Los C# Script también pueden guardarse como "macros", lo que te facilita administrar y ejecutar varios scripts distintos. El código se almacena en tu propia carpeta `%localappdata%`, lo que garantiza que solo tú o un administrador local del equipo pueden acceder a los scripts. Siempre eres responsable de garantizar que el código ejecutado no provoque efectos secundarios no deseados. En ningún caso Tabular Editor ApS será responsable de ningún daño, pérdida o filtración causados por el uso de las funciones de C# Script o de acciones personalizadas/macros.

Las organizaciones que no quieran dejar esto a criterio de cada usuario pueden gestionarlo de forma centralizada. Las [políticas](xref:policies) `DisableCSharpScripts` y `DisableMacros` desactivan por completo los scripts de C# y las macros, en todas las ediciones. Con Tabular Editor 3 Edición Enterprise, `BlockUnsafeScripts` mantiene el scripting disponible, pero solo permite scripts y macros que permanezcan dentro del modelo semántico: se rechaza, antes de ejecutarse, cualquier cosa que lea o escriba un archivo, acceda a la red, inicie otro programa o cargue código externo, independientemente de dónde provenga el script: un documento de script, el Best Practice Analyzer, una macro, el Asistente de IA, el servidor MCP o la línea de comandos. Consulta las [políticas de administrador](xref:csharp-scripts#administrator-policies).
