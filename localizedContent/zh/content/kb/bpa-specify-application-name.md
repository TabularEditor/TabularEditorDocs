---
uid: kb.bpa-specify-application-name
title: 在连接字符串中指定应用程序名称
author: Morten Lønskov
updated: 2026-01-09
description: 最佳实践规则：在 SQL Server 连接字符串中包含应用程序名称，以便进行监控和故障排查。
---

# 在连接字符串中指定应用程序名称

## 概述

此规则用于识别其连接字符串中缺少 Application Name 参数的 SQL Server Provider数据源。 包含应用程序名称可提升监控与故障排查的效果。 包含应用程序名称可提升监控与故障排查的效果。

- 类别：性能
- 严重性：低（1）

## 适用于

- Provider数据源

## 为什么重要

- **查询跟踪**：DBA 可以识别生成查询的应用程序
- **性能监控**：隔离表格模型查询以便分析
- **故障排查**：快速定位问题查询的来源
- **审计**：按应用程序跟踪数据访问

## 此规则何时触发

当某个数据源同时满足以下两个条件时，此规则会触发：

1. 连接字符串使用 SQL Server 提供程序（包含 `SQLNCLI`、`SQLOLEDB` 或 `MSOLEDBSQL`）
2. 连接字符串不包含 `Application Name` 参数

换句话说，此规则会识别缺少应用程序名称标识的 SQL Server 连接。

## 如何修复

### 手动修复

将应用程序名称添加到连接字符串中：

```
Provider=MSOLEDBSQL;Data Source=ServerName;Initial Catalog=DatabaseName;Application Name=Tabular Editor;Integrated Security=SSPI;
```

## 示例

### 修复前

```
Provider=MSOLEDBSQL;Data Source=localhost;Initial Catalog=AdventureWorks;
```

### 修复后

```
Provider=MSOLEDBSQL;Data Source=localhost;Initial Catalog=AdventureWorks;Application Name=Sales Model;
```

结果：现在可以在 SQL Server 监控工具中识别这些查询。

## 兼容级别

这个规则适用于兼容级别为 **1200** 及以上的模型。

## 相关规则

- [移除未使用的数据源](xref:kb.bpa-remove-unused-data-sources) - 数据源维护
