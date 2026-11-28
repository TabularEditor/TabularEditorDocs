---
uid: kb.bpa-role-mixed-rls-ols-members
title: Evitar que los miembros tengan un rol RLS y un rol OLS a la vez
author: Morten Lønskov
updated: 2026-11-12
description: Regla de buenas prácticas que señala los roles que comparten un miembro con otro rol cuando uno de los roles aplica seguridad a nivel de filas y el otro seguridad a nivel de objetos a las mismas tablas o a tablas directamente relacionadas.
---

# Evitar miembros tanto en un rol RLS como en un rol OLS

## Información general

Esta regla marca los roles que comparten un miembro con otro rol cuando uno de los dos roles filtra las filas de una tabla con seguridad a nivel de fila (RLS) y el otro oculta columnas o tablas con seguridad a nivel de objeto (OLS) en la misma tabla o en una tabla directamente relacionada. Las consultas de ese miembro fallan con un error que indica que la combinación de roles activos no es compatible.

- Categoría: Seguridad
- Gravedad: Alta (3)

## Se aplica a

- Roles

## Por qué es importante

- Las consultas de un usuario afectado fallan, por lo que los informes basados en el modelo no funcionan para ese usuario.
- El error solo aparece cuando un usuario que pertenece a ambos roles consulta el modelo, por lo que probar cada rol por separado no lo revela.

## Cuándo se activa esta regla

La regla compara cada rol con permiso `Read` o `ReadRefresh` con todos los demás roles con permiso `Read` o `ReadRefresh`. Se activa cuando los dos roles tienen un miembro con el mismo nombre y se da una de estas combinaciones:

| Un rol | Otro rol |
|---|---|
| un filtro de filas en una tabla | OLS `None` en algunas columnas de la misma tabla, mientras que la tabla y al menos una columna permanecen visibles |
| un filtro de filas en una tabla | OLS `None` en una tabla, o en columnas de una tabla, unidas a la tabla filtrada por una relación activa, en cualquier dirección |

La regla marca ambos roles. Un rol que tiene tanto RLS como OLS cuenta como cualquiera de los lados, por lo que un rol con un filtro de filas y OLS de columnas junto a un rol con un filtro de filas en la tabla relacionada también activa la regla. Los nombres de los miembros se comparan sin tener en cuenta las mayúsculas y minúsculas, por lo que `CONTOSO\alice` y `contoso\Alice` coinciden.

```csharp
(ModelPermission == "Read" or ModelPermission == "ReadRefresh")

and

Model.Roles.Any(
    Name != current.Name
    and (ModelPermission == "Read" or ModelPermission == "ReadRefresh")
    and Members.Any(current.Members.Any(string.Equals(MemberName, outerIt.MemberName, StringComparison.OrdinalIgnoreCase)))
    and (
        current.TablePermissions.Any(not string.IsNullOrWhiteSpace(FilterExpression) and outerIt.TablePermissions.Any(Table.Name == outerIt.Table.Name and MetadataPermission != "None" and ColumnPermissions.Any(it == "None") and ColumnPermissions.Any(it != "None")))
        or current.TablePermissions.Any(MetadataPermission != "None" and ColumnPermissions.Any(it == "None") and ColumnPermissions.Any(it != "None") and outerIt.TablePermissions.Any(Table.Name == outerIt.Table.Name and not string.IsNullOrWhiteSpace(FilterExpression)))
        or Model.Relationships.Any(IsActive and (
            (not string.IsNullOrWhiteSpace(current.RowLevelSecurity[FromTable.Name]) and outerIt.TablePermissions.Any(Table.Name == outerIt.ToTable.Name and (MetadataPermission == "None" or ColumnPermissions.Any(it == "None"))))
            or (not string.IsNullOrWhiteSpace(current.RowLevelSecurity[ToTable.Name]) and outerIt.TablePermissions.Any(Table.Name == outerIt.FromTable.Name and (MetadataPermission == "None" or ColumnPermissions.Any(it == "None"))))
            or (current.TablePermissions.Any(Table.Name == outerIt.FromTable.Name and (MetadataPermission == "None" or ColumnPermissions.Any(it == "None"))) and not string.IsNullOrWhiteSpace(outerIt.RowLevelSecurity[ToTable.Name]))
            or (current.TablePermissions.Any(Table.Name == outerIt.ToTable.Name and (MetadataPermission == "None" or ColumnPermissions.Any(it == "None"))) and not string.IsNullOrWhiteSpace(outerIt.RowLevelSecurity[FromTable.Name]))
        ))
    )
)
```

