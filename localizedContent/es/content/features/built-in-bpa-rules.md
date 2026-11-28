---
uid: built-in-bpa-rules
title: Reglas BPA integradas
author: Morten Lønskov
updated: 2026-11-13
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.24.0
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
description: "36 reglas de mejores prácticas seleccionadas e integradas en el código de Tabular Editor 3, con integración de la base de conocimientos."
---

# Reglas BPA integradas

## Resumen

Tabular Editor 3 incluye 36 reglas de buenas prácticas integradas. Estas reglas abarcan problemas comunes en el desarrollo de modelos semánticos y se actualizan automáticamente con cada versión.

A diferencia de las reglas personalizadas almacenadas en archivos JSON, las reglas integradas:

- Están integradas directamente en la aplicación
- Se actualizan automáticamente con las nuevas versiones
- Vinculan a la documentación de la base de conocimiento
- Son de solo lectura para garantizar la coherencia entre equipos
- Funcionan al instante sin configuración

## Características principales

### Categorías de reglas

El **Best Practice Analyzer** agrupa las reglas integradas por categorías:
- **Prevención de errores**: caracteres no válidos, expresiones y columnas de origen faltantes, discrepancias en los tipos de datos, disponibilidad de MDX, nombres de funciones definidas por el usuario
- **Rendimiento**: disponibilidad de MDX, tablas de fechas, relaciones «muchos a muchos», nombres de aplicaciones de cadenas de conexión
- **Mantenimiento**: descripciones, grupos de cálculos y perspectivas vacíos, orígenes de datos no utilizados
- **Convenciones de nomenclatura**: espacios iniciales y finales en los nombres
- **Formato**: cadenas de formato, resumen de columnas numéricas, visibilidad de claves externas
- **Diseño del modelo**: traducciones
- **Gobernanza**: nivel de compatibilidad de Power BI
- **Seguridad**: permisos de roles y combinaciones de seguridad a nivel de fila y a nivel de objeto

### Control global y por regla
![Cuadro de diálogo «Administrar reglas de buenas prácticas» con la colección de buenas prácticas integradas seleccionada y sus reglas agrupadas por categoría, cada una con una casilla de verificación](~/content/assets/images/features/bpa-built-in-rules-preferences.png)
Puedes habilitar o deshabilitar las reglas integradas de forma global o individual. Los ajustes se mantienen entre sesiones y funcionan independientemente de sus reglas personalizadas.

Para administrar las reglas integradas:
1. Vaya a **Herramientas > Preferencias > Tabular Editor > Varios**.
2. En **Best Practice Analyzer**, seleccione o desmarque **Habilitar reglas de buenas prácticas integradas** para activar o desactivar toda la colección.
3. Para habilitar o deshabilitar reglas individuales, abra **Herramientas > Administrar reglas BPA...**, seleccione la colección **Prácticas recomendadas integradas** y marque o desmarque la casilla de verificación de cada regla.

### Notificación al iniciar por primera vez

![Captura de pantalla del cuadro de diálogo de notificación al iniciar por primera vez, que presenta las reglas BPA integradas](~/content/assets/images/features/bpa-built-in-rules-notification.png)

La primera vez que abras un modelo después de actualizar a una versión con reglas integradas, verás una notificación que explica la característica e incluye un enlace a las preferencias. Esta notificación solo aparece una vez.

### Integración con la base de conocimientos


![Ventana de Best Practice Analyzer con la información sobre herramientas de una regla abierta y el enlace «Más información» resaltado](~/content/assets/images/features/bpa-built-in-rules-kb-link.png)

Cada regla integrada enlaza con un artículo de la base de conocimientos. Cada artículo explica qué comprueba la regla, por qué es importante y cómo corregir las infracciones.

Para abrir el artículo, coloca el cursor sobre una regla en la ventana **Best Practice Analyzer** y haz clic en **Más información** en la información sobre herramientas.

### Protección de solo lectura

Las reglas integradas no se pueden editar, clonar ni eliminar. Esto garantiza que todos los usuarios tengan las mismas definiciones de reglas. Puedes desactivar reglas individuales, pero las definiciones de las reglas en sí permanecen sin cambios.

