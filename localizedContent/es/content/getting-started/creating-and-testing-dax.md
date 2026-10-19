---
uid: creating-and-testing-dax
title: Añadir medidas y otros objetos calculados
author: Daniel Otykier
updated: 2026-10-13
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

# Añadir medidas y otros objetos calculados

Desde que se lanzó Tabular Editor 2.x a principios de 2017, la capacidad de modificar rápidamente las expresiones DAX en todas las medidas siempre ha sido la función más popular de la herramienta. Junto con la navegación hacia atrás y hacia delante, las operaciones de copiar/pegar, la visualización de dependencias DAX y el soporte para deshacer/rehacer, la herramienta siempre ha sido la opción preferida de cualquiera que trabaje con modelos de datos grandes y complejos, donde es crucial poder realizar rápidamente múltiples cambios menores.

La única queja al respecto por parte de los usuarios de Tabular Editor 2.x fue la falta de funciones de asistencia para el código DAX (a veces denominadas «IntelliSense»). Especialmente cuando no se domina DAX al 100 % (¡y muy pocas personas lo dominan!), contar con el editor de código DAX para ayudarle a recordar la sintaxis, los parámetros de las funciones, etc., resulta increíblemente útil.

Todo esto se ha solucionado con el nuevo editor de código DAX que utiliza Tabular Editor 3.

![Editar una expresión DAX compleja](~/content/assets/images/dax-editor-screenshot.png)

El resto de este artículo describe cómo crear medidas y otros objetos calculados, y cómo modificar las expresiones DAX de estos objetos. Para obtener más información sobre las numerosas funciones del editor de código DAX, consulte <xref:dax-editor>.

# Añadir medidas

