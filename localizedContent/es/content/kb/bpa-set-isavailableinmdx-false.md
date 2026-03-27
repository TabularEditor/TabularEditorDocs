---
uid: kb.bpa-set-isavailableinmdx-false
title: Establecer IsAvailableInMDX en False
author: Morten Lønskov
updated: 2026-01-09
description: Regla de práctica recomendada para optimizar el rendimiento deshabilitando el acceso a MDX para columnas ocultas que no se usan en relaciones ni jerarquías.
---

# Establecer IsAvailableInMDX en False

## Información general

Esta regla de prácticas recomendadas identifica columnas ocultas que tienen la propiedad `IsAvailableInMDX` establecida en `true`, pero que no necesitan estar accesibles mediante consultas MDX. Si estableces esta propiedad en `false` para columnas ocultas sin uso, puedes mejorar el rendimiento de las consultas y reducir la sobrecarga de memoria.

- Categoría: Rendimiento
- Gravedad: Media (2)

## Se aplica a

- Columnas de datos
- Columnas calculadas
- Columnas de tablas calculadas

## Por qué es importante

Cuando una columna tiene `IsAvailableInMDX` establecido en `true`, el motor de Analysis Services mantiene metadatos y estructuras adicionales para admitir consultas MDX sobre esa columna. En el caso de columnas ocultas que no se usan en relaciones, jerarquías, variaciones, calendarios o como columnas de ordenación, esta sobrecarga es innecesaria y puede:

- Aumentar el consumo de memoria
- Ralentizar el procesamiento de consultas
- Añadir complejidad a los metadatos del modelo

Al establecer explícitamente `IsAvailableInMDX` en `false` para estas columnas, optimizas el modelo para escenarios solo con DAX, el principal lenguaje de consulta de Power BI y de los modelos modernos de Analysis Services.

> [!WARNING]
> **Compatibilidad con tablas dinámicas de Excel**: Establecer `IsAvailableInMDX` en `false` impide que las columnas se puedan arrastrar al área de filas o columnas de las tablas dinámicas de Excel. Las tablas dinámicas de Excel generan consultas MDX al conectarse a modelos tabulares de Analysis Services, y necesitan jerarquías de atributos (que solo se crean cuando `IsAvailableInMDX = true`) para funcionar correctamente. Si sus usuarios necesitan analizar datos con tablas dinámicas de Excel u otras herramientas basadas en MDX, **no** aplique esta regla a las columnas a las que necesiten acceder. Para más detalles, consulta el [artículo de Chris Webb sobre IsAvailableInMDX](https://blog.crossjoin.co.uk/2018/07/02/isavailableinmdx-ssas-tabular/).

## Cuándo se activa esta regla

La regla se activa cuando se cumplen todas las condiciones siguientes:

1. La columna tiene `IsAvailableInMDX = true`
2. La columna está oculta (o lo está la tabla que la contiene)
3. La columna NO se usa en ninguna relación de `SortBy`
4. La columna NO se usa en ninguna jerarquía
5. La columna NO se usa en ninguna variación
6. La columna NO se usa en ningún calendario
7. La columna NO actúa como `SortByColumn` de otra columna

## Cómo solucionarlo

### Corrección automática

Esta regla incluye una expresión de corrección automática. Cuando apliques la corrección en el Best Practice Analyzer:

```csharp
IsAvailableInMDX = false
```

Para aplicarlo:

1. En el **Best Practice Analyzer**, selecciona los objetos marcados
2. Haz clic en **Aplicar corrección**

### Corrección manual

1. En el **Explorador TOM**, localiza la columna marcada
2. En el panel de **Propiedades**, busca la propiedad `IsAvailableInMDX`
3. Establece el valor a `false`
4. Guarda los cambios

## Ejemplo

Considera una columna calculada oculta que solo se usa para cálculos intermedios:

```dax
_TempCalculation = 
CALCULATE(
    SUM('Sales'[Amount]),
    ALLEXCEPT('Sales', 'Sales'[ProductKey])
)
```

Si esta columna está:

- Oculta para las herramientas cliente
- No se usa en jerarquías ni en relaciones
- No se hace referencia en operaciones de ordenación

Se recomienda establecer `IsAvailableInMDX = false` para obtener un rendimiento óptimo.

## Nivel de compatibilidad

Esta regla se aplica a modelos con nivel de compatibilidad **1200** y superior.

## Reglas relacionadas

- [Establecer IsAvailableInMDX en True cuando sea necesario](xref:kb.bpa-set-isavailableinmdx-true-necessary) - La regla complementaria que garantiza que las columnas que necesitan acceso a MDX lo tengan habilitado
