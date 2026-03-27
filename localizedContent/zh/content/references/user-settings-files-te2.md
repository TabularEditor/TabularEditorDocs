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

## Tabular Editor 2 的用户设置文件

启动 Tabular Editor 2 时，它会在磁盘的多个位置写入一些额外文件。 下面将说明这些文件及其内容：

### 位于 %ProgramData%\TabularEditor

- **BPARules.json** 所有用户都可使用的 Best Practice Analyzer 规则。
- **TOMWrapper.dll** 在 Tabular Editor 中执行脚本时会用到此文件。 你也可以在自己的 .NET 项目中引用该 .dll，以便使用这些封装代码。 如果你在升级 Tabular Editor 后执行高级脚本时遇到问题，请删除此文件并重启 Tabular Editor。
- **Preferences.json** 此文件保存通过“文件 > 偏好设置”对话框设置的所有偏好。

### 位于 %AppData%\Local\TabularEditor

- **BPARules.json** 仅当前用户可用的 Best Practice Analyzer 规则。
- **CustomActions.json** 可从资源管理器树的右键菜单或“工具”菜单调用的自定义脚本操作。 这些操作可以在“高级脚本编辑器”选项卡中创建。
- **RecentFiles.json** 存储最近打开的 .bim 文件列表。 该列表中最新的 10 个项目会显示在“文件 > 最近使用的文件”菜单中。
- **RecentServers.json** 存储最近访问的服务器名称列表。 这些名称会显示在“连接到数据库”对话框的下拉列表中，也会显示在 Deployment Wizard 中。
