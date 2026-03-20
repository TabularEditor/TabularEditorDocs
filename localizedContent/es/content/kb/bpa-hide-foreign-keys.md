---
uid: kb.bpa-hide-foreign-keys
title: Ocultar columnas de claves externas
author: Morten Lønskov
updated: 2026-01-09
description: Regla de mejores prácticas para ocultar columnas de claves externas y simplificar el modelo para los usuarios finales.
---

# Ocultar columnas de claves externas

## Descripción general

Esta regla de mejores prácticas identifica las columnas de claves externas (el lado "muchos" de las relaciones) que son visibles para los usuarios finales. Las claves externas deberían ocultarse porque solo sirven para establecer relaciones y no aportan valor analítico cuando se muestran.

- Categoría: Formato

- Gravedad: Media (2)

## Se aplica a

- Columnas de datos
- Columnas calculadas
- Columnas de tablas calculadas

## Por qué es importante

Las columnas de claves externas visibles crean desorden innecesario:

- **Confusión de los usuarios**: Las claves externas parecen datos útiles, pero duplican los atributos de la dimensión
- **Campos redundantes**: Los usuarios ven tanto la clave como los atributos de la dimensión relacionada
- **Listas de campos más largas**: Más elementos entre los que desplazarse para encontrar los campos relevantes
- **Uso incorrecto**: Los usuarios pueden agrupar por claves en lugar de por los atributos de dimensión adecuados
- **Visualizaciones deficientes**: Gráficos que muestran valores de la clave en lugar de nombres descriptivos

Las claves externas existen solo para crear relaciones entre tablas. Una vez establecidas las relaciones, los usuarios deberían trabajar con los atributos de la dimensión, no con las claves externas en sí.

## Cuándo se activa esta regla

La regla se activa cuando una columna es:

1. Se usa como la columna "from" en una relación (lado de muchos)
2. La relación tiene cardinalidad de muchos en el lado "from"
3. La columna está visible (`IsHidden = false`)

```csharp
UsedInRelationships.Any(FromColumn.Name == current.Name and FromCardinality == "Many")
and
IsHidden == false
```

## Cómo corregirlo

### Corrección automática

Esta regla incluye una corrección automática:

```csharp
IsHidden = true
```

Para aplicarlo:

1. En el **Best Practice Analyzer**, selecciona las columnas de clave externa marcadas
2. Haz clic en **Aplicar corrección**

### Corrección manual

1. En el **Explorador TOM**, localiza la columna de clave externa
2. En el panel **Propiedades**, configura **IsHidden** como **true**
3. Guarda los cambios

## Causas comunes

### Causa 1: Configuración incompleta del modelo

Las claves externas siguen siendo visibles después de crear relaciones.

### Causa 2: Importación masiva

Tablas importadas sin procesamiento posterior para ocultar las claves externas.

### Causa 3: Modelos heredados

Modelos antiguos en los que no se exigía ocultar las claves externas.

## Ejemplo

### Antes de la corrección

```
Campos de la tabla Sales (visibles):
  - OrderDate
  - CustomerKey  ← Clave foránea (debería ocultarse)
  - ProductKey   ← Clave foránea (debería ocultarse)
  - SalesAmount
  - Quantity
```

**Experiencia de usuario**: La lista de campos está sobrecargada. Los usuarios podrían usar por error `Sales[CustomerKey]` en lugar de `Customer[CustomerName]`.

### Después de la corrección

```
Campos de la tabla Sales (visibles):
  - OrderDate
  - SalesAmount
  - Quantity
```

**Experiencia de usuario**: La lista de campos está limpia. Los usuarios usan de forma natural los atributos de dimensión; el filtrado por relación funciona automáticamente.

## Nivel de compatibilidad

Esta regla se aplica a los modelos con nivel de compatibilidad **1200** y superior.

## Reglas relacionadas

- [Establecer SummarizeBy en None para columnas numéricas](xref:kb.bpa-do-not-summarize-numeric) - Configuración relacionada con la columna
- [Cadena de formato para columnas](xref:kb.bpa-format-string-columns) - Configuración de visualización de columnas
