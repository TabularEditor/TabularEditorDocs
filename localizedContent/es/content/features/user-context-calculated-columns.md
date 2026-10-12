---
uid: user-context-calculated-columns
title: Columnas calculadas con contexto de usuario
author: Morten Lønskov
updated: 2026-10-12
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.27.0
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Columnas calculadas con contexto de usuario

Una _columna calculada con contexto de usuario_ es una columna calculada que se evalúa por usuario. Su expresión puede llamar a funciones como [`USERPRINCIPALNAME`](https://dax.guide/userprincipalname) o [`USERNAME`](https://dax.guide/username) y devolver un valor distinto para cada usuario. En cambio, una columna calculada estándar se evalúa una sola vez, cuando se procesa la tabla, y devuelve el mismo valor para todos los usuarios.

La propiedad `ExpressionContext` de la columna calculada determina si la columna se evalúa una sola vez o por usuario:

| Contexto de expresión   | Significado                                                                                                                                                                                   |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Estándar**            | La opción predeterminada. La expresión solo puede usar funciones estándar. La columna tiene un valor por fila, igual para todos los usuarios. |
| **Contexto de usuario** | La expresión puede llamar a funciones de contexto de usuario. La columna se evalúa para cada usuario.                                                         |

Selecciona una columna calculada en @tom-explorer-view y establece **Contexto de expresión** en **Opciones** de @properties-view.

> [!NOTE]
> `ExpressionContext` requiere un nivel de compatibilidad 1705 o superior; por debajo de 1705, las columnas calculadas siempre son **Standard**.

## Para qué no se puede usar una columna con contexto de usuario

Los objetos que se evalúan una vez para todo el modelo no pueden hacer referencia a una columna calculada con contexto de usuario. El analizador semántico de Tabular Editor informa de un error en cada uno de estos casos:

| Una columna con contexto de usuario no puede ser referenciada por | Mensaje                                                                                                                                                                               |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Una columna calculada estándar                                    | "Esta expresión hace referencia a la columna calculada con contexto de usuario `Table[Column]`, lo que no está permitido en una columna calculada estándar."          |
| Una tabla calculada                                               | "Esta expresión hace referencia a la columna calculada con contexto de usuario `Table[Column]`, lo que no está permitido en una tabla calculada."                     |
| Un filtro de seguridad a nivel de filas                           | "Esta expresión hace referencia a la columna calculada con contexto de usuario `Table[Column]`, lo que no está permitido en un filtro de seguridad a nivel de filas." |
| Una relación, como uno de sus extremos                            | "Una relación no puede usar la columna calculada con contexto de usuario `Table[Column]` como uno de sus extremos."                                                   |

Las tres primeras reglas también se aplican a las referencias indirectas, por ejemplo, a través de una medida. Las medidas y otras columnas calculadas con contexto de usuario pueden hacer referencia a una columna con contexto de usuario.

## Dónde aparecen los errores

| Cómo se hace referencia a la columna            | Editor de DAX | @vista-de-mensajes | [`te validate`](xref:te-cli-commands#validate) |
| ----------------------------------------------- | ------------- | ------------------------------- | ---------------------------------------------- |
| Directamente                                    | Sí            | Sí                              | Sí                                             |
| Indirectamente, por ejemplo mediante una medida | No            | Sí                              | Sí                                             |
| Como extremo de una relación                    | No            | Sí                              | Sí                                             |

El editor de DAX no subraya las infracciones indirectas, así que revisa los mensajes en @messages-view antes de desplegar.

Una infracción en un extremo de la relación también aparece en la propiedad **Mensajes de error** de la relación. Se comprueban tanto las relaciones activas como las inactivas, y los errores se reportan por extremo, así que una relación con columnas de contexto de usuario en ambos extremos tendrá dos errores.

> [!NOTE]
> `te validate --errors-only` sigue reportando estas infracciones, ya que la opción solo oculta advertencias y antipatrones.

## Pasos a seguir

- @vista de mensajes
- @dax-editor
- @preferencias
