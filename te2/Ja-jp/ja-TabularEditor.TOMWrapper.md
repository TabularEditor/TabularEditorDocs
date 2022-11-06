# TabularEditor.TOMWrapper Reference

これは、TOMWrapper APIの自動生成されたドキュメントです。特定のクラスやプロパティ、メソッドを探すには、「CTRL+F」または右側のサイドバーをご利用ください。

## `AddObjectType`

```csharp
public enum TabularEditor.TOMWrapper.AddObjectType
    : Enum, IComparable, IFormattable, IConvertible

```

Enum

| Value | Name | Summary | 
| --- | --- | --- | 
| `1` | Measure |  | 
| `2` | CalculatedColumn |  | 
| `3` | Hierarchy |  | 

## `CalculatedColumn`

CalculatedColumn の基底クラス宣言

```csharp
public class TabularEditor.TOMWrapper.CalculatedColumn
    : Column, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IErrorMessageObject, IDescriptionObject, IAnnotationObject, ITabularPerspectiveObject, IDaxObject, IExpressionObject

```

Properties

| Type | Name | Summary |
| --- | --- | --- |
| `Dictionary<IDaxObject, List<Dependency>>` | Dependencies |  |
| `String` | Expression | CalculatedColumn の Expression を取得または設定します。 |
| `Boolean` | IsDataTypeInferred | CalculatedColumn の IsDataTypeInferred を取得または設定します。 |
| `CalculatedColumn` | MetadataObject |  |
| `Boolean` | NeedsValidation |  |

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `TabularNamedObject` | Clone(`String` newName = null, `Boolean` includeTranslations = True) |  | 
| `TabularNamedObject` | CloneTo(`Table` table, `String` newName = null, `Boolean` includeTranslations = True) |  | 
| `void` | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue) |  | 

## `CalculatedTable`

```csharp
public class TabularEditor.TOMWrapper.CalculatedTable
    : Table, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IHideableObject, IDescriptionObject, IAnnotationObject, ITabularObjectContainer, IDetailObjectContainer, ITabularPerspectiveObject, IDaxObject, IDynamicPropertyObject, IErrorMessageObject, IExpressionObject

```

Properties

| Type | Name | Summary |
| --- | --- | --- |
| `Dictionary<IDaxObject, List<Dependency>>` | Dependencies |  |
| `String` | Expression |  |
| `Boolean` | NeedsValidation |  |
| `String` | ObjectTypeName |  |

Methods

| Type | Name | Summary |
| --- | --- | --- |
| `void` | CheckChildrenErrors() |  |
| `Boolean` | Editable(`String` propertyName) |  |
| `void` | Init() |  |
| `void` | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue) |  |
| `void` | ReinitColumns() | モデルがDBに保存された後にこのメソッドを呼び出し、変更されたカラムをチェックする（式の変更の場合）。 |

## `CalculatedTableColumn`

CalculatedTableColumn の基底クラス宣言

```csharp
public class TabularEditor.TOMWrapper.CalculatedTableColumn
    : Column, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IErrorMessageObject, IDescriptionObject, IAnnotationObject, ITabularPerspectiveObject, IDaxObject
```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `Column` | ColumnOrigin | Gets or sets the ColumnOrigin of the CalculatedTableColumn. | 
| `Boolean` | IsDataTypeInferred | Gets or sets the IsDataTypeInferred of the CalculatedTableColumn. | 
| `Boolean` | IsNameInferred | Gets or sets the IsNameInferred of the CalculatedTableColumn. | 
| `CalculatedTableColumn` | MetadataObject |  | 
| `String` | SourceColumn | Gets or sets the SourceColumn of the CalculatedTableColumn. | 

## `Column`

Column の基底クラス宣言

```csharp
public abstract class TabularEditor.TOMWrapper.Column
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IErrorMessageObject, IDescriptionObject, IAnnotationObject, ITabularPerspectiveObject, IDaxObject
```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `Alignment` | Alignment | ColumnのAlignmentを取得または設定します。 | 
| `String` | DataCategory | ColumnのDataCategoryを取得または設定します。 | 
| `DataType` | DataType | ColumnのDataTypeを取得または設定します。 | 
| `String` | DaxObjectFullName |  | 
| `String` | DaxObjectName |  | 
| `String` | DaxTableName |  | 
| `HashSet<IExpressionObject>` | Dependants |  | 
| `String` | Description | ColumnのDescriptionを取得または設定します。 | 
| `String` | DisplayFolder | ColumnのDisplayFolderを取得または設定します。 | 
| `Int32` | DisplayOrdinal | ColumnのDisplayOrdinalを取得または設定します。 | 
| `String` | ErrorMessage | ColumnのErrorMessageを取得または設定します。 | 
| `String` | FormatString | ColumnのFormatStringを取得または設定します。 | 
| `PerspectiveIndexer` | InPerspective |  | 
| `Boolean` | IsAvailableInMDX | Column の IsAvailableInMDX を取得または設定します。 | 
| `Boolean` | IsDefaultImage | ColumnのIsDefaultImageを取得または設定します。 | 
| `Boolean` | IsDefaultLabel | ColumnのIsDefaultLabelを取得または設定します。 | 
| `Boolean` | IsHidden | ColumnのIsHiddenを取得または設定します。 | 
| `Boolean` | IsKey | ColumnのIsKeyを取得または設定します。 | 
| `Boolean` | IsNullable | ColumnのIsNullableを取得または設定します。 | 
| `Boolean` | IsUnique | ColumnのIsUniqueを取得または設定します。 | 
| `Boolean` | KeepUniqueRows | ColumnのKeepUniqueRowsを取得または設定します。 | 
| `Column` | MetadataObject |  | 
| `Column` | SortByColumn | ColumnのSortByColumnを取得または設定します。 | 
| `String` | SourceProviderType | ColumnのSourceProviderTypeを取得または設定します。 | 
| `ObjectState` | State | ColumnのStateを取得または設定します。 | 
| `AggregateFunction` | SummarizeBy | ColumnのSummarizeByを取得または設定します。 | 
| `Table` | Table |  | 
| `Int32` | TableDetailPosition | ColumnのTableDetailPositionを取得または設定します。 | 
| `TranslationIndexer` | TranslatedDescriptions |このColumnのローカライズされた説明文のコレクション。 | 
| `TranslationIndexer` | TranslatedDisplayFolders | このColumnのローカライズされたDisplay Foldersのコレクション。 | 
| `ColumnType` | Type | ColumnのTypeを取得または設定します。 | 
| `IEnumerable<Hierarchy>` | UsedInHierarchies<a id="used-in-hierarchy"></a> | このカラムがレベルとして使用されるすべての階層を列挙します。 | 
| `IEnumerable<Relationship>` | UsedInRelationships | この列が参加するすべてのリレーションシップを列挙する（as または ) 。 |

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `void` | Delete() |  | 
| `String` | GetAnnotation(`String` name) |  | 
| `void` | Init() |  | 
| `void` | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue) |  | 
| `void` | OnPropertyChanging(`String` propertyName, `Object` newValue, `Boolean&` undoable, `Boolean&` cancel) |  | 
| `void` | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |  | 
| `void` | Undelete(`ITabularObjectCollection` collection) |  | 

## `ColumnCollection`

Column用のコレクションクラスです。一度に複数のオブジェクトにプロパティを設定するための便利なプロパティを提供します。

```csharp
public class TabularEditor.TOMWrapper.ColumnCollection
    : TabularObjectCollection<Column, Column, Table>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Column>, IEnumerable<Column>, IList<Column>, ITabularObjectCollection, IExpandableIndexer

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `Alignment` | Alignment |  | 
| `String` | DataCategory |  | 
| `DataType` | DataType |  | 
| `String` | Description |  | 
| `String` | DisplayFolder |  | 
| `Int32` | DisplayOrdinal |  | 
| `String` | FormatString |  | 
| `Boolean` | IsAvailableInMDX |  | 
| `Boolean` | IsDefaultImage |  | 
| `Boolean` | IsDefaultLabel |  | 
| `Boolean` | IsHidden |  | 
| `Boolean` | IsKey |  | 
| `Boolean` | IsNullable |  | 
| `Boolean` | IsUnique |  | 
| `Boolean` | KeepUniqueRows |  | 
| `Table` | Parent |  | 
| `Column` | SortByColumn |  | 
| `String` | SourceProviderType |  | 
| `AggregateFunction` | SummarizeBy |  | 
| `Int32` | TableDetailPosition |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `IEnumerator<Column>` | GetEnumerator() |  | 
| `String` | ToString() |  | 

## `Culture`

Culture の基本クラス宣言

```csharp
public class TabularEditor.TOMWrapper.Culture
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IAnnotationObject, IDynamicPropertyObject

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | DisplayName |  | 
| `Culture` | MetadataObject |  | 
| `String` | Name |  | 
| `ObjectTranslationCollection` | ObjectTranslations |  | 
| `String` | StatsColumnCaptions |  | 
| `String` | StatsColumnDisplayFolders |  | 
| `String` | StatsHierarchyCaptions |  | 
| `String` | StatsHierarchyDisplayFolders |  | 
| `String` | StatsLevelCaptions |  | 
| `String` | StatsMeasureCaptions |  | 
| `String` | StatsMeasureDisplayFolders |  | 
| `String` | StatsTableCaptions |  | 
| `Boolean` | Unassigned |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `Boolean` | Browsable(`String` propertyName) |  | 
| `TabularNamedObject` | Clone(`String` newName, `Boolean` includeTranslations) |  | 
| `Boolean` | Editable(`String` propertyName) |  | 
| `String` | GetAnnotation(`String` name) |  | 
| `void` | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue) |  | 
| `void` | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |  | 
| `void` | Undelete(`ITabularObjectCollection` collection) |  | 

