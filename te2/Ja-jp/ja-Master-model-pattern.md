# Master Model Pattern

組織内に複数のTabularモデルがあり、機能がかなり重複していることは珍しくありません。開発チームにとって、これらのモデルを共有機能で最新の状態に維持することは、苦痛を伴う場合があります。この記事では、これらのモデルをすべて1つの「マスター」モデルにまとめ、それをいくつかの異なるサブセットモデルに部分的にデプロイすることが理にかなっているような状況に適した別のアプローチについて見ていきます。Tabular Editorは、特別な方法でパースペクティブを利用することにより、このアプローチを可能にします（パースペクティブが通常の方法で機能することは可能です）。

**免責事項:** この手法は有効ですが、マイクロソフト社のサポートはありませんし、かなりの量の学習、スクリプト作成、ハッキングが必要です。あなたのチームに適した方法かどうか、ご自身で判断してください。

簡単のために、AdventureWorksのサンプルモデルを考えてみましょう。

![image](https://user-images.githubusercontent.com/8976200/43959290-895c1c96-9cae-11e8-8112-008f54cb400a.png)

たとえば、何らかの理由で、インターネット販売に関連するすべてを1つのモデルとして配備し、再販に関連するすべてを別のモデルとして配備する必要があるとします。これは、セキュリティ上の理由、パフォーマンス、スケーラビリティ、あるいはあなたのチームが多くの外部顧客にサービスを提供しており、各顧客が共有機能と特定の機能の両方を含む独自のモデルのコピーを必要とするためかもしれません。

異なるバージョンごとに1つの開発ブランチを維持する代わりに、ここで紹介する手法では、デプロイ時にモデルをどのように分割するかを示すメタデータを使用して、1つのモデルだけを維持できます。

## パースペクティブの活用

考え方は非常にシンプルです。デプロイする必要のあるターゲットモデルの数に対応する数の新しいパースペクティブをモデルに追加することから始めます。これらのパースペクティブは、ユーザー指向のパースペクティブと区別するために、一貫した方法で接頭辞を付けることを確認します。

![image](https://user-images.githubusercontent.com/8976200/43960154-6b637042-9cb1-11e8-906b-6671bbb9558e.png)

ここでは、パースペクティブ名のプレフィックスとして ``$`` 記号を使用しています。後で、これらのパースペクティブがどのようにモデルから取り除かれ、エンドユーザーがそれらを見ることがないようにするのかを見ます。これらはモデル開発者のみが使用します。

あとは、個々のモデルで必要なすべてのオブジェクトを、これらのパースペクティブに追加するだけです。モデルが必要なオブジェクトを含んでいることを確認するには、Tabular EditorのPerspectiveドロップダウンを使用します。ここに、すべての依存関係がパースペクティブにも含まれていることを確認するために使用できる便利なスクリプトがあります。

```csharp
// Look through all hierarchies in the current perspective:
foreach(var h in Model.AllHierarchies.Where(h => h.InPerspective[Selected.Perspective]))
{
    // Make sure columns used in hierarchy levels are included in the perspective:
    foreach(var level in h.Levels) {
        level.Column.InPerspective[Selected.Perspective] = true;
    }
}

// Loop through all measures and columns in the current perspective:
foreach(var obj in Model.AllMeasures.Cast<ITabularPerspectiveObject>()
    .Concat(Model.AllColumns).Where(m => m.InPerspective[Selected.Perspective])
    .OfType<IDaxDependantObject>().ToList())
{
    // Loop through all objects that the current object depends on:
    foreach(var dep in obj.DependsOn.Deep())
    {
        // Include columns, measure and table dependencies:
        var columnDep = dep as Column; if(columnDep != null) columnDep.InPerspective[Selected.Perspective] = true;
        var measureDep = dep as Measure; if(measureDep != null) measureDep.InPerspective[Selected.Perspective] = true;
        var tableDep = dep as Table; if(tableDep != null) tableDep.InPerspective[Selected.Perspective] = true;
    }    
}

// Look through all columns that have a SortByColumn in the current perspective:
foreach(var c in Model.AllColumns.Where(c => c.InPerspective[Selected.Perspective] && c.SortByColumn != null))
{
    c.SortByColumn.InPerspective[Selected.Perspective] = true;   
}
```

**説明:** まず、スクリプトは現在のパースペクティブ（画面上部のドロップダウンで現在選択されているパースペクティブ）のすべての階層をループします。そのような階層ごとに、階層レベルとして使用されるすべての列がパースペクティブに表示されることを確認します。次に、スクリプトは、現在のパースペクティブのすべての列とメジャーをループします。これらのオブジェクトのそれぞれについて、メジャー、列、またはテーブル参照の形式をとるすべての DAX 依存関係もパースペクティブに含まれます。DISTINCTCOUNT('Customer'[CustomerId])` などの式は、[CustomerId]列自体と 'Customer' テーブルの両方に依存関係があるものとしてTabular Editorが扱うため、結果として 'Customer' テーブルのすべての列がパースペクティブに含まれることを注意してください。最後に、スクリプトは、「Sort By」列として使用されている列も含まれるようにします。

このスクリプトは、今後簡単に呼び出せるよう、モデルレベルのカスタムアクションとして保存しておくことをオススメします。

ちなみに、パースペクティブのコピーを作成したい場合は、すでにUIから行うことができます。エクスプローラツリーで「パースペクティブ」ノードをクリックし、プロパティグリッドの省略ボタンをクリックします。

![image](https://user-images.githubusercontent.com/8976200/44028910-c7ffab80-9efb-11e8-813a-5b0f5c137bab.png)

パースペクティブの作成と削除、および既存のパースペクティブのクローンを作成するためのダイアログが表示されます。

![image](https://user-images.githubusercontent.com/8976200/44028953-f13c91ca-9efb-11e8-936a-1f0e1d4eb93f.png)

これを補足するために、少しきれいにする必要がある場合に備えて、パースペクティブからすべての不可視オブジェクトと未使用オブジェクトを削除するスクリプトを紹介します。

```csharp
// 現在のパースペクティブのすべての列をループします。
foreach(var c in Model.AllColumns.Where(c => c.InPerspective[Selected.Perspective])) {
    if(
        //カラムが非表示の場合（または親テーブルが非表示の場合）。
        (c.IsHidden || c.Table.IsHidden) 

        // また、どのようなリレーションでも使用しない:
        && !c.UsedInRelationships.Any()
        
        // また、パースペクティブの他の列のSortByColumnとして使用されることはありません。
        && !c.UsedInSortBy.Any(sb => !sb.IsHidden && sb.InPerspective[Selected.Perspective])
        
        // そして、パースペクティブのどの階層にも使用されていない。
        && !c.UsedInHierarchies.Any(h => h.InPerspective[Selected.Perspective])
        
        // また、パースペクティブ内の他の可視オブジェクトのDAX式では参照されない。
        && !c.ReferencedBy.Deep().OfType<ITabularPerspectiveObject>()
            .Any(obj => obj.InPerspective[Selected.Perspective] && !(obj as IHideableObject).IsHidden)
            
        // そして、どの役割からも参照されない。
        && !c.ReferencedBy.Roles.Any()    )
    {
        // 上記の全てに該当する場合、その列は現在のパースペクティブから削除することができます。
        c.InPerspective[Selected.Perspective] = false; 
    }
}

// 現在の視点のすべてのメジャーをループします。
foreach(var m in Model.AllMeasures.Where(m => m.InPerspective[Selected.Perspective])) {
    if(
        // メジャーが非表示である場合 (または、親テーブルが非表示である場合)。
        (m.IsHidden || m.Table.IsHidden) 

        // また、パースペクティブ内の他の可視オブジェクトのDAX式では参照されない。
        && !m.ReferencedBy.Deep().OfType<ITabularPerspectiveObject>()
            .Any(obj => obj.InPerspective[Selected.Perspective] && !(obj as IHideableObject).IsHidden)
    )
    {
        // 上記の全てに該当する場合、その列は現在のパースペクティブから削除することができます。
        m.InPerspective[Selected.Perspective] = false; 
    }
}
```

**説明** このスクリプトは、まず、現在選択されているパースペクティブのすべての列をループします。次のすべてが真である場合にのみ、パースペクティブから列を削除します。

* 列が非表示（または列の存在するテーブルが非表示）である
* 列はリレーションシップに関与していない
* 列は、パースペクティブ内の他の可視列の SortByColumn として使用されていない
* 列はパースペクティブ内の階層のレベルとして使用されていない
* 列はパースペクティブ内の他の可視オブジェクトの DAX 式で直接的または間接的に参照されていない
* 列は行レベルのフィルター式では使用されていない。

メジャーについても同様ですが、以下の基準を満たすメジャーのみを削除するように簡略化しています。

* メジャーが非表示である (または、メジャーの存在するテーブルが非表示である）
* メジャーが、パースペクティブ内の他の可視オブジェクトのDAX式で直接的または間接的に参照されていない。

もしあなたがモデルの開発に携わっている開発者チームであれば、すでにTabular Editorsの「フォルダーに保存」機能（/Advanced-features#folder-serialization）とGitなどのソース管理環境を使っていることでしょう。ファイル」→「環境設定」→「フォルダーに保存」で「オブジェクトごとにパースペクティブをシリアライズする」オプションを必ずチェックし、パースペクティブ定義で大量のマージ競合が発生しないようにしてください。
![image](https://user-images.githubusercontent.com/8976200/44029969-935e0efe-9eff-11e8-93de-c1223f7ebe7f.png)

## よりきめ細かい制御を可能にする

もうお分かりかと思いますが、スクリプトを使用して、固定された開発者パースペクティブごとに1つのバージョンのモデルを作成する予定です。スクリプトは、指定された開発者パースペクティブに含まれないすべてのオブジェクトをモデルから削除するだけです。しかし、その前に、処理しなければならない状況がいくつかあります。

### 非主観的（non-perspective）なオブジェクトを制御する

パースペクティブ、データソース、ロールなどの一部のオブジェクトは、パースペクティブ自体に含まれることも除外されることもありませんが、それらのどのモデルのバージョンに属するべきかを指定する必要があります。この場合、アノテーションを使用します。たとえば、Adventure Worksのモデルに戻ると、「在庫」と「インターネット運用」のパースペクティブは「$InternetModel」と「$ManagementModel」に、「Reseller Operation」は「$ResellerModel」と「$ManagementModel」に表示させることができます。
そこで、3つのオリジナル視点それぞれに「DevPerspectives」という新しいアノテーションを追加し、開発者視点の名前をカンマ区切りの文字列として提供することにしましょう。

![image](https://user-images.githubusercontent.com/8976200/44032304-01bdcc70-9f07-11e8-9b28-db0912ea1ade.png)

新しい *user* パースペクティブをモデルに追加するときは、同じアノテーションを追加し、*user* パースペクティブを含めたい開発者パースペクティブの名前を指定するのを忘れないようにしてください。後で最終的なモデルのバージョンをスクリプト化する際に、これらのアノテーションの情報を使用して、必要なパースペクティブを含めることになります。データ・ソースとロールについても、同じことができます。

### オブジェクトのメタデータを制御する

また、同じメジャーでも、異なるモデルのバージョン間で微妙に異なる式やフォーマット文字列を持つべき状況もあるでしょう。この場合も、アノテーションを使用して開発者の視点ごとにメタデータを提供し、最終的なモデルをスクリプトアウトするときにメタデータを適用できます。

すべてのオブジェクトプロパティをテキストにシリアライズするもっとも簡単な方法は、おそらく [ExportProperties](/Useful-script-snippets#export-object-properties-to-a-file) スクリプト関数を使う方法でしょう。しかし、この使用例では少しやりすぎなので、アノテーションとして保存したいプロパティを直接指定することにしましょう。以下のスクリプトを作成します。

```csharp
foreach(var m in Selected.Measures) { 
    m.SetAnnotation(Selected.Perspective.Name + "_Expression", m.Expression);
    m.SetAnnotation(Selected.Perspective.Name + "_FormatString", m.FormatString);
    m.SetAnnotation(Selected.Perspective.Name + "_Description", m.Description);
}
```

そして、「メタデータをアノテーションとして保存する」という名前のカスタムアクションとして保存します。

![image](https://user-images.githubusercontent.com/8976200/44033695-7a754482-9f0b-11e8-937b-0bc0987ce7cb.png)

同様に、以下のスクリプトを「Load Metadata from Annotations」というカスタムアクションとして保存します。

```csharp
foreach(Measure m in Selected.Measures) { 
    var expr = m.GetAnnotation(Selected.Perspective.Name + "_Expression"); if(expr == null) continue;
    m.Expression = expr;
    m.FormatString = m.GetAnnotation(Selected.Perspective.Name + "_FormatString");
    m.Description = m.GetAnnotation(Selected.Perspective.Name + "_Description");
}
```

このアイデアは、開発者の視点ごとに、異なるバージョンを維持したいプロパティのために1つのアノテーションを作成することです。スクリプトで示した以外のプロパティ（Expression、FormatString、Description）を個別に管理する必要がある場合は、スクリプトに追加するだけでよい。他のオブジェクト・タイプでも同じことができますが、メジャーや計算列、パーティション（モデルのバージョンごとに異なるクエリ式を管理する場合など）以外では、おそらく意味がないでしょう。

新しいカスタムアクションを使用して、モデルバージョン固有の変更を開発者パースペクティブに適用します（または、手作業でアノテーションを追加します）。たとえば、Adventure Worksのサンプルでは[Day Count]メジャーに $ResellerModelパースペクティブで異なる式を持たせたいので、メジャーに変更を適用し、ドロップダウンで「$ResellerModel」パースペクティブを選択した状態で「アノテーションとしてメタデータを保存」アクションを呼び出します。

![image](https://user-images.githubusercontent.com/8976200/44033944-3104e414-9f0c-11e8-9f06-396bf85a0e4f.png)

上記のスクリーンショットでは、各開発者パースペクティブに対して3つのアノテーションを作成しています。しかし、実際には、プロパティがネイティブの値と異なる開発者パースペクティブに対してのみ、これらのアノテーションを作成する必要があります。

## パーティションクエリーの変更

同様の手法で、異なるバージョン間のパーティションクエリに変更を加えることができます。たとえば、あるパーティションクエリーの `WHERE` 基準をバージョンによって変えたい場合です。まず、*table* オブジェクトに新しいアノテーションを作成し、各バージョンでパーティションが使用する基本SQLクエリを指定することから始めてみましょう。たとえば、3つのバージョンのうち2つのバージョンで、Productテーブルに含まれるレコードを制限したい場合です。

![image](https://user-images.githubusercontent.com/8976200/44736562-69221580-aaa4-11e8-82ee-88388015d30d.png)

複数のパーティションがあるテーブルの場合、WHERE条件を「プレースホルダー」で指定し、あとで置き換える。

![image](https://user-images.githubusercontent.com/8976200/44737015-b3f05d00-aaa5-11e8-9bad-cadd5b4dae35.png)

各パーティション内のプレースホルダー値を定義します（注意：UIでパーティションアノテーションを編集するには、[Tabular Editor v. 2.7.3](https://github.com/otykier/TabularEditor/releases/tag/2.7.3) 以降を使用する必要があります）。

![image](https://user-images.githubusercontent.com/8976200/44737199-2a8d5a80-aaa6-11e8-8813-8189b593da98.png)

動的パーティション分割のシナリオでは、新しいパーティションを作成するとき、使用するスクリプトに、これらの注釈を含めることを忘れないでください。次のセクションでは、デプロイ時にこれらのプレースホルダー値を適用する方法について説明します。

## 異なるバージョンのデプロイ

最後に、モデルを3つの異なるバージョンとしてデプロイする準備が整いました。残念ながら、Tabular EditorのデプロイメントウィザードUIでは、作成したパースペクティブやアノテーションに基づいてモデルを分割することができません。したがって、モデルを特定のバージョンに分解する追加のスクリプトを作成する必要があります。このスクリプトは、コマンドラインのデプロイの一部として実行することができ、デプロイプロセス全体をコマンドファイル、PowerShell実行ファイル、あるいはビルド/自動デプロイプロセスに統合できます。

必要なスクリプトは、次のようなものです。開発者の視点ごとに1つのスクリプトを作成することを考えます。スクリプトをテキストファイルとして保存し、`ResellerModel.cs`のような名前をつけます。

```csharp
var version = "`$`ResellerModel"; // TODO: Replace this with the name of your developer perspective

// パースペクティブの一部でないテーブル、メジャー、列、階層を削除します。
foreach(var t in Model.Tables.ToList()) {
    if(!t.InPerspective[version]) t.Delete();
    else {
        foreach(var m in t.Measures.ToList()) if(!m.InPerspective[version]) m.Delete();   
        foreach(var c in t.Columns.ToList()) if(!c.InPerspective[version]) c.Delete();
        foreach(var h in t.Hierarchies.ToList()) if(!h.InPerspective[version]) h.Delete();
    }
}

// アノテーションに基づくユーザー視点と、すべての開発者視点を削除します。
foreach(var p in Model.Perspectives.ToList()) {
    if(p.Name.StartsWith("`$`")) p.Delete();

    // DevPerspectives "アノテーションを持たない他のすべてのパースペクティブを保持し、同時に
    // アノテーションで<version>が指定されていない場合は、アノテーションを持つもの。
    if(p.GetAnnotation("DevPerspectives") != null && !p.GetAnnotation("DevPerspectives").Contains(version)) 
        p.Delete();
}

// アノテーションに基づきデータソースを削除します。
foreach(var ds in Model.DataSources.ToList()) {
    if(ds.GetAnnotation("DevPerspectives") == null) continue;
    if(!ds.GetAnnotation("DevPerspectives").Contains(version)) ds.Delete();
}

// アノテーションに基づきロールを削除する。
foreach(var r in Model.Roles.ToList()) {
    if(r.GetAnnotation("DevPerspectives") == null) continue;
    if(!r.GetAnnotation("DevPerspectives").Contains(version)) r.Delete();
}

// アノテーションに基づくメジャーの修正。
foreach(Measure m in Model.AllMeasures) {
    var expr = m.GetAnnotation(version + "_Expression"); if(expr == null) continue;
    m.Expression = expr;
    m.FormatString = m.GetAnnotation(version + "_FormatString");
    m.Description = m.GetAnnotation(version + "_Description");    
}

// アノテーションに応じたクエリの分割を設定する。
foreach(Table t in Model.Tables) {
    var queryWithPlaceholders = t.GetAnnotation(version + "_PartitionQuery"); if(queryWithPlaceholders == null) continue;
    
    // このテーブルのすべてのパーティションをループします。
    foreach(Partition p in t.Partitions) {
        
        var finalQuery = queryWithPlaceholders;

        // プレースホルダー値をすべて置き換える。
        foreach(var placeholder in p.Annotations.Keys) {
            finalQuery = finalQuery.Replace("%" + placeholder + "%", p.GetAnnotation(placeholder));
        }

        p.Query = finalQuery;
    }
}

// TODO: アノテーションに基づき、他のオブジェクトを修正する（該当する場合）...
```

**Explanation:** まず、スクリプトの1行目で定義されたパースペクティブの一部ではない、すべてのテーブル、列、メジャー、および階層を削除します。次に、前述の「DevPerspectives」アノテーションを適用した可能性のある追加オブジェクトと、すべての開発者パースペクティ ブそのものを削除します。その後、アノテーションに基づくメジャー式、フォーマット文字列、説明文の変更があれば、それを適用します。最後に、アノテーションで定義されたパーティションクエリーを適用し（ある場合）、プレースホルダーの値をアノテーションされた値に置き換えます（ある場合）。

このスクリプトに直接特定のモデルの変更を追加することもできますが、この演習の要点は、Tabular Editorの中から直接複数のモデルを管理する方法です。上記のスクリプトは、どのバージョンをデプロイする場合でも同じです（もちろん、1行目を除きます）。

最後に、以下の[コマンドライン構文](/Command-line-Options)を使って、Model.bimファイルをロードし、スクリプトを実行し、変更したモデルを一度にデプロイできます。

```sh
start /wait /d "c:\Program Files (x86)\Tabular Editor" TabularEditor.exe Model.bim -S ResellerModel.cs -D localhost AdventureWorksReseller -O -R
```

インターネット版や管理版を導入する場合も同様に、対応するスクリプトを用意する必要があります。

```sh
start /wait /d "c:\Program Files (x86)\Tabular Editor" TabularEditor.exe Model.bim -S InternetModel.cs -D localhost AdventureWorksInternet -O -R
start /wait /d "c:\Program Files (x86)\Tabular Editor" TabularEditor.exe Model.bim -S ManagementModel.cs -D localhost AdventureWorksManagement -O -R
```

これは、Model.bimファイル（または "Save to Folder "機能を使用している場合はDatabase.jsonファイル）のディレクトリ内でコマンドラインを実行していることを想定しています。-Sスイッチは与えられたスクリプトをモデル適用するようTabular Editorに指示し、-Dスイッチはデプロイを実行します。-Oスイッチで既存のデータベースを同名で上書きし、-Rスイッチでターゲットデータベースのロールも上書きすることを指示します。

## マスターモデル処理

処理専用のサーバーがあり、大量のデータが個々のモデル間で重複している場合、データを分割する前に、まずマスターモデルに処理することが理にかなっている場合があります。このようにすれば、同じデータを何度も個別のモデルに処理することを避けることができます。**ただし、[このセクション](/Master-model-pattern#altering-partition-queries)で示したように、バージョン間でパーティションクエリが変更されたテーブルを処理しないことが前提になります**。

1. (オプション - メタデータの変更があった場合）マスターモデルを処理サーバーにデプロイする
2. マスターモデルに対して必要な処理を行う（バージョン固有のパーティションクエリを持つテーブルは処理しない）
3. マスターモデルを各個別モデルに同期させ、同期後に上記のコマンドを使用して個別モデルをストリップダウンし、必要に応じてProcessRecalcを実行します。
4. （オプション）個別モデルで、バージョン固有のパーティションクエリを持つテーブルを処理する。

## ヒントとコツ

カスタムアノテーションを多用するようになると、特定のアノテーションを持つすべてのオブジェクトをリストアップしたい状況が発生することがあります。そこで、Filter-BoxのDynamic LINQ式が役に立ちます。

まず最初に、"$InternetModel_Expression" という名前のアノテーションを追加したすべてのオブジェクトを見つけたい場合を考えてみましょう。Filterテキストボックスに次のように入力し、ENTERを押してください。

```
:GetAnnotation("`$`InternetModel_Expression")<>null
```

また、"_Expression "という言葉で終わる注釈を持つすべてのオブジェクトを見つけたい場合は、次のようにします。

```
:GetAnnotations().Any(EndsWith("_Expression"))
```

これらの関数は大文字と小文字を区別するので、アノテーションが小文字で書かれていた場合、上記のフィルタでは捕捉できないことに注意してください。

また、アノテーションが特定の値を持つオブジェクトを検索することもできます。

```
:GetAnnotation(`$`InternetModel_Description).Contains("TODO")
```

## 結論

ここで説明したテクニックは、Calendarテーブルやその他の共通ディメンションなど、多くの共有機能を持つ多くの類似したモデルを管理する際に非常に役に立ちます。使用されるスクリプトはTabular Editorのカスタムアクションとしてきれいに再利用でき、実際のデプロイはさまざまな方法で自動化できます。
