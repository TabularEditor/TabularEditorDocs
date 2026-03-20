---
uid: script-remove-measures-with-error
title: Ver/eliminar medidas con errores
author: Kurt Buhler
updated: 2023-02-28
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      full: true
---

# Ver/eliminar medidas con errores

## Propósito del script

Si quieres ver todas las medidas con errores y tener la opción de eliminarlas del modelo, puedes guardar una copia de seguridad en un archivo .tsv de las medidas eliminadas en el directorio que selecciones (por si quieres volver a agregarlas más adelante).

## Script

### Ver y eliminar medidas con errores

```csharp
// Este script examina el modelo y muestra todas las medidas con errores, dando la opción de quitarlas.
//
// El método .GetCachedSemantics(...) solo está disponible en TE3
using System.Windows.Forms;

// Oculta el spinbox de "Running Macro"
ScriptHelper.WaitFormVisible = false;

// Obtén todas las medidas que tienen errores
var measuresWithError = Model.AllMeasures.Where(m => m.GetCachedSemantics(ExpressionProperty.Expression).HasError).ToList();
// En versiones anteriores a Tabular Editor 3.12.0 debe usarse el método GetSemantics.
//var measuresWithError = Model.AllMeasures.Where(m => m.GetSemantics(ExpressionProperty.Expression).HasError).ToList();

// Si no hay medidas con errores, finaliza el script con un error.
if ( measuresWithError.Count == 0 )
{ 
Info ( "¡No hay medidas con errores! 👍" );
}

// Gestiona las medidas erróneas
else 
{

// Muestra la lista de medidas con un error
measuresWithError.Output();

//   En la lista, puedes seleccionar 1 o más medidas para eliminarlas
var _ToDelete = SelectObjects(measuresWithError, measuresWithError, "Selecciona las medidas que quieres eliminar.\nMás adelante podrás exportar una copia de seguridad.");

    // Elimina las medidas seleccionadas
    try
    {
        foreach ( var _m in _ToDelete ) 
            {
                _m.Delete();
            }
    
        Info ( 
            "Se eliminaron " + 
            Convert.ToString(_ToDelete.Count()) + 
            " medidas con errores." 
        );
    
        // Crea una instancia de la clase FolderBrowserDialog
        FolderBrowserDialog folderBrowserDialog = new FolderBrowserDialog();
        
        // Establece el título del cuadro de diálogo
        folderBrowserDialog.Description = "Selecciona un directorio donde guardar una copia de seguridad de las medidas eliminadas.";
        
        // Establece la carpeta raíz del cuadro de diálogo
        folderBrowserDialog.RootFolder = Environment.SpecialFolder.MyComputer;
        
        // Muestra el cuadro de diálogo y obtiene el resultado
        DialogResult result = folderBrowserDialog.ShowDialog();
        
        // Comprueba si el usuario hizo clic en Aceptar y obtiene la ruta seleccionada
        if (result == DialogResult.OK && !string.IsNullOrWhiteSpace(folderBrowserDialog.SelectedPath))
            {
                // Obtén la ruta de salida como una cadena
                string _outputPath = folderBrowserDialog.SelectedPath;
                
                // Obtén las propiedades de las medidas eliminadas
                var _backup = ExportProperties( _ToDelete );
    
                // Guarda una copia de seguridad de las medidas eliminadas
                SaveFile( _outputPath + "/DeletedMeasures-" + Model.Name + DateTime.Today.ToString("-yyyy-MM-dd") + ".tsv", _backup);
    
                Info ( 
                    "Se exportó una copia de seguridad de " + 
                    Convert.ToString(_ToDelete.Count()) +
                    " medidas a " + 
                    _outputPath
                );
            }
    }
    catch
    // Muestra un cuadro de información si no se seleccionó ninguna medida
    {
    Info ( "No se seleccionó ninguna medida." );
    }
}

```

### Explicación

Este fragmento obtiene todas las medidas que tienen errores según el análisis semántico de Tabular Editor. Después, las mostrará en una ventana de salida donde podrás revisarlas manualmente o hacer cambios. A continuación, se pueden seleccionar medidas para eliminarlas. Las medidas quitadas se pueden guardar como un archivo .tsv de copia de seguridad por si quieres importarlas más adelante.

## Ejemplo de salida

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-view-error-measures.png" alt="An output dialog that lets the user view and edit any measures with errors in Tabular Editor" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 1:</strong> Un cuadro de diálogo de salida te permite ver y editar cualquier medida que actualmente tenga "errores" según el análisis semántico de Analysis Services.</figcaption>
</figure>

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-delete-error-measures.png" alt="A selection dialog that lets the user select measures to delete" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 2:</strong> Las medidas con errores se pueden seleccionar para eliminarlas.</figcaption>
</figure>

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-delete-error-measures-success.png" alt="A confirmation dialog that informs the user the deletion was successful" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 3:</strong> Un cuadro de diálogo de confirmación te informará de que la eliminación de las medidas se realizó correctamente.</figcaption>
</figure>

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-delete-error-measures-backup.png" alt="A dialog that lets the user select a directory to save a .tsv back-up of the deleted measure metadata" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 4:</strong> De forma opcional, se puede guardar en un directorio local una copia de seguridad .tsv de las propiedades y definiciones de las medidas, por si fuera necesario volver a agregarlas más adelante.</figcaption>
</figure>
