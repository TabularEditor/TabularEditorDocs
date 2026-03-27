---
uid: kb.bpa-data-column-source
title: La columna de datos debe tener una columna de origen
author: Morten Lønskov
updated: 2026-01-09
description: Regla de mejores prácticas que garantiza que las columnas de datos tengan una asignación válida a una columna de origen para evitar errores de actualización.
---

# La columna de datos debe tener una columna de origen

## Descripción general

Esta regla de mejores prácticas identifica las columnas de datos que no tienen una propiedad `SourceColumn` válida. Cada columna de datos debe hacer referencia a una columna de origen en el Data source subyacente para funcionar correctamente durante la actualización.

- Categoría: Prevención de errores
- Gravedad: Alta (3)

## Se aplica a

- Columnas de datos

## Por qué es importante

- **Fallos de actualización**: Las operaciones de actualización de datos fallan con errores de "columna no encontrada"
- **Problemas de implementación**: La validación del modelo falla en Power BI Service o Analysis Services
- **Integridad de datos**: La columna permanece vacía o contiene datos desactualizados
- **Dependencias rotas**: Las medidas y las relaciones producen resultados incorrectos

## Cuándo se activa esta regla

La regla se activa cuando una columna de datos tiene:

```csharp
string.IsNullOrWhitespace(SourceColumn)
```

## Cómo corregirlo

### Corrección manual

1. En el **Explorador TOM**, localiza la columna de datos marcada
2. En el panel de **Propiedades**, busca la propiedad `Source Column`
3. Especifica el nombre correcto de la columna de origen en la consulta de tu Data source
4. Comprueba que la asignación coincida con la consulta de la partición

El nombre de la columna de origen debe coincidir exactamente con:

- Para Power Query: nombre de la columna en la salida de la expresión M
- Para SQL: nombre de la columna o alias en la instrucción SELECT
- Para Direct Lake: nombre de la columna en la tabla de Delta Lake

## Causas habituales

### Causa 1: Columna de origen con nombre cambiado

Se modificó la consulta de origen y se renombró la columna.

### Causa 2: Creación manual de columnas

La columna se creó manualmente sin especificar el origen.

### Causa 3: Corrupción al copiar y pegar

Se copiaron columnas de otra tabla sin conservar los metadatos.

## Ejemplo

### Antes de corregir

```
Tabla: Sales
Columna: ProductName (DataColumn)
  SourceColumn: [empty]
```

Resultado: la actualización falla con "No se encuentra la columna 'ProductName' en la consulta de origen"

### Después de corregir

```
Tabla: Sales
Columna: ProductName (DataColumn)
  SourceColumn: ProductName
```

Resultado: la columna se carga correctamente durante la actualización

## Nivel de compatibilidad

Esta regla se aplica a modelos con nivel de compatibilidad **1200** o superior.

## Reglas relacionadas

- [Expresión obligatoria para objetos calculados](xref:kb.bpa-expression-required) - Garantiza que las columnas calculadas tengan expresiones
