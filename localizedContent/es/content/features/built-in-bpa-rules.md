---
uid: built-in-bpa-rules
title: Reglas BPA integradas
author: Morten Lønskov
updated: 2026-01-09
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.24.0
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
description: Función de la Edición Enterprise que ofrece 27 reglas de prácticas recomendadas seleccionadas e incorporadas de forma nativa en Tabular Editor 3, con integración en la base de conocimiento.
---

# Reglas BPA integradas

## Información general

La Edición Enterprise de Tabular Editor 3 incluye 27 reglas de prácticas recomendadas integradas. Estas reglas cubren problemas habituales en el desarrollo de un modelo semántico y se actualizan automáticamente con cada versión.

A diferencia de las reglas personalizadas almacenadas en archivos JSON, las reglas integradas:

- Están integradas directamente en la aplicación
- Se actualizan automáticamente con las nuevas versiones
- Vinculan a la documentación de la base de conocimiento
- Son de solo lectura para garantizar la coherencia entre equipos
- Funcionan al instante sin configuración

## Características principales

### Categorías de reglas

Las 27 reglas integradas cubren cuatro áreas:

- **Prevención de errores**: caracteres no válidos, expresiones ausentes, incompatibilidades de tipo de datos
- **Rendimiento**: relaciones, particiones, agregaciones
- **Formato**: cadenas de formato, visibilidad, convenciones de nomenclatura
- **Mantenimiento**: descripciones, grupos de cálculo, objetos sin usar

### Control global y por regla

![Captura de pantalla que muestra las preferencias de BPA con el conmutador global de habilitación/deshabilitación y casillas de verificación por regla](~/content/assets/images/features/bpa-built-in-rules-preferences.png)
Puede habilitar o deshabilitar las reglas integradas de forma global o individual. La configuración se mantiene entre sesiones y funciona de forma independiente de sus reglas personalizadas.

Para administrar las reglas integradas:

1. Vaya a **Herramientas** > **Preferencias** > **Best Practice Analyzer**
2. Busque la sección **Reglas integradas**
3. Active o desactive **Habilitar reglas integradas** para activar o desactivar toda la colección
4. Use el BPA Manager para habilitar o deshabilitar reglas individuales

### Notificación al iniciar por primera vez

![Captura de pantalla del cuadro de diálogo de notificación al iniciar por primera vez, que presenta las reglas BPA integradas](~/content/assets/images/features/bpa-built-in-rules-notification.png)

La primera vez que abras un modelo después de actualizar a una versión con reglas integradas, verás una notificación que explica la característica e incluye un enlace a las preferencias. Esta notificación solo aparece una vez.

### Integración con la base de conocimientos

![Captura de pantalla que muestra la ventana de BPA con una regla seleccionada y el botón "Ver documentación" resaltado](~/content/assets/images/features/bpa-built-in-rules-kb-link.png)

Cada regla integrada enlaza a un artículo de la base de conocimientos mediante la propiedad `KnowledgeBaseArticle`. Cada artículo explica qué comprueba la regla, por qué es importante y cómo corregir las infracciones.

Para ver la documentación, selecciona una regla en la ventana de Best Practice Analyzer.

### Protección de solo lectura

Las reglas integradas no se pueden editar, clonar ni eliminar. Esto garantiza que todos los usuarios tengan las mismas definiciones de reglas. Puedes desactivar reglas individuales, pero las definiciones de las reglas en sí permanecen sin cambios.

![Captura de pantalla que muestra una regla integrada con una insignia o un icono de solo lectura en la ventana de BPA](~/content/assets/images/features/bpa-built-in-rules-readonly.png)

### Prevención de colisiones de ID

Las reglas integradas usan prefijos de ID reservados. Cuando creas una regla personalizada, Tabular Editor valida que tu ID no entre en conflicto con las reglas integradas y muestra un error si lo hace.

## Catálogo de reglas integradas

La versión inicial incluye las siguientes reglas:

### Reglas de prevención de errores

- [Evitar caracteres no válidos en los nombres de los objetos](xref:kb.bpa-avoid-invalid-characters-names)
- [Evita caracteres no válidos en las descripciones](xref:kb.bpa-avoid-invalid-characters-descriptions)
- [Se requiere una expresión para los objetos calculados](xref:kb.bpa-expression-required)
- [La columna de datos debe tener un origen](xref:kb.bpa-data-column-source)
- [Las columnas de relación deben tener el mismo tipo de datos](xref:kb.bpa-relationship-same-datatype)
- [Evita las particiones del proveedor con orígenes de datos estructurados](xref:kb.bpa-avoid-provider-partitions-structured)

### Reglas de rendimiento

