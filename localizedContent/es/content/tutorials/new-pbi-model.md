---
uid: new-pbi-model
title: Crear un modelo semántico de Power BI
author: Daniel Otykier
updated: 2021-09-06
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Escritorio
          none: true
        - edition: Business
          partial: true
          note: "Solo para los puntos de conexión XMLA de Premium por usuario"
        - edition: Enterprise
          full: true
---

# (Tutorial) Cómo crear tu primer modelo semántico de Power BI

Esta página te guía paso a paso por el proceso de crear un nuevo modelo semántico de Power BI desde cero con Tabular Editor 3.

> [!IMPORTANT]
> La Edición Business de Tabular Editor 3 está limitada a [Power BI Premium por usuario](https://docs.microsoft.com/en-us/power-bi/admin/service-premium-per-user-faq). Para usar una capacidad de Fabric/Power BI Premium o Embedded, debes actualizar a la Edición Enterprise de Tabular Editor 3. En cualquiera de los casos, el Workspace de Power BI en el que se vaya a implementar el modelo semántico debe tener habilitado el [punto de conexión XMLA de lectura/escritura](https://docs.microsoft.com/en-us/power-bi/admin/service-premium-connect-tools#enable-xmla-read-write).
>
> La Edición de escritorio de Tabular Editor 3 no admite modelos semánticos de Power BI.
>
> [Más información](xref:editions).

##### Crear un nuevo modelo semántico

1. En el menú Archivo, elige Nuevo > Modelo... o pulsa `CTRL+N`

![Nuevo modelo](~/content/assets/images/tutorials/new-pbi-model.png)

- Indica un nombre para tu modelo o usa el valor predeterminado. Luego, establece el nivel de compatibilidad en "1609 (Power BI / Fabric)".
- Para obtener la mejor experiencia de desarrollo, marca la opción "Usar base de datos del Workspace". Esto requiere que tengas un Workspace de desarrollo disponible en Power BI, con el punto de conexión XMLA de lectura/escritura habilitado. Al hacer clic en Aceptar, se te pedirá que introduzcas la cadena de conexión del Workspace de Power BI en el que quieres que se cree la base de datos del Workspace.

> [!NOTE]
> Con una base de datos del Workspace, puedes validar Power Query (expresiones M) e importar el esquema de la tabla desde expresiones de Power Query. También puedes actualizar y consultar datos en la base de datos del Workspace, lo que facilita la depuración y las pruebas de tus expresiones DAX.
