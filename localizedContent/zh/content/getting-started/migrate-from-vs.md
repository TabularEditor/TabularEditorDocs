---
uid: migrate-from-vs
title: 从 Visual Studio 迁移
author: Daniel Otykier
updated: 2021-09-30
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: 桌面版
          none: true
        - edition: 商业版
          full: true
        - edition: 企业版
          full: true
---

# 从 Visual Studio / SQL Server Data Tools 迁移

本文假设你已熟悉使用 [Analysis Services Projects for Visual Studio](https://marketplace.visualstudio.com/items?itemName=ProBITools.MicrosoftAnalysisServicesModelingProjects)（原名 SQL Server Data Tools）进行表格模型开发。 这在使用 SQL Server Analysis Services（Tabular）或 Azure Analysis Services 的开发者中很常见。

- 如果你从未使用过 Visual Studio 进行表格模型开发，可以放心跳过本主题。
- 如果你之前使用 Tabular Editor 2.x 进行表格模型开发，我们建议你直接跳转到 @migrate-from-te2 一文。

## 部分迁移

Tabular Editor 3 提供了一些功能，让你在表格模型开发中可以完全不再依赖 Visual Studio。 相比之下，在 Tabular Editor 2.x 中，一些用户仍更喜欢用 Visual Studio 来做表导入、可视化关系以及预览数据等工作。

不过，随着你逐渐熟悉 Tabular Editor 3，你可能仍会觉得时不时在 Visual Studio 中打开表格模型很有用。 这在任何时候都可行，因为 Tabular Editor 3 不会修改 Visual Studio 使用的 **Model.bim** 文件格式（即 [TOM JSON](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions)），从而确保与 Visual Studio 兼容。

唯一的例外是，如果你选择使用 Tabular Editor 的 [保存到文件夹](xref:parallel-development#what-is-save-to-folder) 功能，因为这种文件格式不受 Visual Studio 支持。 不过，你可以在 Tabular Editor 中通过 **File > Save As...** 选项，轻松重新生成供 Visual Studio 使用的 Model.bim 文件。 反向转换也可以这样做：在 Tabular Editor 中加载 Model.bim 文件，然后使用 **File > 保存到文件夹...** 选项即可。

### 自动化文件格式转换

如果你经常需要在 Tabular Editor 的基于文件夹的格式（Database.json）与 Visual Studio 的文件格式（model.bim）之间来回转换，可以考虑使用 [Tabular Editor 2.x CLI](xref:command-line-options) 编写一个简单的 Windows 命令脚本来自动化这一转换过程。

# [Model.bim 转换为文件夹](#tab/frombim)

要将 model.bim 转换为 Database.json（基于文件夹的格式）：

```cmd
tabulareditor.exe model.bim -F Database.json
```

# [从文件夹转换为 model.bim](#tab/fromfolder)

要将 Database.json（基于文件夹的格式）转换为 model.bim：

```cmd
tabulareditor.exe Database.json -B model.bim
```

***

> [!NOTE]
> 上述命令行脚本假定你已安装 [Tabular Editor 2.x](xref:getting-started-te2)。 另外，你也需要把 Tabular Editor 2.x 的安装位置加入你的 [PATH 环境变量](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/path)。

## 集成 Workspace 服务器

在 Visual Studio 中启动新的 Analysis Services（Tabular）项目时，系统会提示你选择使用 Visual Studio 的集成 Workspace 服务器，还是提供你自己的 Analysis Services 实例。 此外，你还必须选择该表格模式模型的兼容级别（见下方截图）。

![VS New Project](~/content/assets/images/vs-new-project.png)

相比之下，在 Tabular Editor 中创建新模型时，是否使用 Workspace 服务器完全是可选的（但建议使用——请参阅 [工作区模式](xref:workspace-mode)）。

下面是在 Tabular Editor 3 中创建新模型时显示的对话框：

![New model dialog](~/content/assets/images/new-model.png)

如果你启用 **使用工作区数据库** 选项，Tabular Editor 会提示你输入一个 Analysis Services 实例和数据库名称，作为你在处理模型时使用的 Workspace 数据库。 如果不启用此选项，你仍然可以在“离线”模式下创建并处理模型，依然可以添加表、关系、编写 DAX 表达式等。 但在你能够刷新、预览并查询模型中的数据之前，必须先将离线模型部署到某个 Analysis Services 实例。

> [!IMPORTANT]
> Tabular Editor 3 不提供与 Visual Studio 的 **集成 Workspace** 选项等效的功能。 本质上，集成 Workspace 是由 Visual Studio 管理的一个 Analysis Services 实例。 由于 Analysis Services 是 Microsoft 的专有软件，我们无法将它随 Tabular Editor 3 一起发布。 作为替代方案，如果你希望运行一个供 Tabular Editor 使用的本地 Analysis Services 实例，我们建议你安装 [SQL Server Developer Edition](https://www.microsoft.com/en-us/sql-server/sql-server-downloads)。

### 兼容级别要求

Tabular Editor 允许你为创建 Analysis Services 数据库选择以下兼容级别：

- 1200（Azure Analysis Services / SQL Server 2016+）
- 1400（Azure Analysis Services / SQL Server 2017+）
- 1500（Azure Analysis Services / SQL Server 2019+）

此外，Tabular Editor 还允许你为将通过 [XMLA endpoint](xref:powerbi-xmla) 部署到 Power BI 服务的 Power BI Dataset 选择合适的兼容级别。

> [!NOTE]
> Tabular Editor 不支持低于 1200 的兼容级别，因为这些版本不使用 [Tabular Object Model (TOM)](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) 元数据格式。 如果你计划将兼容级别为 1100 或 1103 的模型开发从 Visual Studio 迁移到 Tabular Editor，那么在迁移到 Tabular Editor 之前，**必须将兼容级别升级到至少 1200**。 这样一来，你将无法再将该模型部署到 SQL Server 2014 Analysis Services。

## Visual Studio 项目

在 Visual Studio 中创建 Analysis Services (Tabular) 项目时，会在项目文件夹中、Model.bim 文件旁创建多个文件。 这些文件包含项目和用户特定的信息，与 Tabular Object Model (TOM) 无关。 下图展示了在 Visual Studio 中新建 Tabular 项目后生成的文件。

![VS Project File Structure](~/content/assets/images/vs-file-structure.png)

迁移到 Tabular Editor 时，你只需要带上 Model.bim 文件，因为这里没有“项目”的概念。 相反，Tabular Editor 会直接从 Model.bim 文件加载模型元数据。 在某些情况下，Model.bim 文件旁还会生成一个名为 [Tabular Model User Options (tmuo) 文件](xref:user-options) 的文件。 Tabular Editor 使用该文件来存储与用户和模型相关的特定设置，例如是否使用 Workspace 数据库、数据源的（加密）用户凭据等。

为保持“项目”目录整洁，我们建议在 Tabular Editor 加载文件之前，先将 Visual Studio 创建的 Model.bim 文件复制到一个新目录中。

![Te File Structure](~/content/assets/images/te-file-structure.png)

如果你想使用 [保存到文件夹](xref:parallel-development#what-is-save-to-folder) 功能（建议用于并行开发以及与版本控制系统集成），现在就可以在 Tabular Editor 中将模型保存为文件夹 (**文件 > 保存到文件夹...**)。

![Te Folder Structure](~/content/assets/images/te-folder-structure.png)

## 版本控制

Tabular Editor 不提供任何用于模型元数据的集成版本控制功能。 不过，由于所有模型元数据都以纯文本（JSON）文件的形式存放在磁盘上，将 Tabular 模型元数据纳入任何类型的版本控制系统都很容易。 因此，大多数 Tabular Editor 用户仍然倾向于保留 Visual Studio，以便使用 [Visual Studio Team Explorer](https://docs.microsoft.com/en-us/azure/devops/user-guide/work-team-explorer?view=azure-devops) 或者（特别是针对 git）使用 Visual Studio 2019 的新 [Git Changes 窗口](https://docs.microsoft.com/en-us/visualstudio/version-control/git-with-visual-studio?view=vs-2019)。

> [!NOTE]
> 如今，大多数开发人员似乎更倾向于使用 [git](https://git-scm.com/) 作为版本控制系统。 Tabular Editor 3 的 Git 集成计划在未来的更新中推出。

迁移到 Tabular Editor 后，你无需再保留 Visual Studio 创建的原始 Tabular 模型项目及其配套文件。 你仍然可以使用 Visual Studio Team Explorer 或 Git Changes 窗口来查看代码更改、管理版本控制分支、执行提交、合并等操作。

当然，大多数版本控制系统也都有自己的一套工具，你无需依赖 Visual Studio 也能使用。 例如，Git 有命令行工具，也有许多直接集成到 Windows 资源管理器中的热门工具，例如 [TortoiseGit](https://tortoisegit.org/)。

### 保存到文件夹与版本控制

使用 [Save-to-folder](xref:parallel-development#what-is-save-to-folder) 选项的主要优势是：模型元数据会拆分为多个小文件，而不是把所有内容都存到一个大型 JSON 文档中。 TOM 中的许多属性都是对象数组（例如表、度量值和列）。 由于所有此类对象都有明确的名称，它们在数组中的顺序并不重要。 有时在序列化为 JSON 时顺序会被改变，这会导致大多数版本控制系统提示该文件发生了更改。 不过，由于这种排序并不具有任何语义意义，我们不必为这类更改可能引发的合并冲突而费心。

采用 Save-to-folder 序列化后，JSON 文件中使用的数组数量会大幅减少：原本以数组形式存储的对象现在被拆分为单独的文件，并存放在子文件夹中。 当 Tabular Editor 从磁盘加载模型元数据时，会遍历所有这些子文件夹，确保所有对象都能正确反序列化到 TOM 中。

因此，当两个或更多开发者对同一个表格模型进行并行更改时，Save-to-folder 序列化能大大降低遇到合并冲突的概率。

## 界面差异

本节列出 Tabular Editor 3 与 Visual Studio 在表格模型开发用户界面方面最重要的差异。 如果你是 Visual Studio 的资深用户，你会很快适应 Tabular Editor 3 的用户界面。 如果你想看更详细的讲解，可以查看 <xref:user-interface>。

### Tabular Model Explorer 与 TOM Explorer 对比

在 Visual Studio 中，你可以在 **Tabular Model Explorer** 中看到模型元数据的层次结构概览。

![Vs Tom Explorer](~/content/assets/images/vs-tom-explorer.png)

在 Tabular Editor 中，这个视图称为 **TOM Explorer**。 在 Tabular Editor 中，所有数据建模通常都围绕着在 TOM Explorer 中找到相关对象，然后通过调用右键上下文菜单、导航到主菜单，或在 **Properties** 视图中编辑对象属性来执行相应操作。 在 Tabular Editor 中，你可以在所有数据建模操作中使用直观的多选、拖放、复制粘贴以及撤销/重做等操作。

![Vs Tom Explorer](~/content/assets/images/tom-explorer.png)

Tabular Editor 中的 TOM Explorer 还提供一些快捷选项，可快速显示/隐藏特定类型的对象、隐藏对象和显示文件夹，并支持对元数据层次结构进行快速搜索与筛选。

更多信息见 @tom-explorer-view。

### 属性网格

Visual Studio 和 Tabular Editor 都提供属性网格，让你可以编辑当前所选对象的大多数属性。 下面对比的是同一个度量值在 Visual Studio 的属性网格（左）和 Tabular Editor 的属性网格（右）中的显示：

![Visual Studio 与 Tabular Editor 中的属性网格](~/content/assets/images/property-grid-vs-te.png)

两者的工作方式总体相同，不过 Tabular Editor 使用的属性名称与 TOM 对象属性更一致。 Tabular Editor 还新增了一些 TOM 中没有的属性，以便更轻松地完成某些建模操作。 例如，展开 **Translated Names** 属性后，你可以在模型的所有区域设置之间对比并编辑对象名称的翻译。

### 编辑 DAX 表达式

在 Visual Studio 中，你可以使用公式栏；也可以在“表格模型资源管理器”中右键单击某个度量值，并选择“编辑公式”来打开 DAX 编辑器窗口。

Tabular Editor 也差不多，只是用 **表达式编辑器** 视图替代了公式栏。 另外，如果你想在独立文档中编辑一个或多个对象（度量值、计算列、计算表格）的 DAX 表达式，可以右键单击这些对象，然后选择 **Script DAX**。

Tabular Editor 3 的 DAX 代码编辑器，是很多人选择这款工具的主要原因之一。 你可以在[此处](xref:dax-editor)了解更多。

### 错误列表与信息视图

在 Visual Studio 中，DAX 语法错误会以警告的形式显示在 **错误列表** 中（见下方截图）。 此外，包含错误的度量值会在度量值网格中用一个警告三角形标记出来。

![Vs 错误列表](~/content/assets/images/vs-error-list.png)

在 Tabular Editor 中，你可以用信息视图来汇总模型开发过程中不同来源发布的所有错误、警告和信息。 针对 DAX 语法错误，这些会在信息视图中显示为错误；任何包含错误的度量值都会在 TOM Explorer 中用红点标记（见下方截图）。

![Te 信息](~/content/assets/images/te-messages.png)

在上面的截图中，你可以看到有三个不同的信息发布来源：

- **Analysis Services**：当元数据更改保存到已连接的 Analysis Services 实例时，服务器会更新 TOM 元数据，以标明是否有对象处于错误状态。 具体来说，度量值的 [State](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.measure.state?view=analysisservices-dotnet#Microsoft_AnalysisServices_Tabular_Measure_State) 和 [ErrorMessage](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.measure.errormessage?view=analysisservices-dotnet#Microsoft_AnalysisServices_Tabular_Measure_ErrorMessage) 属性会被更新。 Tabular Editor 会在信息视图中显示这些错误信息。 当 Tabular Editor 以脱机方式使用（即未连接到 Analysis Services）时，不会显示这些信息。
- **Tabular Editor 语义分析**：此外，Tabular Editor 3 会对模型中的所有 DAX 表达式执行其自身的语义分析。 遇到的任何语法或语义错误都会在此处的 Report 中报告。
- **表达式编辑器**：最后，如果你在 Tabular Editor 3 中打开了任何文档（例如表达式编辑器），则文档中遇到的任何 DAX 语法或语义错误都会在此处的 Report 中报告。

### 预览表数据

在 Visual Studio 中，加载 Model.bim 文件后，表及其内容会以选项卡式视图显示。 在 Tabular Editor 3 中，你可以在 TOM Explorer 中右键单击某个表，然后选择 **预览数据** 来预览表数据。 这会打开一个新的文档选项卡，你可以滚动查看表的所有行，并对列进行筛选和排序。 它甚至适用于使用 DirectQuery 的模型！

此外，你还可以自由重新排列这些文档选项卡，以便同时查看多个表的内容（见下方截图）。

![Te3 表格预览](~/content/assets/images/te3-table-preview.png)

### 导入表

要在 Tabular Editor 3 中导入新表，请使用 **Model > Import tables...** 选项。 这会启动 Tabular Editor 3 的“导入表向导”，引导你完成连接到数据源并选择要导入的表的流程。 该流程与 Visual Studio 中的旧版表导入相对类似。

一个重要的区别是，Tabular Editor 3 不包含 Visual Power Query 编辑器。 你仍然可以以文本方式编辑 Power Query (M) 表达式；但如果你的模型非常依赖用 Power Query 查询来表达的复杂数据转换，你可以考虑继续用 Visual Studio 来编辑这些 Power Query 查询。

> [!NOTE]
> 由于会增加数据刷新操作的开销，通常不建议在企业级数据建模中使用 Power Query 来执行复杂的数据转换。 相反，建议你使用其他 ETL 工具把数据准备成星型架构，并将星型架构数据存储在关系数据库中，例如 SQL Server 或 Azure SQL Database。 然后，将该数据库中的表导入到你的表格模型中。

#### 编辑分区并更新表架构

在 Tabular Editor 3 中，你可以在不强制刷新表的情况下更新表的架构。 分区会在 TOM Explorer 中作为独立对象显示。 单击某个分区，即可在表达式编辑器中编辑其表达式（M 或 SQL）。

更新分区表达式后，Tabular Editor 可以自动检测更新后的表达式生成的表架构是否与模型中定义的列集合不同。 要执行架构更新，请在 TOM Explorer 中右键单击分区或表，然后选择 **Update table schema...**。

有关表导入和架构更新的更多信息，请参阅 @importing-tables。

### 关系可视化

Visual Studio 包含一个图表工具，可用于可视化并创建表之间的关系。

Tabular Editor 3 同样包含一个图表工具，可通过 **文件 > 新建 > 图表** 访问。 随后会创建一个新的图表文档选项卡。你可以通过从 TOM Explorer 拖放表来添加表，或使用 **图表 > 添加表...** 菜单添加表。

将表添加到图表后，你只需将一列拖到另一列上，即可在列之间创建关系。

![Te3 图表视图](~/content/assets/images/te3-diagram-view.png)

> [!NOTE]
> 出于性能考虑，图表工具不会检查模型数据，也不会验证你创建的任何关系的唯一性或方向性。 你需要自行确保关系创建正确。 如果某个关系定义不正确，Analysis Services 会返回错误状态，并会在 **信息视图** 中显示。

### 模型部署

Tabular Editor 可让你轻松将模型元数据部署到任何 Analysis Services 实例。 你可以在 **模型 > 部署...** 中打开 Tabular Editor 的 Deployment Wizard，或按 CTRL+SHIFT+D。

有关更多信息，请参阅 [模型部署](../features/deployment.md)。

## 后续步骤

- @migrate-from-te2
- @parallel-development
- @boosting-productivity-te3