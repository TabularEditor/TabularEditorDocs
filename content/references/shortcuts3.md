---
uid: shortcuts3
title: Keyboard shortcuts Tabular Editor 3
author: Daniel Otykier
updated: 2021-09-08
applies_to:
  editions:
    - edition: Desktop
    - edition: Business
    - edition: Enterprise
---
# Keyboard shortcuts

## General

|Command|Shortcut|
|---|---|
|New model|Ctrl+N|
|Open file|Ctrl+O|
|Load model from a database|Ctrl+Shift+O|
|Save current item|Ctrl+S|
|Save all|Ctrl+Shift+S|
|Exit|Alt+F4|
|Deployment wizard|Ctrl+Shift+D|

## Edit

|Command|Shortcut|
|---|---|
|Select All|Ctrl+A|
|Copy|Ctrl+C|
|Cut|Ctrl+X|
|Paste|Ctrl+V|
|Undo|Ctrl+Z|
|Redo|Ctrl+Y|
|Find|Ctrl+F|
|Replace|Ctrl+H|

## Data modelling

|Command|Shortcut|
|---|---|
|Properties|F4|
|Edit object name / batch rename|F2|
|Batch rename children|Shift+F2|
|View dependencies|Shift+F12|
|Make invisible|Ctrl+I|
|Make visible|Ctrl+U|
|Create measure|Alt+1|
|Create calculated column|Alt+2|
|Create hierarchy|Alt+3|
|Create data column|Alt+4|
|Create table|Alt+5|
|Create calculated table|Alt+6|
|Create calculation group|Alt+7|
|Accept expression change|F5|

## TOM Explorer

|Command|Shortcut|
|---|---|
|Navigate up or down|Up / Down arrow|
|Expand / collapse current node|Right / Left arrow|
|Expand / collapse current node and all subnodes|Ctrl+Right / Left arrow|
|Expand / collapse entire tree|Ctrl+Shift+Right / Left arrow|
|Toggle measures|Ctrl+1|
|Toggle columns|Ctrl+2|
|Toggle hierarchies|Ctrl+3|
|Toggle partitions|Ctrl+4|
|Toggle display folders|Ctrl+5|
|Toggle hidden objects|Ctrl+6|
|Toggle info columns|Ctrl+7|
|Navigate back|Alt+Left arrow|
|Navigate forward|Alt+Right arrow|

## Text/code editing (general)

|Command|Shortcut|
|---|---|
|Cut line|Ctrl+L|
|Delete line|Ctrl+Shift+L|
|Copy line|Ctrl+Shift+T|
|Transpose lines|Ctrl+T|
|Duplicate line|Ctrl+D|
|Lowercase line|Ctrl+U|
|Uppercase line|Ctrl+Shift+U|
|Move lines up|Alt+Up arrow|
|Move lines down|Alt+Down arrow|

## DAX code

|Command|Shortcut|
|---|---|
|Go to definition|F12|
|Peek definition|Alt+F12]
|Refactor|Ctrl+R|
|Show auto-complete|Ctrl+Space|
|Show calltip|Ctrl+Shift+Space|
|Format DAX|F6|
|Format DAX (Short lines)|Ctrl+F6|
|Comment lines|Ctrl+K|
|Uncomment lines|Ctrl+U|
|Toggle comments|Ctrl+/|
|Collapse all foldable regions|Ctrl+Alt+[|
|Expand all foldable regions|Ctrl+Alt+]|
|Toggle all foldable regions state|Ctrl+Alt+;|
|Collapse foldable region|Ctrl+Shift+[|
|Expand  foldable region|Ctrl+Shift+]|
|Toggle foldable region state|Ctrl+Shift+;|
|Delete reference or words|Ctrl+Backspace or Ctrl+Delete|
|Expand Selection|Ctrl+Shift+E|

## DAX Query

|Command|Shortcut|
|---|---|
|Execute query|F5|
|Execute selection|Shift+F5|

## DAX Script

|Command|Shortcut|
|---|---|
|Apply script|F5|
|Apply selection|F8|
|Apply script and save model|Shift+F5|
|Apply selection and save model|Shift+F8|

## DAX Debugger

|Command|Shortcut|
|---|---|
|Step over|F10|
|Step back|Shift+F10|
|Step in|F11|
|Step out|Shift+F11|
|Next row (innermost row context)|F9|
|Previous row (innermost row context)|Shift+F9|

## C# Script

|Command|Shortcut|
|---|---|
|Run script|F5|

# Customizing Shortcuts

Tabular Editor 3 allows for the customization of shortcuts by rebinding existing or adding new shortcuts.

Setting shortcuts can be done through **Tools -> Preferences -> Keyboard** and locating the command that should have a shortcut binding and setting the binding in the menu. 
Shortcuts can be set for many different parts of Tabular Editor 3 including [Macros](xref:creating-macros) to have C# scripts available at the fingertips. 

![Dax Script](~/content/assets/images/SetShortcuts.png)

1. Keyboard Menu in Preferences
2. Find command that should have a shortcut
3. Set shortcut by holding desired shortcuts key and use "Assign Shortcut"