## `CultureCollection`

Cultureのためのコレクションクラス。一度に複数のオブジェクトにプロパティを設定するための便利なプロパティを提供します。

```csharp
public class TabularEditor.TOMWrapper.CultureCollection
    : TabularObjectCollection<Culture, Culture, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Culture>, IEnumerable<Culture>, IList<Culture>, ITabularObjectCollection, IExpandableIndexer

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `Model` | Parent |  | 


Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | ToString() |  | 

## `CultureConverter`

```csharp
public class TabularEditor.TOMWrapper.CultureConverter
    : TypeConverter

```

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `Boolean` | CanConvertFrom(`ITypeDescriptorContext` context, `Type` sourceType) |  | 
| `Boolean` | CanConvertTo(`ITypeDescriptorContext` context, `Type` destinationType) |  | 
| `Object` | ConvertFrom(`ITypeDescriptorContext` context, `CultureInfo` culture, `Object` value) |  | 
| `Object` | ConvertTo(`ITypeDescriptorContext` context, `CultureInfo` culture, `Object` value, `Type` destinationType) |  | 
| `StandardValuesCollection` | GetStandardValues(`ITypeDescriptorContext` context) |  | 
| `Boolean` | GetStandardValuesExclusive(`ITypeDescriptorContext` context) |  | 
| `Boolean` | GetStandardValuesSupported(`ITypeDescriptorContext` context) |  | 


## `Database`

```csharp
public class TabularEditor.TOMWrapper.Database

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `Nullable<Int32>` | CompatibilityLevel |  | 
| `Nullable<DateTime>` | CreatedTimestamp |  | 
| `String` | ID |  | 
| `Nullable<DateTime>` | LastProcessed |  | 
| `Nullable<DateTime>` | LastSchemaUpdate |  | 
| `Nullable<DateTime>` | LastUpdate |  | 
| `String` | Name |  | 
| `String` | ServerName |  | 
| `String` | ServerVersion |  | 
| `Database` | TOMDatabase |  | 
| `Nullable<Int64>` | Version |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | ToString() |  | 

## `DataColumn`

DataColumn の基底クラス宣言

```csharp
public class TabularEditor.TOMWrapper.DataColumn
    : Column, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IErrorMessageObject, IDescriptionObject, IAnnotationObject, ITabularPerspectiveObject, IDaxObject

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `DataColumn` | MetadataObject |  | 
| `String` | SourceColumn | Gets or sets the SourceColumn of the DataColumn. | 

## `DataSource`

DataSource の基底クラス宣言

```csharp
public abstract class TabularEditor.TOMWrapper.DataSource
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | Description | Gets or sets the Description of the DataSource. | 
| `DataSource` | MetadataObject |  | 
| `TranslationIndexer` | TranslatedDescriptions | Collection of localized descriptions for this DataSource. | 
| `DataSourceType` | Type | Gets or sets the Type of the DataSource. | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | GetAnnotation(`String` name) |  | 
| `void` | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |  | 

## `DataSourceCollection`

DataSourceのコレクションクラスです。複数のオブジェクトに一度にプロパティを設定するための便利なプロパティを提供します。

```csharp
public class TabularEditor.TOMWrapper.DataSourceCollection
    : TabularObjectCollection<DataSource, DataSource, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<DataSource>, IEnumerable<DataSource>, IList<DataSource>, ITabularObjectCollection, IExpandableIndexer

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | Description |  | 
| `Model` | Parent |  | 


Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | ToString() |  | 

## `Dependency`

```csharp
public struct TabularEditor.TOMWrapper.Dependency

```

Fields

| Type | Name | Summary | 
| --- | --- | --- | 
| `Int32` | from |  | 
| `Boolean` | fullyQualified |  | 
| `Int32` | to |  | 

## `DependencyHelper`

```csharp
public static class TabularEditor.TOMWrapper.DependencyHelper

```

Static Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `void` | AddDep(this `IExpressionObject` target, `IDaxObject` dependsOn, `Int32` fromChar, `Int32` toChar, `Boolean` fullyQualified) |  | 
| `String` | NoQ(this `String` objectName, `Boolean` table = False) | Removes qualifiers such as ' ' and [ ] around a name. | 

## `DeploymentMode`

```csharp
public enum TabularEditor.TOMWrapper.DeploymentMode
    : Enum, IComparable, IFormattable, IConvertible

```

Enum

| Value | Name | Summary | 
| --- | --- | --- | 
| `0` | CreateDatabase |  | 
| `1` | CreateOrAlter |  | 

## `DeploymentOptions`

```csharp
public class TabularEditor.TOMWrapper.DeploymentOptions

```

Fields

| Type | Name | Summary | 
| --- | --- | --- | 
| `Boolean` | DeployConnections |  | 
| `DeploymentMode` | DeployMode |  | 
| `Boolean` | DeployPartitions |  | 
| `Boolean` | DeployRoleMembers |  | 
| `Boolean` | DeployRoles |  | 

Static Fields

| Type | Name | Summary | 
| --- | --- | --- | 
| `DeploymentOptions` | Default |  | 
| `DeploymentOptions` | StructureOnly |  | 

## `DeploymentResult`

```csharp
public class TabularEditor.TOMWrapper.DeploymentResult

```

Fields

| Type | Name | Summary | 
| --- | --- | --- | 
| `IReadOnlyList<String>` | Issues |  | 
| `IReadOnlyList<String>` | Warnings |  | 

## `DeploymentStatus`

```csharp
public enum TabularEditor.TOMWrapper.DeploymentStatus
    : Enum, IComparable, IFormattable, IConvertible

```

Enum

| Value | Name | Summary | 
| --- | --- | --- | 
| `0` | ChangesSaved |  | 
| `1` | DeployComplete |  | 
| `2` | DeployCancelled |  | 

## `Folder`

TreeView内のFolderを表します。TOMのどのオブジェクトにも対応しません。  Folderは、それ自体が他の表示フォルダの中に位置することができるので、IDisplayFolderObjectを実装しています。  Folderは、子オブジェクトを含むことができるので、IParentObjectを実装しています。

```csharp
public class TabularEditor.TOMWrapper.Folder
    : IDetailObject, ITabularTableObject, ITabularNamedObject, ITabularObject, INotifyPropertyChanged, ITabularObjectContainer, IDetailObjectContainer, IErrorMessageObject

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `IDetailObjectContainer` | Container |  | 
| `Culture` | Culture |  | 
| `String` | DisplayFolder |  | 
| `String` | ErrorMessage |  | 
| `String` | FullPath |  | 
| `TabularModelHandler` | Handler |  | 
| `Int32` | MetadataIndex |  | 
| `Model` | Model |  | 
| `String` | Name |  | 
| `ObjectType` | ObjectType |  | 
| `Table` | ParentTable |  | 
| `String` | Path |  | 
| `Table` | Table |  | 
| `TranslationIndexer` | TranslatedDisplayFolders |  | 
| `TranslationIndexer` | TranslatedNames |  | 

Events

| Type | Name | Summary | 
| --- | --- | --- | 
| `PropertyChangedEventHandler` | PropertyChanged |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `void` | CheckChildrenErrors() |  | 
| `void` | Delete() | フォルダを削除しても、子オブジェクトは削除されず、単にフォルダが削除されるだけです。  子フォルダはすべて維持されます（ただし、表示フォルダの階層は上に移動します）。 | 
| `IEnumerable<ITabularNamedObject>` | GetChildren() |  | 
| `IEnumerable<IDetailObject>` | GetChildrenByFolders(`Boolean` recursive = False) |  | 
| `void` | SetFolderName(`String` newName) |  | 
| `void` | UndoSetPath(`String` value) |  | 

Static Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `Folder` | CreateFolder(`Table` table, `String` path = , `Boolean` useFixedCulture = False, `Culture` fixedCulture = null) |  | 

## `FolderHelper`

```csharp
public static class TabularEditor.TOMWrapper.FolderHelper

```

Static Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | ConcatPath(this `String` path, `String` additionalPath) |  | 
| `String` | ConcatPath(this `IEnumerable<String>` pathBits) |  | 
| `IDetailObjectContainer` | GetContainer(this `IDetailObject` obj) |  | 
| `String` | GetDisplayFolder(this `IDetailObject` folderObject, `Culture` culture) |  | 
| `String` | GetFullPath(`ITabularNamedObject` obj) |  | 
| `Boolean` | HasAncestor(this `IDetailObject` child, `ITabularNamedObject` ancestor, `Culture` culture) |  | 
| `Boolean` | HasParent(this `IDetailObject` child, `ITabularNamedObject` parent, `Culture` culture) |  | 
| `Int32` | Level(this `String` path) |  | 
| `String` | PathFromFullPath(`String` path) |  | 
| `void` | SetDisplayFolder(this `IDetailObject` folderObject, `String` newFolderName, `Culture` culture) |  | 
| `String` | TrimFolder(this `String` folderPath) |  | 

## `Hierarchy`

Hierarchyの基底クラス宣言