Una vez que haya [importado algunas tablas](xref:importing-tables-data-modeling#importing-new-tables) a su modelo y [creado relaciones entre ellas](xref:importing-tables-data-modeling#modifying-relationships-using-the-diagram), es hora de añadir algunas medidas explícitas que contengan su lógica empresarial.

> [!TIP]
> Técnicamente, no es necesario que agregues medidas explícitas a tu modelo antes de visualizar los datos en un informe de Power BI. Sin embargo, es una práctica recomendada hacerlo siempre, ya que las herramientas cliente basadas en MDX (como Excel y Pivot Grid de Tabular Editor 3) requieren medidas explícitas. Además, los [grupos de cálculos](https://docs.microsoft.com/analysis-services/tabular-models/calculation-groups?view=asallproducts-allversions) solo se aplican a medidas explícitas.

Para añadir una nueva medida utilizando Tabular Editor, haga clic con el botón derecho en la tabla en la que desea añadir la medida y, a continuación, seleccione **Crear > Medida** (ALT+1).

![Añadir una nueva medida](~/content/assets/images/adding-new-measure.png)

Cuando se agregue una nueva medida, el nombre de esa medida será editable. Pulse INTRO cuando haya indicado un nombre para la medida. Siempre puede editar el nombre más tarde en la vista **Propiedades** o pulsando F2 mientras la medida está seleccionada en el **Explorador TOM**.

La vista **Editor de expresiones** se utiliza para proporcionar la expresión DAX para la medida. A medida que introduzca el código, observe cómo el editor DAX proporciona sugerencias de código e incluso subraya los errores de sintaxis o semánticos.

![Añadir medida Editar DAX](~/content/assets/images/add-measure-edit-dax.png)

El cuadro desplegable situado en la esquina superior izquierda del **Editor de expresiones** se utiliza para alternar entre las diferentes propiedades DAX del objeto seleccionado actualmente. Por ejemplo, en las versiones más recientes de Analysis Services, las medidas tienen una propiedad «Expresión», así como una propiedad ['Expresión de filas de detalle'](https://www.sqlbi.com/articles/controlling-drillthrough-in-excel-pivottables-connected-to-power-bi-or-analysis-services/). Otros tipos de objetos pueden tener diferentes propiedades que contengan código DAX. Por ejemplo, los [KPI](https://docs.microsoft.com/analysis-services/tabular-models/kpis-ssas-tabular?view=asallproducts-allversions) tienen tres propiedades DAX diferentes. Para añadir un KPI en Tabular Editor, haga clic derecho en una medida y elija **Crear > KPI**.

![Editar KPI](~/content/assets/images/editing-kpis.png)

Si quieres que tu medida esté oculta, simplemente haz clic derecho y elige la opción **Hacer invisible** (CTRL+I). Del mismo modo, puedes mostrar una medida seleccionando la opción **Hacer visible** (CTRL+U).

## Otras propiedades de las medidas

Además de las propiedades «Nombre», «Expresión» y «Oculto», puede utilizar la vista **Propiedades** para revisar y editar el valor de todas las propiedades de los objetos seleccionados actualmente en el **Explorador TOM**. En el caso de las medidas, aquí es donde puede establecer la «Cadena de formato», por ejemplo. Para obtener más información, consulte [Vista de propiedades](xref:properties-view).

# Añadir columnas calculadas

Para añadir una columna calculada, haga clic derecho en la tabla en la que desea añadir la columna y elija **Crear > Columna calculada** (ALT+2). Asigne un nombre a la columna y edite su expresión DAX utilizando el **Editor de expresiones**, de forma similar a como lo hicimos con las medidas anteriores.

> [!IMPORTANT]
> Esta opción no está disponible de forma predeterminada cuando se está conectado a un modelo de Power BI Desktop. Esto se debe a las [limitaciones de la compatibilidad de Power BI Desktop con herramientas externas](xref:desktop-limitations). Haga clic en el enlace para obtener más información.

> [!NOTE]
> Cuando se ha modificado la expresión DAX de una columna calculada, es necesario actualizar la tabla en la que se encuentra la columna antes de poder usarla en un informe. Consulta <xref:refresh-preview-query#refreshing-data> para obtener más información.

# Adición de tablas calculadas

Para añadir una tabla calculada, haga clic con el botón derecho en el modelo o en la carpeta «Tablas» y elija **Crear > Tabla calculada** (ALT+6). Asigne un nombre a la tabla y edite su expresión DAX utilizando el **Editor de expresiones**, de forma similar a como lo hicimos con las medidas anteriores. Observe que las columnas de la tabla cambian automáticamente cuando realiza un cambio en la expresión DAX. Esto puede provocar efectos en cascada si otras expresiones DAX hacen referencia a la tabla o si se usan columnas en una jerarquía.

> [!IMPORTANT]
> Esta opción no está disponible de forma predeterminada cuando se está conectado a un modelo de Power BI Desktop. Esto se debe a las [limitaciones de la compatibilidad de Power BI Desktop con herramientas externas](xref:desktop-limitations). Haga clic en el enlace para obtener más información.

> [!NOTE]
> Cuando se ha modificado la expresión DAX de una tabla calculada, es necesario actualizar la tabla antes de poder usarla en un informe. Consulta <xref:refresh-preview-query#refreshing-data> para obtener más información.

# Añadir grupos de cálculos

Para añadir un [grupo de cálculos](https://docs.microsoft.com/analysis-services/tabular-models/calculation-groups?view=asallproducts-allversions), haga clic derecho en el modelo o en la carpeta «Tablas» y elija **Crear > Grupo de cálculos** (ALT+7). Asigne un nombre al grupo de cálculo. Considere también un nombre diferente para la columna **Nombre** predeterminada.

> [!IMPORTANT]
> Esta opción solo está disponible en modelos con un nivel de compatibilidad de 1470 o superior. Analysis Services admite grupos de cálculos a partir del nivel de compatibilidad 1500.

Para añadir elementos de cálculo, haga clic derecho en el grupo de cálculos recién creado y elija **Crear > Elemento de cálculo**. Asigna un nombre al elemento de cálculo y edita su expresión DAX utilizando el **Editor de expresiones** de forma similar a como lo hicimos con las medidas anteriores.

Puede organizar el orden de visualización de los elementos de cálculo arrastrándolos por el Explorador TOM o estableciendo la propiedad «Ordinal» en la vista **Propiedades**. Al establecer «Ordinal», el elemento se desplaza a esa posición, y un valor superior a la última posición desplaza el elemento al final.

> [!NOTE]
> Cuando se añaden, se cambian de nombre o se eliminan elementos de cálculo de un grupo de cálculos, es necesario actualizar el grupo de cálculos antes de poder usarlo en un informe. Consulta <xref:refresh-preview-query#refreshing-data> para obtener más información.

# Operaciones de modelado comunes

## Copiar/pegar

Todos los objetos del Explorador TOM se pueden copiar y pegar con Tabular Editor. Incluso puedes copiar y pegar entre diferentes instancias de Tabular Editor, e incluso entre Tabular Editor 2.x y Tabular Editor 3. Puede usar los accesos directos de teclado habituales:

- **Editar > Copiar** (CTRL+C)
- **Editar > Cortar** (CTRL+X)
- **Editar > Pegar** (CTRL+V)

> [!TIP]
> Si deseas reemplazar una tabla por otra, conservando todas las relaciones existentes hacia/desde esa tabla, copia una tabla al portapapeles, luego selecciona la tabla que deseas reemplazar en el Explorador TOM y pégala. Se le preguntará si desea reemplazar la tabla seleccionada por la que está en el portapapeles.

## Deshacer/rehacer

Cada vez que se realiza un cambio en un objeto o una propiedad en Tabular Editor, se registra el historial completo de cambios, lo que le permite deshacer todos los cambios realizados. Puede usar los conocidos atajos de teclado:

- **Editar > Deshacer** (CTRL+Z)
- **Editar > Rehacer** (CTRL+Y)

> [!NOTE]
> Los editores de texto de Tabular Editor 3 tienen su propio historial de deshacer. Cuando el cursor está en un editor de texto, **Ctrl+Z** y **Ctrl+Y** deshacen y rehacen la escritura en ese editor. Para deshacer un cambio en el modelo, haga clic primero en el Explorador TOM o seleccione la entrada de deshacer del modelo en el menú **Editar**. Consulte [Deshacer en editores de texto](xref:undo-redo#undo-in-text-editors).

# Navegación

Mientras el cursor esté sobre una referencia de objeto en el editor DAX, haga clic derecho y elija **Ir a definición** (F12) para pasar rápidamente a ese objeto. Por supuesto, también puede navegar entre objetos utilizando el Explorador TOM.

Puede usar los botones de flecha en la esquina superior derecha del **Editor de expresiones** para pasar rápidamente de un objeto visitado a otro.

## Dependencias de DAX

Para ver las dependencias DAX entre objetos, seleccione un objeto en el **Explorador TOM**, luego haga clic derecho y elija **Mostrar dependencias** (**Mayús+F12**). Esto abre la vista **Dependencias DAX**, que muestra las dependencias del objeto seleccionado. Haga doble clic en un objeto del árbol para navegar hasta él, o haga clic derecho para **Ir al elemento**, **Copiar como texto** y **Copiar como JSON**.

![Dependencias DAX y Explorador TOM](~/content/assets/images/dax-dependencies-and-tom-explorer.png)

La vista muestra una dirección a la vez. Elija cuál con los botones de opción:

| Opción | Muestra |
|---|---|
| **Objetos que dependen de este** | Qué dejaría de funcionar si modificara o eliminara el objeto seleccionado |
| **Objetos de los que este depende** | De dónde lee el objeto seleccionado |
| **Relaciones que comienzan desde esta tabla** | Las relaciones que salen de la tabla seleccionada. Con una columna seleccionada, esto muestra **Relaciones que comienzan desde esta columna** |

Marque **Mostrar inactivos** para incluir las relaciones inactivas.

### Seguir al Explorador TOM

En lugar de invocar **Mostrar dependencias** para cada objeto por turno, marque **Seguir Explorador TOM** y la vista seguirá lo que esté seleccionado en el árbol. Al marcarlo, se muestran inmediatamente las dependencias del objeto que *ya* está seleccionado, en lugar de esperar al siguiente cambio de selección.

El seguimiento se aplica a un único objeto seleccionado. Si se seleccionan varios objetos, o ninguno, se borra la vista en lugar de mostrar una respuesta parcial.

# Carpetas de visualización

Cuando tu modelo empiece a tener un número considerable de medidas, una buena práctica es organizarlas mediante carpetas de visualización. En Tabular Editor, para crear una carpeta de visualización, edita la propiedad «Carpeta de visualización» a través de la vista **Propiedades** o, como alternativa, haz clic con el botón derecho en la(s) medida(s) y selecciona la opción **Crear > Carpeta de visualización**.

También puede cortar/copiar/pegar o arrastrar y soltar objetos entre carpetas de visualización.

# Próximos pasos

- @dax-script-introduction
- @bpa
- @cs-scripts-and-macros