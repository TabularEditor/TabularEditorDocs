---
uid: pivot-grid
title: Pivot Grid
author: Daniel Otykier
updated: 2026-05-27
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

# Pivot Grid

> [!NOTE]
> 本文中的信息适用于 Tabular Editor 3.16.0 或更高版本。 请确保你使用的是最新版本的 Tabular Editor 3，以充分利用新功能和各项改进。

在开发语义模型时，你可能经常需要测试 DAX 表达式是否返回预期的值。 传统上，这通常是借助 Excel 或 Power BI 等客户端工具来完成的。 在 Tabular Editor 3 中，你可以使用 **Pivot Grid**，其行为与 Excel 中广为人知的数据透视表非常相似。 Pivot Grid 可让你快速为模型中的数据创建汇总视图，从而在按不同列和层次结构进行筛选与切片时，测试 DAX 度量值的表现。

![Pivot Grid 示例](~/content/assets/images/pivot-grid-example.png)

上面的屏幕截图展示了一个 Pivot Grid，其中包含两个度量值 `[Total Net Order Value]` 和 `[Net Orders]`；它在水平方向按 Year 进行切片，并筛选为 2021 和 2022；在垂直方向按 Product Hierarchy 进行切片。 Tabular Editor 3 用户可以使用此功能来确保度量值背后的 DAX 表达式按预期工作，并快速验证模型中的数据。

默认情况下，每次保存对语义模型的更改时（Ctrl+S），Pivot Grid 都会自动更新。 因此，你可以快速迭代 DAX 表达式并在 Pivot Grid 中查看结果：只需修改度量值并保存模型，无需等待模型刷新，Pivot Grid 就会立即反映新的度量值定义。 一个不错的工作流是：在 **表达式编辑器** 中编写 DAX 表达式或使用 **DAX脚本** 时，将 Pivot Grid 在单独的窗口中打开。

> [!TIP]
> 关于术语，这里做几点说明：
>
> - **字段** 指的是模型中的度量值、KPI、列和层次结构。 换句话说，就是任何可以拖入 Pivot Grid 的内容。
> - **KPI** 是一种可在 Tabular Editor 中创建的特殊度量值。 它们在 Pivot Grid 中的显示方式与度量值相同，但会带有特殊图标，以表明它们是 KPI。 每个 KPI 最多可以有 3 个不同的值（目标、趋势和状态），它们会在 Pivot Grid 中分别显示。
> - Pivot Grid 中的 **列**（例如术语“列区域”中的“列”）不要与模型中的列混淆。 在 Pivot Grid 中，列用于在水平方向切分数据，而行用于在垂直方向切分数据。
> - Pivot Grid 中的 **单元格** 是行与列交叉处的单个数据点。 每个单元格都包含一个值。该值是特定度量值的 DAX 表达式在由 _行区域_ 和 _列区域_ 中的值所产生的筛选语境下，并结合应用于 _筛选区域_ 中字段的任何筛选条件计算得到的结果。

> [!NOTE]
> 有多维背景的开发人员可能会更熟悉 _Dimensions_ 和 _Attributes_ 这两个术语。 在语义模型中，_Dimensions_ 由模型 _表_ 表示，而 _Attributes_ 由模型 _列_ 表示。 语义模型中的_层次结构_只是将列归为一组的一种方式，例如日历层次结构：年 > 季度 > 月 > 日。 在多维模型中，这类层次结构过去称为_属性层次结构_或_用户定义的层次结构_。

## 创建 Pivot Grid

你可以通过 **文件 > 新建 > 新建 Pivot Grid** 菜单创建一个新的空 Pivot Grid。 或者，在 **TOM Explorer** 中选择一个或多个度量值，右键单击，或转到 **度量值** 菜单并选择 **添加到 Pivot Grid**，以创建一个包含所选度量值的新 Pivot Grid。

![通过 TOM Explorer 创建 Pivot Grid](~/content/assets/images/create-pivot-grid-from-TOM-Explorer.png)

你可以根据需要创建任意数量的 Pivot Grid。

