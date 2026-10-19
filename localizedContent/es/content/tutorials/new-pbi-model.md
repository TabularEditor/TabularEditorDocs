---
uid: new-pbi-model
title: Crear un modelo semántico de Power BI
author: Daniel Otykier
updated: 2026-10-12
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          partial: true
          note: "Premium Per User XMLA Endpoints Only"
        - edition: Enterprise
          full: true
---
# (Tutorial) Creación de su primer modelo semántico de Power BI

Esta página te guía a través del proceso de creación de un nuevo modelo semántico de Power BI desde cero utilizando Tabular Editor 3.

> [!IMPORTANT]
> Tabular Editor 3 Edición Business está limitado a [Power BI Premium por usuario](https://learn.microsoft.com/fabric/enterprise/powerbi/service-premium-per-user-faq). Para la capacidad de Fabric, Power BI Premium o Embedded, debe actualizar a Tabular Editor 3 Edición Enterprise. En cualquier caso, el área de trabajo de destino debe permitir el [acceso de lectura/escritura XMLA](https://learn.microsoft.com/fabric/enterprise/powerbi/service-premium-connect-tools#enable-xmla-read-write), que es el valor predeterminado en todos los SKU de capacidad desde junio de 2025.
>
> Tabular Editor 3 Desktop Edition no es compatible con los modelos semánticos de Power BI.
> 
> [Más información](xref:editions).

## Creación de un nuevo modelo semántico

1. En el menú Archivo, seleccione Nuevo > Modelo... o pulse «CTRL+N».

![Nuevo modelo](~/content/assets/images/tutorials/new-pbi-model.png)

- Proporcione un nombre para su modelo o use el valor predeterminado. A continuación, establezca el nivel de compatibilidad como «1706 (Power BI / Fabric)».
- Para disfrutar de la mejor experiencia de desarrollo, marque la opción «Usar base de datos del área de trabajo». Para ello, debes tener un área de trabajo de desarrollo disponible en Power BI, con la lectura/escritura de XMLA habilitada. Cuando haga clic en «Aceptar», se le pedirá que introduzca la cadena de conexión del área de trabajo de Power BI en la que desea que se cree la base de datos del área de trabajo.

> [!NOTE]
> Con una base de datos de área de trabajo, puede validar Power Query (expresiones M) e importar el esquema de tabla desde expresiones de Power Query. También puede actualizar y consultar datos en la base de datos del área de trabajo, lo que facilita la depuración y la prueba de sus expresiones DAX.
