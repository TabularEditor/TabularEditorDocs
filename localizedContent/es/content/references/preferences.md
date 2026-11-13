---
uid: preferences
title: Control de las preferencias
author: Morten Lønskov
updated: 2026-10-19
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

El cuadro de diálogo «Preferencias» controla la interfaz de usuario de Tabular Editor 3, los formatos de archivo, la conectividad, la navegación por los datos, las funciones de IA y el comportamiento del editor.

Este artículo describe los cuadros de diálogo de Preferencias de Tabular Editor 3 y los ajustes que puede controlar a través de ellos.

Para acceder al cuadro de diálogo de preferencias, vaya a **Herramientas > Preferencias**.

> [!NOTE]
> Todas las preferencias de Tabular Editor se almacenan para cada perfil de usuario de Windows, en la carpeta `%localappdata%\TabularEditor3`. Es posible migrar su configuración a otro equipo simplemente copiando el contenido de esta carpeta.

> [!TIP]
> Utilice el cuadro de búsqueda situado en la parte superior del cuadro de diálogo Preferencias para encontrar rápidamente ajustes específicos.

## Tabular Editor > Funciones

![Preferencias > Funciones generales](~/content/assets/images/pref-general-features.png)

### Power BI

**Permitir la edición no admitida** (deshabilitada): se aplica únicamente a las versiones de Power BI Desktop anteriores a junio de 2025, que restringen las operaciones de modelado que puede realizar una herramienta externa. Cuando está marcada, todas las propiedades TOM están disponibles para su edición mientras Tabular Editor 3 está conectado a dicha versión, incluidos los cambios que [Power BI Desktop no admite](xref:desktop-limitations). Esta configuración no tiene ningún efecto en Power BI Desktop de junio de 2025 o posterior.

**Ocultar advertencias de fecha/hora automática** (desactivado): cuando está marcada, oculta las advertencias sobre las tablas de fecha/hora automática de Power BI. Estas advertencias aparecen cuando está habilitada la configuración «Fecha/hora automática» en Power BI Desktop, que crea tablas calculadas que activan advertencias en el analizador DAX integrado de Tabular Editor 3.

**Salto de línea en la primera línea de DAX** (deshabilitado): En Power BI Desktop es habitual insertar un salto de línea en la primera línea de una expresión DAX, debido a la forma en que la barra de fórmulas muestra el código DAX. Si sueles pasar de Tabular Editor a Power BI Desktop y viceversa, plantéate activar esta opción para que Tabular Editor 3 inserte el salto de línea automáticamente.

**Solo para expresiones DAX de varias líneas** (habilitado): Cuando está habilitada la opción «Salto de línea en la primera línea de DAX», este subajuste controla si el salto de línea se añade solo para las expresiones DAX de varias líneas. Cuando está marcado, las expresiones de una sola línea no se modifican.

**Modo de autenticación predeterminado de Power BI** (Integrado): Seleccione el método de autenticación predeterminado (Integrado, ServicePrincipal o MasterUser) a utilizar al conectarse a conjuntos de datos de Power BI.

### Best Practice Analyzer

**Buscar violaciones de mejores prácticas en segundo plano** (habilitado): Ejecuta el Analizador de mejores prácticas en un subproceso en segundo plano cada vez que cambia el modelo. Si la desactiva, ejecute el análisis desde la ventana **Best Practice Analyzer**. En modelos grandes o con reglas complejas, el análisis en segundo plano ralentiza la edición.

**Reglas integradas del BPA** (habilitadas para nuevos usuarios): Elige si quieres habilitar, deshabilitar o que se te pregunte sobre el uso de las reglas integradas del Best Practice Analyzer de Tabular Editor. Las reglas integradas abarcan las principales prácticas recomendadas en materia de formato, metadatos, diseño del modelo, expresiones DAX y traducciones. En las nuevas instalaciones, las reglas integradas estarán habilitadas de forma predeterminada.

### Notificaciones

**Notificación de actualización de datos** (habilitada): Cuando está marcada, se muestra una notificación cuando se completa una operación de actualización de datos.

### Corrección de fórmulas DAX

**Habilitar corrección de fórmulas** (habilitado): Ajusta automáticamente las referencias en las expresiones DAX cuando se cambian de nombre o se mueven los objetos. Esta función garantiza que tu código DAX siga siendo válido cuando reorganices tu modelo.

**Habilitar la corrección de fórmulas al pegar** (habilitado): Ajusta automáticamente las referencias en las expresiones DAX al pegar objetos. Esto es útil cuando se copian medidas o columnas calculadas entre tablas o modelos.

## Tabular Editor > Actualizaciones y comentarios

![Preferencias de actualizaciones y comentarios](~/content/assets/images/pref-updates-and-feedback.png)

### Actualizaciones

**Mostrar página «Primeros pasos» en actualizaciones** (habilitado): Cuando está marcada, la página **Primeros pasos** se abre automáticamente la primera vez que ejecutas Tabular Editor después de que se haya actualizado. Aparece **en las actualizaciones**, no en cada inicio. Puedes abrirla en cualquier momento desde **Ayuda > Introducción**.

**Buscar actualizaciones al iniciar** (habilitado): Busca una nueva versión cuando se inicia la aplicación.

**Solo actualizaciones principales** (desactivada): cuando está marcada, solo las actualizaciones de versiones principales activan notificaciones. Las actualizaciones menores y los parches se ignoran. Este ajuste solo está disponible cuando la opción **Buscar actualizaciones al iniciar** está marcada.

La versión que estás ejecutando se muestra debajo de estos ajustes, junto con un botón **Buscar actualizaciones** que ejecuta la búsqueda inmediatamente.

### Gestionado por tu organización

Cuando un administrador ha configurado [políticas](xref:policies), se añade a esta página una sección de solo lectura, **Gestionado por su organización**, en la que se enumeran todos los valores de las políticas que Tabular Editor ha encontrado, en forma de `Name = value`. Pase el cursor sobre una entrada para ver de qué clave de registro y de qué subárbol procede.

Un valor que Tabular Editor no ha podido interpretar se muestra con el marcador `(invalid)` en lugar de omitirse. Ese marcador es la forma más rápida de encontrar el error tipográfico detrás de una política que parece no hacer nada, así que compruebe aquí primero cuando una política no surta efecto.

La sección no aparece cuando no se aplica ninguna directiva. Los ajustes que una política bloquea o limita se muestran en modo de solo lectura en otra parte de este cuadro de diálogo y en el cuadro de diálogo **Herramientas > Servidor MCP...**, con una información sobre herramientas que así lo indica.

### Datos de uso y comentarios

**Ayudar a mejorar Tabular Editor recopilando datos de uso anónimos** (habilitado): Los datos no contienen ninguna información de identificación personal, ni ninguna información sobre la estructura o el contenido de sus modelos de datos. Desmárcala para no participar en la telemetría.

**Enviar informes de errores** (habilitado): En caso de bloqueos, Tabular Editor muestra una opción para enviar un informe de bloqueo cuando esta opción está marcada.

## Tabular Editor > Valores predeterminados

<!-- SE NECESITA IMAGEN: pref-defaults.png
     La página de preferencias Tabular Editor > Valores predeterminados con su configuración predeterminada.
     Texto alternativo: «La página de preferencias de Valores predeterminados» -->

**Nivel de compatibilidad de modelo nuevo** (1600): Establezca el nivel de compatibilidad predeterminado para los modelos recién creados. Las opciones son las mismas que en el cuadro de diálogo **Nuevo modelo**:

| Nivel | Objetivo |
|---|---|
| 1200 | Azure Analysis Services / SQL Server 2016 o posterior |
| 1400 | Azure Analysis Services / SQL Server 2017 o posterior |
| 1500 | Azure Analysis Services / SQL Server 2019 o posterior |
| 1600 | Azure Analysis Services / SQL Server 2022 o posterior |
| 1700 | Azure Analysis Services / SQL Server 2025 o posterior |
| 1706 | Power BI / Fabric |

1700 es el nivel más alto que admite Analysis Services; 1706 es el nivel más alto en general y solo está disponible para Power BI y Fabric.

