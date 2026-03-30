---
uid: preferences
title: Control de preferencias
author: Daniel Otykier
updated: 2026-01-12
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

### Sincronización de metadatos

Estas configuraciones controlan el comportamiento de Tabular Editor 3 cuando los metadatos del modelo se cargan desde una base de datos en una instancia de Analysis Services. Las configuraciones especifican cómo debe gestionar Tabular Editor 3 los cambios de metadatos que se apliquen a la base de datos desde fuera de la aplicación.

##### _Advertir cuando los metadatos locales estén desincronizados con el modelo implementado_ (habilitado)

Cuando la marcas, se muestra una barra de información dentro de Tabular Editor, siempre que hayas hecho cambios locales en el modelo que aún no se hayan guardado en Analysis Services. Por ejemplo, si te preguntas por qué una consulta DAX o una Pivot Grid no producen el resultado esperado, podría deberse a que se ha cambiado la expresión de una medida en Tabular Editor sin guardar el cambio en Analysis Services. La barra desaparece cuando pulsas Guardar (Ctrl+S).

##### _Hacer seguimiento de los cambios externos en el modelo_ (habilitado)

Al igual que Power BI Desktop puede detectar cuándo una herramienta externa realiza cambios en el Data model, Tabular Editor también puede hacerlo. Esta opción solo es relevante para instancias locales de Analysis Services (es decir, procesos msmdsrv.exe que se ejecutan en el mismo equipo que Tabular Editor). Al marcarla, Tabular Editor inicia una traza en Analysis Services y te notifica si se realizan cambios externos.

##### _Actualizar automáticamente los metadatos locales del Tabular Object Model_ (habilitado)

Cuando está habilitado el mecanismo de trazas descrito anteriormente, esta opción permite que Tabular Editor actualice automáticamente los metadatos del modelo cuando se detecta un cambio externo. Esto es útil si cambias a menudo entre Power BI Desktop y Tabular Editor 3.

##### _Limpiar trazas huérfanas de Tabular Editor_

Normalmente, Tabular Editor 3 debería detener y eliminar automáticamente cualquier traza de AS iniciada debido a la configuración anterior. Sin embargo, si la aplicación se cerró de forma prematura, es posible que las trazas nunca se detengan. Al hacer clic en este botón, se eliminarán todas las trazas de AS iniciadas por cualquier instancia de Tabular Editor.

> [!NOTE]
> El botón de limpieza solo está disponible cuando Tabular Editor está conectado a una instancia de Analysis Services.

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

![Marcador de posición: Captura de pantalla de la página de preferencias de Actualizaciones y comentarios]

##### _Buscar actualizaciones al iniciar_ (habilitado)

Si lo activas, Tabular Editor buscará nuevas versiones cuando se inicie la aplicación. Así te mantienes al día con las últimas funciones y correcciones de errores.

##### _Buscar solo actualizaciones principales_ (deshabilitado)

Si lo activas, solo las actualizaciones de versión principal activarán las notificaciones. Se ignorarán las actualizaciones menores y de parches.

##### _Ayuda a mejorar Tabular Editor recopilando datos de uso anónimos_ (habilitado)

Los datos no contienen información de identificación personal ni información sobre la estructura o el contenido de tus Data models. Si aun así quieres excluirte de la telemetría, desmarca esta opción.

##### _Enviar Reports de error_ (habilitado)

En caso de bloqueo, si esta opción está activada, Tabular Editor muestra la opción de enviar un Report de bloqueo. ¡Los Crash Reports son muy útiles para depurar, así que, si no te importa, déjalo marcado!

## Tabular Editor > Implementación

![Marcador de posición: Captura de pantalla de la página de preferencias de Implementación]

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

Especifica la carpeta donde se almacenan las copias de seguridad de los despliegues. De forma predeterminada, no se crean copias de seguridad a menos que se especifique una ubicación.

##### _Copia de seguridad al implementar_ (habilitado)

Crea una copia de seguridad del modelo de destino antes de implementar los cambios. Esto te permite restaurar la versión anterior si es necesario.

##### _Ubicación de copia de seguridad_

De forma predeterminada, no se crean copias de seguridad a menos que se especifique una ubicación. Especifica la carpeta donde se almacenan las copias de seguridad creadas al guardar.

## Tabular Editor > Valores predeterminados

![Marcador de posición: captura de pantalla de la página de preferencias de «Valores predeterminados»]

##### _Nivel de compatibilidad del nuevo modelo_ (1600)

