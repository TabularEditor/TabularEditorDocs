---
uid: editions
title: Comparar ediciones
author: Søren Toft Joensen
updated: 2026-09-22
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      full: true
---

# Ediciones de Tabular Editor 3

Este documento ofrece una visión general y una comparación de las distintas ediciones de Tabular Editor 3.

> [!NOTE]
> Las licencias de Tabular Editor 3 son **por desarrollador**. En otras palabras, solo las personas que usan el producto Tabular Editor 3 necesitarán una licencia.

The editions differ in two ways: **which data modeling scenarios** they support - that is, where the model you are editing may live - and **which features** are available once it is open. The two sections below cover each in turn. Anything not listed in either is available in every edition.

> [!TIP]
> Upgrading a license takes effect straight away. Activate the new key under **Help > About Tabular Editor**, and the features it unlocks are available without restarting Tabular Editor 3.

## Escenarios compatibles de modelado de Data model

The first difference between the editions is which types of tabular data modeling scenarios they support. Para entender esta diferencia, tenga en cuenta que Analysis Services (Tabular) existe en varias “variantes”:

- Power BI Desktop (asegúrate de entender las [limitaciones](xref:desktop-limitations))
- Power BI Premium a través del punto de conexión XMLA (Premium Per User, **Premium Capacity [SKUs A, EM o P]**, **Fabric Capacity [SKUs F]**)
- SQL Server (2016+) Analysis Services (ediciones: Developer, Standard y **Enterprise**)
- Azure Analysis Services (niveles: Developer, Basic y **Standard**)

Consideramos que las variantes **resaltadas** de Analysis Services son de nivel Enterprise y, por tanto, solo se pueden usar con la Edición Enterprise de Tabular Editor 3.

We draw that line where Microsoft draws its own, between per-user and capacity-based licensing:

