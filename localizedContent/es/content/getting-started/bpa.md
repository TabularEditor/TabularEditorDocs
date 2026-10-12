---
uid: bpa
title: Mejora la calidad del código con el Best Practice Analyzer
author: Daniel Otykier
updated: 2026-10-12
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

El **Best Practice Analyzer** (BPA) analiza en segundo plano el Tabular Object Model (TOM) del modelo cargado para detectar objetos que infringen las reglas de buenas prácticas que definas. TOM tiene muchos [tipos de objeto y propiedades](xref:TabularEditor.TOMWrapper), y el valor adecuado para una propiedad suele depender del diseño del modelo. Las reglas de BPA comprueban que cada propiedad tenga el valor que exigen tus convenciones.

Usa las reglas del Best Practice Analyzer para comprobar:

- **Expresiones DAX**: avisan cuando se usan determinadas funciones o construcciones de DAX.
- **Formato**: requieren cadenas de formato, descripciones y propiedades similares.
- **Convenciones de nomenclatura**: comprueban que los tipos de objetos, como las columnas clave o las columnas ocultas, sigan patrones de nombres.
- **Rendimiento**: comprueban aspectos del modelo relacionados con el rendimiento, por ejemplo el número de columnas calculadas.

Las reglas tienen acceso a todos los metadatos del modelo y a las estadísticas del Analizador VertiPaq.

> [!NOTE]
> Tabular Editor 3 incluye [reglas integradas de Best Practice Analyzer](xref:built-in-bpa-rules), habilitadas de forma predeterminada. Aparecen en la **vista de Best Practice Analyzer**, junto con tus reglas personalizadas, y en la colección **(Reglas integradas)**, en **Herramientas > Administrar reglas de BPA...**.

## Administración de reglas de buenas prácticas

Abre **Herramientas > Administrar reglas de BPA...** para agregar, quitar o modificar las reglas que se aplican a tu modelo.

![Cuadro de diálogo Administrar reglas de prácticas recomendadas con la lista de colecciones de reglas en la parte superior y las reglas de la colección seleccionada en la parte inferior](~/content/assets/images/bpa-manager.png)

La lista superior muestra las **colecciones** de reglas cargadas, y la lista inferior muestra las reglas de la colección que selecciones. Cuando se carga un modelo, se muestran estas colecciones:

- **Reglas del modelo actual**: reglas definidas en el modelo actual, almacenadas como una anotación en el objeto Model.
- **Reglas del usuario local**: reglas almacenadas en `%LocalAppData%\TabularEditor3\BPARules.json`. Se aplican a todos los modelos que el usuario actual de Windows cargue en Tabular Editor.
- **Reglas en la máquina local**: reglas almacenadas en `%ProgramData%\TabularEditor\BPARules.json`. Se aplican a todos los modelos que se carguen en Tabular Editor en el equipo.

Si una regla con el mismo ID existe en más de una colección, la colección situada más arriba en la lista tiene precedencia. Una regla definida en el modelo prevalece sobre una regla con el mismo ID en la máquina local, por lo que puedes ajustar una regla compartida a las convenciones específicas del modelo.

La colección **(Reglas efectivas)** situada en la parte superior de la lista muestra las reglas que se aplican al modelo cargado una vez resuelta la precedencia. La lista inferior muestra a qué colección pertenece cada regla. El nombre de una regla aparece tachado si existe una regla con el mismo ID en una colección con mayor precedencia:

![Lista de reglas efectivas con una regla sobrescrita que aparece tachada](~/content/assets/images/rule-overrides.png)

### Agregar colecciones adicionales

Puedes agregar un archivo de reglas, por ejemplo uno en un recurso compartido de red, al modelo actual como una colección de reglas. Si tienes acceso de escritura al archivo, puedes agregar, modificar y quitar sus reglas. Las colecciones agregadas de esta forma tienen precedencia sobre las reglas definidas en el modelo. Si agregas varias, muévelas hacia arriba y hacia abajo para establecer su precedencia.

Haz clic en **Agregar...** para agregar una colección de reglas al modelo:

![Agregar colección de reglas de prácticas recomendadas](~/content/assets/images/add-rule-file.png)

