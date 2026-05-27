---
uid: how-to-tom-interfaces
title: 关键 TOM 接口
author: Morten Lønskov
updated: 2026-04-10
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 关键 TOM 接口

TOMWrapper 封装器定义了若干跨领域接口，可由多种对象类型实现。 在编写对具备特定能力的任意对象执行操作的通用代码时(例如设置描述、检查可见性或读取注释)，可以使用这些接口。

## 快速参考

```csharp
// Set description on any object that supports it
foreach (var obj in Selected.OfType<IDescriptionObject>())
    obj.Description = "Reviewed";

// Hide any hideable object
foreach (var obj in Selected.OfType<IHideableObject>())
    obj.IsHidden = true;

// Read annotations on any annotatable object
foreach (var obj in Model.AllMeasures.OfType<IAnnotationObject>())
    if (obj.HasAnnotation("Status")) Info(obj.GetAnnotation("Status"));
```

## 接口参考

| 界面                                                                                                                           | 关键成员                                                                                               | 由以下对象实现                      |
| ---------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | ---------------------------- |
| (xref:TabularEditor.TOMWrapper.IDescriptionObject)        | `Description`                                                                                      | 表、列、度量值、层次结构、分区、关系、透视、角色、数据源 |
| (xref:TabularEditor.TOMWrapper.IHideableObject)           | `IsHidden`、`IsVisible`                                                                             | 表、列、度量值、层次结构、级别              |
| (xref:TabularEditor.TOMWrapper.ITabularPerspectiveObject) | `InPerspective` 索引器                                                                                | 表、列、度量值、层次结构                 |
| (xref:TabularEditor.TOMWrapper.ITranslatableObject)       | `TranslatedNames`、`TranslatedDescriptions`                                                         | 表、列、度量值、层次结构、级别              |
| (xref:TabularEditor.TOMWrapper.IFolderObject)             | `DisplayFolder`、`TranslatedDisplayFolders`                                                         | 度量值、列、层次结构                   |
| (xref:TabularEditor.TOMWrapper.IAnnotationObject)         | `GetAnnotation()`, `SetAnnotation()`, `HasAnnotation()`, `RemoveAnnotation()`, `Annotations`       | 几乎所有 TOM 对象                  |
| (xref:TabularEditor.TOMWrapper.IExtendedPropertyObject)   | `GetExtendedProperty()`, `SetExtendedProperty()`, `ExtendedProperties`                             | 表、列、度量值、层次结构、分区              |
| (xref:TabularEditor.TOMWrapper.IExpressionObject)         | `Expression` (TE2)；`GetExpression()`、`SetExpression()` (TE3) | 度量值、计算列、计算项、分区、KPI           |
| (xref:TabularEditor.TOMWrapper.IDaxObject)                | `DaxObjectName`、`DaxObjectFullName`、`ReferencedBy`                                                 | 表、列、度量值                      |
| (xref:TabularEditor.TOMWrapper.IDaxDependantObject)       | `DependsOn`                                                                                        | 度量值、计算列、计算项、KPI、表、分区         |

## 何时使用接口

当你需要编写适用于多种对象类型的通用代码时，应使用接口。 与其逐个检查每种类型，不如这样：

```csharp
// Without interfaces -- repetitive
foreach (var m in Selected.Measures)
    m.Description = "Reviewed";
foreach (var c in Selected.Columns)
    c.Description = "Reviewed";
foreach (var t in Selected.Tables)
    t.Description = "Reviewed";
```

使用接口配合 `OfType<T>()`，即可一次性处理所有类型：

```csharp
// With interfaces -- handles any object that has a Description
foreach (var obj in Selected.OfType<IDescriptionObject>())
    obj.Description = "Reviewed";
```

## 常见接口模式

### 检查并设置可见性

```csharp
// Hide all selected objects that support hiding
Selected.OfType<IHideableObject>().ForEach(obj => obj.IsHidden = true);
```

### 为不同类型设置显示文件夹

```csharp
// Move all selected folder-bearing objects to a display folder
Selected.OfType<IFolderObject>().ForEach(obj => obj.DisplayFolder = "Archive");
```

### 用注释给对象打标签

```csharp
// Tag any annotatable object
Selected.OfType<IAnnotationObject>().ForEach(obj =>
    obj.SetAnnotation("ReviewDate", DateTime.Today.ToString("yyyy-MM-dd")));
```

### 查找所有包含 DAX 表达式的对象

```csharp
// List all objects that have a DAX expression and depend on a specific table
var dependents = Model.AllMeasures.Cast<IDaxDependantObject>()
    .Concat(Model.AllColumns.OfType<CalculatedColumn>().Cast<IDaxDependantObject>())
    .Where(obj => obj.DependsOn.Tables.Any(t => t.Name == "Date"));
```

## 另见

- @how-to-check-object-types
- @how-to-filter-query-objects-linq
- @how-to-annotations-extended-properties
- @how-to-work-with-dependencies