Establece el nivel de compatibilidad predeterminado para los modelos recién creados. El nivel de compatibilidad 1600 corresponde a SQL Server 2022 y Power BI.

##### _Usar el nivel de compatibilidad más reciente como valor predeterminado_ (habilitado)

Usa automáticamente el nivel de compatibilidad más reciente disponible para los modelos nuevos. Cuando está habilitado, esto sobrescribe la configuración específica del nivel de compatibilidad indicada arriba.

##### _Los nuevos modelos usan la base de datos de Workspace_ (habilitado)

Al crear un modelo nuevo, crea automáticamente una base de datos de Workspace en Analysis Services. Esto te permite probar y consultar el modelo de inmediato durante el desarrollo.

##### _Modo de guardado predeterminado_ (AlwaysAsk)

Elige si quieres guardar siempre como archivo (.bim), carpeta (varios archivos JSON), TMDL (Tabular Model Definition Language) o que pregunte siempre al guardar. Opciones: AlwaysAsk, File, Folder, TMDL.

##### _Usar el nombre del archivo PBIX al guardar en disco_ (habilitado)

Al guardar un modelo cargado desde un archivo PBIX, usa el nombre del archivo PBIX como valor predeterminado. Esto mantiene la coherencia de nombres entre los archivos de Power BI y los metadatos del modelo guardados.

##### _Crear opciones de usuario para modelos nuevos_ (habilitado)

Crea automáticamente archivos .tmuo (Tabular Model User Options) para los modelos nuevos. Estos archivos almacenan ajustes específicos de cada usuario, como los diseños del diagrama y las posiciones de las ventanas.

<a name="tabular-editor--keyboard"></a>

## Tabular Editor > Teclado

![Asignaciones de teclas](~/content/assets/images/keyboard-mappings.png)

Configura los atajos de teclado para todos los comandos de Tabular Editor. Usa la función de búsqueda para encontrar rápidamente comandos específicos y asignar o modificar sus atajos de teclado para adaptarlos a tu flujo de trabajo.

## Tabular Editor > Vista del Explorador TOM

![Configuración de Tom Explorer](~/content/assets/images/tom-explorer-settings.png)

Controla qué objetos y propiedades son visibles en el Explorador TOM (Tabular Object Model):

##### _Mostrar carpetas de visualización_ (activado)

Muestra u oculta las agrupaciones de carpetas de visualización. Cuando está activado, los objetos se organizan según su jerarquía de carpetas de visualización.

##### _Mostrar objetos ocultos_ (desactivado)

Muestra u oculta los objetos marcados como ocultos en el modelo. Activa esta opción si necesitas trabajar con tablas, columnas o medidas ocultas.

##### _Todos los tipos de objetos_ (activado)

Muestra todos los tipos de objetos en el árbol del explorador. Cuando está desactivado, solo se muestran los tipos de objetos más comunes.

##### _Ordenar alfabéticamente_ (activado)

Ordena los objetos alfabéticamente en lugar de por orden de creación. Esto facilita encontrar objetos específicos en modelos grandes.

##### _Mostrar medidas_ (activado)

Muestra las medidas en el árbol del explorador.

##### _Mostrar columnas_ (activado)

Muestra las columnas en el árbol del explorador.

##### _Mostrar jerarquías_ (activado)

Muestra las jerarquías en el árbol del explorador.

##### _Mostrar particiones_ (activado)

Muestra las particiones en el árbol del explorador.

##### _Mostrar información de metadatos_ (desactivado)

Muestra propiedades de metadatos adicionales en la información sobre herramientas y en la cuadrícula de propiedades. Esto incluye información como etiquetas de linaje, marcas de tiempo de creación y otros metadatos técnicos.

##### _Mostrar rama completa_ (deshabilitado)

Al filtrar el Explorador TOM, de forma predeterminada, Tabular Editor 3 muestra en la jerarquía todos los elementos que coinciden con la cadena de filtro, incluidos sus elementos padre. Si quieres ver también todos los elementos secundarios (aunque no coincidan con la cadena de filtro), habilita esta opción.

##### _Mostrar siempre advertencias de eliminación_ (deshabilitado)

Si prefieres que Tabular Editor 3 te pida confirmación para todas las eliminaciones de objetos, habilita esta opción. De lo contrario, Tabular Editor 3 solo te pedirá que confirmes la eliminación de varios objetos o la de objetos a los que hacen referencia otros objetos.

> [!NOTE]
> Todas las operaciones de eliminación en Tabular Editor 3 se pueden deshacer con CTRL+Z.

