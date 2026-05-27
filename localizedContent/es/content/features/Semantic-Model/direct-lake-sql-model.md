---
uid: direct-lake-sql-model
title: Direct Lake en modelos semánticos SQL
author: Morten Lønskov
updated: 2026-03-27
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

Los modelos semánticos de Direct Lake en SQL se conectan directamente a las fuentes de datos almacenadas en [OneLake en Fabric](https://learn.microsoft.com/en-us/fabric/onelake/onelake-overview) a través del punto de conexión SQL.

> [!IMPORTANT]
> A partir de [Tabular Editor 3.22.0](../../references/release-notes/3_22_0.md), Tabular Editor 3 es compatible con Direct Lake en OneLake, lo cual se recomienda en la mayoría de los escenarios. Consulta nuestro artículo de [guía de Direct Lake](xref:direct-lake-guidance) para obtener más información.

Tabular Editor 3 puede crear y conectarse a este tipo de modelo. Para ver un tutorial, consulta este artículo de nuestro blog: [Modelos semánticos de Direct Lake: cómo usarlos con Tabular Editor](https://blog.tabulareditor.com/2023/09/26/fabric-direct-lake-with-tabular-editor-part-2-creation/).
Tabular Editor 3 puede crear modelos semánticos de Direct Lake tanto con el punto de conexión SQL de Lakehouse como con el de Datawarehouse.

Tabular Editor 2 puede conectarse a modelos semánticos de Direct Lake, pero no incluye ninguna funcionalidad integrada para crear nuevas tablas ni modelos semánticos de Direct Lake. Esto debe hacerse manualmente o con un C# Script.

> [!NOTE]
> **Limitaciones de Direct Lake**
> Hay varias limitaciones en cuanto a los cambios que se pueden realizar en un modelo de Direct Lake. Consulta [Direct Lake Considerations and Limitations](https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview#considerations-and-limitations) para ver la lista completa. Consulta también [este artículo de SQLBI](https://www.sqlbi.com/blog/marco/2024/04/06/direct-lake-vs-import-mode-in-power-bi/) para obtener una visión general a la hora de elegir entre Direct Lake e Import mode.

## Crear un modelo de Direct Lake en SQL en Tabular Editor 3

La creación de un modelo de Direct Lake en SQL en Tabular Editor 3 (3.15.0 o superior) debe especificarse al crear el modelo en el cuadro de diálogo _Nuevo modelo_, mediante la casilla Direct Lake.

![Direct Lake New Model](~/content/assets/images/common/DirectLakeNewModelDialog.png)

Usar la casilla garantiza que se establezcan las propiedades y anotaciones específicas de Direct Lake, y también limita la importación de tablas a orígenes compatibles con Direct Lake.

> [!NOTE]
> En este momento, los modelos de Direct Lake en SQL usan una intercalación diferente a la de los modelos semánticos de importación habituales de Power BI. Esto puede provocar resultados diferentes al consultar el modelo o al hacer referencia a nombres de objetos en código DAX.
> Para más información, consulta esta entrada del blog de Kurt Buhler: [Modelos con distinción entre mayúsculas y minúsculas en Power BI: consecuencias y consideraciones](https://data-goblins.com/power-bi/case-specific).

> [!IMPORTANT]
> A partir de [Tabular Editor 3.22.0](../../references/release-notes/3_22_0.md), se ha eliminado la casilla Direct Lake del cuadro de diálogo Nuevo modelo. Debes [establecer manualmente la intercalación de tu modelo para que coincida con la de tu Fabric Warehouse](xref:direct-lake-guidance#collation) si usas Direct Lake en SQL.

## Enmarcado de nuevos modelos e importaciones de tablas

Tabular Editor 3 (3.15.0 o superior) enmarca (refresca) automáticamente el modelo en el primer despliegue. Esto garantiza que el modo Direct Lake esté activado; de lo contrario, el modelo volvería automáticamente a DirectQuery.

Además, al importar nuevas tablas, Tabular Editor 3 (3.15.0 o superior) enmarca (refresca) el modelo la próxima vez que se guarde. Esta preferencia se encuentra en **Herramientas > Preferencias > Implementación de modelo > Actualización de datos**.

## Identificación de un modelo Direct Lake

La barra de título superior de Tabular Editor muestra qué tipo de modelo está abierto en esa instancia de Tabular Editor. Además, el Explorador TOM muestra el tipo y el modo de cada tabla (Import, DirectQuery, Dual o Direct Lake). Si un modelo contiene una combinación de modos de tabla, la barra de título mostrará "Híbrido". Actualmente, no es posible que un modelo Direct Lake on SQL contenga tablas en modo Import, DirectQuery o Dual.

## Convertir un modelo Direct Lake a Import Mode

El siguiente C# Script convierte un modelo existente al modo Import mode. Esto puede ser útil si los requisitos de latencia de datos de tu modelo no requieren Direct Lake, o si quieres evitar las limitaciones de un modelo Direct Lake pero ya has empezado a crear uno en Fabric.

Es posible ejecutar el script cuando Tabular Editor está conectado a un modelo semántico a través del punto de conexión XMLA. Sin embargo, guardar los cambios directamente en el Workspace de Power BI/Fabric no está admitido por Microsoft. Para evitarlo, el enfoque recomendado es usar la opción "Modelo > Implementar...". Esto permite implementar el modelo recién convertido como una nueva entidad en un Workspace.

> [!NOTE]
> Después de implementar el modelo recién convertido en modo de importación, tendrás que especificar las credenciales para acceder al Lakehouse y actualizar los datos en el modelo.

### Script de C# para convertir un modelo Direct Lake a Import Mode

```csharp
// **********************************************************************************
// Convertir un modelo en modo Direct Lake a modo Import
// ---------------------------------------------
//
// Cuando este script se ejecute en un modelo semántico, hará lo siguiente:
//
//   - Recorrer todas las tablas. Cualquier tabla que contenga exactamente 1 partición y que
//     esté en modo Direct Lake, verá su partición reemplazada por una partición equivalente
//     en modo Import.
//   - Establecer la intercalación del modelo en null (predeterminado)
// 
// Observaciones:
// 
//   - Las particiones en modo Import usarán el endpoint SQL del Lakehouse.
//   - El script asume que la expresión compartida que especifica el endpoint SQL
//     se llama "DatabaseQuery".
//   - Como TE2 no expone la propiedad "SchemaName" en los objetos EntityPartition,
//     tenemos que usar reflexión para acceder a los objetos TOM subyacentes.
//
// Compatibilidad:
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
    // Las tablas en modo Direct Lake solo tienen 1 partición...
    if(table.Partitions.Count != 1) continue;
    
    // ...que debería estar en modo "DirectLake":
    var partition = table.Partitions[0];
    if(partition.Mode != ModeType.DirectLake) continue;

    // Lamentablemente, Tabular Editor no expone la propiedad SchemaName de EntityPartitionSources,
    // así que tendremos que usar reflexión para acceder al objeto TOM subyacente.
    var pMetadataObjct = typeof(Partition).GetProperty("MetadataObject", BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.DeclaredOnly);
    var tomPartition = pMetadataObjct.GetValue(partition) as Microsoft.AnalysisServices.Tabular.Partition;
    var tomPartitionSource = tomPartition.Source as Microsoft.AnalysisServices.Tabular.EntityPartitionSource;
    
    // La tabla no tiene un EntityPartitionSource, lo que significa que no es una tabla de Direct Lake
    // (no debería ocurrir, ya que comprobamos el modo DirectLake más arriba...)
    if(tomPartitionSource == null) continue;
    
    var schemaName = tomPartitionSource.SchemaName;
    var tableName = tomPartitionSource.EntityName;

    // Cambiar el nombre de la partición original (Direct Lake) (ya que no podemos tener dos particiones con el mismo nombre):
    var partitionName = partition.Name;
    partition.Name += "_old";
    
    // Agregar la nueva partición (Import):
    table.AddMPartition(partitionName, string.Format(mImportTemplate, schemaName, tableName));
    
    // Eliminar la partición antigua (Direct Lake)):
    partition.Delete();
}

// Actualizar la intercalación del modelo:
Model.Collation = null;
Model.DefaultMode = ModeType.Import;
Model.RemoveAnnotation("TabularEditor_DirectLake");
```