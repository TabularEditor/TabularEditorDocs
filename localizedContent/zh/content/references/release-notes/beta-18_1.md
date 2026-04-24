# Tabular Editor 3 BETA-18.1

> [!IMPORTANT]
> 已有更新版本的 Tabular Editor 可用。 你可以在[这里](https://docs.tabulareditor.com/references/release-notes)找到最新版本。 你可以在[这里](https://docs.tabulareditor.com/references/release-notes)找到最新版本。

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

Tabular Editor 3 Beta 新版本现已发布。 而我对这个版本尤其期待，原因只有一个： 而我对这个版本尤其期待，原因只有一个：

Tabular Editor 首次可以检测 Power Query 数据源和分区上的架构更改。 而且不仅适用于关系型数据源，还适用于任何可由你的 Analysis Services 引擎求值的 Power Query 表达式。 “这到底怎么可能？！”你可能会这么想。 那么，请特别留意上一句里的这段话：“任何可由你的 Analysis Services 引擎求值的 Power Query 表达式”。 而且不仅适用于关系型数据源，还适用于任何可由你的 Analysis Services 引擎求值的 Power Query 表达式。 “这到底怎么可能？！”你可能会这么想。 那么，请特别留意上一句里的这段话：“任何可由你的 Analysis Services 引擎求值的 Power Query 表达式”。

关于 Analysis Services 引擎，有个不太为人所知的事实：它其实是一个事务型系统。 这意味着，我们可以对一个已部署到 Analysis Services 的数据库开启事务，进行一些元数据更改、刷新部分数据、查询一些数据，然后在最后回滚整个事务，使数据库恢复到原始状态，就像我们从未动过它一样。 这意味着，我们可以对一个已部署到 Analysis Services 的数据库开启事务，进行一些元数据更改、刷新部分数据、查询一些数据，然后在最后回滚整个事务，使数据库恢复到原始状态，就像我们从未动过它一样。

因此，为了检测 Power Query 分区的架构更改，Tabular Editor 3 现在会向模型添加一个隐藏的临时表，并在需要检测架构的源查询上使用 M 函数 [`Table.Schema`](https://docs.microsoft.com/en-us/powerquery-m/table-schema) 来填充该表。 然后，在服务器上刷新该临时表（使用服务器上已存在的凭据来访问数据源）——得益于在 M 引擎内部发生的查询折叠，这次刷新只需片刻。 最后，Tabular Editor 会查询该表以读取架构，然后回滚整个事务。 结果： 然后，在服务器上刷新该临时表（使用服务器上已存在的凭据来访问数据源）——得益于在 M 引擎内部发生的查询折叠，这次刷新只需片刻。 最后，Tabular Editor 会查询该表以读取架构，然后回滚整个事务。 结果：

![image](https://github.com/TabularEditor3/PublicPreview/blob/master/update%20schema.gif?raw=true)

当然，唯一需要注意的是，Tabular Editor 3 必须连接到 Analysis Services 实例。但你正在处理的模型是否包含数据并不重要——只要数据源的凭据已存储在 AS 中（并且 AS 确实能够访问该数据源）即可。 如果你使用 Tabular Editor 3 的 [工作区模式](https://docs.tabulareditor.com/Workspace-Database.html)，这种方法尤其有用。 如果你使用 Tabular Editor 3 的 [工作区模式](https://docs.tabulareditor.com/Workspace-Database.html)，这种方法尤其有用。

除了检测列名和数据类型之外，Tabular Editor 3 还支持从源端更新 Description 属性（如果存在）。 对于 SQL Server 数据源，这对应于 MS_Description 扩展属性。 如果源中的某一列被重命名，它会在“应用架构更改”对话框中显示为一次“导入列”和一次“移除列”。 不过，如上面的 GIF 所示，如果你在这两项架构更改上按 Ctrl+右键单击，就可以将它们合并为一项“重命名源列”的架构更改。 这种方法的好处是，Tabular Editor 3 会自动修正所有引用了已重命名列的 DAX 表达式。

### 此版本的限制：

- 只有当 Tabular Editor 连接到 Analysis Services 实例时，“架构比较”选项才可用于 Power Query 分区
- 离线状态下的架构比较仅适用于传统（Provider）分区，类似于 Tabular Editor 2.X。 不过，这项功能未包含在 BETA-18.1 中，因为我目前主要希望先收集关于 Power Query 分区架构比较的反馈。 此功能以及“导入表向导”将在下一个 Beta 版本中提供。
- 此功能也可用于 Power BI Desktop 模型，但要注意：在表上添加/修改/删除列不属于 [External Tools 支持的建模操作](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-external-tools#data-modeling-operations)。 另外要注意，Power BI Desktop 可能会缓存某些类型数据源的元数据，因此你可能需要先在 Power BI Desktop 中执行一次刷新，Tabular Editor 才能获取到这些架构更改。 另外要注意，Power BI Desktop 可能会缓存某些类型数据源的元数据，因此你可能需要先在 Power BI Desktop 中执行一次刷新，Tabular Editor 才能获取到这些架构更改。
