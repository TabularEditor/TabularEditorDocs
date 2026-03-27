---
uid: kb.bpa-specify-application-name
title: Especificar el nombre de la aplicación en las cadenas de conexión
author: Morten Lønskov
updated: 2026-01-09
description: Regla de prácticas recomendadas para incluir el nombre de la aplicación en cadenas de conexión de SQL Server y facilitar la supervisión y la solución de problemas.
---

# Especificar el nombre de la aplicación en las cadenas de conexión

## Descripción general

Esta regla identifica los orígenes de datos del proveedor de SQL Server que no incluyen el parámetro `Application Name` en sus cadenas de conexión. Incluir el nombre de la aplicación permite una mejor supervisión y solución de problemas.

- Categoría: Rendimiento
- Gravedad: Baja (1)

## Se aplica a

- Orígenes de datos del proveedor

## Por qué es importante

- **Seguimiento de consultas**: Los DBA pueden identificar qué aplicación generó las consultas
- **Supervisión del rendimiento**: Aislar las consultas del modelo tabular para analizarlas
- **Solución de problemas**: Identificar rápidamente el origen de las consultas problemáticas
- **Auditoría**: Hacer seguimiento del acceso a los datos por aplicación

## Cuándo se activa esta regla

Esta regla se activa cuando un Data source cumple estas dos condiciones:

1. La cadena de conexión usa un proveedor de SQL Server (contiene `SQLNCLI`, `SQLOLEDB` o `MSOLEDBSQL`)
2. La cadena de conexión no incluye el parámetro `Application Name`

En otras palabras, la regla identifica las conexiones de SQL Server que no incluyen el identificador del nombre de la aplicación.

## Cómo solucionarlo

### Solución manual

Añade "Application Name" a la cadena de conexión:

```
Provider=MSOLEDBSQL;Data Source=ServerName;Initial Catalog=DatabaseName;Application Name=Tabular Editor;Integrated Security=SSPI;
```

## Ejemplo

### Antes de la corrección

```
Provider=MSOLEDBSQL;Data Source=localhost;Initial Catalog=AdventureWorks;
```

### Después de la corrección

```
Provider=MSOLEDBSQL;Data Source=localhost;Initial Catalog=AdventureWorks;Application Name=Sales Model;
```

Resultado: ahora es posible identificar las consultas en las herramientas de supervisión de SQL Server.

## Nivel de compatibilidad

Esta regla se aplica a modelos con nivel de compatibilidad **1200** y superior.

## Reglas relacionadas

- [Eliminar Data sources no utilizados](xref:kb.bpa-remove-unused-data-sources) - Mantenimiento de Data sources
