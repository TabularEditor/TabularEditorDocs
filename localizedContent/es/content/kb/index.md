# Base de conocimientos

Esta sección contiene artículos sobre prácticas recomendadas, reglas de análisis de código y patrones de optimización de DAX para Tabular Editor y modelos de Power BI.

## En esta sección

### Reglas de prácticas recomendadas (BPA)

Directrices completas para crear modelos de Power BI y Analysis Services de alta calidad y fáciles de mantener.

- @kb.bpa-avoid-invalid-characters-descriptions - Evita la corrupción de metadatos eliminando caracteres de control de las descripciones
- @kb.bpa-avoid-invalid-characters-names - Asegura que los nombres de los objetos contengan solo caracteres válidos
- @kb.bpa-data-column-source - Verifica que todas las columnas de datos tengan asignaciones de origen correctas
- @kb.bpa-relationship-same-datatype - Impone la coherencia de los tipos de datos en las relaciones
- @kb.bpa-visible-objects-no-description - Asegura que todos los objetos visibles tengan descripciones significativas
- @kb.bpa-trim-object-names - Elimina los espacios al principio y al final de los nombres
- @kb.bpa-expression-required - Valida que los objetos calculados tengan expresiones
- @kb.bpa-format-string-columns - Aplica un formato coherente a las columnas numéricas y de fecha
- @kb.bpa-format-string-measures - Proporciona cadenas de formato para todas las medidas
- @kb.bpa-do-not-summarize-numeric - Evita la agregación inadecuada de columnas numéricas
- @kb.bpa-date-table-exists - Asegura una configuración correcta de la tabla de fechas
- @kb.bpa-hide-foreign-keys - Oculta las columnas de clave externa a los usuarios finales
- @kb.bpa-many-to-many-single-direction - Aplica el filtrado en una sola dirección en relaciones de muchos a muchos
- @kb.bpa-avoid-provider-partitions-structured - Usa orígenes de partición adecuados para datos estructurados
- @kb.bpa-translate-descriptions - Ofrece compatibilidad con descripciones en varios idiomas
- @kb.bpa-translate-display-folders - Localiza los nombres de las carpetas de visualización
- @kb.bpa-translate-hierarchy-levels - Traduce las etiquetas de los niveles de jerarquía
- @kb.bpa-translate-perspectives - Localiza los nombres de las perspectivas
- @kb.bpa-translate-visible-names - Traduce los nombres de los objetos visibles para todas las configuraciones regionales
- @kb.bpa-perspectives-no-objects - Asegura que las perspectivas contengan objetos relevantes
- @kb.bpa-calculation-groups-no-items - Validar las definiciones de los grupos de cálculo
- @kb.bpa-set-isavailableinmdx-false - Controlar la disponibilidad de los objetos en MDX
- @kb.bpa-set-isavailableinmdx-true-necessary - Habilitar la disponibilidad en MDX cuando sea necesario
- @kb.bpa-remove-auto-date-table - Limpiar las tablas de fechas generadas automáticamente
- @kb.bpa-remove-unused-data-sources - Eliminar definiciones de Data source no utilizadas
- @kb.bpa-specify-application-name - Establecer nombres de aplicación en las cadenas de conexión para la supervisión
- @kb.bpa-powerbi-latest-compatibility - Mantener la compatibilidad con las últimas funcionalidades de Power BI
- @kb.bpa-udf-use-compound-names - Ensure UDF names don't conflict with future built-in DAX functions

## Acciones de código

### Análisis de código DAX (DI)

Sugerencias de mejora para la estructura y la eficiencia del código DAX. Estas reglas identifican oportunidades para simplificar y optimizar sus expresiones.

- @DI001 - Eliminar variable no utilizada
- @DI002 - Eliminar variable no utilizada
- @DI003 - Eliminar el nombre de la tabla
- @DI004 - Agregar el nombre de la tabla
- @DI005 - Reescribir el filtro de tabla FILTER como predicado escalar
- @DI006 - Dividir el filtro FILTER de varias columnas en varios filtros
- @DI007 - Simplificar la instrucción SWITCH
- @DI008 - Eliminar CALCULATE superfluo
- @DI009 - Evitar la sintaxis abreviada de CALCULATE
- @DI010 - Usar MIN/MAX en lugar de IF
- @DI011 - Usar ISEMPTY en lugar de COUNTROWS
- @DI012 - Usar DIVIDE en lugar de la división
- @DI013 - Usar la división en lugar de DIVIDE
- @DI014 - Reemplazar IFERROR por DIVIDE
- @DI015 - Sustituir IF por DIVIDE

### Refactorización de DAX (DR)

Sugerencias de refactorización para patrones de DAX complejos o ineficientes. Estas reglas ayudan a modernizar y mejorar la legibilidad de tu código DAX.

- @DR001 - Convertir en predicado escalar
- @DR002 - Usar un agregador en lugar de un iterador
- @DR003 - Usar VALUES en lugar de SUMMARIZE
- @DR004 - Añadir un prefijo a la variable
- @DR005 - Añadir un prefijo a la columna temporal
- @DR006 - Mover la agregación constante a una variable
- @DR007 - Simplificar un bloque de 1 variable
- @DR008 - Simplificar un bloque de varias variables
- @DR009 - Reescribir usando DISTINCTCOUNT
- @DR010 - Reescribir usando COALESCE
- @DR011 - Reescribir usando ISBLANK
- @DR012 - Eliminar BLANK innecesario
- @DR013 - Simplificar la lógica negada
- @DR014 - Simplificar usando IN

### Reescrituras de DAX (RW)

Reescrituras sugeridas para patrones de DAX específicos que pueden expresarse de forma más eficaz con sintaxis alternativa.

- @RW001 - Reescribir TOTALxTD usando CALCULATE
- @RW002 - Reescribir usando FILTER
- @RW003 - Invertir la expresión IF

---
