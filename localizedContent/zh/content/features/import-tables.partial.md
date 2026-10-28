---
uid: import-tables
title: 导入表格
author: Morten Lønskov
updated: 2026-10-12
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
Tabular Editor 3 中的**表导入向导**会在您的模型中创建数据源，并从 SQL Server 数据库等关系源导入表和视图。

![表导入向导](~/content/assets/images/import-tables-wizard.png)

## TOM 数据源的类型

模型元数据中可用的数据源类型取决于您的 Analysis Services 版本：

- **提供程序（旧版）**：在每个版本的 Analysis Services 和每个兼容级别中均可用。支持有限的源范围，主要通过 OLE DB 和 ODBC 驱动程序支持关系源。分区通常是对源本机执行的 SQL 语句。凭据在 Tabular Object Model 的提供程序数据源对象中进行管理，并在服务器端进行存储和加密。
- **结构化（Power Query）**：自 SQL Server 2017 起可用（兼容级别为 1400 及以上）。支持比提供程序数据源更多的源。分区通常是 M（Power Query）表达式。凭据在 Tabular Object Model 的 Structured 数据源对象中进行管理，您在每次部署到 Analysis Services 时都需要再次指定凭据。
- **隐式**：仅供 Power BI 语义模型使用。模型没有数据源对象，M (Power Query) 表达式定义了数据源。Power BI Desktop 或 Power BI 服务管理凭据，而 Tabular Object Model 不存储凭据。

> [!NOTE]
> Tabular Editor 2.x 中的“表导入向导”和“更新表架构”仅支持具有 SQL 分区的旧版数据源，不支持 Power Query 分区。如果模型的开发人员也使用 Tabular Editor 2.x，请使用旧版数据源。

## 导入新表格

**模型 > 导入表格…**列出了新数据源的上述数据源类型，然后是模型中已存在的数据源。如果可以通过现有数据源使用要导入的表，请选择该数据源。

> [!TIP]
> 语义模型通常是关系数据仓库的内存缓存。在可能的情况下，为模型提供一个指向基于 SQL 的数据仓库或数据超市的单个数据源。

## 创建新的数据源

当你创建新的数据源时，向导会列出 Tabular Editor 3 支持的数据源：

![创建新源](~/content/assets/images/create-new-source.png)

