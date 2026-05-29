---
uid: editions
title: Comparar ediciones
author: Søren Toft Joensen
updated: 2025-02-07
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      full: true
---

# Ediciones de Tabular Editor 3

Este documento ofrece una descripción general y una comparación de las distintas ediciones de Tabular Editor 3.

> [!NOTE]
> Las licencias de Tabular Editor 3 son **por desarrollador**. En otras palabras, solo necesitan licencia las personas que usan el producto Tabular Editor 3.

## Escenarios de modelado de Data model compatibles

La principal diferencia entre las distintas ediciones de Tabular Editor 3 es qué tipos de escenarios de modelado de Data model tabulares admiten. Para entender esta diferencia, tenga en cuenta que Analysis Services (Tabular) existe en varias "variantes":

- Power BI Desktop (asegúrate de comprender las [limitaciones](xref:desktop-limitations))
- Power BI Premium a través del punto de conexión XMLA (Premium Per User, **capacidad Premium [SKU A, EM o P]**, **capacidad de Fabric [SKU F]**)
- SQL Server (2016+) Analysis Services (ediciones: Developer, Standard, **Enterprise**)
- Azure Analysis Services (niveles: Developer, Basic, **Standard**)

Consideramos que las variantes de Analysis Services **resaltadas** son de nivel Enterprise y, por tanto, solo pueden usarse con la Edición Enterprise de Tabular Editor 3.

> [!IMPORTANT]
> Tabular Editor solo permite editar Data models con nivel de compatibilidad 1200 o superior. Este es el valor predeterminado en cualquier instancia de Analysis Services a partir de SQL Server 2016. Por el mismo motivo, Tabular Editor no es compatible con PowerPivot para Excel, ya que usa un nivel de compatibilidad anterior.

Consulta la matriz siguiente para ver el resumen completo de los escenarios compatibles:

| Escenario / Edición                                                        | Desktop                                                 | Business                                                  | Enterprise                                              |
| -------------------------------------------------------------------------- | ------------------------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------- |
| Herramienta externa para Power BI Desktop                                  | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   | <span class="emoji">&#10004;</span> |
| Cargar/guardar los metadatos del modelo en el disco\*\*                    | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>\* | <span class="emoji">&#10004;</span> |
| Modo del área de trabajo\*\*\*                                             | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>\* | <span class="emoji">&#10004;</span> |
| Power BI Premium por usuario                                               | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>   | <span class="emoji">&#10004;</span> |
| SQL Server Developer Edition                                               | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>\* | <span class="emoji">&#10004;</span> |
| SQL Server Standard Edition                                                | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>   | <span class="emoji">&#10004;</span> |
| SQL Server Edición Enterprise                                              | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |
| Nivel para desarrolladores de Azure AS                                     | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>\* | <span class="emoji">&#10004;</span> |
| Nivel básico de Azure AS                                                   | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>   | <span class="emoji">&#10004;</span> |
| Nivel estándar de Azure AS                                                 | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |
| Capacidad de Power BI Premium (SKUs P)                  | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |
| Capacidad de Power BI Embedded (SKUs A/EM)              | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |
| Capacidad de Fabric (SKUs F)                            | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |
| Puente semántico (Databricks)                           | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |
| [Cuadro de diálogo de actualización avanzada](xref:advanced-refresh)       | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>   | <span class="emoji">&#10004;</span> |
| [Licencia gratuita del Optimizador de DAX](xref:dax-optimizer-integration) | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |

\***Nota:** Se requiere la Edición Enterprise si el Data model de Analysis Services contiene perspectivas o tablas con varias particiones (no se aplica a los modelos de Power BI Desktop ni a los de Power BI Premium Per User).

\*\***Nota:** Los formatos de archivo compatibles son: **.pbip** (Proyecto de Power BI), **.pbit** (Plantilla de Power BI), **.bim** (metadatos del modelo de Analysis Services), **.vpax** (Analizador VertiPaq) y **Database.json** (estructura de carpetas de Tabular Editor) y **TMDL** (Tabular Model Definition Language).

\*\*\***Nota:** El modo del área de trabajo permite a Tabular Editor 3 guardar simultáneamente metadatos del modelo en disco y sincronizar una base de datos en cualquiera de las ediciones de Analysis Services o Power BI compatibles con la edición de Tabular Editor 3 adquirida.

## Restricciones de modelado

También restringimos algunas operaciones de modelado de datos dentro de Tabular Editor 3, en línea con las restricciones de determinados niveles de servicio de Microsoft (Azure Analysis Services _Basic Tier_, SQL Server Analysis Services _Standard Edition_ y Power BI _Premium-Per-User_).

