# Tabular Editor 3 BETA-18.3

> [!IMPORTANT]
> Tabular Editor 已推出新版本。 You can find the latest version [here](https://docs.tabulareditor.com/references/release-notes).

- 下载 [Tabular Editor 3 BETA-18.3](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-18.3.x86.msi)
- 下载 [Tabular Editor 3 BETA-18.3（64 位）](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-18.3.x64.msi)

## BETA-18.3 修复内容：

- 提升了大型模型上的语义分析器性能（BETA-18.x 中的回归问题）
- 将数据刷新操作加入队列时，UI 不会再卡死
- 现在又可以使用键盘按键（左/右方向键，以及用于重命名的 F2）在 Tabular Explorer 树中导航

## BETA-18.2 修复内容：

- DAX 解析器现在能正确识别包含双引号的对象名称（见问题 #22）。

## BETA-18.1 新增功能：

- 从 Power Query 源更新表架构（见下文）

## BETA-18.1 修复内容：

- Tabular Editor 现在会在升级前后保留主题设置
- 修复了与 Lineage tag 相关的一个 Bug：复制计算表格或计算组表时可能会导致崩溃
- 修复了对 COALESCE 和 COMBINEVALUES DAX 函数的误报错误
- 安装包中已包含 Microsoft.AnalysisServices.dll，这将确保 Tabular Editor 能正确导入/导出 VPAX 文件
- Tabular Editor 现在会在数据刷新时自动重新建立与 AS 的连接

## 从 Power Query 源更新表架构

Tabular Editor 3 beta 发布新版本了。 And I'm really excited about this one, for one particular reason:

Tabular Editor 首次能够检测 Power Query 数据源和分区的架构更改。 And not just for relational data sources, but for ANY Power Query expression that can be evaluated by your Analysis Services engine. "How on earth is that even possible?!?", you might be thinking. Well, pay close attention to that last sentence: "ANY Power Query expression that can be evaluated by your Analysis Services engine".

关于 Analysis Services 引擎，有一个鲜为人知的事实：它实际上是一个事务型系统。 This means that we can start a transaction against a database that is already deployed on Analysis Services, make some metadata changes, refresh some data, query some data and then finally roll back the transaction, leaving the database in the original state as if we didn't even touch it at all.

因此，为了检测 Power Query 分区的架构变化，Tabular Editor 3 现在会在模型中添加一个隐藏的临时表，并对我们要检测其架构的源查询使用 M 函数 [`Table.Schema`](https://docs.microsoft.com/en-us/powerquery-m/table-schema) 来填充该表。 Then, that temporary table is refreshed on the server (using the credentials that are already present on the server to access the data source) - this refresh only takes a split second, thanks to query folding happening inside the M engine. Finally, Tabular Editor will query the table to read the schema, before rolling back the entire transaction. The result:

![image](~/content/assets/images/beta-18-3-01.gif)

唯一需要注意的是：Tabular Editor 3 必须连接到一个 Analysis Services 实例。不过，你正在处理的模型是否包含任何数据并不重要——只要数据源的凭据存储在 AS 中（并且 AS 确实能够访问该数据源）即可。 This technique is particularly useful if you use Tabular Editor 3's [workspace mode](https://docs.tabulareditor.com/Workspace-Database.html).

In addition to detecting column names and data types, Tabular Editor 3 will also let you update the Description property from the source (if present). On SQL Server sources, this would be the MS_Description extended property. If a column is renamed in the source, it will show up in the Apply Schema Changes dialog as a column import and a column remove. However, as shown in the GIF above, if you Ctrl+Right Click on these two schema changes, you can combine them as a single "rename source column" schema change. The advantage of this approach, is that Tabular Editor 3 will automatically fix up any DAX expressions that reference the renamed column.

### 此版本的限制：

- 只有当 Tabular Editor 连接到 Analysis Services 实例时，“架构比较”选项才适用于 Power Query 分区
- Schema compare while offline will only be available for Legacy (Provider) partitions, similar to Tabular Editor 2.X. However, this functionality is not included in BETA-18.1, as I am initially looking for feedback on schema compare for Power Query partitions. Both this feature and the Import Tables Wizard will be available in the next beta release.
- 该功能也可用于 Power BI Desktop 模型，但要注意，对表执行添加/修改/删除列，并不在[外部工具受支持的建模操作](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-external-tools#data-modeling-operations)之列。 Also, be aware that Power BI Desktop may be caching metadata for certain types of data sources, so you may have to run a refresh within Power BI Desktop before Tabular Editor can pick up the schema changes.
