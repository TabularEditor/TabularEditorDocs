---
uid: save-to-folder
title: 保存到文件夹
author: Morten Lønskov
updated: 2023-08-08
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: 桌面版
          none: true
        - edition: 商业版
          full: true
        - edition: 企业版
          full: true
---

# 保存到文件夹

使用“保存到文件夹”，你可以将模型元数据存储为独立文件，便于用版本控制系统进行管理。 你不必再使用一个包含 Data model 中所有对象（例如表、度量值、关系等）的单一文件 (.bim 或 .pbix)，而是可以将它们拆分为多个独立文件，并存放在一个文件夹中。 这样一来，你就可以使用版本控制系统来跟踪更改、比较版本，并与其他开发者协作开发你的 Data model。

> [!NOTE]
> 你可以使用两种不同的格式将 Data model 保存到文件夹：JSON 或 [TMDL](tmdl.md)。

要把模型保存到文件夹，按以下步骤操作：

1. 点击“文件 > 保存到文件夹”
2. 选择用于保存模型文件的文件夹。
3. 点击“保存”。 Tabular Editor 会在所选文件夹中创建或更新文件，并根据序列化设置以指定的 JSON 或 TMDL 格式保存。
4. 现在，你可以将该文件夹中的文件用于版本控制、部署或备份。

## 序列化设置

序列化设置用于定义如何将模型对象拆分为单独的文件。 在这些设置中，你还可以选择使用 JSON 或 TMDL 格式。

### [Tabular Editor 2 偏好](#tab/TE2Preferences)

序列化设置位于“文件 > 偏好 > 序列化”。 <br></br>
![TE2 偏好](~/content/assets/images/common/TE2SaveToFolderSerializationSettings.png)

上面所示的设置是 Tabular Editor 3 的默认设置，但并非 Tabular Editor 2.X 的默认设置

### [Tabular Editor 3 偏好](#tab/TE3Preferences)

序列化设置位于“工具 > 偏好 > 文件格式”下。
“常规”和“保存到文件夹”选项卡包含与模型序列化相关的设置。 <br></br>
![TE3 偏好](~/content/assets/images/common/TE3SaveToFolderSerializationSettings.png)

Tabular Editor 3 对 JSON 序列化有一套默认设置；如果要使用不同设置，你必须在序列化模式中主动选择。在那里也可以切换到 TMDL 格式。

***

### 序列化模型注释

Tabular Editor 会将序列化设置保存在模型中，这样无论谁在处理该模型，这些设置都会保持一致。 这可确保开发者的本地偏好不会覆盖模型的设置，从而避免在源代码管理中出现难以处理的合并冲突。 你可以在 TOM Explorer 的“Model”对象属性中找到这些注释，路径为：Model > Annotations > TabularEditor_SerializeOptions <br></br>
![TE3 偏好](~/content/assets/images/common/SaveToFolderModelAnnotation.png)

#### 覆盖模型序列化设置

如果需要，可以覆盖模型上的注释。 先在 Tabular Editor 中设置好序列化偏好，然后选择“文件 > 保存到文件夹”。
这会打开 Windows 资源管理器，此处需要取消勾选该复选框。 <br></br>
![TE3 偏好](~/content/assets/images/common/SaveToFolderOverwriteModelAnnotation.png)
