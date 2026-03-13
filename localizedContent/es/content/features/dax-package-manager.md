---
uid: dax-package-manager
title: Administrador de paquetes de DAX
author: Daniel Otykier
updated: 2025-11-03
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Escritorio
          full: true
        - edition: Negocios
          full: true
        - edition: Empresarial
          full: true
---

# Administrador de paquetes de DAX

## Descripción general

El **Administrador de paquetes de DAX** (DPM) de Tabular Editor permite a los usuarios descubrir, instalar, actualizar y administrar bibliotecas de [funciones DAX definidas por el usuario (UDF)](xref:udfs) (llamadas paquetes de DAX), directamente en la aplicación.  
Estas bibliotecas amplían sus capacidades de DAX con funciones reutilizables, lo que facilita crear modelos semánticos de Power BI coherentes y fáciles de mantener.

Como su nombre indica, esta función actúa como un administrador de paquetes, de forma similar a cómo NuGet o npm gestionan bibliotecas de código para los desarrolladores. La fuente de los paquetes de DAX es https://daxlib.org, que es un proyecto de código abierto y sin ánimo de lucro de [SQLBI](https://sqlbi.com).

Puede usar el Administrador de paquetes de DAX con cualquier modelo que admita funciones DAX definidas por el usuario; es decir, el nivel de compatibilidad del modelo debe ser 1702 o superior.

