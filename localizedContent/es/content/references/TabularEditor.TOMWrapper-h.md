# Referencia de TabularEditor.TOMWrapper

Esta es documentación generada automáticamente para la API de TOMWrapper. Usa CTRL+F o la barra lateral de la derecha para localizar una clase, una propiedad o un método concretos.

## `AddObjectType`

```csharp
public enum TabularEditor.TOMWrapper.AddObjectType
    : Enum, IComparable, IFormattable, IConvertible

```

Enumeración

| Valor | Nombre           | Resumen |
| ----- | ---------------- | ------- |
| `1`   | Medida           |         |
| `2`   | CalculatedColumn |         |
| `3`   | Jerarquía        |         |

## `CalculatedColumn`

Declaración de la clase base de CalculatedColumn

```csharp
public class TabularEditor.TOMWrapper.CalculatedColumn
    : Column, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IErrorMessageObject, IDescriptionObject, IAnnotationObject, ITabularPerspectiveObject, IDaxObject, IExpressionObject

```

Propiedades

| Tipo                                       | Nombre             | Resumen                                                                                  |
| ------------------------------------------ | ------------------ | ---------------------------------------------------------------------------------------- |
| `Dictionary<IDaxObject, List<Dependency>>` | Dependencias       |                                                                                          |
| `String`                                   | Expresión          | Obtiene o establece la expresión de CalculatedColumn.                    |
| `Boolean`                                  | IsDataTypeInferred | Obtiene o establece la propiedad IsDataTypeInferred de CalculatedColumn. |
| `CalculatedColumn`                         | MetadataObject     |                                                                                          |
| `Boolean`                                  | NeedsValidation    |                                                                                          |

Métodos

| Tipo                 | Nombre                                                                                                   | Resumen |
| -------------------- | -------------------------------------------------------------------------------------------------------- | ------- |
| `TabularNamedObject` | Clone(`String` newName = null, `Boolean` includeTranslations = True)                  |         |
| `TabularNamedObject` | CloneTo(`Table` table, `String` newName = null, `Boolean` includeTranslations = True) |         |
| `void`               | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue)        |         |

## `CalculatedTable`

```csharp
public class TabularEditor.TOMWrapper.CalculatedTable
    : Table, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IHideableObject, IDescriptionObject, IAnnotationObject, ITabularObjectContainer, IDetailObjectContainer, ITabularPerspectiveObject, IDaxObject, IDynamicPropertyObject, IErrorMessageObject, IExpressionObject

```

Propiedades

| Tipo                                       | Nombre          | Resumen |
| ------------------------------------------ | --------------- | ------- |
| `Dictionary<IDaxObject, List<Dependency>>` | Dependencias    |         |
| `String`                                   | Expresión       |         |
| `Boolean`                                  | NeedsValidation |         |
| `String`                                   | ObjectTypeName  |         |

Métodos

| Tipo      | Nombre                                                                                            | Resumen                                                                                                                                                                   |
| --------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `void`    | CheckChildrenErrors()                                                          |                                                                                                                                                                           |
| `Boolean` | Editable(`String` propertyName)                                                |                                                                                                                                                                           |
| `void`    | Init()                                                                         |                                                                                                                                                                           |
| `void`    | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue) |                                                                                                                                                                           |
| `void`    | ReinitColumns()                                                                | Llame a este método después de guardar el modelo en una base de datos para comprobar si hay columnas modificadas (por si han cambiado las expresiones) |

## `CalculatedTableColumn`

Declaración de la clase base para CalculatedTableColumn

```csharp
public class TabularEditor.TOMWrapper.CalculatedTableColumn
    : Column, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IErrorMessageObject, IDescriptionObject, IAnnotationObject, ITabularPerspectiveObject, IDaxObject

```

Propiedades

| Tipo                    | Nombre             | Resumen                                                                                       |
| ----------------------- | ------------------ | --------------------------------------------------------------------------------------------- |
| `Column`                | ColumnOrigin       | Obtiene o establece la propiedad ColumnOrigin de CalculatedTableColumn.       |
| `Boolean`               | IsDataTypeInferred | Obtiene o establece la propiedad IsDataTypeInferred de CalculatedTableColumn. |
| `Boolean`               | IsNameInferred     | Obtiene o establece la propiedad IsNameInferred de CalculatedTableColumn.     |
| `CalculatedTableColumn` | MetadataObject     |                                                                                               |
| `String`                | SourceColumn       | Obtiene o establece la propiedad SourceColumn de CalculatedTableColumn.       |

## `Column`

Declaración de la clase base para Column

```csharp
public abstract class TabularEditor.TOMWrapper.Column
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IErrorMessageObject, IDescriptionObject, IAnnotationObject, ITabularPerspectiveObject, IDaxObject

```

Propiedades

| Tipo                         | Nombre                                             | Resumen                                                                                                              |
| ---------------------------- | -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `Alignment`                  | Alignment                                          | Obtiene o establece la propiedad Alignment de la columna.                                            |
| `String`                     | DataCategory                                       | Obtiene o establece la propiedad DataCategory de la columna.                                         |
| `DataType`                   | DataType                                           | Obtiene o establece la propiedad DataType de la columna.                                             |
| `String`                     | DaxObjectFullName                                  |                                                                                                                      |
| `String`                     | DaxObjectName                                      |                                                                                                                      |
| `String`                     | DaxTableName                                       |                                                                                                                      |
| `HashSet<IExpressionObject>` | Dependants                                         |                                                                                                                      |
| `String`                     | Description                                        | Obtiene o establece la propiedad Description de la columna.                                          |
| `String`                     | DisplayFolder                                      | Obtiene o establece la propiedad DisplayFolder de la columna.                                        |
| `Int32`                      | DisplayOrdinal                                     | Obtiene o establece la propiedad DisplayOrdinal de la columna.                                       |
| `String`                     | ErrorMessage                                       | Obtiene o establece la propiedad ErrorMessage de la columna.                                         |
| `String`                     | FormatString                                       | Obtiene o establece la propiedad FormatString de la columna.                                         |
| `IndexadorDePerspectiva`     | EnPerspectiva                                      |                                                                                                                      |
| `Boolean`                    | IsAvailableInMDX                                   | Obtiene o establece la propiedad IsAvailableInMDX de la columna.                                     |
| `Boolean`                    | IsDefaultImage                                     | Obtiene o establece la propiedad IsDefaultImage de la columna.                                       |
| `Boolean`                    | IsDefaultLabel                                     | Obtiene o establece la propiedad IsDefaultLabel de la columna.                                       |
| `Boolean`                    | IsHidden                                           | Obtiene o establece la propiedad IsHidden de la columna.                                             |
| `Boolean`                    | IsKey                                              | Obtiene o establece la propiedad IsKey de la columna.                                                |
| `Boolean`                    | IsNullable                                         | Obtiene o establece la propiedad IsNullable de la columna.                                           |
| `Boolean`                    | IsUnique                                           | Obtiene o establece la propiedad IsUnique de la columna.                                             |
| `Boolean`                    | KeepUniqueRows                                     | Obtiene o establece la propiedad KeepUniqueRows de la columna.                                       |
| `Column`                     | MetadataObject                                     |                                                                                                                      |
| `Column`                     | SortByColumn                                       | Obtiene o establece la propiedad SortByColumn de la columna.                                         |
| `String`                     | SourceProviderType                                 | Obtiene o establece la propiedad SourceProviderType de la columna.                                   |
| `ObjectState`                | State                                              | Obtiene o establece la propiedad State de la columna.                                                |
| `AggregateFunction`          | SummarizeBy                                        | Obtiene o establece la propiedad SummarizeBy de la columna.                                          |
| `Table`                      | Table                                              |                                                                                                                      |
| `Int32`                      | TableDetailPosition                                | Obtiene o establece el valor de TableDetailPosition de la columna.                                   |
| `TranslationIndexer`         | TranslatedDescriptions                             | Colección de descripciones localizadas para esta columna.                                            |
| `TranslationIndexer`         | TranslatedDisplayFolders                           | Colección de carpetas de visualización localizadas para esta columna.                                |
| `ColumnType`                 | Tipo                                               | Obtiene o establece el tipo de la columna.                                                           |
| `IEnumerable<Hierarchy>`     | Se usa en jerarquías<a id="used-in-hierarchy"></a> | Enumera todas las jerarquías en las que esta columna se usa como nivel.                              |
| `IEnumerable<Relationship>`  | Se usa en relaciones                               | Enumera todas las relaciones en las que participa esta columna (ya sea como  o ). |

Métodos

| Tipo     | Nombre                                                                                                                  | Resumen |
| -------- | ----------------------------------------------------------------------------------------------------------------------- | ------- |
| `void`   | Delete()                                                                                             |         |
| `String` | GetAnnotation(`String` name)                                                                         |         |
| `void`   | Init()                                                                                               |         |
| `void`   | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue)                       |         |
| `void`   | OnPropertyChanging(`String` propertyName, `Object` newValue, `Boolean&` undoable, `Boolean&` cancel) |         |
| `void`   | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True)                              |         |
| `void`   | Undelete(`ITabularObjectCollection` collection)                                                      |         |

## `ColumnCollection`

Clase de colección de `Column`. Proporciona propiedades útiles para establecer una propiedad en varios objetos a la vez.

```csharp
public class TabularEditor.TOMWrapper.ColumnCollection
    : TabularObjectCollection<Column, Column, Table>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Column>, IEnumerable<Column>, IList<Column>, ITabularObjectCollection, IExpandableIndexer

```

Propiedades

| Tipo                | Nombre              | Resumen |
| ------------------- | ------------------- | ------- |
| `Alignment`         | Alignment           |         |
| `String`            | DataCategory        |         |
| `DataType`          | DataType            |         |
| `String`            | Descripción         |         |
| `String`            | DisplayFolder       |         |
| `Int32`             | DisplayOrdinal      |         |
| `String`            | FormatString        |         |
| `Boolean`           | IsAvailableInMDX    |         |
| `Boolean`           | IsDefaultImage      |         |
| `Boolean`           | IsDefaultLabel      |         |
| `Boolean`           | IsHidden            |         |
| `Boolean`           | IsKey               |         |
| `Boolean`           | IsNullable          |         |
| `Boolean`           | IsUnique            |         |
| `Boolean`           | KeepUniqueRows      |         |
| `Table`             | Padre               |         |
| `Column`            | SortByColumn        |         |
| `String`            | SourceProviderType  |         |
| `AggregateFunction` | SummarizeBy         |         |
| `Int32`             | TableDetailPosition |         |

Métodos

| Tipo                  | Nombre                             | Resumen |
| --------------------- | ---------------------------------- | ------- |
| `IEnumerator<Column>` | GetEnumerator() |         |
| `String`              | ToString()      |         |

## `configuración regional`

Declaración de la clase base de la configuración regional

```csharp
public class TabularEditor.TOMWrapper.Culture
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IAnnotationObject, IDynamicPropertyObject

```

Propiedades

| Tipo                          | Nombre                                                    | Resumen |
| ----------------------------- | --------------------------------------------------------- | ------- |
| `String`                      | Nombre para mostrar                                       |         |
| `configuración regional`      | Objeto de metadatos                                       |         |
| `String`                      | Nombre                                                    |         |
| `ObjectTranslationCollection` | Traducciones del objeto                                   |         |
| `String`                      | Títulos de columnas de estadísticas                       |         |
| `String`                      | Carpetas de visualización para columnas de estadísticas   |         |
| `String`                      | Títulos de jerarquías de estadísticas                     |         |
| `String`                      | Carpetas de visualización para jerarquías de estadísticas |         |
| `String`                      | Títulos de niveles de estadísticas                        |         |
| `String`                      | Títulos de medidas de estadísticas                        |         |
| `String`                      | Carpetas de visualización para medidas de estadísticas    |         |
| `String`                      | Títulos de tablas de estadísticas                         |         |
| `Boolean`                     | Sin asignar                                               |         |

Métodos

| Tipo                 | Nombre                                                                                            | Resumen |
| -------------------- | ------------------------------------------------------------------------------------------------- | ------- |
| `Boolean`            | Browsable(`String` propertyName)                                               |         |
| `TabularNamedObject` | Clone(`String` newName, `Boolean` includeTranslations)                         |         |
| `Boolean`            | Editable(`String` propertyName)                                                |         |
| `String`             | GetAnnotation(`String` name)                                                   |         |
| `void`               | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue) |         |
| `void`               | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True)        |         |
| `void`               | Undelete(`ITabularObjectCollection` collection)                                |         |

