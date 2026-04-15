---
uid: ai-assistant
title: Asistente de IA
author: Morten Lønskov
updated: 2026-04-15
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

> [!NOTE]
> El Asistente de IA está en vista previa pública a partir de Tabular Editor 3.26.0. Agradecemos tus comentarios sobre la experiencia mientras seguimos mejorándola.

![Primer panel del Asistente de IA al abrirlo](~/content/assets/images/ai-assistant/ai-assistant-panel-first-open.png)

## Primeros pasos

1. Abre **Herramientas > Preferencias > Asistente de IA**
2. Selecciona tu proveedor de IA e introduce tu clave de API
3. Abre el panel del Asistente de IA desde **Vista > Asistente de IA**
4. Escribe mensajes y pulsa **Enter** para iniciar una conversación

> [!TIP]
> Usa nuestra [demo interactiva del Asistente de IA](https://demos.tabulareditor.com/psl/of150vcy?) para ver cómo configurarlo y usarlo.

> [!NOTE]
> Las claves de API se almacenan cifradas en tu equipo local.

## Proveedores compatibles

Configura tu proveedor de IA en **Herramientas > Preferencias > Asistente de IA > Proveedor de IA**. Selecciona un proveedor en el menú desplegable, introduce tu clave de API y, si lo deseas, sobrescribe el nombre del modelo predeterminado.

| Proveedor                                                | Modelo predeterminado            | Configuración necesaria                                                        |
| -------------------------------------------------------- | -------------------------------- | ------------------------------------------------------------------------------ |
| OpenAI                                                   | gpt-4o                           | Clave de API. ID opcional de la organización e ID del proyecto |
| Anthropic                                                | claude-sonnet-4-6                | Clave de API                                                                   |
| Azure OpenAI                                             | Dependiente de la implementación | Clave de API, URL del punto de conexión y nombre de la implementación          |
| Personalizado (compatible con OpenAI) | Especificado por el usuario      | Clave de API y URL personalizada del punto de conexión                         |

![Selección del proveedor del Asistente de IA en Preferencias](~/content/assets/images/ai-assistant/ai-assistant-provider-preferences.png)

### OpenAI

Selecciona **OpenAI** como proveedor e introduce tu clave de API. Opcionalmente, puedes especificar un ID de organización y un ID de proyecto si tu cuenta de OpenAI los usa. El modelo predeterminado es **gpt-4o**, pero puedes cambiarlo por cualquier modelo disponible en tu cuenta.

![Configuración de OpenAI en el Asistente de IA](~/content/assets/images/ai-assistant/ai-assistant-openai-config.png)

### Anthropic

Selecciona **Anthropic** como proveedor e introduce tu clave de API. El modelo predeterminado es **claude-sonnet-4-6**. Puedes cambiar el nombre del modelo a cualquier modelo de Anthropic disponible en tu cuenta.

![Configuración de Anthropic en el Asistente de IA](~/content/assets/images/ai-assistant/ai-assistant-anthropic-config.png)

> [!IMPORTANT]
> Anthropic aplica límites de velocidad de tokens de entrada por minuto (ITPM) en función del nivel de tu cuenta. Una nueva clave de API empieza en el Nivel 1 con 30.000 ITPM para Claude Sonnet 4.x. Una sola solicitud a un modelo grande puede superar este límite. Compra 40 USD o más en créditos de API para alcanzar el Nivel 2 (450.000 ITPM). Consulta la [documentación de límites de velocidad de Anthropic](https://docs.anthropic.com/en/api/rate-limits) para ver todos los detalles de los niveles.

### Azure OpenAI

Select **Azure OpenAI** as the provider and configure three fields:

- **API key** — the access key for your Azure OpenAI resource
- **Service endpoint** — the endpoint URL for your resource, for example `https://your-resource.openai.azure.com`. Use the resource URL, not the `privatelink` alias; the SSL certificate is issued for `*.openai.azure.com` and connecting directly to `*.privatelink.openai.azure.com` fails certificate validation
- **Model name** — the **deployment name**, not the underlying model name and not the resource name

Azure OpenAI requires the deployment name in every API call. A deployment name is chosen when the deployment is created, so it can be any string. Deployments are often named after the model they serve (for example `gpt-4o`), but that is a convention, not a requirement. If you enter the resource name or a raw model name that does not exist as a deployment, the request fails.

#### Finding your deployment name

In the [Azure AI Foundry portal](https://ai.azure.com):

1. Sign in and select your Azure OpenAI resource
2. Open **Deployments** (or **Models + endpoints** if the resource has been upgraded to Foundry)
3. Copy the value from the **Name** column

Deployments created before your organization adopted Azure AI Foundry may not appear in the portal. List them from the Azure CLI:

```bash
az cognitiveservices account deployment list --name "<resource-name>" --resource-group "<resource-group>" --output table
```

See [Create and deploy an Azure OpenAI resource](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/create-resource#deploy-a-model) for more details.

For 403 errors, SSL failures or "DeploymentNotFound" responses, see @azure-openai-connection-errors.

### Personalizado (compatible con OpenAI)

La opción de proveedor Personalizado admite LLM locales o de tu organización que expongan un punto de conexión de API compatible con OpenAI. Introduce tu clave de API y la URL del punto de conexión personalizado. Esto te permite mantener todos los datos dentro de tu propia infraestructura por motivos de privacidad o requisitos de cumplimiento.

### Uso de un LLM local o de tu organización

Puedes ejecutar el Asistente de IA con un LLM autoalojado mediante el proveedor Personalizado. Esto mantiene todos los datos dentro de tu propia infraestructura, ya sea un modelo que se ejecuta en tu equipo local o un LLM alojado de forma centralizada dentro de la red de tu organización. En cualquier caso, no se envía ningún dato a un proveedor de nube de terceros.

Varias herramientas pueden alojar modelos con una API compatible con OpenAI:

- [Ollama](https://ollama.com) — CLI ligera para descargar y ejecutar modelos localmente
- [LM Studio](https://lmstudio.ai) — aplicación de escritorio con interfaz gráfica para administrar y ejecutar modelos locales
- [LocalAI](https://localai.io) — alternativa autoalojada, impulsada por la comunidad, con una amplia compatibilidad de modelos

Estas herramientas pueden ejecutarse en la estación de trabajo de un desarrollador para uso individual o implementarse en un servidor compartido dentro de tu organización para ofrecer a tu equipo un punto de conexión de LLM gestionado de forma centralizada.

#### Ejemplo: Ollama

1. [Descarga e instala Ollama](https://ollama.com/download)
2. Descarga un modelo, por ejemplo: `ollama pull llama3.1`
3. Inicia el servidor de Ollama (se ejecuta automáticamente tras la instalación y, de forma predeterminada, en el puerto 11434)
4. En Tabular Editor, ve a **Herramientas > Preferencias > Asistente de IA > Proveedor de IA**
5. Configura **Elegir proveedor** como **Personalizado (compatible con OpenAI)**
6. Establece **Punto de conexión del servicio** en `http://localhost:11434/v1`
7. Establece **Nombre del modelo** con el modelo que descargaste (p. ej., `llama3.1`)
8. El campo **Clave de API** puede establecerse con cualquier valor no vacío (p. ej., `ollama`) — Ollama no requiere autenticación, pero el campo no puede dejarse en blanco

#### Ejemplo: LM Studio

1. [Descargar LM Studio](https://lmstudio.ai/download)
2. Descarga un modelo. Ya sea desde la página de búsqueda de modelos del panel izquierdo o mediante la CLI. Por ejemplo: `lms get lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF`
3. Inicia el servidor de LM Studio. Ya sea desde la página para desarrolladores del panel izquierdo o mediante la CLI. por ejemplo `lms server start`
   Nota: tendrás que configurarlo para que use el modo compatible con OpenAI. Además, puede que tengas que cambiar el tamaño de contexto predeterminado para que sea superior a 100000 tokens.
4. En Tabular Editor, ve a **Herramientas > Preferencias > Asistente de IA > Proveedor de IA**
5. Configura **Elegir proveedor** como **Personalizado (compatible con OpenAI)**
6. Establece **Punto de conexión del servicio** en `http://localhost:1234/v1`
7. Establece **Nombre del modelo** con el modelo que descargaste (p. ej., `lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF`)
8. El campo **Clave de API** puede establecerse con cualquier valor no vacío (p. ej., `lms`) — LM Studio no requiere autenticación, pero el campo no puede dejarse en blanco

> [!NOTE]
> La calidad de las respuestas con modelos locales depende del tamaño del modelo y de tu hardware. Los modelos más grandes suelen producir mejores resultados, pero requieren más RAM y una GPU capaz. Las capacidades de llamada a herramientas del Asistente de IA requieren un modelo que admita llamadas a funciones en el formato compatible con OpenAI.

> [!TIP]
> We recommend a model with a _minimum_ of 30 billion parameters but ideally at least 100 billion parameters. Por ejemplo, el modelo Qwen3.5-122B-A10B funcionó bien en nuestras pruebas internas.

## Capacidades

El Asistente de IA tiene acceso al contexto de tu modelo y puede realizar las siguientes acciones:

- **Exploración del modelo**: Consultar los metadatos del modelo, incluidas tablas, columnas, medidas, relaciones y sus propiedades
- **Redacción de Consultas DAX**: Generar Consultas DAX y ejecutarlas contra tu modelo en modo conectado, devolviendo conjuntos de resultados directamente en el chat
- **Generación de C# Scripts**: Crear C# Scripts para modificar el modelo, que se abren en una nueva ventana del editor. Cuando haces clic en **Ejecutar** en el chat, de forma predeterminada se muestra el cuadro de diálogo [Vista previa de cambios](xref:csharp-scripts#running-scripts-with-preview), lo que te permite revisar todos los cambios en los metadatos del modelo antes de aceptarlos. También puedes abrir el script en el editor y ejecutarlo desde la barra de herramientas de scripts, con o sin la vista previa. Los cambios en los metadatos del modelo se pueden deshacer con **Ctrl+Z**
- **Best Practice Analyzer**: Ejecutar el análisis de BPA, ver infracciones de las reglas y crear o modificar reglas de BPA
- **Analizador VertiPaq**: Consultar estadísticas de uso de memoria y cardinalidad de columnas
- **Acceso a documentos**: Leer y modificar documentos abiertos, como scripts DAX y Consultas DAX
- **Búsqueda en la base de conocimientos**: Buscar en la documentación integrada de Tabular Editor para encontrar respuestas
- **Navegación por la interfaz de usuario**: Generar enlaces de acción `te3://` que abren cuadros de diálogo y funcionalidades específicas de Tabular Editor

## Conversaciones

El Asistente de IA admite varias conversaciones simultáneas. Cada conversación mantiene su propio historial de mensajes y contexto.

- Las conversaciones se conservan entre sesiones y se almacenan localmente en `%LocalAppData%\TabularEditor3\AI\Conversations\`
- Los títulos se generan automáticamente tras el primer intercambio. Puedes cambiar el nombre de las conversaciones manualmente
- **Compactación automática**: Cuando la conversación se acerca al límite de la ventana de contexto (~80%), los mensajes más antiguos se resumen automáticamente para liberar espacio. Se archiva una instantánea de la conversación completa antes de la compactación

## Artefactos

Cuando el Asistente de IA genera código, crea **artefactos** que se abren directamente en ventanas del editor:

- **C# Scripts**: Se abren en un nuevo editor de C# Script con resaltado de sintaxis, compilación y compatibilidad con la ejecución
- **Consultas DAX**: Se abren en un nuevo editor de consultas DAX con resaltado de sintaxis y compatibilidad con la ejecución

Los artefactos se transmiten en tiempo real a medida que la IA los genera. Los artefactos de C# Script incluyen un análisis de seguridad que señala código potencialmente inseguro (p. ej., acceso al sistema de archivos u operaciones de red).

![Asistente de IA: generar un C# Script](~/content/assets/images/ai-assistant/ai-assistant-generate-c-sharp-script.png)

Cuando ejecutas un C# Script desde el chat, el cuadro de diálogo **Vista previa del script** muestra una comparación en paralelo de todos los cambios de metadatos del modelo realizados por el script. Puedes aceptar los cambios o revertirlos. Consulta [Ejecutar scripts con vista previa](xref:csharp-scripts#run-c-scripts-with-preview) para obtener más información.

![Vista previa del script: cambios del modelo](~/content/assets/images/preview-script-changes.png)

## Instrucciones personalizadas

Las instrucciones personalizadas son conjuntos de instrucciones que guían el comportamiento del Asistente de IA para tareas específicas. Se activan automáticamente según la detección de intenciones o se invocan de forma explícita.

### Instrucciones personalizadas integradas

El Asistente de IA incluye las siguientes instrucciones personalizadas integradas:

| Instrucción personalizada | Se activa cuando                                   |
| ------------------------- | -------------------------------------------------- |
| Consulta DAX              | DAX, consulta, EVALUATE, medida                    |
| Modificación del modelo   | Modificar, cambiar, agregar, actualizar, crear     |
| Diseño del modelo         | Diseño, arquitectura, patrón, práctica recomendada |
| Organizar el modelo       | Organizar, limpiar, carpeta, cambiar nombre        |
| Optimizar el modelo       | Optimizar, rendimiento, lento, velocidad           |
| Macros                    | Macro, automatizar, grabar                         |
| UDFs                      | UDF, función, definida por el usuario              |
| BPA                       | BPA, práctica recomendada, regla, infracción       |

Las instrucciones personalizadas se muestran como indicadores encima de las respuestas del asistente, lo que indica qué instrucciones influyeron en la respuesta. Puedes activar o desactivar esta visualización en **Preferencia > Asistente de IA > Preferencia > Mostrar indicador de instrucciones personalizadas**.

### Invocar una instrucción personalizada

Escribe `/` para explorar las instrucciones personalizadas disponibles, o escribe el `/instruction-id` completo al inicio de tu mensaje para invocar explícitamente una instrucción concreta. Por ejemplo, `/dax-querying` fuerza la instrucción de Consulta DAX independientemente del contenido de tu mensaje.

### Añade tus propias instrucciones personalizadas

Puedes crear instrucciones personalizadas colocando archivos `.md` en `%LocalAppData%\TabularEditor3\AI\CustomInstructions\`. Cada archivo requiere un front matter YAML que defina los metadatos de la instrucción:

```yaml
---
id: my-custom-skill
name: My Custom Skill
description: A brief description shown in the autocomplete popup.
priority: 100
always_inject: false
hidden: false
triggers:
  keywords:
    - keyword1
    - keyword2
  patterns:
    - "\\bregex pattern\\b"
  context_required:
    - model_loaded
---

Aquí va el contenido de tu instrucción. Este es el texto que se
insertará en el prompt del sistema de la IA cuando se active la instrucción.
```

| Campo                       | Obligatorio | Predeterminado                                         | Descripción                                                                                                 |
| --------------------------- | ----------- | ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| `id`                        | No          | Nombre de archivo sin `.md`                            | Identificador único; también se usa como `/id` para la invocación explícita                                 |
| `name`                      | No          | `id` con mayúsculas iniciales                          | Nombre para mostrar en el autocompletado                                                                    |
| `description`               | No          | -                                                      | Breve descripción que se muestra debajo del nombre                                                          |
| `priority`                  | No          | 100                                                    | Los valores más altos se inyectan primero cuando coinciden varias instrucciones personalizadas              |
| `always_inject`             | No          | false                                                  | Si es `true`, siempre se incluye en el prompt del sistema                                                   |
| `hidden`                    | No          | false                                                  | Si es `true`, no se muestra en el autocompletado de `/command`                                              |
| `triggers.keywords`         | No          | [] | Palabras que activan la instrucción (no distingue entre mayúsculas y minúsculas)         |
| `triggers.patterns`         | No          | [] | Patrones de regex para coincidencias complejas                                                              |
| `triggers.context_required` | No          | [] | Condiciones que deben cumplirse (p. ej., `model_loaded`) |

Las instrucciones personalizadas con un `id` que coincida con el de una instrucción integrada sustituirán la versión integrada.

## Consentimiento

El Asistente de IA solicita permiso antes de enviar datos al proveedor de IA. El consentimiento se limita a tipos de datos específicos:

| Categoría de consentimiento | Descripción                                                                         |
| --------------------------- | ----------------------------------------------------------------------------------- |
| Datos de consulta           | Resultados de Consultas DAX y muestras de datos                                     |
| Leer documentos             | Lectura del contenido de documentos abiertos, como scripts DAX y Consultas DAX      |
| Modificar documentos        | Realizar cambios en los documentos abiertos                                         |
| Metadatos del modelo        | Esquemas de tablas y columnas, definiciones de medidas y otros metadatos del modelo |
| Editar reglas de BPA        | Crear o modificar reglas de Best Practice Analyzer                                  |
| Leer macros                 | Lectura de las definiciones de macros                                               |

Cuando el Asistente de IA necesita acceder a un tipo de datos por primera vez, aparece un cuadro de diálogo de consentimiento. Puede elegir la duración de su consentimiento:

| Opción           | Ámbito                                                                                                 |
| ---------------- | ------------------------------------------------------------------------------------------------------ |
| Esta vez         | Solo para esta solicitud                                                                               |
| Esta sesión      | Hasta que se reinicie Tabular Editor                                                                   |
| Para este modelo | Se conserva en el archivo de opciones de usuario (.tmuo) del modelo |
| Siempre          | Preferencia global, que se conserva en todos los modelos y sesiones                                    |

![Cuadro de diálogo de consentimiento del Asistente de IA](~/content/assets/images/ai-assistant/ai-assistant-generate-consent-dialog.png)

### Gestión de consentimientos

Puedes revisar y restablecer tus opciones de consentimiento en **Herramientas > Preferencias > Asistente de IA > Consentimientos de IA**. Cada categoría de consentimiento muestra su estado actual. Haz clic en **Restablecer** para revocar un consentimiento de "Siempre permitido" y volver a "Preguntar cuando sea necesario".

![Configuración de consentimiento del Asistente de IA](~/content/assets/images/ai-assistant/ai-assistant-consent-reset.png)

## Preferencias

Configura las opciones de visualización y comportamiento del Asistente de IA en **Herramientas > Preferencias > Asistente de IA > Preferencias**.

### Visualización del chat

| Preferencia                                               | Predeterminado | Descripción                                                                                    |
| --------------------------------------------------------- | -------------- | ---------------------------------------------------------------------------------------------- |
| Mostrar indicador de contexto de selección                | true           | Muestra el objeto del modelo seleccionado actualmente en el chat                               |
| Mostrar indicador de instrucciones personalizadas         | true           | Muestra los indicadores de instrucciones personalizadas encima de las respuestas del asistente |
| Mostrar indicador de búsqueda en la base de conocimientos | true           | Muestra el progreso al buscar en la base de conocimientos                                      |

### Compactación de contexto

| Preferencia                         | Predeterminado | Descripción                                                                       |
| ----------------------------------- | -------------- | --------------------------------------------------------------------------------- |
| Compactación automática             | true           | Resumir automáticamente los mensajes antiguos al acercarse al límite del contexto |
| Umbral de compactación automática % | 80             | Porcentaje de uso de tokens que activa la compactación automática                 |

### Base de conocimientos

| Preferencia                                                   | Predeterminado | Descripción                                                                                        |
| ------------------------------------------------------------- | -------------- | -------------------------------------------------------------------------------------------------- |
| Buscar actualizaciones de la base de conocimientos al iniciar | true           | Buscar automáticamente actualizaciones de la base de conocimientos cuando se inicie Tabular Editor |

### C# Script

| Preferencia           | Predeterminado | Descripción                                                                                                   |
| --------------------- | -------------- | ------------------------------------------------------------------------------------------------------------- |
| Previsualizar cambios | true           | Mostrar el cuadro de diálogo de vista previa de cambios al ejecutar C# Scripts generados por IA desde el chat |

![Preferencias del asistente de IA](~/content/assets/images/ai-assistant/ai-assistant-preferences.png)

## Uso de tokens

Cada mensaje al Asistente de IA consume tokens de entrada. El coste en tokens de un solo mensaje depende de qué contexto se incluya:

- **Prompt del sistema e instrucciones personalizadas**: Se envían con cada mensaje. Normalmente, entre 5.000 y 15.000 tokens, según las instrucciones personalizadas que estén activas.
- **Metadatos del modelo**: Cuando el asistente necesita entender tu modelo, recupera los metadatos mediante llamadas a herramientas. Un resumen compacto incluye nombres de tablas, columnas y medidas, relaciones y descripciones. Una recuperación completa de metadatos incluye la definición completa del modelo. En modelos grandes, esto puede consumir decenas de miles de tokens.

### Reducir el uso de tokens

Selecciona objetos específicos en el **Explorador TOM** antes de hacer tu pregunta. Cuando hay objetos seleccionados, el asistente limita su contexto a esos objetos en lugar de obtener los metadatos de todo el modelo. Esta es la forma más eficaz de reducir tanto el uso de tokens como el coste de la API.

Otras formas de reducir el uso de tokens:

- Ask focused questions about specific tables, measures or columns rather than broad questions about the entire model. A vague prompt such as _"Set display folders on all measures"_ forces the assistant to retrieve metadata for the entire model. A specific prompt such as _"Set display folders on the measures I have selected"_ limits the context to the current selection and uses far fewer tokens
- Inicia nuevas conversaciones al cambiar de tema para evitar acumular historiales de conversación extensos
- Usa un modelo más pequeño o menos costoso para preguntas exploratorias

## Limitaciones

- Requiere una clave de API proporcionada por el usuario. No se incluye ninguna clave de API integrada
- Las respuestas de la IA dependen del modelo seleccionado y de las capacidades del proveedor
- La ventana de contexto máxima es de 200.000 tokens
- El Asistente de IA no sustituye la comprensión de los fundamentos de DAX y del diseño de modelos semánticos
- La calidad de las respuestas varía según el proveedor y el modelo seleccionado
- El Asistente de IA no puede conectarse a archivos o servicios externos ni buscar en la web
- El Asistente de IA no puede añadirse ni actuar como un servidor MCP
- El Asistente de IA no puede conectarse a otro modelo desde el chat. Usa la interfaz de usuario de Tabular Editor para cambiar las conexiones del modelo
- El Asistente de IA no puede administrar las preferencias

## Desactivar el Asistente de IA

El Asistente de IA es un componente opcional. Mientras la característica esté en versión preliminar pública, se excluirá de forma predeterminada durante la instalación, pero los usuarios tienen la opción de incluirla. Puedes modificar una instalación existente de Tabular Editor 3 para incluir o excluir el componente del Asistente de IA volviendo a ejecutar el instalador de Tabular Editor 3. Si usas la versión portable de Tabular Editor 3, puedes quitar el componente del Asistente de IA eliminando el archivo `TabularEditor3.AI.dll` del directorio de instalación.

> [!NOTE]
> Independientemente de si el componente del Asistente de IA está instalado o no, un administrador del sistema puede desactivar toda la funcionalidad de IA en Tabular Editor 3 especificando la [directiva `DisableAi`](xref:policies).