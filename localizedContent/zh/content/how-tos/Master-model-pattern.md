---
uid: master-model-pattern
title: 主模型模式
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 主模型模式

在一个组织中同时存在多个 Tabular 模型并不罕见，而且它们之间往往有大量功能重叠。 对开发团队来说，让这些模型在共享功能上保持同步更新，往往是个痛点。 本文将介绍一种替代思路：在合适的场景下，将这些模型合并为一个“主”模型，并在部署时按需拆分，分别发布为多个不同的子集模型。 Tabular Editor 通过以一种特殊方式利用透视来支持这种做法（同时也让透视按常规方式工作）。

**免责声明：** 虽然这种方法确实可行，但不受 Microsoft 支持，并且需要投入不少学习成本、脚本编写以及一些“hack”式的变通操作。 是否适合你的团队，请自行评估。

为简化说明，我们以 AdventureWorks 示例模型为例：

![image](https://user-images.githubusercontent.com/8976200/43959290-895c1c96-9cae-11e8-8112-008f54cb400a.png)

假设出于某种原因，你需要将所有与 Internet Sales 相关的内容部署为一个模型，将所有与 Reseller Sales 相关的内容部署为另一个模型。 原因可能是安全、性能、可扩展性；也可能是因为你的团队需要服务多个外部客户，而每个客户都需要一份自己的模型副本，其中既包含共享功能，也包含其专属功能。

与其为每个不同版本各自维护一个开发分支，本文介绍的方法可以让你只维护一个模型，并通过元数据来指示部署时应如何拆分该模型。

## （滥）用透视

思路其实很简单。 首先，在模型中新增若干个透视，数量与需要部署的目标模型数量对应。 记得用一致的方式为这些透视添加前缀，好把它们与面向用户的透视区分开：

![image](https://user-images.githubusercontent.com/8976200/43960154-6b637042-9cb1-11e8-906b-6671bbb9558e.png)

这里我们在透视名称前使用 `-` 号作为前缀。 稍后我们会看到如何从模型中剥离这些透视，从而确保最终用户不会看到它们。 它们仅供模型开发人员使用。

接下来，只需把各个独立模型所需的所有对象添加到对应的透视中即可。 在 Tabular Editor 中使用“透视”下拉列表，确认模型包含所需对象。 下面这段实用脚本可用于确保透视中也包含所有依赖项：

```csharp
// 遍历当前透视中的所有层次结构：
foreach(var h in Model.AllHierarchies.Where(h => h.InPerspective[Selected.Perspective]))
{
    // 确保层次级别使用到的列也包含在透视中：
    foreach(var level in h.Levels) {
        level.Column.InPerspective[Selected.Perspective] = true;
    }
}

// 遍历当前透视中的所有度量值和列：
foreach(var obj in Model.AllMeasures.Cast<ITabularPerspectiveObject>()
    .Concat(Model.AllColumns).Where(m => m.InPerspective[Selected.Perspective])
    .OfType<IDaxDependantObject>().ToList())
{
    // 遍历当前对象所依赖的所有对象：
    foreach(var dep in obj.DependsOn.Deep())
    {
        // 包含对列、度量值和表的依赖：
        var columnDep = dep as Column; if(columnDep != null) columnDep.InPerspective[Selected.Perspective] = true;
        var measureDep = dep as Measure; if(measureDep != null) measureDep.InPerspective[Selected.Perspective] = true;
        var tableDep = dep as Table; if(tableDep != null) tableDep.InPerspective[Selected.Perspective] = true;
    }    
}

// 遍历当前透视中设置了 SortByColumn 的所有列：
foreach(var c in Model.AllColumns.Where(c => c.InPerspective[Selected.Perspective] && c.SortByColumn != null))
{
    c.SortByColumn.InPerspective[Selected.Perspective] = true;   
}
```

**说明：** 首先，脚本会遍历当前透视（即屏幕顶部下拉列表中当前选中的透视）中的所有层次结构。 对于每个此类层次结构，它会确保所有用作层次级别的列都包含在透视中。 接着，脚本会遍历当前透视中的所有列和度量值。 对于这些对象中的每一个，透视中还会包含其所有 DAX 依赖项，例如对度量值、列或表的引用。 注意，诸如 `DISTINCTCOUNT('Customer'[CustomerId])` 这样的表达式，会导致 'Customer' 表的所有列都被包含在透视中，因为 Tabular Editor 会将此类表达式视为同时依赖于 [CustomerId] 列本身以及 'Customer' 表。 最后，脚本会确保任何用作“Sort By”列的列也包含在透视中。

我建议将此脚本在模型级别保存为一个自定义操作，方便以后随时调用。

顺便说一句，如果你想复制某个透视，现在已经可以直接在 UI 中完成。 在资源管理器树中点击“透视”节点，然后在属性网格中点击省略号按钮：

![image](https://user-images.githubusercontent.com/8976200/44028910-c7ffab80-9efb-11e8-813a-5b0f5c137bab.png)

这会打开一个对话框，你可以在其中创建和删除透视，也可以克隆现有透视：

![image](https://user-images.githubusercontent.com/8976200/44028953-f13c91ca-9efb-11e8-936a-1f0e1d4eb93f.png)

作为补充，下面这段脚本会从透视中移除所有不可见且未使用的对象，便于你做一些清理：

```csharp
// 遍历当前透视中的所有列：
foreach(var c in Model.AllColumns.Where(c => c.InPerspective[Selected.Perspective])) {
    if(
        // 如果该列已隐藏（或其父表已隐藏）：
        (c.IsHidden || c.Table.IsHidden) 

        // 且未用于任何关系：
        && !c.UsedInRelationships.Any()
        
        // 且未在透视中被用作其他任何列的 SortByColumn：
        && !c.UsedInSortBy.Any(sb => !sb.IsHidden && sb.InPerspective[Selected.Perspective])
        
        // 且未在透视中的任何层次结构里使用：
        && !c.UsedInHierarchies.Any(h => h.InPerspective[Selected.Perspective])
        
        // 且未在透视中其他可见对象的任何 DAX 表达式里被引用：
        && !c.ReferencedBy.Deep().OfType<ITabularPerspectiveObject>()
            .Any(obj => obj.InPerspective[Selected.Perspective] && !(obj as IHideableObject).IsHidden)
            
        // 且未被任何角色引用：
        && !c.ReferencedBy.Roles.Any()    )
    {
        // 如果满足以上所有条件，则可以将该列从当前透视中移除：
        c.InPerspective[Selected.Perspective] = false; 
    }
}

// 遍历当前透视中的所有度量值：
foreach(var m in Model.AllMeasures.Where(m => m.InPerspective[Selected.Perspective])) {
    if(
        // 如果该度量值已隐藏（或其父表已隐藏）：
        (m.IsHidden || m.Table.IsHidden) 

        // 且未在透视中其他可见对象的任何 DAX 表达式里被引用：
        && !m.ReferencedBy.Deep().OfType<ITabularPerspectiveObject>()
            .Any(obj => obj.InPerspective[Selected.Perspective] && !(obj as IHideableObject).IsHidden)
    )
    {
        // 如果满足以上所有条件，则可以将该度量值从当前透视中移除：
        m.InPerspective[Selected.Perspective] = false; 
    }
}
```

**说明：** 脚本首先会遍历当前选中的透视中的所有列。 只有在满足以下所有条件时，它才会将某列从透视中移除：

- 该列已隐藏（或该列所在的表已隐藏）
- 该列不参与任何关系
- 该列未被用作透视中任何其他可见列的“按列排序”列
- 该列未在透视中的任何层次结构里用作级别
- 该列未在透视中其他可见对象的任何 DAX 表达式里被直接或间接引用
- 该列未用于任何行级筛选表达式

对于度量值，我们做同样的处理，但会简化为只移除满足以下条件的度量值：

- 度量值已隐藏（或该度量值所在的表已隐藏）
- 在透视中，度量值未被其他任何可见对象上的 DAX 表达式直接或间接引用

如果你们是一个共同开发该模型的团队，那么应该已经在使用 Tabular Editor 的[“保存到文件夹”功能](xref:folder-serialization)，并配合 Git 等版本控制系统。 请确保在“File”>“偏好”>“保存到文件夹”下勾选“Serialize perspectives per-object”选项，以避免在透视定义上产生大量合并冲突。

![image](https://user-images.githubusercontent.com/8976200/44029969-935e0efe-9eff-11e8-93de-c1223f7ebe7f.png)

## 增加更精细的控制

到这里，你大概已经猜到了：我们会用脚本为每一个带前缀的开发者透视生成一个模型版本。 脚本会直接从模型中移除所有不包含在指定开发者透视中的对象。 不过在开始之前，还有几种情况需要先处理。

### 控制非透视对象

有些对象，例如透视、数据源和角色，本身并不会被透视包含或排除，但我们可能仍然需要一种方式来指定它们应归属到哪些模型版本中。 为此，我们将使用注解。 回到我们的 Adventure Works 模型，我们可能希望让“Inventory”和“Internet Operation”透视出现在“$InternetModel”和“$ManagementModel”中，而“Reseller Operation”则出现在“$ResellerModel”和“$ManagementModel”中。

那么我们就在这 3 个原始透视上各新增一个名为“DevPerspectives”的注释，并把开发者透视的名称以逗号分隔的字符串形式填进去：

![image](https://user-images.githubusercontent.com/8976200/44032304-01bdcc70-9f07-11e8-9b28-db0912ea1ade.png)

在模型中新增 _用户_ 透视时，记得也添加同样的注释，并填写你希望该 _用户_ 透视被包含到哪些开发者透视中。 后面在脚本生成最终模型版本时，我们会使用这些注释中的信息来包含所需的透视。 数据源和角色也可以用同样的方法。

### 控制对象元数据

在某些情况下，同一个度量值在不同模型版本中可能需要略有不同的表达式或格式字符串。 同样地，我们可以用注释按开发者透视提供元数据，然后在脚本生成最终模型时应用这些元数据。

如果要把所有对象属性序列化为文本，最简单的方式大概是使用 [ExportProperties](/Useful-script-snippets#export-object-properties-to-a-file) 脚本函数。 不过对我们的场景来说有点“杀鸡用牛刀”，所以我们直接指定要作为注释存储的属性即可。 创建以下脚本：

```csharp
foreach(var m in Selected.Measures) { 
    m.SetAnnotation(Selected.Perspective.Name + "_Expression", m.Expression);
    m.SetAnnotation(Selected.Perspective.Name + "_FormatString", m.FormatString);
    m.SetAnnotation(Selected.Perspective.Name + "_Description", m.Description);
}
```

并将其保存为名为“Save Metadata as Annotations”的自定义操作：

![image](https://user-images.githubusercontent.com/8976200/44033695-7a754482-9f0b-11e8-937b-0bc0987ce7cb.png)

同样，将以下脚本保存为名为“Load Metadata from Annotations”的自定义操作：

```csharp
foreach(Measure m in Selected.Measures) { 
    var expr = m.GetAnnotation(Selected.Perspective.Name + "_Expression"); if(expr == null) continue;
    m.Expression = expr;
    m.FormatString = m.GetAnnotation(Selected.Perspective.Name + "_FormatString");
    m.Description = m.GetAnnotation(Selected.Perspective.Name + "_Description");
}
```

我们的思路是：针对每个开发者透视，为需要维护不同版本的每个属性各创建一条注释。 如果你需要像脚本中所示的这些属性（Expression、FormatString、Description）之外，还要分别维护其他属性，直接把它们加到脚本里即可。 其他对象类型也可以用同样的方法，但多数情况下意义不大；通常只有度量值，以及可能的计算列和分区才比较适用（例如，为每个模型版本维护不同的查询表达式）。

使用你新建的自定义操作，将特定于模型版本的更改应用到开发者透视（或手动添加注释）。 例如，在我们的 Adventure Works 示例中，我们希望 [Day Count] 度量值在 $ResellerModel 透视中使用不同的表达式。因此我们先对该度量值应用更改，然后在下拉框中选中“$ResellerModel”透视的情况下，调用“Save Metadata as Annotations”操作：

![image](https://user-images.githubusercontent.com/8976200/44033944-3104e414-9f0c-11e8-9f06-396bf85a0e4f.png)

在上面的截图中，我们为每个开发者透视都创建了 3 条注释。 但在实际使用中，我们只需要为那些属性值应该不同于其默认值的开发者透视创建这些注释。

## 修改分区查询

我们也可以用类似的方法，在不同版本之间对分区查询应用不同的更改。 例如，根据版本不同，我们可能希望在某些分区查询中使用不同的 SQL `WHERE` 条件。 我们先在_表_对象上创建一组新的注释，用来为每个版本指定分区要使用的基础 SQL 查询。 比如在这里，我们希望在三个版本中的两个版本中，限制 Product 表包含哪些记录：

![image](https://user-images.githubusercontent.com/8976200/44736562-69221580-aaa4-11e8-82ee-88388015d30d.png)

对于包含多个分区的表，我们使用“占位符”来指定 WHERE 条件，后续会再替换为实际值：

![image](https://user-images.githubusercontent.com/8976200/44737015-b3f05d00-aaa5-11e8-9bad-cadd5b4dae35.png)

在每个分区中定义占位符的值（注意：必须使用 [Tabular Editor v. 2.7.3](https://github.com/TabularEditor/TabularEditor/releases/tag/2.7.3) 或更高版本，才能通过 UI 编辑分区注释）：

![image](https://user-images.githubusercontent.com/8976200/44737199-2a8d5a80-aaa6-11e8-8813-8189b593da98.png)

在动态分区场景中，别忘了在你用来创建新分区的脚本里，也把这些注释包含进去。 下一节我们会看看如何在部署过程中应用这些占位符值。

## 部署不同的版本

最后，我们准备将模型部署为 3 个不同的版本。 遗憾的是，Tabular Editor 中的 Deployment Wizard UI 无法根据我们创建的透视和注释自动拆分模型，因此我们需要额外编写一个脚本，将模型裁剪为某个特定版本。 然后，这个脚本可以作为命令行部署的一部分来执行，这样就能把整个部署过程打包成一个组件，封装到一个命令文件、PowerShell 可执行文件中，甚至集成到你的构建/自动化部署流程里？

我们需要的脚本如下所示。 思路是：为每个开发者透视分别写一个脚本。 将脚本保存为文本文件，并命名为类似 `ResellerModel.cs`：

```csharp
var version = "ResellerModel"; // TODO: 将此替换为你的开发者透视的名称

// 删除不属于该透视的表、度量值、列和层级结构：
foreach(var t in Model.Tables.ToList()) {
    if(!t.InPerspective[version]) t.Delete();
    else {
        foreach(var m in t.Measures.ToList()) if(!m.InPerspective[version]) m.Delete();   
        foreach(var c in t.Columns.ToList()) if(!c.InPerspective[version]) c.Delete();
        foreach(var h in t.Hierarchies.ToList()) if(!h.InPerspective[version]) h.Delete();
    }
}

// 基于注释移除用户透视，并移除所有开发者透视：
foreach(var p in Model.Perspectives.ToList()) {
    if(p.Name.StartsWith("Dev")) p.Delete();

    // 保留所有不带 "DevPerspectives" 注释的其他透视，同时移除
    // 带有该注释、且注释中未指定 <version> 的透视：
    if(p.GetAnnotation("DevPerspectives") != null && !p.GetAnnotation("DevPerspectives").Contains(version)) 
        p.Delete();
}

// 基于注释移除数据源：
foreach(var ds in Model.DataSources.ToList()) {
    if(ds.GetAnnotation("DevPerspectives") == null) continue;
    if(!ds.GetAnnotation("DevPerspectives").Contains(version)) ds.Delete();
}

// 基于注释移除角色：
foreach(var r in Model.Roles.ToList()) {
    if(r.GetAnnotation("DevPerspectives") == null) continue;
    if(!r.GetAnnotation("DevPerspectives").Contains(version)) r.Delete();
}

// 基于注释修改度量值：
foreach(Measure m in Model.AllMeasures) {
    var expr = m.GetAnnotation(version + "_Expression"); if(expr == null) continue;
    m.Expression = expr;
    m.FormatString = m.GetAnnotation(version + "_FormatString");
    m.Description = m.GetAnnotation(version + "_Description");    
}

// 根据注释设置分区查询：
foreach(Table t in Model.Tables) {
    var queryWithPlaceholders = t.GetAnnotation(version + "_PartitionQuery"); if(queryWithPlaceholders == null) continue;
    
    // 遍历此表中的所有分区：
    foreach(Partition p in t.Partitions) {
        
        var finalQuery = queryWithPlaceholders;

        // 替换所有占位符值：
        foreach(var placeholder in p.Annotations.Keys) {
            finalQuery = finalQuery.Replace("%" + placeholder + "%", p.GetAnnotation(placeholder));
        }

        p.Query = finalQuery;
    }
}

// TODO: 如适用，基于注释修改其他对象……
```

**说明：** 首先，我们会删除脚本第 1 行所定义的透视之外的所有表、列、度量值和层级结构。 然后，我们会删除所有此前按说明加了 "DevPerspectives" 注释的额外对象，并同时移除所有开发者透视本身。 之后，如果存在相关注释，我们会根据注释对度量值表达式、格式字符串或说明进行相应更新。 最后，我们会应用注释中定义的分区查询（如果有），并将占位符值替换为注释里提供的值（如果有）。

注意：如果愿意，我们也可以直接在这个脚本里加入更多针对模型的特定改动；但本练习的重点是：如何直接在 Tabular Editor 内维护多个模型。 无论要部署哪个版本，上面的脚本都是一样的（当然，除了第 1 行）。

最后，我们可以加载 Model.bim 文件、执行脚本，并一次性部署修改后的模型，使用以下 [命令行语法](/Command-line-Options)：

```sh
start /wait /d "c:\Program Files (x86)\Tabular Editor" TabularEditor.exe Model.bim -S ResellerModel.cs -D localhost AdventureWorksReseller -O -R
```

要部署 Internet 或 Management 版本，我们同样操作一次，并提供对应的脚本：

```sh
start /wait /d "c:\Program Files (x86)\Tabular Editor" TabularEditor.exe Model.bim -S InternetModel.cs -D localhost AdventureWorksInternet -O -R
start /wait /d "c:\Program Files (x86)\Tabular Editor" TabularEditor.exe Model.bim -S ManagementModel.cs -D localhost AdventureWorksManagement -O -R
```

这里假设你是在 Model.bim 文件所在目录中执行命令行（如果使用“保存到文件夹”功能，则是在 Database.json 文件所在目录）。 -S 参数用于指示 Tabular Editor 将提供的脚本应用到模型上，-D 参数则用于执行部署。 -O 参数允许覆盖同名的现有数据库，-R 参数表示我们也要覆盖目标数据库中的角色。

## 主模型处理

如果你有专用的处理服务器，并且各个独立模型之间有大量数据重叠，那么可以先把数据处理到主模型中，再进行拆分。 这样可以避免对相同数据在各个独立模型中重复处理多次。 **不过，这里有个前提：不要处理那些在不同版本之间分区查询发生过变更的表，如同[本节](/xref:Master-model-pattern#altering-partition-queries)所示。** 对应的做法如下：

1. （可选：如元数据有变更）将主模型部署到处理服务器
2. 对主模型执行所需的处理（不要处理包含特定版本分区查询的表）。
3. 将主模型同步到每个独立模型中，并在同步后使用上面的命令精简独立模型；如有需要，再执行一次 ProcessRecalc。
4. （可选）对各个独立模型中包含特定版本分区查询的表进行处理。

## 技巧与窍门

当你开始大量使用自定义注释时，可能会遇到想列出所有带有某个特定注释的对象的情况。 这时，筛选框中的 Dynamic LINQ 表达式就派上用场了。

首先，假设我们想找出所有添加了名为 "$InternetModel_Expression" 的注释的对象。 在筛选文本框中输入以下内容，然后按下 ENTER 键：

```
:GetAnnotation("$InternetModel_Expression")<>null
```

或者，如果你想找出所有注释名以“_Expression”结尾的对象，请使用：

```
:GetAnnotations().Any(EndsWith("_Expression"))
```

注意，这些函数区分大小写。因此，如果你的注释是用小写写的，上面的筛选条件就匹配不到。

你也可以查找注释具有特定值的对象：

```
:GetAnnotation("$InternetModel_Description").Contains("TODO")
```

## 结论

当你需要维护许多相似且共享大量功能的模型，例如日历表和其他常见维度时，这里介绍的技巧会非常有帮助。 这些脚本可以在 Tabular Editor 中作为自定义操作 Custom Actions 方便地复用；而实际部署也可以通过多种方式实现自动化。