![Captura de pantalla que muestra una regla integrada con una insignia o un icono de solo lectura en la ventana de BPA](~/content/assets/images/features/bpa-built-in-rules-readonly.png)

### Prevención de colisiones de ID

Las reglas integradas usan prefijos de ID reservados. Cuando creas una regla personalizada, Tabular Editor valida que tu ID no entre en conflicto con las reglas integradas y muestra un error si lo hace.

## Catálogo de reglas integradas

Cada entrada enlaza con el artículo de la base de conocimientos de la regla. La gravedad se muestra entre paréntesis.

### Reglas de prevención de errores
- [La columna de datos debe tener un origen](xref:kb.bpa-data-column-source) (3)
- [Se requiere una expresión para los objetos calculados](xref:kb.bpa-expression-required) (3)
- [Evitar las particiones de proveedores con orígenes de datos estructurados](xref:kb.bpa-avoid-provider-partitions-structured) (2)
- [Las columnas de relación deben tener el mismo tipo de datos](xref:kb.bpa-relationship-same-datatype) (3)
- [Evitar caracteres no válidos en los nombres de los objetos](xref:kb.bpa-avoid-invalid-characters-names) (3)
- [Evitar caracteres no válidos en las descripciones](xref:kb.bpa-avoid-invalid-characters-descriptions) (3)
- [Establecer IsAvailableInMDX en True cuando sea necesario](xref:kb.bpa-set-isavailableinmdx-true-necessary) (3)
- [Usar nombres compuestos para las funciones definidas por el usuario](xref:kb.bpa-udf-use-compound-names) (1)

### Reglas de rendimiento
- [Establecer IsAvailableInMDX en False](xref:kb.bpa-set-isavailableinmdx-false) (3)
- [Debe existir una tabla de fechas](xref:kb.bpa-date-table-exists) (2)
- [Eliminar tablas de fechas automáticas](xref:kb.bpa-remove-auto-date-table) (2)
- [Las relaciones «muchos a muchos» deben usar una sola dirección](xref:kb.bpa-many-to-many-single-direction) (2)
- [Especificar nombre de aplicación en las cadenas de conexión](xref:kb.bpa-specify-application-name) (1)

### Reglas de mantenimiento
- [Eliminar fuentes de datos no utilizadas](xref:kb.bpa-remove-unused-data-sources) (1)
- [Los objetos visibles deben tener descripciones](xref:kb.bpa-visible-objects-no-description) (1): cinco reglas, para tablas, columnas, medidas, grupos de cálculo y funciones definidas por el usuario
- [Las perspectivas deben contener objetos](xref:kb.bpa-perspectives-no-objects) (1)
- [Los grupos de cálculo deben contener elementos](xref:kb.bpa-calculation-groups-no-items) (2)

### Reglas de las convenciones de nomenclatura
- [Eliminar espacios de los nombres de los objetos](xref:kb.bpa-trim-object-names) (1)

### Reglas de formato
- [Establecer SummarizeBy en «Ninguno» para las columnas numéricas](xref:kb.bpa-do-not-summarize-numeric) (3)
- [Ocultar columnas de claves externas](xref:kb.bpa-hide-foreign-keys) (2)
- [Proporcionar una cadena de formato para las columnas numéricas y de fecha](xref:kb.bpa-format-string-columns) (2)
- [Proporcionar una cadena de formato para las medidas](xref:kb.bpa-format-string-measures) (2)

### Reglas de diseño del modelo
- [Traducir carpetas de visualización para todas las culturas](xref:kb.bpa-translate-display-folders) (1)
- [Traducir descripciones para todas las culturas](xref:kb.bpa-translate-descriptions) (1)
- [Traducir nombres de objetos visibles para todas las culturas](xref:kb.bpa-translate-visible-names) (1)
- [Traducir los nombres de los niveles de jerarquía para todas las culturas](xref:kb.bpa-translate-hierarchy-levels) (1)
- [Traducir los nombres de las perspectivas para todas las culturas](xref:kb.bpa-translate-perspectives) (1)

