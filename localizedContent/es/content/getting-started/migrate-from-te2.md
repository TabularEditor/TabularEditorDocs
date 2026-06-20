---
uid: migrate-from-te2
title: Migración desde Tabular Editor 2.x
author: Daniel Otykier
updated: 2026-06-10
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

# Migración desde Tabular Editor 2.x

Este artículo está dirigido a desarrolladores que ya tienen algo de experiencia usando Tabular Editor 2.x para desarrollar un Dataset de Power BI o Analysis Services Tabular. El artículo destaca las similitudes y las principales novedades de Tabular Editor 3 para que te pongas al día rápidamente.

## Instalación en paralelo

Tabular Editor 3 tiene un código de producto diferente al de Tabular Editor 2.x. Esto significa que puedes instalar ambas herramientas en paralelo sin problemas. De hecho, las herramientas se instalan en carpetas de programa separadas y su configuración también se guarda en carpetas distintas. En otras palabras, no tiene sentido hablar de “actualizar” o “volver a una versión anterior” entre Tabular Editor 2.x y Tabular Editor 3. Es mejor pensar en Tabular Editor 3 como un producto totalmente distinto.

## Comparación de características

En cuanto a funcionalidades, Tabular Editor 3 es, en esencia, un superconjunto de Tabular Editor 2.x, con pocas excepciones. La tabla siguiente compara las principales funcionalidades de ambas herramientas:

[!include[feature-comparison](../includes/feature-comparison.partial.md)]

## Diferencias de características

A continuación se muestra un resumen de las diferencias más importantes entre las características.

### Interfaz de usuario

Lo primero que notarás al iniciar Tabular Editor 3 es la nueva interfaz, similar al shell de Visual Studio. Esta interfaz es totalmente personalizable, es compatible con pantallas de alta resolución DPI, varios monitores e incluso permite cambiar el tema. Todos los elementos de la interfaz se pueden mover a distintas ubicaciones; por lo tanto, si prefieres el diseño de la interfaz de Tabular Editor 2.x, elige inmediatamente **Diseño clásico** en el menú **Ventana**.

En general, los elementos de la interfaz que existen en Tabular Editor 2.x tienen el mismo nombre en Tabular Editor 3, así que debería ser relativamente fácil orientarte en la nueva interfaz. A continuación se enumeran algunas diferencias importantes:

- La pestaña **Scripting avanzado** de Tabular Editor 2.x ha desaparecido. En Tabular Editor 3, en su lugar, se crean **C# Scripts** desde el menú **Archivo > Nuevo**. No estás limitado a trabajar en un único script cada vez. Además, las **Acciones personalizadas** han pasado a llamarse **macros**.
- El **filtrado con Dynamic LINQ** no está disponible actualmente en el Explorador TOM. En su lugar, si quieres buscar objetos usando [Dynamic LINQ](https://dynamic-linq.net/expression-language), tienes que abrir el cuadro de diálogo **Buscar y reemplazar** pulsando CTRL+F.
- Si cierras el **Editor de expresiones**, puedes volver a abrirlo haciendo doble clic en el icono de un objeto en el **Explorador TOM**, o eligiendo la opción de menú **Ver > Editor de expresiones**.
- Al usar el diseño predeterminado en Tabular Editor 3, el **Best Practice Analyzer** estará en una pestaña junto al **Explorador TOM**. Aquí también encontrarás la nueva vista **Actualización de datos** (que te permite ver la cola de operaciones de actualización en segundo plano) y la vista **macros** (que te permite gestionar las macros guardadas previamente a partir de C# Scripts).
- Tabular Editor 3 muestra todos los errores de sintaxis y semántica de DAX en la nueva **vista de mensajes**. En el diseño predeterminado, se encuentra en la parte inferior izquierda de la interfaz.
- Además, Tabular Editor 3 incluye el **Analizador VertiPaq** (que quizá ya conozcas de [DAX Studio](https://daxstudio.org/)).
- Como nota final, Tabular Editor 3 introduce el concepto de **documentos**, que es simplemente un término genérico para C# Scripts, Scripts DAX, consultas DAX, diagramas, vistas previas de datos y Pivot Grids.

Para más información, consulta <xref:user-interface>.

### Nuevo editor de DAX y capacidades semánticas

Tabular Editor 3 incorpora su propio motor de análisis sintáctico de DAX (también conocido como el "analizador semántico"), lo que significa que la herramienta ahora entiende la semántica de cualquier código DAX de tu modelo. Por supuesto, el editor es altamente configurable, lo que te permite ajustarlo para que se adapte a tu estilo de programación de DAX. Por supuesto, el editor es altamente configurable, lo que te permite ajustarlo para que se adapte a tu estilo de programación de DAX.

Para obtener más información sobre el nuevo editor de DAX, consulta <xref:dax-editor>.

Además, el analizador semántico reporta continuamente cualquier error de sintaxis o semántica de DAX en todos los objetos de tu modelo. Esto funciona incluso sin estar conectado a Analysis Services y es rapidísimo. El analizador semántico también permite a Tabular Editor 3 inferir automáticamente los tipos de datos a partir de expresiones DAX. En otras palabras, Tabular Editor 3 detecta automáticamente qué columnas resultarían de una expresión de tabla calculada. Esto supone una gran mejora respecto a Tabular Editor 2.x, donde tenías que asignar manualmente las columnas de una tabla calculada o depender de Analysis Services para que devolviera los metadatos de las columnas.

### Importación de tablas y actualización del esquema con compatibilidad con Power Query

Otra gran ventaja de Tabular Editor 3 frente a Tabular Editor 2.x es la compatibilidad con orígenes de datos estructurados y particiones de Power Query (M). En concreto, la funcionalidad "Actualización del esquema" ahora funciona con estos tipos de Data sources y particiones, y el Asistente para importar tablas puede generar el código M necesario al importar nuevas tablas.

El propio cuadro de diálogo de comparación de esquemas también incluye varias mejoras; por ejemplo, te permite asignar fácilmente una operación de eliminación de columna + inserción de columna a una única operación de cambio de nombre de columna (y viceversa). También hay opciones para controlar cómo deben tratarse los tipos de datos de punto flotante y decimal (por ejemplo, a veces tu Data source puede estar usando un tipo de datos de punto flotante, pero quizá quieras importarlo siempre como tipo decimal).

Para obtener más información, consulta <xref:importing-tables>.

<a name="workspace-mode"></a>

### Modo del área de trabajo

Tabular Editor 3 introduce el concepto de **modo del área de trabajo**, en el que los metadatos del modelo se cargan desde el disco (Model.bim o Database.json) y, a continuación, se despliegan inmediatamente en una instancia de Analysis Services que elijas. Cada vez que pulsas Guardar (CTRL+S), la base de datos de Workspace se sincroniza y los metadatos actualizados del modelo se guardan de nuevo en disco. La ventaja de este enfoque es que Tabular Editor se conecta a Analysis Services, lo que habilita las [funciones conectadas](#connected-features) que se enumeran a continuación, y al mismo tiempo facilita la actualización de los archivos de origen en el disco. Con Tabular Editor 2.x, tenías que abrir un modelo desde una base de datos y luego acordarte de guardarlo manualmente en el disco de vez en cuando.

Este enfoque es ideal para habilitar el [desarrollo en paralelo](xref:parallel-development) y la integración de metadatos del modelo con sistemas de control de versiones.

Para obtener más información, consulta <xref:workspace-mode>.

<a name="connected-features"></a>

### Funciones conectadas

Tabular Editor 3 incluye varias funciones conectadas nuevas, lo que te permite usarlo como herramienta cliente para Analysis Services. Estas funciones se habilitan siempre que Tabular Editor 3 esté conectado a Analysis Services, ya sea directamente o al usar la característica [modo del área de trabajo](#workspace-mode).

Las nuevas funciones conectadas son:

- Vista previa de datos de tablas
- PivotGrids
- Consulta DAX
- Operaciones de actualización de datos
- Analizador VertiPaq

### Diagramas

Una función muy solicitada de Tabular Editor 2.x era poder visualizar mejor las relaciones entre tablas. Con Tabular Editor 3, ahora puedes crear diagramas del modelo. Cada diagrama es un archivo JSON sencillo que contiene los nombres y las coordenadas de las tablas que se incluirán en el diagrama. A continuación, Tabular Editor 3 renderiza las tablas y sus relaciones, y ofrece funciones para editarlas fácilmente, añadir tablas adicionales al diagrama en función de las relaciones existentes, etc.

![Añade fácilmente tablas relacionadas](~/content/assets/images/diagram-menu.png)

Consulta [Trabajar con diagramas](xref:importing-tables-data-modeling#working-with-diagrams) para obtener más información.

### C# Scripts y grabador de macros

La característica **Scripting avanzado** de Tabular Editor 2.x se ha trasladado a Tabular Editor 3 como **C# Scripts**. Una diferencia importante en Tabular Editor 3 es que ya no estás limitado a trabajar con un único script. En su lugar, con la opción **Archivo > Nuevo > C# Script**, puedes crear y trabajar con tantos C# Scripts como necesites. Al igual que en Tabular Editor 2.x, estos scripts se pueden guardar como acciones reutilizables integradas directamente en el menú contextual del Explorador TOM al hacer clic con el botón derecho. En Tabular Editor 3, llamamos a estas acciones **macros**, y hasta puedes crear tus propios menús y barras de herramientas para añadir macros.

Y, lo más importante, Tabular Editor 3 incluye un **grabador de macros** que puedes usar para generar automáticamente código C# a partir de tus interacciones.

Para obtener más información, consulta @cs-scripts-and-macros.

### Script DAX

La última característica importante que necesitas conocer, si vienes de Tabular Editor 2.x, es **Script DAX**. Con esta característica, puedes crear documentos que te permiten editar la expresión DAX y las propiedades básicas de varios objetos calculados a la vez. Los objetos calculados son medidas, columnas calculadas, tablas calculadas, etc.

Esto es muy práctico al crear una lógica de negocio compleja repartida entre varios objetos. Al (multi)seleccionar objetos en el Explorador TOM, hacer clic con el botón derecho y elegir la opción **Script DAX**, obtienes un nuevo script de DAX que contiene las definiciones de todos los objetos seleccionados. El editor de Script DAX, por supuesto, tiene las mismas capacidades de DAX que el Editor de expresiones y el editor de Consulta DAX.

Al trabajar en modo **conectado** o **Workspace**, Script DAX es una herramienta increíblemente potente para modificar y probar rápidamente la lógica de negocio actualizada; por ejemplo, cuando lo usas junto con un Pivot Grid, como se muestra en la captura de pantalla siguiente. Con solo pulsar SHIFT+F5, la base de datos se actualiza en función de las expresiones DAX del script, tras lo cual el Pivot Grid se actualiza de inmediato.

![Scripting de Dax y Pivot](~/content/assets/images/dax-scripting-and-pivot.png)

Para obtener más información, consulta @dax-script-introduction.

## Principales novedades desde 2021

Tabular Editor 3 ha incorporado muchas funcionalidades desde que se escribió este artículo por primera vez. La tabla comparativa de funciones anterior es el catálogo de referencia. Los aspectos más relevantes para los desarrolladores que vienen de Tabular Editor 2.x son:

- [funciones DAX definidas por el usuario (UDFs)](xref:udfs) con asistencia de autoría, acciones de código y espacios de nombres
- [Editor de calendario](xref:calendars) para crear tablas de fechas con inteligencia temporal avanzada
- [Administrador de paquetes DAX](xref:dax-package-manager) para instalar y compartir código DAX reutilizable
- [Acciones de código](xref:code-actions) para correcciones rápidas y refactorización en el editor de DAX
- [Depurador de DAX](xref:dax-debugger) para recorrer paso a paso la evaluación de expresiones
- [Integración con el Optimizador de DAX](xref:dax-optimizer-integration) junto con el Analizador VertiPaq
- [grupos de tablas](xref:table-groups) para organizar modelos grandes
- [Asistente de IA](xref:ai-assistant) para obtener ayuda con DAX y modelado
- Serialización de [TMDL](xref:tmdl), [Guardar en carpeta](xref:save-to-folder) y [Guardar con archivos auxiliares](xref:save-with-supporting-files) para la integración con Git de Fabric
- [CLI de Tabular Editor](xref:te-cli) multiplataforma (`te`, en versión preliminar pública limitada) para la automatización y CI/CD
- [Semantic Bridge](xref:semantic-bridge) para Databricks Metric Views (Edición Enterprise)
- [Localización](xref:references-application-language) de la interfaz de la aplicación

## Siguientes pasos

- @migrate-from-vs
- @te-cli-migrate
- @parallel-development
- @boosting-productivity-te3
