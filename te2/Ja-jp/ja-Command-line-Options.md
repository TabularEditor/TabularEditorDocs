# Command Line

Tabular Editorは、コマンドラインから実行してさまざまなタスクを実行することができ、自動ビルドやデプロイメントシナリオなどで有用です。

**Note:** TabularEditor.exeはWinFormsアプリケーションなので、Windowsのコマンドプロンプトから直接実行すると、スレッドがすぐにプロンプトに戻ります。このため、コマンドスクリプトなどで問題が発生します。TabularEditor.exeのコマンドラインタスクが完了するのを待つには、常に以下の方法で実行してください。`start /wait TabularEditor ...` を使って実行してください。

Tabular Editorで利用できるコマンドラインオプションを表示するには、次のコマンドを実行します。

**Windows Command line:**

```shell
start /wait TabularEditor.exe /?
```

**PowerShell:**

```powershell
$p = Start-Process -filePath TabularEditor.exe -Wait -NoNewWindow -PassThru -ArgumentList "/?"
```

Output:
```
Tabular Editor 2.16.0 (build 2.16.7781.40242)
--------------------------------
Usage:

TABULAREDITOR ( file | server database ) [-S script1 [script2] [...]]
    [-SC] [-A [rules] | -AX rules] [(-B | -F) output [id]] [-V | -G] [-T resultsfile]
    [-D [server database [-L user pass] [-O [-C [plch1 value1 [plch2 value2 [...]]]]
        [-P [-Y]] [-R [-M]]]
        [-X xmla_script]] [-W] [-E]]

file                Full path of the Model.bim file or database.json model folder to load.
server              Server\instance name or connection string from which to load the model
database            Database ID of the model to load
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
  -O / -OVERWRITE     Allow deploy (overwrite) of an existing database.
    -C / -CONNECTIONS   Deploy (overwrite) existing data sources in the model. After the -C switch, you
                        can (optionally) specify any number of placeholder-value pairs. Doing so, will
                        replace any occurrence of the specified placeholders (plch1, plch2, ...) in the
                        connection strings of every data source in the model, with the specified values
                        (value1, value2, ...).
    -P / -PARTITIONS    Deploy (overwrite) existing table partitions in the model.
      -Y / -SKIPPOLICY    Do not overwrite partitions that have Incremental Refresh Policies defined.
    -R / -ROLES         Deploy roles.
      -M / -MEMBERS       Deploy role members.
  -X / -XMLA        No deployment. Generate XMLA/TMSL script for later deployment instead.
    xmla_script       File name of the new XMLA/TMSL script output.
  -W / -WARN        Outputs information about unprocessed objects as warnings.
  -E / -ERR         Returns a non-zero exit code if Analysis Services returns any error messages after
                      the metadata was deployed / updated.
```

## Connecting to Azure Analysis Services

コマンドのサーバー名の代わりに、任意の有効なSSAS接続文字列を使用できます。次のコマンドは、Azure Analysis Servicesからモデルをロードし、それをModel.bimファイルとしてローカルに保存します。

**Windows Command Line:**

```shell
start /wait TabularEditor.exe "Provider=MSOLAP;Data Source=asazure://northeurope.asazure.windows.net/MyAASServer;User ID=xxxx;Password=xxxx;Persist Security Info=True;Impersonation Level=Impersonate" MyModelDB -B "C:\Projects\FromAzure\Model.bim"
```

**PowerShell:**

```powershell
$p = Start-Process -filePath TabularEditor.exe -Wait -NoNewWindow -PassThru `
       -ArgumentList "`"Provider=MSOLAP;Data Source=asazure://northeurope.asazure.windows.net/MyAASServer;User ID=xxxx;Password=xxxx;Persist Security Info=True;Impersonation Level=Impersonate`" MyModelDB -B C:\Projects\FromAzure\Model.bim"
