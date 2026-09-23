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

Tabular Editor 3 puede actuar como un servidor MCP (Model Context Protocol). Cualquier agente que hable MCP, como Claude Code, GitHub Copilot, el modo agente de VS Code, Codex o Cursor, se conecta a la instancia en ejecución y trabaja sobre el modelo semántico que tienes abierto: lo lee, lo consulta, lo analiza y, si se lo permites, lo modifica.

No necesitas configurar un proveedor de IA en Tabular Editor para usar esto. No tienes que pegar ninguna clave de API ni comprar una segunda suscripción. La inteligencia viene del agente por el que ya estás pagando, y Tabular Editor le proporciona lo que ese agente nunca ha tenido: el modelo real, cargado, validado y listo para editar.

## Por qué ejecutar el agente con Tabular Editor

Un agente que edita archivos del modelo en disco trabaja a ciegas. Tiene el texto de un `.bim` o de una carpeta TMDL, y no tiene forma de saber si el resultado se puede cargar, si el DAX de una medida se valida correctamente o qué efecto tiene el cambio en el resto del modelo. Tabular Editor cierra esa brecha, porque al agente no se le entregan archivos. Se le entrega el modelo.

- **El modelo tal como está ante ti**, incluidos los cambios sin guardar. Lo que Tabular Editor tiene abierto es lo que ve el agente: un modelo de Power BI Desktop, un proyecto PBIP, una carpeta TMDL, un archivo `.bim`, una base de datos en un Workspace o una conexión activa a Analysis Services, Azure Analysis Services o Fabric. El agente funciona igual con todos ellos, en línea o sin conexión.
- **El mismo motor que usas tú.** Los cambios del agente pasan por el [wrapper de Tabular Object Model](xref:csharp-scripts) y por el mismo motor de C# Script, con la misma validación, el mismo ajuste automático de fórmulas y el mismo historial de deshacer. Un agente no puede producir un estado del modelo que tú no pudieras haber producido a mano.
- **Análisis que el agente no puede hacer por sí solo.** Los resultados de [Best Practice Analyzer](xref:best-practice-analyzer), las estadísticas del Analizador VertiPaq, los resultados de consultas DAX sobre datos en vivo y la base de conocimiento de Tabular Editor son herramientas que el agente puede utilizar. Deja de hacer suposiciones sobre tu modelo y empieza a medirlo.
- **Un paso de revisión que puedes ver.** Todo lo que hace el agente aparece en tu sesión como cambios no guardados, marcados en el [Explorador TOM y la vista de propiedades](xref:unsaved-changes). Puedes revisar el diff en la interfaz de usuario, revertir las partes que no quieras y guardar cuando estés conforme. Nada llega al origen hasta que lo guardes.

Ese último punto marca la diferencia entre delegar trabajo y perder el control sobre él. El agente propone, tu sesión conserva el resultado y tú eres quien lo comprueba, lo prueba y lo guarda.

## Antes de empezar

- Tabular Editor 3.27.0 o posterior, cualquier edición.
- El componente **Funciones de IA** instalado. Forma parte de la instalación predeterminada a partir de la versión 3.27.0. Consulta @installation-activation-basic si implementas Tabular Editor de forma centralizada, y @policies si tu administrador ha desactivado las funciones de IA.
- Un agente compatible con MCP a través de HTTP con streaming.

## Iniciar el servidor

