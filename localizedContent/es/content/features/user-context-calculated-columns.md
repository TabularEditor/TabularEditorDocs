---
uid: user-context-calculated-columns
title: Columnas calculadas con contexto de usuario
author: Morten Lønskov
updated: 2026-09-14
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

Normalmente, una columna calculada se evalúa una vez, cuando se procesa la tabla, y todos los usuarios que consultan el modelo ven el mismo valor. En cambio, una _columna calculada con contexto de usuario_ se evalúa para cada usuario, por lo que su expresión puede llamar a funciones como [`USERPRINCIPALNAME`](https://dax.guide/userprincipalname) o [`USERNAME`](https://dax.guide/username) y devolver un resultado distinto para cada usuario.

Esto se controla con la propiedad **Contexto de expresión** de la columna calculada.

| Contexto de expresión   | Significado                                                                                                                                             |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Estándar**            | La opción predeterminada. La expresión solo puede usar funciones estándar, y la columna tiene un valor por fila para todos los usuarios |
| **Contexto de usuario** | La expresión puede llamar a funciones de contexto de usuario y se evalúa para cada usuario                                                              |

Selecciona una columna calculada en @tom-explorer-view y establece **Contexto de expresión** en **Opciones** de la @properties-view.

> [!NOTE]
> **Contexto de expresión** requiere un nivel de compatibilidad de 1705 o superior. Por debajo de ese nivel, una columna calculada siempre es Estándar.

## Para qué no puede usarse una columna con contexto de usuario

Como el valor depende de quién consulta, una columna calculada con contexto de usuario no puede ser leída por ningún elemento que se evalúe una sola vez para todo el modelo. El Semantic Analyzer de Tabular Editor comprueba los cuatro casos y reporta un error en cada uno:

| Una columna con contexto de usuario no puede ser referenciada por | Mensaje                                                                                                                                                                                             |
| ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Una columna calculada **estándar**                                | _Esta expresión hace referencia a la columna calculada dependiente del contexto del usuario `Table[Column]`, lo cual no está permitido en una columna calculada estándar._          |
| Una **tabla calculada**                                           | _Esta expresión hace referencia a la columna calculada dependiente del contexto del usuario `Table[Column]`, lo cual no está permitido en una tabla calculada._                     |
| Un **filtro de seguridad a nivel de filas**                       | _Esta expresión hace referencia a la columna calculada dependiente del contexto del usuario `Table[Column]`, lo cual no está permitido en un filtro de seguridad a nivel de filas._ |
| Una **relación** como extremo                                     | _Una relación no puede usar la columna calculada dependiente del contexto del usuario `Table[Column]` como extremo._                                                                |

Los tres primeros se aplican _tanto de forma indirecta como directa_. Acceder a la columna a través de una medida sigue siendo acceder a ella, y se reporta de la misma manera en el Report.

Hay dos cosas que se permiten explícitamente: una _medida_ puede hacer referencia a una columna con contexto de usuario, y _otra columna calculada con contexto de usuario_ también puede hacerlo.

## Dónde aparecen los errores

| Cómo se hace referencia a la columna               | Editor de DAX | @vista-de-mensajes | `te validate` |
| -------------------------------------------------- | ------------- | ------------------------------- | ------------- |
| Directamente                                       | Sí            | Sí                              | Sí            |
| Indirectamente, por ejemplo a través de una medida | No            | Sí                              | Sí            |
| Como extremo de una relación                       | No            | Sí                              | Sí            |

En una infracción indirecta no aparece ningún subrayado ondulado en el editor, porque la expresión que estás viendo es perfectamente válida por sí sola. Lo que falla es la cadena. Consulta @vista-de-mensajes antes de implementar.

Una infracción en un extremo de una relación también aparece como la propiedad **Mensaje de error** de la relación, y se reporta una vez por cada extremo infractor, por lo que una relación con columnas con contexto de usuario en ambos extremos produce dos errores en Mensajes del Report. También se comprueban las relaciones inactivas.

> [!IMPORTANT]
> `te validate --errors-only` _no_ los oculta. Son errores, no advertencias, y `--errors-only` solo oculta advertencias y antipatrones.

## Pasos a seguir

- @vista de mensajes
- @dax-editor
- @preferencias
