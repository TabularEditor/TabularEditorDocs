---
uid: cicd-github-actions-workflow
title: GitHub Actions workflow reference
author: Peer Grønnerup
updated: 2026-08-12
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      none: true
    - product: Tabular Editor CLI
      full: true
---

# GitHub Actions workflow reference

> [!NOTE]
> This article is under development and will be published alongside the Tabular Editor CLI general availability release.

A complete, annotated GitHub Actions workflow for semantic models: from trigger to production deployment, built on the Tabular Editor CLI. It implements the same conceptual pipeline as the [Azure DevOps reference](xref:cicd-azure-devops-pipeline), so the two can be compared side by side.

The canonical, maintained workflow definitions live in the public [TabularEditor/CLI](https://github.com/TabularEditor/CLI) repository — this article walks through them step by step.

## What this article will cover

- Workflow overview: trigger → checkout → acquire the CLI → validate (BPA + schema) → test → deploy → refresh
- Walkthrough of each job with the full workflow YAML
- Environments, secrets, and OIDC/service principal authentication
- Pull request validation vs. deployment workflows
- Adapting the reference workflow to your environments and [branching strategy](xref:cicd-branching-strategies)
