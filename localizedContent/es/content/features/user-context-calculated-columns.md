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

Normalmente, una columna calculada se evalúa una sola vez, cuando se procesa la tabla, y todos los usuarios que consultan el modelo ven el mismo valor. En cambio, una _columna calculada con contexto de usuario_ se evalúa por usuario, por lo que su expresión puede llamar a funciones como [`USERPRINCIPALNAME`](https://dax.guide/userprincipalname) o [`USERNAME`](https://dax.guide/username) y dar una respuesta diferente a cada usuario.

Esto se controla mediante la propiedad **Contexto de expresión** de la columna calculada.

| Contexto de expresión   | Significado                                                                                                                               |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **Estándar**            | La opción predeterminada. La expresión solo puede usar funciones estándar y la columna tiene un valor por fila para todos |
| **Contexto de usuario** | La expresión puede llamar a funciones de contexto de usuario y se evalúa por usuario                                                      |

Selecciona una columna calculada en @tom-explorer-view y establece **Contexto de expresión** en **Opciones** de @properties-view.

> [!NOTE]
> **Contexto de expresión** requiere un nivel de compatibilidad 1705 o superior. Por debajo de ese nivel, una columna calculada siempre es Estándar.

## Para qué no se puede usar una columna con contexto de usuario

Como el valor depende de quién realiza la consulta, una columna calculada con contexto de usuario no puede ser leída por ningún elemento que se evalúe una sola vez para todo el modelo. El analizador semántico de Tabular Editor comprueba los cuatro casos y genera un Report de error para cada uno:

| Una columna con contexto de usuario no puede ser referenciada por | Mensaje                                                                                                                                                                                         |
| ----------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Una columna calculada **estándar**                                | _Esta expresión hace referencia a la columna calculada sensible al contexto del usuario `Table[Column]`, lo cual no está permitido en una columna calculada estándar._          |
| Una **tabla calculada**                                           | _Esta expresión hace referencia a la columna calculada sensible al contexto del usuario `Table[Column]`, lo cual no está permitido en una tabla calculada._                     |
| Un **filtro de seguridad a nivel de filas**                       | _Esta expresión hace referencia a la columna calculada sensible al contexto del usuario `Table[Column]`, lo cual no está permitido en un filtro de seguridad a nivel de filas._ |
| Una **relación**, como extremo                                    | _Una relación no puede usar la columna calculada sensible al contexto del usuario `Table[Column]` como uno de sus extremos._                                                    |

Los tres primeros se aplican _tanto de forma indirecta como directa_. Acceder a la columna a través de una medida sigue siendo acceder a ella, y se notifica del mismo modo.

Hay dos cosas que se permiten explícitamente: una _medida_ puede hacer referencia a una columna sensible al contexto del usuario, y también puede hacerlo _otra columna calculada sensible al contexto del usuario_.

## Dónde aparecen los errores

| Cómo se hace referencia a la columna            | Editor de DAX | @vista-de-mensajes | `te validate` |
| ----------------------------------------------- | ------------- | ------------------------------- | ------------- |
| Directamente                                    | Sí            | Sí                              | Sí            |
| Indirectamente, por ejemplo mediante una medida | No            | Sí                              | Sí            |
| Como extremo de una relación                    | No            | Sí                              | Sí            |

Una infracción indirecta no aparece subrayada con una línea ondulada en el editor, porque la expresión que estás viendo es perfectamente válida por sí sola. Lo que se rompe es la cadena. Revisa @vista-de-mensajes antes de desplegar.

Una infracción en un extremo de relación también aparece como la propiedad **Mensaje de error** de la relación, y se notifica una vez por cada extremo infractor; por lo tanto, una relación con columnas sensibles al contexto del usuario en ambos extremos genera dos errores. También se comprueban las relaciones inactivas.

> [!IMPORTANT]
> `te validate --errors-only` _no_ los oculta. Son errores, no advertencias, y `--errors-only` solo oculta las advertencias y los antipatrones.

## Pasos a seguir

- @vista de mensajes
- @dax-editor
- @preferencias
