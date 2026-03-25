---
uid: security-privacy
title: Resumen de seguridad
author: Daniel Otykier
updated: 2026-03-25
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

### AI Assistant

Tabular Editor 3 includes an optional AI Assistant for chat-based semantic model development. The AI Assistant is an optional module that the user selects during installation. If you choose not to install the module, no AI-related code is present on the machine and none of the behavior described in this section applies. The AI Assistant uses a **bring-your-own-key** model. You provide an API key from a supported AI provider (OpenAI, Anthropic, Azure OpenAI or any OpenAI-compatible endpoint). No built-in API key is included and Tabular Editor does not provide or intermediate any AI service.

**Data flow.** All communication between the AI Assistant and the AI provider happens directly from the client machine to the provider API. No data passes through Tabular Editor servers. The data sent depends on the actions you perform in the chat and is scoped to the following categories, each requiring explicit user consent before any data is transmitted:

| Consent Category | Data Sent to AI Provider                                                          |
| ---------------- | --------------------------------------------------------------------------------- |
| Model metadata   | Table and column schemas, measure definitions and other structural model metadata |
| Query data       | DAX query results and data samples                                                |
| Read documents   | Content from open documents such as DAX scripts and DAX queries                   |
| Modify documents | Requests to make changes to open documents                                        |
| Edit BPA rules   | Best Practice Analyzer rule definitions                                           |
| Read macros      | Macro definitions from the user macro library                                     |

**Consent management.** The AI Assistant prompts for consent the first time it needs access to each data category. You choose the duration of your consent: single request, current session, the current model only, or always. You can review and revoke consents at any time under **Tools > Preferences > AI Assistant > AI Consents**. Per-model consents for query data and model metadata are stored in the model user options (.tmuo) file. Global "always" consents are stored in the local Preferences.json file.

**API key storage.** API keys are stored encrypted on the local machine in the Preferences.json file. If the AI module is not loaded (for example because it was excluded during installation or disabled by policy), any previously stored API key configuration is cleared automatically.

**Conversation storage.** Conversations are stored locally on the client machine in `%LocalAppData%\TabularEditor3\AI\Conversations\`. No conversation data is sent to Tabular Editor servers.

**Disabling the AI Assistant.** The AI Assistant is an optional component. You can exclude it during installation, disable it under **Tools > Preferences > AI Assistant**, or enforce the `DisableAi` [policy](xref:policies) through the Windows registry.

**Penetration testing.** A separate penetration test of the AI Assistant has been performed. The report is available in our [Trust Center](https://trust.tabulareditor.com/).

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
- **AI Assistant.** When the AI Assistant is configured and in use, Tabular Editor 3 sends requests directly to the configured AI provider API. The endpoints depend on the selected provider (for example `https://api.openai.com` for OpenAI, `https://api.anthropic.com` for Anthropic, or a user-specified endpoint for Azure OpenAI and custom providers). Only data for which the user has granted consent is included in these requests. See the [AI Assistant](#ai-assistant) section above for details on data categories and consent management.
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
- AI Assistant: Depends on the configured provider (e.g. **https://api.openai.com**, **https://api.anthropic.com**, or user-specified Azure OpenAI / custom endpoints)

> [!NOTE]
> Un administrador del sistema puede aplicar determinadas [directivas](xref:policies), que pueden usarse para deshabilitar algunas o todas las funciones mostradas en la lista anterior.

## Seguridad de la aplicación

Tabular Editor no requiere ningún privilegio elevado en el equipo Windows donde está instalado, ni accede a ningún recurso restringido del equipo. Una excepción a esta regla es si se usa el archivo del instalador de Tabular Editor (.msi); en ese caso, el ejecutable y los archivos de soporte necesarios para la herramienta se copian, de forma predeterminada, en la carpeta `Program Files`, que normalmente requiere permisos elevados. Tanto los archivos binarios de Tabular Editor como el archivo del instalador se han firmado con un certificado de firma de código emitido a Kapacity A/S, lo cual garantiza que el código no ha sido manipulado por terceros.

Mientras la aplicación se está ejecutando, todo el acceso a recursos externos se realiza a través de la biblioteca cliente AMO/TOM o de las solicitudes web mencionadas anteriormente.

La funcionalidad de C# Script permite a Tabular Editor ejecutar código C# arbitrario dentro del runtime de .NET. Ese código solo se compila y ejecuta cuando lo solicitas explícitamente. Los C# Script también pueden guardarse como "macros", lo que te facilita administrar y ejecutar varios scripts distintos. El código se almacena en tu propia carpeta `%localappdata%`, lo que garantiza que solo tú o un administrador local del equipo pueden acceder a los scripts. Siempre eres responsable de garantizar que el código ejecutado no provoque efectos secundarios no deseados. En ningún caso Tabular Editor ApS será responsable de ningún daño, pérdida o filtración causados por el uso de las funciones de C# Script o de acciones personalizadas/macros.
