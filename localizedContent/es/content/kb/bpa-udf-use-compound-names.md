---
uid: kb.bpa-udf-use-compound-names
title: Use nombres compuestos para las funciones definidas por el usuario
author: Morten Lønskov
updated: 2026-03-19
description: Regla de buenas prácticas que garantiza que las funciones definidas por el usuario usen caracteres separadores para evitar conflictos de nombres con futuras funciones DAX integradas.
---

# Use nombres compuestos para las funciones definidas por el usuario

## Descripción general

Esta regla de buenas prácticas identifica funciones definidas por el usuario (UDFs) cuyos nombres no contienen un carácter separador (`.` o `_`). Los nombres compuestos evitan conflictos de nombres si Microsoft introduce una función de DAX integrada con el mismo nombre.

- Categoría: Prevención de errores

- Gravedad: Baja (1)

## Se aplica a

- Funciones definidas por el usuario

## Por qué es importante

Las UDFs sin caracteres separadores en sus nombres corren el riesgo de dejar de funcionar en el futuro:

- **Conflictos de nombres**: Si Microsoft agrega una nueva función DAX integrada con el mismo nombre que su UDF, la función integrada tiene prioridad y su UDF dejará de funcionar
- **Ambigüedad**: Sin un espacio de nombres o un prefijo, no queda claro si una llamada a una función hace referencia a una función de DAX integrada o a una UDF personalizada
- **Carga de mantenimiento**: Cambiar el nombre de las UDFs tras producirse un conflicto requiere actualizar todas las referencias en todo el modelo

Usar nombres compuestos (por ejemplo, `Finance.CalcProfit` o `My_CalcProfit`) permite distinguir sus UDFs de las funciones DAX integradas.

## Cuándo se activa esta regla

La regla se activa cuando el nombre de una UDF no contiene ni un punto ni un guion bajo:

```csharp
not Name.Contains(".") and not Name.Contains("_")
```

## Cómo corregir

### Corrección manual

1. En el **Explorador TOM**, localice la función definida por el usuario
2. Cambie el nombre para incluir un separador de espacio de nombres (`.`) o un guion bajo (`_`)
3. Tabular Editor actualiza automáticamente todas las referencias del modelo

## Causas comunes

### Causa 1: Nomenclatura sencilla

Se le dio a la función un nombre simple sin considerar posibles conflictos futuros.

### Causa 2: Importada desde una consulta

Se aplicó una UDF desde la sección DEFINE de una consulta DAX, donde no se respetaron las convenciones de espacios de nombres.

## Ejemplo

### Antes de la corrección

```dax
// Función nombrada sin separador
FUNCTION CalcProfit =
    (
        revenue: DOUBLE,
        cost: DOUBLE
    )
    => revenue - cost
```

### Después de la corrección

```dax
// Función nombrada con separador de espacios de nombres
FUNCTION Finance.CalcProfit =
    (
        revenue: DOUBLE,
        cost: DOUBLE
    )
    => revenue - cost
```

## Nivel de compatibilidad

Esta regla se aplica a modelos con nivel de compatibilidad **1702** y superior.

## Reglas relacionadas

- [Funciones DAX definidas por el usuario](xref:udfs)
- [Reglas BPA integradas](xref:built-in-bpa-rules)
