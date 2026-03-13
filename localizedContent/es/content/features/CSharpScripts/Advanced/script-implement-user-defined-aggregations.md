---
uid: script-implement-user-defined-aggregations
title: Implementar agregaciones definidas por el usuario
author: Just Blindbæk
updated: 2026-02-22
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Implementar agregaciones definidas por el usuario

## Propósito del script

Este script automatiza por completo la configuración de agregaciones definidas por el usuario para una tabla de hechos seleccionada.

El script realiza los siguientes pasos, tal y como se describe en el tutorial [Implementación de agregaciones definidas por el usuario](xref:user-defined-aggregations):

1. Clona la tabla de hechos seleccionada y cambia el nombre de la copia a `<FactTableName> details`
2. Establece el modo de almacenamiento **Dual** en todas las particiones de las tablas de dimensiones relacionadas
3. Reduce la tabla de detalle a una sola partición, la establece en DirectQuery, oculta todas las columnas, oculta la tabla y elimina las medidas copiadas
4. Crea relaciones desde la tabla de detalle a las tablas de dimensiones con **Confiar en la integridad referencial** habilitada
5. Quita las columnas de atributos de la tabla de agregación y oculta la tabla
6. Actualiza las expresiones de las medidas para que hagan referencia a la tabla de detalle
7. Configura la propiedad **Alternate Of** en las columnas base numéricas

<br></br>

> [!NOTE]
> El script identifica las columnas de atributos que se deben quitar de la tabla de agregación según el tipo de datos. Se quitan las columnas con tipos de datos `String`, `DateTime`, `Boolean` o `Unknown` que no se usen como claves de relación. Revisa el resultado después de ejecutar el script para confirmar que se han conservado las columnas correctas.

<br></br>

## Script

### Implementar agregaciones definidas por el usuario para la tabla de hechos seleccionada

