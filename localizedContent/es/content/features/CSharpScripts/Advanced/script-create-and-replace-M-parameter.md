---
uid: script-create-and-replace-parameter
title: Crear un parámetro M (reemplazo automático)
author: Kurt Buhler
updated: 2023-02-28
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      full: true
---

# Crear un nuevo parámetro M y agregarlo a las particiones M existentes

## Propósito del script

Si quieres reemplazar una cadena en las particiones M del modelo (por ejemplo, la cadena de conexión, la condición de filtro, el nombre de una columna, etc.) por el valor de un parámetro. <br></br>

> [!NOTE]
> Este script solo funciona con parámetros del tipo de datos `string`.
> Para otros tipos de datos, modifica los tipos de las variables y el valor del parámetro según corresponda. <br></br>

## Script

### Crear un nuevo parámetro M y agregarlo a las particiones M existentes

```csharp
// Este script crea un nuevo parámetro M como una 'expresión compartida'.
// También buscará el valor predeterminado en todas las particiones M y lo reemplazará por el nombre del objeto del parámetro.
//#r "System.Drawing"

using System.Drawing;
using System.Text.RegularExpressions;
using System.Windows.Forms;

// Ocultar el control giratorio de 'Running Macro'
ScriptHelper.WaitFormVisible = false;

// Inicializar variables
string _ParameterName = "New Parameter";
string _ParameterValue = "ParameterValue";

// Cuadro de diálogo de WinForms para obtener el nombre/valor del parámetro
using (Form prompt = new Form())
{
    Font formFont = new Font("Segoe UI", 11); 

    // Configuración del cuadro de diálogo
    prompt.AutoSize = true;
    prompt.MinimumSize = new Size(380, 120);
    prompt.Text = "Crear nuevo parámetro M";
    prompt.StartPosition = FormStartPosition.CenterScreen;

    // Buscar: etiqueta
    Label parameterNameLabel = new Label() { Text = "Escribe el nombre:" };
    parameterNameLabel.Location = new Point(20, 20);
    parameterNameLabel.AutoSize = true;
    parameterNameLabel.Font = formFont;

    // Cuadro de texto para introducir el texto de la subcadena
    TextBox parameterNameBox = new TextBox();
    parameterNameBox.Width = 200;
    parameterNameBox.Location = new Point(parameterNameLabel.Location.X + parameterNameLabel.Width + 20, parameterNameLabel.Location.Y - 4);
    parameterNameBox.SelectedText = "New Parameter";
    parameterNameBox.Font = formFont;

    // Reemplazar: etiqueta
    Label parameterValueLabel = new Label() { Text = "Escribe el valor:" };
    parameterValueLabel.Location = new Point(parameterNameLabel.Location.X, parameterNameLabel.Location.Y + parameterNameLabel.Height + 20);
    parameterValueLabel.AutoSize = true;
    parameterValueLabel.Font = formFont;

    // Cuadro de texto para introducir el texto de la subcadena
    TextBox parameterValueBox = new TextBox() { Left = parameterValueLabel.Right + 20, Top = parameterValueLabel.Location.Y - 4, Width = parameterNameBox.Width };
    parameterValueBox.SelectedText = "Parameter Value";
    parameterValueBox.Font = formFont;

    // Botón Aceptar
    Button okButton = new Button() { Text = "Crear", Left = 20, Width = 75, Top = parameterValueBox.Location.Y + parameterValueBox.Height + 20 };
    okButton.MinimumSize = new Size(75, 25);
    okButton.AutoSize = true;
    okButton.Font = formFont;

    // Botón Cancelar
    Button cancelButton = new Button() { Text = "Cancelar", Left = okButton.Location.X + okButton.Width + 10, Top = okButton.Location.Y };
    cancelButton.MinimumSize = new Size(75, 25);
    cancelButton.AutoSize = true;
    cancelButton.Font = formFont;

    // Acciones de los botones
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

    // El usuario hizo clic en Aceptar, así que se ejecuta la lógica de buscar y reemplazar
    if (prompt.ShowDialog() == DialogResult.OK)
    {

        // Crea el parámetro
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
        
        
        // Informa al usuario de que el parámetro se creó correctamente
        Info ( 
            "Se creó correctamente un nuevo parámetro: " + @"""" +
            _ParameterName + @"""" +
            "\nValor predeterminado: " + @"""" +
            _ParameterValue + @"""");
        
        
        // Busca el valor predeterminado del parámetro en las particiones M y lo reemplaza por el nombre del parámetro
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
        
                        // Lleva el control de qué particiones M se reemplazaron (y cuántas)
                        _NrReplacements = _NrReplacements + 1;
                        _ReplacementsList.Add( _p.Name );
                    }
        
                // Cuenta el total de particiones M
                _NrMPartitions = _NrMPartitions + 1;
                }
            }
        }
        
        
        // Crea una lista con viñetas de todas las particiones M que se reemplazaron
        string _ReplacedPartitions = " • " + String.Join("\n • ", _ReplacementsList );
        
        
        // Informa 
        //      - Si la búsqueda y el reemplazo se realizaron correctamente
        //      - Cuántas particiones M se reemplazaron
        //      - En qué particiones M se aplicó la búsqueda y el reemplazo
        Info (
            "Se reemplazó correctamente\n\n " +
            _Find + 
            "\n\n por: \n\n" + 
            _Replace + 
            "\n\n en " + 
            Convert.ToString(_NrReplacements) +
            " de " +
            Convert.ToString(_NrMPartitions) +  
            " particiones M:\n" +
            _ReplacedPartitions
        );

    }
    else
    {
    Error ( "Entrada cancelada. El script finalizó sin cambios.");
    }
}
```

### Explicación

Este fragmento abre un cuadro de diálogo para que el usuario introduzca el nombre y el valor del parámetro y, después, crea el parámetro como una 'expresión compartida' en el modelo.
Luego buscará el valor predeterminado en todas las particiones M y lo reemplazará por `#"ParameterName"`.

## Ejemplo de salida

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-create-m-parameter.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 1:</strong> El cuadro de diálogo emergente que aparece al ejecutar el script y solicita el nombre y el valor del parámetro.</figcaption>
</figure>

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-create-parameter-auto-replace.png" alt="Data Security Create Role" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 2:</strong> Cuadro de diálogo de confirmación que muestra que se ha creado el parámetro y que la subcadena de valor correspondiente se ha reemplazado en todas las expresiones de las particiones M. Para parámetros de otros tipos, ajusta el código C# según corresponda.</figcaption>
</figure>