---
uid: how-to-tom-interfaces
title: Interfaces clave de TOM
author: Morten Lønskov
updated: 2026-04-10
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Interfaces clave de TOM

El wrapper de TOM define varias interfaces transversales que implementan distintos tipos de objetos. Use estas interfaces al escribir código genérico que opere sobre cualquier objeto con una capacidad concreta, como establecer descripciones, comprobar la visibilidad o leer anotaciones.

## Referencia rápida

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

## Referencia de interfaz

| Interfaz                                                                                                                     | Miembros clave                                                                                       | Implementado por                                                                                   |
| ---------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| (xref:TabularEditor.TOMWrapper.IDescriptionObject)        | `Description`                                                                                        | Tablas, columnas, medidas, jerarquías, particiones, relaciones, perspectivas, roles y Data sources |
| (xref:TabularEditor.TOMWrapper.IHideableObject)           | `IsHidden`, `IsVisible`                                                                              | Tablas, columnas, medidas, jerarquías y niveles                                                    |
| (xref:TabularEditor.TOMWrapper.ITabularPerspectiveObject) | Indexador `InPerspective` de perspectiva                                                             | Tablas, columnas, medidas y jerarquías                                                             |
| (xref:TabularEditor.TOMWrapper.ITranslatableObject)       | `TranslatedNames`, `TranslatedDescriptions`                                                          | Tablas, columnas, medidas, jerarquías y niveles                                                    |
| (xref:TabularEditor.TOMWrapper.IFolderObject)             | `DisplayFolder`, `TranslatedDisplayFolders`                                                          | Medidas, columnas y jerarquías                                                                     |
| (xref:TabularEditor.TOMWrapper.IAnnotationObject)         | `GetAnnotation()`, `SetAnnotation()`, `HasAnnotation()`, `RemoveAnnotation()`, `Annotations`         | Casi todos los objetos TOM                                                                         |
| (xref:TabularEditor.TOMWrapper.IExtendedPropertyObject)   | `GetExtendedProperty()`, `SetExtendedProperty()`, `ExtendedProperties`                               | Tablas, columnas, medidas, jerarquías, particiones                                                 |
| (xref:TabularEditor.TOMWrapper.IExpressionObject)         | `Expression` (TE2); `GetExpression()`, `SetExpression()` (TE3) | Medidas, columnas calculadas, elementos de cálculo, particiones, KPIs                              |
| (xref:TabularEditor.TOMWrapper.IDaxObject)                | `DaxObjectName`, `DaxObjectFullName`, `ReferencedBy`                                                 | Tablas, columnas, medidas                                                                          |
| (xref:TabularEditor.TOMWrapper.IDaxDependantObject)       | `DependsOn`                                                                                          | Medidas, columnas calculadas, elementos de cálculo, KPIs, tablas, particiones                      |

## Cuándo usar interfaces

Use interfaces cuando necesite escribir código genérico que se aplique a varios tipos de objetos. En lugar de comprobar cada tipo individualmente:

```csharp
// Without interfaces -- repetitive
foreach (var m in Selected.Measures)
    m.Description = "Reviewed";
foreach (var c in Selected.Columns)
    c.Description = "Reviewed";
foreach (var t in Selected.Tables)
    t.Description = "Reviewed";
```

Use `OfType<T>()` con una interfaz para procesar todos los tipos en una sola pasada:

```csharp
// With interfaces -- handles any object that has a Description
foreach (var obj in Selected.OfType<IDescriptionObject>())
    obj.Description = "Reviewed";
```

## Patrones habituales de interfaz

### Comprobar y establecer la visibilidad

```csharp
// Hide all selected objects that support hiding
Selected.OfType<IHideableObject>().ForEach(obj => obj.IsHidden = true);
```

### Establecer la carpeta de visualización en varios tipos

```csharp
// Move all selected folder-bearing objects to a display folder
Selected.OfType<IFolderObject>().ForEach(obj => obj.DisplayFolder = "Archive");
```

### Etiquetar objetos con anotaciones

```csharp
// Tag any annotatable object
Selected.OfType<IAnnotationObject>().ForEach(obj =>
    obj.SetAnnotation("ReviewDate", DateTime.Today.ToString("yyyy-MM-dd")));
```

### Encontrar todos los objetos con una expresión DAX

```csharp
// List all objects that have a DAX expression and depend on a specific table
var dependents = Model.AllMeasures.Cast<IDaxDependantObject>()
    .Concat(Model.AllColumns.OfType<CalculatedColumn>().Cast<IDaxDependantObject>())
    .Where(obj => obj.DependsOn.Tables.Any(t => t.Name == "Date"));
```

## Ver también

- @how-to-check-object-types
- @como-filtrar-objetos-de-consulta-con-linq
- @como-usar-anotaciones-y-propiedades-extendidas
- @como-trabajar-con-dependencias