```csharp
// ============================================================
// Implementar agregaciones definidas por el usuario
//
// Selecciona la tabla de hechos (la tabla de agregación) en el
// Explorador TOM y luego ejecuta este script. Todos los pasos están automatizados:
//
//   1. Clona la tabla de hechos como "<FactTableName> details"
//   2. Establece las particiones de dimensiones relacionadas en modo de almacenamiento Dual
//   3. Reduce la tabla de detalle a una sola partición (AS solo admite
//      una partición DQ con Full DataView), la establece en DirectQuery,
//      oculta todas las columnas y la tabla, elimina las medidas copiadas
//   4. Crea relaciones desde la tabla de detalle a las
//      tablas de dimensiones con Rely On Referential Integrity = true
//   5. Quita las columnas de atributos de la tabla de agregación y
//      oculta la tabla
//   6. Actualiza las expresiones de las medidas para que hagan referencia a la tabla de detalle
//   7. Configura Alternate Of en las columnas base numéricas
// ============================================================

// ── Validar la selección ─────────────────────────────────────────────────────

if (Selected.Table == null)
{
    Error("Selecciona la tabla de hechos original (la tabla de agregación) en el Explorador TOM antes de ejecutar este script.");
    return;
}

var _aggTable   = Selected.Table;
var _detailName = _aggTable.Name + " details";

if (Model.Tables.Contains(_detailName))
{
    Error($"Ya existe una tabla llamada '{_detailName}'. Elimínala o cámbiale el nombre y vuelve a ejecutar el script.");
    return;
}

if (!Model.Relationships.Any(r => r.FromTable.Name == _aggTable.Name))
{
    Error($"No se encontraron relaciones salientes en '{_aggTable.Name}'. La tabla de hechos debe tener relaciones con las tablas de dimensiones antes de ejecutar este script.");
    return;
}

// ── Paso 1: Clonar la tabla de hechos para crear la tabla de detalle ─────────

var _detailTable = _aggTable.Clone(_detailName);

// ── Paso 2: Establecer todas las particiones de dimensiones relacionadas en Dual ─

var _outboundRels = Model.Relationships
    .Where(r => r.FromTable.Name == _aggTable.Name)
    .ToList();

var _dimTables = _outboundRels
    .Select(r => r.ToTable)
    .Distinct()
    .ToList();

foreach (var _dim in _dimTables)
    foreach (var _p in _dim.Partitions)
        _p.Mode = ModeType.Dual;

// ── Paso 3: Configurar la tabla de detalle ───────────────────────────────────
// AS solo admite una partición DirectQuery con Full DataView.
// Conserva la primera partición y elimina el resto; después, configúrala como DirectQuery.

var _allPartitions     = _detailTable.Partitions.ToList();
var _keptPartition     = _allPartitions[0];
var _removedPartitions = _allPartitions.Skip(1).ToList();

foreach (var _p in _removedPartitions)
    _p.Delete();

_keptPartition.Mode = ModeType.DirectQuery;

foreach (var _col in _detailTable.Columns)
{
    _col.IsHidden         = true;
    _col.IsAvailableInMDX = false;
}

_detailTable.IsHidden = true;

// Elimina cualquier medida que se haya copiado durante la clonación:
// las medidas pertenecen a la tabla de agregación, no a la tabla de detalle.
foreach (var _m in _detailTable.Measures.ToList())
    _m.Delete();

// ── Paso 4: Crear relaciones desde la tabla de detalle a las tablas de dimensiones ─

foreach (var _rel in _outboundRels)
{
    var _fromColName = _rel.FromColumn.Name;
    if (!_detailTable.Columns.Contains(_fromColName)) continue;

    var _newRel = Model.AddRelationship();
    _newRel.FromColumn = _detailTable.Columns[_fromColName];
    _newRel.ToColumn   = _rel.ToColumn;
    _newRel.RelyOnReferentialIntegrity = true;
}

// ── Paso 5: Quitar las columnas de atributos de la tabla de agregación ───────
// Conservar: columnas clave (claves externas usadas en las relaciones)
//            columnas numéricas (se asignarán como Alternate Of a columnas base)
// Quitar:    columnas de atributos de tipo string, datetime, boolean y otras no numéricas

var _keyCols = new HashSet<string>(
    _outboundRels.Select(r => r.FromColumn.Name));

var _typesToRemove = new[] {
    DataType.String, DataType.DateTime, DataType.Boolean, DataType.Unknown };

var _colsToRemove = _aggTable.Columns
    .Where(c => !_keyCols.Contains(c.Name)
             && _typesToRemove.Contains(c.DataType))
    .ToList();

foreach (var _col in _colsToRemove)
    _col.Delete();

// Ocultar columnas clave — columnas estructurales, no pensadas para los consumidores de informes
foreach (var _col in _aggTable.Columns.Where(c => _keyCols.Contains(c.Name)).ToList())
{
    _col.IsHidden         = true;
    _col.IsAvailableInMDX = false;
}

// Ocultar la propia tabla de agregación
_aggTable.IsHidden = true;

// ── Paso 6: Actualizar las expresiones de las medidas para que hagan referencia a la tabla de detalle ─

var _oldRef = "'" + _aggTable.Name + "'[";
var _newRef = "'" + _detailName    + "'[";

foreach (var _measure in _aggTable.Measures)
    _measure.Expression = _measure.Expression.Replace(_oldRef, _newRef);

// ── Paso 7: Configurar Alternate Of en columnas base numéricas ───────────────

var _numericTypes = new[] { DataType.Double, DataType.Int64, DataType.Decimal };

var _numericCols = _aggTable.Columns
    .Where(c => _numericTypes.Contains(c.DataType) && !_keyCols.Contains(c.Name))
    .ToList();

var _alternateOfWarnings = new List<string>();

foreach (var _col in _numericCols)
{
    _col.IsHidden         = true;
    _col.IsAvailableInMDX = false;

    if (!_detailTable.Columns.Contains(_col.Name))
    {
        _alternateOfWarnings.Add(_col.Name + " (no se encontró una columna coincidente en la tabla de detalle)");
        continue;
    }

    try
    {
        _col.AddAlternateOf(_detailTable.Columns[_col.Name], SummarizationType.Sum);
    }
    catch
    {
        _alternateOfWarnings.Add(_col.Name + " (configura Alternate Of manualmente en el panel de Propiedades)");
    }
}

// ── Finalizado ───────────────────────────────────────────────────────────────

var _summary =
    $"Agregaciones definidas por el usuario configuradas para '{_aggTable.Name}'.\n\n" +
    $"  Tabla de detalle:            {_detailName}\n" +
    $"  Partición conservada:        {_keptPartition.Name}\n" +
    $"  Particiones eliminadas:      {_removedPartitions.Count}\n" +
    $"  Dimensiones en Dual:         {string.Join(", ", _dimTables.Select(t => t.Name))}\n" +
    $"  Columnas de atributos eliminadas: {_colsToRemove.Count}\n" +
    $"  Columnas base numéricas:     {_numericCols.Count}";

if (_removedPartitions.Count > 0)
    _summary += $"\n\n⚠ IMPORTANTE: Revisa la expresión de partición en '{_keptPartition.Name}'.\n" +
                "  La tabla de detalle debe cubrir todos los datos: elimina cualquier filtro de fecha/rango\n" +
                "  que se utilizó para la actualización incremental en la tabla original.";

if (_alternateOfWarnings.Any())
    _summary += "\n\nNo se pudo establecer Alternate Of automáticamente en las siguientes columnas.\n" +
                "Configúralas manualmente en el panel de Propiedades:\n  - " +
                string.Join("\n  - ", _alternateOfWarnings);

_summary += "\n\nDespués de guardar, ejecuta Process Recalc en el modelo para recalcular\n" +
            "las nuevas relaciones. No es necesario volver a importar datos.\n\n" +
            "Revisa el modelo con cuidado antes de guardar.";

Info(_summary);
```

