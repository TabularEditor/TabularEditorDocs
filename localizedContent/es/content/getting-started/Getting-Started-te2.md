---
uid: getting-started-te2
title: Primeros pasos con Tabular Editor 2
author: Morten Lønskov
updated: 2026-11-19
description: "Instala Tabular Editor 2, el editor gratuito de código abierto para modelos semánticos de Analysis Services y Power BI, y luego abre, edita e implementa un modelo. Tabular Editor 3 es la versión comercial, con una prueba gratuita de 30 días."
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      none: true
---
# Primeros pasos con Tabular Editor 2

Tabular Editor 2 es una aplicación gratuita de código abierto para Windows destinada a editar modelos semánticos de Analysis Services y Power BI. Esta página trata sobre la instalación, la apertura y la edición de un modelo, la implementación, la línea de comandos y C# Script.

[!include[te2-te3-note](../includes/te2-te3-note.partial.md)]

## Herramientas por tarea

Tabular Editor 2, Tabular Editor 3 y [Tabular Editor CLI](xref:te-cli) cubren diferentes tareas:

| Tarea | Herramienta | Documentación |
|------|------|---------------|
| Editar metadatos del modelo en una aplicación de escritorio gratuita | Tabular Editor 2 | Esta página |
| Escribir DAX con autocompletado y revisarlo paso a paso en un depurador | Tabular Editor 3 | @dax-debugger |
| Ejecutar consultas DAX y obtener una vista previa de los datos de la tabla | Tabular Editor 3 | @refresh-preview-query |
| Implementar desde un proceso de CI/CD | Tabular Editor 2 o la interfaz de línea de comandos (CLI) de Tabular Editor | @command-line-options, @te-cli-cicd |
| Ejecutar comprobaciones de Best Practice Analyzer | Las tres | @best-practice-analyzer |
| Permitir que un agente de IA lea, consulte y modifique el modelo abierto en una aplicación de escritorio | Tabular Editor 3 | @mcp-server |
| Permitir que un agente de IA cambie archivos de modelos o modelos implementados desde un terminal | Tabular Editor CLI | @te-cli-skill |

## Instalación