## `CultureCollection`

Clase de colección de jerarquías. Proporciona propiedades convenientes para establecer una propiedad en varios objetos a la vez.

```csharp
public class TabularEditor.TOMWrapper.CultureCollection
    : TabularObjectCollection<Culture, Culture, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Culture>, IEnumerable<Culture>, IList<Culture>, ITabularObjectCollection, IExpandableIndexer
// Culture: configuración regional

```

Propiedades

| Tipo    | Nombre | Resumen |
| ------- | ------ | ------- |
| `Model` | Padre  |         |

Métodos

| Tipo     | Nombre                        | Resumen |
| -------- | ----------------------------- | ------- |
| `String` | ToString() |         |

## `CultureConverter`

```csharp
public class TabularEditor.TOMWrapper.CultureConverter
    : TypeConverter

```

Métodos

| Tipo                       | Nombre                                                                                                                                                                          | Resumen |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- |
| `Boolean`                  | CanConvertFrom(`ITypeDescriptorContext` context, `Type` sourceType)                                                                                          |         |
| `Boolean`                  | CanConvertTo(`ITypeDescriptorContext` context, `Type` destinationType)                                                                                       |         |
| `Object`                   | ConvertFrom(`ITypeDescriptorContext` context, `CultureInfo` culture, `Object` value) — culture: configuración regional                       |         |
| `Object`                   | ConvertTo(`ITypeDescriptorContext` context, `CultureInfo` culture, `Object` value, `Type` destinationType) — culture: configuración regional |         |
| `StandardValuesCollection` | GetStandardValues(`ITypeDescriptorContext` context)                                                                                                          |         |
| `Boolean`                  | GetStandardValuesExclusive(`ITypeDescriptorContext` context)                                                                                                 |         |
| `Boolean`                  | GetStandardValuesSupported(`ITypeDescriptorContext` context)                                                                                                 |         |

## `Database`

```csharp
public class TabularEditor.TOMWrapper.Database

```

Propiedades

| Tipo                 | Nombre             | Resumen |
| -------------------- | ------------------ | ------- |
| `Nullable<Int32>`    | CompatibilityLevel |         |
| `Nullable<DateTime>` | CreatedTimestamp   |         |
| `String`             | ID                 |         |
| `Nullable<DateTime>` | LastProcessed      |         |
| `Nullable<DateTime>` | LastSchemaUpdate   |         |
| `Nullable<DateTime>` | LastUpdate         |         |
| `String`             | Name               |         |
| `String`             | ServerName         |         |
| `String`             | ServerVersion      |         |
| `Database`           | TOMDatabase        |         |
| `Nullable<Int64>`    | Version            |         |

Métodos

| Tipo     | Nombre                        | Resumen |
| -------- | ----------------------------- | ------- |
| `String` | ToString() |         |

## `DataColumn`

Declaración de la clase base para DataColumn

```csharp
public class TabularEditor.TOMWrapper.DataColumn
    : Column, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IErrorMessageObject, IDescriptionObject, IAnnotationObject, ITabularPerspectiveObject, IDaxObject

```

Propiedades

| Tipo         | Nombre         | Resumen                                                                               |
| ------------ | -------------- | ------------------------------------------------------------------------------------- |
| `DataColumn` | MetadataObject |                                                                                       |
| `String`     | SourceColumn   | Obtiene o establece la propiedad SourceColumn de la clase DataColumn. |

## `DataSource`

Declaración de la clase base de DataSource

```csharp
public abstract class TabularEditor.TOMWrapper.DataSource
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject

```

Propiedades

| Tipo                 | Nombre                 | Resumen                                                                      |
| -------------------- | ---------------------- | ---------------------------------------------------------------------------- |
| `String`             | Descripción            | Obtiene o establece la descripción del DataSource.           |
| `DataSource`         | MetadataObject         |                                                                              |
| `TranslationIndexer` | TranslatedDescriptions | Colección de descripciones localizadas para este DataSource. |
| `DataSourceType`     | Tipo                   | Obtiene o establece el tipo del DataSource.                  |

Métodos

| Tipo     | Nombre                                                                                     | Resumen |
| -------- | ------------------------------------------------------------------------------------------ | ------- |
| `String` | GetAnnotation(`String` name)                                            |         |
| `void`   | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |         |

## `DataSourceCollection`

Clase de colección para DataSource. Ofrece propiedades convenientes para establecer una propiedad en varios objetos a la vez.

```csharp
public class TabularEditor.TOMWrapper.DataSourceCollection
    : TabularObjectCollection<DataSource, DataSource, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<DataSource>, IEnumerable<DataSource>, IList<DataSource>, ITabularObjectCollection, IExpandableIndexer

```

Propiedades

| Tipo     | Nombre      | Resumen |
| -------- | ----------- | ------- |
| `String` | Descripción |         |
| `Model`  | Padre       |         |

Métodos

| Tipo     | Nombre                        | Resumen |
| -------- | ----------------------------- | ------- |
| `String` | ToString() |         |

## `Dependency`

```csharp
public struct TabularEditor.TOMWrapper.Dependency

```

Campos

| Tipo      | Nombre         | Resumen |
| --------- | -------------- | ------- |
| `Int32`   | desde          |         |
| `Boolean` | fullyQualified |         |
| `Int32`   | hasta          |         |

## `DependencyHelper`

```csharp
public static class TabularEditor.TOMWrapper.DependencyHelper

```

Métodos estáticos

| Tipo     | Nombre                                                                                                                                         | Resumen                                                                                                                          |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `void`   | AddDep(this `IExpressionObject` target, `IDaxObject` dependsOn, `Int32` fromChar, `Int32` toChar, `Boolean` fullyQualified) |                                                                                                                                  |
| `String` | NoQ(this `String` objectName, `Boolean` table = False)                                                                      | Elimina calificadores como ' ' y [ ] alrededor de un nombre. |

## `DeploymentMode`

```csharp
public enum TabularEditor.TOMWrapper.DeploymentMode
    : Enum, IComparable, IFormattable, IConvertible

```

Enum

| Valor | Nombre         | Resumen |
| ----- | -------------- | ------- |
| `0`   | CreateDatabase |         |
| `1`   | CreateOrAlter  |         |

## `DeploymentOptions`

```csharp
public class TabularEditor.TOMWrapper.DeploymentOptions

```

Campos

| Tipo             | Nombre                     | Resumen |
| ---------------- | -------------------------- | ------- |
| `Boolean`        | DeployConnections          |         |
| `DeploymentMode` | DeployMode                 |         |
| `Boolean`        | Desplegar particiones      |         |
| `Boolean`        | Desplegar miembros del rol |         |
| `Boolean`        | Desplegar roles            |         |

Campos estáticos

| Tipo                | Nombre         | Resumen |
| ------------------- | -------------- | ------- |
| `DeploymentOptions` | Predeterminado |         |
| `DeploymentOptions` | StructureOnly  |         |

## `DeploymentResult`

```csharp
public class TabularEditor.TOMWrapper.DeploymentResult

```

Campos

| Tipo                    | Nombre       | Resumen |
| ----------------------- | ------------ | ------- |
| `IReadOnlyList<String>` | Problemas    |         |
| `IReadOnlyList<String>` | Advertencias |         |

## `DeploymentStatus`

```csharp
public enum TabularEditor.TOMWrapper.DeploymentStatus
    : Enum, IComparable, IFormattable, IConvertible

```

Enumeración

| Valor | Nombre          | Resumen |
| ----- | --------------- | ------- |
| `0`   | ChangesSaved    |         |
| `1`   | DeployComplete  |         |
| `2`   | DeployCancelled |         |

## `Folder`

Representa una carpeta en el TreeView. No se corresponde con ningún objeto en el TOM.  Implementa IDisplayFolderObject, ya que una carpeta también puede estar ubicada dentro de otra carpeta de visualización.  Implementa IParentObject, ya que una carpeta puede contener objetos secundarios.

```csharp
public class TabularEditor.TOMWrapper.Folder
    : IDetailObject, ITabularTableObject, ITabularNamedObject, ITabularObject, INotifyPropertyChanged, ITabularObjectContainer, IDetailObjectContainer, IErrorMessageObject

```

Propiedades

| Tipo                     | Nombre                   | Resumen |
| ------------------------ | ------------------------ | ------- |
| `IDetailObjectContainer` | Container                |         |
| `configuración regional` | Configuración regional   |         |
| `String`                 | DisplayFolder            |         |
| `String`                 | ErrorMessage             |         |
| `String`                 | FullPath                 |         |
| `TabularModelHandler`    | Handler                  |         |
| `Int32`                  | MetadataIndex            |         |
| `Model`                  | Model                    |         |
| `String`                 | Nombre                   |         |
| `ObjectType`             | ObjectType               |         |
| `Table`                  | ParentTable              |         |
| `String`                 | Path                     |         |
| `Table`                  | Table                    |         |
| `TranslationIndexer`     | TranslatedDisplayFolders |         |
| `TranslationIndexer`     | TranslatedNames          |         |

Eventos

| Tipo                          | Nombre          | Resumen |
| ----------------------------- | --------------- | ------- |
| `PropertyChangedEventHandler` | PropertyChanged |         |

Métodos

| Tipo                               | Nombre                                                               | Resumen                                                                                                                                                                                                                                                     |
| ---------------------------------- | -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `void`                             | CheckChildrenErrors()                             |                                                                                                                                                                                                                                                             |
| `void`                             | Delete()                                          | Eliminar una carpeta no elimina los objetos secundarios; solo elimina la carpeta.  Las carpetas secundarias se conservan (pero se moverán un nivel arriba en la jerarquía de carpetas de visualización). |
| `IEnumerable<ITabularNamedObject>` | GetChildren()                                     |                                                                                                                                                                                                                                                             |
| `IEnumerable<IDetailObject>`       | GetChildrenByFolders(`Boolean` recursive = False) |                                                                                                                                                                                                                                                             |
| `void`                             | SetFolderName(`String` newName)                   |                                                                                                                                                                                                                                                             |
| `void`                             | UndoSetPath(`String` value)                       |                                                                                                                                                                                                                                                             |

Métodos estáticos

| Tipo     | Nombre                                                                                                                                            | Resumen |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ------- |
| `Folder` | CreateFolder(`Table` table, `String` path = , `Boolean` useFixedCulture = False, `configuración regional` fixedCulture = null) |         |

## `FolderHelper`

```csharp
public static class TabularEditor.TOMWrapper.FolderHelper

```

Métodos estáticos

| Tipo                     | Nombre                                                                                                                           | Resumen |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------- | ------- |
| `String`                 | ConcatPath(this `String` path, `String` additionalPath)                                                       |         |
| `String`                 | ConcatPath(this `IEnumerable<String>` pathBits)                                                               |         |
| `IDetailObjectContainer` | GetContainer(this `IDetailObject` obj)                                                                        |         |
| `String`                 | GetDisplayFolder(this `IDetailObject` folderObject, `configuración regional` culture)                         |         |
| `String`                 | GetFullPath(`ITabularNamedObject` obj)                                                                        |         |
| `Boolean`                | HasAncestor(this `IDetailObject` child, `ITabularNamedObject` ancestor, `configuración regional` culture)     |         |
| `Boolean`                | HasParent(this `IDetailObject` child, `ITabularNamedObject` parent, `configuración regional` culture)         |         |
| `Int32`                  | Level(this `String` path)                                                                                     |         |
| `String`                 | PathFromFullPath(`String` path)                                                                               |         |
| `void`                   | SetDisplayFolder(this `IDetailObject` folderObject, `String` newFolderName, `configuración regional` culture) |         |
| `String`                 | TrimFolder(this `String` folderPath)                                                                          |         |

## `Hierarchy`

Declaración de la clase base para Hierarchy

```csharp
public class TabularEditor.TOMWrapper.Hierarchy
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IDescriptionObject, IAnnotationObject, ITabularObjectContainer, ITabularPerspectiveObject

```

Propiedades

