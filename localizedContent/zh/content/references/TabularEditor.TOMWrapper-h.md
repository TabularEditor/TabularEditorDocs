# TabularEditor.TOMWrapper Reference

This is auto-generated documentation for the TOMWrapper API. Use CTRL+F or the sidebar on the right, to locate a specific class, property or method.

## `AddObjectType`

```csharp
public enum TabularEditor.TOMWrapper.AddObjectType
    : Enum, IComparable, IFormattable, IConvertible

```

Enum

| 值   | 姓名               | Summary |
| --- | ---------------- | ------- |
| `1` | 度量值              |         |
| `2` | CalculatedColumn |         |
| `3` | 层次结构             |         |

## `CalculatedColumn`

Base class declaration for CalculatedColumn

```csharp
public class TabularEditor.TOMWrapper.CalculatedColumn
    : Column, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IErrorMessageObject, IDescriptionObject, IAnnotationObject, ITabularPerspectiveObject, IDaxObject, IExpressionObject

```

属性

| Type                                       | 姓名                 | Summary                                                                      |
| ------------------------------------------ | ------------------ | ---------------------------------------------------------------------------- |
| `Dictionary<IDaxObject, List<Dependency>>` | Dependencies       |                                                                              |
| `String`                                   | 表达式                | Gets or sets the Expression of the CalculatedColumn.         |
| `Boolean`                                  | IsDataTypeInferred | Gets or sets the IsDataTypeInferred of the CalculatedColumn. |
| `CalculatedColumn`                         | MetadataObject     |                                                                              |
| `Boolean`                                  | NeedsValidation    |                                                                              |

Methods

| Type                 | 姓名                                                                                                       | Summary |
| -------------------- | -------------------------------------------------------------------------------------------------------- | ------- |
| `TabularNamedObject` | Clone(`String` newName = null, `Boolean` includeTranslations = True)                  |         |
| `TabularNamedObject` | CloneTo(`Table` table, `String` newName = null, `Boolean` includeTranslations = True) |         |
| `void`               | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue)        |         |

## `CalculatedTable`

```csharp
public class TabularEditor.TOMWrapper.CalculatedTable
    : Table, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IHideableObject, IDescriptionObject, IAnnotationObject, ITabularObjectContainer, IDetailObjectContainer, ITabularPerspectiveObject, IDaxObject, IDynamicPropertyObject, IErrorMessageObject, IExpressionObject

```

属性

| Type                                       | 姓名              | Summary |
| ------------------------------------------ | --------------- | ------- |
| `Dictionary<IDaxObject, List<Dependency>>` | Dependencies    |         |
| `String`                                   | 表达式             |         |
| `Boolean`                                  | NeedsValidation |         |
| `String`                                   | ObjectTypeName  |         |

Methods

| Type      | 姓名                                                                                                | Summary                                                                                                                            |
| --------- | ------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `void`    | CheckChildrenErrors()                                                          |                                                                                                                                    |
| `Boolean` | Editable(`String` propertyName)                                                |                                                                                                                                    |
| `void`    | Init()                                                                         |                                                                                                                                    |
| `void`    | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue) |                                                                                                                                    |
| `void`    | ReinitColumns()                                                                | Call this method after the model is saved to a DB, to check for changed columns (in case of expression changes) |

## `CalculatedTableColumn`

Base class declaration for CalculatedTableColumn

```csharp
public class TabularEditor.TOMWrapper.CalculatedTableColumn
    : Column, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IErrorMessageObject, IDescriptionObject, IAnnotationObject, ITabularPerspectiveObject, IDaxObject

```

属性

| Type                    | 姓名                 | Summary                                                                           |
| ----------------------- | ------------------ | --------------------------------------------------------------------------------- |
| `Column`                | ColumnOrigin       | Gets or sets the ColumnOrigin of the CalculatedTableColumn.       |
| `Boolean`               | IsDataTypeInferred | Gets or sets the IsDataTypeInferred of the CalculatedTableColumn. |
| `Boolean`               | IsNameInferred     | Gets or sets the IsNameInferred of the CalculatedTableColumn.     |
| `CalculatedTableColumn` | MetadataObject     |                                                                                   |
| `String`                | 源列                 | Gets or sets the SourceColumn of the CalculatedTableColumn.       |

## `Column`

Base class declaration for Column

```csharp
public abstract class TabularEditor.TOMWrapper.Column
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IErrorMessageObject, IDescriptionObject, IAnnotationObject, ITabularPerspectiveObject, IDaxObject

```

属性

| Type                         | 姓名                                              | Summary                                                                                                             |
| ---------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `Alignment`                  | Alignment                                       | Gets or sets the Alignment of the Column.                                                           |
| `String`                     | DataCategory                                    | Gets or sets the DataCategory of the Column.                                                        |
| `DataType`                   | 数据类型                                            | Gets or sets the DataType of the Column.                                                            |
| `String`                     | DaxObjectFullName                               |                                                                                                                     |
| `String`                     | DaxObjectName                                   |                                                                                                                     |
| `String`                     | DaxTableName                                    |                                                                                                                     |
| `HashSet<IExpressionObject>` | Dependants                                      |                                                                                                                     |
| `String`                     | 说明                                              | Gets or sets the Description of the Column.                                                         |
| `String`                     | DisplayFolder                                   | Gets or sets the DisplayFolder of the Column.                                                       |
| `Int32`                      | DisplayOrdinal                                  | Gets or sets the DisplayOrdinal of the Column.                                                      |
| `String`                     | ErrorMessage                                    | Gets or sets the ErrorMessage of the Column.                                                        |
| `String`                     | 格式字符串                                           | Gets or sets the FormatString of the Column.                                                        |
| `PerspectiveIndexer`         | InPerspective                                   |                                                                                                                     |
| `Boolean`                    | IsAvailableInMDX                                | Gets or sets the IsAvailableInMDX of the Column.                                                    |
| `Boolean`                    | IsDefaultImage                                  | Gets or sets the IsDefaultImage of the Column.                                                      |
| `Boolean`                    | IsDefaultLabel                                  | Gets or sets the IsDefaultLabel of the Column.                                                      |
| `Boolean`                    | IsHidden                                        | Gets or sets the IsHidden of the Column.                                                            |
| `Boolean`                    | IsKey                                           | Gets or sets the IsKey of the Column.                                                               |
| `Boolean`                    | IsNullable                                      | Gets or sets the IsNullable of the Column.                                                          |
| `Boolean`                    | IsUnique                                        | Gets or sets the IsUnique of the Column.                                                            |
| `Boolean`                    | KeepUniqueRows                                  | Gets or sets the KeepUniqueRows of the Column.                                                      |
| `Column`                     | MetadataObject                                  |                                                                                                                     |
| `Column`                     | SortByColumn                                    | Gets or sets the SortByColumn of the Column.                                                        |
| `String`                     | SourceProviderType                              | Gets or sets the SourceProviderType of the Column.                                                  |
| `ObjectState`                | State                                           | Gets or sets the State of the Column.                                                               |
| `AggregateFunction`          | SummarizeBy                                     | Gets or sets the SummarizeBy of the Column.                                                         |
| `Table`                      | 表                                               |                                                                                                                     |
| `Int32`                      | TableDetailPosition                             | Gets or sets the TableDetailPosition of the Column.                                                 |
| `TranslationIndexer`         | TranslatedDescriptions                          | Collection of localized descriptions for this Column.                                               |
| `TranslationIndexer`         | TranslatedDisplayFolders                        | Collection of localized Display Folders for this Column.                                            |
| `ColumnType`                 | Type                                            | Gets or sets the Type of the Column.                                                                |
| `IEnumerable<Hierarchy>`     | UsedInHierarchies<a id="used-in-hierarchy"></a> | Enumerates all hierarchies in which this column is used as a level.                                 |
| `IEnumerable<Relationship>`  | UsedInRelationships                             | Enumerates all relationships in which this column participates (either as  or ). |

Methods

| Type     | 名称                                                                                                                      | Summary |
| -------- | ----------------------------------------------------------------------------------------------------------------------- | ------- |
| `void`   | Delete()                                                                                             |         |
| `String` | GetAnnotation(`String` name)                                                                         |         |
| `void`   | Init()                                                                                               |         |
| `void`   | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue)                       |         |
| `void`   | OnPropertyChanging(`String` propertyName, `Object` newValue, `Boolean&` undoable, `Boolean&` cancel) |         |
| `void`   | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True)                              |         |
| `void`   | Undelete(`ITabularObjectCollection` collection)                                                      |         |

## `ColumnCollection`

Collection class for Column. Provides convenient properties for setting a property on multiple objects at once.

```csharp
public class TabularEditor.TOMWrapper.ColumnCollection
    : TabularObjectCollection<Column, Column, Table>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Column>, IEnumerable<Column>, IList<Column>, ITabularObjectCollection, IExpandableIndexer

```

属性

| Type                | 姓名                  | Summary |
| ------------------- | ------------------- | ------- |
| `Alignment`         | Alignment           |         |
| `String`            | DataCategory        |         |
| `DataType`          | 数据类型                |         |
| `String`            | 说明                  |         |
| `String`            | DisplayFolder       |         |
| `Int32`             | DisplayOrdinal      |         |
| `String`            | 格式字符串               |         |
| `Boolean`           | IsAvailableInMDX    |         |
| `Boolean`           | IsDefaultImage      |         |
| `Boolean`           | IsDefaultLabel      |         |
| `Boolean`           | IsHidden            |         |
| `Boolean`           | IsKey               |         |
| `Boolean`           | IsNullable          |         |
| `Boolean`           | IsUnique            |         |
| `Boolean`           | KeepUniqueRows      |         |
| `Table`             | Parent              |         |
| `Column`            | SortByColumn        |         |
| `String`            | SourceProviderType  |         |
| `AggregateFunction` | SummarizeBy         |         |
| `Int32`             | TableDetailPosition |         |

Methods

| Type                  | 姓名                                 | Summary |
| --------------------- | ---------------------------------- | ------- |
| `IEnumerator<Column>` | GetEnumerator() |         |
| `String`              | ToString()      |         |

## `Culture`

Base class declaration for Culture

```csharp
public class TabularEditor.TOMWrapper.Culture
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IAnnotationObject, IDynamicPropertyObject

```

属性

| Type                          | 姓名                           | Summary |
| ----------------------------- | ---------------------------- | ------- |
| `String`                      | DisplayName                  |         |
| `Culture`                     | MetadataObject               |         |
| `String`                      | 姓名                           |         |
| `ObjectTranslationCollection` | ObjectTranslations           |         |
| `String`                      | StatsColumnCaptions          |         |
| `String`                      | StatsColumnDisplayFolders    |         |
| `String`                      | StatsHierarchyCaptions       |         |
| `String`                      | StatsHierarchyDisplayFolders |         |
| `String`                      | StatsLevelCaptions           |         |
| `String`                      | StatsMeasureCaptions         |         |
| `String`                      | StatsMeasureDisplayFolders   |         |
| `String`                      | StatsTableCaptions           |         |
| `Boolean`                     | Unassigned                   |         |

Methods

| Type                 | 姓名                                                                                                | Summary |
| -------------------- | ------------------------------------------------------------------------------------------------- | ------- |
| `Boolean`            | Browsable(`String` propertyName)                                               |         |
| `TabularNamedObject` | Clone(`String` newName, `Boolean` includeTranslations)                         |         |
| `Boolean`            | Editable(`String` propertyName)                                                |         |
| `String`             | GetAnnotation(`String` name)                                                   |         |
| `void`               | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue) |         |
| `void`               | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True)        |         |
| `void`               | Undelete(`ITabularObjectCollection` collection)                                |         |

## `CultureCollection`

Collection class for Culture. Provides convenient properties for setting a property on multiple objects at once.

```csharp
public class TabularEditor.TOMWrapper.CultureCollection
    : TabularObjectCollection<Culture, Culture, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Culture>, IEnumerable<Culture>, IList<Culture>, ITabularObjectCollection, IExpandableIndexer

```

属性

| Type    | 姓名     | Summary |
| ------- | ------ | ------- |
| `Model` | Parent |         |

Methods

| Type     | 姓名                            | Summary |
| -------- | ----------------------------- | ------- |
| `String` | ToString() |         |