1. Elige **Herramientas > Servidor MCP...**.
2. Revisa los permisos (consulta [Decidir qué puede hacer el agente](#deciding-what-the-agent-may-do) más abajo). La configuración predeterminada permite que un agente lea tu modelo, ejecute el Best Practice Analyzer y trabaje con las pestañas de documentos que tengas abiertas, y evita que lea tus datos o modifique el modelo.
3. Haz clic en **Iniciar servidor**.

El cuadro de diálogo muestra la dirección en la que el servidor está escuchando, `http://127.0.0.1:42100/`, a menos que hayas cambiado el puerto. Un indicador de la barra de estado cambia de **MCP detenido** a **MCP iniciado** y muestra la dirección en su información sobre herramientas.

![Cuadro de diálogo Servidor MCP, que muestra la URL del servidor, un token de acceso enmascarado y las cinco filas de permisos del agente](~/content/assets/images/features/mcp-server/mcp-server-dialog.png)

![Indicador de la barra de estado de MCP que muestra MCP Started, con su descripción emergente mostrando "El servidor MCP está escuchando en http://127.0.0.1:42100/. Haz clic para abrir el cuadro de diálogo de conexión."](~/content/assets/images/features/mcp-server/status-bar-menu.png)

El servidor funciona con o sin un modelo abierto. Si un agente se conecta cuando no hay ningún modelo cargado, se le informa de ello en lugar de recibir un error, y después puedes abrir un modelo sin reiniciar el servidor MCP.

Haz clic con el botón derecho en el indicador de la barra de estado para las tareas del día a día: iniciar y detener el servidor, copiar una configuración de registro y abrir la página de preferencias. Al hacer clic con el botón izquierdo, se abre el cuadro de diálogo sin cambiar el estado de ejecución del servidor.

![El indicador de MCP en la barra de estado, con el menú contextual abierto con las opciones Detalles del servidor MCP..., Detener servidor MCP, Copiar configuración de MCP y Preferencias del servidor MCP..., y el submenú Copiar configuración de MCP desplegado para mostrar Claude Code, VS Code, Copilot CLI, Codex y Cursor](~/content/assets/images/features/mcp-server/status-bar-context-menu.png)

### Preferencias de MCP

Abre **Herramientas > Preferencias > Funciones de IA > Servidor MCP**. Aquí puedes configurar las preferencias del servidor MCP para, por ejemplo, iniciarlo automáticamente al iniciar.

![Preferencias del servidor MCP, con las opciones Habilitar servidor MCP, Iniciar el servidor MCP automáticamente, Requerir token de acceso y el puerto](~/content/assets/images/pref-mcp-server.png)

| Preferencia                                 | Predeterminado | Qué hace                                                                                                                                                                                               |
| ------------------------------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Habilitar servidor MCP**                  | Activado       | Al desmarcarlo, se detiene cualquier servidor en ejecución y se eliminan el elemento de menú y el indicador de la barra de estado                                                                      |
| **Iniciar el servidor MCP automáticamente** | Desactivado    | Inicia el servidor cuando se inicia Tabular Editor, para que tu agente pueda conectarse sin que tengas que pensar en ello                                                                              |
| **Requerir token de acceso**                | Desactivado    | Obliga a los agentes a proporcionar el token de acceso que se muestra en el cuadro de diálogo del servidor. Consulta [Ejecución en un equipo compartido](#running-on-a-shared-machine) |
| **Puerto**                                  | 42100          | El puerto de loopback en el que escucha el servidor. Cualquier valor entre 1024 y 49151. Cambiarlo invalida los registros de agentes existentes                        |

Marca **Iniciar el servidor MCP automáticamente** cuando hayas terminado de experimentar. Un registro de agente apunta a una dirección fija, así que si el servidor está siempre disponible, no tendrás que volver a pensar en él.

## Registra a tu agente

Solo tienes que registrar Tabular Editor con tu agente una vez. En el cuadro de diálogo del servidor, selecciona tu agente en **Exportar configuración** y pega lo que se copie en el portapapeles. La configuración incluye la dirección y, si has activado esa opción, el token de acceso. El servidor se registra con el nombre `tabular-editor`.

![El menú desplegable de configuración de exportación, desplegado para mostrar Claude Code, VS Code, Copilot CLI, Codex y Cursor](~/content/assets/images/features/mcp-server/export-configuration.png)

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

Con **Requerir token de acceso** activado, cada una de estas opciones también incluye el token de acceso, en el formato que corresponda. Copia la configuración del cuadro de diálogo en lugar de escribirla a mano para asegurarte de que sea la correcta.

Cualquier otro cliente MCP también funciona. Apúntalo a `http://127.0.0.1:42100/` a través de HTTP streamable y añade el mismo encabezado si has configurado el token como obligatorio.

### Comprueba que ha funcionado

Pregúntale a tu agente _¿a qué modelo estoy conectado en Tabular Editor?_ Te responderá con el nombre del modelo, cómo se carga, si tiene cambios sin guardar y su nivel de compatibilidad. Si no hay ningún modelo abierto, lo indica; también es una respuesta correcta.

Tabular Editor no te muestra ningún aviso. Esa es la idea: los permisos quedaron definidos antes de que el agente se conectara.

## Decidir qué puede hacer el agente

Un agente que se conecta a través de MCP funciona sin supervisión y tú decides de antemano qué puede hacer en Tabular Editor. Los mismos permisos determinan lo que pueden hacer el servidor MCP y el Asistente de IA. Están en el propio cuadro de diálogo **Herramientas > Servidor MCP...**, así que puedes configurarlos al iniciar el servidor. También están en **Herramientas > Preferencias > Funciones de IA > Permisos**, que es la misma configuración en ambos lugares. El agente recibe exactamente las herramientas incluidas en tus permisos. Nunca se le ofrece nada más.

Al pasar el cursor sobre un permiso, ya sea sobre su etiqueta o sobre su lista desplegable, se muestra qué le proporciona ese nivel al agente. Cuando un administrador ha limitado un recurso mediante [una directiva](xref:policies), la lista desplegable es de solo lectura y así lo indica.

Hay cinco recursos, cada uno con un nivel de acceso:

| Recurso                    | Predeterminado | Lo que recibe el agente                                                                                                                                                                                                             |
| -------------------------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Metadatos del modelo**   | Lectura        | Lectura: tablas, columnas, medidas, expresiones, descripciones, relaciones y estadísticas del Analizador VertiPaq. Escritura: la capacidad de cambiar el modelo mediante C# Scripts |
| **Datos del modelo**       | Denegar        | Lectura: resultados de consultas DAX, es decir, valores reales de tu modelo. Requiere una conexión activa                                                                                           |
| **Best Practice Analyzer** | Lectura        | Lectura: el conjunto de reglas y los resultados del análisis. Escritura: agregar y modificar reglas                                                                                 |
| **Documentos**             | Escritura      | Lectura: el contenido de las pestañas de C# Script y de consultas DAX que tengas abiertas. Escritura: crearlas y modificarlas                                                       |
| **macros**                 | Escritura      | Lectura: tu biblioteca de macros, con nombres, descripciones y código. El nivel de Escritura está reservado para herramientas de edición de macros que aún no existen                               |

Un permiso de **Escritura** incluye Lectura, y el cuadro de diálogo etiqueta ese nivel como **Lectura/Escritura** para dejarlo claro. Los **datos del modelo** no tienen nivel de Escritura, porque no hay forma de escribir valores de datos de vuelta en un modelo.

De forma predeterminada, el agente lee tu modelo y ejecuta el Best Practice Analyzer. No puede leer ningún valor de datos ni cambiar el modelo. Esos son los dos permisos que elevas deliberadamente.

Fíjate en lo que los valores predeterminados _sí_ permiten. **Documentos** empieza en Escritura, así que un agente puede crear pestañas de script y consulta en tu sesión, y sobrescribir el contenido de las que ya tengas abiertas. No se ejecuta nada y nada llega al modelo, pero sigue siendo Escritura, y es el único valor predeterminado que merece la pena reducir si guardas trabajo en curso en esas pestañas.

Los dos que elevas deliberadamente merecen un momento de reflexión:

- **Datos del modelo > Lectura** es lo que envía valores de tu modelo a tu agente y, a través de él, al proveedor que use tu agente. Los metadatos describen tu modelo; los datos _son_ tu modelo. Concédelo cuando quieras que el agente contraste su trabajo con números reales, y ten presente que eso es exactamente lo que estás haciendo.
- **Metadatos del modelo > Escritura** es lo que convierte al agente de asesor en editor. También es el permiso que más valor te aporta, y las salvaguardas descritas en [Cómo un agente cambia tu modelo](#how-an-agent-changes-your-model) existen para que concederlo sea una decisión razonable.

![La página Permisos de funciones de IA, con un menú desplegable por recurso en su nivel predeterminado](~/content/assets/images/pref-ai-permissions.png)

> [!IMPORTANT]
> Los permisos se leen cuando se inicia el servidor, y el agente recibe su lista de herramientas cuando se conecta. Después de cambiar un permiso, detén y vuelve a iniciar el servidor; luego vuelve a conectar el agente. Hasta que lo hagas, el agente seguirá funcionando con los permisos que estaban en vigor cuando se conectó.

## Qué puede hacer el agente

Cuando un agente se conecta, Tabular Editor le ofrece un conjunto de capacidades definido por los permisos que le hayas concedido. No tienes que invocar nada de esto tú mismo. Lo importante es saber qué puedes pedir y de qué permiso depende cada solicitud, porque una capacidad que tus permisos no cubren ni siquiera se ofrece desde el principio, en lugar de rechazarse a mitad de una tarea.

**Orientarse.** Todo agente puede identificar la instancia con la que está hablando y el modelo que esa instancia tiene abierto, buscar en la documentación, el blog, las incidencias y los debates de GitHub de Tabular Editor, y consultar la API de scripting: las propiedades, los métodos y las firmas disponibles en los objetos del modelo. Nada de eso afecta a tu modelo, así que no requiere ningún permiso.

Esa última parte importa más de lo que parece. Por eso, cuando un agente escribe un script de Tabular Editor, no tiene que inventarse propiedades, funciones ni APIs de memoria. Consulta la firma en la versión que estás ejecutando.

**Leer el modelo.** Con **Metadatos del modelo > Lectura**, que es el valor predeterminado, un agente puede obtener una visión general de tus tablas, su recuento de columnas y medidas, y cada relación; obtener todos los detalles de los objetos que nombre, incluidas expresiones, descripciones, cadenas de formato y tipos de datos; y buscar en el modelo por nombre, descripción, expresión DAX o M, cadena de formato o anotación. También puede pedir el modelo completo, aunque eso es costoso y se le advierte de ello.

También puede ver lo que tienes seleccionado en el Explorador TOM. Conviene conocer esto: selecciona tres medidas, di _da formato a estas de forma coherente_, y el agente sabe qué significa «estas».

**Medir el modelo.** **Best Practice Analyzer > Lectura** permite a un agente enumerar las reglas vigentes, incluidas las tuyas, y ejecutar el análisis para obtener incumplimientos reales. **Best Practice Analyzer > Escritura** le permite añadir o cambiar reglas en tu colección local. Las estadísticas del Analizador VertiPaq, es decir, los tamaños de las tablas, las cardinalidades de las columnas y el uso de memoria, se incluyen en **Metadatos del modelo > Lectura**. Ejecutar una consulta DAX y obtener filas requiere **Datos del modelo > Lectura**, además del acceso a los metadatos, y devuelve un número limitado de filas en lugar de un conjunto de resultados sin límite.

_Ejecuta el Best Practice Analyzer y corrige lo que encuentre_ es lo más útil que puedes delegar aquí, porque el agente obtiene una lista concreta de problemas reales en tu modelo en lugar de consejos genéricos sobre modelos semánticos.

> [!NOTE]
> Consultar datos requiere una conexión activa, y las estadísticas de VertiPaq requieren una conexión o estadísticas que ya hayas recopilado. Ambos quedan configurados cuando el agente se conecta, así que, si conectas el modelo después, vuelve a conectar el agente para que los recoja.

**Tus documentos y macros.** Para enumerar las pestañas abiertas de scripts y consultas basta con acceso a metadatos. Para leer su contenido se necesita **Documentos > Leer**. Editar una pestaña o mostrarte un nuevo C# Script o una consulta DAX para que puedas revisarlos requiere **Documentos > Escribir**. Todo lo que un agente te entregue de esta forma se compila o se valida con el modelo abierto antes de que lo veas, por lo que ya ha tenido ocasión de corregir sus propios errores; y, para que esa validación tenga lugar, en el caso de una consulta DAX Tabular Editor debe estar conectado a Analysis Services o Power BI. Tu biblioteca de macros es un recurso independiente y se lee con **Macros > Leer**.

**Cambiar el modelo.** Eso requiere **Metadatos del modelo > Escribir**, y funciona de forma lo bastante distinta de todo lo anterior como para merecer su propia sección. Consulta [Cómo cambia un agente tu modelo](#how-an-agent-changes-your-model) más abajo.

## Cómo cambia un agente tu modelo

Con **Metadatos del modelo > Escribir**, un agente puede cambiar tu modelo directamente, y lo hace creando en segundo plano un [C# Script](xref:csharp-scripts) que Tabular Editor compila, verifica que sea seguro y ejecuta sobre el modelo abierto.

No hay una segunda vía, y es así a propósito. Cualquier cosa que la API de scripting de C# pueda hacer en un modelo se puede solicitar de esta manera, así que no hay una lista cerrada de operaciones compatibles que pueda agotarse: medidas, columnas, grupos de cálculo, perspectivas, traducciones, relaciones, políticas de actualización, cambios de nombre masivos, pasadas de formato. Y, como todos los cambios llegan del mismo modo, la seguridad y la revisión se aplican en un único punto en lugar de uno por operación. Ese paso intermedio es lo que hace revisables las ediciones del agente:

- **Un único paso de deshacer.** Todo lo que hizo un script se agrupa en una sola entrada de la pila de deshacer, sin importar qué haya tocado. Un **Ctrl+Z** devuelve el modelo a su estado anterior. Consulta @undo-redo.
- **Todo o nada.** Si un script genera una excepción a mitad de la ejecución, se revierte por completo. Nunca te quedas con una edición a medias.
- **Un resumen estructurado.** El agente recibe una descripción de cada objeto que añadió, cambió o eliminó, además de cualquier texto que haya emitido el script. Puede decirte lo que hizo sin tener que adivinar, y puede detectar cuándo hizo algo distinto de lo que pretendía.
- **Nada queda pendiente.** Un mensaje que un script normalmente mostraría en pantalla mediante `Output`, `Info`, `Warning` o `Error` se devuelve al agente como parte del resultado, en lugar de detener la llamada con un cuadro de diálogo que nadie está mirando. Mientras se ejecuta una llamada larga, Tabular Editor muestra un indicador de **Espere, por favor** e ignora los clics, de modo que no puedes interactuar con la ventana mientras el modelo se modifica, y los clics no se quedan en cola para ejecutarse en cuanto el agente termina.
- **Marcado en la interfaz.** Los objetos y las propiedades modificados aparecen resaltados y con distintivos en el [Explorador TOM y la vista de propiedades](xref:unsaved-changes) hasta que guardes. Usa **Mostrar cambios** para filtrar ambas vistas y dejar solo el trabajo del agente, y haz clic con el botón derecho en **Revertir** para deshacer una sola propiedad, un solo objeto o una rama completa sin tocar el resto.

![El menú Editar abierto en una única entrada: Deshacer C# Script (MCP), con el Explorador TOM a su lado, que marca una medida añadida en verde, una medida cambiada en naranja y una medida eliminada tachada en rojo, y la vista de propiedades filtrada para mostrar la única propiedad que cambió el agente](~/content/assets/images/features/mcp-server/agent-change-review.png)

Ese es el ciclo de revisión: pide, observa cómo se aplica, filtra lo que cambió, deshaz lo que no apruebes y guarda. Estás revisando un diff en la herramienta que ya conoces, no leyendo un resumen y cruzando los dedos.

El chat del [Asistente de IA](xref:ai-assistant) también puede ejecutar scripts del mismo modo, y ofrece el mismo único paso de deshacer y la misma opción de revertir. Hay dos cosas que siguen siendo específicas de un agente. Nunca se le pide confirmación, así que no hay cuadro de diálogo de vista previa ni **Cancelar** al que recurrir; los cambios marcados en el árbol son tu paso de revisión, a posteriori, no de antemano. Y su entrada de deshacer se llama _C# Script (MCP)_, para que puedas distinguir el trabajo de un agente del del chat en la lista desplegable de deshacer.

### Lo que un agente nunca puede hacer

Hay cosas que quedan descartadas independientemente de tus permisos:

- **Ejecución directa de TMSL y XMLA.** `ExecuteCommand` siempre falla en un script ejecutado por un agente. Omite el modelo de objetos, por lo que no se puede deshacer ni revertir, y eso lo hace incompatible con todas las garantías anteriores.
- **Cualquier cosa fuera del modelo.** Un script que acceda al sistema de archivos, haga una solicitud web o haga referencia a un ensamblado externo nunca se ejecuta cuando lo lanza un agente. En su lugar, se abre como un documento **Agent script (review)** en Tabular Editor, y se le indica al agente que debes revisarlo y ejecutarlo tú mismo. Esto requiere el permiso **Documents > Write**; sin él, el script se rechaza de plano. La comprobación es un análisis semántico del script compilado, no un escaneo de su texto, así que también se rechazan las vías indirectas para llegar a lo mismo, mediante reflexión, árboles de expresiones, `Activator`, `AppDomain`, lectores XML o deserialización.
- **Consultar datos para los que no tiene permiso.** Las funciones auxiliares de DAX dentro de un script dependen del permiso **Model data > Read**, igual que la herramienta de consultas, así que un agente no puede acceder a los datos envolviendo una consulta dentro de un script.

### Pedir un borrador en lugar de un cambio

Un agente no tiene por qué ejecutar nada. Con **Documents > Write** puede poner un C# Script o una consulta DAX en un documento en Tabular Editor para que tú mismo los leas y los ejecutes. El script se compila y la consulta se valida con tu modelo antes de que los veas, y los errores se devuelven al agente, que puede corregir el documento ahí mismo.

Este es el modo adecuado para un cambio que quieres inspeccionar antes de que ocurra, o para un trabajo que prefieres ejecutar más tarde en otro modelo.

## Una sesión de trabajo

El ciclo es: abrir el modelo, pedir algo, ver cómo se aplica, revisarlo y guardarlo. Así es como se ve en la práctica.

**Empieza por lo que está mal.** Abre un modelo heredado y pregunta:

> Ejecuta el Best Practice Analyzer y dime qué merece la pena corregir, empezando por lo más grave.

El agente ejecuta el análisis, obtiene infracciones reales con nombres de objetos reales y razona sobre tu modelo en lugar de sobre los modelos semánticos en general. Después, dile _corrige las infracciones de la cadena de formato_ y, si tiene concedido **Metadatos del modelo > Escritura**, generará un único script y lo ejecutará. El Explorador TOM se llena de insignias naranjas. Haz clic en **Mostrar cambios** en la [vista de propiedades](xref:unsaved-changes) para ver el antes y el después de cada propiedad, haz clic con el botón derecho en **Revertir** en las dos con las que no estés de acuerdo y guarda.

**Empieza por un requisito.** Pásale al agente una especificación, un ticket o una hoja de cálculo con definiciones de medidas:

> Añade las medidas de requirements.md a la tabla Sales. Respeta la nomenclatura y las cadenas de formato que ya se usan allí.

Primero lee las medidas existentes para que las nuevas encajen con lo que ya hay en el modelo, en lugar de seguir una convención que se haya inventado.

El archivo de requisitos procede del Workspace del propio agente, no a través de Tabular Editor. Esa separación es todo el planteamiento: tu agente aporta el contexto que ya tiene sobre tu proyecto, y Tabular Editor aporta el modelo que de otro modo nunca podría ver.

**Pídele que compruebe su propio trabajo.** Concede **Datos del modelo > Lectura** y el agente podrá verificar en lugar de afirmar:

> Confirma que la nueva medida Margin % da el mismo total que el cálculo anterior para 2025.

Escribe el DAX, lo ejecuta y compara. Este es el permiso que convierte _he añadido la medida_ en _he añadido la medida y aquí tienes los números_.

**Pide un borrador cuando no quieras aplicar un cambio.** Siempre que prefieras leerlo primero:

> Escríbeme un script que cambie el nombre de todas las medidas a estilo frase, pero no lo ejecutes.

El script aparece como un documento en Tabular Editor, compilado y con comprobaciones de seguridad, y lo ejecutas tú mismo cuando lo hayas leído.

Dos hábitos hacen que todo esto funcione mejor. Di a qué instancia te refieres cuando haya más de una abierta: el agente puede preguntar a una instancia qué modelo tiene, pero no puede leerte la mente para saber cuál querías decir. Y guarda, o al menos revisa, entre tareas: los cambios sin guardar se acumulan, y un diff más pequeño se revisa más rápido.

## Ejecutar varias instancias

Cada instancia de Tabular Editor aloja su propio servidor en su propio puerto, así que puedes ejecutar un agente contra un modelo y un segundo agente contra otro.

Inicia la segunda instancia, abre **Herramientas > Servidor MCP...** y haz clic en **Iniciar servidor**. El puerto configurado ya está en uso, así que Tabular Editor ofrece el siguiente puerto libre que encuentre entre los 20 puertos siguientes. Si todos están ocupados, se reporta el conflicto y puedes elegir tú mismo un puerto en las preferencias. Nunca cambia a otro puerto de forma silenciosa, porque los registros de tu agente apuntan a una dirección fija y un cambio silencioso los dejaría inservibles.

Registra el segundo puerto en tu agente con su propio nombre y, en tus prompts, especifica claramente a cuál te refieres.

## Ejecución en un equipo compartido

El servidor se enlaza a `127.0.0.1`, por lo que nada en otro equipo puede acceder a él. Además, se rechazan las solicitudes del navegador que llevan una cabecera `Origin` no local, como defensa contra el DNS rebinding.

Sin embargo, el loopback es una barrera más débil de lo que parece. Mientras el token esté desactivado, cualquier proceso que se ejecute en el equipo puede conectarse sin credenciales y, en un host donde varias personas hayan iniciado sesión a la vez, por ejemplo en un servidor de Remote Desktop o Citrix, eso incluye las sesiones de otras personas.

Activa **Requerir token de acceso** en **Herramientas > Preferencias > Funciones de IA > Servidor MCP** y reinicia el servidor. Los agentes deben presentar entonces el token que se muestra en el cuadro de diálogo del servidor, y las configuraciones de registro que copies de ese cuadro de diálogo lo incluyen. Las solicitudes que no lo incluyan se rechazan.

El botón de actualización situado junto al token, con la descripción emergente **Regenerar token**, genera uno nuevo. Eso invalida deliberadamente todos los registros existentes y reinicia el servidor si está en ejecución, así que úsalo cuando sospeches que alguien ha visto un token que no debería, y vuelve a registrar tus agentes después.

Los administradores pueden hacer que el token sea obligatorio para todos con la directiva `RequireMcpAccessToken`, que también bloquea la preferencia. Consulta @policies.

## Qué sale de tu equipo

Tabular Editor no contacta con ningún proveedor de IA cuando trabajas así. Responde a llamadas a herramientas procedentes de un proceso de tu propio equipo, mediante una conexión loopback, y la base de conocimiento que consulta el agente es una base de datos local incluida con la aplicación y actualizada desde el propio servicio de Tabular Editor.

Tu agente es quien se comunica con un proveedor, bajo tu propia suscripción y las condiciones de ese proveedor. Así que la pregunta de qué se envía y a quién se responde del mismo modo que para cualquier otro repositorio en el que trabaje tu agente. En Tabular Editor, lo que puedes controlar son las concesiones de permisos: **Datos del modelo > Denegar**, la opción predeterminada, significa que ningún valor de tu modelo puede llegar al agente en primer lugar, pida lo que pida.

Consulta @security-privacy para obtener una visión más amplia, incluido el [AI Assistant](xref:ai-assistant), que sí llama directamente a un proveedor y se configura por separado.

## Controles del administrador

El servidor MCP está activado de forma predeterminada y cualquier usuario puede desactivarlo. Los administradores disponen de más opciones:

- `DisableMcpServer` elimina la función por completo, dejando intacto el chat de AI Assistant.
- `DisableAi` desactiva toda la funcionalidad de IA, incluido el servidor MCP, y evita que el componente de IA se instale en el equipo cuando se ejecuta el instalador.
- `RequireMcpAccessToken` obliga a usar autenticación mediante token.
- `DisableCSharpScripts` impide que un agente ejecute un C# Script y también que redacte uno para incluirlo en un documento. Escribir una consulta DAX, y todo lo que sea de solo lectura, no se ve afectado.
- `BlockUnsafeScripts` mantiene los scripts ejecutados por agentes, pero solo permite los que se mantienen dentro del modelo. Es el mismo criterio con el que ya trabaja el agente, aplicado a todos los scripts de Tabular Editor en lugar de solo a los scripts de agentes, y se aplica sea cual sea lo que pida el agente. Nivel Enterprise.
- Un conjunto de directivas del nivel Enterprise limita hasta dónde pueden llegar el AI Assistant y el servidor MCP por recurso. Los límites `Max...` se aplican a ambas interfaces; los límites `McpMax...` se aplican solo al servidor MCP y solo pueden reducir el límite compartido, de modo que a un agente desatendido nunca se le permite más que al chat interactivo. El mismo nivel también incluye la ubicación y la retención del registro de auditoría, así como el bloqueo del proveedor de IA.

> [!WARNING]
> Las directivas del nivel Enterprise fallan cerradas. Si cualquiera de los nombres de valor está presente en un equipo cuya licencia no sea Enterprise, Consultancy o Trial, el AI Assistant y el servidor MCP se niegan a iniciarse, y desaparecen la opción de menú y el indicador de la barra de estado. Un solo valor configurado en una flota mixta desactiva la función para todos los que estén en la edición incorrecta, así que implementa estas directivas en función de las licencias que realmente tengas. Consulta @policies.

En la Edición Enterprise, Tabular Editor también mantiene un registro local de lo que hicieron el AI Assistant y el servidor MCP, incluidas todas las herramientas que invocó un agente y el texto completo de cualquier C# Script que ejecutó. Los prompts, las respuestas y los valores de datos nunca se registran. **Abrir carpeta de auditoría**, en el cuadro de diálogo del servidor y en **Herramientas > Preferencias > Funciones de IA**, te lleva a esa carpeta. En las ediciones Desktop y Business no se registra nada y no se muestra ninguno de los dos botones. Consulta @ai-audit-log.

Consulta @policies para ver la lista completa, la estructura del Registro y las plantillas administrativas, y @security-privacy para saber qué sale de tu equipo.

## Solución de problemas

| Qué ves                                                                                                  | Qué ocurre                                                                                                                                                                                                                                                                                                                                                                       |
| -------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| El agente dice que no tiene herramientas para Tabular Editor                                             | El servidor no está en ejecución, o el agente se conectó antes de que lo estuviera. Comprueba que en la barra de estado aparezca **MCP Started**, luego vuelve a conectar el agente                                                                                                                                                                              |
| El agente no puede ver un permiso que acabas de conceder                                                 | Los permisos concedidos se leen al iniciar el servidor y la lista de herramientas queda fijada en el momento de la conexión. Detén y vuelve a iniciar el servidor; luego vuelve a conectar el agente                                                                                                                                                             |
| El agente se queda en silencio tras una pausa larga                                                      | Una sesión sin actividad durante 20 minutos se cierra. Vuelve a conectar el agente                                                                                                                                                                                                                                                                               |
| El agente informa en **Report** que no hay ningún modelo abierto                                         | El servidor se ejecuta de forma independiente de tu modelo. Abre un modelo en Tabular Editor y vuelve a intentarlo; no necesitas reiniciar nada                                                                                                                                                                                                                  |
| El agente no puede ejecutar consultas DAX                                                                | De forma predeterminada, **Model data** está en **Deny**. También necesita una conexión activa: con un modelo abierto desde el disco, la herramienta de consultas no está disponible, independientemente de lo que indique el permiso                                                                                                            |
| Las conexiones se rechazan con un 401                                                                    | **Requerir token de acceso** está activado y el agente no está enviando el token. Vuelve a copiar la configuración de registro del cuadro de diálogo, que la incluye                                                                                                                                                                                             |
| El puerto ya está en uso                                                                                 | Lo está usando otra instancia de Tabular Editor u otra aplicación. Acepta el siguiente puerto libre que ofrezca Tabular Editor y actualiza la configuración de registro del agente. Con **Start MCP server automatically** activado, un conflicto al inicio pasa desapercibido: el indicador simplemente muestra **MCP Stopped** |
| **Herramientas > Servidor MCP...** no aparece en el menú | **Habilitar servidor MCP** está desmarcado en las preferencias, el componente de funciones de IA no está instalado, un administrador ha establecido `DisableMcpServer` o `DisableAi`, o se ha configurado un valor de directiva de nivel Enterprise en un equipo sin la licencia correspondiente. Consulta @policies                                |

## Pasos a seguir

- @ai-assistant para ver el modelo de permisos completo y, si prefieres no usar tu propio agente, para usar el chat.

- @unsaved-changes para revisar y revertir lo que hizo un agente.

- Consulta @csharp-scripts para ver qué puede hacer un script; eso marca el límite de lo que un agente puede hacerle a tu modelo.

- @policies para gestionar el servidor a nivel de toda la organización.

- @te-cli-skill si tu agente trabaja con archivos de modelo en un repositorio o en un pipeline, en lugar de trabajar sobre un modelo que tengas abierto.
