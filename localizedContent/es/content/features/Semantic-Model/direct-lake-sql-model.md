---
uid: direct-lake-sql-model
title: Direct Lake en modelos semánticos de SQL
author: Morten Lønskov
updated: 2026-10-12
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          none: true
        - edition: Enterprise
          full: true
---

# Modelos semánticos de Direct Lake
Los modelos semánticos de Direct Lake en SQL se conectan directamente a las fuentes de datos almacenadas en [OneLake en Fabric](https://learn.microsoft.com/fabric/onelake/onelake-overview) a través del punto de conexión SQL. 

> [!IMPORTANT]
> A partir de [Tabular Editor 3.22.0](../../references/release-notes/3_22_0.md), Tabular Editor 3 admite Direct Lake en OneLake, lo cual se recomienda en la mayoría de los escenarios. Consulta nuestro artículo [Guía de Direct Lake](xref:direct-lake-guidance) para obtener más información.

Tabular Editor 3 puede crear este tipo de modelo y conectarse a él. Para obtener un tutorial sobre este tema, consulta nuestro artículo del blog: [Modelos semánticos de Direct Lake: cómo usarlos con Tabular Editor](https://blog.tabulareditor.com/2023/09/26/fabric-direct-lake-with-tabular-editor-part-2-creation/). 
Tabular Editor 3 puede crear modelos semánticos de Direct Lake tanto con el punto de conexión SQL de Lakehouse como con el de Datawarehouse. 

Tabular Editor 2 puede conectarse a modelos semánticos de Direct Lake, pero no dispone de ninguna funcionalidad integrada para crear nuevas tablas ni modelos semánticos de Direct Lake. Esto debe hacerse manualmente o con un script de C#. 

> [!NOTE]
> **Limitaciones de Direct Lake**
> Existen varias limitaciones a los cambios que se pueden realizar en un modelo Direct Lake. Consulte [Consideraciones y limitaciones de Direct Lake](https://learn.microsoft.com/fabric/fundamentals/direct-lake-overview#considerations-and-limitations) para ver la lista completa. Consulte también [este artículo de SQLBI](https://www.sqlbi.com/blog/marco/2024/04/06/direct-lake-vs-import-mode-in-power-bi/) para obtener una descripción general sobre cómo elegir entre el modo Direct Lake y el modo Importación.

## Creación de un modelo Direct Lake en SQL en Tabular Editor 3

La creación de un modelo Direct Lake en SQL en Tabular Editor 3 (3.15.0 o superior) debe especificarse cuando se cree el modelo en el cuadro de diálogo _Nuevo modelo_, utilizando la casilla de verificación Direct Lake. 

![Nuevo modelo Direct Lake](~/content/assets/images/common/DirectLakeNewModelDialog.png)

El uso de la casilla de verificación garantiza que se establezcan las propiedades y anotaciones específicas de Direct Lake, además de limitar la importación de tablas a los orígenes compatibles con Direct Lake. 

> [!NOTE]
> Actualmente, los modelos Direct Lake en SQL utilizan una intercalación diferente a la de los modelos semánticos de importación de Power BI habituales. Esto puede dar lugar a resultados diferentes al consultar el modelo o al hacer referencia a nombres de objetos en el código DAX.
> Para obtener más información, consulta esta entrada del blog de Kurt Buhler: [Modelos que distinguen entre mayúsculas y minúsculas en Power BI: consecuencias y consideraciones](https://data-goblins.com/power-bi/case-specific).

> [!IMPORTANT]
> A partir de [Tabular Editor 3.22.0](../../references/release-notes/3_22_0.md), la casilla de verificación Direct Lake se ha eliminado del cuadro de diálogo Nuevo modelo. Debe [establecer manualmente la intercalación en su modelo para que coincida con la de su almacén de Fabric](xref:direct-lake-guidance#collation) si utiliza Direct Lake en SQL.

## Enmarcado de nuevos modelos e importaciones de tablas

Tabular Editor 3 (3.15.0 o superior) enmarca (actualiza) automáticamente el modelo en la primera implementación. Esto se hace para garantizar que el modo Direct Lake esté activado; de lo contrario, el modelo recurriría automáticamente a DirectQuery.

Además, al importar nuevas tablas, Tabular Editor 3 (3.15.0 o superior) enmarca (actualiza) el modelo cuando se guarda la siguiente vez. Esta preferencia se encuentra en **Herramientas > Preferencias > Implementación de modelo > Actualización de datos**.



## Identificación de un modelo Direct Lake
La barra de título de Tabular Editor 3 muestra el modo de almacenamiento del modelo abierto después del nombre del modelo, como **(Direct Lake)**, **(DirectQuery)** o **(Import)**. Si un modelo contiene una combinación de modos de tabla, la barra de título muestra **(Compuesto)**. El Explorador TOM muestra el tipo y el modo de cada tabla (Importación, DirectQuery, Dual o Direct Lake). Un modelo Direct Lake en SQL no puede contener tablas en modo Importación, DirectQuery o Dual.


## Conversión de un modelo Direct Lake al modo Importación

El siguiente script de C# convierte un modelo existente al modo Importación. Esto puede ser útil si los requisitos de latencia de datos de su modelo no precisan Direct Lake o si desea evitar las limitaciones de un modelo Direct Lake, pero ya ha empezado a crear uno dentro de Fabric.

Es posible ejecutar el script cuando Tabular Editor está conectado a un modelo semántico a través del punto de conexión XMLA. Sin embargo, Microsoft no admite guardar los cambios directamente en el área de trabajo de Power BI/Fabric. Para evitar esto, el enfoque recomendado es usar la opción «Modelo > Implementar...». Esto permite implementar el modelo recién convertido como una nueva entidad en un área de trabajo.

> [!NOTE]
> Después de implementar el modelo recién convertido al modo de importación, deberá especificar las credenciales para acceder al Lakehouse y actualizar los datos en el modelo.

### Script de C# para convertir el modelo Direct Lake al modo de importación

```csharp
// **********************************************************************************
// Convert Direct Lake-mode model to Import-mode
// ---------------------------------------------
//
// When this script is executed on a semantic model, it will:
//
//   - Loop through all tables. Any table that contains exactly 1 partition, which
//     is in Direct Lake mode, will have its partition replaced by an equivalent
//     Import-mode partition.
//   - Set the collation of the model to null (default)
// 
// Remarks:
// 
//   - The Import-mode partitions will use the SQL endpoint of the Lakehouse.
//   - The script assumes that the Shared Expression which specifies the SQL endpoint
//     is called "DatabaseQuery".
//   - Because TE2 does not expose the "SchemaName" property on EntityPartition
//     objects, we have to use reflection to access the underlying TOM objects.
//
// Compatibility:
// TE2.x, TE3.x
// **********************************************************************************

using System.Reflection;

const string mImportTemplate = 
@"let
    Source = DatabaseQuery,
    Data = Source{{[Schema=""{0}"",Item=""{1}""]}}[Data]
in
    Data";

foreach(var table in Model.Tables)
{
    // Direct Lake-mode tables only have 1 partition...
    if(table.Partitions.Count != 1) continue;
    
    // ...which should be in "DirectLake" mode:
    var partition = table.Partitions[0];
    if(partition.Mode != ModeType.DirectLake) continue;

    // Tabular Editor unfortunately doesn't expose the SchemaName property of EntityPartitionSources,
    // so we'll have to use reflection to access the underlying TOM object.
    var pMetadataObjct = typeof(Partition).GetProperty("MetadataObject", BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.DeclaredOnly);
    var tomPartition = pMetadataObjct.GetValue(partition) as Microsoft.AnalysisServices.Tabular.Partition;
    var tomPartitionSource = tomPartition.Source as Microsoft.AnalysisServices.Tabular.EntityPartitionSource;
    
    // Table does not have an EntityPartitionSource, meaning it is not a Direct Lake table
    // (shouldn't happen, since we already checked for DirectLake mode above...)
    if(tomPartitionSource == null) continue;
    
    var schemaName = tomPartitionSource.SchemaName;
    var tableName = tomPartitionSource.EntityName;

    // Rename the original (Direct Lake) partition (as we can't have two partitions with the same name):
    var partitionName = partition.Name;
    partition.Name += "_old";
    
    // Add the new (Import) partition:
    table.AddMPartition(partitionName, string.Format(mImportTemplate, schemaName, tableName));
    
    // Delete the old (Direct Lake) partition):
    partition.Delete();
}

// Update model collation:
Model.Collation = null;
Model.DefaultMode = ModeType.Import;
Model.RemoveAnnotation("TabularEditor_DirectLake");
```