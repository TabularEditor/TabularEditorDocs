---
uid: powerbi-xmla
title: Edición a través del punto de conexión XMLA
author: Daniel Otykier
updated: 2026-06-11
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          partial: true
          note: Solo puntos de conexión XMLA de Premium Per User
        - edition: Enterprise
          full: true
---

# Edición de un modelo semántico de Power BI mediante el punto de conexión XMLA

Puedes usar Tabular Editor 3 para conectarte a un modelo semántico de Power BI publicado en el servicio Power BI a través del [punto de conexión XMLA](https://learn.microsoft.com/en-us/fabric/enterprise/powerbi/service-premium-connect-tools). El punto de conexión XMLA está disponible para los Workspace asignados a una capacidad de Fabric (SKU F), una capacidad de Power BI Embedded (SKU A o EM), una capacidad Premium heredada (SKU P) o una licencia Premium por usuario (PPU).

> [!NOTE]
> Las licencias de Power BI Pro no son suficientes para acceder a los modelos semánticos de Power BI en un Workspace compartido. Se requiere una capacidad de Fabric, una capacidad de Power BI Embedded, una capacidad Premium heredada o una licencia Premium por usuario para tener acceso a XMLA.

## Requisitos previos

Tabular Editor requiere que el punto de conexión XMLA permita tanto el acceso de lectura como el de escritura. Microsoft habilitó de forma predeterminada el acceso de lectura y escritura a XMLA en todas las SKU de capacidad de Fabric y Power BI en junio de 2025. Si no puedes conectarte, pide a [tu administrador de capacidad](https://learn.microsoft.com/en-us/fabric/enterprise/powerbi/service-premium-connect-tools#enable-xmla-read-write) que compruebe la configuración descrita en @xmla-as-connectivity.

> [!IMPORTANT]
> Si usas Tabular Editor 3, ten en cuenta las [limitaciones de licencia](xref:editions) para conectarte al punto de conexión XMLA de Power BI. Necesitas al menos Tabular Editor 3 Business o Edición Enterprise, según el tipo de Workspace de Power BI que uses.

## Limitaciones

Al conectarte a un modelo semántico a través del punto de conexión XMLA, todas las operaciones de modelado de datos compatibles con el [Tabular Object Model (TOM)](https://learn.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) están disponibles para su edición. En otras palabras, las [Limitaciones de Power BI Desktop](xref:desktop-limitations) no se aplican cuando se edita un modelo semántico a través del punto de conexión XMLA del servicio Power BI.

## Flujo de trabajo

El punto de conexión XMLA de Power BI, en esencia, expone una instancia de Analysis Services a la que Tabular Editor puede conectarse. Así, puedes tratar el Workspace de Power BI como el **servidor** de Analysis Services, y cada modelo semántico de Power BI del Workspace como una **base de datos** de Analysis Services. Todas las funciones de modelado y administración de Tabular Editor están disponibles al conectarse al punto de conexión XMLA. Si decides usar Tabular Editor para crear y mantener tus modelos semánticos de Power BI, también deberías plantearte usar algún sistema de control de versiones para los metadatos del modelo.

El flujo de trabajo es el siguiente:

1. Crea un nuevo Data model en Tabular Editor o conéctate a un modelo semántico existente a través del punto de conexión XMLA de Power BI
2. Guarda este modelo como un archivo **Model.bim** o usa la opción [Guardar en carpeta](xref:save-to-folder) de Tabular Editor.
3. Cada vez que quieras hacer cambios en el modelo, carga el archivo o la carpeta que guardaste en el paso 2. La primera vez que lo hagas, decide si quieres usar una [base de datos de Workspace](xref:workspace-mode) o no.
4. Cuando estés listo para publicar tus cambios en el servicio Power BI, realiza un despliegue desde Tabular Editor (**Model > Deploy...**), y así crearás un modelo semántico nuevo o sobrescribirás uno existente en un Workspace de Power BI.

## Pasos siguientes

- @new-pbi-model
- @workspace-mode
- @importing-tables