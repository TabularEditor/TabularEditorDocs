---
uid: preferences
title: Controlling preferences
author: Daniel Otykier
updated: 2026-01-12
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

# Tabular Editor 3 Preferences

Tabular data model development processes and workflows differ greatly from organization to organization. To ensure that the tool can fit into as many of these workflows as possible, Tabular Editor 3 is highly customizable - not just in terms of the user interface's look and feel, but also on more advanced topics such as web proxies, updates and feedback, row limits, timeouts, schema compare preferences, etc.

This article describes the Tabular Editor 3 Preferences dialogs and the settings that you can control through it.

To access the preferences dialog, go to **Tools > Preferences**.

> [!NOTE]
> All Tabular Editor preferences are stored for each Windows user profile, in the `%localappdata%\TabularEditor3` folder. It is possible to migrate your settings to another machine by simply copying the contents of this folder.

> [!TIP]
> Use the search box at the top of the Preferences dialog to quickly find specific settings.

## Tabular Editor > Features

![Pref General Features](~/content/assets/images/pref-general-features.png)

### Power BI

##### _Allow unsupported editing_ (disabled)

This option is only relevant when Tabular Editor 3 is used as an external tool for Power BI Desktop. When checked, all TOM data modeling properties are available for editing when connected to an instance of Power BI Desktop. It's generally recommended to leave this unchecked, to make sure that you do not accidentally make changes to your Power BI file, [that are not supported by Power BI Desktop](xref:desktop-limitations).

##### _Hide auto date/time warnings_ (disabled)

When checked, warnings about Power BI auto date/time tables will be suppressed. These warnings appear when the "Auto date/time" setting in Power BI Desktop is enabled, which creates calculated tables that trigger warnings in Tabular Editor 3's built-in DAX analyzer.

##### _Line break on first line of DAX_ (disabled)

In Power BI Desktop it is common to insert a line break on the first line of a DAX expression, due to the way the formula bar displays the DAX code. If you often switch back and forth between Tabular Editor and Power BI Desktop, consider enabling this option to have Tabular Editor 3 insert the line break automatically.

##### _Default Power BI authentication mode_ (Integrated)

Select the default authentication method (Integrated, ServicePrincipal, or MasterUser) to use when connecting to Power BI datasets.

### Metadata Synchronization

These settings control the behavior of Tabular Editor 3 when model metadata is loaded from a database on an instance of Analysis Services. The settings specify how Tabular Editor 3 should deal with metadata changes applied to the database from outside the application.

##### _Warn when local metadata is out-of-sync with deployed model_ (enabled)

When checked, an information bar is displayed inside Tabular Editor, whenever you have made local changes to the model that have not yet been saved to Analysis Services. For example, if you're wondering why a DAX query or a Pivot Grid does not produce the expected result, this could be due to a measure expression being changed in Tabular Editor without saving the change to Analysis Services. The bar disappears when you hit save (Ctrl+S).

##### _Track external model changes_ (enabled)

Just like Power BI Desktop can detect when an external tool makes a change to the data model, so too can Tabular Editor. This option is only relevant for local instances of Analysis Services (i.e. msmdsrv.exe processes running on the same machine as Tabular Editor). When checked, Tabular Editor starts a trace on Analysis Services and notifies you if external changes are made.

##### _Refresh local Tabular Object Model metadata automatically_ (enabled)

When the tracing mechanism as described above is enabled, this option allows Tabular Editor to automatically refresh the model metadata when an external change is detected. This is useful if you often switch back and forth between Power BI Desktop and Tabular Editor 3.

##### _Cleanup orphaned Tabular Editor traces_

Normally, Tabular Editor 3 should automatically stop and remove any AS traces started due to the settings above. However, if the application was shut down prematurely, the traces may never be stopped. By clicking this button, all AS traces started by any instance of Tabular Editor will be removed.

> [!NOTE]
> The cleanup button is only available when Tabular Editor is connected to an instance of Analysis Services.

### Best Practice Analyzer

##### _Scan for Best Practice violations in the background_ (enabled)

If unchecked, you will have to explicitly run a Best Practice Analysis from inside the Best Practice Analyzer tool window, to view if there are any violations. If checked, the scan happens continuously on a background thread whenever changes are made. For very large models, or models with very complex Best Practice rules, this may cause issues.

