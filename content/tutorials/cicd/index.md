---
uid: cicd-overview
title: CI/CD for Semantic Models
author: Peer Grønnerup
updated: 2026-08-12
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
    - product: Tabular Editor CLI
      full: true
---

# CI/CD for Semantic Models

> [!NOTE]
> This section is under development and will be published alongside the Tabular Editor CLI general availability release.

This section tells the end-to-end story of professional semantic model development with Tabular Editor: multiple developers working in parallel on the same model, every change validated and tested automatically, and deployments to test and production that are repeatable, auditable, and boring — in the best possible way.

The articles are ordered as a narrative, but each one stands on its own if you already have parts of the puzzle in place.

## What this section covers

**Foundations** — the decisions you make once, before the first feature branch:

- @cicd-fabric-workspaces — how to organize development, test, and production workspaces in Microsoft Fabric
- @cicd-repository-setup — what goes in your Git repository and how to structure it
- @cicd-branching-strategies — choosing a branching strategy that matches your team and environments
- @github-flow — a deep dive into the recommended strategy and the Octopus Merge pattern

**Ways of working** — the daily developer workflow:

- @cicd-parallel-development — multiple developers on one model with Git and Save to Folder
- @cicd-workspace-mode — isolated development against personal workspace databases

**Validation and testing** — the quality gates in your pipeline:

- @cicd-validation — Best Practice Analyzer and schema validation as pipeline gates
- @cicd-testing — automated DAX and data tests for semantic models

**Deployment** — getting changes to test and production:

- @cicd-deployment-strategies — XMLA deployment, Fabric Git integration, and deployment pipelines compared
- @powerbi-cicd — deploying semantic models with the Tabular Editor CLI

**Reference pipelines** — complete, annotated pipelines to copy and adapt:

- @cicd-azure-devops-pipeline — Azure DevOps
- @cicd-github-actions-workflow — GitHub Actions

All automation in this section is built on the [Tabular Editor CLI](xref:te-cli). If you are migrating pipelines from the Tabular Editor 2 command line, see [Migrating from TE2 CLI](xref:te-cli-migrate).