| Tipo                     | Nombre                   | Resumen                                                                                             |
| ------------------------ | ------------------------ | --------------------------------------------------------------------------------------------------- |
| `String`                 | Descripción              | Obtiene o establece la descripción de la jerarquía.                                 |
| `String`                 | DisplayFolder            | Obtiene o establece DisplayFolder de la jerarquía.                                  |
| `IndexadorDePerspectiva` | EnPerspectiva            |                                                                                                     |
| `Boolean`                | IsHidden                 | Obtiene o establece IsHidden de la jerarquía.                                       |
| `LevelCollection`        | Levels                   |                                                                                                     |
| `Hierarchy`              | MetadataObject           |                                                                                                     |
| `Boolean`                | Reordering               | Establézcalo en true cuando se vayan a reordenar varios niveles en una sola acción. |
| `ObjectState`            | State                    | Obtiene o establece el estado de la jerarquía.                                      |
| `Table`                  | Tabla                    |                                                                                                     |
| `TranslationIndexer`     | TranslatedDescriptions   | Colección de descripciones localizadas para esta jerarquía.                         |
| `TranslationIndexer`     | TranslatedDisplayFolders | Colección de carpetas de visualización localizadas para esta jerarquía.             |

Métodos

| Tipo                               | Nombre                                                                                            | Resumen |
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

Clase de colección de `Level`. Proporciona propiedades prácticas para establecer una propiedad en varios objetos a la vez.

```csharp
public class TabularEditor.TOMWrapper.HierarchyCollection
    : TabularObjectCollection<Hierarchy, Hierarchy, Table>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Hierarchy>, IEnumerable<Hierarchy>, IList<Hierarchy>, ITabularObjectCollection, IExpandableIndexer

```

Propiedades

| Tipo      | Nombre         | Resumen |
| --------- | -------------- | ------- |
| `String`  | Description    |         |
| `String`  | DisplayFolder  |         |
| `Boolean` | IsHidden       |         |
| `Table`   | Elemento padre |         |

Métodos

| Tipo     | Nombre                        | Resumen |
| -------- | ----------------------------- | ------- |
| `String` | ToString() |         |

## `HierarchyColumnConverter`

```csharp
public class TabularEditor.TOMWrapper.HierarchyColumnConverter
    : TableColumnConverter

```

Métodos

| Tipo      | Nombre                                                                          | Resumen |
| --------- | ------------------------------------------------------------------------------- | ------- |
| `Boolean` | GetStandardValuesExclusive(`ITypeDescriptorContext` context) |         |
| `Boolean` | IsValid(`ITypeDescriptorContext` context, `Object` value)    |         |

## `IAnnotationObject`

```csharp
public interface TabularEditor.TOMWrapper.IAnnotationObject
    : ITabularObject, INotifyPropertyChanged

```

Métodos

| Tipo     | Nombre                                                                                     | Resumen |
| -------- | ------------------------------------------------------------------------------------------ | ------- |
| `String` | GetAnnotation(`String` name)                                            |         |
| `void`   | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |         |

## `IClonableObject`

```csharp
public interface TabularEditor.TOMWrapper.IClonableObject

```

Métodos

| Tipo                 | Nombre                                                                    | Resumen |
| -------------------- | ------------------------------------------------------------------------- | ------- |
| `TabularNamedObject` | Clone(`String` newName, `Boolean` includeTranslations) |         |

## `IDaxObject`

```csharp
public interface TabularEditor.TOMWrapper.IDaxObject
    : ITabularNamedObject, ITabularObject, INotifyPropertyChanged

```

Propiedades

| Tipo                         | Nombre            | Resumen |
| ---------------------------- | ----------------- | ------- |
| `String`                     | DaxObjectFullName |         |
| `String`                     | DaxObjectName     |         |
| `String`                     | DaxTableName      |         |
| `HashSet<IExpressionObject>` | Dependientes      |         |

## `IDescriptionObject`

Objetos que pueden tener descripciones

```csharp
public interface TabularEditor.TOMWrapper.IDescriptionObject

```

Propiedades

| Tipo                 | Nombre                 | Resumen |
| -------------------- | ---------------------- | ------- |
| `String`             | Descripción            |         |
| `TranslationIndexer` | TranslatedDescriptions |         |

## `IDetailObject`

Representa un objeto que puede estar dentro de una carpeta de visualización. Ejemplos:  - medidas  - Columnas  - Jerarquías  - Carpetas

```csharp
public interface TabularEditor.TOMWrapper.IDetailObject
    : ITabularTableObject, ITabularNamedObject, ITabularObject, INotifyPropertyChanged

```

Propiedades

| Tipo                 | Nombre                   | Resumen |
| -------------------- | ------------------------ | ------- |
| `String`             | DisplayFolder            |         |
| `TranslationIndexer` | TranslatedDisplayFolders |         |

## `IDetailObjectContainer`

Representa un objeto que puede contener otros objetos, además de carpetas de visualización. Ejemplos:  - Carpetas  - Tabla

```csharp
public interface TabularEditor.TOMWrapper.IDetailObjectContainer
    : ITabularNamedObject, ITabularObject, INotifyPropertyChanged

```

Propiedades

| Tipo    | Nombre      | Resumen |
| ------- | ----------- | ------- |
| `Table` | ParentTable |         |

Métodos

| Tipo                         | Nombre                                                               | Resumen |
| ---------------------------- | -------------------------------------------------------------------- | ------- |
| `IEnumerable<IDetailObject>` | GetChildrenByFolders(`Boolean` recursive = False) |         |

## `IErrorMessageObject`

Objetos que pueden contener mensajes de error

```csharp
public interface TabularEditor.TOMWrapper.IErrorMessageObject

```

Propiedades

| Tipo     | Nombre       | Resumen |
| -------- | ------------ | ------- |
| `String` | ErrorMessage |         |

## `IExpressionObject`

```csharp
public interface TabularEditor.TOMWrapper.IExpressionObject
    : IDaxObject, ITabularNamedObject, ITabularObject, INotifyPropertyChanged

```

Propiedades

| Tipo                                       | Nombre          | Resumen |
| ------------------------------------------ | --------------- | ------- |
| `Dictionary<IDaxObject, List<Dependency>>` | Dependencias    |         |
| `String`                                   | Expresión       |         |
| `Boolean`                                  | NeedsValidation |         |

## `IHideableObject`

Objetos que se pueden mostrar u ocultar

```csharp
public interface TabularEditor.TOMWrapper.IHideableObject

```

Propiedades

| Tipo      | Nombre   | Resumen |
| --------- | -------- | ------- |
| `Boolean` | IsHidden |         |

## `IntelliSenseAttribute`

```csharp
public class TabularEditor.TOMWrapper.IntelliSenseAttribute
    : Attribute, _Attribute

```

Propiedades

| Tipo     | Nombre      | Resumen |
| -------- | ----------- | ------- |
| `String` | Descripción |         |

## `ITabularNamedObject`

```csharp
public interface TabularEditor.TOMWrapper.ITabularNamedObject
    : ITabularObject, INotifyPropertyChanged

```

Propiedades

| Tipo                 | Nombre          | Resumen |
| -------------------- | --------------- | ------- |
| `Int32`              | MetadataIndex   |         |
| `String`             | Name            |         |
| `TranslationIndexer` | TranslatedNames |         |

## `ITabularObject`

```csharp
public interface TabularEditor.TOMWrapper.ITabularObject
    : INotifyPropertyChanged

```

Propiedades

| Tipo         | Nombre     | Resumen |
| ------------ | ---------- | ------- |
| `Model`      | Model      |         |
| `ObjectType` | ObjectType |         |

## `ITabularObjectCollection`

```csharp
public interface TabularEditor.TOMWrapper.ITabularObjectCollection
    : IEnumerable

```

Propiedades

| Tipo                  | Nombre         | Resumen |
| --------------------- | -------------- | ------- |
| `String`              | CollectionName |         |
| `TabularModelHandler` | Handler        |         |
| `IEnumerable<String>` | Keys           |         |

Métodos

| Tipo                       | Nombre                                               | Resumen |
| -------------------------- | ---------------------------------------------------- | ------- |
| `void`                     | Add(`TabularNamedObject` obj)     |         |
| `void`                     | Clear()                           |         |
| `Boolean`                  | Contains(`Object` value)          |         |
| `Boolean`                  | Contains(`String` key)            |         |
| `ITabularObjectCollection` | GetCurrentCollection()            |         |
| `Int32`                    | IndexOf(`TabularNamedObject` obj) |         |
| `void`                     | Remove(`TabularNamedObject` obj)  |         |

## `ITabularObjectContainer`

Los `TabularObjects` que pueden contener otros objetos deben usar esta interfaz.

```csharp
public interface TabularEditor.TOMWrapper.ITabularObjectContainer

```

Métodos

| Tipo                               | Nombre                           | Resumen |
| ---------------------------------- | -------------------------------- | ------- |
| `IEnumerable<ITabularNamedObject>` | GetChildren() |         |

## `ITabularPerspectiveObject`

Objetos que pueden mostrarse u ocultarse en perspectivas individuales

```csharp
public interface TabularEditor.TOMWrapper.ITabularPerspectiveObject
    : IHideableObject

```

Propiedades

| Tipo                 | Nombre        | Resumen |
| -------------------- | ------------- | ------- |
| `PerspectiveIndexer` | InPerspective |         |

## `ITabularTableObject`

Objeto que pertenece a una tabla específica.

```csharp
public interface TabularEditor.TOMWrapper.ITabularTableObject
    : ITabularNamedObject, ITabularObject, INotifyPropertyChanged

```

Propiedades

| Tipo    | Nombre | Resumen |
| ------- | ------ | ------- |
| `Table` | Tabla  |         |

Métodos

| Tipo   | Nombre                      | Resumen |
| ------ | --------------------------- | ------- |
| `void` | Delete() |         |

## `KPI`

Declaración de la clase base para KPI

```csharp
public class TabularEditor.TOMWrapper.KPI
    : TabularObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, IDescriptionObject, IAnnotationObject, IDynamicPropertyObject

```

Propiedades

| Tipo                 | Nombre                 | Resumen                                                                     |
| -------------------- | ---------------------- | --------------------------------------------------------------------------- |
| `String`             | Descripción            | Obtiene o establece la descripción del KPI.                 |
| `medida`             | Medida                 | Obtiene o establece la medida del KPI.                      |
| `KPI`                | MetadataObject         |                                                                             |
| `String`             | StatusDescription      | Obtiene o establece el valor de StatusDescription del KPI.  |
| `String`             | StatusExpression       | Obtiene o establece el valor de StatusExpression del KPI.   |
| `String`             | StatusGraphic          | Obtiene o establece el valor de StatusGraphic del KPI.      |
| `String`             | TargetDescription      | Obtiene o establece el valor de TargetDescription del KPI.  |
| `String`             | TargetExpression       | Obtiene o establece el valor de TargetExpression del KPI.   |
| `String`             | TargetFormatString     | Obtiene o establece el valor de TargetFormatString del KPI. |
| `TranslationIndexer` | TranslatedDescriptions | Colección de descripciones localizadas para este KPI.       |
| `String`             | TrendDescription       | Obtiene o establece el valor de TrendDescription del KPI.   |
| `String`             | TrendExpression        | Obtiene o establece la propiedad TrendExpression del KPI.   |
| `String`             | TrendGraphic           | Obtiene o establece la propiedad TrendGraphic del KPI.      |

Métodos

| Tipo      | Nombre                                                                                     | Resumen |
| --------- | ------------------------------------------------------------------------------------------ | ------- |
| `Boolean` | Browsable(`String` propertyName)                                        |         |
| `Boolean` | Editable(`String` propertyName)                                         |         |
| `String`  | GetAnnotation(`String` name)                                            |         |
| `void`    | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |         |

## `Level`

Declaración de la clase base para Level

```csharp
public class TabularEditor.TOMWrapper.Level
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject, ITabularTableObject

```

Propiedades

| Tipo                 | Nombre                 | Resumen                                                               |
| -------------------- | ---------------------- | --------------------------------------------------------------------- |
| `Column`             | Columna                | Obtiene o establece la columna del nivel.             |
| `String`             | Descripción            | Obtiene o establece la descripción del nivel.         |
| `Hierarchy`          | Jerarquía              | Obtiene o establece la jerarquía del nivel.           |
| `Level`              | MetadataObject         |                                                                       |
| `Int32`              | Ordinal                | Obtiene o establece el ordinal del nivel.             |
| `Table`              | Tabla                  |                                                                       |
| `TranslationIndexer` | TranslatedDescriptions | Colección de descripciones localizadas de este nivel. |

Métodos

