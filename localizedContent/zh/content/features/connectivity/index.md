---
uid: connectivity
title: 连接
author: Morten Lønskov
updated: 2026-09-23
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

Tabular Editor 3 会分别对这些连接进行身份验证：

- **你编辑的语义模型**，位于 SQL Server Analysis Services、Azure Analysis Services，或通过 XMLA 访问的 Power BI 或 Fabric Workspace 中。参见 @xmla-as-connectivity 和 @connect-ssas。
- **模型导入数据所用的数据源**，通过 [表导入向导](xref:import-tables) 连接。本节中的页面介绍这些连接。

## 数据源

每种数据源都有自己的连接对话框：

- @connect-sql-server：SQL Server、Azure SQL Database、Azure SQL Managed Instance 和 Azure Synapse Analytics
- @connect-snowflake：Snowflake，包括密钥对身份验证
- @connect-databricks：Azure Databricks 和其他云上的 Databricks
- @connect-oracle：通过 Oracle OLE DB 提供程序连接 Oracle 数据库
- @connect-odbc：任何具有 ODBC 驱动程序的数据源，包括 PostgreSQL、MySQL、MariaDB 和 IBM Db2
- @connect-oledb：任何具有 OLE DB 提供程序的数据源
- @connect-onelake：Fabric Lakehouse、Warehouse、SQL 数据库和镜像数据库项
- @connect-dataflows：Power BI Dataflow

## 凭据存储位置

Tabular Editor 会将你在连接对话框中输入的连接设置和凭据保存在 [用户选项](xref:user-options) 文件 (`.tmuo`) 中。该文件按用户和模型分别存储，其中的凭据会在你的 Windows 用户账户下使用 Windows Data Protection API 加密。参见 @supported-files。

- 这些凭据不属于模型元数据，也不会提交到源代码管理。
- 每位用户都需要在每台计算机上提供自己的凭据。
- 生成的 M 表达式不包含凭据。

## 凭据的用途

在你导入表、预览数据和更新表架构时，Tabular Editor 会使用连接对话框中的凭据连接到数据源。如果所选身份验证选项不支持交互式登录，Tabular Editor 会直接使用已保存的凭据进行连接，而不会提示。

Analysis Services 和 Power BI 中的数据刷新使用的是在服务器或 Power BI 服务中为模型里的数据源配置的凭据。导入表后，你需要在数据源属性中设置 Analysis Services 使用的凭据（请参阅[创建新数据源](xref:import-tables#creating-a-new-data-source)）。

## 旧版、结构化和隐式数据源

向导中可用的数据源类型取决于模型：

- **旧版（提供程序）** 数据源适用于除 Direct Lake 模型之外的所有模型。凭据在 Tabular Object Model (TOM) 中的 Provider数据源对象内进行管理，并在服务器端存储并加密。
- **结构化（Power Query）** 数据源在兼容级别 1400 及以上可用。每次部署到 Analysis Services 时，你都需要重新提供凭据。
- **隐式** 数据源适用于 Power BI 和 Fabric 模型。 Direct Lake 模型仅使用隐式数据源。使用隐式数据源时，模型没有数据源对象：导入分区带有用于命名数据源的 M 表达式，Direct Lake 分区引用共享表达式，而凭据由 Power BI Desktop 或 Power BI 服务保存。

当模型没有数据源时，如果可用，向导会预先选择隐式，然后是结构化，最后是旧版。

Snowflake、Databricks 和 Power BI Dataflow 仅可作为隐式数据源使用。对于不支持隐式数据源的模型（例如 Analysis Services 模型），向导会隐藏这些选项（请参阅[Tom 数据源的类型](xref:import-tables#types-of-tom-data-sources)）。
