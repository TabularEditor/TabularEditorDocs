---
uid: script-create-and-replace-parameter
title: M Parameter erstellen (Automatische Ersetzung)
author: Kurt Buhler
updated: 2023-02-28
applies_to:
  versions:
    - version: 3.x
---

# Neuen M Parameter erstellen und zu vorhandenen M Partitionen hinzufügen

## Skriptzweck

Wenn Sie eine Zeichenfolge in Model M Partitionen ersetzen möchten (z. B. Verbindungszeichenfolge, Filterbedingung, Spaltenname usw.) mit einem Parameterwert. <br></br>

> [!NOTE]
> Dieses Skript funktioniert nur mit Parametern vom Datentyp `string`.
> Für andere Datentypen ändern Sie bitte die Variablentypen und den Parameterwert entsprechend. <br></br>

## Skript

### Neuen M Parameter erstellen und zu vorhandenen M Partitionen hinzufügen

```csharp
// Dieses Skript erstellt einen neuen M Parameter als 'Shared Expression'.
// Es findet auch den Standardwert in allen M Partitionen und ersetzt ihn durch den Namen des Parameterobjekts.
//#r "System.Drawing"

using System.Drawing;
using System.Text.RegularExpressions;
using System.Windows.Forms;

// Spinfeld 'Makro wird ausgeführt' ausblenden
ScriptHelper.WaitFormVisible = false;

// Variablen initialisieren
string _ParameterName = "New Parameter";
string _ParameterValue = "ParameterValue";

// WinForms-Eingabeaufforderung zum Eingeben von Parameternamen / Wert
using (Form prompt = new Form())
{
    Font formFont = new Font("Segoe UI", 11); 

    // Eingabeaufforderung konfigurieren
    prompt.AutoSize = true;
    prompt.MinimumSize = new Size(380, 120);
    prompt.Text = "Neuen M Parameter erstellen";
    prompt.StartPosition = FormStartPosition.CenterScreen;

    // Suchen: Bezeichnung
    Label parameterNameLabel = new Label() { Text = "Namen eingeben:" };
    parameterNameLabel.Location = new Point(20, 20);
    parameterNameLabel.AutoSize = true;
    parameterNameLabel.Font = formFont;

    // Textfeld zur Eingabe des Substring-Texts
    TextBox parameterNameBox = new TextBox();
    parameterNameBox.Width = 200;
    parameterNameBox.Location = new Point(parameterNameLabel.Location.X + parameterNameLabel.Width + 20, parameterNameLabel.Location.Y - 4);
    parameterNameBox.SelectedText = "Neuer Parameter";
    parameterNameBox.Font = formFont;

    // Ersetzen: Bezeichnung
    Label parameterValueLabel = new Label() { Text = "Wert eingeben:" };
    parameterValueLabel.Location = new Point(parameterNameLabel.Location.X, parameterNameLabel.Location.Y + parameterNameLabel.Height + 20);
    parameterValueLabel.AutoSize = true;
    parameterValueLabel.Font = formFont;

    // Textfeld zur Eingabe des Substring-Texts
    TextBox parameterValueBox = new TextBox() { Left = parameterValueLabel.Right + 20, Top = parameterValueLabel.Location.Y - 4, Width = parameterNameBox.Width };
    parameterValueBox.SelectedText = "Parameterwert";
    parameterValueBox.Font = formFont;

    // Schaltfläche OK
    Button okButton = new Button() { Text = "Erstellen", Left = 20, Width = 75, Top = parameterValueBox.Location.Y + parameterValueBox.Height + 20 };
    okButton.MinimumSize = new Size(75, 25);
    okButton.AutoSize = true;
    okButton.Font = formFont;

    // Schaltfläche Abbrechen
    Button cancelButton = new Button() { Text = "Abbrechen", Left = okButton.Location.X + okButton.Width + 10, Top = okButton.Location.Y };
    cancelButton.MinimumSize = new Size(75, 25);
    cancelButton.AutoSize = true;
    cancelButton.Font = formFont;

    // Schaltflächenaktionen
    okButton.Click += (sender, e) => { _ParameterName = parameterNameBox.Text; _ParameterValue = parameterValueBox.Text; prompt.DialogResult = DialogResult.OK; };
    cancelButton.Click += (sender, e) => { prompt.DialogResult = DialogResult.Cancel; };

    prompt.AcceptButton = okButton;
    prompt.CancelButton = cancelButton;

    prompt.Controls.Add(parameterNameLabel);
    prompt.Controls.Add(parameterNameBox);
    prompt.Controls.Add(parameterValueLabel);
    prompt.Controls.Add(parameterValueBox);
    prompt.Controls.Add(okButton);
    prompt.Controls.Add(cancelButton);

    // Der Benutzer hat auf OK geklickt, daher wird die Such- und Ersetzungslogik ausgeführt
    if (prompt.ShowDialog() == DialogResult.OK)
    {

        // Erstellt den Parameter
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
        
        
        // Informiert den Benutzer, dass der Parameter erfolgreich erstellt wurde
        Info ( 
            "Parameter erfolgreich erstellt: " + @"""" +
            _ParameterName + @"""" +
            "\nStandardwert: " + @"""" +
            _ParameterValue + @"""");
        
        
        // Findet den Standardwert des Parameters in M Partitionen und ersetzt ihn durch den Parameternamen
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
        
                        // Verfolgt, welche M Partitionen ersetzt wurden (und wie viele)
                        _NrReplacements = _NrReplacements + 1;
                        _ReplacementsList.Add( _p.Name );
                    }
        
                // Zählt die Gesamtzahl der M Partitionen
                _NrMPartitions = _NrMPartitions + 1;
                }
            }
        }
        
        
        // Erstellt eine Aufzählungsliste aller M Partitionen, die ersetzt wurden
        string _ReplacedPartitions = " • " + String.Join("\n • ", _ReplacementsList );
        
        
        // Informiert 
        //      - Ob die Such- und Ersetzung erfolgreich war
        //      - Wie viele M Partitionen ersetzt wurden
        //      - Welche M Partitionen mit der Such- und Ersetzung durchgeführt wurden
        Info (
            "Erfolgreich ersetzt\n\n " +
            _Find + 
            "\n\n mit: \n\n" + 
            _Replace + 
            "\n\n in " + 
            Convert.ToString(_NrReplacements) +
            " von " +
            Convert.ToString(_NrMPartitions) +  
            " M Partitionen:\n" +
            _ReplacedPartitions
        );

    }
    else
    {
    Error ( "Eingabe abgebrochen! Skript ohne Änderungen beendet.");
    }
}
```

### Erklärung

Dieser Codeausschnitt öffnet ein Dialogfeld, in dem der Benutzer den Parameternamen und den Wert eingeben kann, und erstellt dann den Parameter als 'Shared Expression' im Modell.
Anschließend werden alle M Partitionen nach dem Standardwert durchsucht und durch `#"ParameterName"` ersetzt.

## Beispielausgabe

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-create-m-parameter.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Abbildung 1:</strong> Das Popup-Dialogfeld, das beim Ausführen des Skripts angezeigt wird und zur Eingabe des Parameternamens und Werts auffordert.</figcaption>
</figure>

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-create-parameter-auto-replace.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Abbildung 2:</strong> Bestätigungsdialog, der zeigt, dass der Parameter erstellt wurde und die entsprechende Wertteilzeichenfolge in allen M Partitionsausdrücken ersetzt wurde.</figcaption> Passen Sie für Parameter anderer Typen den C#-Code entsprechend an.</figcaption>
</figure>