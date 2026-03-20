---
uid: 命令行选项
title: 命令行
author: Daniel Otykier
updated: 2021-08-26
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      none: true
---

# 命令行

Tabular Editor 可通过命令行执行以执行各种任务，这在自动化构建和部署等场景中可能很有用。

**注意：** 由于 TabularEditor.exe 是一个 WinForms 应用程序，直接从 Windows 命令提示符执行会导致线程立即返回到提示符。 这可能会在命令脚本等场景中引发问题。 如需等待 TabularEditor.exe 完成其命令行任务，请始终使用以下方式执行：`start /wait TabularEditor ...`

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
用法:

TABULAREDITOR ( file | server database | -L [name] ) [-S script1 [script2] [...]]
    [-SC] [-A [rules] | -AX rules] [(-B | -F | -TMDL) output [id]] [-V | -G] [-T resultsfile]
    [-D [server database [-L user pass] [-F | -O [-C [plch1 value1 [plch2 value2 [...]]]]
        [-P [-Y]] [-S] [-R [-M]]]
        [-X xmla_script]] [-W] [-E]]

file                要加载的 Model.bim 文件或 database.json 模型文件夹的完整路径。
server              用于加载模型的服务器\\实例名称或连接字符串
database            要加载的模型的数据库 ID。如果为空 (""), 则选择服务器上第一个可用
                      的数据库。
-L / -LOCAL         连接到 Analysis Services 的 Power BI Desktop (本地) 实例。如果未指定
                      name，则假定恰好有 1 个实例正在运行。否则，name 应与 Power BI Desktop
                      中加载的 .pbix 文件名匹配。
-S / -SCRIPT        在加载后对模型执行指定脚本。
  scriptN             要执行的包含 C# Script 的一个或多个文件的完整路径，或内联
                      脚本。
-SC / -SCHEMACHECK  尝试连接到所有 Provider 数据源，以检测表架构更改。输出...
                      ...对于数据类型不匹配和未映射的源列的警告
                      ...对于未映射的模型列的错误。
-A / -ANALYZE       运行 Best Practice Analyzer 并将结果输出到控制台。
  rules               可选：要分析的附加 BPA 规则文件路径或 URL。如果指定，则不会针对
                      本地用户/本地计算机规则分析模型，但仍会应用模型中定义的规则。
-AX / -ANALYZEX     与 -A / -ANALYZE 相同，但排除在模型注释中指定的规则。
-B / -BIM / -BUILD  将模型 (可选脚本执行后) 保存为 Model.bim 文件。
  output              要保存到的 Model.bim 文件的完整路径。
  id                  保存时分配给 Database 对象的可选 id/name。
-F / -FOLDER        将模型 (可选脚本执行后) 保存为文件夹结构。
  output              要保存到的文件夹的完整路径。如果不存在则创建该文件夹。
  id                  保存时分配给 Database 对象的可选 id/name。
-TMDL               将模型 (可选脚本执行后) 保存为 TMDL 文件夹结构。
  output              要保存到的 TMDL 文件夹的完整路径。如果不存在则创建该文件夹。
  id                  保存时分配给 Database 对象的可选 id/name。
-V / -VSTS          输出 Visual Studio Team Services 日志记录命令。
-G / -GITHUB        输出 GitHub Actions 工作流命令。
-T / -TRX         生成包含执行详细信息的 VSTEST (trx) 文件。
  resultsfile       VSTEST XML 文件的文件名。
-D / -DEPLOY        命令行部署
                      如果未指定其他参数，此开关会将模型元数据保存回源 (文件或数据库)。
  server              要部署到的服务器名称或连接字符串到 Analysis Services。
  database            要部署 (创建/覆盖) 的数据库 ID。
  -L / -LOGIN         连接到服务器时禁用集成安全性。指定:
    user                用户名 (必须是服务器上具有管理员权限的用户)
    pass                密码
  -F / -FULL          部署完整模型元数据，允许覆盖现有数据库。
  -O / -OVERWRITE     允许部署 (覆盖) 现有数据库。
    -C / -CONNECTIONS   部署 (覆盖) 模型中的现有数据源。在 -C 开关之后，您可以 (可选) 指定
                        任意数量的占位符-值对。这样会将模型中每个数据源的连接字符串中出现的
                        指定占位符 (plch1, plch2, ...) 替换为指定的值 (value1, value2, ...)。
    -P / -PARTITIONS    部署 (覆盖) 模型中的现有表分区。
      -Y / -SKIPPOLICY    不要覆盖已定义增量刷新策略的分区。
    -S / -SHARED        部署 (覆盖) 共享表达式。
    -R / -ROLES         部署角色。
      -M / -MEMBERS       部署角色成员。
  -X / -XMLA        不部署。改为生成用于稍后部署的 XMLA/TMSL 脚本。
    xmla_script       新 XMLA/TMSL 脚本输出的文件名。
  -W / -WARN        将有关未处理对象的信息作为警告输出。
  -E / -ERR         如果 Analysis Services 在部署/更新元数据后返回任何错误信息，则返回
                      非零退出代码。
