---
uid: preferences
title: Control de preferencias
author: Daniel Otykier
updated: 2026-09-16
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Preferencias de Tabular Editor 3

Los procesos y flujos de trabajo de desarrollo del Data model tabular varían mucho de una organización a otra. Para garantizar que la herramienta pueda encajar en la mayor cantidad posible de estos flujos de trabajo, Tabular Editor 3 es altamente personalizable, no solo en cuanto al aspecto y la experiencia de la interfaz de usuario, sino también en temas más avanzados como servidores proxy web, actualizaciones y comentarios, límites de filas, tiempos de espera, preferencias de comparación de esquemas, etc.

Este artículo describe los cuadros de diálogo de preferencias de Tabular Editor 3 y la configuración que puedes controlar desde ellos.

Para acceder al cuadro de diálogo de preferencias, ve a **Herramientas > Preferencias**.

> [!NOTE]
> Todas las preferencias de Tabular Editor se almacenan para cada perfil de usuario de Windows en la carpeta `%localappdata%\\TabularEditor3`. Puedes migrar tu configuración a otra máquina simplemente copiando el contenido de esta carpeta.

> [!TIP]
> Usa el cuadro de búsqueda en la parte superior del cuadro de diálogo de preferencias para encontrar rápidamente ajustes específicos.

## Tabular Editor > Características

![Preferencias: características generales](~/content/assets/images/pref-general-features.png)

### Power BI

##### _Permitir edición no admitida_ (deshabilitado)

Esta opción solo es relevante cuando Tabular Editor 3 se usa como herramienta externa para Power BI Desktop. Al activarla, todas las propiedades de modelado del Data model de TOM estarán disponibles para editar cuando te conectes a una instancia de Power BI Desktop. Por lo general, se recomienda dejar esta opción desactivada para asegurarte de que no haces cambios accidentalmente en tu archivo de Power BI [que no son compatibles con Power BI Desktop](xref:desktop-limitations).

##### _Ocultar advertencias de fecha/hora automática_ (deshabilitado)

Cuando la marcas, se ocultarán las advertencias sobre las tablas de fecha/hora automática de Power BI. Estas advertencias aparecen cuando la configuración "Fecha/hora automática" de Power BI Desktop está habilitada, lo que crea tablas calculadas que generan advertencias en el analizador de DAX integrado de Tabular Editor 3.

##### _Salto de línea en la primera línea de DAX_ (deshabilitado)

En Power BI Desktop es habitual insertar un salto de línea en la primera línea de una expresión DAX, debido a la forma en que la barra de fórmulas muestra el código DAX. Si alternas con frecuencia entre Tabular Editor y Power BI Desktop, considera habilitar esta opción para que Tabular Editor 3 inserte el salto de línea automáticamente.

##### _Only for multi-line DAX expressions_ (enabled)

Cuando se habilita "Salto de línea en la primera línea de DAX", esta subconfiguración controla si el salto de línea se añade solo a expresiones DAX de varias líneas. Si se selecciona, las expresiones de una sola línea se dejan sin cambios.

##### _Modo de autenticación predeterminado de Power BI_ (Integrada)

Selecciona el método de autenticación predeterminado (Integrada, ServicePrincipal o MasterUser) que se usará al conectarte a Datasets de Power BI.

### Best Practice Analyzer

##### _Buscar infracciones de prácticas recomendadas en segundo plano_ (habilitado)

Si se desactiva, tendrás que ejecutar explícitamente un análisis de prácticas recomendadas desde la ventana de la herramienta Best Practice Analyzer para comprobar si hay alguna infracción. Si la activas, el análisis se ejecuta continuamente en un subproceso en segundo plano cada vez que haces cambios. Para modelos muy grandes o modelos con reglas de prácticas recomendadas muy complejas, esto puede causar problemas.

##### _Reglas BPA integradas_ (habilitadas para usuarios nuevos)

Elige si quieres habilitar, deshabilitar o que se te pregunte sobre el uso de las reglas integradas de Best Practice Analyzer de Tabular Editor. Las reglas integradas cubren procedimientos recomendados clave en formato, metadatos, diseño del modelo, expresiones DAX y traducciones. Las instalaciones nuevas tendrán las reglas integradas habilitadas de forma predeterminada.

### Notificaciones

##### _Data refresh notification_ (enabled)

Si se selecciona, se muestra una notificación cuando finaliza una operación de actualización de datos.

### Ajuste de fórmulas DAX

##### _Habilitar ajuste de fórmulas_ (habilitado)

Ajusta automáticamente las referencias en las expresiones DAX cuando se cambia el nombre de los objetos o se mueven. Esta característica garantiza que tu código DAX siga siendo válido cuando reorganizas el modelo.

##### _Habilitar ajuste de fórmulas al pegar_ (habilitado)

Ajusta automáticamente las referencias en las expresiones DAX al pegar objetos. Esto es útil al copiar medidas o columnas calculadas entre tablas o modelos.

### Direct Lake

##### _Actualización automática al guardar_ (habilitado)

Actualiza automáticamente las tablas Direct Lake al guardar cambios para garantizar que los datos estén al día. Esto garantiza que tu modelo Direct Lake se mantenga sincronizado con el Data source subyacente.

## Tabular Editor > Actualizaciones y comentarios

![Updates and Feedback preferences](~/content/assets/images/pref-updates-and-feedback.png)

### Updates

##### _Show "Get Started" page on updates_ (enabled)

When checked, the **Get Started** page opens automatically the first time you run Tabular Editor after it has been updated. It appears **on updates**, not on every start-up. You can open it at any time from **Help > Get Started**.

##### _Buscar actualizaciones al iniciar_ (habilitado)

Si lo activas, Tabular Editor buscará nuevas versiones cuando se inicie la aplicación. Así te mantienes al día con las últimas funciones y correcciones de errores.

##### _Major updates only_ (disabled)

When checked, only major version updates trigger notifications. Minor and patch updates are ignored. This setting is only available while _Check for updates on start-up_ is checked.

The version you are running is shown below these settings, along with a **Check for updates** button that runs the check immediately.

### Managed by your organization

Where an administrator has configured [policies](xref:policies), a read-only **Managed by your organization** section is appended to this page listing every policy value Tabular Editor found, as `Name = value`. Hover over an entry to see which registry key and hive it came from.

A value Tabular Editor could not interpret is listed with an `(invalid)` marker rather than being left out. That marker is the fastest way to find the typo behind a policy that appears to do nothing, so check here first when a policy is not taking effect.

The section is absent when no policy applies. Settings that a policy locks or limits are shown read-only elsewhere in this dialog, and in the **Tools > MCP Server...** dialog, with a tooltip saying so.

### Usage Data and Feedback

##### _Ayuda a mejorar Tabular Editor recopilando datos de uso anónimos_ (habilitado)

