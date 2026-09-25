---
uid: powerbi-xmla-pbix-workaround
title: 从 XMLA endpoint 创建 PBIX 文件。
author: Morten Lønskov
updated: 2026-09-11
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          partial: true
          note: "仅限高级每用户 XMLA 终结点"
        - edition: Enterprise
          full: true
---

# 使用 XMLA endpoint 将 Power BI Dataset 下载为 .pbix 文件

一旦通过 XMLA endpoint 对 Power BI 语义模型进行了更改，就无法再从 Power BI 服务将该模型下载为 .pbix 文件。

不过，借助 Power BI Project 文件，你可以按下述三个步骤，从远程模型创建一个 .pbix 文件。

![XLMA to PBIX Overview](~/content/assets/images/power-bi/create-pbix-from-xmla-overview.png)

> [!NOTE]
> The described workaround isn't officially supported by Microsoft. There's no guarantee that it works for every model. 具体而言，如果你添加了自定义分区或其他[此处列出的](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-external-tools#data-modeling-operations)对象，Power BI Desktop 可能无法通过这种方式正确打开该文件。 See below for a script to handle incremental refresh partitions.

## 步骤 1：创建并保存一个空的 Power BI Project（.pbip）文件

第一步是新建一个 Power BI Report，并将其保存为空的 Power BI Project（.pbip）文件，如下图所示。

![Save PBIP file](~/content/assets/images/power-bi/save-pbip-file.png)

这会创建一个文件夹结构，其中包含一个空的 _model_ 文件。 This _model_ file contains the model metadata. You'll overwrite this metadata in the next step with the metadata of the published model that you want to save to .pbix.

![PBIP with Model file](~/content/assets/images/power-bi/pbip-file-bim-model.png)

关闭 Power BI Desktop，然后在 Tabular Editor 中继续下一步操作。

## 步骤 2：使用 Tabular Editor 打开 XMLA 模型

在 Tabular Editor 打开后，通过 XMLA endpoint 连接到 Fabric Workspace。 Load the Power BI semantic model you want to convert to a .pbix.

## 步骤 3：将 XMLA 模型保存为 .pbip

在 Tabular Editor 中，选择 _文件 > 另存为..._，然后导航到 Power BI Project 文件夹。 Overwrite the _model.bim_ file shown in the previous diagram.

这样会把远程模型保存到 Power BI Project 中，现在这个项目会包含模型元数据。

If the .pbip folder is configured to store the model as [TMDL](xref:tmdl) files, you will need to use the Save To Folder option in Tabular Editor instead. 然后导航到该语义模型的 Power BI Project 文件夹（ModelName.SemanticModel），打开 'definition' 文件夹，并将模型保存到该文件夹中。

> [!NOTE]
> 若要启用 TMDL，请依次转到 **Tools > 偏好 > File Formats > Save-to-folder**，并在 **Serialization mode** 下拉列表中选择“TMDL”。 See [TMDL documentation for more information](xref:tmdl)

## 步骤 3.1：移除增量刷新的分区并创建新的分区（可选）

使用下面的 Convert Incremental Refresh 脚本删除增量刷新分区，并为每个表创建一个包含增量刷新中使用的表达式的单一分区。

## 步骤 4：保存为 .pbix 并在 Power BI Desktop 中打开该文件

![包含表的 PBIP](~/content/assets/images/power-bi/pbip-includes-tables.png)

打开 .pbip 后，Power BI Report 现在会包含 XMLA endpoint 语义模型。

在 Power BI Desktop 中使用 _文件 > 另存为..._ 将其保存为 .pbix。

## 重新水合 .pbix

该 .pbix 现已包含发布到 Fabric Workspace 的模型。 When you open the .pbix, you can _re-hydrate_ the file, meaning that you load the data based on the connections specified in the model.

## 转换增量刷新分区

如果语义模型启用了增量刷新，上述步骤 4 将会失败，因为 Power BI Desktop 模型不支持包含多个分区。
In this case the following script should be run against the model to convert incremental refresh partitions into single partitions

```csharp
foreach (var t in Model.Tables)
{
    if(t.EnableRefreshPolicy)
    {
        //We will collect the SourceExpression from the Incremental Refresh Source Expression of the table
        string m_expression = t.SourceExpression.ToString();
         
        //We will generate a new partition name
        string partition_name = t.Name + "-" + Guid.NewGuid();

        //Now we will create a new partition
        var partition = t.AddMPartition(partition_name, m_expression);
        partition.Mode = ModeType.Import;
        
        //Next we will delete all the incremental refresh partitions of the table
        foreach (var p in t.Partitions.OfType<PolicyRangePartition>().ToList())
        {
            p.Delete();
        }
    }
};
```

感谢 [Micah Dail](https://twitter.com/MicahDail) 编写该脚本，并建议将其纳入本文档。
