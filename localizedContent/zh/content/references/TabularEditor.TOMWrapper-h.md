# TabularEditor.TOMWrapper 参考文档

这是为 TOMWrapper API 自动生成的文档。 使用 CTRL+F 或右侧的侧边栏，定位特定的类、属性或方法。

## `AddObjectType`

```csharp
public enum TabularEditor.TOMWrapper.AddObjectType
    : Enum, IComparable, IFormattable, IConvertible

```

枚举

| 值   | 名称   | 摘要 |
| --- | ---- | -- |
| `1` | 度量值  |    |
| `2` | 计算列  |    |
| `3` | 层次结构 |    |

## `CalculatedColumn`

CalculatedColumn 的基类声明

```csharp
public class TabularEditor.TOMWrapper.CalculatedColumn
    : Column, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IErrorMessageObject, IDescriptionObject, IAnnotationObject, ITabularPerspectiveObject, IDaxObject, IExpressionObject

```

属性

| 类型                                         | 名称                 | 摘要                                             |
| ------------------------------------------ | ------------------ | ---------------------------------------------- |
| `Dictionary<IDaxObject, List<Dependency>>` | 依赖项                |                                                |
| `String`                                   | 表达式                | 获取或设置 CalculatedColumn 的 Expression 值。         |
| `Boolean`                                  | IsDataTypeInferred | 获取或设置 CalculatedColumn 的 IsDataTypeInferred 值。 |
| `CalculatedColumn`                         | MetadataObject     |                                                |
| `Boolean`                                  | NeedsValidation    |                                                |

方法

| 类型                   | 名称                                                                                                       | 摘要 |
| -------------------- | -------------------------------------------------------------------------------------------------------- | -- |
| `TabularNamedObject` | Clone(`String` newName = null, `Boolean` includeTranslations = True)                  |    |
| `TabularNamedObject` | CloneTo(`Table` table, `String` newName = null, `Boolean` includeTranslations = True) |    |
| `void`               | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue)        |    |

## `CalculatedTable`

```csharp
public class TabularEditor.TOMWrapper.CalculatedTable
    : Table, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IHideableObject, IDescriptionObject, IAnnotationObject, ITabularObjectContainer, IDetailObjectContainer, ITabularPerspectiveObject, IDaxObject, IDynamicPropertyObject, IErrorMessageObject, IExpressionObject

```

属性

| 类型                                         | 名称              | 摘要 |
| ------------------------------------------ | --------------- | -- |
| `Dictionary<IDaxObject, List<Dependency>>` | 依赖项             |    |
| `String`                                   | 表达式             |    |
| `Boolean`                                  | NeedsValidation |    |
| `String`                                   | ObjectTypeName  |    |

方法

| 类型        | 名称                                                                                                | 摘要                                       |
| --------- | ------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| `void`    | CheckChildrenErrors()                                                          |                                          |
| `Boolean` | Editable(`String` propertyName)                                                |                                          |
| `void`    | Init()                                                                         |                                          |
| `void`    | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue) |                                          |
| `void`    | ReinitColumns()                                                                | 在模型保存到 DB 后调用此方法，以检查是否有列发生更改（例如表达式发生更改时） |

## `CalculatedTableColumn`

`CalculatedTableColumn` 的基类定义

```csharp
public class TabularEditor.TOMWrapper.CalculatedTableColumn
    : Column, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IErrorMessageObject, IDescriptionObject, IAnnotationObject, ITabularPerspectiveObject, IDaxObject

```

属性

| 类型                      | 名称                 | 摘要                                                |
| ----------------------- | ------------------ | ------------------------------------------------- |
| `Column`                | ColumnOrigin       | 获取或设置 CalculatedTableColumn 的 ColumnOrigin。       |
| `Boolean`               | IsDataTypeInferred | 获取或设置 CalculatedTableColumn 的 IsDataTypeInferred。 |
| `Boolean`               | IsNameInferred     | 获取或设置 CalculatedTableColumn 的 IsNameInferred。     |
| `CalculatedTableColumn` | MetadataObject     |                                                   |
| `String`                | SourceColumn       | 获取或设置 CalculatedTableColumn 的 SourceColumn。       |

## `Column`

Column 的基类声明

```csharp
public abstract class TabularEditor.TOMWrapper.Column
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IErrorMessageObject, IDescriptionObject, IAnnotationObject, ITabularPerspectiveObject, IDaxObject

```

属性

| 类型                           | 名称                                              | 摘要                              |
| ---------------------------- | ----------------------------------------------- | ------------------------------- |
| `Alignment`                  | Alignment                                       | 获取或设置列的 Alignment 属性。           |
| `String`                     | DataCategory                                    | 获取或设置列的 DataCategory 属性。        |
| `DataType`                   | DataType                                        | 获取或设置列的 DataType 属性。            |
| `String`                     | DaxObjectFullName                               |                                 |
| `String`                     | DaxObjectName                                   |                                 |
| `String`                     | DaxTableName                                    |                                 |
| `HashSet<IExpressionObject>` | Dependants                                      |                                 |
| `String`                     | Description                                     | 获取或设置列的 Description 属性。         |
| `String`                     | DisplayFolder                                   | 获取或设置列的 DisplayFolder 属性。       |
| `Int32`                      | DisplayOrdinal                                  | 获取或设置列的 DisplayOrdinal 属性。      |
| `String`                     | ErrorMessage                                    | 获取或设置列的 ErrorMessage 属性。        |
| `String`                     | FormatString                                    | 获取或设置列的 FormatString 属性。        |
| `透视索引器`                      | 在透视中                                            |                                 |
| `Boolean`                    | IsAvailableInMDX                                | 获取或设置列的 IsAvailableInMDX 属性。    |
| `Boolean`                    | IsDefaultImage                                  | 获取或设置列的 IsDefaultImage 属性。      |
| `Boolean`                    | IsDefaultLabel                                  | 获取或设置列的 IsDefaultLabel 属性。      |
| `Boolean`                    | IsHidden                                        | 获取或设置列的 IsHidden 属性。            |
| `Boolean`                    | IsKey                                           | 获取或设置列的 IsKey 属性。               |
| `Boolean`                    | IsNullable                                      | 获取或设置该列的 IsNullable 属性。         |
| `Boolean`                    | IsUnique                                        | 获取或设置该列的 IsUnique 属性。           |
| `Boolean`                    | KeepUniqueRows                                  | 获取或设置该列的 KeepUniqueRows 属性。     |
| `Column`                     | MetadataObject                                  |                                 |
| `Column`                     | SortByColumn                                    | 获取或设置该列的 SortByColumn 属性。       |
| `String`                     | SourceProviderType                              | 获取或设置该列的 SourceProviderType 属性。 |
| `ObjectState`                | State                                           | 获取或设置该列的 State 属性。              |
| `AggregateFunction`          | SummarizeBy                                     | 获取或设置该列的 SummarizeBy 属性。        |
| `Table`                      | Table                                           |                                 |
| `Int32`                      | TableDetailPosition                             | 获取或设置列的 TableDetailPosition。    |
| `TranslationIndexer`         | TranslatedDescriptions                          | 此列的本地化说明集合。                     |
| `TranslationIndexer`         | TranslatedDisplayFolders                        | 此列的本地化显示文件夹集合。                  |
| `ColumnType`                 | Type                                            | 获取或设置该列的 Type。                  |
| `IEnumerable<Hierarchy>`     | UsedInHierarchies<a id="used-in-hierarchy"></a> | 枚举所有将此列用作级别的层次结构。               |
| `IEnumerable<Relationship>`  | UsedInRelationships                             | 枚举此列参与的所有关系（可作为  或  ）。          |

方法

| 类型       | 名称                                                                                                                      | 摘要 |
| -------- | ----------------------------------------------------------------------------------------------------------------------- | -- |
| `void`   | Delete()                                                                                             |    |
| `String` | GetAnnotation(`String` name)                                                                         |    |
| `void`   | Init()                                                                                               |    |
| `void`   | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue)                       |    |
| `void`   | OnPropertyChanging(`String` propertyName, `Object` newValue, `Boolean&` undoable, `Boolean&` cancel) |    |
| `void`   | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True)                              |    |
| `void`   | Undelete(`ITabularObjectCollection` collection)                                                      |    |

## `ColumnCollection`

Column 的集合类。 提供便捷属性，可一次为多个对象设置同一属性。

```csharp
public class TabularEditor.TOMWrapper.ColumnCollection
    : TabularObjectCollection<Column, Column, Table>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Column>, IEnumerable<Column>, IList<Column>, ITabularObjectCollection, IExpandableIndexer

```

属性

| 类型                  | 名称                  | 摘要 |
| ------------------- | ------------------- | -- |
| `Alignment`         | Alignment           |    |
| `String`            | DataCategory        |    |
| `DataType`          | DataType            |    |
| `String`            | 描述                  |    |
| `String`            | DisplayFolder       |    |
| `Int32`             | DisplayOrdinal      |    |
| `String`            | FormatString        |    |
| `Boolean`           | IsAvailableInMDX    |    |
| `Boolean`           | IsDefaultImage      |    |
| `Boolean`           | IsDefaultLabel      |    |
| `Boolean`           | IsHidden            |    |
| `Boolean`           | IsKey               |    |
| `Boolean`           | IsNullable          |    |
| `Boolean`           | IsUnique            |    |
| `Boolean`           | KeepUniqueRows      |    |
| `Table`             | 父对象                 |    |
| `Column`            | SortByColumn        |    |
| `String`            | SourceProviderType  |    |
| `AggregateFunction` | SummarizeBy         |    |
| `Int32`             | TableDetailPosition |    |

方法

| 类型                    | 名称                                 | 摘要 |
| --------------------- | ---------------------------------- | -- |
| `IEnumerator<Column>` | GetEnumerator() |    |
| `String`              | ToString()      |    |

## `区域设置`

`区域设置` 的基类声明

```csharp
public class TabularEditor.TOMWrapper.Culture
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IAnnotationObject, IDynamicPropertyObject

```

属性

| 类型                            | 名称          | 摘要 |
| ----------------------------- | ----------- | -- |
| `String`                      | 显示名称        |    |
| `区域设置`                        | 元数据对象       |    |
| `String`                      | 名称          |    |
| `ObjectTranslationCollection` | 对象翻译        |    |
| `String`                      | 统计列标题       |    |
| `String`                      | 统计列显示文件夹    |    |
| `String`                      | 统计层次结构标题    |    |
| `String`                      | 统计层次结构显示文件夹 |    |
| `String`                      | 统计级别标题      |    |
| `String`                      | 统计度量值标题     |    |
| `String`                      | 统计度量值显示文件夹  |    |
| `String`                      | 统计表标题       |    |
| `Boolean`                     | 未分配         |    |

方法

| 类型                   | 名称                                                                                                | 摘要 |
| -------------------- | ------------------------------------------------------------------------------------------------- | -- |
| `Boolean`            | Browsable(`String` propertyName)                                               |    |
| `TabularNamedObject` | Clone(`String` newName, `Boolean` includeTranslations)                         |    |
| `Boolean`            | Editable(`String` propertyName)                                                |    |
| `String`             | GetAnnotation(`String` name)                                                   |    |
| `void`               | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue) |    |
| `void`               | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True)        |    |
| `void`               | Undelete(`ITabularObjectCollection` collection)                                |    |

## `区域设置集合`

区域设置的集合类。 提供便捷的属性，可一次性在多个对象上设置同一属性。

```csharp
public class TabularEditor.TOMWrapper.CultureCollection
    : TabularObjectCollection<Culture, Culture, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Culture>, IEnumerable<Culture>, IList<Culture>, ITabularObjectCollection, IExpandableIndexer

```

属性

| 类型      | 名称 | 摘要 |
| ------- | -- | -- |
| `Model` | 父级 |    |

方法

| 类型       | 名称                            | 摘要 |
| -------- | ----------------------------- | -- |
| `String` | ToString() |    |

