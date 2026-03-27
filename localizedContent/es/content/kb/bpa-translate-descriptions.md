---
uid: kb.bpa-translate-descriptions
title: Traducir las descripciones para todas las configuraciones regionales
author: Morten Lønskov
updated: 2026-01-09
description: Regla de buenas prácticas que garantiza que las descripciones de los objetos estén traducidas para todas las configuraciones regionales definidas.
---

# Traducir las descripciones para todas las configuraciones regionales

## Resumen

Esta regla identifica objetos con descripciones a las que les faltan traducciones para una o varias configuraciones regionales.

- Categoría: Diseño del modelo
- Gravedad: Baja (1)

## Se aplica a

- Modelo
- Tablas
- Medidas
- Jerarquías
- Niveles
- Perspectivas
- Columnas de datos
- Columnas calculadas
- Tablas calculadas
- Columnas de tablas calculadas

## Por qué es importante

- **Localización incompleta**: Las descripciones solo se muestran en el idioma predeterminado
- **Texto de ayuda incoherente**: Los usuarios ven una mezcla de idiomas
- **Confusión de los usuarios**: La documentación parece incompleta
- **Apariencia profesional**: Las traducciones faltantes reducen la calidad del modelo

## Cuándo se activa esta regla

```csharp
not string.IsNullOrEmpty(Description) 
and Model.Cultures.Any(string.IsNullOrEmpty(outerIt.TranslatedDescriptions[it]))
```

Esta regla se activa cuando un objeto cumple ambas condiciones:

1. El objeto tiene una descripción (no está vacía)
2. Al menos una configuración regional del modelo carece de traducción para esa descripción

En otras palabras, si tienes descripciones y varias configuraciones regionales definidas, todas las descripciones deben estar traducidas para todas las configuraciones regionales.

## Cómo solucionarlo

### Solución manual

1. En el **Explorador TOM**, selecciona el objeto
2. En el panel **Propiedades**, expande la sección **Descripciones traducidas**
3. Introduce una traducción para cada configuración regional

## Causas comunes

### Causa 1: Se añadieron nuevas descripciones

Descripciones creadas sin traducciones.

### Causa 2: Se añadió una configuración regional posteriormente

Se añadió una configuración regional después de escribir las descripciones.

### Causa 3: Traducción incompleta

El proceso de traducción no cubrió las descripciones.

## Ejemplo

### Antes de la corrección

```
Medida: [Total Revenue]
Descripción (inglés): "Sum of all revenue"
Descripción (español): (falta)
```

### Después de la corrección

```
Medida: [Total Revenue]
Descripción (inglés): "Sum of all revenue"
Descripción (español): "Suma de todos los ingresos"
```

## Nivel de compatibilidad

Esta regla se aplica a modelos con nivel de compatibilidad **1200** o superior.

## Reglas relacionadas

- [Traducir nombres visibles](xref:kb.bpa-translate-visible-names) - Traducción de nombres de objetos
- [Traducir carpetas de visualización](xref:kb.bpa-translate-display-folders) - Traducción de carpetas de visualización