### Preferencias de columnas

Configura qué columnas son visibles en las vistas de varias columnas y su orden de visualización.

## Tabular Editor > Copiar/Pegar

![Marcador de posición: Captura de pantalla de la página de preferencias de Copiar/Pegar]

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

![Marcador de posición: captura de pantalla de la página de preferencias de perspectivas]

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

![Marcador de posición: captura de pantalla de la página de preferencias de Comparación de esquemas]

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

![Marcador de posición: captura de pantalla de la página de preferencia de Guardar en carpeta]

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

Selecciona qué tipos de objetos se deben serializar en cada nivel de carpeta. Esto te permite organizar los archivos del modelo en una estructura jerárquica.

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

## Exploración de datos > General

![Marcador de posición: Captura de pantalla de la página de preferencias de Exploración de datos > General]

##### _Actualizar automáticamente la vista previa de datos_ (activado)

Actualiza automáticamente las ventanas de Vista previa de tabla cuando se guardan los cambios en el modelo. Esta función es muy útil al depurar: actualiza una expresión en una ventana mientras mantienes abierta una vista previa de tabla en otra. Cada vez que pulses CTRL+S, la vista previa se actualizará automáticamente.

##### _Ejecutar automáticamente consultas DAX_ (activado)

Ejecuta automáticamente las consultas DAX cuando se guardan cambios en el modelo. Al igual que la actualización automática de la vista previa de datos, esto te permite ver el impacto inmediato de los cambios en medidas o columnas calculadas.

##### _Selección inteligente de consultas DAX_ (activado)

Al ejecutar una selección parcial en una consulta DAX, determina de forma inteligente el contexto de la consulta. Esto te permite ejecutar solo una parte de tu consulta para probarla.

##### _Mantener el filtrado y la ordenación en los resultados de las consultas DAX_ (WhenQueryUnchanged)

Controla si se deben conservar los filtros y la ordenación de la cuadrícula al volver a ejecutar consultas:

- **Nunca**: La ordenación y el filtrado siempre se restablecen cuando se ejecuta una consulta
- **WhenQueryUnchanged**: La ordenación y el filtrado se restablecen solo cuando se modifica la consulta
- **Siempre**: La ordenación y el filtrado nunca se restablecen si las columnas siguen existiendo

##### _Máximo de filas en DirectQuery_ (100)

Número máximo de filas que se pueden recuperar en modo DirectQuery. Ajusta este valor si necesitas previsualizar más datos, pero ten en cuenta el rendimiento.

##### _Máximo de filas en consultas DAX_ (1000)

Número máximo de filas que se pueden recuperar para las consultas DAX. Aumenta este valor si necesitas analizar conjuntos de resultados más grandes.

## Exploración de datos > Pivot Grid

![Marcador de posición: captura de pantalla de la página de preferencia de Pivot Grid]

##### _Actualización automática de Pivot Grid_ (activada)

Actualiza automáticamente las cuadrículas Pivot Grid cuando se guardan los cambios del modelo. Al igual que con las consultas DAX, esto te permite ver al instante el impacto de los cambios en las medidas.

##### _Diseño predeterminado para la personalización de Pivot Grid_ (StackedDefault)

Elige el diseño predeterminado para la lista de campos de la Pivot Grid. Las opciones incluyen:

- **StackedDefault**: Campos y áreas en un único panel apilado
- **StackedSideBySide**: Campos y áreas en paneles en paralelo
- **TopPanelOnly**: Lista de campos solo en la parte superior
- **BottomPanelOnly2by2**: Lista de campos en una cuadrícula 2x2 en la parte inferior
- **BottomPanelOnly1by4**: Lista de campos en un diseño 1x4 en la parte inferior

##### _Mostrar todos los campos en la personalización del Pivot Grid_ (habilitado)

Muestra de forma predeterminada todos los campos disponibles en la lista de campos del Pivot Grid, incluidos los campos ocultos.

##### _Ajuste de línea en los encabezados del Pivot Grid_ (habilitado)

Habilita el ajuste de línea en los encabezados del Pivot Grid. Esto hace que los nombres de campo largos sean más legibles.

##### _Avisar si los campos del Pivot Grid no coinciden_ (habilitado)

Muestra una advertencia cuando las definiciones de campos del Pivot Grid no coinciden con el modelo actual. Esto puede ocurrir si has eliminado o cambiado el nombre de los campos usados en un Pivot Grid guardado.

