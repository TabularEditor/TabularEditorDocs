---
uid: script-create-and-replace-parameter
title: Create M Parameter (Auto-Replace)
author: Kurt Buhler
updated: 2023-02-28
applies_to:
  versions:
    - version: 3.x
---
# Create New M Parameter and Add it to Existing M Partitions

## Script Purpose
If you want to replace a string in model M Partitions (i.e. connection string, filter condition, column name, etc.) with a parameter value.
<br></br>
> [!NOTE] 
> This script only works with parameters of `string` data type. 
> For other data types, please modify the variable types & parameter value appropriately.
<br></br>

## Script

### Create New M Parameter and Add it to Existing M Partitions
```csharp
// This script creates a new M Parameter as a 'Shared Expression'.
// It will also find the default value in all M partitions and replace them with the parameter object name.
//
// Opens a dialogue box requesting user input for the parameter name
string _ParameterName = 
    Microsoft.VisualBasic.Interaction.InputBox(
        "Enter the parameter name.\n" + 
        "A new 'Shared Expression' with this name will be created for the M Parameter.", 
        "Parameter Name:", 
        "NewParameter"
    );


// Opens a dialogue box requesting user input for the parameter value (string)
string _ParameterValue = 
    Microsoft.VisualBasic.Interaction.InputBox(
        "Enter the parameter default value (String data type).\n" + 
        "The M Parameter will be configured with this default value, i.e. a connection string.", 
        "Parameter Value:", 
        "DefaultValue"
    );


// Creates the parameter
Model.AddExpression( 
    _ParameterName, 
    @"
""" + _ParameterValue +
@""" meta
[
	IsParameterQuery = true,
	IsParameterQueryRequired = true,
	Type = type text
]"
);


// Informs the user that the parameter was successfully created
Info ( 
    "Successfully created a new parameter: " + @"""" +
    _ParameterName + @"""" +
    "\nDefault value: " + @"""" +
    _ParameterValue + @"""");


// Finds the parameter default value in M Partitions & replaces with the parameter name
string _Find = @"""" + _ParameterValue + @"""";
string _Replace = @"#""" + _ParameterName + @"""";

int _NrMPartitions = 0;
int _NrReplacements = 0;
var _ReplacementsList = new List<string>();

foreach ( var _Tables in Model.Tables )
{
    foreach ( var _p in _Tables.Partitions )
    {
        if ( _p.SourceType == PartitionSourceType.M )
        {
            if ( _p.Expression != _p.Expression.Replace( _Find, _Replace ) )
            {
                _p.Expression = _p.Expression.Replace( _Find, _Replace );

                // Tracks which M partitions were replaced (and how many)
                _NrReplacements = _NrReplacements + 1;
                _ReplacementsList.Add( _p.Name );
            }

        // Counts the total # M Partitions
        _NrMPartitions = _NrMPartitions + 1;
        }
    }
}


// Makes a bulleted list of all the M partitions that were replaced
string _ReplacedPartitions = " • " + String.Join("\n • ", _ReplacementsList );


// Informs 
//      - Whether the Find & Replace was successful
//      - How many M partitions were replaced
//      - Which M partitions had the Find & Replace done
Info (
    "Successfully replaced\n\n " +
    _Find + 
    "\n\n with: \n\n" + 
    _Replace + 
    "\n\n in " + 
    Convert.ToString(_NrReplacements) +
    " of " +
    Convert.ToString(_NrMPartitions) +  
    " M Partitions:\n" +
    _ReplacedPartitions
);
```
### Explanation
This snippet opens a dialogue box for the user to enter the parameter name and value, then creates the parameter as a 'Shared Expression' in the model.
It will then search all M partitions for the default value, replacing them with the `#"ParameterName"`. 

## Example Output
<br>
<img src="~/images/Cscripts/script-create-parameter-auto-replace.png" alt="Image description" id="script-create-parameter-auto-replace">
<script>
    var img = document.getElementById("script-create-parameter-auto-replace");
    img.style.width = "400px";
</script>