---
uid: kb.bpa-set-isavailableinmdx-true-necessary
title: Establecer IsAvailableInMDX en True cuando sea necesario
author: Morten Lønskov
updated: 2026-01-09
description: Regla de práctica recomendada que evita errores de consulta al garantizar que las columnas usadas en jerarquías y relaciones tengan habilitada la disponibilidad de MDX.
---

# Establecer IsAvailableInMDX en True cuando sea necesario

## Descripción general

Esta regla de práctica recomendada identifica columnas que tienen `IsAvailableInMDX` establecido en `false`, pero que en realidad se usan en escenarios que requieren acceso a MDX. Estas columnas deben tener habilitada la disponibilidad de MDX para funcionar correctamente en jerarquías, relaciones y operaciones de ordenación.

- Categoría: Prevención de errores
- Gravedad: Alta (3)

## Se aplica a

- Columnas de datos
- Columnas calculadas
- Columnas de tablas calculadas

## Por qué es importante

Cuando una columna se usa en determinadas estructuras del modelo, el motor de Analysis Services requiere acceso MDX a esa columna. Deshabilitar el acceso MDX para columnas que lo necesitan provoca:

- **Fallos de consulta**: Las jerarquías y las operaciones de ordenación fallan con errores
- **Visualizaciones con errores**: Los gráficos y las tablas que usan las jerarquías afectadas presentan errores
- **Problemas con las relaciones**: Las consultas MDX sobre las relaciones pueden fallar
- **Errores de calendario/variación**: Las funciones de inteligencia temporal dejan de funcionar
- **Comportamiento impredecible**: Algunas consultas funcionan y otras fallan según la herramienta cliente

Las columnas necesitan `IsAvailableInMDX = true` cuando se usan para lo siguiente:

- Se usan como niveles en jerarquías
- Referenciadas como columnas de "Ordenar por"
- Usadas en variaciones (jerarquías alternativas)
- Forman parte de las definiciones del calendario
- Sirven como destino de "Ordenar por" para otras columnas

## Cuándo se activa esta regla

La regla se activa cuando una columna tiene `IsAvailableInMDX = false` y se cumple cualquiera de estas condiciones:

```csharp
IsAvailableInMDX = false
and
(
    UsedInSortBy.Any()
    or
    UsedInHierarchies.Any()
    or
    UsedInVariations.Any()
    or
    UsedInCalendars.Any()
    or
    SortByColumn != null
)
```

La regla comprueba estas colecciones de dependencias:

| Propiedad           | Descripción                                   | Ejemplo de uso                                      |
| ------------------- | --------------------------------------------- | --------------------------------------------------- |
| `UsedInHierarchies` | Jerarquías en las que la columna es un nivel  | Niveles de la jerarquía de productos                |
| `UsedInSortBy`      | Columnas que la usan como clave de ordenación | Nombres de los meses ordenados por el número de mes |
| `UsedInVariations`  | Jerarquías alternativas que usan la columna   | Variaciones de productos                            |
| `UsedInCalendars`   | Referencias a metadatos del calendario        | Definiciones de calendario de la tabla de fechas    |
| `SortByColumn`      | La columna se ordena por otra columna         | Esta columna tiene una referencia de «Ordenar por»  |

## Cómo corregirlo

### Corrección automática

Esta regla incluye una corrección automática:

```csharp
IsAvailableInMDX = true
```

Para aplicar:

1. En el **Best Practice Analyzer**, selecciona los objetos marcados
2. Haz clic en **Aplicar corrección**

### Corrección manual

1. En el **Explorador TOM**, localiza la columna marcada
2. En el panel de **Propiedades**, busca `IsAvailableInMDX`
3. Establece el valor a `true`
4. Guarda y prueba las jerarquías y ordenaciones afectadas

## Escenarios habituales

### Escenario 1: columna de nivel de la jerarquía

**Problema**: una columna usada como nivel de jerarquía tiene MDX deshabilitado

```dax
Jerarquía: Geografía
  Niveles:
    - País
    - Estado (IsAvailableInMDX = false)  ← Problema
    - Ciudad
```

**Error**: "La jerarquía 'Geografía' no se puede usar porque uno de sus niveles no está disponible en MDX."

**Solución**: Establece `State[IsAvailableInMDX] = true`

### Escenario 2: columna de «Ordenar por»

**Problema**: una columna que sirve como destino de «Ordenar por» tiene MDX deshabilitado

```
Columna Nombre del mes:
  - SortByColumn = MonthNumber
  - MonthNumber.IsAvailableInMDX = false  ← Problema
```

**Error**: los meses se muestran en orden alfabético en lugar de en orden de calendario

**Solución**: Establece `MonthNumber[IsAvailableInMDX] = true`

### Escenario 3: definición del calendario

**Problema**: Una columna de fecha utilizada en los metadatos del calendario tiene MDX desactivado

```
DateTable:
  - Calendar usa la columna DateKey
  - DateKey.IsAvailableInMDX = false  ← Problema
```

**Error**: Las funciones de inteligencia temporal fallan

**Solución**: Establecer `DateKey[IsAvailableInMDX] = true`

## Nivel de compatibilidad

Esta regla se aplica a modelos con nivel de compatibilidad **1200** y superior.

## Reglas relacionadas

- [Establecer IsAvailableInMDX en False](xref:kb.bpa-set-isavailableinmdx-false) - La regla de optimización complementaria
