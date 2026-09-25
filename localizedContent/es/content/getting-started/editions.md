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

Las ediciones se diferencian en dos aspectos: **qué escenarios de modelado de datos** admiten —es decir, dónde puede residir el Data model que estás editando— y **qué funciones** están disponibles una vez que se abre. Las dos secciones siguientes tratan cada aspecto por separado. Todo lo que no figure en ninguna de ellas está disponible en todas las ediciones.

> [!TIP]
> La actualización de una licencia surte efecto de inmediato. Activa la nueva clave en **Ayuda > Acerca de Tabular Editor**; las funciones que desbloquea estarán disponibles sin reiniciar Tabular Editor 3.

## Escenarios compatibles de modelado de Data model

La primera diferencia entre las ediciones es qué tipos de escenarios de modelado de datos tabulares, es decir, de Data model, admiten. Para entender esta diferencia, tenga en cuenta que Analysis Services (Tabular) existe en varias “variantes”:

- Power BI Desktop (asegúrate de entender las [limitaciones](xref:desktop-limitations))
- Power BI Premium a través del punto de conexión XMLA (Premium Per User, **Premium Capacity [SKUs A, EM o P]**, **Fabric Capacity [SKUs F]**)
- SQL Server (2016+) Analysis Services (ediciones: Developer, Standard y **Enterprise**)
- Azure Analysis Services (niveles: Developer, Basic y **Standard**)

Consideramos que las variantes **resaltadas** de Analysis Services son de nivel Enterprise y, por tanto, solo se pueden usar con la Edición Enterprise de Tabular Editor 3.

Trazamos esa línea donde Microsoft traza la suya: entre las licencias por usuario y las basadas en capacidad:

