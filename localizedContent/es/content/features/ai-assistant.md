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

## Primeros pasos

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

Selecciona **OpenAI** como proveedor e introduce tu clave de API. Opcionalmente, puedes especificar un ID de organización y un ID de proyecto si tu cuenta de OpenAI los usa. El modelo predeterminado es **gpt-5.5**, pero puedes cambiarlo por cualquier modelo disponible en tu cuenta.

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

Es posible que las implementaciones creadas antes de que tu organización adoptara Azure AI Foundry no aparezcan en el portal. Enuméralas con la CLI de Azure:

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
4. Introduce tu **clave de API** de Foundry
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

| Campo           | Obligatorio | Predeterminado                | Descripción                                                                                                           |
| --------------- | ----------- | ----------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `id`            | No          | Nombre de archivo sin `.md`   | Identificador único; también se usa como `/id` para la invocación explícita                                           |
| `name`          | No          | `id` con mayúsculas iniciales | Nombre para mostrar en el autocompletado                                                                              |
| `description`   | No          | Falls back to `name`          | Say what the instruction covers and when it applies                                                                   |
| `priority`      | No          | 100                           | Higher values are injected first when several Custom Instructions are in effect                                       |
| `always_inject` | No          | false                         | If true, always included in the system prompt. Such an instruction is not offered in `/` autocomplete |
| `hidden`        | No          | false                         | Si es `true`, no se muestra en el autocompletado de `/command`                                                        |

Las instrucciones personalizadas con un `id` que coincida con el de una instrucción integrada sustituirán la versión integrada.

Notes on how files are read:

- Frontmatter must start with `---` on the very first line of the file and end with a `---` line. If it does not, or if the YAML cannot be parsed, the whole file is treated as instruction content and every default above applies
- Keys that are not in the table above are ignored. This is what makes a leftover `triggers:` section harmless
- `{{version}}` anywhere in the body is replaced with the Tabular Editor AI component's version
- Only `.md` files directly in the folder are read; subfolders are not searched

### Custom Instructions from your organization

An administrator can publish a folder of Custom Instructions for everyone, with the `AiCustomInstructionsPath` [policy](xref:policies). It can be a read-only network share. Those instructions load for every user in addition to the built-in ones, and they are used exactly like any other: offered in `/` autocomplete, chosen by their description, invoked by `/id`.

Where the same `id` exists in more than one place, the one that wins is:

1. Your organization's folder
2. Your own folder
3. The built-in instructions

So an organization instruction overrides both a built-in one and a user's own file of the same name. A separate policy, `DisableUserCustomInstructions`, makes Tabular Editor ignore the instructions in your own folder altogether and disables **Open Custom Instructions Folder**; the built-in and organization instructions keep loading.

Both policies require Tabular Editor 3 Enterprise Edition.

## Permissions and consent

What the AI Assistant may touch is governed by _five resources_, each carrying one access level. The same five grants govern the [MCP server](xref:mcp-server), so there is one place to look and one place to change your mind.

| Resource                   | What it covers                                                                                                                                           | Niveles             | Predeterminado |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | -------------- |
| **Model metadata**         | Table, column and measure names, expressions, descriptions and similar. Read also covers VertiPaq Analyzer statistics                    | Deny / Read / Write | **Read**       |
| **Model data**             | Data values from your model, such as DAX query results. Requires a live connection                                                       | Deny / Read         | **Deny**       |
| **Best Practice Analyzer** | Read lists rules and runs the analysis; Write adds or modifies rules                                                                                     | Deny / Read / Write | **Read**       |
| **Documents**              | Your open document editors: C# scripts and DAX queries. Read is their contents; Write is needed to create or modify them | Deny / Read / Write | **Write**      |
| **Macros**                 | Your macro library. Read lists and reads macros; Write is reserved for future macro-editing tools                                        | Deny / Read / Write | **Write**      |

A **Write** grant covers Read, so there is no need to grant both. **Model data** is read-only by nature (the assistant can query your data but has no way to write values back), so it offers only Deny and Read.

> [!NOTE]
> **Model data** is the one resource denied by default. Metadata describes your model; data _is_ your model's contents, so sending it to an AI provider is a decision worth making deliberately rather than inheriting from a default.