## `区域设置转换器`

```csharp
public class TabularEditor.TOMWrapper.区域设置转换器
    : TypeConverter

```

方法

| 类型                         | 名称                                                                                                                         | 摘要 |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------- | -- |
| `Boolean`                  | CanConvertFrom(`ITypeDescriptorContext` context, `Type` sourceType)                                     |    |
| `Boolean`                  | CanConvertTo(`ITypeDescriptorContext` context, `Type` destinationType)                                  |    |
| `Object`                   | ConvertFrom(`ITypeDescriptorContext` context, `CultureInfo` 区域设置, `Object` value)                       |    |
| `Object`                   | ConvertTo(`ITypeDescriptorContext` context, `CultureInfo` 区域设置, `Object` value, `Type` destinationType) |    |
| `StandardValuesCollection` | GetStandardValues(`ITypeDescriptorContext` context)                                                     |    |
| `Boolean`                  | GetStandardValuesExclusive(`ITypeDescriptorContext` context)                                            |    |
| `Boolean`                  | GetStandardValuesSupported(`ITypeDescriptorContext` context)                                            |    |

## `Database`

```csharp
public class TabularEditor.TOMWrapper.Database

```

属性

| 类型                   | 名称                 | 摘要 |
| -------------------- | ------------------ | -- |
| `Nullable<Int32>`    | CompatibilityLevel |    |
| `Nullable<DateTime>` | CreatedTimestamp   |    |
| `String`             | ID                 |    |
| `Nullable<DateTime>` | LastProcessed      |    |
| `Nullable<DateTime>` | LastSchemaUpdate   |    |
| `Nullable<DateTime>` | LastUpdate         |    |
| `String`             | 名称                 |    |
| `String`             | ServerName         |    |
| `String`             | ServerVersion      |    |
| `Database`           | TOMDatabase        |    |
| `Nullable<Int64>`    | Version            |    |

方法

| 类型       | 名称                            | 摘要 |
| -------- | ----------------------------- | -- |
| `String` | ToString() |    |

## `DataColumn`

DataColumn 的基类定义

```csharp
public class TabularEditor.TOMWrapper.DataColumn
    : Column, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IErrorMessageObject, IDescriptionObject, IAnnotationObject, ITabularPerspectiveObject, IDaxObject

```

属性

| 类型           | 名称             | 摘要                               |
| ------------ | -------------- | -------------------------------- |
| `DataColumn` | MetadataObject |                                  |
| `String`     | SourceColumn   | 获取或设置 DataColumn 的 SourceColumn。 |

## `DataSource`

DataSource 的基类声明

```csharp
public abstract class TabularEditor.TOMWrapper.DataSource
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject

```

属性

| 类型                   | 名称                     | 摘要                                 |
| -------------------- | ---------------------- | ---------------------------------- |
| `String`             | Description            | 获取或设置 DataSource 的 Description 属性。 |
| `DataSource`         | MetadataObject         |                                    |
| `TranslationIndexer` | TranslatedDescriptions | 此 DataSource 的本地化描述集合。             |
| `DataSourceType`     | Type                   | 获取或设置 DataSource 的 Type 属性。        |

方法

| 类型       | 名称                                                                                         | 摘要 |
| -------- | ------------------------------------------------------------------------------------------ | -- |
| `String` | GetAnnotation(`String` name)                                            |    |
| `void`   | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |    |

## `DataSourceCollection`

用于 DataSource 的集合类。 提供便捷的属性，可一次性在多个对象上设置同一属性。

```csharp
public class TabularEditor.TOMWrapper.DataSourceCollection
    : TabularObjectCollection<DataSource, DataSource, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<DataSource>, IEnumerable<DataSource>, IList<DataSource>, ITabularObjectCollection, IExpandableIndexer

```

属性

| 类型       | 名称 | 摘要 |
| -------- | -- | -- |
| `String` | 描述 |    |
| `Model`  | 父级 |    |

方法

| 类型       | 名称                            | 摘要 |
| -------- | ----------------------------- | -- |
| `String` | ToString() |    |

## `Dependency`

```csharp
public struct TabularEditor.TOMWrapper.Dependency

```

字段

| 类型        | 名称             | 摘要 |
| --------- | -------------- | -- |
| `Int32`   | 从              |    |
| `Boolean` | fullyQualified |    |
| `Int32`   | 到              |    |

## `DependencyHelper`

```csharp
public static class TabularEditor.TOMWrapper.DependencyHelper

```

静态方法

| 类型       | 名称                                                                                                                                             | 摘要                                                                           |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `void`   | AddDep(this `IExpressionObject` target, `IDaxObject` dependsOn, `Int32` fromChar, `Int32` toChar, `Boolean` fullyQualified) |                                                                              |
| `String` | NoQ(this `String` objectName, `Boolean` table = False)                                                                      | 移除名称周围的限定符，例如 ' ' 和 [ ]。 |

## `DeploymentMode`

```csharp
public enum TabularEditor.TOMWrapper.DeploymentMode
    : Enum, IComparable, IFormattable, IConvertible

```

枚举

| 值   | 名称             | 摘要 |
| --- | -------------- | -- |
| `0` | CreateDatabase |    |
| `1` | CreateOrAlter  |    |

## `DeploymentOptions`

```csharp
public class TabularEditor.TOMWrapper.DeploymentOptions

```

字段

| 类型               | 名称                | 摘要 |
| ---------------- | ----------------- | -- |
| `Boolean`        | DeployConnections |    |
| `DeploymentMode` | DeployMode        |    |
| `Boolean`        | 部署分区              |    |
| `Boolean`        | 部署角色成员            |    |
| `Boolean`        | 部署角色              |    |

静态字段

| 类型                  | 名称      | 摘要 |
| ------------------- | ------- | -- |
| `DeploymentOptions` | Default |    |
| `DeploymentOptions` | 仅包含结构   |    |

## `DeploymentResult`

```csharp
public class TabularEditor.TOMWrapper.DeploymentResult

```

字段

| 类型                      | 名称 | 摘要 |
| ----------------------- | -- | -- |
| `IReadOnlyList<String>` | 问题 |    |
| `IReadOnlyList<String>` | 警告 |    |

## `DeploymentStatus`

```csharp
public enum TabularEditor.TOMWrapper.DeploymentStatus
    : Enum, IComparable, IFormattable, IConvertible

```

枚举

| 值   | 名称              | 摘要 |
| --- | --------------- | -- |
| `0` | ChangesSaved    |    |
| `1` | DeployComplete  |    |
| `2` | DeployCancelled |    |

## `Folder`

表示 TreeView 中的文件夹。 与 TOM 中的任何对象都不对应。  实现 IDisplayFolderObject，因为文件夹本身也可能位于另一个显示文件夹中。  实现 IParentObject，因为文件夹可以包含子对象。

```csharp
public class TabularEditor.TOMWrapper.Folder
    : IDetailObject, ITabularTableObject, ITabularNamedObject, ITabularObject, INotifyPropertyChanged, ITabularObjectContainer, IDetailObjectContainer, IErrorMessageObject

```

属性

| 类型                       | 名称                       | 摘要 |
| ------------------------ | ------------------------ | -- |
| `IDetailObjectContainer` | Container                |    |
| `区域设置`                   | 区域设置                     |    |
| `String`                 | DisplayFolder            |    |
| `String`                 | ErrorMessage             |    |
| `String`                 | FullPath                 |    |
| `TabularModelHandler`    | Handler                  |    |
| `Int32`                  | MetadataIndex            |    |
| `Model`                  | Model                    |    |
| `String`                 | 名称                       |    |
| `ObjectType`             | ObjectType               |    |
| `Table`                  | ParentTable              |    |
| `String`                 | Path                     |    |
| `Table`                  | Table                    |    |
| `TranslationIndexer`     | TranslatedDisplayFolders |    |
| `TranslationIndexer`     | TranslatedNames          |    |

事件

| 类型                            | 名称              | 摘要 |
| ----------------------------- | --------------- | -- |
| `PropertyChangedEventHandler` | PropertyChanged |    |

方法

| 类型                                 | 名称                                                                   | 摘要                                                      |
| ---------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------- |
| `void`                             | CheckChildrenErrors()                             |                                                         |
| `void`                             | Delete()                                          | 删除文件夹不会删除其中的子对象，只会移除该文件夹。  任何子文件夹都会保留（但会在“显示文件夹”层级中上移）。 |
| `IEnumerable<ITabularNamedObject>` | GetChildren()                                     |                                                         |
| `IEnumerable<IDetailObject>`       | GetChildrenByFolders(`Boolean` recursive = False) |                                                         |
| `void`                             | SetFolderName(`String` newName)                   |                                                         |
| `void`                             | UndoSetPath(`String` value)                       |                                                         |

静态方法

| 类型       | 名称                                                                                                                              | 摘要 |
| -------- | ------------------------------------------------------------------------------------------------------------------------------- | -- |
| `Folder` | CreateFolder(`Table` table, `String` path = , `Boolean` useFixedCulture = False, `区域设置` fixedCulture = null) |    |

## `FolderHelper`

```csharp
public static class TabularEditor.TOMWrapper.FolderHelper

```

静态方法

| 类型                       | 名称                                                                                                             | 摘要 |
| ------------------------ | -------------------------------------------------------------------------------------------------------------- | -- |
| `String`                 | ConcatPath(this `String` path, `String` additionalPath)                                     |    |
| `String`                 | ConcatPath(this `IEnumerable<String>` pathBits)                                             |    |
| `IDetailObjectContainer` | GetContainer(this `IDetailObject` obj)                                                      |    |
| `String`                 | GetDisplayFolder(this `IDetailObject` folderObject, `区域设置` culture)                         |    |
| `String`                 | GetFullPath(`ITabularNamedObject` obj)                                                      |    |
| `Boolean`                | HasAncestor(this `IDetailObject` child, `ITabularNamedObject` ancestor, `区域设置` culture)     |    |
| `Boolean`                | HasParent(this `IDetailObject` child, `ITabularNamedObject` parent, `区域设置` culture)         |    |
| `Int32`                  | Level(this `String` path)                                                                   |    |
| `String`                 | PathFromFullPath(`String` path)                                                             |    |
| `void`                   | SetDisplayFolder(this `IDetailObject` folderObject, `String` newFolderName, `区域设置` culture) |    |
| `String`                 | TrimFolder(this `String` folderPath)                                                        |    |

## `Hierarchy`

Hierarchy 的基类声明

```csharp
public class TabularEditor.TOMWrapper.Hierarchy
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IDescriptionObject, IAnnotationObject, ITabularObjectContainer, ITabularPerspectiveObject

```

属性

| 类型                   | 名称                       | 摘要                              |
| -------------------- | ------------------------ | ------------------------------- |
| `String`             | 说明                       | 获取或设置层次结构的说明。                   |
| `String`             | DisplayFolder            | 获取或设置层次结构的显示文件夹。                |
| `透视索引器`              | 在透视中                     |                                 |
| `Boolean`            | IsHidden                 | 获取或设置层次结构是否隐藏。                  |
| `LevelCollection`    | Levels                   |                                 |
| `Hierarchy`          | MetadataObject           |                                 |
| `Boolean`            | Reordering               | 当需要将多个级别作为一次操作重新排序时，将其设置为 true。 |
| `ObjectState`        | State                    | 获取或设置层次结构的状态。                   |
| `Table`              | 表格                       |                                 |
| `TranslationIndexer` | TranslatedDescriptions   | 此层次结构的本地化描述集合。                  |
| `TranslationIndexer` | TranslatedDisplayFolders | 此层次结构的本地化显示文件夹集合。               |

方法

