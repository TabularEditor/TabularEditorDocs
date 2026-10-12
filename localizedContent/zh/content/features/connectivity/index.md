---
uid: connectivity
title: 连接
author: Morten Lønskov
updated: 2026-09-21
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 连接

Tabular Editor 3 可连接到两类不同的对象，而它们的身份验证方式也不同。

- **你正在编辑的模型** 位于 Analysis Services、Azure Analysis Services 或 Power BI 或 Fabric Workspace 中，并通过 XMLA 连接访问。参见 @xmla-as-connectivity。
- **模型导入数据所用的数据源**，通过 [表导入向导](xref:import-tables) 访问。以下页面介绍的就是这一部分内容。

## 凭据存放位置

凭据会按用户和模型分别存储在 [用户选项](xref:user-options) 文件（`.tmuo`）中，并使用你的 Windows 帐户密钥进行加密。它们不属于模型元数据，也绝不会进入源代码管理。参见 @supported-files。

这会带来一个需要事先了解的结果：同事打开同一个模型时需要提供他们自己的凭据；同一个人换到另一台计算机上也是如此。

## 旧版、结构化和隐式数据源

可用的身份验证方式还取决于模型如何存储数据源；这一点由模型决定，而不是由你决定。

- **旧版（提供程序）** 数据源对所有模型都可用，与其兼容级别无关。凭据存储在服务器端的 Tabular Object Model 中。
- **结构化（Power Query）** 数据源在兼容级别 1400 及以上可用。每次部署到 Analysis Services 时，都必须重新提供凭据。
- **隐式** 数据源是 Power BI 和 Fabric 模型使用的类型，而 Direct Lake 模型只能使用这种类型。元数据中根本没有数据源对象：分区中的 M 表达式会指定数据源，凭据则由 Power BI Desktop 或 Power BI 服务保存，而不是由模型保存。

当多种类型都可用时，向导会优先选择隐式，其次是结构化，最后是旧版。

这也是为什么在 Power BI 之外，数据源列表会更短。 Snowflake、Databricks 和 Power BI Dataflow 只能作为隐式数据源访问，因此当模型位于 Analysis Services 上时，向导不会将它们列出。请参阅 [TOM 数据源类型](xref:import-tables#types-of-tom-data-sources)。

无论模型最终采用哪一种，_Tabular Editor_ 用于浏览数据源并读取其架构的凭据，都是你在连接对话框中输入的那些，并会保存在上面提到的 `.tmuo` 文件中。这些凭据与 Analysis Services 或 Power BI 在刷新时使用的凭据相互独立。
