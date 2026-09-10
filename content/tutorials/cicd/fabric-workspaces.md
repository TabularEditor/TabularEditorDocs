---
uid: cicd-fabric-workspaces
title: Organizing workspaces in Microsoft Fabric
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

# Organizing workspaces in Microsoft Fabric

> [!NOTE]
> This article is under development and will be published alongside the Tabular Editor CLI general availability release.

How you organize workspaces in Microsoft Fabric is the foundation of your CI/CD setup: it determines where developers work, where changes are validated, and how deployments flow toward production.

## What this article will cover

- Recommended workspace topology: development, test, and production workspaces per solution
- Personal/feature developer workspaces and how they relate to [Workspace Mode](xref:cicd-workspace-mode)
- Capacity considerations for each environment
- XMLA endpoint read/write requirements
- Permissions: developer access, service principals, and workspace roles for pipeline identities
- How the workspace topology maps to your [branching strategy](xref:cicd-branching-strategies) and [deployment strategy](xref:cicd-deployment-strategies)
