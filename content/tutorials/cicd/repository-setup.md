---
uid: cicd-repository-setup
title: Setting up your repository
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

# Setting up your repository

> [!NOTE]
> This article is under development and will be published alongside the Tabular Editor CLI general availability release.

A well-structured Git repository makes everything downstream easier: reviews stay readable, pipelines stay simple, and team assets stay in sync.

## What this article will cover

- Choosing a serialization format: Save to Folder (database.json) vs. TMDL
- Recommended repository layout: model metadata, BPA rules, macros, pipeline definitions
- One repository per model vs. shared repositories
- What to `.gitignore`
- Pull request policies and branch protection
- Keeping team assets in the repository — see also *Sharing macros, BPA rules and preferences across a team*<!-- TODO: replace with (xref:sharing-macros-bpa-rules) once users-jtb/sharing-macros-and-bpa merges -->
