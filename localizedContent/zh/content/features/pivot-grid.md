---
uid: pivot-grid
title: Pivot Grid
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
# Pivot Grid

> [!NOTE]
> 本文中的信息与 Tabular Editor 3.16.0 或更高版本相关。请确保您正在使用最新版本的 Tabular Editor 3，以便利用新功能和改进。

在开发语义模型时，您可能经常希望测试您的 DAX 表达式是否返回预期值。传统上，这是使用 Excel 或 Power BI 等客户端工具来完成的。使用 Tabular Editor 3，您可以使用**数据透视网格**，其行为与 Excel 中广为人知的数据透视表非常相似。Pivot Grid让您能够快速创建模型中数据的汇总视图，从而让您能够在按各种列和层次结构进行筛选和切片时测试DAX度量值的行为。

![Pivot Grid 示例](~/content/assets/images/pivot-grid-example.png)

上图的屏幕截图显示了一个包含两个度量值（`[Total Net Order Value]` 和 `[Net Orders]`）的 Pivot Grid，该 Pivot Grid 按年份水平切片，筛选为 2021 年和 2022 年，并按产品层次结构垂直切片。Tabular Editor 3 用户可以使用此功能来确保 Measure 背后的 DAX 表达式按预期工作，并快速验证模型中的数据。

默认情况下，每次保存对语义模型的更改（Ctrl+S）时，Pivot Grid 都会自动更新。因此，您可以快速迭代 DAX 表达式，并在 Pivot Grid 中查看结果，而无需等待模型刷新。只需更改度量值、保存模型，即可直接在 Pivot Grid 中看到新的度量值定义。一个好的工作流程是在**表达式编辑器**中处理 DAX 表达式或使用**DAX 脚本**时，在单独的窗口中打开 Pivot Grid。

> [!TIP]
> 关于术语的一些说明：
> - **字段**是指模型度量值、KPI、列和层次结构。换言之，任何可以拖入Pivot Grid的内容。
> - **KPI** 是一种特殊类型的度量值，可以在 Tabular Editor 中创建。它们在 Pivot Grid 中显示的方式与度量值一样，但带有一个特殊图标，以表示它们是 KPI。每个KPI最多可以有3个不同的值（目标、趋势和状态），这些值在Pivot Grid中分别显示。
> - Pivot Grid 中的**列**（例如“列区域”一词中的列）不应与模型中的列混淆。在 Pivot Grid 中，列用于水平切片数据，而行用于垂直切片数据。
> - Pivot Grid 中的**单元格**是行和列相交处的单个数据点。每个单元格都包含一个单个值，该值是特定度量的 DAX 表达式的结果，在*行区域*和*列区域*中的值所产生的筛选器上下文中进行评估，并与应用于*筛选器区域*中字段的任何筛选器相结合。

> [!NOTE]
> 具有多维背景的开发人员可能更熟悉*维度*和*属性*这两个术语。在语义模型中，*维度*由模型*表*表示，*属性*由模型*列*表示。语义模型中的*层次结构*只是将列分组的一种方式，例如在日历层次结构中：年 > 季度 > 月 > 日。在多维模型中，此类层次结构曾被称为*属性层次结构*或*用户定义的层次结构*。

## 创建 Pivot Grid

您可以通过**文件 > 新建 > 新建Pivot Grid**菜单选项来创建一个新的空Pivot Grid。或者，在**TOM Explorer**中选择一个或多个度量值，右键单击或转到**度量值**菜单，然后选择**添加到 Pivot Grid**，以使用所选度量值创建新的 Pivot Grid。

![通过 TOM Explorer 创建 Pivot Grid](~/content/assets/images/create-pivot-grid-from-TOM-Explorer.png)

您可以根据需要创建任意数量的 Pivot Grid。

> [!IMPORTANT]
> 仅当 Tabular Editor 3 连接到 Analysis Services 实例或 Power BI/Fabric XMLA endpoint 时，才能使用创建 Pivot Grid 的选项。

## Pivot Grid布局

Pivot Grid分为4个区域：**筛选器区域**、**列区域**、**行区域**和**数据区域**。您可以将字段从**字段列表**或**TOM资源管理器**拖入这些区域，以创建Pivot Grid布局。**数据区域**是放置度量值或 KPI 的区域，而**行区域**和**列区域**用于按层次结构和列对数据进行切片。**筛选器区域**用于根据列或层次结构中的值筛选数据。

