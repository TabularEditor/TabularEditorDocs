---
uid: cs-scripts-and-macros
title: Introduction to C# scripts and macros
author: Daniel Otykier
updated: 2021-11-03
---
# Introduction to C# scripts and macros

Any software that claims to improve your productivity should provide some means of **automating user interactions**. In Tabular Editor, you can write C# scripts for exactly this purpose. With C# scripts in Tabular Editor, you can, for example:

- Automate creation of TOM objects such as measures, tables, calculation items
- Interact with the currently selected object(s) in the TOM Explorer
- Automatically assign properties to multiple objects
- Import and export metadata in various formats, for auditing or documentation purposes

If a script modifies your model metadata, you will be able to view the modifications immediately in the TOM Explorer and the Properties view. Moreover, you can **undo script changes**, effectively rolling back the model metadata to the point before the script was executed. If a script fails execution, the changes are automatically rolled back by default.

Tabular Editor 3 includes a simple **script recorder** which helps you learn the syntax used, by incrementally adding lines of script code as you make changes to your model.

A script can be saved as a standalone file (`.csx` file extension), which can be shared among Tabular Editor users. In addition, a script can be stored as a reusable **macro**, which integrates the script more closely with Tabular Editors user interface.

# Creating a script

To create a new C# script, use the **File > New > C# Script** menu option. Note that this option is available even when no model is loaded in Tabular Editor.

For your first script, enter the following code:

```csharp
Info("Hello world!");
```

Hit F5 to run the code.

![Your very first script](~/assets/images/first-script.png)

If you made a mistake while typing the code, any syntax errors will be shown in the **Messages view**.

- To save the script as a file, simply hit **File > Save** (Ctrl+S).
- To open a script from a file, use the **File > Open > File...** (Ctrl+O) option. The Open File dialog will look for files with the `.cs` or `.csx` extensions by default.

# Using the script recorder

While a C# script is in focus, you can start the script recorder in Tabular Editor by using the **C# Script > Record script** menu option. While the script is recording, any change you make to your model metadata will cause additional lines of code to be added to the script. Note that you cannot edit the script manually until you stop the recording.

![Csharp Script Recorder](~/assets/images/csharp-script-recorder.png)

# Accessing model metadata

In order to access specific objects within the currently loaded model, you need to use the C# syntax for navigating through the Tabular Object Model (TOM) hierarchy. The root of this hierarchy is the `Model` object.

The script below outputs the name of the currently loaded model. If no model is loaded, a warning is displayed.

```csharp
if(Model != null)
    Info("The name of the current model is: " + Model.Name);
else
    Warning("No model is currently loaded!");
```

