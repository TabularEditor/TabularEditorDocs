---
uid: kb.bpa-avoid-invalid-characters-descriptions
title: Evitar caracteres no válidos en las descripciones
author: Morten Lønskov
updated: 2026-01-09
description: Regla de prácticas recomendadas que evita problemas de visualización e implementación al identificar caracteres de control en las descripciones de los objetos.
---

# Evitar caracteres no válidos en las descripciones

## Información general

Esta regla de buenas prácticas identifica objetos cuyas descripciones contienen caracteres de control no válidos (caracteres no imprimibles, excepto los espacios en blanco estándar). Estos caracteres pueden provocar problemas de visualización, corrupción de metadatos y fallos de implementación.

- Categoría: Prevención de errores
- Gravedad: Alta (3)

## Se aplica a

- Tablas
- Medidas
- Jerarquías
- Niveles
- Perspectivas
- Particiones
- Columnas de datos
- Columnas calculadas
- Columnas de tablas calculadas
- KPI
- Roles del modelo
- Grupos de cálculo
- Elementos de cálculo

## Por qué es importante

Los caracteres de control en las descripciones provocan varios problemas:

- **Corrupción de la visualización**: Las descripciones emergentes y los paneles de documentación pueden mostrar texto ilegible
- **Problemas de metadatos**: La exportación TMSL/XMLA puede generar XML no válido
- **Fallos de despliegue**: Power BI Service o Analysis Services pueden rechazar el modelo
- **Problemas de documentación**: La documentación generada puede romper el formato
- **Errores de codificación**: Problemas de sincronización multiplataforma
- **Confusión del usuario**: Los caracteres invisibles generan descripciones confusas o dañadas

El espacio en blanco estándar (espacios, saltos de línea, tabulaciones) es aceptable, pero deben eliminarse los caracteres de control no imprimibles.

## Cuándo se activa esta regla

La regla se activa cuando la descripción de un objeto contiene caracteres de control que no sean espacios en blanco estándar:

```csharp
Description.ToCharArray().Any(char.IsControl(it) and !char.IsWhiteSpace(it))
```

Esto detecta caracteres problemáticos y, al mismo tiempo, permite el espaciado legítimo.

## Cómo corregirlo

### Corrección automática

Esta regla incluye una corrección automática que reemplaza los caracteres no válidos por espacios:

```csharp
Description = string.Concat(
    it.Description.ToCharArray().Select(
        c => (char.IsControl(c) && !char.IsWhiteSpace(c)) ? ' ' : c
    )
)
```

Para aplicarlo:

1. En el **Best Practice Analyzer**, selecciona los objetos marcados
2. Haz clic en **Aplicar corrección**

### Corrección manual

1. En el **Explorador TOM**, selecciona el objeto
2. En el panel **Propiedades**, localiza el campo **Descripción**
3. Edita la descripción para eliminar los caracteres no válidos
4. Guarda los cambios

## Causas comunes

### Causa 1: Copiar y pegar desde texto enriquecido

Copiar descripciones desde documentos de Word, páginas web o correos electrónicos puede introducir caracteres de formato ocultos.

### Causa 2: Generación automática de documentación

Los scripts que generan descripciones pueden incluir caracteres de control procedentes de los sistemas de origen.

### Causa 3: Importación de datos desde orígenes externos

La importación de metadatos que contienen artefactos de codificación o códigos de control.

## Ejemplo

### Antes de la corrección

```
Medida: [Total Revenue]
Descripción: "Calcula\x00ingresos\x0Btotales"  (contiene NULL y tabulación vertical)
```

La información sobre herramientas muestra: "Calcula□los□ingresos totales" (con corrupción visible)

### Después de la corrección

```
Medida: [Total Revenue]
Descripción: "Calcula los ingresos totales"  (los caracteres de control se sustituyen por espacios)
```

El tooltip se muestra correctamente: "Calcula los ingresos totales"

## Nivel de compatibilidad

Esta regla se aplica a los modelos con nivel de compatibilidad **1200** y superior.

## Reglas relacionadas

- [Evitar caracteres no válidos en los nombres](xref:kb.bpa-avoid-invalid-characters-names) - Validación similar para los nombres de objetos
- [Los objetos visibles deben tener descripciones](xref:kb.bpa-visible-objects-no-description) - Garantiza que existan descripciones