##### _Built-in BPA rules_ (enabled for new users)

Choose whether to enable, disable, or be prompted about using Tabular Editor's built-in Best Practice Analyzer rules. The built-in rules cover key best practices across formatting, metadata, model layout, DAX expressions, and translations. New installations will have built-in rules enabled by default.

### DAX Formula Fix-up

##### _Enable formula fix-up_ (enabled)

Automatically adjusts references in DAX expressions when objects are renamed or moved. This feature ensures that your DAX code remains valid when you reorganize your model.

##### _Enable formula fix-up on paste_ (enabled)

Automatically adjusts references in DAX expressions when pasting objects. This is useful when copying measures or calculated columns between tables or models.

### Direct Lake

##### _Auto-refresh on save_ (enabled)

Automatically refresh Direct Lake tables when saving changes to ensure data is current. This ensures that your Direct Lake model stays in sync with the underlying data source.

## Tabular Editor > Updates and Feedback

![Placeholder: Screenshot of Updates and Feedback preferences page]

##### _Check for updates on start-up_ (enabled)

When checked, Tabular Editor will check for new versions when the application starts. This ensures you stay up to date with the latest features and bug fixes.

##### _Check for major updates only_ (disabled)

When checked, only major version updates will trigger notifications. Minor and patch updates will be ignored.

##### _Help improve Tabular Editor by collecting anonymous usage data_ (enabled)

Data does not contain any personally identifiable information, nor any information about the structure or content of your data models. If you would still like to opt out of telemetry, uncheck this.

##### _Send error reports_ (enabled)

In cases of crashes, Tabular Editor displays an option for sending a crash report when this is checked. Crash reports are very helpful when debugging, so please leave this checked if you don't mind!

## Tabular Editor > Deployment

![Placeholder: Screenshot of Deployment preferences page]

Configure which types of objects are deployed by default when using the deployment wizard:

##### _Deploy data sources_ (disabled)

Include data source definitions when deploying. Enable this if you want data source connection strings and settings to be deployed along with your model changes.

##### _Deploy partitions_ (disabled)

Include partition definitions when deploying. Enable this if you want partition configurations to be deployed along with your model changes.

##### _Deploy refresh policy partitions_ (disabled)

Include incremental refresh policy partitions when deploying. This controls whether partitions created by incremental refresh policies are deployed.

##### _Deploy model roles_ (disabled)

Include role definitions when deploying. Enable this if you want Row-Level Security (RLS) and Object-Level Security (OLS) roles to be deployed.

##### _Deploy model role members_ (disabled)

Include role member assignments when deploying. Enable this if you want user and group assignments to security roles to be deployed.

##### _Deploy shared expressions_ (disabled)

Include shared expressions (M expressions) when deploying. Enable this if you want Power Query shared expressions to be deployed.

### Deployment Metadata

##### _Annotate deployment metadata_ (disabled)

Add deployment timestamp and user information as annotations on deployed objects. This can be useful for tracking when and by whom model changes were deployed.

### Backup Settings

##### _Backup on save_ (enabled)

Create a backup of the model when saving changes locally. This provides a safety net in case you need to revert changes.

##### _Save backup location_

Specify the folder where save backups are stored. By default, backups are not created unless a location is specified.

##### _Backup on deploy_ (enabled)

Create a backup of the target model before deploying changes. This allows you to restore the previous version if needed.

##### _Backup location_

Specify the folder where deployment backups are stored. By default, backups are not created unless a location is specified.

## Tabular Editor > Defaults

![Placeholder: Screenshot of Defaults preferences page]

##### _New model compatibility level_ (1600)

Set the default compatibility level for newly created models. Compatibility level 1600 corresponds to SQL Server 2022 and Power BI.

##### _Use latest compatibility level as default_ (enabled)

Automatically use the latest available compatibility level for new models. When enabled, this overrides the specific compatibility level setting above.

##### _New models use workspace database_ (enabled)

When creating a new model, automatically create a workspace database on Analysis Services. This allows you to immediately test and query your model during development.

##### _Default save mode_ (AlwaysAsk)

Choose whether to always save as a file (.bim), folder (multiple JSON files), TMDL (Tabular Model Definition Language), or always ask when saving. Options: AlwaysAsk, File, Folder, TMDL.

