---
uid: kb.bpa-avoid-provider-partitions-structured
title: 避免在 Structured数据源中使用提供程序分区
author: Morten Lønskov
updated: 2026-01-09
description: 此最佳实践规则通过识别 Power BI 中与 Structured数据源一起使用的旧版提供程序分区，帮助避免部署错误。
---

# 避免在 Structured数据源中使用提供程序分区

## 概述

此最佳实践规则用于识别 Power BI 模型中与 Structured数据源配合使用旧版基于提供程序的查询（SourceType = Query）的分区。 Power BI Service 不支持这种组合，因而会导致部署失败。

- 类别：错误预防

- 严重性：中等（2）

## 适用范围

- 分区

## 为何重要

Power BI Service 要求 Structured数据源使用 Power Query（M）分区，而非旧版提供程序分区。 在 Structured数据源中使用提供程序分区会导致：

- **部署失败**：模型无法发布到 Power BI Service
- **刷新错误**：在服务中执行的计划刷新会失败
- **兼容性问题**：模型无法正确共享或部署
- **迁移障碍**：阻碍从 Analysis Services 迁移到 Power BI

## 规则触发条件

当某个分区同时满足以下所有条件时，规则会触发：

1. `SourceType = "Query"`（旧版提供程序分区）
2. `DataSource.Type = "Structured"`（Power Query/M 数据源）
3. `Model.Database.CompatibilityMode != "AnalysisServices"`（Power BI 或 Azure AS）

这种组合表示结构不匹配，Power BI 无法处理。

## 如何修复

### 手动修复

1. 在 **TOM Explorer** 中，选择受影响的分区
2. 在 **Properties** 窗格中，记录现有查询
3. 使用 M 表达式新建一个 **Power Query** 分区
4. 确认新分区可正常工作后，删除旧的提供程序分区

## 常见原因

### 原因 1：从 Analysis Services 迁移

从 SQL Server Analysis Services 迁移的模型会保留旧版提供程序分区。

### 原因 2：混用分区类型

在模型开发过程中混用分区类型，会造成不兼容的配置。

## 示例

### 修复前

```
分区: Sales_Partition
  SourceType: Query
  Query: SELECT * FROM Sales
  DataSource: PowerQuerySource (Type: Structured)
```

**错误**：部署到 Power BI 服务时失败

### 修复后

```
分区: Sales_Partition
  SourceType: M
  Expression: 
    let
        Source = Sql.Database("server", "database"),
        Sales = Source{[Schema="dbo",Item="Sales"]}[Data]
    in
        Sales
  DataSource: PowerQuerySource (Type: Structured)
```

**结果**：成功部署到 Power BI 服务

## 兼容级别

此规则适用于兼容级别为 **1200** 及以上、并部署到 Power BI 或 Azure Analysis Services 的模型。

## 相关规则

- [数据列必须有源](xref:kb.bpa-data-column-source) - 确保列源映射
