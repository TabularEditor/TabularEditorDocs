---
uid: dax-script-introduction
title: Using the DAX Scripting feature
author: Daniel Otykier
updated: 2021-10-08
applies_to:
  editions:
    - edition: Desktop
    - edition: Business
    - edition: Enterprise
---
# Using the DAX Scripting feature

In the [previous article](xref:creating-and-testing-dax), you learned how to add and edit calculated objects such as measures, calculated columns, etc. in your model.

As your model grows in complexity, you may reach a point in which it starts to become cumbersome to navigate the TOM Explorer or jump back and forth between measures, when authoring and maintaining business logic. It is not uncommon to have long chains of dependencies between measures, and so for that reason, it is sometimes useful to collect all the DAX code making up the business logic, in a single document.

This is exactly the purpose of the new **DAX script** feature introduced in Tabular Editor 3.

To use this feature, locate the measures for which you would like to generate a single document, in the TOM Explorer. Multi-select the measures, then right-click and choose **Script DAX**. A new document is created, containing the definition of all the selected measures. You can also generate a DAX script for all measures within a table or all measures within the model, by choosing the table or model object respectively.

![Dax Script](~/images/dax-script.png)

Editing objects through a DAX script is slightly different than editing through the **Expression Editor**. With the latter, changes are applied immediately when you navigate to a different object. In a DAX script, however, changes are not applied until you explicitly do so by using the **Script > Apply** (F5) option. If you are connected to an instance of Analysis Services, you can use the **Script > Apply & Sync** (SHIFT+F5) option to simultaneously apply the changes and save the updated model metadata to Analysis Services.

# DAX Scripting capabilities

Tabular Editor 3 supports editing the following types of objects using a DAX script:

- Measures (including KPIs)
- Calculated columns
- Calculated tables
- Calculation groups (including calculation items)

# DAX script syntax

The basic syntax for DAX scripts is the following:

```dax
MEASURE 'Table name'[Measure name] = <DAX expression> [<Property list>]
COLUMN 'Table name'[Column name] = <DAX expression> [<Property list>]
TABLE 'Table name' = <DAX expression> [<Property list>]
```

(WIP)