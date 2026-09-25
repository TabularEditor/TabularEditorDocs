---
uid: save-to-folder
title: 保存到文件夹
author: Morten Lønskov
updated: 2026-09-11
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

# 保存到文件夹

Save to Folder allows you to store your model metadata as individual files, which can be easily managed by version control systems. Instead of having a single file (.bim or .pbix) that contains all the objects of your data model, such as tables, measures, relationships, etc., you can split them into separate files and store them in a folder. This way, you can use source control tools to track the changes, compare versions, and collaborate with other developers on your data model.

> [!NOTE]
> 你可以使用两种不同的格式将 Data model 保存到文件夹：JSON 或 [TMDL](tmdl.md)。

要把模型保存到文件夹，按以下步骤操作：

1. 点击“文件 > 保存到文件夹”
2. 选择用于保存模型文件的文件夹。
3. Click on Save. Tabular Editor 会在所选文件夹中创建或更新文件，并根据序列化设置以指定的 JSON 或 TMDL 格式保存。
4. 现在，你可以将该文件夹中的文件用于版本控制、部署或备份。

## 序列化设置

序列化设置用于定义如何将模型对象拆分为单独的文件。 In these settings you can also define if you wish to use JSON or TMDL formats.

### [Tabular Editor 2 偏好](#tab/TE2Preferences)

序列化设置位于“文件 > 偏好 > 序列化”。 <br></br>
![TE2 偏好](~/content/assets/images/common/TE2SaveToFolderSerializationSettings.png)

上面所示的设置是 Tabular Editor 3 的默认设置，但并非 Tabular Editor 2.X 的默认设置

### [Tabular Editor 3 偏好](#tab/TE3Preferences)

Serialization settings are found under Tools > Preferences > File Formats
The tabs General and Save-to-folder contains settings regarding the serialization of the model. <br></br>
![TE3 偏好](~/content/assets/images/common/TE3SaveToFolderSerializationSettings.png)

Tabular Editor 3 对 JSON 序列化有一套默认设置；如果要使用不同设置，你必须在序列化模式中主动选择。在那里也可以切换到 TMDL 格式。

***

### User Defined Functions (UDFs)

Since Tabular Editor 3.27.0, the JSON folder format can store each [DAX User-Defined Function](xref:udfs) in its own file, the same way it already does for tables, measures and columns. The functions go in a `functions` subfolder at the model root:

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

Turn it on with the **User Defined Functions (UDFs)** level, under **Tools > Preferences > File Formats > Save-to-folder** or, for the model you have open, under **Model > Serialization options...**.

![Model > Serialization options, with the User Defined Functions (UDFs) level ticked](~/content/assets/images/serialization-options-udf.png)

> [!IMPORTANT]
> Tabular Editor selects this level by default only for a model you save to a folder for the _first_ time. A model that's already folder-serialized keeps the levels stored in its own serialization annotation, so its functions stay inline until you select **User Defined Functions (UDFs)** under **Model > Serialization options...** and save the model again.

### 序列化模型注释

Tabular Editor 会将序列化设置保存在模型中，这样无论谁在处理该模型，这些设置都会保持一致。 This ensures that a developer's local preferences do not overwrite model's setting and lead to an unmanageable merge in your source control. 你可以在 TOM Explorer 的“Model”对象属性中找到这些注释，路径为：Model > Annotations > TabularEditor_SerializeOptions <br></br>
![TE3 偏好](~/content/assets/images/common/SaveToFolderModelAnnotation.png)

#### 覆盖模型序列化设置

The model's annotation can be overwritten if so desired. First set up the serialization preferences inside Tabular Editor and go to File > Save to Folder.
This open up Windows Explorer and here the ticket button needs to be unselected. <br></br>
![TE3 Preferences](~/content/assets/images/common/SaveToFolderOverwriteModelAnnotation.png)
