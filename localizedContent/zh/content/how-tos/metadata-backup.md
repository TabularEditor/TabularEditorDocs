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

## 元数据备份

如果需要，Tabular Editor 可以在每次保存（连接到现有数据库时）或部署之前，自动为现有模型元数据保存一份备份。 如果你没有使用版本控制系统，但仍需要将模型回退到之前的版本，这个功能就很有用。 如果你没有使用版本控制系统，但仍需要将模型回退到之前的版本，这个功能就很有用。

要启用此设置，请依次选择“File”>“偏好”，勾选复选框，并选择一个用于存放元数据备份的文件夹：

<img src="https://user-images.githubusercontent.com/8976200/91543926-3de69100-e91f-11ea-88de-3def2b97eae0.png" width="300" />

启用该设置后，每当你使用 Deployment Wizard，或在连接到（workspace，工作区）数据库时点击 "Save" 按钮，系统都会将现有模型元数据的压缩（zipped）版本保存到此位置。