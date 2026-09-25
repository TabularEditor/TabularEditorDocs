# TabularEditor.TOMWrapper 参考文档

这是为 TOMWrapper API 自动生成的文档。使用 CTRL+F 或右侧的侧边栏，定位特定的类、属性或方法。

## `AddObjectType`

```csharp
public enum TabularEditor.TOMWrapper.AddObjectType
    : Enum, IComparable, IFormattable, IConvertible

```

枚举

| 值   | 姓名               | 摘要 |
| --- | ---------------- | -- |
| `1` | 度量值              |    |
| `2` | CalculatedColumn |    |
| `3` | 层次结构             |    |

## `CalculatedColumn`

CalculatedColumn 的基类声明

```csharp
public class TabularEditor.TOMWrapper.CalculatedColumn
    : Column, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IErrorMessageObject, IDescriptionObject, IAnnotationObject, ITabularPerspectiveObject, IDaxObject, IExpressionObject

```

属性

| 类型                                         | 姓名                 | 摘要                                              |
| ------------------------------------------ | ------------------ | ----------------------------------------------- |
| `Dictionary<IDaxObject, List<Dependency>>` | 依赖项                |                                                 |
| `String`                                   | 表达式                | 获取或设置 CalculatedColumn 的 Expression 属性。         |
| `Boolean`                                  | IsDataTypeInferred | 获取或设置 CalculatedColumn 的 IsDataTypeInferred 属性。 |
| `CalculatedColumn`                         | MetadataObject     |                                                 |
| `Boolean`                                  | NeedsValidation    |                                                 |

方法

| 类型                   | 姓名                                                                                                       | 摘要 |
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

| 类型                                         | 姓名              | 摘要 |
| ------------------------------------------ | --------------- | -- |
| `Dictionary<IDaxObject, List<Dependency>>` | 依赖项             |    |
| `String`                                   | 表达式             |    |
| `Boolean`                                  | NeedsValidation |    |
| `String`                                   | ObjectTypeName  |    |

方法

| 类型        | 姓名                                                                                                | 摘要                                      |
| --------- | ------------------------------------------------------------------------------------------------- | --------------------------------------- |
| `void`    | CheckChildrenErrors()                                                          |                                         |
| `Boolean` | Editable(`String` propertyName)                                                |                                         |
| `void`    | Init()                                                                         |                                         |
| `void`    | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue) |                                         |
| `void`    | ReinitColumns()                                                                | 在模型保存到数据库后调用此方法，用于检查列是否发生更改（例如表达式发生变化时） |

## `CalculatedTableColumn`

CalculatedTableColumn 的基类声明

```csharp
public class TabularEditor.TOMWrapper.CalculatedTableColumn
    : Column, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IErrorMessageObject, IDescriptionObject, IAnnotationObject, ITabularPerspectiveObject, IDaxObject

```

属性

| 类型                      | 姓名                 | 摘要                                                   |
| ----------------------- | ------------------ | ---------------------------------------------------- |
| `列`                     | ColumnOrigin       | 获取或设置 CalculatedTableColumn 的 ColumnOrigin 属性。       |
| `Boolean`               | IsDataTypeInferred | 获取或设置 CalculatedTableColumn 的 IsDataTypeInferred 属性。 |
| `Boolean`               | IsNameInferred     | 获取或设置 CalculatedTableColumn 的 IsNameInferred 属性。     |
| `CalculatedTableColumn` | MetadataObject     |                                                      |
| `String`                | 源列                 | 获取或设置 CalculatedTableColumn 的 SourceColumn 属性。       |

## `列`

列的基类声明

```csharp
public abstract class TabularEditor.TOMWrapper.Column
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IErrorMessageObject, IDescriptionObject, IAnnotationObject, ITabularPerspectiveObject, IDaxObject

```

属性

| 类型                           | 姓名                                              | 摘要                              |
| ---------------------------- | ----------------------------------------------- | ------------------------------- |
| `对齐方式`                       | 对齐方式                                            | 获取或设置列的对齐方式。                    |
| `String`                     | DataCategory                                    | 获取或设置列的 DataCategory。           |
| `数据类型`                       | 数据类型                                            | 获取或设置列的数据类型。                    |
| `String`                     | DaxObjectFullName                               |                                 |
| `String`                     | DaxObjectName                                   |                                 |
| `String`                     | DaxTableName                                    |                                 |
| `HashSet<IExpressionObject>` | Dependants                                      |                                 |
| `String`                     | 说明                                              | 获取或设置列的描述。                      |
| `String`                     | DisplayFolder                                   | 获取或设置列的 DisplayFolder。          |
| `Int32`                      | DisplayOrdinal                                  | 获取或设置该列的 DisplayOrdinal。        |
| `String`                     | ErrorMessage                                    | 获取或设置该列的 ErrorMessage。          |
| `String`                     | 格式字符串                                           | 获取或设置该列的 FormatString。          |
| `透视索引器`                      | 在透视中                                            |                                 |
| `Boolean`                    | IsAvailableInMDX                                | 获取或设置该列的 IsAvailableInMDX。      |
| `Boolean`                    | IsDefaultImage                                  | 获取或设置该列的 IsDefaultImage。        |
| `Boolean`                    | IsDefaultLabel                                  | 获取或设置该列的 IsDefaultLabel。        |
| `Boolean`                    | IsHidden                                        | 获取或设置该列的 IsHidden。              |
| `Boolean`                    | IsKey                                           | 获取或设置该列的 IsKey。                 |
| `Boolean`                    | IsNullable                                      | 获取或设置该列的 IsNullable 属性。         |
| `Boolean`                    | IsUnique                                        | 获取或设置该列的 IsUnique 属性。           |
| `Boolean`                    | KeepUniqueRows                                  | 获取或设置该列的 KeepUniqueRows 属性。     |
| `列`                          | MetadataObject                                  |                                 |
| `列`                          | SortByColumn                                    | 获取或设置该列的 SortByColumn 属性。       |
| `String`                     | SourceProviderType                              | 获取或设置该列的 SourceProviderType 属性。 |
| `ObjectState`                | State                                           | 获取或设置该列的 State 属性。              |
| `AggregateFunction`          | SummarizeBy                                     | 获取或设置该列的 SummarizeBy 属性。        |
| `表`                          | 表                                               |                                 |
| `Int32`                      | TableDetailPosition                             | 获取或设置此列的 TableDetailPosition。   |
| `TranslationIndexer`         | TranslatedDescriptions                          | 此列的本地化描述集合。                     |
| `TranslationIndexer`         | TranslatedDisplayFolders                        | 此列的本地化“显示文件夹”集合。                |
| `ColumnType`                 | Type                                            | 获取或设置此列的 Type。                  |
| `IEnumerable<Hierarchy>`     | UsedInHierarchies<a id="used-in-hierarchy"></a> | 枚举所有将此列用作级别的层次结构。               |
| `IEnumerable<Relationship>`  | UsedInRelationships                             | 枚举此列参与的所有关系（无论作为  还是  ）。        |

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

用于 Column 的集合类。提供便捷的属性，使你可以一次性在多个对象上设置同一属性。

```csharp
public class TabularEditor.TOMWrapper.ColumnCollection
    : TabularObjectCollection<Column, Column, Table>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Column>, IEnumerable<Column>, IList<Column>, ITabularObjectCollection, IExpandableIndexer

```

属性

| 类型          | 姓名                 | 摘要 |
| ----------- | ------------------ | -- |
| `Alignment` | Alignment          |    |
| `String`    | DataCategory       |    |
| `数据类型`      | 数据类型               |    |
| `String`    | 说明                 |    |
| `String`    | DisplayFolder      |    |
| `Int32`     | DisplayOrdinal     |    |
| `String`    | 格式字符串              |    |
| `布尔值`       | IsAvailableInMDX   |    |
| `布尔值`       | IsDefaultImage     |    |
| `布尔值`       | IsDefaultLabel     |    |
| `布尔值`       | IsHidden           |    |
| `布尔值`       | IsKey              |    |
| `布尔值`       | IsNullable         |    |
| `布尔值`       | IsUnique           |    |
| `布尔值`       | KeepUniqueRows     |    |
| `表`         | Parent             |    |
| `列`         | SortByColumn       |    |
| `字符串`       | SourceProviderType |    |
| `聚合函数`      | SummarizeBy        |    |
| `Int32`     | 表详细信息位置            |    |

方法

| 类型                    | 姓名                                 | 摘要 |
| --------------------- | ---------------------------------- | -- |
| `IEnumerator<Column>` | GetEnumerator() |    |
| `String`              | ToString()      |    |

## `区域设置`

区域设置的基类声明

```csharp
public class TabularEditor.TOMWrapper.Culture
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IAnnotationObject, IDynamicPropertyObject

```

属性

| 类型                            | 姓名                           | 摘要 |
| ----------------------------- | ---------------------------- | -- |
| `String`                      | DisplayName                  |    |
| `区域设置`                        | MetadataObject               |    |
| `String`                      | 姓名                           |    |
| `ObjectTranslationCollection` | ObjectTranslations           |    |
| `String`                      | StatsColumnCaptions          |    |
| `String`                      | StatsColumnDisplayFolders    |    |
| `String`                      | StatsHierarchyCaptions       |    |
| `String`                      | StatsHierarchyDisplayFolders |    |
| `String`                      | StatsLevelCaptions           |    |
| `String`                      | Stats度量值Captions             |    |
| `String`                      | Stats度量值DisplayFolders       |    |
| `String`                      | StatsTableCaptions           |    |
| `Boolean`                     | 未分配                          |    |

方法

| 类型                   | 姓名                                                                                                | 摘要 |
| -------------------- | ------------------------------------------------------------------------------------------------- | -- |
| `Boolean`            | Browsable(`String` propertyName)                                               |    |
| `TabularNamedObject` | Clone(`String` newName, `Boolean` includeTranslations)                         |    |
| `Boolean`            | Editable(`String` propertyName)                                                |    |
| `String`             | GetAnnotation(`String` name)                                                   |    |
| `void`               | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue) |    |
| `void`               | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True)        |    |
| `void`               | Undelete(`ITabularObjectCollection` collection)                                |    |

## `区域设置集合`

用于区域设置的集合类。提供便捷的属性，可一次性在多个对象上设置同一属性。