## `CultureConverter`

```csharp
public class TabularEditor.TOMWrapper.CultureConverter
    : TypeConverter

```

Methods

| Type                       | 姓名                                                                                                                            | Summary |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ------- |
| `Boolean`                  | CanConvertFrom(`ITypeDescriptorContext` context, `Type` sourceType)                                        |         |
| `Boolean`                  | CanConvertTo(`ITypeDescriptorContext` context, `Type` destinationType)                                     |         |
| `Object`                   | ConvertFrom(`ITypeDescriptorContext` context, `CultureInfo` culture, `Object` value)                       |         |
| `Object`                   | ConvertTo(`ITypeDescriptorContext` context, `CultureInfo` culture, `Object` value, `Type` destinationType) |         |
| `StandardValuesCollection` | GetStandardValues(`ITypeDescriptorContext` context)                                                        |         |
| `Boolean`                  | GetStandardValuesExclusive(`ITypeDescriptorContext` context)                                               |         |
| `Boolean`                  | GetStandardValuesSupported(`ITypeDescriptorContext` context)                                               |         |

## `Database`

```csharp
public class TabularEditor.TOMWrapper.Database

```

属性

| Type                 | 姓名                 | Summary |
| -------------------- | ------------------ | ------- |
| `Nullable<Int32>`    | CompatibilityLevel |         |
| `Nullable<DateTime>` | CreatedTimestamp   |         |
| `String`             | ID                 |         |
| `Nullable<DateTime>` | LastProcessed      |         |
| `Nullable<DateTime>` | LastSchemaUpdate   |         |
| `Nullable<DateTime>` | LastUpdate         |         |
| `String`             | 姓名                 |         |
| `String`             | ServerName         |         |
| `String`             | ServerVersion      |         |
| `Database`           | TOMDatabase        |         |
| `Nullable<Int64>`    | Version            |         |

Methods

| Type     | 姓名                            | Summary |
| -------- | ----------------------------- | ------- |
| `String` | ToString() |         |

## `DataColumn`

Base class declaration for DataColumn

```csharp
public class TabularEditor.TOMWrapper.DataColumn
    : Column, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IErrorMessageObject, IDescriptionObject, IAnnotationObject, ITabularPerspectiveObject, IDaxObject

```

属性

| Type         | 姓名             | Summary                                                          |
| ------------ | -------------- | ---------------------------------------------------------------- |
| `DataColumn` | MetadataObject |                                                                  |
| `String`     | 源列             | Gets or sets the SourceColumn of the DataColumn. |

## `DataSource`

Base class declaration for DataSource

```csharp
public abstract class TabularEditor.TOMWrapper.DataSource
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject

```

属性

| Type                 | 姓名                     | Summary                                                                   |
| -------------------- | ---------------------- | ------------------------------------------------------------------------- |
| `String`             | 说明                     | Gets or sets the Description of the DataSource.           |
| `DataSource`         | MetadataObject         |                                                                           |
| `TranslationIndexer` | TranslatedDescriptions | Collection of localized descriptions for this DataSource. |
| `DataSourceType`     | Type                   | Gets or sets the Type of the DataSource.                  |

Methods

| Type     | 姓名                                                                                         | Summary |
| -------- | ------------------------------------------------------------------------------------------ | ------- |
| `String` | GetAnnotation(`String` name)                                            |         |
| `void`   | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |         |

## `DataSourceCollection`

Collection class for DataSource. Provides convenient properties for setting a property on multiple objects at once.

```csharp
public class TabularEditor.TOMWrapper.DataSourceCollection
    : TabularObjectCollection<DataSource, DataSource, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<DataSource>, IEnumerable<DataSource>, IList<DataSource>, ITabularObjectCollection, IExpandableIndexer

```

属性

| Type     | 姓名     | Summary |
| -------- | ------ | ------- |
| `String` | 说明     |         |
| `Model`  | Parent |         |

Methods

| Type     | 姓名                            | Summary |
| -------- | ----------------------------- | ------- |
| `String` | ToString() |         |

## `Dependency`

```csharp
public struct TabularEditor.TOMWrapper.Dependency

```

Fields

| Type      | 姓名             | Summary |
| --------- | -------------- | ------- |
| `Int32`   | from           |         |
| `Boolean` | fullyQualified |         |
| `Int32`   | to             |         |

## `DependencyHelper`

```csharp
public static class TabularEditor.TOMWrapper.DependencyHelper

```

Static Methods

| Type     | 姓名                                                                                                                                             | Summary                                                                                                                   |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `void`   | AddDep(this `IExpressionObject` target, `IDaxObject` dependsOn, `Int32` fromChar, `Int32` toChar, `Boolean` fullyQualified) |                                                                                                                           |
| `String` | NoQ(this `String` objectName, `Boolean` table = False)                                                                      | Removes qualifiers such as ' ' and [ ] around a name. |

## `DeploymentMode`

```csharp
public enum TabularEditor.TOMWrapper.DeploymentMode
    : Enum, IComparable, IFormattable, IConvertible

```

Enum

| 值   | 姓名             | Summary |
| --- | -------------- | ------- |
| `0` | CreateDatabase |         |
| `1` | CreateOrAlter  |         |

## `DeploymentOptions`

```csharp
public class TabularEditor.TOMWrapper.DeploymentOptions

```

Fields

| Type             | 姓名                | Summary |
| ---------------- | ----------------- | ------- |
| `Boolean`        | DeployConnections |         |
| `DeploymentMode` | DeployMode        |         |
| `Boolean`        | DeployPartitions  |         |
| `Boolean`        | DeployRoleMembers |         |
| `Boolean`        | DeployRoles       |         |

Static Fields

| Type                | 姓名            | Summary |
| ------------------- | ------------- | ------- |
| `DeploymentOptions` | 默认值           |         |
| `DeploymentOptions` | StructureOnly |         |

## `DeploymentResult`

```csharp
public class TabularEditor.TOMWrapper.DeploymentResult

```

Fields

| Type                    | 姓名       | Summary |
| ----------------------- | -------- | ------- |
| `IReadOnlyList<String>` | Issues   |         |
| `IReadOnlyList<String>` | Warnings |         |

## `DeploymentStatus`

```csharp
public enum TabularEditor.TOMWrapper.DeploymentStatus
    : Enum, IComparable, IFormattable, IConvertible

```

Enum

| 值   | 姓名              | Summary |
| --- | --------------- | ------- |
| `0` | ChangesSaved    |         |
| `1` | DeployComplete  |         |
| `2` | DeployCancelled |         |

## `Folder`

Represents a Folder in the TreeView. Does not correspond to any object in the TOM.  Implements IDisplayFolderObject since a Folder can itself be located within another  display folder.  Implements IParentObject since a Folder can contain child objects.

```csharp
public class TabularEditor.TOMWrapper.Folder
    : IDetailObject, ITabularTableObject, ITabularNamedObject, ITabularObject, INotifyPropertyChanged, ITabularObjectContainer, IDetailObjectContainer, IErrorMessageObject

```

属性

| Type                     | 姓名                       | Summary |
| ------------------------ | ------------------------ | ------- |
| `IDetailObjectContainer` | Container                |         |
| `Culture`                | Culture                  |         |
| `String`                 | DisplayFolder            |         |
| `String`                 | ErrorMessage             |         |
| `String`                 | FullPath                 |         |
| `TabularModelHandler`    | Handler                  |         |
| `Int32`                  | MetadataIndex            |         |
| `Model`                  | 模型                       |         |
| `String`                 | 姓名                       |         |
| `ObjectType`             | ObjectType               |         |
| `Table`                  | ParentTable              |         |
| `String`                 | Path                     |         |
| `Table`                  | 表                        |         |
| `TranslationIndexer`     | TranslatedDisplayFolders |         |
| `TranslationIndexer`     | TranslatedNames          |         |

Events

| Type                          | 姓名              | Summary |
| ----------------------------- | --------------- | ------- |
| `PropertyChangedEventHandler` | PropertyChanged |         |

Methods

| Type                               | 姓名                                                                   | Summary                                                                                                                                                                                                               |
| ---------------------------------- | -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `void`                             | CheckChildrenErrors()                             |                                                                                                                                                                                                                       |
| `void`                             | Delete()                                          | Deleting a folder does not delete child objects - it just removes the folder.  Any child folders are retained (but will be moved up the display folder hierarchy). |
| `IEnumerable<ITabularNamedObject>` | GetChildren()                                     |                                                                                                                                                                                                                       |
| `IEnumerable<IDetailObject>`       | GetChildrenByFolders(`Boolean` recursive = False) |                                                                                                                                                                                                                       |
| `void`                             | SetFolderName(`String` newName)                   |                                                                                                                                                                                                                       |
| `void`                             | UndoSetPath(`String` value)                       |                                                                                                                                                                                                                       |

Static Methods

| Type     | 姓名                                                                                                                                 | Summary |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------- | ------- |
| `Folder` | CreateFolder(`Table` table, `String` path = , `Boolean` useFixedCulture = False, `Culture` fixedCulture = null) |         |

## `FolderHelper`

```csharp
public static class TabularEditor.TOMWrapper.FolderHelper

```

Static Methods

| Type                     | 姓名                                                                                                                | Summary |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------- | ------- |
| `String`                 | ConcatPath(this `String` path, `String` additionalPath)                                        |         |
| `String`                 | ConcatPath(this `IEnumerable<String>` pathBits)                                                |         |
| `IDetailObjectContainer` | GetContainer(this `IDetailObject` obj)                                                         |         |
| `String`                 | GetDisplayFolder(this `IDetailObject` folderObject, `Culture` culture)                         |         |
| `String`                 | GetFullPath(`ITabularNamedObject` obj)                                                         |         |
| `Boolean`                | HasAncestor(this `IDetailObject` child, `ITabularNamedObject` ancestor, `Culture` culture)     |         |
| `Boolean`                | HasParent(this `IDetailObject` child, `ITabularNamedObject` parent, `Culture` culture)         |         |
| `Int32`                  | Level(this `String` path)                                                                      |         |
| `String`                 | PathFromFullPath(`String` path)                                                                |         |
| `void`                   | SetDisplayFolder(this `IDetailObject` folderObject, `String` newFolderName, `Culture` culture) |         |
| `String`                 | TrimFolder(this `String` folderPath)                                                           |         |

## `Hierarchy`

Base class declaration for Hierarchy

```csharp
public class TabularEditor.TOMWrapper.Hierarchy
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IDescriptionObject, IAnnotationObject, ITabularObjectContainer, ITabularPerspectiveObject

```

属性

| Type                 | 姓名                       | Summary                                                                                     |
| -------------------- | ------------------------ | ------------------------------------------------------------------------------------------- |
| `String`             | 说明                       | Gets or sets the Description of the Hierarchy.                              |
| `String`             | DisplayFolder            | Gets or sets the DisplayFolder of the Hierarchy.                            |
| `PerspectiveIndexer` | InPerspective            |                                                                                             |
| `Boolean`            | IsHidden                 | Gets or sets the IsHidden of the Hierarchy.                                 |
| `LevelCollection`    | 级别                       |                                                                                             |
| `Hierarchy`          | MetadataObject           |                                                                                             |
| `Boolean`            | Reordering               | Set to true, when multiple levels are going to be re-ordered as one action. |
| `ObjectState`        | State                    | Gets or sets the State of the Hierarchy.                                    |
| `Table`              | 表                        |                                                                                             |
| `TranslationIndexer` | TranslatedDescriptions   | Collection of localized descriptions for this Hierarchy.                    |
| `TranslationIndexer` | TranslatedDisplayFolders | Collection of localized Display Folders for this Hierarchy.                 |

Methods

| Type                               | 姓名                                                                                                | Summary |
| ---------------------------------- | ------------------------------------------------------------------------------------------------- | ------- |
| `Level`                            | AddLevel(`Column` column, `String` levelName = null, `Int32` ordinal = -1)     |         |
| `Level`                            | AddLevel(`String` columnName, `String` levelName = null, `Int32` ordinal = -1) |         |
| `void`                             | AddLevels(`IEnumerable<Column>` columns, `Int32` ordinal = -1)                 |         |
| `void`                             | CompactLevelOrdinals()                                                         |         |
| `void`                             | Delete()                                                                       |         |
| `void`                             | FixLevelOrder(`Level` level, `Int32` newOrdinal)                               |         |
| `String`                           | GetAnnotation(`String` name)                                                   |         |
| `IEnumerable<ITabularNamedObject>` | GetChildren()                                                                  |         |
| `void`                             | Init()                                                                         |         |
| `void`                             | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True)        |         |
| `void`                             | SetLevelOrder(`IList<Level>` order)                                            |         |
| `void`                             | Undelete(`ITabularObjectCollection` collection)                                |         |

