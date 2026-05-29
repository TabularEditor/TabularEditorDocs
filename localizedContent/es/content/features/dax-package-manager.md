---
uid: dax-package-manager
title: Administrador de paquete DAX
author: Daniel Otykier
updated: 2025-11-03
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

# Administrador de paquetes DAX

## Información general

El **Administrador de paquetes DAX** (DPM) en Tabular Editor permite a los usuarios descubrir, instalar, actualizar y administrar fácilmente bibliotecas de [funciones DAX definidas por el usuario (UDF)](xref:udfs) (denominadas paquetes DAX), directamente dentro de la aplicación.  
Estas bibliotecas amplían tus capacidades de DAX con funciones reutilizables, lo que facilita la creación de modelos semánticos de Power BI coherentes y fáciles de mantener.

Como su nombre indica, esta característica actúa como un administrador de paquetes, similar a cómo NuGet o npm gestionan bibliotecas de código para los desarrolladores. La fuente de los paquetes DAX es https://daxlib.org, un proyecto de código abierto y sin ánimo de lucro de [SQLBI](https://sqlbi.com).

Puedes usar el Administrador de paquetes DAX con cualquier modelo que admita funciones DAX definidas por el usuario; es decir, el nivel de compatibilidad del modelo debe ser 1702 o superior.

