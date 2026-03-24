---
uid: desktop-limitations
title: Limitaciones de Power BI Desktop (obsoletas)
author: Morten Lønskov
updated: 2023-08-21
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

# Limitaciones de Power BI Desktop

Al usar Tabular Editor (cualquier edición) como [herramienta externa para Power BI Desktop](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-external-tools), hay algunas limitaciones que debes tener en cuenta.

Las limitaciones mencionadas en este artículo también se aplican a Tabular Editor 2.x.

## Operaciones no compatibles

A partir de la actualización de junio de 2025 de Power BI Desktop, ya no hay operaciones de escritura no compatibles. En otras palabras, las herramientas de terceros ahora pueden modificar libremente cualquier aspecto del modelo semántico alojado en Power BI Desktop, incluida la posibilidad de agregar y quitar tablas y columnas, cambiar tipos de datos, etc. Por lo tanto, la mayor parte de la información de este artículo ya no es relevante. Sin embargo, si usas una versión de Power BI Desktop anterior a la actualización de junio de 2025, consulta las limitaciones en la sección [Operaciones de modelado de datos](#data-modeling-operations) más abajo.

Más información en [la entrada oficial del blog](https://powerbi.microsoft.com/en-us/blog/open-and-edit-any-semantic-model-with-power-bi-tools/).

## Tipos de archivo de Power BI

Al usar Power BI, encontrarás tres tipos de archivo habituales:

- **.pbix** (Power BI Report)
- **.pbit** (Plantilla de Power BI)
- **.pbip** (Proyecto de Power BI)

Estos dos archivos se pueden abrir en Power BI Desktop y, básicamente, definen todo lo relacionado con un Report de Power BI: Data sources, transformaciones de Power Query, el Data model tabular, páginas del Report, Visuals, Bookmarks, etc.

La principal diferencia es que los archivos **.pbix y .pbip contienen datos del modelo**, mientras que el archivo **.pbit no contiene datos**. Además, un archivo **.pbix** no contiene los metadatos del modelo en este formato y, por tanto, **no se puede cargar un archivo .pbix directamente en Tabular Editor** en modo alguno. En su lugar, tendrás que recurrir a la integración de Herramientas externas, que requiere cargar el archivo .pbix en Power BI Desktop, tal como se describe a continuación.

> [!WARNING]
> Aunque técnicamente es posible cargar y guardar metadatos del modelo desde y hacia un archivo .pbit, este enfoque no es compatible con Power BI Desktop. Por ello, siempre existe el riesgo de hacer cambios en el archivo .pbit que hagan que Power BI Desktop ya no pueda cargarlo o que generen problemas de estabilidad una vez cargado. En ese caso, el soporte técnico de Microsoft no podrá ayudarte.

> [!NOTE]
> Dado que **Tabular Editor 3 Edición de escritorio** está pensado únicamente para usarse como herramienta externa de Power BI Desktop, esta edición no permite cargar ni guardar un archivo .pbit. No obstante, puedes seguir usando Tabular Editor 2.x para este fin. Consulta <xref:editions> para obtener más información sobre las diferencias entre las ediciones de Tabular Editor 3.

## Arquitectura de herramientas externas

Cuando un Report de Power BI Desktop (archivo .pbix o .pbit) contiene un Data model (es decir, se han agregado una o más tablas en modo Import o DirectQuery), ese Data model se aloja dentro de una instancia de Analysis Services administrada por Power BI Desktop. Las herramientas externas pueden conectarse a esta instancia de Analysis Services para distintos propósitos.

> [!IMPORTANT]
> Los Report de Power BI Desktop que usan una **Live Connection** a SSAS, Azure AS o a un Dataset en un Workspace de Power BI no contienen un Data model. Por lo tanto, estos Reports **no** se pueden usar con herramientas externas como Tabular Editor.

Las herramientas externas pueden conectarse a la instancia de Analysis Services administrada por Power BI Desktop mediante un número de puerto específico asignado por Power BI Desktop. Cuando una herramienta se inicia directamente desde la cinta "Herramientas externas" de Power BI Desktop, este número de puerto se pasa a la herramienta externa como argumento de la línea de comandos. En el caso de Tabular Editor, esto hace que el Data model se cargue en Tabular Editor.

<img class="noscale" src="~/content/assets/images/external-tool-architecture.png" />

Una vez conectada a la instancia de Analysis Services, una herramienta externa puede obtener información sobre los metadatos del modelo, ejecutar consultas DAX o MDX sobre el Data model e incluso aplicar cambios a los metadatos del modelo mediante las [bibliotecas de cliente proporcionadas por Microsoft](https://docs.microsoft.com/en-us/analysis-services/client-libraries?view=asallproducts-allversions). En este sentido, la instancia de Analysis Services administrada por Power BI Desktop no difiere de cualquier otro tipo de instancia de Analysis Services.

## Operaciones de modelado del Data model

Sin embargo, debido a la forma en que Power BI Desktop interactúa con Analysis Services, existen algunas limitaciones importantes respecto al tipo de cambios que las herramientas externas pueden aplicar a los metadatos del modelo. Estas se enumeran [en la documentación oficial de herramientas externas](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-external-tools#data-modeling-operations) y se repiten aquí para mayor comodidad:

### [Antes de junio de 2025](#tab/postjune2023)

**Limitaciones de Power BI Desktop previas a junio de 2025 al conectarse mediante herramientas de terceros:**

| Objeto                                               | Conectarse a la instancia de AS |
| ---------------------------------------------------- | ------------------------------- |
| Tablas                                               | No                              |
| Columnas                                             | Sí <sup>[1](#columns)</sup>     |
| Tablas calculadas                                    | Sí                              |
| Columnas calculadas                                  | Sí                              |
| Relaciones                                           | Sí                              |
| Medidas                                              | Sí                              |
| KPIs del modelo                                      | Sí                              |
| Grupos de cálculo                                    | Sí                              |
| Perspectivas                                         | Sí                              |
| Traducciones                                         | Sí                              |
| Seguridad a nivel de fila (RLS)   | Sí                              |
| Seguridad a nivel de objeto (OLS) | Sí                              |
| Anotaciones                                          | Sí                              |
| Expresiones M                                        | No                              |

<a name="columns">1</a> - Al usar herramientas externas para conectarse a la instancia de AS, se admite cambiar el tipo de datos de una columna; sin embargo, no se admite renombrar columnas.

Los _archivos de proyecto_ de Power BI Desktop ofrecen un alcance más amplio de operaciones de escritura compatibles. Los objetos y las operaciones que no se admiten al usar Tabular Editor como herramienta externa pueden estar disponibles al editar los archivos de proyecto de Power BI Desktop. Consulta la documentación de Microsoft para obtener más información: [Proyectos de Power BI Desktop: creación del modelo](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview#model-authoring).

### [Antes de junio de 2023](#tab/prejune2023)

**Limitaciones de Power BI Desktop anteriores a junio de 2023 al conectarse mediante herramientas de terceros:**

- Definir y editar medidas para cálculos, incluyendo la cadena de formato, el KPI y la configuración de filas de detalle.
- Agregar grupos de cálculo para reutilizar cálculos en modelos complejos.
- Crear perspectivas para definir vistas enfocadas, específicas del dominio de negocio, de los metadatos del Dataset.
- Aplicar traducciones de metadatos para admitir versiones multilingües dentro de un único Dataset.
- Agregar roles del Dataset con reglas de seguridad a nivel de filas (RLS) y de seguridad a nivel de objetos (OLS) para restringir el acceso a los datos.
- Definir y editar parámetros de campo.

Aunque no esté admitido, resulta que aún se pueden aplicar varias operaciones sin causar problemas. Por ejemplo, en el momento de escribir esto, establecer propiedades como carpeta de visualización, Descripción, Resumir por, etc., en columnas individuales mediante una herramienta externa parece funcionar sin problemas. Por este motivo, Tabular Editor incluye una opción que permite a los usuarios avanzados experimentar, habilitando todas las operaciones de modelado de datos incluso al estar conectados a un Data model de Power BI Desktop. Puedes habilitar esta opción en **Herramientas > Preferencias > Power BI > Permitir operaciones de modelado _no compatibles_**, pero asegúrate de comprender los riesgos antes de hacerlo.

---

## Limitaciones del modelado del Data model

Se puede acceder a todos los metadatos del Tabular Object Model (TOM) en modo de solo lectura. Las operaciones de escritura son limitadas porque Power BI Desktop debe mantenerse sincronizado con las modificaciones externas; por lo tanto, además de las mencionadas en las pestañas anteriores, no se admiten las siguientes operaciones:

- Cualquier tipo de objeto TOM que no esté incluido en las operaciones de escritura compatibles, como tablas y columnas.
- Editar un archivo de plantilla de Power BI Desktop (PBIT).
- Traducciones a nivel de Report o a nivel de datos.
- Aún no se admite cambiar el nombre de las tablas ni de las columnas
- Enviar comandos de procesamiento a un Dataset cargado en Power BI Desktop

> [!NOTE]
> La instancia de Analysis Services administrada por Power BI Desktop no aplica las restricciones correspondientes a las operaciones permitidas de modelado del Data model. La herramienta externa debe asegurarse de que no se realicen cambios no compatibles. Ignorar esto puede provocar resultados impredecibles, archivos de Report .pbix/.pbit corruptos o que Power BI Desktop se vuelva inestable.

> [!IMPORTANT]
> Los cambios en el Data model pueden hacer que los Visuales de tu Report de Power BI dejen de funcionar. Si, por ejemplo, se mueve una medida de una tabla a otra, cualquier Visual que use esa medida tendrá que actualizarse. Kurt Buhler tiene una entrada de blog sobre cómo corregir estos errores de una forma menos manual aquí: [Fix Power BI "Something is wrong with one or more fields"](https://data-goblins.com/power-bi/something-is-wrong-with-one-or-more-fields)

# Tabular Editor y Power BI Desktop

Cuando usas Tabular Editor (cualquier edición) como herramienta externa para Power BI Desktop, todas las operaciones no compatibles según la lista anterior se deshabilitan de forma predeterminada. En otras palabras, Tabular Editor no te permitirá agregar o cambiar el nombre de tablas o columnas, realizar actualizaciones, etc. en un modelo de Power BI Desktop.

Aunque no sea compatible, resulta que se pueden aplicar varias operaciones sin causar problemas. Por este motivo, Tabular Editor incluye una opción que permite a los usuarios avanzados experimentar habilitando todas las operaciones de modelado de datos, incluso cuando se conecta a un Data model de Power BI Desktop. Puedes habilitar esta opción en **Herramientas > Preferencia > Power BI > Permitir operaciones de modelado _no admitidas_**, pero asegúrate de entender los riesgos antes de hacerlo.

> [!NOTE]
> En Tabular Editor 2.x, esta configuración está disponible en **Archivo > Preferencia > Permitir características no admitidas de Power BI (experimental)**

Una vez habilitada esta característica, Tabular Editor dejará de bloquear cualquier operación de modelado y, en su lugar, te proporcionará acceso completo de lectura/escritura a todos los objetos y propiedades de TOM. Mientras la característica esté habilitada, verás un aviso cada vez que abras un modelo de Power BI Desktop en Tabular Editor:

![Advertencia mostrada cuando el modelado no admitido está habilitado](~/content/assets/images/pbi-desktop-warning.png)

> [!WARNING]
> Si tu archivo .pbix o .pbit se daña o provoca inestabilidad en Power BI Desktop debido a cambios no admitidos realizados mediante una herramienta externa, el soporte de Microsoft no podrá ayudarte. Por este motivo, conserva **siempre** una copia de seguridad de tu archivo .pbix o .pbit antes de iniciar cualquier herramienta externa que permita hacer cambios en tu Data model.
