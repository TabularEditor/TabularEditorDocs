---
uid: te-cli-interactive
title: 交互模式
author: Peer Grønnerup
updated: 2026-09-11
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      none: true
    - product: Tabular Editor CLI
      full: true
---

# 交互模式

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

交互模式是一种引导式的读-求值-打印循环（REPL），用于从终端探索模型。 It's the gentlest on-ramp for users who are new to command lines, and a convenient workspace for ad-hoc sessions against a single model.

## 启动会话

要启动会话，请运行以下任一命令：

```bash
te interactive                              # Start and connect to a model later
te interactive --model ./model              # Start with a local model
te interactive -s MyWorkspace -d MyModel    # Start with a remote model
```

`te interactive` accepts a few flags for tuning the session:

- `--no-banner` - skip the welcome banner on startup.
- `--echo` - echo each executed command to stdout before its output. Useful for logging when driving the REPL from a script.
- `--batch` - non-interactive batch mode: read commands from stdin line by line, execute each, and exit on EOF. Automatically enabled when stdin is redirected.
- `--no-batch` - force interactive TTY mode even when stdin is redirected (mutually exclusive with `--batch`).

会话会打印欢迎横幅，显示当前活动模型，并将你带到一个具备模型上下文的提示符下：

![Tabular Editor CLI 交互模式会话](~/content/assets/images/features/cli/cli-interactive-mode.png)

如果尚未设置模型，提示符仅为 `te>`。此时只需使用 `connect` 打开连接选择器，或使用 `connect <path>` 或 `connect <workspace> <model>` 连接到某个 Workspace 中的模型。

## 会话内命令

REPL 启动后，所有 `te` 子命令都可用，**且无需加上 `te` 前缀**：

```
ls tables
get Sales/Revenue -p expression
query -q "EVALUATE TOPN(5, 'Sales')"
bpa run --fail-on error
```

与在会话外时一样，每个命令都可以使用 `--help`：

```
deploy --help
```

## 引号与 DAX 风格路径

