---
uid: accessibility
title: Accessibility
author: Morten Lønskov
updated: 2026-09-21
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Accessibility

This page collects the settings in Tabular Editor 3 that affect how readable and how operable the application is, and says what each one does. Most of them live under **Tools > Preferences > User Interface**.

## Color blindness mode

Tabular Editor uses color to tell you what changed. [Unsaved changes](xref:unsaved-changes) mark added objects green, deleted objects red and edited objects orange, and the model comparison view uses the same three.

Check **Color blindness mode** under **Tools > Preferences > User Interface**, in the **Accessibility** group. Added objects are then marked teal instead of green, which moves them onto a channel that can be seen, and leaves deleted and edited where they are, since those two were already far apart. The setting applies to the TOM Explorer and to the model comparison view, and it changes both the row tint and the badge on the object's icon.

The setting is off by default and is remembered per user.

## Keyboard access

Every action in Tabular Editor is reachable from the menus, and the menus are reachable from the keyboard. Commands you use often can be given a shortcut of your own under **Tools > Preferences > Keyboard**, which also lists the shortcuts already assigned.

See @shortcuts3 for the full list of default shortcuts.

## Text size and display scaling

Tabular Editor follows the display scaling set in Windows, so raising the scaling factor in **Settings > System > Display** enlarges the whole interface rather than only part of it.

The DAX, M, SQL and C# editors take their own font and size, under **Tools > Preferences > DAX Editor > General** and the equivalent pages for the other languages. Raising the editor font is usually a better first step than scaling the whole application, since expressions are where most reading happens.

## Themes and contrast

Tabular Editor ships several themes, including dark ones. Choose one under **Tools > Preferences > User Interface**, or from **Window > Theme**. See [Changing themes and palettes](xref:user-interface#changing-themes-and-palettes).

Themes change the application's own chrome. The syntax coloring inside the code editors is set separately, under **Tools > Preferences > DAX Editor**, so a dark theme and a light editor palette can be combined if that reads better for you.

## Language

The interface is available in several languages. Choose one under **Tools > Preferences > User Interface**, in the **Language** group. The setting takes effect after a restart. See @personalizing-te3.

## Reporting an accessibility problem

If something in Tabular Editor 3 is unusable for you, tell us: the settings above are the ones we have, and the list grows from what people report. Use **Help > Community Support**, or **Help > Dedicated Support** if your license includes it.
