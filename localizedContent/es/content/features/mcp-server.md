---
uid: mcp-server
title: Servidor MCP
author: Morten Lønskov
updated: 2026-10-14
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

Tabular Editor 3 puede actuar como servidor MCP (Protocolo de contexto de modelo). Los agentes que admiten MCP, como Claude Code, GitHub Copilot, el modo agente de VS Code, Codex o Cursor, se conectan a la instancia en ejecución para leer, consultar y analizar el modelo semántico que tienes abierto, y para modificarlo si concedes acceso de escritura. Para empezar, seleccione **Herramientas > Servidor MCP...** y registre su agente.

El servidor MCP no utiliza un proveedor de IA ni una clave de API configurados en Tabular Editor, y tu agente utiliza su propio proveedor y su propia suscripción.

El agente trabaja en el modelo que Tabular Editor tiene abierto, incluidos los cambios no guardados. Puede tratarse de un modelo de Power BI Desktop, un proyecto PBIP, una carpeta TMDL (lenguaje de definición de modelo tabular), un archivo `.bim`, una base de datos de área de trabajo o una conexión en tiempo real a Analysis Services, Azure Analysis Services o Fabric. El agente utiliza las mismas herramientas tanto si el modelo está conectado como si está sin conexión, excepto en el caso de las herramientas que necesitan una conexión en tiempo real, como las consultas DAX.

Los cambios del agente pasan por el [envoltorio del Tabular Object Model (TOM)](xref:csharp-scripts) y el motor de scripting de C#, con la misma validación, corrección de fórmulas y pila de deshacer que sus propias modificaciones. Aparecen como cambios sin guardar, marcados en el [Explorador TOM y en la vista Propiedades](xref:unsaved-changes), y no se escribe nada en el origen hasta que guarda.

## Antes de empezar

- Tabular Editor 3.27.0 o posterior, cualquier edición.
- El componente **Funciones de IA** instalado. Forma parte de la instalación predeterminada a partir de la versión 3.27.0. Consulta @installation-activation-basic si implementas Tabular Editor de forma centralizada y @policies si tu administrador ha desactivado las funciones de IA.
- Un agente que admita MCP a través de HTTP transmitible.

## Iniciar el servidor

