---
uid: kb.bpa-perspectives-no-objects
title: Las perspectivas deben contener objetos
author: Morten Lønskov
updated: 2026-01-09
description: Regla de buenas prácticas para eliminar perspectivas vacías que no contienen ningún objeto visible.
---

# Las perspectivas deben contener objetos

## Descripción general

Esta regla de buenas prácticas identifica las perspectivas que no contienen ninguna tabla visible. Las perspectivas vacías no tienen ninguna utilidad y se deben eliminar.

- Categoría: Mantenimiento
- Gravedad: Baja (1)

## Se aplica a

- Perspectivas

## Por qué es importante

- **Confusión de los usuarios**: las perspectivas vacías aparecen en las herramientas cliente, pero no muestran datos

## Cuándo se activa esta regla

La regla se activa cuando una perspectiva no tiene tablas visibles:

```csharp
Model.Tables.Any(InPerspective[current.Name]) == false
```

## Cómo corregirlo

### Corrección automática

Esta regla incluye una corrección automática que elimina la perspectiva vacía:

```csharp
Delete()
```

Para aplicarlo:

1. Ejecuta el **Best Practice Analyzer**
2. Selecciona las perspectivas vacías
3. Haz clic en **Aplicar corrección**

### Corrección manual

1. En el **Explorador TOM**, expande el nodo **Perspectivas**
2. Haz clic con el botón derecho en la perspectiva vacía
3. Selecciona **Eliminar**

## Causas comunes

### Causa 1: Se eliminaron todas las tablas

Se quitaron todas las tablas de la perspectiva sin eliminarla.

### Causa 2: Configuración incompleta

La perspectiva se creó durante el diseño, pero nunca se llegó a rellenar.

## Ejemplo

### Antes de la corrección

```
Perspectivas:
  - Ventas (contiene: tablas de Ventas, Cliente y Producto) ✓
  - Marketing (no contiene tablas) ✗
```

### Después de la corrección

```
Perspectivas:
  - Ventas (contiene: tablas de Ventas, Cliente y Producto) ✓
```

## Nivel de compatibilidad

Esta regla se aplica a modelos con nivel de compatibilidad **1200** y superior.

## Más información

- [Perspectivas en modelos tabulares](https://learn.microsoft.com/analysis-services/tabular-models/perspectives-ssas-tabular)

