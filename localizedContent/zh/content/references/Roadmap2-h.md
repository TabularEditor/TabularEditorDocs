# 路线图

> [!IMPORTANT]
> Tabular Editor 2 已不再进行积极开发，我们这边也不会再为其新增或改进任何重大功能。不过，我们仍致力于让它保持最新状态，确保在 Microsoft 发布新的语义模型功能时提供支持，并修复任何严重或阻塞性问题。由于该项目基于 MIT 许可证开源，欢迎任何人提交 Pull Request（PR），我们的团队会进行审核并批准。因此，以下列表应视为已弃用。

- 将对象脚本化为 TMSL 或 DAX（兼容 DAX编辑器）
- 为 DAX 表达式编辑器提供 IntelliSense
- 为 Visual Studio 创建插件，用于启动 Tabular Editor
- 面向开发者的 Tabular Editor 插件架构 / 公共 API
- 使用 VSTS 实现自动化构建、测试、发布和文档生成
- [已完成] 公式修复（即在重命名对象时自动修正 DAX 表达式）
- [已完成] 用于显示对象依赖关系的 UI
- [已完成] 通过命令行生成更改脚本
- [已完成] 支持读取/编辑更多对象类型（表、分区、数据列）
- [已完成] 将 Model.bim 拆分为多个 json 文件（例如每个表一个文件），以便更好地集成到版本控制工作流中。
- [已完成] 导入/导出翻译

## 将对象脚本化为 TMSL 或 DAX

