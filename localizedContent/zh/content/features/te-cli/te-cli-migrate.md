---
uid: te-cli-migrate
title: 从 TE2 命令行迁移
author: Peer Grønnerup
updated: 2026-05-06
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      none: true
    - product: Tabular Editor CLI
      full: true
---

# 从 TE2 命令行迁移

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

对于在现有构建管道中使用 TE2 风格标志（`-S`、`-A`、`-D`、`-O`、`-C` 等）调用 `TabularEditor.exe` 的团队， 可以逐步采用新的 CLI。 Tabular Editor CLI 同时支持两种命令形式：新的基于子命令的形式（如 `te deploy`、`te bpa run` 等） 以及通过内置兼容层提供支持的旧版 TE2 标志语法。

有关旧版 TE2 的 Windows 命令行参考，请参阅 @command-line-options。

## TE2 兼容模式的工作方式

可通过以下三种方式之一激活 TE2 兼容模式：

1. **二进制名称。** 将 `te` 重命名为 `te2`（或为其创建符号链接），CLI 就会以与 TE2 完全一致的模式运行。 这是直接替换的做法：在现有管道中把 `TabularEditor.exe` 换成 `te2`，原来的参数照样可用。
2. **环境变量。** 在调用 `te` 之前设置 `TE_COMPAT=te2`，即可强制启用 TE2 模式。
3. **自动检测。** 如果第一个参数不是 `te` 子命令（`load`、`deploy` 等）， 并且只要在参数列表的任意位置出现了至少一个可识别的 TE2 标志，CLI 就会自动切换到 TE2 模式。 这意味着大多数现有的 TE2 调用无需任何更改即可运行。

```bash
# All three are equivalent - each runs in TE2 mode
./te2 Model.bim -S fix.csx -D "localhost\tabular" MyDB -O
TE_COMPAT=te2 te Model.bim -S fix.csx -D "localhost\tabular" MyDB -O
te Model.bim -S fix.csx -D "localhost\tabular" MyDB -O
```

> [!NOTE]
> TE2 模式会运行与 `TabularEditor.exe` 相同的 `Load → Scripts → Schema Check → Save → BPA → Deploy → TRX` 流程，包括与上下文相关的标志行为（例如，`-D` 之后的 `-S` 表示 `-SHARED`，而不是 `-SCRIPT`）。

## Migrate 命令

可将 `te migrate` 作为实时参考，用来了解 TE2 标志如何映射到新的 CLI。 它会输出一张彩色表格，列出每个已知 TE2 标志、其状态（受支持、已重命名、计划支持）以及对应的 `te` 命令。

```bash
te migrate                   # Full flag mapping table
te migrate -A                # Look up a single flag
te migrate --output-format json     # Machine-readable mapping
```

请参考 `te migrate` 命令的输出，查看与您已安装的 CLI 版本相对应的当前映射。

## 标志映射（整理的子集）

以下是最常用标志的简要汇总，并非完整列表。 运行 `te migrate` 查看完整列表。

