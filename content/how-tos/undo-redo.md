---
uid: undo-redo
title: Undo/Redo support
author: Morten Lønskov
updated: 2026-09-23
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---
# Undo/Redo support

Press **Ctrl+Z** to undo a change and **Ctrl+Y** to redo it. The undo stack has no size limit and is cleared when you load another model, from a file or from a database. An operation that changes many objects, such as a folder drag, a batch rename or a Best Practice Analyzer (BPA) fix, is one undo step.

## Deleting objects

Deleting an object also removes what depends on it. For a column, Tabular Editor removes:

- relationships that use the column
- hierarchy levels based on the column
- its translations and perspective memberships
- in Tabular Editor 3, its entries in calendars and variations

In Tabular Editor 3, it also clears the `SortByColumn` property of columns sorted by the deleted column.

Undo restores the object and its dependents in one step.

If other objects depend on the single object you delete, a confirmation dialog lists the consequences:

- If DAX expressions reference the object, those expressions stop working.
- If the column is used in hierarchies, the corresponding levels are deleted.
- If the column is used in relationships, those relationships are removed.
- In Tabular Editor 3, if the column is used in calendars, it's removed from them.

Deleting several objects at once always shows a confirmation dialog, but the dialog doesn't list the consequences per object.

If a single object has no dependents, it's deleted without a prompt. In Tabular Editor 3, select **Always show delete warnings** in the **Delete** section under **Tools > Preferences > Tabular Editor > TOM Explorer** to confirm every delete.

> [!NOTE]
> Deleting an object doesn't rewrite the DAX that references it. The dependent expressions keep the reference and are reported as errors in the @messages-view. When you rename an object, [formula fix-up](xref:formula-fix-up-dependencies) updates the expressions that reference it.

## Undo and unsaved changes

In Tabular Editor 3, the unsaved-change indicators track the undo stack. Undoing back to the last saved state clears every indicator, and redoing shows them again. Undoing beyond the last save shows indicators on the objects that were rolled back.

**Revert** discards one change and keeps later ones. It restores a property, object, table or the whole model to its last saved state while your other unsaved changes stay in place, and you can undo a revert. See @unsaved-changes.