The `Model` object is a wrapper of the [Microsoft.AnalysisServices.Tabular.Model](https://msdn.microsoft.com/en-us/library/microsoft.analysisservices.tabular.model.aspx) class, exposing a subset of its properties, with some additional methods and properties for convenience.

To access a specific measure, you will need to know the name of that measure as well as the name of the table the measure resides in:

```csharp
var myMeasure = Model.Tables["Internet Sales"].Measures["Internet Total Sales"];
myMeasure.Description = "The formula for this measure is: " + myMeasure.Expression;
```

Line 1 in the script above locates the "Internet Total Sales" measure on the "Internet Sales" table, then stores a reference to that measure in the `myMeasure` variable.

Line 2 in the script sets the description of the measure, based on a hardcoded string and the (DAX) expression of the measure.

Tabular Editor can auto-generate the code that references a specific object, by dragging and dropping the object from the TOM Explorer into the C# script view.

![Generate an object reference by dragging](~/assets/images/generate-csharp-code.gif)

Most TOM objects (tables, columns, measures, etc.) in Tabular Editor, exposes the same set of properties that are available when using the AMO/TOM client libraries directly. For this reason, you can refer to [Microsoft's AMO/TOM documentation](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular?view=analysisservices-dotnet), to learn which properties are available. For example, [here](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.measure?view=analysisservices-dotnet#properties) is the documentation for available measure properties.

# Accessing current TOM Explorer selection

To make scripts reusable, it is rarely enough to be able to reference objects in the model directly by name, as shown above. Instead, it is useful to refer to whichever object(s) is currently selected in Tabular Editor's **TOM Explorer view**. This is possible through the use of the `Selected` object.

```csharp
Info("You have currently selected: " + Selected.Measures.Count + " measure(s).");
```

The `Selected` object by itself is a collection of all objects currently selected, including objects within selected display folders. In addition, the `Selected` object contains multiple properties that makes it easy to refer to specific object types, such as the `.Measures` property shown in the example above. In general, these properties exist in both a plural (`.Measures`) and a singular (`.Measure`) form. The former is a collection that you can iterate through, and which will be empty if the current selection does not contain any objects of that type, where as the latter is a reference to the currently selected object, if and only if exactly one of that type of object is selected.

The @useful-script-snippets article contains many examples of scripts that use the `Selected` object to perform various tasks.

# Interacting with the user

In the examples above, we used the `Info(...)` and `Warning(...)` global methods to show a message to the user in various flavors. Tabular Editor provides a number of these global methods as well as extension methods for showing and collecting information, and for various other common tasks. The most commonly used are listed below:

* `void Output(object value)` - halts script execution and displays detailed information about the provided object. When the provided object is a TOM object or a collection of TOM objects, a detailed view of all properties are shown.
* `void SaveFile(string filePath, string content)` - convenient way to save text data to a file.
* `string ReadFile(string filePath)` - convenient way to load text data from a file.
* `string ExportProperties(IEnumerable<ITabularNamedObject> objects, string properties = "...")` - convenient way to export a set of properties from multiple objects as a TSV string.
* `void ImportProperties(string tsvData)` - convenient way to load properties into multiple objects from a TSV string.
* `string ConvertDax(dax, useSemicolons)` - converts a DAX expression between US/UK and non-US/UK locales. If `useSemicolons` is true (default) the `dax` string is converted from the native US/UK format to non-US/UK. That is, commas (list separators) will be converted to semicolons and periods (decimal separators) will be converted to commas. Vice versa if `useSemicolons` is set to false.
* `void FormatDax(IEnumerable<IDaxDependantObject> objects, bool shortFormat, bool? skipSpace)` - formats DAX expressions on all objects in the provided collection
* `void FormatDax(IDaxDependantObject obj)` - queues an object for DAX expression formatting when script execution is complete, or when the `CallDaxFormatter` method is called.
* `void CallDaxFormatter(bool shortFormat, bool? skipSpace)` - formats all DAX expressions on objects enqueued so far
* `void Info(string message)` - Displays an informational message.
* `void Warning(string message)` - Displays a warning message.
* `void Error(string message)` - Displays an error message.
* `measure SelectMeasure(Measure preselect = null, string label = "...")` - Displays a list of all measures and �prompts the user to select one.
* `T SelectObject<T>(this IEnumerable<T> objects, T preselect = null, string label = "...") where T: TabularNamedObject` - Displays a list of the provided objects, prompting the user to select one, and returns that object (or null if the cancel button was pressed).
* `IList<T> SelectObjects<T>(this IEnumerable<T> objects, IEnumerable<T> preselect = null, string label = "...") where T: TabularNamedObject` - Displays a list of the provided objects, prompting the user to select any number of objects and returns the list of objects selected (or null if the cancel button was pressed).

# Saving a script as a macro

Scripts that you use often can be saved as reusabe macros, which are always available when you launch Tabular Editor. Moreover, macros are automatically integrated in the context menu of the **TOM Explorer view** and you can even use the **Tools > Customize...** option to add macros to existing or custom menus and toolbars.

To save a script as a macro, use the **C# Script > Save as Macro...** option.

![Save New Macro](~/assets/images/save-new-macro.png)

Provide a name for your macro. You can use backslashes to organize macros into folders, i.e. a name such as "My Macros\Test" will create a "My Macros" submenu in the context menu of the TOM Explorer, and within this submenu there will be a "Test" menu option that invokes the script.

You may also provide an optional tooltip which will be displayed when hovering over the menu option created by the macro.

You should also specify the macro context, which specifies the type(s) of objects that needs to be selected in order for the macro to be available in the context menu.

Lastly, you can specify a C# expression which should evaluate to true/false (typically based on the `Selected` or `Model` objects) under **Macro enabled condition (advanced)**. This lets you control more granularly whether the macro should be enabled or not, based on the current selection. For example, you could use the following expression:

```csharp
Selected.Measures.Count == 1
```

to enable your macro only when exactly 1 measure is selected.

# Managing macros

You can view all previously saved macros in the **Macros view**. To bring this view into focus, use the **View > Macros** menu option. This view allows you to:

- **Rename a macro** (simply put the cursor into the **Name** column and type the new name)
- **Delete a macro.** Select it and click the red "X" button above the list of macros.
- **Edit a macro.** Double-click the macro in the list (double-click on the "Id" column of the list). This will open the macro in a new C# script view, where you can make code changes. Hit Ctrl+S to save the code changes. If you need to edit other macro properties (tooltip, macro context, etc.), use the **C# Script > Edit Macro...** menu option.

# Next steps

- @personalizing-te3
- @boosting-productivity-te3

# Further reading

- @csharp-scripts
- @useful-script-snippets