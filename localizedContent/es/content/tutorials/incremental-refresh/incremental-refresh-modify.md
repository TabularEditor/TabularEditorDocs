---
uid: incremental-refresh-modify
title: Modificar una política de actualización existente
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

# Modificar la actualización incremental

![Resumen Visual de la actualización incremental](~/content/assets/images/tutorials/incremental-refresh-modify-a-refresh-policy.png)

---

**La actualización incremental se modifica ajustando las propiedades de la política de actualización.** Según lo que desee cambiar, ajustará una propiedad distinta. Encontrarás una descripción completa de estas propiedades [aquí](xref:incremental-refresh-about#overview-of-all-properties).

> [!IMPORTANT]
> La configuración de la actualización incremental con Tabular Editor 3 solo está disponible para Datasets alojados en el servicio Power BI Datasets. En Analysis Services se requiere la [creación de particiones](https://learn.microsoft.com/en-us/analysis-services/tabular-models/partitions-ssas-tabular?view=asallproducts-allversions) personalizada.

---

## Cambiar la actualización incremental

A continuación se muestra una descripción general de cómo modificar una política de actualización existente:

1. **Conectar:** Conéctese al modelo.

2. **Seleccionar la tabla:** Seleccione la tabla que ya está configurada para la actualización incremental.

3. **Busque las propiedades de "política de actualización":** En la ventana _Propiedades_, vaya a la sección _política de actualización_.

    <img src="~/content/assets/images/tutorials/Incremental-refresh-properties.png" class="noscale" alt="Properties of Incremental Refresh" style="width:704px !important"/>

4. **Cambiar la propiedad:** Cambie la **Propiedad** indicada en las secciones siguientes, según lo que desee cambiar. Para ver un resumen de todas las propiedades de la política de actualización y lo que hacen, consulta [aquí](xref:incremental-refresh-about#overview-of-all-properties).

5. **Aplicar cambios:** Implemente los cambios en el modelo.

6. **Aplicar política de actualización:** Haga clic con el botón derecho en la tabla y seleccione _Aplicar política de actualización_.

    <img src="~/content/assets/images/tutorials/incremental-refresh-apply-refresh-policy.png" class="noscale" alt="Apply Refresh Policy" style="width:450px !important"/>

7. **Actualizar todas las particiones:** Haga clic mientras mantiene pulsada la tecla Mayús para seleccionar todas las particiones. Haz clic con el botón derecho y selecciona _Actualizar > Actualización completa (partición)_. Puedes hacer clic con el botón derecho en la tabla y seleccionar _'Vista previa de datos'_ para ver el resultado.

    <img src="~/content/assets/images/tutorials/incremental-refresh-refresh-all-partitions.png" class="noscale" alt="Refresh All Partitions" style="width:450px !important"/>

---

A continuación se muestra una descripción general de los cambios habituales que se pueden hacer en una política de actualización existente:

### Ampliar o reducir la ventana de datos archivados

**Propósito:** Agregar o reducir la cantidad de datos en el modelo.

**Propiedad:** <span style="color:#BC4A47">_RollingWindowPeriods_</span>. Aumenta el valor para ampliar la ventana (más datos); disminúyelo para reducirla (menos datos).

**Nota:** También puedes cambiar <span style="color:#BC4A47">_RollingWindowGranularity_</span> para hacer una selección más granular; es decir, de 3 años a 36 meses.

<br></br>

---

<br></br>

### Ampliar o reducir la ventana de datos actualizados

**Propósito:** Agregar o reducir la cantidad de datos que se actualizan en una operación de actualización programada.

**Propiedad:** <span style="color:#455C86">_IncrementalWindowPeriods_</span>. Aumenta el valor para ampliar la ventana (más datos); disminúyelo para reducirla (menos datos).

**Nota:** También puedes cambiar <span style="color:#455C86">_IncrementalWindowGranularity_</span> para hacer una selección más granular; es decir, de 3 años a 36 meses.

<br></br>

---

<br></br>

### Actualizar solo períodos completos

**Propósito:** Excluir períodos parciales (incompletos) de la <span style="color:#BC4A47">ventana móvil</span>

**Propiedad:** <span style="color:#455C86">_IncrementalWindowPeriodsOffset_</span>. Establece el valor en `-1` para desplazar el período en 1 y excluir el período actual.

**Nota:** Puedes desplazar aún más esta ventana para actualizar, p. ej., solo los períodos anteriores al período completo más reciente.

<br></br>

---

<br></br>

### Cambiar el modo de actualización incremental

**Propósito:** Cambiar las tablas de `Import` a `Hybrid`, o viceversa.

**Propiedad:** _Mode_

**Nota:** Sigue el proceso que se indica a continuación para cambiar el modo de actualización incremental:

1. Cambia _Mode_ al valor deseado: `Import` o `Hybrid`
2. Haz clic con el botón derecho en la tabla y selecciona _Aplicar política de actualización_
3. Implementa los cambios en el modelo
4. Mantén presionada la tecla Mayús y haz clic para seleccionar todas las particiones. Haz clic con el botón derecho y selecciona _Actualizar > Actualización completa (partición)_. Puedes hacer clic con el botón derecho en la tabla y seleccionar _'Vista previa de datos'_ para ver el resultado.

> [!NOTE]
> Se recomienda comprobar que la ventana móvil esté configurada correctamente para el _Mode_ seleccionado. Al cambiar del modo `Import` al modo `Hybrid`, la última partición de intervalo de la directiva pasará a ser la partición de DirectQuery. Puede que te convenga optar por una ventana más granular para limitar la cantidad de datos consultados con DirectQuery.

<br></br>

---

<br></br>

### Configura "Detectar cambios en los datos"

**Propósito:** Configurar que los datos archivados se actualicen si cambia el valor de una columna de fecha (p. ej., _LastUpdate_).

**Propiedad:** _PollingExpression_. Agrega una expresión M válida que devuelva el valor máximo de fecha de una columna. Se actualizarán todos los registros que contengan esa fecha, independientemente de su partición.

**Nota:** Sigue el proceso que se indica a continuación para configurar "Detectar cambios en los datos":

1. Con la tabla seleccionada, en la ventana del _Editor de expresiones_, selecciona _Expresión de sondeo_ en el menú desplegable de la esquina superior izquierda
2. Copia la siguiente expresión M y sustituye _LastUpdate_ por el nombre de columna que quieras.

```M
// Recupera el valor máximo de la columna [LastUpdate]
// Sustituye LastUpdate por el nombre de tu propia columna
// Los datos se actualizarán para cualquier registro donde el valor de esta columna
//    sea igual al valor máximo de la columna en toda la tabla
let
    #"maxLastUpdate" =
        List.Max(
            // Sustituye lo siguiente por el nombre de tu columna y de tu tabla
            Orders[LastUpdate] 
        ),

    accountForNu11 =
        if #"maxLastUpdate" = null
        then #datetime(1901, 01, 01, 00, 00, 00)
        else #"maxLastUpdate"
in
    accountForNu11
```

3. Haz clic con el botón derecho en la tabla y selecciona _Aplicar política de actualización_
4. Implementa los cambios en el modelo
5. Mayús + clic para seleccionar todas las particiones. Haz clic con el botón derecho y selecciona _Actualizar > Actualización completa (partición)_. Puedes hacer clic con el botón derecho en la tabla y seleccionar _'Vista previa de datos'_ para ver el resultado.

> [!WARNING]
> Se actualizará cualquier registro cuyo valor sea igual al valor máximo de la columna. No necesariamente se actualiza de forma explícita porque el valor haya cambiado o porque sea igual a la fecha de actualización.

<br></br>

---

<br></br>

### Aplicación de políticas de actualización con `EffectiveDate`

Si quieres generar particiones sustituyendo la fecha actual (para generar distintos rangos de ventana deslizante), puedes usar un pequeño script en Tabular Editor para aplicar la política de actualización con el parámetro [EffectiveDate](https://docs.microsoft.com/en-us/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions#optional-parameters).

Con la tabla de actualización incremental seleccionada, ejecuta el siguiente script en el panel _'Nuevo C# Script'_ de Tabular Editor, en lugar de aplicar la política de actualización haciendo clic con el botón derecho en la tabla.

```csharp
// Todo: reemplaza por tu fecha efectiva
var effectiveDate = new DateTime(2020, 1, 1);  
Selected.Table.ApplyRefreshPolicy(effectiveDate);
```

<br></br>

<img src="~/content/assets/images/effective-date-te3.png" class="noscale" alt="Effective Date" style="width:700px !important"/>

<br></br>

---

<br></br>

### Deshabilitar la actualización incremental

**Propósito:** Deshabilitar una política de actualización porque ya no es necesaria o el caso de uso ya no aplica.

**Propiedad:** _EnableRefreshPolicy_

**Nota:** Para deshabilitar la actualización incremental, sigue estos pasos:

1. **Copia la _Expresión de origen_:** Con la tabla seleccionada, en la ventana _Editor de expresiones_, selecciona _Expresión de origen_ en el menú desplegable de la esquina superior izquierda. Copia la _Expresión de origen_ en una ventana aparte de un editor de texto.
2. **Deshabilita la política de actualización:** Cambia _EnableRefreshPolicy_ a `False`
3. **Elimina todas las particiones de Policy Range:** Selecciona y elimina todas las particiones de Policy Range
4. **Crea una nueva partición M:** Haz clic con el botón derecho en la tabla y selecciona _Crear > Nueva partición_. Establece la propiedad _kind_ de la partición en `M`.
5. **Pega la _Expresión de origen_:** Copia la _Expresión de origen_ del **Paso 6** en el _Editor de expresiones_ como _Expresión M_ al seleccionar la nueva partición.
6. **Aplicar cambios:** Implementa los cambios del modelo.
7. **Actualizar la tabla:** Selecciona la tabla y haz clic con el botón derecho. Selecciona _Actualizar > Actualización completa (tabla)_. Puedes hacer clic con el botón derecho en la tabla y seleccionar _'Vista previa de datos'_ para ver el resultado.
