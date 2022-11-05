# Best Practice Analyzer

> ベストプラクティス・アナライザーは Tabular Editor v. 2.8.1 で全面的に改良されたため、この記事の情報やスクリーンショットの一部は古くなっています[Best-Practice-Analyzer-Improvements.md](Best-Practice-Analyzer-Improvements.md)。Dynamic LINQ (ルール式) に関する情報は、現在も最新です。

この[素晴らしい提案](https://github.com/TabularEditor/TabularEditor/issues/39)に触発されて、Tabular Editorのまったく新しい機能であるBest Practice Analyzer (BPA)をご紹介できることを誇りに思います。ツールメニューから「Best Practice Analyzer...」をクリックすると、次のウィンドウが開きます（BPAウィンドウを開いたまま、メインウィンドウでモデルの作業を続けることができます）。

![image](https://cloud.githubusercontent.com/assets/8976200/25298153/07cb3ae0-26f3-11e7-84cb-1c27a5911560.png)

BPAでは、モデルのメタデータにルールを定義し、SSAS Tabularで開発する際に特定の規約やベストプラクティスを推奨できます。

上のリストでルールの1つをクリックすると、下のリストで指定されたルールの条件を満たすすべてのオブジェクトが表示されます。

![image](https://cloud.githubusercontent.com/assets/8976200/25298226/9c036214-26f3-11e7-97ea-03ef82366eb5.png)

リスト内のオブジェクトをダブルクリックすると、Tabular Editorのメインウィンドウにフォーカスが戻り、エクスプローラツリーでそのオブジェクトが選択されます（「Go to object...」）。また、ルールを完全に無視したり（ルールリストのチェックマークを外すことで可能）、特定のオブジェクトのみを無視するように指定することも可能です。無視はModel.bimファイルのメタデータアノテーションに保存されます。

新しいルールを作成するには、Tabular EditorにTabular Modelをロードした状態で、「Add rule...」をクリックするだけです。新しいウィンドウが開き、ルールの名前、説明、条件を指定できます。

![image](https://cloud.githubusercontent.com/assets/8976200/25298330/4178cbe4-26f4-11e7-97ee-d80c1dbc54ed.png)

ビジュアルなルールビルダーは、後のリリースで計画されています。今のところ、ルール条件は[Dynamic LINQ式](https://github.com/kahanu/System.Linq.Dynamic/wiki/Dynamic-Expressions)を使用して指定します。この式では、ドロップダウンで指定したオブジェクトのタイプにあるすべてのプロパティにアクセスすることが可能です。条件を満たすすべてのオブジェクトは、ルールが選択されるとBPA UIに表示されます。

デフォルトではこの方法で作成されたルールは、Tabular Editorで「保存」をクリックすると、Modelオブジェクトのメタデータアノテーションに追加され、Model.bimファイルまたは接続されたデータベースに保存されます。ローカルモデル内に保存されたルールを「グローバル」ルールに昇格させることができます。グローバルルールは、%AppData%Local TieTabularEditorフォルダーにある「BPARules.json」というファイルに保存されます。BPARules.jsonを %ProgramData%TabularEditorフォルダーに置くことで、マシン上のすべてのユーザーがルールを利用できるようにすることもできます。

ルールIDは常に一意である必要があることに注意してください。モデルメタデータ内のルールが%AppData%または%ProgramData%フォルダー内のルールと同じIDを持つ場合、優先順位は次のようになります。

- モデル内にローカル保存されたルール
- AppData%Localフォルダーに保存されたルール
- ProgramData%フォルダーに格納されたルール

## ルール表現サンプル

このセクションでは、ルールを定義するために使用できる動的LINQ式の例をいくつか紹介します。ルール式エディターに入力された式は、テキストボックスからフォーカスが外れるたびに評価され、構文エラーがあれば画面の上部に表示されます。

![image](https://cloud.githubusercontent.com/assets/8976200/25380170/9f01634e-29af-11e7-952e-e10a1f28df32.png)

ルール式は、TOM内のオブジェクトのパブリックプロパティにアクセスできます。そのタイプのオブジェクトが存在しないプロパティにアクセスしようとした場合、エラーも表示されます。

![image](https://cloud.githubusercontent.com/assets/8976200/25381302/798bab98-29b3-11e7-931e-789e5286fc45.png)

"Column "オブジェクトに "Expression" が存在しませんが、ドロップダウンを "Calculated Columns" に切り替えると、上記のステートメントは問題なく動作します。

![image](https://cloud.githubusercontent.com/assets/8976200/25380451/87b160da-29b0-11e7-8e2e-c4e47593007d.png)

Dynamic LINQは、標準的な算術演算子、論理演算子、比較演算子をすべてサポートしており、". "表記を使用すると、すべてのオブジェクトのサブプロパティとメソッドにアクセスすることが可能です。

```
String.IsNullOrWhitespace(Expression) and not Name.StartsWith("Dummy")
```

上記のステートメントを計算列、計算テーブル、またはメジャーに適用すると、オブジェクトの名前が "Dummy" というテキストで始まっていない限り、空のDAX式を持つものにフラグが立てられます。

LINQを使用すると、オブジェクトのコレクションを操作することもできます。以下の式をテーブルに適用すると、10以上のカラムを持ち、ディスプレイフォルダーに整理されていないテーブルを見つけることができます。

```
Columns.Count(DisplayFolder = "") > 10
```

LINQ メソッドを使用してコレクションを反復処理する場合、LINQメソッドの引数として使用される式は常に、コレクション内の項目で評価されます。実際、DisplayFolderは列に対するプロパティであり、Tableレベルには存在しない。

ここでは、Adventure Worksの表形式モデルでこのルールが実行されている様子を見ることができます。Reseller」テーブルが違反であると表示され、「Reseller Sales」が表示されないことに注目してください（後者のカラムはDisplay Folderで整理されています）。

![image](https://cloud.githubusercontent.com/assets/8976200/25380809/d9d1c3a4-29b1-11e7-839e-29450ad39c8a.png)

LINQメソッド内で親オブジェクトを参照するには、特別な "outerIt "構文を使用する。このルールをテーブルに適用すると、テーブル名で始まらない名前のカラムを含むものを見つけることができる。

```
Columns.Any(not Name.StartsWith(outerIt.Name))
```

このルールをColumnsに直接適用する方がおそらく理にかなっており、その場合、次のように記述する必要があります。

```
not Name.StartsWith(Table.Name)
```

列挙プロパティと比較するには、列挙された値を文字列として渡せばよい。このルールは、名前が "Key" または "ID" で終わり、かつSummarizeByプロパティが "None" に設定されていないすべての列を検索します。

```
(Name.EndsWith("Key") or Name.EndsWith("ID")) and SummarizeBy <> "None"
```

## Finding unused objects

表形式モデルを構築する場合、高い基数を持つ列を何としても避けることが重要です。典型的な原因は、誤ってモデルにインポートされたシステムのタイムスタンプやテクニカルキーなどです。一般的に、モデルには実際に必要なカラムだけが含まれるようにすべきです。ベストプラクティス・アナライザーが、どのカラムが全く必要ない可能性が高いかを教えてくれるとしたら、それは素晴らしいことだと思いませんか？

次のルールは、そのカラムを報告します。

- ...が非表示になっている（または親テーブルが非表示になっている）。
- ...どのDAX式からも参照されていない（モデル内のすべてのDAX式（ドリルスルー式、RLSフィルター式を含む）を考慮する
- リレーションシップがない
- ...他のカラムの "Sort By "カラムとしては使用されません。
- ...は、階層のレベルとしては使用されません。

このBPAルールのDynamic LINQ式は次のとおりです。

```
(IsHidden or Table.IsHidden)
and ReferencedBy.Count = 0 
and (not UsedInRelationships.Any())
and (not UsedInSortBy.Any())
and (not UsedInHierarchies.Any())
``` 

同じ手法で、使用されていないメジャーを見つけることができます。メジャーはリレーションシップに参加できないので、もう少し単純になります。そこで、代わりに、指定されたメジャーを参照するダウンストリーム・オブジェクトが表示されているかどうかも考慮することで、少しスパイスを効かせることができます。つまり、メジャー[A]がメジャー[B]から参照され、メジャー[A]と[B]の両方が非表示であり、他のDAX式がこれら2つのメジャーを参照しない場合、開発者にそれらの両方を削除しても安全であることを知らせる必要があります。

```
(IsHidden or Table.IsHidden)
and not ReferencedBy.AllMeasures.Any(not IsHidden)
and not ReferencedBy.AllColumns.Any(not IsHidden)
and not ReferencedBy.AllTables.Any(not IsHidden)
and not ReferencedBy.Roles.Any()
```

## Fixing objects

場合によっては、ルールの基準を満たすオブジェクトの問題を自動的に修正することが可能です。たとえば、オブジェクトに単純なプロパティを設定するだけでよい場合です。次のルールの背後にあるJSONを詳しく見てみましょう。

```json
{
    "ID": "FKCOLUMNS_HIDDEN",
    "Name": "Hide foreign key columns",
    "Category": null,
    "Description": "Columns used on the Many side of a relationship should be hidden.",
    "Severity": 1,
    "Scope": "Column",
    "Expression": "Model.Relationships.Any(FromColumn = outerIt) and not IsHidden and not Table.IsHidden",
    "FixExpression": "IsHidden = true",
    "Compatibility": [
      1200,
      1400
    ],
    "IsValid": false
}
```

このルールは、リレーションシップで使用されるすべての列 ("Many" / "From" 側）を検索しますが、列またはその親テーブルが非表示になっていない場合です。ユーザは関連 (ディメンジョン）テーブルを使用してデータをフィルタリングする必要があるため、このような列は決して表示しないことをオススメします。したがって、この場合の修正は、列のIsHiddenプロパティをtrueに設定することであり、これはまさに上記の "FixExpression" 文字列が行うことです。これを実際に確認するには、ルールに違反するオブジェクトを右クリックして、「修正スクリプトの生成」を選択します。このスクリプトはAdvanced Script Editorに貼り付けることができ、そこから簡単にコードを確認し、実行できます。

![image](https://cloud.githubusercontent.com/assets/8976200/25298489/9035bab6-26f5-11e7-8134-8502daaf4132.png)

Remember that you can always undo (CTRL+Z) changes done to a model after script execution.

Feedback on this new tool is most welcome! In the future, we plan to provide a set of universal Best Practices that will ship with Tabular Editor to get you started. Furthermore, plans are in motion to make the Best Practice Analyzer available as a plug-in to Visual Studio, so those of you not using Tabular Editor can still benefit from it.

## Official Best Practice Rules

To provide Tabular Editor users with a set of standard Best Practices, a new GitHub [repository has been created here](https://github.com/TabularEditor/BestPracticeRules), that will serve as a public collection of Best Practice Rules that the community can contribute to. Any rules that are deemed to be generally viable for all kinds of Tabular modeling, will be included in periodic "Releases" at that repository. At a later time, Tabular Editor will be able to automatically fetch these rules from the GitHub repository, eliminating the need to manually download the BPARules.json file from the repository.
