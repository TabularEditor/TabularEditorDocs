---
uid: cicd-parallel-development
title: Parallel development with Git
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
---

# Parallel development with Git

> [!NOTE]
> This article is under development and will be published alongside the Tabular Editor CLI general availability release. The detailed content currently lives in [Enabling parallel development using Git and Save to Folder](xref:parallel-development) and moves here; the Getting started article becomes a high-level overview.

Multiple developers working on the same semantic model at the same time — without stepping on each other's changes — is what version control was made for. This article shows how Tabular Editor's folder serialization makes that workflow practical.

## What this article will cover

- The Tabular Object Model as source code
- Save to Folder (database.json) and serialization settings that minimize merge conflicts
- Power BI and version control: what changes when you commit to a JSON-based workflow
- The day-to-day workflow: branch, edit, commit, pull request, resolve conflicts
- Where validation and the Octopus Merge fit into the pull request flow — see @github-flow
