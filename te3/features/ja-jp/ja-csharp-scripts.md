# C# スクリプト

本書は、Tabular Editor 3のC#スクリプト機能の紹介です。このドキュメントの情報は変更される可能性があります。また、[useful-script-snippets](TabularEditorDocs\te2\Useful-script-snippets.md)の記事で、Tabular Editorのスクリプト機能を使ってできることの実例をいくつか紹介していますので、ぜひチェックしてみてください。

## なぜC#スクリプトなのか？

Tabular EditorのUIの目標は、Tabularモデルの構築時に一般的に必要とされるほとんどのタスクを簡単に実行できるようにすることです。たとえば、複数のメジャーの表示フォルダーを一度に変更するには、エクスプローラー・ツリーでオブジェクトを選択し、ドラッグ・アンド・ドロップすればよいだけです。エクスプローラツリーの右クリックによるコンテキストメニューでは、パースペクティブからのオブジェクトの追加/削除、複数のオブジェクトの名前変更など、多くの作業を便利に行うことができます。

しかし、UIから簡単に実行できない一般的なワークフロータスクも多くあります。このため、Tabular EditorはC#スクリプトを提供し、上級ユーザーがC#構文を使用してスクリプトを書き、ロードされたTabularモデル内のオブジェクトをより直接的に操作できるようにしています。

> [!NOTE]
> Tabular Editor 3のC#スクリプトエディターでは、まだ IntelliSense(TM) のような機能は有効になっていません。この機能は後のリリースで利用可能になる予定です。詳しくは[@roadmap](TabularEditorDocs\te3\other\roadmap.md)をご覧ください。

## オブジェクト

[スクリプティング API](xref:api-index) は `Model` と `Selected` という2つのトップレベルオブジェクトへのアクセスを提供します。前者はTabularモデル内のすべてのオブジェクトを操作するためのメソッドとプロパティを含んでおり、後者はエクスプローラツリーで現在選択されているオブジェクトのみを公開します。

