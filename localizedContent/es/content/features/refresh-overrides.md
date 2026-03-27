---
uid: refresh-overrides
title: Perfiles de sobrescritura de actualización
author: Daniel Otykier
updated: 2026-01-20
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.25.0
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Perfiles de sobrescritura de actualización

Los perfiles de sobrescritura de actualización te permiten modificar temporalmente determinadas propiedades del modelo durante una operación de actualización, sin cambiar los metadatos reales del modelo. Esto se configura en el [cuadro de diálogo Actualización avanzada](xref:advanced-refresh).

## ¿Por qué usar sobrescrituras de actualización?

Al desarrollar y probar modelos semánticos, a menudo necesitas actualizar los datos con configuraciones distintas de las definidas en los metadatos del modelo. Escenarios habituales:

- **Cargar un subconjunto de datos** para acelerar las actualizaciones durante el desarrollo
- **Conectarse a una fuente de datos diferente** (p. ej., una base de datos de desarrollo o de pruebas)
- **Probar con distintos valores de parámetros** antes de confirmar los cambios en el modelo

Sin sobrescrituras de actualización, tendrías que modificar temporalmente los metadatos del modelo, ejecutar la actualización y, después, acordarte de revertir los cambios. Este enfoque es propenso a errores: es fácil olvidarse de revertir un cambio, lo que podría provocar que se implementen metadatos incorrectos en producción.

Las sobrescrituras de actualización resuelven este problema al mantener las configuraciones temporales de actualización separadas de los metadatos del modelo.

## Estructura del perfil de sobrescritura

