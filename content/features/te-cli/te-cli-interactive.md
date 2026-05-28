---
uid: te-cli-interactive
title: Interactive Mode
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
# Interactive Mode

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

Interactive mode is a guided read-eval-print loop (REPL) for exploring a model from the terminal. It's the gentlest on-ramp for users who are new to command lines, and a convenient workspace for ad-hoc sessions against a single model.


## Starting a session

To Start a session run any of these commands:

```bash
te interactive                              # Start and connect to a model later
te interactive ./model                      # Start with a local model
te interactive -s MyWorkspace -d MyModel    # Start with a remote model
```

The session prints a welcome banner, shows the active model, and opens you at a model-aware prompt:

![Tabular Editor CLI interactive mode session](~/content/assets/images/features/cli/cli-interactive-mode.png)

If no model is set, the prompt is just `te>` - simply use `connect` for connection picker, `connect <path>` or `connect <workspace> <model>` to connect to one.

## Commands inside the session

Once a REPL has started, every `te` subcommand is available **without the `te` prefix**:

```
ls tables
get "Sales/Revenue" -q expression
query -q "EVALUATE TOPN(5, 'Sales')"
bpa run --fail-on error
```

Each command accepts `--help` the same way it does outside the session:

```
deploy --help
```

## Quoting and DAX-style paths

The REPL line splitter recognises the same quoting forms as [object paths](xref:te-cli-commands#object-paths) so DAX-shaped references are interpreted as a single argument:

- `'...'` and `"..."` - single- and double-quoted segments. The quote characters are stripped, doubled quotes escape a literal occurrence.
- `[...]` - bracketed segment. **Brackets are preserved** in the resulting argument so a path like `'Internet Sales'[Sales Amount]` reaches the command as one token that the path parser can re-interpret as a DAX reference. Doubled closing brackets (`]]`) stay verbatim for the same reason.

```
get 'Internet Sales'[Sales Amount]   # One argument, DAX form
get [Total Sales]                    # Lone-bracket model-wide lookup
ls 'Net Sales'/'Sales Amount'        # Quoted segments with a slash separator
```

Unterminated groups absorb to end of line, so a stray opening quote or bracket fails with an explicit error rather than splitting silently.

## Built-in REPL commands

These are handled by the REPL itself, not the regular command tree:

| Command | Purpose |
| -- | -- |
| `help` or `?` | List available commands. |
| `status` or `pwd` | Show the active model/connection. |
| `clear` or `cls` | Clear the screen. |
| `exit`, `quit`, or `q` | Exit interactive mode. |

## Guided prompts

When interactive mode is active, commands that need missing input prompt for it instead of failing. Running `auth` without a subcommand opens a picker for Login / Status / Logout; running `deploy` without `--force` shows a summary and asks for confirmation (`n` is the safe default).

To disable prompts for a single command inside the session, pass `--non-interactive`.

## When to use interactive vs. non-interactive

- **Interactive mode** is best for exploration, learning the CLI, one-off bulk edits against a single model, and demos.
- **Non-interactive mode** (the default outside `te interactive`) is what you reach for when scripting, automating, or running in CI. See @te-cli-automation and @te-cli-cicd.

The two share the same command tree - anything you run inside `te interactive` can be pasted into a shell script by prefixing it with `te`.

## Related pages

- @te-cli-commands - full command reference.
- @te-cli-auth - connect to workspaces and manage profiles.
- @te-cli-automation - when to leave interactive mode.
