---
uid: script-create-databricks-relationships
title: 创建 Databricks 关系
author: Johnny Winter
updated: 2026-04-08
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 创建 Databricks 关系

## 脚本用途

此脚本是 Tabular Editor x Databricks 系列的一部分。 在 Unity Catalog 中，可以在表之间定义主键和外键关系。 此脚本可复用这些信息，在 Tabular Editor 中自动检测并创建关系。 在导入这些关系时，脚本还会隐藏主键和外键，并将 IsAvailableInMDX 设为 false（DateTime 类型的主键除外）。 主键也会在语义模型中标记为 IsKey = TRUE。 <br></br>

> [!NOTE]
> 此脚本需要 Databricks ODBC 驱动程序。 我们推荐使用新版 [Databricks ODBC Driver](https://www.databricks.com/spark/odbc-drivers-download)，它将取代旧版 Simba Spark ODBC Driver。 该脚本会自动检测已安装的驱动程序，并自动使用相应的驱动程序。 我们推荐使用新版 [Databricks ODBC Driver](https://www.databricks.com/spark/odbc-drivers-download)，它将取代旧版 Simba Spark ODBC Driver。 该脚本会自动检测已安装的驱动程序，并自动使用相应的驱动程序。

每次运行该脚本时，都会提示用户输入 Databricks 个人访问令牌。 这用于对 Databricks 进行身份验证。
The script utilises the information_schema tables in Unity Catalog to retrieve relationship information, so you may need to double check with your Databricks administrator to make sure you have permission to query these tables. <br></br>

## 脚本

### 创建 Databricks 关系

```csharp
/*
 * 标题：创建 Databricks 关系
 * 作者：Johnny Winter, greyskullanalytics.com
 *
 * 执行这个脚本时，脚本会循环遍历当前选中的表，并向 Databricks Information Schema 表发送查询，以查看是否已定义任何外键。
 * 识别出外键后，脚本会在语义模型中的表之间创建关系。
 * 除 datetime 类型的维度列外，创建关系后将隐藏键列；同时将主键标记为主键，并将 IsAvailableInMDX 设为 false。
 * 步骤 1：在模型中选择一个或多个表。这些表应是在 Unity Catalog 中定义了外键关系的表
            （通常是事实表，但也可能是桥接表或辅助维度表）。
 * 步骤 2：运行这个脚本
 * 步骤 3：在提示时输入 Databricks 个人访问令牌
 * 步骤 4：脚本将连接到 Databricks，并检测所选表中哪些位置存在外键。
            如果该关系在语义模型中尚不存在，则会创建它。
            如果两个表之间已存在关系，则新关系会创建为非活动关系。
            对于处理的每个表，都会显示一个消息框，说明已创建的关系数量。
 *          点击“确定”以继续处理下一个表。
 * 说明：
 *  -   这个脚本需要已安装 Databricks ODBC Driver（推荐）或旧版 Simba Spark ODBC Driver（下载地址：https://www.databricks.com/spark/odbc-drivers-download）
 *  -   脚本会自动检测已安装的驱动程序
 *  -   每次运行这个脚本时，都会提示你输入 Databricks 个人访问令牌
 */
#r "Microsoft.VisualBasic"
using System;
using System.Data.Odbc;
using System.Drawing;
using System.Text.RegularExpressions;
using System.Windows.Forms;
using Microsoft.VisualBasic;
using sysData = System.Data;

//用于输入 Databricks PAT 令牌的掩码输入框代码
public partial class PasswordInputForm : Form
{
    public string Password { get; private set; }

    private TextBox passwordTextBox;
    private Button okButton;
    private Button cancelButton;
    private Label promptLabel;

    public PasswordInputForm(string prompt, string title)
    {
        InitializeComponent(prompt, title);
    }

    private void InitializeComponent(string prompt, string title)
    {
        this.Text = title;
        this.Size = new System.Drawing.Size(4000, 1500);
        this.StartPosition = FormStartPosition.WindowsDefaultLocation;
        this.FormBorderStyle = FormBorderStyle.FixedDialog;
        this.MaximizeBox = false;
        this.MinimizeBox = false;

        // 提示标签
        promptLabel = new Label();
        promptLabel.Text = prompt;
        promptLabel.Location = new System.Drawing.Point(12, 15);
        promptLabel.Size = new System.Drawing.Size(360, 40);
        promptLabel.AutoSize = false;
        this.Controls.Add(promptLabel);

        // 密码文本框
        passwordTextBox = new TextBox();
        passwordTextBox.Location = new System.Drawing.Point(12, 55);
        passwordTextBox.Size = new System.Drawing.Size(360, 20);
        passwordTextBox.UseSystemPasswordChar = true; // 这会隐藏输入内容
        passwordTextBox.KeyPress += (s, e) =>
        {
            if (e.KeyChar == (char)Keys.Return)
            {
                OkButton_Click(null, null);
                e.Handled = true;
            }
        };
        this.Controls.Add(passwordTextBox);

        // 确定按钮
        okButton = new Button();
        okButton.Text = "确定";
        okButton.Location = new System.Drawing.Point(216, 85);
        okButton.Size = new System.Drawing.Size(150, 50);
        okButton.Click += OkButton_Click;
        this.Controls.Add(okButton);

        // 取消按钮
        cancelButton = new Button();
        cancelButton.Text = "取消";
        cancelButton.Location = new System.Drawing.Point(297, 85);
        cancelButton.Size = new System.Drawing.Size(150, 50);
        cancelButton.Click += CancelButton_Click;
        this.Controls.Add(cancelButton);

        // 设置默认按钮和取消按钮
        this.AcceptButton = okButton;
        this.CancelButton = cancelButton;

        // 窗体加载时将焦点放在文本框上
        this.Load += (s, e) => passwordTextBox.Focus();
    }

    private void OkButton_Click(object sender, EventArgs e)
    {
        Password = passwordTextBox.Text;
        this.DialogResult = DialogResult.OK;
        this.Close();
    }

    private void CancelButton_Click(object sender, EventArgs e)
    {
        Password = string.Empty;
        this.DialogResult = DialogResult.Cancel;
        this.Close();
    }

    public static string ShowDialog(string prompt, string title)
    {
        using (var form = new PasswordInputForm(prompt, title))
        {
            if (form.ShowDialog() == DialogResult.OK)
                return form.Password;
            return string.Empty;
        }
    }
}

public static class MaskedInputHelper
{
    public static string GetMaskedInput(string prompt, string title, string defaultValue = "")
    {
        using (var form = new Form())
        {
            form.Text = title;
            form.Size = new System.Drawing.Size(1000, 500);
            form.StartPosition = FormStartPosition.CenterScreen;
            form.FormBorderStyle = FormBorderStyle.FixedDialog;
            form.MaximizeBox = false;
            form.MinimizeBox = false;

            var label = new Label()
            {
                Left = 12,
                Top = 15,
                Size = new System.Drawing.Size(900, 100),
                Text = prompt,
            };
            var textBox = new TextBox()
            {
                Left = 12,
                Top = 150,
                Size = new System.Drawing.Size(900, 100),
                UseSystemPasswordChar = true,
                Text = defaultValue,
            };
            var buttonOk = new Button()
            {
                Text = "确定",
                Size = new System.Drawing.Size(150, 50),
                Left = 12,
                Width = 150,
                Top = 200,
                DialogResult = DialogResult.OK,
            };
            var buttonCancel = new Button()
            {
                Text = "取消",
                Size = new System.Drawing.Size(150, 50),
                Left = 175,
                Width = 150,
                Top = 200,
                DialogResult = DialogResult.Cancel,
            };

            buttonOk.Click += (sender, e) =>
            {
                form.Close();
            };
            form.Controls.Add(label);
            form.Controls.Add(textBox);
            form.Controls.Add(buttonOk);
            form.Controls.Add(buttonCancel);
            form.AcceptButton = buttonOk;
            form.CancelButton = buttonCancel;

            return form.ShowDialog() == DialogResult.OK ? textBox.Text : string.Empty;
        }
    }
}

//从表分区中的 M 查询检索 Databricks 连接信息的代码
public class DatabricksConnectionInfo
{
    public string ServerHostname { get; set; }
    public string HttpPath { get; set; }
    public string DatabaseName { get; set; }
    public string SchemaName { get; set; }
    public string TableName { get; set; }

    public override string ToString()
    {
        return $"服务器: {ServerHostname}\n"
            + $"HTTP 路径: {HttpPath}\n"
            + $"数据库: {DatabaseName}\n"
            + $"架构: {SchemaName}\n"
            + $"表: {TableName}";
    }
}

public class PowerQueryMParser
{
    public static DatabricksConnectionInfo ParseMQuery(string mQuery)
    {
        if (string.IsNullOrWhiteSpace(mQuery))
            throw new ArgumentException("M 查询不能为 null 或空");

        var connectionInfo = new DatabricksConnectionInfo();

        try
        {
            // 解析 Source 行以提取服务器主机名和 HTTP 路径
            ParseSourceLine(mQuery, connectionInfo);

            // 解析 Database 行以提取数据库名称
            ParseDatabaseLine(mQuery, connectionInfo);

            // 解析 Schema 行以提取架构名称
            ParseSchemaLine(mQuery, connectionInfo);

            // 解析 Data 行以提取表名
            ParseDataLine(mQuery, connectionInfo);

            return connectionInfo;
        }
        catch (Exception ex)
        {
            throw new InvalidOperationException($"解析 M 查询时出错: {ex.Message}", ex);
        }
    }

    private static void ParseSourceLine(string mQuery, DatabricksConnectionInfo connectionInfo)
    {
        // 匹配以下两种模式：
        // Source = DatabricksMultiCloud.Catalogs("hostname", "httppath", null),
        // Source = Databricks.Catalogs("hostname", "httppath", null),
        var sourcePattern =
            @"Source\s*=\s*Databricks(?:MultiCloud)?\.Catalogs\s*\(\s*""([^""]+)""\s*,\s*""([^""]+)""\s*,\s*null\s*\)";
        var sourceMatch = Regex.Match(
            mQuery,
            sourcePattern,
            RegexOptions.IgnoreCase | RegexOptions.Multiline
        );

        if (!sourceMatch.Success)
            throw new FormatException(
                "在 M 查询中找不到有效的 Source 定义（支持 Databricks 和 DatabricksMultiCloud 连接器）"
            );

        connectionInfo.ServerHostname = sourceMatch.Groups[1].Value;
        connectionInfo.HttpPath = sourceMatch.Groups[2].Value;
    }

    private static void ParseDatabaseLine(string mQuery, DatabricksConnectionInfo connectionInfo)
    {
        // 匹配模式：Database = Source{[Name="databasename",Kind="Database"]}[Data],
        var databasePattern =
            @"Database\s*=\s*Source\s*{\s*\[\s*Name\s*=\s*""([^""]+)""\s*,\s*Kind\s*=\s*""Database""\s*\]\s*}\s*\[\s*Data\s*\]";
        var databaseMatch = Regex.Match(
            mQuery,
            databasePattern,
            RegexOptions.IgnoreCase | RegexOptions.Multiline
        );

        if (!databaseMatch.Success)
            throw new FormatException("在 M 查询中找不到有效的 Database 定义");

        connectionInfo.DatabaseName = databaseMatch.Groups[1].Value;
    }

    private static void ParseSchemaLine(string mQuery, DatabricksConnectionInfo connectionInfo)
    {
        // 匹配模式：Schema = Database{[Name="schemaname",Kind="Schema"]}[Data],
        var schemaPattern =
            @"Schema\s*=\s*Database\s*{\s*\[\s*Name\s*=\s*""([^""]+)""\s*,\s*Kind\s*=\s*""Schema""\s*\]\s*}\s*\[\s*Data\s*\]";
        var schemaMatch = Regex.Match(
            mQuery,
            schemaPattern,
            RegexOptions.IgnoreCase | RegexOptions.Multiline
        );

        if (!schemaMatch.Success)
            throw new FormatException("在 M 查询中找不到有效的 Schema 定义");

        connectionInfo.SchemaName = schemaMatch.Groups[1].Value;
    }

    private static void ParseDataLine(string mQuery, DatabricksConnectionInfo connectionInfo)
    {
        // 匹配模式：Data = Schema{[Name="tablename",Kind="Table"]}[Data]
        var dataPattern =
            @"Data\s*=\s*Schema\s*{\s*\[\s*Name\s*=\s*""([^""]+)""\s*,\s*Kind\s*=\s*""Table""\s*\]\s*}\s*\[\s*Data\s*\]";
        var dataMatch = Regex.Match(
            mQuery,
            dataPattern,
            RegexOptions.IgnoreCase | RegexOptions.Multiline
        );

        if (!dataMatch.Success)
            throw new FormatException("在 M 查询中找不到有效的 Data 定义");

        connectionInfo.TableName = dataMatch.Groups[1].Value;
    }
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//主脚本



//检查用户是否已选择表
if (Selected.Tables.Count == 0)
{
    // 切换“正在运行宏”转圈指示
    ScriptHelper.WaitFormVisible = false;
    Interaction.MsgBox("请选择一个或多个表", MsgBoxStyle.Critical, "必须选择表");
    return;
}

//提示输入个人访问令牌 - 这是对 Databricks 进行身份验证所必需的
string dbxPAT;
do
{
    // 切换“正在运行宏”转圈指示
    ScriptHelper.WaitFormVisible = false;
    dbxPAT = MaskedInputHelper.GetMaskedInput(
        "请输入 Databricks 个人访问令牌（连接到 SQL Endpoint 所需）",
        "个人访问令牌"
    );

    if (string.IsNullOrEmpty(dbxPAT))
    {
        return; // 用户已取消
    }

    if (string.IsNullOrWhiteSpace(dbxPAT))
    {
        MessageBox.Show(
            "需要个人访问令牌",
            "需要个人访问令牌",
            MessageBoxButtons.OK,
            MessageBoxIcon.Warning
        );
    }
} while (string.IsNullOrWhiteSpace(dbxPAT));

// 切换“正在运行宏”转圈指示
ScriptHelper.WaitFormVisible = true;

//自动检测 Databricks ODBC 驱动程序
string driverPath;
string newDriverPath = @"C:\Program Files\Databricks ODBC Driver";
string legacyDriverPath = @"C:\Program Files\Simba Spark ODBC Driver";

if (System.IO.Directory.Exists(newDriverPath))
{
    driverPath = newDriverPath;
}
else if (System.IO.Directory.Exists(legacyDriverPath))
{
    driverPath = legacyDriverPath;
}
else
{
    ScriptHelper.WaitFormVisible = false;
    Interaction.MsgBox(
        @"未找到 Databricks ODBC 驱动程序。

请从以下地址安装 Databricks ODBC Driver：
https://www.databricks.com/spark/odbc-drivers-download

预期的安装路径：
  " + newDriverPath + @"
  " + legacyDriverPath,
        MsgBoxStyle.Critical,
        "未找到 ODBC 驱动程序"
    );
    return;
}

//对每个选定的表，从分区信息中获取 Databricks 连接信息
foreach (var t in Selected.Tables)
{
    string mQuery = t.Partitions[t.Name].Expression;
    var connectionInfo = PowerQueryMParser.ParseMQuery(mQuery);
    var rels = 0;
    // 访问各个组成部分
    string serverHostname = connectionInfo.ServerHostname;
    string httpPath = connectionInfo.HttpPath;
    string databaseName = connectionInfo.DatabaseName;
    string schemaName = connectionInfo.SchemaName;
    string tableName = connectionInfo.TableName;

    //使用此查询检查 Unity Catalog 中是否已定义任何主键/外键关系
    var query =
        @"
        SELECT
            fk.table_catalog AS fk_table_catalog,
            fk.table_schema AS fk_table_schema,
            fk.table_name AS fk_table_name,
            fk.column_name AS fk_column,
            pk.table_catalog AS pk_table_catalog,
            pk. table_schema AS pk_table_schema,
            pk.table_name AS pk_table_name,
            pk.column_name AS pk_column
        FROM
            "
        + databaseName
        + @".information_schema.key_column_usage fk
            INNER JOIN "
        + databaseName
        + @".information_schema.referential_constraints rc
                ON fk.constraint_catalog = rc.constraint_catalog
                AND fk.constraint_schema = rc.constraint_schema
                AND fk.constraint_name = rc.constraint_name
            INNER JOIN "
        + databaseName
        + @".information_schema.key_column_usage pk
                ON rc.unique_constraint_catalog = pk.constraint_catalog
                AND rc.unique_constraint_schema = pk.constraint_schema
            AND rc.unique_constraint_name = pk.constraint_name
        WHERE
            fk.table_schema = '"
        + schemaName
        + @"'
            AND fk.table_name = '"
        + tableName
        + @"'
        AND fk.position_in_unique_constraint = 1
";

    //设置 DBX 连接字符串
    var odbcConnStr =
        @"Driver=" + driverPath + ";Host="
        + serverHostname
        + ";Port=443;HTTPPath="
        + httpPath
        + ";SSL=1;ThriftTransport=2;AuthMech=3;UID=token;PWD="
        + dbxPAT;

    //测试连接
    OdbcConnection conn = new OdbcConnection(odbcConnStr);
    try
    {
        conn.Open();
    }
    catch
    {
        // 切换“正在运行宏”转圈指示
        ScriptHelper.WaitFormVisible = false;
        Interaction.MsgBox(
            @"连接失败（使用的驱动程序：" + driverPath + @")

请检查以下前提条件：
    
- 必须已安装 Databricks ODBC Driver 
（下载地址：https://www.databricks.com/spark/odbc-drivers-download）

- 请检查 Databricks 服务器名称 "
                + serverHostname
                + @" 是否正确

- 请检查 Databricks SQL Endpoint / HTTP 路径 "
                + httpPath
                + @" 是否正确

- 请检查你使用的是有效的个人访问令牌",
            MsgBoxStyle.Critical,
            "连接错误"
        );
        return;
    }

    //发送查询
    OdbcDataAdapter da = new OdbcDataAdapter(query, conn);
    var dbxRelationships = new sysData.DataTable();

    try
    {
        da.Fill(dbxRelationships);
    }
    catch
    {
        // 切换“正在运行宏”转圈指示
        ScriptHelper.WaitFormVisible = false;
        Interaction.MsgBox(
            @"连接失败

    可能是以下原因之一： 
        - 表 "
                + schemaName
                + "."
                + tableName
                + " 不存在"
                + @"
        
        - 你没有查询此表的权限
        
        - 连接超时。请检查 SQL Endpoint 群集是否正在运行",
            MsgBoxStyle.Critical,
            "连接错误"
        );
        return;
    }

    //对于模型中的每个表，检查它是否与 Databricks 查询中的某一行匹配
    foreach (var dt in Model.Tables)
    {
        //获取源表信息
        string sourceMQuery = dt.Partitions[dt.Name].Expression;
        var sourceConnectionInfo = PowerQueryMParser.ParseMQuery(sourceMQuery);
        // 访问各个组成部分
        string sourceSchemaName = sourceConnectionInfo.SchemaName;
        string sourceTableName = sourceConnectionInfo.TableName;

        foreach (sysData.DataRow row in dbxRelationships.Rows)
        {
            if (
                string.Equals(
                    sourceSchemaName + "." + sourceTableName,
                    row["pk_table_schema"].ToString() + "." + row["pk_table_name"].ToString(),
                    StringComparison.OrdinalIgnoreCase
                )
            )
            {
                var dimTable = dt;
                foreach (var dc in dt.DataColumns)
                    if (dc.SourceColumn == row["pk_column"].ToString())
                    {
                        var dimColumn = dc;

                        foreach (var fc in t.DataColumns)
                            if (fc.SourceColumn == row["fk_column"].ToString())
                            {
                                var factColumn = fc;

                                // 检查这两列之间是否已存在关系：
                                if (
                                    !Model.Relationships.Any(r =>
                                        r.FromColumn == factColumn && r.ToColumn == dimColumn
                                    )
                                )
                                {
                                    // 如果这两个表之间已存在关系，则新关系将创建为非活动关系：
                                    var makeInactive = Model.Relationships.Any(r =>
                                        r.FromTable == t && r.ToTable == dimTable
                                    );

                                    // 添加新关系：
                                    var rel = Model.AddRelationship();
                                    rel.FromColumn = factColumn;
                                    rel.ToColumn = dimColumn;
                                    factColumn.IsHidden = true;
                                    factColumn.IsAvailableInMDX = false;
                                    dimColumn.IsKey = true;
                                    if (dc.DataType != DataType.DateTime)
                                    {
                                        dimColumn.IsHidden = true;
                                        dimColumn.IsAvailableInMDX = false;
                                    }

                                    if (makeInactive)
                                        rel.IsActive = false;
                                    rels = rels + 1;
                                }
                            }
                    }
            }
        }
    }
    // 切换“正在运行宏”转圈指示
    ScriptHelper.WaitFormVisible = false;
    Interaction.MsgBox(
        "已向 " + t.Name + " 添加 " + rels + " 个关系",
        MsgBoxStyle.Information,
        "添加关系"
    );
    // 切换“正在运行宏”转圈指示
    ScriptHelper.WaitFormVisible = true;
    conn.Close();
}
```

### 说明

脚本使用 WinForms 来提示输入 Databricks 个人访问令牌，用于对 Databricks 进行身份验证。 它会自动检测已安装的是新版 Databricks ODBC Driver 还是旧版 Simba Spark ODBC Driver。 对于每个选中的表，脚本会从该表分区中的 M 查询获取 Databricks 连接字符串信息，以及 schema 和表名。 随后，它会使用检测到的 ODBC 驱动程序向 Databricks 发送一条 SQL 查询，通过查询 information_schema 表来查找在 Unity Catalog 中为该表定义的任何外键关系。 对于 SQL 查询返回的每一行，脚本都会在模型中查找匹配的表名和列名；如果尚未存在关系，则会创建一个新的关系。 对于角色扮演维度，同一张表可能通过多个外键关联到同一目标表，脚本检测到的第一个关系将被设为活动关系，其他随后创建的关系均设为非活动。 脚本还会隐藏主键和外键，并将 IsAvailableInMDX 设为 false（DateTime 类型的主键除外）。 主键也会在语义模型中标记为 IsKey = TRUE。 脚本对所有选定表都运行完成后，会弹出一个对话框，显示新创建了多少个关系。

## 示例输出

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-create-databricks-relationships-before.png" alt="Table relationships before running the script" style="width: 1000px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 1：</strong>运行脚本之前，尚未定义任何关系。</figcaption>
</figure>

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-create-databricks-relationships-pat.png" alt="Prompt for Databricks personal access token" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 2：</strong>脚本会提示你输入 Databricks 个人访问令牌，以便向 Databricks 进行身份验证。</figcaption>
</figure>

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-create-databricks-relationships-done.png" alt="The number of new relationships created" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 3：</strong>脚本对每个选定表运行后，将显示新创建的关系数量。</figcaption>
</figure>

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-create-databricks-relationships-after.png" alt="Table relationships after running the script" style="width: 750px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 4：</strong>运行脚本后的表关系。</figcaption>
</figure>

