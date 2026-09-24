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

![Preferencias de actualizaciones y comentarios](~/content/assets/images/pref-updates-and-feedback.png)

### Actualizaciones

##### _Mostrar la página "Primeros pasos" tras una actualización_ (activado)

Si la activas, la página **Primeros pasos** se abre automáticamente la primera vez que ejecutas Tabular Editor después de actualizarlo. Se muestra **tras una actualización**, no en cada inicio. Puedes abrirla en cualquier momento desde **Ayuda > Primeros pasos**.

##### _Buscar actualizaciones al iniciar_ (habilitado)

Si lo activas, Tabular Editor buscará nuevas versiones cuando se inicie la aplicación. Así te mantienes al día con las últimas funciones y correcciones de errores.

##### _Solo actualizaciones principales_ (desactivada)

Si lo activas, solo las actualizaciones de versión principal activarán las notificaciones. Se ignorarán las actualizaciones menores y las de corrección. Esta configuración solo está disponible cuando está activada la opción _Buscar actualizaciones al iniciar_.

Debajo de estas opciones se muestra la versión que estás usando, junto con un botón **Buscar actualizaciones** que realiza la comprobación de inmediato.

### Administrado por tu organización

Si un administrador ha configurado [directivas](xref:policies), al final de esta página se agrega una sección de solo lectura, **Administrado por tu organización**, que enumera todos los valores de directiva que Tabular Editor encontró, con el formato `Nombre = valor`. Pasa el cursor sobre una entrada para ver de qué clave y colmena del Registro procede.

Un valor que Tabular Editor no pudo interpretar se muestra con la marca `(invalid)` en lugar de omitirse. Esa marca es la forma más rápida de encontrar el error tipográfico detrás de una directiva que parece no hacer nada, así que revisa aquí primero cuando una directiva no esté surtiendo efecto.

La sección no aparece cuando no se aplica ninguna directiva. Las opciones que una directiva bloquea o limita se muestran como de solo lectura en otras partes de este cuadro de diálogo y en el cuadro de diálogo **Herramientas > Servidor MCP...**, con una descripción emergente que lo indica.

### Datos de uso y comentarios

##### _Ayuda a mejorar Tabular Editor recopilando datos de uso anónimos_ (habilitado)

Los datos no contienen información de identificación personal ni información sobre la estructura o el contenido de tus Data models. Si aun así quieres excluirte de la telemetría, desmarca esta opción.

##### _Enviar Reports de error_ (habilitado)

En caso de bloqueo, si esta opción está activada, Tabular Editor muestra la opción de enviar un Report de bloqueo. ¡Los Crash Reports son muy útiles para depurar, así que, si no te importa, déjalo marcado!

## Tabular Editor > Implementación

![Preferencias de implementación del modelo](~/content/assets/images/pref-model-deployment.png)

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

Establece el nivel de compatibilidad predeterminado para los modelos recién creados. Las opciones son las mismas que en el cuadro de diálogo **Nuevo modelo**:

| Nivel | Destino                                    |
| ----- | ------------------------------------------ |
| 1200  | Azure Analysis Services / SQL Server 2016+ |
| 1400  | Azure Analysis Services / SQL Server 2017+ |
| 1500  | Azure Analysis Services / SQL Server 2019+ |
| 1600  | Azure Analysis Services / SQL Server 2022+ |
| 1700  | Azure Analysis Services / SQL Server 2025+ |
| 1706  | Power BI / Fabric                          |

1700 es el nivel más alto compatible con Analysis Services; 1706 es el nivel más alto en general y es exclusivo de Power BI y Fabric.

##### _Usar el nivel de compatibilidad más reciente como valor predeterminado_ (habilitado)

Usa automáticamente el nivel de compatibilidad más reciente disponible para los modelos nuevos. Al habilitarlo, se reemplaza la configuración específica del nivel de compatibilidad anterior y se deshabilita el menú desplegable.

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

## Tabular Editor > Explorador TOM

![Configuración del Explorador Tom](~/content/assets/images/unsaved-changes/preferences.png)

Controla cómo el Explorador TOM (Tabular Object Model) presenta el modelo y qué ocurre con los objetos que eliminas.

