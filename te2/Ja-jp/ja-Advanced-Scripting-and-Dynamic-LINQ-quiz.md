# あなたはTabular Editorのプロですか？

Tabular EditorのAdvanced ScriptingとDynamic LINQフィルター式についての知識をテストしてください。ここにある質問はすべて、たった1行のコードで答えられるかもしれません。

これらの機能をはじめて使う場合は、ここで紹介するソリューション（C#版とDynamic LINQ版の両方）に、これらの機能がどのように動作するかについて多くの有用な情報が掲載されていますので、ぜひチェックしてみてください。

***

#### Question #1) メジャーの総数

* モデルのメジャー数はどのように求めますか？

<details><summary><i>C# スクリプト ソリューション</i></summary> <pre><code>Model.AllMeasures.Count().Output();</code></pre> <b>説明</b> <code>Model</code> オブジェクトは <a href="https://docs.microsoft.com/en-us/sql/analysis-services/tabular-model-programming-compatibility-level-1200/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=sql-server-2017#tabular-object-model-hierarchy">TOM tree</a> のルートに相当します。<a href="https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices?redirectedfrom=MSDN&view=sqlserver-2016">API documentation</a> にあるプロパティのほとんどをサポートし、Tabular Editor 内でのみ利用可能ないくつかの追加プロパティとメソッドを備えています。<code>AllMeasures</code> プロパティは、これらの追加プロパティの 1 つで、利便性を高めるために追加されました。これは、モデル内のすべてのテーブルにわたるすべてのメジャーのコレクションを返すだけです。すべてのコレクション (正確には <i>enumerables</i>) は、強力な <a href="https://docs.microsoft.com/en-us/dotnet/api/system.linq.enumerable?view=netframework-4.7.2#methods">.NET LINQ メソッド</a> をサポートしています。<code>Count()</code> はそのようなメソッドの 1 つで、コレクション内の要素の数を単に整数値として返します。それが手に入れば、あとは <code>Output()</code> するだけです。<br/><br/></details>

<details><summary><i>Dynamic LINQ solution</i></summary>
<pre><code>:ObjectType="Measure"</code></pre> <b>説明:</b> Filterテキストボックスの最初の文字として:'を置くと、動的LINQフィルタリングを有効にします。これが意味するところは、TabularエディターはTOMツリー内のすべてのオブジェクトに対して':'文字の後の式を評価し、式が真と評価されるオブジェクトのみを返すということです。Filterテキストボックスに上記の式を入れると、Tabular Editorは<code>ObjectType</code>プロパティが「Measure」であるすべてのオブジェクトを表示するようになります。画面下部の検索結果数には、合計でいくつのメジャーがあるのかが表示されます。</details>

***

#### Question #2) 式に "TODO "を含むすべてのメジャーを検索する

* Expression プロパティ内に "TODO" という単語を含むすべてのメジャーを検索する最も簡単な方法は何ですか？

<details><summary><i>C#スクリプトソリューション</i></summary> <pre><code>Model.AllMeasures.Where(m => m.Expression.Contains("TODO")).Output();</code></pre> <b>説明：</b>このスクリプトの最初の部分は質問1と同じものです。<code>Where(x =&gt; y)</code> は、いわゆる<i>述語</i>に基づいて先行するコレクションをフィルタリングする、もう一つの.NET LINQメソッドです。述語は、特別なC#ラムダ記法 <code>x =&gt; y</code> を使って表現されています。矢印の左側で、好きな名前の変数を宣言します。矢印の右側の式は、コレクション内のすべてのオブジェクトに対して評価され、左側の変数を使用して個々のオブジェクトを表します。この式は、ブーリアン値（真または偽）として評価される有効なC#式であれば、どのようなものでも使用できます。したがって、<code>Where</code>メソッドは、ラムダ式が真と評価されるオブジェクトだけを返すように、コレクションを単純にフィルタリングします。したがって、上記の例では、モデルの個々のメジャーを表す変数の名前として <code>m</code> を使用することを決定しました。しかし、私たちは <code>Expression</code> プロパティが <code>Contains</code> である単語 "TODO" を持つメジャーだけを保持したいのです。理にかなっていますか？<br/><br/><br/>
</details>

