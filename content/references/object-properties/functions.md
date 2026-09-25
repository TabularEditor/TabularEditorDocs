---
uid: object-properties-functions
title: Function and set properties
author: Jeroen ter Heerdt
updated: 2026-09-23
applies_to:
  products:
    - product: Tabular Editor 2
      partial: true
      note: "Supports functions and sets, but not Namespace, PackageId or PackageVersion"
    - product: Tabular Editor 3
      since: 3.23.0
      note: "User-defined functions need 3.23.0 or later. Sets are supported in all versions."
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# Function and set properties

<!--
SUMMARY: Reference for the properties of DAX user-defined functions and of sets.
-->

This page covers the properties of DAX user-defined functions and of sets. For properties that most objects share, see @object-properties-common.

## Function

A user-defined function (UDF) is a reusable DAX function that you define once in the model and call from any DAX expression, including other functions. It takes parameters, which can be values, tables or references to columns and measures, and returns a value or a table. UDFs belong to the model, not to a table. In the TOM Explorer, they're under the **Functions** folder.

UDFs need compatibility level 1702 or higher. Azure Analysis Services and SQL Server Analysis Services don't support them. For a full introduction, see @udfs.

Tabular Editor 2 also supports UDFs. It shows them under the **Functions** folder, and you add one by right-clicking the folder and choosing **New User-Defined Function**. Tabular Editor 2 doesn't have the **Namespace**, **PackageId** and **PackageVersion** properties.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Hidden](xref:object-properties-common#hidden)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Changed Properties](xref:object-properties-common#changed-properties)
- [Error Message](xref:object-properties-common#error-message)
- [Object Type](xref:object-properties-common#object-type)
- [State](xref:object-properties-common#state)
- [Lineage Tag](xref:object-properties-common#lineage-tag)
- [Source Lineage Tag](xref:object-properties-common#source-lineage-tag)

The name of a function is what you call it by in DAX, so it can't contain spaces. It can contain periods and underscores. Use a compound name such as `Finance.Margin` or `ACME_Margin`, so your function doesn't clash with a built-in DAX function that Microsoft adds later. See @kb.bpa-udf-use-compound-names. When you rename a function, Tabular Editor 3 updates the references to it throughout the model, as @formula-fix-up-dependencies does for measures and columns.

### Basic

#### Namespace
`Namespace` · string · *stored as an annotation* (`TE_Group`)

The group that the function appears under in the @tom-explorer-view when grouping of user-defined functions by namespace is turned on with the toggle button above the TOM Explorer. Tabular Editor works out the namespace in this order:

1. If the function has a `TE_Group` annotation, that's the namespace.
2. Otherwise, if the function's name contains a dot, the namespace is the part before the last dot: `DaxLib.Convert.CelsiusToFahrenheit` is in namespace `DaxLib.Convert`.
3. Otherwise, if the function has a `DAXLIB_PackageId` annotation (see **PackageId** below), the namespace is the package ID.
4. Otherwise, the namespace is empty.

You can set a different namespace without renaming the function. Tabular Editor saves it in the `TE_Group` annotation on the function, so it's saved with the model. To go back to the namespace from the name, reset the property or clear the value. It works like a display folder: it only organizes the TOM Explorer. It doesn't change how you call the function in DAX, where you always use the full name.

For example, if you [batch rename](xref:duplicate-and-batch) a set of functions to remove the `DaxLib.Convert.` prefix from their names, you can keep them grouped by setting their namespace to `DaxLib.Convert`.

### Metadata

#### PackageId
`PackageId` · string · read-only · *stored as an annotation* (`DAXLIB_PackageId`)

The ID of the [DaxLib](https://daxlib.org) package that the function comes from. Tabular Editor reads it from the function's `DAXLIB_PackageId` annotation, which DaxLib packages put on their functions. The Properties view only shows **PackageId** and **PackageVersion** when the function has this annotation, so you don't see them for functions that you wrote yourself.

The DAX Package Manager in Tabular Editor 3 removes the `DAXLIB_` annotations when it installs a function, and tracks the package with extended properties instead (see below). So you typically see these properties on functions from a DaxLib package that were added to the model without the DAX Package Manager of Tabular Editor 3. See @dax-package-manager.

#### PackageVersion
`PackageVersion` · string · read-only · *stored as an annotation* (`DAXLIB_PackageVersion`)

The version of the DaxLib package that the function comes from, read from the function's `DAXLIB_PackageVersion` annotation.

The DAX Package Manager doesn't use **PackageId** and **PackageVersion**. It keeps track of installed packages in extended properties: `TabularEditor_ModelDaxPkgTable` and `TabularEditor_ModelDaxPkgSeq` on the model list the installed packages, and `TabularEditor_ObjDaxPkgHandle` and `TabularEditor_ObjDaxPkgContentHash` on each function record which package the function belongs to and what its expression looked like when it was installed. If you change the expression of a function that came from a package, a later update or removal of the package asks what to do with your changed function.

To stop the DAX Package Manager from tracking a function, remove both its `TabularEditor_ObjDaxPkgHandle` and `TabularEditor_ObjDaxPkgContentHash` extended properties. After that, removing the package no longer deletes the function, and the package still shows as installed. If you later update or reinstall the package, the DAX Package Manager finds a function with the same name and asks how to resolve the conflict. Don't remove only `TabularEditor_ObjDaxPkgContentHash`: the function then counts as changed, so every update asks about it. The DAX Package Manager documentation warns that changing these extended properties by hand can lead to unexpected behavior, so only do this when you no longer want to manage the function as part of the package.

### Options

#### Expression
`Expression` · string

The function's parameter list and body, in lambda notation: the parameters in parentheses, then `=>`, then the DAX expression that uses them. For example:

```dax
// Returns the relative change between two values
(
    oldValue: NUMERIC,  // The original value
    newValue: NUMERIC   // The value to compare against
)
=> DIVIDE ( newValue - oldValue, oldValue )
```

Each parameter can have a type, such as `NUMERIC`, `STRING` or `TABLE`, and an evaluation mode: `VAL` (the default) evaluates the argument once, before the function runs, like a variable. `EXPR` passes the expression itself, so it's evaluated in the context where the function uses it, like a measure. A parameter with `= expression` after it is optional. See @udfs for the full syntax.

Comments in the expression are useful: Tabular Editor 3 shows them in autocomplete suggestions and tooltips when you call the function.

In Tabular Editor 3, you can edit functions together with other objects in a @dax-scripts document, with the `FUNCTION` keyword. You can also write a function in the `DEFINE` section of a @dax-query and apply the query to add the function to the model.

## Set

A set belongs to a table and holds a DAX expression. TOM describes it as a *calculated set*. Sets are only supported in Power BI and Fabric models, at compatibility level 1400 or higher. The TOM library refuses to add a set to a model in Analysis Services compatibility mode, with the error *is not supported at AnalysisServices mode*.

Sets don't appear in the TOM Explorer. To add, edit or remove the sets of a table, select the table and click the ellipsis button of its **Sets** property (see @object-properties-tables). The Properties view only shows that property for models in Power BI compatibility mode at compatibility level 1400 or higher.

<!-- TODO (not verifiable from TE3 source): what a Set is used for. TOM only describes it as a "calculated set" on a table with a DAX expression that can be static or dynamic. It looks like the equivalent of an MDX named set (for example for Excel PivotTables), but that isn't documented. Confirm with the TE/TOM team. -->

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Display Folder](xref:object-properties-common#display-folder)
- [Hidden](xref:object-properties-common#hidden)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Error Message](xref:object-properties-common#error-message)
- [Object Type](xref:object-properties-common#object-type)
- [State](xref:object-properties-common#state)
- [Translated Display Folders](xref:object-properties-common#translated-display-folders)

### Options

#### Expression
`Expression` · string

The DAX expression that defines the set.

<!-- TODO (not verifiable from TE3 source): what kind of DAX expression a set expects (a table expression that returns the members of the set?); add an example. TOM only says "The DAX expression that is evaluated for the calculated set." -->

#### Dynamic
`IsDynamic` · bool

Whether the set is static or dynamic. A static set is evaluated once, so its members don't change with the filters in a query. A dynamic set is evaluated for each query, in the context of that query, so its members can change with the filters.

<!-- TODO (not verifiable from TE3 source): the static/dynamic behavior. It's based on how named sets work in MDX; TOM only says "Indicates whether the set is static or dynamic". -->
