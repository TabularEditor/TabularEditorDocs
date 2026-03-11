---
uid: semantic-bridge-how-tos
title: Semantic Bridge How-Tos
author: Greg Baldini
updated: 2025-01-27
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

- @semantic-bridge-load-inspect - Load a Metric View and explore its structure
- @semantic-bridge-import - Import a Metric View to Tabular and view diagnostics

## Validation

- @semantic-bridge-validate-default - Validate with built-in rules
- @semantic-bridge-validate-simple-rules - Create predicate-based validation rules for naming conventions
- @semantic-bridge-validate-contextual-rules - Create rules with cross-object checks like duplicate detection

## Manipulating the Object Model

- @semantic-bridge-add-object - Add a new object to a Metric View
- @semantic-bridge-remove-object - Remove objects from a Metric View
- @semantic-bridge-rename-objects - Rename objects using copy-modify pattern

## Serialization

- @semantic-bridge-serialize - Serialize a Metric View back to YAML
