# SQL Server 2017 支持

从 2.3 版本开始，Tabular Editor 也支持 SQL Server 2017（兼容级别 1400）。 从 2.3 版本开始，Tabular Editor 也支持 SQL Server 2017（兼容级别 1400）。 这意味着 Tabular Editor 的界面现已支持[这里](https://blogs.msdn.microsoft.com/analysisservices/2017/04/19/whats-new-in-sql-server-2017-ctp-2-0-for-analysis-services/)中介绍的部分新功能。

但请注意，要使用这些功能，你需要下载[Tabular Editor 的正确构建版本](https://github.com/TabularEditor/TabularEditor/releases/tag/2.5-CL1400)。 但请注意，要使用这些功能，你需要下载[Tabular Editor 的正确构建版本](https://github.com/TabularEditor/TabularEditor/releases/tag/2.5-CL1400)。 原因是：Microsoft 为 SQL Server 2017 / SSDT 17.0 提供了一组新的客户端库，而这些库与面向 SQL Server 2016 构建的 Tabular Editor 不兼容。 这些新库可通过新版[SSDT](https://docs.microsoft.com/en-us/sql/ssdt/download-sql-server-data-tools-ssdt)获取（需要 Visual Studio 2015）。 这些新库可通过新版[SSDT](https://docs.microsoft.com/en-us/sql/ssdt/download-sql-server-data-tools-ssdt)获取（需要 Visual Studio 2015）。

如果你不需要兼容级别 1400 的功能，仍然可以使用面向 SQL Server 2016 构建的 [Tabular Editor](https://github.com/TabularEditor/TabularEditor/releases/tag/2.5)。

下面快速介绍一下如何在 Tabular Editor 中使用这些新功能：

## 日期关系

现在，所有关系都会在属性网格中显示“Join on Date Behavior”属性：

![image](https://cloud.githubusercontent.com/assets/8976200/25297821/9dd46be0-26f0-11e7-92bf-10a921ed20dc.png)

## 变体（列/层级重用）

你可以通过在属性网格中展开“Variations”属性来设置列的变体：

![image](https://cloud.githubusercontent.com/assets/8976200/25297845/c69ecc5a-26f0-11e7-93af-b7a2a0cc9310.png)

另外，你也可以在列级别指定 **对象级安全性**。

点击省略号按钮将打开“变体集合编辑器”，你可以在其中配置列和层级在 Power BI 中的呈现方式：

![image](https://cloud.githubusercontent.com/assets/8976200/25297884/fd4faf58-26f0-11e7-9a1a-df7a1b05f663.png)

别忘了在表级别将“Show As Variations Only”属性设置为“True”：

![image](https://cloud.githubusercontent.com/assets/8976200/25297917/2c1e4b64-26f1-11e7-8ce6-a62aef2b7d8a.png)

可直接在表和度量值上设置**详细信息行表达式**。 不过，目前还不支持语法高亮或 IntelliSense。

层级对象新增了**隐藏成员**属性，对参差层级很有用。
