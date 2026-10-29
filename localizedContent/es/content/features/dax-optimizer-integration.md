---
uid: dax-optimizer-integration
title: Integración del Optimizador de DAX
author: Daniel Otykier
updated: 2026-10-11
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# Integración del Optimizador de DAX

> [!NOTE]
> Los usuarios de la **edición Enterprise** de Tabular Editor 3 tienen derecho a acceso gratuito al optimizador de DAX. [Más información](https://blog.tabulareditor.com/2024/10/31/free-dax-optimizer-access-in-tabular-editor-3/)

Tabular Editor 3.18.0 presenta **DAX Optimizer** como una experiencia integrada. [DAX Optimizer](https://daxoptimizer.com) es un servicio que le ayuda a optimizar sus modelos tabulares de SSAS/Azure AS y sus modelos semánticos de Power BI/Fabric. La herramienta combina las [estadísticas del Analizador VertiPaq](https://www.sqlbi.com/tools/vertipaq-analyzer/) con un análisis estático de su código DAX, proporcionando así una lista de recomendaciones priorizadas para ayudarle a identificar rápidamente posibles cuellos de botella en el rendimiento.

> [!IMPORTANT]
> El Optimizador de DAX es un servicio de terceros de pago. Para utilizar la función **Optimizador de DAX** en Tabular Editor 3, necesitará una [cuenta para el Optimizador de DAX](https://www.daxoptimizer.com/free-tour/).

## Introducción en video

Vea a Marco Russo de [SQLBI](https://www.sqlbi.com) presentar la integración de DAX Optimizer en Tabular Editor 3:

<iframe width="640" height="360" src="https://www.youtube-nocookie.com/embed/Z5lZdI79tF8" title="Detectar y solucionar problemas con Tabular Editor 3 y la integración con DAX Optimizer" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Primeros pasos

Para acceder a esta función, vaya al menú **Ver** y seleccione **DAX Optimizer**.

![DAX Optimizer](~/content/assets/images/features/dax-optimizer-view-menu.png)

Se le mostrará una nueva vista similar a la de la siguiente imagen:

![Vista de Dax Optimizer](~/content/assets/images/features/dax-optimizer-view.png)

Para conectar Tabular Editor 3 al servicio del Optimizador de DAX, haga clic en **Conectar...** a través del menú **Opciones**. Se le pedirá que introduzca sus credenciales de Tabular Tools (Optimizador de DAX).

Si deseas **desconectar** o **conectarte con una cuenta diferente**, vuelve al menú **Opciones** y elige la opción **Volver a conectar...**. Si cancela el cuadro de diálogo, se desconectará la sesión actual.

Si desea que Tabular Editor 3 se conecte automáticamente la próxima vez que se inicie la aplicación, puede marcar la opción **Conectar automáticamente** en el menú **Opciones**. Si tienes una cuenta de DAX Optimizer con espacios de trabajo en varias regiones, también puedes elegir a qué región conectarte a través del menú **Opciones**.

Por último, el menú **Opciones** también le permite cambiar a una cuenta diferente en [escenarios de grupo](https://docs.daxoptimizer.com/how-to-guides/managing-groups).

## Exploración de espacios de trabajo y modelos

Una vez establecida la conexión, los menús desplegables de la parte superior de la vista se rellenarán con sus espacios de trabajo, modelos y versiones de modelos existentes. Realice sus selecciones de izquierda a derecha (es decir, elija primero el **Espacio de trabajo**, luego el **Modelo** y, por último, la **Versión**). La vista mostrará un resumen de la versión del modelo seleccionada en ese momento, con información como el tamaño del modelo, el número de tablas, el número de medidas, etc.

![Descripción general del modelo](~/content/assets/images/model-overview.png)

> [!NOTE]
> Tabular Editor 3 le permite cargar archivos VPAX para crear nuevos modelos o versiones de modelos en el servicio del Optimizador de DAX. Sin embargo, si necesita crear o gestionar áreas de trabajo, mover o compartir modelos, etc., tendrá que hacerlo a través de la [interfaz web del Optimizador de DAX](https://app.daxoptimizer.com).

Si una versión del modelo aún no se ha analizado, tendrá la opción de iniciar el análisis. Tenga en cuenta que, dependiendo de su plan de cuenta, es posible que tenga un número limitado de «ejecuciones» disponibles.

Una vez finalizado el análisis, se te mostrará un resumen con el número de problemas detectados. La información que se muestra es similar a la que vería en la interfaz web del Optimizador de DAX.

Vaya a la pestaña **Problemas** o **Medidas** para ver los resultados detallados. Use los encabezados de las columnas para ordenar y filtrar los resultados.

![Problemas de Dax Optimizer](~/content/assets/images/features/dax-optimizer-issues.png)

## Navegar por los problemas y las medidas

Al hacer doble clic en un problema o una medida en la vista detallada que se muestra arriba, accederá a la vista **Resultados del Optimizador de DAX**, donde se muestra la expresión DAX original de la medida, junto con los aspectos destacados de las áreas problemáticas. La lista del lado izquierdo de la pantalla le permite cambiar qué problemas se deben resaltar. Además, puede marcar los problemas como **Corregidos** o **Ignorados** utilizando las casillas de verificación de la lista.

![Resultados del Optimizador de DAX](~/content/assets/images/features/dax-optimizer-results.png)

Haga clic en el botón **Buscar en el Explorador TOM...** en la parte superior derecha de la vista para ir a la medida correspondiente en el modelo cargado actualmente.

Marque la casilla **Seguir Explorador TOM** para mantener el Explorador TOM sincronizado con la medida seleccionada actualmente en la vista Resultados del Optimizador de DAX.

Cuando haga clic en una referencia de medida en el panel de código DAX dentro de la vista **Resultados del Optimizador de DAX**, la vista navegará hasta esa medida. A continuación, puedes usar los botones **Atrás** (Alt+Izquierda) y **Adelante** (Alt+Derecha) para navegar hacia atrás y hacia delante entre las medidas que has visitado.

## Cargar modelos y versiones de modelos

Para cargar estadísticas VPAX al Optimizador de DAX, asegúrese de que Tabular Editor esté conectado actualmente a una instancia de Analysis Services (SSAS, Azure AS, Power BI Desktop o punto de conexión XMLA de Power BI/Fabric). A continuación, seleccione el área de trabajo en el menú desplegable situado en la parte superior izquierda de la vista **Optimizador de DAX**. Haga clic en **Cargar...** dentro del menú **Opciones**.

Se te mostrará un cuadro de diálogo similar al que se muestra a continuación:

![Cargar Vpax](~/content/assets/images/upload-vpax.png)

Aquí puede elegir si el VPAX debe cargarse como un nuevo modelo dentro del área de trabajo o si el VPAX contiene estadísticas actualizadas de un modelo existente.

- Para un **nuevo modelo**, debe proporcionar un nombre y elegir si el VPAX debe [ofuscarse](https://www.sqlbi.com/blog/marco/2024/03/15/vpax-obfuscator-a-library-to-obfuscate-vpax-files/) o no (consulte más abajo para obtener más detalles sobre la ofuscación). También debe elegir bajo qué [contrato](https://docs.daxoptimizer.com/glossary/contract) debe cargarse el modelo. Esto afecta al número y a la frecuencia de las [*ejecuciones*](https://docs.daxoptimizer.com/glossary/run) del Optimizador de DAX que puede realizar posteriormente en el modelo.
- Para una **nueva versión del modelo**, debe seleccionar el modelo existente que desea actualizar.

Una vez que haga clic en el botón **Aceptar**, el archivo VPAX se cargará en el Optimizador de DAX y podrá comenzar a analizar el modelo.

> [!NOTE]
> Si no hay estadísticas del Analizador VertiPaq disponibles en Tabular Editor 3, se recopilan estadísticas del modelo actual antes de cargar el archivo VPAX. Las estadísticas también se vuelven a recopilar si la última recopilación es anterior o igual a la última carga de VPAX para el modelo. Las estadísticas de una carga siempre se leen a partir de los datos del modelo. Si no se pueden leer, la carga no se inicia.

### Ofuscación

De forma predeterminada, los archivos VPAX cargados mediante Tabular Editor 3 se ofuscarán. En **Cargar modelo** puedes activar o desactivar la ofuscación para las nuevas cargas de modelos. Las siguientes cargas de versiones del modelo se ofuscarán o no en función de la carga de la primera versión. También puedes exportar un archivo VPAX ofuscado localmente sin cargarlo al Optimizador de DAX a través de la vista **VertiPaq Analyzer**. En este caso, se genera un archivo de diccionario que se almacena en tu equipo local, junto al archivo .ovpax exportado. Este archivo de diccionario se utiliza para desofuscar el contenido del archivo .ovpax.

Cuando los datos VPAX ofuscados se cargan en el servicio del Optimizador de DAX a través de la vista **Optimizador de DAX**, Tabular Editor realiza automáticamente un seguimiento de los diccionarios de ofuscación almacenándolos en la carpeta `%LocalAppData%\TabularEditor3\DaxOptimizer` de su equipo local. Por lo tanto, al explorar modelos con la función **Optimizador de DAX** en Tabular Editor 3, los modelos se desofuscan automáticamente si se encuentra un diccionario adecuado en esta carpeta, lo que proporciona una experiencia más fluida al usar la ofuscación.

Si no se encuentra el diccionario, tendrá la opción de especificar manualmente un archivo de diccionario.

![Modelo ofuscado](~/content/assets/images/obfuscated-model.png)

Si no se proporciona ningún archivo de diccionario, solo podrá explorar el modelo ofuscado y los resultados del Optimizador de DAX, lo que significa que no podrá ver las expresiones DAX originales ni navegar hasta las medidas correspondientes en el Explorador TOM.

[Más información sobre la ofuscación del Optimizador de DAX](https://docs.daxoptimizer.com/how-to-guides/obfuscating-files).

> [!TIP]
> Si quieres explorar un modelo ofuscado a través de la interfaz web del Optimizador de DAX, puedes especificar un diccionario desde la ubicación `%LocalAppData%\TabularEditor3\DaxOptimizer`. La interfaz web del Optimizador de DAX realiza la desofuscación en el lado del cliente, por lo que su diccionario nunca se carga en el servicio del Optimizador de DAX.

### Analizar un modelo

Una vez que se haya cargado un archivo VPAX, espere unos segundos a que el servicio del Optimizador de DAX «verifique» el archivo. Una vez verificado, puede realizar una «ejecución» del DAX Optimizer marcando la casilla «Acepta **consumir 1 ejecución** para analizar este modelo» y, a continuación, haciendo clic en el botón **Analizar** en la vista **DAX Optimizer**:

![Análisis de Dax Optimizer](~/content/assets/images/features/dax-optimizer-analyze.png)

El análisis tardará unos minutos en completarse, dependiendo del tamaño del modelo y del número de medidas. Una vez finalizado el análisis, se le presentará un resumen de los problemas detectados.

## Problemas y limitaciones conocidos

A continuación se indican los problemas y limitaciones conocidos de la función **Optimizador de DAX**, que esperamos abordar en futuras versiones:

- La vista del **Optimizador de DAX** no muestra cuántas «ejecuciones» quedan en un contrato determinado. Como solución alternativa, inicia sesión en https://app.daxoptimizer.com y haz clic en el icono del «relámpago» en la esquina superior derecha para ver cuántas «ejecuciones» te quedan por contrato.