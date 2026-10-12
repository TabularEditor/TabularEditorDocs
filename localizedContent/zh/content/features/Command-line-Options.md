---
uid: command-line-options
title: 命令行（Tabular Editor 2）
author: Daniel Otykier
updated: 2026-06-09
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      none: true
    - product: Tabular Editor CLI
      none: true
---

# 命令行（Tabular Editor 2）

Tabular Editor 可通过命令行执行以执行各种任务，这在自动化构建和部署等场景中可能很有用。

## 这些工具如何配合使用

Tabular Editor 3 是面向开发人员的桌面应用程序。它本身不提供命令行界面。对于自动化部署和 CI/CD 管道，可以使用 `TabularEditor.exe`（本页介绍的 Tabular Editor 2 CLI），也可以使用新的跨平台 [Tabular Editor CLI](xref:te-cli)（`te`）。

在 CI/CD 管道中运行 `TabularEditor.exe` 无需 Tabular Editor 3 许可证。只有 Tabular Editor 3 应用程序的用户才需要许可证。

> [!TIP]
> 在寻找新的跨平台 CLI？请参阅 @te-cli 了解 Tabular Editor CLI（有限公开预览版）。它是可在 Windows、macOS 和 Linux 上运行的后继版本。

## TabularEditor.exe 与 Tabular Editor CLI 对比

Tabular Editor CLI（`te`）是 `TabularEditor.exe` 的跨平台后继版本。它不仅仅是面向 macOS 和 Linux 的重写版本——还将模型编辑、检查、差异对比、测试、触发刷新和 VertiPaq 分析作为管道中的一等公民操作引入，而这些都是 `TabularEditor.exe` 无法实现的。 `te` CLI 目前处于有限公开预览阶段（将于 2026-10-31 到期）；目前用于生产流水线请使用 `TabularEditor.exe`。

#### 概览

| 方面    | TE2 CLI (`TabularEditor.exe`) | TE CLI (`te`) |
| ----- | ------------------------------------------------ | -------------------------------- |
| 状态    | 稳定，可用于生产环境                                       | 有限公开预览（将于 2026-10-31 结束）         |
| 平台    | 仅限 Windows                                       | Windows、macOS、Linux              |
| 需要许可证 | 否                                                | 否（预览版）；正式发布时待定                   |
| 二进制文件 | WinForms 应用，需要通过 `start /wait` 进行封装              | 专为控制台设计的二进制文件，无需包装器              |

#### 身份验证

| 功能       | TE2 CLI (`TabularEditor.exe`) | TE CLI (`te`)                                                               |
| -------- | ------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| 服务主体     | 通过 MSOLAP 连接字符串                                  | 原生支持 `--auth spn`、`--auth env`、`--auth managed-identity`；凭据可通过环境变量、stdin 或证书提供；支持操作系统原生的安全凭据存储 |
| 托管标识     | 否                                                | 是（`--auth managed-identity`），适用于 Azure 托管运行器                                                   |
| 交互式浏览器登录 | 否                                                | 是（`te auth login`）                                                                             |

#### CI/CD

| 功能        | TE2 CLI (`TabularEditor.exe`) | TE CLI (`te`)                            |
| --------- | ------------------------------------------------ | ----------------------------------------------------------- |
| CI 注释     | `-V`（Azure DevOps）、`-G`（GitHub）                  | 每个命令都可使用 `--ci vsts`、`--ci github`                          |
| 非交互模式     | 无显式标志；出错时可能会提示                                   | 全局标志 `--non-interactive`——快速失败，不会出现提示                       |
| 可预测的退出代码  | 部分支持                                             | `0` = 成功，`1` = 失败（对于 `te diff`：表示发现差异），`2` = `te diff` 比较错误 |
| 结构化输出     | 否                                                | 每个命令都支持 `--output-format json/csv/tmdl/tmsl`                |
| VSTEST 结果 | `-T` 标志                                          | 在 `validate`、`bpa run` 和 `test run` 命令中使用 `--trx <file>`    |

#### 部署

