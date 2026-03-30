---
uid: creating-and-testing-dax
title: Agregar medidas y otros objetos calculados
author: Daniel Otykier
updated: 2021-10-08
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

# Agregar medidas y otros objetos calculados

Desde que se lanzó Tabular Editor 2.x a principios de 2017, la posibilidad de modificar rápidamente expresiones DAX en varias medidas siempre ha sido la característica más popular de la herramienta. Junto con la navegación hacia atrás y hacia adelante, las operaciones de copiar y pegar, la visualización de dependencias de DAX y la compatibilidad con deshacer/rehacer, la herramienta siempre ha sido la opción preferida para quienes trabajan con modelos de Data model grandes y complejos, donde la capacidad de realizar rápidamente varios cambios pequeños es crucial.

La única queja al respecto por parte de los usuarios de Tabular Editor 2.x era la falta de funciones de Code Assist para DAX (a veces llamadas "IntelliSense"). Especialmente cuando no dominas DAX al 100% (¡y muy poca gente lo hace!), que el editor de código DAX te ayude a recordar la sintaxis, los parámetros de las funciones, etc., resulta increíblemente útil.

Todo esto se ha resuelto con el nuevo editor de código DAX que usa Tabular Editor 3.

![Edición de una expresión DAX compleja](~/content/assets/images/dax-editor-screenshot.png)

El resto de este artículo describe cómo crear medidas y otros objetos calculados, y cómo modificar las expresiones DAX en estos objetos. Para obtener más información sobre las numerosas funciones del editor de código DAX, consulta <xref:dax-editor>.

# Agregar medidas