Los conmutadores que determinan qué tipos de objetos aparecen en el árbol, como medidas, columnas, jerarquías, particiones, carpetas de visualización y objetos ocultos, no son preferencias. Se encuentran en la barra de herramientas @tom-explorer-view, donde puedes cambiarlos en cada modelo sin abrir este cuadro de diálogo.

### Visualización y filtrado

##### _Usar grupos de tablas_ (activado)

Agrupa tus tablas en el Explorador TOM, por ejemplo, para mantener separados los grupos de cálculo, las dimensiones y las tablas de hechos. Tabular Editor registra el grupo de una tabla en una anotación de la propia tabla, de modo que la agrupación acompaña al modelo. Es interno de Tabular Editor: ninguna otra herramienta cliente, ni siquiera Power BI Desktop, muestra esa agrupación. Consulta @table-groups.

##### _Mostrar rama completa_ (deshabilitado)

Cuando filtras el árbol, Tabular Editor muestra los objetos que coinciden con tu cadena de filtro junto con sus nodos principales. Activa esta opción para mostrar también todos los elementos secundarios de una coincidencia, independientemente de que coincidan o no con la cadena.

##### _Resaltar relaciones_ (habilitado)

Resalta las relaciones en las que interviene la tabla o la columna que has seleccionado, para que puedas ver de un vistazo con qué se une una columna.

### Cambios no guardados

Estos ajustes controlan cómo se indican los [cambios no guardados](xref:unsaved-changes) en el Explorador TOM y en la vista de propiedades.

##### _Marcar objetos con cambios no guardados_ (habilitado)

Resalta en el Explorador TOM los objetos que difieren de la última versión guardada del modelo, mediante una fila sombreada y un distintivo en el icono del objeto: naranja para los objetos editados, verde para los objetos añadidos y rojo para los objetos eliminados. Las tablas, carpetas y grupos que contienen objetos modificados reciben un relleno rayado. Cuando está deshabilitado, los objetos eliminados siguen siendo visibles según la configuración siguiente, y el filtro **Mostrar cambios** de la barra de herramientas sigue funcionando. Usa **Modo para daltónicos** en **Interfaz de usuario > Accesibilidad** para marcar los objetos añadidos en verde azulado en lugar de verde.

##### _Mantener visibles los objetos eliminados_ (Hasta que se guarde el modelo)

Cuánto tiempo permanecen visibles los objetos eliminados en el Explorador TOM, tachados, en el lugar que ocupaban. Haz clic con el botón derecho en un objeto eliminado y elige **Restaurar** para recuperarlo. Opciones:

- **Nunca**: Los objetos eliminados desaparecen del Explorador TOM de inmediato.
- **Hasta que se guarde el modelo**: Los objetos eliminados se tratan como cambios no guardados y desaparecen al guardar el modelo.
- **Hasta que se cierre el modelo**: Los objetos eliminados permanecen visibles y se pueden restaurar durante toda la sesión de edición, incluso después de guardar.

##### _Agrupar los objetos eliminados bajo un nodo "Objetos eliminados"_ (deshabilitado)

Muestra juntos los objetos eliminados de una tabla, jerarquía, rol o grupo de tablas bajo un único nodo **Objetos eliminados** al final de su contenedor, en lugar de mostrarlos individualmente donde estaban. Haz clic con el botón derecho en el nodo y elige **Restaurar** para recuperarlos todos de una vez.

##### _Marcar las propiedades con cambios no guardados en el panel de propiedades_ (habilitado)

Resalta en la vista de propiedades aquellas que difieren de la última versión guardada del modelo, mediante una fila sombreada. Cuando está deshabilitado, el filtro **Mostrar cambios** de la barra de herramientas en la vista de propiedades sigue funcionando.

### Eliminar

##### _Mostrar siempre advertencias de eliminación_ (deshabilitado)

Si prefieres que Tabular Editor 3 te pida confirmación para todas las eliminaciones de objetos, habilita esta opción. De lo contrario, Tabular Editor 3 solo te pedirá que confirmes la eliminación de varios objetos o la de objetos a los que hacen referencia otros objetos.

> [!NOTE]
> Todas las operaciones de eliminación en Tabular Editor 3 se pueden deshacer con CTRL+Z.

### Localización

Estos ajustes determinan la cadena de formato que Tabular Editor escribe cuando seleccionas el formato numérico _Moneda_ para un objeto en el panel de propiedades.

