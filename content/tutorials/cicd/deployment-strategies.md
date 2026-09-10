---
uid: cicd-deployment-strategies
title: Deployment strategies
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

# Deployment strategies

> [!NOTE]
> This article is under development and will be published alongside the Tabular Editor CLI general availability release.

There is more than one way to get a semantic model from Git to a workspace. This article compares the options and helps you pick — or combine — the right ones for your environments.

## What this article will cover

- Metadata deployment via the XMLA endpoint with the Tabular Editor CLI
- Fabric Git integration: what it does, and where it fits alongside pipeline-driven deployment
- Fabric deployment pipelines and how they compare to Git-based promotion
- Handling environment differences: data source connections, partitions, roles and members
- Refresh after deployment
- Promotion flows: dev → test → prod, and how they map to your [branching strategy](xref:cicd-branching-strategies)

> [!NOTE]
> Deploying to Azure Analysis Services or SQL Server Analysis Services follows the same XMLA-based approach with a few differences (authentication, endpoints, no Fabric Git integration). These differences are called out inline where relevant.