| Tipo     | Nombre                                                                                                                  | Resumen                                           |
| -------- | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| `void`   | Delete()                                                                                             | Elimina el nivel de la jerarquía. |
| `String` | GetAnnotation(`String` name)                                                                         |                                                   |
| `void`   | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue)                       |                                                   |
| `void`   | OnPropertyChanging(`String` propertyName, `Object` newValue, `Boolean&` undoable, `Boolean&` cancel) |                                                   |
| `void`   | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True)                              |                                                   |
| `void`   | Undelete(`ITabularObjectCollection` collection)                                                      |                                                   |

## `LevelCollection`

Clase de colección para la medida. Proporciona propiedades útiles para establecer una misma propiedad en varios objetos a la vez.

```csharp
public class TabularEditor.TOMWrapper.LevelCollection
    : TabularObjectCollection<Level, Level, Hierarchy>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Level>, IEnumerable<Level>, IList<Level>, ITabularObjectCollection, IExpandableIndexer

```

Propiedades

| Tipo        | Nombre      | Resumen |
| ----------- | ----------- | ------- |
| `String`    | Descripción |         |
| `Hierarchy` | Padre       |         |

Métodos

| Tipo      | Nombre                                  | Resumen |
| --------- | --------------------------------------- | ------- |
| `void`    | Add(`Level` item)    |         |
| `Boolean` | Remove(`Level` item) |         |
| `String`  | ToString()           |         |

## `LogicalGroup`

```csharp
public class TabularEditor.TOMWrapper.LogicalGroup
    : ITabularNamedObject, ITabularObject, INotifyPropertyChanged, ITabularObjectContainer

```

Propiedades

| Tipo                 | Nombre          | Resumen |
| -------------------- | --------------- | ------- |
| `Int32`              | MetadataIndex   |         |
| `Model`              | Model           |         |
| `String`             | Nombre          |         |
| `ObjectType`         | ObjectType      |         |
| `TranslationIndexer` | TranslatedNames |         |

Eventos

| Tipo                          | Nombre          | Resumen |
| ----------------------------- | --------------- | ------- |
| `PropertyChangedEventHandler` | PropertyChanged |         |

Métodos

| Tipo                               | Nombre                           | Resumen |
| ---------------------------------- | -------------------------------- | ------- |
| `IEnumerable<ITabularNamedObject>` | GetChildren() |         |

## `LogicalTreeOptions`

```csharp
public enum TabularEditor.TOMWrapper.LogicalTreeOptions
    : Enum, IComparable, IFormattable, IConvertible

```

Enum

| Valor | Nombre                    | Resumen |
| ----- | ------------------------- | ------- |
| `1`   | DisplayFolders            |         |
| `2`   | Columns                   |         |
| `4`   | Medidas                   |         |
| `8`   | KPI                       |         |
| `16`  | Jerarquías                |         |
| `32`  | Niveles                   |         |
| `64`  | Mostrar elementos ocultos |         |
| `128` | Todos los tipos de objeto |         |
| `256` | Mostrar la raíz           |         |
| `447` | Predeterminado            |         |

## `medida`

Declaración de la clase base de la medida

```csharp
public class TabularEditor.TOMWrapper.Measure
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDetailObject, ITabularTableObject, IHideableObject, IErrorMessageObject, IDescriptionObject, IExpressionObject, IDaxObject, IAnnotationObject, ITabularPerspectiveObject, IDynamicPropertyObject, IClonableObject

```

Propiedades

| Tipo                                       | Nombre                   | Resumen                                                                            |
| ------------------------------------------ | ------------------------ | ---------------------------------------------------------------------------------- |
| `DataType`                                 | DataType                 | Obtiene o establece el DataType de la medida.                      |
| `String`                                   | DaxObjectFullName        |                                                                                    |
| `String`                                   | DaxObjectName            |                                                                                    |
| `String`                                   | DaxTableName             |                                                                                    |
| `HashSet<IExpressionObject>`               | Dependientes             |                                                                                    |
| `Dictionary<IDaxObject, List<Dependency>>` | Dependencias             |                                                                                    |
| `String`                                   | Descripción              | Obtiene o establece la descripción de la medida.                   |
| `String`                                   | DisplayFolder            | Obtiene o establece la propiedad DisplayFolder de la medida.       |
| `String`                                   | ErrorMessage             | Obtiene o establece la propiedad ErrorMessage de la medida.        |
| `String`                                   | Expresión                | Obtiene o establece la expresión de la medida.                     |
| `String`                                   | FormatString             | Obtiene o establece la propiedad FormatString de la medida.        |
| `IndexadorDePerspectiva`                   | EnPerspectiva            |                                                                                    |
| `Boolean`                                  | IsHidden                 | Obtiene o establece la propiedad IsHidden de la medida.            |
| `Boolean`                                  | IsSimpleMeasure          | Obtiene o establece la propiedad IsSimpleMeasure de la medida.     |
| `KPI`                                      | KPI                      | Obtiene o establece el KPI de la medida.                           |
| `medida`                                   | MetadataObject           |                                                                                    |
| `Boolean`                                  | NeedsValidation          |                                                                                    |
| `ObjectState`                              | State                    | Obtiene o establece el estado de la medida.                        |
| `Table`                                    | Table                    |                                                                                    |
| `TranslationIndexer`                       | TranslatedDescriptions   | Colección de descripciones localizadas de esta medida.             |
| `TranslationIndexer`                       | TranslatedDisplayFolders | Colección de carpetas de visualización localizadas de esta medida. |

Métodos

| Tipo                 | Nombre                                                                                                                  | Resumen |
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

Clase de colección para `Table`. Ofrece propiedades prácticas para establecer una propiedad en varios objetos a la vez.

```csharp
public class TabularEditor.TOMWrapper.MeasureCollection
    : TabularObjectCollection<Measure, Measure, Table>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Measure>, IEnumerable<Measure>, IList<Measure>, ITabularObjectCollection, IExpandableIndexer

```

Propiedades

| Tipo      | Nombre          | Resumen |
| --------- | --------------- | ------- |
| `String`  | Descripción     |         |
| `String`  | DisplayFolder   |         |
| `String`  | Expression      |         |
| `String`  | FormatString    |         |
| `Boolean` | IsHidden        |         |
| `Boolean` | IsSimpleMeasure |         |
| `KPI`     | KPI             |         |
| `Table`   | Parent          |         |

Métodos

| Tipo     | Nombre                        | Resumen |
| -------- | ----------------------------- | ------- |
| `String` | ToString() |         |

## `Model`

Declaración de la clase base de la clase Model

```csharp
public class TabularEditor.TOMWrapper.Model
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject, ITabularObjectContainer

```

Campos

| Tipo           | Nombre            | Resumen |
| -------------- | ----------------- | ------- |
| `LogicalGroup` | GroupDataSources  |         |
| `LogicalGroup` | GroupPerspectivas |         |
| `LogicalGroup` | GroupRelaciones   |         |
| `LogicalGroup` | GroupRoles        |         |
| `LogicalGroup` | GroupTables       |         |
| `LogicalGroup` | GroupTranslations |         |

Propiedades

| Tipo                        | Nombre                     | Resumen                                                                      |
| --------------------------- | -------------------------- | ---------------------------------------------------------------------------- |
| `IEnumerable<Column>`       | AllColumns                 |                                                                              |
| `IEnumerable<Hierarchy>`    | AllHierarchies             |                                                                              |
| `IEnumerable<Level>`        | AllLevels                  |                                                                              |
| `IEnumerable<Measure>`      | AllMeasures                |                                                                              |
| `String`                    | Intercalación              | Obtiene o establece la intercalación del modelo.             |
| `String`                    | Configuración regional     | Obtiene o establece la configuración regional del modelo.    |
| `CultureCollection`         | Configuraciones regionales |                                                                              |
| `Database`                  | Base de datos              |                                                                              |
| `DataSourceCollection`      | Fuentes de datos           |                                                                              |
| `DataViewType`              | DefaultDataView            | Obtiene o establece el DefaultDataView del modelo.           |
| `ModeType`                  | DefaultMode                | Obtiene o establece la propiedad DefaultMode del modelo.     |
| `String`                    | Descripción                | Obtiene o establece la descripción del modelo.               |
| `Boolean`                   | HasLocalChanges            | Obtiene o establece la propiedad HasLocalChanges del modelo. |
| `IEnumerable<LogicalGroup>` | LogicalChildGroups         |                                                                              |
| `Model`                     | MetadataObject             |                                                                              |
| `PerspectiveCollection`     | Perspectivas               |                                                                              |
| `RelationshipCollection2`   | Relaciones                 |                                                                              |
| `ModelRoleCollection`       | Roles                      |                                                                              |
| `String`                    | StorageLocation            | Obtiene o establece la propiedad StorageLocation del modelo. |
| `TableCollection`           | Tablas                     |                                                                              |
| `TranslationIndexer`        | TranslatedDescriptions     | Colección de descripciones localizadas para este modelo.     |

Métodos

| Tipo                               | Nombre                                                                                     | Resumen |
| ---------------------------------- | ------------------------------------------------------------------------------------------ | ------- |
| `CalculatedTable`                  | AddCalculatedTable()                                                    |         |
| `perspectiva`                      | AddPerspective(`String` name = null) perspectiva                        |         |
| `RelaciónDeColumnaÚnica`           | AddRelationship() relación                                              |         |
| `RolDelModelo`                     | AddRole(`String` name = null) rol                                       |         |
| `Table`                            | AddTable()                                                              |         |
| `configuración regional`           | AddTranslation(`String` cultureId) configuración regional               |         |
| `String`                           | GetAnnotation(`String` name)                                            |         |
| `IEnumerable<ITabularNamedObject>` | GetChildren()                                                           |         |
| `void`                             | Init()                                                                  |         |
| `void`                             | LoadChildObjects()                                                      |         |
| `void`                             | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |         |

## `ModelRole`

Declaración de la clase base del rol del modelo

```csharp
public class TabularEditor.TOMWrapper.ModelRole
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject

```

Propiedades

| Tipo                 | Nombre                 | Resumen                                                                        |
| -------------------- | ---------------------- | ------------------------------------------------------------------------------ |
| `String`             | Descripción            | Obtiene o establece la descripción del rol del modelo.         |
| `ModelRole`          | MetadataObject         |                                                                                |
| `ModelPermission`    | ModelPermission        | Obtiene o establece el ModelPermission del rol del modelo.     |
| `RoleRLSIndexer`     | RowLevelSecurity       |                                                                                |
| `TranslationIndexer` | TranslatedDescriptions | Colección de descripciones localizadas de este rol del modelo. |

Métodos

| Tipo                 | Nombre                                                                                     | Resumen |
| -------------------- | ------------------------------------------------------------------------------------------ | ------- |
| `TabularNamedObject` | Clone(`String` newName, `Boolean` includeTranslations)                  |         |
| `void`               | Delete()                                                                |         |
| `String`             | GetAnnotation(`String` name)                                            |         |
| `void`               | InitRLSIndexer()                                                        |         |
| `void`               | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |         |
| `void`               | Undelete(`ITabularObjectCollection` collection)                         |         |

## `ModelRoleCollection`

Clase de colección para ModelRole. Proporciona propiedades prácticas para establecer una misma propiedad en varios objetos a la vez.

```csharp
public class TabularEditor.TOMWrapper.ModelRoleCollection
    : TabularObjectCollection<ModelRole, ModelRole, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<ModelRole>, IEnumerable<ModelRole>, IList<ModelRole>, ITabularObjectCollection, IExpandableIndexer

```

Propiedades

| Tipo              | Nombre          | Resumen |
| ----------------- | --------------- | ------- |
| `String`          | Descripción     |         |
| `ModelPermission` | ModelPermission |         |
| `Model`           | Padre           |         |

Métodos

| Tipo     | Nombre                        | Resumen |
| -------- | ----------------------------- | ------- |
| `String` | ToString() |         |

## `NullTree`

```csharp
public class TabularEditor.TOMWrapper.NullTree
    : TabularTree, INotifyPropertyChanged

```

Métodos

| Tipo   | Nombre                                                                                   | Resumen |
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

Enumeración

| Valor | Nombre     | Resumen |
| ----- | ---------- | ------- |
| `0`   | Alfabético |         |
| `1`   | Metadatos  |         |

## `ObjectType`

```csharp
public enum TabularEditor.TOMWrapper.ObjectType
    : Enum, IComparable, IFormattable, IConvertible

```

Enumeración

