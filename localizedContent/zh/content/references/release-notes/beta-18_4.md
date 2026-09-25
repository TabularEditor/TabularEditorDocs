# Tabular Editor 3 BETA-18.4

> [!IMPORTANT]
> Tabular Editor 已推出新版本。你可以在[这里](https://docs.tabulareditor.com/references/release-notes)找到最新版本。

- 下载 [Tabular Editor 3 BETA-18.4](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-18.4.x86.msi)
- 下载 [Tabular Editor 3 BETA-18.4（64 位）](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-18.4.x64.msi)

## BETA-18.4 中的新功能：

- Tabular Editor 3 现在会在个人 .tmuo 文件中存储（加密的）数据源凭据。在使用 Workspace 数据库时，这种方式非常理想，因为这样你就可以指定一组与 Model.bim 文件中定义的凭据不同的凭据。如果你使用版本控制，请确保忽略 .tmuo 扩展名。尽管文件中的凭据已使用 Windows 用户密钥加密，但设计思路是让每位开发人员都拥有自己的 .tmuo 文件，其中包含仅对其本人适用的凭据和偏好，因此此文件不应纳入版本控制。
- Tabular Editor 3 现在会在部署操作期间提示将被覆盖的凭据，因此部署后你无需再通过其他工具设置凭据。注意，Power Query 数据源的凭据在部署过程中总会被清除，因此这类数据源的凭据每次部署时都必须重新输入。
- 创建新模型时，你现在可以选择立即连接到 Workspace 数据库（推荐）。

## BETA-18.4 的 Bug 修复：

- 修复了键盘快捷键和某些操作（撤销/重做等）在不同编辑器之间切换焦点时并不总是可用的问题。
- “查找/替换”对话框现在有最小尺寸，以避免出现滚动条。

## BETA-18.3 的 Bug 修复：

- 改进了大型模型上的语义分析器性能（BETA-18.x 中的回归问题）
- 将数据刷新操作加入队列时，界面不应再冻结
- 键盘按键（左右箭头以及用于重命名的 F2）现在又可以用来在 Tabular Explorer 树形结构中导航了

## BETA-18.2 的 Bug 修复：

- DAX 解析器现在能正确识别包含双引号的对象名称（见问题 #22）。

## BETA-18.1 中的新功能：

- 从 Power Query 数据源更新表架构（见下文）

## BETA-18.1 中的 Bug 修复：

- Tabular Editor 现在会在版本升级之间保留皮肤设置
- 修复了 Lineage tag 相关问题：复制计算表格或计算组表时可能导致崩溃
- 修复了 COALESCE 和 COMBINEVALUES DAX 函数的误报
- 在发行包中加入了 Microsoft.AnalysisServices.dll，从而确保 Tabular Editor 能正确导入/导出 VPAX 文件
- Tabular Editor 现在会在数据刷新时自动重新连接到 AS

## 从 Power Query 源更新表架构

Tabular Editor 3 Beta 版迎来新版本。而我对这个功能真的很兴奋，原因只有一个：

Tabular Editor 首次能够检测 Power Query 数据源和分区的架构更改。而且不仅适用于关系型数据源，也适用于任何可由你的 Analysis Services 引擎求值的 Power Query 表达式。“这到底是怎么做到的？！”你可能会这么想。那么，仔细看最后那句话：“任何可由你的 Analysis Services 引擎求值的 Power Query 表达式”。

关于 Analysis Services 引擎，一个鲜为人知的事实是：它其实是一个事务型系统。这意味着，我们可以针对已部署到 Analysis Services 的数据库启动一个事务，进行一些元数据更改、刷新一些数据、查询一些数据，最后再回滚该事务，使数据库恢复到原始状态，就像我们根本没有动过它一样。

因此，为了检测 Power Query 分区的架构更改，Tabular Editor 3 现在会在模型中添加一个隐藏的临时表，并对我们要检测架构的源查询运行 M 函数 [`Table.Schema`](https://docs.microsoft.com/en-us/powerquery-m/table-schema)，将结果写入该表。然后，该临时表会在服务器上刷新（使用服务器上现有的凭据访问数据源）——由于 M 引擎内部发生了查询折叠，这次刷新只需一瞬间。最后，Tabular Editor 会查询该表以读取架构，然后回滚整个事务。结果：

![image](~/content/assets/images/beta-18-3-01.gif)

当然，唯一要注意的是 Tabular Editor 3 必须连接到一个 Analysis Services 实例。不过你正在处理的模型有没有数据都不重要——只要数据源的凭据已存储在 AS 中（并且 AS 确实能访问该数据源）。如果你使用 Tabular Editor 3 的[工作区模式](https://docs.tabulareditor.com/Workspace-Database.html)，这种技术尤其有用。

除了检测列名和数据类型外，Tabular Editor 3 还可以让你用源中的值更新 Description 属性（如果有的话）。对于 SQL Server 源，这指的是 MS_Description 扩展属性。如果源中的某一列被重命名，它会在“应用架构更改”对话框中显示为一次列导入和一次列删除。但是，如上面的 GIF 所示，如果你按住 Ctrl 键并右键单击这两项架构更改，就可以将它们合并成一项“重命名源列”架构更改。这种方法的好处是，Tabular Editor 3 会自动更新任何引用已重命名列的 DAX 表达式。

### 本版本的限制：

- 当 Tabular Editor 连接到 Analysis Services 实例时，架构比较选项仅适用于 Power Query 分区
- 离线时的架构比较仅适用于旧版（提供程序）分区，类似于 Tabular Editor 2.X。不过，BETA-18.1 中尚未包含此功能，因为我目前首先想收集关于 Power Query 分区架构比较的反馈。该功能和“导入表向导”都将在下一版 Beta 中提供。
- 此功能也可用于 Power BI Desktop 模型，但请注意，在表上添加/修改/删除列并不属于[外部工具支持的建模操作](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-external-tools#data-modeling-operations)。另外请注意，Power BI Desktop 可能会缓存某些类型数据源的元数据，因此在 Tabular Editor 能识别到架构更改之前，你可能需要先在 Power BI Desktop 中执行一次刷新。
