---
uid: parallel-development
title: Enabling parallel development using Git and Save to Folder
author: Daniel Otykier
updated: 2021-09-30
applies_to:
  editions:
    - edition: Desktop
      none: x
    - edition: Business
    - edition: Enterprise
---

# Enabling parallel development using Git and Save to Folder

This article describes the principles of parallel model development (that is, the ability for multiple developers to work in parallel on the same data model) and the role of Tabular Editor in this regard.

# Prerequisites

- The destination of your data model must be one of the following:
  - SQL Server 2016 (or newer) Analysis Services Tabular
  - Azure Analysis Services
  - Power BI Premium Capacity/Power BI Premium-per-user with [XMLA read/write enabled](https://docs.microsoft.com/en-us/power-bi/admin/service-premium-connect-tools#enable-xmla-read-write)
- Git repository accessible by all team members (on-premises or hosted in Azure DevOps, GitHub, etc.)

# TOM as source code

Parallel development has traditionally been difficult to implement on Analysis Services tabular models and Power BI datasets (in this article, we will call both types of models "tabular models" for brevity). With the introduction of the JSON-based model metadata used by the [Tabular Object Model (TOM)](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions), integrating model metadata in version control has certainly become easier.

The use of a text-based file format makes it possible to handle conflicting changes in a graceful way, by using various diff tools that are often included with the version control system. This type of change conflict resolution is very common in traditional software development, where all of the source code resides in a large number of small text files. For this reason, most popular version control systems are optimized for these types of files, for purposes of change detection and (automatic) conflict resolution.

For tabular model development, the "source code" is our JSON-based TOM metadata. When developing tabular models with earlier versions of Visual Studio, the Model.bim JSON file was augmented with information about who modified what and when. This information was simply stored as additional properties on the JSON objects throughout the file. This was problematic, because not only was the information redundant (since the file itself also has metadata that describes who the last person to edit it was, and when the last edit happened), but from a version control perspective, this metadata does not hold any *semantic meaning*. In other words, if you were to remove all of the modification metadata from the file, you would still end up with a perfectly valid TOM JSON-file, that you could deploy to Analysis Services or publish to Power BI, without affecting the functionality and business logic of the model.

Just like source code for traditional software development, we do not want this kind of information to "contaminate" our model metadata. Indeed, a version control system gives a much more detailed view of the changes that were made, who made them, when and why, so there is no reason to include it as part of the files being versioned.

When Tabular Editor was first created, there was no option to get rid of this information from the Model.bim file created by Visual Studio, but that has luckily changed in more recent versions. However, we still need to deal with a single, monolithic file (the Model.bim file) containing all of the "source code" that defines the model.

Power BI dataset developers have it much worse, since they do not even have access to a text-based file containing the model metadata. The best they can do is export their Power BI report as a [Power BI Template (.pbit) file](https://docs.microsoft.com/en-us/power-bi/create-reports/desktop-templates#creating-report-templates) which is basically a zip file containing the report pages, the data model definitions and the query definitions. From the perspective of a version control system, a zip file is a binary file, and binary files cannot be diff'ed, compared and merged, the same way text files can. This forces Power BI developers to use 3rd party tools or come up with elaborate scripts or processes for properly versioning their data models - especially, if they want to be able to merge parallel tracks of development within the same file.

Tabular Editor aims to simplify this process by providing an easy way to extract only the semantically meaningful metadata from the Tabular Object Model, regardless of whether that model is an Analysis Services tabular model or a Power BI dataset. Moreover, Tabular Editor can split up this metadata into several smaller files using its Save to Folder feature.

# What is Save to Folder?

As mentioned above, the model metadata for a tabular model is traditionally stored in a single, monolithic JSON file, typically named **Model.bim**, which is not well suited for version control integration. Since the JSON in this file represents the [Tabular Object Model (TOM)](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions), it turns out that there is a straight forward way to break the file down into smaller pieces: The TOM contains arrays of objects at almost all levels, such as the list of tables within a model, the list of measures within a table, the list of annotations within a measure, etc. When using Tabular Editor's **Save to Folder** feature, these arrays are simply removed from the JSON, and instead, a subfolder is generated containing one file for each object in the original array. This process can be nested. The result is a folder structure, where each folder contains a set of smaller JSON files and subfolders, which semantically contains exactly the same information as the original Model.bim file:

![Save To Folder](~/images/save-to-folder.png)

The names of each of the files representing individual TOM objects are simply based on the `Name` property of the object itself. The name of the "root" file is **Database.json**, which is why we sometimes refer to the folder-based storage format as simply **Database.json**.

## Pros of using Save to Folder

Below are some of the advantages of storing the tabular model metadata in this folder based format:

- **Multiple smaller files work better with many version control systems than few large files.** For example, git stores snapshots of modified files. For this reason alone, it makes sense why representing the model as multiple smaller files is better than storing it as a single, large file.
- **Avoid conflicts when arrays are reordered.** Lists of tables, measures, columns, etc., are represented as arrays in the Model.bim JSON. However, the order of objects within the array does not matter. It is not uncommon for objects to be reordered during model development, for example due to cut/paste operations, etc. With Save to Folder, array objects are stored as individual files, so the arrays are no longer change tracked, reducing the risk of merge conflicts.
- **Different developers rarely change the same file.** As long as developers work on separate parts of the data model, they will rarely make changes to the same files, reducing the risk of merge conflicts.

## Cons of using Save to Folder

As it stands, the only disadvantage of storing the tabular model metadata in the folder based format, is that this format is used exclusively by Tabular Editor. In other words, you can not directly load the model metadata into Visual Studio from the folder based format. Instead, you would have to temporarily convert the folder based format to the Model.bim format, which can of course be done using Tabular Editor.

## Configuring Save to Folder

One size rarely fits all. Tabular Editor has a few configuration options that affect how a model is serialized into the folder structure. In Tabular Editor 3, you can find the general settings under **Tools > Preferences > Save-to-folder**. Once a model is loaded in Tabular Editor, you can find the specific settings that apply to that model under **Model > Serialization options...**. The settings that apply to a specific model are stored as an annotation within the model itself, to ensure that the same settings are used regardless of which user loads and saves the model.

![Configuring Save To Folder](~/images/configuring-save-to-folder.png)

### Serialization settings

- **Use recommended settings**: (Default: checked) When this is checked, Tabular Editor uses the default settings when saving a model as a folder structure for the first time.
- **Serialize relationships on from-tables**: (Default: unchecked) When this is checked, Tabular Editor stores relationships as an annotation on the table at the "from-side" (typically the fact table) of the relationship, instead of storing them at the model level. This is useful when in the early development phase of a model, where table names are still subject to change quite often.
- **Serialize perspective membership info on objects**: (Default: unchecked) When this is checked, Tabular Editor stores information about which perspectives an object (table, column, hierarchy, measure) belongs to, as an annotation on that object, instead of storing the information at the perspective level. This is useful when object names are subject to change, but perspective names are finalised.
- **Serialize translations on translated objects**: (Default: unchecked) When this is checked, Tabular Editor stores metadata translations as an annotation on each translatable object (table, column, hierarchy, level, measure, etc.), instead of storing the translations at the culture level. This is useful when object names are subject to change.
- **Prefix file names sequentially**: (Default: unchecked) In cases where you want to retain the metadata ordering of array members (such as the order of columns in a table), you can check this to have Tabular Editor prefix the filenames with a sequential integer based on the object's index in the array. This is useful if you use the default drillthrough feature in Excel, and would like [columns to appear in a certain order in the drillthrough](https://github.com/TabularEditor/TabularEditor/issues/46#issuecomment-297932090).

> [!NOTE]
> The main purpose of the settings described above, is to reduce the number of merge conflicts encountered during model development, by adjusting how and where certain model metadata is stored. In the early phases of model development, it is not uncommon for objects to be renamed often. If a model already has metadata translations specified, every object rename would cause at least two changes: One change on the object being renamed, and one change for every culture that defines a translation on that object. When **Serialize translations on translated objects** is checked, there would only be a change on the object being renamed, as that object also includes the translated values (since this information would be stored as an annotation).

### Serialization depth

The checklist allows you to specify which objects will be serialized as individual files. Note that some options (perspectives, translations, relationships) may not be available, depending on the settings specified above.

In most cases, it is recommended to always serialize objects to the lowest level. However, there may be special cases where this level of detail is not needed.

# Power BI and version control

As mentioned above, integrating a Power BI report (.pbix) or Power BI template (.pbit) file in version control, does not enable parallel development or conflict resolution, due to these files using a binary file format. At the same time, we have to be aware of the current limitations of using Tabular Editor (or other third party tools) with Power BI Desktop or the Power BI XMLA endpoint respectively.

These limitations are:

- When using Tabular Editor as an external tool for Power BI Desktop, [not all modeling operations are supported](@xref:desktop-limitations).
- Tabular Editor can extract model metadata from a .pbix file loaded in Power BI Desktop, or directly from a .pbit file on disk, but there is **no supported way to update model metadata in a .pbix or .pbit file outside of Power BI Desktop**.
- Once any changes are made to a Power BI dataset through the XMLA endpoint, [that dataset can no longer be downloaded as a .pbix file](https://docs.microsoft.com/en-us/power-bi/admin/service-premium-connect-tools#power-bi-desktop-authored-datasets).

To enable parallel development, we must be able to store the model metadata in one of the text-based (JSON) formats mentioned above (Model.bim or Database.json). There is no way to "recreate" a .pbix or .pbit file from the text-based format, so **once we decide to go this route, we will no longer be able to use Power BI Desktop for editing the data model**. Instead, we will have to rely on tools that can use the JSON-based format, which is exactly the purpose of Tabular Editor.

> [!WARNING]
> If you do not have access to a Power BI Premium workspace (either Premium capacity or Premium-Per-User), you will not be able to publish the model metadata stored in the JSON files, since this operation requires access to the [XMLA endpoint](https://docs.microsoft.com/en-us/power-bi/admin/service-premium-connect-tools).

> [!NOTE]
> Power BI Desktop is still needed for purpose of creating the visual part of the report. It is a [best practice to always separate reports from models](https://docs.microsoft.com/en-us/power-bi/guidance/report-separate-from-model). In case you have an existing Power BI file that contains both, [this blog post](https://powerbi.tips/2020/06/split-an-existing-power-bi-file-into-a-model-and-report/) ([video](https://www.youtube.com/watch?v=PlrtBm9YN_Q))  describes how to split it into a model file and a report file.

# Using git

(WIP)

## Branching strategy

(WIP)

## Common workflow

(WIP)

# Next steps

- @optimizing-workflow-workspace-mode
- @powerbi-cicd
- @as-cicd