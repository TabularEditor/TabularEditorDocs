---
uid: command-line-options
title: Command Line (Tabular Editor 2)
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

# Command Line (Tabular Editor 2)

Tabular Editor 可通过命令行执行以执行各种任务，这在自动化构建和部署等场景中可能很有用。

## How the tools fit together

Tabular Editor 3 is a desktop application for developers. It has no command-line interface of its own. For automated deployments and CI/CD pipelines, use either `TabularEditor.exe` (the Tabular Editor 2 CLI documented on this page) or the new cross-platform [Tabular Editor CLI](xref:te-cli) (`te`).

Running `TabularEditor.exe` in a CI/CD pipeline does not require a Tabular Editor 3 license. Only users of the Tabular Editor 3 application need a license.

> [!TIP]
> Looking for the new cross-platform CLI? See @te-cli for the Tabular Editor CLI (Limited Public Preview), a successor that runs on Windows, macOS, and Linux.

## TabularEditor.exe vs. the Tabular Editor CLI

The Tabular Editor CLI (`te`) is the cross-platform successor to `TabularEditor.exe`. It's not just a rewrite for macOS and Linux - it adds model editing, inspection, diffing, testing, refresh triggering, and VertiPaq analysis as first-class pipeline operations, none of which were possible with `TabularEditor.exe`. The `te` CLI is in Limited Public Preview (expires 2026-10-31); use `TabularEditor.exe` for production pipelines today.

#### At a glance

| Aspect           | TE2 CLI (`TabularEditor.exe`) | TE CLI (`te`)                               |
| ---------------- | ------------------------------------------------ | -------------------------------------------------------------- |
| 状态               | Stable, production-ready                         | Limited Public Preview (expires 2026-10-31) |
| 平台               | Windows only                                     | Windows, macOS, Linux                                          |
| License required | 否                                                | No (preview); TBD at GA                     |
| Binary           | WinForms app, requires `start /wait` wrapper     | Purpose-built console binary, no wrapper needed                |

#### 身份验证

| Capability                | TE2 CLI (`TabularEditor.exe`) | TE CLI (`te`)                                                                                                                 |
| ------------------------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| Service Principal         | Via MSOLAP connection string                     | Native `--auth spn`, `--auth env`, `--auth managed-identity`; credentials via env vars, stdin, or certificate; OS-native secure credential store |
| Managed identity          | 否                                                | Yes (`--auth managed-identity`), for Azure-hosted runners                                                                     |
| Interactive browser login | 否                                                | Yes (`te auth login`)                                                                                                         |

#### CI/CD

| Capability             | TE2 CLI (`TabularEditor.exe`)                         | TE CLI (`te`)                                                                                                     |
| ---------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| CI annotations         | `-V` (Azure DevOps), `-G` (GitHub) | `--ci vsts`, `--ci github` on every command                                                                                          |
| 非交互模式                  | No explicit flag; errors may prompt                                      | `--non-interactive` global flag - fails fast, no prompts                                                                             |
| Predictable exit codes | Partial                                                                  | `0` = success, `1` = failure (for `te diff`: differences found), `2` = `te diff` comparison error |
| 结构化输出                  | 否                                                                        | `--output-format json/csv/tmdl/tmsl` on every command                                                                                |
| VSTEST results         | `-T` flag                                                                | 在 `validate`、`bpa run` 和 `test run` 命令中使用 `--trx <file>`                                                                             |

#### 部署

| Capability                           | TE2 CLI (`TabularEditor.exe`) | TE CLI (`te`)                                                                                                                                |
| ------------------------------------ | ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Deploy model                         | `-D` flag                                        | `te deploy` with fine-grained flags (`--deploy-roles`, `--deploy-partitions`, `--deploy-connections`, `--deploy-full`, etc.) |
| Generate XMLA/TMSL without deploying | `-X` flag                                        | The default: `te deploy` without `--execute` prints the TMSL to stdout                                                                          |
| BPA gate before deploy               | 否                                                | Built-in; `--skip-bpa` or `--fix-bpa` to override                                                                                                               |
| 连接配置文件                               | 否                                                | `te profile set/list/show` - reusable named profiles per environment                                                                                            |

#### Best Practice Analyzer and model editing

