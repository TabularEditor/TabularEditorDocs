# Tabular Editor 3 BETA-17.4

> [!IMPORTANT]
> Hay una versión más reciente de Tabular Editor disponible. Puedes encontrar la versión más reciente [aquí](https://docs.tabulareditor.com/references/release-notes).

- Descarga [Tabular Editor 3 BETA-17.4](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-17.4.x86.msi)
- Descarga [Tabular Editor 3 BETA-17.4 (64 bits)](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-17.4.x64.msi)

## Novedades en BETA-17.4:

- Se corrigió un problema por el que el analizador semántico de DAX generaba un Report de dependencias circulares falsas en algunas situaciones.
- Los editores de DAX ahora muestran los atajos de teclado en el menú contextual al hacer clic con el botón derecho
- Ahora puedes cerrar el editor de Ver la definición presionando ESC mientras el cursor esté dentro de él. Además, Autocompletar/Calltips ya no deberían mostrarse dentro del editor, ya que por diseño es de solo lectura.
- Ahora puedes especificar la propiedad AlternateOf de BaseColumn al usar la agregación "Count".
- Mejor compatibilidad con cadenas de conexión que apuntan a un Dataset del servicio de Power BI.

## Novedades en BETA-17.3:

- Ahora se pueden arrastrar tablas a la Vista de diagrama (ver #15)
- Ahora las medidas Inline/Define en el modo de script de DAX funcionan como se espera (ver #91)
- El Analizador VertiPaq ahora debería detectar correctamente los cambios del Data model realizados fuera de Tabular Editor al recopilar estadísticas
- Ahora se puede acceder a los datos del Analizador VertiPaq mediante scripts (ver #90): hay un nuevo método global de script, `CollectVertiPaqAnalyzerStats();`, además de dos nuevos métodos de extensión para tablas y columnas: `.GetCardinality()` y `.GetTotalSize()`.
- Varias mejoras en la función de autocompletado. Por ejemplo, al escribir código entre corchetes (ver #92)
- Las dependencias circulares entre objetos con ámbito de consulta en una consulta DAX u objetos con ámbito de script en un script DAX ya no deberían provocar un bloqueo
- Se añadió una nueva opción de autoformato de DAX para controlar si las columnas de extensión siempre se cualifican, incluso cuando el nombre de la tabla está en blanco, como `''[MyExtColumn]`.
- Se corrigió un bloqueo que a veces podía producirse al hacer doble clic en un elemento de la Vista de mensajes
- Se corrigieron los mensajes de error de las funciones ISSELECTEDMEASURE, SELECTEDMEASURE, SELECTEDMEASURENAME y SELECTEDMEASUREFORMATSTRING cuando se usan fuera de un elemento de cálculo o de una expresión de medida.

## Novedades en BETA-17.2:

- Se corrigió un problema con las versiones del ensamblado del Analizador VertiPaq.
- Se añadió el panel "Particiones" al Analizador VertiPaq.
- El instalador ya no eliminará el contenido de la carpeta `%LocalAppData%\TabularEditor3`, lo que permitirá conservar la configuración durante actualizaciones y desinstalaciones.
- Soporte para arrastrar y soltar objetos en los editores de DAX y C# (#15).
- Soporte para arrastrar y soltar texto seleccionado en todos los editores de código. Mantén pulsada la tecla CTRL mientras arrastras para copiar la selección.
- Soporte para los nuevos argumentos OneWay_LeftFiltersRight y OneWay_RightFiltersLeft en la función CROSSFILTER de DAX.
- Se actualizó TOM a 19.20.1.
- Varias mejoras de estabilidad.

## Actualizaciones en BETA-17.1:

![image](https://user-images.githubusercontent.com/8976200/112887423-762b9900-90d3-11eb-8248-d9da55fe8fe3.png)

- Se añadió [Analizador VertiPaq](https://www.sqlbi.com/tools/vertipaq-analyzer/) (puede que tengas que eliminar el archivo Layout.gz en %LocalAppData%\TabularEditor3 y/o restablecer el Workspace predeterminado de la ventana si la nueva vista no aparece en la interfaz)
  - Recopila estadísticas (cardinalidades y tamaños de columnas y tablas), que luego aparecerán en la información sobre herramientas del Explorador TOM, así como al pasar el cursor sobre una referencia de columna o tabla en cualquier editor de DAX.
  - Importar/exportar estadísticas desde/hacia archivos VPAX
  - Cargar un modelo desde un archivo VPAX
- Permitir editar sinónimos
- Incluir SortByColumn en la vista de dependencias

## Correcciones de errores en BETA-17.1:

- Se corrigió un problema por el que, al copiar y pegar configuraciones regionales, se sobrescribían las existentes

## Actualizaciones en BETA-17.0:

- Tabular Editor 3 ahora te permite editar expresiones M y consultas de particiones en el Editor de expresiones principal (ver #2)
- Los 4 tipos de editores de código (DAX, C#, SQL, M) ahora se pueden configurar de forma independiente en Herramientas > Preferencias > Editores de texto (p. ej., números de línea, guías de sangría, espacios en blanco, etc.)
- Los editores de código ahora admiten el pegado múltiple (#87). Puedes desactivar esta función en Herramientas > Preferencias > Editores de texto > General.

## Correcciones de errores en BETA-17.0:

- El grabador de macros ahora genera el código correcto para hacer referencia al objeto original cuando se cambia su nombre.
- La tecla ALT ya no moverá el foco a la barra de menús (esto interfería con la selección en bloque en los editores de texto). En su lugar, puedes usar F10 para cambiar el foco. Las combinaciones ALT+letra pueden seguir usándose para navegar por los menús.
- Tabular Editor 3 ahora gestiona correctamente la propiedad LineageTag, por ejemplo, al copiar una medida en un modelo de Power BI Desktop
- Las macros ahora pueden usar el método FormatDax.
- Varias correcciones de errores de TOMWrapper portadas desde Tabular Editor 2.
- Se corrigió el comportamiento de la cuadrícula de propiedades para elementos de solo lectura (ahora aparecen atenuados en la cuadrícula de propiedades).
- Se añadieron opciones al hacer clic con el botón derecho en ciertas propiedades de la cuadrícula de propiedades (por ejemplo, para añadir/quitar objetos AlternateOf, KPIs y más).
