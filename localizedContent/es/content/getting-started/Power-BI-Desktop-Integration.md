---
uid: desktop-integration
title: Integración con Power BI Desktop
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

# Integración con Power BI Desktop

[Power BI Desktop admite herramientas externas](https://docs.microsoft.com/en-us/power-bi/create-reports/desktop-external-tools), lo que permite a Tabular Editor realizar operaciones de modelado al trabajar con datos importados o DirectQuery en Power BI Desktop.

![image](~/content/assets/images/getting-started/power-bi-desktop-integration.png)

## Requisitos previos

- [Power BI Desktop](https://www.microsoft.com/en-us/download/details.aspx?id=58494) (julio de 2020 o posterior)
- [La versión más reciente de Tabular Editor](https://tabulareditor.com/downloads)

Además, se recomienda encarecidamente que la opción [fecha/hora automática](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-auto-date-time) esté **deshabilitada** (configuración de Power BI Desktop en "Carga de datos").

## Arquitectura de herramientas externas

Cuando un Report de Power BI Desktop contiene un Data model (es decir, se han agregado una o más tablas en modo Import o DirectQuery), ese Data model se hospeda dentro de una instancia de Analysis Services administrada por Power BI Desktop. Las herramientas externas pueden conectarse a esta instancia de Analysis Services con distintos fines.

> [!IMPORTANT]
> Los Reports de Power BI Desktop que usan una **conexión en vivo** a SSAS, Azure AS o a un Dataset en un Workspace de Power BI no contienen un Data model. Por tanto, estos Reports **no pueden** usarse con herramientas externas como Tabular Editor.

> [!IMPORTANT]
> Los Reports de Power BI Desktop que editan directamente un modelo **Direct Lake** u otro modelo de Fabric no contienen un Data model. En su lugar, Tabular Editor abrirá el modelo directamente desde el servicio, que es básicamente lo mismo que hace Power BI Desktop.

Las herramientas externas pueden conectarse a la instancia de Analysis Services administrada por Power BI Desktop a través de un número de puerto específico asignado por Power BI Desktop. Cuando se inicia una herramienta directamente desde la cinta de opciones "Herramientas externas" de Power BI Desktop, este número de puerto se pasa a la herramienta externa como argumento de la línea de comandos. En el caso de Tabular Editor, esto hace que el Data model se cargue en Tabular Editor.

<img class="noscale" src="~/content/assets/images/external-tool-architecture.png" />

Una vez conectada a la instancia de Analysis Services, una herramienta externa puede obtener información sobre los metadatos del modelo, ejecutar consultas DAX o MDX contra el Data model e incluso aplicar cambios a los metadatos del modelo mediante [bibliotecas cliente proporcionadas por Microsoft](https://docs.microsoft.com/en-us/analysis-services/client-libraries?view=asallproducts-allversions). En este sentido, la instancia de Analysis Services administrada por Power BI Desktop no se diferencia de cualquier otro tipo de instancia de Analysis Services.

## Operaciones de modelado compatibles

A partir de la actualización de Power BI Desktop de junio de 2025, ya no hay operaciones de escritura no compatibles. En otras palabras, las herramientas de terceros ahora pueden modificar libremente cualquier aspecto del modelo semántico hospedado en Power BI Desktop, incluida la adición y eliminación de tablas y columnas, el cambio de tipos de datos, etc. Sin embargo, si estás usando una versión de Power BI Desktop anterior a la actualización de junio de 2025, consulta las limitaciones en el artículo [Limitaciones de Power BI Desktop](xref:desktop-limitations).

Más información en [la entrada oficial del blog](https://powerbi.microsoft.com/en-us/blog/open-and-edit-any-semantic-model-with-power-bi-tools/).
