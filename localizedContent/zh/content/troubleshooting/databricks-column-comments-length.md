---
uid: databricks-column-comments-length
title: Databricks 列注释长度超限错误
author: 支持团队
updated: 2026-02-06
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

# Databricks 列注释长度超限错误

使用“导入表向导”从 Databricks 导入表时，如果列注释（描述）超过 512 个字符，你可能会遇到连接错误。 这一限制来自 Simba Spark ODBC Driver，尽管 Databricks Unity Catalog 允许更长的列注释。

典型的错误信息如下：

**"Unable to connect to database 'database_name' on 'adb-xxxx.azuredatabricks.net/sql/1.0/warehouses/xxxx': Exception has been thrown by the target of an invocation."**

这篇文章会解释为什么会出现这个问题，并提供两种变通办法来解决它。

---

## 了解问题

Tabular Editor 通过 Simba Spark ODBC Driver 连接到 Databricks，而该驱动对列注释默认限制为 512 个字符。 无论 Databricks Unity Catalog 允许的长度是多少，这个限制都会被强制执行。

### 为什么会这样

1. **驱动程序默认限制**：Simba Spark ODBC Driver 默认配置的 `MaxCommentLen` 参数为 512 个字符。

2. **Unity Catalog 支持更长的注释**：Databricks Unity Catalog 允许列描述超过 512 个字符，因此可能会超出驱动程序的限制。

3. **导入向导读取元数据**：当“导入表向导”查询表元数据时，会尝试读取所有列注释。 只要有任意注释超过驱动程序限制，连接就会因调用异常而失败。

---

## 解决方案

解决此问题有两种方法：

### 方案 1：限制 Databricks 中的列注释长度（推荐，操作最简单）

最简单的方法是确保 Databricks Unity Catalog 表中所有列的描述不超过 512 个字符。

**步骤：**

1. 查看 Databricks 表中的列注释。
2. 找出超过 512 个字符的注释。
3. 将这些注释编辑为不超过 512 个字符。
4. 在 Databricks 中保存更改。
5. 在 Tabular Editor 中重试导入。

**优势：**

- 易于实施
- 无需更改配置
- 适用于所有连接到 Databricks 的工具

**权衡：**

- 需要修改源元数据
- 如果描述被截断，可能会丢失信息
- 如果需要更长的描述，就不适用

### 选项 2：在 Simba Driver 中提高 MaxCommentLen 参数值

如果需要保留超过 512 个字符的列注释，你可以配置 Simba Spark ODBC Driver，使其支持更长的注释。