##### _Mostrar siempre la lista de campos del Pivot Grid_ (habilitado)

Mantén visible, de forma predeterminada, la lista de campos del Pivot Grid. Desactiva esta opción si prefieres disponer de más espacio en pantalla para el propio Pivot Grid.

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

Esta opción controla específicamente si debe aplicarse el formato automático de las llamadas a funciones (espaciado entre argumentos y paréntesis) al cerrar un paréntesis.

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

Esta configuración permite cambiar el uso de mayúsculas/minúsculas de las palabras clave, como `ORDER BY`, `VAR`, `EVALUATE`, etc.

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

_Disparador de sugerencias de llamada_

## Editor de DAX > Code Assist

![Marcador de posición: Captura de pantalla de la página de preferencias de Code Assist del Editor de DAX]

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

![Marcador de posición: captura de pantalla de la página de preferencias de Acciones de código del Editor de DAX]

Configura sugerencias automáticas de mejora de código:

##### _Prefijos de variables_

Define prefijos aceptables para nombres de variables (p. ej., `_`, `__`, `var_`, `var`, `v_`, `v`, `VAR_`). Las acciones de código sugerirán añadir estos prefijos a los nombres de variables que no sigan la convención.

##### _Prefijos de columnas_

Define prefijos aceptables para nombres de columnas temporales (p. ej., `@`, `_`, `x`, `x_`). Las acciones de código sugerirán añadir estos prefijos a los nombres de columnas temporales que no sigan la convención.

## Editor SQL / Editor M / Editor de C\\\#

![Marcador de posición: captura de pantalla de las páginas de preferencias de los editores SQL/M/C#]

Hay opciones de configuración similares para los editores de scripts SQL, M (Power Query) y C# Script, entre ellas:

- Resaltado de sintaxis y esquemas de color
- Opciones de formato automático
- Funciones de Code Assist y autocompletado
- Estilos de comentarios y preferencias de sangría

Cada editor se puede personalizar de forma independiente para ajustarse a tu estilo de programación preferido.

## DAX Formatter

![Marcador de posición: Captura de pantalla de la página de preferencias de DAX Formatter]

##### _Consentimiento para DAX Formatter_ (deshabilitado)

Aceptar enviar el código DAX al servicio externo de formato DAX (www.daxformatter.com). Cuando está habilitado, puedes usar este servicio para dar formato al código DAX según los estándares de la comunidad.

##### _Tiempo de espera de la solicitud de DAX Formatter_ (5000)

Tiempo de espera, en milisegundos, para las solicitudes a DAX Formatter. Aumentar este valor si a menudo recibes errores de tiempo de espera al usar DAX Formatter.

## Integración con el Optimizador de DAX

![Marcador de posición: Captura de pantalla de la página de preferencias de la integración con el Optimizador de DAX]

Configura la integración con el Optimizador de DAX (solo en la Edición Enterprise):

##### _Conectar automáticamente_ (null/prompt)

Conectar automáticamente con el Optimizador de DAX cuando esté disponible. Si no lo configuras, se te preguntará la primera vez.

##### _Ofuscar archivos VPAX_ (habilitado)

Anonimizar los metadatos del modelo al enviarlos al Optimizador de DAX. Esto protege información confidencial como nombres de tablas y columnas, sin impedir el análisis.

##### _Directorio del diccionario de ofuscación_ (`%LocalAppData%\\TabularEditor3\\DaxOptimizer`)

Especifica dónde se almacenan los diccionarios de ofuscación. El diccionario mantiene una ofuscación coherente en varios análisis.

## Analizador VertiPaq

![Marcador de posición: Captura de pantalla de la página de preferencias del Analizador VertiPaq]

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

![Marcador de posición: Captura de pantalla de la página de preferencias de integración con Power BI]

##### _URL base del punto de conexión de Power BI_ (`https://api.powerbi.com`)

La URL base para las llamadas a la API de Power BI. Cámbiala si estás trabajando con una nube soberana o un entorno personalizado.

##### _URL base del punto de conexión de Fabric_ (`https://api.fabric.microsoft.com`)

La URL base para las llamadas a la API de Microsoft Fabric. Cambia esto si trabajas con una nube soberana o un entorno personalizado.

##### _Usar el navegador integrado para la autenticación_ (activado)

Usa el navegador integrado para la autenticación OAuth en lugar del navegador del sistema. Esto ofrece una experiencia más Integrada.

## Configuración del proxy

![Marcador de posición: captura de pantalla de la página de preferencias de configuración del proxy]

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
