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

## Objetivo del script

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
// Implement User-Defined Aggregations
//
// Select the fact table (the aggregation table) in the TOM
// Explorer, then run this script. All steps are automated:
//
//   1. Clones the fact table as "<FactTableName> details"
//   2. Sets related dimension partitions to Dual storage mode
//   3. Reduces the detail table to a single partition (AS only supports
//      one DQ partition with Full DataView), sets it to DirectQuery,
//      hides all columns and the table, deletes copied measures
//   4. Creates relationships from the detail table to dimension
//      tables with Rely On Referential Integrity = true
//   5. Removes attribute columns from the aggregation table,
//      hides the table
//   6. Updates measure expressions to reference the detail table
//   7. Configures Alternate Of on numeric base columns
// ============================================================

// ── Validate selection ────────────────────────────────────────────────────────

if (Selected.Table == null)
{
    Error("Select the original fact table (the aggregation table) in the TOM Explorer before running this script.");
    return;
}

var _aggTable   = Selected.Table;
var _detailName = _aggTable.Name + " details";

if (Model.Tables.Contains(_detailName))
{
    Error($"A table named '{_detailName}' already exists. Remove or rename it, then re-run the script.");
    return;
}

if (!Model.Relationships.Any(r => r.FromTable.Name == _aggTable.Name))
{
    Error($"No outbound relationships found on '{_aggTable.Name}'. The fact table must have relationships to dimension tables before running this script.");
    return;
}

// ── Step 1: Clone the fact table to create the detail table ──────────────────

var _detailTable = _aggTable.Clone(_detailName);

// ── Step 2: Set all related dimension partitions to Dual ─────────────────────

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

// ── Step 3: Configure the detail table ───────────────────────────────────────
// AS only supports one DirectQuery partition with Full DataView.
// Keep the first partition and delete the rest, then set it to DirectQuery.

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

// Delete any measures that were copied during cloning —
// measures belong on the aggregation table, not the detail table.
foreach (var _m in _detailTable.Measures.ToList())
    _m.Delete();

// ── Step 4: Create relationships from detail table to dimension tables ─────────

foreach (var _rel in _outboundRels)
{
    var _fromColName = _rel.FromColumn.Name;
    if (!_detailTable.Columns.Contains(_fromColName)) continue;

    var _newRel = Model.AddRelationship();
    _newRel.FromColumn = _detailTable.Columns[_fromColName];
    _newRel.ToColumn   = _rel.ToColumn;
    _newRel.RelyOnReferentialIntegrity = true;
}

// ── Step 5: Remove attribute columns from the aggregation table ───────────────
// Keep:   key columns (foreign keys used in relationships)
//         numeric columns (will be mapped as Alternate Of base columns)
// Remove: string, datetime, boolean, and other non-numeric attribute columns

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

// Hide key columns — structural columns, not for report consumers
foreach (var _col in _aggTable.Columns.Where(c => _keyCols.Contains(c.Name)).ToList())
{
    _col.IsHidden         = true;
    _col.IsAvailableInMDX = false;
}

// Hide the aggregation table itself
_aggTable.IsHidden = true;

// ── Step 6: Update measure expressions to reference the detail table ──────────

var _oldRef = "'" + _aggTable.Name + "'[";
var _newRef = "'" + _detailName    + "'[";

foreach (var _measure in _aggTable.Measures)
    _measure.Expression = _measure.Expression.Replace(_oldRef, _newRef);

// ── Step 7: Configure Alternate Of on numeric base columns ───────────────────

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
        _alternateOfWarnings.Add(_col.Name + " (no matching column found in detail table)");
        continue;
    }

    try
    {
        _col.AddAlternateOf(_detailTable.Columns[_col.Name], SummarizationType.Sum);
    }
    catch
    {
        _alternateOfWarnings.Add(_col.Name + " (configure Alternate Of manually in the Properties panel)");
    }
}

// ── Done ─────────────────────────────────────────────────────────────────────

var _summary =
    $"User-defined aggregations configured for '{_aggTable.Name}'.\n\n" +
    $"  Detail table:                {_detailName}\n" +
    $"  Partition retained:          {_keptPartition.Name}\n" +
    $"  Partitions removed:          {_removedPartitions.Count}\n" +
    $"  Dimensions set to Dual:      {string.Join(", ", _dimTables.Select(t => t.Name))}\n" +
    $"  Attribute columns removed:   {_colsToRemove.Count}\n" +
    $"  Numeric base columns:        {_numericCols.Count}";

if (_removedPartitions.Count > 0)
    _summary += $"\n\n⚠ IMPORTANT: Review the partition expression on '{_keptPartition.Name}'.\n" +
                "  The detail table must cover all data — remove any date/range filtering\n" +
                "  that was used for incremental refresh on the original table.";

if (_alternateOfWarnings.Any())
    _summary += "\n\nThe following columns could not have Alternate Of set automatically.\n" +
                "Configure them manually in the Properties panel:\n  - " +
                string.Join("\n  - ", _alternateOfWarnings);

_summary += "\n\nAfter saving, run Process Recalc on the model to recalculate\n" +
            "the new relationships. No data reimport is needed.\n\n" +
            "Review the model carefully before saving.";

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
