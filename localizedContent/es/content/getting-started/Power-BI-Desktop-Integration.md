---
uid: desktop-integration
title: Integración con Power BI Desktop
author: Morten Lønskov
updated: 2026-09-23
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

[Power BI Desktop admite Herramientas externas](https://docs.microsoft.com/power-bi/create-reports/desktop-external-tools), lo que permite a Tabular Editor realizar operaciones de modelado al trabajar con datos importados o en modo DirectQuery en Power BI Desktop.

![Tabular Editor 3 iniciado desde la cinta de opciones Herramientas externas de Power BI Desktop, con una medida abierta en el Editor de expresiones](~/content/assets/images/getting-started/power-bi-desktop-integration.png)

## Requisitos previos

- [Power BI Desktop](https://www.microsoft.com/en-us/download/details.aspx?id=58494) (julio de 2020 o posterior)
- [La versión más reciente de Tabular Editor](https://tabulareditor.com/downloads)

Además, se recomienda encarecidamente que la opción [fecha/hora automática](https://docs.microsoft.com/power-bi/transform-model/desktop-auto-date-time) esté **desactivada** (configuración de Power BI Desktop en "Carga de datos").

## Arquitectura de herramientas externas

Cuando un Report de Power BI Desktop contiene un Data model (una o varias tablas en modo Import o DirectQuery), Power BI Desktop aloja ese Data model en una instancia local de Analysis Services. Las herramientas externas se conectan a esta instancia.

> [!IMPORTANT]
> Los Reports de Power BI Desktop que usan una **Live Connection** a SSAS, Azure AS o a un Dataset en un Workspace de Power BI no contienen un Data model, y las herramientas externas como Tabular Editor **no pueden** conectarse a ellos.

> [!IMPORTANT]
> Los Reports de Power BI Desktop que editan directamente un modelo **Direct Lake** u otro modelo de Fabric no contienen un Data model. Tabular Editor abre el modelo desde el servicio, igual que Power BI Desktop.

Power BI Desktop asigna un número de puerto a la instancia de Analysis Services. Cuando se inicia una herramienta desde la cinta **Herramientas externas**, Power BI Desktop le pasa el número de puerto como argumento de línea de comandos y Tabular Editor carga el Data model.

<img class="noscale" src="~/content/assets/images/external-tool-architecture.png" />

Una vez conectada a la instancia de Analysis Services, una herramienta externa puede obtener información sobre los metadatos del modelo, ejecutar consultas DAX o MDX sobre el Data model e incluso aplicar cambios a los metadatos del modelo mediante las [bibliotecas cliente proporcionadas por Microsoft](https://docs.microsoft.com/analysis-services/client-libraries?view=asallproducts-allversions). En este sentido, la instancia de Analysis Services administrada por Power BI Desktop no se diferencia de cualquier otro tipo de instancia de Analysis Services.

## Operaciones de modelado compatibles

A partir de la actualización de junio de 2025 de Power BI Desktop, las herramientas externas pueden cambiar cualquier parte del modelo semántico alojado en Power BI Desktop, lo que incluye agregar y quitar tablas y columnas y cambiar tipos de datos. Para versiones anteriores de Power BI Desktop, consulta [Limitaciones de Power BI Desktop](xref:desktop-limitations) y [la entrada oficial del blog](https://powerbi.microsoft.com/en-us/blog/open-and-edit-any-semantic-model-with-power-bi-tools/).
