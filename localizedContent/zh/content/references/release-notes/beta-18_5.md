# Tabular Editor 3 BETA-18.5

> [!IMPORTANT]
> Tabular Editor 已推出新版本。 You can find the latest version [here](https://docs.tabulareditor.com/references/release-notes).

- 下载 [Tabular Editor 3 BETA-18.5](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-18.5.x86.msi)
- 下载 [Tabular Editor 3 BETA-18.5（64 位）](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-18.5.x64.msi)
- [所有发行版](https://docs.tabulareditor.com/projects/te3/en/latest/downloads.html)

## BETA-18.5 中的新功能：

- The Search dialog (CTRL+F) now supports searching the entire model. When this option is selected in the dropdown, another dropdown appears that lets you choose which object properties to search. 同时还提供正则表达式、反斜杠表达式，以及[类似 Tabular Editor 2.x 的 Dynamic LINQ 搜索](https://docs.tabulareditor.com/Advanced-Filtering-of-the-Explorer-Tree.html)（也可以在“查找内容”字段中以 `:` 作为第一个字符来启用 Dynamic LINQ）。 Search results are displayed in a separate window, and double-clicking on an item in the search results window will take you directly to that item, highlighting the relevant property in the property grid:

![image](~/content/assets/images/beta-18-5-01.png)

- 新增对 DAX 日期字面量语法 `dt"2021-05-27"` 的支持
- 已将 TOM 更新至 19.21.0 版本

## BETA-18.5 中的错误修复和小幅更新：

- 为表的 SourceExpressions 添加了多行字符串编辑器
- 确保在剪切和粘贴时不会重新生成关系名称
- 为 FixExpressions 中的 `it` 关键字添加了 BPA 支持，参见 https://github.com/TabularEditor/TabularEditor/issues/846
- 改进了在不同文档和 UI 元素之间切换时“查找/替换”窗口的行为
- 修复了 NOT 关键字优先级顺序的问题，参见 https://github.com/TabularEditor/TabularEditor3/issues/5。
