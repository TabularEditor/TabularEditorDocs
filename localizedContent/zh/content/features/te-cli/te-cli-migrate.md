---
uid: te-cli-migrate
title: 从 TE2 命令行迁移
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

# 从 TE2 命令行迁移

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

对于在现有构建管道中使用 TE2 风格标志（`-S`、`-A`、`-D`、`-O`、`-C` 等）调用 `TabularEditor.exe` 的团队， 可以逐步采用新的 CLI。 Tabular Editor CLI 同时支持两种命令形式：新的基于子命令的形式（如 `te deploy`、`te bpa run` 等） 以及通过内置兼容层提供支持的旧版 TE2 标志语法。

有关旧版 TE2 的 Windows 命令行参考，请参阅 @command-line-options。

## TE2 兼容模式的工作方式

可通过以下三种方式之一激活 TE2 兼容模式：

1. **二进制名称。** 将 `te` 重命名为 `te2`（或为其创建符号链接），CLI 就会以与 TE2 完全一致的模式运行。 这是直接替换的做法：在现有管道中把 `TabularEditor.exe` 换成 `te2`，原来的参数照样可用。
2. **环境变量。** 在调用 `te` 之前设置 `TE_COMPAT=te2`，即可强制启用 TE2 模式。
3. **自动检测。** 如果第一个参数不是 `te` 子命令（`deploy`、`validate` 等） 并且只要在参数列表的任意位置出现了至少一个可识别的 TE2 标志，CLI 就会自动切换到 TE2 模式。 这意味着大多数现有的 TE2 调用无需任何更改即可运行。

```bash
# All three are equivalent - each runs in TE2 mode
./te2 Model.bim -S fix.csx -D "localhost\tabular" MyDB -O
TE_COMPAT=te2 te Model.bim -S fix.csx -D "localhost\tabular" MyDB -O
te Model.bim -S fix.csx -D "localhost\tabular" MyDB -O
```

> [!NOTE]
> TE2 模式会运行与 `TabularEditor.exe` 相同的 `Load → Scripts → Schema Check → Save → BPA → Deploy → TRX` 流程，包括与上下文相关的标志行为（例如，`-D` 之后的 `-S` 表示 `-SHARED`，而不是 `-SCRIPT`）。

## Migrate 命令

可将 `te util migrate` 作为实时参考，用于了解 TE2 选项如何映射到新的 CLI。 它会输出一张彩色表格，列出每个已知 TE2 标志、其状态（受支持、已重命名、计划支持）以及对应的 `te` 命令。

```bash
te util migrate                   # Full flag mapping table
te util migrate -A                # Look up a single flag
te util migrate --output-format json     # Machine-readable mapping
```

请查看 `te util migrate` 命令的输出，其中包含与你已安装的 CLI 版本相对应的当前映射关系。

## 标志映射（整理的子集）

下面是最常用选项的非完整汇总。 要看完整列表，运行 `te util migrate`。

