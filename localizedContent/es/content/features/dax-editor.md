---
uid: dax-editor
title: Editor de DAX
author: Daniel Otykier
updated: 2026-10-11
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

El **Editor de DAX** es la pieza central de Tabular Editor 3.

Está disponible en tres *versiones* diferentes:

- **Editor de expresiones** Se utiliza para realizar cambios rápidos en expresiones DAX singulares en objetos del Explorador TOM.
- **Consulta DAX** (función conectada) Se utiliza para escribir consultas DAX con el fin de recuperar datos de la instancia conectada de Analysis Services / Power BI.
- **Script DAX** Se utiliza para ver y editar expresiones DAX y propiedades básicas en múltiples objetos en un único documento.

Las tres versiones admiten las mismas operaciones en términos de [accesos directos de teclado](xref:shortcuts3#dax-code), resaltado de sintaxis, asistencia de código, etc.

## Funciones de Code Assist

Los principales elementos que favorecen la productividad en el editor DAX de Tabular Editor 3 son sus funciones **Información de parámetros** y **Autocompletar**. En conjunto, se conocen como funciones de **Code Assist** (otros proveedores utilizan el término «IntelliSense»).

**Información de parámetros** proporciona detalles sobre la función DAX y su parámetro en la posición del cursor. La información se muestra en una información sobre herramientas situada encima del cursor. Pulse [Esc] para cerrar la información sobre herramientas y [Ctrl+Mayús+Espacio] para mostrarla.

**Autocompletar** ofrece sugerencias contextuales mientras escribes, en un cuadro desplegable. Puede usar el teclado para desplazarse por los elementos del menú desplegable y, si pulsa [Intro] o [Tab], se insertará el elemento seleccionado en su código. Puede pulsar [Esc] para cerrar el menú desplegable y [Ctrl+Espacio] para abrirlo.

Estas funciones también se pueden activar a través del menú contextual del editor.

Las sugerencias de llamada de DAX se actualizan a medida que vas pasando por las alternativas de sintaxis utilizando las flechas arriba/abajo.

![Code Assist de DAX](~/content/assets/images/dax-code-assist.png)

La mayoría de los aspectos de la asistencia de código se pueden configurar en [**Herramientas > Preferencias > Editores de texto > Editor de DAX > Asistencia de código**](xref:preferences#text-editors--dax-editor--code-assist).

## Ver la definición

Mientras el cursor esté sobre una referencia de objeto, como una variable o una referencia de medida, presione [Alt+F12] para mostrar un editor insertado con la definición de ese objeto, debajo del cursor. Esto es útil cuando desea ver el código DAX de un objeto referenciado sin abandonar la posición actual en el documento.

![Ver la definición](~/content/assets/images/peek-definition.png)

Use la tecla Esc para volver a cerrar el panel Ver la definición.

## Ir a definición

En lugar de echar un vistazo, también podemos ir directamente a la ubicación donde se define el objeto al que se hace referencia. Para ello, pulse [F12]. Si el objeto al que se hace referencia no está definido dentro del documento actual, esta operación saltará a ese objeto en el Explorador TOM. Si es necesario, puedes volver atrás usando [Alt+Flecha izquierda].

## Definir medida

En el caso de los scripts DAX y las consultas DAX, a veces resulta útil incluir la definición de una medida a la que se hace referencia en otra parte del código. La función **Definir medida** le permite hacerlo cuando el cursor está sobre una referencia de medida. También puede elegir la opción **Definir medida con dependencias** si desea incluir también todas las referencias de medidas posteriores.

![Definir medida con dependencias](~/content/assets/images/define-measure-with-deps.png)

## Medida en línea

Si desea incorporar la definición de una medida al documento actual, la función **Medida en línea** le permite hacerlo. Haga clic con el botón derecho en una referencia de medida en el editor DAX y elija **Medida en línea**.

Una referencia de medida convierte implícitamente la fila actual en un filtro antes de que se evalúe la expresión de la medida. Por lo tanto, pegar la expresión tal cual cambiaría el resultado, de modo que cuando la referencia se encuentra dentro de un contexto de fila, por ejemplo, como el segundo argumento de un iterador como [`SUMX`](https://dax.guide/sumx) o [`FILTER`](https://dax.guide/filter), Tabular Editor envuelve la expresión insertada en [`CALCULATE`](https://dax.guide/calculate) para preservar ese comportamiento:

```dax
// Before using inline measure on the [Margin] measure
SUMX ( 'Sales', [Margin] )

// After using inline measure on the [Margin] measure
SUMX ( 'Sales', CALCULATE ( 'Sales'[Amount] - 'Sales'[Cost] ) )
```

El encapsulamiento solo se añade cuando puede marcar la diferencia. La expresión se inserta sin envolver cuando:

- La referencia **no está dentro de un contexto de fila**, incluso cuando ya se encuentra dentro de su propio `CALCULATE( ... )`.
- La expresión de la medida **no lee nada del modelo** (una constante, una referencia a otra medida o una llamada a una función como `TODAY()`). Una referencia a una tabla, una columna, un calendario o una [función definida por el usuario](xref:udfs) sí cuenta como lectura del modelo y sí se le aplica el «wrap».
- La expresión **ya realiza la transición por sí misma**, a través de un `CALCULATE( ... )` o `CALCULATETABLE( ... )` sin argumentos de filtro. Con un argumento de filtro, el «wrap» se añade de todos modos, ya que los argumentos de filtro se evalúan antes de la transición.

Si no se puede analizar la expresión de la medida, se añade el encapsulamiento, partiendo del principio de que un encapsulamiento que no era necesario es inofensivo, mientras que uno que falta no lo es.

## Formatear DAX

El editor DAX de Tabular Editor 3 formatea automáticamente su código mientras escribe, es decir, corrige las mayúsculas y minúsculas de las funciones y las referencias a objetos, añade la sangría adecuada y espacios entre paréntesis, etc. Todo esto se puede configurar en [**Herramientas > Preferencias > Editores de texto > Editor de DAX > Formato automático**](xref:preferences#text-editors--dax-editor--auto-formatting).

Sin embargo, a veces es necesario dar formato a todo el documento. Para ello, pulse [F6] o [Mayús+F6] si prefiere saltos de línea más frecuentes. En el caso de las consultas DAX, también puede usar [Alt+F6] para formatear de nuevo el código de forma que siempre se añadan comas al principio de una línea, lo cual resulta útil al depurar. 

## Refactorización

Si desea cambiar el nombre de una variable o de una columna de extensión, puede usar la opción **Refactorizar** (Ctrl+R) mientras el cursor esté situado en la referencia de la variable o de la columna de extensión. Esto seleccionará todas las instancias de ese objeto, lo que le permitirá cambiarle el nombre en todas partes a la vez.

## Accesos directos de teclado configurables

El Editor de DAX y los editores de código en general son muy configurables y admiten muchos comandos adicionales para editar código de forma rápida y productiva. Puede ver todos estos comandos, así como modificar y asignar atajos de teclado en **Herramientas > Preferencias > Tabular Editor > Teclado**.