```csharp
public class TabularEditor.TOMWrapper.Hierarchy
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IDescriptionObject, IAnnotationObject, ITabularObjectContainer, ITabularPerspectiveObject

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | Description | Hierarchy の Description を取得または設定します。 | 
| `String` | DisplayFolder | Hierarchy の DisplayFolder を取得または設定します。 | 
| `PerspectiveIndexer` | InPerspective |  | 
| `Boolean` | IsHidden | Hierarchy の IsHidden を取得または設定します。 | 
| `LevelCollection` | Levels |  | 
| `Hierarchy` | MetadataObject |  | 
| `Boolean` | Reordering | 複数のレベルが1つのアクションとして再注文される場合、trueに設定されます。 | 
| `ObjectState` | State | HierarchyのStateを取得または設定します。 | 
| `Table` | Table |  | 
| `TranslationIndexer` | TranslatedDescriptions | この Hierarchy のローカライズされた説明文のコレクション。 | 
| `TranslationIndexer` | TranslatedDisplayFolders | この階層にローカライズされた表示フォルダのコレクション。 | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `Level` | AddLevel(`Column` column, `String` levelName = null, `Int32` ordinal = -1) |  | 
| `Level` | AddLevel(`String` columnName, `String` levelName = null, `Int32` ordinal = -1) |  | 
| `void` | AddLevels(`IEnumerable<Column>` columns, `Int32` ordinal = -1) |  | 
| `void` | CompactLevelOrdinals() |  | 
| `void` | Delete() |  | 
| `void` | FixLevelOrder(`Level` level, `Int32` newOrdinal) |  | 
| `String` | GetAnnotation(`String` name) |  | 
| `IEnumerable<ITabularNamedObject>` | GetChildren() |  | 
| `void` | Init() |  | 
| `void` | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |  | 
| `void` | SetLevelOrder(`IList<Level>` order) |  | 
| `void` | Undelete(`ITabularObjectCollection` collection) |  | 

## `HierarchyCollection`

Hierarchyのコレクションクラス。複数のオブジェクトに一度にプロパティを設定するための便利なプロパティを提供します。

```csharp
public class TabularEditor.TOMWrapper.HierarchyCollection
    : TabularObjectCollection<Hierarchy, Hierarchy, Table>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Hierarchy>, IEnumerable<Hierarchy>, IList<Hierarchy>, ITabularObjectCollection, IExpandableIndexer

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | Description |  | 
| `String` | DisplayFolder |  | 
| `Boolean` | IsHidden |  | 
| `Table` | Parent |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | ToString() |  | 

## `HierarchyColumnConverter`

```csharp
public class TabularEditor.TOMWrapper.HierarchyColumnConverter
    : TableColumnConverter

```

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `Boolean` | GetStandardValuesExclusive(`ITypeDescriptorContext` context) |  | 
| `Boolean` | IsValid(`ITypeDescriptorContext` context, `Object` value) |  | 

## `IAnnotationObject`

```csharp
public interface TabularEditor.TOMWrapper.IAnnotationObject
    : ITabularObject, INotifyPropertyChanged

```

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | GetAnnotation(`String` name) |  | 
| `void` | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |  | 

## `IClonableObject`

```csharp
public interface TabularEditor.TOMWrapper.IClonableObject

```

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `TabularNamedObject` | Clone(`String` newName, `Boolean` includeTranslations) |  | 

## `IDaxObject`

```csharp
public interface TabularEditor.TOMWrapper.IDaxObject
    : ITabularNamedObject, ITabularObject, INotifyPropertyChanged

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | DaxObjectFullName |  | 
| `String` | DaxObjectName |  | 
| `String` | DaxTableName |  | 
| `HashSet<IExpressionObject>` | Dependants |  | 

## `IDescriptionObject`

Objects that can have descriptions
```csharp
public interface TabularEditor.TOMWrapper.IDescriptionObject

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | Description |  | 
| `TranslationIndexer` | TranslatedDescriptions |  | 

## `IDetailObject`

ディスプレイフォルダに格納可能なオブジェクトを表す。
例

- Measures
- Columns
- Hierarchies
- Folders

```csharp
public interface TabularEditor.TOMWrapper.IDetailObject
    : ITabularTableObject, ITabularNamedObject, ITabularObject, INotifyPropertyChanged

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | DisplayFolder |  | 
| `TranslationIndexer` | TranslatedDisplayFolders |  | 

## `IDetailObjectContainer`

表示フォルダーと同様に他のオブジェクトを含むことができるオブジェクトを表す。

例：

- フォルダ
- テーブル

```csharp
public interface TabularEditor.TOMWrapper.IDetailObjectContainer
    : ITabularNamedObject, ITabularObject, INotifyPropertyChanged

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `Table` | ParentTable |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `IEnumerable<IDetailObject>` | GetChildrenByFolders(`Boolean` recursive = False) |  | 

## `IErrorMessageObject`

エラーメッセージを表示することができるオブジェクト

```csharp
public interface TabularEditor.TOMWrapper.IErrorMessageObject

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | ErrorMessage |  | 

## `IExpressionObject`

```csharp
public interface TabularEditor.TOMWrapper.IExpressionObject
    : IDaxObject, ITabularNamedObject, ITabularObject, INotifyPropertyChanged

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `Dictionary<IDaxObject, List<Dependency>>` | Dependencies |  | 
| `String` | Expression |  | 
| `Boolean` | NeedsValidation |  | 

## `IHideableObject`

表示／非表示が可能なオブジェクト

```csharp
public interface TabularEditor.TOMWrapper.IHideableObject

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `Boolean` | IsHidden |  | 


## `IntelliSenseAttribute`

```csharp
public class TabularEditor.TOMWrapper.IntelliSenseAttribute
    : Attribute, _Attribute

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | Description |  | 


## `ITabularNamedObject`

```csharp
public interface TabularEditor.TOMWrapper.ITabularNamedObject
    : ITabularObject, INotifyPropertyChanged

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `Int32` | MetadataIndex |  | 
| `String` | Name |  | 
| `TranslationIndexer` | TranslatedNames |  | 

## `ITabularObject`

```csharp
public interface TabularEditor.TOMWrapper.ITabularObject
    : INotifyPropertyChanged

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `Model` | Model |  | 
| `ObjectType` | ObjectType |  | 

## `ITabularObjectCollection`

```csharp
public interface TabularEditor.TOMWrapper.ITabularObjectCollection
    : IEnumerable

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | CollectionName |  | 
| `TabularModelHandler` | Handler |  | 
| `IEnumerable<String>` | Keys |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `void` | Add(`TabularNamedObject` obj) |  | 
| `void` | Clear() |  | 
| `Boolean` | Contains(`Object` value) |  | 
| `Boolean` | Contains(`String` key) |  | 
| `ITabularObjectCollection` | GetCurrentCollection() |  | 
| `Int32` | IndexOf(`TabularNamedObject` obj) |  | 
| `void` | Remove(`TabularNamedObject` obj) |  | 

## `ITabularObjectContainer`

他のオブジェクトを含むことができるTabularObjectは、このインタフェースを使用する必要がある。

```csharp
public interface TabularEditor.TOMWrapper.ITabularObjectContainer

```

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `IEnumerable<ITabularNamedObject>` | GetChildren() |  | 

## `ITabularPerspectiveObject`

個々のパースペクティブで表示/非表示が可能なオブジェクト

```csharp
public interface TabularEditor.TOMWrapper.ITabularPerspectiveObject
    : IHideableObject

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `PerspectiveIndexer` | InPerspective |  | 

## `ITabularTableObject`

特定のテーブルに属するオブジェクト。

```csharp
public interface TabularEditor.TOMWrapper.ITabularTableObject
    : ITabularNamedObject, ITabularObject, INotifyPropertyChanged

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `Table` | Table |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `void` | Delete() |  | 

## `KPI`

KPI の基底クラス宣言

```csharp
public class TabularEditor.TOMWrapper.KPI
    : TabularObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, IDescriptionObject, IAnnotationObject, IDynamicPropertyObject

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | Description | Gets or sets the Description of the KPI. | 
| `Measure` | Measure | Gets or sets the Measure of the KPI. | 
| `KPI` | MetadataObject |  | 
| `String` | StatusDescription | Gets or sets the StatusDescription of the KPI. | 
| `String` | StatusExpression | Gets or sets the StatusExpression of the KPI. | 
| `String` | StatusGraphic | Gets or sets the StatusGraphic of the KPI. | 
| `String` | TargetDescription | Gets or sets the TargetDescription of the KPI. | 
| `String` | TargetExpression | Gets or sets the TargetExpression of the KPI. | 
| `String` | TargetFormatString | Gets or sets the TargetFormatString of the KPI. | 
| `TranslationIndexer` | TranslatedDescriptions | Collection of localized descriptions for this KPI. | 
| `String` | TrendDescription | Gets or sets the TrendDescription of the KPI. | 
| `String` | TrendExpression | Gets or sets the TrendExpression of the KPI. | 
| `String` | TrendGraphic | Gets or sets the TrendGraphic of the KPI. | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `Boolean` | Browsable(`String` propertyName) |  | 
| `Boolean` | Editable(`String` propertyName) |  | 
| `String` | GetAnnotation(`String` name) |  | 
| `void` | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |  | 

## `Level`

Levelの基底クラス宣言

```csharp
public class TabularEditor.TOMWrapper.Level
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject, ITabularTableObject

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `Column` | Column | Gets or sets the Column of the Level. | 
| `String` | Description | Gets or sets the Description of the Level. | 
| `Hierarchy` | Hierarchy | Gets or sets the Hierarchy of the Level. | 
| `Level` | MetadataObject |  | 
| `Int32` | Ordinal | Gets or sets the Ordinal of the Level. | 
| `Table` | Table |  | 
| `TranslationIndexer` | TranslatedDescriptions | Collection of localized descriptions for this Level. | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `void` | Delete() | Deletes the level from the hierarchy. | 
| `String` | GetAnnotation(`String` name) |  | 
| `void` | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue) |  | 
| `void` | OnPropertyChanging(`String` propertyName, `Object` newValue, `Boolean&` undoable, `Boolean&` cancel) |  | 
| `void` | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |  | 
| `void` | Undelete(`ITabularObjectCollection` collection) |  | 

## `LevelCollection`

Levelのコレクションクラスです。複数のオブジェクトに一度にプロパティを設定するための便利なプロパティを提供します。

```csharp
public class TabularEditor.TOMWrapper.LevelCollection
    : TabularObjectCollection<Level, Level, Hierarchy>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Level>, IEnumerable<Level>, IList<Level>, ITabularObjectCollection, IExpandableIndexer

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | Description |  | 
| `Hierarchy` | Parent |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `void` | Add(`Level` item) |  | 
| `Boolean` | Remove(`Level` item) |  | 
| `String` | ToString() |  | 

