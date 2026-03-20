---
uid: pivot-grid
title: Pivot Grid
author: Daniel Otykier
updated: 2024-05-28
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: 桌面版
          full: true
        - edition: 商业版
          full: true
        - edition: 企业版
          full: true
---

# Pivot Grid

> [!NOTE]
> 本文信息适用于 Tabular Editor 3.16.0 或更高版本。 请确保你使用的是最新版本的 Tabular Editor 3，以便充分利用新增功能和改进。

在开发语义模型时，你经常需要测试 DAX 表达式是否返回了预期值。 传统上，这通常通过 Excel 或 Power BI 等客户端工具来完成。 在 Tabular Editor 3 中，你可以使用 **Pivot Grids**，其行为与 Excel 中广为人知的 PivotTables 非常相似。 Pivot Grid 可让你快速创建模型数据的汇总视图，从而在对不同列和层级进行筛选与切片时，测试 DAX 度量值的行为。

![Pivot Grid 示例](~/content/assets/images/pivot-grid-example.png)

上面的截图展示了一个 Pivot Grid，其中包含两个度量值 `[Total Net Order Value]` 和 `[Net Orders]`：横向按 Year 切片，并筛选到 2021 和 2022；纵向按 Product Hierarchy 切片。 Tabular Editor 3 用户可以使用此功能，确保度量值背后的 DAX 表达式按预期工作，并快速验证模型中的数据。

默认情况下，每次你保存对语义模型的更改（Ctrl+S）时，Pivot Grid 都会自动更新。 因此，你可以快速迭代 DAX 表达式并在 Pivot Grid 中查看结果：修改度量值并保存模型后，无需等待模型刷新，Pivot Grid 会立即反映新的度量值定义。 一个不错的工作流是：在单独的窗口中打开 Pivot Grid，同时在 **表达式编辑器** 中编写 DAX 表达式，或使用 **DAX脚本**。

> [!TIP]
> 关于术语的一些说明：
>
> - **Fields** 指模型度量值、KPI、列和层级。 换句话说，就是任何可以拖到 Pivot Grid 里的内容。
> - **KPIs** 是一种特殊的度量值类型，可在 Tabular Editor 中创建。 它们在 Pivot Grid 中的显示方式与度量值相同，但会带有一个特殊图标，用于标明它们是 KPI。 每个 KPI 最多可包含 3 个不同的值（目标、趋势和状态），并在 Pivot Grid 中分别显示。
> - Pivot Grid 中的**列**（例如术语“Column Area”中的列）不要与模型中的列混为一谈。 在 Pivot Grid 中，列用于按水平方向切分数据，而行用于按垂直方向切分数据。
> - Pivot Grid 中的**单元格**是行与列交叉处的单个数据点。 每个单元格仅包含一个值。该值是在由 _Row Area_ 和 _Column Area_ 中的值所产生的筛选语境下，并结合对 _Filter Area_ 中各字段应用的任何筛选条件，对特定度量值的 DAX 表达式求值得到的结果。

> [!NOTE]
> 具有多维模型背景的开发者可能更熟悉 _Dimensions_ 和 _Attributes_ 这两个术语。 在语义模型中，_Dimensions_ 由模型_表_表示，而 _Attributes_ 由模型_列_表示。 语义模型中的 _Hierarchies_ 只是将多列分组在一起的一种方式，例如日历层次结构：Year > Quarter > Month > Day。 在多维模型中，这类层次结构过去称为 _Attribute Hierarchies_ 或 _User-Defined Hierarchies_。

## 创建 Pivot Grid

你可以通过菜单选项 **File > New > New Pivot Grid** 创建一个新的空 Pivot Grid。 或者，在 **TOM Explorer** 中选择一个或多个度量值，右键点击或打开 **度量值** 菜单并选择 **Add to Pivot Grid**，即可创建一个包含所选度量值的新 Pivot Grid。

![从 TOM Explorer 创建 Pivot Grid](~/content/assets/images/create-pivot-grid-from-TOM-Explorer.png)

你可以按需创建任意数量的 Pivot Grid。

> [!IMPORTANT]
> 仅当 Tabular Editor 3 连接到 Analysis Services 实例或 Power BI / Fabric XMLA endpoint 时，才能创建 Pivot Grid。

## Pivot Grid 布局

Pivot Grid 分为 4 个区域：**Filter Area**、**Column Area**、**Row Area** 和 **Data Area**。 你可以将字段从 **字段列表** 或 **TOM Explorer** 拖入这些区域，来创建 Pivot Grid 布局。 **Data Area** 用于放置度量值或 KPI；**Row Area** 和 **Column Area** 用于按层次结构和列切分数据。 **Filter Area** 用于根据列或层次结构中的值筛选数据。

![突出显示的空 Pivot Grid](~/content/assets/images/empty-pivot-grid-highlighted.png)

上图展示了一个空的 Pivot Grid 布局。 字段列表底部的 4 个空框分别代表 Pivot Grid 的 4 个区域。 你可以将字段从字段列表拖到这些列表框中，以创建 Pivot Grid 的布局。 或者，你也可以直接将字段拖到 Pivot Grid 中。

