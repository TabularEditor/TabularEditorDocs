---
uid: kb.bpa-powerbi-latest-compatibility
title: Usar el nivel de compatibilidad más reciente para los modelos de Power BI
author: Morten Lønskov
updated: 2026-09-23
description: Regla de buenas prácticas que garantiza que los modelos de Power BI usen el nivel de compatibilidad más reciente para obtener funciones y rendimiento óptimos.
---

# Usar el nivel de compatibilidad más reciente para los modelos de Power BI

## Resumen

This rule flags Power BI models below the highest compatibility level that your Tabular Editor 3 version supports. New model features, such as new DAX functions and TOM properties, require the newer levels.

- Categoría: Gobernanza
- Gravedad: Alta (3)

## Se aplica a

- Modelo (solo modelos semánticos de Power BI)

## Por qué es importante

- new DAX functions and model features aren't available below the level that introduces them
- a model kept at a recent level needs smaller upgrades later

## Cuándo se activa esta regla

The rule triggers for Power BI models whose compatibility level isn't the current maximum:

```csharp
Model.Database.CompatibilityMode=="PowerBI" 
and Model.Database.CompatibilityLevel<>[CurrentMaxLevel]
```

## Cómo corregirlo

### Corrección automática

The rule's automatic fix sets the compatibility level to the highest level your installed version of Tabular Editor 3 supports. To get a newer level, update Tabular Editor 3.

```csharp
Model.Database.CompatibilityLevel = [PowerBIMaxCompatibilityLevel]
```

### Solución manual

1. In the TOM Explorer, select **Model** and expand **Database** in the **Properties** view.
2. Set **Compatibility Level** to the latest level.
3. Test the DAX expressions and features of the model.
4. Deploy to the Power BI Service.

See @update-compatibility-level.

## Causas habituales

### Causa 1: Modelo creado en Power BI Desktop

Power BI Desktop doesn't always create models at the latest compatibility level.

### Causa 2: Modelo creado con un nivel de compatibilidad inferior

An older version of Power BI Desktop created the model.

### Causa 3: Enfoque conservador

A team policy delays upgrades.

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

The model can use [custom calendars](xref:calendars) (1701+), [DAX user-defined functions](xref:udfs) (1702+), [user-context calculated columns](xref:user-context-calculated-columns) (1705+) and the `StringIndexingBehavior` column property (1706+).

## Nivel de compatibilidad

Esta regla se aplica a los modelos de Power BI en todos los niveles de compatibilidad.