---
uid: dax-editor
title: Editor de DAX
author: Daniel Otykier
updated: 2026-09-14
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

# Editor de DAX

El **Editor de DAX** es la pieza central de Tabular Editor 3.

Viene en tres _sabores_ diferentes:

- **Editor de expresiones** Se utiliza para realizar cambios rápidos en expresiones DAX individuales en los objetos del Explorador TOM.
- **Consulta DAX** (funcionalidad conectada): Se utiliza para escribir consultas DAX y recuperar datos de la instancia conectada de Analysis Services/Power BI.
- **Script DAX:** Se utiliza para ver y editar expresiones DAX y propiedades básicas en varios objetos dentro de un único documento.

Las tres modalidades admiten las mismas operaciones, como [atajos de teclado](xref:shortcuts3#dax-code), resaltado de sintaxis, Code Assist, etc.

## Funciones de Code Assist

El principal impulsor de la productividad en el Editor de DAX de Tabular Editor 3 son las funciones **Información de parámetros** y **Autocompletar**. En conjunto, se conocen como funciones de **Code Assist** (otros proveedores usan el término "IntelliSense").

**Información de parámetros** ofrece detalles sobre la función DAX y su parámetro en la posición del cursor. La información se muestra en un globo de ayuda sobre el cursor. Pulsa [Esc] para cerrar el globo de ayuda y [Ctrl+Shift+Space] para mostrarlo.

**Autocompletar** ofrece sugerencias en función del contexto mientras escribes, en una lista desplegable. Puedes usar el teclado para desplazarte por los elementos de la lista desplegable, y al pulsar [Enter] o [Tab] se insertará el elemento seleccionado en tu código. Puedes pulsar [Esc] para cerrar la lista desplegable y [Ctrl+Space] para abrirla.

Estas funciones también se pueden activar desde el menú contextual del editor.

Los calltips de DAX se actualizan al alternar entre las opciones de sintaxis con las flechas Arriba/Abajo.

![Code Assist de Dax](~/content/assets/images/dax-code-assist.png)

La mayoría de los aspectos de Code Assist se pueden configurar en [**Herramientas > Preferencias > Editores de texto > Editor de DAX > Code Assist**](xref:preferences#dax-editor--code-assist).

## Peek Definition

Con el cursor sobre una referencia a un objeto, como una variable o una referencia a una medida, pulsa [Alt+F12] para mostrar un editor en línea con la definición de ese objeto, debajo del cursor. Esto resulta útil cuando desea ver el código DAX de un objeto al que se hace referencia sin salir de la posición actual del documento.

![Ver la definición](~/content/assets/images/peek-definition.png)

Usa la tecla Esc para volver a cerrar el panel de Ver la definición.

## Ir a definición

En lugar de usar Ver la definición, también podemos saltar directamente a la ubicación donde está definido el objeto referenciado. Para ello, pulsa [F12]. Si el objeto referenciado no está definido en el documento actual, esta operación saltará a ese objeto en el Explorador TOM. Si lo necesita, puede volver atrás con [Alt+Flecha izquierda].

## Definir medida

En los scripts DAX y las consultas DAX, a veces es útil incluir la definición de una medida a la que se hace referencia en otra parte del código. La función **Definir medida** permite hacerlo cuando el cursor está sobre una referencia a una medida. También puede elegir la opción **Definir medida con dependencias** si desea incluir también todas las referencias posteriores a medidas.

![Definir medida con dependencias](~/content/assets/images/define-measure-with-deps.png)

## Medida en línea

Si desea traer la definición de una medida al documento actual, la función **Medida en línea** permite hacerlo. Right-click a measure reference in the DAX editor and choose **Inline Measure**.

A measure reference implicitly turns the current row into a filter before the measure's expression is evaluated. Pasting the expression in as-is would therefore change the result, so when the reference sits inside a row context, for example as the second argument of an iterator such as [`SUMX`](https://dax.guide/sumx) or [`FILTER`](https://dax.guide/filter), Tabular Editor wraps the inlined expression in [`CALCULATE`](https://dax.guide/calculate) to preserve that behavior:

```dax
// Before using inline measure on the [Margin] measure
SUMX ( 'Sales', [Margin] )

// After using inline measure on the [Margin] measure
SUMX ( 'Sales', CALCULATE ( 'Sales'[Amount] - 'Sales'[Cost] ) )
```

The wrap is only added where it can make a difference. The expression is inserted unwrapped when:

- the reference is **not inside a row context**, including when it already sits inside a `CALCULATE( ... )` of its own
- the measure's expression **reads nothing from the model** (a constant, a reference to another measure or a call to a function such as `TODAY()`). A reference to a table, a column, a calendar or a [user-defined function](xref:udfs) does count as reading from the model, and does get the wrap
- the expression **already performs the transition itself**, through a `CALCULATE( ... )` or `CALCULATETABLE( ... )` with no filter arguments. With a filter argument the wrap is still added, because filter arguments are evaluated before the transition

If the measure's expression cannot be analyzed, the wrap is added, on the principle that a wrap that was not needed is harmless where a missing one is not.

## Dar formato a DAX

El Editor de DAX de Tabular Editor 3 formatea automáticamente su código mientras escribe; es decir, corrige las mayúsculas y minúsculas de las funciones y las referencias a objetos, añade la sangría adecuada y los espacios entre paréntesis, etc. Todo esto se puede configurar en [**Herramientas > Preferencias > Editores de texto > Editor de DAX > Formato automático**](xref:preferences#dax-editor--auto-formatting).

Sin embargo, a veces es necesario formatear todo el documento. Puedes hacerlo pulsando [F6] o [Shift+F6] si prefieres saltos de línea más frecuentes. Para las Consultas DAX, también puedes usar [Alt+F6] para reformatear el código y hacer que las comas se coloquen siempre al principio de cada línea, lo cual es útil al depurar.

## Refactorización

Si quieres cambiar el nombre de una variable o de una columna de extensión, puedes usar la opción **Refactor** (Ctrl+R) con el cursor situado sobre la referencia de la variable o de la columna de extensión. Esto seleccionará todas las apariciones de ese objeto, lo que te permite cambiarle el nombre en todas partes de una sola vez.

## Atajos de teclado configurables

El Editor de DAX y los editores de código en general son muy configurables y admiten muchos comandos adicionales para editar código de forma rápida y productiva. Puedes ver todos estos comandos, así como modificar y asignar atajos de teclado en **Herramientas > Preferencias > Tabular Editor > Teclado**.
