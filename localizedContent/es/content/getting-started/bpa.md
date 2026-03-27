---
uid: bpa
title: Mejora la calidad del código con el Best Practice Analyzer
author: Daniel Otykier
updated: 2021-11-02
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Mejora la calidad del código con el Best Practice Analyzer

A estas alturas, probablemente ya sepas que el Tabular Object Model (TOM) es una estructura de datos relativamente compleja, con muchos tipos distintos de objetos y propiedades. No siempre está claro cuáles son los mejores valores para asignar a estas propiedades, y muchas veces depende de casos de uso concretos o del diseño del modelo. El **Best Practice Analyzer** de Tabular Editor analiza continuamente el TOM en busca de infracciones de las reglas de prácticas recomendadas que puedes definir. Esto te ayuda a comprobar que las propiedades de los objetos estén siempre configuradas con sus valores ideales.

Aspectos que puedes comprobar con el Best Practice Analyzer:

- **Expresiones DAX:** Crea reglas que te avisen cuando se usen determinadas funciones o construcciones de DAX.
- **Formato:** Crea reglas que te recuerden especificar cadenas de formato, descripciones, etc.
- **Convenciones de nomenclatura:** Crea reglas que comprueben si determinados tipos de objetos (p. ej., columnas clave, columnas ocultas, etc.) siguen determinados patrones de nomenclatura.
- **Rendimiento:** Crea reglas que comprueben varios aspectos relacionados con el rendimiento de tu modelo; por ejemplo, para fomentar la reducción del número de columnas calculadas.

El Best Practice Analyzer tiene acceso a todos los metadatos del modelo y también puede acceder a las estadísticas del Analizador VertiPaq para escenarios más avanzados.

> [!NOTE]
> Tabular Editor 3 incluye un conjunto completo de [reglas integradas de Best Practice Analyzer](xref:built-in-bpa-rules) que están habilitadas de forma predeterminada.

# Administración de reglas de buenas prácticas

Para agregar, quitar o modificar las reglas que se aplican a tu modelo, usa la opción de menú "Tools > Manage BPA Rules...".

![Administrador de Bpa](~/content/assets/images/bpa-manager.png)

Esta interfaz de usuario contiene dos listas: la lista superior representa las **colecciones** de reglas que están cargadas actualmente. Al seleccionar una colección en esta lista se mostrarán todas las reglas definidas dentro de esa colección en la lista inferior. Cuando se carga un modelo, verás las siguientes tres colecciones de reglas:

- **Reglas dentro del modelo actual**: Como indica el nombre, esta es la colección de reglas que se han definido dentro del modelo actual. Las definiciones de reglas se almacenan como una anotación en el objeto Model.
- **Reglas para el usuario local**: Son reglas que se almacenan en el archivo `%LocalAppData%\TabularEditor3\BPARules.json`. Estas reglas se aplicarán a todos los modelos que se carguen en Tabular Editor para el usuario de Windows con el que hayas iniciado sesión.
- **Reglas en la máquina local**: Estas reglas se almacenan en el archivo `%ProgramData%\TabularEditor\BPARules.json`. Estas reglas se aplicarán a todos los modelos que se carguen en Tabular Editor en la máquina actual.

Si la misma regla (por ID) se encuentra en más de una colección, el orden de precedencia va de arriba abajo; es decir, una regla definida dentro del modelo tiene prioridad sobre otra, con el mismo ID, definida en la máquina local. Esto te permite sobrescribir reglas existentes, por ejemplo, para tener en cuenta convenciones específicas del modelo.

En la parte superior de la lista, verás una colección especial llamada **(Reglas efectivas)**. Al seleccionar esta colección, verás la lista de reglas que realmente se aplican al modelo cargado actualmente, respetando la precedencia de las reglas con el mismo ID, como se mencionó anteriormente. La lista inferior indicará a qué colección pertenece una regla. Además, verás que el nombre de una regla aparece tachado si existe una regla con un ID similar en una colección con mayor prioridad:

![Rule Overrides](~/content/assets/images/rule-overrides.png)

## Agregar colecciones adicionales

Las colecciones de reglas se pueden agregar a un modelo específico. Si tienes un archivo de reglas ubicado en un recurso compartido de red, puedes incluir ese archivo como una colección de reglas en el modelo actual. Si tienes acceso de escritura a la ubicación del archivo, también podrás agregar/modificar/eliminar reglas del archivo. Las colecciones de reglas que se agregan de esta forma tienen prioridad sobre las reglas que se definen en el modelo. Si agregas varias colecciones de este tipo, puedes subirlas y bajarlas para controlar su prioridad relativa.

