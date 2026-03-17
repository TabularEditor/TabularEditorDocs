---
uid: kb.bpa-remove-unused-data-sources
title: Eliminar Data sources sin usar
author: Morten Lønskov
updated: 2026-01-09
description: Regla de prácticas recomendadas para eliminar los Data sources huérfanos, reducir la complejidad del modelo y facilitar su mantenimiento.
---

# Eliminar Data sources sin usar

## Información general

Esta regla de prácticas recomendadas identifica Data sources a los que no hace referencia ninguna partición ni ninguna expresión de tabla. Eliminar Data sources sin usar reduce la complejidad del modelo, mejora su mantenibilidad y evita confusiones.

- Categoría: Mantenimiento
- Gravedad: Baja (1)

## Se aplica a

- Orígenes de datos del proveedor
- Orígenes de datos estructurados

## Por qué es importante

Los Data sources sin usar generan una sobrecarga innecesaria:

- **Carga de mantenimiento**: Es necesario mantener las credenciales y las cadenas de conexión de las conexiones sin uso
- **Riesgos de seguridad**: Las cadenas de conexión innecesarias pueden exponer información confidencial
- **Complejidad del modelo**: Los objetos adicionales saturan la lista de Data sources
- **Confusión**: Los desarrolladores pueden usar por error Data sources obsoletos
- **Problemas de implementación**: Los Data sources sin usar pueden apuntar a sistemas que ya no existen
- **Sobrecarga de documentación**: Los objetos adicionales requieren explicación en la documentación del modelo

Los Data sources sin usar suelen deberse a:

- Refactorizar las particiones para usar otros orígenes de datos
- Consolidar varios orígenes en uno solo
- Eliminar tablas sin limpiar los Data sources asociados
- Probar métodos de conexión alternativos

## Cuándo se activa esta regla

La regla se activa cuando un Data source cumple todas estas condiciones:

```csharp
UsedByPartitions.Count() == 0
and not Model.Tables.Any(SourceExpression.Contains(OuterIt.Name))
and not Model.AllPartitions.Any(Query.Contains(OuterIt.Name))
```

En otras palabras:

1. Ninguna partición hace referencia directamente al Data source
2. Ninguna expresión de origen de tabla (consultas M) hace referencia al Data source por su nombre
3. Ninguna consulta de partición contiene el nombre del Data source

## Cómo corregirlo

### Corrección automática

Esta regla incluye una corrección automática que elimina el Data source no utilizado:

```csharp
Delete()
```

Para aplicarlo:

1. En **Best Practice Analyzer**, selecciona los objetos marcados
2. Haz clic en **Aplicar corrección**

### Corrección manual

1. En **Explorador TOM**, expande el nodo **Data sources**
2. Haz clic con el botón derecho en el Data source no utilizado
3. Selecciona **Eliminar**
4. Confirma la eliminación

### Antes de eliminar

Comprueba que el Data source realmente no está en uso:

- Revisa todas las particiones de todas las tablas
- Busca referencias al nombre del Data source en las expresiones M
- Revisa las expresiones personalizadas y las tablas calculadas
- Asegúrate de que ninguna documentación haga referencia a la conexión

## Ejemplo

### Antes de la corrección

```
Data sources:
  - SQLServer_Production (Provider, usado por la partición Sales)
  - SQLServer_Staging (Provider, NO SE UTILIZA)  ← Eliminar
  - AzureSQL_Archive (Structured, NO SE UTILIZA)  ← Eliminar
  - PowerQuery_Web (Structured, usado por la partición Product)
```

### Después de la corrección

```
Data sources:
  - SQLServer_Production (Provider, usado por la partición Sales)
  - PowerQuery_Web (Structured, usado por la partición Product)
```

**Resultado**: Un modelo más sencillo con solo los Data sources necesarios

## Falsos positivos

La regla puede señalar Data sources que:

- Se referencian mediante expresiones M dinámicas usando variables
- Se usan en consultas de partición comentadas
- Se referencian por nombre en anotaciones o descripciones

**Solución**: Verifica manualmente antes de eliminarlo; añade comentarios o anotaciones si el Data source debe conservarse por motivos de documentación.

## Nivel de compatibilidad

Esta regla se aplica a modelos con nivel de compatibilidad **1200** o superior.