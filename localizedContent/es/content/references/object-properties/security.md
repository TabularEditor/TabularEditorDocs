---
uid: object-properties-security
title: Propiedades de roles y seguridad
author: Jeroen ter Heerdt
updated: 2026-10-09
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Propiedades de roles y seguridad

<!--
SUMMARY: Reference for the properties of roles, table permissions and role members, which define row-level and object-level security.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

Esta página describe las propiedades de los roles, los permisos de tabla y los miembros de cada rol. Un permiso de tabla contiene la configuración de seguridad de un rol para una tabla. Para las propiedades que comparten la mayoría de los objetos, consulta @object-properties-common.

La seguridad de un modelo semántico se define mediante los roles. Un rol concede a sus miembros un nivel de acceso al modelo y restringe lo que ven mediante:

- **seguridad a nivel de filas (RLS)**, que filtra las filas de una tabla con una expresión DAX para cada tabla, por ejemplo, para que un responsable de ventas vea solo las ventas de su propia región
- **seguridad a nivel de objetos (OLS)**, que oculta tablas o columnas completas, incluidos sus metadatos, por ejemplo, una columna de salarios que solo puede ver RR. HH. OLS requiere un nivel de compatibilidad 1400 o superior.

El Tabular Object Model (TOM) almacena ambos para cada tabla, en un _permiso de tabla_ del rol. También puedes editarlos desde el lado de la tabla: en una tabla, `RowLevelSecurity` y `ObjectLevelSecurity` muestran la configuración de cada rol (consulta @object-properties-tables), y en una columna, `ObjectLevelSecurity` hace lo mismo (consulta @object-properties-columns). Independientemente de cómo los edites, Tabular Editor crea los permisos de tabla cuando son necesarios.

Consulta @data-security-about, @data-security-setup-rls, @data-security-setup-ols, @data-security-testing y @roles-and-rls.

## Rol

Un rol es un conjunto de permisos con nombre, junto con los usuarios y grupos que los reciben. Un usuario que es miembro de varios roles obtiene la unión de lo que permiten los roles: si un rol filtra una tabla y otro no, el usuario ve todas las filas. Añadir un usuario a un rol adicional solo puede ampliar lo que puede ver.

