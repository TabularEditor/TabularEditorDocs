---
uid: script-remove-measures-with-error
title: View/Remove Measures with Errors
author: Kurt Buhler
updated: 2023-02-28
applies_to:
  versions:
    - version: 3.x
---
# Create M Partition

## Script Purpose
If you want to see all the measures that have errors and have the option to delete them from the model, saving a back-up .tsv of the deleted measures to a selected directory (in case you want to re-add them, later).

## Script

### View & Remove Measures with Errors
```csharp
// This script scans the model and shows all measures with errors, giving the option to remove them.
//
// .GetSemantics(...) method is only available in TE3
using System.Windows.Forms;
var measuresWithError = Model.AllMeasures.Where(m => m.GetSemantics(ExpressionProperty.Expression).HasError).ToList();

// If no measures with errors, end script with error.
if ( measuresWithError.Count == 0 )
{ 
Error ( "No measures with errors! 👍" );
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
### Explanation
This snippet gets all the measures that have errors according to the Tabular Editor Semantic Analysis. It then will display them in an output box where you can manually browse them or make changes. Thereafter, measures can be selected for removal. The removed measures can be saved as a back-up .tsv file in case you want to import them, later.

## Example Output
<br>
<img src="~/images/Cscripts/script-view-error-measures.png" alt="Image description" id="view-error-measures">
<script>
    var img = document.getElementById("view-error-measures");
    img.style.width = "600px";
</script>

<br>
<img src="~/images/Cscripts/script-delete-error-measures.png" alt="Image description" id="delete-error-measures">
<script>
    var img = document.getElementById("delete-error-measures");
    img.style.width = "600px";
</script>

<br>
<img src="~/images/Cscripts/script-delete-error-measures-success.png" alt="Image description" id="delete-error-measures-success">
<script>
    var img = document.getElementById("delete-error-measures-success");
    img.style.width = "350px";
</script>

<br>
<img src="~/images/Cscripts/script-delete-error-measures-backup.png" alt="Image description" id="delete-error-measures-backup">
<script>
    var img = document.getElementById("delete-error-measures-backup");
    img.style.width = "350px";
</script>