## `LogicalGroup`

```csharp
public class TabularEditor.TOMWrapper.LogicalGroup
    : ITabularNamedObject, ITabularObject, INotifyPropertyChanged, ITabularObjectContainer

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `Int32` | MetadataIndex |  | 
| `Model` | Model |  | 
| `String` | Name |  | 
| `ObjectType` | ObjectType |  | 
| `TranslationIndexer` | TranslatedNames |  | 

Events

| Type | Name | Summary | 
| --- | --- | --- | 
| `PropertyChangedEventHandler` | PropertyChanged |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `IEnumerable<ITabularNamedObject>` | GetChildren() |  | 

## `LogicalTreeOptions`

```csharp
public enum TabularEditor.TOMWrapper.LogicalTreeOptions
    : Enum, IComparable, IFormattable, IConvertible

```

Enum

| Value | Name | Summary | 
| --- | --- | --- | 
| `1` | DisplayFolders |  | 
| `2` | Columns |  | 
| `4` | Measures |  | 
| `8` | KPIs |  | 
| `16` | Hierarchies |  | 
| `32` | Levels |  | 
| `64` | ShowHidden |  | 
| `128` | AllObjectTypes |  | 
| `256` | ShowRoot |  | 
| `447` | Default |  | 

## `Measure`

Measure の基底クラス宣言

```csharp
public class TabularEditor.TOMWrapper.Measure
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IErrorMessageObject, IDescriptionObject, IExpressionObject, IDaxObject, IAnnotationObject, ITabularPerspectiveObject, IDynamicPropertyObject, IClonableObject

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `DataType` | DataType | メジャーの DataType を取得または設定します。 | 
| `String` | DaxObjectFullName |  | 
| `String` | DaxObjectName |  | 
| `String` | DaxTableName |  | 
| `HashSet<IExpressionObject>` | Dependants |  | 
| `Dictionary<IDaxObject, List<Dependency>>` | Dependencies |  | 
| `String` | Description | メジャーの説明を取得または設定します。 | 
| `String` | DisplayFolder | メジャーの DisplayFolder を取得または設定します。 | 
| `String` | ErrorMessage | メジャーの ErrorMessage を取得または設定します。 | 
| `String` | Expression |メジャーのExpressionを取得または設定します。 | 
| `String` | FormatString | メジャーの FormatString を取得または設定します。 | 
| `PerspectiveIndexer` | InPerspective |  | 
| `Boolean` | IsHidden | メジャーの IsHidden を取得または設定します。 | 
| `Boolean` | IsSimpleMeasure |メジャーの IsSimpleMeasure を取得または設定します。 | 
| `KPI` | KPI | メジャーの KPI を取得または設定します。 | 
| `Measure` | MetadataObject |  | 
| `Boolean` | NeedsValidation |  | 
| `ObjectState` | State | メジャーの状態を取得または設定します。 | 
| `Table` | Table |  | 
| `TranslationIndexer` | TranslatedDescriptions | このメジャーに関するローカライズされた説明文のコレクション。 | 
| `TranslationIndexer` | TranslatedDisplayFolders | この小節のローカライズされた表示フォルダのコレクション。 | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `Boolean` | Browsable(`String` propertyName) |  | 
| `TabularNamedObject` | Clone(`String` newName = null, `Boolean` includeTranslations = True) |  | 
| `TabularNamedObject` | CloneTo(`Table` table, `String` newName = null, `Boolean` includeTranslations = True) |  | 
| `void` | Delete() |  | 
| `Boolean` | Editable(`String` propertyName) |  | 
| `String` | GetAnnotation(`String` name) |  | 
| `void` | Init() |  | 
| `void` | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue) |  | 
| `void` | OnPropertyChanging(`String` propertyName, `Object` newValue, `Boolean&` undoable, `Boolean&` cancel) |  | 
| `void` | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |  | 
| `void` | Undelete(`ITabularObjectCollection` collection) |  | 


## `MeasureCollection`

Measure用のコレクションクラスです。一度に複数のオブジェクトにプロパティを設定するための便利なプロパティを提供します。

```csharp
public class TabularEditor.TOMWrapper.MeasureCollection
    : TabularObjectCollection<Measure, Measure, Table>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Measure>, IEnumerable<Measure>, IList<Measure>, ITabularObjectCollection, IExpandableIndexer

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | Description |  | 
| `String` | DisplayFolder |  | 
| `String` | Expression |  | 
| `String` | FormatString |  | 
| `Boolean` | IsHidden |  | 
| `Boolean` | IsSimpleMeasure |  | 
| `KPI` | KPI |  | 
| `Table` | Parent |  | 


Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | ToString() |  | 


## `Model`

Model の基底クラス宣言

```csharp
public class TabularEditor.TOMWrapper.Model
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject, ITabularObjectContainer
```

Fields

| Type | Name | Summary | 
| --- | --- | --- | 
| `LogicalGroup` | GroupDataSources |  | 
| `LogicalGroup` | GroupPerspectives |  | 
| `LogicalGroup` | GroupRelationships |  | 
| `LogicalGroup` | GroupRoles |  | 
| `LogicalGroup` | GroupTables |  | 
| `LogicalGroup` | GroupTranslations |  | 


Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `IEnumerable<Column>` | AllColumns |  | 
| `IEnumerable<Hierarchy>` | AllHierarchies |  | 
| `IEnumerable<Level>` | AllLevels |  | 
| `IEnumerable<Measure>` | AllMeasures |  | 
| `String` | Collation | モデルの照合順序を取得または設定します。 | 
| `String` | Culture | モデルのCultureを取得または設定します。 | 
| `CultureCollection` | Cultures |  | 
| `Database` | Database |  | 
| `DataSourceCollection` | DataSources |  | 
| `DataViewType` | DefaultDataView | モデルのDefaultDataViewを取得または設定します。 | 
| `ModeType` | DefaultMode | モデルのDefaultModeを取得または設定します。| 
| `String` | Description | モデルのDescriptionを取得または設定します。 | 
| `Boolean` | HasLocalChanges |モデルのHasLocalChangesを取得または設定します。 | 
| `IEnumerable<LogicalGroup>` | LogicalChildGroups |  | 
| `Model` | MetadataObject |  | 
| `PerspectiveCollection` | Perspectives |  | 
| `RelationshipCollection2` | Relationships |  | 
| `ModelRoleCollection` | Roles |  | 
| `String` | StorageLocation | モデルのStorageLocationを取得または設定します。 | 
| `TableCollection` | Tables |  | 
| `TranslationIndexer` | TranslatedDescriptions | この機種に関するローカライズされた説明文のコレクション。 | 


Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `CalculatedTable` | AddCalculatedTable() |  | 
| `Perspective` | AddPerspective(`String` name = null) |  | 
| `SingleColumnRelationship` | AddRelationship() |  | 
| `ModelRole` | AddRole(`String` name = null) |  | 
| `Table` | AddTable() |  | 
| `Culture` | AddTranslation(`String` cultureId) |  | 
| `String` | GetAnnotation(`String` name) |  | 
| `IEnumerable<ITabularNamedObject>` | GetChildren() |  | 
| `void` | Init() |  | 
| `void` | LoadChildObjects() |  | 
| `void` | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |  | 


## `ModelRole`

ModelRole の基底クラス宣言

```csharp
public class TabularEditor.TOMWrapper.ModelRole
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | Description | ModelRoleのDescriptionを取得または設定します。 | 
| `ModelRole` | MetadataObject |  | 
| `ModelPermission` | ModelPermission | ModelRoleのModelPermissionを取得または設定します。 | 
| `RoleRLSIndexer` | RowLevelSecurity |  | 
| `TranslationIndexer` | TranslatedDescriptions | この ModelRole のローカライズされた説明文のコレクション。 | 


Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `TabularNamedObject` | Clone(`String` newName, `Boolean` includeTranslations) |  | 
| `void` | Delete() |  | 
| `String` | GetAnnotation(`String` name) |  | 
| `void` | InitRLSIndexer() |  | 
| `void` | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |  | 
| `void` | Undelete(`ITabularObjectCollection` collection) |  | 


## `ModelRoleCollection`

ModelRoleのコレクションクラスです。複数のオブジェクトに一度にプロパティを設定するための便利なプロパティを提供します。

```csharp
public class TabularEditor.TOMWrapper.ModelRoleCollection
    : TabularObjectCollection<ModelRole, ModelRole, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<ModelRole>, IEnumerable<ModelRole>, IList<ModelRole>, ITabularObjectCollection, IExpandableIndexer

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | Description |  | 
| `ModelPermission` | ModelPermission |  | 
| `Model` | Parent |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | ToString() |  | 

## `NullTree`

```csharp
public class TabularEditor.TOMWrapper.NullTree
    : TabularTree, INotifyPropertyChanged

