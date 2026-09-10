---
uid: cicd-testing
title: Testing semantic models
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

# Testing semantic models

> [!NOTE]
> This article is under development and will be published alongside the Tabular Editor CLI general availability release.

Validation checks that the model is well-formed; testing checks that it is *correct*. This article covers automated tests that run DAX against a deployed model and assert on the results.

## What this article will cover

- Writing DAX test queries: expected-value checks, reconciliation against source data, regression tests
- Running tests with the Tabular Editor CLI and publishing VSTEST-compatible results to the pipeline
- Testing row-level and object-level security
- When tests run: against a test deployment after merge, before promotion to production
- Organizing test definitions in the repository — see @cicd-repository-setup