En concreto, [Azure AS Basic Tier y SQL Server Standard Edition no admiten perspectivas, varias particiones ni DirectQuery](https://azure.microsoft.com/en-us/pricing/details/analysis-services/), por lo que los modelos de SSAS/Azure AS que usan estas características requieren la Edición Enterprise de TE3.

Del mismo modo, [los Workspace de Power BI Premium-Per-User no admiten los Dataset de Direct Lake](https://learn.microsoft.com/en-us/power-bi/enterprise/directlake-overview#prerequisites), por lo que los modelos de Power BI que usan esta característica también requieren la Edición Enterprise de TE3.

| Tipo de modelo  | Característica         | Business                                                | Enterprise                                              |
| --------------- | ---------------------- | ------------------------------------------------------- | ------------------------------------------------------- |
| Azure AS / SSAS | Perspectivas           | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Azure AS / SSAS | Varias particiones     | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Azure AS / SSAS | DirectQuery\*          | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Azure AS / SSAS | Direct Lake            | N/A                                                     | N/A                                                     |
| Power BI        | Perspectivas\*\*       | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Power BI        | Varias particiones\*\* | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Power BI        | DirectQuery            | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Power BI        | Direct Lake            | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |

\***Nota:** Analysis Services en SQL Server Standard Edition anteriores a 2019 no admite DirectQuery. Azure AS Basic Tier tampoco. [Más información](https://learn.microsoft.com/en-us/analysis-services/analysis-services-features-by-edition?view=asallproducts-allversions#tabular-models).

\*\***Nota:** Las perspectivas y varias particiones están disponibles en la Edición Business para los modelos de Power BI, pero el `CompatibilityMode` del modelo debe establecerse en `PowerBI`. Consulta [Cambiar el modo de compatibilidad](xref:change-compatibility-mode) para obtener instrucciones.

Si intentas abrir un modelo que usa una o varias de las restricciones de modelado indicadas arriba mientras usas una licencia de la Edición Business de TE3, verás el siguiente mensaje de error:

![Esta edición de Tabular Editor 3 no admite modelos semánticos de nivel Enterprise](https://github.com/TabularEditor/TabularEditorDocs/assets/8976200/7ef69593-ea4b-4a16-a8df-543f5c31ac65)

No hay más diferencias de funcionalidades entre las ediciones de Tabular Editor 3 que las indicadas arriba.

> [!NOTE]
> Ten en cuenta que Power BI Desktop [actualmente no admite todas las operaciones de Data model](xref:desktop-limitations). Por este motivo, Tabular Editor 3 bloquea de forma predeterminada las operaciones que Power BI Desktop no admite. Sin embargo, puedes quitar esta restricción en Herramientas > Preferencias > Power BI.

> [!IMPORTANT]
> Tabular Editor solo se puede usar como herramienta externa para Power BI Desktop cuando el archivo de Report de Power BI (.pbix, .pbip o .pbit) contiene un Data model (Importación, DirectQuery o Compuesto). **No se admiten los Reports con conexión en vivo** porque no contienen un Data model. [Más información](xref:desktop-limitations).

## Licencias personales frente a transferibles

Nuestra Edición de escritorio y la Edición Business utilizan un modelo de licencia **personal**. Esto significa que cada usuario recibe su propia clave de licencia personal, que no se puede compartir ni transferir a otros usuarios. Cuando un usuario ya no necesite el producto, debe cancelarse la suscripción para evitar pagos recurrentes.

Nuestra Edición Enterprise usa un modelo de licencia **transferible**. El administrador de licencias recibe una única clave de licencia, que es válida para un número de usuarios con nombre hasta el límite de la cantidad adquirida. Los usuarios se identifican por su dirección de correo electrónico, que se introduce la primera vez que un usuario activa una instalación de Tabular Editor 3. La primera vez que un usuario activa una instalación de Tabular Editor 3 con la clave de licencia, queda vinculado a esa licencia durante 30 días. Una vez transcurrido el período de vinculación de 30 días, se puede desvincular a un usuario de la licencia en cualquier momento, liberando el cupo de licencia para otro usuario. Los administradores de licencias pueden ver y administrar usuarios desde nuestro [portal de autoservicio](https://tabulareditor.com/my-account). También puedes <a href="mailto:support@tabulareditor.com?subject=Transferable%20License%20Rotation">ponerte en contacto con el servicio de soporte</a> para obtener ayuda.

## Varias instalaciones

Cada usuario de Tabular Editor 3 puede instalar la herramienta en varios equipos, según el tipo de licencia que tenga:

|                           | Desktop | Business | Enterprise |
| ------------------------- | ------- | -------- | ---------- |
| Instalaciones simultáneas | 1       | 2        | 3          |

> [!NOTE]
> Compartir una única licencia entre varios usuarios incumple nuestros [términos de licencia](https://tabulareditor.com/license-terms).

Puedes desactivar una instalación existente en cualquier momento desde la propia herramienta, seleccionando la opción "Change license key..." en "Help > About Tabular Editor". También puedes desactivar una instalación desde nuestro [portal de autoservicio](https://tabulareditor.com/sign-in) yendo a la pestaña "Licenses".

Si necesitas más instalaciones simultáneas de Tabular Editor 3 de las indicadas arriba, ponte en contacto con [licensing@tabulareditor.com](mailto:licensing@tabulareditor.com).

## Descuentos por volumen de la Edición Enterprise

El precio de nuestra Edición Enterprise se estructura en niveles, según la siguiente tabla (se aplican tasas de descuento similares con el compromiso mensual):

| Tramo                        | Precio anual por puesto |
| ---------------------------- | ----------------------- |
| Primeros 5 puestos           | $950,00 USD             |
| Siguientes 6-10 puestos      | $900,00 USD             |
| Siguientes 11-20 puestos     | $850,00 USD             |
| Siguientes 21 a 50 licencias | $800,00 USD             |
| 51 o más licencias           | $750,00 USD             |

A modo de ejemplo, si necesitas 12 asientos, el precio se desglosa de la siguiente manera:

```text
Seats 1-5:    5 x 950.00 = $  4,750.00
Seats 6-10:   5 x 900.00 = $  4,500.00
Seats 11-12:  2 x 850.00 = $  1,700.00
--------------------------------------
Total                      $ 10,950.00
======================================
```

Si necesitas más de 100 asientos, <a href="mailto:sales@tabulareditor.com">ponte en contacto con Ventas</a> para solicitar un presupuesto.
