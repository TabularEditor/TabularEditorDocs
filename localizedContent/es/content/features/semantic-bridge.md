---
uid: semantic-bridge
title: Puente semántico
author: Greg Baldini
updated: 2025-01-23
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.25.0
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          none: true
        - edition: Enterprise
          full: true
---

# Puente semántico

<!--
SUMMARY: Overview of the Semantic Bridge feature - a multi-platform semantic model compiler that enables translation between different semantic model platforms (e.g., Databricks Metric Views to Microsoft's Tabular model in Analysis Services and Power BI / Fabric).
-->

> [!NOTE]
> El Puente semántico, tal como se lanzó en 3.25.0, es una característica MVP. Tiene limitaciones, como se documenta a continuación, y tanto la API como el alcance de la funcionalidad pueden cambiar.

El Puente semántico es un compilador de modelos semánticos capaz de traducir la estructura y las expresiones de un modelo semántico de una plataforma a otra.
Esto permite reutilizar la lógica de negocio en varias plataformas de datos, dar soporte a los usuarios finales y llegar hasta donde consumen los datos.
También permite migraciones de una plataforma a otra.

<a name="interface"></a>

## Interfaz

### Importar YAML de Metric View

El Puente semántico está disponible a través de **Archivo > Abrir > Importar desde Metric View YAML**.
Se abrirá un cuadro de diálogo que le guiará a través de la importación de una Metric View en el modelo tabular actual y añadirá tablas, columnas, medidas y relaciones según la estructura de la Metric View.
Debe tener un modelo tabular abierto en Tabular Editor.
Puede ser un modelo nuevo y vacío, o un modelo existente que desee mejorar con los objetos de la Metric View.
El botón del menú no se habilitará hasta que abra o cree un nuevo modelo tabular.

![Importar una Metric View desde el menú Archivo con Archivo > Abrir > Importar desde Metric View YAML](~/content/assets/images/features/semantic-bridge/semantic-bridge-file-menu-import.png)

### Introducir los detalles de conexión de Databricks

Debe proporcionar tres datos en este cuadro de diálogo:

1. La ruta del archivo YAML de Metric View.
   Puedes pegar la ruta del archivo o usar el botón **Examinar** para localizarlo.
2. El nombre de host de Databricks.
   Esto sirve para proporcionar el argumento correcto en la partición M que se genera para el sistema de origen de Databricks.
3. La ruta HTTP de Databricks.
   Esto sirve para proporcionar el argumento correcto en la partición M que se genera para el sistema de origen de Databricks.

Si solo estás probando la función de traducción, puedes indicar valores de marcador de posición para los dos últimos elementos, pero tendrás que corregir las definiciones de las particiones M antes de poder actualizar los datos en tu modelo tabular.

Después de completar los detalles, haz clic en **Aceptar**.
Semantic Bridge traducirá tu Metric View a Tabular y creará todos los objetos TOM por ti.

![Detalles de Databricks en el cuadro de diálogo de importación](~/content/assets/images/features/semantic-bridge/semantic-bridge-metric-view-details.png)

### Resultado

Hay tres resultados posibles:

1. Éxito: todo lo que había en Metric View se tradujo a Tabular y tienes un modelo tabular listo para usar.
2. Éxito, pero con algunos problemas: Semantic Bridge no pudo traducir todos los objetos de Metric View; hay mensajes de diagnóstico que puedes revisar para entender qué requiere tu atención.
3. Fallo: Semantic Bridge no pudo traducir Metric View

Después de cualquiera de los dos tipos de éxito, puedes usar las funciones de deshacer/rehacer con normalidad en Tabular Editor para deshacer o repetir al instante la importación.

**Éxito**

![Notificación de importación exitosa](~/content/assets/images/features/semantic-bridge/semantic-bridge-import-success.png)

**Éxito con problemas**

![Notificación de importación exitosa con incidencias](~/content/assets/images/features/semantic-bridge/semantic-bridge-import-success-with-issues.png)

Si haces clic en **Ver diagnósticos**, puedes ver una lista de mensajes que describen los problemas en la traducción.
Estos diagnósticos están disponibles para revisarlos más adelante al emitirlos desde un C# Script:

```csharp
// Mostrar todos los mensajes de diagnóstico del último intento de importación de una Metric View
SemanticBridge.MetricView.ImportDiagnostics.Output();
```

![Diagnóstico de importación](~/content/assets/images/features/semantic-bridge/semantic-bridge-import-diagnostics.png)

**Fallo**

![Importación fallida](~/content/assets/images/features/semantic-bridge/semantic-bridge-import-failed.png)

Ver los diagnósticos de un fallo es lo mismo que para un éxito con problemas.

## Proceso de traducción

La traducción de una Metric View a un modelo tabular se realiza en varios pasos:

1. Leer el YAML del disco
2. Deserializar el YAML
3. Validar que el YAML deserializado represente una Metric View válida
4. Si es una Metric View válida, almacenarla como la Metric View cargada actualmente, de forma similar a como se interactúa con un modelo tabular cargado.
   Si no es una Metric View válida, el proceso se detiene aquí y se mostrarán mensajes.
5. Analizar la Metric View e intentar transformarla en una representación intermedia
6. Intentar transformar la representación intermedia en un modelo tabular

La GUI de importación descrita anteriormente se encarga de todo por ti, pero también puedes usar scripts C# para personalizar distintos pasos del proceso y operar sobre Metric View mediante programación, de forma similar a como lo haces con un modelo tabular.
En concreto, puedes

- cargar una Metric View desde el disco con [`SemanticBridge.MetricView.Load`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Load_System_String_): la carga la pone a disposición en scripts de C# como [`SemanticBridge.MetricView.Model`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Model), pero no importa la estructura en el modelo tabular
- deserializar una Metric View desde una cadena con [`SemanticBridge.MetricView.Deserialize`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Deserialize_System_String_): al igual que al cargarla, el modelo queda disponible como [`SemanticBridge.MetricView.Model`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Model), pero no se importa
- guardar una Metric View en el disco con [`SemanticBridge.MetricView.Save`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Save_System_String_)
- serializar una Metric View en una cadena con [`SemanticBridge.MetricView.Serialize`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Serialize).
- validar una Metric View usando un sistema similar al [Best Practice Analyzer](xref:best-practice-analyzer) con [`SemanticBridge.MetricView.Validate`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Validate)
  - puedes crear tus propias reglas de validación personalizadas con [`SemanticBridge.MetricView.MakeValidationRule`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_MakeValidationRule__1_System_String_System_String_System_Func___0_TabularEditor_SemanticBridge_Platforms_Databricks_Validation_IReadOnlyValidationContext_System_Collections_Generic_IEnumerable_TabularEditor_SemanticBridge_Orchestration_DiagnosticMessage___) y sus versiones más simples
- importar una Metric View a un modelo tabular con [`SemanticBridge.MetricView.ImportToTabularFromFile`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_ImportToTabularFromFile_System_String_TabularEditor_TOMWrapper_Model_System_String_System_String_System_Collections_Generic_List_TabularEditor_SemanticBridge_Orchestration_DiagnosticMessage___System_Boolean_), que hace exactamente lo mismo que la GUI mostrada arriba, o [`SemanticBridge.MetricView.ImportToTabular`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_ImportToTabular_TabularEditor_TOMWrapper_Model_System_String_System_String_System_Collections_Generic_List_TabularEditor_SemanticBridge_Orchestration_DiagnosticMessage___System_Boolean_), que es similar, pero opera sobre la Metric View cargada actualmente, en lugar de leer una desde el disco.

<a name="mvp-limitations"></a>

## Limitaciones del MVP

### Plataformas compatibles

En la versión MVP, admitimos traducciones desde una Databricks Metric View a un modelo tabular.
En concreto, admitimos las siguientes partes de una Databricks Metric View:

- v0.1 Propiedades de Metric View:
  - compatibles:
    - `source`: el origen de la tabla de hechos
    - `joins`: colección de tablas unidas por la izquierda a la tabla de hechos
    - `dimensions`: colección plana de campos de cualquier tabla, ya sea la única tabla de hechos o cualquiera de las muchas uniones
    - `measures`: colección plana de medidas con nombre que representan la lógica de negocio
  - no compatibles:
    - `filter`: una expresión de filtro SQL para la Metric View

En el MVP no se admite ningún metadato v1.1.
Cualquier metadato v1.1 se ignora silenciosamente al deserializar una Metric View, por lo que no será visible en un C# Script y no afectará en modo alguno a la traducción a Tabular.

> [!WARNING]
> Como los metadatos v1.1 se ignoran silenciosamente, a una Metric View que deserialices y luego serialices le faltarán estos metadatos.
> Tenga cuidado de no sobrescribir un archivo YAML fuente v1.1 mediante un C# Script, ya que eso eliminará todos los metadatos v1.1.

### Limitaciones de la traducción desde SQL

Las Metric Views proporcionan una capa estructurada sobre expresiones SQL, por lo que parte de traducir una Metric View consiste en traducir SQL a DAX y M en el modelo tabular.

- No se admiten `joins` de Metric View con `joins` anidados.
  En otras palabras, para la traducción solo se admiten esquemas en estrella estrictos; no se admiten los modelos en copo de nieve
- No se admiten `joins` de Metric View con criterios de unión `using`; solo se admiten equijoins sobre un único campo clave mediante la propiedad `on`.
- Las `dimensions` de Metric View con expresiones SQL no se traducen a M ni a DAX; se presentan como columnas calculadas del modelo tabular, con su expresión SQL comentada
- Las `measures` de Metric View con agregaciones no básicas no se traducen a DAX; se presentan como una medida del modelo tabular, con su expresión SQL comentada
  - Las únicas agregaciones admitidas son `sum`, `max`, `min`, `average`, `count` y `distinct count`.
  - Los comentarios SQL en una agregación básica no se conservan en DAX

> [!WARNING]
> Tenga en cuenta que SQL y DAX son lenguajes diferentes con semánticas distintas.
> No podemos garantizar que una medida traducida se comporte de forma idéntica entre el SQL de Metric View y el DAX tabular que generamos.
> Las agregaciones básicas definidas sobre campos de la tabla de hechos deberían comportarse igual, mientras que las agregaciones definidas sobre campos de las tablas de dimensiones tienen más probabilidades de producir resultados no deseados.

### Conectividad

El MVP no se conecta a ninguna plataforma aparte de Tabular, sino que funciona completamente con archivos locales.
Debe crear su YAML de Metric View por su cuenta y luego colocarlo donde Tabular Editor pueda verlo.

### API de C\#

La interfaz de C# se ha diseñado para optimizar el flujo de trabajo de traducción automática.
Por ello, hay pocas opciones para interactuar con la Metric View cargada actualmente, y ciertos tipos de operaciones resultan torpes.

## Apéndice sobre nomenclatura

Puede resultar confuso hablar del Semantic Bridge, ya que hay muchas palabras que tienen significados tanto genéricos como específicos, según el nivel de abstracción del que estemos hablando y la plataforma que estemos tratando.
Por ejemplo, el término "modelo semántico" es a la vez genérico, ya que se refiere al concepto de una colección de datos y lógica de negocio en una forma adecuada para dar soporte a las necesidades de informes y análisis, y también es el nombre que Microsoft ha adoptado para referirse a su implementación específica de este concepto genérico en Power BI y Fabric.
Así, un modelo semántico puede referirse de forma genérica a una Metric View de Databricks, a un cubo OLAP/multidimensional, a un modelo semántico de Power BI o a un modelo hospedado en la capa semántica de otra plataforma.
Del mismo modo, "dimension" hace referencia a un concepto del modelado dimensional, pero también es el nombre de un tipo específico de objeto en una Metric View.
Por ello, hemos adoptado las siguientes definiciones y estándares en nuestra documentación para mantener la claridad y la coherencia.

> [!NOTE]
> Estas convenciones solo están pensadas para la documentación sobre la funcionalidad Semantic Bridge.

### Definiciones

- _modelo semántico_: cuando se usa por sí solo, siempre se refiere al concepto genérico de una colección de datos, metadatos y lógica de negocio para respaldar la elaboración de informes y el análisis.
  Si y solo si va inmediatamente precedido de "Fabric" o "Power BI", entonces se refiere a ese tipo de artefacto en esa plataforma, concretamente a un modelo tabular que se guarda como TMDL o BIM y utiliza M y DAX; solemos preferir usar el término modelo tabular para referirnos al modelo semántico de Power BI / Fabric y evitar esta confusión siempre que sea posible, porque el modelo tabular se comparte en Power BI / Fabric, así como en Analysis Services Tabular.
- _Plataforma_: una solución tecnológica que tiene una capa semántica, en la que se aloja un modelo semántico genérico.
  Databricks Metric Views representan una plataforma; Fabric / Power BI representan una plataforma; Analysis Services Tabular es una plataforma; Analysis Services Multidimensional es una plataforma para la que hoy no tenemos compatibilidad en Semantic Bridge.
- _Formato de serialización_: una forma de representar un modelo semántico en disco en un formato textual.
  TMDL y TMSL (.bim) son dos formatos de serialización para un modelo semántico de Power BI; YAML es el formato de serialización de un Databricks Metric View.
- _Modelo de objetos_: una representación en memoria de un modelo semántico con la que trabajamos en Tabular Editor mediante Semantic Bridge, ya sea a través de acciones en la GUI o mediante C# Scripts.
  El TOM, o Tabular Object Model, debería resultar familiar a los usuarios actuales de Tabular Editor.
  También hemos creado un modelo de objetos para Databricks Metric Views, para permitir su manipulación en nuestra herramienta.

### Terminología general de modelado dimensional

Hay muchos términos que se usan de forma general al hablar de un modelo dimensional o de un modelo semántico, y también dentro del modelo de objetos y los formatos de serialización de una plataforma específica.
En una Metric View, una medida es una expresión SQL con nombre que define una agregación en la Metric View, y en un modelo tabular, una medida es una expresión DAX con nombre que define una agregación en el modelo tabular.
Es imposible hablar del trabajo de Semantic Bridge sin hablar a la vez de los múltiples significados de estas palabras.
Por ejemplo, hablamos de traducir una medida de Metric View a una medida tabular.
Por eso, **siempre nos referimos a un objeto del modelo de una plataforma específica indicando la plataforma y el objeto, por ejemplo "medida de Metric View" o "medida tabular"**.
Si alguna vez se usa el término sin ir acompañado del nombre de una plataforma, entonces estamos hablando de la idea de forma genérica.

### Términos comunes en Metric Views y modelos tabulares

Para los usuarios que quizá no estén familiarizados ni con Metric Views ni con modelos tabulares, a continuación ofrecemos una piedra de Rosetta incompleta.
Nos referimos a los nombres de los objetos de Metric View en función de su representación en YAML, y a los de Tabular en función del nombre del tipo de objeto en TMDL/TMSL.

| Término general | Nombre en Tabular | Nombre en Metric View                                | Descripción                                                                                                                         | Nota                                                                                                                                                                                                                                                                                                                                   |
| --------------- | ----------------- | ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| hecho           | tabla             | fuente                                               | Una tabla que contiene claves foráneas hacia las dimensiones y valores cuantitativos que se van a agregar                           | una Metric View tiene un único hecho, sin nombre, que se registra como el atributo `source` en el nivel raíz del YAML. Los modelos tabulares no diferencian entre tipos de tablas: si una tabla es una tabla de hechos solo puede inferirse                                                            |
| dimensión       | tabla             | unión                                                | Una tabla que contiene atributos descriptivos y una clave principal con la que se relaciona el hecho                                | Los modelos tabulares no diferencian, por lo que el rol de "dimensión" solo se infiere, igual que con un hecho.                                                                                                                                                                                                        |
| partición       | partición         | fuente (solo para joins)          | Un objeto para la administración de datos que contiene un subconjunto de datos en una tabla                                         | Las tablas de un modelo tabular pueden tener muchas particiones y deben tener al menos una. El hecho de Metric View, como se mencionó anteriormente, se define únicamente como una fuente, pero las uniones de Metric View también tienen una propiedad `source`, que actúa, en términos generales, como una partición |
| campo           | columna           | dimensión                                            | Una columna en una tabla                                                                                                            |                                                                                                                                                                                                                                                                                                                                        |
| medida          | medida            | medida                                               | Un valor cuantitativo que se agrega conforme a la lógica de negocio del modelo                                                      | Las medidas en un modelo tabular se escriben en DAX y, en una Metric View, en SQL                                                                                                                                                                                                                                                      |
| join o relación | relación          | join.on o join.using | Una correspondencia entre los campos clave de dos tablas: una clave externa en una y una clave principal en la otra | Las relaciones son objetos explícitos en un modelo tabular y se definen implícitamente como una propiedad del objeto `join` en el YAML de Metric View                                                                                                                                                                                  |

## Recursos adicionales

- [Documentación de Metric View de Databricks](https://learn.microsoft.com/en-us/azure/databricks/metric-views/)
- [Referencia de YAML de Metric View de Databricks](https://learn.microsoft.com/en-us/azure/databricks/metric-views/data-modeling/syntax)
- @semantic-bridge-how-tos
