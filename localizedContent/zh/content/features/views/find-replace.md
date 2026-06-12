---
uid: find-replace
title: 查找/替换
author: Morten Lønskov
updated: 2023-03-22
applies_to:
  products:
    - product: Tabular Editor 2
      partial: true
      note: "其工作方式与本文所示不同"
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

<a name="find"></a>

# 查找

在 Tabular Editor 中，你可以使用高级“查找”功能，在打开的文档和数据集中查找特定表达式。 可以通过键盘快捷键 Ctrl+F 打开“查找”对话框。 可以通过键盘快捷键 Ctrl+F 打开“查找”对话框。

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/user-interface/find-dialog.png" alt="Find Dialog Box" style="width: 300px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 1：</strong>Tabular Editor 中的“查找”窗口。 Ctrl+F 可打开该对话框 </figcaption>
</figure>

要执行搜索，请先定义要查找的表达式，并使用“选项”来决定是否需要满足特定条件。 要执行搜索，请先定义要查找的表达式，并使用“选项”来决定是否需要满足特定条件。 例如，你可以选择查找表达式与匹配文本是否区分大小写，或使用正则表达式进行搜索。

## 查找范围

此外，你还可以在“查找范围”中指定要查看的位置，即 Tabular Editor 实例的不同区域，以限制或扩展搜索范围。 “查找范围”选项包括： “查找范围”选项包括：

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/user-interface/find-dialog-look-in.png" alt="Find and Replace Dialog Box" style="width: 200px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 2：</strong>Tabular Editor 中的“查找/替换”窗口。 Ctrl+F 可打开该对话框 </figcaption>
</figure>

- _选区_: 在当前打开文档的选定内容中搜索（无法搜索数据集）
- _当前文档_: 在你当前打开的整个文档中搜索（无法搜索数据集）
- _所有打开的文档_: 在所有打开的文档中搜索（无法搜索数据集）
- _整个模型_：在 TOM Explorer 中查找 Dataset 中的匹配项。
  - 可在 Dataset 的各个部分中搜索，例如名称、表达式、注释等。
  - 在此模式下，你还可以使用 Dynamic LINQ 进行搜索，例如查找所有 summarize 未设置为 none 的列。

> [!TIP]
> 你也可以直接使用 TOM Explorer 中的搜索框来搜索你的 Dataset，而不必使用“查找”对话框

<a name="replace"></a>

## 替换

“替换”对话框与“查找”类似：先搜索一个表达式，然后将其替换为另一个表达式。

“替换”对话框不要求在 _替换为_ 字段中填写任何内容，但如果留空，会将你搜索的表达式替换为空表达式。
“替换”对话框不要求在 _替换为_ 字段中填写任何内容，但如果留空，会将你搜索的表达式替换为空表达式。
你可以使用与“查找”对话框相同的选项来确定搜索条件，但 _查找范围_ 功能仅适用于文档；也就是说，你无法在 Dataset 对象中进行搜索和替换。

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/user-interface/find-dialog.png" alt="Replace Dialog Box" style="width: 300px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 3：</strong> Tabular Editor 中的“替换”窗口。 按 Ctrl+F 可打开该对话框 </figcaption>
 按 Ctrl+F 可打开该对话框 </figcaption>
</figure>

> [!TIP]
> 如果你想在 DAX 语句（表达式或脚本）中重命名变量，Ctrl+R 可对所选变量执行重构