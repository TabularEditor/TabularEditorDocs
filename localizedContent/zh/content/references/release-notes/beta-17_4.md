# Tabular Editor 3 BETA-17.4

> [!IMPORTANT]
> Tabular Editor 已有更新版本。 你可以在[这里](https://docs.tabulareditor.com/references/release-notes)找到最新版本。

- 下载 [Tabular Editor 3 BETA-17.4](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-17.4.x86.msi)
- 下载 [Tabular Editor 3 BETA-17.4（64 位）](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-17.4.x64.msi)

## BETA-17.4 更新内容：

- 修复在某些情况下 DAX 语义分析器错误 Report 出循环依赖的问题。
- DAX 编辑器现在会在右键菜单中显示键盘快捷键
- 当光标位于“窥视定义”编辑器内时，现在可按 ESC 关闭该编辑器。 此外，由于该编辑器按设计为只读，AutoComplete/Calltips 将不再在其中弹出。
- 在使用“Count”汇总时，可指定 AlternateOf BaseColumn 属性。
- 改进了对指向 Power BI 服务中 Dataset 的连接字符串的支持。

## BETA-17.3 更新：

- 现在可以将表拖到图表视图中（参见 #15）
- 在 DAX 脚本模式下，Inline/Define 度量值现在按预期工作（参见 #91）
- VertiPaq分析器在收集统计信息时，现在应能正确识别在 Tabular Editor 外部对 Data model 所做的更改
- VertiPaq分析器的数据现在可通过脚本访问（参见 #90）：新增一个全局脚本方法 `CollectVertiPaqAnalyzerStats();`，以及针对 Tables 和 Columns 的两个新扩展方法：`.GetCardinality()` 和 `.GetTotalSize()`。
- 对 AutoComplete 功能进行了多项改进。 例如，在方括号之间输入代码时（参见 #92）
- DAX 查询中的查询作用域对象，或 DAX 脚本中的脚本化对象之间的循环依赖，不再导致崩溃
- 新增一个 DAX 自动格式设置选项，用于控制扩展列是否始终带限定符——即使表名为空，例如 `''[MyExtColumn]`。
- 修复在信息视图中双击某个项目时有时会发生的崩溃
- 修复在计算项或度量值表达式之外使用 ISSELECTEDMEASURE、SELECTEDMEASURE、SELECTEDMEASURENAME 和 SELECTEDMEASUREFORMATSTRING 函数时的错误信息。

## BETA-17.2 更新：

- 修复 VertiPaq分析器程序集版本相关的问题。
- 在 VertiPaq 分析器中新增“分区”窗格。
- 安装程序将不再删除 `%LocalAppData%\TabularEditor3` 文件夹中的内容，从而使用户在升级或卸载后仍能保留设置。
- 支持将对象拖放到 DAX 和 C# 编辑器中（#15）。
- 支持在所有代码编辑器中拖放所选文本。 拖动时按住 CTRL 键可复制所选内容。
- 支持 DAX 的 CROSSFILTER 函数中新增的 OneWay_LeftFiltersRight 和 OneWay_RightFiltersLeft 参数。
- 已将 TOM 升级到 19.20.1。
- 多项稳定性改进。

## BETA-17.1 中的更新：

![image](https://user-images.githubusercontent.com/8976200/112887423-762b9900-90d3-11eb-8248-d9da55fe8fe3.png)

- 新增 [VertiPaq分析器](https://www.sqlbi.com/tools/vertipaq-analyzer/)（如果新视图未在界面中显示，你可能需要删除 %LocalAppData%\TabularEditor3 下的 Layout.gz 文件，并/或将窗口 Workspace 重置为默认窗口 Workspace）
  - 收集统计信息（列和表的基数与大小），这些信息会显示在 TOM Explorer 的工具提示中；在任意 DAX 编辑器中将鼠标悬停在列或表引用上时也会显示。
  - 从 VPAX 文件导入统计信息或导出到 VPAX 文件
  - 从 VPAX 文件加载模型
- 允许编辑同义词
- 在依赖关系视图中显示 SortByColumn

## BETA-17.1 中的错误修复：

- 修复复制/粘贴区域设置时会覆盖现有区域设置的问题

## BETA-17.0 中的更新：

- Tabular Editor 3 现在支持在主表达式编辑器中编辑 M 表达式和分区查询（见 #2）
- 全部 4 种代码编辑器（DAX、C#、SQL、M）现在都可以在“工具 > 偏好 > 文本编辑器”下分别独立配置（例如行号、缩进引导线、空白字符等）
- 代码编辑器现在支持多项粘贴（#87）。 你可以在“工具 > 偏好 > 文本编辑器 > 常规”中关闭此功能。

## BETA-17.0 中的错误修复：

- 当对象名称被更改时，宏记录器现在会生成可正确引用原始对象的代码。
- ALT 键将不再把焦点切到菜单栏（此前这会干扰文本编辑器中的区块选择）。 你可以改用 F10 来切换焦点。 ALT+字母键组合仍可用于浏览菜单。
- Tabular Editor 3 现在可以正确处理 LineageTag 属性，例如在 Power BI Desktop 模型中复制度量值时
- 宏现在可以使用 FormatDax 方法。
- 从 Tabular Editor 2 移植了多项 TOMWrapper 错误修复。
- 修复了属性网格中只读项的显示行为（现在会灰显）。
- 在属性网格中为部分属性新增了右键菜单选项（例如用于添加/移除 AlternateOf 对象、KPI 等）。
