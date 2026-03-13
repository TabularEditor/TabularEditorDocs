---
uid: advanced-refresh
title: Cuadro de diálogo de actualización avanzada
author: Daniel Otykier
updated: 2026-01-15
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.25.0
      editions:
        - edition: Escritorio
          none: true
        - edition: Empresarial
          full: true
        - edition: Enterprise
          full: true
---

# Cuadro de diálogo de actualización avanzada

El cuadro de diálogo **Actualización avanzada** ofrece un control detallado sobre las operaciones de actualización de datos, lo que te permite configurar el tipo de actualización, el grado de paralelismo, la configuración de actualización incremental y los perfiles de sobrescritura. Esto resulta útil cuando necesitas más control del que ofrecen las opciones estándar del menú de actualización.

Para abrir el cuadro de diálogo **Actualización avanzada**, ve a **Modelo > Actualizar modelo > Avanzado...** o usa el atajo de teclado **Ctrl+Shift+F5**.

> [!Note]
> El cuadro de diálogo de Actualización avanzada está disponible en la Edición Business y en la Edición Enterprise.

![Menú de actualización avanzada](~/content/assets/images/advanced-refresh-menu.png)

## Ámbito de actualización

El ámbito de actualización indica qué objetos se actualizarán. El ámbito depende de lo que esté seleccionado en el Explorador TOM cuando abres el cuadro de diálogo:

- **Modelo completo**: Cuando no hay ninguna tabla o partición específica seleccionada
- **Tablas seleccionadas**: Cuando se seleccionan una o varias tablas
- **Particiones seleccionadas**: Cuando se seleccionan una o varias particiones

## Configuración general

![Cuadro de diálogo de actualización avanzada](~/content/assets/images/advanced-refresh.png)

### Tipo de actualización

El menú desplegable **Tipo de actualización** permite elegir el tipo de operación de actualización que se va a realizar. Las opciones disponibles dependen del ámbito de actualización:

| Tipo de actualización | Descripción                                                                                                                  | Disponibilidad                        |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| **Automático**        | Permite que Analysis Services determine el tipo de actualización óptimo en función del estado actual de los objetos          | Todos los ámbitos                     |
| **Completo**          | Descarta todos los datos y los vuelve a cargar desde el origen de datos y, después, recalcula todos los objetos dependientes | Todos los ámbitos                     |
| **Limpiar**           | Descarta todos los datos de los objetos seleccionados sin recargar                                                           | Todos los ámbitos                     |
| **DataOnly**          | Carga datos desde el origen de datos sin recalcular los objetos dependientes                                                 | Todos los ámbitos                     |
| **Calcular**          | Recalcula los objetos seleccionados y todos sus dependientes sin recargar los datos                                          | Todos los ámbitos                     |
| **Defrag**            | Desfragmenta los diccionarios de todas las columnas del ámbito                                                               | Solo en los ámbitos de modelo y tabla |
| **Agregar**           | Añade nuevos datos a las particiones sin procesar los datos existentes                                                       | Ámbito de partición solamente         |

### Paralelismo máximo

La configuración de **Paralelismo máximo** controla cuántos objetos se pueden procesar simultáneamente durante la operación de actualización. Un valor de **0** significa paralelismo ilimitado, lo que permite a Analysis Services procesar en paralelo tantos objetos como permitan los recursos. Establezca un valor específico para limitar las operaciones en paralelo, lo que puede ser útil cuando se quiere reducir el consumo de recursos en el servidor.

## Configuración de actualización incremental

![Configuración de actualización incremental](~/content/assets/images/advanced-refresh-incremental-effective-date.png)

La sección **Configuración de actualización incremental** aparece cuando el ámbito de actualización incluye al menos una tabla con una [política de actualización incremental](xref:incremental-refresh-about) configurada. Esta sección no está disponible en el ámbito de partición.

- **Aplicar política de actualización**: Si está activado, la operación de actualización respetará la política de actualización incremental definida en la tabla(s), creando y administrando particiones según la configuración de la ventana deslizante de la política.
- **Fecha efectiva**: Especifica la fecha que se usará al evaluar la política de actualización incremental. De forma predeterminada, es la fecha actual, pero se puede seleccionar una fecha diferente para simular cómo se comportaría la actualización en otro momento. Esto es útil para probar configuraciones de actualización incremental.

## Configuración de anulaciones de actualización

Las anulaciones de actualización permiten modificar temporalmente determinadas propiedades durante una operación de actualización sin cambiar los metadatos reales del modelo. Esto elimina el riesgo de dejar accidentalmente modificaciones temporales en el modelo.

### Casos de uso de las anulaciones de actualización

- **Limitar datos durante el desarrollo**: Anular las consultas de partición para cargar solo un subconjunto de filas (p. ej., usando cláusulas TOP o WHERE), lo que acelera las operaciones de actualización durante el desarrollo y las pruebas
- **Actualizar desde orígenes alternativos**: Cargar datos desde una base de datos de prueba o de desarrollo en lugar del origen de producción configurado en el modelo
- **Probar con expresiones modificadas**: Anular expresiones compartidas (parámetros M) para probar distintas configuraciones

### Perfiles de anulación

Los perfiles de anulación almacenan configuraciones con nombre de anulaciones de TMSL que se pueden reutilizar en distintas operaciones de actualización.

![Editor de perfiles de anulación](~/content/assets/images/advanced-refresh-edit-profile.png)

- **Nuevo...**: Crea un nuevo perfil de anulación. Proporciona un nombre de perfil y la definición de TMSL que especifica las anulaciones.
- **Editar...**: Modifica el perfil de sustitución seleccionado.
- **Eliminar**: Elimina el perfil de sustitución seleccionado.

La definición de TMSL sigue la [especificación del comando de actualización de TMSL](https://learn.microsoft.com/en-us/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions), lo que permite sobrescribir propiedades en:

- Fuentes de datos
- Expresiones compartidas
- Particiones
- Columnas de datos

> [!TIP]
> Consulte [Perfiles de sustitución de actualización](xref:refresh-overrides) para ver ejemplos detallados y fragmentos de código TMSL que puede usar como punto de partida para sus propios perfiles de sustitución.

### Almacenamiento de perfiles

Los perfiles de anulación se almacenan por modelo en el archivo `UserOptions.tmuo`. Al trabajar con metadatos del modelo guardados en disco, el archivo `.tmuo` se guarda junto con los archivos del modelo. Cuando se conecta directamente a un modelo mediante el punto de conexión XMLA, los archivos `.tmuo` se almacenan en `%LocalAppData%\TabularEditor3\UserOptions`.

## Exportar script TMSL

El botón **Exportar script TMSL...** abre un cuadro de diálogo en el que puede ver y copiar el comando de actualización TMSL generado. Esto resulta útil cuando desea:

- Ejecutar el comando de actualización con otras herramientas (como SQL Server Management Studio)
- Incluir el comando de actualización en scripts de automatización o canalizaciones de CI/CD
- Revisar el TMSL exacto que se enviará a Analysis Services