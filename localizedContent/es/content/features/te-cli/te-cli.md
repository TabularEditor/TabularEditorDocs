---
uid: te-cli
title: Tabular Editor CLI (Vista previa pública limitada)
author: Peer Grønnerup
updated: 2026-06-11
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      none: true
    - product: Tabular Editor CLI
      full: true
---

# Tabular Editor CLI (Vista previa pública limitada)

Tabular Editor CLI (`te`) es una interfaz de línea de comandos multiplataforma para modelos semánticos de Power BI y Analysis Services. Funciona en Windows, macOS y Linux como un único ejecutable autocontenido y se basa en la misma base que sustenta Tabular Editor 3.

Con Tabular Editor CLI puedes inspeccionar, editar, validar, implementar, actualizar y probar modelos semánticos desde la terminal, ya sea con archivos TMDL o BIM locales, con Power BI Desktop o con modelos semánticos en Workspaces de Fabric y del servicio Power BI.

A diferencia de las opciones de línea de comandos de `TabularEditor.exe` exclusivas de Windows (TE2) —diseñadas principalmente para automatizar C# Scripts y macros desde un binario de escritorio—, `te` es una CLI multiplataforma diseñada específicamente, con salida estructurada, códigos de salida predecibles y un shell interactivo. Esto habilita escenarios que nuestra [CLI de TE2](xref:command-line-options) actual no cubre bien: trabajo con modelos desde la terminal en macOS y Linux, agentes de IA que aplican cambios al modelo directamente y un reemplazo directo y limpio para cualquier runner moderno de CI.

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

## Diseñado para tres tipos de usuarios

Tres pilares de diseño están presentes en todos los comandos:

- **Structured output** - JSON, CSV, TMDL, TMSL alongside default human-readable text.
- **Non-interactive mode** - a global `--non-interactive` flag that disables prompts and fails fast.
- **Clear errors** - written to stderr with predictable exit codes.

En conjunto, hacen que el mismo binario funcione bien para tres perfiles muy distintos:

- **Personas** — automatizando ediciones masivas mediante scripts, explorando un modelo desde la terminal y componiendo comandos en canalizaciones de shell.
- **Agentes de IA** — JSON eficiente en tokens, formatos de error analizables por máquina y códigos de salida que indican éxito o error sin necesidad de analizar stdout.
- **Canalizaciones de CI/CD** — ejecución no interactiva, anotaciones de GitHub Actions y Azure DevOps, y resultados de pruebas compatibles con VSTEST.