| 类型                                 | 名称                                                                                                | 摘要 |
| ---------------------------------- | ------------------------------------------------------------------------------------------------- | -- |
| `Level`                            | AddLevel(`Column` column, `String` levelName = null, `Int32` ordinal = -1)     |    |
| `Level`                            | AddLevel(`String` columnName, `String` levelName = null, `Int32` ordinal = -1) |    |
| `void`                             | AddLevels(`IEnumerable<Column>` columns, `Int32` ordinal = -1)                 |    |
| `void`                             | CompactLevelOrdinals()                                                         |    |
| `void`                             | Delete()                                                                       |    |
| `void`                             | FixLevelOrder(`Level` level, `Int32` newOrdinal)                               |    |
| `String`                           | GetAnnotation(`String` name)                                                   |    |
| `IEnumerable<ITabularNamedObject>` | GetChildren()                                                                  |    |
| `void`                             | Init()                                                                         |    |
| `void`                             | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True)        |    |
| `void`                             | SetLevelOrder(`IList<Level>` order)                                            |    |
| `void`                             | Undelete(`ITabularObjectCollection` collection)                                |    |

## `HierarchyCollection`

Hierarchy 的集合类。 提供便捷的属性，可一次为多个对象设置同一属性。

```csharp
public class TabularEditor.TOMWrapper.HierarchyCollection
    : TabularObjectCollection<Hierarchy, Hierarchy, Table>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Hierarchy>, IEnumerable<Hierarchy>, IList<Hierarchy>, ITabularObjectCollection, IExpandableIndexer

```

属性

| 类型        | 名称            | 摘要 |
| --------- | ------------- | -- |
| `String`  | Description   |    |
| `String`  | DisplayFolder |    |
| `Boolean` | IsHidden      |    |
| `Table`   | 父级            |    |

方法

| 类型       | 名称                            | 摘要 |
| -------- | ----------------------------- | -- |
| `String` | ToString() |    |

## `HierarchyColumnConverter`

```csharp
public class TabularEditor.TOMWrapper.HierarchyColumnConverter
    : TableColumnConverter

```

方法

| 类型        | 名称                                                                              | 摘要 |
| --------- | ------------------------------------------------------------------------------- | -- |
| `Boolean` | GetStandardValuesExclusive(`ITypeDescriptorContext` context) |    |
| `Boolean` | IsValid(`ITypeDescriptorContext` context, `Object` value)    |    |

## `IAnnotationObject`

```csharp
public interface TabularEditor.TOMWrapper.IAnnotationObject
    : ITabularObject, INotifyPropertyChanged

```

方法

| 类型       | 名称                                                                                         | 摘要 |
| -------- | ------------------------------------------------------------------------------------------ | -- |
| `String` | GetAnnotation(`String` name)                                            |    |
| `void`   | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |    |

## `IClonableObject`

```csharp
public interface TabularEditor.TOMWrapper.IClonableObject

```

方法

| 类型                   | 名称                                                                        | 摘要 |
| -------------------- | ------------------------------------------------------------------------- | -- |
| `TabularNamedObject` | Clone(`String` newName, `Boolean` includeTranslations) |    |

## `IDaxObject`

```csharp
public interface TabularEditor.TOMWrapper.IDaxObject
    : ITabularNamedObject, ITabularObject, INotifyPropertyChanged

```

属性

| 类型                           | 名称                | 摘要 |
| ---------------------------- | ----------------- | -- |
| `String`                     | DaxObjectFullName |    |
| `String`                     | DaxObjectName     |    |
| `String`                     | DaxTableName      |    |
| `HashSet<IExpressionObject>` | 依赖此对象的项           |    |

## `IDescriptionObject`

可具有描述的对象

```csharp
public interface TabularEditor.TOMWrapper.IDescriptionObject

```

属性

| 类型                   | 名称                     | 摘要 |
| -------------------- | ---------------------- | -- |
| `String`             | Description            |    |
| `TranslationIndexer` | TranslatedDescriptions |    |

## `IDetailObject`

表示可包含在显示文件夹中的对象。 示例：* 度量值
* 列
* 层次结构
* 文件夹

```csharp
public interface TabularEditor.TOMWrapper.IDetailObject
    : ITabularTableObject, ITabularNamedObject, ITabularObject, INotifyPropertyChanged

```

属性

| 类型                   | 名称                       | 摘要 |
| -------------------- | ------------------------ | -- |
| `String`             | DisplayFolder            |    |
| `TranslationIndexer` | TranslatedDisplayFolders |    |

## `IDetailObjectContainer`

表示既可包含其他对象，也可包含显示文件夹的对象。 示例：  - 文件夹  - 表

```csharp
public interface TabularEditor.TOMWrapper.IDetailObjectContainer
    : ITabularNamedObject, ITabularObject, INotifyPropertyChanged

```

属性

| 类型      | 名称          | 摘要 |
| ------- | ----------- | -- |
| `Table` | ParentTable |    |

方法

| 类型                           | 名称                                                                   | 摘要 |
| ---------------------------- | -------------------------------------------------------------------- | -- |
| `IEnumerable<IDetailObject>` | GetChildrenByFolders(`Boolean` recursive = False) |    |

## `IErrorMessageObject`

可包含错误信息的对象

```csharp
public interface TabularEditor.TOMWrapper.IErrorMessageObject

```

属性

| 类型       | 名称           | 摘要 |
| -------- | ------------ | -- |
| `String` | ErrorMessage |    |

## `IExpressionObject`

```csharp
public interface TabularEditor.TOMWrapper.IExpressionObject
    : IDaxObject, ITabularNamedObject, ITabularObject, INotifyPropertyChanged

```

属性

| 类型                                         | 名称              | 摘要 |
| ------------------------------------------ | --------------- | -- |
| `Dictionary<IDaxObject, List<Dependency>>` | 依赖项             |    |
| `String`                                   | 表达式             |    |
| `Boolean`                                  | NeedsValidation |    |

## `IHideableObject`

可显示或隐藏的对象

```csharp
public interface TabularEditor.TOMWrapper.IHideableObject

```

属性

| 类型        | 名称       | 摘要 |
| --------- | -------- | -- |
| `Boolean` | IsHidden |    |

## `IntelliSenseAttribute`

```csharp
public class TabularEditor.TOMWrapper.IntelliSenseAttribute
    : Attribute, _Attribute

```

属性

| 类型       | 名称 | 摘要 |
| -------- | -- | -- |
| `String` | 说明 |    |

## `ITabularNamedObject`

```csharp
public interface TabularEditor.TOMWrapper.ITabularNamedObject
    : ITabularObject, INotifyPropertyChanged

```

属性

| 类型                   | 名称              | 摘要 |
| -------------------- | --------------- | -- |
| `Int32`              | MetadataIndex   |    |
| `String`             | 名称              |    |
| `TranslationIndexer` | TranslatedNames |    |

## `ITabularObject`

```csharp
public interface TabularEditor.TOMWrapper.ITabularObject
    : INotifyPropertyChanged

```

属性

| 类型           | 名称         | 摘要 |
| ------------ | ---------- | -- |
| `Model`      | Model      |    |
| `ObjectType` | ObjectType |    |

## `ITabularObjectCollection`

```csharp
public interface TabularEditor.TOMWrapper.ITabularObjectCollection
    : IEnumerable

```

属性

| 类型                    | 名称             | 摘要 |
| --------------------- | -------------- | -- |
| `String`              | CollectionName |    |
| `TabularModelHandler` | Handler        |    |
| `IEnumerable<String>` | Keys           |    |

方法

| 类型                         | 名称                                                   | 摘要 |
| -------------------------- | ---------------------------------------------------- | -- |
| `void`                     | Add(`TabularNamedObject` obj)     |    |
| `void`                     | Clear()                           |    |
| `Boolean`                  | Contains(`Object` value)          |    |
| `Boolean`                  | Contains(`String` key)            |    |
| `ITabularObjectCollection` | GetCurrentCollection()            |    |
| `Int32`                    | IndexOf(`TabularNamedObject` obj) |    |
| `void`                     | Remove(`TabularNamedObject` obj)  |    |

## `ITabularObjectContainer`

可包含其他对象的 TabularObject 应实现此接口。

```csharp
public interface TabularEditor.TOMWrapper.ITabularObjectContainer

```

方法

| 类型                                 | 名称                               | 摘要 |
| ---------------------------------- | -------------------------------- | -- |
| `IEnumerable<ITabularNamedObject>` | GetChildren() |    |

## `ITabularPerspectiveObject`

可在各个透视中显示或隐藏的对象

```csharp
public interface TabularEditor.TOMWrapper.ITabularPerspectiveObject
    : IHideableObject

```

属性

| 类型                   | 名称            | 摘要 |
| -------------------- | ------------- | -- |
| `PerspectiveIndexer` | InPerspective |    |

## `ITabularTableObject`

属于特定表的对象。

```csharp
public interface TabularEditor.TOMWrapper.ITabularTableObject
    : ITabularNamedObject, ITabularObject, INotifyPropertyChanged

```

属性

| 类型      | 名称    | 摘要 |
| ------- | ----- | -- |
| `Table` | Table |    |

方法

| 类型     | 名称                          | 摘要 |
| ------ | --------------------------- | -- |
| `void` | Delete() |    |

## `KPI`

KPI 的基类声明

```csharp
public class TabularEditor.TOMWrapper.KPI
    : TabularObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, IDescriptionObject, IAnnotationObject, IDynamicPropertyObject

```

属性

| 类型                   | 名称                     | 摘要                                 |
| -------------------- | ---------------------- | ---------------------------------- |
| `String`             | Description            | 获取或设置 KPI 的描述。                     |
| `度量值`                | 度量值                    | 获取或设置 KPI 的度量值。                    |
| `KPI`                | MetadataObject         |                                    |
| `String`             | StatusDescription      | 获取或设置 KPI 的 StatusDescription 属性。  |
| `String`             | StatusExpression       | 获取或设置 KPI 的 StatusExpression 属性。   |
| `String`             | StatusGraphic          | 获取或设置 KPI 的 StatusGraphic 属性。      |
| `String`             | TargetDescription      | 获取或设置 KPI 的 TargetDescription 属性。  |
| `String`             | TargetExpression       | 获取或设置 KPI 的 TargetExpression 属性。   |
| `String`             | TargetFormatString     | 获取或设置 KPI 的 TargetFormatString 属性。 |
| `TranslationIndexer` | TranslatedDescriptions | 此 KPI 的本地化描述集合。                    |
| `String`             | TrendDescription       | 获取或设置 KPI 的 TrendDescription 属性。   |
| `String`             | TrendExpression        | 获取或设置 KPI 的 TrendExpression。       |
| `String`             | TrendGraphic           | 获取或设置 KPI 的 TrendGraphic。          |

方法

| 类型        | 名称                                                                                         | 摘要 |
| --------- | ------------------------------------------------------------------------------------------ | -- |
| `Boolean` | Browsable(`String` propertyName)                                        |    |
| `Boolean` | Editable(`String` propertyName)                                         |    |
| `String`  | GetAnnotation(`String` name)                                            |    |
| `void`    | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |    |

## Level

Level 的基类声明

```csharp
public class TabularEditor.TOMWrapper.Level
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject, ITabularTableObject

```

属性

| 类型                   | 名称    | 摘要           |
| -------------------- | ----- | ------------ |
| `Column`             | 列     | 获取或设置该级别的列。  |
| `String`             | 描述    | 获取或设置该级别的描述。 |
| `Hierarchy`          | 层级    | 获取或设置该级别的层级。 |
| `Level`              | 元数据对象 |              |
| `Int32`              | 序号    | 获取或设置该级别的序号。 |
| `Table`              | 表     |              |
| `TranslationIndexer` | 本地化描述 | 此级别的本地化描述集合。 |

方法

| 类型       | 名称                                                                                                                      | 摘要           |
| -------- | ----------------------------------------------------------------------------------------------------------------------- | ------------ |
| `void`   | Delete()                                                                                             | 从层次结构中删除该级别。 |
| `String` | GetAnnotation(`String` name)                                                                         |              |
| `void`   | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue)                       |              |
| `void`   | OnPropertyChanging(`String` propertyName, `Object` newValue, `Boolean&` undoable, `Boolean&` cancel) |              |
| `void`   | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True)                              |              |
| `void`   | Undelete(`ITabularObjectCollection` collection)                                                      |              |

