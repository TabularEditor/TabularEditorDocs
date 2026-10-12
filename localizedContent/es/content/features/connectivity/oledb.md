---
uid: connect-oledb
title: Conectar mediante OLE DB
author: Morten Lønskov
updated: 2026-09-23
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

# Conectar mediante OLE DB

El conector OLE DB se conecta a fuentes que tienen un proveedor OLE DB, pero no tienen un controlador ODBC que se pueda usar. Al seleccionar **Modelo > Importar tablas...** y elegir **OLE DB**, se abre el cuadro de diálogo **Propiedades de vínculo de datos** de Windows.

![Cuadro de diálogo Propiedades de vínculo de datos en la pestaña Proveedor, con la lista de proveedores OLE DB instalados en el equipo](~/content/assets/images/features/connectivity/oledb-connection.png)

## Requisitos previos

Instala un proveedor OLE DB para el origen que coincida con la arquitectura de tu versión de Tabular Editor.

> [!WARNING]
> Analysis Services admite menos proveedores OLE DB que Windows. Si Analysis Services no admite el proveedor, el origen se importa en Tabular Editor, pero la actualización falla en el servidor. Usa un cuadro de diálogo de conexión específico cuando lo haya y [ODBC](xref:connect-odbc) cuando no lo haya.

## Campos de conexión

El cuadro de diálogo **Propiedades de vínculo de datos** tiene estas pestañas:

| Campo                              | Descripción                                                                                              |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Pestaña **Proveedor**              | Los proveedores OLE DB instalados en este equipo. Selecciona el proveedor para el origen |
| Pestaña **Conexión**               | El Data source, las credenciales y otros ajustes que necesita el proveedor seleccionado                  |
| Pestañas **Avanzadas** y **Todas** | Más propiedades de la cadena de conexión específicas del proveedor                                       |

Si una cadena de conexión guardada especifica un proveedor que no está instalado, aparece una advertencia. Instala el proveedor o selecciona otro.

## Autenticación

El proveedor determina cómo inicias sesión, así que introduce en la pestaña **Conexión** la configuración de inicio de sesión correspondiente, como un nombre de usuario y una contraseña o seguridad Integrada.

Tabular Editor guarda la configuración de conexión y las credenciales en tu archivo de opciones de usuario (consulta [Dónde se almacenan las credenciales](xref:connectivity#where-credentials-are-stored)).