`Model`オブジェクトは [Microsoft.AnalysisServices.Tabular.Model](https://msdn.microsoft.com/en-us/library/microsoft.analysisservices.tabular.model.aspx) クラスのラッパーで、そのプロパティのサブセットを公開し、トランスレーション、パースペクティブ、オブジェクトコレクションを簡単に操作するためのいくつかのメソッドとプロパティが追加されています。同じことが、テーブル、メジャー、カラムなどの子孫オブジェクトにも適用され、これらはすべて対応するラッパーオブジェクトを持っています。タブラー・エディター・ラッパー・ライブラリーのオブジェクト、プロパティ、メソッドの完全なリストについては、<xref:api-index>を参照してください。

このラッパーで作業する主な利点は、すべての変更がTabular EditorのUIから元に戻せることです。スクリプトを実行した後、CTRL+Zを押すだけで、そのスクリプトによって行われたすべての変更が即座に取り消されるのがわかります。さらに、このラッパーは、多くの一般的なタスクをシンプルなワンライナーに変える便利なメソッドを提供します。以下に、いくつかの例を紹介します。読者はすでにC#とLINQにある程度慣れていることが前提です。なぜなら、Tabular Editorsのスクリプト機能のこれらの側面はここではカバーされないからです。C#やLINQに慣れていない方でも、以下の例にはついていけるはずです。

## オブジェクトのプロパティを設定する

あるオブジェクトのプロパティを変更したい場合、当然ながらUIから直接行うのがもっとも簡単な方法でしょう。しかし、例として、スクリプトを使用して同じことを実現する方法を見てみましょう。

FactInternetSales' テーブルの[Sales Amount]メジャーのFormat Stringを変更する必要があるとします。エクスプローラー・ツリーでメジャーを見つけると、それをスクリプト・エディターにドラッグするだけでよいのです。すると、Tabular Editorによって以下のコードが生成され、Tabularオブジェクト・モデルでこの特定のメジャーを表します。

```csharp
Model.Tables["FactInternetSales"].Measures["Sales Amount"]
```

右端の括弧の後にドット (.) を追加すると、オートコンプリート・メニューがポップアップ表示され、この特定のメジャーに存在するプロパティおよびメソッドが表示されます。メニューから "フォーマット文字列" を選択するか、最初の数文字を入力してTabキーを押すだけです。次に、等号の後に「0.0%」を入力します。このメジャーの表示フォルダーも変更します。最終的なコードは、以下のようになります。

```csharp
Model.Tables["FactInternetSales"].Measures["Sales Amount"].FormatString = "0.0%";
Model.Tables["FactInternetSales"].Measures["Sales Amount"].DisplayFolder = "New Folder";
```

**Note:** 各行の最後にはセミコロン（;）を付けることを忘れないでください。これはC#の必須条件です。これを忘れると、スクリプトを実行しようとしたときに、構文エラーメッセージが表示されます。

F5キーを押すか、スクリプトエディターの上にある「再生」ボタンをクリックして、スクリプトを実行します。すぐに、変更された表示フォルダーを反映して、エクスプローラツリー内でメジャーが移動するのを確認できるはずです。プロパティ・グリッドでメジャーを確認すると、Format Stringプロパティがそれに応じて変更されていることも確認できます。

### 複数のオブジェクトを一度に操作する

オブジェクト・モデルの多くのオブジェクトは、実際には複数のオブジェクトのコレクションです。たとえば、各テーブル・オブジェクトはMeasuresコレクションを持っています。ラッパーは、これらのコレクションに一連の便利なプロパティとメソッドを公開し、一度に複数のオブジェクトに同じプロパティを簡単に設定できるようにします。これについては、以下で詳しく説明します。さらに、標準的なLINQ拡張メソッドをすべて使用して、 コレクションのオブジェクトをフィルタリングしたりブラウズしたりできます。

以下に、最も一般的に使用されるLINQ拡張メソッドの例をいくつか示します。

* `Collection.First([predicate])` オプションの[predicate]の条件を満たす、コレクション内の最初のオブジェクトを返します。
* `Collection.Any([predicate])` コレクションにオブジェクトが含まれる場合（オプションで[predicate]の条件を満たす場合）、真を返します。
* `Collection.Where(predicate)` predicateの条件によってフィルタリングされたオリジナルのコレクションを返します。
* `Collection.Select(map)` 指定されたマップにしたがって、コレクション内の各オブジェクトを別のオブジェクトに投影する。
* `Collection.ForEach(action)` コレクション内の各要素に対して、指定されたアクションを実行します。

上記の例では、 `predicate` はラムダ式であり、1つのオブジェクトを入力として受け取り、ブール値を出力として返す。たとえば、 `Collection` がメジャーのコレクションであれば、典型的な `predicate` は以下のようなものになる。

`m => m.Name.Contains("Reseller")`

このpredicateは、メジャーの名前に文字列 "Reseller" が含まれている場合にのみ、trueを返します。より高度なロジックが必要な場合は、式を中括弧で囲み、`return` キーワードを使用します。

```csharp
.Where(obj => {
    if(obj is Column) {
        return false;
    }
    return obj.Name.Contains("test");
})
```

上の例に戻ると、 `map` はラムダ式で、入力としてオブジェクトを受け取り、出力として任意のオブジェクトを返します。action` はラムダ式で、入力としてオブジェクトをひとつ受け取り、出力として値を返しません。

## **モデル**オブジェクトの操作

現在ロードされているTabular Modelの任意のオブジェクトを素早く参照するには、エクスプローラツリーからC#スクリプトエディタにオブジェクトをドラッグアンドドロップします。

![Dragging and dropping an object into the C# script editor](../../../images/drag-object-to-script.gif)

モデルやその子孫オブジェクトにどのようなプロパティが存在するかの概要については、[TOM documentation](https://msdn.microsoft.com/en-us/library/microsoft.analysisservices.tabular.model.aspx)を参照してください。さらに、ラッパーオブジェクトによって公開されるプロパティとメソッドの完全なリストについては、<xref:api-index>を参照してください。

## **選択された**オブジェクトを操作する

しかし、時にはエクスプローラツリーからオブジェクトを選択し、選択されたオブジェクトのみに対してスクリプトを実行したい場合があります。そこで、`Selected`オブジェクトが役に立ちます。

Selected` オブジェクトは、現在選択されているものを簡単に識別するための様々なプロパティを提供し、特定のタイプのオブジェクトに選択を限定することもできます。ディスプレイフォルダでブラウジングしているときに、エクスプローラツリーで1つ以上のフォルダが選択されていると、その子アイテムもすべて選択されているとみなされます。 単一選択の場合は、アクセスしたいオブジェクトのタイプを表す単数形の名前を使用します。たとえば、以下のようになります。

`Selected.Hierarchy`

は、ツリー内で現在選択されている階層を参照します。ただし、選択されている階層が1つだけであることが条件です。複数選択可能な場合は、複数形の型名を使用します。

`Selected.Hierarchies`

単数形のオブジェクトに存在するすべてのプロパティは、いくつかの例外を除いて、その複数形にも存在します。つまり、上記のLINQ拡張メソッドを使用せずに、1行のコードで、複数のオブジェクトに対して一度にこれらのプロパティの値を設定できます。たとえば、現在選択されているすべてのメジャーを "Test" という名前の新しい表示フォルダーに移動させたいとします。

`Selected.Measures.DisplayFolder = "Test";`

ツリーで現在どのメジャーも選択されていない場合、上記のコードは何も行わず、エラーも発生しません。そうでない場合は、選択されたすべてのメジャーに対してDisplayFolderプロパティが "Test" に設定されます（`Selected` オブジェクトは選択されたフォルダー内のオブジェクトも含むため、フォルダー内に存在するメジャーも含まれます）。Measures` の代わりに単数形の `Measure` を使用すると、現在の選択範囲に正確に1つのメジャーが含まれていない限り、エラーが発生します。

複数のオブジェクトのNameプロパティを一度に設定することはできませんが、いくつかのオプションは用意されています。ある文字列の出現箇所をすべて別の文字列に置き換えるだけなら、提供されている「Rename」メソッドを使えばいい。

```csharp
Selected.Measures
        .Rename("Amount", "Value");
```

この場合、現在選択されているすべてのメジャーの名前に含まれる "Amount" という単語が "Value" に置き換えられます。 また、上記のようにLINQ ForEach() メソッドを使用して、より高度なロジックを組み込むこともできます。

```csharp
Selected.Measures
        .ForEach(m => if(m.Name.Contains("Reseller")) m.Name += " DEPRECATED");
```

この例では、選択されたすべてのメジャーの名前に、名前に "Reseller" という単語が含まれている場合は、" DEPRECATED" というテキストが追加されます。別の方法として、LINQ拡張メソッド `Where()` を使用して、`ForEach()` オペレーションを適用する前にコレクションをフィルタリングすることもでき、まったく同じ結果を得ることができます。

```csharp
Selected.Measures
        .Where(m => m.Name.Contains("Reseller"))
        .ForEach(m => m.Name += " DEPRECATED");
```

## ヘルパーメソッド

Tabular Editorは、特定のスクリプトタスクを簡単に実現するための特別なヘルパーメソッド群を提供します。これらのいくつかは拡張メソッドとして呼び出すことができることに注意してください。たとえば、`object.Output();` と `Output(object);` は等価です。

* `void Output(object value)` - は、スクリプトの実行を停止し、指定されたオブジェクトに関する情報を表示します。スクリプトがコマンドライン実行の一部として実行されている場合、これはコンソールにオブジェクトの文字列表現を書き込みます。
* `void SaveFile(string filePath, string content)` - テキストデータをファイルに保存する便利な方法です。
* `string ReadFile(string filePath)` - ファイルからテキストデータを読み込む便利な方法です。
* `string ExportProperties(IEnumerable<ITabularNamedObject> objects, string properties)` - 複数のオブジェクトから一連のプロパティをTSV文字列としてエクスポートする便利な方法です。
* `void ImportProperties(string tsvData)` - TSV文字列から複数のオブジェクトにプロパティをロードする便利な方法です。
* `void CustomAction(string name)` - マクロを名前で呼び出す。
* `void CustomAction(this IEnumerable<ITabularNamedObject> objects, string name)` - 指定されたオブジェクトに対してマクロを呼び出す。
* `string ConvertDax(string dax, bool useSemicolons)` - は、US/UKとnon-US/UKのロケール間でDAX式を変換します。`useSemicolons` がtrue（デフォルト）の場合、 `dax` 文字列はネイティブのUS/UKフォーマットからnon-US/UKフォーマットに変換される。つまり、カンマ (リストセパレーター) はセミコロンに、ピリオド (小数点以下のセパレーター) はカンマに変換されます。UseSemicolons` がfalseに設定されている場合は、その逆となる。
* `void FormatDax(this IEnumerable<IDaxDependantObject> objects, bool shortFormat, bool? skipSpace)` - 指定されたコレクション内のすべてのオブジェクトに対して DAX 式をフォーマットします。
* `void FormatDax(this IDaxDependantObject obj)` - スクリプトの実行が完了したとき、あるいは `CallDaxFormatter` メソッドが呼ばれたときに、DAX式のフォーマット用にオブジェクトをキューに追加します。
* `void CallDaxFormatter(bool shortFormat, bool? skipSpace)` - これまでにキューイングされたオブジェクトのすべてのDAX式をフォーマットします。
* `void Info(string)` - コンソールに情報メッセージを書き込みます（スクリプトがコマンドライン実行の一部として実行された場合のみ）。
* `void Warning(string)` - コンソールに警告メッセージを書き込みます（スクリプトがコマンドライン実行の一部として実行された場合のみ）。
* `void Error(string)` - コンソールにエラーメッセージを書き込みます（スクリプトがコマンドライン実行の一部として実行された場合のみ）。
* `T SelectObject(this IEnumerable<T> objects, T preselect = null, string label = "Select object") where T: TabularNamedObject` - 指定されたオブジェクトの1つを選択するよう促すダイアログをユーザに表示する。ユーザがダイアログをキャンセルした場合、このメソッドはnullを返します。
* `void CollectVertiPaqAnalyzerStats()` - Tabular EditorがAnalysis Servicesのインスタンスに接続されている場合、VertiPaq Analyzerの統計コレクターが実行されます。
* `long GetCardinality(this Column column)` - VertiPaq Analyzerの統計情報が現在のモデルで利用可能な場合、このメソッドは指定された列のカーディナリティを返します。

利用可能なヘルパーメソッドの一覧とその構文については、@script-helper-methodsを参照してください。

### デバッグ用スクリプト

前述のように、`Output(object);` メソッドを使うと、スクリプトの実行を一時停止し、渡されたオブジェクトに関する情報を表示するダイアログボックスを開くことができます。また、このメソッドを拡張メソッドとして、`object.Output();`として呼び出すこともできます。ダイアログが閉じられると、スクリプトは再開されます。

ダイアログは、出力されるオブジェクトの種類に応じて、4つの異なる方法のうちの1つで表示されます。

- 特異なオブジェクト（文字列、int、DateTimesなど、TabularNamedObjectから派生したオブジェクトは除く）は、オブジェクトの `.ToString()` メソッドを呼び出すことで、シンプルなメッセージダイアログとして表示されます。

![image](https://user-images.githubusercontent.com/8976200/29941982-9917d0cc-8e94-11e7-9e78-24aaf11fd311.png)

- 特異なTabularNamedObject（Table、Measure、またはTabular Editorで利用可能なその他のTOM NamedMetadataObjectなど）は、Tree Explorerでオブジェクトが選択されたときと同様にProperty Gridに表示される。オブジェクトのプロパティはグリッドで編集できるが、スクリプト実行の後の時点でエラーが発生した場合、"Rollback on error" が有効になっていれば、編集は自動的に戻されることに注意。

![image](https://user-images.githubusercontent.com/8976200/29941852-2acc9846-8e94-11e7-9380-f84fef26a78c.png)

- オブジェクトの任意のIEnumerable（TabularNamedObjectsを除く）はリストに表示され、各リストアイテムはIEnumerable内のオブジェクトの `.ToString()` 値とタイプを表示します。

![image](https://user-images.githubusercontent.com/8976200/29942113-02dad928-8e95-11e7-9c04-5bb87b396f3f.png)

- TabularNamedObjectsのIEnumerableはダイアログの左側にオブジェクトのリストを表示し、右側にProperty Gridを表示します。Property Gridはリストで選択されたオブジェクトから入力され、単一のTabularNamedObjectが出力されているときと同様にプロパティを編集できます。

![image](https://user-images.githubusercontent.com/8976200/29942190-498cbb5c-8e95-11e7-8455-32750767cf13.png)

左下にある "Don't show more outputs" チェックボックスをチェックすると、それ以上 `.Output()` を呼び出したときにスクリプトが停止するのを防ぐことができます。

## .NETリファレンス

通常のC#ソースコードと同様に、`using` キーワードを使用してクラス名などを短縮できます。また、Azure Functionsで使用する .csxスクリプトと同様に、`#r "<アセンブリ名または DLL パス>"` という構文で、外部アセンブリをインクルードすることが可能です。
たとえば、以下のスクリプトは期待通りに動作します。

```csharp
// Assembly references must be at the very top of the file:
#r "System.IO.Compression"

// Using keywords must come before any other statements:
using System.IO.Compression;
using System.IO;

var xyz = 123;

// Using statements still work the way they're supposed to:
using(var data = new MemoryStream())
using(var zip = new ZipArchive(data, ZipArchiveMode.Create)) 
{
   // ...
}
```

Tabular Editorはデフォルトで以下の`using`キーワードを適用し（スクリプトで指定されていなくても）、一般的な作業を容易にします。

```csharp
using System;
using System.Linq;
using System.Collections.Generic;
using Newtonsoft.Json;
using TabularEditor.TOMWrapper;
using TabularEditor.TOMWrapper.Utils;
using TabularEditor.UI;
```

また、以下の.NET Frameworkアセンブリがデフォルトでロードされます。

- System.Dll
- System.Core.Dll
- System.Data.Dll
- System.Windows.Forms.Dll
- Microsoft.Csharp.Dll
- Newtonsoft.Json.Dll
- TomWrapper.Dll
- TabularEditor.Exe
- Microsoft.AnalysisServices.Tabular.Dll

## Roslynでのコンパイル

Visual Studio 2017で導入された新しいRoslynコンパイラーを使用してスクリプトをコンパイルしたい場合は、**Tools > Preferences > Tabular Editor > C# SCripts and Maros**で設定できます。これにより、文字列補間などの新しいC#言語の機能を利用できます。コンパイラの実行ファイル（`csc.exe`）を格納するディレクトリのパスを指定し、コンパイラのオプションとして言語バージョンを指定するだけで、簡単に設定できます。

![Custom Compiler Te3](~/images/custom-compiler-te3.png)

### Visual Studio 2017

一般的なVisual Studio 2017 Enterpriseのインストールでは、Roslynコンパイラはここに配置されています。

```
c:\Program Files (x86)\Microsoft Visual Studio\2017\Enterprise\MSBuild\15.0\Bin\Roslyn
```

これには、C# 6.0の言語機能がデフォルトで含まれています。

![image](https://user-images.githubusercontent.com/8976200/92464584-a52cfc80-f1cd-11ea-9b66-3b47ac36f6c6.png)

### Visual Studio 2019

一般的な Visual Studio 2019 Community インストールの場合、Roslyn コンパイラはここにあります。

```
c:\Program Files (x86)\Microsoft Visual Studio\2019\Community\MSBuild\Current\Bin\Roslyn
```

VS2019に同梱されているコンパイラは、C#8.0の言語機能をサポートしており、コンパイラオプションとして以下を指定することで有効にすることができます。

```
-langversion:8.0
```
