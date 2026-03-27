---
uid: kb.bpa-avoid-invalid-characters-descriptions
title: 避免在描述中使用无效字符
author: Morten Lønskov
updated: 2026-01-09
description: 一条最佳实践规则，通过识别对象描述中的控制字符来防止显示和部署问题。
---

# 避免在描述中使用无效字符

## 概述

此最佳做法规则会识别描述中包含无效控制字符（不可打印字符，标准空白字符除外）的对象。 这些字符可能导致显示问题、元数据损坏以及部署失败。

- 类别：预防错误
- 严重性：高（3）

## 适用范围

- 表格
- 度量值
- 层次结构
- 级别
- 透视
- 分区
- 数据列
- 计算列
- 计算表格列
- KPI
- 模型角色
- 计算组
- 计算项

## 为什么这很重要

描述中的控制字符会引发多种问题：

- **显示错乱**：工具提示和文档面板可能显示乱码
- **元数据问题**：TMSL/XMLA 导出可能生成无效的 XML
- **部署失败**：Power BI 服务或 Analysis Services 可能会拒绝该模型
- **文档问题**：生成的文档可能导致格式错乱
- **编码错误**：可能导致跨平台同步问题
- **用户困惑**：不可见字符可能导致描述内容令人困惑或显示异常

标准空白字符（空格、换行符、制表符）可以保留，但要移除不可打印的控制字符。

## 何时触发此规则

当对象的描述中包含非标准空白字符的控制字符时，就会触发此规则：

```csharp
Description.ToCharArray().Any(char.IsControl(it) and !char.IsWhiteSpace(it))
```

这样既能检测到有问题的字符，又允许保留合法的空白格式。

## 如何修复

### 自动修复

这个规则带有自动修复功能，会把无效字符替换成空格：

```csharp
Description = string.Concat(
    it.Description.ToCharArray().Select(
        c => (char.IsControl(c) && !char.IsWhiteSpace(c)) ? ' ' : c
    )
)
```

应用步骤：

1. 在 **Best Practice Analyzer** 中选择被标记的对象
2. 单击 **Apply Fix**

### 手动修复

1. 在 **TOM Explorer** 中选择该对象
2. 在 **属性** 窗格中找到 **描述** 字段
3. 编辑描述，移除无效字符
4. 保存更改

## 常见原因

### 原因 1：从富文本复制/粘贴

从 Word 文档、网页或电子邮件复制说明可能会引入隐藏的格式字符。

### 原因 2：自动化文档生成

用于生成说明的脚本可能会从源系统中带入控制字符。

### 原因 3：从外部源导入数据

导入包含编码伪影或控制代码的元数据。

## 示例

### 修复前

```
度量值：[Total Revenue]
Description: "Calculates\x00total\x0Brevenue"（包含 NULL 和垂直制表符）
```

工具提示显示：“Calculates□total□revenue”（出现明显乱码）

### 修复后

```
度量值：[Total Revenue]
Description: "Calculates total revenue"（将控制字符替换为空格）
```

工具提示正确显示："Calculates total revenue"

## 兼容级别

此规则适用于兼容级别为 **1200** 及以上的模型。

## 相关规则

- [避免名称中出现无效字符](xref:kb.bpa-avoid-invalid-characters-names)——对对象名称进行类似验证
- [可见对象应具有说明](xref:kb.bpa-visible-objects-no-description)——确保存在说明
