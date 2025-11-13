---
uid: general-introduction
title: General introduction and architecture
author: Daniel Otykier
updated: 2021-09-30
---

# General introduction and architecture

Tabular Editor is a Windows desktop application for developing tabular models. Specifically, the tool lets you edit the Tabular Object Model (TOM) metadata. The tool can load the TOM metadata from a file or from an existing Analysis Services database, and it can also deploy updated TOM metadata to Analysis Services.

> [!NOTE]
> We use the term **tabular model** to represent both Analysis Services Tabular models as well as Power BI datasets, since Analysis Services Tabular is the data model engine used by Power BI. Similarly, when we use term **Analysis Services**, we mean "any instance of Analysis Services", which could be SQL Server Analysis Services, Power BI Desktop or the Power BI Service XMLA Endpoint.

## Tabular Object Model (TOM) metadata

A data model is made up by a number of tables. Each table has one or more columns, and a table may also contain measures and hierarchies. Typically, the data model also defines relationships between tables, data sources containing connection details and table partitions containing data source expressions (SQL or M queries) for loading data, etc. All of this information is collectively called the **model metadata**, and it is stored in a JSON based format known as the **Tabular Object Model (TOM)**.

- When a tabular model is created using Visual Studio, the JSON representing the TOM metadata is stored in a file called **Model.bim**.
- When a data model is created using Power BI Desktop, the TOM metadata is embedded within the .pbix or .pbit file (since this file format also contains a lot of other details, such as definitions of visuals, bookmarks, etc., which is not related to the data model itself).

Using a client library called [AMO/TOM](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions), Tabular Editor is able to load and save metadata to and from this JSON based format. In addition, the client library allows Tabular Editor to connect directly to any instance of Analysis Services, in order to obtain the model metadata from an existing database. This is illustrated in the figure below.

![Architecture](~/content/assets/images/architecture.png)

> [!NOTE]
> In the paragraph above, we used the term **database** to represent a model that has been deployed to Analysis Services. Within the Power BI Service the term **dataset** is used to represent the same thing, namely a tabular model.

Tabular Editor can load model metadata from the following sources:

- [1] Model.bim files
- [2] Database.json files (see @parallel-development for more information)
- [3] .pbit files (Power BI Template)
- [4] A database on SQL Server Analysis Services (Tabular)
- [5] A database on Azure Analysis Services
- [6] A dataset in a Power BI Premium\* Workspace
- [7] A Power BI Desktop report in Import/DirectQuery mode