##### _Use PBIX file name when saving to disk_ (enabled)

When saving a model loaded from a PBIX file, use the PBIX filename as the default. This maintains naming consistency between Power BI files and saved model metadata.

##### _Create user options for new models_ (enabled)

Automatically create .tmuo (Tabular Model User Options) files for new models. These files store user-specific settings like diagram layouts and window positions.

## Tabular Editor > Keyboard

![Keyboard mappings](~/content/assets/images/keyboard-mappings.png)

Configure keyboard shortcuts for all Tabular Editor commands. Use the search functionality to quickly find specific commands and assign or modify their keyboard shortcuts to match your preferred workflow.

## Tabular Editor > TOM Explorer View

![Tom Explorer Settings](~/content/assets/images/tom-explorer-settings.png)

Control which objects and properties are visible in the TOM (Tabular Object Model) Explorer:

##### _Display folders_ (enabled)

Show or hide display folder groupings. When enabled, objects are organized into their display folder hierarchy.

##### _Hidden objects_ (disabled)

Show or hide objects marked as hidden in the model. Enable this if you need to work with hidden tables, columns, or measures.

##### _All object types_ (enabled)

Show all object types in the explorer tree. When disabled, only the most common object types are shown.

##### _Sort alphabetically_ (enabled)

Sort objects alphabetically instead of by creation order. This makes it easier to find specific objects in large models.

##### _Show measures_ (enabled)

Display measures in the explorer tree.

##### _Show columns_ (enabled)

Display columns in the explorer tree.

##### _Show hierarchies_ (enabled)

Display hierarchies in the explorer tree.

##### _Show partitions_ (enabled)

Display partitions in the explorer tree.

##### _Show metadata information_ (disabled)

Display additional metadata properties in tooltips and property grid. This includes information like lineage tags, creation timestamps, and other technical metadata.

##### _Show full branch_ (disabled)

When filtering the TOM Explorer, by default Tabular Editor 3 shows all items in the hierarchy that matches the filter string, including their parents. If you want to see all child items as well (even though these might not match the filter string), enable this option.

##### _Always show delete warnings_ (disabled)

If you prefer Tabular Editor 3 to prompt you to confirm all object deletions, enable this setting. Otherwise, Tabular Editor 3 will only prompt you to confirm multi-object deletions, or deletions of objects that are referenced by other objects.

> [!NOTE]
> All delete operations in Tabular Editor 3 can be undone by hitting CTRL+Z.

### Column Preferences

Configure which columns are visible in multi-column views and their display order.

## Tabular Editor > Copy/Paste

![Placeholder: Screenshot of Copy/Paste preferences page]

Control what metadata is included when copying objects:

##### _Include translations_ (enabled)

Copy translation metadata with objects. When enabled, any translations defined for the copied object will also be copied.

##### _Include perspectives_ (enabled)

Copy perspective membership with objects. When enabled, the copied object will belong to the same perspectives as the original.

##### _Include RLS_ (enabled)

Copy Row-Level Security expressions with objects. This applies when copying tables that have RLS rules defined.

##### _Include OLS_ (enabled)

Copy Object-Level Security settings with objects. This applies when copying objects that have OLS restrictions.

## Tabular Editor > Perspectives

![Placeholder: Screenshot of Perspectives preferences page]

Control how perspective membership is handled:

##### _Inherit perspective membership for new objects_ (disabled)

Newly created objects automatically inherit perspective membership from their parent. For example, a new measure would automatically be added to the same perspectives as its parent table.

##### _Inherit perspective membership for relocated objects_ (disabled)

Objects that are moved inherit perspective membership from their new parent. This is useful when reorganizing your model structure.

##### _Inherit when adding table to perspective_ (enabled)

Automatically add all table objects (columns, measures, hierarchies) when a table is added to a perspective.

##### _Inherit when removing table from perspective_ (enabled)

Automatically remove all table objects when a table is removed from a perspective.

## Tabular Editor > Schema Compare

![Placeholder: Screenshot of Schema Compare preferences page]

Configure which changes are ignored during schema comparison when updating table schemas:

##### _Ignore Import mode changes_ (disabled)

Don't flag changes to Import mode properties. Enable this if you want to ignore changes between Import, DirectQuery, and Dual modes during schema comparison.

##### _Ignore data type changes_ (disabled)

