---
uid: kb.bpa-avoid-invalid-characters-names
title: Evite caracteres no válidos en los nombres de los objetos
author: Morten Lønskov
updated: 2026-01-09
description: Regla de mejores prácticas que evita errores de implementación al identificar caracteres de control en los nombres de los objetos.
---

# Evite caracteres no válidos en los nombres de los objetos

## Información general

Esta regla de mejores prácticas identifica objetos cuyos nombres contienen caracteres de control no válidos (caracteres no imprimibles, excepto los espacios en blanco estándar). Estos caracteres pueden provocar fallos de implementación, problemas de representación y corrupción de datos.

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

Los caracteres de control en los nombres de los objetos provocan problemas graves:

- **Fallos de implementación**: Power BI Service y Analysis Services pueden rechazar modelos con caracteres no válidos
- **Problemas de renderizado**: Las herramientas cliente pueden mostrar nombres ilegibles o invisibles
- **Errores de análisis de DAX**: Los caracteres no válidos pueden invalidar expresiones DAX que hagan referencia al objeto
- **Corrupción de XML**: Los metadatos del modelo (TMSL/XMLA) pueden quedar mal formados
- **Problemas al copiar y pegar**: Es posible que los nombres no se transfieran correctamente entre aplicaciones
- **Problemas de codificación**: Incidencias de compatibilidad entre plataformas

Se permite el espacio en blanco estándar (espacios, saltos de línea, retornos de carro), pero deben eliminarse los caracteres de control.

## Cuándo se activa esta regla

La regla se activa cuando el nombre de un objeto contiene caracteres de control que no son espacios en blanco estándar:

```csharp
Name.ToCharArray().Any(char.IsControl(it) and !char.IsWhiteSpace(it))
```

Esto detecta caracteres problemáticos y, a la vez, permite un formato de espacio en blanco válido.

## Cómo solucionarlo

### Corrección automática

Esta regla incluye una corrección automática que reemplaza los caracteres no válidos por espacios:

```csharp
Name = string.Concat(
    it.Name.ToCharArray().Select(
        c => (char.IsControl(c) && !char.IsWhiteSpace(c)) ? ' ' : c
    )
)
```

Para aplicarlo:

1. En el **Best Practice Analyzer**, selecciona los objetos marcados
2. Haz clic en **Aplicar corrección**

### Corrección manual

1. En el **Explorador TOM**, selecciona el objeto
2. En el panel **Propiedades**, busca el campo **Nombre**
3. Edita el nombre para eliminar los caracteres no válidos
4. Guarda los cambios

## Causas comunes

### Causa 1: Copiar y pegar desde texto enriquecido

Copiar nombres desde documentos de Word, páginas web o correos electrónicos puede introducir caracteres de formato ocultos.

### Causa 2: Generación automatizada de nombres

Los scripts que generan nombres pueden incluir caracteres de control de los sistemas de origen.

### Causa 3: Importación de datos desde orígenes externos

Importación de metadatos que contienen artefactos de codificación o códigos de control.

## Ejemplo

### Antes de la corrección

```
Nombre de la medida: "Total\x00Sales"  (contiene un carácter NULL)
```

La implementación falla con el error "Invalid character in object name"

### Después de la corrección

```
Nombre de la medida: "Total Sales"  (NULL sustituido por un espacio)
```

Se implementa correctamente y se muestra correctamente en todas las herramientas.

## Nivel de compatibilidad

Esta regla se aplica a modelos con nivel de compatibilidad **1200** o superior.

## Reglas relacionadas

- [Evitar caracteres no válidos en las descripciones](xref:kb.bpa-avoid-invalid-characters-descriptions) - Validación similar para las propiedades de descripción
- [Recortar nombres de objetos](xref:kb.bpa-trim-object-names) - Eliminación de espacios al inicio y al final

## Más información

- [Reglas de nomenclatura de DAX](https://learn.microsoft.com/dax/dax-syntax-reference)
