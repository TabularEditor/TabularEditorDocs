---
uid: dax-package-manager
title: DAX 组件管理器
author: Daniel Otykier
updated: 2025-11-03
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# DAX 组件管理器

## 概述

Tabular Editor 中的 **DAX 组件管理器**（DPM）使用户能够直接在应用程序内轻松发现、安装、更新并管理 [DAX 用户自定义函数（UDF）](xref:udfs) 库（称为 DAX 组件）。  
这些库通过可重用函数扩展了你的 DAX 能力，让你更轻松地构建一致且易于维护的 Power BI 语义模型。

顾名思义，这项功能相当于一个组件管理器，其工作方式类似 NuGet 或 npm 为开发者管理代码库。 DAX 组件的来源是 https://daxlib.org，这是由 [SQLBI](https://sqlbi.com) 发起并维护的开源非营利项目。

你可以在任何支持 DAX 用户自定义函数的模型中使用 DAX 组件管理器，也就是说，模型的兼容级别必须为 1702 或更高。

> [!WARNING]
> DAX 用户自定义函数目前（截至 2025 年十一月）仍是 Power BI 的一项预览功能。 使用前请先了解相关[限制](https://learn.microsoft.com/en-us/dax/best-practices/dax-user-defined-functions#considerations-and-limitations)。

---

![DAX 组件管理器](~/content/assets/images/dax-package-manager-overview.png)

## 界面布局

### 1. 启动 DAX 组件管理器

你可以通过 **视图** 菜单打开 DPM 面板。 你也可以通过 **Tools > Preferences > Keyboard** 为 `View.DaxPackageManager` 命令分配自定义快捷键。

- **菜单：** `视图 → DAX 组件管理器`
- **快捷键：** _(如果已在偏好设置中分配)_

---

### 2. 组件列表

在屏幕左侧，你会看到以下三个选项卡。 每个选项卡都对应一个相关的组件列表：

| 选项卡     | 说明                                      |
| ------- | --------------------------------------- |
| **浏览**  | 从提供程序（例如 `api.daxlib.org`）发现可用的 DAX 组件。 |
| **已安装** | 查看当前已安装的所有组件及其版本。                       |
| **更新**  | 查看有可用新版本的组件。                            |

每个组件条目都包括：

- **名称及简短描述**
- **版本号**
- **作者或所有者**
- **提供方 URL**
- **安装 / 卸载 / 更新按钮**
- **受欢迎程度指标（下载次数）**

---

### 3. 搜索栏

输入搜索关键词或组件名称（可输入部分名称），即可将列表筛选为仅显示与搜索条件匹配的项目。 这项功能适用于三个选项卡，即 **浏览**、**已安装** 和 **更新**。

> [!NOTE]
> 目前我们只显示符合搜索条件的前 20 个组件。 目前还不支持分页；此功能将在后续更新中提供。 如果你需要浏览所有可用组件，请前往源站点，例如 https://daxlib.org。

---

### 4. 组件详细信息窗格

选择某个组件后，会显示以下详细信息：

| 字段                 | 说明                                   |
| ------------------ | ------------------------------------ |
| **已安装 / 版本**       | 当前版本以及可用更新。                          |
| **说明**             | 对该库所提供内容的概述。                         |
| **发布说明**           | 有关最新版本中新功能或变更的信息。                    |
| **提供方 / 所有者 / 作者** | 署名元数据。                               |
| **标签**             | 有助于分类和搜索。                            |
| **URL**            | 项目文档、API 以及 GitHub repository 的直接链接。 |
| **发布日期**           | 当前版本发布的时间戳。                          |
| **下载量**            | 所有用户的总安装次数。                          |

尚未安装的组件会显示 **“安装”** 按钮。 单击此按钮会立即将该组件中的 UDF 添加到你的模型中。

已安装的组件会显示 **“移除”** 按钮。

有较新版本可用的组件会显示 **“更新”** 按钮。

> [!WARNING]
> 如果你移除或更新某个组件，而你已修改过其中一个或多个 UDF 的 DAX 表达式，则会显示警告信息，提示你的更改将丢失。

---

### 5. 更新通知

当你打开使用了某个有更新可用的组件的模型时，会在 **TOM Explorer** 底部看到更新通知。

单击更新通知，或打开 DAX 组件管理器视图，查看并安装更新。

---

## 安装组件

1. 打开 **DAX 组件管理器**。
2. 在 **浏览** 选项卡中，选择一个组件（例如 `DaxLib.SVG`）。 按需使用搜索栏进一步筛选结果。
3. 单击 **安装**。
4. 安装完成后，该组件及其函数将显示在 TOM Explorer 中。

安装前还可以选择特定 **版本**，这对于回归测试或确保与旧模型兼容很有帮助。

---

## 更新组件

1. 转到 **更新** 选项卡，或选择一个有较新版本可用的组件。
2. 单击 **全部更新** 以更新所有已安装的组件，或对某个组件单击 **更新**。
3. DPM 会获取最新定义，并自动替换现有函数。

---

## 移除组件

1. 转到 **已安装** 选项卡。
2. 选择要移除的组件。
3. 点击 **移除**。

所有关联的 UDF 都将从模型中移除。

> [!CAUTION]
> 移除 UDF 可能会导致模型中其他区域（度量值、计算列等）中的 DAX 表达式 变得无效。 如果发生这种情况，你随时可以点击 **撤销**（Ctrl+Z）来撤销移除组件的操作。 在移除组件之前，请先使用 **显示依赖关系**（Shift+F12）功能确定这些 UDF 的使用位置。

---

## 技术注意事项

DAX Package Manager 使用 [扩展属性](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.extendedproperty?view=analysisservices-dotnet) 来跟踪已安装的组件。 扩展属性与批注类似，但更适合以 JSON 格式存储自定义元数据。

DAX Package Manager 会在 **模型** 对象上创建以下扩展属性：

| 属性名称                             | 说明                                                                       |
| -------------------------------- | ------------------------------------------------------------------------ |
| `TabularEditor_ModelDaxPkgTable` | 一个 JSON 字典，每个已安装的组件对应一个条目。 键为按顺序递增的整数；值则包含组件提供程序、该提供程序中的组件 ID 以及组件版本等信息。 |
| `TabularEditor_ModelDaxPkgSeq`   | 一个整数值，每次安装组件时都会递增。 这用于为 `TabularEditor_ModelDaxPkgTable` 属性生成唯一键。        |

此外，通过 DAX Package Manager 导入的每个 UDF 都会被赋予以下扩展属性：

| 属性名称                                 | 说明                                                                                        |
| ------------------------------------ | ----------------------------------------------------------------------------------------- |
| `TabularEditor_ObjDaxPkgHandle`      | 一个整数值，对应于模型上 `TabularEditor_ModelDaxPkgTable` 属性中的键。 这使 Tabular Editor 能够识别某个 UDF 属于哪个组件。 |
| `TabularEditor_ObjDaxPkgContentHash` | 在安装时根据 UDF 的 DAX 表达式计算出的哈希值。 它用于检测 UDF 自安装以来是否被修改过，这在更新或移除组件时非常重要。                        |

> [!CAUTION]
> 手动修改或删除这些扩展属性可能会导致 DAX 组件管理器出现异常行为。

## 处理冲突

### 修改来自组件的 UDF

如果你修改了从 DAX 组件导入的 UDF 的 DAX 表达式，那么在升级或移除该组件时会看到以下提示：

![更新已修改的 UDF](~/content/assets/images/dax-package-manager-update-modified.png)

你有以下选项：

- **是**：将继续更新，并用 DAX 组件管理器源中提供的定义覆盖你对 UDF 所做的更改。
- **否**：将继续更新，但已修改的 UDF(s) 将保持不变；如果此次组件更新包含破坏性更改，可能会引发问题。
- **取消**：取消更新。

> [!TIP]
> 如果你想让现有 UDF 与 DAX 组件管理器“取消关联”，请从 UDF 对象中移除扩展属性 `TabularEditor_ObjDaxPkgHandle` 和 `TabularEditor_ObjDaxPkgContentHash`。 这样一来，DAX 组件管理器将不再跟踪这些 UDF，它们也不会受到后续组件更新或移除的影响。 不过，你仍然需要注意名称冲突。

### 安装存在名称冲突的组件

如果你尝试安装的组件中包含某个 UDF，其名称与模型中现有 UDF 相同（无论该 UDF 是从其他组件导入的还是手动创建的），你会看到以下提示：

![安装组件时的名称冲突](~/content/assets/images/dax-package-manager-install-conflict.png)

你有以下选项：

- **是**：将继续安装，组件中的 UDF 会覆盖模型中现有的 UDF。
- **否**：将继续安装，但会跳过组件中存在冲突的 UDF(s)。
- **取消**：取消安装。

---

## 补充资源

- [DaxLib 项目网站](https://daxlib.org)
- [DaxLib GitHub repository](https://github.com/daxlib/daxlib)
- [DAX 用户自定义函数（Microsoft Learn）](https://learn.microsoft.com/en-us/dax/best-practices/dax-user-defined-functions)
- [Tabular Editor 3 中的用户自定义函数](xref:udfs)
