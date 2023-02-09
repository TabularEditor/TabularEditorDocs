---
uid: using-bpa-sample-rules-expressions
title: Sample Rules Expression
author: Daniel Otykier
updated: 2023-02-09
---
#  Rule Expression Samples
In this section, you'll see some examples of Dynamic LINQ expressions that can be used to define rules. The expression that is entered in the Rule Expression Editor, will be evaluated whenever focus leaves the textbox, and any syntax errors will be shown on top of the screen:

![image](https://cloud.githubusercontent.com/assets/8976200/25380170/9f01634e-29af-11e7-952e-e10a1f28df32.png)

Your rule expressions may access any public properties on the objects in the TOM. If you try to access a property that does not exist on that type of object, an error will also be shown:

![image](https://cloud.githubusercontent.com/assets/8976200/25381302/798bab98-29b3-11e7-931e-789e5286fc45.png)

"Expression" does not exist on the "Column" object, but if we switch the dropdown to "Calculated Columns", the statement above works fine:

![image](https://cloud.githubusercontent.com/assets/8976200/25380451/87b160da-29b0-11e7-8e2e-c4e47593007d.png)

Dynamic LINQ supports all the standard arithmetic, logical and comparison operators, and using the "."-notation, you can access subproperties and -methods of all objects.

```
String.IsNullOrWhitespace(Expression) and not Name.StartsWith("Dummy")
```

The above statement, applied to Calculated Columns, Calculated Tables or Measures, flags those that have an empty DAX expression unless the object's name starts with the text "Dummy".

Using LINQ, we can also work with collections of objects. The following expression, applied to tables, will find those that have more than 10 columns which are not organized in Display Folders:

```
Columns.Count(DisplayFolder = "") > 10
```

Whenever we use a LINQ method to iterate over a collection, the expression used as an argument to the LINQ method is evaluated on the items in the collection. Indeed, DisplayFolder is a property on columns that does not exist at the Table level.

Here, we see this rule in action on the Adventure Works tabular model. Note how the "Reseller" table shows up as being in violation, while the "Reseller Sales" does not show up (columns in the latter have been organized in Display Folders):

![image](https://cloud.githubusercontent.com/assets/8976200/25380809/d9d1c3a4-29b1-11e7-839e-29450ad39c8a.png)

To refer to the parent object inside a LINQ method, use the special "outerIt" syntax. This rule, applied to tables, will find those that contain columns whose name does not start with the table name:

```
Columns.Any(not Name.StartsWith(outerIt.Name))
```

It would probably make more sense to apply this rule to Columns directly, in which case it should be written as:

```
not Name.StartsWith(Table.Name)
```

To compare against enumeration properties, simply pass the enumerated value as a string. This rule, will find all columns whose name end with the word "Key" or "ID", but where the SummarizeBy property has not been set to "None":

```
(Name.EndsWith("Key") or Name.EndsWith("ID")) and SummarizeBy <> "None"
```

## Finding unused objects
When building Tabular Models it is important to avoid high-cardinality columns at all costs. Typical culprits are system timestamps, technical keys, etc. that have been imported to the model by mistake. In general, we should make sure that the model only contains columns that are actually needed. Wouldn't it be nice if the Best Practice Analyzer could tell us which columns are likely not needed at all?

The following rule will report columns that:

- ...are hidden (or whose parent table is hidden)
- ...are not referenced by any DAX expressions (considers all DAX expressions in the model - even drillthrough and RLS filter expressions)
- ...do not participate in any relationships
- ...are not used as the "Sort By"-column of any other column
- ...are not used as levels of a hierarchy.

The Dynamic LINQ expression for this BPA rule is:

```
(IsHidden or Table.IsHidden)
and ReferencedBy.Count = 0 
and (not UsedInRelationships.Any())
and (not UsedInSortBy.Any())
and (not UsedInHierarchies.Any())
``` 

The same technique can be used to find unused measures. It's a little simpler, since measures can't participate in relationships, etc. So instead, let's spice things up a bit, by also considering whether any downstream objects that reference a given measure, are visible or not. That is, if measure [A] is referenced by measure [B], and both measure [A]Â and [B] are hidden, and no other DAX expressions refer to these two measures, we should let the developer know that it is safe to remove both of them:

```
(IsHidden or Table.IsHidden)
and not ReferencedBy.AllMeasures.Any(not IsHidden)
and not ReferencedBy.AllColumns.Any(not IsHidden)
and not ReferencedBy.AllTables.Any(not IsHidden)
and not ReferencedBy.Roles.Any()
```

## Fixing objects
In some cases, it is possible to automatically fix the issues on objects satisfying the criteria of a rule. For example when it's just a matter of setting a simple property on the object. Take a closer look at the JSON behind the following rule:

```json
{
    "ID": "FKCOLUMNS_HIDDEN",
    "Name": "Hide foreign key columns",
    "Category": null,
    "Description": "Columns used on the Many side of a relationship should be hidden.",
    "Severity": 1,
    "Scope": "Column",
    "Expression": "Model.Relationships.Any(FromColumn = outerIt) and not IsHidden and not Table.IsHidden",
    "FixExpression": "IsHidden = true",
    "Compatibility": [
      1200,
      1400
    ],
    "IsValid": false
}
```

This rule finds all columns that are used in a relationship (on the "Many"/"From" side), but where the column or its parent table are not hidden. It is recommended that such columns are never shown, as users should filter data using the related (dimension) table instead. So the fix in this case, would be to set the columns IsHidden property to true, which is exactly what the "FixExpression" string above does. To see this in action, right-click any objects that violate the rule, and choose "Generate Fix Script". This puts a small script into the clipboard, which can be pasted into the Advanced Script Editor, from where you can easily review the code and execute it:

![image](https://cloud.githubusercontent.com/assets/8976200/25298489/9035bab6-26f5-11e7-8134-8502daaf4132.png)

Remember that you can always undo (CTRL+Z) changes done to a model after script execution.
