---
uid: semantic-bridge
title: Semantic Bridge
author: Greg Baldini
updated: 2025-01-23
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.25.0
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          none: true
        - edition: Enterprise
          full: true
---
# Semantic Bridge

<!--
SUMMARY: Overview of the Semantic Bridge feature - a multi-platform semantic model compiler that enables translation between different semantic model platforms (e.g., Databricks Metric Views to Microsoft's Tabular model in Analysis Services and Power BI / Fabric).
-->

> [!NOTE]
> The Semantic Bridge as released in 3.25.0 is an MVP feature. It has limitations as documented below, and the API and feature surface area are subject to change.

The Semantic Bridge is a semantic model compiler, with the capability to translate the structure and expressions of a semantic model from one platform to another.
This allows you to reuse business logic on multiple data platforms, supporting end users and meeting them where they consume the data.
It also allows for migrations from one platform to another.

## Interface

### Import Metric View YAML

The Semantic Bridge is available through **File > Open > Import from Metric View YAML**.
This will launch a dialogue to guide you through importing a Metric View into the current Tabular model, adding tables, columns, measures, and relationships based on the structure of the Metric View.
You must have a Tabular model open in Tabular Editor.
This can be a new, empty model or an existing model you want to enhance with the objects from the Metric View.
The menu button will not be enabled until you open or create a new Tabular model.

![Import a Metric View from the file menu with **File > Open > Import from Metric View YAML**](/images/features/semantic-bridge/semantic-bridge-file-menu-import.png)

### Enter Databricks connection details

You need to provide three details in this dialogue:

1. The path to the Metric View YAML file.
   You can paste the path to the file or use the **Browse** button to find it.
2. The Databricks hostname.
   This is to provide the correct argument in the M partition generated for the Databricks source system.
3. The HTTP path for Databricks.
   This is to provide the correct argument in the M partition generated for the Databricks source system.

If you are just testing the translation feature, you can provide placeholder values for the last two items, but you will need to fix the M partition definitions before you can refresh data into your Tabular model.

After filling out the details, click **OK**.
The Semantic Bridge will translate your Metric View to Tabular and create all the TOM objects for you.

![Databricks details in import dialog](/images/features/semantic-bridge/semantic-bridge-metric-view-details.png)

### Result

There are three possible results:

1. Success: everything in the Metric View was translated to Tabular and you have a Tabular model ready to use.
2. Success, but with some issues: the Semantic Bridge was not able to translate every object in the Metric View; there are diagnostic messages you can view to understand what needs your attention.
3. Failure: the Semantic Bridge could not translate the Metric View

After either success type, you can use undo/redo functionality like normal in Tabular Editor to undo or instantly replay the import.

**Success**

![Import success notification](/images/features/semantic-bridge/semantic-bridge-import-success.png)

**Success with issues**

![Import success notification with issues](/images/features/semantic-bridge/semantic-bridge-import-success-with-issues.png)

If you click on **View Diagnostics**, you can see a list of messages describing the issues in translation.
These diagnostics are available for review later by outputting them from a C# script:

```csharp
// Show all diagnostic messages from the last attempted import of a Metric View
SemanticBridge.MetricView.ImportDiagnostics.Output();
```

![Import diagnostics](/images/features/semantic-bridge/semantic-bridge-import-diagnostics.png)

**Failure**

![Import failure](/images/features/semantic-bridge/semantic-bridge-import-failed.png)

Viewing diagnostics for a failure is the same as for success with issues.

## Translation process

Translating a Metric View to a Tabular model happens in several steps:

1. Read the YAML from disk
2. Deserialize the YAML
3. Validate that the deserialized YAML represents a valid Metric View
4. If it is a valid Metric View, store it as a the currently loaded Metric View, similar to how there is a loaded Tabular model that you interact with.
   If it is not a valid Metric View, the process stops here and messages are available.
4. Analyze the Metric View and attempt to transform it to an intermediate representation
5. Attempt to transform the intermediate representation to a Tabular model

The import GUI described above handles all of this for you, but you can also use C# scripts to customize different steps of the process and operate on the Metric View programatically, similarly to how you are used to doing with a Tabular model.
Specifically, you can

- load a Metric View from disk with [`SemanticBridge.MetricView.Load`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Load_System_String_): loading makes it available in C# scripts as [`SemanticBridge.MetricView.Model`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Model), but does not import the structure into the Tabular model
- deserialize a Metric view from a string with [`SemanticBridge.MetricView.Deserialize`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Deserialize_System_String_): similar to loading, the model is available as [`SemanticBridge.MetricView.Model`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Model), but is not imported
- save a Metric View to disk with [`SemanticBridge.MetricView.Save`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Save_System_String_)
- serialize a Metric View to a string with [`SemanticBridge.MetricView.Serialize`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Serialize).
- validate a Metric View using a system that is similar to the [Best Practice Analyzer](xref:best-practice-analyzer) with [`SemanticBridge.MetricView.Validate`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_Validate)
	- you can create your own custom validation rules with [`SemanticBridge.MetricView.MakeValidationRule`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_MakeValidationRule__1_System_String_System_String_System_Func___0_TabularEditor_SemanticBridge_Platforms_Databricks_Validation_IReadOnlyValidationContext_System_Collections_Generic_IEnumerable_TabularEditor_SemanticBridge_Orchestration_DiagnosticMessage___) and its simpler versions
- import a Metric View to Tabular with [`SemanticBridge.MetricView.ImportToTabularFromFile`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_ImportToTabularFromFile_System_String_TabularEditor_TOMWrapper_Model_System_String_System_String_System_Collections_Generic_List_TabularEditor_SemanticBridge_Orchestration_DiagnosticMessage___System_Boolean_), which does the exact same as the GUI shown above, or [`SemanticBridge.MetricView.ImportToTabular`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_ImportToTabular_TabularEditor_TOMWrapper_Model_System_String_System_String_System_Collections_Generic_List_TabularEditor_SemanticBridge_Orchestration_DiagnosticMessage___System_Boolean_), which is similar, but operates on the currently loaded Metric View, rather than reading one from disk.


## MVP Limitations

### Supported platforms

In the MVP release, we support translations from a Databricks Metric View to a Tabular model.
Specifically we support the following surface area of a Databricks Metric View:

- v0.1 Metric View properties:
	- supported:
		- `source`: the source of the fact table
		- `joins`: collection of tables left-joined to the fact
		- `dimensions`: flat collection of fields from any table, either the single fact or any of the many joins
		- `measures`: flat collection of named aggregations representing business logic
	- unsupported:
		- `filter`: a SQL filter expression for the Metric View

All v1.1 metadata is not supported in the MVP.
Any v1.1 metadata is silently ignored upon deserialization of a Metric View, so it will not be visible in a C# script and it will not affect the translation to Tabular in any way.

> [!WARNING]
> Because the v1.1 metadata is silently ignored, a Metric View that you deserialize and then serialize will be missing this metadata.
> Be careful not to overwrite a v1.1 source YAML file from a C# script, as that will remove all v1.1 metadata.

### Limitations on translation from SQL

Metric Views provide a structured layer on top of SQL expressions, and so part of translating a Metric View is translating SQL to DAX and M in the Tabular model.

- Metric View `joins` with nested `joins` are not supported.
  In other words, only strict star schemas are supported for translation; snowflake models are not supported
- Metric View `joins` with `using` join criteria are not supported; only equijoins on a single key field using the `on` property are supported.
- Metric View `dimensions` with SQL expressions are not translated to M or DAX; they are presented as Tabular model calculated columns with their SQL expression commented out
- Metric View `measures` with non-basic aggregations are not translated to DAX; they are presented as a Tabular model measure with their SQL expression commented out
	- The only aggregations supported are sum, max, min, average, count, and distinct count.
	- SQL comments in a basic aggregation are not preserved in DAX

> [!WARNING]
> Note that SQL and DAX are different languages with different semantics.
> We can make no guarantee that a translated measure will behave identically between the Metric View SQL and the Tabular DAX we generate.
> Basic aggregates defined on fact table fields should behave the same, whereas aggregates defined on fields in dimension tables are more likely to produce undesired results.

### Connectivity

The MVP does not connect to any platforms besides Tabular, but works entirely with local files.
You must create your Metric View YAML on your own and then put it where Tabular Editor can see it.

### C# API

The C# interface has been built to optimize for the automatic translation workflow.
As such, there are limited affordances for interacting with the currently loaded Metric View, and certain types of operations are clunky.

## Appendix on nomenclature

It can be confusing to discuss things when talking about the Semantic Bridge, as there are many words that have both generic and specific meanings, depending what level of abstraction we are talking about and which platform we are discussing.
For example, the term "semantic model" is both generic, referring to the concept of a collection of data and business logic in some form suitable for supporting business reporting and analytical needs, and also the name Microsoft has adopted for referring to their specific implementation of this generic concept in Power BI and Fabric.
Thus, a semantic model might generically refer to a Databricks Metric View, an OLAP / Multidimensional Cube, a Power BI semantic model, or a model hosted in another platform's semantic layer.
Similarly, "dimension" refers to a concept in dimensional modeling, but it is also the name of a specific type of object in a Metric View.
Because of this, we have adopted the following definitions and standards in our documentation to maintain clarity and sanity.

> [!NOTE]
> These conventions are only intended for documentation about the Semantic Bridge feature.

### Definitions

- *Semantic model*: when used on its own always refers to the generic concept of a collection of data, metadata, and business logic to support reporting and analytics.
  If and only if it is immediately preceded by "Fabric" or "Power BI", then it is referring to that artifact type in that platform, specifically a Tabular model that is saved as TMDL or BIM and using M and DAX; we tend to prefer to use the term Tabular model to refer to the Power BI / Fabric semantic model to avoid this confusion where possible, because the Tabular model is shared across Power BI / Fabric as well as Analysis Serviced Tabular.
- *Platform*: a technology solution that has a semantic layer, on which a generic semantic model is hosted.
  Databricks Metric Views represent a platform; Fabric / Power BI represent a platform; Analysis Services Tabular is a platform; Analysis Services Multidimensional is a platform which we have no support for in the Semantic Bridge today.
- *Serialization format*: a way to represent a semantic model on disk in a textual format.
  TMDL and TMSL (.bim) are two serialization formats for a Power BI semantic model; YAML is the serialization format for a Databricks Metric View.
- *Object model*: an in-memory representation of a semantic model that we operate on in Tabular Editor via the Semantic Bridge either through GUI actions or C# scripts.
  The TOM or Tabular Object Model should be familiar to existing users of Tabular Editor.
  We have also created an object model for Databricks Metric Views, to allow manipulation of these in our tool.

### General dimensional modeling terminology

There are many terms that exist generally in discussion of a dimensional model or semantic model and also in a specific platform's object model and serialization formats.
For example, the term "measure" refers generically to a quantitative value that is aggregated in a dimensional model to represent a business metric of interest, but it also refers to a specific kind of object in both Databricks Metric Views and Tabular models; in a Metric View, a measure is a named SQL expression that defines an aggregation in the Metric View, and in a Tabular model a measure is a named DAX expression tat defines an aggregation in the Tabular model.
It is impossible to discuss the work of the Semantic Bridge without talking about multiple meanings of such words at once.
For example, we talk about translating a Metric View measure to a Tabular measure.
As such, **we always refer to an object in a specific platform's model by saying the platform and the object, e.g. "Metric View measure" or "Tabular measure"**.
If the term is ever used without being accompanied by a platform's name, then we are discussing the idea generically.

### Common terms across Metric Views and Tabular models

For those of our users who may be unfamiliar with either Metric Views or Tabular models, we provide an incomplete rosetta stone below.
We refer to the names of Metric View objects based on their representation in YAML, and Tabular based on the name of the type of object in TMDL/TMSL.

| General term         | Name in Tabular | Name in Metric View   | Description                                                                                          | Note                                                                                                                                                                                                                                       |
|----------------------|-----------------|-----------------------|------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| fact                 | table           | source                | A table holding foreign keys to dimensions and quantitative values to be aggregated                  | a Metric View has a single fact which is unnamed and captured as the root-level `source` attribute in YAML. Tabular models do not differentiate between types of tables: whether a table is a fact can only be inferred                    |
| dimension            | table           | join                  | A table holding descriptive attributes and one primary key to which the fact is related              | Tabular models do not differentiate, so the role of "dimension" is inferred only, as with a fact.                                                                                                                                          |
| partition            | parition        | source (join only)    | An object for data management, holding a subset of data in a table                                   | Tabular model tables can have many partitions and must have at least one. The Metric View fact, as mentioned above is defined purely as a source, but Metric View joins also have a `source` property, which acts roughly like a partition |
| field                | column          | dimension             | A column in a table                                                                                  |                                                                                                                                                                                                                                            |
| measure              | measure         | measure               | A quantitative value that is aggregated according to business logic in the model                     | Measures in a Tabular model are written in DAX, and in a Metric View in SQL                                                                                                                                                                |
| join or relationship | relationship    | join.on or join.using | A correspondence between key fields in two tables, a foreign key in one and primary key in the other | Relationships are explicit objects in a Tabular model, and implicitly defined as a property of the `join` object in Metric View YAML                                                                                                       |

## Additional Resources

- [Databricks Metric View documentation](https://learn.microsoft.com/en-us/azure/databricks/metric-views/)
- [Databricks Metric View YAML reference](https://learn.microsoft.com/en-us/azure/databricks/metric-views/data-modeling/syntax)
- @semantic-bridge-how-tos
