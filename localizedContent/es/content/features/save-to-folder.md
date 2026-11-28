---
uid: save-to-folder
title: Guardar en carpeta
author: Morten Lønskov
updated: 2026-11-13
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Guardar en carpeta

La opción Guardar en carpeta le permite almacenar los metadatos de su modelo como archivos individuales, que pueden gestionarse fácilmente con sistemas de control de versiones. En lugar de tener un único archivo (.bim o .pbix) que contenga todos los objetos de su modelo de datos, como tablas, medidas, relaciones, etc., puede dividirlos en archivos independientes y guardarlos en una carpeta. De este modo, puede usar herramientas de control de código fuente para realizar un seguimiento de los cambios, comparar versiones y colaborar con otros desarrolladores en su modelo de datos.

> [!NOTE]
> Una carpeta de modelos utiliza uno de estos dos formatos: Database.json (JSON) o [TMDL](xref:tmdl). En Tabular Editor 3, **Archivo > Guardar en carpeta** escribe el formato establecido en **Formato de Guardar en carpeta** en **Herramientas > Preferencias > Formatos de archivo > Guardar en carpeta**, TMDL de forma predeterminada. Un modelo cargado desde una carpeta conserva el formato de su carpeta cuando usa **Archivo > Guardar**.

Para guardar el modelo en una carpeta, siga estos pasos:

1. Seleccione **Archivo > Guardar en carpeta**.
2. Elija una carpeta en la que desee guardar los archivos de su modelo.
3. Haga clic en **Guardar**. Tabular Editor crea o actualiza los archivos en la carpeta seleccionada.
4. Ahora puede usar los archivos de la carpeta para control de versiones, despliegue o copia de seguridad.

## Configuración de serialización

La configuración de serialización determina cómo se dividen los objetos del modelo en archivos independientes. En esta configuración también puede definir si desea usar los formatos JSON o TMDL.

### [Preferencias de Tabular Editor 2](#tab/TE2Preferences)

La configuración de serialización se encuentra en Archivo > Preferencias > Serialización. <br></br>
![Preferencias de TE2](~/content/assets/images/common/TE2SaveToFolderSerializationSettings.png)

La configuración mostrada arriba es la establecida como predeterminada al usar Tabular Editor 3, pero no es la que Tabular Editor 2.X establece de forma predeterminada

### [Preferencias de Tabular Editor 3](#tab/TE3Preferences)
La configuración de serialización se encuentra en **Herramientas > Preferencias > Formatos de archivo**:

- **General** contiene los ajustes compartidos entre los formatos. Los **ajustes generales de serialización** (**Incluir datos confidenciales** e **Ignorar particiones de actualización incremental**) se aplican a los archivos Model.bim, a las carpetas Database.json y a las carpetas TMDL. La **configuración de serialización JSON** se aplica a los archivos Model.bim y a las carpetas Database.json.
- **Guardar en carpeta** establece el formato en el que **Archivo > Guardar en carpeta** escribe y enlaza con **Modelo > Opciones de serialización...**.
- **Guardar en carpeta > Serialización JSON** se aplica a los elementos que se guardan en una carpeta Database.json.
- **Guardar en carpeta > Serialización TMDL** se aplica a los guardados en una carpeta TMDL. En la Edición Enterprise, también activa la [serialización TMDL por objeto](xref:tmdl-per-object-serialization).

**Modelo > Opciones de serialización...** edita los ajustes almacenados con el modelo cargado. El cuadro de diálogo muestra el formato del modelo, por ejemplo, **Formato actual: TMDL**, y las secciones para ese formato. Para cambiar el formato, use **Archivo > Guardar en carpeta** o **Archivo > Guardar como**.

Las páginas de serialización JSON y serialización TMDL tienen cada una un botón **Restablecer valores predeterminados**. Para conocer cada configuración, su valor predeterminado y cuándo se aplican sus preferencias, consulte [Preferencias](xref:preferences#file-formats--general).
***

### Funciones definidas por el usuario (UDFs)

El formato de carpeta JSON puede almacenar cada [función definida por el usuario de DAX](xref:udfs) en su propio archivo, de la misma manera que ya lo hace con las tablas, las medidas y las columnas. Las funciones se colocan en una subcarpeta `functions` en la raíz del modelo:

```
MyModel/
├── database.json
├── functions/
│   ├── Sales.MarginPct.json
│   └── Time.SameDayLastYear.json
├── tables/
└── ...
```

La ventaja es la misma que para cualquier otro tipo de objeto: si dos desarrolladores editan dos funciones distintas, cambian dos archivos distintos, por lo que Git no tiene nada que fusionar. Sin esta opción, todas las funciones quedan insertadas en `database.json`, y cualquier edición en paralelo entra en conflicto en ese único archivo.

Actívelo con el nivel **Funciones definidas por el usuario (UDF)**, en **Herramientas > Preferencias > Formatos de archivo > Guardar en carpeta > Serialización JSON** o, para el modelo que tenga abierto, en **Modelo > Opciones de serialización...**.

![Modelo > Opciones de serialización, con el nivel Funciones definidas por el usuario (UDFs) marcado](~/content/assets/images/serialization-options-udf.png)

> [!IMPORTANT]
> Tabular Editor selecciona este nivel de forma predeterminada solo cuando guardas un modelo en una carpeta por _primera_ vez. Un modelo que ya está serializado en una carpeta conserva los niveles almacenados en su propia anotación de serialización, por lo que sus funciones permanecen insertadas en línea hasta que selecciones **Funciones definidas por el usuario (UDFs)** en **Modelo > Opciones de serialización...** y vuelvas a guardar el modelo.

### Anotación de serialización del modelo
Tabular Editor guarda la configuración de serialización en tu modelo para que siempre siga siendo la misma, independientemente de quién esté trabajando en el modelo. Esto garantiza que las preferencias locales de un desarrollador no sobrescriban la configuración del modelo y provoquen una fusión inmanejable en su control de código fuente. Puedes encontrar estas anotaciones en las propiedades del Explorador TOM del Modelo > Anotaciones > TabularEditor_SerializeOptions

Un guardado TMDL no escribe ninguna anotación cuando las opciones **Incluir elementos confidenciales**, **Ignorar particiones de actualización incremental** y **Guardar objetos en archivos separados** no están marcadas y los ajustes TMDL están en sus valores predeterminados.
<br></br>
![Preferencias de TE3](~/content/assets/images/common/SaveToFolderModelAnnotation.png)


### Sobrescritura de la serialización del modelo
Para sustituir la anotación del modelo por sus preferencias, configure las preferencias de serialización y seleccione **Archivo > Guardar en carpeta**. En el cuadro de diálogo de la carpeta, desmarque **Usar configuración de serialización de anotaciones**. El cuadro de diálogo muestra esta casilla de verificación solo para un modelo que tiene la anotación, tanto para los guardados de Database.json como de TMDL. 
<br></br>
![Preferencias de TE3](~/content/assets/images/common/SaveToFolderOverwriteModelAnnotation.png)
