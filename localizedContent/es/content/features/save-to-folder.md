---
uid: save-to-folder
title: Guardar en carpeta
author: Morten Lønskov
updated: 2023-08-08
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
> Puede guardar su modelo de datos en una carpeta usando dos formatos diferentes: JSON o [TMDL](tmdl.md).

Para guardar el modelo en una carpeta, siga estos pasos:

1. Haga clic en Archivo > Guardar en carpeta
2. Elija una carpeta donde desee guardar los archivos del modelo.
3. Haga clic en Guardar. Tabular Editor creará o actualizará los archivos en la carpeta seleccionada, usando el formato JSON o TMDL según se especifique en la configuración de serialización.
4. Ahora puede usar los archivos de la carpeta para control de versiones, despliegue o copia de seguridad.

## Configuración de serialización

La configuración de serialización determina cómo se dividen los objetos del modelo en archivos independientes. En esta configuración también puede definir si desea usar los formatos JSON o TMDL.

### [Preferencias de Tabular Editor 2](#tab/TE2Preferences)

La configuración de serialización se encuentra en Archivo > Preferencias > Serialización. <br></br>
![Preferencias de TE2](~/content/assets/images/common/TE2SaveToFolderSerializationSettings.png)

La configuración mostrada arriba es la establecida como predeterminada al usar Tabular Editor 3, pero no es la que Tabular Editor 2.X establece de forma predeterminada

### [Preferencias de Tabular Editor 3](#tab/TE3Preferences)

La configuración de serialización se encuentra en Herramientas > Preferencia > Formatos de archivo
Las pestañas General y Guardar en carpeta contienen ajustes relacionados con la serialización del modelo. <br></br>
![Preferencias de TE3](~/content/assets/images/common/TE3SaveToFolderSerializationSettings.png)

Tabular Editor 3 tiene una configuración predeterminada para la serialización JSON y debes seleccionar explícitamente otra opción en el modo de serialización, donde también puedes cambiar al formato TMDL.

***

### Anotación de serialización del modelo

Tabular Editor guarda la configuración de serialización en tu modelo para que siempre se mantenga igual, independientemente de quién esté trabajando en el modelo. Esto garantiza que las preferencias locales de un desarrollador no sobrescriban la configuración del modelo ni provoquen una fusión inmanejable en tu control de código fuente. Puede encontrar estas anotaciones en las propiedades del Explorador TOM de Model > Annotations > TabularEditor_SerializeOptions <br></br>
![Anotación del modelo](~/content/assets/images/common/SaveToFolderModelAnnotation.png)

#### Sobrescritura de la serialización del modelo

Si lo deseas, se puede sobrescribir la anotación del modelo. Primero, configura las preferencias de serialización en Tabular Editor y ve a Archivo > Guardar en carpeta.
Esto abrirá el Explorador de Windows y, una vez allí, debe desmarcarse la casilla. <br></br>
![Preferencias de TE3](~/content/assets/images/common/SaveToFolderOverwriteModelAnnotation.png)
