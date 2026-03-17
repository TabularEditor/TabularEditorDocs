---
uid: powerbi-xmla-pbix-workaround
title: 从 XMLA endpoint 创建 PBIX 文件。
author: Morten Lønskov
updated: 2023-10-18
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: 桌面版
          none: true
        - edition: 商业版
          partial: true
          note: "仅适用于 Premium Per User 的 XMLA endpoint"
        - edition: 企业版
          full: true
---

# 使用 XMLA endpoint 将 Power BI Dataset 下载为 .pbix 文件

一旦通过 XMLA endpoint 对 Power BI 语义模型进行了更改，就无法再从 Power BI 服务将该模型下载为 .pbix 文件。

不过，借助 Power BI Project 文件，你可以按下述三个步骤，从远程模型创建一个 .pbix 文件。

![XLMA to PBIX Overview](~/content/assets/images/power-bi/create-pbix-from-xmla-overview.png)

> [!NOTE]
> 本文所述的变通方法并非 Microsoft 官方支持。 无法保证它对每个模型都有效。 特别是，如果你添加了自定义分区或其他 [此处列出的](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-external-tools#data-modeling-operations) 对象，Power BI Desktop 可能无法按此方式正确打开该文件。 下方提供了一个脚本，用于处理增量刷新分区。

## 步骤 1：创建并保存一个空的 Power BI Project（.pbip）文件

第一步是新建一个 Power BI Report，并将其保存为空的 Power BI Project（.pbip）文件，如下图所示。

![Save PBIP file](~/content/assets/images/power-bi/save-pbip-file.png)

这会创建一个文件夹结构，其中包含一个空的 _model_ 文件。 该 _model_ 文件包含模型元数据。 在下一步中，你将用要保存为 .pbix 的已发布模型的元数据覆盖这些元数据。

![PBIP with Model file](~/content/assets/images/power-bi/pbip-file-bim-model.png)

关闭 Power BI Desktop，然后在 Tabular Editor 中继续下一步操作。

## 步骤 2：使用 Tabular Editor 打开 XMLA 模型

打开 Tabular Editor 后，通过 XMLA endpoint 连接到 Fabric Workspace。 加载要转换为 .pbix 的 Power BI 语义模型。

## 步骤 3：将 XMLA 模型保存为 .pbip

在 Tabular Editor 中使用 _文件 > 另存为..._，导航到 Power BI Project 文件夹。 覆盖上一张图中显示的 _model.bim_ 文件。

这样会把远程模型保存到 Power BI Project 中，现在这个项目会包含模型元数据。

如果 .pbip 文件夹配置为将模型存储为 [TMDL](xref:tmdl) 文件，你就需要改用 Tabular Editor 里的“保存到文件夹”选项。 然后转到该语义模型的 Power BI Project 文件夹（ModelName.SemanticModel），打开“definition”文件夹，并把模型保存在那里。

> [!NOTE]
> 若要启用 TMDL，请转到 **Tools > 偏好 > File Formats > Save-to-folder**，并在 **Serialization mode** 下拉列表中选择 "TMDL"。 有关详细信息，请参阅 [TMDL 文档](xref:tmdl)

## 步骤 3.1：移除增量刷新的分区并创建新的分区（可选）

使用下面的 Convert Incremental Refresh 脚本删除增量刷新分区，并为每个表创建一个包含增量刷新中使用的表达式的单一分区。

## 步骤 4：保存为 .pbix 并在 Power BI Desktop 中打开该文件

![包含表的 PBIP](~/content/assets/images/power-bi/pbip-includes-tables.png)

打开 .pbip 后，Power BI Report 现在会包含 XMLA endpoint 语义模型。

在 Power BI Desktop 中使用 _文件 > 另存为..._ 将其保存为 .pbix。

## 重新水合 .pbix

这个 .pbix 现在包含已发布到 Fabric Workspace 的模型。 打开 .pbix 后，可以对该文件进行 _重新水合_，也就是根据模型中指定的连接来加载数据。

## 转换增量刷新分区

如果语义模型启用了增量刷新，上述步骤 4 将失败，因为 Power BI Desktop 模型不能包含多个分区。
在这种情况下，应针对该模型运行以下脚本，将增量刷新分区转换为单一分区

```csharp
foreach (var t in Model.Tables)
{
    if(t.EnableRefreshPolicy)
    {
        //我们将从表的增量刷新源表达式中收集 SourceExpression
        string m_expression = t.SourceExpression.ToString();
         
        //我们将生成一个新的分区名称
        string partition_name = t.Name + "-" + Guid.NewGuid();

        //现在我们将创建一个新的分区
        var partition = t.AddMPartition(partition_name, m_expression);
        partition.Mode = ModeType.Import;
        
        //接下来我们将删除该表的所有增量刷新分区
        foreach (var p in t.Partitions.OfType<PolicyRangePartition>().ToList())
        {
            p.Delete();
        }
    }
};
```

感谢 [Micah Dail](https://twitter.com/MicahDail) 编写该脚本，并建议将其纳入本文档。
