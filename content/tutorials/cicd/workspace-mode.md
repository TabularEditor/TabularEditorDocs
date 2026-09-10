---
uid: cicd-workspace-mode
title: Isolated development with Workspace Mode
author: Peer Grønnerup
updated: 2026-08-12
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          partial: true
          note: Premium Per User XMLA Endpoints Only
        - edition: Enterprise
          full: true
---

# Isolated development with Workspace Mode

> [!NOTE]
> This article is under development and will be published alongside the Tabular Editor CLI general availability release. The detailed content currently lives in [Optimizing development workflow using Workspace Mode](xref:optimizing-workflow-workspace-mode) and moves here; the Getting started article becomes a high-level overview.

Workspace Mode gives every developer a live, personal copy of the model to develop and test against — while the source of truth stays in Git.

## What this article will cover

- What Workspace Mode does: syncing local folder changes to a personal workspace database on every save
- Setting up workspace databases in a shared development workspace — see @cicd-fabric-workspaces
- Testing with live data while developing, including connecting Power BI Desktop to your workspace database
- How Workspace Mode combines with feature branches in the [parallel development workflow](xref:cicd-parallel-development)
- Limitations and considerations (e.g. models with incremental refresh)
