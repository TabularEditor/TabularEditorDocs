# Tabular Editor 3 BETA-18.3

> [!IMPORTANT]
> Tabular Editor 有新版本可用。 你可以在[这里](https://docs.tabulareditor.com/references/release-notes)找到最新版本。

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

Tabular Editor 3 beta 发布新版本了。 而我对这个版本格外期待，原因只有一个：

这是 Tabular Editor 首次能够检测 Power Query 数据源和分区的架构更改。 而且不只是针对关系型数据源，而是针对 Analysis Services 引擎可计算的任何 Power Query 表达式。 “这到底怎么可能？！”你可能会这么想。 请特别留意最后一句话：“任何可由 Analysis Services 引擎评估的 Power Query 表达式”。

关于 Analysis Services 引擎，有一个鲜为人知的事实：它实际上是一个事务型系统。 这意味着，我们可以对一个已部署到 Analysis Services 的数据库启动事务，做一些元数据更改、刷新部分数据、查询部分数据，然后最终回滚事务，让数据库恢复到原始状态，就像我们根本没有动过它一样。

因此，为了检测 Power Query 分区的架构变化，Tabular Editor 3 现在会在模型中添加一个隐藏的临时表，并对我们要检测其架构的源查询使用 M 函数 [`Table.Schema`](https://docs.microsoft.com/en-us/powerquery-m/table-schema) 来填充该表。 然后，这个临时表会在服务器上刷新（使用服务器上现有的凭据来访问数据源）——由于在 M 引擎内部进行了查询折叠，这次刷新只需瞬间即可完成。 最后，Tabular Editor 会查询该表以读取架构，然后回滚整个事务。 结果如下：

![image](https://github.com/TabularEditor/TabularEditor3/blob/master/media/update%20schema.gif?raw=true)

唯一需要注意的是：Tabular Editor 3 必须连接到一个 Analysis Services 实例。不过，你正在处理的模型是否包含任何数据并不重要——只要数据源的凭据存储在 AS 中（并且 AS 确实能够访问该数据源）即可。 如果你使用 Tabular Editor 3 的[工作区模式](https://docs.tabulareditor.com/Workspace-Database.html)，这种技术尤其有用。

除了检测列名和数据类型之外，Tabular Editor 3 还允许你从源端更新 Description 属性（如果源端提供）。 在 SQL Server 数据源上，这对应的是 MS_Description 扩展属性。 如果源端对某一列进行了重命名，它会在“应用架构更改”对话框中显示为一次“导入列”和一次“删除列”。 不过，如上面的 GIF 所示，如果你按住 Ctrl 键并右键单击这两项架构更改，就可以将它们合并为单个“重命名源列”的架构更改。 这种做法的优势在于，Tabular Editor 3 会自动修复所有引用了已重命名列的 DAX 表达式。

### 此版本的限制：

- 只有当 Tabular Editor 连接到 Analysis Services 实例时，“架构比较”选项才适用于 Power Query 分区
- 离线状态下的架构比较仅适用于传统（Provider）分区，与 Tabular Editor 2.X 类似。 但该功能未包含在 BETA-18.1 中，因为我目前主要希望先收集关于 Power Query 分区架构比较的反馈。 该功能以及“导入表向导”都将在下一个 Beta 版本中提供。
- 该功能也可用于 Power BI Desktop 模型，但要注意，对表执行添加/修改/删除列，并不在[外部工具受支持的建模操作](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-external-tools#data-modeling-operations)之列。 另外，要注意 Power BI Desktop 可能会对某些类型的数据源缓存元数据，因此你可能需要先在 Power BI Desktop 中执行一次刷新，Tabular Editor 才能检测到架构更改。