Don't flag column data type changes. Enable this if you want to ignore data type changes during schema comparison.

##### _Ignore description changes_ (disabled)

Don't flag changes to object descriptions. Enable this if you don't want to see description changes in the schema comparison.

##### _Ignore decimal to double changes_ (disabled)

Don't flag changes between decimal and double data types. This is useful when working with data sources that don't distinguish between these types.

##### _Prioritize Analysis Services schema detector_ (disabled)

Use Analysis Services metadata as the source of truth for schema detection. When enabled, Tabular Editor will query the Analysis Services instance directly instead of using the data source provider's schema information.

## Tabular Editor > Save to Folder/File

![Placeholder: Screenshot of Save to Folder preferences page]

### Serialization Mode

##### _Use TMDL format_ (disabled)

Save model metadata using the Tabular Model Definition Language (TMDL) format instead of JSON. TMDL is the modern format recommended for version control and collaboration.

##### _Use recommended serialization settings_ (enabled)

Apply recommended settings for folder-based serialization (overrides custom settings). When enabled, Tabular Editor uses best practices for saving models to folders, optimized for version control.

### Legacy (JSON) Serialization Settings

##### _Prefix filenames_ (disabled)

Add numeric prefixes to filenames for ordering. This can help maintain a consistent file order in file explorers.

##### _Local relationships_ (enabled)

Store relationship definitions with individual tables instead of in a central location. This makes it easier to see which relationships belong to each table when using version control.

##### _Local perspectives_ (enabled)

Store perspective membership with individual objects instead of in a central location. This reduces merge conflicts in version control.

##### _Local translations_ (enabled)

Store translations with individual objects instead of in a central location. This reduces merge conflicts in version control.

##### _Levels_

Select which object types to serialize at different folder levels. This allows you to organize your model files into a hierarchical structure.

##### _Ignore inferred objects_ (enabled)

Don't serialize objects that are automatically inferred by the engine. This reduces clutter in saved metadata.

##### _Ignore inferred properties_ (enabled)

Don't serialize properties that are automatically inferred by the engine. This keeps saved metadata clean and focused on explicitly set values.

##### _Ignore timestamps_ (enabled)

Don't serialize timestamp metadata. This is highly recommended for version control as it prevents unnecessary changes in every commit.

##### _Ignore lineage tags_ (disabled)

Don't serialize Power BI lineage tag metadata. Enable this if you don't want lineage information in your saved metadata.

##### _Ignore privacy settings_ (disabled)

Don't serialize data source privacy settings. Enable this if you manage privacy settings separately.

##### _Include sensitive data_ (disabled)

Include sensitive information like passwords in serialized metadata. This is not recommended for security reasons.

##### _Ignore incremental refresh partitions_ (disabled)

Don't serialize partitions created by incremental refresh policies. Enable this if you want incremental refresh to be managed separately from your saved metadata.

##### _Split multiline strings_ (enabled)

Split long string values across multiple lines for better readability in version control. This makes it easier to see changes in DAX expressions and other long text properties.

##### _Sort arrays_ (disabled)

Sort array elements alphabetically for consistent serialization. This can reduce meaningless differences in version control, but may change the logical order of some elements.

### TMDL Serialization Settings

##### _Indentation mode_ (tabs)

Choose between tabs or spaces for indentation in TMDL files. Tabs are the default and recommended option.

##### _Indentation spaces_ (4)

When using spaces, specify the number of spaces per indentation level.

## Data Browsing > General

![Placeholder: Screenshot of Data Browsing General preferences page]

##### _Auto-refresh data preview_ (enabled)

Automatically refresh table preview windows when model changes are saved. This feature is super-useful when debugging - update an expression in one window while having a data preview open in another. Whenever you hit CTRL+S, the preview is automatically refreshed.

##### _Auto-execute DAX queries_ (enabled)

Automatically execute DAX queries when model changes are saved. Similar to auto-refresh data preview, this allows you to see the immediate impact of changes to measures or calculated columns.

##### _DAX query smart selection_ (enabled)

When executing a partial selection in a DAX query, intelligently determine the query context. This allows you to execute just a portion of your query for testing.

##### _Keep filtering and sorting in DAX query results_ (WhenQueryUnchanged)

Control whether to preserve grid filters and sorting when re-executing queries:

