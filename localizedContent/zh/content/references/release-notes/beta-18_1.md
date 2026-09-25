# Tabular Editor 3 BETA-18.1

> [!IMPORTANT]
> Tabular Editor 已推出新版本。 You can find the latest version [here](https://docs.tabulareditor.com/references/release-notes).

- 下载 [Tabular Editor 3 BETA-18.1](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-18.1.x86.msi)
- 下载 [Tabular Editor 3 BETA-18.1（64 位）](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-18.1.x64.msi)

## 此版本的新功能：

- 从 Power Query 源更新表架构（见下文）

## 此版本的 Bug 修复：

- Tabular Editor 现在会在版本升级间保留界面皮肤设置
- 修复了因 Lineage tag 导致的崩溃问题：复制计算表格或计算组表时会崩溃
- 修复了 COALESCE 和 COMBINEVALUES DAX 函数的误报错误
- 发行包中已包含 Microsoft.AnalysisServices.dll，这将确保 Tabular Editor 能正确导入/导出 VPAX 文件
- Tabular Editor 现在会自动重新连接到 AS，以便进行数据刷新

## 从 Power Query 源更新表架构

Tabular Editor 3 Beta 新版本现已发布。 And I'm really excited about this one, for one particular reason:

Tabular Editor 首次可以检测 Power Query 数据源和分区上的架构更改。 And not just for relational data sources, but for ANY Power Query expression that can be evaluated by your Analysis Services engine. "How on earth is that even possible?!?", you might be thinking. Well, pay close attention to that last sentence: "ANY Power Query expression that can be evaluated by your Analysis Services engine".

关于 Analysis Services 引擎，有个不太为人所知的事实：它其实是一个事务型系统。 This means that we can start a transaction against a database that is already deployed on Analysis Services, make some metadata changes, refresh some data, query some data and then finally roll back the transaction, leaving the database in the original state as if we didn't even touch it at all.

因此，为了检测 Power Query 分区的架构更改，Tabular Editor 3 现在会向模型添加一个隐藏的临时表，并在需要检测架构的源查询上使用 M 函数 [`Table.Schema`](https://docs.microsoft.com/en-us/powerquery-m/table-schema) 来填充该表。 Then, that temporary table is refreshed on the server (using the credentials that are already present on the server to access the data source) - this refresh only takes a split second, thanks to query folding happening inside the M engine. Finally, Tabular Editor will query the table to read the schema, before rolling back the entire transaction. The result:

![image](https://github.com/TabularEditor3/PublicPreview/blob/master/update%20schema.gif?raw=true)

当然，唯一需要注意的是，Tabular Editor 3 必须连接到 Analysis Services 实例。但你正在处理的模型是否包含数据并不重要——只要数据源的凭据已存储在 AS 中（并且 AS 确实能够访问该数据源）即可。 This technique is particularly useful if you use Tabular Editor 3's [workspace mode](https://docs.tabulareditor.com/Workspace-Database.html).

In addition to detecting column names and data types, Tabular Editor 3 will also let you update the Description property from the source (if present). On SQL Server sources, this would be the MS_Description extended property. If a column is renamed in the source, it will show up in the Apply Schema Changes dialog as a column import and a column remove. However, as shown in the GIF above, if you Ctrl+Right Click on these two schema changes, you can combine them as a single "rename source column" schema change. The advantage of this approach, is that Tabular Editor 3 will automatically fix up any DAX expressions that reference the renamed column.

### 此版本的限制：

- 只有当 Tabular Editor 连接到 Analysis Services 实例时，“架构比较”选项才可用于 Power Query 分区
- Schema compare while offline will only be available for Legacy (Provider) partitions, similar to Tabular Editor 2.X. However, this functionality is not included in BETA-18.1, as I am initially looking for feedback on schema compare for Power Query partitions. Both this feature and the Import Tables Wizard will be available in the next beta release.
- 此功能也可用于 Power BI Desktop 模型，但要注意：在表上添加/修改/删除列不属于 [External Tools 支持的建模操作](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-external-tools#data-modeling-operations)。 Also, be aware that Power BI Desktop may be caching metadata for certain types of data sources, so you may have to run a refresh within Power BI Desktop before Tabular Editor can pick up the schema changes.
