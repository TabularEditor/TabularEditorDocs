---
uid: databricks-refresh-empty-catalog
title: La actualización de Databricks falla con un error de catálogo vacío
author: Morten Lønskov
updated: 2026-04-16
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# La actualización de Databricks falla con un error de catálogo vacío

> [!NOTE]
> A partir de Tabular Editor 3.26.1, el Asistente de importación de tablas usa la Implementación 2,0 de forma predeterminada para las conexiones a Databricks. Este problema solo afecta a las consultas M creadas con versiones anteriores de Tabular Editor o a las consultas M en las que el tercer parámetro de `Databricks.Catalogs()` es `null`.

Al actualizar un modelo semántico que importa datos de Databricks, puede aparecer el siguiente error:

**"[Microsoft][ThriftExtension] (38) Se intentó establecer una cadena vacía como catálogo actual. No se permite este tipo de operación."**

Este error se produce cuando la consulta M generada por el Asistente de importación de tablas usa la implementación heredada del conector con un Workspace de Databricks que requiere el controlador más reciente Arrow Database Connectivity (ADBC), también conocido como Implementación 2,0.

---

## Comprender el problema

La función de Power Query `Databricks.Catalogs()` acepta un tercer parámetro opcional que controla qué implementación del conector se usa. Cuando este parámetro es `null`, el conector usa de forma predeterminada la implementación heredada (1,0).

### Por qué sucede

1. **Los Workspaces más recientes de Databricks requieren la Implementación 2,0.** Las instancias recientes de Databricks aplican una gestión de catálogos más estricta que es incompatible con el conector heredado.

2. **El Asistente de importación de tablas en versiones de Tabular Editor anteriores a la 3.26.1 genera consultas M con `null` como tercer parámetro.** Esto significa que se usa la implementación heredada, que falla en los Workspaces más recientes de Databricks.

3. **Power BI Desktop ya usa la Implementación 2,0 de forma predeterminada.** Microsoft ha establecido el [controlador Arrow Database Connectivity](https://learn.microsoft.com/en-us/power-query/connectors/databricks#arrow-database-connectivity-driver-connector-implementation-preview) como opción predeterminada para las nuevas conexiones de Databricks en Power BI Desktop.

---

## Resolución

Edita la consulta M en cada partición afectada para incluir `[Implementation="2.0"]` (versión 2.0) como tercer parámetro de la llamada a `Databricks.Catalogs()`.

### Antes (implementación heredada)

```powerquery
let
    Source = Databricks.Catalogs("adb-xxxx.1.azuredatabricks.net", "/sql/1.0/warehouses/xxxx", null),
    Database = Source{[Name="my_catalog",Kind="Database"]}[Data],
    Schema = Database{[Name="my_schema",Kind="Schema"]}[Data],
    Data = Schema{[Name="my_table",Kind="Table"]}[Data]
in
    Data
```

### Después (Implementación 2,0)

```powerquery
let
    Source = Databricks.Catalogs("adb-xxxx.1.azuredatabricks.net", "/sql/1.0/warehouses/xxxx", [Implementation="2.0"]),
    Database = Source{[Name="my_catalog",Kind="Database"]}[Data],
    Schema = Database{[Name="my_schema",Kind="Schema"]}[Data],
    Data = Schema{[Name="my_table",Kind="Table"]}[Data]
in
    Data
```

El único cambio es sustituir `null` por `[Implementation="2.0"]` (versión 2.0) en el tercer parámetro.

### Pasos

1. Abre tu modelo en Tabular Editor 3.
2. En el **Explorador TOM**, despliega la tabla afectada y selecciona su partición.
3. En el **Editor de expresiones**, localiza la llamada a `Databricks.Catalogs(...)`.
4. Sustituye `null` (el tercer parámetro) por `[Implementation="2.0"]` (versión 2.0).
5. Repite el proceso en cada partición de Databricks de tu modelo.
6. Guarda el modelo y vuelve a intentar la actualización.

> [!TIP]
> Si tu modelo tiene muchas particiones de Databricks, usa **Editar > Buscar y reemplazar** (**Ctrl+H**) para reemplazar `Catalogs("adb-` en todas las expresiones. Como alternativa, usa el siguiente C# Script para actualizar todas las particiones de Databricks a la vez.

### Actualización masiva con un C# Script

El siguiente script busca todas las particiones M que invocan `Databricks.Catalogs` con `null` como tercer parámetro y lo reemplaza por `[Implementation="2.0"]`:

```csharp
var pattern = new System.Text.RegularExpressions.Regex(
    @"(Databricks\.Catalogs\([^,]+,\s*""[^""]*"",\s*)null(\s*\))");

var updated = 0;
foreach (var partition in Model.AllPartitions.OfType<MPartition>())
{
    if (partition.Expression == null) continue;
    var newExpr = pattern.Replace(partition.Expression, "$1[Implementation=\"2.0\"]$2");
    if (newExpr != partition.Expression)
    {
        partition.Expression = newExpr;
        updated++;
    }
}

Info($"Updated {updated} partition(s).");
```

---

## Prevención

- **Tabular Editor 3.26.1 y versiones posteriores:** El Asistente para importar tablas genera consultas M con Implementation 2,0 de forma predeterminada. Actualiza a la versión 3.26.1 o posterior para evitar este problema en las nuevas importaciones.
- **Modelos existentes:** Revisa las expresiones de las particiones de Databricks después de actualizar. Debes actualizar todas las expresiones que tengan `null` como tercer parámetro.

---

## Recursos adicionales

- [Controlador de conectividad de base de datos Arrow (documentación de Microsoft)](https://learn.microsoft.com/en-us/power-query/connectors/databricks#arrow-database-connectivity-driver-connector-implementation-preview)
- [Conectarse a Azure Databricks](xref:connecting-to-azure-databricks)
- [Asistente para importar tablas](xref:importing-tables)
- [Error de longitud en los comentarios de columnas de Databricks](xref:databricks-column-comments-length)