> [!IMPORTANT]
> 只有当 Tabular Editor 3 连接到 Analysis Services 实例或 Power BI / Fabric XMLA endpoint 时，才会显示用于创建 Pivot Grid 的选项。

## Pivot Grid 布局

Pivot Grid 分为 4 个区域：**筛选区域**、**列区域**、**行区域**和**数据区域**。 你可以将 **字段列表** 或 **TOM Explorer** 中的字段拖到这些区域中，以创建 Pivot Grid 布局。 **数据区域**用于放置度量值或 KPI，而 **行区域** 和 **列区域** 用于按层次结构和列对数据进行切片。 **筛选区域**用于根据列或层次结构中的值筛选数据。

![高亮显示的空白 Pivot Grid](~/content/assets/images/empty-pivot-grid-highlighted.png)

上面的屏幕截图显示了一个空白的 Pivot Grid 布局。 字段列表底部的 4 个空框表示 Pivot Grid 的 4 个区域。 你可以将字段从字段列表拖到这些列表框中，以创建 Pivot Grid 布局。 或者，你也可以将字段直接拖到 Pivot Grid 中。

## Pivot Grid 菜单和工具栏

默认情况下，当 Pivot Grid 是 Tabular Editor 3 中的活动窗口时，会显示 **Pivot Grid** 菜单和工具栏。 该菜单包含与工具栏相同的操作。

![Pivot Grid 工具栏](~/content/assets/images/pivot-grid-toolbar.png)

![Pivot Grid 菜单](~/content/assets/images/pivot-grid-menu.png)

这些操作包括：

- **身份模拟...**：显示一个对话框，可让你指定要在 Pivot Grid 中模拟的角色或用户。 当你想测试模型在不同用户或角色下的行为时，例如在模型已应用 [RLS 或 OLS](xref:data-security-about) 的情况下，这会很有用。
- **刷新**：重新执行由 Pivot Grid 生成的查询。 在禁用自动刷新时，或在 Tabular Editor 3 之外对模型进行了更改时，这会很有用。
- **自动刷新**：打开或关闭自动刷新。 启用自动刷新后，每次你保存对模型的更改，或某个 [数据刷新操作](xref:data-refresh-view) 完成时，Pivot Grid 都会自动刷新。
- **清除筛选器**：清除 Pivot Grid 中的所有筛选器。
- **清除**：从 Pivot Grid 中移除所有字段。
- **在列中显示空值**：切换是否要在 Pivot Grid 中显示空值，适用于已添加到 Pivot Grid 列区域的字段。
- **在行中显示空值**：切换是否要在 Pivot Grid 中显示空值，适用于已添加到 Pivot Grid 行区域的字段。
- **字段列表**：显示或隐藏字段列表。

## 字段列表

默认情况下，字段列表显示在 Pivot Grid 的右侧。 字段列表包含模型中所有可用字段（度量值、KPI、列和层次结构）。 你可以将字段从字段列表拖到 Pivot Grid 中，以创建布局。 你也可以在 Pivot Grid 的不同区域之间拖动字段，以重新排列布局。

字段列表本身可以停靠在 Pivot Grid 的左侧或右侧、上方或下方，也可以隐藏，或者取消停靠，使其作为单独窗口“浮动”显示。 如果你同时打开了多个 Pivot Grid，每个 Pivot Grid 都有各自的字段列表。

如果你不希望默认显示字段列表，请在 **工具 > 偏好 > 数据浏览 > Pivot Grid > 字段列表** 下取消选中 **始终显示字段列表** 选项。

你可以在 **工具 > 偏好 > 数据浏览 > Pivot Grid > 字段列表 > 布局** 下更改字段列表的默认布局。 你也可以在字段列表的空白区域右键单击，然后从上下文菜单中选择所需布局，以更改任意字段列表的布局。

![字段列表设置](~/content/assets/images/field-list-settings.png)

默认情况下，你添加到 Pivot Grid 的任何字段都会在字段列表中保持可见。 如果你希望隐藏已添加到 Pivot Grid 的字段，可以取消选中 **工具 > 偏好 > 数据浏览 > Pivot Grid > 字段列表** 下的 **保持字段可见** 选项（此行为类似于 Tabular Editor v. 3.16.0 之前的 Pivot Grid 工作方式）。

