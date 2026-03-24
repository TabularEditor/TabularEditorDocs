---
uid: implementación
title: Implementación del modelo
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

## Implementación del modelo

Tabular Editor 3 (Edición Business y Edición Enterprise) puede tomar una copia de los metadatos del modelo semántico cargado actualmente y desplegarla en una instancia de Analysis Services o en el punto de conexión XMLA de Power BI / Fabric.

Para realizar una implementación, inicia el **Asistente de implementación** desde la opción de menú **Modelo > Implementar...**.

> [!NOTE]
> Tabular Editor 3 Edición Business tiene ciertas [limitaciones](xref:editions) con respecto a qué tipo de instancia de Analysis Services, o Workspace de Power BI / Fabric se admite para la conectividad XMLA. Esto también se aplica a la implementación.

## Opciones de implementación

Después de seleccionar el servidor y la base de datos de destino para la implementación, se muestra una lista de **opciones de implementación**, como se ve en la captura de pantalla siguiente.

![Opciones de implementación](~/content/assets/images/deployment-options.png)

Son las siguientes:

- **Implementar la estructura del modelo**: Indica que se implementarán los metadatos del modelo. Si desmarcas esta opción, no podrás realizar la implementación (la opción existe por motivos históricos).
- **Implementar orígenes de datos**: Para los modelos que usan orígenes de datos _explícitos_, esta opción indica si se incluirá algún origen de datos de este tipo en la implementación. Desmarcar esta opción puede ser útil si se han modificado una o varias propiedades de un origen de datos y no tiene intención de implementar estas modificaciones. Por ejemplo, si estás implementando metadatos del modelo desde un entorno de desarrollo a un entorno de pruebas, es posible que quieras conservar las cadenas de conexión, etc. del entorno de destino tal como están. Tenga en cuenta que, por lo general, esta opción no está habilitada para los modelos semánticos de Power BI / Fabric, ya que estos modelos usan orígenes de datos _implícitos_, en los que las credenciales las administra el servicio de Power BI y los detalles de conexión se almacenan en las consultas M de las particiones o en las expresiones compartidas del modelo.
- **Implementar particiones de tablas**: Esta opción indica si se deben implementar las particiones de tablas. En algunos casos, la base de datos de destino puede contener particiones que no están presentes en los metadatos del modelo. Desmarcar esta opción evitará que la implementación modifique cualquier partición existente en el servidor de destino. Si esta opción está seleccionada, Tabular Editor sincronizará las particiones del servidor de destino con los metadatos del modelo. Si hay particiones en el servidor de destino que no estén en los metadatos del modelo, se eliminarán (incluidos los datos que contengan).
  - **Implementar particiones regidas por las Políticas de actualización incremental**: Cuando la opción **Implementar particiones de tabla** está habilitada, tendrá la opción de evitar implementar particiones regidas por las Políticas de actualización incremental. Esto resulta útil cuando tiene un modelo con particiones que se crean automáticamente mediante la [política de actualización incremental](xref:incremental-refresh-about) y quiere implementar todas las particiones excepto las regidas por la política.
- **Implementar roles del modelo**: Esta opción indica si se deben implementar los roles definidos en el modelo. Al desmarcar esta opción, se mantendrán tal cual los roles existentes en el modelo. Si va a implementar cambios en tablas o columnas del modelo, quizá tenga que revisar la [configuración de RLS u OLS](xref:data-security-about) para asegurarse de que siga siendo válida.
  - **Implementar miembros de roles del modelo**: Esta opción indica si se deben implementar los miembros de los roles. Es habitual administrar los miembros de rol directamente en el servidor, en lugar de hacerlo en los metadatos del modelo. Al desmarcar esta opción, se evitará que la implementación modifique los miembros de rol existentes en el servidor de destino.

## Script de implementación

Durante la implementación, Tabular Editor genera un [script TMSL CreateOrReplace](https://learn.microsoft.com/en-us/analysis-services/tmsl/createorreplace-command-tmsl?view=asallproducts-allversions), que luego se ejecuta en el motor de Analysis Services. El script CreateOrReplace contiene todos los metadatos necesarios para volver a crear el modelo, incluidas tablas, columnas, medidas, relaciones, perspectivas, traducciones, etc. Si el modelo aún no existe en el servidor de destino, se creará. Si el modelo ya existe, los objetos existentes se reemplazarán por los nuevos metadatos especificados en el script.

Si se desmarcó alguna de las opciones de la página **Opciones de implementación**, Tabular Editor usará la definición de metadatos original de esos objetos en el script TMSL generado, conservando así sus definiciones tal cual en el servidor.

La última página del Asistente de implementación le permite exportar el script generado, para que pueda revisar los cambios antes de ejecutarlos.

## Impacto de la implementación

> [!WARNING]
> Este tipo de implementación es una **implementación solo de metadatos**. Según los tipos de cambios realizados en el modelo, durante la implementación podrían perderse datos importados. En ese caso, puede que tenga que ejecutar una operación de actualización una vez finalizada la implementación.

Como regla general, los siguientes cambios se pueden realizar en el modelo sin necesidad de una actualización de datos posterior:

- Agregar/editar/eliminar medidas y KPIs, incluidas sus expresiones DAX.
- Edición de propiedades como FormatString, Description, DisplayFolder, etc.
- Agregar/editar/quitar traducciones de metadatos, perspectivas y roles de OLS y RLS.

Los siguientes cambios pueden requerir una **actualización de cálculo** antes de poder consultar los objetos:

- Agregar/editar columnas calculadas, tablas calculadas y grupos de cálculo
- Agregar/editar relaciones
- Agregar/editar jerarquías
- Eliminar columnas/tablas

Los siguientes cambios pueden requerir una **actualización completa**:

- Agregar/editar particiones, tablas y columnas

> [!WARNING]
> Debido al posible impacto de desplegar un modelo semántico de esta manera, recomendamos no usar esta opción para realizar un despliegue en un entorno de producción. Es mejor configurar una [canalización de CI/CD para implementar modelos en entornos de producción](https://blog.tabulareditor.com/category/ci-cd/).