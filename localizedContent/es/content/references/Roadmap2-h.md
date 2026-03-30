# Hoja de ruta

> [!IMPORTANT]
> Tabular Editor 2 ya no está en desarrollo activo y no recibirá nuevas funciones importantes ni grandes mejoras por nuestra parte. Sin embargo, seguimos comprometidos a mantenerlo actualizado, garantizando la compatibilidad con las nuevas funcionalidades de modelado de modelos semánticos a medida que Microsoft las publique y corrigiendo cualquier problema crítico o bloqueante. Como el proyecto es de código abierto bajo la licencia MIT, cualquiera puede enviar pull requests, que nuestro equipo revisará y aprobará. Por lo tanto, la siguiente lista debe considerarse obsoleta.

- Generar scripts de objetos en TMSL o DAX (compatible con el Editor de DAX)
- IntelliSense en el Editor de expresiones DAX
- Crear un complemento para Visual Studio para iniciar Tabular Editor
- Arquitectura de complementos de Tabular Editor / API pública para desarrolladores
- Compilación, pruebas, publicación y documentación automatizadas con VSTS
- [Hecho] Corrección de fórmulas (es decir, corregir automáticamente expresiones DAX al cambiar el nombre de los objetos)
- [Hecho] Interfaz de usuario para mostrar dependencias de objetos
- [Hecho] Generar scripts de los cambios desde la línea de comandos
- [Hecho] Posibilidad de leer/editar más tipos de objetos (tablas, particiones, columnas de datos)
- [Hecho] Dividir un Model.bim en varios archivos json (por ejemplo, un archivo por tabla) para una mejor integración en flujos de trabajo de control de versiones.
- [Hecho] Importar/exportar traducciones

## Generar scripts de objetos en TMSL o DAX