<details><summary><i>ダイナミックLINQソリューション</i></summary> <pre><code>:ObjectType="Measure" and Expression.Contains("TODO")</code></pre> <b>説明：</b>このダイナミックLINQ式の最初の部分は、質問1と同じです。Dynamic LINQでは、<a href="https://github.com/kahanu/System.Linq.Dynamic/wiki/Dynamic-Expressions#operators"><code>and</code>や<code>or</code>などのさまざまな演算子を使って、複雑なロジックを表現することができます。式の後半部分は、メジャーを表す変数を宣言していないことを除けば、上で使用したC#のLambda式と似ていることに注目してください。Dynamic LINQはTOMツリー内のすべてのオブジェクトに対して評価されるので、式にプロパティ名やメソッド名を追加すると、暗黙のうちに現在のオブジェクトに対して評価されることになります。オブジェクトの種類によってプロパティが異なるため、Filter ボックスに無効な式が含まれていてもエラーは発生しません。ただし、<a href="/Best-Practice-Analyzer">Best Practice Analyzer</a> 内で Dynamic LINQ 式を記述する場合、選択したオブジェクト タイプに存在しないプロパティまたはメソッドにアクセスしようとすると、エラーが表示されるようになりました。
</details>

***

#### Question #3) ダイレクトメジャー依存の数を数える

* 現在選択されているメジャーを直接参照しているメジャーの数を知るにはどうしたらよいのでしょうか。"依存関係の表示" ダイアログに対して、いつでも答えを確認できます。

<details><summary><i>C# スクリプト ソリューション</i></summary> <pre><code>Selected.Measure.ReferencedBy.Measures.Count().Output();</code></pre> <b>説明:</b> <code>Selected.Measure</code> は、エクスプローラ ツリーの現在選択中のメジャーを指します。DAX を通して参照できるすべてのオブジェクト (メジャー、テーブル、列、KPI) は、<code>ReferencedBy</code> プロパティを持ち、これは、前者を直接参照するオブジェクトの特別なコレクションです。LINQ メソッド <code>.OfType&lt;Measure&gt;()</code> を使用して、コレクションをメジャーだけに絞り込むこともできますが、この特定のコレクションには、これを実行する便利なプロパティのセットが含まれています。そのうちの 1 つが、<code>Measures</code> です。<br/><br/><br/> このコレクションには、これを行う便利なプロパティが含まれています。
</details>

<details><summary><i>動的 LINQ ソリューション</i></summary> <pre><code>:ObjectType="Measure" and DependsOn.Measures.Any(Name="Reseller Total Sales")</code></pre> <b>説明：</b>現在の選択に基づいて動的 LINQ フィルター式を作成することができないため、代わりにこの例で特定のメジャーを考慮します、 [Reseller Total Sales] です。この例では、"Reseller Total Sales" という名前のメジャーに直接依存しているすべてのオブジェクトが返されます。ここで "ReferencedBy" の代わりに "DependsOn" を使用しているのは、検索フィルタ式がモデル内のすべてのオブジェクトに対して評価されるためです。これは、C# スクリプトで行っていることとは逆で、特定のメジャーに対するハンドルを既に持っており、そのメジャーを参照するメジャーのリストを取得する場合です。
</details>

***

#### Question #4) メジャー依存の数を再帰的に数える

* もっと深く考えてみましょう。現在選択されているメジャーに再帰的に依存するメジャーの数をどのように取得するのでしょうか。

<details><summary><i>C# スクリプト ソリューション</i></summary> <pre><code>Selected.Measure.ReferencedBy.Deep().OfType&lt;Measure&gt;().Count().Output();</code></pre> ここで、依存関係ツリーを再帰的にトラバースし、直接または他のオブジェクトを介して間接的に元のメジャーを参照するすべてのオブジェクトのコレクションを取得する <code>Deep()</code> メソッドを追加しました。計算された列や RLS 式などが表示されないように、このコレクションを手動で "メジャー" タイプのオブジェクトにフィルタリングする必要があります。<br/><br/> ところで、カウントだけでなく、これらのメジャーのリストを表示したい場合は、次のように記述できます。
<pre><code>Selected.Measure.ReferencedBy.Deep().OfType<Measure>().Output();</code></pre> <pre>Selection.Measure.ReferencedBy.Deep().Output();

</details>

<details>
<summary><i>動的 LINQ ソリューション</i></summary> <pre><code>:ObjectType="Measure" and DependsOn.Deep().Any(Name="Reseller Total Sales")</code></pre> <b>説明：</b> C# を使用して呼び出すことができるすべてのメソッドは、動的 LINQ を使用して呼び出される可能性もあります。つまり、上で行ったように、<code>Deep()</code>メソッドを呼び出して依存関係ツリーを上方に再帰的に走査し、「Reseller Total Sales」という名前のオブジェクトに依存関係を持つすべてのオブジェクトを見つけます。厳密に言うと、これは上記の C# 式と全く同じではありません。なぜなら、"Reseller Total Sales" という名前の非メジャー型オブジェクトも正にヒットしてしまうからです。これを回避するには、メジャーのみを考慮することを明示的に記述するか... <pre><code>:DependsOn.Deep().Any(Name="Reseller Total Sales" and ObjectType="Measure")</code></pre> ...を使用するか。または、<code>DaxObjectFullName</code> プロパティを使用してヒットを確認できます (列名は完全修飾され、メジャーはモデル全体で一意に命名される必要があります): <pre><code>:DependsOn.Deep().Any(DaxObjectFullName="[Reseller Total Sales]")</code></pre>
</details>