> [!WARNING]
> Las funciones DAX definidas por el usuario están actualmente (a noviembre de 2025) en versión preliminar en Power BI. Ten en cuenta sus [limitaciones](https://learn.microsoft.com/en-us/dax/best-practices/dax-user-defined-functions#considerations-and-limitations) antes de usarlas.

---

![Administrador de paquetes DAX](~/content/assets/images/dax-package-manager-overview.png)

## Diseño de la interfaz

### 1. Abrir el Administrador de paquetes DAX

Puedes abrir el panel del Administrador de paquetes DAX desde el menú **Ver**. También puedes asignar un atajo personalizado al comando `View.DaxPackageManager` desde **Herramientas > Preferencias > Teclado**.

- **Menú:** `Ver → Administrador de paquetes DAX`
- **Atajo:** _(si lo has asignado en Preferencias)_

---

### 2. Listas de paquetes

En la parte izquierda de la pantalla, encontrarás las tres pestañas siguientes. Cada pestaña va acompañada de una lista de paquetes pertinente para su contexto:

| Pestaña             | Descripción                                                                                                                                        |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Examinar**        | Descubre los paquetes DAX disponibles del proveedor (p. ej., `api.daxlib.org`). |
| **Instalados**      | Consulta todos los paquetes instalados actualmente y sus versiones.                                                                |
| **Actualizaciones** | Consulta los paquetes para los que hay versiones más recientes disponibles.                                                        |

Cada entrada del paquete incluye:

- **Nombre y breve descripción**
- **Número de versión**
- **Autores o propietarios**
- **URL del proveedor**
- **Botones de Instalar / Quitar / Actualizar**
- **Indicador de popularidad (número de descargas)**

---

### 3. Barra de búsqueda

Introduce tus palabras clave de búsqueda o el nombre (parcial) del paquete para filtrar la lista y mostrar solo los elementos que coincidan con los términos de búsqueda. Esta función se aplica a las tres pestañas: **Examinar**, **Instalados** y **Actualizaciones**.

> [!NOTE]
> Actualmente solo mostramos los 20 primeros paquetes que coinciden con los criterios de búsqueda. Aún no hay paginación; llegará en una actualización futura. Si necesitas examinar todos los paquetes disponibles, consulta la fuente; por ejemplo, https://daxlib.org.

---

### 4. Panel de detalles del paquete

Al seleccionar un paquete, se muestra información detallada:

| Campo                                  | Descripción                                                                                          |
| -------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Instalado / Versión**                | Versión actual y actualizaciones disponibles.                                        |
| **Descripción**                        | Resumen de lo que proporciona la biblioteca.                                         |
| **Notas de la versión**                | Información sobre las nuevas funciones o los cambios de la versión más reciente.     |
| **Proveedor / Propietarios / Autores** | Metadatos de atribución.                                                             |
| **Etiquetas**                          | Útil para la categorización y la búsqueda.                                           |
| **Direcciones URL**                    | Enlaces directos a la documentación del proyecto, la API y el repositorio de GitHub. |
| **Fecha de publicación**               | Marca de tiempo de la versión actual.                                                |
| **Descargas**                          | Total de instalaciones realizadas por todos los usuarios.                            |

Un paquete que no esté instalado mostrará un botón **“Instalar”**. Al hacer clic en este botón, las UDF del paquete se añadirán al instante a tu modelo.

Los paquetes que ya estén instalados mostrarán un botón **“Quitar”**.

Los paquetes para los que haya versiones más recientes disponibles mostrarán un botón **“Actualizar”**.

> [!WARNING]
> Si quitas o actualizas un paquete en el que has modificado la expresión DAX de una o varias UDF, verás un mensaje de advertencia que indica que se perderán tus cambios.

---

### 5. Notificaciones de actualización

Al abrir un modelo que usa un paquete para el que hay una actualización disponible, verás una notificación de actualización en la parte inferior del **Explorador TOM**.

Haz clic en la notificación de actualización o abre la vista del **Administrador de paquetes DAX** para ver e instalar la actualización.

---

## Instalación de paquetes

1. Abre el **Administrador de paquetes DAX**.
2. En la pestaña **Examinar**, selecciona un paquete (por ejemplo, `DaxLib.SVG`). Usa la barra de búsqueda para acotar la búsqueda según lo necesites.
3. Haz clic en **Instalar**.
4. Una vez instalado, el paquete y sus funciones aparecerán en el Explorador TOM.

También puedes seleccionar **versiones** específicas antes de instalar, lo que resulta útil para las pruebas de regresión o para garantizar la compatibilidad con modelos antiguos.

---

## Actualización de paquetes

1. Ve a la pestaña **Actualizaciones** o selecciona un paquete que tenga una versión más reciente disponible.
2. Haz clic en **Actualizar todo** para actualizar todos los paquetes instalados, o en **Actualizar** para uno concreto.
3. DPM obtiene las definiciones más recientes y reemplaza automáticamente las funciones existentes.

---

## Eliminar paquetes

1. Ve a la pestaña **Instalados**.
2. Selecciona el paquete que deseas eliminar.
3. Haz clic en **Quitar**.

Todas las UDF asociadas se eliminarán del modelo.

> [!CAUTION]
> Eliminar UDFs puede provocar que las expresiones DAX en otras áreas del modelo (medidas, columnas calculadas, etc.) dejen de ser válidas. Si esto ocurre, siempre puedes pulsar **Deshacer** (Ctrl+Z) para deshacer la eliminación del paquete. Usa la función **Mostrar dependencias** (Mayús+F12) para identificar dónde se usan las UDF antes de eliminar un paquete.

---

## Consideraciones técnicas

El DAX Package Manager usa [propiedades extendidas](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.extendedproperty?view=analysisservices-dotnet) para llevar un registro de los paquetes instalados. Las propiedades extendidas son similares a las anotaciones, pero se adaptan mejor al almacenamiento de metadatos personalizados en formato JSON.

DAX Package Manager crea las siguientes propiedades extendidas en el objeto **Modelo**:

| Nombre de la propiedad           | Descripción                                                                                                                                                                                                                                                                              |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TabularEditor_ModelDaxPkgTable` | Un diccionario JSON con una entrada por cada paquete instalado. La clave es un entero secuencial, mientras que el valor contiene información sobre el proveedor del paquete, el identificador del paquete dentro del proveedor y la versión del paquete. |
| `TabularEditor_ModelDaxPkgSeq`   | Un valor entero que se incrementa cada vez que se instala un paquete. Se usa para generar claves únicas para la propiedad `TabularEditor_ModelDaxPkgTable`.                                                                                              |

Además, cada UDF importada a través del DAX Package Manager tendrá asignadas las siguientes propiedades extendidas:

| Nombre de la propiedad               | Descripción                                                                                                                                                                                                                                                            |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TabularEditor_ObjDaxPkgHandle`      | Un valor entero que corresponde a la clave de la propiedad `TabularEditor_ModelDaxPkgTable` en el modelo. Esto permite a Tabular Editor identificar a qué paquete pertenece una UDF.                                                   |
| `TabularEditor_ObjDaxPkgContentHash` | Un valor de hash calculado a partir de la expresión DAX de la UDF en el momento de la instalación. Se utiliza para detectar si una UDF se ha modificado desde la instalación, lo cual es importante al actualizar o eliminar paquetes. |

> [!CAUTION]
> Modificar o eliminar manualmente estas propiedades extendidas puede provocar un comportamiento inesperado en el Administrador de paquetes DAX.

## Gestión de conflictos

### Modificar UDF de paquetes

Si modificas la expresión DAX de una UDF importada desde un paquete DAX, verás el siguiente mensaje al actualizar o eliminar el paquete:

![Actualizar UDF modificada](~/content/assets/images/dax-package-manager-update-modified.png)

Tienes las siguientes opciones:

- **Sí**: La actualización continuará y sobrescribirá los cambios que hiciste en la UDF con su definición del origen del Administrador de paquetes DAX.
- **No**: La actualización continuará, pero las UDF(s) modificadas permanecerán intactas, lo que podría causar problemas si la actualización del paquete incluyó cambios importantes.
- **Cancelar**: Cancela la actualización.

> [!TIP]
> Si quieres "desvincular" las UDF existentes del Administrador de paquetes DAX, elimina las propiedades extendidas `TabularEditor_ObjDaxPkgHandle` y `TabularEditor_ObjDaxPkgContentHash` de los objetos UDF. De este modo, el Administrador de paquetes DAX dejará de realizar el seguimiento de estas UDF y no se verán afectadas por futuras actualizaciones o eliminaciones de paquetes. Aun así, debes seguir teniendo en cuenta los conflictos de nombres.

### Instalar un paquete con conflictos de nombres

Si intentas instalar un paquete que contenga una UDF con el mismo nombre que una UDF existente en el modelo (independientemente de si se importó desde otro paquete o se creó manualmente), verás el siguiente mensaje:

![Conflicto de nombres al instalar un paquete](~/content/assets/images/dax-package-manager-install-conflict.png)

Tienes las siguientes opciones:

- **Sí**: La instalación continuará y la UDF del paquete sobrescribirá la UDF existente en el modelo.
- **No**: La instalación continuará, pero se omitirán las UDF(s) en conflicto del paquete.
- **Cancelar**: Cancela la instalación.

---

## Recursos adicionales

- [Sitio del proyecto de DaxLib](https://daxlib.org)
- [Repositorio de GitHub de DaxLib](https://github.com/daxlib/daxlib)
- [Funciones DAX definidas por el usuario (Microsoft Learn)](https://learn.microsoft.com/en-us/dax/best-practices/dax-user-defined-functions)
- [Funciones definidas por el usuario en Tabular Editor 3](xref:udfs)