![突出显示的空 Pivot Grid](~/content/assets/images/empty-pivot-grid-highlighted.png)

上方的屏幕截图显示了一个空的Pivot Grid布局。字段列表底部的4个空框代表Pivot Grid的4个区域。您可以将字段从“字段列表”拖入这些列表框，以创建Pivot Grid布局。或者，您可以直接将字段拖入Pivot Grid。

## Pivot Grid 菜单和工具栏

默认情况下，当 Pivot Grid 是 Tabular Editor 3 中的活动窗口时，将提供**Pivot Grid**菜单和工具栏。菜单包含与工具栏相同的操作。

![Pivot Grid工具栏](~/content/assets/images/pivot-grid-toolbar.png)

![Pivot Grid菜单](~/content/assets/images/pivot-grid-menu.png)

这些操作包括：

- **模拟身份…**：显示一个对话框，允许你指定要通过 Pivot Grid 模拟的角色或用户。当您想要测试模型对不同用户或角色的行为时，这非常有用，例如，当[RLS 或 OLS](xref:data-security-about)已应用于模型时。
- **刷新**：重新执行由Pivot Grid生成的查询。当禁用自动刷新时，或者在 Tabular Editor 3 之外对模型进行了更改时，此操作非常有用。
- **自动刷新**：切换自动刷新功能的启用或禁用。启用自动刷新后，每次您保存对模型的更改时，或者在[数据刷新操作](xref:data-refresh-view)完成后，Pivot Grid 将自动刷新。
- **清除筛选器**：清除Pivot Grid中的所有筛选器。
- **清除**：从Pivot Grid中删除所有字段。
- **在列上显示空值**：切换是否应在 Pivot Grid 中显示空值（对于添加到 Pivot Grid 列区域的字段）。
- **在行上显示空值**：切换是否应在 Pivot Grid 中显示空值（对于添加到 Pivot Grid 行区域的字段）。
- **字段列表**：切换字段列表的显示/隐藏。

## 字段列表

默认情况下，字段列表显示在Pivot Grid的右侧。字段列表包含模型中可用的所有字段（度量值、KPI、列和层次结构）。您可以将字段从“字段列表”拖动到Pivot Grid中，以创建布局。您还可以将字段在Pivot Grid的不同区域之间拖动，以重新排列布局。

“字段列表”本身可以停靠在 Pivot Grid 的左侧或右侧、上方或下方，可以隐藏，也可以取消停靠，使其作为单独的窗口“浮动”。如果您打开了多个 Pivot Grid，则每个 Pivot Grid 都有自己的字段列表。

如果您不希望默认显示字段列表，请取消选中**工具 > 首选项 > 数据浏览 > Pivot Grid > 字段列表**下的**始终显示字段列表**选项。

您可以在**工具 > 首选项 > 数据浏览 > 数据透视表 > 字段列表 > 布局**下更改字段列表的默认布局。您还可以通过右键单击字段列表的空白区域，然后从上下文菜单中选择所需的布局，来更改任何字段列表的布局。

![字段列表设置](~/content/assets/images/field-list-settings.png)

默认情况下，您添加到 Pivot Grid 的任何字段都将保留在字段列表中。如果您希望隐藏添加到 Pivot Grid 的字段，可以取消选中**工具 > 首选项 > 数据浏览 > Pivot Grid > 字段列表**下的**保持字段可见**选项（此行为类似于 Pivot Grid 在 Tabular Editor v. 3.16.0 之前的运作方式）。

如果您正在处理一个庞大而复杂的模型，并且预计 Pivot Grid 中使用的度量值会相对较慢，则可以选中字段列表底部的**延迟布局更新**选项。这将阻止 Pivot Grid 在您每次添加或删除字段时更新布局。如果您打算在更新 Pivot Grid 布局之前对其进行多次更改，此选项可能很有用。点击**更新**按钮，将更改应用于 Pivot Grid。

> [!IMPORTANT]
> 不含属性层次结构的列（IsAvailableIn MDX = false）不能在Pivot Grid中使用，也不会显示在字段列表中。

## 自定义 Pivot Grid

### 添加字段

有几种方法可以将字段添加到 Pivot Grid：

