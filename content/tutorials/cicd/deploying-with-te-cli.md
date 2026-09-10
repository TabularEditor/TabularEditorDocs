---
uid: powerbi-cicd
title: Deploying with the Tabular Editor CLI
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

# Deploying with the Tabular Editor CLI

> [!NOTE]
> This article is under development and will be published alongside the Tabular Editor CLI general availability release.

The hands-on deployment article: from serialized model metadata in Git to a deployed semantic model in Power BI/Fabric, using the Tabular Editor CLI in a pipeline.

## What this article will cover

- Authenticating in a pipeline: service principals and secret handling — see [Authentication and Connections](xref:te-cli-auth)
- Deploying model metadata to a workspace via the XMLA endpoint
- Controlling what gets deployed: roles, members, partitions, connections
- Environment-specific configuration at deploy time
- Triggering a refresh after deployment
- Verifying a deployment and handling failures

> [!NOTE]
> Deploying to Azure Analysis Services or SQL Server Analysis Services uses the same commands with different endpoints and authentication options — called out inline where the steps differ.

For the complete pipeline context around this step, see the reference pipelines for [Azure DevOps](xref:cicd-azure-devops-pipeline) and [GitHub Actions](xref:cicd-github-actions-workflow).
