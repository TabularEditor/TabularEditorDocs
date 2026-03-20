---
uid: kb.bpa-relationship-same-datatype
title: Las columnas de una relación deben tener el mismo tipo de datos
author: Morten Lønskov
updated: 2026-01-09
description: Regla de buenas prácticas que garantiza que las relaciones conecten columnas con tipos de datos coincidentes para evitar errores y problemas de rendimiento.
---

# Las columnas de una relación deben tener el mismo tipo de datos

## Descripción general

Esta regla de prácticas recomendadas identifica relaciones en las que las columnas vinculadas tienen tipos de datos distintos. Ambas columnas de una relación deben compartir el mismo tipo de datos para garantizar un filtrado correcto, evitar errores y mantener un rendimiento óptimo de las consultas.

- Categoría: Prevención de errores

- Gravedad: Alta (3)

## Se aplica a

- Relaciones

## Por qué es importante

Las relaciones con tipos de datos que no coinciden provocan problemas graves:

- **Errores de validación del modelo**: Es posible que el modelo no se pueda guardar ni publicar
- **Errores al crear relaciones**: Power BI y Analysis Services pueden rechazar la relación
- **Conversiones implícitas**: Conversiones de tipo de datos costosas en cada consulta
- **Resultados incorrectos**: La conversión forzada de tipos provoca un comportamiento de filtrado inesperado
- **Degradación del rendimiento**: Convertir tipos de datos durante las consultas ralentiza la ejecución
- **Sobrecarga de memoria**: Se requiere memoria adicional para los búferes de conversión

## Cuándo se activa esta regla

La regla se activa cuando:

```csharp
FromColumn.DataType != ToColumn.DataType
```

Esto detecta relaciones que conectan columnas con tipos de datos diferentes.

## Cómo corregirlo

### Solución manual

1. Identifica qué columna debe cambiar de tipo de datos
2. Cambia el tipo de datos en **Power Query**, en el Data source subyacente o en el modelo
3. Elimina la relación existente
4. Crea una nueva relación entre las columnas corregidas
5. Comprueba que el filtrado funciona correctamente

## Causas comunes

### Causa 1: Selección incoherente de tipos de datos

Se eligieron distintos tipos de datos para la misma clave lógica durante la importación o la creación de la tabla.

### Causa 2: Diferencias entre sistemas de origen

Claves foráneas importadas desde distintos sistemas de origen con convenciones de tipo diferentes.

### Causa 3: Desajuste entre DateTime y Date

Tablas de hechos que usan columnas DateTime mientras que las dimensiones de fecha usan el tipo Date.

## Ejemplo

### Antes de la corrección

```
Relación: Sales[CustomerID] (Int64) → Customers[CustomerID] (String)
```

**Error**: la relación no pasa la validación o provoca problemas de rendimiento por conversión implícita

### Después de la corrección

```
Relación: Sales[CustomerID] (Int64) → Customers[CustomerID] (Int64)
```

**Resultado**: la relación funciona de forma eficiente, sin sobrecarga por conversión de tipos

## Nivel de compatibilidad

Esta regla se aplica a modelos con nivel de compatibilidad **1200** y superior.

## Reglas relacionadas

- [Las relaciones de muchos a muchos deben usar una sola dirección](xref:kb.bpa-many-to-many-single-direction) - Optimización del rendimiento de las relaciones
