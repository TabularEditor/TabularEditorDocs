---
uid: te-cli-interactive
title: Interactive Mode
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
# Interactive Mode

> [!IMPORTANT]
> The Tabular Editor CLI is in **Limited Public Preview**. It is offered for evaluation with a Tabular Editor account; no license is required during preview. Commands, flags, and outputs may change before general availability. **The preview build stops functioning after 2026-09-30.** We recommend against using the CLI in production CI/CD pipelines during preview.

Interactive mode is a guided REPL (read-eval-print loop) for exploring a model from the terminal. It's the gentlest on-ramp for users who are new to command lines, and a convenient workspace for ad-hoc sessions against a single model.

## Starting a session

```bash
te interactive                              # Start and connect to a model later
te interactive ./model                      # Start with a local model
te interactive -s MyWorkspace -d MyModel    # Start with a remote model
```

The session prints a welcome banner, shows the active model, and drops you at a model-aware prompt:

```
te [MyModel]>
```

If no model is set, the prompt is just `te>` — use `connect <path>` or `connect <workspace> <model>` inside the session to bind one.

## Commands inside the session

Every `te` subcommand is available **without the `te` prefix**:

```
te [MyModel]> ls tables
te [MyModel]> get "Sales/Revenue" -q expression
te [MyModel]> query -q "EVALUATE TOPN(5, 'Sales')"
te [MyModel]> bpa run --fail-on error
```

Each command accepts `--help` the same way it does outside the session:

```
te [MyModel]> deploy --help
```

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

The two share the same command tree — anything you run inside `te interactive` can be pasted into a shell script by prefixing it with `te`.

## Related pages

- @te-cli-commands — full command reference.
- @te-cli-auth — connect to workspaces and manage profiles.
- @te-cli-automation — when to leave interactive mode.
