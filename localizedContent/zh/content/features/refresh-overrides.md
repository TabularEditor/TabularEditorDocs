---
uid: refresh-overrides
title: 刷新覆盖配置文件
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

# 刷新覆盖配置文件

Refresh override profiles allow you to temporarily modify certain model properties during a refresh operation without changing the actual model metadata. This is configured through the [Advanced Refresh dialog](xref:advanced-refresh).

## 为什么要使用刷新覆盖？

在开发和测试语义模型时，你经常需要使用与模型元数据中定义不同的配置来刷新数据。 Common scenarios include:

- **只加载一部分数据**，以加快开发阶段的刷新操作
- **连接到不同的数据源**（例如开发或测试数据库）
- **使用不同的参数值进行测试**，再提交对模型的更改

Without refresh overrides, you would need to temporarily modify the model metadata, perform the refresh, and then remember to revert the changes. This approach is error-prone—it's easy to forget to revert a change, potentially resulting in incorrect metadata being deployed to production.

刷新覆盖通过将临时刷新配置与模型元数据分离，解决了这个问题。

## 覆盖配置文件结构

覆盖配置文件使用符合[TMSL 刷新命令规范](https://learn.microsoft.com/en-us/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions)的 JSON。 The JSON is an array of override objects, where each object can contain one or more of the following:

- `scope` - 将覆盖范围限定为特定的表或分区（可选）
- `dataSources` - 覆盖数据源连接属性
- `expressions` - 覆盖共享表达式（M 参数）
- `partitions` - 覆盖分区源查询
- `columns` - 覆盖列的源映射（仅适用于 DataColumns）

在 `dataSources`、`expressions`、`partitions` 或 `columns` 中的每个覆盖项都必须包含 `originalObject` 属性，用于标识要覆盖的模型对象。

### 覆盖范围

By default, overrides apply globally to the refresh operation. However, you can use the `scope` property to limit an override to only affect a specific table or partition. This is useful when you want to refresh the entire model but need specific tables to source data differently than what's configured in the model metadata.

`scope` 对象可以包含：

- `database` - 数据库名
- `table` - 表名（仅在刷新此表时应用覆盖）
- `partition` - 分区名（仅在刷新此分区时应用覆盖）

## 示例

下面的示例可直接复制到新的覆盖配置文件中，并按需修改。

### 使用 SQL 查询覆盖来限制行数

此示例覆盖一个分区，使其仅加载前 10,000 行，以加快开发阶段的刷新速度：

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

### 按日期范围筛选数据

通过添加 WHERE 子句仅加载最近的数据：

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

### 覆盖多个分区

你可以在一个配置文件中覆盖多个分区：

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

### 重写数据源连接字符串

刷新时连接到其他服务器或数据库：

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

### 重写共享表达式（M 参数）

重写 M 参数值，例如服务器名称参数：

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

### 组合多种重写类型

你可以在单个配置文件中组合数据源、表达式和分区的重写：

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

### 重写 Power Query 分区

对于使用 M（Power Query）的分区，可以重写其表达式：

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

### 使用 scope 指定特定表

刷新整个模型时，你可以使用 `scope` 属性，使重写仅应用于特定表。 This example overrides the data source connection string, but only when refreshing the "Sales" table:

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

使用此配置后，刷新整个模型时，除“Sales”表外，所有表都会使用默认数据源；“Sales”表将从重写中指定的连接加载数据。

### 多个作用域重写

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

## 创建重写配置文件的提示

1. **查找对象名称**：`originalObject` 属性要求数据库、表、分区、数据源和表达式的名称与它们在模型中显示的完全一致。 You can find these names in the TOM Explorer.

2. **从简单开始**：先从单个覆盖开始，测试通过后再逐步增加复杂度。

3. **使用导出 TMSL 脚本**：配置好覆盖配置文件后，在“高级刷新”对话框中点击 **导出 TMSL 脚本...** 按钮，即可查看将生成的完整 TMSL 命令。 This helps verify your overrides are correctly applied.

4. **数据库名称**：`originalObject` 中的数据库名称应与你在服务器上看到的语义模型名称一致（或部署后将显示的名称）。

## 配置文件存储

覆盖配置文件按模型存储在 `UserOptions.tmuo` 文件中：

- **适用于保存在磁盘上的模型**：`.tmuo` 文件与模型文件存放在同一位置（例如与你的 `.bim` 文件或 Database.tmdl 位于同一文件夹中）
- **对于通过 XMLA 连接的模型**：`.tmuo` 文件存放在 `%LocalAppData%\TabularEditor3\UserOptions` 下

This means override profiles are preserved across Tabular Editor sessions. As it's not recommended to add the .tmuo files to source control, you can share override profiles among team members by manually editing the .tmuo files.