## Pivot Grid 菜单和工具栏

默认情况下，在 Tabular Editor 3 中，只要 Pivot Grid 是活动窗口，就会显示 **Pivot Grid** 菜单和工具栏。 这个菜单包含与工具栏相同的操作。

![Pivot Grid 工具栏](~/content/assets/images/pivot-grid-toolbar.png)

![Pivot Grid 菜单](~/content/assets/images/pivot-grid-menu.png)

这些操作包括：

- **模拟身份...**：显示一个对话框，允许你在 Pivot Grid 中指定要模拟的角色或用户。 当你希望测试模型在不同用户或角色下的行为时，这会很有用，例如模型已应用了 [RLS 或 OLS](xref:data-security-about) 的情况。
- **刷新**：重新执行 Pivot Grid 生成的查询。 当禁用自动刷新时，或在 Tabular Editor 3 之外对模型进行了更改时，这会很有用。
- **自动刷新**：开启/关闭自动刷新。 启用自动刷新后，每次保存对模型的更改，或当某个 [数据刷新操作](xref:data-refresh-view) 完成时，Pivot Grid 都会自动刷新。
- **清除筛选器**：清除 Pivot Grid 中的所有筛选器。
- **清除**：从 Pivot Grid 中移除所有字段。
- **在列中显示空值**：切换是否在 Pivot Grid 中显示空值，适用于添加到 Pivot Grid 列区域的字段。
- **在行中显示空值**：切换是否在 Pivot Grid 中显示空值，适用于添加到 Pivot Grid 行区域的字段。
- **字段列表**：切换字段列表显示/隐藏。

## 字段列表

默认情况下，字段列表显示在 Pivot Grid 的右侧。 字段列表包含模型中所有可用字段（度量值、KPI、列和层级结构）。 你可以将字段从字段列表拖到 Pivot Grid 中以创建布局。 你还可以在 Pivot Grid 的不同区域之间拖动字段，以重新排列布局。

字段列表可以停靠在 Pivot Grid 的左侧、右侧、上方或下方；也可以隐藏；或取消停靠，以独立窗口“浮动”显示。 如果你同时打开了多个 Pivot Grid，每个 Pivot Grid 都有自己的字段列表。

如果你希望默认不显示字段列表，请在 **工具 > 偏好 > 数据浏览 > Pivot Grid > 字段列表** 下取消勾选 **始终显示字段列表** 选项。

你可以在 **工具 > 偏好 > 数据浏览 > Pivot Grid > 字段列表 > 布局** 中更改字段列表的默认布局。 你也可以更改任何字段列表的布局：在字段列表的空白处单击右键，然后在快捷菜单中选择所需的布局。

![字段列表设置](~/content/assets/images/field-list-settings.png)

默认情况下，你添加到 Pivot Grid 的任何字段都会在字段列表中保持显示。 如果你希望隐藏已添加到 Pivot Grid 的字段，可以在 **工具 > 偏好 > 数据浏览 > Pivot Grid > 字段列表** 下取消勾选 **保持字段可见** 选项（此行为与 Tabular Editor v. 3.16.0 之前的 Pivot Grid 类似）。

如果你正在处理大型复杂模型，并且预计 Pivot Grid 中用到的度量值计算会比较慢，你可以勾选字段列表底部的 **延迟更新布局** 选项。 这样可避免 Pivot Grid 在你每次添加或移除字段时都更新布局；如果你打算在更新前对 Pivot Grid 布局做多项修改，这会很有用。 点击 **更新** 按钮，将更改应用到 Pivot Grid。

> [!IMPORTANT]
> 没有属性层次结构（IsAvailableIn MDX = false）的列无法在 Pivot Grid 中使用，也不会显示在字段列表中。

## 自定义 Pivot Grid

### 添加字段

将字段添加到 Pivot Grid 有多种方式：

**从 TOM Explorer：**

- 右键单击一个或多个 _度量值_，然后选择 **添加到 Pivot Grid**。
- 右键单击 _列_ 或 _层次结构_，然后选择任一 **Add to pivot** 选项（可选择添加到行、列或筛选器）。
- 如果某个度量值、列或层次结构已经显示在 Pivot Grid 中，右键选项会允许你 **从 Pivot Grid 中移除**。 此外，你还会看到用于在 Pivot Grid 的不同区域之间移动列或层次结构的选项。
- 当你在 TOM Explorer 中选择了一个或多个此类对象时，上述所有选项也可以分别在 **度量值**、**列** 和 **层次结构** 菜单(分别)中找到。
- 除了以上方式，你还可以将一个或多个度量值、列或层次结构从 TOM Explorer 拖放到 Pivot Grid 的各个区域。

![通过 TOM Explorer 将层次结构添加到 Pivot Grid](~/content/assets/images/add-through-tom-explorer.png)

**从字段列表中：**

