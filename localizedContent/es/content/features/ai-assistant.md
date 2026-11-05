---
uid: ai-assistant
title: Asistente de IA
author: Morten Lønskov
updated: 2026-10-14
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

El asistente de IA es un panel de chat para el desarrollo de modelos semánticos. Explora los metadatos de su modelo, escribe y ejecuta consultas DAX, genera scripts de C#, explica y corrige los errores de su modelo y de los documentos abiertos, realiza comprobaciones de Best Practice Analyzer, consulta las estadísticas del Analizador VertiPaq y busca en la base de conocimientos de Tabular Editor. La [configuración de permisos](#permissions-and-consent) controla lo que envía a su proveedor de IA. El Asistente de IA se ha sometido a pruebas de penetración independientes; consulte el [Centro de cumplimiento de Tabular Editor](https://trust.tabulareditor.com).

El Asistente de IA utiliza un modelo de «trae tu propia clave», en el que tú proporcionas una clave de API de uno de los proveedores compatibles y el asistente se ejecuta directamente con la API de ese proveedor.

También puedes usar tu propio agente a través del [servidor MCP](xref:mcp-server), sin clave de API. Un agente como Claude Code, GitHub Copilot, el modo agente de VS Code, Codex o Cursor funciona en el modelo abierto con las mismas herramientas y configuraciones de permisos que el chat, excepto por los permisos de sesión y por modelo, que solo se aplican al chat. Consulta [Diferencias entre el servidor MCP y el asistente de IA](#mcp-server-and-ai-assistant-differences).



![El panel del Asistente de IA al abrirse por primera vez, con el saludo del asistente que enumera lo que puede hacer (responder a preguntas, consultar el modelo, escribir y ejecutar scripts de C#, cambiar el modelo) y lo que no puede, encima de un cuadro de mensaje vacío](~/content/assets/images/ai-assistant/ai-assistant-panel-first-open.png)

## Primeros pasos

1. Abra **Herramientas > Preferencias > Funciones de IA > Asistente de IA > Proveedor de IA**
2. Seleccione su proveedor de IA (en una instalación nueva, el valor predeterminado es **Ninguno [IA desactivada]**) y, a continuación, introduzca su clave API.
3. Abra el panel del Asistente de IA desde **Vista > Asistente de IA**
4. Escriba un mensaje y pulse **Intro** para iniciar una conversación.

> [!TIP]
> La [demostración interactiva del asistente de IA](https://demos.tabulareditor.com/psl/of150vcy?) explica cómo configurarlo y usarlo.

> [!NOTE]
> Las claves API se almacenan cifradas en su equipo local.

## Proveedores compatibles

Configure su proveedor de IA en **Herramientas > Preferencias > Funciones de IA > Asistente de IA > Proveedor de IA**. Seleccione un proveedor en el menú desplegable (el valor predeterminado es **Ninguno (IA desactivada)** hasta que configure uno), introduzca su clave de API y, opcionalmente, anule el modelo predeterminado.

Deja el campo del modelo en blanco para usar el modelo predeterminado del proveedor. OpenAI y Anthropic tienen valores predeterminados; Azure OpenAI y el proveedor personalizado siempre necesitan un valor.

| Proveedor | Modelo predeterminado | Configuración necesaria |
| -- | -- | -- |
| OpenAI | gpt-5.5 | Clave de API. URL base, ID de organización e ID de proyecto opcionales |
| Anthropic | claude-sonnet-4-6 | Clave de API. URL base opcional |
| Azure OpenAI | Ninguno. Se requiere un nombre de implementación | Clave de API, URL del endpoint y nombre de implementación |
| Personalizado (compatible con OpenAI) | Ninguno. Se requiere un nombre de modelo | Clave de API y URL de endpoint personalizada |

![La página de preferencias del proveedor de IA con el menú desplegable «Elegir proveedor» abierto en «Ninguno» (IA desactivada), «OpenAI», «Anthropic», «Azure OpenAI» y «Personalizado» (compatible con OpenAI), y un campo para la URL y la clave de API debajo](~/content/assets/images/ai-assistant/ai-assistant-provider-preferences.png)

### Elegir un modelo

El modelo activo se muestra en la barra de estado situada encima del cuadro de mensajes, junto a la barra de uso del contexto. Haz clic en él para abrir un selector que muestra los modelos disponibles para el proveedor configurado; el modelo que elijas se aplicará a partir de la siguiente solicitud. La última entrada, **Preferencias...**, abre **Herramientas > Preferencias > Funciones de IA > Asistente de IA > Proveedor de IA** para cualquier elemento que no esté en la lista. En el caso de los proveedores Azure OpenAI y Personalizado, o antes de que se haya recuperado la lista de modelos, el nombre del modelo es un enlace que abre dichas preferencias.

![El selector de modelos abierto encima del cuadro de mensajes, con una lista que incluye claude-sonnet-5, claude-fable-5-1, claude-fable-5, claude-opus-5, claude-haiku-4-5, claude-opus-4-8 y el modelo activo claude-sonnet-4-6 en negrita, con «Preferencias...» debajo de un separador](~/content/assets/images/ai-assistant/ui-model-picker.png)

> [!NOTE]
> El indicador del modelo permanece oculto hasta que se hayan configurado un proveedor, una clave API y un modelo.

### OpenAI

Seleccione **OpenAI** como proveedor e introduzca su clave de API. Si su cuenta de OpenAI utiliza un ID de organización o un ID de proyecto, introdúzcalos también. El nombre del modelo admite cualquier modelo disponible en su cuenta.

![La página de preferencias del proveedor de IA de una versión anterior, con OpenAI seleccionado, una clave de API oculta, los campos «ID de organización» e «ID de proyecto» vacíos y «gpt-4o» como nombre del modelo](~/content/assets/images/ai-assistant/ai-assistant-openai-config.png)

### Anthropic

Seleccione **Anthropic** como proveedor e introduzca su clave de API. El nombre del modelo admite cualquier modelo de Anthropic disponible en su cuenta.

![La página de preferencias del proveedor de IA con Anthropic seleccionado como proveedor, la URL base https://api.anthropic.com, una clave API oculta y claude-sonnet-4-6 como nombre del modelo](~/content/assets/images/ai-assistant/ai-assistant-anthropic-config.png)

> [!IMPORTANT]
> Anthropic aplica límites de tasa de tokens de entrada por minuto (ITPM) en función del nivel de tu cuenta. Una nueva clave de API comienza en el nivel 1 con 30 000 ITPM para Claude Sonnet 4.x. Una sola solicitud a un modelo grande puede superar este límite. Compra 40 $ o más en créditos de API para alcanzar el nivel 2 (450 000 ITPM). Consulta la [documentación sobre los límites de tasa de Anthropic](https://docs.anthropic.com/en/api/rate-limits) para obtener todos los detalles de los niveles.

### Azure OpenAI

Seleccione **Azure OpenAI** como proveedor y configure estos campos:

- **Clave de API**: la clave de acceso a tu recurso de Azure OpenAI
- **Punto de conexión del servicio**: la URL del recurso, por ejemplo, `https://your-resource.openai.azure.com`. El certificado SSL se emite para `*.openai.azure.com`, por lo que una dirección `*.privatelink.openai.azure.com` no supera la validación del certificado.
- **Implementación**: el nombre de la implementación que se muestra en la columna **Nombre** de **Implementaciones**

Azure OpenAI requiere el nombre de la implementación en cada llamada a la API. El nombre se establece cuando se crea la implementación y, a menudo, coincide con el modelo al que sirve, por ejemplo, `gpt-4o`, pero puede ser diferente. Si introduce el nombre del recurso o un nombre de modelo que no existe como implementación, la solicitud fallará.

Encuentra el nombre de la implementación en el [portal de Azure AI Foundry](https://ai.azure.com):

1. Inicie sesión y seleccione su recurso de Azure OpenAI.
2. Abra **Implementaciones** (o **Modelos + puntos de conexión** si el recurso se ha actualizado a Foundry).
3. Copie el valor de la columna **Nombre**.

Si una implementación creada antes de que su organización adoptara Azure AI Foundry no aparece en el portal, enumere las implementaciones con la CLI de Azure:

```bash
az cognitiveservices account deployment list --name "<resource-name>" --resource-group "<resource-group>" --output table
```

Consulte [Crear e implementar un recurso de Azure OpenAI](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/create-resource#deploy-a-model).

Para errores 403, fallos de SSL o respuestas «DeploymentNotFound», consulte @azure-openai-connection-errors. Para los modelos implementados en Microsoft Foundry, consulta [Uso de Microsoft Foundry](#using-microsoft-foundry).

### Personalizado (compatible con OpenAI)

El proveedor personalizado se conecta a cualquier LLM que exponga un punto de conexión de API compatible con OpenAI, como un modelo en tu propio equipo o uno alojado en la red de tu organización. Introduzca su clave de API y la URL del punto de conexión. Con un modelo autoalojado, todos los datos permanecen dentro de su propia infraestructura y no se envía nada a un proveedor de nube externo. Consulte [Uso de un LLM local u organizativo](#using-a-local-or-organizational-llm).

## Uso de un LLM local o de la organización

Puedes ejecutar el Asistente de IA con un LLM autoalojado utilizando el proveedor personalizado. De este modo, todos los datos permanecen dentro de su propia infraestructura, ya sea un modelo que se ejecute en su equipo local o un LLM alojado de forma centralizada en la red de su organización. En cualquier caso, no se envían datos a un proveedor de nube externo.
Estas herramientas alojan modelos con una API compatible con OpenAI, en la estación de trabajo de un desarrollador o en un servidor compartido que sirve como endpoint para el equipo:

- [Ollama](https://ollama.com): CLI ligera para descargar y ejecutar modelos localmente
- [LM Studio](https://lmstudio.ai): aplicación de escritorio con una interfaz gráfica para gestionar y ejecutar modelos locales
- [LocalAI](https://localai.io): alternativa autoalojada e impulsada por la comunidad con amplia compatibilidad con modelos

### Ejemplo: Ollama

1. [Descarga e instala Ollama](https://ollama.com/download)
2. Extraiga un modelo, por ejemplo, `ollama pull llama3.1`.
3. Inicie el servidor de Ollama. Se inicia automáticamente después de la instalación, de forma predeterminada en el puerto 11434.
4. En Tabular Editor, vaya a **Herramientas > Preferencias > Funciones de IA > Asistente de IA > Proveedor de IA**
5. Establezca **Elegir proveedor** en **Personalizado (compatible con OpenAI)**
6. Establezca **Punto de conexión del servicio** en `http://localhost:11434/v1`
7. Establezca **Nombre del modelo** como el modelo que ha extraído, por ejemplo, `llama3.1`.
8. Establezca **Clave de API** en cualquier valor que no esté vacío, por ejemplo, `ollama`. Ollama no requiere autenticación, pero el campo no puede estar en blanco.

### Ejemplo: LM Studio

1. [Descarga e instala LM Studio](https://lmstudio.ai/download)
2. Descargue un modelo desde la página de búsqueda de modelos del panel izquierdo o con la CLI; por ejemplo, `lms get lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF`
3. Inicie el servidor de LM Studio desde la página de desarrolladores del panel izquierdo o con `lms server start`. Active el modo compatible con OpenAI. Si el tamaño del contexto es inferior a 100 000 tokens, auméntalo por encima de 100 000.
4. En Tabular Editor, vaya a **Herramientas > Preferencias > Funciones de IA > Asistente de IA > Proveedor de IA**
5. Establezca **Elegir proveedor** en **Personalizado (compatible con OpenAI)**.
6. Establezca **Punto de conexión del servicio** en `http://localhost:1234/v1`
7. Establezca **Nombre del modelo** como el modelo que descargó, por ejemplo, `lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF`
8. Establezca **Clave de API** en cualquier valor que no esté vacío, por ejemplo, `lms`. LM Studio no requiere autenticación, pero el campo no puede estar en blanco.


> [!NOTE]
> La calidad de las respuestas con modelos locales depende del tamaño del modelo y de tu hardware. Los modelos más grandes dan mejores resultados y necesitan más RAM y una GPU potente. La llamada a herramientas del asistente de IA requiere un modelo que admita la llamada a funciones en el formato compatible con OpenAI.

> [!TIP]
> Utilice un modelo con al menos 30 000 millones de parámetros y, preferiblemente, 100 000 millones o más. Qwen3.5-122B-A10B obtuvo buenos resultados en las pruebas internas.

## Uso de Microsoft Foundry

[Microsoft Foundry](https://ai.azure.com) (anteriormente Azure AI Foundry) implementa modelos de OpenAI y Anthropic en tu entorno de Azure. Conéctate a estos modelos con el proveedor **OpenAI** o **Anthropic** en Tabular Editor.

> [!IMPORTANT]
> No utilice el proveedor **Azure OpenAI** para los modelos de Microsoft Foundry. Solo funciona con los recursos clásicos de Azure OpenAI que usan el parámetro de consulta `api-version`.

### Modelos de OpenAI en Microsoft Foundry

Configura un modelo de OpenAI implementado en Microsoft Foundry, como GPT-4o o GPT-5.4-mini:

1. En Tabular Editor, vaya a **Herramientas > Preferencias > Funciones de IA > Asistente de IA > Proveedor de IA**
2. Establezca **Elegir proveedor** en **OpenAI**.
3. Establezca la **URL base** en el punto de conexión de su recurso de Foundry con `/openai/v1` añadido, en uno de estos formatos:
   - `https://your-resource.services.ai.azure.com/openai/v1`
   - `https://your-resource.openai.azure.com/openai/v1`
4. Introduzca su **clave de API** de Foundry.
5. Establece **Nombre del modelo** como el nombre de tu implementación, por ejemplo, `gpt-5.4-mini`.

> [!NOTE]
> El portal de Microsoft Foundry no muestra la URL base. Muestra un **URI de destino** con la ruta completa de la API, por ejemplo, `https://your-resource.services.ai.azure.com/api/projects/YourProject/openai/v1/responses`. Para la URL base, use solo `https://your-resource.services.ai.azure.com/openai/v1`.

### Modelos de Anthropic en Microsoft Foundry

Para un modelo de Anthropic implementado en Microsoft Foundry, como Claude Sonnet 4.6:

1. En Tabular Editor, vaya a **Herramientas > Preferencias > Funciones de IA > Asistente de IA > Proveedor de IA**
2. Establezca **Elegir proveedor** en **Anthropic**.
3. Establezca la **URL base** como el punto de conexión de su recurso de Foundry con `/anthropic` añadido, por ejemplo, `https://your-resource.services.ai.azure.com/anthropic`
4. Introduzca su **clave de API** de Foundry.
5. Establezca **Nombre del modelo** como el identificador del modelo, por ejemplo, `claude-sonnet-4-6`

> [!NOTE]
> El portal muestra un **URI de destino** como `https://your-resource.services.ai.azure.com/anthropic/v1/messages`. Para la URL base, usa la parte hasta e incluyendo `/anthropic`.

## Funcionalidades

Dentro de tus [concesiones de permisos](#permissions-and-consent), el Asistente de IA trabaja con el contexto de tu modelo:

- **Exploración del modelo**: consulta los metadatos del modelo, incluidas las tablas, las columnas, las medidas, las relaciones y sus propiedades.
- **Escritura de consultas DAX**: genera consultas DAX, las ejecuta en su modelo conectado y devuelve los conjuntos de resultados en el chat.
- **Generación de scripts de C#**: crea scripts de C# para los cambios en el modelo. Dependiendo de su configuración, el asistente abre el script en una ventana del editor para que lo ejecute usted o lo ejecuta él mismo; consulte [Permitir que el asistente cambie su modelo](#letting-the-assistant-change-your-model)
- **Best Practice Analyzer**: ejecuta análisis BPA, enumera las infracciones de las reglas y crea o modifica reglas BPA.
- **Analizador VertiPaq**: consulta las estadísticas de uso de la memoria y la cardinalidad de las columnas.
- **Errores del modelo**: enumera los errores, las advertencias y los mensajes de Analysis Services del modelo, los mismos que muestra la [vista Mensajes](xref:messages-view), con las causas raíz en primer lugar. Se informa al asistente cuando cambian los errores del modelo.
- **Acceso a documentos**: lee y modifica consultas DAX abiertas, scripts de C# y scripts DAX, y lee los errores y advertencias de todos los documentos abiertos, incluidas las Pivot Grids. El documento activo forma parte del contexto del asistente, por lo que puede preguntar «¿Por qué veo este error en esta consulta?». No puede leer ni cambiar la estructura de un Pivot Grid.
- **Búsqueda en la base de conocimientos**: busca en la documentación integrada de Tabular Editor.
- **Navegación por la interfaz de usuario**: genera enlaces de acción `te3://` que abren cuadros de diálogo y funciones específicos de Tabular Editor.

Un agente conectado a través del [servidor MCP](xref:mcp-server) tiene las mismas capacidades, excepto la navegación por la interfaz de usuario. Ambos cambian su modelo ejecutando un script de C# como un único paso que se puede deshacer. Difieren en la forma de revisar los cambios y conceder permisos; consulta [Diferencias entre el servidor MCP y el asistente de IA](#mcp-server-and-ai-assistant-differences).

> [!NOTE]
> Cuando el modelo se carga desde un archivo, como un archivo `.bim` o una carpeta TMDL, y no está conectado a Analysis Services o Power BI, las herramientas que necesitan una conexión permanecen ocultas, incluidas la ejecución de consultas DAX y las estadísticas de VertiPaq Analyzer. El asistente sigue escribiendo consultas DAX, pero la opción **Ejecutar** en los artefactos de consultas DAX está deshabilitada hasta que se conecte. Las estadísticas del Analizador VertiPaq cargadas desde un archivo `.vpax` siguen estando disponibles.

## Permitir que el asistente cambie tu modelo

De forma predeterminada, el asistente escribe un script de C# y lo abre en una ventana del editor, donde puedes leerlo y ejecutarlo. También puede ejecutar el script por sí mismo si selecciona **Permitir que el asistente de IA ejecute scripts de C# directamente** en **Herramientas > Preferencias > Funciones de IA > Asistente de IA > Preferencias**.

El ajuste está desactivado de forma predeterminada y no está disponible hasta que **Metadatos del modelo** se establezca en **Lectura/Escritura** en **Herramientas > Preferencias > Funciones de IA > Permisos**.

### ¿Qué sucede cuando el asistente ejecuta un script?

- Si la opción **Vista previa de los cambios** está activada (valor predeterminado), el [cuadro de diálogo de vista previa](xref:csharp-scripts#run-c-scripts-with-preview) aparece antes de que se apliquen los cambios. **Cancelar** los revierte y comunica el rechazo al asistente. Si la opción **Vista previa de los cambios** está desactivada, los cambios se aplican sin que aparezca ningún cuadro de diálogo.
- Los cambios del script constituyen una sola entrada de deshacer, **Script de C# (Asistente de IA)**. El foco permanece en el cuadro de chat, donde **Ctrl+Z** no deshace los cambios en el modelo. Para deshacer todo el script, haga clic en el Explorador TOM y pulse **Ctrl+Z**, o seleccione **Deshacer script C# (Asistente de IA)** en el menú **Editar**.
- Si el script falla a mitad de camino, el modelo no se modifica y el asistente informa del error.
- Si el script se ejecuta correctamente e introduce o resuelve errores DAX, el asistente recibe una lista de esos errores, agrupados por causa raíz.
- Un script que accede a archivos, a la red o a ensamblados externos no se ejecuta. Se abre como un artefacto de script con una insignia de **Inseguro** y la opción **Ejecutar** desactivada, y la respuesta del asistente indica lo que ha utilizado el script.

Si solicita un script, por ejemplo, «Escríbeme un script que cambie el nombre de todas las medidas a mayúscula inicial», el asistente lo abrirá como un documento de script que usted mismo ejecutará, incluso con esta configuración activada.

La [política](xref:policies) `DisableCSharpScripts` se aplica en todas las ediciones y desactiva tanto la ejecución directa como los scripts que el asistente le proporciona para que los ejecute.

La política `BlockUnsafeScripts` requiere la Edición Enterprise y se aplica a todas las secuencias de comandos de Tabular Editor, incluidas las secuencias de comandos que se ejecutan a través del [servidor MCP](xref:mcp-server). Cuando está activada, el asistente aún puede escribir un script que acceda a archivos, a la red o a ensamblados externos, pero el script no se ejecuta y no se abre ningún artefacto para su revisión. Consulte [Políticas del administrador](xref:csharp-scripts#administrator-policies).

## Conversaciones

El asistente de IA admite varias conversaciones simultáneas, cada una con su propio historial de mensajes y contexto.

- Las conversaciones se mantienen entre sesiones y se almacenan localmente en `%LocalAppData%\TabularEditor3\AI\Conversations\`
- Los títulos se generan automáticamente después del primer intercambio, y puedes cambiar el nombre de una conversación.
- **Compactación automática**: cuando una conversación se acerca al límite de la ventana de contexto, los mensajes más antiguos se resumen para liberar espacio, después de archivar una instantánea de la conversación completa. El umbral es un porcentaje de la propia ventana de contexto del modelo, establecido en [Compactación del contexto](#context-compaction).

### Eliminar una conversación

**Eliminar conversación** se encuentra en el extremo izquierdo de la barra de herramientas del Asistente de IA, junto a **Nueva conversación**. Después de confirmar el mensaje, la conversación y su historial se eliminan del disco y no se pueden recuperar. El botón de cerrar de la barra de título del panel, o **Ver > Asistente de IA**, oculta el panel sin eliminar nada.

## Artefactos

El código que genera el asistente de IA se abre como un *artefacto* en una ventana del editor:

- **Scripts de C#**: un editor de scripts de C# con resaltado de sintaxis, compilación y ejecución
- **Consultas DAX**: un editor de consultas DAX con resaltado de sintaxis y ejecución

Los artefactos van llegando a medida que la IA los genera, y los artefactos de C# Script incluyen un análisis de seguridad que señala el código no seguro, como el acceso al sistema de archivos o las operaciones de red.

![El panel del Asistente de IA muestra un artefacto de C# Script generado con un botón «Ejecutar» y la explicación del asistente sobre lo que hace el script y la advertencia sobre la distinción entre mayúsculas y minúsculas que lo acompaña](~/content/assets/images/ai-assistant/ai-assistant-generate-c-sharp-script.png)

Si la opción **Vista previa de los cambios** está activada, al ejecutar un C# Script desde el chat se abrirá el cuadro de diálogo **Vista previa del script** con una comparación en paralelo de todos los cambios en los metadatos del modelo realizados por el script, donde podrás aceptar o revertir los cambios. Consulte [Ejecución de scripts con vista previa](xref:csharp-scripts#run-c-scripts-with-preview).

![El cuadro de diálogo Vista previa del script - Cambios en el modelo, el modelo antes y después uno al lado del otro, con la cadena de formato de la medida «Internet Total Freight» modificada y una descripción y una carpeta de visualización añadidas, cada una marcada en comparación con su versión original](~/content/assets/images/preview-script-changes.png)

## Instrucciones personalizadas

Las *instrucciones personalizadas* son conjuntos de instrucciones que guían al asistente de IA en tareas específicas. El asistente recibe una lista de todas las instrucciones disponibles con su `description` y carga el texto completo solo de aquellas que sean relevantes para tu solicitud, así que procura que las descripciones sean precisas y específicas. Una instrucción cargada permanece vigente durante el resto de la conversación.

### Instrucciones personalizadas integradas

El asistente de IA incluye estas instrucciones personalizadas:

| Instrucción personalizada | Invocar con | Abarca |
| -- | -- | -- |
| Consultas DAX | `/dax-querying` | Escritura y ejecución de consultas DAX: calificación de columnas y medidas, verificación de valores de filtro, validación y actualización de consultas |
| Modificación del modelo | `/model-modification` | Scripts de C# que crean o cambian objetos del modelo: patrones de la API TOMWrapper, orden de ejecución, actualizaciones idempotentes, reglas de nomenclatura |
| Diseño de modelos semánticos | `/model-design` | Esquema estrella, relaciones y filtrado cruzado, tablas de fechas, medidas frente a columnas calculadas, grupos de cálculo, nomenclatura |
| Organización del modelo semántico | `/organize-model` | Auditoría y ordenación de los metadatos del modelo: convenciones de nomenclatura, grupos de tablas, carpetas de visualización, columnas ocultas, cadenas de formato, descripciones |
| Optimización del tamaño del modelo semántico | `/optimize-model` | Reducción de la memoria y el tamaño del modelo: medición de VertiPaq, eliminación de columnas, ajuste de tipos de datos, cambios estructurales, límites de SKU |
| Macros | `/macros` | Macros de C# reutilizables para la ventana Macros: contextos de selección, reglas de código genérico |
| Funciones definidas por el usuario de DAX | `/udf` | Escritura de UDF de DAX: sintaxis, modos de parámetros `VAL`/`EXPR`, sugerencias de tipo, espacios de nombres, DaxLib |
| Best Practice Analyzer | `/bpa` | Revisión de infracciones y redacción de reglas personalizadas como expresiones LINQ Dynamic |

Con la opción **Mostrar indicador de instrucciones personalizadas** seleccionada en **Herramientas > Preferencias > Funciones de IA > Asistente de IA > Preferencias**, los indicadores situados encima de cada respuesta muestran qué instrucciones la han influido.

### Invocar una instrucción personalizada

Escriba `/` para ver las instrucciones personalizadas disponibles. Comience su mensaje con el `/id` de una instrucción para cargarla independientemente del contenido del mensaje; por ejemplo, `/dax-querying` carga la instrucción de consulta DAX. Un `/id` sin mensaje carga la instrucción sin realizar una solicitud. Una instrucción cargada explícitamente permanece vigente durante el resto de la conversación, al igual que una que el asistente carga por sí mismo.

### Añadir sus propias instrucciones personalizadas

Cree una instrucción personalizada colocando un archivo `.md` en `%LocalAppData%\TabularEditor3\AI\CustomInstructions\`. La carpeta se crea la primera vez que se ejecuta el asistente de IA, con un archivo `example.md` en ella para copiarlo. **Abrir carpeta de instrucciones personalizadas** en la barra de herramientas del Asistente de IA la abre.

El encabezado YAML que define los metadatos de la instrucción es opcional:

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

| Campo | Obligatorio | Predeterminado | Descripción |
| -- | -- | -- | -- |
| `id` | No | Nombre de archivo sin `.md` | Identificador único, también utilizado como `/id` para la invocación explícita |
| `name` | No | `id` con mayúscula inicial | Nombre que se muestra en el autocompletado |
| `description` | No | Se recurre a `name` | Indica qué abarca la instrucción y cuándo se aplica |
| `priority` | No | 100 | Los valores más altos se inyectan primero cuando hay varias instrucciones personalizadas activas |
| `always_inject` | No | false | Si es true, se incluye siempre en el «prompt» del sistema. Esta instrucción no se ofrece en el autocompletado `/` |
| `hidden` | No | false | Si es true, no se muestra en el autocompletado de `/command` |

Una instrucción personalizada cuyo `id` coincide con una instrucción integrada anula la versión integrada.

Tabular Editor lee los archivos de la siguiente manera:

- La materia preliminar debe comenzar con `---` en la primera línea del archivo y terminar con una línea `---`. Si no es así, o si no se puede analizar el YAML, todo el archivo se trata como contenido de la instrucción y se aplican todos los valores predeterminados anteriores.
- Las claves que no figuran en la tabla anterior se ignoran. Los archivos de versiones anteriores que aún tienen una sección `triggers:` se cargan sin cambios.
- `{{version}}` en cualquier parte del cuerpo se sustituye por la versión del componente de IA de Tabular Editor.
- Solo se leen los archivos `.md` que se encuentran directamente en la carpeta; no se buscan subcarpetas.

### Instrucciones personalizadas de tu empresa

Un administrador puede publicar una carpeta de instrucciones personalizadas para todos con la [política](xref:policies) `AiCustomInstructionsPath`, y la carpeta puede ser un recurso compartido de red de solo lectura. Esas instrucciones se cargan para todos los usuarios además de las integradas y funcionan como las demás instrucciones: se ofrecen en el autocompletado `/`, se eligen por su descripción y se invocan mediante `/id`.

Cuando el mismo `id` existe en más de un lugar, la prioridad es la siguiente:

1. La carpeta de tu organización
2. Tu propia carpeta
3. Las instrucciones integradas

Una política independiente, `DisableUserCustomInstructions`, hace que Tabular Editor ignore las instrucciones de su propia carpeta y desactive **Abrir carpeta de instrucciones personalizadas**. Las instrucciones integradas y de la organización siguen cargándose. Ambas políticas requieren Tabular Editor 3 Edición Enterprise.

## Permisos y consentimiento

Establece un nivel de acceso para cada recurso para controlar a qué puede acceder el Asistente de IA, y el [servidor MCP](xref:mcp-server) utiliza los mismos ajustes.

| Recurso | Qué abarca | Niveles | Predeterminado |
| -- | -- | -- | -- |
| **Metadatos del modelo** | Nombres de tablas, columnas y medidas, expresiones, descripciones y elementos similares. El permiso de lectura también abarca las estadísticas del Analizador VertiPaq y los mensajes de error y advertencia del modelo | Denegar / Lectura / Escritura | **Lectura** |
| **Datos del modelo** | Valores de datos de tu modelo, como los resultados de las consultas DAX y el texto de los errores devueltos por Analysis Services, que pueden contener valores de datos. Las consultas DAX requieren una conexión en vivo | Denegar / Leer | **Denegar** |
| **Best Practice Analyzer** | Lectura: lee las reglas de las listas y ejecuta el análisis; Escritura: añade o modifica reglas | Denegar / Lectura / Escritura | **Lectura** |
| **Documentos** | Sus documentos abiertos: consultas DAX, scripts de C#, scripts DAX y Pivot Grids. Lectura se refiere a su contenido y a sus errores y advertencias; Escritura es necesaria para crearlos o modificarlos. Los diseños de Pivot Grid no se pueden leer ni modificar | Denegar / Lectura / Escritura | **Escritura** |
| **Macros** | Tu biblioteca de macros. Lectura permite ver las listas y las macros; Escritura está reservado para futuras herramientas de edición de macros | Denegar / Lectura / Escritura | **Escritura** |

**Escritura** (denominada **Lectura/Escritura** en los menús desplegables) incluye Lectura.

> [!NOTE]
> Conceder **Datos del modelo** envía los valores de los datos de tu modelo a tu proveedor de IA.

Algunos permisos dependen de otros:

- **Metadatos del modelo > Escritura** es necesario para la [ejecución directa](#letting-the-assistant-change-your-model), que se activa por separado.
- Para ejecutar Best Practice Analyzer, se necesita **Metadatos del modelo > Lectura**, además de **Best Practice Analyzer > Lectura**.
- Para ejecutar una consulta DAX se necesita **Metadatos del modelo > Leer** además de **Datos del modelo > Leer**. Una consulta puede leer metadatos a través de las funciones `INFO`, las DMV y los nombres de las columnas en su resultado.

### Configuración de las concesiones de permisos

Abra **Herramientas > Preferencias > Funciones de IA > Permisos**, donde cada recurso tiene un menú desplegable con sus niveles disponibles.

![Funciones de IA > Preferencias de permisos, un menú desplegable por recurso con su valor predeterminado](~/content/assets/images/pref-ai-permissions.png)

El chat no tiene un nivel de «solicitud» independiente y muestra una [tarjeta de permisos](#permission-cards-in-the-chat) cuando necesita un recurso configurado como **Denegar**.

> [!NOTE]
> A partir de la versión 3.27.0, **Metadatos del modelo**, **Documentos** y **Macros** tienen como valor predeterminado Lectura o superior, y el chat ya no solicita permisos para ellos. De forma predeterminada, solo los resultados de las consultas DAX y las modificaciones de las reglas del Best Practice Analyzer muestran una tarjeta. Establezca un recurso en **Denegar** para que vuelva a aparecer su aviso.

> [!NOTE]
> En la edición Enterprise, los administradores pueden limitar estos permisos mediante directivas. Consulte @policies.

### Tarjetas de permisos en el chat

Cuando el asistente necesita un recurso que tu concesión permanente no cubre, aparece una tarjeta de **Permiso requerido** en la conversación. La tarjeta indica lo que el asistente quiere hacer, por ejemplo, «La IA quiere acceder a los metadatos de tu modelo semántico», o muestra la consulta DAX que propone ejecutar.

![Una tarjeta de Permiso requerido en el chat, que indica la consulta DAX que el asistente quiere ejecutar, con los botones Permitir, Permitir para la sesión, Permitir para este modelo, Permitir siempre y Denegar](~/content/assets/images/ai-assistant/ai-assistant-generate-consent-dialog.png)

| Botón | Qué hace |
| -- | -- |
| **Permitir** | Se aplica solo a este turno. El asistente puede repetir la misma solicitud mientras termina su tarea, y no se recuerda nada después |
| **Permitir solo para esta sesión** | Se aplica hasta que se reinicie Tabular Editor. El permiso se mantiene en la memoria y nunca se escribe en el disco |
| **Permitir para este modelo** | Se registra en el archivo de [opciones de usuario](xref:user-options) del modelo y se aplica la próxima vez que abra este modelo. Se ofrece solo para **Metadatos del modelo** y **Datos del modelo**, y únicamente mientras haya un modelo cargado |
| **Permitir siempre** | Eleva el nivel de autorización permanente en la página Permisos, para todos los modelos y todas las sesiones |
| **Denegar** | Deniega esta solicitud. El asistente continúa sin ese acceso, y la tarjeta vuelve a aparecer la próxima vez que lo necesite |

**Permitir siempre** nunca reduce un permiso existente; si se permite la lectura de un recurso con permiso de escritura, se mantiene el permiso de escritura.

### Detener un turno mientras el permiso está pendiente

El turno se pausa hasta que responda a una tarjeta de **Permiso requerido**. **Detener** finaliza el turno sin una respuesta, elimina la tarjeta y considera la solicitud como denegada. Envíe un nuevo mensaje para continuar la conversación.

### Diferencias entre el servidor MCP y el asistente de IA

El [servidor MCP](xref:mcp-server) utiliza los mismos cinco permisos, pero no muestra tarjetas de permiso:

- Los permisos se leen cuando se inicia el servidor y se aplican hasta que se detiene, por lo que un permiso modificado solo entra en vigor después de reiniciar el servidor.
- Solo se aplican los permisos globales. Los permisos concedidos con **Permitir para este modelo** o **Permitir para la sesión** solo se aplican al chat.
- Las herramientas de un recurso denegado no aparecen en la lista de herramientas del agente.

### Retirar un permiso

Vuelve a establecer un recurso como **Denegar** en la página Permisos para retirar su concesión. A continuación, el chat mostrará una tarjeta de permisos la próxima vez que necesite ese recurso.

Reducir un permiso global no elimina un permiso por modelo. Elimine el archivo `.tmuo` del modelo, o la entrada `Permissions` que contiene, para retirar los permisos por modelo. Consulte @user-options.

### Registro de auditoría

En la Edición Enterprise, incluidas las licencias de consultoría y de prueba, Tabular Editor escribe un registro local de la actividad del Asistente de IA y del [servidor MCP](xref:mcp-server). Registra:

- qué permisos se solicitaron y cómo respondiste
- qué herramientas se ejecutaron y si cada una tuvo éxito, falló o se bloqueó
- el texto completo de cualquier script de C# que el asistente o un agente de MCP haya ejecutado o enviado para su ejecución, incluidos los scripts que hayan fallado en tiempo de ejecución o hayan sido rechazados.

Tus indicaciones, las respuestas del asistente y los valores de los datos de tu modelo nunca se registran. No se guarda un script que no se pueda compilar, ni tampoco el texto de un script que el asistente escriba en un documento para que lo ejecute usted mismo. **Abrir carpeta de auditoría** en **Herramientas > Preferencias > Funciones de IA** abre la carpeta de registros.

Sin una licencia Enterprise, y antes de que se active una licencia, no se registra nada, no se crea ninguna carpeta y no se muestra el botón. Consulte @ai-audit-log para saber qué contiene cada registro, dónde se almacenan los archivos y qué políticas los redirigen.

## Preferencias

Configure las opciones de visualización y comportamiento del Asistente de IA en **Herramientas > Preferencias > Funciones de IA > Asistente de IA > Preferencias**.

### Visualización del chat

| Preferencia | Valor predeterminado | Descripción |
| -- | -- | -- |
| Mostrar indicador del contexto de la selección | Desactivado | Mostrar el objeto del modelo actualmente seleccionado en el chat |
| Mostrar indicador de instrucciones personalizadas | Desactivado | Mostrar indicadores de instrucciones personalizadas encima de las respuestas del asistente |
| Mostrar indicador de búsqueda en la base de conocimientos | Desactivado | Mostrar el progreso al buscar en la base de conocimientos |

### Compactación del contexto

| Preferencia | Predeterminado | Descripción |
| -- | -- | -- |
| Compresión automática | Activada | Resume automáticamente los mensajes antiguos al acercarse al límite de contexto |
| Umbral de compactación automática % | 80 | Porcentaje de la ventana de contexto propia del modelo en el que se activa la compactación automática. El campo acepta valores de 25 a 100. Los valores inferiores a 50 se consideran 50 y los valores superiores a 90 se consideran 90 |

### Script de C#

| Preferencia | Valor predeterminado | Descripción |
| -- | -- | -- |
| Permitir que el asistente de IA ejecute C# Scripts directamente | Desactivado | Permite que el asistente ejecute sus C# Scripts por sí mismo. Cuando está desactivada, el asistente abre cada script y tú lo ejecutas. No está disponible hasta que **Metadatos del modelo** se establezca en **Lectura/Escritura** en **Permisos**, y no está disponible en absoluto con la [política](xref:policies) `DisableCSharpScripts`. Consulta [Permitir que el asistente cambie tu modelo](#letting-the-assistant-change-your-model) |
| Vista previa de los cambios | Activada | Muestra el cuadro de diálogo de vista previa de los cambios al ejecutar scripts de C# generados por IA desde el chat |

**Buscar actualizaciones de la base de conocimientos al iniciar** y el botón **Abrir carpeta de auditoría** se encuentran en la página **Funciones de IA**, encima de **Asistente de IA**, y ambos también se aplican al servidor MCP. Consulte @preferences.

![La página de preferencias del asistente de IA, con los tres indicadores de visualización del chat desactivados (valor predeterminado), «Compactación automática» seleccionada con un umbral de 80, «Permitir que el asistente de IA ejecute C# Scripts directamente» desactivada y «Vista previa de los cambios» seleccionada](~/content/assets/images/ai-assistant/ai-assistant-preferences.png)

## Uso de tokens

Cada mensaje enviado al asistente de IA consume tokens de entrada. El coste en tokens de un único mensaje depende del contexto que incluya:

- **Aviso del sistema e instrucciones personalizadas**: se envían con cada mensaje; suelen ser de 5000 a 15 000 tokens, en función de qué instrucciones personalizadas estén activas.
- **Metadatos del modelo**: se obtienen mediante llamadas a herramientas, por etapas. El asistente primero obtiene una descripción general ligera (nombres de tablas y medidas, relaciones), luego busca objetos relevantes por nombre, descripción o expresión DAX y recupera los detalles completos solo para las tablas u objetos que requiere la pregunta. Si el resultado de una herramienta es muy grande, se trunca y se ofrecen indicaciones sobre cómo puede el asistente recuperar el resto.

### Contador de tokens

El contador de tokens se encuentra en la barra de estado situada encima del cuadro de mensajes, junto al [indicador de modelo activo](#choosing-a-model). La barra indica los tokens usados/totales en miles y se muestra en verde, ámbar o rojo a medida que se va llenando el contexto. Un `±` delante de la cifra significa que aún no se dispone de un recuento exacto.

Pasa el cursor por encima del contador para ver un desglose:

| Sección | Qué abarca |
| -- | -- |
| **Último turno** | El coste del intercambio más reciente: entrada nueva, tokens servidos desde la caché de «prompts» del proveedor, tokens escritos en la caché y salida |
| **Esta conversación (facturada)** | Las mismas cuatro cifras acumuladas en cada solicitud de la conversación, incluidos los viajes de ida y vuelta de las herramientas |
| **Contexto** | Tokens actualmente en la ventana de contexto, en comparación con el tamaño real de la ventana |

Una línea dice, por ejemplo, `37,588 input + 131,744 cached · write 37,558 · output 2,866`. Las partes relativas a la caché se omiten en el caso de los proveedores que no admiten el almacenamiento en caché de «prompts», y se omite una sección cuando no hay nada que informar.

> [!TIP]
> Compara **Último turno** con **Esta conversación (facturada)** para ver cuánto cuesta una sola pregunta. En una conversación larga, es normal que haya una cifra elevada en **Esta conversación (facturada)** junto a una cifra baja en **Último turno**.

### Ventana de contexto

La barra de uso del contexto, el punto de compactación automática y la longitud máxima de una sola respuesta utilizan la ventana de contexto del modelo seleccionado. Por ejemplo, un modelo con una ventana de un millón de tokens se mide en relación con un millón de tokens. Si no se conoce la ventana del modelo (un nombre de implementación de Azure OpenAI o personalizado, o un dispositivo en el que nunca se ha recuperado el catálogo de modelos), Tabular Editor utiliza 200 000 tokens.

### Reducción del uso de tokens

Seleccione objetos específicos en el **Explorador TOM** antes de formular su pregunta. A continuación, el asistente limita su contexto a los objetos seleccionados y no recupera los metadatos de todo el modelo, lo que reduce al máximo tanto el uso de tokens como el coste de la API.

Otras formas de reducir el uso de tokens:

- Haga preguntas concretas sobre tablas, medidas o columnas específicas. Una indicación imprecisa como «Establecer carpetas de visualización en todas las medidas» hace que el asistente recupere los metadatos de todo el modelo. Una indicación específica como «Establecer carpetas de visualización en las medidas que he seleccionado» limita el contexto a la selección actual y utiliza muchos menos tokens.
- Iniciar una nueva conversación cuando cambies de tema, para que no se acumulen historiales largos.
- Usar un modelo más pequeño o menos costoso para las preguntas exploratorias.

## Limitaciones

- Requiere su propia clave de API; no hay ninguna clave de API integrada.
- La calidad de las respuestas depende del proveedor y del modelo que se seleccione.
- El Asistente de IA no sustituye a los conocimientos de DAX ni a los fundamentos del diseño de modelos semánticos.
- El asistente de IA no puede acceder a archivos o servicios externos ni buscar en la web.
- El Asistente de IA no puede conectarse a servidores MCP externos para ampliar sus propias herramientas. Para usar tu propio agente con Tabular Editor 3, consulta @mcp-server
- El Asistente de IA no puede conectarse a un modelo distinto desde el chat. Cambiar las conexiones del modelo en la interfaz de usuario de Tabular Editor
- El asistente de IA no puede gestionar las preferencias.

## Desactivación del asistente de IA

El Asistente de IA es un componente opcional que se instala de forma predeterminada a partir de Tabular Editor 3.27.0. Ejecuta de nuevo el instalador de Tabular Editor 3 y selecciona **Modificar** para incluirlo o excluirlo de una instalación existente. Una actualización mantiene la selección existente; consulta [Actualizaciones y el componente de funciones de IA](xref:installation-activation-basic#upgrades-and-the-ai-features-component). En la compilación portátil, elimina `TabularEditor3.AI.dll` del directorio de instalación para quitarlo.

El mismo componente contiene el servidor MCP, por lo que, si lo excluyes o eliminas `TabularEditor3.AI.dll`, se eliminarán ambos. Para desactivar solo el chat, mantenga el componente y establezca la política `DisableAiChat`.

> [!NOTE]
> Tanto si el componente está instalado como si no, un administrador del sistema puede desactivar todas las funciones de IA en Tabular Editor 3, incluido el servidor MCP, con la [política `DisableAi`](xref:policies). `DisableMcpServer` desactiva únicamente el servidor MCP. Consulte @policies.
