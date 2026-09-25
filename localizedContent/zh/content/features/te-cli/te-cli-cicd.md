---
uid: te-cli-cicd
title: CI/CD 集成
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

# CI/CD 集成

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

The Tabular Editor CLI is designed for unattended execution in continuous integration and delivery pipelines. A single binary, structured output, non-interactive mode, native CI annotations for GitHub Actions and Azure DevOps, and VSTEST-compatible test results make it a natural replacement for ad-hoc TE2 invocations.

> [!WARNING]
> **在有限公开预览期间，不要在生产管道中使用 CLI。** 管道所有者需要注意以下两项预览版特有风险：
>
> - **Hard expiry.** The preview binary stops functioning on **2026-10-31** - any pipeline depending on it will fail on that date, regardless of your release calendar.
> - **不保证向后兼容。** 命令、选项、输出结构和退出代码可能会在不同预览版本之间变更，因此当你更新随仓库一并提交的二进制文件时，可能需要同步调整管道步骤。
>
> 在非生产管道中构建和评估，并在公开的 [TabularEditor/CLI](https://github.com/TabularEditor/CLI) repository 中分享反馈，以便 GA 版本更符合你的需求。

## CLI 为何适合 CI

- **单个自包含二进制文件。** 无需安装运行时，不需要 `TabularEditor.exe`，也不需要 `start /wait`。
- **`--non-interactive` 全局标志。** 禁用所有提示；出现错误时会快速失败，并给出可操作的错误信息。
- **Dry run by default.** `te deploy` and `te refresh` print the exact TMSL they would send; add `--execute` to act. Both ask for confirmation at a terminal, so `--execute --force` is required in CI, where a prompt cannot be answered.
- **Failure is failure.** `te deploy` exits non-zero when the server accepts the metadata but parks objects with errors, and `te script` exits non-zero when a script reports an error - a gate on the exit code cannot pass a broken run.
- **`--ci vsts` / `--ci github`.** Emit native pipeline annotations to stderr, carrying the finding's code (`code=` on Azure DevOps, `title=` on GitHub). `azdo` / `azure-devops` and `gh` are accepted aliases, `none` means no annotations, and a mistyped value is rejected before the command runs instead of silently emitting nothing.
- **`--trx <file>`。** 生成可供 Azure DevOps 测试发布使用的 VSTEST 结果。
- **Structured errors.** `--error-format json` emits `{"error": "...", "hint": "..."}` to stderr so pipeline steps can fail with a useful message.
- **One findings JSON.** `te validate`, `te bpa run`, `te test run`, and `te query` share a single machine-readable JSON document under `--output-format json` - a `summary`, a flat `findings[]` array with `severity`/`source`/`code`/`message`, and, where resolvable, an `objectPath` you can feed back to `te get`. See @te-cli-findings.

## 将 CLI 添加到你的仓库

在有限公开预览期间，CLI 需要登录 [tabulareditor.com](https://tabulareditor.com/download-tabular-editor-cli) 才能下载，因此管道无法通过公开 URL 获取该压缩包。 The simplest reproducible approach is to commit the binary that matches your runner into your repository and reference it from each pipeline step.

常见布局：

```
your-repo/
└── tools/
    └── te/
        ├── te         # Linux / macOS binary (needs chmod +x at runtime)
        └── te.exe     # Windows binary
```

Place the **extracted** binary - not the archive - so the pipeline can call it directly. Pick the build that matches your runner OS/arch; see @te-cli-install for the filename table. The self-contained binary is ~70 MB; consider Git LFS if your repo is sensitive to size.

> [!NOTE]
> Committing the binary also pins the CLI version to whatever you checked in, which is desirable for CI reproducibility. To upgrade, replace the binary in `tools/te/` and commit it - the commit message is your version log. Keep in mind that the preview binary still expires on **2026-10-31** regardless of when you committed it, so a vendored copy is not a permanent dependency - plan to refresh it (and re-validate your pipeline against the new API surface) on preview-build cadence.

## GitHub Actions

A complete deploy + test workflow. 示例假定 Linux 版 `te` 二进制文件已提交到 `tools/te/te`，并且服务主体存放在 repository secrets 中（`AZURE_CLIENT_ID`、`AZURE_CLIENT_SECRET`、`AZURE_TENANT_ID`）。

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
        run: te validate --model ./model --ci github --trx validate.trx

      - name: Best Practice Analyzer (gate)
        run: te bpa run --model ./model --fail-on error --ci github --trx bpa.trx

      - name: Deploy
        run: |
          te deploy --model ./model \
            --target-server "${{ vars.WORKSPACE }}" \
            --target-database "${{ vars.MODEL }}" \
            --auth env \
            --non-interactive \
            --execute \
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

上述 GitHub Actions 工作流在 Azure DevOps Pipelines 中的等效版本。 The example assumes `te.exe` is committed at `tools\te\te.exe`. `--ci vsts` emits `##vso[...]` commands that the pipeline interprets as errors, warnings, and task-status updates.

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

  - script: te validate --model ./model --ci vsts --trx validate.trx
    displayName: 'Validate'

  - script: te bpa run --model ./model --fail-on error --ci vsts --trx bpa.trx
    displayName: 'BPA gate'

  - script: |
      te deploy --model ./model ^
        --target-server "$(WORKSPACE)" --target-database "$(MODEL)" ^
        --auth env --non-interactive --execute --force --ci vsts
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

`te deploy` and `te save-as` run the Best Practice Analyzer as a pre-flight gate by default. Three behaviors are worth determining up-front:

- **Enforce** - the default. Pipeline fails if BPA finds violations at severity >= error. Pair with `--fail-on warning` on a standalone `te bpa run` step if you want warnings to fail too.
- **自动修复**——`--fix-bpa` 会在内存中对部署产物应用 `fixExpression`。 Source files are not modified. Useful when the source of truth lives in the model and you want deploys to normalize style without developer intervention.
- **绕过**——`--skip-bpa` 会为单个命令禁用该门禁。 Useful for emergency hotfixes; not recommended as a default.

```bash
# Treat warnings as failures in PR validation
te bpa run --model ./model --fail-on warning --ci github --trx bpa.trx

# Auto-fix during deploy (source unchanged)
te deploy --model ./model --target-server my-ws --target-database my-model --fix-bpa --execute --force --ci github

# Emergency bypass
te deploy --model ./model --target-server my-ws --target-database my-model --skip-bpa --execute --force --ci github
```

要通过 `bpa.onDeploy` / `bpa.onSave` 配置键全局控制 BPA 门禁，参见 @te-cli-config。

## Script validation

C# scripts can be compile-checked without loading any model - an offline lint step for PR validation:

```bash
# Compile-check C# scripts without a model (offline lint)
te script --file ./scripts/fix.csx --validate
```

## 刷新模式

Refresh in pipelines is typically a follow-up step after deployment. Add `--execute --force` (without `--execute` the command only prints the TMSL it would run; without `--force` it stops to ask for a confirmation nobody can give), use `--non-interactive`, and pick a deterministic `--type`:

```bash
# Full refresh of the whole model after deploy
te refresh -s my-ws -d my-model --type full --execute --force --non-interactive

# Refresh a single fact table (e.g., daily incremental pipeline)
te refresh -s my-ws -d my-model --table Sales --type full --execute --force --non-interactive

# Recalculate only (useful after calculation-group changes)
te refresh -s my-ws -d my-model --type calculate --execute --force --non-interactive
```

For incremental refresh workflows, use `--apply-refresh-policy` (pass `true`, `false`, or a table name to scope the refresh to that table) together with `--effective-date <yyyy-MM-dd>` and `--execute --force`. See @te-cli-commands for details.

## 工件模式

无需部署，直接将 TMSL 或 XMLA 输出为工件，这样 DBA 或后续作业就可以查看或应用它：

```bash
# Produce the TMSL script that a deploy would send - do not deploy (dry run is the default)
te deploy --model ./model --target-server my-ws --target-database my-model > deploy.tmsl

# Produce the TMSL refresh command - do not execute (dry run is the default)
te refresh -s my-ws -d my-model --type full > refresh.tmsl
```

Commit these artifacts to git, upload them to the pipeline's artifact storage, or pass them between jobs. They're plain text and diff cleanly in pull requests.

## 机密管理

| 方式                                                                                         | When to use                                    | 说明                                                                                                                                                 |
| ------------------------------------------------------------------------------------------ | ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| 通过环境变量使用服务主体（`AZURE_CLIENT_ID` / `AZURE_CLIENT_SECRET` / `AZURE_TENANT_ID`，`--auth env`）   | 通用 CI/CD                                       | 在步骤级或作业级将流水线机密映射为环境变量。 Never pass secrets in command arguments.                                                                    |
| 服务主体：每个作业只需通过 `te auth login` 登录一次（`echo $SECRET \| te auth login -u $ID -p - -t $TENANT`） | Multi-step jobs                                | 登录会被缓存，因此后续的 `te` 命令会静默获取令牌，无需为每个步骤设置 `AZURE_CLIENT_*`，也不必再次传递 `-u/-p/-t`。 Pipe the secret via stdin rather than interpolating it. |
| 托管标识 (`--auth managed-identity`)                                        | Azure 虚拟机、Azure Container Apps、Azure Functions | No secrets to manage. Preferred in Azure-hosted environments.                                                      |
| 证书 (`--certificate <path>`)                                             | 需要证书轮换的企业场景                                    | 将证书作为安全文件挂载；通过环境变量传递 `--certificate-password`。                                                                                                     |

> [!WARNING]
> Do not echo secrets or the output of `te auth status` to pipeline logs. The CLI writes warnings to stderr when secrets are passed on the command line - respect those warnings in CI.

## 相关页面

- @te-cli-auth：身份验证方法详解。
- @te-cli-config - 配置和配置文件覆盖。
- @te-cli-automation：通用脚本模式。
- @te-cli-migrate：迁移现有的基于 TE2 的管道。
