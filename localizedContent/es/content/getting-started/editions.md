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

Este documento ofrece una visión general y una comparación de las distintas ediciones de Tabular Editor 3.

> [!NOTE]
> Las licencias de Tabular Editor 3 son **por desarrollador**. En otras palabras, solo las personas que usan el producto Tabular Editor 3 necesitarán una licencia.

## Escenarios compatibles de modelado de Data model

La principal diferencia entre las distintas ediciones de Tabular Editor 3 es qué tipos de escenarios de modelado de Data model tabulares admiten. Para entender esta diferencia, tenga en cuenta que Analysis Services (Tabular) existe en varias “variantes”:

- Power BI Desktop (asegúrate de entender las [limitaciones](xref:desktop-limitations))
- Power BI Premium a través del punto de conexión XMLA (Premium Per User, **Premium Capacity [SKUs A, EM o P]**, **Fabric Capacity [SKUs F]**)
- SQL Server (2016+) Analysis Services (ediciones: Developer, Standard y **Enterprise**)
- Azure Analysis Services (niveles: Developer, Basic y **Standard**)

Consideramos que las variantes **resaltadas** de Analysis Services son de nivel Enterprise y, por tanto, solo se pueden usar con la Edición Enterprise de Tabular Editor 3.

> [!IMPORTANT]
> Tabular Editor solo permite editar Data models con un nivel de compatibilidad 1200 o superior. Este es el valor predeterminado en cualquier instancia de Analysis Services a partir de SQL Server 2016. Por el mismo motivo, Tabular Editor no es compatible con Excel PowerPivot, ya que usa un nivel de compatibilidad anterior.

Consulta la matriz siguiente para ver el resumen completo de escenarios compatibles:

| Escenario / Edición                                                       | Desktop                                                 | Business                                                  | Enterprise                                              |
| ------------------------------------------------------------------------- | ------------------------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------- |
| Herramienta externa para Power BI Desktop                                 | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span>   | <span class="emoji">&#10004;</span> |
| Cargar/guardar metadatos del modelo en disco\*\*                          | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>\* | <span class="emoji">&#10004;</span> |
| Modo del área de trabajo\*\*\*                                            | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>\* | <span class="emoji">&#10004;</span> |
| Power BI Premium por usuario                                              | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>   | <span class="emoji">&#10004;</span> |
| SQL Server Developer Edition - edición para desarrolladores               | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>\* | <span class="emoji">&#10004;</span> |
| Edición Standard de SQL Server                                            | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>   | <span class="emoji">&#10004;</span> |
| Edición Enterprise de SQL Server                                          | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |
| Nivel para desarrolladores de Azure AS                                    | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>\* | <span class="emoji">&#10004;</span> |
| Nivel básico de Azure AS                                                  | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>   | <span class="emoji">&#10004;</span> |
| Nivel estándar de Azure AS                                                | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |
| Capacidad de Power BI Premium (SKUs P)                 | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |
| Capacidad de Power BI Embedded (SKUs A/EM)             | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |
| Capacidad de Fabric (SKUs F)                           | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |
| Semantic Bridge (Databricks)                           | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |
| [Cuadro de diálogo de actualización avanzada](xref:advanced-refresh)      | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span>   | <span class="emoji">&#10004;</span> |
| [Licencia gratuita de Optimizador de DAX](xref:dax-optimizer-integration) | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span>   | <span class="emoji">&#10004;</span> |

\***Nota:** Se requiere la Edición Enterprise si el Data model de Analysis Services contiene perspectivas o tablas con varias particiones (no se aplica a los modelos de Power BI Desktop ni de Power BI Premium Per User).

\*\***Nota:** Los formatos de archivo compatibles son: **.pbip** (Proyecto de Power BI), **.pbit** (Plantilla de Power BI), **.bim** (metadatos del modelo de Analysis Services), **.vpax** (Analizador VertiPaq) y **Database.json** (estructura de carpetas de Tabular Editor), **TMDL** (Lenguaje de definición de modelos tabulares).

\*\*\***Nota:** El modo del área de trabajo permite a Tabular Editor 3 guardar simultáneamente los metadatos del modelo en disco y sincronizar una base de datos en cualquiera de las ediciones de Analysis Services o Power BI compatibles con la edición de Tabular Editor 3 adquirida.

## Restricciones de modelado

También restringimos algunas operaciones de modelado de datos dentro de Tabular Editor 3, en línea con las limitaciones de algunos niveles de servicio de Microsoft (Azure Analysis Services _Basic Tier_, SQL Server Analysis Services _Standard Edition_ y Power BI _Premium-Per-User_).

