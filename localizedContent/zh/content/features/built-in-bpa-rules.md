---
uid: built-in-bpa-rules
title: 内置 BPA 规则
author: Morten Lønskov
updated: 2026-11-13
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
description: 36 条精选最佳做法规则硬编码到 Tabular Editor 3 中，并集成知识库。
---

# 内置 BPA 规则

## 概览

Tabular Editor 3 包含 36 条内置最佳做法规则。这些规则涵盖了语义模型开发中的常见问题，并会在每个版本发布时自动更新。

与存储在 JSON 文件中的自定义规则不同，内置规则：

- 直接集成在应用程序中
- 随新版本发布自动更新
- 链接到知识库文档
- 为确保各团队之间一致性，这些规则为只读
- 无需配置即可立即使用

## 主要功能

### 规则类别

**Best Practice Analyzer** 按类别对内置规则进行分组：
- **错误预防**：无效字符、缺失的表达式和源列、数据类型不匹配、MDX 可用性、用户定义函数名称
- **性能**：MDX 可用性、日期表、多对多关系、连接字符串应用程序名称
- **维护**：说明、空计算组和透视、未使用的数据源
- **命名约定**：名称中的前导空格和尾随空格
- **格式化**：格式字符串、数值列的汇总、外键可见性
- **模型布局**：翻译
- **治理**：Power BI 兼容级别
- **安全性**：角色权限以及行级和对象级安全的组合

### 全局控制与按规则控制
![“管理最佳实践规则”对话框，其中选择了“内置最佳实践”集合，并且其规则按类别分组，每个类别都有一个复选框](~/content/assets/images/features/bpa-built-in-rules-preferences.png)
您可以全局或单独启用或禁用内置规则。设置在各会话中保持不变，并独立于您的自定义规则。

要管理内置规则：
1. 转到**工具 > 首选项 > Tabular Editor > 其他**。
2. 在**最佳实践分析器**下，选中或取消选中**启用内置最佳实践规则**，以启用或禁用整个集合。
3. 要启用或禁用个别规则，请打开**工具 > 管理BPA规则...**，选择**内置最佳实践**集合，然后选中或取消选中每条规则的复选框。

### 首次运行通知

![首次运行通知对话框屏幕截图：介绍 BPA 内置规则](~/content/assets/images/features/bpa-built-in-rules-notification.png)

升级到包含内置规则的版本后，你首次打开模型时，会看到一条通知，说明该功能，并提供前往“偏好”的链接。此通知只会出现一次。

### 知识库集成


![Best Practice Analyzer 窗口，其中显示了一条规则的工具提示，并突出显示了“了解更多”链接](~/content/assets/images/features/bpa-built-in-rules-kb-link.png)

每个内置规则都链接到一篇知识库文章。每篇文章都解释了规则检查的内容、其重要性以及如何解决冲突。

要打开文章，请将鼠标悬停在**最佳实践分析器**窗口中的某条规则上，然后单击工具提示中的**了解详细信息**。

### 只读保护

内置规则无法编辑、克隆或删除。这可确保所有用户使用相同的规则定义。你可以禁用单个规则，但规则定义本身保持不变。

![屏幕截图：BPA 窗口中的内置规则，带有只读标记/图标](~/content/assets/images/features/bpa-built-in-rules-readonly.png)

### 防止 ID 冲突

内置规则使用保留的 ID 前缀。当你创建自定义规则时，Tabular Editor 会验证你的 ID 是否与内置规则冲突；若发生冲突，将显示错误提示。

## 内置规则目录

每个条目均链接到该规则的知识库文章。严重程度显示在括号中。

### 错误预防规则
- [数据列必须有源](xref:kb.bpa-data-column-source) (3)
- [计算对象需要表达式](xref:kb.bpa-expression-required) (3)
- [避免使用结构化数据源的提供程序分区](xref:kb.bpa-avoid-provider-partitions-structured) (2)
- [关系列必须具有相同的数据类型](xref:kb.bpa-relationship-same-datatype) (3)
- [避免在对象名称中使用无效字符](xref:kb.bpa-avoid-invalid-characters-names) (3)
- [避免在描述中使用无效字符](xref:kb.bpa-avoid-invalid-characters-descriptions) (3)
- [在必要时将 IsAvailableInMDX 设置为 True](xref:kb.bpa-set-isavailableinmdx-true-necessary) (3)
- [对用户定义函数使用复合名称](xref:kb.bpa-udf-use-compound-names) (1)

