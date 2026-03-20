---
uid: kb.bpa-translate-hierarchy-levels
title: Traducir los nombres de los niveles de jerarquía para todas las configuraciones regionales
author: Morten Lønskov
updated: 2026-01-09
description: Regla de buenas prácticas que garantiza que los nombres de los niveles de jerarquía estén traducidos para todas las configuraciones regionales definidas.
---

# Traducir los nombres de los niveles de jerarquía para todas las configuraciones regionales

## Descripción general

Esta regla identifica niveles de jerarquía en jerarquías visibles cuyos nombres carecen de traducciones para una o varias configuraciones regionales.

- Categoría: Diseño del modelo
- Gravedad: Baja (1)

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

## Cómo solucionarlo

### Solución manual

1. En el **Explorador TOM**, selecciona el nivel
2. En el panel **Propiedades**, expande **Nombres traducidos**
3. Introduce la traducción para cada configuración regional

## Causas habituales

### Causa 1: Se añadieron nuevos niveles

Niveles creados sin traducción.

### Causa 2: La configuración regional se añadió más tarde

Se agregó la configuración regional después de crear la jerarquía.

### Causa 3: Traducción incompleta

El proceso de traducción no cubrió todos los niveles de la jerarquía.

## Ejemplo

### Antes de corregir

```
Jerarquía: Geografía
  Nivel: País
    Inglés: "Country"
    Español: (sin traducir)
```

### Después de corregir

```
Jerarquía: Geografía
  Nivel: País
    Inglés: "Country"
    Español: "País"
```

## Nivel de compatibilidad

Esta regla se aplica a modelos con nivel de compatibilidad **1200** y superior.

## Reglas relacionadas

- [Traducir nombres visibles](xref:kb.bpa-translate-visible-names) - Traducción de nombres de objetos
- [Traducir perspectivas](xref:kb.bpa-translate-perspectives) - Traducción de nombres de perspectiva