Analysis Services 和 Power BI 支持的源比此列表中的更多。该列表包含 Tabular Editor 直接连接以导入表元数据（列名和数据类型）的源。对于其他源，Tabular Editor 3 可以[通过 Analysis Services 更新表格架构](#updating-table-schema-through-analysis-services)。

每个源都有自己的连接对话框和身份验证选项，这些内容在其页面上有记录，包括哪些选项会打开交互式登录。标记为*仅隐式*的数据源仅在 Power BI 模型中可用作隐式数据源，而不在 SSAS 或 Azure AS 中可用。有关凭据的存储和使用方式，请参阅 @connectivity。

- SQL Server 数据库、Azure SQL 数据库和 Azure Synapse Analytics（SQL 池和无服务器 SQL 池）：@connect-sql-server
- Oracle： @connect-oracle
- ODBC，包括 PostgreSQL、MySQL、MariaDB 和 IBM Db2：@connect-odbc
- OLE DB：@connect-oledb
- Snowflake，仅限隐式，包括密钥对身份验证： @connect-snowflake
- Power BI 数据流，仅限隐式：@connect-dataflows
- Databricks，仅限隐式： @connect-databricks 和教程[连接到 Azure Databricks](xref:connecting-to-azure-databricks)
- Microsoft Fabric Lakehouse、Microsoft Fabric Warehouse、Microsoft Fabric SQL 数据库和 Microsoft Fabric 镜像数据库： @connect-onelake

连接对话框会获取源的服务器地址、凭据和其他设置。Tabular Editor 使用这些设置来建立自身与源的连接，并按用户和模型将它们保存在您的 @user-options 文件中。凭据使用您 Windows 用户帐户下的 Windows 数据保护 API 进行加密，绝不会成为模型元数据的一部分。

![SQL 身份验证](~/content/assets/images/sql-auth.png)

要为 Analysis Services 提供不同的凭据，请在导入表格后编辑 Tabular Object Model 中的数据源属性。

## 选择要导入的对象

定义数据源后，请从列表中选择表和视图，或编写要对源运行的本机查询。

![源选项](~/content/assets/images/source-options.png)

使用第一个选项，Tabular Editor 将连接到源并列出其表和视图，您可以在下一页预览这些表和视图：

![选择源对象](~/content/assets/images/choose-source-objects.png)

在左侧选择多个表和视图，以便一次性导入。对于每个表/视图，选择或取消选择要导入的列。

> [!TIP]
> 如果您控制源，请在要导入的每个表格之上创建一个视图。在视图中，更正语义模型使用的名称和拼写，并删除其不需要的列，例如系统列和时间戳。
>
> 在模型中，从视图导入所有列，这将生成 `SELECT * FROM ...` 语句。当源发生变化时，Tabular Editor 中的**更新表格架构...**会显示发生了哪些变化。

![高级导入](~/content/assets/images/advanced-import.png)

当您在左上角的下拉菜单中将预览模式设置为**仅架构**时，您可以更改每个源列的导入数据类型和列名称。例如，将浮点源值导入为定点小数。

![确认选择](~/content/assets/images/confirm-selection.png)

在最后一页上，确认您的选择，并选择要创建的分区类型。对于提供程序数据源，默认值为 `SQL`；对于 Structured数据源，默认值为 `M`。

![确认选择 Direct Lake](~/content/assets/images/confirm-selection-direct-lake.png)

对于 Fabric 数据源，最后一页上的下拉菜单用于设置是在 Direct Lake 模式还是在导入模式下创建所选内容。

向导将创建包含所有列、数据类型和源列映射的表。列将按其在源表中的显示顺序创建：

![导入完成](~/content/assets/images/import-complete.png)

> [!NOTE]
> 从**Microsoft Fabric 湖仓**或**Microsoft Fabric 仓库**导入的表格通过数据源的 SQL 分析端点读取其架构。如果 Tabular Editor 无法确定端点，且导入设置未指定端点，则会显示一条错误消息，指出缺少的内容：作为服务器的 SQL 端点，或工作区 ID 和项目 ID。在这种情况下，Tabular Editor 不会创建没有列的表。

## 更新表格架构

**更新表格架构…**会在源中添加或更改列后，或者在您修改分区表达式或查询后，更新模型中的列元数据。

![更新表架构](~/content/assets/images/update-table-schema.png)

在模型、所选表或单个分区上运行此操作。

Tabular Editor 连接到相关数据源，根据需要提示输入凭据，并确定要添加、修改或删除的列。更新后，列将保持源列的顺序。

> [!IMPORTANT]
> 如果导入到语义模型的列在源中被删除或重命名，请更新表格架构。在您执行此操作之前，数据刷新将失败。

![架构比较对话框](~/content/assets/images/schema-compare-dialog.png)

在上面的截图中，Tabular Editor 检测到两个尚未导入的新源列（`Color` 和 `Material`），并标记了两个要删除的现有列（`Colour` 和 `Substance Type`），因为它们的名称不再与源列匹配。重命名检测仅适用于简单更改。在这里，在源中，`Colour` 被重命名为 `Color`，`Substance Type` 被重命名为 `Material`，但名称差异较大，以至于 Tabular Editor 将每次重命名都报告为一次删除和一次添加。

按住 **Ctrl** 键，在“架构更改”对话框中选择`Color`（导入）和`Colour`（移除）行，然后右键单击，将移除和添加合并为单个 SourceColumn 更新。引用 `[Colour]` 的现有 DAX 公式仍可正常工作：

![合并 Sourcecolumn 更新](~/content/assets/images/combine-sourcecolumn-update.png)

如果您只想更新 `SourceColumn` 属性并保留导入列的名称，请在下拉列表中清除 `Name` 更新操作：

![取消选择名称](~/content/assets/images/deselect-name.png)

## 通过 Analysis Services 更新表格架构

默认情况下，Tabular Editor 3 直接连接到数据源以更新导入的表架构，这仅适用于 Tabular Editor 3 支持的数据源。在**工具 > 偏好 > 架构比较**下启用**使用 Analysis Services 进行更改检测**，以更新来自不受支持源的表的架构。该选项还涵盖分区和共享表达式，其 M 对于内置架构检测来说过于复杂，例如使用其不支持的 M 函数的表达式。

![通过 AS 更新表架构](~/content/assets/images/update-table-schema-through-as.png)

启用此选项且 Tabular Editor 3 连接到 Analysis Services 或 Power BI XMLA endpoint 时，您可以更新从 Analysis Services 或 Power BI 支持的**任何**数据源导入的表的架构。

> [!TIP]
> [工作区模式](xref:workspace-mode)使 Tabular Editor 3 在您进行开发时保持连接到 Analysis Services 或 Power BI XMLA endpoint。

启用此选项后，架构更新将执行以下步骤：

1. Tabular Editor 3 对已连接的 Analysis Services 实例启动事务。
2. 它向模型添加一个临时表，其中包含一个 Power Query 分区表达式，该表达式通过 [`Table.Schema` M 函数](https://docs.microsoft.com/powerquery-m/table-schema)返回原始表达式的架构。
3. Analysis Services 刷新临时表，连接到数据源以检索架构。
4. Tabular Editor 3 查询临时表以获取架构元数据。
5. Tabular Editor 3 回滚事务，使 Analysis Services 数据库或 Power BI 语义模型恢复到步骤 1 之前的状态。
6. 如果架构发生更改，则会显示上图所示的**应用架构更改**对话框。

> [!NOTE]
> 如果您的 M 表达式组合来自多个源的数据（例如通过 M [`Table.NestedJoin`](https://learn.microsoft.com/powerquery-m/table-nestedjoin) 函数），您可能需要将 Power BI 服务中语义模型的[**隐私级别**](https://powerbi.microsoft.com/blog/privacy-levels-for-cloud-data-sources/)从“私有”更改为“组织”。否则，您可能会看到一个错误，指出`<Query> references other queries or steps, so it may not directly access a data source. Please rebuild this data combination.`。即使未启用**使用 Analysis Services 进行更改检测**，也可能出现此错误，因为当 M 表达式对于 Tabular Editor 3 的内置架构检测来说过于复杂时，Tabular Editor 3 将自动回退到此检测机制。

### 通过 Analysis Services 导入新表

要从向导不支持的源导入表，请从该源复制现有表，并修改副本分区的 M 表达式。将更改保存到工作区数据库，然后按照上述说明更新表格架构。
