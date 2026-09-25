# 路线图

> [!IMPORTANT]
> abular Editor 2 is no longer under active development and will not receive any major feature additions or improvements from our side. We are, however, committed to keeping it up-to-date, ensuring support for new semantic modelling features as they are released from Microsoft, and also fixing any critical or blocking issues. As the project is open-source under MIT, anyone is welcome to submit pull requests, which will be reviewed and approved by our team. The following list should therefore be considered deprecated.

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

It should be possible, when selecting one or more objects in the explorer tree, to generate a script for these objects. In fact, this is already possible by dragging and dropping the objects into another text editor (or SSMS), but there should be a similar right-click option to more clearly communicate to end-users what's going on. 应支持生成 TMSL 脚本（用于 SSMS）以及可在 [DAX编辑器](https://github.com/DaxEditor/) 中使用的 DAX 风格代码。

Today, measures and calculated columns can be dragged between instances of Tabular Editor to copy them between models, but to better expose this functionality, there should be an UI option for importing a provided piece of TMSL, either from the clipboard or from a file. See [this issue](https://github.com/TabularEditor/TabularEditor/issues/69). Lastly, the standard copy-paste shortcuts should be enabled.

## 为 Visual Studio 创建插件，用于启动 Tabular Editor

为 Visual Studio 添加一个简单的上下文菜单扩展：确保 Model.bim 文件已关闭，然后启动 TabularEditor.exe 并加载该 Model.bim 文件。

## 为 DAX 表达式编辑器提供 IntelliSense

在表达式编辑器中编写 DAX 代码时，应弹出自动完成框，帮助补全表名、列名、度量值名称或函数（及其参数）。

也可以看看 [此问题](https://github.com/TabularEditor/TabularEditor/issues/64)。

## 面向开发者的 Tabular Editor 插件架构 / 公共 API

偏好使用 C# 以脚本方式编写表格模型的用户，现在就已经可以改用 TOMWrapper.dll，而无需直接使用 Analysis Services TOM API。 This provides some benefits, for example, the TOMWrapper namespace makes it easier to work with perspectives and translations, thanks to the convenient methods and properties available.

更进一步，如果能向开发者开放更多 Tabular Editor 功能，会很有意思：

- 解析 DAX 对象
- 查看 Best Practice Analyzer 的分析结果
- Tabular Editor UI（支持为 Tabular Editor 创建“插件”，可带/不带自定义 UI）

## 使用 VSTS 进行自动化构建、测试、发布和生成文档

使用 VSTS 进行 DevOps，并对 Tabular Editor 源代码进行整体清理。

## Formula fix-up

当任何模型对象被重命名时，应更新所有引用该对象的 DAX 表达式，以反映名称变更。

**更新**：从 2.2 起，可在“文件”>“偏好”中切换启用此功能。

## 用于显示对象依赖关系的 UI

右键单击度量值或计算列，就会在弹出对话框中显示依赖关系树。 It should be possible to show either objects that depend on the chosen object, or objects on which the chosen object depend.

**Update**: As of 2.2, this feature is available. Simply right-click an object and choose "Show dependencies...".

## 通过命令行以脚本方式应用更改

Today, it is possible to deploy a model directly from the command-line. 同样，你也应该能够通过管道传入一个包含要在模型上执行的 C# Script 的 .cs 文件。 After script execution, it should be possible to save or deploy the updated model. This requires a few changes to the current command-line options.

**Update**: As of 2.3, scripts can be executed from the command-line, by using the "-S" switch. Deployment works as usual, but if you want to save the modified model as a .bim, you can use the "-B" switch.

## 支持读取/编辑更多对象类型

Tabular Editor currently only lets end-users read and edit a subset of the objects in the Tabular Object Model. 理想情况下，应允许在 Tabular Editor 中访问模型树中的所有对象：关系、KPI、计算表格和角色都应可直接编辑。 Data Sources, tables, data columns and table partitions should be editable with some constraints (for example, we should not expect Tabular Editor to be able to fetch data schemas from arbitrary data sources and queries).

**更新**：从 2.1 版本起，许多新的对象类型现在会直接显示在 Tree Explorer 中。 Using the right-click menu, you can create, duplicate and delete many of these objects (roles, perspectives, translations). We're still lacking support for creating/deleting relationships and data sources, but this will come in a future release.

**更新**：从 2.2 版本起，我们现在可以创建和删除关系。 More object types coming later.

**Update**: As of 2.3, tables, partitions and data columns can now be edited. 现在，Visual Studio 只在创建空白模型本身时才需要——其他所有操作都可以在 Tabular Editor 中完成。

**Update**: Previous update was a lie! 我忘了 KPI——不过从 2.4 版本起，它们现在也可以创建/编辑/删除了。

## 将 Model.bim 拆分为多个 json 文件

Model.bim 文件的布局和结构非常不利于源代码管理和版本控制。 Not only is the entire Tabular Object Model written into just one file, the file also contains "ModifiedTime" information everywhere in the structure, making source control DIFF operations useless.

为了让 Tabular 模型的发布管理流程更顺畅，如果 Tabular Editor 能将 Model.bim 文件以文件夹结构保存/加载，并为度量值、计算列等使用独立文件，会很有价值。 There should be command-line options available for exporting/importing Model.bim files from/to this format, and it should be possible to deploy directly from this format (in cases where you don't need the Model.bim file itself). These individual files should contain the same JSON as the Model.bim file, but without the "ModifiedTime" information, so that they can easily be used in a version control system, allowing multiple developers to work on the same model at once.

**更新**：[在 2.2 中可用](/Advanced-features#folder-serialization)。

**Update**: As of 2.3, options exist to store Perspective and Translation metadata as annotations on the individual objects. This is useful for source control scenarios with multiple developers, to avoid having single files that gets lots of edits when developers change translations, perspective memberships, etc.

## Power BI 兼容性

目前已经可以将 Tabular Editor 连接到托管在 Power BI Desktop 中的模型。 The approach is similar to what is [described here for Excel and SSMS](http://biinsight.com/connect-to-power-bi-desktop-model-from-excel-and-ssms/). Doing this, it is actually possible to add Display Folders to the Power BI Desktop model, and they actually stay in Power BI, even after saving and reopening the .pbix file. However, it seems that there are some compatibility level issues, which should be looked into before proceeding.

**更新**：从 2.1 版本起，Tabular Editor 现在会检测正在运行的 Power BI Desktop 实例以及 Visual Studio 集成 Workspace。 You can connect to these instances and make changes as you would normal instances, although this approach of changing Power BI and Integrated Workspace models is not supported by Microsoft.

## 导入/导出翻译

这是 SSDT 里的标准功能，在 Tabular Editor 里也会很有用。

**更新**：[2.2 中已支持导入/导出翻译](/Advanced-features#import-export-translations)。
