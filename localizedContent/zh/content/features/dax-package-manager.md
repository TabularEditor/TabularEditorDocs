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

## 概览

Tabular Editor 中的 **DAX 组件管理器**（DPM）使用户能够直接在应用内轻松发现、安装、更新并管理 [DAX 用户自定义函数（UDF）](xref:udfs) 库（称为 DAX 组件）。  
These libraries extend your DAX capabilities with reusable functions, making it easier to build consistent and maintainable Power BI semantic models.

As the name suggests, this feature acts like a package manager similar to how NuGet or npm manage code libraries for developers. DAX 组件来源于 https://daxlib.org，这是由 [SQLBI](https://sqlbi.com) 创建的开源非营利项目。

只要模型支持 DAX 用户自定义函数，你就可以使用 DAX 组件管理器；也就是说，模型的兼容级别必须为 1702 或更高。

> [!WARNING]
> DAX 用户自定义函数目前（截至 2025 年十一月）是 Power BI 的预览功能。 Consider their [limitations](https://learn.microsoft.com/en-us/dax/best-practices/dax-user-defined-functions#considerations-and-limitations) before use.

---

![DAX 组件管理器](~/content/assets/images/dax-package-manager-overview.png)

## 界面布局

### 1. 启动 DAX 组件管理器

You can open the DPM panel through the **View** menu. 你也可以通过 **工具 > 偏好 > 键盘** 为 `View.DaxPackageManager` 命令分配自定义快捷键。

- **菜单：** `视图 → DAX 组件管理器`
- **快捷键：** _(如果已在偏好设置中分配)_

---

### 2. Package lists

On the left of the screen, you'll find the following three tabs. Each tab is accompanied by a list of packages relevant to its context:

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

### 3。 Search bar

Enter your search keywords or the (partial) name of the package, to filter the list of items to only those that match the search terms. This feature applies to all three tabs, i.e., **Browse**, **Installed**, and **Updates**.

> [!NOTE]
> We currently only show the top 20 packages matching the search criteria. There is no pagination feature yet - this will come in a future update. If you need to browse all available packages, go to the source, e.g. https://daxlib.org.

---

### 4. Package Detail Pane

选择某个组件后，会显示详细信息：

| 字段                 | 说明                                    |
| ------------------ | ------------------------------------- |
| **已安装 / 版本**       | 当前版本及可用更新信息。                          |
| **说明**             | 该库提供内容的摘要。                            |
| **发布说明**           | 关于最新版本中新功能或变更的信息。                     |
| **提供方 / 所有者 / 作者** | Attribution metadata. |
| **标签**             | 便于分类和搜索。                              |
| **URL**            | 项目文档、API 以及 GitHub repository 的直接链接。  |
| **发布日期**           | 当前版本发布的时间戳。                           |
| **下载量**            | 所有用户的总安装次数。                           |

A package that is not installed, will show an **“Install”** button. Clicking this button will instantly add the UDFs in the package to your model.

已安装的组件会显示 **“移除”** 按钮。

有新版本可用的组件会显示 **“更新”** 按钮。

> [!WARNING]
> 如果你移除或更新某个组件，而你曾修改过其中一个或多个 UDF 的 DAX 表达式，你会看到一条警告信息，提示这些更改将会丢失。

---

### 5. 更新通知

打开使用了有可用更新的组件的模型时，你会在 **TOM Explorer** 底部看到更新通知。

点击更新通知，或打开 DAX 组件管理器视图，即可查看并安装更新。

---

## 安装组件

1. 打开 **DAX 组件管理器**。
2. 在 **浏览** 选项卡中，选择一个组件（例如 `DaxLib.SVG`）。 Use the search bar to refine the search as needed.
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
> 移除 UDF 可能会导致模型中其他位置（度量值、计算列等）的 DAX 表达式 to become invalid. If this happens, you can always hit **Undo** (Ctrl+Z) to undo the package removal. Use the **Show dependencies** (Shift+F12) feature to identify where the UDFs are used before removing a package.

---

## 技术注意事项

DAX 组件管理器使用 [扩展属性](https://learn.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.extendedproperty?view=analysisservices-dotnet) 来跟踪已安装的组件。 Extended properties are similar to annotations, but are better suited for storing custom metadata in JSON format.

DAX 组件管理器会在 **Model** 对象上创建以下扩展属性：

| 属性名称                             | 说明                                                                                                                                                                                                |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TabularEditor_ModelDaxPkgTable` | 一个 JSON 字典，每个已安装的组件对应一个条目。 The key is a sequential integer, while the value contains information about the package provider, package ID within the provider, and package version. |
| `TabularEditor_ModelDaxPkgSeq`   | An integer value that is incremented each time a package is installed. This is used to generate unique keys for the `TabularEditor_ModelDaxPkgTable` property.    |

此外，通过 DAX 组件管理器导入的每个 UDF 都会被赋予以下扩展属性：

| 属性名称                                 | 说明                                                                                                                                                                            |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TabularEditor_ObjDaxPkgHandle`      | 一个整数值，对应模型上 `TabularEditor_ModelDaxPkgTable` 属性中的键。 This allows Tabular Editor to identify which package a UDF belongs to.                                    |
| `TabularEditor_ObjDaxPkgContentHash` | 一个哈希值，在安装时根据该 UDF 的 DAX 表达式计算得出。 This is used to detect if a UDF has been modified since installation, which is important when updating or removing packages. |

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
> 如果你想将现有 UDF 与 DAX 组件管理器“取消关联”，请从 UDF 对象中删除扩展属性 `TabularEditor_ObjDaxPkgHandle` 和 `TabularEditor_ObjDaxPkgContentHash`。 This way, the DAX Package Manager will no longer track these UDFs, and they will not be affected by future package updates or removals. However, you still need to be aware of name conflicts.

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
