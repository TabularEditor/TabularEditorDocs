# Custom Actions

> [!NOTE]
> この機能は、多次元モデルで利用可能なカスタムアクション機能とは無関係であることに注意してください。

たとえば、`Selected`オブジェクトを使って便利なスクリプトを作成し、エクスプローラツリーの異なるオブジェクトに対して何度もスクリプトを実行できるようにしたいとします。スクリプトを実行したいときに "Play "ボタンを押す代わりに、Tabular Editorではスクリプトをカスタムアクションとして保存できます。

![image](https://user-images.githubusercontent.com/8976200/33581673-0db35ed0-d952-11e7-90cd-e3164e198865.png)

カスタムアクションを保存すると、エクスプローラツリーの右クリックコンテキストメニューから直接利用できるようになり、ツリーで選択したオブジェクトに対して簡単にスクリプトを呼び出すことができます。カスタムアクションは必要な数だけ作成できます。バックスラッシュの使用 (\\) を指定すると、コンテキストメニューの中にサブメニュー構造が作成されます。

![Custom Actions show up directly in the context menu](https://raw.githubusercontent.com/otykier/TabularEditor/master/Documentation/InvokeCustomAction.png)

Custom Actionsは%AppData%LocalTabularEditor内のCustomActions.jsonファイルに保存されます。上記の例では、このファイルの内容は次のようになります。

```json
{
  "Actions": [
    {
      "Name": "Custom Formatting\\Number with 1 decimal",
      "Enabled": "true",
      "Execute": "Selected.Measures.ForEach(m => m.FormatString = \"0.0\";",
      "Tooltip": "Sets the FormatString property to \"0.0\"",
      "ValidContexts": "Measure, Column"
    }
  ]
}
```

見ての通り、`Name` と `Tooltip` はアクションが保存されたときに指定された値を取得します。Execute` は、アクションが呼び出されたときに実行される実際のスクリプトです。CustomActions.jsonファイルに構文エラーがあると、Tabular EditorはすべてのCustom Actionの読み込みを完全にスキップします。したがって、Custom Actionとして保存する前に、Advanced Scripting Editor内でスクリプトを正常に実行できることを確認してください。

`ValidContexts`プロパティは、アクションが利用できるオブジェクトタイプのリストを保持します。ツリーでオブジェクトを選択する際に、`ValidContexts`プロパティに記載されているタイプとは異なるオブジェクトが含まれていると、コンテキストメニューからそのアクションが非表示になります。

## Controlling Action Availability

もし、コンテキストメニューからアクションを呼び出すタイミングをさらにコントロールしたい場合には、`Enabled` プロパティをカスタム式に設定できます。この式は、与えられた選択に対してアクションが利用できるかどうかを示すブール値を返さなければなりません。デフォルトでは、`Enabled` プロパティは "true" という値を持っており、有効なコンテキスト内では常にアクションが有効になることを意味します。このことは、 `Selected` オブジェクトに対して、 `Selected.Measure` や `Selected.Table` のような単数形のオブジェクト参照を使用する際に、現在の選択オブジェクトがそのタイプのオブジェクトを含んでいない場合にはエラーをスローすることになりますので覚えておいてください。このような場合は、 `Enabled` プロパティを使用して、必要なタイプのオブジェクトが1つだけ選択されていることを確認することをオススメします。

```json
{
  "Actions": [
    {
      "Name": "Reset measure name",
      "Enabled": "Selected.Measures.Count == 1",
      "Execute": "Selected.Measure.Name == \"New Measure\"",
      "ValidContexts": "Measure"
    }
  ]
}
```

これにより、ツリーで1つのメジャーが選択されていない限り、コンテキスト・メニュー項目は無効となります。

## Reusing custom actions

リリース2.7では、新しいスクリプトメソッド `CustomAction(...)` が導入され、以前に保存されたカスタムアクションを呼び出すことができるようになりました。このメソッドはスタンドアローンのメソッドとして (`Output(...)` と同様) 使用することもできますし、任意のオブジェクトのセットに対して拡張メソッドとして使用することもできます。

```csharp
// Executes "My custom action" against the current selection:
CustomAction("My custom action");                

// Executes "My custom action" against all tables in the model:
CustomAction(Model.Tables, "My custom action");

// Executes "My custom action" against every measure in the current selection whose name starts with "Sum":
Selected.Measures.Where(m => m.Name.StartsWith("Sum")).CustomAction("My custom action");
```

カスタムアクションの名前は、コンテキストメニューのフォルダー名も含めてフルネームで指定する必要があることに注意してください。

指定した名前のアクションが見つからない場合は、スクリプトを実行するときにエラーが発生します。
