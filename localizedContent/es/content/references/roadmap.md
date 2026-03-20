---
uid: roadmap
title: Hoja de ruta
author: Morten Lønskov
updated: 2025-10-29
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      full: true
---

# Hoja de ruta de Tabular Editor 3

A continuación se muestra un resumen de las principales novedades que se incluirán en las actualizaciones de Tabular Editor 3 a corto y largo plazo:

# [Próximamente](#tab/upcoming)

## En desarrollo

- **Mejoras de Semantic Bridge**: compatibilidad con las propiedades de la versión 1.1 y una interfaz de importación mejorada
- **Mejoras de localización**: ampliación de la compatibilidad con idiomas y perfeccionamiento de las traducciones existentes
- **Autoformato de Power Query (M)**: capacidades de formato avanzadas para expresiones M
- **Comparación gráfica de modelos**: ver los cambios que se aplican a

## Próximamente

- Asistente de IA en Tabular Editor
- Compatibilidad con «.NET 10»
- Integración con Git
- Mejoras en la edición de Power Query (M)
- Propiedades de TOM mostradas como scripts de TMDL y TMSL
- Aplicación CLI independiente
- Macros integradas

## Futuro

- Visual de contexto de filtro del depurador de DAX
- Fragmentos de código de autocompletado de Daxscilla configurables
- Temas configurables para los editores de código (colores de resaltado de sintaxis)
- Implementación incremental (al estilo de [ALM Toolkit](http://alm-toolkit.com/))
- Mejoras en Acciones de macro, como la aplicación automática en todo el modelo y preferencias para decidir cuáles aplicar

# [Lanzado](#tab/shipped)

Para obtener información detallada sobre cada versión, consulta el [historial completo de versiones](xref:release-history).

## Lanzado en 2026

✅ [**Localización**](xref:references-application-language) - Compatibilidad con chino, español (vista previa), japonés, alemán y francés (experimental) (v3.25.0)

✅ [**Reglas integradas del Best Practice Analyzer**](xref:built-in-bpa-rules) - Conjunto completo de reglas de BPA que cubren el formato, los metadatos, el diseño del modelo, las expresiones DAX y las traducciones (v3.25.0)

✅ **Semantic Bridge** - Crea modelos semánticos a partir de Databricks Metric Views (Edición Enterprise, v3.25.0)

✅ [**Guardar con archivos auxiliares para Fabric**](xref:save-with-supporting-files) - Compatibilidad con archivos .platform y definition.pbism para ajustarse a la estructura del repositorio de Fabric (v3.25.0)

✅ **Editor de calendario**: interfaz mejorada para administrar objetos de calendario para la inteligencia temporal (v3.25.0)

✅ [**Cuadro de diálogo de actualización avanzada**](xref:advanced-refresh): configura el paralelismo, la fecha de vigencia de la actualización incremental y los [perfiles de anulación de actualización](xref:refresh-overrides) (Edición Business/Edición Enterprise, v3.25.0)

## Lanzado en 2025

✅ [**Administrador de paquetes DAX**](xref:dax-package-manager): busca e instala paquetes DAX desde daxlib.org con un solo clic (v3.24.0)

✅ **Espacios de nombres de UDF**: organización jerárquica de funciones definidas por el usuario con propiedades de espacio de nombres personalizables (v3.24.0)

✅ **Mejoras en los Cálculos Visuales**: mejor compatibilidad del editor DAX con funciones de Cálculo Visual y referencias a columnas Visuales (v3.24.0)

✅ [**Funciones DAX definidas por el usuario (UDF)**](xref:udfs): crea y administra una función DAX definida por el usuario reutilizable (v3.23.0)

✅ [**Calendarios**](xref:calendars): funciones de inteligencia temporal basadas en calendarios con una interfaz mejorada (v3.23.0)

✅ **Compatibilidad con Fabric SQL Databases y Mirrored Databases**: el asistente de importación ahora admite nuevos Data sources de Fabric en los modos Import y Direct Lake (v3.23.0)

✅ [**Direct Lake en OneLake y SQL**](xref:direct-lake-guidance): compatibilidad completa con los modos de Direct Lake, incluidos el modo mixto y los modelos híbridos (Edición Enterprise, v3.22.0)

✅ **Autocompletado por palabras**: el editor DAX ahora admite búsquedas de varias palabras en el autocompletado (v3.22.0)

✅ **Mejoras en la vista de diagrama**: iconos del tipo de datos de las columnas, indicadores de relación bidireccional y opciones mejoradas de visualización de tablas (v3.21.0)

✅ **Copiar scripts de TMDL desde el Explorador TOM**: exporta objetos individuales como TMDL al portapapeles o a un archivo (v3.21.0)

✅ **Compatibilidad con RLS en el Optimizador de DAX**: ve los resultados del Optimizador de DAX para RLS y expresiones de elementos de cálculo (v3.21.0)

✅ **Propiedad MetadataSource**: nueva propiedad del objeto Model para que los C# Scripts puedan acceder a la ubicación de los metadatos del modelo (v3.21.0)

✅ **Mejoras en el editor de C#**: experiencia de edición de código mejorada con un IntelliSense más preciso y búsqueda flexible

✅ **Compilaciones nativas ARM64**: rendimiento optimizado en procesadores ARM64 (v3.23.0)

## Lanzado en 2024

✅ Mejora de variables locales del depurador de DAX

✅ Integración completa con Direct Lake

✅ Integración del Optimizador de DAX (vista previa)

✅ Migración a .Net 8

✅ Mejora de Pivot Grid

✅ Mejora de la Consulta DAX

✅ Compatibilidad con TMDL GA

✅ Acciones de código

✅ Disponibilidad general de la integración con el Optimizador de DAX

✅ Mejoras en la vista de actualización de datos

✅ Resaltado de Power Query (M)

## Lanzado en 2023

✅ Compatibilidad con TMDL como formato de archivo estándar de Guardar en carpeta. (Dependiendo del lanzamiento de TMDL por parte de Microsoft)

✅ Compatibilidad del Asistente para importar tablas con Databricks (a la espera de que esté disponible el punto de conexión REST para obtener metadatos/esquema)

✅ Editor de traducción de metadatos (vista que se puede abrir al seleccionar una o varias configuraciones regionales, similar a la herramienta Tabular Translator)

✅ Editor de perspectivas (vista que se puede abrir al seleccionar una o varias perspectivas, lo que le permite marcar o desmarcar los objetos visibles en esas perspectivas)

✅ Compatibilidad mejorada con bases de datos Oracle

✅ Compatibilidad del Asistente para importar tablas con datamarts de Power BI (Use el punto de conexión SQL del datamart)

## Lanzado en 2022

✅ Depurador de DAX

✅ Migración a .NET 6

✅ Code Assist para C# (autocompletar, información de parámetros, etc.)

✅ Compatibilidad del Asistente para importar tablas con Snowflake

✅  Compatibilidad del Asistente para importar tablas con Dataflow de Power BI

✅ Atajos de teclado configurables

✅ Compatibilidad con funciones de ventana de DAX

✅ Integración con Git (vista previa privada)

## Lanzado en 2021

✅ Asistente para importar tablas

✅  Versión portátil

✅  Pivot Grid, Vista previa de tabla y suplantación en la Consulta DAX de un rol o usuario específicos, lo que facilita probar RLS/OLS

✅  Compatibilidad con Script DAX para grupos de cálculo y elementos de cálculo

✅  Formato DAX sin conexión

***

# Hoja de ruta de Tabular Editor 2

> [!NOTE]
> Tabular Editor 2 ya no está en desarrollo activo y no recibirá de nuestra parte nuevas funciones importantes ni mejoras. Sin embargo, nos comprometemos a mantenerlo actualizado, garantizando la compatibilidad con las nuevas funcionalidades de los modelos semánticos a medida que Microsoft las publique, y también a corregir cualquier incidencia crítica o bloqueante. Como el proyecto es de código abierto bajo la licencia MIT, cualquiera puede enviar pull requests, que nuestro equipo revisará y aprobará.