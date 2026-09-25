---
uid: direct-lake-sql-model
title: SQL 语义模型上的 Direct Lake
author: Morten Lønskov
updated: 2026-03-27
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

SQL 语义模型上的 Direct Lake 可通过 SQL 端点直接连接到存储在 [Fabric 中的 OneLake](https://learn.microsoft.com/en-us/fabric/onelake/onelake-overview) 中的数据源。

> [!IMPORTANT]
> 自 [Tabular Editor 3.22.0](../../references/release-notes/3_22_0.md) 起，Tabular Editor 3 支持在 OneLake 上使用 Direct Lake，且在大多数情况下建议采用此方式。 See our [Direct Lake guidance](xref:direct-lake-guidance) article for more information.

Tabular Editor 3 can create and connect to this type of model. For a tutorial on this please refer to our blog article: [Direct Lake semantic models: How to use them with Tabular Editor](https://blog.tabulareditor.com/2023/09/26/fabric-direct-lake-with-tabular-editor-part-2-creation/).
Tabular Editor 3 可以通过 Lakehouse 和 Warehouse SQL Endpoint 创建 Direct Lake 语义模型。

Tabular Editor 2 可以连接到 Direct Lake 语义模型，但不提供用于创建新表或 Direct Lake 语义模型的内置功能。 This needs to be done manually or with a C# script.

> [!NOTE]
> **Direct Lake limitations**
> There are several limitations to the changes that can be made to a Direct Lake model. See [Direct Lake Considerations and Limitations](https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview#considerations-and-limitations) for the full list. See also [this article by SQLBI](https://www.sqlbi.com/blog/marco/2024/04/06/direct-lake-vs-import-mode-in-power-bi/) for an overview of choosing between Direct Lake and Import mode.

## 在 Tabular Editor 3 中创建基于 SQL 的 Direct Lake 模型

在 Tabular Editor 3（3.15.0 或更高版本）中创建基于 SQL 的 Direct Lake 模型时，需要在创建模型时于 _New Model_ 对话框中勾选 Direct Lake 复选框进行指定。

![Direct Lake 新建模型](~/content/assets/images/common/DirectLakeNewModelDialog.png)

使用该复选框可确保设置 Direct Lake 特有的属性与注释，并将表的导入限制为 Direct Lake 支持的数据源。

> [!NOTE]
> 基于 SQL 的 Direct Lake 模型当前使用的排序规则与常规 Power BI 导入语义模型不同。 This may lead to different results when querying the model, or when referencing object names in DAX code.
> For more information, see this blog post by Kurt Buhler: [Case-sensitive models in Power BI: consequences & considerations](https://data-goblins.com/power-bi/case-specific).

> [!IMPORTANT]
> As of [Tabular Editor 3.22.0](../../references/release-notes/3_22_0.md), the Direct Lake checkbox has been removed from the New Model dialog. 如果在 SQL 上使用 Direct Lake，你必须[手动将模型的排序规则设置为与 Fabric Warehouse 的排序规则一致](xref:direct-lake-guidance#collation)。

## 为新模型和表导入设定框架

Tabular Editor 3 (3.15.0 or higher) automatically frames (refreshes) the model on first deployment. 这是为了确保启用 Direct Lake 模式；否则模型会自动回退到 DirectQuery。

此外，在导入新表后，Tabular Editor 3（3.15.0 或更高版本）会在你下次保存模型时对模型进行 framing（刷新）。 This preference is located under **Tools > Preferences > Model Deployment > Data Refresh**.

## 识别 Direct Lake 模型

Tabular Editor 顶部的标题栏会显示该 Tabular Editor 实例中当前打开的是哪种类型的模型。 Additionally, the TOM Explorer displays the type and mode of every table (Import, DirectQuery, Dual or Direct Lake). If a model contains a mix of table modes, the title bar will show "Hybrid". Currently, it is not possible for a Direct Lake on SQL model to contain tables in Import, DirectQuery or Dual mode.

## 将 Direct Lake 模型转换为导入模式

The below C# script converts an existing model into Import mode. 如果你的模型对数据延迟的要求不高，无需 Direct Lake，或者你想避开 Direct Lake 模型的限制，但已经在 Fabric 中开始构建 Direct Lake 模型，那么这会很有用。

Running the script is possible when Tabular Editor is connected to a semantic model through the XMLA endpoint. However, saving changes directly back to the Power BI/Fabric workspace is not supported by Microsoft. To circumvent this, the recommended approach is to use the "Model > Deploy..." option. This allows for the deployment of the newly converted model as a new entity in a workspace.

> [!NOTE]
> 部署新转换的导入模式模型后，你需要指定用于访问 Lakehouse 的凭据，才能将数据刷新到模型中。

### 将 Direct Lake 模型转换为导入模式的 C# Script

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