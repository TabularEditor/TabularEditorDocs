---
uid: advanced-filtering-explorer-tree
title: Advanced Object Filtering
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      partial: true
---

# Advanced Object Filtering

This article describes how to use the "Filter" textbox within Tabular Editor - an incredibly useful feature when navigating complex models.

## Filtering Mode
As of [2.7.4](https://github.com/TabularEditor/TabularEditor/releases/tag/2.7.4), Tabular Editor now lets you decide how the filter should apply to objects in the hierarchy, and how search results are displayed. This is controlled using the three right-most toolbar buttons next to the Filter button:

![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-01.png)

* ![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-02.png) **Hierarchical by parent**: The search will apply to _parent_ objects, that is Tables and Display Folders (if those are enabled). All child items will be displayed, when a parent item matches the search criteria.
* ![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-03.png) **Hierarchical by children**: The search will apply to _child_ objects, that is Measures, Columns, Hierarchies, etc. Parent objects will only be displayed if they have at least one child object matching the search criteria.
* ![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-04.png) **Flat**: The search will apply to all objects, and results will be displayed in a flat list. Objects that contain child items will still display these in a hierarchical manner.

## Simple search
Type anything into the Filter textbox and hit [Enter] to do a simple case-insensitive search within object names. For example, typing "sales" in the Filter textbox, using the "By Parent" filtering mode, will produce the following results:

![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-05.png)

Expanding any of the tables will reveal all measures, columns, hierarchies and partitions of the table. If we change the filtering mode to "By Child", the results will look like this:

![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-06.png)

Notice how the "Employee" table now appears in the list, since it has a couple of child items (columns in this case), that contain the word "sales".

## Wildcard search
When typing in a string in the Filter textbox, you can use the wildcard `?` to denote any single character, and `*` to denote any sequence of characters (zero or more). So typing `*sales*` would produce exactly the same results as shown above, however typing `sales*` will only show objects whose name _starts_ with the word "sales" (again, this is case-insensitive).

Searching for `sales*` by parent:

![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-07.png)

Searching for `sales*` by child:

![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-08.png)

Flat search for `sales*` (toggle info columns [Ctrl]+[F1] to show detailed information about each object):

![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-09.png)

Wildcards can be placed anywhere in the string, and you can include as many as you need. If that's not complex enough, read on...

## Dynamic LINQ search
You can also use [Dynamic LINQ](https://github.com/kahanu/System.Linq.Dynamic/wiki/Dynamic-Expressions) to search for objects, which is the same thing you do when creating [Best Practice Analyzer rules](xref:best-practice-analyzer). To enable Dynamic LINQ mode in the filter box, simply put a `:` (colon) in front of your search string. For example, to view all objects whose name end with "Key" (case-sensitive) write:

```
:Name.EndsWith("Key")
```

...and hit [Enter]. In "Flat" filtering mode, the result looks like this:

![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-10.png)

For case-insensitive search in Dynamic LINQ, you can either convert the input string using something like:

```
:Name.ToUpper().EndsWith("KEY")
```

or you can supply the [StringComparison](https://docs.microsoft.com/en-us/dotnet/api/system.string.endswith?view=netframework-4.7.2#System_String_EndsWith_System_String_System_StringComparison_) argument, like:

```
:Name.EndsWith("Key", StringComparison.InvariantCultureIgnoreCase)
```

You are not restricted to searching within the names of objects. Dynamic LINQ search strings can be as complex as you like, to evaluate any property (as well as sub-properties) of an object. So if you want to find all objects having an expression that contains the word "TODO", you would use the following search filter:

```
:Expression.ToUpper().Contains("TODO")
```

As another example, the following will display all hidden measures in the model that are not referenced by anything else:

```
:ObjectType="Measure" and (IsHidden or Table.IsHidden) and ReferencedBy.Count=0
````

You can also use Regular Expressions. The following will find all columns whose name contains the word "Number" OR "Amount":

```
:ObjectType="Column" and RegEx.IsMatch(Name,"(Number)|(Amount)")
```

Note, that the display options (the toolbar buttons directly above the tree), may affect the results when using "By Parent" and "By Child" filtering mode. For example, the above LINQ filter only returns columns, but if your display options are currently set to not show columns, nothing will be displayed.
