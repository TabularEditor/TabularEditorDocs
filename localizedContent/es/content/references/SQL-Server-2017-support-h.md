# Soporte para SQL Server 2017

A partir de la versión 2,3, Tabular Editor ahora también es compatible con SQL Server 2017 (nivel de compatibilidad 1400). Esto significa que la interfaz de usuario de Tabular Editor expone parte de la nueva funcionalidad descrita [aquí](https://blogs.msdn.microsoft.com/analysisservices/2017/04/19/whats-new-in-sql-server-2017-ctp-2-0-for-analysis-services/).

Sin embargo, ten en cuenta que necesitas descargar la [compilación adecuada de Tabular Editor](https://github.com/TabularEditor/TabularEditor/releases/tag/2.5-CL1400), versión 2,5-CL1400, para usar estas funciones. Esto se debe a que Microsoft proporciona un nuevo conjunto de bibliotecas cliente para SQL Server 2017 / SSDT 17,0, y estas bibliotecas son incompatibles con la compilación de Tabular Editor para SQL Server 2016. Las nuevas bibliotecas se pueden obtener a través de la nueva [versión de SSDT](https://docs.microsoft.com/en-us/sql/ssdt/download-sql-server-data-tools-ssdt) (requiere Visual Studio 2015).

Si no necesitas las funciones del nivel de compatibilidad 1400, aún puedes usar la compilación de SQL Server 2016 de [Tabular Editor](https://github.com/TabularEditor/TabularEditor/releases/tag/2.5), versión 2,5.

A continuación tienes un resumen rápido de cómo se usan las nuevas características en Tabular Editor:

## Relaciones de fechas

Todas las relaciones ahora muestran la propiedad "Join on Date Behavior" en la cuadrícula de propiedades:

![imagen](~/content/assets/images/sql-server-2017-support-01.png)

## Variaciones (reutilización de columna/jerarquía)

Puedes configurar variaciones en una columna expandiendo la propiedad "Variaciones" en la cuadrícula de propiedades:

![imagen](~/content/assets/images/sql-server-2017-support-02.png)

Ten en cuenta que también puedes especificar **Seguridad de nivel de objeto** a nivel de columna.

Al hacer clic en el botón de puntos suspensivos, se abre el Editor de la colección de variaciones, desde donde puedes configurar cómo se vuelven a mostrar las columnas y las jerarquías en Power BI:

![imagen](~/content/assets/images/sql-server-2017-support-03.png)

Recuerda establecer la propiedad "Show As Variations Only" en "True" a nivel de tabla:

![imagen](~/content/assets/images/sql-server-2017-support-04.png)

Las **Expresiones de fila de detalle** se pueden establecer directamente en tablas y medidas. Sin embargo, por ahora no hay resaltado de sintaxis ni IntelliSense.

Los objetos de jerarquía exponen una nueva propiedad **Ocultar miembros**, que resulta útil para jerarquías irregulares.