```

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `void` | OnNodesChanged(`ITabularObject` nodeItem) |  | 
| `void` | OnNodesInserted(`ITabularObject` parent, `ITabularObject[]` children) |  | 
| `void` | OnNodesRemoved(`ITabularObject` parent, `ITabularObject[]` children) |  | 
| `void` | OnStructureChanged(`ITabularNamedObject` obj = null) |  | 

## `ObjectOrder`

```csharp
public enum TabularEditor.TOMWrapper.ObjectOrder
    : Enum, IComparable, IFormattable, IConvertible

```

Enum

| Value | Name | Summary | 
| --- | --- | --- | 
| `0` | Alphabetical |  | 
| `1` | Metadata |  | 

## `ObjectType`

```csharp
public enum TabularEditor.TOMWrapper.ObjectType
    : Enum, IComparable, IFormattable, IConvertible

```

Enum

| Value | Name | Summary | 
| --- | --- | --- | 
| `-2` | Group |  | 
| `-1` | Folder |  | 
| `1` | Model |  | 
| `2` | DataSource |  | 
| `3` | Table |  | 
| `4` | Column |  | 
| `5` | AttributeHierarchy |  | 
| `6` | Partition |  | 
| `7` | Relationship |  | 
| `8` | Measure |  | 
| `9` | Hierarchy |  | 
| `10` | Level |  | 
| `11` | Annotation |  | 
| `12` | KPI |  | 
| `13` | Culture |  | 
| `14` | ObjectTranslation |  | 
| `15` | LinguisticMetadata |  | 
| `29` | Perspective |  | 
| `30` | PerspectiveTable |  | 
| `31` | PerspectiveColumn |  | 
| `32` | PerspectiveHierarchy |  | 
| `33` | PerspectiveMeasure |  | 
| `34` | Role |  | 
| `35` | RoleMembership |  | 
| `36` | TablePermission |  | 
| `1000` | Database |  | 

## `Partition`

Partitionの基底クラス宣言

```csharp
public class TabularEditor.TOMWrapper.Partition
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDynamicPropertyObject, IErrorMessageObject, ITabularTableObject, IDescriptionObject, IAnnotationObject

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `DataSource` | DataSource |  | 
| `DataViewType` | DataView | PartitionのDataViewを取得または設定します。 | 
| `String` | Description | パーティションの説明を取得または設定します。 | 
| `String` | ErrorMessage | PartitionのErrorMessageを取得または設定します。 | 
| `String` | Expression |  | 
| `Partition` | MetadataObject |  | 
| `ModeType` | Mode | Partition の Mode を取得または設定する。 | 
| `String` | Name |  | 
| `String` | Query |  | 
| `DateTime` | RefreshedTime |  | 
| `String` | Source |  | 
| `PartitionSourceType` | SourceType | PartitionのSourceTypeを取得または設定します。 | 
| `ObjectState` | State |PartitionのStateを取得または設定します。 | 
| `Table` | Table |  | 
| `TranslationIndexer` | TranslatedDescriptions | このパーティションに関するローカライズされた説明文のコレクション。 | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `Boolean` | Browsable(`String` propertyName) |  | 
| `Boolean` | Editable(`String` propertyName) |  | 
| `String` | GetAnnotation(`String` name) |  | 
| `void` | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |  | 
| `void` | Undelete(`ITabularObjectCollection` collection) |  | 

## `PartitionCollection`

Partitionのコレクションクラス。複数のオブジェクトに一度にプロパティを設定するための便利なプロパティを提供します。

```csharp
public class TabularEditor.TOMWrapper.PartitionCollection
    : TabularObjectCollection<Partition, Partition, Table>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Partition>, IEnumerable<Partition>, IList<Partition>, ITabularObjectCollection, IExpandableIndexer

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `DataViewType` | DataView |  | 
| `String` | Description |  | 
| `ModeType` | Mode |  | 
| `Table` | Parent |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | ToString() |  | 

## `Perspective`

Perspectiveの基底クラス宣言

```csharp
public class TabularEditor.TOMWrapper.Perspective
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | Description | パースペクティブの説明を取得または設定します。 | 
| `Perspective` | MetadataObject |  | 
| `TranslationIndexer` | TranslatedDescriptions | このパースペクティブのローカライズされた説明文のコレクション。 | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `TabularNamedObject` | Clone(`String` newName, `Boolean` includeTranslations) |  | 
| `void` | Delete() |  | 
| `String` | GetAnnotation(`String` name) |  | 
| `void` | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |  | 
| `void` | Undelete(`ITabularObjectCollection` collection) |  | 

## `PerspectiveCollection`

Perspectiveのためのコレクションクラスです。複数のオブジェクトに一度にプロパティを設定するための便利なプロパティを提供します。

```csharp
public class TabularEditor.TOMWrapper.PerspectiveCollection
    : TabularObjectCollection<Perspective, Perspective, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Perspective>, IEnumerable<Perspective>, IList<Perspective>, ITabularObjectCollection, IExpandableIndexer

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | Description |  | 
| `Model` | Parent |  | 


Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | ToString() |  | 

## `PerspectiveColumnIndexer`

```csharp
public class TabularEditor.TOMWrapper.PerspectiveColumnIndexer
    : PerspectiveIndexer, IEnumerable<Boolean>, IEnumerable, IExpandableIndexer

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `Column` | Column |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `void` | Refresh() |  | 
| `void` | SetInPerspective(`Perspective` perspective, `Boolean` included) |  | 

## `PerspectiveHierarchyIndexer`

```csharp
public class TabularEditor.TOMWrapper.PerspectiveHierarchyIndexer
    : PerspectiveIndexer, IEnumerable<Boolean>, IEnumerable, IExpandableIndexer

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `Hierarchy` | Hierarchy |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `void` | Refresh() |  | 
| `void` | SetInPerspective(`Perspective` perspective, `Boolean` included) |  | 

## `PerspectiveIndexer`

```csharp
public abstract class TabularEditor.TOMWrapper.PerspectiveIndexer
    : IEnumerable<Boolean>, IEnumerable, IExpandableIndexer

```

Fields

| Type | Name | Summary | 
| --- | --- | --- | 
| `TabularNamedObject` | TabularObject |  | 

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `Boolean` | Item |  | 
| `Boolean` | Item |  | 
| `IEnumerable<String>` | Keys |  | 
| `Dictionary<Perspective, Boolean>` | PerspectiveMap |  | 
| `String` | Summary |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `void` | All() | すべてのパースペクティブにオブジェクトを含む。 | 
| `Dictionary<String, Boolean>` | Copy() |  | 
| `void` | CopyFrom(`PerspectiveIndexer` source) |  | 
| `void` | CopyFrom(`IDictionary<String, Boolean>` source) |  | 
| `String` | GetDisplayName(`String` key) |  | 
| `IEnumerator<Boolean>` | GetEnumerator() |  | 
| `void` | None() |  | 
| `void` | Refresh() |  | 
| `void` | SetInPerspective(`Perspective` perspective, `Boolean` included) |  | 

## `PerspectiveMeasureIndexer`

```csharp
public class TabularEditor.TOMWrapper.PerspectiveMeasureIndexer
    : PerspectiveIndexer, IEnumerable<Boolean>, IEnumerable, IExpandableIndexer

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `Measure` | Measure |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `void` | Refresh() |  | 
| `void` | SetInPerspective(`Perspective` perspective, `Boolean` included) |  | 

## `PerspectiveTableIndexer`

```csharp
public class TabularEditor.TOMWrapper.PerspectiveTableIndexer
    : PerspectiveIndexer, IEnumerable<Boolean>, IEnumerable, IExpandableIndexer

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `Boolean` | Item |  | 
| `Table` | Table |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `PerspectiveTable` | EnsurePTExists(`Perspective` perspective) |  | 
| `void` | Refresh() |  | 
| `void` | SetInPerspective(`Perspective` perspective, `Boolean` included) |  | 

## `ProviderDataSource`

ProviderDataSource の基底クラス宣言

```csharp
public class TabularEditor.TOMWrapper.ProviderDataSource
    : DataSource, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject, IDynamicPropertyObject

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | Account | ProviderDataSourceのAccountを取得または設定します。 | 
| `String` | ConnectionString | ProviderDataSourceのConnectionStringを取得または設定します。 | 
| `ImpersonationMode` | ImpersonationMode | ProviderDataSourceのImpersonationModeを取得または設定します。 | 
| `DatasourceIsolation` | Isolation | ProviderDataSourceのIsolationを取得または設定します。 | 
| `Boolean` | IsPowerBIMashup |  | 
| `String` | Location |  | 
| `Int32` | MaxConnections | ProviderDataSourceのMaxConnectionsを取得または設定します。 | 
| `ProviderDataSource` | MetadataObject |  | 
| `String` | MQuery |  | 
| `String` | Name |  | 
| `String` | Password | ProviderDataSourceのPasswordを取得または設定します。 | 
| `String` | Provider | ProviderDataSource のプロバイダを取得または設定します。 | 
| `String` | SourceID |  | 
| `Int32` | Timeout | ProviderDataSourceのタイムアウトを取得または設定します。 | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `Boolean` | Browsable(`String` propertyName) |  | 
| `Boolean` | Editable(`String` propertyName) |  | 
| `void` | Init() |  | 

## `Relationship`

リレーションシップの基底クラス宣言