Los miembros de los roles de administrador del modelo y los usuarios con acceso de escritura al Workspace de Power BI no están restringidos por RLS ni por OLS. En Power BI, RLS y OLS se aplican solo a los usuarios con el rol **Visor** del Workspace, y no a los roles **Administrador**, **Miembro** y **Colaborador**, que tienen permisos de edición en el modelo semántico (consulta la documentación de Microsoft: [seguridad a nivel de filas (RLS) con Power BI](https://learn.microsoft.com/fabric/security/service-admin-row-level-security)). Prueba la seguridad con un usuario que solo tenga acceso de lectura o con las funciones de suplantación de roles de @data-security-testing.

### Propiedades comunes

- [Nombre](xref:object-properties-common#name)
- [Descripción](xref:object-properties-common#description)
- [Anotaciones](xref:object-properties-common#annotations)
- [Propiedades extendidas](xref:object-properties-common#extended-properties)
- [Tipo de objeto](xref:object-properties-common#object-type)

### Permisos de tabla

`MetadataPermission` · por tabla · Seguridad · solo lectura · nivel de compatibilidad 1400+ · _atajo a_ los permisos de tabla del rol

El permiso de seguridad a nivel de objetos (OLS) de cada tabla de este rol. Expande la propiedad para ver una entrada por tabla y elige un valor para cada una:

| Valor     | Significado                                                                                                                                                                                                    |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Default` | No se ha establecido ningún permiso. Los miembros del rol pueden ver la tabla si `ModelPermission` permite la lectura.                                                         |
| `Read`    | Los miembros del rol pueden ver y consultar la tabla.                                                                                                                                          |
| `None`    | La tabla queda oculta para los miembros del rol, junto con sus columnas, medidas y relaciones. Las consultas y las medidas que hacen referencia a ella les devuelven un error. |

Las tablas de grupos de cálculo no se muestran en la lista. Tabular Editor muestra esta propiedad en el nivel de compatibilidad 1400 o superior. El valor, al contraerse, resume la configuración; por ejemplo, "OLS habilitado en 2 de 15 tablas".

Para proteger columnas individuales, usa [Permisos de columna de OLS](#ols-column-permissions) en el permiso de tabla o `ObjectLevelSecurity` en la columna.

> [!NOTE]
> El rol también tiene una colección de objetos de permisos de tabla que comparten el mismo nombre para mostrar. Consulta [Permisos de tabla](#table-permissions-1) más abajo.

### Seguridad a nivel de filas

`RowLevelSecurity` · por tabla · Seguridad · solo lectura · _acceso directo a_ los permisos de tabla del rol

El filtro de seguridad a nivel de filas (RLS) de cada tabla de este rol. Expande la propiedad para ver una entrada por tabla. Cada entrada es una expresión DAX que devuelve `TRUE` para las filas que pueden ver los miembros del rol, y una entrada vacía deja esa tabla sin filtrar. Las tablas de grupos de cálculo no aparecen en la lista. El valor contraído resume la configuración; por ejemplo: "RLS habilitada en 1 de 15 tablas".

Un filtro estático codifica de forma fija los valores permitidos:

```dax
'Region'[Country] = "Denmark"
```

Un filtro dinámico busca al usuario actual, así que un solo rol sirve para todos los usuarios:

```dax
'Salesperson'[Email] = USERPRINCIPALNAME ()
```

Los filtros se propagan a través de las relaciones desde el lado "uno" al lado "varios", por lo que filtrar una dimensión como `Region` también filtra las tablas de hechos relacionadas con ella. Para que un filtro se propague en ambas direcciones de una relación, establece `SecurityFilteringBehavior` en la relación (consulta @object-properties-relationships). La expresión se evalúa para cada fila de la tabla en la que está, así que filtra la tabla más pequeña que puedas, normalmente una dimensión.

Al establecer un filtro, se crea un permiso de tabla para esa tabla si aún no existe. Al borrarlo, se elimina de nuevo el permiso de tabla, a menos que el permiso de tabla también contenga configuración de OLS. El propio filtro se almacena en la propiedad `FilterExpression` del permiso de tabla.

En Tabular Editor 3, comprueba un filtro suplantando a un usuario o a un rol en una @table-preview o una @pivot-grid.

### Miembros

`Members` · colección de miembros del rol · Traducciones, Perspectivas, Seguridad · solo lectura

Los usuarios y grupos que pertenecen al rol. Haz clic en el botón de puntos suspensivos para agregar, quitar y editar miembros en el editor de colecciones, o haz clic con el botón derecho en el rol y elige **Editar miembros...** (consulta @data-security-setup-rls). La colección contiene dos tipos de miembros:

- **Miembros de Windows AD** para SQL Server Analysis Services con Active Directory local (consulta [Miembro del rol de Windows](#windows-role-member))
- **Miembros de Azure AD** (miembros externos) para Azure Analysis Services y Power BI, identificados mediante Microsoft Entra ID (consulta [Miembro externo del rol](#external-role-member))

En Power BI y Fabric, la pertenencia a roles suele administrarse en la configuración de seguridad del modelo semántico en el servicio. En Analysis Services, muchos equipos administran los miembros directamente en el servidor. Tabular Editor solo implementa los miembros de los roles si seleccionas **Implementar miembros de roles del modelo**. Si desactivas la opción, los roles de la base de datos de destino conservan sus miembros y una base de datos nueva recibe roles sin miembros (consulta @deployment).

En Power BI, no puedes agregar entidades de servicio como miembros de roles.

Los miembros que alguien agrega en la página **Seguridad** del modelo semántico en el servicio de Power BI son miembros normales de los roles del modelo. A través del punto de conexión XMLA, son idénticos a los miembros agregados en Tabular Editor: miembros externos con `IdentityProvider` `AzureAD` y el ID de objeto del usuario como `MemberID`. Cuando implementas con **Implementar miembros de roles del modelo**, los miembros de tu modelo los reemplazan. Para conservar los miembros agregados en el servicio, implementa sin esa opción.

### Permiso del modelo

`ModelPermission` · Permiso del modelo · Traducciones, perspectivas, seguridad

El nivel de acceso que el rol concede a sus miembros a todo el modelo.

| Valor           | Significado                                                                                                                                                                                                      |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `None`          | Sin acceso. Los miembros no pueden conectarse al modelo, independientemente de lo que permitan las demás configuraciones del rol.                                                |
| `Read`          | Los miembros pueden leer los metadatos del modelo y consultar sus datos, sujeto a la RLS y la OLS del rol. Este es el valor de casi todos los roles para los usuarios de Report. |
| `ReadRefresh`   | Como `Read`, pero los miembros también pueden actualizar el modelo.                                                                                                                              |
| `Refresh`       | Los miembros pueden actualizar el modelo y no pueden consultarlo; por ejemplo, cuentas que solo ejecutan actualizaciones.                                                                        |
| `Administrator` | Los miembros tienen control total sobre el modelo, incluida la posibilidad de cambiarlo, y la RLS y la OLS no se les aplican. Solo en Analysis Services.                         |

Un rol nuevo no tiene acceso hasta que establezcas esta propiedad. Si agregas un filtro a nivel de fila a un rol cuyo `ModelPermission` es `None` y que todavía no tiene permisos de tabla, Tabular Editor lo establece en `Read`.

Power BI y Fabric solo admiten `Read` para los roles del modelo: Microsoft lo documenta como el único permiso de rol que puedes establecer mediante el punto de conexión XMLA. Los permisos de actualización, compilación y otros se gestionan con los roles del Workspace y los permisos del modelo semántico en el servicio, y los roles del modelo en Power BI solo se usan para RLS y OLS. En el servicio de Power BI, al implementar un rol con cualquier otro valor, se produce el error "Please set the permission level for your seguridad a nivel de filas (RLS) roles to 'Read'".

### Permisos de tabla

`TablePermissions` · colección de permisos de tabla · Traducciones, Perspectivas, Seguridad · de solo lectura

Los objetos de permiso de tabla del rol: uno por cada tabla que tenga un filtro RLS o una configuración OLS en este rol (consulta [permiso de tabla](#table-permission)).

La vista **Propiedades** no muestra esta colección. Edita estos mismos ajustes en [Seguridad a nivel de filas](#row-level-security) y [Permisos de tabla](#table-permissions) (OLS) más arriba, y Tabular Editor agrega y quita los permisos de tabla. En un C# Script, usa la colección para recorrer las tablas protegidas de un rol:

```csharp
foreach (var tp in Selected.Role.TablePermissions)
    Output(tp.Table.Name + ": " + tp.FilterExpression);
```

En Tabular Editor 3, el **Explorador TOM** muestra los permisos de tabla de un rol bajo el rol. Un permiso de tabla cuya configuración se ha restablecido por completo a los valores predeterminados no tiene efecto y se muestra atenuado.

## Permiso de tabla

Un permiso de tabla contiene la configuración de seguridad de un rol para una tabla: el filtro RLS y los permisos OLS de la tabla y sus columnas. El permiso de tabla toma el nombre de su tabla y no puedes cambiarle el nombre.

Tabular Editor crea un permiso de tabla cuando estableces un filtro RLS o un permiso OLS para una tabla en un rol. Cuando borras el filtro RLS y el permiso de tabla no contiene ninguna configuración OLS, Tabular Editor lo elimina. Restablecer un permiso OLS a `Default` mantiene el permiso de tabla, sin efecto, hasta que lo elimines. En Tabular Editor 3, también puedes agregar uno manualmente: haz clic con el botón derecho en el rol y elige **Agregar permiso de tabla...**. En @data-security-setup-rls se explica esto y cómo probar una expresión de filtro en una consulta DAX antes de usarla.

### Propiedades comunes

- [Anotaciones](xref:object-properties-common#annotations)
- [Propiedades extendidas](xref:object-properties-common#extended-properties)
- [Mensaje de error](xref:object-properties-common#error-message)
- [Estado](xref:object-properties-common#state)

La vista **Propiedades** no muestra `Name` ni `ObjectType` en los permisos de tabla. `RoleName` y `TableName` en la categoría **Metadatos** identifican el permiso de tabla.

### Rol

`RoleName` · string · Metadatos · de solo lectura · _acceso directo al_ nombre del rol

El nombre del rol al que pertenece este permiso de tabla.

### Tabla

`TableName` · string · Metadatos · de solo lectura · _acceso directo al_ nombre de la tabla

El nombre de la tabla que protege este permiso de tabla.

### Rol

`Role` · ModelRole · Opciones · de solo lectura

El rol al que pertenece este permiso de tabla, para C# Scripts que permiten pasar de un permiso de tabla de vuelta a su rol. La vista **Propiedades** no lo muestra; en su lugar, muestra `RoleName` en la categoría **Metadatos**.

### Permisos OLS a nivel de columna

`ColumnPermissions` · por columna · Seguridad · solo lectura · nivel de compatibilidad 1400+

El permiso de seguridad a nivel de objetos (OLS) de cada columna de la tabla en este rol. Amplía la propiedad para ver una entrada por columna. Los valores son los mismos que para una tabla:

| Valor     | Significado                                                                                                                                                       |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Default` | No se ha establecido ningún permiso. La columna sigue el permiso de la tabla.                                                     |
| `Read`    | Los miembros del rol pueden ver y consultar la columna.                                                                                           |
| `None`    | La columna está oculta para los miembros del rol. Las consultas y las medidas que hacen referencia a ella les devuelven un error. |

Usa OLS a nivel de columna para ocultar columnas confidenciales, como salarios o datos personales, mientras el resto de la tabla sigue estando disponible. Las medidas que hacen referencia a una columna protegida fallan para los miembros del rol. Para ver qué objetos hacen referencia a una columna, haz clic derecho sobre ella en el **Explorador TOM** y elige **Mostrar dependencias...** (consulta @formula-fix-up-dependencies).

Es la misma configuración que `ObjectLevelSecurity` en la columna (consulta @object-properties-columns).

### Expresión de filtro

`FilterExpression` · string · traducciones, perspectivas y seguridad

El filtro de seguridad a nivel de filas de la tabla en este rol: una expresión DAX que devuelve `TRUE` para las filas que los miembros del rol pueden ver. Un filtro vacío deja la tabla sin filtrar para este rol. Edítalo en el **Editor de expresiones** o mediante `RowLevelSecurity` en el rol o en la tabla. Para ver ejemplos, consulta [Seguridad a nivel de filas](#row-level-security).

La expresión se evalúa en el contexto de cada fila de la tabla, por lo que puedes hacer referencia a sus columnas directamente, por ejemplo `'Region'[Country] = "Denmark"`. Para usar valores de otras tablas, usa `RELATED` o `LOOKUPVALUE`. Para obtener el usuario actual, usa `USERPRINCIPALNAME ()` o `USERNAME ()`.

### Permiso de tabla OLS

`MetadataPermission` · MetadataPermission · traducciones, perspectivas y seguridad · nivel de compatibilidad 1400+

El permiso de seguridad a nivel de objetos (OLS) de la tabla en este rol.

| Valor            | Significado                                                                                                    |
| ---------------- | -------------------------------------------------------------------------------------------------------------- |
| `Predeterminado` | No se ha establecido ningún permiso. Los miembros del rol pueden ver la tabla. |
| `Lectura`        | Los miembros del rol pueden ver y consultar la tabla.                                          |
| `Ninguno`        | La tabla se oculta para los miembros del rol, junto con sus columnas, medidas y relaciones.    |

Es la misma configuración que [Permisos de tabla](#table-permissions) en el rol y `ObjectLevelSecurity` en la tabla.

No puedes combinar RLS y OLS de distintos roles. Un usuario que sea miembro de una combinación de roles de este tipo recibe un error en tiempo de consulta, tanto en SQL Server Analysis Services como en Azure Analysis Services y en Power BI. Consulta @data-security-about, [Combinar OLS con RLS](xref:data-security-setup-ols#5-combine-ols-with-rls) y las [restricciones de Microsoft sobre la seguridad a nivel de objetos](https://learn.microsoft.com/analysis-services/tabular-models/object-level-security#restrictions).

Tampoco puedes ocultar una tabla con OLS si con ello se rompe una cadena de relaciones con otras tablas. El motor lo rechaza con un error.

## Miembro del rol de Windows

Un miembro de un rol de Windows es un usuario o grupo de Active Directory; por ejemplo, `CONTOSO\SalesManagers`. SQL Server Analysis Services usa miembros de Windows, y Azure Analysis Services y Power BI usan [miembros externos del rol](#external-role-member). El servicio de Power BI rechaza un miembro de Windows durante la implementación con el error "Solo se admiten usuarios o grupos de Microsoft Entra. Usa 'AzureAD' como valor del proveedor de identidad".

Agrega grupos siempre que puedas: agregar y quitar personas de un grupo no requiere cambiar ni volver a implementar el modelo.

### Propiedades comunes

- [Anotaciones](xref:object-properties-common#annotations)
- [Propiedades extendidas](xref:object-properties-common#extended-properties)
- [Tipo de objeto](xref:object-properties-common#object-type)

La vista **Propiedades** no muestra `Name` para los miembros del rol. `MemberName` identifica al miembro.

### ID de miembro

`MemberID` · cadena · Opciones

El identificador de seguridad (SID) del usuario o grupo, por ejemplo `S-1-5-21-...`. Puedes dejarlo en blanco y completar solo `MemberName`. En Tabular Editor 3, cuando seleccionas el miembro con el selector de objetos de Windows (el botón de puntos suspensivos de `MemberName`), Tabular Editor rellena tanto el nombre como el SID.

Cuando implementas en SQL Server Analysis Services, Tabular Editor implementa `MemberID` tal cual. Solo quita los identificadores de miembro cuando el destino es Azure Analysis Services o Power BI (consulta `MemberID` en [miembro externo del rol](#external-role-member)).

Cuando implementas un miembro de Windows con solo `MemberName` establecido, SQL Server Analysis Services busca la cuenta y almacena su SID en `MemberID`. Rechaza una cuenta que no existe con un error como "El rol 'Sales' incluye una cuenta de dominio que no existe". Esto se observó en SQL Server 2025 Analysis Services.

### Nombre del miembro

`MemberName` · string · Opciones

El nombre del usuario o grupo de Windows en el formato `DOMAIN\\name`, por ejemplo `CONTOSO\\SalesManagers`. Si la cuenta no existe en un dominio en el que confía el servidor, la implementación falla.

### Rol

`Rol` · ModelRole · Opciones · de solo lectura

El rol al que pertenece este miembro, para C# Scripts que van desde un miembro hasta su rol. La vista **Propiedades** no lo muestra.

## Miembro externo del rol

Un miembro externo del rol es un usuario o grupo identificado por un proveedor de identidades externo, que en la práctica es Microsoft Entra ID (antes llamado Azure Active Directory). Azure Analysis Services y Power BI usan miembros externos. En Tabular Editor, agréguelos como **Azure AD Member** en la colección `Members` del rol (consulte @data-security-setup-rls).

### Propiedades comunes

- [Anotaciones](xref:object-properties-common#annotations)
- [Propiedades extendidas](xref:object-properties-common#extended-properties)
- [Tipo de objeto](xref:object-properties-common#object-type)

La vista **Propiedades** no muestra `Name` en los miembros del rol. `MemberName` identifica al miembro.

### Proveedor de identidades

`IdentityProvider` · string · Opciones

El proveedor de identidades que autentica al miembro. Tabular Editor lo establece en `AzureAD` al agregar un miembro externo. Es el único valor que usan Azure Analysis Services y Power BI.

### ID del miembro

`MemberID` · string · Opciones

El identificador de objeto del usuario o grupo en Microsoft Entra ID. SQL Server Analysis Services lo requiere: SQL Server 2025 Analysis Services rechaza a un miembro externo sin un ID de miembro con el error "MemberID must be specified when creating an External RoleMembership object". Para Azure Analysis Services y Power BI, déjalo vacío. En los ejemplos de Microsoft, los miembros externos se agregan solo con `MemberName` e `IdentityProvider`.

No establezcas los identificadores de miembro al implementar en Azure Analysis Services o Power BI. Cuando el destino de implementación es Azure Analysis Services o el servicio de Power BI, Tabular Editor quita los identificadores de miembro de todos los miembros del rol, incluidos los miembros que conserva de la base de datos de destino. Las implementaciones en SQL Server Analysis Services sí los conservan. No puedes activar ni desactivar este comportamiento.

### Nombre del miembro

`MemberName` · string · Opciones

El nombre que identifica al usuario o grupo. En el caso de un usuario, es el nombre de usuario principal, normalmente la dirección de correo electrónico; por ejemplo, `anna@contoso.com`. Los formatos admitidos para grupos y otros miembros dependen del destino.

En Azure Analysis Services:

- agrega un grupo de seguridad como `obj:<group object ID>@<tenant ID>` o por su dirección de correo electrónico, y un grupo de Microsoft 365 por su dirección de correo electrónico
- agrega una entidad de servicio como `app:<application ID>@<tenant ID>`
- durante la implementación, todos los nombres se comprueban en Microsoft Entra ID, y el nombre para mostrar de un usuario o grupo, o un usuario que no existe, provoca el error "was not found in your organization's Microsoft Entra ID"
- el nombre se almacena tal como lo escribiste, de modo que un nombre `obj:` sigue siendo un nombre `obj:` y `MemberID` permanece vacío

En el servicio de Power BI:

- funciona el nombre de usuario principal de un usuario, y también `obj:<object ID>@<tenant ID>`, que el servicio reescribe como el nombre de usuario principal
- agrega un grupo de seguridad como `obj:<group object ID>@<tenant ID>`, que el servicio conserva tal como lo escribiste, o un grupo de seguridad habilitado para correo por su dirección de correo electrónico
- el nombre para mostrar de un usuario o grupo, la dirección de correo electrónico de un usuario que no existe o un grupo de Microsoft 365 producen en los roles el error "There are invalid rolememberships in roles"
- el servicio rellena `MemberID` con el ID de objeto del usuario

En la configuración de seguridad del servicio de Power BI, puedes agregar usuarios y grupos por dirección de correo electrónico o por nombre. Esa configuración admite grupos de distribución, grupos habilitados para correo y grupos de seguridad de Microsoft Entra, y no admite grupos de Microsoft 365.

### Tipo de miembro

`MemberType` · RoleMemberType · Opciones

Si el miembro es un usuario individual o un grupo.

| Valor   | Significado                                                                              |
| ------- | ---------------------------------------------------------------------------------------- |
| `Auto`  | El servidor determina si el miembro es un usuario o un grupo.            |
| `User`  | El miembro es un usuario individual.                                     |
| `Group` | El miembro es un grupo de seguridad y todos sus miembros reciben el rol. |

Los miembros del rol de Windows no tienen esta propiedad: el servidor determina, a partir de la cuenta, si se trata de un usuario o de un grupo.

Azure Analysis Services y el servicio de Power BI ignoran el valor que configures:

- Azure Analysis Services almacena cada miembro externo como `Auto`, independientemente de que establezcas `Auto`, `User` o `Group`, tanto para usuarios como para grupos.
- el servicio de Power BI determina el tipo por sí mismo y almacena un usuario como `User` y un grupo como `Group`, tanto si estableces `Auto`, `User` o `Group`. También rellena `MemberID` en ambos casos. En Power BI, deja esta propiedad en `Auto`.

### Rol

`rol` · ModelRole · Options · de solo lectura

El rol al que pertenece este miembro, para C# Script que permiten pasar de un miembro a su rol. La vista **Properties** no lo muestra.