| Capability          | TE2 CLI (`TabularEditor.exe`) | TE CLI (`te`)                                                                                                  |
| ------------------- | ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| Run BPA             | `-A` / `-AX` flags                               | `te bpa run` with `--fail-on warning/error`, `--fix`, `--path` scoping, `--vpax` for VPA-aware rules                              |
| BPA rule management | 否                                                | `te bpa rules add/rm/set/list/disable/enable/init`                                                                                |
| Run C# scripts      | `-S` flag                                        | `te script` - multiple scripts, inline code, stdin, `--validate` compile check, preprocessor symbols (`TECLI`) |
| Run macros          | 否                                                | `te macro run` with `--on <object>` context                                                                                       |
| Set/get properties  | 否                                                | `te get`, `te set`, `te add`, `te rm`, `te mv`                                                                                    |
| DAX formatting      | 否                                                | `te set --format` for model objects, `te util format-dax` / `format-m` for loose expressions                                      |

#### Inspection, refresh, testing and VertiPaq analysis

| Capability               | TE2 CLI (`TabularEditor.exe`) | TE CLI (`te`)                                                                                       |
| ------------------------ | ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| List model objects       | 否                                                | `te ls` with wildcard path filters, `--type`, `--paths-only`, `--output-format bim`                                    |
| Search expressions/names | 否                                                | `te find` with regex and scope (`--in expressions/names/descriptions`)                              |
| Diff two models          | 否                                                | `te diff` - structural comparison with exit code `1` on any difference                                                 |
| Dependency analysis      | 否                                                | `te deps` - upstream/downstream for any object; `--unused` to find dead code                                           |
| Trigger refresh          | 否                                                | `te refresh` with `--type`, `--table`, `--partition`, `--apply-refresh-policy`; dry run by default, `--execute` to run |
| DAX assertion tests      | 否                                                | `te test run` with `--tag`, `--trx`, `--ci`; `te test init/snapshot/compare`                                           |
| Storage statistics       | 否                                                | `te vertipaq` - columns, relationships, partitions; `--export`/`--import` VPAX                                         |

#### Other

| Capability                 | TE2 CLI (`TabularEditor.exe`) | TE CLI (`te`)                                                       |
| -------------------------- | ------------------------------------------------ | -------------------------------------------------------------------------------------- |
| Interactive REPL           | 否                                                | `te interactive` - model-aware shell with persistent history and staged edits          |
| Shell tab completion       | 否                                                | `te completion bash/zsh/pwsh`                                                          |
| TE2 backward compatibility | Native                                           | Built-in compatibility layer - existing `TabularEditor.exe` invocations work unchanged |

For a flag-by-flag mapping from TE2 syntax to the new CLI, see @te-cli-migrate.

