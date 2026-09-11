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

交互模式是一种引导式的读-求值-打印循环（REPL），用于从终端探索模型。 对命令行新手来说，这是最温和的入门方式；而在针对单个模型进行临时操作时，它也是一个便捷的 Workspace。

## 启动会话

要启动会话，请运行以下任一命令：

```bash
te interactive                              # Start and connect to a model later
te interactive --model ./model              # Start with a local model
te interactive -s MyWorkspace -d MyModel    # Start with a remote model
```

`te interactive` 提供一些用于调整会话的标志：

- `--no-banner` - 启动时跳过欢迎横幅。
- `--echo` - 在输出结果之前，先将每条执行的命令回显到 stdout。 在用脚本驱动 REPL 时，便于记录日志。
- `--batch` - 非交互式批处理模式：从 stdin 逐行读取命令，依次执行，并在遇到 EOF 时退出。 当 stdin 被重定向时会自动启用。
- `--no-batch` - 即使 stdin 被重定向，也强制使用交互式 TTY 模式（与 `--batch` 互斥）。

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

启用交互模式后，需要补全输入的命令会提示你输入，而不是直接失败。 Running `auth` without a subcommand opens a picker for Login / Status / Logout; running `deploy --execute` or `refresh --execute` without `--force` shows a summary and asks for confirmation (`n` is the safe default). A `deploy` or `refresh` without `--execute` is a dry run that prints the TMSL it would send, so it never prompts.

如果想在当前会话中为单个命令禁用提示，传入 `--non-interactive`。

## 管道与重定向输入

交互模式也支持通过管道传入或重定向的 stdin，因此你可以用脚本驱动同一个 REPL，而不必手动逐条输入。 每一行输入都会作为一条命令执行，就像你在提示符处输入它一样；当输入耗尽时，会话将退出（或者在读到 `exit` 这一行时退出）。 If staged edits are still unsaved at that point, the session warns and exits non-zero - end a mutating script with `save` (or `exit --force` to discard on purpose).

```bash
printf "ls\nexit\n" | te interactive --model ./model    # bash / git-bash
te interactive --model ./model < script.te              # redirected file
```

```bat
(echo ls & echo exit) | te interactive --model .\model  :: Windows cmd.exe
```

The `-` stdin convention (`set -p Expression=-`, `query -q -`, and so on) is refused inside the interactive session, because the session itself owns stdin - use it from the outer shell instead.

以 `#` 开头的行会被视为注释并跳过，因此你可以为脚本文件添加注释：

```
# script.te - inspect the model, then exit
ls tables
ls measures
exit
```

### 批处理模式和退出代码

当 stdin 通过管道传入时，`--batch` 是 **默认**：会话会在第一条失败的命令处停止，并以非零退出代码退出，因此可以安全地将管道运行用作构建或 CI 步骤。 使用 `--no-batch` 即可在某条命令失败后继续运行剩余各行。 运行成功时，进程退出代码为 `0`；在批处理模式下如果命令失败，则为非零。

```bash
# Default when piped: stop at the first failing command, exit non-zero
printf "bpa run --fail-on error\ndeploy --execute --force\nexit\n" | te interactive --model ./model

# Run every line regardless of failures
printf "bpa run --fail-on error\ndeploy --execute --force\nexit\n" | te interactive --model ./model --no-batch
```

### 便于阅读的执行记录

`--echo` 会在对应输出之前将每一行输入写入 stdout，这在捕获管道运行的执行记录时很方便。 注释行不会被回显。

```bash
printf "ls tables\nexit\n" | te interactive --model ./model --echo
```

### 选项

| 选项            | 说明                                        |
| ------------- | ----------------------------------------- |
| `--no-banner` | 不显示欢迎横幅。                                  |
| `--echo`      | 将每一行输入回显到 stdout（便于生成管道运行的执行记录）。          |
| `--batch`     | 在第一个命令失败时即以非零状态码退出（当 stdin 通过管道输入时为默认行为）。 |
| `--no-batch`  | 即使 stdin 通过管道传入，出错后也继续执行。                 |

### 欢迎横幅与预览提示

会话开始时可能会出现两条不同的信息——不要把它们混为一谈：

- **欢迎横幅** 是在 [启动会话](#starting-a-session) 中介绍的交互式欢迎界面。 可使用 `--no-banner` 隐藏它。 当 stdin 通过管道传入时，本来就不会输出欢迎横幅，因此 `--no-banner` 只有在真正的交互式（TTY）会话中才会产生可见效果。
- **预览到期通知**（`This is an early preview release ...`）则是另一条信息。 它始终写入 **stderr**，并且**不受** `--no-banner` 影响。 可使用 `te config set hidePreviewNotice true` 隐藏它。

## 无参数调用时自动启动

在终端中不带任何参数运行 `te`，会直接进入交互式 REPL，因此探索模型就像打开 shell 后输入 `te` 一样快。 当 stdin、stdout 或 stderr 被重定向时（如管道输出、CI 流水线或脚本中），CLI 会转入常规解析流程并改为输出帮助——因此，不带子命令调用 `te` 的 shell 脚本仍会保持原有行为。

此行为由 `launchInteractiveMode` 配置项控制，提供三个取值：

| 值          | 效果                                                        |
| ---------- | --------------------------------------------------------- |
| `auto`（默认） | 仅当三个流都连接到 TTY 时才启动 REPL。 否则回退到常规解析流程。                     |
| `always`   | 无论流是否被重定向，都启动 REPL。 适合始终需要交互式会话的情况。                       |
| `never`    | 从不自动启动 REPL。 `te` on its own prints help. |

可通过以下方式全局更改：

```bash
te config set launchInteractiveMode never    # keep the classic help-on-empty behavior
te config set launchInteractiveMode auto     # restore the default
```

你也可以通过 `TE_INTERACTIVE` 环境变量仅对单次调用进行覆盖（取值相同），或在命令行中传入 `--non-interactive`——这两种方式都会在该次调用中强制设为 `never`，因此 `te --non-interactive` 会输出帮助信息，而不是启动 REPL。

## 何时使用交互模式与非交互模式

- **交互模式** 最适合探索、学习 CLI、针对单个模型执行一次性批量编辑，以及演示。
- **非交互模式**（在 `te interactive` 之外的默认模式）适用于编写脚本、自动化或在 CI 中运行。 见 @te-cli-automation 和 @te-cli-cicd。

两者共用同一套命令树——你在 `te interactive` 中运行的任何命令，只要在前面加上 `te` 前缀，就可以直接粘贴到 Shell 脚本中。

## 相关页面

- @te-cli-commands - 完整的命令参考。
- @te-cli-auth - 连接到 Workspace，并管理配置文件。
- @te-cli-automation - 何时应退出交互模式。
