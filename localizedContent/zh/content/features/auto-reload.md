---
uid: auto-reload
title: 从磁盘自动重新加载
author: Morten Lønskov
updated: 2026-10-11
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
# 从磁盘自动重新加载

当您从文件或文件夹加载的模型的元数据文件在磁盘上发生变化时，Tabular Editor 会自动重新加载该模型。如果您有未保存的更改，系统会显示提示，让您选择重新加载或保留更改。外部更改的常见来源包括 AI 代理、脚本、其他编辑器、“git pull”或编辑共享文件夹的同事。

![示意图：文件 > 保存将 Tabular Editor 中的模型写入磁盘上的文件；另一个工具写入文件；自动重新加载将更改后的文件重新加载到 Tabular Editor 中](~/content/assets/images/features/auto-reload-sync.png)

> [!NOTE]
> 自动重新加载功能会监视文件，并且独立于 [工具 > 首选项 > Tabular Editor > 其他](xref:preferences#tabular-editor--miscellaneous) 下的 **跟踪外部模型更改** 和 **自动刷新本地 Tabular Object Model 元数据**。这些设置使用 Analysis Services 跟踪来检测对已连接数据库的更改。

## 受监视的文件

| 模型加载自 | 受监视的文件 |
|---|---|
| “.bim”文件 | 该文件。同一文件夹中的其他文件将被忽略。|
| JSON (Database.json) 格式的文件夹 | 模型根目录下的每个“.json”文件，包括子文件夹。|
| [表格模型定义语言 (TMDL)](xref:tmdl) 格式的文件夹 | 模型根目录下的每个“.tmdl”文件，包括子文件夹。|
| 工作区数据库 | 在[工作区模式](xref:workspace-mode)下支持模型的文件，遵循与上述行相同的规则。|
| 数据库或 Power BI Desktop，非工作区模式 | 无。模型在磁盘上没有文件。|
| “.pbit”模板或您从未保存过的模型 | 无。|

## 重新加载并保留未保存的更改

如果您有未保存的更改，则会显示“检测到外部更改”提示，并且您可以选择要保留的版本，因为 Tabular Editor 不会合并这些更改。

![带有“重新加载”和“忽略”按钮的“检测到外部更改”提示，焦点在“重新加载”上](~/content/assets/images/features/external-changes-prompt.png)

- **重新加载**将放弃您未保存的更改，并加载磁盘上的版本。
- **忽略**将保留您的更改。磁盘上的文件保留外部更改，您下次保存时将覆盖这些更改。

按 **Esc** 或关闭提示的效果与**忽略**相同。

> [!WARNING]
> **重新加载**是默认按钮，因此在提示时按**Enter**也会重新加载。重新加载会放弃您未保存的更改，无需进一步确认，且无法撤消。

### 示例

1. 您打开一个 TMDL 文件夹模型并重命名一个度量值。
2. 在同一文件夹中工作的 AI 代理重写了四个“.tmdl”文件。
3. 代理的写入操作完成后，将显示一个**检测到外部更改**提示。
4. 您选择**重新加载**，这将放弃重命名并加载代理的更改。TOM Explorer 保留其展开的节点。

## 多次写入和后台更改

当工具重写文件夹序列化模型时，它会快速连续地更改多个文件，并且 Tabular Editor 在写入完成后会重新加载一次。

如果文件发生变化时 Tabular Editor 不是活动窗口，则在您切换回该窗口时会进行重新加载或显示提示。在非活动状态下所做的所有更改都会产生一个提示。

## 工作区模式

在[工作区模式](xref:workspace-mode)下，重新加载还会将模型重新部署到工作区数据库。

## 关闭

默认情况下，自动重新加载处于启用状态。要将其禁用，请在**工具 > 首选项 > Tabular Editor > 其他**下取消选中**自动从磁盘重新加载（热重载）**。

![工具 > 首选项 > Tabular Editor > 其他，显示“元数据同步”下的自动重新加载设置](~/content/assets/images/pref-miscellaneous.png)

如果某个持续运行的进程（例如文件同步客户端或在后台刷新的 CI 签出）也会写入模型文件夹，请将其关闭。每次更改都会触发重新加载，或者当您有未保存的更改时，会弹出模态提示。

取消该设置后，使用**文件 > 从磁盘重新加载**来加载外部更改，或使用**文件 > 保存**使用 Tabular Editor 中的模型覆盖它们。有关该页面上的其他设置，请参阅[偏好](xref:preferences#tabular-editor--miscellaneous)。