```csharp
public class TabularEditor.TOMWrapper.CultureCollection
    : TabularObjectCollection<Culture, Culture, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Culture>, IEnumerable<Culture>, IList<Culture>, ITabularObjectCollection, IExpandableIndexer

```

属性

| 类型      | 姓名 | 摘要 |
| ------- | -- | -- |
| `Model` | 父级 |    |

方法

| 类型       | 姓名                            | 摘要 |
| -------- | ----------------------------- | -- |
| `String` | ToString() |    |

## `区域设置转换器`

```csharp
public class TabularEditor.TOMWrapper.CultureConverter
    : TypeConverter

```

方法

| 类型                         | 姓名                                                                                                                         | 摘要 |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------- | -- |
| `Boolean`                  | CanConvertFrom(`ITypeDescriptorContext` context, `Type` sourceType)                                     |    |
| `Boolean`                  | CanConvertTo(`ITypeDescriptorContext` context, `Type` destinationType)                                  |    |
| `Object`                   | ConvertFrom(`ITypeDescriptorContext` context, `CultureInfo` 区域设置, `Object` value)                       |    |
| `对象`                       | ConvertTo(`ITypeDescriptorContext` context, `CultureInfo` 区域设置, `Object` value, `Type` destinationType) |    |
| `StandardValuesCollection` | GetStandardValues(`ITypeDescriptorContext` context)                                                     |    |
| `Boolean`                  | GetStandardValuesExclusive(`ITypeDescriptorContext` context)                                            |    |
| `Boolean`                  | GetStandardValuesSupported(`ITypeDescriptorContext` context)                                            |    |

## `数据库`

```csharp
public class TabularEditor.TOMWrapper.Database

```

属性

| 类型                   | 姓名                 | 说明 |
| -------------------- | ------------------ | -- |
| `Nullable<Int32>`    | CompatibilityLevel |    |
| `Nullable<DateTime>` | CreatedTimestamp   |    |
| `String`             | ID                 |    |
| `Nullable<DateTime>` | LastProcessed      |    |
| `Nullable<DateTime>` | LastSchemaUpdate   |    |
| `Nullable<DateTime>` | LastUpdate         |    |
| `String`             | 姓名                 |    |
| `String`             | ServerName         |    |
| `String`             | ServerVersion      |    |
| `数据库`                | TOMDatabase        |    |
| `Nullable<Int64>`    | Version            |    |

方法

| 类型       | 姓名                            | 摘要 |
| -------- | ----------------------------- | -- |
| `String` | ToString() |    |

## `DataColumn`

DataColumn 的基类声明

```csharp
public class TabularEditor.TOMWrapper.DataColumn
    : Column, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IErrorMessageObject, IDescriptionObject, IAnnotationObject, ITabularPerspectiveObject, IDaxObject

```

属性

| 类型           | 姓名             | 摘要                               |
| ------------ | -------------- | -------------------------------- |
| `DataColumn` | MetadataObject |                                  |
| `String`     | 源列             | 获取或设置 DataColumn 的 SourceColumn。 |

## `DataSource`

DataSource 的基类声明

```csharp
public abstract class TabularEditor.TOMWrapper.DataSource
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject

```

属性

| 类型                   | 姓名                     | 摘要                     |
| -------------------- | ---------------------- | ---------------------- |
| `String`             | 说明                     | 获取或设置 DataSource 的描述。  |
| `DataSource`         | MetadataObject         |                        |
| `TranslationIndexer` | TranslatedDescriptions | 此 DataSource 的本地化描述集合。 |
| `DataSourceType`     | Type                   | 获取或设置 DataSource 的类型。  |

方法

| 类型       | 姓名                                                                                         | 摘要 |
| -------- | ------------------------------------------------------------------------------------------ | -- |
| `String` | GetAnnotation(`String` name)                                            |    |
| `void`   | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |    |

## `DataSourceCollection`

DataSource 的集合类。提供便捷的属性，可一次性为多个对象设置同一属性。

```csharp
public class TabularEditor.TOMWrapper.DataSourceCollection
    : TabularObjectCollection<DataSource, DataSource, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<DataSource>, IEnumerable<DataSource>, IList<DataSource>, ITabularObjectCollection, IExpandableIndexer

```

属性

| 类型       | 姓名     | 摘要 |
| -------- | ------ | -- |
| `String` | 说明     |    |
| `模型`     | Parent |    |

方法

| 类型       | 姓名                            | 摘要 |
| -------- | ----------------------------- | -- |
| `String` | ToString() |    |

## `Dependency`

```csharp
public struct TabularEditor.TOMWrapper.Dependency

```

字段

| 类型        | 姓名             | 摘要 |
| --------- | -------------- | -- |
| `Int32`   | from           |    |
| `Boolean` | fullyQualified |    |
| `Int32`   | to             |    |

## `DependencyHelper`

```csharp
public static class TabularEditor.TOMWrapper.DependencyHelper

```

静态方法

| 类型       | 姓名                                                                                                                                             | 摘要                                                                           |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `void`   | AddDep(this `IExpressionObject` target, `IDaxObject` dependsOn, `Int32` fromChar, `Int32` toChar, `Boolean` fullyQualified) |                                                                              |
| `String` | NoQ(this `String` objectName, `Boolean` table = False)                                                                      | 移除名称周围的限定符，例如 ' ' 和 [ ]。 |

## `DeploymentMode`

```csharp
public enum TabularEditor.TOMWrapper.DeploymentMode
    : Enum, IComparable, IFormattable, IConvertible

```

枚举

| 值   | 姓名             | 摘要 |
| --- | -------------- | -- |
| `0` | CreateDatabase |    |
| `1` | CreateOrAlter  |    |

## `DeploymentOptions`

```csharp
public class TabularEditor.TOMWrapper.DeploymentOptions

```

字段

| 类型               | 姓名                | 摘要 |
| ---------------- | ----------------- | -- |
| `Boolean`        | DeployConnections |    |
| `DeploymentMode` | DeployMode        |    |
| `Boolean`        | DeployPartitions  |    |
| `Boolean`        | DeployRoleMembers |    |
| `Boolean`        | DeployRoles       |    |

静态字段

| 类型                  | 姓名            | 摘要 |
| ------------------- | ------------- | -- |
| `DeploymentOptions` | 默认值           |    |
| `DeploymentOptions` | StructureOnly |    |

## `DeploymentResult`

```csharp
public class TabularEditor.TOMWrapper.DeploymentResult

```

字段

| 类型                      | 姓名 | 摘要 |
| ----------------------- | -- | -- |
| `IReadOnlyList<String>` | 问题 |    |
| `IReadOnlyList<String>` | 警告 |    |

## `DeploymentStatus`

```csharp
public enum TabularEditor.TOMWrapper.DeploymentStatus
    : Enum, IComparable, IFormattable, IConvertible

```

枚举

| 值   | 姓名              | 摘要 |
| --- | --------------- | -- |
| `0` | ChangesSaved    |    |
| `1` | DeployComplete  |    |
| `2` | DeployCancelled |    |

## `Folder`

表示 TreeView 中的一个文件夹。它不对应 TOM 中的任何对象。实现 IDisplayFolderObject，因为 Folder 本身也可以位于另一个显示文件夹中。实现 IParentObject，因为 Folder 可以包含子对象。

```csharp
public class TabularEditor.TOMWrapper.Folder
    : IDetailObject, ITabularTableObject, ITabularNamedObject, ITabularObject, INotifyPropertyChanged, ITabularObjectContainer, IDetailObjectContainer, IErrorMessageObject

```

属性

| 类型                       | 姓名              | 摘要 |
| ------------------------ | --------------- | -- |
| `IDetailObjectContainer` | 容器              |    |
| `区域设置`                   | 区域设置            |    |
| `字符串`                    | 显示文件夹           |    |
| `字符串`                    | 错误消息            |    |
| `字符串`                    | 完整路径            |    |
| `TabularModelHandler`    | 处理程序            |    |
| `Int32`                  | 元数据索引           |    |
| `模型`                     | 模型              |    |
| `字符串`                    | 姓名              |    |
| `对象类型`                   | 对象类型            |    |
| `表`                      | 父表              |    |
| `字符串`                    | 路径              |    |
| `表`                      | 表               |    |
| `TranslationIndexer`     | 已翻译的显示文件夹       |    |
| `TranslationIndexer`     | TranslatedNames |    |

事件

| 类型                            | 姓名              | 摘要 |
| ----------------------------- | --------------- | -- |
| `PropertyChangedEventHandler` | PropertyChanged |    |

方法

| 类型                                 | 姓名                                                                   | 摘要                                                    |
| ---------------------------------- | -------------------------------------------------------------------- | ----------------------------------------------------- |
| `void`                             | CheckChildrenErrors()                             |                                                       |
| `void`                             | Delete()                                          | 删除文件夹不会删除其子对象，只是移除该文件夹。所有子文件夹都会保留（但会在显示文件夹层级结构中向上移动）。 |
| `IEnumerable<ITabularNamedObject>` | GetChildren()                                     |                                                       |
| `IEnumerable<IDetailObject>`       | GetChildrenByFolders(`Boolean` recursive = False) |                                                       |
| `void`                             | SetFolderName(`String` newName)                   |                                                       |
| `void`                             | UndoSetPath(`String` value)                       |                                                       |

静态方法

| 类型       | 姓名                                                                                                                              | 摘要 |
| -------- | ------------------------------------------------------------------------------------------------------------------------------- | -- |
| `Folder` | CreateFolder(`Table` table, `String` path = , `Boolean` useFixedCulture = False, `区域设置` fixedCulture = null) |    |

## `FolderHelper`

```csharp
public static class TabularEditor.TOMWrapper.FolderHelper

```

静态方法

| 类型                       | 姓名                                                                                                             | 摘要 |
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

## `层次结构`

Hierarchy 的基类声明

```csharp
public class TabularEditor.TOMWrapper.Hierarchy
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IDescriptionObject, IAnnotationObject, ITabularObjectContainer, ITabularPerspectiveObject

```

属性