Los datos no contienen información de identificación personal ni información sobre la estructura o el contenido de tus Data models. Si aun así quieres excluirte de la telemetría, desmarca esta opción.

##### _Enviar Reports de error_ (habilitado)

En caso de bloqueo, si esta opción está activada, Tabular Editor muestra la opción de enviar un Report de bloqueo. ¡Los Crash Reports son muy útiles para depurar, así que, si no te importa, déjalo marcado!

## Tabular Editor > Implementación

![Model Deployment preferences](~/content/assets/images/pref-model-deployment.png)

Configura qué tipos de objetos se implementan de forma predeterminada al usar el Asistente de implementación:

##### _Implementar Data sources_ (deshabilitado)

Incluye las definiciones de los Data sources al implementar. Activa esta opción si quieres que las cadenas de conexión y la configuración de los Data sources se implementen junto con tus cambios en el modelo.

##### _Implementar particiones_ (deshabilitado)

Incluye las definiciones de particiones al implementar. Activa esta opción si quieres que la configuración de las particiones se implemente junto con tus cambios en el modelo.

##### _Implementar particiones de política de actualización_ (deshabilitado)

Incluye las particiones de la política de actualización incremental durante la implementación. Esto controla si se implementan las particiones creadas por las políticas de actualización incremental.

##### _Implementar roles del modelo_ (deshabilitado)

Incluye las definiciones de rol al implementar. Activa esta opción si quieres que se implementen los roles de seguridad a nivel de filas (RLS) y de seguridad a nivel de objetos (OLS).

##### _Implementar miembros de los roles del modelo_ (deshabilitado)

Incluye las asignaciones de miembros a roles al implementar. Activa esta opción si quieres que se implementen las asignaciones de usuarios y grupos a los roles de seguridad.

##### _Implementar expresiones compartidas_ (deshabilitado)

Incluye expresiones compartidas (expresiones M) al implementar. Activa esta opción si quieres que se implementen las expresiones compartidas de Power Query.

### Metadatos de implementación

##### _Anotar metadatos de implementación_ (deshabilitado)

Añade la marca de tiempo de implementación y la información del usuario como anotaciones en los objetos implementados. Esto puede ser útil para realizar un seguimiento de cuándo y por quién se implementaron los cambios del modelo.

### Configuración de copia de seguridad

##### _Crear copia de seguridad al guardar_ (habilitado)

Crea una copia de seguridad del modelo al guardar cambios localmente. Esto te ofrece una red de seguridad por si necesitas revertir cambios.

##### _Ubicación para guardar la copia de seguridad_

Especifica la carpeta en la que se almacenan las copias de seguridad del despliegue. De forma predeterminada, no se crean copias de seguridad a menos que se especifique una ubicación.

##### _Copia de seguridad al implementar_ (habilitado)

Crea una copia de seguridad del modelo de destino antes de implementar los cambios. Esto te permite restaurar la versión anterior si es necesario.

##### _Ubicación de copia de seguridad_

Especifica la carpeta en la que se almacenan las copias de seguridad de las partidas guardadas. De forma predeterminada, no se crean copias de seguridad a menos que se especifique una ubicación.

## Tabular Editor > Valores predeterminados

<!-- IMAGE NEEDED: pref-defaults.png
     The Tabular Editor > Defaults preferences page at its default settings.
     Alt text: "The Defaults preferences page" -->

##### _Nivel de compatibilidad del nuevo modelo_ (1600)

Establece el nivel de compatibilidad predeterminado para los modelos recién creados. The choices are the same as in the **New Model** dialog:

| Nivel | Target                                     |
| ----- | ------------------------------------------ |
| 1200  | Azure Analysis Services / SQL Server 2016+ |
| 1400  | Azure Analysis Services / SQL Server 2017+ |
| 1500  | Azure Analysis Services / SQL Server 2019+ |
| 1600  | Azure Analysis Services / SQL Server 2022+ |
| 1700  | Azure Analysis Services / SQL Server 2025+ |
| 1706  | Power BI / Fabric                          |

1700 is the highest level Analysis Services supports; 1706 is the highest overall and is Power BI and Fabric only.

##### _Usar el nivel de compatibilidad más reciente como valor predeterminado_ (habilitado)

Usa automáticamente el nivel de compatibilidad más reciente disponible para los modelos nuevos. When enabled, this overrides the specific compatibility level setting above, and the dropdown is disabled.

##### _Los nuevos modelos usan la base de datos de Workspace_ (habilitado)

Al crear un modelo nuevo, crea automáticamente una base de datos de Workspace en Analysis Services. Esto te permite probar y consultar el modelo de inmediato durante el desarrollo.

##### _Modo de guardado predeterminado_ (AlwaysAsk)

Elige si quieres guardar siempre como archivo (.bim), carpeta (varios archivos JSON), TMDL (Tabular Model Definition Language) o que pregunte siempre al guardar. Opciones: AlwaysAsk, File, Folder, TMDL.

##### _Usar el nombre del archivo PBIX al guardar en disco_ (habilitado)

Al guardar un modelo cargado desde un archivo PBIX, usa el nombre del archivo PBIX como valor predeterminado. Esto mantiene la coherencia de nombres entre los archivos de Power BI y los metadatos del modelo guardados.

##### _Crear opciones de usuario para modelos nuevos_ (habilitado)

Crea automáticamente archivos .tmuo (Tabular Model User Options) para los modelos nuevos. Estos archivos almacenan ajustes específicos de cada usuario, como los diseños del diagrama y las posiciones de las ventanas.

## Tabular Editor > Teclado

![Asignaciones de teclas](~/content/assets/images/keyboard-mappings.png)

Configura los atajos de teclado para todos los comandos de Tabular Editor. Usa la función de búsqueda para encontrar rápidamente comandos específicos y asignar o modificar sus atajos de teclado para adaptarlos a tu flujo de trabajo.

## Tabular Editor > TOM Explorer

![Tom Explorer Settings](~/content/assets/images/unsaved-changes/preferences.png)

Control how the TOM (Tabular Object Model) Explorer presents the model, and what happens to the objects you delete.

The toggles that decide which object types appear in the tree, such as measures, columns, hierarchies, partitions, display folders and hidden objects, are not preferences. They live on the @tom-explorer-view toolbar, where you can change them per model without opening this dialog.

### Display and filtering

##### _Use table groups_ (enabled)

Group your tables in the TOM Explorer, for example to keep calculation groups, dimensions and fact tables apart. Tabular Editor records a table's group in an annotation on the table itself, so the grouping travels with the model. It is internal to Tabular Editor: no other client tool, Power BI Desktop included, shows it. See @table-groups.

##### _Mostrar rama completa_ (deshabilitado)

When you filter the tree, Tabular Editor shows the objects that match your filter string together with their parents. Enable this to also show every child of a match, whether or not the children match the string themselves.