> [!WARNING]
> Las funciones DAX definidas por el usuario son actualmente (a fecha de noviembre de 2025) una característica en versión preliminar de Power BI. Considere sus [limitaciones](https://learn.microsoft.com/en-us/dax/best-practices/dax-user-defined-functions#considerations-and-limitations) antes de usarlas.

---

![Administrador de paquetes de DAX](~/content/assets/images/dax-package-manager-overview.png)

## Diseño de la interfaz

### 1. Abrir el Administrador de paquetes de DAX

Puede abrir el panel de DPM desde el menú **Ver**. También es posible asignar un atajo personalizado al comando `View.DaxPackageManager` desde **Herramientas > Preferencias > Teclado**.

- **Menú:** `Ver → Administrador de paquetes de DAX`
- **Atajo:** _(si se ha asignado en Preferencias)_

---

### 2. Listas de paquetes

A la izquierda de la pantalla, encontrarás las tres pestañas siguientes. Cada pestaña va acompañada de una lista de paquetes relevantes para su contexto:

| Pestaña             | Descripción                                                                                                                                           |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Explorar**        | Descubre los paquetes de DAX disponibles del proveedor (p. ej., `api.daxlib.org`). |
| **Instalados**      | Consulta todos los paquetes instalados actualmente y sus versiones.                                                                   |
| **Actualizaciones** | Consulta los paquetes para los que hay versiones más recientes disponibles.                                                           |

Cada entrada de paquete incluye:

- **Nombre y descripción breve**
- **Número de versión**
- **Autores o propietarios**
- **URL del proveedor**
- **Botones de Instalar / Quitar / Actualizar**
- **Indicador de popularidad (número de descargas)**

---

### 3. Barra de búsqueda

Escribe tus palabras clave de búsqueda o el nombre (parcial) del paquete para filtrar la lista de elementos y mostrar solo los que coincidan con los términos de búsqueda. Esta característica se aplica a las tres pestañas, es decir, **Explorar**, **Instalados** y **Actualizaciones**.

> [!NOTE]
> Actualmente solo mostramos los primeros 20 paquetes que coinciden con los criterios de búsqueda. Todavía no hay una función de paginación; llegará en una actualización futura. Si necesitas explorar todos los paquetes disponibles, consulta la fuente; por ejemplo, https://daxlib.org.

---

### 4. Panel de detalles del paquete

Al seleccionar un paquete, se muestra información detallada:

| Campo                                  | Descripción                                                                                          |
| -------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Instalado / Versión**                | Versión actual y actualizaciones disponibles.                                        |
| **Descripción**                        | Resumen de lo que ofrece la biblioteca.                                              |
| **Notas de la versión**                | Información sobre nuevas funciones o cambios en la versión más reciente.             |
| **Proveedor / Propietarios / Autores** | Metadatos de atribución.                                                             |
| **Etiquetas**                          | Útiles para la categorización y la búsqueda.                                         |
| **Direcciones URL**                    | Enlaces directos a la documentación del proyecto, la API y el repositorio de GitHub. |
| **Fecha de publicación**               | Marca de tiempo de la versión actual.                                                |
| **Descargas**                          | Instalaciones totales de todos los usuarios.                                         |

Un paquete que no esté instalado mostrará un botón **"Instalar"**. Al hacer clic en este botón, las UDF del paquete se añadirán al instante a tu modelo.

Los paquetes que ya están instalados mostrarán un botón **“Eliminar”**.

Los paquetes que tengan versiones más recientes disponibles mostrarán un botón **“Actualizar”**.

> [!WARNING]
> Si elimina o actualiza un paquete en el que haya realizado modificaciones en la expresión DAX de una o más UDF, verá un mensaje de advertencia indicando que se perderán sus cambios.

---

### 5. Notificaciones de actualización

Al abrir un modelo que usa un paquete para el que hay una actualización disponible, verá una notificación de actualización en la parte inferior del **Explorador TOM**.

Haga clic en la notificación de actualización o abra la vista del Administrador de paquetes DAX para ver e instalar la actualización.

---

## Instalación de paquetes

1. Abra **Administrador de paquetes DAX**.
2. En la pestaña **Examinar**, seleccione un paquete (p. ej., `DaxLib.SVG`). Use la barra de búsqueda para acotar la búsqueda según sea necesario.
3. Haga clic en **Instalar**.
4. Una vez instalado, el paquete y sus funciones aparecerán en el Explorador TOM.

También puede seleccionar **versiones** concretas antes de instalarlas —útil para pruebas de regresión o para garantizar la compatibilidad con modelos más antiguos.

---

## Actualización de paquetes

1. Vaya a la pestaña **Actualizaciones** o seleccione un paquete con una versión más reciente disponible.
2. Haga clic en **Actualizar todo** para actualizar todos los paquetes instalados, o en **Actualizar** para uno en concreto.
3. DPM obtiene las definiciones más recientes y reemplaza automáticamente las funciones existentes.

---

## Eliminación de paquetes

1. Vaya a la pestaña **Instalados**.
2. Seleccione el paquete que quiera eliminar.
3. Haga clic en **Eliminar**.

Todas las UDF asociadas se eliminarán del modelo.

> [!CAUTION]
> Eliminar UDFs puede afectar a las expresiones DAX en otras áreas del modelo (medidas, columnas calculadas, etc.) queden inválidas. Si esto ocurre, siempre puedes pulsar **Deshacer** (Ctrl+Z) para revertir la eliminación del paquete. Usa la función **Mostrar dependencias** (Shift+F12) para identificar dónde se usan las UDF antes de eliminar un paquete.

---

## Consideraciones técnicas

El DAX Package Manager usa [propiedades extendidas](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.extendedproperty?view=analysisservices-dotnet) para llevar un registro de los paquetes instalados. Las propiedades extendidas son similares a las anotaciones, pero se adaptan mejor al almacenamiento de metadatos personalizados en formato JSON.

El DAX Package Manager crea las siguientes propiedades extendidas en el objeto **Modelo**:

| Nombre de la propiedad           | Descripción                                                                                                                                                                                                                                                                   |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TabularEditor_ModelDaxPkgTable` | Un diccionario JSON con una entrada por cada paquete instalado. La clave es un entero secuencial, mientras que el valor contiene información sobre el proveedor del paquete, el ID del paquete dentro del proveedor y la versión del paquete. |
| `TabularEditor_ModelDaxPkgSeq`   | Un valor entero que se incrementa cada vez que se instala un paquete. Se usa para generar claves únicas para la propiedad `TabularEditor_ModelDaxPkgTable`.                                                                                   |

Además, cada UDF importada mediante el DAX Package Manager tendrá asignadas las siguientes propiedades extendidas:

| Nombre de la propiedad               | Descripción                                                                                                                                                                                                                                                     |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TabularEditor_ObjDaxPkgHandle`      | Un valor entero que corresponde a la clave de la propiedad `TabularEditor_ModelDaxPkgTable` en el modelo. Esto permite a Tabular Editor identificar a qué paquete pertenece una UDF.                                            |
| `TabularEditor_ObjDaxPkgContentHash` | Un valor hash calculado a partir de la expresión DAX de la UDF en el momento de la instalación. Se usa para detectar si una UDF se ha modificado desde la instalación, lo cual es importante al actualizar o eliminar paquetes. |

> [!CAUTION]
> Modificar o eliminar manualmente estas propiedades extendidas puede provocar un comportamiento inesperado en el Administrador de paquetes DAX.

## Gestión de conflictos

### Modificar UDF procedentes de paquetes

Si modificas la expresión DAX de una UDF importada desde un paquete DAX, verás el siguiente aviso al actualizar o desinstalar el paquete:

![Actualizar UDF modificada](~/content/assets/images/dax-package-manager-update-modified.png)

Tienes las siguientes opciones:

- **Sí**: La actualización continuará y sobrescribirá los cambios que hiciste en la UDF con la definición procedente del origen del Administrador de paquetes DAX.
- **No**: La actualización continuará, pero las UDF(s) modificadas permanecerán intactas, lo que podría causar problemas si la actualización del paquete incluyera cambios incompatibles.
- **Cancelar**: Cancela la actualización.

> [!TIP]
> Si deseas "desvincular" las UDF existentes del Administrador de paquetes DAX, elimina las propiedades extendidas `TabularEditor_ObjDaxPkgHandle` y `TabularEditor_ObjDaxPkgContentHash` de los objetos UDF. De este modo, el Administrador de paquetes DAX dejará de realizar el seguimiento de estas UDF y no se verán afectadas por futuras actualizaciones o desinstalaciones de paquetes. Aun así, debes tener en cuenta los conflictos de nombres.

### Instalar un paquete con conflictos de nombres

Si intentas instalar un paquete que contiene una UDF con el mismo nombre que una UDF existente en el modelo (independientemente de si se importó de otro paquete o se creó manualmente), verás el siguiente aviso:

![Instalar paquete: conflicto de nombres](~/content/assets/images/dax-package-manager-install-conflict.png)

Tienes las siguientes opciones:

- **Sí**: La instalación continuará y la UDF del paquete sobrescribirá la UDF existente en el modelo.
- **No**: La instalación continuará, pero se omitirán las UDF(s) del paquete que entren en conflicto.
- **Cancelar**: Cancela la instalación.

---

## Recursos adicionales

- [Sitio del proyecto DaxLib](https://daxlib.org)
- [Repositorio de GitHub de DaxLib](https://github.com/daxlib/daxlib)
- [Funciones DAX definidas por el usuario (Microsoft Learn)](https://learn.microsoft.com/en-us/dax/best-practices/dax-user-defined-functions)
- [Funciones definidas por el usuario en Tabular Editor 3](xref:udfs)
