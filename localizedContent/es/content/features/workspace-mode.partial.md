---
uid: workspace-mode
title: Modo del área de trabajo
author: Morten Lønskov
updated: 2026-09-23
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

## Modo del área de trabajo

En el **modo del área de trabajo**, Tabular Editor 3 conecta un modelo cargado desde un archivo con una **base de datos de Workspace**. El modo del área de trabajo está disponible cuando creas un modelo nuevo o cargas el archivo Model.bim o Database.json de un modelo existente.

Cuando guardas (**Ctrl+S**), Tabular Editor escribe los cambios de metadatos en el/los archivo(s) del disco y los sincroniza con la base de datos del Workspace.

Asigna a cada desarrollador del modelo su propia base de datos de Workspace, porque una compartida provoca conflictos entre desarrolladores.

> [!WARNING]
> No habilites la integración con Git en el Workspace de Fabric que aloja las bases de datos de Workspace de Tabular Editor. Tabular Editor modifica la base de datos de Workspace a través del punto de conexión XMLA, y esos cambios provocan conflictos de Git con la rama conectada.

> [!NOTE]
> Para modelos con nivel de compatibilidad 1200, 1400 o 1500, aloja la base de datos de Workspace en una instancia local de Analysis Services, como la incluida con [SQL Server Developer Edition 2019](https://www.microsoft.com/en-us/sql-server/sql-server-downloads).

## Crear un nuevo modelo

Cuando creas un nuevo modelo en Tabular Editor, la opción **Usar base de datos de Workspace** está seleccionada de forma predeterminada:

![Nuevo modelo](~/content/assets/images/new-model.png)

Con la opción seleccionada, después de hacer clic en **OK** aparece un cuadro de diálogo para conectarte a una instancia de Analysis Services. Tabular Editor implementa la base de datos de Workspace en esta instancia.

> [!IMPORTANT]
> Si implementas tu base de datos de Workspace en el punto de conexión XMLA del servicio de Power BI, selecciona el nivel de compatibilidad **1706 (Power BI / Fabric)** en el cuadro de diálogo anterior.

Después de introducir los detalles del servidor y, opcionalmente, las credenciales, aparece una lista de las bases de datos del servidor. Para un Workspace de Power BI, la lista muestra los modelos semánticos implementados en el Workspace:

![Seleccionar base de datos del área de trabajo](~/content/assets/images/select-workspace-database.png)

Tabular Editor sugiere un nombre único para la base de datos de Workspace, basado en tu nombre de usuario de Windows y en la fecha y hora actuales, y puedes cambiarlo.

Haz clic en **OK** para crear el modelo, implementar la base de datos de Workspace y conectarla. Después, pulsa **Ctrl+S** para guardar el modelo como un archivo Model.bim, o selecciona **Archivo > Guardar en carpeta...** para almacenar los metadatos en un sistema de control de versiones como Git.

![Guardar nuevo en carpeta](~/content/assets/images/save-new-to-folder.png)

Ahora puedes definir los Data sources y agregar tablas al modelo. Cada vez que guardas, se actualizan tanto la base de datos de Workspace como el archivo o la carpeta que hayas elegido.

Tabular Editor almacena los detalles de la base de datos de Workspace del modelo en un archivo Tabular Model User Options (.tmuo) junto al archivo de metadatos del modelo. Consulta @user-options.

## Abrir un archivo Model.bim o Database.json

Cuando abres un archivo Model.bim o Database.json existente, se te pregunta si quieres conectar una base de datos de Workspace a ese archivo.

![Conectar a la base de datos de Workspace](~/content/assets/images/connect-to-wsdb.png)

Las opciones son:

- **Sí**: conéctate a una instancia de Analysis Services y elige una base de datos de Workspace existente o crea una. Tabular Editor implementa los metadatos del archivo en la base de datos de Workspace seleccionada y se conecta a esa misma base de datos la próxima vez que cargues el archivo.
- **No**: carga los metadatos sin conexión, sin conectarse a Analysis Services.
- **No volver a preguntar**: carga sin conexión y no vuelve a mostrar el aviso para este archivo.
- **Cancelar**: no cargues el archivo.

Tabular Editor guarda la opción seleccionada, así como el servidor y la base de datos del Workspace, en el [archivo Tabular Model User Options (.tmuo)](xref:user-options).

> [!WARNING]
> Tabular Editor 3 despliega los metadatos del modelo cargado en la base de datos del Workspace que elijas. Nunca uses una base de datos de producción como base de datos del Workspace. Usa una instancia independiente de Analysis Services o un Workspace independiente de Power BI para las bases de datos del Workspace.

## Ventajas del modo del área de trabajo

En el modo del área de trabajo, Tabular Editor permanece conectado a una instancia de Analysis Services, lo que habilita las [funciones conectadas](xref:migrate-from-te2#connected-features) de Tabular Editor 3. Cada vez que guardas (**Ctrl+S**), tus cambios también se despliegan en la instancia para probarlos. Abrir un modelo directamente desde Analysis Services funciona igual, excepto que el modo del área de trabajo también guarda los metadatos en disco.

> [!NOTE]
> Cuando se está ejecutando una operación de actualización, Tabular Editor no puede sincronizar la instancia de Analysis Services, porque las operaciones de actualización bloquean otras operaciones de escritura. Si guardas durante una actualización, los metadatos del modelo se siguen escribiendo en disco.

## Desactivar el modo del área de trabajo para un modelo

Puedes deshabilitar el modo del área de trabajo para un modelo de forma permanente o para la sesión actual, y editar el archivo del modelo sin conexión.

### Desactivar permanentemente el modo del área de trabajo

1. En el Explorador de archivos, busca el archivo `.tmuo` del modelo junto al archivo `.bim`, `.tmdl` o `.json`.

2. Elimina el archivo `.tmuo` o ábrelo en un editor de texto y establece:

   ```json
   {
     "UseWorkspaceDatabase": false
   }
   ```

3. Abre el modelo desde el archivo `.bim`, `.tmdl` o `.json`.

A partir de entonces, Tabular Editor carga el modelo sin conexión.

### Desactivar el modo del área de trabajo solo para la sesión actual

1. En el cuadro de diálogo **Abrir modelo semántico**, selecciona **Cargar sin base de datos del Workspace**.

![Cargar sin base de datos de Workspace](~/content/assets/images/load-without-wsdb.png)

El modelo se carga sin conexión para esta sesión, y el modo del área de trabajo vuelve a habilitarse la próxima vez que lo abras.