Una vez que hayas [importado algunas tablas](xref:importing-tables-data-modeling#importing-new-tables) a tu modelo y [creado relaciones entre ellas](xref:importing-tables-data-modeling#modifying-relationships-using-the-diagram), es el momento de agregar algunas medidas explícitas que contengan tu lógica de negocio.

> [!TIP]
> Técnicamente, no es obligatorio agregar medidas explícitas a tu modelo antes de visualizar datos en un Report de Power BI. Sin embargo, es una buena práctica hacerlo siempre, ya que las herramientas cliente basadas en MDX (como Excel y el Pivot Grid de Tabular Editor 3) requieren que las medidas se definan explícitamente. Además, los [grupos de cálculo](https://docs.microsoft.com/en-us/analysis-services/tabular-models/calculation-groups?view=asallproducts-allversions) solo se aplican a medidas explícitas.

Para agregar una nueva medida con Tabular Editor, haz clic con el botón derecho en la tabla en la que quieres agregar la medida y luego elige **Crear > Medida** (ALT+1).

![Agregar una nueva medida](~/content/assets/images/adding-new-measure.png)

Cuando se agrega una nueva medida, podrás editar su nombre. Pulsa ENTER cuando hayas proporcionado un nombre para la medida. Puedes editar el nombre más adelante en la vista **Properties** o pulsando F2 mientras la medida está seleccionada en el **Explorador TOM**.

La vista **Editor de expresiones** se usa para escribir la expresión DAX de la medida. Mientras escribes el código, fíjate en cómo el editor de DAX ofrece sugerencias e incluso subraya errores sintácticos o semánticos.

![Agregar Medida Editar Dax](~/content/assets/images/add-measure-edit-dax.png)

El desplegable de la esquina superior izquierda del **Editor de expresiones** se usa para alternar entre distintas propiedades DAX del objeto actualmente seleccionado. Por ejemplo, en las versiones más recientes de Analysis Services, las medidas tienen una propiedad `Expression` además de una [`Detail Rows Expression`](https://www.sqlbi.com/articles/controlling-drillthrough-in-excel-pivottables-connected-to-power-bi-or-analysis-services/). Otros tipos de objetos pueden tener propiedades diferentes que contengan código DAX. Por ejemplo, los [KPI](https://docs.microsoft.com/en-us/analysis-services/tabular-models/kpis-ssas-tabular?view=asallproducts-allversions) tienen tres propiedades de DAX diferentes. Para agregar un KPI en Tabular Editor, haz clic con el botón derecho en una medida y selecciona **Create > KPI**.

![Editar Kpis](~/content/assets/images/editing-kpis.png)

Si quieres que tu medida esté oculta, haz clic con el botón derecho y selecciona la opción **Make invisible** (CTRL+I). Del mismo modo, puedes volver a mostrar una medida seleccionando la opción **Make visible** (CTRL+U).

## Otras propiedades de la medida

Además de las propiedades `Name`, `Expression` y `Hidden`, puedes usar la vista **Properties** para revisar y editar el valor de todas las propiedades del objeto(s) seleccionado actualmente en el **Explorador TOM**. En el caso de las medidas, aquí puedes establecer, por ejemplo, `Format String`. Para más información, consulta [vista de propiedades](xref:properties-view).

# Agregar columnas calculadas

Para agregar una columna calculada, haz clic con el botón derecho en la tabla a la que quieras agregarla y elige **Create > Calculated Column** (ALT+2). Ponle un nombre a la columna y edita su expresión DAX con el **Editor de expresiones**, igual que hicimos con las medidas más arriba.

> [!IMPORTANT]
> Esta opción no está disponible de forma predeterminada cuando estás conectado a un modelo de Power BI Desktop. Esto se debe a las [limitaciones de compatibilidad de Power BI Desktop con herramientas externas](xref:desktop-limitations). Haz clic en el vínculo para obtener más información.

> [!NOTE]
> Cuando se haya cambiado la expresión DAX de una columna calculada, debes actualizar la tabla en la que se encuentra la columna antes de poder usarla en un Report. Consulta <xref:refresh-preview-query#refreshing-data> para obtener más información.

# Agregar tablas calculadas

Para agregar una tabla calculada, haz clic con el botón derecho en el modelo o en la carpeta "Tablas" y elige **Crear > Tabla calculada** (ALT+6). Asigna un nombre a la tabla y edita su expresión DAX con el **Editor de expresiones**, igual que hicimos antes con las medidas. Observa que las columnas de la tabla cambian automáticamente cuando haces un cambio en la expresión DAX. Esto puede provocar efectos en cascada si otras expresiones DAX hacen referencia a la tabla o si se usan columnas en una jerarquía.

> [!IMPORTANT]
> Esta opción no está disponible de forma predeterminada cuando te conectas a un modelo de Power BI Desktop. Esto se debe a las [limitaciones de la compatibilidad de Power BI Desktop con herramientas externas](xref:desktop-limitations). Haz clic en el enlace para obtener más información.

> [!NOTE]
> Cuando cambias la expresión DAX de una tabla calculada, tienes que actualizar la tabla antes de poder usarla en un Report. Consulta <xref:refresh-preview-query#refreshing-data> para obtener más información.

# Agregar grupos de cálculo

Para agregar un [grupo de cálculo](https://docs.microsoft.com/en-us/analysis-services/tabular-models/calculation-groups?view=asallproducts-allversions), haz clic con el botón derecho en el modelo o en la carpeta "Tablas" y elige **Crear > Grupo de cálculo** (ALT+7). Asigna un nombre al grupo de cálculo. Considera también usar un nombre diferente para la columna **Name** predeterminada.

> [!IMPORTANT]
> Esta opción solo está disponible en modelos con nivel de compatibilidad 1500 o superior.

Para agregar elementos de cálculo, haz clic con el botón derecho en el grupo de cálculo recién creado y elige **Crear > Elemento de cálculo**. Asigna un nombre al elemento de cálculo y edita su expresión DAX con el **Editor de expresiones**, igual que hicimos antes con las medidas.

Puedes organizar el orden de visualización de los elementos de cálculo arrastrándolos en el Explorador TOM o estableciendo la propiedad `Ordinal` en la vista **Propiedades**.

> [!NOTE]
> Cuando agregas, cambias el nombre o eliminas elementos de cálculo de un grupo de cálculo, tienes que actualizar el grupo de cálculo antes de poder usarlo en un Report. Consulta <xref:refresh-preview-query#refreshing-data> para obtener más información.

# Operaciones de modelado comunes

## Copiar y pegar

Todos los objetos del Explorador TOM se pueden copiar y pegar en Tabular Editor. Incluso puedes copiar y pegar entre diferentes instancias de Tabular Editor, e incluso entre Tabular Editor 2.x y Tabular Editor 3. Puedes usar los atajos de teclado habituales:

- **Editar > Copiar** (CTRL+C)
- **Editar > Cortar** (CTRL+X)
- **Editar > Pegar** (CTRL+V)

> [!TIP]
> Si quieres sustituir una tabla por otra y conservar todas las relaciones existentes con esa tabla, copia una tabla al portapapeles; después, en el Explorador TOM, selecciona la tabla que quieras sustituir y pega. Se te preguntará si quieres reemplazar la tabla seleccionada por la que está en el portapapeles.

## Deshacer / rehacer

Cada vez que haces un cambio en un objeto o una propiedad en Tabular Editor, se registra el historial completo de cambios, lo que te permite deshacer cualquier cambio que hayas hecho. Puedes usar los atajos de teclado habituales:

- **Editar > Deshacer** (CTRL+Z)
- **Editar > Rehacer** (CTRL+Y)

> [!NOTE]
> Todos los editores de texto de Tabular Editor 3 tienen su propio historial de deshacer/rehacer, por lo que, si el cursor está dentro de un editor de texto, los atajos de teclado desharán y rehacerán lo que hayas escrito en ese editor. Puedes usar las opciones del menú **Editar** para deshacer/rehacer a nivel de modelo, o desactivar el editor de texto actual haciendo clic en otro elemento de la interfaz de usuario (como el Explorador TOM).

# Navegación

Cuando el cursor esté sobre una referencia a un objeto en el editor de DAX, haz clic con el botón derecho y elige **Ir a definición** (F12) para saltar rápidamente a ese objeto. Por supuesto, también puedes navegar entre objetos usando el Explorador TOM.

Puedes usar los botones de flecha de la esquina superior derecha del **Editor de expresiones** para saltar rápidamente hacia delante y hacia atrás entre los objetos visitados.

## Dependencias de DAX

Para ver las dependencias de DAX entre objetos, selecciona un objeto en el **Explorador TOM**; luego, haz clic con el botón derecho y elige **Mostrar dependencias** (SHIFT+F12). Esto abrirá una ventana que muestra las dependencias (en ambas direcciones) del objeto seleccionado. Haz doble clic en un objeto en esta ventana para navegar rápidamente hasta él.

![Dependencias de Dax y Explorador Tom](~/content/assets/images/dax-dependencies-and-tom-explorer.png)

# Carpetas de visualización

Cuando tu modelo empieza a tener un número considerable de medidas, una buena práctica es organizarlas usando carpetas de visualización. En Tabular Editor, para crear una carpeta de visualización, edita la propiedad `Display Folder` en la vista **Propiedades** o, alternativamente, haz clic con el botón derecho en medida(s) y selecciona la opción **Crear > Carpeta de visualización**.

También puedes cortar/copiar/pegar o arrastrar y soltar objetos entre carpetas de visualización.

# Próximos pasos

- @dax-script-introduction
- @bpa
- @cs-scripts-and-macros