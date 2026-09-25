---
uid: mcp-server
title: Servidor MCP
author: Morten Lønskov
updated: 2026-09-22
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

Tabular Editor 3 puede actuar como servidor MCP (Model Context Protocol). Cualquier agente compatible con MCP, como Claude Code, GitHub Copilot, el modo agente de VS Code, Codex o Cursor, se conecta a la instancia en ejecución y trabaja sobre el modelo semántico que tienes abierto: lo lee, lo consulta, lo analiza y, si se lo permites, lo modifica.

No tienes que configurar ningún proveedor de IA en Tabular Editor para usarlo. No hay ninguna clave de API que pegar ni una segunda suscripción que comprar. La inteligencia viene del agente por el que ya estás pagando, y Tabular Editor aporta lo que ese agente nunca ha tenido: el modelo real, cargado, validado y listo para editar.

## Por qué ejecutar el agente con Tabular Editor

Un agente que edita archivos de modelo en disco trabaja a ciegas. Solo tiene el texto de un archivo `.bim` o de una carpeta TMDL y no tiene forma de saber si el resultado se puede cargar, si el DAX de una medida se resuelve correctamente o qué efecto tuvo el cambio en el resto del modelo. Tabular Editor cierra esa brecha, porque el agente no recibe archivos. Se le entrega el modelo.

- **El modelo tal como lo ves ahora mismo**, con las ediciones no guardadas incluidas. Todo lo que Tabular Editor tiene abierto es lo que ve el agente: un modelo de Power BI Desktop, un proyecto PBIP, una carpeta TMDL, un archivo `.bim`, una base de datos de un Workspace o una conexión en directo a Analysis Services, Azure Analysis Services o Fabric. El agente funciona igual con todos ellos, en línea o sin conexión.
- **El mismo motor que usas tú.** Los cambios del agente pasan por el [wrapper de Tabular Object Model](xref:csharp-scripts) y por el mismo motor de scripting de C#, con la misma validación, la misma corrección de fórmulas y la misma pila de deshacer. Un agente no puede producir un estado del modelo que tú no podrías haber producido manualmente.
- **Análisis que el agente no puede hacer por sí solo.** Los resultados de [Best Practice Analyzer](xref:best-practice-analyzer), las estadísticas del Analizador VertiPaq, los resultados de consultas DAX contra datos en directo y la base de conocimientos de Tabular Editor son herramientas a las que el agente puede recurrir. Deja de hacer suposiciones sobre tu modelo y empieza a medirlo.
- **Un paso de revisión que puedes ver.** Todo lo que hace el agente aparece en tu sesión como cambios no guardados, marcados en el [Explorador TOM y la vista de propiedades](xref:unsaved-changes). Lees el diff en la interfaz, deshaces las partes que no quieres y guardas cuando estás conforme. Nada llega al origen hasta que lo guardas.

Ese último punto marca la diferencia entre delegar trabajo y perder el control sobre él. El agente propone, tu sesión conserva el resultado y eres tú quien lo revisa, lo prueba y lo guarda.

## Antes de empezar

- Tabular Editor 3.27.0 o posterior, en cualquier edición.
- Tener instalado el componente **Funciones de IA**. Forma parte de la instalación predeterminada a partir de la versión 3.27.0. Consulta @installation-activation-basic si despliegas Tabular Editor de forma centralizada, y @policies si tu administrador ha desactivado las funciones de IA.
- Un agente que admita MCP sobre HTTP con streaming.

## Inicia el servidor

