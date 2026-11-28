---
uid: getting-started-te2
title: Tabular Editor 2 入门
author: Morten Lønskov
updated: 2026-11-19
description: 安装 Tabular Editor 2（面向 Analysis Services 和 Power BI 语义模型的免费开源编辑器），然后打开、编辑和部署模型。Tabular Editor 3 是商业版本，提供 30 天免费试用。
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      none: true
---
# Tabular Editor 2 入门

Tabular Editor 2 是一款免费的开源 Windows 应用程序，用于编辑 Analysis Services 和 Power BI 语义模型。本页介绍了安装、打开和编辑模型、部署、命令行和 C# 脚本。

[!include[te2-te3-note](../includes/te2-te3-note.partial.md)]

## 按任务划分的工具

Tabular Editor 2、Tabular Editor 3 和 [Tabular Editor CLI](xref:te-cli) 涵盖不同的任务：

| 任务 | 工具 | 文档 |
|------|------|---------------|
| 在免费的桌面应用程序中编辑模型元数据 | Tabular Editor 2 | 本页 |
| 使用自动补全功能编写 DAX，并在调试器中单步执行 | Tabular Editor 3 | @dax-debugger |
| 运行 DAX 查询并预览表格数据 | Tabular Editor 3 | @refresh-preview-query |
| 从 CI/CD 管道部署 | Tabular Editor 2 或 Tabular Editor CLI | @command-line-options、@te-cli-cicd |
| 运行 Best Practice Analyzer 检查 | 三者均可 | @best-practice-analyzer |
| 让 AI 代理读取、查询和更改在桌面应用程序中打开的模型 | Tabular Editor 3 | @mcp-server |
| 让 AI 代理从终端更改模型文件或已部署的模型 | Tabular Editor CLI | @te-cli-skill |

## 安装