如果你正在处理一个大型且复杂的模型，并且预计 Pivot Grid 中使用的度量值计算起来会比较慢，可以勾选字段列表底部的 **延迟布局更新** 选项。 这会阻止 Pivot Grid 在每次添加或移除字段时都更新布局。如果你打算在更新前对 Pivot Grid 布局进行多项更改，这会很有用。 单击 **更新** 按钮，将更改应用到 Pivot Grid。

> [!IMPORTANT]
> 没有属性层次结构的列（IsAvailableIn MDX = false）无法在 Pivot Grid 中使用，也不会显示在字段列表中。

## 自定义 Pivot Grid

### 添加字段

将字段添加到 Pivot Grid 有多种方式：

**从 TOM Explorer：**

- 右键单击一个或多个 _度量值_，然后选择 **添加到 Pivot Grid**。
- 右键单击某个 _列_ 或 _层次结构_，然后选择任一 **Add to pivot** 选项（可选择添加到行、列或筛选器）。
- 如果某个度量值、列或层次结构已显示在 Pivot Grid 中，右键菜单中也会显示 **从 Pivot Grid 中移除** 选项。 此外，你还会看到可在 Pivot Grid 不同区域之间移动列或层次结构的选项。
- 当你在 TOM Explorer 中选择了一个或多个此类对象时，也可以分别通过 **度量值**、**列** 和 **层次结构** 菜单 (分别) 使用上述所有选项。
- 除了上述方法外，你还可以将一个或多个度量值、列或层次结构从 TOM Explorer 拖放到 Pivot Grid 的各个区域中。

![通过 TOM Explorer 将层次结构添加到 Pivot Grid](~/content/assets/images/add-through-tom-explorer.png)

**从字段列表：**

- 将字段从字段列表拖入 Pivot Grid。
- 将字段从字段列表拖到字段列表底部的各区域列表框中，即可将其添加到 Pivot Grid。
- 右键单击字段列表中的某个字段，可查看将其添加到 Pivot Grid 的选项。
- 如果某个字段已显示在 Pivot Grid 中，右键快捷菜单中也会提供移除该字段，或将其移动到其他区域的选项（仅限列/层次结构字段）。
- 双击某个字段会立即将其添加到 Pivot Grid。 度量值/KPI 会添加到数据区域，而列和层次结构会添加到筛选区域。

![通过字段列表添加](~/content/assets/images/add-through-field-list.png)

### 调整字段

将字段添加到 Pivot Grid 后，你可以调整列宽，以便更好地适应其内容。 双击列标题之间的分隔线会自动调整列宽，使其适应该列内容。 你也可以拖动列标题分隔线来手动调整列宽。 最后，你还可以右键单击列标题，在上下文菜单中选择 **最适合** 或 **设置宽度...**。

![最适合列 2](~/content/assets/images/best-fit-columns-2.png)

若要一次性对 Pivot Grid 中的所有列应用“最适合”或设置指定的像素宽度，请右键单击“值”标题，然后从右键菜单中选择所需选项。

默认情况下，字段标题会在垂直方向自动展开，以容纳字段名称的内容。 如果你希望将字段标题的高度限制为一行，可以在 **工具 > 偏好 > Pivot Grid > 字段标题** 中禁用 **字段标题自动换行** 选项。

若要更改 Pivot Grid 中字段的顺序，可以在 Pivot Grid 的不同区域之间拖动字段。 你也可以在同一区域内拖动字段来更改其顺序。 若要从 Pivot Grid 中移除字段，可将其拖回“字段列表”，或右键单击该字段，然后在右键菜单中选择 **从 Pivot Grid 中移除**。

如果你希望度量值显示在行而不是列上，请将“值”字段从“列区域”拖到“行区域”。

### 可视化规则

你可以为 Pivot Grid 中的单元格添加可视化规则，这有助于根据单元格的值突出显示单元格，例如更容易发现异常值。 若要添加可视化规则，请右键单击 Pivot Grid 数据区域中的任意单元格，然后在右键菜单中选择要应用的规则（见下图）。

