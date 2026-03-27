---
uid: kb.bpa-visible-objects-no-description
title: Los objetos visibles deben tener descripciones
author: Morten Lønskov
updated: 2026-01-09
description: Regla de buenas prácticas que garantiza que los objetos visibles del modelo tengan descripciones para facilitar su descubrimiento y mejorar la experiencia del usuario.
---

# Los objetos visibles deben tener descripciones

## Resumen

Esta regla de buenas prácticas identifica tablas, columnas, medidas, grupos de cálculo y funciones definidas por el usuario visibles que carecen de descripciones. Añadir descripciones mejora la usabilidad del modelo, la calidad de la documentación y la experiencia del usuario.

- Categoría: **Mantenimiento**

- Gravedad: Baja (1)

## Se aplica a

- Tablas
- Tablas calculadas
- Columnas de datos
- Columnas calculadas
- Columnas de tablas calculadas
- Medidas
- Grupos de cálculo
- Funciones definidas por el usuario (nivel de compatibilidad 1702+)

## Por qué es importante

Las descripciones aportan contexto crítico a los usuarios del modelo:

- **Mayor facilidad de descubrimiento**: Los usuarios entienden para qué sirven los campos antes de usarlos
- **Mejor BI de autoservicio**: Los usuarios de negocio pueden trabajar de forma independiente con una guía clara
- **Menor carga de soporte**: Menos preguntas sobre las definiciones de los campos
- **Tooltips mejorados**: Power BI y Excel muestran descripciones en la información sobre herramientas al pasar el cursor
- **Fundamento de la documentación**: Las descripciones sirven de base para la documentación automatizada
- **Gobernanza y cumplimiento**: Las descripciones pueden incluir el linaje de datos y definiciones empresariales
- **Uso por IA**: Los agentes de IA pueden inferir mejor el propósito de un objeto si tiene una descripción.
  Sin descripciones, los usuarios tienen que adivinar el significado de los campos, lo que lleva a análisis incorrectos y a más solicitudes de soporte.

## Cuándo se activa esta regla

La regla se activa cuando un objeto es **visible** Y tiene una descripción vacía o formada únicamente por espacios en blanco:

```csharp
string.IsNullOrWhitespace(Description)
and
IsHidden == false
```

**Nota**: Se excluyen los objetos ocultos porque no están pensados para el consumo de los usuarios finales.

## Cómo solucionarlo

### Solución manual

1. En el **Explorador TOM**, selecciona el objeto
2. En el panel de **Propiedades**, localiza el campo **Descripción**
3. Escribe una descripción clara y concisa
4. Guarda los cambios

## Causas comunes

### Causa 1: Falta de documentación durante el desarrollo

Objetos creados sin añadir descripciones.

### Causa 2: Prototipado rápido

Modelos creados rápidamente sin la documentación adecuada.

### Causa 3: Modelos heredados

Modelos antiguos creados antes de que se establecieran los estándares de descripción.

## Ejemplo

### Antes de la solución

```
Medida: [Total Revenue]
Descripción: (vacía)
```

**Experiencia de usuario**: La información sobre herramientas no muestra información; los usuarios deben adivinar para qué sirve la medida.

### Después de la corrección

```
Medida: [Total Revenue]
Descripción: "Ingresos totales excluyendo impuestos y descuentos. Se calcula como SUM(Sales[UnitPrice] * Sales[Quantity]). Úsela para informes financieros."
```

**Experiencia de usuario**: Una información sobre herramientas clara ayuda a los usuarios a comprender y a usar correctamente la medida.

## Nivel de compatibilidad

Esta regla se aplica a modelos con nivel de compatibilidad **1200** y superior.

Las descripciones de las funciones definidas por el usuario se validan en el nivel de compatibilidad **1702** y superior.

## Reglas relacionadas

- [Evitar caracteres no válidos en las descripciones](xref:kb.bpa-avoid-invalid-characters-descriptions) - Garantizar la calidad de las descripciones
