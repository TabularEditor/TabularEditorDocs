---
uid: faq
title: 常见问题
---

# 常见问题

## 什么是 Tabular Editor？

从本质上讲，Tabular Editor 提供了一个用于编辑构成 Analysis Services 表格模型之元数据的 UI。与在 Visual Studio 中编辑模型相比，使用 Tabular Editor 的主要区别在于：Tabular Editor 不会加载任何 _数据_，只会加载 _元数据_。这意味着，当你创建和修改度量值、显示文件夹等时，不会执行任何验证或计算。只有当用户选择将更改持久化保存到数据库时，才会执行验证和计算。对于中大型模型，这能带来更好的开发体验，因为这类模型在 Visual Studio 中操作往往较慢。

此外，Tabular Editor 还提供了大量[功能](../getting-started/boosting-productivity-te3.md)，通常可以提升你的效率，让某些任务更容易完成。

## 为什么我们还需要另一个用于 SSAS Tabular 的工具？

在使用 Analysis Services Tabular 时，你可能已经熟悉 SQL Server Data Tools（Visual Studio）、[DAX编辑器](https://www.sqlbi.com/tools/dax-editor/)、[DAX Studio](https://www.sqlbi.com/tools/dax-studio/)、[BISM Normalizer](http://bism-normalizer.com/) 以及 [BIDSHelper](https://bidshelper.codeplex.com/)。这些都是优秀的工具，各自都有自己的用途。 Tabular Editor 并不是为了取代这些工具，而更应被视为对它们的补充。你可以查看 [为什么选择 Tabular Editor](https://tabulareditor.com/why-tabular-editor) 一文，了解为什么 Tabular Editor 值得使用。

## 为什么 Tabular Editor 不以 Visual Studio 插件的形式提供？

虽然大家当然会希望在 Visual Studio 里处理表格模型能有更好的体验，但独立工具相比插件仍然有一些优势：首先，**使用 Tabular Editor 不需要安装 Visual Studio/SSDT**。 Tabular Editor 只需要 AMO 库；与 VS 相比，安装体积要小得多。其次，TabularEditor.exe 可以通过命令行选项执行部署、脚本编写等操作，而这在 .vsix（插件）项目中是无法实现的。

另外也值得一提：Tabular Editor 可以以[独立 .zip 文件](https://github.com/TabularEditor/TabularEditor/releases/latest/download/TabularEditor.Portable.zip)下载，这意味着你无需安装任何东西。换句话说，即使你在 Windows 计算机上没有管理员权限，也可以运行 Tabular Editor。只需下载 zip 文件，解压后运行 TabularEditor.exe 即可。

## 接下来版本计划加入哪些功能？

你可以在[这里](roadmap.md)查看当前路线图。
