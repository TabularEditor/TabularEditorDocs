---
uid: import-tables
title: Importar tablas
author: Morten Lønskov
updated: 2026-10-12
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
El **Asistente para la importación de tablas** de Tabular Editor 3 crea un origen de datos en su modelo e importa tablas y vistas de orígenes relacionales, como una base de datos de SQL Server.

![Asistente para la importación de tablas](~/content/assets/images/import-tables-wizard.png)

## Tipos de orígenes de datos TOM

Los tipos de fuentes de datos disponibles en los metadatos del modelo dependen de su versión de Analysis Services:

- **Proveedor (heredado)**: disponible en todas las versiones de Analysis Services y en todos los niveles de compatibilidad. Admite una gama limitada de orígenes, principalmente orígenes relacionales a través de controladores OLE DB y ODBC. Las particiones suelen ser instrucciones SQL que se ejecutan de forma nativa contra el origen. Las credenciales se gestionan en el objeto de origen de datos del proveedor en el Tabular Object Model y se almacenan y cifran en el lado del servidor.
- **Estructurado (Power Query)**: disponible a partir de SQL Server 2017 (nivel de compatibilidad 1400 y superior). Admite más orígenes que los orígenes de datos de proveedor. Las particiones suelen ser expresiones M (Power Query). Las credenciales se gestionan en el objeto de origen de datos estructurado del Tabular Object Model, y usted las especifica de nuevo en cada implementación en Analysis Services.
- **Implícita**: utilizada solo por los modelos semánticos de Power BI. El modelo no tiene ningún objeto de origen de datos, y la expresión M (Power Query) define el origen de datos. Power BI Desktop o el servicio Power BI gestionan las credenciales, y el Tabular Object Model no las almacena.

> [!NOTE]
> El Asistente para importar tablas y la función Actualizar esquema de tabla en Tabular Editor 2.x solo admiten orígenes de datos heredados con particiones SQL, no particiones Power Query. Si los desarrolladores del modelo también utilizan Tabular Editor 2.x, utilice orígenes de datos heredados.

## Importación de nuevas tablas

**Modelo > Importar tablas...** enumera los tipos de orígenes de datos anteriores para un nuevo origen de datos, seguidos de los orígenes de datos que ya están en el modelo. Si las tablas que quieres importar están disponibles a través de un origen de datos existente, selecciona ese origen de datos.

> [!TIP]
> Un modelo semántico suele ser una caché en memoria de un almacén de datos relacional. Siempre que sea posible, asigne al modelo un único origen de datos que apunte al almacén de datos o al data mart basado en SQL.

## Creación de una nueva Data source

Cuando creas una nueva Data source, el asistente muestra una lista de las fuentes que admite Tabular Editor 3:

![Crear nuevo origen](~/content/assets/images/create-new-source.png)

