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
# Editing a Power BI dataset through the XMLA endpoint

Once a change is made to a Power BI dataset through the XMLA endpoint, it is not be possible to download the dataset as a .pbix file from the Power BI service. 

However with the Power BI Project file it is possible to create a pbix file from the remote model in the following manner. 

![XLMA to PBIX Overview](~/images/power-bi/create-pbix-from-xmla-overview.png)

> [!NOTE]
> The described workaround is not officially supported by Microsoft and as such there is no guarantee that it will work for every model

## Create empty Power BI Project

The first step is to create a new Power BI report and save it as an empty Power BI Project (.pbip) file:

![Save PBIP file](~/images/power-bi/save-pbip-file.png)

This will create a folder structure containing an empty model file that will be overwritten later to move the XMLA endpoint semantic model to Power BI

![PBIP with Model file](~/images/power-bi/pbip-file-bim-model.png)

Close Power BI desktop afterwards.

## Open and Save Model into Power BI Project

With Tabular Editor open the XMLA endpoint and load the semantic model into the tool. 

Using "File > Save As" navigate to the Power BI Project folder and overwrite the model file shown above. 

This will save the remote model into the Power BI Project that will now contain the model metadata.

![PBIP with Tables](~/images/power-bi/pbip-includes-tables.png)

## Save to pbix

The next step is to save the Power BI project to a .pbix using File > Save As in Power BI Desktop.

Once the file is saved, the data inside the newly created .pbix file can be refreshed accordingly.
