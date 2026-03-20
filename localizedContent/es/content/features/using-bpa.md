---
uid: using-bpa
title: Uso del Best Practice Analyzer
author: Morten Lønskov
updated: 2023-02-09
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

# Best Practice Analyzer

El Best Practice Analyzer (BPA) le permite definir reglas sobre los metadatos de su modelo para fomentar determinadas convenciones y prácticas recomendadas durante el desarrollo de su modelo de Power BI o Analysis Services.

> [!NOTE]
> Tabular Editor 3 incluye un conjunto completo de [reglas integradas del Best Practice Analyzer](xref:built-in-bpa-rules) que están habilitadas de forma predeterminada para los usuarios nuevos.

## Descripción general de BPA

La descripción general de BPA le muestra todas las reglas definidas en su modelo que actualmente se están incumpliendo:

![BPA Overview](~/content/assets/images/common/BPAOverview.png)

Y siempre podrá ver en la interfaz principal cuántas reglas está infringiendo actualmente.

![BPA Overview Line](~/content/assets/images/common/PBAOverviewMenuLine.png)

Al hacer clic en el enlace (o pulsar F10) se abre la ventana completa de BPA.

> [!NOTE]
> Si prefiere un recorrido en vídeo, PowerBI.tips tiene un vídeo con nuestro propio Daniel Otykier mostrando el Best Practice Analyzer en detalle aquí:

<iframe width="640" height="360" src="https://www.youtube-nocookie.com/embed/5WnN0NG2nBk" title="PowerBI.Tips - Tutorial - Best Practice Analyzer in Tabular Editor" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

### Funcionalidad

Cada vez que se realiza un cambio en el modelo, el Best Practice Analyzer analiza su modelo en segundo plano en busca de problemas. Puede desactivar esta función en **Herramientas > Preferencias > Best Practice Analyzer**.

La ventana de BPA, tanto en TE2 como en TE3, le permite acoplarla en un lado de su escritorio, mientras mantiene la ventana principal en el otro, lo que le permite trabajar con su modelo mientras ve los problemas de BPA.

La ventana del Best Practice Analyzer enumera continuamente todas las **reglas efectivas** de su modelo, así como los objetos que incumplen cada regla. Al hacer clic con el botón derecho en cualquier parte de la lista o usar los botones de la barra de herramientas en la parte superior de la ventana, puede realizar las siguientes acciones:

- **Administrar reglas...**: Se abre la interfaz de Administrar reglas, que veremos más abajo. También puedes acceder a esta interfaz desde el menú "Herramientas > Administrar reglas de BPA..." de la interfaz principal.
- **Ir al objeto...**: Al elegir esta opción o hacer doble clic en un objeto de la lista, se te llevará al mismo objeto en la interfaz principal.
- **Ignorar elemento/elementos**: Si seleccionas uno o varios objetos de la lista y eliges esta opción, se aplicará una anotación a los objetos seleccionados que indica que Best Practice Analyzer debe ignorarlos en adelante. Si ignoraste un objeto por error, activa el botón "Mostrar ignorados" en la parte superior de la pantalla. Esto te permitirá dejar de ignorar un objeto que se había ignorado previamente.
- **Ignorar regla**: Si has seleccionado una o varias reglas en la lista, esta opción agregará una anotación a nivel de modelo que indica que la regla seleccionada siempre debe ignorarse. De nuevo, activando el botón "Mostrar ignorados" también puedes dejar de ignorar reglas.
- **Generar script de corrección**: En las reglas que tengan una corrección sencilla (es decir, cuando el problema se puede resolver simplemente estableciendo una única propiedad en el objeto), esta opción estará habilitada. Al hacer clic, se copiará un C# Script en el portapapeles. Luego puedes pegar este script en el área de [Scripting avanzado](/Advanced-Scripting) de Tabular Editor, donde podrás revisarlo antes de ejecutarlo para aplicar la corrección.
- **Aplicar corrección**: Esta opción también está disponible para las reglas que tengan una corrección sencilla, como se mencionó anteriormente. En lugar de copiar el script al portapapeles, se ejecutará de inmediato.

## Gestión de reglas de mejores prácticas

Si necesitas agregar, quitar o modificar las reglas que se aplican a tu modelo, hay una interfaz específica para ello. Puedes abrirla haciendo clic en el botón de la esquina superior izquierda de la ventana de Best Practice Analyzer, o usando la opción de menú "Herramientas > Administrar reglas de BPA..." en la ventana principal.

![BPA Manage Rules](~/content/assets/images/common/BPAOverviewManageRules.png)

La ventana Administrar reglas de BPA contiene dos listas: la lista superior representa las **colecciones** de reglas que están cargadas actualmente. Al seleccionar una colección en esta lista, se mostrarán todas las reglas definidas dentro de esa colección en la lista inferior.

![BPA Manage Rules UI](~/content/assets/images/common/PBAOverviewManageRulesPopUp.png)