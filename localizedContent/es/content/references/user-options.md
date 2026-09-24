---
uid: user-options
title: Archivo de opciones de usuario (.tmuo)
author: Daniel Otykier
updated: 2026-09-15
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

Cuando abres un modelo desde el disco, el archivo se crea junto a él y se nombra según el modelo y tu nombre de usuario de Windows. Tabular Editor busca un archivo con ese nombre cada vez que se carga un modelo desde el disco.

| Lo que abriste                                                                                             | Archivo de opciones de usuario             |
| ---------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| `SpaceParts.bim`, o cualquier archivo `.bim` / `.pbit` / `Database.json`                                   | `SpaceParts.<UserName>.tmuo`, junto a él   |
| Un archivo `model.tmdl` o `database.tmdl`                                                                  | `model.<UserName>.tmuo`, junto a él        |
| Una carpeta que contiene `Database.json`                                                                   | `database.<UserName>.tmuo`, en esa carpeta |
| Una carpeta que contiene archivos de modelo en Tabular Model Definition Language (TMDL) | `model.<UserName>.tmuo`, en esa carpeta    |

TMDL siempre usa el prefijo `model` para mantener la continuidad con las versiones anteriores a `database.tmdl`.

Para un modelo abierto a través de una conexión, en lugar de desde el disco, no hay ningún lugar junto al modelo donde colocar el archivo, así que se guarda por servidor y por base de datos en `%LocalAppData%\\TabularEditor3\\UserOptions\\`.

La opción _Crear archivo de opciones de usuario (.tmuo)_ en @preferencias determina si se crea o no el archivo para un modelo nuevo.

> [!IMPORTANT]
> El archivo **.tmuo** contiene preferencias específicas del usuario y, por lo tanto, no debe incluirse en un entorno compartido de control de versiones. Si usas Git para el control de versiones, asegúrate de incluir la extensión `.tmuo` en tu archivo `.gitignore`.

## Contenido del archivo

El archivo es JSON y todas las propiedades son opcionales. Tabular Editor solo crea uno cuando hay algo que guardar, así que un archivo real contiene solo algunos de los bloques siguientes, no todos. Si no hay nada que guardar, no se escribe ningún archivo.

Un archivo mínimo, para un modelo que no hace nada más que conectarse a una base de datos de Workspace:

```json
{
  "UseWorkspace": true,
  "WorkspaceConnection": {
    "ConnectionString": "Data source=localhost",
    "EncryptedCredentials": "AQAAANCMnd8BFdERjHoAwE..."
  },
  "WorkspaceDatabase": "WorkspaceDB_MyUser_20260915"
}
```

### Propiedades de nivel superior

| Propiedad                     | Tipo            | Se escribe cuando                                                                                                                                                                           |
| ----------------------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `UseWorkspace`                | Booleano        | Ya has respondido a la pregunta sobre Workspace para este modelo. Mientras no esté presente, Tabular Editor te lo pregunta cada vez que se carga el modelo. |
| `WorkspaceConnection`         | Cadena u objeto | Se ha configurado una conexión a Workspace. Forma de objeto cuando la cadena de conexión incluye una contraseña.                                            |
| `WorkspaceConnectionAuthMode` | Cadena          | Heredado y solo cuando no es `Integrated`. Ahora el modo de autenticación viene implícito en la cadena de conexión.                                         |
| `WorkspaceDatabase`           | Cadena          | Se ha configurado un nombre de base de datos para Workspace.                                                                                                                |
| `Deployment`                  | Objeto          | Se ha ejecutado el Asistente de implementación para este modelo.                                                                                                            |
| `DataSourceOverrides`         | Objeto          | Se ha definido al menos una anulación de Data source.                                                                                                                       |
| `TableImportSettings`         | Objeto          | Al menos un Data source tiene configuración de importación.                                                                                                                 |
| `RefreshOverrides`            | Objeto          | Se ha definido al menos un perfil de reemplazo de actualización.                                                                                                            |
| `AIConsent`                   | Objeto          | Legado. Se lee cuando está presente; nunca se vuelve a escribir.                                                                                            |
| `Permissions`                 | Objeto          | Se ha concedido al menos una concesión de IA por modelo.                                                                                                                    |

Aparecen en ese orden.

### Base de datos del Workspace

