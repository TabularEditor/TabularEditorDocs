---
uid: kb.bpa-avoid-provider-partitions-structured
title: Evitar particiones de proveedor con orígenes de datos estructurados
author: Morten Lønskov
updated: 2026-01-09
description: Regla de mejores prácticas que evita errores de implementación al identificar particiones heredadas de proveedor que se usan con orígenes de datos estructurados en Power BI.
---

# Evitar particiones de proveedor con orígenes de datos estructurados

## Resumen

Esta regla de mejores prácticas identifica particiones que usan consultas heredadas basadas en proveedor (SourceType = Query) con orígenes de datos estructurados en modelos de Power BI. Esta combinación no es compatible con el servicio Power BI y provocará fallos de despliegue.

- Categoría: Prevención de errores

- Gravedad: Media (2)

## Se aplica a

- Particiones

## Por qué es importante

El servicio Power BI requiere que los orígenes de datos estructurados utilicen particiones de Power Query (M) en lugar de particiones de proveedor heredadas. El uso de particiones de proveedor con orígenes de datos estructurados provoca:

- **Fallos de despliegue**: Los modelos no se pueden publicar en el servicio Power BI
- **Errores de actualización**: Las operaciones de actualización programada fallan en el servicio
- **Problemas de compatibilidad**: El modelo no se puede compartir ni desplegar correctamente
- **Bloqueos de migración**: Impide pasar de Analysis Services a Power BI

## Cuándo se activa esta regla

La regla se activa cuando una partición cumple todas estas condiciones:

1. `SourceType = "Query"` (partición de proveedor heredada)
2. `DataSource.Type = "Structured"` (Data source de Power Query/M)
3. `Model.Database.CompatibilityMode != "AnalysisServices"` (Power BI o Azure AS)

Esta combinación indica una incompatibilidad estructural que Power BI no puede procesar.

## Cómo solucionarlo

### Solución manual

1. En el **Explorador TOM**, selecciona la partición afectada
2. En el panel **Propiedades**, toma nota de la consulta existente
3. Crea una nueva partición de **Power Query** con una expresión M
4. Después de verificar que la nueva partición funciona, elimina la partición del proveedor anterior

## Causas habituales

### Causa 1: Migración desde Analysis Services

Los modelos migrados desde SQL Server Analysis Services conservan particiones heredadas del proveedor.

### Causa 2: Tipos de partición mezclados

Mezclar tipos de partición durante el desarrollo del modelo crea configuraciones incompatibles.

## Ejemplo

### Antes de la solución

```
Partición: Sales_Partition
  SourceType: Query
  Query: SELECT * FROM Sales
  DataSource: PowerQuerySource (Type: Structured)
```

**Error**: La implementación en Power BI Service falla

### Después de la solución

```
Partición: Sales_Partition
  SourceType: M
  Expression: 
    let
        Source = Sql.Database("server", "database"),
        Sales = Source{[Schema="dbo",Item="Sales"]}[Data]
    in
        Sales
  DataSource: PowerQuerySource (Type: Structured)
```

**Resultado**: Se implementa correctamente en Power BI Service

## Nivel de compatibilidad

Esta regla se aplica a los modelos con nivel de compatibilidad **1200** o superior al implementarlos en Power BI o Azure Analysis Services.

## Reglas relacionadas

- [La columna de datos debe tener un origen](xref:kb.bpa-data-column-source) - Para garantizar las asignaciones del origen de la columna
