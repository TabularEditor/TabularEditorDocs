---
uid: workspace-mode
title: Modo del área de trabajo
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

Tabular Editor 3 presenta el concepto de **modo del área de trabajo** al crear un nuevo modelo dentro de la herramienta o al cargar un archivo Model.bim o Database.json de un modelo existente.

Al usar el modo del área de trabajo, Tabular Editor sincronizará los cambios en los metadatos del modelo con una **base de datos del área de trabajo**, cada vez que pulses Guardar (Ctrl+S), al mismo tiempo que guarda los cambios de metadatos en el/los archivo(s) del disco.

Idealmente, cada desarrollador de modelos debería usar su propia base de datos del área de trabajo para evitar conflictos durante el desarrollo.

> [!WARNING]
> No habilites la integración con Git en el área de trabajo de Fabric que utilizas para alojar las bases de datos del área de trabajo de Tabular Editor. De este modo evitarás conflictos de Git mientras desarrollas el modelo, ya que Tabular Editor realiza cambios en la base de datos del área de trabajo a través del punto de conexión XMLA, y esos cambios no estarán sincronizados con ninguna rama de Git subyacente.

> [!NOTE]
> Para modelos con nivel de compatibilidad 1200, 1400 o 1500, recomendamos usar una instancia local de Analysis Services para alojar la base de datos del área de trabajo, como la que se incluye con [SQL Server Developer Edition 2019](https://www.microsoft.com/en-us/sql-server/sql-server-downloads).

# Crear un nuevo modelo

Cuando creas un nuevo modelo en Tabular Editor, la opción "Usar base de datos del área de trabajo" está marcada de forma predeterminada:

![Nuevo modelo](~/content/assets/images/new-model.png)

Si lo dejas seleccionado, después de hacer clic en "OK" se te pedirá que te conectes a una instancia de Analysis Services. Esta es la instancia de Analysis Services en la que se implementará tu base de datos del área de trabajo.

> [!IMPORTANT]
> Si planeas implementar tu base de datos del área de trabajo en el punto de conexión XMLA del servicio de Power BI, asegúrate de elegir el nivel de compatibilidad 1609 (Power BI / Fabric) en el cuadro de diálogo anterior.

Después de introducir los datos del servidor de Analysis Services y las credenciales (opcionales), se muestra una lista de todas las bases de datos que residen actualmente en el servidor (o, para un área de trabajo de Power BI, la lista de conjuntos de datos implementados en el área de trabajo):

![Seleccionar base de datos del área de trabajo](~/content/assets/images/select-workspace-database.png)

Tabular Editor sugiere un nuevo nombre único para tu base de datos del área de trabajo, basado en tu nombre de usuario de Windows y la fecha y hora actuales, pero puedes cambiarlo por un nombre más descriptivo.

Después de hacer clic en Aceptar, se crea tu nuevo modelo y se implementa y conecta la base de datos del área de trabajo. En este punto, pulsa Guardar (Ctrl+S) para guardar el modelo como un archivo Model.bim. También puedes elegir Archivo > Guardar en carpeta... elemento de menú si tienes pensado almacenar los metadatos del modelo en un sistema de control de versiones como Git.

![Guardar nuevo en carpeta](~/content/assets/images/save-new-to-folder.png)

En este punto, ya está listo para definir fuentes de datos y agregar nuevas tablas a su modelo. Cada vez que vuelvas a pulsar Guardar (Ctrl+S), la base de datos de Workspace se actualizará con los cambios y también se actualizará el archivo o la carpeta que elegiste anteriormente.

La información sobre la base de datos de Workspace asociada a este modelo se almacena en un archivo Tabular Model User Options (.tmuo) junto al archivo de metadatos del modelo. Vea @user-options para obtener más información.

# Abrir un archivo Model.bim o Database.json

Si abres un archivo Model.bim o Database.json existente, Tabular Editor 3 te preguntará si quieres inicializar una base de datos de Workspace para ese archivo.

![Conectar a la base de datos de Workspace](~/content/assets/images/connect-to-wsdb.png)

Tus opciones son:

- **Sí**: Conéctate a una instancia de Analysis Services y elige una base de datos de Workspace existente o crea una nueva. La próxima vez que cargues el mismo archivo Model.bim o Database.json, Tabular Editor se conectará a la misma base de datos de Workspace. Tabular Editor realizará un despliegue del archivo Model.bim o Database.json en la base de datos de Workspace seleccionada.
- **No**: Tabular Editor cargará los metadatos del archivo sin conexión, sin conectividad con Analysis Services.
- **No volver a preguntar**: Igual que arriba, pero Tabular Editor ya no te preguntará si quieres conectarte a una base de datos de Workspace la próxima vez que abras el mismo archivo Model.bim o Database.json.
- **Cancelar**: El archivo no se cargará en absoluto.

La información sobre si se debe conectar a una base de datos de Workspace para un modelo determinado, así como qué servidor y base de datos de Workspace se deben usar, se almacena en el [archivo Tabular Model User Options (.tmuo)](xref:user-options).

> [!WARNING]
> Al elegir una base de datos de Workspace, Tabular Editor 3 desplegará los metadatos del modelo cargado en esa base de datos de Workspace. Por este motivo, nunca debes usar una base de datos de producción como base de datos de Workspace. Además, recomendamos usar una instancia independiente de Analysis Services o un Workspace de Power BI aparte para las bases de datos de su Workspace.

# Ventajas del modo del área de trabajo

La principal ventaja del modo del área de trabajo es que permite a Tabular Editor mantenerse conectado a una instancia de Analysis Services. En otras palabras, se habilitan las nuevas [funcionalidades conectadas](xref:migrate-from-te2#connected-features) de Tabular Editor 3. Pero incluso si decides no usar estas funcionalidades, es mucho más fácil sincronizar una instancia de Analysis Services con el objetivo de probar tus cambios. Solo tienes que pulsar Guardar (CTRL+S). Esto es similar a cuando Tabular Editor abre directamente los metadatos del modelo desde una instancia de Analysis Services; pero, con el modo del área de trabajo, los metadatos del modelo se guardan simultáneamente en disco.

> [!NOTE]
> Cuando se está ejecutando una operación de actualización, Tabular Editor no puede sincronizar la instancia de Analysis Services (las operaciones de actualización bloquean otras operaciones de escritura). Sin embargo, al pulsar Guardar (CTRL+S) mientras una operación de este tipo está en curso, los metadatos del modelo se seguirán guardando en disco al usar el modo del área de trabajo.

# Desactivar el modo del área de trabajo para un modelo

Si prefieres _deshabilitar el modo del área de trabajo_ y editar un archivo de modelo completamente sin conexión, elige uno de los métodos siguientes.

## Desactivar permanentemente el modo del área de trabajo

1. Localiza el archivo de área de trabajo `.tmuo` del modelo (se encuentra junto a tu archivo `.bim`, `.tmdl` o `.json`) en el Explorador de archivos.

2. Realiza **cualquiera** de las siguientes acciones:
   - **Elimina** el archivo `.tmuo`, **o bien**
   - Ábrelo en un editor de texto y establece:

     ```json
     {
       "UseWorkspaceDatabase": false
     }
     ```

3. Abre el modelo desde el archivo `.bim`, `.tmdl` o `.json` como de costumbre.

A partir de ahora, Tabular Editor permanecerá sin conexión cada vez que cargues este modelo.

## Desactivar el modo del área de trabajo solo para la sesión actual

1. En el cuadro de diálogo **Abrir modelo semántico**, marca la opción **Cargar sin base de datos de Workspace**.

![Cargar sin base de datos de Workspace](~/content/assets/images/load-without-wsdb.png)

El modelo se carga sin conexión durante esta sesión; la próxima vez que lo abras, el modo del área de trabajo se volverá a activar a menos que repitas estos pasos.