## `HierarchyCollection`

Collection class for Hierarchy. Provides convenient properties for setting a property on multiple objects at once.

```csharp
public class TabularEditor.TOMWrapper.HierarchyCollection
    : TabularObjectCollection<Hierarchy, Hierarchy, Table>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Hierarchy>, IEnumerable<Hierarchy>, IList<Hierarchy>, ITabularObjectCollection, IExpandableIndexer

```

属性

| Type      | 姓名            | Summary |
| --------- | ------------- | ------- |
| `String`  | 说明            |         |
| `String`  | DisplayFolder |         |
| `Boolean` | IsHidden      |         |
| `Table`   | Parent        |         |

Methods

| Type     | 姓名                            | Summary |
| -------- | ----------------------------- | ------- |
| `String` | ToString() |         |

## `HierarchyColumnConverter`

```csharp
public class TabularEditor.TOMWrapper.HierarchyColumnConverter
    : TableColumnConverter

```

Methods

| Type      | 姓名                                                                              | Summary |
| --------- | ------------------------------------------------------------------------------- | ------- |
| `Boolean` | GetStandardValuesExclusive(`ITypeDescriptorContext` context) |         |
| `Boolean` | IsValid(`ITypeDescriptorContext` context, `Object` value)    |         |

## `IAnnotationObject`

```csharp
public interface TabularEditor.TOMWrapper.IAnnotationObject
    : ITabularObject, INotifyPropertyChanged

```

Methods

| Type     | 姓名                                                                                         | Summary |
| -------- | ------------------------------------------------------------------------------------------ | ------- |
| `String` | GetAnnotation(`String` name)                                            |         |
| `void`   | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |         |

## `IClonableObject`

```csharp
public interface TabularEditor.TOMWrapper.IClonableObject

```

Methods

| Type                 | 姓名                                                                        | Summary |
| -------------------- | ------------------------------------------------------------------------- | ------- |
| `TabularNamedObject` | Clone(`String` newName, `Boolean` includeTranslations) |         |

## `IDaxObject`

```csharp
public interface TabularEditor.TOMWrapper.IDaxObject
    : ITabularNamedObject, ITabularObject, INotifyPropertyChanged

```

属性

| Type                         | 姓名                | Summary |
| ---------------------------- | ----------------- | ------- |
| `String`                     | DaxObjectFullName |         |
| `String`                     | DaxObjectName     |         |
| `String`                     | DaxTableName      |         |
| `HashSet<IExpressionObject>` | Dependants        |         |

## `IDescriptionObject`

Objects that can have descriptions

```csharp
public interface TabularEditor.TOMWrapper.IDescriptionObject

```

属性

| Type                 | 姓名                     | Summary |
| -------------------- | ---------------------- | ------- |
| `String`             | 说明                     |         |
| `TranslationIndexer` | TranslatedDescriptions |         |

## `IDetailObject`

Represents an object than can be contained in a Display Folder. Examples:  - Measures  - Columns  - Hierarchies  - Folders

```csharp
public interface TabularEditor.TOMWrapper.IDetailObject
    : ITabularTableObject, ITabularNamedObject, ITabularObject, INotifyPropertyChanged

```

属性

| Type                 | 姓名                       | Summary |
| -------------------- | ------------------------ | ------- |
| `String`             | DisplayFolder            |         |
| `TranslationIndexer` | TranslatedDisplayFolders |         |

## `IDetailObjectContainer`

Represents an objects that can contain other objects as well as display folders. Examples:  - Folders  - Table

```csharp
public interface TabularEditor.TOMWrapper.IDetailObjectContainer
    : ITabularNamedObject, ITabularObject, INotifyPropertyChanged

```

属性

| Type    | 姓名          | Summary |
| ------- | ----------- | ------- |
| `Table` | ParentTable |         |

Methods

| Type                         | 姓名                                                                   | Summary |
| ---------------------------- | -------------------------------------------------------------------- | ------- |
| `IEnumerable<IDetailObject>` | GetChildrenByFolders(`Boolean` recursive = False) |         |

## `IErrorMessageObject`

Objects that can have error messages

```csharp
public interface TabularEditor.TOMWrapper.IErrorMessageObject

```

属性

| Type     | 姓名           | Summary |
| -------- | ------------ | ------- |
| `String` | ErrorMessage |         |

## `IExpressionObject`

```csharp
public interface TabularEditor.TOMWrapper.IExpressionObject
    : IDaxObject, ITabularNamedObject, ITabularObject, INotifyPropertyChanged

```

属性

| Type                                       | 姓名              | Summary |
| ------------------------------------------ | --------------- | ------- |
| `Dictionary<IDaxObject, List<Dependency>>` | Dependencies    |         |
| `String`                                   | 表达式             |         |
| `Boolean`                                  | NeedsValidation |         |

## `IHideableObject`

Objects that can be shown/hidden

```csharp
public interface TabularEditor.TOMWrapper.IHideableObject

```

属性

| Type      | 姓名       | Summary |
| --------- | -------- | ------- |
| `Boolean` | IsHidden |         |

## `IntelliSenseAttribute`

```csharp
public class TabularEditor.TOMWrapper.IntelliSenseAttribute
    : Attribute, _Attribute

```

属性

| Type     | 姓名 | Summary |
| -------- | -- | ------- |
| `String` | 说明 |         |

## `ITabularNamedObject`

```csharp
public interface TabularEditor.TOMWrapper.ITabularNamedObject
    : ITabularObject, INotifyPropertyChanged

```

属性

| Type                 | 姓名              | Summary |
| -------------------- | --------------- | ------- |
| `Int32`              | MetadataIndex   |         |
| `String`             | 姓名              |         |
| `TranslationIndexer` | TranslatedNames |         |

## `ITabularObject`

```csharp
public interface TabularEditor.TOMWrapper.ITabularObject
    : INotifyPropertyChanged

```

属性

| Type         | 姓名         | Summary |
| ------------ | ---------- | ------- |
| `Model`      | 模型         |         |
| `ObjectType` | ObjectType |         |

## `ITabularObjectCollection`

```csharp
public interface TabularEditor.TOMWrapper.ITabularObjectCollection
    : IEnumerable

```

属性

| Type                  | 姓名             | Summary |
| --------------------- | -------------- | ------- |
| `String`              | CollectionName |         |
| `TabularModelHandler` | Handler        |         |
| `IEnumerable<String>` | Keys           |         |

Methods

| Type                       | 姓名                                                   | Summary |
| -------------------------- | ---------------------------------------------------- | ------- |
| `void`                     | Add(`TabularNamedObject` obj)     |         |
| `void`                     | Clear()                           |         |
| `Boolean`                  | Contains(`Object` value)          |         |
| `Boolean`                  | Contains(`String` key)            |         |
| `ITabularObjectCollection` | GetCurrentCollection()            |         |
| `Int32`                    | IndexOf(`TabularNamedObject` obj) |         |
| `void`                     | Remove(`TabularNamedObject` obj)  |         |

## `ITabularObjectContainer`

TabularObjects that can contain other objects should use this interface.

```csharp
public interface TabularEditor.TOMWrapper.ITabularObjectContainer

```

Methods

| Type                               | 姓名                               | Summary |
| ---------------------------------- | -------------------------------- | ------- |
| `IEnumerable<ITabularNamedObject>` | GetChildren() |         |

## `ITabularPerspectiveObject`

Objects that can be shown/hidden in individual perspectives

```csharp
public interface TabularEditor.TOMWrapper.ITabularPerspectiveObject
    : IHideableObject

```

属性

| Type                 | 姓名            | Summary |
| -------------------- | ------------- | ------- |
| `PerspectiveIndexer` | InPerspective |         |

## `ITabularTableObject`

Object that belongs to a specific table.

```csharp
public interface TabularEditor.TOMWrapper.ITabularTableObject
    : ITabularNamedObject, ITabularObject, INotifyPropertyChanged

```

属性

| Type    | 姓名 | Summary |
| ------- | -- | ------- |
| `Table` | 表  |         |

Methods

| Type   | 姓名                          | Summary |
| ------ | --------------------------- | ------- |
| `void` | Delete() |         |

## `KPI`

Base class declaration for KPI

```csharp
public class TabularEditor.TOMWrapper.KPI
    : TabularObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, IDescriptionObject, IAnnotationObject, IDynamicPropertyObject

```

属性

| Type                 | 姓名                     | Summary                                                            |
| -------------------- | ---------------------- | ------------------------------------------------------------------ |
| `String`             | 说明                     | Gets or sets the Description of the KPI.           |
| `Measure`            | 度量值                    | Gets or sets the Measure of the KPI.               |
| `KPI`                | MetadataObject         |                                                                    |
| `String`             | StatusDescription      | Gets or sets the StatusDescription of the KPI.     |
| `String`             | StatusExpression       | Gets or sets the StatusExpression of the KPI.      |
| `String`             | StatusGraphic          | Gets or sets the StatusGraphic of the KPI.         |
| `String`             | TargetDescription      | Gets or sets the TargetDescription of the KPI.     |
| `String`             | TargetExpression       | Gets or sets the TargetExpression of the KPI.      |
| `String`             | TargetFormatString     | Gets or sets the TargetFormatString of the KPI.    |
| `TranslationIndexer` | TranslatedDescriptions | Collection of localized descriptions for this KPI. |
| `String`             | TrendDescription       | Gets or sets the TrendDescription of the KPI.      |
| `String`             | TrendExpression        | Gets or sets the TrendExpression of the KPI.       |
| `String`             | TrendGraphic           | Gets or sets the TrendGraphic of the KPI.          |

Methods

| Type      | 姓名                                                                                         | Summary |
| --------- | ------------------------------------------------------------------------------------------ | ------- |
| `Boolean` | Browsable(`String` propertyName)                                        |         |
| `Boolean` | Editable(`String` propertyName)                                         |         |
| `String`  | GetAnnotation(`String` name)                                            |         |
| `void`    | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |         |

## `Level`

Base class declaration for Level

```csharp
public class TabularEditor.TOMWrapper.Level
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject, ITabularTableObject

```

属性

| Type                 | 姓名                     | Summary                                                              |
| -------------------- | ---------------------- | -------------------------------------------------------------------- |
| `Column`             | Column                 | Gets or sets the Column of the Level.                |
| `String`             | 说明                     | Gets or sets the Description of the Level.           |
| `Hierarchy`          | 层次结构                   | Gets or sets the Hierarchy of the Level.             |
| `Level`              | MetadataObject         |                                                                      |
| `Int32`              | Ordinal                | Gets or sets the Ordinal of the Level.               |
| `Table`              | 表                      |                                                                      |
| `TranslationIndexer` | TranslatedDescriptions | Collection of localized descriptions for this Level. |

Methods

| Type     | 姓名                                                                                                                      | Summary                                               |
| -------- | ----------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| `void`   | Delete()                                                                                             | Deletes the level from the hierarchy. |
| `String` | GetAnnotation(`String` name)                                                                         |                                                       |
| `void`   | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue)                       |                                                       |
| `void`   | OnPropertyChanging(`String` propertyName, `Object` newValue, `Boolean&` undoable, `Boolean&` cancel) |                                                       |
| `void`   | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True)                              |                                                       |
| `void`   | Undelete(`ITabularObjectCollection` collection)                                                      |                                                       |

## `LevelCollection`

Collection class for Level. Provides convenient properties for setting a property on multiple objects at once.

```csharp
public class TabularEditor.TOMWrapper.LevelCollection
    : TabularObjectCollection<Level, Level, Hierarchy>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Level>, IEnumerable<Level>, IList<Level>, ITabularObjectCollection, IExpandableIndexer

```

属性

