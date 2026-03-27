---
uid: update-compatibility-level
title: Actualizar el nivel de compatibilidad
author: Morten Lønskov
updated: 2026-01-12
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

# Actualizar el nivel de compatibilidad

El **nivel de compatibilidad** de un modelo controla qué características del Tabular Object Model (TOM) puedes usar. Cuando Microsoft introduce nuevas capacidades, como calendarios personalizados o funciones DAX definidas por el usuario, a menudo quedan disponibles solo a partir de un nivel de compatibilidad más reciente. Tendrás que actualizar antes de que estas características aparezcan en Tabular Editor.

> [!WARNING]
> Las actualizaciones de compatibilidad son unidireccionales. Puedes actualizar, pero no puedes volver atrás de forma fiable. Trátalo como una actualización de esquema y valida primero los destinos de implementación.

## Cuándo actualizar

Actualiza cuando:

- Existe una característica en Power BI Desktop, pero falta la propiedad TOM relacionada en Tabular Editor
- Necesitas capacidades introducidas recientemente, como **calendarios personalizados** (1701+) o **funciones DAX definidas por el usuario** (1702+)
- Estás estandarizando el desarrollo entre entornos y quieres conjuntos mínimos de características coherentes

## Antes de empezar

### Haz una copia de seguridad del modelo

Como las actualizaciones son irreversibles:

- Haz una copia de seguridad de los metadatos del modelo (e idealmente del proyecto completo)
- Usa control de versiones y asegúrate de tener un commit limpio antes de cambiar nada

### Confirma la compatibilidad del destino

El soporte del nivel de compatibilidad varía según la plataforma (SSAS, Azure Analysis Services, Fabric/Power BI Premium). Si tu destino de implementación no admite el nivel seleccionado, no podrás implementar. Consulta [Nivel de compatibilidad para modelos tabulares en Analysis Services](https://learn.microsoft.com/en-us/analysis-services/tabular-models/compatibility-level-for-tabular-models-in-analysis-services)

## Actualiza el nivel de compatibilidad

![Actualizar el nivel de compatibilidad](~/content/assets/images/how-to/updatecompatabilitylevel.gif)

### Abre tu modelo

Abre tu modelo en Tabular Editor con uno de estos métodos:

- Abre una definición de modelo basada en un archivo (un archivo `.bim`)
- Conéctate a un modelo en ejecución (modelo semántico de SSAS/AAS/Power BI a través del punto de conexión XMLA)

### Selecciona la raíz del modelo

En el **Explorador TOM**, selecciona el **Model** de nivel superior (nodo raíz).

### Localiza el nivel de compatibilidad

En el panel de **Propiedades**:

1. Expande **Database**
2. Busca **nivel de compatibilidad**

### Establece el nuevo nivel

Establece el nivel de compatibilidad en el mínimo necesario para tu funcionalidad (o en el máximo que admita tu plataforma).

Ejemplos:

- **Calendarios personalizados:** 1701+
- **UDFs de DAX:** 1702+

> [!NOTE]
> Los niveles mínimos necesarios para las funcionalidades pueden cambiar a medida que evoluciona la plataforma. Verifica siempre los requisitos previos en la documentación actual. Algunos niveles/funcionalidades son exclusivos de Power BI y es posible que no estén disponibles en SSAS/AAS.

### Guardar

Guarda el modelo para aplicar el cambio:

- Si estás conectado a un modelo remoto, al guardar se aplica de nuevo en el servidor el cambio en los metadatos
- Si estás editando un modelo basado en archivos, al guardar se actualizan los metadatos en el disco

Después de guardar, Tabular Editor muestra los objetos y propiedades que se acaban de habilitar.

## Elige el nivel adecuado

### Para implementaciones de SSAS/AAS

Elige el [nivel de compatibilidad más reciente compatible con la versión de tu servidor](https://learn.microsoft.com/en-us/analysis-services/tabular-models/compatibility-level-for-tabular-models-in-analysis-services)

### Para Power BI Desktop

Consulta el motor de Power BI Desktop para ver qué niveles de compatibilidad admite. Usa [DAX Studio o Vista de Consulta DAX](https://www.sqlbi.com/blog/marco/2024/03/10/compatibility-levels-and-engine-supported-by-power-bi-desktop/):

```sql
SELECT * FROM $SYSTEM.DISCOVER_PROPERTIES
WHERE [PropertyName] = 'ProviderVersion'
   OR [PropertyName] = 'DBMSVersion'
   OR [PropertyName] = 'SupportedCompatibilityLevels'
```

## Solución de problemas

### No se puede implementar en SSAS/AAS después de la actualización

Puede que hayas seleccionado un nivel de compatibilidad que no admite el servidor de destino. Valida la compatibilidad del servidor antes de actualizar.

**Referencia:** [Nivel de compatibilidad para modelos tabulares en Analysis Services](https://learn.microsoft.com/en-us/analysis-services/tabular-models/compatibility-level-for-tabular-models-in-analysis-services)

### ¿Puedo volver a una versión anterior?

No. No se admiten las bajadas de versión y no son una estrategia de corrección segura ni fiable.

## Verificación

Después de actualizar y guardar:

- Confirma que **Base de datos → Nivel de compatibilidad** refleja el nuevo valor en Tabular Editor
- Verifica que se muestran las características esperadas (p. ej., el nodo **Functions** está disponible a partir de 1702+)
- Si el destino es SSAS/AAS, valida la implementación con los niveles de compatibilidad que admite el servidor