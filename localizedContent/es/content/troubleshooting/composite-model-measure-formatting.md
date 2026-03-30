---
uid: composite-model-measure-formatting
title: Propiedades de formato de medidas en modelos compuestos
author: Equipo de soporte
updated: 2026-01-26
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

# Propiedades de formato de medidas en modelos compuestos

Al trabajar con modelos compuestos que usan una conexión en vivo a Analysis Services (SSAS/AAS), es posible que te encuentres con errores de validación o comportamientos confusos al editar las propiedades de formato de una medida. Un mensaje de error habitual es:

**"Una medida no puede tener a la vez FormatString y Format Expression."**

En este artículo se explica por qué ocurre y cómo resolverlo.

---

## Comprender el problema

Los modelos compuestos combinan tablas locales de Power BI con tablas remotas de un modelo semántico de SSAS/AAS mediante una conexión en vivo. En esta arquitectura, el formato de las medidas puede ser ambiguo:

- **FormatString**: Una definición de formato estática (p. ej., "0.00" o "0,00" para moneda).
- **Format String Expression**: Una expresión de cadena de formato dinámica que se evalúa en el momento de la consulta.

El error se produce porque el modelo acaba teniendo a la vez un formato estático y una expresión de formato dinámica, un estado que el Tabular Object Model (TOM) no permite.

### Por qué sucede

En los modelos compuestos:

1. **Ambigüedad de propiedad**: las medidas remotas pertenecen al modelo SSAS/AAS remoto. Cuando editas el formato en Tabular Editor, puede que estés intentando sobrescribir los metadatos remotos, lo que genera conflictos.

2. **Sincronización de metadatos**: cuando una medida tiene una expresión de cadena de formato dinámica, FormatString suele mostrarse como "Custom" para indicar que el formato dinámico está activo. Si después intentas establecer un FormatString estático a la vez, ambas propiedades se rellenan y se desencadena el error de validación.

3. **Limitaciones de persistencia**: los cambios en los metadatos de las medidas remotas pueden no persistir correctamente porque el modelo remoto conserva el control definitivo. Esto deja el modelo compuesto local en un estado inconsistente.

---

## Causas raíz

### Formato de medidas remotas

Si la medida problemática está definida en el modelo SSAS/AAS remoto:

- El formato debe gestionarse en el modelo de origen, no en el modelo compuesto de Power BI.
- Intentar reemplazar el formato de una medida remota en Power BI puede hacer que se rellenen tanto FormatString como la expresión de cadena de formato dinámica, lo que provoca el error de validación.

### Script o automatización que establece ambas propiedades

- Si utilizas C# Script, transformaciones de Power Query o reglas de BPA para aplicar formato, asegúrate de que, por cada medida, solo se use un enfoque (estático o dinámico, pero no ambos).

### Grupos de cálculo con expresiones de formato

- Los grupos de cálculo pueden definir expresiones de cadena de formato dinámicas que sobrescriben los formatos de las medidas. Si la expresión de formato de un elemento de cálculo está activa, la IU puede seguir mostrando el FormatString estático de la medida, dando la impresión de que ambos están establecidos.

### Limitaciones de versión o entorno

- Los formatos dinámicos para medidas están disponibles de forma limitada y es posible que no sean totalmente compatibles con determinadas versiones de Power BI o modos de implementación (Report Server).
- Si usas una versión de Power BI Desktop anterior a 2025 o una versión de Power BI Report Server anterior a enero de 2025, es posible que no se admitan los formatos dinámicos de las medidas.

---

## Solución

La solución depende de si la medida es **remota** (de SSAS/AAS) o **local** (creada en el modelo compuesto).

### Si la medida es remota (de SSAS/AAS)

Este es el escenario más común. Las medidas remotas pertenecen al modelo semántico de origen.

**Enfoque recomendado:**

1. **Gestiona el formato en el modelo de origen.** Abre SSAS/AAS en SQL Server Management Studio o en Tabular Editor conectado al modelo de origen y configura el formato allí.