| TE2 标志                                    | 新 CLI 等效参数                                                        | 说明                                                                     |
| ----------------------------------------- | ----------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `file`（位置参数）                              | `te <command> <path>` 或使用全局参数 `--model`                           | 在大多数命令中，这是第一个位置参数。                                                     |
| `server`、`database`                       | `te connect <server>` 或 `te deploy <server> <database>`           | Server 参数不再是全局位置参数。                                                    |
| `-L` / `-LOCAL`                           | `te connect --local`                                              | 仅限 Windows。                                                            |
| `-S` / `-SCRIPT`                          | `te script -s <file.csx>` 或 `-e "code"`                           | 支持多个脚本、内联代码和 stdin。                                                    |
| `-A` / `-ANALYZE`                         | `te bpa run --rules <file-or-url>`                                | 支持 `--fail-on`、`--fix` 和多个规则文件。                                        |
| `-AX` / `-ANALYZEX`                       | `te bpa run --rules <file>`（不带 `--model-rules`）                   | 现在默认会排除嵌入模型的规则。                                                        |
| `-B` / `-BIM`                             | `te save <model> -o <file.bim> --serialization bim`               |                                                                        |
| `-F` / `-FOLDER`                          | `te save <model> -o <dir> --serialization te-folder`              | 在 `-D` 之后，TE2 的 `-F` 表示 `-FULL`；参见 `--deploy-full`。                    |
| `-TMDL`                                   | `te save <model> -o <dir> --serialization tmdl`                   | TMDL 是默认保存格式。                                                          |
| `-D` / `-DEPLOY`                          | `te deploy <server> <database> <model>`                           | 这是一个独立的命令，使用具名选项。                                                      |
| `-O` / `-OVERWRITE`                       | （默认）或使用 `--create-only` 选择不覆盖                                     | 在新的 CLI 中，覆盖是默认行为。                                                     |
| `-C` / `-CONNECTIONS`                     | `te deploy --deploy-connections`                                  |                                                                        |
| `-P` / `-PARTITIONS` 分区                   | `te deploy --deploy-partitions` 部署分区                              |                                                                        |
| `-Y` / `-SKIPPOLICY`                      | `te deploy --deploy-partitions --skip-refresh-policy` 部署分区并跳过刷新策略 | 需要 `--deploy-partitions`。                                              |
| `-SHARED`                                 | `te deploy --deploy-shared-expressions`                           | 在 `-D` 之后，TE2 的 `-S` 表示 `-SHARED`。                                     |
| `-R` / `-ROLES` 角色                        | `te deploy --deploy-roles`                                        |                                                                        |
| `-M` / `-MEMBERS`                         | `te deploy --deploy-role-members`                                 |                                                                        |
| `-FULL`（在 `-D` 之后）                        | `te deploy --deploy-full`                                         | 等同于：覆盖 + 连接 + 分区 + 共享 + 角色 + 角色成员。                                     |
| `-X` / `-XMLA <file>`                     | `te deploy ... --xmla <file>`                                     | 输出到 stdout 时使用 `-`。                                                    |
| `-V` / `-VSTS`                            | 在 `validate`、`bpa run` 和 `deploy` 命令中使用 `--ci vsts`               | 会向 stderr 输出 `##vso[...]` 注释。                                          |
| `-G` / `-GITHUB`                          | `--ci github`                                                     | 会输出 `::error::` / `::warning::` 注释。                                    |
| `-T` / `-TRX <file>`                      | 在 `validate`、`bpa run` 和 `test run` 命令中使用 `--trx <file>`          | 用于 Azure DevOps 测试发布的 VSTEST `.trx` 文件。                                |
| `-W` / `-WARN`                            | （默认）                                                              | 部署结果中始终会 Report 警告。                                                    |
| `-E` / `-ERR`                             | （默认）                                                              | 出现 DAX 错误时，部署会返回非零退出代码。                                                |
| `-SC` / `-SCHEMACHECK`                    | _尚未实现。_                                                           | TE2 架构检查会连接到真实的数据源。 这不同于 `te validate`（DAX 语义验证，不连接数据源）。               |
| `-L` / `-LOGIN <user> <pass>`（位于 `-D` 之后） | `te auth login -u <id> -p <secret> -t <tenant>`                   | 使用服务主体或基于环境变量的凭据。 登录状态会被缓存，因此后续命令会静默获取令牌——见 @te-cli-auth。 |

## 迁移指南

从基于 TE2 的管道迁移到新 CLI 的推荐路径：

1. **直接替换。** 在现有管道中用 `te`（或 `te2`）替换 `TabularEditor.exe`。 确认管道仍可正常运行——TE2 兼容层会让大多数调用方式保持不变。
2. **逐步替换标志。** 每次转换一组标志：
   - 先从 `-A` / `-AX` → `te bpa run` 开始，以获得更丰富的 BPA 输出（`--fail-on`、`--fix`、`--trx`）。
   - 然后把 `-D` 替换为 `te deploy`，以获得更细粒度的部署控制。
   - 最后：`-V` / `-G` → `--ci vsts` / `--ci github`。
3. **切换为非交互式 CI 参数。** 给每个 `te` 命令加上 `--non-interactive --ci <vsts|github>`，并去掉任何 `start /wait` 包装命令——新的 CLI 是标准控制台可执行文件，不需要它们。
4. **采用服务主体身份验证。** 将 `-D -L <user> <pass>` 替换为 `te auth login -u …… -p …… -t ...`，或在管道中使用基于环境变量凭据的步骤。 见 @te-cli-auth。

## 重要差异

- **部署时的 BPA 检查。** `te deploy` 现在默认会在部署前运行 BPA，作为前置检查。 使用 `--skip-bpa` 可保留旧行为，或使用 `--fix-bpa` 在部署前自动修复违规项。 见 @te-cli-config。
- **部署时的交互式确认。** 默认情况下，`te deploy` 会提示确认（为安全起见，默认回答为 `n`）。 CI 管道必须指定 `--force`。
- **结构化输出。** 每个命令都支持 `--output-format json`，以生成机器可读输出——参见 @te-cli-automation。
- **无需 `start /wait`。** 新 CLI 是普通的控制台可执行文件；你可以在 shell 脚本、PowerShell 和 CI 任务中直接调用它。
- **跨平台。** CLI 可在 Windows、macOS 和 Linux 上运行。 本地 SSAS 和 Power BI Desktop 连接仍仅支持 Windows。

## 相关页面

- @command-line-options —— 旧版 TE2 命令行参考。
- @te-cli-commands —— 新 CLI 的完整命令参考。
- @te-cli-cicd —— 适用于 GitHub Actions 和 Azure DevOps 的管道示例。
