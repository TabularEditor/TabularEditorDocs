---
uid: deployment
title: Implementación del modelo
author: Morten Lønskov
updated: 2026-10-11
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

# Implementación del modelo

Tabular Editor 3 (Edición Business y Edición Enterprise) puede tomar una copia de los metadatos del modelo semántico cargado actualmente y desplegarla en una instancia de Analysis Services o en el punto de conexión XMLA de Power BI / Fabric.

Para realizar una implementación, inicia el **Asistente de implementación** desde la opción de menú **Modelo > Implementar...**.

> [!NOTE]
> Tabular Editor 3 Edición Business tiene ciertas [limitaciones](xref:editions) con respecto a qué tipo de instancia de Analysis Services, o Workspace de Power BI / Fabric se admite para la conectividad XMLA. Esto también se aplica a la implementación.

## Servidor de destino

En la página **Servidor de destino**, introduzca un nombre de servidor o elija uno de la lista **Servidor** de servidores recientes. Haga clic con el botón derecho en un servidor de la lista para anclarlo en la parte superior de la lista o eliminarlo. La lista se comparte con **Archivo > Abrir > Modelo desde BD...**. Para obtener más información, consulte [Servidores recientes y anclados](xref:xmla-as-connectivity#recent-and-pinned-servers).

## Opciones de implementación

Después de seleccionar el servidor y la base de datos de destino para la implementación, se muestra una lista de **opciones de implementación**, como se ve en la captura de pantalla siguiente.

![Opciones de implementación](~/content/assets/images/deployment-options.png)

Son las siguientes:

- **Implementar la estructura del modelo**: Indica que se implementarán los metadatos del modelo. Si desmarcas esta opción, no podrás realizar la implementación (la opción existe por motivos históricos).
- **Implementar orígenes de datos**: Para los modelos que usan orígenes de datos _explícitos_, esta opción indica si se incluirá algún origen de datos de este tipo en la implementación. Desmarcar esta opción puede ser útil si se han modificado una o varias propiedades de un origen de datos y no tiene intención de implementar estas modificaciones. Por ejemplo, si estás implementando metadatos del modelo desde un entorno de desarrollo a un entorno de pruebas, es posible que quieras conservar las cadenas de conexión, etc. del entorno de destino tal como están. Tenga en cuenta que, por lo general, esta opción no está habilitada para los modelos semánticos de Power BI / Fabric, ya que estos modelos usan orígenes de datos _implícitos_, en los que las credenciales las administra el servicio de Power BI y los detalles de conexión se almacenan en las consultas M de las particiones o en las expresiones compartidas del modelo.
- **Implementar particiones de tablas**: Esta opción indica si se deben implementar las particiones de tablas. En algunos casos, la base de datos de destino puede contener particiones que no están presentes en los metadatos del modelo. Desmarcar esta opción evitará que la implementación modifique cualquier partición existente en el servidor de destino. Si esta opción está seleccionada, Tabular Editor sincronizará las particiones del servidor de destino con los metadatos del modelo. Si hay particiones en el servidor de destino que no estén en los metadatos del modelo, se eliminarán (incluidos los datos que contengan).
  - **Implementar particiones regidas por las Políticas de actualización incremental**: Cuando la opción **Implementar particiones de tabla** está habilitada, tendrá la opción de evitar implementar particiones regidas por las Políticas de actualización incremental. Esto resulta útil cuando tiene un modelo con particiones que se crean automáticamente mediante la [política de actualización incremental](xref:incremental-refresh-about) y quiere implementar todas las particiones excepto las regidas por la política.
- **Implementar expresiones compartidas**: Implementa las expresiones compartidas del modelo, como los parámetros de Power Query y las consultas compartidas. Desmárquela para conservar las expresiones compartidas que existen en la base de datos de destino.
- **Implementar roles del modelo**: Esta opción indica si se deben implementar los roles definidos en el modelo. Al desmarcar esta opción, se mantendrán tal cual los roles existentes en el modelo. Si va a implementar cambios en tablas o columnas del modelo, quizá tenga que revisar la [configuración de RLS u OLS](xref:data-security-about) para asegurarse de que siga siendo válida.
  - **Implementar miembros de roles del modelo**: Esta opción indica si se deben implementar los miembros de los roles. Es habitual administrar los miembros de rol directamente en el servidor, en lugar de hacerlo en los metadatos del modelo. Al desmarcar esta opción, se evitará que la implementación modifique los miembros de rol existentes en el servidor de destino.
- **Implementar metadatos lingüísticos (sinónimos de preguntas y respuestas, instrucciones de IA y esquema de datos de IA)**: Implementa los metadatos lingüísticos de cada configuración regional del modelo. En Power BI, los metadatos lingüísticos de una cultura contienen sus sinónimos de preguntas y respuestas, así como las instrucciones de IA y el esquema de datos de IA configurados con **Preparar datos para IA** en el servicio Power BI. La opción está seleccionada de forma predeterminada. Desmárquela para conservar los metadatos lingüísticos en el modelo semántico de destino cuando vuelva a implementarlos sobre él:
  - Una cultura presente en ambos modelos obtiene las traducciones del modelo y conserva los metadatos lingüísticos del destino.
  - Una cultura que solo existe en el destino se mantiene con sus metadatos lingüísticos y sin sus traducciones.
  - Una cultura que solo existe en el modelo se implementa sin metadatos lingüísticos.

Tabular Editor no actualiza los metadatos lingüísticos conservados, por lo que un esquema de datos de IA conservado puede enumerar tablas o columnas que el modelo implementado ya no contiene.

## Credenciales del Data source

De forma predeterminada, Tabular Editor no guarda contraseñas, claves de cuenta ni otros secretos cuando guarda un modelo en disco. Por lo tanto, un modelo cargado desde un archivo puede tener Data source con un secreto faltante. El asistente de implementación lo comprueba antes de realizar la implementación. Un secreto se considera ausente si está vacío o es `********`. El asistente comprueba:

- un origen de datos del proveedor cuya cadena de conexión contiene una palabra clave de contraseña, como `Password` o `Pwd`,
- un origen de datos del proveedor que suplanta la identidad de una cuenta de Windows específica,
- un origen de datos estructurado que usa autenticación de Windows o de nombre de usuario y contraseña, o una clave de cuenta.

Para cada secreto ausente, el asistente te pide las credenciales que el servidor debe usar para actualizar el modelo. Tabular Editor almacena lo que introduces, cifrado, como una sobrescritura del Data source en el archivo @user-options y lo usa en la siguiente implementación en lugar de volver a pedírtelo.

Si desmarcas **Implementar Data source**, el asistente ejecuta la misma comprobación en los Data source que ya existen en el destino. Si el servidor no devuelve un secreto que uno de ellos necesita, el asistente lo pide en cada implementación, porque esas respuestas no se almacenan.

Los modelos semánticos de Power BI y Fabric no almacenan credenciales en el modelo. En su lugar, las configuras en el modelo semántico en el servicio de Power BI.

## Script de implementación

Durante la implementación, Tabular Editor genera un [script TMSL de CreateOrReplace](https://learn.microsoft.com/analysis-services/tmsl/createorreplace-command-tmsl?view=asallproducts-allversions), que posteriormente se ejecuta en el motor de Analysis Services. El script CreateOrReplace contiene todos los metadatos necesarios para volver a crear el modelo, incluidas tablas, columnas, medidas, relaciones, perspectivas, traducciones, etc. Si el modelo aún no existe en el servidor de destino, se creará. Si el modelo ya existe, los objetos existentes se reemplazarán por los nuevos metadatos especificados en el script.

Si desmarcas una opción en la página **Opciones de implementación**, el script TMSL generado mantiene la definición existente de esos objetos en el destino.
La última página del asistente de implementación, **Resumen de implementación**, enumera las opciones seleccionadas. Haz clic en **Script TMSL** para revisar el script generado antes de implementarlo. **Exportar compilación...** ignora las opciones **Implementar expresiones compartidas** e **Implementar metadatos lingüísticos**.

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