En concreto, [Azure AS Basic Tier y SQL Server Standard Edition no admiten perspectivas, múltiples particiones ni DirectQuery](https://azure.microsoft.com/en-us/pricing/details/analysis-services/), por lo que los modelos de SSAS/Azure AS que usan estas funciones requieren la Edición Enterprise de TE3.

Del mismo modo, [los Workspaces de Power BI Premium-Per-User no admiten los Datasets de Direct Lake](https://learn.microsoft.com/en-us/power-bi/enterprise/directlake-overview#prerequisites), por eso los modelos de Power BI que usan esta función también requieren la Edición Enterprise de TE3.

| Tipo de modelo  | Funcionalidad           | Business                                                | Enterprise                                              |
| --------------- | ----------------------- | ------------------------------------------------------- | ------------------------------------------------------- |
| Azure AS / SSAS | Perspectivas            | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Azure AS / SSAS | Múltiples particiones   | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Azure AS / SSAS | DirectQuery\*           | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Azure AS / SSAS | Direct Lake             | N/D                                                     | N/D                                                     |
| Power BI        | Perspectives\*\*        | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Power BI        | Multiple partitions\*\* | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Power BI        | DirectQuery             | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Power BI        | Direct Lake             | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |

\***Nota:** Analysis Services en SQL Server Standard Edition anterior a 2019 no admite DirectQuery. Tampoco lo admite el nivel Basic de Azure AS. [Más información](https://learn.microsoft.com/en-us/analysis-services/analysis-services-features-by-edition?view=asallproducts-allversions#tabular-models).

\*\***Note:** Perspectives and multiple partitions are available in Business Edition for Power BI models, but the model's `CompatibilityMode` must be set to `PowerBI`. See [Change compatibility mode](xref:change-compatibility-mode) for instructions.

Si intentas abrir un modelo que utiliza una o más de las restricciones de modelado indicadas anteriormente con una licencia TE3 de Edición Business, verás los siguientes mensajes de error:

![Esta edición de Tabular Editor 3 no admite modelos semánticos de nivel Enterprise](https://github.com/TabularEditor/TabularEditorDocs/assets/8976200/7ef69593-ea4b-4a16-a8df-543f5c31ac65)

No hay más diferencias de funcionalidades entre las ediciones de Tabular Editor 3 que las enumeradas arriba.

> [!NOTE]
> Tenga en cuenta que Power BI Desktop [actualmente no admite todas las operaciones de modelado de datos](xref:desktop-limitations). Por este motivo, Tabular Editor 3 bloquea, de forma predeterminada, las operaciones que Power BI Desktop no admite. Sin embargo, esta restricción se puede quitar en Herramientas > Preferencias > Power BI.

> [!IMPORTANT]
> Tabular Editor solo puede usarse como herramienta externa para Power BI Desktop cuando el archivo de Report de Power BI (.pbix, .pbip o .pbit) contiene un Data model (Importación, DirectQuery o compuesto). **No se admiten los Report que usan Live connection** porque estos Report no incluyen un Data model. [Más información](xref:desktop-limitations).

## Licencias personales vs. transferibles

Nuestra Edición de escritorio y la Edición Business utilizan un modelo de licencia **personal**. Esto significa que cada usuario recibe su propia clave de licencia personal, que no se puede compartir ni transferir a otros usuarios. Cuando un usuario ya no necesite el producto, debe cancelar su suscripción para evitar pagos recurrentes.

Nuestra Edición Enterprise usa un modelo de licencias **transferible**. El administrador de licencias recibe una única clave de licencia, que luego es válida para un número de usuarios nominados, hasta la cantidad adquirida. Los usuarios se identifican por su dirección de correo electrónico, que se introduce la primera vez que un usuario activa una instalación de Tabular Editor 3. La primera vez que un usuario activa una instalación de Tabular Editor 3 con la clave de licencia, queda "vinculado" a esa licencia durante 30 días. Después del periodo de vinculación de 30 días, se puede quitar a un usuario de la licencia en cualquier momento, liberando un asiento de licencia para otro usuario. Los administradores de licencias pueden ver y administrar usuarios a través de nuestro [portal de autoservicio](https://tabulareditor.com/my-account). También puedes <a href="mailto:support@tabulareditor.com?subject=Transferable%20License%20Rotation">ponerte en contacto con el equipo de soporte</a> para obtener ayuda.

## Varias instalaciones

Cada usuario de Tabular Editor 3 puede instalar la herramienta en varias máquinas, según el tipo de licencia que tenga:

|                           | Escritorio | Business | Enterprise |
| ------------------------- | ---------- | -------- | ---------- |
| Instalaciones simultáneas | 1          | 2        | 3          |

> [!NOTE]
> Compartir una sola licencia entre varios usuarios va en contra de nuestros [términos de licencia](https://tabulareditor.com/license-terms).

Puedes desactivar una instalación existente en cualquier momento desde la propia herramienta; para ello, elige la opción "Change license key..." en "Help > About Tabular Editor". También puedes desactivar una instalación a través de nuestro [portal de autoservicio](https://tabulareditor.com/sign-in) yendo a la pestaña "Licenses".

Si necesitas más instalaciones simultáneas de Tabular Editor 3 de las indicadas anteriormente, ponte en contacto con [licensing@tabulareditor.com](mailto:licensing@tabulareditor.com).

## Descuentos por volumen para la Edición Enterprise

Nuestra Edición Enterprise tiene precios por niveles, según la siguiente tabla (también se aplican tasas de descuento similares para los compromisos mensuales):

| Nivel                     | Precio anual por puesto |
| ------------------------- | ----------------------- |
| Primeros 5 puestos        | $950,00 USD             |
| Siguientes 6-10 asientos  | $900,00 USD             |
| Siguientes 11-20 asientos | $850,00 USD             |
| Siguientes 21-50 asientos | $800,00 USD             |
| Puestos 51 y en adelante  | $750,00 USD             |

Por ejemplo, si necesitas 12 licencias, el precio se desglosa de la siguiente manera:

```text
Asientos 1-5:    5 x 950,00 = $  4.750,00
Asientos 6-10:   5 x 900,00 = $  4.500,00
Asientos 11-12:  2 x 850,00 = $  1.700,00
--------------------------------------
Total                      $ 10.950,00
======================================
```

Si necesitas más de 100 puestos, <a href="mailto:sales@tabulareditor.com">contacta con ventas</a> para solicitar un presupuesto.
