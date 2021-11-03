---
uid: bpa
title: Improve code quality with the Best Practice Analyzer
author: Daniel Otykier
updated: 2021-11-02
---

# Improve code quality with the Best Practice Analyzer

By now, you are probably already aware that the Tabular Object Model (TOM) is a relatively complex data structure, with many different types of objects and properties. It is not always clear what the best values to assign to these properties are, and many times it depends on specific use cases or model designs. Tabular Editor's **Best Practice Analyzer** continuously scans the TOM for violations of best practice rules that you can define. This helps you verify that object properties are always set to their ideal values.

Things you can check with the Best Practice Analyzer:

- **DAX Expressions** Create rules that warn you when certain DAX functions or constructs are used.
- **Formatting** Create rules that remind you to specify format strings, descriptions, etc.
- **Naming conventions** Create rules that check whether certain types of objects (e.g. key columns, hidden columns, etc.) follow certain name patterns.
- **Performance** Create rules that check various performance-related aspects of your model, for example to encourage reducing the number of calculated columns, etc.

The Best Practice Analyzer has access to the full metadata of the model, and can also access VertiPaq Analyzer statistics for more advanced scenarios.

> [!NOTE]
> Tabular Editor does not ship with any rules out-of-the-box. You will have to define your own rules initially, or use a set of standard rules such as [those recommended by the Power BI CAT Team](https://powerbi.microsoft.com/en-ca/blog/best-practice-rules-to-improve-your-models-performance/).

# Managing Best Practice Rules

In order to add, remove or modify rules applying to your model, use the "Tools > Manage BPA Rules..." menu option.

![Bpa Manager](~/images/bpa-manager.png)

This UI contains two lists: The top list represents the **collections** of rules that are currently loaded. Selecting a collection in this list, will display all the rules that are defined within this collection in the bottom list. When a model is loaded, you will see the following three rule collections:

* **Rules within the current model**: As the name indicates, this is the collection of rules that have been defined within the current model. The rule definitions are stored as an annotation on the Model object.
* **Rules for the local user**: These are rules that are stored in your `%LocalAppData%\TabularEditor3\BPARules.json` file. These rules will apply to all models that are loaded in Tabular Editor by the currently logged in Windows user.
* **Rules on the local machine**: These rules are stored in the `%ProgramData%\TabularEditor\BPARules.json`. These rules will apply to all models that are loaded in Tabular Editor on the current machine.

If the same rule (by ID) is located in more than one collection, the order of precedence is from top to bottom, meaning a rule defined within the model takes precedence over a rule, with the same ID, defined on the local machine. This allows you to override existing rules, for example to take model specific conventions into account.

At the top of the list, you'll see a special collection called **(Effective rules)**. Selecting this collection will show you the list of rules that actually apply to the currently loaded model, respecting the precedence of rules with identical ID's, as mentioned above. The lower list will indicate which collection a rule belongs to. Also, you will notice that a rule will have its name striked out, if a rule with a similar ID exists in a collection of higher precedence:

![Rule Overrides](~/images/rule-overrides.png)

## Adding additional collections
Rule collections can be added to a specific model. If you have a rules file located on a network share, you can include that file as a rule collection in the current model. If you have write access to the location of the file, you'll also be able to add/modify/remove rules from the file. Rule collections that are added this way take precedence over rules that are defined within the model. If you add multiple such collections, you can shift them up and down to control their mutual precedence.

Click the "Add..." button to add a new rule collection to the model. This provides the following options:

![Add Best Practice rule collection](~/images/add-rule-file.png)

* **Create new Rule File**: This will create a new, empty, .json file at a specified location, which you can subsequently add rules to. When choosing the file, notice that there is an option for using relative file paths. This is useful when you want to store the rule file in the same code repository as the current model. However, please be aware that a relative rule file reference only works, when the model has been loaded from disk (since there is no working directory when loading a model from an instance of Analysis Services).
* **Include local Rule File**: Use this option if you already have a .json file containing rules, that you want to include in your model. Again, you have the option of using relative file paths, which may be beneficial if the file is located close to the model metadata. If the file is located on a network share (or generally, on a drive different than where the currently loaded model metadata resides), you can only include it using an absolute path.
* **Include Rule File from URL**: This option lets you specify an HTTP/HTTPS URL, that should return a valid set of rules (in json format). This is useful if you want to include rules from an online source, for example the [standard BPA rules](https://raw.githubusercontent.com/TabularEditor/BestPracticeRules/master/BPARules-standard.json) from the [BestPracticeRules GitHub site](https://github.com/TabularEditor/BestPracticeRules). Note that rule collections added from online sources will be read-only.

## Modifying rules within a collection
The lower part of the screen will let you add, edit, clone and delete rules within the currently selected collection, provided you have write access to the location where the collection is stored. Moreover, the "Move to..." button allows you to move or copy the selected rule to another collection, making it easy to manage multiple collections of rules.

## Adding rules

To add a new rule to a collection, click on the **New rule...** button. This brings up the Best Practice Rule editor (see screenshot below).

![Bpa Rule Editor](~/images/bpa-rule-editor.png)

When creating a new rule, you must specify the following details:

- **Name**: The name of the rule, which will be displayed to users of Tabular Editor
- **ID**: An internal ID of the rule. Must be unique within a rule collection. If multiple rules have identical IDs across different collections, only the rule within the collection of the highest precedence is applied.
- **Severity**: The severity is not used within Tabular Editor's UI, but when running a Best Practice Analysis through [Tabular Editor's command line interface](xref:command-line-options), the number determines how "severe" a rule violation is.
  - 1 = Information only
  - 2 = Warning
  - 3 (or above) = Error
- **Category**: This is used for logically grouping rules together to make management of rules easier.
- **Description** (optional): Can be used to provide a description of what the rule is intended for. Will be shown in the Best Practice Analyzer view as a tooltip. You may use the following placeholder values within the description field, to provide a more contextual message:
  - `%object%` returns a fully qualified DAX reference (if applicable) to the current object
  - `%objectname%` returns only the name of the current object
  - `%objecttype%` returns the type of the current object
- **Applies to**: Select the type of object(s) to which the rule should apply.
- **Expression**: Type a [Dynamic LINQ](https://dynamic-linq.net/expression-language) search expression which should evaluate to `true` for those objects (among the object types selected in the **Applies to** dropdown) that violate the rule. The Dynamic LINQ expression can access the TOM properties available on the selected object types, as well as a wide range of standard .NET methods and properties.
- **Minimum compatibility level**: Some TOM properties are not available at all compatibility levels. If you are creating generic rules, use this dropdown to specify the minimum compatibility level of the models to which the rule should apply.

When a rule is saved to a rule collection on disk, all of the above properties are stored in a JSON format. You can add/edit/delete rules by editing the JSON file as well, which also allows you to specify the `FixExpression` property on a rule. This is a string that is used to generate a [C# script](xref:cs-scripts-and-macros) which will be applied to the model in order to fix the rule violation.

# Using the Best Practice Analyzer view

Tabular Editor displays the best practice rule violations within the **Best Practice Analyzer view**. You can also see the number of rule violations in the status bar at the bottom of the main window. To bring the view into focus, use the **View > Best Practice Analyzer** menu option or blick on the "# BP issues" button in the status bar.

![Best Practice Analyzer View](~/images/best-practice-analyzer-view.png)

The **Best Practice Analyzer view** shows a list of all rules that have objects in violation. Below each rule is a list of the violating objects. You can double-click on an object in the list, to navigate to that object in the **TOM Explorer**.

![Item options](~/images/bpa-options.png)

When right-clicking on an object, you are presented with a number of options as shown above. These are:

- **Go to object**: This is identical to double-clicking on an object, in order to navigate to that object in the **TOM Explorer**.
- **Ignore object**: This adds an annotation on the object, instructing the Best Practice Analyzer to ignore this particular rule on that object. Ignored rules are specified using their ID.
- **Generate fix script**: This option is available only if a rule has the `FixExpression` property specified. When choosing this option, Tabular Editor creates a new C# script based on the `FixExpression` of the selected rule(s).
- **Apply fix**: This option is available only if a rule has the `FixExpression` property specified. When choosing this option, Tabular Editor executes the `FixExpression` of the selected rule(s) in order to automatically fix the rule violation.

> [!NOTE]
> You can multi-select objects in the Best Practice Analyzer view, by holding down the Shift or Ctrl keys.

The options shown above are also available as toolbar buttons at the top of the **Best Practice Analyzer view**. In addition, there are buttons available for expanding/collapsing all items, showing ignored rules/objects and for performing a manual refresh (which is needed when background scans are disabled, see below).

# Disabling the Best Practice Analyzer

In some cases, you may want to disable the Best Practice Analyzer background scan. For example, when you have rules that take a relatively long time to evaluate, or when you are working with very large models.

The background scan can be disabled under **Tools > Preferences > Features > Best Practice Analyzer** by unchecking the **Scan for Best Practice violations in the background**.

Note that you can still manually perform a scan using the **Refresh** button of the **Best Practice Analyzer view**, as mentioned above, even when background scans are disabled.

# Next steps

- @cs-scripts-and-macros
- @personalizing-te3