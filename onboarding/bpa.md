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

In order to add, remove or modify the rules applying to your model, use the "Tools > Manage BPA Rules..." menu option.

![image](https://user-images.githubusercontent.com/8976200/53632990-2f29fb80-3c0e-11e9-82fe-ee9c921662c7.png)

This UI contains two lists: The top list represents the **collections** of rules that are currently loaded. Selecting a collection in this list, will display all the rules that are defined within this collection in the bottom list. By default, three rule collections will show up:

* **Rules within the current model**: As the name indicates, this is the collection of rules that have been defined within the current model. The rule definitions are stored as an annotation on the Model object.
* **Rules for the local user**: These are rules that are stored in your `%AppData%\..\Local\TabularEditor\BPARules.json` file. These rules will apply to all models that are loaded in Tabular Editor by the currently logged in Windows user.
* **Rules on the local machine**: These rules are stored in the `%ProgramData%\TabularEditor\BPARules.json`. These rules will apply to all models that are loaded in Tabular Editor on the current machine.

If the same rule (by ID) is located in more than one collection, the order of precedence is from top to bottom, meaning a rule defined within the model takes precedence over a rule, with the same ID, defined on the local machine. This allows you to override existing rules, for example to take model specific conventions into account.

At the top of the list, you'll see a special collection called **(Effective rules)**. Selecting this collection will show you the list of rules that actually apply to the currently loaded model, respecting the precedence of rules with identical ID's, as mentioned above. The lower list will indicate which collection a rule belongs to. Also, you will notice that a rule will have its name striked out, if a rule with a similar ID exists in a collection of higher precedence:

![image](https://user-images.githubusercontent.com/8976200/53633831-74e7c380-3c10-11e9-925e-1419987f5a17.png)

## Adding additional collections
A new feature in Tabular Editor 2.8.1, is the possibility of including rules from other sources on a model. If, for example, you have a rules file located on a network share, you can now include that file as a rule collection in the current model. If you have write access to the location of the file, you'll also be able to add/modify/remove rules from the file. Rule collections that are added this way take precedence over rules that are defined within the model. If you add multiple such collections, you can shift them up and down to control their mutual precedence.

Click the "Add..." button to add a new rule collection to the model. This provides the following options:

![image](https://user-images.githubusercontent.com/8976200/53634211-7cf43300-3c11-11e9-8fed-7df113264a6f.png)

* **Create new Rule File**: This will create a new, empty, .json file at the specified location, which you can subsequently add rules to. When choosing the file, notice that there is an option for using relative file paths. This is useful when you want to store the rule file in the same code repository as the current model. However, please be aware that a relative rule file reference only works, when the model has been loaded from disk (since there is no working directory when loading a model from an instance of Analysis Services).
* **Include local Rule File**: Use this option if you already have a .json file containing rules, that you want to include in your model. Again, you have the option of using relative file paths, which may be beneficial if the file is located close to the model metadata. If the file is located on a network share (or generally, on a drive different than where the currently loaded model metadata resides), you can only include it using an absolute path.
* **Include Rule File from URL**: This option lets you specify an HTTP/HTTPS URL, that should return a valid rule definition (json). This is useful if you want to include rules from an online source, for example the [standard BPA rules](https://raw.githubusercontent.com/TabularEditor/BestPracticeRules/master/BPARules-standard.json) from the [BestPracticeRules GitHub site](https://github.com/TabularEditor/BestPracticeRules). Note that rule collections added from online sources will be read-only.

## Modifying rules within a collection
The lower part of the screen will let you add, edit, clone and delete rules within the currently selected collection, provided you have write access to the location where the collection is stored. Also, the "Move to..." button allows you to move or copy the selected rule to another collection, making it easy to manage multiple collections of rules.

## Adding rules

(WIP)

# Using the Best Practice Analyzer view

(WIP)