---
uid: powerbi-xmla-pbix-workaround
title: Creación de un archivo PBIX a partir de un punto de conexión XMLA.
author: Morten Lønskov
updated: 2023-10-18
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          partial: true
          note: "Solo puntos de conexión XMLA Premium por usuario"
        - edition: Enterprise
          full: true
---

# Descargar un Dataset de Power BI a un archivo .pbix mediante el punto de conexión XMLA

Una vez que se realiza un cambio en un modelo semántico de Power BI mediante el punto de conexión XMLA, no es posible descargar el modelo como un archivo .pbix desde el servicio de Power BI.

Sin embargo, con el archivo de Proyecto de Power BI, es posible crear un archivo .pbix a partir del modelo remoto siguiendo el proceso de tres pasos que se describe a continuación.

![Resumen de XMLA a PBIX](~/content/assets/images/power-bi/create-pbix-from-xmla-overview.png)

> [!NOTE]
> La solución alternativa descrita no está respaldada oficialmente por Microsoft. No hay garantía de que funcione con todos los modelos. En concreto, si has agregado particiones personalizadas u otros objetos [enumerados aquí](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-external-tools#data-modeling-operations), es posible que Power BI Desktop no pueda abrir correctamente el archivo siguiendo este enfoque. Consulta a continuación un script para gestionar las particiones de actualización incremental.

## Paso 1: Crear y guardar un archivo de Proyecto de Power BI (.pbip) vacío

El primer paso es crear un nuevo Report de Power BI y guardarlo como un archivo de Proyecto de Power BI (.pbip) vacío, como se muestra en el siguiente diagrama.

![Save PBIP file](~/content/assets/images/power-bi/save-pbip-file.png)

Esto crea una estructura de carpetas que contiene un archivo _model_ vacío. Este archivo _model_ contiene los metadatos del modelo. En el siguiente paso sobrescribirás estos metadatos con los del modelo publicado que quieres guardar en .pbix.

![PBIP with Model file](~/content/assets/images/power-bi/pbip-file-bim-model.png)

Cierra Power BI Desktop y continúa con el siguiente paso en Tabular Editor.

## Paso 2: Abrir el modelo XMLA con Tabular Editor

Con Tabular Editor abierto, conéctate al Workspace de Fabric mediante el punto de conexión XMLA. Carga el modelo semántico de Power BI que quieras convertir en un archivo .pbix.

## Paso 3: Guardar el modelo XMLA en un archivo .pbip

En Tabular Editor, selecciona _Archivo > Guardar como..._ y navega hasta la carpeta del Proyecto de Power BI. Sobrescribe el archivo _model.bim_ que se muestra en el diagrama anterior.

Esto guardará el modelo remoto en el Proyecto de Power BI, que ahora contendrá los metadatos del modelo.

Si la carpeta .pbip está configurada para almacenar el modelo como archivos [TMDL](xref:tmdl), tendrás que usar la opción Guardar en carpeta en Tabular Editor. Luego, navega hasta la carpeta del Proyecto de Power BI del modelo semántico (ModelName.SemanticModel), abre la carpeta "definition" y guarda ahí tu modelo.

> [!NOTE]
> Para habilitar TMDL, ve a **Herramientas > Preferencias > Formatos de archivo > Guardar en carpeta** y selecciona "TMDL" en la lista desplegable **Modo de serialización**. Consulta la [documentación de TMDL para más información](xref:tmdl)

## Paso 3,1: Eliminar las particiones de actualización incremental y crear otras nuevas (Opcional)

Usa el script Convert Incremental Refresh que aparece a continuación para eliminar las particiones de actualización incremental y crear una única partición por tabla que contenga la expresión usada en la actualización incremental.

## Paso 4: Guardar como un archivo .pbix y abrirlo en Power BI Desktop

![PBIP con tablas](~/content/assets/images/power-bi/pbip-includes-tables.png)

Abre el archivo .pbip y el Report de Power BI pasará a contener el modelo semántico del punto de conexión XMLA.

Guárdalo como un archivo .pbix con _Archivo > Guardar como..._ en Power BI Desktop.

## Rehidratar el archivo .pbix

El .pbix ahora contiene el modelo que se publicó en el Workspace de Fabric. Cuando abras el .pbix, puedes _rehidratar_ el archivo; es decir, cargar los datos según las conexiones especificadas en el modelo.

## Convertir particiones de actualización incremental

El paso 4 anterior fallará si el modelo semántico tiene la actualización incremental habilitada, ya que un modelo de Power BI Desktop no puede contener varias particiones.
En ese caso, debes ejecutar el siguiente script en el modelo para convertir las particiones de actualización incremental en particiones únicas

```csharp
foreach (var t in Model.Tables)
{
    if(t.EnableRefreshPolicy)
    {
        //Recopilaremos el SourceExpression de la expresión de origen de la actualización incremental de la tabla
        string m_expression = t.SourceExpression.ToString();
         
        //Generaremos un nuevo nombre de partición
        string partition_name = t.Name + "-" + Guid.NewGuid();

        //Ahora crearemos una nueva partición
        var partition = t.AddMPartition(partition_name, m_expression);
        partition.Mode = ModeType.Import;
        
        //A continuación eliminaremos todas las particiones de actualización incremental de la tabla
        foreach (var p in t.Partitions.OfType<PolicyRangePartition>().ToList())
        {
            p.Delete();
        }
    }
};
```

Gracias a [Micah Dail](https://twitter.com/MicahDail) por crear el script y sugerir que se incluyera en este documento.