### Explicación

El script comienza validando la selección y comprobando que en el modelo no exista ya una tabla llamada `<FactTableName> details`.

**Paso 1** clona la tabla de hechos seleccionada mediante el método integrado `.Clone()`, creando una copia exacta llamada `<FactTableName> details`. Esto copia todas las columnas, particiones y medidas del original.

**Paso 2** identifica las tablas de dimensiones siguiendo las relaciones salientes desde la tabla de agregación y, después, establece el modo de almacenamiento `Dual` para cada partición de cada tabla de dimensiones.

**Paso 3** configura la tabla de detalle. Analysis Services solo admite una partición de DirectQuery cuando se usa Full DataView, por lo que se eliminan todas las particiones excepto la primera. La partición restante se establece en `DirectQuery`. Se ocultan todas las columnas y se marcan como no disponibles en MDX. Se eliminan todas las medidas copiadas durante la clonación. Si se han eliminado particiones, el cuadro de diálogo de resumen advierte de que debe revisarse la expresión de la partición conservada — hay que eliminar cualquier filtro de fecha o de rango heredado de una configuración de actualización incremental para que la tabla de detalle abarque todos los datos.

**Paso 4** crea relaciones desde la tabla de detalle hacia cada tabla de dimensiones, replicando las relaciones existentes en la tabla de agregación. En cada relación nueva, `Rely On Referential Integrity` se establece en `true`, lo que indica al motor que use INNER JOIN en lugar de OUTER JOIN en el SQL de DirectQuery.

**Paso 5** quita las columnas de atributos (string, datetime, boolean) de la tabla de agregación, conservando solo las columnas clave y las columnas numéricas. Las columnas clave se ocultan. La propia tabla de agregación también se oculta.

**Paso 6** actualiza las expresiones de las medidas para que hagan referencia a la tabla de detalle en lugar de a la tabla de agregación. Esto es necesario para que el mecanismo de reserva de DirectQuery funcione correctamente.

**Paso 7** configura la propiedad `Alternate Of` en cada columna base numérica mediante `AddAlternateOf()`, que inicializa y establece el mapeo en una sola llamada. Si una columna no se puede asignar automáticamente (por ejemplo, si no existe una columna coincidente en la tabla de detalle), se añade una advertencia al cuadro de diálogo de resumen y la columna debe configurarse manualmente en el panel **Propiedades**.

> [!NOTE]
> Después de guardar el modelo, ejecuta **Process Recalc** sobre el modelo. Las tablas conservan su estado procesado: solo las nuevas relaciones quedan en estado `CalculationNeeded` y deben recalcularse. No es necesario volver a importar los datos.
