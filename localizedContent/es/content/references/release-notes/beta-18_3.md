# Tabular Editor 3 BETA-18.3

> [!IMPORTANT]
> Hay disponible una versión más reciente de Tabular Editor. Puedes encontrar la versión más reciente [aquí](https://docs.tabulareditor.com/references/release-notes).

- Descargar [Tabular Editor 3 BETA-18.3](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-18.3.x86.msi)
- Descargar [Tabular Editor 3 BETA-18.3 (64 bits)](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-18.3.x64.msi)

## Correcciones de errores en BETA-18.3:

- Mejora del rendimiento del analizador semántico en modelos grandes (regresión en BETA-18.x)
- Poner en cola una operación de actualización de datos ya no debería bloquear la interfaz de usuario
- Ahora puedes volver a usar las teclas del teclado (flechas izquierda/derecha y F2 para cambiar el nombre) para navegar por el árbol de Tabular Explorer

## Correcciones de errores en BETA-18.2:

- El analizador DAX ahora reconoce correctamente los nombres de objeto que contienen comillas dobles (consulta el problema #22).

## Novedades en BETA-18.1:

- Actualizar el esquema de la tabla desde orígenes de Power Query (ver más abajo)

## Correcciones de errores en BETA-18.1:

- Tabular Editor ahora recordará la configuración del tema entre actualizaciones
- Se corrigió un error con las etiquetas de linaje que provocaba bloqueos al copiar tablas calculadas o tablas de grupos de cálculo
- Se corrigió un falso error en las funciones DAX COALESCE y COMBINEVALUES
- Se incluyó Microsoft.AnalysisServices.dll en la distribución, lo que debería garantizar que Tabular Editor pueda importar y exportar archivos VPAX correctamente
- Tabular Editor ahora restablecerá automáticamente la conexión con AS para la actualización de datos

## Actualizar el esquema de la tabla desde orígenes de Power Query

Ya está disponible una nueva versión beta de Tabular Editor 3. Y esta me entusiasma especialmente, por un motivo concreto:

Por primera vez, Tabular Editor puede detectar cambios de esquema en los Data sources y las particiones de Power Query. Y no solo para Data sources relacionales, sino para cualquier expresión de Power Query que pueda evaluarse con tu motor de Analysis Services. «¿Pero cómo demonios es posible?!?», quizás estés pensando. Bueno, presta mucha atención a esa última frase: «CUALQUIER expresión de Power Query que pueda evaluar tu motor de Analysis Services».

Un dato poco conocido sobre el motor de Analysis Services es que, en realidad, es un sistema transaccional. Esto significa que podemos iniciar una transacción en una base de datos que ya está implementada en Analysis Services, realizar algunos cambios de metadatos, actualizar datos, consultar datos y, por último, revertir la transacción, dejando la base de datos en su estado original, como si ni siquiera la hubiéramos tocado.

Así que, para detectar cambios de esquema en particiones de Power Query, Tabular Editor 3 ahora agregará una tabla temporal oculta al modelo y la rellenará mediante la función M [`Table.Schema`](https://docs.microsoft.com/en-us/powerquery-m/table-schema) sobre la consulta de origen cuyo esquema queremos detectar. Luego, esa tabla temporal se actualiza en el servidor (usando las credenciales que ya están presentes en el servidor para acceder al Data source). Esta actualización solo tarda una fracción de segundo, gracias al plegado de consultas que ocurre dentro del motor M. Por último, Tabular Editor consultará la tabla para leer el esquema, antes de revertir toda la transacción. El resultado:

![image](https://github.com/TabularEditor/TabularEditor3/blob/master/media/update%20schema.gif?raw=true)

La única salvedad, por supuesto, es que Tabular Editor 3 tiene que estar conectado a una instancia de Analysis Services, pero no importa si el modelo con el que estás trabajando contiene datos o no, siempre que las credenciales de los Data sources estén almacenadas en AS (y que AS pueda acceder realmente al Data source). Esta técnica es especialmente útil si usas el [modo del área de trabajo](https://docs.tabulareditor.com/Workspace-Database.html) de Tabular Editor 3.

Además de detectar nombres de columnas y tipos de datos, Tabular Editor 3 también te permitirá actualizar la propiedad Description a partir del origen (si existe). En orígenes de SQL Server, sería la propiedad extendida MS_Description. Si se cambia el nombre de una columna en el origen, aparecerá en el cuadro de diálogo Aplicar cambios de esquema como una importación de columna y otra de eliminación de columna. Sin embargo, como se muestra en el GIF anterior, si haces Ctrl+clic derecho sobre estos dos cambios de esquema, puedes combinarlos en un único cambio de esquema de tipo «renombrar columna de origen». La ventaja de este enfoque es que Tabular Editor 3 corregirá automáticamente cualquier expresión DAX que haga referencia a la columna renombrada.

### Limitaciones de esta versión:

- La opción de comparación de esquema solo está disponible para particiones de Power Query mientras Tabular Editor está conectado a una instancia de Analysis Services
- La comparación de esquema sin conexión solo estará disponible para particiones heredadas (Provider), de forma similar a Tabular Editor 2.X. Sin embargo, esta funcionalidad no está incluida en BETA-18.1, ya que inicialmente busco comentarios sobre la comparación de esquema para particiones de Power Query. Tanto esta funcionalidad como el Asistente para importar tablas estarán disponibles en la próxima versión beta.
- Esta funcionalidad también se puede usar en un modelo de Power BI Desktop, pero ten en cuenta que agregar/modificar/eliminar columnas en una tabla no se incluye entre las [operaciones de modelado compatibles para herramientas externas](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-external-tools#data-modeling-operations). Además, ten en cuenta que Power BI Desktop puede estar almacenando en caché los metadatos de ciertos tipos de Data sources, por lo que quizá tengas que ejecutar una actualización en Power BI Desktop antes de que Tabular Editor pueda detectar los cambios de esquema.