Three grants are worth a closer look:

- **Model metadata > Write** lets the assistant change your model. On its own, that means writing a C# script and handing it to you to run. It is also the grant that makes [direct execution](#letting-the-assistant-change-your-model) possible, but the assistant only runs scripts itself once you have turned that on separately. Either way, only scripts that are statically determined to be safe ever run, and a script that reaches outside the model, to the file system or the network, is never executed for you.
- **Best Practice Analyzer > Read** lets the assistant run the analysis, but running it also needs **Model metadata > Read**, since the analysis reads the model.
- **Model data > Read** is not sufficient on its own to run a DAX query: that needs **Model metadata > Read** as well, because a query can read metadata through `INFO` functions, DMVs and the column names in its own result.

### Setting the permission grants

Open **Tools > Preferences > AI Features > Permissions**. Each resource has a dropdown carrying its available levels.

![AI Features > Permissions preferences, one dropdown per resource at its default](~/content/assets/images/pref-ai-permissions.png)

There is no separate "ask me" level. **Deny** is what asking looks like: in the chat, a resource you have not granted produces a permission card at the moment it is needed. Over MCP, where there is nobody to ask, a denied resource's tools are unavailable.

> [!NOTE]
> If you used the AI Assistant before 3.27.0 you will notice fewer prompts. Model metadata, Documents and Macros now start at Read or above, so the chat no longer asks for them. Only DAX query results and Best Practice Analyzer rule edits still raise a card out of the box. Set a resource to **Deny** to get its prompt back.

> [!NOTE]
> In the Enterprise Edition, IT administrators can set policies that determine these permissions. See @policies.

### Permission cards in the chat

When the assistant needs a resource your standing grant does not cover, a **Permission Required** card appears in the conversation, naming what it wants to do, for instance "The AI would like to access the metadata of your semantic model", or the DAX query it proposes to run.

![A Permission Required card in the chat, naming the DAX query the assistant wants to run, with Allow, Allow for session, Allow for this model, Always allow and Deny buttons](~/content/assets/images/ai-assistant/ai-assistant-generate-consent-dialog.png)

| Button                   | Qué hace                                                                                                                                                                                                                  |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Allow**                | This turn only. The assistant may repeat the same request while it finishes what you asked, and nothing is remembered afterwards                                                                          |
| **Allow for session**    | Until Tabular Editor is restarted. Held in memory, never written to disk                                                                                                                                  |
| **Allow for this model** | Recorded in the model's [user options](xref:user-options) file, so it applies the next time you open this model. Offered for **Model metadata** and **Model data** only, and only while a model is loaded |
| **Always allow**         | Raises the standing grant on the Permissions page, for every model and every session                                                                                                                                      |
| **Deny**                 | Refuses this request. The assistant carries on without that access and asks again next time                                                                                                               |

**Always allow** only ever raises a grant, never lowers one: allowing a read cannot narrow a Write grant you already had.

