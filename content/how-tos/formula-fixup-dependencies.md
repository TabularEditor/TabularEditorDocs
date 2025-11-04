## Formula Fix-up and Formula Dependencies
Tabular Editor continuously parses the DAX expressions of all measures, calculated columns and calculated tables in your model, to construct a dependency tree of these objects. This dependency tree is used for the Formula Fix-up functionality, which may be enabled under "File" > "Preferences". Formula Fix-up automatically updates the DAX expression of any measure, calculated column or calculated table, whenever an object that was referenced in the expression is renamed.

To visualize the dependency tree, right-click the object in the explorer tree and choose "Show dependencies..."

![image](https://cloud.githubusercontent.com/assets/8976200/22482528/b37d27e2-e7f9-11e6-8b89-c503f9fffcac.png)