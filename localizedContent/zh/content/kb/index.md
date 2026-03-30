# 知识库

本节收录有关 Tabular Editor 和 Power BI 模型的最佳实践、代码分析规则以及 DAX 优化模式的文章。

## 本节包含

### 最佳实践规则 (BPA)

用于构建高质量、易维护的 Power BI 和 Analysis Services 模型的全面指南。

- @kb.bpa-avoid-invalid-characters-descriptions - 通过移除描述中的控制字符，防止元数据损坏
- @kb.bpa-avoid-invalid-characters-names - 确保对象名称仅包含有效字符
- @kb.bpa-data-column-source - 验证所有数据列都有正确的源映射
- @kb.bpa-relationship-same-datatype - 强制关系中的数据类型保持一致
- @kb.bpa-visible-objects-no-description - 确保所有可见对象都有有意义的描述
- @kb.bpa-trim-object-names - 移除名称开头和结尾的空格
- @kb.bpa-expression-required - 验证计算对象是否具有表达式
- @kb.bpa-format-string-columns - 对数值列和日期列应用一致的格式设置
- @kb.bpa-format-string-measures - 为所有度量值提供格式字符串
- @kb.bpa-do-not-summarize-numeric - 防止对数值列进行不恰当的汇总
- @kb.bpa-date-table-exists - 确保日期表配置正确
- @kb.bpa-hide-foreign-keys - 对最终用户隐藏外键列
- @kb.bpa-many-to-many-single-direction - 在多对多关系中强制使用单向筛选
- @kb.bpa-avoid-provider-partitions-structured - 为结构化数据使用正确的分区源
- @kb.bpa-translate-descriptions - 支持多语言描述
- @kb.bpa-translate-display-folders - 本地化显示文件夹名称
- @kb.bpa-translate-hierarchy-levels - 翻译层次结构级别标题
- @kb.bpa-translate-perspectives - 本地化透视名称
- @kb.bpa-translate-visible-names - 为所有区域设置翻译可见对象名称
- @kb.bpa-perspectives-no-objects - 确保透视包含相关对象
- @kb.bpa-calculation-groups-no-items - 验证计算组定义
- @kb.bpa-set-isavailableinmdx-false - 控制对象的 MDX 可用性
- @kb.bpa-set-isavailableinmdx-true-necessary - 按需启用 MDX 可用性
- @kb.bpa-remove-auto-date-table - 清理自动生成的日期表
- @kb.bpa-remove-unused-data-sources - 移除未使用的数据源定义
- @kb.bpa-specify-application-name - 在连接字符串中设置应用程序名称以便监控
- @kb.bpa-powerbi-latest-compatibility - 保持对最新 Power BI 功能的兼容性
- @kb.bpa-udf-use-compound-names - 确保 UDF 名称不会与未来的内置 DAX 函数发生冲突

## 代码操作

### DAX 代码分析（DI）

针对 DAX 代码结构和效率的改进建议。 这些规则有助于你发现简化和优化表达式的机会。 这些规则有助于你发现简化和优化表达式的机会。

- @DI001 - 移除未使用的变量
- @DI002 - 移除未使用的变量
- @DI003 - 移除表名
- @DI004 - 添加表名
- @DI005 - 将表筛选 FILTER 重写为标量谓词
- @DI006 - 将多列筛选 FILTER 拆分为多个筛选 FILTER
- @DI007 - 简化 SWITCH 语句
- @DI008 - 移除多余的 CALCULATE
- @DI009 - 避免使用 CALCULATE 的快捷语法
- @DI010 - 用 MIN/MAX 替代 IF
- @DI011 - 用 ISEMPTY 替代 COUNTROWS
- @DI012 - 用 DIVIDE 替代除法运算
- @DI013 - 用除法运算替代 DIVIDE
- @DI014 - 用 DIVIDE 替换 IFERROR
- @DI015 - 用 DIVIDE 替代 IF

### DAX 重构 (DR)

针对复杂或低效 DAX 模式的重构建议。 针对复杂或低效 DAX 模式的重构建议。 这些规则可帮助你使 DAX 代码更现代化，并提升可读性。

- @DR001 - 转换为标量谓词
- @DR002 - 用聚合函数替代迭代器
- @DR003 - 用 VALUES 替代 SUMMARIZE
- @DR004 - 为变量添加前缀
- @DR005 - 为临时列添加前缀
- @DR006 - 将常量聚合移入变量
- @DR007 - 简化 1 变量代码块
- @DR008 - 简化多变量代码块
- @DR009 - 用 DISTINCTCOUNT 改写
- @DR010 - 用 COALESCE 改写
- @DR011 - 用 ISBLANK 改写
- @DR012 - 移除不必要的 BLANK
- @DR013 - 简化取反逻辑
- @DR014 - 使用 IN 简化

### DAX 改写 (RW)

针对可用替代语法更有效表达的特定 DAX 模式，提供改写建议。

- @RW001 - 使用 CALCULATE 改写 TOTALxTD
- @RW002 - 使用 FILTER 改写
- @RW003 - 反转 IF 逻辑

---