| 类型                   | 姓名             | 摘要                             |
| -------------------- | -------------- | ------------------------------ |
| `String`             | 说明             | 获取或设置 Hierarchy 的描述。           |
| `String`             | DisplayFolder  | 获取或设置 Hierarchy 的显示文件夹。        |
| `透视Indexer`          | In透视           |                                |
| `Boolean`            | IsHidden       | 获取或设置 Hierarchy 是否隐藏。          |
| `LevelCollection`    | 级别             |                                |
| `层次结构`               | MetadataObject |                                |
| `Boolean`            | Reordering     | 当要将多个级别作为一次操作重新排序时，将此项设为 true。 |
| `ObjectState`        | 状态             | 获取或设置此层次结构的状态。                 |
| `Table`              | 表              |                                |
| `TranslationIndexer` | 翻译后的说明         | 该层次结构的本地化说明集合。                 |
| `TranslationIndexer` | 翻译后的显示文件夹      | 该层次结构的本地化显示文件夹集合。              |

方法

| 类型                                 | 姓名                                                                                                | 摘要 |
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

用于 Hierarchy 的集合类。提供便捷属性，可一次性在多个对象上设置同一属性。

```csharp
public class TabularEditor.TOMWrapper.HierarchyCollection
    : TabularObjectCollection<Hierarchy, Hierarchy, Table>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Hierarchy>, IEnumerable<Hierarchy>, IList<Hierarchy>, ITabularObjectCollection, IExpandableIndexer

```

属性

| 类型        | 姓名            | 摘要 |
| --------- | ------------- | -- |
| `String`  | 说明            |    |
| `String`  | DisplayFolder |    |
| `Boolean` | IsHidden      |    |
| `表`       | Parent        |    |

方法

| 类型       | 姓名                            | 摘要 |
| -------- | ----------------------------- | -- |
| `String` | ToString() |    |

## `HierarchyColumnConverter`

```csharp
public class TabularEditor.TOMWrapper.HierarchyColumnConverter
    : TableColumnConverter

```

方法

| 类型        | 姓名                                                                              | 摘要 |
| --------- | ------------------------------------------------------------------------------- | -- |
| `Boolean` | GetStandardValuesExclusive(`ITypeDescriptorContext` context) |    |
| `Boolean` | IsValid(`ITypeDescriptorContext` context, `Object` value)    |    |

## `IAnnotationObject`

```csharp
public interface TabularEditor.TOMWrapper.IAnnotationObject
    : ITabularObject, INotifyPropertyChanged

```

方法

| 类型       | 姓名                                                                                         | 摘要 |
| -------- | ------------------------------------------------------------------------------------------ | -- |
| `String` | GetAnnotation(`String` name)                                            |    |
| `void`   | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |    |

## `IClonableObject`

```csharp
public interface TabularEditor.TOMWrapper.IClonableObject

```

方法

| 类型                   | 姓名                                                                        | 摘要 |
| -------------------- | ------------------------------------------------------------------------- | -- |
| `TabularNamedObject` | Clone(`String` newName, `Boolean` includeTranslations) |    |

## `IDaxObject`

```csharp
public interface TabularEditor.TOMWrapper.IDaxObject
    : ITabularNamedObject, ITabularObject, INotifyPropertyChanged

```

属性

| 类型                           | 姓名                | 摘要 |
| ---------------------------- | ----------------- | -- |
| `String`                     | DaxObjectFullName |    |
| `String`                     | DaxObjectName     |    |
| `String`                     | DaxTableName      |    |
| `HashSet<IExpressionObject>` | 依赖项               |    |

## `IDescriptionObject`

可带有描述的对象

```csharp
public interface TabularEditor.TOMWrapper.IDescriptionObject

```

属性

| 类型                   | 姓名                     | 摘要 |
| -------------------- | ---------------------- | -- |
| `String`             | 说明                     |    |
| `TranslationIndexer` | TranslatedDescriptions |    |

## `IDetailObject`

表示可包含在显示文件夹中的对象。例如：度量值、列、层次结构和文件夹

```csharp
public interface TabularEditor.TOMWrapper.IDetailObject
    : ITabularTableObject, ITabularNamedObject, ITabularObject, INotifyPropertyChanged

```

属性

| 类型                   | 姓名                       | 摘要 |
| -------------------- | ------------------------ | -- |
| `String`             | DisplayFolder            |    |
| `TranslationIndexer` | TranslatedDisplayFolders |    |

## `IDetailObjectContainer`

表示一个既可包含其他对象，也可包含显示文件夹的对象。示例：* 文件夹
* 表

```csharp
public interface TabularEditor.TOMWrapper.IDetailObjectContainer
    : ITabularNamedObject, ITabularObject, INotifyPropertyChanged

```

属性

| 类型      | 姓名          | 摘要 |
| ------- | ----------- | -- |
| `Table` | ParentTable |    |

方法

| 类型                           | 姓名                                                                   | 摘要 |
| ---------------------------- | -------------------------------------------------------------------- | -- |
| `IEnumerable<IDetailObject>` | GetChildrenByFolders(`Boolean` recursive = False) |    |

## `IErrorMessageObject`

可包含错误信息的对象

```csharp
public interface TabularEditor.TOMWrapper.IErrorMessageObject

```

属性

| 类型       | 姓名           | 摘要 |
| -------- | ------------ | -- |
| `String` | ErrorMessage |    |

## `IExpressionObject`

```csharp
public interface TabularEditor.TOMWrapper.IExpressionObject
    : IDaxObject, ITabularNamedObject, ITabularObject, INotifyPropertyChanged

```

属性

| 类型                                         | 姓名              | 摘要 |
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

| 类型        | 姓名       | 摘要 |
| --------- | -------- | -- |
| `Boolean` | IsHidden |    |

## `IntelliSenseAttribute`

```csharp
public class TabularEditor.TOMWrapper.IntelliSenseAttribute
    : Attribute, _Attribute

```

属性

| 类型       | 姓名 | 摘要 |
| -------- | -- | -- |
| `String` | 说明 |    |

## `ITabularNamedObject`

```csharp
public interface TabularEditor.TOMWrapper.ITabularNamedObject
    : ITabularObject, INotifyPropertyChanged

```

属性

| 类型                   | 姓名              | 摘要 |
| -------------------- | --------------- | -- |
| `Int32`              | MetadataIndex   |    |
| `String`             | 姓名              |    |
| `TranslationIndexer` | TranslatedNames |    |

## `ITabularObject`

```csharp
public interface TabularEditor.TOMWrapper.ITabularObject
    : INotifyPropertyChanged

```

属性

| 类型     | 姓名   | 摘要 |
| ------ | ---- | -- |
| `模型`   | 模型   |    |
| `对象类型` | 对象类型 |    |

## `ITabularObjectCollection`

```csharp
public interface TabularEditor.TOMWrapper.ITabularObjectCollection
    : IEnumerable

```

属性

| 类型                    | 姓名             | 摘要 |
| --------------------- | -------------- | -- |
| `String`              | CollectionName |    |
| `TabularModelHandler` | Handler        |    |
| `IEnumerable<String>` | Keys           |    |

方法

| 类型                         | 姓名                                                   | 摘要 |
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

| 类型                                 | 姓名                               | 摘要 |
| ---------------------------------- | -------------------------------- | -- |
| `IEnumerable<ITabularNamedObject>` | GetChildren() |    |

## `ITabularPerspectiveObject`

可在各个单独的透视中显示或隐藏的对象

```csharp
public interface TabularEditor.TOMWrapper.ITabularPerspectiveObject
    : IHideableObject

```

属性

| 类型                   | 姓名            | 摘要 |
| -------------------- | ------------- | -- |
| `PerspectiveIndexer` | InPerspective |    |

## `ITabularTableObject`

属于特定表的对象。

```csharp
public interface TabularEditor.TOMWrapper.ITabularTableObject
    : ITabularNamedObject, ITabularObject, INotifyPropertyChanged

```

属性

| 类型      | 姓名 | 摘要 |
| ------- | -- | -- |
| `Table` | 表  |    |

方法

| 类型     | 姓名                          | 摘要 |
| ------ | --------------------------- | -- |
| `void` | Delete() |    |

## `KPI`

KPI 的基类声明

```csharp
public class TabularEditor.TOMWrapper.KPI
    : TabularObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, IDescriptionObject, IAnnotationObject, IDynamicPropertyObject

```

属性

| 类型                   | 姓名                     | 摘要                                 |
| -------------------- | ---------------------- | ---------------------------------- |
| `String`             | 说明                     | 获取或设置 KPI 的描述。                     |
| `度量值`                | 度量值                    | 获取或设置 KPI 的度量值。                    |
| `KPI`                | MetadataObject         |                                    |
| `String`             | StatusDescription      | 获取或设置 KPI 的状态描述。                   |
| `String`             | StatusExpression       | 获取或设置 KPI 的状态表达式。                  |
| `String`             | StatusGraphic          | 获取或设置 KPI 的状态图标。                   |
| `String`             | TargetDescription      | 获取或设置 KPI 的目标描述。                   |
| `String`             | TargetExpression       | 获取或设置 KPI 的 TargetExpression 属性。   |
| `String`             | TargetFormatString     | 获取或设置 KPI 的 TargetFormatString 属性。 |
| `TranslationIndexer` | TranslatedDescriptions | 此 KPI 的本地化描述集合。                    |
| `String`             | TrendDescription       | 获取或设置 KPI 的 TrendDescription 属性。   |
| `String`             | TrendExpression        | 获取或设置 KPI 的 TrendExpression 属性。    |
| `String`             | TrendGraphic           | 获取或设置 KPI 的 TrendGraphic 属性。       |

方法

| 类型        | 姓名                                                                                         | 摘要 |
| --------- | ------------------------------------------------------------------------------------------ | -- |
| `Boolean` | Browsable(`String` propertyName)                                        |    |
| `Boolean` | Editable(`String` propertyName)                                         |    |
| `String`  | GetAnnotation(`String` name)                                            |    |
| `void`    | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |    |

## `级别`

Level 的基类定义

```csharp
public class TabularEditor.TOMWrapper.Level
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject, ITabularTableObject

```

属性

| 类型                   | 姓名                     | 摘要             |
| -------------------- | ---------------------- | -------------- |
| `列`                  | 列                      | 获取或设置该级别的列。    |
| `String`             | 说明                     | 获取或设置该级别的描述。   |
| `层次结构`               | 层次结构                   | 获取或设置该级别的层次结构。 |
| `级别`                 | MetadataObject         |                |
| `Int32`              | 序号                     | 获取或设置该级别的序号。   |
| `表`                  | 表                      |                |
| `TranslationIndexer` | TranslatedDescriptions | 此级别的本地化描述集合。   |

方法

