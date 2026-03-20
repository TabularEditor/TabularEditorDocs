---
uid: kb.bpa-format-string-columns
title: Proporcionar una cadena de formato para columnas numéricas y de fecha
author: Morten Lønskov
updated: 2026-01-09
description: Regla de prácticas recomendadas que garantiza que las columnas numéricas y de fecha visibles tengan cadenas de formato adecuadas para una visualización coherente.
---

# Proporcionar una cadena de formato para columnas numéricas y de fecha

## Descripción general

Esta regla de prácticas recomendadas identifica columnas visibles de tipo numérico o de fecha que no tienen definida ninguna cadena de formato. Las cadenas de formato garantizan una visualización de datos coherente y profesional en todas las herramientas de cliente.

- Categoría: Formato

- Gravedad: Media (2)

## Se aplica a

- Columnas de datos
- Columnas calculadas
- Columnas de tablas calculadas

## Por qué es importante

Las columnas sin cadenas de formato se muestran de forma incoherente:

- **Aspecto poco profesional**: Números en bruto como 1234567.89 en lugar de $1.234.567,89
- **Confusión del usuario**: Los usuarios no pueden saber si los valores son moneda, porcentajes o números sin formato
- **Formato incoherente**: Distintos Visuales pueden mostrar formatos diferentes
- **Carga de formato manual**: Los usuarios deben dar formato a cada Visual de forma individual
- **Ambigüedad en las fechas**: Las fechas muestran marcas de tiempo cuando solo se necesita la fecha

## Cuándo se activa esta regla

```csharp
IsVisible
and string.IsNullOrWhitespace(FormatString)
and (DataType = "Int64" or DataType = "DateTime" or DataType = "Double" or DataType = "Decimal")
```

## Cómo solucionarlo

### Corrección manual

1. En el **Explorador TOM**, selecciona la columna
2. En el panel **Propiedades**, busca el campo **Cadena de formato**
3. Elige entre formatos estándar o introduce un formato personalizado
4. Guarda los cambios

## Causas habituales

### Causa 1: Falta la definición del formato

Las columnas no tienen una cadena de formato al importarlas.

## Ejemplo

### Antes de la corrección

```
Columna: SalesAmount
Cadena de formato: (vacío)
```

**Visualización**: 1234567.89 (difícil de leer, sin símbolo de moneda)

### Después de la corrección

```
Columna: SalesAmount
Cadena de formato: "$#,0,00"
```

**Visualización**: $1.234.567,89 (formato claro y profesional)

## Nivel de compatibilidad

Esta regla se aplica a modelos con nivel de compatibilidad **1200** o superior.

## Reglas relacionadas

- [Proporcionar cadena de formato para medidas](xref:kb.bpa-format-string-measures) - Validación similar para las medidas
