---
uid: best-practice-analyzer
title: Best Practice Analyzer
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

# Best Practice Analyzer

A partir de [Tabular Editor 2.8.1](https://github.com/TabularEditor/TabularEditor/releases/tag/2.8.1), el Best Practice Analyzer ha recibido una importante renovación.

Lo primero que notarás es que Tabular Editor ahora informa del número de problemas de Best Practice directamente en la interfaz de usuario principal:

![image](https://user-images.githubusercontent.com/8976200/53631987-baee5880-3c0b-11e9-9d66-e906cccce2be.png)

Cada vez que se realiza un cambio en el modelo, el Best Practice Analyzer analiza tu modelo en segundo plano en busca de incidencias. Puedes desactivar esta función en Archivo > Preferencias.

Al hacer clic en el enlace (o pulsar F10), se abre la interfaz de usuario nueva y mejorada del Best Practice Analyzer:

![image](https://user-images.githubusercontent.com/8976200/53631947-9eeab700-3c0b-11e9-9217-5739d4de2f88.png)

Si has usado el Best Practice Analyzer en versiones anteriores, lo primero que notarás es que la interfaz de usuario se ha rediseñado por completo, de modo que ocupa menos espacio en pantalla. Esto te permite acoplar la ventana a un lado del escritorio y dejar la ventana principal al otro, para trabajar con ambas a la vez.

La ventana del Best Practice Analyzer muestra continuamente todas las **reglas efectivas** del modelo, así como los objetos que incumplen cada regla. Al hacer clic con el botón derecho en cualquier parte de la lista o al usar los botones de la barra de herramientas en la parte superior de la ventana, puedes realizar las siguientes acciones:

- **Administrar reglas...**: Esto abre la interfaz de Administrar reglas, que veremos más abajo. También puedes acceder a esta interfaz desde el menú "Tools > Manage BPA Rules..." de la interfaz de usuario principal.
- **Ir al objeto...**: Al elegir esta opción o hacer doble clic en un objeto de la lista, irás al mismo objeto en la interfaz de usuario principal.
- **Ignorar elemento/elementos**: Al seleccionar uno o varios objetos de la lista y elegir esta opción, se aplicará una anotación a los objetos seleccionados indicando que el Best Practice Analyzer debe ignorarlos de ahora en adelante. Si ignoraste un objeto por error, activa o desactiva el botón "Mostrar ignorados" en la parte superior de la pantalla. Esto te permitirá dejar de ignorar un objeto que se había ignorado anteriormente.
- **Ignorar regla**: Si has seleccionado una o varias reglas en la lista, esta opción agregará una anotación a nivel de modelo que indica que la regla seleccionada debe ignorarse siempre. De nuevo, al activar/desactivar el botón "Mostrar ignorados", también puedes dejar de ignorar reglas.
- **Generar script de corrección**: Las reglas que tienen una corrección sencilla (es decir, el problema se puede resolver simplemente estableciendo una sola propiedad en el objeto) tendrán esta opción habilitada. Al hacer clic, se copiará un C# Script al portapapeles. Luego, puedes pegar este script en el área de [Scripting avanzado](../how-tos/Advanced-Scripting.md) de Tabular Editor, donde podrás revisarlo antes de ejecutarlo para aplicar la corrección.
- **Aplicar corrección**: Esta opción también está disponible para las reglas que tienen una corrección sencilla, como se mencionó anteriormente. En lugar de copiar el script al portapapeles, se ejecutará inmediatamente.

## Gestión de reglas de prácticas recomendadas

Si necesita agregar, quitar o modificar las reglas que se aplican a su modelo, también hay una interfaz de usuario totalmente nueva para ello. Puede abrirla haciendo clic en el botón de la esquina superior izquierda de la ventana de Best Practice Analyzer o usando la opción de menú "Herramientas > Administrar Reglas de BPA..." en la ventana principal.

![image](https://user-images.githubusercontent.com/8976200/53632990-2f29fb80-3c0e-11e9-82fe-ee9c921662c7.png)

Esta interfaz de usuario contiene dos listas: La lista superior representa las **colecciones** de reglas que están cargadas actualmente. Al seleccionar una colección en esta lista, se mostrarán todas las reglas definidas dentro de esa colección en la lista inferior. De forma predeterminada, se muestran tres colecciones de reglas:

- **Reglas dentro del modelo actual**: Como indica el nombre, es la colección de reglas que se han definido dentro del modelo actual. Las definiciones de las reglas se almacenan como una anotación en el objeto modelo.
- **Reglas para el usuario local**: Estas son reglas que se almacenan en el archivo `%AppData%\..\Local\TabularEditor3\BPARules.json` (Tabular Editor 3) o en el archivo `%AppData%\..\Local\TabularEditor\BPARules.json` (Tabular Editor 2). Estas reglas se aplicarán a todos los modelos que el usuario de Windows que haya iniciado sesión cargue en Tabular Editor.
- **Reglas en el equipo local**: Estas reglas se almacenan en `%ProgramData%\\TabularEditor\\BPARules.json`. Estas reglas se aplicarán a todos los modelos que se carguen en Tabular Editor en este equipo.

Si la misma regla (por ID) se encuentra en más de una colección, el orden de prioridad va de arriba abajo; es decir, una regla definida en el modelo tiene prioridad sobre una regla con el mismo ID definida en el equipo local. Esto le permite anular reglas existentes, por ejemplo, para tener en cuenta convenciones específicas del modelo.

En la parte superior de la lista, verá una colección especial llamada **(Reglas efectivas)**. Al seleccionar esta colección, verá la lista de reglas que realmente se aplican al modelo cargado actualmente, respetando la prioridad de las reglas con IDs idénticos, como se mencionó anteriormente. La lista inferior indicará a qué colección pertenece una regla. Además, verá que el nombre de una regla estará tachado si existe una regla con un ID similar en una colección de mayor prioridad:

![image](https://user-images.githubusercontent.com/8976200/53633831-74e7c380-3c10-11e9-925e-1419987f5a17.png)

### Agregar colecciones adicionales

Una nueva característica de Tabular Editor 2.8.1 es la posibilidad de incluir en un modelo reglas provenientes de otras fuentes. Por ejemplo, si tiene un archivo de reglas en un recurso compartido de red, ahora puede incluir ese archivo como una colección de reglas en el modelo actual. Si tienes acceso de escritura a la ubicación del archivo, también podrás agregar/modificar/eliminar reglas en el archivo. Las colecciones de reglas que se agregan de esta forma tienen prioridad sobre las reglas definidas dentro del modelo. Si agregas varias colecciones de este tipo, puedes subirlas y bajarlas para controlar su prioridad relativa.

Haz clic en el botón "Agregar..." para agregar una nueva colección de reglas al modelo. Esto ofrece las siguientes opciones:

![image](https://user-images.githubusercontent.com/8976200/53634211-7cf43300-3c11-11e9-8fed-7df113264a6f.png)

- **Crear nuevo archivo de reglas**: Esto creará un nuevo archivo .json vacío en la ubicación especificada, al que podrás agregar reglas posteriormente. Al elegir el archivo, ten en cuenta que hay una opción para usar rutas de archivo relativas. Esto es útil cuando quieres almacenar el archivo de reglas en el mismo repositorio de código que el modelo actual. Sin embargo, ten en cuenta que una referencia relativa al archivo de reglas solo funciona cuando el modelo se ha cargado desde el disco (ya que no hay un directorio de trabajo al cargar un modelo desde una instancia de Analysis Services).
- **Incluir archivo de reglas local**: Usa esta opción si ya tienes un archivo .json que contiene reglas y quieres incluirlo en tu modelo. De nuevo, tienes la opción de usar rutas de archivo relativas, lo cual puede ser útil si el archivo está cerca de los metadatos del modelo. Si el archivo está en un recurso compartido de red (o, en general, en una unidad distinta de aquella donde residen los metadatos del modelo cargado actualmente), solo puedes incluirlo mediante una ruta absoluta.
- **Incluir archivo de reglas desde URL**: Esta opción te permite especificar una URL HTTP/HTTPS que debe devolver una definición de reglas (JSON) válida. Esto es útil si quieres incluir reglas desde una fuente en línea; por ejemplo, las [reglas BPA estándar](https://raw.githubusercontent.com/microsoft/Analysis-Services/master/BestPracticeRules/BPARules.json) del [sitio de GitHub de BestPracticeRules](https://github.com/microsoft/Analysis-Services/tree/master/BestPracticeRules). Ten en cuenta que las colecciones de reglas agregadas desde fuentes en línea serán de solo lectura.

### Modificar reglas dentro de una colección

La parte inferior de la pantalla te permitirá agregar, editar, clonar y eliminar reglas dentro de la colección seleccionada, siempre que tengas acceso de escritura a la ubicación donde se almacena la colección. Además, el botón "Mover a..." te permite mover o copiar la regla seleccionada a otra colección, lo que facilita la administración de varias colecciones de reglas.

### Marcadores de posición de la descripción de la regla

Una pequeña mejora respecto a versiones anteriores es que ahora puedes usar los siguientes valores de marcador de posición en la descripción de la regla de prácticas recomendadas. Esto ofrece descripciones más personalizables que aparecerán como información sobre herramientas en la interfaz de usuario de prácticas recomendadas:

- `%object%` devuelve una referencia DAX totalmente calificada (si corresponde) al objeto actual
- `%objectname%` devuelve solo el nombre del objeto actual
- `%objecttype%` devuelve el tipo del objeto actual

![image](https://user-images.githubusercontent.com/8976200/53671918-587f7180-3c78-11e9-855f-ed497f2c0c98.png)
