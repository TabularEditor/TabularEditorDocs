---
uid: cicd-azure-devops-pipeline
title: Azure DevOps pipeline reference
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

# Azure DevOps pipeline reference

> [!NOTE]
> This article is under development and will be published alongside the Tabular Editor CLI general availability release.

A complete, annotated Azure DevOps pipeline for semantic models: from trigger to production deployment, built on the Tabular Editor CLI.

The canonical, maintained pipeline definitions live in the public [TabularEditor/CLI](https://github.com/TabularEditor/CLI) repository — this article walks through them step by step.

## What this article will cover

- Pipeline overview: trigger → checkout → acquire the CLI → validate (BPA + schema) → test → deploy → refresh
- Walkthrough of each stage with the full YAML
- Service connections, variable groups, and secret handling
- Pull request validation vs. deployment pipelines
- Adapting the reference pipeline to your environments and [branching strategy](xref:cicd-branching-strategies)