> [!Note]
> Cuando uses la TE CLI con agentes, usa la [skill de TE CLI para agentes de codificación con IA](https://github.com/TabularEditor/CLI/tree/main/skill), que encapsula la TE CLI de principio a fin.

## Qué puede hacer la CLI

La CLI organiza más de 50 comandos en 10 familias. Cada familia se corresponde con una etapa concreta del ciclo de vida del modelo semántico.

Consulta @te-cli-commands para ver una referencia completa de los comandos, con la sintaxis, las opciones y ejemplos de cada uno. Haz clic en cualquier comando de ejemplo de la tabla para ir directamente a su entrada de referencia.

| Familia                                                                        | Qué hace                                                                                        | Comandos de ejemplo                                                                                                                                                                      |
| ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [E/S del modelo](xref:te-cli-commands#model-io)                                | Cargar, guardar, convertir e inicializar modelos                                                | [`te load`](xref:te-cli-commands#load), [`te save`](xref:te-cli-commands#save), [`te init`](xref:te-cli-commands#init)                                                                   |
| [Edición del modelo](xref:te-cli-commands#model-editing)                       | Obtener y establecer propiedades; añadir, quitar y mover objetos                                | [`te set`](xref:te-cli-commands#set), [`te add`](xref:te-cli-commands#add), [`te remove`](xref:te-cli-commands#remove), [`te move`](xref:te-cli-commands#move)                           |
| [Inspección](xref:te-cli-commands#inspection)                                  | Listar objetos, buscar, comparar y analizar dependencias                                        | [`te list`](xref:te-cli-commands#list), [`te find`](xref:te-cli-commands#find), [`te diff`](xref:te-cli-commands#diff), [`te deps`](xref:te-cli-commands#deps)                           |
| [Análisis y calidad](xref:te-cli-commands#analysis-and-quality)                | Validar, ejecutar BPA, dar formato a DAX y analizar el almacenamiento                           | [`te validate`](xref:te-cli-commands#validate), [`te bpa run`](xref:te-cli-commands#bpa-run), [`te format`](xref:te-cli-commands#format), [`te vertipaq`](xref:te-cli-commands#vertipaq) |
| [Ejecución](xref:te-cli-commands#execution)                                    | Ejecutar consultas DAX, C# Scripts y macros                                                     | [`te query`](xref:te-cli-commands#query), [`te script`](xref:te-cli-commands#script), [`te macro`](xref:te-cli-commands#macro)                                                           |
| [Implementación y actualización](xref:te-cli-commands#deployment-and-refresh)  | Implementar en el Workspace, iniciar una actualización y realizar una actualización incremental | [`te deploy`](xref:te-cli-commands#deploy), [`te refresh`](xref:te-cli-commands#refresh), [`te incremental-refresh`](xref:te-cli-commands#incremental-refresh)                           |
| [Pruebas](xref:te-cli-commands#testing)                                        | Pruebas de aserciones, instantáneas, comparación A/B                                            | [`te test run`](xref:te-cli-commands#test-run)                                                                                                                                           |
| [Conexión y autenticación](xref:te-cli-commands#connection-and-authentication) | Conéctate a los Workspace y gestiona la autenticación y los perfiles                            | [`te connect`](xref:te-cli-commands#connect), [`te auth`](xref:te-cli-commands#auth-login--status--logout), [`te profile`](xref:te-cli-commands#profile-list--show--set--remove)         |
| [Configuración](xref:te-cli-commands#configuration)                            | Configuración y licencias                                                                       | [`te config`](xref:te-cli-commands#config-list--paths--init--set)                                                                                                                        |
| [Shell](xref:te-cli-commands#shell)                                            | Modo interactivo, estado de la sesión, completado automático del shell                          | [`te interactive`](xref:te-cli-commands#interactive), [`te session`](xref:te-cli-commands#session), [`te completion`](xref:te-cli-commands#completion)                                   |

> [!TIP]
> The docs use canonical long-form verbs (`list`, `remove`, `move`), but the classic short forms still work as aliases (`ls`, `rm`, `mv`, `rename`). This applies to top-level commands and to `remove` / `list` subcommands under groups like `te bpa rules`, `te macro`, `te config`, `te profile`, `te session`, and `te test`. See @te-cli-commands#command-aliases for the full mapping.

## Primeros pasos

1. **Regístrate o inicia sesión** en [tabulareditor.com](https://tabulareditor.com/download-tabular-editor-cli) con una cuenta de Tabular Editor.
2. **Descarga e instala**: consulta @te-cli-install para ver las instrucciones para Windows, macOS y Linux.
3. **Autentícate**: ejecuta `te auth login` para conectarte a Power BI o Fabric. Consulta @te-cli-auth.
4. **Ejecuta tu primer comando**: `te --help` enumera todos los comandos; `te <command> --help` muestra las opciones detalladas. Tip: running `te` on its own in a terminal drops you into the interactive REPL - a friendly way to explore a model. Consulta @te-cli-interactive.

Para ver por primera vez un modelo en vivo, solo necesitas dos comandos:

```bash
te auth login
te list -s MyWorkspace -d MyModel
```

![Tabular Editor CLI te list example output](~/content/assets/images/features/cli/cli-command-ls.png)

## Aviso de versión preliminar

De forma predeterminada, todos los comandos imprimen un banner amarillo de versión preliminar en stderr:

![Banner del aviso de versión preliminar de la CLI de Tabular Editor](~/content/assets/images/features/cli/cli-preview-notice.png)

Para ocultar el aviso de versión preliminar, simplemente ejecuta:

```bash
te config set hidePreviewNotice true
```

> [!WARNING]
> El banner vuelve a aparecer con cada comando en los **14 días previos a la fecha de finalización de la versión preliminar** (2026-09-30), independientemente de `hidePreviewNotice`. Esto garantiza que veas una advertencia antes de que la CLI deje de funcionar.

## Perspectiva de licencias

Durante la vista previa pública limitada, la CLI no requiere una licencia; solo necesitas una cuenta de Tabular Editor para descargarla. En la disponibilidad general (GA), la CLI requerirá una licencia; los precios aún se están ultimando y se anunciarán antes de GA.

## Comentarios y comunidad

Durante la vista previa, los Report de errores, las solicitudes de funcionalidades y el debate general se realizan en el repositorio público [TabularEditor/CLI](https://github.com/TabularEditor/CLI) en GitHub:

- **Incidencias**: para enviar un Report de errores, solicitar funcionalidades y hacer seguimiento de los problemas conocidos.
- **Debates**: haz preguntas, comparte comentarios e intercambia consejos de uso con otros adoptantes tempranos.

El repositorio no aloja el código fuente de la CLI; existe para dar a la comunidad un lugar público donde contactar con nosotros durante la vista previa.

## Siguientes pasos

- @te-cli-install - descargar, instalar y verificar.
- @te-cli-auth - autenticarse en Power BI, Fabric y Azure Analysis Services.
- @te-cli-commands - referencia completa de comandos.
- @te-cli-config - archivo de configuración y sobrescrituras de rutas.
- @te-cli-interactive - modo REPL guiado para nuevos usuarios.
- @te-cli-automation - salida estructurada y patrones de scripting para Python, PowerShell y Bash.
- @te-cli-cicd - ejemplos de canalizaciones de GitHub Actions y Azure DevOps.
- @te-cli-migrate - migración desde la línea de comandos de Tabular Editor 2.
