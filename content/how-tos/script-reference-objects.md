---
uid: scripting-referencing-objects
title: Scripting/referencing objects
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

## Scripting/referencing objects
You can use drag-and-drop functionality, to script out objects in the following ways:

* Drag one or more objects to another Windows application (text editor or SSMS)
JSON code representing the dragged object(s) will be created. When dragging the Model node, a Table, a Role or a Data Source, a "createOrReplace" script is created.

* Dragging an object (measure, column or table) into the DAX expression editor, will insert a fully-qualified DAX-reference to the object in question.

* Dragging an object to the Advanced Script editor, will insert the C# code necessary to access the object through the TOM tree.