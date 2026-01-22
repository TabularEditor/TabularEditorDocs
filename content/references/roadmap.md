---
uid: roadmap
title: Roadmap
author: Morten Lønskov
updated: 2025-10-29
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      full: true
---
# Tabular Editor 3 Roadmap

Below is an overview of major new features to be shipped with Tabular Editor 3 updates in the short- to long term:

# [Upcoming](#tab/upcoming)

## In Development

- **Semantic Bridge enhancements**: Support for v1.1 properties and enhanced import UI
- **Localization improvements**: Expanding language support and refining existing translations
- **Power Query (M) Auto-Formatting**: Advanced formatting capabilities for M expressions
- **Graphical Model Comparison**: See the changes that are applied to 

## Up Next

- AI Assistant in Tabular Editor
- .NET 10 Support
- Git integration
- Power Query (M) Editing Enhancements
- TOM Properties shown as TMDL and TMSL Scripts
- Standalone CLI application
- Built-in Macros

## Future

- DAX Debugger Filter Context visualizer
- Configurable Daxscilla autocomplete code snippets
- Configurable theming for code editors (syntax highlighting colors)
- Incremental deployment (a la [ALM Toolkit](http://alm-toolkit.com/))
- Macro Actions improvements such as automatic application across model and preferences for which to apply

# [Shipped](#tab/shipped)

For detailed information about each release, see the [full release history](xref:release-history).

## Shipped in 2026

✅ [**Localization**](xref:references-application-language) - Chinese, Spanish (Preview), Japanese, German, and French (Experimental) language support (v3.25.0)

✅ [**Built-in Best Practice Analyzer rules**](xref:built-in-bpa-rules) - Comprehensive set of BPA rules covering formatting, metadata, model layout, DAX expressions, and translations (v3.25.0)

✅ **Semantic Bridge** - Create semantic models from Databricks Metric Views (Enterprise Edition, v3.25.0)

✅ [**Save with supporting files for Fabric**](xref:save-with-supporting-files) - Support for .platform and definition.pbism files to match Fabric repository structure (v3.25.0)

✅ **Calendar Editor** - Enhanced UI for managing calendar objects for time intelligence (v3.25.0)

✅ [**Advanced Refresh dialog**](xref:advanced-refresh) - Configure parallelism, effective date for incremental refresh, and [refresh override profiles](xref:refresh-overrides) (Business/Enterprise Edition, v3.25.0)

## Shipped in 2025

✅ [**DAX Package Manager**](xref:dax-package-manager) - Find and install DAX packages from daxlib.org with a single click (v3.24.0)

✅ **UDF Namespaces** - Hierarchical organization of User-Defined Functions with customizable namespace properties (v3.24.0)

✅ **Visual Calculations improvements** - Enhanced DAX editor support for Visual Calculation functions and visual column references (v3.24.0)

✅ [**DAX User-Defined Functions (UDFs)**](xref:udfs) - Create and manage reusable DAX functions (v3.23.0)

✅ [**Calendars**](xref:calendars) - Calendar-based time intelligence features with enhanced UI (v3.23.0)

✅ **Fabric SQL Databases and Mirrored Databases support** - Import wizard support for new Fabric data sources in Import and Direct Lake modes (v3.23.0)

✅ [**Direct Lake on OneLake and SQL**](xref:direct-lake-guidance) - Full support for Direct Lake modes including mixed mode/hybrid models (Enterprise Edition, v3.22.0)

✅ **Word-based autocomplete** - DAX editor now supports multi-word search in autocomplete (v3.22.0)

✅ **Diagram view enhancements** - Column data type icons, bi-directional relationship indicators, and improved table display options (v3.21.0)

✅ **Copy TMDL scripts from TOM Explorer** - Export individual objects as TMDL to clipboard or file (v3.21.0)

✅ **DAX Optimizer RLS support** - View DAX Optimizer results for RLS and Calculation Item expressions (v3.21.0)

✅ **MetadataSource property** - New Model object property for C# scripts to access model metadata location (v3.21.0)

✅ **C# Editor improvements** - Enhanced code editing experience with better IntelliSense and flexible search

✅ **Native ARM64 builds** - Optimized performance on ARM64 processors (v3.23.0)

## Shipped in 2024
✅ DAX Debugger Locals Enhancement

✅ Full Direct Lake Integration

✅ DAX Optimizer Integration (Preview)

✅ .Net 8 migration

✅ Pivot Grid Enhancement

✅ DAX Query Enhancement

✅ TMDL GA Support

✅ Code Actions

✅ GA of DAX Optimizer Integration

✅ Data Refresh View Improvements

✅ Power Query (M) Highlighting

## Shipped in 2023
✅ TMDL Support as standard Save to Folder file format. (Depending on release of TMDL by Microsoft)

✅ Import Table Wizard support for Databricks (pending availability of REST endpoint for fetching metadata/schema)

✅ Metadata Translation Editor (view that can be opened when selecting one or more cultures, similar to the Tabular Translator tool)

✅ Perspective Editor (view that can be opened when selecting one or more perspectives, allowing you to check/uncheck objects visible in those perspectives)

✅ Improved Support for Oracle Databases

✅ Import Table Wizard support for Power BI datamarts (Use Datamart SQL Endpoint)

## Shipped in 2022

✅  DAX Debugger

✅  .NET 6 migration

✅  C# code assist (autocomplete, calltips, etc.)

✅  Import Table Wizard support for Snowflake

✅  Import Table Wizard support for Power BI dataflows

✅  Configurable hotkeys

✅  Support for DAX window functions

✅  Git integration (private preview)

## Shipped in 2021
✅  Import Table Wizard

✅  Portable Version

✅  Pivot Grid, Table Preview and DAX Query impersonation of a specific role or user, making it easy to test RLS/OLS

✅  DAX Script support for calculation groups and calculation items

✅  Offline DAX formatting

# Tabular Editor 2 Roadmap
> [!NOTE] 
>Tabular Editor 2 is no longer under active development and will not receive any major feature additions or improvements from our side. We are, however, committed to keeping it up-to-date, ensuring support for new semantic modelling features as they are released from Microsoft, and also fixing any critical or blocking issues. As the project is open-source under MIT, anyone is welcome to submit pull requests, which will be reviewed and approved by our team.