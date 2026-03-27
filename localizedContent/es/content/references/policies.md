---
uid: policies
title: Directivas
author: Daniel Otykier
updated: 2026-03-25
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

# Directivas

Algunas organizaciones de TI pueden querer limitar ciertas funcionalidades de Tabular Editor. Esto es posible mediante el uso de directivas de grupo, estableciendo determinados valores en el Registro de Windows.

> [!NOTE]
> Esta funcionalidad requiere las siguientes versiones de Tabular Editor:
>
> - Tabular Editor 2, versión [2.17.0](https://github.com/TabularEditor/TabularEditor/releases/tag/2.17.0) o posterior
> - Tabular Editor 3, versión [3.3.5](https://github.com/TabularEditor/TabularEditor3/releases/tag/3.3.5) o posterior.

A continuación se muestra una lista de las directivas que se pueden controlar. Para aplicar una o varias de estas directivas, agregue un valor DWORD distinto de cero a la clave del registro. El nombre del valor indica qué directiva se aplicará.

**Clave del Registro:** HKEY_CURRENT_USER\Software\Policies\Kapacity\Tabular Editor\

| Valor                          | Cuando se aplica...                                                                                                                                                                                                                                                                   |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DisableUpdates                 | Tabular Editor no comprobará si hay versiones más recientes disponibles en línea. Además, los usuarios no podrán comprobar manualmente si hay nuevas actualizaciones disponibles en la herramienta.                                                                                                   |
| DisableCSharpScripts           | Tabular Editor no permitirá a los usuarios crear ni ejecutar C# Scripts.                                                                                                                                                                                                                                              |
| DisableMacros                  | Tabular Editor no permitirá a los usuarios guardar ni ejecutar macros. Además, las macros definidas en la carpeta %LocalAppData% no se cargarán ni se compilarán al iniciar la aplicación.                                                                                                            |
| DisableBpaDownload             | Tabular Editor no permitirá descargar desde la web las reglas de Best Practice Analyzer.                                                                                                                                                                                                                              |
| DisableWebDaxFormatter         | Tabular Editor deshabilitará el formateador de código DAX, que realiza una solicitud web a daxformatter.com. (TE3 seguirá permitiendo dar formato al código mediante el formateador de DAX integrado)                                                                              |
| DisableErrorReports            | **(Solo TE3)** Tabular Editor no permitirá a los usuarios enviar Reportes de error/caída al equipo de soporte de Tabular Editor 3.                                                                                                                                                                 |
| DisableTelemetry               | **(Solo TE3)** Tabular Editor no recopilará ni enviará datos de uso anónimos al equipo de soporte de Tabular Editor 3.                                                                                                                                                                             |
| DisableDaxOptimizer            | **(Solo TE3)** La función de integración del Optimizador de DAX no estará disponible                                                                                                                                                                                                                               |
| DisableDaxOptimizerUpload      | **(Solo TE3)** No se permitirá a los usuarios cargar archivos VPAX mediante la función de integración del Optimizador de DAX. Se aplica implícitamente cuando se aplica `DisableDaxOptimizer`.                                                                                     |
| RequireDaxOptimizerObfuscation | **(Solo TE3)** No se permitirá a los usuarios cargar archivos VPAX sin ofuscar (en texto sin formato) mediante la función de integración del Optimizador de DAX. Se aplica implícitamente cuando se aplica `DisableDaxOptimizer` o `DisableDaxOptimizerUpload`. |
| DisableDaxPackageManager       | **(Solo TE3)** La función del Administrador de paquetes de DAX no estará disponible.                                                                                                                                                                                                               |
| DisableAi                      | **(Solo TE3)** Toda la funcionalidad de IA está deshabilitada. El módulo de IA no se carga al iniciar y no se dispone de ninguna función relacionada con la IA. Se borra cualquier configuración de clave de API almacenada previamente.                           |

## Deshabilitar las comunicaciones web

Si quieres asegurarte de que Tabular Editor no realice solicitudes web, especifica las directivas `DisableUpdates`, `DisableBpaDownload`, `DisableWebDaxFormatter`, `DisableErrorReports`, `DisableTelemetry`, `DisableDaxOptimizer` y `DisableAi`.

> [!NOTE]
> Incluso cuando se especifican las políticas anteriores, Tabular Editor 3 seguirá realizando solicitudes ocasionales a `https://api.tabulareditor.com` para validar la licencia. Si Tabular Editor 3 no puede acceder a este endpoint (debido a un cortafuegos o un proxy), el usuario tendrá que [activar manualmente](xref:installation-activation-basic#manual-activation-no-internet) el producto cada 30 días.

## Deshabilitar los scripts personalizados

Si quieres asegurarte de que Tabular Editor no permita a los usuarios ejecutar código arbitrario, especifica las políticas `DisableCSharpScripts` y `DisableMacros` para deshabilitar las macros.

## Deshabilitar las funciones de IA

Si quieres impedir toda la funcionalidad de IA, especifica la directiva `DisableAi`. Esto evita que el módulo de IA se cargue al inicio y borra cualquier configuración de clave de API almacenada previamente.