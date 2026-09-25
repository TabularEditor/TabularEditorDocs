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

## Objetivo del script

Si quieres ver todas las medidas con errores y tener la opción de eliminarlas del modelo, puedes guardar una copia de seguridad en un archivo .tsv de las medidas eliminadas en el directorio que selecciones (por si quieres volver a agregarlas más adelante).

## Script

### Ver y eliminar medidas con errores

```csharp
// This script scans the model and shows all measures with errors, giving the option to remove them.
//
// .GetCachedSemantics(...) method is only available in TE3
using System.Windows.Forms;

// Hide the 'Running Macro' spinbox
ScriptHelper.WaitFormVisible = false;

// Get all the measures that have errors
var measuresWithError = Model.AllMeasures.Where(m => m.GetCachedSemantics(ExpressionProperty.Expression).HasError).ToList();
//Prior to Tabular Editor 3.12.0 the GetSemantics method must be used.
//var measuresWithError = Model.AllMeasures.Where(m => m.GetSemantics(ExpressionProperty.Expression).HasError).ToList();

// If no measures with errors, end script with error.
if ( measuresWithError.Count == 0 )
{ 
Info ( "No measures with errors! 👍" );
}

// Handle erroneous measures
else 
{

// View the list of measures with an error
measuresWithError.Output();

//   From the list, you can select 1 or more measures to delete
var _ToDelete = SelectObjects(measuresWithError, measuresWithError, "Select measures to delete.\nYou will be able to export a back-up, later.");

    // Delete the selected measures
    try
    {
        foreach ( var _m in _ToDelete ) 
            {
                _m.Delete();
            }
    
        Info ( 
            "Deleted " + 
            Convert.ToString(_ToDelete.Count()) + 
            " measures with errors." 
        );
    
        // Create an instance of the FolderBrowserDialog class
        FolderBrowserDialog folderBrowserDialog = new FolderBrowserDialog();
        
        // Set the title of the dialog box
        folderBrowserDialog.Description = "Select a directory to output a backup of the deleted measures.";
        
        // Set the root folder of the dialog box
        folderBrowserDialog.RootFolder = Environment.SpecialFolder.MyComputer;
        
        // Show the dialog box and get the result
        DialogResult result = folderBrowserDialog.ShowDialog();
        
        // Check if the user clicked the OK button and get the selected path
        if (result == DialogResult.OK && !string.IsNullOrWhiteSpace(folderBrowserDialog.SelectedPath))
            {
                // Get the output path as a string
                string _outputPath = folderBrowserDialog.SelectedPath;
                
                // Get the properties of the deleted measures
                var _backup = ExportProperties( _ToDelete );
    
                // Save a backup of the deleted measures
                SaveFile( _outputPath + "/DeletedMeasures-" + Model.Name + DateTime.Today.ToString("-yyyy-MM-dd") + ".tsv", _backup);
    
                Info ( 
                    "Exported a backup of " + 
                    Convert.ToString(_ToDelete.Count()) +
                    " Measures to " + 
                    _outputPath
                );
            }
    }
    catch
    // Display an info box if no measure was selected
    {
    Info ( "No measure selected." );
    }
}

```

### Explicación

Este fragmento obtiene todas las medidas que tienen errores según el análisis semántico de Tabular Editor. Después, las mostrará en una ventana de salida donde podrás revisarlas manualmente o hacer cambios. A continuación, se pueden seleccionar medidas para eliminarlas. Las medidas quitadas se pueden guardar como un archivo .tsv de copia de seguridad por si quieres importarlas más adelante.

## Salida de ejemplo

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
