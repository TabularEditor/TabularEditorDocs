---
uid: te-cli-limitations
title: Known Limitations
author: Peer Grønnerup
updated: 2026-09-04
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      none: true
    - product: Tabular Editor CLI
      full: true
---
# Known Limitations

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

This page lists known limitations of the Tabular Editor CLI (`te`) so you can plan around them and avoid common pitfalls. It is updated with each release; if you find an issue that is not listed here, please file it in the public [TabularEditor/CLI](https://github.com/TabularEditor/CLI) repository.
 
> [!NOTE]
> Limitations are grouped by area. Each entry describes the constraint and, where one exists, a workaround or the recommended CLI-friendly alternative.

## Scripting

The CLI runs C# scripts (`te script`) against the same `Model` object you use in Tabular Editor 2 and 3, but it is a headless console host. Anything that depends on a Windows Forms UI, on the TOM Explorer selection, or on a live UI-side service (macro registry, online DAX Formatter, live VertiPaq Analyzer) behaves differently - usually by being empty, no-op, or returning an error.

| Limitation | Notes / Workaround |
| -- | -- |
| **`System.Windows.Forms` not loaded** | The CLI uses a cross-platform `TOMWrapper` build that strips all WinForms-coupled code; the WinForms assembly is never loaded into the AppDomain. Scripts that reference `System.Windows.Forms` types (`MessageBox`, `Form`, file pickers, custom dialogs, …) fail to compile. Refactor any UI interaction into environment variables or stdin input. |
| **`Selected.<Plural>` returns an empty enumerable** | `Selected.Tables`, `Selected.Measures`, `Selected.Columns`, `Selected.Hierarchies`, etc. iterate to nothing in the CLI - no compile or runtime error, just no rows. Replace with explicit lookups: `Model.AllMeasures.Where(...)`, `Model.Tables["Sales"].Measures`, or pass object paths into the script via environment variables or stdin. |
| **`Selected.<Singular>` throws an error at runtime** | `Selected.Table`, `Selected.Measure`, `Selected.Column`, `Selected.Hierarchy`, etc. return an error because they require exactly one selected object of that type and the CLI selection is always empty. Reference the object directly - e.g. `Model.Tables["Sales"]`. |
| **`Selected.ActivePerspectives` and `Selected.ActiveCulture`** | Always return an empty collection and `null` respectively. Set the perspective or culture explicitly in the script if needed. |
| **`Select<Object>` dialogs throw `NotSupportedException`** | `SelectTable`, `SelectColumn`, `SelectMeasure`, `SelectObject`, `SelectObjects` (and all overloads) return the following error: *"Object selection dialogs … are not available in CLI scripts. Pre-select the object by name or path before scripting."* Resolve targets up front from environment variables, config, or by querying the model. |
| **`Info` / `Warning` / `Error` / `Output` write to the console** | These still work, but route to stdout/stderr instead of opening a dialog. They never block and never offer an "ignore further popups" prompt. Safe to use in CI. |
| **`ShowPrompt(...)` always returns `Cancel`** | No interactive confirmation is possible. Pre-decide the answer via environment variables or configuration. |
| **`SuspendWaitForm` / `WaitFormVisible` are no-ops** | The "Please wait" spinner is a TE3 UI element. `WaitFormVisible` is a settable flag with no visual effect, and `SuspendWaitForm` is silently ignored - existing scripts continue to compile. |
| **`host.Macro(...)` / `CustomAction(...)` throws an error** | The CLI does not load `%APPDATA%/TabularEditor3/MacroActions.json`, so invoking a macro from inside a script returns an error. Inline the macro logic, call the macro's underlying script file directly, or invoke the macro through `te macro run <name>` with a CLI macros file (`--macros` / `TE_MACROS_PATH` / the `macros` config key). |
| **`table.GetCardinality()` / `column.GetTotalSize()` return 0** | The in-script VertiPaq cardinality helpers have no live VPA in the CLI host. For VPA statistics, load a VPAX explicitly and use `host.Vpa.*`, or run [`te vertipaq`](xref:te-cli-commands#vertipaq). |

## Best Practice Analyzer

| Limitation | Notes / Workaround |
| -- | -- |
| **BPA rule sources must be HTTPS URLs or local file paths** | Only `https://` URLs and bare local file paths are accepted. `http://` is recognized but deliberately rejected at load time with a clear error - BPA rules are executable rule expressions, and fetching them over an unauthenticated channel would be a tampering risk. Other URL schemes (`file://`, `ftp://`, …) are not supported. Applies to both `te bpa run --rules` and the rule list configured via [`te config set`](xref:te-cli-commands#config-list--paths--init--set). |
| **Rule-URL validation runs at gate time, not on `te config set`** | A typo such as `http://` is accepted by `te config set` and only surfaces when BPA actually runs. After editing the configured rule sources, run `te bpa run` (or `te validate`) once to verify each URL loads. |
| **`--rules` does not suppress built-in rules** | When `te bpa run --rules <path-or-url>` is passed, the supplied rules replace the entries in [`bpa.rules`](xref:te-cli-commands#config-list--paths--init--set) and `TE_BPA_RULES` for that invocation, but the built-in defaults still load alongside. To run only the explicit rule file, also pass `--no-defaults`. When a supplied rule file defines the same rule ID as a built-in rule, the rule is evaluated once - the definition from the explicit `--rules` file wins for that `te bpa run` invocation (in the deploy/save gate, the built-in definition wins). |
| **No per-invocation flag to skip `bpa.rules` config** | Once `bpa.rules` is configured, every `te bpa run` loads those rules in addition to the built-ins. There is currently no flag to skip the configured rule files for a single run. Workaround: pass `--rules <path-or-url>` explicitly - the flag fully replaces `bpa.rules` and `TE_BPA_RULES` for that invocation. |

## Validation

| Limitation | Notes / Workaround |
| -- | -- |
| **`te validate` cannot auto-fix Code Action violations** | `te validate` reports Code Action violations but offers no CLI flag to apply the suggested fix. Apply the fix in Tabular Editor 3, or use `te bpa run --fix` for the subset of Code Actions that overlap with BPA rules. |

## Model I/O

| Limitation | Notes / Workaround |
| -- | -- |
| **`--serialization` cannot combine a serialization with a PBIP container** | The `--serialization` option on [`te save-as`](xref:te-cli-commands#save-as) treats `bim`, `tmdl`, `database.json`, and `pbip` as mutually exclusive, so you cannot produce a full PBIP container around a TMSL-serialized (`.bim`) model. To wrap a `tmdl` or `bim` output in a `{modelName}.SemanticModel/` folder with `.platform` and `definition.pbism` files, pass `--supporting-files`; for a complete PBIP (including the report artifact), use `--serialization pbip`. |

## Model editing

| Limitation | Notes / Workaround |
| -- | -- |
| **Calculated sets cannot be created, removed, or moved from the CLI** | Sets are addressable for inspection (`te list Sets`, `te get "Sales/Sets/<name>"`), but `te add`, `te remove`, and `te move` do not support set objects. Use `te script` for set mutations. |
| **No whole-model Power Query formatting sweep** | `te set <path> --format <Property>` formats named expression properties on one object and `te util format-m` formats a single loose expression, but there is no command to format every M expression in a model in one pass. (Whole-model DAX formatting is available via `te script --inline "Model.AllMeasures.FormatDax();" --save`.) |
| **Schema sync treats renamed source columns as removed + added** | `te set <table> --update-schema` cannot detect a rename; a renamed source column shows up as one removed and one new column. Remap manually with `te set <table>/<column> -p SourceColumn=<newName>` before syncing. `--update-schema` is refused on calculated tables and calculation groups. |

## Authentication

| Limitation | Notes / Workaround |
| -- | -- |
| **Only one cached identity per auth method** | The CLI caches one UPN (interactive) identity and one SPN (service principal) identity at a time. Switching to a different user or tenant under the same auth method requires `te auth logout` followed by `te auth login` again, which invalidates the previous cache. |

## Command-line input

| Limitation | Notes / Workaround |
| -- | -- |
| **DAX object paths with spaces must be enclosed in shell quotes** | When a table or column name contains spaces, the entire DAX object reference must be wrapped in shell quotes from the terminal: `te get "'My Table'[My Column]"`. Without the outer quotes, the shell splits the path into multiple arguments and parsing fails. Inside [`te interactive`](xref:te-cli-interactive) no shell quoting is needed because the REPL receives the raw input before the shell breaks it into arguments. |
| **Object names containing reserved path characters must be quoted** | `/ [ ] ' " * ? { }` are reserved in object and filter paths. A name containing one must be quoted with the segment quoting rules, e.g. `te get "Tables/'{foo}'"` or `te get 'Sales/"my*name"'`. `?` is reserved but has no wildcard meaning. The Windows `cmd.exe` shell cannot express the mixed-quote forms - use PowerShell or a POSIX shell for such names (or `te interactive`, which takes the raw line). |
| **`-` (read from stdin) is not available inside `te interactive`** | The shell rejects it with *'-' (stdin) is not available inside the interactive shell.* Pass the value inline, or run the command from your OS shell where piping works. |

## Reporting a missing limitation

If a behavior surprises you and it's not listed here, please open an issue at [TabularEditor/CLI](https://github.com/TabularEditor/CLI/issues) with the command you ran, the output you saw, and the output you expected. Confirmed limitations are added to this page in the next release.

## Related pages

- @csharp-scripts - full C# scripting reference (UI and CLI).
- @script-helper-methods - list of `ScriptHost` helper methods and how they behave in the CLI.
- @te-cli-commands - full CLI command reference.
- @te-cli-automation - patterns for using the CLI in scripts and pipelines.