```

Azure Active Directory 認証ではなく、Service Principal (Application ID and Key) を使って接続したい場合は、以下のような接続文字列を使用します。

```
Provider=MSOLAP;Data Source=asazure://northeurope.asazure.windows.net/MyAASServer;User ID=app:<APPLICATION ID>@<TENANT ID>;Password=<APPLICATION KEY>;Persist Security Info=True;Impersonation Level=Impersonate
```

## Automating script changes

Tabular Editor内でスクリプトを作成し、デプロイ前にこのスクリプトをModel.bimファイルに適用したい場合、コマンドラインオプション「-S」（Script）を使用することができます。

**Windows Command Line:**

```shell
start /wait TabularEditor.exe "C:\Projects\MyModel\Model.bim" -S "C:\Projects\MyModel\MyScript.cs" -D localhost\tabular MyModel
```

**PowerShell:**

```powershell
$p = Start-Process -filePath TabularEditor.exe -Wait -NoNewWindow -PassThru `
       -ArgumentList "`"C:\Projects\MyModel\Model.bim`" -S `"C:\Projects\MyModel\MyScript.cs`" -D `"localhost\tabular`" `"MyModel`""
```

このコマンドは、Model.bimファイルをTabular Editorで読み込み、指定されたスクリプトを適用して、変更されたモデルを新しいデータベース "MyModel" として "localhosttabular" サーバーにデプロイします。サーバー上の同名の既存データベースを上書きする場合は、"-O" (Overwrite) スイッチを使用します。

D" (Deploy) スイッチの代わりに "-B" (Build) スイッチを使用すると、変更したモデルを直接デプロイする代わりに、新しいModel.bimファイルとして出力できます。これは、他のデプロイツールを使ってモデルをデプロイしたい場合や、デプロイ前にVisual StudioやTabular Editorでモデルを検査したい場合などに便利です。また、自動ビルドのシナリオで、デプロイ前に修正したモデルをリリースの成果物として保存したい場合にも有用です。

## Modifying connection strings during deployment

以下のような接続文字列を持つData Sourceを含むモデルがあると仮定します。

```
Provider=SQLOLEDB.1;Data Source=sqldwdev;Persist Security Info=False;Integrated Security=SSPI;Initial Catalog=DW
```

デプロイ時に、この文字列を変更して、UATまたは本番用データベースを指すようにしたい。そのためには、まず接続文字列全体をプレースホルダーの値に変更するスクリプトを使用し、次に-Cスイッチを使用してプレースホルダーと実際の接続文字列を入れ替えるのが最適な方法です。

以下のスクリプトを "ClearConnectionStrings.cs "などと呼ばれるファイルに記述する。

```csharp
// This will replace the connection string of all Provider (legacy) data sources in the model
// with a placeholder based on the name of the data source. E.g., if your data source is called
// "SQLDW", the connection string after running this script would be "SQLDW":

foreach(var ds in Model.DataSources.OfType<ProviderDataSource>())
    ds.ConnectionString = ds.Name;
```

以下のコマンドでTabular Editorにスクリプトの実行を指示し、プレースホルダーの入れ替えを実行できます。

**Windows Command Line:**

```shell
start /wait TabularEditor.exe "Model.bim" -S "ClearConnectionStrings.cs" -D localhost\tabular MyModel -C "SQLDW" "Provider=SQLOLEDB.1;Data Source=sqldwprod;Persist Security Info=False;Integrated Security=SSPI;Initial Catalog=DW"
```

**PowerShell:**

```powershell
$p = Start-Process -filePath TabularEditor.exe -Wait -NoNewWindow -PassThru `
       -ArgumentList "Model.bim -S ClearConnectionStrings.cs -D localhost\tabular MyModel -C SQLDW `"Provider=SQLOLEDB.1;Data Source=sqldwprod;Persist Security Info=False;Integrated Security=SSPI;Initial Catalog=DW`""
