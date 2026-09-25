---
uid: messages-view
title: 信息视图
author: Daniel Otykier
updated: 2021-09-08
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 信息视图

Tabular Editor 3 的信息视图是一个工具窗口，用于显示与当前数据集相关的各类信息。

> [!TIP]
> 你可以双击一条信息，直接跳转到模型树或脚本编辑器中对应的错误源。

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/user-interface/messages-view.png" alt="Message View" style="width: 500px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 1：</strong> Tabular Editor 中的信息窗口。 Provides an overview of all warnings and errors in your dataset </figcaption>
</figure>

信息视图会告诉你消息的来源以及生成该消息的对象。

显示的信息分为两类：“错误”和“警告”

- 错误：这个选项卡会显示任何会导致你的模型无法部署或保存的错误。 For example, if you have an invalid expression in a calculation item or a circular dependency in a relationship.
- 警告：此选项卡显示不符合规范、但不会影响模型正常使用的警告。 This is for example having fully qualified measure references.
-

## 复制信息

The message view allows for copying out the error message using Ctrl+C.

从 Tabular Editor 3.23.0 起，Ctrl+C 默认复制所选单元格。 Use Ctrl+Shift+C (or Copy Row in right-click menu) for row-level copy.

> [!TIP]
> 右键点击单元格以选择“复制单元格”/“复制行”。

![信息视图副本](~/content/assets/images/messages-view-copy.png)

