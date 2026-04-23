---
uid: te-cli-cicd
title: CI/CD Integration
author: Peer Grønnerup
updated: 2026-04-20
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      none: true
    - product: Tabular Editor CLI
      full: true
---
# CI/CD Integration

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

The Tabular Editor CLI is designed for unattended execution in continuous integration and delivery pipelines. A single binary, structured output, non-interactive mode, native CI annotations for GitHub Actions and Azure DevOps, and VSTEST-compatible test results make it a natural replacement for ad-hoc TE2 invocations.

> [!WARNING]
> During preview, we recommend against using the CLI in **production** pipelines. Commands, flags, and outputs may change before GA. Build and evaluate in non-production pipelines first; share feedback so the GA shape matches your needs.

## What makes the CLI CI-friendly

- **Single self-contained binary.** No runtime install, no `TabularEditor.exe`, no `start /wait`.
- **`--non-interactive` global flag.** Disables every prompt; fails fast with actionable errors.
- **`--force`** on mutating commands (`te deploy`, `te refresh`) skips confirmation prompts.
- **`--ci vsts` / `--ci github`.** Emit native pipeline annotations to stderr.
- **`--trx <file>`.** Produce VSTEST results consumable by Azure DevOps test publishing.
- **Structured errors.** `--output json` emits `{"error": "...", "hint": "..."}` to stderr so pipeline steps can fail with a useful message.

## GitHub Actions

A complete deploy + test workflow. The example assumes a service principal stored in repository secrets (`AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID`).

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

      - name: Download Tabular Editor CLI
        run: |
          # TBD: replace with the official download URL once confirmed.
          curl -L -o te.zip "<download-url-linux-x64>"
          unzip te.zip -d $HOME/.local/bin
          chmod +x $HOME/.local/bin/te
          echo "$HOME/.local/bin" >> $GITHUB_PATH

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

Equivalent YAML for Azure DevOps. `--ci vsts` emits `##vso[...]` commands that the pipeline interprets as errors, warnings, and task-status updates.

```yaml
trigger:
  - main

pool:
  vmImage: 'windows-latest'

variables:
  - group: 'te-cli-secrets'   # Contains AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID

steps:
  - checkout: self

  - task: PowerShell@2
    displayName: 'Install Tabular Editor CLI'
    inputs:
      targetType: 'inline'
      script: |
        # TBD: replace with the official download URL once confirmed.
        Invoke-WebRequest -Uri "<download-url-win-x64>" -OutFile te.zip
        Expand-Archive te.zip -DestinationPath $(Agent.ToolsDirectory)\te
        Write-Host "##vso[task.prependpath]$(Agent.ToolsDirectory)\te"

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

## BPA gate patterns

`te deploy` and `te save` run the Best Practice Analyzer as a pre-flight gate by default. Three behaviors are worth picking up front:

- **Enforce** — the default. Pipeline fails if BPA finds violations at severity ≥ error. Pair with `--fail-on warning` on a standalone `te bpa run` step if you want warnings to fail too.
- **Auto-fix** — `--fix-bpa` applies `fixExpression`s in memory for the deployed artifact. Source files are not modified. Useful when the source of truth lives in the model and you want deploys to normalize style without developer intervention.
- **Bypass** — `--skip-bpa` disables the gate for a single command. Useful for emergency hotfixes; not recommended as a default.

```bash
# Treat warnings as failures in PR validation
te bpa run ./model --fail-on warning --ci github --trx bpa.trx

# Auto-fix during deploy (source unchanged)
te deploy ./model -s my-ws -d my-model --fix-bpa --force --ci github

# Emergency bypass
te deploy ./model -s my-ws -d my-model --skip-bpa --force --ci github
```

See @te-cli-config for controlling the BPA gate globally via `bpaOnDeploy` / `bpaOnSave` config keys.

## Refresh patterns

Refresh in pipelines is typically a follow-up step after deploy. Use `--non-interactive` and pick a deterministic `--type`:

```bash
# Full refresh of the whole model after deploy
te refresh -s my-ws -d my-model --type full --non-interactive --ci github

# Refresh a single fact table (e.g., daily incremental pipeline)
te refresh -s my-ws -d my-model --table Sales --type full --non-interactive

# Recalculate only (useful after calculation-group changes)
te refresh -s my-ws -d my-model --type calculate --non-interactive
```

For incremental refresh workflows, combine `--apply-refresh-policy`, `--effective-date <yyyy-MM-dd>`, and `--partition <Table.Partition>` flags. See @te-cli-commands for details.

## Artifact patterns

Emit TMSL or XMLA as an artifact without deploying, so DBAs or a later job can review or apply it:

```bash
# Produce the XMLA/TMSL script that would deploy — do not deploy
te deploy ./model -s my-ws -d my-model --xmla deploy.tmsl --force

# Produce the TMSL refresh command — do not execute
te refresh -s my-ws -d my-model --type full --dry-run > refresh.tmsl
```

Commit these artifacts to git, upload them to the pipeline's artifact storage, or pass them between jobs. They're plain text and diff cleanly in pull requests.

## Secret handling

| Approach | When to use | Notes |
| -- | -- | -- |
| Service principal via env vars (`AZURE_CLIENT_ID` / `AZURE_CLIENT_SECRET` / `AZURE_TENANT_ID`, `--auth env`) | General CI/CD | Map pipeline secrets to environment variables at the step or job level. Never pass secrets in command arguments. |
| Service principal via flags (`te auth login -u ... -p -`, reading secret from stdin) | One-off automation | Pipe the secret rather than interpolating it: `echo $SECRET | te auth login -u $ID -p - -t $TENANT`. |
| Managed identity (`--auth managed-identity`) | Azure VMs, Container Apps, Azure Functions | No secrets to manage. Preferred in Azure-hosted environments. |
| Certificate (`--certificate <path>`) | Enterprise scenarios with cert rotation | Mount the certificate as a secure file step; pass `--certificate-password` via env. |

> [!WARNING]
> Do not echo secrets or the output of `te auth status` to pipeline logs. The CLI writes warnings to stderr when secrets are passed on the command line — respect those warnings in CI.

## Related pages

- @te-cli-auth — authentication methods in detail.
- @te-cli-config — configuration and profile overrides.
- @te-cli-automation — general scripting patterns.
- @te-cli-migrate — migrating an existing TE2-based pipeline.