- **Never**: Sorting and filtering are always reset when a query is executed
- **WhenQueryUnchanged**: Sorting and filtering are reset only when the query is modified
- **Always**: Sorting and filtering are never reset if the columns still exist

##### _Direct query max rows_ (100)

Maximum number of rows to retrieve in Direct Query mode. Adjust this if you need to preview more data, but be mindful of performance.

##### _DAX query max rows_ (1000)

Maximum number of rows to retrieve for DAX queries. Increase this if you need to analyze larger result sets.

## Data Browsing > Pivot Grid

![Placeholder: Screenshot of Pivot Grid preferences page]

##### _Auto-refresh pivot grid_ (enabled)

Automatically refresh pivot grids when model changes are saved. Just like with DAX queries, this allows you to immediately see the impact of changes to measures.

##### _Pivot grid customization default layout_ (StackedDefault)

Choose the default layout for the pivot grid field list. Options include:

- **StackedDefault**: Fields and areas in a single stacked panel
- **StackedSideBySide**: Fields and areas in side-by-side panels
- **TopPanelOnly**: Field list at the top only
- **BottomPanelOnly2by2**: Field list in a 2x2 grid at the bottom
- **BottomPanelOnly1by4**: Field list in a 1x4 layout at the bottom

##### _Show all fields in pivot customization_ (enabled)

Display all available fields in the pivot grid field list by default, including hidden fields.

##### _Pivot header word wrap_ (enabled)

Enable word wrapping in pivot grid headers. This makes long field names more readable.

##### _Warn if pivot grid fields mismatch_ (enabled)

Show a warning when pivot grid field definitions don't match the current model. This can happen if you've deleted or renamed fields used in a saved pivot grid.

##### _Always show pivot grid field list_ (enabled)

Keep the pivot grid field list visible by default. Disable this if you prefer more screen space for the pivot grid itself.

## DAX Editor > General

![Dax Editor General](~/content/assets/images/dax-editor-general.png)

Tabular Editor 3's DAX editor is highly configurable. This page provides settings for general configuration of the DAX editor:

##### _Line numbers_ (enabled)

Display line numbers in the left margin of the editor.

##### _Code folding_ (enabled)

Enable collapsible regions in DAX code for better readability. Make sure you try out this feature!

##### _Visible whitespace_ (disabled)

Show dots for spaces and arrows for tabs. This can be helpful when diagnosing indentation issues.

##### _Indentation guides_ (enabled)

Display vertical lines to show indentation levels.

##### _Use tabs_ (disabled)

When checked, a tab character (`\t`) is inserted whenever the TAB button is hit. Otherwise, a number of spaces corresponding to the _Indent width_ setting is inserted.

##### _Comment style_ (slashes)

DAX supports line comments that use slashes (`//`) or hyphens (`--`). This setting determines which style of comment is used when Tabular Editor 3 generates DAX code.

##### _DAX function documentation_

Use this setting to specify which URL to launch in the default web browser, whenever you hit F12 while the cursor is on a DAX function. Options include https://dax.guide (recommended) and Microsoft's official documentation.

### DAX Settings

##### _Locale_

Specify the locale for DAX functions and formatting.

##### _Analysis Services version settings_

These settings are relevant only when Tabular Editor 3 cannot determine the version of Analysis Services used, as is the case when a Model.bim file is loaded directly. In this case, Tabular Editor tries to guess which version the model will be deployed to, based on the compatibility level. If Tabular Editor reports incorrect semantic/syntax errors, you may need to tweak these settings.

## DAX Editor > Auto Formatting

![Auto Formatting Settings](~/content/assets/images/auto-formatting-settings.png)

The DAX Editor is **very** powerful and helps you produce beautiful, readable DAX code as you type.

##### _Auto format code as you type_ (enabled)

This option will automatically apply certain formatting rules whenever certain keystrokes occur. For example, when a parenthesis is closed, this feature will ensure that everything within the parentheses is formatted according to the other settings on this page.

##### _Auto-format function calls_ (enabled)

This option specifically controls whether automatic formatting of function calls (spacing between arguments and parentheses) should happen when a parenthesis is closed.

##### _Auto-indent_ (enabled)

This option automatically indents function arguments when a line break is inserted within a function call.

##### _Auto-brace_ (enabled)