- 将字段从字段列表拖放到 Pivot Grid。
- 将字段从字段列表拖放到字段列表底部的各个区域列表框中，即可将其添加到 Pivot Grid。
- 在“字段列表”中右键单击某个字段，即可看到将其添加到 Pivot Grid 的选项。
- 如果某个字段已显示在 Pivot Grid 中，右键上下文菜单还会提供移除该字段的选项，或将其移动到其他区域（仅列/层级字段）。
- 双击某个字段会立即将其添加到 Pivot Grid。 度量值/KPI 会添加到“数据区域”，而列和层级字段会添加到“筛选区域”。

![通过字段列表添加](~/content/assets/images/add-through-field-list.png)

### 调整字段

将字段添加到 Pivot Grid 后，你可以调整列宽，让内容显示得更合适。 双击列标题分隔线，会自动将列宽调整为适合该列内容的宽度。 你也可以拖动列标题分隔线，手动调整列宽。 最后，你可以在列标题上右键单击，在上下文菜单中使用 **最佳适应** 或 **设置宽度...** 选项。

![最佳适应列 2](~/content/assets/images/best-fit-columns-2.png)

要同时对 Pivot Grid 中的所有列应用“最佳适应”，或为所有列设置特定的像素宽度，请在“值”标题上右键单击，然后在上下文菜单中选择所需选项。

默认情况下，字段标题会在垂直方向自动扩展，以适应字段名称的内容。 如果你想把字段标题的高度限制为一行，可以在 **工具 > 偏好 > Pivot Grid > 字段标题** 中禁用 **字段标题自动换行** 选项。

要更改 Pivot Grid 中字段的顺序，你可以在 Pivot Grid 的不同区域之间拖动字段。 你也可以在同一区域内拖动字段来调整顺序。 要从 Pivot Grid 中移除字段，你可以把它拖回“字段列表”，或在该字段上右键单击，然后从上下文菜单中选择 **从 Pivot Grid 中移除**。

如果你想让度量值显示在行上而不是列上，把“值”字段从“列区域”拖到“行区域”即可。

### 可视化规则

你可以为 Pivot Grid 中的单元格添加可视化规则，这有助于根据数值突出显示单元格，例如更容易发现异常值。 要添加可视化规则，在 Pivot Grid 的任意“数据区域”单元格上右键单击，然后从上下文菜单中选择要应用的规则（见下方截图）。

![自定义 Pivot Grid](~/content/assets/images/customizing-pivot-grids.png)

## 保存 Pivot Grid 布局

当你关闭 Pivot Grid 时，Tabular Editor 会提示你保存 Pivot Grid 的布局。 如果你选择保存布局，那么下次打开 Pivot Grid 时，它会恢复到你关闭时的布局。 当 Pivot Grid 窗口处于活动状态时，你也可以按 (Ctrl+S) 或使用 **文件 > 保存** 选项手动保存 Pivot Grid 的布局。

用于保存 Pivot Grid 布局的文件扩展名是 `.te3pivot`。 这是一个简单的 json 文件，用于指定 Pivot Grid 中显示哪些模型对象，以及它们放置在哪些区域。 对象通过名称和 Lineage tag（如有）进行引用，因此即使自保存布局以来模型发生了修改，通常也能恢复 Pivot Grid 布局。

> [!NOTE]
> 你可以打开在其他模型中创建的 Pivot Grid 布局，不过要注意：该布局中的字段可能在你当前连接的模型中并不存在。 在这种情况下，Pivot Grid 会显示一条警告信息，并将模型中不存在的字段从布局中移除。 你可以在 **工具 > 偏好 > 数据浏览 > Pivot Grid > 如果 Pivot Grid 与模型不匹配则显示警告** 中关闭这条警告信息。

## 其他功能

Pivot Grid 还有一些值得了解的功能：

- 如果你在字段上右键单击，可以选择 **转到** 该字段。 这会将焦点切换到 TOM Explorer，并选中对应的模型对象。 对于度量值和计算列，焦点会切换到 **表达式编辑器**，并显示相应对象的 DAX 表达式。
- 如果你在 Pivot Grid 的单元格上右键单击，可以选择 **调试此值**。 这将启动 [**DAX Debugger**](xref:dax-debugger)，并以生成该单元格值的特定度量值和筛选语境为起点进行调试。
- 当 Pivot Grid 正在 **刷新** 时，某些工具栏项会被禁用，上下文菜单操作也会暂时不可用。

## 限制与已知问题

下面列出了 Tabular Editor 3.16.0 中 Pivot Grid 的已知限制与问题，我们正在努力在后续版本中解决：

- 格式规则（例如图标集、数据条等） 在将 Pivot Grid 布局保存为 `.te3pivot` 文件时，这些规则无法被正确保留。
- 如果你在与保存布局时不同的模型上打开 `.te3pivot` 文件，当前模型中不存在的字段会从布局中移除。 按“保存”(Ctrl+S) 会保存该布局，并将已移除的字段也一并从文件中去除。 我们可能会在未来版本中更改此行为，让 `.te3pivot` 文件在你明确确认之前不会被覆盖。