![自定义 Pivot Grid](~/content/assets/images/customizing-pivot-grids.png)

## 保存 Pivot Grid 布局

关闭 Pivot Grid 时，Tabular Editor 会提示你保存该 Pivot Grid 的布局。 如果你选择保存布局，下次打开 Pivot Grid 时，它会恢复到关闭时的相同布局。 当 Pivot Grid 为活动窗口时，你也可以按 (Ctrl+S) 或使用 **文件 > 保存** 选项来手动保存 Pivot Grid 的布局。

用于保存 Pivot Grid 布局的文件扩展名是 `.te3pivot`。 这是一个简单的 json 文件，用于指定 Pivot Grid 中显示哪些模型对象，以及它们放置在哪些区域。 对象通过名称和 Lineage tag（如果存在）进行引用，因此即使模型在保存布局后已被修改，Pivot Grid 布局通常仍可恢复。

> [!NOTE]
> 可以打开在其他模型中创建的 Pivot Grid 布局，但请注意，布局中的字段可能在你当前连接的模型中不存在。 在这种情况下，Pivot Grid 会显示警告信息，且模型中不存在的字段会从布局中移除。 你可以在 **工具 > 偏好 > 数据浏览 > Pivot Grid > 如果 Pivot Grid 与模型不匹配则显示警告** 中关闭此警告信息。

## 其他功能

Pivot Grid 还有一些值得了解的实用功能：

- 如果你右键单击某个字段，可以选择 **转到** 该字段。 这会将焦点切换到 TOM Explorer，并选中对应的模型对象。 对于度量值和计算列，焦点会切换到 **表达式编辑器**，并显示该度量值或列的 DAX 表达式。
- 如果你右键单击 Pivot Grid 中的某个单元格，可以选择 **调试此值** 选项。 这将启动 [**DAX 调试器**](xref:dax-debugger)，并以生成该单元格值的特定度量值和筛选语境为起点。
- 当 Pivot Grid 正在**刷新**时，某些工具栏项会被禁用，右键菜单操作也会暂时不可用。

## 限制与已知问题

以下列出了 Tabular Editor 3.16.0 中 Pivot Grid 的已知限制和问题，我们正在后续版本中逐步解决这些问题：

- 格式规则（如图标集、数据条等） 在将 Pivot Grid 布局保存为 `.te3pivot` 文件时，不会被正确保留。
- 如果你在与保存该布局时所用模型不同的模型上打开 .te3pivot 文件，当前模型中不存在的字段将从布局中移除。 按下“保存”(Ctrl+S) 后，布局会以移除这些字段后的状态保存。 我们可能会在未来版本中更改此行为，以避免在未明确确认的情况下覆盖 .te3pivot 文件。
- 使用 **Group By Columns** 属性的列（包括字段参数列）不能单独添加到行区域或列区域。 这样做会产生错误 _“列 X 是复合键的一部分，但表达式或其依赖表达式中并未包含该复合键的所有列”_。 这是 MDX 客户端的通用限制，在 Excel 数据透视表中使用此类列时也会出现相同情况。 要临时解决此问题，请在添加依赖列_之前_，先将相关的 Group By Column 添加到 Pivot Grid。 例如，如果 `[ProductKey]` 被配置为 `[ProductName]` 的 Group By Column，先将 `[ProductKey]` 添加到行区域或列区域，再添加 `[ProductName]`。
- 对行区域或列区域中的列显式应用升序或降序排序时，无论该列的数据类型如何，值都会按字符串的字典顺序排序。 采用长日期格式的日期（例如“May 4, 2024”）和整数会按字典序排序，而不是按时间顺序或数值大小排序。 这是 MDX 客户端排序方式的限制，连接到该模型的 Excel 数据透视表中也会出现相同的行为。 若要按时间顺序或数值顺序排序，请使用该列的自然排序（不要显式应用排序），或在模型列上使用 **按列排序** 属性，将其指向一个底层值可排序的列。