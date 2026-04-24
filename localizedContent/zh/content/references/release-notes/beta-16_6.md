# Tabular Editor 3 BETA-16.6

> [!IMPORTANT]
> Tabular Editor 有更新版本可用。 你可以在[这里](https://docs.tabulareditor.com/references/release-notes)找到最新版本。

- 下载 [Tabular Editor 3 BETA-16.6](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-16.6.x86.msi)
- 下载 [Tabular Editor 3 BETA-16.6（64 位）](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-16.6.x64.msi)

## BETA-16.6 更新内容：

- 修复了“Group By Columns”集合编辑器的“添加”按钮问题。
- 将新建 Power BI 数据集的默认兼容级别更改为 1560。
- 当当前所选对象本身就是表级对象时，允许创建新的表级对象（度量值、列、层级结构）。

## BETA-16.5 更新内容：

- 安装程序现在应能正确将 Tabular Editor 3 注册为 Power BI Desktop 的外部工具
- 新增命令行选项“-nosplash”。Power BI Desktop 启动 Tabular Editor 3 时会使用该选项，因为启动画面有时会导致 Tabular Editor 3 被 Power BI Desktop 遮挡在后方。 升级 Tabular Editor 3 后，记得重启 Power BI Desktop。
- 下载链接现已改用我们的 Azure CDN，今后 Tabular Editor 3 的二进制文件将托管于此。 以下 URL 始终指向 Tabular Editor 3 的最新版本：
  - https://cdn.tabulareditor.com/files/latest/TabularEditor.3.x86.msi
  - https://cdn.tabulareditor.com/files/latest/TabularEditor.3.x64.msi

## BETA-16.4 更新内容：

大量 Bug 修复和小幅改进即将到来：

### 常规改进：

- 在将 .pbix 模型保存为 .bim/文件夹结构时，现在会使用 .pbix 文件名作为数据库名称。
- 新增 x64 支持（x64 和 x86 构建均以“Any CPU”为目标，但后者设置了“Prefer32Bits”标志）
- 安装程序已更新。 现在改用 WiX，这可确保卸载产品时能干净地清理注册表和本地应用数据文件夹。 此外，它看起来也更美观了 :-)
- 宏录制器现已支持录制大多数（甚至全部？） 可通过 UI 进行的模型更改
- 新增对多列标量谓词的支持。这是一种最近新增的 DAX 语法。 Tabular Editor 会根据模型元数据推断所使用的 Analysis Services 版本，但这并不总是可行（例如离线工作时）。因此，你可以在“工具 > 偏好 > DAX编辑器 > 常规 > 语义引擎功能”中，指定 Tabular Editor 如何处理多列标量谓词表筛选表达式）。
- 将 TOM 更新到 19.18.0 版。

### 易用性改进：