| Valor  | Nombre                   | Resumen |
| ------ | ------------------------ | ------- |
| `-2`   | Grupo                    |         |
| `-1`   | Carpeta                  |         |
| `1`    | Modelo                   |         |
| `2`    | Fuente de datos          |         |
| `3`    | Tabla                    |         |
| `4`    | Columna                  |         |
| `5`    | Jerarquía de atributos   |         |
| `6`    | Partición                |         |
| `7`    | Relación                 |         |
| `8`    | Medida                   |         |
| `9`    | Jerarquía                |         |
| `10`   | Nivel                    |         |
| `11`   | Anotación                |         |
| `12`   | KPI                      |         |
| `13`   | Configuración regional   |         |
| `14`   | Traducción de objetos    |         |
| `15`   | Metadatos lingüísticos   |         |
| `29`   | Perspectiva              |         |
| `30`   | Tabla de perspectiva     |         |
| `31`   | Columna de perspectiva   |         |
| `32`   | Jerarquía de perspectiva |         |
| `33`   | Medida de perspectiva    |         |
| `34`   | Rol                      |         |
| `35`   | Membresía del rol        |         |
| `36`   | Permiso de tabla         |         |
| `1000` | Base de datos            |         |

## `partición`

Declaración de la clase base de `partición`

```csharp
public class TabularEditor.TOMWrapper.Partition
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDynamicPropertyObject, IErrorMessageObject, ITabularTableObject, IDescriptionObject, IAnnotationObject

```

Propiedades

| Tipo                      | Nombre                 | Resumen                                                                          |
| ------------------------- | ---------------------- | -------------------------------------------------------------------------------- |
| `DataSource`              | DataSource             |                                                                                  |
| `DataViewType`            | DataView               | Obtiene o establece la propiedad `DataView` de la partición.     |
| `String`                  | Description            | Obtiene o establece la propiedad `Description` de la partición.  |
| `String`                  | ErrorMessage           | Obtiene o establece la propiedad `ErrorMessage` de la partición. |
| `String`                  | Expression             |                                                                                  |
| `partición`               | MetadataObject         |                                                                                  |
| `ModeType`                | Mode                   | Obtiene o establece la propiedad `Mode` de la partición.         |
| `String`                  | Name                   |                                                                                  |
| `String`                  | Query                  |                                                                                  |
| `DateTime`                | RefreshedTime          |                                                                                  |
| `String`                  | Source                 |                                                                                  |
| `TipoDeOrigenDePartición` | SourceType             | Obtiene o establece el SourceType de la partición.               |
| `ObjectState`             | State                  | Obtiene o establece el State de la partición.                    |
| `Table`                   | Table                  |                                                                                  |
| `TranslationIndexer`      | TranslatedDescriptions | Colección de descripciones localizadas para esta partición.      |

Métodos

| Tipo      | Nombre                                                                                     | Resumen |
| --------- | ------------------------------------------------------------------------------------------ | ------- |
| `Boolean` | Browsable(`String` propertyName)                                        |         |
| `Boolean` | Editable(`String` propertyName)                                         |         |
| `String`  | GetAnnotation(`String` name)                                            |         |
| `void`    | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |         |
| `void`    | Undelete(`ITabularObjectCollection` collection)                         |         |

## `Colección de particiones`

Clase de colección para la partición. Ofrece propiedades prácticas para establecer una misma propiedad en varios objetos a la vez.

```csharp
public class TabularEditor.TOMWrapper.PartitionCollection
    : TabularObjectCollection<Partition, Partition, Table>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Partition>, IEnumerable<Partition>, IList<Partition>, ITabularObjectCollection, IExpandableIndexer

```

Propiedades

| Tipo           | Nombre      | Resumen |
| -------------- | ----------- | ------- |
| `DataViewType` | DataView    |         |
| `String`       | Descripción |         |
| `ModeType`     | Modo        |         |
| `Table`        | Padre       |         |

Métodos

| Tipo     | Nombre                        | Resumen |
| -------- | ----------------------------- | ------- |
| `String` | ToString() |         |

## `perspectiva`

Declaración de la clase base de la perspectiva

```csharp
public class TabularEditor.TOMWrapper.Perspective
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject

```

Propiedades

| Tipo                 | Nombre                 | Resumen                                                                     |
| -------------------- | ---------------------- | --------------------------------------------------------------------------- |
| `String`             | Descripción            | Obtiene o establece la descripción de la perspectiva.       |
| `perspectiva`        | MetadataObject         |                                                                             |
| `TranslationIndexer` | TranslatedDescriptions | Colección de descripciones localizadas de esta perspectiva. |

Métodos

| Tipo                 | Nombre                                                                                     | Resumen |
| -------------------- | ------------------------------------------------------------------------------------------ | ------- |
| `TabularNamedObject` | Clone(`String` newName, `Boolean` includeTranslations)                  |         |
| `void`               | Delete()                                                                |         |
| `String`             | GetAnnotation(`String` name)                                            |         |
| `void`               | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |         |
| `void`               | Undelete(`ITabularObjectCollection` collection)                         |         |

## `PerspectiveCollection`

Clase de colección para la perspectiva. Ofrece propiedades prácticas para establecer una misma propiedad en varios objetos a la vez.

```csharp
public class TabularEditor.TOMWrapper.PerspectiveCollection
    : TabularObjectCollection<Perspective, Perspective, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Perspective>, IEnumerable<Perspective>, IList<Perspective>, ITabularObjectCollection, IExpandableIndexer

```

Propiedades

| Tipo     | Nombre      | Resumen |
| -------- | ----------- | ------- |
| `String` | Descripción |         |
| `Model`  | Padre       |         |

Métodos

| Tipo     | Nombre                        | Resumen |
| -------- | ----------------------------- | ------- |
| `String` | ToString() |         |

## `PerspectiveColumnIndexer`

```csharp
public class TabularEditor.TOMWrapper.PerspectiveColumnIndexer
    : PerspectiveIndexer, IEnumerable<Boolean>, IEnumerable, IExpandableIndexer

```

Propiedades

| Tipo     | Nombre  | Resumen |
| -------- | ------- | ------- |
| `Column` | Columna |         |

Métodos

| Tipo   | Nombre                                                                             | Resumen |
| ------ | ---------------------------------------------------------------------------------- | ------- |
| `void` | Refresh()                                                       |         |
| `void` | SetInPerspective(`perspectiva` perspectiva, `Boolean` included) |         |

## `PerspectiveHierarchyIndexer`

```csharp
public class TabularEditor.TOMWrapper.PerspectiveHierarchyIndexer
    : PerspectiveIndexer, IEnumerable<Boolean>, IEnumerable, IExpandableIndexer

```

Propiedades

| Tipo        | Nombre    | Resumen |
| ----------- | --------- | ------- |
| `Hierarchy` | Hierarchy |         |

Métodos

| Tipo   | Nombre                                                                             | Resumen |
| ------ | ---------------------------------------------------------------------------------- | ------- |
| `void` | Refresh()                                                       |         |
| `void` | SetInPerspective(`perspectiva` perspectiva, `Boolean` included) |         |

## `Indexador de perspectivas`

```csharp
public abstract class TabularEditor.TOMWrapper.PerspectiveIndexer
    : IEnumerable<Boolean>, IEnumerable, IExpandableIndexer

```

Campos

| Tipo                 | Nombre        | Resumen |
| -------------------- | ------------- | ------- |
| `TabularNamedObject` | TabularObject |         |

Propiedades

| Tipo                               | Nombre               | Resumen |
| ---------------------------------- | -------------------- | ------- |
| `Boolean`                          | Item                 |         |
| `Boolean`                          | Item                 |         |
| `IEnumerable<String>`              | Keys                 |         |
| `Dictionary<Perspective, Boolean>` | Mapa de perspectivas |         |
| `String`                           | Summary              |         |

Métodos

| Tipo                          | Nombre                                                                             | Resumen                                                      |
| ----------------------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| `void`                        | All()                                                           | Incluye el objeto en todas las perspectivas. |
| `Dictionary<String, Boolean>` | Copy()                                                          |                                                              |
| `void`                        | CopyFrom(`PerspectiveIndexer` source)                           |                                                              |
| `void`                        | CopyFrom(`IDictionary<String, Boolean>` source)                 |                                                              |
| `String`                      | GetDisplayName(`String` key)                                    |                                                              |
| `IEnumerator<Boolean>`        | GetEnumerator()                                                 |                                                              |
| `void`                        | None()                                                          |                                                              |
| `void`                        | Refresh()                                                       |                                                              |
| `void`                        | SetInPerspective(`Perspective` perspective, `Boolean` included) |                                                              |

## `PerspectiveMeasureIndexer`

```csharp
public class TabularEditor.TOMWrapper.PerspectiveMeasureIndexer
    : PerspectiveIndexer, IEnumerable<Boolean>, IEnumerable, IExpandableIndexer

```

Propiedades

| Tipo     | Nombre | Resumen |
| -------- | ------ | ------- |
| `medida` | Medida |         |

Métodos

| Tipo   | Nombre                                                                             | Resumen |
| ------ | ---------------------------------------------------------------------------------- | ------- |
| `void` | Refresh()                                                       |         |
| `void` | SetInPerspective(`perspectiva` perspectiva, `Boolean` included) |         |

## `PerspectiveTableIndexer`

```csharp
public class TabularEditor.TOMWrapper.PerspectiveTableIndexer
    : PerspectiveIndexer, IEnumerable<Boolean>, IEnumerable, IExpandableIndexer

```

Propiedades

| Tipo      | Nombre | Resumen |
| --------- | ------ | ------- |
| `Boolean` | Item   |         |
| `Table`   | Table  |         |

Métodos

| Tipo               | Nombre                                                                             | Resumen |
| ------------------ | ---------------------------------------------------------------------------------- | ------- |
| `PerspectiveTable` | EnsurePTExists(`Perspective` perspective)                       |         |
| `void`             | Refresh()                                                       |         |
| `void`             | SetInPerspective(`Perspective` perspective, `Boolean` included) |         |

## `ProviderDataSource`

Declaración de la clase base de ProviderDataSource

```csharp
public class TabularEditor.TOMWrapper.ProviderDataSource
    : DataSource, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IDescriptionObject, IAnnotationObject, IDynamicPropertyObject

```

Propiedades

| Tipo                  | Nombre            | Resumen                                                                                   |
| --------------------- | ----------------- | ----------------------------------------------------------------------------------------- |
| `String`              | Account           | Obtiene o establece la propiedad Account de ProviderDataSource.           |
| `String`              | ConnectionString  | Obtiene o establece la propiedad ConnectionString de ProviderDataSource.  |
| `ImpersonationMode`   | ImpersonationMode | Obtiene o establece la propiedad ImpersonationMode de ProviderDataSource. |
| `DatasourceIsolation` | Isolation         | Obtiene o establece la propiedad Isolation de ProviderDataSource.         |
| `Boolean`             | IsPowerBIMashup   |                                                                                           |
| `String`              | Location          |                                                                                           |
| `Int32`               | MaxConnections    | Obtiene o establece el valor de MaxConnections de ProviderDataSource.     |
| `ProviderDataSource`  | MetadataObject    |                                                                                           |
| `String`              | MQuery            |                                                                                           |
| `String`              | Name              |                                                                                           |
| `String`              | Password          | Obtiene o establece el valor de Password de ProviderDataSource.           |
| `String`              | Provider          | Obtiene o establece el valor de Provider de ProviderDataSource.           |
| `String`              | SourceID          |                                                                                           |
| `Int32`               | Timeout           | Obtiene o establece el valor de Timeout de ProviderDataSource.            |

Métodos

| Tipo      | Nombre                                              | Resumen |
| --------- | --------------------------------------------------- | ------- |
| `Boolean` | Browsable(`String` propertyName) |         |
| `Boolean` | Editable(`String` propertyName)  |         |
| `void`    | Init()                           |         |

## `relación`

Declaración de la clase base de la relación

```csharp
public abstract class TabularEditor.TOMWrapper.Relationship
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IAnnotationObject

```

Propiedades

