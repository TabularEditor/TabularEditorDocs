---
uid: save-to-folder
title: Save to folder
author: Morten Lønskov
updated: 2023-08-08
applies_to:
  versions:
    - version: 2.x
    - version: 3.x
---
# Save to folder

Save to Folder allows you to store your model metadata as individual files, which can be easily managed by version control systems. Instead of having a single file (.bim or .pbix) that contains all the objects of your data model, such as tables, measures, relationships, etc., you can split them into separate files and store them in a folder. This way, you can use source control tools to track the changes, compare versions, and collaborate with other developers on your data model.

> [!NOTE]
>You can save your data model to a folder using two different formats: JSON or [TMDL](tmdl-common.md).

To save your model to folder, follow these steps:

1. Click on File > Save To Folder
2. Choose a folder where you want to save your model files. 
3. Click on Save. Tabular Editor will create or update the files in the selected folder, using the JSON or TMDL format as specified in the [serialization settings](#Serialization-settings).
4. You can now use the files in the folder for version control, deployment, or backup purposes.



## Serialization settings
The serialisation settings defines how the model objects are split into seperate files. In these settings you can also define if you wish to use JSON or TMDL formats.

> [!NOTE]
>JSON is the default format as TMDL is currently in preview. 


### [Tabular Editor 2 Preferences](#tab/TE2Preferences)
Serialisation settings are found under File > Preferences > Serialization 
![TE2 Preferences](~/images/common/TE2SaveToFolderSerializationSettings.png)

The settings shown above are those set as default when using Tabular Editor 3, but are not those that are set per default by Tabular Editor 2.X

### [Tabular Editor 3 Preferences](#tab/TE3Preferences)
Serialisation settings are found under Tools > Preferences > File Formats
The tabs General and Save-to-folder contains settings regarding the serialization of the model. 

![TE3 Preferences](~/images/common/TE3SaveToFolderSerializationSettings.png)

Tabular Editor 3 has a default setting for JSON serialization and you must actively choose a different setting in serialization mode, which is also where you change to the TMDL format. 
