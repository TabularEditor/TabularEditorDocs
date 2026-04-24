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

Tabular Editor 中的 **DAX 组件管理器**（DPM）使用户能够直接在应用内轻松发现、安装、更新并管理 [DAX 用户自定义函数（UDF）](xref:udfs) 库（称为 DAX 组件）。  
这些库通过可重用函数扩展你的 DAX 功能，让你更容易构建一致且易于维护的 Power BI 语义模型。

顾名思义，该功能的工作方式类似于 NuGet 或 npm 等组件管理器，用于帮助开发者管理代码库。 DAX 组件来源于 https://daxlib.org，这是由 [SQLBI](https://sqlbi.com) 创建的开源非营利项目。

只要模型支持 DAX 用户自定义函数，你就可以使用 DAX 组件管理器；也就是说，模型的兼容级别必须为 1702 或更高。

> [!WARNING]
> DAX 用户自定义函数目前（截至 2025 年十一月）是 Power BI 的预览功能。 使用前请先了解其[限制](https://learn.microsoft.com/en-us/dax/best-practices/dax-user-defined-functions#considerations-and-limitations)。

---

![DAX 组件管理器](~/content/assets/images/dax-package-manager-overview.png)

## 界面布局

### 1。 启动 DAX 组件管理器

你可以通过 **视图** 菜单打开 DPM 面板。 你也可以通过 **工具 > 偏好 > 键盘** 为 `View.DaxPackageManager` 命令分配自定义快捷键。

- **菜单：** `视图 → DAX 组件管理器`
- **快捷键：** _(如果已在偏好设置中分配)_

---

### 2。 组件列表

在屏幕左侧，你会看到以下三个选项卡。 每个选项卡旁都会显示一个与该选项卡相关的组件列表：

| 选项卡     | 说明                                                          |
| ------- | ----------------------------------------------------------- |
| **浏览**  | 从提供方 (例如 `api.daxlib.org`) 发现可用的 DAX 组件。 |
| **已安装** | 查看当前已安装的所有组件及其版本。                                           |
| **更新**  | 查看有可用新版本的组件。                                                |

每个组件条目包含：

- **名称和简短说明**
- **版本号**
- **作者或所有者**
- **提供方 URL**
- **安装 / 删除 / 更新按钮**
- **热度指标（下载次数）**

---

### 3。 搜索栏

输入搜索关键词或组件名称（可输入部分名称），即可筛选列表，仅显示与搜索词匹配的项目。 此功能适用于这三个选项卡，即 **浏览**、**已安装** 和 **更新**。

> [!NOTE]
> 我们目前只显示与搜索条件匹配的前 20 个组件。 目前还没有分页功能——将在后续更新中加入。 如果需要浏览所有可用的组件，请前往来源网站，例如 https://daxlib.org。

---

### 4。 组件详情面板

选择某个组件后，会显示详细信息：

| 字段                 | 说明                                   |
| ------------------ | ------------------------------------ |
| **已安装 / 版本**       | 当前版本及可用更新信息。                         |
| **说明**             | 该库提供内容的摘要。                           |
| **发布说明**           | 关于最新版本中新功能或变更的信息。                    |
| **提供方 / 所有者 / 作者** | 署名元数据。                               |
| **标签**             | 便于分类和搜索。                             |
| **URL**            | 项目文档、API 以及 GitHub repository 的直接链接。 |
| **发布日期**           | 当前版本发布的时间戳。                          |
| **下载量**            | 所有用户的总安装次数。                          |

未安装的组件会显示 **“安装”** 按钮。 点击该按钮会立即将该组件中的 UDF 添加到你的模型中。

已安装的组件会显示 **“移除”** 按钮。

有新版本可用的组件会显示 **“更新”** 按钮。

> [!WARNING]
> 如果你移除或更新某个组件，而你曾修改过其中一个或多个 UDF 的 DAX 表达式，你会看到一条警告信息，提示这些更改将会丢失。

---

### 5。 更新通知

打开使用了有可用更新的组件的模型时，你会在 **TOM Explorer** 底部看到更新通知。

点击更新通知，或打开 DAX 组件管理器视图，即可查看并安装更新。

---

## 安装组件

1. 打开 **DAX 组件管理器**。
2. 在 **浏览** 选项卡中，选择一个组件（例如 `DaxLib.SVG`）。 按需使用搜索栏缩小搜索范围。
3. 点击 **安装**。
4. 安装完成后，该组件及其函数会显示在 TOM Explorer 中。

你也可以在安装前选择特定的 **版本**——这对回归测试或确保与旧模型兼容很有用。

---

## 更新组件

1. 前往 **更新** 选项卡，或选择一个有新版本可用的组件。
2. 点击 **全部更新** 以更新所有已安装的组件，或对某个组件点击 **更新**。
3. DPM 会获取最新定义，并自动替换现有函数。

---

## 移除组件

1. 转到 **已安装** 选项卡。
2. 选择你要移除的组件。
3. 点击 **移除**。

所有关联的 UDF 都将从模型中移除。

> [!CAUTION]
> 移除 UDF 可能会导致模型中其他位置（度量值、计算列等）的 DAX 表达式 变得无效。 如果发生这种情况，你随时可以按 **撤销**（Ctrl+Z）来撤销移除组件的操作。 在移除组件之前，你可以使用 **显示依赖项**（Shift+F12）功能来查看这些 UDF 在哪些地方被使用。

---

## 技术注意事项

DAX 组件管理器使用 [扩展属性](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.extendedproperty?view=analysisservices-dotnet) 来跟踪已安装的组件。 扩展属性类似于注释，但更适合以 JSON 格式存储自定义元数据。

DAX 组件管理器会在 **Model** 对象上创建以下扩展属性：

| 属性名称                             | 说明                                                                   |
| -------------------------------- | -------------------------------------------------------------------- |
| `TabularEditor_ModelDaxPkgTable` | 一个 JSON 字典，每个已安装的组件对应一个条目。 键是按顺序递增的整数，而值包含组件提供方、提供方内的组件 ID，以及组件版本信息。 |
| `TabularEditor_ModelDaxPkgSeq`   | 一个整数值，每安装一个组件就会递增。 用于为 `TabularEditor_ModelDaxPkgTable` 属性生成唯一键。     |

此外，通过 DAX 组件管理器导入的每个 UDF 都会被赋予以下扩展属性：

| 属性名称                                 | 说明                                                                                       |
| ------------------------------------ | ---------------------------------------------------------------------------------------- |
| `TabularEditor_ObjDaxPkgHandle`      | 一个整数值，对应模型上 `TabularEditor_ModelDaxPkgTable` 属性中的键。 这使 Tabular Editor 能够识别某个 UDF 属于哪个组件。 |
| `TabularEditor_ObjDaxPkgContentHash` | 一个哈希值，在安装时根据该 UDF 的 DAX 表达式计算得出。 用于检测 UDF 自安装以来是否被修改——这在更新或移除组件时很重要。                     |

> [!CAUTION]
> 手动修改或删除这些扩展属性可能会导致 DAX 组件管理器出现意外行为。

## 处理冲突

### 修改从组件导入的 UDF

如果你修改了从 DAX 组件导入的 UDF 的 DAX 表达式，那么在升级或卸载该组件时，你会看到以下提示：

![更新已修改的 UDF](~/content/assets/images/dax-package-manager-update-modified.png)

你有以下选项：

- **是**：将继续更新，并使用 DAX 组件管理器源中的定义覆盖你对该 UDF 所做的更改。
- **否**：更新将继续进行，但已修改的 UDF(s) 将保持不变；如果此次组件更新包含破坏性更改，可能会引发问题。
- **取消**：取消更新。

> [!TIP]
> 如果你想将现有 UDF 与 DAX 组件管理器“取消关联”，请从 UDF 对象中删除扩展属性 `TabularEditor_ObjDaxPkgHandle` 和 `TabularEditor_ObjDaxPkgContentHash`。 这样一来，DAX 组件管理器将不再跟踪这些 UDF，它们也不会受到后续组件更新或卸载的影响。 不过，你仍需要留意名称冲突。

### 安装存在名称冲突的组件

如果你尝试安装的组件中包含一个与模型中现有 UDF 同名的 UDF（无论该现有 UDF 是从其他组件导入还是手动创建的），你会看到以下提示：

![安装组件名称冲突](~/content/assets/images/dax-package-manager-install-conflict.png)

你有以下选项：

- **是**：将继续安装，且组件中的 UDF 会覆盖模型中的现有 UDF。
- **否**：安装将继续进行，但将跳过组件中存在冲突的 UDF(s)。
- **取消**：取消安装。

---

## 更多资源

- [DaxLib 项目站点](https://daxlib.org)
- [DaxLib GitHub repository](https://github.com/daxlib/daxlib)
- [DAX 用户自定义函数（Microsoft Learn）](https://learn.microsoft.com/en-us/dax/best-practices/dax-user-defined-functions)
- [Tabular Editor 3 中的用户自定义函数](xref:udfs)