| Tipo                                     | Nombre                     | Resumen                                                                                    |
| ---------------------------------------- | -------------------------- | ------------------------------------------------------------------------------------------ |
| `CrossFilteringBehavior`                 | CrossFilteringBehavior     | Obtiene o establece el CrossFilteringBehavior de la relación.              |
| `Table`                                  | FromTable                  | Obtiene o establece el FromTable de la relación.                           |
| `Boolean`                                | IsActive                   | Obtiene o establece el IsActive de la relación.                            |
| `Comportamiento de relación de DateTime` | JoinOnDateBehavior         | Obtiene o establece el valor de JoinOnDateBehavior de la relación.         |
| `relación`                               | MetadataObject             |                                                                                            |
| `Boolean`                                | RelyOnReferentialIntegrity | Obtiene o establece el valor de RelyOnReferentialIntegrity de la relación. |
| `SecurityFilteringBehavior`              | SecurityFilteringBehavior  | Obtiene o establece el valor de SecurityFilteringBehavior de la relación.  |
| `ObjectState`                            | State                      | Obtiene o establece el valor de State de la relación.                      |
| `Table`                                  | ToTable                    | Obtiene o establece el valor de ToTable de la relación.                    |
| `Tipo de relación`                       | Type                       | Obtiene o establece el valor de Type de la relación.                       |

Métodos

| Tipo     | Nombre                                                                                     | Resumen |
| -------- | ------------------------------------------------------------------------------------------ | ------- |
| `String` | GetAnnotation(`String` name)                                            |         |
| `void`   | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True) |         |

## `RelationshipCollection`

Clase de colección para la relación. Ofrece propiedades prácticas para establecer una misma propiedad en varios objetos a la vez.

```csharp
public class TabularEditor.TOMWrapper.RelationshipCollection
    : TabularObjectCollection<Relationship, Relationship, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Relationship>, IEnumerable<Relationship>, IList<Relationship>, ITabularObjectCollection, IExpandableIndexer

```

Propiedades

| Tipo                           | Nombre                     | Resumen |
| ------------------------------ | -------------------------- | ------- |
| `CrossFilteringBehavior`       | CrossFilteringBehavior     |         |
| `Boolean`                      | IsActive                   |         |
| `DateTimeRelationshipBehavior` | JoinOnDateBehavior         |         |
| `Model`                        | Parent                     |         |
| `Boolean`                      | RelyOnReferentialIntegrity |         |
| `SecurityFilteringBehavior`    | SecurityFilteringBehavior  |         |

Métodos

| Tipo     | Nombre                        | Resumen |
| -------- | ----------------------------- | ------- |
| `String` | ToString() |         |

## `RelationshipCollection2`

```csharp
public class TabularEditor.TOMWrapper.RelationshipCollection2
    : TabularObjectCollection<SingleColumnRelationship, Relationship, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<SingleColumnRelationship>, IEnumerable<SingleColumnRelationship>, IList<SingleColumnRelationship>, ITabularObjectCollection, IExpandableIndexer

```

Propiedades

| Tipo                           | Nombre                     | Resumen |
| ------------------------------ | -------------------------- | ------- |
| `CrossFilteringBehavior`       | CrossFilteringBehavior     |         |
| `Boolean`                      | IsActive                   |         |
| `DateTimeRelationshipBehavior` | JoinOnDateBehavior         |         |
| `Model`                        | Parent                     |         |
| `Boolean`                      | RelyOnReferentialIntegrity |         |
| `SecurityFilteringBehavior`    | SecurityFilteringBehavior  |         |

Métodos

| Tipo     | Nombre                        | Resumen |
| -------- | ----------------------------- | ------- |
| `String` | ToString() |         |

## `RoleRLSIndexer`

El RoleRLSIndexer se utiliza para explorar todos los filtros de todas las tablas del modelo, para un rol específico. Esto contrasta con el TableRLSIndexer, que explora los filtros de todos los roles del modelo, para una tabla específica.

```csharp
public class TabularEditor.TOMWrapper.RoleRLSIndexer
    : IEnumerable<String>, IEnumerable, IExpandableIndexer

```

Campos

| Tipo        | Nombre | Resumen |
| ----------- | ------ | ------- |
| `ModelRole` | Rol    |         |

Propiedades

| Tipo                        | Nombre   | Resumen |
| --------------------------- | -------- | ------- |
| `String`                    | Elemento |         |
| `String`                    | Elemento |         |
| `IEnumerable<String>`       | Claves   |         |
| `Dictionary<Table, String>` | RLSMap   |         |
| `String`                    | Resumen  |         |

Métodos

| Tipo                  | Nombre                                                              | Resumen |
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

Campos

| Tipo              | Nombre                   | Resumen |
| ----------------- | ------------------------ | ------- |
| `Boolean`         | IgnoreInferredObjects    |         |
| `Boolean`         | IgnoreInferredProperties |         |
| `Boolean`         | IgnoreTimestamps         |         |
| `HashSet<String>` | Levels                   |         |
| `Boolean`         | PrefixFilenames          |         |
| `Boolean`         | SplitMultilineStrings    |         |

Propiedades estáticas

| Tipo               | Nombre         | Resumen |
| ------------------ | -------------- | ------- |
| `SerializeOptions` | Predeterminado |         |

## `SingleColumnRelationship`

Declaración de la clase base para `SingleColumnRelationship`

```csharp
public class TabularEditor.TOMWrapper.SingleColumnRelationship
    : Relationship, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IAnnotationObject, IDynamicPropertyObject

```

Propiedades

| Tipo                         | Nombre          | Resumen                                                                                                   |
| ---------------------------- | --------------- | --------------------------------------------------------------------------------------------------------- |
| `RelationshipEndCardinality` | FromCardinality | Obtiene o establece la propiedad FromCardinality de la relación SingleColumnRelationship. |
| `Column`                     | FromColumn      | Obtiene o establece la propiedad FromColumn de la relación SingleColumnRelationship.      |
| `SingleColumnRelationship`   | MetadataObject  |                                                                                                           |
| `String`                     | Nombre          |                                                                                                           |
| `RelationshipEndCardinality` | ToCardinality   | Obtiene o establece la propiedad ToCardinality de la relación SingleColumnRelationship.   |
| `Column`                     | ToColumn        | Obtiene o establece la propiedad ToColumn de la relación SingleColumnRelationship.        |

Métodos

| Tipo      | Nombre                                                                                                                  | Resumen |
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

Declaración de la clase base para `Table`

```csharp
public class TabularEditor.TOMWrapper.Table
    : TabularNamedObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable, IHideableObject, IDescriptionObject, IAnnotationObject, ITabularObjectContainer, IDetailObjectContainer, ITabularPerspectiveObject, IDaxObject, IDynamicPropertyObject, IErrorMessageObject

```

Propiedades

| Tipo                         | Nombre                 | Resumen                                                                            |
| ---------------------------- | ---------------------- | ---------------------------------------------------------------------------------- |
| `IEnumerable<Level>`         | AllLevels              |                                                                                    |
| `ColumnCollection`           | Columns                |                                                                                    |
| `String`                     | DataCategory           | Obtiene o establece la propiedad DataCategory de la clase `Table`. |
| `String`                     | DaxObjectFullName      |                                                                                    |
| `String`                     | DaxObjectName          |                                                                                    |
| `String`                     | DaxTableName           |                                                                                    |
| `HashSet<IExpressionObject>` | Dependants             |                                                                                    |
| `String`                     | Description            | Obtiene o establece la propiedad Description de la tabla.          |
| `String`                     | ErrorMessage           |                                                                                    |
| `HierarchyCollection`        | Hierarchies            |                                                                                    |
| `IndexadorDePerspectiva`     | EnPerspectiva          |                                                                                    |
| `Boolean`                    | IsHidden               | Obtiene o establece la propiedad IsHidden de la tabla.             |
| `ColecciónDeMedidas`         | Medidas                |                                                                                    |
| `Table`                      | MetadataObject         |                                                                                    |
| `String`                     | Name                   |                                                                                    |
| `Table`                      | ParentTable            |                                                                                    |
| `ColecciónDeParticiones`     | Particiones            |                                                                                    |
| `TableRLSIndexer`            | RowLevelSecurity       |                                                                                    |
| `String`                     | Origen                 |                                                                                    |
| `TipoDeOrigenDePartición`    | SourceType             |                                                                                    |
| `TranslationIndexer`         | TranslatedDescriptions | Colección de descripciones localizadas para esta tabla.            |

Métodos

| Tipo                               | Nombre                                                                                                                    | Resumen                                                                          |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `CalculatedColumn`                 | AddCalculatedColumn(`String` name = null, `String` expression = null, `String` displayFolder = null)   |                                                                                  |
| `DataColumn`                       | AddDataColumn(`String` name = null, `String` sourceColumn = null, `String` displayFolder = null)       |                                                                                  |
| `Hierarchy`                        | AddHierarchy(`String` name = null, `String` displayFolder = null, `Column[]` levels)                   |                                                                                  |
| `Hierarchy`                        | AddHierarchy(`String` name, `String` displayFolder = null, `String[]` levels)                          |                                                                                  |
| `medida`                           | AddMeasure(`String` name = null, `String` expression = null, `String` displayFolder = null)            |                                                                                  |
| `Boolean`                          | Browsable(`String` propertyName)                                                                       |                                                                                  |
| `void`                             | CheckChildrenErrors()                                                                                  |                                                                                  |
| `void`                             | Children_CollectionChanged(`Object` sender, `NotifyCollectionChangedEventArgs` e) |                                                                                  |
| `TabularNamedObject`               | Clone(`String` newName = null, `Boolean` includeTranslations = False)                                  |                                                                                  |
| `void`                             | Delete()                                                                                               |                                                                                  |
| `Boolean`                          | Editable(`String` propertyName)                                                                        |                                                                                  |
| `String`                           | GetAnnotation(`String` name)                                                                           |                                                                                  |
| `IEnumerable<ITabularNamedObject>` | GetChildren()                                                                                          | Devuelve todas las columnas, medidas y jerarquías de esta tabla. |
| `IEnumerable<IDetailObject>`       | GetChildrenByFolders(`Boolean` recursive)                                                              |                                                                                  |
| `void`                             | Init()                                                                                                 |                                                                                  |
| `void`                             | InitRLSIndexer()                                                                                       |                                                                                  |
| `void`                             | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue)                         |                                                                                  |
| `void`                             | OnPropertyChanging(`String` propertyName, `Object` newValue, `Boolean&` undoable, `Boolean&` cancel)   |                                                                                  |
| `void`                             | SetAnnotation(`String` name, `String` value, `Boolean` undoable = True)                                |                                                                                  |
| `void`                             | Undelete(`ITabularObjectCollection` collection)                                                        |                                                                                  |

Campos estáticos

| Tipo     | Nombre                | Resumen |
| -------- | --------------------- | ------- |
| `Char[]` | InvalidTableNameChars |         |

## `TableCollection`

Clase de colección para configuraciones regionales. Proporciona propiedades prácticas para establecer una propiedad en varios objetos a la vez.

```csharp
public class TabularEditor.TOMWrapper.TableCollection
    : TabularObjectCollection<Table, Table, Model>, IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<Table>, IEnumerable<Table>, IList<Table>, ITabularObjectCollection, IExpandableIndexer

```

Propiedades

| Tipo      | Nombre       | Resumen |
| --------- | ------------ | ------- |
| `String`  | DataCategory |         |
| `String`  | Descripción  |         |
| `Boolean` | IsHidden     |         |
| `Model`   | Parent       |         |

Métodos

| Tipo     | Nombre                        | Resumen |
| -------- | ----------------------------- | ------- |
| `String` | ToString() |         |

## `TableExtension`

```csharp
public static class TabularEditor.TOMWrapper.TableExtension

```

Métodos estáticos

| Tipo                  | Nombre                                               | Resumen |
| --------------------- | ---------------------------------------------------- | ------- |
| `PartitionSourceType` | GetSourceType(this `Table` table) |         |

## `TableRLSIndexer`

El TableRLSIndexer se utiliza para recorrer todos los filtros definidos en una tabla concreta, en todos los roles del modelo. A diferencia del RoleRLSIndexer, que recorre los filtros de todas las tablas para un rol concreto.

```csharp
public class TabularEditor.TOMWrapper.TableRLSIndexer
    : IEnumerable<String>, IEnumerable, IExpandableIndexer

```

Campos

| Tipo    | Nombre | Resumen |
| ------- | ------ | ------- |
| `Table` | Tabla  |         |

Propiedades

| Tipo                            | Nombre   | Resumen |
| ------------------------------- | -------- | ------- |
| `String`                        | Elemento |         |
| `String`                        | Elemento |         |
| `IEnumerable<String>`           | Claves   |         |
| `Dictionary<ModelRole, String>` | RLSMap   |         |
| `String`                        | Resumen  |         |

Métodos