**Usar el nivel de compatibilidad más reciente como predeterminado** (habilitado): Usar automáticamente el nivel de compatibilidad más reciente disponible para los nuevos modelos. Cuando está habilitado, esto anula la configuración del nivel de compatibilidad específico anterior y el menú desplegable queda deshabilitado.

**Los nuevos modelos usan la base de datos del área de trabajo** (habilitado): Al crear un nuevo modelo, se crea automáticamente una base de datos del área de trabajo en Analysis Services. Esto te permite probar y consultar tu modelo de inmediato durante el desarrollo.

**Modo de guardado predeterminado** (AlwaysAsk): Elija si desea guardar siempre como archivo (.bim), carpeta (varios archivos JSON), TMDL (lenguaje de definición de modelo tabular) o si prefiere que se le pregunte siempre al guardar. Opciones: AlwaysAsk, File, Folder, TMDL.

**Usar el nombre del archivo PBIX al guardar en el disco** (habilitado): Al guardar un modelo cargado desde un archivo PBIX, usar el nombre del archivo PBIX como valor predeterminado. Esto mantiene la coherencia en la nomenclatura entre los archivos de Power BI y los metadatos del modelo guardado.

**Crear opciones de usuario para nuevos modelos** (habilitado): Crea automáticamente archivos .tmuo (Opciones de usuario del modelo tabular) para nuevos modelos. Estos archivos almacenan ajustes específicos del usuario, como los diseños de los diagramas y las posiciones de las ventanas.

## Tabular Editor > Teclado

![Asignaciones de teclado](~/content/assets/images/keyboard-mappings.png)

Configure los accesos directos de teclado para todos los comandos de Tabular Editor. Utiliza la función de búsqueda para encontrar rápidamente comandos específicos y asignar o modificar sus atajos de teclado para que coincidan con tu flujo de trabajo preferido.

## Tabular Editor > Interfaz de usuario

Controle las barras de herramientas y los menús, la cantidad de ubicación de origen del modelo que se muestra, el diseño de las ventanas, el idioma, la accesibilidad y las listas de elementos recientes.

<!-- MARCADOR DE POSICIÓN DE CAPTURA DE PANTALLA (3.27.1): nueva imagen pref-user-interface.png. Herramientas > Preferencias > Tabular Editor > Interfaz de usuario con los detalles de la ubicación de origen del modelo visibles. Insertar como ![Preferencias de la interfaz de usuario](~/content/assets/images/pref-user-interface.png). -->

### Barras de herramientas y menús

**Mostrar barras de herramientas en ventanas flotantes** (habilitado): Muestra las barras de herramientas en los documentos y vistas que desacople en ventanas flotantes.

**Ocultar barras de herramientas inactivas** (habilitado): Oculta las barras de herramientas que no se aplican al documento o a la vista activos.

