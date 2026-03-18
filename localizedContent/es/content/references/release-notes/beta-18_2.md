# Notas de la versión de Tabular Editor 3 BETA-18.2

> [!IMPORTANT]
> Hay disponible una versión más reciente de Tabular Editor. Puedes encontrar la versión más reciente [aquí](https://docs.tabulareditor.com/references/release-notes).

- Descarga [Tabular Editor 3 BETA-18.2](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-18.2.x86.msi)
- Descarga [Tabular Editor 3 BETA-18.2 (64 bits)](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-18.2.x64.msi)

## Correcciones de errores en BETA-18.2:

- El analizador de DAX ahora reconoce correctamente los nombres de objetos que contienen comillas dobles (consulte el problema #22).

## Novedades en BETA-18.1:

- Actualizar el esquema de la tabla desde orígenes de Power Query (ver más abajo)

## Correcciones de errores en BETA-18.1:

- Tabular Editor ahora recordará la configuración del tema entre actualizaciones
- Se corrigió un error con las etiquetas de linaje que provocaba bloqueos al copiar tablas calculadas o tablas de grupo de cálculo
- Se corrigió una falsa alerta de error en las funciones DAX COALESCE y COMBINEVALUES
- Se incluyó Microsoft.AnalysisServices.dll en la distribución, lo que debería garantizar que Tabular Editor pueda importar/exportar archivos VPAX correctamente
- Tabular Editor ahora restablecerá automáticamente la conexión con AS para actualizar los datos

## Actualizar el esquema de la tabla desde orígenes de Power Query

Ya está aquí una nueva versión beta de Tabular Editor 3. Y esta me entusiasma especialmente por un motivo en particular:

Por primera vez, Tabular Editor ya puede detectar cambios de esquema en los Data sources y las particiones de Power Query. Y no solo para Data sources relacionales, sino para CUALQUIER expresión de Power Query que pueda evaluar tu motor de Analysis Services. «¿Cómo demonios es posible?!?», podrías estar pensando. Pues fíjate bien en esa última frase: «CUALQUIER expresión de Power Query que pueda evaluar tu motor de Analysis Services».

Un dato poco conocido del motor de Analysis Services es que en realidad es un sistema transaccional. Esto significa que podemos iniciar una transacción contra una base de datos que ya está implementada en Analysis Services, hacer algunos cambios de metadatos, actualizar algunos datos, consultar algunos datos y, finalmente, revertir la transacción, dejando la base de datos en su estado original, como si ni la hubiéramos tocado.

Así que, para detectar cambios de esquema en las particiones de Power Query, Tabular Editor 3 ahora agregará al modelo una tabla temporal oculta y la rellenará usando la función M [`Table.Schema`](https://docs.microsoft.com/en-us/powerquery-m/table-schema) en la consulta de origen de la que queremos detectar el esquema. Después, esa tabla temporal se actualiza en el servidor (usando las credenciales que ya están presentes en el servidor para acceder al Data source). Esta actualización solo lleva una fracción de segundo, gracias al plegado de consultas que se realiza dentro del motor M. Por último, Tabular Editor consultará la tabla para leer el esquema, antes de revertir toda la transacción. El resultado:

![image](https://github.com/TabularEditor3/PublicPreview/blob/master/update%20schema.gif?raw=true)

La única salvedad es, por supuesto, que Tabular Editor 3 debe estar conectado a una instancia de Analysis Services, pero no importa si el modelo con el que trabajas contiene datos o no, siempre que las credenciales de los Data source estén almacenadas en AS (y que AS pueda acceder realmente al Data source). Esta técnica es especialmente útil si usas el [modo del área de trabajo](https://docs.tabulareditor.com/Workspace-Database.html) de Tabular Editor 3.

Además de detectar los nombres de las columnas y los tipos de datos, Tabular Editor 3 también te permitirá actualizar la propiedad Description desde el origen (si existe). En orígenes de SQL Server, sería la propiedad extendida MS_Description. Si se cambia el nombre de una columna en el origen, aparecerá en el cuadro de diálogo Aplicar cambios de esquema como una importación de columna y una eliminación de columna. Sin embargo, como se muestra en el GIF anterior, si haces Ctrl + clic derecho sobre estos dos cambios de esquema, puedes combinarlos en un único cambio de esquema: "renombrar columna de origen". La ventaja de este enfoque es que Tabular Editor 3 corregirá automáticamente cualquier expresión DAX que haga referencia a la columna cuyo nombre se ha cambiado.

### Limitaciones de esta versión:

- La opción de comparación de esquema solo está disponible para particiones de Power Query cuando Tabular Editor está conectado a una instancia de Analysis Services
- La comparación de esquema sin conexión solo estará disponible para particiones Legacy (Provider), de forma similar a Tabular Editor 2.X. Sin embargo, esta funcionalidad no está incluida en BETA-18.1, ya que de momento busco comentarios sobre la comparación de esquema para particiones de Power Query. Tanto esta función como el Asistente para importar tablas estarán disponibles en la próxima versión beta.
- Esta característica también se puede usar en un modelo de Power BI Desktop, pero ten en cuenta que agregar/modificar/eliminar columnas en una tabla no está entre las [operaciones de modelado compatibles para Herramientas externas](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-external-tools#data-modeling-operations). Además, ten en cuenta que Power BI Desktop puede estar almacenando en caché los metadatos de ciertos tipos de Data source, por lo que puede que tengas que realizar una actualización dentro de Power BI Desktop antes de que Tabular Editor pueda detectar los cambios de esquema.
