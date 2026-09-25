---
uid: semantic-bridge
title: Puente semántico
author: Greg Baldini
updated: 2026-07-02
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
> The Semantic Bridge is in public preview.
> Tiene limitaciones, como se documenta a continuación, y tanto la API como el alcance de la funcionalidad pueden cambiar.

El Puente semántico es un compilador de modelos semánticos capaz de traducir la estructura y las expresiones de un modelo semántico de una plataforma a otra.
Esto permite reutilizar la lógica de negocio en varias plataformas de datos, dar soporte a los usuarios finales y llegar hasta donde consumen los datos.
También permite migraciones de una plataforma a otra.

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

```csharp {compile}
// Show all diagnostic messages from the last attempted import of a Metric View
var sb = new System.Text.StringBuilder();
foreach (var d in SemanticBridge.MetricView.ImportDiagnostics)
{
    sb.AppendLine($"[{d.Severity}] {d.Code} {d.Path}");
    sb.AppendLine($"    {d.Context} {d.Message}");
    sb.AppendLine();
}
Output(sb.ToString());
```

![Diagnóstico de importación](~/content/assets/images/features/semantic-bridge/semantic-bridge-import-diagnostics.png)

**Fallo**

![Importación fallida](~/content/assets/images/features/semantic-bridge/semantic-bridge-import-failed.png)

Ver los diagnósticos de un fallo es lo mismo que para un éxito con problemas.

## Limitaciones

### Plataformas compatibles

En la versión preliminar pública, admitimos traducciones de una Metric View de Databricks a un modelo tabular.

### Conectividad

The public preview does not connect to any platforms besides Fabric, Power BI, and Analysis Services.
Working with models from other platforms, e.g., Databricks Metric Views, is based on local source files, such as a Metric View YAML definition.

## Apéndice sobre nomenclatura

Puede resultar confuso hablar del Semantic Bridge, ya que hay muchas palabras que tienen significados tanto genéricos como específicos, según el nivel de abstracción del que estemos hablando y la plataforma que estemos tratando.
Por ejemplo, el término "modelo semántico" es a la vez genérico, ya que se refiere al concepto de una colección de datos y lógica de negocio en una forma adecuada para dar soporte a las necesidades de informes y análisis, y también es el nombre que Microsoft ha adoptado para referirse a su implementación específica de este concepto genérico en Power BI y Fabric.
Así, un modelo semántico puede referirse de forma genérica a una Metric View de Databricks, a un cubo OLAP/multidimensional, a un modelo semántico de Power BI o a un modelo hospedado en la capa semántica de otra plataforma.
Por ello, hemos adoptado las siguientes definiciones y estándares en nuestra documentación para mantener la claridad y la coherencia.

> [!NOTE]
> Estas convenciones solo están pensadas para la documentación sobre la funcionalidad Semantic Bridge.

### Definiciones

- _modelo semántico_: cuando se usa por sí solo, siempre se refiere al concepto genérico de una colección de datos, metadatos y lógica de negocio para respaldar la elaboración de informes y el análisis.
  If and only if it is immediately preceded by "Fabric" or "Power BI", then it is referring to that artifact type in that platform, specifically a Tabular model that is saved as TMDL or BIM and using M and DAX; we tend to prefer to use the term Tabular model to refer to the Power BI / Fabric semantic model to avoid this confusion where possible, because the Tabular model is shared across Power BI / Fabric as well as Analysis Services Tabular.
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
As such, **we always refer to an object in a specific platform's model by saying the platform and the object, e.g., "Metric View measure" or "Tabular measure"; "Metric View field" or "TOM column".**
If the term is ever used without being accompanied by a platform's name, then we are discussing the idea generically.

## Recursos adicionales

- [Metric View documentation](https://learn.microsoft.com/azure/databricks/business-semantics/)
- [Metric View YAML reference](https://learn.microsoft.com/azure/databricks/business-semantics/metric-views/yaml-reference)
- @semantic-bridge-metric-view-tabular-translation
- @semantic-bridge-metric-view-object-model
- @semantic-bridge-metric-view-validation
- @semantic-bridge-metric-view-fields-and-dimensions
- @semantic-bridge-how-tos
