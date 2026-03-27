---
uid: dq-over-as-limitations
title: Consulta directa sobre Analysis Services
author: Morten Lønskov
updated: 2025-07-14
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

## Información general

Tabular Editor 3 puede **conectarse** a modelos compuestos que aprovechan **DirectQuery over Analysis Services (DQ‑over‑AS)**, pero la compatibilidad total con el modelado **aún no está disponible**.  La mayoría de las tareas de autoría funcionan según lo esperado; sin embargo, las operaciones que dependen de sincronizar metadatos con el modelo semántico remoto —como _Actualizar esquema de tabla_— están actualmente limitadas.

> [!IMPORTANT]
> Hasta que se lance la compatibilidad completa con DQ‑over‑AS, los metadatos del modelo que se editen en Tabular Editor 3 **no se mantienen sincronizados automáticamente** con el conjunto de datos de origen. Debe aplicar una de las soluciones alternativas que se enumeran a continuación siempre que se agreguen columnas o medidas al modelo subyacente de Analysis Services.

## Limitaciones actuales

| Característica                  | Estado en TE3  | Notas                                                                                                                               |
| ------------------------------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **Actualizar esquema de tabla** | ❌ No se admite | Al intentar ejecutar **Modelo > Actualizar esquema de tabla** en una tabla DQ‑over‑AS, no se produce ningún efecto. |
| **Sincronización de medidas**   | ❌ No se admite | Las medidas creadas en el conjunto de datos de origen no aparecen automáticamente en el modelo compuesto.           |

## Soluciones alternativas

### 1. Agregar manualmente las columnas que faltan

1. En el **Explorador TOM**, seleccione la tabla que requiere la nueva columna.
2. Elija **Agregar > Columna de datos**.
3. En la ventana _Propiedades_, configure lo siguiente:

   - **SourceColumnName** – debe coincidir _exactamente_ con el **Name** de la columna de la tabla remota.
   - **SourceLineageTag** – copie el valor de **LineageTag** de la columna de origen.
4. Guarde e implemente el modelo.

> [!NOTE]
> Los nombres de las columnas y las etiquetas de linaje deben coincidir _carácter por carácter_.  Cualquier discrepancia provocará errores de implementación.

### 2. Use el script de C# “Importar tablas desde el modelo remoto”

El artículo de Daniel Otykier en LinkedIn ofrece un [script de automatización en C# listo para usar](https://www.linkedin.com/pulse/composite-models-tabular-editor-daniel-otykier/) que:

1. Importa temporalmente copias completas de tablas del modelo remoto.
2. Le permite copiar columnas (y otros metadatos) en tablas existentes.
3. Elimina las tablas temporales cuando finaliza la copia.

Este enfoque es más rápido cuando varias tablas necesitan actualizaciones.

### 3. Macro de un solo clic para incorporar medidas nuevas

El repositorio de GitHub de [rem-bou](https://github.com/rem-bou) incluye una macro avanzada que analiza el Dataset de origen en busca de medidas que **faltan** en el modelo compuesto y las agrega automáticamente: [Create-Update DQ over AS model connection](https://github.com/rem-bou/TabularEditor-Scripts/blob/main/Advanced/One-Click%20Macros/Create-Update%20DQ%20over%20AS%20model%20connection.csx)
