---
uid: save-to-folder
title: 保存到文件夹
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

# 保存到文件夹

使用“保存到文件夹”，你可以将模型元数据存储为独立文件，便于用版本控制系统进行管理。你不必再使用一个包含 Data model 中所有对象（例如表、度量值、关系等）的单一文件 (.bim 或 .pbix)，而是可以将它们拆分为多个独立文件，并存放在一个文件夹中。这样一来，你就可以使用版本控制系统来跟踪更改、比较版本，并与其他开发者协作开发你的 Data model。

> [!NOTE]
> 模型文件夹使用以下两种格式之一：Database.json (JSON) 或 [TMDL](xref:tmdl)。在 Tabular Editor 3 中，**文件 > 保存到文件夹**将写入在**工具 > 首选项 > 文件格式 > 保存到文件夹**下的**保存到文件夹格式**中设置的格式，默认情况下为 TMDL。当您使用**文件 > 保存**时，从文件夹加载的模型会保留其文件夹的格式。

要把模型保存到文件夹，按以下步骤操作：

1. 选择**文件 > 保存到文件夹**。
2. 选择要保存模型文件的文件夹。
3. 点击**保存**。Tabular Editor 将创建或更新所选文件夹中的文件。
4. 现在，你可以将该文件夹中的文件用于版本控制、部署或备份。

## 序列化设置

序列化设置用于定义如何将模型对象拆分为单独的文件。在这些设置中，你还可以选择使用 JSON 或 TMDL 格式。

### [Tabular Editor 2 偏好](#tab/TE2Preferences)

序列化设置位于“文件 > 偏好 > 序列化”。 <br></br>
![TE2 偏好](~/content/assets/images/common/TE2SaveToFolderSerializationSettings.png)

上面所示的设置是 Tabular Editor 3 的默认设置，但并非 Tabular Editor 2.X 的默认设置

### [Tabular Editor 3 偏好](#tab/TE3Preferences)
序列化设置位于**工具 > 首选项 > 文件格式**下：

- **常规**包含跨格式共享的设置。**常规序列化设置**（**包含敏感信息**和**忽略增量刷新分区**）适用于 Model.bim 文件、Database.json 文件夹和 TMDL 文件夹。**JSON 序列化设置**适用于 Model.bim 文件和 Database.json 文件夹。
- **保存到文件夹**设置**文件 > 保存到文件夹**写入的格式，并链接到**模型 > 序列化选项...**。
- **“保存到文件夹”>“JSON 序列化”**适用于保存到 Database.json 文件夹。
- **保存到文件夹 > TMDL 序列化**适用于保存到 TMDL 文件夹。在企业版中，它还会启用[按对象 TMDL 序列化](xref:tmdl-per-object-serialization)。

**模型 > 序列化选项...**编辑与已加载模型一起存储的设置。该对话框显示模型的格式（例如**当前格式：TMDL**）以及该格式的各个部分。要更改格式，请使用**文件 > 保存到文件夹**或**文件 > 另存为**。

“JSON 序列化”和“TMDL 序列化”页面均具有**恢复默认值**按钮。有关每个设置、其默认值以及何时应用您的首选项，请参阅[首选项](xref:preferences#file-formats--general)。
***

### 用户自定义函数（UDFs）

JSON 文件夹格式可以将每个[DAX 用户定义函数](xref:udfs)存储在其自己的文件中，与它对表、度量值和列的处理方式相同。函数位于模型根目录下的 `functions` 子文件夹中：

```
MyModel/
├── database.json
├── functions/
│   ├── Sales.MarginPct.json
│   └── Time.SameDayLastYear.json
├── tables/
└── ...
```

好处与其他任何对象类型相同：两位开发人员分别编辑两个不同的函数时，会修改两个不同的文件，因此 Git 没有任何需要合并的内容。如果不启用它，每个函数都会以内联方式保存在 `database.json` 中，任何两项并行编辑都会在这一个文件里发生冲突。

在“工具”>“首选项”>“文件格式”>“保存到文件夹”>“JSON 序列化”下，或对于您已打开的模型，在“模型”>“序列化选项…”下，使用**用户定义函数 (UDF)** 级别将其启用。

![模型 > 序列化选项，其中已勾选“用户定义函数（UDFs）”级别](~/content/assets/images/serialization-options-udf.png)

> [!IMPORTANT]
> 只有在&#x4F60;_&#x9996;&#x6B21;_&#x5C06;模型保存到文件夹时，Tabular Editor 才会默认选中此级别。已采用文件夹序列化的模型会在自身的序列化注释中保留已存储的级别，因此在你于 **模型 > 序列化选项...** 中选择 **用户自定义函数（UDFs）** 并再次保存模型之前，这些函数仍会继续以内联方式存储。

### 序列化模型注释
Tabular Editor 会在您的模型中保存序列化设置，这样，无论谁在处理模型，这些设置都将始终保持不变。这样可确保开发人员的本地首选项不会覆盖模型的设置，从而导致源代码管理中出现无法管理的合并。您可以在“模型” > “批注” > “TabularEditor_SerializeOptions”的 TOM Explorer 属性中找到这些批注。

当未选中**包含敏感项**、**忽略增量刷新分区**和**将对象保存到单独文件**，且 TMDL 设置为默认值时，TMDL 保存操作不会写入任何批注。
<br></br>
![TE3 首选项](~/content/assets/images/common/SaveToFolderModelAnnotation.png)


### 覆盖模型序列化设置
要将模型的注释替换为您的首选项，请设置序列化首选项，然后选择**文件 > 保存到文件夹**。在文件夹对话框中，取消选中**使用注释中的序列化设置**。对于 Database.json 和 TMDL 保存，该对话框仅对具有该批注的模型显示此复选框。 
<br></br>
![TE3 首选项](~/content/assets/images/common/SaveToFolderOverwriteModelAnnotation.png)