- [Las relaciones de muchos a muchos deben usar una sola dirección](xref:kb.bpa-many-to-many-single-direction)
- [Oculta las columnas de clave externa](xref:kb.bpa-hide-foreign-keys)
- [Establece SummarizeBy en None para las columnas numéricas](xref:kb.bpa-do-not-summarize-numeric)
- [Elimina las tablas automáticas de fechas](xref:kb.bpa-remove-auto-date-table)
- [Elimina las fuentes de datos no utilizadas](xref:kb.bpa-remove-unused-data-sources)

### Reglas de formato

- [Proporciona una cadena de formato para las medidas](xref:kb.bpa-format-string-measures)
- [Proporciona una cadena de formato para columnas numéricas y de fecha](xref:kb.bpa-format-string-columns)
- [Los objetos visibles deben tener descripciones](xref:kb.bpa-visible-objects-no-description)
- [Recorta los nombres de los objetos](xref:kb.bpa-trim-object-names)
- [Debe existir una tabla de fechas](xref:kb.bpa-date-table-exists)

### Reglas de mantenimiento

- [Los grupos de cálculo deben contener elementos](xref:kb.bpa-calculation-groups-no-items)
- [Las perspectivas deben contener objetos](xref:kb.bpa-perspectives-no-objects)
- [Usa el nivel de compatibilidad más reciente de Power BI](xref:kb.bpa-powerbi-latest-compatibility)

## Trabajar con reglas integradas y personalizadas

Las reglas integradas y las personalizadas conviven:

| Característica      | Reglas integradas                        | Reglas personalizadas                       |
| ------------------- | ---------------------------------------- | ------------------------------------------- |
| **Almacenamiento**  | Integrado en el código de la aplicación  | Archivos JSON o anotaciones del modelo      |
| **Actualizaciones** | Automático con cada versión              | Requiere edición manual                     |
| **Modificación**    | Solo lectura                             | Totalmente editable                         |
| **Documentación**   | Artículos de KB integrados               | Descripciones proporcionadas por el usuario |
| **Disponibilidad**  | Solo disponible en la Edición Enterprise | Todas las ediciones                         |
| **Compartir**       | Consistente entre equipos                | Requiere distribución manual                |

### Flujo de trabajo recomendado

1. Habilita las reglas integradas para obtener cobertura inmediata
2. Revisa las infracciones y aplica correcciones
3. Deshabilita las reglas que no se ajusten a tus convenciones
4. Añade reglas personalizadas para requisitos específicos de la organización
5. Usa la función "Ignorar" para infracciones deliberadas

## Prácticas recomendadas

### Incorporación de equipos

Al implementar las reglas integradas en tu equipo:

- Empieza con todas las reglas habilitadas para establecer una línea de referencia
- Revisen las infracciones en conjunto y acuerden qué reglas se aplican
- Documenta por qué se deshabilitan reglas específicas
- Añade reglas personalizadas para requisitos específicos de la organización

### Mantenimiento del modelo

- Ejecuta el BPA antes de confirmar los cambios en el control de versiones
- Corrige las infracciones de alta gravedad de inmediato
- Revisa periódicamente los problemas de gravedad media y baja
- Usa correcciones automáticas cuando estén disponibles

### Reglas personalizadas

- No dupliques la funcionalidad de las reglas integradas
- Usa prefijos de ID distintos para evitar conflictos
- Documenta tus reglas personalizadas
- Comparte colecciones de reglas con tu equipo

## Solución de problemas

### Las reglas integradas no aparecen

Si las reglas integradas no se muestran en la ventana del BPA:

1. Comprueba que estás usando Tabular Editor 3 Edición Enterprise
2. Verifica que las reglas integradas estén habilitadas en **Tools** > **Preferences** > **Best Practice Analyzer**
3. Reinicia Tabular Editor si acabas de cambiar las preferencias
4. Confirma que tu licencia está activa

### No se puede modificar una regla integrada

Es lo esperado. Las reglas integradas son de solo lectura. Si necesitas una lógica distinta, crea una regla personalizada con tu expresión y desactiva la regla integrada correspondiente.

### Error de colisión de ID

Las reglas integradas reservan ciertos prefijos de ID. Elige un ID diferente que no empiece por `TE3_BUILT_IN`.

## Compatibilidad

- Requiere Tabular Editor 3.24.0 o una versión posterior
- Solo para la Edición Enterprise
- Funciona con todos los niveles de compatibilidad (1200+)

## Siguientes pasos

- [Uso del Best Practice Analyzer](xref:using-bpa)
- [Reglas y expresiones de ejemplo de BPA](xref:using-bpa-sample-rules-expressions)
- [Reglas BPA personalizadas](xref:best-practice-analyzer)