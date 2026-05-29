---
uid: ai-assistant
title: Asistente de IA
author: Morten Lønskov
updated: 2026-04-17
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

El Asistente de IA es una interfaz conversacional para el desarrollo de modelos semánticos con ayuda de IA, diseñada para ayudarte a crear modelos semánticos más rápido. Con un diseño preparado para entornos empresariales, control total sobre lo que se envía a la IA y gestión integrada del consentimiento, puedes usar el Asistente de IA con confianza. El Asistente de IA ha sido sometido a pruebas de penetración de seguridad independientes. Para obtener más información, visita el [Centro de confianza de Tabular Editor](https://trust.tabulareditor.com). El Asistente de IA puede explorar los metadatos de tu modelo, escribir y ejecutar consultas DAX, generar C# Scripts, ejecutar comprobaciones del Best Practice Analyzer, consultar las estadísticas del Analizador VertiPaq y buscar en la base de conocimientos de Tabular Editor.

El Asistente de IA utiliza un modelo BYOK, «trae tu propia clave». Proporcionas una clave de API de uno de los proveedores compatibles y el asistente se ejecuta directamente contra la API de ese proveedor.

> [!NOTE]
> El Asistente de IA está en vista previa pública a partir de Tabular Editor 3.26.0. Agradecemos tus comentarios sobre la experiencia mientras seguimos perfeccionándola.

![Panel del Asistente de IA al abrirlo por primera vez](~/content/assets/images/ai-assistant/ai-assistant-panel-first-open.png)

## Primeros pasos

1. Abre **Herramientas > Preferencias > Asistente de IA**
2. Selecciona tu proveedor de IA — en una instalación limpia, el valor predeterminado es **Ninguno (IA deshabilitada)** — y, a continuación, introduce tu clave de API
3. Abre el panel del Asistente de IA desde **Ver > Asistente de IA**
4. Escribe un mensaje y pulsa **Enter** para iniciar una conversación

> [!TIP]
> Usa nuestra [demo interactiva del Asistente de IA](https://demos.tabulareditor.com/psl/of150vcy?) para ver cómo configurarlo y usarlo.

> [!NOTE]
> Las claves de API se almacenan cifradas en tu máquina local.

## Proveedores compatibles

Configura tu proveedor de IA en **Herramientas > Preferencias > Asistente de IA > Proveedor de IA**. Selecciona un proveedor en la lista desplegable — el valor predeterminado es **Ninguno (IA deshabilitada)** hasta que configures uno —, introduce tu clave de API y, si quieres, sobrescribe el modelo predeterminado. Para OpenAI y Anthropic, el campo **Nombre del modelo** es un cuadro combinado precargado con modelos conocidos; también puedes escribir un nombre de modelo personalizado.

| Proveedor                                                | Modelo predeterminado  | Configuración requerida                                                              |
| -------------------------------------------------------- | ---------------------- | ------------------------------------------------------------------------------------ |
| OpenAI                                                   | gpt-4o                 | Clave de API. URL base opcional, ID de organización e ID de proyecto |
| Anthropic                                                | claude-sonnet-4-6      | Clave de API. URL base opcional                                      |
| Azure OpenAI                                             | Depende del despliegue | Clave de API, URL del punto de conexión y nombre del despliegue                      |
| Personalizado (compatible con OpenAI) | Especificado por ti    | Clave de API y URL del punto de conexión personalizada                               |

![Selección del proveedor del Asistente de IA en Preferencias](~/content/assets/images/ai-assistant/ai-assistant-provider-preferences.png)

### OpenAI

Selecciona **OpenAI** como proveedor e introduce tu clave de API. Opcionalmente, puedes especificar un ID de organización y un ID de proyecto si tu cuenta de OpenAI los utiliza. El modelo predeterminado es **gpt-4o**, pero puedes cambiarlo a cualquier modelo disponible en tu cuenta.

![Configuración de OpenAI del asistente de IA](~/content/assets/images/ai-assistant/ai-assistant-openai-config.png)

### Anthropic

Selecciona **Anthropic** como proveedor e introduce tu clave de API. El modelo predeterminado es **claude-sonnet-4-6**. Puedes cambiar el nombre del modelo a cualquier modelo de Anthropic disponible en tu cuenta.

![Configuración de Anthropic del asistente de IA](~/content/assets/images/ai-assistant/ai-assistant-anthropic-config.png)

> [!IMPORTANT]
> Anthropic impone límites de tasa de tokens de entrada por minuto (ITPM) según el nivel de tu cuenta. Una clave de API nueva empieza en el nivel 1, con 30.000 ITPM para Claude Sonnet 4.x. Una sola solicitud a un modelo grande puede superar este límite. Compra créditos de API por un importe de 40 USD o más para alcanzar el nivel 2 (450.000 ITPM). Consulta la [documentación sobre los límites de velocidad de Anthropic](https://docs.anthropic.com/en/api/rate-limits) para ver todos los detalles de cada nivel.

### Azure OpenAI

Selecciona **Azure OpenAI** como proveedor y configura estos tres campos:

- **Clave de API** — la clave de acceso de tu recurso de Azure OpenAI
- **Punto de conexión del servicio** — la URL del punto de conexión de tu recurso, por ejemplo `https://your-resource.openai.azure.com`. Usa la URL del recurso, no el alias `privatelink`; el certificado SSL se emite para `*.openai.azure.com`, y conectarse directamente a `*.privatelink.openai.azure.com` hace que falle la validación del certificado
- **Nombre del modelo** — el **nombre de la implementación**, no el nombre del modelo subyacente ni el nombre del recurso

Azure OpenAI requiere el nombre de la implementación en cada llamada a la API. El nombre de la implementación se elige al crearla, así que puede ser cualquier cadena. Las implementaciones suelen llevar el nombre del modelo al que sirven (por ejemplo, `gpt-4o`), pero eso es una convención, no un requisito. Si introduces el nombre del recurso o un nombre de modelo base que no exista como implementación, la solicitud fallará.

#### Cómo encontrar el nombre de tu implementación

En el [portal de Azure AI Foundry](https://ai.azure.com):

1. Inicia sesión y selecciona tu recurso de Azure OpenAI
2. Abre **Deployments** (o **Models + endpoints** si el recurso se ha actualizado a Foundry)
3. Copia el valor de la columna **Name**

Es posible que las implementaciones creadas antes de que tu organización adoptara Azure AI Foundry no aparezcan en el portal. Enuméralas con la CLI de Azure:

```bash
az cognitiveservices account deployment list --name "<resource-name>" --resource-group "<resource-group>" --output table
```

Consulta [Crear e implementar un recurso de Azure OpenAI](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/create-resource#deploy-a-model) para obtener más información.

Para errores 403, fallos de SSL o respuestas "DeploymentNotFound", consulta @azure-openai-connection-errors.

> [!NOTE]
> El proveedor **Azure OpenAI** está pensado para recursos clásicos de Azure OpenAI que usan el parámetro de consulta `api-version`. Si usas el nuevo **Microsoft Foundry**, consulta [Uso de Microsoft Foundry](#using-microsoft-foundry) a continuación.

### Personalizado (compatible con OpenAI)

La opción del proveedor Personalizado admite LLM locales o de tu organización que expongan un punto de conexión de API compatible con OpenAI. Introduce tu clave de API y la URL del punto de conexión personalizado. Esto te permite mantener todos los datos dentro de tu propia infraestructura para cumplir con los requisitos de privacidad de datos o de cumplimiento normativo.

### Uso de un LLM local o de tu organización

Puedes ejecutar el Asistente de IA con un LLM autoalojado usando el proveedor Personalizado. Esto mantiene todos los datos dentro de tu propia infraestructura, ya sea un modelo que se ejecuta en tu equipo local o un LLM alojado de forma centralizada dentro de la red de tu organización. En cualquier caso, no se envían datos a un proveedor de nube externo.

Hay varias herramientas que pueden alojar modelos con una API compatible con OpenAI:

- [Ollama](https://ollama.com) — CLI ligera para descargar y ejecutar modelos localmente
- [LM Studio](https://lmstudio.ai) — aplicación de escritorio con interfaz gráfica para administrar y ejecutar modelos locales
- [LocalAI](https://localai.io) — alternativa autoalojada, impulsada por la comunidad y con amplia compatibilidad de modelos

Estas herramientas pueden ejecutarse en la estación de trabajo de un desarrollador para uso individual o implementarse en un servidor compartido dentro de tu organización para proporcionar a tu equipo un punto de conexión de LLM gestionado de forma centralizada.

#### Ejemplo: Ollama

1. [Descarga e instala Ollama](https://ollama.com/download)
2. Descarga un modelo, por ejemplo: `ollama pull llama3.1`
3. Inicia el servidor de Ollama (se ejecuta automáticamente después de la instalación, de forma predeterminada en el puerto 11434)
4. En Tabular Editor, ve a **Herramientas > Preferencias > Asistente de IA > Proveedor de IA**
5. Configura **Elegir proveedor** como **Personalizado (compatible con OpenAI)**
6. Configura **Punto de conexión del servicio** como `http://localhost:11434/v1`
7. Configura **Nombre del modelo** como el modelo que descargaste (por ejemplo, `llama3.1`)
8. Puedes poner cualquier valor no vacío en el campo **Clave de API** (por ejemplo, `ollama`) — Ollama no requiere autenticación, pero el campo no puede dejarse en blanco

#### Ejemplo: LM Studio

1. [Descargar LM Studio](https://lmstudio.ai/download)
2. Descarga un modelo. Ya sea desde la página de búsqueda de modelos del panel izquierdo o desde la CLI. Por ejemplo: `lms get lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF`
3. Inicia el servidor de LM Studio. Ya sea desde la página para desarrolladores del panel izquierdo o mediante la CLI. por ejemplo `lms server start`
   Nota: tendrás que configurarlo para usar el modo compatible con OpenAI. Además, puede que tengas que cambiar el tamaño de contexto predeterminado para que supere los 100.000 tokens.
4. En Tabular Editor, ve a **Herramientas > Preferencias > Asistente de IA > Proveedor de IA**
5. Configura **Elegir proveedor** como **Personalizado (compatible con OpenAI)**
6. Configura **Punto de conexión del servicio** como `http://localhost:1234/v1`
7. Configura **Nombre del modelo** con el modelo que descargaste (p. ej., `lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF`)
8. Puedes poner cualquier valor no vacío en el campo **Clave de API** (por ejemplo, `lms`) — LM Studio no requiere autenticación, pero el campo no puede dejarse en blanco

> [!NOTE]
> La calidad de las respuestas con modelos locales depende del tamaño del modelo y de tu hardware. En general, los modelos más grandes producen mejores resultados, pero requieren más RAM y una GPU potente. Las capacidades de llamada a herramientas del Asistente de IA requieren un modelo que admita la llamada a funciones en el formato compatible con OpenAI.

> [!TIP]
> Recomendamos un modelo con un _mínimo_ de 30 mil millones de parámetros, pero idealmente de al menos 100 mil millones de parámetros. Por ejemplo, el modelo Qwen3.5-122B-A10B obtuvo buenos resultados en nuestras pruebas internas.

### Uso de Microsoft Foundry

[Microsoft Foundry](https://ai.azure.com) (anteriormente Azure AI Foundry) te permite implementar modelos de OpenAI y Anthropic en tu entorno de Azure. Se accede a estos modelos a través del proveedor **OpenAI** o **Anthropic** en Tabular Editor — no a través del proveedor **Azure OpenAI**, que es para recursos clásicos de Azure OpenAI.

> [!IMPORTANT]
> No uses el proveedor **Azure OpenAI** para modelos de Microsoft Foundry. El proveedor **Azure OpenAI** solo es compatible con recursos clásicos de Azure OpenAI.

#### Modelos de OpenAI en Microsoft Foundry

Para usar un modelo de OpenAI (como GPT-4o o GPT-5.4-mini; 5,4) implementado en Microsoft Foundry:

1. En Tabular Editor, ve a **Herramientas > Preferencia > Asistente de IA > Proveedor de IA**
2. Establece **Choose provider** en **OpenAI**
3. Establece **Base URL** en el punto de conexión de tu recurso de Foundry y añade `/openai/v1` al final. La URL sigue uno de estos formatos:
   - `https://your-resource.services.ai.azure.com/openai/v1`
   - `https://your-resource.openai.azure.com/openai/v1`
4. Introduce tu **API Key** de Foundry
5. Establece **Model name** en el nombre de tu implementación (p. ej., `gpt-5.4-mini`; 5,4)

> [!NOTE]
> La URL base no se muestra directamente en el portal de Microsoft Foundry. El portal muestra un **URI de destino** que incluye la ruta completa de la API (por ejemplo, `https://your-resource.services.ai.azure.com/api/projects/YourProject/openai/v1/responses`). Para la URL base, usa solo `https://your-resource.services.ai.azure.com/openai/v1`.

#### Modelos de Anthropic en Microsoft Foundry

Para usar un modelo de Anthropic (como Claude Sonnet 4.6; 4,6) implementado en Microsoft Foundry:

1. En Tabular Editor, ve a **Herramientas > Preferencia > Asistente de IA > Proveedor de IA**
2. Establece **Choose provider** en **Anthropic**
3. Establece **Base URL** en el punto de conexión de tu recurso de Foundry y añade `/anthropic` al final; por ejemplo, `https://your-resource.services.ai.azure.com/anthropic`
4. Introduce tu **API Key** de Foundry
5. Establece **Nombre del modelo** en el identificador del modelo (por ejemplo, `claude-sonnet-4-6`)

> [!NOTE]
> El portal muestra un **URI de destino** como `https://your-resource.services.ai.azure.com/anthropic/v1/messages`. Para la URL base, usa solo la parte hasta e incluyendo `/anthropic`.

## Capacidades

El Asistente de IA tiene acceso al contexto de tu modelo y puede realizar las siguientes acciones:

- **Exploración del modelo**: Consultar metadatos del modelo, incluidas tablas, columnas, medidas, relaciones y sus propiedades
- **Redacción de consultas DAX**: Generar Consultas DAX y ejecutarlas en modo conectado contra tu modelo, devolviendo conjuntos de resultados directamente en el chat
- **Generación de C# Script**: Crear C# Scripts para modificaciones del modelo que se abren en una nueva ventana del editor. Al hacer clic en **Ejecutar** en el chat, se muestra de forma predeterminada el cuadro de diálogo [vista previa de cambios](xref:csharp-scripts#run-c-scripts-with-preview), lo que te permite revisar todos los cambios en los metadatos del modelo antes de aceptarlos. También puedes abrir el script en el editor y ejecutarlo desde la barra de herramientas de scripts, con o sin la vista previa. Los cambios en los metadatos del modelo se pueden deshacer con **Ctrl+Z**
- **Best Practice Analyzer**: Ejecutar análisis de BPA, ver infracciones de reglas y crear o modificar reglas de BPA
- **Analizador VertiPaq**: Consultar estadísticas de uso de memoria y cardinalidad de columnas
- **Acceso a documentos**: Leer y modificar documentos abiertos, como scripts DAX y Consultas DAX
- **Búsqueda en la base de conocimientos**: Buscar respuestas en la documentación integrada de Tabular Editor
- **Navegación por la interfaz de usuario**: Generar vínculos de acción `te3://` que abren cuadros de diálogo y funciones específicas de Tabular Editor

> [!NOTE]
> Las herramientas que requieren una conexión activa a la base de datos —como la ejecución de Consultas DAX y las estadísticas del Analizador VertiPaq— se ocultan automáticamente cuando trabajas con un archivo de modelo (por ejemplo, un archivo `.bim` o una carpeta `.tmdl`) que no está conectado a Analysis Services o Power BI. El asistente seguirá escribiendo Consultas DAX por ti, pero el botón **Ejecutar** en los artefactos de Consulta DAX estará deshabilitado hasta que se establezca una conexión. Las estadísticas del Analizador VertiPaq siguen estando disponibles si se cargaron previamente desde un archivo `.vpax`.

## Conversaciones

El Asistente de IA admite varias conversaciones simultáneas. Cada conversación mantiene su propio historial de mensajes y contexto.

- Las conversaciones persisten entre sesiones y se almacenan localmente en `%LocalAppData%\TabularEditor3\AI\Conversations\`
- Los títulos se generan automáticamente después del primer intercambio. Puedes cambiar manualmente el nombre de las conversaciones
- **Compactación automática**: Cuando la conversación se acerca al límite de la ventana de contexto (~80 %), los mensajes más antiguos se resumen automáticamente para liberar espacio. Se archiva una instantánea de toda la conversación antes de la compactación

## Artefactos

Cuando el Asistente de IA genera código, crea **artefactos** que se abren directamente en ventanas del editor:

- **C# Scripts**: Se abren en un nuevo editor de scripts de C# con resaltado de sintaxis y soporte para la compilación y la ejecución
- **Consultas DAX**: Se abren en un nuevo editor de consultas DAX con resaltado de sintaxis y soporte para la ejecución

Los artefactos se muestran en tiempo real a medida que la IA los genera. Los artefactos de C# Script incluyen un análisis de seguridad que marca código potencialmente inseguro (por ejemplo, acceso al sistema de archivos u operaciones de red).

![Asistente de IA: generar C# Script](~/content/assets/images/ai-assistant/ai-assistant-generate-c-sharp-script.png)

Cuando ejecutas un C# Script desde el chat, el cuadro de diálogo **Vista previa del script** muestra una comparación lado a lado de todos los cambios en los metadatos del modelo realizados por el script. Puedes aceptar los cambios o revertirlos. Consulta [Ejecutar scripts con vista previa](xref:csharp-scripts#run-c-scripts-with-preview) para más información.

![Vista previa del script: cambios del modelo](~/content/assets/images/preview-script-changes.png)

## Instrucciones personalizadas

Las instrucciones personalizadas son conjuntos de instrucciones que guían el comportamiento del Asistente de IA en tareas específicas. Se activan automáticamente según la detección de intención o se invocan de forma explícita.

### Instrucciones personalizadas integradas

El Asistente de IA incluye las siguientes instrucciones personalizadas integradas:

| Instrucción personalizada | Se activa con                                      |
| ------------------------- | -------------------------------------------------- |
| Consulta DAX              | DAX, consulta, evaluar, medida                     |
| Modificación del modelo   | Modificar, cambiar, agregar, actualizar, crear     |
| Diseño del modelo         | Diseño, arquitectura, patrón, práctica recomendada |
| Organizar modelo          | Organizar, limpiar, carpeta, renombrar             |
| Optimizar modelo          | Optimizar, rendimiento, lento, velocidad           |
| Macros                    | Macro, automatizar, grabar                         |
| UDFs                      | UDF, función, definida por el usuario              |
| BPA                       | BPA, práctica recomendada, regla, infracción       |

Las instrucciones personalizadas se muestran como indicadores encima de las respuestas del asistente y señalan qué instrucciones influyeron en ellas. Puedes activar o desactivar esta visualización en **Preferencias > Asistente de IA > Preferencias > Mostrar indicador de instrucciones personalizadas**.

### Invocar una instrucción personalizada

Escribe `/` para explorar las instrucciones personalizadas disponibles, o escribe el `/instruction-id` completo al principio de tu mensaje para invocar explícitamente una instrucción concreta. Por ejemplo, `/dax-querying` fuerza la instrucción de Consulta DAX independientemente del contenido del mensaje.

### Añade tus propias instrucciones personalizadas

Puedes crear instrucciones personalizadas colocando archivos `.md` en `%LocalAppData%\TabularEditor3\AI\CustomInstructions\`. Cada archivo requiere un bloque de frontmatter en YAML que defina los metadatos de la instrucción:

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

Your instruction content goes here. This is the text that will be
injected into the AI's system prompt when the instruction is activated.
```

| Campo                       | Obligatorio | Predeterminado                                         | Descripción                                                                                                 |
| --------------------------- | ----------- | ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| `id`                        | No          | Nombre de archivo sin `.md`                            | Identificador único; también se usa como `/id` para la invocación explícita                                 |
| `name`                      | No          | `id` con inicial mayúscula                             | Nombre para mostrar en el autocompletado                                                                    |
| `description`               | No          | -                                                      | Descripción breve que se muestra debajo del nombre                                                          |
| `priority`                  | No          | 100                                                    | Los valores más altos se insertan primero cuando coinciden varias instrucciones personalizadas              |
| `always_inject`             | No          | false                                                  | Si es true, se incluye siempre en el prompt del sistema                                                     |
| `hidden`                    | No          | false                                                  | Si es true, no se muestra en el autocompletado de `/command`                                                |
| `triggers.keywords`         | No          | [] | Palabras que activan la instrucción (sin distinguir entre mayúsculas y minúsculas)       |
| `triggers.patterns`         | No          | [] | Patrones de expresiones regulares para coincidencias complejas                                              |
| `triggers.context_required` | No          | [] | Condiciones que deben cumplirse (p. ej., `model_loaded`) |

Las instrucciones personalizadas cuyo `id` coincida con el de una instrucción integrada sustituirán la versión integrada.

## Consentimiento

El Asistente de IA solicita permiso antes de enviar datos al proveedor de IA. El consentimiento se limita a tipos de datos específicos:

| Categoría de consentimiento | Descripción                                                                         |
| --------------------------- | ----------------------------------------------------------------------------------- |
| Datos de consulta           | Resultados de Consultas DAX y muestras de datos                                     |
| Leer documentos             | Lectura del contenido de documentos abiertos, como scripts DAX y Consultas DAX      |
| Modificar documentos        | Realizar cambios en documentos abiertos                                             |
| Metadatos del modelo        | Esquemas de tablas y columnas, definiciones de medidas y otros metadatos del modelo |
| Editar reglas de BPA        | Crear o modificar reglas de Best Practice Analyzer                                  |
| Leer macros                 | Leyendo definiciones de macros                                                      |

Cuando el Asistente de IA necesita acceder a un tipo de datos por primera vez, aparece un cuadro de diálogo de consentimiento. Puedes elegir la duración de tu consentimiento:

| Opción           | Alcance                                                                                              |
| ---------------- | ---------------------------------------------------------------------------------------------------- |
| Esta vez         | Solo para una única solicitud                                                                        |
| Esta sesión      | Hasta que se reinicie Tabular Editor                                                                 |
| Para este modelo | Se guarda en el archivo de opciones de usuario del modelo (.tmuo) |
| Siempre          | Preferencia global, conservada en todos los modelos y sesiones                                       |

![Cuadro de diálogo de consentimiento del Asistente de IA](~/content/assets/images/ai-assistant/ai-assistant-generate-consent-dialog.png)

### Gestión de consentimientos

Puedes revisar y restablecer tus opciones de consentimiento en **Herramientas > Preferencias > Asistente de IA > Consentimientos de IA**. Cada categoría de consentimiento muestra su estado actual. Haz clic en **Restablecer** para revocar un consentimiento de "Siempre permitido" y devolverlo a "Preguntar cuando sea necesario".

![Configuración de consentimiento del Asistente de IA](~/content/assets/images/ai-assistant/ai-assistant-consent-reset.png)

## Preferencias

Configura las opciones de visualización y comportamiento del Asistente de IA en **Herramientas > Preferencias > Asistente de IA > Preferencias**.

### Visualización del chat

| Preferencia                                               | Predeterminado | Descripción                                                                            |
| --------------------------------------------------------- | -------------- | -------------------------------------------------------------------------------------- |
| Mostrar el indicador de contexto de selección             | true           | Mostrar en el chat el objeto del modelo seleccionado                                   |
| Mostrar indicador de instrucciones personalizadas         | true           | Mostrar indicadores de instrucciones personalizadas sobre las respuestas del asistente |
| Mostrar indicador de búsqueda en la base de conocimientos | true           | Mostrar el progreso al buscar en la base de conocimientos                              |

### Compactación del contexto

| Preferencia                         | Predeterminado | Descripción                                                                       |
| ----------------------------------- | -------------- | --------------------------------------------------------------------------------- |
| Compactación automática             | true           | Resumir automáticamente los mensajes antiguos al acercarse al límite del contexto |
| Umbral de compactación automática % | 80             | Porcentaje de uso de tokens que activa la compactación automática                 |

### Base de conocimientos

| Preferencia                                                             | Predeterminado | Descripción                                                                                           |
| ----------------------------------------------------------------------- | -------------- | ----------------------------------------------------------------------------------------------------- |
| Comprobar si hay actualizaciones de la base de conocimientos al iniciar | true           | Comprobar automáticamente si hay actualizaciones de la base de conocimiento al iniciar Tabular Editor |

### C# Script

| Preferencia             | Predeterminado | Descripción                                                                                                   |
| ----------------------- | -------------- | ------------------------------------------------------------------------------------------------------------- |
| Vista previa de cambios | true           | Mostrar el cuadro de diálogo de vista previa de cambios al ejecutar C# Scripts generados por IA desde el chat |

![Preferencias del Asistente de IA](~/content/assets/images/ai-assistant/ai-assistant-preferences.png)

## Uso de tokens

Cada mensaje que envías al Asistente de IA consume tokens de entrada. El coste en tokens de un solo mensaje depende del contexto que se incluya:

- **Prompt del sistema e instrucciones personalizadas**: Se envían con cada mensaje. Normalmente, entre 5.000 y 15.000 tokens, según las instrucciones personalizadas que estén activas.
- **Metadatos del modelo**: Cuando el asistente necesita comprender tu modelo, recupera metadatos mediante llamadas a herramientas. Para mantenerse dentro de los límites de frecuencia del proveedor en modelos grandes, el asistente usa un enfoque de revelación progresiva: primero obtiene un resumen ligero (nombres de tablas y medidas, relaciones); después busca los objetos relevantes por nombre, descripción o expresión DAX; y solo profundiza en los detalles completos de las tablas u objetos concretos que requiera la pregunta. Los resultados de las herramientas que, de otro modo, serían muy grandes se truncan con indicaciones sobre cómo el asistente puede recuperar los datos restantes.

### Contador de tokens

El contador de tokens, en la esquina inferior derecha del área de entrada del chat, muestra el uso acumulado de tokens de la conversación actual, incluidos los tokens de entrada de los intercambios con herramientas. Pasa el cursor sobre el contador para ver un desglose:

- **Entrada** — tokens de entrada a precio completo de la conversación, con una sublínea que muestra cuántos de ellos proceden de la caché de prompts del proveedor
- **Escritura en caché** — tokens escritos en la caché de prompts (depende del proveedor)
- **Salida** — tokens generados por el modelo
- **Presión de contexto** — porcentaje de la ventana de contexto que está en uso actualmente; también se visualiza en la barra deslizante junto al contador

### Reducir el uso de tokens

Selecciona objetos específicos en el **Explorador TOM** antes de hacer tu pregunta. Cuando se seleccionan objetos, el asistente acota su contexto a esos objetos en lugar de recuperar los metadatos de todo el modelo. Esta es la forma más eficaz de reducir tanto el uso de tokens como el costo de la API.

Otras formas de reducir el uso de tokens:

- Haz preguntas concretas sobre tablas, medidas o columnas específicas en lugar de preguntas generales sobre todo el modelo. Un prompt impreciso como _"Establece carpetas de visualización en todas las medidas"_ obliga al asistente a recuperar metadatos de todo el modelo. Un prompt específico como _"Establecer carpetas de visualización en las medidas que he seleccionado"_ limita el contexto a la selección actual y utiliza muchos menos tokens
- Inicia nuevas conversaciones al cambiar de tema para evitar acumular historiales de conversación largos
- Usa un modelo más pequeño o menos costoso para preguntas exploratorias

## Limitaciones

- Requiere una clave de API proporcionada por el usuario. No se incluye una clave de API integrada
- Las respuestas de la IA dependen del modelo seleccionado y de las capacidades del proveedor
- La ventana de contexto máxima es de 200.000 tokens
- El Asistente de IA no sustituye el conocimiento de DAX ni los fundamentos del diseño de modelos semánticos
- La calidad de las respuestas varía según el proveedor y el modelo seleccionado
- El Asistente de IA no puede conectarse a archivos o servicios externos ni buscar en la web
- El Asistente de IA no puede añadirse ni actuar como un servidor MCP
- El Asistente de IA no puede conectarse a un modelo diferente desde el chat. Usa la interfaz de usuario de Tabular Editor para cambiar las conexiones del modelo
- El Asistente de IA no puede gestionar las preferencias

## Deshabilitar el Asistente de IA

El Asistente de IA es un componente opcional. Mientras la característica esté en versión preliminar pública, se excluirá de forma predeterminada durante la instalación, pero los usuarios pueden optar por incluirla. Puedes modificar una instalación existente de Tabular Editor 3 para incluir o excluir el componente Asistente de IA volviendo a ejecutar el instalador de Tabular Editor 3. Si usas la versión portátil de Tabular Editor 3, puedes quitar el componente del Asistente de IA borrando el archivo `TabularEditor3.AI.dll` del directorio de instalación.

> [!NOTE]
> Independientemente de si el componente del Asistente de IA esté instalado o no, un administrador del sistema puede deshabilitar toda la funcionalidad de IA en Tabular Editor 3 mediante la [directiva `DisableAi`](xref:policies).