##### _Highlight relationships_ (enabled)

Highlight the relationships that involve the table or column you have selected, so you can see at a glance what a column is joined to.

### Unsaved changes

These settings control how [unsaved changes](xref:unsaved-changes) are indicated in the TOM Explorer and the Properties view.

##### _Mark objects with unsaved changes_ (enabled)

Highlight objects in the TOM Explorer that differ from the last saved version of the model, using a tinted row and a badge on the object's icon: orange for edited objects, green for added objects and red for deleted objects. Tables, folders and groups that contain changed objects get a hatched fill. When disabled, deleted objects still stay visible according to the setting below, and the **Show changes** toolbar filter still works. Use **Color blindness mode** under **User Interface > Accessibility** to mark added objects in teal instead of green.

##### _Keep deleted objects visible_ (Until the model is saved)

How long deleted objects remain visible in the TOM Explorer, struck through, where they used to be. Right-click a deleted object and choose **Restore** to bring it back. Options:

- **Never**: Deleted objects disappear from the TOM Explorer at once.
- **Until the model is saved**: Deleted objects are treated as unsaved changes and disappear when the model is saved.
- **Until the model is closed**: Deleted objects stay visible, and restorable, for the whole editing session, even across saves.

##### _Gather deleted objects under a "Deleted objects" node_ (disabled)

Show the deleted objects of a table, hierarchy, role or table group together under a single **Deleted objects** node at the end of their container, instead of each where it used to be. Right-click the node and choose **Restore** to bring back all of them at once.

##### _Mark properties with unsaved changes in the Properties pane_ (enabled)

Highlight properties in the Properties view that differ from the last saved version of the model, using a tinted row. When disabled, the **Show changes** toolbar filter in the Properties view still works.

### Delete

##### _Mostrar siempre advertencias de eliminación_ (deshabilitado)

Si prefieres que Tabular Editor 3 te pida confirmación para todas las eliminaciones de objetos, habilita esta opción. De lo contrario, Tabular Editor 3 solo te pedirá que confirmes la eliminación de varios objetos o la de objetos a los que hacen referencia otros objetos.

> [!NOTE]
> Todas las operaciones de eliminación en Tabular Editor 3 se pueden deshacer con CTRL+Z.

### Localization

These settings decide the format string Tabular Editor writes when you pick the _Currency_ number format for an object in the Properties pane.

##### _Default currency_ (English (United States))

The formatting convention to base the currency format string on. Pick the locale whose currency symbol, decimal separator and digit grouping you want.

##### _Use a custom currency symbol_ (disabled)

Supply your own symbol instead of taking one from the locale above. The three settings below apply only while this is checked.

##### _Custom currency symbol_

The symbol to use. Enter the symbol on its own, without the number; whitespace is ignored.

##### _Custom currency symbol position_ (Before number)

Whether the symbol goes before or after the numeric value.

##### _Put a space between the number and symbol_ (disabled)

Separate the symbol from the numeric value with a space.

## Tabular Editor > Copiar/Pegar

<!-- IMAGE NEEDED: pref-copy-paste.png
     The Tabular Editor > Copy/Paste preferences page at its default settings.
     Alt text: "The Copy/Paste preferences page" -->

Controla qué metadatos se incluyen al copiar objetos:

##### _Incluir traducciones_ (habilitado)

Copia los metadatos de traducción junto con los objetos. Cuando está habilitado, también se copiarán las traducciones definidas para el objeto copiado.

##### _Incluir perspectivas_ (habilitado)

Copia la pertenencia a las perspectivas junto con los objetos. Cuando está habilitado, el objeto copiado pertenecerá a las mismas perspectivas que el original.

##### _Incluir RLS_ (habilitado)

Copia las expresiones de seguridad a nivel de filas junto con los objetos. Esto se aplica al copiar tablas que tengan definidas reglas de RLS.

##### _Incluir OLS_ (habilitado)

Copia la configuración de seguridad a nivel de objetos junto con los objetos. Esto se aplica al copiar objetos con restricciones de OLS.

## Tabular Editor > Perspectivas

<!-- IMAGE NEEDED: pref-perspectives.png
     The Tabular Editor > Perspectives preferences page at its default settings.
     Alt text: "The Perspectives preferences page" -->

Controla cómo se gestiona la pertenencia a las perspectivas:

##### _Heredar la pertenencia a las perspectivas para objetos nuevos_ (deshabilitado)

Los objetos recién creados heredan automáticamente la pertenencia a las perspectivas de su objeto padre. Por ejemplo, una nueva medida se agregaría automáticamente a las mismas perspectivas que su tabla padre.

##### _Heredar la pertenencia a las perspectivas para objetos reubicados_ (deshabilitado)

Los objetos que se mueven heredan la pertenencia a las perspectivas de su nuevo objeto padre. Esto resulta útil al reorganizar la estructura del modelo.

##### _Heredar al agregar una tabla a una perspectiva_ (habilitado)

Agrega automáticamente todos los objetos de la tabla (columnas, medidas, jerarquías) cuando se agrega una tabla a una perspectiva.

##### _Heredar al quitar una tabla de una perspectiva_ (habilitado)

Quita automáticamente todos los objetos de la tabla cuando se quita una tabla de una perspectiva.

## Tabular Editor > Comparación de esquemas

![Schema Compare preferences](~/content/assets/images/pref-schema-compare.png)

Configura qué cambios se ignoran durante la comparación de esquemas al actualizar los esquemas de las tablas:

##### _Ignorar cambios en Import mode_ (deshabilitado)

No marques cambios en las propiedades de Import mode. Activa esta opción si quieres ignorar los cambios entre los modos Import, DirectQuery y Dual durante la comparación de esquemas.

##### _Ignorar cambios de tipo de datos_ (deshabilitado)

No marques cambios en el tipo de datos de las columnas. Activa esta opción si quieres ignorar cambios de tipo de datos durante la comparación de esquemas.

##### _Ignorar cambios de descripción_ (deshabilitado)

No marques cambios en las descripciones de los objetos. Activa esta opción si no quieres ver los cambios en las descripciones al comparar esquemas.

##### _Ignorar cambios de decimal a double_ (deshabilitado)

No marques como cambios las diferencias entre los tipos de datos decimal y double. Esto resulta útil cuando trabajas con varios Data source que no distinguen entre estos tipos.

##### _Priorizar el detector de esquemas de Analysis Services_ (deshabilitado)

Usa los metadatos de Analysis Services como fuente de referencia para la detección de esquemas. Cuando está habilitado, Tabular Editor consultará directamente la instancia de Analysis Services, en lugar de usar la información del esquema del proveedor del Data source.

## Tabular Editor > Guardar en carpeta/archivo

![Save to Folder preferences](~/content/assets/images/pref-save-to-folder.png)

### Modo de serialización

##### _Usar formato TMDL_ (deshabilitado)