## `LevelCollection`

用于 Level 的集合类。 提供便捷的属性，可在多个对象上一次性设置某项属性。

```csharp
public class TabularEditor.TOMWrapper.LevelCollection
    : TabularObjectCollection<Level, Level, Hierarchy>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Level>, IEnumerable<Level>, IList<Level>, ITabularObjectCollection, IExpandableIndexer

```

属性

| 类型          | 名称 | 摘要 |
| ----------- | -- | -- |
| `String`    | 描述 |    |
| `Hierarchy` | 父级 |    |

方法

| 类型        | 名称                                      | 摘要 |
| --------- | --------------------------------------- | -- |
| `void`    | Add(`Level` item)    |    |
| `Boolean` | Remove(`Level` item) |    |
| `String`  | ToString()           |    |

## `LogicalGroup`

```csharp
public class TabularEditor.TOMWrapper.LogicalGroup
    : ITabularNamedObject, ITabularObject, INotifyPropertyChanged, ITabularObjectContainer

```

属性

| 类型                   | 名称              | 摘要 |
| -------------------- | --------------- | -- |
| `Int32`              | MetadataIndex   |    |
| `Model`              | Model           |    |
| `String`             | 名称              |    |
| `ObjectType`         | ObjectType      |    |
| `TranslationIndexer` | TranslatedNames |    |

事件

| 类型                            | 名称              | 摘要 |
| ----------------------------- | --------------- | -- |
| `PropertyChangedEventHandler` | PropertyChanged |    |

方法

| 类型                                 | 名称                               | 摘要 |
| ---------------------------------- | -------------------------------- | -- |
| `IEnumerable<ITabularNamedObject>` | GetChildren() |    |

## `LogicalTreeOptions`

```csharp
public enum TabularEditor.TOMWrapper.LogicalTreeOptions
    : Enum, IComparable, IFormattable, IConvertible

```

枚举

| 值     | 名称             | 摘要 |
| ----- | -------------- | -- |
| `1`   | DisplayFolders |    |
| `2`   | Columns        |    |
| `4`   | 度量值            |    |
| `8`   | KPI            |    |
| `16`  | 层次结构           |    |
| `32`  | 层级             |    |
| `64`  | 显示隐藏项          |    |
| `128` | 所有对象类型         |    |
| `256` | 显示根节点          |    |
| `447` | 默认             |    |

## `度量值`

度量值的基类声明

```csharp
public class TabularEditor.TOMWrapper.Measure
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IErrorMessageObject, IDescriptionObject, IExpressionObject, IDaxObject, IAnnotationObject, ITabularPerspectiveObject, IDynamicPropertyObject, IClonableObject

```

属性

| 类型                                         | 名称                       | 摘要                             |
| ------------------------------------------ | ------------------------ | ------------------------------ |
| `DataType`                                 | DataType                 | 获取或设置度量值的 DataType 属性。         |
| `String`                                   | DaxObjectFullName        |                                |
| `String`                                   | DaxObjectName            |                                |
| `String`                                   | DaxTableName             |                                |
| `HashSet<IExpressionObject>`               | Dependants               |                                |
| `Dictionary<IDaxObject, List<Dependency>>` | Dependencies             |                                |
| `String`                                   | Description              | 获取或设置该度量值的说明。                  |
| `String`                                   | DisplayFolder            | 获取或设置该度量值的显示文件夹。               |
| `String`                                   | ErrorMessage             | 获取或设置该度量值的错误信息。                |
| `String`                                   | Expression               | 获取或设置该度量值的表达式。                 |
| `String`                                   | FormatString             | 获取或设置该度量值的格式字符串。               |
| `PerspectiveIndexer`                       | InPerspective            |                                |
| `Boolean`                                  | IsHidden                 | 获取或设置该度量值的 IsHidden 属性。        |
| `Boolean`                                  | IsSimpleMeasure          | 获取或设置该度量值的 IsSimpleMeasure 属性。 |
| `KPI`                                      | KPI                      | 获取或设置该度量值的 KPI 属性。             |
| `度量值`                                      | MetadataObject           |                                |
| `Boolean`                                  | NeedsValidation          |                                |
| `ObjectState`                              | State                    | 获取或设置该度量值的 State 属性。           |
| `Table`                                    | Table                    |                                |
| `TranslationIndexer`                       | TranslatedDescriptions   | 此度量值的本地化描述集合。                  |
| `TranslationIndexer`                       | TranslatedDisplayFolders | 此度量值的本地化显示文件夹集合。               |

方法

| 类型                   | 名称                                                                                                                      | 摘要 |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------- | -- |
| `Boolean`            | Browsable(`String` propertyName)                                                                     |    |
| `TabularNamedObject` | Clone(`String` newName = null, `Boolean` includeTranslations = True)                                 |    |
| `TabularNamedObject` | CloneTo(`Table` table, `String` newName = null, `Boolean` includeTranslations = True)                |    |
| `void`               | Delete()                                                                                             |    |
| `Boolean`            | Editable(`String` propertyName)                                                                      |    |
| `String`             | GetAnnotation(`String` name)                                                                         |    |
| `void`               | Init()                                                                                               |    |
| `void`               | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue)                       |    |
| `void`               | OnPropertyChanging(`String` propertyName, `Object` newValue, `Boolean&` undoable, `Boolean&` cancel) |    |
| `void`               | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True)                              |    |
| `void`               | Undelete(`ITabularObjectCollection` collection)                                                      |    |

## `度量值集合`

度量值集合类。 提供便捷属性，可一次性在多个对象上设置同一属性。

```csharp
public class TabularEditor.TOMWrapper.MeasureCollection
    : TabularObjectCollection<Measure, Measure, Table>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Measure>, IEnumerable<Measure>, IList<Measure>, ITabularObjectCollection, IExpandableIndexer
// Measure：度量值

```

属性

| 类型        | 名称       | 摘要 |
| --------- | -------- | -- |
| `String`  | 说明       |    |
| `String`  | 显示文件夹    |    |
| `String`  | 表达式      |    |
| `String`  | 格式字符串    |    |
| `Boolean` | 是否隐藏     |    |
| `Boolean` | 是否为简单度量值 |    |
| `KPI`     | KPI      |    |
| `Table`   | 父级对象     |    |

方法

| 类型       | 名称                            | 摘要 |
| -------- | ----------------------------- | -- |
| `String` | ToString() |    |

## `Model`

Model 的基类声明

```csharp
public class TabularEditor.TOMWrapper.Model
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject, ITabularObjectContainer

```

字段

| 类型             | 名称                        | 摘要 |
| -------------- | ------------------------- | -- |
| `LogicalGroup` | GroupDataSources          |    |
| `LogicalGroup` | GroupPerspectives - 透视分组  |    |
| `LogicalGroup` | GroupRelationships - 关系分组 |    |
| `LogicalGroup` | GroupRoles - 角色分组         |    |
| `LogicalGroup` | GroupTables               |    |
| `LogicalGroup` | GroupTranslations         |    |

属性

| 类型                           | 名称                 | 摘要                           |
| ---------------------------- | ------------------ | ---------------------------- |
| `IEnumerable<Column>`        | 所有列                |                              |
| `IEnumerable<Hierarchy>`     | 所有层次结构             |                              |
| `IEnumerable<Level>`         | 所有级别               |                              |
| `IEnumerable<Measure>` 度量值   | 所有度量值              |                              |
| `String`                     | 排序规则               | 获取或设置模型的排序规则。                |
| `String`                     | 区域设置               | 获取或设置模型的区域设置。                |
| `CultureCollection` 区域设置集合   | 区域设置集合             |                              |
| `Database`                   | 数据库                |                              |
| `DataSourceCollection`       | 数据源集合              |                              |
| `DataViewType`               | DefaultDataView    | 获取或设置模型的 DefaultDataView 属性。 |
| `ModeType`                   | DefaultMode        | 获取或设置模型的 DefaultMode 属性。     |
| `String`                     | Description        | 获取或设置模型的 Description 属性。     |
| `Boolean`                    | HasLocalChanges    | 获取或设置模型的 HasLocalChanges 属性。 |
| `IEnumerable<LogicalGroup>`  | LogicalChildGroups |                              |
| `Model`                      | MetadataObject     |                              |
| `PerspectiveCollection` 透视   | 透视                 |                              |
| `RelationshipCollection2` 关系 | 关系                 |                              |
| `ModelRoleCollection` 角色     | 角色                 |                              |
| `String`                     | StorageLocation    | 获取或设置模型的 StorageLocation 属性。 |
| `TableCollection`            | Tables             |                              |
| `TranslationIndexer`         | 已翻译的描述             | 此模型的本地化描述集合。                 |

方法

| 类型                                 | 名称                                                                                         | 摘要 |
| ---------------------------------- | ------------------------------------------------------------------------------------------ | -- |
| `CalculatedTable`                  | AddCalculatedTable()                                                    |    |
| `透视`                               | Add透视(`String` name = null)                                             |    |
| `单列关系`                             | Add关系()                                                                 |    |
| `模型角色`                             | Add角色(`String` name = null)                                             |    |
| `Table`                            | AddTable()                                                              |    |
| `区域设置`                             | AddTranslation(`String` 区域设置Id)                                         |    |
| `String`                           | GetAnnotation(`String` name)                                            |    |
| `IEnumerable<ITabularNamedObject>` | GetChildren()                                                           |    |
| `void`                             | Init()                                                                  |    |
| `void`                             | LoadChildObjects()                                                      |    |
| `void`                             | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |    |

## `ModelRole`

ModelRole 的基类声明

```csharp
public class TabularEditor.TOMWrapper.ModelRole
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject

```

属性

| 类型                   | 名称                     | 摘要                                 |
| -------------------- | ---------------------- | ---------------------------------- |
| `String`             | 描述                     | 获取或设置 ModelRole 的 Description。     |
| `ModelRole`          | MetadataObject         |                                    |
| `ModelPermission`    | ModelPermission        | 获取或设置 ModelRole 的 ModelPermission。 |
| `RoleRLSIndexer`     | RowLevelSecurity       |                                    |
| `TranslationIndexer` | TranslatedDescriptions | 此 ModelRole 的本地化描述集合。              |

方法

| 类型                   | 名称                                                                                         | 摘要 |
| -------------------- | ------------------------------------------------------------------------------------------ | -- |
| `TabularNamedObject` | Clone(`String` newName, `Boolean` includeTranslations)                  |    |
| `void`               | Delete()                                                                |    |
| `String`             | GetAnnotation(`String` name)                                            |    |
| `void`               | InitRLSIndexer()                                                        |    |
| `void`               | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |    |
| `void`               | Undelete(`ITabularObjectCollection` collection)                         |    |

## `ModelRoleCollection`

ModelRole 的集合类。 提供便捷属性，可一次性为多个对象设置同一属性。

```csharp
public class TabularEditor.TOMWrapper.ModelRoleCollection
    : TabularObjectCollection<ModelRole, ModelRole, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<ModelRole>, IEnumerable<ModelRole>, IList<ModelRole>, ITabularObjectCollection, IExpandableIndexer

```

属性

| 类型                | 名称              | 摘要 |
| ----------------- | --------------- | -- |
| `String`          | 描述              |    |
| `ModelPermission` | ModelPermission |    |
| `Model`           | 父对象             |    |

方法

| 类型       | 名称                            | 摘要 |
| -------- | ----------------------------- | -- |
| `String` | ToString() |    |

## `NullTree`

```csharp
public class TabularEditor.TOMWrapper.NullTree
    : TabularTree, INotifyPropertyChanged

```

方法

