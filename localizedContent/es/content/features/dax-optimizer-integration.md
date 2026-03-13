---
uid: dax-optimizer-integration
title: Integración con el Optimizador de DAX
author: Daniel Otykier
updated: 2024-10-30
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Escritorio
          full: true
        - edition: Empresarial
          full: true
        - edition: Corporativo
          full: true
---

# Integración con el Optimizador de DAX

> [!NOTE]
> Los usuarios de Tabular Editor 3 **Edición Enterprise** pueden obtener acceso gratuito al Optimizador de DAX. [Más información](https://blog.tabulareditor.com/2024/10/31/free-dax-optimizer-access-in-tabular-editor-3/)

Tabular Editor 3.18.0 presenta **Optimizador de DAX** como una experiencia integrada. [Optimizador de DAX](https://daxoptimizer.com) es un servicio que le ayuda a optimizar sus modelos tabulares de SSAS/Azure AS y sus modelos semánticos de Power BI/Fabric. La herramienta combina estadísticas del [Analizador VertiPaq](https://www.sqlbi.com/tools/vertipaq-analyzer/) con un análisis estático de su código DAX y proporciona una lista priorizada de recomendaciones para ayudarle a identificar rápidamente posibles cuellos de botella de rendimiento.

> [!IMPORTANT]
> El Optimizador de DAX es un servicio de terceros de pago. Para usar la funcionalidad **Optimizador de DAX** en Tabular Editor 3, necesitará una [cuenta para el Optimizador de DAX](https://www.daxoptimizer.com/free-tour/).

## Introducción en vídeo

Mira cómo Marco Russo, de [SQLBI](https://www.sqlbi.com), presenta la integración del Optimizador de DAX en Tabular Editor 3:

<iframe width="640" height="360" src="https://www.youtube-nocookie.com/embed/Z5lZdI79tF8" title="Detect and Fix Issues with Tabular Editor 3 and DAX Optimizer Integration" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Primeros pasos

Para acceder a esta funcionalidad, vaya al menú **Ver** y elija **Optimizador de DAX**.

![Optimizador de DAX](~/content/assets/images/features/dax-optimizer-view-menu.png)

Aparecerá una nueva vista similar a la de la figura siguiente:

![Vista del Optimizador de DAX](~/content/assets/images/features/dax-optimizer-view.png)

Para conectar Tabular Editor 3 al servicio de Optimizador de DAX, haga clic en **Conectar...** desde el menú **Opciones**. Se te pedirá que introduzcas tus credenciales de Tabular Tools (Optimizador de DAX).

Si quieres **desconectarte** o **conectarte con una cuenta diferente**, vuelve a abrir el menú **Opciones** y selecciona la opción **Reconectar...**. Al cancelar el cuadro de diálogo, se desconectará la sesión actual.

Si quieres que Tabular Editor 3 se conecte automáticamente la próxima vez que se inicie la aplicación, puedes marcar la opción **Conectar automáticamente** dentro del menú **Opciones**. Si tienes una cuenta del Optimizador de DAX con varios Workspace en distintas regiones, también puedes elegir a qué región conectarte desde el menú **Opciones**.

Por último, el menú **Opciones** también te permite cambiar a una cuenta diferente en [escenarios de grupo](https://docs.daxoptimizer.com/how-to-guides/managing-groups).

## Explorar Workspaces y modelos

Una vez conectado, las listas desplegables de la parte superior de la vista se rellenarán con los Workspace existentes, los modelos y las versiones de modelo. Haz tus selecciones de izquierda a derecha (es decir, elige primero el **Workspace**, luego el **Modelo** y después la **Versión**). La vista mostrará un resumen de la versión del modelo seleccionada actualmente, con información como el tamaño del modelo, el número de tablas, el número de medidas, etc.

![Resumen del modelo](~/content/assets/images/model-overview.png)

> [!NOTE]
> Tabular Editor 3 te permite cargar archivos VPAX para crear nuevos modelos o versiones de modelo en el servicio del Optimizador de DAX. Sin embargo, si necesitas crear o administrar Workspaces, mover o compartir modelos, etc., tendrás que hacerlo a través de la [interfaz web del Optimizador de DAX](https://app.daxoptimizer.com).

Si una versión de modelo aún no se ha analizado, tendrás la opción de iniciar el análisis. Ten en cuenta que, según el plan de tu cuenta, es posible que tengas un número limitado de "ejecuciones" disponibles.

Una vez que el análisis haya finalizado, se te mostrará un resumen con el número de incidencias detectadas. La información que se muestra es similar a la que verías en la interfaz web del Optimizador de DAX.

Ve a la pestaña **Problemas** o **Medidas** para ver los resultados detallados. Usa los encabezados de las columnas para ordenar y filtrar los resultados.

![Dax Optimizer Issues](~/content/assets/images/features/dax-optimizer-issues.png)

## Navegar por problemas y medidas

Cuando haces doble clic en un problema o una medida en la vista detallada mostrada arriba, se abrirá la vista **Resultados del Optimizador de DAX**, donde se muestra la expresión DAX original de la medida, junto con resaltados de las zonas problemáticas. La lista del lado izquierdo de la pantalla te permite activar o desactivar los problemas que se resaltan. Además, puedes marcar los problemas como **Corregido** o **Ignorado** usando las casillas de verificación de la lista.

![Dax Optimizer Results](~/content/assets/images/features/dax-optimizer-results.png)

Haz clic en el botón **Buscar en el Explorador TOM...** situado en la esquina superior derecha de la vista para ir a la medida correspondiente del modelo cargado actualmente.

Marca la casilla **Seguir el Explorador TOM** para mantener el Explorador TOM sincronizado con la medida seleccionada actualmente en la vista **Resultados del Optimizador de DAX**.

Cuando haces clic en una referencia a una medida en el panel de código DAX dentro de la vista **Resultados del Optimizador de DAX**, la vista irá a esa medida. Luego puedes usar los botones **Atrás** (Alt+Left) y **Adelante** (Alt+Right) para navegar atrás y adelante entre las medidas que has visitado.

## Subir modelos y versiones de modelo

Para subir estadísticas de VPAX al Optimizador de DAX, asegúrate de que Tabular Editor esté conectado actualmente a una instancia de Analysis Services (SSAS, Azure AS, Power BI Desktop o un punto de conexión XMLA de Power BI/Fabric). Luego, en el menú desplegable de la esquina superior izquierda de la vista **Optimizador de DAX**, selecciona el Workspace. Haz clic en **Subir...** dentro del menú **Opciones**.

Se mostrará un cuadro de diálogo similar al que se muestra a continuación:

![Subir Vpax](~/content/assets/images/upload-vpax.png)

Aquí puedes elegir si el VPAX debe cargarse como un modelo nuevo dentro del Workspace o si el VPAX contiene estadísticas actualizadas para un modelo existente.

- Para un **modelo nuevo**, debes proporcionar un nombre y elegir si el VPAX debe estar [ofuscado](https://www.sqlbi.com/blog/marco/2024/03/15/vpax-obfuscator-a-library-to-obfuscate-vpax-files/) o no (consulta más abajo para obtener más detalles sobre la ofuscación). También debes elegir bajo qué [contrato](https://docs.daxoptimizer.com/glossary/contract) se debe subir el modelo. Esto afecta al número y la frecuencia de [_ejecuciones_](https://docs.daxoptimizer.com/glossary/run) del Optimizador de DAX que podrás realizar posteriormente sobre el modelo.
- Para una **nueva versión del modelo**, debes seleccionar el modelo existente que quieres actualizar.

Cuando hagas clic en el botón **Aceptar**, el archivo VPAX se subirá al Optimizador de DAX y podrás empezar a analizar el modelo.

> [!NOTE]
> Si Tabular Editor 3 no tiene estadísticas del Analizador VertiPaq disponibles, esas estadísticas se recopilarán para el modelo actual antes de subir el archivo VPAX. También volveremos a recopilar automáticamente las estadísticas si la última recopilación es anterior o coincide con la de la última subida del archivo VPAX, para ese modelo en concreto.

### Ofuscación

De forma predeterminada, los archivos VPAX subidos con Tabular Editor 3 se ofuscarán. En **Subir modelo** puedes activar o desactivar la ofuscación para las subidas de modelos nuevos. Las subidas posteriores de versiones del modelo se ofuscarán o no en función de cómo se haya subido la primera versión. También puedes exportar localmente un archivo VPAX ofuscado sin subirlo al Optimizador de DAX desde la vista **Analizador VertiPaq**. En este caso, se genera un archivo de diccionario y se guarda en tu equipo local, junto al archivo .ovpax exportado. Este archivo de diccionario se usa para desofuscar el contenido del archivo .ovpax.

Cuando se suben datos VPAX ofuscados al servicio del Optimizador de DAX a través de la vista **Optimizador de DAX**, Tabular Editor realiza automáticamente el seguimiento de los diccionarios de ofuscación y los guarda en la carpeta `%LocalAppData%\\TabularEditor3\\DaxOptimizer` de tu equipo local. Por ello, al explorar modelos con la característica **Optimizador de DAX** en Tabular Editor 3, los modelos se desofuscan automáticamente si se encuentra un diccionario adecuado en esta carpeta, lo que ofrece una experiencia más fluida al usar la ofuscación.

Si no se encuentra el diccionario, tendrás la opción de especificar manualmente un archivo de diccionario.

![Modelo ofuscado](~/content/assets/images/obfuscated-model.png)

Si no se proporciona ningún archivo de diccionario, solo podrás explorar el modelo ofuscado y los resultados del Optimizador de DAX, lo que significa que no podrás ver las expresiones DAX originales ni navegar hasta las medidas correspondientes en el Explorador TOM.

[Más información sobre la ofuscación del Optimizador de DAX](https://docs.daxoptimizer.com/how-to-guides/obfuscating-files).

> [!TIP]
> Si quieres explorar un modelo ofuscado a través de la interfaz web del Optimizador de DAX, puedes especificar un diccionario desde la ubicación `%LocalAppData%\\TabularEditor3\\DaxOptimizer`. La interfaz web del Optimizador de DAX realiza la desofuscación en el lado del cliente, por lo que tu diccionario nunca se carga en el servicio del Optimizador de DAX.

### Analizar un modelo

Una vez que se haya cargado un archivo VPAX, espera unos segundos a que el servicio del Optimizador de DAX "verifique" el archivo. Una vez verificado, puedes realizar un "run" del Optimizador de DAX marcando la casilla "Aceptas **consumir 1 run** para analizar este modelo.", y luego haciendo clic en el botón **Analizar** en la vista de **DAX Optimizer**:

![Análisis del Optimizador de Dax](~/content/assets/images/features/dax-optimizer-analyze.png)

El análisis tardará unos minutos en completarse, en función del tamaño del modelo y del número de medidas. Cuando el análisis se complete, verás un resumen de los problemas detectados.

## Problemas conocidos y limitaciones

A continuación se indican los problemas conocidos y las limitaciones de la funcionalidad **Optimizador de DAX**, que esperamos solucionar en versiones futuras:

- La vista de **Optimizador de DAX** no muestra cuántos "runs" quedan en un contrato determinado. Como solución alternativa, inicie sesión en https://app.daxoptimizer.com y haga clic en el icono de "relámpago" en la esquina superior derecha para ver cuántos "runs" le quedan por cada contrato.