| Type        | 姓名     | Summary |
| ----------- | ------ | ------- |
| `String`    | 说明     |         |
| `Hierarchy` | Parent |         |

Methods

| Type      | 姓名                                      | Summary |
| --------- | --------------------------------------- | ------- |
| `void`    | Add(`Level` item)    |         |
| `Boolean` | Remove(`Level` item) |         |
| `String`  | ToString()           |         |

## `LogicalGroup`

```csharp
public class TabularEditor.TOMWrapper.LogicalGroup
    : ITabularNamedObject, ITabularObject, INotifyPropertyChanged, ITabularObjectContainer

```

属性

| Type                 | 姓名              | Summary |
| -------------------- | --------------- | ------- |
| `Int32`              | MetadataIndex   |         |
| `Model`              | 模型              |         |
| `String`             | 姓名              |         |
| `ObjectType`         | ObjectType      |         |
| `TranslationIndexer` | TranslatedNames |         |

Events

| Type                          | 姓名              | Summary |
| ----------------------------- | --------------- | ------- |
| `PropertyChangedEventHandler` | PropertyChanged |         |

Methods

| Type                               | 姓名                               | Summary |
| ---------------------------------- | -------------------------------- | ------- |
| `IEnumerable<ITabularNamedObject>` | GetChildren() |         |

## `LogicalTreeOptions`

```csharp
public enum TabularEditor.TOMWrapper.LogicalTreeOptions
    : Enum, IComparable, IFormattable, IConvertible

```

Enum

| 值     | 姓名             | Summary |
| ----- | -------------- | ------- |
| `1`   | DisplayFolders |         |
| `2`   | 列              |         |
| `4`   | 度量值            |         |
| `8`   | KPI            |         |
| `16`  | 层次结构           |         |
| `32`  | 级别             |         |
| `64`  | ShowHidden     |         |
| `128` | AllObjectTypes |         |
| `256` | ShowRoot       |         |
| `447` | 默认值            |         |

## `Measure`

Base class declaration for Measure

```csharp
public class TabularEditor.TOMWrapper.Measure
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IErrorMessageObject, IDescriptionObject, IExpressionObject, IDaxObject, IAnnotationObject, ITabularPerspectiveObject, IDynamicPropertyObject, IClonableObject

```

属性

| Type                                       | 姓名                       | Summary                                                                   |
| ------------------------------------------ | ------------------------ | ------------------------------------------------------------------------- |
| `DataType`                                 | 数据类型                     | Gets or sets the DataType of the Measure.                 |
| `String`                                   | DaxObjectFullName        |                                                                           |
| `String`                                   | DaxObjectName            |                                                                           |
| `String`                                   | DaxTableName             |                                                                           |
| `HashSet<IExpressionObject>`               | Dependants               |                                                                           |
| `Dictionary<IDaxObject, List<Dependency>>` | Dependencies             |                                                                           |
| `String`                                   | 说明                       | Gets or sets the Description of the Measure.              |
| `String`                                   | DisplayFolder            | Gets or sets the DisplayFolder of the Measure.            |
| `String`                                   | ErrorMessage             | Gets or sets the ErrorMessage of the Measure.             |
| `String`                                   | 表达式                      | Gets or sets the Expression of the Measure.               |
| `String`                                   | 格式字符串                    | Gets or sets the FormatString of the Measure.             |
| `PerspectiveIndexer`                       | InPerspective            |                                                                           |
| `Boolean`                                  | IsHidden                 | Gets or sets the IsHidden of the Measure.                 |
| `Boolean`                                  | IsSimpleMeasure          | Gets or sets the IsSimpleMeasure of the Measure.          |
| `KPI`                                      | KPI                      | Gets or sets the KPI of the Measure.                      |
| `Measure`                                  | MetadataObject           |                                                                           |
| `Boolean`                                  | NeedsValidation          |                                                                           |
| `ObjectState`                              | State                    | Gets or sets the State of the Measure.                    |
| `Table`                                    | 表                        |                                                                           |
| `TranslationIndexer`                       | TranslatedDescriptions   | Collection of localized descriptions for this Measure.    |
| `TranslationIndexer`                       | TranslatedDisplayFolders | Collection of localized Display Folders for this Measure. |

Methods

| Type                 | 姓名                                                                                                                      | Summary |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------- | ------- |
| `Boolean`            | Browsable(`String` propertyName)                                                                     |         |
| `TabularNamedObject` | Clone(`String` newName = null, `Boolean` includeTranslations = True)                                 |         |
| `TabularNamedObject` | CloneTo(`Table` table, `String` newName = null, `Boolean` includeTranslations = True)                |         |
| `void`               | Delete()                                                                                             |         |
| `Boolean`            | Editable(`String` propertyName)                                                                      |         |
| `String`             | GetAnnotation(`String` name)                                                                         |         |
| `void`               | Init()                                                                                               |         |
| `void`               | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue)                       |         |
| `void`               | OnPropertyChanging(`String` propertyName, `Object` newValue, `Boolean&` undoable, `Boolean&` cancel) |         |
| `void`               | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True)                              |         |
| `void`               | Undelete(`ITabularObjectCollection` collection)                                                      |         |

## `MeasureCollection`

Collection class for Measure. Provides convenient properties for setting a property on multiple objects at once.

```csharp
public class TabularEditor.TOMWrapper.MeasureCollection
    : TabularObjectCollection<Measure, Measure, Table>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Measure>, IEnumerable<Measure>, IList<Measure>, ITabularObjectCollection, IExpandableIndexer

```

属性

| Type      | 姓名              | Summary |
| --------- | --------------- | ------- |
| `String`  | 说明              |         |
| `String`  | DisplayFolder   |         |
| `String`  | 表达式             |         |
| `String`  | 格式字符串           |         |
| `Boolean` | IsHidden        |         |
| `Boolean` | IsSimpleMeasure |         |
| `KPI`     | KPI             |         |
| `Table`   | Parent          |         |

Methods

| Type     | 姓名                            | Summary |
| -------- | ----------------------------- | ------- |
| `String` | ToString() |         |

## `Model`

Base class declaration for Model

```csharp
public class TabularEditor.TOMWrapper.Model
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject, ITabularObjectContainer

```

Fields

| Type           | 姓名                 | Summary |
| -------------- | ------------------ | ------- |
| `LogicalGroup` | GroupDataSources   |         |
| `LogicalGroup` | GroupPerspectives  |         |
| `LogicalGroup` | GroupRelationships |         |
| `LogicalGroup` | GroupRoles         |         |
| `LogicalGroup` | GroupTables        |         |
| `LogicalGroup` | GroupTranslations  |         |

属性

| Type                         | 姓名                     | Summary                                                              |
| ---------------------------- | ---------------------- | -------------------------------------------------------------------- |
| `IEnumerable<Column>`        | AllColumns             |                                                                      |
| `IEnumerable<Hierarchy>`     | AllHierarchies         |                                                                      |
| `IEnumerable<Level>`         | AllLevels              |                                                                      |
| `IEnumerable<Measure>`：度量值集合 | AllMeasures            |                                                                      |
| `String`                     | Collation              | Gets or sets the Collation of the Model.             |
| `String`                     | Culture                | Gets or sets the Culture of the Model.               |
| `CultureCollection`          | Cultures               |                                                                      |
| `Database`                   | 数据库                    |                                                                      |
| `DataSourceCollection`       | DataSources            |                                                                      |
| `DataViewType`               | DefaultDataView        | Gets or sets the DefaultDataView of the Model.       |
| `ModeType`                   | DefaultMode            | Gets or sets the DefaultMode of the Model.           |
| `String`                     | 说明                     | Gets or sets the Description of the Model.           |
| `Boolean`                    | HasLocalChanges        | Gets or sets the HasLocalChanges of the Model.       |
| `IEnumerable<LogicalGroup>`  | LogicalChildGroups     |                                                                      |
| `Model`                      | MetadataObject         |                                                                      |
| `PerspectiveCollection`      | 透视                     |                                                                      |
| `RelationshipCollection2`    | 关系                     |                                                                      |
| `ModelRoleCollection`        | Roles                  |                                                                      |
| `String`                     | StorageLocation        | Gets or sets the StorageLocation of the Model.       |
| `TableCollection`            | 表                      |                                                                      |
| `TranslationIndexer`         | TranslatedDescriptions | Collection of localized descriptions for this Model. |

Methods

| Type                               | 姓名                                                                                         | Summary |
| ---------------------------------- | ------------------------------------------------------------------------------------------ | ------- |
| `CalculatedTable`                  | AddCalculatedTable()                                                    |         |
| `Perspective`                      | AddPerspective(`String` name = null)                                    |         |
| `SingleColumnRelationship`         | AddRelationship()                                                       |         |
| `ModelRole`                        | AddRole(`String` name = null)                                           |         |
| `Table`                            | AddTable()                                                              |         |
| `Culture`                          | AddTranslation(`String` cultureId)                                      |         |
| `String`                           | GetAnnotation(`String` name)                                            |         |
| `IEnumerable<ITabularNamedObject>` | GetChildren()                                                           |         |
| `void`                             | Init()                                                                  |         |
| `void`                             | LoadChildObjects()                                                      |         |
| `void`                             | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |         |

## `ModelRole`

Base class declaration for ModelRole

```csharp
public class TabularEditor.TOMWrapper.ModelRole
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject

```

属性

| Type                 | 姓名                     | Summary                                                                  |
| -------------------- | ---------------------- | ------------------------------------------------------------------------ |
| `String`             | 说明                     | Gets or sets the Description of the ModelRole.           |
| `ModelRole`          | MetadataObject         |                                                                          |
| `ModelPermission`    | ModelPermission        | Gets or sets the ModelPermission of the ModelRole.       |
| `RoleRLSIndexer`     | RowLevelSecurity       |                                                                          |
| `TranslationIndexer` | TranslatedDescriptions | Collection of localized descriptions for this ModelRole. |

Methods

| Type                 | 姓名                                                                                         | Summary |
| -------------------- | ------------------------------------------------------------------------------------------ | ------- |
| `TabularNamedObject` | Clone(`String` newName, `Boolean` includeTranslations)                  |         |
| `void`               | Delete()                                                                |         |
| `String`             | GetAnnotation(`String` name)                                            |         |
| `void`               | InitRLSIndexer()                                                        |         |
| `void`               | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |         |
| `void`               | Undelete(`ITabularObjectCollection` collection)                         |         |

## `ModelRoleCollection`

Collection class for ModelRole. Provides convenient properties for setting a property on multiple objects at once.

```csharp
public class TabularEditor.TOMWrapper.ModelRoleCollection
    : TabularObjectCollection<ModelRole, ModelRole, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<ModelRole>, IEnumerable<ModelRole>, IList<ModelRole>, ITabularObjectCollection, IExpandableIndexer

```

属性

| Type              | 姓名              | Summary |
| ----------------- | --------------- | ------- |
| `String`          | 说明              |         |
| `ModelPermission` | ModelPermission |         |
| `Model`           | Parent          |         |

Methods

| Type     | 姓名                            | Summary |
| -------- | ----------------------------- | ------- |
| `String` | ToString() |         |

## `NullTree`

```csharp
public class TabularEditor.TOMWrapper.NullTree
    : TabularTree, INotifyPropertyChanged

```

Methods

| Type   | 姓名                                                                                       | Summary |
| ------ | ---------------------------------------------------------------------------------------- | ------- |
| `void` | OnNodesChanged(`ITabularObject` nodeItem)                             |         |
| `void` | OnNodesInserted(`ITabularObject` parent, `ITabularObject[]` children) |         |
| `void` | OnNodesRemoved(`ITabularObject` parent, `ITabularObject[]` children)  |         |
| `void` | OnStructureChanged(`ITabularNamedObject` obj = null)                  |         |

## `ObjectOrder`

```csharp
public enum TabularEditor.TOMWrapper.ObjectOrder
    : Enum, IComparable, IFormattable, IConvertible

```

Enum

| 值   | 姓名           | Summary |
| --- | ------------ | ------- |
| `0` | Alphabetical |         |
| `1` | Metadata     |         |

## `ObjectType`

```csharp
public enum TabularEditor.TOMWrapper.ObjectType
    : Enum, IComparable, IFormattable, IConvertible

```

Enum

