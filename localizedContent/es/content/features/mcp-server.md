---
uid: mcp-server
title: Servidor MCP
author: Morten Lønskov
updated: 2026-10-09
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.27.0
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Servidor MCP

Tabular Editor 3 puede actuar como servidor MCP (Model Context Protocol). Los agentes que admiten MCP, como Claude Code, GitHub Copilot, el modo de agente de VS Code, Codex o Cursor, se conectan a la instancia en ejecución para leer, consultar y analizar el modelo semántico que tienes abierto y modificarlo si concedes acceso de escritura. Para empezar, selecciona **Herramientas > Servidor MCP...** y registra tu agente.

El servidor MCP no usa ningún proveedor de IA ni clave de API configurados en Tabular Editor, y tu agente usa su propio proveedor y su propia suscripción.

El agente trabaja con el modelo que Tabular Editor tiene abierto, incluidos los cambios no guardados. Puede ser un modelo de Power BI Desktop, un proyecto PBIP, una carpeta de TMDL (Tabular Model Definition Language), un archivo `.bim`, una base de datos de Workspace o una conexión en vivo a Analysis Services, Azure Analysis Services o Fabric. El agente usa las mismas herramientas tanto si el modelo está conectado como si está sin conexión, salvo las herramientas que necesitan una conexión en vivo, como las consultas DAX.

Los cambios del agente pasan por el [wrapper de Tabular Object Model (TOM)](xref:csharp-scripts) y el motor de C# Script, con la misma validación, el mismo ajuste de fórmulas y la misma pila de deshacer que tus propias ediciones. Aparecen como cambios no guardados, marcados en el [Explorador TOM y la vista de propiedades](xref:unsaved-changes), y no se escribe nada en el origen hasta que guardes.

## Antes de empezar

- Tabular Editor 3.27.0 o posterior, en cualquier edición.
- Tener instalado el componente **Funciones de IA**. Forma parte de la instalación predeterminada a partir de la versión 3.27.0. Consulta @installation-activation-basic si despliegas Tabular Editor de forma centralizada, y @policies si tu administrador ha desactivado las funciones de IA.
- Un agente que admita MCP sobre HTTP con streaming.

## Inicia el servidor

