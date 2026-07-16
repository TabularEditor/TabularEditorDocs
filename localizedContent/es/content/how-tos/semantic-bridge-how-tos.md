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

- @semantic-bridge-load-inspect: Cargar una Metric View y explorar su estructura
- @semantic-bridge-metric-view-import-from-file: Importar una Metric View directamente desde un archivo YAML
- @semantic-bridge-import: Importar en Tabular una Metric View cargada y ver los diagnósticos

## Validación

- @semantic-bridge-validate-default: Validar con reglas integradas
- @semantic-bridge-validate-simple-rules: Crear reglas de validación basadas en predicados para convenciones de nomenclatura
- @semantic-bridge-validate-contextual-rules: Crear reglas con comprobaciones entre objetos, como nombres reutilizados en distintos tipos de objetos

## Manipulación del modelo de objetos

- @semantic-bridge-add-object: Agregar objetos a una Metric View y configurar sus propiedades
- @semantic-bridge-remove-object: Quitar objetos de una Metric View
- @semantic-bridge-rename-objects: Renombrar un campo en una Metric View

## Serialización

- @semantic-bridge-serialize: Serializar una Metric View de nuevo a YAML

## Solución de problemas

- @semantic-bridge-metric-view-handle-failures: Gestionar entradas no válidas, archivos faltantes e importaciones que no llegan a completarse