- 增大了 TOM Explorer 中展开/折叠箭头的可点击区域（见[此评论](https://github.com/TabularEditor3/PublicPreview/issues/81#issuecomment-789637586)）
- 在 TOM Explorer 中双击对象旁的图标，即可打开 DAX 表达式编辑器。

### Bug 修复：

- 修复了 DAX 语义分析器的问题，该问题会在某些表达式中产生“幽灵”错误信息
- 修复了问题 #75
- 修复了问题 #77
- 修复了问题 #84
- 根据遥测数据修复了多处崩溃问题。 @**Everyone**：发生异常时请继续发送这些错误报告，并尽量附上描述——这在我们排查问题、弄清楚哪里出错时非常宝贵！ 谢谢！

## BETA-16.3 更新：

- “Custom Actions” 已重命名为“宏”。
  - 新增一个窗口，可让你管理当前定义的所有宏。 双击列表项即可编辑现有宏。
  - 当将 C# Script 保存为宏后，之后每次保存（Ctrl+S）时，文档都会更新该宏。 使用“文件 > 另存为……” 即可将脚本保存为文件。
  - 宏名称可以相同。 在内部会通过自动分配的 ID 来区分它们。
  - 修复了导致无法保存宏的问题
- “窗口”菜单现在也包含一个“新建”子菜单，其中包含与“文件 > 新建”相同的菜单项
- 默认隐藏未启用的工具栏和菜单，以减少 UI 杂乱（可在“工具 > 偏好 > 用户界面”中更改）。
- 修复了 DAX 解析器的一个 bug：该问题会导致 `GENERATESERIES` 返回的表中有一列列名错误，可能与 #61 有关
- 修复问题 #74（在调用 BeginBatch() 之前调用 EndBatch() 会导致崩溃）
- 新增：保存到数据库时，若在 Tabular Editor 之外更改了已部署模型的元数据，将发出警告并刷新本地 TOM 树

## BETA-16.2 更新：

- 表格预览现在可以像 DAX 查询和 Pivot Grid 一样自动刷新（见问题 #73）
- 修复了一个 bug：表格预览无法显示尚未刷新的计算表格
- 新增：支持使用 DAX脚本创建计算列和计算表格
- DAX脚本现在支持部分执行（见问题 #69）。 编辑 DAX脚本时，“DAX脚本”工具栏上的 4 个按钮应该会亮起。 这些按钮对应的快捷键如下：
  - `F5` 将应用完整脚本。
  - `Shift+F5` 将应用完整脚本，并同步已连接的数据库。
  - `F8` 将仅应用当前所选内容。
  - `Shift+F8` 将应用当前所选内容，并同步已连接的数据库。
- 在图表视图中添加了水印，用于引导用户将表添加到图表中（见问题 #76）
- 后台运行的 Best Practice Analysis 不应再导致 UI 卡死（见问题 #79）
- Best Practice Analyzer 视图中用于忽略规则/对象的工具栏按钮和右键菜单选项，现在应能正常工作
- “请稍候”窗口不应再与由 C# Script 弹出的任何对话框重叠
- 修复了多项 bug（可能与问题 #74 有关）

## BETA-16.1 更新：

- 度量值现在使用“计算器”图标，以便更好地与 Power BI Desktop 的体验保持一致。 计算项图标也做了轻微调整，以便与度量值区分开来。
- 关键列现在以 **粗体** 显示
- 新增“Define Measure”和“Inline Measure”重构选项
- 改进了 DAX 查询中 DEFINE / EVALUATE 语句相关的自动补全行为。 例如，自动补全现在也会提示在查询内部定义的度量值、列和表。
- 自动补全现在也会针对 SUMMARIZECOLUMNS、ADDCOLUMNS 等函数的 Name 参数提示度量值，并可一次性补全 Name 和 Expression 参数：
  ![autocomplete names](https://user-images.githubusercontent.com/8976200/107629428-66aada80-6c62-11eb-91e4-d5528947840a.gif)
- 重新审阅了 #42。
- Deployment Wizard 现在会将部署偏好（目标 + 选项）保存到磁盘上与 Model.bim 或 Database.json 同目录的 .tmuo 文件中。 如果每个模型始终部署到同一目标，那么在不同模型之间切换时执行部署会更轻松。
- 已将 TOM 更新到 19.16.3。 应可修复问题 #63。
- 已修复问题 #64。
- 修复了模型文件出现在“最近使用的文件”菜单中的一个错误。

## BETA-16.0 更新：

- Deployment Wizard 已更新。 同时修复了问题 #42 和 #43。
- 在 DAX 查询中支持 DEFINE COLUMN 和 TABLE 语法
- “文件”菜单现在包含“最近使用的文件”和“最近使用的表格模型”子菜单。 前者会列出最近保存或打开的 10 个 DAX脚本、模型关系图、DAX 查询和 C# Script。 后者保存对最近 10 个模型文件（bim / pbit / 文件夹）的引用。
- 已修复 #67
- 已修复 #66