Haz clic en el botón "Agregar..." para agregar una nueva colección de reglas al modelo. Esto ofrece las siguientes opciones:

![Agregar colección de reglas de prácticas recomendadas](~/content/assets/images/add-rule-file.png)

- **Crear nuevo archivo de reglas**: Esto creará un archivo .json nuevo y vacío en la ubicación especificada, al que luego podrás agregar reglas. Al seleccionar el archivo, ten en cuenta que hay una opción para usar rutas de archivo relativas. Esto es útil cuando quieres almacenar el archivo de reglas en el mismo repositorio de código que el modelo actual. Sin embargo, ten en cuenta que una referencia relativa al archivo de reglas solo funciona cuando el modelo se ha cargado desde el disco (ya que no hay un directorio de trabajo cuando se carga un modelo desde una instancia de Analysis Services).
- **Incluir archivo de reglas local**: Usa esta opción si ya tienes un archivo .json que contiene reglas y quieres incluirlo en tu modelo. De nuevo, tienes la opción de usar rutas de archivo relativas, lo que puede ser beneficioso si el archivo está ubicado cerca de los metadatos del modelo. Si el archivo está ubicado en un recurso compartido de red (o, en general, en una unidad distinta de aquella donde residen los metadatos del modelo cargado actualmente), solo puedes incluirlo mediante una ruta absoluta.
- **Incluir archivo de reglas desde URL**: Esta opción te permite especificar una URL HTTP/HTTPS que debe devolver un conjunto de reglas válido (en formato json). Esto es útil si quieres incluir reglas desde una fuente en línea; por ejemplo, las [reglas BPA estándar](https://raw.githubusercontent.com/TabularEditor/BestPracticeRules/master/BPARules-standard.json) del [sitio de GitHub de BestPracticeRules](https://github.com/TabularEditor/BestPracticeRules). Ten en cuenta que las colecciones de reglas agregadas desde fuentes en línea serán de solo lectura.

## Modificar reglas en una colección

La parte inferior de la pantalla te permitirá agregar, editar, clonar y eliminar reglas dentro de la colección seleccionada, siempre que tengas acceso de escritura a la ubicación donde se almacena la colección. Además, el botón "Mover a..." te permite mover o copiar la regla seleccionada a otra colección, lo que facilita administrar varias colecciones de reglas.

## Agregar reglas

Para agregar una nueva regla a una colección, haz clic en el botón **Nueva regla...**. Esto abre el editor de reglas de prácticas recomendadas (consulta la captura de pantalla a continuación).

![Bpa Rule Editor](~/content/assets/images/bpa-rule-editor.png)

Al crear una nueva regla, debes especificar los siguientes detalles:

- **Nombre**: El nombre de la regla, que se mostrará a los usuarios de Tabular Editor
- **ID**: un ID interno de la regla. Tiene que ser único dentro de una colección de reglas. Si varias reglas tienen el mismo ID en distintas colecciones, solo se aplica la regla de la colección con mayor precedencia.
- **Gravedad**: La gravedad no se usa en la interfaz de usuario de Tabular Editor, pero al ejecutar un análisis de prácticas recomendadas mediante la [interfaz de línea de comandos de Tabular Editor](xref:command-line-options), el número determina lo "grave" que es una infracción de la regla.
  - 1 = Solo informativo
  - 2 = Advertencia
  - 3 (o superior) = Error
- **Categoría**: Se usa para agrupar reglas de forma lógica y así facilitar su administración.
- **Descripción** (opcional): Se puede usar para describir para qué está pensada la regla. Se mostrará en la vista de Best Practice Analyzer como información sobre herramientas. Puedes usar los siguientes valores de marcador de posición dentro del campo de descripción para proporcionar mensajes más contextuales:
  - `%object%` devuelve una referencia DAX totalmente calificada (si corresponde) al objeto actual
  - `%objectname%` devuelve solo el nombre del objeto actual
  - `%objecttype%` devuelve el tipo del objeto actual
- **Se aplica a**: Selecciona el tipo de objeto(s) al que debe aplicarse la regla.
- **Expresión**: Escribe una expresión de búsqueda de [Dynamic LINQ](https://dynamic-linq.net/expression-language) que debe evaluarse como `true` para aquellos objetos (entre los tipos de objeto seleccionados en la lista desplegable **Se aplica a**) que infrinjan la regla. La expresión de Dynamic LINQ puede acceder a las propiedades de TOM disponibles en los tipos de objeto seleccionados, así como a una amplia gama de métodos y propiedades estándar de .NET.
- **Nivel de compatibilidad mínimo**: Algunas propiedades de TOM no están disponibles en todos los niveles de compatibilidad. Si estás creando reglas genéricas, usa esta lista desplegable para especificar el nivel de compatibilidad mínimo de los modelos a los que debe aplicarse la regla.

Cuando se guarda una regla en una colección de reglas en disco, todas las propiedades anteriores se almacenan en formato JSON. También puedes agregar/editar/eliminar reglas editando el archivo JSON, lo que además te permite especificar la propiedad `FixExpression` en una regla. Es una cadena que se usa para generar un [C# Script](xref:cs-scripts-and-macros) que se aplicará al modelo para corregir el incumplimiento de la regla.

# Uso de la vista de Best Practice Analyzer

Tabular Editor muestra los incumplimientos de reglas de prácticas recomendadas en la **vista de Best Practice Analyzer**. También puedes ver el número de incumplimientos de reglas en la barra de estado en la parte inferior de la ventana principal. Para poner el foco en la vista, usa la opción de menú **View > Best Practice Analyzer** o haz clic en el botón "# BP issues" de la barra de estado.

![Vista de Best Practice Analyzer](~/content/assets/images/best-practice-analyzer-view.png)

La **vista de Best Practice Analyzer** muestra una lista de todas las reglas que tienen objetos que las infringen. Debajo de cada regla hay una lista de los objetos que infringen la regla. Puedes hacer doble clic en un objeto de la lista para navegar a ese objeto en el **Explorador TOM**.

> [!TIP]
> **Usuarios de la Edición Enterprise**: Las reglas BPA integradas se muestran junto con cualquier regla personalizada que definas. Estas reglas están habilitadas de forma predeterminada y ofrecen una guía completa de mejores prácticas. Puedes administrar las reglas integradas en **Tools > Manage BPA Rules...**, donde aparecen en la colección **(Built-in rules)**. Para más información, consulta [reglas BPA integradas](xref:built-in-bpa-rules).

![Opciones del elemento](~/content/assets/images/bpa-options.png)

Al hacer clic con el botón derecho en un objeto, se muestran varias opciones, tal como se indica arriba. Son las siguientes:

- **Ir al objeto**: Esto equivale a hacer doble clic en un objeto para desplazarte hasta ese objeto en el **Explorador TOM**.
- **Ignorar objeto**: Esto agrega una anotación al objeto e indica al Best Practice Analyzer que ignore esta regla concreta para ese objeto. Las reglas ignoradas se especifican mediante su ID.
- **Generar script de corrección**: Esta opción solo está disponible si una regla tiene especificada la propiedad `FixExpression`. Al elegir esta opción, Tabular Editor crea un nuevo script de C# basado en la `FixExpression` de las reglas seleccionadas.
- **Aplicar corrección**: Esta opción solo está disponible si una regla tiene especificada la propiedad `FixExpression`. Al elegir esta opción, Tabular Editor ejecuta la `FixExpression` de las reglas seleccionadas para corregir automáticamente el incumplimiento de la regla.

> [!NOTE]
> Puedes seleccionar varios objetos en la vista del Best Practice Analyzer manteniendo pulsadas las teclas Shift o Ctrl.

Las opciones indicadas arriba también están disponibles como botones de la barra de herramientas en la parte superior de la **vista del Best Practice Analyzer**. Además, hay botones para expandir o contraer todos los elementos, mostrar reglas u objetos ignorados y realizar una actualización manual (necesaria cuando los análisis en segundo plano están deshabilitados; ver más abajo).

# Desactivar el Best Practice Analyzer

En algunos casos, quizá quieras desactivar el análisis en segundo plano del Best Practice Analyzer. Por ejemplo, cuando tienes reglas que tardan relativamente mucho en evaluarse o cuando trabajas con modelos muy grandes.

Puedes desactivar el análisis en segundo plano en **Tools > Preferencias > Best Practice Analyzer** desmarcando la opción **Scan for Best Practice violations in the background**.

Ten en cuenta que, incluso cuando los análisis en segundo plano estén deshabilitados, puedes seguir ejecutando un análisis manualmente con el botón **Refresh** de la **vista del Best Practice Analyzer**, como se mencionó arriba.

# Pasos siguientes

- @cs-scripts-and-macros
- @personalizing-te3