Descarga el instalador .msi o el archivo .zip portátil desde la [página de versiones](https://github.com/TabularEditor/TabularEditor/releases/latest). Ejecute el archivo .msi o extraiga el archivo .zip en una carpeta y ejecute `TabularEditor.exe`.

El archivo .msi registra Tabular Editor 2 como [herramienta externa](xref:desktop-integration) en Power BI Desktop.

## Requisitos previos

Tabular Editor 2 requiere [.NET Framework 4.8](https://dotnet.microsoft.com/download/dotnet-framework/net48). El instalador .msi se detiene si falta .NET Framework 4.8 y proporciona un enlace para descargarlo.

> [!NOTE]
> Tabular Editor 2 utiliza el [Tabular Object Model](https://learn.microsoft.com/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo) (TOM) para cargar y guardar metadatos en archivos Model.bim o bases de datos existentes y desde ellos. El instalador incluye las [bibliotecas cliente de Analysis Services](https://learn.microsoft.com/analysis-services/client-libraries).

## Requisitos del sistema

- **Sistema operativo:** Versión de Windows compatible con .NET Framework 4.8
- **.NET Framework:** [4.8](https://dotnet.microsoft.com/download/dotnet-framework/net48)

## Abrir un modelo

Abra un modelo desde el disco con **Archivo > Abrir > Desde archivo...** (**Ctrl+O**). Los formatos compatibles son los archivos Model.bim, las carpetas guardadas con [Guardar en carpeta](xref:save-to-folder) (database.json), las carpetas [TMDL](xref:tmdl), los archivos .pbit y los proyectos .pbip.

Abra una base de datos implementada con **Archivo > Abrir > Desde BD...** (**Ctrl+Mayús+O**). El cuadro de diálogo **Conectar a Tabular Server** solicita un nombre de servidor y una autenticación:

![Conexión a un modelo tabular ya implementado](~/content/assets/images/getting-started-te-01.png)

El nombre del servidor admite instancias de Analysis Services y servidores de Azure Analysis Services (`asazure://<servername>`). El menú desplegable **Instancia local** muestra las instancias en ejecución de Power BI Desktop, los espacios de trabajo integrados de Visual Studio y Analysis Services local. A partir de la actualización de junio de 2025 de Power BI Desktop, las herramientas externas pueden cambiar cualquier parte de un modelo alojado en Power BI Desktop. Consulte @desktop-integration.

Seleccione **Aceptar** y, a continuación, seleccione una base de datos de la lista del servidor.

## Editar el modelo

La ventana principal tiene este aspecto después de cargar un modelo:

![La interfaz de usuario principal de Tabular Editor](~/content/assets/images/getting-started-te-02.png)

El árbol de la izquierda muestra todas las tablas del modelo. Expanda una tabla para ver sus columnas, medidas y jerarquías, agrupadas por carpeta de visualización. Los botones situados encima del árbol activan o desactivan las carpetas de visualización, los objetos ocultos y los tipos de objetos, y el cuadro de texto filtra los objetos por nombre. Haga clic con el botón derecho en el árbol para realizar acciones comunes, como añadir medidas, ocultar, duplicar y eliminar objetos. Pulse **F2** para cambiar el nombre del objeto seleccionado. Cuando selecciona varios objetos, **F2** abre **Cambio de nombre por lotes**:

![El cambio de nombre por lotes le permite cambiar el nombre de varios objetos simultáneamente](~/content/assets/images/getting-started-te-03.png)

El **Editor de expresiones** situado en la parte superior derecha edita la expresión DAX de la medida seleccionada o de la columna calculada. **Formatear DAX** formatea la expresión mediante [DAX Formatter](https://www.daxformatter.com).

La cuadrícula de propiedades situada en la parte inferior derecha muestra y establece las propiedades de los objetos, como `FormatString`, `Description`, las traducciones y la pertenencia a perspectivas. Para cambiar `DisplayFolder` en varios objetos a la vez, selecciónelos con **Ctrl** o **Mayús** y arrástrelos a una carpeta del árbol.

Para editar perspectivas o traducciones, seleccione el objeto **Modelo** en el árbol y seleccione el botón de puntos suspensivos junto a la propiedad `Perspectives` o `Cultures`. Se abrirá un editor de colecciones para añadir, eliminar y editar elementos:

![Editar perspectivas: haga clic en el botón de puntos suspensivos de la derecha](~/content/assets/images/getting-started-te-04.png)

Pulse **Ctrl+S** para guardar. Un modelo abierto desde un archivo se guarda de nuevo en ese archivo, y un modelo abierto desde una base de datos se guarda de nuevo en la base de datos. Si alguien ha modificado la base de datos implementada después de que usted la haya cargado, un mensaje de **Conflicto de cambios** le preguntará si desea sobrescribirla. Pulse **Ctrl+Z** para deshacer y **Ctrl+Y** para rehacer.

## Implementación

**Modelo > Implementar...** abre el asistente de implementación, que implementa el modelo cargado en un servidor. Después de seleccionar un servidor y una base de datos, elige qué partes del modelo quieres implementar:

![Asistente de implementación](~/content/assets/images/getting-started-te-05.png)

| Opción | Cuando está desmarcada |
|--------|--------------|
| **Implementar orígenes de datos** | Los orígenes de datos de la base de datos de destino permanecen como están. La implementación falla si una tabla utiliza un origen de datos que no existe en el destino. |
| **Implementar particiones de tabla** | Las particiones de la base de datos de destino permanecen como están, al igual que sus datos. |
| **Implementar particiones regidas por directivas de actualización incremental** | Las particiones creadas por la actualización incremental permanecen tal como están. Requiere **Implementar particiones de tabla**. |
| **Implementar expresiones compartidas** | Las expresiones compartidas en el destino permanecen como están. Requiere el nivel de compatibilidad 1400 o superior. |
| **Implementar roles** | Los roles del destino permanecen como están. |
| **Implementar miembros de roles** | Los miembros de roles en el destino permanecen como están. Requiere **Implementar roles**. |

**Implementar estructura del modelo** siempre está seleccionada cuando el destino es una base de datos existente. Las otras opciones se seleccionan de forma predeterminada cuando el modelo contiene ese tipo de objeto, y **Implementar roles** cuando el modelo contiene miembros de roles. Si la base de datos aún no existe, el asistente implementa los orígenes de datos, las particiones y las expresiones compartidas con el modelo, y solo se aplican las opciones de rol. La página de resumen también dispone de **Exportar compilación...** para escribir archivos de implementación para el Asistente de implementación de Analysis Services y **Script TMSL** para mostrar la implementación como un script TMSL.

## Línea de comandos

`TabularEditor.exe` ejecuta implementaciones, scripts y comprobaciones de Best Practice Analyzer desde la línea de comandos. Los siguientes ejemplos implementan un modelo:

`TabularEditor.exe c:\Projects\Model.bim`

Abre Tabular Editor 2 y carga el archivo Model.bim sin implementar nada.

`TabularEditor.exe c:\Projects\Model.bim -deploy localhost AdventureWorks`

Crea la base de datos AdventureWorks en la instancia de Analysis Services del host local, sin abrir la interfaz de usuario. Si la base de datos ya existe, la implementación falla.

`TabularEditor.exe c:\Projects\Model.bim -deploy localhost AdventureWorks -O -P -R -M`

Sobrescribe la base de datos AdventureWorks existente, incluidas sus particiones, roles y miembros de roles.

Añada estos modificadores después del nombre de la base de datos para controlar lo que sobrescribe la implementación:

- `-O` sobrescribir una base de datos existente
- `-C` sobrescribir orígenes de datos (**c**onexiones)
- `-P` sobrescribir **p**articiones
- `-Y` omitir particiones con políticas de actualización incremental (con `-P`)
- `-S` sobrescribir expresiones **c**ompartidas
- `-R` sobrescribir **r**oles
- `-M` sobrescribir **m**iembros de roles (con `-R`)

Sin estos modificadores, los orígenes de datos, las particiones, las expresiones compartidas y los roles del destino permanecen como están. @command-line-options enumera todos los modificadores, incluidos los scripts, las comprobaciones de Best Practice Analyzer y la salida para Azure DevOps y GitHub Actions.

> [!NOTE]
> `TabularEditor.exe` es una aplicación de Windows Forms, por lo que una llamada desde la línea de comandos devuelve un resultado antes de que finalice la implementación. En un trabajo por lotes que espera a la implementación, use `start /wait`:
>
> `start /wait TabularEditor.exe c:\Projects\Model.bim -deploy localhost AdventureWorks`

La [CLI de Tabular Editor](xref:te-cli) funciona con Windows, macOS y Linux y acepta la mayoría de los modificadores de `TabularEditor.exe`. Consulta @te-cli-migrate.

## C# Script

La pestaña **C# Script** ejecuta código C# contra el modelo cargado. Úsala para aplicar el mismo cambio a muchos objetos a la vez. Los scripts tienen acceso a dos objetos:

- `Selected` contiene los objetos seleccionados en el árbol.
- `Model` contiene todo el Tabular Object Model.

El editor de scripts dispone de IntelliSense básico:

![IntelliSense te ayuda a crear scripts para Tabular Editor](~/content/assets/images/getting-started-te-06.png)

Tabular Editor 2 denomina a esta función «Scripting avanzado». Consulte @advanced-scripting para ver la API de scripting y ejemplos.

## Comparación de funciones

La tabla compara Tabular Editor 2, Tabular Editor 3 y Tabular Editor CLI:

[!include[feature-comparison](../includes/feature-comparison.partial.md)]

## Próximos pasos

- @migrate-from-te2 describe las diferencias de funciones entre Tabular Editor 2 y Tabular Editor 3.
- @getting-started explica cómo instalar Tabular Editor 3 e iniciar el período de prueba gratuito.
- @te-cli-skill instala una habilidad que enseña a los agentes de codificación de IA los comandos de Tabular Editor CLI.