1. Seleccione **Herramientas > Servidor MCP...**.
2. Revise los permisos. Consulte [Establecer permisos del agente](#set-agent-permissions).
3. Haz clic en **Iniciar servidor**.

El cuadro de diálogo muestra la dirección en la que escucha el servidor: `http://127.0.0.1:42100/`, a menos que haya cambiado el puerto. El indicador de la barra de estado cambia de **MCP detenido** a **MCP iniciado**, con la dirección en su información sobre herramientas.

![El cuadro de diálogo del servidor MCP, que muestra la URL del servidor, un token de acceso enmascarado y las cinco filas de permisos del agente configuradas con niveles distintos de los predeterminados](~/content/assets/images/features/mcp-server/mcp-server-dialog.png)

![El indicador de la barra de estado de MCP que indica «MCP iniciado», con su información sobre herramientas que muestra «El servidor MCP está escuchando en http://127.0.0.1. Haz clic para abrir el cuadro de diálogo de conexión."](~/content/assets/images/features/mcp-server/status-bar-menu.png)

El servidor se ejecuta con o sin un modelo abierto. Si no hay ningún modelo abierto, los resultados de la herramienta lo indican, y puedes abrir un modelo en cualquier momento sin reiniciar el servidor.

Haga clic con el botón derecho en el indicador de la barra de estado para iniciar o detener el servidor, copiar una configuración de registro o abrir las preferencias del servidor MCP. Haga clic con el botón izquierdo para abrir el cuadro de diálogo sin iniciar ni detener el servidor.

![El indicador de la barra de estado de MCP con su menú contextual abierto en Detalles del servidor MCP..., Detener el servidor MCP, Copiar la configuración de MCP y Preferencias del servidor MCP..., y el submenú Copiar la configuración de MCP expandido para mostrar Claude Code, VS Code, Copilot CLI, Codex y Cursor](~/content/assets/images/features/mcp-server/status-bar-context-menu.png)

### Preferencias de MCP

Abra **Herramientas > Preferencias > Funciones de IA > Servidor MCP** para configurar las opciones de inicio, autenticación y puerto del servidor.

![Preferencias del servidor MCP, que muestran las opciones «Habilitar servidor MCP», «Iniciar servidor MCP automáticamente», «Requerir token de acceso» y el puerto](~/content/assets/images/pref-mcp-server.png)

| Preferencia | Valor predeterminado | Qué hace |
| -- | -- | -- |
| **Habilitar servidor MCP** | Activado | Si se desactiva, se detiene un servidor en ejecución y se eliminan el elemento del menú y el indicador de la barra de estado |
| **Iniciar el servidor MCP automáticamente** | Desactivado | Inicia el servidor cuando se inicia Tabular Editor |
| **Requerir token de acceso** | Desactivado | Los agentes deben presentar el token de acceso que se muestra en el cuadro de diálogo del servidor. Consulte [Ejecución en un equipo compartido](#running-on-a-shared-machine) |
| **Puerto** | 42100 | El puerto de bucle invertido en el que escucha el servidor, de 1024 a 49151. Si se cambia, se invalidan los registros de agentes existentes |

## Registra tu agente

En el cuadro de diálogo del servidor, seleccione su agente en **Exportar configuración** y pegue la configuración copiada en su agente. Registra cada agente una sola vez, y la configuración registra el servidor con el nombre `tabular-editor`.

![El menú desplegable «Exportar configuración», expandido para mostrar Claude Code, VS Code, Copilot CLI, Codex y Cursor](~/content/assets/images/features/mcp-server/export-configuration.png)

**Claude Code**: ejecuta el comando copiado en un terminal:

```bash
claude mcp add --transport http tabular-editor http://127.0.0.1:42100/
```

**VS Code**: añade lo siguiente a tu configuración de MCP:

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

**CLI de Copilot**: añada a `~/.copilot/mcp-config.json`:

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

**Codex**: añada a `~/.codex/config.toml`:

```toml
[mcp_servers.tabular-editor]
url = "http://127.0.0.1:42100/"
```

**Cursor**: añada lo siguiente a `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "tabular-editor": {
      "url": "http://127.0.0.1:42100/"
    }
  }
}
```

Cuando la opción **Requerir token de acceso** está activada, la configuración exportada incluye el token en el formato de cada cliente. Copie la configuración del cuadro de diálogo; no la escriba a mano.

Cualquier otro cliente MCP se conecta a `http://127.0.0.1:42100/` a través de HTTP transmisible. Si la opción **Requerir token de acceso** está activada, envía el token en un encabezado `Authorization: Bearer <token>`.

### Comprueba que haya funcionado

Pregúntale a tu agente:

> ¿A qué modelo estoy conectado en Tabular Editor?

El agente responde con el nombre del modelo, cómo se carga el modelo, si tiene cambios sin guardar y su nivel de compatibilidad, o informa de que no hay ningún modelo abierto. No aparece ningún mensaje en Tabular Editor.

El nombre del modelo que recibe el agente sigue la configuración **Detalle del origen del modelo** en **Herramientas > Preferencias > Tabular Editor > Interfaz de usuario**. Con **Solo nombre**, el agente no recibe rutas de archivo ni nombres de servidores, y con **Oculto**, recibe `Model loaded` en lugar del nombre del modelo.

## Establecer permisos del agente

Los permisos controlan qué herramientas recibe un agente, y el [asistente de IA](xref:ai-assistant) utiliza los mismos permisos. Establézcalos en el cuadro de diálogo **Herramientas > Servidor MCP...** o en **Herramientas > Preferencias > Funciones de IA > Permisos**, ya que ambos modifican la misma configuración.

![La página de permisos de las funciones de IA, con un menú desplegable por recurso en su nivel predeterminado](~/content/assets/images/pref-ai-permissions.png)

Pasa el cursor sobre la etiqueta o el menú desplegable de un permiso para ver qué permite cada nivel. Si un administrador ha limitado un recurso mediante una [política](xref:policies), el menú desplegable es de solo lectura e indica la política.

Cada recurso tiene un nivel de acceso:

| Recurso | Predeterminado | Lo que obtiene el agente |
| -- | -- | -- |
| **Metadatos del modelo** | Lectura | Lectura: tablas, columnas, medidas, expresiones, descripciones, relaciones, estadísticas del Analizador VertiPaq y los mensajes de error y advertencia del modelo. Escritura: la capacidad de cambiar el modelo mediante scripts de C# |
| **Datos del modelo** | Denegar | Leer: resultados de consultas DAX (valores de datos de su modelo) y el texto de los errores devueltos por Analysis Services, que pueden contener valores de datos. Las consultas DAX necesitan una conexión en tiempo real |
| **Best Practice Analyzer** | Lectura | Lectura: el conjunto de reglas y los resultados del análisis. Escritura: añadir y modificar reglas |
| **Documentos** | Escritura | Lectura: el contenido de tus consultas DAX abiertas, tus scripts de C# y tus scripts DAX, así como los errores y las advertencias de todos los documentos abiertos, incluidas las Pivot Grids. Escritura: modificarlos y crear scripts de C# y consultas DAX. Los diseños de Pivot Grid no se pueden leer ni modificar |
| **Macros** | Escritura | Lectura: tu biblioteca de macros, con nombres, descripciones y código. Escritura: no hay herramientas adicionales en esta versión |

**Escritura** (denominada **Lectura/Escritura** en los menús desplegables) incluye Lectura, y **Datos del modelo** no tiene nivel de Escritura.

El valor predeterminado de **Documentos** es Escritura, lo que permite a un agente crear pestañas y sobrescribir el contenido de las consultas DAX, los C# Scripts y los scripts DAX abiertos. El agente no los ejecuta y el modelo no cambia. Si conserva trabajo sin guardar en esas pestañas, establezca **Documentos** en **Lectura**.

Si se elevan estos permisos por encima de sus valores predeterminados, el agente tendrá más acceso:

- **Datos del modelo > Lectura** envía valores desde tu modelo a tu agente y, a través de él, al proveedor de tu agente. Conceda este permiso cuando el asistente necesite comparar los resultados con valores reales.
- **Metadatos del modelo > Escritura** permite al agente cambiar el modelo a través de scripts de C#. Consulta [Cómo cambia un agente tu modelo](#how-an-agent-changes-your-model) para conocer las medidas de seguridad.

> [!IMPORTANT]
> Los permisos se leen cuando se inicia el servidor, y un agente obtiene su lista de herramientas cuando se conecta. Después de cambiar un permiso, detenga e inicie el servidor y, a continuación, vuelva a conectar el agente. Hasta entonces, el agente conserva los permisos que estaban vigentes cuando se conectó.

## Qué puede hacer el agente

Las herramientas del agente dependen de tus concesiones. En la siguiente tabla se indica lo que puedes solicitar y la concesión que necesita cada solicitud.

| Solicitud | Concesión necesaria |
| -- | -- |
| Identificar la instancia de Tabular Editor y el modelo que tiene abierto | Ninguno |
| Buscar en la documentación de Tabular Editor, el blog, los problemas de GitHub y los debates | Ninguno |
| Buscar en la API de scripting: las propiedades, los métodos y las firmas de los objetos del modelo, para la versión de Tabular Editor que estés ejecutando | Ninguno |
| Obtener una descripción general de las tablas, el número de columnas y medidas de cada una y todas las relaciones | **Metadatos del modelo > Leer** |
| Obtener información completa sobre los objetos con nombre, incluidas las expresiones, las descripciones, las cadenas de formato y los tipos de datos | **Metadatos del modelo > Leer** |
| Buscar en el modelo por nombre, descripción, expresión DAX o M, cadena de formato o anotación | **Metadatos del modelo > Leer** |
| Obtener el modelo completo. Esto utiliza muchos tokens, y la descripción de la herramienta advierte al agente | **Metadatos del modelo > Leer** |
| Ver los objetos seleccionados en el Explorador TOM | **Metadatos del modelo > Leer** |
| Obtener estadísticas del Analizador VertiPaq: tamaños de las tablas, cardinalidades de las columnas y uso de la memoria | **Metadatos del modelo > Lectura** |
| Enumerar las reglas efectivas del [Best Practice Analyzer](xref:best-practice-analyzer), incluidas las tuyas propias, y ejecutar el análisis | **Best Practice Analyzer > Leer** |
| Añadir o cambiar reglas en tu colección local | **Best Practice Analyzer > Escritura** |
| Ejecutar una consulta DAX y obtener filas a cambio. Una consulta devuelve 100 filas de forma predeterminada y, como máximo, 500 | **Datos del modelo > Leer** y **Metadatos del modelo > Leer** |
| Enumerar los errores, las advertencias y los mensajes de Analysis Services del modelo, empezando por las causas raíz | **Metadatos del modelo > Lectura**. El texto de los errores de Analysis Services también necesita **Datos del modelo > Lectura** |
| Enumerar sus consultas DAX abiertas, scripts de C#, scripts DAX y Pivot Grids, con el documento activo y el número de errores y advertencias de cada documento | **Metadatos del modelo > Leer** |
| Leer el contenido de una consulta DAX abierta, un script de C# o un script de DAX | **Documentos > Leer** |
| Leer los errores y las advertencias de un documento abierto, incluidos los errores que devolvió el servidor la última vez que se ejecutó | **Documentos > Leer**. El texto de los errores del servidor también necesita **Datos del modelo > Leer** |
| Editar una consulta DAX abierta, un script de C# o un script de DAX, o abrir un nuevo script de C# o una nueva consulta DAX para revisarlos | **Documentos > Escritura** |
| Leer tu biblioteca de macros | **Macros > Leer** |
| Cambiar el modelo. Consulte [Cómo cambia un agente su modelo](#how-an-agent-changes-your-model) | **Metadatos del modelo > Escritura** |

Seleccione objetos en el Explorador TOM antes de hacer referencia a ellos en una solicitud, por ejemplo, antes de pedir «formatear estos de forma coherente». Para preguntar sobre un error en una consulta o un script, haga que su pestaña sea el documento activo primero, por ejemplo, antes de preguntar «¿Por qué veo este error en esta consulta?».

Antes de que un C# Script o una consulta DAX del agente se abra como documento, el Tabular Editor compila el script o valida la consulta con el modelo abierto y devuelve los errores al agente. La validación de consultas DAX requiere que Tabular Editor esté conectado a Analysis Services o a Power BI.

> [!NOTE]
> Para consultar datos se necesita una conexión en tiempo real, y para las estadísticas de VertiPaq se necesita una conexión o unas estadísticas que ya hayas recopilado. La disponibilidad de las herramientas se establece cuando el agente se conecta, por lo que, si conecta el modelo posteriormente, deberá volver a conectar el agente.

## Cómo cambia un agente tu modelo

Con **Metadatos del modelo > Escribir**, un agente cambia su modelo creando un [script de C#](xref:csharp-scripts) en segundo plano. Tabular Editor compila el script, lo comprueba para garantizar su seguridad y lo ejecuta en el modelo abierto.

Un script puede hacer cualquier cosa que admita la API de C# Script, por ejemplo, añadir medidas, columnas, grupos de cálculo, perspectivas, traducciones, relaciones y políticas de actualización, o cambiar el nombre y dar formato a objetos de forma masiva. Un script ejecutado por un agente tiene estas propiedades:

- Sus cambios constituyen una única entrada de deshacer, **Script de C# (MCP)**, y **Ctrl+Z** deshace todo el script. Si un documento tiene el foco, **Ctrl+Z** deshace la escritura en el documento. Haga clic primero en el Explorador TOM o seleccione **Deshacer script de C# (MCP)** en el menú **Editar**. Consulte [Deshacer en editores de texto](xref:undo-redo#undo-in-text-editors).
- Si el script genera una excepción a mitad de su ejecución, se revierten todos sus cambios.
- El agente recibe una lista de todos los objetos que el script ha añadido, modificado o eliminado, además de todo lo que el script ha impreso. Si el script introdujo o resolvió errores DAX, el resultado también los enumera, agrupados por causa raíz.
- Los mensajes de `Output`, `Info`, `Warning` o `Error` se devuelven al agente como parte del resultado, y no se abre ningún cuadro de diálogo.
- Mientras se ejecuta una llamada larga, aparece un indicador de **Espere** y se descartan los clics en Tabular Editor.
- Los objetos y propiedades modificados se marcan en el [Explorador TOM y en la vista Propiedades](xref:unsaved-changes) hasta que se guarden. **Mostrar cambios** filtra ambas vistas para mostrar los cambios, y al hacer clic con el botón derecho en **Revertir** se deshace una sola propiedad, un solo objeto o una rama completa.

![El menú Editar abierto en una sola entrada de Deshacer script de C# (MCP), con el Explorador TOM marcando una medida añadida en verde, una medida modificada en naranja y una medida eliminada tachada en rojo, y la vista Propiedades filtrada para mostrar la única propiedad modificada](~/content/assets/images/features/mcp-server/agent-change-review.png)

El chat del [asistente de IA](xref:ai-assistant) ejecuta los scripts de la misma manera, con el mismo paso único de deshacer y revertir, bajo la entrada de deshacer **Script de C# (asistente de IA)**. Los scripts del agente no tienen cuadro de diálogo de vista previa ni opción de **Cancelar**. Revise sus cambios posteriormente en el Explorador TOM y en la vista Propiedades.

### Operaciones bloqueadas

Estas operaciones están bloqueadas independientemente de sus concesiones:

- `ExecuteCommand`, que ejecuta TMSL o XMLA sin procesar, siempre falla en un script ejecutado por un agente.
- Un script de agente que accede al sistema de archivos, realiza una solicitud web o hace referencia a un ensamblado externo no se ejecuta. La comprobación es el mismo análisis del script compilado que utiliza la política `BlockUnsafeScripts`; consulte [Qué se considera permanecer dentro del modelo](xref:csharp-scripts#what-counts-as-staying-within-the-model) para ver la lista completa. Lo que sucede con el script depende de sus concesiones y políticas:
  - Con **Documentos > Escritura**, el script se abre como un documento **Script de agente (revisión)**, y el resultado de la herramienta indica al agente que usted lo revise y lo ejecute.
  - Sin **Documentos > Escritura**, el script no se ejecuta y no se abre ningún documento.
  - Con la [política](xref:policies) `BlockUnsafeScripts` establecida, el script no se ejecuta y no se abre ningún documento.
- Los ayudantes de DAX dentro de un script necesitan **Datos del modelo > Leer**, al igual que la herramienta de consultas.

## Ejemplos de tareas

### Corregir las infracciones del Best Practice Analyzer

Abra un modelo y pregunte:

> Ejecuta Best Practice Analyzer y dime qué merece la pena corregir, empezando por lo peor.

Continúe con «corregir las infracciones de la cadena de formato». Si se concede **Metadatos del modelo > Escritura**, el agente escribe un script y lo ejecuta, y los objetos modificados se marcan en naranja en el Explorador TOM. **Mostrar cambios** en la [vista Propiedades](xref:unsaved-changes) muestra los valores anteriores y posteriores de cada propiedad. Haga clic con el botón derecho en **Revertir** en cualquier cambio que no desee y, a continuación, guárdelo.

### Agregar medidas desde una especificación

Indique al agente una especificación, un «ticket» o una hoja de cálculo con definiciones de medidas:

> Añada las medidas de requirements.md a la tabla Ventas. Siga las cadenas de nomenclatura y formato que ya se utilizan allí.

El agente lee `requirements.md` desde su propio espacio de trabajo.

### Verificar los resultados con una consulta

Con el permiso **Datos del modelo > Leer** concedido, el agente puede ejecutar DAX para comprobar su trabajo:

> Confirme que la nueva medida «Margin %» da el mismo total que el cálculo anterior para 2025.

Escribe la consulta DAX, la ejecuta y compara los resultados.

### Redactar un script sin ejecutarlo

Con **Documentos > Escribir**, el agente puede introducir un script de C# o una consulta DAX en un documento que usted revisa y ejecuta por su cuenta, por ejemplo, para comprobar un cambio antes de ejecutarlo o para ejecutarlo en otro modelo más adelante:

> Escríbeme un script que cambie el nombre de todas las medidas a mayúscula inicial, pero no lo ejecutes.

El script se abre como un documento en Tabular Editor, compilado y con la seguridad comprobada. Ejecútelo después de leerlo.

> [!TIP]
> Revisa y guarda entre tareas para que cada conjunto de cambios sin guardar sea pequeño.

## Ejecución de varias instancias

Cada instancia de Tabular Editor aloja su propio servidor en su propio puerto. Para trabajar en dos modelos a la vez, abra cada uno en su propia instancia y conecte un agente a cada uno.

Para un segundo servidor, inicie la segunda instancia, abra **Herramientas > Servidor MCP...** y haga clic en **Iniciar servidor**. Si el puerto configurado está ocupado, un mensaje le ofrecerá el primer puerto libre de entre los 20 siguientes, o aparecerá un error si no hay ninguno libre. También puede configurar otro puerto en **Herramientas > Preferencias > Funciones de IA > Servidor MCP**.

Registra el segundo puerto con tu agente con su propio nombre y nombra la instancia a la que te refieres en tus indicaciones.

## Ejecución en un equipo compartido

El servidor se vincula a `127.0.0.1`, a la que otros equipos no pueden acceder. También rechaza las solicitudes del navegador con un encabezado `Origin` no local.

Cuando la opción **Requerir token de acceso** está desactivada, cualquier proceso del equipo puede conectarse sin credenciales. En un host en el que varias personas han iniciado sesión a la vez, como un Escritorio remoto o un servidor Citrix, eso incluye procesos en las sesiones de otras personas.

Seleccione **Requerir token de acceso** en **Herramientas > Preferencias > Funciones de IA > Servidor MCP** y reinicie el servidor. A continuación, los agentes deben presentar el token que se muestra en el cuadro de diálogo del servidor, y las solicitudes que no lo incluyan se rechazarán.

Seleccione **Regenerar token** (el botón de actualización junto al token) para emitir un nuevo token, lo que invalida los registros existentes y reinicia un servidor en ejecución. Si el token queda expuesto, vuelve a generarlo y registra de nuevo a tus agentes. Los administradores pueden hacer que el token sea obligatorio para todos con la directiva `RequireMcpAccessToken`, que también bloquea la preferencia. Consulte @policies.

## Qué sale de tu equipo

Cuando usas el servidor MCP, Tabular Editor no se pone en contacto con ningún proveedor de IA y solo responde a las llamadas de herramientas de los procesos de tu dispositivo, a través de una conexión de bucle invertido. La base de conocimientos que busca el agente es una base de datos local que se incluye con Tabular Editor y que se actualiza desde el servicio de Tabular Editor.

Tu agente envía datos a su proveedor en virtud de tu suscripción y de las condiciones de dicho proveedor, y la configuración de tu agente controla lo que se envía. Con **Datos del modelo** en su valor predeterminado, **Denegar**, el agente no recibe ningún valor de datos de Tabular Editor, y el texto de los errores de Analysis Services se sustituye por una frase fija. Para que el agente no reciba las rutas de los archivos ni los nombres de los servidores, establezca **Detalles del origen del modelo** en **Herramientas > Preferencias > Tabular Editor > Interfaz de usuario** en **Solo nombre** u **Oculto**.

Consulte @security-privacy para obtener una visión más amplia, incluido el [Asistente de IA](xref:ai-assistant), que llama directamente a un proveedor y se configura por separado.

## Controles del administrador

El servidor MCP está activado de forma predeterminada, y cualquier usuario puede desactivarlo. Los administradores pueden usar estas [políticas](xref:policies) para controlar cómo funciona el MCP:

| Política | Edición | Qué hace |
| -- | -- | -- |
| `DisableMcpServer` | Todas | Elimina el servidor MCP. El chat del asistente de IA no se ve afectado |
| `DisableAi` | Todas | Desactiva todas las funcionalidades de IA, incluido el servidor MCP. Con un valor `REG_DWORD` de `1`, el instalador también deja el componente de IA fuera de las nuevas instalaciones y lo elimina al actualizar |
| `RequireMcpAccessToken` | Todos | Fuerza la autenticación con token y bloquea la preferencia |
| `DisableCSharpScripts` | Todos | Impide que un agente ejecute un script de C# y lo redacte en un documento. La redacción de una consulta DAX y todas las herramientas que solo leen no se ven afectadas |
| `BlockUnsafeScripts` | Enterprise | Permite únicamente los scripts que permanecen dentro del modelo, para cada script en Tabular Editor. Un script de agente que accede a archivos, a la red, a otros procesos o a ensamblados externos no se ejecuta, y no se abre ningún documento de revisión |
| Límites de permisos `Max...` y `McpMax...` | Enterprise | Limitan cada recurso. Los límites `Max...` se aplican al asistente de IA y al servidor MCP. Los límites `McpMax...` se aplican únicamente al servidor MCP y solo pueden reducir el límite `Max...` |
| `AiAuditLogPath`, `AiAuditLogRetentionDays` | Enterprise | Establecen la ubicación y el período de conservación del [registro de auditoría](xref:ai-audit-log) |
| `AiProvider` y valores relacionados | Enterprise | Bloquear el proveedor del asistente de IA. El servidor MCP no se ve afectado |

> [!WARNING]
> Sin una licencia Enterprise, cualquier valor de política Enterprise impide que el Asistente de IA y el servidor MCP se inicien y elimina el elemento del menú y el indicador de la barra de estado. El valor `BlockUnsafeScripts` también bloquea todos los scripts y macros, por lo que debe implementar las políticas Enterprise solo en equipos con licencia Enterprise (consulte [Qué sucede sin la Enterprise Edition](xref:policies#what-happens-without-enterprise-edition)).

En la edición Enterprise, Tabular Editor mantiene un [registro de auditoría](xref:ai-audit-log) local de la actividad del Asistente de IA y del servidor MCP, que incluye todas las herramientas a las que ha llamado un agente y el texto completo de cualquier script de C# que haya ejecutado. No se registran las indicaciones, las respuestas ni los valores de los datos. **Abrir carpeta de auditoría** en el cuadro de diálogo del servidor y en **Herramientas > Preferencias > Funciones de IA** abre la carpeta de registros. En las ediciones Desktop y Business, no se registra nada y no aparece ninguno de los dos botones.

Consulta @policies para ver la lista completa, la estructura del registro y las plantillas administrativas.

## Resolución de problemas

| Lo que ves | Lo que está pasando |
| -- | -- |
| El agente dice que no tiene herramientas para Tabular Editor | El servidor no está en funcionamiento o el agente se conectó antes de que lo estuviera. Compruebe que en la barra de estado aparezca **MCP iniciado** y, a continuación, vuelva a conectar el agente |
| El agente no puede ver un permiso que acabas de conceder | Los permisos se leen al iniciar el servidor y la lista de herramientas se fija en el momento de la conexión. Detenga e inicie el servidor y, a continuación, vuelva a conectar el agente |
| El agente pierde la conexión después de un largo descanso | El servidor cierra una sesión después de 20 minutos sin solicitudes ni flujos abiertos. Vuelva a conectar el agente |
| El agente informa de que no hay ningún modelo abierto | El servidor se ejecuta independientemente de tu modelo. Abre un modelo en Tabular Editor y vuelve a preguntar. No es necesario reiniciar nada |
| El agente no puede ejecutar consultas DAX | **Datos del modelo** está configurado como **Denegar** de forma predeterminada. Las consultas también necesitan una conexión en vivo: en el caso de un modelo abierto desde el disco, la herramienta de consultas no está disponible independientemente del permiso. |
| Las conexiones se rechazan con un código 401 | La opción **Requerir token de acceso** está activada y el agente no está enviando el token. Vuelva a copiar la configuración de registro del cuadro de diálogo. Incluye el token |
| El puerto ya está en uso | Otra instancia de Tabular Editor u otra aplicación lo está utilizando. Acepte el siguiente puerto libre en el mensaje y actualice el registro del agente. Si la opción **Iniciar el servidor MCP automáticamente** está activada, un conflicto al iniciar no mostrará ningún mensaje y el indicador indicará **MCP detenido** |
| **Herramientas > Servidor MCP...** no aparece en el menú | La opción **Habilitar servidor MCP** está desactivada en las preferencias, el componente de funciones de IA no está instalado, un administrador ha establecido `DisableMcpServer` o `DisableAi`, o se ha establecido un valor de política Enterprise en un equipo que no tiene licencia para ello. Consulte @policies |

## Próximos pasos

- @ai-assistant para conocer el modelo de permisos completo y el chat integrado.
- @unsaved-changes para revisar y revertir lo que ha hecho un agente.
- @csharp-scripts para saber qué puede cambiar un script y, por lo tanto, un agente.
- @policies para gestionar el servidor en toda una organización.
- @te-cli-skill si tu agente trabaja en archivos de modelo en un repositorio o en un pipeline.