在资源管理器树中选择一个或多个对象时，应能为这些对象生成脚本。实际上，这已经可以通过将对象拖放到另一个文本编辑器（或 SSMS）中来实现，但还应提供类似的右键选项，以便让最终用户更清楚了解正在执行的操作。应支持生成 TMSL 脚本（用于 SSMS）以及可在 [DAX编辑器](https://github.com/DaxEditor/) 中使用的 DAX 风格代码。

目前，度量值和计算列可以在不同的 Tabular Editor 实例之间拖放，以便在模型之间复制；但为了更好地呈现此功能，界面中还应提供一个选项，用于导入提供的 TMSL 片段，来源可以是剪贴板或文件。参见 [这个问题](https://github.com/TabularEditor/TabularEditor/issues/69)。最后，还应启用标准的复制和粘贴快捷键。

## 为 Visual Studio 创建插件，用于启动 Tabular Editor

为 Visual Studio 添加一个简单的上下文菜单扩展：确保 Model.bim 文件已关闭，然后启动 TabularEditor.exe 并加载该 Model.bim 文件。

## 为 DAX 表达式编辑器提供 IntelliSense

在表达式编辑器中编写 DAX 代码时，应弹出自动完成框，帮助补全表名、列名、度量值名称或函数（及其参数）。

也可以看看 [此问题](https://github.com/TabularEditor/TabularEditor/issues/64)。

## 面向开发者的 Tabular Editor 插件架构 / 公共 API

偏好使用 C# 以脚本方式编写表格模型的用户，现在就已经可以改用 TOMWrapper.dll，而无需直接使用 Analysis Services TOM API。这带来了一些好处。例如，借助现成的便捷方法和属性，TOMWrapper 命名空间让处理透视和翻译变得更容易。

更进一步，如果能向开发者开放更多 Tabular Editor 功能，会很有意思：

- 解析 DAX 对象
- 查看 Best Practice Analyzer 的分析结果
- Tabular Editor UI（支持为 Tabular Editor 创建“插件”，可带/不带自定义 UI）

## 使用 VSTS 进行自动化构建、测试、发布和生成文档

使用 VSTS 进行 DevOps，并对 Tabular Editor 源代码进行整体清理。

## 公式修复

当任何模型对象被重命名时，应更新所有引用该对象的 DAX 表达式，以反映名称变更。

**更新**：从 2.2 起，可在“文件”>“偏好”中切换启用此功能。

## 用于显示对象依赖关系的 UI

右键单击度量值或计算列，就会在弹出对话框中显示依赖关系树。应能显示依赖所选对象的对象，或所选对象所依赖的对象。

**更新**：自 2.2 起，此功能已可用。只需右键单击某个对象，然后选择“显示依赖项...”即可。

## 通过命令行以脚本方式应用更改

目前，已可以直接通过命令行部署模型。同样，你也应该能够通过管道传入一个包含要在模型上执行的 C# Script 的 .cs 文件。执行脚本后，应能保存或部署更新后的模型。这需要对当前的命令行选项做一些调整。

**更新**：自 2.3 起，可通过命令行使用 "-S" 开关执行脚本。部署方式与以往相同；但如果你想将修改后的模型保存为 .bim，可以使用 "-B" 开关。

## 支持读取/编辑更多对象类型

Tabular Editor 目前仅允许最终用户读取和编辑 Tabular Object Model 中的一部分对象。理想情况下，应允许在 Tabular Editor 中访问模型树中的所有对象：关系、KPI、计算表格和角色都应可直接编辑。数据源、表、数据列和表分区都应可编辑，但会有一些限制（例如，我们不应期望 Tabular Editor 能够从任意数据源和查询中获取数据架构）。

**更新**：从 2.1 版本起，许多新的对象类型现在会直接显示在 Tree Explorer 中。通过右键菜单，你可以创建、复制和删除其中许多对象（角色、透视、翻译）。我们目前仍不支持创建或删除关系和数据源，但这一功能会在未来版本中加入。

**更新**：从 2.2 版本起，我们现在可以创建和删除关系。后续会支持更多对象类型。

**更新**：自 2.3 起，表、分区和数据列现已可编辑。现在，Visual Studio 只在创建空白模型本身时才需要——其他所有操作都可以在 Tabular Editor 中完成。

**更新**：之前那次更新是谎话！我忘了 KPI——不过从 2.4 版本起，它们现在也可以创建/编辑/删除了。

## 将 Model.bim 拆分为多个 json 文件

Model.bim 文件的布局和结构非常不利于源代码管理和版本控制。整个 Tabular Object Model 不仅被写进同一个文件，这个文件还在结构中到处包含“ModifiedTime”信息，导致源代码管理中的 DIFF 操作形同虚设。

为了让 Tabular 模型的发布管理流程更顺畅，如果 Tabular Editor 能将 Model.bim 文件以文件夹结构保存/加载，并为度量值、计算列等使用独立文件，会很有价值。应该提供命令行选项，用于将 Model.bim 文件导出为这种格式，或从这种格式导入回 Model.bim 文件；也应该可以直接从这种格式进行部署（在不需要 Model.bim 文件本身的情况下）。这些独立文件应包含与 Model.bim 文件相同的 JSON，但不包含“ModifiedTime”信息，以便能轻松用于版本控制系统，让多位开发人员可以同时协作开发同一个模型。

**更新**：[在 2.2 中可用](/Advanced-features#folder-serialization)。

**更新**：从 2.3 版本开始，已可通过选项将透视和翻译元数据存储为各个对象上的注释。这对于有多个开发人员参与的版本控制场景很有用，可以避免开发人员更改翻译、透视成员关系等内容时，导致某个单一文件频繁出现大量改动。

## Power BI 兼容性

目前已经可以将 Tabular Editor 连接到托管在 Power BI Desktop 中的模型。这种做法类似于[这里针对 Excel 和 SSMS 的说明](http://biinsight.com/connect-to-power-bi-desktop-model-from-excel-and-ssms/)。这样就可以将显示文件夹添加到 Power BI Desktop 模型中，并且即使保存并重新打开 .pbix 文件，它们仍会保留在 Power BI 中。不过，似乎存在一些兼容级别问题，在继续之前应该先弄清楚。

**更新**：从 2.1 版本起，Tabular Editor 现在会检测正在运行的 Power BI Desktop 实例以及 Visual Studio 集成 Workspace。你可以连接到这些实例，并像操作普通实例一样进行更改；不过，这种修改 Power BI 和集成 Workspace 模型的方法不受 Microsoft 支持。

## 导入/导出翻译

这是 SSDT 里的标准功能，在 Tabular Editor 里也会很有用。

**更新**：[2.2 中已支持导入/导出翻译](/Advanced-features#import-export-translations)。
