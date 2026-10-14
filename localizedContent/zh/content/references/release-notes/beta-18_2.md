# Tabular Editor 3 BETA-18.2 发布说明

> [!IMPORTANT]
> Tabular Editor 已推出新版本。你可以在[这里](https://docs.tabulareditor.com/references/release-notes)查看最新版本。

- 下载 [Tabular Editor 3 BETA-18.2](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-18.2.x86.msi)
- 下载 [Tabular Editor 3 BETA-18.2（64 位）](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-18.2.x64.msi)

## BETA-18.2 缺陷修复：

- DAX 解析器现在能正确识别包含双引号的对象名称（参见问题 #22）。

## BETA-18.1 中的新功能：

- 从 Power Query 源更新表架构（见下文）

## BETA-18.1 缺陷修复：

- Tabular Editor 现在会在升级之间保留主题设置
- 修复了与 Lineage tag 相关的一个问题：复制计算表格或计算组表时会导致崩溃
- 修复了 COALESCE 和 COMBINEVALUES DAX 函数的误报
- 在发行包中包含 Microsoft.AnalysisServices.dll，从而确保 Tabular Editor 能正确导入/导出 VPAX 文件
- 为进行数据刷新，Tabular Editor 现在会自动重新建立到 AS 的连接

## 从 Power Query 源更新表架构

Tabular Editor 3 Beta 迎来了新版本。而我之所以对这一点特别兴奋，只有一个原因：

Tabular Editor 首次能够检测 Power Query 数据源和分区的架构更改。而且这不仅适用于关系型数据源，也适用于你的 Analysis Services 引擎能够求值的任何 Power Query 表达式。你可能会想：“这到底是怎么可能的？！”。请仔细留意上一句中的这段话：“你的 Analysis Services 引擎能够求值的任何 Power Query 表达式”。

关于 Analysis Services 引擎，有个不太为人所知的事实：它其实是一个事务型系统。这意味着，我们可以针对一个已经部署到 Analysis Services 的数据库启动事务，进行一些元数据更改、刷新部分数据、查询一些数据，最后再回滚事务，让数据库恢复到原始状态，就像我们根本没有动过它一样。

因此，为了检测 Power Query 分区的架构更改，Tabular Editor 3 现在会向模型中添加一张隐藏的临时表，并在需要检测架构的源查询上使用 M 函数 [`Table.Schema`](https://docs.microsoft.com/en-us/powerquery-m/table-schema) 来填充该表。随后，服务器会刷新该临时表（使用服务器上已有的凭据访问数据源）——得益于 M 引擎内部的查询折叠，这次刷新几乎在眨眼间完成。最后，Tabular Editor 会查询该表以读取架构，然后回滚整个事务。结果如下：

![image](https://github.com/TabularEditor3/PublicPreview/blob/master/update%20schema.gif?raw=true)

当然，唯一的前提是 Tabular Editor 3 必须连接到某个 Analysis Services 实例。但你正在处理的模型是否包含任何数据并不重要——只要数据源的凭据已存储在 AS 中（并且 AS 确实能够访问该数据源）。如果你使用 Tabular Editor 3 的[工作区模式](https://docs.tabulareditor.com/Workspace-Database.html)，这种方法尤其有用。

除了检测列名和数据类型之外，Tabular Editor 3 还可以让你从源端更新 Description 属性（如果有的话）。对于 SQL Server 源，这就是 MS_Description 扩展属性。如果源端某列被重命名，它会在“应用架构更改”对话框中显示为两项更改：“导入列”和“删除列”。不过，如上面的 GIF 所示，如果你对这两项架构更改执行 Ctrl+右键单击，就可以将它们合并为一项“重命名源列”架构更改。这种做法的好处是，Tabular Editor 3 会自动修正所有引用了已重命名列的 DAX 表达式。

### 此版本的限制：

- 当 Tabular Editor 连接到某个 Analysis Services 实例时，“架构比较”选项仅适用于 Power Query 分区
- 离线状态下的架构比较仅适用于 Legacy（Provider）分区，类似于 Tabular Editor 2.X。不过，BETA-18.1 中不包含此功能，因为现阶段我主要想先收集大家对 Power Query 分区架构比较功能的反馈。此功能和“导入表向导”都会在下一个 Beta 版本中提供。
- 此功能也可用于 Power BI Desktop 中的模型，但要注意：在表中添加/修改/删除列并不属于 [External Tools 支持的建模操作](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-external-tools#data-modeling-operations)。另外，要注意，Power BI Desktop 可能会缓存某些类型数据源的元数据，因此你可能需要先在 Power BI Desktop 里刷新一次，Tabular Editor 才能识别这些架构更改。