| 类型     | 名称                                                                                       | 摘要 |
| ------ | ---------------------------------------------------------------------------------------- | -- |
| `void` | OnNodesChanged(`ITabularObject` nodeItem)                             |    |
| `void` | OnNodesInserted(`ITabularObject` parent, `ITabularObject[]` children) |    |
| `void` | OnNodesRemoved(`ITabularObject` parent, `ITabularObject[]` children)  |    |
| `void` | OnStructureChanged(`ITabularNamedObject` obj = null)                  |    |

## `ObjectOrder`

```csharp
public enum TabularEditor.TOMWrapper.ObjectOrder
    : Enum, IComparable, IFormattable, IConvertible

```

枚举

| 值   | 名称    | 说明 |
| --- | ----- | -- |
| `0` | 按字母顺序 |    |
| `1` | 元数据   |    |

## `ObjectType`

```csharp
public enum TabularEditor.TOMWrapper.ObjectType
    : Enum, IComparable, IFormattable, IConvertible

```

枚举

| 值      | 名称     | 说明 |
| ------ | ------ | -- |
| `-2`   | 组      |    |
| `-1`   | 文件夹    |    |
| `1`    | 模型     |    |
| `2`    | 数据源    |    |
| `3`    | 表      |    |
| `4`    | 列      |    |
| `5`    | 属性层级结构 |    |
| `6`    | 分区     |    |
| `7`    | 关系     |    |
| `8`    | 度量值    |    |
| `9`    | 层次结构   |    |
| `10`   | 级别     |    |
| `11`   | 注释     |    |
| `12`   | KPI    |    |
| `13`   | 区域设置   |    |
| `14`   | 对象翻译   |    |
| `15`   | 语言元数据  |    |
| `29`   | 透视     |    |
| `30`   | 透视表    |    |
| `31`   | 透视列    |    |
| `32`   | 透视层次结构 |    |
| `33`   | 透视度量值  |    |
| `34`   | 角色     |    |
| `35`   | 角色成员资格 |    |
| `36`   | 表权限    |    |
| `1000` | 数据库    |    |

## `分区`

分区的基类声明

```csharp
public class TabularEditor.TOMWrapper.Partition
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDynamicPropertyObject, IErrorMessageObject, ITabularTableObject, IDescriptionObject, IAnnotationObject

```

属性

| 类型                   | 名称             | 摘要                      |
| -------------------- | -------------- | ----------------------- |
| `DataSource`         | DataSource     |                         |
| `DataViewType`       | DataView       | 获取或设置分区的 DataView。      |
| `String`             | Description    | 获取或设置分区的 Description。   |
| `String`             | ErrorMessage   | 获取或设置分区的 ErrorMessage。  |
| `String`             | Expression     |                         |
| `分区`                 | MetadataObject |                         |
| `ModeType`           | Mode           | 获取或设置分区的 Mode。          |
| `String`             | Name           |                         |
| `String`             | Query          |                         |
| `DateTime`           | RefreshedTime  |                         |
| `String`             | Source         |                         |
| `分区源类型`              | 源类型            | 获取或设置分区的 SourceType 属性。 |
| `ObjectState`        | 状态             | 获取或设置分区的状态。             |
| `Table`              | 表              |                         |
| `TranslationIndexer` | 已翻译的描述         | 此分区的本地化描述集合。            |

方法

| 类型        | 名称                                                                                         | 摘要 |
| --------- | ------------------------------------------------------------------------------------------ | -- |
| `Boolean` | Browsable(`String` propertyName)                                        |    |
| `Boolean` | Editable(`String` propertyName)                                         |    |
| `String`  | GetAnnotation(`String` name)                                            |    |
| `void`    | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |    |
| `void`    | Undelete(`ITabularObjectCollection` collection)                         |    |

## `PartitionCollection` 分区集合

分区的集合类。 提供便捷属性，可一次性在多个对象上设置同一属性。

```csharp
public class TabularEditor.TOMWrapper.PartitionCollection
    : TabularObjectCollection<Partition, Partition, Table>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Partition>, IEnumerable<Partition>, IList<Partition>, ITabularObjectCollection, IExpandableIndexer

```

属性

| 类型             | 名称   | 摘要 |
| -------------- | ---- | -- |
| `DataViewType` | 数据视图 |    |
| `String`       | 说明   |    |
| `ModeType`     | 模式   |    |
| `Table`        | 父对象  |    |

方法

| 类型       | 名称                            | 摘要 |
| -------- | ----------------------------- | -- |
| `String` | ToString() |    |

## `透视`

透视的基类声明

```csharp
public class TabularEditor.TOMWrapper.Perspective
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject

```

属性

| 类型                   | 名称                     | 摘要           |
| -------------------- | ---------------------- | ------------ |
| `String`             | 描述                     | 获取或设置此透视的描述。 |
| `透视`                 | MetadataObject         |              |
| `TranslationIndexer` | TranslatedDescriptions | 此透视的本地化描述集合。 |

方法

| 类型                   | 名称                                                                                         | 摘要 |
| -------------------- | ------------------------------------------------------------------------------------------ | -- |
| `TabularNamedObject` | Clone(`String` newName, `Boolean` includeTranslations)                  |    |
| `void`               | Delete()                                                                |    |
| `String`             | GetAnnotation(`String` name)                                            |    |
| `void`               | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |    |
| `void`               | Undelete(`ITabularObjectCollection` collection)                         |    |

## `PerspectiveCollection`

透视的集合类。 提供便捷的属性，用于一次性在多个对象上设置同一个属性。

```csharp
public class TabularEditor.TOMWrapper.PerspectiveCollection
    : TabularObjectCollection<Perspective, Perspective, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Perspective>, IEnumerable<Perspective>, IList<Perspective>, ITabularObjectCollection, IExpandableIndexer

```

属性

| 类型       | 名称   | 摘要 |
| -------- | ---- | -- |
| `String` | 说明   |    |
| `Model`  | 父级对象 |    |

方法

| 类型       | 名称                            | 摘要 |
| -------- | ----------------------------- | -- |
| `String` | ToString() |    |

## `PerspectiveColumnIndexer`

```csharp
public class TabularEditor.TOMWrapper.PerspectiveColumnIndexer
    : PerspectiveIndexer, IEnumerable<Boolean>, IEnumerable, IExpandableIndexer

```

属性

| 类型       | 名称 | 摘要 |
| -------- | -- | -- |
| `Column` | 列  |    |

方法

| 类型     | 名称                                                                                     | 摘要 |
| ------ | -------------------------------------------------------------------------------------- | -- |
| `void` | Refresh()                                                           |    |
| `void` | SetInPerspective(`Perspective` perspective, `Boolean` included)（透视） |    |

## `PerspectiveHierarchyIndexer`

```csharp
public class TabularEditor.TOMWrapper.PerspectiveHierarchyIndexer
    : PerspectiveIndexer, IEnumerable<Boolean>, IEnumerable, IExpandableIndexer

```

属性

| 类型          | 名称        | 摘要 |
| ----------- | --------- | -- |
| `Hierarchy` | Hierarchy |    |

方法

| 类型     | 名称                                                                                     | 摘要 |
| ------ | -------------------------------------------------------------------------------------- | -- |
| `void` | Refresh()                                                           |    |
| `void` | SetInPerspective(`Perspective` perspective, `Boolean` included)（透视） |    |

## `PerspectiveIndexer` 透视索引器

```csharp
public abstract class TabularEditor.TOMWrapper.PerspectiveIndexer
    : IEnumerable<Boolean>, IEnumerable, IExpandableIndexer
// 透视索引器

```

字段

| 类型                   | 名称            | 摘要 |
| -------------------- | ------------- | -- |
| `TabularNamedObject` | TabularObject |    |

属性

| 类型                                 | 名称      | 摘要 |
| ---------------------------------- | ------- | -- |
| `Boolean`                          | Item    |    |
| `Boolean`                          | Item    |    |
| `IEnumerable<String>`              | Keys    |    |
| `Dictionary<Perspective, Boolean>` | 透视映射    |    |
| `String`                           | Summary |    |

方法

| 类型                            | 名称                                                                                       | 摘要            |
| ----------------------------- | ---------------------------------------------------------------------------------------- | ------------- |
| `void`                        | All()                                                                 | 在所有透视中都包含该对象。 |
| `Dictionary<String, Boolean>` | Copy()                                                                |               |
| `void`                        | CopyFrom(`PerspectiveIndexer` source)                                 |               |
| `void`                        | CopyFrom(`IDictionary<String, Boolean>` source)                       |               |
| `String`                      | GetDisplayName(`String` key)                                          |               |
| `IEnumerator<Boolean>`        | GetEnumerator()                                                       |               |
| `void`                        | None()                                                                |               |
| `void`                        | Refresh()                                                             |               |
| `void`                        | 设置为透视：SetInPerspective(`Perspective` perspective, `Boolean` included) |               |

## `PerspectiveMeasureIndexer`

```csharp
public class TabularEditor.TOMWrapper.PerspectiveMeasureIndexer
    : PerspectiveIndexer, IEnumerable<Boolean>, IEnumerable, IExpandableIndexer

```

属性

| 类型    | 名称  | 摘要 |
| ----- | --- | -- |
| `度量值` | 度量值 |    |

方法

| 类型     | 名称                                                                                        | 摘要 |
| ------ | ----------------------------------------------------------------------------------------- | -- |
| `void` | Refresh()                                                              |    |
| `void` | 在透视中设置：SetInPerspective(`Perspective` perspective, `Boolean` included) |    |

## `PerspectiveTableIndexer`

```csharp
public class TabularEditor.TOMWrapper.PerspectiveTableIndexer
    : PerspectiveIndexer, IEnumerable<Boolean>, IEnumerable, IExpandableIndexer

```

属性

| 类型        | 名称    | 摘要 |
| --------- | ----- | -- |
| `Boolean` | Item  |    |
| `Table`   | Table |    |

方法

| 类型     | 名称                                                                        | 摘要 |
| ------ | ------------------------------------------------------------------------- | -- |
| `透视表`  | EnsurePTExists(`透视` perspective)                       |    |
| `void` | Refresh()                                              |    |
| `void` | SetInPerspective(`透视` perspective, `Boolean` included) |    |

## `ProviderDataSource`

ProviderDataSource 的基类声明

```csharp
public class TabularEditor.TOMWrapper.ProviderDataSource
    : DataSource, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject, IDynamicPropertyObject

```

属性

| 类型                    | 名称                | 摘要                                               |
| --------------------- | ----------------- | ------------------------------------------------ |
| `String`              | Account           | 获取或设置 ProviderDataSource 的 Account 属性。           |
| `String`              | ConnectionString  | 获取或设置 ProviderDataSource 的 ConnectionString 属性。  |
| `ImpersonationMode`   | ImpersonationMode | 获取或设置 ProviderDataSource 的 ImpersonationMode 属性。 |
| `DatasourceIsolation` | Isolation         | 获取或设置 ProviderDataSource 的 Isolation 属性。         |
| `Boolean`             | IsPowerBIMashup   |                                                  |
| `String`              | Location          |                                                  |
| `Int32`               | MaxConnections    | 获取或设置 ProviderDataSource 的 MaxConnections 属性。    |
| `ProviderDataSource`  | MetadataObject    |                                                  |
| `String`              | MQuery            |                                                  |
| `String`              | Name              |                                                  |
| `String`              | Password          | 获取或设置 ProviderDataSource 的 Password 属性。          |
| `String`              | Provider          | 获取或设置 ProviderDataSource 的 Provider 属性。          |
| `String`              | SourceID          |                                                  |
| `Int32`               | Timeout           | 获取或设置 ProviderDataSource 的 Timeout 属性。           |

方法

| 类型        | 名称                                                  | 摘要 |
| --------- | --------------------------------------------------- | -- |
| `Boolean` | Browsable(`String` propertyName) |    |
| `Boolean` | Editable(`String` propertyName)  |    |
| `void`    | Init()                           |    |

## `关系`

关系的基类声明

```csharp
public abstract class TabularEditor.TOMWrapper.Relationship
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IAnnotationObject

```

属性

