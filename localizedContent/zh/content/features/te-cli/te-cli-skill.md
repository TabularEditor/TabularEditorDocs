---
uid: te-cli-skill
title: AI 智能体技能
author: Morten Lønskov
updated: 2026-06-04
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      none: true
    - product: Tabular Editor CLI
      full: true
---

# AI 智能体技能

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

Tabular Editor CLI 自带一个开箱即用的**智能体技能**，让 AI 编码智能体学会如何驱动 `te` 命令行界面。 它就是一个 Markdown 文件，[`SKILL.md`](https://github.com/TabularEditor/CLI/tree/main/skills/te-cli)，其中汇集了 CLI 的约定、命令参考、工作流和常见陷阱。 安装后，如果你说“部署这个模型”或“添加一个计算利润率的度量值”，智能体会给出符合 `te` 用法的命令，而不是靠猜测或臆造选项。

该技能在公开的 [TabularEditor/CLI](https://github.com/TabularEditor/CLI/tree/main/skills/te-cli) repository 中维护，并会随着 CLI 预览功能的演进持续更新。

## 什么是技能

技能是 AI 智能体根据你的提示按需加载的 Markdown 文件。 它的 YAML frontmatter（`name`、`description`、`version`）会告诉智能体**何时**加载它，以及它涵盖**哪些**内容。 Markdown 正文则教会智能体**如何**完成这项工作。

## 技能涵盖的内容

该技能会向智能体讲解 `te` 的完整功能：

- 所有系列的 `te` 命令——涵盖 load、save、init、deploy、refresh、bpa、validate、query、script、format 等
- 身份验证模式——交互式、使用机密或证书的服务主体、环境变量、托管标识
- 对象路径语法——斜杠形式、DAX 形式和通配符
- 暂存模型——`--save`、`--stage` 和 `--revert` 的行为
- TE2 到 CLI 的迁移映射
- 适用于 GitHub Actions 和 Azure DevOps 的 CI/CD 实践方案
- 输出格式、退出代码、环境变量和配置键
- 常用 `-q` 属性速查表
- 实践中容易让智能体出错的常见坑点

这些内容与本节其余部分面向人类读者的说明是同一套内容。 命令参考请参见 @te-cli-commands，身份验证请参见 @te-cli-auth，流水线模式请参见 @te-cli-cicd。

## 下载技能文件

该技能只有一个文件：[`SKILL.md`](https://github.com/TabularEditor/CLI/blob/main/skills/te-cli/SKILL.md)。

1. 在 GitHub 上打开 [`SKILL.md`](https://github.com/TabularEditor/CLI/blob/main/skills/te-cli/SKILL.md)。
2. 点击**下载原始文件**（位于文件查看器右上角）。
3. 将文件保存到一个方便的位置。

在下面的安装步骤中，你需要将此文件移动到工具专用的位置。 在下载较新版本之前，如果你想看看版本之间有哪些变更，可以查阅 [CHANGELOG](https://github.com/TabularEditor/CLI/blob/main/skills/te-cli/CHANGELOG.md)。

## 选择安装范围

每个代理都支持两种安装范围：

- **项目范围** - 技能仅在某个项目或 repository 中可用。 如果不是每个项目都会涉及语义模型，就用这个选项。
- **用户范围** - 技能在你这台机器上的所有项目中都可用。 如果你会在多个仓库中处理语义模型，就用这个选项。

## 为 Claude Code 安装

Claude Code 会从 `.claude/skills/` 下的命名文件夹中加载技能。 `description` 字段会和你的提示词匹配，所以技能只会在相关时才加载；当你处理无关代码时，它不会消耗任何 token。

**项目范围** - 技能只会在这个项目中加载：

1. 在项目根目录中，创建文件夹 `.claude/skills/te-cli/`。
2. 将下载的 `SKILL.md` 放入该文件夹中。

最终路径为 `<your-project>/.claude/skills/te-cli/SKILL.md`。

**用户范围** - 技能会在当前用户的所有项目中加载：

1. 在你的用户级 Claude 技能目录中创建 `te-cli` 文件夹：
   - **macOS / Linux：** `~/.claude/skills/te-cli/`
   - **Windows：** `%USERPROFILE%\\.claude\\skills\\te-cli\\`（通常为 `C:\\Users\\<you>\\.claude\\skills\\te-cli\\`）
2. 将下载的 `SKILL.md` 放入该文件夹中。

> [!NOTE]
> Claude Code 会监视技能目录，并在当前会话中识别新增或已编辑的技能，无需重启。 例外情况是：如果 `.claude/skills/` 目录在会话开始时并不存在，而你后来才创建它，则需要重启一次 Claude Code，让它开始监视这个新目录。

### 验证技能是否已加载

在 Claude Code 会话中，运行：

```
/skills
```

你应该能在列表中看到 `te-cli`。 如果没有，请确认文件路径无误，并且文件以 `---` 开头、第二行包含 `name: te-cli`，然后重启 Claude Code。

要进行功能性冒烟测试，可以这样提问：

```
what does `te deploy --xmla` do?
```

Claude 会按文档所述的行为作答——它会将 TMSL/XMLA 脚本输出到 stdout，而不是直接部署——这就表明该技能已加载并在使用中。

## 在 Claude.ai 和 Claude Desktop 中安装

Claude.ai（网页和桌面版）内置了 **Skills** 功能。 Skills 需要启用代码执行，并且上传时应使用技能文件夹打包成的 ZIP，而不是单独的 `SKILL.md` 文件。

1. 启用代码执行：前往 **Settings > Capabilities**，并开启 **Code execution and file creation**。 在 Team 和 Enterprise 计划中，所有者需要在组织设置里启用这个功能。
2. 将下载的 `SKILL.md` 放入名为 `te-cli` 的文件夹中，然后将该文件夹压缩为 `te-cli.zip`。
3. 前往 **Settings > Capabilities > Skills**（也可通过 **Customize > Skills** 进入）。
4. 点击 **+**，选择 **Upload skill**，然后选中 `te-cli.zip`。 Claude 会读取里面的 `SKILL.md`，并显示这个技能的摘要。
5. 开启这个技能。 当你提到 `te` 或相关概念时，它会自动加载。

你上传的自定义技能默认只有你的账户能看到，除非 Team 或 Enterprise 的所有者启用了组织范围共享。

如果界面文案有变化，可以查看 Anthropic 的 [Skills 帮助文章](https://support.claude.com/en/articles/12512180-use-skills-in-claude)，了解当前的 UI 流程。

## 在 GitHub Copilot 中安装

VS Code 中的 GitHub Copilot 原生支持 Agent Skills 开放标准——也就是 Claude Code 和 Codex 使用的同一种 `SKILL.md` 格式。 这是推荐的方式，因为技能只会在相关时加载。 如果你的 Copilot 配置早于 Agent Skills 推出，请改用下方这个始终启用的自定义说明文件。

### Agent Skills（VS Code）

把技能放到 skills 目录下一个单独命名的文件夹里。 文件夹名称必须与 frontmatter 中的 `name` 字段一致，因此请使用 `te-cli`，并保持 YAML frontmatter 完整不变。

- **Workspace 作用域：** `.github/skills/te-cli/SKILL.md`（Copilot 也会读取 `.claude/skills/` 和 `.agents/skills/`）。
- **用户范围：** `~/.copilot/skills/te-cli/SKILL.md`（Copilot 也会读取 `~/.claude/skills/` 和 `~/.agents/skills/`）。

在 Copilot Chat 中输入 `/`，确认 `te-cli` 显示为斜杠命令；或者使用命令面板中的 **Chat: Open Customizations** 打开 Agent 自定义编辑器。

## 在 OpenAI Codex CLI 中安装

Codex CLI 会直接从 `.agents/skills/` 下的命名文件夹中加载技能，和 Claude Code 一样采用基于目录的模式。 请保留 YAML frontmatter——Codex 要求包含 `name` 和 `description` 字段，并会根据 `description` 来决定何时加载该技能。

**项目范围**——该技能只会在这个项目中加载：

1. 在项目根目录中创建文件夹 `.agents/skills/te-cli/`。
2. 将下载的 `SKILL.md` 放入该文件夹中。

Codex 会从你的工作目录向上扫描，因此提交在 repository 根目录（`$REPO_ROOT/.agents/skills/te-cli/`）的技能，会在该 repository 中的所有协作者之间共享。

**个人范围**——该技能会在你的每个项目中加载：

1. 在你的个人 Codex 技能目录中创建 `te-cli` 文件夹：`~/.agents/skills/te-cli/`。
2. 将下载的 `SKILL.md` 放入该文件夹中。

在 Codex CLI 或 IDE 中运行 `/skills`，确认列表中有 `te-cli`，并输入 `te-cli` 以显式指定该技能。

## 为通用 Agent 安装

对于遵循 [`AGENTS.md` convention](https://agents.md) 或支持使用任意说明文件的工具——Aider、Continue、自定义内部 Agent：

1. 下载 `SKILL.md`。
2. 删除顶部的 YAML frontmatter 块（也就是第一处和第二处 `---` 之间的所有内容，包括这两行本身）。
3. 将文件重命名为 `AGENTS.md`，并放到项目根目录，或该工具预期的说明文件位置。
4. 这个项目中下一次运行 Agent 时，就会读取这些说明。

## 更新技能

要获取更新版本：

1. 在 GitHub 上打开 [`SKILL.md`](https://github.com/TabularEditor/CLI/blob/main/skills/te-cli/SKILL.md)，然后使用 **Download raw file** 下载最新副本。
2. 替换你之前安装的文件：
   - **原生技能（Claude Code、Codex、Copilot Agent Skills）：** 覆盖技能文件夹中的 `SKILL.md`。
   - **Claude.ai / Desktop：** 重新将 `te-cli` 文件夹打包成 ZIP 文件，再通过 Skills UI 重新上传。
   - \*\*通过说明文件安装（Copilot 自定义指令、AGENTS.md）：\*\*请将正文重新粘贴到 `.github/copilot-instructions.md` 或 `AGENTS.md`。

查看 [CHANGELOG](https://github.com/TabularEditor/CLI/blob/main/skills/te-cli/CHANGELOG.md) 了解各版本之间的变更。

## 后续步骤

- @te-cli-install - 下载、安装并验证 CLI 本身。
- @te-cli-auth - 对 Power BI、Fabric 和 Azure Analysis Services 进行身份验证。
- @te-cli-commands - 完整命令参考。
- @te-cli-automation - 结构化输出与脚本模式。
- @te-cli-cicd - GitHub Actions 和 Azure DevOps 管道。
