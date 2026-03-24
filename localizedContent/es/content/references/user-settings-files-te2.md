---
uid: archivos-de-configuracion-del-usuario-te2
title: Archivos de configuración del usuario de Tabular Editor 2
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      none: true
---

## Archivos de configuración del usuario de Tabular Editor 2

Cuando se inicia Tabular Editor 2, escribe algunos archivos adicionales en el disco en varias ubicaciones. A continuación se describen estos archivos y su contenido:

### En %ProgramData%\TabularEditor

- **BPARules.json** Reglas del Best Practice Analyzer disponibles para todos los usuarios.
- **TOMWrapper.dll** Este archivo se utiliza al ejecutar scripts dentro de Tabular Editor. También puedes hacer referencia a la .dll en tus propios proyectos .NET para aprovechar el código del wrapper. Si tienes problemas al ejecutar scripts avanzados después de actualizar Tabular Editor, elimina este archivo y reinicia Tabular Editor.
- **Preferences.json** Este archivo almacena todas las preferencias establecidas en el cuadro de diálogo Archivo > Preferencias.

### En %AppData%\Local\TabularEditor

- **BPARules.json** Reglas del Best Practice Analyzer disponibles solo para el usuario actual.
- **CustomActions.json** Acciones de script personalizadas que se pueden invocar desde el menú contextual de clic derecho o desde el menú Herramientas del árbol del Explorador. Estas acciones se pueden crear en la pestaña Editor avanzado de scripts.
- **RecentFiles.json** Almacena una lista de archivos .bim abiertos recientemente. Los 10 últimos elementos de esta lista se muestran en el menú Archivo > Archivos recientes.
- **RecentServers.json** Almacena una lista de nombres de servidores a los que se accedió recientemente. Se muestran en la lista desplegable del cuadro de diálogo "Conectar a la base de datos" y en el Asistente de implementación.
