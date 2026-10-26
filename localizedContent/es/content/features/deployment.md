---
uid: deployment
title: Implementación de modelo
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

# Implementación de modelo

Tabular Editor 3 (Ediciones Business y Enterprise) puede hacer una copia de los metadatos del modelo semántico cargado actualmente e implementarla en una instancia de Analysis Services o en el punto de conexión XMLA de Power BI / Fabric.

Para realizar una implementación, inicie el **Asistente de implementación** a través de la opción de menú **Modelo > Implementar...**.

> [!NOTE]
> Tabular Editor 3 Business Edition tiene ciertas [limitaciones](xref:editions) en cuanto al tipo de instancia de Analysis Services o de área de trabajo de Power BI / Fabric que se admite para la conectividad XMLA. Esto también se aplica a la implementación.

## Servidor de destino

En la página **Servidor de destino**, introduzca un nombre de servidor o elija uno de la lista **Servidor** de servidores recientes. Haga clic con el botón derecho en un servidor de la lista para anclarlo a la parte superior de la lista o eliminarlo. La lista se comparte con **Archivo > Abrir > Modelo desde BD...**. Para obtener más información, consulte [Servidores recientes y anclados](xref:xmla-as-connectivity#recent-and-pinned-servers).

## Opciones de implementación

Después de seleccionar el servidor de destino y la base de datos que quieres implementar, se te mostrará una lista de **Opciones de implementación**, como se muestra en la siguiente captura de pantalla.

![Opciones de implementación](~/content/assets/images/deployment-options.png)

Estas son:

- **Implementar estructura del modelo**: Indica que se implementarán los metadatos del modelo. Si desmarca esta opción, no podrá realizar la implementación (la opción existe por razones históricas).
- **Implementar orígenes de datos**: para los modelos que utilizan orígenes de datos *explícitos*, esta opción indica si se incluirán dichos orígenes de datos en la implementación. Desmarcar esta opción puede ser útil si se han modificado una o más propiedades de un origen de datos y no tienes intención de implementar estas modificaciones. Por ejemplo, si está implementando metadatos del modelo desde un entorno de desarrollo a un entorno de prueba, es posible que desee conservar las cadenas de conexión, etc., en el entorno de destino tal cual. Tenga en cuenta que esta opción normalmente no está habilitada para los modelos semánticos de Power BI / Fabric, ya que dichos modelos utilizan orígenes de datos *implícitos*, en los que las credenciales son administradas por el servicio Power BI y los detalles de conexión se almacenan en las consultas M de las particiones o en las expresiones compartidas del modelo.
- **Implementar particiones de tabla**: Esta opción indica si deben implementarse las particiones de tabla. En algunos casos, la base de datos de destino puede contener particiones que no están presentes en los metadatos del modelo. Si desmarca esta opción, evitará que la implementación modifique las particiones existentes en el servidor de destino. Si esta opción está marcada, Tabular Editor sincronizará las particiones del servidor de destino con los metadatos del modelo. Si hay particiones en el servidor de destino, pero no en los metadatos del modelo, se eliminarán (incluidos los datos que contengan).
  - **Implementar particiones regidas por directivas de actualización incremental**: Cuando la opción **Implementar particiones de tabla** esté habilitada, tendrá la opción de evitar la implementación de particiones que estén regidas por directivas de actualización incremental. Esto es útil cuando tiene un modelo con particiones creadas automáticamente por la [Política de actualización incremental](xref:incremental-refresh-about) y desea implementar todas las particiones excepto las que se rigen por la política.
- **Implementar expresiones compartidas**: Implementa las expresiones compartidas del modelo, como los parámetros de Power Query y las consultas compartidas. Desmárquela para conservar las expresiones compartidas que existen en la base de datos de destino.
- **Implementar roles de modelo**: Esta opción indica si deben implementarse los roles definidos en el modelo. Si desactiva esta opción, los roles existentes en el modelo se mantendrán tal cual. Si está implementando cambios en tablas o columnas del modelo, es posible que tenga que revisar la [configuración de RLS u OLS](xref:data-security-about) para asegurarse de que sigan siendo válidas.
  - **Implementar miembros de roles de modelo**: Esta opción indica si deben implementarse los miembros de los roles. Es habitual gestionar los miembros de los roles directamente en el servidor, en lugar de hacerlo en los metadatos del modelo. Si desmarca esta opción, evitará que la implementación modifique cualquier miembro de rol existente en el servidor de destino.
- **Implementar metadatos lingüísticos (sinónimos de preguntas y respuestas, instrucciones de IA y esquema de datos de IA)**: Implementa los metadatos lingüísticos de cada configuración regional del modelo. En Power BI, los metadatos lingüísticos de una cultura contienen sus sinónimos de preguntas y respuestas, así como las instrucciones de IA y el esquema de datos de IA configurados con **Preparar datos para IA** en el servicio Power BI. La opción está seleccionada de forma predeterminada. Desactívala para conservar los metadatos lingüísticos en el modelo semántico de destino cuando vuelvas a implementar sobre él:
  - Una cultura presente en ambos modelos obtiene las traducciones del modelo y conserva los metadatos lingüísticos del destino.
  - Una cultura que solo existe en el destino se mantiene con sus metadatos lingüísticos y sin sus traducciones.
  - Una cultura que solo existe en el modelo se implementa sin metadatos lingüísticos.

Tabular Editor no actualiza los metadatos lingüísticos conservados, por lo que un esquema de datos de IA conservado puede enumerar tablas o columnas que el modelo implementado ya no contiene.

## Credenciales del origen de datos

De forma predeterminada, Tabular Editor no guarda contraseñas, claves de cuenta ni otros secretos cuando guarda un modelo en el disco. Por lo tanto, un modelo cargado desde un archivo puede tener orígenes de datos con un secreto faltante. El asistente de implementación comprueba esto antes de realizar la implementación. Un secreto se considera ausente cuando está vacío o es «********». El asistente comprueba:

- un origen de datos de proveedor cuya cadena de conexión contiene una palabra clave de contraseña, como «Password» o «Pwd»,
- un origen de datos del proveedor que suplanta a una cuenta de Windows específica,
- un origen de datos estructurado que utiliza la autenticación de Windows o de nombre de usuario/contraseña, o una clave de cuenta.

Por cada secreto que falte, el asistente le solicitará las credenciales que el servidor debe usar cuando actualice el modelo. Tabular Editor almacena lo que introduce, cifrado, como una anulación de origen de datos en el archivo @user-options, y lo utiliza en la siguiente implementación en lugar de volver a solicitarlo.

Cuando desmarca **Implementar orígenes de datos**, el asistente realiza la misma comprobación en los orígenes de datos que ya existen en el destino. Si el servidor no devuelve un secreto que uno de ellos necesita, el asistente lo solicitará en cada implementación, ya que estas respuestas no se almacenan.

Los modelos semánticos de Power BI y Fabric no almacenan credenciales en el modelo. En su lugar, las estableces en el modelo semántico del servicio Power BI.

## Script de implementación

Durante la implementación, Tabular Editor genera un [script TMSL CreateOrReplace](https://learn.microsoft.com/analysis-services/tmsl/createorreplace-command-tmsl?view=asallproducts-allversions), que luego se ejecuta en el motor de Analysis Services. El script CreateOrReplace contiene todos los metadatos necesarios para recrear el modelo, incluidas tablas, columnas, medidas, relaciones, perspectivas, traducciones, etc. Si el modelo aún no existe en el servidor de destino, se creará. Si el modelo ya existe, los objetos existentes se sustituirán por los nuevos metadatos especificados en el script.

Si desmarcas una opción en la página **Opciones de implementación**, el script TMSL generado mantiene la definición existente de esos objetos en el destino.
La última página del asistente de implementación, **Resumen de implementación**, enumera las opciones seleccionadas. Haz clic en **Script TMSL** para revisar el script generado antes de implementarlo. **Exportar compilación...** ignora las opciones **Implementar expresiones compartidas** e **Implementar metadatos lingüísticos**.

## Impacto de la implementación

> [!WARNING]
> Este tipo de implementación es una **implementación solo de metadatos**. Dependiendo de los tipos de cambios realizados en el modelo, los datos importados podrían perderse durante la implementación. En este caso, es posible que deba ejecutar una operación de actualización una vez completada la implementación.

Como regla general, se pueden realizar los siguientes cambios en el modelo sin necesidad de una actualización posterior de los datos:

- Añadir/editar/eliminar medidas y KPI, incluidas sus expresiones DAX.
- Editar propiedades como FormatString, Description, DisplayFolder, etc.
- Añadir/editar/eliminar traducciones de metadatos, perspectivas y roles OLS y RLS.

Los siguientes cambios pueden requerir una **Actualización de cálculo** antes de que se puedan consultar los objetos:

- Añadir/editar columnas calculadas, tablas calculadas y grupos de cálculos
- Añadir/editar relaciones
- Añadir/editar jerarquías
- Eliminar columnas/tablas

Los siguientes cambios pueden requerir una **actualización completa**:

- Añadir/editar particiones, tablas y columnas

> [!WARNING]
> Debido al impacto potencial de implementar un modelo semántico de esta manera, recomendamos no usar esta opción para realizar una implementación en un entorno de producción. Es mejor configurar una [canalización CI/CD para implementar modelos en entornos de producción](https://blog.tabulareditor.com/category/ci-cd/).