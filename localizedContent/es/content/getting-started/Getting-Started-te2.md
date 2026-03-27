---
uid: getting-started-te2
title: Primeros pasos con Tabular Editor 2
author: Daniel Otykier
updated: 2021-09-21
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      none: true
---

# Primeros pasos

## Instalación

Simplemente descarga el archivo .msi desde la [página de versiones](https://github.com/TabularEditor/TabularEditor/releases/latest) y ejecuta el instalador .msi.

## Requisitos previos

Ninguno.

> [!NOTE]
> Tabular Editor usa el [Tabular Object Model](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) para cargar metadatos desde archivos Model.bim o bases de datos existentes, y volver a guardarlos en ellos. Esto se incluye en el instalador .msi. Consulta la documentación oficial de Microsoft sobre [Analysis Services Client Libraries](https://docs.microsoft.com/en-us/azure/analysis-services/analysis-services-data-providers).

## Requisitos del sistema

- **Sistema operativo:** Windows 7, Windows 8, Windows 10, Windows Server 2016, Windows Server 2019 o posterior
- **.NET Framework:** [4,6](https://dotnet.microsoft.com/download/dotnet-framework)

## Trabajar con Tabular Editor

El flujo de trabajo recomendado es configurar las tablas y relaciones con SSDT como de costumbre y, a continuación, usar Tabular Editor para el resto. Es decir: crea columnas calculadas, medidas, jerarquías, perspectivas, traducciones, carpetas de visualización y cualquier otro ajuste fino que se te ocurra.

Carga un archivo Model.bim seleccionando Abrir > Desde archivo... en el menú Archivo (CTRL+O), o abre una base de datos existente desde una instancia de Analysis Services seleccionando Abrir > Desde BD... opción. En este último caso, se te pedirá un nombre de servidor y credenciales opcionales:

![Conexión a un modelo tabular ya implementado](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/Connect.png)

Esto también es compatible con el nuevo Azure Analysis Services PaaS. El menú desplegable "Instancia local" se puede usar para explorar y conectarte a cualquier instancia en ejecución de Power BI Desktop o a espacios de trabajo integrados de Visual Studio. **Ten en cuenta que, aunque Tabular Editor puede realizar cambios en un modelo de Power BI a través de TOM, Microsoft no admite todas las operaciones de modelado. [Más información](Power-BI-Desktop-Integration.md)**

Después de hacer clic en "Aceptar", se mostrará una lista de bases de datos en el servidor.

Así es como se ve la interfaz de usuario después de cargar un modelo en Tabular Editor:

![La interfaz de usuario principal de Tabular Editor](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/Main%20UI.png)

El árbol del lado izquierdo de la pantalla muestra todas las tablas del modelo tabular. Al expandir una tabla, se mostrarán todas las columnas, medidas y jerarquías dentro de la tabla, agrupadas por sus carpetas de visualización. Usa los botones justo encima del árbol para alternar las carpetas de visualización, los objetos ocultos, ciertos tipos de objetos o para filtrar objetos por nombre. Al hacer clic con el botón derecho en cualquier parte del árbol, se abrirá un menú contextual con acciones habituales, como agregar nuevas medidas, ocultar un objeto, duplicar objetos, eliminar objetos, etc. Pulsa F2 para cambiar el nombre del objeto seleccionado actualmente, o selecciona varios y haz clic con el botón derecho para cambiar el nombre en lote de varios objetos.

![El cambio de nombre en lote te permite cambiar el nombre de varios objetos a la vez](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/BatchRename.png)

En la parte superior derecha de la interfaz de usuario principal, verás el Editor de DAX, que puedes usar para editar la expresión DAX de cualquier medida o columna calculada del modelo. Haz clic en el botón "DAX Formatter" para dar formato automáticamente al código a través de www.daxformatter.com.

Usa la cuadrícula de propiedades en la esquina inferior derecha para revisar y configurar las propiedades de los objetos, como la cadena de formato, la descripción, las traducciones y la pertenencia a perspectivas. Aquí también puedes establecer la propiedad "carpeta de visualización", pero es más sencillo arrastrar y soltar objetos dentro del árbol para actualizar su carpeta de visualización (prueba a seleccionar varios objetos con CTRL o SHIFT).

Para editar perspectivas o traducciones (configuraciones regionales), selecciona el objeto "Model" en el árbol y localiza las propiedades "Model Perspectives" o "Model Cultures" en la cuadrícula de propiedades. Haz clic en el pequeño botón de puntos suspensivos para abrir un editor de colecciones y agregar, quitar o editar perspectivas y configuraciones regionales.

![Edición de perspectivas: haz clic en el botón de puntos suspensivos de la derecha](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/Edit%20Perspectives.png)

Para guardar los cambios en el archivo Model.bim, haz clic en el botón Guardar o pulsa CTRL+S. Si abriste una base de datos tabular existente, los cambios se guardan directamente en la base de datos. Se te avisará si la base de datos cambió desde que la cargaste en Tabular Editor. Siempre puedes deshacer los cambios pulsando CTRL+Z.

Si quieres implementar tu modelo en otra ubicación, ve al menú "Modelo" y elige "Implementar".

## Implementación

Tabular Editor incluye un asistente de implementación que ofrece algunas ventajas frente a la implementación desde SSDT, especialmente al implementar en una base de datos existente. Después de elegir un servidor y una base de datos donde realizar la implementación, tienes las siguientes opciones:

![Asistente de implementación](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/Deployment.png)

Si dejas sin marcar la casilla "Implementar conexiones", te aseguras de que todos los Data source de la base de datos de destino se mantengan intactos. Recibirás un error si tu modelo contiene una o más tablas con un Data source que no exista ya en la base de datos de destino.

Del mismo modo, si omites "Implementar particiones de tabla", te aseguras de que las particiones existentes en tus tablas no se modifiquen, manteniendo intactos los datos de las particiones.

Cuando la casilla "Implementar roles" está marcada, los roles de la base de datos de destino se actualizarán para reflejar lo que tienes en el modelo cargado; sin embargo, si la casilla "Implementar miembros de rol" está desmarcada, los miembros de cada rol no cambiarán en la base de datos de destino.

## Uso de la línea de comandos

Puedes usar la línea de comandos para una implementación automatizada. Todas las opciones de implementación disponibles en la GUI también lo están en la línea de comandos.

### Ejemplos de implementación

`TabularEditor.exe c:\Projects\Model.bim`

Abre la GUI de Tabular Editor y carga el archivo Model.bim especificado (sin implementar nada).

`TabularEditor.exe c:\Projects\Model.bim -deploy localhost AdventureWorks`

Implementa el archivo Model.bim especificado en la instancia de SSAS que se ejecuta en localhost, sobrescribiendo o creando la base de datos AdventureWorks. La GUI no se cargará.

De forma predeterminada, las particiones, los Data source y los roles no se sobrescribirán en la base de datos de destino. Este comportamiento se puede cambiar añadiendo uno o más de los siguientes modificadores al comando anterior:

- `-P` Sobrescribir **p**articiones
- `-C` Sobrescribir **c**onexiones (Data source)
- `-R` Sobrescribir **r**oles
- `-M` Sobrescribir **m**iembros del rol

Puedes encontrar más información sobre las opciones de la línea de comandos [aquí](../features/Command-line-Options.md).

> [!NOTE]
> Como TabularEditor.exe es una aplicación de Windows Forms, al ejecutarla desde la línea de comandos se hará en un subproceso distinto, devolviendo el control al proceso que la invocó de inmediato. Si tienes estos problemas, usa `start /wait` para que TabularEditor termine su trabajo antes de devolver el control al proceso que lo invocó: Esto puede causar problemas al ejecutar despliegues como parte de un trabajo por lotes, cuando necesitas esperar a que el despliegue se complete correctamente antes de continuar con la tarea.
>
> `start /wait TabularEditor.exe c:\Projects\Model.bim -deploy localhost AdventureWorks`

## Scripting avanzado

Tabular Editor te permite usar C# para crear scripts que modifiquen el modelo cargado. Esto es práctico cuando quieres aplicar varios cambios a muchos objetos a la vez. El editor de scripts avanzado tiene acceso a dos objetos:

- `Selected`, que representa todos los objetos que están seleccionados actualmente en el árbol del explorador.
- `Model`, que representa todo el árbol del Tabular Object Model.

El editor de scripts avanzado incluye una funcionalidad de IntelliSense limitada para ayudarte a empezar:

![IntelliSense te ayuda a crear scripts para Tabular Editor](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/AdvancedEditor%20intellisense.png)

Puedes encontrar más documentación y ejemplos sobre scripting avanzado [aquí](../how-tos/Advanced-Scripting.md).
