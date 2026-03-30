本文演示如何在 Tabular Editor 中使用“高级脚本”功能，以一致的方式在多个对象之间维护 DAX 逻辑。 在[实用脚本片段一文](/Useful-script-snippets)中，我们已经看到，[如何使用自定义操作快速批量生成许多逻辑相近的度量值](/Useful-script-snippets#generate-time-intelligence-measures)；例如在创建时间智能计算时，这会很有用。

在本文中，我们将在这个思路上更进一步，创建一个脚本“框架”，使我们能够在一个 TSV 文件（Tab Separated Values，制表符分隔值）中集中定义所需的全部计算。 使用 TSV 文件的优势在于：既可以在 Excel 中轻松编辑，又便于在 Tabular Editor 的脚本中解析并加载。

本文将以经典的 Adventure Works 为例，聚焦 Internet Sales 事实表及其相关维度表：

![image](https://user-images.githubusercontent.com/8976200/44193845-85cd5d80-a134-11e8-8f39-2da1380fdc63.png)

事实表中有多个数值列，我们将它们简单汇总为七个简单的 `SUM` 度量值：

![image](https://user-images.githubusercontent.com/8976200/44196409-270be200-a13c-11e8-9994-0a8f2fa19e1a.png)

在本文中，我们把这些称为**基础度量值**。 在实际项目中，基础度量值的公式可能更复杂，但这通常无关紧要——稍后你会看到原因。 核心思路是：我们用 TSV 文件定义一组基于基础度量值的公式，并定义将在计算之外应用的筛选语境。

\*\*\* TODO \*\*\*

，只要我们要构建的计算仍然可以由一个或多个基础度量值组合而成，并且能在任何有效的筛选语境中求值。

\*\*\* TODO \*\*\*
