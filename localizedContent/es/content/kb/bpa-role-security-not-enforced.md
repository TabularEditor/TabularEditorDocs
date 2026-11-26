---
uid: kb.bpa-role-security-not-enforced
title: La seguridad a nivel de filas y a nivel de objetos requiere permiso de lectura
author: Morten Lønskov
updated: 2026-11-12
description: Regla de buenas prácticas que señala los roles cuya seguridad a nivel de fila u objeto no tiene ningún efecto o bloquea la implementación debido al permiso de modelo del rol.
---

# La seguridad a nivel de fila y a nivel de objeto requiere permiso de lectura

## Información general

Esta regla marca los roles que tienen configuraciones de seguridad que su permiso de modelo ignora o no permite. Los filtros de seguridad de nivel de fila (RLS) y la seguridad de nivel de objeto (OLS) solo surten efecto en los roles cuyo `ModelPermission` sea `Read` o `ReadRefresh`.

- Categoría: Seguridad
- Gravedad: Alta (3)

## Se aplica a

- Roles (modelos cuyo modo de compatibilidad no es Power BI)

## Por qué es importante

- No se puede implementar un rol `Administrator` o `Refresh` con permisos de tabla. SQL Server 2025 Analysis Services lo rechaza incluso cuando los permisos de tabla no contienen ningún filtro de filas ni OLS, con un error como «... es un rol de administrador y, por lo tanto, no permite objetos TablePermission bajo él».
- Los miembros de un rol con permiso `None` no pueden conectarse al modelo, por lo que la RLS y la OLS del rol nunca restringen a nadie.
- La seguridad que describen los ajustes del rol no es la seguridad que obtienen sus miembros.

## Cuándo se activa esta regla

La regla se activa para un rol en un modelo que no está en modo de compatibilidad con Power BI cuando se da alguna de estas situaciones:

- `ModelPermission` es `Administrator` o `Refresh` y el rol tiene algún permiso de tabla
- `ModelPermission` es `None` y un permiso de tabla tiene un filtro de filas, una tabla con OLS configurada como `None` o, en el nivel de compatibilidad 1400 y superior, una columna con OLS configurada como `None`

```csharp
Model.Database.CompatibilityMode != "PowerBI"

and

(
    ((ModelPermission == "Administrator" or ModelPermission == "Refresh") and TablePermissions.Any())
    or
    (ModelPermission == "None" and TablePermissions.Any(not string.IsNullOrWhiteSpace(FilterExpression) or MetadataPermission == "None" or (Model.Database.CompatibilityLevel >= 1400 and ColumnPermissions.Any(it == "None"))))
)
```

Un ajuste de OLS de `Read` no cuenta como seguridad para un rol `None`. Para conocer los roles en los modelos de Power BI, consulte @kb.bpa-powerbi-role-read-permission.

## Cómo solucionarlo

La regla no tiene corrección automática. Al cambiar el permiso de un rol, se modifica quién puede consultar qué datos, así que decídalo por rol.

### Corrección manual

Si los miembros del rol son usuarios de informes cuyo acceso a los datos desea restringir:

1. En el **Explorador TOM**, seleccione el rol.
2. En la vista **Propiedades**, establezca **Permiso del modelo** en `Read`, o en `ReadRefresh` si los miembros también actualizan el modelo.

Si los miembros del rol necesitan acceso de administrador o de actualización:

1. En el **Explorador TOM**, expanda el rol.
2. Elimine los permisos de tabla del rol.

Consulte @object-properties-security para conocer los valores de **Permiso del modelo**.

## Causas comunes

### Causa 1: El permiso se modificó después de definir la seguridad

El rol tenía el permiso `Read` cuando se añadieron sus filtros de filas, y alguien lo cambió más tarde a `Administrator` o `Refresh`.

### Causa 2: Rol copiado de un rol de administrador

Un rol duplicado a partir de un rol de administrador o de procesamiento conservó el permiso del rol de origen cuando se le agregaron filtros.

### Causa 3: Rol nuevo sin permiso

Un nuevo rol tiene el permiso `None` hasta que lo establezca. El rol obtuvo su configuración de seguridad antes de que nadie estableciera su permiso.

## Ejemplo

### Antes de la corrección

```text
Role:               Regional Managers
Model Permission:   Administrator
Row Level Security: 'Region'[Country] = "Denmark"
```

La implementación en SQL Server 2025 Analysis Services falla. La RLS no se aplica a los administradores, por lo que el filtro no tiene ningún efecto sobre los miembros del rol.

### Después de la corrección

```text
Role:               Regional Managers
Model Permission:   Read
Row Level Security: 'Region'[Country] = "Denmark"
```

## Reglas relacionadas

- [Los roles de Power BI deben tener permiso de lectura](xref:kb.bpa-powerbi-role-read-permission)
- [Los roles sin seguridad anulan los roles protegidos](xref:kb.bpa-role-unrestricted-read)
- [Evitar miembros tanto en un rol RLS como en un rol OLS](xref:kb.bpa-role-mixed-rls-ols-members)

## Nivel de compatibilidad

Esta regla se aplica a los modelos con un nivel de compatibilidad de **1200** o superior. La OLS de columna se comprueba en el nivel de compatibilidad 1400 y superior.
