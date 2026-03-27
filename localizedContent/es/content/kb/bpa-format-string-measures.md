---
uid: kb.bpa-format-string-measures
title: Proporcionar una cadena de formato a las medidas
author: Morten Lønskov
updated: 2026-01-09
description: Regla de mejores prácticas que garantiza que las medidas visibles tengan cadenas de formato adecuadas para una visualización coherente.
---

# Proporcionar una cadena de formato a las medidas

## Información general

Esta regla de mejores prácticas identifica las medidas visibles con tipos de datos numéricos o de fecha que no tienen una cadena de formato. Todas las medidas deben tener cadenas de formato explícitas para una visualización profesional y coherente.

- Categoría: Formato

- Gravedad: Media (2)

## Se aplica a

- Medidas

## Por qué es importante

Las medidas sin cadenas de formato muestran valores sin procesar, lo que genera confusión entre los usuarios y Reports incoherentes. Las cadenas de formato garantizan:

- **Aspecto profesional**: Los valores se muestran con el formato adecuado de moneda, porcentaje o número
- **Coherencia**: Todos los Reports muestran los valores con el mismo formato
- **Confianza del usuario**: Los números con el formato correcto son más fáciles de leer e interpretar
- **Alineación con el negocio**: El formato coincide con los estándares corporativos

## Cuándo se activa esta regla

```csharp
IsVisible
and string.IsNullOrWhitespace(FormatString)
and (DataType = "Int64" or DataType = "DateTime" or DataType = "Double" or DataType = "Decimal")
```

## Cómo solucionarlo

### Corrección manual

1. En el **Explorador TOM**, seleccione la medida
2. En el panel de **Propiedades**, busca el campo **Cadena de formato**
3. Escribe una cadena de formato adecuada en función de lo que calcule la medida
4. Guarda los cambios

### Patrones de formato habituales

```dax
Ingresos totales = 
SUM('Sales'[Amount])
// Cadena de formato: "$#,0"

Precio promedio = 
AVERAGE('Sales'[UnitPrice])
// Cadena de formato: "$#,0,00"

Crecimiento interanual = 
DIVIDE([This Year] - [Last Year], [Last Year], 0)
// Cadena de formato: "0,0%"

Recuento de pedidos = 
COUNTROWS('Orders')
// Cadena de formato: "#,0"
```

## Causas habituales

### Causa 1: Falta la definición de formato

Al crear una nueva medida, de forma predeterminada no se establece ninguna cadena de formato.

### Causa 2: Copiar y pegar desde columnas calculadas

Copia de medidas desde columnas que no requieren cadenas de formato.

## Ejemplo

### Antes de la corrección

```dax
Total Revenue = SUM('Sales'[Amount])
// Sin cadena de formato
```

**Visualización**: 1234567.89 (difícil de leer, sin símbolo de moneda)

### Después de la corrección

```dax
Total Revenue = SUM('Sales'[Amount])
// Cadena de formato: "$#,0"
```

**Visualización**: $1.234.568 (formato claro y profesional)

## Nivel de compatibilidad

Esta regla se aplica a modelos con nivel de compatibilidad **1200** o superior.

## Reglas relacionadas

- [Cadena de formato para columnas](xref:kb.bpa-format-string-columns) - Validación similar para las columnas
