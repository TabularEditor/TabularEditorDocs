---
uid: index
title: Tabular Editor
author: Daniel Otykier
updated: 2021-09-09
---

# Tabular Editor

Tabular Editor es una herramienta que te permite manipular y administrar fácilmente medidas, columnas calculadas, carpetas de visualización, perspectivas y traducciones en modelos semánticos tabulares de Analysis Services y Power BI.

La herramienta está disponible en dos versiones diferentes:

- Tabular Editor 2.x (gratuito, [licencia MIT](https://github.com/TabularEditor/TabularEditor/blob/master/LICENSE)) - [Página del proyecto en GitHub](https://github.com/TabularEditor/TabularEditor)
- Tabular Editor 3 (comercial) - [Página principal](https://tabulareditor.com)

## Documentación

Este sitio contiene la documentación de ambas versiones. Selecciona tu versión en la barra de navegación en la parte superior de la pantalla para ver la documentación específica del producto.

## Cómo elegir entre TE3 y TE2

Tabular Editor 3 es la evolución de Tabular Editor 2. Se ha diseñado para quienes buscan una solución de «una sola herramienta para todo» para el modelado y el desarrollo del Data model de datos tabulares.

### [Tabular Editor 3](#tab/TE3)

Tabular Editor 3 es una aplicación más avanzada que ofrece una experiencia de primer nivel, con muchas funciones prácticas para cubrir todas tus necesidades de Data model y desarrollo de datos en una sola herramienta.

![Tabular Editor 3](assets/images/te3.png)

**Características principales de Tabular Editor 3:**

- Una interfaz de usuario muy personalizable e intuitiva
- Compatibilidad con pantallas High-DPI, varios monitores y temas (sí, ¡hay modo oscuro!)
- [Editor de DAX](xref:dax-editor) de primer nivel, con resaltado de sintaxis, comprobación semántica, autocompletado, reconocimiento de contexto y mucho, mucho más
- Explorador de tablas, explorador de Pivot Grid y editor de consultas DAX
- [Asistente para importar tablas](xref:importing-tables) con compatibilidad con orígenes de datos de Power Query
- [Vista de actualización de datos](xref:data-refresh-view) junto con el [cuadro de diálogo de actualización avanzada](xref:advanced-refresh) para poner en cola y ejecutar operaciones de actualización en segundo plano
- Editor de diagramas para visualizar y editar fácilmente las relaciones entre tablas
- Funcionalidad de [Script DAX](xref:dax-scripts) para editar expresiones DAX de varios objetos en un solo documento
- [funciones DAX definidas por el usuario (UDFs)](xref:udfs) con asistencia, acciones de código y espacios de nombres
- [Editor de calendario](xref:calendars) para crear y administrar tablas de fechas con inteligencia temporal avanzada
- [Administrador de paquetes DAX](xref:dax-package-manager) para instalar y administrar paquetes DAX
- [Reglas integradas de Best Practice Analyzer](xref:built-in-bpa-rules)
- Integración del Analizador VertiPaq con el [Optimizador de DAX](xref:dax-optimizer-integration)
- [Depurador DAX](xref:dax-debugger)
- [Acciones de código](xref:code-actions) para soluciones rápidas y refactorización
- [Editor de traducción de metadatos](xref:metadata-translation-editor) y [Editor de perspectiva](xref:perspective-editor)
- [Guardar con archivos auxiliares](xref:save-with-supporting-files) para la integración de Fabric con Git
- [Soporte de localización](xref:references-application-language) (chino, español, japonés, alemán, francés)

### [Tabular Editor 2.x](#tab/TE2)

Tabular Editor 2.x es una aplicación liviana que permite modificar rápidamente el TOM (Tabular Object Model) de un modelo de datos de Analysis Services o Power BI. La herramienta se publicó originalmente en 2016 y recibe actualizaciones y correcciones de errores de forma periódica.

![Tabular Editor 2.x](assets/images/te2.png)

**Principales características de Tabular Editor 2.x:**

- Aplicación muy ligera con una interfaz sencilla e intuitiva para navegar por el TOM
- Vista de dependencias de DAX, además de atajos de teclado para navegar entre objetos DAX
- Soporte para editar las perspectivas del modelo y las traducciones de metadatos
- Cambio de nombre en lote
- Cuadro de búsqueda para moverse rápidamente por modelos grandes y complejos
- Asistente para la implementación
- Analizador de prácticas recomendadas
- Scripting avanzado mediante scripts de estilo C# para automatizar tareas repetitivas
- Interfaz de línea de comandos (puede usarse para integrar Tabular Editor con canalizaciones de DevOps)

***

### Descripción general de las características

En la tabla siguiente se muestran las principales características de ambas herramientas.

|                                                                                                                                                                                                        | TE2 (Gratuito)                       | TE3 (De pago)                          |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------- | --------------------------------------------------------- |
| Editar todos los objetos y propiedades de TOM                                                                                                                                                          | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| Edición y cambio de nombre en lote                                                                                                                                                                     | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| Compatibilidad con copiar y pegar y arrastrar y soltar                                                                                                                                                 | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| Deshacer/rehacer operaciones de modelado del Data model                                                                                                                                                | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| Cargar/guardar los metadatos del modelo en el disco                                                                                                                                                    | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>\* |
| Guardar en una carpeta                                                                                                                                                                                 | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>\* |
| Integración con [daxformatter.com](https://daxformatter.com)                                                                                                                           | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| Modelado avanzado del Data model (OLS, perspectivas, grupos de cálculo, traducciones de metadatos, etc.)                                                            | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>\* |
| Resaltado de sintaxis y corrección automática de fórmulas                                                                                                                                              | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| Ver dependencias de DAX entre objetos                                                                                                                                                                  | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| Asistente para importar tablas                                                                                                                                                                         | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| Asistente de implementación                                                                                                                                                                            | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>\* |
| Best Practice Analyzer                                                                                                                                                                                 | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| C# Script y automatización                                                                                                                                                                             | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| Usar como herramienta externa para Power BI Desktop                                                                                                                                                    | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| Conéctate a SSAS, Azure AS o Power BI Premium                                                                                                                                                          | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>\* |
| Interfaz de línea de comandos                                                                                                                                                                          | <span class="emoji">&#10004;</span> |                                                           |
| Interfaz de usuario premium y personalizable, con compatibilidad con pantallas de alta densidad DPI, varios monitores y temas                                                                          |                                                         | <span class="emoji">&#10004;</span>   |
| Editor de DAX de primer nivel con funciones similares a IntelliSense<sup>TM</sup>, formato sin conexión y mucho más                                                                                    |                                                         | <span class="emoji">&#10004;</span>   |
| Comprobación sin conexión de la sintaxis de DAX e inferencia de tipos de columna y datos                                                                                                               |                                                         | <span class="emoji">&#10004;</span>   |
| Asistente para importar tablas mejorado y comprobación de actualización del esquema de tablas, con compatibilidad con Power Query                                                                      |                                                         | <span class="emoji">&#10004;</span>   |
| Consulta DAX, Vista previa de tabla y Pivot Grid                                                                                                                                                       |                                                         | <span class="emoji">&#10004;</span>   |
| Crear diagrama para visualizar y editar relaciones entre tablas                                                                                                                                        |                                                         | <span class="emoji">&#10004;</span>   |
| Ejecuta operaciones de actualización de datos en segundo plano                                                                                                                                         |                                                         | <span class="emoji">&#10004;</span>\* |
| Grabador de macros de C#                                                                                                                                                                               |                                                         | <span class="emoji">&#10004;</span>   |
| Edita varias expresiones DAX en un solo documento mediante [Script DAX](xref:dax-scripts)                                                                                                              |                                                         | <span class="emoji">&#10004;</span>   |
| Integración de [Analizador VertiPaq](https://www.sqlbi.com/tools/vertipaq-analyzer/)                                                                                                                   |                                                         | <span class="emoji">&#10004;</span>   |
| [Depurador de DAX](xref:dax-debugger)                                                                                                                                                                  |                                                         | <span class="emoji">&#10004;</span>   |
| [Editor de traducción de metadatos](xref:metadata-translation-editor)                                                                                                                                  |                                                         | <span class="emoji">&#10004;</span>   |
| [Editor de perspectiva](xref:perspective-editor)                                                                                                                                                       |                                                         | <span class="emoji">&#10004;</span>   |
| [Grupos de tablas](xref:table-groups)                                                                                                                                                                  |                                                         | <span class="emoji">&#10004;</span>   |
| [Integración con el Optimizador de DAX](xref:dax-optimizer-integration)                                                                                                                                |                                                         | <span class="emoji">&#10004;</span>   |
| [Acciones de código](xref:code-actions)                                                                                                                                                                |                                                         | <span class="emoji">&#10004;</span>   |
| Asistencia, acciones de código y espacios de nombres para las [funciones DAX definidas por el usuario (UDFs)](xref:udfs)                                                            |                                                         | <span class="emoji">&#10004;</span>   |
| [Editor de calendario](xref:calendars) para una mejor inteligencia temporal                                                                                                                            |                                                         | <span class="emoji">&#10004;</span>   |
| [Administrador de paquetes DAX](xref:dax-package-manager)                                                                                                                                              |                                                         | <span class="emoji">&#10004;</span>   |
| [Reglas integradas de Best Practice Analyzer](xref:built-in-bpa-rules)                                                                                                                                 |                                                         | <span class="emoji">&#10004;</span>   |
| [Cuadro de diálogo de actualización avanzada](xref:advanced-refresh) con [perfiles de sobrescritura de actualización](xref:refresh-overrides) (Edición Business/Edición Enterprise) |                                                         | <span class="emoji">&#10004;</span>\* |
| [Guardar con archivos complementarios para Fabric](xref:save-with-supporting-files)                                                                                                                    |                                                         | <span class="emoji">&#10004;</span>   |
| Puente semántico para Metric Views de Databricks (Edición Enterprise)                                                                                                               |                                                         | <span class="emoji">&#10004;</span>\* |
| [Soporte de localización](xref:references-application-language) (chino, español, japonés, alemán, francés)                                                                          |                                                         | <span class="emoji">&#10004;</span>   |

\***Nota:** Se aplican limitaciones en función de la [edición](xref:editions) de Tabular Editor 3 que estés usando.

### Características comunes

Ambas herramientas ofrecen las mismas características en cuanto a las opciones de modelado de datos disponibles, ya que, básicamente, exponen todos los objetos y propiedades del [Tabular Object Model](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) mediante una interfaz de usuario intuitiva y ágil. Puedes editar propiedades avanzadas de los objetos que no están disponibles en las herramientas estándar. Las herramientas pueden cargar los metadatos del modelo desde archivos o desde cualquier instancia de Analysis Services. Los cambios solo se sincronizan cuando pulsas Ctrl+S (guardar), lo que ofrece una experiencia de edición "sin conexión" que la mayoría considera superior al modo "siempre sincronizado" de las herramientas estándar. Esto se nota especialmente al trabajar con Data model grandes y complejos.

Además, ambas herramientas permiten hacer varios cambios en los metadatos del modelo en lote, cambiar el nombre de objetos en lote, copiar y pegar objetos, arrastrar y soltar objetos entre tablas y carpetas de visualización, etc. Las herramientas incluso incluyen compatibilidad con deshacer/rehacer.

Ambas herramientas incluyen el Best Practice Analyzer, que analiza continuamente los metadatos del modelo según reglas que tú mismo puedes definir; por ejemplo, para aplicar determinadas convenciones de nomenclatura, asegurarte de que las columnas de atributo que no sean de dimensión estén siempre ocultas, etc.

También puedes escribir y ejecutar scripts de estilo C# en ambas herramientas para automatizar tareas repetitivas, como generar medidas de inteligencia de tiempo y detectar automáticamente relaciones en función de los nombres de las columnas.

Por último, gracias a la funcionalidad "Save-to-folder", un nuevo formato de archivo en el que cada objeto del modelo se guarda como un archivo individual, se facilita el desarrollo en paralelo y la integración con el control de versiones, algo que no es fácil de conseguir usando solo las herramientas estándar.

## Conclusión

Si eres nuevo en el modelado tabular en general, te recomendamos que uses las herramientas estándar hasta que te familiarices con conceptos como tablas calculadas, medidas, relaciones, DAX, etc. En ese punto, prueba Tabular Editor 2.x y comprueba lo mucho más rápido que te permite realizar determinadas tareas. ¡Si te gusta y quieres más, considera Tabular Editor 3.x!

## Siguientes pasos

- [Primeros pasos con Tabular Editor 2](xref:getting-started-te2)
- [Primeros pasos con Tabular Editor 3](xref:getting-started)
- [Plan de ruta de Tabular Editor 3](xref:roadmap)

