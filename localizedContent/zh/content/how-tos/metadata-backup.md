---
uid: metadata-backup
title: 元数据备份
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 元数据备份

如果需要，Tabular Editor 可以在每次保存（连接到现有数据库时）或部署之前，自动为现有模型元数据保存一份备份。 This is useful if you're not using a version control system, but still need to rollback to a previous version of your model.

To enable this setting, go to **Tools > Preferences** (**File > Preferences** in Tabular Editor 2), enable the checkbox and choose a folder to place the metadata backups:

<img src="../assets/images/metadata-backup-01.png" width="300" />

启用该设置后，每当你使用 Deployment Wizard，或在连接到（workspace，工作区）数据库时点击 "Save" 按钮，系统都会将现有模型元数据的压缩（zipped）版本保存到此位置。