2. **Si se requiere un formato específico del Report,** crea una medida "wrapper" local en tu modelo compuesto de Power BI:

   - Define una nueva medida en el modelo local que haga referencia a la medida remota.
   - Aplica la cadena de formato deseada a la medida "wrapper".
   - Usa la medida "wrapper" en tu Report en lugar de la medida remota.

   **Inconveniente:** Este enfoque crea duplicados y aumenta el esfuerzo de mantenimiento, pero es la forma más fiable de aplicar un formato específico del Report en un escenario de conexión en vivo.

### Si la medida es local (creada en el modelo compuesto)

**Para formato estático (lo más habitual):**

1. Selecciona la medida en Tabular Editor.
2. Vacía el campo **Expresión de cadena de formato dinámica** (déjalo en blanco o en null).
3. Establece el **Format String** de la medida en el formato estático deseado (p. ej., `"0.00%"` para porcentaje, `"$#,##0.00"` para moneda).
4. Guarda el modelo.

**Para formato dinámico:**

1. Selecciona la medida.
2. Mantén o establece la **expresión de cadena de formato dinámica** en la expresión DAX que quieras (es la única propiedad de formato que deberías usar).
3. Deja el **Format String** como "Custom" (no intentes establecer también una cadena de formato estática).
4. Comprueba que tu entorno admite cadenas de formato dinámicas (Power BI Desktop 2025 o posterior, o Power BI Report Server de enero de 2025 o posterior).

---

## Lista rápida de comprobación para solucionar problemas

- [ ] **Determina la propiedad de la medida**: ¿La medida es remota (SSAS/AAS) o local (modelo compuesto)?
- [ ] **Comprueba la expresión de cadena de formato dinámica**: Aunque no la hayas configurado, verifica si está rellenada. En la cuadrícula de propiedades, busca un campo "Expresión de cadena de formato dinámica" que no esté vacío.
- [ ] **Revisa scripts y reglas**: Si usas C# Scripts o reglas BPA para establecer formatos de medidas, asegúrate de que no establezcan FormatString y la expresión de cadena de formato dinámica a la vez en la misma ejecución.
- [ ] **Comprueba los grupos de cálculo**: Confirma si algún elemento de un grupo de cálculo define un campo "Expresión de cadena de formato dinámica" que pueda estar reemplazando o entrando en conflicto con el formato de la medida.
- [ ] **Verifica la versión del entorno**: Confirma la versión de Power BI Desktop (2025 o posterior) o de Power BI Report Server (enero de 2025 o posterior), especialmente si usas formatos dinámicos.

---

## Ejemplos paso a paso

### Ejemplo 1: Corregir una medida remota con formato estático

**Escenario:** Tienes una medida "Sales Amount" en el modelo SSAS remoto y quieres darle formato de moneda en tu Report de Power BI.

**Pasos:**

1. En Tabular Editor, conéctate directamente al modelo SSAS/AAS (no al modelo compuesto de Power BI).
2. Ve a la medida "Sales Amount".
3. Establece su **Format String** en `"$#,##0.00"`.
4. Vuelve a guardar el modelo en SSAS/AAS.
5. Vuelve a Tabular Editor con conexión al modelo compuesto de Power BI; ahora el formato debería heredarse.

Si el formato sigue sin verse correcto en el Report, crea una medida envolvente local (consulta más abajo).

### Ejemplo 2: Crear una medida envolvente para un formato específico del Report

**Escenario:** Necesitas que la medida Sales Amount de SSAS tenga un formato diferente en este Report específico.

**Pasos:**

1. En Tabular Editor, conéctate al modelo compuesto de Power BI.
2. Crea una nueva medida en una tabla local (o en la tabla de medidas, si tienes una):
   ```
   Sales Amount (Formatted) = [Sales Amount]
   ```
