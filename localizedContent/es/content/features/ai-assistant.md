---
uid: ai-assistant
title: Asistente de IA
author: Morten Lønskov
updated: 2026-09-17
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.26.0
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Asistente de IA

El Asistente de IA es una interfaz de chat para el desarrollo de modelos semánticos asistido por IA, diseñada para ayudarte a crear modelos semánticos con mayor rapidez. Con un diseño preparado para entornos empresariales, control total sobre lo que se envía a la IA y gestión del consentimiento integrada, puedes usar el Asistente de IA con confianza. El Asistente de IA se ha sometido a pruebas de penetración de seguridad independientes. Para más detalles, visita el [Centro de confianza de Tabular Editor](https://trust.tabulareditor.com). Puede explorar los metadatos de tu modelo, escribir y ejecutar consultas DAX, generar C# Scripts, ejecutar comprobaciones del Best Practice Analyzer, consultar estadísticas del Analizador VertiPaq y buscar en la base de conocimientos de Tabular Editor.

El Asistente de IA utiliza un modelo BYOK de clave aportada por el usuario. Tú proporcionas una clave de API de uno de los proveedores compatibles y el asistente se ejecuta directamente a través de la API de ese proveedor.

There is a second way in that needs no key at all. From 3.27.0 Tabular Editor 3 can act as an MCP server, so an agent you already subscribe to, such as Claude Code, GitHub Copilot, VS Code agent mode, Codex or Cursor, works on the open model through the same tools and the same permissions as the chat. See @mcp-server. The two share one permission record, so whichever you use, you set the boundaries once.

> [!NOTE]
> El Asistente de IA está en vista previa pública a partir de Tabular Editor 3.26.0. Agradecemos tus comentarios sobre la experiencia mientras seguimos mejorándola.

![The AI Assistant pane as it first opens, with the assistant's greeting listing what it can do - answer questions, query the model, write and execute C# scripts, change the model - and what it cannot, above an empty message box](~/content/assets/images/ai-assistant/ai-assistant-panel-first-open.png)

## Getting Started

1. Open **Tools > Preferences > AI Features > AI Assistant**
2. Select your AI provider (on a fresh install this defaults to **None (AI disabled)**), then enter your API key
3. Abre el panel del Asistente de IA desde **Vista > Asistente de IA**
4. Escribe mensajes y pulsa **Enter** para iniciar una conversación

The model the assistant is using is shown in the status strip directly above the message box. See [Choosing a model](#choosing-a-model) to change it without leaving the chat.

> [!TIP]
> Usa nuestra [demo interactiva del Asistente de IA](https://demos.tabulareditor.com/psl/of150vcy?) para ver cómo configurarlo y usarlo.

> [!NOTE]
> Las claves de API se almacenan cifradas en tu equipo local.

## Proveedores compatibles

Configure your AI provider under **Tools > Preferences > AI Features > AI Assistant > AI Provider**. Select a provider from the dropdown (the default is **None (AI disabled)** until you configure one), enter your API key and optionally override the default model.

Leave the model field blank to use the provider's default model. For OpenAI and Anthropic the defaults are listed in the table below; Azure OpenAI and the Custom provider have no default, so those two always need a value.

| Proveedor                                                | Modelo predeterminado                                  | Configuración necesaria                                                                |
| -------------------------------------------------------- | ------------------------------------------------------ | -------------------------------------------------------------------------------------- |
| OpenAI                                                   | gpt-5.5                                | Clave de API. URL base, ID de organización e ID de proyecto opcionales |
| Anthropic                                                | claude-sonnet-4-6                                      | Clave de API. URL base opcional                                        |
| Azure OpenAI                                             | Ninguno. A deployment name is required | Clave de API, URL del punto de conexión y nombre de la implementación                  |
| Personalizado (compatible con OpenAI) | Ninguno. A model name is required      | Clave de API y URL personalizada del punto de conexión                                 |

![The AI Provider preferences page with the Choose provider dropdown open on None (AI disabled), OpenAI, Anthropic, Azure OpenAI and Custom (OpenAI-compatible), and a URL and API Key field beneath it](~/content/assets/images/ai-assistant/ai-assistant-provider-preferences.png)

### Choosing a model

The active model is shown in the status strip above the message box, next to the context usage bar. Click it to open a picker listing the models currently available for the configured provider; choosing one applies to every request that follows, with no dialog and no restart. The last entry, **Preferences...**, opens **Tools > Preferences > AI Features > AI Assistant** for anything not on the list.

![The model picker open above the message box, listing claude-sonnet-5, claude-fable-5-1, claude-fable-5, claude-opus-5, claude-haiku-4-5, claude-opus-4-8 and the active claude-sonnet-4-6 in bold, with Preferences... beneath a separator](~/content/assets/images/ai-assistant/ui-model-picker.png)

Where there is no list to offer (a Custom or Azure OpenAI deployment name, or a machine where the model list has never been retrieved), the model name is a plain link to those same preferences instead of a picker.

> [!NOTE]
> The indicator is hidden until a provider, an API key and a model are all in place.

### OpenAI

Selecciona **OpenAI** como proveedor e introduce tu clave de API. Opcionalmente, puedes especificar un ID de organización y un ID de proyecto si tu cuenta de OpenAI los usa. The default model is **gpt-5.5**, but you can change it to any model available on your account.

![The AI Provider preferences page with OpenAI selected, a masked API key, empty Organization ID and Project ID fields, and the model name](~/content/assets/images/ai-assistant/ai-assistant-openai-config.png)

### Anthropic

Selecciona **Anthropic** como proveedor e introduce tu clave de API. El modelo predeterminado es **claude-sonnet-4-6**. Puedes cambiar el nombre del modelo a cualquier modelo de Anthropic disponible en tu cuenta.

![The AI Assistant preferences page with Anthropic selected as the provider, the base URL https://api.anthropic.com, a masked API key and claude-sonnet-4-6 as the model name](~/content/assets/images/ai-assistant/ai-assistant-anthropic-config.png)

> [!IMPORTANT]
> Anthropic aplica límites de velocidad de tokens de entrada por minuto (ITPM) en función del nivel de tu cuenta. Una nueva clave de API empieza en el Nivel 1 con 30.000 ITPM para Claude Sonnet 4.x. Una sola solicitud a un modelo grande puede superar este límite. Compra 40 USD o más en créditos de API para alcanzar el Nivel 2 (450.000 ITPM). Consulta la [documentación de límites de velocidad de Anthropic](https://docs.anthropic.com/en/api/rate-limits) para ver todos los detalles de los niveles.

### Azure OpenAI

Selecciona **Azure OpenAI** como proveedor y configura tres campos:

- **API key**: the access key for your Azure OpenAI resource
- **Service endpoint**: the endpoint URL for your resource, for example `https://your-resource.openai.azure.com`. Usa la URL del recurso, no el alias `privatelink`; el certificado SSL se emite para `*.openai.azure.com` y, si te conectas directamente a `*.privatelink.openai.azure.com`, fallará la validación del certificado
- **Deployment**: the **deployment name**, not the underlying model name and not the resource name

Azure OpenAI requiere el nombre de la implementación en cada llamada a la API. El nombre de la implementación se elige al crearla, así que puede ser cualquier cadena. Las implementaciones suelen llevar el nombre del modelo al que sirven (por ejemplo, `gpt-4o`), pero es una convención, no un requisito. Si introduces el nombre del recurso o un nombre de modelo que no exista como implementación, la solicitud fallará.

#### Cómo encontrar el nombre de tu implementación

En el [portal de Azure AI Foundry](https://ai.azure.com):

1. Inicia sesión y selecciona tu recurso de Azure OpenAI
2. Abre **Implementaciones** (o **Modelos + puntos de conexión** si el recurso se ha actualizado a Foundry)
3. Copia el valor de la columna **Nombre**

Es posible que las implementaciones creadas antes de que tu organización adoptara Azure AI Foundry no aparezcan en el portal. Enuméralas desde la CLI de Azure:

```bash
az cognitiveservices account deployment list --name "<resource-name>" --resource-group "<resource-group>" --output table
```

Consulta [Crear y desplegar un recurso de Azure OpenAI](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/create-resource#deploy-a-model) para más detalles.

Para errores 403, fallos de SSL o respuestas "DeploymentNotFound", consulta @azure-openai-connection-errors.

> [!NOTE]
> El proveedor **Azure OpenAI** es para recursos clásicos de Azure OpenAI que usan el parámetro de consulta `api-version`. Si usas el nuevo **Microsoft Foundry**, consulta [Uso de Microsoft Foundry](#using-microsoft-foundry) más abajo.

### Personalizado (compatible con OpenAI)

La opción de proveedor Personalizado admite LLM locales o de tu organización que expongan un punto de conexión de API compatible con OpenAI. Introduce tu clave de API y la URL del punto de conexión personalizado. Esto te permite mantener todos los datos dentro de tu propia infraestructura por motivos de privacidad o requisitos de cumplimiento.

### Uso de un LLM local o de tu organización

Puedes ejecutar el Asistente de IA con un LLM autoalojado mediante el proveedor Personalizado. This keeps all data within your own infrastructure, whether that is a model running on your local machine or a centrally hosted LLM within your organization's network. En cualquier caso, no se envía ningún dato a un proveedor de nube de terceros.

Varias herramientas pueden alojar modelos con una API compatible con OpenAI:

- [Ollama](https://ollama.com): lightweight CLI for downloading and running models locally
- [LM Studio](https://lmstudio.ai): desktop application with a graphical interface for managing and running local models
- [LocalAI](https://localai.io): self-hosted, community-driven alternative with broad model support

Estas herramientas pueden ejecutarse en la estación de trabajo de un desarrollador para uso individual o implementarse en un servidor compartido dentro de tu organización para ofrecer a tu equipo un punto de conexión de LLM gestionado de forma centralizada.

#### Ejemplo: Ollama

1. [Descarga e instala Ollama](https://ollama.com/download)
2. Descarga un modelo, por ejemplo: `ollama pull llama3.1`
3. Inicia el servidor de Ollama (se ejecuta automáticamente tras la instalación y, de forma predeterminada, en el puerto 11434)
4. In Tabular Editor, go to **Tools > Preferences > AI Features > AI Assistant > AI Provider**
5. Configura **Elegir proveedor** como **Personalizado (compatible con OpenAI)**
6. Establece **Punto de conexión del servicio** en `http://localhost:11434/v1`
7. Establece **Nombre del modelo** con el modelo que descargaste (p. ej., `llama3.1`)
8. The **API Key** field can be set to any non-empty value (e.g. `ollama`). Ollama does not require authentication, but the field cannot be left blank

#### Ejemplo: LM Studio

1. [Descargar LM Studio](https://lmstudio.ai/download)
2. Descarga un modelo. Ya sea desde la página de búsqueda de modelos del panel izquierdo o mediante la CLI. Por ejemplo: `lms get lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF`
3. Inicia el servidor de LM Studio. Ya sea desde la página para desarrolladores del panel izquierdo o mediante la CLI. por ejemplo `lms server start`
   Nota: tendrás que configurarlo para que use el modo compatible con OpenAI. Además, puede que tengas que cambiar el tamaño de contexto predeterminado para que sea superior a 100000 tokens.
4. In Tabular Editor, go to **Tools > Preferences > AI Features > AI Assistant > AI Provider**
5. Configura **Elegir proveedor** como **Personalizado (compatible con OpenAI)**
6. Establece **Punto de conexión del servicio** en `http://localhost:1234/v1`
7. Establece **Nombre del modelo** con el modelo que descargaste (p. ej., `lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF`)
8. The **API Key** field can be set to any non-empty value (e.g. `lms`). LM Studio does not require authentication, but the field cannot be left blank

> [!NOTE]
> La calidad de las respuestas con modelos locales depende del tamaño del modelo y de tu hardware. Los modelos más grandes suelen producir mejores resultados, pero requieren más RAM y una GPU capaz. Las capacidades de llamada a herramientas del Asistente de IA requieren un modelo que admita llamadas a funciones en el formato compatible con OpenAI.

> [!TIP]
> We recommend a model with a _minimum_ of 30 billion parameters but ideally at least 100 billion parameters. Por ejemplo, el modelo Qwen3.5-122B-A10B funcionó bien en nuestras pruebas internas.

### Uso de Microsoft Foundry

[Microsoft Foundry](https://ai.azure.com) (antes llamado Azure AI Foundry) te permite desplegar modelos de OpenAI y Anthropic en tu entorno de Azure. These models are accessed through the **OpenAI** or **Anthropic** provider in Tabular Editor, not the **Azure OpenAI** provider, which is for classic Azure OpenAI resources.

> [!IMPORTANT]
> No uses el proveedor **Azure OpenAI** para modelos de Microsoft Foundry. El proveedor **Azure OpenAI** solo es compatible con recursos clásicos de Azure OpenAI.

#### Modelos de OpenAI en Microsoft Foundry

Para usar un modelo de OpenAI (como GPT-4o o GPT-5.4-mini) desplegado en Microsoft Foundry:

1. In Tabular Editor, go to **Tools > Preferences > AI Features > AI Assistant > AI Provider**
2. Selecciona **OpenAI** en **Elegir proveedor**
3. Configura **URL base** con el punto de conexión del recurso de Foundry y añade `/openai/v1` al final. La URL sigue uno de estos formatos:
   - `https://your-resource.services.ai.azure.com/openai/v1`
   - `https://your-resource.openai.azure.com/openai/v1`
4. Introduce tu **Clave de API** de Foundry
5. Configura **Nombre del modelo** como el nombre de tu implementación (por ejemplo, `gpt-5.4-mini`)

> [!NOTE]
> La URL base no se muestra directamente en el portal de Microsoft Foundry. El portal muestra un **URI de destino** que incluye la ruta completa de la API (por ejemplo, `https://your-resource.services.ai.azure.com/api/projects/YourProject/openai/v1/responses`). Para la URL base, usa solo `https://your-resource.services.ai.azure.com/openai/v1`.

#### Modelos de Anthropic en Microsoft Foundry

Para usar un modelo de Anthropic (como Claude Sonnet 4,6) desplegado en Microsoft Foundry:

1. In Tabular Editor, go to **Tools > Preferences > AI Features > AI Assistant > AI Provider**
2. Configura **Elegir proveedor** como **Anthropic**
3. Establece **URL base** en el punto de conexión de tu recurso de Foundry, con `/anthropic` añadido al final; por ejemplo: `https://your-resource.services.ai.azure.com/anthropic`
4. Introduce tu **Clave de API** de Foundry
5. En **Nombre del modelo**, introduce el identificador del modelo (p. ej., `claude-sonnet-4-6`)

> [!NOTE]
> El portal muestra un **URI de destino** como `https://your-resource.services.ai.azure.com/anthropic/v1/messages`. Para la URL base, usa solo la parte hasta `/anthropic` inclusive.

## Capacidades

El Asistente de IA tiene acceso al contexto de tu modelo y puede realizar las siguientes acciones:

- **Exploración del modelo**: Consultar los metadatos del modelo, incluidas tablas, columnas, medidas, relaciones y sus propiedades
- **Redacción de Consultas DAX**: Generar Consultas DAX y ejecutarlas contra tu modelo en modo conectado, devolviendo conjuntos de resultados directamente en el chat
- **C# script generation**: Create C# scripts for model modifications. The assistant either opens the script in a new editor window for you to run, or carries the change out itself, depending on your settings. See [Letting the assistant change your model](#letting-the-assistant-change-your-model). Los cambios en los metadatos del modelo se pueden deshacer con **Ctrl+Z**
- **Best Practice Analyzer**: Ejecutar el análisis de BPA, ver infracciones de las reglas y crear o modificar reglas de BPA
- **Analizador VertiPaq**: Consultar estadísticas de uso de memoria y cardinalidad de columnas
- **Acceso a documentos**: Leer y modificar documentos abiertos, como scripts DAX y Consultas DAX
- **Búsqueda en la base de conocimientos**: Buscar en la documentación integrada de Tabular Editor para encontrar respuestas
- **Navegación por la interfaz de usuario**: Generar enlaces de acción `te3://` que abren cuadros de diálogo y funcionalidades específicas de Tabular Editor

An agent connected over the [MCP server](xref:mcp-server) is offered the same capabilities, with one exception: UI navigation is chat-only. Both surfaces can change your model by running a C# script, and both do it as a single undoable step. What differs is how the change is put to you, and how permission is settled. See [What the MCP server shares, and what it does not](#what-the-mcp-server-shares-and-what-it-does-not).

> [!NOTE]
> Tools that require an active database connection, including DAX query execution and VertiPaq Analyzer statistics, are automatically hidden when working with a model file (for example a `.bim` or `.tmdl` folder) that is not connected to Analysis Services or Power BI. The assistant still writes DAX queries for you, but the **Execute** button on DAX query artifacts is disabled until a connection is established. Las estadísticas del Analizador VertiPaq siguen estando disponibles si se cargaron previamente desde un archivo `.vpax`.

## Letting the assistant change your model

By default the assistant writes a C# script and opens it in an editor window for you to read and run. From Tabular Editor 3.27.0 it can carry the change out itself instead.

Tick **Allow AI assistant to run C# scripts directly** under **Tools > Preferences > AI Features > AI Assistant**. The setting is off until you turn it on, and the checkbox is unavailable until **Model metadata** is set to **Write** under **Tools > Preferences > AI Features > Permissions**.

### What happens when the assistant runs a script

- **You see the change first.** With **Preview changes** on, which is the default, the [preview dialog](xref:csharp-scripts#run-c-scripts-with-preview) appears before anything stands. Choosing **Cancel** puts the model back and tells the assistant you rejected the change, so it asks what to do differently rather than trying the same thing again. With the preference off, the change is applied without a dialog.
- **One undo step.** Everything the script did collapses into a single entry named _C# script (AI Assistant)_. One **Ctrl+Z** puts the model back.
- **All or nothing.** A script that fails part way through leaves the model untouched, and the assistant reports the error rather than leaving you with half an edit.
- **Only model work runs this way.** A script that reaches for files, the network or an external assembly is never executed for you. It comes back as a script artifact carrying an **Unsafe** badge with **Execute** disabled, and the assistant tells you what it used.

Asking for a script rather than for the change still gives you a script. _Write me a script that renames every measure to sentence case_ opens a script document for you to run yourself, whatever this setting says.

Administrators can prevent this entirely with the `DisableCSharpScripts` [policy](xref:policies), which also stops the assistant writing scripts for you to run.

They can also allow scripting but keep it inside the model, with the `BlockUnsafeScripts` policy. Under it a script that reaches for files, the network or an external assembly is refused outright rather than handed to you for review, wherever it came from. See [Administrator policies](xref:csharp-scripts#administrator-policies).

## Conversaciones

El Asistente de IA admite varias conversaciones simultáneas. Cada conversación mantiene su propio historial de mensajes y contexto.

- Las conversaciones se conservan entre sesiones y se almacenan localmente en `%LocalAppData%\TabularEditor3\AI\Conversations\`
- Los títulos se generan automáticamente tras el primer intercambio. Puedes cambiar el nombre de las conversaciones manualmente
- **Auto-compaction**: when the conversation approaches the context window limit, older messages are automatically summarized to free up space. A snapshot of the full conversation is archived before compaction. The threshold is set under [Context Compaction](#context-compaction), and is a percentage of the model's own context window

### Deleting a conversation

**Delete conversation** sits at the left-hand end of the AI Assistant toolbar, next to **New conversation**. It asks for confirmation first.

The conversation and its history are removed from disk and cannot be recovered. To hide the AI Assistant panel instead of deleting anything, use the close button on the panel's title bar, or **View > AI Assistant**.

## Artefactos

Cuando el Asistente de IA genera código, crea **artefactos** que se abren directamente en ventanas del editor:

- **C# Scripts**: Se abren en un nuevo editor de C# Script con resaltado de sintaxis, compilación y compatibilidad con la ejecución
- **Consultas DAX**: Se abren en un nuevo editor de consultas DAX con resaltado de sintaxis y compatibilidad con la ejecución

Los artefactos se transmiten en tiempo real a medida que la IA los genera. Los artefactos de C# Script incluyen un análisis de seguridad que señala código potencialmente inseguro (p. ej., acceso al sistema de archivos u operaciones de red).

![The AI Assistant pane showing a generated C# script artifact with an Execute button, and the assistant's explanation of what the script does and the case-sensitivity caveat it comes with](~/content/assets/images/ai-assistant/ai-assistant-generate-c-sharp-script.png)

Cuando ejecutas un C# Script desde el chat, el cuadro de diálogo **Vista previa del script** muestra una comparación en paralelo de todos los cambios de metadatos del modelo realizados por el script. Puedes aceptar los cambios o revertirlos. Consulta [Ejecutar scripts con vista previa](xref:csharp-scripts#run-c-scripts-with-preview) para obtener más información.

![The Script Preview - Model Changes dialog, the model before and after side by side, with the Internet Total Freight measure's format string changed and a description and a display folder added, each marked against its original](~/content/assets/images/preview-script-changes.png)

## Instrucciones personalizadas

Las instrucciones personalizadas son conjuntos de instrucciones que guían el comportamiento del Asistente de IA para tareas específicas. The assistant is given a list of every available instruction and only loads the full text of the ones it judges relevant to your request. Once an instruction has been loaded it stays in effect for the rest of the conversation.

> [!IMPORTANT]
> The `description` is now the only thing the assistant reads when deciding if an instruction should be used, so keep yours accurate and specific.

### Instrucciones personalizadas integradas

El Asistente de IA incluye las siguientes instrucciones personalizadas integradas:

| Instrucción personalizada              | Invoke with           | Covers                                                                                                                                               |
| -------------------------------------- | --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Consulta DAX                           | `/dax-querying`       | Writing and executing DAX queries: column and measure qualification, verifying filter values, validating and updating queries        |
| Modificación del modelo                | `/model-modification` | C# scripts that create or change model objects: TOMWrapper API patterns, execution order, idempotent updates, naming rules           |
| Semantic Model Design                  | `/model-design`       | Star schema, relationships and cross-filtering, date tables, measures versus calculated columns, calculation groups, naming                          |
| Semantic Model Organization            | `/organize-model`     | Auditing and tidying model metadata: naming conventions, table groups, display folders, hidden columns, format strings, descriptions |
| Semantic Model Size Optimization       | `/optimize-model`     | Reducing model memory and size: VertiPaq measurement, column removal, data type tuning, structural changes, SKU limits               |
| Macros                                 | `/macros`             | Reusable C# macros for the Macros window: selection contexts, generic-code rules                                                     |
| Funciones DAX definidas por el usuario | `/udf`                | Writing DAX UDFs: syntax, `VAL`/`EXPR` parameter modes, type hints, namespaces, DaxLib                                               |
| Best Practice Analyzer                 | `/bpa`                | Reviewing violations and writing custom rules as LINQ Dynamic expressions                                                                            |

Las instrucciones personalizadas se muestran como indicadores encima de las respuestas del asistente, lo que indica qué instrucciones influyeron en la respuesta. You can toggle this display in **Tools > Preferences > AI Features > AI Assistant > Preferences > Show custom instructions indicator**.

### Invocar una instrucción personalizada

Escribe `/` para explorar las instrucciones personalizadas disponibles, o escribe el `/instruction-id` completo al inicio de tu mensaje para invocar explícitamente una instrucción concreta. Por ejemplo, `/dax-querying` fuerza la instrucción de Consulta DAX independientemente del contenido de tu mensaje. If you type nothing after the `/id`, the assistant is just asked to use that instruction.

Explicit invocation is still worth using when you want to be certain the instruction is applied. An explicitly invoked instruction stays in effect for the rest of the conversation, just as an automatically loaded one does.

### Añade tus propias instrucciones personalizadas

Puedes crear instrucciones personalizadas colocando archivos `.md` en `%LocalAppData%\TabularEditor3\AI\CustomInstructions\`. The folder is created the first time the AI Assistant runs, with an `example.md` file in it to copy from. Use **Open Custom Instructions Folder** on the AI Assistant toolbar to get there.

Each file may open with YAML frontmatter defining the instruction metadata. None of it is required:

```yaml
---
id: my-custom-instruction
name: My Custom Instruction
description: A brief description shown in the autocomplete popup.
priority: 100
always_inject: false
hidden: false
---

Your instruction content goes here. This is the text that will be
injected into the AI's system prompt when the instruction is activated.
```

| Campo           | Obligatorio | Predeterminado                     | Descripción                                                                                                                                 |
| --------------- | ----------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`            | No          | Nombre de archivo sin `.md`        | Identificador único; también se usa como `/id` para la invocación explícita                                                                 |
| `name`          | No          | Title-cased `id`                   | Nombre para mostrar en el autocompletado                                                                                                    |
| `description`   | No          | Si no se especifica, se usa `name` | Indica qué cubre la instrucción y cuándo se aplica                                                                                          |
| `priority`      | No          | 100                                | Los valores más altos se inyectan primero cuando hay varias instrucciones personalizadas en vigor                                           |
| `always_inject` | No          | false                              | Si es `true`, siempre se incluye en el prompt del sistema. Este tipo de instrucción no aparece en el autocompletado de `/.` |
| `hidden`        | No          | false                              | Si es `true`, no se muestra en el autocompletado de `/command`                                                                              |

Las instrucciones personalizadas con un `id` que coincida con el de una instrucción integrada sustituirán la versión integrada.

Notas sobre cómo se leen los archivos:

- El frontmatter debe empezar con `---` en la primera línea del archivo y terminar con una línea `---`. Si no es así, o si no se puede analizar el YAML, todo el archivo se trata como contenido de la instrucción y se aplican todos los valores predeterminados anteriores
- Las claves que no estén en la tabla anterior se ignoran. Esto es lo que hace que una sección `triggers:` sobrante sea inofensiva
- Cualquier `{{version}}` en el cuerpo se reemplaza por la versión del componente de IA de Tabular Editor
- Solo se leen los archivos `.md` que estén directamente en la carpeta; no se buscan subcarpetas

### Instrucciones personalizadas de tu organización

Un administrador puede publicar una carpeta de instrucciones personalizadas para todos mediante la directiva `AiCustomInstructionsPath` [directiva](xref:policies). Puede ser un recurso compartido de red de solo lectura. Esas instrucciones se cargan para cada usuario, además de las integradas, y se usan exactamente igual que cualquier otra: se ofrecen en el autocompletado de `/`, se eligen por su descripción y se invocan con `/id`.

Si el mismo `id` existe en más de un lugar, el que prevalece es:

1. La carpeta de tu organización
2. Tu propia carpeta
3. Las instrucciones integradas

Así, una instrucción de la organización prevalece sobre una integrada y sobre el archivo propio del usuario con el mismo nombre. Una directiva independiente, `DisableUserCustomInstructions`, hace que Tabular Editor ignore por completo las instrucciones de tu propia carpeta y deshabilita **Abrir carpeta de instrucciones personalizadas**; las instrucciones integradas y de la organización se siguen cargando.

Ambas directivas requieren Tabular Editor 3 Edición Enterprise.

## Permisos y consentimiento

Lo que el Asistente de IA puede tocar se rige por _cinco recursos_, cada uno con un nivel de acceso. Las mismas cinco autorizaciones rigen el [servidor MCP](xref:mcp-server), así que hay un único lugar que consultar y un único lugar donde cambiar de opinión.

| Recurso                    | Qué abarca                                                                                                                                                                                        | Niveles                       | Predeterminado |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- | -------------- |
| **Metadatos del modelo**   | Nombres de tablas, columnas y medidas, expresiones, descripciones y elementos similares. El permiso de lectura también incluye las estadísticas del Analizador VertiPaq           | Denegar / Leer / Escribir     | **Leer**       |
| **Datos del modelo**       | Valores de datos de tu modelo, como los resultados de consultas DAX. Requiere una conexión activa                                                                                 | Denegar / Leer                | **Denegar**    |
| **Best Practice Analyzer** | Leer enumera las reglas y ejecuta el análisis; Escribir agrega o modifica reglas                                                                                                                  | Denegar / Lectura / Escritura | **Lectura**    |
| **Documentos**             | Los editores de documentos que tienes abiertos: C# Scripts y consultas DAX. Lectura permite ver su contenido; Escritura es necesaria para crearlos o modificarlos | Denegar / Lectura / Escritura | **Escritura**  |
| **macros**                 | Tu biblioteca de macros. Lectura permite listar y leer macros; Escritura se reserva para futuras herramientas de edición de macros                                                | Denegar / Lectura / Escritura | **Escritura**  |

Un permiso de **Escritura** incluye **Lectura**, así que no hace falta conceder ambos. Los **datos del modelo** son de solo lectura por naturaleza (el asistente puede consultar tus datos, pero no puede escribir valores en ellos), así que solo ofrece Denegar y Lectura.

> [!NOTE]
> Los **datos del modelo** son el único recurso que se deniega de forma predeterminada. Los metadatos describen tu modelo; los datos _son_ el contenido de tu modelo, así que enviarlos a un proveedor de IA es una decisión que conviene tomar de forma deliberada, en lugar de heredar una configuración predeterminada.

Conviene examinar más de cerca tres permisos:

- **Metadatos del modelo > Escritura** permite que el asistente cambie tu modelo. Por sí solo, eso significa escribir un C# Script y dártelo para que lo ejecutes. También es el permiso que hace posible la [ejecución directa](#letting-the-assistant-change-your-model), pero el asistente solo ejecuta scripts por sí mismo una vez que lo has activado por separado. En cualquier caso, solo se ejecutan scripts cuya seguridad puede determinarse estáticamente, y nunca se ejecuta por ti un script que salga del modelo, acceda al sistema de archivos o a la red.
- **Best Practice Analyzer > Lectura** permite que el asistente ejecute el análisis, pero para hacerlo también necesita **Metadatos del modelo > Lectura**, ya que el análisis lee el modelo.
- **Datos del modelo > Lectura** no basta por sí solo para ejecutar una consulta DAX: para eso también hace falta **Metadatos del modelo > Lectura**, porque una consulta puede leer metadatos mediante funciones `INFO`, DMVs y los nombres de columna de su propio resultado.

### Configurar los permisos

Abre **Herramientas > Preferencias > Funciones de IA > Permisos**. Cada recurso tiene un menú desplegable con sus niveles disponibles.

![Funciones de IA > Preferencias de permisos, un menú desplegable por recurso con su configuración predeterminada](~/content/assets/images/pref-ai-permissions.png)

No existe un nivel independiente de "Pregúntame". **Denegar** es, en la práctica, lo que equivale a pedir permiso: en el chat, un recurso al que no le hayas concedido acceso genera una tarjeta de permiso justo cuando se necesita. En MCP, donde no hay nadie a quien preguntar, las herramientas de un recurso denegado no están disponibles.

> [!NOTE]
> Si usaste el Asistente de IA antes de la versión 3.27.0, verás menos avisos. Los metadatos del modelo, los documentos y las macros ahora empiezan en el nivel Lectura o superior, por lo que el chat ya no los solicita. Solo los resultados de consultas DAX y las ediciones de reglas del Best Practice Analyzer siguen generando una tarjeta de forma predeterminada. Establece un recurso en **Denegar** para que vuelva a mostrarse su solicitud.

> [!NOTE]
> En la Edición Enterprise, los administradores de TI pueden establecer directivas que determinen estos permisos. Consulta @policies.

### Tarjetas de permiso en el chat

Cuando el asistente necesita un recurso que tus permisos actuales no cubren, aparece en la conversación una tarjeta de **Permiso requerido** que indica lo que quiere hacer, por ejemplo: "La IA desea acceder a los metadatos de tu modelo semántico", o la consulta DAX que propone ejecutar.

![Una tarjeta de Permiso requerido en el chat, que muestra la consulta DAX que el asistente quiere ejecutar, con los botones Permitir, Permitir para esta sesión, Permitir para este modelo, Permitir siempre y Denegar](~/content/assets/images/ai-assistant/ai-assistant-generate-consent-dialog.png)

| Botón                         | Qué hace                                                                                                                                                                                                                                                                 |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Permitir**                  | Solo esta vez. El asistente puede repetir la misma solicitud mientras termina lo que le pediste, y después no se guarda nada                                                                                                                             |
| **Permitir para esta sesión** | Hasta que se reinicie Tabular Editor. Se mantiene en memoria; nunca se escribe en disco                                                                                                                                                                  |
| **Permitir para este modelo** | Se registra en el archivo de [opciones de usuario](xref:user-options) del modelo, por lo que se aplica la próxima vez que abras este modelo. Solo se ofrece para **Metadatos del modelo** y **Datos del modelo**, y solo mientras haya un modelo cargado |
| **Permitir siempre**          | Aumenta el permiso permanente en la página Permisos, para todos los modelos y todas las sesiones                                                                                                                                                                         |
| **Denegar**                   | Deniega esta solicitud. El asistente continúa sin ese acceso y vuelve a pedirlo la próxima vez                                                                                                                                                           |

**Permitir siempre** solo aumenta un permiso; nunca lo reduce: permitir el acceso de lectura no puede restringir un permiso de escritura que ya tenías.

No tienes que responder a la tarjeta en absoluto. Consulta [Detener un turno mientras hay un permiso pendiente](#stopping-a-turn-while-permission-is-pending) más abajo.

### Lo que comparte el servidor MCP y lo que no

El [servidor MCP](xref:mcp-server) lee los _mismos cinco permisos_, pero no usa el flujo de tarjetas. Un agente que se conecta por MCP se ejecuta sin supervisión, así que no hay nadie a quien preguntar:

- Los permisos se _capturan en una instantánea al iniciar el servidor_ y determinan qué herramientas expone durante toda su ejecución. Cambiar un permiso mientras el servidor está en ejecución no surte efecto hasta que lo reinicies.
- Solo se leen los permisos _globales_. Tanto un permiso que hayas concedido con **Permitir para este modelo** como un permiso de sesión se aplican solo al chat y nunca llegan a un agente MCP.
- Las herramientas de un recurso denegado ni siquiera se ofrecen al agente; no se ofrecen primero para luego denegarse.

### Retirar permisos

Configura de nuevo el recurso en **Denegar** en la página Permisos. El chat volverá a pedirlo la próxima vez que necesite ese recurso; un servidor MCP en ejecución mantiene el acceso con el que se inició hasta que lo reinicies.

Reducir un permiso global no elimina un permiso por modelo. Para retirar uno de ellos, elimina el archivo `.tmuo` del modelo o la entrada `Permissions` dentro de él. Consulta los detalles en @user-options.

### Registro de auditoría

En la Edición Enterprise de Tabular Editor 3, se conserva un registro local de lo que hicieron el Asistente de IA y el [servidor MCP](xref:mcp-server): qué permisos se solicitaron y cómo respondiste, qué herramientas se ejecutaron y si cada una se completó correctamente, falló o fue denegada, y el texto completo de cualquier C# Script que se ejecutó o se te entregó para revisión. Tus indicaciones, las respuestas del asistente y los valores de datos de tu modelo nunca se registran. La opción **Abrir carpeta de auditoría** en **Herramientas > Preferencias > Funciones de IA** te lleva a los archivos.

En Desktop y en la Edición Business, y antes de activar una licencia, no se registra nada, no se crea ninguna carpeta ni se muestra el botón.

Consulta @ai-audit-log para saber qué incluye cada registro, dónde se almacenan los archivos y qué directivas los redirigen.

### Detener un turno mientras el permiso está pendiente

Una tarjeta de **Permiso requerido** espera una respuesta antes de que el asistente pueda continuar. No tienes que responderla: al pulsar **Detener**, el turno finaliza, se elimina la tarjeta y la solicitud se considera denegada. El panel vuelve a su estado normal y puedes continuar en la misma conversación con un mensaje nuevo.

## Preferencias

Configura las opciones de visualización y comportamiento del Asistente de IA en **Herramientas > Preferencias > Funciones de IA > Asistente de IA > Preferencias**.

### Visualización del chat

| Preferencia                                               | Predeterminado | Descripción                                                                                    |
| --------------------------------------------------------- | -------------- | ---------------------------------------------------------------------------------------------- |
| Mostrar indicador de contexto de selección                | true           | Muestra el objeto del modelo seleccionado actualmente en el chat                               |
| Mostrar indicador de instrucciones personalizadas         | true           | Muestra los indicadores de instrucciones personalizadas encima de las respuestas del asistente |
| Mostrar indicador de búsqueda en la base de conocimientos | true           | Muestra el progreso al buscar en la base de conocimientos                                      |

### Compactación de contexto

| Preferencia                         | Predeterminado | Descripción                                                                                                                                                                                             |
| ----------------------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Compactación automática             | true           | Resumir automáticamente los mensajes antiguos al acercarse al límite del contexto                                                                                                                       |
| Umbral de compactación automática % | 80             | Porcentaje de la ventana de contexto del propio modelo a partir del cual se activa la compactación automática. Los valores fuera del intervalo 50-100 no tienen ningún efecto adicional |

### C# Script

| Preferencia                                                     | Predeterminado | Descripción                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| --------------------------------------------------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Permitir que el Asistente de IA ejecute C# Scripts directamente | false          | Permite que el asistente aplique por sí mismo los cambios en el modelo, en lugar de abrir un script para que lo ejecutes. No estará disponible hasta que configures **Metadatos del modelo** en **Escritura** dentro de **Permisos**, y no estará disponible en absoluto con la `DisableCSharpScripts` [policy](xref:policies). Consulta [Dejar que el asistente cambie tu modelo](#letting-the-assistant-change-your-model) |
| Previsualizar cambios                                           | true           | Mostrar el cuadro de diálogo de vista previa de cambios al ejecutar C# Scripts generados por IA desde el chat                                                                                                                                                                                                                                                                                                                                                |

Hay otros dos ajustes en la propia página **Funciones de IA**, encima de **Asistente de IA**, porque también se aplican al servidor MCP: _Buscar actualizaciones de la base de conocimientos al iniciar_ y el botón **Abrir carpeta de auditoría**. Consulta @preferencias.

![La página de preferencias del Asistente de IA, con los tres indicadores de visualización del chat, Compactación automática y su umbral, y los dos ajustes de C# Script: Permitir que el asistente de IA ejecute C# Scripts directamente, desmarcado, y Vista previa de los cambios, marcado](~/content/assets/images/ai-assistant/ai-assistant-preferences.png)

## Uso de tokens

Cada mensaje al Asistente de IA consume tokens de entrada. El coste en tokens de un solo mensaje depende de qué contexto se incluya:

- **Prompt del sistema e instrucciones personalizadas**: Se envían con cada mensaje. Normalmente, entre 5.000 y 15.000 tokens, según las instrucciones personalizadas que estén activas.
- **Metadatos del modelo**: cuando el asistente necesita entender tu modelo, recupera los metadatos mediante llamadas a herramientas. Para mantenerse dentro de los límites de tasa del proveedor en modelos grandes, el asistente usa un enfoque de divulgación progresiva. Es decir, primero obtiene un resumen ligero (nombres de tablas y medidas, relaciones); luego busca objetos relevantes por nombre, descripción o expresión DAX, y solo profundiza en los detalles completos de las tablas u objetos específicos que requiera la pregunta. Los resultados de las herramientas que, de otro modo, serían muy grandes se truncan e incluyen indicaciones sobre cómo el asistente puede recuperar los datos restantes.

### Contador de tokens

El contador de tokens está en la franja de estado situada encima del cuadro de mensaje, junto al [indicador de modelo activo](#choosing-a-model). La barra muestra _usado_ / _total_ en miles de tokens y se colorea en verde, ámbar o rojo a medida que se llena el contexto. Un `±` delante de la cifra significa que todavía no hay un recuento exacto disponible.

Pasa el cursor por encima para ver un desglose en tres secciones etiquetadas:

| Sección                                              | Qué incluye                                                                                                                                                            |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Último intercambio**                               | Lo que costó el intercambio más reciente: entrada nueva, tokens servidos desde la caché de prompts del proveedor, tokens escritos en la caché y salida |
| **Esta conversación (facturada)** | Las mismas cuatro cifras acumuladas en todas las solicitudes de la conversación, incluidas las interacciones de ida y vuelta con las herramientas                      |
| **Contexto**                                         | Tokens que hay actualmente en la ventana de contexto, frente al tamaño real de la ventana                                                                              |

Una línea dice, por ejemplo, `37,588 input + 131,744 cached · write 37,558 · output 2,866`. Las partes relacionadas con la caché se omiten en los proveedores que no admiten la caché de prompts, y una sección se omite por completo cuando no tiene nada que Report.

> [!TIP]
> Separar el último intercambio del total de la conversación es lo que te indica si una breve pregunta de seguimiento salió realmente cara. Que aparezca una cifra alta en **Esta conversación (facturada)** junto a una cifra baja en **Último intercambio** es normal en una conversación larga.

### Ventana de contexto

La barra de uso del contexto, el punto de compactación automática y la longitud máxima de una sola respuesta dependen de la _ventana de contexto real del modelo en uso_, no de una cifra fija. Un modelo con una ventana de un millón de tokens se mide con respecto a un millón de tokens.

Cuando no se conoce la ventana real del modelo (por ejemplo, con un nombre de implementación de Azure OpenAI o Custom, o en un equipo en el que nunca se ha recuperado el catálogo de modelos), Tabular Editor recurre a 200.000 tokens.

### Reducir el uso de tokens

Selecciona objetos específicos en el **Explorador TOM** antes de hacer tu pregunta. Cuando hay objetos seleccionados, el asistente limita su contexto a esos objetos en lugar de obtener los metadatos de todo el modelo. Esta es la forma más eficaz de reducir tanto el uso de tokens como el coste de la API.

Otras formas de reducir el uso de tokens:

- Haz preguntas concretas sobre tablas, medidas o columnas específicas en lugar de preguntas generales sobre todo el modelo. Una instrucción imprecisa como _"Establece carpetas de visualización en todas las medidas"_ obliga al asistente a recuperar metadatos de todo el modelo. Una instrucción específica como _"Establece carpetas de visualización en las medidas que he seleccionado"_ limita el contexto a la selección actual y usa muchos menos tokens
- Inicia nuevas conversaciones al cambiar de tema para evitar acumular historiales de conversación extensos
- Usa un modelo más pequeño o menos costoso para preguntas exploratorias

## Limitaciones

- Requiere una clave de API proporcionada por el usuario. No se incluye ninguna clave de API integrada
- Las respuestas de la IA dependen del modelo seleccionado y de las capacidades del proveedor
- La ventana de contexto utilizable es la del modelo seleccionado; cuando Tabular Editor no puede determinarla, se asume un valor de 200.000 tokens
- El Asistente de IA no sustituye la comprensión de los fundamentos de DAX y del diseño de modelos semánticos
- La calidad de las respuestas varía según el proveedor y el modelo seleccionado
- El Asistente de IA no puede conectarse a archivos o servicios externos ni buscar en la web
- El Asistente de IA no puede conectarse a servidores MCP externos para ampliar sus propias herramientas. Esto solo se refiere al chat: Tabular Editor 3 sí actúa como servidor MCP, así que tu propio agente puede trabajar con el modelo abierto. Consulta @mcp-server
- El Asistente de IA no puede conectarse a otro modelo desde el chat. Usa la interfaz de usuario de Tabular Editor para cambiar las conexiones del modelo
- El Asistente de IA no puede administrar las preferencias

## Desactivar el Asistente de IA

El Asistente de IA es un componente opcional, instalado de forma predeterminada a partir de Tabular Editor 3.27.0. Puedes modificar una instalación existente de Tabular Editor 3 para incluir o excluir el componente del Asistente de IA volviendo a ejecutar el instalador de Tabular Editor 3. Si usas la versión portable de Tabular Editor 3, puedes quitar el componente del Asistente de IA eliminando el archivo `TabularEditor3.AI.dll` del directorio de instalación.

El Asistente de IA y el servidor MCP vienen en el mismo componente, por lo que, si lo excluyes o eliminas `TabularEditor3.AI.dll`, se eliminan ambos. Para desactivar el chat y mantener el servidor MCP, deje el componente instalado y use la directiva `DisableAiChat`.

> [!NOTE]
> Independientemente de que el componente del Asistente de IA esté instalado o no, un administrador del sistema puede desactivar toda la funcionalidad de IA en Tabular Editor 3, incluido el servidor MCP, especificando la [directiva `DisableAi`](xref:policies). `DisableAiChat` desactiva solo el chat, y `DisableMcpServer` desactiva solo el servidor MCP. Consulta @policies.