| 类型                             | 名称                         | 摘要                                       |
| ------------------------------ | -------------------------- | ---------------------------------------- |
| `CrossFilteringBehavior`       | CrossFilteringBehavior     | 获取或设置关系的 CrossFilteringBehavior。         |
| `Table`                        | FromTable                  | 获取或设置关系的 FromTable。                      |
| `Boolean`                      | IsActive                   | 获取或设置关系的 IsActive。                       |
| `DateTimeRelationshipBehavior` | JoinOnDateBehavior         | 获取或设置该关系的 JoinOnDateBehavior 属性。         |
| `关系`                           | MetadataObject             |                                          |
| `Boolean`                      | RelyOnReferentialIntegrity | 获取或设置该关系的 RelyOnReferentialIntegrity 属性。 |
| `SecurityFilteringBehavior`    | SecurityFilteringBehavior  | 获取或设置该关系的 SecurityFilteringBehavior 属性。  |
| `ObjectState`                  | State                      | 获取或设置该关系的 State 属性。                      |
| `Table`                        | ToTable                    | 获取或设置该关系的 ToTable 属性。                    |
| `RelationshipType`             | Type                       | 获取或设置该关系的 Type 属性。                       |

方法

| 类型       | 名称                                                                                         | 摘要 |
| -------- | ------------------------------------------------------------------------------------------ | -- |
| `String` | GetAnnotation(`String` name)                                            |    |
| `void`   | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |    |

## `关系集合`

关系集合类。 提供便捷属性，可一次性为多个对象设置同一属性。

```csharp
public class TabularEditor.TOMWrapper.RelationshipCollection
    : TabularObjectCollection<Relationship, Relationship, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Relationship>, IEnumerable<Relationship>, IList<Relationship>, ITabularObjectCollection, IExpandableIndexer

```

属性

| 类型                          | 名称                         | 摘要 |
| --------------------------- | -------------------------- | -- |
| `CrossFilteringBehavior`    | CrossFilteringBehavior     |    |
| `Boolean`                   | IsActive                   |    |
| `DateTime关系行为`              | JoinOnDateBehavior         |    |
| `Model`                     | Parent                     |    |
| `Boolean`                   | RelyOnReferentialIntegrity |    |
| `SecurityFilteringBehavior` | SecurityFilteringBehavior  |    |

方法

| 类型       | 名称                            | 摘要 |
| -------- | ----------------------------- | -- |
| `String` | ToString() |    |

## `RelationshipCollection2`

```csharp
public class TabularEditor.TOMWrapper.RelationshipCollection2
    : TabularObjectCollection<SingleColumnRelationship, Relationship, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<SingleColumnRelationship>, IEnumerable<SingleColumnRelationship>, IList<SingleColumnRelationship>, ITabularObjectCollection, IExpandableIndexer

```

属性

| 类型                             | 名称                         | 摘要 |
| ------------------------------ | -------------------------- | -- |
| `CrossFilteringBehavior`       | CrossFilteringBehavior     |    |
| `Boolean`                      | IsActive                   |    |
| `DateTimeRelationshipBehavior` | JoinOnDateBehavior         |    |
| `Model`                        | Parent                     |    |
| `Boolean`                      | RelyOnReferentialIntegrity |    |
| `SecurityFilteringBehavior`    | SecurityFilteringBehavior  |    |

方法

| 类型       | 名称                            | 摘要 |
| -------- | ----------------------------- | -- |
| `String` | ToString() |    |

## `RoleRLSIndexer`

RoleRLSIndexer 用于针对某一特定角色浏览模型中所有表的全部筛选器。 相比之下，TableRLSIndexer 用于针对某一特定表浏览模型中所有角色的筛选器。

```csharp
public class TabularEditor.TOMWrapper.RoleRLSIndexer
    : IEnumerable<String>, IEnumerable, IExpandableIndexer

```

字段

| 类型          | 名称 | 摘要 |
| ----------- | -- | -- |
| `ModelRole` | 角色 |    |

属性

| 类型                          | 名称     | 摘要 |
| --------------------------- | ------ | -- |
| `String`                    | Item   |    |
| `String`                    | Item   |    |
| `IEnumerable<String>`       | 键      |    |
| `Dictionary<Table, String>` | RLSMap |    |
| `String`                    | 摘要     |    |

方法

| 类型                    | 名称                                                                  | 摘要 |
| --------------------- | ------------------------------------------------------------------- | -- |
| `void`                | Clear()                                          |    |
| `void`                | CopyFrom(`RoleRLSIndexer` source)                |    |
| `String`              | GetDisplayName(`String` key)                     |    |
| `IEnumerator<String>` | GetEnumerator()                                  |    |
| `void`                | Refresh()                                        |    |
| `void`                | SetRLS(`Table` table, `String` filterExpression) |    |

## `SerializeOptions`

```csharp
public class TabularEditor.TOMWrapper.SerializeOptions

```

字段

| 类型                | 名称                       | 摘要 |
| ----------------- | ------------------------ | -- |
| `Boolean`         | IgnoreInferredObjects    |    |
| `Boolean`         | IgnoreInferredProperties |    |
| `Boolean`         | IgnoreTimestamps         |    |
| `HashSet<String>` | Levels                   |    |
| `Boolean`         | PrefixFilenames          |    |
| `Boolean`         | SplitMultilineStrings    |    |

静态属性

| 类型                 | 名称 | 摘要 |
| ------------------ | -- | -- |
| `SerializeOptions` | 默认 |    |

## `SingleColumnRelationship`

SingleColumnRelationship 的基类声明

```csharp
public class TabularEditor.TOMWrapper.SingleColumnRelationship
    : Relationship, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IAnnotationObject, IDynamicPropertyObject

```

属性

| 类型                           | 名称              | 摘要                                                   |
| ---------------------------- | --------------- | ---------------------------------------------------- |
| `RelationshipEndCardinality` | FromCardinality | 获取或设置 SingleColumnRelationship 的 FromCardinality 属性。 |
| `Column`                     | FromColumn      | 获取或设置 SingleColumnRelationship 的 FromColumn 属性。      |
| `SingleColumnRelationship`   | MetadataObject  |                                                      |
| `String`                     | Name            |                                                      |
| `RelationshipEndCardinality` | ToCardinality   | 获取或设置 SingleColumnRelationship 的 ToCardinality 属性。   |
| `Column`                     | ToColumn        | 获取或设置 SingleColumnRelationship 的 ToColumn 属性。        |

方法

| 类型        | 名称                                                                                                                      | 摘要 |
| --------- | ----------------------------------------------------------------------------------------------------------------------- | -- |
| `Boolean` | Browsable(`String` propertyName)                                                                     |    |
| `void`    | Delete()                                                                                             |    |
| `Boolean` | Editable(`String` propertyName)                                                                      |    |
| `void`    | Init()                                                                                               |    |
| `void`    | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue)                       |    |
| `void`    | OnPropertyChanging(`String` propertyName, `Object` newValue, `Boolean&` undoable, `Boolean&` cancel) |    |
| `String`  | ToString()                                                                                           |    |
| `void`    | Undelete(`ITabularObjectCollection` collection)                                                      |    |

## `Table`

Table 的基类声明

```csharp
public class TabularEditor.TOMWrapper.Table
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IHideableObject, IDescriptionObject, IAnnotationObject, ITabularObjectContainer, IDetailObjectContainer, ITabularPerspectiveObject, IDaxObject, IDynamicPropertyObject, IErrorMessageObject

```

属性

| 类型                           | 名称                     | 摘要                          |
| ---------------------------- | ---------------------- | --------------------------- |
| `IEnumerable<Level>`         | AllLevels              |                             |
| `ColumnCollection`           | Columns                |                             |
| `String`                     | DataCategory           | 获取或设置 Table 的 DataCategory。 |
| `String`                     | DaxObjectFullName      |                             |
| `String`                     | DaxObjectName          |                             |
| `String`                     | DaxTableName           |                             |
| `HashSet<IExpressionObject>` | 依赖项                    |                             |
| `String`                     | 描述                     | 获取或设置表的描述。                  |
| `String`                     | 错误消息                   |                             |
| `HierarchyCollection`        | 层次结构                   |                             |
| `透视索引器`                      | 在透视中                   |                             |
| `Boolean`                    | 是否隐藏                   | 获取或设置表是否隐藏。                 |
| `度量值集合`                      | 度量值                    |                             |
| `Table`                      | 元数据对象                  |                             |
| `String`                     | 名称                     |                             |
| `Table`                      | ParentTable            |                             |
| `分区集合`                       | 分区                     |                             |
| `TableRLSIndexer`            | RowLevelSecurity       |                             |
| `String`                     | Source                 |                             |
| `分区源类型`                      | SourceType             |                             |
| `TranslationIndexer`         | TranslatedDescriptions | 此表的本地化描述集合。                 |

方法

| 类型                                 | 名称                                                                                                                        | 摘要                  |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------- |
| `CalculatedColumn`                 | AddCalculatedColumn(`String` name = null, `String` expression = null, `String` displayFolder = null)   |                     |
| `DataColumn`                       | AddDataColumn(`String` name = null, `String` sourceColumn = null, `String` displayFolder = null)       |                     |
| `Hierarchy`                        | AddHierarchy(`String` name = null, `String` displayFolder = null, `Column[]` levels)                   |                     |
| `Hierarchy`                        | AddHierarchy(`String` name, `String` displayFolder = null, `String[]` levels)                          |                     |
| `度量值`                              | AddMeasure(`String` name = null, `String` expression = null, `String` displayFolder = null)            |                     |
| `Boolean`                          | Browsable(`String` propertyName)                                                                       |                     |
| `void`                             | CheckChildrenErrors()                                                                                  |                     |
| `void`                             | Children_CollectionChanged(`Object` sender, `NotifyCollectionChangedEventArgs` e) |                     |
| `TabularNamedObject`               | Clone(`String` newName = null, `Boolean` includeTranslations = False)                                  |                     |
| `void`                             | Delete()                                                                                               |                     |
| `Boolean`                          | Editable(`String` propertyName)                                                                        |                     |
| `String`                           | GetAnnotation(`String` name)                                                                           |                     |
| `IEnumerable<ITabularNamedObject>` | GetChildren()                                                                                          | 返回此表中的所有列、度量值和层次结构。 |
| `IEnumerable<IDetailObject>`       | GetChildrenByFolders(`Boolean` recursive)                                                              |                     |
| `void`                             | Init()                                                                                                 |                     |
| `void`                             | InitRLSIndexer()                                                                                       |                     |
| `void`                             | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue)                         |                     |
| `void`                             | OnPropertyChanging(`String` propertyName, `Object` newValue, `Boolean&` undoable, `Boolean&` cancel)   |                     |
| `void`                             | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True)                                |                     |
| `void`                             | Undelete(`ITabularObjectCollection` collection)                                                        |                     |

静态字段

| 类型       | 名称                    | 摘要 |
| -------- | --------------------- | -- |
| `Char[]` | InvalidTableNameChars |    |

## `TableCollection`

用于 Table 的集合类。 提供便捷的属性，可一次性为多个对象设置同一属性。

```csharp
public class TabularEditor.TOMWrapper.TableCollection
    : TabularObjectCollection<Table, Table, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Table>, IEnumerable<Table>, IList<Table>, ITabularObjectCollection, IExpandableIndexer

```

属性

| 类型        | 名称           | 摘要 |
| --------- | ------------ | -- |
| `String`  | DataCategory |    |
| `String`  | 描述           |    |
| `Boolean` | IsHidden     |    |
| `Model`   | Parent       |    |

方法

| 类型       | 名称                            | 摘要 |
| -------- | ----------------------------- | -- |
| `String` | ToString() |    |

## `TableExtension`

```csharp
public static class TabularEditor.TOMWrapper.TableExtension

```

静态方法

| 类型                    | 名称                                                   | 摘要 |
| --------------------- | ---------------------------------------------------- | -- |
| `PartitionSourceType` | GetSourceType(this `Table` table) |    |

