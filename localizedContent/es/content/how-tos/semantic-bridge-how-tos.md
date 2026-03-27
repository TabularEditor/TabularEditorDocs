---
uid: semantic-bridge-how-tos
title: Guías prácticas del puente semántico
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

# Guías prácticas del puente semántico

Estas guías prácticas se centran en interactuar con el [modelo de objetos de Metric View de Databricks](xref:semantic-bridge-metric-view-object-model) y en respaldar los flujos de trabajo de importación para incorporar estas Metric Views en un modelo semántico tabular.

## Primeros pasos

- @semantic-bridge-load-inspect - Cargar una Metric View y explorar su estructura
- @semantic-bridge-import - Importar una Metric View a Tabular y ver los diagnósticos

## Validación

- @semantic-bridge-validate-default - Validar con reglas integradas
- @semantic-bridge-validate-simple-rules - Crear reglas de validación basadas en predicados para convenciones de nomenclatura
- @semantic-bridge-validate-contextual-rules - Crear reglas con comprobaciones entre objetos, como la detección de duplicados

## Manipulación del modelo de objetos

- @semantic-bridge-add-object - Agregar un nuevo objeto a una Metric View
- @semantic-bridge-remove-object - Quitar objetos de una Metric View
- @semantic-bridge-rename-objects - Cambiar el nombre de los objetos mediante el patrón de copiar y modificar

## Serialización

- @semantic-bridge-serialize - Serializar una Metric View de nuevo a YAML
