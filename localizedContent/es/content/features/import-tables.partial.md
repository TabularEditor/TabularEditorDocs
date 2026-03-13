---
uid: import-tables
title: Importar tablas
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Escritorio
          full: true
        - edition: Negocio
          full: true
        - edition: Empresarial
          full: true
---

Tabular Editor 3 incluye un **Asistente de importación de tablas** que le ayuda a crear un origen de datos en su modelo e importar tablas o vistas desde orígenes de datos relacionales, como una base de datos de SQL Server.

![Asistente para importar tablas](~/content/assets/images/import-tables-wizard.png)

## Tipos de orígenes de datos de TOM

Según su versión de Analysis Services, existen diferentes formas de definir orígenes de datos dentro de los metadatos del modelo:

- **Proveedor (también llamado "Legacy")**: Disponible en todas las versiones de Analysis Services y en cualquier nivel de compatibilidad. Admite un conjunto limitado de orígenes, principalmente relacionales, a través de controladores OLE DB/ODBC. Las particiones suelen definirse mediante una instrucción SQL, que se ejecuta de forma nativa contra el origen. Las credenciales se administran en el objeto origen de datos del proveedor en el Tabular Object Model y se almacenan y cifran del lado del servidor.
- **Estructurado (también conocido como Power Query)**: Disponible desde SQL Server 2017 (nivel de compatibilidad 1400+). Admite una gama más amplia de orígenes de datos que los proveedores Legacy. Las particiones suelen definirse mediante expresiones M (Power Query). Las credenciales se administran en el objeto origen de datos estructurado en el Tabular Object Model y deben especificarse en cada despliegue en Analysis Services.
- **Orígenes de datos implícitos**: Se usan exclusivamente en los modelos semánticos de Power BI. No se crea ningún objeto de origen de datos explícito en el modelo. En su lugar, la expresión M (Power Query) define implícitamente el origen de datos. Las credenciales no se almacenan en el Tabular Object Model, sino que las gestiona Power BI Desktop o el servicio Power BI.

> [!NOTE]
> El Asistente para importar tablas y la función Actualizar esquema de tabla de Tabular Editor 2.x solo admiten orígenes de datos Legacy con particiones SQL. En otras palabras, no hay compatibilidad con particiones de Power Query. Por este motivo, suelen recomendarse los orígenes de datos heredados, ya que proporcionan el mayor nivel de interoperabilidad entre las herramientas de desarrollo.

## Importación de nuevas tablas

Al importar tablas (menú Modelo > Importar tablas...), Tabular Editor te muestra las opciones mencionadas anteriormente (para crear un nuevo origen de datos), además de una lista de los orígenes de datos ya presentes en el modelo. Evita crear nuevos orígenes de datos si las tablas que quieres importar ya están disponibles en alguno de los orígenes de datos especificados en el modelo.

> [!TIP]
> Por lo general, un modelo semántico se considera una caché semántica optimizada en memoria de un almacén de datos relacional. Por este motivo, lo ideal es que un modelo solo contenga un único origen de datos, que apunte a un almacén de datos basado en SQL o a un data mart.

## Crear un nuevo origen de datos

Si necesitas crear un nuevo origen de datos, Tabular Editor te ofrece una lista de orígenes de datos compatibles:

![Crear nuevo origen](~/content/assets/images/create-new-source.png)

