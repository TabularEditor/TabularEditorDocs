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

| 命令                  | 用途                                                                   |
| ------------------- | -------------------------------------------------------------------- |
| `help` 或 `?`        | 列出可用命令。                                                              |
| `status` 或 `pwd`    | 显示当前活动的模型/连接。                                                        |
| `save`              | 将所有暂存在内存中的编辑提交并写回模型源。                                                |
| `revert`            | 丢弃自上次保存以来的所有暂存编辑。                                                    |
| `clear` 或 `cls`     | 清空屏幕。                                                                |
| `exit`、`quit` 或 `q` | 退出交互模式。 如果暂存编辑尚未保存，系统会要求你确认（默认值为 `n`）；`exit --force` 会直接丢弃这些编辑而不再询问。 |

会话中的 `save` 不接受任何参数；如果要将模型重新序列化到其他格式或位置，请使用 `save-as`（例如 `save-as -o ./out --serialization bim`），与会话外完全相同。

## 暂存编辑

在会话中，修改类命令 (`set`, `add`, `remove`, `move`, `script`, `macro run`, ...) 会先将更改暂存在内存中，而不是写回源文件；只要存在未保存的暂存编辑，提示符就会显示一个指示标记。 内置的 `save` 命令会提交所有已暂存的更改；`revert` 会丢弃所有已暂存的更改。

每个修改类命令也可以自行决定处理方式：`--save` 会立即保存该命令的更改，`--stage` 会将其保留在内存中（默认行为），而 `--revert` 会在显示该命令的效果后回滚更改——很适合用来做一次“这会产生什么效果？”的试探。 这三者互斥，并且 `--stage`/`--revert` 仅在会话内可用。

每个命令的默认行为由配置键 `interactiveEditMode` 决定（`stage` | `save` | `revert`）——请参阅 @te-cli-config。

暂存编辑绝不会被悄悄丢弃。 如果在仍保留这些编辑的情况下关闭会话——无论是使用 `exit`、按 **Ctrl+D**，还是到达管道输入的末尾——都会先检查是否存在未保存的更改。 如果存在未保存的更改且当前终端可交互，系统会要求你确认，默认选项为“否”；如果你选择不退出，就会返回提示符，且这些编辑会原样保留。 如果无法进行确认（例如 stdin 被管道传入或重定向，或使用了 `--non-interactive`），会话会输出一条警告，说明有哪些未保存的更改，然后以失败退出码退出，而不是成功退出码。 无论哪种退出方式，都不会在退出时自动保存：请先运行 `save`，或者使用 `exit --force` 有意丢弃这些编辑。

## 行编辑与按键

提示符支持单行编辑：

- **Left/Right** 移动光标；**Home/End**（也可用 **Ctrl+A**/**Ctrl+E**）跳到行首/行尾；**Backspace/Delete** 在当前位置删除字符。
- **Up/Down** 浏览命令历史记录，并且该历史会在不同会话之间保留。
- **Ctrl+C** 会取消当前命令而不退出会话，并永久放弃那条输入到一半的命令行——它不会被执行，按 **Up** 也无法找回，而且不会加入历史记录。
- 在空提示符下按 **Ctrl+D** 可退出（Windows 上为先按 **Ctrl+Z** 再按 **Enter**）。

会话内没有 Tab 补全功能；通过 `te completion` 启用的 shell 补全只对外层 shell 生效。

## 引导式提示

启用交互模式后，需要补全输入的命令会提示你输入，而不是直接失败。 运行 `auth` 时如果不带子命令，会打开一个选择器，让你在 Login / Status / Logout 之间选择；运行 `deploy --execute` 或 `refresh --execute` 时如果不带 `--force`，会先显示摘要并请求确认（`n` 是更安全的默认选项）。 不带 `--execute` 的 `deploy` 或 `refresh` 属于试运行：它会打印将要发送的 TMSL，因此不会弹出确认提示。

如果想在当前会话中为单个命令禁用提示，传入 `--non-interactive`。

## 管道与重定向输入

交互模式也支持通过管道传入或重定向的 stdin，因此你可以用脚本驱动同一个 REPL，而不必手动逐条输入。 每一行输入都会作为一条命令执行，就像你在提示符处输入它一样；当输入耗尽时，会话将退出（或者在读到 `exit` 这一行时退出）。 如果此时暂存的编辑仍未保存，会话会发出警告并以非零退出码退出——会产生更改的脚本应以 `save` 结束（或使用 `exit --force` 有意丢弃更改）。

```bash
printf "ls\nexit\n" | te interactive --model ./model    # bash / git-bash
te interactive --model ./model < script.te              # redirected file
```

```bat
(echo ls & echo exit) | te interactive --model .\model  :: Windows cmd.exe
```

在交互式会话中会拒绝使用 `-` 这一 stdin 约定（`set -p Expression=-`、`query -q -` 等），因为 stdin 由会话本身占用——请在外层 shell 中使用。

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

| 值          | 效果                                    |
| ---------- | ------------------------------------- |
| `auto`（默认） | 仅当三个流都连接到 TTY 时才启动 REPL。 否则回退到常规解析流程。 |
| `always`   | 无论流是否被重定向，都启动 REPL。 适合始终需要交互式会话的情况。   |
| `never`    | 从不自动启动 REPL。 `te` 单独运行时会输出帮助信息。       |

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