You do not have to answer the card at all. See [Stopping a turn while permission is pending](#stopping-a-turn-while-permission-is-pending) below.

### What the MCP server shares, and what it does not

The [MCP server](xref:mcp-server) reads the _same five grants_, but it does not use the card flow. An agent connecting over MCP is unattended, so there is nobody to prompt:

- Grants are _snapshotted when the server starts_ and govern its tool surface for the server's lifetime. Changing a grant while the server is running has no effect until you restart it.
- Only the _global_ grants are read. A grant you gave with **Allow for this model**, and a session grant, apply to the chat alone and never reach an MCP agent.
- A denied resource's tools are not offered to the agent at all, rather than being offered and then refused.

### Withdrawing permission

Set the resource back to **Deny** on the Permissions page. The chat asks again the next time it needs that resource; a running MCP server keeps the access it started with until you restart it.

Lowering a global grant does not clear a per-model grant. To withdraw one of those, delete the model's `.tmuo` file, or the `Permissions` entry within it. See details in @user-options.

### Audit record

On Tabular Editor 3 Enterprise Edition, a local record is kept of what the AI Assistant and the [MCP server](xref:mcp-server) did: which permissions were asked for and how you answered, which tools ran and whether each one succeeded, failed or was refused, and the full text of any C# script that was run or handed to you for review. Your prompts, the assistant's replies and data values from your model are never recorded. **Open audit folder** under **Tools > Preferences > AI Features** takes you to the files.

On Desktop and Business Edition, and before a license is activated, nothing is recorded, no folder is created and the button is not shown.

See @ai-audit-log for what each record holds, where the files live and the policies that redirect them.

### Stopping a turn while permission is pending

A **Permission Required** card waits for an answer before the assistant can carry on. You do not have to answer it: pressing **Stop** ends the turn, removes the card and treats the request as denied. The panel returns to its normal state and you can carry on in the same conversation with a new message.

## Preferencias

Configure AI Assistant display and behavior options under **Tools > Preferences > AI Features > AI Assistant > Preferences**.

### Visualización del chat

| Preferencia                                               | Predeterminado | Descripción                                                                                    |
| --------------------------------------------------------- | -------------- | ---------------------------------------------------------------------------------------------- |
| Mostrar indicador de contexto de selección                | true           | Muestra el objeto del modelo seleccionado actualmente en el chat                               |
| Mostrar indicador de instrucciones personalizadas         | true           | Muestra los indicadores de instrucciones personalizadas encima de las respuestas del asistente |
| Mostrar indicador de búsqueda en la base de conocimientos | true           | Muestra el progreso al buscar en la base de conocimientos                                      |

### Compactación de contexto

| Preferencia                         | Predeterminado | Descripción                                                                                                                                         |
| ----------------------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Compactación automática             | true           | Resumir automáticamente los mensajes antiguos al acercarse al límite del contexto                                                                   |
| Umbral de compactación automática % | 80             | Percentage of the model's own context window at which auto-compaction is triggered. Values outside 50-100 have no additional effect |

### C# Script

| Preferencia                                   | Predeterminado | Descripción                                                                                                                                                                                                                                                                                                                                                                             |
| --------------------------------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Allow AI assistant to run C# scripts directly | false          | Let the assistant carry out model changes itself instead of opening a script for you to run. Unavailable until **Model metadata** is set to **Write** under **Permissions**, and unavailable entirely under the `DisableCSharpScripts` [policy](xref:policies). See [Letting the assistant change your model](#letting-the-assistant-change-your-model) |
| Previsualizar cambios                         | true           | Mostrar el cuadro de diálogo de vista previa de cambios al ejecutar C# Scripts generados por IA desde el chat                                                                                                                                                                                                                                                                           |

Two further settings sit on the **AI Features** page itself, above **AI Assistant**, because they apply to the MCP server as well: _Check for knowledge base updates on startup_, and the **Open audit folder** button. See @preferences.

![The AI Assistant preferences page, with the three chat display indicators, Auto compact and its threshold, and the two C# script settings: Allow AI assistant to run C# scripts directly, cleared, and Preview changes, ticked](~/content/assets/images/ai-assistant/ai-assistant-preferences.png)

## Uso de tokens

Cada mensaje al Asistente de IA consume tokens de entrada. El coste en tokens de un solo mensaje depende de qué contexto se incluya:

- **Prompt del sistema e instrucciones personalizadas**: Se envían con cada mensaje. Normalmente, entre 5.000 y 15.000 tokens, según las instrucciones personalizadas que estén activas.
- **Model metadata**: when the assistant needs to understand your model, it retrieves metadata through tool calls. To stay within provider rate limits on large models, the assistant uses a progressive-disclosure approach. That is, it first fetches a lightweight overview (table and measure names, relationships), then searches for relevant objects by name, description or DAX expression and only drills into full details for the specific tables or objects that the question requires. Los resultados de las herramientas que, de otro modo, serían muy grandes se truncan e incluyen indicaciones sobre cómo el asistente puede recuperar los datos restantes.

### Contador de tokens

The token counter sits in the status strip above the message box, next to the [active model indicator](#choosing-a-model). The bar reads _used_ / _total_ in thousands of tokens and is colored green, amber or red as the context fills up. A `±` in front of the figure means an exact count is not available yet.

Hover over it for a breakdown in three labeled sections:

| Section                                           | What it covers                                                                                                                                          |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Last turn**                                     | What the most recent exchange cost: fresh input, tokens served from the provider's prompt cache, tokens written to the cache and output |
| **This conversation (billed)** | The same four figures accumulated across every request in the conversation, tool round-trips included                                                   |
| **Context**                                       | Tokens currently in the context window, against the window's real size                                                                                  |

A line reads, for example, `37,588 input + 131,744 cached · write 37,558 · output 2,866`. The cache parts are left out for providers that do not support prompt caching, and a section is left out entirely when it has nothing to report.

> [!TIP]
> Separating the last turn from the conversation total is what tells you whether a short follow-up question was actually expensive. A large **This conversation (billed)** figure next to a small **Last turn** figure is normal in a long conversation.

### Context window

The context usage bar, the auto-compaction point and the maximum length of a single reply all follow the _real context window of the model in use_, not one fixed figure. A model with a one-million-token window is measured against a million tokens.

Where the model's real window is not known (an Azure OpenAI or Custom deployment name, or a machine where the model catalog has never been retrieved), Tabular Editor falls back to 200,000 tokens.

### Reducir el uso de tokens

Selecciona objetos específicos en el **Explorador TOM** antes de hacer tu pregunta. Cuando hay objetos seleccionados, el asistente limita su contexto a esos objetos en lugar de obtener los metadatos de todo el modelo. Esta es la forma más eficaz de reducir tanto el uso de tokens como el coste de la API.

Otras formas de reducir el uso de tokens:

- Haz preguntas concretas sobre tablas, medidas o columnas específicas en lugar de preguntas generales sobre todo el modelo. Una instrucción imprecisa como _"Establece carpetas de visualización en todas las medidas"_ obliga al asistente a recuperar metadatos de todo el modelo. Una instrucción específica como _"Establece carpetas de visualización en las medidas que he seleccionado"_ limita el contexto a la selección actual y usa muchos menos tokens
- Inicia nuevas conversaciones al cambiar de tema para evitar acumular historiales de conversación extensos
- Usa un modelo más pequeño o menos costoso para preguntas exploratorias

## Limitaciones

- Requiere una clave de API proporcionada por el usuario. No se incluye ninguna clave de API integrada
- Las respuestas de la IA dependen del modelo seleccionado y de las capacidades del proveedor
- The usable context window is the selected model's own; where Tabular Editor cannot determine it, 200,000 tokens is assumed
- El Asistente de IA no sustituye la comprensión de los fundamentos de DAX y del diseño de modelos semánticos
- La calidad de las respuestas varía según el proveedor y el modelo seleccionado
- El Asistente de IA no puede conectarse a archivos o servicios externos ni buscar en la web
- The AI Assistant cannot connect to external MCP servers to extend its own tools. This is about the chat only: Tabular Editor 3 itself acts as an MCP server, so your own agent can work on the open model. See @mcp-server
- El Asistente de IA no puede conectarse a otro modelo desde el chat. Usa la interfaz de usuario de Tabular Editor para cambiar las conexiones del modelo
- El Asistente de IA no puede administrar las preferencias

## Desactivar el Asistente de IA

The AI Assistant is an optional component, installed by default from Tabular Editor 3.27.0. Puedes modificar una instalación existente de Tabular Editor 3 para incluir o excluir el componente del Asistente de IA volviendo a ejecutar el instalador de Tabular Editor 3. Si usas la versión portable de Tabular Editor 3, puedes quitar el componente del Asistente de IA eliminando el archivo `TabularEditor3.AI.dll` del directorio de instalación.

The AI Assistant and the MCP server ship in the same component, so excluding it or deleting `TabularEditor3.AI.dll` removes both. To turn off the chat while keeping the MCP server, leave the component in place and use the `DisableAiChat` policy.

> [!NOTE]
> Regardless of whether the AI Assistant component is installed or not, a system admin can disable all AI functionality in Tabular Editor 3, the MCP server included, by specifying the [`DisableAi` policy](xref:policies). `DisableAiChat` turns off the chat alone, and `DisableMcpServer` the MCP server alone. See @policies.
