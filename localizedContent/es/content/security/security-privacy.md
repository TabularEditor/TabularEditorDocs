---
uid: security-privacy
title: Descripción general de la seguridad
author: Morten Lønskov
updated: 2026-10-12
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
# Seguridad y privacidad de Tabular Editor 3

Este documento describe las consideraciones de seguridad y privacidad de Tabular Editor 3 y su uso. A continuación, la expresión «Tabular Editor» puede referirse tanto a la herramienta comercial Tabular Editor 3 como a la herramienta de código abierto Tabular Editor 2.X. Siempre que se haga referencia a una sola de las herramientas, usaremos sus nombres explícitos «Tabular Editor 3» o «Tabular Editor 2.X».

## Recomendaciones de Microsoft sobre herramientas de terceros como Tabular Editor

Microsoft respalda el uso de herramientas de terceros de la comunidad, tal y como se indica aquí: [Herramientas de la comunidad y de terceros para desarrollar modelos de Power BI y Analysis Services a nivel empresarial]( https://powerbi.microsoft.com/en-us/blog/community-tools-for-enterprise-powerbi-and-analysisservices)

La documentación de planificación de la implementación de Power BI de Microsoft incluye específicamente a Tabular Editor en escenarios avanzados de modelado de datos y desarrollo empresarial: [Escenarios de uso de Power BI: Gestión avanzada de modelos de datos](https://learn.microsoft.com/power-bi/guidance/powerbi-implementation-planning-usage-scenario-advanced-data-model-management#tabular-editor)

## Centro de cumplimiento
En Tabular Editor, estamos comprometidos con la transparencia y con unas sólidas prácticas de seguridad. Visite nuestro [Centro de confianza](https://trust.tabulareditor.com/) para obtener información sobre nuestro informe de auditoría SOC 2, los documentos clave de nuestras políticas, los términos de las licencias y nuestro enfoque en materia de seguridad de la infraestructura y de la organización. También encontrará información sobre nuestros subencargados del tratamiento y sobre cómo trabajamos para mantener sus datos seguros.

## Metadatos y privacidad de los datos

Tabular Editor es principalmente una herramienta sin conexión, lo que significa que todos los datos y metadatos residen localmente en el equipo cliente en el que está instalado Tabular Editor, y todas las interacciones de los usuarios también se realizan localmente. No se requiere una conexión a Internet para ejecutar y usar Tabular Editor.

Dicho esto, hay situaciones en las que Tabular Editor se conecta a servicios remotos para diversos fines. A continuación se describen:

### Protocolo XMLA de Analysis Services

Toda la comunicación con las instancias de Analysis Services o los espacios de trabajo de Power BI Premium se realiza mediante el uso de las bibliotecas cliente de [Microsoft Analysis Management Objects (AMO)](https://docs.microsoft.com/analysis-services/amo/developing-with-analysis-management-objects-amo?view=asallproducts-allversions), o más concretamente, de la [extensión Tabular Object Model (TOM) para AMO](https://docs.microsoft.com/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions). Microsoft proporciona estas bibliotecas cliente para su redistribución en aplicaciones de terceros como Tabular Editor. Para obtener información sobre las licencias, consulta el [CLUF de AMO](https://go.microsoft.com/fwlink/?linkid=852989).

Cuando Tabular Editor se conecta a una instancia de Analysis Services (red local o nube) o a un área de trabajo de Power BI Premium (nube), esta conexión se realiza a través de las bibliotecas cliente mencionadas anteriormente. Por diseño, la biblioteca AMO se encarga de la autenticación y la autorización del usuario. Solo los usuarios con privilegios administrativos en la instancia de Analysis Services o en el área de trabajo de Power BI Premium pueden conectarse. Esto no es diferente de cuando se utilizan herramientas de Microsoft como SQL Server Management Studio o SQL Server Data Tools (que utilizan las mismas bibliotecas cliente para la conectividad).

### Metadatos del Tabular Object Model

Una vez que la biblioteca cliente AMO/TOM establece la conexión, Tabular Editor solicitará los metadatos completos del Tabular Object Model (TOM) para la base de datos de Analysis Services o el conjunto de datos de Power BI específicos a los que el usuario desee conectarse. A continuación, la biblioteca cliente AMO/TOM proporciona estos metadatos a la aplicación cliente (Tabular Editor) mediante un enfoque programático, lo que permite a la aplicación aplicar cambios en los metadatos, como cambiar el nombre de un objeto, añadir una descripción, modificar una expresión DAX, etc. Además, la biblioteca cliente AMO/TOM proporciona métodos para serializar los metadatos TOM en un formato basado en JSON. Tabular Editor utiliza esta técnica para permitir a los usuarios guardar los metadatos del modelo como un archivo JSON local, con el fin de controlar las versiones de la estructura del modelo de datos. **Nota: El archivo JSON generado de esta manera no contiene registros de datos reales. El archivo contiene únicamente metadatos del modelo, es decir, información sobre la estructura del modelo en términos de tablas, columnas, medidas, expresiones DAX, etc.** Aunque los metadatos del modelo generalmente no se consideran información confidencial, es responsabilidad del usuario de Tabular Editor tratar cualquier archivo generado de esta manera con la confidencialidad necesaria (es decir, no compartir el archivo con terceros, etc.).

**Tabular Editor no recopila, publica, comparte, transfiere ni hace públicos de ninguna otra forma los metadatos del modelo obtenidos a través de la biblioteca cliente AMO/TOM, a menos que el usuario inicie específicamente una acción para hacerlo** (por ejemplo, guardando el archivo JSON de los metadatos del modelo en una ubicación de red compartida o implementando los metadatos del modelo en otra instancia de Analysis Services o en otro área de trabajo de Power BI).

### Contenido de los datos del modelo

En lo sucesivo, «datos del modelo» se refiere a los registros de datos reales almacenados en la base de datos de Analysis Services o en el conjunto de datos de Power BI. Dependiendo de la base de datos o del conjunto de datos de origen, es muy probable que los datos del modelo sean confidenciales.

Debido al requisito de que un usuario tenga privilegios administrativos en la instancia de Analysis Services o en el área de trabajo de Power BI a la que se conecta, el usuario, por definición, también tendrá acceso a todo el contenido de datos de la base de datos de Analysis Services o del conjunto de datos de Power BI. Tabular Editor solo permite la recuperación de datos a través de la biblioteca cliente AMO mencionada anteriormente. Tabular Editor 3 ofrece funciones para explorar y consultar los datos del modelo. Independientemente de la técnica que se utilice para acceder a los datos, **Tabular Editor solo almacena los datos recuperados en la memoria local. Tabular Editor no recopila, publica, comparte, transfiere ni hace públicos de ninguna otra forma los datos del modelo obtenidos a través de la herramienta**. Si un usuario decide copiar o exportar los resultados de las consultas obtenidos a través de Tabular Editor, es su responsabilidad tratar los datos copiados o exportados de acuerdo con su nivel de confidencialidad. Esto no es diferente a que un usuario se conecte a la base de datos de Analysis Services o al conjunto de datos de Power BI utilizando herramientas cliente como Excel o Power BI, en cuyo caso también tendrá la opción de copiar los resultados de las consultas.

### Asistente de IA

Tabular Editor 3 incluye un Asistente de IA para el desarrollo de modelos semánticos basado en chat. A partir de la versión 3.27.0, forma parte de la instalación predeterminada; antes de esa versión, había que seleccionarlo deliberadamente. Si el componente no está instalado, no hay ningún código relacionado con la IA en el equipo y no se aplica ninguno de los comportamientos descritos en esta sección.

El asistente de IA utiliza un modelo de **trae tu propia clave**. Tú proporcionas una clave de API de un proveedor de IA compatible (OpenAI, Anthropic, Azure OpenAI o cualquier punto de conexión compatible con OpenAI). No se incluye ninguna clave de API integrada y Tabular Editor no proporciona ni intermedia ningún servicio de IA.

**Flujo de datos.** Toda la comunicación entre el asistente de IA y el proveedor de IA se realiza directamente desde el equipo cliente hasta la API del proveedor. No pasan datos por los servidores de Tabular Editor. Lo que se envía depende de lo que solicites y está limitado por cinco recursos de permisos, cada uno de los cuales tiene un nivel de acceso:

| Recurso | Qué abarca | Niveles | Predeterminado |
| -- | -- | -- | -- |
| Metadatos del modelo | Nombres de tablas, columnas y medidas, expresiones, descripciones y elementos similares. La lectura también abarca las estadísticas del Analizador VertiPaq | Denegar / Lectura / Escritura | Lectura |
| Datos del modelo | Valores de datos de tu modelo, como los resultados de las consultas DAX. Requiere una conexión en vivo | Denegar / Leer | Denegar |
| Best Practice Analyzer | Lectura: lee las reglas de las listas y ejecuta el análisis; Escritura: añade o modifica reglas | Denegar / Lectura / Escritura | Lectura |
| Documentos | Sus editores de scripts de C# y de consultas DAX abiertos. Lectura se refiere a su contenido; Escritura es necesaria para crearlos o modificarlos | Denegar / Lectura / Escritura | Escritura |
| Macros | Su biblioteca de macros | Denegar / Lectura / Escritura | Escritura |

El permiso de escritura incluye el de lectura. Los datos del modelo se deniegan de forma predeterminada, ya que los metadatos describen un modelo en el que los valores de los datos son el contenido del modelo.

**Gestión de permisos.** Los permisos son ajustes permanentes, no solicitudes que se presentan cada vez que se realiza una petición. Revíselos y cámbielos en **Herramientas > Preferencias > Funciones de IA > Permisos**, o en el cuadro de diálogo **Herramientas > Servidor MCP...**, que edita el mismo registro. Cuando el chat necesita algo que un permiso no cubre, muestra una tarjeta de permiso en ese momento, y usted responde para el turno, la sesión, el modelo actual o siempre. **Permitir siempre** aumenta el permiso permanente y nunca lo reduce. Los permisos globales se almacenan en el archivo local Preferences.json; los permisos concedidos para un solo modelo se almacenan en el archivo de opciones de usuario (.tmuo) de ese modelo y se aplican únicamente al chat. Si se vuelve a establecer un recurso en **Denegar**, el chat volverá a preguntar.

**Límites del administrador.** En las ediciones Enterprise, Consultancy y Trial, un administrador puede limitar cada recurso mediante [políticas](xref:policies), por separado para el chat y para el servidor MCP, y el límite del MCP solo puede ser inferior. Un límite tiene prioridad sobre cualquier concesión, incluida una que un usuario ya haya otorgado, y la opción correspondiente se muestra como de solo lectura. Estas políticas fallan en modo cerrado: si algún valor de política de nivel Enterprise está presente en un equipo que no tiene licencia para ello, el asistente de IA y el servidor MCP se niegan a iniciarse en lugar de ignorar la política.

**Registro de auditoría.** Tabular Editor 3 escribe un registro local de lo que hicieron el Asistente de IA y el servidor MCP: qué permisos se solicitaron y cómo se respondió a ellos, qué herramientas se ejecutaron y si cada una tuvo éxito, falló o fue rechazada, y el texto completo de cualquier script de C# que el Asistente de IA o un agente ejecutara o enviara para su ejecución, incluidos los scripts que fallaran en tiempo de ejecución o fueran rechazados. No se registran las indicaciones, las respuestas ni los valores de los datos, ni tampoco los scripts que no se compilan ni el texto de los scripts escritos en un documento para que el usuario los ejecute. Los archivos diarios se conservan durante 30 días y se pueden abrir con **Abrir carpeta de auditoría** en **Herramientas > Preferencias > Funciones de IA**. Los administradores pueden redirigir la ubicación y cambiar el período de conservación.

**Almacenamiento de claves API.** Las claves API se almacenan cifradas en el equipo local, en el archivo Preferences.json. Si el módulo de IA no se carga (por ejemplo, porque se excluyó durante la instalación o se deshabilitó por una política), cualquier configuración de clave de API almacenada previamente se borra automáticamente.

**Almacenamiento de conversaciones.** Las conversaciones se almacenan localmente en el equipo cliente en «%LocalAppData%\TabularEditor3\AI\Conversations\». No se envían datos de las conversaciones a los servidores de Tabular Editor.

**Desactivación del asistente de IA.** Puede excluir el componente de funciones de IA durante la instalación, eliminar el proveedor en **Herramientas > Preferencias > Funciones de IA > Asistente de IA** o aplicar una [política](xref:policies) a través del registro de Windows: «DisableAi» desactiva todas las funciones de IA, incluido el servidor MCP, y elimina la configuración del proveedor almacenada, mientras que «DisableAiChat» desactiva únicamente el chat y deja el servidor MCP en funcionamiento.

**Pruebas de penetración.** Se ha realizado una prueba de penetración independiente del asistente de IA. El informe está disponible en nuestro [Centro de cumplimiento](https://trust.tabulareditor.com/).

### Servidor MCP

Tabular Editor 3 puede actuar como servidor MCP (Protocolo de Contexto de Modelo), de modo que un agente de IA que se ejecute en el mismo dispositivo pueda trabajar en el modelo que tengas abierto. Consulta @mcp-server para obtener información sobre la propia función.

**Exposición de la red.** El servidor es un «listener» HTTP vinculado explícitamente a «127.0.0.1», de forma predeterminada en el puerto 42100. No se puede acceder a él desde otro equipo. Las solicitudes del navegador que llevan un encabezado «Origin» no local se rechazan como medida de defensa contra el «rebinding» de DNS. El servidor se ejecuta solo después de que lo inicies, o desde el inicio de la aplicación si lo has solicitado.

**Autenticación.** La vinculación de bucle invertido es el límite predeterminado, por lo que el servidor acepta conexiones locales sin credenciales de forma automática. En un host en el que varias personas han iniciado sesión a la vez, como un Escritorio remoto o un servidor Citrix, eso no es suficiente: cualquier sesión en el equipo llega a «127.0.0.1». Mientras el token esté desactivado, cualquier proceso del equipo puede conectarse sin credenciales. Active **Requerir token de acceso** en **Herramientas > Preferencias > Funciones de IA > Servidor MCP**. Los clientes deberán presentar un token al portador, que se almacena cifrado en el archivo local Preferences.json. Los administradores pueden imponer esto con la [directiva](xref:policies) «RequireMcpAccessToken».

**Flujo de datos.** Tabular Editor no se pone en contacto con ningún proveedor de IA para esta función y no dispone de ninguna clave de API para ella. El agente es la única parte que se comunica con un proveedor, con su propia configuración y su propia suscripción. Lo que el agente puede leer del modelo está limitado por los mismos cinco permisos que rigen el Asistente de IA, de los que se toma una instantánea cuando se inicia el servidor, y cualquier herramienta que no esté cubierta por un permiso nunca se ofrece al agente. Los datos del modelo se deniegan de forma predeterminada, por lo que ningún resultado de consulta DAX sale del modelo a menos que lo concedas explícitamente. Los valores introducidos en la definición del modelo, como una expresión «DATATABLE» o una tabla Introducir datos, son metadatos del modelo y están cubiertos por el permiso de metadatos del modelo.

**Cambios en el modelo.** Un agente solo puede cambiar el modelo a través del motor de scripting de C# Script, de forma atómica y como un único paso de deshacer, y únicamente con el permiso de metadatos del modelo en Escritura. La ejecución de TMSL y XMLA en bruto nunca está disponible para un agente, y nunca se ejecuta para él un script que se extienda más allá del modelo.

**Registro de auditoría.** Las decisiones sobre permisos, las llamadas a herramientas y el texto completo de cualquier script de C# que un agente haya ejecutado o enviado para su ejecución se registran en un registro de auditoría local. No se registran las indicaciones, las respuestas ni los valores de los datos.

**Deshabilitar el servidor MCP.** Desactive **Habilitar servidor MCP** en **Herramientas > Preferencias > Funciones de IA > Servidor MCP**, o aplique la [política](xref:policies) «DisableMcpServer» o «DisableAi». El servidor forma parte del componente de funciones de IA, por lo que, si se excluye ese componente durante la instalación, también se elimina el servidor.

### Solicitudes web

Tabular Editor puede realizar solicitudes a recursos en línea (URL web) únicamente en los siguientes casos:

- **Activación de la licencia\*.** Cuando se inicia Tabular Editor 3 por primera vez, y a intervalos periódicos a partir de entonces, la herramienta puede realizar una solicitud a nuestro servicio de licencias. Esta solicitud contiene información cifrada sobre la clave de licencia introducida por el usuario, la dirección de correo electrónico del usuario (si se proporciona), el nombre del equipo local y un hash codificado unidireccional que identifica la instalación actual. No se transmiten otros datos en esta solicitud. El propósito de esta solicitud es activar y validar la clave de licencia utilizada por la instalación, hacer cumplir las limitaciones de la versión de prueba, así como permitir al usuario gestionar sus instalaciones de Tabular Editor 3 a través de nuestro servicio de licencias.
- **Comprobaciones de actualizaciones\*.** Cada vez que se inicia Tabular Editor 3, puede realizar una solicitud a nuestro servicio de aplicaciones para determinar si hay una versión más reciente de Tabular Editor 3 disponible. Esta solicitud no contiene ningún dato.
- **Telemetría de uso\*.** De forma predeterminada, Tabular Editor 3 recopila y transmite datos de uso anónimos a medida que los usuarios interactúan con la herramienta. Estos datos incluyen información sobre los objetos de la interfaz de usuario con los que interactúa un usuario y el momento en que lo hace. También contiene información de alto nivel sobre el modelo de datos tabulares que se está editando a través de la herramienta. Esta información solo se refiere a propiedades de alto nivel, como el nivel y el modo de compatibilidad, el número de tablas, el tipo de servidor (Analysis Services frente a Power BI frente a Power BI Desktop), etc. **No se recopilan datos de identificación personal de esta manera**, ni tampoco recopilamos información sobre los nombres de los objetos o las expresiones DAX en el propio Tabular Object Model. Un usuario puede optar por no enviarnos datos de telemetría en cualquier momento.
- **Informes de errores\*.** Cuando se produce un error inesperado, transmitimos el seguimiento de la pila y el mensaje de error (anonimizado), junto con una descripción opcional proporcionada por el usuario. Si un usuario opta por no enviar datos de telemetría, tampoco se enviarán los informes de errores.
- **Uso del formateador de DAX.** (Solo en Tabular Editor 2.x) Se puede formatear una expresión DAX haciendo clic en un botón de Tabular Editor. En este caso, la expresión DAX (y nada más) se envía al servicio web www.daxformatter.com. La primera vez que un usuario hace clic en este botón, se muestra un mensaje de advertencia explícito en el que se le pide que confirme su intención. Tabular Editor 3 no realiza solicitudes web al formatear código DAX.
- **Optimizador de DAX**. Si un usuario tiene una [cuenta de Tabular Tools](https://tabulartools.com) con una suscripción al [Optimizador de DAX](https://daxoptimizer.com), podrá navegar por su espacio de trabajo del Optimizador de DAX, ver problemas y sugerencias, y cargar nuevos archivos VPAX directamente desde Tabular Editor 3. Los archivos VPAX contienen metadatos y estadísticas del modelo, pero no *datos* reales del modelo. La función de integración de DAX Optimizer en Tabular Editor 3 genera varias solicitudes a uno o más de los siguientes puntos finales (en función del tipo de autenticación y de la región especificados al crear la cuenta de Tabular Tools).<br/>
  Para obtener más información, consulta la [documentación de DAX Optimizer](https://docs.daxoptimizer.com/legal/data-processing).<br/>
  Puntos finales utilizados:
  - https://account.tabulartools.com
  - https://licensing.api.daxoptimizer.com/api
  - https://australiaeast.api.daxoptimizer.com/api
  - https://eastus.api.daxoptimizer.com/api
  - https://westeurope.api.daxoptimizer.com/api
- **Asistente de IA.** Cuando el Asistente de IA está configurado y en uso, Tabular Editor 3 envía solicitudes directamente a la API del proveedor de IA configurado. Los puntos de conexión dependen del proveedor seleccionado (por ejemplo, «https://api.openai.com» para OpenAI, «https://api.anthropic.com» para Anthropic o un punto de conexión especificado por el usuario para Azure OpenAI y proveedores personalizados). En estas solicitudes solo se incluyen los datos cubiertos por las concesiones de permisos. Consulta la sección [Asistente de IA](#ai-assistant) anterior para conocer los recursos y sus valores predeterminados.
- **Actualizaciones de la base de conocimientos de IA.** La base de conocimientos en la que busca el asistente de IA es una base de datos local que se incluye con el componente de características de IA. Tabular Editor 3 busca una copia más reciente y la descarga desde «https://cdn.tabulareditor.com». La solicitud no contiene datos sobre ti ni sobre tu modelo.
- **Catálogo de modelos de IA.** Cuando un usuario abre la lista de modelos del proveedor OpenAI o Anthropic, Tabular Editor 3 descarga la lista de modelos disponibles desde «https://api.tabulareditor.com/AiModels» y la almacena en caché en «%LocalAppData%\TabularEditor3\AiModels.json» durante 24 horas. La solicitud es anónima y no contiene datos sobre usted, su clave de API ni su modelo. La directiva «DisableUpdates» la desactiva.
- **Servidor MCP.** El servidor MCP no realiza solicitudes salientes. Solo acepta conexiones en la interfaz de bucle invertido, y el agente que se conecta a él es el que se comunica con un proveedor de IA, según su propia configuración. Consulta la sección [Servidor MCP](#mcp-server) anterior.
- **Importación de reglas de buenas prácticas.** Tabular Editor dispone de una función que permite al usuario especificar una URL desde la que recuperar una lista de reglas de buenas prácticas en un formato basado en JSON. Este tipo de solicitud solo descarga los datos JSON de la URL; no se transmiten datos a la URL.
- **Uso de scripts de C#.** Tabular Editor permite a los usuarios escribir y ejecutar código escrito en C# con fines de automatización. Dicho script puede conectarse potencialmente a recursos en línea, utilizando las características del lenguaje C# y el tiempo de ejecución de .NET. El usuario es siempre responsable de garantizar que el código ejecutado no provoque ningún intercambio involuntario de datos. Tabular Editor ApS no se hace responsable de ningún daño, pérdida o filtración causados por el uso de la función de C# Script en general. Tabular Editor nunca ejecutará scripts de C# sin la acción explícita del usuario.

\***Cualquier información que obtengamos a través del servicio de activación de licencias, la telemetría de uso o los informes de errores se mantiene confidencial. No compartiremos, publicaremos ni distribuiremos los datos recopilados de ninguna manera, forma o modo.**

**Lista de elementos permitidos/lista de elementos aceptados del cortafuegos**
Para permitir el tráfico hacia las solicitudes web mencionadas anteriormente, tendrás que incluir en la lista blanca:
- Activación de licencias / Comprobaciones de actualización / Catálogo de modelos de IA: **https://api.tabulareditor.com**
- Telemetría de uso / Informes de errores: **https://*.in.applicationinsights.azure.com**
- Formateador DAX (solo Tabular Editor 2.x): **https://www.daxformatter.com**
- Importar reglas de buenas prácticas / scripts C#: depende del contexto
- Optimizador de DAX: puntos de conexión enumerados anteriormente.
- Asistente de IA: depende del proveedor configurado (por ejemplo, **https://api.openai.com**, **https://api.anthropic.com** o puntos de conexión de Azure OpenAI/personalizados especificados por el usuario).
- Actualizaciones de la base de conocimientos de IA: **https://cdn.tabulareditor.com**
- Servidor MCP: nada. Escucha en **127.0.0.1** y no realiza ninguna solicitud saliente.

> [!NOTE]
> Un administrador del sistema puede aplicar ciertas [políticas](xref:policies), que se pueden utilizar para desactivar algunas o todas las funciones que se muestran en la lista anterior.

## Seguridad de la aplicación

Tabular Editor no requiere ningún privilegio elevado en el equipo Windows en el que está instalado, ni accede a ningún recurso restringido del equipo. Una excepción a esta regla se da si se utiliza el archivo de instalación de Tabular Editor (.msi), en cuyo caso el ejecutable y los archivos de soporte que requiere la herramienta se copian de forma predeterminada en la carpeta «Archivos de programa», que normalmente requiere permisos elevados. Tanto los archivos binarios de Tabular Editor como el archivo del instalador se han firmado con un certificado de firma de código emitido a Tabular Editor ApS, lo que constituye su garantía de que ningún tercero ha manipulado el código.

Cuando la aplicación se está ejecutando, todos los accesos a recursos externos se realizan a través de la biblioteca cliente AMO/TOM o de las solicitudes web mencionadas anteriormente.

La función de C# Script permite a Tabular Editor ejecutar código C# arbitrario dentro del tiempo de ejecución de .NET. Dicho código solo se compila y ejecuta a petición explícita del usuario. Los C# Scripts también se pueden guardar como «macros», lo que facilita al usuario la gestión y ejecución de varios scripts diferentes. El código se almacena en la carpeta «%localappdata%» del propio usuario, lo que garantiza que solo él o un administrador del equipo local puedan acceder a los scripts. El usuario es siempre responsable de garantizar que el código ejecutado no provoque ningún efecto secundario no deseado. Bajo ninguna circunstancia se podrá considerar a Tabular Editor ApS responsable de ningún daño, pérdida o filtración causados por el uso de las funciones de C# Script o de las acciones/macros personalizadas.

Las organizaciones que no quieran dejar esto en manos de cada usuario pueden gestionarlo de forma centralizada. Las [políticas](xref:policies) «DisableCSharpScripts» y «DisableMacros» desactivan por completo las funciones, en todas las ediciones. Con Tabular Editor 3 Edición Enterprise, «BlockUnsafeScripts» mantiene disponible el scripting, pero solo permite scripts y macros que se queden dentro del modelo semántico: cualquier elemento que lea o escriba un archivo, acceda a la red, inicie otro programa o cargue código externo se rechaza antes de ejecutarse, independientemente de la procedencia del script: un documento de script, Best Practice Analyzer, una macro, el Asistente de IA, el servidor MCP o la línea de comandos. Consulte [Políticas de administrador](xref:csharp-scripts#administrator-policies).
