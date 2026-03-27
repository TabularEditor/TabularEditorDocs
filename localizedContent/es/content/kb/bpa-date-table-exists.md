---
uid: kb.bpa-date-table-exists
title: Debe existir una tabla de fechas
author: Morten Lønskov
updated: 2026-01-09
description: Regla de buenas prácticas que garantiza que tu modelo incluya una tabla de fechas dedicada para que la inteligencia temporal funcione correctamente.
---

# Debe existir una tabla de fechas

## Descripción general

Esta regla de buenas prácticas verifica que tu modelo tabular contenga al menos una tabla de fechas configurada correctamente. Las tablas de fechas son esenciales para los cálculos de inteligencia temporal y para garantizar un filtrado coherente basado en fechas en todo tu modelo.

- Categoría: Rendimiento

- Gravedad: Media (2)

## Se aplica a

- Modelo

## Por qué es importante

Una tabla de fechas dedicada es esencial porque:

- **Habilita la inteligencia temporal**: Funciones como `DATESYTD`, `SAMEPERIODLASTYEAR` y `TOTALYTD` requieren una tabla de fechas
- **Garantiza un filtrado coherente**: Proporciona una única fuente de verdad para los atributos de fecha
- **Mejora el rendimiento**: establece las relaciones de calendario adecuadas
- **Admite calendarios personalizados**: permite cálculos de año fiscal y jerarquías personalizadas

Sin una tabla de fechas correctamente marcada, muchas funciones DAX de inteligencia temporal fallarán o producirán resultados incorrectos.

## Cuándo se activa esta regla

La regla se activa cuando **todas** las tablas de tu modelo cumplen las siguientes condiciones:

1. Ninguna tabla tiene calendarios definidos (`Calendars.Count = 0`)
2. Ninguna tabla contiene una columna marcada como clave con `DataType = DateTime`
3. Ninguna tabla tiene `DataCategory = "Time"`

Esto indica que al modelo le falta una dimensión de fechas adecuada.

## Cómo solucionarlo

### Opción 1: Crear una tabla de fechas con DAX

Agrega una tabla calculada con un rango de fechas completo:

```dax
DateTable = 
ADDCOLUMNS (
    CALENDAR (DATE(2020, 1, 1), DATE(2030, 12, 31)),
    "Year", YEAR([Date]),
    "Quarter", "Q" & FORMAT([Date], "Q"),
    "Month", FORMAT([Date], "MMMM"),
    "MonthNumber", MONTH([Date]),
    "Day", DAY([Date]),
    "WeekDay", FORMAT([Date], "dddd")
)
```

### Opción 2: Importar desde el Data source

Crea una tabla de dimensión de fechas en tu Warehouse o Data source, e impórtala al modelo.

### Marcar como tabla de fechas

Después de crear la tabla:

1. Selecciona la tabla de fechas en el **Explorador TOM**
2. Haz clic con el botón derecho y selecciona **Marcar como tabla de fechas**
3. Selecciona la columna de fecha como columna clave
4. Crea relaciones entre la tabla de fechas y tus tablas de hechos

### Configurar los metadatos del calendario

Como alternativa, configura los metadatos del calendario:

1. Selecciona la tabla de fechas
2. En el panel de **Propiedades**, expande la sección **Calendarios**
3. Agrega un calendario nuevo y configura la referencia de la columna de fecha

## Ejemplo

Una estructura típica de tabla de fechas:

| Fecha                                               | Año                                                 | Trimestre                                           | Mes                                                 | Número de mes                                       | Día                                                 |
| --------------------------------------------------- | --------------------------------------------------- | --------------------------------------------------- | --------------------------------------------------- | --------------------------------------------------- | --------------------------------------------------- |
| 2025-01-01                                          | 2025                                                | Q1                                                  | Enero                                               | 1                                                   | 1                                                   |
| 2025-01-02                                          | 2025                                                | Q1                                                  | Enero                                               | 1                                                   | 2                                                   |
| ... | ... | ... | ... | ... | ... |

Una vez creada, establezca las relaciones:

```
'DateTable'[Date] (1) -> (*) 'Sales'[OrderDate]
'DateTable'[Date] (1) -> (*) 'Orders'[ShipDate]
```

## Nivel de compatibilidad

Esta regla se aplica a modelos con nivel de compatibilidad **1200** y superior.

## Reglas relacionadas

- [Quitar la tabla de fechas automática](xref:kb.bpa-remove-auto-date-table) - Eliminación de las tablas de fechas automáticas que duplican la funcionalidad

## Más información

- [Crear tablas de fechas en Power BI](https://learn.microsoft.com/power-bi/guidance/model-date-tables)
- [Funciones de inteligencia temporal en DAX](https://learn.microsoft.com/dax/time-intelligence-functions-dax)
- [Marcar como tabla de fechas](https://learn.microsoft.com/power-bi/transform-model/desktop-date-tables)
