---
uid: undo-redo
title: Undo/Redo support
author: Morten Lønskov
updated: 2026-09-16
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Undo/Redo support

Any change you make in Tabular Editor can be undone with **Ctrl+Z** and redone with **Ctrl+Y**. There's no limit to how many operations you can undo, but the stack is reset when you load a different model, whether from a file or from a database.

An operation that touches many objects undoes as one step. Dragging a display folder full of measures to a new parent, renaming a batch of objects, or applying a Best Practice Analyzer fix script each undo in a single **Ctrl+Z**.

## Eliminar objetos

Deleting an object also removes what depended on it. For a column, that means the relationships it takes part in, the hierarchy levels built on it, and its translations and perspective memberships. In Tabular Editor 3 it's also dropped from any calendars and variations that used it, and a _Sort by column_ pointing at it is cleared.

Undo restores the object _and_ everything that was removed alongside it, as one step.

Tabular Editor warns you before a delete that has consequences. Deleting a single object that other objects reference tells you so and asks you to confirm, naming what will happen:

- The object is referenced by other objects through DAX expressions, so those expressions will stop working.
- The column is used in one or more hierarchies, so the corresponding levels will be deleted.
- The column is used in one or more relationships, so those relationships will be removed.
- In Tabular Editor 3, the column is used in one or more calendars, so it will be removed from them.

Deleting several objects at once always asks for confirmation, though it doesn't itemise which object raises which concern.

A single object that nothing depends on is deleted without a prompt, on the grounds that undo is one keystroke away. If you would rather be asked every time, tick **Always show delete warnings** under **Tools > Preferences > TOM Explorer > Delete** in Tabular Editor 3.

> [!NOTE]
> Deleting an object doesn't rewrite the DAX that referenced it. The dependent expressions keep the now-dangling reference and are reported as errors in the @messages-view. This is different from renaming, where [formula fix-up](xref:formula-fix-up-dependencies) updates the referencing expressions for you.

## Undo and unsaved changes

In Tabular Editor 3, undo and the unsaved-change indicators work against the same reference point. Undoing back to the state the model was last saved in clears every indicator; redoing brings them back. Undoing _past_ the last save point makes indicators reappear for the objects that were rolled back.

**Revert** is the more direct tool when you want to discard a specific change rather than walk the undo stack back to it. It puts a single property, an object, a table or the whole model back to its last saved state in one undoable step, leaving every other unsaved edit alone. See @unsaved-changes.
