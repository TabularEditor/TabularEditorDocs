---
uid: kb.bpa-calculation-groups-no-items
title: Los grupos de cálculo deben contener elementos
author: Morten Lønskov
updated: 2026-01-09
description: Regla de prácticas recomendadas que identifica grupos de cálculo sin elementos de cálculo que deben completarse o eliminarse.
---

# Los grupos de cálculo deben contener elementos

## Información general

Esta regla de prácticas recomendadas identifica grupos de cálculo que no contienen elementos de cálculo. Los grupos de cálculo vacíos no tienen ninguna utilidad y deben completarse o eliminarse.

- Categoría: Mantenimiento
- Gravedad: Media (2)

## Se aplica a

- Grupos de cálculo

## Por qué es importante

- **Errores de implementación**: Los grupos vacíos pueden no superar la validación en Power BI Service
- **Errores del modelo**: Pueden provocar comportamientos inesperados en los cálculos DAX
- **Confusión entre los desarrolladores**: Los miembros del equipo pierden tiempo investigando estructuras incompletas
- **Sobrecarga de rendimiento**: El motor procesa metadatos innecesarios

## Cuándo se activa esta regla

La regla se activa cuando un grupo de cálculo no tiene ningún elemento de cálculo:

```csharp
CalculationItems.Count == 0
```

## Cómo solucionarlo

### Opción 1: Agregar elementos de cálculo

Si el grupo de cálculo tiene un propósito empresarial válido:

1. En el **Explorador TOM**, expanda la tabla del grupo de cálculo
2. Expande la columna **grupo de cálculo**
3. Haz clic con el botón derecho y selecciona **Agregar elemento de cálculo**
4. Define la expresión del elemento de cálculo

### Opción 2: Eliminar el grupo de cálculo

Si ya no lo necesitas:

1. En el **Explorador TOM**, localiza la tabla del grupo de cálculo
2. Haz clic con el botón derecho en la tabla
3. Selecciona **Eliminar**

## Causas comunes

### Causa 1: Desarrollo incompleto

Se creó un grupo de cálculo durante la planificación, pero aún no se ha implementado.

### Causa 2: Migración desde otros modelos

Se copió la estructura del grupo de cálculo sin elementos.

### Causa 3: Refactorización

Se movieron todos los elementos de cálculo a un grupo de cálculo diferente.

## Ejemplo

### Antes de corregir

```
Grupo de cálculo: Inteligencia temporal
  Elementos: (ninguno)  ← Problema
```

### Después de corregir

```
Grupo de cálculo: Inteligencia temporal
  Elementos:
    - Período actual: SELECTEDMEASURE()
    - Acumulado del año: CALCULATE(SELECTEDMEASURE(), DATESYTD('Date'[Date]))
    - Año anterior: CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Date'[Date]))
```

## Nivel de compatibilidad

Esta regla se aplica a los modelos con nivel de compatibilidad **1200** y superior.

## Reglas relacionadas

- [Las perspectivas deben contener objetos](xref:kb.bpa-perspectives-no-objects) - Regla similar para las perspectivas vacías
- [Expresión obligatoria](xref:kb.bpa-expression-required) - Asegura que los elementos de cálculo tengan expresiones

## Más información

- [Grupos de cálculo en modelos tabulares](https://learn.microsoft.com/analysis-services/tabular-models/calculation-groups)
- [Creación de grupos de cálculo](https://www.sqlbi.com/articles/introducing-calculation-groups/)
- [Patrones para grupos de cálculo](https://www.sqlbi.com/calculation-groups/)