***

#### Question #5) 関連するディメンジョンをすべてリストアップ

* ファクト・テーブル`'Reseller Sales'`がある場合、関連するすべてのディメンジョン・テーブルのリストを取得するにはどうすればよいですか?

<details><summary><i>C# script solution</i></summary>
<pre><code>var t = Model.Tables["Reseller Sales"];<br/>
t.UsedInRelationships.Where(r => r.FromTable == t).Select(r => r.ToTable).Output();</code></pre>
<b>説明:</b> さて、これは少しトリッキーであり、与えられたテーブルを保持するために変数を使用したため、1 行ではなく 2 行のコードで終わっていることを認めます。素朴なアプローチは、単に <code>t.RelatedTables.Output();</code> と書くことですが、質問では関連する <i>dimension</i> テーブルのみを出力するように明確に尋ねられたため、与えられたテーブルが「From」側にあるそれらの関係のみを考慮する必要があります。これが <code>t.UsedInRelationships.Where(r => r.FromTable == t)</code> の目的です。しかし、これらのリレーションシップが指す<i>テーブル</i>のリストが欲しいので、各リレーションシップの`ToTable`プロパティを取得するために、このリストを投影する必要があります。これはまさに <code>.Select(r => r.ToTable)</code> が行うことです。お分かりいただけたでしょうか？では、以下のDynamic LINQソリューションをご覧ください。<br/><br/></details>

<details><summary><i>Dynamic LINQ solution</i></summary>
<pre><code>:UsedInRelationships.Any(ToTable=current and FromTable.Name = "Reseller Sales")</code></pre>
<b>Explanation:</b> この式は、モデル内のすべてのオブジェクトに対して評価されることを念頭に置いて、左から右へと読んでいきましょう。<code>UsedInRelationships</code> は、現在のオブジェクトが参加しているリレーションシップのリストです。この時点で、テーブルやカラムオブジェクトでないものは除外しました。なぜなら、これらは<code>UsedInRelationships</code>プロパティを持つ唯一のものだからです。ディメンジョン・テーブルでないものをフィルタリングするために、問題のテーブルから <i> 現在のオブジェクトへの</i>指し示す関係のみを考慮したいと思います。<code>.Any( ... )</code> は、少なくとも1つのリレーションシップが条件を満たしていれば、trueと評価されます。<code>ToTable=current and FromTable.Name = "Reseller Total Sales"</code> という条件を満たす場合、真と評価されます。特別なキーワード<code>current</code>は、評価されている現在のオブジェクトを指します。我々はこれをリレーションシップの<code>ToTable</code>プロパティと同一視しているため、このプロパティはテーブル型のみであるため、検索結果から列を除外しているのです。<code>FromTable.Name = ...</code> は自明です。
</details>

***

#### Question #6) 名前に "Total "と "Amount "が含まれるオブジェクトをすべて探す

![image](https://user-images.githubusercontent.com/8976200/44931220-c2dd4680-ad15-11e8-9e52-29ec07f1edb6.png)

Hint: そのための正規表現は次のようになります。 `Total.*Amount`

<details><summary><i>C# script solution</i></summary>
<pre><code>Model.AllMeasures.Where(m => System.Text.RegularExpressions.Regex.IsMatch(m.Name, "Total.*Amount")).Output();</code></pre>
<b>Explanation:</b> これは、Advanced Scriptタブで行うには、実はかなり面倒です。厳密に言うと、1 つのビューですべてを表示する場合、実際にはすべてのコレクション (Tables, AllMeasures, AllColumns, AllHierarchies, ...) を検索して、その結果を連結する必要があります。さらに、<code>System.Text.RegularExpressions</code> 名前空間はデフォルトでスコープ内にないため、このスクリプトはそれほどタイピングに適したものではありません。代わりに Dynamic LINQ ソリューションをチェックアウトしてください。</details>

<details><summary><i>Dynamic LINQ solution</i></summary>
<pre><code>:Regex.IsMatch(Name, "Total.*Amount")</code></pre>
きれいでしょう？
</details>

***

#### Question #7) 6と同じですが、大文字・小文字を区別して検索します。

<details><summary><i>C# script solution</i></summary>
<pre><code>Model.AllMeasures.Where(m => System.Text.RegularExpressions.Regex.IsMatch(m.Name, "Total.*Amount", RegexOptions.IgnoreCase)).Output();</code></pre></details>

<details><summary><i>Dynamic LINQ solution</i></summary>
<pre><code>:Regex.IsMatch(Name, "Total.*Amount", "IgnoreCase")</code></pre></details>

#### 今後もご期待ください
