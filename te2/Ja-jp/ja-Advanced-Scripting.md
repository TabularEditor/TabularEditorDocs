# Advanced Scripting

本書は、Tabular EditorのAdvanced Scripting機能の紹介です。このドキュメントの情報は変更される可能性があります。また、[Useful script snippets](/Useful-script-snippets) の記事で、Tabular Editorのスクリプト機能を使ってできることの実例をいくつか紹介していますので、ぜひご覧ください。

## What is Advanced Scripting?

Tabular EditorのUIの目標は、Tabularモデルの構築時に一般的に必要とされるほとんどのタスクを簡単に実行できるようにすることです。たとえば、複数のメジャーの表示フォルダーを一度に変更するには、エクスプローラー・ツリーでオブジェクトを選択し、ドラッグ・アンド・ドロップすればよいだけです。エクスプローラツリーの右クリックによるコンテキストメニューでは、パースペクティブからのオブジェクトの追加/削除、複数のオブジェクトの名前変更など、多くの作業を便利に行うことができます。

しかし、その他の一般的なワークフロータスクは、UIから簡単に実行できないものも多くあります。このため、Tabular Editorは上級ユーザーがC#シンタックスを使用してスクリプトを書き、ロードされたTabularモデル内のオブジェクトをより直接的に操作できるようにする、高度なスクリプトを導入しています。

## Objects

スクリプティング [API](xref:api-index) は `Model` と `Selected` という二つのトップレベルオブジェクトへのアクセスを提供します。前者は Tabular モデル内のすべてのオブジェクトを操作するためのメソッドとプロパティを含んでおり、後者はエクスプローラツリーで現在選択されているオブジェクトのみを公開します。

