---
uid: semantic-bridge-how-tos
title: 语义桥操作指南
author: Greg Baldini
updated: 2025-01-27
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
          none: true
        - edition: Enterprise
          full: true
---

# 语义桥操作指南

这些操作指南重点介绍如何与 [Databricks Metric View 对象模型](xref:semantic-bridge-metric-view-object-model) 交互，并支持通过导入工作流将这些 Metric View 引入 Tabular 语义模型。

## 入门

- @semantic-bridge-load-inspect - 加载 Metric View 并查看其结构
- @semantic-bridge-import - 将 Metric View 导入 Tabular，并查看诊断信息

## 验证

- @semantic-bridge-validate-default - 使用内置规则进行验证
- @semantic-bridge-validate-simple-rules - 创建基于谓词的验证规则，用于命名约定
- @semantic-bridge-validate-contextual-rules - 创建包含跨对象检查的规则，例如重复检测

## 操作对象模型

- @semantic-bridge-add-object - 向 Metric View 添加新对象
- @semantic-bridge-remove-object - 从 Metric View 移除对象
- @semantic-bridge-rename-objects - 使用“复制-修改”模式重命名对象

## 序列化

- @semantic-bridge-serialize - 将 Metric View 序列化回 YAML
