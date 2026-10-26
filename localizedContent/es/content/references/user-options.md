---
uid: user-options
title: Archivo de opciones de usuario (.tmuo)
author: Daniel Otykier
updated: 2026-10-12
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

Tabular Editor 3 introduce un nuevo archivo basado en JSON para almacenar las preferencias específicas del desarrollador y del modelo. Este archivo se denomina archivo de **Opciones de usuario del modelo tabular** y utiliza la extensión **.tmuo**.

Cuando abre un modelo desde el disco, el archivo se crea junto a él, con el mismo nombre que el modelo y con su nombre de usuario de Windows. Tabular Editor busca un archivo con ese nombre cada vez que se carga un modelo desde el disco.

| Lo que ha abierto | Archivo de opciones de usuario |
|---|---|
| `SpaceParts.bim`, o cualquier archivo `.bim` / `.pbit` / `database.json` | `SpaceParts.<Nombre de usuario>.tmuo`, junto a él |
| Un archivo «model.tmdl» o «database.tmdl» | «model.<Nombre de usuario>.tmuo`, junto a él |
| Una carpeta que contiene `database.json` | `database.<Nombre de usuario>.tmuo`, en esa carpeta |
| Una carpeta que contiene archivos de modelo del Lenguaje de definición de modelo tabular (TMDL) | `model.<Nombre de usuario>.tmuo`, en esa carpeta |

TMDL siempre utiliza el prefijo «model», para mantener la continuidad con las versiones anteriores a «database.tmdl».

En el caso de un modelo abierto a través de una conexión y no desde el disco, no hay ningún lugar aparte del modelo donde colocar el archivo, por lo que se guarda por servidor y base de datos en `%LocalAppData%\TabularEditor3\UserOptions\`.

El hecho de que se cree o no el archivo para un nuevo modelo se rige por *Crear archivo de opciones de usuario (.tmuo)* en @preferencias.

> [!IMPORTANT]
> El archivo **.tmuo** contiene preferencias específicas del usuario y, como tal, no debe incluirse en un entorno de control de versiones compartido. Si utiliza Git para el control de versiones, asegúrese de incluir la extensión `.tmuo` en su archivo `.gitignore`.

## Contenido del archivo

El archivo es JSON y todas las propiedades son opcionales. Tabular Editor solo escribe uno cuando hay algo que almacenar, por lo que un archivo real contiene unos pocos de los bloques que se muestran a continuación, en lugar de todos ellos. Si no hay nada que almacenar, no se escribe ningún archivo.

Un archivo mínimo, para un modelo que no hace nada más que conectarse a una base de datos del área de trabajo:

```json
{
  "UseWorkspace": true,
  "WorkspaceConnection": {
    "ConnectionString": "data source=localhost",
    "EncryptedCredentials": "AQAAANCMnd8BFdERjHoAwE..."
  },
  "WorkspaceDatabase": "WorkspaceDB_MyUser_20260915"
}
```

### Propiedades de nivel superior

| Propiedad | Tipo | Se escribe cuando |
|---|---|---|
| `UseWorkspace` | Booleano | Ha respondido a la pregunta sobre el espacio de trabajo para este modelo. Mientras no esté presente, Tabular Editor lo preguntará cada vez que se cargue el modelo. |
| `WorkspaceConnection` | Cadena u objeto | Se establece una conexión al espacio de trabajo. Formato de objeto cuando la cadena de conexión contiene una contraseña. |
| `WorkspaceConnectionAuthMode` | Cadena | Heredado, y solo cuando no es `Integrated`. El modo de autenticación ahora está implícito en la cadena de conexión. |
| `WorkspaceDatabase` | Cadena | Se establece un nombre de base de datos del área de trabajo. |
| `Deployment` | Objeto | El asistente de implementación se ha ejecutado con este modelo. |
| `DataSourceOverrides` | Objeto | Se ha definido al menos una anulación de origen de datos. |
| `TableImportSettings` | Objeto | Al menos un origen de datos tiene configuración de importación. |
| `RefreshOverrides` | Objeto | Se ha definido al menos un perfil de anulación de actualización. |
| `AIConsent` | Objeto | Obsoleto. Se lee cuando está presente, nunca se vuelve a escribir. |
| `Permissions` | Objeto | Se ha concedido al menos un permiso de IA por modelo. |

Aparecen en ese orden.

### Base de datos del área de trabajo

- `UseWorkspace` decide si Tabular Editor se conecta a una base de datos de área de trabajo cuando carga el modelo. La base de datos del área de trabajo se sobrescribe con los metadatos del archivo cargado o de la estructura de carpetas.
- `WorkspaceConnection` es la instancia de Analysis Services o el punto de conexión XMLA de Power BI en la que se implementa la base de datos del área de trabajo.
- `WorkspaceDatabase` es el nombre de esa base de datos. Haga que sea único para cada desarrollador y para cada modelo, ya que la idea es que cada desarrollador tenga el suyo propio.

### Anulaciones de origen de datos

`DataSourceOverrides` se utiliza para proporcionar a la base de datos del área de trabajo detalles de conexión distintos de los del archivo del modelo, de modo que Analysis Services se actualice desde un lugar distinto del indicado por el modelo.

| Propiedad | Tipo | Se escribe cuando |
|---|---|---|
| `ImpersonationMode` | Cadena | No es `Default`. Uno de `Default`, `ImpersonateAccount`, `ImpersonateAnonymous`, `ImpersonateCurrentUser`, `ImpersonateServiceAccount`, `ImpersonateUnattendedAccount`. |
| `Username` | Cadena | Establecido. |
| `ConnectionString` | Objeto cifrado | Establecido. |
| `Password` | Objeto cifrado | Establecido. |
| `AccountKey` | Objeto cifrado | Establecido. Se utiliza para orígenes de almacenamiento de blobs. |
| `PrivacySetting` | Cadena | Establecer. |

Una anulación cuyo origen de datos ya no exista en el modelo se eliminará la próxima vez que se escriba el archivo, y una cuyo origen de datos se haya renombrado seguirá el cambio de nombre.

### Configuración de importación de tablas

`TableImportSettings` se utiliza cuando ejecuta [Importar tabla o actualización de esquema](xref:importing-tables), para explorar las tablas y vistas disponibles y para recoger los cambios del esquema de origen.

| Propiedad | Tipo | Se escribe cuando |
|---|---|---|
| `ServerType` | Cadena | Siempre. Uno de los siguientes: `Sql`, `Oracle`, `Odbc`, `OleDb`, `Snowflake`, `Dataflow`, `PostgreSql`, `MySql`, `MariaDb`, `Db2`, `Databricks`, `OneLake`. |
| `Options` | Objeto de cadenas | El conjunto no está vacío. |
| `UserId` | Cadena | Establecido. |
| `Password` | Objeto cifrado | Se ha establecido *y* ha optado por guardarlo. |
| `Provider` | Cadena | `ServerType` es `OleDb`. |
| `PasswordKey`, `UserIdKey` | Cadena | `ServerType` es `OleDb` y el valor correspondiente está establecido. |
| `Server` | Cadena | `ServerType` no es `Odbc` y está establecido. |
| `ServerKey`, `DatabaseKey` | Cadena | `ServerType` no es `Sql` y el valor está establecido. |
| `Database` | Cadena | Establecida. |
| `Authentication` | Cadena | `ServerType` es `Sql`, `OleDb` o `Databricks`. Uno de `Sql`, `WindowsIntegrated`, `AadInteractive`, `AadPassword`, `AadIntegrated`, `AadServicePrincipal`, `AccessToken`, `OAuth`. |
| `Encrypt` | Booleano | Establecido de una forma u otra. |
| `Dsn` | Cadena | Establecido. Se utiliza para ODBC. |
| `RowLimitClause`, `IdentifierQuoting` | Número | No con sus valores predeterminados. |
| `Schema` | Cadena | Establecida. |

En `Options` es donde acaba todo lo específico de un proveedor, como cadenas simples: un almacén de Snowflake es `Options.warehouse`, un espacio de trabajo de OneLake es `Options.workspaceid`. Las propiedades «…Key» son los *nombres* de las claves de la cadena de conexión, como «PWD», no secretos.

`Password` es el único valor cifrado aquí. `UserId`, `Server`, `Database`, `Dsn` y todo lo que hay en `Options` se almacenan como texto sin formato, por lo que debe tratar el archivo como confidencial incluso cuando no contenga ninguna contraseña. Un token de acceso de Power BI se almacena como «Password» y está cifrado.

### Implementación

`Deployment` contiene lo que el asistente de implementación utilizó por última vez para este modelo. Las siete opciones booleanas siempre se escriben una vez que existe el bloque, tanto si son true como si son false:

| Propiedad | Tipo | Se escribe cuando |
|---|---|---|
| `DeployDataSources` | Booleano | Siempre |
| `DeployPartitions` | Booleano | Siempre |
| `DeployRefreshPolicyPartitions` | Booleano | Siempre |
| `DeployModelRoles` | Booleano | Siempre |
| `DeployModelRoleMembers` | Booleano | Siempre |
| `DeploySharedExpressions` | Booleano | Siempre |
| `DeployLinguisticMetadata` | Booleano | Siempre |
| `TargetConnectionString` | Cadena u objeto | Siempre, `null` si no se establece. Formato de objeto cuando la cadena de conexión contiene una contraseña. |
| `TargetDatabase` | Cadena | Siempre, `null` si no se establece. |
| `TargetCredentials` | Objeto | Se establecen tanto un nombre de usuario como una contraseña. |

### Anulaciones de actualización

`RefreshOverrides` se indexa por nombre de perfil, y esa clave es el único lugar donde se almacena el nombre. Cada perfil contiene una única matriz `Overrides` que describe qué cambia el perfil cuando se ejecuta. Consulta @refresh-overrides para saber qué hacen los perfiles y cómo definirlos.

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

`Permissions` registra las concesiones de permisos de IA que se aplican únicamente a este modelo, escritas cuando responde **Permitir para este modelo** en una tarjeta de permisos del @ai-assistant.

```json
"Permissions": {
  "Grants": { "ModelMetadata": "Write", "ModelData": "Read" },
  "LastGrantedAt": "2026-09-15T08:12:44.117Z"
}
```

`Grants` contiene una entrada por cada recurso que haya concedido: `ModelMetadata`, `ModelData`, `Bpa`, `Documents` o `Macros`, cada una configurada como `Deny`, `Read` o `Write`. Estos aumentan su concesión permanente para el chat mientras este modelo esté abierto. El servidor MCP solo lee los permisos globales, por lo que nada de lo que aparece aquí llega a él.

### Cómo se cifran las credenciales

Todos los datos confidenciales se cifran con la API de protección de datos de Windows bajo su propia cuenta de usuario, por lo que un archivo que contenga datos cifrados no se puede compartir con otro usuario ni trasladar a otro equipo. Aparecen tres formas, según lo que se esté protegiendo:

Una cadena de conexión que no contiene ninguna contraseña no está cifrada en absoluto y sigue siendo una cadena JSON sin formato, por lo que `WorkspaceConnection` aparece de ambas formas en la práctica.

Si un valor no se puede descifrar, por ejemplo, porque el archivo procede de otro usuario, el valor se lee como vacío en lugar de producir un error en la carga.

## Cuando no se puede leer el archivo

Un modelo se abre con o sin un archivo `.tmuo`.

Si el archivo no se puede deserializar, por ejemplo, porque se ha editado manualmente y ha quedado como un JSON no válido, Tabular Editor muestra una advertencia titulada *Error al cargar el archivo de opciones de usuario (.tmuo)* que contiene el error subyacente, y luego abre el modelo con las opciones predeterminadas. No se pierde nada del modelo en sí; se pierden los ajustes que contenía el archivo, y la siguiente vez que se guarde se escribirá uno nuevo.

## Próximos pasos

- @workspace-mode