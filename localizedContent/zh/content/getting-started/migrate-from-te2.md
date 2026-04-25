---
uid: migrate-from-te2
title: 从 Tabular Editor 2.x 迁移
author: Daniel Otykier
updated: 2021-09-30
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 从 Tabular Editor 2.x 迁移

本文面向已具备一定经验、使用 Tabular Editor 2.x 进行 Power BI Dataset 或 Analysis Services Tabular 开发的开发者。 本文重点介绍 Tabular Editor 3 的相似之处与关键新增功能，帮助你快速上手。

## 并行安装

Tabular Editor 3 的产品代码与 Tabular Editor 2.x 不同。 这意味着你可以将两个工具并排安装，而不会有问题。 实际上，这两个工具会安装到不同的程序文件夹中，它们的设置也分别存放在不同的文件夹里。 换句话说，Tabular Editor 2.x 与 Tabular Editor 3 之间并不适用“升级”或“降级”的说法。 你可以把 Tabular Editor 3 当作一款完全不同的产品。

## 功能对比

从功能角度来看，除少数例外，Tabular Editor 3 基本上是 Tabular Editor 2.x 的超集。 下表对比了两款工具的所有主要功能：

|                                                                   | Tabular Editor 2.x                      | Tabular Editor 3                                          |
| ----------------------------------------------------------------- | ------------------------------------------------------- | --------------------------------------------------------- |
| 编辑所有 TOM 对象及其属性                                                   | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| 批量编辑和重命名                                                          | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| 支持复制/粘贴和拖放                                                        | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| 撤销/重做 Data model 建模操作                                             | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| 从磁盘加载/保存模型元数据                                                     | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>\* |
| 保存到文件夹                                                            | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>\* |
| 与 [daxformatter.com](https://daxformatter.com) 集成 | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| 高级 Data model 建模（OLS、透视图、计算组、元数据翻译等）                              | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>\* |
| 语法高亮与公式自动修复                                                       | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| 查看对象间的 DAX 依赖关系                                                   | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| 导入表向导                                                             | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| Deployment Wizard                                                 | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>\* |
| Best Practice Analyzer                                            | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| C# Script 脚本和自动化                                                  | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| 作为 Power BI Desktop 的外部工具使用                                       | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   |
| 连接到 SSAS/Azure AS/Power BI Premium                                | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>\* |
| 命令行接口                                                             | <span class="emoji">&#10004;</span> | _[即将推出](xref:roadmap)_                                    |
| 高级且可自定义的用户界面，支持高 DPI、多显示器和主题                                      |                                                         | <span class="emoji">&#10004;</span>   |
| 世界级 DAX 编辑器，具备类似 IntelliSense<sup>TM</sup> 的特性                    |                                                         | <span class="emoji">&#10004;</span>   |
| 离线 DAX 语法检查与列和数据类型推断                                              |                                                         | <span class="emoji">&#10004;</span>   |
| 改进的表导入向导和表架构更新检查，并支持 Power Query                                  |                                                         | <span class="emoji">&#10004;</span>   |
| DAX 查询、表格预览和 Pivot Grid                                           |                                                         | <span class="emoji">&#10004;</span>   |
| 创建图表，用于可视化和编辑表关系                                                  |                                                         | <span class="emoji">&#10004;</span>   |
| 在后台执行数据刷新操作                                                       |                                                         | <span class="emoji">&#10004;</span>\* |
| C# 宏录制器                                                           |                                                         | <span class="emoji">&#10004;</span>   |
| 使用 DAX脚本在单个文档中编辑多个 DAX 表达式                                        |                                                         | <span class="emoji">&#10004;</span>   |
| 集成 [VertiPaq分析器](https://www.sqlbi.com/tools/vertipaq-analyzer/)  |                                                         | <span class="emoji">&#10004;</span>   |

\***注意：** 具体限制取决于你使用的 Tabular Editor 3 [版本](xref:editions)。

## 功能差异

以下总结了主要的功能差异。

### 用户界面

启动 Tabular Editor 3 时，你首先会注意到全新的、类似 Visual Studio Shell 的界面。 这个界面完全可自定义，支持高 DPI、多显示器，还能更换主题。 所有界面元素都可以拖动到不同位置。因此，如果你更喜欢 Tabular Editor 2.x 的界面布局，可以直接在 **Window** 菜单中选择 **Classic layout**。

不过总体而言，Tabular Editor 2.x 中已有的界面元素在 Tabular Editor 3 里名称保持一致，因此你应该能比较轻松地上手新界面。 下面列出了一些重要差异：

- Tabular Editor 2.x 中的 **Advanced Scripting** 选项卡已不再提供。 在 Tabular Editor 3 中，你需要改为通过 **File > New** 菜单创建 **C# Script**。 你不再局限于一次只能处理一个脚本。 此外，**Custom actions** 已更名为 **宏**。
- TOM Explorer 目前不支持 **Dynamic LINQ filtering**。 如果你想使用 [Dynamic LINQ](https://dynamic-linq.net/expression-language) 查找对象，需要按 CTRL+F 打开 **Find and replace** 对话框。
- 如果你关闭了 **表达式编辑器**，可以在 **TOM Explorer** 中双击某个对象的图标将其重新打开，或选择 **View > Expression Editor** 菜单项。
- 在 Tabular Editor 3 的默认布局中，**Best Practice Analyzer** 会作为一个选项卡显示在 **TOM Explorer** 旁边。 在这里，你还会看到全新的 **数据刷新** 视图（用于查看后台刷新操作队列）以及 **宏** 视图（用于管理此前从 C# Script 保存的宏）。
- Tabular Editor 3 会在全新的 **信息视图** 中显示所有 DAX 语法和语义错误。 在默认布局中，它位于界面左下角。
- 此外，Tabular Editor 3 还包含 **VertiPaq分析器**（你可能在 [DAX Studio](https://daxstudio.org/) 里见过它）。
- 最后补充一点：Tabular Editor 3 引入了 **文档** 的概念，这是一个统称，用来指代 C# Script、DAX脚本、DAX 查询、图示、数据预览和 Pivot Grid。

想了解更多信息，可以看看 <xref:user-interface>。

### 新的 DAX 编辑器与语义功能

Tabular Editor 3 拥有自己的 DAX 解析引擎（又称“语义分析器”），这意味着该工具现在能够理解模型中任何 DAX 代码的语义。 这个引擎也用来驱动我们的 DAX 编辑器（代号“Daxscilla”），并支持语法高亮、自动格式化、代码补全、参数提示、重构等更多功能。 当然，编辑器也高度可配置，你可以根据自己偏好的 DAX 编码风格进行调整。

想了解更多关于新 DAX 编辑器的内容，可以看看 <xref:dax-editor>。

此外，语义分析器会持续 Report 模型中所有对象的任何 DAX 语法或语义错误。 即使未连接到 Analysis Services，这也同样有效，而且速度快得惊人。 语义分析器还使 Tabular Editor 3 能够从 DAX 表达式中自动推断数据类型。 换句话说，Tabular Editor 3 会自动检测计算表格表达式将生成哪些列。 与 Tabular Editor 2.x 相比，这是一个很大的改进：在之前的版本中，你必须在计算表格上手动映射列，或依赖 Analysis Services 返回列元数据。

### 支持 Power Query 的表导入和架构更新

与 Tabular Editor 2.x 相比，Tabular Editor 3 的另一大优势是支持 Structured数据源以及 Power Query (M) 分区。 具体来说，“架构更新”功能现在适用于这些类型的数据源和分区，并且表导入向导在导入新表时可以生成所需的 M 代码。

架构比较对话框本身也有多项改进，例如允许你轻松将“列删除 + 列插入”操作映射为一次“列重命名”操作（反之亦然）。 此外还提供了选项，用于控制如何处理浮点和十进制数据类型（例如，有时你的数据源使用的是浮点数据类型，但你可能仍希望始终将其导入为十进制类型）。

要了解更多信息，请参阅 <xref:importing-tables>。

<a name="workspace-mode"></a>

### 工作区模式

Tabular Editor 3 引入了 **工作区模式** 的概念：模型元数据从磁盘（Model.bim 或 Database.json）加载后，会立即部署到你选择的 Analysis Services 实例中。 每当你点击“保存”（CTRL+S）时，Workspace 数据库都会同步，并将更新后的模型元数据保存回磁盘。 这种方式的优势在于，Tabular Editor 会连接到 Analysis Services，从而启用下面列出的[已连接功能](#connected-features)，同时也便于更新磁盘上的源文件。 在 Tabular Editor 2.x 中，你必须从数据库打开模型，然后还得记得隔一段时间手动保存到磁盘。

这种方式非常适合实现[并行开发](xref:parallel-development)，并将模型元数据集成到版本控制系统中。

要了解更多信息，请参阅 <xref:workspace-mode>。

<a name="connected-features"></a>

### 已连接功能

Tabular Editor 3 包含多项新的已连接功能，让你可以将其用作 Analysis Services 的客户端工具。 这些功能会在 Tabular Editor 3 连接到 Analysis Services 时启用——不管是直接连接，还是使用[工作区模式](#workspace-mode)功能。

新的已连接功能包括：

- 表数据预览
- PivotGrids
- DAX 查询
- 数据刷新操作
- VertiPaq分析器

### 模型关系图

Tabular Editor 2.x 中一个呼声很高的需求是：能够更好地可视化表之间的关系。 使用 Tabular Editor 3，你现在可以创建模型关系图。 每个图表都是一个简单的 JSON 文件，用于保存要包含在图表中的表名称及其坐标。 随后，Tabular Editor 3 会呈现这些表和关系，并提供便于编辑关系、基于现有关系向图表添加更多表等功能。

![轻松添加相关表](~/content/assets/images/diagram-menu.png)

更多信息请参阅[使用图表](xref:importing-tables-data-modeling#working-with-diagrams)。

### C# Script 与宏录制器

Tabular Editor 2.x 的 **Advanced Scripting** 功能在 Tabular Editor 3 中延续为 **C# Script**。 Tabular Editor 3 的一个重要差异是，你不再局限于只能使用单个脚本。 相反，使用 **文件 > 新建 > C# Script** 选项，你可以按需创建并使用任意数量的 C# Script。 与 Tabular Editor 2.x 类似，这些脚本可以保存为可复用的操作，并直接集成到 TOM Explorer 的右键上下文菜单中。 在 Tabular Editor 3 中，我们将这些操作称为 **宏**，你甚至可以创建自己的菜单和工具栏，并在其中添加宏。

更重要的是，Tabular Editor 3 提供了 **宏录制器**，可根据用户操作自动生成 C# 代码。

要了解更多信息，请参阅 @cs-scripts-and-macros。

### DAX脚本

如果你是从 Tabular Editor 2.x 迁移过来，需要了解的最后一个重要功能是 **DAX脚本**。 借助此功能，你可以创建文档，一次性编辑多个计算对象的 DAX 表达式和基本属性。 计算对象包括度量值、计算列、计算表格等。

当你需要在多个对象之间编写复杂的业务逻辑时，这会非常方便。 在 TOM Explorer 中（多）选中对象后，右键并选择 **Script DAX** 选项，即可生成一个新的 DAX脚本，其中包含所有已选对象的定义。 当然，DAX脚本编辑器具备与表达式编辑器和 DAX 查询编辑器相同的全部 DAX 能力。

在 **连接** 或 **Workspace** 模式下，DAX脚本是一项非常强大的工具，可用于快速修改并测试更新后的业务逻辑。例如，如下图所示，你可以将其与 Pivot Grid 配合使用。 只需按下 SHIFT+F5，就会根据脚本中的 DAX 表达式更新数据库，随后 Pivot Grid 会立即刷新。

![Dax 脚本与 Pivot](~/content/assets/images/dax-scripting-and-pivot.png)

要了解更多信息，请参阅 @dax-script-introduction。

## 后续步骤

- @migrate-from-vs
- @parallel-development
- @boosting-productivity-te3
