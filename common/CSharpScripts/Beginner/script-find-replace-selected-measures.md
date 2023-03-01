---
uid: script-find-replace
title: Find/Replace Measure DAX
author: Kurt Buhler
updated: 2023-03-01
applies_to:
  versions:
    - version: 2.x
    - version: 3.x
---
# Edit Hidden Partitions

## Script Purpose
Will find & replace a substring in the selected measures' DAX expression. I.e. if you want to replace `'Customers'[Key Account]` with `'Products'[Type]` in many measures. 
An input box lets the user enter the text to find and a subsequent input lets the user define the replacement text.

## Script

```csharp
// Use this script to find & replace in all the DAX expressions of the selected measures

using System.Text.RegularExpressions;
using System.Windows.Forms;

// ---------------------------------------------------------------------//
// CONFIG
// Replace Selected.Measures with Model.AllMeasures to scan all measures
var _measures = Selected.Measures; // Model.AllMeasures;
// Replace _m.Expression with _m.Name to find & replace in names.
// ---------------------------------------------------------------------//

// Initialize _find and _replace string variables
string _find = "Find";
string _replace = "Replace";

// WinForms prompt to get Find & Replace input
using (Form prompt = new Form())
{
    // Prompt config
    prompt.Width = 350;
    prompt.Height = 180;
    prompt.Text = "Find and Replace Dialog";
    prompt.StartPosition = FormStartPosition.CenterScreen;

    // Set the AutoScaleMode property to Dpi
    prompt.AutoScaleMode = AutoScaleMode.Dpi;

    // Find / Replace input positions & config
    Label findLabel = new Label() { Left = 20, Top = 20, Text = "Find:" };
    TextBox findBox = new TextBox() { Left = findLabel.Right + 20, Top = 20, Width = 150 };
    Label replaceLabel = new Label() { Left = 20, Top = 60, Text = "Replace:" };
    TextBox replaceBox = new TextBox() { Left = replaceLabel.Right + 20, Top = 60, Width = 150 };
    Button okButton = new Button() { Text = "OK", Left = 20, Width = 75, Top = 100 };
    Button cancelButton = new Button() { Text = "Cancel", Left = 100, Width = 75, Top = 100 };

    // Buttons
    okButton.Click += (sender, e) => { _find = findBox.Text; _replace = replaceBox.Text; prompt.DialogResult = DialogResult.OK; };
    cancelButton.Click += (sender, e) => { prompt.DialogResult = DialogResult.Cancel; };

    prompt.AcceptButton = okButton;
    prompt.CancelButton = cancelButton;

    prompt.Controls.Add(findLabel);
    prompt.Controls.Add(findBox);
    prompt.Controls.Add(replaceLabel);
    prompt.Controls.Add(replaceBox);
    prompt.Controls.Add(okButton);
    prompt.Controls.Add(cancelButton);

    // The user clicked OK, so perform the find-and-replace logic
    if (prompt.ShowDialog() == DialogResult.OK)
        {
            
            int _occurrences = 0;
            var _ReplacedList = new List<string>();
    
            foreach (var _m in _measures)
                {
                    if (_m.Expression != _m.Expression.Replace(_find, _replace))
                        {
                            try
                                {
                                    // Count number of occurrences of _find substring in the string
                                    string _pattern = Regex.Escape(_find);
                                    _occurrences = Regex.Matches(_m.Expression, _pattern).Count;
                                }
                            catch
                                {
                                    // If it's not found there are 0 occurrences
                                    _occurrences = 0;
                                }
            
                            // Perform the Find/Replace
                            _m.Expression = _m.Expression.Replace(_find, _replace);
                            _ReplacedList.Add(_m.DaxObjectName);
                        }
                }
    
            // Create a list of all the measures replaced
            string _Replaced = _ReplacedList.Count > 0
                ? "\n\nMeasures with Replacements:\n • " + string.Join("\n • ", _ReplacedList)
                : "";
    
            // Return a success Info box pop-up
            Info(
                "Replaced " + 
                _occurrences + 
                " occurrences of '" + 
                _find + 
                "' with '" + 
                _replace + 
                "'" + 
                _Replaced);
        }
    else
        {
            Error("Find/Replace cancelled!");
        }
}

```
### Explanation
This snippet will create a pop-up dialogue with WinForms that will let you input a substring to search the selected measures and replace with a different substring. A success box dialogue will inform you that the find/replace was successful.

### Example Output
<br>
<img src="~/images/Cscripts/script-find-replace-dialogue.png" alt="Image description" id="script-find-replace-dialogue">
<script>
    var img = document.getElementById("script-find-replace-dialogue");
    img.style.width = "400px";
</script>

<br>
<img src="~/images/Cscripts/script-find-replace-success.png" alt="Image description" id="script-find-replace-success">
<script>
    var img = document.getElementById("script-find-replace-success");
    img.style.width = "400px";
</script>