| 类型       | 姓名                                                                                                                      | 摘要           |
| -------- | ----------------------------------------------------------------------------------------------------------------------- | ------------ |
| `void`   | Delete()                                                                                             | 从层次结构中删除该级别。 |
| `String` | GetAnnotation(`String` name)                                                                         |              |
| `void`   | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue)                       |              |
| `void`   | OnPropertyChanging(`String` propertyName, `Object` newValue, `Boolean&` undoable, `Boolean&` cancel) |              |
| `void`   | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True)                              |              |
| `void`   | Undelete(`ITabularObjectCollection` collection)                                                      |              |

## `LevelCollection`

Level 的集合类。提供便捷属性，可一次为多个对象设置同一属性。

```csharp
public class TabularEditor.TOMWrapper.LevelCollection
    : TabularObjectCollection<Level, Level, Hierarchy>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Level>, IEnumerable<Level>, IList<Level>, ITabularObjectCollection, IExpandableIndexer

```

属性

| 类型          | 姓名 | 摘要 |
| ----------- | -- | -- |
| `String`    | 说明 |    |
| `Hierarchy` | 父级 |    |

方法

| 类型        | 姓名                                      | 摘要 |
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

| 类型                   | 姓名              | 摘要 |
| -------------------- | --------------- | -- |
| `Int32`              | MetadataIndex   |    |
| `模型`                 | 模型              |    |
| `String`             | 姓名              |    |
| `ObjectType`         | ObjectType      |    |
| `TranslationIndexer` | TranslatedNames |    |

事件

| 类型                            | 姓名              | 摘要 |
| ----------------------------- | --------------- | -- |
| `PropertyChangedEventHandler` | PropertyChanged |    |

方法

| 类型                                 | 姓名                               | 摘要 |
| ---------------------------------- | -------------------------------- | -- |
| `IEnumerable<ITabularNamedObject>` | GetChildren() |    |

## `LogicalTreeOptions`

```csharp
public enum TabularEditor.TOMWrapper.LogicalTreeOptions
    : Enum, IComparable, IFormattable, IConvertible

```

枚举

| 值     | 姓名             | 摘要 |
| ----- | -------------- | -- |
| `1`   | DisplayFolders |    |
| `2`   | 列              |    |
| `4`   | 度量值            |    |
| `8`   | KPI            |    |
| `16`  | 层次结构           |    |
| `32`  | 级别             |    |
| `64`  | ShowHidden     |    |
| `128` | AllObjectTypes |    |
| `256` | ShowRoot       |    |
| `447` | 默认值            |    |

## `度量值`

度量值的基类声明

```csharp
public class TabularEditor.TOMWrapper.Measure
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IErrorMessageObject, IDescriptionObject, IExpressionObject, IDaxObject, IAnnotationObject, ITabularPerspectiveObject, IDynamicPropertyObject, IClonableObject

```

属性

| 类型                                         | 姓名                       | 摘要                            |
| ------------------------------------------ | ------------------------ | ----------------------------- |
| `DataType`                                 | 数据类型                     | 获取或设置该度量值的 DataType。          |
| `String`                                   | DaxObjectFullName        |                               |
| `String`                                   | DaxObjectName            |                               |
| `String`                                   | DaxTableName             |                               |
| `HashSet<IExpressionObject>`               | Dependants               |                               |
| `Dictionary<IDaxObject, List<Dependency>>` | Dependencies             |                               |
| `String`                                   | 说明                       | 获取或设置度量值的描述。                  |
| `String`                                   | DisplayFolder            | 获取或设置度量值的显示文件夹。               |
| `String`                                   | ErrorMessage             | 获取或设置度量值的错误消息。                |
| `String`                                   | 表达式                      | 获取或设置度量值的表达式。                 |
| `String`                                   | 格式字符串                    | 获取或设置度量值的格式字符串。               |
| `透视Indexer`                                | In透视                     |                               |
| `Boolean`                                  | IsHidden                 | 获取或设置度量值的 IsHidden 属性。        |
| `Boolean`                                  | IsSimpleMeasure          | 获取或设置度量值的 IsSimpleMeasure 属性。 |
| `KPI`                                      | KPI                      | 获取或设置度量值的 KPI 属性。             |
| `度量值`                                      | MetadataObject           |                               |
| `Boolean`                                  | NeedsValidation          |                               |
| `ObjectState`                              | State                    | 获取或设置度量值的 State 属性。           |
| `Table`                                    | 表                        |                               |
| `翻译Indexer`                                | TranslatedDescriptions   | 此度量值的本地化描述集合。                 |
| `翻译Indexer`                                | TranslatedDisplayFolders | 此度量值的本地化显示文件夹集合。              |

方法

| 类型                   | 姓名                                                                                                                      | 摘要 |
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

## `MeasureCollection`

Measure 的集合类。提供便捷的属性，支持一次为多个对象设置同一属性。

```csharp
public class TabularEditor.TOMWrapper.MeasureCollection
    : TabularObjectCollection<Measure, Measure, Table>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Measure>, IEnumerable<Measure>, IList<Measure>, ITabularObjectCollection, IExpandableIndexer

```

属性

| 类型        | 姓名              | 摘要 |
| --------- | --------------- | -- |
| `String`  | 说明              |    |
| `String`  | DisplayFolder   |    |
| `String`  | 表达式             |    |
| `String`  | 格式字符串           |    |
| `Boolean` | IsHidden        |    |
| `Boolean` | IsSimpleMeasure |    |
| `KPI`     | KPI             |    |
| `Table`   | Parent          |    |

方法

| 类型       | 姓名                            | 摘要 |
| -------- | ----------------------------- | -- |
| `String` | ToString() |    |

## `Model`

Model 的基类声明

```csharp
public class TabularEditor.TOMWrapper.Model
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject, ITabularObjectContainer

```

字段

| 类型             | 姓名                    | 摘要 |
| -------------- | --------------------- | -- |
| `LogicalGroup` | GroupDataSources      |    |
| `LogicalGroup` | GroupPerspectives 透视  |    |
| `LogicalGroup` | GroupRelationships 关系 |    |
| `LogicalGroup` | GroupRoles 角色         |    |
| `LogicalGroup` | GroupTables           |    |
| `LogicalGroup` | GroupTranslations 翻译  |    |

属性

| 类型                           | 姓名                     | 摘要                           |
| ---------------------------- | ---------------------- | ---------------------------- |
| `IEnumerable<Column>`        | AllColumns             |                              |
| `IEnumerable<Hierarchy>`     | AllHierarchies         |                              |
| `IEnumerable<Level>`         | AllLevels              |                              |
| `IEnumerable<Measure>`：度量值集合 | AllMeasures 所有度量值      |                              |
| `String`                     | 排序规则                   | 获取或设置模型的排序规则。                |
| `String`                     | 区域设置                   | 获取或设置模型的区域设置。                |
| `区域设置集合`                     | 区域设置集合                 |                              |
| `Database`                   | 数据库                    |                              |
| `DataSourceCollection`       | 数据源集合                  |                              |
| `DataViewType`               | DefaultDataView        | 获取或设置模型的DefaultDataView。     |
| `ModeType`                   | 默认模式                   | 获取或设置模型的默认模式。                |
| `String`                     | 说明                     | 获取或设置模型的说明。                  |
| `Boolean`                    | 是否有本地更改                | 获取或设置模型是否有本地更改。              |
| `IEnumerable<LogicalGroup>`  | 逻辑子组                   |                              |
| `Model`                      | 元数据对象                  |                              |
| `透视集合`                       | 透视                     |                              |
| `RelationshipCollection2`    | 关系                     |                              |
| `模型角色集合`                     | 角色                     |                              |
| `String`                     | StorageLocation        | 获取或设置模型的 StorageLocation 属性。 |
| `TableCollection`            | 表                      |                              |
| `翻译索引器`                      | TranslatedDescriptions | 此模型的本地化描述集合。                 |

方法

| 类型                                 | 姓名                                                                                         | 摘要 |
| ---------------------------------- | ------------------------------------------------------------------------------------------ | -- |
| `CalculatedTable`                  | AddCalculatedTable()                                                    |    |
| `透视`                               | Add透视(`String` name = null)                                             |    |
| `单列关系`                             | Add关系()                                                                 |    |
| `模型角色`                             | Add角色(`String` name = null)                                             |    |
| `Table`                            | AddTable()                                                              |    |
| `区域设置`                             | AddTranslation(`String` cultureId)                                      |    |
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

| 类型                   | 姓名                     | 摘要                                    |
| -------------------- | ---------------------- | ------------------------------------- |
| `String`             | 说明                     | 获取或设置 ModelRole 的 Description 属性。     |
| `ModelRole`          | MetadataObject         |                                       |
| `ModelPermission`    | ModelPermission        | 获取或设置 ModelRole 的 ModelPermission 属性。 |
| `RoleRLSIndexer`     | RowLevelSecurity       |                                       |
| `TranslationIndexer` | TranslatedDescriptions | 此模型角色的本地化描述集合。                        |

方法

| 类型                   | 姓名                                                                                         | 摘要 |
| -------------------- | ------------------------------------------------------------------------------------------ | -- |
| `TabularNamedObject` | Clone(`String` newName, `Boolean` includeTranslations) 包括翻译             |    |
| `void`               | Delete()                                                                |    |
| `String`             | GetAnnotation(`String` name)                                            |    |
| `void`               | InitRLSIndexer()                                                        |    |
| `void`               | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |    |
| `void`               | Undelete(`ITabularObjectCollection` collection)                         |    |

## `ModelRoleCollection` 模型角色集合

模型角色的集合类。提供便捷的属性，便于一次为多个对象设置同一属性。

```csharp
public class TabularEditor.TOMWrapper.ModelRoleCollection
    : TabularObjectCollection<ModelRole, ModelRole, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<ModelRole>, IEnumerable<ModelRole>, IList<ModelRole>, ITabularObjectCollection, IExpandableIndexer

```

属性

| 类型                | 姓名              | 摘要 |
| ----------------- | --------------- | -- |
| `String`          | 说明              |    |
| `ModelPermission` | ModelPermission |    |
| `模型`              | 父级              |    |

方法

| 类型       | 姓名                            | 摘要 |
| -------- | ----------------------------- | -- |
| `String` | ToString() |    |

## `NullTree`

```csharp
public class TabularEditor.TOMWrapper.NullTree
    : TabularTree, INotifyPropertyChanged

```

方法