| 值      | 姓名                   | Summary |
| ------ | -------------------- | ------- |
| `-2`   | Group                |         |
| `-1`   | Folder               |         |
| `1`    | 模型                   |         |
| `2`    | DataSource           |         |
| `3`    | 表                    |         |
| `4`    | Column               |         |
| `5`    | AttributeHierarchy   |         |
| `6`    | Partition            |         |
| `7`    | Relationship         |         |
| `8`    | 度量值                  |         |
| `9`    | 层次结构                 |         |
| `10`   | 级别                   |         |
| `11`   | Annotation           |         |
| `12`   | KPI                  |         |
| `13`   | Culture              |         |
| `14`   | ObjectTranslation    |         |
| `15`   | LinguisticMetadata   |         |
| `29`   | Perspective          |         |
| `30`   | PerspectiveTable     |         |
| `31`   | PerspectiveColumn    |         |
| `32`   | PerspectiveHierarchy |         |
| `33`   | PerspectiveMeasure   |         |
| `34`   | 角色                   |         |
| `35`   | RoleMembership       |         |
| `36`   | TablePermission      |         |
| `1000` | 数据库                  |         |

## `Partition`

Base class declaration for Partition

```csharp
public class TabularEditor.TOMWrapper.Partition
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDynamicPropertyObject, IErrorMessageObject, ITabularTableObject, IDescriptionObject, IAnnotationObject

```

属性

| Type                  | 姓名                     | Summary                                                                  |
| --------------------- | ---------------------- | ------------------------------------------------------------------------ |
| `DataSource`          | DataSource             |                                                                          |
| `DataViewType`        | DataView               | Gets or sets the DataView of the Partition.              |
| `String`              | 说明                     | Gets or sets the Description of the Partition.           |
| `String`              | ErrorMessage           | Gets or sets the ErrorMessage of the Partition.          |
| `String`              | 表达式                    |                                                                          |
| `Partition`           | MetadataObject         |                                                                          |
| `ModeType`            | 模式                     | Gets or sets the Mode of the Partition.                  |
| `String`              | 姓名                     |                                                                          |
| `String`              | Query                  |                                                                          |
| `DateTime`            | RefreshedTime          |                                                                          |
| `String`              | Source                 |                                                                          |
| `PartitionSourceType` | SourceType             | Gets or sets the SourceType of the Partition.            |
| `ObjectState`         | State                  | Gets or sets the State of the Partition.                 |
| `Table`               | 表                      |                                                                          |
| `TranslationIndexer`  | TranslatedDescriptions | Collection of localized descriptions for this Partition. |

Methods

| Type      | 姓名                                                                                         | Summary |
| --------- | ------------------------------------------------------------------------------------------ | ------- |
| `Boolean` | Browsable(`String` propertyName)                                        |         |
| `Boolean` | Editable(`String` propertyName)                                         |         |
| `String`  | GetAnnotation(`String` name)                                            |         |
| `void`    | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |         |
| `void`    | Undelete(`ITabularObjectCollection` collection)                         |         |

## `PartitionCollection`

Collection class for Partition. Provides convenient properties for setting a property on multiple objects at once.

```csharp
public class TabularEditor.TOMWrapper.PartitionCollection
    : TabularObjectCollection<Partition, Partition, Table>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Partition>, IEnumerable<Partition>, IList<Partition>, ITabularObjectCollection, IExpandableIndexer

```

属性

| Type           | 姓名       | Summary |
| -------------- | -------- | ------- |
| `DataViewType` | DataView |         |
| `String`       | 说明       |         |
| `ModeType`     | 模式       |         |
| `Table`        | Parent   |         |

Methods

| Type     | 姓名                            | Summary |
| -------- | ----------------------------- | ------- |
| `String` | ToString() |         |

## `Perspective`

Base class declaration for Perspective

```csharp
public class TabularEditor.TOMWrapper.Perspective
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject

```

属性

| Type                 | 姓名                     | Summary                                                                    |
| -------------------- | ---------------------- | -------------------------------------------------------------------------- |
| `String`             | 说明                     | Gets or sets the Description of the Perspective.           |
| `Perspective`        | MetadataObject         |                                                                            |
| `TranslationIndexer` | TranslatedDescriptions | Collection of localized descriptions for this Perspective. |

Methods

| Type                 | 姓名                                                                                         | Summary |
| -------------------- | ------------------------------------------------------------------------------------------ | ------- |
| `TabularNamedObject` | Clone(`String` newName, `Boolean` includeTranslations)                  |         |
| `void`               | Delete()                                                                |         |
| `String`             | GetAnnotation(`String` name)                                            |         |
| `void`               | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |         |
| `void`               | Undelete(`ITabularObjectCollection` collection)                         |         |

## `PerspectiveCollection`

Collection class for Perspective. Provides convenient properties for setting a property on multiple objects at once.

```csharp
public class TabularEditor.TOMWrapper.PerspectiveCollection
    : TabularObjectCollection<Perspective, Perspective, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Perspective>, IEnumerable<Perspective>, IList<Perspective>, ITabularObjectCollection, IExpandableIndexer

```

属性

| Type     | 姓名     | Summary |
| -------- | ------ | ------- |
| `String` | 说明     |         |
| `Model`  | Parent |         |

Methods

| Type     | 姓名                            | Summary |
| -------- | ----------------------------- | ------- |
| `String` | ToString() |         |

## `PerspectiveColumnIndexer`

```csharp
public class TabularEditor.TOMWrapper.PerspectiveColumnIndexer
    : PerspectiveIndexer, IEnumerable<Boolean>, IEnumerable, IExpandableIndexer

```

属性

| Type     | 姓名     | Summary |
| -------- | ------ | ------- |
| `Column` | Column |         |

Methods

| Type   | 姓名                                                                                 | Summary |
| ------ | ---------------------------------------------------------------------------------- | ------- |
| `void` | Refresh()                                                       |         |
| `void` | SetInPerspective(`Perspective` perspective, `Boolean` included) |         |

## `PerspectiveHierarchyIndexer`

```csharp
public class TabularEditor.TOMWrapper.PerspectiveHierarchyIndexer
    : PerspectiveIndexer, IEnumerable<Boolean>, IEnumerable, IExpandableIndexer

```

属性

| Type        | 姓名   | Summary |
| ----------- | ---- | ------- |
| `Hierarchy` | 层次结构 |         |

Methods

| Type   | 姓名                                                                                 | Summary |
| ------ | ---------------------------------------------------------------------------------- | ------- |
| `void` | Refresh()                                                       |         |
| `void` | SetInPerspective(`Perspective` perspective, `Boolean` included) |         |

## `PerspectiveIndexer`

```csharp
public abstract class TabularEditor.TOMWrapper.PerspectiveIndexer
    : IEnumerable<Boolean>, IEnumerable, IExpandableIndexer

```

Fields

| Type                 | 姓名            | Summary |
| -------------------- | ------------- | ------- |
| `TabularNamedObject` | TabularObject |         |

属性

| Type                               | 姓名             | Summary |
| ---------------------------------- | -------------- | ------- |
| `Boolean`                          | Item           |         |
| `Boolean`                          | Item           |         |
| `IEnumerable<String>`              | Keys           |         |
| `Dictionary<Perspective, Boolean>` | PerspectiveMap |         |
| `String`                           | Summary        |         |

Methods

| Type                          | 姓名                                                                                 | Summary                                                  |
| ----------------------------- | ---------------------------------------------------------------------------------- | -------------------------------------------------------- |
| `void`                        | All()                                                           | Includes the object in all perspectives. |
| `Dictionary<String, Boolean>` | Copy()                                                          |                                                          |
| `void`                        | CopyFrom(`PerspectiveIndexer` source)                           |                                                          |
| `void`                        | CopyFrom(`IDictionary<String, Boolean>` source)                 |                                                          |
| `String`                      | GetDisplayName(`String` key)                                    |                                                          |
| `IEnumerator<Boolean>`        | GetEnumerator()                                                 |                                                          |
| `void`                        | None()                                                          |                                                          |
| `void`                        | Refresh()                                                       |                                                          |
| `void`                        | SetInPerspective(`Perspective` perspective, `Boolean` included) |                                                          |

## `PerspectiveMeasureIndexer`

```csharp
public class TabularEditor.TOMWrapper.PerspectiveMeasureIndexer
    : PerspectiveIndexer, IEnumerable<Boolean>, IEnumerable, IExpandableIndexer

```

属性

| Type      | 姓名  | Summary |
| --------- | --- | ------- |
| `Measure` | 度量值 |         |

Methods

| Type   | 姓名                                                                                 | Summary |
| ------ | ---------------------------------------------------------------------------------- | ------- |
| `void` | Refresh()                                                       |         |
| `void` | SetInPerspective(`Perspective` perspective, `Boolean` included) |         |

## `PerspectiveTableIndexer`

```csharp
public class TabularEditor.TOMWrapper.PerspectiveTableIndexer
    : PerspectiveIndexer, IEnumerable<Boolean>, IEnumerable, IExpandableIndexer

```

属性

| Type      | 姓名   | Summary |
| --------- | ---- | ------- |
| `Boolean` | Item |         |
| `Table`   | 表    |         |

Methods

| Type               | 姓名                                                                                 | Summary |
| ------------------ | ---------------------------------------------------------------------------------- | ------- |
| `PerspectiveTable` | EnsurePTExists(`Perspective` perspective)                       |         |
| `void`             | Refresh()                                                       |         |
| `void`             | SetInPerspective(`Perspective` perspective, `Boolean` included) |         |

## `ProviderDataSource`

Base class declaration for ProviderDataSource

```csharp
public class TabularEditor.TOMWrapper.ProviderDataSource
    : DataSource, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject, IDynamicPropertyObject

```

属性

| Type                  | 姓名                | Summary                                                                       |
| --------------------- | ----------------- | ----------------------------------------------------------------------------- |
| `String`              | Account           | Gets or sets the Account of the ProviderDataSource.           |
| `String`              | ConnectionString  | Gets or sets the ConnectionString of the ProviderDataSource.  |
| `ImpersonationMode`   | ImpersonationMode | Gets or sets the ImpersonationMode of the ProviderDataSource. |
| `DatasourceIsolation` | Isolation         | Gets or sets the Isolation of the ProviderDataSource.         |
| `Boolean`             | IsPowerBIMashup   |                                                                               |
| `String`              | 地点                |                                                                               |
| `Int32`               | MaxConnections    | Gets or sets the MaxConnections of the ProviderDataSource.    |
| `ProviderDataSource`  | MetadataObject    |                                                                               |
| `String`              | MQuery            |                                                                               |
| `String`              | 姓名                |                                                                               |
| `String`              | Password          | Gets or sets the Password of the ProviderDataSource.          |
| `String`              | Provider          | Gets or sets the Provider of the ProviderDataSource.          |
| `String`              | SourceID          |                                                                               |
| `Int32`               | Timeout           | Gets or sets the Timeout of the ProviderDataSource.           |

Methods

| Type      | 姓名                                                  | Summary |
| --------- | --------------------------------------------------- | ------- |
| `Boolean` | Browsable(`String` propertyName) |         |
| `Boolean` | Editable(`String` propertyName)  |         |
| `void`    | Init()                           |         |

## `Relationship`

Base class declaration for Relationship

```csharp
public abstract class TabularEditor.TOMWrapper.Relationship
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IAnnotationObject

```

属性

| Type                           | 姓名                         | Summary                                                                          |
| ------------------------------ | -------------------------- | -------------------------------------------------------------------------------- |
| `CrossFilteringBehavior`       | CrossFilteringBehavior     | Gets or sets the CrossFilteringBehavior of the Relationship.     |
| `Table`                        | FromTable                  | Gets or sets the FromTable of the Relationship.                  |
| `Boolean`                      | IsActive                   | Gets or sets the IsActive of the Relationship.                   |
| `DateTimeRelationshipBehavior` | JoinOnDateBehavior         | Gets or sets the JoinOnDateBehavior of the Relationship.         |
| `Relationship`                 | MetadataObject             |                                                                                  |
| `Boolean`                      | RelyOnReferentialIntegrity | Gets or sets the RelyOnReferentialIntegrity of the Relationship. |
| `SecurityFilteringBehavior`    | SecurityFilteringBehavior  | Gets or sets the SecurityFilteringBehavior of the Relationship.  |
| `ObjectState`                  | State                      | Gets or sets the State of the Relationship.                      |
| `Table`                        | ToTable                    | Gets or sets the ToTable of the Relationship.                    |
| `RelationshipType`             | Type                       | Gets or sets the Type of the Relationship.                       |