- `UseWorkspace` decide si Tabular Editor se conecta a una base de datos del Workspace al cargar el modelo. La base de datos del Workspace se sobrescribe con los metadatos del archivo cargado o de la estructura de carpetas.
- `WorkspaceConnection` es la instancia de Analysis Services o el punto de conexión XMLA de Power BI en el que se implementa la base de datos del Workspace.
- `WorkspaceDatabase` es el nombre de esa base de datos del Workspace. Debe ser único para cada desarrollador y cada modelo, ya que la idea es que cada desarrollador tenga el suyo.

### Sobrescrituras del Data source

`DataSourceOverrides` se usa para proporcionar a la base de datos del Workspace detalles de conexión distintos a los del archivo del modelo, de modo que Analysis Services actualice desde un origen diferente al indicado por el modelo.

| Propiedad           | Tipo           | Se escribe cuando                                                                                                                                                                                             |
| ------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ImpersonationMode` | Cadena         | Distinto de `Default`. Uno de `Default`, `ImpersonateAccount`, `ImpersonateAnonymous`, `ImpersonateCurrentUser`, `ImpersonateServiceAccount`, `ImpersonateUnattendedAccount`. |
| `Username`          | Cadena         | Se establece.                                                                                                                                                                                 |
| `ConnectionString`  | Objeto cifrado | Al establecerse.                                                                                                                                                                              |
| `Password`          | Objeto cifrado | Al establecerse.                                                                                                                                                                              |
| `AccountKey`        | Objeto cifrado | Al establecerse. Se usa para orígenes de almacenamiento de blobs.                                                                                                             |
| `PrivacySetting`    | Cadena         | Al establecerse.                                                                                                                                                                              |

Una anulación cuya Data source ya no exista en el modelo se elimina la próxima vez que se escriba el archivo, y otra cuya Data source se haya cambiado de nombre seguirá ese cambio.

### Configuración de importación de tablas

`TableImportSettings` se usa al ejecutar [Importar tabla o actualizar esquema](xref:importing-tables) para explorar las tablas y vistas disponibles y detectar los cambios en el esquema de origen.

| Propiedad                             | Tipo              | Se escribe cuando                                                                                                                                                                                                  |
| ------------------------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `ServerType`                          | Cadena            | Siempre. Uno de `Sql`, `Oracle`, `Odbc`, `OleDb`, `Snowflake`, `Dataflow`, `PostgreSql`, `MySql`, `MariaDb`, `Db2`, `Databricks`, `OneLake`.                                       |
| `Options`                             | Objeto de cadenas | La colección no está vacía.                                                                                                                                                                        |
| `UserId`                              | Cadena            | Configurado.                                                                                                                                                                                       |
| `Contraseña`                          | Objeto cifrado    | Configurado, _y_ elegiste guardarlo.                                                                                                                                                               |
| `Proveedor`                           | Cadena            | `ServerType` es `OleDb`.                                                                                                                                                                           |
| `PasswordKey`, `UserIdKey`            | Cadena            | `ServerType` es `OleDb` y el valor correspondiente está configurado.                                                                                                                               |
| `Servidor`                            | Cadena            | `ServerType` no es `Odbc` y está configurado.                                                                                                                                                      |
| `ServerKey`, `DatabaseKey`            | Cadena            | `ServerType` no es `Sql` y el valor está configurado.                                                                                                                                              |
| `Base de datos`                       | Cadena            | Configurado.                                                                                                                                                                                       |
| `Autenticación`                       | Cadena            | `ServerType` es `Sql`, `OleDb` o `Databricks`. Uno de `Sql`, `WindowsIntegrated`, `AadInteractive`, `AadPassword`, `AadIntegrated`, `AadServicePrincipal`, `AccessToken`, `OAuth`. |
| `Cifrar`                              | Booleano          | Se establece en cualquiera de los dos casos.                                                                                                                                                       |
| `Dsn`                                 | Cadena            | Se establece. Se usa para ODBC.                                                                                                                                                    |
| `RowLimitClause`, `IdentifierQuoting` | Número            | No tienen sus valores predeterminados.                                                                                                                                                             |
| `Schema`                              | Cadena            | Se establece.                                                                                                                                                                                      |

`Options` es donde se guarda todo lo específico de un proveedor, como cadenas de texto sin formato: un Warehouse de Snowflake es `Options.warehouse`; un Workspace de OneLake es `Options.workspaceid`. Las propiedades `…Key` son los _nombres_ de las claves de la cadena de conexión, como `PWD`, no valores secretos.

`Password` es el único valor cifrado aquí. `UserId`, `Server`, `Database`, `Dsn` y todo lo que hay en `Options` se almacena como texto sin formato, así que trata el archivo como confidencial incluso cuando no contenga ninguna contraseña. Un token de acceso de Power BI se almacena como `Password` y está cifrado.

### Implementación

`Deployment` contiene la última configuración que usó el Asistente de implementación para este modelo. Las seis opciones booleanas siempre se escriben una vez que existe el bloque, tanto si son verdaderas como falsas:

| Propiedad                       | Tipo            | Se escribe cuando                                                                                                                            |
| ------------------------------- | --------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `DeployDataSources`             | Booleano        | Siempre                                                                                                                                      |
| `Desplegar particiones`         | Booleano        | Siempre                                                                                                                                      |
| `DeployRefreshPolicyPartitions` | Booleano        | Siempre                                                                                                                                      |
| `DeployModelRoles`              | Booleano        | Siempre                                                                                                                                      |
| `DeployModelRoleMembers`        | Booleano        | Siempre                                                                                                                                      |
| `DeploySharedExpressions`       | Booleano        | Siempre                                                                                                                                      |
| `TargetConnectionString`        | Cadena u objeto | Siempre; `null` si no está configurado. Forma de objeto cuando la cadena de conexión incluye una contraseña. |
| `TargetDatabase`                | Cadena          | Siempre; `null` si no está configurado.                                                                                      |
| `TargetCredentials`             | Objeto          | Se han establecido tanto un nombre de usuario como una contraseña.                                                           |

### Anulaciones de actualización

`RefreshOverrides` se indexa por el nombre del perfil, y esa clave es el único lugar donde se guarda el nombre. Cada perfil contiene una única matriz `Overrides` que describe qué cambia el perfil cuando se ejecuta. Consulta @refresh-overrides para ver qué hacen los perfiles y cómo definirlos.

```json
"RefreshOverrides": {
  "Nightly": {
    "Overrides": [
      {
        "scope": { "table": "Sales" },
        "partitions": [
          {
            "originalObject": { "table": "Sales", "partition": "Sales-2025" },
            "source": { "query": "SELECT * FROM dbo.FactSales WHERE Year = 2025" }
          }
        ]
      }
    ]
  }
}
```

### Permisos de IA por modelo

`Permissions` registra las concesiones de permisos de IA que se aplican solo a este modelo, y se escribe cuando respondes **Permitir para este modelo** en una tarjeta de permisos del @ai-assistant.

```json
"Permissions": {
  "Grants": { "ModelMetadata": "Write", "ModelData": "Read" },
  "LastGrantedAt": "2026-09-15T08:12:44.117Z"
}
```

`Grants` contiene una entrada por cada recurso al que has concedido permisos: `ModelMetadata`, `ModelData`, `Bpa`, `Documents` o `Macros`, cada uno establecido en `Deny`, `Read` o `Write`. Esto eleva tu concesión de permisos vigente para el chat mientras este modelo esté abierto. El servidor MCP solo lee los permisos globales, así que nada de esto le llega.

### Cómo se cifran las credenciales

Todo lo sensible se cifra con la API de protección de datos de Windows bajo tu propia cuenta de usuario, así que un archivo que contiene datos cifrados no se puede compartir con otro usuario ni mover a otro equipo. Aparecen tres formas, según lo que se esté protegiendo:

Una cadena de conexión sin contraseña no se cifra en absoluto y permanece como una cadena JSON en texto plano, por eso `WorkspaceConnection` aparece de ambas formas en la práctica.

Si no se puede descifrar un valor, por ejemplo porque el archivo procede de otro usuario, el valor se lee como vacío en lugar de hacer que falle la carga.

## Cuando no se puede leer el archivo

Un modelo se abre con o sin un archivo `.tmuo`.

Si el archivo no se puede deserializar, por ejemplo porque se editó manualmente y quedó como JSON no válido, Tabular Editor muestra una advertencia titulada _Error al cargar el archivo de opciones de usuario (.tmuo)_, que incluye el error subyacente, y luego abre el modelo con las opciones predeterminadas. No se pierde nada del modelo en sí; pierdes la configuración que contenía el archivo, y en el siguiente guardado se escribirá uno nuevo.

## Siguientes pasos

- @Workspace-mode