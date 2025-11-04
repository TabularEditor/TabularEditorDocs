## User Settings Files

When Tabular Editor is executed, it writes some additional files to the disk at various locations. What follows is a description of these files and their content:

### In %ProgramData%\TabularEditor

- **BPARules.json** Best Practice Analyzer rules that are available to all users.
- **TOMWrapper.dll** This file is used when executing scripts inside Tabular Editor. You can also reference the .dll in your own .NET projects, to utilise the wrapper code. If you are having issues executing advanced scripts after upgrading Tabular Editor, please delete this file and restart Tabular Editor.
- **Preferences.json** This file stores all preferences set in the File > Preferences dialog.

### In %AppData%\Local\TabularEditor

- **BPARules.json** Best Practice Analyzer rules that are available only to the current user.
- **CustomActions.json** Custom script actions that can be invoked from the right-click menu or the Tools-menu of the Explorer Tree. These actions can be created on the Advanced Script Editor tab.
- **RecentFiles.json** Stores a list of recently opened .bim files. The last most 10 items in this list is displayed in the File > Recent Files menu.
- **RecentServers.json** Stores a list of recently accessed server names. These are displayed in the dropdown portion of the "Connect to Database" dialog box and in the Deployment Wizard.
