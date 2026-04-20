---
uid: te-cli
title: Tabular Editor CLI (Limited Public Preview)
author: Peer Grønnerup
updated: 2026-04-20
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

The Tabular Editor CLI (`te`) is a cross-platform command-line interface for Power BI and Analysis Services semantic models. It runs on Windows, macOS, and Linux as a single self-contained executable and wraps the same model engine (TOMWrapper) that powers Tabular Editor 3 Desktop.

Use it to inspect, edit, validate, deploy, refresh, and test semantic models from a terminal — against local TMDL or BIM files, Power BI Desktop, or semantic models in Fabric and Power BI Service workspaces.

> [!IMPORTANT]
> The Tabular Editor CLI is in **Limited Public Preview**. It is offered for evaluation with a Tabular Editor account; no license is required during preview. Commands, flags, and outputs may change before general availability. **The preview build stops functioning after 2026-09-30.** We recommend against using the CLI in production CI/CD pipelines during preview.

## Built for three audiences

The CLI was designed to serve three consumers from the same binary:

- **Humans** — scripting bulk edits, exploring a model from the terminal, composing commands in shell pipelines.
- **AI agents** — token-lean structured output, predictable exit codes, machine-parseable errors.
- **CI/CD pipelines** — non-interactive mode, GitHub Actions and Azure DevOps annotations, VSTEST-compatible test results.

The same design choices — structured JSON output, a `--non-interactive` global flag, clear errors — serve all three.

## What the CLI can do

The CLI organizes more than 50 commands into 10 families. Each family maps to a concrete stage of the semantic-model lifecycle.

| Family | What it does | Example commands |
| -- | -- | -- |
| Model I/O | Load, save, export, initialize models | `te load`, `te save`, `te export` |
| Model Editing | Get/set properties, add/remove/move objects | `te set`, `te add`, `te rm`, `te mv` |
| Inspection | List objects, search, diff, dependency analysis | `te ls`, `te find`, `te diff`, `te deps` |
| Analysis & Quality | Validate, run BPA, format DAX, analyze storage | `te validate`, `te bpa run`, `te format`, `te vertipaq` |
| Execution | Run DAX queries, C# scripts, macros | `te query`, `te script`, `te macro` |
| Deployment & Refresh | Deploy to workspace, trigger refresh, incremental refresh | `te deploy`, `te refresh`, `te incremental-refresh` |
| Testing | Assertion tests, snapshots, A/B comparison | `te test run` |
| Connection & Auth | Connect to workspaces, manage authentication and profiles | `te connect`, `te auth`, `te profile` |
| Configuration | Settings and licensing | `te config`, `te license` |
| Shell | Interactive mode, shell completions | `te interactive`, `te completion` |

See @te-cli-commands for a full command reference with syntax, options, and examples for each command.

## Getting started

1. **Sign up or sign in** at [tabulareditor.com](https://tabulareditor.com) with a Tabular Editor account.
2. **Download and install** — see @te-cli-install for Windows, macOS, and Linux instructions.
3. **Authenticate** — run `te auth login` to connect to Power BI or Fabric. See @te-cli-auth.
4. **Run your first command** — `te --help` lists every command; `te <command> --help` shows detailed options.

A first look at a live model takes two commands:

```bash
te auth login
te ls -s MyWorkspace -d MyModel
```

## Preview notice

Every command prints a yellow preview banner on stderr by default. To quiet it down:

```bash
te config set hidePreviewNotice true
```

The banner **always** reappears within 14 days of the expiry date (2026-09-30), regardless of this setting, to give you a clear runway to update.

## License outlook

During Limited Public Preview, the CLI does not require a license; you only need a Tabular Editor account to download it. At general availability the CLI will require a license; pricing is still being finalized and will be announced ahead of GA.

<!-- TBD: confirm exact license-outlook wording with marketing before publishing. -->

## Next steps

- @te-cli-install — download, install, verify.
- @te-cli-auth — authenticate to Power BI, Fabric, and Azure Analysis Services.
- @te-cli-commands — full command reference.
- @te-cli-config — configuration file and path overrides.
- @te-cli-interactive — guided REPL mode for new users.
- @te-cli-automation — structured output, scripting patterns for Python, PowerShell, and Bash.
- @te-cli-cicd — GitHub Actions and Azure DevOps pipeline examples.
- @te-cli-migrate — migrating from the Tabular Editor 2 command line.

<!-- TBD: add official download URL once confirmed. Blog draft says "Get it here"/"Download Tabular Editor CLI" — link not yet final. -->
<!-- TBD: add feedback link for preview (blog references "[Feedback link]" — not yet resolved). -->
