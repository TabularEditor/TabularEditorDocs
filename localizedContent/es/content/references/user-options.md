---
uid: user-options
title: Archivo de opciones de usuario (.tmuo)
author: Daniel Otykier
updated: 2021-09-27
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

# Archivo de opciones de usuario del modelo tabular (.tmuo)

Tabular Editor 3 presenta un nuevo archivo basado en JSON para almacenar preferencias específicas del desarrollador y del modelo. Este archivo se denomina **Tabular Model User Options** y utiliza la extensión **.tmuo**.

Cuando abras un archivo Model.bim o Database.json en Tabular Editor 3, se creará el archivo con el nombre del archivo que cargaste y tu nombre de usuario de Windows. Por ejemplo, si un usuario abre un archivo llamado `AdventureWorks.bim`, el archivo de opciones de usuario se guardará como `AdventureWorks.<UserName>.tmuo`, donde `<UserName>` es el nombre de usuario de Windows del usuario actual. Tabular Editor busca un archivo con ese nombre cada vez que se carga un modelo desde el disco.

> [!IMPORTANT]
> El archivo **.tmuo** contiene preferencias específicas del usuario y, por lo tanto, no debe incluirse en un entorno compartido de control de versiones. Si usas Git para el control de versiones, asegúrate de incluir la extensión `.tmuo` en tu archivo `.gitignore`.

## Contenido del archivo

A continuación se muestra un ejemplo del contenido del archivo:

```json
{
  "UseWorkspace": true,
  "WorkspaceConnection": "provider=MSOLAP;data source=localhost",
  "WorkspaceDatabase": "WorkspaceDB_DanielOtykier_20210904_222118",
  "DataSourceOverrides": {
    "SQLDW": {
      "ConnectionString": {
        "Encryption": "UserKey",
        "EncryptedString": "..."
      },
      "PrivacySetting": "NA"
    }
  },
  "TableImportSettings": {
    "SQLDW": {
      "ServerType": "Sql",
      "UserId": "sqladmin",
      "Password": {
        "Encryption": "UserKey",
        "EncryptedString": "..."
      },
      "Server": "localhost",
      "Database": "AdventureWorksDW2019",
      "Authentication": 0
    }
  }
}
```

En este ejemplo, las propiedades JSON mostradas tienen el siguiente significado:

- `UseWorkspace`: Indica si Tabular Editor debe conectarse a una base de datos del Workspace al cargar el modelo. La base de datos del Workspace se sobrescribirá con los metadatos del archivo cargado o de la estructura de carpetas cargada. Si este valor no está presente, Tabular Editor te preguntará al cargar el modelo si quieres usar una base de datos del Workspace.
- `WorkspaceConnection`: Nombre del servidor de la instancia de Analysis Services o del punto de conexión XMLA de Power BI en el que se implementará la base de datos del Workspace.
- `WorkspaceDatabase`: Nombre de la base de datos del Workspace que se va a implementar. Lo ideal es que sea único para cada desarrollador y modelo.
- `DataSourceOverrides`: Esta estructura puede usarse para especificar propiedades y credenciales alternativas del Data source, que se utilizarán cada vez que se implemente la base de datos del Workspace. Esto es útil si el archivo Model.bim incluye detalles de conexión del Data source que desea sobrescribir para la base de datos de su Workspace; por ejemplo, cuando desea que Analysis Services actualice los datos desde un origen distinto del especificado en el archivo Model.bim.
- `TableImportSettings`: Esta estructura se usa cada vez que se utiliza la funcionalidad [Importar tabla o actualizar esquema](xref:importing-tables) de Tabular Editor. Tabular Editor utiliza las credenciales y la configuración especificadas aquí al establecer una conexión con el origen para explorar las tablas y vistas disponibles, y actualizar el esquema de la tabla importada cuando se hayan realizado cambios en el origen.

Todas las credenciales y cadenas de conexión del archivo .tmuo se cifran con la clave de usuario de Windows. En otras palabras, un archivo .tmuo que contiene datos cifrados no se puede compartir entre varios usuarios.

## Siguientes pasos

- @Workspace-mode