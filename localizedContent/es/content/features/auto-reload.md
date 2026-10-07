---
uid: auto-reload
title: Recarga automática desde el disco
author: Morten Lønskov
updated: 2026-09-23
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.27.0
      editions:
        - edition: Desktop
          none: true
          note: "Desktop Edition can't open or save model metadata files."
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Recarga automática desde el disco

When the metadata files of a model you loaded from a file or folder change on disk, Tabular Editor reloads the model automatically. If you have unsaved changes, a prompt appears where you choose to reload or keep your changes. Typical sources of external changes are an AI agent, a script, another editor, a `git pull` or a colleague editing a shared folder.

![Diagram: File > Save writes the model in Tabular Editor to the files on disk; another tool writes to the files; an automatic reload loads the changed files back into Tabular Editor](~/content/assets/images/features/auto-reload-sync.png)

> [!NOTE]
> Auto-reload monitors files and is independent of **Track external model changes** and **Refresh local Tabular Object Model metadata automatically** under [Tools > Preferences > Tabular Editor > Miscellaneous](xref:preferences#miscellaneous). Those settings use an Analysis Services trace to detect changes to a connected database.

## Monitored files

| Modelo cargado desde                                                                            | Monitored files                                                                                                            |
| ----------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Un archivo `.bim`                                                                               | That file. Se ignoran los demás archivos de la misma carpeta.                              |
| Una carpeta en formato JSON (Database.json)                  | Todos los archivos `.json` que estén bajo la raíz del modelo, incluidos los de las subcarpetas.            |
| Una carpeta en formato [Tabular Model Definition Language (TMDL)](xref:tmdl) | Todos los archivos `.tmdl` debajo de la raíz del modelo, incluidas las subcarpetas.                        |
| Una base de datos del Workspace                                                                 | The files backing the model in [workspace mode](xref:workspace-mode), by the same rules as the rows above. |
| Una base de datos o Power BI Desktop, fuera del modo del área de trabajo                        | Ninguno. The model has no files on disk.                                                   |
| Una plantilla `.pbit` o un modelo que nunca has guardado                                        | Ninguno.                                                                                                   |

## Reload with unsaved changes

If you have unsaved changes, the **External changes detected** prompt appears and you choose which version to keep, because Tabular Editor doesn't merge them.

![External changes detected prompt with the Reload and Ignore buttons, Reload focused](~/content/assets/images/features/external-changes-prompt.png)

- **Reload** discards your unsaved changes and loads the version on disk.
- **Ignore** keeps your changes. The files on disk keep the external changes, and your next save overwrites them.

Pressing **Esc** or closing the prompt has the same effect as **Ignore**.

> [!WARNING]
> **Reload** is the default button, so pressing **Enter** at the prompt also reloads. A reload discards your unsaved changes without further confirmation, and you can't undo it.

### Ejemplo

1. Abres un modelo TMDL basado en carpetas y cambias el nombre de una medida.
2. Un agente de IA que trabaja en la misma carpeta reescribe cuatro archivos `.tmdl`.
3. After the agent's writes finish, one **External changes detected** prompt appears.
4. You choose **Reload**, which discards the rename and loads the agent's changes. The TOM Explorer keeps its expanded nodes.

## Multiple writes and background changes

When a tool rewrites a folder-serialized model, it changes many files in quick succession, and Tabular Editor reloads once, after the writes finish.

If Tabular Editor isn't the active window when the files change, the reload or prompt happens when you switch back to it. All changes made while it was inactive produce one prompt.

## Modo del área de trabajo

In [workspace mode](xref:workspace-mode), a reload also redeploys the model to the workspace database.

## Desactivarlo

Auto-reload is enabled by default, and you turn it off by clearing **Automatically reload from disk (hot reload)** under **Tools > Preferences > Tabular Editor > Miscellaneous**.

![Tools > Preferences > Tabular Editor > Miscellaneous, showing the automatic reload setting under Metadata Synchronization](~/content/assets/images/pref-miscellaneous.png)

Turn it off if a continuously running process also writes to the model folder, such as a file sync client or a CI checkout that refreshes in the background. Each change triggers a reload, or the modal prompt when you have unsaved changes.

With the setting cleared, use **File > Reload from disk** to load external changes, or **File > Save** to overwrite them with the model in Tabular Editor. See [Preferences](xref:preferences#miscellaneous) for the other settings on that page.