| TE2 标志                                    | 新 CLI 等效参数                                                                                  | 说明                                                                                                                          |
| ----------------------------------------- | ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `file`（位置参数）                              | `--model <path>`（全局选项）                                                                      | 始终使用全局 `--model` 选项；没有任何命令会将模型作为位置参数接收。 或者通过 `te connect <path>` 一次设置并激活某个模型。                                               |
| `server`、`database`                       | `te connect <server> <database>` 或全局 `-s <server> -d <database>`                            | `-s`/`-d` 始终用于标识模型源；部署目标使用 `--target-server` / `--target-database`。                                                         |
| `-L` / `-LOCAL`                           | `te connect --local`                                                                        | 仅限 Windows。                                                                                                                 |
| `-S` / `-SCRIPT`                          | `te script --file <file.csx>` 或 `--inline "code"`                                           | 也可以直接使用 `.csx` 路径（`te script fix.csx`）。 支持多个脚本（`--file a.csx --file b.csx`）、内联代码以及标准输入（stdin，`--inline -`）；文件和内联代码会按给定顺序运行。 |
| `-A` / `-ANALYZE`                         | `te bpa run --rules <file-or-url>`                                                          | 支持 `--fail-on`、`--fix` 和多个规则文件。                                                                                             |
| `-AX` / `-ANALYZEX`                       | `te bpa run --rules <file> --no-model-rules`                                                | 默认包含嵌入在模型中的规则；`--no-model-rules` 会将其排除，这与 `-AX` 的行为一致。                                                                      |
| `-B` / `-BIM`                             | `te save-as --model <model> -o <file.bim> --serialization bim`                              |                                                                                                                             |
| `-F` / `-FOLDER`                          | `te save-as --model <model> -o <dir> --serialization Database.json`                         | 在 `-D` 之后，TE2 的 `-F` 表示 `-FULL`；参见 `--deploy-full`。                                                                         |
| `-TMDL`                                   | `te save-as --model <model> -o <dir> --serialization tmdl`                                  | `--serialization` 可以省略——格式会根据输出路径推断。                                                                                        |
| `-D` / `-DEPLOY`                          | `te deploy --model <model> --target-server <server> --target-database <database> --execute` | 这是一个独立的命令，使用具名选项。 如果不带 `--execute`，`te deploy` 会进行试运行，并打印它将发送的 TMSL。                                                        |
| `-O` / `-OVERWRITE`                       | （默认）或使用 `--create-only` 选择不覆盖                                                               | 在新的 CLI 中，覆盖是默认行为。                                                                                                          |
| `-C` / `-CONNECTIONS`                     | `te deploy --deploy-connections`                                                            |                                                                                                                             |
| `-P` / `-PARTITIONS` 分区                   | `te deploy --deploy-partitions` 部署分区                                                        |                                                                                                                             |
| `-Y` / `-SKIPPOLICY`                      | `te deploy --deploy-partitions --skip-refresh-policy` 部署分区并跳过刷新策略                           | 需要 `--deploy-partitions`。                                                                                                   |
| `-SHARED`                                 | `te deploy --deploy-shared-expressions`                                                     | 在 `-D` 之后，TE2 的 `-S` 表示 `-SHARED`。                                                                                          |
| `-R` / `-ROLES` 角色                        | `te deploy --deploy-roles`                                                                  |                                                                                                                             |
| `-M` / `-MEMBERS`                         | `te deploy --deploy-role-members`                                                           |                                                                                                                             |
| `-FULL`（在 `-D` 之后）                        | `te deploy --deploy-full`                                                                   | 等同于：覆盖 + 连接 + 分区 + 共享 + 角色 + 角色成员。                                                                                          |
| `-X` / `-XMLA <file>`                     | `te deploy ... > <file>`（省略 `--execute`）                                                    | 默认会输出脚本：如果不带 `--execute`，`te deploy` 会以只读方式连接，并将 TMSL 打印到 stdout——把它重定向到文件即可。                                               |
| `-V` / `-VSTS`                            | 在 `validate`、`bpa run`、`deploy` 和 `test run` 命令中使用 `--ci vsts`                              | 会向 stderr 输出 `##vso[...]` 注释。 `azdo` 和 `azure-devops` 都是可接受的别名。                                                             |
| `-G` / `-GITHUB`                          | `--ci github`（别名 `gh`）                                                                      | 会输出 `::error::` / `::warning::` / `::notice::` 注释。                                                                          |
| `-T` / `-TRX <file>`                      | 在 `validate`、`bpa run` 和 `test run` 命令中使用 `--trx <file>`                                    | 用于 Azure DevOps 测试发布的 VSTEST `.trx` 文件。                                                                                     |
| `-W` / `-WARN`                            | （默认）                                                                                        | 部署结果中始终会 Report 警告。                                                                                                         |
| `-E` / `-ERR`                             | （默认）                                                                                        | 出现 DAX 错误时，部署会返回非零退出代码。                                                                                                     |
| `-SC` / `-SCHEMACHECK`                    | _尚未实现。_                                                                                     | TE2 架构检查会连接到真实的数据源。 这不同于 `te validate`（DAX 语义验证，不连接数据源）。                                                                    |
| `-L` / `-LOGIN <user> <pass>`（位于 `-D` 之后） | `te auth login -u <id> -p <secret> -t <tenant>`                                             | 使用服务主体或基于环境变量的凭据。 登录状态会被缓存，因此后续命令会静默获取令牌——见 @te-cli-auth。                                                      |

## 迁移指南

从基于 TE2 的管道迁移到新 CLI 的推荐路径：

1. **直接替换。** 在现有管道中用 `te`（或 `te2`）替换 `TabularEditor.exe`。 确认管道仍可正常运行——TE2 兼容层会让大多数调用方式保持不变。
2. **逐步替换标志。** 每次转换一组标志：
   - 先从 `-A` / `-AX` → `te bpa run` 开始，以获得更丰富的 BPA 输出（`--fail-on`、`--fix`、`--trx`）。
   - 然后把 `-D` 替换为 `te deploy`，以获得更细粒度的部署控制。
   - 最后：`-V` / `-G` → `--ci vsts` / `--ci github`。
3. **切换到非交互式 CI 标志。** 为每个 `te` 命令都加上 `--non-interactive`（并在 `validate`、`bpa run`、`deploy` 和 `test run` 中加上 `--ci <vsts|github>`）；对必须执行实际操作的 `deploy`/`refresh` 步骤，传入 `--execute --force`；并移除所有 `start /wait` 包装——新的 CLI 是普通的控制台可执行文件，不需要这些。
4. **采用服务主体身份验证。** 将 `-D -L <user> <pass>` 替换为 `te auth login -u …… -p …… -t ...`，或在管道中使用基于环境变量凭据的步骤。 见 @te-cli-auth。

## 重要差异

- **部署时的 BPA 检查。** `te deploy` 现在默认会在部署前运行 BPA，作为前置检查。 使用 `--skip-bpa` 可保留旧行为，或使用 `--fix-bpa` 在部署前自动修复违规项。 见 @te-cli-config。
- **默认进行试运行。** `te deploy` 和 `te refresh` 会打印它们将发送的确切 TMSL，但不会做任何更改；传入 `--execute` 才会实际执行。 `--execute` 会在终端中请求确认（安全默认值为 `n`）；CI 管道必须传入 `--execute --force`。
- **结构化输出。** 每个命令都支持 `--output-format json`，以生成机器可读输出——参见 @te-cli-automation。
- **无需 `start /wait`。** 新 CLI 是普通的控制台可执行文件；你可以在 shell 脚本、PowerShell 和 CI 任务中直接调用它。
- **跨平台。** CLI 可在 Windows、macOS 和 Linux 上运行。 本地 SSAS 和 Power BI Desktop 连接仍仅支持 Windows。

## 相关页面

- @command-line-options —— 旧版 TE2 命令行参考。
- @te-cli-commands —— 新 CLI 的完整命令参考。
- @te-cli-cicd —— 适用于 GitHub Actions 和 Azure DevOps 的管道示例。
