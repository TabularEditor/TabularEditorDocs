---
uid: te-cli-interactive
title: 交互模式
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

# 交互模式

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

交互模式是一种引导式的读-求值-打印循环（REPL），用于从终端探索模型。 对命令行新手来说，这是最温和的入门方式；而在针对单个模型进行临时操作时，它也是一个便捷的 Workspace。 对命令行新手来说，这是最温和的入门方式；而在针对单个模型进行临时操作时，它也是一个便捷的 Workspace。

## 启动会话

要启动会话，请运行以下任一命令：

```bash
te interactive                              # Start and connect to a model later
te interactive ./model                      # Start with a local model
te interactive -s MyWorkspace -d MyModel    # Start with a remote model
```

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
- `[...]` — 用方括号括起来的分段。 `[...]` — 用方括号括起来的分段。 **方括号会在生成的参数中保留**，因此像 `'Internet Sales'[Sales Amount]` 这样的路径会以单个令牌的形式传递给命令，路径解析器随后可以将其重新解释为 DAX 引用。 出于同样的原因，成对的右方括号 (`]]`) 也会按原样保留。 出于同样的原因，成对的右方括号 (`]]`) 也会按原样保留。

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

启用交互模式后，需要补全输入的命令会提示你输入，而不是直接失败。 启用交互模式后，需要补全输入的命令会提示你输入，而不是直接失败。 不带子命令运行 `auth` 时，会打开一个选择界面，让你在 Login / Status / Logout 之间选择；不带 `--force` 运行 `deploy` 时，会显示摘要并要求确认（安全的默认值为 `n`）。

如果想在当前会话中为单个命令禁用提示，传入 `--non-interactive`。

## 何时使用交互模式与非交互模式

- **交互模式** 最适合探索、学习 CLI、针对单个模型执行一次性批量编辑，以及演示。
- **非交互模式**（在 `te interactive` 之外的默认模式）适用于编写脚本、自动化或在 CI 中运行。 见 @te-cli-automation 和 @te-cli-cicd。 见 @te-cli-automation 和 @te-cli-cicd。

两者共用同一套命令树——你在 `te interactive` 中运行的任何命令，只要在前面加上 `te` 前缀，就可以直接粘贴到 Shell 脚本中。

## 相关页面

- @te-cli-commands - 完整的命令参考。
- @te-cli-auth - 连接到 Workspace，并管理配置文件。
- @te-cli-automation - 何时应退出交互模式。
