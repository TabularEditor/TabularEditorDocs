# 高度なオブジェクトフィルタリング

この記事では、複雑なモデルを操作する際に非常に便利な機能である、Tabular Editorの「フィルター」テキストボックスの使用方法について説明します。

## Filtering Mode

[2.7.4](https://github.com/otykier/TabularEditor/releases/tag/2.7.4)より、Tabular Editorでは、階層内のオブジェクトにどのようにフィルターを適用するか、また検索結果をどのように表示するかを設定できるようになりました。これは、Filterボタンの隣にある3つの右端のツールバーボタンを使ってコントロールします。

![image](https://user-images.githubusercontent.com/8976200/46567931-08a4b480-c93d-11e8-96fd-e197e87a0587.png)

* ![image](https://user-images.githubusercontent.com/8976200/46567944-44d81500-c93d-11e8-91e2-d9822078dba7.png) **Hierarchical by parent**: 検索は、_parent_オブジェクト、つまりテーブルとディスプレイフォルダ（これらが有効な場合）に適用されます。親アイテムが検索条件に一致すると、すべての子アイテムが表示されます。
* ![image](https://user-images.githubusercontent.com/8976200/46567940-2ffb8180-c93d-11e8-9fba-84fbb79b6bb3.png) **Hierarchical by children**: この検索は、_child_オブジェクト（メジャー、カラム、階層など）に適用されます。親オブジェクトは、検索条件に一致する子オブジェクトを少なくとも1つ持っている場合にのみ表示されます。
* ![image](https://user-images.githubusercontent.com/8976200/46567941-37bb2600-c93d-11e8-9c02-86502f41bce8.png) **Flat**: 検索はすべてのオブジェクトに適用され、結果はフラットなリストで表示されます。子項目を含むオブジェクトは、引き続き階層的に表示されます。

## Simple search

[Filter]テキストボックスに何かを入力して[Enter]を押すと、オブジェクト名の中で大文字と小文字を区別しないシンプルな検索が行われます。例えば、Filterテキストボックスに「sales」と入力し、「By Parent」フィルタリングモードを使用すると、次のような結果が得られます。

![image](https://user-images.githubusercontent.com/8976200/46568002-5f5ebe00-c93e-11e8-997b-7f89dfd92076.png)

いずれかのテーブルを展開すると、そのテーブルのすべてのメジャー、列、階層、およびパーティションが表示されます。フィルタリングモードを「By Child」に変更すると、結果は次のようになります。

![image](https://user-images.githubusercontent.com/8976200/46568016-9f25a580-c93e-11e8-9bc2-c0a16a890256.png)

[Employee」テーブルは、「sales」という単語を含むいくつかの子項目（この場合は列）を持っているため、リストに表示されていることに注目してください。

## ワイルドカード検索

テキストボックスに文字列を入力する際、ワイルドカードとして `?` を使用すると任意の1文字を、 `*` を使用すると任意の連続した文字（0文字以上）を表すことができます。しかし、`sales*`と入力すると、名前が "sales" という単語で始まるオブジェクトのみが表示されます（繰り返しますが、これは大文字と小文字を区別しません）。

Searching for `sales*` by parent:

![image](https://user-images.githubusercontent.com/8976200/46568043-19eec080-c93f-11e8-8d81-2a6214bfa572.png)

Searching for `sales*` by child:

![image](https://user-images.githubusercontent.com/8976200/46568117-f9733600-c93f-11e8-96ab-f87769b8097c.png)

フラット検索で `sales*` を検索（情報欄の切り替え [Ctrl]+[F1] で各オブジェクトの詳細情報が表示されます）。

![image](https://user-images.githubusercontent.com/8976200/46568118-042dcb00-c940-11e8-82d1-516207450559.png)

ワイルドカードは文字列のどこにでも入れることができ、必要な数だけ入れることができます。これでもまだ複雑でないなら、続きを読んでください...

## 動的なLINQ検索

[Dynamic LINQ](https://github.com/kahanu/System.Linq.Dynamic/wiki/Dynamic-Expressions) を使ってオブジェクトを検索することもできます。これは [Best Practice Analyzer rules](/Best-Practice-Analyzer) を作成するときに行うのと同じことです。フィルタボックスでDynamic LINQモードを有効にするには、検索文字列の前に `:` (コロン) を置くだけです。たとえば、名前が "Key" で終わるすべてのオブジェクトを表示するには、次のように記述します (大文字と小文字を区別します)。

```
:Name.EndsWith("Key")
```

...そして[Enter]キーを押します。フラット」フィルタリングモードでは、以下のような結果になります。

![image](https://user-images.githubusercontent.com/8976200/46568130-33dcd300-c940-11e8-903c-193e1acde0ad.png)

Dynamic LINQで大文字小文字を区別しない検索を行うには、以下のような方法で入力文字列を変換できます。

```
:Name.ToUpper().EndsWith("KEY")
```

下のように、[StringComparison](https://docs.microsoft.com/en-us/dotnet/api/system.string.endswith?view=netframework-4.7.2#System_String_EndsWith_System_String_System_StringComparison_) という引数を与えることもできます。

```
:Name.EndsWith("Key", StringComparison.InvariantCultureIgnoreCase)
```

検索対象はオブジェクトの名前に限定されるわけではありません。動的LINQ検索文字列は、オブジェクトのあらゆるプロパティ（およびサブプロパティ）を評価するために、好きなだけ複雑にできます。たとえば、"TODO "という単語を含む式を持つすべてのオブジェクトを検索したい場合、次のような検索フィルターを使用することになります。

```
:Expression.ToUpper().Contains("TODO")
```

別の例として、以下では、他の何からも参照されていないモデル内のすべての非表示メジャーが表示されます。

```
:ObjectType="Measure" and (IsHidden or Table.IsHidden) and ReferencedBy.Count=0
````

また、正規表現を使うこともできます。以下は、名前に「Number」または「Amount」という単語が含まれるすべてのカラムを検索します。

```
:ObjectType="Column" and RegEx.IsMatch(Name,"(Number)|(Amount)")
```

表示オプション（ツリーの真上にあるツールバーボタン）は、"By Parent" と "By Child" フィルタリングモードを使用した場合の結果に影響を与える可能性があることに注意してください。たとえば、上記のLINQフィルターは列のみを返しますが、表示オプションが現在、列を表示しないように設定されている場合、何も表示されません。