This option automatically inserts the closing brace or quote whenever an opening brace or quote is entered.

##### _Wrap selection_ (enabled)

When enabled, this option automatically wraps the current selection with the closing brace, when an opening brace is entered.

### Formatting Rules

These settings control how DAX code whitespace is formatted, both when auto-formatting occurs and when code is manually formatted.

##### _Space after functions_ (disabled)

# [Enabled](#tab/space-after-function-on)

```DAX
SUM ( 'Sales'[Amount] )
```

# [Disabled](#tab/space-after-function-off)

```DAX
SUM( 'Sales'[Amount] )
```

***

##### _Newline after functions_ (disabled)

Applies only when a function call needs to be broken across multiple lines.

# [Enabled](#tab/newline-after-function-on)

```DAX
SUM
(
    'Sales'[Amount]
)
```

# [Disabled](#tab/newline-after-function-off)

```DAX
SUM(
    'Sales'[Amount]
)
```

***

##### _Pad parentheses_ (enabled)

# [Enabled](#tab/pad-parentheses-on)

```DAX
SUM( Sales[Amount] )
```

# [Disabled](#tab/pad-parentheses-off)

```DAX
SUM(Sales[Amount])
```

***

##### _Long format line limit_ (120)

The maximal number of characters to keep on a single line before an expression is broken across multiple lines, when using the **Format DAX (long lines)** option.

##### _Short format line limit_ (60)

The maximal number of characters to keep on a single line before an expression is broken across multiple lines, when using the **Format DAX (short lines)** option.

### Casings and Quotes

In addition to formatting the DAX code whitespace, Tabular Editor 3 can also fix object references and function/keyword casings.

##### _Fix measure/column qualifiers_ (enabled)

When checked, table prefixes are automatically removed from measure references, and automatically inserted on column references.

##### _Preferred keyword casing_ (UPPER)

This setting allows you to change the casing used for keywords, such as `ORDER BY`, `VAR`, `EVALUATE`, etc.

##### _Preferred function casing_ (UPPER)

This setting allows you to change the casing used for functions, such as `CALCULATE(...)`, `SUM(...)`, etc.

##### _Fix keyword/function casing_ (enabled)

When checked, casing of keywords and functions is automatically corrected whenever code is auto-formatted or manually formatted.

##### _Fix object reference casing_ (enabled)

DAX is a case-insensitive language. When this is enabled, references to tables, columns and measures are automatically corrected such that the casing matches the physical name of the referenced objects.

##### _Always quote tables_ (disabled)

Referencing certain table names do not require surrounding single quotes in DAX. However, if you prefer table references to always be quoted, you can check this option.

##### _Always prefix extension columns_ (disabled)

Extension columns can be defined without a table name. When checked, the DAX editor will always add the table prefix to an extension column.

## DAX Editor > Code Assist

![Placeholder: Screenshot of DAX Editor Code Assist preferences page]

On this page, you can configure the two most important Code Assist features, namely calltips (aka. "parameter info") and auto-complete.

##### _Auto-complete trigger_

Control when the auto-complete list appears. Options include automatic triggering after typing a certain number of characters, or manual triggering with CTRL+Space.

##### _Calltip trigger_

Control when parameter information appears. Options include automatic triggering when opening a function parenthesis, or manual triggering.

##### _Incremental search_ (enabled)

Enable fuzzy/incremental searching in auto-complete. This allows you to find items by typing parts of their name, not just the beginning.

##### _Suggest table names_ (enabled)

Include table names in auto-complete suggestions.

##### _Always quote table names_ (disabled)

Automatically quote table names in suggestions, even when not required.

##### _Show first letter only_ (disabled)

Only show items starting with the typed letter. Disable this to use incremental search instead.

## DAX Editor > Code Actions

![Placeholder: Screenshot of DAX Editor Code Actions preferences page]

Configure automatic code improvement suggestions:

##### _Variable prefixes_

Define acceptable prefixes for variable names (e.g., `_`, `__`, `$`, `var_`, `var`, `v_`, `v`, `VAR_`). Code actions will suggest adding these prefixes to variable names that don't follow the convention.

##### _Column prefixes_

Define acceptable prefixes for temporary column names (e.g., `@`, `$`, `_`, `x`, `x_`). Code actions will suggest adding these prefixes to temporary column names that don't follow the convention.

