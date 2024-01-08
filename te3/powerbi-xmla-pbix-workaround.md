---
uid: powerbi-xmla-pbix-workaround
title: Creating PBIX File from XMLA Endoint.
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

Once a change is made to a Power BI semantic model through the XMLA endpoint, it's not possible to download the dataset as a .pbix file from the Power BI service. 

However, with the Power BI Project file, it's possible to create a .pbix file from the remote model by following the three-step process, which is described as follows. 

![XLMA to PBIX Overview](~/images/power-bi/create-pbix-from-xmla-overview.png)

> [!NOTE]
> The described workaround isn't officially supported by Microsoft. There's no guarantee that it works for every model. Specifically, if you've added custom partitions or other objects [not listed here](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-external-tools#data-modeling-operations), Power BI Desktop may not be able to correctly open the file following this approach.

## Step 1: Create and save an empty Power BI projects (.pbip) file

The first step is to create a new Power BI report and save it as an empty Power BI Project (.pbip) file, as depicted in the following diagram.

![Save PBIP file](~/images/power-bi/save-pbip-file.png)

This creates a folder structure that contains an empty _model_ file. This _model_ file contains the model metadata. You'll overwrite this metadata in the next step with the metadata of the published model that you want to save to .pbix.

![PBIP with Model file](~/images/power-bi/pbip-file-bim-model.png)

Close Power BI desktop, and proceed with the next step in Tabular Editor.

## Step 2: Open XMLA model with Tabular Editor and save the model as .pbip

With Tabular Editor open, connect to the Fabric workspace via the XMLA endpoint. Load the Power BI semantic model you want to convert to a .pbix. 

## Step 3: Save XMLA model into .pbip

In Tabular Editor using _File > Save as..._, navigate to the Power BI Project folder. Overwrite the _model.bim_ file shown in the previous diagram. 

This will save the remote model into the Power BI Project that will now contain the model metadata.


## Step 4: Save to .pbix and open this file in Power BI Desktop

![PBIP with Tables](~/images/power-bi/pbip-includes-tables.png)

Open the .pbip and the Power BI report will now contain the XMLA endpoint semantic model.

Save it to a .pbix using _File > Save As..._ in Power BI Desktop.

## Re-hydrate .pbix
The .pbix now contains the model that was published to the Fabric workspace. When you open the .pbix, you can _re-hydrate_ the file, meaning that you load the data based on the connections specified in the model.
