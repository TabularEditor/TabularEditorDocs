---
uid: direct-lake-sql-model
title: Direct Lake on SQL 语义模型
author: Morten Lønskov
updated: 2026-10-12
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          none: true
        - edition: Enterprise
          full: true
---

# Direct Lake 语义模型
Direct Lake on SQL 语义模型通过 SQL 端点直接连接到存储在 [Fabric 中的 OneLake](https://learn.microsoft.com/fabric/onelake/onelake-overview) 中的数据源。 

> [!IMPORTANT]
> 自 [Tabular Editor 3.22.0](../../references/release-notes/3_22_0.md) 起，Tabular Editor 3 支持 Direct Lake on OneLake，在大多数情况下都建议使用此功能。有关详细信息，请参阅我们的[Direct Lake 指南](xref:direct-lake-guidance)文章。

Tabular Editor 3 可以创建此类模型并连接到此类模型。有关这方面的教程，请参阅我们的博客文章：[Direct Lake 语义模型：如何在 Tabular Editor 中使用它们](https://blog.tabulareditor.com/2023/09/26/fabric-direct-lake-with-tabular-editor-part-2-creation/)。 
Tabular Editor 3 可以使用湖仓和数据仓库 SQL 端点创建 Direct Lake 语义模型。 

Tabular Editor 2 可以连接到 Direct Lake 语义模型，但没有任何内置功能可用于创建新表或 Direct Lake 语义模型。这需要手动完成或使用 C# 脚本完成。 

> [!NOTE]
> **Direct Lake 的限制**
> 对 Direct Lake 模型可以进行的更改存在多项限制。请参阅[Direct Lake 的注意事项和限制](https://learn.microsoft.com/fabric/fundamentals/direct-lake-overview#considerations-and-limitations)，了解完整列表。另请参阅[SQLBI 的这篇文章](https://www.sqlbi.com/blog/marco/2024/04/06/direct-lake-vs-import-mode-in-power-bi/)，了解有关在 Direct Lake 和导入模式之间进行选择的概述。

## 在 Tabular Editor 3 中创建 Direct Lake on SQL 模型

在 Tabular Editor 3 (3.15.0 或更高版本) 中创建 Direct Lake on SQL 模型时，必须在“_新建模型_”对话框中通过勾选“Direct Lake”复选框来指定。 

![Direct Lake 新建模型](~/content/assets/images/common/DirectLakeNewModelDialog.png)

使用此复选框可确保设置 Direct Lake 特有属性和批注，并将表的导入限制为 Direct Lake 支持的源。 

> [!NOTE]
> Direct Lake on SQL 模型目前使用的排序规则与常规 Power BI 导入语义模型不同。这可能会导致在查询模型时或在 DAX 代码中引用对象名称时产生不同的结果。
> 有关更多信息，请参阅 Kurt Buhler 的这篇博客文章：[Power BI 中的区分大小写模型：影响和注意事项](https://data-goblins.com/power-bi/case-specific)。

> [!IMPORTANT]
> 自 [Tabular Editor 3.22.0](../../references/release-notes/3_22_0.md) 起，“新建模型”对话框中已删除“Direct Lake”复选框。如果使用 Direct Lake on SQL，您必须[手动设置模型的排序规则，使其与 Fabric 仓库的排序规则相匹配](xref:direct-lake-guidance#collation)。

## 构建新模型和表格导入

Tabular Editor 3（3.15.0 或更高版本）在首次部署时自动对模型进行建模（刷新）。这是为了确保激活 Direct Lake 模式，否则模型将自动回退到 DirectQuery。

此外，在导入新表时，Tabular Editor 3（3.15.0 或更高版本）会在下次保存模型时对其进行构架（刷新）。此首选项位于**工具 > 首选项 > 模型部署 > 数据刷新**下。



## 识别 Direct Lake 模型
Tabular Editor 3 标题栏在模型名称后显示打开的模型的存储模式，例如 **(Direct Lake)**、**(DirectQuery)** 或 **(Import)**。如果模型包含多种表格模式，则标题栏显示 **(复合)**。TOM 资源管理器显示每个表的类型和模式（导入、DirectQuery、双重或 Direct Lake）。Direct Lake on SQL 模型不能包含处于导入、DirectQuery 或双重模式的表。


## 将 Direct Lake 模型转换为导入模式

以下 C# 脚本将现有模型转换为导入模式。如果您的模型的数据延迟要求不需要 Direct Lake，或者您想避免 Direct Lake 模型的限制，但已经开始在 Fabric 中构建一个 Direct Lake 模型，则此操作可能很有用。

当 Tabular Editor 通过 XMLA 端点连接到语义模型时，可以运行该脚本。但是，Microsoft 不支持将更改直接保存回 Power BI/Fabric 工作区。为了规避这个问题，建议的方法是使用“模型 > 部署…”选项。这样，就可以将新转换的模型作为新实体部署到工作区中。

> [!NOTE]
> 部署新转换的导入模式模型后，您需要指定访问 Lakehouse 的凭据，以便将数据刷新到模型中。

### 用于将Direct Lake模型转换为导入模式的C#脚本

```csharp
// **********************************************************************************
// Convert Direct Lake-mode model to Import-mode
// ---------------------------------------------
//
// When this script is executed on a semantic model, it will:
//
//   - Loop through all tables. Any table that contains exactly 1 partition, which
//     is in Direct Lake mode, will have its partition replaced by an equivalent
//     Import-mode partition.
//   - Set the collation of the model to null (default)
// 
// Remarks:
// 
//   - The Import-mode partitions will use the SQL endpoint of the Lakehouse.
//   - The script assumes that the Shared Expression which specifies the SQL endpoint
//     is called "DatabaseQuery".
//   - Because TE2 does not expose the "SchemaName" property on EntityPartition
//     objects, we have to use reflection to access the underlying TOM objects.
//
// Compatibility:
// TE2.x, TE3.x
// **********************************************************************************

using System.Reflection;

const string mImportTemplate = 
@"let
    Source = DatabaseQuery,
    Data = Source{{[Schema=""{0}"",Item=""{1}""]}}[Data]
in
    Data";

foreach(var table in Model.Tables)
{
    // Direct Lake-mode tables only have 1 partition...
    if(table.Partitions.Count != 1) continue;
    
    // ...which should be in "DirectLake" mode:
    var partition = table.Partitions[0];
    if(partition.Mode != ModeType.DirectLake) continue;

    // Tabular Editor unfortunately doesn't expose the SchemaName property of EntityPartitionSources,
    // so we'll have to use reflection to access the underlying TOM object.
    var pMetadataObjct = typeof(Partition).GetProperty("MetadataObject", BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.DeclaredOnly);
    var tomPartition = pMetadataObjct.GetValue(partition) as Microsoft.AnalysisServices.Tabular.Partition;
    var tomPartitionSource = tomPartition.Source as Microsoft.AnalysisServices.Tabular.EntityPartitionSource;
    
    // Table does not have an EntityPartitionSource, meaning it is not a Direct Lake table
    // (shouldn't happen, since we already checked for DirectLake mode above...)
    if(tomPartitionSource == null) continue;
    
    var schemaName = tomPartitionSource.SchemaName;
    var tableName = tomPartitionSource.EntityName;

    // Rename the original (Direct Lake) partition (as we can't have two partitions with the same name):
    var partitionName = partition.Name;
    partition.Name += "_old";
    
    // Add the new (Import) partition:
    table.AddMPartition(partitionName, string.Format(mImportTemplate, schemaName, tableName));
    
    // Delete the old (Direct Lake) partition):
    partition.Delete();
}

// Update model collation:
Model.Collation = null;
Model.DefaultMode = ModeType.Import;
Model.RemoveAnnotation("TabularEditor_DirectLake");
```