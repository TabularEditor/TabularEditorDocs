---
uid: kb.bpa-powerbi-role-read-permission
title: Los roles de Power BI deben tener permiso de lectura
author: Morten Lønskov
updated: 2026-11-12
description: Regla de prácticas recomendadas que marca los roles en los modelos semánticos de Power BI cuyo permiso de modelo es diferente de Lectura.
---

# Los roles de Power BI deben tener permiso de lectura

## Información general

Esta regla marca los roles en los modelos semánticos de Power BI cuyo `ModelPermission` no es `Read`. Power BI solo admite el permiso `Read` en los roles de modelo. El acceso, como la actualización o la edición del modelo, procede de los roles del área de trabajo y de los permisos del modelo semántico en el servicio Power BI.

- Categoría: Seguridad
- Gravedad: Alta (3)

## Se aplica a

- Roles (solo modelos semánticos de Power BI)

## Por qué es importante

- El servicio Power BI rechaza la implementación de un rol con permiso `None`, `ReadRefresh`, `Refresh` o `Administrator`, con o sin permisos de tabla, con el error «Establezca el nivel de permiso de sus roles de seguridad a nivel de fila (RLS) en «Leer»».
- Los roles de modelo en Power BI aplican seguridad a nivel de filas (RLS) y seguridad a nivel de objetos (OLS) a sus miembros y no conceden ningún otro tipo de acceso.

## Cuándo se activa esta regla

La regla se activa para cada rol de un modelo en modo de compatibilidad con Power BI cuyo permiso no sea `Read`:

```csharp
Model.Database.CompatibilityMode == "PowerBI"

and

ModelPermission != "Read"
```

Los roles de los modelos en modo de compatibilidad con Analysis Services se comprueban mediante @kb.bpa-role-security-not-enforced.

## Cómo solucionarlo

La regla no tiene corrección automática. Configurar un rol como `Read` concede a sus miembros acceso a los datos, así que revise primero cada rol.

### Corrección manual

1. En el **Explorador TOM**, seleccione el rol.
2. Comprueba que los filtros de fila del rol y la seguridad de nivel de objeto (OLS) restrinjan lo que ven sus miembros.
3. En la vista **Propiedades**, establezca **Permiso del modelo** en `Read`.
4. Conceda acceso para actualizar, crear o editar a través de los roles del área de trabajo o los permisos del modelo semántico en el servicio Power BI.

> [!WARNING]
> Si el rol no tiene filtros de filas ni OLS, configurarlo como `Read` da a sus miembros acceso a todos los datos del modelo.

La RLS y la OLS no se aplican a los usuarios con el rol de **Administrador**, **Miembro** o **Colaborador** del área de trabajo. Consulta @object-properties-security.

## Causas comunes

### Causa 1: Rol copiado de un modelo de Analysis Services

El rol procede de un modelo de Analysis Services, donde `Administrator`, `ReadRefresh` y `Refresh` son permisos válidos.

### Causa 2: Rol para una cuenta de actualización

El rol se creó para permitir que una cuenta de servicio actualizara el modelo.

### Causa 3: Nuevo rol sin permiso

Un nuevo rol tiene el permiso `None` hasta que lo establezca.

## Ejemplo

### Antes de la corrección

```text
Role:               Sales Refresh
Model Permission:   ReadRefresh
Row Level Security: 'Region'[Country] = "Denmark"
```

### Después de la corrección

```text
Role:               Sales Refresh
Model Permission:   Read
Row Level Security: 'Region'[Country] = "Denmark"
```

La cuenta de actualización obtiene el rol de **Colaborador** en el área de trabajo del servicio Power BI y no es miembro del rol.

## Reglas relacionadas

- [La seguridad a nivel de fila y a nivel de objeto requiere permiso de lectura](xref:kb.bpa-role-security-not-enforced)
- [Los roles sin seguridad anulan los roles protegidos](xref:kb.bpa-role-unrestricted-read)
- [Evitar miembros tanto en un rol RLS como en un rol OLS](xref:kb.bpa-role-mixed-rls-ols-members)

## Nivel de compatibilidad

Esta regla se aplica a los modelos de Power BI con un nivel de compatibilidad de **1200** o superior.
