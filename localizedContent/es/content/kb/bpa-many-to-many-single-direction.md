---
uid: kb.bpa-many-to-many-single-direction
title: Las relaciones de muchos a muchos deberían ser unidireccionales
author: Morten Lønskov
updated: 2026-01-09
description: Regla de prácticas recomendadas para evitar problemas de rendimiento mediante filtrado unidireccional en relaciones de muchos a muchos.
---

# Las relaciones de muchos a muchos deberían ser unidireccionales

## Descripción general

Esta regla de prácticas recomendadas identifica relaciones de muchos a muchos que usan filtrado cruzado bidireccional. Las relaciones de muchos a muchos con filtrado en ambas direcciones provocan una degradación significativa del rendimiento.

- Categoría: Rendimiento
- Gravedad: Media (2)

## Se aplica a

- Relaciones

## Por qué es importante

- **Impacto grave en el rendimiento**: el motor debe evaluar los filtros en ambas direcciones
- **Consumo de memoria**: se mantienen contextos de filtro adicionales
- **Rutas de filtro ambiguas**: varias rutas producen resultados inesperados
- **Lógica DAX compleja**: depurar el contexto de filtro se vuelve difícil
- **Riesgo de dependencias circulares**: puede provocar bucles de evaluación infinitos

## Cuándo se activa esta regla

La regla se activa cuando una relación cumple todas estas condiciones:

1. `FromCardinality = "Many"`
2. `ToCardinality = "Many"`
3. `CrossFilteringBehavior = "BothDirections"`

## Cómo solucionarlo

### Corrección manual

1. En el **Explorador TOM**, localiza la relación marcada
2. En el panel de **Propiedades**, busca `Dirección de filtro cruzado`
3. Cambia de **Ambos** a **Único**

Elige la dirección según el flujo típico del filtro:

- De la dimensión a la tabla de hechos
- De la tabla de búsqueda a la tabla de datos

Cuando necesites filtrar en sentido contrario, manéjalo explícitamente en las medidas:

```dax
SalesWithCrossFilter = 
CALCULATE(
    SUM('Sales'[Amount]),
    CROSSFILTER('BridgeTable'[Key], 'DimensionTable'[Key], Both)
)
```

## Causas habituales

### Causa 1: Configuración predeterminada en ambas direcciones

El diseñador de modelos aplicó el filtrado bidireccional de forma predeterminada.

### Causa 2: Requisitos mal entendidos

Se creía que el filtrado en ambas direcciones era necesario para todos los escenarios.

### Causa 3: Enfoque de corrección rápida

Se usó el filtrado en ambas direcciones para resolver un problema concreto sin considerar el rendimiento.

## Ejemplo

### Antes de la corrección

```
'Sales' (Muchos) <--> (Muchos) 'ProductBridge'
Dirección de filtro cruzado: Ambos  ← Problema
```

### Después de la corrección

```
'Sales' (Muchos) --> (Muchos) 'ProductBridge'
Dirección de filtro cruzado: Único
```

Si 'Products' debe filtrar 'Sales', usa DAX:

```dax
SalesForSelectedProducts = 
VAR SelectedProducts = VALUES('Products'[ProductKey])
RETURN
CALCULATE(
    SUM('Sales'[Amount]),
    TREATAS(SelectedProducts, 'ProductBridge'[ProductKey])
)
```

## Nivel de compatibilidad

Esta regla se aplica a modelos con nivel de compatibilidad **1200** o superior.

## Reglas relacionadas

- [Los tipos de datos de la relación deben coincidir](xref:kb.bpa-relationship-same-datatype) - Garantizar la integridad de la relación

## Más información

- [Relaciones de muchos a muchos en Power BI](https://learn.microsoft.com/power-bi/transform-model/desktop-many-to-many-relationships)
- [Filtrado cruzado de relaciones](https://learn.microsoft.com/power-bi/transform-model/desktop-relationships-understand)
- [Función CROSSFILTER de DAX](https://dax.guide/crossfilter/)
- [Función TREATAS de DAX](https://dax.guide/treatas)
