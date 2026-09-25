---
uid: kb.bpa-translate-display-folders
title: Translate Display Folders for All Cultures
author: Morten Lønskov
updated: 2026-01-09
description: Regla de buenas prácticas que garantiza que las carpetas de visualización estén traducidas para todas las configuraciones regionales definidas.
---

# Translate Display Folders for All Cultures

## Resumen

Esta regla identifica objetos visibles con carpetas de visualización a las que les faltan traducciones en una o varias configuraciones regionales.

- Categoría: Diseño del modelo
- Gravedad: baja (1)

## Se aplica a

- Medidas
- Jerarquías
- Columnas de datos
- Columnas calculadas
- Columnas de tablas calculadas

## Por qué es importante

- **Localización incompleta**: Las carpetas de visualización solo se muestran en el idioma predeterminado
- **Navegación inconsistente**: Estructura de carpetas traducida solo en parte
- **Confusión del usuario**: La organización parece incompleta
- **Imagen profesional**: La falta de traducciones reduce la calidad del modelo

## Cuándo se activa esta regla

Esta regla se activa cuando un objeto cumple las tres condiciones siguientes:

1. El objeto es **visible** para los usuarios finales (no está oculto)
2. El objeto tiene asignada una **carpeta de visualización** (para organizarlo en una estructura de carpetas)
3. Al menos a una configuración regional del modelo le **falta una traducción** para esa carpeta de visualización

En pocas palabras: los objetos visibles organizados en carpetas de visualización deben tener esos nombres de carpeta traducidos para todas las configuraciones regionales de tu modelo.

```csharp
IsVisible
and not string.IsNullOrEmpty(DisplayFolder)
and Model.Cultures.Any(string.IsNullOrEmpty(outerIt.TranslatedDisplayFolders[it]))
```

## Cómo corregir

### Solución automática

```csharp
TranslatedDisplayFolders.Reset()
```

Restablece las traducciones para usar la carpeta de visualización predeterminada.

### Solución manual

1. Selecciona el objeto en el **Explorador TOM**
2. Expande **Carpetas de visualización traducidas** en las propiedades
3. Introduce la traducción para cada configuración regional

## Causas comunes

### Causa 1: Se añadieron nuevas carpetas de visualización

Carpetas de visualización creadas sin traducciones.

### Causa 2: Configuración regional agregada más tarde

Culture added after display folders were defined.

### Causa 3: Traducción incompleta

El flujo de trabajo de traducción no incluía las carpetas de visualización.

## Ejemplo

### Antes de la corrección

```
Measure: [Total Sales]
Display Folder (English): "Sales Metrics"
Display Folder (French): (missing)
```

### Después de la corrección

```
Measure: [Total Sales]
Display Folder (English): "Sales Metrics"
Display Folder (French): "Métriques de Vente"
```

## Nivel de compatibilidad

Esta regla se aplica a modelos con nivel de compatibilidad **1200** o superior.

## Reglas relacionadas

- [Traducir nombres visibles](xref:kb.bpa-translate-visible-names) - Traducción de nombres de objetos
- [Traducir descripciones](xref:kb.bpa-translate-descriptions) - Traducción de descripciones