```

> [!WARNING]
> 在 [Tabular Editor 2.27.0](https://github.com/TabularEditor/TabularEditor/releases/tag/2.27.0) 中新增 `-S` / `-SHARED` 部署选项标志，这是一次**破坏性变更**。 如果你使用 Tabular Editor CLI 执行部署，并且正在从更早版本的 Tabular Editor 升级，请务必在 CLI 命令中包含该标志，否则**不会部署共享表达式**。

> [!TIP]
> `-F` 标志在 [Tabular Editor 2.27.0](https://github.com/TabularEditor/TabularEditor/releases) 中引入。 它用于执行“完整”部署，等同于指定 `-O -C -P -S -R -M`。

## 连接到 Azure Analysis Services

在命令中，你可以用任何有效的 SSAS 连接字符串替代服务器名称。 以下命令从 Azure Analysis Services 加载模型，并将其在本地保存为 Model.bim 文件：

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

该命令会在 Tabular Editor 中加载 Model.bim 文件，应用指定脚本，并将修改后的模型作为新数据库“MyModel”部署到“localhost\tabular”服务器。 如果你希望覆盖服务器上已存在的同名数据库，请使用“-O”（Overwrite）开关。

你也可以用“-B”（Build）开关替代“-D”（Deploy）开关，将修改后的模型输出为新的 Model.bim 文件，而不是直接部署到服务器。 当你想用其他部署工具来部署模型，或希望在部署前先在 Visual Studio 或 Tabular Editor 中检查模型时，这会很有用。 在自动化构建场景中也同样实用：你可以在部署前，将修改后的模型作为发布产物进行保存。

## 在部署期间修改连接字符串

假设你的模型包含一个数据源，其连接字符串如下：

```
Provider=SQLOLEDB.1;Data Source=sqldwdev;Persist Security Info=False;Integrated Security=SSPI;Initial Catalog=DW
```

在部署期间，你希望修改该字符串，使其指向 UAT 或生产数据库。 最佳做法是：先用脚本将整个连接字符串替换为一个占位符值，然后使用 -C 开关将该占位符替换为实际连接字符串。

将以下脚本放到名为“ClearConnectionStrings.cs”或类似名称的文件中：

```csharp
// 这将把模型中所有 Provider（旧版）数据源的连接字符串替换为
// 基于数据源名称的占位符。例如，如果你的数据源名为
// "SQLDW"，运行此脚本后，连接字符串将变为 "SQLDW"：

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

上述命令会将 Model.bim 文件部署为“localhost\\tabular”SSAS 实例上的一个新的 SSAS 数据库“MyModel”。 在部署之前，脚本会先把所有提供程序（旧版）数据源上的连接字符串替换为数据源名称，作为占位符使用。 假设我们只有一个名为“SQLDW”的数据源，那么 -C 开关会更新连接字符串，将“SQLDW”替换为指定的完整字符串。

当你需要将同一个模型部署到多个环境、并让它们从不同（结构相同）的来源处理数据时，这个技巧就很有用——例如生产、预生产或 UAT 数据库。 如果使用 Azure DevOps（见下文），建议用变量来保存实际要使用的连接字符串，而不是把它硬编码在命令里。

## 与 Azure DevOps 集成