### Combinaciones que la regla no marca

Estas combinaciones funcionan y la regla no las marca:

- RLS y OLS en tablas sin relación entre ellas, o unidas únicamente por una relación inactiva
- OLS a nivel de tabla, con o sin OLS de columna, en una tabla RLS que no tiene relaciones
- OLS de columna que oculta todas las columnas de la tabla RLS
- un ajuste de OLS de `Read`, que no restringe nada

Estas combinaciones también fallan en el momento de la consulta, y la regla no las detecta:

- RLS y OLS en tablas con dos o más relaciones activas separadas
- OLS a nivel de tabla en una tabla RLS que tiene relaciones activas
- Usuarios que pertenecen a ambos roles a través de un grupo, por ejemplo, cuando un rol incluye un grupo de seguridad y el otro incluye un usuario de ese grupo, o cuando los dos roles incluyen grupos diferentes con un miembro en común.
- Miembros que no están en el modelo cargado, como los miembros de roles gestionados en el servicio Power BI.

> [!NOTE]
> La [documentación sobre seguridad a nivel de objeto](https://learn.microsoft.com/analysis-services/tabular-models/object-level-security#restrictions) de Microsoft indica que no se admite ninguna combinación de RLS y OLS de distintos roles. La regla sigue el comportamiento de SQL Server 2025 Analysis Services y del servicio Power BI, donde las combinaciones enumeradas anteriormente como funcionales no fallan.

## Cómo solucionarlo

La regla no tiene corrección automática.

### Corrección manual

Realice una de las siguientes acciones para cada miembro que figure en ambos roles:

- Define el filtro de filas y la OLS en un solo rol y haz que el miembro pertenezca únicamente a ese rol. La RLS y la OLS en el mismo rol funcionan conjuntamente.
- Elimine al miembro de uno de los dos roles.

Configure los filtros de fila y la OLS del rol combinado en la vista **Propiedades**. Consulte [Combinar OLS con RLS](xref:data-security-setup-ols#5-combine-ols-with-rls) y @object-properties-security.

## Causas comunes

### Causa 1: Roles separados para filas y columnas

El modelo tiene un conjunto de roles que filtra los datos por región y otro que oculta las columnas confidenciales, y algunos usuarios necesitan ambos.

### Causa 2: Miembros añadidos a lo largo del tiempo

Se añadió un usuario a un rol de RLS y, posteriormente, a un rol de OLS para otro informe.

## Ejemplo

### Antes de la corrección

```text
Relationship: 'Invoices'[CustomerKey] -> 'Customers'[CustomerKey] (active)

Role: Europe           Model Permission: Read
                       Row Level Security on 'Customers': [Continent] = "Europe"
                       Members: CONTOSO\alice
Role: No Sales Value   Model Permission: Read
                       Object Level Security on 'Invoices'[Value]: None
                       Members: contoso\Alice
```

Las consultas de `CONTOSO\alice` fallan con un error.

### Después de la corrección

```text
Role: Europe No Sales Value   Model Permission: Read
                              Row Level Security on 'Customers': [Continent] = "Europe"
                              Object Level Security on 'Invoices'[Value]: None
                              Members: CONTOSO\alice
```

`CONTOSO\alice` se quita de `Europe` y `No Sales Value`.

## Reglas relacionadas

- [La seguridad a nivel de fila y a nivel de objeto requiere permiso de lectura](xref:kb.bpa-role-security-not-enforced)
- [Los roles de Power BI deben tener permiso de lectura](xref:kb.bpa-powerbi-role-read-permission)
- [Los roles sin seguridad anulan los roles protegidos](xref:kb.bpa-role-unrestricted-read)

## Nivel de compatibilidad

Esta regla se aplica a los modelos con un nivel de compatibilidad de **1400** o superior.
