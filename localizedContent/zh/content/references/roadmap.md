---
uid: roadmap
title: 路线图
author: Morten Lønskov
updated: 2025-10-29
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      full: true
---

# Tabular Editor 3 路线图

以下概述 Tabular Editor 3 在未来从短期到长期更新中将推出的主要新功能：

# [即将推出](#tab/upcoming)

## 开发中

- **Semantic Bridge 增强**：支持 v1.1 属性，并改进导入 UI
- **本地化改进**：扩展语言支持，并优化现有翻译
- **Power Query (M) 自动格式化**：为 M 表达式提供更高级的格式化能力
- **图形化模型比较**：查看将要应用的更改

## 即将推出

- Tabular Editor 中的 AI 助手
- 支持.NET 10
- Git 集成
- Power Query (M) 编辑功能增强
- 将 TOM 属性显示为 TMDL 和 TMSL 脚本
- 独立的 CLI 应用程序
- 内置宏

## 未来

- DAX 调试器筛选语境 Visual 可视化器
- 可配置的 Daxscilla 自动完成代码片段
- 可配置的代码编辑器主题（语法高亮颜色）
- 增量部署（类似于 [ALM Toolkit](http://alm-toolkit.com/)）
- 改进宏操作，例如可自动应用到整个模型，并可设置应用偏好以选择应用范围

# [已发布](#tab/shipped)

如需了解每个版本的详细信息，请参阅[完整发布历史](xref:release-history)。

## 于 2026 年发布

✅ [**本地化**](xref:references-application-language) — 支持中文、西班牙语（预览）、日语、德语和法语（实验性）（v3.25.0）

✅ [**内置 Best Practice Analyzer 规则**](xref:built-in-bpa-rules) — 一套全面的 BPA 规则，覆盖格式化、元数据、模型布局、DAX 表达式和翻译（v3.25.0）

✅ **Semantic Bridge** - 从 Databricks Metric Views 创建语义模型（企业版，v3.25.0）

✅ [**保存时附带 Fabric 支持文件**](xref:save-with-supporting-files) — 支持 .platform 和 definition.pbism 文件，以匹配 Fabric repository 结构（v3.25.0）

✅ **日历编辑器** - 面向时间智能的日历对象管理界面已增强（v3.25.0）

✅ [**高级刷新对话框**](xref:advanced-refresh) - 配置并行度、增量刷新的生效日期，以及 [刷新覆盖配置文件](xref:refresh-overrides)（商业版/企业版，v3.25.0）

## 2025 年发布

✅ [**DAX 组件管理器**](xref:dax-package-manager) - 从 daxlib.org 一键查找并安装 DAX 组件（v3.24.0）

✅ **UDF 命名空间** - 以层级方式组织用户自定义函数，并支持自定义命名空间属性（v3.24.0）

✅ **Visual Calculations 改进** - 增强 DAX 编辑器对 Visual Calculation 函数和可视化列引用的支持（v3.24.0）

✅ [**DAX 用户自定义函数 (UDFs)**](xref:udfs) - 创建和管理可复用的 DAX 函数（v3.23.0）

✅ [**日历**](xref:calendars) - 提供基于日历的时间智能功能，并带来增强的 UI（v3.23.0）

✅ **Fabric SQL 数据库与镜像数据库支持** - 导入向导现支持新的 Fabric 数据源，可在 Import 和 Direct Lake 模式下使用（v3.23.0）

✅ [**在 OneLake 和 SQL 上使用 Direct Lake**](xref:direct-lake-guidance) - 完整支持 Direct Lake 模式，包括混合模式和混合模型（企业版，v3.22.0）

✅ **按词自动补全** - DAX 编辑器的自动补全现支持多词搜索（v3.22.0）

✅ **图表视图增强** - 列数据类型图标、双向关系指示器，以及改进的表显示选项（v3.21.0）

✅ **从 TOM Explorer 复制 TMDL 脚本** - 将单个对象以 TMDL 导出到剪贴板或文件（v3.21.0）

✅ **DAX优化器 RLS 支持** - 查看 DAX优化器针对 RLS 和计算项表达式的结果（v3.21.0）

✅ **MetadataSource 属性** - 新增 Model 对象属性，让 C# Script 能访问模型元数据位置（v3.21.0）

✅ **C# 编辑器改进** - 更好的代码编辑体验：更强的 IntelliSense 与更灵活的搜索

✅ **原生 ARM64 版本** - 在 ARM64 处理器上提供更优性能（v3.23.0）

## 2024 年发布

✅ DAX 调试器 Locals 增强

✅ 完整的 Direct Lake 集成

✅ DAX优化器集成（预览）

✅ .Net 8 迁移

✅ Pivot Grid 增强

✅ DAX 查询增强功能

✅ 支持 TMDL GA 正式版

✅ 代码操作

✅ DAX优化器集成正式发布

✅ 数据刷新视图改进

✅ Power Query (M) 语法高亮

## 已于 2023 年发布

✅ “保存到文件夹”默认使用 TMDL 作为文件格式。 （取决于 Microsoft 发布 TMDL 的时间） （取决于 Microsoft 发布 TMDL 的时间）

✅ 导入表向导支持 Databricks（待用于获取元数据/架构的 REST 端点可用）

✅ 元数据翻译编辑器（在选择一个或多个区域设置时可打开的视图，类似于 Tabular Translator 工具）

✅ 透视编辑器（在选择一个或多个透视时可打开的视图，可勾选/取消勾选在这些透视中可见的对象）

✅ 增强对 Oracle 数据库的支持

✅ 导入表向导支持 Power BI 数据集市（使用 Datamart SQL 端点）

## 已于 2022 年发布

✅ DAX 调试器

✅ .NET 6 迁移

✅ C# Code Assist（自动完成、参数信息、调用提示等）

✅ 导入表向导支持 Snowflake

✅ 导入表向导支持 Power BI Dataflow

✅ 可配置的快捷键

✅ 支持 DAX 窗口函数

✅ Git 集成（私有预览）

## 已于 2021 年发布

✅ 导入表向导

✅  便携版

✅  支持模拟特定角色或用户的身份来使用 Pivot Grid、表格预览和 DAX 查询，便于测试 RLS/OLS

✅  支持计算组和计算项的 DAX脚本

✅  离线 DAX 格式化

***

# Tabular Editor 2 路线图

> [!NOTE]
> Tabular Editor 2 已不再进行积极开发，我们将不再添加或改进任何重大功能。 不过，我们还是会让它保持最新：确保支持 Microsoft 发布的新的语义模型功能，并修复任何关键或阻断性问题。 由于该项目基于 MIT 协议开源，任何人都可以提交 Pull Request，我们团队会审核并批准。