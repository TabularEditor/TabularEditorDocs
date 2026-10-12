---
uid: kb.bpa-powerbi-latest-compatibility
title: Usar el nivel de compatibilidad más reciente para los modelos de Power BI
author: Morten Lønskov
updated: 2026-09-23
description: Regla de buenas prácticas que garantiza que los modelos de Power BI usen el nivel de compatibilidad más reciente para obtener funciones y rendimiento óptimos.
---

# Usar el nivel de compatibilidad más reciente para los modelos de Power BI

## Resumen

Esta regla señala los modelos de Power BI que están por debajo del nivel de compatibilidad más alto que admite tu versión de Tabular Editor 3. Las nuevas características del modelo, como las nuevas funciones de DAX y las propiedades TOM, requieren niveles más recientes.

- Categoría: Gobernanza
- Gravedad: Alta (3)

## Se aplica a

- Modelo (solo modelos semánticos de Power BI)

## Por qué es importante

- las nuevas funciones DAX y las características del modelo no están disponibles por debajo del nivel que las incorpora
- un modelo que se mantiene en un nivel reciente necesita actualizaciones menores más adelante

## Cuándo se activa esta regla

La regla se activa para los modelos de Power BI cuyo nivel de compatibilidad no es el máximo actual:

```csharp
Model.Database.CompatibilityMode=="PowerBI" 
and Model.Database.CompatibilityLevel<>[CurrentMaxLevel]
```

## Cómo corregirlo

### Corrección automática

La corrección automática de la regla establece el nivel de compatibilidad en el nivel más alto que admite tu versión instalada de Tabular Editor 3. Para obtener un nivel más reciente, actualiza Tabular Editor 3.

```csharp
Model.Database.CompatibilityLevel = [PowerBIMaxCompatibilityLevel]
```

### Solución manual

1. En el Explorador TOM, selecciona **Modelo** y expande **Base de datos** en la vista **Propiedades**.
2. Establece el **nivel de compatibilidad** en el nivel más reciente disponible.
3. Prueba las expresiones DAX y las características del modelo.
4. Implementa en el servicio de Power BI.

Consulta @update-compatibility-level.

## Causas habituales

### Causa 1: Modelo creado en Power BI Desktop

Power BI Desktop no siempre crea modelos con el nivel de compatibilidad más reciente.

### Causa 2: Modelo creado con un nivel de compatibilidad inferior

Una versión anterior de Power BI Desktop creó el modelo.

### Causa 3: Enfoque conservador

La política del equipo retrasa las actualizaciones.

## Ejemplo

### Antes de la corrección

```text
Model Compatibility Level: 1500
Current Maximum Level: 1706
```

### Después de la corrección

```text
Model Compatibility Level: 1706 (Latest)
```

El modelo puede usar [calendarios personalizados](xref:calendars) (1701+), [funciones definidas por el usuario en DAX](xref:udfs) (1702+), [columnas calculadas con contexto de usuario](xref:user-context-calculated-columns) (1705+) y la propiedad de columna `StringIndexingBehavior` (1706+).

## Nivel de compatibilidad

Esta regla se aplica a los modelos de Power BI en todos los niveles de compatibilidad.