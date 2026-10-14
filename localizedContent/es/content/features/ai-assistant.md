---
uid: ai-assistant
title: Asistente de IA
author: Morten Lønskov
updated: 2026-10-09
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

El Asistente de IA es un panel de chat para el desarrollo de modelos semánticos. Explora los metadatos de tu modelo, escribe y ejecuta consultas DAX, genera C# Scripts, ejecuta comprobaciones del Best Practice Analyzer, consulta las estadísticas del Analizador VertiPaq y busca en la base de conocimientos de Tabular Editor. La [configuración de permisos](#permissions-and-consent) controla lo que envía a tu proveedor de IA. El Asistente de IA se ha sometido a pruebas de penetración independientes; consulta el [Centro de confianza de Tabular Editor](https://trust.tabulareditor.com).

El Asistente de IA usa un modelo Bring Your Own Key, en el que proporcionas una clave de API de uno de los proveedores compatibles y el asistente se ejecuta directamente contra la API de ese proveedor.

También puedes usar tu propio agente a través del [servidor MCP](xref:mcp-server), sin clave de API. Un agente como Claude Code, GitHub Copilot, el modo agente de VS Code, Codex o Cursor trabaja sobre el modelo abierto con las mismas herramientas y la misma configuración de permisos que el chat, salvo las autorizaciones de sesión y por modelo, que solo se aplican al chat. Consulta [las diferencias entre el servidor MCP y el Asistente de IA](#mcp-server-and-ai-assistant-differences).

![El panel del Asistente de IA al abrirse por primera vez, con el saludo del asistente que enumera lo que puede hacer (responder preguntas, consultar el modelo, escribir y ejecutar C# Scripts, cambiar el modelo) y lo que no puede hacer, encima de un cuadro de mensajes vacío](~/content/assets/images/ai-assistant/ai-assistant-panel-first-open.png)

## Primeros pasos

1. Abre **Herramientas > Preferencias > Funciones de IA > Asistente de IA > Proveedor de IA**
2. Selecciona tu proveedor de IA (en una instalación limpia, el valor predeterminado es **Ninguno (IA deshabilitada)**) y luego introduce tu clave de API
3. Abre el panel del Asistente de IA desde **Vista > Asistente de IA**
4. Escribe mensajes y pulsa **Enter** para iniciar una conversación

> [!TIP]
> La [demo interactiva del Asistente de IA](https://demos.tabulareditor.com/psl/of150vcy?) te guía por la configuración y el uso.

> [!NOTE]
> Las claves de API se almacenan cifradas en tu equipo local.

## Proveedores compatibles

Configura tu proveedor de IA en **Herramientas > Preferencias > Funciones de IA > Asistente de IA > Proveedor de IA**. Selecciona un proveedor en la lista desplegable (el valor predeterminado es **Ninguno (IA deshabilitada)** hasta que configures uno), introduce tu clave de API y, si lo deseas, reemplaza el modelo predeterminado.

Deja en blanco el campo del modelo para usar el modelo predeterminado del proveedor. OpenAI y Anthropic tienen valores predeterminados; Azure OpenAI y el proveedor personalizado siempre requieren un valor.

| Proveedor                                                | Modelo predeterminado                                            | Configuración necesaria                                                                |
| -------------------------------------------------------- | ---------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| OpenAI                                                   | gpt-5.5                                          | Clave de API. URL base, ID de organización e ID de proyecto opcionales |
| Anthropic                                                | claude-sonnet-4-6                                                | Clave de API. URL base opcional                                        |
| Azure OpenAI                                             | Ninguno. Se requiere un nombre de implementación | Clave de API, URL del punto de conexión y nombre de la implementación                  |
| Personalizado (compatible con OpenAI) | Ninguno. Se requiere un nombre de modelo         | Clave de API y URL personalizada del punto de conexión                                 |

![La página de preferencias del Proveedor de IA con la lista desplegable Elegir proveedor abierta en Ninguno (IA deshabilitada), OpenAI, Anthropic, Azure OpenAI y Personalizado (compatible con OpenAI), y debajo un campo de URL y otro de clave de API](~/content/assets/images/ai-assistant/ai-assistant-provider-preferences.png)

### Elegir un modelo

El modelo activo se muestra en la barra de estado situada encima del cuadro de mensajes, junto a la barra de uso del contexto. Haz clic para abrir un selector con los modelos disponibles para el proveedor configurado; el modelo que elijas se aplicará a partir de la siguiente solicitud. La última entrada, **Preferencias...**, abre **Herramientas > Preferencias > Funciones de IA > Asistente de IA > Proveedor de IA** para cualquier opción que no aparezca en la lista. Para los proveedores Azure OpenAI y Personalizado, o antes de que se haya recuperado la lista de modelos, el nombre del modelo es un enlace que abre esas preferencias.

![El selector de modelos abierto encima del cuadro de mensajes, con claude-sonnet-5, claude-fable-5-1, claude-fable-5, claude-opus-5, claude-haiku-4-5, claude-opus-4-8 y el claude-sonnet-4-6 activo en negrita, con Preferencias... debajo de un separador](~/content/assets/images/ai-assistant/ui-model-picker.png)

> [!NOTE]
> El indicador de modelo permanece oculto hasta que se hayan configurado un proveedor, una clave de API y un modelo.

### OpenAI

Selecciona **OpenAI** como proveedor e introduce tu clave de API. Si tu cuenta de OpenAI usa un Organization ID o un Project ID, también debes introducirlos. El nombre del modelo admite cualquier modelo disponible en tu cuenta.

![La página de preferencias del Proveedor de IA de una versión anterior, con OpenAI seleccionado, una clave de API oculta, los campos Organization ID y Project ID vacíos y gpt-4o como nombre del modelo](~/content/assets/images/ai-assistant/ai-assistant-openai-config.png)

### Anthropic

Selecciona **Anthropic** como proveedor e introduce tu clave de API. El nombre del modelo admite cualquier modelo de Anthropic disponible en tu cuenta.

![La página de preferencias del Proveedor de IA con Anthropic seleccionado como proveedor, la URL base https://api.anthropic.com, una clave de API oculta y claude-sonnet-4-6 como nombre del modelo](~/content/assets/images/ai-assistant/ai-assistant-anthropic-config.png)

> [!IMPORTANT]
> Anthropic aplica límites de velocidad de tokens de entrada por minuto (ITPM) en función del nivel de tu cuenta. Una nueva clave de API empieza en el Nivel 1 con 30.000 ITPM para Claude Sonnet 4.x. Una sola solicitud a un modelo grande puede superar este límite. Compra 40 USD o más en créditos de API para alcanzar el Nivel 2 (450.000 ITPM). Consulta la [documentación de límites de velocidad de Anthropic](https://docs.anthropic.com/en/api/rate-limits) para ver todos los detalles de los niveles.

### Azure OpenAI

Selecciona **Azure OpenAI** como proveedor y configura estos campos:

- **Clave de API**: la clave de acceso de tu recurso de Azure OpenAI
- **Service endpoint**: la URL del recurso, por ejemplo `https://your-resource.openai.azure.com`. El certificado SSL se emite para `*.openai.azure.com`, por lo que una dirección `*.privatelink.openai.azure.com` no supera la validación del certificado
- **Deployment**: el nombre de la implementación que se muestra en la columna **Name** de **Deployments**

Azure OpenAI requiere el nombre de la implementación en cada llamada a la API. El nombre se establece al crear la implementación y a menudo coincide con el modelo que sirve, por ejemplo `gpt-4o`, pero puede ser distinto. Si introduces el nombre del recurso o un nombre de modelo que no exista como implementación, la solicitud fallará.

Busca el nombre de la implementación en el [portal de Azure AI Foundry](https://ai.azure.com):

1. Inicia sesión y selecciona tu recurso de Azure OpenAI
2. Abre **Implementaciones** (o **Modelos + puntos de conexión** si el recurso se ha actualizado a Foundry)
3. Copia el valor de la columna **Nombre**

Si una implementación creada antes de que tu organización adoptara Azure AI Foundry no aparece en el portal, usa Azure CLI para enumerar las implementaciones:

```bash
az cognitiveservices account deployment list --name "<resource-name>" --resource-group "<resource-group>" --output table
```

Consulta [Crear y desplegar un recurso de Azure OpenAI](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/create-resource#deploy-a-model).

Para errores 403, fallos de SSL o respuestas "DeploymentNotFound", consulta @azure-openai-connection-errors. Para los modelos implementados en Microsoft Foundry, consulta [Uso de Microsoft Foundry](#using-microsoft-foundry).

### Personalizado (compatible con OpenAI)

El proveedor personalizado se conecta a cualquier LLM que exponga un punto de conexión de API compatible con OpenAI, como un modelo en tu propia máquina o alojado en la red de tu organización. Introduce tu clave de API y la URL del punto de conexión. Con un modelo autoalojado, todos los datos permanecen dentro de tu propia infraestructura y no se envía nada a un proveedor de nube de terceros. Consulta [Uso de un LLM local o de la organización](#using-a-local-or-organizational-llm).

## Uso de un LLM local o de tu organización

Puedes ejecutar el Asistente de IA con un LLM autoalojado mediante el proveedor Personalizado. Esto mantiene todos los datos dentro de tu propia infraestructura, ya sea un modelo que se ejecuta en tu equipo local o un LLM alojado de forma centralizada dentro de la red de tu organización. En cualquier caso, no se envía ningún dato a un proveedor de nube de terceros.
Estas herramientas alojan modelos con una API compatible con OpenAI, en la estación de trabajo de un desarrollador o en un servidor compartido que actúa como punto de conexión del equipo:

- [Ollama](https://ollama.com): CLI ligera para descargar y ejecutar modelos localmente
- [LM Studio](https://lmstudio.ai): aplicación de escritorio con interfaz gráfica para administrar y ejecutar modelos locales
- [LocalAI](https://localai.io): alternativa autoalojada e impulsada por la comunidad, con amplio soporte para modelos

### Ejemplo: Ollama

1. [Descarga e instala Ollama](https://ollama.com/download)
2. Descarga un modelo, por ejemplo `ollama pull llama3.1`
3. Inicia el servidor de Ollama. Se inicia automáticamente después de la instalación y, de forma predeterminada, usa el puerto 11434
4. En Tabular Editor, ve a **Herramientas > Preferencias > Funciones de IA > Asistente de IA > Proveedor de IA**
5. Configura **Elegir proveedor** como **Personalizado (compatible con OpenAI)**
6. Establece **Punto de conexión del servicio** en `http://localhost:11434/v1`
7. Establece **Model name** en el modelo que descargaste, por ejemplo `llama3.1`
8. Configura **API Key** con cualquier valor no vacío, por ejemplo `ollama`. Ollama no requiere autenticación, pero el campo no puede quedar en blanco

### Ejemplo: LM Studio

1. [Descarga e instala LM Studio](https://lmstudio.ai/download)
2. Descarga un modelo desde la página de búsqueda de modelos del panel izquierdo o con la CLI, por ejemplo `lms get lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF`
3. Inicia el servidor de LM Studio desde la página para desarrolladores del panel izquierdo o con `lms server start`. Activa el modo compatible con OpenAI. Si el tamaño del contexto es inferior a 100.000 tokens, súbelo por encima de 100.000
4. En Tabular Editor, ve a **Herramientas > Preferencias > Funciones de IA > Asistente de IA > Proveedor de IA**
5. Configura **Elegir proveedor** como **Personalizado (compatible con OpenAI)**
6. Establece **Punto de conexión del servicio** en `http://localhost:1234/v1`
7. Establece **Nombre del modelo** en el modelo que descargaste, por ejemplo `lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF`
8. En **Clave de API**, introduce cualquier valor no vacío, por ejemplo `lms`. LM Studio no requiere autenticación, pero el campo no puede quedar en blanco

> [!NOTE]
> La calidad de las respuestas con modelos locales depende del tamaño del modelo y de tu hardware. Los modelos más grandes suelen ofrecer mejores resultados, pero requieren más RAM y una GPU potente. La invocación de herramientas del Asistente de IA requiere un modelo que admita la llamada a funciones en el formato compatible con OpenAI.

> [!TIP]
> Usa un modelo con al menos 30 mil millones de parámetros y, preferiblemente, 100 mil millones o más. Qwen3.5-122B-A10B funcionó bien en pruebas internas.

## Uso de Microsoft Foundry

[Microsoft Foundry](https://ai.azure.com) (antes llamado Azure AI Foundry) te permite desplegar modelos de OpenAI y Anthropic en tu entorno de Azure. Conéctate a estos modelos con el proveedor **OpenAI** o **Anthropic** en Tabular Editor.

> [!IMPORTANT]
> No uses el proveedor **Azure OpenAI** para modelos de Microsoft Foundry. Solo funciona con recursos clásicos de Azure OpenAI que usan el parámetro de consulta `api-version`.

### Modelos de OpenAI en Microsoft Foundry

Configura un modelo de OpenAI desplegado en Microsoft Foundry, como GPT-4o o GPT-5.4-mini:

1. En Tabular Editor, ve a **Herramientas > Preferencias > Funciones de IA > Asistente de IA > Proveedor de IA**
2. Selecciona **OpenAI** en **Elegir proveedor**
3. En **URL base**, introduce el punto de conexión de tu recurso de Foundry y añade `/openai/v1` al final, en uno de estos formatos:
   - `https://your-resource.services.ai.azure.com/openai/v1`
   - `https://your-resource.openai.azure.com/openai/v1`
4. Introduce tu **Clave de API** de Foundry
5. En **Nombre del modelo**, introduce el nombre de tu implementación, por ejemplo `gpt-5.4-mini`

> [!NOTE]
> El portal de Microsoft Foundry no muestra la URL base. En su lugar, muestra un **URI de destino** con la ruta completa de la API, por ejemplo `https://your-resource.services.ai.azure.com/api/projects/YourProject/openai/v1/responses`. Para la URL base, usa solo `https://your-resource.services.ai.azure.com/openai/v1`.

### Modelos de Anthropic en Microsoft Foundry

Para un modelo de Anthropic desplegado en Microsoft Foundry, como Claude Sonnet 4.6:

1. En Tabular Editor, ve a **Herramientas > Preferencias > Funciones de IA > Asistente de IA > Proveedor de IA**
2. Configura **Elegir proveedor** como **Anthropic**
3. En **URL base**, introduce el punto de conexión de tu recurso de Foundry y añade `/anthropic` al final, por ejemplo `https://your-resource.services.ai.azure.com/anthropic`
4. Introduce tu **Clave de API** de Foundry
5. En **Nombre del modelo**, introduce el identificador del modelo, por ejemplo `claude-sonnet-4-6`

> [!NOTE]
> El portal muestra un **URI de destino** como `https://your-resource.services.ai.azure.com/anthropic/v1/messages`. Para la URL base, usa solo la parte hasta `/anthropic` inclusive.

## Capacidades

En el marco de tus [concesiones de permisos](#permissions-and-consent), el Asistente de IA trabaja con el contexto de tu modelo:

- **Exploración del modelo**: consulta los metadatos del modelo, incluidas tablas, columnas, medidas, relaciones y sus propiedades
- **Redacción de consultas DAX**: genera consultas DAX, las ejecuta en tu modelo en modo conectado y devuelve los conjuntos de resultados en el chat
- **Generación de C# Scripts**: crea C# Scripts para realizar cambios en el modelo. Según tu configuración, el asistente abre el script en una ventana del editor para que lo revises y lo ejecutes, o lo ejecuta automáticamente; consulta [Permitir que el asistente cambie el modelo](#letting-the-assistant-change-your-model). **Ctrl+Z** deshace los cambios en los metadatos del modelo
- **Best Practice Analyzer**: ejecuta el análisis de BPA, lista las infracciones de las reglas y crea o modifica reglas de BPA
- **Analizador VertiPaq**: consulta estadísticas de uso de memoria y cardinalidad de columnas
- **Acceso a documentos**: lee y modifica documentos abiertos: consultas DAX, C# Scripts y scripts DAX
- **Búsqueda en la base de conocimientos**: busca en la documentación integrada de Tabular Editor
- **Navegación por la interfaz de usuario**: genera enlaces de acción `te3://` que abren cuadros de diálogo y funcionalidades específicas de Tabular Editor

Un agente conectado a través del [servidor MCP](xref:mcp-server) tiene las mismas capacidades, excepto la navegación por la interfaz de usuario. Ambos cambian tu modelo ejecutando un C# Script como un único paso que se puede deshacer. Se diferencian en cómo revisas los cambios y otorgas permisos; consulta [Diferencias entre el servidor MCP y AI Assistant](#mcp-server-and-ai-assistant-differences).

> [!NOTE]
> Cuando el modelo se carga desde un archivo, como un archivo `.bim` o una carpeta TMDL, y no está conectado a Analysis Services o Power BI, se ocultan las herramientas que requieren conexión, como la ejecución de consultas DAX y las estadísticas del Analizador VertiPaq. El asistente sigue escribiendo consultas DAX, pero el botón **Ejecutar** de los artefactos de consulta DAX está desactivado hasta que te conectes. Las estadísticas del Analizador VertiPaq cargadas desde un archivo `.vpax` siguen disponibles.

## Permitir que el asistente cambie tu modelo

De forma predeterminada, el asistente escribe un C# Script y lo abre en una ventana del editor, donde puedes leerlo y ejecutarlo. El asistente también puede ejecutar el script por sí mismo cuando seleccionas **Permitir que AI Assistant ejecute C# Scripts directamente** en **Herramientas > Preferencias > Funciones de IA > AI Assistant > Preferencias**.

La configuración está desactivada de forma predeterminada y no está disponible hasta que **Metadatos del modelo** esté establecido en **Lectura/escritura** en **Herramientas > Preferencias > Funciones de IA > Permisos**.

### Qué ocurre cuando el asistente ejecuta un script

- Si **Vista previa de cambios** está activada (de forma predeterminada), aparece el [cuadro de diálogo de vista previa](xref:csharp-scripts#run-c-scripts-with-preview) antes de que se apliquen los cambios. **Cancelar** revierte los cambios y envía un Report del rechazo al asistente. Si **Vista previa de cambios** está desactivada, los cambios se aplican sin mostrar ningún cuadro de diálogo.
- Los cambios del script quedan registrados como una única entrada de deshacer: **C# script (AI Assistant)**. **Ctrl+Z** deshace todo el script.
- Si el script falla a mitad de la ejecución, el modelo no se modifica y el asistente genera un Report del error.
- No se ejecuta ningún script que acceda a archivos, la red o ensamblados externos. Se abre como un artefacto de script con la insignia **Inseguro** y **Ejecutar** deshabilitado, y la respuesta del asistente indica qué utilizaba el script.

Si pides un script, por ejemplo: "Escríbeme un script que cambie el nombre de todas las medidas a estilo oración", el asistente lo abre como un documento de script que ejecutas tú mismo, incluso con esta configuración activada.

La [directiva](xref:policies) `DisableCSharpScripts` se aplica en todas las ediciones y desactiva tanto la ejecución directa como los scripts que el asistente te proporciona para que los ejecutes.

La directiva `BlockUnsafeScripts` requiere la Edición Enterprise y se aplica a todos los scripts de Tabular Editor, incluidos los scripts ejecutados a través del [servidor MCP](xref:mcp-server). Cuando está activada, el asistente aún puede escribir un script que acceda a archivos, a la red o a ensamblados externos, pero el script no se ejecuta y no se abre ningún artefacto para revisarlo. Consulta [Directivas de administrador](xref:csharp-scripts#administrator-policies).

## Conversaciones

El Asistente de IA admite varias conversaciones simultáneas, cada una con su propio historial de mensajes y contexto.

- las conversaciones se conservan entre sesiones y se almacenan localmente en `%LocalAppData%\TabularEditor3\AI\Conversations\`
- los títulos se generan automáticamente tras el primer intercambio, y puedes cambiar el nombre de una conversación
- **Compactación automática**: cuando una conversación se acerca al límite de la ventana de contexto, los mensajes más antiguos se resumen para liberar espacio, después de archivar una instantánea de la conversación completa. El umbral es un porcentaje de la propia ventana de contexto del modelo y se configura en [Compactación del contexto](#context-compaction)

### Eliminar una conversación

**Eliminar conversación** está en el extremo izquierdo de la barra de herramientas del Asistente de IA, junto a **Nueva conversación**. Después de confirmar la solicitud, la conversación y su historial se eliminan del disco y no se pueden recuperar. El botón de cierre de la barra de título del panel, o **Ver > Asistente de IA**, oculta el panel sin eliminar nada.

## Artefactos

El código que genera el Asistente de IA se abre como un _artefacto_ en una ventana del editor:

- **Scripts de C#**: un editor de C# Script con resaltado de sintaxis, compilación y ejecución
- **Consultas DAX**: un editor de consultas DAX con resaltado de sintaxis y ejecución

Los artefactos se van mostrando a medida que la IA los genera, y los artefactos de C# Script incluyen un análisis de seguridad que señala el código inseguro, como el acceso al sistema de archivos o las operaciones de red.

![El panel de AI Assistant muestra un artefacto de C# Script generado con un botón Execute y la explicación del asistente sobre lo que hace el script, además de la advertencia sobre la distinción entre mayúsculas y minúsculas](~/content/assets/images/ai-assistant/ai-assistant-generate-c-sharp-script.png)

Si **Vista previa de cambios** está activada, al ejecutar un C# Script desde el chat se abre el cuadro de diálogo **Vista previa del script** con una comparación en paralelo de todos los cambios en los metadatos del modelo que realizó el script, donde puedes aceptar o revertir los cambios. Consulta [Ejecutar scripts con vista previa](xref:csharp-scripts#run-c-scripts-with-preview).

![El cuadro de diálogo Vista previa del script: cambios en el modelo, con el modelo antes y después uno junto al otro, con la cadena de formato de la medida Internet Total Freight modificada y con una descripción y una carpeta de visualización añadidas, cada una marcada respecto de su valor original](~/content/assets/images/preview-script-changes.png)

## Instrucciones personalizadas

Las _instrucciones personalizadas_ son conjuntos de instrucciones que guían al Asistente de IA en tareas específicas. El asistente recibe una lista de todas las instrucciones disponibles con su `description`, y carga el texto completo solo de las que son relevantes para tu solicitud, así que procura que las descripciones sean precisas y específicas. Una instrucción cargada sigue en vigor durante el resto de la conversación.

### Instrucciones personalizadas integradas

El Asistente de IA incluye las siguientes instrucciones personalizadas:

| Instrucción personalizada                    | Invocar con           | Cubre                                                                                                                                                                                            |
| -------------------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Consulta DAX                                 | `/dax-querying`       | Escritura y ejecución de consultas DAX: referencias completas de columnas y medidas, comprobación de valores de filtro, validación y actualización de consultas                  |
| Modificación del modelo                      | `/model-modification` | C# Scripts para crear o cambiar objetos del modelo: patrones de la API de TOMWrapper, orden de ejecución, actualizaciones idempotentes, reglas de nomenclatura                   |
| Diseño del modelo semántico                  | `/model-design`       | Esquema en estrella, relaciones y filtrado cruzado, tablas de fechas, medidas frente a columnas calculadas, grupos de cálculo, nomenclatura                                                      |
| Organización del modelo semántico            | `/organize-model`     | Auditoría y limpieza de los metadatos del modelo: convenciones de nomenclatura, grupos de tablas, carpetas de visualización, columnas ocultas, cadenas de formato, descripciones |
| Optimización del tamaño del modelo semántico | `/optimize-model`     | Reducción de la memoria y del tamaño del modelo: medida de VertiPaq, eliminación de columnas, ajuste de tipos de datos, cambios estructurales, límites de SKU                    |
| Macros                                       | `/macros`             | Macros de C# reutilizables para la ventana de macros: contextos de selección, reglas de código genérico                                                                          |
| Funciones DAX definidas por el usuario       | `/udf`                | Creación de UDFs de DAX: sintaxis, modos de parámetro `VAL`/`EXPR`, sugerencias de tipo, espacios de nombres, DaxLib                                                             |
| Best Practice Analyzer                       | `/bpa`                | Revisión de infracciones y creación de reglas personalizadas mediante expresiones de LINQ Dynamic                                                                                                |

Con la preferencia **Mostrar indicador de instrucciones personalizadas** seleccionada en **Herramientas > Preferencias > Funciones de IA > Asistente de IA > Preferencias**, los indicadores situados encima de cada respuesta muestran qué instrucciones influyeron en ella.

### Invocar una instrucción personalizada

Escribe `/` para ver las instrucciones personalizadas disponibles. Empieza tus mensajes con el `/id` de una instrucción para cargarla independientemente del contenido de los mensajes; por ejemplo, `/dax-querying` carga la instrucción de consulta DAX. Un `/id` sin mensajes carga la instrucción sin enviar ninguna solicitud. Una instrucción cargada explícitamente sigue en vigor durante el resto de la conversación, igual que una que el asistente carga por sí solo.

### Añade tus propias instrucciones personalizadas

Crea una instrucción personalizada colocando un archivo `.md` en `%LocalAppData%\TabularEditor3\AI\CustomInstructions\`. La carpeta se crea la primera vez que se ejecuta el Asistente de IA, con un archivo `example.md` que puedes usar como base. La opción **Abrir carpeta de instrucciones personalizadas** en la barra de herramientas del Asistente de IA la abre.

El front matter en YAML que define los metadatos de la instrucción es opcional:

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
| `name`          | No          | `id` con mayúsculas iniciales      | Nombre para mostrar en el autocompletado                                                                                                    |
| `description`   | No          | Si no se especifica, se usa `name` | Indica qué cubre la instrucción y cuándo se aplica                                                                                          |
| `priority`      | No          | 100                                | Los valores más altos se inyectan primero cuando hay varias instrucciones personalizadas en vigor                                           |
| `always_inject` | No          | false                              | Si es `true`, siempre se incluye en el prompt del sistema. Este tipo de instrucción no aparece en el autocompletado de `/.` |
| `hidden`        | No          | false                              | Si es `true`, no se muestra en el autocompletado de `/command`                                                                              |

Una instrucción personalizada cuyo `id` coincide con el de una instrucción integrada sustituye la versión integrada.

Tabular Editor lee los archivos de la siguiente manera:

- el frontmatter debe comenzar con `---` en la primera línea del archivo y terminar con una línea que contenga `---`. Si no es así, o si no se puede analizar el YAML, todo el archivo se trata como contenido de la instrucción y se aplican todos los valores predeterminados anteriores
- las claves que no estén en la tabla anterior se ignoran. Los archivos de versiones anteriores que aún tengan una sección `triggers:` se cargan sin cambios
- Cualquier `{{version}}` en el cuerpo se reemplaza por la versión del componente de IA de Tabular Editor
- solo se leen los archivos `.md` ubicados directamente en la carpeta; no se buscan subcarpetas

### Instrucciones personalizadas de tu organización

Un administrador puede publicar una carpeta de instrucciones personalizadas para todos mediante la [directiva](xref:policies) `AiCustomInstructionsPath`, y la carpeta puede ser un recurso compartido de red de solo lectura. Estas instrucciones se cargan para todos los usuarios, además de las integradas, y funcionan como las demás: aparecen en el autocompletado de `/`, se eligen por su descripción y se invocan con `/id`.

Cuando el mismo `id` existe en más de un lugar, el orden de prioridad es:

1. la carpeta de tu organización
2. tu propia carpeta
3. las instrucciones integradas

Una directiva independiente, `DisableUserCustomInstructions`, hace que Tabular Editor ignore las instrucciones de tu propia carpeta y deshabilita **Abrir carpeta de instrucciones personalizadas**; las instrucciones integradas y de la organización siguen cargándose. Ambas directivas requieren Tabular Editor 3 Edición Enterprise.

## Permisos y consentimiento

Establece un nivel de acceso para cada recurso para controlar a qué puede acceder el Asistente de IA, y el [servidor MCP](xref:mcp-server) usa la misma configuración.

| Recurso                    | Qué abarca                                                                                                                                                                              | Niveles                       | Predeterminado |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- | -------------- |
| **Metadatos del modelo**   | Nombres de tablas, columnas y medidas, expresiones, descripciones y elementos similares. El permiso de lectura también incluye las estadísticas del Analizador VertiPaq | Denegar / Leer / Escribir     | **Leer**       |
| **Datos del modelo**       | Valores de datos de tu modelo, como los resultados de consultas DAX. Requiere una conexión activa                                                                       | Denegar / Leer                | **Denegar**    |
| **Best Practice Analyzer** | Leer enumera las reglas y ejecuta el análisis; Escribir agrega o modifica reglas                                                                                                        | Denegar / Lectura / Escritura | **Lectura**    |
| **Documentos**             | Tus documentos abiertos: consultas DAX, C# Scripts y scripts DAX. Lectura permite ver su contenido; Escritura es necesaria para crearlos o modificarlos | Denegar / Lectura / Escritura | **Escritura**  |
| **macros**                 | Tu biblioteca de macros. Lectura permite listar y leer macros; Escritura se reserva para futuras herramientas de edición de macros                                      | Denegar / Lectura / Escritura | **Escritura**  |

**Escritura** (que aparece como **Lectura/Escritura** en las listas desplegables) incluye **Lectura**.

> [!NOTE]
> Otorgar acceso a **Datos del modelo** envía valores de datos de tu modelo a tu proveedor de IA.

Algunos permisos dependen de otros:

- Se requiere **Metadatos del modelo > Escritura** para la [ejecución directa](#letting-the-assistant-change-your-model), que se activa por separado.
- Ejecutar el Best Practice Analyzer requiere **Metadatos del modelo > Lectura**, además de **Best Practice Analyzer > Lectura**.
- Ejecutar una consulta DAX requiere **Metadatos del modelo > Lectura**, además de **Datos del modelo > Lectura**. Una consulta puede leer metadatos mediante las funciones `INFO`, las DMV y los nombres de columna del resultado.

### Configurar los permisos

Abre **Herramientas > Preferencias > Funciones de IA > Permisos**, donde cada recurso tiene una lista desplegable con sus niveles disponibles.

![Funciones de IA > Preferencias de permisos, un menú desplegable por recurso con su configuración predeterminada](~/content/assets/images/pref-ai-permissions.png)

El chat no tiene un nivel independiente de "solicitar" y muestra una [tarjeta de permiso](#permission-cards-in-the-chat) cuando necesita un recurso configurado en **Denegar**.

> [!NOTE]
> A partir de la versión 3.27.0, **Metadatos del modelo**, **Documentos** y **macros** tienen como valor predeterminado Lectura o un nivel superior, y el chat ya no los solicita. De forma predeterminada, solo los resultados de consultas DAX y las ediciones de reglas de Best Practice Analyzer muestran una tarjeta. Establece un recurso en **Denegar** para que vuelva a mostrarse su solicitud.

> [!NOTE]
> En la Edición Enterprise, los administradores pueden limitar estos permisos mediante una directiva. Consulta @policies.

### Tarjetas de permiso en el chat

Cuando el asistente necesita un recurso que tu autorización permanente no cubre, aparece una tarjeta de **Permiso necesario** en la conversación. La tarjeta indica lo que el asistente quiere hacer, por ejemplo "La IA quiere acceder a los metadatos de tu modelo semántico", o muestra la consulta DAX que propone ejecutar.

![Una tarjeta de Permiso requerido en el chat, que muestra la consulta DAX que el asistente quiere ejecutar, con los botones Permitir, Permitir para esta sesión, Permitir para este modelo, Permitir siempre y Denegar](~/content/assets/images/ai-assistant/ai-assistant-generate-consent-dialog.png)

| Botón                         | Qué hace                                                                                                                                                                                                                                                       |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Permitir**                  | Se aplica solo a esta interacción. El asistente puede repetir la misma solicitud mientras termina tu tarea, y después no se recuerda nada                                                                                                      |
| **Permitir para esta sesión** | Se aplica hasta que se reinicie Tabular Editor. El permiso se mantiene en memoria y nunca se guarda en disco                                                                                                                                   |
| **Permitir para este modelo** | Se registra en el archivo de [opciones de usuario](xref:user-options) del modelo y se aplica la próxima vez que abras este modelo. Solo se ofrece para **Metadatos del modelo** y **Datos del modelo**, y solo mientras haya un modelo cargado |
| **Permitir siempre**          | Aumenta el permiso permanente en la página Permisos, para todos los modelos y todas las sesiones                                                                                                                                                               |
| **Denegar**                   | Deniega esta solicitud. El asistente continúa sin ese acceso, y la tarjeta vuelve a aparecer la próxima vez que lo necesite                                                                                                                    |

**Permitir siempre** nunca reduce un permiso existente; conceder Lectura a un recurso que ya está en Escritura lo mantiene en Escritura.

### Detener un turno mientras el permiso está pendiente

La interacción se pausa hasta que respondas a una tarjeta de **Permiso necesario**. **Detener** finaliza la interacción sin respuesta, quita la tarjeta y cuenta la solicitud como denegada. Envía un mensaje nuevo para continuar la conversación.

### Diferencias entre el servidor MCP y el Asistente de IA

El [servidor MCP](xref:mcp-server) usa los mismos cinco permisos, pero no muestra tarjetas de permiso:

- los permisos se leen cuando se inicia el servidor y se aplican hasta que se detiene, por lo que los cambios en un permiso solo surten efecto después de reiniciar el servidor
- solo se aplican las subvenciones globales. Las subvenciones otorgadas con **Permitir para este modelo** o **Permitir para la sesión** se aplican solo al chat
- las herramientas de un recurso denegado no aparecen en la lista de herramientas del agente

### Retirar permisos

Vuelve a establecer un recurso en **Denegar** en la página de Permisos para retirar su concesión. El chat mostrará entonces una tarjeta de permiso la próxima vez que necesite ese recurso.

Reducir una concesión global no elimina una concesión por modelo. Elimina el archivo `.tmuo` del modelo, o la entrada `Permissions` que hay en él, para retirar las concesiones por modelo. Consulta @user-options.

### Registro de auditoría

En la Edición Enterprise, incluidas las licencias de Consultancy y Trial, Tabular Editor escribe un registro local de la actividad de AI Assistant y del [servidor MCP](xref:mcp-server). Registra:

- qué permisos se solicitaron y cómo respondiste
- qué herramientas se ejecutaron y si cada una se completó correctamente, falló o fue bloqueada
- el texto completo de cualquier C# Script que el asistente o un agente de MCP haya ejecutado o haya enviado a ejecutar, incluidos los que fallaron durante la ejecución o cuya ejecución fue rechazada

Tus indicaciones, las respuestas del asistente y los valores de datos de tu modelo nunca se registran. Un script que no llega a compilarse no se guarda, y tampoco se guarda el texto de un script que el asistente escribe en un documento para que lo ejecutes tú mismo. **Abrir carpeta de auditoría** en **Herramientas > Preferencias > Funciones de IA** abre la carpeta de registros.

Sin una licencia Enterprise, y antes de activar una licencia, no se registra nada, no se crea ninguna carpeta y no se muestra el botón. Consulta @ai-audit-log para ver qué contiene cada registro, dónde se almacenan los archivos y las directivas que los redirigen.

## Preferencias

Configura las opciones de visualización y comportamiento del Asistente de IA en **Herramientas > Preferencias > Funciones de IA > Asistente de IA > Preferencias**.

### Visualización del chat

| Preferencia                                               | Predeterminado | Descripción                                                                                    |
| --------------------------------------------------------- | -------------- | ---------------------------------------------------------------------------------------------- |
| Mostrar indicador de contexto de selección                | Desactivado    | Muestra el objeto del modelo seleccionado actualmente en el chat                               |
| Mostrar indicador de instrucciones personalizadas         | Desactivado    | Muestra los indicadores de instrucciones personalizadas encima de las respuestas del asistente |
| Mostrar indicador de búsqueda en la base de conocimientos | Desactivado    | Muestra el progreso al buscar en la base de conocimientos                                      |

### Compactación de contexto

| Preferencia                         | Predeterminado | Descripción                                                                                                                                                                                                                                                               |
| ----------------------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Compactación automática             | Activado       | Resumir automáticamente los mensajes antiguos al acercarse al límite del contexto                                                                                                                                                                                         |
| Umbral de compactación automática % | 80             | Porcentaje de la ventana de contexto del propio modelo a partir del cual se activa la compactación automática. El campo acepta valores de 25 a 100. Los valores inferiores a 50 se tratan como 50 y los superiores a 90 se tratan como 90 |

### C# Script

| Preferencia                                                     | Predeterminado | Descripción                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| --------------------------------------------------------------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Permitir que el Asistente de IA ejecute C# Scripts directamente | Desactivado    | Permite que el asistente ejecute sus C# Scripts por sí solo. Cuando está desactivado, el asistente abre cada script y tú lo ejecutas. No está disponible hasta que **Metadatos del modelo** se configure como **Lectura/escritura** en **Permisos**, y no está disponible en absoluto si se aplica la [directiva](xref:policies) `DisableCSharpScripts`. Consulta [Dejar que el asistente cambie tu modelo](#letting-the-assistant-change-your-model) |
| Previsualizar cambios                                           | Activado       | Mostrar el cuadro de diálogo de vista previa de cambios al ejecutar C# Scripts generados por IA desde el chat                                                                                                                                                                                                                                                                                                                                                                                         |

La opción **Buscar actualizaciones de la base de conocimiento al iniciar** y el botón **Abrir carpeta de auditoría** están en la página **Funciones de IA**, por encima de **AI Assistant**, y ambos también se aplican al servidor MCP. Consulta @preferencias.

![La página de preferencias de AI Assistant, con los tres indicadores de visualización del chat desactivados (valor predeterminado), Compactación automática seleccionada con un umbral de 80, la opción Permitir que AI Assistant ejecute C# Scripts directamente desactivada y Vista previa de cambios seleccionada](~/content/assets/images/ai-assistant/ai-assistant-preferences.png)

## Uso de tokens

Cada mensaje al Asistente de IA consume tokens de entrada. El coste en tokens de un mensaje individual depende del contexto que incluya:

- **Prompt del sistema e Instrucciones personalizadas**: se envían con cada mensaje; por lo general, entre 5.000 y 15.000 tokens, según qué Instrucciones personalizadas estén activas
- **Metadatos del modelo**: se recuperan mediante llamadas a herramientas, por etapas. Primero, el asistente obtiene un resumen ligero (nombres de tablas y medidas, relaciones); luego busca objetos relevantes por nombre, descripción o expresión DAX, y recupera los detalles completos solo de las tablas u objetos que requiera la pregunta. Un resultado de una herramienta muy grande se trunca, con indicaciones sobre cómo el asistente puede recuperar el resto

### Contador de tokens

El contador de tokens está en la barra de estado, encima del cuadro de mensaje, junto al [indicador del modelo activo](#choosing-a-model). La barra muestra utilizados/total en miles de tokens y se colorea en verde, ámbar o rojo a medida que se llena el contexto. Un `±` delante de la cifra significa que todavía no hay un recuento exacto.

Pasa el cursor sobre el contador para ver el desglose:

| Sección                                              | Qué incluye                                                                                                                                                            |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Último intercambio**                               | Lo que costó el intercambio más reciente: entrada nueva, tokens servidos desde la caché de prompts del proveedor, tokens escritos en la caché y salida |
| **Esta conversación (facturada)** | Las mismas cuatro cifras acumuladas en todas las solicitudes de la conversación, incluidas las interacciones de ida y vuelta con las herramientas                      |
| **Contexto**                                         | Tokens que hay actualmente en la ventana de contexto, frente al tamaño real de la ventana                                                                              |

Una línea dice, por ejemplo, `37,588 input + 131,744 cached · write 37,558 · output 2,866`. Las secciones de caché se omiten para los proveedores que no admiten el almacenamiento en caché de prompts, y también se omite una sección cuando no tiene nada que incluir en el Report.

> [!TIP]
> Compara **Último turno** con **Esta conversación (facturada)** para ver cuánto costó una sola pregunta. En una conversación larga, es normal ver una cifra alta en **Esta conversación (facturada)** junto a una cifra pequeña en **Último turno**.

### Ventana de contexto

La barra de uso del contexto, el punto de compactación automática y la longitud máxima de una sola respuesta se basan en la ventana de contexto del modelo seleccionado. Por ejemplo, un modelo con una ventana de un millón de tokens se mide contra un millón de tokens. Si no se conoce la ventana del modelo (un nombre de implementación de Azure OpenAI o Custom, o un equipo en el que nunca se ha recuperado el catálogo de modelos), Tabular Editor usa 200.000 tokens.

### Reducir el uso de tokens

Selecciona objetos específicos en el **Explorador TOM** antes de hacer tu pregunta. Después, el asistente limita su contexto a los objetos seleccionados y no recupera metadatos de todo el modelo; esto es lo que más reduce tanto el uso de tokens como el coste de la API.

Otras formas de reducir el uso de tokens:

- Haz preguntas concretas sobre tablas, medidas o columnas específicas. Una instrucción imprecisa como "Establece carpetas de visualización en todas las medidas" obliga al asistente a recuperar metadatos de todo el modelo. Una instrucción específica como "Establece carpetas de visualización en las medidas que he seleccionado" limita el contexto a la selección actual y usa muchos menos tokens
- Inicia una conversación nueva cuando cambies de tema, para evitar que se acumulen historiales largos
- Usa un modelo más pequeño o menos costoso para preguntas exploratorias

## Limitaciones

- requiere tu propia clave de API; no se incluye ninguna clave de API
- la calidad de las respuestas depende del proveedor y del modelo que selecciones
- el Asistente de IA no sustituye el conocimiento de DAX ni los fundamentos del diseño de modelos semánticos
- el Asistente de IA no puede acceder a archivos o servicios externos ni buscar en la web
- el Asistente de IA no puede conectarse a servidores MCP externos para ampliar sus propias herramientas. Para usar tu propio agente con Tabular Editor 3, consulta @mcp-server
- el Asistente de IA no puede conectarse a otro modelo desde el chat. Cambia las conexiones del modelo en la interfaz de usuario de Tabular Editor
- el Asistente de IA no puede administrar las preferencias

## Desactivar el Asistente de IA

El Asistente de IA es un componente opcional, instalado de forma predeterminada a partir de Tabular Editor 3.27.0. Vuelve a ejecutar el instalador de Tabular Editor 3 para incluirlo o excluirlo de una instalación existente. En la versión portátil, elimina `TabularEditor3.AI.dll` del directorio de instalación para quitar este componente.

El mismo componente contiene el servidor MCP, por lo que excluirlo o eliminar `TabularEditor3.AI.dll` elimina ambos. Para desactivar solo el chat, mantén el componente y establece la directiva `DisableAiChat`.

> [!NOTE]
> Independientemente de si el componente está instalado o no, un administrador del sistema puede desactivar toda la funcionalidad de IA en Tabular Editor 3, incluido el servidor MCP, mediante la [directiva `DisableAi`](xref:policies). `DisableMcpServer` desactiva solo el servidor MCP. Consulta @policies.