```

上記のコマンドは、Model.bimファイルを "localhosttabular" SSASインスタンスに "MyModel" という新しいSSASデータベースとしてデプロイするものです。デプロイ前に、このスクリプトは、プロバイダー（レガシー）データソースのすべての接続文字列を、プレースホルダーとして使用するデータソースの名前に置き換えるため使用されます。「SQLDW」という名前のデータソースが1つだけあると仮定すると、-Cスイッチによって接続文字列が更新され、「SQLDW」が指定した文字列全体に置き換えられます。

このテクニックは、異なる（同一の）ソースからのデータを処理する複数の環境に同じモデルをデプロイしたい場合、たとえば、プロダクション、プレプロダクション、UATデータベースなどのシナリオで有用です。Azure DevOps（下記参照）を使用する場合、実際に使用する接続文字列をコマンドにハードコードするのではなく、変数を使用して保存することを検討してください。

## Integration with Azure DevOps

Azure DevOpsパイプライン内でTabular Editor CLIを使用したい場合、スクリプトで実行されるTabularEditor.exeコマンドに「-V」スイッチを使用する必要があります。このスイッチにより、Tabular Editorはログコマンドを[Azure DevOpsが読める形式](https://github.com/Microsoft/vsts-tasks/blob/master/docs/authoring/commands.md)で出力するようになります。これにより、Azure DevOpsはエラーなどに適切に対応できるようになります。

コマンドラインを通じてデプロイメントを実行する場合、未処理のオブジェクトに関する情報がプロンプトに出力されます。自動化されたデプロイメントシナリオでは、たとえば新しいカラムを追加したり、計算テーブルのDAX式を変更したりするときなど、オブジェクトが未処理の状況にビルドエージェントを反応させたい場合があります。この場合、前述の「-V」スイッチに加えて「-W」スイッチを使用することで、この情報を警告として出力することができる。そうすることで、デプロイ完了後Azure DevOpsに「SucceededWithIssues」ステータスが返されます。また、デプロイ成功後にサーバーからDAXエラーが報告された場合、デプロイがステータス「Failed」を返すようにしたい場合は、「-E」スイッチを使用することもできます。

Azure DevOpsパイプラインのCommand Line Task内でTabularEditor.exeを実行する場合、`start /wait`は必要ありません。これは、タスクによって生成されたすべてのスレッドが終了するまで、Command Line Taskが完了しないためです。言い換えれば、TabularEditor.exeの呼び出しの後に追加のコマンドがある場合にのみ、`start /wait` を使用する必要があります。TabularEditor.exeからの出力をパイプラインログに正しく戻すには、`/B`スイッチが必要です。

```shell
TabularEditor.exe "C:\Projects\My Model\Model.bim" -D ssasserver databasename -O -C -P -V -E -W
```

Or with multiple commands:

```shell
start /B /wait TabularEditor.exe "C:\Projects\Finance\Model.bim" -D ssasserver Finance -O -C -P -V -E -W
start /B /wait TabularEditor.exe "C:\Projects\Sales\Model.bim" -D ssasserver Sales -O -C -P -V -E -W
```

下図は、Azure DevOpsでこのようなビルドがどのように見えるかを示しています。

![image](https://user-images.githubusercontent.com/8976200/27128146-bc044356-50fd-11e7-9a67-b893fc48ea50.png)

何らかの理由でデプロイに失敗した場合、「-W」スイッチを使用しているかどうかにかかわらず、Tabular EditorはAzure DevOpsに「Failed」ステータスを返します。

Azure DevOpsとTabular Editorの詳細については、このブログシリーズ](https://tabulareditor.github.io/2019/02/20/DevOps1.html) (とくに[第3章](https://tabulareditor.github.io/2019/10/08/DevOps3.html) 以降）をご覧ください。

### Azure DevOps PowerShell Task

コマンドラインタスクの代わりにPowerShellタスクを使いたい場合は、上記のように `Start-Process` コマンドレットを使ってTabularEditor.exeを実行する必要があります。さらに、PowerShellスクリプトのexitパラメーターにプロセスの終了コードを渡して、Tabular Editorで発生したエラーがPowerShellタスクの失敗の原因にしてください。

```powershell
$p = Start-Process -filePath TabularEditor.exe -Wait -NoNewWindow -PassThru `
       -argumentList "`"C:\Projects\My Model\Model.bim`" -D ssasserver databasename -O -C -P -V -E -W"