如果你想在 Azure DevOps 管道中使用 Tabular Editor CLI，那么脚本中执行的任何 TabularEditor.exe 命令都应该使用“-V”开关。 该开关会让 Tabular Editor 以 [Azure DevOps 可读取的格式](https://github.com/Microsoft/vsts-tasks/blob/master/docs/authoring/commands.md) 输出日志命令。 这样 Azure DevOps 才能正确响应错误等情况。

通过命令行执行部署时，未处理对象的相关信息会输出到命令提示符中。 在自动化部署场景中，你可能希望构建代理能够对对象变为未处理的情况做出响应，例如新增列、修改计算表格的 DAX 表达式等。 这种情况下，除了上面提到的“-V”开关之外，你还可以使用“-W”开关，将这些信息以警告的形式输出。 这样一来，部署完成后会向 Azure DevOps 返回“SucceededWithIssues”状态。 如果你希望在成功部署后，服务器报告任何 DAX 错误时让部署返回“Failed”状态，也可以使用“-E”开关。

在 Azure DevOps 管道的“命令行任务”中执行 TabularEditor.exe 时，不需要使用 `start /wait`。 因为命令行任务会一直等待，直到该任务启动的所有线程都已终止，才会结束。 换句话说，只有在调用 TabularEditor.exe 之后还要执行其他命令时，才需要使用 `start /wait`；并且在这种情况下，请确保使用 `start /B /wait`。 需要使用 `/B` 开关，才能将 TabularEditor.exe 的输出正确地通过管道回传到流水线日志中。

```shell
TabularEditor.exe "C:\Projects\My Model\Model.bim" -D ssasserver databasename -O -C -P -S -V -E -W
```

或者执行多条命令：

```shell
start /B /wait TabularEditor.exe "C:\Projects\Finance\Model.bim" -D ssasserver Finance -O -C -P -S -V -E -W
start /B /wait TabularEditor.exe "C:\Projects\Sales\Model.bim" -D ssasserver Sales -O -C -P -S -V -E -W
```

下图展示了此类构建在 Azure DevOps 中的样子：

![image](https://user-images.githubusercontent.com/8976200/27128146-bc044356-50fd-11e7-9a67-b893fc48ea50.png)

如果部署因任何原因失败，Tabular Editor 都会向 Azure DevOps 返回“Failed”状态，无论你是否使用了“-W”开关。

如需了解 Azure DevOps 与 Tabular Editor 的更多信息，请参阅[这套博客系列](https://tabulareditor.github.io/2019/02/20/DevOps1.html)（尤其是[第 3 章](https://tabulareditor.github.io/2019/10/08/DevOps3.html)及之后的内容）。

### Azure DevOps PowerShell 任务

如果你更倾向于使用 PowerShell 任务而不是命令行任务，则必须像上面演示的那样，使用 `Start-Process` cmdlet 来执行 TabularEditor.exe。 此外，请确保在 PowerShell 脚本中将进程退出代码作为 exit 参数传递，这样 Tabular Editor 中发生的错误就会导致 PowerShell 任务失败：

```powershell
$p = Start-Process -filePath TabularEditor.exe -Wait -NoNewWindow -PassThru `
       -argumentList "`"C:\Projects\My Model\Model.bim`" -D ssasserver databasename -O -C -P -S -V -E -W"
exit $p.ExitCode
```

### 通过环境变量将参数传递给脚本

在 Azure DevOps 管道中使用 `-S` 选项执行 C# 脚本时，建议通过环境变量而非命令行参数传递参数。 C# 脚本可以使用 `Environment.GetEnvironmentVariable()` 读取环境变量；Azure DevOps 会自动将所有管道变量作为环境变量提供。

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

这种方法比在脚本中硬编码值或使用复杂的字符串替换方式更简洁、更易维护。 有关在 C# 脚本中使用环境变量的更多信息，请参阅 [C# Scripts - Accessing Environment Variables](xref:csharp-scripts#accessing-environment-variables)。

## 运行 Best Practice Analyzer

你可以使用 "-A" 开关，让 Tabular Editor 扫描模型，找出所有违反最佳实践规则的对象（规则可定义在本机上，位于 %AppData%\..\Local\TabularEditor\BPARules.json 文件中；也可作为注释存储在模型本身中）。 或者，你也可以在 "-A" 开关后指定一个包含最佳实践规则的 .json 文件路径，以使用该文件中定义的规则来扫描模型。 违规的对象将输出到控制台。

如果你同时使用“-V”开关，则每条规则的严重性级别将决定如何将规则违规情况报告到构建管道：

- Severity = 1 仅作信息提示
- Severity = 2 会触发 WARNING
- Severity >= 3 会触发 ERROR

## 执行数据源架构检查

从 [2.8 版本](https://github.com/TabularEditor/TabularEditor/releases/tag/2.8)开始，你可以使用 -SC（-SCHEMACHECK）开关来验证表的源查询。 这相当于调用[刷新表元数据 UI](xref:importing-tables-te2#refreshing-table-metadata)，但不会对模型做任何更改，而是会将架构差异报告到控制台。 数据类型更改以及源中新增的列将以警告形式报告。 源中缺失的列将以错误形式报告。 如果同时指定了 -SC（-SCHEMACHECK）和 -S（-SCRIPT）开关，则架构检查会在脚本成功执行之后运行。这样你就可以在执行架构检查之前修改数据源属性，例如用于指定凭据密码。

如果你希望架构检查以特定方式处理表和列，也可以为它们添加注释。 [更多信息请参见此处](xref:importing-tables-te2#ignoring-objects)。

## 命令行输出与退出代码

命令行会根据所使用的开关以及执行过程中遇到的事件，提供各类详细信息。 退出代码在 [2.7.4 版本](https://github.com/TabularEditor/TabularEditor/releases/tag/2.7.4) 中引入。

| 级别 | 命令            | 信息                                 | 说明                                                                                                                      |
| -- | ------------- | ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| 错误 | （任意）          | 参数语法无效                             | 向 Tabular Editor CLI 提供了无效的参数                                                                                           |
| 错误 | （任意）          | 未找到文件……                            |                                                                                                                         |
| 错误 | （任意）          | 加载文件时出错……                          | 文件已损坏，或不包含 JSON 格式的有效 TOM 元数据                                                                                           |
| 错误 | （任意）          | 加载模型时出错……                          | 无法连接到所提供的 Analysis Services 实例，或找不到数据库，或数据库元数据已损坏，或数据库的兼容级别不受支持                                                         |
| 错误 | -SCRIPT       | 未找到指定的脚本文件                         |                                                                                                                         |
| 错误 | -SCRIPT       | 脚本编译错误：                            | 脚本包含无效的 C# 语法。 详细信息将输出在后续几行中。                                                                                           |
| 错误 | -SCRIPT       | 脚本执行错误：……                          | 执行脚本时发生未处理的异常。                                                                                                          |
| 信息 | -SCRIPT       | 脚本行号 #：……                          | 在脚本中使用 `Info(string)` 或 `Output(string)` 方法。                                                                            |
| 警告 | -SCRIPT       | 脚本警告：……                            | 在脚本中使用 `Warning(string)` 方法。                                                                                            |
| 错误 | -SCRIPT       | 脚本错误：……                            | 在脚本中使用 `Error(string)` 方法。                                                                                              |
| 错误 | -FOLDER, -BIM | -FOLDER 和 -BIM 参数互斥。               | Tabular Editor 无法在一次运行中将当前加载的模型同时保存为文件夹结构和 .bim 文件。                                                     |
| 错误 | -ANALYZE      | 未找到规则文件：……                         |                                                                                                                         |
| 错误 | -ANALYZE      | 无效的规则文件：……                         | 指定的 BPA 规则文件已损坏或不包含有效的 JSON。                                                                                            |
| 信息 | -ANALYZE      | …… 违反规则……                          | Best Practice Analyzer 针对严重性级别为 1 或以下规则的结果。                                                                             |
| 警告 | -ANALYZE      | …… 违反规则 ……                         | Best Practice Analyzer 针对严重性级别 2 的规则的结果。                                                                                |
| 错误 | -ANALYZE      | …… 违反规则 ……                         | Best Practice Analyzer 针对严重性级别 3 或更高的规则的结果。                                                                             |
| 错误 | -DEPLOY       | 部署失败！ ……                           | 由 Analysis Services 实例直接返回的失败原因（例如：找不到数据库、不允许数据库覆盖等）                                                                    |
| 信息 | -DEPLOY       | 未处理的对象: ……         | 成功部署后处于 "NoData" 或 "CalculationNeeded" 状态的对象。 使用 -W 开关将这些按 Level=Warning 处理。                                            |
| 警告 | -DEPLOY       | 对象不处于"Ready"状态: …… | 成功部署后处于 "DependencyError"、"EvaluationError" 或 "SemanticError" 状态的对象。 如果使用 -W 开关，还包括处于“NoData”或“CalculationNeeded”状态的对象。 |
| 警告 | -DEPLOY       | X 上发生错误：……                         | 成功部署后包含无效 DAX 的对象（度量值、计算列、计算表格、角色）。 使用 -E 选项将这些视为 Level=Error。                                                          |

如果检测到任何级别为“Error”的输出，Tabular Editor 将返回 Exit Code = 1。 否则返回 0。