##### _Moneda predeterminada_ (Inglés (Estados Unidos))

La convención de formato que se usa como base para la cadena de formato de moneda. Elige la configuración regional cuyo símbolo de moneda, separador decimal y agrupación de dígitos quieras usar.

##### _Usar un símbolo de moneda personalizado_ (desactivado)

Indica tu propio símbolo en lugar de usar el de la configuración regional anterior. Las tres opciones siguientes solo se aplican mientras esta casilla esté seleccionada.

##### _Símbolo de moneda personalizado_

El símbolo que se usará. Escribe solo el símbolo, sin el número; se ignoran los espacios en blanco.

##### _Posición del símbolo de moneda personalizado_ (Antes del número)

Si el símbolo va antes o después del valor numérico.

##### _Poner un espacio entre el número y el símbolo_ (desactivado)

Separa el símbolo del valor numérico con un espacio.

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

![Preferencias de comparación de esquema](~/content/assets/images/pref-schema-compare.png)

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

![Preferencias de Guardar en carpeta](~/content/assets/images/pref-save-to-folder.png)

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

Selecciona qué tipos de objetos se deben serializar en cada nivel de carpeta. Esto te permite organizar los archivos del modelo en una estructura jerárquica. Los niveles disponibles son Data sources, funciones definidas por el usuario (UDFs), expresiones compartidas, perspectivas, relaciones, roles, tablas, columnas, jerarquías, medidas, particiones, elementos de cálculo y traducciones.

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

## Funciones de IA

La página principal contiene las dos opciones que se aplican a todas las funciones de IA, tanto al chat como al [servidor MCP](xref:mcp-server).

##### _Buscar actualizaciones de la base de conocimientos al iniciar_ (activado)

El Asistente de IA busca en una copia local de la documentación de Tabular Editor. Cuando esta opción está seleccionada, Tabular Editor busca una copia más reciente al iniciarse y la descarga si hay una disponible. Esta es la única solicitud saliente que realiza por sí sola cualquier función de IA.

##### Registro de auditoría

**Abrir carpeta de auditoría** abre el registro de este equipo de lo que hicieron el Asistente de IA y el servidor MCP: decisiones de permisos, qué herramientas se llamaron y cómo terminó cada una, y el texto completo de cualquier script que se ejecutó o se entregó para su revisión. Los prompts, las respuestas y los valores de datos nunca se registran. El registro es una función de la Edición Enterprise: en las ediciones Desktop y Business no se registra nada y no se muestra el botón. Consulta @ai-audit-log.

## Funciones de IA > Asistente de IA

Configuración de conexión para el chat del Asistente de IA. La subpágina **Proveedor de IA** se muestra aquí. Consulta @ai-assistant para ver qué necesita cada proveedor.

##### _Elegir proveedor_ (Ninguno)

Con qué proveedor de IA se comunica el chat: **OpenAI**, **Anthropic**, **Azure OpenAI** o **Personalizado (compatible con OpenAI)**. Los campos de abajo cambian según tu elección. Un administrador puede fijarlo a un único proveedor o limitar la lista mediante una directiva.

##### _URL base_ / _Punto de conexión del servicio_

Dónde se envían las solicitudes. OpenAI y Anthropic proporcionan uno predeterminado y el campo es opcional. Azure OpenAI y Personalizado no tienen ningún valor predeterminado, por lo que se requiere un punto de conexión.

##### _Clave de API_

Tu propia clave para el proveedor elegido. Se almacena cifrada en este equipo, en el archivo de preferencias `Preferences.json`. Tabular Editor no incluye ninguna clave integrada y nunca actúa como proxy de tus solicitudes.

##### _ID de organización de OpenAI_ y _ID de proyecto de OpenAI_

Son opcionales y solo se muestran para el proveedor OpenAI. Úsalos cuando tu cuenta de OpenAI facture o delimite el uso por organización o proyecto.

##### _Nombre del modelo_ (_Implementación_ para Azure OpenAI)

Qué modelo usar. Para OpenAI y Anthropic, es una lista desplegable que se rellena desde un catálogo en línea, por lo que estará vacía hasta que se haya descargado el catálogo al menos una vez en este equipo. En Azure OpenAI, el campo se etiqueta como **Implementación** y toma el nombre que le diste a la implementación, que no necesariamente coincide con el nombre del modelo subyacente. Si se deja en blanco, se usa el valor predeterminado del proveedor, salvo en Azure OpenAI y Personalizado, que no tienen valor predeterminado.