- **Premium Per User is a per-seat license.** The person editing the model is the person who paid for the seat. That matches how Business Edition is licensed: a personal, non-transferable key tied to a single user. See [Personal vs. Transferable licenses](#personal-vs-transferable-licenses).
- **Premium Capacity (P SKUs), Embedded Capacity (A/EM SKUs) and Fabric Capacity (F SKUs) are shared, organization-scale deployments.** Models hosted there are team-owned and serve many consumers, which is the scenario Enterprise Edition is built and priced for.

The same logic applies outside Power BI. Business Edition covers the SQL Server Analysis Services Developer and Standard editions along with the Azure Analysis Services Developer and Basic tiers. Those tiers serve a single developer or a small-scale deployment. SQL Server Analysis Services Enterprise Edition and Azure Analysis Services Standard tier host organization-scale models, so they require Enterprise Edition.

> [!IMPORTANT]
> Tabular Editor solo permite editar Data models con un nivel de compatibilidad 1200 o superior. Este es el valor predeterminado en cualquier instancia de Analysis Services a partir de SQL Server 2016. Por el mismo motivo, Tabular Editor no es compatible con Excel PowerPivot, ya que usa un nivel de compatibilidad anterior.

Consulta la matriz siguiente para ver el resumen completo de escenarios compatibles:

| Escenario / Edición                                           | Desktop                                                 | Business                                                  | Enterprise                                              |
| ------------------------------------------------------------- | ------------------------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------- |
| Herramienta externa para Power BI Desktop                     | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   | <span class="emoji">&#10004;</span> |
| Cargar/guardar los metadatos del modelo en disco\*\*          | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>\* | <span class="emoji">&#10004;</span> |
| Modo del área de trabajo\*\*\*                                | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>\* | <span class="emoji">&#10004;</span> |
| Power BI Premium por usuario                                  | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>   | <span class="emoji">&#10004;</span> |
| SQL Server Developer Edition - edición para desarrolladores   | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>\* | <span class="emoji">&#10004;</span> |
| Edición Standard de SQL Server                                | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>   | <span class="emoji">&#10004;</span> |
| Edición Enterprise de SQL Server                              | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |
| Nivel para desarrolladores de Azure AS                        | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>\* | <span class="emoji">&#10004;</span> |
| Nivel básico de Azure AS                                      | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>   | <span class="emoji">&#10004;</span> |
| Nivel estándar de Azure AS                                    | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |
| Capacidad de Power BI Premium (SKUs P)     | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |
| Capacidad de Power BI Embedded (SKUs A/EM) | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |
| Capacidad de Fabric (SKUs F)               | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |

\***Nota:** Se requiere la Edición Enterprise si el Data model de Analysis Services contiene perspectivas o tablas con varias particiones (no se aplica a los modelos de Power BI Desktop ni de Power BI Premium Per User).

\*\***Nota:** Los formatos de archivo compatibles son: **.pbip** (Proyecto de Power BI), **.pbit** (Plantilla de Power BI), **.bim** (metadatos del modelo de Analysis Services), **.vpax** (Analizador VertiPaq) y **Database.json** (estructura de carpetas de Tabular Editor), **TMDL** (Lenguaje de definición de modelos tabulares).

\*\*\***Nota:** El modo del área de trabajo permite a Tabular Editor 3 guardar simultáneamente los metadatos del modelo en disco y sincronizar una base de datos en cualquiera de las ediciones de Analysis Services o Power BI compatibles con la edición de Tabular Editor 3 adquirida.

## Feature availability

Beyond the scenarios above, these are the features whose availability depends on the edition. Trial and Consultancy licenses carry the Enterprise Edition feature set.

### Editing and refreshing

| Funcionalidad                                                                                            | Desktop                                                 | Business                                                | Enterprise                                              |
| -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- |
| [Save with supporting files](xref:save-with-supporting-files) for Fabric                                 | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| [Advanced Refresh dialog](xref:advanced-refresh) and [refresh override profiles](xref:refresh-overrides) | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Automatic metadata backups on save and deploy                                                            | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |

Ordinary refresh commands, and everything else in the refresh menu, are available in every edition. The three rows above are unavailable in Desktop Edition because that edition works only against a live Power BI Desktop model, with no model files of its own.

### Modeling features

| Funcionalidad                                                       | Desktop                                                 | Business                                                | Enterprise                                              |
| ------------------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- |
| Perspectives in an Analysis Services model\*                        | N/D                                                     | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Tables with multiple partitions in an Analysis Services model\*     | N/D                                                     | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Perspectives and multiple partitions in a Power BI model            | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Direct Lake tables                                                  | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| [Semantic Bridge](xref:semantic-bridge) for Databricks Metric Views | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |

\***Note:** Desktop Edition cannot open Analysis Services models at all, which is why these two rows do not apply to it. See [Modeling Restrictions](#modeling-restrictions) below for what happens when a model uses one of these features on an edition that does not allow it.

The Semantic Bridge row covers the **Import from Metric View YAML...** command and the `SemanticBridge` object in [C# scripts](xref:csharp-scripts); on a lower edition the menu item is not shown, and a script that reaches for the service reports that it is unavailable at your license level.

### AI Assistant, MCP server and administrator policies

The [AI Assistant](xref:ai-assistant) and the [MCP server](xref:mcp-server) themselves are available in every edition. What Enterprise Edition adds is the ability to govern them centrally, and a record of what they did.

| Funcionalidad                                                                                                           | Desktop                                                 | Business                                                | Enterprise                                              |
| ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- |
| AI Assistant and MCP server                                                                                             | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| General administrator [policies](xref:policies), such as turning off updates, telemetry, scripts, macros or AI entirely | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Capping what the AI Assistant and the MCP server may reach, per resource                                                | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Locking the AI provider, endpoint, model, organization and project, or restricting them to an allowlist                 | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Publishing Custom Instructions for the organization, and ruling out the ones a user keeps                               | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Withholding individual MCP tools, and fixing the MCP server port                                                        | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Allowing only C# scripts and macros that stay within the model (`BlockUnsafeScripts`)                | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| A local audit record of AI Assistant and MCP server activity                                                            | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |

> [!IMPORTANT]
> The Enterprise policies are never quietly ignored on an edition that is not licensed for them. If any of their values is set on a machine running Desktop or Business Edition, the AI Assistant and the MCP server refuse to start and name the values that require Enterprise Edition, and a `BlockUnsafeScripts` value stops every script and macro from running until an Enterprise license is activated. Roll them out against the licenses you actually have. See @policies.

### Licensing and support

| Funcionalidad                                                         | Desktop                                                 | Business                                                | Enterprise                                              |
| --------------------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- |
| [Free DAX Optimizer access](xref:dax-optimizer-integration)           | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| **Help > Dedicated Support** for contacting our support team directly | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Simultaneous installations per user                                   | 1                                                       | 2                                                       | 3                                                       |

The DAX Optimizer _integration_ itself is in every edition; what Enterprise Edition adds is eligibility for a redemption code that gives you DAX Optimizer access at no extra cost.

### Available in every edition

Everything else is the same whichever edition you hold, including the DAX editor and IntelliSense-like [code assist](xref:code-actions), [DAX queries](xref:dax-query) and the [DAX debugger](xref:dax-debugger), [DAX scripts](xref:dax-scripts) and [user-defined functions](xref:udfs), [C# scripts](xref:csharp-scripts) and [macros](xref:macros), the [Best Practice Analyzer](xref:using-bpa) with its [built-in rules](xref:built-in-bpa-rules), the [Perspective Editor](xref:perspective-editor), the [Metadata Translation Editor](xref:metadata-translation-editor), the [Calendar Editor](xref:calendars), [table groups](xref:table-groups), [diagrams](xref:diagram-view), [data preview](xref:table-preview) and [pivot grids](xref:pivot-grid), the VertiPaq Analyzer integration, the [DAX Package Manager](xref:dax-package-manager), the [Table Import Wizard](xref:import-tables) and [unsaved change indicators](xref:unsaved-changes).

## Restricciones de modelado

También restringimos algunas operaciones de modelado de datos dentro de Tabular Editor 3, en línea con las limitaciones de algunos niveles de servicio de Microsoft (Azure Analysis Services _Basic Tier_, SQL Server Analysis Services _Standard Edition_ y Power BI _Premium-Per-User_).

Specifically, [Azure AS Basic Tier and SQL Server Standard Edition do not support perspectives or multiple partitions](https://azure.microsoft.com/en-us/pricing/details/analysis-services/), and as such, SSAS/Azure AS models using these features require TE3 Enterprise Edition. DirectQuery is not restricted by your Tabular Editor 3 edition at all: whether you can use it depends on the server the model is hosted on.

Del mismo modo, [los Workspaces de Power BI Premium-Per-User no admiten los Datasets de Direct Lake](https://learn.microsoft.com/en-us/power-bi/enterprise/directlake-overview#prerequisites), por eso los modelos de Power BI que usan esta función también requieren la Edición Enterprise de TE3.

| Tipo de modelo  | Funcionalidad             | Desktop                                                 | Business                                                | Enterprise                                              |
| --------------- | ------------------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- |
| Azure AS / SSAS | Perspectivas              | N/D                                                     | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Azure AS / SSAS | Múltiples particiones     | N/D                                                     | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Azure AS / SSAS | DirectQuery\*             | N/D                                                     | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Azure AS / SSAS | Direct Lake               | N/D                                                     | N/D                                                     | N/D                                                     |
| Power BI        | Perspectivas\*\*          | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Power BI        | Múltiples particiones\*\* | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Power BI        | DirectQuery               | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Power BI        | Direct Lake               | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |

\***Nota:** Analysis Services en SQL Server Standard Edition anterior a 2019 no admite DirectQuery. Tampoco lo admite el nivel Basic de Azure AS. [Más información](https://learn.microsoft.com/en-us/analysis-services/analysis-services-features-by-edition?view=asallproducts-allversions#tabular-models).

\*\***Nota:** Las perspectivas y las múltiples particiones están disponibles en la Edición Business para modelos de Power BI, pero el `CompatibilityMode` del modelo debe establecerse en `PowerBI`. Consulte [Cambiar el modo de compatibilidad](xref:change-compatibility-mode) para obtener instrucciones.

Desktop Edition works only against a live Power BI Desktop model, which is why the Analysis Services rows do not apply to it.

Si intentas abrir un modelo que utiliza una o más de las restricciones de modelado indicadas anteriormente con una licencia TE3 de Edición Business, verás los siguientes mensajes de error:

![This edition of Tabular Editor 3 does not support Enterprise-tier semantic models](~/content/assets/images/editions-01.png)

A model that acquires one of these while you are editing it is not silently mangled either: the save is refused, and the message names the feature and, for multiple partitions, the tables in question. Adding a perspective to an Analysis Services model is prevented up front - the **Perspectives** folder is not shown in the TOM Explorer and the command to create one is unavailable.

> [!IMPORTANT]
> Tabular Editor solo puede usarse como herramienta externa para Power BI Desktop cuando el archivo de Report de Power BI (.pbix, .pbip o .pbit) contiene un Data model (Importación, DirectQuery o compuesto). **No se admiten los Report que usan Live connection** porque estos Report no incluyen un Data model. [Más información](xref:desktop-limitations).

## Licencias personales vs. transferibles

Nuestra Edición de escritorio y la Edición Business utilizan un modelo de licencia **personal**. Esto significa que cada usuario recibe su propia clave de licencia personal, que no se puede compartir ni transferir a otros usuarios. Cuando un usuario ya no necesite el producto, debe cancelar su suscripción para evitar pagos recurrentes.

Nuestra Edición Enterprise usa un modelo de licencias **transferible**. El administrador de licencias recibe una única clave de licencia, que luego es válida para un número de usuarios nominados, hasta la cantidad adquirida. Los usuarios se identifican por su dirección de correo electrónico, que se introduce la primera vez que un usuario activa una instalación de Tabular Editor 3. La primera vez que un usuario activa una instalación de Tabular Editor 3 con la clave de licencia, queda "vinculado" a esa licencia durante 30 días. Después del periodo de vinculación de 30 días, se puede quitar a un usuario de la licencia en cualquier momento, liberando un asiento de licencia para otro usuario. Los administradores de licencias pueden ver y administrar usuarios a través de nuestro [portal de autoservicio](https://tabulareditor.com/my-account). También puedes <a href="mailto:support@tabulareditor.com?subject=Transferable%20License%20Rotation">ponerte en contacto con el equipo de soporte</a> para obtener ayuda.

## Varias instalaciones

Cada usuario de Tabular Editor 3 puede instalar la herramienta en varias máquinas, según el tipo de licencia que tenga:

|                           | Desktop | Business | Enterprise |
| ------------------------- | ------- | -------- | ---------- |
| Instalaciones simultáneas | 1       | 2        | 3          |

> [!NOTE]
> Sharing a single license among multiple users is against our [licensing terms](https://tabulareditor.com/eula-te3).

Puedes desactivar una instalación existente en cualquier momento desde la propia herramienta; para ello, elige la opción "Change license key..." en "Help > About Tabular Editor". También puedes desactivar una instalación a través de nuestro [portal de autoservicio](https://tabulareditor.com/sign-in) yendo a la pestaña "Licenses".

Si necesitas más instalaciones simultáneas de Tabular Editor 3 de las indicadas anteriormente, ponte en contacto con [licensing@tabulareditor.com](mailto:licensing@tabulareditor.com).

## Descuentos por volumen para la Edición Enterprise

Nuestra Edición Enterprise tiene precios por niveles, según la siguiente tabla (también se aplican tasas de descuento similares para los compromisos mensuales):

| Tier                      | Precio anual por puesto |
| ------------------------- | ----------------------- |
| Primeros 5 puestos        | $950,00 USD             |
| Siguientes 6-10 asientos  | $900,00 USD             |
| Siguientes 11-20 asientos | $850,00 USD             |
| Siguientes 21-50 asientos | $800,00 USD             |
| Puestos 51 y en adelante  | $750,00 USD             |

Por ejemplo, si necesitas 12 licencias, el precio se desglosa de la siguiente manera:

```text
Seats 1-5:    5 x 950.00 = $  4,750.00
Seats 6-10:   5 x 900.00 = $  4,500.00
Seats 11-12:  2 x 850.00 = $  1,700.00
--------------------------------------
Total                      $ 10,950.00
======================================
```

Si necesitas más de 100 puestos, <a href="mailto:sales@tabulareditor.com">contacta con ventas</a> para solicitar un presupuesto.

## Command-line and CI/CD licensing

Tabular Editor 3 is a desktop application. It has no command-line interface of its own. For automated deployments and CI/CD pipelines, use either `TabularEditor.exe` (the [Tabular Editor 2 command line](xref:command-line-options)) or the cross-platform [Tabular Editor CLI](xref:te-cli) (`te`). Both are separate from the Tabular Editor 3 desktop application.

> **Do I need a license to run CI/CD pipelines?**
> No. `TabularEditor.exe` (TE2 CLI) and the Tabular Editor CLI (`te`, during preview) do not require a Tabular Editor 3 license. Only developers using the Tabular Editor 3 desktop application need a license.

At General Availability the Tabular Editor CLI will require a license; pricing is still being finalized and will be announced ahead of GA.