| 类型     | 姓名                                                                                       | 摘要 |
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

| 值   | 姓名    | 摘要 |
| --- | ----- | -- |
| `0` | 按字母顺序 |    |
| `1` | 元数据   |    |

## `ObjectType`

```csharp
public enum TabularEditor.TOMWrapper.ObjectType
    : Enum, IComparable, IFormattable, IConvertible

```

枚举

| 值      | 姓名     | 摘要 |
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
| `35`   | 角色成员   |    |
| `36`   | 表权限    |    |
| `1000` | 数据库    |    |

## `分区`

分区的基类声明

```csharp
public class TabularEditor.TOMWrapper.Partition
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDynamicPropertyObject, IErrorMessageObject, ITabularTableObject, IDescriptionObject, IAnnotationObject

```

属性

| 类型             | 姓名                     | 摘要                      |
| -------------- | ---------------------- | ----------------------- |
| `DataSource`   | DataSource             |                         |
| `DataViewType` | DataView               | 获取或设置分区的数据视图。           |
| `String`       | 说明                     | 获取或设置分区的描述。             |
| `String`       | 错误信息                   | 获取或设置分区的错误信息。           |
| `String`       | 表达式                    |                         |
| `分区`           | MetadataObject         |                         |
| `ModeType`     | 模式                     | 获取或设置分区的模式。             |
| `String`       | 姓名                     |                         |
| `String`       | Query                  |                         |
| `DateTime`     | RefreshedTime          |                         |
| `String`       | Source                 |                         |
| `分区SourceType` | SourceType             | 获取或设置分区的 SourceType 属性。 |
| `ObjectState`  | State                  | 获取或设置分区的 State 属性。      |
| `Table`        | 表                      |                         |
| `翻译Indexer`    | TranslatedDescriptions | 该分区的本地化描述集合。            |

方法

| 类型        | 姓名                                                                                         | 摘要 |
| --------- | ------------------------------------------------------------------------------------------ | -- |
| `Boolean` | Browsable(`String` propertyName)                                        |    |
| `Boolean` | Editable(`String` propertyName)                                         |    |
| `String`  | GetAnnotation(`String` name)                                            |    |
| `void`    | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |    |
| `void`    | Undelete(`ITabularObjectCollection` collection)                         |    |

## `分区Collection`

分区的集合类。提供便捷属性，便于一次性在多个对象上设置同一属性。

```csharp
public class TabularEditor.TOMWrapper.PartitionCollection
    : TabularObjectCollection<Partition, Partition, Table>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Partition>, IEnumerable<Partition>, IList<Partition>, ITabularObjectCollection, IExpandableIndexer

```

属性

| 类型             | 姓名       | 摘要 |
| -------------- | -------- | -- |
| `DataViewType` | DataView |    |
| `String`       | 说明       |    |
| `ModeType`     | 模式       |    |
| `Table`        | 父级       |    |

方法

| 类型       | 姓名                            | 摘要 |
| -------- | ----------------------------- | -- |
| `String` | ToString() |    |

## `透视`

透视的基类声明

```csharp
public class TabularEditor.TOMWrapper.Perspective
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject

```

属性

| 类型       | 姓名                     | 摘要           |
| -------- | ---------------------- | ------------ |
| `String` | 说明                     | 获取或设置透视的描述。  |
| `透视`     | MetadataObject         |              |
| `翻译索引器`  | TranslatedDescriptions | 此透视的本地化描述集合。 |

方法

| 类型                   | 姓名                                                                                         | 摘要 |
| -------------------- | ------------------------------------------------------------------------------------------ | -- |
| `TabularNamedObject` | Clone(`String` newName, `Boolean` includeTranslations)                  |    |
| `void`               | Delete()                                                                |    |
| `String`             | GetAnnotation(`String` name)                                            |    |
| `void`               | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |    |
| `void`               | Undelete(`ITabularObjectCollection` collection)                         |    |

## `PerspectiveCollection` 透视集合

透视集合类。提供便捷属性，可同时在多个对象上设置某个属性。

```csharp
public class TabularEditor.TOMWrapper.PerspectiveCollection
    : TabularObjectCollection<Perspective, Perspective, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Perspective>, IEnumerable<Perspective>, IList<Perspective>, ITabularObjectCollection, IExpandableIndexer

```

属性

| 类型       | 姓名 | 摘要 |
| -------- | -- | -- |
| `String` | 说明 |    |
| `Model`  | 父级 |    |

方法

| 类型       | 姓名                            | 摘要 |
| -------- | ----------------------------- | -- |
| `String` | ToString() |    |

## `透视ColumnIndexer`

```csharp
public class TabularEditor.TOMWrapper.PerspectiveColumnIndexer
    : PerspectiveIndexer, IEnumerable<Boolean>, IEnumerable, IExpandableIndexer

```

属性

| 类型  | 姓名 | 摘要 |
| --- | -- | -- |
| `列` | 列  |    |

方法

| 类型     | 姓名                                                                        | 摘要 |
| ------ | ------------------------------------------------------------------------- | -- |
| `void` | Refresh()                                              |    |
| `void` | SetInPerspective(`透视` perspective, `Boolean` included) |    |

## `透视HierarchyIndexer`

```csharp
public class TabularEditor.TOMWrapper.PerspectiveHierarchyIndexer
    : PerspectiveIndexer, IEnumerable<Boolean>, IEnumerable, IExpandableIndexer

```

属性

| 类型     | 姓名   | 摘要 |
| ------ | ---- | -- |
| `层次结构` | 层次结构 |    |

方法

| 类型     | 姓名                                                                        | 摘要 |
| ------ | ------------------------------------------------------------------------- | -- |
| `void` | Refresh()                                              |    |
| `void` | SetInPerspective(`透视` perspective, `Boolean` included) |    |

## `透视Indexer`

```csharp
public abstract class TabularEditor.TOMWrapper.PerspectiveIndexer
    : IEnumerable<Boolean>, IEnumerable, IExpandableIndexer

```

字段

| 类型                   | 姓名            | 摘要 |
| -------------------- | ------------- | -- |
| `TabularNamedObject` | TabularObject |    |

属性

| 类型                                 | 姓名   | 摘要 |
| ---------------------------------- | ---- | -- |
| `Boolean`                          | 项    |    |
| `Boolean`                          | 项    |    |
| `IEnumerable<String>`              | 键    |    |
| `Dictionary<Perspective, Boolean>` | 透视映射 |    |
| `String`                           | 摘要   |    |

方法

| 类型                            | 姓名                                                                        | 摘要            |
| ----------------------------- | ------------------------------------------------------------------------- | ------------- |
| `void`                        | All()                                                  | 将该对象包含在所有透视中。 |
| `Dictionary<String, Boolean>` | Copy()                                                 |               |
| `void`                        | CopyFrom(`透视Indexer` source)                           |               |
| `void`                        | CopyFrom(`IDictionary<String, Boolean>` source)        |               |
| `String`                      | GetDisplayName(`String` key)                           |               |
| `IEnumerator<Boolean>`        | GetEnumerator()                                        |               |
| `void`                        | None()                                                 |               |
| `void`                        | Refresh()                                              |               |
| `void`                        | SetInPerspective(`透视` perspective, `Boolean` included) |               |

## `透视度量值Indexer`

```csharp
public class TabularEditor.TOMWrapper.PerspectiveMeasureIndexer
    : PerspectiveIndexer, IEnumerable<Boolean>, IEnumerable, IExpandableIndexer

```

属性

| 类型    | 姓名  | 摘要 |
| ----- | --- | -- |
| `度量值` | 度量值 |    |

方法

| 类型     | 姓名                                                                        | 摘要 |
| ------ | ------------------------------------------------------------------------- | -- |
| `void` | Refresh()                                              |    |
| `void` | SetInPerspective(`透视` perspective, `Boolean` included) |    |

## `透视TableIndexer`

```csharp
public class TabularEditor.TOMWrapper.PerspectiveTableIndexer
    : PerspectiveIndexer, IEnumerable<Boolean>, IEnumerable, IExpandableIndexer

```

属性

| 类型        | 姓名   | 摘要 |
| --------- | ---- | -- |
| `Boolean` | Item |    |
| `Table`   | 表    |    |

方法

| 类型        | 姓名                                                                        | 摘要 |
| --------- | ------------------------------------------------------------------------- | -- |
| `透视Table` | EnsurePTExists(`透视` perspective)                       |    |
| `void`    | Refresh()                                              |    |
| `void`    | SetInPerspective(`透视` perspective, `Boolean` included) |    |

## `ProviderDataSource`

ProviderDataSource 的基类声明

```csharp
public class TabularEditor.TOMWrapper.ProviderDataSource
    : DataSource, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject, IDynamicPropertyObject

```

属性

| 类型                    | 姓名                | 摘要                                               |
| --------------------- | ----------------- | ------------------------------------------------ |
| `String`              | Account           | 获取或设置 ProviderDataSource 的 Account 属性。           |
| `String`              | ConnectionString  | 获取或设置 ProviderDataSource 的 ConnectionString 属性。  |
| `ImpersonationMode`   | ImpersonationMode | 获取或设置 ProviderDataSource 的 ImpersonationMode 属性。 |
| `DatasourceIsolation` | Isolation         | 获取或设置 ProviderDataSource 的 Isolation 属性。         |
| `Boolean`             | IsPowerBIMashup   |                                                  |
| `String`              | 地点                |                                                  |
| `Int32`               | MaxConnections    | 获取或设置 ProviderDataSource 的 MaxConnections 属性。    |
| `ProviderDataSource`  | MetadataObject    |                                                  |
| `String`              | MQuery            |                                                  |
| `String`              | 姓名                |                                                  |
| `String`              | Password          | 获取或设置 ProviderDataSource 的 Password 属性。          |
| `String`              | Provider          | 获取或设置 ProviderDataSource 的 Provider 属性。          |
| `String`              | SourceID          |                                                  |
| `Int32`               | Timeout           | 获取或设置 ProviderDataSource 的 Timeout 属性。           |

方法

| 类型        | 姓名                                                  | 摘要 |
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

