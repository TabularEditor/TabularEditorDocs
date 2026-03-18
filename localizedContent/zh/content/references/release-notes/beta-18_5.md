# Tabular Editor 3 BETA-18.5

> [!IMPORTANT]
> 已有更新版本的 Tabular Editor 可用。 你可以在 [这里](https://docs.tabulareditor.com/references/release-notes) 找到最新版本。

- 下载 [Tabular Editor 3 BETA-18.5](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-18.5.x86.msi)
- 下载 [Tabular Editor 3 BETA-18.5（64 位）](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-18.5.x64.msi)
- [所有发行版](https://docs.tabulareditor.com/projects/te3/en/latest/downloads.html)

## BETA-18.5 中的新功能：

- “搜索”对话框（CTRL+F）现在支持搜索整个模型。 在下拉菜单中选择该选项后，会出现另一个下拉菜单，供你选择要搜索哪些对象属性。 同时还提供正则表达式、反斜杠表达式，以及[类似 Tabular Editor 2.x 的 Dynamic LINQ 搜索](https://docs.tabulareditor.com/Advanced-Filtering-of-the-Explorer-Tree.html)（也可以在“查找内容”字段中以 `:` 作为第一个字符来启用 Dynamic LINQ）。 搜索结果会显示在单独的窗口中；在搜索结果窗口中双击某个项，会直接跳转到该项，并在属性网格中高亮显示相关属性：

![image](https://user-images.githubusercontent.com/30911111/119983803-edd94f80-bfc0-11eb-91cb-aee084e0c83d.png)

- 新增对 DAX 日期字面量语法 `dt"2021-05-27"` 的支持
- 已将 TOM 更新至 19.21.0 版本

## BETA-18.5 中的错误修复和小幅更新：

- 为表的 SourceExpressions 添加了多行字符串编辑器
- 确保在剪切和粘贴时不会重新生成关系名称
- 为 FixExpressions 中的 `it` 关键字添加了 BPA 支持，参见 https://github.com/TabularEditor/TabularEditor/issues/846
- 改进了在不同文档和 UI 元素之间切换时“查找/替换”窗口的行为
- 修复了 NOT 关键字优先级顺序的问题，参见 https://github.com/TabularEditor/TabularEditor3/issues/5。