| 功能                 | TE2 CLI (`TabularEditor.exe`) | TE CLI (`te`)                                                                                        |
| ------------------ | ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| 部署模型               | `-D` 标志                                          | `te deploy` 提供细粒度标志（`--deploy-roles`、`--deploy-partitions`、`--deploy-connections`、`--deploy-full` 等），可分别部署角色、分区、连接或完整内容 |
| 无需部署即可生成 XMLA/TMSL | `-X` 标志                                          | 默认行为：不带 `--execute` 的 `te deploy` 会将 TMSL 输出到 stdout                                                                    |
| 部署前 BPA 门禁检查       | 否                                                | 内置；可用 `--skip-bpa` 或 `--fix-bpa` 覆盖默认行为                                                                                 |
| 连接配置文件             | 否                                                | `te profile set/list/show` - 为每个环境提供可复用的命名配置文件                                                                          |

#### Best Practice Analyzer 与模型编辑

| 功能           | TE2 CLI (`TabularEditor.exe`) | TE CLI (`te`)                                                        |
| ------------ | ------------------------------------------------ | --------------------------------------------------------------------------------------- |
| 运行 BPA       | `-A` / `-AX` 选项                                  | `te bpa run`，支持 `--fail-on warning/error`、`--fix`、`--path` 范围限定，以及用于 VPA 感知规则的 `--vpax` |
| BPA 规则管理     | 否                                                | `te bpa rules add/rm/set/list/disable/enable/init`                                      |
| 运行 C# Script | `-S` 选项                                          | `te script`：多个脚本、内联代码、stdin、`--validate` 编译检查、预处理器符号（`TECLI`）                           |
| 运行宏          | 否                                                | `te macro run`，可通过 `--on <object>` 指定上下文                                                |
| 设置/获取属性      | 否                                                | `te get`, `te set`, `te add`, `te rm`, `te mv`                                          |
| DAX 格式化      | 否                                                | 模型对象使用 `te set --format`，独立表达式使用 `te util format-dax` / `format-m`                      |

#### 检查、刷新、测试和 VertiPaq 分析

| 功能        | TE2 CLI (`TabularEditor.exe`) | TE CLI (`te`)                                                                              |
| --------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| 列出模型对象    | 否                                                | `te ls`，支持通配符路径筛选、`--type`、`--paths-only`、`--output-format bim`                                               |
| 搜索表达式/名称  | 否                                                | `te find`，支持正则表达式和搜索范围 (`--in expressions/names/descriptions`)                             |
| 比较两个模型的差异 | 否                                                | `te diff` - 结构比较；如有任何差异则以退出代码 `1` 结束                                                                          |
| 依赖关系分析    | 否                                                | `te deps` - 查看任何对象的上游/下游依赖；使用 `--unused` 查找死代码                                                                |
| 触发刷新      | 否                                                | `te refresh` 可与 `--type`、`--table`、`--partition`、`--apply-refresh-policy` 一起使用；默认仅进行干运行，需加 `--execute` 才会实际运行 |
| DAX 断言测试  | 否                                                | `te test run` 支持 `--tag`、`--trx`、`--ci`；也可使用 `te test init/snapshot/compare`                                  |
| 存储统计      | 否                                                | `te vertipaq` - 列、关系、分区；`--export`/`--import` VPAX                                                            |

#### 其他

| 功能             | TE2 CLI (`TabularEditor.exe`) | TE CLI (`te`)                   |
| -------------- | ------------------------------------------------ | -------------------------------------------------- |
| 交互式 REPL       | 否                                                | `te interactive` - 具备模型感知能力的 shell，提供持久化历史记录和分阶段编辑 |
| Shell Tab 自动补全 | 否                                                | `te completion bash/zsh/pwsh`                      |
| TE2 向后兼容性      | 原生                                               | 内置兼容层——现有 `TabularEditor.exe` 调用无需修改即可继续使用         |

如需查看从 TE2 语法到新 CLI 的逐项标志映射，请参见 @te-cli-migrate。

**注意：** 由于 TabularEditor.exe 是一个 WinForms 应用程序，直接从 Windows 命令提示符执行会导致线程立即返回到提示符。这可能会在命令脚本等场景中引发问题。如需等待 TabularEditor.exe 完成其命令行任务，请始终使用以下方式执行：`start /wait TabularEditor ...`

要查看 Tabular Editor 提供的命令行选项，请运行以下命令：

**Windows 命令行：**

```shell
start /wait TabularEditor.exe /?
```

**PowerShell：**

```powershell
$p = Start-Process -filePath TabularEditor.exe -Wait -NoNewWindow -PassThru -ArgumentList "/?"
```

