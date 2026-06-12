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

# 快速入门

## 安装

只需从[发布页面](https://github.com/TabularEditor/TabularEditor/releases/latest)下载 .msi 文件，然后运行该 .msi 安装程序即可。

## 先决条件

无。

> [!NOTE]
> Tabular Editor 使用 [Tabular Object Model](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) 在 Model.bim 文件和现有数据库之间加载和保存元数据。 该组件已包含在 .msi 安装包中。 请参阅 Microsoft 官方文档：[Analysis Services Client Libraries](https://docs.microsoft.com/en-us/azure/analysis-services/analysis-services-data-providers)。 该组件已包含在 .msi 安装包中。 请参阅 Microsoft 官方文档：[Analysis Services Client Libraries](https://docs.microsoft.com/en-us/azure/analysis-services/analysis-services-data-providers)。

## 系统要求

- **操作系统：** Windows 7、Windows 8、Windows 10、Windows Server 2016、Windows Server 2019 或更高版本
- **.NET Framework：** [4.6](https://dotnet.microsoft.com/download/dotnet-framework)

## 使用 Tabular Editor

推荐的工作流是：像平时一样使用 SSDT 设置表和关系，然后用 Tabular Editor 完成其余工作。 也就是说：创建计算列、度量值、层次结构、透视、翻译、显示文件夹，以及你能想到的其他各种细节调整。 也就是说：创建计算列、度量值、层次结构、透视、翻译、显示文件夹，以及你能想到的其他各种细节调整。

通过选择“打开 > 从文件...”加载 Model.bim 文件…… （位于“文件”菜单中，CTRL+O）；或通过选择“打开 > 从数据库...”从 Analysis Services 实例打开现有数据库…… 选项即可。 在后一种情况下，程序会提示你输入服务器名称以及可选的凭据：

![连接到已部署的表格模型](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/Connect.png)

这也适用于新版 Azure Analysis Services PaaS。 可使用“本地实例”下拉列表浏览并连接到任何正在运行的 Power BI Desktop 实例或 Visual Studio 集成工作区。 **注意：尽管 Tabular Editor 可以通过 TOM 对 Power BI 模型进行更改，但并非所有建模操作都受 Microsoft 支持。 [更多信息](Power-BI-Desktop-Integration.md)**

单击“确定”后，你将看到服务器上的数据库列表。

模型加载到 Tabular Editor 后，界面如下所示：

![Tabular Editor 的主 UI](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/Main%20UI.png)

屏幕左侧的树状视图显示 Tabular 模型中的所有表。 展开某个表会显示该表中的所有列、度量值和层次结构，并按其显示文件夹进行分组。 使用树状视图上方的按钮，可切换显示文件夹、隐藏对象、特定类型的对象，或按名称筛选对象。 在树状视图中的任意位置右键单击，会弹出包含常用操作的上下文菜单，例如添加新度量值、将对象设为隐藏、复制对象、删除对象等。 按 F2 可重命名当前选中的对象；或多选后右键单击，以批量重命名多个对象。 展开某个表会显示该表中的所有列、度量值和层次结构，并按其显示文件夹进行分组。 使用树状视图上方的按钮，可切换显示文件夹、隐藏对象、特定类型的对象，或按名称筛选对象。 在树状视图中的任意位置右键单击，会弹出包含常用操作的上下文菜单，例如添加新度量值、将对象设为隐藏、复制对象、删除对象等。 按 F2 可重命名当前选中的对象；或多选后右键单击，以批量重命名多个对象。

![批量重命名可让你同时重命名多个对象](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/BatchRename.png)

在主 UI 的右上角，你会看到 DAX编辑器，可用于编辑模型中任意度量值或计算列的 DAX 表达式。 单击“DAX Formatter”按钮，通过 www.daxformatter.com 自动格式化代码。 单击“DAX Formatter”按钮，通过 www.daxformatter.com 自动格式化代码。

使用右下角的属性网格，检查并设置对象的属性，例如格式字符串、说明及其翻译，以及透视成员资格。 使用右下角的属性网格，检查并设置对象的属性，例如格式字符串、说明及其翻译，以及透视成员资格。 你也可以在此设置显示文件夹属性，但更简单的做法是直接在树状视图中拖放对象来更新其显示文件夹（可尝试使用 CTRL 或 SHIFT 选择多个对象）。

要编辑透视或翻译（区域设置），请在树状视图中选择“Model”对象，然后在属性网格中找到“Model Perspectives”或“Model Cultures”属性。 点击小省略号按钮，打开集合编辑器，以添加、删除或编辑透视和区域设置。 点击小省略号按钮，打开集合编辑器，以添加、删除或编辑透视和区域设置。

![编辑透视——点击右侧的省略号按钮](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/Edit%20Perspectives.png)

要将更改保存回 Model.bim 文件，单击保存按钮或按 CTRL+S。 如果你打开的是现有 Tabular 数据库，更改将直接保存回该数据库。 如果自你将数据库加载到 Tabular Editor 后该数据库发生过更改，系统会提示你。 你始终可以按 CTRL+Z 撤销更改。

如果要将模型部署到其他位置，请转到“Model”菜单并选择“Deploy”。

## 部署

Tabular Editor 自带部署向导 Deployment Wizard，相比从 SSDT 部署有一些优势——尤其是在部署到现有数据库时。 在选择要部署到的服务器和数据库后，本次部署你可以选择以下选项： 在选择要部署到的服务器和数据库后，本次部署你可以选择以下选项：

![Deployment Wizard](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/Deployment.png)

不勾选“Deploy Connections”复选框，将确保目标数据库中的所有数据源保持不变。 如果你的模型中有一个或多个表所使用的数据源在目标数据库中不存在，则会报错。 如果你的模型中有一个或多个表所使用的数据源在目标数据库中不存在，则会报错。

同样，不勾选“Deploy Table Partitions”将确保表上的现有分区不会被更改，从而保持分区中的数据不受影响。

勾选“Deploy Roles”后，目标数据库中的角色会更新为与已加载模型一致；但如果不勾选“Deploy Role Members”，则目标数据库中各角色的成员将保持不变。

## 命令行用法

你可以使用命令行进行自动化部署。 GUI 中提供的所有部署选项，命令行同样支持。 GUI 中提供的所有部署选项，命令行同样支持。

### 部署示例

`TabularEditor.exe c:\Projects\Model.bim`

打开 Tabular Editor 的 GUI 并加载指定的 Model.bim 文件（不部署任何内容）。

`TabularEditor.exe c:\Projects\Model.bim -deploy localhost AdventureWorks`

将指定的 Model.bim 文件部署到 localhost 上运行的 SSAS 实例，并覆盖现有或创建新的 AdventureWorks 数据库。 不会加载 GUI。 不会加载 GUI。

默认情况下，目标数据库中的分区、数据源和角色不会被覆盖。 你可以在上述命令后添加以下一个或多个开关参数，以更改此行为：

- `-P` 覆盖 **p**artitions：分区
- `-C` 覆盖 **c**onnections（连接，即数据源）
- `-R` 覆盖 **r**oles：角色
- `-M` 覆盖角色 **m**embers：成员

有关命令行选项的更多信息，请参见[这里](../features/Command-line-Options.md)。

> [!NOTE]
> 由于 TabularEditor.exe 是一个 Windows Forms 应用程序，从命令行运行时会在不同的线程中执行，并会立即将控制权返回给调用方。 在批处理作业中运行部署时，这可能会引发问题，因为你需要等待部署成功完成后才能继续执行作业。 如果你遇到此类问题，请使用 `start /wait` 让 TabularEditor 先完成工作，再将控制权返回给调用方： 在批处理作业中运行部署时，这可能会引发问题，因为你需要等待部署成功完成后才能继续执行作业。 如果你遇到此类问题，请使用 `start /wait` 让 TabularEditor 先完成工作，再将控制权返回给调用方：
>
> `start /wait TabularEditor.exe c:\Projects\Model.bim -deploy localhost AdventureWorks`

## 高级脚本编写

Tabular Editor 允许你使用 C# 通过脚本方式修改已加载的模型。 当你需要一次性对大量对象应用多项更改时，这很实用。 高级脚本编辑器可访问两个对象： 当你需要一次性对大量对象应用多项更改时，这很实用。 高级脚本编辑器可访问两个对象：

- `Selected`，表示资源管理器树中当前选中的所有对象。
- `Model`，表示整个 Tabular Object Model 树。

高级脚本编辑器提供有限的 IntelliSense 功能，帮助你快速上手：

![IntelliSense 帮助你为 Tabular Editor 创建脚本](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/AdvancedEditor%20intellisense.png)

有关高级脚本编写的更多文档和示例，可在[此处](../how-tos/Advanced-Scripting.md)找到。
