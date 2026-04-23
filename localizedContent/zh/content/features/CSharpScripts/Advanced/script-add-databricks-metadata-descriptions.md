---
uid: script-add-databricks-metadata-descriptions
title: 添加 Databricks 元数据说明
author: Johnny Winter
updated: 2026-04-08
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 添加 Databricks 元数据说明

## 脚本用途

本脚本为 Tabular Editor x Databricks 系列的一部分而创建。 在 Unity Catalog 中，可以为表和列添加描述性注释。 此脚本可复用这些信息，自动补全语义模型中的表和列说明。 <br></br>

> [!NOTE]
> 此脚本需要 Databricks ODBC 驱动程序。 我们推荐新版 [Databricks ODBC Driver](https://www.databricks.com/spark/odbc-drivers-download)，它将取代旧版 Simba Spark ODBC Driver。 脚本会自动检测已安装的驱动程序，并据此使用相应驱动程序。

每次运行脚本时，都会提示你输入 Databricks 个人访问令牌。 这是用于向 Databricks 进行身份验证所必需的。
该脚本会使用 Unity Catalog 中的 information_schema 表来检索关系信息，因此你可能需要向 Databricks 管理员再次确认，确保自己有权限查询这些表。 <br></br>

## 脚本

### 添加 Databricks 元数据说明

```csharp
/*
 * 标题：添加 Databricks 元数据描述
 * 作者：Johnny Winter, greyskullanalytics.com
 *
 * 这个脚本运行时，会遍历当前选中的表，并向 Databricks 发送查询，以检查每个表是否在 Unity Catalog 中定义了元数据描述。
 * 如果存在描述，则会将其添加到语义模型的描述中。
 * 步骤 1：在模型中选择一个或多个表
 * 步骤 2：运行这个脚本
 * 步骤 3：根据提示输入 Databricks 个人访问令牌
 * 步骤 4：脚本将连接到 Databricks，并在存在描述时更新表和列的描述。
 *          对于处理的每个表，消息框都会显示已更新的描述数量。
 *          点击“确定”继续处理下一个表。
 * 说明：
 *  -   这个脚本需要先安装 Databricks ODBC Driver（推荐）或旧版 Simba Spark ODBC Driver（下载地址：https://www.databricks.com/spark/odbc-drivers-download）
 *  -   脚本会自动检测已安装的驱动程序
 *  -   每次运行脚本时，都会提示用户输入 Databricks 个人访问令牌
 */
#r "Microsoft.VisualBasic"
using System;
using System.Data.Odbc;
using System.Drawing;
using System.Text.RegularExpressions;
using System.Windows.Forms;
using Microsoft.VisualBasic;
using sysData = System.Data;

//用于创建 Databricks PAT 掩码输入框的代码
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

        //提示标签
        promptLabel = new Label();
        promptLabel.Text = prompt;
        promptLabel.Location = new System.Drawing.Point(12, 15);
        promptLabel.Size = new System.Drawing.Size(360, 40);
        promptLabel.AutoSize = false;
        this.Controls.Add(promptLabel);

        //密码文本框
        passwordTextBox = new TextBox();
        passwordTextBox.Location = new System.Drawing.Point(12, 55);
        passwordTextBox.Size = new System.Drawing.Size(360, 20);
        passwordTextBox.UseSystemPasswordChar = true; //这会隐藏输入内容
        passwordTextBox.KeyPress += (s, e) =>
        {
            if (e.KeyChar == (char)Keys.Return)
            {
                OkButton_Click(null, null);
                e.Handled = true;
            }
        };
        this.Controls.Add(passwordTextBox);

        //确定按钮
        okButton = new Button();
        okButton.Text = "确定";
        okButton.Location = new System.Drawing.Point(216, 85);
        okButton.Size = new System.Drawing.Size(150, 50);
        okButton.Click += OkButton_Click;
        this.Controls.Add(okButton);

        //取消按钮
        cancelButton = new Button();
        cancelButton.Text = "取消";
        cancelButton.Location = new System.Drawing.Point(297, 85);
        cancelButton.Size = new System.Drawing.Size(150, 50);
        cancelButton.Click += CancelButton_Click;
        this.Controls.Add(cancelButton);

        //设置默认按钮和取消按钮
        this.AcceptButton = okButton;
        this.CancelButton = cancelButton;

        //窗体加载时将焦点放到文本框
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
        return $"服务器：{ServerHostname}\n"
            + $"HTTP 路径：{HttpPath}\n"
            + $"数据库：{DatabaseName}\n"
            + $"架构：{SchemaName}\n"
            + $"表：{TableName}";
    }
}

public class PowerQueryMParser
{
    public static DatabricksConnectionInfo ParseMQuery(string mQuery)
    {
        if (string.IsNullOrWhiteSpace(mQuery))
            throw new ArgumentException("M 查询不能为 null 或空字符串");

        var connectionInfo = new DatabricksConnectionInfo();

        try
        {
            //解析 Source 行以提取服务器主机名和 HTTP 路径
            ParseSourceLine(mQuery, connectionInfo);

            //解析 Database 行以提取数据库名称
            ParseDatabaseLine(mQuery, connectionInfo);

            //解析 Schema 行以提取架构名称
            ParseSchemaLine(mQuery, connectionInfo);

            //解析 Data 行以提取表名
            ParseDataLine(mQuery, connectionInfo);

            return connectionInfo;
        }
        catch (Exception ex)
        {
            throw new InvalidOperationException($"解析 M 查询时出错：{ex.Message}", ex);
        }
    }

    private static void ParseSourceLine(string mQuery, DatabricksConnectionInfo connectionInfo)
    {
        //用于匹配以下两种模式：
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
                "在 M 查询中找不到有效的 Source 定义（同时支持 Databricks 和 DatabricksMultiCloud 连接器）"
            );

        connectionInfo.ServerHostname = sourceMatch.Groups[1].Value;
        connectionInfo.HttpPath = sourceMatch.Groups[2].Value;
    }

    private static void ParseDatabaseLine(string mQuery, DatabricksConnectionInfo connectionInfo)
    {
        //用于匹配：Database = Source{[Name="databasename",Kind="Database"]}[Data],
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
        //用于匹配：Schema = Database{[Name="schemaname",Kind="Schema"]}[Data],
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
        //用于匹配：Data = Schema{[Name="tablename",Kind="Table"]}[Data]
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
    //切换“Running Macro”旋转提示
    ScriptHelper.WaitFormVisible = false;
    Interaction.MsgBox("请选择一个或多个表", MsgBoxStyle.Critical, "需要表");
    return;
}

//提示输入个人访问令牌 - 这是 Databricks 身份验证所必需的
string dbxPAT;
do
{
    //切换“Running Macro”旋转提示
    ScriptHelper.WaitFormVisible = false;
    dbxPAT = MaskedInputHelper.GetMaskedInput(
        "请输入 Databricks 个人访问令牌（连接到 SQL Endpoint 需要此令牌）",
        "个人访问令牌"
    );

    if (string.IsNullOrEmpty(dbxPAT))
    {
        return; //用户已取消
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

//切换“Running Macro”旋转提示
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

预期安装路径：
  " + newDriverPath + @"
  " + legacyDriverPath,
        MsgBoxStyle.Critical,
        "未找到 ODBC 驱动程序"
    );
    return;
}

//对于每个选中的表，从分区信息中获取 Databricks 连接信息
foreach (var t in Selected.Tables)
{
    string mQuery = t.Partitions[t.Name].Expression;
    var connectionInfo = PowerQueryMParser.ParseMQuery(mQuery);
    var columnDescriptions = 0;
    var tableDescriptions = 0;
    //访问各个组成部分
    string serverHostname = connectionInfo.ServerHostname;
    string httpPath = connectionInfo.HttpPath;
    string databaseName = connectionInfo.DatabaseName;
    string schemaName = connectionInfo.SchemaName;
    string tableName = connectionInfo.TableName;
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
        //切换“Running Macro”旋转提示
        ScriptHelper.WaitFormVisible = false;
        Interaction.MsgBox(
            @"连接失败（使用的驱动程序：" + driverPath + @"）

请检查以下前提条件：
    
- 必须已安装 Databricks ODBC Driver
（下载地址：https://www.databricks.com/spark/odbc-drivers-download）

- 请确认 Databricks 服务器名称 "
                + serverHostname
                + @" 正确

- 请确认 Databricks SQL Endpoint / HTTP Path "
                + httpPath
                + @" 正确

- 请确认你使用的是有效的个人访问令牌",
            MsgBoxStyle.Critical,
            "连接错误"
        );
        return;
    }

    //获取表元数据
    var tableQuery =
        "SELECT comment FROM "
        + databaseName
        + ".information_schema.tables WHERE table_schema = '"
        + schemaName
        + "' AND table_name = '"
        + tableName
        + "'";
    OdbcDataAdapter td = new OdbcDataAdapter(tableQuery, conn);
    var dbxTable = new sysData.DataTable();

    try
    {
        td.Fill(dbxTable);
    }
    catch
    {
        //切换“Running Macro”旋转提示
        ScriptHelper.WaitFormVisible = false;
        Interaction.MsgBox(
            @"连接失败

可能原因如下：
    - 表 "
                + schemaName
                + "."
                + tableName
                + " 不存在"
                + @"
    
    - 你没有查询此表的权限
    
    - 连接已超时。请检查 SQL Endpoint 集群是否正在运行",
            MsgBoxStyle.Critical,
            "连接错误 - 表元数据"
        );
        return;
    }
    string tableUpdate = "";
    foreach (sysData.DataRow row in dbxTable.Rows)
    {
        if (t.Description != row["comment"].ToString())
        {
            t.Description = row["comment"].ToString();
            tableUpdate = t.Name + " 表描述已更新。";
        }
    }

    //获取列元数据
    var columnsQuery = @"DESCRIBE " + databaseName + "." + schemaName + "." + tableName;
    OdbcDataAdapter da = new OdbcDataAdapter(columnsQuery, conn);
    var dbxColumns = new sysData.DataTable();

    try
    {
        da.Fill(dbxColumns);
    }
    catch
    {
        //切换“Running Macro”旋转提示
        ScriptHelper.WaitFormVisible = false;
        Interaction.MsgBox(
            @"连接失败

可能原因如下：
    - 表 "
                + schemaName
                + "."
                + tableName
                + " 不存在"
                + @"
    
    - 你没有查询此表的权限
    
    - 连接已超时。请检查 SQL Endpoint 集群是否正在运行",
            MsgBoxStyle.Critical,
            "连接错误 - 列元数据"
        );
        return;
    }

    //更新列描述
    int counter = 0;
    foreach (sysData.DataRow row in dbxColumns.Rows)
    {
        string sourceColumn = row["col_name"].ToString();
        if (sourceColumn.Length != 0)
        {
            foreach (var c in t.DataColumns)
            {
                if (c.SourceColumn == sourceColumn && c.Description != row["comment"].ToString())
                {
                    c.Description = row["comment"].ToString();
                    counter = counter + 1;
                }
            }
        }
    }
    string msg;
    if (tableUpdate.Length > 0)
    {
        msg =
            tableUpdate
            + @"

已更新 "
            + t.Name
            + " 中的 "
            + counter
            + " 个描述";
    }
    else
    {
        msg = "已更新 " + t.Name + " 中的 " + counter + " 个描述";
    }
    //切换“Running Macro”旋转提示
    ScriptHelper.WaitFormVisible = false;
    Interaction.MsgBox(msg, MsgBoxStyle.Information, "更新元数据描述");
    //切换“Running Macro”旋转提示
    ScriptHelper.WaitFormVisible = true;
    conn.Close();
}
```

### 说明

该脚本使用 WinForms 弹窗提示输入 Databricks 个人访问令牌，用于对 Databricks 进行身份验证。 它会自动检测已安装的是新版 Databricks ODBC Driver 还是旧版 Simba Spark ODBC Driver。 对每个选中的表，脚本都会从其分区中的 M 查询提取 Databricks 连接字符串信息，以及架构名和表名。 随后，脚本会使用检测到的 ODBC 驱动程序向 Databricks 发送 SQL 查询，查询 information_schema 表，从而返回 Unity Catalog 中定义的表说明。 然后会将其更新到语义模型中的表说明。 还会对所选表再发送一条使用 DESCRIBE 命令的 SQL 查询，以获取列说明。 随后会遍历这些结果，并在模型中补充说明。 脚本在每个选定的表上运行完毕后，会弹出对话框，显示已更新的描述数量。

## 输出示例

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-create-databricks-relationships-pat.png" alt="Prompt for Databricks personal access token" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 1：</strong>脚本会提示你输入 Databricks 个人访问令牌，以便向 Databricks 进行身份验证。</figcaption>
</figure>

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-add-databricks-metadata-descriptions-done.png" alt="The number of descriptions updated" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 2：</strong>脚本对每个选定的表运行完毕后，会显示已更新的描述数量。</figcaption>
</figure>



