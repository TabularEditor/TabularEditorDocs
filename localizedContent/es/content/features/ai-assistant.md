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

Hay una segunda forma de acceder que no requiere ninguna clave. A partir de la versión 3.27.0, Tabular Editor 3 puede actuar como servidor MCP, así que un agente al que ya estés suscrito, como Claude Code, GitHub Copilot, el modo de agente de VS Code, Codex o Cursor, puede trabajar en el modelo que tengas abierto con las mismas herramientas y los mismos permisos que el chat. Consulta @mcp-server. Ambos comparten un único registro de permisos, así que, uses el que uses, solo tienes que definir los límites una vez.

> [!NOTE]
> El Asistente de IA está en vista previa pública a partir de Tabular Editor 3.26.0. Agradecemos tus comentarios sobre la experiencia mientras seguimos mejorándola.

![El panel del Asistente de IA al abrirse por primera vez, con el saludo del asistente indicando lo que puede hacer —responder preguntas, consultar el modelo, escribir y ejecutar C# Scripts, cambiar el modelo— y lo que no, encima de un cuadro de mensajes vacío](~/content/assets/images/ai-assistant/ai-assistant-panel-first-open.png)

## Primeros pasos

1. Abre **Herramientas > Preferencias > Funciones de IA > Asistente de IA**
2. Selecciona tu proveedor de IA (en una instalación limpia, el valor predeterminado es **Ninguno (IA deshabilitada)**) y luego introduce tu clave de API
3. Abre el panel del Asistente de IA desde **Vista > Asistente de IA**
4. Escribe mensajes y pulsa **Enter** para iniciar una conversación

El modelo que está usando el asistente se muestra en la barra de estado situada justo encima del cuadro de mensajes. Consulta [Elegir un modelo](#choosing-a-model) para cambiarlo sin salir del chat.

> [!TIP]
> Usa nuestra [demo interactiva del Asistente de IA](https://demos.tabulareditor.com/psl/of150vcy?) para ver cómo configurarlo y usarlo.

> [!NOTE]
> Las claves de API se almacenan cifradas en tu equipo local.

## Proveedores compatibles

Configura tu proveedor de IA en **Herramientas > Preferencias > Funciones de IA > Asistente de IA > Proveedor de IA**. Selecciona un proveedor en la lista desplegable (el valor predeterminado es **Ninguno (IA deshabilitada)** hasta que configures uno), introduce tu clave de API y, si lo deseas, reemplaza el modelo predeterminado.

Deja en blanco el campo del modelo para usar el modelo predeterminado del proveedor. En el caso de OpenAI y Anthropic, los valores predeterminados aparecen en la tabla siguiente; Azure OpenAI y el proveedor Personalizado no tienen valores predeterminados, por lo que en esos dos casos siempre hace falta uno.

| Proveedor                                                | Modelo predeterminado                                            | Configuración necesaria                                                                |
| -------------------------------------------------------- | ---------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| OpenAI                                                   | gpt-5.5                                          | Clave de API. URL base, ID de organización e ID de proyecto opcionales |
| Anthropic                                                | claude-sonnet-4-6                                                | Clave de API. URL base opcional                                        |
| Azure OpenAI                                             | Ninguno. Se requiere un nombre de implementación | Clave de API, URL del punto de conexión y nombre de la implementación                  |
| Personalizado (compatible con OpenAI) | Ninguno. Se requiere un nombre de modelo         | Clave de API y URL personalizada del punto de conexión                                 |

![La página de preferencias del Proveedor de IA con la lista desplegable Elegir proveedor abierta en Ninguno (IA deshabilitada), OpenAI, Anthropic, Azure OpenAI y Personalizado (compatible con OpenAI), y debajo un campo de URL y otro de clave de API](~/content/assets/images/ai-assistant/ai-assistant-provider-preferences.png)

### Elegir un modelo

El modelo activo se muestra en la barra de estado situada encima del cuadro de mensajes, junto a la barra de uso del contexto. Haz clic en él para abrir un selector con los modelos disponibles actualmente para el proveedor configurado; el que elijas se aplicará a todas las solicitudes posteriores, sin cuadro de diálogo y sin necesidad de reiniciar. La última entrada, **Preferencias...**, abre **Herramientas > Preferencias > Funciones de IA > Asistente de IA** para cualquier ajuste que no aparezca en la lista.

![El selector de modelos abierto encima del cuadro de mensajes, con claude-sonnet-5, claude-fable-5-1, claude-fable-5, claude-opus-5, claude-haiku-4-5, claude-opus-4-8 y el claude-sonnet-4-6 activo en negrita, con Preferencias... debajo de un separador](~/content/assets/images/ai-assistant/ui-model-picker.png)

Cuando no hay ninguna lista disponible (por ejemplo, con un nombre de implementación del proveedor Personalizado o de Azure OpenAI, o en un equipo donde nunca se haya recuperado la lista de modelos), el nombre del modelo es un enlace normal a esas mismas preferencias en lugar de un selector.

> [!NOTE]
> El indicador permanece oculto hasta que se hayan configurado un proveedor, una clave de API y un modelo.

### OpenAI

Selecciona **OpenAI** como proveedor e introduce tu clave de API. Opcionalmente, puedes especificar un ID de organización y un ID de proyecto si tu cuenta de OpenAI los usa. El modelo predeterminado es **gpt-5.5**, pero puedes cambiarlo por cualquier modelo disponible en tu cuenta.

![La página de preferencias del proveedor de IA con OpenAI seleccionado, una clave de API enmascarada, los campos ID de la organización e ID del proyecto vacíos, y el nombre del modelo](~/content/assets/images/ai-assistant/ai-assistant-openai-config.png)

### Anthropic

Selecciona **Anthropic** como proveedor e introduce tu clave de API. El modelo predeterminado es **claude-sonnet-4-6**. Puedes cambiar el nombre del modelo a cualquier modelo de Anthropic disponible en tu cuenta.

![La página de preferencias del Asistente de IA con Anthropic seleccionado como proveedor, la URL base https://api.anthropic.com, una clave de API enmascarada y claude-sonnet-4-6 como nombre del modelo](~/content/assets/images/ai-assistant/ai-assistant-anthropic-config.png)

> [!IMPORTANT]
> Anthropic aplica límites de velocidad de tokens de entrada por minuto (ITPM) en función del nivel de tu cuenta. Una nueva clave de API empieza en el Nivel 1 con 30.000 ITPM para Claude Sonnet 4.x. Una sola solicitud a un modelo grande puede superar este límite. Compra 40 USD o más en créditos de API para alcanzar el Nivel 2 (450.000 ITPM). Consulta la [documentación de límites de velocidad de Anthropic](https://docs.anthropic.com/en/api/rate-limits) para ver todos los detalles de los niveles.

### Azure OpenAI

Selecciona **Azure OpenAI** como proveedor y configura tres campos:

- **Clave de API**: la clave de acceso de tu recurso de Azure OpenAI
- **Punto de conexión del servicio**: la URL del punto de conexión de tu recurso, por ejemplo `https://your-resource.openai.azure.com`. Usa la URL del recurso, no el alias `privatelink`; el certificado SSL se emite para `*.openai.azure.com` y, si te conectas directamente a `*.privatelink.openai.azure.com`, fallará la validación del certificado
- **Despliegue**: el **nombre del despliegue**, no el nombre del modelo subyacente ni el del recurso

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

Puedes ejecutar el Asistente de IA con un LLM autoalojado mediante el proveedor Personalizado. Esto mantiene todos los datos dentro de tu propia infraestructura, ya sea un modelo que se ejecuta en tu equipo local o un LLM alojado de forma centralizada dentro de la red de tu organización. En cualquier caso, no se envía ningún dato a un proveedor de nube de terceros.

Varias herramientas pueden alojar modelos con una API compatible con OpenAI:

- [Ollama](https://ollama.com): CLI ligera para descargar y ejecutar modelos localmente
- [LM Studio](https://lmstudio.ai): aplicación de escritorio con interfaz gráfica para administrar y ejecutar modelos locales
- [LocalAI](https://localai.io): alternativa autoalojada e impulsada por la comunidad, con amplio soporte para modelos

Estas herramientas pueden ejecutarse en la estación de trabajo de un desarrollador para uso individual o implementarse en un servidor compartido dentro de tu organización para ofrecer a tu equipo un punto de conexión de LLM gestionado de forma centralizada.

#### Ejemplo: Ollama

1. [Descarga e instala Ollama](https://ollama.com/download)
2. Descarga un modelo, por ejemplo: `ollama pull llama3.1`
3. Inicia el servidor de Ollama (se ejecuta automáticamente tras la instalación y, de forma predeterminada, en el puerto 11434)
4. En Tabular Editor, ve a **Herramientas > Preferencias > Funciones de IA > Asistente de IA > Proveedor de IA**
5. Configura **Elegir proveedor** como **Personalizado (compatible con OpenAI)**
6. Establece **Punto de conexión del servicio** en `http://localhost:11434/v1`
7. Establece **Nombre del modelo** con el modelo que descargaste (p. ej., `llama3.1`)
8. El campo **Clave de API** puede establecerse en cualquier valor no vacío (por ejemplo, `ollama`). Ollama no requiere autenticación, pero el campo no puede dejarse en blanco

#### Ejemplo: LM Studio

1. [Descargar LM Studio](https://lmstudio.ai/download)
2. Descarga un modelo. Ya sea desde la página de búsqueda de modelos del panel izquierdo o mediante la CLI. Por ejemplo: `lms get lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF`
3. Inicia el servidor de LM Studio. Ya sea desde la página para desarrolladores del panel izquierdo o mediante la CLI. por ejemplo `lms server start`
   Nota: tendrás que configurarlo para que use el modo compatible con OpenAI. Además, puede que tengas que cambiar el tamaño de contexto predeterminado para que sea superior a 100000 tokens.
4. En Tabular Editor, ve a **Herramientas > Preferencias > Funciones de IA > Asistente de IA > Proveedor de IA**
5. Configura **Elegir proveedor** como **Personalizado (compatible con OpenAI)**
6. Establece **Punto de conexión del servicio** en `http://localhost:1234/v1`
7. Establece **Nombre del modelo** con el modelo que descargaste (p. ej., `lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF`)
8. El campo **Clave de API** puede establecerse en cualquier valor no vacío (por ejemplo, `lms`). LM Studio no requiere autenticación, pero el campo no puede dejarse en blanco

> [!NOTE]
> La calidad de las respuestas con modelos locales depende del tamaño del modelo y de tu hardware. Los modelos más grandes suelen producir mejores resultados, pero requieren más RAM y una GPU capaz. Las capacidades de llamada a herramientas del Asistente de IA requieren un modelo que admita llamadas a funciones en el formato compatible con OpenAI.

> [!TIP]
> We recommend a model with a _minimum_ of 30 billion parameters but ideally at least 100 billion parameters. Por ejemplo, el modelo Qwen3.5-122B-A10B funcionó bien en nuestras pruebas internas.

### Uso de Microsoft Foundry

[Microsoft Foundry](https://ai.azure.com) (antes llamado Azure AI Foundry) te permite desplegar modelos de OpenAI y Anthropic en tu entorno de Azure. Puedes acceder a estos modelos mediante el proveedor **OpenAI** o **Anthropic** en Tabular Editor, no mediante el proveedor **Azure OpenAI**, que es para recursos clásicos de Azure OpenAI.

> [!IMPORTANT]
> No uses el proveedor **Azure OpenAI** para modelos de Microsoft Foundry. El proveedor **Azure OpenAI** solo es compatible con recursos clásicos de Azure OpenAI.

#### Modelos de OpenAI en Microsoft Foundry

Para usar un modelo de OpenAI (como GPT-4o o GPT-5.4-mini) desplegado en Microsoft Foundry:

1. En Tabular Editor, ve a **Herramientas > Preferencias > Funciones de IA > Asistente de IA > Proveedor de IA**
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

1. En Tabular Editor, ve a **Herramientas > Preferencias > Funciones de IA > Asistente de IA > Proveedor de IA**
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
- **Generación de C# Scripts**: Crea C# Scripts para realizar modificaciones en el modelo. Según tu configuración, el asistente abre el script en una nueva ventana del editor para que lo ejecutes tú, o realiza el cambio por sí mismo. Consulta [Permitir que el asistente cambie tu modelo](#letting-the-assistant-change-your-model). Los cambios en los metadatos del modelo se pueden deshacer con **Ctrl+Z**
- **Best Practice Analyzer**: Ejecutar el análisis de BPA, ver infracciones de las reglas y crear o modificar reglas de BPA
- **Analizador VertiPaq**: Consultar estadísticas de uso de memoria y cardinalidad de columnas
- **Acceso a documentos**: Leer y modificar documentos abiertos, como scripts DAX y Consultas DAX
- **Búsqueda en la base de conocimientos**: Buscar en la documentación integrada de Tabular Editor para encontrar respuestas
- **Navegación por la interfaz de usuario**: Generar enlaces de acción `te3://` que abren cuadros de diálogo y funcionalidades específicas de Tabular Editor

Un agente conectado a través del [servidor MCP](xref:mcp-server) dispone de las mismas capacidades, con una excepción: la navegación por la interfaz solo está disponible en el chat. Ambas interfaces pueden cambiar tu modelo ejecutando un C# Script, y ambas lo hacen como un único paso que se puede deshacer. La diferencia está en cómo se te presenta el cambio y en cómo se concede el permiso. Consulta [Lo que comparte el servidor MCP y lo que no](#what-the-mcp-server-shares-and-what-it-does-not).

> [!NOTE]
> Las herramientas que requieren una conexión activa a la base de datos, como la ejecución de consultas DAX y las estadísticas del Analizador VertiPaq, se ocultan automáticamente al trabajar con un archivo de modelo (por ejemplo, un archivo `.bim` o una carpeta `.tmdl`) que no está conectado a Analysis Services ni a Power BI. El asistente sigue escribiendo consultas DAX por ti, pero el botón **Ejecutar** en los artefactos de consulta DAX está deshabilitado hasta que se establezca una conexión. Las estadísticas del Analizador VertiPaq siguen estando disponibles si se cargaron previamente desde un archivo `.vpax`.

## Permitir que el asistente cambie tu modelo

De forma predeterminada, el asistente escribe un **C# Script** y lo abre en una ventana del editor para que lo leas y lo ejecutes. A partir de Tabular Editor 3.27.0, el asistente puede realizar el cambio por sí mismo.

Marca la casilla **Permitir que el asistente de IA ejecute C# Scripts directamente** en **Herramientas > Preferencias > Funciones de IA > Asistente de IA**. La preferencia permanece desactivada hasta que la actives, y la casilla no estará disponible hasta que **Metadatos del modelo** esté configurado en **Escritura** en **Herramientas > Preferencias > Funciones de IA > Permisos**.

### Qué ocurre cuando el asistente ejecuta un script

- **Primero ves el cambio.** Con **Vista previa de cambios** activada, que es la opción predeterminada, aparece el [cuadro de diálogo de vista previa](xref:csharp-scripts#run-c-scripts-with-preview) antes de que se aplique nada. Al elegir **Cancelar**, el modelo vuelve a su estado anterior y el asistente entiende que rechazaste el cambio, por lo que te pregunta qué hacer de otro modo en lugar de intentar lo mismo otra vez. Con la preferencia desactivada, el cambio se aplica sin mostrar ningún cuadro de diálogo.
- **Un solo paso de deshacer.** Todo lo que hizo el script se agrupa en una única entrada llamada _C# Script (AI Assistant)_. Con un solo **Ctrl+Z**, el modelo vuelve a su estado anterior.
- **Todo o nada.** Si un script falla a mitad del proceso, el modelo queda intacto y el asistente muestra el error en un **Report** en lugar de dejarte con una edición a medias.
- **Solo las operaciones del modelo se ejecutan así.** Un script que intente acceder a archivos, a la red o a un ensamblado externo nunca se ejecuta por ti. Aparece como un artefacto de script con la insignia **Inseguro** y **Ejecutar** deshabilitado, y el asistente te indica qué usó.

Si pides un script en lugar del cambio, seguirás obteniendo un script. _Escríbeme un script que cambie el nombre de todas las medidas a tipo frase_ abre un documento de script para que lo ejecutes tú mismo, independientemente de lo que indique esta configuración.

Los administradores pueden impedirlo por completo con la [política](xref:policies) `DisableCSharpScripts`, que también evita que el asistente escriba scripts para que los ejecutes tú.

También pueden permitir el uso de scripts, pero limitarlos al modelo, con la política `BlockUnsafeScripts`. Con ella, un script que intente acceder a archivos, a la red o a un ensamblado externo se rechaza directamente en lugar de entregártelo para que lo revises, venga de donde venga. Consulta [Directivas de administrador](xref:csharp-scripts#administrator-policies).

## Conversaciones

El Asistente de IA admite varias conversaciones simultáneas. Cada conversación mantiene su propio historial de mensajes y contexto.

- Las conversaciones se conservan entre sesiones y se almacenan localmente en `%LocalAppData%\TabularEditor3\AI\Conversations\`
- Los títulos se generan automáticamente tras el primer intercambio. Puedes cambiar el nombre de las conversaciones manualmente
- **Compactación automática**: cuando la conversación se acerca al límite de la ventana de contexto, los mensajes más antiguos se resumen automáticamente para liberar espacio. Se archiva una instantánea de la conversación completa antes de la compactación. El umbral se configura en [Compactación de contexto](#context-compaction) y es un porcentaje de la propia ventana de contexto del modelo

### Eliminar una conversación

**Eliminar conversación** se encuentra en el extremo izquierdo de la barra de herramientas de AI Assistant, junto a **Nueva conversación**. Primero pide confirmación.

La conversación y su historial se eliminan del disco y no se pueden recuperar. Para ocultar el panel de AI Assistant en lugar de eliminar nada, usa el botón de cerrar de la barra de título del panel o **View > AI Assistant**.

## Artefactos

Cuando el Asistente de IA genera código, crea **artefactos** que se abren directamente en ventanas del editor:

- **C# Scripts**: Se abren en un nuevo editor de C# Script con resaltado de sintaxis, compilación y compatibilidad con la ejecución
- **Consultas DAX**: Se abren en un nuevo editor de consultas DAX con resaltado de sintaxis y compatibilidad con la ejecución

Los artefactos se transmiten en tiempo real a medida que la IA los genera. Los artefactos de C# Script incluyen un análisis de seguridad que señala código potencialmente inseguro (p. ej., acceso al sistema de archivos u operaciones de red).

![El panel de AI Assistant muestra un artefacto de C# Script generado con un botón Execute y la explicación del asistente sobre lo que hace el script, además de la advertencia sobre la distinción entre mayúsculas y minúsculas](~/content/assets/images/ai-assistant/ai-assistant-generate-c-sharp-script.png)

Cuando ejecutas un C# Script desde el chat, el cuadro de diálogo **Vista previa del script** muestra una comparación en paralelo de todos los cambios de metadatos del modelo realizados por el script. Puedes aceptar los cambios o revertirlos. Consulta [Ejecutar scripts con vista previa](xref:csharp-scripts#run-c-scripts-with-preview) para obtener más información.

![El cuadro de diálogo Vista previa del script: cambios en el modelo, con el modelo antes y después uno junto al otro, con la cadena de formato de la medida Internet Total Freight modificada y con una descripción y una carpeta de visualización añadidas, cada una marcada respecto de su valor original](~/content/assets/images/preview-script-changes.png)

## Instrucciones personalizadas

Las instrucciones personalizadas son conjuntos de instrucciones que guían el comportamiento del Asistente de IA para tareas específicas. Al asistente se le proporciona una lista de todas las instrucciones disponibles y solo carga el texto completo de las que considera relevantes para tu solicitud. Una vez que se ha cargado una instrucción, sigue en vigor durante el resto de la conversación.

> [!IMPORTANT]
> Ahora el asistente solo lee la `description` al decidir si debe usar una instrucción, así que mantenla precisa y específica.

### Instrucciones personalizadas integradas

El Asistente de IA incluye las siguientes instrucciones personalizadas integradas:

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

Las instrucciones personalizadas se muestran como indicadores encima de las respuestas del asistente, lo que indica qué instrucciones influyeron en la respuesta. Puedes activar o desactivar esta visualización en **Herramientas > Preferencias > Funciones de IA > Asistente de IA > Preferencias > Mostrar indicador de instrucciones personalizadas**.

### Invocar una instrucción personalizada

Escribe `/` para explorar las instrucciones personalizadas disponibles, o escribe el `/instruction-id` completo al inicio de tu mensaje para invocar explícitamente una instrucción concreta. Por ejemplo, `/dax-querying` fuerza la instrucción de Consulta DAX independientemente del contenido de tu mensaje. Si no escribes nada después de `/id`, al asistente simplemente se le pide que use esa instrucción.

La invocación explícita sigue siendo útil cuando quieres asegurarte de que se aplique la instrucción. Una instrucción invocada explícitamente sigue en vigor durante el resto de la conversación, igual que una cargada automáticamente.

### Añade tus propias instrucciones personalizadas

Puedes crear instrucciones personalizadas colocando archivos `.md` en `%LocalAppData%\TabularEditor3\AI\CustomInstructions\`. La carpeta se crea la primera vez que se ejecuta el Asistente de IA, con un archivo `example.md` que puedes usar como base. Usa **Abrir carpeta de instrucciones personalizadas** en la barra de herramientas del Asistente de IA para acceder a ella.

Cada archivo puede comenzar con un frontmatter en YAML que define los metadatos de la instrucción. Nada de esto es obligatorio:

```yaml
---
id: my-custom-instruction
name: My Custom Instruction
description: A brief description shown in the autocomplete popup.
priority: 100
always_inject: false
hidden: false
---

Aquí va el contenido de tu instrucción. Este es el texto que se
inyectará en el prompt del sistema de la IA cuando se active la instrucción.
```

| Campo           | Obligatorio | Predeterminado                     | Descripción                                                                                                                             |
| --------------- | ----------- | ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `id`            | No          | Nombre de archivo sin `.md`        | Identificador único; también se usa como `/id` para la invocación explícita                                                             |
| `name`          | No          | `id` con mayúsculas iniciales      | Nombre para mostrar en el autocompletado                                                                                                |
| `description`   | No          | Si no está definido, se usa `name` | Indica qué cubre la instrucción y cuándo se aplica                                                                                      |
| `priority`      | No          | 100                                | Los valores más altos se inyectan primero cuando hay varias instrucciones personalizadas en vigor                                       |
| `always_inject` | No          | false                              | Si es `true`, siempre se incluye en el prompt del sistema. Una instrucción así no se ofrece en el autocompletado de `/` |
| `hidden`        | No          | false                              | Si es `true`, no se muestra en el autocompletado de `/command`                                                                          |

Las instrucciones personalizadas con un `id` que coincida con el de una instrucción integrada sustituirán la versión integrada.

Notas sobre cómo se leen los archivos:

- El frontmatter debe comenzar con `---` en la primera línea del archivo y terminar con una línea `---`. Si no es así, o si no se puede interpretar el YAML, todo el archivo se trata como contenido de la instrucción y se aplican todos los valores predeterminados anteriores
- Las claves que no aparecen en la tabla anterior se ignoran. Esto es lo que hace que una sección `triggers:` que haya quedado sea inofensiva
- `{{version}}` en cualquier parte del cuerpo se reemplaza por la versión del componente de IA de Tabular Editor
- Solo se leen los archivos `.md` que están directamente en la carpeta; no se buscan subcarpetas

### Instrucciones personalizadas de tu organización

Un administrador puede publicar una carpeta de instrucciones personalizadas para todos mediante la [directiva](xref:policies) `AiCustomInstructionsPath`. Puede ser un recurso compartido de red de solo lectura. Esas instrucciones se cargan para cada usuario, además de las integradas, y se usan exactamente igual que cualquier otra: se ofrecen en el autocompletado al escribir `/`, se eligen por su descripción y se invocan con `/id`.

Si el mismo `id` existe en más de un lugar, la prioridad es esta:

1. La carpeta de tu organización
2. Tu propia carpeta
3. Las instrucciones integradas

Así, una instrucción de la organización tiene prioridad tanto sobre una integrada como sobre tu propio archivo con el mismo nombre. Otra directiva, `DisableUserCustomInstructions`, hace que Tabular Editor ignore por completo las instrucciones de tu propia carpeta y deshabilita **Open Custom Instructions Folder**; las instrucciones integradas y las de la organización se siguen cargando.

Ambas directivas requieren Tabular Editor 3 Edición Enterprise.

## Permisos y consentimiento

A lo que el Asistente de IA puede acceder lo determinan _cinco recursos_, cada uno con un nivel de acceso. Los mismos cinco permisos rigen el [servidor MCP](xref:mcp-server), así que solo hay un lugar para consultarlo y otro para cambiar de opinión.

| Recurso                    | Qué abarca                                                                                                                                                                             | Niveles                          | Predeterminado |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- | -------------- |
| **Metadatos del modelo**   | Nombres de tablas, columnas y medidas, expresiones, descripciones y similares. El acceso de lectura también incluye las estadísticas del Analizador VertiPaq           | Denegar / Leer / Escribir        | **Leer**       |
| **Datos del modelo**       | Valores de datos de tu modelo, como los resultados de consultas DAX. Requiere una conexión en directo                                                                  | Sin acceso / Lectura             | **Sin acceso** |
| **Best Practice Analyzer** | Lectura enumera las reglas y ejecuta el análisis; Escritura permite agregar o modificar reglas                                                                                         | Sin acceso / Lectura / Escritura | **Lectura**    |
| **Documentos**             | Tus editores de documentos abiertos: C# Scripts y consultas DAX. Lectura permite ver su contenido; Escritura es necesaria para crearlos o modificarlos | Sin acceso / Lectura / Escritura | **Escritura**  |
| **macros**                 | Tu biblioteca de macros. Lectura enumera las macros y permite leerlas; Escritura se reserva para futuras herramientas de edición de macros                             | Sin acceso / Lectura / Escritura | **Escritura**  |

Un permiso de **Escritura** incluye **Lectura**, así que no hace falta conceder ambos. Los **datos del modelo** son de solo lectura por naturaleza (el asistente puede consultar tus datos, pero no tiene forma de escribir valores de vuelta), por lo que solo ofrece las opciones Sin acceso y Lectura.

> [!NOTE]
> Los **datos del modelo** son el único recurso denegado de forma predeterminada. Los metadatos describen tu modelo; los datos _son_ el contenido de tu modelo, así que enviarlos a un proveedor de IA es una decisión que conviene tomar de forma deliberada, en lugar de dejarla en manos de una configuración predeterminada.

Hay tres permisos que conviene examinar más de cerca:

- **Metadatos del modelo > Escritura** permite al asistente cambiar tu modelo. Por sí solo, eso significa escribir un C# Script y dártelo para que lo ejecutes. También es el permiso que hace posible la [ejecución directa](#letting-the-assistant-change-your-model), pero el asistente solo ejecuta scripts por su cuenta cuando lo has activado por separado. En cualquier caso, solo se ejecutan los scripts que, mediante análisis estático, se determina que son seguros, y nunca se ejecuta por ti un script que salga del modelo y acceda al sistema de archivos o a la red.
- **Best Practice Analyzer > Leer** permite al asistente ejecutar el análisis, pero para hacerlo también necesita **Metadatos del modelo > Leer**, ya que el análisis lee el modelo.
- El permiso **Datos del modelo > Leer** no es suficiente por sí solo para ejecutar una consulta DAX: para eso también se necesita **Metadatos del modelo > Leer**, porque una consulta puede leer metadatos mediante las funciones `INFO`, las DMV y los nombres de columna de su propio resultado.

### Configurar las concesiones de permisos

Abre **Herramientas > Preferencias > Funciones de IA > Permisos**. Cada recurso tiene una lista desplegable con sus niveles disponibles.

![Preferencias de Funciones de IA > Permisos, una lista desplegable por recurso con su valor predeterminado](~/content/assets/images/pref-ai-permissions.png)

No hay un nivel independiente de «pregúntame». **Denegar** equivale a «pregúntame»: en el chat, un recurso al que no hayas dado permiso genera una tarjeta de permiso en el momento en que se necesita. En MCP, donde no hay nadie a quien preguntar, las herramientas de un recurso denegado no están disponibles.

> [!NOTE]
> Si usaste el Asistente de IA antes de la versión 3.27.0, verás menos solicitudes. Metadatos del modelo, Documentos y macros ahora empiezan en Leer o en un nivel superior, así que el chat ya no te los pide. Solo los resultados de consultas DAX y las ediciones de reglas de Best Practice Analyzer siguen generando una tarjeta de forma predeterminada. Establece un recurso en **Denegar** para que vuelva a mostrarse su solicitud.

> [!NOTE]
> En la Edición Enterprise, los administradores de TI pueden establecer directivas que determinan estos permisos. Consulta @policies.

### Tarjetas de permiso en el chat

Cuando el asistente necesita un recurso que tus permisos actuales no cubren, aparece en la conversación una tarjeta de **Permiso necesario** que indica lo que quiere hacer; por ejemplo, «La IA quiere acceder a los metadatos de tu modelo semántico» o la consulta DAX que propone ejecutar.

![Una tarjeta de Permiso necesario en el chat, que muestra la consulta DAX que el asistente quiere ejecutar, con los botones Permitir, Permitir para la sesión, Permitir para este modelo, Permitir siempre y Denegar](~/content/assets/images/ai-assistant/ai-assistant-generate-consent-dialog.png)

| Botón                         | Qué hace                                                                                                                                                                                                                                                                 |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Permitir**                  | Solo en esta interacción. El asistente puede repetir la misma solicitud mientras termina lo que le pediste, y después no se conserva nada                                                                                                                |
| **Permitir para la sesión**   | Hasta que se reinicie Tabular Editor. Se mantiene en memoria y nunca se escribe en disco                                                                                                                                                                 |
| **Permitir para este modelo** | Se registra en el archivo de [opciones de usuario](xref:user-options) del modelo, por lo que se aplica la próxima vez que abras este modelo. Se ofrece solo para **Metadatos del modelo** y **Datos del modelo**, y solo mientras haya un modelo cargado |
| **Permitir siempre**          | Aumenta la concesión permanente en la página de Permisos para todos los modelos y todas las sesiones                                                                                                                                                                     |
| **Denegar**                   | Rechaza esta solicitud. El asistente continúa sin ese acceso y vuelve a preguntar la próxima vez                                                                                                                                                         |

**Permitir siempre** solo eleva un permiso; nunca lo reduce: permitir la lectura no puede limitar un permiso de escritura que ya estuviera concedido.

No tienes que responder a la tarjeta en absoluto. Consulta [Detener un turno mientras hay un permiso pendiente](#stopping-a-turn-while-permission-is-pending) más abajo.

### Qué comparte el servidor MCP y qué no

El [servidor MCP](xref:mcp-server) lee los _mismos cinco permisos_, pero no usa el flujo de tarjetas. Un agente que se conecta mediante MCP funciona sin supervisión, así que no hay nadie a quien preguntar:

- Los permisos se _capturan al iniciar el servidor_ y rigen las herramientas disponibles durante toda la vida útil del servidor. Cambiar un permiso mientras el servidor está en ejecución no surte efecto hasta que lo reinicies.
- Solo se leen los permisos _globales_. Un permiso que otorgaste con **Permitir para este modelo** y un permiso de sesión solo se aplican al chat y nunca llegan a un agente MCP.
- Si un recurso se deniega, sus herramientas no se ofrecen al agente en ningún momento; no se ofrecen para luego rechazarse.

### Revocar permisos

Vuelve a establecer el recurso en **Denegar** en la página Permisos. El chat volverá a preguntar la próxima vez que necesite ese recurso; un servidor MCP en ejecución conserva el acceso con el que se inició hasta que lo reinicies.

Reducir un permiso global no elimina un permiso por modelo. Para revocar uno de esos permisos, elimina el archivo `.tmuo` del modelo o la entrada `Permissions` dentro de él. Consulta los detalles en @user-options.

### Registro de auditoría

En la Edición Enterprise de Tabular Editor 3, se mantiene un registro local de lo que hicieron el Asistente de IA y el [servidor MCP](xref:mcp-server): qué permisos se solicitaron y cómo respondiste, qué herramientas se ejecutaron y si cada una se completó correctamente, falló o fue rechazada, y el texto completo de cualquier C# Script que se ejecutó o se te entregó para revisión. Tus indicaciones, las respuestas del asistente y los valores de datos de tu modelo nunca se registran. **Abrir carpeta de auditoría** en **Herramientas > Preferencias > Funciones de IA** te lleva a los archivos.

En la edición Desktop y en la Edición Business, y antes de activar una licencia, no se registra nada, no se crea ninguna carpeta y el botón no se muestra.

Consulta @ai-audit-log para ver qué contiene cada registro, dónde se guardan los archivos y las directivas que los redirigen.

### Detener un turno mientras hay un permiso pendiente

Una tarjeta de **Se requiere permiso** espera una respuesta antes de que el asistente pueda continuar. No tienes que responderla: al pulsar **Detener**, se termina el turno, se quita la tarjeta y la solicitud se considera denegada. El panel vuelve a su estado normal y puedes seguir en la misma conversación con un nuevo mensaje.

## Preferencias

Configura las opciones de visualización y comportamiento del Asistente de IA en **Herramientas > Preferencias > Funciones de IA > Asistente de IA > Preferencias**.

### Visualización del chat

| Preferencia                                               | Predeterminado | Descripción                                                                                    |
| --------------------------------------------------------- | -------------- | ---------------------------------------------------------------------------------------------- |
| Mostrar indicador de contexto de selección                | true           | Muestra el objeto del modelo seleccionado actualmente en el chat                               |
| Mostrar indicador de instrucciones personalizadas         | true           | Muestra los indicadores de instrucciones personalizadas encima de las respuestas del asistente |
| Mostrar indicador de búsqueda en la base de conocimientos | true           | Muestra el progreso al buscar en la base de conocimientos                                      |

### Compactación de contexto

| Preferencia                         | Predeterminado | Descripción                                                                                                                                                                                         |
| ----------------------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Compactación automática             | true           | Resumir automáticamente los mensajes antiguos al acercarse al límite del contexto                                                                                                                   |
| Umbral de compactación automática % | 80             | Porcentaje de la propia ventana de contexto del modelo a partir del cual se activa la compactación automática. Los valores fuera del rango 50-100 no tienen ningún efecto adicional |

### C# Script

| Preferencia                                                     | Predeterminado | Descripción                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| --------------------------------------------------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Permitir que el Asistente de IA ejecute C# Scripts directamente | false          | Permite que el asistente realice por sí mismo los cambios en el modelo en lugar de abrir un script para que lo ejecutes tú. No está disponible hasta que **Metadatos del modelo** se establezca en **Escritura** en **Permisos**, y no está disponible en absoluto cuando se aplica la [política](xref:policies) `DisableCSharpScripts`. Consulta [Dejar que el asistente cambie tu modelo](#dejar-que-el-asistente-cambie-tu-modelo) |
| Previsualizar cambios                                           | true           | Mostrar el cuadro de diálogo de vista previa de cambios al ejecutar C# Scripts generados por IA desde el chat                                                                                                                                                                                                                                                                                                                                                         |

Hay otras dos opciones en la propia página **Funciones de IA**, encima de **Asistente de IA**, porque también se aplican al servidor MCP: _Buscar actualizaciones de la base de conocimiento al iniciar_ y el botón **Abrir carpeta de auditoría**. Consulta @preferencias.

![La página de preferencias del Asistente de IA, con los tres indicadores de visualización del chat, la compactación automática y su umbral, y las dos opciones de C# Script: Permitir que el Asistente de IA ejecute C# scripts directamente, desmarcada, y Vista previa de cambios, marcada](~/content/assets/images/ai-assistant/ai-assistant-preferences.png)

## Uso de tokens

Cada mensaje al Asistente de IA consume tokens de entrada. El coste en tokens de un solo mensaje depende de qué contexto se incluya:

- **Prompt del sistema e instrucciones personalizadas**: Se envían con cada mensaje. Normalmente, entre 5.000 y 15.000 tokens, según las instrucciones personalizadas que estén activas.
- **Metadatos del modelo**: cuando el asistente necesita entender tu modelo, recupera los metadatos mediante llamadas a herramientas. Para mantenerse dentro de los límites de frecuencia del proveedor en modelos grandes, el asistente usa un enfoque de divulgación progresiva. Es decir, primero obtiene un resumen breve (nombres de tablas y medidas, relaciones); después busca objetos relevantes por nombre, descripción o expresión DAX y solo entra en los detalles completos de las tablas u objetos concretos que requiera la pregunta. Los resultados de las herramientas que, de otro modo, serían muy grandes se truncan e incluyen indicaciones sobre cómo el asistente puede recuperar los datos restantes.

### Contador de tokens

El contador de tokens está en la barra de estado sobre el cuadro de mensaje, junto al [indicador del modelo activo](#choosing-a-model). La barra muestra _usados_ / _total_ en miles de tokens y se colorea en verde, ámbar o rojo a medida que se llena el contexto. Un `±` delante de la cifra significa que aún no hay un recuento exacto disponible.

Pasa el cursor sobre ella para ver un desglose en tres secciones etiquetadas:

| Sección                                              | Qué abarca                                                                                                                                                          |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Último turno**                                     | El coste del intercambio más reciente: entrada nueva, tokens servidos desde la caché de prompts del proveedor, tokens escritos en la caché y salida |
| **Esta conversación (facturada)** | Las mismas cuatro cifras acumuladas en todas las solicitudes de la conversación, incluidos los intercambios con herramientas                                        |
| **Contexto**                                         | Los tokens que hay actualmente en la ventana de contexto, en comparación con el tamaño real de la ventana                                                           |

Una línea dice, por ejemplo, `37,588 input + 131,744 cached · write 37,558 · output 2,866`. Los elementos de caché se omiten en los proveedores que no admiten la caché de prompts, y una sección se omite por completo cuando no tiene ningún Report que mostrar.

> [!TIP]
> Separar el último turno del total de la conversación es lo que te permite saber si una breve pregunta de seguimiento fue realmente costosa. Es normal ver una cifra alta en **Esta conversación (facturada)** junto a una cifra baja en **Último turno** en una conversación larga.

### Ventana de contexto

La barra de uso del contexto, el punto de compactación automática y la longitud máxima de una sola respuesta se rigen por la _ventana de contexto real del modelo en uso_, no por una cifra fija. Un modelo con una ventana de un millón de tokens se evalúa con respecto a un millón de tokens.

Cuando no se conoce la ventana real del modelo (por ejemplo, un nombre de implementación de Azure OpenAI o una implementación personalizada, o un equipo en el que nunca se ha recuperado el catálogo de modelos), Tabular Editor recurre a 200.000 tokens.

### Reducir el uso de tokens

Selecciona objetos específicos en el **Explorador TOM** antes de hacer tu pregunta. Cuando hay objetos seleccionados, el asistente limita su contexto a esos objetos en lugar de obtener los metadatos de todo el modelo. Esta es la forma más eficaz de reducir tanto el uso de tokens como el coste de la API.

Otras formas de reducir el uso de tokens:

- Haz preguntas concretas sobre tablas, medidas o columnas específicas en lugar de preguntas generales sobre todo el modelo. Una instrucción imprecisa como _"Establece carpetas de visualización en todas las medidas"_ obliga al asistente a recuperar metadatos de todo el modelo. Una instrucción específica como _"Establece carpetas de visualización en las medidas que he seleccionado"_ limita el contexto a la selección actual y usa muchos menos tokens
- Inicia nuevas conversaciones al cambiar de tema para evitar acumular historiales de conversación extensos
- Usa un modelo más pequeño o menos costoso para preguntas exploratorias

## Limitaciones

- Requiere una clave de API proporcionada por el usuario. No se incluye ninguna clave de API integrada
- Las respuestas de la IA dependen del modelo seleccionado y de las capacidades del proveedor
- La ventana de contexto utilizable es la propia del modelo seleccionado; cuando Tabular Editor no puede determinarla, se asume un límite de 200.000 tokens
- El Asistente de IA no sustituye la comprensión de los fundamentos de DAX y del diseño de modelos semánticos
- La calidad de las respuestas varía según el proveedor y el modelo seleccionado
- El Asistente de IA no puede conectarse a archivos o servicios externos ni buscar en la web
- El Asistente de IA no puede conectarse a servidores MCP externos para ampliar sus propias herramientas. Esto se refiere solo al chat: Tabular Editor 3 actúa como servidor MCP, por lo que tu propio agente puede trabajar con el modelo abierto. Consulta @mcp-server
- El Asistente de IA no puede conectarse a otro modelo desde el chat. Usa la interfaz de usuario de Tabular Editor para cambiar las conexiones del modelo
- El Asistente de IA no puede administrar las preferencias

## Desactivar el Asistente de IA

El Asistente de IA es un componente opcional que viene instalado de forma predeterminada a partir de Tabular Editor 3.27.0. Puedes modificar una instalación existente de Tabular Editor 3 para incluir o excluir el componente del Asistente de IA volviendo a ejecutar el instalador de Tabular Editor 3. Si usas la versión portable de Tabular Editor 3, puedes quitar el componente del Asistente de IA eliminando el archivo `TabularEditor3.AI.dll` del directorio de instalación.

El Asistente de IA y el servidor MCP se incluyen en el mismo componente, por lo que excluirlo o eliminar `TabularEditor3.AI.dll` elimina ambos. Para desactivar el chat y mantener el servidor MCP, deja el componente instalado y usa la directiva `DisableAiChat`.

> [!NOTE]
> Independientemente de si el componente del Asistente de IA está instalado o no, un administrador del sistema puede desactivar toda la funcionalidad de IA en Tabular Editor 3, incluido el servidor MCP, especificando la [directiva `DisableAi`](xref:policies). `DisableAiChat` desactiva solo el chat y `DisableMcpServer` desactiva solo el servidor MCP. Consulta @policies.
