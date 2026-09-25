---
uid: new-as-model
title: Crear un modelo de Analysis Services
author: Daniel Otykier
updated: 2026-09-14
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
          note: "Limitado a SQL Server Standard Edition"
        - edition: Enterprise
          full: true
---

# (Tutorial) Cómo crear tu primer modelo de Analysis Services

En esta página te guiamos paso a paso por el proceso de crear desde cero un nuevo modelo tabular de Analysis Services con Tabular Editor 3.

> [!NOTE]
> La Edición Business de Tabular Editor 3 se limita a la [edición Standard de SQL Server](https://docs.microsoft.com/en-us/analysis-services/analysis-services-features-supported-by-the-editions-of-sql-server-2016?view=asallproducts-allversions#tabular-models) y al [nivel Basic de Azure Analysis Services](https://docs.microsoft.com/en-us/azure/analysis-services/analysis-services-overview#basic-tier). Ten en cuenta que algunas características de modelado no se admiten en estos niveles.

##### Crear un nuevo modelo

- En el menú Archivo, elige Nuevo > Modelo... o pulsa `CTRL+N`

![New model](~/content/assets/images/new-as-model-new-model.png)

- Indica un nombre para tu modelo o usa el valor predeterminado. Luego, elige el nivel de compatibilidad en función de la versión de Analysis Services a la que apuntas. Tus opciones son las siguientes:

  - 1200 (Azure Analysis Services / SQL Server 2016+)
  - 1400 (Azure Analysis Services / SQL Server 2017+)
  - 1500 (Azure Analysis Services / SQL Server 2019+)
  - 1600 (Azure Analysis Services / SQL Server 2022+)
  - 1700 (Azure Analysis Services / SQL Server 2025+)
  - 1706 (Power BI / Fabric)

  1700 is the highest level Analysis Services supports. 1706 is for Power BI and Fabric only, and is the level to choose when you deploy the model through the Power BI XMLA endpoint.

- Para obtener la mejor experiencia de desarrollo, marca la opción "Usar base de datos del Workspace". Esto requiere que tengas disponible una instancia de Analysis Services en la que se implementará la base de datos del Workspace. Puede ser una instancia local o remota de SQL Server Analysis Services, o una instancia de Azure Analysis Services. Al hacer clic en Aceptar, se te solicitará que introduzcas la cadena de conexión de la instancia de Analysis Services en la que quieres que se cree la base de datos del Workspace.

  [Más información sobre las bases de datos de Workspace](xref:workspace-mode).

> [!NOTE]
> Con una base de datos del Workspace, puedes validar Power Query (expresiones M) e importar el esquema de la tabla desde expresiones de Power Query. También puedes actualizar y consultar datos en la base de datos del Workspace, lo que facilita la depuración y las pruebas de tus expresiones DAX.

Una vez creado el modelo, el siguiente paso es agregar un Data source y algunas tablas.

#### Agregar un Data source y tablas

Antes de poder importar datos a tu modelo tabular, tienes que configurar uno o varios Data sources. Ubica el Explorador TOM, haz clic con el botón derecho en la carpeta "Data sources" y elige "Crear". Para un modelo que use un nivel de compatibilidad 1400 o superior, tienes dos opciones: Legacy y Data sources de Power Query. Para obtener más información sobre las diferencias entre estos dos tipos de Data source, [consulta el blog de Microsoft Analysis Services](https://docs.microsoft.com/en-us/archive/blogs/analysisservices/using-legacy-data-sources-in-tabular-1400).

![Add data source](~/content/assets/images/new-as-model-add-data-source.png)

En este ejemplo, crearemos un Data source de Power Query, que usaremos para importar algunas tablas de una base de datos relacional de SQL Server. Una vez creado el Data source, pulsa F2 para cambiarle el nombre y configúralo con la cuadrícula de propiedades, como se muestra en la captura de pantalla siguiente:

![Set data source properties](~/content/assets/images/new-as-model-data-source-properties.png)

En nuestro ejemplo, establecimos las siguientes propiedades:

| Propiedad          | Valor                  |
| ------------------ | ---------------------- |
| Nombre             | `AdventureWorks`       |
| Protocolo          | `tds`                  |
| Base de datos      | `AdventureWorksDW2017` |
| Servidor           | `localhost`            |
| AuthenticationKind | `ServiceAccount`       |

Haz clic en Guardar (Ctrl+S). Se te pedirá que indiques una ruta y un nombre de archivo para el archivo Model.bim, que contendrá los metadatos del modelo que has creado hasta ahora. También puedes guardar el modelo como una estructura de carpetas (Archivo > Guardar en carpeta...), lo cual se recomienda si piensas integrar los metadatos del modelo en un entorno con control de versiones. Si estás usando una base de datos de Workspace, Tabular Editor 3 también sincronizará los metadatos con la instancia conectada de Analysis Services.

A continuación, añade una nueva tabla al modelo haciendo clic con el botón derecho en la carpeta "Tablas" y eligiendo "Crear > Tabla" (también puedes pulsar Alt+5). Asigna un nombre a la tabla; en nuestro ejemplo, `Internet Sales`. Expande la tabla, localiza la partición de la tabla y proporciona la siguiente consulta M como expresión de la partición, para rellenar la tabla con datos:

```M
let
    Source = #"AdventureWorks",
    Data = Source{[Schema="dbo",Item="FactInternetSales"]}[Data]
in
    Data
```

Esto asume que la base de datos relacional de SQL Server contiene una tabla llamada "FactInternetSales" dentro del esquema "dbo".

![M partition expression](~/content/assets/images/new-as-model-m-partition.png)

A continuación, haz clic con el botón derecho en la tabla recién creada y elige "Actualizar esquema de tabla...". Esto permite que Tabular Editor rellene automáticamente las columnas de la tabla en función de la consulta de la partición.

> [!NOTE]
> Si no estás usando una base de datos de Workspace, esta operación solo está disponible en Tabular Editor, versión 3.1.0 o posterior.

![Schema compare](~/content/assets/images/new-as-model-schema-compare.png)

Haz clic en "Aceptar" para añadir las columnas a la tabla. Haz clic en Guardar de nuevo (Ctrl+S). Si estás usando una base de datos de Workspace, puedes actualizar la tabla en el servidor y explorar los datos de la tabla una vez que finalice la operación de actualización. Para ello, haz clic con el botón derecho en la tabla y elige "Actualizar tabla > Automático (tabla)". Espera a que finalice la operación en la pestaña "Actualización de datos" y, después, haz clic con el botón derecho en la tabla y elige "Vista previa" (también puedes hacerlo desde el Explorador TOM) para ver los datos reales de la tabla:

![Data refresh](~/content/assets/images/new-as-model-data-refresh.png)

Si la tabla que importaste es una tabla de dimensión, recomendamos establecer la propiedad "Key" de la columna de clave principal de la tabla como "true". Esto facilita definir relaciones entre esta tabla y otras, como veremos más adelante.

Repite este proceso con cualquier tabla que quieras importar en tu modelo tabular. No tienes que actualizar los datos de cada tabla una por una; en su lugar, puedes ejecutar la operación de actualización a nivel del modelo.

#### Definición de relaciones

Una vez que hayas importado varias tablas, la forma más sencilla de definir las relaciones entre ellas con Tabular Editor 3 es crear un nuevo diagrama. Elige "File > New > Diagram". Después, selecciona varias tablas y arrástralas a la Vista de diagrama, o haz clic con el botón derecho en las tablas y elige "Add to diagram":

![Add to diagram](~/content/assets/images/new-as-model-add-to-diagram.png)

Para crear una relación entre dos tablas, localiza la columna de clave externa en la tabla de hechos y "arrastra" esa columna hasta la columna de clave primaria de la tabla de dimensiones. Pulsa "OK" para confirmar la configuración de la relación en el cuadro de diálogo que aparece.

![Diagram view](~/content/assets/images/new-as-model-diagram-view.png)

Cierra la Vista de diagrama (no hace falta guardarla, ya que siempre puedes reconstruir el diagrama más adelante). Pulsa Ctrl+S de nuevo para guardar el modelo. Ahora toca añadir algo de lógica de negocio. Si estás usando una Workspace Database, este es un buen momento para ejecutar una actualización ("Automatic" o "Calculate") a nivel del modelo, para asegurarte de que en el servidor se crean las estructuras de soporte para las relaciones y, así, dejar el modelo en un estado consultable.

#### Añadir medidas

Selecciona una de las tablas en el Explorador TOM y pulsa Alt+1 (o elige Create > New Measure) para añadir una medida a esa tabla. Asigna un nombre a la medida y proporciona una expresión DAX para la medida.

![Add measure](~/content/assets/images/new-as-model-add-measure.png)

Pulsa Ctrl+S para guardar los metadatos del modelo.

Si estás usando una Workspace Database, ahora puedes probar tu nueva medida directamente en Tabular Editor 3. La forma más sencilla de probarla es usar un Pivot Grid. Elige File > New > Pivot Grid y, a continuación, arrastra la medida recién creada desde el Explorador TOM a la cuadrícula. También puedes arrastrar columnas y jerarquías desde el Explorador TOM a las áreas Filter, Row o Column del Pivot Grid para segmentar tu medida por distintos atributos de dimensión:

![Pivot Grid](~/content/assets/images/new-as-model-pivot-grid.png)

Si no usaste una Workspace Database, tendrás que desplegar tu modelo en una instancia de Analysis Services antes de poder realizar actualizaciones de datos y consultar el modelo.

#### Implementación del Data model

Para implementar los metadatos del modelo en cualquier instancia de Analysis Services, haz clic en el menú "Modelo" y elige "Implementar...". Esto abre el Asistente de implementación de Tabular Editor 3, similar al Asistente de implementación de Tabular Editor 2.X. Sigue las instrucciones de las distintas páginas del asistente para implementar los metadatos del modelo en una instancia de Analysis Services. También puedes usar el Asistente de implementación para generar un script TMSL/XMLA, que puedes entregar a un administrador del servidor de Analysis Services para que lo implemente manualmente.

![Deployment](~/content/assets/images/new-as-model-deployment.png)

Para actualizar y probar la base de datos implementada, puedes usar las herramientas estándar de administración y cliente proporcionadas por Microsoft, o bien otra instancia de Tabular Editor 3 (siempre que tengas acceso administrativo a la instancia de Analysis Services donde se encuentra el modelo implementado).

El párrafo anterior ofrece un buen motivo para usar el enfoque de la base de datos de Workspace descrito anteriormente. Cuando estés conectado a una base de datos de Workspace, podrás realizar todas las operaciones de desarrollo, incluida la actualización de datos y las pruebas de la lógica de negocio, dentro de la misma instancia de Tabular Editor 3, sin depender de otras herramientas.