| 类型                          | 姓名                         | 摘要                                    |
| --------------------------- | -------------------------- | ------------------------------------- |
| `CrossFilteringBehavior`    | CrossFilteringBehavior     | 获取或设置关系的 CrossFilteringBehavior 属性。   |
| `Table`                     | FromTable                  | 获取或设置关系的 FromTable 属性。                |
| `Boolean`                   | IsActive                   | 获取或设置关系的 IsActive 属性。                 |
| `DateTime关系行为`              | JoinOnDateBehavior         | 获取或设置该关系的 JoinOnDateBehavior。         |
| `关系`                        | MetadataObject             |                                       |
| `Boolean`                   | RelyOnReferentialIntegrity | 获取或设置该关系的 RelyOnReferentialIntegrity。 |
| `SecurityFilteringBehavior` | SecurityFilteringBehavior  | 获取或设置该关系的 SecurityFilteringBehavior。  |
| `ObjectState`               | State                      | 获取或设置该关系的 State。                      |
| `Table`                     | ToTable                    | 获取或设置该关系的 ToTable。                    |
| `关系类型`                      | Type                       | 获取或设置该关系的 Type。                       |

方法

| 类型       | 姓名                                                                                         | 摘要 |
| -------- | ------------------------------------------------------------------------------------------ | -- |
| `String` | GetAnnotation(`String` name)                                            |    |
| `void`   | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |    |

## `RelationshipCollection`

用于表示“关系”的集合类。提供一些便捷属性，可一次为多个对象设置同一属性。

```csharp
public class TabularEditor.TOMWrapper.RelationshipCollection
    : TabularObjectCollection<Relationship, Relationship, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Relationship>, IEnumerable<Relationship>, IList<Relationship>, ITabularObjectCollection, IExpandableIndexer

```

属性

| 类型                             | 姓名                         | 摘要 |
| ------------------------------ | -------------------------- | -- |
| `CrossFilteringBehavior`       | CrossFilteringBehavior     |    |
| `Boolean`                      | IsActive                   |    |
| `DateTimeRelationshipBehavior` | JoinOnDateBehavior         |    |
| `Model`                        | Parent                     |    |
| `Boolean`                      | RelyOnReferentialIntegrity |    |
| `SecurityFilteringBehavior`    | SecurityFilteringBehavior  |    |

方法

| 类型       | 姓名                            | 摘要 |
| -------- | ----------------------------- | -- |
| `String` | ToString() |    |

## `RelationshipCollection2`

```csharp
public class TabularEditor.TOMWrapper.RelationshipCollection2
    : TabularObjectCollection<SingleColumnRelationship, Relationship, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<SingleColumnRelationship>, IEnumerable<SingleColumnRelationship>, IList<SingleColumnRelationship>, ITabularObjectCollection, IExpandableIndexer

```

属性

| 类型                             | 姓名                         | 摘要 |
| ------------------------------ | -------------------------- | -- |
| `CrossFilteringBehavior`       | CrossFilteringBehavior     |    |
| `Boolean`                      | IsActive                   |    |
| `DateTimeRelationshipBehavior` | JoinOnDateBehavior         |    |
| `模型`                           | Parent                     |    |
| `Boolean`                      | RelyOnReferentialIntegrity |    |
| `SecurityFilteringBehavior`    | SecurityFilteringBehavior  |    |

方法

| 类型       | 姓名                            | 摘要 |
| -------- | ----------------------------- | -- |
| `String` | ToString() |    |

## `RoleRLSIndexer`

RoleRLSIndexer 用于在模型中针对某个特定角色浏览所有表上的全部筛选器。相比之下，TableRLSIndexer 用于针对某个特定表浏览模型中所有角色的筛选器。

```csharp
public class TabularEditor.TOMWrapper.RoleRLSIndexer
    : IEnumerable<String>, IEnumerable, IExpandableIndexer

```

字段

| 类型          | 姓名 | 摘要 |
| ----------- | -- | -- |
| `ModelRole` | 角色 |    |

属性

| 类型                          | 姓名     | 摘要 |
| --------------------------- | ------ | -- |
| `String`                    | 项      |    |
| `String`                    | 项      |    |
| `IEnumerable<String>`       | 键      |    |
| `Dictionary<Table, String>` | RLSMap |    |
| `String`                    | 摘要     |    |

方法

| 类型                    | 姓名                                                                  | 摘要 |
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

| 类型                | 姓名                       | 摘要 |
| ----------------- | ------------------------ | -- |
| `Boolean`         | IgnoreInferredObjects    |    |
| `Boolean`         | IgnoreInferredProperties |    |
| `Boolean`         | IgnoreTimestamps         |    |
| `HashSet<String>` | 级别                       |    |
| `Boolean`         | PrefixFilenames          |    |
| `Boolean`         | SplitMultilineStrings    |    |

静态属性

| 类型                 | 姓名  | 摘要 |
| ------------------ | --- | -- |
| `SerializeOptions` | 默认值 |    |

## `SingleColumnRelationship`

SingleColumnRelationship 的基类声明

```csharp
public class TabularEditor.TOMWrapper.SingleColumnRelationship
    : Relationship, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IAnnotationObject, IDynamicPropertyObject

```

属性

| 类型                                 | 姓名              | 摘要                                                   |
| ---------------------------------- | --------------- | ---------------------------------------------------- |
| `RelationshipEndCardinality`：关系端基数 | FromCardinality | 获取或设置 SingleColumnRelationship 的 FromCardinality 属性。 |
| `列`                                | FromColumn      | 获取或设置 SingleColumnRelationship 的 FromColumn 属性。      |
| `SingleColumnRelationship`：单列关系    | MetadataObject  |                                                      |
| `String`                           | 姓名              |                                                      |
| `RelationshipEndCardinality`：关系端基数 | ToCardinality   | 获取或设置 SingleColumnRelationship 的 ToCardinality 属性。   |
| `列`                                | ToColumn        | 获取或设置 SingleColumnRelationship 的 ToColumn 属性。        |

方法

| 类型        | 姓名                                                                                                                      | 摘要 |
| --------- | ----------------------------------------------------------------------------------------------------------------------- | -- |
| `Boolean` | Browsable(`String` propertyName)                                                                     |    |
| `void`    | Delete()                                                                                             |    |
| `Boolean` | Editable(`String` propertyName)                                                                      |    |
| `void`    | Init()                                                                                               |    |
| `void`    | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue)                       |    |
| `void`    | OnPropertyChanging(`String` propertyName, `Object` newValue, `Boolean&` undoable, `Boolean&` cancel) |    |
| `String`  | ToString()                                                                                           |    |
| `void`    | Undelete(`ITabularObjectCollection` collection)                                                      |    |

## `表`

Table 的基类声明

```csharp
public class TabularEditor.TOMWrapper.Table
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IHideableObject, IDescriptionObject, IAnnotationObject, ITabularObjectContainer, IDetailObjectContainer, ITabularPerspectiveObject, IDaxObject, IDynamicPropertyObject, IErrorMessageObject

```

属性

| 类型                           | 姓名                | 摘要                      |
| ---------------------------- | ----------------- | ----------------------- |
| `IEnumerable<Level>`         | AllLevels         |                         |
| `ColumnCollection`           | 列                 |                         |
| `String`                     | DataCategory      | 获取或设置表的 DataCategory。   |
| `String`                     | DaxObjectFullName |                         |
| `String`                     | DaxObjectName     |                         |
| `String`                     | DaxTableName      |                         |
| `HashSet<IExpressionObject>` | Dependants        |                         |
| `String`                     | 说明                | 获取或设置表的 Description 属性。 |
| `String`                     | 错误信息              |                         |
| `HierarchyCollection`        | 层次结构              |                         |
| `透视索引器`                      | 在透视中              |                         |
| `Boolean`                    | IsHidden          | 获取或设置表的 IsHidden 属性。    |
| `度量值集合`                      | 度量值               |                         |
| `Table`                      | MetadataObject    |                         |
| `String`                     | 姓名                |                         |
| `Table`                      | ParentTable       |                         |
| `分区集合`                       | 分区                |                         |
| `TableRLSIndexer`            | RowLevelSecurity  |                         |
| `String`                     | Source            |                         |
| `分区源类型`                      | 源类型               |                         |
| `TranslationIndexer`         | 翻译后的描述            | 此表的本地化描述集合。             |

方法

| 类型                                 | 姓名                                                                                                                        | 摘要                  |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------- |
| `CalculatedColumn`                 | AddCalculatedColumn(`String` name = null, `String` expression = null, `String` displayFolder = null)   |                     |
| `DataColumn`                       | AddDataColumn(`String` name = null, `String` sourceColumn = null, `String` displayFolder = null)       |                     |
| `层次结构`                             | AddHierarchy(`String` name = null, `String` displayFolder = null, `Column[]` levels)                   |                     |
| `层次结构`                             | AddHierarchy(`String` name, `String` displayFolder = null, `String[]` levels)                          |                     |
| `度量值`                              | AddMeasure(`String` name = null, `String` expression = null, `String` displayFolder = null)            |                     |
| `Boolean`                          | Browsable(`String` propertyName)                                                                       |                     |
| `void`                             | CheckChildrenErrors()                                                                                  |                     |
| `void`                             | Children_CollectionChanged(`Object` sender, `NotifyCollectionChangedEventArgs` e) |                     |
| `TabularNamedObject`               | Clone(`String` newName = null, `Boolean` includeTranslations = False)                                  |                     |
| `void`                             | Delete()                                                                                               |                     |
| `Boolean`                          | Editable(`String` propertyName)                                                                        |                     |
| `String`                           | GetAnnotation(`String` name)                                                                           |                     |
| `IEnumerable<ITabularNamedObject>` | GetChildren()                                                                                          | 返回该表中的所有列、度量值和层次结构。 |
| `IEnumerable<IDetailObject>`       | GetChildrenByFolders(`Boolean` recursive)                                                              |                     |
| `void`                             | Init()                                                                                                 |                     |
| `void`                             | InitRLSIndexer()                                                                                       |                     |
| `void`                             | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue)                         |                     |
| `void`                             | OnPropertyChanging(`String` propertyName, `Object` newValue, `Boolean&` undoable, `Boolean&` cancel)   |                     |
| `void`                             | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True)                                |                     |
| `void`                             | Undelete(`ITabularObjectCollection` collection)                                                        |                     |

静态字段

| 类型       | 姓名                    | 摘要 |
| -------- | --------------------- | -- |
| `Char[]` | InvalidTableNameChars |    |

## `TableCollection`

用于 Table 的集合类。提供便捷的属性，可一次性为多个对象设置同一属性。

