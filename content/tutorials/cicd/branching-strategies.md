---
uid: cicd-branching-strategies
title: Branching strategies
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

# Branching strategies

> [!NOTE]
> This article is under development and will be published alongside the Tabular Editor CLI general availability release.

Your branching strategy decides how changes flow from a developer's machine to production — and how your branches map to workspaces and deployment environments.

## What this article will cover

- GitHub Flow with the Octopus Merge pattern (recommended) — see the deep dive in @github-flow
- GitFlow for teams with formal, versioned releases
- Trunk-based development as the simplest baseline
- Mapping branches to Fabric workspaces and deployment environments
- Choosing a strategy: team size, release cadence, and environment count
