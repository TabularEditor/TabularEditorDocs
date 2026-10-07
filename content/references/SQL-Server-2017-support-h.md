# SQL Server 2017 Support

Starting from version 2.3, Tabular Editor now also supports SQL Server 2017 (Compatibility Level 1400). This means that the Tabular Editor UI exposes some of the new functionality described [here](https://blogs.msdn.microsoft.com/analysisservices/2017/04/19/whats-new-in-sql-server-2017-ctp-2-0-for-analysis-services/).

Please note, however, that you need to download the [proper build of Tabular Editor](https://github.com/TabularEditor/TabularEditor/releases/tag/2.5-CL1400) to use these features. This is because a new set of client libraries are provided by Microsoft for SQL Server 2017 / SSDT 17.0, and these libs are incompatible with the SQL Server 2016-build of Tabular Editor. The new libraries can be obtained through the new [version of SSDT](https://docs.microsoft.com/en-us/sql/ssdt/download-sql-server-data-tools-ssdt) (requires Visual Studio 2015).

If you don't need Compatibility Level 1400 features, you can still use the SQL Server 2016-build of [Tabular Editor](https://github.com/TabularEditor/TabularEditor/releases/tag/2.5).

Here is a quick rundown of how the new features are used in Tabular Editor:

## Date Relationships
All relationships now expose the "Join on Date Behavior" property in the property grid:

![image](~/content/assets/images/sql-server-2017-support-01.png)

## Variations (column/hierarchy reuse)
You can set up variations on a column, by expanding the "Variations" property in the property grid:

![image](~/content/assets/images/sql-server-2017-support-02.png)

Note that you can also specify **Object Level Security** at the column level.

Clicking the ellipsis button opens the Variations Collection Editor, from where you can set up how columns and hierarchies are resurfaced in Power BI:

![image](~/content/assets/images/sql-server-2017-support-03.png)

Remember to set the "Show As Variations Only" property to "True" at the table level:

![image](~/content/assets/images/sql-server-2017-support-04.png)

**Detail Row Expressions** can be set directly on tables and measures. At this time, however, no syntax highlighting or IntelliSense is available.

Hierarchy objects exposes a new **Hide Members** property that is useful for ragged hierarchies.