**Ocultar menús inactivos** (habilitado): Oculta los [menús dinámicos](xref:user-interface#dynamic-menus-context-dependent) que no se aplican al documento o a la vista activos.

**Ocultar número de versión** (desactivado): Oculta el número de compilación y versión de Tabular Editor 3 de la barra de título.

**Detalle de la fuente del modelo** (Ruta completa): Establezca qué parte de la ubicación de origen del modelo cargado aparece en la barra de título, en el elemento de conexión de la barra de estado, en las información sobre herramientas de las pestañas de los documentos y en el texto que aparece al pasar el cursor por los menús de archivos y modelos recientes:

- **Ruta completa**: el nombre del modelo con su ruta completa, servidor o ubicación del espacio de trabajo.
- **Solo nombre**: el nombre del archivo, el nombre de la carpeta o el nombre de la base de datos, sin rutas ni nombres de servidores.
- **Oculto**: ni el nombre del modelo ni su ubicación. La barra de título muestra **Modelo cargado** y la barra de estado muestra **Conectado** cuando está conectado a un servidor.

Los agentes conectados a través del @mcp-server reciben el título del modelo en el mismo nivel. Si seleccionó **Ocultar detalles de origen del modelo** en una versión anterior, este ajuste estará **Oculto**.

### Buscar y reemplazar

**Opacidad del cuadro de diálogo cuando está inactivo** (70 %): Opacidad del cuadro de diálogo **Buscar y reemplazar** cuando no tiene el foco.

### Diseño

**Recordar si la ventana está maximizada** (habilitado): Restaura el estado maximizado de la ventana principal cuando se inicia Tabular Editor 3.

**Recordar posición y tamaño de la ventana** (habilitado): Restaura la posición y el tamaño de la ventana principal cuando se inicia Tabular Editor 3.

### Idioma

**Idioma de la interfaz de usuario** (inglés): El idioma de la interfaz de usuario. Reinicie Tabular Editor 3 para aplicar un cambio.

### Accesibilidad

**Modo daltonismo** (desactivado): Marque los objetos añadidos desde el último guardado en color turquesa donde de otro modo serían verdes, en los indicadores de cambios del **Explorador TOM** y en la vista de comparación de modelos. Consulte @accessibility.

### Elementos recientes

**Usar rutas de archivo compactas** (habilitado): Acorta las rutas de archivo largas en los menús de archivos y modelos recientes. Con **Detalle de origen del modelo** establecido como **Ruta completa**, la parte de la ubicación de la barra de título también se acorta.

**Número de archivos recientes mostrados** (10): El número máximo de archivos en el menú de archivos recientes, hasta 50.

**Número de modelos recientes mostrados** (10): El número máximo de modelos en el menú de modelos recientes, hasta 50.

**Número de servidores recientes mostrados** (10): El número máximo de servidores en la lista **Servidor** cuando se conecta a un modelo semántico, hasta 50. Los servidores anclados no se cuentan y siempre permanecen en la lista. Consulta @xmla-as-connectivity.

**Borrar archivos recientes**, **Borrar modelos recientes**, **Borrar servidores recientes** y **Borrar todos los elementos recientes**: Borra las listas correspondientes. **Borrar servidores recientes** y **Borrar todos los elementos recientes** conservan los servidores anclados y sus ajustes guardados.

## Tabular Editor > Explorador TOM

![Configuración del Explorador TOM](~/content/assets/images/unsaved-changes/preferences.png)

Controle cómo presenta el modelo el Explorador TOM (Tabular Object Model) y qué sucede con los objetos que elimina.

Los botones de activación/desactivación que deciden qué tipos de objetos aparecen en el árbol, como medidas, columnas, jerarquías, particiones, carpetas de visualización y objetos ocultos, no son preferencias. Se encuentran en la barra de herramientas @tom-explorer-view, donde puede cambiarlos por modelo sin abrir este cuadro de diálogo.

### Visualización y filtrado

**Usar grupos de tablas** (habilitado): Agrupe sus tablas en el Explorador TOM, por ejemplo, para mantener separados los grupos de cálculos, las dimensiones y las tablas de hechos. Tabular Editor registra el grupo de una tabla en una anotación en la propia tabla, de modo que la agrupación viaja con el modelo. Es interna a Tabular Editor: ninguna otra herramienta cliente, incluido Power BI Desktop, la muestra. Consulte @table-groups.

**Mostrar rama completa** (desactivado): Cuando filtra el árbol, Tabular Editor muestra los objetos que coinciden con su cadena de filtro junto con sus elementos principales. Habilite esta opción para mostrar también todos los elementos secundarios de una coincidencia, independientemente de que los elementos secundarios coincidan o no con la cadena.

**Resaltar relaciones** (habilitado): Resalta las relaciones que involucran la tabla o columna que ha seleccionado, para que pueda ver de un vistazo a qué está unida una columna.

### Cambios sin guardar

Estos ajustes controlan cómo se indican los [cambios sin guardar](xref:unsaved-changes) en el Explorador TOM y en la vista Propiedades.

**Marcar objetos con cambios no guardados** (habilitado): Resalta los objetos en el Explorador TOM que difieren de la última versión guardada del modelo, usando una fila coloreada y una insignia en el icono del objeto: naranja para los objetos modificados, verde para los objetos añadidos y rojo para los objetos eliminados. Las tablas, las carpetas y los grupos que contengan objetos modificados se rellenarán con un sombreado de rayas. Cuando está desactivada, los objetos eliminados siguen siendo visibles según la configuración que se indica a continuación, y el filtro **Mostrar cambios** de la barra de herramientas sigue funcionando. Use el **Modo daltonismo** en **Interfaz de usuario > Accesibilidad** para marcar los objetos añadidos en color azul verdoso en lugar de verde.

**Mantener visibles los objetos eliminados** (hasta que se guarde el modelo): cuánto tiempo permanecen visibles los objetos eliminados en el Explorador TOM, tachados, en el lugar donde solían estar. Haga clic derecho en un objeto eliminado y elija **Restaurar** para recuperarlo. Opciones:

- **Nunca**: Los objetos eliminados desaparecen del Explorador TOM de inmediato.
- **Hasta que se guarde el modelo**: Los objetos eliminados se tratan como cambios sin guardar y desaparecen cuando se guarda el modelo.
- **Hasta que se cierre el modelo**: Los objetos eliminados permanecen visibles y se pueden restaurar durante toda la sesión de edición, incluso después de guardar el modelo.

**Reunir los objetos eliminados bajo un nodo «Objetos eliminados»** (deshabilitado): Mostrar los objetos eliminados de una tabla, jerarquía, rol o grupo de tablas juntos bajo un único nodo **Objetos eliminados** al final de su contenedor, en lugar de cada uno donde solía estar. Haga clic derecho en el nodo y elija **Restaurar** para recuperarlos todos a la vez.

**Marcar las propiedades con cambios no guardados en el panel «Propiedades»** (habilitado): Resalta las propiedades de la vista «Propiedades» que difieren de la última versión guardada del modelo, usando una fila coloreada. Cuando está desactivado, el filtro de la barra de herramientas **Mostrar cambios** de la vista Propiedades sigue funcionando.

### Eliminar

**Mostrar siempre advertencias de eliminación** (deshabilitado): Le pide que confirme cada eliminación de objetos. Cuando está desactivada, solo aparece una confirmación para las eliminaciones de varios objetos y para los objetos a los que hacen referencia otros objetos.

> [!NOTE]
> Todas las operaciones de eliminación en Tabular Editor 3 se pueden deshacer pulsando CTRL+Z.

### Localización

Estos ajustes determinan la cadena de formato que escribe Tabular Editor cuando elige el formato numérico **Moneda** para un objeto en el panel Propiedades.

**Moneda predeterminada** (inglés (Estados Unidos)): la convención de formato en la que se basa la cadena de formato de moneda. Elija la configuración regional cuyo símbolo de moneda, separador decimal y agrupación de dígitos desee.

**Usar un símbolo de moneda personalizado** (desactivado): Proporcione su propio símbolo en lugar de tomar uno de la configuración regional anterior. Los tres ajustes siguientes solo se aplican mientras esta opción esté marcada.

**Símbolo de moneda personalizado**: El símbolo que se usará. Introduzca el símbolo por sí solo, sin el número; se ignoran los espacios en blanco.

**Posición del símbolo de moneda personalizado** (antes del número): si el símbolo va antes o después del valor numérico.

**Poner un espacio entre el número y el símbolo** (desactivado): Separe el símbolo del valor numérico con un espacio.

## Tabular Editor > Copiar/Pegar

<!-- IMAGEN NECESARIA: pref-copy-paste.png
     La página de preferencias Tabular Editor > Copiar/Pegar con su configuración predeterminada.
     Texto alternativo: «La página de preferencias de Copiar/Pegar» -->

Controlar qué metadatos se incluyen al copiar objetos:

**Incluir traducciones** (habilitado): Copiar los metadatos de las traducciones junto con los objetos. Cuando está habilitada, también se copiarán todas las traducciones definidas para el objeto copiado.

**Incluir perspectivas** (habilitado): Copiar la pertenencia a perspectivas junto con los objetos. Cuando está habilitado, el objeto copiado pertenecerá a las mismas perspectivas que el original.

**Incluir RLS** (habilitado): Copiar las expresiones de seguridad a nivel de filas junto con los objetos. Esto se aplica al copiar tablas que tienen definidas reglas de RLS.

**Incluir OLS** (habilitado): Copiar los ajustes de seguridad a nivel de objeto junto con los objetos. Esto se aplica al copiar objetos que tienen restricciones de OLS.

## Tabular Editor > Perspectivas

<!-- SE NECESITA IMAGEN: pref-perspectives.png
     La página de preferencias Tabular Editor > Perspectivas con su configuración predeterminada.
     Texto alternativo: «La página de preferencias de Perspectivas» -->

Controle cómo se gestiona la pertenencia a perspectivas:

**Heredar pertenencia a perspectiva para objetos nuevos** (desactivada): Los objetos recién creados heredan automáticamente la pertenencia a perspectiva de su elemento principal. Por ejemplo, una nueva medida se añadiría automáticamente a las mismas perspectivas que su tabla principal.

**Heredar pertenencia a perspectiva para objetos reubicados** (desactivado): Los objetos que se mueven heredan la pertenencia a perspectiva de su nuevo elemento principal. Esto es útil cuando se reorganiza la estructura de tu modelo.

**Heredar al agregar una tabla a una perspectiva** (habilitado): Agregar automáticamente todos los objetos de la tabla (columnas, medidas, jerarquías) cuando se agrega una tabla a una perspectiva.

**Heredar al quitar una tabla de una perspectiva** (habilitado): Quitar automáticamente todos los objetos de la tabla cuando se quita una tabla de una perspectiva.

## Tabular Editor > Comparación de esquemas

![Preferencias de comparación de esquema](~/content/assets/images/pref-schema-compare.png)

Configure qué cambios se ignoran durante la comparación de esquemas al actualizar los esquemas de tabla:

**Ignorar cambios en el modo de importación** (desactivado): No marcar los cambios en las propiedades del modo de importación. Habilite esto si desea ignorar los cambios entre los modos Importación, DirectQuery y Dual durante la comparación de esquemas.

**Ignorar cambios en tipo de datos** (deshabilitado): No marcar cambios en tipo de datos de columnas. Habilite esto si desea ignorar los cambios en el tipo de datos durante la comparación de esquemas.

**Ignorar cambios en la descripción** (desactivado): No marcar los cambios en las descripciones de los objetos. Habilite esto si no desea ver los cambios en la descripción en la comparación de esquemas.

**Ignorar cambios de decimal a doble** (deshabilitado): No marcar cambios entre los tipos de datos decimal y doble. Esto resulta útil cuando se trabaja con Data source que no distinguen entre estos tipos.

**Dar prioridad al detector de esquemas de Analysis Services** (deshabilitado): Usar los metadatos de Analysis Services como fuente de referencia para la detección de esquemas. Cuando está habilitada, la detección de esquemas consulta directamente a la instancia de Analysis Services.

## Tabular Editor > Guardar en carpeta/archivo

![Preferencias de Guardar en carpeta](~/content/assets/images/pref-save-to-folder.png)

### Modo de serialización

**Usar el formato TMDL** (deshabilitado): Guarde los metadatos del modelo utilizando el formato del Lenguaje de definición de modelo tabular (TMDL) en lugar de JSON. TMDL es el formato moderno recomendado para el control de versiones y la colaboración.

**Usar la configuración de serialización recomendada** (habilitada): Aplica la configuración recomendada para la serialización basada en carpetas (anula la configuración personalizada). Cuando está habilitado, Tabular Editor utiliza las mejores prácticas para guardar modelos en carpetas, optimizadas para el control de versiones.

### Configuración de serialización heredada (JSON)

**Añadir prefijos a los nombres de archivo** (desactivado): Añadir prefijos numéricos a los nombres de archivo para ordenarlos. Esto puede ayudar a mantener un orden de archivos coherente en los exploradores de archivos.

**Relaciones locales** (habilitado): almacena las definiciones de las relaciones con tablas individuales en lugar de en una ubicación central. Esto facilita ver qué relaciones pertenecen a cada tabla cuando se utiliza el control de versiones.

**Perspectivas locales** (habilitadas): Almacenar la pertenencia a perspectivas con objetos individuales en lugar de en una ubicación central. Esto reduce los conflictos de fusión en el control de versiones.

**Traducciones locales** (habilitadas): Almacenar las traducciones con objetos individuales en lugar de en una ubicación central. Esto reduce los conflictos de fusión en el control de versiones.

**Niveles**: Seleccione qué tipos de objetos serializar en diferentes niveles de carpetas. Esto te permite organizar los archivos de tu modelo en una estructura jerárquica. Los niveles disponibles son: fuentes de datos, funciones definidas por el usuario (UDF), expresiones compartidas, perspectivas, relaciones, roles, tablas, columnas, jerarquías, medidas, particiones, elementos de cálculo y traducciones.

**Ignorar objetos inferidos** (habilitado): No serializar los objetos que el motor infiere automáticamente. Esto reduce el desorden en los metadatos guardados.

**Ignorar propiedades inferidas** (habilitado): No serializar las propiedades que el motor infiere automáticamente. Esto mantiene los metadatos guardados limpios y centrados en los valores establecidos explícitamente.

**Ignorar marcas de tiempo** (habilitado): No serializar los metadatos de las marcas de tiempo. Esto es muy recomendable para el control de versiones, ya que evita cambios innecesarios en cada confirmación.

**Ignorar etiquetas de linaje** (desactivado): No serializar los metadatos de las etiquetas de linaje de Power BI. Habilite esto si no desea que haya información de linaje en sus metadatos guardados.

**Ignorar configuración de privacidad** (deshabilitado): No serializar la configuración de privacidad del origen de datos. Habilite esto si gestiona la configuración de privacidad por separado.

**Incluir datos sensibles** (desactivado): Incluir información sensible, como contraseñas, en los metadatos serializados. No se recomienda por motivos de seguridad.

**Ignorar particiones de actualización incremental** (deshabilitado): No serializar las particiones creadas por las políticas de actualización incremental. Habilite esto si desea que la actualización incremental se gestione por separado de sus metadatos guardados.

**Dividir cadenas de varias líneas** (habilitado): Divide los valores de cadenas largas en varias líneas para mejorar la legibilidad en el control de versiones. Esto facilita la visualización de los cambios en las expresiones DAX y en otras propiedades de texto largo.

**Ordenar matrices** (desactivado): Ordene los elementos de las matrices alfabéticamente para lograr una serialización coherente. Reduce las diferencias de ordenación en el control de versiones y cambia el orden de algunos elementos.

### Configuración de serialización de TMDL

**Modo de sangría** (tabulaciones): Elija entre tabulaciones o espacios para la sangría en los archivos TMDL. Las tabulaciones son la opción predeterminada y recomendada.

**Espacios de sangría** (4): Cuando utilice espacios, especifique el número de espacios por nivel de sangría.

## Funciones de IA

La página principal contiene los dos ajustes que se aplican a todas las funciones de IA, tanto al chat como al [servidor MCP](xref:mcp-server).

**Buscar actualizaciones de la base de conocimientos al iniciar** (habilitado): El Asistente de IA busca una copia local de la documentación de Tabular Editor. Cuando está marcada esta opción, Tabular Editor busca una copia más reciente al iniciar y la descarga si hay una disponible. Esta es la única solicitud saliente que cualquier función de IA realiza por sí sola.

**Registro de auditoría**: **Abrir carpeta de auditoría** abre el registro de este ordenador sobre lo que hicieron el Asistente de IA y el servidor MCP: decisiones sobre permisos, qué herramientas se invocaron y cómo finalizó cada una, y el texto completo de cualquier script que se ejecutó o se entregó para su revisión. Las indicaciones, las respuestas y los valores de los datos nunca se registran. El registro es una función de la Edición Enterprise: en las ediciones Desktop y Business no se registra nada y el botón no se muestra. Consulta @ai-audit-log.

## Funciones de IA > Asistente de IA

Configuración de conexión para el chat del Asistente de IA. La página secundaria **Proveedor de IA** se muestra aquí. Consulta @ai-assistant para saber qué necesita cada proveedor.

**Elegir proveedor** (Ninguno): Con qué proveedor de IA se comunica el chat: **OpenAI**, **Anthropic**, **Azure OpenAI** o **Personalizado (compatible con OpenAI)**. Los campos que aparecen a continuación cambian en función de tu elección. Un administrador puede bloquear esto para que solo se use un único proveedor o reducir la lista mediante una directiva.

**URL base** / **Punto de conexión del servicio**: A dónde se envían las solicitudes. OpenAI y Anthropic proporcionan un valor predeterminado y el campo es opcional. Azure OpenAI y Personalizado no tienen ningún valor predeterminado, por lo que se requiere un punto de conexión.

**Clave de API**: Tu propia clave para el proveedor elegido. Se almacena cifrada en esta máquina en `Preferences.json`. Tabular Editor no incluye ninguna clave integrada y nunca actúa como proxy de tus solicitudes.

**ID de organización de OpenAI** e **ID de proyecto de OpenAI**: Opcionales y solo se muestran para el proveedor OpenAI. Úselos cuando su cuenta de OpenAI facture o determine el uso por organización o proyecto.

**Nombre del modelo** (**Despliegue** para Azure OpenAI): Qué modelo usar. En el caso de OpenAI y Anthropic, se trata de un menú desplegable que se rellena a partir de un catálogo en línea, por lo que está vacío hasta que se haya descargado el catálogo una vez en este equipo. En Azure OpenAI, el campo se denomina **Despliegue** y adopta el nombre que le dio al despliegue, que no es necesariamente el nombre del modelo subyacente. Si lo deja en blanco, se utilizará el valor predeterminado del proveedor, excepto en el caso de Azure OpenAI y Personalizado, que no tienen ninguno.

## Funciones de IA > Asistente de IA > Preferencias

Cómo se comporta el chat. Consulta @ai-assistant para obtener más detalles sobre cada grupo.

### Visualización del chat

**Mostrar indicador del contexto de la selección** (habilitado): muestra qué objeto del modelo está seleccionado actualmente encima del chat, para que pueda ver qué considerará el asistente como contexto.

**Mostrar indicador de instrucciones personalizadas** (habilitado): Muestra qué [instrucciones personalizadas](xref:ai-assistant#custom-instructions) se aplicaron encima de cada respuesta.

**Mostrar indicador de búsqueda en la base de conocimientos** (habilitado): muestra el progreso mientras el asistente busca en la base de conocimientos.

### Compactación del contexto

**Compactación automática** (habilitada): resume automáticamente la parte más antigua de una conversación a medida que se acerca al límite de contexto del modelo, de modo que una conversación larga pueda continuar.

**Umbral de compactación automática %** (80): Indica el grado de llenado de la ventana de contexto antes de que se ejecute la compactación, como porcentaje de la ventana de contexto del modelo seleccionado. Los valores fuera del rango de 50 a 100 no tienen ningún efecto adicional.

### Script de C#

**Permitir que el asistente de IA ejecute C# Scripts directamente** (desactivado): Permite que el asistente realice el cambio de modelo que has solicitado, en lugar de escribir un script y abrirlo para que lo ejecutes. Solo se ejecutan de esta manera los scripts que el análisis de seguridad considera seguros, es decir, los scripts que afectan a objetos del modelo y nada más; cualquier script que acceda a archivos, a la red o a un ensamblado externo se te seguirá entregando para que lo revises. Cada ejecución se registra como un único paso de deshacer.

Este ajuste no está disponible hasta que **Metadatos del modelo** se establezca en **Escribir** en la página [Permisos](#ai-features--permissions), y estará disponible en cuanto cambies ese menú desplegable, sin cerrar el cuadro de diálogo. Tampoco está disponible, con una información sobre herramientas que así lo indica, cuando un administrador ha establecido la [política](xref:policies) `DisableCSharpScripts`. Está desactivado de forma predeterminada deliberadamente: **Metadatos del modelo > Escritura** es también lo que un agente necesita en el servidor MCP, y concederlo allí no debe cambiar de forma silenciosa lo que hace el chat. Consulta [Permitir que el asistente cambie tu modelo](xref:ai-assistant#letting-the-assistant-change-your-model).

**Vista previa de los cambios** (habilitada): muestra el cuadro de diálogo de vista previa del script antes de que se aplique un cambio realizado por el asistente, para que pueda ver todos los cambios en los metadatos del modelo y aceptarlos o cancelarlos. Al cancelar, se restaura el modelo y se informa al asistente de que ha rechazado el cambio.

## Funciones de IA > Servidor MCP

Configuración del [servidor MCP](xref:mcp-server), que permite que un agente externo como Claude Code, GitHub Copilot o Cursor trabaje en el modelo que tengas abierto.

![Preferencias del servidor MCP](~/content/assets/images/pref-mcp-server.png)

**Habilitar servidor MCP** (habilitado): Indica si el servidor MCP está disponible o no. Si se desactiva, se detiene un servidor en ejecución y se eliminan tanto el elemento del menú **Herramientas > Servidor MCP...** como el indicador de la barra de estado.

**Iniciar el servidor MCP automáticamente** (deshabilitado): Inicia el servidor cuando se inicie Tabular Editor, de modo que un agente pueda conectarse sin que tengas que iniciarlo manualmente. Si el puerto está en uso al iniciar, el servidor no se inicia y no se muestra ningún mensaje.

**Requerir token de acceso** (deshabilitado): hace que los agentes presenten un token al portador, que se muestra en el cuadro de diálogo **Herramientas > Servidor MCP...**. El servidor escucha solo en la interfaz de bucle invertido, por lo que esto es más importante en un equipo en el que varias personas han iniciado sesión a la vez, como un Escritorio remoto o un host Citrix, donde cada sesión puede acceder a `127.0.0.1`. Los administradores pueden aplicarlo con la [directiva](xref:policies) `RequireMcpAccessToken`.

**Puerto** (42100): El puerto de bucle invertido en el que escucha el servidor, de 1024 a 49151. Si se cambia, se invalidan los registros de agentes existentes, que apuntan a una dirección fija. Si el puerto está ocupado cuando inicia el servidor manualmente, Tabular Editor ofrece el siguiente puerto libre que encuentre.

## Funciones de IA > Permisos

Un permiso permanente por recurso, que rige tanto el chat del Asistente de IA como cualquier agente conectado a través del servidor MCP. El chat puede solicitar además algo que un permiso no cubra; un agente no puede hacerlo, por lo que, en el caso del MCP, los permisos se aplican tal cual y solo cambian cuando se reinicia el servidor.

![Preferencias de permisos de las funciones de IA](~/content/assets/images/pref-ai-permissions.png)

| Recurso | Niveles | Predeterminado | Qué cubre |
| -- | -- | -- | -- |
| **Metadatos del modelo** | Denegar / Lectura / Escritura | Lectura | Tablas, columnas, medidas, expresiones, descripciones y relaciones, además de las estadísticas del Analizador VertiPaq. El nivel «Escribir» permite realizar cambios mediante scripts de C# |
| **Datos del modelo** | Denegar / Leer | Denegar | Valores de datos de tu modelo, como los resultados de las consultas DAX. No hay nivel de escritura |
| **Best Practice Analyzer** | Denegar / Lectura / Escritura | Lectura | Lectura: consulta las reglas y ejecuta el análisis; Escritura: añade o modifica reglas |
| **Documentos** | Denegar / Lectura / Escritura | Escritura | Sus pestañas abiertas de script de C# y de consulta DAX. Lectura se refiere a su contenido; Escritura los crea o los modifica |
| **Macros** | Denegar / Lectura / Escritura | Escritura | Su biblioteca de macros |

**Escritura** abarca Lectura, por lo que no es necesario conceder ambos permisos. **Datos del modelo** es el único recurso denegado de forma predeterminada.

En las ediciones Enterprise, Consultancy y Trial, un administrador puede limitar cualquiera de estos recursos mediante [políticas](xref:policies), por separado para el chat y para el servidor MCP. Una lista desplegable limitada se muestra en modo de solo lectura. Consulte @ai-assistant para saber cómo solicita el chat lo que no cubre un permiso, y @mcp-server para saber lo que ve un agente.

<a name="miscellaneous"></a>

## Tabular Editor > Varios

![Preferencias varias](~/content/assets/images/pref-miscellaneous.png)

### Sincronización de metadatos

Estos ajustes controlan cómo gestiona Tabular Editor 3 los metadatos del modelo que cambian fuera de la aplicación. Los tres primeros se refieren a un modelo cargado desde una base de datos en una instancia de Analysis Services y se basan en un seguimiento de Analysis Services. **Volver a cargar automáticamente desde el disco** se aplica a un modelo cargado desde un archivo o una carpeta y supervisa esos archivos directamente.

**Advertir cuando los metadatos locales no estén sincronizados con el modelo implementado** (habilitado): cuando está marcada esta opción, se muestra una barra de información dentro de Tabular Editor cada vez que haya realizado cambios locales en el modelo que aún no se hayan guardado en Analysis Services. La barra desaparece cuando guarda (**Ctrl+S**).

**Rastrear cambios externos del modelo** (habilitado): Al igual que Power BI Desktop puede detectar cuándo una herramienta externa realiza un cambio en el modelo de datos, también puede hacerlo Tabular Editor. Esta opción solo es relevante para las instancias locales de Analysis Services (es decir, los procesos msmdsrv.exe que se ejecutan en el mismo equipo que Tabular Editor). Cuando está marcada, Tabular Editor inicia un seguimiento en Analysis Services y le notifica si se realizan cambios externos.

**Actualizar automáticamente los metadatos del Tabular Object Model local** (habilitada): Cuando el mecanismo de seguimiento descrito anteriormente está habilitado, esta opción permite que Tabular Editor actualice automáticamente los metadatos del modelo cuando se detecta un cambio externo. Esto resulta útil si sueles alternar entre Power BI Desktop y Tabular Editor 3.

**Volver a cargar automáticamente desde el disco** (habilitado): Cuando está marcado, Tabular Editor supervisa los archivos de metadatos desde los que se cargó el modelo y vuelve a cargar el modelo cuando otra aplicación los modifica. A diferencia de los dos ajustes anteriores, este no implica un seguimiento de Analysis Services: supervisa los propios archivos, por lo que abarca un modelo cargado desde un archivo `.bim` o desde una carpeta, independientemente de si hay un servidor implicado o no. Si el modelo tiene cambios sin guardar, Tabular Editor le preguntará qué copia desea conservar. Consulte [Recarga automática desde el disco](xref:auto-reload).

**Limpiar rastros huérfanos de Tabular Editor**: Elimina todos los rastros de Analysis Services iniciados por cualquier instancia de Tabular Editor. Úsela cuando queden rastreos después de que Tabular Editor 3 se haya cerrado inesperadamente.

> [!NOTE]
> El botón de limpieza solo está disponible cuando Tabular Editor está conectado a una instancia de Analysis Services.

## Implementación de modelo > General

![Preferencias de implementación de modelo](~/content/assets/images/pref-model-deployment.png)

### Opciones de implementación

**Agregar anotación de metadatos al implementar** (deshabilitado): Añade detalles de la implementación al modelo implementado: el usuario, el equipo cliente, la hora, la versión de Tabular Editor y el modo de implementación.

**Guardar copia de seguridad de Model.bim al implementar** (habilitado): Guarda una copia comprimida del archivo `Model.bim` del modelo en la carpeta **Ubicación de la copia de seguridad** en cada implementación. No se guarda ninguna copia de seguridad mientras **Ubicación de copia de seguridad** esté vacía.

**Ubicación de copia de seguridad**: La carpeta para las copias de seguridad de las implementaciones. Disponible cuando se selecciona **Guardar copia de seguridad de Model.bim al implementar**.

### Opciones de guardado de modelo

**Guardar copia de seguridad de Model.bim al guardar modelo** (habilitado): Guarda una copia comprimida del archivo `Model.bim` del modelo en la carpeta **Ubicación de la copia de seguridad** cada vez que guarda el modelo. No se guarda ninguna copia de seguridad mientras **Ubicación de copia de seguridad** esté vacía.

**Ubicación de copia de seguridad**: La carpeta para guardar las copias de seguridad. Disponible cuando se selecciona **Guardar copia de seguridad de Model.bim al guardar modelo**.

## Implementación de modelo > Actualización de datos

### Direct Lake

**Actualización automática al guardar nuevas tablas** (habilitada): Actualiza un modelo Direct Lake cuando lo guarda con nuevas tablas. Si la desactiva, las nuevas tablas permanecerán sin procesar hasta que actualice el modelo, y las consultas que se realicen sobre ellas recurrirán al modo DirectQuery.

## Exploración de datos > Pivot Grid

<!-- NUEVA CAPTURA DE PANTALLA (3.27.1): pref-pivot-grid.png. Muestra la sección «Mantener Pivot Grids abiertos cuando se abra un modelo diferente» y las etiquetas «Encabezados de campo» y «Lista de campos». -->
![Preferencias de Pivot Grid](~/content/assets/images/pref-pivot-grid.png)

### Básico

**Actualizar automáticamente Pivot Grids de forma predeterminada** (habilitado): Actualiza automáticamente las Pivot Grids cuando se guardan los cambios en el modelo. Al igual que con las consultas DAX, esto le permite ver inmediatamente el impacto de los cambios en las medidas.

**Mostrar advertencia si Pivot Grid no coincide con el modelo** (habilitado): Muestra una advertencia cuando un diseño de Pivot Grid utiliza campos que el modelo actual no tiene, por ejemplo, después de eliminar o cambiar el nombre de un campo, abrir un diseño guardado desde un modelo diferente o mantener un Pivot Grid abierto mientras abre un modelo diferente. El ajuste también controla la confirmación que aparece antes de que se abra un modelo diferente mientras permanecen abiertos los Pivot Grids con campos en su diseño.

### Encabezados de campo

**Ajuste de línea en encabezados de campo** (habilitado): Los encabezados de campo se ajustan a varias líneas cuando el texto del encabezado no cabe en una sola línea.

### Lista de campos

**Mostrar siempre lista de campos** (habilitado): Muestra la lista de campos cuando se crea una nueva Pivot Grid.

**Mantener campos visibles** (habilitado): Mantiene un campo en la sección Campos de la lista de campos después de añadirlo al Pivot Grid.

**Diseño** (sección de campos y sección de áreas apiladas): El diseño predeterminado de la lista de campos:

- **Sección de campos y sección de áreas apiladas**
- **Sección de campos y sección de áreas lado a lado**
- **Solo sección de campos**
- **Solo sección de áreas (2 x 2)**
- **Solo sección de áreas (1 x 4)**

### Mantener los documentos abiertos al cambiar de modelo

**Mantener los Pivot Grids abiertos cuando se abra un modelo diferente** (habilitado): Mantener los documentos de Pivot Grid abiertos cuando se abra un modelo diferente y conectarlos al nuevo modelo. Se mantiene el diseño de los campos y se eliminan los campos que el nuevo modelo no tiene. Cuando está desactivada, las Pivot Grids se cierran junto con el modelo anterior. Consulte @pivot-grid.

## Exploración de datos > Consulta DAX

<!-- VOLVER A HACER CAPTURA DE PANTALLA (3.27.1): pref-dax-query.png. Muestre la sección «Mantener las consultas DAX abiertas cuando se abra un modelo diferente». -->
![Preferencias de consultas DAX](~/content/assets/images/pref-dax-query.png)

### Básico

**Ejecutar automáticamente consultas DAX de forma predeterminada** (habilitado): Las nuevas consultas DAX se abren con la **Ejecución automática** habilitada, por lo que la consulta se vuelve a ejecutar cada vez que se realizan cambios en el modelo semántico implementado. Desactívela si prefiere ejecutar cada consulta usted mismo.

**Mantener la ordenación y el filtrado existentes en la cuadrícula de resultados** (WhenQueryUnchanged): Controle si desea conservar los filtros y la ordenación de la cuadrícula al volver a ejecutar las consultas:
- **Nunca**: la ordenación y el filtrado siempre se restablecen cuando se ejecuta una consulta.
- **WhenQueryUnchanged**: la ordenación y el filtrado solo se restablecen cuando se modifica la consulta.
- **Siempre**: la ordenación y el filtrado nunca se restablecen si las columnas siguen existiendo.

### Configuración de consulta

**Selección inteligente** (habilitada): Cuando ejecuta parte de una consulta, Tabular Editor convierte esa selección en una consulta DAX válida en su nombre, envolviendo una expresión escalar entre llaves y añadiendo la sección `DEFINE` o la palabra clave `EVALUATE` cuando no forman parte de la selección. En un documento con varias consultas `DEFINE ... EVALUATE`, la sección `DEFINE` añadida es la que pertenece a la consulta seleccionada. Una referencia de columna seleccionada, incluida una en una cláusula `ORDER BY`, devuelve los valores distintos de la columna.

**Límite de filas** (1000): Encierra cada sentencia `EVALUATE` en una llamada `TOPN`, para evitar que una consulta accidental sobre una tabla grande se ejecute durante mucho tiempo o agote la memoria. Establézcalo en `0` para eliminar el límite por completo.

### Generación de código

**Usar comentarios como separadores** (activado): Inserta comentarios en las definiciones de objetos generadas, por ejemplo, en el bloque `DEFINE` producido por **Definir objeto en consulta**, para que sean más fáciles de leer.

### Mantener los documentos abiertos al cambiar de modelo

**Mantener abiertas las consultas DAX cuando se abra un modelo diferente** (habilitado): Mantener abiertos los documentos de consultas DAX cuando se abra un modelo diferente. Se conserva el texto de la consulta, se borran los resultados anteriores y la consulta se ejecuta contra el modelo recién abierto. Cuando está desactivada, los documentos de consultas DAX se cierran junto con el modelo anterior. Consulte @dax-query.

## Exploración de datos > Vista previa de tabla

![Preferencias de vista previa de tabla](~/content/assets/images/pref-table-preview.png)

### Básico

**Actualizar automáticamente vistas previas de tabla de forma predeterminada** (habilitado): Las nuevas vistas previas de tabla se abren con la **Actualización automática** habilitada, por lo que la vista previa se actualiza cada vez que se realizan cambios en el modelo semántico implementado. Esto es útil al depurar: actualice una expresión en una ventana mientras una vista previa de la misma tabla está abierta en otra.

**Ordenar las columnas de la vista previa de la tabla alfabéticamente** (desactivado): Cuando está marcado, las columnas de la vista previa de la tabla se ordenan alfabéticamente por nombre, coincidiendo con el orden en que @tom-explorer-view enumera las columnas de una tabla. Cuando no está marcada (valor predeterminado), las columnas aparecen en el orden en que las devuelve el motor, que es aproximadamente el orden interno de las columnas y puede parecer arbitrario.

**Número máximo de valores en el menú desplegable de filtros** (5000): Número máximo de valores distintos que aparecen en el menú desplegable de filtros de una columna. En una columna con más valores distintos que este número, los valores que superen el límite no se mostrarán y no se podrán marcar directamente. Si se aumenta, se mostrarán más valores, pero a costa de una consulta más pesada cada vez que se abra el menú desplegable. Acepta valores de 100 a 1 000 000.

**Máx. de filas para ordenar sin una jerarquía de atributos** (100 000): Límite superior del número de filas que Tabular Editor ordena por una columna que no tiene una jerarquía de atributos por la que ordenar.

### DirectQuery

**Límite de filas** (100): Número máximo de filas que se van a recuperar para una vista previa de tabla en el modo DirectQuery. Auméntelo si necesita ver más datos, teniendo en cuenta que cada fila se extrae del origen subyacente.

### Comportamiento

**Seguir la columna seleccionada en el Explorador TOM** (habilitado): Cuando selecciona una columna en la @tom-explorer-view, la vista previa de la tabla abierta desplaza esa columna hasta que quede visible y la resalta, lo cual es la forma más rápida de encontrar una columna de una tabla muy ancha. El mismo ajuste se puede activar y desactivar para una sola vista previa con **Seguir columna seleccionada** en la barra de herramientas de la vista previa de tabla.

## Editores de texto > Editor de DAX > General

![Editor DAX - General](~/content/assets/images/dax-editor-general.png)

El editor DAX de Tabular Editor 3 es altamente configurable. Esta página ofrece ajustes para la configuración general del editor DAX:

**Números de línea** (habilitado): Muestra los números de línea en el margen izquierdo del editor.

**Plegado de código** (habilitado): Habilita las regiones contraíbles en el código DAX para mejorar la legibilidad. ¡Asegúrate de probar esta función!

**Espacios en blanco visibles** (desactivado): Muestra puntos para los espacios y flechas para las tabulaciones. Esto puede ser útil para diagnosticar problemas de sangría.

**Guías de sangría** (habilitadas): Muestra líneas verticales para indicar los niveles de sangría.

**Usar tabulaciones** (desactivado): cuando está marcado, se inserta un carácter de tabulación (`\t`) cada vez que se pulsa la tecla TAB. De lo contrario, se inserta un número de espacios correspondiente al ajuste **Ancho de sangría**.

**Estilo de comentario** (barras diagonales): DAX admite comentarios de línea que utilizan barras diagonales (`//`) o guiones (`--`). Este ajuste determina qué estilo de comentario se utiliza cuando Tabular Editor 3 genera código DAX.

**Documentación de funciones DAX**: Use esta configuración para especificar qué URL abrir en el navegador web predeterminado cada vez que pulse F12 mientras el cursor esté situado sobre una función DAX. Las opciones incluyen https://dax.guide (recomendada) y la documentación oficial de Microsoft.

### Configuración de DAX

**Configuración regional**: Especifique la configuración regional para las funciones y el formato de DAX.

**Configuración de la versión de Analysis Services**: Estos ajustes solo son relevantes cuando Tabular Editor 3 no puede determinar la versión de Analysis Services utilizada, como ocurre cuando se carga directamente un archivo Model.bim. En este caso, Tabular Editor intenta adivinar en qué versión se implementará el modelo, en función del nivel de compatibilidad. Si Tabular Editor informa de errores semánticos o de sintaxis incorrectos, configúrelos según la versión de Analysis Services en la que vaya a implementar.

## Editores de texto > Editor de DAX > Formato automático

![Ajustes de formato automático](~/content/assets/images/auto-formatting-settings.png)

El editor de DAX es **muy** potente y le ayuda a crear un código DAX atractivo y legible mientras escribe.

**Formatear código automáticamente mientras escribe** (habilitado): Aplica reglas de formato cuando se pulsan determinadas teclas. Por ejemplo, cuando se cierra un paréntesis, todo lo que hay dentro de los paréntesis se formatea de acuerdo con los demás ajustes de esta página.

**Formatear llamadas a funciones automáticamente** (habilitado): Formatea las llamadas a funciones (espaciado entre argumentos y paréntesis) cuando se cierra un paréntesis.

**Sangría automática** (habilitada): Esta opción aplica sangría automáticamente a los argumentos de la función cuando se inserta un salto de línea dentro de una llamada a función.

**Llave automática** (habilitada): Esta opción inserta automáticamente la llave o comilla de cierre cada vez que se introduce una llave o comilla de apertura.

**Envolver selección** (habilitado): Cuando está habilitada, esta opción envuelve automáticamente la selección actual con la llave de cierre cuando se introduce una llave de apertura.

### Reglas de formato

Estos ajustes controlan cómo se formatean los espacios en blanco del código DAX, tanto cuando se produce el formateo automático como cuando el código se formatea manualmente.

**Espacio después de funciones** (desactivado)

# [Habilitado](#tab/space-after-function-on)

```DAX
SUM ( 'Sales'[Amount] )
```

# [Desactivado](#tab/space-after-function-off)

```DAX
SUM( 'Sales'[Amount] )
```

***

**Nueva línea después de funciones** (deshabilitado): Se aplica solo cuando una llamada a función debe dividirse en varias líneas.

# [Habilitado](#tab/newline-after-function-on)

```DAX
SUM
(
    'Sales'[Amount]
)
```

# [Desactivado](#tab/newline-after-function-off)

```DAX
SUM(
    'Sales'[Amount]
)
```

***

**Rellenar paréntesis** (activado)

# [Habilitado](#tab/pad-parentheses-on)

```DAX
SUM( Sales[Amount] )
```

# [Deshabilitado](#tab/pad-parentheses-off)

```DAX
SUM(Sales[Amount])
```

***

**Límite de línea de formato largo** (120): El número máximo de caracteres que se pueden mantener en una sola línea antes de que una expresión se divida en varias líneas, al usar la opción **Formatear DAX (líneas largas)**.

**Límite de línea de formato corto** (60): El número máximo de caracteres que se pueden mantener en una sola línea antes de que una expresión se divida en varias líneas, al usar la opción **Formatear DAX (líneas cortas)**.

### Mayúsculas y comillas

Además de formatear los espacios en blanco del código DAX, Tabular Editor 3 también puede corregir las referencias a objetos y las mayúsculas y minúsculas de las funciones y palabras clave.

**Corregir calificadores de medida/columna** (habilitado): Cuando está marcada esta opción, los prefijos de tabla se eliminan automáticamente de las referencias a medidas y se insertan automáticamente en las referencias a columnas.

**Mayúsculas preferidas para palabras clave** (MAYÚSCULAS): Este ajuste le permite cambiar las mayúsculas utilizadas para las palabras clave, como `ORDER BY`, `VAR`, `EVALUATE`, etc. También rige los valores fijos de las palabras clave que ofrece el autocompletado para las funciones que los utilizan: `ASC` y `DESC`, `KEEP`, `FIRST`, `LAST` y `DEFAULT`, las direcciones de `CROSSFILTER` y `EXPLICIT` e `INFERRED` de `LOOKUP`. Elija **Poner en mayúscula solo la primera letra** para que se le ofrezca `Explicit` en lugar de `EXPLICIT`.

**Mayúsculas preferidas para funciones** (MAYÚSCULAS): Este ajuste le permite cambiar las mayúsculas utilizadas para las funciones, como `CALCULATE(...)`, `SUM(...)`, etc.

**Corregir mayúsculas de palabras clave/funciones** (habilitado): Cuando está marcada esta opción, las mayúsculas de las palabras clave y las funciones se corrigen automáticamente cada vez que el código se formatea automáticamente o manualmente.

**Corregir mayúsculas de referencias de objetos** (habilitado): DAX es un lenguaje que no distingue entre mayúsculas y minúsculas. Cuando esto está habilitado, las referencias a tablas, columnas y medidas se corrigen automáticamente de modo que las mayúsculas coincidan con el nombre físico de los objetos a los que se hace referencia.

**Entrecomillar siempre tablas** (deshabilitado): Hacer referencia a ciertos nombres de tabla no requiere entrecomillarlos con comillas simples en DAX. Sin embargo, si prefiere que las referencias a tablas vayan siempre entre comillas, puede marcar esta opción.

**Prefijar siempre las columnas de extensión** (deshabilitado): Las columnas de extensión se pueden definir sin un nombre de tabla. Cuando está marcado, el Editor de DAX añade el prefijo de la tabla a una columna de extensión.

## Editores de texto > Editor de DAX > Code Assist

![Preferencias de Code Assist del editor de DAX](~/content/assets/images/pref-dax-code-assist.png)

En esta página, puede configurar las dos funciones más importantes de Code Assist, a saber, las descripciones emergentes (también llamadas «información de parámetros») y el autocompletado.

**Activador de autocompletar**: Controle cuándo aparece la lista de autocompletar. Las opciones incluyen la activación automática después de escribir un cierto número de caracteres o la activación manual con CTRL+Espacio.

**Activador de información sobre llamadas**: Controle cuándo aparece la información sobre los parámetros. Las opciones incluyen la activación automática al abrir un paréntesis de función o la activación manual.

**Búsqueda incremental** (habilitada): habilita la búsqueda difusa/incremental en el autocompletado. Esto le permite encontrar elementos escribiendo partes de su nombre, no solo el principio.

**Sugerir nombres de tablas** (habilitado): Incluir nombres de tablas en las sugerencias de autocompletado.

**Entrecomillar siempre los nombres de tabla** (deshabilitado): Entrecomilla automáticamente los nombres de tabla en las sugerencias, incluso cuando no sea necesario.

**Mostrar solo la primera letra** (desactivado): Mostrar solo los elementos que comienzan con la letra escrita. Deshabilite esta opción para usar la búsqueda incremental en su lugar.

## Editores de texto > Editor de DAX > Acciones de código

![Preferencias de acciones de código del editor de DAX](~/content/assets/images/pref-dax-code-actions.png)

Configurar sugerencias automáticas de mejora del código:

**Prefijos de variables**: Defina los prefijos aceptables para los nombres de variables (p. ej., `_`, `__`, `$`, `var_`, `var`, `v_`, `v`, `VAR_`). Las acciones de código sugieren añadir estos prefijos a los nombres de variables que no siguen la convención.

**Prefijos de columna**: Defina los prefijos aceptables para los nombres de columnas temporales (p. ej., `@`, `$`, `_`, `x`, `x_`). Las acciones de código sugieren añadir estos prefijos a los nombres de columnas temporales que no siguen la convención.

## Editor SQL / Editor M / Editor C#

<!-- SE NECESITA IMAGEN: pref-code-editors.png
     Una de las páginas de preferencias del Editor SQL, el Editor M y el Editor C#. Los tres comparten un
     diseño, por lo que una sola captura de pantalla cubre la sección.
     Texto alternativo: «La página de preferencias del editor de código, compartida por los editores de SQL, M y C#» -->

Hay opciones de configuración similares disponibles para los editores de scripts SQL, M (Power Query) y C#, incluidas las siguientes:
- Resaltado de sintaxis y esquemas de color
- Opciones de formato automático
- Funciones de Code Assist y autocompletado
- Estilos de comentarios y preferencias de sangrado

Cada editor se puede personalizar de forma independiente para que coincida con tu estilo de programación preferido.

## Formateador DAX

<!-- SE NECESITA IMAGEN: pref-dax-formatter.png
     La página de preferencias del formateador DAX con su configuración predeterminada.
     Texto alternativo: «La página de preferencias de DAX Formatter» -->

**Consentimiento para el formateador de DAX** (desactivado): Acepte enviar código DAX al servicio externo de formateo de DAX (www.daxformatter.com). Cuando está habilitado, puede usar este servicio para formatear código DAX de acuerdo con los estándares de la comunidad.

**Tiempo de espera de las solicitudes del formateador de DAX** (5000): Tiempo de espera en milisegundos para las solicitudes del formateador de DAX. Aumente este valor si suele recibir errores de tiempo de espera al usar el formateador de DAX.

## Integración del Optimizador de DAX

<!-- IMAGEN NECESARIA: pref-dax-optimizer.png
     La página de preferencias de la integración con el Optimizador de DAX con su configuración predeterminada.
     Texto alternativo: «Página de preferencias de la integración con el Optimizador de DAX» -->

Configure la integración con DAX Optimizer (solo en la Edición Enterprise):

**Conectar automáticamente** (nulo/solicitar): Conectar automáticamente al Optimizador de DAX cuando esté disponible. Cuando no está configurado, aparece un mensaje la primera vez.

**Ofuscar archivos VPAX** (habilitado): anonimiza los metadatos del modelo cuando se envían al Optimizador de DAX. Esto protege la información confidencial, como los nombres de las tablas y las columnas, al tiempo que permite realizar análisis.

**Directorio del diccionario de ofuscación** (`%LocalAppData%\TabularEditor3\DaxOptimizer`): especifique dónde se almacenan los diccionarios de ofuscación. El diccionario mantiene una ofuscación coherente en múltiples análisis.

## Formatos de archivo > Analizador VertiPaq

![Preferencias del Analizador VertiPaq](~/content/assets/images/pref-vertipaq-analyzer.png)

**Incluir metadatos del TOM** (habilitado): Incluir los metadatos del Tabular Object Model en las estadísticas de VertiPaq Analyzer. Esto proporciona información más completa sobre la estructura de tu modelo.

**Leer estadísticas de datos** (habilitado): Lee las estadísticas analizando los datos reales (más preciso, pero más lento). Cuando está desactivada, solo se utilizan los metadatos. Si la lectura de estadísticas a partir de los datos falla, por ejemplo, cuando una columna de alta cardinalidad supera el límite de memoria por consulta de una capacidad de Power BI, **Recopilar estadísticas** recopila las estadísticas a partir de los metadatos y aparece una advertencia de **Estadísticas recopiladas sin leer datos**.

**Modo de extracción Direct Lake** (ResidentOnly): Cómo extraer estadísticas de modelos Direct Lake:
- **ResidentOnly**: Solo analizar los datos cargados actualmente en la memoria
- **Todos**: Incluir datos no residentes (más lento, puede desencadenar la carga de datos)

**Leer estadísticas de las vistas de administración dinámica** (desactivado): Utilice las DMV para recopilar estadísticas (más rápido, pero menos preciso). Esta es una alternativa a la lectura de datos.

**Filas de muestra de relaciones** (3): Número de filas que se van a muestrear al analizar las relaciones. Los valores más altos proporcionan mayor precisión, pero tardan más.

**Tamaño de lote de columnas** (50): Número de columnas que se van a analizar en cada lote. Ajusta este valor en función del tamaño de tu modelo y de tus requisitos de rendimiento.

## Integración con Power BI

![Preferencias de integración de Power BI](~/content/assets/images/pref-power-bi.png)

**URL base del punto de conexión de Power BI** (`https://api.powerbi.com`): La URL base para las llamadas a la API de Power BI. Cambia esto si trabajas con una nube soberana o un entorno personalizado.

**URL base del punto de conexión de Fabric** (`https://api.fabric.microsoft.com`): La URL base para las llamadas a la API de Microsoft Fabric. Cambia esto si trabajas con una nube soberana o un entorno personalizado.

**Usar el navegador integrado para la autenticación** (habilitado): Usa el navegador integrado para la autenticación OAuth en lugar del navegador del sistema. Esto proporciona una experiencia más integrada.

## Configuración de proxy

![Preferencias de configuración de proxy](~/content/assets/images/pref-proxy-settings.png)

**Tipo de proxy** (Ninguno): Elija entre:
- **Ninguno**: Sin configuración de proxy
- **Sistema**: Utilizar la configuración de proxy del sistema
- **Personalizado**: Especifique una configuración de proxy personalizada.

**Dirección de proxy**: La dirección del servidor proxy (p. ej., `http://proxy.company.com:8080`).

**Usuario del proxy**: Nombre de usuario para la autenticación del proxy, si es necesario.

**Contraseña del proxy**: Contraseña para la autenticación del proxy (almacenada cifrada).

**Usar credenciales predeterminadas** (habilitado): Usar las credenciales actuales de Windows para la autenticación del proxy. Esto implementa [el mismo comportamiento que Power BI Desktop](https://docs.microsoft.com/power-bi/connect-data/desktop-troubleshooting-sign-in#using-default-system-credentials-for-web-proxy).

**Omitir el proxy en local** (habilitado): Omitir el proxy para las direcciones locales. Se recomienda por motivos de rendimiento.

**Lista de omisión del proxy**: Lista de direcciones que deben omitir el proxy (p. ej., `localhost;*.company.local`).

## Pasos siguientes

Para obtener una guía fácil de usar sobre las preferencias que se ajustan con más frecuencia, consulta la guía de introducción [Personalización de Tabular Editor 3](xref:personalizing-te3).