`Model` オブジェクトは [Microsoft.AnalysisServices.Tabular.Model](https://msdn.microsoft.com/en-us/library/microsoft.analysisservices.tabular.model.aspx) クラスのラッパーで、そのプロパティのサブセットを公開し、トランスレーション、パースペクティブ、オブジェクトコレクションを簡単に操作するためのいくつかのメソッドとプロパティが追加されています。同じことが、Table、Measure、Column などの子孫オブジェクトにもあてはまり、これらはすべて対応するラッパーオブジェクトを持っています。タブラー・エディター・ラッパー・ライブラリーのオブジェクト、プロパティ、メソッドの完全なリストについては、<xref:api-index>をご覧ください。

このラッパーで作業する主な利点は、すべての変更がタブラーエディターのUIから元に戻せることです。スクリプトを実行した後、CTRL+Zを押すだけで、そのスクリプトによって行われたすべての変更が即座に取り消されるのがわかります。さらに、このラッパーは、多くの一般的なタスクをシンプルなワンライナーに変える便利なメソッドを提供します。以下に、いくつかの例を紹介します。読者はすでにC#とLINQにある程度慣れていることが前提です。なぜなら、Tabular Editorsのスクリプト機能のこれらの側面はここではカバーされないからです。C#やLINQに慣れていない方でも、以下の例にはついていけるはずです。

## Setting object properties

あるオブジェクトのプロパティを変更したい場合、当然ながらUIから直接行うのが最も簡単な方法でしょう。しかし、例として、スクリプトを使用して同じことを実現する方法を見てみましょう。

'FactInternetSales' テーブルの[Sales Amount]メジャーのFormat Stringを変更する必要があるとします。エクスプローラー・ツリーでメジャーを見つけると、それをスクリプト・エディターにドラッグするだけでよいのです。すると、Tabular Editorによって以下のコードが生成され、Tabularオブジェクト・モデルでこの特定のメジャーを表します。

```csharp
Model.Tables["FactInternetSales"].Measures["Sales Amount"]
```

右端の括弧の後にドット (.) を追加すると、オートコンプリート・メニューがポップアップ表示され、この特定のメジャーに存在するプロパティおよびメソッドが表示されるはずです。メニューから[フォーマット文字列]を選択するか、または最初の数文字を入力してTabキーを押します。それから、等号の後に「0.0%」を入力します。このメジャーの表示フォルダーも変更します。最終的なコードは以下のようになります。

```csharp
Model.Tables["FactInternetSales"].Measures["Sales Amount"].FormatString = "0.0%";
Model.Tables["FactInternetSales"].Measures["Sales Amount"].DisplayFolder = "New Folder";
```

**注意:** 各行の最後にセミコロン(;)を付けることを忘れないでください。これはC#の要求事項です。これを忘れると、スクリプトを実行しようとしたときに構文エラーメッセージが表示されます。

F5キーを押すか、スクリプトエディターの上にある「Play」ボタンを押すと、スクリプトが実行されます。すぐに、エクスプローラツリー内でメジャーが移動し、変更された表示フォルダーが確認できるはずです。Property Gridでメジャーを確認すると、Format String プロパティがそれに応じて変更されていることも確認できるはずです。

### Working with multiple objects at once

オブジェクト・モデルの多くのオブジェクトは、実際には複数のオブジェクトのコレクションです。たとえば、各テーブル・オブジェクトはMeasuresコレクションを持っています。ラッパーは、これらのコレクションに一連の便利なプロパティとメソッドを公開し、一度に複数のオブジェクトに同じプロパティを簡単に設定できるようにします。これについては、以下で詳しく説明します。さらに、標準的なLINQ拡張メソッドをすべて使用して、コレクション内のオブジェクトをフィルタリングしたりブラウズしたりできます。

以下は、もっともよく使われるLINQ拡張メソッドの例です。

* `Collection.First([predicate])` オプションの[predicate]条件を満たす、コレクション内の最初のオブジェクトを返します。
* `Collection.Any([predicate])` コレクションが何らかのオブジェクト（オプションで [predicate]条件を満たす）を含んでいれば真を返します。
* `Collection.Where([predicate])` コレクション内の任意のオブジェクトを返します。Where(predicate)` 述語の条件でフィルタリングされたオリジナルのコレクションを返す
* `Collection.Select(map)` 指定されたマップにしたがって、コレクション内の各オブジェクトを別のオブジェクトにプロジェクションする
* `Collection.ForEach(action)` コレクション内の各要素に対して指定されたアクションを実行する。
* `Collection.ForEach(action)` コレクション内の各要素に対して指定されたアクションを実行する。

上記の例で、`predicate` はラムダ式であり、入力として1つのオブジェクトを受け取り、出力としてブール値を返す。たとえば、 `Collection` がメジャーのコレクションである場合、典型的な `predicate` は以下のようになります。

m => m.Name.Contains("Reseller")` となります。

この述語は、メジャーのNameに文字列 "Reseller" が含まれている場合にのみ、trueを返します。より高度なロジックが必要な場合は、中括弧で式を囲み、`return` キーワードを使用します。

```csharp
.Where(obj => {
    if(obj is Column) {
        return false;
    }
    return obj.Name.Contains("test");
})
```

上の例に戻ると、 `map` はラムダ式で、入力としてオブジェクトを受け取り、出力として任意のオブジェクトを返します。action` はラムダ式で、1つのオブジェクトを入力として受け取り、値は返しません。

他にどのようなLINQメソッドがあるかは、アドバンストスクリプトエディターのインテリセンス機能を使うか、あるいは [LINQ-to-Objects documentation](https://msdn.microsoft.com/en-us/library/9eekhta0.aspx) を参照してください。

## Working with the **Model** object

現在ロードされているTabular Modelの任意のオブジェクトを素早く参照するには、エクスプローラツリーからAdvanced Scriptingエディターにオブジェクトをドラッグ＆ドロップします。

![Dragging and dropping an object into the Advanced Scripting editor](https://raw.githubusercontent.com/otykier/TabularEditor/master/Documentation/DragDropTOM.gif)

モデルやその子孫オブジェクトにどのようなプロパティが存在するかの概要については、[TOM documentation](https://msdn.microsoft.com/en-us/library/microsoft.analysisservices.tabular.model.aspx)を参照してください。さらに、ラッパーオブジェクトによって公開されるプロパティとメソッドの完全なリストについては、<xref:api-index>を参照してください。

## Working with the **Selected** object

しかし、時にはエクスプローラツリーからオブジェクトを選択し、選択されたオブジェクトのみに対してスクリプトを実行したい場合があります。このような場合に `Selected` オブジェクトが役に立ちます。

Selected` オブジェクトは、現在選択されているオブジェクトを簡単に識別するためのプロパティを提供し、また、特定のタイプのオブジェクトに選択を限定できます。フォルダーを表示してブラウジングしているときに、エクスプローラツリーで1つ以上のフォルダーが選択されていると、その子項目もすべて選択されているとみなされます。 単一選択の場合は、アクセスしたいオブジェクトのタイプの単数名を使用します。たとえば

`Selected.Hierarchy` とします。

は、ツリーで現在選択されている階層を指します。ただし、選択されている階層は1つだけです。複数選択されている場合は、複数の型名を使用できます。

`Selected.Hierarchies` となります。

単数形のオブジェクトに存在するすべてのプロパティは、いくつかの例外を除いて、複数形のオブジェクトにも存在します。つまり、上記のLINQ拡張メソッドを使わずに、1行のコードで複数のオブジェクトに対して一度にこれらのプロパティの値を設定することができるのです。たとえば、現在選択されているすべてのメジャーを「Test」という名前の新しい表示フォルダーに移動したいとします。

たとえば、現在選択されているすべてのメジャーを「Test」という新しい表示フォルダーに移動したいとします。

ツリーで現在選択されているメジャーがない場合、上記のコードは何も行わず、エラーも発生しません。そうでない場合は、選択されたすべてのメジャー (フォルダー内のメジャーも含む。`Selected` オブジェクトには選択されたフォルダー内のオブジェクトも含まれるため）のDisplayFolderプロパティが "Test" に設定されます。Measures` の代わりに単数形の `Measure` を使用すると、現在の選択範囲に正確に1つのメジャーが含まれていない限り、エラーになります。

複数のオブジェクトのNameプロパティを一度に設定することはできませんが、まだいくつかのオプションがあります。ある文字列の出現箇所をすべて別の文字列に置き換えるだけなら、 提供されている「âuRename」メソッドを使用できます。

```csharp
Selected.Measures
        .Rename("Amount", "Value");
```

これにより、現在選択されているすべてのメジャーの名前に出現する「金額」という単語が「値」に置き換えられます。 また、上記のようにLINQ ForEach() メソッドを使用して、より高度なロジックを組み込むことも可能です。

```csharp
Selected.Measures
        .ForEach(m => if(m.Name.Contains("Reseller")) m.Name += " DEPRECATED");
```

この例では、選択されたすべてのメジャーの名前に、名前に "Reseller" という単語が含まれている場合は、" DEPRECATED" というテキストが追加されます。別の方法として、LINQ 拡張メソッド `Where()` を使用して、`ForEach()` オペレーションを適用する前にコレクションをフィルタリングすることもでき、まったく同じ結果を得ることができます。

```csharp
Selected.Measures
        .Where(m => m.Name.Contains("Reseller"))
        .ForEach(m => m.Name += " DEPRECATED");
```

## Helper methods

スクリプトのデバッグを容易にするため、Tabular Editorは特別なヘルパーメソッドのセットを提供します。内部的には、これらは `[ScriptMethod]`-attributeで装飾された静的メソッドです。この属性によって、スクリプトは名前空間やクラス名を指定することなく、直接メソッドを呼び出すことができます。プラグインも `[ScriptMethod]` 属性を用いて、同様の方法でスクリプト用のパブリックな静的メソッドを公開することができる。

2.7.4以降、Tabular Editorは以下のスクリプトメソッドを提供します。これらのいくつかは拡張メソッドとして呼び出すことができることに注意してください。たとえば、`object.Output();` と `Output(object);` は等価です。

* `Output(object);`は、スクリプトの実行を停止し、指定されたオブジェクトに関する情報を表示します。スクリプトがコマンドライン実行の一部として実行されている場合、これはコンソールにオブジェクトの文字列表現を書き込みます。
* `SaveFile(filePath, content);` - convenient way to save text data to a file.
* `ReadFile(filePath);` - ファイルからテキストデータを読み込む便利な方法です。
* `ExportProperties(objects, properties);` - 複数のオブジェクトから一連のプロパティをTSV文字列としてエクスポートする便利な方法です。
* `ImportProperties(tsvData);` - TSV文字列から複数のオブジェクトにプロパティをロードする便利な方法です。
* `CustomAction(name);` - カスタムアクションを名前で呼び出す。
* `CustomAction(objects, name);` - 指定されたオブジェクトに対してカスタムアクションを実行します。
* `ConvertDax(dax, useSemicolons);` - は、US/UKとnon-US/UKのロケール間でDAX式を変換します。`useSemicolons` がtrue（デフォルト）の場合、 `dax` 文字列はネイティブのUS/UKフォーマットからnon-US/UKフォーマットに変換される。つまり、カンマ (リストセパレーター) はセミコロンに、ピリオド (小数点以下のセパレーター) はカンマに変換されます。UseSemicolons` がfalseに設定されている場合は、その逆となる。
* ~~`FormatDax(string dax);`~~ - www.daxformatter.com を使ってDAX式をフォーマットする (非推奨。使わないでください!)
* `FormatDax(IEnumerable<IDaxDependantObject> objects, bool shortFormat, bool? skipSpace)` - 指定されたコレクション内のすべてのオブジェクトに対してDAX式をフォーマットします。
* `FormatDax(IDaxDependantObject obj)` - スクリプトの実行が完了したとき、あるいは `CallDaxFormatter` メソッドが呼ばれたときに、DAX 式のフォーマット用にオブジェクトをキューに入れます。 * `CallDaxFormatter(bool shortFormat, bool? skipSpace)` - これまでにキューに入っているすべてのDAX式をフォーマットする。
* `Info(string);` - コンソールに情報メッセージを書き込みます（スクリプトがコマンドライン実行の一部として実行された場合のみ）。
* `Warning(string);` - コンソールに警告メッセージを書き込みます（スクリプトがコマンドライン実行の一部として実行された場合のみ）。
* `Error(string);` - コンソールにエラーメッセージを書き込みます（スクリプトがコマンドライン実行の一部として実行された場合のみ）。

### Debugging scripts

前述のように、`Output(object);` メソッドを使うと、スクリプトの実行を一時停止し、渡されたオブジェクトに関する情報を表示するダイアログボックスを開くことができます。また、このメソッドを拡張メソッドとして、`object.Output();`として呼び出すこともできます。ダイアログが閉じられると、スクリプトは再開されます。

ダイアログは、出力されるオブジェクトの種類によって、4つの異なる方法のうちの1つが表示されます。

* 特異なオブジェクト（文字列、int、DateTimesなど、TabularNamedObjectから派生したオブジェクトは除く）は、オブジェクトの `.ToString()` メソッドを呼び出すことで、シンプルなメッセージダイアログとして表示されます。

![image](https://user-images.githubusercontent.com/8976200/29941982-9917d0cc-8e94-11e7-9e78-24aaf11fd311.png)

* 特異なTabularNamedObject（Table、Measure、またはTabular Editorで利用可能なその他のTOM NamedMetadataObjectなど）は、Tree Explorerでオブジェクトが選択されたときと同様にProperty Gridに表示される。オブジェクトのプロパティはグリッドで編集できるが、スクリプト実行の後の時点でエラーが発生した場合、"Rollback on error" が有効になっていれば、編集は自動で元に戻されることは注意。

![image](https://user-images.githubusercontent.com/8976200/29941852-2acc9846-8e94-11e7-9380-f84fef26a78c.png)

* オブジェクトの任意のIEnumerable（TabularNamedObjectsを除く）はリストに表示され、各リストアイテムはIEnumerable内のオブジェクトの `.ToString()` 値とタイプを表示します。

![image](https://user-images.githubusercontent.com/8976200/29942113-02dad928-8e95-11e7-9c04-5bb87b396f3f.png)

* TabularNamedObjectsのIEnumerableはダイアログの左側にオブジェクトのリストを表示し、右側にProperty Gridを表示します。Property Gridはリストで選択されたオブジェクトから入力され、単一のTabularNamedObjectが出力されているときと同様にプロパティを編集できます。

![image](https://user-images.githubusercontent.com/8976200/29942190-498cbb5c-8e95-11e7-8455-32750767cf13.png)

左下にある "Don't show more outputs" チェックボックスをチェックすると、それ以上 `.Output()` を呼び出したときにスクリプトが停止するのを防ぐことができます。

## .NET references

[Tabular Editor version 2.8.6](https://github.com/otykier/TabularEditor/tree/2.8.6) では、複雑なスクリプトを書くのがとても簡単になりました。新しいプリプロセッサのおかげで、通常のC#ソースコードのように、`using`キーワードを使ってクラス名などを短縮できるようになりました。さらに、Azure Functions で使用する .csx スクリプトと同様に、`#r "<アセンブリ名または DLL パス>"` という構文を使用して、外部アセンブリをインクルードできます。

たとえば、以下のスクリプトは期待通りの動作をするようになりました。

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

Tabular Editorはデフォルトで以下の`using`キーワードを適用し、（スクリプトで指定されていなくても）一般的なタスクを簡単に行えるようにします。

```csharp
using System;
using System.Linq;
using System.Collections.Generic;
using Newtonsoft.Json;
using TabularEditor.TOMWrapper;
using TabularEditor.TOMWrapper.Utils;
using TabularEditor.UI;
```

In addition, the following .NET Framework assemblies are loaded by default:

- System.Dll
- System.Core.Dll
- System.Data.Dll
- System.Windows.Forms.Dll
- Microsoft.Csharp.Dll
- Newtonsoft.Json.Dll
- TomWrapper.Dll
- TabularEditor.Exe
- Microsoft.AnalysisServices.Tabular.Dll

## Compiling with Roslyn

Visual Studio 2017で導入された新しいRoslynコンパイラーを使用してスクリプトをコンパイルしたい場合は、Tabular Editorバージョン2.12.2から、ファイル > プリファレンス > 一般で設定できます。これにより、文字列補間など、より新しいC#言語の機能を利用できます。コンパイラの実行ファイル（`csc.exe`）を格納するディレクトリのパスを指定し、コンパイラのオプションとして言語バージョンを指定するだけで、簡単に設定できます。

![image](https://user-images.githubusercontent.com/8976200/92464140-0902f580-f1cd-11ea-998a-b6ecce57b399.png)

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

VS2019に同梱されているコンパイラは、C#8.0の言語機能をサポートしており、コンパイラオプションとして以下を指定することで有効にができます。

```
-langversion:8.0
```
