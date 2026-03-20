---
uid: dax-editor
title: Editor de DAX
author: Daniel Otykier
updated: 2023-02-03
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Escritorio
          full: true
        - edition: Negocios
          full: true
        - edition: Empresarial
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

![Dax Code Assist](~/content/assets/images/dax-code-assist.png)

La mayoría de los aspectos de Code Assist se pueden configurar en [**Herramientas > Preferencias > Editores de texto > Editor de DAX > Code Assist**](xref:preferences#dax-editor--code-assist).

## Ver la definición

Con el cursor sobre una referencia a un objeto, como una variable o una referencia a una medida, pulsa [Alt+F12] para mostrar un editor en línea con la definición de ese objeto, debajo del cursor. Esto resulta útil cuando desea ver el código DAX de un objeto al que se hace referencia sin salir de la posición actual del documento.

![Ver la definición](~/content/assets/images/peek-definition.png)

Usa la tecla Esc para volver a cerrar el panel de Ver la definición.

## Ir a definición

En lugar de usar Ver la definición, también podemos saltar directamente a la ubicación donde está definido el objeto referenciado. Para ello, pulsa [F12]. Si el objeto referenciado no está definido en el documento actual, esta operación saltará a ese objeto en el Explorador TOM. Si lo necesita, puede volver atrás con [Alt+Flecha izquierda].

# Definir medida

En los scripts DAX y las consultas DAX, a veces es útil incluir la definición de una medida a la que se hace referencia en otra parte del código. La función **Definir medida** permite hacerlo cuando el cursor está sobre una referencia a una medida. También puede elegir la opción **Definir medida con dependencias** si desea incluir también todas las referencias posteriores a medidas.

![Definir medida con dependencias](~/content/assets/images/define-measure-with-deps.png)

# Medida en línea

Si desea traer la definición de una medida al documento actual, la función **Medida en línea** permite hacerlo. Cuando un contexto de fila envuelve la referencia a la medida original, Tabular Editor encierra automáticamente la expresión de la medida en [`CALCULATE`](https://dax.guide/calculate) (tal como ocurre implícitamente en las referencias a medidas).

# Formatear DAX

El Editor de DAX de Tabular Editor 3 formatea automáticamente su código mientras escribe; es decir, corrige las mayúsculas y minúsculas de las funciones y las referencias a objetos, añade la sangría adecuada y los espacios entre paréntesis, etc. Todo esto se puede configurar en [**Herramientas > Preferencias > Editores de texto > Editor de DAX > Formato automático**](xref:preferences#dax-editor--auto-formatting).

Sin embargo, a veces es necesario formatear todo el documento. Puedes hacerlo pulsando [F6] o [Shift+F6] si prefieres saltos de línea más frecuentes. Para las Consultas DAX, también puedes usar [Alt+F6] para reformatear el código y hacer que las comas se coloquen siempre al principio de cada línea, lo cual es útil al depurar.

# Refactorización

Si quieres cambiar el nombre de una variable o de una columna de extensión, puedes usar la opción **Refactor** (Ctrl+R) con el cursor situado sobre la referencia de la variable o de la columna de extensión. Esto seleccionará todas las apariciones de ese objeto, lo que te permite cambiarle el nombre en todas partes de una sola vez.

# Atajos de teclado configurables

El Editor de DAX y los editores de código en general son muy configurables y admiten muchos comandos adicionales para editar código de forma rápida y productiva. Puedes ver todos estos comandos, así como modificar y asignar atajos de teclado en **Herramientas > Preferencias > Tabular Editor > Teclado**.