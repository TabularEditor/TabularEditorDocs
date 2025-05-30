﻿---
uid: using-bpa
title: Using the Best Practice Analyzer
author: Morten Lønskov
updated: 2023-02-09
---

# Best Practice Analyzer

The Best Practice Analyzer (BPA) lets you define rules on the metadata of your model, to encourage certain conventions and best practices while developing your Power BI or Analysis Services Model.

## PBA Overview
The BPA overview shows you all the rules defined in your model that are currently being broken:

![BPA Overview](~/content/assets/images/common/BPAOverview.png)

And you will always be able to see in the main UI how many rules you are currently being broken.

![BPA Overview Line](~/content/assets/images/common/PBAOverviewMenuLine.png)

Clicking the link (or pressing F10), brings up the full BPA window.

> [!NOTE]
> If you are more into a video walk through then PowerBI.tips has a video with our own Daniel Otykier showing the Best Practice Analyzer in detail here: 
> [!Video https://www.youtube.com/embed/5WnN0NG2nBk]


### Functionality

Whenever a change is made to the model, the Best Practice Analyzer scans your model for issues in the background. You can disable this feature under File > Preferences.

The BPA Window in both TE2 and TE3 allows you to dock the window on one side of your desktop, while keeping the main window in the other side, allowing you to work with your model while you can see BPA issues.

The Best Practice Analyzer window continuously lists all the **effective rules** on your model as well as the objects that are in violation of each rule. Right-clicking anywhere inside the list or using the toolbar buttons at the top of the window, let's you perform the following actions:

* **Manage rules...**: This opens the Manage Rules UI, which we will cover below. This UI can also be accessed through the "Tools > Manage BPA Rules..." menu of the main UI.
* **Go to object...**: Choosing this option or double-clicking on an object in the list, takes you to the same object in the main UI.
* **Ignore item/items**: Selecting one or more objects in the list and choosing this option, will apply an annotation to the chosen objects indicating that the Best Practice Analyzer should ignore the objects going forward. If you ignored an object by mistake, toggle the "Show ignored" button at the top of the screen. This will let you unignore an object that was previously ignored.
* **Ignore rule**: If you've selected one or more rules in the list, this option will put an annotation at the model level that indicates, that the selected rule should always be ignored. Again, by toggling the "Show ignored" button, you can unignore rules as well.
* **Generate fix script**: Rules that have an easy fix (meaning the issue can be resolved simply by setting a single property on the object), will have this option enabled. By clicking, you will get a C# script copied into your clipboard. This script can then be subsequently pasted into the [Advanced Scripting](/Advanced-Scripting) area of Tabular Editor, where you can review it before executing it to apply the fix.
* **Apply fix**: This option is also available for rules than have an easy fix, as mentioned above. Instead of copying the script to the clipboard, it will be executed immediately.

## Managing Best Practice Rules
If you need to add, remove or modify the rules applying to your model, there's a specific UI for that. You can bring it up by clicking the top-left button on the Best Practice Analyzer window, or by using the "Tools > Manage BPA Rules..." menu item in the main window.

![BPA Manage Rules](~/content/assets/images/common/BPAOverviewManageRules.png)

The Manage BPA rules window contains two lists: The top list represents the **collections** of rules that are currently loaded. Selecting a collection in this list, will display all the rules that are defined within this collection in the bottom list.

![BPA Manage Rules UI](~/content/assets/images/common/PBAOverviewManageRulesPopUp.png)

### Rule Collections
 By default, three rule collections will show up:

 ### [Tabular Editor 3](#tab/TE3Rules) 
* **Rules within the current model**: As the name indicates, this is the collection of rules that have been defined within the current model. The rule definitions are stored as an annotation on the Model object.
* **Rules for the local user**: These are rules that are stored in your `%AppData%\..\Local\TabularEditor3\BPARules.json` file. These rules will apply to all models that are loaded in Tabular Editor by the currently logged in Windows user.
* **Rules on the local machine**: These rules are stored in the `%ProgramData%\TabularEditor3\BPARules.json`. These rules will apply to all models that are loaded in Tabular Editor on the current machine.

### [Tabular Editor 2](#tab/TE2Rules) 
* **Rules within the current model**: As the name indicates, this is the collection of rules that have been defined within the current model. The rule definitions are stored as an annotation on the Model object.
* **Rules for the local user**: These are rules that are stored in your `%AppData%\..\Local\TabularEditor\BPARules.json` file. These rules will apply to all models that are loaded in Tabular Editor by the currently logged in Windows user.
* **Rules on the local machine**: These rules are stored in the `%ProgramData%\TabularEditor\BPARules.json`. These rules will apply to all models that are loaded in Tabular Editor on the current machine.
***

#### Rule Precedence
If the same rule (by ID) is located in more than one collection, the order of precedence is from top to bottom, meaning a rule defined within the model takes precedence over a rule, with the same ID, defined on the local machine. This allows you to override existing rules, for example to take model specific conventions into account.

##### Effective Rules
At the top of the list, you'll see a special collection called **(Effective rules)**. Selecting this collection will show you the list of rules that actually apply to the currently loaded model, respecting the precedence of rules with identical ID's, as mentioned above. The lower list will indicate which collection a rule belongs to. Also, you will notice that a rule will have its name striked out, if a rule with a similar ID exists in a collection of higher precedence:

![BPA Manage Rules UI](~/content/assets/images/common/PBAOverviewManageRulesPopUpHigherPrecedence.png)

#### Adding additional collections
Tabular Editor provides the possibility of including rules from other sources on a model. If, for example, you have a rules file located on a network share, you can now include that file as a rule collection in the current model. If you have write access to the location of the file, you'll also be able to add/modify/remove rules from the file. Rule collections that are added this way take precedence over rules that are defined within the model. If you add multiple such collections, you can shift them up and down to control their mutual precedence.

Click the "Add..." button to add a new rule collection to the model. This provides the following options:

![BPA Manage Rules UI](~/content/assets/images/common/PBAOverviewManageRulesPopUpCreateNewRuleFile.png)

* **Create new Rule File**: This will create a new, empty, .json file at the specified location, which you can subsequently add rules to. When choosing the file, notice that there is an option for using relative file paths. This is useful when you want to store the rule file in the same code repository as the current model. However, please be aware that a relative rule file reference only works, when the model has been loaded from disk (since there is no working directory when loading a model from an instance of Analysis Services).
* **Include local Rule File**: Use this option if you already have a .json file containing rules, that you want to include in your model. Again, you have the option of using relative file paths, which may be beneficial if the file is located close to the model metadata. If the file is located on a network share (or generally, on a drive different than where the currently loaded model metadata resides), you can only include it using an absolute path.
* **Include Rule File from URL**: This option lets you specify an HTTP/HTTPS URL, that should return a valid rule definition (json). This is useful if you want to include rules from an online source, for example the [Microsoft standard BPA rules](https://raw.githubusercontent.com/microsoft/Analysis-Services/master/BestPracticeRules/BPARules.json) from the [BestPracticeRules GitHub site](https://github.com/microsoft/Analysis-Services/tree/master/BestPracticeRules). Note that rule collections added from online sources will be read-only.

#### Modifying rules within a collection
The lower part of the screen will let you add, edit, clone and delete rules within the currently selected collection, provided you have write access to the location where the collection is stored. Also, the "Move to..." button allows you to move or copy the selected rule to another collection, making it easy to manage multiple collections of rules. Please see our article with [samples of rule expressions ](/common/using-bpa-sample-rules-expressions.md) for more information on how to use that.

#### Rule Description Placeholders
You can use placeholder values within the Best Practice Rule's description. This provides more customizable descriptions that will appear as tooltips in the Best Practice UI:

* `%object%` returns a fully qualified DAX reference (if applicable) to the current object
* `%objectname%` returns only the name of the current object
* `%objecttype%` returns the type of the current object

![BPA Manage Rules UI](~/content/assets/images/common/BPAOverviewRuleDescriptionPlaceHolders.png)
