---
uid: kb.bpa-translate-visible-names
title: Traducir los nombres visibles de los objetos en todas las configuraciones regionales
author: Morten Lønskov
updated: 2026-01-09
description: Regla de buenas prácticas que garantiza que los nombres visibles de los objetos estén traducidos en todas las configuraciones regionales definidas en el modelo.
---

# Traducir los nombres visibles de los objetos en todas las configuraciones regionales

## Descripción general

Esta regla identifica objetos visibles cuyos nombres no tienen traducción para una o más configuraciones regionales definidas en el modelo.

- Categoría: Diseño del modelo
- Gravedad: Baja (1)

## Se aplica a

- Tablas
- Medidas
- Jerarquías
- Columnas de datos
- Columnas calculadas
- Tablas calculadas
- Columnas de tablas calculadas

## Por qué es importante

- **Localización incompleta**: Los usuarios de distintas configuraciones regionales ven nombres sin traducir
- **Experiencia inconsistente**: Mezcla de contenido traducido y sin traducir
- **Confusión para el usuario**: No se ofrece la compatibilidad de idioma esperada
- **Apariencia profesional**: Una traducción incompleta da una imagen poco cuidada

## Cuándo se activa esta regla

Esta regla se activa cuando un objeto cumple estas dos condiciones:

1. El objeto es **visible** para los usuarios finales (no está oculto)
2. Al menos una configuración regional del modelo **no tiene traducción** del nombre del objeto

En otras palabras, los objetos visibles con varias configuraciones regionales definidas deberían tener su nombre traducido en cada configuración regional.

```csharp
IsVisible 
and Model.Cultures.Any(string.IsNullOrEmpty(outerIt.TranslatedNames[it]))
```

## Cómo corregirlo

### Corrección manual

1. En el **Explorador TOM**, selecciona el objeto
2. En el panel de **Propiedades**, expande **Nombres traducidos**
3. Introduce la traducción de cada configuración regional
4. Guarda los cambios

## Causas habituales

### Causa 1: Se agregaron objetos nuevos

Se crearon objetos nuevos sin traducciones.

### Causa 2: Configuración regional agregada más tarde

Configuración regional agregada al modelo después de que se crearan los objetos.

### Causa 3: Proceso de traducción incompleto

El flujo de trabajo de traducción no cubrió todos los objetos.

## Ejemplo

### Antes de la corrección

```
Medida: [Total Sales]
Inglés: "Total Sales"
Español: (falta)
Francés: (falta)
```

### Después de la corrección

```
Medida: [Total Sales]
Inglés: "Total Sales"
Español: "Total de Ventas"
Francés: "Total des Ventes"
```

## Nivel de compatibilidad

Esta regla se aplica a modelos con nivel de compatibilidad **1200** o superior.

## Reglas relacionadas

- [Traducir perspectivas](xref:kb.bpa-translate-perspectives) - Traducción de los nombres de las perspectivas
- [Traducir descripciones](xref:kb.bpa-translate-descriptions) - Traducción de descripciones
