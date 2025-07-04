---
uid: powerbi-xmla-pbix-workaround
title: Creating PBIX File from XMLA Endpoint.
author: Morten Lønskov
updated: 2023-10-18
applies_to:
  editions:
    - edition: Desktop
      none: x
    - edition: Business
      partial: Tabular Editor 3 Business Edition only allows connecting to the XMLA endpoint of Premium-Per-User (PPU) workspaces.
    - edition: Enterprise
---
# Downloading a Power BI dataset to a .pbix using the XMLA endpoint

Once a change is made to a Power BI semantic model through the XMLA endpoint, it's not possible to download the model as a .pbix file from the Power BI service. 

However, with the Power BI Project file, it's possible to create a .pbix file from the remote model by following the three-step process, which is described as follows. 

![XLMA to PBIX Overview](~/content/assets/images/power-bi/create-pbix-from-xmla-overview.png)

> [!NOTE]
> The described workaround isn't officially supported by Microsoft. There's no guarantee that it works for every model. Specifically, if you've added custom partitions or other objects [listed here](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-external-tools#data-modeling-operations), Power BI Desktop may not be able to correctly open the file following this approach. See below for a script to handle incremental refresh partitions.

## Step 1: Create and save an empty Power BI projects (.pbip) file

The first step is to create a new Power BI report and save it as an empty Power BI Project (.pbip) file, as depicted in the following diagram.

![Save PBIP file](~/content/assets/images/power-bi/save-pbip-file.png)

This creates a folder structure that contains an empty _model_ file. This _model_ file contains the model metadata. You'll overwrite this metadata in the next step with the metadata of the published model that you want to save to .pbix.

![PBIP with Model file](~/content/assets/images/power-bi/pbip-file-bim-model.png)

Close Power BI desktop, and proceed with the next step in Tabular Editor.

## Step 2: Open XMLA model with Tabular Editor

With Tabular Editor open, connect to the Fabric workspace via the XMLA endpoint. Load the Power BI semantic model you want to convert to a .pbix. 

## Step 3: Save XMLA model into .pbip

In Tabular Editor using _File > Save as..._, navigate to the Power BI Project folder. Overwrite the _model.bim_ file shown in the previous diagram. 

This will save the remote model into the Power BI Project that will now contain the model metadata.

If the .pbip folder is configured to store the model as [TMDL](xref:tmdl) files, you will need to use the Save To Folder option in Tabular Editor instead. Then navigate to the Power BI project folder for the semantic model (ModelName.SemanticModel), open the 'definition' folder and save your model there.

> [!NOTE]
> To enable TMDL go to **Tools > Preferences > File Formats > Save-to-folder**, and select "TMDL" in the **Serialization mode** dropdown. See [TMDL documentation for more information](xref:tmdl)

## Step 3.1: Remove incremental refresh partitions and create new (Optional)
Use the Convert Incremental Refresh script below to delete incremental refresh partitions and create a single partition for each table containing the expression used in the incremental refresh expression.

## Step 4: Save to .pbix and open this file in Power BI Desktop

![PBIP with Tables](~/content/assets/images/power-bi/pbip-includes-tables.png)

Open the .pbip and the Power BI report will now contain the XMLA endpoint semantic model.

Save it to a .pbix using _File > Save As..._ in Power BI Desktop.

## Re-hydrate .pbix
The .pbix now contains the model that was published to the Fabric workspace. When you open the .pbix, you can _re-hydrate_ the file, meaning that you load the data based on the connections specified in the model.

## Convert Incremental Refresh partitions
The above step 4 will fail if the semantic model has incremental refresh enabled as a Power BI desktop model cannot contain multiple partitions.
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

Thank you to [Micah Dail](https://twitter.com/MicahDail) for creating the script and suggesting it to be included in this document. 
