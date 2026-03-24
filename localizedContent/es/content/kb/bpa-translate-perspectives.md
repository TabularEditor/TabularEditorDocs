---
uid: kb.bpa-translate-perspectives
title: Traducir los nombres de las perspectivas en todas las configuraciones regionales
author: Morten Lønskov
updated: 2026-01-09
description: Regla de buenas prácticas que garantiza que los nombres de las perspectivas estén traducidos en todas las configuraciones regionales definidas.
---

# Traducir los nombres de las perspectivas en todas las configuraciones regionales

## Resumen

Esta regla identifica las perspectivas del modelo cuyo nombre no tiene traducción en una o más configuraciones regionales.

- Categoría: Diseño del modelo
- Gravedad: Baja (1)

## Se aplica a

- Modelo
- Perspectivas

## Por qué es importante

- **Localización incompleta**: Las perspectivas se muestran solo en el idioma predeterminado
- **Experiencia incoherente**: Mezcla de nombres de perspectivas traducidos y sin traducir
- **Confusión del usuario**: La compatibilidad de idioma esperada no está disponible
- **Apariencia profesional**: Las traducciones incompletas reducen la calidad del modelo

## Cuándo se activa esta regla

Esta regla se activa cuando una perspectiva tiene:

- Al menos una configuración regional del modelo en la que **falta la traducción** del nombre de la perspectiva

```csharp
Model.Cultures.Any(string.IsNullOrEmpty(outerIt.TranslatedNames[it]))
```

## Cómo solucionarlo

### Solución manual

1. En el **Explorador TOM**, selecciona la perspectiva
2. En el panel **Propiedades**, expande **Nombres traducidos**
3. Introduce la traducción para cada configuración regional

## Causas comunes

### Causa 1: Se agregaron nuevas perspectivas

Perspectivas creadas sin traducciones.

### Causa 2: La configuración regional se agregó más tarde

La configuración regional se agregó después de que se definieran las perspectivas.

### Causa 3: Traducción incompleta

El flujo de trabajo de traducción no incluyó las perspectivas.

## Ejemplo

### Antes de la corrección

```
Perspectiva: "Sales Analysis"
Inglés: "Sales Analysis"
Alemán: (sin traducir)
```

### Después de la corrección

```
Perspectiva: "Sales Analysis"
Inglés: "Sales Analysis"
Alemán: "Vertriebsanalyse"
```

## Nivel de compatibilidad

Esta regla se aplica a modelos con nivel de compatibilidad **1200** o superior.

## Reglas relacionadas

- [Traducir nombres visibles](xref:kb.bpa-translate-visible-names) - Traducción de nombres de objetos
- [Traducir descripciones](xref:kb.bpa-translate-descriptions) - Traducción de descripciones