```csharp
public abstract class TabularEditor.TOMWrapper.Relationship
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IAnnotationObject

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `CrossFilteringBehavior` | CrossFilteringBehavior | リレーションシップの CrossFilteringBehavior を取得または設定します。 | 
| `Table` | FromTable | リレーションシップの FromTable を取得または設定します。 | 
| `Boolean` | IsActive | リレーションシップのIsActiveを取得または設定します。 | 
| `DateTimeRelationshipBehavior` | JoinOnDateBehavior | リレーションシップの JoinOnDateBehavior を取得または設定します。| 
| `Relationship` | MetadataObject |  | 
| `Boolean` | RelyOnReferentialIntegrity | リレーションシップの RelyOnReferentialIntegrity を取得または設定します。 | 
| `SecurityFilteringBehavior` | SecurityFilteringBehavior | リレーションシップの SecurityFilteringBehavior を取得または設定します。 | 
| `ObjectState` | State | リレーションシップの状態を取得または設定します。 | 
| `Table` | ToTable | リレーションシップのToTableを取得または設定します。 | 
| `RelationshipType` | Type | リレーションシップのTypeを取得または設定します。 | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | GetAnnotation(`String` name) |  | 
| `void` | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |  | 


## `RelationshipCollection`

リレーションシップのためのコレクションクラス。複数のオブジェクトに一度にプロパティを設定するための便利なプロパティを提供します。

```csharp
public class TabularEditor.TOMWrapper.RelationshipCollection
    : TabularObjectCollection<Relationship, Relationship, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Relationship>, IEnumerable<Relationship>, IList<Relationship>, ITabularObjectCollection, IExpandableIndexer

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `CrossFilteringBehavior` | CrossFilteringBehavior |  | 
| `Boolean` | IsActive |  | 
| `DateTimeRelationshipBehavior` | JoinOnDateBehavior |  | 
| `Model` | Parent |  | 
| `Boolean` | RelyOnReferentialIntegrity |  | 
| `SecurityFilteringBehavior` | SecurityFilteringBehavior |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | ToString() |  | 

## `RelationshipCollection2`

```csharp
public class TabularEditor.TOMWrapper.RelationshipCollection2
    : TabularObjectCollection<SingleColumnRelationship, Relationship, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<SingleColumnRelationship>, IEnumerable<SingleColumnRelationship>, IList<SingleColumnRelationship>, ITabularObjectCollection, IExpandableIndexer

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `CrossFilteringBehavior` | CrossFilteringBehavior |  | 
| `Boolean` | IsActive |  | 
| `DateTimeRelationshipBehavior` | JoinOnDateBehavior |  | 
| `Model` | Parent |  | 
| `Boolean` | RelyOnReferentialIntegrity |  | 
| `SecurityFilteringBehavior` | SecurityFilteringBehavior |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | ToString() |  | 

## `RoleRLSIndexer`

RoleRLSIndexerは、ある特定のロールに対して、モデル内の全てのテーブルを横断する全てのフィルタを参照するために使用されます。これはTableRLSIndexerとは対照的で、1つの特定のテーブルに対して、モデル内の全てのロールを横断してフィルタを参照するものです。

```csharp
public class TabularEditor.TOMWrapper.RoleRLSIndexer
    : IEnumerable<String>, IEnumerable, IExpandableIndexer

```

Fields

| Type | Name | Summary | 
| --- | --- | --- | 
| `ModelRole` | Role |  | 

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | Item |  | 
| `String` | Item |  | 
| `IEnumerable<String>` | Keys |  | 
| `Dictionary<Table, String>` | RLSMap |  | 
| `String` | Summary |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `void` | Clear() |  | 
| `void` | CopyFrom(`RoleRLSIndexer` source) |  | 
| `String` | GetDisplayName(`String` key) |  | 
| `IEnumerator<String>` | GetEnumerator() |  | 
| `void` | Refresh() |  | 
| `void` | SetRLS(`Table` table, `String` filterExpression) |  | 

## `SerializeOptions`

```csharp
public class TabularEditor.TOMWrapper.SerializeOptions

```

Fields

| Type | Name | Summary | 
| --- | --- | --- | 
| `Boolean` | IgnoreInferredObjects |  | 
| `Boolean` | IgnoreInferredProperties |  | 
| `Boolean` | IgnoreTimestamps |  | 
| `HashSet<String>` | Levels |  | 
| `Boolean` | PrefixFilenames |  | 
| `Boolean` | SplitMultilineStrings |  | 

Static Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `SerializeOptions` | Default |  | 


## `SingleColumnRelationship`

SingleColumnRelationship の基底クラス宣言。

```csharp
public class TabularEditor.TOMWrapper.SingleColumnRelationship
    : Relationship, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IAnnotationObject, IDynamicPropertyObject

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `RelationshipEndCardinality` | FromCardinality | SingleColumnRelationship の FromCardinality を取得または設定する。 | 
| `Column` | FromColumn | SingleColumnRelationship の FromColumn を取得または設定する。 | 
| `SingleColumnRelationship` | MetadataObject |  | 
| `String` | Name |  | 
| `RelationshipEndCardinality` | ToCardinality |SingleColumnRelationship の ToCardinality を取得または設定する。 | 
| `Column` | ToColumn | SingleColumnRelationship の ToColumn を取得または設定する。 | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `Boolean` | Browsable(`String` propertyName) |  | 
| `void` | Delete() |  | 
| `Boolean` | Editable(`String` propertyName) |  | 
| `void` | Init() |  | 
| `void` | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue) |  | 
| `void` | OnPropertyChanging(`String` propertyName, `Object` newValue, `Boolean&` undoable, `Boolean&` cancel) |  | 
| `String` | ToString() |  | 
| `void` | Undelete(`ITabularObjectCollection` collection) |  | 

## `Table`

Table の基底クラス宣言

```csharp
public class TabularEditor.TOMWrapper.Table
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IHideableObject, IDescriptionObject, IAnnotationObject, ITabularObjectContainer, IDetailObjectContainer, ITabularPerspectiveObject, IDaxObject, IDynamicPropertyObject, IErrorMessageObject

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `IEnumerable<Level>` | AllLevels |  | 
| `ColumnCollection` | Columns |  | 
| `String` | DataCategory | テーブルの DataCategory を取得または設定します。 | 
| `String` | DaxObjectFullName |  | 
| `String` | DaxObjectName |  | 
| `String` | DaxTableName |  | 
| `HashSet<IExpressionObject>` | Dependants |  | 
| `String` | Description | テーブルの説明を取得または設定します。 | 
| `String` | ErrorMessage |  | 
| `HierarchyCollection` | Hierarchies |  | 
| `PerspectiveIndexer` | InPerspective |  | 
| `Boolean` | IsHidden | テーブルのIsHiddenを取得または設定します。 | 
| `MeasureCollection` | Measures |  | 
| `Table` | MetadataObject |  | 
| `String` | Name |  | 
| `Table` | ParentTable |  | 
| `PartitionCollection` | Partitions |  | 
| `TableRLSIndexer` | RowLevelSecurity |  | 
| `String` | Source |  | 
| `PartitionSourceType` | SourceType |  | 
| `TranslationIndexer` | TranslatedDescriptions | この表のローカライズされた説明文のコレクション。 | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `CalculatedColumn` | AddCalculatedColumn(`String` name = null, `String` expression = null, `String` displayFolder = null) |  | 
| `DataColumn` | AddDataColumn(`String` name = null, `String` sourceColumn = null, `String` displayFolder = null) |  | 
| `Hierarchy` | AddHierarchy(`String` name = null, `String` displayFolder = null, `Column[]` levels) |  | 
| `Hierarchy` | AddHierarchy(`String` name, `String` displayFolder = null, `String[]` levels) |  | 
| `Measure` | AddMeasure(`String` name = null, `String` expression = null, `String` displayFolder = null) |  | 
| `Boolean` | Browsable(`String` propertyName) |  | 
| `void` | CheckChildrenErrors() |  | 
| `void` | Children_CollectionChanged(`Object` sender, `NotifyCollectionChangedEventArgs` e) |  | 
| `TabularNamedObject` | Clone(`String` newName = null, `Boolean` includeTranslations = False) |  | 
| `void` | Delete() |  | 
| `Boolean` | Editable(`String` propertyName) |  | 
| `String` | GetAnnotation(`String` name) |  | 
| `IEnumerable<ITabularNamedObject>` | GetChildren() | このテーブル内のすべての列、メジャー、および階層を返します。 | 
| `IEnumerable<IDetailObject>` | GetChildrenByFolders(`Boolean` recursive) |  | 
| `void` | Init() |  | 
| `void` | InitRLSIndexer() |  | 
| `void` | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue) |  | 
| `void` | OnPropertyChanging(`String` propertyName, `Object` newValue, `Boolean&` undoable, `Boolean&` cancel) |  | 
| `void` | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |  | 
| `void` | Undelete(`ITabularObjectCollection` collection) |  | 

Static Fields

| Type | Name | Summary | 
| --- | --- | --- | 
| `Char[]` | InvalidTableNameChars |  | 


## `TableCollection`

Table用のコレクションクラス。複数のオブジェクトに一度にプロパティを設定するための便利なプロパティを提供します。

```csharp
public class TabularEditor.TOMWrapper.TableCollection
    : TabularObjectCollection<Table, Table, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Table>, IEnumerable<Table>, IList<Table>, ITabularObjectCollection, IExpandableIndexer

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | DataCategory |  | 
| `String` | Description |  | 
| `Boolean` | IsHidden |  | 
| `Model` | Parent |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | ToString() |  | 

## `TableExtension`

```csharp
public static class TabularEditor.TOMWrapper.TableExtension

```

Static Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `PartitionSourceType` | GetSourceType(this `Table` table) |  | 

## `TableRLSIndexer`

TableRLSIndexerは、モデル内のすべてのロールにおいて、ある特定のテーブルで定義されたすべてのフィルタを参照するために使用されます。これはRoleRLSIndexerとは対照的で、1つの特定のロールの全テーブルに渡ってフィルタをブラウズします。

