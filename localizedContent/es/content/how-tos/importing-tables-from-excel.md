---
uid: importing-tables-from-excel
title: Importación de tablas desde Excel
author: Daniel Otykier
updated: 2021-11-10
---

# Importación de tablas desde Excel

Si necesitas agregar hojas de cálculo de Excel como tablas a tu modelo tabular, puedes hacerlo con Tabular Editor 2.x y el controlador ODBC de Excel.

# Requisitos previos

Tabular Editor 2.x es una aplicación de 32 bits, y la mayoría de la gente suele tener instalada la versión de 64 bits de Office (que incluye un controlador ODBC de Excel de 64 bits). Lamentablemente, Tabular Editor 2.x no puede usar el controlador de 64 bits y, si simplemente descargas e intentas instalar el de 32 bits, recibirás un error si ya tienes instalada una versión de Office de 64 bits. Sin embargo, es posible instalar el controlador ODBC de Excel de 32 bits junto a Office de 64 bits usando esta solución alternativa:

1. Descarga la versión de 32 bits del controlador desde aquí: https://www.microsoft.com/en-us/download/details.aspx?id=54920
2. Descomprime el archivo AccessDatabaseEngine.exe
3. Dentro encontrarás el archivo aceredist.msi, que debe ejecutarse desde la línea de comandos con el modificador /passive:

  ```shell
  aceredist.msi /passive
  ```

4. Confirma la instalación en la configuración de ODBC Data source (32 bits) (botón Inicio de Windows, busca "ODBC"; la plataforma debe indicar "32/64 bit", como en la captura de pantalla siguiente):
   ![ODBC de Excel 32/64](~/content/assets/images/excel-odbc-32-64.png)

# Configuración de un Data source ODBC

Después de asegurarte de que tienes instalado el controlador ODBC de Excel de 32 bits, tal y como se describe arriba, para agregar una tabla desde un archivo de Excel con Tabular Editor 2.x debes seguir estos pasos:

1. En Tabular Editor, haz clic con el botón derecho en el modelo, elige "Importar tablas…" y haz clic en "Siguiente"
2. En el cuadro de diálogo de Propiedades de conexión, haz clic en "Cambiar…". Selecciona la opción "Microsoft ODBC Data source" y haz clic en "Aceptar".
3. Selecciona "Usar cadena de conexión" y pulsa "Generar…". Elige "Archivos de Excel" y pulsa "Aceptar".
   ![Propiedades de conexión Odbc de Excel](~/content/assets/images/odbc-connection-properties-excel.png)
4. Busca el archivo de Excel del que quieres cargar las tablas y pulsa "Aceptar". Esto debería generar una cadena de conexión parecida a esta:

  ```connectionstring
  Dsn=Excel Files;dbq=C:\Users\DanielOtykier\Documents\A Beer Dataset Calculation.xlsx;defaultdir=C:\Users\DanielOtykier\Documents;driverid=1046;maxbuffersize=2048;pagetimeout=5
  ```

5. Después de hacer clic en "OK", Tabular Editor debería mostrar la lista de hojas de cálculo y áreas de datos del archivo de Excel. Lamentablemente, el Asistente para importar tablas no puede previsualizar los datos en este momento, porque genera una instrucción SQL no válida:
   ![Import Tables Excel](~/content/assets/images/import-tables-excel.png)
6. Aun así, puedes marcar la tabla que quieras importar. Cuando termines, pulsa "Import" e ignora los mensajes de error.
7. En la tabla recién añadida, localiza la partición y modifica el SQL para eliminar el corchete vacío y el punto delante del nombre de la hoja de cálculo. Aplica el cambio (pulsa F5).
   ![Corregir expresiones de partición de Excel](~/content/assets/images/fix-partition-expressions-excel.png)
8. Luego, haz clic derecho en la partición y elige "Refresh Table Metadata…". Tabular Editor ahora lee los metadatos de las columnas del archivo de Excel a través del controlador ODBC:
   ![Refresh Metadata Excel](~/content/assets/images/refresh-metadata-excel.png)
9. (Opcional) Si no quieres usar ODBC para actualizar los datos en la tabla, tienes que sustituir la partición para usar una expresión basada en M que cargue los mismos datos de la hoja de cálculo. Para ello, agrega una nueva partición de Power Query a la tabla (haz clic con el botón derecho en "Partitions" y elige "New Partition (Power Query")). Elimina la partición heredada. A continuación, establece la expresión M de la nueva partición como sigue:

  ```M
  let
      Source = Excel.Workbook(File.Contents("<excel file path>"), null, true),
      Customer_Sheet = Source{[Item="<sheet name>",Kind="Sheet"]}[Data],
      #"Promoted Headers" = Table.PromoteHeaders(Customer_Sheet, [PromoteAllScalars=true])
  in
      #"Promoted Headers"
  ```

Sustituye los marcadores de posición `<excel file path>` y `<sheet name>` por sus valores reales.

# Conclusión

Importar tablas desde archivos de Excel es posible con Tabular Editor 2.x, pero requiere usar el controlador ODBC de Excel, como se muestra arriba, lo que añade algo de complejidad al proceso.