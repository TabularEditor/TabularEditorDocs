---
uid: new-as-model
title: Crear un modelo de Analysis Services
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
          note: "Limited to SQL Server Standard Edition"
        - edition: Enterprise
          full: true
---
# (Tutorial) Creación de su primer modelo de Analysis Services

Esta página te guía a través del proceso de creación de un nuevo modelo tabular de Analysis Services desde cero utilizando Tabular Editor 3.

> [!NOTE]
> Tabular Editor 3 Edición Business está limitado a [SQL Server Edición Standard](https://docs.microsoft.com/analysis-services/analysis-services-features-supported-by-the-editions-of-sql-server-2016?view=asallproducts-allversions#tabular-models) y al [nivel básico de Azure Analysis Services](https://docs.microsoft.com/azure/analysis-services/analysis-services-overview#basic-tier). Tenga en cuenta que ciertas funciones de modelado no son compatibles con estos niveles.

## Creación de un nuevo modelo

- En el menú Archivo, seleccione Nuevo > Modelo... o pulse `CTRL+N`. 

![Nuevo modelo](~/content/assets/images/new-as-model-new-model.png)

- Proporcione un nombre para su modelo o use el valor predeterminado. El nombre que introduzca se utilizará para el nombre de la base de datos, el ID de la base de datos y el nombre del modelo. A continuación, elija el nivel de compatibilidad para la versión de Analysis Services a la que se dirige. El cuadro de diálogo muestra estas opciones:
  - 1200 (Azure Analysis Services / SQL Server 2016 o posterior)
  - 1400 (Azure Analysis Services / SQL Server 2017 o posterior)
  - 1500 (Azure Analysis Services / SQL Server 2019+)
  - 1600 (Azure Analysis Services / SQL Server 2022 o posterior)
  - 1700 (Azure Analysis Services / SQL Server 2025 o posterior)
  - 1706 (Power BI / Fabric)

  1700 es el nivel más alto que admite Analysis Services. Use 1706 solo para Power BI y Fabric, por ejemplo, cuando implemente el modelo a través del punto de conexión XMLA de Power BI.

- Para disfrutar de la mejor experiencia de desarrollo, marque la opción «Usar base de datos del área de trabajo». Esto requiere que tengas disponible una instancia de Analysis Services en la que se implementará la base de datos de tu área de trabajo. Podría tratarse de una instancia local o remota de SQL Server Analysis Services o de una instancia de Azure Analysis Services. Cuando haga clic en Aceptar, se le pedirá que introduzca la cadena de conexión de la instancia de Analysis Services en la que desea que se cree la base de datos del área de trabajo.

  [Más información sobre las bases de datos del área de trabajo](xref:workspace-mode).

> [!NOTE]
> Con una base de datos de área de trabajo, puede validar Power Query (expresiones M) e importar el esquema de tabla desde expresiones de Power Query. También puede actualizar y consultar datos en la base de datos del área de trabajo, lo que facilita la depuración y la prueba de sus expresiones DAX.

Una vez creado tu modelo, el siguiente paso es añadir una Data source y algunas tablas.

## Agregar un origen de datos y tablas

Antes de poder importar datos a su modelo tabular, debe configurar uno o más orígenes de datos. Localice el Explorador TOM, haga clic derecho en la carpeta «Fuentes de datos» y elija «Crear». Para un modelo que utiliza el nivel de compatibilidad 1400 o superior, tenemos dos opciones: orígenes de datos heredados y orígenes de datos de Power Query. Para obtener más información sobre las diferencias entre estos dos tipos de orígenes de datos, [consulte el blog de Microsoft Analysis Services](https://docs.microsoft.com/archive/blogs/analysisservices/using-legacy-data-sources-in-tabular-1400).

![Añadir origen de datos](~/content/assets/images/new-as-model-add-data-source.png)

En este ejemplo, crearemos un origen de datos de Power Query, que usaremos para importar algunas tablas de una base de datos relacional de SQL Server. Una vez creado el origen de datos, pulse F2 para cambiarle el nombre y configurar el origen de datos utilizando la cuadrícula de propiedades, como se muestra en la siguiente captura de pantalla:

![Establecer propiedades del origen de datos](~/content/assets/images/new-as-model-data-source-properties.png)

En nuestro ejemplo, establecemos las siguientes propiedades:

| Propiedad | Valor |
|---|---|
| Nombre | `AdventureWorks` |
| Protocolo | `tds` |
| Base de datos | `AdventureWorksDW2017` |
| Servidor | `localhost` |
| AuthenticationKind | `ServiceAccount` |

Pulse Guardar (Ctrl+S). Se le pedirá que proporcione una ruta y un nombre de archivo para el archivo Model.bim, que contendrá los metadatos del modelo que ha creado hasta ahora. También puede guardar el modelo como una estructura de carpetas (Archivo > Guardar en carpeta...), lo cual se recomienda si tiene previsto integrar los metadatos de su modelo en un entorno con control de versiones. Si está utilizando una base de datos del área de trabajo, Tabular Editor 3 también sincronizará los metadatos con la instancia conectada de Analysis Services.

A continuación, añade una nueva tabla al modelo haciendo clic con el botón derecho en la carpeta «Tablas» y eligiendo «Crear > Tabla» (también puedes pulsar Alt+5). Ponga un nombre a la tabla; en nuestro ejemplo, `Internet Sales`. Expanda la tabla, localice la partición en la tabla e introduzca la siguiente consulta M como expresión de partición para rellenar la tabla con datos:

```M
let
    Source = #"AdventureWorks",
    Data = Source{[Schema="dbo",Item="FactInternetSales"]}[Data]
in
    Data
```

Esto supone que la base de datos relacional de SQL Server contiene una tabla denominada «FactInternetSales» dentro del esquema «dbo».

![Expresión de partición M](~/content/assets/images/new-as-model-m-partition.png)

A continuación, haga clic con el botón derecho en la tabla recién creada y elija «Actualizar esquema de tabla...». Esto permite que Tabular Editor rellene automáticamente las columnas de la tabla en función de la consulta de la partición.

> [!NOTE]
> Si no está utilizando una base de datos del área de trabajo, esta operación solo está disponible en Tabular Editor versión 3.1.0 o posterior.

![Comparación de esquemas](~/content/assets/images/new-as-model-schema-compare.png)

Pulse «Aceptar» para añadir las columnas a la tabla. Pulse de nuevo Guardar (Ctrl+S). Si está utilizando una base de datos del área de trabajo, puede actualizar la tabla en el servidor y consultar los datos de la tabla una vez que se haya completado la operación de actualización. Para ello, haga clic con el botón derecho en la tabla y elija «Actualizar tabla > Automática (tabla)». Espere a que finalice la operación en la pestaña «Actualización de datos», luego haga clic derecho en la tabla y elija «Vista previa» (también puede hacerlo desde el Explorador TOM) para ver los datos reales de la tabla:

![Actualización de datos](~/content/assets/images/new-as-model-data-refresh.png)

Si la tabla que ha importado es una tabla de dimensiones, le recomendamos que establezca la propiedad «Clave» de la columna de clave primaria de la tabla en «true». Esto facilita la definición de relaciones entre esta tabla y otras, como veremos más adelante.

Repite este proceso para cualquier tabla que quieras importar a tu modelo tabular. No es necesario actualizar los datos de cada tabla uno por uno; en su lugar, puede ejecutar la operación de actualización a nivel de modelo.

## Definición de relaciones

Una vez que hayas importado varias tablas, la forma más fácil de definir las relaciones entre ellas con Tabular Editor 3 es crear un nuevo diagrama. Elija «Archivo > Nuevo > Diagrama». A continuación, seleccione varias tablas a la vez y arrástrelas a la vista de diagrama o haga clic derecho en las tablas y elija "Agregar al diagrama":

![Agregar al diagrama](~/content/assets/images/new-as-model-add-to-diagram.png)

Para crear una relación entre dos tablas, localice la columna de clave externa en la tabla de hechos y «arrastre» esa columna a la columna de clave primaria de la tabla de dimensiones. Pulse «Aceptar» para confirmar la configuración de la relación en el cuadro de diálogo que aparece.

![Vista de diagrama](~/content/assets/images/new-as-model-diagram-view.png)

Cierre la vista de diagrama (no es necesario guardarla, ya que siempre puede reconstruir el diagrama más tarde). Pulse Ctrl+S una vez más para guardar el modelo. Ahora es el momento de añadir algo de lógica empresarial. Si está utilizando una base de datos del área de trabajo, ahora es un buen momento para ejecutar una actualización (automática o calculada) a nivel de modelo, para asegurarse de que las estructuras de soporte de las relaciones se creen en el servidor, lo que hará que el modelo esté en un estado en el que se puedan realizar consultas.

## Añadir medidas

Seleccione una de las tablas en el Explorador TOM y presione Alt+1 (o elija Crear > Nueva medida) para añadir una medida a esa tabla. Ponga un nombre a la medida e indique una expresión DAX para la medida.

![Añadir medida](~/content/assets/images/new-as-model-add-measure.png)

Pulse Ctrl+S para guardar los metadatos del modelo.

Si estás utilizando una base de datos del área de trabajo, ahora puedes probar tu nueva medida directamente dentro de Tabular Editor 3. La forma más fácil de probarla es usando un Pivot Grid. Elija Archivo > Nuevo > Pivot Grid y, a continuación, arrastre la medida recién creada desde el Explorador TOM a la cuadrícula. También puede arrastrar columnas y jerarquías del Explorador TOM al área de Filtro, Fila o Columna del Pivot Grid, para segmentar su medida por diferentes atributos de dimensión:

![Pivot Grid](~/content/assets/images/new-as-model-pivot-grid.png)

Si no has usado una base de datos del área de trabajo, tendrás que implementar tu modelo en una instancia de Analysis Services antes de poder realizar actualizaciones de datos y consultar el modelo.

## Implementación del modelo de datos

Para implementar los metadatos del modelo en cualquier instancia de Analysis Services, haz clic en el menú «Modelo» y elige «Implementar...». Esto abrirá el Asistente de implementación de Tabular Editor 3, que es similar al Asistente de implementación de Tabular Editor 2.X. Sigue las instrucciones de las distintas páginas del asistente para implementar los metadatos del modelo en una instancia de Analysis Services. También puede utilizar el Asistente de implementación para generar un script TMSL/XMLA, que puede entregarse a un administrador del servidor de Analysis Services para su implementación manual.

![Implementación](~/content/assets/images/new-as-model-deployment.png)

Para actualizar y probar la base de datos implementada, puedes utilizar las herramientas estándar de gestión y cliente proporcionadas por Microsoft, o bien puedes utilizar otra instancia de Tabular Editor 3 (suponiendo que tengas acceso administrativo a la instancia de Analysis Services en la que se encuentra el modelo implementado).

El párrafo anterior ofrece una buena razón para utilizar el enfoque de la base de datos del área de trabajo descrito anteriormente. Cuando esté conectado a una base de datos de área de trabajo, podrá realizar todas las operaciones de desarrollo, incluidas la actualización de datos y las pruebas de la lógica empresarial, dentro de la misma instancia de Tabular Editor 3, sin tener que depender de otras herramientas.
