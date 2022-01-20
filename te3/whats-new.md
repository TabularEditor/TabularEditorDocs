---
uid: whats-new
title: What's new in Tabular Editor 3
author: Daniel Otykier
updated: 2021-06-01
---
# What's new in Tabular Editor 3?

(The following section assumes that you are somewhat familiar with the open-source Tabular Editor 2).

Tabular Editor 3 adds the following features that are not available in the open-source version:

- UI overhaul
  - Visual Studio-like, fully customizable shell
  - Theming support (dark mode!)
  - Hi-DPI and multi-monitor support
- New, super-powerful DAX Editor
  - Powered by Scintilla (SciTe, Notepad++, etc.)
  - Many Code Assist features (aka. "IntelliSense")
  - Offline syntax and semantic checking and highlighting
  - **Roadmap:** Configurable hotkeys and color schemes
  - DAX debugging
- Full offline metadata analysis with syntax and semantic checking
  - Metadata automatically inferred for calculated objects, without being connected to AS
  - Messages view that displays all DAX errors/warnings and allows you to quickly navigate to the code that has issues
- Find/replace dialog box
  - Allows you to display all find results in a window to quickly navigate between objects
  - Supports RegEx, backslash expressions and Dynamic LINQ searches
- Diagram view
  - Easily navigate large models, including only tables that are related to the table you're looking at
  - Easily add/edit relationships
  - Save/load diagrams to files
  - **Roadmap:** Save/load diagrams to model annotations
- DAX Scripting
  - Edit multiple measures in a single script
  - Supports editing various measure properties (DisplayFolder, Description, IsHidden, KPIs, etc.) in addition to the DAX expression itself
  - Support for calculated tables and calculated columns
  - Support for calculation groups/items
- Macro recorder (C# aka. "Advanced Scripting")
  - Scripts can be saved as reusable macros (aka. "custom actions") that are fully customizable with the rest of the UI shell
- New connected features:
  - Workspace Mode (simultaneously synchronize model metadata to disk AND to analysis services)
  - Table Preview (infinite scrolling on tables in import mode, filtering/sorting supported in both import and DirectQuery mode)
  - DAX Query Editor
  - Pivot Grid view (drag and drop columns/measures from TOM explorer)
  - Async Data Refresh
  - VertiPaq Analyzer (also allows you to import an existing vpax file when working offline)
- Power Query support
  - Load column metadata from tables that use Power Query partitions
  - **Roadmap:** Power Query editor with IntelliSense<sup>TM</sup>-like features

In addition to the features listed above, Tabular Editor 3 will have full feature parity with Tabular Editor 2.

# Next steps

- @editions
- [Overview of Tabular Editor 3's User Interface](xref:user-interface)
- @security-privacy
- @preferences
- [Tabular Editor 3 Onboarding Guide](xref:onboarding-te3)