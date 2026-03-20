---
uid: kb.bpa-remove-auto-date-table
title: Eliminar tablas de fechas automáticas
author: Morten Lønskov
updated: 2026-01-09
description: Regla de buenas prácticas para identificar y eliminar tablas de fechas generadas automáticamente que aumentan el tamaño del modelo y reducen el rendimiento.
---

# Eliminar tablas de fechas automáticas

## Descripción general

Esta regla de buenas prácticas identifica las tablas de fechas generadas automáticamente por Power BI Desktop. Estas tablas generadas automáticamente (`DateTableTemplate_` y `LocalDateTable_`) deben eliminarse y sustituirse por una única tabla de fechas explícita para optimizar el tamaño y el rendimiento del modelo.

- Categoría: Rendimiento

- Gravedad: Media (2)

## Se aplica a

- Tablas
- Tablas calculadas

## Por qué es importante

Power BI crea automáticamente tablas de fechas ocultas para cada columna de fecha o fecha y hora cuando está habilitada la opción "Auto Date/Time". Esto provoca problemas:

- **Aumento del tamaño del modelo**: Cada tabla generada automáticamente añade datos innecesarios
- **Sobrecarga de memoria**: Varias tablas de fechas consumen más memoria que una sola tabla compartida
- **Actualización más lenta**: Las tablas adicionales aumentan la duración de la actualización

Una única tabla de fechas bien diseñada es mucho más eficiente y fácil de mantener.

## Cuándo se activa esta regla

La regla se activa cuando encuentra tablas calculadas cuyos nombres:

- Comienzan por `"DateTableTemplate_"`, o
- Comienzan por `"LocalDateTable_"`

Estos prefijos indican las tablas de fechas generadas automáticamente por Power BI.

## Cómo solucionarlo

### Solución manual

1. Deshabilita **Fecha/hora automática** en Power BI Desktop (**Archivo** > **Opciones** > **Carga de datos**)
2. Crea una tabla de fechas específica.
3. Márcala como tabla de fechas y crea relaciones con las tablas de hechos
4. En el **Explorador TOM**, elimina las tablas que empiecen por `DateTableTemplate_` o `LocalDateTable_`
5. Comprueba que las relaciones de la tabla de fechas personalizada funcionen correctamente

## Causas habituales

### Causa 1: Función de Fecha/hora automática habilitada

La función "Fecha/hora automática" de Power BI Desktop crea estas tablas automáticamente.

### Causa 2: Modelos migrados

Modelos creados con las tablas automáticas habilitadas y que nunca se depuraron.

### Causa 3: Configuración predeterminada

Los modelos nuevos usan la configuración predeterminada, que habilita las tablas de fechas automáticas.

## Ejemplo

### Antes de la corrección

```
Tablas:
  - Sales
  - LocalDateTable_OrderDate (oculta, generada automáticamente)
  - LocalDateTable_ShipDate (oculta, generada automáticamente)
  - Products
  - LocalDateTable_ReleaseDate (oculta, generada automáticamente)
```

**Resultado**: Varias tablas ocultas aumentan el tamaño del modelo

### Después de la corrección

```
Tablas:
  - Sales
  - Products
  - DateTable (explícita, marcada mediante Marcar como tabla de fechas)
    -> Relaciones con Sales[OrderDate], Sales[ShipDate], Products[ReleaseDate]
```

**Resultado**: Una única tabla de fechas eficiente sirve para todas las relaciones de fechas

## Nivel de compatibilidad

Esta regla se aplica a modelos con nivel de compatibilidad **1200** y superior.

## Reglas relacionadas

- [Debe existir una tabla de fechas](xref:kb.bpa-date-table-exists) - Garantiza que haya una tabla de fechas adecuada

## Más información

- [Desactivar fecha y hora automáticas en Power BI](https://learn.microsoft.com/power-bi/guidance/auto-date-time)
- [Crear tablas de fechas](https://learn.microsoft.com/power-bi/guidance/model-date-tables)
- [Prácticas recomendadas para tablas de fechas](https://www.sqlbi.com/articles/creating-a-simple-date-table-in-dax/)