> [!NOTE]
> 在继续之前，请确保已安装适用于 Databricks 的最新版 Simba Spark ODBC Driver。 你可以从 [Microsoft Azure Databricks ODBC 下载页面](https://learn.microsoft.com/azure/databricks/integrations/odbc/download) 下载。

**步骤：**

1. **找到 Simba Spark ODBC Driver 的安装文件夹。**

   64 位驱动程序的默认安装位置为：

   ```
   C:\Program Files\Simba Spark ODBC Driver\
   ```

   如果你将驱动程序安装到了自定义位置，请改为前往该文件夹。

2. **创建或编辑 microsoft.sparkodbc.ini 文件。**

   在驱动程序安装文件夹中，新建名为 **microsoft.sparkodbc.ini** 的文件（如果尚不存在）。

   > [!NOTE]> Simba Spark ODBC Driver 安装程序默认不会创建此 .ini 文件，因此通常需要你手动创建。

3. **添加 MaxCommentLen 配置项。**

   用文本编辑器（如记事本）打开 **microsoft.sparkodbc.ini** 文件，并添加以下内容：

   ```ini
   [Driver]
   MaxCommentLen=2048
   ```

   根据所需的最大注释长度调整该值（本示例为 2048）。

4. **保存文件。**

   确保将文件保存在驱动程序安装文件夹中，并命名为 **microsoft.sparkodbc.ini**（而不是 microsoft.sparkodbc.ini.txt）。

5. **重新启动 Tabular Editor。**

   关闭所有 Tabular Editor 实例，然后重新打开应用，以使配置更改生效。

6. **重试导入。**

   再次使用“导入表向导”导入 Databricks 表。 提高注释长度上限后，连接应可成功建立。

**优势：**

- 保留完整的列说明
- 无需修改源元数据
- 适用于使用此驱动程序的所有 Databricks 连接

**取舍：**

- 需要访问驱动程序安装文件夹的文件系统权限
- 必须手动创建配置文件
- 更改会在整台机器范围内生效，并影响使用同一驱动程序的其他应用

---

## 分步示例：创建 microsoft.sparkodbc.ini 文件

如果您以前从未创建过 .ini 文件，请按以下详细步骤操作：

1. **打开记事本**（或您常用的文本编辑器）。

2. **输入以下内容：**

   ```ini
   [Driver]
   MaxCommentLen=2048
   ```

3. **保存文件：**
   - 点击 **文件 > 另存为**

   - 转到 `C:\Program Files\Simba Spark ODBC Driver\`

   - 在 **保存类型** 下拉列表中，选择 **所有文件 (_._)**（重要！）

   - 在 **文件名** 字段中，准确输入：**microsoft.sparkodbc.ini**

   - 点击 **保存**
   > [!IMPORTANT]> 一定要把文件类型选为“所有文件”，否则记事本会把它保存为 microsoft.sparkodbc.ini.txt，导致无法使用。

4. **验证文件是否正确创建：**
   - 打开文件资源管理器并转到 `C:\Program Files\Simba Spark ODBC Driver\`
   - 确认你能看到名为 **microsoft.sparkodbc.ini** 的文件（而不是 microsoft.sparkodbc.ini.txt）

5. **关闭并重启 Tabular Editor**，使更改生效。

---

## 快速故障排查清单

- [ ] **确认错误信息**：确认在通过“导入表向导”连接 Databricks 时出现该连接错误。
- [ ] **检查列注释长度**：查询你的 Databricks 表，找出任何超过 512 个字符的列注释。
- [ ] **验证驱动程序安装情况**：确认已安装 Simba Spark ODBC Driver，并找到其安装目录。
- [ ] **检查 .ini 文件位置**：确保 **microsoft.sparkodbc.ini** 文件位于正确的文件夹中（驱动程序安装目录，而不是其子目录）。
- [ ] **验证文件扩展名**：确认文件名为 **microsoft.sparkodbc.ini**，而不是 **microsoft.sparkodbc.ini.txt**。
- [ ] **重启 Tabular Editor**：配置更改只有在重启应用程序后才会生效。

---

## 预防最佳实践

1. **制定注释长度规范**：如果你在管理 Databricks 元数据，建议制定规范，将列注释控制在 512 个字符以内，以获得最佳兼容性。

2. **尽早测试导入**：在搭建新的 Databricks 环境时，尽量在开发初期就用 Tabular Editor 测试表导入，以便尽早发现元数据问题。

3. **记录驱动程序配置**：如果你修改了 **microsoft.sparkodbc.ini** 文件，就在团队的运行手册中记录这次更改，让其他人也知道这项自定义配置。

4. **驱动程序更新后复查**：更新 Simba Spark ODBC Driver 时，记得确认 **microsoft.sparkodbc.ini** 文件仍然存在，因为驱动程序更新可能会覆盖或删除自定义配置文件。

---

## 其他资源

- **[Databricks 知识库 - Unity Catalog 元数据错误](https://kb.databricks.com/unity-catalog/error-when-trying-to-load-a-dataset-after-integrating-unity-catalog-metadata-with-power-bi)**：Databricks 官方文档，介绍此问题以及 MaxCommentLen 参数。
- **[适用于 Azure Databricks 的 Simba Spark ODBC Driver](https://learn.microsoft.com/azure/databricks/integrations/odbc/download)**：下载适用于 Databricks 的最新版 Simba Spark ODBC Driver。
- **[导入表向导](xref:importing-tables)**：详细了解如何在 Tabular Editor 中使用导入表向导。

---

## 还是需要帮助？

如果以上步骤未能解决你的问题：

1. **确认 ODBC 驱动程序版本**：确保已安装最新版本的 Simba Spark ODBC Driver。 你可以从 [Microsoft Azure Databricks ODBC 下载页面](https://learn.microsoft.com/azure/databricks/integrations/odbc/download) 下载。

2. **检查 ODBC 数据源配置**：打开 Windows 的 ODBC 数据源管理器 (odbcad32.exe)，确认你的 Databricks 连接已正确配置。

3. **用更简单的表测试**：尝试导入一张你确定列注释很短（或没有注释）的 Databricks 表，先确认连接本身是否正常。

4. **查看 ODBC 驱动程序日志**：Simba Spark ODBC Driver 可以生成详细日志。 参考驱动程序文档，按说明启用日志记录；日志可能会提供更多诊断信息。

5. **联系支持**：联系 Tabular Editor 支持团队，并提供：
   - 完整的错误信息文本
   - 你的 Databricks 连接详细信息（不含凭据）
   - Simba Spark ODBC Driver 版本
   - 你是否已创建 microsoft.sparkodbc.ini 文件及其内容