Debería ser posible, al seleccionar uno o varios objetos en el árbol del explorador, generar un script para esos objetos. De hecho, esto ya es posible arrastrando y soltando los objetos en otro editor de texto (o en SSMS), pero debería existir una opción similar al hacer clic con el botón derecho para comunicar con más claridad a los usuarios finales lo que está ocurriendo. Debería ser posible generar tanto scripts TMSL (para SSMS) como código de estilo DAX, que pueda usarse en el [Editor de DAX](https://github.com/DaxEditor/).

Hoy en día, las medidas y las columnas calculadas se pueden arrastrar entre instancias de Tabular Editor para copiarlas entre modelos, pero para exponer mejor esta funcionalidad debería existir una opción en la interfaz de usuario para importar un fragmento de TMSL proporcionado, ya sea desde el portapapeles o desde un archivo. Consulta [esta incidencia](https://github.com/TabularEditor/TabularEditor/issues/69). Por último, deberían habilitarse los atajos estándar de copiar y pegar.

## Crear un complemento para Visual Studio para iniciar Tabular Editor

Una extensión sencilla del menú contextual de Visual Studio que se asegure de que el archivo Model.bim esté cerrado y, a continuación, inicie TabularEditor.exe con el archivo Model.bim cargado.

## IntelliSense en el Editor de expresiones de DAX

Al escribir código DAX en el Editor de expresiones, debería aparecer un cuadro de autocompletado para ayudar a completar nombres de tablas, nombres de columnas, nombres de medidas o funciones (y sus argumentos).

Consulta también [esta incidencia](https://github.com/TabularEditor/TabularEditor/issues/64).

## Arquitectura de complementos de Tabular Editor / API pública para desarrolladores

Quienes prefieren crear scripts de modelos tabulares con C# ya pueden usar TOMWrapper.dll desde hoy, en lugar de usar directamente la API TOM de Analysis Services. Por ejemplo, el espacio de nombres TOMWrapper facilita el trabajo con perspectivas y traducciones, gracias a los métodos y propiedades disponibles.

Yendo un paso más allá, sería interesante exponer más funcionalidades de Tabular Editor a los desarrolladores:

- Análisis sintáctico de objetos DAX
- Acceso a los resultados del Best Practice Analyzer
- IU de Tabular Editor (lo que permite crear "plug-ins" para Tabular Editor, con o sin IU personalizada)

## Compilación, pruebas, publicación y documentación automatizadas con VSTS

DevOps con VSTS y una limpieza general del código fuente de Tabular Editor.

## Corrección automática de fórmulas

Cuando se cambie el nombre de cualquier objeto del modelo, se deben actualizar todas las expresiones DAX que hagan referencia a ese objeto para reflejar el nombre modificado.

**Actualización**: Desde la versión 2.2, esta función ahora se puede activar en "Archivo" > "Preferencias".

## IU para mostrar las dependencias de objetos

Al hacer clic con el botón derecho en una medida o una columna calculada, debería mostrarse un árbol de dependencias en un cuadro de diálogo emergente. Debería ser posible mostrar los objetos que dependen del objeto seleccionado o los objetos de los que depende el objeto seleccionado.

**Actualización**: Desde la versión 2.2, esta función está disponible. Simplemente haz clic con el botón derecho en un objeto y elige "Mostrar dependencias...".

## Aplicar cambios mediante scripts desde la línea de comandos

Hoy en día es posible desplegar un modelo directamente desde la línea de comandos. Del mismo modo, debería ser posible pasar por la canalización un archivo .cs con un C# Script para ejecutarlo en el modelo. Tras ejecutar el script, debería ser posible guardar o desplegar el modelo actualizado. Esto requiere algunos cambios en las opciones actuales de la línea de comandos.

**Actualización**: Desde la versión 2.3, los scripts se pueden ejecutar desde la línea de comandos usando el modificador "-S". El despliegue funciona como siempre, pero si quieres guardar el modelo modificado como un archivo .bim, puedes usar la opción "-B".

## Posibilidad de leer/editar más tipos de objetos

Actualmente, Tabular Editor solo permite a los usuarios finales leer y editar un subconjunto de los objetos del Tabular Object Model. Sería deseable que todos los objetos del árbol del modelo fueran accesibles en Tabular Editor: las relaciones, los KPI, las tablas calculadas y los roles deberían poder editarse directamente. Los Data sources, las tablas, las columnas de datos y las particiones de tabla deberían poder editarse, con ciertas limitaciones (por ejemplo, no deberíamos esperar que Tabular Editor pueda recuperar esquemas de datos a partir de Data sources y consultas arbitrarias).

**Actualización**: A partir de 2,1, muchos tipos de objetos nuevos ahora son visibles directamente en el Tree Explorer. Con el menú contextual, puedes crear, duplicar y eliminar muchos de estos objetos (roles, perspectivas, traducciones). Aún no hay soporte para crear y eliminar relaciones y Data sources, pero llegará en una versión futura.

**Actualización**: A partir de 2,2, ya podemos crear y eliminar relaciones. Se añadirán más tipos de objetos más adelante.

**Actualización**: A partir de 2,3, ya se pueden editar tablas, particiones y columnas de datos. Ahora Visual Studio solo es necesario para crear el modelo en blanco en sí; todo lo demás se puede hacer en Tabular Editor.

**Actualización**: ¡La actualización anterior fue una mentira! Se me olvidaron los KPI, pero a partir de la versión 2,4 ya se pueden crear, editar y eliminar.

## Dividir un Model.bim en varios archivos json

El diseño y la estructura del archivo Model.bim lo hacen terrible para el control de código fuente y la gestión de versiones. No solo se guarda todo el Tabular Object Model en un único archivo; además, el archivo contiene información de "ModifiedTime" por toda la estructura, lo que hace inútiles las operaciones DIFF del control de código fuente.

Para mejorar los flujos de trabajo de gestión de versiones con modelos tabulares, sería interesante que Tabular Editor pudiera guardar y cargar un archivo Model.bim como una estructura de carpetas con archivos individuales para medidas, columnas calculadas, etc. Debería haber opciones de línea de comandos disponibles para exportar e importar archivos Model.bim desde y hacia este formato, y debería ser posible implementar directamente desde este formato (en los casos en los que no necesites el propio archivo Model.bim). Estos archivos individuales deberían contener el mismo JSON que el archivo Model.bim, pero sin la información de "ModifiedTime", para que se puedan usar fácilmente en un sistema de control de versiones y permitir que varios desarrolladores trabajen a la vez en el mismo modelo.

**Actualización**: [Disponible en 2,2](/Advanced-features#folder-serialization).

**Actualización**: A partir de 2,3, existen opciones para almacenar los metadatos de Perspectiva y Traducción como anotaciones en los objetos individuales. Esto es útil en escenarios de control de código fuente con varios desarrolladores, para evitar que un único archivo acumule muchos cambios cuando se modifican traducciones, pertenencias a perspectivas, etc.

## Compatibilidad con Power BI

Hoy en día ya es posible conectar Tabular Editor a un modelo alojado en Power BI Desktop. El enfoque es similar a lo que se [describe aquí para Excel y SSMS](http://biinsight.com/connect-to-power-bi-desktop-model-from-excel-and-ssms/). Al hacerlo, es posible agregar carpetas de visualización al modelo de Power BI Desktop, y se mantienen en Power BI incluso después de guardar y volver a abrir el archivo .pbix. Sin embargo, parece que hay algunos problemas con el nivel de compatibilidad, que convendría revisar antes de continuar.

**Actualización**: A partir de 2,1, Tabular Editor ahora detecta instancias en ejecución de Power BI Desktop y Visual Studio Integrated Workspaces. Puedes conectarte a estas instancias y hacer cambios como lo harías en instancias normales, aunque este enfoque de modificar modelos de Power BI y de Integrated Workspace no está admitido por Microsoft.

## Importar/exportar traducciones

Es una funcionalidad estándar de SSDT, y también sería útil tenerla en Tabular Editor.

**Actualización**: [Disponible en 2,2](/Advanced-features#import-export-translations).
