---
uid: kb.bpa-expression-required
title: Se requiere una expresión para los objetos calculados
author: Morten Lønskov
updated: 2026-01-09
description: Regla de mejores prácticas que garantiza que las medidas, las columnas calculadas y los elementos de cálculo tengan expresiones DAX válidas.
---

# Se requiere una expresión para los objetos calculados

## Resumen

Esta regla de mejores prácticas identifica medidas, columnas calculadas y elementos de cálculo que no tienen una expresión DAX. Todos los objetos calculados deben tener una expresión válida y no vacía para funcionar correctamente y evitar errores durante la implementación del modelo y la ejecución de consultas.

- Categoría: Prevención de errores

- Gravedad: Alta (3)

## Se aplica a

- Medidas
- Columnas calculadas
- Elementos de cálculo

## Por qué es importante

Los objetos calculados sin una expresión provocarán fallos críticos:

- **Errores de validación del modelo**: el modelo no superará la validación al guardarse o implementarse
- **Errores en las consultas**: los intentos de usar el objeto en consultas generarán errores
- **Dependencias rotas**: otras medidas o cálculos que hagan referencia al objeto fallarán
- **Bloqueos de implementación**: Power BI Service y Analysis Services rechazarán los modelos con expresiones vacías
- **Comportamiento inesperado**: el objeto puede aparecer en las listas de campos, pero no devolver resultados

Las expresiones vacías suelen deberse a una creación incompleta del objeto, operaciones de copiar y pegar o errores en la generación programática del modelo.

## Cuándo se activa esta regla

La regla se activa cuando cualquiera de los siguientes objetos tenga una expresión vacía o compuesta solo por espacios en blanco:

```csharp
string.IsNullOrWhiteSpace(Expression)
```

Esto se aplica a:

- **Medidas**: deben contener una agregación o un cálculo DAX
- **Columnas calculadas**: deben contener una expresión DAX con contexto de fila
- **Elementos de cálculo**: deben contener una expresión DAX que modifique la medida base

## Cómo corregirlo

### Corrección manual

1. En el **Explorador TOM**, localiza la medida, la columna calculada o el elemento de cálculo
2. Haz doble clic para abrir el **Editor de DAX**
3. Introduce una expresión DAX válida
4. Valida la sintaxis y guarda los cambios

## Causas comunes

### Causa 1: Creación incompleta

El objeto se creó con la intención de definirlo más adelante, pero se olvidó hacerlo.

### Causa 2: Creación basada en plantillas

Los scripts o las plantillas crearon objetos sin expresiones.

### Causa 3: Error en la operación de copia

Copiaste un objeto, pero la expresión no se transfirió.

## Ejemplo

### Antes de la corrección

```
Medida: [Total Revenue]
  Expresión: [empty]
  FormatString: $#.0,00
```

**Error al consultar**: "La expresión de la medida '[Total Revenue]' no es válida."

### Después de la corrección

```
Medida: [Total Revenue]
  Expresión: SUM('Sales'[Revenue])
  FormatString: $#.0,00
```

**Resultado**: La medida funciona correctamente y devuelve los ingresos agregados.

## Nivel de compatibilidad

Esta regla se aplica a los modelos con un nivel de compatibilidad **1200** o superior.