输出：

```cmd
Usage:

TABULAREDITOR ( file | server database | -L [name] ) [-S script1 [script2] [...]]
    [-SC] [-A [rules] | -AX rules] [(-B | -F | -TMDL) output [id]] [-V | -G] [-T resultsfile]
    [-D [server database [-L user pass] [-F | -O [-C [plch1 value1 [plch2 value2 [...]]]]
        [-P [-Y]] [-S] [-R [-M]]]
        [-X xmla_script]] [-W] [-E]]

file                Full path of the Model.bim file or database.json model folder to load.
server              Server\instance name or connection string from which to load the model
database            Database ID of the model to load. If blank (") picks the first available
                      database on the server.
-L / -LOCAL         Connects to a Power BI Desktop (local) instance of Analysis Services. If no
                      name is specified, this assumes that exactly 1 instance is running. Otherwise,
                      name should match the name of the .pbix file loaded in Power BI Desktop.
-S / -SCRIPT        Execute the specified script on the model after loading.
  scriptN             Full path of one or more files containing a C# script to execute or an inline
                      script.
-SC / -SCHEMACHECK  Attempts to connect to all Provider Data Sources in order to detect table schema
                    changes. Outputs...
                      ...warnings for mismatched data types and unmapped source columns
                      ...errors for unmapped model columns.
-A / -ANALYZE       Runs Best Practice Analyzer and outputs the result to the console.
  rules               Optional path of file or URL of additional BPA rules to be analyzed. If
                      specified, model is not analyzed against local user/local machine rules,
                      but rules defined within the model are still applied.
-AX / -ANALYZEX     Same as -A / -ANALYZE but excludes rules specified in the model annotations.
-B / -BIM / -BUILD  Saves the model (after optional script execution) as a Model.bim file.
  output              Full path of the Model.bim file to save to.
  id                  Optional id/name to assign to the Database object when saving.
-F / -FOLDER        Saves the model (after optional script execution) as a Folder structure.
  output              Full path of the folder to save to. Folder is created if it does not exist.
  id                  Optional id/name to assign to the Database object when saving.
-TMDL               Saves the model (after optional script execution) as a TMDL folder structure.
  output              Full path of the TMDL folder to save to. Folder is created if it does not exist.
  id                  Optional id/name to assign to the Database object when saving.
-V / -VSTS          Output Visual Studio Team Services logging commands.
-G / -GITHUB        Output GitHub Actions workflow commands.
-T / -TRX         Produces a VSTEST (trx) file with details on the execution.
  resultsfile       File name of the VSTEST XML file.
-D / -DEPLOY        Command-line deployment
                      If no additional parameters are specified, this switch will save model metadata
                      back to the source (file or database).
  server              Name of server to deploy to or connection string to Analysis Services.
  database            ID of the database to deploy (create/overwrite).
  -L / -LOGIN         Disables integrated security when connecting to the server. Specify:
    user                Username (must be a user with admin rights on the server)
    pass                Password
  -F / -FULL          Deploy the full model metadata, allowing overwrite of an existing database.
  -O / -OVERWRITE     Allow deploy (overwrite) of an existing database.
    -C / -CONNECTIONS   Deploy (overwrite) existing data sources in the model. After the -C switch, you
                        can (optionally) specify any number of placeholder-value pairs. Doing so, will
                        replace any occurrence of the specified placeholders (plch1, plch2, ...) in the
                        connection strings of every data source in the model, with the specified values
                        (value1, value2, ...).
    -P / -PARTITIONS    Deploy (overwrite) existing table partitions in the model.
      -Y / -SKIPPOLICY    Do not overwrite partitions that have Incremental Refresh Policies defined.
    -S / -SHARED        Deploy (overwrite) shared expressions.
    -R / -ROLES         Deploy roles.
      -M / -MEMBERS       Deploy role members.
  -X / -XMLA        No deployment. Generate XMLA/TMSL script for later deployment instead.
    xmla_script       File name of the new XMLA/TMSL script output.
  -W / -WARN        Outputs information about unprocessed objects as warnings.
  -E / -ERR         Returns a non-zero exit code if Analysis Services returns any error messages after
                      the metadata was deployed / updated.
```

