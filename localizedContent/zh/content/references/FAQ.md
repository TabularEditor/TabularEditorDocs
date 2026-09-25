---
uid: faq
title: 常见问题
---

# 常见问题

## 什么是 Tabular Editor？

Essentially, Tabular Editor provides a UI for editing the metadata making up an Analysis Services Tabular Model. The main difference between using Tabular Editor for editing a model versus using Visual Studio, is that Tabular Editor does not load any _data_ - only _metadata_. This means that no validations or calculations are performed when you create and modify measures, display folders, etc. Validations and calculations are performed only when the user chooses to persist the changes to the database. This provides a better developer experience for medium to large sized models, which tend to be slow to work with in Visual Studio.

此外，Tabular Editor 还提供了大量[功能](../getting-started/boosting-productivity-te3.md)，通常可以提升你的效率，让某些任务更容易完成。

## 为什么我们还需要另一个用于 SSAS Tabular 的工具？

在使用 Analysis Services Tabular 时，你可能已经熟悉 SQL Server Data Tools（Visual Studio）、[DAX编辑器](https://www.sqlbi.com/tools/dax-editor/)、[DAX Studio](https://www.sqlbi.com/tools/dax-studio/)、[BISM Normalizer](http://bism-normalizer.com/) 以及 [BIDSHelper](https://bidshelper.codeplex.com/)。 These are all excellent tools, each with their own purposes. Tabular Editor is not intended to replace any of these tools, but should rather be seen as a supplement to them. Please view the [Why Tabular Editor](https://tabulareditor.com/why-tabular-editor) article, to see why Tabular Editor is justified.

## 为什么 Tabular Editor 不以 Visual Studio 插件的形式提供？

虽然大家当然会希望在 Visual Studio 里处理表格模型能有更好的体验，但独立工具相比插件仍然有一些优势：首先，**使用 Tabular Editor 不需要安装 Visual Studio/SSDT**。 Tabular Editor only requires the AMO libraries, which is quite a small installation compared to VS. Secondly, TabularEditor.exe can be executed with command-line options for deployment, scripting, etc., which would not be possible in a .vsix (plug-in) project.

另外也值得一提：Tabular Editor 可以以[独立 .zip 文件](https://github.com/TabularEditor/TabularEditor/releases/latest/download/TabularEditor.Portable.zip)下载，这意味着你无需安装任何东西。 In other words, you can run Tabular Editor without having admin rights on your Windows machine. Simply download the zip file, extract it, and run TabularEditor.exe.

## 接下来版本计划加入哪些功能？

你可以在[这里](roadmap.md)查看当前路线图。
