# FormatDaxの非推奨

Tabular Editorで利用可能な[ヘルパーメソッド](/Advanced-Scripting.md#helper-methods)の1つである `FormatDax` メソッドはTabular Editor 2.13.0のリリースで非推奨とされました。

非推奨になった理由は、https://www.daxformatter.com/ のウェブサービスで、複数のリクエストを連続して行うと負荷が高くなり、その結果、ウェブサービス側で問題が発生するようになったからです。これは、`FormatDax`メソッドがスクリプト内で呼び出されるたびにウェブリクエストを実行するためで、多くの人が以下のようなスクリプトを使用してきました。

**やめてくれ！**

```csharp
foreach(var m in Model.AllMeasures)
{
    // DON'T DO THIS
    m.Expression = FormatDax(m.Expression);
}
```

これは数十のメジャーを持つ小さなモデルでは問題ありませんが、www.daxformatter.comのトラフィックを見ると、上記のようなスクリプトが数千のメジャーを持つ複数のモデルにわたって、一日に数回でも実行されていることがわかります。

この問題に対処するため、Tabular Editor 2.13.0では、上記の構文で `FormatDax` が連続して3回以上呼び出されると警告を表示するようにしました。さらに、それ以降の呼び出しは、各呼び出しの間に5秒の遅延を設けて、スロットルされます。

## 代替構文

Tabular Editor 2.13.0では、FormatDaxを呼び出す方法が2種類導入されています。上記のスクリプトは、以下のどちらかに書き換えることができます。

```csharp
foreach(var m in Model.AllMeasures)
{
    m.FormatDax();
}
```

...いや、単に...:

```csharp
Model.AllMeasures.FormatDax();
```

これらのアプローチは、すべての www.daxformatter.com の呼び出しを一回のリクエストにまとめます。お好みでグローバルメソッドの構文も使用できます。

```csharp
foreach(var m in Model.AllMeasures)
{
    FormatDax(m);
}
```

...いや、単に...:

```csharp
FormatDax(Model.AllMeasures);
```

## 詳細はこちら

技術的には、`FormatDax` は2つのオーバーロードされた拡張メソッドとして実装されています。

1) `void FormatDax(this IDaxDependantObject obj)`
2) `void FormatDax(this IEnumerable<IDaxDependantObject> objects, bool shortFormat = false, bool? skipSpaceAfterFunctionName = null)` となります。

上記のオーバーロード#1はスクリプトの実行が完了したとき、あるいは新しい `void CallDaxFormatter()` メソッドの呼び出しが行われたときに、与えられたオブジェクトをフォーマットするためキューに入ります。オーバーロード #2は、単一のWebリクエストで www.daxformatter.com を直ちに呼び出し、列挙可能なすべてのオブジェクトに対してすべてのDAX式をフォーマットします。これらのメソッドのいずれかを、適切と思われる方法で使用できます。

新しいメソッドは、文字列の引数を取らないことに注意してください。このメソッドは、提供されたオブジェクトのすべてのDAXプロパティを考慮してフォーマットします (メジャーの場合はExpressionおよびDetailRowsExpressionプロパティ、KPIの場合はStatusExpression、TargetExpression、およびTrendExpressionなどです）。