```csharp
public class TabularEditor.TOMWrapper.TableCollection
    : TabularObjectCollection<Table, Table, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Table>, IEnumerable<Table>, IList<Table>, ITabularObjectCollection, IExpandableIndexer

```

属性

| 类型        | 姓名           | 摘要 |
| --------- | ------------ | -- |
| `String`  | DataCategory |    |
| `String`  | 说明           |    |
| `Boolean` | IsHidden     |    |
| `Model`   | Parent       |    |

方法

| 类型       | 姓名                            | 摘要 |
| -------- | ----------------------------- | -- |
| `String` | ToString() |    |

## `TableExtension`

```csharp
public static class TabularEditor.TOMWrapper.TableExtension

```

静态方法

| 类型      | 姓名                                                   | 摘要 |
| ------- | ---------------------------------------------------- | -- |
| `分区源类型` | GetSourceType(this `Table` table) |    |

## `TableRLSIndexer`

TableRLSIndexer 用于浏览模型中所有角色中针对某个特定表定义的所有筛选器。相比之下，RoleRLSIndexer 会针对某个特定角色浏览该角色在所有表上定义的筛选器。

```csharp
public class TabularEditor.TOMWrapper.TableRLSIndexer
    : IEnumerable<String>, IEnumerable, IExpandableIndexer

```

字段

| 类型      | 姓名 | 摘要 |
| ------- | -- | -- |
| `Table` | 表  |    |

属性

| 类型                              | 姓名     | 摘要 |
| ------------------------------- | ------ | -- |
| `String`                        | 项      |    |
| `String`                        | 项      |    |
| `IEnumerable<String>`           | 键      |    |
| `Dictionary<ModelRole, String>` | RLSMap |    |
| `String`                        | 摘要     |    |

方法

| 类型                    | 姓名                                                                     | 摘要 |
| --------------------- | ---------------------------------------------------------------------- | -- |
| `void`                | Clear()                                             |    |
| `void`                | CopyFrom(`TableRLSIndexer` source)                  |    |
| `String`              | GetDisplayName(`String` key)                        |    |
| `IEnumerator<String>` | GetEnumerator()                                     |    |
| `void`                | Refresh()                                           |    |
| `void`                | SetRLS(`ModelRole` role, `String` filterExpression) |    |

## `TabularCollectionHelper`

```csharp
public static class TabularEditor.TOMWrapper.TabularCollectionHelper

```

静态方法

| 类型     | 姓名                                                                                                                           | 摘要 |
| ------ | ---------------------------------------------------------------------------------------------------------------------------- | -- |
| `void` | InPerspective(this `IEnumerable<Table>` tables, `String` perspective, `Boolean` value)                    |    |
| `void` | InPerspective(this `IEnumerable<Column>` columns, `String` perspective, `Boolean` value)                  |    |
| `void` | InPerspective(this `IEnumerable<Hierarchy>` hierarchies, `String` perspective, `Boolean` value)           |    |
| `void` | InPerspective(this `IEnumerable<Measure>` measures, `String` perspective, `Boolean` value)                |    |
| `void` | InPerspective(this `IEnumerable<Table>` tables, `Perspective` perspective, `Boolean` value)               |    |
| `void` | InPerspective(this `IEnumerable<Column>` columns, `透视` perspective, `Boolean` value)                      |    |
| `void` | InPerspective(this `IEnumerable<Hierarchy>` hierarchies, `透视` perspective, `Boolean` value)               |    |
| `void` | InPerspective(this `IEnumerable<Measure>` measures, `Perspective` perspective, `Boolean` value) 在透视中设置度量值 |    |
| `void` | SetDisplayFolder(this `IEnumerable<Measure>` measures, `String` displayFolder) 为度量值设置显示文件夹                |    |

## `TabularCommonActions`

提供在 Tabular 模型上执行常见操作的便捷方法，这些操作通常会一次性更改多个对象。例如，这些方法可用于轻松执行 UI 拖放操作，从而更改层级、显示文件夹等。

```csharp
public class TabularEditor.TOMWrapper.TabularCommonActions

```

属性

| 类型                    | 姓名   | 摘要 |
| --------------------- | ---- | -- |
| `TabularModelHandler` | 处理程序 |    |

方法

| 类型       | 姓名                                                                                                                           | 摘要 |
| -------- | ---------------------------------------------------------------------------------------------------------------------------- | -- |
| `void`   | AddColumnsToHierarchy(`IEnumerable<Column>` columns, `Hierarchy` hierarchy, `Int32` firstOrdinal = -1)    |    |
| `级别`     | AddColumnToHierarchy(`Column` column, `Hierarchy` hierarchy, `Int32` ordinal = -1)                        |    |
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

| 类型       | 姓名                                                                                                | 摘要 |
| -------- | ------------------------------------------------------------------------------------------------- | -- |
| `String` | GetConnectionString(`String` serverName)                                       |    |
| `String` | GetConnectionString(`String` serverName, `String` userName, `String` password) |    |

## `Tabular区域设置Helper`

```csharp
public static class TabularEditor.TOMWrapper.TabularCultureHelper

```

静态方法

| 类型        | 姓名                                                                                                                | 摘要 |
| --------- | ----------------------------------------------------------------------------------------------------------------- | -- |
| `Boolean` | Import翻译(`String` 区域设置Json, `Model` Model, `Boolean` overwriteExisting, `Boolean` haltOnError) |    |

## `TabularDeployer`

```csharp
public class TabularEditor.TOMWrapper.TabularDeployer

```

静态方法

| 类型                 | 姓名                                                                                                                                | 摘要                                                                 |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| `void`             | Deploy(`Database` db, `String` targetConnectionString, `String` targetDatabaseName)                            | 使用指定的选项，将指定数据库部署到指定的目标服务器和数据库 ID。在部署成功的情况下，返回数据库中对象的 DAX 错误列表（如有）。 |
| `DeploymentResult` | Deploy(`Database` db, `String` targetConnectionString, `String` targetDatabaseID, `DeploymentOptions` options) | 使用指定的选项，将指定数据库部署到指定的目标服务器和数据库 ID。在部署成功的情况下，返回数据库中对象的 DAX 错误列表（如有）。 |
| `String`           | GetTMSL(`Database` db, `Server` server, `String` targetDatabaseID, `DeploymentOptions` options)                |                                                                    |
| `void`             | SaveModelMetadataBackup(`String` connectionString, `String` targetDatabaseID, `String` backupFilePath)         |                                                                    |
| `void`             | WriteZip(`String` fileName, `String` content)                                                                  |                                                                    |

## `TabularModelHandler`

```csharp
public class TabularEditor.TOMWrapper.TabularModelHandler
    : IDisposable

```

字段

| 类型                                             | 姓名                 | 摘要 |
| ---------------------------------------------- | ------------------ | -- |
| `Dictionary<String, ITabularObjectCollection>` | WrapperCollections |    |
| `Dictionary<MetadataObject, TabularObject>`    | WrapperLookup      |    |

属性

| 类型                                          | 姓名                       | 摘要                                                                        |
| ------------------------------------------- | ------------------------ | ------------------------------------------------------------------------- |
| `TabularCommonActions`                      | 操作                       |                                                                           |
| `布尔值`                                       | AutoFixup                | 指定对象名称（表、列、度量值）更改时，是否应自动更新 DAX 表达式以反映新名称。设置为 true 时，会解析模型中的所有表达式以构建依赖关系树。 |
| `数据库`                                       | 数据库                      |                                                                           |
| `布尔值`                                       | DelayBuildDependencyTree |                                                                           |
| `IList<Tuple<NamedMetadataObject, String>>` | 错误                       |                                                                           |
| `布尔值`                                       | HasUnsavedChanges        |                                                                           |
| `布尔值`                                       | IsConnected              |                                                                           |
| `模型`                                        | 模型                       |                                                                           |
| `字符串`                                       | 状态                       |                                                                           |
| `TabularTree`                               | 树                        |                                                                           |
| `UndoManager`                               | UndoManager              |                                                                           |
| `Int64`                                     | 版本                       |                                                                           |

方法

| 类型                          | 姓名                                                                                                                 | 摘要                                                                                                                      |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| `IDetailObject`             | Add(`AddObjectType` objectType, `IDetailObjectContainer` container)                             |                                                                                                                         |
| `void`                      | BeginUpdate(`String` undoName)                                                                  |                                                                                                                         |
| `void`                      | BuildDependencyTree(`IExpressionObject` expressionObj)                                          |                                                                                                                         |
| `void`                      | BuildDependencyTree()                                                                           |                                                                                                                         |
| `ConflictInfo`              | CheckConflicts()                                                                                |                                                                                                                         |
| `IList<TabularNamedObject>` | DeserializeObjects(`String` json)                                                               |                                                                                                                         |
| `void`                      | Dispose()                                                                                       |                                                                                                                         |
| `void`                      | DoFixup(`IDaxObject` obj, `String` newName)                                                     | 将所有对对象 "obj" 的引用更新为 "newName"                                                                                           |
| `Int32`                     | EndUpdate(`Boolean` undoable = True, `Boolean` rollback = False)                                |                                                                                                                         |
| `Int32`                     | EndUpdateAll(`Boolean` rollback = False)                                                        |                                                                                                                         |
| `Model`                     | GetModel()                                                                                      |                                                                                                                         |
| `Boolean`                   | ImportTranslations(`String` culturesJson, `Boolean` overwriteExisting, `Boolean` ignoreInvalid) | 应用来自 JSON 字符串的翻译。                                                                                                       |
| `void`                      | SaveDB()                                                                                        | 将更改保存到数据库。用户有责任检查自数据库加载到 TOMWrapper 以来，数据库是否已发生更改。为此，你可以使用 Handler.CheckConflicts()。 |
| `void`                      | SaveFile(`String` fileName, `SerializeOptions` options)                                         |                                                                                                                         |
| `void`                      | SaveToFolder(`String` path, `SerializeOptions` options)                                         |                                                                                                                         |
| `String`                    | ScriptCreateOrReplace()                                                                         | 为整个数据库生成脚本                                                                                                              |
| `String`                    | ScriptCreateOrReplace(`TabularNamedObject` obj)                                                 | 为整个数据库生成脚本                                                                                                              |
| `String`                    | ScriptTranslations(`IEnumerable<Culture>` translations)                                         |                                                                                                                         |
| `String`                    | SerializeObjects(`IEnumerable<TabularNamedObject>` objects)                                     |                                                                                                                         |
| `void`                      | UpdateFolders(`Table` table)                                                                    |                                                                                                                         |
| `void`                      | UpdateLevels(`Hierarchy` hierarchy)                                                             |                                                                                                                         |
| `void`                      | UpdateObject(`ITabularObject` obj)                                                              |                                                                                                                         |
| `void`                      | UpdateTables()                                                                                  |                                                                                                                         |

