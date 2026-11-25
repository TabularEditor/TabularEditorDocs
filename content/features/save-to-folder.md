---
uid: save-to-folder
title: Save to folder
author: Morten Lønskov
updated: 2026-11-13
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# Save to folder

Save to Folder allows you to store your model metadata as individual files, which can be easily managed by version control systems. Instead of having a single file (.bim or .pbix) that contains all the objects of your data model, such as tables, measures, relationships, etc., you can split them into separate files and store them in a folder. This way, you can use source control tools to track the changes, compare versions, and collaborate with other developers on your data model.

> [!NOTE]
> A model folder uses one of two formats: Database.json (JSON) or [TMDL](xref:tmdl). In Tabular Editor 3, **File > Save to Folder** writes the format set in **Save to Folder format** under **Tools > Preferences > File Formats > Save-to-folder**, TMDL by default. A model loaded from a folder keeps its folder's format when you use **File > Save**.

To save your model to folder, follow these steps:

1. Select **File > Save to Folder**.
2. Choose a folder where you want to save your model files.
3. Click **Save**. Tabular Editor creates or updates the files in the selected folder.
4. You can now use the files in the folder for version control, deployment, or backup purposes.



## Serialization settings
The serialization settings defines how the model objects are split into separate files. In these settings you can also define if you wish to use JSON or TMDL formats.


### [Tabular Editor 2 Preferences](#tab/TE2Preferences)
Serialization settings are found under File > Preferences > Serialization 
<br></br>
![TE2 Preferences](~/content/assets/images/common/TE2SaveToFolderSerializationSettings.png)

The settings shown above are those set as default when using Tabular Editor 3, but are not those that are set per default by Tabular Editor 2.X

### [Tabular Editor 3 Preferences](#tab/TE3Preferences)
Serialization settings are under **Tools > Preferences > File Formats**:

- **General** holds the settings shared across formats. **General serialization settings** (**Include sensitive** and **Ignore incremental refresh partitions**) apply to Model.bim files, Database.json folders and TMDL folders. **JSON serialization settings** apply to Model.bim files and Database.json folders.
- **Save-to-folder** sets the format **File > Save to Folder** writes, and links to **Model > Serialization options...**.
- **Save-to-folder > JSON Serialization** applies to saves to a Database.json folder.
- **Save-to-folder > TMDL Serialization** applies to saves to a TMDL folder. In Enterprise Edition, it also turns on [per-object TMDL serialization](xref:tmdl-per-object-serialization).

**Model > Serialization options...** edits the settings stored with the loaded model. The dialog shows the model's format, for example **Current format: TMDL**, and the sections for that format. To change the format, use **File > Save to Folder** or **File > Save As**.

The JSON Serialization and TMDL Serialization pages each have a **Reset to default** button. For every setting, its default and when your preferences apply, see [Preferences](xref:preferences#file-formats--general).
***

### User Defined Functions (UDFs)

The JSON folder format can store each [DAX User-Defined Function](xref:udfs) in its own file, the same way it already does for tables, measures and columns. The functions go in a `functions` subfolder at the model root:

```
MyModel/
├── database.json
├── functions/
│   ├── Sales.MarginPct.json
│   └── Time.SameDayLastYear.json
├── tables/
└── ...
```

The benefit is the same as for every other object type: two developers editing two different functions change two different files, so Git has nothing to merge. Without it every function lives inline in `database.json`, and any two parallel edits collide in that one file.

Turn it on with the **User Defined Functions (UDFs)** level, under **Tools > Preferences > File Formats > Save-to-folder > JSON Serialization** or, for the model you have open, under **Model > Serialization options...**.

![Model > Serialization options, with the User Defined Functions (UDFs) level ticked](~/content/assets/images/serialization-options-udf.png)

> [!IMPORTANT]
> Tabular Editor selects this level by default only for a model you save to a folder for the *first* time. A model that's already folder-serialized keeps the levels stored in its own serialization annotation, so its functions stay inline until you select **User Defined Functions (UDFs)** under **Model > Serialization options...** and save the model again.

### Serialization Model Annotation
Tabular Editor saves the serialization settings on your model so that they will always stay the same no matter who is working on the model. This ensures that a developer's local preferences do not overwrite model's setting and lead to an unmanageable merge in your source control. You can find these annotations in the TOM Explorer properties of the Model > Annotations > TabularEditor_SerializeOptions

A TMDL save writes no annotation when **Include sensitive**, **Ignore incremental refresh partitions** and **Save objects to separate files** are unchecked and the TMDL settings are at their defaults.
<br></br>
![TE3 Preferences](~/content/assets/images/common/SaveToFolderModelAnnotation.png)


### Overwriting Model Serialization
To replace the model's annotation with your preferences, set up the serialization preferences and select **File > Save to Folder**. In the folder dialog, uncheck **Use serialization settings from annotations**. The dialog shows this checkbox only for a model that has the annotation, for both Database.json and TMDL saves. 
<br></br>
![TE3 Preferences](~/content/assets/images/common/SaveToFolderOverwriteModelAnnotation.png)
