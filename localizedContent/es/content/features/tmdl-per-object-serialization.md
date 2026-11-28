---
uid: tmdl-per-object-serialization
title: Serialización TMDL por objeto
author: Morten Lønskov
updated: 2026-11-13
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.28.0
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          partial: true
          note: "Opens per-object folders and saves them in the standard layout"
        - edition: Enterprise
          full: true
---
# Serialización TMDL por objeto

La serialización TMDL por objeto guarda cada columna, medida, partición y jerarquía de una tabla, así como cada función, expresión compartida, origen de datos y relación del modelo, en su propio archivo `.tmdl`. Una carpeta de [Lenguaje de definición de modelo tabular (TMDL)](xref:tmdl) en el diseño estándar conserva cada tabla con todos sus objetos en un archivo, y escribe todas las funciones en `functions.tmdl`, todas las expresiones compartidas en `expressions.tmdl`, todas las fuentes de datos en `dataSources.tmdl` y todas las relaciones en `relationships.tmdl`. Con los archivos por objeto, un cambio en una medida se muestra en el control de código fuente como un cambio en un archivo, y dos desarrolladores que editan medidas diferentes de la misma tabla editan archivos diferentes.

Los elementos de cálculo siempre permanecen en el archivo de su tabla.

## Diseño de carpetas

El archivo propio de la tabla permanece en la carpeta `tables` y conserva las propiedades, la descripción, las anotaciones, la directiva de actualización y los elementos de cálculo de la tabla. Los objetos de la tabla que se dividen van en una carpeta con el nombre de la tabla, con una subcarpeta por tipo de objeto. Las funciones, las expresiones compartidas, las fuentes de datos y las relaciones se colocan en una carpeta por tipo en la raíz de la carpeta TMDL:

```text
definition/
├── model.tmdl
├── expressions/
│   ├── Database.tmdl
│   └── Server.tmdl
├── functions/
│   └── Sales.MarginPct.tmdl
├── relationships/
│   └── 3a5c9e1d-7b2f-4c8a-9d6e-1f0b2a4c6e8d.tmdl
└── tables/
    ├── Sales.tmdl
    └── Sales/
        ├── columns/
        │   ├── Amount.tmdl
        │   └── Order Date.tmdl
        ├── measures/
        │   └── Total Amount.tmdl
        └── partitions/
            └── Sales.tmdl
```

Una tabla o un modelo sin objetos de un tipo no tiene carpeta para ese tipo. Cada archivo de objeto de tabla comienza con una línea `ref table` que vincula el objeto a su tabla:

```tmdl
ref table Sales

	measure 'Total Amount' = SUM(Sales[Amount])
		formatString: #,0.00
```

La carpeta es TMDL estándar. Power BI Desktop, Tabular Editor 2.26 o posterior y Tabular Editor 3.19 o posterior la leen de la misma manera que leen una carpeta en el diseño estándar.

> [!WARNING]
> No abras una carpeta por objeto en Tabular Editor 3 anterior a la versión 3.19 o en Tabular Editor 2 anterior a la versión 2.26. Si la carpeta se guardó con la opción **Incluir orden de metadatos** marcada, esas versiones cargan las expresiones compartidas con texto vacío y no consiguen cargar una carpeta con archivos de origen de datos por objeto. Si guarda el modelo desde una de esas versiones, las expresiones compartidas se guardan sin su texto.

## Guardar un modelo con archivos por objeto

1. Abra **Herramientas &gt; Preferencias &gt; Formatos de archivo &gt; Guardar en carpeta &gt; Serialización TMDL**.
2. Marque **Guardar objetos en archivos separados**.
3. En el árbol situado debajo, marca los tipos de objetos que tendrán sus propios archivos.
4. Haga clic en **Aceptar**.
5. Seleccione **Archivo &gt; Guardar en carpeta** y elija una carpeta. Si el cuadro de diálogo de la carpeta muestra **Usar configuración de serialización de anotaciones**, desmárquelo.

