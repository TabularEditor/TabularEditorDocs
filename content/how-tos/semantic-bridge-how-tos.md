---
uid: semantic-bridge-how-tos
title: Semantic Bridge How-Tos
author: Greg Baldini
updated: 2026-07-02
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.25.0
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          none: true
        - edition: Enterprise
          full: true
---
# Semantic Bridge How-Tos

These how-tos are focused on interacting with the [Databricks Metric View object model](xref:semantic-bridge-metric-view-object-model) and supporting import workflows to bring these Metric Views into a Tabular semantic model.

## Getting Started

- @semantic-bridge-load-inspect: Load a Metric View and explore its structure
- @semantic-bridge-metric-view-import-from-file: Import a Metric View directly from a YAML file
- @semantic-bridge-import: Import a loaded Metric View to Tabular and view diagnostics

## Validation

- @semantic-bridge-validate-default: Validate with built-in rules
- @semantic-bridge-validate-simple-rules: Create predicate-based validation rules for naming conventions
- @semantic-bridge-validate-contextual-rules: Create rules with cross-object checks, such as names reused across object types

## Manipulating the Object Model

- @semantic-bridge-add-object: Add objects to a Metric View and set their properties
- @semantic-bridge-remove-object: Remove objects from a Metric View
- @semantic-bridge-rename-objects: Rename a field in a Metric View

## Serialization

- @semantic-bridge-serialize: Serialize a Metric View back to YAML
