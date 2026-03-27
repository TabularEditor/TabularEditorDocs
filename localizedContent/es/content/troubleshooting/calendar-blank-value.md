---
uid: calendar-blank-value
title: Error de fecha en blanco en la función Calendar
author: Morten Lønskov
updated: 2025-10-20
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Error de fecha en blanco en la función Calendar

## Información general

Este error puede aparecer al actualizar un modelo en **Tabular Editor 3 (TE3)**, incluso si la tabla afectada no hace referencia directamente a una función `CALENDAR()`. Normalmente indica que una tabla de Fecha o Calendario dependiente se basa en valores de otras tablas que están temporalmente vacías, lo que da como resultado valores en blanco para la fecha de inicio o de fin.

## Síntomas

- La actualización del modelo en Tabular Editor 3 falla con:

  ```
  La fecha de inicio o la fecha de fin en la función Calendar no puede estar en blanco.
  ```

- El mismo modelo o tabla se actualiza correctamente en Power BI Desktop o en Power BI Service.

- Reimportar la tabla con un nombre nuevo (por ejemplo, _TableName 1_) funciona de manera temporal.

- La expresión M de la tabla afectada parece sencilla y válida:

  ```m
  let
    Source = <DataSource>,
    Data = Source{[Schema=SchemaVar,Item="TableX"]}[Data]
  in
    Data
  ```

## Causa

Aunque el error pueda parecer no estar relacionado con la tabla que se está actualizando, por lo general se origina en una dependencia posterior del modelo.

Por ejemplo, una tabla de Fecha o Calendario puede definir su rango de forma dinámica en función de las fechas mínima y máxima de varias tablas transaccionales:

```dax
CALENDAR(
  MINX(UNION(TableA, TableB, TableC), [Date]),
  MAXX(UNION(TableA, TableB, TableC), [Date])
)
```

Si una o varias de esas tablas de origen están vacías, las expresiones `MINX` o `MAXX` devuelven un valor en blanco, lo que hace que la función `CALENDAR()` falle.

## Pasos para solucionarlo

1. **Identifica las tablas dependientes**
   - Usa la vista **Dependencies** en Tabular Editor 3 para localizar tablas de fecha o calendario que hagan referencia a campos de fecha de otras tablas.
2. **Comprueba si hay tablas vacías**
   - Comprueba que todas las tablas a las que se hace referencia contienen datos. Si una tabla de origen está vacía, actualiza el Data source o ajusta la configuración de la variable de esquema.
3. **Agrega valores predeterminados alternativos**
   - Para evitar límites vacíos, envuelve las expresiones con `COALESCE()` o especifica valores de fecha predeterminados:

     ```dax
     CALENDAR(
       COALESCE(MINX(...), DATE(2000,1,1)),
       COALESCE(MAXX(...), TODAY())
     )
     ```
4. **Vuelve a procesar el modelo**
   - Después de aplicar correcciones o actualizaciones de datos, vuelve a procesar las tablas afectadas en Tabular Editor 3.

## Notas adicionales

> [!NOTE]
> Este problema puede producirse al introducir variables de esquema en scripts M, por ejemplo, al usar una variable para definir el nombre del esquema (p. ej., `SchemaVar`).