3. Establece la **Cadena de formato** de la nueva medida en el formato que desees (p. ej., `\"$#,##0.00\"`).
4. Guarda el modelo.
5. Actualiza los Visuales del Report para usar la medida envolvente en lugar de la medida remota original.

### Ejemplo 3: Configurar una medida local con formato dinámico

**Escenario:** Tienes una medida local en el modelo compuesto y quieres aplicar formato condicional en función de un umbral.

**Pasos:**

1. Selecciona la medida en Tabular Editor.
2. Asegúrate de que **Cadena de formato** esté vacía (no establezcas un formato estático).
3. Establece **Expresión de cadena de formato dinámica** en tu expresión condicional:
   ```dax
   IF(
       [YourMeasure] > 1000,
       "#,##0.00",
       "0.00"
   )
   ```
4. No establezcas tampoco un FormatString estático.
5. Guarda el modelo.
6. Comprueba que tu versión de Power BI admite cadenas de formato dinámicas (Desktop 2025+ o PBIRS enero de 2025+).

---

## Buenas prácticas de prevención

1. **Define la estrategia de formato cuanto antes**: Decide si cada medida debe usar formato estático o dinámico y mantén un único enfoque por medida.

2. **Audita las medidas remotas**: Antes de editar el formato en un modelo compuesto, comprueba si la medida es remota. Si es así, gestiona el formato en el modelo SSAS/AAS de origen.

3. **Usa funciones compatibles con tu versión**: Si usas cadenas de formato dinámicas, asegúrate de que todos los entornos relevantes (Desktop, Report Server, Analysis Services) las admiten en tu versión de Power BI.

4. **Escribe scripts de forma defensiva**: Si escribes C# Scripts o reglas de BPA para dar formato a medidas, separa la lógica para que solo establezcas una propiedad de formato por medida e incluye una validación para comprobar si la otra propiedad ya está establecida.

5. **Borra la expresión de cadena de formato dinámica al pasar a formato estático**: Si una medida usaba antes formato dinámico, borra siempre la expresión de cadena de formato dinámica antes de intentar establecer un FormatString estático.

---

## Recursos adicionales

- **[Microsoft Docs - Cadenas de formato de medidas](https://learn.microsoft.com/en-us/analysis-services/tmsl/measures-object-tmsl)**: Documentación oficial sobre el formato de medidas en el Tabular Object Model.
- **[Modelos compuestos en Power BI](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-composite-models)**: Cómo funcionan las conexiones en vivo y la arquitectura de modelos compuestos.
- **[Cadenas de formato dinámicas](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-dynamic-format-strings)**: Disponibilidad de la funcionalidad y guía de uso.

---

## ¿Aún necesitas ayuda?

Si los pasos anteriores no resuelven tu problema:

1. **Verifica que la medida es local**: Conéctate directamente a tu archivo de Power BI (.pbix) en Tabular Editor para confirmar que la medida está definida localmente, no de forma remota.

2. **Exporta información de diagnóstico**: Ejecuta el siguiente script de Tabular Editor para auditar todas las medidas:
   ```csharp
   var measures = Model.AllMeasures;
   foreach (var m in measures)
   {
       var hasStaticFormat = !string.IsNullOrEmpty(m.FormatString);
       var hasDynamicFormat = !string.IsNullOrEmpty(m.FormatStringExpression);
       if (hasStaticFormat && hasDynamicFormat)
       {
           Output($"CONFLICT - {m.Name}: FormatString='{m.FormatString}', Expression='{m.FormatStringExpression}'");
       }
       else if (hasStaticFormat)
       {
           Output($"STATIC - {m.Name}: '{m.FormatString}'");
       }
       else if (hasDynamicFormat)
       {
           Output($"DYNAMIC - {m.Name}: '{m.FormatStringExpression}'");
       }
   }
   ```

3. **Contacta con el soporte técnico**: Ponte en contacto y comparte la salida de diagnóstico, así como los números de versión de Power BI y Tabular Editor.
