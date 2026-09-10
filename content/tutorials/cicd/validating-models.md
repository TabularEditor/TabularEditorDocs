---
uid: cicd-validation
title: Validating models in the pipeline
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

# Validating models in the pipeline

> [!NOTE]
> This article is under development and will be published alongside the Tabular Editor CLI general availability release.

Every pull request should answer two questions automatically: does the model follow our standards, and is it still consistent with its data sources? The Tabular Editor CLI answers both as pipeline gates.

## What this article will cover

- Running Best Practice Analyzer checks in the pipeline: rule collections, severity thresholds, failing vs. warning
- Schema validation against data sources
- Exit codes and structured output for pipeline annotations (GitHub Actions and Azure DevOps)
- Where validation runs: on pull request, after merge, before deployment
- Sharing BPA rules between the pipeline and developers' machines — see *Sharing macros, BPA rules and preferences across a team*<!-- TODO: replace with (xref:sharing-macros-bpa-rules) once users-jtb/sharing-macros-and-bpa merges -->

For CLI command details, see [CI/CD Integration](xref:te-cli-cicd) and the [Command Reference](xref:te-cli-commands).