Guarda los metadatos del modelo usando el formato Tabular Model Definition Language (TMDL) en lugar de JSON. TMDL es el formato moderno recomendado para el control de versiones y la colaboración.

##### _Usar configuración de serialización recomendada_ (habilitado)

Aplica la configuración recomendada para la serialización basada en carpetas (sobrescribe la configuración personalizada). Cuando está habilitado, Tabular Editor aplica prácticas recomendadas para guardar modelos en carpetas, optimizadas para el control de versiones.

### Configuración de serialización heredada (JSON)

##### _Anteponer prefijos a los nombres de archivo_ (deshabilitado)

Añade prefijos numéricos a los nombres de archivo para ordenarlos. Esto puede ayudar a mantener un orden coherente de los archivos en los exploradores de archivos.

##### _Relaciones locales_ (habilitado)

Guarda las definiciones de relación junto con cada tabla, en lugar de en una ubicación central. Esto facilita ver qué relaciones pertenecen a cada tabla cuando usas control de versiones.

##### _Perspectivas locales_ (habilitado)

Guarda la pertenencia a perspectivas junto con cada objeto, en lugar de en una ubicación central. Esto reduce los conflictos de combinación en el control de versiones.

##### _Traducciones locales_ (activadas)

Guarda las traducciones junto a cada objeto, en lugar de en una ubicación central. Esto reduce los conflictos de combinación en el control de versiones.

##### _Niveles_

Selecciona qué tipos de objetos se deben serializar en cada nivel de carpeta. Esto te permite organizar los archivos del modelo en una estructura jerárquica. The available levels are Data Sources, User Defined Functions (UDFs), Shared Expressions, Perspectives, Relationships, Roles, Tables, Columns, Hierarchies, Measures, Partitions, Calculation Items and Translations.

##### _Ignorar objetos inferidos_ (activado)

No serialices los objetos que el motor infiere automáticamente. Esto reduce el desorden en los metadatos guardados.

##### _Ignorar propiedades inferidas_ (activado)

No serialices las propiedades que el motor infiere automáticamente. Esto mantiene los metadatos guardados limpios y centrados en los valores establecidos explícitamente.

##### _Ignorar marcas de tiempo_ (activado)

No serialices los metadatos de marca de tiempo. Te lo recomendamos encarecidamente para el control de versiones, ya que evita cambios innecesarios en cada commit.

##### _Ignorar etiquetas de linaje_ (desactivado)

No serialices los metadatos de la etiqueta de linaje de Power BI. Actívalo si no quieres información de linaje en los metadatos guardados.

##### _Ignorar configuración de privacidad_ (desactivado)

No serialices la configuración de privacidad del Data source. Actívalo si administras la configuración de privacidad por separado.

##### _Incluir datos confidenciales_ (desactivado)

Incluye información confidencial, como contraseñas, en los metadatos serializados. No se recomienda por motivos de seguridad.

##### _Ignorar particiones de actualización incremental_ (desactivado)

No serialices las particiones creadas por las políticas de actualización para la actualización incremental. Activa esta opción si quieres que la actualización incremental se gestione por separado de los metadatos guardados.

##### _Dividir cadenas multilínea_ (activado)

Divide los valores de cadena largos en varias líneas para mejorar la legibilidad en el control de versiones. Esto facilita ver los cambios en las expresiones DAX y en otras propiedades de texto extensas.

##### _Ordenar arrays_ (desactivado)

Ordena alfabéticamente los elementos del array para una serialización coherente. Esto puede reducir diferencias irrelevantes en el control de versiones, pero puede cambiar el orden lógico de algunos elementos.

### Configuración de serialización de TMDL

##### _Modo de sangría_ (tabulaciones)

Elige entre tabulaciones o espacios para la sangría en los archivos TMDL. Las tabulaciones son la opción predeterminada y recomendada.

##### _Espacios de sangría_ (4)

Si usas espacios, especifica el número de espacios por nivel de sangría.

<a name="miscellaneous"></a>

## AI Features

The parent page carries the two settings that apply to every AI feature, the chat and the [MCP server](xref:mcp-server) alike.

##### _Check for knowledge base updates on startup_ (enabled)

The AI Assistant searches a local copy of the Tabular Editor documentation. When checked, Tabular Editor looks for a newer copy at start-up and downloads it if one is available. This is the only outbound request any AI feature makes on its own.

##### Audit log

**Open audit folder** opens this computer's record of what the AI Assistant and the MCP server did: permission decisions, which tools were called and how each one ended, and the full text of any script that was run or handed over for review. Prompts, replies and data values are never recorded. The record is an Enterprise Edition feature: on Desktop and Business nothing is recorded and the button is not shown. See @ai-audit-log.

## AI Features > AI Assistant

Connection settings for the AI Assistant chat. The **AI Provider** child page renders here. See @ai-assistant for what each provider needs.

##### _Choose provider_ (None)

Which AI provider the chat talks to: **OpenAI**, **Anthropic**, **Azure OpenAI** or **Custom (OpenAI-compatible)**. The fields below change with your choice. An administrator can lock this to a single provider, or narrow the list, by policy.

##### _Base URL_ / _Service endpoint_

Where requests are sent. OpenAI and Anthropic supply a default and the field is optional. Azure OpenAI and Custom have no default, so an endpoint is required.

##### _API Key_

Your own key for the chosen provider. It is stored encrypted on this machine in `Preferences.json`. Tabular Editor ships no built-in key and never proxies your requests.

##### _OpenAI Organization ID_ and _OpenAI Project ID_

Optional, and shown for the OpenAI provider only. Use them where your OpenAI account bills or scopes usage per organization or project.

##### _Model name_ (_Deployment_ for Azure OpenAI)

Which model to use. For OpenAI and Anthropic this is a dropdown filled from an online catalog, so it is empty until the catalog has been fetched once on this machine. For Azure OpenAI the field is labelled **Deployment** and takes the name you gave the deployment, which is not necessarily the name of the underlying model. Leaving it blank uses the provider's default, except for Azure OpenAI and Custom, which have none.

## AI Features > AI Assistant > Preferences

How the chat behaves. See @ai-assistant for the detail behind each group.

### Visualización del chat

##### _Show selection context indicator_ (enabled)

Show which model object is currently selected above the chat, so you can see what the assistant will treat as context.

##### _Show custom instructions indicator_ (enabled)