Methods

| Type     | 姓名                                                                                         | Summary |
| -------- | ------------------------------------------------------------------------------------------ | ------- |
| `String` | GetAnnotation(`String` name)                                            |         |
| `void`   | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |         |

## `RelationshipCollection`

Collection class for Relationship. Provides convenient properties for setting a property on multiple objects at once.

```csharp
public class TabularEditor.TOMWrapper.RelationshipCollection
    : TabularObjectCollection<Relationship, Relationship, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Relationship>, IEnumerable<Relationship>, IList<Relationship>, ITabularObjectCollection, IExpandableIndexer

```

属性

| Type                           | 姓名                         | Summary |
| ------------------------------ | -------------------------- | ------- |
| `CrossFilteringBehavior`       | CrossFilteringBehavior     |         |
| `Boolean`                      | IsActive                   |         |
| `DateTimeRelationshipBehavior` | JoinOnDateBehavior         |         |
| `Model`                        | Parent                     |         |
| `Boolean`                      | RelyOnReferentialIntegrity |         |
| `SecurityFilteringBehavior`    | SecurityFilteringBehavior  |         |

Methods

| Type     | 姓名                            | Summary |
| -------- | ----------------------------- | ------- |
| `String` | ToString() |         |

## `RelationshipCollection2`

```csharp
public class TabularEditor.TOMWrapper.RelationshipCollection2
    : TabularObjectCollection<SingleColumnRelationship, Relationship, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<SingleColumnRelationship>, IEnumerable<SingleColumnRelationship>, IList<SingleColumnRelationship>, ITabularObjectCollection, IExpandableIndexer

```

属性

| Type                           | 姓名                         | Summary |
| ------------------------------ | -------------------------- | ------- |
| `CrossFilteringBehavior`       | CrossFilteringBehavior     |         |
| `Boolean`                      | IsActive                   |         |
| `DateTimeRelationshipBehavior` | JoinOnDateBehavior         |         |
| `Model`                        | Parent                     |         |
| `Boolean`                      | RelyOnReferentialIntegrity |         |
| `SecurityFilteringBehavior`    | SecurityFilteringBehavior  |         |

Methods

| Type     | 姓名                            | Summary |
| -------- | ----------------------------- | ------- |
| `String` | ToString() |         |

## `RoleRLSIndexer`

The RoleRLSIndexer is used to browse all filters across all tables in the model, for  one specific role. This is in contrast to the TableRLSIndexer, which browses the  filters across all roles in the model, for one specific table.

```csharp
public class TabularEditor.TOMWrapper.RoleRLSIndexer
    : IEnumerable<String>, IEnumerable, IExpandableIndexer

```

Fields

| Type        | 姓名 | Summary |
| ----------- | -- | ------- |
| `ModelRole` | 角色 |         |

属性

| Type                        | 姓名      | Summary |
| --------------------------- | ------- | ------- |
| `String`                    | Item    |         |
| `String`                    | Item    |         |
| `IEnumerable<String>`       | Keys    |         |
| `Dictionary<Table, String>` | RLSMap  |         |
| `String`                    | Summary |         |

Methods

| Type                  | 姓名                                                                  | Summary |
| --------------------- | ------------------------------------------------------------------- | ------- |
| `void`                | Clear()                                          |         |
| `void`                | CopyFrom(`RoleRLSIndexer` source)                |         |
| `String`              | GetDisplayName(`String` key)                     |         |
| `IEnumerator<String>` | GetEnumerator()                                  |         |
| `void`                | Refresh()                                        |         |
| `void`                | SetRLS(`Table` table, `String` filterExpression) |         |

## `SerializeOptions`

```csharp
public class TabularEditor.TOMWrapper.SerializeOptions

```

Fields

| Type              | 姓名                       | Summary |
| ----------------- | ------------------------ | ------- |
| `Boolean`         | IgnoreInferredObjects    |         |
| `Boolean`         | IgnoreInferredProperties |         |
| `Boolean`         | IgnoreTimestamps         |         |
| `HashSet<String>` | 级别                       |         |
| `Boolean`         | PrefixFilenames          |         |
| `Boolean`         | SplitMultilineStrings    |         |

Static Properties

| Type               | 姓名  | Summary |
| ------------------ | --- | ------- |
| `SerializeOptions` | 默认值 |         |

## `SingleColumnRelationship`

Base class declaration for SingleColumnRelationship

```csharp
public class TabularEditor.TOMWrapper.SingleColumnRelationship
    : Relationship, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IAnnotationObject, IDynamicPropertyObject

```

属性

| Type                         | 姓名              | Summary                                                                           |
| ---------------------------- | --------------- | --------------------------------------------------------------------------------- |
| `RelationshipEndCardinality` | FromCardinality | Gets or sets the FromCardinality of the SingleColumnRelationship. |
| `Column`                     | FromColumn      | Gets or sets the FromColumn of the SingleColumnRelationship.      |
| `SingleColumnRelationship`   | MetadataObject  |                                                                                   |
| `String`                     | 姓名              |                                                                                   |
| `RelationshipEndCardinality` | ToCardinality   | Gets or sets the ToCardinality of the SingleColumnRelationship.   |
| `Column`                     | ToColumn        | Gets or sets the ToColumn of the SingleColumnRelationship.        |

Methods

| Type      | 姓名                                                                                                                      | Summary |
| --------- | ----------------------------------------------------------------------------------------------------------------------- | ------- |
| `Boolean` | Browsable(`String` propertyName)                                                                     |         |
| `void`    | Delete()                                                                                             |         |
| `Boolean` | Editable(`String` propertyName)                                                                      |         |
| `void`    | Init()                                                                                               |         |
| `void`    | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue)                       |         |
| `void`    | OnPropertyChanging(`String` propertyName, `Object` newValue, `Boolean&` undoable, `Boolean&` cancel) |         |
| `String`  | ToString()                                                                                           |         |
| `void`    | Undelete(`ITabularObjectCollection` collection)                                                      |         |

## `Table`

Base class declaration for Table

```csharp
public class TabularEditor.TOMWrapper.Table
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IHideableObject, IDescriptionObject, IAnnotationObject, ITabularObjectContainer, IDetailObjectContainer, ITabularPerspectiveObject, IDaxObject, IDynamicPropertyObject, IErrorMessageObject

```

属性

| Type                         | 姓名                     | Summary                                                              |
| ---------------------------- | ---------------------- | -------------------------------------------------------------------- |
| `IEnumerable<Level>`         | AllLevels              |                                                                      |
| `ColumnCollection`           | 列                      |                                                                      |
| `String`                     | DataCategory           | Gets or sets the DataCategory of the Table.          |
| `String`                     | DaxObjectFullName      |                                                                      |
| `String`                     | DaxObjectName          |                                                                      |
| `String`                     | DaxTableName           |                                                                      |
| `HashSet<IExpressionObject>` | Dependants             |                                                                      |
| `String`                     | 说明                     | Gets or sets the Description of the Table.           |
| `String`                     | ErrorMessage           |                                                                      |
| `HierarchyCollection`        | 层次结构                   |                                                                      |
| `PerspectiveIndexer`         | InPerspective          |                                                                      |
| `Boolean`                    | IsHidden               | Gets or sets the IsHidden of the Table.              |
| `MeasureCollection`          | 度量值                    |                                                                      |
| `Table`                      | MetadataObject         |                                                                      |
| `String`                     | 姓名                     |                                                                      |
| `Table`                      | ParentTable            |                                                                      |
| `PartitionCollection`        | 分区                     |                                                                      |
| `TableRLSIndexer`            | RowLevelSecurity       |                                                                      |
| `String`                     | Source                 |                                                                      |
| `PartitionSourceType`        | SourceType             |                                                                      |
| `TranslationIndexer`         | TranslatedDescriptions | Collection of localized descriptions for this Table. |

Methods

| Type                               | 姓名                                                                                                                        | Summary                                                                          |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `CalculatedColumn`                 | AddCalculatedColumn(`String` name = null, `String` expression = null, `String` displayFolder = null)   |                                                                                  |
| `DataColumn`                       | AddDataColumn(`String` name = null, `String` sourceColumn = null, `String` displayFolder = null)       |                                                                                  |
| `Hierarchy`                        | AddHierarchy(`String` name = null, `String` displayFolder = null, `Column[]` levels)                   |                                                                                  |
| `Hierarchy`                        | AddHierarchy(`String` name, `String` displayFolder = null, `String[]` levels)                          |                                                                                  |
| `Measure`                          | AddMeasure(`String` name = null, `String` expression = null, `String` displayFolder = null)            |                                                                                  |
| `Boolean`                          | Browsable(`String` propertyName)                                                                       |                                                                                  |
| `void`                             | CheckChildrenErrors()                                                                                  |                                                                                  |
| `void`                             | Children_CollectionChanged(`Object` sender, `NotifyCollectionChangedEventArgs` e) |                                                                                  |
| `TabularNamedObject`               | Clone(`String` newName = null, `Boolean` includeTranslations = False)                                  |                                                                                  |
| `void`                             | Delete()                                                                                               |                                                                                  |
| `Boolean`                          | Editable(`String` propertyName)                                                                        |                                                                                  |
| `String`                           | GetAnnotation(`String` name)                                                                           |                                                                                  |
| `IEnumerable<ITabularNamedObject>` | GetChildren()                                                                                          | Returns all columns, measures and hierarchies inside this table. |
| `IEnumerable<IDetailObject>`       | GetChildrenByFolders(`Boolean` recursive)                                                              |                                                                                  |
| `void`                             | Init()                                                                                                 |                                                                                  |
| `void`                             | InitRLSIndexer()                                                                                       |                                                                                  |
| `void`                             | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue)                         |                                                                                  |
| `void`                             | OnPropertyChanging(`String` propertyName, `Object` newValue, `Boolean&` undoable, `Boolean&` cancel)   |                                                                                  |
| `void`                             | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True)                                |                                                                                  |
| `void`                             | Undelete(`ITabularObjectCollection` collection)                                                        |                                                                                  |

Static Fields

| Type     | 姓名                    | Summary |
| -------- | --------------------- | ------- |
| `Char[]` | InvalidTableNameChars |         |

## `TableCollection`

Collection class for Table. Provides convenient properties for setting a property on multiple objects at once.

```csharp
public class TabularEditor.TOMWrapper.TableCollection
    : TabularObjectCollection<Table, Table, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Table>, IEnumerable<Table>, IList<Table>, ITabularObjectCollection, IExpandableIndexer

```

属性

| Type      | 姓名           | Summary |
| --------- | ------------ | ------- |
| `String`  | DataCategory |         |
| `String`  | 说明           |         |
| `Boolean` | IsHidden     |         |
| `Model`   | Parent       |         |

Methods

| Type     | 姓名                            | Summary |
| -------- | ----------------------------- | ------- |
| `String` | ToString() |         |

## `TableExtension`

```csharp
public static class TabularEditor.TOMWrapper.TableExtension

```

Static Methods

| Type                  | 姓名                                                   | Summary |
| --------------------- | ---------------------------------------------------- | ------- |
| `PartitionSourceType` | GetSourceType(this `Table` table) |         |

## `TableRLSIndexer`

The TableRLSIndexer is used to browse all filters defined on one specific table, across  all roles in the model. This is in contrast to the RoleRLSIndexer, which browses the  filters across all tables for one specific role.

```csharp
public class TabularEditor.TOMWrapper.TableRLSIndexer
    : IEnumerable<String>, IEnumerable, IExpandableIndexer

```

Fields

| Type    | 姓名 | Summary |
| ------- | -- | ------- |
| `Table` | 表  |         |

属性

| Type                            | 姓名      | Summary |
| ------------------------------- | ------- | ------- |
| `String`                        | Item    |         |
| `String`                        | Item    |         |
| `IEnumerable<String>`           | Keys    |         |
| `Dictionary<ModelRole, String>` | RLSMap  |         |
| `String`                        | Summary |         |

