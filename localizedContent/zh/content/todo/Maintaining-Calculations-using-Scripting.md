本文演示如何在 Tabular Editor 中使用“高级脚本”功能，以一致的方式在多个对象之间维护 DAX 逻辑。 In the [Useful Script Snippets article](/Useful-script-snippets), we already saw [how we can use Custom Actions to quickly generate many measures](/Useful-script-snippets#generate-time-intelligence-measures) with similar logic, which can be useful when creating Time Intelligence calculations, for example.

在本文中，我们将在这个思路上更进一步，创建一个脚本“框架”，使我们能够在一个 TSV 文件（Tab Separated Values，制表符分隔值）中集中定义所需的全部计算。 The advantages of using a TSV file is that it can be easily edited within Excel, while at the same time being easy to parse and load from within a script in Tabular Editor.

本文将以经典的 Adventure Works 为例，聚焦 Internet Sales 事实表及其相关维度表：

![image](https://user-images.githubusercontent.com/8976200/44193845-85cd5d80-a134-11e8-8f39-2da1380fdc63.png)

事实表中有多个数值列，我们将它们简单汇总为七个简单的 `SUM` 度量值：

![image](https://user-images.githubusercontent.com/8976200/44196409-270be200-a13c-11e8-9994-0a8f2fa19e1a.png)

For the purposes of this article, we'll call these the **base measures**. In real life, the formula of the base measures could be more complex, but that does not matter in general, as we will see in a moment. The central idea, is that we will use our TSV file to define a set of formulas involving the base measures as well as filter contexts that will be applied outside the calculations.

\*\*\* TODO \*\*\*

，只要我们要构建的计算仍然可以由一个或多个基础度量值组合而成，并且能在任何有效的筛选语境中求值。

\*\*\* TODO \*\*\*
