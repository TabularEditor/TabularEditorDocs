---
uid: semantic-bridge-how-tos
title: Guías prácticas del puente semántico
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

# Guías prácticas del puente semántico

Estas guías prácticas se centran en interactuar con el [modelo de objetos de Metric View de Databricks](xref:semantic-bridge-metric-view-object-model) y en respaldar los flujos de trabajo de importación para incorporar estas Metric Views en un modelo semántico tabular.

## Primeros pasos

- @semantic-bridge-load-inspect: Load a Metric View and explore its structure
- @semantic-bridge-metric-view-import-from-file: Import a Metric View directly from a YAML file
- @semantic-bridge-import: Import a loaded Metric View to Tabular and view diagnostics

## Validación

- @semantic-bridge-validate-default: Validate with built-in rules
- @semantic-bridge-validate-simple-rules: Create predicate-based validation rules for naming conventions
- @semantic-bridge-validate-contextual-rules: Create rules with cross-object checks, such as names reused across object types

## Manipulación del modelo de objetos

- @semantic-bridge-add-object: Add objects to a Metric View and set their properties
- @semantic-bridge-remove-object: Remove objects from a Metric View
- @semantic-bridge-rename-objects: Rename a field in a Metric View

## Serialización

- @semantic-bridge-serialize: Serialize a Metric View back to YAML

## Solución de problemas

- @semantic-bridge-metric-view-handle-failures: Handle invalid input, missing files, and imports that don't complete
