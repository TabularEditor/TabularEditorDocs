---
uid: te-cli-cicd
title: CI/CD 集成
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

# CI/CD 集成

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

Tabular Editor CLI 专为在持续集成和持续交付管道中进行无人值守执行而设计。 单一可执行文件、结构化输出、非交互模式、面向 GitHub Actions 和 Azure DevOps 的原生 CI 注解，以及与 VSTEST 兼容的测试结果，使其成为替代临时调用 TE2 的理想选择。

> [!WARNING]
> **在有限公开预览期间，不要在生产管道中使用 CLI。** 管道所有者需要注意以下两项预览版特有风险：
>
> - **硬性到期。** 预览版二进制文件会在 **2026-09-30** 停止运行——任何依赖它的管道都会在当天失败，无论你的发布日程如何安排。
> - **不保证向后兼容。** 命令、选项、输出结构和退出代码可能会在不同预览版本之间变更，因此当你更新随仓库一并提交的二进制文件时，可能需要同步调整管道步骤。
>
> 在非生产管道中构建和评估，并在公开的 [TabularEditor/CLI](https://github.com/TabularEditor/CLI) repository 中分享反馈，以便 GA 版本更符合你的需求。

## CLI 为何适合 CI

- **单个自包含二进制文件。** 无需安装运行时，不需要 `TabularEditor.exe`，也不需要 `start /wait`。
- **`--non-interactive` 全局标志。** 禁用所有提示；出现错误时会快速失败，并给出可操作的错误信息。
- 在会更改状态的命令（`te deploy`、`te refresh`）上使用 **`--force`** 可跳过确认提示。
- **`--ci vsts` / `--ci github`。** 将原生管道注解输出到 stderr。
- **`--trx <file>`。** 生成可供 Azure DevOps 测试发布使用的 VSTEST 结果。
- **结构化错误。** `--output-format json` 会向 stderr 输出 `{"error": "...", "hint": "..."}`，以便管道步骤在失败时显示有用的信息。

## 将 CLI 添加到你的仓库

在有限公开预览期间，CLI 需要登录 [tabulareditor.com](https://tabulareditor.com/download-tabular-editor-cli) 才能下载，因此管道无法通过公开 URL 获取该压缩包。 最简单且可复现的方法是，将与你的运行器匹配的二进制文件提交到你的 repository，并在每个管道步骤中引用它。 最简单且可复现的方法是，将与你的运行器匹配的二进制文件提交到你的 repository，并在每个管道步骤中引用它。

常见布局：

```
your-repo/
└── tools/
    └── te/
        ├── te         # Linux / macOS binary (needs chmod +x at runtime)
        └── te.exe     # Windows binary
```

请把**解压后的**二进制文件放到位——不是压缩包——这样管道就能直接调用。 选择与 runner 的 OS/架构匹配的构建；文件名对照表见 @te-cli-install。 自包含的二进制文件约为 70 MB；如果你的仓库对体积比较敏感，可以考虑使用 Git LFS。

> [!NOTE]
> 提交这个二进制文件也会把 CLI 版本固定为你提交的那个版本，这有利于 CI 的可重现性。 要升级时，替换 `tools/te/` 中的二进制文件并提交——提交信息就是你的版本日志。 请注意：预览版二进制文件无论你何时提交，都会在 **2026-09-30** 到期。因此，随仓库提交的副本并非永久依赖——请按预览版构建的发布节奏更新它（并在新的 API 接口面上重新验证你的管道）。

## GitHub Actions

完整的部署 + 测试工作流。 完整的部署 + 测试工作流。 示例假定 Linux 版 `te` 二进制文件已提交到 `tools/te/te`，并且服务主体存放在 repository secrets 中（`AZURE_CLIENT_ID`、`AZURE_CLIENT_SECRET`、`AZURE_TENANT_ID`）。

```yaml
name: Deploy semantic model

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    env:
      AZURE_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
      AZURE_CLIENT_SECRET: ${{ secrets.AZURE_CLIENT_SECRET }}
      AZURE_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
    steps:
      - uses: actions/checkout@v4

      - name: Set up Tabular Editor CLI
        run: |
          chmod +x ./tools/te/te
          echo "$GITHUB_WORKSPACE/tools/te" >> $GITHUB_PATH

      - name: Validate
        run: te validate ./model --ci github --trx validate.trx

      - name: Best Practice Analyzer (gate)
        run: te bpa run ./model --fail-on error --ci github --trx bpa.trx

      - name: Deploy
        run: |
          te deploy ./model \
            -s "${{ vars.WORKSPACE }}" \
            -d "${{ vars.MODEL }}" \
            --auth env \
            --non-interactive \
            --force \
            --ci github

      - name: Regression tests
        run: |
          te test run \
            -s "${{ vars.WORKSPACE }}" \
            -d "${{ vars.MODEL }}" \
            --auth env --non-interactive \
            --ci github --trx tests.trx

      - name: Publish test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: trx-results
          path: '*.trx'
```

## Azure DevOps Pipelines

上述 GitHub Actions 工作流在 Azure DevOps Pipelines 中的等效版本。 示例假定 `te.exe` 已提交到 `tools\\te\\te.exe`。 `--ci vsts` 会输出 `##vso[...]` 命令，管道会将其解释为错误、警告和任务状态更新。 示例假定 `te.exe` 已提交到 `tools\\te\\te.exe`。 `--ci vsts` 会输出 `##vso[...]` 命令，管道会将其解释为错误、警告和任务状态更新。

```yaml
trigger:
  - main

pool:
  vmImage: 'windows-latest'

variables:
  - group: 'te-cli-secrets'   # Contains AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID

steps:
  - checkout: self

  - powershell: Write-Host "##vso[task.prependpath]$(Build.SourcesDirectory)\tools\te"
    displayName: 'Set up Tabular Editor CLI'

  - script: te validate ./model --ci vsts --trx validate.trx
    displayName: 'Validate'

  - script: te bpa run ./model --fail-on error --ci vsts --trx bpa.trx
    displayName: 'BPA gate'

  - script: |
      te deploy ./model ^
        -s "$(WORKSPACE)" -d "$(MODEL)" ^
        --auth env --non-interactive --force --ci vsts
    displayName: 'Deploy'
    env:
      AZURE_CLIENT_ID: $(AZURE_CLIENT_ID)
      AZURE_CLIENT_SECRET: $(AZURE_CLIENT_SECRET)
      AZURE_TENANT_ID: $(AZURE_TENANT_ID)

  - script: te test run -s "$(WORKSPACE)" -d "$(MODEL)" --auth env --non-interactive --ci vsts --trx tests.trx
    displayName: 'Regression tests'
    env:
      AZURE_CLIENT_ID: $(AZURE_CLIENT_ID)
      AZURE_CLIENT_SECRET: $(AZURE_CLIENT_SECRET)
      AZURE_TENANT_ID: $(AZURE_TENANT_ID)

  - task: PublishTestResults@2
    condition: always()
    inputs:
      testResultsFormat: 'VSTest'
      testResultsFiles: '*.trx'
```

## BPA 门禁模式

默认情况下，`te deploy` 和 `te save` 会先运行 Best Practice Analyzer 作为预检门禁。 有三种行为值得提前确定： 有三种行为值得提前确定：

- **强制执行**——默认行为。 **强制执行**——默认行为。 如果 BPA 发现严重级别 ≥ error 的违规项，管道将失败。 如果你也希望警告导致失败，可在独立的 `te bpa run` 步骤中配合 `--fail-on warning` 使用。 如果你也希望警告导致失败，可在独立的 `te bpa run` 步骤中配合 `--fail-on warning` 使用。
- **自动修复**——`--fix-bpa` 会在内存中对部署产物应用 `fixExpression`。 不会修改源文件。 当模型是唯一可信来源，而你希望部署在无需开发者干预的情况下规范化样式时，这很有用。 不会修改源文件。 当模型是唯一可信来源，而你希望部署在无需开发者干预的情况下规范化样式时，这很有用。
- **绕过**——`--skip-bpa` 会为单个命令禁用该门禁。 适合紧急热修复；不建议作为默认做法。 适合紧急热修复；不建议作为默认做法。

```bash
# Treat warnings as failures in PR validation
te bpa run ./model --fail-on warning --ci github --trx bpa.trx

# Auto-fix during deploy (source unchanged)
te deploy ./model -s my-ws -d my-model --fix-bpa --force --ci github

# Emergency bypass
te deploy ./model -s my-ws -d my-model --skip-bpa --force --ci github
```

要通过 `bpa.onDeploy` / `bpa.onSave` 配置键全局控制 BPA 门禁，参见 @te-cli-config。

## 刷新模式

在流水线中，刷新通常是部署之后的后续步骤。 使用 `--non-interactive`，并选择一个确定性的 `--type`：

```bash
# Full refresh of the whole model after deploy
te refresh -s my-ws -d my-model --type full --non-interactive

# Refresh a single fact table (e.g., daily incremental pipeline)
te refresh -s my-ws -d my-model --table Sales --type full --non-interactive

# Recalculate only (useful after calculation-group changes)
te refresh -s my-ws -d my-model --type calculate --non-interactive
```

对于增量刷新工作流，请组合使用 `--apply-refresh-policy`、`--effective-date <yyyy-MM-dd>` 和用于分区的 `--partition <Table.Partition>` 标志。 更多信息见 @te-cli-commands。 更多信息见 @te-cli-commands。

## 工件模式

无需部署，直接将 TMSL 或 XMLA 输出为工件，这样 DBA 或后续作业就可以查看或应用它：

```bash
# Produce the XMLA/TMSL script that would deploy - do not deploy
te deploy ./model -s my-ws -d my-model --xmla deploy.tmsl --force

# Produce the TMSL refresh command - do not execute
te refresh -s my-ws -d my-model --type full --dry-run > refresh.tmsl
```

你可以将这些工件提交到 Git、上传到流水线的工件存储，或在作业之间传递。 它们都是纯文本，在拉取请求中也能清晰地显示差异。

## 机密管理

| 方式                                                                                         | 适用场景                                           | 说明                                                                                                                                     |
| ------------------------------------------------------------------------------------------ | ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| 通过环境变量使用服务主体（`AZURE_CLIENT_ID` / `AZURE_CLIENT_SECRET` / `AZURE_TENANT_ID`，`--auth env`）   | 通用 CI/CD                                       | 在步骤级或作业级将流水线机密映射为环境变量。 不要在命令参数中传递机密信息。 不要在命令参数中传递机密信息。                                                                                 |
| 服务主体：每个作业只需通过 `te auth login` 登录一次（`echo $SECRET \| te auth login -u $ID -p - -t $TENANT`） | 多步骤作业                                          | 登录会被缓存，因此后续的 `te` 命令会静默获取令牌，无需为每个步骤设置 `AZURE_CLIENT_*`，也不必再次传递 `-u/-p/-t`。 通过 stdin 将机密信息传入，而不要把它插值到命令中。 通过 stdin 将机密信息传入，而不要把它插值到命令中。 |
| 托管标识 (`--auth managed-identity`)                                        | Azure 虚拟机、Azure Container Apps、Azure Functions | 无需管理机密信息。 在 Azure 托管环境中优先使用。                                                                                                           |
| 证书 (`--certificate <path>`)                                             | 需要证书轮换的企业场景                                    | 将证书作为安全文件挂载；通过环境变量传递 `--certificate-password`。                                                                                         |

> [!WARNING]
> 不要将机密信息或 `te auth status` 的输出回显到流水线日志中。 当在命令行中传递机密信息时，CLI 会将警告写入 stderr；在 CI 中务必重视这些警告。

## 相关页面

- @te-cli-auth：身份验证方法详解。
- @te-cli-config - 配置和配置文件覆盖。
- @te-cli-automation：通用脚本模式。
- @te-cli-migrate：迁移现有的基于 TE2 的管道。