## `TableRLSIndexer`

TableRLSIndexer 用于浏览模型中针对某个特定表定义的所有筛选器，涵盖模型中的所有角色。 这与 RoleRLSIndexer 相对：后者用于浏览模型中某个特定角色在所有表上定义的筛选器。

```csharp
public class TabularEditor.TOMWrapper.TableRLSIndexer
    : IEnumerable<String>, IEnumerable, IExpandableIndexer

```

字段

| 类型      | 名称    | 摘要 |
| ------- | ----- | -- |
| `Table` | Table |    |

属性

| 类型                              | 名称      | 摘要 |
| ------------------------------- | ------- | -- |
| `String`                        | Item    |    |
| `String`                        | Item    |    |
| `IEnumerable<String>`           | Keys    |    |
| `Dictionary<ModelRole, String>` | RLSMap  |    |
| `String`                        | Summary |    |

方法

| 类型                    | 名称                                                                   | 摘要 |
| --------------------- | -------------------------------------------------------------------- | -- |
| `void`                | Clear()                                           |    |
| `void`                | CopyFrom(`TableRLSIndexer` source)                |    |
| `String`              | GetDisplayName(`String` key)                      |    |
| `IEnumerator<String>` | GetEnumerator()                                   |    |
| `void`                | Refresh()                                         |    |
| `void`                | SetRLS(`ModelRole` 角色, `String` filterExpression) |    |

## `TabularCollectionHelper`

```csharp
public static class TabularEditor.TOMWrapper.TabularCollectionHelper

```

静态方法

| 类型     | 名称                                                                                                                                  | 摘要 |
| ------ | ----------------------------------------------------------------------------------------------------------------------------------- | -- |
| `void` | InPerspective(this `IEnumerable<Table>` tables, `String` 透视, `Boolean` value)                                    |    |
| `void` | InPerspective(this `IEnumerable<Column>` columns, `String` 透视, `Boolean` value)                                  |    |
| `void` | InPerspective(this `IEnumerable<Hierarchy>` hierarchies, `String` 透视, `Boolean` value)                           |    |
| `void` | InPerspective(this `IEnumerable<Measure>` 度量值, `String` 透视, `Boolean` value)                                     |    |
| `void` | InPerspective(this `IEnumerable<Table>` tables, `透视` 透视, `Boolean` value)                                        |    |
| `void` | InPerspective(this `IEnumerable<Column>` columns, `透视` perspective, `Boolean` value)                             |    |
| `void` | InPerspective(this `IEnumerable<Hierarchy>` hierarchies, `透视` perspective, `Boolean` value)                      |    |
| `void` | InPerspective(this `IEnumerable<Measure>` measures, `Perspective` perspective, `Boolean` value) - 在透视中将度量值设置为指定值 |    |
| `void` | SetDisplayFolder(this `IEnumerable<Measure>` measures, `String` displayFolder) - 设置度量值的显示文件夹                     |    |

## `TabularCommonActions`

提供用于在 Tabular 模型上执行常见操作的便捷方法，这些操作通常会同时更改多个对象。  例如，可使用这些方法轻松执行 UI 拖放操作，从而更改层次结构级别、显示文件夹等。

```csharp
public class TabularEditor.TOMWrapper.TabularCommonActions

```

属性

| 类型                    | 名称      | 摘要 |
| --------------------- | ------- | -- |
| `TabularModelHandler` | Handler |    |

方法

| 类型       | 名称                                                                                                                           | 摘要 |
| -------- | ---------------------------------------------------------------------------------------------------------------------------- | -- |
| `void`   | AddColumnsToHierarchy(`IEnumerable<Column>` columns, `Hierarchy` hierarchy, `Int32` firstOrdinal = -1)    |    |
| `Level`  | AddColumnToHierarchy(`Column` column, `Hierarchy` hierarchy, `Int32` ordinal = -1)                        |    |
| `void`   | MoveObjects(`IEnumerable<IDetailObject>` objects, `Table` newTable, `区域设置` culture)                       |    |
| `String` | NewColumnName(`String` prefix, `Table` table)                                                             |    |
| `String` | New度量值Name(`String` prefix)                                                                               |    |
| `void`   | ReorderLevels(`IEnumerable<Level>` levels, `Int32` firstOrdinal)                                          |    |
| `void`   | SetContainer(`IEnumerable<IDetailObject>` objects, `IDetailObjectContainer` newContainer, `区域设置` culture) |    |

## `TabularConnection`

```csharp
public static class TabularEditor.TOMWrapper.TabularConnection

```

静态方法

| 类型       | 名称                                                                                                | 摘要 |
| -------- | ------------------------------------------------------------------------------------------------- | -- |
| `String` | GetConnectionString(`String` serverName)                                       |    |
| `String` | GetConnectionString(`String` serverName, `String` userName, `String` password) |    |

## `Tabular区域设置Helper`

```csharp
public static class TabularEditor.TOMWrapper.Tabular区域设置Helper

```

静态方法

| 类型        | 名称                                                                                                                              | 摘要 |
| --------- | ------------------------------------------------------------------------------------------------------------------------------- | -- |
| `Boolean` | ImportTranslations(`String` culturesJson, `Model` Model, `Boolean` overwriteExisting, `Boolean` haltOnError) |    |

## `TabularDeployer`

```csharp
public class TabularEditor.TOMWrapper.TabularDeployer

```

静态方法

| 类型                 | 名称                                                                                                                                | 摘要                                                                |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| `void`             | Deploy(`Database` db, `String` targetConnectionString, `String` targetDatabaseName)                            | 使用指定的选项，将指定数据库部署到指定的目标服务器和数据库 ID。  部署成功后，将返回数据库中对象的 DAX 错误列表（如有）。 |
| `DeploymentResult` | Deploy(`Database` db, `String` targetConnectionString, `String` targetDatabaseID, `DeploymentOptions` options) | 使用指定的选项，将指定数据库部署到指定的目标服务器和数据库 ID。  部署成功后，将返回数据库中对象的 DAX 错误列表（如有）。 |
| `String`           | GetTMSL(`Database` db, `Server` server, `String` targetDatabaseID, `DeploymentOptions` options)                |                                                                   |
| `void`             | SaveModelMetadataBackup(`String` connectionString, `String` targetDatabaseID, `String` backupFilePath)         |                                                                   |
| `void`             | WriteZip(`String` fileName, `String` content)                                                                  |                                                                   |

## `TabularModelHandler`

```csharp
public class TabularEditor.TOMWrapper.TabularModelHandler
    : IDisposable

```

字段

| 类型                                             | 名称                 | 摘要 |
| ---------------------------------------------- | ------------------ | -- |
| `Dictionary<String, ITabularObjectCollection>` | WrapperCollections |    |
| `Dictionary<MetadataObject, TabularObject>`    | WrapperLookup      |    |

属性

| 类型                                          | 名称                       | 摘要                                                                              |
| ------------------------------------------- | ------------------------ | ------------------------------------------------------------------------------- |
| `TabularCommonActions`                      | Actions                  |                                                                                 |
| `Boolean`                                   | AutoFixup                | 用于指定对象名称（表、列、度量值）发生更改时，是否应自动更新 DAX 表达式以反映新名称。 设置为 true 时，将解析模型中的所有表达式，以构建依赖关系树。 |
| `Database`                                  | Database                 |                                                                                 |
| `Boolean`                                   | DelayBuildDependencyTree |                                                                                 |
| `IList<Tuple<NamedMetadataObject, String>>` | Errors                   |                                                                                 |
| `Boolean`                                   | HasUnsavedChanges        |                                                                                 |
| `Boolean`                                   | IsConnected              |                                                                                 |
| `Model`                                     | Model                    |                                                                                 |
| `String`                                    | Status                   |                                                                                 |
| `TabularTree`                               | Tree                     |                                                                                 |
| `UndoManager`                               | UndoManager              |                                                                                 |
| `Int64`                                     | Version                  |                                                                                 |

方法

| 类型                          | 名称                                                                                                                 | 摘要                                                                                                                      |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| `IDetailObject`             | Add(`AddObjectType` objectType, `IDetailObjectContainer` container)                             |                                                                                                                         |
| `void`                      | BeginUpdate(`String` undoName)                                                                  |                                                                                                                         |
| `void`                      | BuildDependencyTree(`IExpressionObject` expressionObj)                                          |                                                                                                                         |
| `void`                      | BuildDependencyTree()                                                                           |                                                                                                                         |
| `ConflictInfo`              | CheckConflicts()                                                                                |                                                                                                                         |
| `IList<TabularNamedObject>` | DeserializeObjects(`String` json)                                                               |                                                                                                                         |
| `void`                      | Dispose()                                                                                       |                                                                                                                         |
| `void`                      | DoFixup(`IDaxObject` obj, `String` newName)                                                     | 将对对象“obj”的所有引用更改为“newName”                                                                                              |
| `Int32`                     | EndUpdate(`Boolean` undoable = True, `Boolean` rollback = False)                                |                                                                                                                         |
| `Int32`                     | EndUpdateAll(`Boolean` rollback = False)                                                        |                                                                                                                         |
| `Model`                     | GetModel()                                                                                      |                                                                                                                         |
| `Boolean`                   | ImportTranslations(`String` culturesJson, `Boolean` overwriteExisting, `Boolean` ignoreInvalid) | 从 JSON 字符串中应用翻译内容。                                                                                                      |
| `void`                      | SaveDB()                                                                                        | 将更改保存到数据库。 用户需自行检查：自数据库加载到 TOMWrapper 之后，数据库是否已被更改。 为此，可使用 Handler.CheckConflicts()。 |
| `void`                      | SaveFile(`String` fileName, `SerializeOptions` options)                                         |                                                                                                                         |
| `void`                      | SaveToFolder(`String` path, `SerializeOptions` options)                                         |                                                                                                                         |
| `String`                    | ScriptCreateOrReplace()                                                                         | 为整个数据库生成脚本                                                                                                              |
| `String`                    | ScriptCreateOrReplace(`TabularNamedObject` obj)                                                 | 为整个数据库生成脚本                                                                                                              |
| `String`                    | 脚本翻译 ScriptTranslations(`IEnumerable<Culture>` translations)                                    |                                                                                                                         |
| `String`                    | SerializeObjects(`IEnumerable<TabularNamedObject>` objects)                                     |                                                                                                                         |
| `void`                      | UpdateFolders(`Table` table)                                                                    |                                                                                                                         |
| `void`                      | UpdateLevels(`Hierarchy` hierarchy)                                                             |                                                                                                                         |
| `void`                      | UpdateObject(`ITabularObject` obj)                                                              |                                                                                                                         |
| `void`                      | UpdateTables()                                                                                  |                                                                                                                         |

静态字段

| 类型       | 名称                                          | 摘要 |
| -------- | ------------------------------------------- | -- |
| `String` | PROP_ERRORS            |    |
| `String` | PROP_HASUNSAVEDCHANGES |    |
| `String` | PROP_ISCONNECTED       |    |
| `String` | PROP_STATUS            |    |

静态属性

| 类型                    | 名称 | 摘要 |
| --------------------- | -- | -- |
| `TabularModelHandler` | 单例 |    |

静态方法

| 类型                                              | 名称                                                           | 摘要 |
| ----------------------------------------------- | ------------------------------------------------------------ | -- |
| `List<Tuple<NamedMetadataObject, String>>`      | CheckErrors(`Database` database)          |    |
| `List<Tuple<NamedMetadataObject, ObjectState>>` | CheckProcessingState(`Database` database) |    |

## `TabularNamedObject`

TabularObject 是对 Microsoft.AnalysisServices.Tabular.NamedMetadataObject 类的封装。  该封装用于所有需要在 Tabular Editor 中查看和编辑的对象。  Tabular Model 中的各类对象都使用同一个基类。 该基类提供一个方法，用于编辑（本地化）名称和说明。

```csharp
public abstract class TabularEditor.TOMWrapper.TabularNamedObject
    : TabularObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable

```