Analysis Services y Power BI admiten más orígenes que los que aparecen en esta lista. La lista contiene los orígenes a los que Tabular Editor se conecta directamente para importar los metadatos de las tablas (nombres de columnas y tipos de datos). Para otros orígenes, Tabular Editor 3 puede [actualizar el esquema de tabla a través de Analysis Services](#updating-table-schema-through-analysis-services).

Cada origen tiene su propio cuadro de diálogo de conexión y sus propias opciones de autenticación, documentadas en su página, incluidas las opciones que abren un inicio de sesión interactivo. Los orígenes marcados como *solo implícitos* solo están disponibles como orígenes de datos implícitos en los modelos de Power BI, no en SSAS ni en Azure Analysis Services. Consulte @connectivity para saber cómo se almacenan y se usan las credenciales.

- Bases de datos de SQL Server, bases de datos de Azure SQL y Azure Synapse Analytics (pool de SQL y pool de SQL sin servidor): @connect-sql-server
- Oracle: @connect-oracle
- ODBC, incluidos PostgreSQL, MySQL, MariaDB e IBM Db2: @connect-odbc
- OLE DB: @connect-oledb
- Snowflake, solo implícito, incluida la autenticación con par de claves: @connect-snowflake
- Flujo de datos de Power BI, solo implícito: @connect-dataflows
- Databricks, solo implícito: @connect-databricks y el tutorial [Conexión a Azure Databricks](xref:connecting-to-azure-databricks)
- Microsoft Fabric Lakehouse, Microsoft Fabric Warehouse, Microsoft Fabric SQL Database y Microsoft Fabric Mirrored Database: @connect-onelake

El cuadro de diálogo de conexión recoge la dirección del servidor, las credenciales y otras configuraciones del origen. Tabular Editor utiliza estos ajustes para su propia conexión con el origen y los guarda por usuario y por modelo en su archivo @user-options. Las credenciales se cifran con la API de protección de datos de Windows en su cuenta de usuario de Windows y nunca forman parte de los metadatos del modelo.

![Autenticación SQL](~/content/assets/images/sql-auth.png)

Para proporcionar credenciales diferentes a Analysis Services, edite las propiedades del origen de datos en el Tabular Object Model después de importar las tablas.

## Elegir objetos para importar

Después de definir el origen de datos, elige tablas y vistas de una lista o escribe una consulta nativa para ejecutarla contra el origen.

![Opciones de origen](~/content/assets/images/source-options.png)

Con la primera opción, Tabular Editor se conecta al origen y enumera sus tablas y vistas, que puede previsualizar en la página siguiente:

![Elegir objetos de origen](~/content/assets/images/choose-source-objects.png)

Seleccione varias tablas y vistas de la izquierda para importarlas todas a la vez. Para cada una, selecciona o desmarca las columnas que quieres importar.

> [!TIP]
> Si controla el origen, cree una vista sobre cada tabla que importe. En la vista, corrija los nombres y la ortografía que usa el modelo semántico y elimine las columnas que no necesita, como las columnas del sistema y las marcas de tiempo.
>
> En el modelo, importe todas las columnas de la vista, lo que genera una sentencia `SELECT * FROM ...`. Cuando cambia el origen, **Actualizar esquema de tabla...** en Tabular Editor muestra qué ha cambiado.

![Importación avanzada](~/content/assets/images/advanced-import.png)

Cuando establece el modo de vista previa en **Solo esquema** en el menú desplegable de la esquina superior izquierda, puede cambiar el tipo de datos importado y el nombre de columna de cada columna de origen. Por ejemplo, importe valores de origen de punto flotante como decimales fijos.

![Confirmar selección](~/content/assets/images/confirm-selection.png)

En la última página, confirme su selección y elija el tipo de partición que desea crear. El valor predeterminado es `SQL` para los orígenes de datos de proveedor y `M` para los orígenes de datos estructurados.

![Confirmar selección Direct Lake](~/content/assets/images/confirm-selection-direct-lake.png)

En el caso de los orígenes de datos de Fabric, un menú desplegable en la última página determina si la selección se crea en modo Direct Lake o en modo Importación.

El asistente crea las tablas con todas las columnas, los tipos de datos y las asignaciones de columnas de origen. Las columnas se crean en el orden en que aparecen en la tabla de origen:

![Importación completada](~/content/assets/images/import-complete.png)

> [!NOTE]
> Las tablas importadas desde un **Microsoft Fabric Lakehouse** o un **Microsoft Fabric Warehouse** leen su esquema a través del punto de conexión de análisis SQL del origen de datos. Si Tabular Editor no puede determinar el punto de conexión y los ajustes de importación no especifican ninguno, un error indica lo que falta: el punto de conexión SQL como servidor, o un ID de área de trabajo y un ID de elemento. En ese caso, Tabular Editor no crea una tabla sin columnas.

## Actualizar esquema de tabla

**Actualizar esquema de tabla...** actualiza los metadatos de las columnas de su modelo después de que se añadan o cambien columnas en el origen, o después de que usted modifique una expresión de partición o una consulta.

![Actualizar esquema de tabla](~/content/assets/images/update-table-schema.png)

Ejecútela en el modelo, en una selección de tablas o en particiones individuales.

Tabular Editor se conecta a los orígenes de datos pertinentes, solicita las credenciales cuando es necesario y determina qué columnas hay que añadir, modificar o eliminar. Después de la actualización, las columnas mantienen el orden de las columnas del origen.

> [!IMPORTANT]
> Si una columna importada a tu modelo semántico se ha eliminado o se le ha cambiado el nombre en el origen, actualiza el esquema de tabla. Hasta que lo hagas, la actualización de datos fallará.

![Cuadro de diálogo de comparación de esquema](~/content/assets/images/schema-compare-dialog.png)

En la captura de pantalla anterior, Tabular Editor detectó dos nuevas columnas de origen que aún no se han importado (`Color` y `Material`) y marcó dos columnas existentes para su eliminación (`Colour` y `Substance Type`), porque sus nombres ya no coinciden con ninguna columna de origen. La detección de cambios de nombre solo funciona para cambios simples. En este caso, `Colour` se ha renombrado como `Color` y `Substance Type` como `Material` en el origen, pero los nombres difieren lo suficiente como para que Tabular Editor considere cada cambio de nombre como una eliminación y una adición.

Mantenga pulsada la tecla **Ctrl**, seleccione las filas `Color` (importar) y `Colour` (eliminar) en el cuadro de diálogo Cambio de esquema y, a continuación, haga clic con el botón derecho para combinar la eliminación y la adición en una sola actualización de SourceColumn. Las fórmulas DAX existentes que hacen referencia a `[Colour]` siguen funcionando:

![Combinar actualización de SourceColumn](~/content/assets/images/combine-sourcecolumn-update.png)

Si desea actualizar solo la propiedad `SourceColumn` y conservar el nombre de la columna importada, desmarque la operación de actualización `Name` en el menú desplegable:

![Deseleccionar nombre](~/content/assets/images/deselect-name.png)

## Actualización del esquema de tabla a través de Analysis Services

De forma predeterminada, Tabular Editor 3 se conecta directamente al origen de datos para actualizar el esquema de la tabla importada, lo que solo funciona con los orígenes que admite Tabular Editor 3. Habilite **Usar Analysis Services para detección de cambios** en **Herramientas > Preferencias > Comparación de esquemas** para actualizar el esquema de una tabla de un origen no compatible. La opción también cubre las particiones y las expresiones compartidas cuyo M sea demasiado complejo para la detección de esquemas integrada, por ejemplo, las expresiones que utilizan funciones M que no admite.

![Actualización del esquema de tabla a través de AS](~/content/assets/images/update-table-schema-through-as.png)

Cuando la opción está habilitada y Tabular Editor 3 está conectado a Analysis Services o al punto de conexión XMLA de Power BI, puedes actualizar el esquema de las tablas importadas desde **cualquier** origen de datos compatible con Analysis Services o Power BI.

> [!TIP]
> El [modo de espacio de trabajo](xref:workspace-mode) mantiene Tabular Editor 3 conectado a Analysis Services o al punto de conexión XMLA de Power BI mientras realiza el desarrollo.

Con la opción habilitada, una actualización de esquema ejecuta estos pasos:

1. Tabular Editor 3 inicia una transacción con la instancia de Analysis Services conectada.
2. Añade una tabla temporal al modelo, con una expresión de partición de Power Query que devuelve el esquema de la expresión original a través de la [función M [`Table.Schema`](https://docs.microsoft.com/powerquery-m/table-schema).
3. Analysis Services actualiza la tabla temporal, conectándose al origen de datos para recuperar el esquema.
4. Tabular Editor 3 consulta la tabla temporal para obtener los metadatos del esquema.
5. Tabular Editor 3 revierte la transacción, lo que devuelve la base de datos de Analysis Services o el modelo semántico de Power BI a su estado anterior al paso 1.
6. Si el esquema ha cambiado, aparecerá el cuadro de diálogo **Aplicar cambios de esquema** que se muestra arriba.

> [!NOTE]
> Si sus expresiones M combinan datos de varios orígenes, por ejemplo, a través de la función M [`Table.NestedJoin`](https://learn.microsoft.com/powerquery-m/table-nestedjoin), es posible que deba cambiar el [**Nivel de privacidad**](https://powerbi.microsoft.com/blog/privacy-levels-for-cloud-data-sources/) de «Privado» a «Organizacional» en el modelo semántico del servicio Power BI. De lo contrario, es posible que vea un error que indique que `<Query> references other queries or steps, so it may not directly access a data source. Please rebuild this data combination.`. Este error también puede producirse incluso si no está habilitada la opción **Usar Analysis Services para detección de cambios**, ya que Tabular Editor 3 recurrirá automáticamente a este mecanismo de detección cuando la expresión M sea demasiado compleja para la detección de esquemas integrada de Tabular Editor 3.

### Importación de nuevas tablas a través de Analysis Services

Para importar una tabla desde un origen que el asistente no admite, copie una tabla existente de ese origen y modifique la expresión M de la partición de la copia. Guarde los cambios en la base de datos del área de trabajo y, a continuación, actualice el esquema de tabla como se ha descrito anteriormente.
