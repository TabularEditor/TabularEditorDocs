---
uid: drag-drop
title: 拖放对象
author: Morten Lønskov
updated: 2026-09-15
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 拖放对象

你可以在 @tom-explorer-view 中重新组织模型——也就是你用来浏览模型的同一棵树。在哪里找到对象，就从哪里拖起；该放到哪里，就放到哪里。无需先切换到单独的建模界面；也不会因为当前视图恰好没有绘制某个对象而无法操作它。

这个手势始终表示移动操作。允许放置时，Tabular Editor 会显示移动光标；不允许时则显示禁止放置光标。而且没有任何修饰键可以把拖动变为复制。如果要复制对象，请改用 **Duplicate**，详见 @duplicate-and-batch。

## 重新组织显示文件夹

拖动一个显示文件夹时，其下的所有对象都会一起移动，包括嵌套的子文件夹，而且层级结构会保持不变。这正是此功能存在的原因：重构大型模型的文件夹布局时，每个文件夹只需一次拖放，而不是每个度量值都要单独编辑一次。

<!-- IMAGE NEEDED: drag-drop-display-folders.gif
     An animation of a display folder being dragged onto another folder in the TOM Explorer,
     with the measures and subfolders beneath it following. Needs a model with at least two
     levels of nesting so the shape is visibly preserved.
     Alt text: "A display folder being dragged onto another folder in the TOM Explorer" -->

树中的其他内容也都按同样方式移动：

- 使用 **Ctrl+单击** 或 **Shift+单击** 选择多个对象，然后一起拖动。只要它们位于同一个表中，你就可以混合选择度量值、列、层次结构和文件夹。
- 将对象放到 **表节点** 本身上，即可把它们从所属文件夹中移出，并恢复到表的顶层。
- 将一个文件夹放到另一个文件夹中，即可将其嵌套。 Tabular Editor 不允许把文件夹放入其自己的子文件夹中，因此你不会把某个分支塞进它自己里面。

每次放下都算作一次 **编辑 > 撤销** 操作，无论涉及多少个对象。

显示文件夹本质上只是每个对象上的一个字符串属性，层级之间用 `\\` 分隔，因此 `Sales\\Ratios` 表示 _Sales_ 下的 _Ratios_ 文件夹。一个对象也可以同时位于多个文件夹中，只需用 `;` 分隔这些路径。

## 将对象移动到另一个表

度量值和计算列可以拖到另一个表中，既可以放到该表节点上，也可以直接放进它的某个显示文件夹中。其他任何类型的对象都不能以这种方式跨表移动。

会随对象一并移动的内容：

- **其名称和说明的翻译**。
- **透视成员关系。** 默认情况下，对象会保留它原本所属的各个透视。在 **Tools > 偏好 > Tabular Editor** 下勾选 _Inherit table membership when object pasted or moved to table_，即可让对象改为继承目标表的归属。
- 有 KPI 的度量值的 **KPI**。
- **错误和警告指示器。** 移动前无效的表达式在移动后仍会被标记为无效，而不会在你下次编辑之前看起来像没问题一样。

> [!WARNING]
> 将 **计算列** 移动到另一个表时，会删除在原位置依赖它的对象。它参与的任何关系都会被删除，基于它构建的任何层次结构级别都会被删除；它会从日历和变体中移除，指向它的 _Sort by column_ 也会被清除。系统不会要求你确认此操作。 **Edit > Undo** 可一步还原所有这些更改，因此在执行其他操作之前先检查模型。

按旧表名引用该列的 DAX，例如 `'Reseller Sales'[Margin]`，不会被重写，仍会继续指向该列已经离开的表。度量值引用写作 `[Measure]`，不带表名，因此不受影响。移动后运行 @using-bpa 或检查 @messages-view，以找出哪里出了问题。

## 构建层次结构并排序计算项

- 将一个或多个**列拖到层次结构上**，把它们添加为级别。拖放到两个现有级别之间即可选择位置。如果某列已经是该层次结构中的级别，则无法再次添加。
- 在层次结构内拖动**级别**可重新排序；将其拖到同一表中的另一个层次结构上，可将其移动到那里。
- 拖动**计算项**可在其所属计算组内重新排序；将其拖到另一个计算组上，则会把它们移过去。

## 表格分组