| Tipo                  | Nombre                                                                | Resumen |
| --------------------- | --------------------------------------------------------------------- | ------- |
| `void`                | Clear()                                            |         |
| `void`                | CopyFrom(`TableRLSIndexer` source)                 |         |
| `String`              | GetDisplayName(`String` key)                       |         |
| `IEnumerator<String>` | GetEnumerator()                                    |         |
| `void`                | Refresh()                                          |         |
| `void`                | SetRLS(`ModelRole` rol, `String` filterExpression) |         |

## `TabularCollectionHelper`

```csharp
public static class TabularEditor.TOMWrapper.TabularCollectionHelper

```

Métodos estáticos

| Tipo   | Nombre                                                                                                                  | Resumen |
| ------ | ----------------------------------------------------------------------------------------------------------------------- | ------- |
| `void` | InPerspective(this `IEnumerable<Table>` tables, `String` perspectiva, `Boolean` value)               |         |
| `void` | InPerspective(this `IEnumerable<Column>` columns, `String` perspectiva, `Boolean` value)             |         |
| `void` | InPerspective(this `IEnumerable<Hierarchy>` hierarchies, `String` perspectiva, `Boolean` value)      |         |
| `void` | InPerspective(this `IEnumerable<Measure>` medidas, `String` perspectiva, `Boolean` value)            |         |
| `void` | InPerspective(this `IEnumerable<Table>` tables, `Perspective` perspectiva, `Boolean` value)          |         |
| `void` | InPerspective(this `IEnumerable<Column>` columns, `perspectiva` perspectiva, `Boolean` value)        |         |
| `void` | InPerspective(this `IEnumerable<Hierarchy>` hierarchies, `perspectiva` perspectiva, `Boolean` value) |         |
| `void` | InPerspective(this `IEnumerable<Measure>` measures, `Perspective` perspective, `Boolean` value)      |         |
| `void` | SetDisplayFolder(this `IEnumerable<Measure>` measures, `String` displayFolder)                       |         |

## `TabularCommonActions`

Proporciona métodos prácticos para realizar acciones comunes en un modelo tabular, que a menudo implican modificar varios objetos a la vez.  Por ejemplo, estos métodos pueden usarse para realizar con facilidad operaciones de arrastrar y soltar en la interfaz de usuario, que cambian niveles de jerarquía, carpetas de visualización, etc.

```csharp
public class TabularEditor.TOMWrapper.TabularCommonActions

```

Propiedades

| Tipo                  | Nombre  | Resumen |
| --------------------- | ------- | ------- |
| `TabularModelHandler` | Handler |         |

Métodos

| Tipo     | Nombre                                                                                                                                         | Resumen |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ------- |
| `void`   | AddColumnsToHierarchy(`IEnumerable<Column>` columns, `Hierarchy` hierarchy, `Int32` firstOrdinal = -1)                      |         |
| `Level`  | AddColumnToHierarchy(`Column` column, `Hierarchy` hierarchy, `Int32` ordinal = -1)                                          |         |
| `void`   | MoveObjects(`IEnumerable<IDetailObject>` objects, `Table` newTable, `configuración regional` culture)                       |         |
| `String` | NewColumnName(`String` prefix, `Table` table)                                                                               |         |
| `String` | NewMeasureName(`String` prefix)                                                                                             |         |
| `void`   | ReorderLevels(`IEnumerable<Level>` levels, `Int32` firstOrdinal)                                                            |         |
| `void`   | SetContainer(`IEnumerable<IDetailObject>` objects, `IDetailObjectContainer` newContainer, `configuración regional` culture) |         |

## `TabularConnection`

```csharp
public static class TabularEditor.TOMWrapper.TabularConnection

```

Métodos estáticos

| Tipo     | Nombre                                                                                            | Resumen |
| -------- | ------------------------------------------------------------------------------------------------- | ------- |
| `String` | GetConnectionString(`String` serverName)                                       |         |
| `String` | GetConnectionString(`String` serverName, `String` userName, `String` password) |         |

## `TabularCultureHelper`

```csharp
public static class TabularEditor.TOMWrapper.TabularCultureHelper

```

Métodos estáticos

| Tipo      | Nombre                                                                                                                          | Resumen |
| --------- | ------------------------------------------------------------------------------------------------------------------------------- | ------- |
| `Boolean` | ImportTranslations(`String` culturesJson, `Model` Model, `Boolean` overwriteExisting, `Boolean` haltOnError) |         |

## `TabularDeployer`

```csharp
public class TabularEditor.TOMWrapper.TabularDeployer

```

Métodos estáticos

| Tipo               | Nombre                                                                                                                            | Resumen                                                                                                                                                                                                                                                                                                                                                        |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `void`             | Deploy(`Database` db, `String` targetConnectionString, `String` targetDatabaseName)                            | Despliega la base de datos especificada en el servidor de destino y en la base de datos con el ID especificado, utilizando las opciones indicadas.  Devuelve una lista de errores de DAX (si los hay) de los objetos de la base de datos, en caso de que la implementación se haya realizado correctamente. |
| `DeploymentResult` | Deploy(`Database` db, `String` targetConnectionString, `String` targetDatabaseID, `DeploymentOptions` options) | Despliega la base de datos especificada en el servidor de destino y en la base de datos con el ID especificado, utilizando las opciones indicadas.  Devuelve una lista de errores de DAX (si los hay) de los objetos de la base de datos, en caso de que la implementación se haya realizado correctamente. |
| `String`           | GetTMSL(`Database` db, `Server` server, `String` targetDatabaseID, `DeploymentOptions` options)                |                                                                                                                                                                                                                                                                                                                                                                |
| `void`             | SaveModelMetadataBackup(`String` connectionString, `String` targetDatabaseID, `String` backupFilePath)         |                                                                                                                                                                                                                                                                                                                                                                |
| `void`             | WriteZip(`String` fileName, `String` content)                                                                  |                                                                                                                                                                                                                                                                                                                                                                |

## `TabularModelHandler`

```csharp
public class TabularEditor.TOMWrapper.TabularModelHandler
    : IDisposable

```

Campos

| Tipo                                           | Nombre             | Resumen |
| ---------------------------------------------- | ------------------ | ------- |
| `Dictionary<String, ITabularObjectCollection>` | WrapperCollections |         |
| `Dictionary<MetadataObject, TabularObject>`    | WrapperLookup      |         |

Propiedades

| Tipo                                        | Nombre                   | Resumen                                                                                                                                                                                                                                                                                                                                                        |
| ------------------------------------------- | ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TabularCommonActions`                      | Actions                  |                                                                                                                                                                                                                                                                                                                                                                |
| `Boolean`                                   | AutoFixup                | Especifica si los cambios en los nombres de los objetos (tablas, columnas, medidas) deben provocar actualizaciones automáticas de las expresiones DAX para reflejar los nombres modificados. Cuando se establece en true, se analizan todas las expresiones del modelo para crear un árbol de dependencias. |
| `Database`                                  | Database                 |                                                                                                                                                                                                                                                                                                                                                                |
| `Boolean`                                   | DelayBuildDependencyTree |                                                                                                                                                                                                                                                                                                                                                                |
| `IList<Tuple<NamedMetadataObject, String>>` | Errors                   |                                                                                                                                                                                                                                                                                                                                                                |
| `Boolean`                                   | HasUnsavedChanges        |                                                                                                                                                                                                                                                                                                                                                                |
| `Boolean`                                   | IsConnected              |                                                                                                                                                                                                                                                                                                                                                                |
| `Model`                                     | Model                    |                                                                                                                                                                                                                                                                                                                                                                |
| `String`                                    | Status                   |                                                                                                                                                                                                                                                                                                                                                                |
| `TabularTree`                               | Tree                     |                                                                                                                                                                                                                                                                                                                                                                |
| `UndoManager`                               | UndoManager              |                                                                                                                                                                                                                                                                                                                                                                |
| `Int64`                                     | Version                  |                                                                                                                                                                                                                                                                                                                                                                |

Métodos

| Tipo                        | Nombre                                                                                                             | Resumen                                                                                                                                                                                                                                                                                                         |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `IDetailObject`             | Add(`AddObjectType` objectType, `IDetailObjectContainer` container)                             |                                                                                                                                                                                                                                                                                                                 |
| `void`                      | BeginUpdate(`String` undoName)                                                                  |                                                                                                                                                                                                                                                                                                                 |
| `void`                      | BuildDependencyTree(`IExpressionObject` expressionObj)                                          |                                                                                                                                                                                                                                                                                                                 |
| `void`                      | BuildDependencyTree()                                                                           |                                                                                                                                                                                                                                                                                                                 |
| `ConflictInfo`              | CheckConflicts()                                                                                |                                                                                                                                                                                                                                                                                                                 |
| `IList<TabularNamedObject>` | DeserializeObjects(`String` json)                                                               |                                                                                                                                                                                                                                                                                                                 |
| `void`                      | Dispose()                                                                                       |                                                                                                                                                                                                                                                                                                                 |
| `void`                      | DoFixup(`IDaxObject` obj, `String` newName)                                                     | Cambia todas las referencias al objeto "obj" para que reflejen "newName"                                                                                                                                                                                                                                        |
| `Int32`                     | EndUpdate(`Boolean` undoable = True, `Boolean` rollback = False)                                |                                                                                                                                                                                                                                                                                                                 |
| `Int32`                     | EndUpdateAll(`Boolean` rollback = False)                                                        |                                                                                                                                                                                                                                                                                                                 |
| `Model`                     | GetModel()                                                                                      |                                                                                                                                                                                                                                                                                                                 |
| `Boolean`                   | ImportTranslations(`String` culturesJson, `Boolean` overwriteExisting, `Boolean` ignoreInvalid) | Aplica una traducción a partir de una cadena JSON.                                                                                                                                                                                                                                              |
| `void`                      | SaveDB()                                                                                        | Guarda los cambios en la base de datos. Es responsabilidad del usuario comprobar si se han realizado cambios en la base de datos desde que se cargó en TOMWrapper. Puedes usar Handler.CheckConflicts() para este propósito. |
| `void`                      | SaveFile(`String` fileName, `SerializeOptions` options)                                         |                                                                                                                                                                                                                                                                                                                 |
| `void`                      | SaveToFolder(`String` path, `SerializeOptions` options)                                         |                                                                                                                                                                                                                                                                                                                 |
| `String`                    | ScriptCreateOrReplace()                                                                         | Genera un script de toda la base de datos                                                                                                                                                                                                                                                                       |
| `String`                    | ScriptCreateOrReplace(`TabularNamedObject` obj)                                                 | Genera un script de toda la base de datos                                                                                                                                                                                                                                                                       |
| `String`                    | ScriptTraducciones(`IEnumerable<Culture>` translations)                                         |                                                                                                                                                                                                                                                                                                                 |
| `String`                    | SerializeObjects(`IEnumerable<TabularNamedObject>` objects)                                     |                                                                                                                                                                                                                                                                                                                 |
| `void`                      | UpdateFolders(`Table` table)                                                                    |                                                                                                                                                                                                                                                                                                                 |
| `void`                      | UpdateLevels(`Hierarchy` hierarchy)                                                             |                                                                                                                                                                                                                                                                                                                 |
| `void`                      | UpdateObject(`ITabularObject` obj)                                                              |                                                                                                                                                                                                                                                                                                                 |
| `void`                      | UpdateTables()                                                                                  |                                                                                                                                                                                                                                                                                                                 |

Campos estáticos

| Tipo     | Nombre                                      | Resumen |
| -------- | ------------------------------------------- | ------- |
| `String` | PROP_ERRORS            |         |
| `String` | PROP_HASUNSAVEDCHANGES |         |
| `String` | PROP_ISCONNECTED       |         |
| `String` | PROP_STATUS            |         |

Propiedades estáticas

| Tipo                  | Nombre    | Resumen |
| --------------------- | --------- | ------- |
| `TabularModelHandler` | Singleton |         |

Métodos estáticos

| Tipo                                            | Nombre                                                       | Resumen |
| ----------------------------------------------- | ------------------------------------------------------------ | ------- |
| `List<Tuple<NamedMetadataObject, String>>`      | CheckErrors(`Database` database)          |         |
| `List<Tuple<NamedMetadataObject, ObjectState>>` | CheckProcessingState(`Database` database) |         |

## `TabularNamedObject`

Un TabularObject es una clase envoltorio de la clase Microsoft.AnalysisServices.Tabular.NamedMetadataObject.  Este envoltorio se utiliza para todos los objetos que deben ser visibles y editables en Tabular Editor.  La misma clase base se usa para todo tipo de objetos de un modelo tabular. Esta clase base proporciona un método para editar el nombre y la descripción (localizados).

```csharp
public abstract class TabularEditor.TOMWrapper.TabularNamedObject
    : TabularObject, ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging, ITabularNamedObject, IComparable

