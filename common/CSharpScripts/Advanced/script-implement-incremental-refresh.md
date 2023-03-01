---
uid: script-implement-incremental-refresh
title: Setup Incremental Refresh
author: Kurt Buhler
updated: 2023-03-01
applies_to:
  versions:
    - version: 2.x
    - version: 3.x
---
# Configure Incremental Refresh

## Script Purpose
If you want to configure Incremental Refresh for an import table based on a specific date field.
This script will work for `datetime`, `date`, or `integer` date columns for which you want to configure incremental refresh.

To use the script, select the date column in the table for which you want to configure incremental refresh, then run the script. The script will only run if you don't already have a #"RangeStart" and #"RangeEnd" parameter, and the selected table doesn't already have a Refresh Policy configured.

<br></br>
> [!NOTE] 
> This script will automatically modify the M partition of the table to add the filter step.
> Be sure to check that this was done correctly. 
>
> If you have many steps you must be sure to move this step to a point when it will fold to the data source. 
> Make sure you adjust all the `#"Step References" in Power Query
<br></br>

<br></br>
> [!NOTE] 
> This script uses user input to generate the refresh policy. 
> Make sure you enter the correct values in the user input dialogue box.
<br></br>

## Script

### Implement Incremental Refresh for Selected Column
```csharp
// This script will automatically generate an Incremental Refresh policy for a selected table
// It is generated based on the selected column
// It requires input from the user with a dialogue pop-up box.
//
using System.Windows.Forms;

var _Table = Selected.Column.Table;
string _MExpression = _Table.Partitions[0].Expression;

try 
{ 
    Model.Expressions.Contains(Model.Expressions["RangeStart"]);
    Info ("RangeStart already exists!");
}
catch
{
    // Add RangeStart parameter
    Model.AddExpression( 
        "RangeStart", 
        @"
    #datetime(2023, 01, 01, 0, 0, 0) meta
    [
        IsParameterQuery = true,
        IsParameterQueryRequired = true,
        Type = type datetime
    ]"
    );

    // Success message
    Info ( "Created 'RangeStart' M Parameter!" );
}

// Test if the RangeEnd parameter exists
try 
{ 
    Model.Expressions.Contains(Model.Expressions["RangeEnd"]);
    Info ("RangeEnd already exists!");
}
catch
{
    // Add RangeEnd parameter
    Model.AddExpression( 
        "RangeEnd", 
        @"
    #datetime(2023, 31, 01, 0, 0, 0) meta
    [
        IsParameterQuery = true,
        IsParameterQueryRequired = true,
        Type = type datetime
    ]"
    );

    // Success message
    Info ( "Created 'RangeEnd' M Parameter!" );

}

