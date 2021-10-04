---
uid: migrate-from-desktop
title: Migrating from Power BI Desktop
author: Daniel Otykier
updated: 2021-09-30
---

# Migrating from Power BI Desktop

If you are already familiar with data modeling concepts in Power BI Desktop, this article is intended to help you migrate your data modeling over to Tabular Editor. Thus, we assume you have a solid understanding of concepts such as the Power Query Editor, imported vs. calculated tables, calculated columns, measures, etc.

## Power BI and Tabular Editor

Historically, Tabular Editor was designed as a tool for SQL Server Analysis Services (Tabular) and Azure Analysis Services developer. When Power BI first launched, there was no supported way for third party tools to access the Analysis Services instance hosting the Power BI data model, and so the only way to create and edit a Power BI dataset, was through Power BI Desktop.

This changed in March 2020, when [Microsoft announced the read/write XMLA endpoint in Power BI Premium](https://powerbi.microsoft.com/en-us/blog/announcing-read-write-xmla-endpoints-in-power-bi-premium-public-preview/). A few months later, it even became possible to use third party tools in conjunction with Power BI Desktop, with the [announcement of the External Tools feature](https://powerbi.microsoft.com/en-us/blog/announcing-public-preview-of-external-tools-in-power-bi-desktop/).

The availability of the XMLA endpoint in Power BI Premium allows data model developers to leverage their existing skills and tools, and it is not a secret that Microsoft is investing heavily in making [Power BI Premium a superset of Analysis Services](https://community.powerbi.com/t5/Webinars-and-Video-Gallery/Power-BI-Premium-as-a-superset-of-Analysis-Services-the-XMLA/m-p/1434121). In other words, the integration of third party tools, community as well as commercial, with Power BI is something that is here to stay. In fact, Amir Netz, CTO of Microsoft Analytics, made a [joint statement](https://powerbi.microsoft.com/en-us/blog/community-tools-for-enterprise-powerbi-and-analysisservices/) with Marco Russo, founder of SQLBI, to affirm this point.

Here at Tabular Editor ApS, we firmly believe that Tabular Editor 3 is the best tabular data modeling tool available right now, and thanks to the integrations mentioned above, the tool is no longer reserved for SQL Server or Azure Analysis Services developers. 

Before proceeding, it is important to understand that Tabular Editor can be used in conjunction with Power BI in two very different scenarios:

- **Scenario 1:** Tabular Editor as an External Tool for Power BI Desktop.
- **Scenario 2:** Tabular Editor with the Power BI Premium XMLA Endpoint.

> [!IMPORTANT]
> You cannot use Tabular Editor to directly load a .pbix file. For more information, see <xref:desktop-limitations#power-bi-file-types>.

### Scenario 1: Tabular Editor as an External Tool for Power BI Desktop

Generally, this scenario is intended for self-service analysts and Power BI Desktop users without access to Power BI Premium, to make certain data modeling operations easier (for example, adding and editing measures), and to unlock advanced modeling options not otherwise available (calculation groups, perspectives and metadata translations).

External tools connect to the Analysis Services model hosted by Power BI Desktop. This allows the tool to make certain changes to the data model. Currently, however, not all types of data modeling operations are supported by Power BI Desktop. It is important to understand this limitation and how Tabular Editor behaves when used as an external tool for Power BI Desktop. See <xref:desktop-limitations> for more information about this.

The typical workflow in this scenario, is the following:

1. Open a .pbit or .pbix file in Power BI Desktop
2. Launch Tabular Editor through the External Tools ribbon
3. Switch back and forth between Tabular Editor and Power BI Desktop, depending on what type of change you need to make. For example, you can add and edit measures through Tabular Editor, but you must use Power BI Desktop if you need to add a new table to the model.
4. Whenever you make a change in Tabular Editor, use **File > Save** (CTRL+S) to write the changes back to Power BI Desktop.
5. When you are done making changes, close Tabular Editor. Then, publish or save the report as usual from within Power BI Desktop.

> [!NOTE]
> As of October 2021, there is a bug in Power BI Desktop that sometimes prevents Desktop from automatically refreshing the field list and visuals to reflect changes made through external tools. When this happens, saving the .pbix file and reopening it, or manually refreshing a table within the model, usually causes the field list and all visuals to update correctly.

The [modeling limitations](xref:desktop-limitations) that apply to External Tools are only relevant regarding write operations/model modifications. You can still use Tabular Editor 3's connected features to browse the data within the model through table data previews, Pivot Grids or DAX queries, as described later in this guide.

### Scenario 2: Tabular Editor with the Power BI Premium XMLA Endpoint

This scenario is for BI professionals in organizations that use Power BI Premium Capacity or Power BI Premium-Per-User workspaces, who intend to replace Power BI Desktop altogether for purposes of dataset development.

Essentially, the Power BI Premium XMLA Endpoint exposes an instance of Analysis Services (Tabular). In this scenario, Tabular Editor behaves no different than it would when connected to Azure Analysis Services or SQL Server Analysis Services (Tabular).

The typical workflow in this scenario, is the following:

1. When first migrating to Tabular Editor, use the XMLA endpoint to open a Power BI dataset in Tabular Editor, then save the model metadata as a file (Model.bim) or folder (Database.json). See @parallel-development for more information.
2. Going forward, open the model metadata in Tabular Editor from the file or folder you saved in step 1. Optionally use [workspace mode](xref:workspace-mode).
3. Apply changes using Tabular Editor.
4. If using workspace mode, changes should be immediately visible in the Power BI service every time you hit Save (CTRL+S) in Tabular Editor.
5. If not using workspace mode or when done making changes, use Tabular Editor's **Model > Deploy...** option to publish the changes to the Power BI service.

As the model metadata "source of truth" in this scenario, is the file or folder structure stored on disk, this scenario not only enables parallel development with version control integration, but also continuous integration/continuous deployment (CI/CD) using an automated build server such as Azure DevOps. See <xref:powerbi-cicd> for more information.

> [!WARNING]
> As soon as you apply changes to a Power BI dataset through the Power BI service XMLA endpoint, that dataset can no longer be downloaded as a .pbix file. See [Dataset connectivity with the XMLA endpoint](https://docs.microsoft.com/en-us/power-bi/admin/service-premium-connect-tools#power-bi-desktop-authored-datasets) for more information.

When using Tabular Editor to connect to the dataset through the XMLA endpoint, there are no limitations to the types of write operations/model modifications that can be made.

The remainder of this article focuses on differences between Power BI Desktop and Tabular Editor for data model development. Some sections only apply to scenario 2, due to the [modeling limitations](xref:desktop-limitations) that apply when using Tabular Editor as an external tool for Power BI Desktop (scenario 1).

## Tabular Editor 3 user interface

If you are new to Tabular Editor, we recommend reading through the following resources to understand Tabular Editor 3's user interface:

- [Getting to know Tabular Editor 3's User Interface](xref:user-interface)
- [TOM Explorer view](xref:tom-explorer-view)
- [Properties grid](xref:properties-view)
- [DAX editor](xref:dax-editor)

What follows is a quick walkthrough of how to achieve common tasks in Tabular Editor 3.

### How to modify the DAX expression of a measure

Locate the measure you want to modify in the **TOM Explorer** and select it. You can toggle the display of hidden objects (CTRL+6) and display folders (CTRL+5) using the toolbar buttons near the top of the TOM Explorer. You may also type the partial name of the measure in the search box, to filter the **TOM explorer**.

Once the measure is selected, you should see the DAX expression of the measure in the **Expression Editor** and various properties such as `Description`, `Format String`, `Hidden`, etc. in the **Properties** grid.

![Modify Measure](~/images/modify-measure.png)

To modify the DAX expression, simply place the cursor in the **Expression Editor** and update the DAX code. Hit F6 to automatically format the code. If you select a different object in the TOM Explorer or click the green checkmark button **Expression > Accept** (F5), the expression change is stored locally in Tabular Editor. You can also cancel the modification you made by hitting the red "X", **Expression > Cancel**. If you accidentally hit **Accept**, you can always undo the change by using the **Edit > Undo** (CTRL+Z) option.

To save your changes back to Power BI Desktop, the Power BI XMLA endpoint, or the file on disk from which the model was loaded, hit **File > Save** (CTRL+S).

### How to change the format string of a measure

Locate the measure you want to modify in the **TOM Explorer** and select it. You can toggle the display of hidden objects (CTRL+6) and display folders (CTRL+5) using the toolbar buttons near the top of the TOM Explorer. You may also type the partial name of the measure in the search box, to filter the **TOM explorer**.

Once the measure is selected, locate the `Format String` property in the **Properties** grid, expand it, and set the format string properties according to your preferences. Note the dropdown button at the right of the `Format` property. You may also freely enter a format string in the `Format String` property itself.

![Format String](~/images/format-string.png)

### How to modify the DAX expression of multiple measures

Tabular Editor 3 allows you to select multiple measures in order to create a [DAX Script](xref:dax-scripts), which lets you modify the DAX expression and various properties of all selected measures at once.

To create a DAX script based on existing measures, simply select the measures in the **TOM Explorer** (hold down the CTLR key to select multiple objects or hold down the SHIFT key to select a range of objects). Then, right click and hit **Script DAX**