---
uid: kb.bpa-do-not-summarize-numeric
title: Establece SummarizeBy en None para columnas numéricas
author: Morten Lønskov
updated: 2026-01-09
description: Regla de mejores prácticas que evita agregaciones predeterminadas incorrectas en columnas numéricas que no deben sumarse.
---

# Establece SummarizeBy en None para columnas numéricas

## Descripción general

Esta regla de mejores prácticas identifica las columnas numéricas visibles (Int64, Decimal, Double) cuyo comportamiento de agregación predeterminado (`SummarizeBy`) es distinto de `None`. La mayoría de las columnas numéricas no deberían agregarse automáticamente, ya que sumar valores como IDs, cantidades en contextos no aditivos o códigos produce resultados sin sentido.

- Categoría: Formato

- Gravedad: Alta (3)

## Se aplica a

- Columnas de datos
- Columnas calculadas
- Columnas de tablas calculadas

## Por qué es importante

La agregación predeterminada en columnas inadecuadas provoca problemas graves:

- **Análisis incorrecto**: Los usuarios obtienen totales sin sentido (suma de CustomerIDs, etc.)
- **Dashboards engañosos**: Los Visuales muestran números incorrectos de forma predeterminada
- **Confusión del usuario**: Los usuarios deben cambiar manualmente la agregación en cada Visual
- **Decisiones equivocadas**: Decisiones empresariales basadas en agregaciones automáticas incorrectas
- **Credibilidad de los datos**: Los usuarios pierden la confianza en el modelo y en los datos

Entre las columnas habituales que NO deberían agregarse se incluyen los IDs, las claves, los códigos, los ratios, los porcentajes y las cantidades no aditivas.

## Cuándo se activa esta regla

La regla se activa cuando una columna cumple ALL estas condiciones:

```csharp
(DataType = "Int64" or DataType="Decimal" or DataType="Double")
and
SummarizeBy <> "None"
and not (IsHidden or Table.IsHidden)
```

En otras palabras: columnas numéricas visibles cuyo comportamiento de resumen no es "None".

## Cómo corregir

### Corrección automática

Esta regla incluye una corrección automática:

```csharp
SummarizeBy = AggregateFunction.None
```

Para aplicarla:

1. En **Best Practice Analyzer**, selecciona los objetos marcados
2. Haz clic en **Aplicar corrección**

### Corrección manual

1. En **Explorador TOM**, localiza la columna
2. En el panel **Propiedades**, busca **Resumir por**
3. Cambia de **Sum**, **Average**, **Min**, **Max**, **Count** o **DistinctCount** a **None**
4. Guarda los cambios

## Causas habituales

### Causa 1: Comportamiento predeterminado de importación

De forma predeterminada, las columnas numéricas usan la agregación Suma durante la importación.

### Causa 2: Falta de revisión de columnas

Modelos implementados sin revisar la configuración de agregación de las columnas.

### Causa 3: Columnas de ID no ocultas

Las columnas numéricas de ID siguen visibles con la agregación Suma predeterminada.

## Ejemplo

### Antes de la corrección

```
Column: CustomerID
  DataType: Int64
  SummarizeBy: Sum
```

**Resultado**: El Visual muestra "Sum of CustomerID: 12.456.789" (un número sin sentido)

### Después de la corrección

```
Column: CustomerID
  DataType: Int64
  SummarizeBy: None
```

**Resultado**: El Visual requiere una agregación explícita o muestra los identificadores de cliente de forma individual

## Nivel de compatibilidad

Esta regla se aplica a modelos con nivel de compatibilidad **1200** o superior.

## Reglas relacionadas

- [Ocultar claves externas](xref:kb.bpa-hide-foreign-keys) - Regla relacionada de limpieza de columnas
- [Cadena de formato de columnas](xref:kb.bpa-format-string-columns) - Formato de columnas

## Más información

- [Propiedades de las columnas](https://learn.microsoft.com/analysis-services/tabular-models/column-properties-ssas-tabular)
- [Cuándo usar medidas frente a columnas calculadas](https://learn.microsoft.com/power-bi/transform-model/desktop-tutorial-create-measures)
