---
uid: kb.bpa-powerbi-latest-compatibility
title: Usar el nivel de compatibilidad más reciente para los modelos de Power BI
author: Morten Lønskov
updated: 2026-01-09
description: Regla de buenas prácticas que garantiza que los modelos de Power BI usen el nivel de compatibilidad más reciente para obtener funciones y rendimiento óptimos.
---

# Usar el nivel de compatibilidad más reciente para los modelos de Power BI

## Resumen

Esta regla identifica los modelos de Power BI que no están usando el nivel de compatibilidad más reciente disponible. Usar el nivel más reciente garantiza el acceso a las funciones más nuevas, optimizaciones de rendimiento y correcciones de errores.

- Categoría: Gobernanza
- Gravedad: Alta (3)

## Se aplica a

- Modelo (solo modelos semánticos de Power BI)

## Por qué es importante

- **Funciones ausentes**: nuevas funciones de DAX y capacidades del modelo no disponibles
- **Compatibilidad futura**: actualizaciones más sencillas al usar niveles recientes

## Cuándo se activa esta regla

En los modelos de Power BI, se activa cuando el nivel de compatibilidad está por debajo del máximo actual:

```csharp
Model.Database.CompatibilityMode=="PowerBI" 
and Model.Database.CompatibilityLevel<>[CurrentMaxLevel]
```

## Cómo corregirlo

### Corrección automática

La regla de prácticas recomendadas incluye una corrección automática que establece el nivel de compatibilidad en el nivel más alto disponible en la instalación actual de Tabular Editor 3. Si tienes instalada una versión antigua de Tabular Editor 3, deberías actualizarla.

```csharp
Model.Database.CompatibilityLevel = [PowerBIMaxCompatibilityLevel]
```

### Corrección manual

1. En Tabular Editor, ve a las propiedades de **Model**
2. Establece el **nivel de compatibilidad** en el nivel más reciente disponible
3. Prueba todas las expresiones y funcionalidades de DAX
4. Implementa en el servicio Power BI

## Causas habituales

### Causa 1: Modelo creado en Power BI Desktop

Un modelo creado en Power BI Desktop no necesariamente tiene el nivel de compatibilidad más reciente.

### Causa 2: Modelo creado con un nivel de compatibilidad inferior

Modelo creado con una versión anterior de Power BI Desktop.

### Causa 3: Enfoque conservador

Política del equipo: retrasar las actualizaciones.

## Ejemplo

### Antes de la corrección

```
Nivel de compatibilidad del modelo: 1500
Nivel máximo actual: 1700
```

### Después de la corrección

```
Nivel de compatibilidad del modelo: 1700 (la más reciente)
```

Acceso a nuevas funcionalidades, como grupos de cálculo mejorados y parámetros de campo.

## Nivel de compatibilidad

Esta regla se aplica a los modelos de Power BI en todos los niveles de compatibilidad.