---
uid: dq-over-as-limitations
title: Analysis Services 上的直接查询
author: Morten Lønskov
updated: 2025-07-14
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

## 概述

Tabular Editor 3 可以**连接**使用 **DirectQuery over Analysis Services (DQ‑over‑AS)** 的复合模型，但完整的建模支持**尚未提供**。  大多数创作任务都符合预期；但是，依赖与远程语义模型同步元数据的操作——例如 _更新
0表
0架构_——目前受到限制。

> [!IMPORTANT]
> 在完整的 DQ‑over‑AS 支持发布之前，Tabular Editor 3 中编辑的模型元数据**不会自动与源数据集保持同步**。 每当在底层 Analysis Services 模型中新增列或度量值时，都必须采用下面列出的其中一种变通方法。

## 当前限制

| 功能                    | TE3 中的状态 | 说明                                                           |
| --------------------- | -------- | ------------------------------------------------------------ |
| **更新&#xA;0表&#xA;0架构** | ❌ 不支持    | 在 DQ‑over‑AS 表上尝试运行 **Model > Update table schema** 不会有任何效果。 |
| **度量值同步**             | ❌ 不支持    | 在源数据集中创建的度量值不会自动出现在复合模型中。                                    |

## 变通方法

### 1. 手动添加缺失的列

1. 在 **TOM Explorer** 中，选择需要新增列的表。
2. 选择 **添加 > 数据列**。
3. 在 _属性_ 窗口中，设置：

   - **SourceColumnName** – 必须与远程表中该列的 **Name** _完全_一致。
   - **SourceLineageTag** – 从源列复制 **LineageTag** 值。
4. 保存并部署模型。

> [!NOTE]
> 列名和 Lineage tag 必须_逐字符_完全一致。  任何不一致都会导致部署错误。

### 2. 使用“Import tables from remote model” C# 脚本

Daniel Otykier 在 LinkedIn 上的文章提供了一个[现成的 C# 自动化脚本](https://www.linkedin.com/pulse/composite-models-tabular-editor-daniel-otykier/)：

1. 临时从远程模型导入表的完整副本。
2. 可将列（以及其他元数据）复制到现有表中。
3. 复制完成后删除这些临时表。

当需要更新的表较多时，这种方法更快。

### 3. 一键宏：拉取新增度量值

[rem-bou's](https://github.com/rem-bou) 的 GitHub 仓库包含一个高级宏，用于扫描源数据集，查找复合模型中**缺失**的度量值并自动添加：[Create-Update DQ over AS model connection](https://github.com/rem-bou/TabularEditor-Scripts/blob/main/Advanced/One-Click%20Macros/Create-Update%20DQ%20over%20AS%20model%20connection.csx)
