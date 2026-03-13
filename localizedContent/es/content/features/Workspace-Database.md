---
uid: bases-de-datos-del-espacio-de-trabajo
title: Presentamos las bases de datos de Workspace
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Escritorio
          none: true
        - edition: Empresa
          full: true
        - edition: Enterprise
          full: true
---

## Presentamos las bases de datos de Workspace

Tabular Editor 3.0 permite editar los metadatos del modelo cargados desde el disco mientras se mantiene una conexión simultánea a una base de datos implementada en una instancia de Analysis Services. A esta base de datos la llamamos _base de datos de Workspace_. De ahora en adelante, este es el enfoque recomendado para el modelado tabular en Tabular Editor.

Esto simplifica mucho el flujo de trabajo de desarrollo, ya que solo tienes que pulsar Guardar (Ctrl+S) una sola vez para guardar los cambios en el disco **y** actualizar simultáneamente los metadatos en la base de datos de Workspace. Esto también tiene la ventaja de que cualesquiera mensajes de error devueltos por Analysis Services son inmediatamente visibles en Tabular Editor al pulsar Guardar. En cierto modo, es similar a cómo funcionan SSDT / Visual Studio o Power BI Desktop, salvo que tú controlas cuándo se actualiza la base de datos de Workspace.

Cuando cargas un modelo desde un archivo Model.bim o una estructura de carpetas, verás el siguiente aviso:

![image](https://user-images.githubusercontent.com/8976200/58166683-a65db180-7c8a-11e9-9df3-be9a716b3ad1.png)

- **Sí**: Los metadatos del modelo se cargan desde el disco y, a continuación, se implementan inmediatamente en una instancia de Analysis Services. Luego, Tabular Editor se conectará a la base de datos recién implementada. La próxima vez que se cargue el mismo modelo desde el disco, Tabular Editor volverá a implementarlo y se conectará a la base de datos automáticamente.
- **No**: Los metadatos del modelo se cargan desde el disco en Tabular Editor como siempre, sin conectarse a una instancia de Analysis Services.
- **No, no preguntar de nuevo**: Igual que la opción anterior, pero Tabular Editor no volverá a preguntar la próxima vez que se cargue el mismo modelo.

### Configurar una base de datos de Workspace

Cuando seleccionas la opción "Sí" en el aviso mostrado arriba, se te pedirá un nombre de servidor y credenciales (opcionales) para una instancia de Analysis Services. Al hacer clic en "OK", verás una lista de las bases de datos que ya existen en la instancia. Tabular Editor asume que quieres desplegar una nueva base de datos y proporciona un nombre predeterminado para ella, basado en tu nombre de usuario de Windows y la fecha y hora actuales:

![image](https://user-images.githubusercontent.com/8976200/58179509-a10f5f80-7ca8-11e9-9764-4cb76b9d1a8b.png)

Si desea usar una base de datos existente como base de datos de Workspace, simplemente selecciónela en la lista. **Advertencia: Si elige una base de datos existente, se sobrescribirá con los metadatos del modelo cargado desde el disco. Por este motivo, no se recomienda configurar bases de datos de Workspace en una instancia de producción!**

### El archivo de opciones de usuario (.tmuo)

Para realizar un seguimiento de la configuración de Workspace de cada modelo en su sistema de archivos, Tabular Editor 3.0 introduce un nuevo archivo de tipo .tmuo (abreviatura de Tabular Model User Options), que se colocará junto al archivo Model.bim o al archivo Database.json.

El archivo .tmuo es un simple documento JSON con el siguiente contenido:

```json
{
  "UseWorkspace": true,
  "WorkspaceConnection": "Data Provider=MSOLAP;Data Source=localhost",
  "WorkspaceDatabase": "AdventureWorks_WS_Feature123"
}
```

Al cargar metadatos del modelo desde el disco, Tabular Editor busca la presencia de un archivo .tmuo en el mismo directorio que el archivo de modelo cargado. El nombre del archivo .tmuo debe seguir el patrón:

```
<modelfilename>.<windowsusername>.tmuo
```

El archivo incluye un nombre de usuario para evitar que varios desarrolladores sobrescriban sin darse cuenta las bases de datos de Workspace de otros en flujos de trabajo de desarrollo en paralelo. Si el archivo está presente y el indicador "UseWorkspace" del archivo está establecido en "true", Tabular Editor realizará los siguientes pasos al cargar un modelo desde el disco:

1. Desplegar los metadatos del modelo en la base de datos de Workspace (sobrescribiendo los metadatos existentes), usando el nombre del servidor y el de la base de datos especificados en el archivo .tmuo.
2. Conectarse a la base de datos recién implementada en "modo del área de trabajo".

En "modo del área de trabajo", Tabular Editor guarda simultáneamente su modelo en disco y actualiza la base de datos de Workspace cada vez que pulsa Guardar (ctrl+s). Esto le permite probar rápidamente código nuevo y ver los mensajes de error proporcionados por Analysis Services, sin tener que desplegar manualmente la base de datos ni invocar Archivo > Guardar como... o Archivo > Guardar en carpeta... siempre que desee guardar los metadatos del modelo en el disco.