REPL 的行拆分器可识别与 [对象路径](xref:te-cli-commands#object-paths) 相同的引号形式，因此 DAX 形式的引用会被解释为单个参数：

- `'...'` and `"..."` - single- and double-quoted segments. The quote characters are stripped, doubled quotes escape a literal occurrence.
- `[...]` - bracketed segment. **方括号会在生成的参数中保留**，因此像 `'Internet Sales'[Sales Amount]` 这样的路径会以单个令牌的形式传递给命令，路径解析器随后可以将其重新解释为 DAX 引用。 Doubled closing brackets (`]]`) stay verbatim for the same reason.

```
get 'Internet Sales'[Sales Amount]   # One argument, DAX form
get [Total Sales]                    # Lone-bracket model-wide lookup
ls 'Net Sales'/'Sales Amount'        # Quoted segments with a slash separator
```

未闭合的分组会一直延伸到行末，因此误写的起始引号或括号会触发明确的错误，而不会悄悄把内容拆开。

## 内置 REPL 命令

这些由 REPL 自身处理，而不是常规命令树：

| 命令                  | 用途                                                                                                                                                                 |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `help` 或 `?`        | 列出可用命令。                                                                                                                                                            |
| `status` 或 `pwd`    | 显示当前活动的模型/连接。                                                                                                                                                      |
| `save`              | Commit all staged in-memory edits back to the model source.                                                                                        |
| `revert`            | Discard all staged edits made since the last save.                                                                                                 |
| `clear` 或 `cls`     | 清空屏幕。                                                                                                                                                              |
| `exit`、`quit` 或 `q` | 退出交互模式。 If staged edits are unsaved you are asked to confirm (`n` is the default); `exit --force` discards them without asking. |

`save` inside the session takes no arguments - re-serializing the model to another format or location is `save-as` (e.g. `save-as -o ./out --serialization bim`), exactly as outside the session.

## Staged edits

Inside the session, mutating commands (`set`, `add`, `remove`, `move`, `script`, `macro run`, ...) stage their changes in memory instead of writing to the source, and the prompt shows an indicator while unsaved staged edits exist. The built-in `save` command commits everything staged; `revert` discards everything staged.

Each mutating command can also decide for itself: `--save` persists that one command's change immediately, `--stage` keeps it in memory (the default), and `--revert` rolls the command's change back after showing its effect - useful for a "what would this do?" probe. The three are mutually exclusive, and `--stage`/`--revert` exist only inside the session.

The default per-command behavior is the `interactiveEditMode` config key (`stage` | `save` | `revert`) - see @te-cli-config.

Staged edits are never thrown away silently. Closing a session that still holds them - with `exit`, **Ctrl+D**, or by reaching the end of piped input - first checks for unsaved changes. If unsaved changes exist and a terminal is active, you are asked to confirm, with "no" as the default, and declining returns you to the prompt with the edits intact. Where nobody can answer (stdin piped or redirected, or `--non-interactive`), the session writes a warning naming the unsaved changes and exits with a failure code instead of a success one. Nothing is saved on the way out either way: run `save` first, or `exit --force` to discard the edits deliberately.

## Line editing and keys

The prompt offers single-line editing:

- **Left/Right** move the caret; **Home/End** (also **Ctrl+A**/**Ctrl+E**) jump to the ends; **Backspace/Delete** edit in place.
- **Up/Down** browse the command history, which persists across sessions.
- **Ctrl+C** cancels the current command without leaving the session and abandons the half-typed line for good - it is never run, Up does not bring it back, and it is not added to the history.
- **Ctrl+D** on an empty prompt exits (**Ctrl+Z** then **Enter** on Windows).

There is no tab completion inside the session - shell completion via `te completion` applies to the outer shell only.

## 引导式提示

When interactive mode is active, commands that need missing input prompt for it instead of failing. Running `auth` without a subcommand opens a picker for Login / Status / Logout; running `deploy --execute` or `refresh --execute` without `--force` shows a summary and asks for confirmation (`n` is the safe default). A `deploy` or `refresh` without `--execute` is a dry run that prints the TMSL it would send, so it never prompts.

如果想在当前会话中为单个命令禁用提示，传入 `--non-interactive`。

## Piped and redirected input

Interactive mode also accepts piped or redirected stdin, so the same REPL can be driven from a script instead of typed by hand. Each line of input is run as a command, exactly as if you had entered it at the prompt, and the session exits when input is exhausted (or when it reaches an `exit` line). If staged edits are still unsaved at that point, the session warns and exits non-zero - end a mutating script with `save` (or `exit --force` to discard on purpose).

```bash
printf "ls\nexit\n" | te interactive --model ./model    # bash / git-bash
te interactive --model ./model < script.te              # redirected file
```

```bat
(echo ls & echo exit) | te interactive --model .\model  :: Windows cmd.exe
```

The `-` stdin convention (`set -p Expression=-`, `query -q -`, and so on) is refused inside the interactive session, because the session itself owns stdin - use it from the outer shell instead.

Lines that start with `#` are treated as comments and skipped, so you can annotate a script file:

```
# script.te - inspect the model, then exit
ls tables
ls measures
exit
```

### Batch mode and exit codes

When stdin is piped, `--batch` is the **default**: the session stops at the first command that fails and exits with a non-zero code, which makes a piped run safe to use as a build or CI step. Pass `--no-batch` to keep running the remaining lines even after a command fails. The process exit code is `0` for a clean run and non-zero when a command fails under batch mode.

```bash
# Default when piped: stop at the first failing command, exit non-zero
printf "bpa run --fail-on error\ndeploy --execute --force\nexit\n" | te interactive --model ./model

# Run every line regardless of failures
printf "bpa run --fail-on error\ndeploy --execute --force\nexit\n" | te interactive --model ./model --no-batch
```

### Readable transcripts

`--echo` writes each input line to stdout ahead of its output, which is handy when capturing a transcript of a piped run. Comment lines are not echoed.

```bash
printf "ls tables\nexit\n" | te interactive --model ./model --echo
```

### Options

| 选项            | 说明                                                                                                           |
| ------------- | ------------------------------------------------------------------------------------------------------------ |
| `--no-banner` | Suppress the welcome banner.                                                                 |
| `--echo`      | Echo each input line to stdout (useful for piped transcripts).            |
| `--batch`     | Exit non-zero on the first failing command (default when stdin is piped). |
| `--no-batch`  | Continue after errors even when stdin is piped.                                              |

### Welcome banner vs. preview notice

Two separate messages can appear at the start of a session - don't conflate them:

- The **welcome banner** is the interactive splash described under [Starting a session](#starting-a-session). It is suppressed with `--no-banner`. When stdin is piped, no welcome banner is emitted in the first place, so `--no-banner` has a visible effect only in a true interactive (TTY) session.
- The **preview-expiry notice** (`This is an early preview release ...`) is a different message. It is always written to **stderr** and is **not** affected by `--no-banner`. Suppress it with `te config set hidePreviewNotice true`.

## Auto-launch on empty invocation

Running `te` in a terminal with no arguments drops you straight into the interactive REPL, so exploring a model is as fast as opening a shell and typing `te`. When stdin, stdout, or stderr is redirected (piped output, CI pipelines, scripts), the CLI falls through to its normal parse and prints help instead - so shell scripts that invoke `te` without a subcommand keep behaving the same way.

The behavior is controlled by the `launchInteractiveMode` config key with three values:

| 值                                   | Effect                                                                                                                                     |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `auto` (default) | Launch the REPL only when all three streams are attached to a TTY. Otherwise fall through to normal parse. |
| `always`                            | Launch the REPL regardless of stream redirection. Useful when you always want an interactive session.      |
| `never`                             | Never auto-launch the REPL. `te` on its own prints help.                                                   |

Change it globally with:

```bash
te config set launchInteractiveMode never    # keep the classic help-on-empty behavior
te config set launchInteractiveMode auto     # restore the default
```

Override for a single invocation via the `TE_INTERACTIVE` environment variable (same values), or pass `--non-interactive` on the command line - both force `never` for that call, so `te --non-interactive` prints help instead of launching the REPL.

## 何时使用交互模式与非交互模式

- **交互模式** 最适合探索、学习 CLI、针对单个模型执行一次性批量编辑，以及演示。
- **非交互模式**（在 `te interactive` 之外的默认模式）适用于编写脚本、自动化或在 CI 中运行。 See @te-cli-automation and @te-cli-cicd.

两者共用同一套命令树——你在 `te interactive` 中运行的任何命令，只要在前面加上 `te` 前缀，就可以直接粘贴到 Shell 脚本中。

## 相关页面

- @te-cli-commands - 完整的命令参考。
- @te-cli-auth - 连接到 Workspace，并管理配置文件。
- @te-cli-automation - 何时应退出交互模式。