在 Tabular Editor 3 中，你可以将一个或多个表拖到某个**表格组**上，将它们归入其中。将表拖放到另一张表上，会让它们加入该表所在的组；这也是将表移出组的方法：把它们拖放到一张不属于任何组的表上。

表格组只是 Tabular Editor 中用于整理树视图的便捷功能。它们会作为注解存储，不属于模型元数据，所以不会显示在 Power BI 或 Analysis Services 中。

## 显示文件夹和翻译

拖动只会更改 TOM Explorer &#x4E2D;_&#x4F60;当前正在查看的翻&#x8BD1;_&#x5BF9;应的显示文件夹，而且只改这一项。

- 默认情况下未选择任何翻译时，拖动会写入未翻译版本的显示文件夹名称。已翻译的显示文件夹名称会原样保留，因此在这些区域设置中，对象仍会留在旧文件夹中。
- 在 TOM Explorer 的“翻译”下拉列表中选择某个区域设置后，拖动操作会写入该区域设置下已翻译的显示文件夹，并保持未翻译的显示文件夹不变。

因此，在默认视图中重新整理文件夹时，不会把对应的翻译也一起调整。你可以在 @metadata-translation-editor 中让它们重新保持一致，或运行内置的 Best Practice Analyzer 规则来查找“有显示文件夹但没有已翻译显示文件夹”的对象；该规则的修复操作会将未翻译的值复制到每个区域设置中。

将对象移动到另一张表是个例外：对象自身的翻译会在移动过程中保留。

## 哪些对象可以拖动，以及可以拖到哪里

| 拖动               | 拖放到                | 结果         |
| ---------------- | ------------------ | ---------- |
| 度量值、列、层次结构、显示文件夹 | 同一表中的显示文件夹         | 对象会移入该文件夹  |
| 同上               | 表节点                | 对象会移出其文件夹  |
| 度量值、计算列          | 另一张表，或该表中的显示文件夹    | 对象会移动到该表   |
| 列                | 某个层次结构或其某个级别       | 列会添加为级别    |
| 级别               | 同一层次结构，或该表中的另一层次结构 | 级别会重新排序或移动 |
| 计算项              | 其所属计算组，或另一个计算组     | 项会重新排序或移动  |
| 表                | 一个表格组，或另一张表        | 表会归入该组     |

分区、角色、透视、关系、数据源和共享表达式无法拖动。自上次保存后已删除的对象会在树状结构中以删除线显示，且无法拖动，也不能作为放置目标。对象只会出现在树中已设置显示它们的位置。因此，在将对象拖放到显示文件夹或表格组之前，必须先在工具栏中启用显示文件夹和表格组。

## 通过脚本执行相同操作

显示文件夹是一个属性，因此脚本可以直接设置该字符串值。在普通 C# 字符串中使用 `\\`，或使用逐字字符串：

```csharp
Selected.Measures.SetDisplayFolder(@"Sales\Ratios");
Model.Tables["Sales"].Measures["Margin %"].DisplayFolder = @"Sales\Ratios";
Model.Tables["Sales"].Measures["Margin %"].TranslatedDisplayFolders["da-DK"] = @"Salg\Nøgletal";
```

度量值可以用 `MoveTo` 在表之间移动，错误指示器的保留方式和拖动时完全一样：

```csharp
Model.Tables["Sales"].Measures["Margin %"].MoveTo(Model.Tables["Reseller Sales"]);
```

计算列没有 `MoveTo`。使用与树视图相同的操作：

```csharp
var column = Model.Tables["Sales"].Columns["Margin"];
column.Handler.Actions.MoveObject(column, Model.Tables["Reseller Sales"], false, null);
```

表格组也是一个属性：`Model.Tables["Sales"].TableGroup = "Facts";`。想了解如何运行这些操作，见 @csharp-scripts。

## 在应用程序其他位置进行拖动

TOM Explorer 是唯一会通过拖动来更改模型结构的地方，但它也是其他几种放置操作的拖动来源：

- 将对象拖到 DAX 或 C# 编辑器中，即可插入其完全限定名称，无需手动输入。见 @dax-editor。
- 将树中的表拖到已打开的模型关系图上，即可将它们添加到该关系图中。在关系图中，将某列拖到另一张表中的某列上，即可在它们之间创建关系。见 @diagram-view。
- 将列、度量值或层次结构拖到 Pivot Grid 上，即可将它们添加为字段。