Methods

| Type                  | 姓名                                                                     | Summary |
| --------------------- | ---------------------------------------------------------------------- | ------- |
| `void`                | Clear()                                             |         |
| `void`                | CopyFrom(`TableRLSIndexer` source)                  |         |
| `String`              | GetDisplayName(`String` key)                        |         |
| `IEnumerator<String>` | GetEnumerator()                                     |         |
| `void`                | Refresh()                                           |         |
| `void`                | SetRLS(`ModelRole` role, `String` filterExpression) |         |

## `TabularCollectionHelper`

```csharp
public static class TabularEditor.TOMWrapper.TabularCollectionHelper

```

Static Methods

| Type   | 姓名                                                                                                                      | Summary |
| ------ | ----------------------------------------------------------------------------------------------------------------------- | ------- |
| `void` | InPerspective(this `IEnumerable<Table>` tables, `String` perspective, `Boolean` value)               |         |
| `void` | InPerspective(this `IEnumerable<Column>` columns, `String` perspective, `Boolean` value)             |         |
| `void` | InPerspective(this `IEnumerable<Hierarchy>` hierarchies, `String` perspective, `Boolean` value)      |         |
| `void` | InPerspective(this `IEnumerable<Measure>` measures, `String` perspective, `Boolean` value)           |         |
| `void` | InPerspective(this `IEnumerable<Table>` tables, `Perspective` perspective, `Boolean` value)          |         |
| `void` | InPerspective(this `IEnumerable<Column>` columns, `Perspective` perspective, `Boolean` value)        |         |
| `void` | InPerspective(this `IEnumerable<Hierarchy>` hierarchies, `Perspective` perspective, `Boolean` value) |         |
| `void` | InPerspective(this `IEnumerable<Measure>` measures, `Perspective` perspective, `Boolean` value)      |         |
| `void` | SetDisplayFolder(this `IEnumerable<Measure>` measures, `String` displayFolder)                       |         |

## `TabularCommonActions`

Provides convenient methods for common actions on a Tabular Model, that often involve changing multiple objects at once.  For example, these methods may be used to easily perform UI drag and drop operations that will change hierarchy levels,  display folders, etc.

```csharp
public class TabularEditor.TOMWrapper.TabularCommonActions

```

属性

| Type                  | 姓名      | Summary |
| --------------------- | ------- | ------- |
| `TabularModelHandler` | Handler |         |

Methods

| Type     | 姓名                                                                                                                              | Summary |
| -------- | ------------------------------------------------------------------------------------------------------------------------------- | ------- |
| `void`   | AddColumnsToHierarchy(`IEnumerable<Column>` columns, `Hierarchy` hierarchy, `Int32` firstOrdinal = -1)       |         |
| `Level`  | AddColumnToHierarchy(`Column` column, `Hierarchy` hierarchy, `Int32` ordinal = -1)                           |         |
| `void`   | MoveObjects(`IEnumerable<IDetailObject>` objects, `Table` newTable, `Culture` culture)                       |         |
| `String` | NewColumnName(`String` prefix, `Table` table)                                                                |         |
| `String` | NewMeasureName(`String` prefix)                                                                              |         |
| `void`   | ReorderLevels(`IEnumerable<Level>` levels, `Int32` firstOrdinal)                                             |         |
| `void`   | SetContainer(`IEnumerable<IDetailObject>` objects, `IDetailObjectContainer` newContainer, `Culture` culture) |         |

## `TabularConnection`

```csharp
public static class TabularEditor.TOMWrapper.TabularConnection

```

Static Methods

| Type     | 姓名                                                                                                | Summary |
| -------- | ------------------------------------------------------------------------------------------------- | ------- |
| `String` | GetConnectionString(`String` serverName)                                       |         |
| `String` | GetConnectionString(`String` serverName, `String` userName, `String` password) |         |

## `TabularCultureHelper`

```csharp
public static class TabularEditor.TOMWrapper.TabularCultureHelper

```

Static Methods

| Type      | 姓名                                                                                                                              | Summary |
| --------- | ------------------------------------------------------------------------------------------------------------------------------- | ------- |
| `Boolean` | ImportTranslations(`String` culturesJson, `Model` Model, `Boolean` overwriteExisting, `Boolean` haltOnError) |         |

## `TabularDeployer`

```csharp
public class TabularEditor.TOMWrapper.TabularDeployer

```

Static Methods

| Type               | 姓名                                                                                                                                | Summary                                                                                                                                                                                                                                                                      |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `void`             | Deploy(`Database` db, `String` targetConnectionString, `String` targetDatabaseName)                            | Deploys the specified database to the specified target server and database ID, using the specified options.  Returns a list of DAX errors (if any) on objects inside the database, in case the deployment was successful. |
| `DeploymentResult` | Deploy(`Database` db, `String` targetConnectionString, `String` targetDatabaseID, `DeploymentOptions` options) | Deploys the specified database to the specified target server and database ID, using the specified options.  Returns a list of DAX errors (if any) on objects inside the database, in case the deployment was successful. |
| `String`           | GetTMSL(`Database` db, `Server` server, `String` targetDatabaseID, `DeploymentOptions` options)                |                                                                                                                                                                                                                                                                              |
| `void`             | SaveModelMetadataBackup(`String` connectionString, `String` targetDatabaseID, `String` backupFilePath)         |                                                                                                                                                                                                                                                                              |
| `void`             | WriteZip(`String` fileName, `String` content)                                                                  |                                                                                                                                                                                                                                                                              |

## `TabularModelHandler`

```csharp
public class TabularEditor.TOMWrapper.TabularModelHandler
    : IDisposable

```

Fields

| Type                                           | 姓名                 | Summary |
| ---------------------------------------------- | ------------------ | ------- |
| `Dictionary<String, ITabularObjectCollection>` | WrapperCollections |         |
| `Dictionary<MetadataObject, TabularObject>`    | WrapperLookup      |         |

属性

| Type                                        | 姓名                       | Summary                                                                                                                                                                                                                                                                                      |
| ------------------------------------------- | ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TabularCommonActions`                      | Actions                  |                                                                                                                                                                                                                                                                                              |
| `Boolean`                                   | AutoFixup                | Specifies whether object name changes (tables, column, measures) should result in  automatic DAX expression updates to reflect the changed names. When set to true,  all expressions in the model are parsed, to build a dependency tree. |
| `Database`                                  | 数据库                      |                                                                                                                                                                                                                                                                                              |
| `Boolean`                                   | DelayBuildDependencyTree |                                                                                                                                                                                                                                                                                              |
| `IList<Tuple<NamedMetadataObject, String>>` | Errors                   |                                                                                                                                                                                                                                                                                              |
| `Boolean`                                   | HasUnsavedChanges        |                                                                                                                                                                                                                                                                                              |
| `Boolean`                                   | IsConnected              |                                                                                                                                                                                                                                                                                              |
| `Model`                                     | 模型                       |                                                                                                                                                                                                                                                                                              |
| `String`                                    | 状态                       |                                                                                                                                                                                                                                                                                              |
| `TabularTree`                               | Tree                     |                                                                                                                                                                                                                                                                                              |
| `UndoManager`                               | UndoManager              |                                                                                                                                                                                                                                                                                              |
| `Int64`                                     | Version                  |                                                                                                                                                                                                                                                                                              |

Methods

| Type                        | 姓名                                                                                                                 | Summary                                                                                                                                                                                                                                                                                            |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `IDetailObject`             | Add(`AddObjectType` objectType, `IDetailObjectContainer` container)                             |                                                                                                                                                                                                                                                                                                    |
| `void`                      | BeginUpdate(`String` undoName)                                                                  |                                                                                                                                                                                                                                                                                                    |
| `void`                      | BuildDependencyTree(`IExpressionObject` expressionObj)                                          |                                                                                                                                                                                                                                                                                                    |
| `void`                      | BuildDependencyTree()                                                                           |                                                                                                                                                                                                                                                                                                    |
| `ConflictInfo`              | CheckConflicts()                                                                                |                                                                                                                                                                                                                                                                                                    |
| `IList<TabularNamedObject>` | DeserializeObjects(`String` json)                                                               |                                                                                                                                                                                                                                                                                                    |
| `void`                      | Dispose()                                                                                       |                                                                                                                                                                                                                                                                                                    |
| `void`                      | DoFixup(`IDaxObject` obj, `String` newName)                                                     | Changes all references to object "obj", to reflect "newName"                                                                                                                                                                                                                                       |
| `Int32`                     | EndUpdate(`Boolean` undoable = True, `Boolean` rollback = False)                                |                                                                                                                                                                                                                                                                                                    |
| `Int32`                     | EndUpdateAll(`Boolean` rollback = False)                                                        |                                                                                                                                                                                                                                                                                                    |
| `Model`                     | GetModel()                                                                                      |                                                                                                                                                                                                                                                                                                    |
| `Boolean`                   | ImportTranslations(`String` culturesJson, `Boolean` overwriteExisting, `Boolean` ignoreInvalid) | Applys translation from a JSON string.                                                                                                                                                                                                                                             |
| `void`                      | SaveDB()                                                                                        | Saves the changes to the database. It is the users responsibility to check if changes were made  to the database since it was loaded to the TOMWrapper. You can use Handler.CheckConflicts() for  this purpose. |
| `void`                      | SaveFile(`String` fileName, `SerializeOptions` options)                                         |                                                                                                                                                                                                                                                                                                    |
| `void`                      | SaveToFolder(`String` path, `SerializeOptions` options)                                         |                                                                                                                                                                                                                                                                                                    |
| `String`                    | ScriptCreateOrReplace()                                                                         | Scripts the entire database                                                                                                                                                                                                                                                                        |
| `String`                    | ScriptCreateOrReplace(`TabularNamedObject` obj)                                                 | Scripts the entire database                                                                                                                                                                                                                                                                        |
| `String`                    | ScriptTranslations(`IEnumerable<Culture>` translations)                                         |                                                                                                                                                                                                                                                                                                    |
| `String`                    | SerializeObjects(`IEnumerable<TabularNamedObject>` objects)                                     |                                                                                                                                                                                                                                                                                                    |
| `void`                      | UpdateFolders(`Table` table)                                                                    |                                                                                                                                                                                                                                                                                                    |
| `void`                      | UpdateLevels(`Hierarchy` hierarchy)                                                             |                                                                                                                                                                                                                                                                                                    |
| `void`                      | UpdateObject(`ITabularObject` obj)                                                              |                                                                                                                                                                                                                                                                                                    |
| `void`                      | UpdateTables()                                                                                  |                                                                                                                                                                                                                                                                                                    |

Static Fields

| Type     | 姓名                                          | Summary |
| -------- | ------------------------------------------- | ------- |
| `String` | PROP_ERRORS            |         |
| `String` | PROP_HASUNSAVEDCHANGES |         |
| `String` | PROP_ISCONNECTED       |         |
| `String` | PROP_STATUS            |         |

Static Properties

| Type                  | 姓名        | Summary |
| --------------------- | --------- | ------- |
| `TabularModelHandler` | Singleton |         |

Static Methods

| Type                                            | 姓名                                                           | Summary |
| ----------------------------------------------- | ------------------------------------------------------------ | ------- |
| `List<Tuple<NamedMetadataObject, String>>`      | CheckErrors(`Database` database)          |         |
| `List<Tuple<NamedMetadataObject, ObjectState>>` | CheckProcessingState(`Database` database) |         |

## `TabularNamedObject`

A TabularObject is a wrapper for the Microsoft.AnalysisServices.Tabular.NamedMetadataObject class.  This wrapper is used for all objects that are to be viewable and editable in the Tabular Editor.  The same base class is used for all kinds of objects in a Tabular Model. This base class provides  method for editing the (localized) name and description.

```csharp
public abstract class TabularEditor.TOMWrapper.TabularNamedObject
    : TabularObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable

