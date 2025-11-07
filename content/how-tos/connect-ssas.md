---
uid: connect-ssas
title: Connect & Deploy to SSAS
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

## Connect/deploy to SSAS Tabular Databases
Hitting CTRL+SHIFT+O lets you open a Tabular Model directly from a Tabular Database that has already been deployed. Enter the server address and (optionally) provide a username and password. After hitting "OK", you will be prompted with a list of databases and the server. Select the one you want to load, and click "OK" again. 

![](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/Connect.png)

The dialog shown also lets you connect to Azure Analysis Services instances, if you provide the full name of the Azure AS instance, starting with "azureas://". The "Local Instance" dropdown, may be used to browse and connect to any running instances of Power BI Desktop or Visual Studio Integrated Workspaces. **Note that although Tabular Editor can make changes to a Power BI model through the TOM, this is not supported by Microsoft and may corrupt your .pbix file. Proceed at your own risk!**

Any time you press CTRL+S after the database has been loaded, the database will be updated with any changes you've made in Tabular Editor. Client tools (Excel, Power BI, DAX Studio, etc.) should be able to immediately view the changes in the database after this. Note that you may need to manually recalculate objects in the model, depending on the changes made, to successfully query the model.

If you want to save the connected model to a Model.bim file, choose "Save As..." from the "File" menu.