### 性能规则
- [将 IsAvailableInMDX 设置为 False](xref:kb.bpa-set-isavailableinmdx-false) (3)
- [应存在日期表](xref:kb.bpa-date-table-exists) (2)
- [移除自动日期表](xref:kb.bpa-remove-auto-date-table) (2)
- [多对多关系应使用单向](xref:kb.bpa-many-to-many-single-direction) (2)
- [在连接字符串中指定应用程序名称](xref:kb.bpa-specify-application-name) (1)

### 维护规则
- [移除未使用的 হয়ত源](xref:kb.bpa-remove-unused-data-sources) (1)
- [可见对象应有描述](xref:kb.bpa-visible-objects-no-description) (1)：五条规则，适用于表、列、度量值、计算组和用户定义函数
- [透视应包含对象](xref:kb.bpa-perspectives-no-objects) (1)
- [计算组应包含项目](xref:kb.bpa-calculation-groups-no-items) (2)

### 命名约定规则
- [修剪对象名称](xref:kb.bpa-trim-object-names) (1)

### 格式规则
- [将数字列的 SummarizeBy 设置为 None](xref:kb.bpa-do-not-summarize-numeric) (3)
- [隐藏外键列](xref:kb.bpa-hide-foreign-keys) (2)
- [为数字和日期列提供格式字符串](xref:kb.bpa-format-string-columns) (2)
- [为度量值提供格式字符串](xref:kb.bpa-format-string-measures) (2)

### 模型布局规则
- [翻译所有文化的显示文件夹](xref:kb.bpa-translate-display-folders) (1)
- [翻译所有文化的描述](xref:kb.bpa-translate-descriptions) (1)
- [为所有文化翻译可见对象名称](xref:kb.bpa-translate-visible-names) (1)
- [为所有文化翻译层次结构级别名称](xref:kb.bpa-translate-hierarchy-levels) (1)
- [为所有文化翻译透视名称](xref:kb.bpa-translate-perspectives) (1)

### 治理规则
- [对 Power BI 模型使用最新兼容级别](xref:kb.bpa-powerbi-latest-compatibility) (3)

### 安全规则
- [行级和对象级安全性需要读取权限](xref:kb.bpa-role-security-not-enforced) (3)
- [Power BI 角色必须具有读取权限](xref:kb.bpa-powerbi-role-read-permission) (3)
- [没有安全权限的角色覆盖有安全权限的角色](xref:kb.bpa-role-unrestricted-read) (2)
- [避免成员同时具有 RLS 角色和 OLS 角色](xref:kb.bpa-role-mixed-rls-ols-members) (3)

安全规则没有自动修复。

## 使用内置规则和自定义规则

内置规则与自定义规则可并行使用：

| 功能     | 内置规则      | 自定义规则        |
| ------ | --------- | ------------ |
| **存储** | 在应用中硬编码   | JSON 文件或模型注释 |
| **更新** | 随版本发布自动更新 | 需要手动编辑       |
| **修改** | 只读        | 完全可编辑        |
| **文档** | 集成的 KB 文章 | 用户提供的说明      |
| **共享** | 跨团队保持一致   | 需要手动分发       |

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
1. 确认在**工具 > 偏好 > Tabular Editor > 其他**中已选中**启用内置最佳做法规则**
2. 如果你刚更改了偏好，重启 Tabular Editor
3. 确认你的许可证处于激活状态

### 无法修改内置规则

这是正常现象。内置规则为只读。如果你需要不同的逻辑，请使用你的表达式创建自定义规则，并禁用对应的内置规则。

### ID 冲突错误

内置规则会保留某些 ID 前缀。选择一个不以 `TE3_BUILT_IN` 开头的其他 ID。

## 兼容性

内置规则适用于兼容级别为 1200 或更高的模型。某些规则需要更高的级别：同时具有行级安全角色和对象级安全角色的成员的规则需要 1400，用户定义函数的两条规则需要 1702。每篇知识库文章都说明了规则的兼容级别。

## 下一步

- [使用 Best Practice Analyzer](xref:using-bpa)
- [BPA 示例规则与表达式](xref:using-bpa-sample-rules-expressions)
- [自定义 BPA 规则](xref:best-practice-analyzer)