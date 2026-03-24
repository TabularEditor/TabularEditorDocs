---
uid: table-groups
title: Grupos de tablas
author: Daniel Otykier
updated: 2023-03-08
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

# Grupos de tablas

Los grupos de tablas son una nueva funcionalidad disponible en Tabular Editor 3 a partir de la [versión 3.5.0](xref:release-3-5-0). Esta funcionalidad permite organizar rápidamente las tablas en carpetas, lo que facilita más que nunca administrar y navegar por modelos grandes y complejos en el [Explorador TOM](xref:tom-explorer-view) de Tabular Editor 3.

![Grupos de tablas](~/content/assets/images/user-interface/table-groups.png)

Puedes configurar los grupos de tablas haciendo clic con el botón derecho en una tabla y eligiendo la opción de menú **Crear > Grupo de tablas**, o bien especificando un nombre para el grupo de tablas en la **vista de propiedades** mientras seleccionas una o varias tablas.

Las tablas se pueden mover entre grupos de tablas arrastrando y soltando en el Explorador TOM. Ten en cuenta que, a diferencia de las carpetas de visualización para medidas, columnas y jerarquías, los grupos de tablas no se pueden anidar.

Al hacer clic con el botón derecho en un grupo de tablas en el Explorador TOM, obtienes las mismas opciones del menú contextual que si hubieras seleccionado la tabla o las tablas dentro de ese grupo de tablas.

> [!NOTE]
> Los grupos de tablas son una característica exclusiva de Tabular Editor. Las herramientas cliente (como Excel, Power BI Desktop, etc.) no contemplarán los grupos de tablas, ya que el [formato CSDL](https://learn.microsoft.com/en-us/ef/ef6/modeling/designer/advanced/edmx/csdl-spec), que especifica el esquema conceptual del modelo de datos, no admite los grupos de tablas.

## Metadatos y scripts

Tabular Editor usa una anotación en cada tabla para especificar a qué grupo de tablas pertenece esa tabla. El nombre de la anotación es `TabularEditor_TableGroup`. Sin embargo, al aplicar cambios al modelo mediante scripts de C#, puedes modificar el grupo de tablas directamente a través de la nueva propiedad `Table.TableGroup` (string).

A continuación se muestra un ejemplo de C# Script que recorre todas las tablas de un modelo y las organiza en grupos de tablas en función de su tipo y uso:

```csharp
// Recorrer todas las tablas:
foreach(var table in Model.Tables)
{
    if (table is CalculationGroupTable)
    {
        table.TableGroup = "Grupos de cálculo";
    }
    else if (!table.UsedInRelationships.Any() && table.Measures.Any(m => m.IsVisible))
    {
        // Tablas que contienen medidas visibles, pero sin relaciones con otras tablas
        table.TableGroup = "Grupos de medidas";
    }
    else if (table.UsedInRelationships.All(r => r.FromTable == table) && table.UsedInRelationships.Any())
    {
        // Tablas que están exclusivamente en el lado "muchos" de las relaciones:
        table.TableGroup = "Hechos";
    }
    else if (!table.UsedInRelationships.Any() && table is CalculatedTable && !table.Measures.Any())
    {
        // Tablas sin ninguna relación, que son tablas calculadas y no tienen medidas:
        table.TableGroup = "Tablas de parámetros";
    }
    else if (table.UsedInRelationships.Any(r => r.ToTable == table))
    {
        // Tablas en el lado "uno" de las relaciones:
        table.TableGroup = "Dimensiones";
    }
    else
    {
        // Todas las demás tablas:
        table.TableGroup = "Varios";
    }
}
```

## Ocultar grupos de tablas

Si prefieres ver siempre la lista completa de tablas sin agrupar en el Explorador TOM, pero colaboras con otras personas en un modelo que incluye anotaciones de grupos de tablas, aun así puedes desactivar los grupos de tablas por completo en tu instalación de Tabular Editor 3. Esto se hace desde el cuadro de diálogo **Herramientas > Preferencias**. Ve a la página **Explorador TOM** y, en **Visualización y filtrado**, desmarca **Usar grupos de tablas**:

![Desactivar grupos de tablas](~/content/assets/images/table-groups-disable.png)

> [!NOTE]
> Aunque hayas desactivado los grupos de tablas como se describe arriba, las tablas de tu modelo pueden seguir teniendo asignada la anotación `TabularEditor_TableGroup`. Si deseas borrar todas esas anotaciones del modelo, puedes usar el siguiente C# Script:
>
> ```csharp
> foreach(var table in Model.Tables) table.TableGroup = null;
> ```