**从 TOM Explorer：**

- 右键单击一个或多个*度量值*，然后选择**添加到 Pivot Grid**。
- 右键单击*列*或*层次结构*，然后选择任意一个**添加到数据透视**选项（在行、列或筛选器之间进行选择）。
- 如果Pivot Grid中已显示度量值、列或层次结构，则右键单击选项将允许您**从Pivot Grid中删除**。此外，您还将看到在Pivot Grid的不同区域之间移动列或层次结构的选项。
- 当在 TOM Explorer 中选择一个或多个此类对象时，上述所有选项也可以通过**度量值**、**列**和**层次结构**菜单（分别）使用。
- 除上述操作外，您还可以将一个或多个度量值、列或层次结构从 TOM Explorer 拖动到 Pivot Grid 区域。

![通过 TOM Explorer 将层次结构添加到 Pivot Grid](~/content/assets/images/add-through-tom-explorer.png)

**从字段列表：**

- 将字段从“字段列表”拖到Pivot Grid中。
- 将字段从“字段列表”拖到“字段列表”底部的区域列表框中，以将其添加到 Pivot Grid 中。
- 右键单击字段列表中的字段，以查看将其添加到 Pivot Grid 的选项。
- 如果字段已显示在Pivot Grid中，则右键单击上下文菜单中也会有删除字段或将其移动到其他区域（仅限列/层次结构字段）的选项。
- 双击字段将立即将其添加到 Pivot Grid 中。量度/KPI 被添加到数据区域，而列和层次结构被添加到筛选器区域。

![通过字段列表添加](~/content/assets/images/add-through-field-list.png)

### 调整字段

将字段添加到 Pivot Grid 后，您可以调整列的宽度，以便更好地容纳其内容。双击列标题分隔符将自动调整列宽，以适应列的内容。您还可以拖动列标题分隔符，手动调整列宽。最后，您可以通过右键单击列标题，使用上下文菜单选项**最佳适应**或**设置宽度……**。

![列最佳适应 2](~/content/assets/images/best-fit-columns-2.png)

要同时对Pivot Grid中的所有列应用“最佳拟合”或设置特定的像素宽度，请右键单击“值”标题，然后从上下文菜单中选择所需选项。

默认情况下，字段标题垂直展开以适应字段名称。要将字段标题限制为一行，请在**工具 > 首选项 > 数据浏览 > 数据透视表 > 字段标题**下取消选中**字段标题自动换行**。

要更改 Pivot Grid 中字段的顺序，您可以将字段在 Pivot Grid 的不同区域之间拖动。您还可以拖动同一区域内的字段，以更改其顺序。要从 Pivot Grid 中删除字段，请将其拖回字段列表，或右键单击该字段，然后从上下文菜单中选择**从 Pivot Grid 中删除**。

如果您希望将度量值显示在行上而不是列上，请将“值”字段从列区域拖动到行区域。

### 可视化规则

您可以向数据透视中的单元格添加可视化规则，这对于根据单元格的值突出显示单元格非常有用，例如，以便更好地发现异常值。要添加可视化规则，请右键单击 Pivot Grid 中任何数据区域单元格，然后从上下文菜单中选择要应用的规则（请参阅下图）。

![自定义 Pivot Grid](~/content/assets/images/customizing-pivot-grids.png)

## 持久化 Pivot Grid 布局

关闭 Pivot Grid 时，Tabular Editor 将提示您保存 Pivot Grid 的布局。如果您选择保存布局，下次打开数据透视表时，它将恢复到关闭时的布局。当Pivot Grid为活动窗口时，您还可以通过按 (Ctrl+S) 或使用**“文件”>“保存”**选项，手动保存Pivot Grid的布局。

用于保存 Pivot Grid 布局的文件扩展名为 `.te3pivot`。这是一个简单的 json 文件，用于指定在 Pivot Grid 中显示哪些模型对象，以及将它们放置在哪些区域。对象通过名称和沿袭标签（如果存在）进行引用，因此即使自保存布局以来模型已更改，通常也可以还原 Pivot Grid 布局。