exit $p.ExitCode
```

## Running the Best Practice Analyzer

「-A」スイッチを使用すると、ローカルマシン（%AppData%... \LocalTabularEditor</BPARules.json file）またはモデル自体のアノテーションとして定義されたベストプラクティスルールに違反するすべてのオブジェクトをTabular Editorでモデルスキャンするように設定できます。また、「-A」スイッチの後にベストプラクティスルールを含む.jsonファイルのパスを指定すると、そのファイルに定義されたルールを使ってモデルをスキャンできます。違反のあるオブジェクトは、コンソールに出力されます。

「-V」スイッチも使用している場合、各ルールの深刻度によって、ルール違反がビルドパイプラインにどのように報告されるかが決まります。

* Severity = 1 は情報提供のみとなります
* Severity = 2 は警告を発生させます
* Severity >= 3 はエラー（ERROR）を発生させます

## Performing a data source schema check

[バージョン 2.8](https://github.com/otykier/TabularEditor/releases/tag/2.8) では、-SC (-SCHEMACHECK) スイッチを使用して、テーブルソースクエリを検証できます。これは [Refresh Table Metadata UI](/Importing-Tables#refreshing-table-metadata) の実行と同等ですが、モデルへの変更は行われませんが、スキーマの相違はコンソールに報告されます。変更されたデータ型とソースに追加されたカラムは、警告としてレポートされます。ソースにない列はエラーとして報告されます。SC（-SCHEMACHECK）スイッチと-S（-SCRIPT）スイッチの両方を指定すると、スクリプトが正常に実行された後にスキーマ チェックが実行されるため、スキーマ チェックが実行される前にデータ ソースのプロパティを変更できます（たとえば、資格情報パスワードを指定するためなど）。

また、スキーマチェックを行う際に、テーブルやカラムを特定の方法で処理したい場合は、アノテーションを付けることができます。[詳細はこちら](/Importing-Tables#ignoring-objects)を参照してください。

## Command Line output and Exit Codes

コマンドラインは、使用されたスイッチや実行中遭遇したイベントに応じて、さまざまな詳細を提供します。Exit Codesは [version 2.7.4](https://github.com/otykier/TabularEditor/releases/tag/2.7.4) で導入されました。

|Level|Command|Message|Clarification|
|---|---|---|---|
|Error|(Any)|Invalid argument syntax|Tabular Editor CLIに無効な引数が指定されました。|
|Error|(Any)|File not found: ...||
|Error|(Any)|Error loading file: ...|ファイルが壊れているか、有効な TOM メタデータが JSON 形式で含まれていない。|
|Error|(Any)|Error loading model: ...|提供された Analysis Services インスタンスに接続できない、データベースが見つからない、データベースのメタデータが破損している、またはサポートされている互換性レベルのデータベースでない|
|Error|-SCRIPT|Specified script file not found||
|Error|-SCRIPT|Script compilation errors:|スクリプトに無効なC#の構文が含まれていました。詳細は以下の行に出力されます。
|Error|-SCRIPT|Script execution error: ...|スクリプトの実行時に未処理の例外が発生しました。|
|Information|-SCRIPT|Script line #: ...|スクリプト内で `Info(string)` メソッドまたは `Output(string)` メソッドを使用する。|
|Warning|-SCRIPT|Script warning: ...|スクリプト内で `Warning(string)` メソッドを使用する。|
|Error|-SCRIPT|Script error: ...|スクリプト内で `Error(string)` メソッドを使用する。|
|Error|-FOLDER, -BIM|-FOLDER and -BIM arguments are mutually exclusive.|Tabular Editorで、現在ロードされているモデルを一度の実行でフォルダー構造および.bimファイルに保存できない。|
|Error|-ANALYZE|Rulefile not found: ...||
|Error|-ANALYZE|Invalid rulefile: ...|指定されたBPAルールファイルが破損しているか、有効なJSONを含んでいません。|
|Information|-ANALYZE|... violates rule ...|重大度レベル1以下のルールに対するベストプラクティス・アナライザーの結果。|
|Warning|-ANALYZE|... violates rule ...|重大度レベル2のルールに対するベストプラクティス・アナライザーの結果。|
|Error|-ANALYZE|... violates rule ...|重大度レベル3以上のルールに対するベストプラクティス・アナライザーの結果。|
|Error|-DEPLOY|Deployment failed! ...|Analysis Serviceインスタンスから直接返される失敗の理由（例：データベースが見つからない、データベースのオーバーライドが許可されていない、など）。|
|Information|-DEPLOY|Unprocessed object: ...|デプロイに成功した後、状態が "NoData" または "CalculationNeeded" になっているオブジェクト。W スイッチを使用すると、これらを Level=Warning として扱います。|
|Warning|-DEPLOY|Object not in "Ready" state: ...|デプロイに成功した後、状態が "DependencyError", "EvaluationError" または "SemanticError" であるオブジェクト。Wスイッチを使用した場合、状態「NoData」または「CalculationNeeded」のオブジェクトも含まれます。|
|Warning|-DEPLOY|Error on X:...|デプロイに成功した後に、無効な DAX を含むオブジェクト (メジャー、計算列、計算テーブル、ロール) が表示されます。これらを Level=Error として処理するには、-E スイッチを使用します。|

Error "レベルの出力に遭遇した場合、Tabular EditorはExit Code = 1を返します。それ以外は0です。
