# 路线图

> [!IMPORTANT]
> Tabular Editor 2 已不再处于积极开发状态，我们也不会再为其添加或改进任何重大功能。 不过，我们还是会持续维护它，确保支持 Microsoft 发布的最新语义模型建模功能，并修复任何关键或阻塞性问题。 由于该项目在 MIT 许可下开源，欢迎任何人提交拉取请求，我们的团队将进行审核并批准。 因此，下列列表应视为已弃用。

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

在资源管理器树中选中一个或多个对象时，应能为这些对象生成脚本。 其实，现在把对象拖放到另一个文本编辑器（或 SSMS）里就能做到，但还是需要提供类似的右键选项，让最终用户更清楚这个功能在做什么。 应支持生成 TMSL 脚本（用于 SSMS）以及可在 [DAX编辑器](https://github.com/DaxEditor/) 中使用的 DAX 风格代码。

目前，可以在 Tabular Editor 的不同实例之间拖放度量值和计算列，从而在模型之间复制它们。但为了更好地呈现这一功能，应提供一个 UI 选项，用于导入一段指定的 TMSL，可从剪贴板或文件导入。 参见 [此问题](https://github.com/TabularEditor/TabularEditor/issues/69)。 最后，应启用标准的复制/粘贴快捷键。

## 为 Visual Studio 创建插件，用于启动 Tabular Editor

为 Visual Studio 添加一个简单的上下文菜单扩展：确保 Model.bim 文件已关闭，然后启动 TabularEditor.exe 并加载该 Model.bim 文件。

## 为 DAX 表达式编辑器提供 IntelliSense

在表达式编辑器中编写 DAX 代码时，应弹出自动完成框，帮助补全表名、列名、度量值名称或函数（及其参数）。

也可以看看 [此问题](https://github.com/TabularEditor/TabularEditor/issues/64)。

## 面向开发者的 Tabular Editor 插件架构 / 公共 API

偏好使用 C# 以脚本方式编写表格模型的用户，现在就已经可以改用 TOMWrapper.dll，而无需直接使用 Analysis Services TOM API。 这带来一些好处。例如，借助 TOMWrapper 命名空间提供的便捷方法和属性，可以更轻松地处理透视和翻译。

更进一步，如果能向开发者开放更多 Tabular Editor 功能，会很有意思：

- 解析 DAX 对象
- 查看 Best Practice Analyzer 的分析结果
- Tabular Editor UI（支持为 Tabular Editor 创建“插件”，可带/不带自定义 UI）

## 使用 VSTS 进行自动化构建、测试、发布和生成文档

使用 VSTS 进行 DevOps，并对 Tabular Editor 源代码进行整体清理。

## 公式自动修正

当任何模型对象被重命名时，应更新所有引用该对象的 DAX 表达式，以反映名称变更。

**更新**：从 2.2 起，可在“文件”>“偏好”中切换启用此功能。

## 用于显示对象依赖关系的 UI

右键单击度量值或计算列，就会在弹出对话框中显示依赖关系树。 可以支持显示两种视图：依赖于所选对象的对象，或所选对象所依赖的对象。

**更新**：从 2.2 起，此功能已可用。 只需右键单击某个对象，然后选择“显示依赖关系...”。

## 通过命令行以脚本方式应用更改

目前，可以直接通过命令行部署模型。 同样，你也应该能够通过管道传入一个包含要在模型上执行的 C# Script 的 .cs 文件。 脚本执行后，你可以保存或部署更新后的模型。 这需要对当前命令行选项做些调整。

**更新**：从 2.3 起，可通过命令行使用“-S”开关执行脚本。 部署方式与平时一致；但如果你想将修改后的模型保存为 .bim，可以使用“-B”开关。

## 支持读取/编辑更多对象类型

目前，Tabular Editor 只允许最终用户读取和编辑 Tabular Object Model 中的一部分对象。 理想情况下，应允许在 Tabular Editor 中访问模型树中的所有对象：关系、KPI、计算表格和角色都应可直接编辑。 数据源、表、数据列和表分区应在一定限制下可编辑（例如，不应期望 Tabular Editor 能从任意数据源和查询中获取数据架构）。

**更新**：从 2.1 版本起，许多新的对象类型现在会直接显示在 Tree Explorer 中。 通过右键菜单，你可以创建、复制和删除其中的许多对象（角色、透视、翻译）。 目前仍缺少创建/删除关系和数据源的支持，但会在未来版本中提供。

**更新**：从 2.2 版本起，我们现在可以创建和删除关系。 后续会支持更多对象类型。

**更新**：从 2.3 版本起，现在可以编辑表、分区和数据列。 现在，Visual Studio 只在创建空白模型本身时才需要——其他所有操作都可以在 Tabular Editor 中完成。

**更新**：上一条更新是胡说的！ 我忘了 KPI——不过从 2.4 版本起，它们现在也可以创建/编辑/删除了。

## 将 Model.bim 拆分为多个 json 文件

Model.bim 文件的布局和结构非常不利于源代码管理和版本控制。 不仅整个 Tabular Object Model 都写在一个文件中，而且该文件在结构中到处都包含 "ModifiedTime" 信息，使版本控制的 DIFF 操作毫无用处。

为了让 Tabular 模型的发布管理流程更顺畅，如果 Tabular Editor 能将 Model.bim 文件以文件夹结构保存/加载，并为度量值、计算列等使用独立文件，会很有价值。 应提供命令行选项，用于将 Model.bim 文件导出/导入到这种格式；并且应能直接基于这种格式进行部署（在不需要 Model.bim 文件本身的情况下）。 这些独立文件应该包含与 Model.bim 文件相同的 JSON，但不包含“ModifiedTime”信息，这样更适合放进版本控制系统，也能让多个开发者同时改同一个模型。

**更新**：[在 2.2 中可用](/Advanced-features#folder-serialization)。

**更新**：从 2.3 版本起，已提供选项，可将透视和翻译元数据作为注释存储在各个对象上。 这在多开发者的版本控制场景中很有用，可避免开发者更改翻译、透视成员关系等时，导致某个单一文件产生大量改动。

## Power BI 兼容性

目前已经可以将 Tabular Editor 连接到托管在 Power BI Desktop 中的模型。 其方法与[这里针对 Excel 和 SSMS 的说明](http://biinsight.com/connect-to-power-bi-desktop-model-from-excel-and-ssms/)类似。 这样做之后，确实可以为 Power BI Desktop 模型添加显示文件夹，并且即使保存并重新打开 .pbix 文件，它们也会保留在 Power BI 中。 不过，似乎存在一些兼容级别方面的问题，继续之前最好先确认一下。

**更新**：从 2.1 版本起，Tabular Editor 现在会检测正在运行的 Power BI Desktop 实例以及 Visual Studio 集成 Workspace。 你可以连接到这些实例，并像对普通实例那样进行更改；不过，Microsoft 不支持以这种方式更改 Power BI 和集成 Workspace 模式模型。

## 导入/导出翻译

这是 SSDT 里的标准功能，在 Tabular Editor 里也会很有用。

**更新**：[2.2 中已支持导入/导出翻译](/Advanced-features#import-export-translations)。