1. Selecciona **Herramientas > Servidor MCP...**.
2. Revisa los permisos. Consulta [Configurar permisos del agente](#set-agent-permissions).
3. Haz clic en **Iniciar servidor**.

El cuadro de diálogo muestra la dirección en la que escucha el servidor: `http://127.0.0.1:42100/`, a menos que hayas cambiado el puerto. El indicador de la barra de estado cambia de **MCP detenido** a **MCP iniciado**, con la dirección en su descripción emergente.

![Cuadro de diálogo del servidor MCP que muestra la dirección URL del servidor, un token de acceso enmascarado y las cinco filas de permisos del agente establecidas en niveles no predeterminados](~/content/assets/images/features/mcp-server/mcp-server-dialog.png)

![El indicador de la barra de estado que muestra MCP iniciado, con su descripción emergente mostrando "El servidor MCP está escuchando en http://127.0.0.1:42100/. Haz clic para abrir el cuadro de diálogo de conexión."](~/content/assets/images/features/mcp-server/status-bar-menu.png)

El servidor se ejecuta con o sin un modelo abierto. Si no hay ningún modelo abierto, los resultados de las herramientas lo indican, y puedes abrir un modelo en cualquier momento sin reiniciar el servidor.

Haz clic con el botón derecho en el indicador de la barra de estado para iniciar o detener el servidor, copiar una configuración de registro o abrir las preferencias del servidor MCP. Haz clic con el botón izquierdo para abrir el cuadro de diálogo sin iniciar ni detener el servidor.

![El indicador de MCP en la barra de estado con el menú del clic derecho abierto, mostrando Detalles del servidor MCP..., Detener servidor MCP, Copiar configuración de MCP y Preferencias del servidor MCP..., y el submenú Copiar configuración de MCP desplegado con Claude Code, VS Code, Copilot CLI, Codex y Cursor](~/content/assets/images/features/mcp-server/status-bar-context-menu.png)

### Preferencias de MCP

Abre **Herramientas > Preferencias > Características de IA > Servidor MCP** para configurar las opciones de inicio, autenticación y puerto del servidor.

![Preferencias del servidor MCP, mostrando Habilitar servidor MCP, Iniciar servidor MCP automáticamente, Requerir token de acceso y el puerto](~/content/assets/images/pref-mcp-server.png)

| Preferencia                              | Predeterminado | Qué hace                                                                                                                                                                                          |
| ---------------------------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Habilitar servidor MCP**               | Activado       | Al desmarcarlo, se detiene el servidor en ejecución y se eliminan el elemento del menú y el indicador de la barra de estado                                                                       |
| **Iniciar servidor MCP automáticamente** | Desactivado    | Inicia el servidor al iniciar Tabular Editor                                                                                                                                                      |
| **Requerir token de acceso**             | Desactivado    | Los agentes deben proporcionar el token de acceso que se muestra en el cuadro de diálogo del servidor. Consulta [Ejecución en un equipo compartido](#running-on-a-shared-machine) |
| **Puerto**                               | 42100          | El puerto de loopback en el que escucha el servidor, entre 1024 y 49151. Cambiarlo invalida los registros de agentes existentes                                                   |

## Registra tu agente

En el cuadro de diálogo del servidor, selecciona tu agente en **Exportar configuración** y pega la configuración copiada en tu agente. Solo tienes que registrar cada agente una vez, y la configuración registra el servidor con el nombre `tabular-editor`.

![La lista desplegable de configuración de exportación, expandida para mostrar Claude Code, VS Code, Copilot CLI, Codex y Cursor](~/content/assets/images/features/mcp-server/export-configuration.png)

**Claude Code**: ejecuta el comando copiado en una terminal:

```bash
claude mcp add --transport http tabular-editor http://127.0.0.1:42100/
```

**VS Code**: añade esto a tu configuración de MCP:

```json
{
  "servers": {
    "tabular-editor": {
      "type": "http",
      "url": "http://127.0.0.1:42100/"
    }
  }
}
```

**Copilot CLI**: añade lo siguiente en `~/.copilot/mcp-config.json`:

```json
{
  "mcpServers": {
    "tabular-editor": {
      "type": "http",
      "url": "http://127.0.0.1:42100/"
    }
  }
}
```

**Codex**: añade lo siguiente en `~/.codex/config.toml`:

```toml
[mcp_servers.tabular-editor]
url = "http://127.0.0.1:42100/"
```

**Cursor**: añade lo siguiente en `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "tabular-editor": {
      "url": "http://127.0.0.1:42100/"
    }
  }
}
```

Cuando está activado **Requerir token de acceso**, la configuración exportada incluye el token en el formato de cada cliente. Copia la configuración del cuadro de diálogo; no la escribas a mano.

Cualquier otro cliente MCP se conecta a `http://127.0.0.1:42100/` mediante HTTP con streaming. Si **Requerir token de acceso** está activado, envía el token en la cabecera `Authorization: Bearer <token>`.

### Comprueba que ha funcionado

Pregúntale a tu agente:

> ¿A qué modelo estoy conectado en Tabular Editor?

El agente responde con el nombre del modelo, cómo se carga, si tiene cambios sin guardar y su nivel de compatibilidad, o reporta que no hay ningún modelo abierto. No aparece ningún mensaje en Tabular Editor.

## Configurar los permisos del agente

Los permisos controlan qué herramientas recibe un agente, y el [Asistente de IA](xref:ai-assistant) usa los mismos permisos. Configúralos en el cuadro de diálogo **Herramientas > Servidor MCP...** o en **Herramientas > Preferencias > Funciones de IA > Permisos**; ambas opciones modifican la misma configuración.

![La página Permisos de funciones de IA, con un menú desplegable por recurso en su nivel predeterminado](~/content/assets/images/pref-ai-permissions.png)

Pasa el cursor sobre la etiqueta o la lista desplegable de un permiso para ver qué permite cada nivel. Si un administrador ha limitado un recurso mediante una [directiva](xref:policies), la lista desplegable es de solo lectura e indica la directiva.

Cada recurso tiene un nivel de acceso:

| Recurso                    | Predeterminado | Lo que obtiene el agente                                                                                                                                                                                                              |
| -------------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Metadatos del modelo**   | Lectura        | Lectura: tablas, columnas, medidas, expresiones, descripciones, relaciones y estadísticas del Analizador VertiPaq. Escritura: la capacidad de modificar el modelo mediante C# Scripts |
| **Datos del modelo**       | Denegar        | Lectura: resultados de consultas DAX (valores de datos de tu modelo). Requiere una conexión en vivo                                                                                |
| **Best Practice Analyzer** | Lectura        | Lectura: el conjunto de reglas y los resultados del análisis. Escritura: añadir y modificar reglas                                                                                    |
| **Documentos**             | Escritura      | Lectura: el contenido de tus consultas DAX abiertas, C# Scripts y scripts DAX. Escribir: modificarlos y crear scripts de C# y consultas DAX                                           |
| **Macros**                 | Escritura      | Lectura: tu biblioteca de macros, con nombres, descripciones y código. Escritura: no hay herramientas adicionales en esta versión                                                     |

**Escritura** (que aparece como **Lectura/escritura** en las listas desplegables) incluye **Lectura**, y **Datos del modelo** no tiene nivel de **Escritura**.

**Documentos** tiene **Escritura** de forma predeterminada, lo que permite a un agente crear pestañas y sobrescribir el contenido de los documentos abiertos: consultas DAX, C# Scripts y scripts DAX. El agente no los ejecuta y el modelo no cambia. Si tienes trabajo sin guardar en esas pestañas, establece **Documentos** en **Lectura**.

Aumentar estos permisos por encima de sus valores predeterminados le da al agente más acceso:

- **Datos del modelo > Leer** envía valores de tu modelo a tu agente y, a través de este, al proveedor del agente. Concédelo cuando el agente necesite contrastar los resultados con valores reales.
- **Metadatos del modelo > Escribir** permite al agente cambiar el modelo mediante C# Scripts. Consulta [Cómo un agente cambia tu modelo](#how-an-agent-changes-your-model) para ver las medidas de protección.

> [!IMPORTANT]
> Los permisos se leen cuando se inicia el servidor, y un agente obtiene su lista de herramientas cuando se conecta. Después de cambiar un permiso, detén el servidor, vuelve a iniciarlo y luego vuelve a conectar el agente. Hasta entonces, el agente conserva los permisos que estaban en vigor cuando se conectó.

## Qué puede hacer el agente

Las herramientas del agente dependen de los permisos que le concedas, y la siguiente tabla enumera lo que puedes pedir y el permiso que requiere cada solicitud.

| Solicitud                                                                                                                                                                  | Autorización necesaria                                              |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Identificar la instancia de Tabular Editor y el modelo que tiene abierto                                                                                                   | Ninguna                                                             |
| Buscar en la documentación, el blog, los issues y los debates de GitHub de Tabular Editor                                                                                  | Ninguna                                                             |
| Consultar la API de scripting: las propiedades, los métodos y las firmas de los objetos del modelo, para la versión de Tabular Editor que estés ejecutando | Ninguna                                                             |
| Obtener una visión general de las tablas, el recuento de columnas y medidas, y todas las relaciones                                                                        | **Metadatos del modelo > Leer**                                     |
| Obtener todos los detalles de los objetos con nombre, incluidas las expresiones, las descripciones, las cadenas de formato y los tipos de datos                            | **Metadatos del modelo > Leer**                                     |
| Buscar en el modelo por nombre, descripción, expresión DAX o M, cadena de formato o anotación                                                                              | **Metadatos del modelo > Leer**                                     |
| Obtener el modelo completo. Esto consume muchos tokens, y la descripción de la herramienta advierte al agente                                              | **Metadatos del modelo > Leer**                                     |
| Ver los objetos seleccionados en el Explorador TOM                                                                                                                         | **Metadatos del modelo > Lectura**                                  |
| Obtener estadísticas del Analizador VertiPaq: tamaños de tablas, cardinalidades de columnas y uso de memoria                                               | **Metadatos del modelo > Lectura**                                  |
| Listar las reglas efectivas del [Best Practice Analyzer](xref:best-practice-analyzer), incluidas las tuyas, y ejecutar el análisis                                         | **Best Practice Analyzer > Lectura**                                |
| Agregar o cambiar reglas en tu colección local                                                                                                                             | **Best Practice Analyzer > Escritura**                              |
| Ejecutar una consulta DAX y obtener filas como resultado. Una consulta devuelve 100 filas de forma predeterminada y como máximo 500                        | **Datos del modelo > Lectura** y **Metadatos del modelo > Lectura** |
| Ver las consultas DAX, los C# Scripts y los scripts DAX que tienes abiertos                                                                                                | **Metadatos del modelo > Lectura**                                  |
| Leer el contenido de las pestañas abiertas                                                                                                                                 | **Documentos > Lectura**                                            |
| Editar una pestaña o abrir un nuevo C# Script o una nueva consulta DAX para su revisión                                                                                    | **Documentos > Escritura**                                          |
| Leer tu biblioteca de macros                                                                                                                                               | **macros > Lectura**                                                |
| Cambiar el modelo. Consulta [Cómo un agente cambia tu modelo](#how-an-agent-changes-your-model)                                                            | **Metadatos del modelo > Escritura**                                |

Selecciona objetos en el Explorador TOM antes de mencionarlos en un prompt; por ejemplo, antes de pedir "dales un formato coherente".

Antes de que un C# Script o una consulta DAX del agente se abra como documento, Tabular Editor compila el script o valida la consulta contra el modelo abierto y devuelve al agente los errores que encuentre. La validación de consultas DAX requiere que Tabular Editor esté conectado a Analysis Services o Power BI.

> [!NOTE]
> Para consultar datos se necesita una conexión activa, y las estadísticas de VertiPaq requieren una conexión o estadísticas que ya hayas recopilado. La disponibilidad de las herramientas se establece cuando el agente se conecta, así que si conectas el modelo después, vuelve a conectar al agente.

## Cómo un agente cambia tu modelo

Con **Model metadata > Write**, un agente modifica tu modelo creando un [C# Script](xref:csharp-scripts) en segundo plano. Tabular Editor compila el script, comprueba que sea seguro y lo ejecuta en el modelo abierto.

Un script puede hacer todo lo que permite la API de scripting de C#; por ejemplo, agregar medidas, columnas, grupos de cálculo, perspectivas, traducciones, relaciones y políticas de actualización, o renombrar y dar formato a objetos de forma masiva. Un script ejecutado por un agente tiene estas propiedades:

- sus cambios aparecen como una sola entrada de deshacer, **C# Script (MCP)**, y **Ctrl+Z** deshace todo el script. Ver @undo-redo.
- si el script genera una excepción a mitad del proceso, se revierten todos sus cambios.
- el agente recibe una lista de todos los objetos que el script agregó, cambió o quitó, además de cualquier salida que haya generado el script.
- los mensajes de `Output`, `Info`, `Warning` o `Error` se devuelven al agente como parte del resultado y no se abre ningún cuadro de diálogo.
- mientras se ejecuta una llamada prolongada, aparece un indicador de **Please wait** y se descartan los clics en Tabular Editor.
- los objetos y propiedades modificados se marcan en el [Explorador TOM y la vista de propiedades](xref:unsaved-changes) hasta que guardes. **Mostrar cambios** filtra ambas vistas para mostrar solo los cambios, y al hacer clic con el botón derecho en **Revert** puedes deshacer una sola propiedad, un solo objeto o toda una rama.

![El menú Editar abierto con una única entrada "Deshacer C# Script (MCP)", con el Explorador TOM marcando una medida agregada en verde, una medida modificada en naranja y una medida eliminada tachada en rojo, y la vista de propiedades filtrada para mostrar la única propiedad modificada](~/content/assets/images/features/mcp-server/agent-change-review.png)

El chat del [Asistente de IA](xref:ai-assistant) ejecuta scripts del mismo modo, con un único paso de deshacer y la misma reversión, en la entrada de deshacer **C# Script (AI Assistant)**. Los scripts de agente no tienen cuadro de diálogo de vista previa ni **Cancelar**. Revisa sus cambios después en el Explorador TOM y la vista de propiedades.

### Operaciones bloqueadas

Estas operaciones se bloquean independientemente de tus permisos:

- `ExecuteCommand`, que ejecuta TMSL o XMLA sin procesar, siempre falla en un script ejecutado por un agente.
- Un script de agente que accede al sistema de archivos, hace una solicitud web o hace referencia a un ensamblado externo no se ejecuta. La comprobación es el mismo análisis del script compilado que utiliza la directiva `BlockUnsafeScripts`; consulta [Qué cuenta como mantenerse dentro del modelo](xref:csharp-scripts#what-counts-as-staying-within-the-model) para ver la lista completa. Lo que ocurra con el script depende de tus permisos y políticas:
  - Con **Documents > Write**, el script se abre como un documento **Agent script (review)** y el resultado de la herramienta indica al agente que te pida que lo revises y lo ejecutes.
  - Sin **Documents > Write**, el script no se ejecuta y no se abre ningún documento.
  - Si está establecida la [política](xref:policies) `BlockUnsafeScripts`, el script no se ejecuta y no se abre ningún documento.
- Los asistentes de DAX dentro de un script requieren **Datos del modelo > Leer**, al igual que la herramienta de consultas.

## Tareas de ejemplo

### Corregir infracciones del Best Practice Analyzer

Abre un modelo y pregunta:

> Ejecuta el Best Practice Analyzer y dime qué merece la pena corregir, empezando por lo peor.

A continuación, escribe "corrige las infracciones de las cadenas de formato". Si se concede **Metadatos del modelo > Escribir**, el agente escribe un script y lo ejecuta, y los objetos modificados se marcan en naranja en el Explorador TOM. La opción **Mostrar cambios** en la [vista de propiedades](xref:unsaved-changes) muestra los valores anteriores y posteriores de cada propiedad. Haz clic con el botón derecho en **Revertir** sobre cualquier cambio que no quieras y, después, guarda.

### Agregar medidas a partir de una especificación

Indícale al agente una especificación, un ticket o una hoja de cálculo con definiciones de medidas:

> Añade las medidas de requirements.md a la tabla Sales. Sigue la nomenclatura y las cadenas de formato que ya se usan allí.

El agente lee `requirements.md` en su propio Workspace.

### Verificar los resultados con una consulta

Si se concede **Datos del modelo > Leer**, el agente puede ejecutar DAX para comprobar su trabajo:

> Confirma que la nueva medida Margin % da el mismo total que el cálculo anterior para 2025.

Escribe la consulta DAX, la ejecuta y compara los resultados.

### Preparar un script sin ejecutarlo

Con **Documentos > Escribir**, el agente puede incluir un C# Script o una consulta DAX en un documento para que lo revises y lo ejecutes tú mismo, por ejemplo, para comprobar un cambio antes de ejecutarlo o para ejecutarlo más adelante en otro modelo:

> Escríbeme un script que renombre todas las medidas a tipo oración, pero no lo ejecutes.

El script se abre como documento en Tabular Editor, compilado y sometido a comprobaciones de seguridad. Ejecútalo después de leerlo.

> [!TIP]
> Revisa y guarda entre tareas para mantener reducido cada conjunto de cambios sin guardar.

## Ejecutar varias instancias

Cada instancia de Tabular Editor ejecuta su propio servidor en su propio puerto. Para trabajar con dos modelos a la vez, abre cada uno en su propia instancia y conecta un agente a cada instancia.

Para un segundo servidor, inicia la segunda instancia, abre **Herramientas > Servidor MCP...** y haz clic en **Iniciar servidor**. Si el puerto configurado está ocupado, un aviso ofrece el primer puerto libre entre los 20 siguientes; si no hay ninguno libre, aparece un error. También puedes configurar otro puerto en **Herramientas > Preferencia > Funciones de IA > Servidor MCP**.

Registra el segundo puerto en tu agente con su propio nombre y especifica en tus prompts el nombre de la instancia a la que te refieres.

## Ejecutar en un equipo compartido

El servidor escucha en `127.0.0.1`, al que otras máquinas no pueden acceder. También rechaza las solicitudes del navegador con un encabezado `Origin` no local.

Cuando **Requerir token de acceso** está desactivado, cualquier proceso de la máquina puede conectarse sin credenciales. En un host donde varias personas tienen sesión iniciada a la vez, como un servidor de Remote Desktop o Citrix, eso incluye los procesos de las sesiones de otras personas.

Selecciona **Requerir token de acceso** en **Herramientas > Preferencias > Funciones de IA > Servidor MCP** y reinicia el servidor. Los agentes deben presentar entonces el token que se muestra en el cuadro de diálogo del servidor, y las solicitudes que no lo incluyan se rechazan.

Selecciona **Regenerar token** (el botón de actualización junto al token) para generar un nuevo token, lo que invalida los registros existentes y reinicia el servidor si está en ejecución. Si el token queda expuesto, regénéralo y vuelve a registrar tus agentes. Los administradores pueden hacer que el token sea obligatorio para todos con la directiva `RequireMcpAccessToken`, que además bloquea esa preferencia. Consulta @policies.

## Qué sale de tu equipo

Cuando usas el servidor MCP, Tabular Editor no se comunica con ningún proveedor de IA y solo responde a llamadas a herramientas de procesos de tu máquina, a través de una conexión de loopback. La base de conocimiento que consulta el agente es una base de datos local que se incluye con Tabular Editor y se actualiza desde el servicio de Tabular Editor.

Tu agente envía datos a su proveedor conforme a tu suscripción y a las condiciones de ese proveedor, y la configuración de tu agente controla qué se envía. Con **Datos del modelo** en su valor predeterminado, **Denegar**, el agente no recibe ningún resultado de consultas DAX desde Tabular Editor. Los valores introducidos en la definición del modelo, como una expresión `DATATABLE` o una tabla de **Introducir datos**, son metadatos del modelo y llegan al agente en **Metadatos del modelo > Leer**.

Consulta @security-privacy para obtener una visión más amplia, incluido el [Asistente de IA](xref:ai-assistant), que se comunica directamente con un proveedor y se configura por separado.

## Controles de administrador

El servidor MCP está activado de forma predeterminada y cualquier usuario puede desactivarlo. Los administradores pueden usar estas [directivas](xref:policies) para controlar cómo funciona el MCP:

| Directiva                                   | Edición    | Qué hace                                                                                                                                                                                                                                                |
| ------------------------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DisableMcpServer`                          | Todas      | Elimina el servidor MCP. El chat del Asistente de IA no se ve afectado                                                                                                                                                                  |
| `DisableAi`                                 | Todas      | Desactiva toda la funcionalidad de IA, incluido el servidor MCP. Con un valor `REG_DWORD` de `1`, el instalador también deja desactivado el componente de IA en el equipo                                                               |
| `RequireMcpAccessToken`                     | Todas      | Fuerza la autenticación por token y bloquea la preferencia                                                                                                                                                                                              |
| `DisableCSharpScripts`                      | Todos      | Impide que un agente ejecute un C# Script y lo inserte en un documento. La redacción de una consulta DAX y cualquier herramienta que solo lea no se ven afectadas                                                                       |
| `BlockUnsafeScripts`                        | Enterprise | En Tabular Editor, solo se permiten scripts que se mantengan dentro del modelo. Un script de agente que acceda a archivos, a la red, a otros procesos o a ensamblados externos no se ejecuta, y no se abre ningún documento de revisión |
| Límites de permisos `Max...` y `McpMax...`  | Enterprise | Establece un límite para cada recurso. Los límites `Max...` se aplican al Asistente de IA y al servidor MCP. Los límites `McpMax...` se aplican únicamente al servidor MCP y solo pueden reducir el límite `Max...`     |
| `AiAuditLogPath`, `AiAuditLogRetentionDays` | Enterprise | Configura la ubicación y la retención del [registro de auditoría](xref:ai-audit-log)                                                                                                                                                                    |
| `AiProvider` y valores relacionados         | Enterprise | Bloquea el proveedor del Asistente de IA. El servidor MCP no se ve afectado                                                                                                                                                             |

> [!WARNING]
> Sin una licencia Enterprise, cualquier valor de directiva Enterprise impide que se inicien el Asistente de IA y el servidor MCP, y elimina el elemento de menú y el indicador de la barra de estado. Un valor de `BlockUnsafeScripts` también bloquea todos los scripts y las macros, así que implementa directivas Enterprise solo en equipos con licencia Enterprise (consulta [Qué ocurre sin la Edición Enterprise](xref:policies#what-happens-without-enterprise-edition)).

En la Edición Enterprise, Tabular Editor mantiene un [registro de auditoría](xref:ai-audit-log) local de la actividad del Asistente de IA y del servidor MCP, incluidas todas las herramientas que un agente invocó y el texto completo de cualquier C# Script que ejecutó. Los prompts, las respuestas y los valores de datos no se registran. El botón **Abrir carpeta de auditoría** en el cuadro de diálogo del servidor y en **Herramientas > Preferencias > Características de IA** abre la carpeta del registro. En las ediciones Desktop y Edición Business, no se registra nada y no aparece ninguno de los dos botones.

Consulta @policies para ver la lista completa, la estructura del Registro y las plantillas administrativas.

## Solución de problemas

| Lo que ves                                                                                               | Qué ocurre                                                                                                                                                                                                                                                                                                                                         |
| -------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| El agente dice que no tiene herramientas para Tabular Editor                                             | El servidor no está en ejecución, o el agente se conectó antes de que arrancara. Comprueba que la barra de estado muestre **MCP iniciado** y, a continuación, vuelve a conectar el agente                                                                                                                                          |
| El agente no puede ver un permiso que acabas de conceder                                                 | Los permisos se leen al iniciar el servidor y la lista de herramientas queda fijada en el momento de la conexión. Detén el servidor y vuelve a iniciarlo; luego vuelve a conectar el agente                                                                                                                                        |
| El agente pierde la conexión tras una pausa larga                                                        | El servidor cierra una sesión tras 20 minutos sin solicitudes y sin ningún flujo abierto. Vuelve a conectar el agente                                                                                                                                                                                                              |
| El agente reporta que no hay ningún modelo abierto                                                       | El servidor se ejecuta de forma independiente de tu modelo. Abre un modelo en Tabular Editor y vuelve a preguntar. No hace falta reiniciar nada                                                                                                                                                                    |
| El agente no puede ejecutar consultas DAX                                                                | De forma predeterminada, **Datos del modelo** está configurado como **Denegar**. Las consultas también necesitan una conexión activa: con un modelo abierto desde el disco, la herramienta de consultas no está disponible, independientemente del permiso concedido                                               |
| Las conexiones se rechazan con un 401                                                                    | **Requerir token de acceso** está activada y el agente no está enviando el token. Vuelve a copiar la configuración de registro desde el cuadro de diálogo. Incluye el token                                                                                                                                        |
| El puerto ya está en uso                                                                                 | Otra instancia de Tabular Editor u otra aplicación lo está usando. Acepta el siguiente puerto libre cuando se te pida y actualiza el registro del agente. Si **Iniciar el servidor MCP automáticamente** está activado, un conflicto al iniciar no muestra ningún aviso y el indicador muestra **MCP Stopped**     |
| **Herramientas > Servidor MCP...** no aparece en el menú | La opción **Habilitar servidor MCP** está desmarcada en las preferencias, el componente de funciones de IA no está instalado, un administrador ha establecido `DisableMcpServer` o `DisableAi`, o se ha configurado un valor de directiva Enterprise en un equipo que no tiene licencia para ello. Consulta @policies |

## Pasos a seguir

- @ai-assistant para el modelo completo de permisos y el chat integrado.
- @unsaved-changes para revisar y revertir lo que hizo un agente.
- @csharp-scripts para saber qué puede cambiar un script y, por tanto, un agente.
- @policies para gestionar el servidor a nivel de toda la organización.
- @te-cli-skill si tu agente trabaja con archivos de modelo en un repositorio o una canalización.
