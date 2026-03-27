---
uid: kb.bpa-avoid-invalid-characters-names
title: 避免在对象名称中使用无效字符
author: Morten Lønskov
updated: 2026-01-09
description: 这条最佳实践规则通过识别对象名称中的控制字符来防止部署错误。
---

# 避免在对象名称中使用无效字符

## 概述

这条最佳实践规则用于识别名称中包含无效控制字符的对象（即不包括标准空白字符的不可打印字符）。 这些字符可能导致部署失败、呈现问题以及数据损坏。

- 类别：错误预防
- 严重性：高（3）

## 适用于

- 表
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

对象名称中的控制字符会引发严重问题：

- **部署失败**：Power BI 服务和 Analysis Services 可能会拒绝包含无效字符的模型
- **呈现问题**：客户端工具可能会显示乱码或不可见的名称
- **DAX 解析错误**：无效字符可能会导致引用该对象的 DAX 表达式出错
- **XML 损坏**：模型元数据（TMSL/XMLA）可能会变得格式异常
- **复制/粘贴问题**：名称在不同应用之间可能无法正确传递
- **编码问题**：影响跨平台兼容性

允许使用标准空白字符（空格、换行、回车），但要移除控制字符。

## 何时会触发此规则

当对象名称包含非标准空白字符的控制字符时，此规则会触发：

```csharp
Name.ToCharArray().Any(char.IsControl(it) and !char.IsWhiteSpace(it))
```

这样既能保留正常的空白格式，也能检测出有问题的字符。

## 如何修复

### 自动修复

这个规则提供自动修复，会把无效字符替换为空格：

```csharp
Name = string.Concat(
    it.Name.ToCharArray().Select(
        c => (char.IsControl(c) && !char.IsWhiteSpace(c)) ? ' ' : c
    )
)
```

操作步骤：

1. 在 **Best Practice Analyzer** 中选择被标记的对象
2. 单击 **Apply Fix**

### 手动修复

1. 在 **TOM Explorer** 中选择对象
2. 在 **Properties** 窗格中找到 **Name** 字段
3. 编辑名称，移除无效字符
4. 保存更改

## 常见原因

### 原因 1：从富文本复制/粘贴

从 Word 文档、网页或邮件中复制名称，可能会带入隐藏的格式字符。

### 原因 2：自动生成名称

用于生成名称的脚本可能会从源系统带入控制字符。

### 原因 3：从外部源导入数据

导入包含编码残留或控制码的元数据。

## 示例

### 修复前

```
度量值名称：“Total\x00Sales”（包含 NULL 字符）
```

部署失败，提示“对象名称中包含无效字符”

### 修复后

```
度量值名称：“Total Sales”（将 NULL 替换为空格）
```

部署成功，并在所有工具中正确显示。

## 兼容级别

本规则适用于兼容级别为 **1200** 及以上的模型。

## 相关规则

- [避免在描述中使用无效字符](xref:kb.bpa-avoid-invalid-characters-descriptions) —— 针对描述属性的类似验证
- [修剪对象名称](xref:kb.bpa-trim-object-names) —— 删除首尾空格

## 了解更多

- [DAX 命名规则](https://learn.microsoft.com/dax/dax-syntax-reference)