```csharp
public class TabularEditor.TOMWrapper.TableRLSIndexer
    : IEnumerable<String>, IEnumerable, IExpandableIndexer

```

Fields

| Type | Name | Summary | 
| --- | --- | --- | 
| `Table` | Table |  | 

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | Item |  | 
| `String` | Item |  | 
| `IEnumerable<String>` | Keys |  | 
| `Dictionary<ModelRole, String>` | RLSMap |  | 
| `String` | Summary |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `void` | Clear() |  | 
| `void` | CopyFrom(`TableRLSIndexer` source) |  | 
| `String` | GetDisplayName(`String` key) |  | 
| `IEnumerator<String>` | GetEnumerator() |  | 
| `void` | Refresh() |  | 
| `void` | SetRLS(`ModelRole` role, `String` filterExpression) |  | 

## `TabularCollectionHelper`

```csharp
public static class TabularEditor.TOMWrapper.TabularCollectionHelper

```

Static Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `void` | InPerspective(this `IEnumerable<Table>` tables, `String` perspective, `Boolean` value) |  | 
| `void` | InPerspective(this `IEnumerable<Column>` columns, `String` perspective, `Boolean` value) |  | 
| `void` | InPerspective(this `IEnumerable<Hierarchy>` hierarchies, `String` perspective, `Boolean` value) |  | 
| `void` | InPerspective(this `IEnumerable<Measure>` measures, `String` perspective, `Boolean` value) |  | 
| `void` | InPerspective(this `IEnumerable<Table>` tables, `Perspective` perspective, `Boolean` value) |  | 
| `void` | InPerspective(this `IEnumerable<Column>` columns, `Perspective` perspective, `Boolean` value) |  | 
| `void` | InPerspective(this `IEnumerable<Hierarchy>` hierarchies, `Perspective` perspective, `Boolean` value) |  | 
| `void` | InPerspective(this `IEnumerable<Measure>` measures, `Perspective` perspective, `Boolean` value) |  | 
| `void` | SetDisplayFolder(this `IEnumerable<Measure>` measures, `String` displayFolder) |  | 

## `TabularCommonActions`

複数のオブジェクトを一度に変更するような、Tabularモデル上の一般的な操作のための便利なメソッドを提供します。  例えば、これらのメソッドは、階層レベルや表示フォルダーなどを変更する UI ドラッグ＆ドロップ操作を簡単に実行するために使用されます。

```csharp
public class TabularEditor.TOMWrapper.TabularCommonActions

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `TabularModelHandler` | Handler |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `void` | AddColumnsToHierarchy(`IEnumerable<Column>` columns, `Hierarchy` hierarchy, `Int32` firstOrdinal = -1) |  | 
| `Level` | AddColumnToHierarchy(`Column` column, `Hierarchy` hierarchy, `Int32` ordinal = -1) |  | 
| `void` | MoveObjects(`IEnumerable<IDetailObject>` objects, `Table` newTable, `Culture` culture) |  | 
| `String` | NewColumnName(`String` prefix, `Table` table) |  | 
| `String` | NewMeasureName(`String` prefix) |  | 
| `void` | ReorderLevels(`IEnumerable<Level>` levels, `Int32` firstOrdinal) |  | 
| `void` | SetContainer(`IEnumerable<IDetailObject>` objects, `IDetailObjectContainer` newContainer, `Culture` culture) |  | 

## `TabularConnection`

```csharp
public static class TabularEditor.TOMWrapper.TabularConnection

```

Static Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | GetConnectionString(`String` serverName) |  | 
| `String` | GetConnectionString(`String` serverName, `String` userName, `String` password) |  | 

## `TabularCultureHelper`

```csharp
public static class TabularEditor.TOMWrapper.TabularCultureHelper

```

Static Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `Boolean` | ImportTranslations(`String` culturesJson, `Model` Model, `Boolean` overwriteExisting, `Boolean` haltOnError) |  | 

## `TabularDeployer`

```csharp
public class TabularEditor.TOMWrapper.TabularDeployer

```

Static Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `void` | Deploy(`Database` db, `String` targetConnectionString, `String` targetDatabaseName) | 指定されたデータベースを、指定されたオプションを使用して、指定されたターゲットサーバーおよびデータベースIDにデプロイします。  デプロイに成功した場合、データベース内のオブジェクトに関する DAX エラーのリスト (もしあれば) を返します。 | 
| `DeploymentResult` | Deploy(`Database` db, `String` targetConnectionString, `String` targetDatabaseID, `DeploymentOptions` options) | 指定したデータベースを、指定したオプションを用いて指定したターゲットサーバとデータベース ID にデプロイします。  デプロイに成功した場合は、データベース内のオブジェクトに対する DAX エラーのリストを返します。 | 
| `String` | GetTMSL(`Database` db, `Server` server, `String` targetDatabaseID, `DeploymentOptions` options) |  | 
| `void` | SaveModelMetadataBackup(`String` connectionString, `String` targetDatabaseID, `String` backupFilePath) |  | 
| `void` | WriteZip(`String` fileName, `String` content) |  | 

## `TabularModelHandler`

```csharp
public class TabularEditor.TOMWrapper.TabularModelHandler
    : IDisposable

```

Fields

| Type | Name | Summary | 
| --- | --- | --- | 
| `Dictionary<String, ITabularObjectCollection>` | WrapperCollections |  | 
| `Dictionary<MetadataObject, TabularObject>` | WrapperLookup |  | 

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `TabularCommonActions` | Actions |  | 
| `Boolean` | AutoFixup | オブジェクト名 (テーブル、列、メジャー) の変更によって、変更された名前を反映するために DAX 式を自動的に更新 するかどうかを指定します。True に設定すると、モデル内のすべての式が解析され、依存関係ツリーが構築されます。 | 
| `Database` | Database |  | 
| `Boolean` | DelayBuildDependencyTree |  | 
| `IList<Tuple<NamedMetadataObject, String>>` | Errors |  | 
| `Boolean` | HasUnsavedChanges |  | 
| `Boolean` | IsConnected |  | 
| `Model` | Model |  | 
| `String` | Status |  | 
| `TabularTree` | Tree |  | 
| `UndoManager` | UndoManager |  | 
| `Int64` | Version |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `IDetailObject` | Add(`AddObjectType` objectType, `IDetailObjectContainer` container) |  | 
| `void` | BeginUpdate(`String` undoName) |  | 
| `void` | BuildDependencyTree(`IExpressionObject` expressionObj) |  | 
| `void` | BuildDependencyTree() |  | 
| `ConflictInfo` | CheckConflicts() |  | 
| `IList<TabularNamedObject>` | DeserializeObjects(`String` json) |  | 
| `void` | Dispose() |  | 
| `void` | DoFixup(`IDaxObject` obj, `String` newName) | オブジェクト "obj" へのすべての参照を "newName" を反映するように変更します。 | 
| `Int32` | EndUpdate(`Boolean` undoable = True, `Boolean` rollback = False) |  | 
| `Int32` | EndUpdateAll(`Boolean` rollback = False) |  | 
| `Model` | GetModel() |  | 
| `Boolean` | ImportTranslations(`String` culturesJson, `Boolean` overwriteExisting, `Boolean` ignoreInvalid) | JSON文字列から翻訳を適用します。 | 
| `void` | SaveDB() | データベースへの変更を保存します。TOMWrapperにロード（読み込み）されてから、データベースに変更が加えられたかどうかをチェックするのは、ユーザーの責任です。この目的のために、［Handler.CheckConflicts()］を利用することができます。 | 
| `void` | SaveFile(`String` fileName, `SerializeOptions` options) |  | 
| `void` | SaveToFolder(`String` path, `SerializeOptions` options) |  | 
| `String` | ScriptCreateOrReplace() | Scripts the entire database | 
| `String` | ScriptCreateOrReplace(`TabularNamedObject` obj) | Scripts the entire database | 
| `String` | ScriptTranslations(`IEnumerable<Culture>` translations) |  | 
| `String` | SerializeObjects(`IEnumerable<TabularNamedObject>` objects) |  | 
| `void` | UpdateFolders(`Table` table) |  | 
| `void` | UpdateLevels(`Hierarchy` hierarchy) |  | 
| `void` | UpdateObject(`ITabularObject` obj) |  | 
| `void` | UpdateTables() |  | 

Static Fields

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | PROP_ERRORS |  | 
| `String` | PROP_HASUNSAVEDCHANGES |  | 
| `String` | PROP_ISCONNECTED |  | 
| `String` | PROP_STATUS |  | 

Static Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `TabularModelHandler` | Singleton |  | 

Static Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `List<Tuple<NamedMetadataObject, String>>` | CheckErrors(`Database` database) |  | 
| `List<Tuple<NamedMetadataObject, ObjectState>>` | CheckProcessingState(`Database` database) |  | 

## `TabularNamedObject`

TabularObjectはMicrosoft.AnalysisServices.Tabular.NamedMetadataObjectクラスのラッパーのようなものです。  このラッパーは、Tabular Editorで表示および編集可能なすべてのオブジェクトに使用されます。  同じベースクラスが、Tabularモデル内のすべての種類のオブジェクトに使用されます。この基底クラスは（ローカライズされた）名前と説明を編集するためのメソッドを提供します。

```csharp
public abstract class TabularEditor.TOMWrapper.TabularNamedObject
    : TabularObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable
