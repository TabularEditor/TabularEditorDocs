# Tabular Editor 3 BETA-18.1

> [!IMPORTANT]
> Hay disponible una versión más reciente de Tabular Editor. Puedes encontrar la versión más reciente [aquí](https://docs.tabulareditor.com/references/release-notes).

- Descargar [Tabular Editor 3 BETA-18.1](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-18.1.x86.msi)
- Descargar [Tabular Editor 3 BETA-18.1 (64 bit)](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-18.1.x64.msi)

## Novedades de esta versión:

- Actualizar el esquema de la tabla desde orígenes de Power Query (ver más abajo)

## Correcciones de errores en esta versión:

- Tabular Editor ahora recordará la configuración de la apariencia entre actualizaciones
- Se corrigió un error con las etiquetas de linaje que provocaba bloqueos al copiar tablas calculadas o tablas de grupo de cálculo
- Se corrigió un falso error en las funciones DAX COALESCE y COMBINEVALUES
- Se incluyó Microsoft.AnalysisServices.dll en la distribución, lo que debería garantizar que Tabular Editor pueda importar y exportar archivos VPAX correctamente
- Tabular Editor ahora restablecerá automáticamente la conexión con AS para actualizar los datos

## Actualizar el esquema de la tabla desde orígenes de Power Query

Ya está aquí una nueva versión beta de Tabular Editor 3. Y esta me entusiasma especialmente por un motivo en particular:

Por primera vez, Tabular Editor ahora puede detectar cambios de esquema en Data sources y particiones de Power Query. Y no solo para Data sources relacionales, sino para CUALQUIER expresión de Power Query que pueda evaluar tu motor de Analysis Services. «¿Cómo demonios es posible?!?», quizá estés pensando. Pues fíjate bien en esa última frase: «CUALQUIER expresión de Power Query que pueda evaluar tu motor de Analysis Services».

Un dato poco conocido del motor de Analysis Services es que, en realidad, es un sistema transaccional. Esto significa que podemos iniciar una transacción sobre una base de datos que ya está implementada en Analysis Services, hacer algunos cambios de metadatos, actualizar datos, consultar datos y, por último, revertir la transacción, dejando la base de datos en su estado original, como si ni la hubiéramos tocado.

Así que, para detectar cambios de esquema en particiones de Power Query, Tabular Editor 3 ahora agregará al modelo una tabla temporal oculta y rellenará esa tabla usando la función M [`Table.Schema`](https://docs.microsoft.com/en-us/powerquery-m/table-schema) sobre la consulta de origen cuyo esquema queremos detectar. Luego, esa tabla temporal se actualiza en el servidor (usando las credenciales que ya están presentes en el servidor para acceder al Data source); esta actualización solo tarda un instante, gracias al plegado de consultas dentro del motor M. Por último, Tabular Editor consultará la tabla para leer el esquema, antes de revertir toda la transacción. El resultado:

![image](https://github.com/TabularEditor3/PublicPreview/blob/master/update%20schema.gif?raw=true)

La única salvedad es, por supuesto, que Tabular Editor 3 debe estar conectado a una instancia de Analysis Services; pero da igual que el modelo con el que estés trabajando contenga datos o no, siempre que las credenciales de los Data source estén almacenadas en AS (y que AS pueda acceder realmente al Data source). Esta técnica es especialmente útil si usas el [modo del área de trabajo](https://docs.tabulareditor.com/Workspace-Database.html) de Tabular Editor 3.

Además de detectar los nombres de las columnas y los tipos de datos, Tabular Editor 3 también te permitirá actualizar la propiedad Description a partir del origen (si existe). En orígenes de SQL Server, sería la propiedad extendida MS_Description. Si se cambia el nombre de una columna en el origen, en el cuadro de diálogo Aplicar cambios de esquema aparecerá como "importar columna" y "eliminar columna". Sin embargo, como se muestra en el GIF anterior, si haces Ctrl+clic derecho en estos dos cambios de esquema, puedes combinarlos en un único cambio de esquema de "cambiar el nombre de la columna de origen". La ventaja de este enfoque es que Tabular Editor 3 corregirá automáticamente cualquier expresión DAX que haga referencia a la columna renombrada.

### Limitaciones de esta versión:

- La opción de comparar esquemas solo está disponible para particiones de Power Query mientras Tabular Editor está conectado a una instancia de Analysis Services
- La comparación de esquemas sin conexión solo estará disponible para particiones heredadas (Provider), de forma similar a Tabular Editor 2.X. Sin embargo, esta funcionalidad no está incluida en BETA-18.1, ya que inicialmente estoy buscando comentarios sobre la comparación de esquemas para particiones de Power Query. Tanto esta función como el Asistente para importar tablas estarán disponibles en la próxima versión beta.
- Esta función también se puede usar en un modelo de Power BI Desktop, pero ten en cuenta que añadir, modificar o eliminar columnas en una tabla no está entre las [operaciones de modelado compatibles para Herramientas externas](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-external-tools#data-modeling-operations). Además, ten en cuenta que Power BI Desktop puede estar almacenando en caché los metadatos de determinados tipos de Data source, por lo que puede que tengas que actualizar en Power BI Desktop antes de que Tabular Editor pueda detectar los cambios de esquema.