```

属性

| Type                  | 姓名              | Summary                                                        |
| --------------------- | --------------- | -------------------------------------------------------------- |
| `Int32`               | MetadataIndex   |                                                                |
| `NamedMetadataObject` | MetadataObject  |                                                                |
| `String`              | 姓名              |                                                                |
| `TranslationIndexer`  | TranslatedNames | Collection of localized names for this object. |

Methods

| Type                 | 姓名                                                                        | Summary                                                                                                                                                                                                                                                                                                |
| -------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `TabularNamedObject` | Clone(`String` newName, `Boolean` includeTranslations) |                                                                                                                                                                                                                                                                                                        |
| `Int32`              | CompareTo(`Object` obj)                                |                                                                                                                                                                                                                                                                                                        |
| `void`               | Delete()                                               |                                                                                                                                                                                                                                                                                                        |
| `void`               | Init()                                                 |                                                                                                                                                                                                                                                                                                        |
| `void`               | Undelete(`ITabularObjectCollection` collection)        | Hacky workaround needed to undo a delete operations.  Derived classes must take care to update any objects "owned" by the  object in question. For example, a Measure must take care of updating  the wrapper for its KPI (if any). |

## `TabularObject`

```csharp
public abstract class TabularEditor.TOMWrapper.TabularObject
    : ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging

```

Fields

| Type                       | 姓名         | Summary |
| -------------------------- | ---------- | ------- |
| `ITabularObjectCollection` | Collection |         |
| `TabularModelHandler`      | Handler    |         |

属性

| Type                 | 姓名                       | Summary |
| -------------------- | ------------------------ | ------- |
| `MetadataObject`     | MetadataObject           |         |
| `Model`              | 模型                       |         |
| `ObjectType`         | ObjectType               |         |
| `String`             | ObjectTypeName           |         |
| `TranslationIndexer` | TranslatedDescriptions   |         |
| `TranslationIndexer` | TranslatedDisplayFolders |         |

Events

| Type                           | 姓名               | Summary |
| ------------------------------ | ---------------- | ------- |
| `PropertyChangedEventHandler`  | PropertyChanged  |         |
| `PropertyChangingEventHandler` | PropertyChanging |         |

Methods

| Type      | 姓名                                                                                                                      | Summary                                                                                                                                                                                                                                      |
| --------- | ----------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `void`    | Init()                                                                                               | Derived members should override this method to instantiate child objects                                                                                                                                                                     |
| `void`    | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue)                       |                                                                                                                                                                                                                                              |
| `void`    | OnPropertyChanging(`String` propertyName, `Object` newValue, `Boolean&` undoable, `Boolean&` cancel) | Called before a property is changed on an object. Derived classes can control how the change is handled.  Throw ArgumentException within this method, to display an error message in the UI. |
| `Boolean` | SetField(`T&` field, `T` value, `String` propertyName = null)                                        |                                                                                                                                                                                                                                              |

## `TabularObjectCollection<T, TT, TP>`

```csharp
public abstract class TabularEditor.TOMWrapper.TabularObjectCollection<T, TT, TP>
    : IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<T>, IEnumerable<T>, IList<T>, ITabularObjectCollection, IExpandableIndexer

```

属性

| Type                                    | 姓名                       | Summary |
| --------------------------------------- | ------------------------ | ------- |
| `String`                                | CollectionName           |         |
| `Int32`                                 | Count                    |         |
| `TabularModelHandler`                   | Handler                  |         |
| `Boolean`                               | IsFixedSize              |         |
| `Boolean`                               | IsReadOnly               |         |
| `Boolean`                               | IsSynchronized           |         |
| `T`                                     | Item                     |         |
| `T`                                     | Item                     |         |
| `IEnumerable<String>`                   | Keys                     |         |
| `NamedMetadataObjectCollection<TT, TP>` | MetadataObjectCollection |         |
| `String`                                | Summary                  |         |
| `Object`                                | SyncRoot                 |         |

Events

| Type                                  | 姓名                | Summary |
| ------------------------------------- | ----------------- | ------- |
| `NotifyCollectionChangedEventHandler` | CollectionChanged |         |

Methods

| Type                       | 姓名                                                         | Summary |
| -------------------------- | ---------------------------------------------------------- | ------- |
| `void`                     | Add(`T` item)                           |         |
| `void`                     | Add(`TabularNamedObject` item)          |         |
| `Int32`                    | Add(`Object` value)                     |         |
| `void`                     | Clear()                                 |         |
| `Boolean`                  | Contains(`T` item)                      |         |
| `Boolean`                  | Contains(`Object` value)                |         |
| `Boolean`                  | Contains(`String` name)                 |         |
| `void`                     | CopyTo(`T[]` array, `Int32` arrayIndex) |         |
| `void`                     | CopyTo(`Array` array, `Int32` index)    |         |
| `void`                     | ForEach(`Action<T>` action)             |         |
| `ITabularObjectCollection` | GetCurrentCollection()                  |         |
| `String`                   | GetDisplayName(`String` key)            |         |
| `IEnumerator<T>`           | GetEnumerator()                         |         |
| `Int32`                    | IndexOf(`TabularNamedObject` obj)       |         |
| `Int32`                    | IndexOf(`T` item)                       |         |
| `Int32`                    | IndexOf(`Object` value)                 |         |
| `void`                     | Insert(`Int32` index, `T` item)         |         |
| `void`                     | Insert(`Int32` index, `Object` value)   |         |
| `void`                     | Refresh()                               |         |
| `void`                     | Remove(`TabularNamedObject` item)       |         |
| `Boolean`                  | Remove(`T` item)                        |         |
| `void`                     | Remove(`Object` value)                  |         |
| `void`                     | RemoveAt(`Int32` index)                 |         |

## `TabularObjectComparer`

```csharp
public class TabularEditor.TOMWrapper.TabularObjectComparer
    : IComparer<ITabularNamedObject>, IComparer

```

属性

| Type          | 姓名    | Summary |
| ------------- | ----- | ------- |
| `ObjectOrder` | Order |         |

Methods

| Type    | 姓名                                                                           | Summary |
| ------- | ---------------------------------------------------------------------------- | ------- |
| `Int32` | Compare(`Object` x, `Object` y)                           |         |
| `Int32` | Compare(`ITabularNamedObject` x, `ITabularNamedObject` y) |         |

## `TabularObjectHelper`

```csharp
public static class TabularEditor.TOMWrapper.TabularObjectHelper

```

Static Methods

| Type      | 姓名                                                                                              | Summary |
| --------- | ----------------------------------------------------------------------------------------------- | ------- |
| `String`  | GetLinqPath(this `TabularNamedObject` obj)                                   |         |
| `String`  | GetName(this `ITabularNamedObject` obj, `Culture` culture)                   |         |
| `String`  | GetObjectPath(this `MetadataObject` obj)                                     |         |
| `String`  | GetObjectPath(this `TabularObject` obj)                                      |         |
| `String`  | GetTypeName(this `ObjectType` objType, `Boolean` plural = False)             |         |
| `String`  | GetTypeName(this `ITabularObject` obj, `Boolean` plural = False)             |         |
| `Boolean` | SetName(this `ITabularNamedObject` obj, `String` newName, `Culture` culture) |         |
| `String`  | SplitCamelCase(this `String` str)                                            |         |

## `TabularTree`

The TabularLogicalModel controls the relation between TabularObjects for display in the TreeViewAdv  control. Each individual TabularObject does not know or care about its logical relation to other  objects (for example, through DisplayFolders in a specific culture). TabularObjects only care  about their physical relations which are inherited from the Tabular Object Model directly (i.e.,  a measure belongs to a table, etc.).

```csharp
public abstract class TabularEditor.TOMWrapper.TabularTree
    : INotifyPropertyChanged

```

Fields

| Type                         | 姓名         | Summary |
| ---------------------------- | ---------- | ------- |
| `Dictionary<String, Folder>` | FolderTree |         |

属性

| Type                  | 姓名          | Summary |
| --------------------- | ----------- | ------- |
| `Culture`             | Culture     |         |
| `String`              | 筛选          |         |
| `TabularModelHandler` | Handler     |         |
| `Model`               | 模型          |         |
| `LogicalTreeOptions`  | Options     |         |
| `Perspective`         | Perspective |         |
| `Int32`               | UpdateLocks |         |

Events

| Type                          | 姓名              | Summary |
| ----------------------------- | --------------- | ------- |
| `PropertyChangedEventHandler` | PropertyChanged |         |

Methods

| Type                   | 姓名                                                                                                           | Summary                                                                                                                                                                                |
| ---------------------- | ------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `void`                 | BeginUpdate()                                                                             |                                                                                                                                                                                        |
| `void`                 | EndUpdate()                                                                               |                                                                                                                                                                                        |
| `IEnumerable`          | GetChildren(`ITabularObjectContainer` tabularObject)                                      | This method encapsulates the logic of how the tree representation of the tabular model should be structured                                                                            |
| `Func<String, String>` | GetFolderMutation(`Object` source, `Object` destination)                                  |                                                                                                                                                                                        |
| `Func<String, String>` | GetFolderMutation(`String` oldPath, `String` newPath)                                     |                                                                                                                                                                                        |
| `void`                 | ModifyDisplayFolder(`Table` table, `String` oldPath, `String` newPath, `Culture` culture) | Updates the DisplayFolder property of all tabular objects within one table. Objects residing  in subfolders to the updated path, will also be updated. |
| `void`                 | OnNodesChanged(`ITabularObject` nodeItem)                                                 |                                                                                                                                                                                        |
| `void`                 | OnNodesInserted(`ITabularObject` parent, `ITabularObject[]` children)                     |                                                                                                                                                                                        |
| `void`                 | OnNodesInserted(`ITabularObject` parent, `IEnumerable<ITabularObject>` children)          |                                                                                                                                                                                        |
| `void`                 | OnNodesRemoved(`ITabularObject` parent, `ITabularObject[]` children)                      |                                                                                                                                                                                        |
| `void`                 | OnNodesRemoved(`ITabularObject` parent, `IEnumerable<ITabularObject>` children)           |                                                                                                                                                                                        |
| `void`                 | OnStructureChanged(`ITabularNamedObject` obj = null)                                      |                                                                                                                                                                                        |
| `void`                 | SetCulture(`String` cultureName)                                                          |                                                                                                                                                                                        |
| `void`                 | SetPerspective(`String` perspectiveName)                                                  |                                                                                                                                                                                        |
| `void`                 | UpdateFolder(`Folder` folder, `String` oldFullPath = null)                                |                                                                                                                                                                                        |
| `Boolean`              | VisibleInTree(`ITabularNamedObject` tabularObject)                                        |                                                                                                                                                                                        |

## `TranslationIndexer`

```csharp
public class TabularEditor.TOMWrapper.TranslationIndexer
    : IEnumerable<String>, IEnumerable, IExpandableIndexer

```

属性

| Type                  | 姓名              | Summary |
| --------------------- | --------------- | ------- |
| `String`              | DefaultValue    |         |
| `String`              | Item            |         |
| `String`              | Item            |         |
| `IEnumerable<String>` | Keys            |         |
| `String`              | Summary         |         |
| `Int32`               | TranslatedCount |         |

Methods

| Type                         | 姓名                                                                                                    | Summary                                                                                                                                                                                                                                                                             |
| ---------------------------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `void`                       | Clear()                                                                            | Clears all translated values for the object.                                                                                                                                                                                                                        |
| `Boolean`                    | Contains(`Culture` culture)                                                        |                                                                                                                                                                                                                                                                                     |
| `Dictionary<String, String>` | Copy()                                                                             |                                                                                                                                                                                                                                                                                     |
| `void`                       | CopyFrom(`TranslationIndexer` translations, `Func<String, String>` mutator = null) |                                                                                                                                                                                                                                                                                     |
| `void`                       | CopyFrom(`IDictionary<String, String>` source)                                     |                                                                                                                                                                                                                                                                                     |
| `String`                     | GetDisplayName(`String` key)                                                       |                                                                                                                                                                                                                                                                                     |
| `IEnumerator<String>`        | GetEnumerator()                                                                    |                                                                                                                                                                                                                                                                                     |
| `void`                       | Refresh()                                                                          |                                                                                                                                                                                                                                                                                     |
| `void`                       | Reset()                                                                            | Resets the translations of the object. Caption translations are removed, making the object appear with  the base name in all locales. Display Folder and Description translations are set to the untranslated  value of the object. |
| `void`                       | SetAll(`String` value)                                                             |                                                                                                                                                                                                                                                                                     |