// Throw an error if there is already a refresh policy
if ( _Table.EnableRefreshPolicy == true )
{
    Error ( 
        "A refresh policy is already configured for" +
        Selected.Column.Table.Name + 
        "!\n\n" +
        "No changes were made."
    );
}
else 
{
    

    // Incremental Refresh Configuration
    // --------------------------------------------------------//

    // Label for how long data should be stored
    var storeDataLabel = new Label();
    storeDataLabel.Text = "Store data in the last:";
    storeDataLabel.Location = new System.Drawing.Point(20, 20);
    storeDataLabel.AutoSize = true;
    
    // User input for how long data should be stored
    var storeDataTextBox = new TextBox();
    storeDataTextBox.Location = new System.Drawing.Point(150, 20);
    storeDataTextBox.Size = new System.Drawing.Size(100, 20);
    
    // Adjust the Location of the storeDataLabel to align with the storeDataTextBox
    storeDataLabel.Location = 
        new System.Drawing.Point(
        storeDataTextBox.Location.X - storeDataLabel.Width - 20, 
        storeDataTextBox.Location.Y + 4
        );
    
    // User selection for how long data should be stored (granularity)
    var storeDataComboBox = new ComboBox();
    storeDataComboBox.Location = new System.Drawing.Point(270, 20);
    storeDataComboBox.Size = new System.Drawing.Size(100, 20);
    storeDataComboBox.DropDownStyle = ComboBoxStyle.DropDownList;
    storeDataComboBox.Items.AddRange(new object[] { "days", "months", "quarters", "years" });
    
    // Label for how much data should be refreshed
    var refreshDataLabel = new Label();
    refreshDataLabel.Text = "Refresh data in the last:";
    refreshDataLabel.Location = new System.Drawing.Point(20, 60);
    refreshDataLabel.AutoSize = true;
    
    // User input for how much data should be refreshed
    var refreshDataTextBox = new TextBox();
    refreshDataTextBox.Location = new System.Drawing.Point(150, 60);
    refreshDataTextBox.Size = new System.Drawing.Size(100, 20);
    
    // Adjust the Location of the refreshDataLabel to align with the refreshDataTextBox
    refreshDataLabel.Location = 
        new System.Drawing.Point(
        refreshDataTextBox.Location.X - refreshDataLabel.Width - 32, 
        refreshDataTextBox.Location.Y + 4
        );
    
    // User selection for how much data should be refreshed (Period)
    var refreshDataComboBox = new ComboBox();
    refreshDataComboBox.Location = new System.Drawing.Point(270, 60);
    refreshDataComboBox.Size = new System.Drawing.Size(100, 20);
    refreshDataComboBox.DropDownStyle = ComboBoxStyle.DropDownList;
    refreshDataComboBox.Items.AddRange(new object[] { "days", "months", "quarters", "years" });
    
    // User input to refresh full periods or not
    var fullPeriodsCheckBox = new CheckBox();
    fullPeriodsCheckBox.Text = "Refresh only full periods";
    fullPeriodsCheckBox.Location = new System.Drawing.Point(20, 100);
    fullPeriodsCheckBox.AutoSize = true;
    
    // Form OK button
    var okButton = new Button();
    okButton.Text = "OK";
    okButton.Location = new System.Drawing.Point(200, 140);
    okButton.Size = new System.Drawing.Size(80, 25);
    okButton.DialogResult = DialogResult.OK;
    
    // Form cancel button
    var cancelButton = new Button();
    cancelButton.Text = "Cancel";
    cancelButton.Location = new System.Drawing.Point(300, 140);
    cancelButton.Size = new System.Drawing.Size(80, 25);
    cancelButton.DialogResult = DialogResult.Cancel;
    
    // Form config
    var form = new Form();
    form.Text = "Incremental Refresh configuration:";
    form.ClientSize = new System.Drawing.Size(450, 200);
    form.FormBorderStyle = FormBorderStyle.FixedDialog;
    form.MaximizeBox = false;
    form.MinimizeBox = false;

    // Open the dialogue in the center of the screen
    form.StartPosition = FormStartPosition.CenterScreen;

    // Set the AutoScaleMode property to Dpi
    form.AutoScaleMode = AutoScaleMode.Dpi;

    // Add controls to form specified above
    form.Controls.Add(storeDataLabel);
    form.Controls.Add(storeDataTextBox);
    form.Controls.Add(storeDataComboBox);
    form.Controls.Add(refreshDataLabel);
    form.Controls.Add(refreshDataTextBox);
    form.Controls.Add(refreshDataComboBox);
    form.Controls.Add(fullPeriodsCheckBox);
    form.Controls.Add(okButton);
    form.Controls.Add(cancelButton);
    
    // Draw the form
    var result = form.ShowDialog();

    // Get the values of the user input if entered
    if (result == DialogResult.OK)
    {
        // Enables the refresh policy
        _Table.EnableRefreshPolicy = true;
        
        var storeDataValue = storeDataTextBox.Text;
        var storeDataComboBoxValue = storeDataComboBox.SelectedItem.ToString();
        var refreshDataValue = refreshDataTextBox.Text;
        var refreshDataComboBoxValue = refreshDataComboBox.SelectedItem.ToString();
        var fullPeriodsChecked = fullPeriodsCheckBox.Checked;
    
        // Display the input values in a message box
        var message = string.Format(
            "Store data in the last: {0} {1}" + 
            "\nRefresh data in the last: {2} {3}" + 
            "\nRefresh only full periods: {4}",
            storeDataTextBox.Text,
            storeDataComboBox.SelectedItem.ToString(),
            refreshDataTextBox.Text,
            refreshDataComboBox.SelectedItem.ToString(),
            fullPeriodsCheckBox.Checked);
    
        Info(message);

    // --------------------------------------------------------//
    
        // Convert StoreDataGranularity to correct TOM Property
        var StoreDataGranularity = RefreshGranularityType.Month;
        switch (storeDataComboBox.SelectedItem.ToString())
        {
            case "years":
                StoreDataGranularity = RefreshGranularityType.Year;
                break;
    
            case "quarters":
                StoreDataGranularity = RefreshGranularityType.Quarter;
                break;
    
            case "months":
                StoreDataGranularity = RefreshGranularityType.Month;
                break;
    
            case "days":
                StoreDataGranularity = RefreshGranularityType.Day;
                break; 
    
            default:
                Error ( "Bad selection for Incremental Granularity." );
                break;
        }
    
        // Convert RefreshDataGranularity to correct TOM Property
        var RefreshDataGranularity = RefreshGranularityType.Year;
        switch (refreshDataComboBox.SelectedItem.ToString())
        {
            case "years":
                RefreshDataGranularity = RefreshGranularityType.Year;
                break;
    
            case "quarters":
                RefreshDataGranularity = RefreshGranularityType.Quarter;
                break;
    
            case "months":
                RefreshDataGranularity = RefreshGranularityType.Month;
                break;
    
            case "days":
                RefreshDataGranularity = RefreshGranularityType.Month;
                break; 
    
            default:
                Error ( "Bad selection for Incremental Granularity." );
                break;
        }
    
        // Convert RefreshCompletePeriods checkbox to correct TOM property
        int RefreshCompletePeriods;
        if ( fullPeriodsCheckBox.Checked == true )
        { 
        RefreshCompletePeriods = -1;
        }
        else
        {
        RefreshCompletePeriods = 0;
        }


        // Set incremental window: period to be refreshed
        // -------------------------------------------------------//
        _Table.IncrementalGranularity = RefreshDataGranularity;
    
        // Default: 30 days - change # if you want
        _Table.IncrementalPeriods = Convert.ToInt16(storeDataTextBox.Text);
    
        // Only refresh complete days. Change to 0 if you don't want.
        _Table.IncrementalPeriodsOffset = RefreshCompletePeriods;
        
    
        // Set rolling window: period to be archived
        // -------------------------------------------------------//
        // Granularity = day, can change to month, quarter, year...
        _Table.RollingWindowGranularity = StoreDataGranularity;
    
        // Keep data for 1 year. Includes 1 full year and current partial year 
        //    i.e. if it is Nov 2023, keeps data from Jan 1, 2022. 
        //    On Jan 1, 2024, it will drop 2022 automatically.
        _Table.RollingWindowPeriods = Convert.ToInt16(refreshDataTextBox.Text);
        
    
        // If the selected date column is an integer of type YYYYMMDD...
        if ( Selected.Column.DataType == DataType.Int64 )
        {
            // Add DateTimeToInt Function
            var _DateTimeToInt = Model.AddExpression( 
                "fxDateTimeToInt", 
                @"(x as datetime) => 
Date.Year(x)    * 10000 + 
Date.Month(x)   * 100 + 
Date.Day(x)"
        );

        _DateTimeToInt.SetAnnotation("PBI_ResultType", "Function");
        _DateTimeToInt.Kind = ExpressionKind.M;

        // Source expression obtained from the original M partition
        _Table.SourceExpression = 

            // Gets expression before final "in" keyword
            _MExpression.Split("\nin")[0].TrimEnd() +

            // Adds comma and newline
            ",\n" +

            // Adds step called "Incremental Refresh" for filtering
            @"    #""Incremental Refresh"" = Table.SelectRows( " +

            // Gets name of last step (after "in" keyword)
            _MExpression.Split("\nin")[1].TrimStart() +

            // Adds 'each' keyword
            @", each " +

            // Bases incremental refresh on current column name
            Selected.Column.DaxObjectName +

            // Greater than or equal to RangeStart
            @" >= fxDateTimeToInt ( #""RangeStart"" ) and " +

            // and
            Selected.Column.DaxObjectName +

            // Less than RangeEnd
            @" < fxDateTimeToInt ( #""RangeEnd"" ) )" +

            // re-add 'in' keyword
            "\nin\n" +

            // Reference final step just added
            @"    #""Incremental Refresh""";
    }
    

        // Otherwise treat it like a normal date/datetime column
        else
        {
            // Source expression obtained from the original M partition
            _Table.SourceExpression = 
                // Gets expression before final "in" keyword
                _MExpression.Split("\nin")[0].TrimEnd() +
    
                // Adds comma and newline
                ",\n" +
                
                // Adds step called "Incremental Refresh" for filtering
                @"    #""Incremental Refresh"" = Table.SelectRows( " +
                
                // Gets name of last step (after "in" keyword)
                _MExpression.Split("\nin")[1].TrimStart() +
                
                // Adds 'each' keyword
                @", each " +
                
                // Bases incremental refresh on current column name
                Selected.Column.DaxObjectName +
                
                // Greater than or equal to RangeStart
                @" >= Date.From ( #""RangeStart"" ) and " +
                
                // and
                Selected.Column.DaxObjectName +
                
                // Less than RangeEnd
                @" < Date.From ( #""RangeEnd"" ) )" +
                
                // re-add 'in' keyword
                "\nin\n" +
                
                // Reference final step just added
                @"    #""Incremental Refresh""";
        }

        // Success message
        Info ( 
        "Successfully configured the Incremental Refresh policy.\n" + 
        "\nSelect the table and right-click on 'Apply Refresh Policy...'" + 
        "\nSelect & peform a 'Full Refresh' of all new policy partitons that are created." 
        );
        }
    else if (result == DialogResult.Cancel)
    {
        // if the user clicks the Cancel button, close the form and exit the script
        form.Close();
        Info ( "Cancelled configuration!" );
        return;
    }
}
```
### Explanation
This snippet will configure incremental refresh in the selected table based on a selected date column.

## Example Output
<br>
<img src="~/images/Cscripts/script-configure-incremental-refresh.png" alt="Image description" id="script-configure-incremental-refresh"/>
<script>
    var img = document.getElementById("script-configure-incremental-refresh");
    img.style.width = "500px";
</script>
<br>
<img src="~/images/Cscripts/script-configure-incremental-refresh-success.png" alt="Image description" id="script-configure-incremental-refresh-success"/>
<script>
    var img = document.getElementById("script-configure-incremental-refresh-success");
    img.style.width = "500px";
</script>