Ten en cuenta que, en particular, Analysis Services y Power BI admiten una gama mucho más amplia de orígenes de datos. Sin embargo, los que aparecen en la captura de pantalla anterior son aquellos a los que Tabular Editor puede conectarse para importar automáticamente los metadatos de la tabla (es decir, los nombres de las columnas y los tipos de datos). Para los orígenes de datos que no figuran en esta lista, Tabular Editor 3 aún puede [actualizar el esquema de la tabla mediante Analysis Services](#updating-table-schema-through-analysis-services).

Actualmente, Tabular Editor 3 admite de forma nativa los siguientes orígenes de datos:

- Bases de datos de SQL Server
- Bases de datos de Azure SQL
- Azure Synapse Analytics (SQL pool y SQL pool sin servidor)
- Oracle
- ODBC
- OLE DB
- Snowflake\*
- Dataflow de Power BI\*
- Databricks\*
- Lakehouse de Fabric\*
- Warehouse de Fabric\*
- Base de datos SQL de Fabric\*
- Base de datos reflejada de Fabric\*

\*=Estos orígenes de datos solo se admiten como orígenes de datos implícitos en los modelos de datos de Power BI. No están disponibles en SSAS / Azure AS.

> [!TIP]
> Para obtener más información sobre cómo conectarse a Azure Databricks, consulte [Conectarse a Azure Databricks](xref:connecting-to-azure-databricks).

Después de elegir uno de los orígenes de datos de la lista, Tabular Editor muestra un cuadro de diálogo con los detalles de conexión, que le permite especificar direcciones de servidor, credenciales, etc., específicos del origen de datos que desea crear. La configuración que especifique debe ser la que Tabular Editor use para establecer una conexión local con el origen. Estos ajustes se guardan en tus @user-options.

![Autenticación SQL](~/content/assets/images/sql-auth.png)

Si desea que Analysis Services use credenciales diferentes al conectarse, puede especificarlo editando las propiedades del origen de datos en el Tabular Object Model después de importar las tablas.

## Seleccionar objetos para importar

Una vez definido su origen de datos, tiene la opción de elegir tablas/vistas de una lista o especificar una consulta nativa que se ejecutará en el origen.

![Opciones de origen](~/content/assets/images/source-options.png)

Si selecciona la primera opción, Tabular Editor se conectará al origen y mostrará una lista de tablas y vistas que podrá previsualizar en la página siguiente:

![Elegir objetos de origen](~/content/assets/images/choose-source-objects.png)

Puede importar varias tablas/vistas a la vez marcándolas en el lado izquierdo. Para cada tabla/vista, puede deseleccionar o seleccionar las columnas que desea importar.

> [!TIP]
> Si tiene el control del origen, recomendamos crear siempre una vista sobre las tablas que desee importar. En la vista, asegúrese de corregir cualquier nombre, ortografía, etc., que se vaya a usar en el modelo semántico, y elimine las columnas que el modelo semántico no necesite (columnas del sistema, marcas de tiempo, etc.).
>
> Luego, en el modelo, importe todas las columnas de esta vista (básicamente generando una instrucción `SELECT * FROM ...`). Esto facilita el mantenimiento, ya que solo necesita ejecutar una actualización de esquema en Tabular Editor para comprobar si se ha cambiado algo en el origen.

![Importación avanzada](~/content/assets/images/advanced-import.png)

Si cambia el modo de vista previa a "Solo esquema" usando el menú desplegable de la esquina superior izquierda, puede cambiar el tipo de datos importado y el nombre de la columna de cada columna de origen. Esto puede ser útil, por ejemplo, si el origen usa valores de coma flotante, pero desea que los datos se importen como decimal fijo.

![Confirmar selección](~/content/assets/images/confirm-selection.png)

En la última página, confirme su selección y elija qué tipo de particiones desea crear. Para los orígenes de datos del proveedor, el tipo de partición que se crea de forma predeterminada es `SQL`, mientras que para los orígenes de datos estructurados, es `M`.

![Confirm Selection Direct Lake](~/content/assets/images/confirm-selection-direct-lake.png)

Para los orígenes de datos de Fabric, en la última página hay una lista desplegable que le permite elegir si desea que su selección se cree como Direct Lake o modo de importación.

En este punto, debería ver sus tablas importadas con todas las columnas, los tipos de datos y las asignaciones de columnas de origen aplicadas:

![Import Complete](~/content/assets/images/import-complete.png)

# Actualización del esquema de tabla

Si se agregan o cambian columnas en el origen, o si ha modificado recientemente una expresión de partición o una consulta, puede usar la característica **Actualizar esquema de tabla** de Tabular Editor para actualizar los metadatos de las columnas en su modelo.

![Update Table Schema](~/content/assets/images/update-table-schema.png)

Esta opción del menú se puede invocar a nivel de modelo, así como en una colección de tablas o incluso en particiones individuales de una tabla.

Al usar esta opción, Tabular Editor se conectará a todos los orígenes de datos pertinentes (solicitando credenciales cuando sea necesario) para determinar si es necesario agregar nuevas columnas o si alguna columna existente debe modificarse o eliminarse.

> [!IMPORTANT]
> Si una columna que se importó anteriormente en su modelo semántico se ha quitado o se ha cambiado de nombre en el origen, debe actualizar el esquema de la tabla en su modelo semántico. De lo contrario, las operaciones de actualización de datos pueden fallar.

![Diálogo de comparación de esquema](~/content/assets/images/schema-compare-dialog.png)

En la captura de pantalla anterior, Tabular Editor detectó algunas columnas nuevas, un cambio de tipo de datos y dos columnas cuyo nombre se cambió en el origen. Ten en cuenta que la detección de un cambio de nombre de columna solo funciona para cambios simples. En otros casos, un cambio de nombre suele hacer que Tabular Editor detecte la eliminación de una columna y la adición de otra; es lo que ocurre con la columna `Tax Amount` que aparece a continuación, que parece haberse renombrado a `TaxAmt` en el origen.

Para evitar que se rompan las fórmulas DAX existentes que dependen de la columna `[Tax Amount]`, puedes mantener pulsada la tecla Ctrl y hacer clic en las dos filas del cuadro de diálogo Cambios de esquema y, a continuación, hacer clic con el botón derecho para combinar la eliminación y la adición de la columna en una única operación de actualización de SourceColumn:

![Combinar actualización de SourceColumn](~/content/assets/images/combine-sourcecolumn-update.png)

Si no quieres que el cambio de nombre se propague a la columna importada (y solo quieres actualizar la propiedad SourceColumn para reflejar el nombre cambiado en el origen de datos), puedes desmarcar la operación de actualización `Name` en el menú desplegable:

![Deselect Name](~/content/assets/images/deselect-name.png)

## Actualizar el esquema de la tabla mediante Analysis Services

De forma predeterminada, Tabular Editor 3 intenta conectarse directamente al origen de datos para actualizar el esquema de la tabla importada. Naturalmente, esto solo funciona cuando el origen de datos es compatible con Tabular Editor 3. Si necesitas actualizar el esquema de una tabla importada desde un origen de datos que no es compatible con Tabular Editor 3, puedes habilitar la opción **Usar Analysis Services para la detección de cambios** en **Herramientas > Preferencias > Comparación de esquema**. Esto también se aplica cuando la expresión M de una partición o una expresión compartida es demasiado compleja para la función integrada de detección de esquema de Tabular Editor 3. Por ejemplo, la detección de esquema integrada no admite determinadas funciones M.

![Actualizar el esquema de la tabla mediante As](~/content/assets/images/update-table-schema-through-as.png)

Cuando esta opción está habilitada y Tabular Editor 3 está conectado a Analysis Services o al punto de conexión XMLA de Power BI, puedes actualizar el esquema de tablas importadas desde **cualquier** origen de datos compatible con Analysis Services o Power BI.

> [!NOTE]
> La opción **Usar Analysis Services para la detección de cambios** solo funciona mientras Tabular Editor 3 está conectado a Analysis Services o al punto de conexión XMLA de Power BI. Por este motivo, recomendamos que los desarrolladores usen siempre el [modo del área de trabajo](xref:workspace-mode) al desarrollar modelos.

Cuando la opción **Usar Analysis Services para la detección de cambios** está habilitada, Tabular Editor 3 utilizará la siguiente técnica cuando se solicite una actualización del esquema:

1. Se crea una nueva transacción en la instancia de Analysis Services a la que se está conectado
2. Se agrega una nueva tabla temporal al modelo. Esta tabla usa una expresión de partición de Power Query que devuelve el esquema de la expresión original, para la que se solicitó una actualización del esquema. Esto se hace mediante la [función M `Table.Schema`](https://docs.microsoft.com/en-us/powerquery-m/table-schema).
3. La tabla temporal se actualiza mediante Analysis Services. Analysis Services se encarga de conectarse al origen de datos para obtener el esquema actualizado.
4. Tabular Editor 3 consulta el contenido de la tabla temporal para obtener los metadatos del esquema.
5. La transacción se revierte, dejando la base de datos de Analysis Services o el modelo semántico de Power BI en el estado original en el que se encontraba antes del paso 1.
6. Tabular Editor 3 muestra el cuadro de diálogo "Aplicar cambios de esquema" como se muestra arriba, por si hubiera cambios en el esquema.

Con esta técnica, Tabular Editor 3 permite importar y actualizar tablas desde orígenes de datos que, de otro modo, no son compatibles, independientemente de la complejidad y del uso de funciones en las consultas M que hay detrás de las tablas.

> [!NOTE]
> Si sus expresiones M combinan datos de varios orígenes, por ejemplo, mediante la función M [`Table.NestedJoin`](https://learn.microsoft.com/en-us/powerquery-m/table-nestedjoin), es posible que tenga que cambiar el [**Nivel de privacidad**](https://powerbi.microsoft.com/en-us/blog/privacy-levels-for-cloud-data-sources/) de "Privado" a "Organizacional" en el modelo semántico del servicio de Power BI. De lo contrario, es posible que vea un error que indique que `<Query> hace referencia a otras consultas o pasos, por lo que es posible que no pueda acceder directamente a un origen de datos. Por favor, vuelva a crear esta combinación de datos`. Este error también puede producirse aunque **Usar Analysis Services para la detección de cambios** no esté habilitado, ya que Tabular Editor 3 volverá automáticamente a este mecanismo de detección cuando la expresión M sea demasiado compleja para la detección de esquema integrada de Tabular Editor 3.

### Importación de nuevas tablas a través de Analysis Services

Para importar una tabla desde un origen de datos que, de otro modo, no es compatible, puede copiar una tabla existente de ese origen de datos, modificar la expresión M en la consulta de la partición de la tabla copiada y, a continuación, guardar los cambios en la base de datos del espacio de trabajo y actualizar el esquema de la tabla, como se ha descrito anteriormente.