静态字段

| 类型       | 姓名                                          | 摘要 |
| -------- | ------------------------------------------- | -- |
| `String` | PROP_ERRORS            |    |
| `String` | PROP_HASUNSAVEDCHANGES |    |
| `String` | PROP_ISCONNECTED       |    |
| `String` | PROP_STATUS            |    |

静态属性

| 类型                    | 姓名 | 摘要 |
| --------------------- | -- | -- |
| `TabularModelHandler` | 单例 |    |

静态方法

| 类型                                              | 姓名                                                           | 摘要 |
| ----------------------------------------------- | ------------------------------------------------------------ | -- |
| `List<Tuple<NamedMetadataObject, String>>`      | CheckErrors(`Database` database)          |    |
| `List<Tuple<NamedMetadataObject, ObjectState>>` | CheckProcessingState(`Database` database) |    |

## `TabularNamedObject`

TabularObject 是对 Microsoft.AnalysisServices.Tabular.NamedMetadataObject 类的封装。此封装用于所有需要在 Tabular Editor 中查看和编辑的对象。这个基类适用于 Tabular 模型中的各种对象。这个基类提供了用于编辑（本地化）名称和描述的方法。

```csharp
public abstract class TabularEditor.TOMWrapper.TabularNamedObject
    : TabularObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable

```

属性

| 类型                    | 姓名              | 摘要            |
| --------------------- | --------------- | ------------- |
| `Int32`               | MetadataIndex   |               |
| `NamedMetadataObject` | MetadataObject  |               |
| `String`              | 姓名              |               |
| `翻译索引器`               | TranslatedNames | 这个对象的本地化名称集合。 |

方法

| 类型                   | 姓名                                                                 | 摘要                                                                         |
| -------------------- | ------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| `TabularNamedObject` | Clone(`String` newName, `Boolean` include翻译)    |                                                                            |
| `Int32`              | CompareTo(`Object` obj)                         |                                                                            |
| `void`               | Delete()                                        |                                                                            |
| `void`               | Init()                                          |                                                                            |
| `void`               | Undelete(`ITabularObjectCollection` collection) | 要撤销删除操作，需要采用一种不太优雅的变通方案。派生类必须确保更新该对象“拥有”的所有对象。例如，度量值必须负责更新其 KPI 的封装器（如果有）。 |

## `TabularObject`

```csharp
public abstract class TabularEditor.TOMWrapper.TabularObject
    : ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging

```

字段

| 类型                         | 姓名         | 摘要 |
| -------------------------- | ---------- | -- |
| `ITabularObjectCollection` | Collection |    |
| `TabularModelHandler`      | Handler    |    |

属性

| 类型                   | 姓名                       | 摘要 |
| -------------------- | ------------------------ | -- |
| `MetadataObject`     | MetadataObject           |    |
| `模型`                 | 模型                       |    |
| `ObjectType`         | ObjectType               |    |
| `String`             | ObjectTypeName           |    |
| `翻译索引器`              | TranslatedDescriptions   |    |
| `TranslationIndexer` | TranslatedDisplayFolders |    |

事件

| 类型                             | 姓名               | 摘要 |
| ------------------------------ | ---------------- | -- |
| `PropertyChangedEventHandler`  | PropertyChanged  |    |
| `PropertyChangingEventHandler` | PropertyChanging |    |

方法

| 类型        | 姓名                                                                                                                      | 摘要                                                                   |
| --------- | ----------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `void`    | Init()                                                                                               | 派生类应重写此方法以实例化子对象                                                     |
| `void`    | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue)                       |                                                                      |
| `void`    | OnPropertyChanging(`String` propertyName, `Object` newValue, `Boolean&` undoable, `Boolean&` cancel) | 在更改对象属性之前调用。派生类可以控制如何处理此更改。在此方法中抛出 ArgumentException，以便在 UI 中显示错误信息。 |
| `Boolean` | SetField(`T&` field, `T` value, `String` propertyName = null)                                        |                                                                      |

## `TabularObjectCollection<T, TT, TP>`

```csharp
public abstract class TabularEditor.TOMWrapper.TabularObjectCollection<T, TT, TP>
    : IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<T>, IEnumerable<T>, IList<T>, ITabularObjectCollection, IExpandableIndexer

```

属性

| 类型                                      | 姓名                       | 摘要 |
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

| 类型                                    | 姓名                | 摘要 |
| ------------------------------------- | ----------------- | -- |
| `NotifyCollectionChangedEventHandler` | CollectionChanged |    |

方法

| 类型                         | 姓名                                                         | 摘要 |
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

| 类型            | 姓名 | 摘要 |
| ------------- | -- | -- |
| `ObjectOrder` | 顺序 |    |

方法

| 类型      | 姓名                                                                           | 摘要 |
| ------- | ---------------------------------------------------------------------------- | -- |
| `Int32` | Compare(`Object` x, `Object` y)                           |    |
| `Int32` | Compare(`ITabularNamedObject` x, `ITabularNamedObject` y) |    |

## `TabularObjectHelper`

```csharp
public static class TabularEditor.TOMWrapper.TabularObjectHelper

```

静态方法

| 类型        | 姓名                                                                                           | 摘要 |
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

TabularLogicalModel 用于控制 TabularObjects 之间的关系，以便在 TreeViewAdv 控件中显示。每个 TabularObject 本身既不知道也不关心它与其他对象之间的逻辑关系（例如，通过特定区域设置下的 DisplayFolders）。 TabularObjects 只关心它们的物理关系，这些关系直接继承自 Tabular Object Model（即：度量值属于某个表等）。

```csharp
public abstract class TabularEditor.TOMWrapper.TabularTree
    : INotifyPropertyChanged

```

字段

| 类型                           | 姓名         | 摘要 |
| ---------------------------- | ---------- | -- |
| `Dictionary<String, Folder>` | FolderTree |    |

属性

| 类型                    | 姓名          | 摘要 |
| --------------------- | ----------- | -- |
| `区域设置`                | 区域设置        |    |
| `String`              | 筛选          |    |
| `TabularModelHandler` | 处理程序        |    |
| `模型`                  | 模型          |    |
| `LogicalTreeOptions`  | 选项          |    |
| `透视`                  | 透视          |    |
| `Int32`               | UpdateLocks |    |

事件

| 类型                            | 姓名              | 摘要 |
| ----------------------------- | --------------- | -- |
| `PropertyChangedEventHandler` | PropertyChanged |    |

方法

| 类型                     | 姓名                                                                                                        | 摘要                                                      |
| ---------------------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| `void`                 | BeginUpdate()                                                                          |                                                         |
| `void`                 | EndUpdate()                                                                            |                                                         |
| `IEnumerable`          | GetChildren(`ITabularObjectContainer` tabularObject)                                   | 此方法封装了用于定义表格模型树形表示结构的逻辑                                 |
| `Func<String, String>` | GetFolderMutation(`Object` source, `Object` destination)                               |                                                         |
| `Func<String, String>` | GetFolderMutation(`String` oldPath, `String` newPath)                                  |                                                         |
| `void`                 | ModifyDisplayFolder(`Table` table, `String` oldPath, `String` newPath, `区域设置` culture) | 更新某个表中所有表格对象的 DisplayFolder 属性。位于该更新路径下各子文件夹中的对象也会一并更新。 |
| `void`                 | OnNodesChanged(`ITabularObject` nodeItem)                                              |                                                         |
| `void`                 | OnNodesInserted(`ITabularObject` parent, `ITabularObject[]` children)                  |                                                         |
| `void`                 | OnNodesInserted(`ITabularObject` parent, `IEnumerable<ITabularObject>` children)       |                                                         |
| `void`                 | OnNodesRemoved(`ITabularObject` parent, `ITabularObject[]` children)                   |                                                         |
| `void`                 | OnNodesRemoved(`ITabularObject` parent, `IEnumerable<ITabularObject>` children)        |                                                         |
| `void`                 | OnStructureChanged(`ITabularNamedObject` obj = null)                                   |                                                         |
| `void`                 | SetCulture(`String` 区域设置名称)                                                            |                                                         |
| `void`                 | SetPerspective(`String` 透视名称)                                                          |                                                         |
| `void`                 | UpdateFolder(`Folder` folder, `String` oldFullPath = null)                             |                                                         |
| `Boolean`              | VisibleInTree(`ITabularNamedObject` tabularObject)                                     |                                                         |

## `翻译索引器`

```csharp
public class TabularEditor.TOMWrapper.TranslationIndexer
    : IEnumerable<String>, IEnumerable, IExpandableIndexer

```

属性

| 类型                    | 姓名              | 摘要 |
| --------------------- | --------------- | -- |
| `String`              | DefaultValue    |    |
| `String`              | Item            |    |
| `String`              | Item            |    |
| `IEnumerable<String>` | Keys            |    |
| `String`              | Summary         |    |
| `Int32`               | TranslatedCount |    |

方法

| 类型                           | 姓名                                                                                          | 摘要                                                                 |
| ---------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| `void`                       | Clear()                                                                  | 清除此对象的所有已翻译值。                                                      |
| `Boolean`                    | Contains(`区域设置` culture)                                                 |                                                                    |
| `Dictionary<String, String>` | 复制()                                                                     |                                                                    |
| `void`                       | CopyFrom(`TranslationIndexer` 翻译, `Func<String, String>` mutator = null) |                                                                    |
| `void`                       | CopyFrom(`IDictionary<String, String>` source)                           |                                                                    |
| `String`                     | GetDisplayName(`String` key)                                             |                                                                    |
| `IEnumerator<String>`        | GetEnumerator()                                                          |                                                                    |
| `void`                       | Refresh()                                                                |                                                                    |
| `void`                       | Reset()                                                                  | 重置该对象的翻译。标题翻译将被移除，使该对象在所有区域设置中都以基础名称显示。显示文件夹和说明的翻译将被设置为该对象的未翻译原始值。 |
| `void`                       | SetAll(`String` value)                                                   |                                                                    |