```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `Int32` | MetadataIndex |  | 
| `NamedMetadataObject` | MetadataObject |  | 
| `String` | Name |  | 
| `TranslationIndexer` | TranslatedNames | このオブジェクトのローカライズされた名前のコレクション。 | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `TabularNamedObject` | Clone(`String` newName, `Boolean` includeTranslations) |  | 
| `Int32` | CompareTo(`Object` obj) |  | 
| `void` | Delete() |  | 
| `void` | Init() |  | 
| `void` | Undelete(`ITabularObjectCollection` collection) | 削除操作を取り消すには、ハッキーな回避策が必要です。  派生クラスは、対象のオブジェクトが "所有する" すべてのオブジェクトを更新するように注意する必要があります。例えば、メジャーは、その KPI のラッパー (存在する場合) を更新するように注意する必要があります。 | 

## `TabularObject`

```csharp
public abstract class TabularEditor.TOMWrapper.TabularObject
    : ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging

```

Fields

| Type | Name | Summary | 
| --- | --- | --- | 
| `ITabularObjectCollection` | Collection |  | 
| `TabularModelHandler` | Handler |  | 

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `MetadataObject` | MetadataObject |  | 
| `Model` | Model |  | 
| `ObjectType` | ObjectType |  | 
| `String` | ObjectTypeName |  | 
| `TranslationIndexer` | TranslatedDescriptions |  | 
| `TranslationIndexer` | TranslatedDisplayFolders |  | 

Events

| Type | Name | Summary | 
| --- | --- | --- | 
| `PropertyChangedEventHandler` | PropertyChanged |  | 
| `PropertyChangingEventHandler` | PropertyChanging |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `void` | Init() | 派生したメンバは、子オブジェクトをインスタンス化するためにこのメソッドをオーバーライドする必要があります。 | 
| `void` | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue) |  | 
| `void` | OnPropertyChanging(`String` propertyName, `Object` newValue, `Boolean&` undoable, `Boolean&` cancel) | オブジェクトのプロパティが変更される前に呼び出されます。派生クラスは、変更がどのように処理されるかを制御することができます。  このメソッド内でArgumentExceptionを投げると、UIにエラーメッセージが表示されます。 | 
| `Boolean` | SetField(`T&` field, `T` value, `String` propertyName = null) |  | 

## `TabularObjectCollection<T, TT, TP>`

```csharp
public abstract class TabularEditor.TOMWrapper.TabularObjectCollection<T, TT, TP>
    : IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<T>, IEnumerable<T>, IList<T>, ITabularObjectCollection, IExpandableIndexer

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | CollectionName |  | 
| `Int32` | Count |  | 
| `TabularModelHandler` | Handler |  | 
| `Boolean` | IsFixedSize |  | 
| `Boolean` | IsReadOnly |  | 
| `Boolean` | IsSynchronized |  | 
| `T` | Item |  | 
| `T` | Item |  | 
| `IEnumerable<String>` | Keys |  | 
| `NamedMetadataObjectCollection<TT, TP>` | MetadataObjectCollection |  | 
| `String` | Summary |  | 
| `Object` | SyncRoot |  | 

Events

| Type | Name | Summary | 
| --- | --- | --- | 
| `NotifyCollectionChangedEventHandler` | CollectionChanged |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `void` | Add(`T` item) |  | 
| `void` | Add(`TabularNamedObject` item) |  | 
| `Int32` | Add(`Object` value) |  | 
| `void` | Clear() |  | 
| `Boolean` | Contains(`T` item) |  | 
| `Boolean` | Contains(`Object` value) |  | 
| `Boolean` | Contains(`String` name) |  | 
| `void` | CopyTo(`T[]` array, `Int32` arrayIndex) |  | 
| `void` | CopyTo(`Array` array, `Int32` index) |  | 
| `void` | ForEach(`Action<T>` action) |  | 
| `ITabularObjectCollection` | GetCurrentCollection() |  | 
| `String` | GetDisplayName(`String` key) |  | 
| `IEnumerator<T>` | GetEnumerator() |  | 
| `Int32` | IndexOf(`TabularNamedObject` obj) |  | 
| `Int32` | IndexOf(`T` item) |  | 
| `Int32` | IndexOf(`Object` value) |  | 
| `void` | Insert(`Int32` index, `T` item) |  | 
| `void` | Insert(`Int32` index, `Object` value) |  | 
| `void` | Refresh() |  | 
| `void` | Remove(`TabularNamedObject` item) |  | 
| `Boolean` | Remove(`T` item) |  | 
| `void` | Remove(`Object` value) |  | 
| `void` | RemoveAt(`Int32` index) |  | 

## `TabularObjectComparer`

```csharp
public class TabularEditor.TOMWrapper.TabularObjectComparer
    : IComparer<ITabularNamedObject>, IComparer

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `ObjectOrder` | Order |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `Int32` | Compare(`Object` x, `Object` y) |  | 
| `Int32` | Compare(`ITabularNamedObject` x, `ITabularNamedObject` y) |  | 

## `TabularObjectHelper`

```csharp
public static class TabularEditor.TOMWrapper.TabularObjectHelper

```

Static Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | GetLinqPath(this `TabularNamedObject` obj) |  | 
| `String` | GetName(this `ITabularNamedObject` obj, `Culture` culture) |  | 
| `String` | GetObjectPath(this `MetadataObject` obj) |  | 
| `String` | GetObjectPath(this `TabularObject` obj) |  | 
| `String` | GetTypeName(this `ObjectType` objType, `Boolean` plural = False) |  | 
| `String` | GetTypeName(this `ITabularObject` obj, `Boolean` plural = False) |  | 
| `Boolean` | SetName(this `ITabularNamedObject` obj, `String` newName, `Culture` culture) |  | 
| `String` | SplitCamelCase(this `String` str) |  | 

## `TabularTree`

TabularLogicalModelはTreeViewAdvコントロールに表示するためのTabularObject間の関係を制御します。個々のTabularObjectは他のオブジェクトとの論理的な関係（例えば、特定のカルチャーのDisplayFoldersを通して）を知りませんし、気にすることもありません。TabularObjectはTabular Object Modelから直接継承される物理的な関係のみを気にします（例えば、メジャーはテーブルに属する、など）。

```csharp
public abstract class TabularEditor.TOMWrapper.TabularTree
    : INotifyPropertyChanged

```

Fields

| Type | Name | Summary | 
| --- | --- | --- | 
| `Dictionary<String, Folder>` | FolderTree |  | 

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `Culture` | Culture |  | 
| `String` | Filter |  | 
| `TabularModelHandler` | Handler |  | 
| `Model` | Model |  | 
| `LogicalTreeOptions` | Options |  | 
| `Perspective` | Perspective |  | 
| `Int32` | UpdateLocks |  | 

Events

| Type | Name | Summary | 
| --- | --- | --- | 
| `PropertyChangedEventHandler` | PropertyChanged |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `void` | BeginUpdate() |  | 
| `void` | EndUpdate() |  | 
| `IEnumerable` | GetChildren(`ITabularObjectContainer` tabularObject) | このメソッドは、表形式モデルのツリー表現がどのように構成されるべきかというロジックをカプセル化するものである | 
| `Func<String, String>` | GetFolderMutation(`Object` source, `Object` destination) |  | 
| `Func<String, String>` | GetFolderMutation(`String` oldPath, `String` newPath) |  | 
| `void` | ModifyDisplayFolder(`Table` table, `String` oldPath, `String` newPath, `Culture` culture) | 1つのテーブル内のすべてのタブラーオブジェクトのDisplayFolderプロパティを更新します。更新されたパスのサブフォルダに存在するオブジェクトも更新される。 | 
| `void` | OnNodesChanged(`ITabularObject` nodeItem) |  | 
| `void` | OnNodesInserted(`ITabularObject` parent, `ITabularObject[]` children) |  | 
| `void` | OnNodesInserted(`ITabularObject` parent, `IEnumerable<ITabularObject>` children) |  | 
| `void` | OnNodesRemoved(`ITabularObject` parent, `ITabularObject[]` children) |  | 
| `void` | OnNodesRemoved(`ITabularObject` parent, `IEnumerable<ITabularObject>` children) |  | 
| `void` | OnStructureChanged(`ITabularNamedObject` obj = null) |  | 
| `void` | SetCulture(`String` cultureName) |  | 
| `void` | SetPerspective(`String` perspectiveName) |  | 
| `void` | UpdateFolder(`Folder` folder, `String` oldFullPath = null) |  | 
| `Boolean` | VisibleInTree(`ITabularNamedObject` tabularObject) |  | 

## `TranslationIndexer`

```csharp
public class TabularEditor.TOMWrapper.TranslationIndexer
    : IEnumerable<String>, IEnumerable, IExpandableIndexer

```

Properties

| Type | Name | Summary | 
| --- | --- | --- | 
| `String` | DefaultValue |  | 
| `String` | Item |  | 
| `String` | Item |  | 
| `IEnumerable<String>` | Keys |  | 
| `String` | Summary |  | 
| `Int32` | TranslatedCount |  | 

Methods

| Type | Name | Summary | 
| --- | --- | --- | 
| `void` | Clear() | オブジェクトの翻訳された値をすべてクリアします。 | 
| `Boolean` | Contains(`Culture` culture) |  | 
| `Dictionary<String, String>` | Copy() |  | 
| `void` | CopyFrom(`TranslationIndexer` translations, `Func<String, String>` mutator = null) |  | 
| `void` | CopyFrom(`IDictionary<String, String>` source) |  | 
| `String` | GetDisplayName(`String` key) |  | 
| `IEnumerator<String>` | GetEnumerator() |  | 
| `void` | Refresh() |  | 
| `void` | Reset() | オブジェクトの翻訳をリセットします。キャプションのトランスレーションが削除され、オブジェクトはすべてのロケールでベース名で表示されます。Display FolderとDescriptionのトランスレ-ションは、オブジェクトの未翻訳の値に設定されます。| 
| `void` | SetAll(`String` value) |  | 