## SQL Editor / M Editor / C# Editor

![Placeholder: Screenshot of SQL/M/C# Editor preferences pages]

Similar configuration options are available for SQL, M (Power Query), and C# script editors, including:

- Syntax highlighting and color schemes
- Auto-formatting options
- Code assist and auto-complete features
- Comment styles and indentation preferences

Each editor can be customized independently to match your preferred coding style.

## DAX Formatter

![Placeholder: Screenshot of DAX Formatter preferences page]

##### _DAX formatter consent_ (disabled)

Agree to send DAX code to the external DAX formatting service (www.daxformatter.com). When enabled, you can use this service to format DAX code according to community standards.

##### _DAX formatter request timeout_ (5000)

Timeout in milliseconds for DAX formatter requests. Increase this if you frequently get timeout errors when using the DAX formatter.

## DAX Optimizer Integration

![Placeholder: Screenshot of DAX Optimizer Integration preferences page]

Configure integration with DAX Optimizer (Enterprise Edition only):

##### _Connect automatically_ (null/prompt)

Automatically connect to DAX Optimizer when available. When not set, you will be prompted the first time.

##### _Obfuscate VPAX files_ (enabled)

Anonymize model metadata when sending to DAX Optimizer. This protects sensitive information like table and column names while still allowing analysis.

##### _Obfuscation dictionary directory_ (`%LocalAppData%\TabularEditor3\DaxOptimizer`)

Specify where obfuscation dictionaries are stored. The dictionary maintains consistent obfuscation across multiple analyses.

## VertiPaq Analyzer

![Placeholder: Screenshot of VertiPaq Analyzer preferences page]

##### _Include TOM metadata_ (enabled)

Include Tabular Object Model metadata in VertiPaq Analyzer statistics. This provides richer information about your model structure.

##### _Read stats from data_ (enabled)

Read statistics by scanning actual data (more accurate but slower). When disabled, only metadata is used.

##### _Direct Lake extraction mode_ (ResidentOnly)

How to extract statistics from Direct Lake models:

- **ResidentOnly**: Only analyze data currently loaded in memory
- **All**: Include non-resident data (slower, may trigger data loading)

##### _Read stats from Dynamic Management Views_ (disabled)

Use DMVs to gather statistics (faster but less accurate). This is an alternative to reading from data.

##### _Relationship sample rows_ (3)

Number of rows to sample when analyzing relationships. Higher values provide more accuracy but take longer.

##### _Column batch size_ (50)

Number of columns to analyze in each batch. Adjust this based on your model size and performance requirements.

## Power BI Integration

![Placeholder: Screenshot of Power BI Integration preferences page]

##### _Power BI endpoint base URL_ (`https://api.powerbi.com`)

The base URL for Power BI API calls. Change this if you're working with a sovereign cloud or custom environment.

##### _Fabric endpoint base URL_ (`https://api.fabric.microsoft.com`)

The base URL for Microsoft Fabric API calls. Change this if you're working with a sovereign cloud or custom environment.

##### _Use embedded browser for authentication_ (enabled)

Use the embedded browser for OAuth authentication instead of the system browser. This provides a more integrated experience.

## Proxy Settings

![Placeholder: Screenshot of Proxy Settings preferences page]

##### _Proxy type_ (None)

Choose between:

- **None**: No proxy configuration
- **System**: Use system proxy settings
- **Custom**: Specify custom proxy configuration

##### _Proxy address_

The address of the proxy server (e.g., `http://proxy.company.com:8080`).

##### _Proxy user_

Username for proxy authentication if required.

##### _Proxy password_

Password for proxy authentication (stored encrypted).

##### _Use default credentials_ (enabled)

Use the current Windows credentials for proxy authentication. This implements the [same behavior as Power BI Desktop](https://docs.microsoft.com/en-us/power-bi/connect-data/desktop-troubleshooting-sign-in#using-default-system-credentials-for-web-proxy).

##### _Bypass proxy on local_ (enabled)

Bypass the proxy for local addresses. This is recommended for performance.

##### _Proxy bypass list_

List of addresses that should bypass the proxy (e.g., `localhost;*.company.local`).

## Next Steps

For a user-friendly guide to the most commonly adjusted preferences, see the getting started guide (Personalizing TE3)[xrefid: personalizing-te3].