**Archivo &gt; Guardar en carpeta** escribe en TMDL cuando **Formato de guardar en carpeta** en **Herramientas &gt; Preferencias &gt; Formatos de archivo &gt; Guardar en carpeta** es **TMDL**, el valor predeterminado.

![La página de preferencias de serialización TMDL con la opción «Guardar objetos en archivos separados» marcada](~/content/assets/images/pref-tmdl-serialization.png)

Para el modelo que tienes abierto, selecciona **Modelo &gt; Opciones de serialización...**, marca **Guardar objetos en archivos separados** y haz clic en **Aceptar**. La siguiente vez que pulse **Ctrl+S**, se escribirá la estructura por objeto.

Tabular Editor guarda la opción en la anotación `TabularEditor_SerializeOptions` en `model.tmdl` como `"TmdlApplySerializationDepth": true`, junto con los tipos de objetos marcados. **Archivo &gt; Guardar** (**Ctrl+S**) lee la anotación y mantiene el diseño, independientemente de sus preferencias. Para obtener más información sobre la anotación, consulte [Anotación del modelo de serialización](xref:save-to-folder#serialization-model-annotation).

> [!NOTE]
> **Guardar objetos en archivos separados** está desactivado de forma predeterminada. Una carpeta TMDL guardada por Power BI Desktop o por una versión anterior de Tabular Editor no tiene `TmdlApplySerializationDepth` en su anotación, y **Ctrl+S** la mantiene en la estructura estándar.

### Tipos de objetos

Cada fila marcada en el árbol desplaza un tipo de objeto a sus propios archivos:


| Fila                               | Carpeta                       | Nota                                                        |
| --------------------------------- | ---------------------------- | ----------------------------------------------------------- |
| **Orígenes de datos**                  | `dataSources`                |                                                             |
| **Funciones definidas por el usuario (UDF)** | `functions`                  |                                                             |
| **Expresiones compartidas**            | `expressions`                |                                                             |
| **Relaciones**                 | `relationships`              |                                                             |
| **Tablas &gt; Columnas**           | `tables/<table>/columns`     | Marcarla o desmarcarla hace lo mismo con las **Jerarquías**. |
| **Tablas > Jerarquías**       | `tables/<table>/hierarchies` | Marcarla o desmarcarla hace lo mismo con las **Columnas**.     |
| **Tablas &gt; Medidas**          | `tables/<table>/measures`    |                                                             |
| **Tablas &gt; Particiones**        | `tables/<table>/partitions`  |                                                             |


**Tablas**, **Perspectivas**, **Roles** y **Traducciones** se muestran marcados y en gris. El diseño TMDL estándar ya escribe cada tabla, perspectiva, rol y cultura en un archivo propio. El árbol no tiene ninguna fila para los elementos de cálculo.

### Nombres de archivo

Cada archivo y carpeta de tablas recibe el nombre de su objeto. Los caracteres que no son válidos en los nombres de archivo de Windows (`" < > | : * ? / \`) se codifican en el nombre.

Cuando cambia el nombre de un objeto, el siguiente guardado elimina el archivo antiguo y escribe un archivo con el nuevo nombre. Cuando eliminas una tabla, el siguiente guardado elimina su archivo y su carpeta.

## Reutilizar la configuración almacenada de un modelo

Cuando selecciona **Archivo &gt; Guardar en carpeta** para un modelo que tiene una anotación `TabularEditor_SerializeOptions`, el cuadro de diálogo de la carpeta muestra **Usar configuración de serialización de anotaciones**. Márcalo para guardar con la configuración almacenada del modelo, incluida su estructura por objeto. Desmárcala para guardar con tus preferencias y escribirlas en la anotación.

Si el modelo procede de una carpeta Database.json y marca **Usar configuración de serialización de anotaciones**, su profundidad de serialización se transfiere a la carpeta TMDL cuando **Guardar objetos en archivos separados** está marcado en la página **Serialización TMDL** o la anotación del modelo contiene `TmdlApplySerializationDepth`. Los elementos de cálculo permanecen en el archivo de su tabla, sea cual sea la profundidad.

## Volver al diseño estándar

1. Seleccione **Modelo &gt; Opciones de serialización...**.
2. Desmarca **Guardar objetos en archivos separados** y haz clic en **Aceptar**.
3. Pulse **Ctrl+S**.
4. Haga clic en **Sí** en la advertencia **Serialización TMDL por objeto**.

Tabular Editor reescribe la carpeta con un archivo por tabla y un archivo para cada una de las funciones, expresiones compartidas, fuentes de datos y relaciones, y elimina `TmdlApplySerializationDepth` de la anotación. El resto de la configuración de serialización del modelo, incluido el formato TMDL, permanece en la anotación.

## Advertencia al guardar

Cualquier operación de guardado que escriba el diseño estándar en una carpeta con archivos por objeto mostrará primero la advertencia **Serialización TMDL por objeto**. Esto se aplica a **Archivo &gt; Guardar**, **Archivo &gt; Guardar en carpeta** y a los guardados en [modo de espacio de trabajo](xref:workspace-mode). La advertencia dice lo siguiente:

> Su modelo está actualmente serializado por objeto. Si guarda ahora, sus archivos volverán a la serialización TMDL estándar. Consulta esta documentación para obtener más detalles.
>
> ¿Desea continuar?

El enlace de la advertencia abre esta página.

![La advertencia de serialización TMDL por objeto que se muestra antes de que un guardado escriba el diseño estándar](~/content/assets/images/tmdl-per-object-save-warning.png)


| Respuesta  | Resultado                                                                                                            |
| ------- | ----------------------------------------------------------------------------------------------------------------- |
| **Sí** | La carpeta se reescribe en el diseño estándar y `TmdlApplySerializationDepth` se elimina de la anotación. |
| **No**  | No se escribe nada y se cancela el guardado. En el modo de área de trabajo, la base de datos del área de trabajo tampoco se actualiza.     |


Después de un **Sí**, la carpeta permanece en el formato estándar cuando la vuelves a abrir en Tabular Editor 3 Edición Enterprise, hasta que vuelvas a marcar **Guardar objetos en archivos separados**.

## Edición y soporte de herramientas


| Herramienta                                | Abre una carpeta por objeto | Guarda archivos por objeto                                      |
| ----------------------------------- | ------------------------- | ----------------------------------------------------------- |
| Tabular Editor 3 Edición Enterprise | Sí                       | Sí                                                         |
| Tabular Editor 3 Edición Business   | Sí                       | No. Al guardar, se escribe el diseño estándar después de la advertencia de guardado. |
| Tabular Editor 3 Edición Desktop    | No                        | No.                                                         |
| Power BI Desktop                    | Sí                       | No. Al guardar, se escribe el diseño estándar sin advertencia.      |


En Business Edition, **Guardar objetos en archivos separados** y el árbol de tipos de objetos no aparecen en la página **Serialización TMDL** ni en **Modelo &gt; Opciones de serialización...**.

> [!WARNING]
> Si alguien guarda una carpeta por objeto con una herramienta que escribe el diseño estándar, todos los archivos de tabla y todos los archivos por objeto cambian en el control de código fuente.

## Orden de los objetos

Las funciones, las expresiones compartidas, las fuentes de datos y las relaciones mantienen su orden cuando se marca **Incluir orden de metadatos**: al guardar, se escribe una línea `ref` para cada una de ellas en `model.tmdl`, por ejemplo:

```tmdl
ref expression Server
ref expression Database
ref function 'Sales.MarginPct'
```

Las columnas, las medidas, las particiones y las jerarquías en sus propios archivos se cargan por orden de nombre de archivo cuando se abre la carpeta, y **Incluir orden de metadatos** no tiene ningún efecto sobre ellas.

## Consulte también

- @tmdl
- @save-to-folder
- @save-with-supporting-files
- @parallel-development