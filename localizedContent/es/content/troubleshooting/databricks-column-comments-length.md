---
uid: databricks-column-comments-length
title: Error de longitud del comentario de columna en Databricks
author: Equipo de soporte
updated: 2026-02-06
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

# Error de longitud del comentario de columna en Databricks

Al usar el Asistente para importar tablas para importar tablas desde Databricks, puede aparecer un error de conexión si los comentarios de columna (descripciones) superan los 512 caracteres. Esta limitación existe en el controlador ODBC de Simba Spark, aunque Databricks Unity Catalog permite comentarios de columna más largos.

Un ejemplo de mensajes de error típicos se ve así:

**"No se puede conectar a la base de datos 'database_name' en 'adb-xxxx.azuredatabricks.net/sql/1.0/warehouses/xxxx': Se ha producido una excepción en el destino de una invocación."**

Este artículo explica por qué pasa esto y ofrece dos soluciones alternativas para resolver el problema.

---

## Comprender el problema

El controlador ODBC Simba Spark, que Tabular Editor utiliza para conectarse a Databricks, tiene un límite predeterminado de 512 caracteres para los comentarios de columna. Este límite se aplica independientemente de lo que permita Databricks Unity Catalog.

### Por qué sucede

1. **Limitación predeterminada del controlador**: El controlador ODBC Simba Spark está configurado con un parámetro `MaxCommentLen` predeterminado de 512 caracteres.

2. **Unity Catalog permite comentarios más largos**: Databricks Unity Catalog permite descripciones de columna de más de 512 caracteres, lo que puede superar el límite del controlador.

3. **Recuperación en el asistente de importación**: Cuando el Asistente para importar tablas consulta los metadatos de la tabla, intenta recuperar todos los comentarios de columna. Si algún comentario supera el límite del controlador, la conexión falla con una excepción de invocación.

---

## Resolución

Hay dos formas de resolver este problema:

### Opción 1: Limitar los comentarios de columna en Databricks (Recomendado por su sencillez)

El enfoque más sencillo es asegurarse de que todas las descripciones de columna de las tablas de Databricks Unity Catalog no superen los 512 caracteres.

**Pasos:**

1. Revisa los comentarios de las columnas en tus tablas de Databricks.
2. Identifica los comentarios que superen los 512 caracteres.
3. Edita esos comentarios para que tengan 512 caracteres o menos.
4. Guarda los cambios en Databricks.
5. Vuelve a intentar la importación en Tabular Editor.

**Ventajas:**

- Fácil de implementar
- No requiere cambios de configuración
- Funciona con todas las herramientas que se conectan a Databricks

**Compensaciones:**

- Requiere modificar los metadatos de origen
- Puede perderse información si las descripciones se truncan
- No es adecuado si se necesitan descripciones más largas

### Opción 2: Aumentar el parámetro MaxCommentLen en el controlador Simba

Si necesitas conservar comentarios de columna de más de 512 caracteres, puedes configurar el Simba Spark ODBC Driver para admitir comentarios más extensos.