> [!NOTE]
> 您可以打开在不同模型中创建的 Pivot Grid 布局。如果布局使用了您所连接的模型中不存在的字段，则会显示警告，并且这些字段将从布局中删除。当已打开的 Pivot Grid 保持打开状态并连接到不同的模型时，也会发生同样的情况，如[切换模型](#switching-models)中所述。要关闭警告，请在**工具 > 首选项 > 数据浏览 > Pivot Grid**下取消选中**如果 Pivot Grid 与模型不匹配则显示警告**。

## 切换模型

当您打开不同的模型时，已打开的 Pivot Grid 将保持打开状态并连接到新模型。每个 Pivot Grid 都保留其字段布局，新模型中不包含的任何字段都会从布局中删除。删除字段时，将显示警告：“刚才打开的模型不包含此Pivot Grid使用的所有字段。缺少的字段已从布局中删除。” 如果新模型没有可浏览的数据，例如从不含工作区数据库的文件加载的模型，则Pivot Grid将被清空。

如果 Pivot Grid 的**自动刷新**已关闭，则该网格将保留其先前的布局和值，直到您单击**刷新**或打开其字段列表。此时，它将连接到新模型并删除所有缺失的字段。

如果已打开的 Pivot Grid 的布局中包含字段，则在新模型打开之前，将显示**Pivot Grid 将重新绑定到新模型**确认消息：

- **是**将打开新模型。
- **是，不再询问**将打开新模型并清除**如果 Pivot Grid 与模型不匹配则显示警告**偏好设置，这将同时关闭此确认提示和有关已丢弃字段的警告。
- **取消**将保持当前模型加载的状态，所有文档均保持不变。

要保留原始布局，请点击**取消**，并在切换模型之前使用**文件 > 另存为**保存 Pivot Grid 的副本。

在**工具 > 首选项 > 数据浏览 > Pivot Grid**下取消选中**打开其他模型时保持 Pivot Grid 打开**，以便在您打开其他模型时关闭 Pivot Grid。此选项默认为选中状态。

## 其他功能

Pivot Grid还有一些值得了解的实用功能：

- 如果右键单击某个字段，您将可以选择**转到**该字段。这将使 TOM Explorer 成为焦点，并选中等效的模型对象。对于度量值和计算列，**表达式编辑器**将成为焦点，并显示度量值的 DAX 表达式。
- 如果右键单击 Pivot Grid 中的单元格，您可以选择**调试此值**选项。这将启动[**DAX 调试器**](xref:dax-debugger)，从产生单元格中值的特定度量值和筛选器上下文开始。
- Pivot Grid **正在刷新**时，某些工具栏项将被禁用，上下文菜单操作将暂时不可用。

## 限制和已知问题

以下是 Tabular Editor 3.16.0 中 Pivot Grid 的已知限制和问题列表，我们正在努力在未来版本中解决这些问题：

- 将Pivot Grid布局另存为`.te3pivot`文件时，格式规则（例如图标集、数据条等）未正确保留。
- 如果您在与保存布局的模型不同的模型上打开 `.te3pivot` 文件，或者在已保存的 Pivot Grid 打开时切换模型，则当前模型中不存在的字段将从布局中删除。如果随后进行保存（**Ctrl+S**），则 `.te3pivot` 文件将被覆盖，且不包含这些字段。
- 使用“按列分组”属性的列（包括字段参数列）不能单独添加到行区域或列区域。这样做会导致出现错误“*列 X 是复合键的一部分，但并非复合键的所有列都包含在表达式或其依赖表达式中*”。这是 MDX 客户端的一般性限制，在 Excel 数据透视表中也存在使用此类列时会出现这种情况。要解决此问题，请在添加从属列*之前*将相关的“分组依据列”添加到Pivot Grid。例如，如果 `[ProductKey]` 被配置为 `[ProductName]` 的“分组依据列”，请先将 `[ProductKey]` 添加到行区域或列区域，然后再添加 `[ProductName]`。
- 对行区域或列区域中的列应用显式升序或降序排序时，无论列的数据类型如何，都会按字母顺序将值作为字符串排序。格式化为长日期的日期（例如“2024 年 5 月 4 日”）和整数按字典顺序排序，而不是按时间顺序或数字顺序排序。这是 MDX 客户端排序方式的限制，连接到模型的 Excel 数据透视表也会出现相同的行为。要获得按时间顺序或数值顺序的排序，请依靠列的自然排序（不要应用显式排序），或使用模型列上的**按列排序**属性，以指向具有可排序底层值的列。