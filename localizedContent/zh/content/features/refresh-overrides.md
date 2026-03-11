---
uid: refresh-overrides
title: Refresh Override Profiles
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
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# Refresh Override Profiles

Refresh override profiles allow you to temporarily modify certain model properties during a refresh operation without changing the actual model metadata. This is configured through the [Advanced Refresh dialog](xref:advanced-refresh).

## Why use refresh overrides?

When developing and testing semantic models, you often need to refresh data with different configurations than what's defined in the model metadata. Common scenarios include:

- **Loading a subset of data** to speed up development refresh operations
- **Connecting to a different data source** (e.g., a development or test database)
- **Testing with different parameter values** before committing changes to the model

Without refresh overrides, you would need to temporarily modify the model metadata, perform the refresh, and then remember to revert the changes. This approach is error-prone—it's easy to forget to revert a change, potentially resulting in incorrect metadata being deployed to production.

Refresh overrides solve this problem by keeping temporary refresh configurations separate from the model metadata.

## Override profile structure

Override profiles use JSON that follows the [TMSL refresh command specification](https://learn.microsoft.com/en-us/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions). The JSON is an array of override objects, where each object can contain one or more of the following:

- `scope` - Limit the override to a specific table or partition (optional)
- `dataSources` - Override data source connection properties
- `expressions` - Override shared expressions (M parameters)
- `partitions` - Override partition source queries
- `columns` - Override column source mappings (DataColumns only)

Each override within `dataSources`, `expressions`, `partitions`, or `columns` must include an `originalObject` property that identifies which model object to override.

### Override scope

By default, overrides apply globally to the refresh operation. However, you can use the `scope` property to limit an override to only affect a specific table or partition. This is useful when you want to refresh the entire model but need specific tables to source data differently than what's configured in the model metadata.

The `scope` object can contain:
- `database` - The database name
- `table` - The table name (applies override only when refreshing this table)
- `partition` - The partition name (applies override only when refreshing this partition)

## Examples

Below are examples you can copy directly into a new override profile and modify for your needs.

### Limiting rows with a SQL query override

This example overrides a partition to load only the top 10,000 rows, useful for faster refresh during development:

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

### Filtering data by date range

Load only recent data by adding a WHERE clause:

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

### Overriding multiple partitions

You can override multiple partitions in a single profile:

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

### Overriding a data source connection string

Connect to a different server or database during refresh:

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

### Overriding a shared expression (M parameter)

Override an M parameter value, such as a server name parameter:

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

### Combining multiple override types

You can combine data source, expression, and partition overrides in a single profile:

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

### Overriding a Power Query partition

For partitions that use M (Power Query), override the expression:

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

### Using scope to target a specific table

When refreshing the entire model, you can use the `scope` property to apply an override only to a specific table. This example overrides the data source connection string, but only when refreshing the "Sales" table:

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

With this configuration, when you refresh the entire model, all tables will use the default data source except for the "Sales" table, which will load data from the connection specified in the override.

### Multiple scoped overrides

You can combine multiple scoped overrides in a single profile. This example uses different data sources for different tables:

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

## Tips for creating override profiles

1. **Find object names**: The `originalObject` property requires exact names of databases, tables, partitions, data sources, and expressions as they appear in your model. You can find these names in the TOM Explorer.

2. **Start simple**: Begin with a single override and test it before adding more complexity.

3. **Use Export TMSL script**: After configuring an override profile, use the **Export TMSL script...** button in the Advanced Refresh dialog to see the complete TMSL command that will be generated. This helps verify your overrides are correctly applied.

4. **Database name**: The database name in the `originalObject` should match the name of your semantic model as it appears on the server (or will appear after deployment).

## Profile storage

Override profiles are stored per-model in the `UserOptions.tmuo` file:

- **For models saved on disk**: The `.tmuo` file is stored alongside the model files (e.g., in the same folder as your `.bim` file or Database.tmdl)
- **For XMLA-connected models**: The `.tmuo` files are stored under `%LocalAppData%\TabularEditor3\UserOptions`

This means override profiles are preserved across Tabular Editor sessions. As it's not recommended to add the .tmuo files to source control, you can share override profiles among team members by manually editing the .tmuo files.