- **Crear nuevo archivo de reglas**: crea un archivo .json vacío en la ubicación que especifiques. El cuadro de diálogo de selección de archivo incluye una opción de ruta relativa, que te permite guardar el archivo de reglas en el mismo repositorio que el modelo. Una referencia relativa solo funciona cuando el modelo se carga desde el disco. Un modelo cargado desde una instancia de Analysis Services no tiene directorio de trabajo.
- **Incluir archivo de reglas local**: incluye un archivo de reglas .json existente. Puedes usar una ruta relativa si el archivo está en la misma unidad que los metadatos del modelo. Un archivo en un recurso compartido de red o en otra unidad requiere una ruta absoluta.
- **Incluir archivo de reglas desde una URL**: incluye las reglas que devuelve una URL HTTP o HTTPS; por ejemplo, las [reglas BPA estándar](https://raw.githubusercontent.com/TabularEditor/BestPracticeRules/master/BPARules-standard.json) del [repositorio de GitHub de BestPracticeRules](https://github.com/TabularEditor/BestPracticeRules). Las colecciones agregadas desde una URL son de solo lectura.

### Modificar reglas en una colección

En la parte inferior del cuadro de diálogo puedes agregar, editar, clonar y eliminar reglas de la colección seleccionada si tienes acceso de escritura a su ubicación. **Mover a...** mueve o copia la regla seleccionada a otra colección.

### Agregar reglas

Haz clic en **Nueva regla...** para abrir el editor de reglas de mejores prácticas:

![Editor de reglas de mejores prácticas con los campos de nombre, ID, gravedad, categoría, descripción, se aplica a y expresión](~/content/assets/images/bpa-rule-editor.png)

Una regla tiene estas propiedades:

- **Nombre**: el nombre de la regla que se muestra en Tabular Editor.
- **ID**: un ID interno, único dentro de una colección de reglas. Si las reglas de distintas colecciones comparten un ID, solo se aplica la regla de la colección con mayor precedencia.
- **Gravedad**: no se usa en la interfaz de usuario de Tabular Editor. Al ejecutar un análisis de prácticas recomendadas desde la [línea de comandos](xref:command-line-options), el número indica la gravedad de una infracción:
  - 1 = solo informativo
  - 2 = advertencia
  - 3 (o superior) = error
- **Categoría**: agrupa reglas relacionadas.
- **Descripción** (opcional): una descripción de la regla, que se muestra como una ayuda emergente en la **vista del Best Practice Analyzer**. La descripción admite estos marcadores de posición:
  - `%object%` devuelve una referencia DAX totalmente calificada (si corresponde) al objeto actual
  - `%objectname%` devuelve solo el nombre del objeto actual
  - `%objecttype%` devuelve el tipo del objeto actual
- **Se aplica a**: los tipos de objeto que comprueba la regla.
- **Expresión**: una expresión de [Dynamic LINQ](https://dynamic-linq.net/expression-language) que se evalúa como `true` para los objetos, entre los tipos seleccionados en **Se aplica a**, que infringen la regla. La expresión puede usar las propiedades de TOM de los tipos de objeto seleccionados y una amplia variedad de métodos y propiedades estándar de .NET.
- **Nivel mínimo de compatibilidad**: el nivel de compatibilidad más bajo de los modelos a los que se aplica la regla. Algunas propiedades de TOM no existen en todos los niveles de compatibilidad.

Una colección de reglas en disco almacena estas propiedades como JSON. También puedes agregar, editar y eliminar reglas directamente en el archivo JSON. En el archivo, puedes establecer la propiedad `FixExpression` de una regla: una cadena que genera un [C# Script](xref:cs-scripts-and-macros) que corrige la infracción.

## Uso de la vista de Best Practice Analyzer

La **vista del Best Practice Analyzer** enumera las infracciones de las reglas, y la barra de estado en la parte inferior de la ventana principal muestra su número. Abre la vista desde **View > Best Practice Analyzer** o mediante el botón **# BP issues** de la barra de estado.

![Vista de Best Practice Analyzer](~/content/assets/images/best-practice-analyzer-view.png)

La vista muestra cada regla con objetos que la incumplen, y debajo, los objetos. Haz doble clic en un objeto para seleccionarlo en el **Explorador TOM**.

![Menú contextual de un objeto en la vista del Best Practice Analyzer](~/content/assets/images/bpa-options.png)

Haz clic con el botón derecho en un objeto para ver estas opciones:

- **Ir al objeto**: selecciona el objeto en el **Explorador TOM**, igual que al hacer doble clic en él.
- **Ignorar objeto**: agrega una anotación al objeto para que el Best Practice Analyzer omita esta regla para ese objeto. La anotación almacena el ID de la regla.
- **Generar script de corrección**: crea un C# Script a partir de la `FixExpression` de las reglas seleccionadas. Disponible solo si la regla tiene una `FixExpression`.
- **Aplicar corrección**: ejecuta la `FixExpression` de las reglas seleccionadas. Disponible solo si la regla tiene una `FixExpression`.

> [!NOTE]
> Mantén pulsada la tecla Mayús o Ctrl para seleccionar varios objetos en la vista de Best Practice Analyzer.

La barra de herramientas situada en la parte superior de la vista tiene las mismas opciones, además de botones para expandir o contraer todos los elementos, mostrar las reglas y los objetos ignorados, y actualizar manualmente el análisis.

## Desactivar el Best Practice Analyzer

Desactiva el análisis en segundo plano si algunas reglas tardan mucho en evaluarse o el modelo es muy grande: desmarca **Buscar infracciones de mejores prácticas en segundo plano** en la sección **Best Practice Analyzer** de **Herramientas > Preferencia > Tabular Editor > Varios**. Con el análisis en segundo plano desactivado, haz clic en **Actualizar** en la **vista de Best Practice Analyzer** para ejecutar el análisis.

## Pasos siguientes

- @cs-scripts-and-macros
- @personalizing-te3