Los perfiles de sobrescritura usan JSON que sigue la [especificación del comando de actualización de TMSL](https://learn.microsoft.com/en-us/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions). El JSON es una matriz de objetos de sobrescritura, donde cada objeto puede contener uno o varios de los siguientes:

- `scope` - Limita la sobrescritura a una tabla o partición específicas (opcional)
- `dataSources` - Sobrescribe las propiedades de conexión de la fuente de datos
- `expressions` - Sobrescribe las expresiones compartidas (parámetros M)
- `partitions` - Sobrescribe las consultas de origen de las particiones
- `columns` - Sobrescribe las asignaciones de origen de las columnas (solo DataColumns)

Cada sobrescritura dentro de `dataSources`, `expressions`, `partitions` o `columns` debe incluir una propiedad `originalObject` que identifique qué objeto del modelo se va a sobrescribir.

### Ámbito de la sobrescritura

De forma predeterminada, las sobrescrituras se aplican de manera global a la operación de actualización. Sin embargo, puedes usar la propiedad `scope` para limitar una sobrescritura y que solo afecte a una tabla o partición específicas. Esto es útil cuando quieres actualizar todo el modelo, pero necesitas que determinadas tablas obtengan los datos de forma distinta a como está configurado en los metadatos del modelo.

El objeto `scope` puede contener:

- `database` - El nombre de la base de datos
- `table` - El nombre de la tabla (aplica la sobrescritura solo al actualizar esta tabla)
- `partition` - El nombre de la partición (aplica la sobrescritura solo al actualizar esta partición)

## Ejemplos

A continuación tienes ejemplos que puedes copiar directamente en un nuevo perfil de sobrescritura y modificar según tus necesidades.

### Limitar filas con una sobrescritura de consulta SQL

Este ejemplo sobrescribe una partición para cargar solo las primeras 10.000 filas, útil para acelerar la actualización durante el desarrollo:

```json
[
  {
    "partitions": [
      {
        "originalObject": {
          "database": "AdventureWorks",
          "table": "FactInternetSales",
          "partition": "FactInternetSales"
        },
        "source": {
          "query": "SELECT TOP 10000 * FROM [dbo].[FactInternetSales]"
        }
      }
    ]
  }
]
```

### Filtrar datos por rango de fechas

Carga solo los datos recientes añadiendo una cláusula WHERE:

```json
[
  {
    "partitions": [
      {
        "originalObject": {
          "database": "AdventureWorks",
          "table": "FactInternetSales",
          "partition": "FactInternetSales"
        },
        "source": {
          "query": "SELECT * FROM [dbo].[FactInternetSales] WHERE OrderDate >= '2024-01-01'"
        }
      }
    ]
  }
]
```

### Sobrescribir varias particiones

Puedes sobrescribir varias particiones en un solo perfil:

```json
[
  {
    "partitions": [
      {
        "originalObject": {
          "database": "AdventureWorks",
          "table": "FactInternetSales",
          "partition": "FactInternetSales"
        },
        "source": {
          "query": "SELECT TOP 1000 * FROM [dbo].[FactInternetSales]"
        }
      },
      {
        "originalObject": {
          "database": "AdventureWorks",
          "table": "FactResellerSales",
          "partition": "FactResellerSales"
        },
        "source": {
          "query": "SELECT TOP 1000 * FROM [dbo].[FactResellerSales]"
        }
      }
    ]
  }
]
```

### Sobrescritura de la cadena de conexión de un origen de datos

Conectarse a un servidor o una base de datos diferente durante la actualización:

```json
[
  {
    "dataSources": [
      {
        "originalObject": {
          "database": "AdventureWorks",
          "dataSource": "SqlServer localhost AdventureWorksDW"
        },
        "connectionString": "Data Source=devserver;Initial Catalog=AdventureWorksDW_Dev;Integrated Security=True"
      }
    ]
  }
]
```

### Sobrescritura de una expresión compartida (parámetro M)

Sobrescribir el valor de un parámetro M, como un parámetro de nombre de servidor:

```json
[
  {
    "expressions": [
      {
        "originalObject": {
          "database": "AdventureWorks",
          "expression": "ServerName"
        },
        "expression": "\"devserver\" meta [IsParameterQuery=true, Type=\"Text\", IsParameterQueryRequired=true]"
      }
    ]
  }
]
```

### Combinar varios tipos de sobrescritura

Puede combinar sobrescrituras de orígenes de datos, expresiones y particiones en un solo perfil:

```json
[
  {
    "dataSources": [
      {
        "originalObject": {
          "database": "AdventureWorks",
          "dataSource": "SqlServer localhost AdventureWorksDW"
        },
        "connectionString": "Data Source=devserver;Initial Catalog=AdventureWorksDW_Dev;Integrated Security=True"
      }
    ],
    "partitions": [
      {
        "originalObject": {
          "database": "AdventureWorks",
          "table": "FactInternetSales",
          "partition": "FactInternetSales"
        },
        "source": {
          "query": "SELECT TOP 5000 * FROM [dbo].[FactInternetSales]"
        }
      }
    ]
  }
]
```

### Sobrescritura de una partición de Power Query

Para las particiones que usan M (Power Query), sobrescriba la expresión:

```json
[
  {
    "partitions": [
      {
        "originalObject": {
          "database": "AdventureWorks",
          "table": "DimCustomer",
          "partition": "DimCustomer"
        },
        "source": {
          "expression": "let\n    Source = Sql.Database(\"devserver\", \"AdventureWorksDW_Dev\"),\n    dbo_DimCustomer = Source{[Schema=\"dbo\",Item=\"DimCustomer\"]}[Data],\n    #\"Kept First Rows\" = Table.FirstN(dbo_DimCustomer, 1000)\nin\n    #\"Kept First Rows\""
        }
      }
    ]
  }
]
```

### Uso de scope para dirigirse a una tabla específica

Al actualizar todo el modelo, puede usar la propiedad `scope` para aplicar una sobrescritura solo a una tabla específica. Este ejemplo sobrescribe la cadena de conexión del origen de datos, pero solo al actualizar la tabla "Sales":

```json
[
  {
    "scope": {
      "database": "AdventureWorks",
      "table": "Sales"
    },
    "dataSources": [
      {
        "originalObject": {
          "dataSource": "SqlServer localhost AdventureWorksDW"
        },
        "connectionString": "Provider=SQLNCLI11;Data Source=devserver;Initial Catalog=AdventureWorksDW_Dev;Integrated Security=SSPI;Persist Security Info=false"
      }
    ]
  }
]
```

Con esta configuración, al actualizar todo el modelo, todas las tablas usarán el origen de datos predeterminado, excepto la tabla "Sales", que cargará los datos desde la conexión especificada en la sobrescritura.

### Múltiples sobrescrituras con ámbito

Puede combinar varias sobrescrituras con ámbito en un solo perfil. Este ejemplo utiliza distintos orígenes de datos para distintas tablas:

```json
[
  {
    "scope": {
      "database": "AdventureWorks",
      "table": "FactInternetSales"
    },
    "dataSources": [
      {
        "originalObject": {
          "dataSource": "SqlServer localhost AdventureWorksDW"
        },
        "connectionString": "Data Source=salesdb;Initial Catalog=SalesData_Test;Integrated Security=True"
      }
    ]
  },
  {
    "scope": {
      "database": "AdventureWorks",
      "table": "DimCustomer"
    },
    "dataSources": [
      {
        "originalObject": {
          "dataSource": "SqlServer localhost AdventureWorksDW"
        },
        "connectionString": "Data Source=customerdb;Initial Catalog=CustomerData_Test;Integrated Security=True"
      }
    ]
  }
]
```

## Consejos para crear perfiles de sobrescritura

1. **Buscar nombres de objetos**: La propiedad `originalObject` requiere los nombres exactos de bases de datos, tablas, particiones, orígenes de datos y expresiones tal como aparecen en su modelo. Puede encontrar estos nombres en el Explorador TOM.

2. **Empieza por lo simple**: Empieza con una sola sobrescritura y pruébala antes de añadir más complejidad.

3. **Usa Export TMSL script**: Después de configurar un perfil de sobrescritura, usa el botón **Export TMSL script...** del cuadro de diálogo Actualización avanzada para ver el comando TMSL completo que se generará. Esto ayuda a comprobar que las sobrescrituras se aplican correctamente.

4. **Nombre de la base de datos**: El nombre de la base de datos en `originalObject` debe coincidir con el nombre del modelo semántico tal y como aparece en el servidor (o como aparecerá tras la implementación).

## Almacenamiento de perfiles

Los perfiles de sobrescritura se almacenan por modelo en el archivo `UserOptions.tmuo`:

- **Para modelos guardados en disco**: El archivo `.tmuo` se almacena junto a los archivos del modelo (por ejemplo, en la misma carpeta que el archivo `.bim` o Database.tmdl)
- **Para modelos en modo conectado mediante XMLA**: Los archivos `.tmuo` se almacenan en `%LocalAppData%\\TabularEditor3\\UserOptions`

Esto significa que los perfiles de sobrescritura se conservan entre sesiones de Tabular Editor. Como no se recomienda añadir los archivos .tmuo al control de código fuente, puedes compartir perfiles de sobrescritura entre los miembros del equipo editando manualmente los archivos .tmuo.