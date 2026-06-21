---
uid: built-in-bpa-rules
title: 内置 BPA 规则
author: Morten Lønskov
updated: 2026-03-19
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.24.0
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
description: 企业版功能：Tabular Editor 3 内置 28 条精选最佳实践规则，并与知识库集成。
---

# 内置 BPA 规则

## 概述

Tabular Editor 3 企业版包含 28 条内置最佳实践规则。 这些规则覆盖语义模型开发中的常见问题，并会随每次发布自动更新。

与存储在 JSON 文件中的自定义规则不同，内置规则：

- 直接集成在应用程序中
- 随新版本发布自动更新
- 链接到知识库文档
- 为确保各团队之间一致性，这些规则为只读
- 无需配置即可立即使用

## 主要功能

### 规则类别

这 28 条内置规则涵盖四个方面：

- **错误预防**：无效字符、缺失表达式、数据类型不匹配
- **性能**：关系、分区、聚合
- **格式设置**：格式字符串、可见性、命名规范
- **维护**：描述、计算组、未使用的对象

### 全局控制与按规则控制

![屏幕截图：BPA 偏好设置，包含全局启用/禁用开关以及按规则的复选框](~/content/assets/images/features/bpa-built-in-rules-preferences.png)
你可以全局或按规则单独启用或禁用内置规则。 这些设置会在会话之间保留，并且与自定义规则相互独立。

要管理内置规则：

1. 转到 **工具** > **偏好设置** > **Best Practice Analyzer**
2. 找到 **内置规则** 部分
3. 切换 **启用内置规则**，以开启或关闭整个规则集合
4. 使用 BPA 管理器启用或禁用单个规则

### 首次运行通知

![首次运行通知对话框屏幕截图：介绍 BPA 内置规则](~/content/assets/images/features/bpa-built-in-rules-notification.png)

升级到包含内置规则的版本后，你首次打开模型时，会看到一条通知，说明该功能，并提供前往“偏好”的链接。 此通知只会出现一次。

### 知识库集成

![屏幕截图：BPA 窗口中选中了某条规则，并高亮显示“查看文档”按钮](~/content/assets/images/features/bpa-built-in-rules-kb-link.png)

每条内置规则都会通过 `KnowledgeBaseArticle` 属性链接到一篇知识库文章。 每篇文章都会说明该规则检查什么、为什么重要，以及如何修复违规项。

要查看文档，请在 Best Practice Analyzer 窗口中选择一条规则。

### 只读保护

内置规则无法编辑、克隆或删除。 这可确保所有用户使用相同的规则定义。 你可以禁用单个规则，但规则定义本身保持不变。

![屏幕截图：BPA 窗口中的内置规则，带有只读标记/图标](~/content/assets/images/features/bpa-built-in-rules-readonly.png)

### 防止 ID 冲突

内置规则使用保留的 ID 前缀。 当你创建自定义规则时，Tabular Editor 会验证你的 ID 是否与内置规则冲突；若发生冲突，将显示错误提示。

## 内置规则目录

当前规则集包含以下规则：

### 错误预防规则

- [避免在对象名称中使用无效字符](xref:kb.bpa-avoid-invalid-characters-names)
- [避免在说明中使用无效字符](xref:kb.bpa-avoid-invalid-characters-descriptions)
- [计算对象需要表达式](xref:kb.bpa-expression-required)
- [数据列必须有来源](xref:kb.bpa-data-column-source)
- [关系列必须具有相同的数据类型](xref:kb.bpa-relationship-same-datatype)
- [避免在 Structured数据源中使用提供程序分区](xref:kb.bpa-avoid-provider-partitions-structured)
- [为用户定义函数使用复合名称](xref:kb.bpa-udf-use-compound-names)

### 性能规则

- [多对多关系应使用单向筛选方向](xref:kb.bpa-many-to-many-single-direction)
- [隐藏外键列](xref:kb.bpa-hide-foreign-keys)
- [将数值列的 SummarizeBy 设置为 None](xref:kb.bpa-do-not-summarize-numeric)
- [删除自动日期表](xref:kb.bpa-remove-auto-date-table)
- [删除未使用的数据源](xref:kb.bpa-remove-unused-data-sources)

### 格式规则

- [为度量值提供格式字符串](xref:kb.bpa-format-string-measures)
- [为数值列和日期列提供格式字符串](xref:kb.bpa-format-string-columns)
- [可见对象应提供说明](xref:kb.bpa-visible-objects-no-description)
- [去除对象名称首尾空格](xref:kb.bpa-trim-object-names)
- [应包含日期表](xref:kb.bpa-date-table-exists)

### 维护规则

- [计算组应包含计算项](xref:kb.bpa-calculation-groups-no-items)
- [透视中应包含对象](xref:kb.bpa-perspectives-no-objects)
- [使用最新的 Power BI 兼容级别](xref:kb.bpa-powerbi-latest-compatibility)

## 使用内置规则和自定义规则

内置规则与自定义规则可并行使用：

| 功能      | 内置规则      | 自定义规则        |
| ------- | --------- | ------------ |
| **存储**  | 在应用中硬编码   | JSON 文件或模型注释 |
| **更新**  | 随版本发布自动更新 | 需要手动编辑       |
| **修改**  | 只读        | 完全可编辑        |
| **文档**  | 集成的 KB 文章 | 用户提供的说明      |
| **可用性** | 仅限企业版     | 所有版本         |
| **共享**  | 跨团队保持一致   | 需要手动分发       |

### 推荐工作流程

1. 启用内置规则，立即获得检查覆盖
2. 审查违规项并应用修复
3. 禁用不适用于你们约定的规则
4. 为组织特定需求添加自定义规则
5. 对于有意为之的违规，使用“忽略”功能

## 最佳实践

### 团队入门

向团队推行内置规则时：

- 先启用所有规则，建立基线
- 一起审查违规情况，并就哪些规则适用达成一致
- 记录为何禁用特定规则
- 针对组织特定需求添加自定义规则

### 模型维护

- 在将更改提交到版本控制之前运行 BPA
- 立即修复高严重性违规项
- 定期审查中、低严重性问题
- 在可用时使用自动修复功能

### 自定义规则

- 不要重复实现内置规则的功能
- 使用不同的 ID 前缀以避免冲突
- 为自定义规则编写文档
- 在团队内共享规则集

## 故障排除

### 内置规则未显示

如果 BPA 窗口中未显示内置规则：

1. 确认你正在使用 Tabular Editor 3 企业版
2. 确认已在 **工具** > **偏好** > **Best Practice Analyzer** 中启用内置规则
3. 如果你刚更改了偏好，重启 Tabular Editor
4. 确认你的许可证处于激活状态

### 无法修改内置规则

这是正常现象。 内置规则为只读。 如果你需要不同的逻辑，请使用你的表达式创建自定义规则，并禁用对应的内置规则。

### ID 冲突错误

内置规则会保留某些 ID 前缀。 选择一个不以 `TE3_BUILT_IN` 开头的其他 ID。

## 兼容性

- 需要 Tabular Editor 3.24.0 或更高版本
- 仅限企业版
- 适用于所有兼容级别（1200+）

## 下一步

- [使用 Best Practice Analyzer](xref:using-bpa)
- [BPA 示例规则与表达式](xref:using-bpa-sample-rules-expressions)
- [自定义 BPA 规则](xref:best-practice-analyzer)