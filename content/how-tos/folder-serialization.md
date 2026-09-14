---
uid: folder-serialization
title: Folder Serialization
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---
# Folder Serialization
This feature allows you to more easily integrate your SSAS Tabular Models in a file-based source control environment such as TFS, SubVersion or Git. By choosing "File" > "Save to Folder...", Tabular Editor will deconstruct the Model.bim file and save its content as separate files in a folder structure similar to the structure of the JSON within the Model.bim. When subsequently saving the model, only files with changed metadata will be touched, meaning most version control systems can easily detect which changes have been done to the model, making source merging and conflict handling a lot easier, than when working with a single Model.bim file.

![Folder serialization example](~/content/assets/images/folder-serialization-example.png)

By default, objects are serialized down to the lowest object level (meaning measures, columns and hierarchies are stored as individual .json files).

Additionally, Tabular Editor's [command-line syntax](xref:command-line-options) supports loading a model from this folder structure and deploying it directly to a database, making it easy for you to automate builds for continuous integration workflows.

If you want to customize the granularity at which metadata is saved to individual files, go to File > Preferences and click the "Save to folder"-tab. Here, it's possible to toggle some serialization options which are passed to the TOM when serializing into JSON. Furthermore, you can check/uncheck the types of objects for which individual files will be generated. In some Version Control scenarios, you might want to store everything related to one table in a file on its own, whereas in other scenarios you may need individual files for columns and measures.

These settings are saved in an annotation on the model, the first time you use the Save to Folder function, so that the settings are reused when the model is loaded and the "Save"-button is subsequently clicked. If you want to apply new settings, use "File > Save to Folder..." again.

<img src="~/content/assets/images/folder-serialization-settings-te2.png" width="300" />
