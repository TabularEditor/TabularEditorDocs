# Tabular Editor 3 BETA-16.6

> [!IMPORTANT]
> Hay disponible una versión más reciente de Tabular Editor. Puedes encontrar la versión más reciente [aquí](https://docs.tabulareditor.com/references/release-notes).

- Descarga [Tabular Editor 3 BETA-16.6](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-16.6.x86.msi)
- Descarga [Tabular Editor 3 BETA-16.6 (64 bits)](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-16.6.x64.msi)

## Actualizaciones de BETA-16.6:

- Se corrigió un problema con el botón "Add" del editor de colecciones "Group By Columns".
- Se cambió el nivel de compatibilidad predeterminado de los nuevos conjuntos de datos de Power BI a 1560.
- Permite crear nuevos objetos a nivel de tabla (medidas, columnas, jerarquías) cuando el objeto seleccionado actualmente es, a su vez, un objeto a nivel de tabla.

## Actualizaciones de BETA-16.5:

- Ahora el instalador debería registrar correctamente Tabular Editor 3 como herramienta externa de Power BI Desktop
- Se agregó la opción de CLI "-nosplash", que se usa cuando Power BI Desktop inicia Tabular Editor 3, ya que la pantalla de presentación a veces podía provocar que Tabular Editor 3 quedara "oculto" detrás de Power BI Desktop. Después de actualizar Tabular Editor 3, asegúrate de reiniciar Power BI Desktop.
- Los enlaces de descarga ahora usan nuestra CDN de Azure, donde alojaremos los binarios de Tabular Editor 3 a partir de ahora. Las siguientes direcciones URL siempre apuntan a la versión más reciente de Tabular Editor 3:
  - https://cdn.tabulareditor.com/files/latest/TabularEditor.3.x86.msi
  - https://cdn.tabulareditor.com/files/latest/TabularEditor.3.x64.msi

## Actualizaciones de BETA-16.4:

Se avecina una lista bastante grande de correcciones de errores y pequeñas mejoras:

### Mejoras generales:

- El nombre del archivo .pbix ahora se usa como nombre de la base de datos al guardar un modelo .pbix como un archivo .bim o una estructura de carpetas.
- Se añadió soporte para x64 (tanto las compilaciones x64 como x86 tienen como destino "Any CPU", pero en esta última está establecido el indicador "Prefer32Bits")
- Se actualizó el instalador. Ahora usa WiX, lo que garantiza que el registro y la carpeta local de datos de la aplicación se limpien correctamente al desinstalar el producto. Además, se ve mejor :-)
- El grabador de macros ahora permite registrar la mayoría (¿todos?) de los cambios del modelo que se pueden realizar desde la interfaz de usuario
- Se agregó compatibilidad con predicados escalares de varias columnas, que es una nueva sintaxis de DAX añadida recientemente. Tabular Editor intenta deducir qué versión de Analysis Services se está usando a partir de los metadatos del modelo, pero como esto no siempre es posible (p. ej., al trabajar sin conexión), puedes cambiar manualmente cómo Tabular Editor trata las expresiones de filtro de tabla del predicado escalar de varias columnas en Herramientas > Preferencias > Editor de DAX > General > Funcionalidades del motor semántico).
- Se actualizó TOM a la versión 19.18.0.

### Mejoras de usabilidad:

- Se amplió la "hitbox" de la flecha de expandir/contraer en el Explorador TOM (ver [este comentario](https://github.com/TabularEditor3/PublicPreview/issues/81#issuecomment-789637586))
- Al hacer doble clic en el icono junto a un objeto en el Explorador TOM, ahora se muestra el Editor de expresiones de DAX.

### Correcciones de errores:

- Se corrigió un problema del analizador semántico de DAX que provocaba mensajes de error "fantasma" en determinadas expresiones
- Se corrigió el problema #75
- Se corrigió el problema #77
- Se corrigió el problema #84
- Se corrigieron varios bloqueos en base a la telemetría. @**Everyone**: Sigan enviando esos Report de errores cuando se produzca una excepción y, por favor, incluyan descripciones - ¡son inestimables cuando intentamos averiguar qué salió mal! ¡Gracias!

## Actualizaciones en BETA-16.3:

- Se ha cambiado el nombre de "Acciones personalizadas" a "macros".
  - Hay una nueva ventana que te permite administrar todas las macros definidas actualmente. Edita una macro existente haciendo doble clic en un elemento.
  - Una vez que un C# Script se guarda como una macro, el documento actualizará la macro en los guardados posteriores (Ctrl+S). Usa Archivo > Guardar como... si necesitas guardar el script como un archivo.
  - Las macros pueden tener nombres idénticos. Se distinguen internamente mediante un identificador asignado automáticamente.
  - Se corrigió un problema que impedía que se guardara una macro
- El menú Ventana ahora también incluye un submenú "Nuevo", con los mismos elementos de menú que "Archivo > Nuevo"
- Las barras de herramientas y los menús inactivos ahora se ocultan de forma predeterminada para reducir el desorden en la interfaz de usuario (se puede cambiar en Herramientas > Preferencias > Interfaz de usuario).
- Se corrigió un error en el analizador de DAX que hacía que `GENERATESERIES` devolviera una tabla con una columna con un nombre incorrecto, posiblemente relacionado con el #61
- Corrección del problema #74 (bloqueo al llamar a EndBatch() antes de BeginBatch())
- Se añadió una advertencia y se actualiza el árbol TOM local al guardar en la base de datos, si se realizaron cambios en los metadatos del modelo implementado fuera de Tabular Editor

## Actualizaciones en BETA-16.2:

- La Vista previa de tabla ahora puede actualizarse automáticamente, igual que las consultas DAX o Pivot Grid (ver el problema #73)
- Se corrigió un error que impedía que la Vista previa de tabla mostrara una tabla calculada que no se había actualizado
- Compatibilidad con Scripts DAX para crear columnas calculadas y tablas calculadas
- Ahora los Scripts DAX se pueden ejecutar parcialmente (ver el problema #69). Al editar un Script DAX, deberían activarse 4 botones en la barra de herramientas "Script DAX". Estos botones tienen los siguientes accesos directos:
  - `F5` aplicará el script completo.
  - `Shift+F5` aplicará el script completo y también sincronizará la base de datos conectada.
  - `F8` aplicará solo la selección actual.
  - `Shift+F8` aplicará la selección actual y sincronizará la base de datos conectada.
- Se agregó una marca de agua a la Vista de diagrama para guiar a los usuarios sobre cómo agregar tablas al diagrama (ver el problema #76)
- El análisis de procedimientos recomendados en segundo plano ya no debería bloquear la interfaz de usuario (ver el problema #79)
- Los botones de la barra de herramientas y las opciones del menú contextual para ignorar reglas u objetos en la vista del Best Practice Analyzer ahora deberían funcionar correctamente
- El formulario "por favor, espere" ya no debería superponerse a ningún cuadro de diálogo generado desde un C# Script
- Varias correcciones de errores (posiblemente relacionadas con el problema #74)

## Actualizaciones en BETA-16.1:

- Las medidas ahora usan un icono de "calculadora" para alinear mejor la experiencia con Power BI Desktop. Los iconos de los elementos de cálculo también se han modificado ligeramente, para que se distingan de las medidas.
- Las columnas clave ahora se muestran en **negrita**
- Se han añadido las opciones de refactorización "Definir medida" y "Medida en línea"
- Se ha mejorado el comportamiento del autocompletado en torno a las instrucciones DEFINE / EVALUATE de las consultas DAX. Por ejemplo, ahora el autocompletado también puede sugerir medidas, columnas y tablas definidas dentro de la consulta.
- El autocompletado ahora también sugiere medidas para el parámetro Name de funciones como SUMMARIZECOLUMNS, ADDCOLUMNS, etc., y completa de una vez los parámetros Name y Expression:
  ![autocomplete names](https://user-images.githubusercontent.com/8976200/107629428-66aada80-6c62-11eb-91e4-d5528947840a.gif)
- Revisado el #42.
- El Asistente de implementación ahora guarda las preferencias de implementación (destino + opciones) en el archivo .tmuo que se encuentra junto al archivo Model.bim o Database.json en el disco. Esto facilita las implementaciones al cambiar entre distintos modelos cuando cada modelo se implementa siempre en el mismo destino.
- TOM actualizado a 19.16.3. Debería corregir el problema #63.
- Corregido el problema #64.
- Se ha corregido un error por el que los archivos de modelo aparecían en el menú "Archivos recientes".

## Actualizaciones en BETA-16.0:

- Asistente de implementación actualizado. También corrige los problemas #42 y #43.
- Compatibilidad con la sintaxis DEFINE COLUMN y TABLE en las consultas DAX
- El menú Archivo ahora tiene un submenú "Archivos recientes" y otro "Modelos tabulares recientes". El primero contiene referencias a los 10 Scripts DAX, diagramas de modelo, consultas DAX y C# Scripts más recientes que se guardaron o abrieron. El segundo contiene referencias a los 10 archivos de modelo más recientes (bim / pbit / carpeta).
- Corregido el problema #67
- Corregido el problema #66