### Reglas de gobernanza
- [Usar el nivel de compatibilidad más reciente para los modelos de Power BI](xref:kb.bpa-powerbi-latest-compatibility) (3)

### Reglas de seguridad
- [La seguridad a nivel de fila y a nivel de objeto requiere permiso de lectura](xref:kb.bpa-role-security-not-enforced) (3)
- [Los roles de Power BI deben tener permiso de lectura](xref:kb.bpa-powerbi-role-read-permission) (3)
- [Los roles sin seguridad anulan los roles protegidos](xref:kb.bpa-role-unrestricted-read) (2)
- [Evitar miembros tanto en un rol RLS como en un rol OLS](xref:kb.bpa-role-mixed-rls-ols-members) (3)

Las reglas de seguridad no tienen corrección automática.

## Trabajar con reglas integradas y personalizadas

Las reglas integradas y las personalizadas conviven:

| Característica      | Reglas integradas                       | Reglas personalizadas                       |
| ------------------- | --------------------------------------- | ------------------------------------------- |
| **Almacenamiento**  | Integrado en el código de la aplicación | Archivos JSON o anotaciones del modelo      |
| **Actualizaciones** | Automático con cada versión             | Requiere edición manual                     |
| **Modificación**    | Solo lectura                            | Totalmente editable                         |
| **Documentación**   | Artículos de KB integrados              | Descripciones proporcionadas por el usuario |
| **Compartir**       | Consistente entre equipos               | Requiere distribución manual                |

### Flujo de trabajo recomendado

1. Habilita las reglas integradas para obtener cobertura inmediata
2. Revisa las infracciones y aplica correcciones
3. Deshabilita las reglas que no se ajusten a tus convenciones
4. Añade reglas personalizadas para requisitos específicos de la organización
5. Usa la función "Ignorar" para infracciones deliberadas

## Prácticas recomendadas

### Incorporación de equipos

Al implementar las reglas integradas en tu equipo:

- Empieza con todas las reglas habilitadas para establecer una línea de referencia
- Revisen las infracciones en conjunto y acuerden qué reglas se aplican
- Documenta por qué se deshabilitan reglas específicas
- Añade reglas personalizadas para requisitos específicos de la organización

### Mantenimiento del modelo

- Ejecuta el BPA antes de confirmar los cambios en el control de versiones
- Corrige las infracciones de alta gravedad de inmediato
- Revisa periódicamente los problemas de gravedad media y baja
- Usa correcciones automáticas cuando estén disponibles

### Reglas personalizadas

- No dupliques la funcionalidad de las reglas integradas
- Usa prefijos de ID distintos para evitar conflictos
- Documenta tus reglas personalizadas
- Comparte colecciones de reglas con tu equipo

## Solución de problemas

### Las reglas integradas no aparecen

Si las reglas integradas no se muestran en la ventana del BPA:
1. Compruebe que la opción **Habilitar reglas de mejores prácticas integradas** esté seleccionada en **Herramientas > Preferencias > Tabular Editor > Varios**.
2. Reinicia Tabular Editor si acabas de cambiar las preferencias
3. Confirma que tu licencia está activa

### No se puede modificar una regla integrada

Es lo esperado. Las reglas integradas son de solo lectura. Si necesitas una lógica distinta, crea una regla personalizada con tu expresión y desactiva la regla integrada correspondiente.

### Error de colisión de ID

Las reglas integradas reservan ciertos prefijos de ID. Elige un ID diferente que no empiece por `TE3_BUILT_IN`.

## Compatibilidad

Las reglas integradas se aplican a los modelos con un nivel de compatibilidad de 1200 o superior. Algunas reglas requieren un nivel superior: la regla para los miembros tanto de un rol de seguridad a nivel de filas como de un rol de seguridad a nivel de objetos requiere 1400, y las dos reglas para las funciones definidas por el usuario requieren 1702. Cada artículo de la base de conocimientos indica el nivel de compatibilidad de la regla.

## Siguientes pasos

- [Uso del Best Practice Analyzer](xref:using-bpa)
- [Reglas y expresiones de ejemplo de BPA](xref:using-bpa-sample-rules-expressions)
- [Reglas BPA personalizadas](xref:best-practice-analyzer)