## Funciones de IA > Asistente de IA > Preferencias

Cómo se comporta el chat. Consulta @ai-assistant para conocer los detalles de cada grupo.

### Visualización del chat

##### _Mostrar indicador de contexto de selección_ (habilitado)

Muestra qué objeto del modelo está seleccionado actualmente encima del chat, para que veas qué tratará el asistente como contexto.

##### _Mostrar indicador de instrucciones personalizadas_ (habilitado)

Muestra qué [Instrucciones personalizadas](xref:ai-assistant#custom-instructions) se aplicaron sobre cada respuesta.

##### _Mostrar indicador de búsqueda en la base de conocimientos_ (habilitado)

Muestra el progreso mientras el asistente busca en la base de conocimientos.

### Compactación de contexto

##### _Compactación automática_ (habilitado)

Resume automáticamente la parte más antigua de una conversación cuando se acerca al límite de contexto del modelo, para que una conversación larga pueda continuar.

##### _Umbral de compactación automática %_ (80)

Cuánto se llena la ventana de contexto antes de que se ejecute la compactación, como porcentaje de la ventana del _propio modelo_ en lugar de un número fijo de tokens. Los valores fuera del rango de 50 a 100 no tienen ningún efecto adicional.

### C# Script

##### _Permitir que el asistente de IA ejecute C# Scripts directamente_ (deshabilitado)

Permite que el asistente realice el cambio en el modelo que pediste, en lugar de escribir un script y abrirlo para que lo ejecutes. Solo se ejecutan así los scripts que el análisis de seguridad considera seguros; es decir, scripts que solo modifican objetos del modelo y nada más. Cualquier script que acceda a archivos, a la red o a un ensamblado externo se te seguirá entregando para su revisión. Cada ejecución queda registrada como un único paso de deshacer.

Esta opción no está disponible hasta que configures **Metadatos del modelo** como **Escritura** en la página [Permisos](#ai-features--permissions), y pasa a estar disponible en cuanto cambies esa lista desplegable, sin cerrar el cuadro de diálogo. Tampoco está disponible, con un tooltip que lo indica, cuando un administrador ha establecido la [directiva](xref:policies) `DisableCSharpScripts`. Está desactivada deliberadamente de forma predeterminada: **Metadatos del modelo > Escritura** es también lo que un agente necesita a través del servidor MCP, y concederlo ahí no debe cambiar silenciosamente el comportamiento del chat. Consulta [Permitir que el asistente cambie tu modelo](xref:ai-assistant#letting-the-assistant-change-your-model).

##### _Vista previa de los cambios_ (activada)

Muestra el cuadro de diálogo de vista previa del script antes de que se aplique un cambio realizado por el asistente, para que puedas ver todos los cambios de metadatos del modelo y aceptarlos o cancelarlos. Al cancelar, el modelo vuelve a su estado anterior y el asistente recibe la indicación de que rechazaste el cambio.

## Funciones de IA > Servidor MCP

Configuración del [servidor MCP](xref:mcp-server), que permite que un agente externo, como Claude Code, GitHub Copilot o Cursor, trabaje en el modelo que tienes abierto.

![Preferencias del servidor MCP](~/content/assets/images/pref-mcp-server.png)

##### _Habilitar el servidor MCP_ (activado)

Determina si el servidor MCP está disponible. Al desmarcarlo, se detiene el servidor en ejecución y se eliminan tanto la opción de menú **Herramientas > Servidor MCP...** como el indicador de la barra de estado.

##### _Iniciar el servidor MCP automáticamente_ (desactivado)

Inicia el servidor cuando se inicia Tabular Editor, para que un agente pueda conectarse sin que tengas que iniciarlo manualmente. Si el puerto está en uso al iniciar, el servidor no se inicia y no se muestra ningún aviso.

##### _Requerir token de acceso_ (desactivado)

Hace que los agentes deban presentar un token bearer, que se muestra en el cuadro de diálogo **Herramientas > Servidor MCP...**. El servidor solo escucha en la interfaz de loopback, por lo que esto es especialmente relevante en una máquina en la que varias personas han iniciado sesión a la vez, como un host de Escritorio remoto o Citrix, donde cada sesión puede acceder a `127.0.0.1`. Los administradores pueden imponerlo mediante la [directiva](xref:policies) `RequireMcpAccessToken`.

##### _Puerto_ (42100)

El puerto de loopback en el que escucha el servidor, entre 1024 y 49151. Cambiarlo invalida los registros existentes de los agentes, que apuntan a una dirección fija. Si el puerto está ocupado cuando inicias el servidor manualmente, Tabular Editor te ofrece el siguiente puerto libre que encuentre.

## Funciones de IA > Permisos

Una autorización permanente por recurso, que se aplica tanto al chat del Asistente de IA como a cualquier agente conectado a través del servidor MCP. Además, el chat puede pedir algo que una autorización no cubra; un agente no puede hacerlo, así que en MCP las autorizaciones se aplican tal como están y solo cambian cuando el servidor se reinicia.

![Preferencias de permisos de las funciones de IA](~/content/assets/images/pref-ai-permissions.png)

| Recurso                    | Niveles                   | Predeterminado | Qué cubre                                                                                                                                                                                     |
| -------------------------- | ------------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Metadatos del modelo**   | Denegar / Leer / Escribir | Leer           | Tablas, columnas, medidas, expresiones, descripciones y relaciones, además de las estadísticas del Analizador VertiPaq. Escribir permite realizar cambios mediante C# Scripts |
| **Datos del modelo**       | Denegar / Leer            | Denegar        | Valores de datos del modelo, como los resultados de Consultas DAX. No existe un nivel de escritura                                                                            |
| **Best Practice Analyzer** | Denegar / Leer / Escribir | Leer           | Leer muestra las reglas y ejecuta el análisis; escribir agrega o modifica reglas                                                                                                              |
| **Documentos**             | Denegar / Leer / Escribir | Escribir       | Tus pestañas abiertas de C# Scripts y de Consultas DAX. Leer permite ver su contenido; escribir permite crearlas o modificarlas                                               |
| **Macros**                 | Denegar / Leer / Escribir | Escribir       | Tu biblioteca de macros                                                                                                                                                                       |

**Escribir** incluye el permiso de lectura, por lo que no es necesario conceder ambos permisos. Los **datos del modelo** son el único recurso que se deniega de forma predeterminada, porque los metadatos describen tu modelo, mientras que los datos _son_ su contenido.

En las ediciones Enterprise, Consultancy y Trial, un administrador puede establecer un límite para cualquiera de estos mediante una [política](xref:policies), por separado para el chat y para el servidor MCP. Un desplegable con límite se muestra en modo de solo lectura. Consulta @ai-assistant para ver cómo el chat solicita lo que un permiso no cubre, y @mcp-server para ver lo que ve un agente.

## Tabular Editor > Miscelánea

![Preferencias de Miscelánea](~/content/assets/images/pref-miscellaneous.png)

### Sincronización de metadatos

Estas configuraciones controlan cómo gestiona Tabular Editor 3 los metadatos del modelo que cambian fuera de la aplicación. Las tres primeras se aplican a un modelo cargado desde una base de datos en una instancia de Analysis Services y dependen de una traza de Analysis Services. **Recargar automáticamente desde disco** se aplica a un modelo cargado desde un archivo o una carpeta, y supervisa esos archivos directamente.

##### _Advertir cuando los metadatos locales estén desincronizados con el modelo implementado_ (habilitado)

Cuando la marcas, se muestra una barra de información dentro de Tabular Editor, siempre que hayas hecho cambios locales en el modelo que aún no se hayan guardado en Analysis Services. Por ejemplo, si te preguntas por qué una consulta DAX o una Pivot Grid no producen el resultado esperado, podría deberse a que se ha cambiado la expresión de una medida en Tabular Editor sin guardar el cambio en Analysis Services. La barra desaparece cuando pulsas Guardar (Ctrl+S).

##### _Hacer seguimiento de los cambios externos en el modelo_ (habilitado)

Al igual que Power BI Desktop puede detectar cuándo una herramienta externa realiza cambios en el Data model, Tabular Editor también puede hacerlo. Esta opción solo es relevante para instancias locales de Analysis Services (es decir, procesos msmdsrv.exe que se ejecutan en el mismo equipo que Tabular Editor). Al marcarla, Tabular Editor inicia una traza en Analysis Services y te notifica si se realizan cambios externos.

##### _Actualizar automáticamente los metadatos locales del Tabular Object Model_ (habilitado)

Cuando está habilitado el mecanismo de trazas descrito anteriormente, esta opción permite que Tabular Editor actualice automáticamente los metadatos del modelo cuando se detecta un cambio externo. Esto es útil si cambias a menudo entre Power BI Desktop y Tabular Editor 3.

##### _Recargar automáticamente desde disco_ (habilitado)

Cuando está marcada, Tabular Editor supervisa los archivos de metadatos desde los que se cargó el modelo y vuelve a cargar el modelo cuando otra aplicación los modifica. A diferencia de las dos opciones anteriores, esto no implica una traza de Analysis Services: supervisa los propios archivos, por lo que se aplica a un modelo cargado desde un archivo `.bim` o desde una carpeta, haya o no un servidor de por medio. Si el modelo tiene cambios sin guardar, Tabular Editor te pregunta qué copia quieres conservar. Consulta [Recarga automática desde disco](xref:auto-reload).

##### _Limpiar trazas huérfanas de Tabular Editor_

Normalmente, Tabular Editor 3 debería detener y eliminar automáticamente cualquier traza de AS iniciada debido a la configuración anterior. Sin embargo, si la aplicación se cerró de forma prematura, es posible que las trazas nunca se detengan. Al hacer clic en este botón, se eliminarán todas las trazas de AS iniciadas por cualquier instancia de Tabular Editor.

> [!NOTE]
> El botón de limpieza solo está disponible cuando Tabular Editor está conectado a una instancia de Analysis Services.

## Exploración de datos > Pivot Grid

![Preferencias de Pivot Grid](~/content/assets/images/pref-pivot-grid.png)

### Básico

##### _Actualización automática de Pivot Grid_ (activada)

Actualiza automáticamente las cuadrículas Pivot Grid cuando se guardan los cambios del modelo. Al igual que con las consultas DAX, esto te permite ver al instante el impacto de los cambios en las medidas.

##### _Avisar si los campos del Pivot Grid no coinciden_ (habilitado)

Muestra una advertencia cuando las definiciones de campos del Pivot Grid no coinciden con el modelo actual. Esto puede ocurrir si has eliminado o cambiado el nombre de los campos usados en un Pivot Grid guardado.

### Encabezados de campo

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

## Exploración de datos > Consulta DAX

![Preferencias de la Consulta DAX](~/content/assets/images/pref-dax-query.png)

### Básico

##### _Ejecutar automáticamente las Consultas DAX de forma predeterminada_ (habilitado)

Las nuevas Consultas DAX se abren con **Ejecución automática** activada, por lo que se vuelven a ejecutar cada vez que se realizan cambios en el modelo semántico implementado. Desactiva esta opción si prefieres ejecutar cada consulta por tu cuenta.

##### _Mantener la ordenación y el filtrado existentes en la cuadrícula de resultados_ (WhenQueryUnchanged)

Controla si se deben conservar los filtros y la ordenación de la cuadrícula al volver a ejecutar consultas:

- **Nunca**: la ordenación y el filtrado siempre se restablecen cuando se ejecuta una consulta
- **WhenQueryUnchanged**: la ordenación y el filtrado se restablecen solo cuando se modifica la consulta
- **Always**: la ordenación y el filtrado nunca se restablecen si las columnas siguen existiendo

### Configuración de la consulta

##### _Selección inteligente_ (habilitada)

Cuando ejecutas parte de una consulta, Tabular Editor convierte esa selección en una consulta DAX válida automáticamente, envolviendo una expresión escalar entre llaves y añadiendo la sección `DEFINE` o la palabra clave `EVALUATE` cuando no forman parte de la selección.

##### _Límite de filas_ (1,000)

Envuelve cada instrucción `EVALUATE` en una llamada a `TOPN`, para evitar que una consulta accidental sobre una tabla grande se ejecute durante mucho tiempo o agote la memoria. Establécelo en `0` para quitar el límite por completo.

### Generación de código

##### _Usar comentarios como separadores_ (habilitado)

Inserta comentarios en las definiciones de objetos generadas, por ejemplo en el bloque `DEFINE` producido por **Definir objeto en la consulta**, para que sean más fáciles de leer.

## Exploración de datos > Vista previa de tabla

![Preferencias de Vista previa de tabla](~/content/assets/images/pref-table-preview.png)

### Básico

##### _Actualizar automáticamente las Vistas previas de tabla de forma predeterminada_ (habilitado)

Las nuevas Vistas previas de tabla se abren con **Actualización automática** habilitada, de modo que la vista previa se actualiza cada vez que se realizan cambios en el modelo semántico implementado. Esto es útil al depurar: actualiza una expresión en una ventana mientras mantienes abierta una vista previa de la misma tabla en otra.

##### _Ordenar alfabéticamente las columnas de la Vista previa de tabla_ (desactivado)

Al marcarla, las columnas de la Vista previa de tabla se ordenan alfabéticamente por nombre, coincidiendo con el orden en que @tom-explorer-view muestra las columnas de una tabla. Cuando no está marcada (valor predeterminado), las columnas aparecen en el orden en que las devuelve el motor, que es aproximadamente el orden interno de las columnas y puede parecer arbitrario.

##### _Máx. valores en el menú desplegable del filtro_ (5,000)

Número máximo de valores distintos que se muestran en el desplegable de filtro de una columna. En una columna con más valores distintos que este límite, los valores que lo superen no se mostrarán en la lista ni podrán marcarse directamente. Al aumentarlo, se mostrarán más valores, a costa de una consulta más pesada cada vez que se abra el desplegable. Acepta de 100 a 1.000.000.

##### _Máx. filas para ordenar sin una jerarquía de atributos_ (100.000)

Límite superior del número de filas que Tabular Editor ordena al ordenar por una columna que no tiene una jerarquía de atributos para ordenar.

### DirectQuery

##### _Límite de filas_ (100)

Número máximo de filas que se pueden recuperar para una Vista previa de tabla en modo DirectQuery. Auméntalo si necesitas ver más datos, teniendo en cuenta que cada fila se recupera del origen subyacente.

### Comportamiento

##### _Seguir la columna seleccionada en el Explorador TOM_ (habilitado)

Cuando seleccionas una columna en la vista @tom-explorer-view, la Vista previa de tabla abierta se desplaza hasta esa columna y la resalta; es la forma más rápida de encontrar una columna en una tabla muy ancha. La misma configuración puede activarse y desactivarse para una sola vista previa con **Seguir la columna seleccionada** en la barra de herramientas de la Vista previa de tabla.

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

Esta configuración permite cambiar el uso de mayúsculas/minúsculas de las palabras clave, como `ORDER BY`, `VAR`, `EVALUATE`, etc. También controla los _valores_ de palabras clave fijas que ofrece el autocompletado para las funciones que los aceptan: `ASC` y `DESC`, `KEEP`, `FIRST`, `LAST` y `DEFAULT`, las direcciones de `CROSSFILTER` y los valores `EXPLICIT` e `INFERRED` de `LOOKUP`. Elige **Capitalizar solo la primera letra** para que se ofrezca `Explicit` en lugar de `EXPLICIT`.

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

![Preferencias de Code Assist del Editor de DAX](~/content/assets/images/pref-dax-code-assist.png)

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

![Preferencias de acciones de código del Editor de DAX](~/content/assets/images/pref-dax-code-actions.png)

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

![Preferencias del Analizador VertiPaq](~/content/assets/images/pref-vertipaq-analyzer.png)

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

![Preferencias de integración con Power BI](~/content/assets/images/pref-power-bi.png)

##### _URL base del punto de conexión de Power BI_ (`https://api.powerbi.com`)

La URL base para las llamadas a la API de Power BI. Cambia esto si trabajas con una nube soberana o un entorno personalizado.

##### _URL base del punto de conexión de Fabric_ (`https://api.fabric.microsoft.com`)

La URL base para las llamadas a la API de Microsoft Fabric. Cámbiala si estás trabajando con una nube soberana o un entorno personalizado.

##### _Usar el navegador integrado para la autenticación_ (activado)

Usa el navegador integrado para la autenticación OAuth en lugar del navegador del sistema. Esto ofrece una experiencia más Integrada.

## Configuración del proxy

![Preferencias de configuración de proxy](~/content/assets/images/pref-proxy-settings.png)

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
