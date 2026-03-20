---
uid: incremental-refresh-schema
title: Agregar o quitar columnas en una tabla con actualización incremental
author: Kurt Buhler
updated: 2023-01-09
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Modificar los esquemas de tablas con actualización incremental

![Resumen visual del modo Workspace de actualización incremental](~/content/assets/images/tutorials/incremental-refresh-update-schema-header.png)

---

> [!IMPORTANT]
> La configuración de la actualización incremental con Tabular Editor 3 se limita a los Datasets hospedados en el servicio Power BI Datasets. Para Analysis Services, se requiere un [particionamiento](https://learn.microsoft.com/en-us/analysis-services/tabular-models/partitions-ssas-tabular?view=asallproducts-allversions) personalizado de particiones.

---

**Al agregar o quitar columnas de una tabla configurada con actualización incremental, debes actualizar el esquema de la tabla.** Por lo general, esto sigue el mismo procedimiento que para actualizar los esquemas de tablas de una sola partición. Tabular Editor puede detectar y actualizar el esquema automáticamente:

1. **Detectar cambios de esquema:** Haz clic con el botón derecho en la tabla y selecciona _'Actualizar esquema de tabla...'_.

  <img src="~/content/assets/images/tutorials/incremental-refresh-update-table-schema.png" class="noscale" alt="Update Table Schema" style="width:450px !important"/>

2. **Aplicar cambios de esquema detectados:** En el cuadro de diálogo _'Aplicar cambios de esquema'_, confirma los cambios de esquema que quieras aplicar.
3. **Aplicar cambios:** Implementa los cambios del modelo.
4. **Aplicar política de actualización:** Haz clic con el botón derecho en la tabla y selecciona _Aplicar política de actualización_.

  <img src="~/content/assets/images/tutorials/incremental-refresh-apply-refresh-policy.png" class="noscale" alt="Apply Refresh Policy" style="width:450px !important"/>

5. **Actualizar todas las particiones:** Haz Mayús + clic para seleccionar todas las particiones. Haz clic con el botón derecho y selecciona _Actualizar > Actualización completa (partición)_. Puedes hacer clic con el botón derecho en la tabla y seleccionar _'Vista previa de datos'_ para ver el resultado.

  <img src="~/content/assets/images/tutorials/incremental-refresh-refresh-all-partitions.png" class="noscale" alt="Refresh All Partitions" style="width:450px !important"/>

---

### Consideraciones sobre la actualización del esquema con actualización incremental

- En la actualización incremental, la principal consideración es que **todas las particiones deben actualizarse**.<br />Para ello, **selecciona y haz clic con el botón derecho en todas las particiones**. Selecciona _Actualizar > Actualización completa (partición)___.

- La segunda consideración es que **puede que sea necesario actualizar las _Source Expression_ y _Polling Expression_ para reflejar cambios en el esquema**. No actualizar estas expresiones M puede provocar errores de actualización. Ejemplos:
  - El paso `Table.TransformColumnTypes` hace referencia a una columna que se eliminará en el esquema actualizado.
  - El paso `Table.SelectColumns` enumera las columnas que se conservarán; la nueva columna no se añade a esta lista.

<div class="WARNING">
  <h5>REVISA LAS EXPRESIONES M ANTES DE ACTUALIZAR EL ESQUEMA DE LA TABLA</h5>
  <p>Si los cambios en el esquema proceden del Data source, puede que aun así tengas que realizar cambios en tu <b><em>Source Expression</em></b> o <b><em>Polling Expression</em></b> de Power Query. Se recomienda que revises estas expresiones detenidamente antes de usar <em>'Actualizar esquema de tabla...'</em></p>
</div>

---

### Eliminar columnas

Según dónde se elimine la columna, puede que debas seguir un protocolo ligeramente distinto:

# [Data source compatible](#tab/removingfromsource)

Para las columnas eliminadas en el **Data source** (es decir, eliminadas de la vista a la que accede Power BI), sigue los pasos siguientes:

1. **Detectar cambios de esquema:** Haz clic con el botón derecho en la tabla y selecciona _'Actualizar esquema de tabla...'_.
2. **Aplicar cambios de esquema detectados:** En el cuadro de diálogo _'Aplicar cambios de esquema'_, confirma los cambios de esquema deseados.
3. **Aplicar cambios:** Implementa los cambios del modelo.
4. **Aplicar política de actualización:** Haz clic con el botón derecho en la tabla y selecciona _Aplicar política de actualización_.
5. **Actualizar todas las particiones:** Haz Mayús+clic para seleccionar todas las particiones. Haz clic con el botón derecho y selecciona _Actualizar > Actualización completa (partición)_. Puedes hacer clic con el botón derecho en la tabla y seleccionar _'Vista previa de datos'_ para ver el resultado.

# [Power Query](#tab/removingfrompq)

Para columnas eliminadas a través de **Power Query** (es decir, usando `Table.RemoveColumns`), sigue los pasos siguientes:

1. **Detectar cambios de esquema:** Haz clic con el botón derecho en la tabla y selecciona _'Actualizar esquema de tabla...'_.
2. **Aplicar cambios de esquema detectados:** En el cuadro de diálogo _'Aplicar cambios de esquema'_, confirma los cambios de esquema deseados.
3. **Aplicar cambios:** Implementa los cambios del modelo.
4. **Aplicar política de actualización:** Haz clic con el botón derecho en la tabla y selecciona _Aplicar política de actualización_.
5. **Actualizar todas las particiones:** Mantén presionada la tecla Mayús y haz clic para seleccionar todas las particiones. Haz clic con el botón derecho y selecciona _Actualizar > Actualización completa (partición)_. Puedes hacer clic con el botón derecho en la tabla y seleccionar _'Vista previa de datos'_ para ver el resultado.

# [Data source no compatible](#tab/removingfromunsupportedsource)

Si **no puedes actualizar automáticamente el esquema de la tabla** con _'Actualizar el esquema de la tabla...'_ desde el menú contextual de la tabla, sigue los pasos a continuación. Estos pasos son los mismos tanto si las columnas se quitaron en el Data source como en Power Query.

1. **Selecciona la expresión de origen:** Con la tabla seleccionada, en la ventana del _Editor de expresiones_, selecciona _Source Expression_ en la lista desplegable de la esquina superior izquierda.
2. **Actualiza las expresiones de Power Query:** Comprueba y quita cualquier referencia con nombre a la columna eliminada, si corresponde. Si la columna se está excluyendo mediante Power Query, puedes hacer los cambios correspondientes aquí.
3. **Actualiza manualmente el esquema:** Elimina el objeto de columna de datos de la tabla.
4. **Aplicar cambios:** Implementa los cambios del modelo.
5. **Aplicar política de actualización:** Haz clic con el botón derecho en la tabla y selecciona _Aplicar política de actualización_.
6. **Actualizar todas las particiones:** Mantén presionada la tecla Mayús y haz clic para seleccionar todas las particiones. Haz clic con el botón derecho y selecciona _Actualizar > Actualización completa (partición)_. Puedes hacer clic con el botón derecho en la tabla y seleccionar _'Vista previa de datos'_ para ver el resultado.

***

<div class="NOTE">
  <h5>LOS OBJETOS DE COLUMNA ELIMINADOS AÚN PUEDEN CONSULTARSE</h5>
  <p>Eliminar objetos de columna del modelo no impide que se sigan consultando si aún existen en el origen y no se eliminan de la consulta nativa o de <b><em>Source Expression</em></b>. Las columnas consultadas pero no usadas pueden afectar negativamente al tiempo de actualización y al uso de recursos. Se recomienda eliminar las columnas tanto de los metadatos como de los Data source (p. ej., vistas) o de <b><em>Source Expression</em></b>.</p>
</div>

---

### Agregar columnas

Según dónde se agregue la columna, puede que tengas que seguir un protocolo ligeramente diferente:

# [Data source compatible](#tab/addingfromsource)

Para las columnas agregadas en el **Data source** (es decir, añadidas a la vista a la que accede Power BI), sigue estos pasos:

1. **Detectar cambios de esquema:** Haz clic con el botón derecho en la tabla y selecciona _'Actualizar el esquema de la tabla...'_.
2. **Aplicar los cambios de esquema detectados:** En el cuadro de diálogo _'Aplicar cambios de esquema'_, confirma los cambios de esquema deseados.
3. **Aplicar cambios:** Implementa los cambios del modelo.
4. **Aplicar política de actualización:** Haz clic con el botón derecho en la tabla y selecciona _Aplicar política de actualización_.
5. **Actualizar todas las particiones:** Mantén pulsada la tecla Shift y haz clic para seleccionar todas las particiones. Haz clic con el botón derecho y selecciona _Actualizar > Actualización completa (partición)_. Puedes hacer clic con el botón derecho en la tabla y seleccionar _'Vista previa de datos'_ para ver el resultado.

# [Power Query](#tab/addingfrompq)

Para las columnas eliminadas mediante **Power Query** (es decir, usando `Table.AddColumns`), sigue estos pasos:

1. **Detectar cambios de esquema:** Haz clic con el botón derecho en la tabla y selecciona _'Actualizar esquema de tabla...'_.
2. **Aplicar los cambios de esquema detectados:** En el cuadro de diálogo _'Aplicar cambios de esquema'_, confirma los cambios de esquema deseados.
3. **Aplicar cambios:** Implementa los cambios del modelo.
4. **Aplicar política de actualización:** Haz clic con el botón derecho en la tabla y selecciona _Aplicar política de actualización_.
5. **Actualizar todas las particiones:** Mantén pulsada la tecla Shift y haz clic para seleccionar todas las particiones. Haz clic con el botón derecho y selecciona _Actualizar > Actualización completa (partición)_. Puedes hacer clic con el botón derecho en la tabla y seleccionar _'Vista previa de datos'_ para ver el resultado.

# [Data source no compatible](#tab/addingfromunsupportedsource)

Si **no puedes actualizar automáticamente el esquema de la tabla** mediante _'Actualizar esquema de tabla...'_ desde el menú contextual de la tabla, sigue estos pasos. Estos pasos son los mismos tanto para las columnas eliminadas en el Data source como en Power Query.

1. **Seleccionar la expresión de origen:** Con la tabla seleccionada, en la ventana _Editor de expresiones_, selecciona _Source Expression_ en la lista desplegable de la esquina superior izquierda.
2. **Actualizar las expresiones de Power Query:** Revisa y elimina cualquier referencia con nombre a la columna eliminada, si corresponde. Si la columna se está excluyendo mediante Power Query, puedes realizar aquí los cambios necesarios.
3. **Actualizar manualmente el esquema:** Haz clic con el botón derecho en la tabla y selecciona _Crear > Columna de datos_. Asigna un nombre adecuado a la columna.
4. **Configurar la nueva columna:** Configura la propiedad `data type` de la columna según corresponda. Configura la propiedad `Source Column` para que coincida con el origen. También se pueden configurar propiedades adicionales (p. ej., `Format String`, `SummarizeBy`, `Data Category`...) y la columna se puede agregar a la carpeta de visualización correspondiente.
5. **Aplicar cambios:** Implementa los cambios del modelo.
6. **Aplicar política de actualización:** Haz clic con el botón derecho en la tabla y selecciona _Aplicar política de actualización_.
7. **Actualizar todas las particiones:** Mantén pulsada la tecla Mayús y haz clic para seleccionar todas las particiones. Haz clic con el botón derecho y selecciona _Actualizar > Actualización completa (partición)_. Puedes hacer clic con el botón derecho en la tabla y seleccionar _'Vista previa de datos'_ para ver el resultado.

***