- **Premium Per User es una licencia por puesto.** La persona que edita el modelo es la misma que ha adquirido la licencia. Esto coincide con la licencia de la Edición Business: una clave personal, intransferible y vinculada a un único usuario. Consulta [Licencias personales frente a licencias transferibles](#personal-vs-transferable-licenses).
- **Premium Capacity (P SKUs), Embedded Capacity (A/EM SKUs) y Fabric Capacity (F SKUs) son implementaciones compartidas a escala de toda la organización.** Los modelos alojados allí son propiedad del equipo y dan servicio a muchos consumidores; este es el escenario para el que se ha diseñado la Edición Enterprise y en el que se basa su precio.

La misma lógica se aplica fuera de Power BI. La Edición Business cubre las ediciones Developer y Standard de SQL Server Analysis Services, junto con los niveles Developer y Basic de Azure Analysis Services. Esos niveles están pensados para un solo desarrollador o para una implementación a pequeña escala. SQL Server Analysis Services Enterprise Edition y Azure Analysis Services Standard tier alojan modelos a escala de toda la organización, por lo que requieren la Edición Enterprise.

> [!IMPORTANT]
> Tabular Editor solo permite editar Data models con un nivel de compatibilidad 1200 o superior. Este es el valor predeterminado en cualquier instancia de Analysis Services a partir de SQL Server 2016. Por el mismo motivo, Tabular Editor no es compatible con Excel PowerPivot, ya que usa un nivel de compatibilidad anterior.

Consulta la matriz siguiente para ver el resumen completo de escenarios compatibles:

| Escenario / Edición                                           | Desktop                                                 | Edición Business                                          | Edición Enterprise                                      |
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

## Disponibilidad de funciones

Además de los escenarios anteriores, estas son las funciones cuya disponibilidad depende de la edición. Las licencias Trial y Consultancy incluyen el conjunto de funciones de la Edición Enterprise.

### Edición y actualización

| Funcionalidad                                                                                                                 | Desktop                                                 | Business                                                | Enterprise                                              |
| ----------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- |
| [Guardar con archivos de soporte](xref:save-with-supporting-files) para Fabric                                                | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| [Diálogo de actualización avanzada](xref:advanced-refresh) y [perfiles de anulación de actualización](xref:refresh-overrides) | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Copias de seguridad automáticas de metadatos al guardar y desplegar                                                           | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |

Los comandos habituales de actualización, así como el resto del menú de actualización, están disponibles en todas las ediciones. Las tres filas anteriores no están disponibles en la Edición de escritorio, porque esa edición solo funciona con un modelo activo de Power BI Desktop y no tiene sus propios archivos de modelo.

### Funciones de modelado

| Funcionalidad                                                        | Desktop                                                 | Business                                                | Enterprise                                              |
| -------------------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- |
| Perspectivas en un modelo de Analysis Services\*                     | N/D                                                     | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Tablas con múltiples particiones en un modelo de Analysis Services\* | N/D                                                     | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Perspectivas y múltiples particiones en un modelo de Power BI        | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Tablas de Direct Lake                                                | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| [Semantic Bridge](xref:semantic-bridge) para Databricks Metric Views | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |

\***Nota:** La Edición de escritorio no puede abrir en absoluto modelos de Analysis Services, por lo que estas dos filas no se le aplican. Consulta [Restricciones de modelado](#modeling-restrictions) más abajo para saber qué ocurre cuando un modelo usa una de estas características en una edición que no la permite.

La fila de Semantic Bridge abarca el comando **Importar desde YAML de vista de métricas...** y el objeto `SemanticBridge` en los [C# Scripts](xref:csharp-scripts); en una edición inferior, la opción de menú no se muestra y un script que intenta acceder al servicio genera un Report indicando que no está disponible para tu nivel de licencia.

### Asistente de IA, servidor MCP y políticas de administrador

El [Asistente de IA](xref:ai-assistant) y el [servidor MCP](xref:mcp-server) están disponibles en todas las ediciones. Lo que aporta la Edición Enterprise es la capacidad de gestionarlos de forma centralizada y disponer de un registro de lo que han hecho.

| Funcionalidad                                                                                                                                           | Desktop                                                 | Business                                                | Enterprise                                              |
| ------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- |
| Asistente de IA y servidor MCP                                                                                                                          | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| [Políticas](xref:policies) generales de administrador, como desactivar por completo las actualizaciones, la telemetría, los scripts, las macros o la IA | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> | <span class="emoji">&#10004;</span> |
| Limitar, por recurso, a qué pueden acceder el Asistente de IA y el servidor MCP                                                                         | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Bloquear el proveedor de IA, el punto de conexión, el modelo, la organización y el proyecto, o restringirlos a una lista de elementos permitidos        | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Publicar instrucciones personalizadas para la organización y excluir las que un usuario conserve                                                        | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Restringir herramientas MCP individuales y fijar el puerto del servidor MCP                                                                             | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Permitir únicamente C# Scripts y macros que se limiten al modelo (`BlockUnsafeScripts`)                                              | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Un registro de auditoría local de la actividad del AI Assistant y del servidor MCP                                                                      | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |

> [!IMPORTANT]
> Las políticas de Enterprise nunca se ignoran silenciosamente en una edición que no tenga licencia para ellas. Si alguno de sus valores se configura en un equipo que ejecute Desktop o la Edición Business, el AI Assistant y el servidor MCP se niegan a iniciarse y señalan los valores que requieren la Edición Enterprise; además, un valor de `BlockUnsafeScripts` impide que se ejecute ningún script ni macro hasta que se active una licencia Enterprise. Impleméntalas según las licencias que realmente tengas. Consulta @policies.

### Licencias y soporte

| Funcionalidad                                                                                    | Desktop                                                 | Business                                                | Enterprise                                              |
| ------------------------------------------------------------------------------------------------ | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- |
| [Acceso gratuito al Optimizador de DAX](xref:dax-optimizer-integration)                          | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| **Ayuda > Soporte dedicado** para ponerte en contacto directamente con nuestro equipo de soporte | <span class="emoji">&#10060;</span> | <span class="emoji">&#10060;</span> | <span class="emoji">&#10004;</span> |
| Instalaciones simultáneas por usuario                                                            | 1                                                       | 2                                                       | 3                                                       |

La propia _integración_ del Optimizador de DAX está incluida en todas las ediciones; lo que añade la Edición Enterprise es la posibilidad de canjear un código que te da acceso al Optimizador de DAX sin coste adicional.

### Disponible en todas las ediciones

Todo lo demás es igual, independientemente de la edición que tengas, incluido el editor de DAX y [Code Assist](xref:code-actions), similar a IntelliSense; las [consultas DAX](xref:dax-query) y el [Depurador de DAX](xref:dax-debugger); los [scripts DAX](xref:dax-scripts) y las [funciones definidas por el usuario](xref:udfs); los [C# Script](xref:csharp-scripts) y las [macro](xref:macros); el [Best Practice Analyzer](xref:using-bpa) con sus [reglas integradas](xref:built-in-bpa-rules); el [Editor de perspectiva](xref:perspective-editor); el [Editor de traducción de metadatos](xref:metadata-translation-editor); el [Editor de calendario](xref:calendars); los [grupos de tablas](xref:table-groups); los [diagramas](xref:diagram-view); la [vista previa de datos](xref:table-preview) y las [Pivot Grid](xref:pivot-grid); la integración del Analizador VertiPaq; el [Administrador de paquetes DAX](xref:dax-package-manager); el [Asistente para importar tablas](xref:import-tables) y los [indicadores de cambios no guardados](xref:unsaved-changes).

## Restricciones de modelado

También restringimos algunas operaciones de modelado de datos dentro de Tabular Editor 3, en línea con las limitaciones de algunos niveles de servicio de Microsoft (Azure Analysis Services _Basic Tier_, SQL Server Analysis Services _Standard Edition_ y Power BI _Premium-Per-User_).

En concreto, [Azure AS Basic Tier y SQL Server Standard Edition no admiten perspectivas ni múltiples particiones](https://azure.microsoft.com/en-us/pricing/details/analysis-services/), por lo que los modelos de SSAS/Azure AS que usan estas funciones requieren la Edición Enterprise de TE3. DirectQuery no está restringido en absoluto por tu edición de Tabular Editor 3: que puedas usarlo depende del servidor en el que esté alojado el modelo.

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

La edición de escritorio solo funciona con un modelo de Power BI Desktop en vivo, por lo que las filas de Analysis Services no le aplican.

Si intentas abrir un modelo que utiliza una o más de las restricciones de modelado indicadas anteriormente con una licencia TE3 de Edición Business, verás los siguientes mensajes de error:

![Esta edición de Tabular Editor 3 no admite modelos semánticos de nivel Enterprise](~/content/assets/images/editions-01.png)

Un modelo que incorpore una de estas características mientras lo editas tampoco se estropea sin avisar: se rechaza el guardado y en Mensajes se indica la característica y, si hay varias particiones, las tablas en cuestión. Se bloquea de entrada la posibilidad de agregar una perspectiva a un modelo de Analysis Services: la carpeta **Perspectives** no se muestra en el Explorador TOM y el comando para crear una no está disponible.

> [!IMPORTANT]
> Tabular Editor solo puede usarse como herramienta externa para Power BI Desktop cuando el archivo de Report de Power BI (.pbix, .pbip o .pbit) contiene un Data model (Importación, DirectQuery o compuesto). **No se admiten los Report que usan Live connection** porque estos Report no incluyen un Data model. [Más información](xref:desktop-limitations).

## Licencias personales vs. transferibles

Nuestra Edición de escritorio y la Edición Business utilizan un modelo de licencia **personal**. Esto significa que cada usuario recibe su propia clave de licencia personal, que no se puede compartir ni transferir a otros usuarios. Cuando un usuario ya no necesite el producto, debe cancelar su suscripción para evitar pagos recurrentes.

Nuestra Edición Enterprise usa un modelo de licencias **transferible**. El administrador de licencias recibe una única clave de licencia, que luego es válida para un número de usuarios nominados, hasta la cantidad adquirida. Los usuarios se identifican por su dirección de correo electrónico, que se introduce la primera vez que un usuario activa una instalación de Tabular Editor 3. La primera vez que un usuario activa una instalación de Tabular Editor 3 con la clave de licencia, queda "vinculado" a esa licencia durante 30 días. Después del periodo de vinculación de 30 días, se puede quitar a un usuario de la licencia en cualquier momento, liberando un asiento de licencia para otro usuario. Los administradores de licencias pueden ver y administrar usuarios a través de nuestro [portal de autoservicio](https://tabulareditor.com/my-account). También puedes <a href="mailto:support@tabulareditor.com?subject=Transferable%20License%20Rotation">ponerte en contacto con el equipo de soporte</a> para obtener ayuda.

## Varias instalaciones

Cada usuario de Tabular Editor 3 puede instalar la herramienta en varias máquinas, según el tipo de licencia que tenga:

|                           | Desktop | Negocios | Corporativo |
| ------------------------- | ------- | -------- | ----------- |
| Instalaciones simultáneas | 1       | 2        | 3           |

> [!NOTE]
> Compartir una sola licencia entre varios usuarios va en contra de nuestros [términos de licencia](https://tabulareditor.com/eula-te3).

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
Seats 1-5:    5 x 950.00 = $  4,750.00
Seats 6-10:   5 x 900.00 = $  4,500.00
Seats 11-12:  2 x 850.00 = $  1,700.00
--------------------------------------
Total                      $ 10,950.00
======================================
```

Si necesitas más de 100 puestos, <a href="mailto:sales@tabulareditor.com">contacta con ventas</a> para solicitar un presupuesto.

## Licencias para la línea de comandos y CI/CD

Tabular Editor 3 es una aplicación de escritorio. No tiene una interfaz de línea de comandos propia. Para implementaciones automatizadas y canalizaciones de CI/CD, utilice `TabularEditor.exe` (la [línea de comandos de Tabular Editor 2](xref:command-line-options)) o el [Tabular Editor CLI](xref:te-cli) (`te`), que es multiplataforma. Ambos son independientes de la aplicación de escritorio Tabular Editor 3.

> **¿Necesito una licencia para ejecutar canalizaciones de CI/CD?**
> No. `TabularEditor.exe` (TE2 CLI) y el Tabular Editor CLI (`te`, en versión preliminar) no requieren una licencia de Tabular Editor 3. Solo los desarrolladores que usan la aplicación de escritorio Tabular Editor 3 necesitan una licencia.

En la disponibilidad general (GA), el Tabular Editor CLI requerirá una licencia; los precios aún se están ultimando y se anunciarán antes de la GA.