> [!NOTE]
> Antes de continuar, asegúrate de tener instalada la versión más reciente del Simba Spark ODBC Driver for Databricks. Puedes descargarlo desde la [página de descarga de ODBC de Microsoft Azure Databricks](https://learn.microsoft.com/azure/databricks/integrations/odbc/download).

**Pasos:**

1. **Busca la carpeta de instalación de Simba Spark ODBC Driver.**

   La ubicación de instalación predeterminada del controlador de 64 bits es:

   ```
   C:\Program Files\Simba Spark ODBC Driver\
   ```

   Si instalaste el controlador en una ubicación personalizada, ve a esa carpeta.

2. **Crea o edita el archivo microsoft.sparkodbc.ini.**

   En la carpeta de instalación del controlador, crea un archivo nuevo llamado **microsoft.sparkodbc.ini** (si aún no existe).

   > [!NOTE]> El instalador de Simba Spark ODBC Driver no crea este archivo .ini de forma predeterminada, así que probablemente tendrás que crearlo manualmente.

3. **Añade la configuración MaxCommentLen.**

   Abre el archivo **microsoft.sparkodbc.ini** en un editor de texto (como el Bloc de notas) y añade el siguiente contenido:

   ```ini
   [Driver]
   MaxCommentLen=2048
   ```

   Ajusta el valor (2048 en este ejemplo) para que admita la longitud máxima de comentario que necesites.

4. **Guarda el archivo.**

   Asegúrate de guardar el archivo como **microsoft.sparkodbc.ini** (no microsoft.sparkodbc.ini.txt) en la carpeta de instalación del controlador.

5. **Reinicia Tabular Editor.**

   Cierra todas las instancias de Tabular Editor y vuelve a abrir la aplicación para que el cambio de configuración surta efecto.

6. **Reintenta la importación.**

   Vuelve a ejecutar el Asistente para importar tablas para volver a importar tus tablas de Databricks. Ahora la conexión debería realizarse correctamente con el límite de longitud de comentarios aumentado.

**Ventajas:**

- Conserva las descripciones completas de las columnas
- No es necesario modificar los metadatos de origen
- Se aplica a todas las conexiones de Databricks que usan este controlador

**Inconvenientes:**

- Requiere acceso al sistema de archivos de la carpeta de instalación del controlador
- El archivo de configuración debe crearse manualmente
- Los cambios se aplican en todo el equipo y afectan a otras aplicaciones que usan el mismo controlador

---

## Ejemplo paso a paso: cómo crear el archivo microsoft.sparkodbc.ini

Si nunca has creado un archivo .ini, sigue estos pasos detallados:

1. **Abre el Bloc de notas** (o tu editor de texto preferido).

2. **Escribe el siguiente contenido:**

   ```ini
   [Driver]
   MaxCommentLen=2048
   ```

3. **Guarda el archivo:**
   - Haz clic en **Archivo > Guardar como**

   - Navega hasta `C:\Program Files\Simba Spark ODBC Driver\`

   - En la lista desplegable **Guardar como tipo**, selecciona **Todos los archivos (_._)** (¡importante!)

   - En el campo **Nombre de archivo**, escribe exactamente: **microsoft.sparkodbc.ini**

   - Haga clic en **Guardar**
   > [!IMPORTANT]> Asegúrate de seleccionar "Todos los archivos" como tipo de archivo; de lo contrario, el Bloc de notas lo guardará como microsoft.sparkodbc.ini.txt y no funcionará.

4. **Comprueba que el archivo se creó correctamente:**
   - Abre el Explorador de archivos y ve a `C:\Program Files\Simba Spark ODBC Driver\`
   - Confirma que ves un archivo llamado **microsoft.sparkodbc.ini** (no microsoft.sparkodbc.ini.txt)

5. **Cierra y reinicia Tabular Editor** para que los cambios surtan efecto.

---

## Lista de comprobación rápida para la solución de problemas

- [ ] **Confirma los mensajes de error**: Verifica que el error de conexión se produce durante el Asistente para importar tablas al conectarte a Databricks.
- [ ] **Comprueba la longitud de los comentarios de las columnas**: Consulta tus tablas de Databricks para identificar cualquier comentario de columna que supere los 512 caracteres.
- [ ] **Verifica la instalación del controlador**: Confirma que el Simba Spark ODBC Driver esté instalado y localiza su carpeta de instalación.
- [ ] **Comprueba la ubicación del archivo .ini**: Asegúrate de que el archivo **microsoft.sparkodbc.ini** esté en la carpeta correcta (el directorio de instalación del controlador, no un subdirectorio).
- [ ] **Verifica la extensión del archivo**: Confirma que el archivo se llama **microsoft.sparkodbc.ini** y no **microsoft.sparkodbc.ini.txt**.
- [ ] **Reinicia Tabular Editor**: Los cambios de configuración solo surten efecto después de reiniciar la aplicación.

---

## Buenas prácticas de prevención

1. **Establece directrices sobre la longitud de los comentarios**: Si gestionas metadatos de Databricks, considera establecer directrices para mantener los comentarios de las columnas por debajo de 512 caracteres y lograr la máxima compatibilidad.

2. **Prueba las importaciones cuanto antes**: Al configurar un nuevo entorno de Databricks, prueba la importación de tablas en Tabular Editor al principio del proceso de desarrollo para identificar cualquier problema de metadatos.

3. **Documenta la configuración del controlador**: Si modificas el archivo **microsoft.sparkodbc.ini**, documenta el cambio en el runbook de tu equipo para que los demás conozcan la personalización.

4. **Revisa después de actualizar el controlador**: Al actualizar el Simba Spark ODBC Driver, comprueba que tu archivo **microsoft.sparkodbc.ini** siga presente, ya que las actualizaciones del controlador pueden sobrescribir o eliminar archivos de configuración personalizados.

---

## Recursos adicionales

- **[Databricks Knowledge Base - Unity Catalog Metadata Error](https://kb.databricks.com/unity-catalog/error-when-trying-to-load-a-dataset-after-integrating-unity-catalog-metadata-with-power-bi)**: Documentación oficial de Databricks que cubre este problema y el parámetro MaxCommentLen.
- **[Simba Spark ODBC Driver for Azure Databricks](https://learn.microsoft.com/azure/databricks/integrations/odbc/download)**: Descarga la versión más reciente del Simba Spark ODBC Driver para Azure Databricks.
- **[Asistente para importar tablas](xref:importing-tables)**: Obtén más información sobre cómo usar el Asistente para importar tablas en Tabular Editor.

---

## ¿Aún necesitas ayuda?

Si los pasos anteriores no resuelven el problema:

1. **Verifica la versión del controlador ODBC**: Asegúrate de tener instalada la versión más reciente del controlador ODBC Simba Spark. Puedes descargarlo desde la [página de descarga del ODBC de Microsoft Azure Databricks](https://learn.microsoft.com/azure/databricks/integrations/odbc/download).

2. **Comprueba la configuración del Data source ODBC**: Abre el Administrador de Data source ODBC de Windows (odbcad32.exe) y verifica que la conexión a Databricks esté configurada correctamente.

3. **Prueba con una tabla más sencilla**: Intenta importar una tabla de Databricks que sabes que tiene comentarios de columna cortos (o sin comentarios) para confirmar que la conexión funciona en general.

4. **Revisa los registros del controlador ODBC**: El Simba Spark ODBC Driver puede generar registros detallados. Consulta la documentación del controlador para obtener instrucciones sobre cómo habilitar el registro, ya que puede aportar información de diagnóstico adicional.

5. **Contacta con soporte**: Ponte en contacto con el soporte de Tabular Editor con:
   - El texto completo de los mensajes de error
   - Los detalles de tu conexión a Databricks (sin incluir credenciales)
   - La versión del Simba Spark ODBC Driver
   - Si has creado el archivo microsoft.sparkodbc.ini y su contenido
