---
uid: getting-started-te2
title: Tabular Editor 2 快速入门
author: Daniel Otykier
updated: 2021-09-21
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      none: true
---

# 入门

## 安装

只需从[发布页面](https://github.com/TabularEditor/TabularEditor/releases/latest)下载 .msi 文件，然后运行该 .msi 安装程序即可。

## 先决条件

无。

> [!NOTE]
> Tabular Editor 使用 [Tabular Object Model](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) 在 Model.bim 文件和现有数据库之间加载和保存元数据。 This is included in the .msi installer. Visit the official Microsoft documentation for [Analysis Services Client Libraries](https://docs.microsoft.com/en-us/azure/analysis-services/analysis-services-data-providers).

## 系统要求

- **操作系统：** Windows 7、Windows 8、Windows 10、Windows Server 2016、Windows Server 2019 或更高版本
- **.NET Framework：** [4.6](https://dotnet.microsoft.com/download/dotnet-framework)

## 使用 Tabular Editor

推荐的工作流是：像平时一样使用 SSDT 设置表和关系，然后用 Tabular Editor 完成其余工作。 That is: Create calculated columns, measures, hierarchies, perspectives, translations, display folders, and every other kind of fine-tuning you can think of.

通过选择“打开 > 从文件...”加载 Model.bim 文件……（位于“文件”菜单中，CTRL+O）；或通过选择“打开 > 从数据库...”从 Analysis Services 实例打开现有数据库…… option. In the latter case, you will be prompted for a server name and optional credentials:

![Connecting to an already deployed Tabular Model](~/content/assets/images/getting-started-te-01.png)

This also works with the new Azure Analysis Services PaaS. The "Local Instance" dropdown, may be used to browse and connect to any running instances of Power BI Desktop or Visual Studio Integrated Workspaces. **Note that although Tabular Editor can make changes to a Power BI model through the TOM, not all modeling operations are supported by Microsoft. [More information](Power-BI-Desktop-Integration.md)**

单击“确定”后，你将看到服务器上的数据库列表。

模型加载到 Tabular Editor 后，界面如下所示：

![The main UI of Tabular Editor](~/content/assets/images/getting-started-te-02.png)

屏幕左侧的树状视图显示 Tabular 模型中的所有表。 Expanding a table will show all columns, measures and hierarchies within the table, grouped by their Display Folders. Use the buttons just above the tree, to toggle display folders, hidden objects, certain types of objects, or filter out objects by names. Right-clicking anywhere in the tree, will bring up a context menu with common actions, such as adding new measures, making an object hidden, duplicating objects, deleting objects, etc. Hit F2 to rename the currently selected object or multiselect and right-click to batch rename multiple objects.

![Batch Renaming lets you rename multiple objects simultaneously](~/content/assets/images/getting-started-te-03.png)

在主 UI 的右上角，你会看到 DAX编辑器，可用于编辑模型中任意度量值或计算列的 DAX 表达式。 Click the "DAX Formatter" button to automatically format the code through www.daxformatter.com.

Use the property grid in the lower right corner, to examine and set properties of objects, such as Format String, Description along with translations and perspective memberships. 你也可以在此设置显示文件夹属性，但更简单的做法是直接在树状视图中拖放对象来更新其显示文件夹（可尝试使用 CTRL 或 SHIFT 选择多个对象）。

要编辑透视或翻译（区域设置），请在树状视图中选择“Model”对象，然后在属性网格中找到“Model Perspectives”或“Model Cultures”属性。 Click the small ellipsis button to open a collection editor for adding/removing/editing perspectives/cultures.

![Editing perspectives - click the ellipsis button to the right](~/content/assets/images/getting-started-te-04.png)

To save your changes back to the Model.bim file, click the save button or hit CTRL+S. If you opened an existing Tabular Database, the changes are saved directly back to the database. You will be prompted if the database was changed since you loaded it into Tabular Editor. You can always undo your changes by pressing CTRL+Z.

如果要将模型部署到其他位置，请转到“Model”菜单并选择“Deploy”。

## 部署

Tabular Editor 自带部署向导 Deployment Wizard，相比从 SSDT 部署有一些优势——尤其是在部署到现有数据库时。 After choosing a server and a database to deploy to, you have the following options for the deployment at hand:

![Deployment Wizard](~/content/assets/images/getting-started-te-05.png)

不勾选“Deploy Connections”复选框，将确保目标数据库中的所有数据源保持不变。 You will get an error if your model contains one or more tables with a data source, that does not already exist in the target database.

同样，不勾选“Deploy Table Partitions”将确保表上的现有分区不会被更改，从而保持分区中的数据不受影响。

勾选“Deploy Roles”后，目标数据库中的角色会更新为与已加载模型一致；但如果不勾选“Deploy Role Members”，则目标数据库中各角色的成员将保持不变。

## 命令行用法

你可以使用命令行进行自动化部署。 All deployment options that are available through the GUI, are also available through the command line.

### 部署示例

`TabularEditor.exe c:\Projects\Model.bim`

打开 Tabular Editor 的 GUI 并加载指定的 Model.bim 文件（不部署任何内容）。

`TabularEditor.exe c:\Projects\Model.bim -deploy localhost AdventureWorks`

将指定的 Model.bim 文件部署到 localhost 上运行的 SSAS 实例，并覆盖现有或创建新的 AdventureWorks 数据库。 The GUI will not be loaded.

By default, partitions, data sources and roles will not be overwritten in the target database. This behaviour can be changed by adding one or more of the following switches to the command above:

- `-P` 覆盖 **p**artitions：分区
- `-C` 覆盖 **c**onnections（连接，即数据源）
- `-R` 覆盖 **r**oles：角色
- `-M` 覆盖角色 **m**embers：成员

有关命令行选项的更多信息，请参见[这里](../features/Command-line-Options.md)。

> [!NOTE]
> 由于 TabularEditor.exe 是一个 Windows Forms 应用程序，从命令行运行时会在不同的线程中执行，并会立即将控制权返回给调用方。 This may cause issues when running deployments as part of a batch job where you need to await successful deployment before proceeding with the job. If you experience these issues, use `start /wait` to let TabularEditor finish its job before returning control to the caller:
>
> `start /wait TabularEditor.exe c:\Projects\Model.bim -deploy localhost AdventureWorks`

## 高级脚本编写

Tabular Editor 允许你使用 C# 通过脚本方式修改已加载的模型。 This is practical when you want to apply several changes to many objects at once. The Advanced Script editor has access to two objects:

- `Selected`，表示资源管理器树中当前选中的所有对象。
- `Model`，表示整个 Tabular Object Model 树。

高级脚本编辑器提供有限的 IntelliSense 功能，帮助你快速上手：

![IntelliSense helps you create scripts for Tabular Editor](~/content/assets/images/getting-started-te-06.png)

有关高级脚本编写的更多文档和示例，可在[此处](../how-tos/Advanced-Scripting.md)找到。