属性

| 类型                    | 名称              | 摘要           |
| --------------------- | --------------- | ------------ |
| `Int32`               | MetadataIndex   |              |
| `NamedMetadataObject` | MetadataObject  |              |
| `String`              | Name            |              |
| `TranslationIndexer`  | TranslatedNames | 此对象的本地化名称集合。 |

方法

| 类型                   | 名称                                                                        | 摘要                                                                            |
| -------------------- | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `TabularNamedObject` | Clone(`String` newName, `Boolean` includeTranslations) |                                                                               |
| `Int32`              | CompareTo(`Object` obj)                                |                                                                               |
| `void`               | Delete()                                               |                                                                               |
| `void`               | Init()                                                 |                                                                               |
| `void`               | Undelete(`ITabularObjectCollection` collection)        | 要撤销删除操作，需要一个不太优雅的临时变通方案。  派生类必须注意更新该对象所“拥有”的所有对象。 例如，度量值必须负责更新其 KPI 的包装器（如有）。 |

## `TabularObject`

```csharp
public abstract class TabularEditor.TOMWrapper.TabularObject
    : ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging

```

字段

| 类型                         | 名称   | 摘要 |
| -------------------------- | ---- | -- |
| `ITabularObjectCollection` | 集合   |    |
| `TabularModelHandler`      | 处理程序 |    |

属性

| 类型               | 名称                       | 摘要 |
| ---------------- | ------------------------ | -- |
| `MetadataObject` | 元数据对象                    |    |
| `Model`          | 模型                       |    |
| `ObjectType`     | ObjectType               |    |
| `String`         | ObjectTypeName           |    |
| `翻译索引器`          | TranslatedDescriptions   |    |
| `翻译索引器`          | TranslatedDisplayFolders |    |

事件

| 类型                             | 名称               | 摘要 |
| ------------------------------ | ---------------- | -- |
| `PropertyChangedEventHandler`  | PropertyChanged  |    |
| `PropertyChangingEventHandler` | PropertyChanging |    |

方法

| 类型        | 名称                                                                                                                      | 摘要                                                                       |
| --------- | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| `void`    | Init()                                                                                               | 派生类应重写此方法，以实例化子对象                                                        |
| `void`    | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue)                       |                                                                          |
| `void`    | OnPropertyChanging(`String` propertyName, `Object` newValue, `Boolean&` undoable, `Boolean&` cancel) | 在对象的属性更改之前调用。 派生类可以控制如何处理此更改。  在此方法中抛出 ArgumentException，以便在 UI 中显示错误信息。 |
| `Boolean` | SetField(`T&` field, `T` value, `String` propertyName = null)                                        |                                                                          |

## `TabularObjectCollection<T, TT, TP>`

```csharp
public abstract class TabularEditor.TOMWrapper.TabularObjectCollection<T, TT, TP>
    : IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<T>, IEnumerable<T>, IList<T>, ITabularObjectCollection, IExpandableIndexer

```

属性

| 类型                                      | 名称                       | 摘要 |
| --------------------------------------- | ------------------------ | -- |
| `String`                                | CollectionName           |    |
| `Int32`                                 | Count                    |    |
| `TabularModelHandler`                   | Handler                  |    |
| `Boolean`                               | IsFixedSize              |    |
| `Boolean`                               | IsReadOnly               |    |
| `Boolean`                               | IsSynchronized           |    |
| `T`                                     | Item                     |    |
| `T`                                     | Item                     |    |
| `IEnumerable<String>`                   | Keys                     |    |
| `NamedMetadataObjectCollection<TT, TP>` | MetadataObjectCollection |    |
| `String`                                | Summary                  |    |
| `Object`                                | SyncRoot                 |    |

事件

| 类型                                    | 名称                | 摘要 |
| ------------------------------------- | ----------------- | -- |
| `NotifyCollectionChangedEventHandler` | CollectionChanged |    |

方法

| 类型                         | 名称                                                         | 摘要 |
| -------------------------- | ---------------------------------------------------------- | -- |
| `void`                     | Add(`T` item)                           |    |
| `void`                     | Add(`TabularNamedObject` item)          |    |
| `Int32`                    | Add(`Object` value)                     |    |
| `void`                     | Clear()                                 |    |
| `Boolean`                  | Contains(`T` item)                      |    |
| `Boolean`                  | Contains(`Object` value)                |    |
| `Boolean`                  | Contains(`String` name)                 |    |
| `void`                     | CopyTo(`T[]` array, `Int32` arrayIndex) |    |
| `void`                     | CopyTo(`Array` array, `Int32` index)    |    |
| `void`                     | ForEach(`Action<T>` action)             |    |
| `ITabularObjectCollection` | GetCurrentCollection()                  |    |
| `String`                   | GetDisplayName(`String` key)            |    |
| `IEnumerator<T>`           | GetEnumerator()                         |    |
| `Int32`                    | IndexOf(`TabularNamedObject` obj)       |    |
| `Int32`                    | IndexOf(`T` item)                       |    |
| `Int32`                    | IndexOf(`Object` value)                 |    |
| `void`                     | Insert(`Int32` index, `T` item)         |    |
| `void`                     | Insert(`Int32` index, `Object` value)   |    |
| `void`                     | Refresh()                               |    |
| `void`                     | Remove(`TabularNamedObject` item)       |    |
| `Boolean`                  | Remove(`T` item)                        |    |
| `void`                     | Remove(`Object` value)                  |    |
| `void`                     | RemoveAt(`Int32` index)                 |    |

## `TabularObjectComparer`

```csharp
public class TabularEditor.TOMWrapper.TabularObjectComparer
    : IComparer<ITabularNamedObject>, IComparer

```

属性

| 类型            | 名称 | 摘要 |
| ------------- | -- | -- |
| `ObjectOrder` | 顺序 |    |

方法

| 类型      | 名称                                                                           | 摘要 |
| ------- | ---------------------------------------------------------------------------- | -- |
| `Int32` | Compare(`Object` x, `Object` y)                           |    |
| `Int32` | Compare(`ITabularNamedObject` x, `ITabularNamedObject` y) |    |

## `TabularObjectHelper`

```csharp
public static class TabularEditor.TOMWrapper.TabularObjectHelper

```

静态方法

| 类型        | 名称                                                                                           | 摘要 |
| --------- | -------------------------------------------------------------------------------------------- | -- |
| `String`  | GetLinqPath(this `TabularNamedObject` obj)                                |    |
| `String`  | GetName(this `ITabularNamedObject` obj, `区域设置` culture)                   |    |
| `String`  | GetObjectPath(this `MetadataObject` obj)                                  |    |
| `String`  | GetObjectPath(this `TabularObject` obj)                                   |    |
| `String`  | GetTypeName(this `ObjectType` objType, `Boolean` plural = False)          |    |
| `String`  | GetTypeName(this `ITabularObject` obj, `Boolean` plural = False)          |    |
| `Boolean` | SetName(this `ITabularNamedObject` obj, `String` newName, `区域设置` culture) |    |
| `String`  | SplitCamelCase(this `String` str)                                         |    |

## `TabularTree`

TabularLogicalModel 用于控制 TabularObjects 之间的关系，使其能够在 TreeViewAdv 控件中显示。 单个 TabularObject 本身既不知道，也不关心它与其他对象之间的逻辑关系（例如，在特定区域设置下通过 DisplayFolders 建立的关系）。 TabularObjects 只关心其物理关系，这些关系直接从 Tabular Object Model 继承而来（例如，度量值属于某个表等）。

```csharp
public abstract class TabularEditor.TOMWrapper.TabularTree
    : INotifyPropertyChanged

```

字段

| 类型                           | 名称         | 摘要 |
| ---------------------------- | ---------- | -- |
| `Dictionary<String, Folder>` | FolderTree |    |

属性

| 类型                    | 名称          | 摘要 |
| --------------------- | ----------- | -- |
| `区域设置`                | 区域设置        |    |
| `String`              | 筛选器         |    |
| `TabularModelHandler` | 处理程序        |    |
| `Model`               | 模型          |    |
| `LogicalTreeOptions`  | 选项          |    |
| `透视`                  | 透视          |    |
| `Int32`               | UpdateLocks |    |

事件

| 类型                            | 名称              | 摘要 |
| ----------------------------- | --------------- | -- |
| `PropertyChangedEventHandler` | PropertyChanged |    |

方法

| 类型                     | 名称                                                                                                           | 摘要                                                        |
| ---------------------- | ------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------- |
| `void`                 | BeginUpdate()                                                                             |                                                           |
| `void`                 | EndUpdate()                                                                               |                                                           |
| `IEnumerable`          | GetChildren(`ITabularObjectContainer` tabularObject)                                      | 此方法封装了用于定义表格式模型的树形表示应如何构建的逻辑                              |
| `Func<String, String>` | GetFolderMutation(`Object` source, `Object` destination)                                  |                                                           |
| `Func<String, String>` | GetFolderMutation(`String` oldPath, `String` newPath)                                     |                                                           |
| `void`                 | ModifyDisplayFolder(`Table` table, `String` oldPath, `String` newPath, `Culture` culture) | 更新同一张表中所有表格对象的 DisplayFolder 属性。 位于更新后路径下各子文件夹中的对象也会同步更新。 |
| `void`                 | OnNodesChanged(`ITabularObject` nodeItem)                                                 |                                                           |
| `void`                 | OnNodesInserted(`ITabularObject` parent, `ITabularObject[]` children)                     |                                                           |
| `void`                 | OnNodesInserted(`ITabularObject` parent, `IEnumerable<ITabularObject>` children)          |                                                           |
| `void`                 | OnNodesRemoved(`ITabularObject` parent, `ITabularObject[]` children)                      |                                                           |
| `void`                 | OnNodesRemoved(`ITabularObject` parent, `IEnumerable<ITabularObject>` children)           |                                                           |
| `void`                 | OnStructureChanged(`ITabularNamedObject` obj = null)                                      |                                                           |
| `void`                 | SetCulture(`String` cultureName)                                                          |                                                           |
| `void`                 | SetPerspective(`String` perspectiveName)                                                  |                                                           |
| `void`                 | UpdateFolder(`Folder` folder, `String` oldFullPath = null)                                |                                                           |
| `Boolean`              | VisibleInTree(`ITabularNamedObject` tabularObject)                                        |                                                           |

## `翻译索引器`

```csharp
public class TabularEditor.TOMWrapper.TranslationIndexer
    : IEnumerable<String>, IEnumerable, IExpandableIndexer

```

属性

| 类型                    | 名称              | 摘要 |
| --------------------- | --------------- | -- |
| `String`              | DefaultValue    |    |
| `String`              | Item            |    |
| `String`              | Item            |    |
| `IEnumerable<String>` | Keys            |    |
| `String`              | Summary         |    |
| `Int32`               | TranslatedCount |    |

方法

| 类型                           | 名称                                                                                          | 摘要                                                                  |
| ---------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `void`                       | Clear()                                                                  | 清除该对象的所有翻译值。                                                        |
| `Boolean`                    | Contains(`区域设置` culture)                                                 |                                                                     |
| `Dictionary<String, String>` | Copy()                                                                   |                                                                     |
| `void`                       | CopyFrom(`TranslationIndexer` 翻译, `Func<String, String>` mutator = null) |                                                                     |
| `void`                       | CopyFrom(`IDictionary<String, String>` source)                           |                                                                     |
| `String`                     | GetDisplayName(`String` key)                                             |                                                                     |
| `IEnumerator<String>`        | GetEnumerator()                                                          |                                                                     |
| `void`                       | Refresh()                                                                |                                                                     |
| `void`                       | Reset()                                                                  | 重置该对象的翻译内容。 将删除标题翻译，使该对象在所有区域设置中都显示为基本名称。 显示文件夹和描述的翻译将被设置为该对象的未翻译值。 |
| `void`                       | SetAll(`String` value)                                                   |                                                                     |


