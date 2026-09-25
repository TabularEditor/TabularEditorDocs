---
uid: importing-tables-data-modeling
title: Importación de tablas y modelado del Data model
author: Daniel Otykier
updated: 2026-09-14
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Importación de tablas y modelado del Data model

Este artículo describe cómo usar el [Asistente de importación de tablas](#table-import-wizard) de Tabular Editor 3 para agregar nuevas tablas al modelo. También hay una sección sobre cómo [actualizar el esquema de la tabla](#updating-table-schema) de una tabla existente. Por último, explicamos cómo usar la [herramienta de diagramas](#working-with-diagrams) para definir y editar relaciones entre tablas.

## Asistente para importar tablas

[!include[importing-tables1](../features/import-tables.partial.md)]

# Trabajar con diagramas

En Tabular Editor 3, los **diagramas** son documentos que puedes usar para visualizar y editar las relaciones entre las tablas del modelo. Puedes crear tantos diagramas como quieras para visualizar áreas concretas de tu modelo. Un diagrama se puede guardar como un archivo independiente. Consulta <xref:supported-files#diagram-file-te3diag> para obtener más información.

> [!NOTE]
> Recomendamos crear varios diagramas pequeños en lugar de unos pocos diagramas grandes. Cuando un diagrama contiene más de unas 20 tablas, enseguida se vuelve abrumador y difícil de entender.

Después de cargar un modelo en Tabular Editor 3, elige la opción de menú **Archivo > Nuevo > Diagrama** para crear un diagrama nuevo.

[!include[diagram-basics](../features/views/diagram-basics.partial.md)]

# Pasos a seguir

- @refresh-preview-query
- @creating-and-testing-dax