# Tabular Editor 3 BETA-18.3

> [!IMPORTANT]
> Tabular Editor 已推出新版本。你可以在[这里](https://docs.tabulareditor.com/references/release-notes)找到最新版本。

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

Tabular Editor 3 beta 发布新版本了。而我之所以对这个功能特别兴奋，是因为一个特别的原因：

Tabular Editor 首次能够检测 Power Query 数据源和分区的架构更改。而且不仅适用于关系型数据源，也适用于你的 Analysis Services 引擎可计算的任何 Power Query 表达式。“这怎么可能？！”你可能会这么想。那么，请特别留意最后这句话：“你的 Analysis Services 引擎可计算的任何 Power Query 表达式”。

关于 Analysis Services 引擎，有一个鲜为人知的事实：它实际上是一个事务型系统。这意味着，我们可以针对一个已经部署到 Analysis Services 的数据库启动事务，进行一些元数据更改、刷新一些数据、查询一些数据，最后再回滚事务，让数据库恢复到原始状态，仿佛我们根本没有动过它。

因此，为了检测 Power Query 分区的架构变化，Tabular Editor 3 现在会在模型中添加一个隐藏的临时表，并对我们要检测其架构的源查询使用 M 函数 [`Table.Schema`](https://docs.microsoft.com/en-us/powerquery-m/table-schema) 来填充该表。随后，这个临时表会在服务器上刷新（使用服务器上已有的凭据访问数据源）——由于 M 引擎内部发生了查询折叠，这次刷新只需一瞬间。最后，Tabular Editor 会查询该表以读取架构，然后回滚整个事务。结果如下：

![图片](~/content/assets/images/beta-18-3-01.gif)

唯一需要注意的是：Tabular Editor 3 必须连接到一个 Analysis Services 实例。不过，你正在处理的模型是否包含任何数据并不重要——只要数据源的凭据存储在 AS 中（并且 AS 确实能够访问该数据源）即可。如果你使用 Tabular Editor 3 的[工作区模式](https://docs.tabulareditor.com/Workspace-Database.html)，这项技术尤其有用。

除了检测列名和数据类型外，Tabular Editor 3 还允许你从源端更新 Description 属性（如果有）。对于 SQL Server 源，这就是 MS_Description 扩展属性。如果源中的某列被重命名，它会在“应用架构更改”对话框中显示为“导入列”和“删除列”两项架构更改。不过，正如上面的 GIF 所示，如果你对这两项架构更改执行 Ctrl+右键单击，就可以把它们合并为一项“重命名源列”的架构更改。这种方法的好处是，Tabular Editor 3 会自动修复所有引用该重命名列的 DAX 表达式。

### 此版本的限制：

- 只有当 Tabular Editor 连接到 Analysis Services 实例时，“架构比较”选项才适用于 Power Query 分区
- 脱机状态下的架构比较将仅适用于 Legacy（提供程序）分区，这与 Tabular Editor 2.X 类似。不过，BETA-18.1 还不包含此功能，因为现阶段我想先收集大家对 Power Query 分区架构比较功能的反馈。该功能和“导入表向导”都会在下一个 Beta 版本中提供。
- 该功能也可用于 Power BI Desktop 模型，但要注意，对表执行添加/修改/删除列，并不在[外部工具受支持的建模操作](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-external-tools#data-modeling-operations)之列。另外，要注意，Power BI Desktop 可能会缓存某些类型数据源的元数据，因此你可能需要先在 Power BI Desktop 中刷新一次，Tabular Editor 才能检测到这些架构更改。
