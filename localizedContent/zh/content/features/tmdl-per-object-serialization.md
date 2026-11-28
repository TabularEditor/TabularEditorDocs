---
uid: tmdl-per-object-serialization
title: 按对象 TMDL 序列化
author: Morten Lønskov
updated: 2026-11-13
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.28.0
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          partial: true
          note: "Opens per-object folders and saves them in the standard layout"
        - edition: Enterprise
          full: true
---
# 按对象 TMDL 序列化

按对象 TMDL 序列化将表的每个列、度量值、分区和层次结构，以及模型的每个函数、共享表达式、数据源和关系，都保存到其各自的 `.tmdl` 文件中。标准布局中的[表格模型定义语言 (TMDL)](xref:tmdl) 文件夹将每个表及其所有对象保存在一个文件中，并将所有函数写入 `functions.tmdl`、所有共享表达式写入 `expressions.tmdl`、所有数据源写入 `dataSources.tmdl`，以及所有关系写入 `relationships.tmdl`。使用按对象分文件的方式，对一个度量的更改在源代码管理中显示为对一个文件的更改，而编辑同一表的不同度量的两位开发人员编辑的是不同的文件。

计算项始终保留在其表格的文件中。

## 文件夹布局

表格的自有文件保存在 `tables` 文件夹中，并保留表格的属性、描述、注释、刷新策略和计算项。您拆分的表对象将放入以表命名的文件夹中，每个对象类型对应一个子文件夹。函数、共享表达式、数据源和关系位于 TMDL 文件夹根目录下的每个类型的文件夹中：

```text
definition/
├── model.tmdl
├── expressions/
│   ├── Database.tmdl
│   └── Server.tmdl
├── functions/
│   └── Sales.MarginPct.tmdl
├── relationships/
│   └── 3a5c9e1d-7b2f-4c8a-9d6e-1f0b2a4c6e8d.tmdl
└── tables/
    ├── Sales.tmdl
    └── Sales/
        ├── columns/
        │   ├── Amount.tmdl
        │   └── Order Date.tmdl
        ├── measures/
        │   └── Total Amount.tmdl
        └── partitions/
            └── Sales.tmdl
```

没有某类型对象的表或模型不会有该类型的文件夹。每个表对象文件都以一行 `ref table` 开头，该行将对象绑定到其表：

```tmdl
ref table Sales

	measure 'Total Amount' = SUM(Sales[Amount])
		formatString: #,0.00
```

该文件夹是标准 TMDL。Power BI Desktop、Tabular Editor 2.26 或更高版本以及 Tabular Editor 3.19 或更高版本读取该文件夹的方式与读取标准布局中的文件夹的方式相同。

> [!WARNING]
> 请勿在 3.19 之前的 Tabular Editor 3 或 2.26 之前的 Tabular Editor 2 中打开每个对象的文件夹。如果保存文件夹时选中了**包含元数据顺序**，则这些版本会加载包含空文本的共享表达式，并且无法加载包含每个对象数据源文件的文件夹。如果您从此类版本保存模型，则共享表达式将不带其文本保存。

## 保存包含每个对象文件的模型

1. 打开**工具 &gt； 首选项 &gt； 文件格式 &gt； 保存到文件夹 &gt； TMDL 序列化**。
2. 勾选**将对象保存到单独的文件**。
3. 在其下方的树中，选中将拥有自己文件的对象类型。
4. 点击**确定**。
5. 选择**文件 > 保存到文件夹**，然后选择一个文件夹。如果文件夹对话框显示**使用注释中的序列化设置**，请取消选中该选项。

当**工具 &gt; 首选项 &gt; 文件格式 &gt; 保存到文件夹**下的**保存到文件夹格式**为默认值**TMDL**时，**文件 &gt; 保存到文件夹**将写入 TMDL。

![选中“将对象保存到单独文件”的 TMDL 序列化首选项页面](~/content/assets/images/pref-tmdl-serialization.png)

对于您打开的模型，请选择**模型 &gt; 序列化选项...**，勾选**将对象保存到单独的文件**，然后点击**确定**。接下来按 **Ctrl+S** 将写入每个对象的布局。