Show which [Custom Instructions](xref:ai-assistant#custom-instructions) were applied above each reply.

##### _Show knowledge base search indicator_ (enabled)

Show progress while the assistant searches the knowledge base.

### Compactación de contexto

##### _Auto compact_ (enabled)

Summarize the older part of a conversation automatically as it approaches the model's context limit, so a long conversation can carry on.

##### _Auto compact threshold %_ (80)

How full the context window gets before compaction runs, as a percentage of the _model's own_ window rather than a fixed number of tokens. Values outside 50 to 100 have no further effect.

### C# Script

##### _Allow AI assistant to run C# scripts directly_ (disabled)

Let the assistant carry out the model change you asked for, instead of writing a script and opening it for you to run. Only scripts the safety analysis considers safe are run this way, meaning scripts that touch model objects and nothing else; anything reaching for files, the network or an external assembly is still handed to you for review. Each run lands as a single undo step.

This setting is unavailable until **Model metadata** is set to **Write** on the [Permissions](#ai-features--permissions) page, and it becomes available as soon as you change that dropdown, without closing the dialog. It is also unavailable, with a tooltip saying so, where an administrator has set the `DisableCSharpScripts` [policy](xref:policies). It is off by default deliberately: **Model metadata > Write** is also what an agent needs over the MCP server, and granting it there must not silently change what the chat does. See [Letting the assistant change your model](xref:ai-assistant#letting-the-assistant-change-your-model).

##### _Preview changes_ (enabled)

Show the script preview dialog before a change the assistant made stands, so you can see every model metadata change and accept or cancel it. Cancelling puts the model back and tells the assistant you rejected the change.

## AI Features > MCP Server

Settings for the [MCP server](xref:mcp-server), which lets an external agent such as Claude Code, GitHub Copilot or Cursor work on the model you have open.

![MCP Server preferences](~/content/assets/images/pref-mcp-server.png)

##### _Enable MCP Server_ (enabled)

Whether the MCP server is available at all. Clearing it stops a running server and removes both the **Tools > MCP Server...** menu item and the status bar indicator.

##### _Start MCP server automatically_ (disabled)

Start the server when Tabular Editor starts, so an agent can connect without you starting it by hand. If the port is in use at start-up, the server does not start and no prompt is shown.

##### _Require access token_ (disabled)

Make agents present a bearer token, shown in the **Tools > MCP Server...** dialog. The server listens on the loopback interface only, so this matters most on a machine where several people are signed in at once, such as a Remote Desktop or Citrix host, where every session can reach `127.0.0.1`. Administrators can enforce it with the `RequireMcpAccessToken` [policy](xref:policies).

##### _Port_ (42100)

The loopback port the server listens on, from 1024 to 49151. Changing it invalidates existing agent registrations, which point at a fixed address. If the port is taken when you start the server by hand, Tabular Editor offers the next free port it finds.

## AI Features > Permissions

One standing grant per resource, governing both the AI Assistant chat and any agent connected over the MCP server. The chat can additionally ask for something a grant does not cover; an agent cannot, so for MCP the grants apply as they stand and only change when the server restarts.

![AI Features Permissions preferences](~/content/assets/images/pref-ai-permissions.png)

| Resource                   | Niveles             | Predeterminado | What it covers                                                                                                                                                     |
| -------------------------- | ------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Model metadata**         | Deny / Read / Write | Read           | Tables, columns, measures, expressions, descriptions and relationships, plus VertiPaq Analyzer statistics. Write allows changes through C# scripts |
| **Model data**             | Deny / Read         | Deny           | Data values from your model, such as DAX query results. There is no write level                                                                    |
| **Best Practice Analyzer** | Deny / Read / Write | Read           | Read lists rules and runs the analysis; Write adds or modifies rules                                                                                               |
| **Documents**              | Deny / Read / Write | Write          | Your open C# script and DAX query tabs. Read is their contents; Write creates or modifies them                                                     |
| **Macros**                 | Deny / Read / Write | Write          | Your macro library                                                                                                                                                 |

**Write** covers Read, so there is no need to grant both. **Model data** is the one resource denied by default, because metadata describes your model while data _is_ its contents.

In the Enterprise, Consultancy and Trial editions an administrator can cap any of these by [policy](xref:policies), separately for the chat and for the MCP server. A capped dropdown is shown read-only. See @ai-assistant for how the chat asks for what a grant does not cover, and @mcp-server for what an agent sees.

## Tabular Editor > Miscellaneous

![Miscellaneous preferences](~/content/assets/images/pref-miscellaneous.png)

### Sincronización de metadatos

These settings control how Tabular Editor 3 deals with model metadata that changes outside the application. The first three cover a model loaded from a database on an instance of Analysis Services and rely on an Analysis Services trace. **Automatically reload from disk** covers a model loaded from a file or a folder, and watches those files directly.

##### _Advertir cuando los metadatos locales estén desincronizados con el modelo implementado_ (habilitado)

Cuando la marcas, se muestra una barra de información dentro de Tabular Editor, siempre que hayas hecho cambios locales en el modelo que aún no se hayan guardado en Analysis Services. Por ejemplo, si te preguntas por qué una consulta DAX o una Pivot Grid no producen el resultado esperado, podría deberse a que se ha cambiado la expresión de una medida en Tabular Editor sin guardar el cambio en Analysis Services. La barra desaparece cuando pulsas Guardar (Ctrl+S).

##### _Hacer seguimiento de los cambios externos en el modelo_ (habilitado)

Al igual que Power BI Desktop puede detectar cuándo una herramienta externa realiza cambios en el Data model, Tabular Editor también puede hacerlo. Esta opción solo es relevante para instancias locales de Analysis Services (es decir, procesos msmdsrv.exe que se ejecutan en el mismo equipo que Tabular Editor). Al marcarla, Tabular Editor inicia una traza en Analysis Services y te notifica si se realizan cambios externos.

##### _Actualizar automáticamente los metadatos locales del Tabular Object Model_ (habilitado)

Cuando está habilitado el mecanismo de trazas descrito anteriormente, esta opción permite que Tabular Editor actualice automáticamente los metadatos del modelo cuando se detecta un cambio externo. Esto es útil si cambias a menudo entre Power BI Desktop y Tabular Editor 3.

##### _Automatically reload from disk_ (enabled)

When checked, Tabular Editor watches the metadata files the model was loaded from and reloads the model when another application changes them. Unlike the two settings above, this doesn't involve an Analysis Services trace: it watches the files themselves, so it covers a model loaded from a `.bim` file or from a folder, whether or not a server is involved. If the model has unsaved changes, Tabular Editor asks you which copy to keep. See [Auto-reload from disk](xref:auto-reload).

##### _Limpiar trazas huérfanas de Tabular Editor_

Normalmente, Tabular Editor 3 debería detener y eliminar automáticamente cualquier traza de AS iniciada debido a la configuración anterior. Sin embargo, si la aplicación se cerró de forma prematura, es posible que las trazas nunca se detengan. Al hacer clic en este botón, se eliminarán todas las trazas de AS iniciadas por cualquier instancia de Tabular Editor.

> [!NOTE]
> El botón de limpieza solo está disponible cuando Tabular Editor está conectado a una instancia de Analysis Services.

## Exploración de datos > Pivot Grid

![Pivot Grid preferences](~/content/assets/images/pref-pivot-grid.png)

### Basic

##### _Actualización automática de Pivot Grid_ (activada)

Actualiza automáticamente las cuadrículas Pivot Grid cuando se guardan los cambios del modelo. Al igual que con las consultas DAX, esto te permite ver al instante el impacto de los cambios en las medidas.

##### _Avisar si los campos del Pivot Grid no coinciden_ (habilitado)

Muestra una advertencia cuando las definiciones de campos del Pivot Grid no coinciden con el modelo actual. Esto puede ocurrir si has eliminado o cambiado el nombre de los campos usados en un Pivot Grid guardado.

### Field Headers

##### _Ajuste de línea en los encabezados del Pivot Grid_ (habilitado)

Habilita el ajuste de línea en los encabezados del Pivot Grid. Esto hace que los nombres de campo largos sean más legibles.

### Lista de campos

##### _Mostrar siempre la lista de campos del Pivot Grid_ (habilitado)

Mantén visible, de forma predeterminada, la lista de campos del Pivot Grid. Desactiva esta opción si prefieres disponer de más espacio en pantalla para el propio Pivot Grid.

##### _Mostrar todos los campos en la personalización del Pivot Grid_ (habilitado)

Muestra de forma predeterminada todos los campos disponibles en la lista de campos del Pivot Grid, incluidos los campos ocultos.

##### _Diseño predeterminado para la personalización de Pivot Grid_ (StackedDefault)

Elige el diseño predeterminado para la lista de campos de la Pivot Grid. Las opciones incluyen:

- **StackedDefault**: Campos y áreas en un único panel apilado
- **StackedSideBySide**: Campos y áreas en paneles en paralelo
- **TopPanelOnly**: Lista de campos solo en la parte superior
- **BottomPanelOnly2by2**: Lista de campos en una cuadrícula 2x2 en la parte inferior
- **BottomPanelOnly1by4**: Lista de campos en un diseño 1x4 en la parte inferior

## Data Browsing > DAX Query

![DAX Query preferences](~/content/assets/images/pref-dax-query.png)

### Basic

##### _Automatically execute DAX queries by default_ (enabled)

New DAX queries open with **Auto-execute** enabled, so the query re-runs whenever changes are made to the deployed semantic model. Turn it off if you would rather execute each query yourself.

##### _Keep existing sorting and filtering in the result grid_ (WhenQueryUnchanged)

Controla si se deben conservar los filtros y la ordenación de la cuadrícula al volver a ejecutar consultas:

- **Never**: sorting and filtering are always reset when a query is executed
- **WhenQueryUnchanged**: sorting and filtering are reset only when the query is modified
- **Always**: sorting and filtering are never reset if the columns still exist

### Query settings

##### _Smart selection_ (enabled)

When you execute part of a query, Tabular Editor turns that selection into a valid DAX query on your behalf, wrapping a scalar expression in curly braces and adding the `DEFINE` section or the `EVALUATE` keyword when they are not part of the selection.

##### _Row limit_ (1,000)

Wraps every `EVALUATE` statement in a `TOPN` call, to keep an accidental query over a large table from running for a long time or exhausting memory. Set it to `0` to remove the limit entirely.

### Code Generation

##### _Use comments as separators_ (enabled)

Insert comments into generated object definitions, for example the `DEFINE` block produced by **Define object in query**, to make them easier to read.

## Data Browsing > Table Preview

![Table Preview preferences](~/content/assets/images/pref-table-preview.png)

### Basic

##### _Automatically refresh table previews by default_ (enabled)

New table previews open with **Auto-refresh** enabled, so the preview refreshes whenever changes are made to the deployed semantic model. This is useful when debugging: update an expression in one window while a preview of the same table is open in another.

##### _Sort table preview columns alphabetically_ (disabled)

When checked, table preview columns are sorted alphabetically by name, matching the order the @tom-explorer-view lists a table's columns in. When unchecked (the default), columns appear in the order the engine returns them, which is roughly internal column order and can look arbitrary.

##### _Max. values in filter dropdown_ (5,000)

Maximum number of distinct values listed in a column's filter dropdown. On a column with more distinct values than this, the values beyond the limit are not listed and cannot be ticked directly. Raising it lists more values at the cost of a heavier query each time the dropdown is opened. Accepts 100 to 1,000,000.

##### _Max. rows to sort without an attribute hierarchy_ (100,000)

Upper bound on the number of rows Tabular Editor sorts by a column that has no attribute hierarchy to sort on.

### DirectQuery

##### _Row limit_ (100)

Maximum number of rows to retrieve for a table preview in DirectQuery mode. Raise it if you need to see more data, bearing in mind that every row is fetched from the underlying source.

### Comportamiento

##### _Track selected column in TOM Explorer_ (enabled)

When you select a column in the @tom-explorer-view, the open table preview scrolls that column into view and highlights it, which is the quickest way to find one column of a very wide table. The same setting can be turned on and off for a single preview with **Track selected column** on the Table Preview toolbar.

## Editor de DAX > General

![Editor de Dax General](~/content/assets/images/dax-editor-general.png)

El Editor de DAX de Tabular Editor 3 es muy configurable. Esta página ofrece opciones para la configuración general del Editor de DAX:

##### _Números de línea_ (habilitado)

Muestra los números de línea en el margen izquierdo del editor.

##### _Plegado de código_ (habilitado)

Habilita regiones plegables en el código DAX para mejorar la legibilidad. ¡Asegúrate de probar esta función!

##### _Espacios en blanco visibles_ (desactivado)

Muestra puntos para los espacios y flechas para las tabulaciones. Esto puede ser útil para diagnosticar problemas de sangría.

##### _Guías de sangría_ (habilitado)

Muestra líneas verticales para indicar los niveles de sangría.

##### _Usar tabulaciones_ (desactivado)

Si se selecciona, se inserta un carácter de tabulación (`\t`) cada vez que se pulsa la tecla TAB. De lo contrario, se insertará el número de espacios correspondiente al ajuste _Ancho de sangría_.

##### _Estilo de comentario_ (barras)

DAX admite comentarios de línea con barras (`//`) o guiones (`--`). Esta configuración determina qué estilo de comentario se usa cuando Tabular Editor 3 genera código DAX.

##### _Documentación de funciones DAX_

Utiliza esta configuración para especificar qué URL se abrirá en el navegador web predeterminado cada vez que pulses F12 con el cursor sobre una función DAX. Las opciones incluyen https://dax.guide (recomendado) y la documentación oficial de Microsoft.

### Configuración de DAX

##### _Configuración regional_

Especifica la configuración regional para las funciones de DAX y el formato.

##### _Configuración de la versión de Analysis Services_

Estas configuraciones solo son relevantes cuando Tabular Editor 3 no puede determinar la versión de Analysis Services utilizada, como ocurre cuando se carga directamente un archivo Model.bim. En este caso, Tabular Editor intenta deducir a qué versión se implementará el modelo, en función del nivel de compatibilidad. Si Tabular Editor genera un Report de errores semánticos o de sintaxis que no lo son, puede que debas ajustar esta configuración.

## Editor de DAX > Formato automático

![Configuración de formato automático](~/content/assets/images/auto-formatting-settings.png)

El Editor de DAX es **muy** potente y te ayuda a generar código DAX bonito y fácil de leer mientras escribes.

##### _Formatear el código automáticamente mientras escribes_ (habilitado)

Esta opción aplicará automáticamente ciertas reglas de formato cuando se produzcan determinadas pulsaciones de teclas. Por ejemplo, al cerrar un paréntesis, esta función garantiza que todo lo que esté dentro del paréntesis se formatee según los demás ajustes de esta página.

##### _Formatear automáticamente las llamadas a funciones_ (habilitado)

Esta opción aplica sangría automáticamente a los argumentos de una función cuando se inserta un salto de línea dentro de una llamada a una función.

##### _Cierre automático de llaves_ (habilitado)

Esta opción aplica sangría automáticamente a los argumentos de una función cuando se inserta un salto de línea dentro de una llamada a una función.

##### _Sangría automática_ (habilitado)

Cuando está habilitada, esta opción envuelve automáticamente la selección actual con la llave de cierre al escribir una llave de apertura.

##### _Envolver la selección_ (habilitado)

Esta opción inserta automáticamente la llave o la comilla de cierre cuando se escribe una llave o comilla de apertura.

### Reglas de formato

Estos ajustes controlan cómo se formatean los espacios en blanco del código DAX, tanto cuando se aplica el formato automático como cuando formateas el código manualmente.

##### _Espacio después de las funciones_ (deshabilitado)

# [Deshabilitado](#tab/space-after-function-off)

```DAX
SUM ( 'Sales'[Amount] )
```

# [Habilitado](#tab/space-after-function-on)

```DAX
SUM( 'Sales'[Amount] )
```

***

##### [Habilitado](#tab/newline-after-function-on)

Se aplica solo cuando es necesario dividir una llamada de función en varias líneas.

# [Deshabilitado](#tab/newline-after-function-off)

```DAX
SUM
(
    'Sales'[Amount]
)
```

# _Salto de línea después de las funciones_ (deshabilitado)

```DAX
SUM(
    'Sales'[Amount]
)
```

***

##### _Añadir espacios en los paréntesis_ (habilitado)

# [Deshabilitado](#tab/pad-parentheses-off)

```DAX
SUM( Sales[Amount] )
```

# [Habilitado](#tab/pad-parentheses-on)

```DAX
SUM(Sales[Amount])
```

***

##### _Límite de línea del formato largo_ (120)

El número máximo de caracteres que se conservarán en una sola línea antes de dividir una expresión en varias líneas, al usar la opción **Formatear DAX (líneas cortas)**.

##### _Límite de línea del formato corto_ (60)

El número máximo de caracteres que se pueden mantener en una sola línea antes de dividir una expresión en varias líneas, al usar la opción **Formatear DAX (líneas largas)**.

### Mayúsculas/minúsculas y comillas

Además de dar formato a los espacios en blanco del código DAX, Tabular Editor 3 también puede corregir referencias a objetos y el uso de mayúsculas/minúsculas en funciones y palabras clave.

##### _Corregir calificadores de medidas/columnas_ (habilitado)

Si se activa, los prefijos de tabla se quitan automáticamente de las referencias a medidas y se agregan automáticamente a las referencias a columnas.

##### _Uso de mayúsculas preferido para palabras clave_ (MAYÚSCULAS)

Esta configuración permite cambiar el uso de mayúsculas/minúsculas de las palabras clave, como `ORDER BY`, `VAR`, `EVALUATE`, etc. It also governs the fixed keyword _values_ auto-complete offers for functions that take them: `ASC` and `DESC`, `KEEP`, `FIRST`, `LAST` and `DEFAULT`, the `CROSSFILTER` directions and `LOOKUP`'s `EXPLICIT` and `INFERRED`. Choose **Capitalize first letter only** to be offered `Explicit` rather than `EXPLICIT`.

##### _Uso de mayúsculas preferido para funciones_ (MAYÚSCULAS)

Esta configuración permite cambiar el uso de mayúsculas/minúsculas de las funciones, como `CALCULATE(...)`, `SUM(...)`, etc.

##### _Corregir mayúsculas/minúsculas de palabras clave/funciones_ (habilitado)

Si se activa, el uso de mayúsculas/minúsculas de las palabras clave y las funciones se corrige automáticamente cada vez que el código se formatea automáticamente o manualmente.

##### _Corregir mayúsculas/minúsculas en referencias a objetos_ (habilitado)

DAX no distingue entre mayúsculas y minúsculas. Si se activa, las referencias a tablas, columnas y medidas se corrigen automáticamente para que el uso de mayúsculas/minúsculas coincida con el nombre físico de los objetos a los que se hace referencia.

##### _Poner siempre comillas a los nombres de tabla_ (deshabilitado)

Para hacer referencia a ciertos nombres de tabla no es necesario encerrarlos entre comillas simples en DAX. Sin embargo, si prefieres que las referencias a tablas siempre lleven comillas, puedes activar esta opción.

##### _Anteponer siempre el prefijo a las columnas de extensión_ (deshabilitado)

Las columnas de extensión se pueden definir sin un nombre de tabla. Si se activa, el Editor de DAX siempre agregará el prefijo de tabla a una columna de extensión.

## Editor de DAX > Code Assist

![DAX Editor Code Assist preferences](~/content/assets/images/pref-dax-code-assist.png)

En esta página puedes configurar las dos funciones más importantes de Code Assist: los calltips (también conocidos como "información de parámetros") y el autocompletado.

##### _Disparador de autocompletado_

Controla cuándo aparece la lista de autocompletado. Las opciones incluyen la activación automática después de escribir un determinado número de caracteres, o la activación manual con Ctrl+Espacio.

##### _Disparador de sugerencias de llamada_

Controla cuándo aparece la información de parámetros. Las opciones incluyen la activación automática al abrir el paréntesis de una función o la activación manual.

##### _Búsqueda incremental_ (activada)

Habilita la búsqueda difusa/incremental en el autocompletado. Esto te permite encontrar elementos escribiendo partes de su nombre, no solo el inicio.

##### _Sugerir nombres de tablas_ (activado)

Incluye nombres de tablas en las sugerencias de autocompletado.

##### _Poner siempre entre comillas los nombres de las tablas_ (desactivado)

Pone automáticamente entre comillas los nombres de las tablas en las sugerencias, incluso cuando no es necesario.

##### _Mostrar solo la primera letra_ (desactivado)

Muestra solo los elementos que empiezan por la letra escrita. Desactiva esta opción para usar la búsqueda incremental en su lugar.

## Editor de DAX > Acciones de código

![DAX Editor Code Actions preferences](~/content/assets/images/pref-dax-code-actions.png)

Configura sugerencias automáticas de mejora de código:

##### _Prefijos de variables_

Define prefijos aceptables para nombres de variables (p. ej., `_`, `__`, `var_`, `var`, `v_`, `v`, `VAR_`). Las acciones de código sugerirán añadir estos prefijos a los nombres de variables que no sigan la convención.

##### _Prefijos de columnas_

Define prefijos aceptables para nombres de columnas temporales (p. ej., `@`, `_`, `x`, `x_`). Las acciones de código sugerirán añadir estos prefijos a los nombres de columnas temporales que no sigan la convención.

## Editor SQL / Editor M / Editor C\#

<!-- IMAGE NEEDED: pref-code-editors.png
     One of the SQL Editor, M Editor and C# Editor preferences pages. The three share a
     layout, so a single shot covers the section.
     Alt text: "The code editor preferences page, shared by the SQL, M and C# editors" -->

Hay opciones de configuración similares para los editores de scripts SQL, M (Power Query) y C# Script, entre ellas:

- Resaltado de sintaxis y esquemas de color
- Opciones de formato automático
- Funciones de Code Assist y autocompletado
- Estilos de comentarios y preferencias de sangría

Cada editor se puede personalizar de forma independiente para ajustarse a tu estilo de programación preferido.

## DAX Formatter

<!-- IMAGE NEEDED: pref-dax-formatter.png
     The DAX Formatter preferences page at its default settings.
     Alt text: "The DAX Formatter preferences page" -->

##### _Consentimiento para DAX Formatter_ (deshabilitado)

Aceptar enviar el código DAX al servicio externo de formato DAX (www.daxformatter.com). Cuando está habilitado, puedes usar este servicio para dar formato al código DAX según los estándares de la comunidad.

##### _Tiempo de espera de la solicitud de DAX Formatter_ (5000)

Tiempo de espera, en milisegundos, para las solicitudes a DAX Formatter. Aumentar este valor si a menudo recibes errores de tiempo de espera al usar DAX Formatter.

## Integración con el Optimizador de DAX

<!-- IMAGE NEEDED: pref-dax-optimizer.png
     The DAX Optimizer Integration preferences page at its default settings.
     Alt text: "The DAX Optimizer Integration preferences page" -->

Configura la integración con el Optimizador de DAX (solo en la Edición Enterprise):

##### _Conectar automáticamente_ (null/prompt)

Conectar automáticamente con el Optimizador de DAX cuando esté disponible. Si no lo configuras, se te preguntará la primera vez.

##### _Ofuscar archivos VPAX_ (habilitado)

Anonimizar los metadatos del modelo al enviarlos al Optimizador de DAX. Esto protege información confidencial como nombres de tablas y columnas, sin impedir el análisis.

##### _Directorio del diccionario de ofuscación_ (`%LocalAppData%\\TabularEditor3\\DaxOptimizer`)

Especifica dónde se almacenan los diccionarios de ofuscación. El diccionario mantiene una ofuscación coherente en varios análisis.

## Analizador VertiPaq

![VertiPaq Analyzer preferences](~/content/assets/images/pref-vertipaq-analyzer.png)

##### _Incluir metadatos de TOM_ (habilitado)

Incluye los metadatos del Tabular Object Model en las estadísticas del Analizador VertiPaq. Esto aporta información más completa sobre la estructura de tu modelo.

##### _Leer estadísticas de los datos_ (habilitado)

Lee las estadísticas analizando los datos reales (más preciso, pero más lento). Si lo deshabilitas, solo se usan los metadatos.

##### _Modo de extracción de Direct Lake_ (ResidentOnly)

Cómo extraer estadísticas de los modelos de Direct Lake:

- **ResidentOnly**: Analiza solo los datos cargados actualmente en memoria
- **All**: Incluye datos no residentes (más lento; puede desencadenar la carga de datos)

##### _Leer estadísticas de las vistas de administración dinámica_ (deshabilitado)

Usa las DMV para recopilar estadísticas (más rápido, pero menos preciso). Es una alternativa a leer las estadísticas directamente de los datos.

##### _Filas de muestra de relaciones_ (3)

Número de filas que se toman como muestra al analizar las relaciones. Valores más altos ofrecen mayor precisión, pero tardan más.

##### _Tamaño del lote de columnas_ (50)

Número de columnas que se analizan en cada lote. Ajusta esto en función del tamaño de tu modelo y de tus requisitos de rendimiento.

## Integración con Power BI

![Power BI Integration preferences](~/content/assets/images/pref-power-bi.png)

##### _URL base del punto de conexión de Power BI_ (`https://api.powerbi.com`)

La URL base para las llamadas a la API de Power BI. Cambia esto si trabajas con una nube soberana o un entorno personalizado.

##### _URL base del punto de conexión de Fabric_ (`https://api.fabric.microsoft.com`)

La URL base para las llamadas a la API de Microsoft Fabric. Cámbiala si estás trabajando con una nube soberana o un entorno personalizado.

##### _Usar el navegador integrado para la autenticación_ (activado)

Usa el navegador integrado para la autenticación OAuth en lugar del navegador del sistema. Esto ofrece una experiencia más Integrada.

## Configuración del proxy

![Proxy Settings preferences](~/content/assets/images/pref-proxy-settings.png)

##### _Tipo de proxy_ (Ninguno)

Elige entre:

- **Ninguno**: Sin configuración de proxy
- **Sistema**: Usar la configuración de proxy del sistema
- **Personalizado**: Especificar una configuración de proxy personalizada

##### _Dirección del proxy_

La dirección del servidor proxy (por ejemplo, `http://proxy.company.com:8080`).

##### _Usuario del proxy_

Nombre de usuario para la autenticación del proxy, si es necesario.

##### _Contraseña del proxy_

Contraseña para la autenticación del proxy (se almacena cifrada).

##### _Usar credenciales predeterminadas_ (activado)

Usa las credenciales actuales de Windows para la autenticación del proxy. Esto implementa el [mismo comportamiento que Power BI Desktop](https://docs.microsoft.com/en-us/power-bi/connect-data/desktop-troubleshooting-sign-in#using-default-system-credentials-for-web-proxy).

##### _Omitir el proxy para direcciones locales_ (activado)

Omite el proxy para las direcciones locales. Se recomienda para mejorar el rendimiento.

##### _Lista de exclusión del proxy_

Lista de direcciones que deben omitir el proxy (p. ej., `localhost;*.company.local`).

## Próximos pasos

Para obtener una guía fácil de usar sobre las preferencias que se ajustan con más frecuencia, consulta la guía de inicio (Personalizing TE3)[xrefid: personalizing-te3].
