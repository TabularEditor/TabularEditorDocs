# Tabular Editor 3 BETA-18.4

> [!IMPORTANT]
> Tabular Editor 已推出新版本。 You can find the latest version [here](https://docs.tabulareditor.com/references/release-notes).

- 下载 [Tabular Editor 3 BETA-18.4](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-18.4.x86.msi)
- 下载 [Tabular Editor 3 BETA-18.4（64 位）](https://cdn.tabulareditor.com/files/TabularEditor.3.BETA-18.4.x64.msi)

## BETA-18.4 中的新功能：

- Tabular Editor 3 现在会在个人 .tmuo 文件中存储（加密的）数据源凭据。 This is ideal when using a workspace database, as you can then specify a set of credentials different from those defined in the Model.bim file. If you're using version control, make sure to ignore the .tmuo extension. Even though the credentials in the file are encrypted with the Windows user key, the idea is that each developer can have their own .tmuo file containing credentials and preferences that apply only for them, and therefore this file should not be included in version control.
- Tabular Editor 3 现在会在部署操作期间提示将被覆盖的凭据，因此部署后你无需再通过其他工具设置凭据。 Please note that Power Query data sources will always have their credentials wiped during a deployment operation, so credentials for these types of data sources must be entered upon every deployment.
- 创建新模型时，你现在可以选择立即连接到 Workspace 数据库（推荐）。

## BETA-18.4 的 Bug 修复：

- Fixed an issue with keyboard shortcuts and certain actions (Undo/Redo, etc.) not always being enabled when switching the focus between different editors.
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

Tabular Editor 3 Beta 版迎来新版本。 And I'm really excited about this one, for one particular reason:

Tabular Editor 首次能够检测 Power Query 数据源和分区的架构更改。 And not just for relational data sources, but for ANY Power Query expression that can be evaluated by your Analysis Services engine. "How on earth is that even possible?!?", you might be thinking. Well, pay close attention to that last sentence: "ANY Power Query expression that can be evaluated by your Analysis Services engine".

关于 Analysis Services 引擎，一个鲜为人知的事实是：它其实是一个事务型系统。 This means that we can start a transaction against a database that is already deployed on Analysis Services, make some metadata changes, refresh some data, query some data and then finally roll back the transaction, leaving the database in the original state as if we didn't even touch it at all.

因此，为了检测 Power Query 分区的架构更改，Tabular Editor 3 现在会在模型中添加一个隐藏的临时表，并对我们要检测架构的源查询运行 M 函数 [`Table.Schema`](https://docs.microsoft.com/en-us/powerquery-m/table-schema)，将结果写入该表。 Then, that temporary table is refreshed on the server (using the credentials that are already present on the server to access the data source) - this refresh only takes a split second, thanks to query folding happening inside the M engine. Finally, Tabular Editor will query the table to read the schema, before rolling back the entire transaction. The result:

![image](~/content/assets/images/beta-18-3-01.gif)

当然，唯一要注意的是 Tabular Editor 3 必须连接到一个 Analysis Services 实例。不过你正在处理的模型有没有数据都不重要——只要数据源的凭据已存储在 AS 中（并且 AS 确实能访问该数据源）。 This technique is particularly useful if you use Tabular Editor 3's [workspace mode](https://docs.tabulareditor.com/Workspace-Database.html).

In addition to detecting column names and data types, Tabular Editor 3 will also let you update the Description property from the source (if present). On SQL Server sources, this would be the MS_Description extended property. If a column is renamed in the source, it will show up in the Apply Schema Changes dialog as a column import and a column remove. However, as shown in the GIF above, if you Ctrl+Right Click on these two schema changes, you can combine them as a single "rename source column" schema change. The advantage of this approach, is that Tabular Editor 3 will automatically fix up any DAX expressions that reference the renamed column.

### 本版本的限制：

- 当 Tabular Editor 连接到 Analysis Services 实例时，架构比较选项仅适用于 Power Query 分区
- Schema compare while offline will only be available for Legacy (Provider) partitions, similar to Tabular Editor 2.X. However, this functionality is not included in BETA-18.1, as I am initially looking for feedback on schema compare for Power Query partitions. Both this feature and the Import Tables Wizard will be available in the next beta release.
- 此功能也可用于 Power BI Desktop 模型，但请注意，在表上添加/修改/删除列并不属于[外部工具支持的建模操作](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-external-tools#data-modeling-operations)。 Also, be aware that Power BI Desktop may be caching metadata for certain types of data sources, so you may have to run a refresh within Power BI Desktop before Tabular Editor can pick up the schema changes.
