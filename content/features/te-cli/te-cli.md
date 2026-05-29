---
uid: te-cli
title: Tabular Editor CLI (Limited Public Preview)
author: Peer Grønnerup
updated: 2026-05-12
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      none: true
    - product: Tabular Editor CLI
      full: true
---
# Tabular Editor CLI (Limited Public Preview)

The Tabular Editor CLI (`te`) is a cross-platform command-line interface for Power BI and Analysis Services semantic models. It runs on Windows, macOS, and Linux as a single self-contained executable and is based on the same foundation that powers Tabular Editor 3.

With the Tabular Editor CLI you can inspect, edit, validate, deploy, refresh, and test semantic models from a terminal - against local TMDL or BIM files, Power BI Desktop, or semantic models in Fabric and Power BI Service workspaces.

Unlike the Windows-only `TabularEditor.exe` command-line options (TE2) - which was designed primarily to automate C# scripts and macros from a desktop binary - `te` is a purpose-built, cross-platform CLI with structured output, predictable exit codes, and an interactive shell. This unlocks scenarios that our existing [TE2 CLI](xref:command-line-options) can't cover well: terminal-driven model work on macOS and Linux, AI agents driving model changes directly, and clean drop-in for any modern CI runner.

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

## Built for three audiences

Three design pillars run through every command:

- **Structured output** — JSON, CSV, TMDL, TMSL alongside default human-readable text.
- **Non-interactive mode** — a global `--non-interactive` flag that disables prompts and fails fast.
- **Clear errors** — written to stderr with predictable exit codes.

Together they make the same binary work well for three very different audiences:

- **Humans** - scripting bulk edits, exploring a model from the terminal, composing commands in shell pipelines.
- **AI agents** - token-lean JSON, machine-parseable error shapes, exit codes that signal success or failure without parsing stdout.
- **CI/CD pipelines** - non-interactive execution, GitHub Actions and Azure DevOps annotations, VSTEST-compatible test results.

## What the CLI can do

The CLI organizes more than 50 commands into 10 families. Each family maps to a concrete stage of the semantic-model lifecycle.

See @te-cli-commands for a full command reference with syntax, options, and examples for each command. Click any example command in the table to jump straight to its reference entry.

| Family | What it does | Example commands |
| -- | -- | -- |
| [Model I/O](xref:te-cli-commands#model-io) | Load, save, convert, initialize models | [`te load`](xref:te-cli-commands#load), [`te save`](xref:te-cli-commands#save), [`te init`](xref:te-cli-commands#init) |
| [Model Editing](xref:te-cli-commands#model-editing) | Get/set properties, add/remove/move objects | [`te set`](xref:te-cli-commands#set), [`te add`](xref:te-cli-commands#add), [`te rm`](xref:te-cli-commands#rm), [`te mv`](xref:te-cli-commands#mv) |
| [Inspection](xref:te-cli-commands#inspection) | List objects, search, diff, dependency analysis | [`te ls`](xref:te-cli-commands#ls), [`te find`](xref:te-cli-commands#find), [`te diff`](xref:te-cli-commands#diff), [`te deps`](xref:te-cli-commands#deps) |
| [Analysis & Quality](xref:te-cli-commands#analysis-and-quality) | Validate, run BPA, format DAX, analyze storage | [`te validate`](xref:te-cli-commands#validate), [`te bpa run`](xref:te-cli-commands#bpa-run), [`te format`](xref:te-cli-commands#format), [`te vertipaq`](xref:te-cli-commands#vertipaq) |
| [Execution](xref:te-cli-commands#execution) | Run DAX queries, C# scripts, macros | [`te query`](xref:te-cli-commands#query), [`te script`](xref:te-cli-commands#script), [`te macro`](xref:te-cli-commands#macro) |
| [Deployment & Refresh](xref:te-cli-commands#deployment-and-refresh) | Deploy to workspace, trigger refresh, incremental refresh | [`te deploy`](xref:te-cli-commands#deploy), [`te refresh`](xref:te-cli-commands#refresh), [`te incremental-refresh`](xref:te-cli-commands#incremental-refresh) |
| [Testing](xref:te-cli-commands#testing) | Assertion tests, snapshots, A/B comparison | [`te test run`](xref:te-cli-commands#test-run) |
| [Connection & Authentication](xref:te-cli-commands#connection-and-auth) | Connect to workspaces, manage authentication and profiles | [`te connect`](xref:te-cli-commands#connect), [`te auth`](xref:te-cli-commands#auth-login--status--logout), [`te profile`](xref:te-cli-commands#profile-list--show--set--remove) |
| [Configuration](xref:te-cli-commands#configuration) | Settings and licensing | [`te config`](xref:te-cli-commands#config-show--paths--init--set) |
| [Shell](xref:te-cli-commands#shell) | Interactive mode, shell completions | [`te interactive`](xref:te-cli-commands#interactive), [`te completion`](xref:te-cli-commands#completion) |

## Getting started

1. **Sign up or sign in** at [tabulareditor.com](https://tabulareditor.com/download-tabular-editor-cli) with a Tabular Editor account.
2. **Download and install** - see @te-cli-install for Windows, macOS, and Linux instructions.
3. **Authenticate** - run `te auth login` to connect to Power BI or Fabric. See @te-cli-auth.
4. **Run your first command** - `te --help` lists every command; `te <command> --help` shows detailed options.

A first look at a live model takes two commands:

```bash
te auth login
te ls -s MyWorkspace -d MyModel
```

![Tabular Editor CLI te ls example output](~/content/assets/images/features/cli/cli-command-ls.png)

## Preview notice

Every command prints a yellow preview banner on stderr by default:

![Tabular Editor CLI preview notice banner](~/content/assets/images/features/cli/cli-preview-notice.png)

To hide the preview notice, simply run:

```bash
te config set hidePreviewNotice true
```

> [!WARNING]
> The banner reappears on every command within **14 days of the preview end date** (2026-09-30), regardless of `hidePreviewNotice`. This ensures you have visible warning before the CLI stops functioning.

## License outlook

During Limited Public Preview, the CLI does not require a license; you only need a Tabular Editor account to download it. At General Availability (GA) the CLI will require a license; pricing is still being finalized and will be announced ahead of GA.

## Feedback and community

During the preview, bug reports, feature requests, and general discussion happen in the public [TabularEditor/CLI](https://github.com/TabularEditor/CLI) repository on GitHub:

- **Issues** - report bugs, request features, and track known problems.
- **Discussions** - ask questions, share feedback, and swap usage tips with other early adopters.

The repository does not host the CLI source code; it exists to give the community a public place to reach us during the preview.

## Next steps

- @te-cli-install - download, install, verify.
- @te-cli-auth - authenticate to Power BI, Fabric, and Azure Analysis Services.
- @te-cli-commands - full command reference.
- @te-cli-config - configuration file and path overrides.
- @te-cli-interactive - guided REPL mode for new users.
- @te-cli-automation - structured output, scripting patterns for Python, PowerShell, and Bash.
- @te-cli-cicd - GitHub Actions and Azure DevOps pipeline examples.
- @te-cli-migrate - migrating from the Tabular Editor 2 command line.