```

Propiedades

| Tipo                  | Nombre          | Resumen                                                          |
| --------------------- | --------------- | ---------------------------------------------------------------- |
| `Int32`               | MetadataIndex   |                                                                  |
| `NamedMetadataObject` | MetadataObject  |                                                                  |
| `String`              | Nombre          |                                                                  |
| `TranslationIndexer`  | TranslatedNames | Colección de nombres localizados de este objeto. |

Métodos

| Tipo                 | Nombre                                                                    | Resumen                                                                                                                                                                                                                                                                                                                                          |
| -------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `TabularNamedObject` | Clone(`String` newName, `Boolean` includeTranslations) |                                                                                                                                                                                                                                                                                                                                                  |
| `Int32`              | CompareTo(`Object` obj)                                |                                                                                                                                                                                                                                                                                                                                                  |
| `void`               | Delete()                                               |                                                                                                                                                                                                                                                                                                                                                  |
| `void`               | Init()                                                 |                                                                                                                                                                                                                                                                                                                                                  |
| `void`               | Undelete(`ITabularObjectCollection` collection)        | Se necesita un apaño algo chapucero para deshacer una operación de borrado.  Las clases derivadas deben asegurarse de actualizar cualquier objeto "propiedad" del objeto en cuestión. Por ejemplo, una medida debe asegurarse de actualizar el wrapper de su KPI (si lo hay). |

## `TabularObject`

```csharp
public abstract class TabularEditor.TOMWrapper.TabularObject
    : ITabularObject, INotifyPropertyChanged, INotifyPropertyChanging

```

Campos

| Tipo                       | Nombre     | Resumen |
| -------------------------- | ---------- | ------- |
| `ITabularObjectCollection` | Collection |         |
| `TabularModelHandler`      | Handler    |         |

Propiedades

| Tipo                    | Nombre                   | Resumen |
| ----------------------- | ------------------------ | ------- |
| `MetadataObject`        | MetadataObject           |         |
| `Model`                 | Model                    |         |
| `ObjectType`            | ObjectType               |         |
| `String`                | ObjectTypeName           |         |
| `IndexadorDeTraducción` | TranslatedDescriptions   |         |
| `IndexadorDeTraducción` | TranslatedDisplayFolders |         |

Eventos

| Tipo                           | Nombre           | Resumen |
| ------------------------------ | ---------------- | ------- |
| `PropertyChangedEventHandler`  | PropertyChanged  |         |
| `PropertyChangingEventHandler` | PropertyChanging |         |

Métodos

| Tipo      | Nombre                                                                                                                  | Resumen                                                                                                                                                                                                                                                                          |
| --------- | ----------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `void`    | Init()                                                                                               | Los miembros derivados deben sobrescribir este método para crear instancias de los objetos secundarios                                                                                                                                                                           |
| `void`    | OnPropertyChanged(`String` propertyName, `Object` oldValue, `Object` newValue)                       |                                                                                                                                                                                                                                                                                  |
| `void`    | OnPropertyChanging(`String` propertyName, `Object` newValue, `Boolean&` undoable, `Boolean&` cancel) | Se llama antes de cambiar una propiedad de un objeto. Las clases derivadas pueden controlar cómo se gestiona el cambio.  Lance ArgumentException dentro de este método para mostrar mensajes de error en la interfaz de usuario. |
| `Boolean` | SetField(`T&` field, `T` value, `String` propertyName = null)                                        |                                                                                                                                                                                                                                                                                  |

## `TabularObjectCollection<T, TT, TP>`

```csharp
public abstract class TabularEditor.TOMWrapper.TabularObjectCollection<T, TT, TP>
    : IList, ICollection, IEnumerable, INotifyCollectionChanged, ICollection<T>, IEnumerable<T>, IList<T>, ITabularObjectCollection, IExpandableIndexer

```

Propiedades

| Tipo                                    | Nombre                   | Resumen |
| --------------------------------------- | ------------------------ | ------- |
| `String`                                | CollectionName           |         |
| `Int32`                                 | Count                    |         |
| `TabularModelHandler`                   | Handler                  |         |
| `Boolean`                               | IsFixedSize              |         |
| `Boolean`                               | IsReadOnly               |         |
| `Boolean`                               | IsSynchronized           |         |
| `T`                                     | Elemento                 |         |
| `T`                                     | Elemento                 |         |
| `IEnumerable<String>`                   | Claves                   |         |
| `NamedMetadataObjectCollection<TT, TP>` | MetadataObjectCollection |         |
| `String`                                | Resumen                  |         |
| `Object`                                | SyncRoot                 |         |

Eventos

| Tipo                                  | Nombre            | Resumen |
| ------------------------------------- | ----------------- | ------- |
| `NotifyCollectionChangedEventHandler` | CollectionChanged |         |

Métodos

| Tipo                       | Nombre                                                     | Resumen |
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

Propiedades

| Tipo          | Nombre | Resumen |
| ------------- | ------ | ------- |
| `ObjectOrder` | Orden  |         |

Métodos

| Tipo    | Nombre                                                                       | Resumen |
| ------- | ---------------------------------------------------------------------------- | ------- |
| `Int32` | Compare(`Object` x, `Object` y)                           |         |
| `Int32` | Compare(`ITabularNamedObject` x, `ITabularNamedObject` y) |         |

## `TabularObjectHelper`

```csharp
public static class TabularEditor.TOMWrapper.TabularObjectHelper

```

Métodos estáticos

| Tipo      | Nombre                                                                                                         | Resumen |
| --------- | -------------------------------------------------------------------------------------------------------------- | ------- |
| `String`  | GetLinqPath(this `TabularNamedObject` obj)                                                  |         |
| `String`  | GetName(this `ITabularNamedObject` obj, `configuración regional` culture)                   |         |
| `String`  | GetObjectPath(this `MetadataObject` obj)                                                    |         |
| `String`  | GetObjectPath(this `TabularObject` obj)                                                     |         |
| `String`  | GetTypeName(this `ObjectType` objType, `Boolean` plural = False)                            |         |
| `String`  | GetTypeName(this `ITabularObject` obj, `Boolean` plural = False)                            |         |
| `Boolean` | SetName(this `ITabularNamedObject` obj, `String` newName, `configuración regional` culture) |         |
| `String`  | SplitCamelCase(this `String` str)                                                           |         |

## `TabularTree`

El TabularLogicalModel controla la relación entre TabularObjects para su visualización en el control TreeViewAdv. Cada TabularObject individual no sabe ni le importa cuál es su relación lógica con otros objetos (por ejemplo, a través de DisplayFolders en una configuración regional específica). Los TabularObjects solo se preocupan por sus relaciones físicas, que se heredan directamente del Tabular Object Model (es decir, una medida pertenece a una tabla, etc.).

```csharp
public abstract class TabularEditor.TOMWrapper.TabularTree
    : INotifyPropertyChanged

```

Campos

| Tipo                         | Nombre     | Resumen |
| ---------------------------- | ---------- | ------- |
| `Dictionary<String, Folder>` | FolderTree |         |

Propiedades

| Tipo                     | Nombre                 | Resumen |
| ------------------------ | ---------------------- | ------- |
| `configuración regional` | Configuración regional |         |
| `String`                 | Filtro                 |         |
| `TabularModelHandler`    | Manejador              |         |
| `Model`                  | Modelo                 |         |
| `LogicalTreeOptions`     | Opciones               |         |
| `perspectiva`            | Perspectiva            |         |
| `Int32`                  | UpdateLocks            |         |

Eventos

| Tipo                          | Nombre          | Resumen |
| ----------------------------- | --------------- | ------- |
| `PropertyChangedEventHandler` | PropertyChanged |         |

Métodos

| Tipo                   | Nombre                                                                                                                      | Resumen                                                                                                                                                                                                               |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `void`                 | BeginUpdate()                                                                                            |                                                                                                                                                                                                                       |
| `void`                 | EndUpdate()                                                                                              |                                                                                                                                                                                                                       |
| `IEnumerable`          | GetChildren(`ITabularObjectContainer` tabularObject)                                                     | Este método encapsula la lógica de cómo debe estructurarse la representación en árbol del modelo tabular                                                                                                              |
| `Func<String, String>` | GetFolderMutation(`Object` source, `Object` destination)                                                 |                                                                                                                                                                                                                       |
| `Func<String, String>` | GetFolderMutation(`String` oldPath, `String` newPath)                                                    |                                                                                                                                                                                                                       |
| `void`                 | ModifyDisplayFolder(`Table` table, `String` oldPath, `String` newPath, `configuración regional` culture) | Actualiza la propiedad DisplayFolder de todos los objetos tabulares dentro de una tabla. Los objetos que se encuentren en subcarpetas de la ruta actualizada también se actualizarán. |
| `void`                 | OnNodesChanged(`ITabularObject` nodeItem)                                                                |                                                                                                                                                                                                                       |
| `void`                 | OnNodesInserted(`ITabularObject` parent, `ITabularObject[]` children)                                    |                                                                                                                                                                                                                       |
| `void`                 | OnNodesInserted(`ITabularObject` parent, `IEnumerable<ITabularObject>` children)                         |                                                                                                                                                                                                                       |
| `void`                 | OnNodesRemoved(`ITabularObject` parent, `ITabularObject[]` children)                                     |                                                                                                                                                                                                                       |
| `void`                 | OnNodesRemoved(`ITabularObject` parent, `IEnumerable<ITabularObject>` children)                          |                                                                                                                                                                                                                       |
| `void`                 | OnStructureChanged(`ITabularNamedObject` obj = null)                                                     |                                                                                                                                                                                                                       |
| `void`                 | SetConfiguraciónRegional(`String` nombreConfiguraciónRegional)                                           |                                                                                                                                                                                                                       |
| `void`                 | SetPerspectiva(`String` nombrePerspectiva)                                                               |                                                                                                                                                                                                                       |
| `void`                 | UpdateFolder(`Folder` folder, `String` oldFullPath = null)                                               |                                                                                                                                                                                                                       |
| `Boolean`              | VisibleInTree(`ITabularNamedObject` tabularObject)                                                       |                                                                                                                                                                                                                       |

## `Indexador de traducción`

```csharp
// Indexador de traducción
public class TabularEditor.TOMWrapper.TranslationIndexer
    : IEnumerable<String>, IEnumerable, IExpandableIndexer

```

Propiedades

| Tipo                  | Nombre          | Resumen |
| --------------------- | --------------- | ------- |
| `String`              | DefaultValue    |         |
| `String`              | Item            |         |
| `String`              | Item            |         |
| `IEnumerable<String>` | Keys            |         |
| `String`              | Summary         |         |
| `Int32`               | TranslatedCount |         |

Métodos

| Tipo                         | Nombre                                                                                                | Resumen                                                                                                                                                                                                                                                                                                                                          |
| ---------------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `void`                       | Clear()                                                                            | Elimina todos los valores traducidos del objeto.                                                                                                                                                                                                                                                                                 |
| `Boolean`                    | Contains(`configuración regional` configuraciónRegional)                           |                                                                                                                                                                                                                                                                                                                                                  |
| `Dictionary<String, String>` | Copy()                                                                             |                                                                                                                                                                                                                                                                                                                                                  |
| `void`                       | CopyFrom(`TranslationIndexer` traducciones, `Func<String, String>` mutator = null) |                                                                                                                                                                                                                                                                                                                                                  |
| `void`                       | CopyFrom(`IDictionary<String, String>` source)                                     |                                                                                                                                                                                                                                                                                                                                                  |
| `String`                     | GetDisplayName(`String` key)                                                       |                                                                                                                                                                                                                                                                                                                                                  |
| `IEnumerator<String>`        | GetEnumerator()                                                                    |                                                                                                                                                                                                                                                                                                                                                  |
| `void`                       | Refresh()                                                                          |                                                                                                                                                                                                                                                                                                                                                  |
| `void`                       | Reset()                                                                            | Restablece las traducciones del objeto. Se eliminan las traducciones del título, haciendo que el objeto aparezca con el nombre base en todas las configuraciones regionales. Las traducciones de la carpeta de visualización y la descripción se establecen en el valor no traducido del objeto. |
| `void`                       | SetAll(`String` value)                                                             |                                                                                                                                                                                                                                                                                                                                                  |


