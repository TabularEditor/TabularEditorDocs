---
uid: change-compatibility-mode
title: Cambiar el modo de compatibilidad
author: Morten Lønskov
updated: 2026-04-08
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

# Cambiar el modo de compatibilidad

El **modo de compatibilidad** de un modelo indica a qué plataforma se dirige. Esta propiedad determina:

- Qué objetos y propiedades del Tabular Object Model (TOM) están disponibles
- Qué restricciones según la edición aplica Tabular Editor

El modo de compatibilidad es independiente del [nivel de compatibilidad](xref:update-compatibility-level), que habilita o bloquea características en función de los números de versión.

## Valores del modo de compatibilidad

La propiedad `Database.CompatibilityMode` acepta los siguientes valores, definidos por la enumeración [Microsoft.AnalysisServices.CompatibilityMode](https://learn.microsoft.com/dotnet/api/microsoft.analysisservices.compatibilitymode?view=analysisservices-dotnet):

| Valor              | Significado                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Unknown`          | Sin modo específico. Valor predeterminado cuando el modo no se ha configurado explícitamente. La biblioteca cliente de AS detecta automáticamente el modo real en función de las características de TOM que se utilicen (por ejemplo, si hay alguna característica específica de Power BI).                                                                                                                                                                 |
| `AnalysisServices` | El modelo está destinado a SQL Server Analysis Services o Azure Analysis Services.                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `PowerBI`          | El modelo está destinado a Power BI (Desktop, Premium Per User, Premium Capacity, Fabric). Algunas propiedades de TOM solo están disponibles en este modo. Consulta la sección Remarks de cada propiedad en la [referencia del espacio de nombres Microsoft.AnalysisServices.Tabular](https://learn.microsoft.com/dotnet/api/microsoft.analysisservices.tabular?view=analysisservices-dotnet) para obtener más información. |
| `Excel`            | El modelo proviene de un Data model de Power Pivot en Excel. Tabular Editor no admite modelos de Power Pivot.                                                                                                                                                                                                                                                                                                                                                                                  |

Azure Analysis Services y SQL Server Analysis Services solo admiten el modo `AnalysisServices`. Power BI y Fabric admiten los modos `AnalysisServices` y `PowerBI`.

> [!IMPORTANT]
> Tabular Editor usa el modo de compatibilidad para determinar las restricciones de edición. Un modelo configurado en modo `AnalysisServices` activa restricciones exclusivas de la edición Enterprise para características como las perspectivas y varias particiones, aunque se implemente en Power BI.

## Cuándo cambiar el modo de compatibilidad

Cambia el modo de compatibilidad a `PowerBI` cuando se cumplan todas estas condiciones:

- El modelo se implementa en Power BI (Premium Per User, Premium Capacity o Fabric)
- El modelo **no** se implementará en SSAS ni en Azure Analysis Services
- El archivo `.bim` se creó originalmente en Visual Studio, SSDT u otra herramienta cuyo modo predeterminado es `AnalysisServices`
- Aparece un error de edición sobre características del nivel Enterprise (como las perspectivas) que deberían estar disponibles en tu edición para modelos de Power BI

## Cambiar el modo de compatibilidad

1. Abre tu modelo en Tabular Editor.
2. En el **Explorador TOM**, selecciona el nodo **Model** de nivel superior.
3. En el panel de **Propiedades**, expande la sección **Base de datos**.
4. Localiza `CompatibilityMode`.
5. Cambia el valor de `AnalysisServices` a `PowerBI`.
6. Guarda el modelo (**Ctrl+S**).

![Cambiar el modo de compatibilidad](~/content/assets/images/how-to/change-compatibility-mode.png)

> [!NOTE]
> Cambiar el modo de compatibilidad afecta a qué propiedades de TOM están disponibles y a cómo se valida el modelo. Comprueba que el destino de implementación coincida con el modo seleccionado antes de guardar.