从[发布页面](https://github.com/TabularEditor/TabularEditor/releases/latest)下载 .msi 安装程序或便携式 .zip 文件。运行 .msi，或将 .zip 解压缩到文件夹并运行 `TabularEditor.exe`。

.msi 将 Tabular Editor 2 注册为 Power BI Desktop 中的[外部工具](xref:desktop-integration)。

## 前提条件

Tabular Editor 2 需要 [.NET Framework 4.8](https://dotnet.microsoft.com/download/dotnet-framework/net48)。如果缺少 .NET Framework 4.8，.msi 安装程序将停止，并提供下载链接。

> [!NOTE]
> Tabular Editor 2 使用 [Tabular Object Model](https://learn.microsoft.com/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo) (TOM) 加载和保存 Model.bim 文件或现有数据库中的元数据。安装程序包含[Analysis Services 客户端库](https://learn.microsoft.com/analysis-services/client-libraries)。

## 系统要求

- **操作系统：** .NET Framework 4.8 支持的 Windows 版本
- **.NET Framework：**[4.8](https://dotnet.microsoft.com/download/dotnet-framework/net48)

## 打开模型

使用**文件 > 打开 > 从文件...** (**Ctrl+O**) 从磁盘打开模型。支持的格式包括 Model.bim 文件、使用[保存到文件夹](xref:save-to-folder)（database.json）保存的文件夹、[TMDL](xref:tmdl) 文件夹、.pbit 文件和 .pbip 项目。

使用**文件 > 打开 > 从数据库…** (**Ctrl+Shift+O**)打开已部署的数据库。**连接到 Tabular Server** 对话框会要求提供服务器名称和身份验证：

![正在连接到已部署的表格模型](~/content/assets/images/getting-started-te-01.png)

服务器名称接受 Analysis Services 实例和 Azure Analysis Services 服务器 (`asazure://<servername>`)。**本地实例**下拉列表列出了正在运行的 Power BI Desktop、Visual Studio 集成工作区和本地 Analysis Services 实例。从 2025 年 6 月的 Power BI Desktop 更新开始，外部工具可以更改托管在 Power BI Desktop 中的模型的任何部分。请参阅 @desktop-integration。

选择**确定**，然后从服务器上的列表中选择一个数据库。

## 编辑模型

模型加载后，主窗口如下所示：

![Tabular Editor 的主界面](~/content/assets/images/getting-started-te-02.png)

左侧的树状视图列出了模型中的所有表格。展开表以查看其列、度量值和层次结构，这些内容按显示文件夹分组。树上方的按钮用于切换显示文件夹、隐藏对象和对象类型，文本框用于按名称筛选对象。在树中右键单击，即可执行常见操作，例如添加度量值、隐藏、复制和删除对象。按 **F2** 可重命名所选对象。当您选择多个对象时，按 **F2** 将打开**批量重命名**：

![批量重命名让您可以同时重命名多个对象](~/content/assets/images/getting-started-te-03.png)

右上角的**表达式编辑器**用于编辑所选度量值或计算列的 DAX 表达式。**格式化DAX**通过[DAX Formatter](https://www.daxformatter.com)格式化表达式。

右下角的属性网格显示并设置对象属性，例如 `FormatString`、`Description`、翻译和透视成员资格。要一次更改多个对象的`DisplayFolder`，请使用**Ctrl**或**Shift**选中这些对象，然后将它们拖动到树中的文件夹。

要编辑透视或翻译，请在树中选择“**模型**”对象，然后选择 `Perspectives` 或 `Cultures` 属性旁边的省略号按钮。集合编辑器将打开，用于添加、删除和编辑项：

![编辑透视 - 点击右侧的省略号按钮](~/content/assets/images/getting-started-te-04.png)

按 **Ctrl+S** 保存。从文件打开的模型将保存回该文件，从数据库打开的模型将保存回数据库。如果您加载已部署的数据库后有人对其进行了更改，则会显示**更改冲突**提示，询问是否要覆盖它。按 **Ctrl+Z** 撤消，按 **Ctrl+Y** 恢复。

## 部署

**“模型”>“部署...”**将打开部署向导，该向导会将已加载的模型部署到服务器。选择服务器和数据库后，选择要部署模型的哪些部分：

![部署向导](~/content/assets/images/getting-started-te-05.png)

| 选项 | 取消选中时 |
|--------|--------------|
| **部署数据源** | 目标数据库上的数据源保持不变。如果表格使用目标上不存在的数据源，则部署将失败。|
| **部署表分区** | 目标上的分区保持不变，其数据也保持不变。|
| **部署受增量刷新策略管理的分区** | 由增量刷新创建的分区保持原样。需要**部署表分区**。|
| **部署共享表达式** | 目标上的共享表达式保持不变。需要兼容级别 1400 或更高版本。|
| **部署角色** | 目标上的角色保持不变。|
| **部署角色成员** | 目标上的角色成员保持不变。需要**部署角色**。|

当目标是现有数据库时，始终会选中**部署模型结构**。当模型包含该类型的对象时，默认选中其他选项；当模型包含角色成员时，选中**部署角色**。如果数据库尚不存在，则向导会使用模型部署数据源、分区和共享表达式，并且仅应用角色选项。摘要页面还包含**导出生成...**，用于为 Analysis Services Deployment Wizard 写入部署文件，以及**TMSL 脚本**，用于将部署显示为 TMSL 脚本。

## 命令行

`TabularEditor.exe` 从命令行运行部署、脚本和 Best Practice Analyzer 检查。以下示例部署了一个模型：

`TabularEditor.exe c:\Projects\Model.bim`

打开 Tabular Editor 2 并加载 Model.bim 文件，但不部署任何内容。

`TabularEditor.exe c:\Projects\Model.bim -deploy localhost AdventureWorks`

在本地主机的 Analysis Services 实例上创建 AdventureWorks 数据库，而不打开用户界面。如果数据库已存在，则部署失败。

`TabularEditor.exe c:\Projects\Model.bim -deploy localhost AdventureWorks -O -P -R -M`

覆盖现有的 AdventureWorks 数据库，包括其分区、角色和角色成员。

在数据库名称后添加以下开关，以控制部署要覆盖的内容：

- `-O` 覆盖现有数据库
- `-C` 覆盖数据源（**连**接）
- `-P` 覆盖**p**artition（分区）
- `-Y` 跳过具有增量刷新策略的分区（使用 `-P`）
- `-S` 覆盖**共**享表达式
- `-R` 覆盖**角色**
- `-M` 覆盖角色**成**员（使用 `-R`）

如果没有这些开关，目标上的数据源、分区、共享表达式和角色将保持原样。@command-line-options 列出了每个开关，包括脚本、Best Practice Analyzer 检查以及 Azure DevOps 和 GitHub Actions 的输出。

> [!NOTE]
> `TabularEditor.exe` 是一款 Windows Forms 应用程序，因此命令行调用会在部署完成之前返回。在等待部署的批处理作业中，请使用 `start /wait`：
>
> `start /wait TabularEditor.exe c:\Projects\Model.bim -deploy localhost AdventureWorks`

[Tabular Editor CLI](xref:te-cli) 在 Windows、macOS 和 Linux 上运行，并接受大多数 `TabularEditor.exe` 开关。请参阅 @te-cli-migrate。

## C# 脚本

**C# Script**选项卡对加载的模型运行C#代码。使用它可将相同的更改一次性应用于多个对象。脚本可以访问两个对象：

- `Selected` 包含在树中选定的对象。
- `Model` 包含整个 Tabular Object Model。

脚本编辑器具有基本的 IntelliSense 功能：

![IntelliSense 帮助您为 Tabular Editor 创建脚本](~/content/assets/images/getting-started-te-06.png)

Tabular Editor 2 将此功能称为“高级脚本”。请参阅 @advanced-scripting，了解脚本 API 和示例。

## 功能比较

下表对 Tabular Editor 2、Tabular Editor 3 和 Tabular Editor CLI 进行了比较：

[!include[feature-comparison](../includes/feature-comparison.partial.md)]

## 后续步骤

- @migrate-from-te2 介绍了 Tabular Editor 2 和 Tabular Editor 3 之间的功能差异。
- @getting-started 介绍了如何安装 Tabular Editor 3 并开始免费试用。
- @te-cli-skill 安装一项技能，用于向 AI 编码代理教授 Tabular Editor CLI 命令。
