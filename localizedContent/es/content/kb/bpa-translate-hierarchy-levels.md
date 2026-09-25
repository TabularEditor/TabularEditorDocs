---
uid: kb.bpa-translate-hierarchy-levels
title: Traducir los nombres de los niveles de jerarquía para todas las configuraciones regionales
author: Morten Lønskov
updated: 2026-01-09
description: Regla de buenas prácticas que garantiza que los nombres de los niveles de jerarquía estén traducidos para todas las configuraciones regionales definidas.
---

# Traducir los nombres de los niveles de jerarquía para todas las configuraciones regionales

## Resumen

Esta regla identifica niveles de jerarquía en jerarquías visibles cuyos nombres carecen de traducciones para una o varias configuraciones regionales.

- Categoría: Diseño del modelo
- Gravedad: baja (1)

## Se aplica a

- Niveles (dentro de jerarquías)

## Por qué es importante

- **Localización incompleta**: Los nombres de los niveles se muestran solo en el idioma predeterminado
- **Experiencia inconsistente**: Jerarquías traducidas parcialmente
- **Confusión del usuario**: La navegación parece incompleta
- **Apariencia profesional**: La falta de traducciones reduce la calidad

## Cuándo se activa esta regla

Esta regla se activa cuando un nivel de jerarquía cumple estas dos condiciones:

1. La jerarquía que contiene el nivel es **visible** para los usuarios finales
2. Al menos una configuración regional del modelo **no tiene una traducción** para el nombre del nivel

Es decir: si tienes jerarquías visibles con varias configuraciones regionales, todos los nombres de nivel dentro de esas jerarquías deben estar traducidos para cada configuración regional.

```csharp
Hierarchy.IsVisible 
and Model.Cultures.Any(string.IsNullOrEmpty(outerIt.TranslatedNames[it]))
```

## Cómo corregir

### Corrección manual

1. En el **Explorador TOM**, selecciona el nivel
2. En el panel de **Propiedades**, expande **Nombres traducidos**
3. Introduce la traducción de cada configuración regional

## Causas comunes

### Causa 1: Se añadieron nuevos niveles

Niveles creados sin traducción.

### Causa 2: Configuración regional agregada más tarde

Culture added after hierarchy was created.

### Causa 3: Traducción incompleta

El proceso de traducción no cubrió todos los niveles de la jerarquía.

## Ejemplo

### Antes de la solución

```
Hierarchy: Geography
  Level: Country
    English: "Country"
    Spanish: (missing)
```

### Después de corregir

```
Hierarchy: Geography
  Level: Country
    English: "Country"
    Spanish: "País"
```

## Nivel de compatibilidad

Esta regla se aplica a modelos con nivel de compatibilidad **1200** y superior.

## Reglas relacionadas

- [Traducir nombres visibles](xref:kb.bpa-translate-visible-names) - Traducción de nombres de objetos
- [Traducir perspectivas](xref:kb.bpa-translate-perspectives) - Traducción de nombres de perspectiva
