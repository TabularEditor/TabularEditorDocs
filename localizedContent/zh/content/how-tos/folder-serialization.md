---
uid: folder-serialization
title: 文件夹序列化
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 文件夹序列化

This feature allows you to more easily integrate your SSAS Tabular Models in a file-based source control environment such as TFS, SubVersion or Git. By choosing "File" > "Save to Folder...", Tabular Editor will deconstruct the Model.bim file and save its content as separate files in a folder structure similar to the structure of the JSON within the Model.bim. When subsequently saving the model, only files with changed metadata will be touched, meaning most version control systems can easily detect which changes have been done to the model, making source merging and conflict handling a lot easier, than when working with a single Model.bim file.

![Folder serialization example](~/content/assets/images/folder-serialization-example.png)

默认情况下，对象会被序列化到最底层对象级别（即度量值、列和层次结构会分别存为独立的 .json 文件）。

此外，Tabular Editor 的 [command-line syntax](xref:command-line-options) 支持从此文件夹结构加载模型并直接部署到数据库，方便您自动化构建以支持持续集成工作流。

If you want to customize the granularity at which metadata is saved to individual files, go to **Tools > Preferences > File Formats > Save-to-folder** (**File > Preferences** in Tabular Editor 2). Here, it's possible to toggle some serialization options which are passed to the TOM when serializing into JSON. Furthermore, you can check/uncheck the types of objects for which individual files will be generated. In some Version Control scenarios, you might want to store everything related to one table in a file on its own, whereas in other scenarios you may need individual files for columns and measures.

首次使用“保存到文件夹”功能时，这些设置会作为模型上的注释保存；这样在加载模型后再点击“保存”按钮时，将沿用这些设置。 If you want to apply new settings, use "File > Save to Folder..." again.

<img src="~/content/assets/images/folder-serialization-settings-te2.png" width="300" />
