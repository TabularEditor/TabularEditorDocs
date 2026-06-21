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

## 文件夹序列化

此功能可让您更轻松地在基于文件的源代码控制环境（如 TFS、Subversion 或 Git）中集成 SSAS 表格模型。 选择“文件”>“保存到文件夹...”，Tabular Editor 会拆解 Model.bim 文件，并将其内容保存为独立文件，以与 Model.bim 中 JSON 结构类似的文件夹层级进行组织。 之后再次保存模型时，只会更新元数据发生变化的文件。这意味着大多数版本控制系统都能轻松识别模型中做了哪些改动；相比只使用单个 Model.bim 文件，这会让代码合并与冲突处理简单得多。

![image](https://cloud.githubusercontent.com/assets/8976200/22483167/5e07ad52-e7fc-11e6-890f-5c0d20fff0cb.png)

默认情况下，对象会被序列化到最底层对象级别（即度量值、列和层次结构会分别存为独立的 .json 文件）。

此外，Tabular Editor 的 [command-line syntax](xref:command-line-options) 支持从此文件夹结构加载模型并直接部署到数据库，方便您自动化构建以支持持续集成工作流。

如果您想自定义将元数据保存为独立文件的粒度，请前往“文件”>“偏好”，然后点击“保存到文件夹”选项卡。 在这里，你可以切换一些序列化选项，这些选项会在序列化为 JSON 时传递给 TOM。 此外，你还可以勾选/取消勾选要生成独立文件的对象类型。 在某些版本控制场景中，你可能希望将某个表相关的所有内容都存到一个独立文件中；而在其他场景中，你可能需要为列和度量值分别生成独立文件。

首次使用“保存到文件夹”功能时，这些设置会作为模型上的注释保存；这样在加载模型后再点击“保存”按钮时，将沿用这些设置。 如果你想应用新设置，请再次使用“文件”>“保存到文件夹...”。

<img src="https://cloud.githubusercontent.com/assets/8976200/25333606/30578a78-28eb-11e7-9885-0fc66f5e4046.png" width="300" />