> [!WARNING]
> 在 [Tabular Editor 2.27.0](https://github.com/TabularEditor/TabularEditor/releases/tag/2.27.0) 中新增 `-S` / `-SHARED` 部署选项标志，这是一次**破坏性变更**。如果你使用 Tabular Editor CLI 执行部署，并且正在从更早版本的 Tabular Editor 升级，请务必在 CLI 命令中包含该标志，否则**不会部署共享表达式**。

> [!TIP]
> `-F` 标志在 [Tabular Editor 2.27.0](https://github.com/TabularEditor/TabularEditor/releases) 中引入。它用于执行“完整”部署，等同于指定 `-O -C -P -S -R -M`。

## 连接到 Azure Analysis Services

在命令中，你可以用任何有效的 SSAS 连接字符串替代服务器名称。以下命令从 Azure Analysis Services 加载模型，并将其在本地保存为 Model.bim 文件：

**Windows 命令行：**

```shell
start /wait TabularEditor.exe "Provider=MSOLAP;Data Source=asazure://northeurope.asazure.windows.net/MyAASServer;User ID=xxxx;Password=xxxx;Persist Security Info=True;Impersonation Level=Impersonate" MyModelDB -B "C:\Projects\FromAzure\Model.bim"
```

**PowerShell：**

```powershell
$p = Start-Process -filePath TabularEditor.exe -Wait -NoNewWindow -PassThru `
       -ArgumentList "`"Provider=MSOLAP;Data Source=asazure://northeurope.asazure.windows.net/MyAASServer;User ID=xxxx;Password=xxxx;Persist Security Info=True;Impersonation Level=Impersonate`" MyModelDB -B C:\Projects\FromAzure\Model.bim"
```

如果你希望使用服务主体（应用程序 ID 和密钥）进行连接，而不是通过 Azure Active Directory 身份验证，可以使用以下连接字符串：

```
Provider=MSOLAP;Data Source=asazure://northeurope.asazure.windows.net/MyAASServer;User ID=app:<APPLICATION ID>@<TENANT ID>;Password=<APPLICATION KEY>;Persist Security Info=True;Impersonation Level=Impersonate
```

## 自动化脚本修改

如果你已在 Tabular Editor 中创建了脚本，并希望在部署前将该脚本应用到 Model.bim 文件，可以使用命令行选项“-S”（Script）：

**Windows 命令行：**

```shell
start /wait TabularEditor.exe "C:\Projects\MyModel\Model.bim" -S "C:\Projects\MyModel\MyScript.cs" -D localhost\tabular MyModel
```

**PowerShell：**

```powershell
$p = Start-Process -filePath TabularEditor.exe -Wait -NoNewWindow -PassThru `
       -ArgumentList "`"C:\Projects\MyModel\Model.bim`" -S `"C:\Projects\MyModel\MyScript.cs`" -D `"localhost\tabular`" `"MyModel`""
```

该命令会在 Tabular Editor 中加载 Model.bim 文件，应用指定脚本，并将修改后的模型作为新数据库“MyModel”部署到“localhost\tabular”服务器。如果你希望覆盖服务器上已存在的同名数据库，请使用“-O”（Overwrite）开关。

你也可以用“-B”（Build）开关替代“-D”（Deploy）开关，将修改后的模型输出为新的 Model.bim 文件，而不是直接部署到服务器。当你想用其他部署工具来部署模型，或希望在部署前先在 Visual Studio 或 Tabular Editor 中检查模型时，这会很有用。在自动化构建场景中也同样实用：你可以在部署前，将修改后的模型作为发布产物进行保存。

## 在部署期间修改连接字符串

假设你的模型包含一个数据源，其连接字符串如下：

```
Provider=SQLOLEDB.1;Data Source=sqldwdev;Persist Security Info=False;Integrated Security=SSPI;Initial Catalog=DW
```

在部署期间，你希望修改该字符串，使其指向 UAT 或生产数据库。最佳做法是：先用脚本将整个连接字符串替换为一个占位符值，然后使用 -C 开关将该占位符替换为实际连接字符串。

将以下脚本放到名为“ClearConnectionStrings.cs”或类似名称的文件中：

```csharp
// This will replace the connection string of all Provider (legacy) data sources in the model
// with a placeholder based on the name of the data source. E.g., if your data source is called
// "SQLDW", the connection string after running this script would be "SQLDW":

foreach(var ds in Model.DataSources.OfType<ProviderDataSource>())
    ds.ConnectionString = ds.Name;
```

我们可以让 Tabular Editor 执行该脚本，然后通过下面的命令进行占位符替换：

**Windows 命令行：**

```shell
start /wait TabularEditor.exe "Model.bim" -S "ClearConnectionStrings.cs" -D localhost\tabular MyModel -C "SQLDW" "Provider=SQLOLEDB.1;Data Source=sqldwprod;Persist Security Info=False;Integrated Security=SSPI;Initial Catalog=DW"
```

**PowerShell：**

```powershell
$p = Start-Process -filePath TabularEditor.exe -Wait -NoNewWindow -PassThru `
       -ArgumentList "Model.bim -S ClearConnectionStrings.cs -D localhost\tabular MyModel -C SQLDW `"Provider=SQLOLEDB.1;Data Source=sqldwprod;Persist Security Info=False;Integrated Security=SSPI;Initial Catalog=DW`""
```

上述命令会将 Model.bim 文件部署为“localhost\\tabular”SSAS 实例上的一个新的 SSAS 数据库“MyModel”。在部署之前，脚本会先把所有提供程序（旧版）数据源上的连接字符串替换为数据源名称，作为占位符使用。假设我们只有一个名为“SQLDW”的数据源，那么 -C 开关会更新连接字符串，将“SQLDW”替换为指定的完整字符串。

当你需要将同一个模型部署到多个环境、并让它们从不同（结构相同）的来源处理数据时，这个技巧就很有用——例如生产、预生产或 UAT 数据库。如果使用 Azure DevOps（见下文），建议用变量来保存实际要使用的连接字符串，而不是把它硬编码在命令里。

## 与 Azure DevOps 集成

如果你想在 Azure DevOps 管道中使用 Tabular Editor CLI，那么脚本中执行的任何 TabularEditor.exe 命令都应该使用“-V”开关。该开关会让 Tabular Editor 以 [Azure DevOps 可读取的格式](https://github.com/Microsoft/vsts-tasks/blob/master/docs/authoring/commands.md) 输出日志命令。这样 Azure DevOps 才能正确响应错误等情况。

通过命令行执行部署时，未处理对象的相关信息会输出到命令提示符中。在自动化部署场景中，你可能希望构建代理能够对对象变为未处理的情况做出响应，例如新增列、修改计算表格的 DAX 表达式等。这种情况下，除了上面提到的“-V”开关之外，你还可以使用“-W”开关，将这些信息以警告的形式输出。这样一来，部署完成后会向 Azure DevOps 返回“SucceededWithIssues”状态。如果你希望在成功部署后，服务器报告任何 DAX 错误时让部署返回“Failed”状态，也可以使用“-E”开关。

在 Azure DevOps 管道的“命令行任务”中执行 TabularEditor.exe 时，不需要使用 `start /wait`。因为命令行任务会一直等待，直到该任务启动的所有线程都已终止，才会结束。换句话说，只有在调用 TabularEditor.exe 之后还要执行其他命令时，才需要使用 `start /wait`；并且在这种情况下，请确保使用 `start /B /wait`。需要使用 `/B` 开关，才能将 TabularEditor.exe 的输出正确地通过管道回传到流水线日志中。

```shell
TabularEditor.exe "C:\Projects\My Model\Model.bim" -D ssasserver databasename -O -C -P -S -V -E -W
```

或者执行多条命令：

```shell
start /B /wait TabularEditor.exe "C:\Projects\Finance\Model.bim" -D ssasserver Finance -O -C -P -S -V -E -W
start /B /wait TabularEditor.exe "C:\Projects\Sales\Model.bim" -D ssasserver Sales -O -C -P -S -V -E -W
```

下图展示了此类构建在 Azure DevOps 中的样子：

![image](~/content/assets/images/command-line-options-01.png)

如果部署因任何原因失败，Tabular Editor 都会向 Azure DevOps 返回“Failed”状态，无论你是否使用了“-W”开关。

如需了解 Azure DevOps 与 Tabular Editor 的更多信息，请参阅[这套博客系列](https://tabulareditor.github.io/2019/02/20/DevOps1.html)（尤其是[第 3 章](https://tabulareditor.github.io/2019/10/08/DevOps3.html)及之后的内容）。

### Azure DevOps PowerShell 任务

如果你更倾向于使用 PowerShell 任务而不是命令行任务，则必须像上面演示的那样，使用 `Start-Process` cmdlet 来执行 TabularEditor.exe。此外，请确保在 PowerShell 脚本中将进程退出代码作为 exit 参数传递，这样 Tabular Editor 中发生的错误就会导致 PowerShell 任务失败：

```powershell
$p = Start-Process -filePath TabularEditor.exe -Wait -NoNewWindow -PassThru `
       -argumentList "`"C:\Projects\My Model\Model.bim`" -D ssasserver databasename -O -C -P -S -V -E -W"
exit $p.ExitCode
```

### 通过环境变量将参数传递给脚本

在 Azure DevOps 管道中使用 `-S` 选项执行 C# 脚本时，建议通过环境变量而非命令行参数传递参数。在 Azure DevOps 管道中使用 `-S` 选项执行 C# 脚本时，建议通过环境变量而非命令行参数传递参数。 C# 脚本可以使用 `Environment.GetEnvironmentVariable()` 读取环境变量；Azure DevOps 会自动将所有管道变量作为环境变量提供。

**示例：在 YAML 中设置环境变量：**

```yaml
variables:
  deployEnv: 'Production'
  serverName: 'prod-sql-server'

steps:
- script: TabularEditor.exe "Model.bim" -S "UpdateModel.csx" -D "$(serverName)" "MyDatabase" -O -V -E -W
  displayName: 'Deploy with Script Parameters'
  env:
    DEPLOY_ENV: $(deployEnv)
    SERVER_NAME: $(serverName)
```

**示例：使用环境变量的 PowerShell 任务：**

```yaml
- task: PowerShell@2
  displayName: 'Run Tabular Editor Script'
  env:
    DEPLOY_ENV: 'UAT'
    CONNECTION_STRING: $(sqldwConnectionString)
  inputs:
    targetType: 'inline'
    script: |
      $p = Start-Process -filePath TabularEditor.exe -Wait -NoNewWindow -PassThru `
             -ArgumentList "`"Model.bim`" -S `"ConfigureModel.csx`" -B `"output/Model.bim`" -V"
      exit $p.ExitCode
```

**在 C# Script 中（例如 UpdateModel.csx）：**

```csharp
var deployEnv = Environment.GetEnvironmentVariable("DEPLOY_ENV");
var serverName = Environment.GetEnvironmentVariable("SERVER_NAME");

Info($"Configuring model for {deployEnv} environment on {serverName}");

// Apply environment-specific changes
foreach(var ds in Model.DataSources.OfType<ProviderDataSource>())
{
    ds.ConnectionString = ds.ConnectionString.Replace("{SERVER}", serverName);
}
```

这种方法比在脚本中硬编码值或使用复杂的字符串替换方式更简洁、更易维护。这种方法比在脚本中硬编码值或使用复杂的字符串替换方式更简洁、更易维护。 有关在 C# 脚本中使用环境变量的更多信息，请参阅 [C# Scripts - Accessing Environment Variables](xref:csharp-scripts#accessing-environment-variables)。

## 运行 Best Practice Analyzer

你可以使用 "-A" 开关，让 Tabular Editor 扫描模型，找出所有违反最佳实践规则的对象（规则可定义在本机上，位于 %AppData%\..\Local\TabularEditor\BPARules.json 文件中；也可作为注释存储在模型本身中）。或者，你也可以在 "-A" 开关后指定一个包含最佳实践规则的 .json 文件路径，以使用该文件中定义的规则来扫描模型。违规的对象将输出到控制台。

如果你同时使用“-V”开关，则每条规则的严重性级别将决定如何将规则违规情况报告到构建管道：

- Severity = 1 仅作信息提示
- Severity = 2 会触发 WARNING
- Severity >= 3 会触发 ERROR

## 执行数据源架构检查

从 [2.8 版本](https://github.com/TabularEditor/TabularEditor/releases/tag/2.8)开始，你可以使用 -SC（-SCHEMACHECK）开关来验证表的源查询。这相当于调用[刷新表元数据 UI](xref:importing-tables-te2#refreshing-table-metadata)，但不会对模型做任何更改，而是会将架构差异报告到控制台。数据类型更改以及源中新增的列将以警告形式报告。源中缺失的列将以错误形式报告。如果同时指定了 -SC（-SCHEMACHECK）和 -S（-SCRIPT）开关，则架构检查会在脚本成功执行之后运行。这样你就可以在执行架构检查之前修改数据源属性，例如用于指定凭据密码。

如果你希望架构检查以特定方式处理表和列，也可以为它们添加注释。[更多信息请参见此处](xref:importing-tables-te2#ignoring-objects)。

## 命令行输出与退出代码

命令行会根据所使用的开关以及执行过程中遇到的事件，提供各类详细信息。退出代码在 [2.7.4 版本](https://github.com/TabularEditor/TabularEditor/releases/tag/2.7.4) 中引入。

| 级别 | 命令            | 信息                                 | 说明                                                                                                                                                                        |
| -- | ------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 错误 | （任意）          | 参数语法无效                             | 向 Tabular Editor CLI 提供了无效的参数                                                                                                                                             |
| 错误 | （任意）          | 未找到文件……                            |                                                                                                                                                                           |
| 错误 | （任意）          | 加载文件时出错……                          | 文件已损坏，或不包含 JSON 格式的有效 TOM 元数据                                                                                                                                             |
| 错误 | （任意）          | 加载模型时出错……                          | 无法连接到所提供的 Analysis Services 实例，或找不到数据库，或数据库元数据已损坏，或数据库的兼容级别不受支持                                                                                                           |
| 错误 | -SCRIPT       | 未找到指定的脚本文件                         |                                                                                                                                                                           |
| 错误 | -SCRIPT       | 脚本编译错误：                            | 脚本包含无效的 C# 语法。详细信息将输出在后续几行中。                                                                                                                                              |
| 错误 | -SCRIPT       | 脚本执行错误：……                          | 执行脚本时发生未处理的异常。                                                                                                                                                            |
| 信息 | -SCRIPT       | 脚本行号 #：……                          | 在脚本中使用 `Info(string)` 或 `Output(string)` 方法。                                                                                                                              |
| 警告 | -SCRIPT       | 脚本警告：……                            | 在脚本中使用 `Warning(string)` 方法。                                                                                                                                              |
| 错误 | -SCRIPT       | 脚本错误：……                            | 在脚本中使用 `Error(string)` 方法。                                                                                                                                                |
| 错误 | -FOLDER, -BIM | -FOLDER 和 -BIM 参数互斥。               | Tabular Editor 无法在一次运行中将当前加载的模型同时保存为文件夹结构和 .bim 文件。                                                                                                       |
| 错误 | -ANALYZE      | 未找到规则文件：……                         |                                                                                                                                                                           |
| 错误 | -ANALYZE      | 无效的规则文件：……                         | 指定的 BPA 规则文件已损坏或不包含有效的 JSON。                                                                                                                                              |
| 信息 | -ANALYZE      | ……违反规则……                           | Best Practice Analyzer 针对严重性级别为 1 或以下规则的结果。                                                                                                                               |
| 警告 | -ANALYZE      | ……违反规则……                           | Best Practice Analyzer 针对严重性级别 2 的规则的结果。                                                                                                                                  |
| 错误 | -ANALYZE      | ……违反规则……                           | Best Practice Analyzer 针对严重性级别 3 或更高的规则的结果。                                                                                                                               |
| 错误 | -DEPLOY       | 部署失败！……                            | 由 Analysis Services 实例直接返回的失败原因（例如：找不到数据库、不允许数据库覆盖等）                                                                                                                      |
| 信息 | -DEPLOY       | 未处理的对象: ……         | 成功部署后处于 "NoData" 或 "CalculationNeeded" 状态的对象。使用 -W 开关将这些按 Level=Warning 处理。                                                                                               |
| 警告 | -DEPLOY       | 对象不处于"Ready"状态: …… | 成功部署后处于 "DependencyError"、"EvaluationError" 或 "SemanticError" 状态的对象。 如果使用 -W 开关，还包括处于“NoData”或“CalculationNeeded”状态的对象。如果使用 -W 开关，还包括处于“NoData”或“CalculationNeeded”状态的对象。 |
| 警告 | -DEPLOY       | X 上发生错误：……                         | 成功部署后包含无效 DAX 的对象（度量值、计算列、计算表格、角色）。使用 -E 选项将这些视为 Level=Error。                                                                                                             |

如果检测到任何级别为“Error”的输出，Tabular Editor 将返回 Exit Code = 1。否则返回 0。
