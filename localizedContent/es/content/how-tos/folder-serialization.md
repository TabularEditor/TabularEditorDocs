---
uid: folder-serialization
title: Serialización en carpetas
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Serialización en carpetas

Esta función te permite integrar más fácilmente tus modelos tabulares de SSAS en un entorno de control de versiones basado en archivos, como TFS, Subversion o Git. Al elegir "Archivo" > "Guardar en carpeta...", Tabular Editor descompondrá el archivo Model.bim y guardará su contenido en archivos independientes dentro de una estructura de carpetas similar a la del JSON contenido en Model.bim. Cuando vuelvas a guardar el modelo, solo se modificarán los archivos cuyos metadatos hayan cambiado. Esto significa que la mayoría de los sistemas de control de versiones pueden detectar fácilmente qué cambios se han hecho en el modelo, lo que facilita mucho la fusión de cambios y la gestión de conflictos en comparación con trabajar con un único archivo Model.bim.

![Ejemplo de serialización de carpetas](~/content/assets/images/folder-serialization-example.png)

De forma predeterminada, los objetos se serializan hasta el nivel de objeto más bajo (es decir, las medidas, las columnas y las jerarquías se almacenan como archivos .json individuales).

Además, la [sintaxis de la línea de comandos](xref:command-line-options) de Tabular Editor permite cargar un modelo desde esta estructura de carpetas e implementarlo directamente en una base de datos, lo que facilita automatizar compilaciones en flujos de trabajo de integración continua.

Si quieres personalizar el nivel de granularidad con el que se guardan los metadatos en archivos individuales, ve a Archivo > Preferencias y haz clic en la pestaña "Guardar en carpeta". Aquí puedes activar o desactivar algunas opciones de serialización que se pasan al TOM al serializar en JSON. Además, puedes marcar o desmarcar los tipos de objetos para los que se generarán archivos individuales. En algunos escenarios de control de versiones, quizá quieras almacenar todo lo relacionado con una tabla en un único archivo, mientras que en otros escenarios quizá necesites archivos individuales para columnas y medidas.

Estos ajustes se guardan en una anotación del modelo la primera vez que usas la función Guardar en carpeta, de modo que se reutilicen cuando se cargue el modelo y, posteriormente, se pulse el botón "Guardar". Si quieres aplicar una nueva configuración, vuelve a usar "Archivo > Guardar en carpeta...".

<img src="~/content/assets/images/folder-serialization-settings-te2.png" width="300" />
