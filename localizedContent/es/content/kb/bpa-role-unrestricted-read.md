---
uid: kb.bpa-role-unrestricted-read
title: Roles sin seguridad que anulan los roles protegidos
author: Morten Lønskov
updated: 2026-11-12
description: Regla de buenas prácticas que señala los roles que conceden acceso de lectura sin restricciones en un modelo en el que otros roles restringen los datos con seguridad a nivel de fila o de objeto.
---

# Roles sin anulación de seguridad que anulan roles protegidos

## Información general

Esta regla marca los roles que conceden acceso `Read` a todos los datos, mientras que otros roles del modelo restringen el acceso con seguridad a nivel de filas (RLS) o seguridad a nivel de objetos (OLS). Se combinan los permisos de varios roles: un usuario que sea miembro de este rol y de un rol protegido puede consultar todos los datos.

- Categoría: Seguridad
- Gravedad: Media (2)

## Se aplica a

- Roles

## Por qué es importante

- Al añadir un usuario a un rol sin restricciones, se eliminan la RLS y la OLS de todos los demás roles a los que pertenece el usuario.
- Un usuario que pertenece al rol equivocado ve datos que la seguridad del modelo está destinada a ocultar, y ninguna consulta devuelve un error.

## Cuándo se activa esta regla

La regla se activa para un rol cuando todas estas condiciones son ciertas:

- `ModelPermission` es `Read` o `ReadRefresh`
- Ninguno de los permisos de tabla del rol tiene un filtro de filas, una tabla con OLS configurado como `None` o, en el nivel de compatibilidad 1400 y superior, una columna con OLS configurado como `None`.
- Otro rol con permiso `Read` o `ReadRefresh` tiene al menos uno de esos ajustes.

```csharp
(ModelPermission == "Read" or ModelPermission == "ReadRefresh")

and

not TablePermissions.Any(not string.IsNullOrWhiteSpace(FilterExpression) or MetadataPermission == "None" or (Model.Database.CompatibilityLevel >= 1400 and ColumnPermissions.Any(it == "None")))

and

Model.Roles.Any(
    (ModelPermission == "Read" or ModelPermission == "ReadRefresh")
    and TablePermissions.Any(not string.IsNullOrWhiteSpace(FilterExpression) or MetadataPermission == "None" or (Model.Database.CompatibilityLevel >= 1400 and ColumnPermissions.Any(it == "None")))
)
```

Un filtro de fila en blanco y un ajuste de OLS de `Read` no restringen nada, y la regla considera que un rol que solo tiene esos elementos no está restringido. En un modelo en el que no se protege ningún rol `Read` o `ReadRefresh`, la regla no se activa.

## Cómo solucionarlo

La regla no tiene ninguna corrección automática. Un rol que concede acceso a todos los datos suele ser intencionado; por ejemplo, para los gerentes o un equipo de soporte.

### Corrección manual

1. En el **Explorador TOM**, seleccione el rol marcado y revise sus **Miembros**.
2. Realice una de las siguientes acciones:
   - Si todos los miembros pueden ver todos los datos, mantén el rol y haz clic con el botón derecho en el resultado en **Best Practice Analyzer** y elige **Ignorar elemento**.
   - Si los miembros del rol necesitan un acceso restringido, añade filtros de fila u OLS al rol.
   - Si un miembro también pertenece a un rol protegido por error, quítelo de este rol.

Consulta @object-properties-security y @using-bpa.

## Causas comunes

### Causa 1: Rol para usuarios que ven todos los datos

El modelo tiene un rol para los gerentes o administradores del informe que necesitan todos los datos.

### Causa 2: Rol creado para realizar pruebas

Se añadió un rol sin filtros para probar el modelo y se mantuvo.

### Causa 3: Filtros eliminados de un rol

Se han borrado los filtros de filas del rol, pero el rol aún tiene miembros.

## Ejemplo

### Antes de la corrección

```text
Role: All Data      Model Permission: Read   Row Level Security: (none)
                    Members: CONTOSO\alice, CONTOSO\bob
Role: Europe        Model Permission: Read   Row Level Security: 'Region'[Continent] = "Europe"
                    Members: CONTOSO\alice
```

`CONTOSO\alice` ve todas las regiones, porque `All Data` concede lo que `Europe` restringe.

### Después de la corrección

```text
Role: All Data      Model Permission: Read   Row Level Security: (none)
                    Members: CONTOSO\bob
Role: Europe        Model Permission: Read   Row Level Security: 'Region'[Continent] = "Europe"
                    Members: CONTOSO\alice
```

La regla sigue marcando `All Data`. Ignore el resultado si `CONTOSO\bob` tiene permiso para ver todos los datos.

## Reglas relacionadas

- [La seguridad a nivel de fila y a nivel de objeto requiere permiso de lectura](xref:kb.bpa-role-security-not-enforced)
- [Los roles de Power BI deben tener permiso de lectura](xref:kb.bpa-powerbi-role-read-permission)
- [Evitar miembros tanto en un rol RLS como en un rol OLS](xref:kb.bpa-role-mixed-rls-ols-members)

## Nivel de compatibilidad

Esta regla se aplica a los modelos con un nivel de compatibilidad de **1200** o superior. La OLS de columna se comprueba en el nivel de compatibilidad 1400 y superior.