**注意：** 由于 TabularEditor.exe 是一个 WinForms 应用程序，直接从 Windows 命令提示符执行会导致线程立即返回到提示符。 This may cause issues in command scripts, etc. To wait for TabularEditor.exe to complete its command-line tasks, always execute it using: `start /wait TabularEditor ...`

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
> 在 [Tabular Editor 2.27.0](https://github.com/TabularEditor/TabularEditor/releases/tag/2.27.0) 中新增 `-S` / `-SHARED` 部署选项标志，这是一次**破坏性变更**。 If you're using the Tabular Editor CLI to perform deployments and you are upgrading from an earlier version of Tabular Editor, make sure to include that flag in your CLI commands, as **shared expressions will otherwise not be deployed**.

> [!TIP]
> `-F` 标志在 [Tabular Editor 2.27.0](https://github.com/TabularEditor/TabularEditor/releases) 中引入。 It is used to perform a "full" deployment and is equivalent to specifying `-O -C -P -S -R -M`.

## 连接到 Azure Analysis Services

You can use any valid SSAS connection string in place of a server name in the command. 以下命令从 Azure Analysis Services 加载模型，并将其在本地保存为 Model.bim 文件：

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

该命令会在 Tabular Editor 中加载 Model.bim 文件，应用指定脚本，并将修改后的模型作为新数据库“MyModel”部署到“localhost\tabular”服务器。 Use the "-O" (Overwrite) switch if you want to overwrite an existing database on the server with the same name.

你也可以用“-B”（Build）开关替代“-D”（Deploy）开关，将修改后的模型输出为新的 Model.bim 文件，而不是直接部署到服务器。 This is useful if you want to deploy the model using another deployment tool, or if you want to inspect the model in Visual Studio or Tabular Editor prior to deployment. It could also be useful for automated build scenarios, where you want to store the modified model as an artifact of the release, before deploying.

## 在部署期间修改连接字符串

假设你的模型包含一个数据源，其连接字符串如下：

```
Provider=SQLOLEDB.1;Data Source=sqldwdev;Persist Security Info=False;Integrated Security=SSPI;Initial Catalog=DW
```

During deployment, you want to modify the string, to point to a UAT or production database. 最佳做法是：先用脚本将整个连接字符串替换为一个占位符值，然后使用 -C 开关将该占位符替换为实际连接字符串。

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

上述命令会将 Model.bim 文件部署为“localhost\\tabular”SSAS 实例上的一个新的 SSAS 数据库“MyModel”。 Before deployment, the script is used to replace all connection strings on provider (legacy) data sources, with the name of the data source, to be used as a placeholder. Assuming we only have a single data source called "SQLDW", the -C switch will then update the connection string, replacing "SQLDW" with the entire string specified.

This technique is useful for scenarios, where you want to deploy the same model to multiple environments that should process data from different (identical) sources - for example, a production, pre-prod or UAT database. 如果使用 Azure DevOps（见下文），建议用变量来保存实际要使用的连接字符串，而不是把它硬编码在命令里。

## 与 Azure DevOps 集成

如果你想在 Azure DevOps 管道中使用 Tabular Editor CLI，那么脚本中执行的任何 TabularEditor.exe 命令都应该使用“-V”开关。 This switch will cause Tabular Editor to output logging commands in a [format readable by Azure DevOps](https://github.com/Microsoft/vsts-tasks/blob/master/docs/authoring/commands.md). These allow Azure DevOps to react properly to errors, etc.

When performing deployment through the command-line, information about unprocessed objects will be outputted to the prompt. In automated deployment scenarios, you may want your build agent to react to situations where objects become unprocessed, for example when adding new columns, changing the DAX expression of a calculated table, etc. In this case, you can use the "-W" switch in addition to the "-V" switch mentioned above, to output this information as warnings. Doing so, will cause the deployment to return the "SucceededWithIssues" status to Azure DevOps, after deployment is completed. You may also use the "-E" switch if you want the deployment to return status "Failed" in case the server reports any DAX errors back after successful deployment.

在 Azure DevOps 管道的“命令行任务”中执行 TabularEditor.exe 时，不需要使用 `start /wait`。 This is because the Command Line Task will not complete, until all threads spawned by the task have terminated. In other words, you need only use `start /wait` if you have additional commands following the call to TabularEditor.exe, and in this case, make sure to use `start /B /wait`. The `/B` switch is required in order for the output from TabularEditor.exe to be correctly piped back to the pipeline log.

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

If you prefer to use a PowerShell task instead of a command line task, you must execute TabularEditor.exe using the `Start-Process` cmdlet, as demonstrated above. 此外，请确保在 PowerShell 脚本中将进程退出代码作为 exit 参数传递，这样 Tabular Editor 中发生的错误就会导致 PowerShell 任务失败：

```powershell
$p = Start-Process -filePath TabularEditor.exe -Wait -NoNewWindow -PassThru `
       -argumentList "`"C:\Projects\My Model\Model.bim`" -D ssasserver databasename -O -C -P -S -V -E -W"
exit $p.ExitCode
```

### 通过环境变量将参数传递给脚本

When executing C# scripts with the `-S` switch in Azure DevOps pipelines, the recommended way to pass parameters is through environment variables rather than command-line arguments. 在 Azure DevOps 管道中使用 `-S` 选项执行 C# 脚本时，建议通过环境变量而非命令行参数传递参数。 C# 脚本可以使用 `Environment.GetEnvironmentVariable()` 读取环境变量；Azure DevOps 会自动将所有管道变量作为环境变量提供。

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

This approach is cleaner and more maintainable than hardcoding values in scripts or using complex string replacement techniques. 这种方法比在脚本中硬编码值或使用复杂的字符串替换方式更简洁、更易维护。 有关在 C# 脚本中使用环境变量的更多信息，请参阅 [C# Scripts - Accessing Environment Variables](xref:csharp-scripts#accessing-environment-variables)。

## 运行 Best Practice Analyzer

你可以使用 "-A" 开关，让 Tabular Editor 扫描模型，找出所有违反最佳实践规则的对象（规则可定义在本机上，位于 %AppData%\..\Local\TabularEditor\BPARules.json 文件中；也可作为注释存储在模型本身中）。 Alternatively, you can specify a path of a .json file containing Best Practice Rules after the "-A" switch, to scan the model using the rules defined in the file. Objects that are in violation will be outputted to the console.

如果你同时使用“-V”开关，则每条规则的严重性级别将决定如何将规则违规情况报告到构建管道：

- Severity = 1 仅作信息提示
- Severity = 2 会触发 WARNING
- Severity >= 3 会触发 ERROR

## 执行数据源架构检查

从 [2.8 版本](https://github.com/TabularEditor/TabularEditor/releases/tag/2.8)开始，你可以使用 -SC（-SCHEMACHECK）开关来验证表的源查询。 This is equivalent to invoking the [Refresh Table Metadata UI](xref:importing-tables-te2#refreshing-table-metadata) except that no changes will be made to the model, but schema differences will be reported to the console. Changed Data Types and columns that were added to the source will be reported as warnings. Missing source columns will be reported as errors. If both the -SC (-SCHEMACHECK) and -S (-SCRIPT) switch are specified, the schema check will run AFTER the script has successfully executed, allowing you to modify Data Source properties before the schema check is performed, for example in order to specify a credential password.

You can also annotate tables and columns if you want the schema check to treat them in a specific way. [更多信息请参见此处](xref:importing-tables-te2#ignoring-objects)。

## 命令行输出与退出代码

The command line provides various details, depending on the switches used and any events encountered during execution. Exit Codes were introduced in [version 2.7.4](https://github.com/TabularEditor/TabularEditor/releases/tag/2.7.4).

| 级别 | 命令            | 信息                                 | Clarification                                                                                                                                                                                                            |
| -- | ------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 错误 | （任意）          | 参数语法无效                             | 向 Tabular Editor CLI 提供了无效的参数                                                                                                                                                                                            |
| 错误 | （任意）          | 未找到文件……                            |                                                                                                                                                                                                                          |
| 错误 | （任意）          | 加载文件时出错……                          | 文件已损坏，或不包含 JSON 格式的有效 TOM 元数据                                                                                                                                                                                            |
| 错误 | （任意）          | 加载模型时出错……                          | 无法连接到所提供的 Analysis Services 实例，或找不到数据库，或数据库元数据已损坏，或数据库的兼容级别不受支持                                                                                                                                                          |
| 错误 | -SCRIPT       | 未找到指定的脚本文件                         |                                                                                                                                                                                                                          |
| 错误 | -SCRIPT       | 脚本编译错误：                            | 脚本包含无效的 C# 语法。 Details will be outputted on the following lines.                                                                                                                                         |
| 错误 | -SCRIPT       | 脚本执行错误：……                          | 执行脚本时发生未处理的异常。                                                                                                                                                                                                           |
| 信息 | -SCRIPT       | 脚本行号 #：……                          | 在脚本中使用 `Info(string)` 或 `Output(string)` 方法。                                                                                                                                                                             |
| 警告 | -SCRIPT       | 脚本警告：……                            | 在脚本中使用 `Warning(string)` 方法。                                                                                                                                                                                             |
| 错误 | -SCRIPT       | 脚本错误：……                            | 在脚本中使用 `Error(string)` 方法。                                                                                                                                                                                               |
| 错误 | -FOLDER, -BIM | -FOLDER 和 -BIM 参数互斥。               | Tabular Editor 无法在一次运行中将当前加载的模型同时保存为文件夹结构和 .bim 文件。                                                                                                                                                      |
| 错误 | -ANALYZE      | 未找到规则文件：……                         |                                                                                                                                                                                                                          |
| 错误 | -ANALYZE      | 无效的规则文件：……                         | 指定的 BPA 规则文件已损坏或不包含有效的 JSON。                                                                                                                                                                                             |
| 信息 | -ANALYZE      | ……违反规则……                           | Best Practice Analyzer 针对严重性级别为 1 或以下规则的结果。                                                                                                                                                                              |
| 警告 | -ANALYZE      | ……违反规则……                           | Best Practice Analyzer 针对严重性级别 2 的规则的结果。                                                                                                                                                                                 |
| 错误 | -ANALYZE      | ……违反规则……                           | Best Practice Analyzer 针对严重性级别 3 或更高的规则的结果。                                                                                                                                                                              |
| 错误 | -DEPLOY       | 部署失败！……                            | 由 Analysis Services 实例直接返回的失败原因（例如：找不到数据库、不允许数据库覆盖等）                                                                                                                                                                     |
| 信息 | -DEPLOY       | 未处理的对象: ……         | Objects that are in state "NoData" or "CalculationNeeded" after successful deployment. Use the -W switch to treat these as Level=Warning.                                                |
| 警告 | -DEPLOY       | 对象不处于"Ready"状态: …… | 成功部署后处于 "DependencyError"、"EvaluationError" 或 "SemanticError" 状态的对象。 如果使用 -W 开关，还包括处于“NoData”或“CalculationNeeded”状态的对象。如果使用 -W 开关，还包括处于“NoData”或“CalculationNeeded”状态的对象。                                                |
| 警告 | -DEPLOY       | X 上发生错误：……                         | Objects containing invalid DAX after successful deployment (measures, calculated columns, calculated tables, roles). Use the -E switch to treat these as Level=Error. |

如果检测到任何级别为“Error”的输出，Tabular Editor 将返回 Exit Code = 1。 Otherwise 0.