1. Elige **Herramientas > Servidor MCP...**.
2. Comprueba los permisos (consulta [Decidir qué puede hacer el agente](#deciding-what-the-agent-may-do) más abajo). La configuración predeterminada permite que un agente lea tu modelo, ejecute el Best Practice Analyzer y trabaje con las pestañas de documentos que tengas abiertas, y evita que lea tus datos o cambie el modelo.
3. Haz clic en **Iniciar servidor**.

El cuadro de diálogo muestra la dirección en la que el servidor está escuchando, `http://127.0.0.1:42100/`, a menos que hayas cambiado el puerto. Un indicador de la barra de estado cambia de **MCP detenido** a **MCP iniciado**, con la dirección en su descripción emergente.

![El cuadro de diálogo Servidor MCP, que muestra la URL del servidor, un token de acceso oculto y las cinco filas de permisos del agente](~/content/assets/images/features/mcp-server/mcp-server-dialog.png)

![El indicador de la barra de estado que muestra MCP iniciado, con su descripción emergente mostrando "El servidor MCP está escuchando en http://127.0.0.1:42100/. Haz clic para abrir el cuadro de diálogo de conexión."](~/content/assets/images/features/mcp-server/status-bar-menu.png)

El servidor funciona tanto con un modelo abierto como sin él. Si un agente se conecta cuando no hay ningún modelo cargado, se le informa de ello en lugar de recibir un error; además, puedes abrir un modelo después sin reiniciar el servidor MCP.

Haz clic con el botón derecho en el indicador de la barra de estado para lo que usarás a diario: iniciar y detener el servidor, copiar una configuración de registro y abrir la página de preferencias. Al hacer clic con el botón izquierdo, se abre el cuadro de diálogo sin cambiar el estado del servidor.

![El indicador de MCP en la barra de estado con el menú del clic derecho abierto, mostrando Detalles del servidor MCP..., Detener servidor MCP, Copiar configuración de MCP y Preferencias del servidor MCP..., y el submenú Copiar configuración de MCP desplegado con Claude Code, VS Code, Copilot CLI, Codex y Cursor](~/content/assets/images/features/mcp-server/status-bar-context-menu.png)

### Preferencias de MCP

Abre **Herramientas > Preferencias > Funciones de IA > Servidor MCP**. Aquí puedes ajustar las preferencias del servidor MCP; por ejemplo, para que se inicie automáticamente al arrancar.

![Preferencias del servidor MCP, mostrando Habilitar servidor MCP, Iniciar servidor MCP automáticamente, Requerir token de acceso y el puerto](~/content/assets/images/pref-mcp-server.png)

| Preferencia                              | Predeterminado | Qué hace                                                                                                                                                                                           |
| ---------------------------------------- | -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Habilitar servidor MCP**               | Activado       | Al desmarcarlo, se detiene el servidor en ejecución y se eliminan el elemento del menú y el indicador de la barra de estado                                                                        |
| **Iniciar servidor MCP automáticamente** | Desactivado    | Inicia el servidor cuando se abre Tabular Editor, para que tu agente pueda conectarse sin que tengas que pensar en ello                                                                            |
| **Requerir token de acceso**             | Desactivado    | Exige que los agentes presenten el token de acceso que se muestra en el cuadro de diálogo del servidor. Consulta [Ejecución en un equipo compartido](#running-on-a-shared-machine) |
| **Puerto**                               | 42100          | El puerto de loopback en el que escucha el servidor. Cualquier valor entre 1024 y 49151. Cambiarlo invalida los registros de agentes existentes                    |

Marca **Iniciar servidor MCP automáticamente** cuando hayas terminado de experimentar. El registro de un agente apunta a una dirección fija, así que un servidor que siempre está ahí es un servidor del que no tendrás que volver a preocuparte.

## Registra tu agente

Solo tienes que registrar Tabular Editor con tu agente una vez. En el cuadro de diálogo del servidor, selecciona tu agente en **Exportar configuración** y pega el contenido del portapapeles. La configuración incluye la dirección y, si lo has activado, el token de acceso. El servidor se registra con el nombre `tabular-editor`.

![La lista desplegable de configuración de exportación, expandida para mostrar Claude Code, VS Code, Copilot CLI, Codex y Cursor](~/content/assets/images/features/mcp-server/export-configuration.png)

**Claude Code.** Ejecuta el comando copiado en una terminal:

```bash
claude mcp add --transport http tabular-editor http://127.0.0.1:42100/
```

**VS Code**, en tu configuración de MCP:

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

**Copilot CLI**, en `~/.copilot/mcp-config.json`:

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

**Codex**, en `~/.codex/config.toml`:

```toml
[mcp_servers.tabular-editor]
url = "http://127.0.0.1:42100/"
```

**Cursor**, en `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "tabular-editor": {
      "url": "http://127.0.0.1:42100/"
    }
  }
}
```

Con **Requerir token de acceso** activado, cada una de estas opciones también incluye el token, en el formato que requiera cada una. Copia la configuración desde el cuadro de diálogo en lugar de escribirla a mano y obtendrás la correcta.

Cualquier otro cliente MCP también funciona. Apúntalo a `http://127.0.0.1:42100/` a través de HTTP con streaming y añade el mismo encabezado si has exigido el token.

### Comprueba que ha funcionado

Pregúntale a tu agente _¿a qué modelo estoy conectado en Tabular Editor?_ Te responderá con el nombre del modelo, cómo está cargado, si tiene cambios sin guardar y su nivel de compatibilidad. Si no hay ningún modelo abierto, te lo dirá; también es una respuesta correcta.

En Tabular Editor no aparece ningún aviso. Ese es precisamente el objetivo: los permisos ya estaban definidos antes de que el agente se conectara.

## Decidir qué puede hacer el agente

Un agente que se conecta mediante MCP funciona sin supervisión, y tú decides de antemano qué puede hacer a través de Tabular Editor. Esos mismos permisos determinan qué pueden hacer el servidor MCP y el Asistente de IA. Están en el propio cuadro de diálogo **Herramientas > Servidor MCP...**, así que puedes configurarlos cuando vayas a iniciar el servidor, y también en **Herramientas > Preferencias > Funciones de IA > Permisos**, que es la misma configuración en ambos lugares. El agente recibe exactamente las herramientas cubiertas por tus permisos. Cualquier otra cosa ni siquiera se le ofrece.

Al pasar el cursor sobre un permiso, ya sea sobre su etiqueta o sobre su lista desplegable, se describe lo que ese nivel le otorga al agente. Cuando un administrador ha limitado un recurso mediante una [directiva](xref:policies), la lista desplegable es de solo lectura y lo indica.

Hay cinco recursos, cada uno con un nivel de acceso:

| Recurso                    | Predeterminado | Lo que obtiene el agente                                                                                                                                                                                                              |
| -------------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Metadatos del modelo**   | Lectura        | Lectura: tablas, columnas, medidas, expresiones, descripciones, relaciones y estadísticas del Analizador VertiPaq. Escritura: la capacidad de modificar el modelo mediante C# Scripts |
| **Datos del modelo**       | Denegar        | Lectura: resultados de consultas DAX; es decir, valores reales de tu modelo. Requiere una conexión en vivo                                                                                            |
| **Best Practice Analyzer** | Lectura        | Lectura: el conjunto de reglas y los resultados del análisis. Escritura: añadir y modificar reglas                                                                                    |
| **Documentos**             | Escritura      | Lectura: el contenido de tus pestañas abiertas de C# Scripts y consultas DAX. Escritura: crearlos y modificarlos                                                                      |
| **Macros**                 | Escritura      | Lectura: tu biblioteca de macros, con nombres, descripciones y código. El permiso de escritura está reservado para herramientas de edición de macros que todavía no existen                           |

Un permiso de **Escritura** incluye el de lectura; el cuadro de diálogo etiqueta ese nivel como **Lectura/Escritura** para dejarlo claro. Los **Datos del modelo** no tienen nivel de escritura, porque no hay forma de escribir los valores de datos de vuelta en el modelo.

De forma predeterminada, el agente lee tu modelo y ejecuta el Best Practice Analyzer. No puede leer ni un solo valor de datos ni cambiar el modelo. Esos son los dos permisos que aumentas deliberadamente.

Fíjate en lo que los valores predeterminados _sí_ permiten. **Documentos** empieza en Escritura, así que un agente puede crear pestañas de script y de consulta en tu sesión y sobrescribir el contenido de las que ya tengas abiertas. No se ejecuta nada ni llega nada al modelo, pero sigue siendo una operación de escritura, y es el único permiso predeterminado que merece la pena reducir si guardas trabajo en curso en esas pestañas.

Los dos que aumentas deliberadamente merecen una reflexión:

- **Datos del modelo > Lectura** es lo que envía valores de tu modelo a tu agente y, a través de él, al proveedor que use tu agente. Los metadatos describen tu modelo; los datos _son_ tu modelo. Concédelo cuando quieras que el agente contraste su trabajo con cifras reales, y sé consciente de que eso es lo que estás haciendo.
- **Metadatos del modelo > Escritura** es lo que hace que el agente pase de ser un asesor a ser un editor. También es el permiso que más te aporta, y las salvaguardas descritas en [Cómo un agente cambia tu modelo](#how-an-agent-changes-your-model) están ahí para que concederlo sea una decisión razonable.

![La página Permisos de funciones de IA, con un menú desplegable por recurso en su nivel predeterminado](~/content/assets/images/pref-ai-permissions.png)

> [!IMPORTANT]
> Los permisos se leen cuando se inicia el servidor, y un agente recibe su lista de herramientas al conectarse. Después de cambiar un permiso, detén el servidor, vuelve a iniciarlo y luego vuelve a conectar el agente. Hasta que lo hagas, el agente seguirá trabajando con los permisos que estaban en vigor cuando se conectó.

## Qué puede hacer el agente

Cuando un agente se conecta, Tabular Editor le ofrece un conjunto de capacidades en función de los permisos que le hayas concedido. No tienes que invocar nada de esto manualmente. Lo importante es saber qué puedes pedir y de qué permiso depende cada solicitud, porque una capacidad que tus permisos no cubren nunca se ofrece de entrada, en lugar de rechazarse a mitad de una tarea.

**Orientarse.** Cualquier agente puede identificar la instancia con la que está hablando y el modelo que esa instancia tiene abierto, buscar en la documentación y el blog de Tabular Editor, en los issues y las discusiones de GitHub, y consultar la API de scripting: las propiedades, los métodos y las firmas disponibles en los objetos del modelo. Nada de eso toca tu modelo, así que nada de eso necesita un permiso.

Esa última parte importa más de lo que parece. Por eso, cuando un agente escribe un script de Tabular Editor, no tiene que inventarse de memoria propiedades, funciones ni APIs. Consulta la firma en la versión que estás ejecutando.

**Leer el modelo.** Con **Metadatos del modelo > Lectura**, que es la opción predeterminada, un agente puede obtener una visión general de tus tablas, de cuántas columnas y medidas tiene cada una, y de todas las relaciones; obtener el detalle completo de los objetos que mencione, incluidas expresiones, descripciones, cadenas de formato y tipos de datos; y buscar en el modelo por nombre, descripción, expresión DAX o M, cadena de formato o anotación. También puede solicitar el modelo completo, aunque es costoso, y se le advierte de ello.

También puede ver lo que has seleccionado en el Explorador TOM. Merece la pena saberlo: selecciona tres medidas, por ejemplo _da formato coherente a estas_, y el agente entiende a qué se refiere "estas".

**Medir el modelo.** **Best Practice Analyzer > Leer** permite a un agente enumerar las reglas vigentes, incluidas las tuyas, y ejecutar el análisis para devolver infracciones reales. **Best Practice Analyzer > Escribir** permite agregar o cambiar reglas en tu colección local. Las estadísticas del Analizador VertiPaq, es decir, tamaños de tablas, cardinalidades de columnas y uso de memoria, se incluyen en **Metadatos del modelo > Leer**. Ejecutar una consulta DAX y recibir filas requiere **Datos del modelo > Leer** además del acceso a metadatos, y devuelve un número limitado de filas en lugar de un conjunto de resultados sin límite.

_Ejecutar el Best Practice Analyzer y corregir lo que encuentre_ es, con diferencia, lo más útil que puedes delegar aquí, porque el agente obtiene una lista concreta de problemas reales de tu modelo en lugar de consejos genéricos sobre modelos semánticos.

> [!NOTE]
> Consultar datos requiere una conexión activa, y las estadísticas de VertiPaq requieren una conexión o estadísticas que ya hayas recopilado. Ambas quedan resueltas cuando el agente se conecta, así que si conectas el modelo después, vuelve a conectar el agente para que las tenga en cuenta.

**Tus documentos y macros.** Enumerar las pestañas abiertas de scripts y consultas solo requiere acceso a metadatos. Leer su contenido requiere **Documentos > Leer**. Editar una pestaña o ponerte delante un nuevo C# Script o una consulta DAX para revisarlos requiere **Documentos > Escribir**. Todo lo que un agente te entregue de esta forma se compila o se valida con el modelo abierto antes de que lo veas, así que ya ha tenido la oportunidad de corregir sus propios errores; para que esa validación se produzca, una consulta DAX necesita que Tabular Editor esté conectado a Analysis Services o Power BI. Tu biblioteca de macros es un recurso independiente y se lee con **Macros > Leer**.

**Cambiar el modelo.** Eso requiere **Metadatos del modelo > Escribir**, y funciona lo bastante distinto de todo lo anterior como para merecer su propia sección. Consulta [Cómo un agente cambia tu modelo](#how-an-agent-changes-your-model) más abajo.

## Cómo un agente cambia tu modelo

Con **Metadatos del modelo > Escribir**, un agente puede cambiar tu modelo directamente. Para ello, crea en segundo plano un [C# Script](xref:csharp-scripts) que Tabular Editor compila, comprueba por seguridad y ejecuta sobre el modelo abierto.

No hay una segunda vía, y eso es deliberado. Todo lo que la API de scripting de C# puede hacerle a un modelo puede pedirse por esta vía, así que no hay una lista cerrada de operaciones admitidas que pueda quedarse corta: medidas, columnas, grupos de cálculo, perspectivas, traducciones, relaciones, políticas de actualización, cambios de nombre masivos, pasadas de formato. Y como todos los cambios llegan de la misma forma, hay un único punto donde se aplican la seguridad y la revisión, en lugar de uno por operación. Esa capa intermedia es lo que hace que las ediciones del agente sean revisables:

- **Un solo paso de deshacer.** Todo lo que hizo un script se agrupa en una sola entrada de la pila de deshacer, independientemente de lo que haya tocado. Un solo **Ctrl+Z** devuelve el modelo a su estado anterior. Ver @undo-redo.
- **Todo o nada.** Si un script produce una excepción a mitad de ejecución, se revierte por completo. Nunca heredas una edición a medias.
- **Un resumen estructurado.** El agente recibe una descripción de cada objeto que agregó, modificó o eliminó, además de todo lo que imprimió el script. Puede decirte lo que hizo sin tener que adivinar, y puede detectar cuándo hizo algo distinto de lo que pretendía.
- **Nada te hace esperar.** Un mensaje que un script normalmente mostraría en pantalla, mediante `Output`, `Info`, `Warning` o `Error`, se devuelve al agente como parte del resultado, en lugar de interrumpir la llamada con un cuadro de diálogo que nadie está viendo. Mientras se ejecuta una llamada larga, Tabular Editor muestra un indicador de **Espere, por favor** e ignora los clics, para que no puedas trabajar en la ventana sobre un modelo que está cambiando por debajo y para que los clics no se acumulen ni se ejecuten en cuanto el agente termine.
- **Marcado en la interfaz de usuario.** Los objetos y las propiedades modificados aparecen con color e indicadores en el [Explorador TOM y la vista de propiedades](xref:unsaved-changes) hasta que guardes. Usa **Mostrar cambios** para filtrar ambas vistas y dejar solo el trabajo del agente, y haz clic con el botón derecho en **Revertir** para deshacer una sola propiedad, un solo objeto o una rama completa sin tocar el resto.

![El menú Edición abierto en una única entrada de deshacer de C# Script (MCP), con el Explorador TOM al lado marcando una medida agregada en verde, una medida modificada en naranja y una medida eliminada tachada en rojo, y la vista de propiedades filtrada para mostrar la única propiedad que cambió el agente](~/content/assets/images/features/mcp-server/agent-change-review.png)

Ese es el ciclo de revisión: solicita, observa cómo se aplica, filtra lo que cambió, revierte lo que no te convenza y guarda. Estás revisando un diff en la herramienta que ya conoces, no leyendo un resumen y cruzando los dedos.

El chat del [Asistente de IA](xref:ai-assistant) puede ejecutar scripts de la misma manera, y cuenta con el mismo único paso de deshacer y la misma reversión. Hay dos cosas que siguen siendo específicas de un agente. Nunca se le pide confirmación, así que no hay cuadro de diálogo de vista previa ni un **Cancelar** al que recurrir; los cambios marcados en el árbol son tu paso de revisión, a posteriori en lugar de antes. Y su entrada de deshacer se llama _C# Script (MCP)_, para que puedas distinguir el trabajo de un agente del del chat en la lista desplegable de deshacer.

### Lo que un agente nunca puede hacer

Algunas cosas quedan fuera, independientemente de los permisos que tengas concedidos:

- **Ejecución directa de TMSL y XMLA.** `ExecuteCommand` siempre falla en un script ejecutado por un agente. Omite el modelo de objetos, así que no se puede deshacer ni revertir, lo que lo hace incompatible con todas las garantías anteriores.
- **Cualquier cosa fuera del modelo.** Un script que acceda al sistema de archivos, haga una solicitud web o haga referencia a un ensamblado externo nunca se ejecuta para un agente. En su lugar, se abre como un documento **Script de agente (revisión)** en Tabular Editor, y se informa al agente de que tienes que revisarlo y ejecutarlo tú mismo. Esto requiere el permiso **Documentos > Escritura**; sin él, el script se rechaza sin más. La comprobación es un análisis semántico del script compilado, no un escaneo de su texto, así que también se rechazan las rutas indirectas hacia esos mismos destinos, mediante reflection, árboles de expresiones, `Activator`, `AppDomain`, lectores XML o deserialización.
- **Consultar datos para los que no tiene permiso.** Las funciones auxiliares de DAX dentro de un script están controladas por **Datos del modelo > Lectura**, exactamente igual que la herramienta de consulta, así que un agente no puede acceder a los datos envolviendo una consulta en un script.

### Pedir un borrador en lugar de un cambio

Un agente no tiene por qué ejecutar nada. Con **Documentos > Escribir** puedes insertar un **C# Script** o una consulta DAX en un documento de Tabular Editor para que puedas leerlo y ejecutarlo tú mismo. El script se compila y la consulta se valida con tu modelo antes de que lo veas; los errores se envían de vuelta al agente, que puede corregir el documento allí mismo.

Este es el modo adecuado para un cambio que quieres inspeccionar antes de que ocurra, o para un trabajo que prefieres ejecutar más tarde en otro modelo.

## Una sesión de trabajo

El ciclo es: abrir el modelo, pedir algo, ver cómo aparece, revisarlo y guardarlo. Así se ve en la práctica.

**Empieza por lo que está mal.** Abre un modelo que hayas heredado y pregunta:

> Ejecuta el Best Practice Analyzer y dime qué merece la pena corregir, empezando por lo peor.

El agente ejecuta el análisis, obtiene incumplimientos reales con nombres de objetos reales y razona sobre tu modelo en lugar de sobre modelos semánticos en general. A continuación, pide _corrige los incumplimientos de las cadenas de formato_ y, con **Metadatos del modelo > Escribir** concedido, escribe un único script y lo ejecuta. El Explorador TOM se llena de insignias naranjas. Haz clic en **Mostrar cambios** en la [vista de propiedades](xref:unsaved-changes) para ver el antes y el después de cada propiedad; en las dos con las que no estés de acuerdo, haz clic con el botón derecho, selecciona **Revertir** y guarda.

**Empieza por un requisito.** Indica al agente una especificación, un ticket o una hoja de cálculo con definiciones de medidas:

> Añade las medidas de requirements.md a la tabla Sales. Sigue la nomenclatura y las cadenas de formato que ya se usan allí.

Primero lee las medidas existentes, para que las nuevas encajen con lo que ya hay en el modelo en lugar de con una convención inventada por él.

El archivo de requisitos proviene del Workspace de tu agente; no pasa por Tabular Editor. Ese reparto lo es todo: tu agente aporta el contexto que ya tiene sobre tu proyecto y Tabular Editor aporta el modelo que nunca podría ver.

**Pídele que compruebe su propio trabajo.** Concede **Datos del modelo > Leer** y el agente podrá verificar en lugar de afirmar:

> Confirma que la nueva medida Margin % da el mismo total que el cálculo anterior para 2025.

Escribe el DAX, lo ejecuta y compara. Este es el permiso que convierte _He añadido la medida_ en _He añadido la medida y aquí tienes los números_.

**Pide un borrador cuando no quieras un cambio.** Siempre que prefieras leerlo primero:

> Escríbeme un script que renombre todas las medidas a tipo oración, pero no lo ejecutes.

El script llega como un documento en Tabular Editor, compilado y revisado por seguridad, y lo ejecutas tú mismo después de haberlo leído.

Hay dos hábitos que hacen que todo esto vaya mejor. Indica a qué instancia te refieres cuando haya más de una abierta: el agente puede preguntar a una instancia qué modelo tiene, pero no puede leerte la mente para saber cuál querías decir. Y guarda, o al menos revisa, entre tareas: los cambios sin guardar se acumulan, y un diff más pequeño se revisa más rápido.

## Ejecutar varias instancias

Cada instancia de Tabular Editor aloja su propio servidor en su propio puerto, así que puedes ejecutar un agente contra un modelo y un segundo agente contra otro.

Inicia la segunda instancia, abre **Tools > MCP Server...** y haz clic en **Start server**. El puerto configurado ya está ocupado, así que Tabular Editor ofrece el siguiente libre que encuentre entre los 20 puertos siguientes. Si todos esos puertos están ocupados, te muestra un Report del conflicto y eliges tú mismo un puerto en las preferencias. Nunca cambia de puerto silenciosamente, porque los registros de tus agentes apuntan a una dirección fija y un cambio silencioso los rompería.

Registra el segundo puerto en tu agente con su propio nombre y sé explícito en tus prompts sobre a cuál te refieres.

## Ejecutar en un equipo compartido

El servidor se vincula a `127.0.0.1`, así que nada en otra máquina puede acceder a él. Además, se rechazan las solicitudes del navegador con una cabecera `Origin` no local, como defensa frente al DNS rebinding.

Sin embargo, el loopback es una barrera más débil de lo que parece. Mientras el token esté desactivado, cualquier proceso que se ejecute en el equipo puede conectarse sin credenciales, y en un host en el que varias personas tienen sesión iniciada a la vez, por ejemplo, un servidor de Escritorio remoto o Citrix, eso incluye las sesiones de otras personas.

Marca **Require access token** en **Tools > Preferences > AI Features > MCP Server** y reinicia el servidor. Entonces, los agentes deben presentar el token que se muestra en el cuadro de diálogo del servidor, y las configuraciones de registro que copias desde ese cuadro de diálogo lo incluyen. Las solicitudes sin él se rechazan.

El botón de actualización junto al token, con el tooltip **Regenerate token**, genera uno nuevo. Eso invalida a propósito todos los registros existentes y reinicia el servidor si está en ejecución; úsalo cuando creas que alguien ha visto un token que no debía ver y vuelve a registrar tus agentes después.

Los administradores pueden hacer que el token sea obligatorio para todos con la directiva `RequireMcpAccessToken`, que además bloquea esa preferencia. Consulta @policies.

## Qué sale de tu equipo

Tabular Editor no se comunica con ningún proveedor de IA cuando trabajas de esta manera. Responde a las llamadas de herramientas desde un proceso en tu propia máquina, a través de una conexión de loopback, y la base de conocimientos en la que busca el agente es una base de datos local que se incluye con la aplicación y se actualiza desde el propio servicio de Tabular Editor.

Es tu agente quien se comunica con un proveedor, bajo tu propia suscripción y las condiciones de ese proveedor. Así que la cuestión de qué se envía y a quién se resuelve en el mismo lugar donde ya la resuelves para cualquier otro repositorio en el que trabaje tu agente. Lo que puedes controlar del lado de Tabular Editor son los permisos concedidos: **Datos del modelo > Denegar**, la opción predeterminada, significa que ningún valor de tu modelo puede llegar al agente en primer lugar, pida lo que pida.

Consulta @security-privacy para obtener una visión más amplia, incluido el [AI Assistant](xref:ai-assistant), que sí llama directamente a un proveedor y se configura por separado.

## Controles de administrador

El servidor MCP está activado de forma predeterminada y cualquier usuario puede desactivarlo. Los administradores pueden hacer aún más:

- `DisableMcpServer` elimina por completo la característica, sin afectar al chat de AI Assistant.
- `DisableAi` desactiva toda la funcionalidad de IA, incluido el servidor MCP, y evita que el componente de IA se instale en la máquina cuando se ejecuta el instalador.
- `RequireMcpAccessToken` obliga a usar autenticación mediante token.
- `DisableCSharpScripts` impide que un agente ejecute un C# Script y también que redacte uno por ti en un documento. Escribir una consulta DAX, y todo lo que sea solo de lectura, no se ve afectado.
- `BlockUnsafeScripts` mantiene los scripts ejecutados por el agente, pero solo permite los que permanecen dentro del modelo. Es el mismo límite con el que ya opera el agente, aplicado a todos los scripts de Tabular Editor en lugar de solo a los scripts del agente, y se aplica independientemente de lo que solicite el agente. Nivel Enterprise.
- Un conjunto de directivas de nivel Enterprise limita hasta dónde pueden llegar AI Assistant y el servidor MCP en cada recurso. Los límites `Max...` se aplican a ambas interfaces; los límites `McpMax...` se aplican solo al servidor MCP y solo pueden rebajar el compartido, de modo que a un agente desatendido nunca se le permite más que al chat interactivo. Ese mismo nivel incluye la ubicación y la retención del registro de auditoría, así como el bloqueo del proveedor de IA.

> [!WARNING]
> Las políticas de nivel Enterprise fallan de forma segura, con denegación por defecto. Si cualquiera de esos nombres de valor está presente en una máquina cuya licencia no es Enterprise, Consultancy o Trial, AI Assistant y el servidor MCP no se inician, y el elemento de menú y el indicador de la barra de estado desaparecen. Un único valor establecido en un parque mixto desactiva la característica para todos los que tengan la edición incorrecta, así que implementa estas directivas en función de las licencias que realmente tengas. Consulta @policies.

En la Edición Enterprise, Tabular Editor también mantiene un registro local de lo que hicieron AI Assistant y el servidor MCP, incluidas todas las herramientas que un agente invocó y el texto completo de cualquier C# Script que ejecutó. Los prompts, las respuestas y los valores de los datos nunca se registran. La opción **Abrir carpeta de auditoría**, tanto en el cuadro de diálogo del servidor como en **Herramientas > Preferencias > Funciones de IA**, te lleva a ella. En Desktop y Business no se registra nada y no se muestra ninguno de los dos botones. Consulta @ai-audit-log.

Consulta @policies para ver la lista completa, la estructura del registro y las plantillas administrativas, y @security-privacy para saber qué sale de tu equipo.

## Solución de problemas

| Lo que ves                                                                                               | Qué ocurre                                                                                                                                                                                                                                                                                                                                                                 |
| -------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| El agente dice que no tiene herramientas para Tabular Editor                                             | El servidor no está en ejecución, o el agente se conectó antes de que arrancara. Comprueba que en la barra de estado aparezca **MCP Started** y, después, vuelve a conectar el agente                                                                                                                                                                      |
| El agente no puede ver un permiso que acabas de conceder                                                 | Los permisos se leen al iniciar el servidor y la lista de herramientas queda fijada en el momento de la conexión. Detén el servidor y vuelve a iniciarlo; luego vuelve a conectar el agente                                                                                                                                                                |
| El agente deja de responder tras una pausa prolongada                                                    | Una sesión sin tráfico durante 20 minutos se cierra. Vuelve a conectar el agente                                                                                                                                                                                                                                                                           |
| El agente reporta que no hay ningún modelo abierto                                                       | El servidor se ejecuta de forma independiente de tu modelo. Abre un modelo en Tabular Editor y vuelve a preguntar; no necesitas reiniciar nada                                                                                                                                                                                                             |
| El agente no puede ejecutar consultas DAX                                                                | De forma predeterminada, **Datos del modelo** está configurado como **Denegar**. Además, requiere una conexión en vivo: con un modelo abierto desde el disco, la herramienta de consultas no está disponible, independientemente de lo que indique el permiso                                                                              |
| Las conexiones se rechazan con un 401                                                                    | **Requerir token de acceso** está activada y el agente no está enviando el token. Vuelve a copiar la configuración de registro desde el cuadro de diálogo, que incluye el token                                                                                                                                                                            |
| El puerto ya está en uso                                                                                 | Lo está usando otra instancia de Tabular Editor u otra aplicación. Acepta el siguiente puerto libre que ofrezca Tabular Editor y actualiza el registro del agente. Con **Iniciar automáticamente el servidor MCP** activado, un conflicto al arrancar pasa desapercibido: el indicador simplemente muestra **MCP Stopped** |
| **Herramientas > Servidor MCP...** no aparece en el menú | **Enable MCP Server** está desmarcado en las preferencias, el componente de funciones de IA no está instalado, un administrador ha establecido `DisableMcpServer` o `DisableAi`, o se ha configurado un valor de directiva de nivel Enterprise en un equipo que no tiene licencia para ello. Consulta @policies                               |

## Pasos a seguir

- @ai-assistant para consultar el modelo de permisos completo y para el chat si prefieres no usar tu propio agente.

- @unsaved-changes para revisar y revertir lo que hizo un agente.

- @csharp-scripts para ver lo que puede hacer un script, que marca el límite de lo que un agente puede hacer en tu modelo.

- @policies para administrar el servidor en toda la organización.

- @te-cli-skill si tu agente trabaja con archivos de modelo en un repositorio o una canalización, en lugar de en un modelo que tienes abierto.
