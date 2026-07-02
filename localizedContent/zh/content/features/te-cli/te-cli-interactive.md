---
uid: te-cli-interactive
title: 交互模式
author: Peer Grønnerup
updated: 2026-06-26
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

交互模式是一种引导式的读-求值-打印循环（REPL），用于从终端探索模型。 对命令行新手来说，这是最温和的入门方式；而在针对单个模型进行临时操作时，它也是一个便捷的 Workspace。

## 启动会话

要启动会话，请运行以下任一命令：

```bash
te interactive                              # Start and connect to a model later
te interactive ./model                      # Start with a local model
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
get "Sales/Revenue" -q expression
query -q "EVALUATE TOPN(5, 'Sales')"
bpa run --fail-on error
```

与在会话外时一样，每个命令都可以使用 `--help`：

```
deploy --help
```

## 引号与 DAX 风格路径

REPL 的行拆分器可识别与 [对象路径](xref:te-cli-commands#object-paths) 相同的引号形式，因此 DAX 形式的引用会被解释为单个参数：

- `'...'` 和 `"..."` - 用单引号和双引号括起来的分段。 引号字符会被剥离；连续的两个引号用于转义，以表示字面量引号。
- `[...]` — 用方括号括起来的分段。 **方括号会在生成的参数中保留**，因此像 `'Internet Sales'[Sales Amount]` 这样的路径会以单个令牌的形式传递给命令，路径解析器随后可以将其重新解释为 DAX 引用。 出于同样的原因，成对的右方括号 (`]]`) 也会按原样保留。

```
get 'Internet Sales'[Sales Amount]   # One argument, DAX form
get [Total Sales]                    # Lone-bracket model-wide lookup
ls 'Net Sales'/'Sales Amount'        # Quoted segments with a slash separator
```

未闭合的分组会一直延伸到行末，因此误写的起始引号或括号会触发明确的错误，而不会悄悄把内容拆开。

## 内置 REPL 命令

这些由 REPL 自身处理，而不是常规命令树：

| 命令                  | 用途            |
| ------------------- | ------------- |
| `help` 或 `?`        | 列出可用命令。       |
| `status` 或 `pwd`    | 显示当前活动的模型/连接。 |
| `clear` 或 `cls`     | 清空屏幕。         |
| `exit`、`quit` 或 `q` | 退出交互模式。       |

## 引导式提示

启用交互模式后，需要补全输入的命令会提示你输入，而不是直接失败。 不带子命令运行 `auth` 时，会打开一个选择界面，让你在 Login / Status / Logout 之间选择；不带 `--force` 运行 `deploy` 时，会显示摘要并要求确认（安全的默认值为 `n`）。

如果想在当前会话中为单个命令禁用提示，传入 `--non-interactive`。

## Piped and redirected input

Interactive mode also accepts piped or redirected stdin, so the same REPL can be driven from a script instead of typed by hand. Each line of input is run as a command, exactly as if you had entered it at the prompt, and the session exits when input is exhausted (or when it reaches an `exit` line).

```bash
printf "ls\nexit\n" | te interactive ./model        # bash / git-bash
te interactive ./model < script.te                  # redirected file
```

```bat
(echo ls & echo exit) | te interactive .\model      :: Windows cmd.exe
```

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
printf "bpa run --fail-on error\ndeploy --force\nexit\n" | te interactive ./model

# Run every line regardless of failures
printf "bpa run --fail-on error\ndeploy --force\nexit\n" | te interactive ./model --no-batch
```

### Readable transcripts

`--echo` writes each input line to stdout ahead of its output, which is handy when capturing a transcript of a piped run. Comment lines are not echoed.

```bash
printf "ls tables\nexit\n" | te interactive ./model --echo
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

| 值                                   | Effect                                                                                                                                                    |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `auto` (default) | Launch the REPL only when all three streams are attached to a TTY. Otherwise fall through to normal parse.                |
| `always`                            | Launch the REPL regardless of stream redirection. Useful when you always want an interactive session.                     |
| `never`                             | Never auto-launch the REPL. `te` on its own prints help, matching the pre-0.6.0 behavior. |

Change it globally with:

```bash
te config set launchInteractiveMode never    # keep the classic help-on-empty behavior
te config set launchInteractiveMode auto     # restore the default
```

Override for a single invocation via the `TE_INTERACTIVE` environment variable (same values), or pass `--non-interactive` on the command line - both force `never` for that call, so `te --non-interactive` prints help instead of launching the REPL.

## 何时使用交互模式与非交互模式

- **交互模式** 最适合探索、学习 CLI、针对单个模型执行一次性批量编辑，以及演示。
- **非交互模式**（在 `te interactive` 之外的默认模式）适用于编写脚本、自动化或在 CI 中运行。 见 @te-cli-automation 和 @te-cli-cicd。

两者共用同一套命令树——你在 `te interactive` 中运行的任何命令，只要在前面加上 `te` 前缀，就可以直接粘贴到 Shell 脚本中。

## 相关页面

- @te-cli-commands - 完整的命令参考。
- @te-cli-auth - 连接到 Workspace，并管理配置文件。
- @te-cli-automation - 何时应退出交互模式。
