---
uid: user-setting-files-te2
title: Tabular Editor 2 的用户设置文件
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      none: true
---

# Tabular Editor 2 的用户设置文件

启动 Tabular Editor 2 时，它会在磁盘的多个位置写入一些额外文件。 What follows is a description of these files and their content:

### 位于 %ProgramData%\TabularEditor

- **BPARules.json** 所有用户都可使用的 Best Practice Analyzer 规则。
- **TOMWrapper.dll** 在 Tabular Editor 中执行脚本时会用到此文件。 You can also reference the .dll in your own .NET projects, to utilise the wrapper code. If you are having issues executing advanced scripts after upgrading Tabular Editor, please delete this file and restart Tabular Editor.
- **Preferences.json** 此文件保存通过“文件 > 偏好设置”对话框设置的所有偏好。

### 位于 %AppData%\Local\TabularEditor

- **BPARules.json** 仅当前用户可用的 Best Practice Analyzer 规则。
- **CustomActions.json** 可从资源管理器树的右键菜单或“工具”菜单调用的自定义脚本操作。 These actions can be created on the Advanced Script Editor tab.
- **RecentFiles.json** 存储最近打开的 .bim 文件列表。 The last most 10 items in this list is displayed in the File > Recent Files menu.
- **RecentServers.json** Stores a list of recently accessed server names. These are displayed in the dropdown portion of the "Connect to Database" dialog box and in the Deployment Wizard.
