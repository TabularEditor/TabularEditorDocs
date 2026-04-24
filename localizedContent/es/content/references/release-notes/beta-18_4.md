# Tabular Editor 3 BETA-18.4

> [!IMPORTANT]
> Hay disponible una versión más reciente de Tabular Editor. Puedes encontrar la versión más reciente [aquí](https://docs.tabulareditor.com/references/release-notes).

- Descarga [Tabular Editor 3 BETA-18.4](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-18.4.x86.msi)
- Descarga [Tabular Editor 3 BETA-18.4 (64 bit)](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-18.4.x64.msi)

## Nuevas funciones en BETA-18.4:

- Tabular Editor 3 ahora almacenará las credenciales (cifradas) de los Data source en el archivo personal .tmuo. Esto es ideal cuando se usa una base de datos de Workspace, ya que entonces puedes especificar un conjunto de credenciales diferente del definido en el archivo Model.bim. Si usas control de versiones, asegúrate de ignorar la extensión .tmuo. Aunque las credenciales del archivo estén cifradas con la clave de usuario de Windows, la idea es que cada desarrollador pueda tener su propio archivo .tmuo con credenciales y preferencias que solo se le apliquen a él; por lo tanto, este archivo no debe incluirse en el control de versiones.
- Tabular Editor 3 ahora solicita las credenciales que se van a sobrescribir durante una operación de despliegue, así que ya no tienes que establecer las credenciales con otra herramienta después del despliegue. Ten en cuenta que los Data source de Power Query siempre tendrán sus credenciales borradas durante una operación de despliegue, por lo que las credenciales de estos tipos de Data source deben introducirse en cada despliegue.
- Al crear un modelo nuevo, ahora tendrás la opción de conectarte de inmediato a una base de datos de Workspace (recomendado).

## Correcciones de errores en BETA-18.4:

- Se corrigió un problema con los atajos de teclado y ciertas acciones (Deshacer/Rehacer, etc.) que no siempre se activaban al cambiar el foco entre distintos editores.
- El cuadro de diálogo Buscar/Reemplazar ahora tiene un tamaño mínimo para evitar barras de desplazamiento.

## Correcciones de errores en BETA-18.3:

- Se mejoró el rendimiento del analizador semántico en modelos grandes (regresión en BETA-18.x)
- Poner en cola una operación de actualización de datos ya no debería bloquear la interfaz de usuario
- Las teclas (flechas izquierda/derecha y F2 para cambiar el nombre) vuelven a poder usarse para navegar por el árbol de Tabular Explorer

## Correcciones de errores en BETA-18.2:

- El analizador de DAX ahora reconoce correctamente los nombres de objeto que contienen comillas dobles (consulta el problema #22).

## Nuevas funciones en BETA-18.1:

- Actualizar el esquema de la tabla desde orígenes de Power Query (ver más abajo)

## Correcciones de errores en BETA-18.1:

- Tabular Editor ahora recordará la configuración del tema entre actualizaciones
- Se corrigió un error con las etiquetas de linaje que provocaba bloqueos al copiar tablas calculadas o tablas de grupo de cálculo
- Se corrigió un error falso en las funciones DAX COALESCE y COMBINEVALUES
- Se incluyó Microsoft.AnalysisServices.dll en la distribución, lo que debería garantizar que Tabular Editor pueda importar y exportar archivos VPAX correctamente
- Tabular Editor ahora restablecerá automáticamente la conexión con AS para poder actualizar los datos

## Actualizar el esquema de la tabla a partir de orígenes de Power Query

Ya está aquí una nueva versión beta de Tabular Editor 3. Y este me entusiasma de verdad, por un motivo en particular:

Por primera vez, Tabular Editor puede detectar cambios de esquema en los Data sources y las particiones de Power Query. Y no solo para Data sources relacionales, sino para CUALQUIER expresión de Power Query que pueda evaluarse en tu motor de Analysis Services. "¿Pero cómo demonios es posible?!?", quizá estés pensando. Bien, presta mucha atención a esa última frase: "CUALQUIER expresión de Power Query que pueda evaluarse en tu motor de Analysis Services".

Un hecho poco conocido del motor de Analysis Services es que, en realidad, es un sistema transaccional. Esto significa que podemos iniciar una transacción contra una base de datos que ya esté implementada en Analysis Services, hacer cambios de metadatos, actualizar algunos datos, consultar algunos datos y, por último, revertir la transacción, dejando la base de datos en su estado original como si ni siquiera la hubiéramos tocado.

Así que, para detectar cambios de esquema en particiones de Power Query, Tabular Editor 3 ahora añadirá al modelo una tabla temporal oculta y la rellenará usando la función M [`Table.Schema`](https://docs.microsoft.com/en-us/powerquery-m/table-schema) sobre la consulta de origen cuyo esquema queremos detectar. Después, esa tabla temporal se actualiza en el servidor (usando las credenciales que ya están presentes en el servidor para acceder al Data source) - esta actualización solo tarda una fracción de segundo, gracias al plegado de consultas, conocido como query folding, que ocurre dentro del motor M. Por último, Tabular Editor consultará la tabla para leer el esquema, antes de revertir toda la transacción. Por último, Tabular Editor consultará la tabla para leer el esquema, antes de revertir toda la transacción. El resultado:

![image](https://github.com/TabularEditor/TabularEditor3/blob/master/media/update%20schema.gif?raw=true)

La única salvedad es, por supuesto, que Tabular Editor 3 debe estar conectado a una instancia de Analysis Services, pero no importa si el modelo con el que trabajas tiene datos o no, siempre que las credenciales de los Data sources estén almacenadas en AS (y que AS pueda acceder realmente al Data source). Esta técnica es especialmente útil si usas el [modo del área de trabajo](https://docs.tabulareditor.com/Workspace-Database.html) de Tabular Editor 3.

Además de detectar nombres de columna y tipos de datos, Tabular Editor 3 también te permitirá actualizar la propiedad Description desde el origen (si está presente). En orígenes de SQL Server, sería la propiedad extendida MS_Description. Si se cambia el nombre de una columna en el origen, aparecerá en el cuadro de diálogo Aplicar cambios de esquema como una columna para importar y otra para eliminar. Sin embargo, como se muestra en el GIF anterior, si haces Ctrl+clic derecho sobre estos dos cambios de esquema, puedes combinarlos en un único cambio de esquema de "renombrar la columna de origen". La ventaja de este enfoque es que Tabular Editor 3 ajustará automáticamente cualquier expresión DAX que haga referencia a la columna cuyo nombre se haya cambiado.

### Limitaciones de esta versión:

- La opción de comparación de esquema solo está disponible para particiones de Power Query mientras Tabular Editor está conectado a una instancia de Analysis Services
- La comparación de esquema sin conexión solo estará disponible para particiones heredadas (Provider), de forma similar a Tabular Editor 2.X. Sin embargo, esta funcionalidad no está incluida en BETA-18.1, ya que inicialmente busco comentarios sobre la comparación de esquema para particiones de Power Query. Tanto esta característica como el Asistente para importar tablas estarán disponibles en la próxima versión beta.
- Esta funcionalidad también se puede usar en un modelo de Power BI Desktop, pero ten en cuenta que agregar, modificar o eliminar columnas de una tabla no está entre las [operaciones de modelado compatibles para herramientas externas](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-external-tools#data-modeling-operations). Además, ten en cuenta que Power BI Desktop puede estar almacenando en caché los metadatos de ciertos tipos de Data sources, por lo que quizá tengas que actualizar dentro de Power BI Desktop antes de que Tabular Editor pueda detectar los cambios de esquema.
