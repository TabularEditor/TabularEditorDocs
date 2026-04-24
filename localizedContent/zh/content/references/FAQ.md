---
uid: faq
title: 常见问题
---

# 常见问题

## 什么是 Tabular Editor？

本质上，Tabular Editor 提供了一个 UI，用于编辑组成 Analysis Services 表格模型的元数据。 使用 Tabular Editor 编辑模型与使用 Visual Studio 的主要区别在于：Tabular Editor 不会加载任何 _数据_——只加载 _元数据_。 这意味着，当你创建和修改度量值、显示文件夹等内容时，不会执行任何验证或计算。 只有在用户选择将更改保存到数据库时，才会执行验证和计算。 这为中大型模型带来了更好的开发体验，因为这类模型在 Visual Studio 中往往操作起来较慢。

此外，Tabular Editor 还提供了大量[功能](../getting-started/boosting-productivity-te3.md)，通常可以提升你的效率，让某些任务更容易完成。

## 为什么我们还需要另一个用于 SSAS Tabular 的工具？

在使用 Analysis Services Tabular 时，你可能已经熟悉 SQL Server Data Tools（Visual Studio）、[DAX编辑器](https://www.sqlbi.com/tools/dax-editor/)、[DAX Studio](https://www.sqlbi.com/tools/dax-studio/)、[BISM Normalizer](http://bism-normalizer.com/) 以及 [BIDSHelper](https://bidshelper.codeplex.com/)。 这些都是非常优秀的工具，各自都有明确的用途。 Tabular Editor 并不是要取代这些工具，而是作为它们的补充来使用。 请参阅 [Why Tabular Editor](https://tabulareditor.com/why-tabular-editor) 一文，了解为什么使用 Tabular Editor 是有充分理由的。 这些都是非常优秀的工具，各自都有明确的用途。 Tabular Editor 并不是要取代这些工具，而是作为它们的补充来使用。 请参阅 [Why Tabular Editor](https://tabulareditor.com/why-tabular-editor) 一文，了解为什么使用 Tabular Editor 是有充分理由的。

## 为什么 Tabular Editor 不以 Visual Studio 插件的形式提供？

虽然大家当然会希望在 Visual Studio 里处理表格模型能有更好的体验，但独立工具相比插件仍然有一些优势：首先，**使用 Tabular Editor 不需要安装 Visual Studio/SSDT**。 Tabular Editor 只需要 AMO 库，与 Visual Studio 相比，安装体积小得多。 其次，TabularEditor.exe 可以通过命令行选项来执行部署、脚本等操作，而在 .vsix（插件）项目中无法实现这一点。 Tabular Editor 只需要 AMO 库，与 Visual Studio 相比，安装体积小得多。 其次，TabularEditor.exe 可以通过命令行选项来执行部署、脚本等操作，而在 .vsix（插件）项目中无法实现这一点。

另外也值得一提：Tabular Editor 可以以[独立 .zip 文件](https://github.com/TabularEditor/TabularEditor/releases/latest/download/TabularEditor.Portable.zip)下载，这意味着你无需安装任何东西。 换句话说，即使你在 Windows 机器上没有管理员权限，也可以运行 Tabular Editor。 只需下载 zip 文件，解压，然后运行 TabularEditor.exe。 换句话说，即使你在 Windows 机器上没有管理员权限，也可以运行 Tabular Editor。 只需下载 zip 文件，解压，然后运行 TabularEditor.exe。

## 接下来版本计划加入哪些功能？

你可以在[这里](roadmap.md)查看当前路线图。