Tabular Editor 将此选择以及选中的对象类型存储在 `model.tmdl` 的 `TabularEditor_SerializeOptions` 注释中，存储为 `"TmdlApplySerializationDepth": true`。**文件 &gt; 保存** (**Ctrl+S**) 将读取该批注并保留布局，无论您的偏好设置如何。有关注释的更多信息，请参阅[序列化模型注释](xref:save-to-folder#serialization-model-annotation)。

> [!NOTE]
> **将对象保存到单独的文件**默认处于禁用状态。由 Power BI Desktop 或较早版本的 Tabular Editor 保存的 TMDL 文件夹在其注解中没有 `TmdlApplySerializationDepth`，并且 **Ctrl+S** 会将其保持为标准布局。

### 对象类型

树中每个选中的行都会将一个对象类型移至其自己的文件中：


| 行                               | 文件夹                       | 注意                                                        |
| --------------------------------- | ---------------------------- | ----------------------------------------------------------- |
| **数据源**                  | `dataSources`                |                                                             |
| **用户定义函数 (UDF)** | `functions`                  |                                                             |
| **共享表达式**            | `expressions`                |                                                             |
| **关系**                 | `relationships`              |                                                             |
| **表 > 列**           | `tables/<table>/columns`     | 选中或取消选中它会对**层次结构**执行相同的操作。 |
| **表 > 层次结构**       | `tables/<table>/hierarchies` | 选中或取消选中它会对**列**执行相同的操作。     |
| **表 > 度量值**          | `tables/<table>/measures`    |                                                             |
| **表 > 分区**        | `tables/<table>/partitions`  |                                                             |


**表**、**透视**、**角色**和**翻译**显示为已选中且呈灰色。标准TMDL布局已将每个表、透视、角色和文化写入其各自的文件。树中没有计算项的行。

### 文件名

每个文件和表格文件夹都以其对象命名。在 Windows 文件名中无效的字符 (`" < > | : * ? / \`) 在名称中被编码。

当您重命名对象时，下一次保存将删除旧文件，并写入一个具有新名称的文件。当您删除表时，下一次保存将删除其文件及其文件夹。

## 重用模型的已存储设置

当您为具有`TabularEditor_SerializeOptions`注释的模型选择**文件 &gt; 保存到文件夹**时，文件夹对话框将显示**使用注释中的序列化设置**。选中此项，即可使用模型的已存储设置（包括其每个对象的布局）进行保存。取消选中该选项，即可按照您的首选项进行保存，并将这些首选项写入注释。

如果模型来自 Database.json 文件夹，并且您选中了**使用注释中的序列化设置**，则当在**TMDL 序列化**页面上选中**将对象保存到单独的文件**时，其序列化深度将转移到 TMDL 文件夹，或者模型的注释包含 `TmdlApplySerializationDepth`。无论深度如何，计算项都保留在其表的文件中。

## 返回标准布局

1. 选择**模型 &gt； 序列化选项...**。
2. 取消选中**将对象保存到单独的文件**，然后单击**确定**。
3. 按 **Ctrl+S**。
4. 在“按对象 TMDL 序列化”警告中，单击**是**。

Tabular Editor 会重写文件夹，使每个表对应一个文件，函数、共享表达式、数据源和关系也各对应一个文件，并从注释中移除 `TmdlApplySerializationDepth`。模型的其他序列化设置（包括 TMDL 格式化）仍保留在注释中。

## 保存警告

任何将标准布局写入包含每个对象文件的文件夹的保存操作都会首先显示**每个对象的 TMDL 序列化**警告。这适用于**文件 &gt; 保存**、**文件 &gt; 保存到文件夹**以及在[工作区模式](xref:workspace-mode)下的保存。警告内容如下：

> 您的模型当前按对象进行序列化。现在保存将使您的文件恢复为标准 TMDL 序列化。有关详细信息，请参阅此文档。
>
> 是否要继续？

警告中的链接将打开此页面。

![在保存写入标准布局之前显示的“按对象 TMDL 序列化”警告](~/content/assets/images/tmdl-per-object-save-warning.png)


| 回答  | 结果                                                                                                            |
| ------- | ----------------------------------------------------------------------------------------------------------------- |
| **是** | 文件夹将以标准布局重写，并且 `TmdlApplySerializationDepth` 将从注释中删除。|
| **否**  | 不写入任何内容，且保存操作被取消。在工作区模式下，工作区数据库也不会更新。     |


选择“是”后，当您再次在 Tabular Editor 3 企业版中打开该文件夹时，它将保持标准布局，直到您再次选中“将对象保存到单独的文件”为止。

## 版本和工具支持


| 工具                                | 打开每个对象的文件夹 | 保存每个对象的文件                                      |
| ----------------------------------- | ------------------------- | ----------------------------------------------------------- |
| Tabular Editor 3 企业版 | 是                       | 是                                                         |
| Tabular Editor 3 商业版   | 是                       | 否。在保存警告后，保存操作将写入标准布局。|
| Tabular Editor 3 Desktop 版    | 否                        | 否。                                                         |
| Power BI Desktop                    | 是                       | 否。保存时在不显示警告的情况下写入标准布局。      |


在 Business Edition 中，**将对象保存到单独的文件**和对象类型树不会显示在**TMDL 序列化**页面或**模型 &gt; 序列化选项……**中。

> [!WARNING]
> 如果有人使用写入标准布局的工具保存每个对象的文件夹，则每个表格文件和每个对象文件都会在源代码管理中发生变化。

## 对象顺序

选中**包含元数据顺序**时，函数、共享表达式、数据源和关系将保持其顺序：保存操作将为其中每个项目写入一行 `ref` 到 `model.tmdl`，例如：

```tmdl
ref expression Server
ref expression Database
ref function 'Sales.MarginPct'
```

当您打开文件夹时，位于各自文件中的列、度量值、分区和层次结构将按文件名顺序加载，**包含元数据顺序**对其没有影响。

## 请参阅

- @tmdl
- @save-to-folder
- @save-with-supporting-files
- @parallel-development