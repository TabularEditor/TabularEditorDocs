---
uid: formula-fix-up-dependencies
title: Formula Fix-up and Formula Dependencies
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Formula Fix-up and Formula Dependencies
Tabular Editor continuously parses the DAX expressions of all measures, calculated columns and calculated tables in your model, to construct a dependency tree of these objects. This dependency tree is used for the Formula Fix-up functionality, which may be enabled under **Tools > Preferences** (**File > Preferences** in Tabular Editor 2). Formula Fix-up automatically updates the DAX expression of any measure, calculated column or calculated table, whenever an object that was referenced in the expression is renamed.

To visualize the dependency tree, right-click the object in the explorer tree and choose "Show dependencies..."

![image](~/content/assets/images/formula-fixup-dependencies-01.png)