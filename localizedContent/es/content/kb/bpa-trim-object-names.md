---
uid: kb.bpa-trim-object-names
title: Recortar espacios iniciales y finales de los nombres de los objetos
author: Morten Lønskov
updated: 2026-01-09
description: Regla de buenas prácticas para eliminar los espacios iniciales y finales de los nombres de los objetos, a fin de evitar confusiones y problemas de referencia.
---

# Recortar espacios iniciales y finales de los nombres de los objetos

## Descripción general

Esta regla de buenas prácticas identifica los objetos cuyos nombres contienen espacios al principio o al final. Estos espacios innecesarios provocan problemas de referencia en DAX, problemas de visualización y confusión en general.

- Categoría: **Convenciones de nomenclatura**
- Gravedad: baja (1)

## Se aplica a

- Modelo
- Tablas
- Medidas
- Jerarquías
- Niveles
- Perspectivas
- Particiones
- Orígenes de datos del proveedor
- Columnas de datos
- Columnas calculadas
- Tablas calculadas
- Columnas de tablas calculadas
- Orígenes de datos estructurados
- Named Expression
- Roles del modelo
- Grupos de cálculo
- Elementos de cálculo

## Por qué es importante

- **Problemas de sintaxis DAX**: Los espacios de más obligan a usar con cuidado la notación entre corchetes
- **Incoherencia en la visualización**: Los objetos aparecen desalineados en las listas de campos
- **Dificultades de búsqueda**: Es posible que los usuarios no encuentren objetos al buscar
- **Confusión en el mantenimiento**: Los desarrolladores pueden crear duplicados sin darse cuenta de que hay espacios

## Cuándo se activa esta regla

La regla se activa cuando el nombre de un objeto empieza o termina con un espacio:

```csharp
Name.StartsWith(" ") or Name.EndsWith(" ")
```

## Cómo corregirlo

### Corrección manual

1. En el **Explorador TOM**, localiza el objeto
2. Haz clic con el botón derecho y selecciona **Cambiar nombre** (o pulsa F2)
3. Quita los espacios iniciales/finales
4. Pulsa Enter para confirmar

## Causas habituales

### Causa 1: Pulsaciones accidentales de la barra espaciadora

Pulsaciones accidentales de la barra espaciadora al asignar nombres.

### Causa 2: Copiar/pegar desde fuentes externas

Copiar/pegar desde documentos con formato.

### Causa 3: Duplicación de objetos

Al duplicar objetos, el nombre llevará añadido el sufijo " copy". Es fácil pasar por alto el espacio antes de "copy"

## Ejemplo

### Antes de la corrección

```
Medidas:
  - Total Sales
  -  Total Sales  (con espacios: ¡parece diferente!)
```

DAX: `[ Total Sales]` - ¿Cuál de los dos?

### Después de la corrección

```
Medidas:
  - Total Sales (una única medida coherente)
```

DAX: `[Total Sales]` - Sin ambigüedades

## Nivel de compatibilidad

Esta regla se aplica a modelos con nivel de compatibilidad **1200** o superior.

## Reglas relacionadas

- [Evitar caracteres no válidos en los nombres](xref:kb.bpa-avoid-invalid-characters-names) - Regla relacionada de higiene de nomenclatura