\*Power BI Premium/Embedded Capacity or Power BI Premium-Per-User is required in order to enable the [XMLA Endpoint](https://docs.microsoft.com/en-us/power-bi/admin/service-premium-connect-tools). The XMLA Endpoint must be enabled for any third party tool to connect to Power BI datasets.

> [!IMPORTANT]
> Tabular Editor 2.x supports all sources 1-7 above. Tabular Editor 3 supports only some sources depending on which [edition of Tabular Editor 3](xref:editions) you are using.

Once the model metadata has been loaded in Tabular Editor, the user is free to add/edit/remove **objects** and change **object properties**. Modifications are not saved back to the source until the user explicitly saves the model, either by choosing **File > Save** or by hitting CTRL+S. If the model metadata was loaded from a file source (sources 1-3 above), that file will then be updated. If the model metadata was loaded from Analysis Services (sources 4-7 above), then the changes are saved back to Analysis Services. Note that certain changes may cause objects to enter a state where they can no longer be queried by end-users. For example, if you add a column to a table, you will need to [refresh the table](xref:refresh-preview-query#refreshing-data) before users can query the contents of that table or any measures that dependent on the table.

> [!WARNING]
> Certain limitations apply when saving model metadata changes back to Power BI Desktop (source 7 above). See @desktop-limitations for more information.

### TOM objects and properties

The TOM metadata is made up of **objects** and **properties**.

Examples of TOM **objects**:

- Data Sources
- Tables
- Partitions
- Measures
- KPIs
- Columns
- Model Roles

Examples of TOM **object properties**:

- `Name` (text)
- `Display Folder` (text)
- `Description` (text)
- `Hidden` (true/false)
- `Summarize By` (one of: None, Sum, Min, Max, ...)

Most properties are simple values (text, true/false, one-of-selections aka. enums), but properties can also reference other objects (for example, the `Sort By Column` property should reference a column). Properties can also be arrays of objects, such as the `Members` property on the Model Role object.

Tabular Editor generally uses the same name for objects and properties as those defind in the [Microsoft.AnalysisServices.Tabular namespace](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular?view=analysisservices-dotnet). If you want to learn more about specific TOM objects or properties, always consult the namespace documentation. For example, to learn what the "Summarize By" column property does, first locate the "Column" class in Microsoft's documentation, then expand "Properties" and scroll to "SummarizeBy". You should then get to [this article](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.column.summarizeby?view=analysisservices-dotnet).

![SummarizeBy on Microsoft's docs](~/content/assets/images/asdocs-summarizyby.png)

### Editing property values

Both versions of Tabular Editor display the object model metadata in a hierarchical view known as the **TOM Explorer** view, which roughly corresponds to the hierarchical structure of the JSON metadata:

![TOM Explorer](~/content/assets/images/tom-explorer.png)

In general, Tabular Editor lets you modify object properties by first selecting an object in the TOM Explorer (you can select multiple objects at once by holding down SHIFT or CTRL), and then simply editing the property value within the **Properties view** (see screenshot below).

![Properties View](~/content/assets/images/properties-view.png)

Tabular Editor does not perform explicit validation of modified property values, except for some basic rules (for example, object names cannot be empty, measure names have to be unique, etc.). It is your responsibility as a tabular model developer to know which properties to set and what values to use.

If you make a mistake while editing property values, you can always press CTRL+Z (Edit > Undo) to roll back the last property change.

## Architecture

As hinted above, Tabular Editor has two different modes of operation: Metadata from file (aka. **file mode**) and metadata from Analysis Services (aka. **connected mode**). In addition, Tabular Editor 3 introduces a hybrid approach called [**workspace mode**](xref:workspace-mode).

Before proceeding, it is important to understand the differences between these modes:

- In **file mode**, Tabular Editor loads and saves all model metadata from and to a file on disk. In this mode, Tabular Editor cannot interact with model **data** (that is, table previews, DAX queries, Pivot Grids, and data refresh operations are not enabled). This mode can be used entirely offline, even when no instance of Analysis Services is available. The supported file formats for model metadata are:
  - Model.bim (same format used by Visual Studio)
  - Database.json (folder structure only used by Tabular Editor)
  - .pbit (Power BI Template)
- In **connected mode**, Tabular Editor loads and saves model metadata from and to Analysis Services. In this mode, it is possible to interact with model **data** using Tabular Editor 3 (table previews, DAX queries, Pivot Grids and data refresh). This mode requires connectivity to an instance of Analysis Services.
- In **workspace mode**, Tabular Editor 3 loads model metadata from a file on disk AND deploys the metadata to Analysis Services. On subsequent saves (CTRL+S), updates are saved both to disk and to the connected instance of Analysis Services. It is possible to interact with model **data** similar to **connected mode**.

### Metadata synchronization

One of the major benefits of Tabular Editor over the standard tools (Visual Studio, Power BI Desktop), is that model metadata is only saved upon request. In other words, you can make multiple changes to objects and properties without having to wait for any Analysis Services instance to become synchronized between each change. The synchronization of the Analysis Services database is an operation that may take several seconds to complete, depending on the size and complexity of the data model. In Power BI Desktop, this synchronization happens every time the notorious "Working on it" spinner appears on the screen. In Tabular Editor, this only happens when you explicitly save your changes (CTRL+S).

The downside is, of course, that you have to remember to explicitly save your changes, before you can test the impact of any metadata modifications that were made.

## Next steps

- @installation-activation-basic
- @migrate-from-vs
- @migrate-from-desktop
- @migrate-from-te2