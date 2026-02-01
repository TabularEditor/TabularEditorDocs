---
uid: undo-redo
title: Undo/Redo support
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---
## Undo/Redo support
Any change you make in Tabular Editor can be undone using CTRL+Z and subsequently redone using CTRL+Y. There is no limit to the number of operations that can be undone, but the stack is reset when you open a Model.bim file or load a model from a database.

When deleting objects from the model, all translations, perspectives and relationships that reference the deleted objects are also automatically deleted (whereas Visual Studio normally shows an error message that the object cannot be deleted). If you make a mistake, you can use the Undo functionality to restore the deleted object, which will also restore any translations, perspectives or relationships that were deleted. Note that even though Tabular Editor can detect [DAX formula dependencies](), Tabular Editor will not warn you in case you delete a measure or column which is used in the DAX expression of another measure or calculated column.