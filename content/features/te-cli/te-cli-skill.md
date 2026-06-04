---
uid: te-cli-skill
title: AI Agent Skill
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
# AI Agent Skill

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

The Tabular Editor CLI ships with a drop-in **agent skill** that teaches AI coding agents how to drive the `te` command-line interface. It's a single Markdown file, [`SKILL.md`](https://github.com/TabularEditor/CLI/tree/main/skill), packed with the CLI's conventions, command reference, workflows, and gotchas. Once installed, an agent answers "deploy this model" or "add a measure that calculates margin" with idiomatic `te` invocations instead of guessing or hallucinating flags.

The skill is maintained in the public [TabularEditor/CLI](https://github.com/TabularEditor/CLI/tree/main/skill) repository and tracks the preview surface of the CLI as it evolves.

## What a skill is

A skill is a Markdown file an AI agent loads on demand based on your prompt. Its YAML frontmatter (`name`, `description`, `version`) tells the agent **when** to load it and **what** it covers. The Markdown body teaches the agent **how** to do the job.

## What the skill covers

The skill teaches the agent the full `te` surface:

- every `te` command across all families - load, save, init, deploy, refresh, bpa, validate, query, script, format, and more
- authentication patterns - interactive, service principal with secret or certificate, environment variables, managed identity
- object path grammar - slash form, DAX form, and wildcards
- the staging model - `--save`, `--stage`, and `--revert` behavior
- TE2 to CLI migration mapping
- CI/CD recipes for GitHub Actions and Azure DevOps
- output formats, exit codes, environment variables, and config keys
- a cheatsheet of common `-q` properties
- the gotchas that trip up agents in practice

This is the same ground the rest of this section documents for humans. See @te-cli-commands for the command reference, @te-cli-auth for authentication, and @te-cli-cicd for pipeline patterns.

## Download the skill file

The skill is a single file: [`SKILL.md`](https://github.com/TabularEditor/CLI/blob/main/skill/SKILL.md).

1. Open [`SKILL.md`](https://github.com/TabularEditor/CLI/blob/main/skill/SKILL.md) on GitHub.
2. Click **Download raw file** (top-right of the file viewer).
3. Save the file somewhere convenient.

You'll move this file to a tool-specific location in the install steps below. To see what changed between versions before grabbing a newer copy, check the [CHANGELOG](https://github.com/TabularEditor/CLI/blob/main/skill/CHANGELOG.md).

## Choose an install scope

Every agent supports two install scopes:

- **Project scope** - the skill is available only in one project or repository. Use this when not every project touches semantic models.
- **User scope** - the skill is available in every project on your machine. Use this if you work with semantic models across many repos.

## Install for Claude Code

Claude Code loads skills from a named folder under `.claude/skills/`. The `description` field is matched against your prompts, so the skill only loads when relevant - it costs no tokens when you're working on unrelated code.

**Project scope** - the skill loads only inside this project:

1. In your project root, create the folder `.claude/skills/te-cli/`.
2. Place the downloaded `SKILL.md` inside that folder.

The final path is `<your-project>/.claude/skills/te-cli/SKILL.md`.

**User scope** - the skill loads in every project for the current user:

1. Create a `te-cli` folder inside your user-level Claude skills directory:
   - **macOS / Linux:** `~/.claude/skills/te-cli/`
   - **Windows:** `%USERPROFILE%\.claude\skills\te-cli\` (typically `C:\Users\<you>\.claude\skills\te-cli\`)
2. Place the downloaded `SKILL.md` inside that folder.

> [!NOTE]
> Claude Code watches skill directories and picks up new or edited skills within the current session - no restart needed. The exception is creating a `.claude/skills/` directory that did not exist when the session started: restart Claude Code once so it begins watching the new directory.

### Verify it loaded

Inside a Claude Code session, run:

```
/skills
```

You should see `te-cli` in the list. If it's missing, confirm the file path and that the file starts with `---` and has `name: te-cli` on the second line, then restart Claude Code.

For a functional smoke test, ask:

```
what does `te deploy --xmla` do?
```

Claude answers with the documented behavior - it generates a TMSL/XMLA script to stdout instead of deploying - which confirms the skill is loaded and in use.

## Install for Claude.ai and Claude Desktop

Claude.ai (web and desktop) has a built-in **Skills** feature. Skills require code execution, and you upload them as a ZIP of the skill folder rather than the bare `SKILL.md`.

1. Enable code execution: go to **Settings > Capabilities** and turn on **Code execution and file creation**. On Team and Enterprise plans, an owner enables this in organization settings.
2. Put the downloaded `SKILL.md` inside a folder named `te-cli`, then compress that folder into `te-cli.zip`.
3. Go to **Settings > Capabilities > Skills** (also reachable under **Customize > Skills**).
4. Click **+**, choose **Upload skill**, and select `te-cli.zip`. Claude reads the `SKILL.md` inside and shows a summary of the skill.
5. Toggle the skill on. It loads automatically when you mention `te` or a related concept.

Custom skills you upload are private to your account unless an owner enables organization-wide sharing on Team or Enterprise.

See Anthropic's [Skills help article](https://support.claude.com/en/articles/12512180-use-skills-in-claude) for the current UI flow if the wording has changed.

## Install for GitHub Copilot

GitHub Copilot in VS Code supports the Agent Skills open standard natively - the same `SKILL.md` format Claude Code and Codex use. This is the recommended approach because the skill loads only when relevant. For Copilot setups that predate Agent Skills, fall back to the always-on custom-instructions file below.

### Agent Skills (VS Code)

Place the skill in a named folder under a skills directory. The folder name must match the `name` field in the frontmatter, so use `te-cli`, and keep the YAML frontmatter intact.

- **Workspace scope:** `.github/skills/te-cli/SKILL.md` (Copilot also reads `.claude/skills/` and `.agents/skills/`).
- **User scope:** `~/.copilot/skills/te-cli/SKILL.md` (Copilot also reads `~/.claude/skills/` and `~/.agents/skills/`).

Type `/` in Copilot Chat to confirm `te-cli` appears as a slash command, or open the Agent Customizations editor with **Chat: Open Customizations** from the Command Palette.


## Install for OpenAI Codex CLI

Codex CLI loads skills natively from a named folder under `.agents/skills/`, the same directory-based model as Claude Code. Keep the YAML frontmatter - Codex requires the `name` and `description` fields and uses the description to decide when to load the skill.

**Project scope** - the skill loads only inside this project:

1. In your project root, create the folder `.agents/skills/te-cli/`.
2. Place the downloaded `SKILL.md` inside that folder.

Codex scans upward from your working directory, so a skill committed at the repository root (`$REPO_ROOT/.agents/skills/te-cli/`) is shared across everyone working in the repo.

**Personal scope** - the skill loads in every project for the current user:

1. Create the folder `te-cli` inside your personal Codex skills directory: `~/.agents/skills/te-cli/`.
2. Place the downloaded `SKILL.md` inside that folder.

Run `/skills` in the Codex CLI or IDE to confirm `te-cli` is listed, and type `$` to mention a skill explicitly.

## Install for generic agents

For tools that follow the [`AGENTS.md` convention](https://agents.md) or accept an arbitrary instructions file - Aider, Continue, custom in-house agents:

1. Download `SKILL.md`.
2. Remove the YAML frontmatter block at the top (everything between the first and second `---` lines, including those lines).
3. Rename the file to `AGENTS.md` and place it at your project root, or wherever the tool expects its instructions file.
4. The next agent invocation in that project picks up the instructions.

## Update the skill

To pull a newer version:

1. Open [`SKILL.md`](https://github.com/TabularEditor/CLI/blob/main/skill/SKILL.md) on GitHub and use **Download raw file** to grab the latest copy.
2. Replace the file you previously installed:
   - **Native skills (Claude Code, Codex, Copilot Agent Skills):** overwrite `SKILL.md` in the skill folder.
   - **Claude.ai / Desktop:** re-zip the `te-cli` folder and re-upload it through the Skills UI.
   - **Instruction-file installs (Copilot custom instructions, AGENTS.md):** re-paste the body into `.github/copilot-instructions.md` or `AGENTS.md`.

See the [CHANGELOG](https://github.com/TabularEditor/CLI/blob/main/skill/CHANGELOG.md) for what changed between versions.

## Next steps

- @te-cli-install - download, install, and verify the CLI itself.
- @te-cli-auth - authenticate to Power BI, Fabric, and Azure Analysis Services.
- @te-cli-commands - full command reference.
- @te-cli-automation - structured output and scripting patterns.
- @te-cli-cicd - GitHub Actions and Azure DevOps pipelines.
