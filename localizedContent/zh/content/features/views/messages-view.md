---
uid: messages-view
title: 信息视图
author: Daniel Otykier
updated: 2026-10-11
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

Tabular Editor 3 中的“消息”视图是一个工具窗口，用于显示与当前数据集相关的各种类型消息。 

> [!TIP]
> 您可以双击一条信息，跳转到模型树或脚本编辑器中的错误源。

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/user-interface/messages-view.png" alt="消息视图" style="width: 500px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 1：</strong> Tabular Editor 中的“信息”窗口。提供数据集中的所有警告和错误的概览 </figcaption>
</figure>


消息按**来源**分组，例如语义分析器、表达式编辑器或 Analysis Services。每行都包含以下列：

| 列 | 显示 |
| -- | -- |
| **对象** | 消息所属的对象或文档。|
| **类型** | 信息的严重程度：错误、警告或信息。|
| **消息** | 消息文本。|
| **原因** | 对于级联错误，是导致该错误的对象的错误。对于根错误，其导致的从属错误数。|
| **行**和**列** | 消息在表达式或文档中的位置。|

错误是 Analysis Services 拒绝的表达式或结构，例如计算项中的无效表达式或循环依赖关系。警告会标记出能够正常工作但未遵循推荐做法的表达式，例如完全限定的度量值引用。

## 级联错误和根本原因

当一个表达式存在错误时，每个引用该表达式的表达式也会出现错误，例如，一个度量值仅因其引用的度量值出错而导致自身出错。这些是*级联错误*，它们追溯到的错误是*根错误*。

**“原因”**列为每种类型的错误显示不同的值：

- 对于级联错误，它会命名具有根错误的对象，当错误追溯到多个根错误时，则在其后加上 **+N**
- 对于根错误，它显示 **+N 个依赖错误**，统计其直接和间接导致的错误

要处理级联错误，请在“信息”视图中右键单击一行：

- **转到根本原因**会在表达式编辑器中打开根本错误，并突出显示该错误。该命令仅在级联错误中显示。
- **显示级联错误**显示或隐藏级联错误。取消选中此项，仅列出您需要修复的根源错误。此设置默认为启用状态，并在会话之间保存。

具有自身错误的对象和对损坏对象的引用将显示两行：根错误和级联错误。Analysis Services 错误以及 DAX 查询、DAX 脚本和 Pivot Grid 中的错误绝不会级联。

## 复制信息
信息视图允许使用 Ctrl+C 复制错误信息。
 
从 Tabular Editor 3.23.0 开始，Ctrl+C 默认复制所选单元格。使用 Ctrl+Shift+C（或右键单击菜单中的“复制行”）进行行级复制。

> [!TIP]
> 右键单击单元格，选择**复制单元格**或**复制行**。同一菜单中还有**转到根本原因**和**显示级联错误**。


![消息视图复制](~/content/assets/images/messages-view-copy.png)

